"""Pin and aggregate-audit OASST1 train messages as a provisional benign lead.

Only the upstream train parquet is acquired. The audit reads a minimal column
set, emits aggregate counts only, and never opens any upstream or PI-Guard test.
"""
from __future__ import annotations

import collections
import hashlib
import json
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pyarrow.parquet as pq


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
PRIVATE = REPO / "workspaces" / "truongnv" / "pi_guard_pipeline"
ROUND07 = PRIVATE / "training_bases" / "datasets" / "project_training" / "versions" / "pi_guard_native_reference_round07_20261013_r01"
SOURCE_DIR = PRIVATE / "training_bases" / "datasets" / "source_audit" / "oasst1_round17"
REPORT = ROOT / "oasst1_candidate_audit_round17.json"
REPOSITORY = "OpenAssistant/oasst1"
REVISION = "c6c1242d280bf4c487619ab08c30d43872afcf56"
TRAIN_PATH = "data/train-00000-of-00001-b42a775f407cee45.parquet"
TRAIN_BYTES = 39_516_251
TRAIN_TREE_OID = "43a49ea628a6d6796a840df5654ad653962f6648"
TRAIN_SHA256 = "bbfadf5ed1278ba2208c837fdcad865adf65f5df55d80abadab2745db13fcb5e"
RESOLVE_URL = f"https://huggingface.co/datasets/{REPOSITORY}/resolve/{REVISION}/{TRAIN_PATH}"

PII_PATTERNS = {
    "email": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "us_ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "phone_candidate": re.compile(r"(?<!\w)(?:\+?1[ .-]?)?(?:\(?\d{3}\)?[ .-]?)\d{3}[ .-]?\d{4}(?!\w)"),
    "ipv4": re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b"),
    "credential_assignment": re.compile(r"(?i)\b(?:api[_ -]?key|access[_ -]?token|password|passwd|secret)\s*[:=]\s*[^\s,;]+"),
}
REVIEW_LABELS = {"spam", "lang_mismatch", "pii", "not_appropriate", "hate_speech", "sexual_content", "violence"}


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "Codex-L2-Research"})
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.read()


def normalize(text: str) -> str:
    return " ".join(text.casefold().split())


def flagged_labels(value: Any) -> set[str]:
    if not isinstance(value, dict):
        return set()
    names, values = value.get("name"), value.get("value")
    if not isinstance(names, list):
        return set()
    value_by_name = dict(zip(names, values)) if isinstance(values, list) else {}
    return {str(name) for name in names
            if str(name) in REVIEW_LABELS and float(value_by_name.get(name, 0.0) or 0.0) > 0.0}


def main() -> int:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    local_file = SOURCE_DIR / "train.parquet"
    raw = local_file.read_bytes() if local_file.exists() else fetch(RESOLVE_URL)
    if len(raw) != TRAIN_BYTES:
        raise ValueError("OASST1_TRAIN_SIZE_MISMATCH")
    source_sha = sha256_bytes(raw)
    if source_sha != TRAIN_SHA256:
        raise ValueError("OASST1_TRAIN_SHA256_MISMATCH")
    if not local_file.exists():
        local_file.write_bytes(raw)

    table = pq.read_table(local_file, columns=[
        "parent_id", "role", "lang", "text", "deleted", "synthetic", "labels",
    ])
    counts: collections.Counter[str] = collections.Counter()
    rows_by_language: collections.Counter[str] = collections.Counter()
    rows_by_role: collections.Counter[str] = collections.Counter()
    flagged_counts: collections.Counter[str] = collections.Counter()
    pii_counts: collections.Counter[str] = collections.Counter()
    candidate_keys: collections.Counter[str] = collections.Counter()
    candidate_characters = 0

    for row in table.to_pylist():
        counts["all_train_messages"] += 1
        role = row.get("role") or "<missing>"
        lang = row.get("lang") or "<missing>"
        rows_by_role[str(role)] += 1
        rows_by_language[str(lang)] += 1
        if role != "prompter":
            continue
        counts["prompter_messages"] += 1
        if row.get("parent_id") not in (None, ""):
            continue
        counts["root_prompter_messages"] += 1
        if lang != "en":
            continue
        counts["english_root_prompter_messages"] += 1
        if row.get("deleted") is not False:
            counts["english_root_deleted_or_unknown_excluded"] += 1
            continue
        if row.get("synthetic") is not False:
            counts["english_root_synthetic_or_unknown_excluded"] += 1
            continue
        text = row.get("text")
        if not isinstance(text, str) or not text.strip():
            counts["english_root_empty_excluded"] += 1
            continue
        labels = flagged_labels(row.get("labels"))
        for label in labels:
            flagged_counts[label] += 1
        if labels:
            counts["english_root_review_label_excluded"] += 1
            continue
        text = text.strip()
        flags = [name for name, pattern in PII_PATTERNS.items() if pattern.search(text)]
        for name in flags:
            pii_counts[name] += 1
        if flags:
            counts["english_root_pii_indicator_excluded"] += 1
            continue
        key = normalize(text)
        if not key:
            counts["english_root_empty_after_normalization_excluded"] += 1
            continue
        candidate_keys[key] += 1
        candidate_characters += len(text)

    package_manifest_path = ROUND07 / "DATASET_MANIFEST.json"
    package_manifest = json.loads(package_manifest_path.read_text(encoding="utf-8"))
    if package_manifest.get("package_id") != "pi_guard_l2_native_reference_round07_r01":
        raise ValueError("UNEXPECTED_ROUND07_PACKAGE")
    old_texts: set[str] = set()
    for split in ("train", "validation"):
        spec = package_manifest["partitions"][split]["rows"]
        path = ROUND07 / spec["path"]
        if sha256_bytes(path.read_bytes()) != spec["sha256"]:
            raise ValueError("ROUND07_" + split.upper() + "_HASH_MISMATCH")
        with path.open("r", encoding="utf-8") as stream:
            for line in stream:
                row = json.loads(line)
                key = normalize(row.get("text", ""))
                if key:
                    old_texts.add(key)

    exact_duplicate_groups = sum(1 for value in candidate_keys.values() if value > 1)
    duplicate_rows = sum(value - 1 for value in candidate_keys.values() if value > 1)
    overlap_keys = {key for key in candidate_keys if key in old_texts}
    overlap_rows = sum(candidate_keys[key] for key in overlap_keys)
    overlap_groups = len(overlap_keys)
    post_exact_new_unique = sum(1 for key in candidate_keys if key not in old_texts)
    post_exact_new_raw = sum(value for key, value in candidate_keys.items() if key not in old_texts)
    manifest = {
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "repository": REPOSITORY,
        "revision": REVISION,
        "license_declared_by_dataset_card": "Apache-2.0",
        "upstream_split": "train only",
        "source_path": TRAIN_PATH,
        "source_tree_oid": TRAIN_TREE_OID,
        "source_size_bytes": len(raw),
        "source_sha256": source_sha,
        "dataset_row_count": table.num_rows,
        "columns_read": ["parent_id", "role", "lang", "text", "deleted", "synthetic", "labels"],
        "all_upstream_validation_or_test_opened": False,
        "round07_opened_partitions": ["train", "validation"],
        "round07_test_opened": False,
        "round07_package_id": package_manifest["package_id"],
        "round07_manifest_sha256": sha256_bytes(package_manifest_path.read_bytes()),
        "row_counts": dict(sorted(counts.items())),
        "role_counts": dict(sorted(rows_by_role.items())),
        "language_counts_top20": dict(rows_by_language.most_common(20)),
        "review_label_exclusion_counts": dict(sorted(flagged_counts.items())),
        "regex_privacy_indicator_rows": dict(sorted(pii_counts.items())),
        "candidate_raw_rows_before_dedup_and_cross_package_filter": sum(candidate_keys.values()),
        "candidate_unique_texts_before_cross_package_filter": len(candidate_keys),
        "candidate_duplicate_groups": exact_duplicate_groups,
        "candidate_duplicate_rows_after_first": duplicate_rows,
        "cross_package_exact_overlap_groups": overlap_groups,
        "exact_overlap_with_round07_train_validation_rows": overlap_rows,
        "new_raw_rows_after_exact_cross_package_filter": post_exact_new_raw,
        "new_unique_texts_after_exact_dedup_and_cross_package_filter": post_exact_new_unique,
        "candidate_text_characters_aggregate": candidate_characters,
        "candidate_mapping_status": "provisional benign reference only; no canonical safety label or package admission",
        "privacy_status": "automated native-label and regex screening only; not full privacy clearance",
        "limitations": [
            "Prompter role and root position do not prove benign intent; native review labels only support exclusions.",
            "Exact duplicates are counted but near-duplicate and collection-family grouping remain pending.",
            "Regex privacy screening is incomplete; contributor/user identifiers were not read or exported.",
        ],
        "l2_package_admitted": False,
        "l3_run": False,
        "smoke_run": False,
    }
    manifest_path = SOURCE_DIR / "aggregate_audit.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    REPORT.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: manifest[key] for key in (
        "dataset_row_count", "row_counts", "role_counts", "language_counts_top20",
        "review_label_exclusion_counts", "regex_privacy_indicator_rows",
        "candidate_raw_rows_before_dedup_and_cross_package_filter",
        "candidate_unique_texts_before_cross_package_filter", "candidate_duplicate_groups",
        "candidate_duplicate_rows_after_first", "exact_overlap_with_round07_train_validation_rows",
        "cross_package_exact_overlap_groups", "new_raw_rows_after_exact_cross_package_filter",
        "new_unique_texts_after_exact_dedup_and_cross_package_filter",
        "l2_package_admitted", "l3_run", "smoke_run",
    )}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
