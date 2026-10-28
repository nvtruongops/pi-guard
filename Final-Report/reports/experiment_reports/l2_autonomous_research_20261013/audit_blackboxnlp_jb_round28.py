"""Aggregate-audit the pinned BlackboxNLP jailbreak-attempt dataset."""
from __future__ import annotations

import collections
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
PRIVATE = REPO / "workspaces" / "truongnv" / "pi_guard_pipeline"
DATASETS = PRIVATE / "training_bases" / "datasets"
SOURCE = DATASETS / "source_datasets" / "jailbreak_features_blackboxnlp2025"
PACKAGE = DATASETS / "project_training" / "versions" / "pi_guard_l2_jbb_round27_baseline_20261014"
OUTPUT_DIR = DATASETS / "source_audit" / "blackboxnlp_jb_round28"
CANDIDATE_PATH = OUTPUT_DIR / "eligible_train_candidates.jsonl"
REPORT = ROOT / "blackboxnlp_jb_candidate_audit_round28.json"
REPOSITORY = "sevdeawesome/jailbreak_success"
PAPER_REPOSITORY = "NLie2/what_features_jailbreak_LLMs"
SIMILARITY_PERCENT = 85


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("HELPER_IMPORT_FAILED:" + name)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


DEDUP = load_module("l2_blackboxnlp_round28_dedup", ROOT / "audit_jbb_train_candidate_round27.py")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as stream:
        for line in stream:
            yield json.loads(line)


def main() -> int:
    source_manifest = json.loads((SOURCE / "source_manifest.json").read_text(encoding="utf-8"))
    if source_manifest.get("dataset_id") != REPOSITORY:
        raise ValueError("BLACKBOXNLP_DATASET_ID_MISMATCH")
    source_file = SOURCE / "latest.csv"
    file_entry = next((x for x in source_manifest.get("files", []) if x.get("path") == "latest.csv"), None)
    if not file_entry or sha256_file(source_file) != file_entry.get("sha256"):
        raise ValueError("BLACKBOXNLP_PINNED_FILE_HASH_MISMATCH")
    manifest_path = PACKAGE / "DATASET_MANIFEST.json"
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes)
    if manifest.get("package_id") != "pi_guard_l2_jbb_round27_baseline_20261014":
        raise ValueError("R27_CLEAN_BASELINE_IDENTITY_MISMATCH")

    prior_texts: dict[str, set[int]] = {}
    prior_by_part: dict[str, set[str]] = {"train": set(), "validation": set()}
    for part in ("train", "validation"):
        row_ref = manifest["partitions"][part]["rows"]
        prov_ref = manifest["partitions"][part]["provenance"]
        row_path, prov_path = PACKAGE / row_ref["path"], PACKAGE / prov_ref["path"]
        if sha256_file(row_path) != row_ref["sha256"] or sha256_file(prov_path) != prov_ref["sha256"]:
            raise ValueError("R27_CLEAN_BASELINE_PARTITION_HASH_MISMATCH:" + part)
        rows, provenance = list(read_jsonl(row_path)), list(read_jsonl(prov_path))
        if len(rows) != len(provenance):
            raise ValueError("R27_CLEAN_BASELINE_ALIGNMENT_FAILURE:" + part)
        for row, source_row in zip(rows, provenance):
            if row.get("id") != source_row.get("id"):
                raise ValueError("R27_CLEAN_BASELINE_ID_ALIGNMENT_FAILURE:" + part)
            key = DEDUP.normalize(str(row.get("text", "")))
            if key:
                prior_by_part[part].add(key)
                prior_texts.setdefault(key, set())

    prompts: dict[str, dict[str, Any]] = {}
    method_occurrences: collections.Counter[str] = collections.Counter()
    base_ids_by_prompt: dict[str, set[str]] = collections.defaultdict(set)
    raw_rows = 0
    missing_fields = collections.Counter()
    privacy_keys: set[str] = set()
    privacy_counts: collections.Counter[str] = collections.Counter()
    with source_file.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if set(reader.fieldnames or ()) != {"prompt_name", "jailbreak_prompt_name", "jailbreak_prompt_text", "original_prompt_text"}:
            raise ValueError("BLACKBOXNLP_SOURCE_COLUMNS_MISMATCH")
        for index, row in enumerate(reader):
            raw_rows += 1
            base_name = row.get("prompt_name", "").strip()
            method = row.get("jailbreak_prompt_name", "").strip()
            text = row.get("jailbreak_prompt_text", "").strip()
            if not base_name:
                missing_fields["prompt_name"] += 1
                continue
            if not method:
                missing_fields["jailbreak_prompt_name"] += 1
                continue
            if not text:
                missing_fields["jailbreak_prompt_text"] += 1
                continue
            key = DEDUP.normalize(text)
            if not key:
                continue
            method_occurrences[method] += 1
            base_hash = sha256_bytes(base_name.encode("utf-8"))
            base_ids_by_prompt[key].add(base_hash)
            item = prompts.setdefault(key, {"text": text, "base_hashes": set(), "methods": set(), "record_ids": []})
            item["base_hashes"].add(base_hash)
            item["methods"].add(method)
            item["record_ids"].append(sha256_bytes((source_manifest["pinned_revision"] + "\x1f" + str(index) + "\x1f" + base_hash + "\x1f" + method).encode("utf-8")))
            for name, pattern in DEDUP.PII_PATTERNS.items():
                if pattern.search(text):
                    privacy_counts[name] += 1
                    privacy_keys.add(key)
    if raw_rows != source_manifest.get("audit_counts", {}).get("input_rows"):
        raise ValueError("BLACKBOXNLP_SOURCE_ROW_COUNT_MISMATCH")

    candidate_keys = set(prompts)
    missing_base_keys = {key for key, value in prompts.items() if not value["base_hashes"]}
    ambiguous_base_keys = {key for key, value in prompts.items() if len(value["base_hashes"]) > 1}
    exact_overlap = {
        "train": len(candidate_keys & prior_by_part["train"]),
        "validation": len(candidate_keys & prior_by_part["validation"]),
    }
    exact_overlap_keys = candidate_keys & (prior_by_part["train"] | prior_by_part["validation"])
    candidate_keys -= privacy_keys | ambiguous_base_keys | missing_base_keys | exact_overlap_keys

    prior_hashes = {key: DEDUP.shingle_hashes(key) for key in prior_texts}
    candidate_hashes = {key: DEDUP.shingle_hashes(key) for key in candidate_keys}
    near_base = DEDUP.near_candidate_keys(candidate_hashes, prior_hashes)
    candidate_hashes = {key: value for key, value in candidate_hashes.items() if key not in near_base}
    near_within_source = DEDUP.candidate_near_pairs(candidate_hashes)
    retained_keys = sorted(set(candidate_hashes) - near_within_source)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    records = []
    retained_methods: collections.Counter[str] = collections.Counter()
    for key in retained_keys:
        item = prompts[key]
        base_hash = next(iter(item["base_hashes"]))
        methods = sorted(item["methods"])
        retained_methods.update(methods)
        records.append({
            "source_record_id": "src_blackboxnlp_" + min(item["record_ids"])[:32],
            "normalized_text_sha256": sha256_bytes(key.encode("utf-8")),
            "base_prompt_sha256": base_hash,
            "methods": methods,
            "text": item["text"],
        })
    with CANDIDATE_PATH.open("w", encoding="utf-8", newline="\n") as stream:
        for record in records:
            stream.write(json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")

    result = {
        "audit_id": "blackboxnlp_jailbreak_attempt_train_candidate_round28_v1",
        "source_repository_id": REPOSITORY,
        "source_revision": source_manifest["pinned_revision"],
        "paper_repository_id": PAPER_REPOSITORY,
        "paper_repository_revision": source_manifest.get("paper_repository_revision"),
        "paper": source_manifest.get("paper", {}),
        "declared_license": source_manifest.get("declared_license"),
        "license_limit": source_manifest.get("license_note"),
        "comparison_package_id": manifest["package_id"],
        "comparison_manifest_sha256": sha256_bytes(manifest_bytes),
        "comparison_partitions_opened": ["train", "validation"],
        "source_file_sha256": file_entry["sha256"],
        "input_rows": raw_rows,
        "distinct_base_prompt_groups": len({next(iter(x["base_hashes"])) for x in prompts.values() if x["base_hashes"]}),
        "distinct_attack_methods": len(method_occurrences),
        "occurrences_by_method": dict(sorted(method_occurrences.items())),
        "normalized_unique_attack_prompts": len(prompts),
        "exact_duplicate_rows_collapsed": raw_rows - len(prompts),
        "exact_duplicate_prompt_keys_with_multiple_base_groups": len(ambiguous_base_keys),
        "missing_required_fields": dict(sorted(missing_fields.items())),
        "exact_overlap_with_clean_r05_train_validation": exact_overlap,
        "unique_prompts_with_privacy_indicators": len(privacy_keys),
        "privacy_indicator_counts": dict(sorted(privacy_counts.items())),
        "near_duplicates_against_clean_r05_train_validation": len(near_base),
        "near_duplicate_candidates_within_source": len(near_within_source),
        "eligible_unique_train_rows": len(records),
        "eligible_base_prompt_groups": len({r["base_prompt_sha256"] for r in records}),
        "eligible_rows_by_method_attribution": dict(sorted(retained_methods.items())),
        "candidate_file_sha256": sha256_file(CANDIDATE_PATH),
        "candidate_file_private_path": str(CANDIDATE_PATH),
        "observation_unit": "one final attack-transformed prompt field; each retained item is one textual input reference",
        "label_policy": "provisional JB-attempt reference from attack intent; target-model success is not used as label",
        "lineage_limit": "paper identifies 300 harmful seed prompts from Jiang et al. 2024 and 35 attack algorithms; MIT card does not resolve upstream seed/algorithm rights or prompt-level authorship",
        "privacy_limit": "configured regex screen only; no human privacy adjudication and no complete PII clearance",
        "source_family_policy": "all retained records are one BlackboxNLP benchmark family; the 35 methods and 300 prompt groups are not independent collection sources",
        "redistribution_allowed": False,
        "test_payload_opened": False,
        "l3_run": False,
        "smoke_run": False,
    }
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: result[key] for key in (
        "audit_id", "input_rows", "distinct_base_prompt_groups", "distinct_attack_methods",
        "normalized_unique_attack_prompts", "exact_duplicate_rows_collapsed",
        "exact_duplicate_prompt_keys_with_multiple_base_groups", "exact_overlap_with_clean_r05_train_validation",
        "unique_prompts_with_privacy_indicators", "privacy_indicator_counts",
        "near_duplicates_against_clean_r05_train_validation", "near_duplicate_candidates_within_source",
        "eligible_unique_train_rows", "eligible_base_prompt_groups", "candidate_file_sha256",
        "test_payload_opened", "l3_run", "smoke_run",
    )}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
