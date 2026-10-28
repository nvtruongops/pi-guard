"""Build paired R27 L2 packages with identical cleaned validation data."""
from __future__ import annotations

import collections
import copy
import hashlib
import importlib.util
import json
import shutil
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
PRIVATE = REPO / "workspaces" / "truongnv" / "pi_guard_pipeline"
TRAINING = PRIVATE / "training_bases"
VERSIONS = TRAINING / "datasets" / "project_training" / "versions"
BASE_ID = "pi_guard_l2_source_diverse_round21_r05"
BASE = VERSIONS / BASE_ID
AUDIT = ROOT / "jbb_train_candidate_audit_round27.json"
CANDIDATES = TRAINING / "datasets" / "source_audit" / "jailbreakbench_artifacts_round27" / "eligible_train_candidates.jsonl"
OUTPUTS = {
    "baseline": ("pi_guard_l2_jbb_round27_baseline_20261014", "0.8.8-r27-clean-validation-baseline"),
    "candidate": ("pi_guard_l2_jbb_round27_candidate_20261014", "0.8.9-r27-jbb-train-candidate"),
}
REPOSITORY = "JailbreakBench/artifacts"
REVISION = "909e68c01d94222b8ad2e397a017e2e12e2adb73"
FAMILY_ID = "sf_jbb_attack_artifacts_r27"
MAPPING_RULE = "jbb_attack_artifact_prompt_to_provisional_jb_attempt_r27"
LABEL_IDS = {"benign": 0, "PI": 1, "JB": 2}


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("HELPER_IMPORT_FAILED:" + name)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


R21 = load_module("l2_jbb_round27_package_helpers", ROOT / "build_l2_source_heldout_round21.py")


def write_json(path: Path, value: Any) -> None:
    R21.R18.write_json(path, value)


def write_jsonl(path: Path, values: list[dict]) -> None:
    R21.R18.write_jsonl(path, values)


def sha256(path: Path) -> str:
    return R21.sha256_file(path)


def ref(path: Path, package: Path) -> dict:
    return {"path": path.relative_to(package).as_posix(), "sha256": sha256(path)}


def read_jsonl(path: Path) -> list[dict]:
    return R21.read_jsonl(path)


def validate_audit(audit: dict, base_manifest: dict) -> list[dict]:
    if audit.get("audit_id") != "jbb_non_jbc_train_candidate_round27_v1":
        raise ValueError("JBB_R27_AUDIT_ID_MISMATCH")
    if audit.get("source_repository_id") != REPOSITORY or audit.get("source_revision") != REVISION:
        raise ValueError("JBB_R27_SOURCE_IDENTITY_MISMATCH")
    if audit.get("comparison_package_id") != BASE_ID:
        raise ValueError("JBB_R27_BASE_PACKAGE_ID_MISMATCH")
    if audit.get("comparison_manifest_sha256") != sha256(BASE / "DATASET_MANIFEST.json"):
        raise ValueError("JBB_R27_BASE_PACKAGE_HASH_MISMATCH")
    if not CANDIDATES.is_file() or sha256(CANDIDATES) != audit.get("eligible_candidate_file_sha256"):
        raise ValueError("JBB_R27_CANDIDATE_FILE_HASH_MISMATCH")
    rows = read_jsonl(CANDIDATES)
    if len(rows) != audit.get("eligible_unique_train_rows") or not rows:
        raise ValueError("JBB_R27_CANDIDATE_COUNT_MISMATCH")
    if len({row["normalized_text_sha256"] for row in rows}) != len(rows):
        raise ValueError("JBB_R27_CANDIDATE_TEXT_DUPLICATES")
    if len({row["source_record_id"] for row in rows}) != len(rows):
        raise ValueError("JBB_R27_CANDIDATE_RECORD_ID_DUPLICATES")
    if len({row["behavior_ancestry_sha256"] for row in rows}) != audit.get("eligible_behavior_groups"):
        raise ValueError("JBB_R27_BEHAVIOR_GROUP_COUNT_MISMATCH")
    return rows


def build_evidence(package: Path, audit: dict) -> tuple[dict, dict]:
    evidence_dir = package / "evidence" / "round27"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    rights_path = evidence_dir / "jbb_rights.json"
    lineage_path = evidence_dir / "jbb_lineage.json"
    privacy_path = evidence_dir / "jbb_privacy.json"
    write_json(rights_path, {
        "source_repository_id": REPOSITORY,
        "source_revision": REVISION,
        "license": "MIT per JailbreakBench artifacts README; artifact-author ownership and upstream component rights are not independently confirmed",
        "authorized_scope": "private_local_research_nonredistributive",
        "redistribution_allowed": False,
        "finding": "First-party repository metadata declares MIT for each artifact and attributes ownership to its artifact author. This supports a private research reference, while individual author ownership and any upstream components remain unresolved; no publication or redistribution is authorized by this record.",
    })
    write_json(lineage_path, {
        "source_repository_id": REPOSITORY,
        "source_revision": REVISION,
        "source_file_manifest_sha256": audit["source_file_manifest_sha256"],
        "eligible_candidate_file_sha256": audit["eligible_candidate_file_sha256"],
        "source_files_selected": audit["source_file_count"],
        "methods_included": ["DSN", "GCG", "PAIR", "prompt_with_random_search"],
        "method_excluded": "JBC/manual; its 100 rows were in R05 validation and its community lineage overlaps other project sources",
        "finding": "Pinned first-party artifact files, prompt source-record hashes, attack-method/model fields, and behavior-ancestry hashes were recorded. All retained methods remain one benchmark collection family; method variants are not independent source families. Upstream prompt authorship and lineage beyond the artifact release are not row-addressable.",
    })
    write_json(privacy_path, {
        "source_repository_id": REPOSITORY,
        "source_revision": REVISION,
        "normalized_unique_non_jbc_prompts": audit["normalized_unique_non_jbc_prompts"],
        "rows_retained": audit["eligible_unique_train_rows"],
        "configured_privacy_indicator_counts": audit["privacy_indicator_counts"],
        "finding": "Configured email, US SSN, phone-candidate, IPv4, and credential-assignment patterns were screened; rows matching a configured pattern were excluded. This automated screen is incomplete and is not human privacy clearance.",
    })
    source = {
        "source_repository_id": REPOSITORY,
        "source_revision": REVISION,
        "source_family_id": FAMILY_ID,
        "license": "MIT (first-party artifact repository declaration; per-author ownership and upstream component rights remain unresolved)",
        "source_locator": f"https://github.com/{REPOSITORY}/tree/{REVISION}/attack-artifacts",
        "rights_scope": "private_local_research_nonredistributive",
        "rights_notice": "Private local research only; no publication or redistribution pending per-artifact ownership and upstream-rights review.",
        "rights_status": "research_only",
        "lineage_status": "verified",
        "privacy_status": "screened",
        "privacy_method": "Pinned file SHA-256 verification; NFKC/casefold exact deduplication; 0.85 five-word-shingle Jaccard screen against frozen R05 train and cleaned validation and within JBB; configured PII regex screen; no human privacy adjudication.",
        "residual_limits": "Artifact authorship and upstream source rights are unresolved; behavior grouping is benchmark-derived and does not prove independent community lineage; regex screening is incomplete and sensitive attack content is present by design.",
        "historical_locked_rows_excluded": True,
        "redistribution_allowed": False,
        "rights_evidence": ref(rights_path, package),
        "lineage_evidence": ref(lineage_path, package),
        "privacy_evidence": ref(privacy_path, package),
    }
    rule = {
        "source_repository_id": REPOSITORY,
        "native_label": "benchmark_attack_artifact_prompt",
        "mapping_rule_id": MAPPING_RULE,
        "label": "JB",
        "mapping_basis": "JailbreakBench defines these as attack prompts intended to bypass model safeguards; each final prompt is mapped only as a provisional single-turn JB-attempt reference. This is not a canonical PI-Guard label or human gold. Attack success is recorded as an outcome and is not used as the input label.",
    }
    return source, rule


def build_one(kind: str, base_parts: tuple, candidate_rows: list[dict], audit: dict,
              test_snapshot: str, base_manifest_sha: str) -> dict:
    output_id, version = OUTPUTS[kind]
    output = VERSIONS / output_id
    staging = VERSIONS / (output_id + ".building")
    if output.exists() or staging.exists():
        raise FileExistsError("R27_OUTPUT_OR_STAGING_ALREADY_EXISTS:" + kind)

    manifest, split, source_review, mapping, train_rows, train_prov, train_meta, val_rows, val_prov, val_meta = copy.deepcopy(base_parts)
    train_rows, train_prov, train_meta = list(train_rows), list(train_prov), list(train_meta)
    val_rows, val_prov, val_meta = list(val_rows), list(val_prov), list(val_meta)
    jbb_val_indices = {
        i for i, row in enumerate(val_prov)
        if row.get("source_repository_id") == REPOSITORY and row.get("source_revision") == REVISION
    }
    if len(jbb_val_indices) != audit["jbb_validation_rows_to_remove_from_both_packages"]:
        raise ValueError("R27_JBB_VALIDATION_ROW_COUNT_MISMATCH")
    if any(val_rows[i].get("label") != "JB" for i in jbb_val_indices):
        raise ValueError("R27_JBB_VALIDATION_LABEL_MISMATCH")
    val_rows = [row for i, row in enumerate(val_rows) if i not in jbb_val_indices]
    val_prov = [row for i, row in enumerate(val_prov) if i not in jbb_val_indices]
    val_meta = [row for i, row in enumerate(val_meta) if i not in jbb_val_indices]

    split["partitions"]["validation"] = val_meta
    split["split_policy"] += (
        " Round 27 removes the complete 100-row JBB JBC/manual family from validation because it overlaps the TrustAIR/JailbreakHub community lineage. The remaining ToxicChat JB validation family is retained; validation support for JB is 76, below the protocol's 100-row diagnostic floor."
    )
    source_review["sources"] = [
        source for source in source_review.get("sources", [])
        if not (source.get("source_repository_id") == REPOSITORY and source.get("source_revision") == REVISION)
    ]
    mapping["rules"] = [
        rule for rule in mapping.get("rules", [])
        if not (rule.get("source_repository_id") == REPOSITORY and rule.get("mapping_rule_id") == "jbb_jbc_manual_attempt_reference_r18")
    ]
    test_families = split["partitions"]["test"].get("families", [])
    if any(family.get("source_repository_id") == REPOSITORY and family.get("source_revision") == REVISION
           for family in test_families if isinstance(family, dict)):
        raise ValueError("R27_JBB_SOURCE_COLLIDES_WITH_SEALED_TEST_FAMILY")

    shutil.copytree(BASE, staging)
    if kind == "candidate":
        source, rule = build_evidence(staging, audit)
        source_review["sources"].append(source)
        mapping["rules"].append(rule)
        existing_norm = {R21.normalize(row["text"]) for row in train_rows + val_rows}
        for candidate in candidate_rows:
            text = candidate["text"].strip()
            normalized = R21.normalize(text)
            if not normalized or normalized in existing_norm:
                raise ValueError("R27_CANDIDATE_OVERLAPS_FROZEN_TRAIN_VALIDATION")
            text_sha = R21.sha256_bytes(text.encode("utf-8"))
            row_id = "l2r27_" + R21.sha256_bytes("\x1f".join((REPOSITORY, REVISION,
                candidate["source_record_id"], text_sha)).encode("utf-8"))[:32]
            behavior_id = "pf_jbb_behavior_" + candidate["behavior_ancestry_sha256"][:24]
            duplicate_id = "dg_jbb_text_" + candidate["normalized_text_sha256"][:24]
            train_rows.append({"id": row_id, "text": text, "label": "JB", "label_id": LABEL_IDS["JB"]})
            train_prov.append({
                "id": row_id,
                "source_repository_id": REPOSITORY,
                "source_revision": REVISION,
                "upstream_split": "pinned_attack_artifact_train_only",
                "source_record_id": candidate["source_record_id"],
                "source_family_id": FAMILY_ID,
                "collection_lineage_id": FAMILY_ID,
                "prompt_family_id": behavior_id,
                "duplicate_group_id": duplicate_id,
                "native_label": "benchmark_attack_artifact_prompt",
                "mapping_rule_id": MAPPING_RULE,
                "language": "en",
                "partition": "train",
                "text_sha256": text_sha,
            })
            train_meta.append({
                "id": row_id,
                "label": "JB",
                "source_family_id": FAMILY_ID,
                "collection_lineage_id": FAMILY_ID,
                "prompt_family_id": behavior_id,
                "duplicate_group_id": duplicate_id,
            })
            existing_norm.add(normalized)

    split["partitions"]["train"] = train_meta
    if json.dumps(split["partitions"]["test"], sort_keys=True) != test_snapshot:
        raise ValueError("R27_TEST_FAMILY_CONTRACT_CHANGED")
    if manifest.get("partitions", {}).get("test") != {"sealed_contract": "split.partitions.test"}:
        raise ValueError("R27_TEST_PAYLOAD_REFERENCE_PRESENT")

    manifest["package_id"] = output_id
    manifest["dataset_version"] = version
    manifest["lineage_packages"] = sorted({
        item for item in manifest.get("lineage_packages", [])
        if not item.startswith(REPOSITORY + "@")
    } | ({REPOSITORY + "@" + REVISION} if kind == "candidate" else set()))
    notes = manifest.setdefault("build_notes", {})
    notes.update({
        "round": 27,
        "round27_base_package_id": BASE_ID,
        "round27_base_manifest_sha256": base_manifest_sha,
        "round27_jbb_validation_rows_removed": len(jbb_val_indices),
        "round27_jbb_train_rows_added": len(candidate_rows) if kind == "candidate" else 0,
        "round27_jbb_source_family_id": FAMILY_ID if kind == "candidate" else None,
        "formal_acceptance_gate": "GATE_UNSPECIFIED",
        "l3_run": False,
        "smoke_run": False,
    })
    status = json.loads((staging / "STATUS.json").read_text(encoding="utf-8"))
    status.update({"package_id": output_id, "dataset_version": version, "l2_run": False,
                   "l3_run": False, "test_opened": False, "formal_acceptance_gate": "GATE_UNSPECIFIED"})

    R21.assert_package_contract(staging, manifest, split, train_rows, train_prov, train_meta,
                                val_rows, val_prov, val_meta)
    if kind == "candidate":
        write_jsonl(staging / manifest["partitions"]["train"]["rows"]["path"], train_rows)
        write_jsonl(staging / manifest["partitions"]["train"]["provenance"]["path"], train_prov)
    write_jsonl(staging / manifest["partitions"]["validation"]["rows"]["path"], val_rows)
    write_jsonl(staging / manifest["partitions"]["validation"]["provenance"]["path"], val_prov)
    write_json(staging / "split_manifest.json", split)
    write_json(staging / "source_review.json", source_review)
    write_json(staging / "label_mapping.json", mapping)
    write_json(staging / "STATUS.json", status)

    for part in ("train", "validation"):
        for kind_name in ("rows", "provenance"):
            spec = manifest["partitions"][part][kind_name]
            spec["sha256"] = sha256(staging / spec["path"])
    for name, filename in (("split", "split_manifest.json"), ("source_review", "source_review.json"), ("label_mapping", "label_mapping.json")):
        manifest["refs"][name] = ref(staging / filename, staging)
    write_json(staging / "DATASET_MANIFEST.json", manifest)
    for part in ("train", "validation"):
        for kind_name in ("rows", "provenance"):
            spec = manifest["partitions"][part][kind_name]
            if sha256(staging / spec["path"]) != spec["sha256"]:
                raise ValueError("R27_FINAL_PARTITION_HASH_MISMATCH:" + part + ":" + kind_name)
    staging.rename(output)
    return {
        "package_id": output_id,
        "dataset_version": version,
        "package_manifest_sha256": sha256(output / "DATASET_MANIFEST.json"),
        "train_rows": len(train_rows),
        "validation_rows": len(val_rows),
        "train_label_counts": dict(sorted(collections.Counter(row["label"] for row in train_rows).items())),
        "validation_label_counts": dict(sorted(collections.Counter(row["label"] for row in val_rows).items())),
        "train_family_counts": {label: len({row["source_family_id"] for row in train_meta if row["label"] == label}) for label in LABEL_IDS},
        "validation_family_counts": {label: len({row["source_family_id"] for row in val_meta if row["label"] == label}) for label in LABEL_IDS},
        "test_contract_unchanged": True,
        "test_payload_opened": False,
        "l3_run": False,
        "smoke_run": False,
        "output_private_path": str(output),
    }


def main() -> int:
    if not BASE.is_dir():
        raise FileNotFoundError("R05_BASE_PACKAGE_MISSING")
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    base_manifest_raw = (BASE / "DATASET_MANIFEST.json").read_bytes()
    manifest = json.loads(base_manifest_raw)
    candidate_rows = validate_audit(audit, manifest)
    split = json.loads((BASE / "split_manifest.json").read_text(encoding="utf-8"))
    source_review = json.loads((BASE / "source_review.json").read_text(encoding="utf-8"))
    mapping = json.loads((BASE / "label_mapping.json").read_text(encoding="utf-8"))
    status = json.loads((BASE / "STATUS.json").read_text(encoding="utf-8"))
    if manifest.get("package_id") != BASE_ID or status.get("package_id") != BASE_ID:
        raise ValueError("R27_BASE_IDENTITY_MISMATCH")
    if status.get("frozen_split") is not True:
        raise ValueError("R27_BASE_SPLIT_NOT_FROZEN")

    for part in ("train", "validation"):
        for kind in ("rows", "provenance"):
            spec = manifest["partitions"][part][kind]
            if sha256(BASE / spec["path"]) != spec["sha256"]:
                raise ValueError("R27_BASE_HASH_MISMATCH:" + part + ":" + kind)
    train_rows = read_jsonl(BASE / manifest["partitions"]["train"]["rows"]["path"])
    train_prov = read_jsonl(BASE / manifest["partitions"]["train"]["provenance"]["path"])
    val_rows = read_jsonl(BASE / manifest["partitions"]["validation"]["rows"]["path"])
    val_prov = read_jsonl(BASE / manifest["partitions"]["validation"]["provenance"]["path"])
    train_meta, val_meta = split["partitions"]["train"], split["partitions"]["validation"]
    if not (len(train_rows) == len(train_prov) == len(train_meta)) or not (len(val_rows) == len(val_prov) == len(val_meta)):
        raise ValueError("R27_BASE_SPLIT_ALIGNMENT_FAILURE")
    test_snapshot = json.dumps(split["partitions"]["test"], sort_keys=True)
    base_parts = (manifest, split, source_review, mapping, train_rows, train_prov, train_meta, val_rows, val_prov, val_meta)

    outputs = {}
    for kind in ("baseline", "candidate"):
        outputs[kind] = build_one(kind, base_parts, candidate_rows, audit, test_snapshot,
                                  hashlib.sha256(base_manifest_raw).hexdigest())
    baseline_path = VERSIONS / OUTPUTS["baseline"][0]
    candidate_path = VERSIONS / OUTPUTS["candidate"][0]
    for relative in ("corpus/rows/validation.jsonl", "corpus/provenance/validation.jsonl"):
        if sha256(baseline_path / relative) != sha256(candidate_path / relative):
            raise ValueError("R27_PAIRED_VALIDATION_MISMATCH:" + relative)
    result = {
        "build_id": "l2_jbb_paired_packages_round27_v1",
        "base_package_id": BASE_ID,
        "base_manifest_sha256": hashlib.sha256(base_manifest_raw).hexdigest(),
        "candidate_file_sha256": audit["eligible_candidate_file_sha256"],
        "packages": outputs,
        "paired_validation_byte_identical": True,
        "jbb_behavior_groups_kept_whole_in_train": audit["eligible_behavior_groups"],
        "jbb_validation_rows_removed": audit["jbb_validation_rows_to_remove_from_both_packages"],
        "validation_jb_support_after_cleanup": outputs["baseline"]["validation_label_counts"].get("JB", 0),
        "protocol_jb_support_diagnostic_floor": 100,
        "formal_acceptance_gate": "GATE_UNSPECIFIED",
        "test_payload_opened": False,
        "l3_run": False,
        "smoke_run": False,
    }
    write_json(ROOT / "l2_jbb_paired_packages_build_round27.json", result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
