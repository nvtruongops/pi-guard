"""Pin publisher dataset metadata and cards without reading dataset rows or code."""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parent
IDS = [
    "wambosec/prompt-injections",
    "wambosec/prompt-injections-subtle",
    "rgeada/tool-response-injections",
    "S-Labs/prompt-injection-dataset",
    "allenai/wildjailbreak",
    "3nesdeniz/english-prompt-injection-3k",
    "3nesdeniz/agentic-prompt-injection-5k",
    "3nesdeniz/agentic-prompt-injection-boundary-pairs",
    "3nesdeniz/guardrail-hard-negatives",
    "neuralchemy/Prompt-injection-dataset",
]


def get(url):
    request = Request(url, headers={"User-Agent": "PI-Guard-source-qualification/1.0"})
    with urlopen(request, timeout=30) as response:
        body = response.read(512_001)
        if len(body) > 512_000:
            raise ValueError("metadata/card exceeded size limit")
        return response.status, body


def main():
    started = datetime.now(timezone.utc).isoformat()
    records = []
    for dataset_id in IDS:
        api_url = "https://huggingface.co/api/datasets/" + quote(dataset_id, safe="/") + "?files_metadata=true"
        entry = {"dataset_id": dataset_id, "api_url": api_url, "observed_utc": datetime.now(timezone.utc).isoformat()}
        try:
            status, body = get(api_url)
            metadata = json.loads(body)
            revision = metadata["sha"]
            card_url = "https://huggingface.co/datasets/" + dataset_id + "/resolve/" + revision + "/README.md"
            entry.update({
                "api_status": status,
                "revision": revision,
                "api_sha256": hashlib.sha256(body).hexdigest(),
                "card_url": card_url,
                "gated": metadata.get("gated"),
                "private": metadata.get("private"),
                "card_license_field": (metadata.get("cardData") or {}).get("license"),
                "tags": [tag for tag in metadata.get("tags", []) if tag.startswith(("license:", "language:", "format:"))],
                "siblings": [{"rfilename": s.get("rfilename"), "size": s.get("size"), "lfs": s.get("lfs")} for s in metadata.get("siblings", [])],
            })
            card_status, card = get(card_url)
            card_name = dataset_id.replace("/", "__") + "__README.md"
            (ROOT / card_name).write_bytes(card)
            entry.update({"card_status": card_status, "card_path": card_name, "card_sha256": hashlib.sha256(card).hexdigest(), "card_bytes": len(card)})
        except (HTTPError, URLError, ValueError, KeyError, json.JSONDecodeError) as error:
            entry["error"] = str(error)
        records.append(entry)
        print(json.dumps({k: entry.get(k) for k in ("dataset_id", "revision", "card_license_field", "gated", "error")}, ensure_ascii=False))
    manifest = {"started_utc": started, "finished_utc": datetime.now(timezone.utc).isoformat(), "collection": "publisher metadata and README only; no rows or executable files", "sources": records}
    (ROOT / "primary_metadata_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
