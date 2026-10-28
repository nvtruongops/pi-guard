"""Build a private L2 train-only successor with the screened WUSTL JB family."""
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
PRIVATE = REPO / "workspaces" / "truongnv" / "pi_guard_pipeline"
TRAINING = PRIVATE / "training_bases"
VERSIONS = TRAINING / "datasets" / "project_training" / "versions"
BASE_ID = "pi_guard_l2_source_diverse_round21_r05"
OUTPUT_ID = "pi_guard_l2_source_diverse_round21_r06"
OUTPUT_VERSION = "0.8.7-source-diverse-wustl-jb-train"
BASE = VERSIONS / BASE_ID
OUTPUT = VERSIONS / OUTPUT_ID
STAGING = VERSIONS / (OUTPUT_ID + ".building")
AUDIT_DIR = PRIVATE / "training_bases" / "datasets" / "source_audit" / "wustl_round24"
AUDIT = ROOT / "wustl_jb_train_candidate_audit_round24.json"
CANDIDATES = AUDIT_DIR / "eligible_train_candidates.jsonl"
SOURCE_DIR = TRAINING / "datasets" / "source_datasets" / "wustl_llm_jailbreak_usenix2024"
REPOSITORY = "WUSTL-CSPL/LLMJailbreak"
REVISION = "2a9e665769de1bbfa657b6e6a9f88d9d427bc57c"
FAMILY_ID = "sf_wustl_cspl_online_jailbreaks_2024_r24"
MAPPING_RULE = "wustl_collected_jailbreak_prompt_to_provisional_jb_attempt_r24"
LABEL_IDS = {"benign": 0, "PI": 1, "JB": 2}


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("HELPER_IMPORT_FAILED:" + name)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


R21 = load_module("l2_wustl_round24_helpers", ROOT / "build_l2_source_heldout_round21.py")


def write_json(path: Path, value: Any) -> None:
    R21.R18.write_json(path, value)


def write_jsonl(path: Path, values: list[dict]) -> None:
    R21.R18.write_jsonl(path, values)


def sha256(path: Path) -> str:
    return R21.sha256_file(path)


def ref(path: Path, package: Path) -> dict:
    return {"path": path.relative_to(package).as_posix(), "sha256": sha256(path)}


def load_candidates(audit: dict) -> list[dict]:
    if audit.get("audit_id") != "wustl_jb_train_candidate_audit_round24_v1":
        raise ValueError("WUSTL_AUDIT_ID_MISMATCH")
    if audit.get("comparison_package_id") != BASE_ID:
        raise ValueError("WUSTL_AUDIT_BASE_PACKAGE_MISMATCH")
    if audit.get("comparison_manifest_sha256") != sha256(BASE / "DATASET_MANIFEST.json"):
        raise ValueError("WUSTL_AUDIT_BASE_MANIFEST_HASH_MISMATCH")
    if audit.get("source_revision") != REVISION:
        raise ValueError("WUSTL_AUDIT_REVISION_MISMATCH")
    expected = audit.get("eligible_candidate_file_sha256")
    if not expected or sha256(CANDIDATES) != expected:
        raise ValueError("WUSTL_ELIGIBLE_CANDIDATE_HASH_MISMATCH")
    source_manifest = json.loads((SOURCE_DIR / "source_manifest.json").read_text(encoding="utf-8"))
    if source_manifest.get("pinned_revision") != REVISION:
        raise ValueError("WUSTL_SOURCE_MANIFEST_REVISION_MISMATCH")
    rows = R21.read_jsonl(CANDIDATES)
    if len(rows) != audit.get("eligible_after_configured_privacy_and_duplicate_filters"):
        raise ValueError("WUSTL_CANDIDATE_COUNT_MISMATCH")
    if not rows or len({row["normalized_text_sha256"] for row in rows}) != len(rows):
        raise ValueError("WUSTL_CANDIDATE_UNIQUENESS_FAILURE")
    return rows


def evidence_records(package: Path, audit: dict) -> tuple[dict, dict]:
    evidence_dir = package / "evidence" / "round24"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    rights_path = evidence_dir / "wustl_rights.json"
    lineage_path = evidence_dir / "wustl_lineage.json"
    privacy_path = evidence_dir / "wustl_privacy.json"
    write_json(rights_path, {
        "source_repository_id": REPOSITORY,
        "source_revision": REVISION,
        "license": "MIT",
        "authorized_scope": "private_local_research_nonredistributive",
        "redistribution_allowed": False,
        "finding": "Pinned author repository declares MIT. The prompt collection was gathered from third-party online sources; repository licensing does not independently resolve every upstream post's rights. Included only for private local research; publication and redistribution are not authorized by this record.",
    })
    write_json(lineage_path, {
        "source_repository_id": REPOSITORY,
        "source_revision": REVISION,
        "upstream_file": "JailbreakPrompts.xlsx / Prompt column",
        "upstream_split": "unsplit collection assigned train-only",
        "source_workbook_sha256": audit["source_workbook_sha256"],
        "eligible_candidate_file_sha256": audit["eligible_candidate_file_sha256"],
        "finding": "Publisher paper/repository describe 448 collected in-the-wild jailbreak prompts. Exact and 0.85 5-word-shingle near duplicates against frozen r05 train/validation were excluded; the 120 retained candidates remain one collection family. Upstream online source ancestry is not row-addressable and shared community lineage remains possible.",
    })
    write_json(privacy_path, {
        "source_repository_id": REPOSITORY,
        "source_revision": REVISION,
        "rows_screened": audit["normalized_unique_candidate_prompts"],
        "rows_retained": audit["eligible_after_configured_privacy_and_duplicate_filters"],
        "configured_privacy_indicator_counts": audit["configured_privacy_indicator_counts"],
        "finding": "Configured email, US SSN, phone-candidate, IPv4 and credential-assignment patterns were screened; one phone-candidate hit was excluded. This incomplete automated screen is not human privacy clearance.",
    })
    source = {
        "source_repository_id": REPOSITORY,
        "source_revision": REVISION,
        "source_family_id": FAMILY_ID,
        "license": "MIT (repository declaration; third-party upstream rights remain unresolved)",
        "source_locator": "https://github.com/WUSTL-CSPL/LLMJailbreak/tree/2a9e665769de1bbfa657b6e6a9f88d9d427bc57c",
        "rights_scope": "private_local_research_nonredistributive",
        "rights_notice": "Private local research only; no publication or redistribution under this package record.",
        "rights_status": "research_only",
        "lineage_status": "verified",
        "privacy_status": "screened",
        "privacy_method": "NFKC/casefold exact normalization; 0.85 five-word-shingle Jaccard near-duplicate screen against frozen r05 train and validation; configured PII regex screen; no human privacy adjudication",
        "residual_limits": "Upstream online-source ancestry is not row-addressable; shared-community lineage remains possible; MIT repository metadata does not independently resolve every third-party prompt right; regex privacy screen is incomplete.",
        "historical_locked_rows_excluded": True,
        "redistribution_allowed": False,
        "rights_evidence": ref(rights_path, package),
        "lineage_evidence": ref(lineage_path, package),
        "privacy_evidence": ref(privacy_path, package),
    }
    rule = {
        "source_repository_id": REPOSITORY,
        "native_label": "collected_jailbreak_prompt",
        "mapping_rule_id": MAPPING_RULE,
        "label": "JB",
        "mapping_basis": "Publisher paper and repository describe the collected prompts as jailbreak attempts intended to circumvent model safety restrictions; provisional JB-attempt reference mapping only, not canonical or human-gold PI-Guard labels. The separate harmful-query seeds are not included.",
    }
    return source, rule


def build() -> dict:
    if OUTPUT.exists() or STAGING.exists():
        raise FileExistsError("ROUND24_OUTPUT_OR_STAGING_ALREADY_EXISTS")
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    candidates = load_candidates(audit)
    base_manifest_path = BASE / "DATASET_MANIFEST.json"
    manifest = json.loads(base_manifest_path.read_text(encoding="utf-8"))
    split = json.loads((BASE / "split_manifest.json").read_text(encoding="utf-8"))
    source_review = json.loads((BASE / "source_review.json").read_text(encoding="utf-8"))
    mapping = json.loads((BASE / "label_mapping.json").read_text(encoding="utf-8"))
    status = json.loads((BASE / "STATUS.json").read_text(encoding="utf-8"))
    if manifest.get("package_id") != BASE_ID or status.get("package_id") != BASE_ID:
        raise ValueError("ROUND24_BASE_IDENTITY_MISMATCH")
    if (REPOSITORY, REVISION, FAMILY_ID) in {
        (source.get("source_repository_id"), source.get("source_revision"), source.get("source_family_id"))
        for source in source_review["sources"]
    }:
        raise ValueError("ROUND24_SOURCE_ALREADY_PRESENT")

    train_rows = R21.read_jsonl(BASE / manifest["partitions"]["train"]["rows"]["path"])
    train_prov = R21.read_jsonl(BASE / manifest["partitions"]["train"]["provenance"]["path"])
    train_meta = split["partitions"]["train"]
    val_rows = R21.read_jsonl(BASE / manifest["partitions"]["validation"]["rows"]["path"])
    val_prov = R21.read_jsonl(BASE / manifest["partitions"]["validation"]["provenance"]["path"])
    val_meta = split["partitions"]["validation"]
    for part in ("train", "validation"):
        for kind in ("rows", "provenance"):
            spec = manifest["partitions"][part][kind]
            if sha256(BASE / spec["path"]) != spec["sha256"]:
                raise ValueError("ROUND24_BASE_HASH_MISMATCH:" + part + ":" + kind)

    frozen_test_contract = json.dumps(split["partitions"]["test"], sort_keys=True)
    existing_train_validation = {R21.normalize(row["text"]) for row in train_rows + val_rows}
    appended_rows, appended_prov, appended_meta = [], [], []
    for candidate in candidates:
        text = candidate["text"].strip()
        normalized = R21.normalize(text)
        if normalized in existing_train_validation:
            raise ValueError("ROUND24_EXACT_OVERLAP_REAPPEARED")
        text_sha = R21.sha256_bytes(text.encode("utf-8"))
        normalized_hash = candidate["normalized_text_sha256"]
        row_id = "l2r24_" + R21.sha256_bytes(
            "\x1f".join((REPOSITORY, REVISION, candidate["source_record_id"], text_sha)).encode("utf-8")
        )[:32]
        category_hash = R21.sha256_bytes(candidate["category"].encode("utf-8"))[:20]
        prompt_family_id = "pf_wustl_" + category_hash
        duplicate_group_id = "dg_" + normalized_hash[:24]
        appended_rows.append({"id": row_id, "text": text, "label": "JB", "label_id": LABEL_IDS["JB"]})
        appended_prov.append({
            "id": row_id,
            "source_repository_id": REPOSITORY,
            "source_revision": REVISION,
            "upstream_split": "unsplit_collection_train_only",
            "source_record_id": candidate["source_record_id"],
            "source_family_id": FAMILY_ID,
            "collection_lineage_id": FAMILY_ID,
            "prompt_family_id": prompt_family_id,
            "duplicate_group_id": duplicate_group_id,
            "native_label": "collected_jailbreak_prompt",
            "mapping_rule_id": MAPPING_RULE,
            "language": "en",
            "partition": "train",
            "text_sha256": text_sha,
        })
        appended_meta.append({
            "id": row_id,
            "label": "JB",
            "source_family_id": FAMILY_ID,
            "collection_lineage_id": FAMILY_ID,
            "prompt_family_id": prompt_family_id,
            "duplicate_group_id": duplicate_group_id,
        })
        existing_train_validation.add(normalized)

    shutil.copytree(BASE, STAGING)
    evidence_source, mapping_rule = evidence_records(STAGING, audit)
    source_review["sources"].append(evidence_source)
    mapping["rules"].append(mapping_rule)
    split["partitions"]["train"].extend(appended_meta)
    split["split_policy"] += (
        " Round 24 appends the pinned WUSTL-CSPL in-the-wild jailbreak collection to train only as one provisional family after exact/near-duplicate and configured privacy-pattern exclusions; validation and the family-only test contract are unchanged."
    )

    train_rows.extend(appended_rows)
    train_prov.extend(appended_prov)
    manifest["package_id"] = OUTPUT_ID
    manifest["dataset_version"] = OUTPUT_VERSION
    manifest["lineage_packages"] = sorted(set(manifest.get("lineage_packages", [])) | {REPOSITORY + "@" + REVISION})
    manifest["build_notes"]["round"] = 24
    manifest["build_notes"]["round24_wustl_jb_rows_added"] = len(appended_rows)
    manifest["build_notes"]["round24_wustl_jb_family_id"] = FAMILY_ID
    manifest["build_notes"]["formal_acceptance_gate"] = "GATE_UNSPECIFIED"
    manifest["build_notes"]["l3_run"] = False
    manifest["build_notes"]["smoke_run"] = False

    R21.assert_package_contract(STAGING, manifest, split, train_rows, train_prov, split["partitions"]["train"],
                                val_rows, val_prov, val_meta)
    write_jsonl(STAGING / manifest["partitions"]["train"]["rows"]["path"], train_rows)
    write_jsonl(STAGING / manifest["partitions"]["train"]["provenance"]["path"], train_prov)
    write_json(STAGING / "split_manifest.json", split)
    write_json(STAGING / "source_review.json", source_review)
    write_json(STAGING / "label_mapping.json", mapping)

    status.update({"package_id": OUTPUT_ID, "dataset_version": OUTPUT_VERSION, "l2_run": False,
                   "l3_run": False, "test_opened": False, "formal_acceptance_gate": "GATE_UNSPECIFIED"})
    write_json(STAGING / "STATUS.json", status)
    manifest["partitions"]["train"]["rows"]["sha256"] = sha256(STAGING / manifest["partitions"]["train"]["rows"]["path"])
    manifest["partitions"]["train"]["provenance"]["sha256"] = sha256(STAGING / manifest["partitions"]["train"]["provenance"]["path"])
    for name in ("split", "source_review", "label_mapping"):
        file_name = {"split": "split_manifest.json", "source_review": "source_review.json", "label_mapping": "label_mapping.json"}[name]
        manifest["refs"][name] = ref(STAGING / file_name, STAGING)
    write_json(STAGING / "DATASET_MANIFEST.json", manifest)

    if json.dumps(split["partitions"]["test"], sort_keys=True) != frozen_test_contract:
        raise ValueError("ROUND24_TEST_CONTRACT_CHANGED")
    if manifest["partitions"].get("test") != {"sealed_contract": "split.partitions.test"}:
        raise ValueError("ROUND24_TEST_PAYLOAD_REFERENCE_PRESENT")
    for part in ("train", "validation"):
        for kind in ("rows", "provenance"):
            spec = manifest["partitions"][part][kind]
            if sha256(STAGING / spec["path"]) != spec["sha256"]:
                raise ValueError("ROUND24_FINAL_HASH_CHECK_FAILED:" + part + ":" + kind)
    STAGING.rename(OUTPUT)

    result = {
        "status": "BUILT_PENDING_METADATA_ONLY_PREFLIGHT",
        "package_id": OUTPUT_ID,
        "dataset_version": OUTPUT_VERSION,
        "package_manifest_sha256": sha256(OUTPUT / "DATASET_MANIFEST.json"),
        "base_package_id": BASE_ID,
        "added_source_family": FAMILY_ID,
        "added_train_rows": len(appended_rows),
        "train_rows": len(train_rows),
        "validation_rows": len(val_rows),
        "train_label_counts": dict(sorted(collections.Counter(row["label"] for row in train_rows).items())),
        "validation_label_counts": dict(sorted(collections.Counter(row["label"] for row in val_rows).items())),
        "validation_rows_byte_identical": sha256(OUTPUT / manifest["partitions"]["validation"]["rows"]["path"]) == sha256(BASE / json.loads(base_manifest_path.read_text(encoding="utf-8"))["partitions"]["validation"]["rows"]["path"]),
        "test_contract_unchanged": True,
        "test_payload_opened": False,
        "l3_run": False,
        "smoke_run": False,
        "formal_acceptance_gate": "GATE_UNSPECIFIED",
        "package_path_private": str(OUTPUT),
    }
    write_json(ROOT / "l2_wustl_train_package_build_round24_r01.json", result)
    return result


if __name__ == "__main__":
    result = build()
    print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)
