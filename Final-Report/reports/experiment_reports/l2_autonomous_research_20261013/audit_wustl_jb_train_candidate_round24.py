"""Aggregate-only audit of the pinned WUSTL in-the-wild jailbreak corpus.

Reads the candidate corpus plus frozen L2 train/validation text for privacy and
duplicate checks. Emits aggregate counts only; never prints row text or IDs and
never opens PI-Guard test payloads.
"""
from __future__ import annotations

import collections
import hashlib
import json
import re
import unicodedata
from pathlib import Path

from openpyxl import load_workbook


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
PRIVATE = REPO / "workspaces" / "truongnv" / "pi_guard_pipeline"
SOURCE_DIR = PRIVATE / "training_bases" / "datasets" / "source_datasets" / "wustl_llm_jailbreak_usenix2024"
AUDIT_OUTPUT = PRIVATE / "training_bases" / "datasets" / "source_audit" / "wustl_round24"
ELIGIBLE_ROWS = AUDIT_OUTPUT / "eligible_train_candidates.jsonl"
PACKAGE = PRIVATE / "training_bases" / "datasets" / "project_training" / "versions" / "pi_guard_l2_source_diverse_round21_r05"
REPORT = ROOT / "wustl_jb_train_candidate_audit_round24.json"
EXPECTED_REVISION = "2a9e665769de1bbfa657b6e6a9f88d9d427bc57c"
EXPECTED_PACKAGE_ID = "pi_guard_l2_source_diverse_round21_r05"
SIMILARITY_PERCENT = 85

PII_PATTERNS = {
    "email": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "us_ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "phone_candidate": re.compile(r"(?<!\w)(?:\+?1[ .-]?)?(?:\(?\d{3}\)?[ .-]?)\d{3}[ .-]?\d{4}(?!\w)"),
    "ipv4": re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b"),
    "credential_assignment": re.compile(r"(?i)\b(?:api[_ -]?key|access[_ -]?token|password|passwd|secret)\s*[:=]\s*[^\s,;]+"),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def shingle_hashes(text: str) -> set[int]:
    words = re.findall(r"\w+", normalize(text))
    chunks = [" ".join(words)] if len(words) < 5 else (
        " ".join(words[pos : pos + 5]) for pos in range(len(words) - 4)
    )
    return {
        int.from_bytes(hashlib.blake2b(chunk.encode("utf-8"), digest_size=8).digest(), "big")
        for chunk in chunks
    }


def main() -> int:
    source_manifest_path = SOURCE_DIR / "source_manifest.json"
    source_manifest = json.loads(source_manifest_path.read_text(encoding="utf-8"))
    if source_manifest.get("pinned_revision") != EXPECTED_REVISION:
        raise ValueError("WUSTL_REVISION_MISMATCH")
    workbook_path = SOURCE_DIR / "JailbreakPrompts.xlsx"
    expected_file = next(item for item in source_manifest["files"] if item["path"] == workbook_path.name)
    workbook_hash = sha256(workbook_path)
    if workbook_hash != expected_file["sha256"]:
        raise ValueError("WUSTL_WORKBOOK_HASH_MISMATCH")

    dataset_manifest_path = PACKAGE / "DATASET_MANIFEST.json"
    dataset_manifest = json.loads(dataset_manifest_path.read_text(encoding="utf-8"))
    if dataset_manifest.get("package_id") != EXPECTED_PACKAGE_ID:
        raise ValueError("COMPARISON_PACKAGE_MISMATCH")

    prior_labels_by_text: dict[str, set[str]] = collections.defaultdict(set)
    prior_hashes_by_text: dict[str, set[int]] = {}
    prior_rows_by_split: collections.Counter[str] = collections.Counter()
    for split in ("train", "validation"):
        spec = dataset_manifest["partitions"][split]["rows"]
        path = PACKAGE / spec["path"]
        if sha256(path) != spec["sha256"]:
            raise ValueError(f"R05_{split.upper()}_HASH_MISMATCH")
        with path.open("r", encoding="utf-8") as stream:
            for line in stream:
                row = json.loads(line)
                text = row.get("text")
                if isinstance(text, str) and text.strip():
                    key = normalize(text)
                    prior_labels_by_text[key].add(str(row.get("label", "unknown")))
                    prior_hashes_by_text.setdefault(key, shingle_hashes(text))
                    prior_rows_by_split[split] += 1

    workbook = load_workbook(workbook_path, read_only=True, data_only=True)
    try:
        prompt_rows: list[tuple[str, str]] = []
        sheet_name = ""
        prompt_column = -1
        category_column = -1
        for sheet in workbook.worksheets:
            header = next(sheet.iter_rows(min_row=1, max_row=1, values_only=True), ())
            header_names = [str(value).strip().casefold() if value is not None else "" for value in header]
            if "prompt" in header_names:
                sheet_name = sheet.title
                prompt_column = header_names.index("prompt")
                category_column = header_names.index("category") if "category" in header_names else -1
                for cells in sheet.iter_rows(min_row=2, values_only=True):
                    value = cells[prompt_column] if prompt_column < len(cells) else None
                    if not isinstance(value, str) or not value.strip():
                        continue
                    category = str(cells[category_column]).strip() if category_column >= 0 and category_column < len(cells) and cells[category_column] is not None else "unspecified"
                    prompt_rows.append((value, category))
                break
        if prompt_column < 0:
            raise ValueError("WUSTL_PROMPT_COLUMN_NOT_FOUND")
    finally:
        workbook.close()

    normalized_counts = collections.Counter(normalize(text) for text, _ in prompt_rows)
    duplicate_keys = {key for key, count in normalized_counts.items() if count > 1}
    unique_rows: dict[str, str] = {}
    for text, category in prompt_rows:
        key = normalize(text)
        if key:
            unique_rows.setdefault(key, category)

    pii_by_key: dict[str, list[str]] = {}
    pii_counts: collections.Counter[str] = collections.Counter()
    for key in unique_rows:
        flags = [name for name, pattern in PII_PATTERNS.items() if pattern.search(key)]
        if flags:
            pii_by_key[key] = flags
            pii_counts.update(flags)

    exact_overlap_keys = set(unique_rows).intersection(prior_labels_by_text)
    exact_overlap_conflicts = sum(
        1 for key in exact_overlap_keys if any(label not in {"JB", "jailbreak", "2", "malicious"} for label in prior_labels_by_text[key])
    )

    clean_candidate_keys = [key for key in unique_rows if key not in pii_by_key and key not in exact_overlap_keys]
    candidate_hashes = {key: shingle_hashes(key) for key in clean_candidate_keys}
    candidate_buckets: dict[tuple[int, ...], list[str]] = collections.defaultdict(list)
    for key, hashes in candidate_hashes.items():
        sketch = sorted(hashes)[:12]
        for start in range(0, len(sketch) - 2, 3):
            candidate_buckets[(start // 3, *sketch[start : start + 3])].append(key)

    near_duplicate_keys: set[str] = set()
    for old_key, old_hashes in prior_hashes_by_text.items():
        sketch = sorted(old_hashes)[:12]
        possible = {
            key
            for start in range(0, len(sketch) - 2, 3)
            for key in candidate_buckets.get((start // 3, *sketch[start : start + 3]), ())
        }
        for key in possible:
            other_hashes = candidate_hashes[key]
            if (len(old_hashes) * 100 < SIMILARITY_PERCENT * len(other_hashes)
                    or len(other_hashes) * 100 < SIMILARITY_PERCENT * len(old_hashes)):
                continue
            common = len(old_hashes & other_hashes)
            if common * 100 >= SIMILARITY_PERCENT * (len(old_hashes) + len(other_hashes) - common):
                near_duplicate_keys.add(key)

    retained_keys = set(clean_candidate_keys) - near_duplicate_keys
    category_counts = collections.Counter(unique_rows[key] for key in retained_keys)
    text_by_key: dict[str, str] = {}
    for text, _ in prompt_rows:
        text_by_key.setdefault(normalize(text), text.strip())
    AUDIT_OUTPUT.mkdir(parents=True, exist_ok=True)
    eligible_records = [
        {
            "source_record_id": "src_" + hashlib.sha256((EXPECTED_REVISION + "\x1f" + key).encode("utf-8")).hexdigest()[:32],
            "normalized_text_sha256": hashlib.sha256(key.encode("utf-8")).hexdigest(),
            "category": unique_rows[key],
            "text": text_by_key[key],
        }
        for key in sorted(retained_keys)
    ]
    with ELIGIBLE_ROWS.open("w", encoding="utf-8", newline="\n") as stream:
        for record in eligible_records:
            stream.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    report = {
        "audit_id": "wustl_jb_train_candidate_audit_round24_v1",
        "source_repository_id": source_manifest["dataset_id"],
        "source_revision": EXPECTED_REVISION,
        "source_workbook_sha256": workbook_hash,
        "eligible_candidate_file_sha256": sha256(ELIGIBLE_ROWS),
        "eligible_candidate_file_private_path": str(ELIGIBLE_ROWS),
        "source_license_declared": source_manifest.get("declared_license"),
        "comparison_package_id": dataset_manifest["package_id"],
        "comparison_dataset_version": dataset_manifest.get("dataset_version"),
        "comparison_manifest_sha256": sha256(dataset_manifest_path),
        "comparison_partitions_opened": ["train", "validation"],
        "comparison_row_counts": dict(sorted(prior_rows_by_split.items())),
        "pi_guard_test_payload_opened": False,
        "upstream_test_payload_opened": False,
        "workbook_sheet_name": sheet_name,
        "candidate_observation_unit": "single-turn prompt collected from online sources, per publisher description",
        "candidate_label": "provisional_JB_attempt_reference_not_canonical_or_human_gold",
        "source_family_policy": "all retained rows remain one WUSTL collection family; upstream online-source ancestry is not row-addressable",
        "source_rows_nonempty": len(prompt_rows),
        "normalized_unique_candidate_prompts": len(unique_rows),
        "normalized_duplicate_groups": len(duplicate_keys),
        "duplicate_occurrences_after_first": sum(count - 1 for count in normalized_counts.values() if count > 1),
        "configured_privacy_indicator_counts": dict(sorted(pii_counts.items())),
        "unique_prompts_with_privacy_indicators": len(pii_by_key),
        "exact_overlap_with_r05_train_validation": len(exact_overlap_keys),
        "exact_overlap_label_conflict_count": exact_overlap_conflicts,
        "near_duplicate_prompts_ge_0_85_5word_shingle_jaccard": len(near_duplicate_keys),
        "eligible_after_configured_privacy_and_duplicate_filters": len(retained_keys),
        "retained_native_category_counts": dict(sorted(category_counts.items())),
        "provisional_family_count": 1 if retained_keys else 0,
        "rights_scope": "MIT repository declaration; author license does not independently resolve third-party online-post rights; private research only pending owner review",
        "privacy_limit": "configured regex screen is incomplete and is not human privacy clearance",
        "lineage_limit": "the collection is independent as a release but online upstream source ancestry is not row-addressable; shared community lineage with prior corpora remains possible",
        "split_role_recommendation": "if admitted, train-only as one family; hold family together in five-fold source-family OOF; never put this collection in both train and validation",
        "l3_run": False,
        "smoke_run": False,
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
