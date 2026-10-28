#!/usr/bin/env python3
"""Exercise the curated L2 adapter only against real candidate metadata."""
from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import hashlib
import json
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"D:\Work\Do-an")
REPORT = ROOT / "Final-Report" / "reports" / "experiment_reports" / "l2_autonomous_research_20261013"
PRIVATE = ROOT / "workspaces" / "truongnv" / "pi_guard_pipeline"
RUNNER_DIR = PRIVATE / "training_bases" / "pi_guard_tfidf_tier1"
VERSIONS = PRIVATE / "training_bases" / "datasets" / "project_training" / "versions"
PROTOCOL = REPORT / "AUTONOMOUS_PROTOCOL.json"
RUNS = REPORT / "adapter_runs"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_sealed_test_contract(adapter: object) -> None:
    family = {
        "source_repository_id": "example/source",
        "source_revision": "a" * 40,
        "source_family_id": "family-test",
        "collection_lineage_id": "lineage-test",
        "label_support": {"benign": 120, "PI": 120, "JB": 120},
    }
    contract = {"schema": "pi_guard_sealed_test_families_v1", "families": [family]}
    validate = getattr(adapter, "validate_sealed_test_contract")
    assert validate(contract, 1, set(), set()) == []
    assert any("TEST_CONTRACT_FIELDS_INVALID" in blocker for blocker in
               validate({**contract, "rows": []}, 1, set(), set()))
    assert any("CROSS_PARTITION_GROUP:source_family_id" in blocker for blocker in
               validate(contract, 1, {"family-test"}, set()))
    assert any("CROSS_PARTITION_GROUP:collection_lineage_id" in blocker for blocker in
               validate(contract, 1, set(), {"lineage-test"}))
    no_jb = {**family, "label_support": {"benign": 120, "PI": 120, "JB": 0}}
    assert any("FAMILY_MINIMUM:test:JB:0/1" == blocker for blocker in
               validate({**contract, "families": [no_jb]}, 1, set(), set()))
    malformed_split = {"schema": adapter.SCHEMA, "frozen": True,
                       "access": [], "partitions": []}
    split_blockers = adapter.validate_split(
        malformed_split, {"train": 2, "validation": 1, "test": 1})
    assert "TEST_ACCESS_DECLARATION_INVALID" in split_blockers
    assert "SPLIT_PARTITION_KEYS_INVALID" in split_blockers


def main() -> int:
    RUNS.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(RUNNER_DIR))
    import fit_l2_curated as adapter  # noqa: E402

    check_sealed_test_contract(adapter)
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    assert digest(PROTOCOL) == adapter.PROTOCOL_SHA256
    assert digest(RUNNER_DIR / "fit_l2_v8.py") == protocol["baseline_helper_sha256"]

    model = adapter.legacy.build_model(protocol["baseline"])
    classifier = model.named_steps["classifier"]
    assert (classifier.C, classifier.class_weight, classifier.max_iter,
            classifier.solver, classifier.random_state) == (2.0, "balanced", 1000, "lbfgs", 42)
    features = model.named_steps["features"]
    assert [name for name, _ in features.transformer_list] == ["word", "char"]
    assert not hasattr(features.transformer_list[0][1], "vocabulary_")
    assert not hasattr(features.transformer_list[1][1], "vocabulary_")

    packages = sorted(p for p in VERSIONS.iterdir() if p.is_dir() and p.name.startswith("pi_guard_v"))
    expected = {"pi_guard_v9_english_source_heldout_20261013",
                "pi_guard_v10_english_readiness_20261013",
                "pi_guard_v11_english_gandalf_20261013",
                "pi_guard_v12_english_rights_overlay_20261013"}
    assert {p.name for p in packages} == expected, "Candidate version set changed; review before extending this check"

    records = []
    for package in packages:
        for fit_flag in (False, True):
            run_id = f"verify_{package.name}_{'fit' if fit_flag else 'preflight'}_{uuid.uuid4().hex[:10]}"
            output = RUNS / run_id
            command = [sys.executable, "-B", "-X", "utf8", str(RUNNER_DIR / "fit_l2_curated.py"),
                       "--package", str(package), "--protocol", str(PROTOCOL), "--output", str(output)]
            if fit_flag:
                command.append("--fit")
            completed = subprocess.run(command, cwd=RUNNER_DIR, text=True, encoding="utf-8",
                                       errors="strict", capture_output=True, check=False)
            result = json.loads(completed.stdout)
            assert completed.returncode == 2, (package.name, fit_flag, completed.returncode, completed.stdout, completed.stderr)
            assert result["status"] == "BLOCKED", (package.name, fit_flag, result)
            assert result["fit_started"] is False, (package.name, fit_flag, result)
            assert result["row_payloads_opened"] == [], (package.name, fit_flag, result)
            assert result["test_opened"] is False and result["l3_run"] is False
            assert not output.exists(), f"Blocked preflight unexpectedly created output: {output}"
            records.append({"command": command, "return_code": completed.returncode,
                            "stdout": completed.stdout, "stderr": completed.stderr,
                            "fit_flag": fit_flag, "row_payloads_opened": result["row_payloads_opened"],
                            "output_created": output.exists()})

    output = {
        "check_id": "l2_curated_adapter_candidate_gates_v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "protocol_sha256": digest(PROTOCOL),
        "adapter_sha256": digest(RUNNER_DIR / "fit_l2_curated.py"),
        "legacy_helper_sha256": digest(RUNNER_DIR / "fit_l2_v8.py"),
        "candidate_packages": sorted(expected),
        "candidate_runs": records,
        "fixed_model_constructed_without_fit": True,
        "vocabulary_fitted": False,
        "sealed_test_contract_checks": "PASS_METADATA_ONLY",
        "row_payloads_opened": [],
        "test_opened": False,
        "l3_run": False,
        "result": "PASS_NEGATIVE_GATE_AND_FIXED_CONFIG_CHECKS",
        "not_tested": ["positive fit path: no qualifying real frozen source-disjoint package exists",
                       "cross-partition metadata mutation: no qualifying real split metadata exists"],
    }
    target = RUNS / f"adapter_gate_check_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
    target.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"result": output["result"], "candidate_commands": len(records),
                      "check_file": str(target), "fit_path_tested": False,
                      "rows_opened": 0, "test_opened": False, "l3_run": False}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
