"""Pin public metadata for two new prospects; never fetch data payloads."""
import hashlib
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "public_source_metadata_20261013"
PROSPECTS = {
    "SoheilKhodayari/in_page_prompt_injection_pub": ["README.md", "data/README.md"],
    "mtasci42/moltbook-a2a-prompt-injection": ["README.md"],
}


def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": "PI-Guard-L2-evidence-audit", "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(request, timeout=45) as response:
        assert response.status == 200
        data = response.read(2_000_001)
        assert len(data) < 2_000_001, "Metadata size cap exceeded"
        return data


def main():
    assert not OUT.exists(), "Never overwrite a metadata run"
    OUT.mkdir()
    records = []
    for repo, documents in PROSPECTS.items():
        commit_url = f"https://api.github.com/repos/{repo}/commits/main"
        commit_bytes = fetch(commit_url)
        commit = json.loads(commit_bytes)
        revision = commit["sha"]
        directory = OUT / repo.replace("/", "__")
        directory.mkdir()
        (directory / "commit.json").write_bytes(commit_bytes)
        tree_url = f"https://api.github.com/repos/{repo}/git/trees/{revision}?recursive=1"
        tree_bytes = fetch(tree_url)
        (directory / "tree.json").write_bytes(tree_bytes)
        docs = []
        for document in documents:
            assert document in ("README.md", "data/README.md")
            url = f"https://raw.githubusercontent.com/{repo}/{revision}/{document}"
            payload = fetch(url)
            target = directory / document.replace("/", "__")
            target.write_bytes(payload)
            docs.append({"document": document, "url": url, "sha256": hashlib.sha256(payload).hexdigest(), "bytes": len(payload), "http_status": 200})
        records.append({"repository_id": repo, "revision": revision,
                        "source_commit_time": commit["commit"]["committer"]["date"],
                        "commit_metadata_url": commit_url, "tree_metadata_url": tree_url,
                        "documents": docs, "payload_downloaded": False,
                        "eligible_families_added": 0, "disposition": "QUARANTINE_METADATA_ONLY_PENDING_LINEAGE_CONTEXT_PRIVACY_AND_CURATOR_GATES"})
    result = {"fetched_at_utc": datetime.now(timezone.utc).isoformat(),
              "scope": "Public repository documentation and file-tree metadata only; no prompt or evaluation payloads.",
              "records": records, "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (OUT / "manifest.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"repositories": len(records), "payload_downloaded": False,
                      "eligible_families_added": 0, "manifest": str(OUT / "manifest.json")}))


if __name__ == "__main__":
    main()
