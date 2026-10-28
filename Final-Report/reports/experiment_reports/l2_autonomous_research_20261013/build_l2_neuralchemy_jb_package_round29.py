"""Build a private train-only package for the qualified NeurAlchemy JB component."""
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
AUDIT_DIR = TRAINING / "datasets" / "source_audit" / "neuralchemy_jb_round29"
BASE_ID = "pi_guard_l2_jbb_round27_baseline_20261014"
OUTPUT_ID = "pi_guard_l2_neuralchemy_jb_round29_candidate_20261014"
OUTPUT_VERSION = "0.8.13-r29-neuralchemy-jb-provisional"
BASE = VERSIONS / BASE_ID
OUTPUT = VERSIONS / OUTPUT_ID
STAGING = VERSIONS / (OUTPUT_ID + ".building")
AUDIT = ROOT / "neuralchemy_jb_component_audit_round29.json"
CANDIDATES = AUDIT_DIR / "eligible_train_candidates.jsonl"
REPOSITORY = "neuralchemy/Prompt-injection-dataset"
REVISION = "7d70432dfcf47a821612cbf9d34e9d9e3ad20e75"
FAMILY_ID = "sf_neuralchemy_original_attack_db_jb_r29"
NATIVE_LABEL = "neuralchemy_v1:jailbreak"
MAPPING_RULE = "neuralchemy_original_attack_db_jailbreak_to_provisional_jb_r29"
LABEL_IDS = {"benign": 0, "PI": 1, "JB": 2}


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("HELPER_IMPORT_FAILED:" + name)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


R21 = load_module("l2_neuralchemy_jb_round29_helpers", ROOT / "build_l2_source_heldout_round21.py")


def write_json(path: Path, value: Any) -> None:
    R21.R18.write_json(path, value)


def write_jsonl(path: Path, values: list[dict]) -> None:
    R21.R18.write_jsonl(path, values)


def sha256(path: Path) -> str:
    return R21.sha256_file(path)


def ref(path: Path, package: Path) -> dict:
    return {"path": path.relative_to(package).as_posix(), "sha256": sha256(path)}


def load_candidates(audit: dict) -> list[dict]:
    if audit.get("audit_id") != "neuralchemy_original_attack_db_jb_train_candidate_round29_v1":
        raise ValueError("NEURALCHEMY_R29_AUDIT_ID_MISMATCH")
    if audit.get("comparison_package_id") != BASE_ID:
        raise ValueError("NEURALCHEMY_R29_BASE_PACKAGE_MISMATCH")
    if audit.get("comparison_manifest_sha256") != sha256(BASE / "DATASET_MANIFEST.json"):
        raise ValueError("NEURALCHEMY_R29_BASE_MANIFEST_HASH_MISMATCH")
    if not CANDIDATES.is_file() or sha256(CANDIDATES) != audit.get("candidate_file_sha256"):
        raise ValueError("NEURALCHEMY_R29_CANDIDATE_HASH_MISMATCH")
    rows = R21.read_jsonl(CANDIDATES)
    if len(rows) != audit.get("eligible_unique_train_rows") or not rows:
        raise ValueError("NEURALCHEMY_R29_CANDIDATE_COUNT_MISMATCH")
    if len({row["normalized_text_sha256"] for row in rows}) != len(rows):
        raise ValueError("NEURALCHEMY_R29_DUPLICATE_NORMALIZED_TEXT")
    if len({row["source_record_id"] for row in rows}) != len(rows):
        raise ValueError("NEURALCHEMY_R29_DUPLICATE_RECORD_ID")
    if len({row["prompt_group_sha256"] for row in rows}) != audit.get("eligible_prompt_groups"):
        raise ValueError("NEURALCHEMY_R29_PROMPT_GROUP_COUNT_MISMATCH")
    return rows


def evidence_records(package: Path, audit: dict) -> tuple[dict, dict]:
    evidence_dir = package / "evidence" / "round29"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    rights_path = evidence_dir / "neuralchemy_rights.json"
    lineage_path = evidence_dir / "neuralchemy_lineage.json"
    privacy_path = evidence_dir / "neuralchemy_privacy.json"
    write_json(rights_path, {
        "source_repository_id": REPOSITORY,
        "source_revision": REVISION,
        "component": "neuralchemy_v1 original attack_db",
        "declared_license": "Apache-2.0 per pinned publisher card and source-component table",
        "authorized_scope": "private_local_research_nonredistributive",
        "redistribution_allowed": False,
        "finding": "The pinned publisher card assigns Apache-2.0 to the neuralchemy_v1 original attack_db component. The row-level license field is empty and the publisher does not resolve every prompt's upstream authorship; this package is restricted to private local research pending owner review.",
    })
    write_json(lineage_path, {
        "source_repository_id": REPOSITORY,
        "source_revision": REVISION,
        "component": "neuralchemy_v1 original attack_db",
        "upstream_partition": "core/train only",
        "source_train_sha256": audit["source_train_sha256"],
        "eligible_candidate_file_sha256": audit["candidate_file_sha256"],
        "candidate_rows": audit["eligible_unique_train_rows"],
        "prompt_groups": audit["eligible_prompt_groups"],
        "finding": "Every retained record is traced to a pinned core/train row whose publisher component is neuralchemy_v1, category is jailbreak, binary label is 1, and augmented flag is false. This component is distinct from the separately listed HackAPrompt competition component. The publisher provides no deeper record-level upstream ancestry or human-authorship evidence.",
    })
    write_json(privacy_path, {
        "source_repository_id": REPOSITORY,
        "source_revision": REVISION,
        "rows_screened": audit["normalized_unique_candidate_prompts"],
        "rows_retained": audit["eligible_unique_train_rows"],
        "configured_privacy_pattern_hits": audit["configured_privacy_pattern_hits"],
        "finding": "Configured email, SSN, phone-candidate, IPv4, credential-assignment, private-key, and bearer-token patterns were screened; no configured hits remained. This is an incomplete automated screen and not human privacy clearance. Attack prompts are sensitive by design.",
    })
    source = {
        "source_repository_id": REPOSITORY,
        "source_revision": REVISION,
        "source_family_id": FAMILY_ID,
        "license": "Apache-2.0 (publisher-declared for neuralchemy_v1 original attack_db; row-level license values empty)",
        "source_locator": f"https://huggingface.co/datasets/{REPOSITORY}/tree/{REVISION}",
        "rights_scope": "private_local_research_nonredistributive",
        "rights_notice": "Private local research pending owner review of row-level upstream authorship and privacy; no redistribution under this package record.",
        "rights_status": "research_only",
        "lineage_status": "verified",
        "privacy_status": "screened",
        "privacy_method": "Pinned core/train parquet hash; component/category/label/augmentation filters; NFKC/casefold exact normalization; 0.85 five-word-shingle screens against clean R05 train/validation and within candidates; configured PII regex screen; no human privacy adjudication",
        "residual_limits": "Publisher identifies this as the neuralchemy_v1 original attack_db component but does not document per-record upstream authorship; row-level license fields are empty; configured privacy screening is incomplete; labels are provisional references only.",
        "historical_locked_rows_excluded": True,
        "redistribution_allowed": False,
        "rights_evidence": ref(rights_path, package),
        "lineage_evidence": ref(lineage_path, package),
        "privacy_evidence": ref(privacy_path, package),
    }
    rule = {
        "source_repository_id": REPOSITORY,
        "native_label": NATIVE_LABEL,
        "mapping_rule_id": MAPPING_RULE,
        "label": "JB",
        "mapping_basis": "Publisher's explicit category=jailbreak under neuralchemy_v1 original attack_db is used as a provisional single-prompt JB-attempt reference. The binary malicious label alone is not used. This is not a canonical or human-adjudicated PI-Guard label.",
    }
    return source, rule


def build() -> dict:
    if OUTPUT.exists() or STAGING.exists():
        raise FileExistsError("NEURALCHEMY_R29_OUTPUT_OR_STAGING_EXISTS")
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    candidates = load_candidates(audit)
    manifest_path = BASE / "DATASET_MANIFEST.json"
    manifest_raw = manifest_path.read_bytes()
    manifest = json.loads(manifest_raw)
    split = json.loads((BASE / "split_manifest.json").read_text(encoding="utf-8"))
    source_review = json.loads((BASE / "source_review.json").read_text(encoding="utf-8"))
    mapping = json.loads((BASE / "label_mapping.json").read_text(encoding="utf-8"))
    status = json.loads((BASE / "STATUS.json").read_text(encoding="utf-8"))
    if manifest.get("package_id") != BASE_ID or status.get("package_id") != BASE_ID:
        raise ValueError("NEURALCHEMY_R29_BASE_IDENTITY_MISMATCH")
    if status.get("frozen_split") is not True:
        raise ValueError("NEURALCHEMY_R29_BASE_SPLIT_NOT_FROZEN")

    train_rows = R21.read_jsonl(BASE / manifest["partitions"]["train"]["rows"]["path"])
    train_prov = R21.read_jsonl(BASE / manifest["partitions"]["train"]["provenance"]["path"])
    train_meta = split["partitions"]["train"]
    val_rows = R21.read_jsonl(BASE / manifest["partitions"]["validation"]["rows"]["path"])
    val_prov = R21.read_jsonl(BASE / manifest["partitions"]["validation"]["provenance"]["path"])
    val_meta = split["partitions"]["validation"]
    if not (len(train_rows) == len(train_prov) == len(train_meta)) or not (len(val_rows) == len(val_prov) == len(val_meta)):
        raise ValueError("NEURALCHEMY_R29_BASE_ALIGNMENT_FAILURE")
    for part in ("train", "validation"):
        for kind in ("rows", "provenance"):
            spec = manifest["partitions"][part][kind]
            if sha256(BASE / spec["path"]) != spec["sha256"]:
                raise ValueError("NEURALCHEMY_R29_BASE_HASH_MISMATCH:" + part + ":" + kind)

    test_contract_snapshot = json.dumps(split["partitions"]["test"], sort_keys=True)
    existing = {R21.normalize(row["text"]) for row in train_rows + val_rows}
    base_ids = {row["id"] for row in train_rows}
    appended_rows, appended_prov, appended_meta = [], [], []
    for candidate in candidates:
        text = candidate["text"].strip()
        normalized = R21.normalize(text)
        if normalized in existing:
            raise ValueError("NEURALCHEMY_R29_EXACT_OVERLAP_REAPPEARED")
        text_sha = R21.sha256_bytes(text.encode("utf-8"))
        row_id = "l2r29_" + R21.sha256_bytes(
            "\x1f".join((REPOSITORY, REVISION, candidate["source_record_id"], text_sha)).encode("utf-8")
        )[:32]
        prompt_family_id = "pf_neuralchemy_jb_" + candidate["prompt_group_sha256"][:24]
        duplicate_group_id = "dg_neuralchemy_jb_" + candidate["normalized_text_sha256"][:24]
        appended_rows.append({"id": row_id, "text": text, "label": "JB", "label_id": LABEL_IDS["JB"]})
        appended_prov.append({
            "id": row_id,
            "source_repository_id": REPOSITORY,
            "source_revision": REVISION,
            "upstream_split": "core/train",
            "source_record_id": candidate["source_record_id"],
            "source_family_id": FAMILY_ID,
            "collection_lineage_id": FAMILY_ID,
            "prompt_family_id": prompt_family_id,
            "duplicate_group_id": duplicate_group_id,
            "native_label": NATIVE_LABEL,
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
        existing.add(normalized)

    if base_ids & {row["id"] for row in appended_rows}:
        raise ValueError("NEURALCHEMY_R29_ROW_ID_COLLISION")
    shutil.copytree(BASE, STAGING)
    source, rule = evidence_records(STAGING, audit)
    source_review["sources"].append(source)
    mapping["rules"].append(rule)
    train_rows.extend(appended_rows)
    train_prov.extend(appended_prov)
    train_meta.extend(appended_meta)
    split["partitions"]["train"] = train_meta
    split["split_policy"] += (
        " Round 29 adds only the pinned NeurAlchemy neuralchemy_v1 original-attack-db category=jailbreak core/train component as one provisional JB source family, after exact/near-duplicate and configured privacy-pattern screening. Validation and the family-only test contract remain unchanged."
    )
    manifest["package_id"] = OUTPUT_ID
    manifest["dataset_version"] = OUTPUT_VERSION
    manifest["lineage_packages"] = sorted(set(manifest.get("lineage_packages", [])) | {REPOSITORY + "@" + REVISION})
    manifest["build_notes"].update({
        "round": 29,
        "round29_neuralchemy_jb_train_rows_added": len(appended_rows),
        "round29_neuralchemy_jb_family_id": FAMILY_ID,
        "formal_acceptance_gate": "GATE_UNSPECIFIED",
        "l3_run": False,
        "smoke_run": False,
    })
    status.update({"package_id": OUTPUT_ID, "dataset_version": OUTPUT_VERSION, "l2_run": False,
                   "l3_run": False, "test_opened": False, "formal_acceptance_gate": "GATE_UNSPECIFIED"})

    R21.assert_package_contract(STAGING, manifest, split, train_rows, train_prov, train_meta,
                                val_rows, val_prov, val_meta)
    write_jsonl(STAGING / manifest["partitions"]["train"]["rows"]["path"], train_rows)
    write_jsonl(STAGING / manifest["partitions"]["train"]["provenance"]["path"], train_prov)
    write_json(STAGING / "split_manifest.json", split)
    write_json(STAGING / "source_review.json", source_review)
    write_json(STAGING / "label_mapping.json", mapping)
    write_json(STAGING / "STATUS.json", status)
    for part in ("train", "validation"):
        for kind in ("rows", "provenance"):
            spec = manifest["partitions"][part][kind]
            spec["sha256"] = sha256(STAGING / spec["path"])
    for name, filename in (("split", "split_manifest.json"), ("source_review", "source_review.json"), ("label_mapping", "label_mapping.json")):
        manifest["refs"][name] = ref(STAGING / filename, STAGING)
    write_json(STAGING / "DATASET_MANIFEST.json", manifest)
    if json.dumps(split["partitions"]["test"], sort_keys=True) != test_contract_snapshot:
        raise ValueError("NEURALCHEMY_R29_TEST_FAMILY_CONTRACT_CHANGED")
    if sha256(STAGING / manifest["partitions"]["validation"]["rows"]["path"]) != sha256(BASE / manifest["partitions"]["validation"]["rows"]["path"]):
        raise ValueError("NEURALCHEMY_R29_VALIDATION_CHANGED")
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
        "validation_rows_byte_identical": sha256(OUTPUT / manifest["partitions"]["validation"]["rows"]["path"]) == sha256(BASE / manifest["partitions"]["validation"]["rows"]["path"]),
        "test_contract_unchanged": True,
        "test_payload_opened": False,
        "l3_run": False,
        "smoke_run": False,
        "formal_acceptance_gate": "GATE_UNSPECIFIED",
        "package_path_private": str(OUTPUT),
    }
    write_json(ROOT / "l2_neuralchemy_jb_package_build_round29.json", result)
    return result


if __name__ == "__main__":
    print(json.dumps(build(), ensure_ascii=False, indent=2), flush=True)
