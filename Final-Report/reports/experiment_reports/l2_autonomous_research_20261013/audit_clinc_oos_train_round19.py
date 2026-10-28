"""Aggregate-only audit of the pinned CLINC150 plus/train split.

Only the upstream train parquet is acquired and read. Native out-of-scope rows,
upstream validation/test files, row text, and row identifiers are never emitted.
"""
from __future__ import annotations

import collections
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

import pyarrow.parquet as pq


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
PRIVATE = REPO / "workspaces" / "truongnv" / "pi_guard_pipeline"
TRAINING = PRIVATE / "training_bases"
SOURCE_FILE = TRAINING / "datasets" / "source_audit" / "clinc_oos_round19" / "plus_train.parquet"
ROUND07 = TRAINING / "datasets" / "project_training" / "versions" / "pi_guard_native_reference_round07_20261013_r01"
ROUND18_B = TRAINING / "datasets" / "project_training" / "versions" / "pi_guard_l2_source_heldout_dolly_aug_round18_r01"
VENDOR = TRAINING / "datasets" / "project_training" / "history" / "pi_guard_v8_english_diagnostic_20261012" / "tools" / "_vendor"
REPORT = ROOT / "clinc_oos_train_candidate_audit_round19.json"

REPOSITORY = "clinc/clinc_oos"
REVISION = "155b9c710419136e17307b80d0a13e68cd46b4ec"
CONFIG = "plus"
EXPECTED_FILE_SHA256 = "30188119cf9f86fc9db27e1c22442d091cb5cb0913c9496f945fe11e7a02a28f"
LANGUAGE_MODEL_SHA256 = "f4f4a2c3465ca1f081541037f9cac23021d68151c2f709c55ae5eedfca522963"

PII_PATTERNS = {
    "email": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "us_ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "ipv4": re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b"),
    "credential_assignment": re.compile(r"(?i)\b(?:api[_ -]?key|access[_ -]?token|password|passwd|secret)\s*[:=]\s*[^\s,;]+"),
    "private_key": re.compile(r"(?i)-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "bearer_token": re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]{16,}"),
    "phone_candidate": re.compile(r"(?<!\w)(?:\+?\d[\d .()\-]{8,}\d)(?!\w)"),
}
REVIEW_PATTERNS = {
    "instruction_override": re.compile(r"\b(ignore|disregard|forget|override|bypass)\b.{0,80}\b(instructions?|rules?|system|developer|policy)\b", re.I | re.S),
    "secret_extraction": re.compile(r"\b(reveal|show|print|repeat|extract|disclose)\b.{0,80}\b(system prompt|hidden prompt|secret|api key|password)\b", re.I | re.S),
    "harmful_intent_terms": re.compile(r"\b(make a bomb|build a weapon|steal credentials|write malware|kill someone|self[- ]harm)\b", re.I),
}


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def language_identifier():
    sys.path.insert(0, str(VENDOR))
    from py3langid.langid import LanguageIdentifier, MODEL_FILE
    import py3langid

    model_path = Path(py3langid.__file__).resolve().parent / MODEL_FILE
    if sha_file(model_path) != LANGUAGE_MODEL_SHA256:
        raise ValueError("PINNED_LANGUAGE_MODEL_HASH_MISMATCH")
    return LanguageIdentifier.from_model_file(MODEL_FILE, norm_probs=True)


def package_texts(package: Path, expected_id: str) -> tuple[set[str], str]:
    manifest_path = package / "DATASET_MANIFEST.json"
    raw = manifest_path.read_bytes()
    manifest = json.loads(raw)
    if manifest.get("package_id") != expected_id:
        raise ValueError("UNEXPECTED_PACKAGE_ID")
    texts: set[str] = set()
    for split in ("train", "validation"):
        spec = manifest["partitions"][split]["rows"]
        path = package / spec["path"]
        if sha_file(path) != spec["sha256"]:
            raise ValueError("PACKAGE_PARTITION_HASH_MISMATCH:" + split)
        with path.open("r", encoding="utf-8") as stream:
            for line in stream:
                value = normalize(json.loads(line).get("text", ""))
                if value:
                    texts.add(value)
    return texts, hashlib.sha256(raw).hexdigest()


def main() -> int:
    if sha_file(SOURCE_FILE) != EXPECTED_FILE_SHA256:
        raise ValueError("PINNED_CLINC_TRAIN_HASH_MISMATCH")
    known, round07_hash = package_texts(ROUND07, "pi_guard_l2_native_reference_round07_r01")
    round18, round18_hash = package_texts(ROUND18_B, "pi_guard_l2_source_heldout_dolly_aug_round18_r01")
    known |= round18

    schema = pq.read_schema(SOURCE_FILE)
    feature_meta = json.loads(schema.metadata[b"huggingface"])["info"]["features"]
    class_names = feature_meta["intent"]["names"]
    oos_ids = {index for index, name in enumerate(class_names) if name.casefold() == "oos"}
    if len(class_names) != 151 or len(oos_ids) != 1 or not {"text", "intent"}.issubset(set(schema.names)):
        raise ValueError("UNEXPECTED_CLINC_PLUS_TRAIN_SCHEMA")
    oos_id = next(iter(oos_ids))
    table = pq.read_table(SOURCE_FILE, columns=["text", "intent"])
    identifier = language_identifier()

    counters: collections.Counter[str] = collections.Counter()
    privacy_counts: collections.Counter[str] = collections.Counter()
    language_counts: collections.Counter[str] = collections.Counter()
    language_label_counts: collections.Counter[str] = collections.Counter()
    language_confidence_bins: collections.Counter[str] = collections.Counter()
    review_counts: collections.Counter[str] = collections.Counter()
    per_intent: collections.Counter[int] = collections.Counter()
    seen: set[str] = set()

    for row in table.to_pylist():
        counters["source_train_rows"] += 1
        intent_id = int(row["intent"])
        if intent_id == oos_id:
            counters["native_oos_train_rows_excluded"] += 1
            continue
        counters["native_in_scope_intent_rows"] += 1
        text = row["text"]
        if not isinstance(text, str) or not text.strip():
            counters["empty_or_invalid_in_scope_text"] += 1
            continue
        matched_privacy = [name for name, pattern in PII_PATTERNS.items() if pattern.search(text)]
        if matched_privacy:
            counters["in_scope_privacy_pattern_rows"] += 1
            for name in matched_privacy:
                privacy_counts[name] += 1
            continue
        matched_review = [name for name, pattern in REVIEW_PATTERNS.items() if pattern.search(text)]
        if matched_review:
            counters["in_scope_attack_or_harm_pattern_rows"] += 1
            for name in matched_review:
                review_counts[name] += 1
            continue
        language, confidence = identifier.classify(text)
        confidence = float(confidence)
        language_label_counts[language] += 1
        language_confidence_bins[">=0.95" if confidence >= 0.95 else ">=0.50" if confidence >= 0.50 else "<0.50"] += 1
        if language != "en":
            counters["in_scope_language_not_english_top1"] += 1
            language_counts[language] += 1
            continue
        counters["in_scope_english_top1_private_screened_rows"] += 1
        language_counts["en_top1"] += 1
        key = normalize(text)
        if key in known:
            counters["exact_overlap_with_round07_or_round18"] += 1
            continue
        if key in seen:
            counters["within_clinc_exact_duplicate"] += 1
            continue
        seen.add(key)
        per_intent[intent_id] += 1

    support = sorted(per_intent.values())
    result = {
        "audit_round": 19,
        "repository": REPOSITORY,
        "revision": REVISION,
        "config": CONFIG,
        "upstream_partition": "train only",
        "source_file": "plus/train-00000-of-00001.parquet",
        "source_file_sha256": EXPECTED_FILE_SHA256,
        "source_file_bytes": SOURCE_FILE.stat().st_size,
        "license_declared_by_dataset_card": "CC-BY-3.0",
        "aggregate_counters": dict(sorted(counters.items())),
        "privacy_pattern_counts": dict(sorted(privacy_counts.items())),
        "attack_or_harm_pattern_counts": dict(sorted(review_counts.items())),
        "language_counts_after_pattern_screens": dict(sorted(language_counts.items())),
        "language_identifier_top1_labels": dict(sorted(language_label_counts.items())),
        "language_identifier_confidence_bins": dict(sorted(language_confidence_bins.items())),
        "language_policy": "Dataset card declares English; keep rows whose pinned detector top-1 label is en and record low-confidence bins rather than applying the unrelated LLMail >=0.95 gate to short command utterances.",
        "unique_in_scope_intents_with_eligible_rows": len(per_intent),
        "eligible_unique_train_rows": len(seen),
        "eligible_rows_per_intent_min": min(support) if support else 0,
        "eligible_rows_per_intent_median": support[len(support) // 2] if support else 0,
        "eligible_rows_per_intent_max": max(support) if support else 0,
        "round07_manifest_sha256": round07_hash,
        "round18_dolly_manifest_sha256": round18_hash,
        "candidate_mapping": "native in-scope assistant intent to provisional benign reference; not a safety label or PI-Guard gold",
        "source_creation": "human crowd-elicited questions and commands; publisher describes paraphrase/scenario tasks, not LLM-generated rows",
        "source_family_limit": "Participant IDs are absent from this release. Treat all retained rows as one CLINC collection family; do not turn the 150 intent labels into 150 source families.",
        "privacy_limit": "PII and attack-intent regex screens are incomplete and are not full privacy or semantic review.",
        "split_limit": "Only the pinned upstream train parquet was acquired/read; validation and test files were not requested or opened.",
        "row_text_ids_or_hashes_emitted": False,
        "upstream_validation_or_test_opened": False,
        "pi_guard_test_opened": False,
        "l3_run": False,
        "smoke_run": False,
        "package_admitted": False,
    }
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: result[key] for key in (
        "aggregate_counters", "privacy_pattern_counts", "attack_or_harm_pattern_counts",
        "language_counts_after_pattern_screens", "language_identifier_top1_labels",
        "language_identifier_confidence_bins", "unique_in_scope_intents_with_eligible_rows",
        "eligible_unique_train_rows", "eligible_rows_per_intent_min",
        "eligible_rows_per_intent_median", "eligible_rows_per_intent_max",
    )}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
