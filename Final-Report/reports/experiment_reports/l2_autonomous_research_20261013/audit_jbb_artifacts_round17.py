"""Acquire and aggregate-audit non-test JailbreakBench artifacts at a pinned commit.

Never fetches paths below test-artifact or evaluation.json, never reads the
PI-Guard test contract, and never prints/writes prompt text or row-level IDs.
The collected payload is private and is not admitted to an L2 package here.
"""
from __future__ import annotations

import collections
import hashlib
import json
import re
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
PRIVATE = REPO / "workspaces" / "truongnv" / "pi_guard_pipeline"
ROUND07 = PRIVATE / "training_bases" / "datasets" / "project_training" / "versions" / "pi_guard_native_reference_round07_20261013_r01"
SOURCE_DIR = PRIVATE / "training_bases" / "datasets" / "source_audit" / "jailbreakbench_artifacts_round17"
REPORT = ROOT / "jbb_artifact_audit_round17.json"
REPOSITORY = "JailbreakBench/artifacts"
REVISION = "909e68c01d94222b8ad2e397a017e2e12e2adb73"
TREE_API = f"https://api.github.com/repos/{REPOSITORY}/git/trees/{REVISION}?recursive=1"
RAW_BASE = f"https://raw.githubusercontent.com/{REPOSITORY}/{REVISION}/"

PII_PATTERNS = {
    "email": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "us_ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "phone_candidate": re.compile(r"(?<!\w)(?:\+?1[ .-]?)?(?:\(?\d{3}\)?[ .-]?)\d{3}[ .-]?\d{4}(?!\w)"),
    "ipv4": re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b"),
    "credential_assignment": re.compile(r"(?i)\b(?:api[_ -]?key|access[_ -]?token|password|passwd|secret)\s*[:=]\s*[^\s,;]+"),
}


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def get_json(url: str) -> Any:
    request = urllib.request.Request(url, headers={"User-Agent": "Codex-L2-Research"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read())


def get_bytes(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "Codex-L2-Research"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def normalized(value: str) -> str:
    return " ".join(value.casefold().split())


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


def main() -> int:
    tree = get_json(TREE_API)
    if tree.get("sha") != REVISION:
        raise ValueError("JBB_REVISION_RESPONSE_MISMATCH")

    files = []
    for entry in tree.get("tree", []):
        path = entry.get("path", "")
        if (entry.get("type") != "blob" or not path.startswith("attack-artifacts/")
                or not path.endswith(".json")
                or re.search(r"(^|/)test-artifact(/|$)", path, re.I)
                or path.rsplit("/", 1)[-1].casefold() == "evaluation.json"):
            continue
        files.append({"path": path, "git_blob_sha": entry["sha"], "size": entry.get("size", 0)})

    if not files:
        raise ValueError("NO_NON_TEST_ARTIFACT_FILES_SELECTED")
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    file_summaries = []
    all_text_keys: collections.Counter[str] = collections.Counter()
    behavior_keys: set[str] = set()
    method_rows: collections.Counter[str] = collections.Counter()
    model_rows: collections.Counter[str] = collections.Counter()
    outcome_rows: collections.Counter[str] = collections.Counter()
    pii_rows: collections.Counter[str] = collections.Counter()
    total_prompts = 0

    for entry in sorted(files, key=lambda item: item["path"]):
        raw = get_bytes(RAW_BASE + entry["path"])
        if len(raw) != entry["size"]:
            raise ValueError("JBB_FILE_SIZE_MISMATCH:" + entry["path"])
        destination = SOURCE_DIR / entry["path"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(raw)
        try:
            value = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError("JBB_INVALID_JSON:" + entry["path"]) from exc

        method = entry["path"].split("/")[1]
        model = entry["path"].rsplit("/", 1)[-1].removesuffix(".json")
        prompts = []
        for record in prompt_records(value):
            text = record["prompt"]
            key = normalized(text)
            if not key:
                continue
            prompts.append(key)
            all_text_keys[key] += 1
            method_rows[method] += 1
            model_rows[model] += 1
            total_prompts += 1
            for name, pattern in PII_PATTERNS.items():
                if pattern.search(text):
                    pii_rows[name] += 1
            outcome = record.get("jailbroken")
            outcome_rows["true" if outcome is True else "false" if outcome is False else "missing_or_other"] += 1
            ancestry = record.get("goal", record.get("behavior"))
            if isinstance(ancestry, str) and ancestry.strip():
                behavior_keys.add(sha256_bytes(normalized(ancestry).encode("utf-8")))
            elif record.get("index") is not None:
                behavior_keys.add(sha256_bytes((method + "\x1f" + str(record["index"])).encode("utf-8")))

        file_summaries.append({
            "path": entry["path"],
            "git_blob_sha": entry["git_blob_sha"],
            "size": len(raw),
            "sha256": sha256_bytes(raw),
            "prompt_rows": len(prompts),
            "normalized_unique_prompts": len(set(prompts)),
            "top_level_type": type(value).__name__,
            "top_level_keys": sorted(value) if isinstance(value, dict) else [],
        })

    package_manifest = json.loads((ROUND07 / "DATASET_MANIFEST.json").read_text(encoding="utf-8"))
    if package_manifest.get("package_id") != "pi_guard_l2_native_reference_round07_r01":
        raise ValueError("UNEXPECTED_ROUND07_PACKAGE")
    package_texts: set[str] = set()
    partitions = package_manifest["partitions"]
    for split in ("train", "validation"):
        spec = partitions[split]["rows"]
        path = ROUND07 / spec["path"]
        if sha256_bytes(path.read_bytes()) != spec["sha256"]:
            raise ValueError("ROUND07_" + split.upper() + "_HASH_MISMATCH")
        with path.open("r", encoding="utf-8") as stream:
            for line in stream:
                row = json.loads(line)
                key = normalized(row.get("text", ""))
                if key:
                    package_texts.add(key)

    duplicate_groups = sum(1 for count in all_text_keys.values() if count > 1)
    duplicate_records = sum(count - 1 for count in all_text_keys.values() if count > 1)
    overlap_records = sum(count for key, count in all_text_keys.items() if key in package_texts)
    result = {
        "audit_round": 17,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "repository": REPOSITORY,
        "revision": REVISION,
        "tree_api": TREE_API,
        "selection_policy": "attack-artifacts JSON only; exclude any test-artifact path and every evaluation.json; prompt field only for candidate inputs",
        "source_files_selected": len(files),
        "source_bytes_selected": sum(entry["size"] for entry in files),
        "source_files_not_selected": {
            "test_artifact_file_count": sum(1 for entry in tree.get("tree", []) if re.search(r"(^|/)test-artifact(/|$)", entry.get("path", ""), re.I)),
            "evaluation_json_file_count": sum(1 for entry in tree.get("tree", []) if entry.get("path", "").casefold().endswith("/evaluation.json")),
        },
        "prompt_rows": total_prompts,
        "normalized_unique_prompt_rows": len(all_text_keys),
        "within_source_normalized_duplicate_groups": duplicate_groups,
        "within_source_duplicate_rows_after_first": duplicate_records,
        "exact_overlap_with_round07_train_validation_rows": overlap_records,
        "round07_package_id": package_manifest["package_id"],
        "round07_opened_partitions": ["train", "validation"],
        "round07_test_opened": False,
        "prompt_rows_by_method": dict(sorted(method_rows.items())),
        "prompt_rows_by_model": dict(sorted(model_rows.items())),
        "jailbroken_outcome_counts_not_used_as_input_label": dict(sorted(outcome_rows.items())),
        "distinct_behavior_ancestry_keys": len(behavior_keys),
        "prompt_privacy_indicator_rows": dict(sorted(pii_rows.items())),
        "file_manifest": file_summaries,
        "mapping_status": "conditional JB-attempt reference mapping only; no canonical label or package admission",
        "limitations": [
            "JBB is an attack-artifact benchmark, not an in-the-wild collection; method/model variants are not independent collection families.",
            "Attack success is not used to decide whether a prompt is a JB attempt; all candidate artifact prompts require a documented attempt-level mapping.",
            "Exact duplicate and regex screens are not near-duplicate adjudication or comprehensive privacy review.",
            "Shared benchmark behavior ancestry may cross methods; group ancestry before any split.",
        ],
        "test_payload_opened": False,
        "l3_run": False,
        "smoke_run": False,
    }
    SOURCE_DIR.joinpath("aggregate_audit.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    REPORT.write_text(json.dumps({key: value for key, value in result.items() if key != "file_manifest"},
                                 ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: result[key] for key in (
        "source_files_selected", "source_bytes_selected", "source_files_not_selected",
        "prompt_rows", "normalized_unique_prompt_rows", "within_source_normalized_duplicate_groups",
        "within_source_duplicate_rows_after_first", "exact_overlap_with_round07_train_validation_rows",
        "prompt_rows_by_method", "prompt_rows_by_model", "jailbroken_outcome_counts_not_used_as_input_label",
        "distinct_behavior_ancestry_keys", "prompt_privacy_indicator_rows", "test_payload_opened",
    )}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
