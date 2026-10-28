"""Inspect published importer code and checksums as documents; never execute it."""
import hashlib
import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
HELPER = HERE.parent / "l2_v9_health_check_20261013/screen_public_sources.py"
spec = importlib.util.spec_from_file_location("public_fetch", HELPER)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
REPO = "rubyglask/llm-redteam-corpus-taxonomy"
OUT = HERE / "aggregate_importer_evidence"


def main():
    OUT.mkdir(exist_ok=False)
    refs, errors = [], []

    def fetch(name, url):
        try:
            data = helper.fetch(url)
            path = OUT / name
            assert path.resolve().is_relative_to(OUT.resolve())
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("xb") as stream:
                stream.write(data)
            refs.append({"path": name, "url": url, "sha256": hashlib.sha256(data).hexdigest(),
                         "bytes": len(data), "downloaded_at_utc": datetime.now(timezone.utc).isoformat()})
            return data
        except HTTPError as error:
            errors.append({"url": url, "http_status": error.code})
            return None

    revision = None
    try:
        repo = fetch("repository.json", f"https://api.github.com/repos/{REPO}")
        if repo:
            branch = json.loads(repo)["default_branch"]
            commit = fetch("commit.json", f"https://api.github.com/repos/{REPO}/commits/{branch}")
            if commit:
                revision = json.loads(commit)["sha"]
                tree = fetch("tree.json", f"https://api.github.com/repos/{REPO}/git/trees/{revision}?recursive=1")
                if tree:
                    tree = json.loads(tree)
                    assert not tree["truncated"]
                    files = [r["path"] for r in tree["tree"] if r["type"] == "blob"]
                    docs = [p for p in files if
                            (p.startswith("src/redteam_corpus/") and p.endswith(".py")) or
                            (p.startswith("docs/") and p.endswith(".md")) or
                            p in {"README.md", "METHODOLOGY.md", "DATASET_CARD.md", "LICENSE", "LICENSE-CODE", "pyproject.toml"} or
                            "checksum" in p.lower() or Path(p).name == "SHA256SUMS"]
                    assert len(docs) <= 100
                    for name in docs:
                        fetch(name, f"https://raw.githubusercontent.com/{REPO}/{revision}/{name}")
    finally:
        manifest = {"repository_id": REPO, "revision": revision, "documents": refs, "errors": errors,
                    "payload_downloaded": False, "source_code_executed": False,
                    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                    "finished_at_utc": datetime.now(timezone.utc).isoformat(),
                    "limitation": "Current publisher code is not automatically the original aggregate build commit"}
        with (OUT / "MANIFEST.json").open("x", encoding="utf-8") as stream:
            json.dump(manifest, stream, indent=2)
            stream.write("\n")
    print(json.dumps({"revision": revision, "documents": len(refs), "errors": errors, "payload_downloaded": False}))


if __name__ == "__main__":
    main()
