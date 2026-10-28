#!/usr/bin/env python3
"""Audit source/category support in the pinned NeurAlchemy core/train shard."""
from __future__ import annotations

import hashlib
import json
import sys
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import pyarrow.parquet as pq

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
ACQUIRED = HERE / "acquired"
SHARD = ACQUIRED / "neuralchemy_core_train.parquet"
SHARD_MANIFEST = ACQUIRED / "neuralchemy_core_train_manifest.json"
CARD = HERE / "neuralchemy__Prompt-injection-dataset__README.md"
OUT = HERE / "neuralchemy_source_component_audit_round02.json"
EXPECTED_REVISION = "7d70432dfcf47a821612cbf9d34e9d9e3ad20e75"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    if OUT.exists():
        raise RuntimeError(f"Refusing to overwrite audit: {OUT}")
    acquired = json.loads(SHARD_MANIFEST.read_text(encoding="utf-8"))
    if acquired["revision"] != EXPECTED_REVISION or sha(SHARD) != acquired["sha256"]:
        raise RuntimeError("Pinned core/train shard revision or checksum mismatch")
    table = pq.read_table(SHARD, columns=["text", "source", "category", "label", "augmented", "group_id"])
    rows = table.to_pylist()

    by_source: dict[str, dict] = {}
    grouped: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    digest_sources: dict[str, set[str]] = defaultdict(set)
    digest_labels: dict[str, set[str]] = defaultdict(set)
    digest_counts: Counter[str] = Counter()
    for row in rows:
        source = str(row.get("source") or "")
        category = str(row.get("category") or "")
        label = str(row.get("label"))
        augmented = str(row.get("augmented"))
        text = row.get("text")
        if not isinstance(text, str) or not text.strip():
            raise RuntimeError("Missing text in pinned core/train shard")
        normalized = " ".join(unicodedata.normalize("NFKC", text).casefold().split())
        digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
        digest_sources[digest].add(source)
        digest_labels[digest].add(label)
        digest_counts[digest] += 1
        counts = by_source.setdefault(source, {
            "rows": 0,
            "labels": Counter(),
            "categories": Counter(),
            "augmented": Counter(),
            "groups": set(),
            "prompt_digests": set(),
        })
        counts["rows"] += 1
        counts["labels"][label] += 1
        counts["categories"][category] += 1
        counts["augmented"][augmented] += 1
        counts["prompt_digests"].add(digest)
        if row.get("group_id") is not None:
            counts["groups"].add(str(row["group_id"]))
            grouped[source][str(row["group_id"])].add(category)

    summary = {}
    for source, counts in sorted(by_source.items()):
        summary[source] = {
            "rows": counts["rows"],
            "native_label_counts": dict(sorted(counts["labels"].items())),
            "category_counts": dict(sorted(counts["categories"].items())),
            "augmented_counts": dict(sorted(counts["augmented"].items())),
            "unique_normalized_prompts": len(counts["prompt_digests"]),
            "duplicate_excess_rows": counts["rows"] - len(counts["prompt_digests"]),
            "group_id_count": len(counts["groups"]),
            "groups_with_multiple_categories": sum(len(value) > 1 for value in grouped[source].values()),
        }

    report = {
        "audit_id": "neuralchemy_core_source_component_audit_round02_v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "dataset_id": acquired["dataset_id"],
        "revision": acquired["revision"],
        "upstream_split": "core/train only",
        "validation_opened": False,
        "test_opened": False,
        "payload_executed": False,
        "shard_sha256": sha(SHARD),
        "card_sha256": sha(CARD),
        "rows": len(rows),
        "native_label_counts": dict(sorted(Counter(str(row.get("label")) for row in rows).items())),
        "row_license_field_counts": dict(sorted(Counter(str(row.get("license") or "") for row in rows).items())),
        "normalized_duplicate_groups": sum(count > 1 for count in digest_counts.values()),
        "normalized_duplicate_excess_rows": len(rows) - len(digest_counts),
        "cross_source_duplicate_groups": sum(len(sources) > 1 for sources in digest_sources.values()),
        "cross_source_duplicate_pairs": {
            "__".join((left, right)): sum(1 for sources in digest_sources.values()
                                           if left in sources and right in sources)
            for left in sorted(by_source)
            for right in sorted(by_source)
            if left < right
        },
        "duplicate_groups_with_cross_label_conflict": sum(len(labels) > 1 for labels in digest_labels.values()),
        "source_components": summary,
        "source_card_license_declarations": {
            "neuralchemy_v1": "Apache-2.0; publisher labels this component original attack_db",
            "hackaprompt": "CC-BY-4.0; competition submissions, user-authored per publisher/research report",
            "harmbench": "MIT; behavior-goal component; task-label compatibility requires audit",
            "harmbench_benign": "MIT; benign counterpart component; provenance/creation compatibility requires audit",
            "wildguard_judgecomp": "Research; exclude unless separate permission is documented",
            "original": "Source mapping unresolved against the pinned card table; quarantine",
        },
        "interpretation_limits": [
            "augmented=false records the upstream flag; it does not independently prove human authorship",
            "native binary malicious labels do not determine PI versus JB without a documented category mapping",
            "source field values are not independent-family proof until upstream ancestry and overlap are checked",
            "row-level license fields are empty; licensing evidence is the pinned publisher card/source table",
        ],
        "prompt_text_emitted": False,
        "test_payload_opened": False,
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": "AUDIT_COMPLETE_TRAIN_ONLY",
        "rows": report["rows"],
        "components": {name: {"rows": item["rows"], "labels": item["native_label_counts"],
                              "categories": item["category_counts"],
                              "augmented": item["augmented_counts"],
                              "duplicate_excess_rows": item["duplicate_excess_rows"]}
                       for name, item in summary.items()},
        "duplicate_groups": report["normalized_duplicate_groups"],
        "duplicate_excess_rows": report["normalized_duplicate_excess_rows"],
        "cross_source_duplicate_groups": report["cross_source_duplicate_groups"],
        "report": str(OUT),
        "validation_opened": False,
        "test_opened": False,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
