#!/usr/bin/env python3
"""Acquire and schema-audit the pinned Tensor Trust attacks dump for private L2 research."""
from __future__ import annotations

import bz2
import hashlib
import json
import shutil
import sys
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
PRIVATE_ROOT = Path(r"D:\Work\Do-an\workspaces\truongnv\pi_guard_pipeline")
TARGET = PRIVATE_ROOT / "training_bases" / "datasets" / "source_datasets" / "tensor_trust_human_attacks_candidate_round01"
ARCHIVE = TARGET / "raw_dump_attacks.jsonl.bz2"
SOURCE_MANIFEST = TARGET / "SOURCE_MANIFEST.json"
REPORT = HERE / "tensortrust_acquisition_round01.json"
REPOSITORY = "HumanCompatibleAI/tensor-trust-data"
REVISION = "747a75e096761ebc01bd3970158827326b4add23"
SOURCE_PATH = "raw-data/v2/raw_dump_attacks.jsonl.bz2"
EXPECTED_SIZE = 98_978_449
EXPECTED_GIT_BLOB_SHA1 = "3d8e42efce1b8ea9a7a36e3a78832b95e16b8c7b"
URL = f"https://raw.githubusercontent.com/{REPOSITORY}/{REVISION}/{SOURCE_PATH}"


def digest_file(path: Path, algorithm: str) -> str:
    digest = hashlib.new(algorithm)
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def git_blob_sha1(path: Path) -> str:
    size = path.stat().st_size
    digest = hashlib.sha1()
    digest.update(f"blob {size}\0".encode("ascii"))
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def value_type(value: object) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return type(value).__name__


def main() -> int:
    if REPORT.exists() or ARCHIVE.exists() or SOURCE_MANIFEST.exists():
        raise RuntimeError("Refusing to overwrite an existing acquisition or report")
    expected_parent = PRIVATE_ROOT.resolve()
    if not TARGET.resolve().is_relative_to(expected_parent):
        raise RuntimeError("Target must stay inside the private workspace")

    TARGET.mkdir(parents=True, exist_ok=True)
    partial = ARCHIVE.with_suffix(ARCHIVE.suffix + ".part")
    if partial.exists():
        raise RuntimeError("Refusing to overwrite an incomplete download")
    request = urllib.request.Request(URL, headers={"User-Agent": "PI-Guard-L2-research/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=60) as response, partial.open("xb") as out:
            shutil.copyfileobj(response, out, length=1024 * 1024)
        if partial.stat().st_size != EXPECTED_SIZE:
            raise RuntimeError("Downloaded byte count differs from the pinned GitHub tree metadata")
        if git_blob_sha1(partial) != EXPECTED_GIT_BLOB_SHA1:
            raise RuntimeError("Downloaded Git blob SHA-1 differs from the pinned source tree")
        partial.replace(ARCHIVE)

        field_types: dict[str, Counter[str]] = {}
        field_nonempty: Counter[str] = Counter()
        rows = 0
        with bz2.open(ARCHIVE, "rt", encoding="utf-8") as stream:
            for line_no, line in enumerate(stream, 1):
                record = json.loads(line)
                if not isinstance(record, dict):
                    raise RuntimeError(f"Expected one JSON object per line at line {line_no}")
                rows += 1
                for name, value in record.items():
                    field_types.setdefault(name, Counter())[value_type(value)] += 1
                    if value is not None and value != "":
                        field_nonempty[name] += 1

        manifest = {
            "dataset_id": REPOSITORY,
            "revision": REVISION,
            "source_path": SOURCE_PATH,
            "source_url": URL,
            "source_git_blob_sha1": EXPECTED_GIT_BLOB_SHA1,
            "archive_sha256": digest_file(ARCHIVE, "sha256"),
            "archive_bytes": ARCHIVE.stat().st_size,
            "rows": rows,
            "field_type_counts": {name: dict(sorted(counts.items())) for name, counts in sorted(field_types.items())},
            "field_nonempty_counts": dict(sorted(field_nonempty.items())),
            "source_rights": "The data repository has no LICENSE file; participant terms consent to research use and public release. Keep this copy and any derived training data private; no redistribution is authorized by this task.",
            "source_authorship": "The paper describes the attacks as human-generated submissions to the online game.",
            "data_role": "attack submissions only; candidate L2 PI research references, pending privacy and split qualification",
            "created_utc": datetime.now(timezone.utc).isoformat(),
            "raw_text_emitted": False,
            "user_identifiers_emitted": False,
            "final_test_opened": False,
        }
        encoded = json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
        SOURCE_MANIFEST.write_text(encoded, encoding="utf-8")
        REPORT.write_text(encoded, encoding="utf-8")
        print(json.dumps({
            "status": "ACQUIRED_AND_SCHEMA_AUDITED_PRIVATE_RESEARCH_ONLY",
            "dataset_id": REPOSITORY,
            "revision": REVISION,
            "rows": rows,
            "archive_bytes": ARCHIVE.stat().st_size,
            "archive_sha256": manifest["archive_sha256"],
            "fields": {name: dict(sorted(counts.items())) for name, counts in sorted(field_types.items())},
            "raw_text_emitted": False,
            "user_identifiers_emitted": False,
            "final_test_opened": False,
        }, ensure_ascii=False, indent=2))
        return 0
    except Exception:
        if partial.exists():
            partial.unlink()
        raise


if __name__ == "__main__":
    raise SystemExit(main())
