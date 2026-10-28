#!/usr/bin/env python3
"""Acquire only the pinned TrustAIRLab 2023-12 training shards for screening."""
from __future__ import annotations

import hashlib
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PRIVATE = Path(r"D:\Work\Do-an\workspaces\truongnv\pi_guard_pipeline")
DEST = PRIVATE / "training_bases" / "datasets" / "source_datasets" / "trustairlab_in_the_wild_candidate_round05"
REPO_ID = "TrustAIRLab/in-the-wild-jailbreak-prompts"
REVISION = "a10aab8eff1c73165a442d4464dce192bd28b9c5"
LICENSE = "MIT"
USER_AGENT = "PI-Guard-train-only-source-screen/1.0"
FILES = {
    "jailbreak_2023_12_25/train-00000-of-00001.parquet": 1405,
    "regular_2023_12_25/train-00000-of-00001.parquet": 13735,
}


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=120) as response:
        if response.status != 200:
            raise RuntimeError(f"Unexpected HTTP {response.status}: {url}")
        return response.read()


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    api_url = f"https://huggingface.co/api/datasets/{REPO_ID}/revision/{REVISION}?blobs=true"
    api = json.loads(fetch(api_url))
    if api.get("sha") != REVISION or api.get("gated"):
        raise RuntimeError("Pinned revision mismatch or gated source")
    card = api.get("cardData", {})
    if str(card.get("license", "")).lower() != LICENSE.lower():
        raise RuntimeError("Pinned Hub metadata does not declare MIT")
    siblings = {item.get("rfilename"): item for item in api.get("siblings", [])}
    if not set(FILES).issubset(siblings):
        raise RuntimeError("Pinned source lacks one of the declared train shards")

    dest = DEST.resolve()
    if not dest.is_relative_to(PRIVATE.resolve()):
        raise RuntimeError("TrustAIRLab destination escapes the ignored private workspace")
    manifest_path = dest / "ACQUISITION_MANIFEST.json"
    if manifest_path.exists():
        raise RuntimeError("Refusing to overwrite an existing TrustAIRLab acquisition")
    dest.mkdir(parents=True, exist_ok=True)

    records = {}
    payloads = {}
    for relative, expected_rows in FILES.items():
        sibling = siblings[relative]
        expected_sha = (sibling.get("lfs") or {}).get("sha256")
        if not expected_sha or len(expected_sha) != 64:
            raise RuntimeError(f"Pinned Hub SHA-256 unavailable for {relative}")
        target = dest / "data" / relative
        if target.exists():
            payload = target.read_bytes()
            observed_sha = sha(payload)
            if observed_sha != expected_sha:
                raise RuntimeError(f"Existing shard differs from pinned revision; refusing overwrite: {target}")
        else:
            url = f"https://huggingface.co/datasets/{REPO_ID}/resolve/{REVISION}/{relative}"
            payload = fetch(url)
            observed_sha = sha(payload)
            if observed_sha != expected_sha:
                raise RuntimeError(f"Pinned payload SHA-256 mismatch: {relative}")
            payloads[relative] = payload
        records[relative] = {"upstream_split": "train", "expected_rows": expected_rows,
                             "bytes": len(payload), "sha256": observed_sha,
                             "local_path": (Path("data") / relative).as_posix()}

    for relative, payload in payloads.items():
        target = dest / "data" / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)

    manifest = {
        "repository_id": REPO_ID,
        "revision": REVISION,
        "license_declared_by_publisher": LICENSE,
        "access_gated": False,
        "files": records,
        "split_scope": "train shards only",
        "validation_payload_opened": False,
        "test_payload_opened": False,
        "source_eval_payload_opened": False,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"result": "PASS_PINNED_TRAIN_ONLY_ACQUISITION",
                      "repository_id": REPO_ID, "revision": REVISION,
                      "file_rows": {name: info["expected_rows"] for name, info in records.items()},
                      "test_payload_opened": False, "manifest": str(manifest_path)},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
