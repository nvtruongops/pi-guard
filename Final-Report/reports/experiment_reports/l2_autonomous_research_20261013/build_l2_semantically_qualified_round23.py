"""Create a new L2 package excluding an unsupported Anthropic-to-JB mapping."""
from __future__ import annotations

import collections
import hashlib
import importlib.util
import json
import shutil
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
TRAINING = REPO / "workspaces" / "truongnv" / "pi_guard_pipeline" / "training_bases"
VERSIONS = TRAINING / "datasets" / "project_training" / "versions"
BASE_ID = "pi_guard_l2_source_diverse_round21_r04"
BASE = VERSIONS / BASE_ID
OUTPUT_ID = "pi_guard_l2_source_diverse_round21_r05"
OUTPUT_VERSION = "0.8.6-source-diverse-label-audited"
OUTPUT = VERSIONS / OUTPUT_ID
STAGING = VERSIONS / (OUTPUT_ID + ".building")
REPORT = ROOT / "l2_semantic_exclusion_package_build_round23_r01.json"

EXCLUDED_REPOSITORY = "Anthropic/hh-rlhf"
EXCLUDED_REVISION = "09be8c5bbc57cb3887f3a9732ad6aa7ec602a1fa"
EXCLUDED_FAMILY = "sf_anthropic_hh_redteam_2022_round21"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("HELPER_IMPORT_FAILED:" + name)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


R21 = load_module("l2_round23_package_helpers", ROOT / "build_l2_source_heldout_round21.py")


def write_json(path: Path, value: Any) -> None:
    R21.R18.write_json(path, value)


def write_jsonl(path: Path, rows: list[dict]) -> None:
    R21.R18.write_jsonl(path, rows)


def sha256(path: Path) -> str:
    return R21.sha256_file(path)


def read_base() -> tuple[dict, dict, dict, dict, list[dict], list[dict], list[dict], list[dict], list[dict]]:
    manifest = json.loads((BASE / "DATASET_MANIFEST.json").read_text(encoding="utf-8"))
    split = json.loads((BASE / "split_manifest.json").read_text(encoding="utf-8"))
    review = json.loads((BASE / "source_review.json").read_text(encoding="utf-8"))
    mapping = json.loads((BASE / "label_mapping.json").read_text(encoding="utf-8"))
    status = json.loads((BASE / "STATUS.json").read_text(encoding="utf-8"))
    if manifest.get("package_id") != BASE_ID or status.get("package_id") != BASE_ID:
        raise ValueError("ROUND22_BASE_IDENTITY_MISMATCH")
    for part in ("train", "validation"):
        for kind in ("rows", "provenance"):
            spec = manifest["partitions"][part][kind]
            if sha256(BASE / spec["path"]) != spec["sha256"]:
                raise ValueError("ROUND22_BASE_HASH_MISMATCH:" + part + ":" + kind)
    train_rows = R21.read_jsonl(BASE / manifest["partitions"]["train"]["rows"]["path"])
    train_prov = R21.read_jsonl(BASE / manifest["partitions"]["train"]["provenance"]["path"])
    val_rows = R21.read_jsonl(BASE / manifest["partitions"]["validation"]["rows"]["path"])
    val_prov = R21.read_jsonl(BASE / manifest["partitions"]["validation"]["provenance"]["path"])
    train_meta = split["partitions"]["train"]
    val_meta = split["partitions"]["validation"]
    if not (len(train_rows) == len(train_prov) == len(train_meta)):
        raise ValueError("ROUND22_TRAIN_ALIGNMENT_FAILURE")
    if not (len(val_rows) == len(val_prov) == len(val_meta)):
        raise ValueError("ROUND22_VALIDATION_ALIGNMENT_FAILURE")
    return manifest, split, review, mapping, train_rows, train_prov, train_meta, val_rows, val_prov


def build() -> dict:
    if OUTPUT.exists() or STAGING.exists():
        raise FileExistsError("ROUND23_OUTPUT_OR_STAGING_ALREADY_EXISTS")
    manifest, split, source_review, mapping, train_rows, train_prov, train_meta, val_rows, val_prov = read_base()
    test_contract_snapshot = json.dumps(split["partitions"]["test"], sort_keys=True)

    excluded_indices = {
        index for index, provenance in enumerate(train_prov)
        if provenance.get("source_repository_id") == EXCLUDED_REPOSITORY
        and provenance.get("source_revision") == EXCLUDED_REVISION
        and provenance.get("source_family_id") == EXCLUDED_FAMILY
    }
    if len(excluded_indices) != 2241:
        raise ValueError("ANTHROPIC_TRAIN_ROWS_DO_NOT_MATCH_OOF_EVIDENCE")
    if any(prov.get("source_repository_id") == EXCLUDED_REPOSITORY for prov in val_prov):
        raise ValueError("ANTHROPIC_PRESENT_IN_VALIDATION_UNEXPECTEDLY")

    kept_rows, kept_prov, kept_meta = [], [], []
    for index, (row, provenance, metadata) in enumerate(zip(train_rows, train_prov, train_meta)):
        if index in excluded_indices:
            continue
        kept_rows.append(row)
        kept_prov.append(provenance)
        kept_meta.append(metadata)

    shutil.copytree(BASE, STAGING)
    split["partitions"]["train"] = kept_meta
    split["split_policy"] += (
        " Round 23 excludes the complete Anthropic HH-RLHF red-team-attempt family from JB training: its native task label does not establish an explicit safety-bypass attempt, and source-family-held-out OOF produced zero JB recall on that 2,241-row family. No rows are relabeled; the family is removed from this new package."
    )

    test_keys = {
        (family.get("source_repository_id"), family.get("source_revision"), family.get("source_family_id"))
        for family in split["partitions"]["test"].get("families", [])
        if isinstance(family, dict)
    }
    anthropic_test_family_needed = (EXCLUDED_REPOSITORY, EXCLUDED_REVISION, EXCLUDED_FAMILY) in test_keys
    source_review["sources"] = [
        source for source in source_review["sources"]
        if not (
            source.get("source_repository_id") == EXCLUDED_REPOSITORY
            and source.get("source_revision") == EXCLUDED_REVISION
            and source.get("source_family_id") == EXCLUDED_FAMILY
            and (EXCLUDED_REPOSITORY, EXCLUDED_REVISION, EXCLUDED_FAMILY) not in test_keys
        )
    ]
    mapping["rules"] = [
        rule for rule in mapping["rules"]
        if not (rule.get("source_repository_id") == EXCLUDED_REPOSITORY
                and rule.get("mapping_rule_id") == "anthropic_single_human_turn_red_team_attempt_to_provisional_jb_attempt_r21")
    ]

    manifest["package_id"] = OUTPUT_ID
    manifest["dataset_version"] = OUTPUT_VERSION
    if not anthropic_test_family_needed:
        manifest["lineage_packages"] = [
            lineage for lineage in manifest.get("lineage_packages", [])
            if lineage != EXCLUDED_REPOSITORY + "@" + EXCLUDED_REVISION
        ]
    manifest["build_notes"]["round"] = 23
    manifest["build_notes"]["round23_excluded_train_rows_by_source"] = {EXCLUDED_REPOSITORY: len(excluded_indices)}
    manifest["build_notes"]["round23_semantic_exclusion_reason"] = (
        "The first human red-team turn is an attempted source task, not proof that each input explicitly attempts to bypass safety; held-out-family OOF showed zero JB recall on the family. Rows were excluded, not relabeled."
    )
    manifest["build_notes"]["formal_acceptance_gate"] = "GATE_UNSPECIFIED"
    manifest["build_notes"]["l3_run"] = False
    manifest["build_notes"]["smoke_run"] = False

    R21.assert_package_contract(STAGING, manifest, split, kept_rows, kept_prov, kept_meta,
                                val_rows, val_prov, split["partitions"]["validation"])
    write_jsonl(STAGING / "corpus" / "rows" / "train.jsonl", kept_rows)
    write_jsonl(STAGING / "corpus" / "provenance" / "train.jsonl", kept_prov)
    write_json(STAGING / "split_manifest.json", split)
    write_json(STAGING / "source_review.json", source_review)
    write_json(STAGING / "label_mapping.json", mapping)
    status = json.loads((STAGING / "STATUS.json").read_text(encoding="utf-8"))
    status.update({"package_id": OUTPUT_ID, "dataset_version": OUTPUT_VERSION, "l2_run": False,
                   "l3_run": False, "test_opened": False, "formal_acceptance_gate": "GATE_UNSPECIFIED"})
    write_json(STAGING / "STATUS.json", status)

    manifest["partitions"]["train"]["rows"]["sha256"] = sha256(STAGING / "corpus" / "rows" / "train.jsonl")
    manifest["partitions"]["train"]["provenance"]["sha256"] = sha256(STAGING / "corpus" / "provenance" / "train.jsonl")
    manifest["refs"]["split"]["sha256"] = sha256(STAGING / "split_manifest.json")
    manifest["refs"]["source_review"]["sha256"] = sha256(STAGING / "source_review.json")
    manifest["refs"]["label_mapping"]["sha256"] = sha256(STAGING / "label_mapping.json")
    write_json(STAGING / "DATASET_MANIFEST.json", manifest)

    if json.dumps(split["partitions"]["test"], sort_keys=True) != test_contract_snapshot:
        raise ValueError("ROUND23_TEST_FAMILY_CONTRACT_CHANGED")
    if manifest["partitions"]["test"] != {"sealed_contract": "split.partitions.test"}:
        raise ValueError("ROUND23_TEST_PAYLOAD_REFERENCE_PRESENT")
    for part in ("train", "validation"):
        for kind in ("rows", "provenance"):
            spec = manifest["partitions"][part][kind]
            if sha256(STAGING / spec["path"]) != spec["sha256"]:
                raise ValueError("ROUND23_FINAL_HASH_CHECK_FAILED:" + part + ":" + kind)

    STAGING.rename(OUTPUT)
    result = {
        "status": "BUILT_PENDING_ADAPTER_PREFLIGHT",
        "package_id": OUTPUT_ID,
        "dataset_version": OUTPUT_VERSION,
        "package_manifest_sha256": hashlib.sha256((OUTPUT / "DATASET_MANIFEST.json").read_bytes()).hexdigest(),
        "base_package_id": BASE_ID,
        "excluded_source_family": EXCLUDED_FAMILY,
        "excluded_rows": len(excluded_indices),
        "train_rows": len(kept_rows),
        "validation_rows": len(val_rows),
        "train_label_counts": dict(sorted(collections.Counter(row["label"] for row in kept_rows).items())),
        "validation_label_counts": dict(sorted(collections.Counter(row["label"] for row in val_rows).items())),
        "test_contract_unchanged": True,
        "test_payload_opened": False,
        "l3_run": False,
        "smoke_run": False,
        "formal_acceptance_gate": "GATE_UNSPECIFIED",
        "output_package": str(OUTPUT),
    }
    write_json(REPORT, result)
    return result


def main() -> int:
    result = build()
    print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
