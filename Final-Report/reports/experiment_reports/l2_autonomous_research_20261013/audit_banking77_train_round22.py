"""Aggregate-only qualification audit for the pinned BANKING77 train split.

Only the publisher's train.csv is read. The publisher test split and PI-Guard
test payload are never opened. Row text and row identifiers are not emitted.
"""
from __future__ import annotations

import collections
import csv
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
PRIVATE = REPO / "workspaces" / "truongnv" / "pi_guard_pipeline"
TRAINING = PRIVATE / "training_bases"
SOURCE_FILE = TRAINING / "datasets" / "source_audit" / "banking77_round22" / "train.csv"
FROZEN_PACKAGE = TRAINING / "datasets" / "project_training" / "versions" / "pi_guard_l2_source_diverse_round21_r02"
REPORT = ROOT / "banking77_train_candidate_audit_round22.json"

REPOSITORY = "PolyAI-LDN/task-specific-datasets"
REVISION = "57ec275d8078af65b7731c2a98be812d844a6d6b"
UPSTREAM_FILE = "banking_data/train.csv"
SOURCE_FILE_SHA256 = "b06e26ac675513959a63135f11b94ea7786ed02da65db93a5650d8838cbc664b"
FROZEN_PACKAGE_ID = "pi_guard_l2_source_diverse_round21_r02"
FROZEN_PACKAGE_MANIFEST_SHA256 = "c8d5e827b28e1ea18f413ecb19e9246df5f59029c5319390dcd76af78719c7ca"
SIMILARITY_PERCENT = 85


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("HELPER_IMPORT_FAILED:" + name)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


CLINC = load_module("banking77_privacy_helpers", ROOT / "audit_clinc_oos_train_round19.py")
TOXIC = load_module("banking77_duplicate_helpers", ROOT / "audit_toxic_chat_train_round21.py")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_frozen_texts() -> tuple[dict[str, set[str]], str]:
    raw_manifest = (FROZEN_PACKAGE / "DATASET_MANIFEST.json").read_bytes()
    manifest_hash = hashlib.sha256(raw_manifest).hexdigest()
    manifest = json.loads(raw_manifest)
    if manifest.get("package_id") != FROZEN_PACKAGE_ID or manifest_hash != FROZEN_PACKAGE_MANIFEST_SHA256:
        raise ValueError("FROZEN_PACKAGE_ID_OR_MANIFEST_HASH_MISMATCH")

    labels_by_text: dict[str, set[str]] = collections.defaultdict(set)
    for partition in ("train", "validation"):
        spec = manifest["partitions"][partition]
        for kind in ("rows", "provenance"):
            path = FROZEN_PACKAGE / spec[kind]["path"]
            if sha256_file(path) != spec[kind]["sha256"]:
                raise ValueError("FROZEN_PARTITION_HASH_MISMATCH:" + partition + ":" + kind)
        path = FROZEN_PACKAGE / spec["rows"]["path"]
        with path.open("r", encoding="utf-8") as stream:
            for line in stream:
                row = json.loads(line)
                text = TOXIC.normalize(str(row.get("text", "")))
                if text:
                    labels_by_text[text].add(str(row.get("label", "unknown")))
    return dict(labels_by_text), manifest_hash


def read_source_rows() -> list[tuple[int, str, str]]:
    if sha256_file(SOURCE_FILE) != SOURCE_FILE_SHA256:
        raise ValueError("PINNED_BANKING77_TRAIN_HASH_MISMATCH")
    with SOURCE_FILE.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != ["text", "category"]:
            raise ValueError("UNEXPECTED_BANKING77_TRAIN_SCHEMA")
        rows = []
        for ordinal, row in enumerate(reader):
            text = row.get("text")
            category = row.get("category")
            if not isinstance(text, str) or not isinstance(category, str):
                rows.append((ordinal, "", ""))
            else:
                rows.append((ordinal, text, category))
        return rows


def run_audit() -> tuple[dict, list[tuple[str, str, int, str]]]:
    frozen, frozen_manifest_sha = load_frozen_texts()
    identifier = CLINC.language_identifier()
    source_rows = read_source_rows()
    counters: collections.Counter[str] = collections.Counter()
    pii_counts: collections.Counter[str] = collections.Counter()
    review_counts: collections.Counter[str] = collections.Counter()
    language_counts: collections.Counter[str] = collections.Counter()
    confidence_bins: collections.Counter[str] = collections.Counter()
    category_counts: collections.Counter[str] = collections.Counter()
    seen_exact: set[str] = set()
    candidates: list[tuple[str, str, int, str]] = []
    exact_cross_labels: collections.Counter[str] = collections.Counter()

    counters["publisher_train_rows"] = len(source_rows)
    for ordinal, text, category in source_rows:
        if not text.strip() or not category.strip():
            counters["empty_or_invalid"] += 1
            continue
        key = TOXIC.normalize(text)
        if not key:
            counters["empty_after_normalization"] += 1
            continue
        pii = [name for name, pattern in CLINC.PII_PATTERNS.items() if pattern.search(text)]
        if pii:
            counters["privacy_pattern_excluded"] += 1
            pii_counts.update(pii)
            continue
        review = [name for name, pattern in CLINC.REVIEW_PATTERNS.items() if pattern.search(text)]
        if review:
            counters["attack_or_harm_pattern_excluded"] += 1
            review_counts.update(review)
            continue
        language, confidence = identifier.classify(text)
        confidence = float(confidence)
        language_counts[language] += 1
        confidence_bins[">=0.95" if confidence >= 0.95 else ">=0.50" if confidence >= 0.50 else "<0.50"] += 1
        if language != "en":
            counters["non_english_top1"] += 1
            continue
        if key in seen_exact:
            counters["within_source_exact_duplicate"] += 1
            continue
        seen_exact.add(key)
        if key in frozen:
            counters["exact_overlap_with_frozen_train_or_validation"] += 1
            for label in frozen[key]:
                exact_cross_labels[label] += 1
            continue
        candidates.append((key, category, ordinal, text.strip()))

    # Deduplicate the candidate source with the same 5-word-shingle/Jaccard
    # protocol used by the adjacent Round 21 candidate audit.
    retained: list[tuple[str, str, int, str]] = []
    retained_hashes: list[set[int]] = []
    candidate_index: dict[tuple[int, int, int, int], list[int]] = collections.defaultdict(list)
    for key, category, ordinal, raw_text in candidates:
        hashes = TOXIC.shingle_hashes(key)
        possible = {
            index
            for bucket in TOXIC.bucket_keys(hashes)
            for index in candidate_index.get(bucket, ())
        }
        if any(TOXIC.similar(hashes, retained_hashes[index]) for index in possible):
            counters["within_source_near_duplicate_at_0_85"] += 1
            continue
        index = len(retained)
        retained.append((key, category, ordinal, raw_text))
        retained_hashes.append(hashes)
        for bucket in TOXIC.bucket_keys(hashes):
            candidate_index[bucket].append(index)

    frozen_near_matches: set[int] = set()
    for partition in ("train", "validation"):
        manifest = json.loads((FROZEN_PACKAGE / "DATASET_MANIFEST.json").read_text(encoding="utf-8"))
        path = FROZEN_PACKAGE / manifest["partitions"][partition]["rows"]["path"]
        with path.open("r", encoding="utf-8") as stream:
            for line in stream:
                row = json.loads(line)
                text = TOXIC.normalize(str(row.get("text", "")))
                if not text:
                    continue
                frozen_hashes = TOXIC.shingle_hashes(text)
                possible = {
                    index
                    for bucket in TOXIC.bucket_keys(frozen_hashes)
                    for index in candidate_index.get(bucket, ())
                }
                for index in possible:
                    if TOXIC.similar(frozen_hashes, retained_hashes[index]):
                        frozen_near_matches.add(index)
    counters["near_overlap_with_frozen_train_or_validation_at_0_85"] = len(frozen_near_matches)
    kept = [item for index, item in enumerate(retained) if index not in frozen_near_matches]
    for _, category, _ordinal, _raw_text in kept:
        category_counts[category] += 1
    counters["eligible_after_exact_and_near_duplicate_gates"] = len(kept)

    report = {
        "schema": "pi_guard_source_candidate_audit_v1",
        "source": {
            "repository": REPOSITORY,
            "revision": REVISION,
            "file": UPSTREAM_FILE,
            "sha256": SOURCE_FILE_SHA256,
            "upstream_split_read": "train only",
            "publisher_license": "CC BY 4.0",
            "language_scope": "English per publisher card and paper; local language top-1 check",
            "source_unit": "single-turn online banking customer-service query",
            "source_family_count": 1,
            "reference_mapping": "non-OOS customer-service intent query -> provisional benign reference; not curator gold",
        },
        "audit": {
            "counts": dict(sorted(counters.items())),
            "native_category_count_after_all_gates": len(category_counts),
            "eligible_category_counts": dict(sorted(category_counts.items())),
            "language_counts_after_privacy_and_attack_screen": dict(sorted(language_counts.items())),
            "language_confidence_bins": dict(sorted(confidence_bins.items())),
            "privacy_pattern_counts": dict(sorted(pii_counts.items())),
            "attack_or_harm_pattern_counts": dict(sorted(review_counts.items())),
            "exact_overlap_frozen_label_counts": dict(sorted(exact_cross_labels.items())),
            "duplicate_method": "NFKC/casefold/whitespace exact; 5-word shingle Jaccard >=0.85, bucket candidates",
            "privacy_status": "screened_only; regex screening does not establish absence of PII",
            "human_adjudication": "not performed",
            "row_text_or_ids_emitted": False,
            "publisher_test_split_opened": False,
            "pi_guard_test_payload_opened": False,
            "l3_or_smoke_run": False,
            "automatic_preview_exposure": "publisher repository card exposed a few illustrative training queries; none copied or used in audit or package",
        },
        "frozen_comparator": {
            "package_id": FROZEN_PACKAGE_ID,
            "manifest_sha256": frozen_manifest_sha,
            "train_validation_only": True,
        },
        "disposition": "conditional_benign_train_family; eligible rows may be tested in a new isolated L2 package, subject to privacy and label limitations",
    }
    return report, kept


def main() -> int:
    report, kept = run_audit()
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({
        "report": str(REPORT),
        "source_train_rows": report["audit"]["counts"]["publisher_train_rows"],
        "eligible_rows": len(kept),
        "pii_excluded": report["audit"]["counts"].get("privacy_pattern_excluded", 0),
        "exact_overlaps": report["audit"]["counts"].get("exact_overlap_with_frozen_train_or_validation", 0),
        "near_overlaps": report["audit"]["counts"].get("near_overlap_with_frozen_train_or_validation_at_0_85", 0),
        "test_opened": False,
        "l3_or_smoke_run": False,
    }, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
