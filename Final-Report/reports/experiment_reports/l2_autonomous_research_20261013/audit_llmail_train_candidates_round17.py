"""Download and aggregate-audit LLMail-Inject train submissions only.

The two pinned labelled-unique phase files are treated as candidate attack
training data. The separate emails_for_fp_tests file is never requested or
opened. This script emits no prompt text, row identifiers, or per-row hashes.
"""
from __future__ import annotations

import collections
import hashlib
import json
import re
import sys
import unicodedata
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
PRIVATE = REPO / "workspaces" / "truongnv" / "pi_guard_pipeline"
TRAINING = PRIVATE / "training_bases"
VENDOR = TRAINING / "datasets" / "project_training" / "history" / "pi_guard_v8_english_diagnostic_20261012" / "tools" / "_vendor"
ROUND07 = TRAINING / "datasets" / "project_training" / "versions" / "pi_guard_native_reference_round07_20261013_r01"
SOURCE_DIR = TRAINING / "datasets" / "source_audit" / "llmail_inject_round17"
REPORT = ROOT / "llmail_train_candidate_audit_round17.json"
REPOSITORY = "microsoft/llmail-inject-challenge"
REVISION = "1063bdf01ec8762b812d5e06ee768a06faa5a6f7"
FILES = {
    "phase1": {
        "path": "data/labelled_unique_submissions_phase1.json",
        "size": 448_194_111,
        "tree_oid": "6eb0414a0ea2d702049563b26444c47937142362",
    },
    "phase2": {
        "path": "data/labelled_unique_submissions_phase2.json",
        "size": 68_586_935,
        "tree_oid": "8c018371e27669e80509c631b1e20a70e76b6a08",
    },
}
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
FAMILY_FIELDS = {"team_id", "participant_id", "scenario", "level", "level_id", "submission_id"}
TRACKED_FIELDS = FAMILY_FIELDS | {"attack_attempt"}


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "Codex-L2-Research"})
    with urllib.request.urlopen(request, timeout=180) as response:
        return response.read()


def normalized(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def named_values(value: Any, path: tuple[str, ...] = ()) -> Iterator[tuple[str, Any]]:
    if isinstance(value, dict):
        for key, child in value.items():
            name = str(key).casefold()
            if name in TRACKED_FIELDS:
                yield name, child
            yield from named_values(child, path + (name,))
    elif isinstance(value, list):
        for child in value:
            yield from named_values(child, path)


def language_identifier():
    sys.path.insert(0, str(VENDOR))
    from py3langid.langid import LanguageIdentifier, MODEL_FILE
    model_path = Path(__import__("py3langid").__file__).resolve().parent / MODEL_FILE
    if sha256_bytes(model_path.read_bytes()) != MODEL_SHA256:
        raise ValueError("PINNED_LANGUAGE_MODEL_HASH_MISMATCH")
    return LanguageIdentifier.from_model_file(MODEL_FILE, norm_probs=True)


def package_text_hashes() -> tuple[set[str], dict]:
    manifest_path = ROUND07 / "DATASET_MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("package_id") != "pi_guard_l2_native_reference_round07_r01":
        raise ValueError("UNEXPECTED_ROUND07_PACKAGE")
    found: set[str] = set()
    for split in ("train", "validation"):
        spec = manifest["partitions"][split]["rows"]
        path = ROUND07 / spec["path"]
        if sha256_bytes(path.read_bytes()) != spec["sha256"]:
            raise ValueError("ROUND07_" + split.upper() + "_HASH_MISMATCH")
        with path.open("r", encoding="utf-8") as stream:
            for line in stream:
                row = json.loads(line)
                text = row.get("text", "")
                key = normalized(text)
                if key:
                    found.add(sha256_bytes(key.encode("utf-8")))
    return found, manifest


def main() -> int:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    raw_files: dict[str, Path] = {}
    source_manifest = []
    for phase, item in FILES.items():
        path = SOURCE_DIR / (phase + ".json")
        if path.exists():
            raw = path.read_bytes()
        else:
            raw = fetch(f"https://huggingface.co/datasets/{REPOSITORY}/resolve/{REVISION}/{item['path']}")
            path.write_bytes(raw)
        if len(raw) != item["size"]:
            raise ValueError("LLMAIL_FILE_SIZE_MISMATCH:" + phase)
        raw_files[phase] = path
        source_manifest.append({
            "phase": phase,
            "path": item["path"],
            "tree_oid": item["tree_oid"],
            "bytes": len(raw),
            "sha256": sha256_bytes(raw),
        })

    identifier = language_identifier()
    old_hashes, old_manifest = package_text_hashes()
    all_hash_counts: collections.Counter[str] = collections.Counter()
    phase_hashes: dict[str, collections.Counter[str]] = {}
    counts: collections.Counter[str] = collections.Counter()
    langs: collections.Counter[str] = collections.Counter()
    pii: collections.Counter[str] = collections.Counter()
    fields_present: collections.Counter[str] = collections.Counter()
    family_value_hashes: dict[str, set[str]] = collections.defaultdict(set)
    native_flags: collections.Counter[str] = collections.Counter()
    phase_summaries = {}

    for phase, path in raw_files.items():
        local_hashes: collections.Counter[str] = collections.Counter()
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("LLMAIL_TOP_LEVEL_OBJECT_REQUIRED:" + phase)
        for prompt, metadata in data.items():
            counts[phase + ":unique_entries"] += 1
            counts["total_entries"] += 1
            normalized_prompt = normalized(prompt)
            if not normalized_prompt:
                counts["empty_prompt"] += 1
                continue
            text_hash = sha256_bytes(normalized_prompt.encode("utf-8"))
            all_hash_counts[text_hash] += 1
            local_hashes[text_hash] += 1
            language, confidence = identifier.classify(prompt.strip())
            langs[language if float(confidence) >= LANGUAGE_THRESHOLD else "below_threshold_or_uncertain"] += 1
            if language == "en" and float(confidence) >= LANGUAGE_THRESHOLD:
                counts[phase + ":english_confident"] += 1
            else:
                counts[phase + ":non_english_or_uncertain"] += 1
            for name, pattern in PII_PATTERNS.items():
                if pattern.search(prompt):
                    pii[name] += 1
                    if language == "en" and float(confidence) >= LANGUAGE_THRESHOLD:
                        pii["english:" + name] += 1
            if text_hash in old_hashes:
                counts["exact_overlap_round07_train_validation"] += 1
            if isinstance(metadata, dict):
                for name, value in named_values(metadata):
                    fields_present[name] += 1
                    if value is None or value == "":
                        continue
                    if isinstance(value, (str, int, float, bool)):
                        family_value_hashes[name].add(sha256_bytes(str(value).encode("utf-8")))
                for name, value in named_values(metadata):
                    if name == "attack_attempt":
                        native_flags[str(value).casefold()] += 1
        phase_hashes[phase] = local_hashes
        phase_summaries[phase] = {
            "unique_entries": counts[phase + ":unique_entries"],
            "english_confident": counts[phase + ":english_confident"],
            "non_english_or_uncertain": counts[phase + ":non_english_or_uncertain"],
            "normalized_duplicate_groups_within_phase": sum(1 for value in local_hashes.values() if value > 1),
            "normalized_duplicate_rows_within_phase_after_first": sum(value - 1 for value in local_hashes.values() if value > 1),
        }
        checkpoint = {
            "phase": phase,
            "revision": REVISION,
            "source_file_sha256": next(row["sha256"] for row in source_manifest if row["phase"] == phase),
            "aggregate_summary": phase_summaries[phase],
            "pii_indicator_rows_so_far": dict(sorted(pii.items())),
            "metadata_distinct_value_counts_by_field_so_far": {key: len(values) for key, values in sorted(family_value_hashes.items())},
            "test_files_not_requested": ["data/emails_for_fp_tests.jsonl"],
            "test_payload_opened": False,
        }
        (SOURCE_DIR / (phase + "_aggregate_checkpoint.json")).write_text(
            json.dumps(checkpoint, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        del data

    cross_phase_duplicate_groups = sum(
        1 for key in set(phase_hashes["phase1"]) & set(phase_hashes["phase2"])
    )
    cross_phase_duplicate_rows = sum(
        min(phase_hashes["phase1"][key], phase_hashes["phase2"][key])
        for key in set(phase_hashes["phase1"]) & set(phase_hashes["phase2"])
    )
    all_duplicates = sum(1 for value in all_hash_counts.values() if value > 1)
    all_duplicate_rows = sum(value - 1 for value in all_hash_counts.values() if value > 1)
    unique_texts = len(all_hash_counts)
    english_entries = sum(value for phase, value in counts.items() if phase.endswith(":english_confident"))
    result = {
        "audit_round": 17,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "repository": REPOSITORY,
        "revision": REVISION,
        "dataset_card_license": "MIT",
        "source_files": source_manifest,
        "selection_policy": "labelled-unique Phase1 and Phase2 submissions only; never acquire raw submission files, emails_for_fp_tests, or PI-Guard test data",
        "source_file_count": len(source_manifest),
        "source_bytes_total": sum(row["bytes"] for row in source_manifest),
        "phase_summaries": phase_summaries,
        "total_entries": counts["total_entries"],
        "english_confident_entries": english_entries,
        "aggregate_language_counts": dict(sorted(langs.items())),
        "normalized_unique_texts_across_phases": unique_texts,
        "normalized_duplicate_groups_across_phases": all_duplicates,
        "normalized_duplicate_rows_after_first_across_phases": all_duplicate_rows,
        "cross_phase_duplicate_groups": cross_phase_duplicate_groups,
        "cross_phase_duplicate_rows": cross_phase_duplicate_rows,
        "exact_overlap_with_round07_train_validation_rows": counts["exact_overlap_round07_train_validation"],
        "pii_indicator_rows": dict(sorted(pii.items())),
        "metadata_field_presence_counts": dict(sorted(fields_present.items())),
        "metadata_distinct_value_counts_by_field": {key: len(values) for key, values in sorted(family_value_hashes.items())},
        "attack_attempt_metadata_value_counts": dict(sorted(native_flags.items())),
        "round07_package_id": old_manifest["package_id"],
        "round07_manifest_sha256": sha256_bytes((ROUND07 / "DATASET_MANIFEST.json").read_bytes()),
        "test_files_not_requested": ["data/emails_for_fp_tests.jsonl"],
        "pi_guard_test_opened": False,
        "mapping_status": "candidate PI-attempt reference mapping only; no canonical label or package admission",
        "rights_status": "publisher metadata declares MIT; no independent legal determination",
        "privacy_status": "regex indicators only; not a complete privacy review",
        "package_admitted": False,
        "l3_run": False,
        "smoke_run": False,
        "limitations": [
            "Prompts are email subject/body attacks submitted to a particular adaptive tool-call challenge, not generic direct user prompts.",
            "Phase and team/level metadata require source-family and behavior ancestry grouping before any split.",
            "Language-ID and regex filters are screening signals, not human adjudication or comprehensive privacy clearance.",
            "Model outcome labels describe challenge results and are not used as the prompt-level PI class label.",
        ],
    }
    (SOURCE_DIR / "aggregate_audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: result[key] for key in (
        "source_bytes_total", "phase_summaries", "total_entries", "english_confident_entries",
        "aggregate_language_counts", "normalized_unique_texts_across_phases",
        "normalized_duplicate_groups_across_phases", "normalized_duplicate_rows_after_first_across_phases",
        "cross_phase_duplicate_groups", "cross_phase_duplicate_rows",
        "exact_overlap_with_round07_train_validation_rows", "pii_indicator_rows",
        "metadata_distinct_value_counts_by_field", "attack_attempt_metadata_value_counts",
        "test_files_not_requested", "package_admitted",
    )}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
