"""Screen additional original publishers using cards, repository trees, and HEAD only."""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parent
HF_IDS = ["jackhhao/jailbreak-classification", "Simsonsun/JailbreakPrompts", "yanismiraoui/prompt_injections"]
GITHUB_REPO = "mirzaakhi/prompt-injection-detection-dataset"


def fetch(url, method="GET", limit=512_000):
    with urlopen(Request(url, method=method, headers={"User-Agent": "PI-Guard-source-qualification/1.0", "Accept": "application/vnd.github+json"}), timeout=30) as response:
        body = b"" if method == "HEAD" else response.read(limit + 1)
        if len(body) > limit:
            raise RuntimeError("metadata exceeds limit")
        return response.status, body, response.headers


def main():
    records = []
    for dataset_id in HF_IDS:
        row = {"publisher": "huggingface", "dataset_id": dataset_id, "observed_utc": datetime.now(timezone.utc).isoformat()}
        try:
            api_url = "https://huggingface.co/api/datasets/" + quote(dataset_id, safe="/")
            status, body, _ = fetch(api_url)
            meta = json.loads(body)
            revision = meta["sha"]
            row.update({"api_url": api_url, "api_status": status, "revision": revision, "api_sha256": hashlib.sha256(body).hexdigest(), "license_field": (meta.get("cardData") or {}).get("license"), "gated": meta.get("gated"), "siblings": [s["rfilename"] for s in meta.get("siblings", [])]})
            card_url = "https://huggingface.co/datasets/" + dataset_id + "/resolve/" + revision + "/README.md"
            card_status, card, _ = fetch(card_url)
            card_name = dataset_id.replace("/", "__") + "__README.md"
            (ROOT / card_name).write_bytes(card)
            row.update({"card_url": card_url, "card_status": card_status, "card_name": card_name, "card_sha256": hashlib.sha256(card).hexdigest()})
            for path in row["siblings"]:
                if "train" in path.lower() and path.lower().endswith((".csv", ".parquet", ".tsv", ".jsonl")):
                    train_url = "https://huggingface.co/datasets/" + dataset_id + "/resolve/" + revision + "/" + quote(path, safe="/")
                    try:
                        head_status, _, headers = fetch(train_url, method="HEAD")
                        row.setdefault("train_heads", []).append({"path": path, "url": train_url, "status": head_status, "bytes": headers.get("Content-Length"), "etag": headers.get("ETag")})
                    except (HTTPError, URLError) as error:
                        row.setdefault("train_heads", []).append({"path": path, "url": train_url, "error": str(error)})
        except (HTTPError, URLError, RuntimeError, KeyError, ValueError) as error:
            row["error"] = str(error)
        records.append(row)
        print(json.dumps({k: row.get(k) for k in ("dataset_id", "revision", "license_field", "gated", "error")}, ensure_ascii=False))

    github = {"publisher": "github", "repository": GITHUB_REPO, "observed_utc": datetime.now(timezone.utc).isoformat()}
    try:
        api_url = "https://api.github.com/repos/" + GITHUB_REPO + "/commits/HEAD"
        _, body, _ = fetch(api_url)
        revision = json.loads(body)["sha"]
        github.update({"revision": revision, "commit_url": api_url, "commit_api_sha256": hashlib.sha256(body).hexdigest()})
        tree_url = "https://api.github.com/repos/" + GITHUB_REPO + "/git/trees/" + revision + "?recursive=1"
        _, body, _ = fetch(tree_url)
        tree = json.loads(body)
        github.update({"tree_url": tree_url, "tree_paths": [{"path": item["path"], "size": item.get("size"), "sha": item.get("sha")} for item in tree.get("tree", []) if item.get("type") == "blob"], "tree_api_sha256": hashlib.sha256(body).hexdigest()})
        for path in ("README.md", "LICENSE", "generate_dataset.py"):
            if path not in {item["path"] for item in github["tree_paths"]}:
                continue
            raw_url = "https://raw.githubusercontent.com/" + GITHUB_REPO + "/" + revision + "/" + path
            _, content, _ = fetch(raw_url, limit=250_000)
            name = "mirzaakhi__" + path
            (ROOT / name).write_bytes(content)
            github.setdefault("retrieved", {})[path] = {"url": raw_url, "local_name": name, "sha256": hashlib.sha256(content).hexdigest(), "bytes": len(content)}
    except (HTTPError, URLError, RuntimeError, KeyError, ValueError) as error:
        github["error"] = str(error)
    records.append(github)
    print(json.dumps({k: github.get(k) for k in ("repository", "revision", "error")}, ensure_ascii=False))
    output = {"finished_utc": datetime.now(timezone.utc).isoformat(), "kind": "publisher metadata/cards/code only; no dataset rows", "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), "sources": records}
    (ROOT / "additional_metadata_manifest.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
