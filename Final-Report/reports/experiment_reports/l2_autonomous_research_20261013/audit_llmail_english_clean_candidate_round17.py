"""Aggregate audit of the LLMail English, pattern-clean attack-attempt cohort.

No prompt text, row key, or per-row hash is written. This does not create a
dataset package, admit the source, or access any test file.
"""
from __future__ import annotations

import collections
import hashlib
import json
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
TRAINING = REPO / "workspaces" / "truongnv" / "pi_guard_pipeline" / "training_bases"
VENDOR = TRAINING / "datasets" / "project_training" / "history" / "pi_guard_v8_english_diagnostic_20261012" / "tools" / "_vendor"
SOURCE_DIR = TRAINING / "datasets" / "source_audit" / "llmail_inject_round17"
SOURCE_AUDIT = SOURCE_DIR / "aggregate_audit.json"
ROUND07 = TRAINING / "datasets" / "project_training" / "versions" / "pi_guard_native_reference_round07_20261013_r01"
REPORT = ROOT / "llmail_english_clean_candidate_audit_round17.json"

MODEL_SHA256 = "f4f4a2c3465ca1f081541037f9cac23021d68151c2f709c55ae5eedfca522963"
LANGUAGE_THRESHOLD = 0.95
PII_PATTERNS = {
    "email": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "us_ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "ipv4": re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b"),
    "credential_assignment": re.compile(r"(?i)\b(?:api[_ -]?key|access[_ -]?token|password|passwd|secret)\s*[:=]\s*[^\s,;]+"),
    "private_key": re.compile(r"(?i)-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "bearer_token": re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]{16,}"),
    "phone_candidate": re.compile(r"(?<!\w)(?:\+?\d[\d .()\-]{8,}\d)(?!\w)"),
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalized(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def is_attack_attempt(metadata: object) -> bool:
    if not isinstance(metadata, dict):
        return False
    value = metadata.get("attack_attempt")
    return value is True or (isinstance(value, str) and value.casefold() == "true")


def language_identifier():
    sys.path.insert(0, str(VENDOR))
    from py3langid.langid import LanguageIdentifier, MODEL_FILE
    model_path = Path(__import__("py3langid").__file__).resolve().parent / MODEL_FILE
    if sha256(model_path.read_bytes()) != MODEL_SHA256:
        raise ValueError("PINNED_LANGUAGE_MODEL_HASH_MISMATCH")
    return LanguageIdentifier.from_model_file(MODEL_FILE, norm_probs=True)


def package_hashes() -> tuple[set[str], str]:
    manifest_path = ROUND07 / "DATASET_MANIFEST.json"
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes)
    if manifest.get("package_id") != "pi_guard_l2_native_reference_round07_r01":
        raise ValueError("UNEXPECTED_ROUND07_PACKAGE")
    found: set[str] = set()
    for split in ("train", "validation"):
        spec = manifest["partitions"][split]["rows"]
        path = ROUND07 / spec["path"]
        if sha256(path.read_bytes()) != spec["sha256"]:
            raise ValueError("ROUND07_" + split.upper() + "_HASH_MISMATCH")
        with path.open("r", encoding="utf-8") as stream:
            for line in stream:
                row = json.loads(line)
                text = normalized(row.get("text", ""))
                if text:
                    found.add(sha256(text.encode("utf-8")))
    return found, sha256(manifest_bytes)


def main() -> int:
    source_audit = json.loads(SOURCE_AUDIT.read_text(encoding="utf-8"))
    source_specs = {item["phase"]: item for item in source_audit["source_files"]}
    identifier = language_identifier()
    old_hashes, old_manifest_hash = package_hashes()
    counters: collections.Counter[str] = collections.Counter()
    langs: collections.Counter[str] = collections.Counter()
    by_phase: dict[str, dict] = {}
    selected_hash_counts: collections.Counter[str] = collections.Counter()
    phase_hash_counts: dict[str, collections.Counter[str]] = {}

    for phase in ("phase1", "phase2"):
        path = SOURCE_DIR / (phase + ".json")
        raw = path.read_bytes()
        spec = source_specs[phase]
        if len(raw) != spec["bytes"] or sha256(raw) != spec["sha256"]:
            raise ValueError("PINNED_SOURCE_FILE_MISMATCH:" + phase)
        data = json.loads(raw.decode("utf-8"))
        local: collections.Counter[str] = collections.Counter()
        for prompt, metadata in data.items():
            if not is_attack_attempt(metadata):
                continue
            counters["native_attack_attempt_true"] += 1
            if any(pattern.search(prompt) for pattern in PII_PATTERNS.values()):
                counters["attack_attempt_true_with_privacy_pattern"] += 1
                continue
            counters["attack_attempt_true_without_privacy_pattern"] += 1
            language, confidence = identifier.classify(prompt.strip())
            if language != "en" or float(confidence) < LANGUAGE_THRESHOLD:
                counters["pattern_clean_attack_attempt_non_english_or_uncertain"] += 1
                langs[language if float(confidence) >= LANGUAGE_THRESHOLD else "below_threshold_or_uncertain"] += 1
                continue
            counters["english_pattern_clean_attack_attempt"] += 1
            langs["en_confident"] += 1
            key = sha256(normalized(prompt).encode("utf-8"))
            selected_hash_counts[key] += 1
            local[key] += 1
            if key in old_hashes:
                counters["exact_overlap_round07_train_validation"] += 1
        phase_hash_counts[phase] = local
        by_phase[phase] = {
            "native_attack_attempt_true": sum(1 for metadata in data.values() if is_attack_attempt(metadata)),
            "attack_attempt_true_without_privacy_pattern": counters["attack_attempt_true_without_privacy_pattern"] - sum(
                item["attack_attempt_true_without_privacy_pattern"] for item in by_phase.values()
            ),
            "english_pattern_clean_attack_attempt": sum(local.values()),
            "normalized_duplicate_groups": sum(1 for count in local.values() if count > 1),
            "normalized_duplicate_rows_after_first": sum(count - 1 for count in local.values() if count > 1),
        }
        del data

    overlap_keys = set(phase_hash_counts["phase1"]) & set(phase_hash_counts["phase2"])
    all_duplicate_groups = sum(1 for count in selected_hash_counts.values() if count > 1)
    result = {
        "audit_round": 17,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "repository": source_audit["repository"],
        "revision": source_audit["revision"],
        "source_file_sha256": {phase: source_specs[phase]["sha256"] for phase in ("phase1", "phase2")},
        "selection_rule": "native attack_attempt=true; exclude any configured privacy-pattern match; require pinned py3langid English confidence >=0.95",
        "language_model_sha256": MODEL_SHA256,
        "language_threshold": LANGUAGE_THRESHOLD,
        "privacy_pattern_names": sorted(PII_PATTERNS),
        "native_attack_attempt_true": counters["native_attack_attempt_true"],
        "attack_attempt_true_with_privacy_pattern": counters["attack_attempt_true_with_privacy_pattern"],
        "attack_attempt_true_without_privacy_pattern": counters["attack_attempt_true_without_privacy_pattern"],
        "pattern_clean_attack_attempt_non_english_or_uncertain": counters["pattern_clean_attack_attempt_non_english_or_uncertain"],
        "english_pattern_clean_attack_attempt": counters["english_pattern_clean_attack_attempt"],
        "normalized_unique_english_pattern_clean_attempts": len(selected_hash_counts),
        "normalized_duplicate_groups": all_duplicate_groups,
        "normalized_duplicate_rows_after_first": sum(count - 1 for count in selected_hash_counts.values() if count > 1),
        "cross_phase_duplicate_groups": len(overlap_keys),
        "cross_phase_duplicate_rows": sum(min(phase_hash_counts["phase1"][key], phase_hash_counts["phase2"][key]) for key in overlap_keys),
        "exact_overlap_round07_train_validation": counters["exact_overlap_round07_train_validation"],
        "phase_summaries": by_phase,
        "aggregate_language_counts_after_privacy_filter": dict(sorted(langs.items())),
        "round07_manifest_sha256": old_manifest_hash,
        "test_files_not_requested": source_audit["test_files_not_requested"],
        "pi_guard_test_opened": False,
        "package_admitted": False,
        "limitations": [
            "Regex privacy filtering is not a comprehensive human privacy review.",
            "The labelled-unique export has no participant, team, or source-family key; hold the collection as one lineage unit.",
            "Native attack-attempt status is an input-class reference mapping, not canonical PI taxonomy adjudication.",
            "No prompt rows, IDs, or per-row hashes are written by this script.",
        ],
    }
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
