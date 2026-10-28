#!/usr/bin/env python3
"""Audit only the pinned NeurAlchemy core/train shard and train-only comparators."""
from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import csv
import hashlib
import json
import re
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import pyarrow.parquet as pq

REPORT = Path(__file__).resolve().parent
SRC = REPORT / "source_qualification"
ACQUIRED = SRC / "acquired"
TRAINING = Path(r"D:\Work\Do-an\workspaces\truongnv\pi_guard_pipeline\training_bases")
NEURAL = ACQUIRED / "neuralchemy_core_train.parquet"
WAMBO = TRAINING / "datasets" / "source_datasets" / "wambosec_prompt_injections_candidate" / "data" / "train-00000-of-00001.parquet"
BOUNDARY = ACQUIRED / "train.jsonl"

PII_PATTERNS = {
    "email": re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"),
    "credential_assignment": re.compile(r"(?i)\b(?:api[_ -]?key|access[_ -]?token|password|passwd|secret)\s*[:=]\s*[^\s,;]+"),
    "ipv4": re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b"),
}


def norm(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def text_hashes(path: Path, fmt: str) -> tuple[set[str], int]:
    values: set[str] = set()
    count = 0
    if fmt == "parquet":
        rows = pq.read_table(path).to_pylist()
        for row in rows:
            text = row.get("text") or row.get("prompt") or row.get("instruction")
            if isinstance(text, str) and norm(text):
                values.add(hashlib.sha256(norm(text).encode("utf-8")).hexdigest())
            count += 1
    else:
        with path.open(encoding="utf-8") as stream:
            for line in stream:
                if not line.strip():
                    continue
                row = json.loads(line)
                text = row.get("text")
                if isinstance(text, str) and norm(text):
                    values.add(hashlib.sha256(norm(text).encode("utf-8")).hexdigest())
                count += 1
    return values, count


def main() -> int:
    acquired = json.loads((ACQUIRED / "neuralchemy_core_train_manifest.json").read_text(encoding="utf-8"))
    if hashlib.sha256(NEURAL.read_bytes()).hexdigest() != acquired["sha256"]:
        raise RuntimeError("Pinned core/train hash mismatch")
    table = pq.read_table(NEURAL)
    columns = set(table.column_names)
    if not {"text", "label", "category"}.issubset(columns):
        raise RuntimeError(f"Required core/train schema missing: {sorted(columns)}")
    rows = table.to_pylist()
    labels = Counter(str(row.get("label")) for row in rows)
    categories = Counter(str(row.get("category") or "") for row in rows)
    sources = Counter(str(row.get("source") or "") for row in rows)
    licenses = Counter(str(row.get("license") or "") for row in rows)
    augmented = Counter(str(row.get("augmented")) for row in rows)
    group_members: dict[str, list[dict]] = defaultdict(list)
    pii_rows = Counter()
    pii_by_category: dict[str, Counter] = defaultdict(Counter)
    exact: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        text = row.get("text")
        if not isinstance(text, str) or not norm(text):
            raise RuntimeError("Empty or invalid model text in core/train")
        digest = hashlib.sha256(norm(text).encode("utf-8")).hexdigest()
        exact[digest].add(str(row.get("label")))
        if row.get("group_id") is not None:
            group_members[str(row["group_id"])].append(row)
        category = str(row.get("category") or "")
        for name, pattern in PII_PATTERNS.items():
            if pattern.search(text):
                pii_rows[name] += 1
                pii_by_category[category][name] += 1

    candidate_counts = {"explicit_benign": int(categories.get("benign", 0)),
                        "explicit_jailbreak_category": int(categories.get("jailbreak", 0)),
                        "other_malicious_categories": sum(n for category, n in categories.items()
                                                           if category not in {"", "benign", "jailbreak"}),
                        "missing_category": int(categories.get("", 0))}
    overlap = {}
    other_sets = {}
    for name, path, fmt in (("wambosec_train", WAMBO, "parquet"),
                            ("3nesdeniz_boundary_train", BOUNDARY, "jsonl")):
        if path.is_file():
            values, count = text_hashes(path, fmt)
            overlap[name] = {"rows": count, "unique_normalized_prompts": len(values),
                             "exact_shared_normalized_prompts": len(set(exact) & values)}
            other_sets[name] = values

    report = {
        "audit_id": "neuralchemy_core_train_native_mapping_screen_v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "dataset_id": acquired["dataset_id"], "revision": acquired["revision"],
        "split_opened": "core/train only", "validation_opened": False, "test_opened": False,
        "source_sha256": acquired["sha256"], "rows": len(rows), "fields": sorted(columns),
        "native_label_counts": dict(sorted(labels.items())),
        "category_counts": dict(sorted(categories.items())),
        "source_counts": dict(sorted(sources.items())),
        "row_license_counts": dict(sorted(licenses.items())),
        "augmented_counts": dict(sorted(augmented.items())),
        "candidate_class_counts_before_source_rights_filter": candidate_counts,
        "normalized_exact_duplicate_groups": sum(len(v) > 1 for v in exact.values()),
        "normalized_exact_duplicate_excess_rows": len(rows) - len(exact),
        "duplicate_groups_with_cross_label_conflict": sum(len(v) > 1 for v in exact.values()),
        "group_id_count": len(group_members),
        "group_ids_with_multiple_rows": sum(len(v) > 1 for v in group_members.values()),
        "privacy_pattern_row_counts": dict(sorted(pii_rows.items())),
        "privacy_scan_scope": "email, credential assignment, IPv4; counts only; no matched content emitted",
        "exact_train_overlap": overlap,
        "source_family_interpretation": "source field values are reported; count them as independent families only after upstream lineage and rights are evidenced",
        "mapping_policy": {"benign": "native category == benign", "JB": "native category == jailbreak",
                           "PI": "not assigned in this screen; remaining malicious categories require a documented category-level mapping", "other": "quarantine"},
        "test_payload_opened": False,
    }
    target = SRC / "neuralchemy_core_train_audit.json"
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "AUDIT_COMPLETE_TRAIN_ONLY", "rows": len(rows),
                      "labels": report["native_label_counts"], "categories": report["category_counts"],
                      "sources": report["source_counts"], "privacy_patterns": report["privacy_pattern_row_counts"],
                      "train_overlap": report["exact_train_overlap"], "report": str(target),
                      "test_opened": False}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
