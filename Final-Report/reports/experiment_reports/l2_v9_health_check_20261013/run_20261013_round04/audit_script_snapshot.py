"""Read-only V9 evidence audit. No fitting, relabeling, or test payload access.

Run with --output NEW_DIRECTORY. Writes only aggregate/ID metadata into a new
directory under this report. --self-check checks the freshly generated evidence.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import os
import platform
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
BASE = REPO / "workspaces/truongnv/pi_guard_pipeline/training_bases"
PROJECT = BASE / "datasets/project_training"
V9 = PROJECT / "versions/pi_guard_v9_english_source_heldout_20261013"
V8 = PROJECT / "history/pi_guard_v8_english_diagnostic_20261012"
REFERENCE_RUN = BASE / "pi_guard_tfidf_tier1/runs/v8_0_1_candidate_english_l2_c2_20261012"
DECISIONS = ("curator_label", "is_injection", "is_safety_bypass", "confidence",
             "rationale_code", "context_sufficient", "annotated_at_utc", "final_label",
             "label_status", "curator_code", "curator_notes")


def readj(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def writej(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_module(path):
    spec = importlib.util.spec_from_file_location("v9_read_only_helpers", path)
    module = importlib.util.module_from_spec(spec)
    # Do not create bytecode inside immutable dataset packages.
    prior = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = prior
    return module


def writecsv(path, rows, fields):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def run(output):
    started = datetime.now(timezone.utc).isoformat()
    if output.exists() or output.parent.resolve() != HERE:
        raise ValueError("Output must be a new direct child of the report directory")
    # Existing helpers have no import-time writes or model fitting.
    helper_path = V9 / "tools/prepare_v9_public_english_queue.py"
    helper = load_module(helper_path)
    sha = helper.sha256_file
    before = {str(p.relative_to(V9)).replace("\\", "/"): sha(p)
              for p in sorted(V9.rglob("*")) if p.is_file()}
    manifest, status = readj(V9 / "DATASET_MANIFEST.json"), readj(V9 / "STATUS.json")
    ingest = readj(V9 / "reports/v9_public_ingest_round02_manifest.json")
    pilot = readj(V9 / "reports/curator_packet_round01_manifest.json")
    round3 = readj(V9 / "reports/v9_round03_assistant_proposal_pilot_manifest.json")
    expected = {
        "annotation/round01_source_blind_pilot.csv": pilot["packet_sha256"],
        "provenance/curator_key_round01.jsonl": pilot["key_sha256"],
        "annotation/round02_public_english_candidate_queue.csv": ingest["output_sha256"]["review_queue"],
        "provenance/english_candidate_index_round02.jsonl": ingest["output_sha256"]["provenance_index"],
        "provenance/round02_exclusion_ledger.jsonl": ingest["output_sha256"]["exclusion_ledger"],
        "annotation/round03_source_blind_curator_review.csv": round3["output_sha256"]["curator_packet"],
        "provenance/curator_key_round03.jsonl": round3["output_sha256"]["curator_key"],
        "annotation/assistant_proposals_round03.jsonl": round3["output_sha256"]["assistant_proposals"],
        "reports/v9_l2_source_coverage_audit_round03.json": round3["output_sha256"]["source_coverage_audit"],
    }
    for rel, value in expected.items():
        assert before[rel] == value, "V9 recorded artifact hash mismatch: " + rel
    assert manifest["review_packet"]["sha256"] == expected[manifest["review_packet"]["path"]]
    assert status["review_packet"]["sha256"] == manifest["review_packet"]["sha256"]
    for item in (manifest, status):
        assert item["dataset_version"] == "9.0.0-candidate-english"
        assert item["trainable"] is False
        assert all(item["canonical_row_counts"][part] == 0 for part in ("train", "validation", "test"))
    index = [json.loads(line) for line in (V9 / "provenance/english_candidate_index_round02.jsonl").read_text(encoding="utf-8").splitlines() if line]
    by_id = {row["blind_item_id"]: row for row in index}
    assert len(by_id) == len(index) == ingest["english_and_pattern_clear_rows"]
    family_rows, duplicate_rows = defaultdict(list), defaultdict(list)
    for row in index:
        assert row["predicted_language"] == "en" and row["language_confidence"] >= 0.95
        assert row["candidate_only"] is True and row["project_label"] is None
        assert row["privacy_pattern_screen"] == "clear_for_email_and_credential_patterns"
        for field in ("source_revision", "source_record_id", "source_license", "source_license_ref", "source_family_id", "duplicate_group_id"):
            assert row[field], "Incomplete candidate lineage: " + field
        family_rows[row["source_family_id"]].append(row)
        duplicate_rows[row["duplicate_group_id"]].append(row)
    queues, decision_counts = {}, {}
    for name, count in (("round01_source_blind_pilot", 43), ("round02_public_english_candidate_queue", 56455), ("round03_source_blind_curator_review", 20)):
        with (V9 / f"annotation/{name}.csv").open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            assert set(reader.fieldnames) == set(helper.FIELDS)
            ids, filled = [], Counter()
            for row in reader:
                ident = row["blind_item_id"]
                assert ident in by_id
                meta = by_id[ident]
                text = row["prompt_text"] + "\n" + row["context_text"]
                norm_hash = hashlib.sha256(helper.normalize(text).encode("utf-8")).hexdigest()
                assert norm_hash == meta["dedup_normalized_input_sha256"]
                assert not helper.EMAIL_RE.search(text) and not helper.CREDENTIAL_RE.search(text)
                for field in DECISIONS:
                    filled[field] += bool(row[field].strip())
                ids.append(ident)
        assert len(set(ids)) == len(ids) == count
        queues[name] = set(ids)
        decision_counts[name] = dict(filled)
    q1, q2, q3 = (queues[name] for name in queues)
    assert not q1 & q2 and q1 | q2 == set(by_id)
    assert q3 <= q2, "Round03 is a subset of Round02, not new candidate data"
    assert all(not any(counts.values()) for counts in decision_counts.values()), "Human decision fields changed; re-audit completed copies before reconciliation"
    excluded = [json.loads(line) for line in (V9 / "provenance/round02_exclusion_ledger.jsonl").read_text(encoding="utf-8").splitlines() if line]
    reasons = Counter(row["reason"] for row in excluded)
    assert len(index) + len(excluded) == ingest["input_rows"]
    assert reasons["privacy_pattern_match"] == ingest["privacy_pattern_quarantined_rows"]
    assert reasons["not_english_or_confidence_below_0.95"] == ingest["language_excluded_rows"]
    assert not set(by_id) & {row["blind_item_id"] for row in excluded}
    source_counts, source_hashes = {}, {}
    for pool in helper.CONFIG["pools"]:
        if not pool["include"]:
            continue
        candidates, source_manifest = helper.load_pool(pool)
        source_counts[pool["pool_id"]] = len(candidates)
        assert len(candidates) == ingest["source_pools"][pool["pool_id"]]["input_rows"]
        source_manifest_path = helper.SOURCE_ROOT / pool["pool_id"] / "manifest.json"
        source_hashes[str(source_manifest_path.relative_to(REPO)).replace("\\", "/")] = sha(source_manifest_path)
        del candidates
    coverage = readj(V9 / "reports/v9_l2_source_coverage_audit_round03.json")
    cross = {key: rows for key, rows in duplicate_rows.items() if len({row["source_family_id"] for row in rows}) > 1}
    assert dict(Counter(row["source_family_id"] for row in index)) == coverage["candidate_rows_by_source_family"]
    assert len(cross) == coverage["cross_family_duplicate_group_count"]
    assert sum(map(len, cross.values())) == coverage["cross_family_duplicate_row_count"]
    nonsingle = [rows for rows in duplicate_rows.values() if len(rows) > 1]
    assert len(nonsingle) == ingest["duplicate_grouping"]["duplicate_groups"]
    assert sum(map(len, nonsingle)) == ingest["duplicate_grouping"]["rows_in_non_singleton_groups"]
    sys.path.insert(0, str(helper.VENDOR))
    import py3langid
    from py3langid.langid import MODEL_FILE
    model_sha = sha(Path(py3langid.__file__).resolve().parent / MODEL_FILE)
    assert model_sha == helper.MODEL_SHA
    rm = readj(REFERENCE_RUN / "run_manifest.json")
    for name, value in rm["artifact_sha256"].items():
        assert sha(REFERENCE_RUN / name) == value, "Historical English run artifact hash mismatch: " + name
    metrics = readj(REFERENCE_RUN / "metrics.json")
    predictions = [json.loads(line) for line in (REFERENCE_RUN / "validation_predictions.jsonl").read_text(encoding="utf-8").splitlines() if line]
    labels = ("benign", "PI", "JB")
    matrix = [[0] * 3 for _ in labels]
    assert len({row["id"] for row in predictions}) == len(predictions) == metrics["rows"]
    for row in predictions:
        matrix[labels.index(row["true_label"])][labels.index(row["predicted_label"]) ] += 1
    assert matrix == metrics["confusion_matrix"] == rm["english_model_metrics"]["confusion_matrix"]
    assert rm["test_opened"] is False and rm["source_eval_opened"] is False and rm["l3_run"] is False
    assert rm["configuration"]["classifier"] == {"C": 2.0, "class_weight": "balanced", "max_iter": 1000, "solver": "lbfgs", "type": "LogisticRegression"}
    gates = {
        "source_snapshot_integrity": "PASS",
        "rights_lineage_metadata_for_candidate_intake": "PASS_WITH_LIMITS_NOT_LEGAL_CLEARANCE",
        "english_filter_recorded_policy_and_model_hash": "PASS_METADATA_AND_HASH_NOT_RECLASSIFICATION",
        "privacy_pattern_screen": "PASS_WITH_QUARANTINES_NOT_FULL_PRIVACY_REVIEW",
        "curator_canonical_labels": "BLOCKED",
        "source_level_privacy_review": "BLOCKED",
        "source_family_independence": "BLOCKED",
        "source_family_2_1_1_per_class": "BLOCKED",
        "duplicate_group_computation": "PASS_RECORDED_GROUPS_NOT_EXHAUSTIVE_SEMANTIC_DEDUP",
        "cross_family_duplicate_partition_resolution": "BLOCKED",
        "source_disjoint_frozen_split": "BLOCKED",
        "v9_l1_input_window_contract": "NOT_RECORDED",
        "v9_baseline_fit_and_validation": "NOT_RUN_DATA_GATES_BLOCKED",
        "numeric_route_risk_workload_support_acceptance": "GATE_UNSPECIFIED",
        "validation_selected_operating_point": "NOT_AVAILABLE",
        "conditional_review_class_and_training_support": "NOT_AVAILABLE",
        "v9_one_time_test": "NOT_RUN_DATA_AND_SELECTION_GATES_BLOCKED",
        "l2_latency_p50_p95_p99": "NOT_AVAILABLE_GATE_UNSPECIFIED",
    }
    pending_privacy = [row for row in index if row["privacy_manual_review_required"]]
    report = {
        "run_id": output.name, "started_utc": started,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "outcome": "BLOCKED", "health_check_status": "NOT_READY",
        "fit_started": False, "test_payload_opened": False, "source_eval_payload_opened": False,
        "l3_run": False, "dataset_changed": False, "assistant_proposal_labels_used": False,
        "dataset_version": manifest["dataset_version"], "dataset_package": str(V9.relative_to(REPO)).replace("\\", "/"),
        "dataset_manifest_sha256": before["DATASET_MANIFEST.json"], "status_sha256": before["STATUS.json"],
        "script_sha256": sha(Path(__file__)), "helper_sha256": sha(helper_path),
        "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO, text=True).strip(),
        "environment": {"python": platform.python_version(), "platform": platform.platform(), "executable": sys.executable, "py3langid_model_sha256": model_sha},
        "v9_input_artifact_sha256": before, "pinned_source_manifest_sha256": source_hashes,
        "source_snapshot_rows_checked": source_counts,
        "candidate_rows": len(index), "unique_round01_rows": len(q1), "unique_round02_rows": len(q2),
        "round03_subset_rows_not_additional": len(q3), "curator_decision_field_counts": decision_counts,
        "canonical_row_counts": manifest["canonical_row_counts"],
        "source_family_candidate_counts": coverage["candidate_rows_by_source_family"],
        "privacy_review_pending_rows": len(pending_privacy),
        "privacy_review_pending_by_pool": dict(Counter(row["pool_id"] for row in pending_privacy)),
        "exclusion_counts": dict(reasons), "duplicate_groups": len(nonsingle),
        "rows_in_non_singleton_groups": sum(map(len, nonsingle)),
        "cross_family_duplicate_groups": len(cross), "cross_family_duplicate_rows": sum(map(len, cross.values())),
        "gates": gates,
        "historical_english_reference": {"run_id": rm["run_id"], "created_utc": rm["created_utc"], "dataset_version": rm["dataset_version"], "run_manifest_sha256": sha(REFERENCE_RUN / "run_manifest.json"), "metrics_sha256": sha(REFERENCE_RUN / "metrics.json"), "configuration": rm["configuration"], "confusion_matrix": matrix, "metrics": rm["english_model_metrics"], "train_rows": rm["train_rows"], "validation_rows": rm["validation_rows"], "split_manifest_sha256": rm["split_manifest_sha256"], "script_sha256_at_fit": rm["script_sha256"], "selected_cutoff_pair": rm["threshold_sweep"]["selected_pair"]},
        "verification_limits": ["No language reclassification or near-duplicate candidate generation rerun; existing hashes, metadata and normalized text alignment checked.", "No claim of source independence or complete privacy clearance.", "Only recorded gates and blank original curator sheets inspected; no external curator attestation supplied.", "Historical run metadata reports no test selection; absence of an independent complete access log does not establish a V9 final-evaluation boundary."]
    }
    after = {str(p.relative_to(V9)).replace("\\", "/"): sha(p) for p in sorted(V9.rglob("*")) if p.is_file()}
    assert before == after, "Audit changed V9 package files"
    report["v9_package_unchanged_before_after"] = True
    output.mkdir()
    writej(output / "audit.json", report)
    writecsv(output / "privacy_review_index.csv", [{"blind_item_id": row["blind_item_id"], "pool_id": row["pool_id"], "duplicate_group_id": row["duplicate_group_id"], "review_status": "PENDING_HUMAN_REVIEW"} for row in pending_privacy], ["blind_item_id", "pool_id", "duplicate_group_id", "review_status"])
    family_review = []
    for family, rows in sorted(family_rows.items()):
        family_review.append({"source_family_id": family, "candidate_rows": len(rows), "parent_repositories": ";".join(sorted({r["source_repository_id"] for r in rows})), "upstream_repositories": ";".join(sorted({r["upstream_repository_id"] for r in rows})), "source_revisions": ";".join(sorted({r["source_revision"] for r in rows})), "source_license_refs": ";".join(sorted({r["source_license_ref"] for r in rows})), "review_status": "PENDING_HUMAN_LINEAGE_REVIEW", "independence_decision": "", "reviewer_code": "", "reviewed_at_utc": "", "evidence_ref": ""})
    writecsv(output / "family_lineage_review.csv", family_review, list(family_review[0]))
    writej(output / "cross_family_duplicate_review.json", {"status": "PENDING_PARTITION_DECISION", "groups": [{"duplicate_group_id": key, "row_count": len(rows), "source_family_ids": sorted({row["source_family_id"] for row in rows}), "blind_item_ids": [row["blind_item_id"] for row in rows]} for key, rows in sorted(cross.items())]})
    print(json.dumps({"run_id": output.name, "outcome": report["outcome"], "candidate_rows": len(index), "privacy_review_pending_rows": len(pending_privacy), "v9_unchanged": True, "fit_started": False, "test_payload_opened": False, "l3_run": False}))
    return 0


def self_check(output):
    data = readj(output / "audit.json")
    assert data["outcome"] == "BLOCKED" and data["health_check_status"] == "NOT_READY"
    assert data["candidate_rows"] == data["unique_round01_rows"] + data["unique_round02_rows"]
    assert data["round03_subset_rows_not_additional"] == 20
    assert data["privacy_review_pending_rows"] == sum(data["privacy_review_pending_by_pool"].values())
    assert data["cross_family_duplicate_rows"] == 78 and data["cross_family_duplicate_groups"] == 25
    assert all(value == 0 for row in data["curator_decision_field_counts"].values() for value in row.values())
    assert data["gates"]["numeric_route_risk_workload_support_acceptance"] == "GATE_UNSPECIFIED"
    assert all(data[key] is False for key in ("fit_started", "test_payload_opened", "source_eval_payload_opened", "l3_run", "dataset_changed"))
    sha = load_module(V9 / "tools/prepare_v9_public_english_queue.py").sha256_file
    assert data["script_sha256"] == sha(Path(__file__))
    for relative, value in data["v9_input_artifact_sha256"].items():
        assert sha(V9 / relative) == value, "Fresh V9 immutability check failed: " + relative
    print("SELF_CHECK_PASS: fail-closed decision, counts, closed test/L3 boundaries, and fresh V9 hashes verified")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    raise SystemExit(self_check(args.output.resolve()) if args.self_check else run(args.output.resolve()))
