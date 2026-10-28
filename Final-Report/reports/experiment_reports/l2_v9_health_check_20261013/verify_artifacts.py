"""Verify the report and its current evidence, with full separate check logs."""
import ast
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    logs = HERE / "verification_logs"
    logs.mkdir(exist_ok=False)
    records = []
    python = sys.executable
    checks = [
        ("audit_self_check", [python, "-B", "-X", "utf8", str(HERE / "audit_v9_l2.py"), "--output", str(HERE / "run_20261013_round04_verified"), "--self-check"]),
        ("scope_report", [python, "-B", "-X", "utf8", str(REPO / "Final-Report/scripts/audit_task_scope.py"), "--file", str(HERE / "REPORT.md"), "--strict"]),
        ("claims_report", [python, "-B", "-X", "utf8", str(REPO / "Final-Report/scripts/audit_claim_evidence.py"), "--file", str(HERE / "REPORT.md")]),
        ("claims_handoff", [python, "-B", "-X", "utf8", str(REPO / "Final-Report/scripts/audit_claim_evidence.py"), "--file", str(HERE / "HUMAN_REVIEW_HANDOFF.md")]),
        ("glossary_report", [python, "-B", "-X", "utf8", str(REPO / "Final-Report/scripts/verify_academic_glossary.py"), "--file", str(HERE / "REPORT.md")]),
        ("protected_paths", [python, "-B", "-X", "utf8", str(REPO / "Final-Report/scripts/audit_workspace_boundaries.py"), "--mode", "working_tree"]),
    ]
    for name, command in checks:
        result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
        (logs / (name + ".log")).write_text(result.stdout + result.stderr, encoding="utf-8")
        records.append({"name": name, "command": command, "exit_code": result.returncode, "log": "verification_logs/" + name + ".log"})
    own_files = [HERE / name for name in ("audit_v9_l2.py", "screen_public_sources.py", "verify_artifacts.py")]
    for path in own_files:
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    records.append({"name": "python_syntax_no_bytecode", "exit_code": 0, "files": [path.name for path in own_files]})
    link_count = 0
    for name in ("REPORT.md", "HUMAN_REVIEW_HANDOFF.md"):
        path = HERE / name
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            if target.startswith(("https://", "http://")):
                continue
            file_part, _, fragment = unquote(target).partition("#")
            dest = path if not file_part else (path.parent / file_part).resolve()
            # VERIFICATION is the report currently being produced.
            assert dest.is_file() or dest == HERE / "VERIFICATION.json", "Missing local link: " + target
            if fragment:
                text = dest.read_text(encoding="utf-8")
                assert 'id="' + fragment + '"' in text, "Missing explicit evidence anchor: " + target
            link_count += 1
    records.append({"name": "local_file_and_evidence_links", "exit_code": 0, "links_checked": link_count})
    audit = json.loads((HERE / "run_20261013_round04_verified/audit.json").read_text())
    v8 = REPO / "workspaces/truongnv/pi_guard_pipeline/training_bases/datasets/project_training/history/pi_guard_v8_english_diagnostic_20261012"
    for relative, expected in audit["v8_current_file_sha256"].items():
        assert sha(v8 / relative) == expected, "Historical current-file integrity changed: " + relative
    records.append({"name": "fresh_current_v8_file_hashes", "exit_code": 0, "files_checked": len(audit["v8_current_file_sha256"]), "original_bundle_mismatches_remain_reported": len(audit["v8_original_english_bundle_hash_mismatches"])})
    metadata = json.loads((HERE / "public_source_metadata_20261013/manifest.json").read_text())
    for source in metadata["records"]:
        assert source["payload_downloaded"] is False and source["eligible_families_added"] == 0
        for doc in source["documents"]:
            path = HERE / "public_source_metadata_20261013" / source["repository_id"].replace("/", "__") / doc["document"].replace("/", "__")
            assert sha(path) == doc["sha256"]
    records.append({"name": "pinned_public_metadata_hashes", "exit_code": 0, "sources_checked": len(metadata["records"]), "prompt_payloads_downloaded": 0})
    gate = json.loads((HERE / "OWNER_GATE_DECLARATION.json").read_text())
    assert gate["owner_code"] is None and gate["approved_at_utc"] is None
    assert audit["outcome"] == "BLOCKED" and audit["health_check_status"] == "NOT_READY"
    records.append({"name": "unapproved_gates_remain_closed", "exit_code": 0})
    value = {"created_utc": datetime.now(timezone.utc).isoformat(), "status": "PASS" if all(row["exit_code"] == 0 for row in records) else "FAIL", "scope": "Artifact integrity and focused report checks only; no L2 PASS claim", "checks": records, "script_sha256": sha(Path(__file__))}
    (HERE / "VERIFICATION.json").write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": value["status"], "checks": len(records), "failed": [row["name"] for row in records if row["exit_code"] != 0]}))
    return 0 if value["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
