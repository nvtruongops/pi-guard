"""Pin the aggregate's build documentation without opening its data files."""
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
HELPER = HERE.parent / "l2_v9_health_check_20261013/screen_public_sources.py"
spec = importlib.util.spec_from_file_location("public_fetch", HELPER)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
REPO = "RUBYGLASK/llm-redteam-corpus-taxonomy-core"
REV = "bbd1f5bd0941d1f297a5a8111c5af33f5621a750"
OUT = HERE / "aggregate_build_evidence"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    OUT.mkdir(exist_ok=False)
    manifest = {"repository_id": REPO, "revision": REV, "documents": [], "errors": [],
                "payload_downloaded": False, "upstream_evaluation_opened": False,
                "script_sha256": sha(Path(__file__)), "fetch_helper_sha256": sha(HELPER),
                "environment": {"python": platform.python_version(), "platform": platform.platform()}}

    def fetch(relative, url):
        try:
            data = helper.fetch(url)
            path = OUT / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("xb") as stream:
                stream.write(data)
            manifest["documents"].append({"path": relative, "url": url, "sha256": sha(path),
                "bytes": len(data), "downloaded_at_utc": datetime.now(timezone.utc).isoformat()})
            return data
        except HTTPError as error:
            manifest["errors"].append({"url": url, "http_status": error.code})
            return None

    try:
        tree = fetch("tree.json", f"https://huggingface.co/api/datasets/{REPO}/tree/{REV}?recursive=true&limit=1000")
        if tree is not None:
            entries = json.loads(tree)
            paths = [r["path"] for r in entries if r["type"] == "file"]
            manifest["repository_file_names"] = paths
            safe_docs = [p for p in paths if p == "README.md" or p.endswith(".py") or Path(p).name in {"LICENSE", "LICENSE.md", "requirements.txt"}]
            for relative in safe_docs:
                if ".." in Path(relative).parts:
                    raise ValueError("Unsafe publisher documentation path")
                fetch(relative, f"https://huggingface.co/datasets/{REPO}/raw/{REV}/{relative}")
            manifest["publisher_build_code_files"] = [p for p in safe_docs if p.endswith(".py")]
        source = ROOT / "workspaces/truongnv/pi_guard_pipeline/training_bases/datasets/project_training/history/pi_guard_v8_source_gate_20261010/corpus/candidates/rubyglask_core_components/snapshots/sources.json"
        manifest["already_staged_source_index_reused"] = {"path_from_repository": source.relative_to(ROOT).as_posix(), "sha256": sha(source)}
    finally:
        manifest["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
        with (OUT / "MANIFEST.json").open("x", encoding="utf-8") as stream:
            json.dump(manifest, stream, indent=2)
            stream.write("\n")
    print(json.dumps({"documents": len(manifest["documents"]), "build_code_files": manifest.get("publisher_build_code_files"),
                      "errors": manifest["errors"], "payload_downloaded": False}))


if __name__ == "__main__":
    main()
