"""Build an isolated L2 package with independent train and validation sources.

New train roles: CLINC OOS in-scope English assistant queries (benign reference)
and Anthropic HH-RLHF single-human-turn red-team attempts (provisional JB
attempt reference). New held-out validation role: ToxicChat human-annotated
jailbreak positives. Only its pinned upstream train file is read, and only the
user_input/jailbreaking columns are projected. No final-test payload is opened.
"""
from __future__ import annotations

import collections
import gzip
import hashlib
import importlib.util
import json
import shutil
import sys
import unicodedata
from pathlib import Path
from typing import Any

import pyarrow.csv as pacsv
import pyarrow.parquet as pq


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
PRIVATE = REPO / "workspaces" / "truongnv" / "pi_guard_pipeline"
TRAINING = PRIVATE / "training_bases"
VERSIONS = TRAINING / "datasets" / "project_training" / "versions"
BASE_PACKAGE = VERSIONS / "pi_guard_l2_source_heldout_round18_r01"
DO_NOT_REDISTRIBUTE_COMPARATOR = VERSIONS / "pi_guard_l2_source_heldout_dolly_aug_round18_r01"
SOURCE_AUDIT = TRAINING / "datasets" / "source_audit"
CLINC_FILE = SOURCE_AUDIT / "clinc_oos_round19" / "plus_train.parquet"
ANTHROPIC_FILE = SOURCE_AUDIT / "anthropic_hh_rlhf_round19" / "red_team_attempts.jsonl.gz"
TOXIC_CHAT_FILE = SOURCE_AUDIT / "toxic_chat_round21" / "data" / "1123" / "toxic-chat_annotation_train.csv"
VENDOR = TRAINING / "datasets" / "project_training" / "history" / "pi_guard_v8_english_diagnostic_20261012" / "tools" / "_vendor"
PROTOCOL_SOURCE = ROOT / "AUTONOMOUS_PROTOCOL.json"
OUTPUT_PACKAGE_ID = "pi_guard_l2_source_diverse_round21_r02"
OUTPUT_VERSION = "0.8.3-source-diverse-l2-reference"
OUTPUT_PACKAGE = VERSIONS / OUTPUT_PACKAGE_ID
REPORT = ROOT / "l2_source_heldout_package_build_round21_r02.json"

CLINC_REPO = "clinc/clinc_oos"
CLINC_REVISION = "155b9c710419136e17307b80d0a13e68cd46b4ec"
CLINC_SHA256 = "30188119cf9f86fc9db27e1c22442d091cb5cb0913c9496f945fe11e7a02a28f"
ANTHROPIC_REPO = "Anthropic/hh-rlhf"
ANTHROPIC_REVISION = "09be8c5bbc57cb3887f3a9732ad6aa7ec602a1fa"
ANTHROPIC_SHA256 = "4c7b0069991460f0064f279fd400b51f3f0095697d14d7793c49b0925f80814f"
TOXIC_CHAT_REPO = "lmsys/toxic-chat"
TOXIC_CHAT_REVISION = "b913fa0c27522a8f0f7d12220c126e39dbbf8173"
TOXIC_CHAT_SHA256 = "0099077aa4c7183040b11d44d2e6852c293ee2fd78a0ffe47ee12b4d1ecd727e"
LANGUAGE_MODEL_SHA256 = "f4f4a2c3465ca1f081541037f9cac23021d68151c2f709c55ae5eedfca522963"
SIMILARITY_PERCENT = 85
LABEL_IDS = {"benign": 0, "PI": 1, "JB": 2}


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("RESEARCH_HELPER_LOAD_FAILED:" + name)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


R18 = load_module("l2_round18_builder_helpers", ROOT / "build_l2_source_heldout_round18.py")
CLINC_AUDIT = load_module("l2_clinc_round19_helpers", ROOT / "audit_clinc_oos_train_round19.py")
ANTHROPIC_AUDIT = load_module("l2_anthropic_round19_helpers", ROOT / "audit_anthropic_redteam_round19.py")
TOXIC_CHAT_AUDIT = load_module("l2_toxic_chat_round21_helpers", ROOT / "audit_toxic_chat_train_round21.py")
SPLIT_HELPERS = load_module("l2_split_v5_helpers", REPO / "Final-Report" / "scripts" / "split_v5_dataset.py")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def read_jsonl(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def load_base_package() -> tuple[dict, dict, dict, dict, list[dict], list[dict], list[dict], list[dict]]:
    manifest = json.loads((BASE_PACKAGE / "DATASET_MANIFEST.json").read_text(encoding="utf-8"))
    split = json.loads((BASE_PACKAGE / "split_manifest.json").read_text(encoding="utf-8"))
    review = json.loads((BASE_PACKAGE / "source_review.json").read_text(encoding="utf-8"))
    mapping = json.loads((BASE_PACKAGE / "label_mapping.json").read_text(encoding="utf-8"))
    train_rows = read_jsonl(BASE_PACKAGE / "corpus" / "rows" / "train.jsonl")
    train_prov = read_jsonl(BASE_PACKAGE / "corpus" / "provenance" / "train.jsonl")
    val_rows = read_jsonl(BASE_PACKAGE / "corpus" / "rows" / "validation.jsonl")
    val_prov = read_jsonl(BASE_PACKAGE / "corpus" / "provenance" / "validation.jsonl")
    if manifest.get("package_id") != "pi_guard_l2_source_heldout_round18_r01":
        raise ValueError("UNEXPECTED_ROUND18_BASE_PACKAGE")
    for part, rows, provenance in (("train", train_rows, train_prov), ("validation", val_rows, val_prov)):
        if len(rows) != len(provenance) or len(rows) != len(split["partitions"][part]):
            raise ValueError("ROUND18_PARTITION_ALIGNMENT_MISMATCH:" + part)
        spec = manifest["partitions"][part]
        for kind in ("rows", "provenance"):
            path = BASE_PACKAGE / spec[kind]["path"]
            if sha256_file(path) != spec[kind]["sha256"]:
                raise ValueError("ROUND18_PARTITION_HASH_MISMATCH:" + part + ":" + kind)
    return manifest, split, review, mapping, train_rows, train_prov, val_rows, val_prov


def base_text_labels(train_rows: list[dict], val_rows: list[dict]) -> dict[str, set[str]]:
    result: dict[str, set[str]] = collections.defaultdict(set)
    for row in train_rows + val_rows:
        key = normalize(row["text"])
        if key:
            result[key].add(row["label"])
    return dict(result)


def make_candidate(source_key: str, repo: str, revision: str, upstream_split: str,
                   record_seed: str, family_id: str, lineage_id: str, native_label: str,
                   rule: str, label: str, text: str, ordinal: int) -> dict:
    normalized = normalize(text)
    return {
        "source_key": source_key,
        "repository": repo,
        "revision": revision,
        "upstream_split": upstream_split,
        "source_record_id": "src_" + sha256_bytes(
            "\x1f".join((repo, revision, upstream_split, record_seed, normalized)).encode("utf-8")
        )[:32],
        "source_family_id": family_id,
        "collection_lineage_id": lineage_id,
        "native_label": native_label,
        "rule": rule,
        "label": label,
        "text": text.strip(),
        "normalized": normalized,
        "ordinal": ordinal,
        "partition": "validation" if source_key == "toxic_chat" else "train",
    }


def candidates_clinc(existing: set[str]) -> tuple[list[dict], dict]:
    if sha256_file(CLINC_FILE) != CLINC_SHA256:
        raise ValueError("PINNED_CLINC_TRAIN_HASH_MISMATCH")
    schema = pq.read_schema(CLINC_FILE)
    feature_meta = json.loads(schema.metadata[b"huggingface"])["info"]["features"]
    class_names = feature_meta["intent"]["names"]
    oos_ids = {index for index, name in enumerate(class_names) if name.casefold() == "oos"}
    if len(class_names) != 151 or len(oos_ids) != 1 or not {"text", "intent"}.issubset(set(schema.names)):
        raise ValueError("UNEXPECTED_CLINC_TRAIN_SCHEMA")
    oos_id = next(iter(oos_ids))
    table = pq.read_table(CLINC_FILE, columns=["text", "intent"])
    identifier = CLINC_AUDIT.language_identifier()
    rows: list[dict] = []
    counters: collections.Counter[str] = collections.Counter()
    seen: set[str] = set()
    privacy: collections.Counter[str] = collections.Counter()
    review: collections.Counter[str] = collections.Counter()
    family_id = "sf_clinc_oos_plus_train_round21"
    lineage_id = "cl_clinc_oos_" + CLINC_REVISION[:12]
    for ordinal, item in enumerate(table.to_pylist()):
        counters["source_train_rows"] += 1
        intent_id = int(item["intent"])
        if intent_id == oos_id:
            counters["native_oos_excluded"] += 1
            continue
        text = item["text"]
        if not isinstance(text, str) or not text.strip():
            counters["empty_or_invalid"] += 1
            continue
        matches = [name for name, pattern in CLINC_AUDIT.PII_PATTERNS.items() if pattern.search(text)]
        if matches:
            counters["privacy_pattern_excluded"] += 1
            privacy.update(matches)
            continue
        matched_review = [name for name, pattern in CLINC_AUDIT.REVIEW_PATTERNS.items() if pattern.search(text)]
        if matched_review:
            counters["attack_or_harm_pattern_excluded"] += 1
            review.update(matched_review)
            continue
        language, _confidence = identifier.classify(text)
        if language != "en":
            counters["non_english_top1"] += 1
            continue
        key = normalize(text)
        if key in existing:
            counters["exact_overlap_frozen_or_prior_comparator"] += 1
            continue
        if key in seen:
            counters["within_source_exact_duplicate"] += 1
            continue
        seen.add(key)
        rows.append(make_candidate(
            "clinc", CLINC_REPO, CLINC_REVISION, "plus/train", f"row_{ordinal}",
            family_id, lineage_id, "in-scope assistant intent (non-OOS)",
            "clinc_plus_train_in_scope_intent_to_provisional_benign_r21", "benign", text, ordinal,
        ))
    counters["unique_pre_near_duplicate_candidates"] = len(rows)
    return rows, {"counters": dict(sorted(counters.items())),
                  "privacy_pattern_counts": dict(sorted(privacy.items())),
                  "attack_or_harm_pattern_counts": dict(sorted(review.items()))}


def candidates_anthropic(existing: set[str]) -> tuple[list[dict], dict]:
    if sha256_file(ANTHROPIC_FILE) != ANTHROPIC_SHA256:
        raise ValueError("PINNED_ANTHROPIC_SOURCE_HASH_MISMATCH")
    identifier = ANTHROPIC_AUDIT.language_identifier()
    counters: collections.Counter[str] = collections.Counter()
    duplicates: collections.Counter[str] = collections.Counter()
    members: dict[str, set[str]] = collections.defaultdict(set)
    texts: dict[str, str] = {}
    ordinals: dict[str, int] = {}
    with gzip.open(ANTHROPIC_FILE, "rt", encoding="utf-8") as stream:
        rows = json.load(stream)
    for ordinal, item in enumerate(rows):
        counters["source_rows"] += 1
        transcript = item.get("transcript")
        if not isinstance(transcript, str):
            counters["missing_transcript"] += 1
            continue
        turns = ANTHROPIC_AUDIT.human_turns(transcript)
        if len(turns) != 1:
            counters["not_single_human_turn"] += 1
            continue
        text = turns[0]
        if not text.strip():
            counters["empty_prompt"] += 1
            continue
        if any(pattern.search(text) for pattern in ANTHROPIC_AUDIT.PII_PATTERNS.values()):
            counters["privacy_pattern_excluded"] += 1
            continue
        language, confidence = identifier.classify(text)
        if language != "en" or float(confidence) < ANTHROPIC_AUDIT.LANGUAGE_THRESHOLD:
            counters["non_english_or_uncertain"] += 1
            continue
        key = normalize(text)
        # Match round19 exactly: duplicate counts include English rows without
        # participant IDs, so a prompt cannot become unique by dropping its
        # ambiguous duplicate before the family check.
        duplicates[key] += 1
        if key in existing:
            counters["exact_overlap_frozen"] += 1
            continue
        member = item.get("red_team_member_id")
        if member is None or not str(member).strip():
            counters["missing_participant_family"] += 1
            continue
        members[key].add(str(member))
        texts.setdefault(key, text)
        ordinals.setdefault(key, ordinal)
    candidates: list[dict] = []
    family_id = "sf_anthropic_hh_redteam_2022_round21"
    lineage_id = "cl_anthropic_hh_rlhf_" + ANTHROPIC_REVISION[:12]
    for key, count in duplicates.items():
        if count != 1 or len(members[key]) != 1:
            counters["within_source_exact_duplicate_or_cross_member_group"] += count
            continue
        ordinal = ordinals[key]
        candidates.append(make_candidate(
            "anthropic", ANTHROPIC_REPO, ANTHROPIC_REVISION,
            "red-team-attempts/red_team_attempts.jsonl.gz", f"source_row_{ordinal}",
            family_id, lineage_id, "human red-team attempt to elicit harmful output in a one-human-turn transcript",
            "anthropic_single_human_turn_red_team_attempt_to_provisional_jb_attempt_r21",
            "JB", texts[key], ordinal,
        ))
    counters["unique_pre_near_duplicate_candidates"] = len(candidates)
    # Never use transcript ratings as input labels; do not retain source actor IDs.
    return candidates, {"counters": dict(sorted(counters.items())),
                        "collection_family_count": 1,
                        "participant_ids_stored": False,
                        "rating_used_as_label": False}


def candidates_toxic_chat(existing: set[str]) -> tuple[list[dict], dict]:
    if sha256_file(TOXIC_CHAT_FILE) != TOXIC_CHAT_SHA256:
        raise ValueError("PINNED_TOXIC_CHAT_TRAIN_HASH_MISMATCH")
    reader = pacsv.open_csv(
        TOXIC_CHAT_FILE,
        parse_options=pacsv.ParseOptions(newlines_in_values=True),
        convert_options=pacsv.ConvertOptions(
            include_columns=["user_input", "jailbreaking"], strings_can_be_null=True,
        ),
    )
    if set(reader.schema.names) != {"user_input", "jailbreaking"}:
        raise ValueError("UNEXPECTED_TOXIC_CHAT_PROJECTED_SCHEMA")
    identifier = TOXIC_CHAT_AUDIT.language_identifier()
    candidates: list[dict] = []
    counters: collections.Counter[str] = collections.Counter()
    seen: set[str] = set()
    family_id = "sf_lmsys_toxic_chat_1123_round21"
    lineage_id = "cl_lmsys_toxic_chat_" + TOXIC_CHAT_REVISION[:12]
    for batch in reader:
        for item in batch.to_pylist():
            ordinal = counters["source_train_rows"]
            counters["source_train_rows"] += 1
            label = str(item.get("jailbreaking") or "").strip().casefold()
            if label not in {"1", "true"}:
                counters["not_native_jailbreaking_positive"] += 1
                continue
            counters["native_jailbreaking_positive"] += 1
            text = item.get("user_input")
            if not isinstance(text, str) or not text.strip():
                counters["positive_empty_or_invalid"] += 1
                continue
            if any(pattern.search(text) for pattern in TOXIC_CHAT_AUDIT.PII_PATTERNS.values()):
                counters["positive_privacy_pattern_excluded"] += 1
                continue
            language, confidence = identifier.classify(text)
            if language != "en" or float(confidence) < TOXIC_CHAT_AUDIT.LANGUAGE_THRESHOLD:
                counters["positive_not_english_or_uncertain"] += 1
                continue
            counters["positive_english_confident_after_privacy"] += 1
            key = normalize(text)
            if key in existing:
                counters["exact_overlap_frozen"] += 1
                continue
            if key in seen:
                counters["within_source_exact_duplicate"] += 1
                continue
            seen.add(key)
            candidates.append(make_candidate(
                "toxic_chat", TOXIC_CHAT_REPO, TOXIC_CHAT_REVISION,
                "data/1123/toxic-chat_annotation_train.csv", f"train_row_{ordinal}",
                family_id, lineage_id, "jailbreaking=1", 
                "toxic_chat_native_jailbreaking_true_to_provisional_jb_attempt_r21",
                "JB", text, ordinal,
            ))
    counters["unique_pre_near_duplicate_candidates"] = len(candidates)
    return candidates, {"counters": dict(sorted(counters.items())),
                        "projected_columns": ["user_input", "jailbreaking"],
                        "model_output_accessed": False,
                        "upstream_test_accessed": False,
                        "collection_family_count": 1}


def candidate_text_hashes(candidates: list[dict]) -> tuple[list[set[int]], dict[tuple[int, ...], list[int]]]:
    hashes_by_index: list[set[int]] = []
    buckets: dict[tuple[int, ...], list[int]] = collections.defaultdict(list)
    for index, candidate in enumerate(candidates):
        hashes = SPLIT_HELPERS.shingle_hashes(candidate["text"])
        hashes_by_index.append(hashes)
        sketch = sorted(hashes)[:12]
        for start in range(0, len(sketch) - 2, 3):
            key = (start // 3, *sketch[start:start + 3])
            buckets[key].append(index)
    return hashes_by_index, dict(buckets)


def near_duplicate_against_frozen(candidates: list[dict], package: Path) -> set[int]:
    candidate_hashes, candidate_buckets = candidate_text_hashes(candidates)
    matched: set[int] = set()
    for split in ("train", "validation"):
        rows_path = package / "corpus" / "rows" / f"{split}.jsonl"
        with rows_path.open("r", encoding="utf-8") as stream:
            for line in stream:
                old_text = json.loads(line).get("text", "")
                if not isinstance(old_text, str) or not old_text.strip():
                    continue
                hashes = SPLIT_HELPERS.shingle_hashes(old_text)
                sketch = sorted(hashes)[:12]
                possible = {
                    candidate_index
                    for start in range(0, len(sketch) - 2, 3)
                    for candidate_index in candidate_buckets.get((start // 3, *sketch[start:start + 3]), ())
                }
                for candidate_index in possible:
                    other = candidate_hashes[candidate_index]
                    if (len(hashes) * 100 >= SIMILARITY_PERCENT * len(other)
                            and len(other) * 100 >= SIMILARITY_PERCENT * len(hashes)):
                        common = len(hashes & other)
                        if common * 100 >= SIMILARITY_PERCENT * (len(hashes) + len(other) - common):
                            matched.add(candidate_index)
    return matched


def source_review_entry(package: Path, source_key: str) -> dict:
    info = {
        "clinc": {
            "repository": CLINC_REPO, "revision": CLINC_REVISION,
            "family": "sf_clinc_oos_plus_train_round21", "license": "CC-BY-3.0",
            "locator": "https://huggingface.co/datasets/clinc/clinc_oos",
            "rights": "CC-BY-3.0 declared by the publisher; attribution retained. Local private, non-commercial research only; no package redistribution.",
            "lineage": f"Pinned plus/train parquet only; SHA-256 {CLINC_SHA256}; validation/test files were not requested or opened.",
            "privacy": "Configured PII and attack/harm intent patterns, English top-1 filter, exact/85%-near duplicate screening against frozen train/validation and new candidates.",
            "residual": "Native in-scope intent is only a provisional benign reference; regex privacy/intent screens are incomplete and are not safety adjudication.",
        },
        "anthropic": {
            "repository": ANTHROPIC_REPO, "revision": ANTHROPIC_REVISION,
            "family": "sf_anthropic_hh_redteam_2022_round21", "license": "MIT",
            "locator": "https://github.com/anthropics/hh-rlhf",
            "rights": "MIT license declared by the publisher; attribution and notice retained. This private L2 research package is not redistributed.",
            "lineage": f"Pinned red-team-attempts file only; SHA-256 {ANTHROPIC_SHA256}; one human turn retained, assistant turns and ratings excluded from input/labels.",
            "privacy": "Publisher reports PII filtering and manual review; local configured PII pattern, English confidence, exact and 85%-near duplicate screens applied.",
            "residual": "Red-team task is mapped to provisional JB-attempt, not success or PI-Guard gold; source lacks PI-Guard taxonomy and pattern privacy screening is incomplete.",
        },
        "toxic_chat": {
            "repository": TOXIC_CHAT_REPO, "revision": TOXIC_CHAT_REVISION,
            "family": "sf_lmsys_toxic_chat_1123_round21", "license": "CC-BY-NC-4.0",
            "locator": "https://huggingface.co/datasets/lmsys/toxic-chat",
            "rights": "CC-BY-NC-4.0 declared by the publisher; attribution retained. Research is non-commercial, classifier-only, private and non-redistributive.",
            "lineage": f"Pinned data/1123 train CSV only; SHA-256 {TOXIC_CHAT_SHA256}; only user_input/jailbreaking columns projected; no source test file opened.",
            "privacy": "Publisher documents manual PII removal; local configured PII pattern, English confidence, exact and 85%-near duplicate screens applied.",
            "residual": "Publisher warns residual PII may remain; automated screening is incomplete. The source is one collection family and is validation-only here.",
        },
    }[source_key]
    evidence_refs = {}
    evidence_findings = {
        "rights": ("rights", info["rights"]),
        "lineage": ("lineage", info["lineage"]),
        "privacy": ("privacy", info["privacy"] + " Residual limit: " + info["residual"]),
    }
    for kind, (_label, finding) in evidence_findings.items():
        path = package / "evidence" / f"round21_{source_key}_{kind}.json"
        evidence = {
            "source_repository_id": info["repository"],
            "source_revision": info["revision"],
            "finding": finding,
        }
        if kind == "rights":
            evidence["authorized_scope"] = "private_local_research_nonredistributive"
            evidence["redistribution_allowed"] = False
        R18.write_json(path, evidence)
        evidence_refs[kind] = R18.ref(path, package)
    return {
        "source_repository_id": info["repository"],
        "source_revision": info["revision"],
        "source_family_id": info["family"],
        "license": info["license"],
        "source_locator": info["locator"],
        "rights_scope": "private_local_research_nonredistributive",
        "rights_notice": info["rights"],
        "rights_status": "research_only",
        "lineage_status": "verified",
        "privacy_status": "screened",
        "privacy_method": info["privacy"],
        "residual_limits": info["residual"],
        "historical_locked_rows_excluded": True,
        "redistribution_allowed": False,
        "rights_evidence": evidence_refs["rights"],
        "lineage_evidence": evidence_refs["lineage"],
        "privacy_evidence": evidence_refs["privacy"],
    }


def make_row_records(candidate: dict, partition: str) -> tuple[dict, dict, dict]:
    text = candidate["text"].strip()
    text_hash = sha256_bytes(text.encode("utf-8"))
    normalized_hash = sha256_bytes(candidate["normalized"].encode("utf-8"))
    row_id = "r21_" + sha256_bytes(
        "\x1f".join((candidate["repository"], candidate["revision"], candidate["source_record_id"], text_hash)).encode("utf-8")
    )[:32]
    prompt_family = "pf_" + normalized_hash[:24]
    duplicate_group = "dg_" + normalized_hash[:24]
    row = {"id": row_id, "text": text, "label": candidate["label"], "label_id": LABEL_IDS[candidate["label"]]}
    provenance = {
        "id": row_id,
        "source_repository_id": candidate["repository"],
        "source_revision": candidate["revision"],
        "upstream_split": candidate["upstream_split"],
        "source_record_id": candidate["source_record_id"],
        "source_family_id": candidate["source_family_id"],
        "collection_lineage_id": candidate["collection_lineage_id"],
        "prompt_family_id": prompt_family,
        "duplicate_group_id": duplicate_group,
        "native_label": candidate["native_label"],
        "mapping_rule_id": candidate["rule"],
        "language": "en",
        "partition": partition,
        "text_sha256": text_hash,
    }
    meta = {
        "id": row_id,
        "label": candidate["label"],
        "source_family_id": candidate["source_family_id"],
        "collection_lineage_id": candidate["collection_lineage_id"],
        "prompt_family_id": prompt_family,
        "duplicate_group_id": duplicate_group,
    }
    return row, provenance, meta


def assert_package_contract(package: Path, manifest: dict, split: dict,
                            train_rows: list[dict], train_prov: list[dict], train_meta: list[dict],
                            val_rows: list[dict], val_prov: list[dict], val_meta: list[dict]) -> None:
    if len(train_rows) != len(train_prov) or len(train_rows) != len(train_meta):
        raise ValueError("ROUND21_TRAIN_ALIGNMENT_FAILURE")
    if len(val_rows) != len(val_prov) or len(val_rows) != len(val_meta):
        raise ValueError("ROUND21_VALIDATION_ALIGNMENT_FAILURE")
    for part, rows, provenance, meta in (
        ("train", train_rows, train_prov, train_meta),
        ("validation", val_rows, val_prov, val_meta),
    ):
        if len({item["id"] for item in rows}) != len(rows):
            raise ValueError("ROUND21_DUPLICATE_ROW_ID:" + part)
        if any(row["id"] != prov["id"] or row["id"] != item["id"] for row, prov, item in zip(rows, provenance, meta)):
            raise ValueError("ROUND21_ROW_PROVENANCE_ALIGNMENT:" + part)
        for row, prov in zip(rows, provenance):
            if row["label"] not in LABEL_IDS or row["label_id"] != LABEL_IDS[row["label"]]:
                raise ValueError("ROUND21_LABEL_ID_MISMATCH:" + part)
            if sha256_bytes(row["text"].encode("utf-8")) != prov["text_sha256"]:
                raise ValueError("ROUND21_TEXT_HASH_MISMATCH:" + part)
    train_families = {item["source_family_id"] for item in train_meta}
    val_families = {item["source_family_id"] for item in val_meta}
    if train_families & val_families:
        raise ValueError("ROUND21_SOURCE_FAMILY_CROSSES_SPLITS")
    train_labels = collections.Counter(row["label"] for row in train_rows)
    val_labels = collections.Counter(row["label"] for row in val_rows)
    if set(train_labels) != set(LABEL_IDS) or set(val_labels) != set(LABEL_IDS):
        raise ValueError("ROUND21_CLASS_COVERAGE_MISSING")
    families_by_label = {
        part: {label: len({x["source_family_id"] for x in meta if x["label"] == label})
               for label in LABEL_IDS}
        for part, meta in (("train", train_meta), ("validation", val_meta))
    }
    if any(count < 2 for count in families_by_label["train"].values()):
        raise ValueError("ROUND21_TRAIN_FAMILY_MINIMUM_NOT_MET")
    if any(count < 1 for count in families_by_label["validation"].values()):
        raise ValueError("ROUND21_VALIDATION_FAMILY_MINIMUM_NOT_MET")
    manifest["aggregate_counts"] = {
        "train": dict(sorted(train_labels.items())),
        "validation": dict(sorted(val_labels.items())),
        "test_contract_only": manifest["aggregate_counts"].get("test_contract_only", {}),
    }
    split["access"] = {"test_opened": False, "test_used_for_selection": False}
    split["frozen"] = True


def main() -> int:
    if OUTPUT_PACKAGE.exists() or REPORT.exists():
        raise FileExistsError("ROUND21_OUTPUT_EXISTS_REFUSING_OVERWRITE")
    manifest, split, review, mapping, base_train, base_train_prov, base_val, base_val_prov = load_base_package()
    frozen = base_text_labels(base_train, base_val)

    # CLINC's prior exact screen also excluded overlaps with the rejected Dolly
    # comparator; keep that conservative exclusion while the R21 package itself
    # uses only the immutable package-A train.
    clinc_old, _ = CLINC_AUDIT.package_texts(
        CLINC_AUDIT.ROUND07, "pi_guard_l2_native_reference_round07_r01"
    )
    clinc_aug, _ = CLINC_AUDIT.package_texts(
        CLINC_AUDIT.ROUND18_B, "pi_guard_l2_source_heldout_dolly_aug_round18_r01"
    )
    clinc_candidates, clinc_audit = candidates_clinc(clinc_old | clinc_aug)
    anthropic_round07, _ = ANTHROPIC_AUDIT.package_texts(
        ANTHROPIC_AUDIT.ROUND07, "pi_guard_l2_native_reference_round07_r01"
    )
    anthropic_candidates, anthropic_audit = candidates_anthropic(set(frozen) | anthropic_round07)
    toxic_candidates, toxic_audit = candidates_toxic_chat(set(frozen))

    audit_path = ROOT / "clinc_oos_train_candidate_audit_round19.json"
    clinc_expected = json.loads(audit_path.read_text(encoding="utf-8"))["eligible_unique_train_rows"]
    anthropic_expected = json.loads((ROOT / "anthropic_redteam_candidate_audit_round19.json").read_text(encoding="utf-8"))["eligible_unique_single_turn_english_private_screened_rows"]
    toxic_expected = json.loads((ROOT / "toxic_chat_train_candidate_audit_round21.json").read_text(encoding="utf-8"))["aggregate_counters"]["eligible_unique_candidate_rows"]
    if len(clinc_candidates) != clinc_expected:
        raise ValueError("CLINC_REPLAY_COUNT_MISMATCH")
    if len(anthropic_candidates) != anthropic_expected:
        raise ValueError("ANTHROPIC_REPLAY_COUNT_MISMATCH")
    toxic_pre_near = toxic_audit["counters"].get("unique_pre_near_duplicate_candidates")
    if toxic_pre_near != 89:
        raise ValueError("TOXIC_CHAT_PRE_NEAR_REPLAY_COUNT_MISMATCH")

    all_candidates = clinc_candidates + anthropic_candidates + toxic_candidates
    exact_existing: set[int] = set()
    # The source-specific pass above is exact; this pass tests all new candidates
    # against package-A train/validation at the project 85% shingle threshold.
    near_old = near_duplicate_against_frozen(all_candidates, BASE_PACKAGE)
    for index in near_old:
        exact_existing.add(index)
    candidates = [item for index, item in enumerate(all_candidates) if index not in exact_existing]

    grouped_rows = [{"text": item["text"], "label": item["label"], "sources": []} for item in candidates]
    groups, grouping = SPLIT_HELPERS.prompt_groups(grouped_rows)
    group_members: dict[int, list[int]] = collections.defaultdict(list)
    for index in range(len(candidates)):
        group_members[groups.find(index)].append(index)
    selected: list[dict] = []
    duplicate_rows_excluded = 0
    conflict_rows_excluded = 0
    cross_partition_groups_excluded = 0
    for indexes in group_members.values():
        values = [candidates[index] for index in indexes]
        labels = {item["label"] for item in values}
        partitions = {item["partition"] for item in values}
        if len(labels) > 1:
            conflict_rows_excluded += len(values)
            continue
        if len(partitions) > 1:
            cross_partition_groups_excluded += len(values)
            continue
        selected.append(values[0])
        duplicate_rows_excluded += len(values) - 1

    train_additions = [item for item in selected if item["partition"] == "train"]
    val_additions = [item for item in selected if item["partition"] == "validation"]
    additions_by_source = collections.Counter(item["source_key"] for item in selected)
    expected_sources = {"clinc", "anthropic", "toxic_chat"}
    if set(additions_by_source) != expected_sources:
        raise ValueError("ROUND21_SOURCE_ROLE_LOST_AFTER_DEDUP")

    train_rows = list(base_train)
    train_prov = list(base_train_prov)
    train_meta = list(split["partitions"]["train"])
    for candidate in train_additions:
        row, prov, meta = make_row_records(candidate, "train")
        train_rows.append(row)
        train_prov.append(prov)
        train_meta.append(meta)
    val_rows = list(base_val)
    val_prov = list(base_val_prov)
    val_meta = list(split["partitions"]["validation"])
    for candidate in val_additions:
        row, prov, meta = make_row_records(candidate, "validation")
        val_rows.append(row)
        val_prov.append(prov)
        val_meta.append(meta)

    OUTPUT_PACKAGE.mkdir(parents=True, exist_ok=False)
    shutil.copytree(BASE_PACKAGE / "evidence", OUTPUT_PACKAGE / "evidence", dirs_exist_ok=True)
    shutil.copy2(BASE_PACKAGE / "AUTONOMOUS_PROTOCOL.json", OUTPUT_PACKAGE / "AUTONOMOUS_PROTOCOL.json")
    new_review = list(review["sources"])
    source_by_key = {}
    for source_key in ("clinc", "anthropic", "toxic_chat"):
        entry = source_review_entry(OUTPUT_PACKAGE, source_key)
        new_review.append(entry)
        source_by_key[source_key] = entry
    review = {"distribution_scope": "private_local_research_nonredistributive", "sources": new_review}

    mapping = json.loads(json.dumps(mapping))
    mapping_rules = {
        "clinc": {
            "repo": CLINC_REPO,
            "native": "in-scope assistant intent (non-OOS)",
            "rule": "clinc_plus_train_in_scope_intent_to_provisional_benign_r21",
            "label": "benign",
            "basis": "Human-elicited task-oriented assistant queries; native intent labels are not safety labels. Provisional benign reference only after privacy, English, intent-pattern and duplicate screens.",
        },
        "anthropic": {
            "repo": ANTHROPIC_REPO,
            "native": "human red-team attempt to elicit harmful output in a one-human-turn transcript",
            "rule": "anthropic_single_human_turn_red_team_attempt_to_provisional_jb_attempt_r21",
            "label": "JB",
            "basis": "The source collection task is human red-teaming for harmful model outputs. Map the first/only human input to a provisional JB-attempt reference; do not use transcript success rating, assistant replies, or claim PI-Guard gold. This is a broad task-level mapping and remains a semantic limitation.",
        },
        "toxic_chat": {
            "repo": TOXIC_CHAT_REPO,
            "native": "jailbreaking=1",
            "rule": "toxic_chat_native_jailbreaking_true_to_provisional_jb_attempt_r21",
            "label": "JB",
            "basis": "The publisher's human annotation marks a user attempt to trick the chatbot; retain only native positive rows. Negative/null rows are not mapped to benign. Provisional JB-attempt reference only.",
        },
    }
    for key, rule in mapping_rules.items():
        mapping["rules"].append({
            "source_repository_id": rule["repo"],
            "native_label": rule["native"],
            "mapping_rule_id": rule["rule"],
            "label": rule["label"],
            "mapping_basis": rule["basis"],
        })

    split["split_policy"] = (
        "Round21 frozen source-heldout L2 protocol: unchanged round18 package-A train plus all qualified CLINC in-scope train candidates and Anthropic HH-RLHF single-human-turn red-team train candidates; validation retains the original held-out OASST1/LLMail/JBC cohorts plus ToxicChat 1123 train-only native jailbreak positives, held out as a distinct collection family. Exact and project 85%-near duplicates are grouped/excluded before freezing. Test remains the prior family-level metadata contract only."
    )
    split["partitions"]["train"] = train_meta
    split["partitions"]["validation"] = val_meta

    rows_root = OUTPUT_PACKAGE / "corpus" / "rows"
    provenance_root = OUTPUT_PACKAGE / "corpus" / "provenance"
    R18.write_jsonl(rows_root / "train.jsonl", train_rows)
    R18.write_jsonl(provenance_root / "train.jsonl", train_prov)
    R18.write_jsonl(rows_root / "validation.jsonl", val_rows)
    R18.write_jsonl(provenance_root / "validation.jsonl", val_prov)
    R18.write_json(OUTPUT_PACKAGE / "split_manifest.json", split)
    R18.write_json(OUTPUT_PACKAGE / "source_review.json", review)
    R18.write_json(OUTPUT_PACKAGE / "label_mapping.json", mapping)

    new_lineages = [
        f"{CLINC_REPO}@{CLINC_REVISION}",
        f"{ANTHROPIC_REPO}@{ANTHROPIC_REVISION}",
        f"{TOXIC_CHAT_REPO}@{TOXIC_CHAT_REVISION}",
    ]
    lineage_packages = list(dict.fromkeys(manifest["lineage_packages"] + new_lineages))
    package_manifest = {
        "package_id": OUTPUT_PACKAGE_ID,
        "dataset_version": OUTPUT_VERSION,
        "schema": manifest["schema"],
        "language": "en",
        "label_status": manifest["label_status"],
        "distribution_scope": "private_local_research_nonredistributive",
        "historical_locked_rows_excluded": True,
        "trainable": True,
        "unknown_rights_holds": 0,
        "baseline": manifest["baseline"],
        "lineage_packages": lineage_packages,
        "partitions": {
            "train": {
                "rows": R18.ref(rows_root / "train.jsonl", OUTPUT_PACKAGE),
                "provenance": R18.ref(provenance_root / "train.jsonl", OUTPUT_PACKAGE),
            },
            "validation": {
                "rows": R18.ref(rows_root / "validation.jsonl", OUTPUT_PACKAGE),
                "provenance": R18.ref(provenance_root / "validation.jsonl", OUTPUT_PACKAGE),
            },
            "test": {"sealed_contract": "split.partitions.test"},
        },
        "refs": {
            "protocol": R18.ref(OUTPUT_PACKAGE / "AUTONOMOUS_PROTOCOL.json", OUTPUT_PACKAGE),
            "split": R18.ref(OUTPUT_PACKAGE / "split_manifest.json", OUTPUT_PACKAGE),
            "source_review": R18.ref(OUTPUT_PACKAGE / "source_review.json", OUTPUT_PACKAGE),
            "label_mapping": R18.ref(OUTPUT_PACKAGE / "label_mapping.json", OUTPUT_PACKAGE),
        },
        "aggregate_counts": {},
        "build_notes": {
            "round": 21,
            "source_candidates": {
                "clinc": clinc_audit,
                "anthropic": anthropic_audit,
                "toxic_chat": toxic_audit,
            },
            "round21_candidate_near_overlap_frozen_rows_excluded": len(near_old),
            "round21_candidate_near_duplicate_rows_excluded": duplicate_rows_excluded,
            "round21_cross_label_conflict_rows_excluded": conflict_rows_excluded,
            "round21_cross_partition_duplicate_groups_excluded": cross_partition_groups_excluded,
            "round21_admitted_additions_by_source": dict(sorted(additions_by_source.items())),
            "formal_acceptance_gate": "GATE_UNSPECIFIED",
            "test_opened": False,
            "l3_run": False,
            "smoke_run": False,
        },
    }
    assert_package_contract(OUTPUT_PACKAGE, package_manifest, split, train_rows, train_prov, train_meta,
                            val_rows, val_prov, val_meta)
    R18.write_json(OUTPUT_PACKAGE / "DATASET_MANIFEST.json", package_manifest)
    status = {
        "package_id": OUTPUT_PACKAGE_ID,
        "dataset_version": OUTPUT_VERSION,
        "schema": manifest["schema"],
        "language": "en",
        "trainable": True,
        "frozen_split": True,
        "distribution_scope": "private_local_research_nonredistributive",
        "l2_run": False,
        "l3_run": False,
        "test_opened": False,
        "formal_acceptance_gate": "GATE_UNSPECIFIED",
    }
    R18.write_json(OUTPUT_PACKAGE / "STATUS.json", status)

    train_families = {label: len({x["source_family_id"] for x in train_meta if x["label"] == label}) for label in LABEL_IDS}
    val_families = {label: len({x["source_family_id"] for x in val_meta if x["label"] == label}) for label in LABEL_IDS}
    result = {
        "round": 21,
        "status": "FROZEN_L2_RESEARCH_PACKAGE",
        "package_id": OUTPUT_PACKAGE_ID,
        "dataset_version": OUTPUT_VERSION,
        "package_path_private": str(OUTPUT_PACKAGE),
        "package_manifest_sha256": sha256_file(OUTPUT_PACKAGE / "DATASET_MANIFEST.json"),
        "source_candidate_counts": {
            "clinc_pre_near": clinc_expected,
            "anthropic_pre_near": anthropic_expected,
            "toxic_chat_pre_near": toxic_pre_near,
            "toxic_chat_after_frozen_and_within_source_screen": toxic_expected,
            "admitted_after_all_duplicates": dict(sorted(additions_by_source.items())),
        },
        "near_duplicate_and_conflict_exclusions": {
            "near_overlap_frozen": len(near_old),
            "within_and_cross_source_duplicate_rows": duplicate_rows_excluded,
            "cross_label_conflict_rows": conflict_rows_excluded,
            "cross_partition_duplicate_group_rows": cross_partition_groups_excluded,
            "project_jaccard_threshold": 0.85,
        },
        "train_rows": len(train_rows),
        "validation_rows": len(val_rows),
        "train_counts": package_manifest["aggregate_counts"]["train"],
        "validation_counts": package_manifest["aggregate_counts"]["validation"],
        "train_source_families_by_label": train_families,
        "validation_source_families_by_label": val_families,
        "test_contract": "family_metadata_only_copied_without_row_ids_text_or_payload",
        "formal_acceptance_gate": "GATE_UNSPECIFIED",
        "test_opened": False,
        "l3_run": False,
        "smoke_run": False,
    }
    R18.write_json(REPORT, result)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
