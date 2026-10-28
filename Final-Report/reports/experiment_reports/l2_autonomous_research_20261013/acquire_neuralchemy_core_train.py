#!/usr/bin/env python3
"""Acquire only the pinned NeurAlchemy core training shard; never fetch eval data."""
from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import hashlib
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPORT = Path(__file__).resolve().parent
OUT_DIR = REPORT / "source_qualification" / "acquired"
DATASET = "neuralchemy/Prompt-injection-dataset"
REVISION = "7d70432dfcf47a821612cbf9d34e9d9e3ad20e75"
RELATIVE_FILE = "core/train-00000-of-00001.parquet"
URL = f"https://huggingface.co/datasets/{DATASET}/resolve/{REVISION}/{RELATIVE_FILE}"


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    destination = OUT_DIR / "neuralchemy_core_train.parquet"
    manifest_path = OUT_DIR / "neuralchemy_core_train_manifest.json"
    if destination.exists() or manifest_path.exists():
        raise FileExistsError("Refusing to overwrite an acquired source snapshot")
    request = urllib.request.Request(URL, headers={"User-Agent": "PI-Guard-local-research/1.0"})
    with urllib.request.urlopen(request, timeout=120) as response:
        if response.status != 200:
            raise RuntimeError(f"Unexpected HTTP status: {response.status}")
        raw = response.read()
    digest = hashlib.sha256(raw).hexdigest()
    with destination.open("xb") as stream:
        stream.write(raw)
        stream.flush()
    record = {
        "dataset_id": DATASET,
        "revision": REVISION,
        "file": RELATIVE_FILE,
        "url": URL,
        "acquired_at_utc": datetime.now(timezone.utc).isoformat(),
        "http_status": 200,
        "bytes": len(raw),
        "sha256": digest,
        "scope": "core train shard only; validation and test files were not requested or opened",
        "dataset_license_claim": "Apache-2.0",
        "upstream_license_policy": "filter or quarantine source families whose applicable source license is Research/unclear",
        "payload_executed": False,
    }
    manifest_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "ACQUIRED_TRAIN_ONLY", "bytes": len(raw), "sha256": digest,
                      "path": str(destination), "test_downloaded": False, "test_opened": False}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
