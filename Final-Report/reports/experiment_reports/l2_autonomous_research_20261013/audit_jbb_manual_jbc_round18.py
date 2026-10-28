"""Audit the manual JBC subset of pinned JailbreakBench artifacts.

Reads only manual attack-artifact prompts from the pinned JBB repository;
never opens test-artifact or evaluation files and emits aggregates only.
"""
from __future__ import annotations

import collections
import hashlib
import json
import re
import unicodedata
from pathlib import Path
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
PRIVATE = REPO / "workspaces" / "truongnv" / "pi_guard_pipeline"
SOURCE_DIR = PRIVATE / "training_bases" / "datasets" / "source_audit" / "jailbreakbench_artifacts_round17" / "attack-artifacts" / "JBC" / "manual"
PACKAGE = PRIVATE / "training_bases" / "datasets" / "project_training" / "versions" / "pi_guard_native_reference_round07_20261013_r01"
REPORT = ROOT / "jbb_manual_jbc_audit_round18.json"
REPOSITORY = "JailbreakBench/artifacts"
REVISION = "909e68c01d94222b8ad2e397a017e2e12e2adb73"
PII_PATTERNS = {
    "email": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "us_ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "phone_candidate": re.compile(r"(?<!\w)(?:\+?1[ .-]?)?(?:\(?\d{3}\)?[ .-]?)\d{3}[ .-]?\d{4}(?!\w)"),
    "ipv4": re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b"),
    "credential_assignment": re.compile(r"(?i)\b(?:api[_ -]?key|access[_ -]?token|password|passwd|secret)\s*[:=]\s*[^\s,;]+"),
}


def normalize(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def prompt_records(value: Any) -> Iterator[dict[str, Any]]:
    if isinstance(value, dict):
        if isinstance(value.get("prompt"), str):
            yield value
        for key, child in value.items():
            if key != "prompt":
                yield from prompt_records(child)
    elif isinstance(value, list):
        for child in value:
            yield from prompt_records(child)


def main() -> int:
    manifest_path = PACKAGE / "DATASET_MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("package_id") != "pi_guard_l2_native_reference_round07_r01":
        raise ValueError("UNEXPECTED_COMPARISON_PACKAGE")
    old_texts: set[str] = set()
    for split in ("train", "validation"):
        spec = manifest["partitions"][split]["rows"]
        path = PACKAGE / spec["path"]
        if sha256(path) != spec["sha256"]:
            raise ValueError("ROUND07_" + split.upper() + "_HASH_MISMATCH")
        with path.open("r", encoding="utf-8") as stream:
            for line in stream:
                row = json.loads(line)
                value = row.get("text", "")
                if value:
                    old_texts.add(normalize(value))

    per_file: dict[str, dict[str, int]] = {}
    prompts: list[tuple[str, str, bool, str]] = []
    privacy = collections.Counter()
    outcomes = collections.Counter()
    for path in sorted(SOURCE_DIR.glob("*.json")):
        value = json.loads(path.read_text(encoding="utf-8"))
        records = list(prompt_records(value))
        seen_in_file: set[str] = set()
        for record in records:
            text = record.get("prompt", "")
            key = normalize(text)
            if not key:
                continue
            ancestry = record.get("goal", record.get("behavior", ""))
            ancestry_key = normalize(ancestry) if isinstance(ancestry, str) else ""
            flags = []
            for name, pattern in PII_PATTERNS.items():
                if pattern.search(text):
                    privacy[name] += 1
                    flags.append(name)
            outcome = record.get("jailbroken")
            outcomes["true" if outcome is True else "false" if outcome is False else "missing_or_other"] += 1
            prompts.append((key, path.name, bool(flags), ancestry_key))
            seen_in_file.add(key)
        per_file[path.name] = {
            "prompt_occurrences": len(records),
            "normalized_unique_prompts": len(seen_in_file),
            "file_bytes": path.stat().st_size,
            "file_sha256": sha256(path),
        }

    counts = collections.Counter(key for key, *_ in prompts)
    duplicates = {key for key, count in counts.items() if count > 1}
    unique_clean: dict[str, str] = {}
    for key, _name, pii, ancestry in prompts:
        if not pii:
            unique_clean.setdefault(key, ancestry)
    cross_overlap = sum(1 for key in unique_clean if key in old_texts)
    clean_ancestry = {value for key, value in unique_clean.items() if value}
    report = {
        "audit_round": 18,
        "repository": REPOSITORY,
        "revision": REVISION,
        "source_subset": "attack-artifacts/JBC/manual/*.json only",
        "license_declared_by_jbb_repository": "MIT",
        "comparison_package_id": manifest["package_id"],
        "comparison_manifest_sha256": sha256(manifest_path),
        "comparison_partitions_opened": ["train", "validation"],
        "pi_guard_test_opened": False,
        "jbb_test_artifacts_or_evaluation_opened": False,
        "files": per_file,
        "prompt_occurrences": len(prompts),
        "normalized_unique_prompts": len(counts),
        "normalized_duplicate_groups": len(duplicates),
        "duplicate_occurrences_after_first": sum(count - 1 for count in counts.values() if count > 1),
        "regex_privacy_indicator_occurrences": dict(sorted(privacy.items())),
        "clean_unique_prompts_after_regex_screen": len(unique_clean),
        "exact_overlap_with_round07_train_validation_unique_prompts": cross_overlap,
        "distinct_nonempty_behavior_ancestry_keys": len(clean_ancestry),
        "jailbroken_outcome_counts_not_used_as_input_label": dict(sorted(outcomes.items())),
        "mapping_status": "conditional JBC/manual attempt-level reference mapping; not canonical or human-adjudicated PI-Guard gold",
        "lineage_limit": "JBC artifacts are a separate benchmark packaging, but the JailbreakChat community also appears in the broader TrustAIR/JailbreakHub in-the-wild lineage; do not call this independent community-origin evidence.",
        "privacy_limit": "Regex screening is incomplete and is not full privacy clearance.",
        "split_limit": "All manual JBC prompts must remain one held-out source-family group; behavior ancestry should also remain grouped if any partition changes.",
        "l3_run": False,
        "smoke_run": False,
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in (
        "files", "prompt_occurrences", "normalized_unique_prompts", "normalized_duplicate_groups",
        "duplicate_occurrences_after_first", "regex_privacy_indicator_occurrences",
        "clean_unique_prompts_after_regex_screen", "exact_overlap_with_round07_train_validation_unique_prompts",
        "distinct_nonempty_behavior_ancestry_keys", "jailbroken_outcome_counts_not_used_as_input_label",
        "pi_guard_test_opened", "jbb_test_artifacts_or_evaluation_opened",
    )}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
