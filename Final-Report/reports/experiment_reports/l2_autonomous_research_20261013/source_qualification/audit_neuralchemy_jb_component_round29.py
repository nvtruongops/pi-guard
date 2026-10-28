"""Aggregate-audit the pinned NeurAlchemy original jailbreak component."""
from __future__ import annotations

import collections
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any

import pyarrow.parquet as pq

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REPO = ROOT.parents[3]
TRAINING = REPO / "workspaces" / "truongnv" / "pi_guard_pipeline" / "training_bases"
ACQUIRED = HERE / "acquired"
SHARD = ACQUIRED / "neuralchemy_core_train.parquet"
SHARD_MANIFEST = ACQUIRED / "neuralchemy_core_train_manifest.json"
CARD = HERE / "neuralchemy__Prompt-injection-dataset__README.md"
PRIOR_AUDIT = HERE / "neuralchemy_source_component_audit_round03.json"
BASE_ID = "pi_guard_l2_jbb_round27_baseline_20261014"
BASE = TRAINING / "datasets" / "project_training" / "versions" / BASE_ID
OUTPUT_DIR = TRAINING / "datasets" / "source_audit" / "neuralchemy_jb_round29"
CANDIDATE_PATH = OUTPUT_DIR / "eligible_train_candidates.jsonl"
REPORT = ROOT / "neuralchemy_jb_component_audit_round29.json"
REPOSITORY = "neuralchemy/Prompt-injection-dataset"
REVISION = "7d70432dfcf47a821612cbf9d34e9d9e3ad20e75"
FAMILY_ID = "sf_neuralchemy_original_attack_db_jb_r29"
SIMILARITY_PERCENT = 85

PII_PATTERNS = {
    "email": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "us_ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "phone_candidate": re.compile(r"(?<!\w)(?:\+?\d[\d .()\-]{8,}\d)(?!\w)"),
    "ipv4": re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b"),
    "credential_assignment": re.compile(r"(?i)\b(?:api[_ -]?key|access[_ -]?token|password|passwd|secret)\s*[:=]\s*[^\s,;]+"),
    "private_key": re.compile(r"(?i)-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "bearer_token": re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]{16,}"),
}


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("HELPER_IMPORT_FAILED:" + name)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


DEDUP = load_module("l2_neuralchemy_jb_round29_dedup", ROOT / "audit_jbb_train_candidate_round27.py")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as stream:
        return [json.loads(line) for line in stream]


def main() -> int:
    source_manifest = json.loads(SHARD_MANIFEST.read_text(encoding="utf-8"))
    prior_audit = json.loads(PRIOR_AUDIT.read_text(encoding="utf-8"))
    if source_manifest.get("dataset_id") != REPOSITORY or source_manifest.get("revision") != REVISION:
        raise ValueError("NEURALCHEMY_R29_SOURCE_IDENTITY_MISMATCH")
    if sha256_file(SHARD) != source_manifest.get("sha256"):
        raise ValueError("NEURALCHEMY_R29_PINNED_TRAIN_HASH_MISMATCH")
    if (prior_audit.get("revision") != REVISION
            or prior_audit.get("shard_sha256") != sha256_file(SHARD)
            or prior_audit.get("card_sha256") != sha256_file(CARD)
            or prior_audit.get("rows") != 4391):
        raise ValueError("NEURALCHEMY_R29_PRIOR_AUDIT_INPUT_MISMATCH")
    if not BASE.is_dir():
        raise FileNotFoundError("R27_CLEAN_BASELINE_MISSING")
    manifest_path = BASE / "DATASET_MANIFEST.json"
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes)
    if manifest.get("package_id") != BASE_ID:
        raise ValueError("NEURALCHEMY_R29_BASE_PACKAGE_ID_MISMATCH")

    prior_texts: dict[str, set[str]] = {"train": set(), "validation": set()}
    for part in ("train", "validation"):
        rows_path = BASE / manifest["partitions"][part]["rows"]["path"]
        prov_path = BASE / manifest["partitions"][part]["provenance"]["path"]
        if (sha256_file(rows_path) != manifest["partitions"][part]["rows"]["sha256"]
                or sha256_file(prov_path) != manifest["partitions"][part]["provenance"]["sha256"]):
            raise ValueError("NEURALCHEMY_R29_BASE_PARTITION_HASH_MISMATCH:" + part)
        rows, provenance = read_jsonl(rows_path), read_jsonl(prov_path)
        if len(rows) != len(provenance):
            raise ValueError("NEURALCHEMY_R29_BASE_ALIGNMENT_FAILURE:" + part)
        for row, sidecar in zip(rows, provenance):
            if row.get("id") != sidecar.get("id"):
                raise ValueError("NEURALCHEMY_R29_BASE_ID_ALIGNMENT_FAILURE:" + part)
            key = DEDUP.normalize(str(row.get("text", "")))
            if key:
                prior_texts[part].add(key)

    raw_counts: collections.Counter[str] = collections.Counter()
    category_counts: collections.Counter[str] = collections.Counter()
    component_counts: collections.Counter[str] = collections.Counter()
    pii_counts: collections.Counter[str] = collections.Counter()
    candidates: dict[str, dict[str, Any]] = {}
    source_rows = pq.read_table(SHARD, columns=["text", "source", "category", "label", "augmented", "group_id"]).to_pylist()
    for ordinal, row in enumerate(source_rows):
        source = str(row.get("source") or "")
        category = str(row.get("category") or "")
        label = str(row.get("label"))
        if source == "neuralchemy_v1":
            component_counts["rows"] += 1
            component_counts["jailbreak_category"] += category == "jailbreak"
            component_counts["malicious_label"] += label == "1"
            component_counts["augmented_false"] += row.get("augmented") is False
        if source != "neuralchemy_v1" or category != "jailbreak" or label != "1" or row.get("augmented") is not False:
            continue
        raw_counts["candidate_rows"] += 1
        text = row.get("text")
        group = row.get("group_id")
        if not isinstance(text, str) or not text.strip() or group is None:
            raw_counts["missing_required_metadata"] += 1
            continue
        key = DEDUP.normalize(text)
        if not key:
            raw_counts["empty_normalized_text"] += 1
            continue
        hits = [name for name, pattern in PII_PATTERNS.items() if pattern.search(text)]
        if hits:
            raw_counts["privacy_pattern_excluded"] += 1
            for name in hits:
                pii_counts[name] += 1
            continue
        raw_counts["privacy_cleared_rows"] += 1
        group_hash = sha256_bytes(str(group).encode("utf-8"))
        record_hash = sha256_bytes((REVISION + "\x1f" + str(ordinal) + "\x1f" + group_hash).encode("utf-8"))
        candidates.setdefault(key, {
            "text": text,
            "source_record_id": "src_neuralchemy_core_" + record_hash[:28],
            "normalized_text_sha256": sha256_bytes(key.encode("utf-8")),
            "prompt_group_sha256": group_hash,
        })

    exact_unique = len(candidates)
    all_prior = prior_texts["train"] | prior_texts["validation"]
    exact_overlap_train = len(set(candidates) & prior_texts["train"])
    exact_overlap_validation = len(set(candidates) & prior_texts["validation"])
    exact_overlap = set(candidates) & all_prior
    after_exact = {key: value for key, value in candidates.items() if key not in exact_overlap}
    prior_hashes = {key: DEDUP.shingle_hashes(key) for key in all_prior}
    candidate_hashes = {key: DEDUP.shingle_hashes(key) for key in after_exact}
    near_base = DEDUP.near_candidate_keys(candidate_hashes, prior_hashes)
    after_base_near = {key: value for key, value in after_exact.items() if key not in near_base}
    within_hashes = {key: DEDUP.shingle_hashes(key) for key in after_base_near}
    within_near = DEDUP.candidate_near_pairs(within_hashes)
    eligible = [after_base_near[key] for key in sorted(set(after_base_near) - within_near)]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with CANDIDATE_PATH.open("w", encoding="utf-8", newline="\n") as stream:
        for item in eligible:
            stream.write(json.dumps(item, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")

    result = {
        "audit_id": "neuralchemy_original_attack_db_jb_train_candidate_round29_v1",
        "dataset_id": REPOSITORY,
        "revision": REVISION,
        "upstream_partition_read": "core/train only",
        "source_validation_opened": False,
        "source_test_opened": False,
        "pi_guard_test_opened": False,
        "payload_executed": False,
        "source_train_sha256": sha256_file(SHARD),
        "card_sha256": sha256_file(CARD),
        "comparison_package_id": BASE_ID,
        "comparison_manifest_sha256": sha256_bytes(manifest_bytes),
        "comparison_partitions_opened": ["train", "validation"],
        "component_row_counts": dict(sorted(component_counts.items())),
        "native_mapping_filter": {"source": "neuralchemy_v1", "category": "jailbreak", "label": "1", "augmented": False},
        "raw_candidate_rows": raw_counts["candidate_rows"],
        "normalized_unique_candidate_prompts": exact_unique,
        "candidate_exact_duplicates_collapsed": raw_counts["privacy_cleared_rows"] - exact_unique,
        "exact_overlap_with_comparison_train": exact_overlap_train,
        "exact_overlap_with_comparison_validation": exact_overlap_validation,
        "unique_candidates_with_exact_overlap_excluded": len(exact_overlap),
        "near_duplicates_against_comparison_train_validation_excluded": len(near_base),
        "within_source_near_duplicate_candidates_excluded": len(within_near),
        "configured_privacy_pattern_hits": dict(sorted(pii_counts.items())),
        "privacy_pattern_excluded_rows": raw_counts["privacy_pattern_excluded"],
        "eligible_unique_train_rows": len(eligible),
        "eligible_prompt_groups": len({item["prompt_group_sha256"] for item in eligible}),
        "candidate_file_sha256": sha256_file(CANDIDATE_PATH),
        "candidate_file_private_path": str(CANDIDATE_PATH),
        "observation_unit": "one prompt text field per original core/train record; augmented=false; category=jailbreak; non-jailbreak and multi_turn categories excluded",
        "label_policy": "provisional JB-attempt reference from publisher category=jailbreak; native binary malicious label alone is not used as JB",
        "rights_limit": "pinned dataset card declares Apache-2.0 and assigns Apache-2.0 to neuralchemy_v1 original attack_db; all row-level license fields are empty and upstream record authorship is not resolved",
        "lineage_limit": "pinned source component neuralchemy_v1 is distinct from HackAPrompt and other listed components; publisher does not provide further upstream lineage for its original attack_db",
        "privacy_limit": "configured email, SSN, phone-candidate, IPv4, credential, private-key, and bearer-token patterns only; no human privacy adjudication; attack prompts are sensitive by design",
        "source_family_policy": "one publisher-defined neuralchemy_v1 original-attack-db family; not represented as multiple independent families",
        "redistribution_allowed": False,
        "l3_run": False,
        "smoke_run": False,
        "prompt_text_emitted": False,
    }
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: result[key] for key in (
        "audit_id", "component_row_counts", "raw_candidate_rows", "normalized_unique_candidate_prompts",
        "candidate_exact_duplicates_collapsed", "exact_overlap_with_comparison_train",
        "exact_overlap_with_comparison_validation", "unique_candidates_with_exact_overlap_excluded",
        "near_duplicates_against_comparison_train_validation_excluded",
        "within_source_near_duplicate_candidates_excluded", "configured_privacy_pattern_hits",
        "eligible_unique_train_rows", "eligible_prompt_groups", "candidate_file_sha256",
        "source_validation_opened", "source_test_opened", "pi_guard_test_opened", "l3_run", "smoke_run",
    )}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
