#!/usr/bin/env python3
"""Verify local JBB-Behaviors rows against one pinned Hugging Face revision."""

from __future__ import annotations

import csv
import hashlib
import io
import json
import sys
from pathlib import Path
from urllib.request import urlopen

REVISION = "d8d87b8fdcb7806e3b4e45fffb2bc24aa6b17f32"
BASE_URL = (
    "https://huggingface.co/datasets/JailbreakBench/JBB-Behaviors/"
    f"resolve/{REVISION}/data/"
)
DATA_DIR = Path(__file__).resolve().parent / "datasets"
SPLITS = {
    "harmful": {
        "source": "harmful-behaviors.csv",
        "local_csv": "jbb_behaviors_harmful.csv",
        "local_json": "jbb_behaviors_harmful.json",
        "source_sha256": "4a8ec6832056b631eb092dccc60d37a61c3d441268268888b3d006288afeffa1",
        "csv_sha256": "f985615b17b7659a7598f751a3c1fe0704e80d4f966d6ba36b6777d53ad18150",
        "json_sha256": "9ee1cb2aab52550f0817f036e4423e9f3cc05a6bb5a0084da404f1817d535e77",
    },
    "benign": {
        "source": "benign-behaviors.csv",
        "local_csv": "jbb_behaviors_benign.csv",
        "local_json": "jbb_behaviors_benign.json",
        "source_sha256": "3cda234d21a991fa309bbfea4b6d9dae31ccdf8e9d452424b6a983e4fdc33468",
        "csv_sha256": "b198c96c550710bfcdb6e6b9e567003e0c7c12c94bd25c47b09412909f2a6ab2",
        "json_sha256": "fac2026f7305db38d1bb58037cec1c95867c7298c8a33f71d33ad76df04bd898",
    },
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def rows_from_csv_bytes(data: bytes) -> list[dict[str, str]]:
    text = data.decode("utf-8-sig")
    return list(csv.DictReader(io.StringIO(text, newline="")))


def normalized_rows(rows: list[dict]) -> list[dict[str, str]]:
    return [{str(key): str(value) for key, value in row.items()} for row in rows]


def verify_split(name: str, spec: dict[str, str]) -> None:
    with urlopen(BASE_URL + spec["source"], timeout=30) as response:
        source_bytes = response.read()

    if sha256(source_bytes) != spec["source_sha256"]:
        raise ValueError(f"{name}: pinned upstream CSV hash changed")

    local_csv_bytes = (DATA_DIR / spec["local_csv"]).read_bytes()
    local_json_bytes = (DATA_DIR / spec["local_json"]).read_bytes()
    if sha256(local_csv_bytes) != spec["csv_sha256"]:
        raise ValueError(f"{name}: local CSV hash changed")
    if sha256(local_json_bytes) != spec["json_sha256"]:
        raise ValueError(f"{name}: local JSON hash changed")

    source_rows = normalized_rows(rows_from_csv_bytes(source_bytes))
    local_csv_rows = normalized_rows(rows_from_csv_bytes(local_csv_bytes))
    local_json_rows = normalized_rows(json.loads(local_json_bytes.decode("utf-8")))

    if len(source_rows) != 100:
        raise ValueError(f"{name}: expected 100 upstream records, got {len(source_rows)}")
    if source_rows != local_csv_rows or source_rows != local_json_rows:
        raise ValueError(f"{name}: row/field mismatch against pinned source")

    print(f"PASS {name}: 100 rows; every source field matches CSV and JSON")


def main() -> int:
    try:
        for name, spec in SPLITS.items():
            verify_split(name, spec)
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print(f"PASS pinned revision {REVISION}; local byte serialization differs from upstream.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
