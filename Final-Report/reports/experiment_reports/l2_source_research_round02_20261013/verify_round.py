"""Verify this research round using pinned real records, without fitting a model."""
import ast
import csv
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urlsplit

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BASE = ROOT / "workspaces/truongnv/pi_guard_pipeline/training_bases"
PROJECT = BASE / "datasets/project_training"
VERSIONS = PROJECT / "versions"
V9 = VERSIONS / "pi_guard_v9_english_source_heldout_20261013"
V10 = VERSIONS / "pi_guard_v10_english_readiness_20261013"
V11 = VERSIONS / "pi_guard_v11_english_gandalf_20261013"
V12 = VERSIONS / "pi_guard_v12_english_rights_overlay_20261013"
CHECKER = BASE / "pi_guard_tfidf_tier1/check_curated_candidate.py"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def rows(path):
    with path.open(encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def record(path, value):
    with path.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(value, indent=2) + "\n")


def binding(prompt, context):
    return hashlib.sha256(json.dumps([prompt, context], ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()


def main():
    logs = HERE / "verification_logs_r03"
    logs.mkdir(exist_ok=False)
    checks = []

    def passed(name, **details):
        checks.append({"name": name, "status": "PASS", **details})

    manifests = {}
    for package in (V9, V10, V11, V12):
        manifest = read(package / "DATASET_MANIFEST.json")
        manifests[package.name] = manifest
        # V9 predates the file-map schema; its complete tree is checked below.
        for relative, ref in manifest.get("files", {}).items():
            path = package / relative
            assert path.resolve().is_relative_to(package.resolve()) and not path.is_symlink()
            assert sha(path) == ref["sha256"], str(path)
    v11, v12 = manifests[V11.name], manifests[V12.name]
    before = read(V11 / "provenance/PARENT_INTEGRITY.json")["parent_files_sha256_before_after_equal"]
    now = {f"{p.name}/{f.relative_to(p).as_posix()}": sha(f)
           for p in (V9, V10) for f in p.rglob("*") if f.is_file()}
    assert now == before
    before11 = read(V12 / "provenance/PARENT_INTEGRITY.json")["parent_files_sha256"]
    assert before11 == {f.relative_to(V11).as_posix(): sha(f) for f in V11.rglob("*") if f.is_file()}
    assert v11["parent_manifest_sha256"] == sha(V10 / "DATASET_MANIFEST.json")
    assert v12["parent_manifest_sha256"] == sha(V11 / "DATASET_MANIFEST.json")
    assert sha(PROJECT / v12["parent_index"]["path_from_project_training"]) == v12["parent_index"]["sha256"]
    for p in (V11, V12):
        m = manifests[p.name]
        assert m["trainable"] is False and m["split_sha256"] is None
        assert sum(m["canonical_row_counts"].values()) == 0
        assert not m["l2_fit"] and not m["l3_run"]
    passed("immutable_versions_and_training_boundaries", parent_files_verified=len(now), v11_files_verified=len(before11))

    source_manifest = read(HERE / "source_snapshots_r02/MANIFEST.json")
    assert sha(HERE / "source_snapshots_r02/MANIFEST.json") == v11["source_snapshot_manifest_sha256"]
    assert len(source_manifest["sources"]) == 9
    documents = 0
    for source in source_manifest["sources"]:
        assert not source["terms_accepted"]
        assert re.fullmatch(r"[0-9a-f]{40}", source["revision"])
        for doc in source["documents"]:
            path = HERE / doc["path"]
            assert path.resolve().is_relative_to(HERE) and sha(path) == doc["sha256"]
            assert path.stat().st_size == doc["bytes"]
            documents += 1
    payloads = [s for s in source_manifest["sources"] if s["payload_downloaded"]]
    assert len(payloads) == source_manifest["downloaded_payload_count"] == 1
    source = payloads[0]
    assert source["source_id"] == "gandalf" and source["upstream_split"] == "train"
    assert source["gated"] is False and source["license_recorded"] == "mit"
    assert sha(HERE / source["payload"]["path"]) == sha(V11 / "snapshots/gandalf_train.parquet") == source["payload"]["sha256"]
    assert sorted(p.name for p in (HERE / "source_snapshots_r02").rglob("*.parquet")) == ["train.parquet"]
    assert not source_manifest["upstream_validation_test_payloads_opened"]
    assert not source_manifest["historical_locked_evaluation_opened"]
    passed("pinned_primary_documents_and_train_only_acquisition", sources=9, documents=documents, payloads=1)

    index = rows(V11 / "provenance/english_candidate_index.jsonl")
    by_id = {r["blind_item_id"]: r for r in index}
    keys = rows(V11 / "provenance/curator_key_pilot.jsonl")
    exclusions = rows(V11 / "provenance/exclusion_ledger.jsonl")
    with (V11 / "annotation/source_blind_pilot.csv").open(encoding="utf-8", newline="") as stream:
        sheet = list(csv.DictReader(stream))
    assert len(index) == len(by_id) == 56990
    assert len(keys) == len(sheet) == 492 and len(exclusions) == 285
    assert len({r["source_family_id"] for r in index}) == 11
    assert all(r["candidate_only"] and r.get("project_label") is None and r.get("curator_label") is None for r in index)
    assert set(r["blind_item_id"] for r in keys) == set(r["blind_item_id"] for r in sheet)
    spec = importlib.util.spec_from_file_location("curator_intake", CHECKER)
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)
    import pyarrow.parquet as pq
    native = pq.read_table(V11 / "snapshots/gandalf_train.parquet").to_pylist()
    assert len(native) == 777 and all(set(r) == {"text", "similarity"} for r in native)
    accepted_offsets = set()
    for row in sheet:
        key = by_id[row["blind_item_id"]]
        assert checker.decision(row) == ("unreviewed", None)
        assert key in keys and binding(row["prompt_text"], row["context_text"]) == key["text_context_binding_sha256"]
        offset = int(key["source_record_id"].split(":")[1])
        accepted_offsets.add(offset)
        assert row["prompt_text"] == native[offset]["text"] and row["context_text"] == ""
        assert key["source_similarity_score_provenance_only"] == native[offset]["similarity"]
        assert key["predicted_language"] == "en" and key["language_confidence"] >= 0.95
    excluded_offsets = {r["source_offset"] for r in exclusions}
    assert len(accepted_offsets) == 492 and len(excluded_offsets) == 285
    assert not accepted_offsets & excluded_offsets and accepted_offsets | excluded_offsets == set(range(777))
    assert Counter(r["reason"] for r in exclusions) == {"not_english_or_confidence_below_0.95": 285}
    assert all(r["predicted_language"] != "en" or r["confidence"] < 0.95 for r in exclusions)
    passed("actual_source_records_annotation_bindings_and_language_partition", downloaded=777, candidates=492, excluded=285)

    groups = defaultdict(list)
    old_groups = defaultdict(set)
    for row in index:
        groups[row["duplicate_group_id"]].append(row)
        if row["parent_duplicate_group_id"] is not None:
            old_groups[row["parent_duplicate_group_id"]].add(row["duplicate_group_id"])
    assert all(len(values) == 1 for values in old_groups.values())
    nonsingletons = [members for members in groups.values() if len(members) > 1]
    cross = [members for members in groups.values() if len({r["source_family_id"] for r in members}) > 1]
    assert len(nonsingletons) == 1178 and sum(map(len, nonsingletons)) == 3131
    assert len(cross) == 25 and sum(map(len, cross)) == 78
    assert not any(r["source_family_id"] == "lakera_gandalf_game" for g in cross for r in g)
    passed("historical_duplicate_constraints_and_joint_group_counts", cross_family_groups=25, cross_family_rows=78, new_source_cross_family_groups=0)

    aggregate = PROJECT / "history/pi_guard_v8_source_gate_20261010/corpus/candidates/rubyglask_core_components"
    aggregate_meta = aggregate / "provenance/source_metadata.jsonl"
    assert sha(aggregate_meta) == read(aggregate / "manifest.json")["provenance_file"]["sha256"]
    assert sha(aggregate_meta) == read(V11 / "provenance/PARENT_INTEGRITY.json")["aggregate_source_metadata_sha256"]
    originals = {r["candidate_id"]: r for r in rows(aggregate_meta)}
    component_rows = [r for r in index if r["pool_id"] == "rubyglask_core_components"]
    assert len(component_rows) == 4476
    for row in component_rows:
        original = originals[row["candidate_id"]]
        assert row["aggregate_source_original_id_recorded"] == original["source_original_id"]
        assert row["upstream_source_id"] == original["source_id"]
        assert row["original_component_revision"] is None
        assert row["original_component_split"] is None
        assert row["component_current_metadata_is_original_ingest_revision"] is False
    holds = rows(V12 / "provenance/rights_quarantine.jsonl")
    held_ids = {r["blind_item_id"] for r in holds}
    affected_ids = {r["blind_item_id"] for r in index if r["source_family_id"] == "rubyglask_do_not_answer"}
    assert len(holds) == len(held_ids) == 554 and held_ids == affected_ids
    assert all(r["human_rights_review_decision"] is None and r["canonical_label"] is None for r in holds)
    assert v12["candidate_rows_not_in_this_explicit_hold"] == len(index) - len(holds) == 56436
    card = HERE / "source_snapshots_r02/do_not_answer/README.md"
    evidence = read(V12 / "provenance/RIGHTS_EVIDENCE.json")
    assert sha(card) == evidence["publisher_card_sha256"]
    assert "license: apache-2.0" in card.read_text(encoding="utf-8")
    assert "Creative Commons Attribution-NonCommercial-ShareAlike 4.0" in card.read_text(encoding="utf-8")
    pilot10 = rows(V10 / "provenance/curator_key_pilot.jsonl")
    # Pilot IDs were deliberately regenerated in V10. Join through the pinned
    # parent crosswalk instead of equating blind IDs from different versions.
    assert all(by_id[r["parent_blind_item_id"]]["candidate_id"] == r["candidate_id"] for r in pilot10)
    held_pilot10 = sum(r["parent_blind_item_id"] in held_ids for r in pilot10)
    assert held_pilot10 == 10
    held_group_ids = {by_id[r]["duplicate_group_id"] for r in held_ids}
    other_group_rows = sum(r["blind_item_id"] not in held_ids for g in held_group_ids for r in groups[g])
    passed("original_ids_without_invented_splits_and_rights_quarantine", original_component_rows=4476,
           rights_quarantined_rows=554, held_v10_pilot_rows=held_pilot10,
           other_rows_sharing_held_duplicate_groups=other_group_rows,
           limitation="Nonheld duplicates require group review; no rows are declared eligible")

    for package in (V10, V11):
        name = "curator_self_check_" + package.name.split("_")[2] + "_r03"
        arguments = ["-B", "-X", "utf8", str(CHECKER), "--package", str(package),
                     "--self-check", "--output", str(HERE / (name + ".json"))]
        started = datetime.now(timezone.utc).isoformat()
        run = subprocess.run([sys.executable, *arguments], cwd=ROOT, capture_output=True, encoding="utf-8", errors="replace")
        record(HERE / (name + ".command.json"), {"run_id": name + "_20261013_r01", "arguments": arguments,
               "cwd": ROOT.as_posix(), "started_at_utc": started, "ended_at_utc": datetime.now(timezone.utc).isoformat(),
               "exit_code": run.returncode, "script_sha256": sha(CHECKER)})
        (HERE / (name + ".log")).write_text(run.stdout + run.stderr, encoding="utf-8")
        assert run.returncode == 0 and read(HERE / (name + ".json"))["self_check"] == "PASS"
    try:
        checker.inspect(V12)
    except ValueError as error:
        assert str(error) == "Expected an immutable supported candidate package"
    else:
        raise AssertionError("Sparse rights overlay must not bypass full-packet intake")
    record(logs / "overlay_intake_rejection.json", {"status": "PASS", "reason": "Sparse V12 is rejected by the full-packet intake checker"})
    passed("curator_intake_compatibility_and_fail_closed_overlay", checked_versions=["V10", "V11"], unsupported_overlay_rejected=True)

    failed = read(HERE / "pin_sources.command.json")
    assert failed["exit_code"] == 1 and sha(HERE / "pin_sources_r01_failed_snapshot.py") == failed["script_sha256"]
    assert sha(HERE / "check_curated_candidate_pre_v11.py") == "0323b83954d8ea002ae52832f0338b74b9a0f886524c666582d2281305c3b824"
    for name, script in (("pin_sources_r02", HERE / "pin_sources.py"), ("build_v11", HERE / "build_v11_candidates.py"),
                         ("quarantine_rights_v12", HERE / "quarantine_rights_v12.py"), ("curator_intake_v11", CHECKER)):
        command = read(HERE / (name + ".command.json"))
        assert command["exit_code"] == 0 and command["started_at_utc"] and command["ended_at_utc"]
        assert command["script_sha256"] == sha(script)
        assert (HERE / (name + ".log")).is_file()
        ast.parse(script.read_text(encoding="utf-8-sig"))
    assert v11["script_sha256"] == sha(HERE / "build_v11_candidates.py")
    assert v11["helper_sha256"] == sha(V9 / "tools/prepare_v9_public_english_queue.py")
    assert v12["script_sha256"] == sha(HERE / "quarantine_rights_v12.py")
    failed_verifier = read(HERE / "verify_round.command.json")
    assert failed_verifier["exit_code"] == 1
    assert failed_verifier["script_sha256"] == sha(HERE / "verify_round_r01_failed_snapshot.py")
    assert read(HERE / "verify_round_r02.command.json")["script_sha256"] == sha(HERE / "verify_round_r02_snapshot.py")
    intake = read(HERE / "curator_intake_v11.json")
    assert intake["review_counts"] == {"unreviewed": 492}
    assert intake["script_sha256"] == sha(CHECKER) and intake["canonical_model_rows_emitted"] == 0
    assert not intake["fit_performed"] and not intake["test_opened"] and not intake["l3_run"]
    passed("failed_run_preservation_and_executed_code_identity")

    commands = sorted((read(p) for p in HERE.glob("*.command.json")), key=lambda r: r["started_at_utc"])
    record(HERE / "RUN_LEDGER_r03.json", {"created_at_utc": datetime.now(timezone.utc).isoformat(), "runs": commands,
           "dataset_manifests": {p.name: sha(p / "DATASET_MANIFEST.json") for p in (V11, V12)},
           "labels_created": 0, "fit_performed": False, "test_opened": False, "l3_run": False,
           "acceptance_status": "BLOCKED/NOT_READY", "verification_record": "VERIFICATION_r03.json"})
    report = (HERE / "REPORT.md").read_text(encoding="utf-8")
    assert all(sha(p / "DATASET_MANIFEST.json") in report for p in (V11, V12))
    local_links = 0
    for doc in (HERE / "REPORT.md", HERE / "TASK.md"):
        for target in re.findall(r"\]\(([^)]+)\)", doc.read_text(encoding="utf-8")):
            parsed = urlsplit(target.strip("<>"))
            if parsed.scheme:
                continue
            if parsed.path:
                resolved = (doc.parent / unquote(parsed.path)).resolve()
                if resolved == HERE / "VERIFICATION_r03.json":
                    continue  # This output is created after checks; write failure aborts the run.
                assert resolved.is_file(), target
                local_links += 1
    passed("reported_manifest_identities_and_local_links", local_links_verified=local_links)

    commands = [
        ("scope", "audit_task_scope.py", ["--file", str(HERE / "REPORT.md"), "--strict"]),
        ("claims", "audit_claim_evidence.py", ["--file", str(HERE / "REPORT.md")]),
        ("glossary", "verify_academic_glossary.py", ["--file", str(HERE / "REPORT.md")]),
        ("boundaries", "audit_workspace_boundaries.py", ["--mode", "working_tree"]),
    ]
    for name, script, options in commands:
        arguments = [sys.executable, "-B", "-X", "utf8", str(ROOT / "Final-Report/scripts" / script), *options]
        run = subprocess.run(arguments, cwd=ROOT, capture_output=True, encoding="utf-8", errors="replace")
        (logs / (name + ".log")).write_text(run.stdout + run.stderr, encoding="utf-8")
        checks.append({"name": name, "status": "PASS" if run.returncode == 0 else "FAIL", "exit_code": run.returncode, "command": arguments})
    result = {"checked_at_utc": datetime.now(timezone.utc).isoformat(), "status": "PASS" if all(c["status"] == "PASS" for c in checks) else "FAIL",
              "checks": checks, "script_sha256": sha(Path(__file__)), "meaning": "Artifact checks only; L2 NOT_READY, no fit/test/L3"}
    result["supersedes"] = "VERIFICATION.json: held V10 pilot count corrected using parent_blind_item_id crosswalk; dataset versions unchanged"
    record(HERE / "VERIFICATION_r03.json", result)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
