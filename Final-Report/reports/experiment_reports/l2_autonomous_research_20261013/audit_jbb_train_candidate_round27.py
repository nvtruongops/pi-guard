"""Aggregate-audit a pinned, non-JBC JailbreakBench train candidate.

Reads only the already-pinned attack-artifact files and frozen R05 train and
validation partitions. It never reads PI-Guard test data and never emits prompt
text or row identifiers to the report or console.
"""
from __future__ import annotations

import collections
import hashlib
import json
import re
import unicodedata
from pathlib import Path
from typing import Any, Iterator

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
PRIVATE = REPO / "workspaces" / "truongnv" / "pi_guard_pipeline"
DATASETS = PRIVATE / "training_bases" / "datasets"
SOURCE = DATASETS / "source_audit" / "jailbreakbench_artifacts_round17"
PACKAGE = DATASETS / "project_training" / "versions" / "pi_guard_l2_source_diverse_round21_r05"
OUTPUT_DIR = DATASETS / "source_audit" / "jailbreakbench_artifacts_round27"
CANDIDATE_PATH = OUTPUT_DIR / "eligible_train_candidates.jsonl"
REPORT = ROOT / "jbb_train_candidate_audit_round27.json"
REPOSITORY = "JailbreakBench/artifacts"
REVISION = "909e68c01d94222b8ad2e397a017e2e12e2adb73"
SIMILARITY_PERCENT = 85

PII_PATTERNS = {
    "email": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "us_ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "phone_candidate": re.compile(r"(?<!\w)(?:\+?1[ .-]?)?(?:\(?\d{3}\)?[ .-]?)\d{3}[ .-]?\d{4}(?!\w)"),
    "ipv4": re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b"),
    "credential_assignment": re.compile(r"(?i)\b(?:api[_ -]?key|access[_ -]?token|password|passwd|secret)\s*[:=]\s*[^\s,;]+"),
}


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize(value: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def prompt_records(value: Any) -> Iterator[dict[str, Any]]:
    if isinstance(value, dict):
        if isinstance(value.get("prompt"), str):
            yield value
        for key, child in value.items():
            if key != "prompt":
                yield from prompt_records(child)
    elif isinstance(value, list):
        for child in value:
            yield from prompt_records(child)


def shingle_hashes(text: str) -> set[int]:
    words = re.findall(r"\w+", normalize(text))
    chunks = [" ".join(words)] if len(words) < 5 else (
        " ".join(words[pos:pos + 5]) for pos in range(len(words) - 4)
    )
    return {
        int.from_bytes(hashlib.blake2b(chunk.encode("utf-8"), digest_size=8).digest(), "big")
        for chunk in chunks
    }


def bucket_keys(hashes: set[int]) -> Iterator[tuple[int, ...]]:
    sketch = sorted(hashes)[:12]
    for start in range(0, len(sketch) - 2, 3):
        yield (start // 3, *sketch[start:start + 3])


def near_jaccard(left: set[int], right: set[int]) -> bool:
    if len(left) * 100 < SIMILARITY_PERCENT * len(right) or len(right) * 100 < SIMILARITY_PERCENT * len(left):
        return False
    common = len(left & right)
    return common * 100 >= SIMILARITY_PERCENT * (len(left) + len(right) - common)


def near_candidate_keys(candidate_hashes: dict[str, set[int]], prior_hashes: dict[str, set[int]]) -> set[str]:
    buckets: dict[tuple[int, ...], set[str]] = collections.defaultdict(set)
    for key, hashes in candidate_hashes.items():
        for bucket in bucket_keys(hashes):
            buckets[bucket].add(key)
    found: set[str] = set()
    for old_hashes in prior_hashes.values():
        possible = {key for bucket in bucket_keys(old_hashes) for key in buckets.get(bucket, ())}
        for key in possible:
            if near_jaccard(old_hashes, candidate_hashes[key]):
                found.add(key)
    return found


def candidate_near_pairs(candidate_hashes: dict[str, set[int]]) -> set[str]:
    buckets: dict[tuple[int, ...], set[str]] = collections.defaultdict(set)
    for key, hashes in candidate_hashes.items():
        for bucket in bucket_keys(hashes):
            buckets[bucket].add(key)
    excluded: set[str] = set()
    checked: set[tuple[str, str]] = set()
    for key, hashes in candidate_hashes.items():
        possible = {other for bucket in bucket_keys(hashes) for other in buckets.get(bucket, ()) if other != key}
        for other in possible:
            pair = tuple(sorted((key, other)))
            if pair in checked:
                continue
            checked.add(pair)
            if near_jaccard(hashes, candidate_hashes[other]):
                excluded.update(pair)
    return excluded


def read_jsonl(path: Path) -> Iterator[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as stream:
        for line in stream:
            yield json.loads(line)


def main() -> int:
    aggregate = json.loads((SOURCE / "aggregate_audit.json").read_text(encoding="utf-8"))
    if aggregate.get("repository") != REPOSITORY or aggregate.get("revision") != REVISION:
        raise ValueError("JBB_PINNED_SOURCE_IDENTITY_MISMATCH")
    package_manifest_path = PACKAGE / "DATASET_MANIFEST.json"
    package_manifest_raw = package_manifest_path.read_bytes()
    package_manifest = json.loads(package_manifest_raw)
    if package_manifest.get("package_id") != "pi_guard_l2_source_diverse_round21_r05":
        raise ValueError("R05_PACKAGE_IDENTITY_MISMATCH")

    prior_texts: dict[str, set[int]] = {}
    prior_by_part: dict[str, set[str]] = {"train": set(), "validation": set()}
    jbb_validation_rows = 0
    for part in ("train", "validation"):
        row_ref = package_manifest["partitions"][part]["rows"]
        prov_ref = package_manifest["partitions"][part]["provenance"]
        row_path, prov_path = PACKAGE / row_ref["path"], PACKAGE / prov_ref["path"]
        if sha256_file(row_path) != row_ref["sha256"] or sha256_file(prov_path) != prov_ref["sha256"]:
            raise ValueError("R05_PARTITION_HASH_MISMATCH:" + part)
        rows, provenance = list(read_jsonl(row_path)), list(read_jsonl(prov_path))
        if len(rows) != len(provenance):
            raise ValueError("R05_ROW_PROVENANCE_ALIGNMENT:" + part)
        for row, source_row in zip(rows, provenance):
            if row.get("id") != source_row.get("id"):
                raise ValueError("R05_ROW_PROVENANCE_ID_MISMATCH:" + part)
            if part == "validation" and source_row.get("source_repository_id") == REPOSITORY:
                jbb_validation_rows += 1
                continue
            key = normalize(str(row.get("text", "")))
            if key:
                prior_by_part[part].add(key)
                prior_texts.setdefault(key, set()).add(int.from_bytes(hashlib.sha256(key.encode("utf-8")).digest()[:8], "big"))
    if jbb_validation_rows != 100:
        raise ValueError("R05_JBB_VALIDATION_ROWS_NOT_100")

    prompt_rows: dict[str, dict[str, Any]] = {}
    method_occurrences: collections.Counter[str] = collections.Counter()
    method_files: collections.Counter[str] = collections.Counter()
    missing_behavior_occurrences: collections.Counter[str] = collections.Counter()
    behavior_methods: dict[str, set[str]] = collections.defaultdict(set)
    behavior_occurrences: collections.Counter[str] = collections.Counter()
    pii_counts: collections.Counter[str] = collections.Counter()
    pii_keys: set[str] = set()
    prompt_occurrences = 0
    jbc_occurrences = 0

    file_manifest = aggregate.get("file_manifest", [])
    if len(file_manifest) != aggregate.get("source_files_selected"):
        raise ValueError("JBB_FILE_MANIFEST_COUNT_MISMATCH")
    for file_entry in sorted(file_manifest, key=lambda item: item["path"]):
        relative = Path(file_entry["path"])
        path = (SOURCE / relative).resolve()
        if not path.is_relative_to(SOURCE.resolve()) or "test-artifact" in {part.casefold() for part in relative.parts} or relative.name.casefold() == "evaluation.json":
            raise ValueError("JBB_FORBIDDEN_ARTIFACT_PATH")
        raw = path.read_bytes()
        if sha256_file(path) != file_entry["sha256"] or len(raw) != file_entry["size"]:
            raise ValueError("JBB_ARTIFACT_HASH_OR_SIZE_MISMATCH")
        method = relative.parts[1]
        model = relative.stem
        method_files[method] += 1
        if method == "JBC":
            for _ in prompt_records(json.loads(raw)):
                jbc_occurrences += 1
            continue
        payload = json.loads(raw)
        for index, record in enumerate(prompt_records(payload)):
            prompt_occurrences += 1
            method_occurrences[method] += 1
            text = record["prompt"].strip()
            key = normalize(text)
            if not key:
                continue
            ancestry = record.get("goal", record.get("behavior"))
            if isinstance(ancestry, str) and ancestry.strip():
                behavior_hash = sha256_bytes(normalize(ancestry).encode("utf-8"))
                behavior_methods[behavior_hash].add(method)
                behavior_occurrences[behavior_hash] += 1
            else:
                behavior_hash = ""
                missing_behavior_occurrences[method] += 1
            entry = prompt_rows.setdefault(key, {
                "text": text,
                "behavior_hashes": set(),
                "source_record_ids": [],
                "methods": set(),
                "models": set(),
            })
            if behavior_hash:
                entry["behavior_hashes"].add(behavior_hash)
            entry["source_record_ids"].append(sha256_bytes((REVISION + "\x1f" + relative.as_posix() + "\x1f" + str(index)).encode("utf-8")))
            entry["methods"].add(method)
            entry["models"].add(model)
            flags = [name for name, pattern in PII_PATTERNS.items() if pattern.search(text)]
            if flags:
                pii_keys.add(key)
                pii_counts.update(flags)

    exact_overlap = {
        "train": len(set(prompt_rows).intersection(prior_by_part["train"])),
        "validation_after_jbb_removal": len(set(prompt_rows).intersection(prior_by_part["validation"])),
    }
    candidate_keys = set(prompt_rows) - pii_keys
    missing_behavior_keys = {key for key, value in prompt_rows.items() if not value["behavior_hashes"]}
    ambiguous_behavior_keys = {key for key, value in prompt_rows.items() if len(value["behavior_hashes"]) > 1}
    candidate_keys -= missing_behavior_keys | ambiguous_behavior_keys
    exact_overlap_keys = set(prompt_rows).intersection(prior_by_part["train"] | prior_by_part["validation"])
    candidate_keys -= exact_overlap_keys

    prior_hashes = {key: shingle_hashes(key) for key in prior_texts}
    candidate_hashes = {key: shingle_hashes(key) for key in candidate_keys}
    near_base = near_candidate_keys(candidate_hashes, prior_hashes)
    after_base = {key: value for key, value in candidate_hashes.items() if key not in near_base}
    near_within_source = candidate_near_pairs(after_base)
    retained_keys = sorted(set(after_base) - near_within_source)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    records = []
    retained_by_method: collections.Counter[str] = collections.Counter()
    for key in retained_keys:
        item = prompt_rows[key]
        behavior_hash = next(iter(item["behavior_hashes"]))
        source_record_id = "src_jbb_" + min(item["source_record_ids"])[:32]
        methods = sorted(item["methods"])
        retained_by_method.update(methods)
        records.append({
            "source_record_id": source_record_id,
            "normalized_text_sha256": sha256_bytes(key.encode("utf-8")),
            "behavior_ancestry_sha256": behavior_hash,
            "methods": methods,
            "models": sorted(item["models"]),
            "text": item["text"],
        })
    with CANDIDATE_PATH.open("w", encoding="utf-8", newline="\n") as stream:
        for record in records:
            stream.write(json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")

    result = {
        "audit_id": "jbb_non_jbc_train_candidate_round27_v1",
        "source_repository_id": REPOSITORY,
        "source_revision": REVISION,
        "source_file_count": len(file_manifest),
        "source_file_manifest_sha256": sha256_bytes(json.dumps(file_manifest, sort_keys=True, separators=(",", ":")).encode("utf-8")),
        "comparison_package_id": package_manifest["package_id"],
        "comparison_manifest_sha256": sha256_bytes(package_manifest_raw),
        "comparison_partitions_opened": ["train", "validation"],
        "jbb_validation_rows_to_remove_from_both_packages": jbb_validation_rows,
        "method_occurrences_non_jbc": dict(sorted(method_occurrences.items())),
        "method_occurrences_excluded_jbc": jbc_occurrences,
        "method_file_counts": dict(sorted(method_files.items())),
        "normalized_unique_non_jbc_prompts": len(prompt_rows),
        "exact_overlap_with_r05_train_and_clean_validation": exact_overlap,
        "privacy_indicator_counts": dict(sorted(pii_counts.items())),
        "unique_prompts_with_privacy_indicators": len(pii_keys),
        "behavior_ancestry_groups": len(behavior_methods),
        "behavior_groups_spanning_multiple_methods": sum(len(methods) > 1 for methods in behavior_methods.values()),
        "behavior_ancestry_missing_occurrences": dict(sorted(missing_behavior_occurrences.items())),
        "unique_prompts_without_behavior_ancestry": len(missing_behavior_keys),
        "unique_prompts_with_ambiguous_behavior_ancestry": len(ambiguous_behavior_keys),
        "exact_duplicate_prompts_collapsed": prompt_occurrences - len(prompt_rows),
        "near_duplicates_against_r05_clean_train_validation": len(near_base),
        "near_duplicate_candidates_within_jbb": len(near_within_source),
        "eligible_unique_train_rows": len(records),
        "eligible_train_rows_by_method_attribution": dict(sorted(retained_by_method.items())),
        "eligible_behavior_groups": len({r["behavior_ancestry_sha256"] for r in records}),
        "eligible_candidate_file_sha256": sha256_file(CANDIDATE_PATH),
        "eligible_candidate_file_private_path": str(CANDIDATE_PATH),
        "observation_unit": "single prompt field from a pinned attack artifact; attempt-level provisional JB reference inferred from benchmark intent",
        "source_family_policy": "all retained methods and models stay in one JailbreakBench artifacts family; method variants are not independent families",
        "attack_success_used_as_label": False,
        "rights_scope": "private_local_research_nonredistributive_only; per-artifact ownership and upstream rights remain unresolved",
        "lineage_limit": "pinned artifact files and behavior ancestry are recorded; artifact authorship and any upstream source ancestry are not independently row-verified",
        "privacy_limit": "configured regex screen only; no human privacy adjudication and no claim of complete PII clearance",
        "redistribution_allowed": False,
        "test_payload_opened": False,
        "l3_run": False,
        "smoke_run": False,
    }
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: result[key] for key in (
        "audit_id", "source_file_count", "jbb_validation_rows_to_remove_from_both_packages",
        "method_occurrences_non_jbc", "normalized_unique_non_jbc_prompts",
        "exact_overlap_with_r05_train_and_clean_validation", "privacy_indicator_counts",
        "behavior_ancestry_groups", "behavior_groups_spanning_multiple_methods",
        "unique_prompts_without_behavior_ancestry", "unique_prompts_with_ambiguous_behavior_ancestry",
        "near_duplicates_against_r05_clean_train_validation", "near_duplicate_candidates_within_jbb",
        "eligible_unique_train_rows", "eligible_behavior_groups", "eligible_candidate_file_sha256",
        "test_payload_opened", "l3_run", "smoke_run",
    )}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
