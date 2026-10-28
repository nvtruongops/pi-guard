"""Finalize this bounded research round's ledger and artifact hashes."""
import hashlib
import json
import platform
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write(name, value):
    path = HERE / name
    if path.exists():
        raise ValueError("Final records must not overwrite a previous record")
    with path.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(value, indent=2) + "\n")


def main():
    links = []
    for document in (HERE / "TASK.md", HERE / "REPORT.md", HERE / "CURATOR_HANDOFF.md"):
        for target in re.findall(r"\]\(([^)]+)\)", document.read_text(encoding="utf-8")):
            if target.startswith(("https://", "http://", "#")):
                continue
            resolved = (document.parent / target.split("#")[0]).resolve()
            assert resolved.is_relative_to(ROOT) and resolved.exists(), str(resolved)
            links.append({"document": document.name, "target": target})
    write("LOCAL_LINK_VERIFICATION.json", {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
                                          "status": "PASS", "links_checked": len(links), "links": links})
    manifest = ROOT / "workspaces/truongnv/pi_guard_pipeline/training_bases/datasets/project_training/versions/pi_guard_v10_english_readiness_20261013/DATASET_MANIFEST.json"
    ledger = []
    for name in ("prepare_v10.command.json", "curator_intake_r01.command.json", "source_followup.command.json", "source_followup_r02.command.json"):
        entry = read(HERE / name)
        uses_data = name.startswith(("prepare", "curator"))
        entry.update(command_record=name,
                     dataset_version="10.0.0-candidate-english-lineage" if uses_data else "none:metadata-only",
                     dataset_manifest_sha256=sha(manifest) if uses_data else None,
                     configuration="Candidate selection/rubric pinned in script; no model fit" if uses_data else "Primary publisher metadata/card only; no terms accepted",
                     split_sha256=None, seed=42 if name.startswith("prepare") else "not_applicable:deterministic_metadata_check",
                     environment={"python": platform.python_version(), "platform": platform.platform()})
        ledger.append(entry)
    write("RUN_LEDGER.json", {"previous_ledger": "../l2_v9_health_check_20261013/RUN_LEDGER.json", "runs": ledger,
                              "verification": "VERIFICATION.json",
                              "standalone_self_check": {"result": "curator_self_check_r01.json", "log": "curator_self_check_r01.log",
                                  "command": "python -B -X utf8 check_curated_candidate.py --self-check --output curator_self_check_r01.json",
                                  "exit_code": 0, "timestamp_limitation": "Exact start time was not captured; no timestamp is invented."},
                              "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
                              "dirty_working_tree": True, "no_training_metrics_created": True})
    status = subprocess.check_output(["git", "status", "--short"], cwd=ROOT, text=True)
    (HERE / "git_status_final.txt").write_text(status, encoding="utf-8")
    files = {p.relative_to(HERE).as_posix(): {"sha256": sha(p), "bytes": p.stat().st_size}
             for p in HERE.rglob("*") if p.is_file() and p.name != "ARTIFACT_MANIFEST.json"}
    write("ARTIFACT_MANIFEST.json", {"created_at_utc": datetime.now(timezone.utc).isoformat(), "files": files,
                                    "private_candidate_manifest_sha256": sha(manifest), "local_links_status": "PASS",
                                    "l2_health_status": "NOT_READY", "overall_l2_goal_achieved": False})
    print(json.dumps({"artifact_files": len(files), "local_links_checked": len(links),
                      "artifact_checks": read(HERE / "VERIFICATION.json")["status"],
                      "data_manifest_sha256": sha(manifest), "working_tree_status": status}))


if __name__ == "__main__":
    main()
