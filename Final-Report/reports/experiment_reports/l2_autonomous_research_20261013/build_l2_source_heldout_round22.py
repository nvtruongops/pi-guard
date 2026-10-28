"""Add a single audited benign source family to Round 21 as immutable Round 22."""
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
VERSIONS = PRIVATE / "training_bases" / "datasets" / "project_training" / "versions"
BASE_ID = "pi_guard_l2_source_diverse_round21_r02"
BASE = VERSIONS / BASE_ID
OUTPUT_ID = "pi_guard_l2_source_diverse_round21_r04"
OUTPUT_VERSION = "0.8.5-source-diverse-l2-reference"
OUTPUT = VERSIONS / OUTPUT_ID
STAGING = VERSIONS / (OUTPUT_ID + ".building")
REPORT = ROOT / "l2_source_heldout_package_build_round22_r04.json"

REPOSITORY = "PolyAI-LDN/task-specific-datasets"
REVISION = "57ec275d8078af65b7731c2a98be812d844a6d6b"
UPSTREAM_FILE = "banking_data/train.csv"
SOURCE_FILE_SHA256 = "b06e26ac675513959a63135f11b94ea7786ed02da65db93a5650d8838cbc664b"
FAMILY_ID = "sf_banking77_train_round22"
LINEAGE_ID = "cl_banking77_train_57ec275d8078"
RULE_ID = "banking77_train_customer_service_intent_to_provisional_benign_round22"
LICENSE = "CC BY 4.0"
LOCATOR = "https://github.com/PolyAI-LDN/task-specific-datasets"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("HELPER_IMPORT_FAILED:" + name)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


R21 = load_module("l2_round21_package_helpers", ROOT / "build_l2_source_heldout_round21.py")
AUDIT = load_module("l2_banking77_round22_audit", ROOT / "audit_banking77_train_round22.py")


def write_json(path: Path, value: Any) -> None:
    R21.R18.write_json(path, value)


def write_jsonl(path: Path, values: list[dict]) -> None:
    R21.R18.write_jsonl(path, values)


def sha256_file(path: Path) -> str:
    return R21.sha256_file(path)


def load_base() -> tuple[dict, dict, dict, dict, list[dict], list[dict], list[dict], list[dict]]:
    manifest = json.loads((BASE / "DATASET_MANIFEST.json").read_text(encoding="utf-8"))
    split = json.loads((BASE / "split_manifest.json").read_text(encoding="utf-8"))
    review = json.loads((BASE / "source_review.json").read_text(encoding="utf-8"))
    mapping = json.loads((BASE / "label_mapping.json").read_text(encoding="utf-8"))
    train_rows = R21.read_jsonl(BASE / "corpus" / "rows" / "train.jsonl")
    train_prov = R21.read_jsonl(BASE / "corpus" / "provenance" / "train.jsonl")
    val_rows = R21.read_jsonl(BASE / "corpus" / "rows" / "validation.jsonl")
    val_prov = R21.read_jsonl(BASE / "corpus" / "provenance" / "validation.jsonl")
    if manifest.get("package_id") != BASE_ID:
        raise ValueError("UNEXPECTED_ROUND21_BASE_PACKAGE")
    if manifest.get("partitions", {}).get("test", {}).get("sealed_contract") is None:
        raise ValueError("ROUND21_FAMILY_ONLY_TEST_CONTRACT_MISSING")
    for partition, rows, provenance in (("train", train_rows, train_prov), ("validation", val_rows, val_prov)):
        spec = manifest["partitions"][partition]
        if len(rows) != len(provenance):
            raise ValueError("BASE_ROW_PROVENANCE_ALIGNMENT:" + partition)
        for kind in ("rows", "provenance"):
            path = BASE / spec[kind]["path"]
            if sha256_file(path) != spec[kind]["sha256"]:
                raise ValueError("ROUND21_BASE_HASH_MISMATCH:" + partition + ":" + kind)
    return manifest, split, review, mapping, train_rows, train_prov, val_rows, val_prov


def source_evidence(package: Path, report: dict) -> dict:
    counts = report["audit"]["counts"]
    findings = {
        "rights": {
            "source_repository_id": REPOSITORY,
            "source_revision": REVISION,
            "finding": "Publisher repository declares CC BY 4.0 for shared datasets; attribution is retained. Mixed-source package remains private and non-redistributive.",
            "license": LICENSE,
            "authorized_scope": "private_local_research_nonredistributive",
            "redistribution_allowed": False,
        },
        "lineage": {
            "source_repository_id": REPOSITORY,
            "source_revision": REVISION,
            "upstream_file": UPSTREAM_FILE,
            "upstream_split": "train only",
            "sha256": SOURCE_FILE_SHA256,
            "finding": "Pinned publisher training CSV only; no upstream test split was acquired or opened. One dataset/collection is treated as one source family.",
        },
        "privacy": {
            "source_repository_id": REPOSITORY,
            "source_revision": REVISION,
            "rows_screened": counts["publisher_train_rows"],
            "rows_retained": counts["eligible_after_exact_and_near_duplicate_gates"],
            "configured_pii_matches_excluded": counts.get("privacy_pattern_excluded", 0),
            "finding": "Configured email, SSN, IPv4, credential, key, bearer-token, and phone patterns were screened. Zero matches were observed, but this does not establish absence of PII.",
        },
    }
    refs = {}
    for kind, evidence in findings.items():
        path = package / "evidence" / "round22" / f"banking77_{kind}.json"
        write_json(path, evidence)
        refs[kind] = R21.R18.ref(path, package)
    return {
        "source_repository_id": REPOSITORY,
        "source_revision": REVISION,
        "source_family_id": FAMILY_ID,
        "license": LICENSE,
        "source_locator": LOCATOR,
        "rights_scope": "private_local_research_nonredistributive",
        "rights_notice": findings["rights"]["finding"],
        "rights_status": "research_only",
        "lineage_status": "verified",
        "privacy_status": "screened",
        "privacy_method": "configured PII regex patterns, publisher English/source metadata, exact deduplication, and 85% 5-word-shingle Jaccard duplicate screening against frozen Round 21 train/validation",
        "residual_limits": "Regex screening is incomplete; no human privacy adjudication was performed. Banking intent labels support only a provisional benign reference, not PI-Guard gold or broad benign coverage.",
        "historical_locked_rows_excluded": True,
        "redistribution_allowed": False,
        "rights_evidence": refs["rights"],
        "lineage_evidence": refs["lineage"],
        "privacy_evidence": refs["privacy"],
    }


def build() -> dict:
    if not BASE.is_dir():
        raise FileNotFoundError("ROUND21_BASE_PACKAGE_MISSING")
    if OUTPUT.exists() or STAGING.exists():
        raise FileExistsError("ROUND22_OUTPUT_OR_STAGING_ALREADY_EXISTS")
    report, eligible = AUDIT.run_audit()
    expected_count = report["audit"]["counts"]["eligible_after_exact_and_near_duplicate_gates"]
    if len(eligible) != expected_count or len(eligible) < 9000:
        raise ValueError("BANKING77_AUDIT_COUNT_GATE_FAILED")
    source_path = AUDIT.SOURCE_FILE
    if sha256_file(source_path) != SOURCE_FILE_SHA256:
        raise ValueError("BANKING77_PINNED_TRAIN_HASH_MISMATCH")

    shutil.copytree(BASE, STAGING)
    manifest, split, source_review, label_mapping, train_rows, train_prov, val_rows, val_prov = load_base()
    train_meta = split["partitions"]["train"]
    if len(train_meta) != len(train_rows):
        raise ValueError("ROUND21_TRAIN_METADATA_ALIGNMENT")

    candidates = []
    for normalized, category, ordinal, text in eligible:
        candidate = R21.make_candidate(
            "banking77", REPOSITORY, REVISION, UPSTREAM_FILE, f"train_row_{ordinal}",
            FAMILY_ID, LINEAGE_ID, category,
            RULE_ID, "benign", text, ordinal,
        )
        if candidate["normalized"] != normalized:
            raise ValueError("BANKING77_NORMALIZATION_DRIFT")
        candidates.append(candidate)

    before_ids = {row["id"] for row in train_rows}
    before_texts = {R21.normalize(row["text"]) for row in train_rows + val_rows}
    for candidate in candidates:
        if candidate["normalized"] in before_texts:
            raise ValueError("BANKING77_FROZEN_EXACT_DUPLICATE_REAPPEARED")
        row, provenance, meta = R21.make_row_records(candidate, "train")
        train_rows.append(row)
        train_prov.append(provenance)
        train_meta.append(meta)
    if len({row["id"] for row in train_rows}) != len(train_rows) or before_ids & {row["id"] for row in train_rows[len(before_ids):]}:
        raise ValueError("ROUND22_ROW_ID_COLLISION")

    split["partitions"]["train"] = train_meta
    split["split_policy"] += " Round 22 adds only pinned BANKING77 publisher train rows as one provisional benign source family after exact and 85%-near duplicate, language, and configured PII/attack-pattern screens; validation is unchanged."
    source_review["sources"].append(source_evidence(STAGING, report))
    if any(item["source_repository_id"] == REPOSITORY and item["source_revision"] == REVISION for item in source_review["sources"][:-1]):
        raise ValueError("BANKING77_SOURCE_ALREADY_PRESENT")
    native_categories = sorted({item["native_label"] for item in train_prov if item["source_repository_id"] == REPOSITORY})
    for category in native_categories:
        label_mapping["rules"].append({
            "source_repository_id": REPOSITORY,
            "native_label": category,
            "mapping_rule_id": RULE_ID,
            "label": "benign",
            "mapping_basis": "Publisher-defined online banking customer-service intent category; provisional private L2 benign reference only, not curator-reviewed gold.",
        })

    manifest["package_id"] = OUTPUT_ID
    manifest["dataset_version"] = OUTPUT_VERSION
    manifest["lineage_packages"] = list(manifest.get("lineage_packages", [])) + [REPOSITORY + "@" + REVISION]
    manifest["build_notes"]["round"] = 22
    manifest["build_notes"]["round22_admitted_additions_by_source"] = {"banking77": len(candidates)}
    manifest["build_notes"]["round22_source_audit"] = {
        "source_file_sha256": SOURCE_FILE_SHA256,
        "source_revision": REVISION,
        "publisher_test_opened": False,
        "test_contract_only": True,
        "formal_acceptance_gate": "GATE_UNSPECIFIED",
    }
    manifest["build_notes"]["l3_run"] = False
    manifest["build_notes"]["smoke_run"] = False

    R21.assert_package_contract(STAGING, manifest, split, train_rows, train_prov, train_meta,
                                val_rows, val_prov, split["partitions"]["validation"])
    write_jsonl(STAGING / "corpus" / "rows" / "train.jsonl", train_rows)
    write_jsonl(STAGING / "corpus" / "provenance" / "train.jsonl", train_prov)
    write_json(STAGING / "split_manifest.json", split)
    write_json(STAGING / "source_review.json", source_review)
    write_json(STAGING / "label_mapping.json", label_mapping)
    status = json.loads((STAGING / "STATUS.json").read_text(encoding="utf-8"))
    status.update({
        "package_id": OUTPUT_ID,
        "dataset_version": OUTPUT_VERSION,
        "schema": manifest["schema"],
        "language": "en",
        "trainable": True,
        "frozen_split": True,
        "distribution_scope": manifest["distribution_scope"],
        "l2_run": False,
        "l3_run": False,
        "test_opened": False,
        "formal_acceptance_gate": "GATE_UNSPECIFIED",
    })
    write_json(STAGING / "STATUS.json", status)

    manifest["partitions"]["train"]["rows"]["sha256"] = sha256_file(STAGING / "corpus" / "rows" / "train.jsonl")
    manifest["partitions"]["train"]["provenance"]["sha256"] = sha256_file(STAGING / "corpus" / "provenance" / "train.jsonl")
    manifest["refs"]["split"]["sha256"] = sha256_file(STAGING / "split_manifest.json")
    manifest["refs"]["source_review"]["sha256"] = sha256_file(STAGING / "source_review.json")
    manifest["refs"]["label_mapping"]["sha256"] = sha256_file(STAGING / "label_mapping.json")
    write_json(STAGING / "DATASET_MANIFEST.json", manifest)

    # Re-open only train/validation artifacts and verify the new hashes and row counts.
    final_manifest = json.loads((STAGING / "DATASET_MANIFEST.json").read_text(encoding="utf-8"))
    for partition in ("train", "validation"):
        for kind in ("rows", "provenance"):
            spec = final_manifest["partitions"][partition][kind]
            if sha256_file(STAGING / spec["path"]) != spec["sha256"]:
                raise ValueError("ROUND22_FINAL_HASH_CHECK_FAILED:" + partition + ":" + kind)
    if final_manifest["partitions"]["test"].get("sealed_contract") != manifest["partitions"]["test"].get("sealed_contract"):
        raise ValueError("ROUND22_SEALED_CONTRACT_CHANGED")
    if len(train_rows) != len(train_prov) or len(train_rows) != len(train_meta):
        raise ValueError("ROUND22_TRAIN_ALIGNMENT_FAILED")

    STAGING.rename(OUTPUT)
    output_manifest_sha = hashlib.sha256((OUTPUT / "DATASET_MANIFEST.json").read_bytes()).hexdigest()
    result = {
        "status": "BUILT_PENDING_ADAPTER_PREFLIGHT",
        "package_id": OUTPUT_ID,
        "dataset_version": OUTPUT_VERSION,
        "manifest_sha256": output_manifest_sha,
        "base_package_id": BASE_ID,
        "added_train_rows": len(candidates),
        "train_rows": len(train_rows),
        "validation_rows": len(val_rows),
        "train_label_counts": dict(sorted(collections.Counter(row["label"] for row in train_rows).items())),
        "validation_label_counts": dict(sorted(collections.Counter(row["label"] for row in val_rows).items())),
        "new_source_family_count": 1,
        "native_mapping_count": len(native_categories),
        "privacy_status": "screened_with_residual_risk",
        "formal_acceptance_gate": "GATE_UNSPECIFIED",
        "test_payload_opened": False,
        "l3_run": False,
        "smoke_run": False,
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
