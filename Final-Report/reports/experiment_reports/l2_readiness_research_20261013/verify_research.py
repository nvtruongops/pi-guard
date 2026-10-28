"""Verify real research artifacts and immutable parent/source identities."""
import csv
import hashlib
import importlib.util
import json
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BASE = ROOT / "workspaces/truongnv/pi_guard_pipeline/training_bases"
PROJECT = BASE / "datasets/project_training"
V10 = PROJECT / "versions/pi_guard_v10_english_readiness_20261013"
V9 = PROJECT / "versions/pi_guard_v9_english_source_heldout_20261013"
CHECKER = BASE / "pi_guard_tfidf_tier1/check_curated_candidate.py"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main():
    logs = HERE / "verification_logs"
    logs.mkdir(exist_ok=False)
    checks = []
    manifest = read(V10 / "DATASET_MANIFEST.json")
    for name, ref in manifest["files"].items():
        assert sha(V10 / name) == ref["sha256"], name
    assert sha(HERE / "prepare_v10_candidate.py") == manifest["code_sha256"]
    integrity = read(V10 / "provenance/PARENT_INTEGRITY.json")
    current = {p.relative_to(V9).as_posix(): sha(p) for p in V9.rglob("*") if p.is_file()}
    assert current == integrity["v9_files_sha256_before_and_after_equal"]
    for relative, expected in integrity["source_evidence_sha256"].items():
        assert sha(PROJECT / relative) == expected
    checks.append({"name": "candidate_and_parent_source_integrity", "status": "PASS",
                   "v9_files_verified": len(current), "source_files_verified": len(integrity["source_evidence_sha256"])})
    with (V10 / "annotation/source_blind_pilot.csv").open(encoding="utf-8", newline="") as stream:
        sheet = list(csv.DictReader(stream))
    keys = [json.loads(line) for line in (V10 / "provenance/curator_key_pilot.jsonl").read_text(encoding="utf-8").splitlines()]
    index = [json.loads(line) for line in (V10 / "provenance/english_candidate_index.jsonl").read_text(encoding="utf-8").splitlines()]
    assert len(sheet) == len(keys) == 96 and len(index) == 56498
    assert len({r["duplicate_group_id"] for r in keys}) == 96
    assert len({r["source_family_id"] for r in keys}) == 10
    assert all(not r[k] for r in sheet for k in ("curator_label", "final_label", "curator_code", "annotated_at_utc"))
    assert sum(r["original_component_split"] is None for r in index) == 4476
    assert all(r["upstream_split_recorded"] for r in index)
    groups = defaultdict(set)
    sizes = Counter()
    for row in index:
        groups[row["duplicate_group_id"]].add(row["source_family_id"])
        sizes[row["duplicate_group_id"]] += 1
    cross = [gid for gid, families in groups.items() if len(families) > 1]
    assert len(cross) == 25 and sum(sizes[g] for g in cross) == 78
    assert not set(cross) & {r["duplicate_group_id"] for r in keys}
    spec = importlib.util.spec_from_file_location("curator_intake", CHECKER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = module.self_check(V10)
    (logs / "intake_self_check.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    checks.append({"name": "real_candidate_counts_bindings_and_fail_closed_intake", "status": "PASS", "pilot_rows": 96})
    for folder in (HERE / "source_followup", HERE / "source_followup_r02"):
        if not (folder / "manifest.json").exists():
            continue  # Initial partial failure is retained in its log and snapshot.
        for record in read(folder / "manifest.json")["records"]:
            directory = folder / record["repository_id"].replace("/", "__")
            assert sha(directory / "metadata.json") == record["metadata_sha256"]
            if record["card_sha256"]:
                assert sha(directory / "README.md") == record["card_sha256"]
            assert record["payload_downloaded"] is False and record["terms_accepted"] is False
    failed = read(HERE / "source_followup.command.json")
    assert failed["exit_code"] == 1
    assert sha(HERE / "screen_source_followup_r01_failed_snapshot.py") == failed["script_sha256"]
    assert read(HERE / "source_followup_r02.command.json")["exit_code"] == 0
    checks.append({"name": "source_metadata_and_failed_run_preserved", "status": "PASS"})
    for filename in ("prepare_v10.command.json", "curator_intake_r01.command.json"):
        command = read(HERE / filename)
        assert command["exit_code"] == 0 and command["started_at_utc"] and command["ended_at_utc"]
    assert read(HERE / "curator_intake_r01.json")["script_sha256"] == sha(CHECKER)
    assert manifest["trainable"] is False and manifest["split_sha256"] is None
    checks.append({"name": "run_code_and_data_identities", "status": "PASS"})
    commands = [
        ("scope", [sys.executable, "-B", "-X", "utf8", "Final-Report/scripts/audit_task_scope.py", "--file", str(HERE / "REPORT.md"), "--strict"]),
        ("claims", [sys.executable, "-B", "-X", "utf8", "Final-Report/scripts/audit_claim_evidence.py", "--file", str(HERE / "REPORT.md")]),
        ("glossary", [sys.executable, "-B", "-X", "utf8", "Final-Report/scripts/verify_academic_glossary.py", "--file", str(HERE / "REPORT.md")]),
        ("boundaries", [sys.executable, "-B", "-X", "utf8", "Final-Report/scripts/audit_workspace_boundaries.py", "--mode", "working_tree"]),
    ]
    for name, args in commands:
        process = subprocess.run(args, cwd=ROOT, capture_output=True, encoding="utf-8", errors="replace")
        (logs / (name + ".log")).write_text(process.stdout + process.stderr, encoding="utf-8")
        checks.append({"name": name, "status": "PASS" if process.returncode == 0 else "FAIL",
                       "exit_code": process.returncode, "command": args})
    evidence = {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
                "status": "PASS" if all(c["status"] == "PASS" for c in checks) else "FAIL",
                "checks": checks, "script_sha256": sha(Path(__file__)),
                "meaning": "Artifact verification only; L2 remains NOT_READY and no model was trained"}
    (HERE / "VERIFICATION.json").write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(evidence, indent=2))
    return 0 if evidence["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
