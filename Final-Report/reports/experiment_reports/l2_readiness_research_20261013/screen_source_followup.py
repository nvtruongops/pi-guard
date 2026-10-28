"""Pin three additional primary dataset cards, with no payload or access agreement."""
import argparse
import hashlib
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError

HERE = Path(__file__).resolve().parent
PREVIOUS = HERE.parent / "l2_v9_health_check_20261013"
spec = importlib.util.spec_from_file_location("metadata_fetch", PREVIOUS / "screen_public_sources.py")
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
REPOS = ["ai-mitra/prompt-injection-dataset", "ScaleAI/mhj", "Mindgard/evaded-prompt-injection-and-jailbreak-samples"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    OUT = args.output.resolve()
    if not OUT.is_relative_to(HERE):
        raise ValueError("Keep this research output within the task directory")
    if OUT.exists():
        raise RuntimeError("Never overwrite a source-research round")
    OUT.mkdir()
    records = []
    for repo in REPOS:
        directory = OUT / repo.replace("/", "__")
        directory.mkdir()
        info_url = f"https://huggingface.co/api/datasets/{repo}"
        info_bytes = helper.fetch(info_url)
        info = json.loads(info_bytes)
        revision = info["sha"]
        url = f"https://huggingface.co/datasets/{repo}/raw/{revision}/README.md"
        (directory / "metadata.json").write_bytes(info_bytes)
        card_bytes = None
        error = None
        try:
            card_bytes = helper.fetch(url)
        except HTTPError as exc:
            error = {"http_status": exc.code, "reason": str(exc.reason)}
        if card_bytes is not None:
            (directory / "README.md").write_bytes(card_bytes)
        records.append({"repository_id": repo, "revision": revision, "gated_recorded": info.get("gated"),
                        "license_recorded": info.get("cardData", {}).get("license"),
                        "card_url": url, "card_sha256": hashlib.sha256(card_bytes).hexdigest() if card_bytes is not None else None,
                        "card_access_error": error,
                        "metadata_sha256": hashlib.sha256(info_bytes).hexdigest(),
                        "metadata_url": info_url, "payload_downloaded": False, "terms_accepted": False,
                        "eligible_families_added": 0, "disposition": "UNQUALIFIED_PROSPECT_METADATA_ONLY"})
    (OUT / "manifest.json").write_text(json.dumps({"fetched_at_utc": datetime.now(timezone.utc).isoformat(),
        "records": records, "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "fetch_helper_sha256": hashlib.sha256((PREVIOUS / "screen_public_sources.py").read_bytes()).hexdigest()}, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"records": records}))


if __name__ == "__main__":
    main()
