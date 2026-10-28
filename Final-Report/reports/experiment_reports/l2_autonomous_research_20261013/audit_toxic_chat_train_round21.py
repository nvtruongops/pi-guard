"""Aggregate-only audit of the pinned ToxicChat train split for L2 research.

Only the upstream train CSV is acquired. The audit projects only the human
prompt and native jailbreak annotation; it never accesses model output fields,
upstream validation/test files, row identifiers, or PI-Guard test payloads.
"""
from __future__ import annotations

import collections
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

import pyarrow.csv as pacsv


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
TRAINING = REPO / "workspaces" / "truongnv" / "pi_guard_pipeline" / "training_bases"
SOURCE_FILE = TRAINING / "datasets" / "source_audit" / "toxic_chat_round21" / "data" / "1123" / "toxic-chat_annotation_train.csv"
PACKAGE = TRAINING / "datasets" / "project_training" / "versions" / "pi_guard_l2_source_heldout_round18_r01"
VENDOR = TRAINING / "datasets" / "project_training" / "history" / "pi_guard_v8_english_diagnostic_20261012" / "tools" / "_vendor"
REPORT = ROOT / "toxic_chat_train_candidate_audit_round21.json"

REPOSITORY = "lmsys/toxic-chat"
REVISION = "b913fa0c27522a8f0f7d12220c126e39dbbf8173"
SOURCE_FILE_SHA256 = "0099077aa4c7183040b11d44d2e6852c293ee2fd78a0ffe47ee12b4d1ecd727e"
LANGUAGE_MODEL_SHA256 = "f4f4a2c3465ca1f081541037f9cac23021d68151c2f709c55ae5eedfca522963"
LANGUAGE_THRESHOLD = 0.95
SIMILARITY_PERCENT = 85

PII_PATTERNS = {
    "email": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "us_ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "ipv4": re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b"),
    "credential_assignment": re.compile(r"(?i)\b(?:api[_ -]?key|access[_ -]?token|password|passwd|secret)\s*[:=]\s*[^\s,;]+"),
    "private_key": re.compile(r"(?i)-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "bearer_token": re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]{16,}"),
    "phone_candidate": re.compile(r"(?<!\w)(?:\+?\d[\d .()\-]{8,}\d)(?!\w)"),
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def shingle_hashes(text: str) -> set[int]:
    words = re.findall(r"\w+", normalize(text))
    chunks = [" ".join(words)] if len(words) < 5 else (
        " ".join(words[pos:pos + 5]) for pos in range(len(words) - 4)
    )
    return {
        int.from_bytes(hashlib.blake2b(chunk.encode("utf-8"), digest_size=8).digest(), "big")
        for chunk in chunks
    }


def bucket_keys(hashes: set[int]) -> list[tuple[int, int, int, int]]:
    sketch = sorted(hashes)[:12]
    return [
        (start // 3, *sketch[start:start + 3])
        for start in range(0, len(sketch) - 2, 3)
    ]


def similar(left: set[int], right: set[int]) -> bool:
    if len(left) * 100 < SIMILARITY_PERCENT * len(right):
        return False
    if len(right) * 100 < SIMILARITY_PERCENT * len(left):
        return False
    common = len(left & right)
    return common * 100 >= SIMILARITY_PERCENT * (len(left) + len(right) - common)


def language_identifier():
    sys.path.insert(0, str(VENDOR))
    from py3langid.langid import LanguageIdentifier, MODEL_FILE
    import py3langid

    model_path = Path(py3langid.__file__).resolve().parent / MODEL_FILE
    if sha256_file(model_path) != LANGUAGE_MODEL_SHA256:
        raise ValueError("PINNED_LANGUAGE_MODEL_HASH_MISMATCH")
    return LanguageIdentifier.from_model_file(MODEL_FILE, norm_probs=True)


def load_frozen_package_texts() -> tuple[dict[str, set[str]], str]:
    raw_manifest = (PACKAGE / "DATASET_MANIFEST.json").read_bytes()
    manifest = json.loads(raw_manifest)
    if manifest.get("package_id") != "pi_guard_l2_source_heldout_round18_r01":
        raise ValueError("UNEXPECTED_FROZEN_PACKAGE_ID")
    texts: dict[str, set[str]] = collections.defaultdict(set)
    for split in ("train", "validation"):
        spec = manifest["partitions"][split]["rows"]
        path = PACKAGE / spec["path"]
        if sha256_file(path) != spec["sha256"]:
            raise ValueError("FROZEN_PARTITION_HASH_MISMATCH:" + split)
        with path.open("r", encoding="utf-8") as stream:
            for line in stream:
                row = json.loads(line)
                value = normalize(row.get("text", ""))
                if value:
                    texts[value].add(str(row.get("label", "unknown")))
    return dict(texts), hashlib.sha256(raw_manifest).hexdigest()


def candidate_bucket_index(
    texts: list[str],
) -> tuple[list[set[int]], dict[tuple[int, int, int, int], list[int]]]:
    hashes_by_index: list[set[int]] = []
    index: dict[tuple[int, int, int, int], list[int]] = collections.defaultdict(list)
    for candidate_index, text in enumerate(texts):
        hashes = shingle_hashes(text)
        hashes_by_index.append(hashes)
        for key in bucket_keys(hashes):
            index[key].append(candidate_index)
    return hashes_by_index, dict(index)


def main() -> int:
    if sha256_file(SOURCE_FILE) != SOURCE_FILE_SHA256:
        raise ValueError("PINNED_TOXIC_CHAT_TRAIN_HASH_MISMATCH")
    frozen_texts, package_manifest_sha256 = load_frozen_package_texts()
    frozen_text_count = len(frozen_texts)
    identifier = language_identifier()

    reader = pacsv.open_csv(
        SOURCE_FILE,
        parse_options=pacsv.ParseOptions(newlines_in_values=True),
        convert_options=pacsv.ConvertOptions(
            include_columns=["user_input", "jailbreaking"],
            strings_can_be_null=True,
        ),
    )
    if set(reader.schema.names) != {"user_input", "jailbreaking"}:
        raise ValueError("UNEXPECTED_PROJECTED_TOXIC_CHAT_SCHEMA")

    counters: collections.Counter[str] = collections.Counter()
    label_values: collections.Counter[str] = collections.Counter()
    privacy: collections.Counter[str] = collections.Counter()
    language_labels: collections.Counter[str] = collections.Counter()
    language_confidence: collections.Counter[str] = collections.Counter()
    seen_exact: set[str] = set()
    screened_candidate_texts: list[str] = []

    for batch in reader:
        for row in batch.to_pylist():
            counters["source_train_rows"] += 1
            raw_label = row.get("jailbreaking")
            label = "null" if raw_label is None else str(raw_label).strip().casefold()
            label_values[label] += 1
            if label not in {"1", "true"}:
                counters["not_native_jailbreaking_positive"] += 1
                continue
            counters["native_jailbreaking_positive"] += 1
            text = row.get("user_input")
            if not isinstance(text, str) or not text.strip():
                counters["positive_empty_or_invalid_prompt"] += 1
                continue

            matches = [name for name, pattern in PII_PATTERNS.items() if pattern.search(text)]
            if matches:
                counters["positive_privacy_pattern_excluded"] += 1
                for name in matches:
                    privacy[name] += 1
                continue

            language, confidence = identifier.classify(text)
            confidence = float(confidence)
            language_labels[language] += 1
            language_confidence[
                ">=0.95" if confidence >= LANGUAGE_THRESHOLD else ">=0.50" if confidence >= 0.50 else "<0.50"
            ] += 1
            if language != "en" or confidence < LANGUAGE_THRESHOLD:
                counters["positive_not_english_or_below_confidence"] += 1
                continue
            counters["positive_english_confident_after_privacy_screen"] += 1

            key = normalize(text)
            if key in seen_exact:
                counters["positive_within_source_exact_duplicate"] += 1
                continue
            seen_exact.add(key)
            if key in frozen_texts:
                counters["exact_overlap_with_frozen_train_or_validation"] += 1
                for label_name in frozen_texts[key]:
                    counters["exact_overlap_existing_label_" + label_name] += 1
                continue
            screened_candidate_texts.append(key)

    # Resolve within-source near duplicates first, preserving the earliest row.
    retained_texts: list[str] = []
    retained_hashes: list[set[int]] = []
    retained_index: dict[tuple[int, int, int, int], list[int]] = collections.defaultdict(list)
    for key in screened_candidate_texts:
        hashes = shingle_hashes(key)
        possible = {
            candidate_index
            for bucket in bucket_keys(hashes)
            for candidate_index in retained_index.get(bucket, ())
        }
        if any(similar(hashes, retained_hashes[i]) for i in possible):
            counters["positive_within_source_near_duplicate_at_0_85"] += 1
            continue
        candidate_index = len(retained_texts)
        retained_texts.append(key)
        retained_hashes.append(hashes)
        for bucket in bucket_keys(hashes):
            retained_index[bucket].append(candidate_index)

    # Scan frozen train/validation once against the small source-candidate index.
    frozen_near_matches: set[int] = set()
    for split in ("train", "validation"):
        spec = json.loads((PACKAGE / "DATASET_MANIFEST.json").read_text(encoding="utf-8"))["partitions"][split]["rows"]
        path = PACKAGE / spec["path"]
        with path.open("r", encoding="utf-8") as stream:
            for line in stream:
                frozen_row = json.loads(line)
                frozen_key = normalize(frozen_row.get("text", ""))
                if not frozen_key:
                    continue
                frozen_hashes = shingle_hashes(frozen_key)
                possible = {
                    candidate_index
                    for bucket in bucket_keys(frozen_hashes)
                    for candidate_index in retained_index.get(bucket, ())
                }
                for candidate_index in possible:
                    if similar(frozen_hashes, retained_hashes[candidate_index]):
                        frozen_near_matches.add(candidate_index)
    counters["near_overlap_with_frozen_train_or_validation_at_0_85"] = len(frozen_near_matches)
    counters["eligible_unique_candidate_rows"] = len(retained_texts) - len(frozen_near_matches)

    result = {
        "audit_round": 21,
        "repository": REPOSITORY,
        "revision": REVISION,
        "upstream_partition": "data/1123/toxic-chat_annotation_train.csv only",
        "source_file_sha256": SOURCE_FILE_SHA256,
        "source_file_bytes": SOURCE_FILE.stat().st_size,
        "license_declared_by_publisher": "CC-BY-NC-4.0",
        "source_description": "Human user queries from the LMSYS Vicuna demo; native jailbreak annotation retained only when jailbreaking=1.",
        "native_label_mapping": "jailbreaking=1 to provisional JB-attempt reference; negatives are not mapped to benign; no curator-gold claim.",
        "source_family_limit": "One LMSYS ToxicChat collection family. conv_id is not treated as a person or independent source family.",
        "aggregate_counters": dict(sorted(counters.items())),
        "native_label_value_counts": dict(sorted(label_values.items())),
        "privacy_pattern_counts": dict(sorted(privacy.items())),
        "language_top1_counts_after_privacy_screen": dict(sorted(language_labels.items())),
        "language_confidence_bins_after_privacy_screen": dict(sorted(language_confidence.items())),
        "language_policy": f"Pinned project py3langid model; retain top-1 English at confidence >= {LANGUAGE_THRESHOLD:.2f}.",
        "duplicate_policy": "NFKC/casefold/whitespace exact match plus project 5-word shingle Jaccard >=85%; compare only source-positive prompts with frozen round18 train+validation and earlier eligible source positives.",
        "frozen_package_manifest_sha256": package_manifest_sha256,
        "frozen_package_text_count": frozen_text_count,
        "projected_columns": ["user_input", "jailbreaking"],
        "model_output_column_projected_or_accessed": False,
        "row_text_ids_or_hashes_emitted": False,
        "upstream_validation_or_test_opened": False,
        "pi_guard_test_opened": False,
        "l3_or_smoke_run": False,
        "package_admitted": False,
        "admission_status": "CONDITIONAL_RESEARCH_CANDIDATE_ONLY",
        "rights_limit": "Non-commercial license; retain attribution; no redistribution. Project owner/rights interpretation is not represented as approved.",
        "privacy_limit": "Publisher warns residual PII may remain. Pattern screening is incomplete and does not establish privacy clearance.",
        "split_limit": "Use only upstream train rows as a candidate train source. No participant-level split evidence; this source cannot be split into independent train/validation families.",
    }
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "aggregate_counters": result["aggregate_counters"],
        "native_label_value_counts": result["native_label_value_counts"],
        "privacy_pattern_counts": result["privacy_pattern_counts"],
        "language_top1_counts_after_privacy_screen": result["language_top1_counts_after_privacy_screen"],
        "language_confidence_bins_after_privacy_screen": result["language_confidence_bins_after_privacy_screen"],
        "package_admitted": result["package_admitted"],
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
