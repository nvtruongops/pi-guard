"""Pin primary component documentation and Gandalf train, never evaluation payloads."""
import argparse
import hashlib
import importlib.util
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OLD = HERE.parent / "l2_v9_health_check_20261013/screen_public_sources.py"
spec = importlib.util.spec_from_file_location("public_fetch", OLD)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
SOURCES = [
    ("gandalf", "hf", "Lakera/gandalf_ignore_instructions"),
    ("aart", "hf", "walledai/AART"),
    ("do_not_answer", "hf", "LibrAI/do-not-answer"),
    ("forbidden_question_set", "hf", "TrustAIRLab/forbidden_question_set"),
    ("harmfulqa", "hf", "declare-lab/HarmfulQA"),
    ("jailbreakbench", "hf", "JailbreakBench/JBB-Behaviors"),
    ("tdc23", "hf", "walledai/TDC23-RedTeaming"),
    ("advbench", "github", "llm-attacks/llm-attacks"),
    ("harmbench", "github", "centerforaisafety/HarmBench"),
]
TRAIN_FILE = "data/train-00000-of-00001-ded53be747ff55cd.parquet"


def save(directory, name, url):
    data = helper.fetch(url)
    (directory / name).write_bytes(data)
    return data, {"path": str((directory / name).relative_to(HERE)).replace("\\", "/"),
                  "url": url, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data),
                  "downloaded_at_utc": datetime.now(timezone.utc).isoformat()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    OUT = args.output.resolve()
    if not OUT.is_relative_to(HERE):
        raise ValueError("Keep evidence in the task directory")
    OUT.mkdir(exist_ok=False)
    records = []
    for source_id, provider, repo in SOURCES:
        directory = OUT / source_id
        directory.mkdir()
        record = {"source_id": source_id, "repository_id": repo, "provider": provider,
                  "documents": [], "payload_downloaded": False, "terms_accepted": False}
        records.append(record)
        try:
            if provider == "hf":
                data, ref = save(directory, "metadata.json", f"https://huggingface.co/api/datasets/{repo}")
                record["documents"].append(ref)
                info = json.loads(data)
                revision = info["sha"]
                record.update(revision=revision, gated=info.get("gated"),
                              license_recorded=info.get("cardData", {}).get("license"))
                try:
                    card, ref = save(directory, "README.md", f"https://huggingface.co/datasets/{repo}/raw/{revision}/README.md")
                    record["documents"].append(ref)
                except HTTPError as exc:
                    record["card_access_error"] = exc.code
                if source_id == "gandalf":
                    assert revision == "04737b65e90a6794ec227012e4a255a7def6344b"
                    assert info.get("gated") is False and record["license_recorded"] == "mit"
                    assert "card_access_error" not in record
                    card_text = card.decode("utf-8").replace("[MIT License](https://opensource.org/license/mit/)", "MIT License")
                    assert "distributed under the MIT License" in card_text
                    assert TRAIN_FILE in {r["rfilename"] for r in info["siblings"]}
                    assert next(s for s in info["cardData"]["dataset_info"]["splits"] if s["name"] == "train")["num_examples"] == 777
                    _, ref = save(directory, "train.parquet", f"https://huggingface.co/datasets/{repo}/resolve/{revision}/{TRAIN_FILE}")
                    record.update(payload_downloaded=True, payload=ref, upstream_split="train", upstream_file=TRAIN_FILE)
            else:
                data, ref = save(directory, "metadata.json", f"https://api.github.com/repos/{repo}")
                record["documents"].append(ref)
                info = json.loads(data)
                branch = info["default_branch"]
                data, ref = save(directory, "commit.json", f"https://api.github.com/repos/{repo}/commits/{branch}")
                record["documents"].append(ref)
                revision = json.loads(data)["sha"]
                record.update(revision=revision, license_recorded=(info.get("license") or {}).get("spdx_id"))
                for filename in ("README.md", "LICENSE"):
                    try:
                        _, ref = save(directory, filename, f"https://raw.githubusercontent.com/{repo}/{revision}/{filename}")
                        record["documents"].append(ref)
                    except HTTPError as exc:
                        record.setdefault("document_errors", {})[filename] = exc.code
            record["status"] = "PRIMARY_METADATA_PINNED_NOT_ORIGINAL_AGGREGATE_REVISION_PROOF"
        except HTTPError as exc:
            record.update(status="METADATA_ACCESS_FAILED", http_status=exc.code)
    assert records[0]["payload_downloaded"] is True, "Gandalf train acquisition did not pass preflight"
    result = {"created_at_utc": datetime.now(timezone.utc).isoformat(), "sources": records,
              "downloaded_payload_count": sum(r["payload_downloaded"] for r in records),
              "upstream_validation_test_payloads_opened": False, "historical_locked_evaluation_opened": False,
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "fetch_helper_sha256": hashlib.sha256(OLD.read_bytes()).hexdigest(),
              "environment": {"python": platform.python_version(), "platform": platform.platform()}}
    (OUT / "MANIFEST.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"records": [{k: v for k, v in r.items() if k != "documents"} for r in records],
                      "manifest": str(OUT / "MANIFEST.json"), "payload_count": result["downloaded_payload_count"]}))


if __name__ == "__main__":
    main()
