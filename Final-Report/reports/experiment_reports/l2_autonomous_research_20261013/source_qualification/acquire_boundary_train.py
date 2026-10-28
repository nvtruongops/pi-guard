"""Acquire one pinned licensed publisher train file; never request validation/test."""

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parent
DATASET_ID = "3nesdeniz/agentic-prompt-injection-boundary-pairs"
REVISION = "a5682e7573e1c7bc4b12e64d49c0dcd90ca776cf"
TRAIN_PATH = "data/train.jsonl"
MAX_BYTES = 10_000_000


def fetch(path, max_bytes):
    url = "https://huggingface.co/datasets/" + DATASET_ID + "/resolve/" + REVISION + "/" + quote(path, safe="/")
    with urlopen(Request(url, headers={"User-Agent": "PI-Guard-source-qualification/1.0"}), timeout=45) as response:
        if response.status != 200:
            raise RuntimeError(f"HTTP {response.status}: {path}")
        body = response.read(max_bytes + 1)
        if len(body) > max_bytes:
            raise RuntimeError(f"size limit exceeded: {path}")
    return url, body


def main():
    metadata = json.loads((ROOT / "primary_metadata_manifest.json").read_text(encoding="utf-8"))
    source = next(s for s in metadata["sources"] if s["dataset_id"] == DATASET_ID)
    if source["revision"] != REVISION or source["card_license_field"] != "cc-by-4.0" or source["gated"]:
        raise RuntimeError("pinned metadata/license/gate mismatch")
    headers = json.loads((ROOT / "train_file_headers.json").read_text(encoding="utf-8"))
    header = next(f for f in headers["files"] if f["dataset_id"] == DATASET_ID)
    if header["train_path"] != TRAIN_PATH or header["status"] != 200 or int(header["content_length"]) > MAX_BYTES:
        raise RuntimeError("train path or HEAD size gate failed")

    acquired = ROOT / "acquired"
    acquired.mkdir(exist_ok=True)
    artifacts = {}
    for path, name, limit in [
        ("LICENSE", "LICENSE", 20_000),
        ("metadata/checksums.sha256", "checksums.sha256", 20_000),
        ("metadata/schema.json", "schema.json", 50_000),
        ("metadata/review_log.md", "review_log.md", 100_000),
        ("scripts/build_dataset.rb", "build_dataset.rb", 200_000),
    ]:
        url, body = fetch(path, limit)
        (acquired / name).write_bytes(body)
        artifacts[path] = {"url": url, "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest()}
    license_text = (acquired / "LICENSE").read_text(encoding="utf-8", errors="replace")
    if "Creative Commons Attribution 4.0" not in license_text and "CC BY 4.0" not in license_text:
        raise RuntimeError("publisher LICENSE does not identify CC BY 4.0")

    train_url, body = fetch(TRAIN_PATH, MAX_BYTES)
    actual_hash = hashlib.sha256(body).hexdigest()
    checksum_lines = (acquired / "checksums.sha256").read_text(encoding="utf-8").splitlines()
    matching = [line for line in checksum_lines if line.strip().endswith(TRAIN_PATH)]
    if len(matching) != 1 or matching[0].split()[0].lower() != actual_hash:
        raise RuntimeError("publisher train checksum mismatch")
    (acquired / "train.jsonl").write_bytes(body)

    keys = Counter()
    labels = Counter()
    categories = Counter()
    families = Counter()
    languages = Counter()
    splits = Counter()
    text_hashes = set()
    duplicate_exact_text = 0
    for lineno, line in enumerate(body.decode("utf-8").splitlines(), 1):
        row = json.loads(line)
        keys.update(row.keys())
        labels.update([str(row.get("label"))])
        categories.update([str(row.get("category"))])
        families.update([str(row.get("attack_family"))])
        languages.update([str(row.get("language"))])
        splits.update([str(row.get("split"))])
        prompt_text = row.get("text")
        if not isinstance(prompt_text, str) or not prompt_text.strip():
            raise RuntimeError(f"missing/empty text at line {lineno}")
        text_hash = hashlib.sha256(prompt_text.encode("utf-8")).digest()
        duplicate_exact_text += text_hash in text_hashes
        text_hashes.add(text_hash)
    if set(splits) != {"train"} or set(languages) != {"en"}:
        raise RuntimeError("train split or English-only gate failed")
    result = {
        "observed_utc": datetime.now(timezone.utc).isoformat(),
        "dataset_id": DATASET_ID,
        "revision": REVISION,
        "license": "cc-by-4.0; publisher LICENSE verified",
        "train_url": train_url,
        "train_path": "acquired/train.jsonl",
        "train_bytes": len(body),
        "train_sha256": actual_hash,
        "publisher_checksum_match": True,
        "row_count": sum(labels.values()),
        "field_presence_counts": dict(sorted(keys.items())),
        "native_label_counts": dict(sorted(labels.items())),
        "native_category_counts": dict(sorted(categories.items())),
        "native_attack_family_counts": dict(sorted(families.items())),
        "language_counts": dict(sorted(languages.items())),
        "split_counts": dict(sorted(splits.items())),
        "exact_text_duplicate_count": duplicate_exact_text,
        "supporting_artifacts": artifacts,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "note": "Native labels only; no PI-Guard mapping or gold-label claim. No validation/test row requested.",
    }
    (ROOT / "acquisition_manifest.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("dataset_id", "revision", "train_bytes", "train_sha256", "row_count", "native_label_counts", "native_category_counts", "native_attack_family_counts", "language_counts", "split_counts", "exact_text_duplicate_count")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
