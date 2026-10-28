"""Aggregate-only screen for the pinned Dolly 15k train split.

The script never prints or writes prompt text, row identifiers, or per-row
hashes. It reads only Dolly's train file and the round07 train/validation
rows; it never opens any test partition.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
import unicodedata
from pathlib import Path
from typing import Any, Iterable


PII_PATTERNS = {
    "email": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "us_ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "phone_candidate": re.compile(r"(?<!\w)(?:\+?1[ .-]?)?(?:\(?\d{3}\)?[ .-]?)\d{3}[ .-]?\d{4}(?!\w)"),
}

REVIEW_PATTERNS = {
    "instruction_override": re.compile(
        r"\b(ignore|disregard|forget|override|bypass)\b.{0,80}\b(instructions?|rules?|system|developer|policy)\b",
        re.I | re.S,
    ),
    "secret_extraction": re.compile(
        r"\b(reveal|show|print|repeat|extract|disclose)\b.{0,80}\b(system prompt|hidden prompt|secret|api key|password)\b",
        re.I | re.S,
    ),
    "harmful_intent_terms": re.compile(
        r"\b(make a bomb|build a weapon|steal credentials|write malware|kill someone|self[- ]harm)\b",
        re.I,
    ),
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def rows(path: Path) -> Iterable[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, start=1):
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"INVALID_JSONL:{path.name}:{line_number}") from exc
            if not isinstance(value, dict):
                raise ValueError(f"ROW_NOT_OBJECT:{path.name}:{line_number}")
            yield value


def normalize(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def text_field(row: dict[str, Any], names: tuple[str, ...]) -> str:
    for name in names:
        value = row.get(name)
        if isinstance(value, str):
            return value
    return ""


def add_field_scan(summary: dict[str, Any], field: str, value: str) -> None:
    if not value:
        return
    summary["field_chars"][field] += len(value)
    for pattern_name, pattern in PII_PATTERNS.items():
        if pattern.search(value):
            summary["pii_indicator_rows"][field][pattern_name] += 1
    for pattern_name, pattern in REVIEW_PATTERNS.items():
        if pattern.search(value):
            summary["review_flag_rows"][field][pattern_name] += 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-jsonl", type=Path, required=True)
    parser.add_argument("--source-revision", required=True)
    parser.add_argument("--source-sha256", required=True)
    parser.add_argument("--comparison-package", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    args = parser.parse_args()

    source_path = args.source_jsonl.resolve(strict=True)
    package_root = args.comparison_package.resolve(strict=True)
    output_path = args.output_json.resolve()
    source_sha = sha256_file(source_path)
    if source_sha.casefold() != args.source_sha256.casefold():
        raise ValueError("SOURCE_FILE_SHA256_MISMATCH")

    manifest_path = package_root / "DATASET_MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("package_id") != "pi_guard_l2_native_reference_round07_r01":
        raise ValueError("UNEXPECTED_COMPARISON_PACKAGE")

    normalized_source: collections.Counter[str] = collections.Counter()
    category_counts: collections.Counter[str] = collections.Counter()
    candidate_records: list[tuple[str, str, bool, bool, bool]] = []
    summary: dict[str, Any] = {
        "source_revision": args.source_revision,
        "source_file_sha256": source_sha,
        "source_file_bytes": source_path.stat().st_size,
        "dataset_rows": 0,
        "category_counts": category_counts,
        "rows_with_context": 0,
        "empty_instruction_rows": 0,
        "normalized_instruction_duplicate_rows": 0,
        "normalized_instruction_duplicate_groups": 0,
        "exact_overlap_with_round07_train_validation_rows": 0,
        "round07_package_id": manifest["package_id"],
        "round07_manifest_sha256": sha256_file(manifest_path),
        "round07_opened_partitions": ["train", "validation"],
        "round07_test_opened": False,
        "field_chars": collections.Counter(),
        "pii_indicator_rows": collections.defaultdict(collections.Counter),
        "review_flag_rows": collections.defaultdict(collections.Counter),
        "notes": [
            "Indicators are conservative audit leads, not privacy clearance or canonical labels.",
            "Only instruction text is considered as a possible L2 input; context and response are never model inputs here.",
            "Category names are authoring categories, not independent source families.",
        ],
    }

    for row in rows(source_path):
        summary["dataset_rows"] += 1
        instruction = text_field(row, ("instruction",))
        context = text_field(row, ("context",))
        response = text_field(row, ("response",))
        category = text_field(row, ("category",)) or "<missing>"
        category_counts[category] += 1
        if context.strip():
            summary["rows_with_context"] += 1
        if not instruction.strip():
            summary["empty_instruction_rows"] += 1
        key = normalize(instruction)
        if key:
            normalized_source[key] += 1
        instruction_pii = any(pattern.search(instruction) for pattern in PII_PATTERNS.values())
        instruction_review = any(pattern.search(instruction) for pattern in REVIEW_PATTERNS.values())
        candidate_records.append((key, category, bool(context.strip()), instruction_pii, instruction_review))
        add_field_scan(summary, "instruction", instruction)
        add_field_scan(summary, "context", context)
        add_field_scan(summary, "response", response)

    duplicate_groups = {key for key, count in normalized_source.items() if count > 1}
    summary["normalized_instruction_duplicate_groups"] = len(duplicate_groups)
    summary["normalized_instruction_duplicate_rows"] = sum(
        normalized_source[key] - 1 for key in duplicate_groups
    )

    package_texts: set[str] = set()
    partitions = manifest["partitions"]
    for split_name in ("train", "validation"):
        relative_path = partitions[split_name]["rows"]["path"]
        path = package_root / relative_path
        if sha256_file(path) != partitions[split_name]["rows"]["sha256"]:
            raise ValueError(f"ROUND07_{split_name.upper()}_SHA256_MISMATCH")
        for row in rows(path):
            value = text_field(row, ("text", "prompt", "instruction", "input"))
            key = normalize(value)
            if key:
                package_texts.add(key)
    summary["exact_overlap_with_round07_train_validation_rows"] = sum(
        count for key, count in normalized_source.items() if key in package_texts
    )
    eligible_unique: set[str] = set()
    excluded = collections.Counter()
    for key, _category, has_context, has_pii, has_review_flag in candidate_records:
        if not key:
            excluded["empty_instruction"] += 1
        elif has_context:
            excluded["nonempty_context_not_standalone_input"] += 1
        elif has_pii:
            excluded["instruction_pii_indicator"] += 1
        elif has_review_flag:
            excluded["instruction_content_review_flag"] += 1
        elif key in package_texts:
            excluded["exact_overlap_with_round07_train_validation"] += 1
        elif key in eligible_unique:
            excluded["duplicate_instruction_after_first"] += 1
        else:
            eligible_unique.add(key)
    summary["provisional_instruction_only_eligible_rows"] = len(eligible_unique)
    summary["provisional_excluded_rows_by_primary_reason"] = dict(sorted(excluded.items()))
    summary["provisional_mapping_status"] = "not_canonical; requires explicit reference-label mapping and review"
    summary["category_counts"] = dict(sorted(category_counts.items()))
    summary["field_chars"] = dict(sorted(summary["field_chars"].items()))
    summary["pii_indicator_rows"] = {
        field: dict(sorted(counts.items())) for field, counts in sorted(summary["pii_indicator_rows"].items())
    }
    summary["review_flag_rows"] = {
        field: dict(sorted(counts.items())) for field, counts in sorted(summary["review_flag_rows"].items())
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "report": str(output_path),
        "source_rows": summary["dataset_rows"],
        "source_sha256": source_sha,
        "category_counts": summary["category_counts"],
        "rows_with_context": summary["rows_with_context"],
        "exact_duplicate_groups": summary["normalized_instruction_duplicate_groups"],
        "exact_overlap_with_round07_train_validation": summary["exact_overlap_with_round07_train_validation_rows"],
        "provisional_instruction_only_eligible_rows": summary["provisional_instruction_only_eligible_rows"],
        "provisional_excluded_rows_by_primary_reason": summary["provisional_excluded_rows_by_primary_reason"],
        "pii_indicator_rows": summary["pii_indicator_rows"],
        "review_flag_rows": summary["review_flag_rows"],
        "test_opened": False,
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
