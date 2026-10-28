"""Local structural audit of acquired train only; never display prompt text."""

import hashlib
import json
import re
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
TRAIN = ROOT / "acquired" / "train.jsonl"


def normalize(value):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", value).casefold()).strip()


def main():
    rows = [json.loads(line) for line in TRAIN.read_text(encoding="utf-8").splitlines()]
    pair_rows = defaultdict(list)
    scenario_rows = defaultdict(list)
    normalized_hashes = Counter()
    for row in rows:
        pair_rows[row["pair_id"]].append(row)
        scenario_rows[row["scenario_id"]].append(row)
        normalized_hashes[hashlib.sha256(normalize(row["text"]).encode("utf-8")).hexdigest()] += 1
    pair_failures = 0
    pair_family_counts = Counter()
    for pair in pair_rows.values():
        if len(pair) != 2 or {r["label"] for r in pair} != {0, 1} or len({r["scenario_id"] for r in pair}) != 1:
            pair_failures += 1
        attack = next((r for r in pair if r["label"] == 1), None)
        if attack:
            pair_family_counts[attack["attack_family"]] += 1
    output = {
        "observed_utc": datetime.now(timezone.utc).isoformat(),
        "source_path": "acquired/train.jsonl",
        "source_sha256": hashlib.sha256(TRAIN.read_bytes()).hexdigest(),
        "rows": len(rows),
        "pair_ids": len(pair_rows),
        "pair_integrity_failures": pair_failures,
        "scenario_ids": len(scenario_rows),
        "scenario_row_counts": dict(sorted(Counter(len(v) for v in scenario_rows.values()).items())),
        "attack_pair_family_counts": dict(sorted(pair_family_counts.items())),
        "normalized_text_duplicate_groups": sum(n > 1 for n in normalized_hashes.values()),
        "normalized_text_duplicate_excess_rows": sum(n - 1 for n in normalized_hashes.values() if n > 1),
        "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "limits": "train-only exact/normalized audit; no cross-source or near-duplicate audit; no label adjudication",
    }
    (ROOT / "train_structure_audit.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: output[k] for k in ("rows", "pair_ids", "pair_integrity_failures", "scenario_ids", "scenario_row_counts", "attack_pair_family_counts", "normalized_text_duplicate_groups", "normalized_text_duplicate_excess_rows")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
