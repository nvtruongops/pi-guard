"""Build a private, train-only R28 package for BlackboxNLP JB diagnostics."""
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
AUDIT_DIR = TRAINING / "datasets" / "source_audit" / "blackboxnlp_jb_round28"
BASE_ID = "pi_guard_l2_jbb_round27_baseline_20261014"
OUTPUT_ID = "pi_guard_l2_blackboxnlp_round28_candidate_r03_20261014"
OUTPUT_VERSION = "0.8.12-r28-blackboxnlp-provisional-r03"
BASE = VERSIONS / BASE_ID
OUTPUT = VERSIONS / OUTPUT_ID
STAGING = VERSIONS / (OUTPUT_ID + ".building")
AUDIT = ROOT / "blackboxnlp_jb_candidate_audit_round28.json"
CANDIDATES = AUDIT_DIR / "eligible_train_candidates.jsonl"
SOURCE_DIR = TRAINING / "datasets" / "source_datasets" / "jailbreak_features_blackboxnlp2025"
REPOSITORY = "sevdeawesome/jailbreak_success"
PAPER_REPOSITORY = "NLie2/what_features_jailbreak_LLMs"
FAMILY_ID = "sf_blackboxnlp_jailbreak_success_r28"
MAPPING_RULE = "blackboxnlp_attack_transformed_prompt_to_provisional_jb_attempt_r28"
LABEL_IDS = {"benign": 0, "PI": 1, "JB": 2}


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("HELPER_IMPORT_FAILED:" + name)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


R21 = load_module("l2_blackboxnlp_round28_helpers", ROOT / "build_l2_source_heldout_round21.py")


def write_json(path: Path, value: Any) -> None:
    R21.R18.write_json(path, value)


def write_jsonl(path: Path, values: list[dict]) -> None:
    R21.R18.write_jsonl(path, values)


def sha256(path: Path) -> str:
    return R21.sha256_file(path)


def ref(path: Path, package: Path) -> dict:
    return {"path": path.relative_to(package).as_posix(), "sha256": sha256(path)}


def load_candidates(audit: dict) -> list[dict]:
    if audit.get("audit_id") != "blackboxnlp_jailbreak_attempt_train_candidate_round28_v1":
        raise ValueError("BLACKBOXNLP_R28_AUDIT_ID_MISMATCH")
    if audit.get("comparison_package_id") != BASE_ID:
        raise ValueError("BLACKBOXNLP_R28_BASE_PACKAGE_MISMATCH")
    if audit.get("comparison_manifest_sha256") != sha256(BASE / "DATASET_MANIFEST.json"):
        raise ValueError("BLACKBOXNLP_R28_BASE_MANIFEST_HASH_MISMATCH")
    if not CANDIDATES.is_file() or sha256(CANDIDATES) != audit.get("candidate_file_sha256"):
        raise ValueError("BLACKBOXNLP_R28_CANDIDATE_HASH_MISMATCH")
    source_manifest = json.loads((SOURCE_DIR / "source_manifest.json").read_text(encoding="utf-8"))
    if (source_manifest.get("dataset_id") != REPOSITORY
            or source_manifest.get("pinned_revision") != audit.get("source_revision")):
        raise ValueError("BLACKBOXNLP_R28_SOURCE_MANIFEST_IDENTITY_MISMATCH")
    rows = R21.read_jsonl(CANDIDATES)
    if len(rows) != audit.get("eligible_unique_train_rows") or not rows:
        raise ValueError("BLACKBOXNLP_R28_CANDIDATE_COUNT_MISMATCH")
    if len({row["normalized_text_sha256"] for row in rows}) != len(rows):
        raise ValueError("BLACKBOXNLP_R28_CANDIDATE_DUPLICATE_TEXT")
    if len({row["source_record_id"] for row in rows}) != len(rows):
        raise ValueError("BLACKBOXNLP_R28_CANDIDATE_DUPLICATE_RECORD")
    return rows


def evidence_records(package: Path, audit: dict) -> tuple[dict, dict]:
    evidence_dir = package / "evidence" / "round28"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    rights_path = evidence_dir / "blackboxnlp_rights.json"
    lineage_path = evidence_dir / "blackboxnlp_lineage.json"
    privacy_path = evidence_dir / "blackboxnlp_privacy.json"
    write_json(rights_path, {
        "source_repository_id": REPOSITORY,
        "source_revision": audit["source_revision"],
        "paper_repository_id": PAPER_REPOSITORY,
        "paper_repository_revision": audit.get("paper_repository_revision"),
        "declared_license": audit.get("declared_license"),
        "authorized_scope": "private_local_research_nonredistributive",
        "redistribution_allowed": False,
        "finding": "The dataset card declares MIT, but this does not independently establish rights in the 300 seed prompts or every generated transformation. This package is restricted to private local L2 diagnostics; publication and redistribution are not cleared.",
    })
    write_json(lineage_path, {
        "source_repository_id": REPOSITORY,
        "source_revision": audit["source_revision"],
        "paper_repository_id": PAPER_REPOSITORY,
        "paper_repository_revision": audit.get("paper_repository_revision"),
        "source_file_sha256": audit["source_file_sha256"],
        "eligible_candidate_file_sha256": audit["candidate_file_sha256"],
        "seed_prompt_groups": audit["eligible_base_prompt_groups"],
        "attack_method_count": audit["distinct_attack_methods"],
        "finding": "The paper describes algorithmic transformations of 300 harmful seed prompts using 35 attack methods. The selected field is the final attack-transformed prompt; the original seed field and model success outcome are excluded. The methods and seed groups belong to one benchmark collection family, not independent sources; record-level upstream authorship and ancestry are unresolved.",
    })
    write_json(privacy_path, {
        "source_repository_id": REPOSITORY,
        "source_revision": audit["source_revision"],
        "normalized_unique_prompts_screened": audit["normalized_unique_attack_prompts"],
        "rows_retained": audit["eligible_unique_train_rows"],
        "configured_privacy_indicator_counts": audit["privacy_indicator_counts"],
        "finding": "Configured PII patterns and exact/near duplicates were screened, with no configured PII hits among retained rows. Attack content is sensitive by design; this automated screen is incomplete and no human privacy adjudication has been completed.",
    })
    source = {
        "source_repository_id": REPOSITORY,
        "source_revision": audit["source_revision"],
        "source_family_id": FAMILY_ID,
        "license": "MIT declared by dataset card; upstream seed and transformation rights unresolved",
        "source_locator": f"https://huggingface.co/datasets/{REPOSITORY}",
        "rights_scope": "private_local_research_nonredistributive",
        "rights_notice": "Private local L2 diagnostics only; no publication or redistribution clearance.",
        "rights_status": "research_only",
        "lineage_status": "verified",
        "privacy_status": "screened",
        "privacy_method": "Pinned source manifest and file hash; NFKC/casefold deduplication; 0.85 five-word-shingle screens against clean R05 train/validation and within source; configured PII regex screen; no human privacy adjudication",
        "residual_limits": "One algorithmic benchmark family; upstream seed rights and record-level authorship unresolved; no independent-source coverage; automated privacy screen incomplete; sensitive attack content retained by design.",
        "historical_locked_rows_excluded": True,
        "redistribution_allowed": False,
        "rights_evidence": ref(rights_path, package),
        "lineage_evidence": ref(lineage_path, package),
        "privacy_evidence": ref(privacy_path, package),
    }
    rule = {
        "source_repository_id": REPOSITORY,
        "native_label": "attack_transformed_prompt",
        "mapping_rule_id": MAPPING_RULE,
        "label": "JB",
        "mapping_basis": "Attack intent of the final transformed prompt is used only as a provisional JB-attempt reference. The source benchmark's success/failure outcome is not used as the input label. This is not a canonical or human-adjudicated PI-Guard label.",
    }
    return source, rule


def build() -> dict:
    if OUTPUT.exists() or STAGING.exists():
        raise FileExistsError("BLACKBOXNLP_R28_OUTPUT_OR_STAGING_EXISTS")
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    candidates = load_candidates(audit)
    base_manifest_path = BASE / "DATASET_MANIFEST.json"
    manifest = json.loads(base_manifest_path.read_text(encoding="utf-8"))
    split = json.loads((BASE / "split_manifest.json").read_text(encoding="utf-8"))
    source_review = json.loads((BASE / "source_review.json").read_text(encoding="utf-8"))
    mapping = json.loads((BASE / "label_mapping.json").read_text(encoding="utf-8"))
    status = json.loads((BASE / "STATUS.json").read_text(encoding="utf-8"))
    if manifest.get("package_id") != BASE_ID or status.get("package_id") != BASE_ID:
        raise ValueError("BLACKBOXNLP_R28_BASE_IDENTITY_MISMATCH")
    if status.get("frozen_split") is not True:
        raise ValueError("BLACKBOXNLP_R28_BASE_SPLIT_NOT_FROZEN")

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
                raise ValueError("BLACKBOXNLP_R28_BASE_HASH_MISMATCH:" + part + ":" + kind)
    frozen_test_contract = json.dumps(split["partitions"]["test"], sort_keys=True)
    if manifest.get("partitions", {}).get("test") != {"sealed_contract": "split.partitions.test"}:
        raise ValueError("BLACKBOXNLP_R28_TEST_PAYLOAD_REFERENCE_PRESENT")
    existing = {R21.normalize(row["text"]) for row in train_rows + val_rows}
    appended_rows, appended_prov, appended_meta = [], [], []
    for candidate in candidates:
        text = candidate["text"].strip()
        normalized = R21.normalize(text)
        if normalized in existing:
            raise ValueError("BLACKBOXNLP_R28_EXACT_OVERLAP_REAPPEARED")
        text_sha = R21.sha256_bytes(text.encode("utf-8"))
        row_id = "l2r28_" + R21.sha256_bytes(
            "\x1f".join((REPOSITORY, audit["source_revision"], candidate["source_record_id"], text_sha)).encode("utf-8")
        )[:32]
        prompt_family_id = "pf_blackboxnlp_seed_" + candidate["base_prompt_sha256"][:24]
        duplicate_group_id = "dg_blackboxnlp_text_" + candidate["normalized_text_sha256"][:24]
        appended_rows.append({"id": row_id, "text": text, "label": "JB", "label_id": LABEL_IDS["JB"]})
        appended_prov.append({
            "id": row_id,
            "source_repository_id": REPOSITORY,
            "source_revision": audit["source_revision"],
            "upstream_split": "unsplit_attack_attempt_collection_train_only",
            "source_record_id": candidate["source_record_id"],
            "source_family_id": FAMILY_ID,
            "collection_lineage_id": FAMILY_ID,
            "prompt_family_id": prompt_family_id,
            "duplicate_group_id": duplicate_group_id,
            "native_label": "attack_transformed_prompt",
            "mapping_rule_id": MAPPING_RULE,
            "attack_methods": candidate["methods"],
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

    shutil.copytree(BASE, STAGING)
    source, rule = evidence_records(STAGING, audit)
    source_review["sources"].append(source)
    mapping["rules"].append(rule)
    train_rows.extend(appended_rows)
    train_prov.extend(appended_prov)
    train_meta.extend(appended_meta)
    split["partitions"]["train"] = train_meta
    split["split_policy"] += (
        " Round 28 adds one pinned BlackboxNLP algorithmic jailbreak-attempt benchmark family to train only after exact/near-duplicate and configured PII screens; validation and family-only test contract are unchanged. The source remains provisional due to unresolved upstream seed rights, record-level lineage, and human privacy review."
    )
    manifest["package_id"] = OUTPUT_ID
    manifest["dataset_version"] = OUTPUT_VERSION
    manifest["lineage_packages"] = sorted(set(manifest.get("lineage_packages", [])) | {REPOSITORY + "@" + audit["source_revision"]})
    manifest["build_notes"].update({
        "round": 28,
        "round28_blackboxnlp_jb_rows_added": len(appended_rows),
        "round28_blackboxnlp_source_family_id": FAMILY_ID,
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
    write_jsonl(STAGING / manifest["partitions"]["validation"]["rows"]["path"], val_rows)
    write_jsonl(STAGING / manifest["partitions"]["validation"]["provenance"]["path"], val_prov)
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
    if json.dumps(split["partitions"]["test"], sort_keys=True) != frozen_test_contract:
        raise ValueError("BLACKBOXNLP_R28_TEST_CONTRACT_CHANGED")
    for part in ("train", "validation"):
        for kind in ("rows", "provenance"):
            spec = manifest["partitions"][part][kind]
            if sha256(STAGING / spec["path"]) != spec["sha256"]:
                raise ValueError("BLACKBOXNLP_R28_FINAL_HASH_MISMATCH:" + part + ":" + kind)
    if sha256(STAGING / manifest["partitions"]["validation"]["rows"]["path"]) != sha256(BASE / manifest["partitions"]["validation"]["rows"]["path"]):
        raise ValueError("BLACKBOXNLP_R28_VALIDATION_CHANGED")
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
        "validation_rows_byte_identical": True,
        "test_contract_unchanged": True,
        "test_payload_opened": False,
        "l3_run": False,
        "smoke_run": False,
        "formal_acceptance_gate": "GATE_UNSPECIFIED",
        "package_path_private": str(OUTPUT),
    }
    write_json(ROOT / "l2_blackboxnlp_package_build_round28.json", result)
    return result


if __name__ == "__main__":
    print(json.dumps(build(), ensure_ascii=False, indent=2), flush=True)
