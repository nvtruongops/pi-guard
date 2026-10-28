"""Inspect only HTTP headers of pinned publisher training files."""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parent
PATHS = {
    "wambosec/prompt-injections": "data/train-00000-of-00001.parquet",
    "wambosec/prompt-injections-subtle": "data/train-00000-of-00001.parquet",
    "rgeada/tool-response-injections": "tool_response_injections_train.csv",
    "S-Labs/prompt-injection-dataset": "data/train.csv",
    "allenai/wildjailbreak": "train/train.tsv",
    "3nesdeniz/english-prompt-injection-3k": "data/train.parquet",
    "3nesdeniz/agentic-prompt-injection-5k": "data/train.parquet",
    "3nesdeniz/agentic-prompt-injection-boundary-pairs": "data/train.jsonl",
    "3nesdeniz/guardrail-hard-negatives": "data/train.parquet",
    "neuralchemy/Prompt-injection-dataset": "core/train-00000-of-00001.parquet",
}


def main():
    manifest_path = ROOT / "primary_metadata_manifest.json"
    metadata = json.loads(manifest_path.read_text(encoding="utf-8"))
    rows = []
    for source in metadata["sources"]:
        dataset_id = source["dataset_id"]
        path = PATHS[dataset_id]
        url = "https://huggingface.co/datasets/" + dataset_id + "/resolve/" + source["revision"] + "/" + quote(path, safe="/")
        row = {"dataset_id": dataset_id, "revision": source["revision"], "train_path": path, "url": url, "observed_utc": datetime.now(timezone.utc).isoformat()}
        try:
            with urlopen(Request(url, method="HEAD", headers={"User-Agent": "PI-Guard-source-qualification/1.0"}), timeout=30) as response:
                row.update({"status": response.status, "content_length": response.headers.get("Content-Length"), "etag": response.headers.get("ETag"), "x_linked_etag": response.headers.get("X-Linked-ETag")})
        except (HTTPError, URLError) as error:
            row.update({"error": str(error), "status": getattr(error, "code", None)})
        rows.append(row)
        print(json.dumps({k: row.get(k) for k in ("dataset_id", "status", "content_length", "etag", "error")}, ensure_ascii=False))
    output = {"kind": "HTTP HEAD only; no dataset payloads", "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), "finished_utc": datetime.now(timezone.utc).isoformat(), "files": rows}
    (ROOT / "train_file_headers.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
