#!/usr/bin/env python3
"""Build a private, source-derived L2 train/validation candidate.

Only pinned train payloads are read. The sealed test contract is copied as
family-level metadata; no test row identifiers, text, or payload are opened.
"""
from __future__ import annotations

import bz2
import collections
import copy
import hashlib
import hmac
import json
import os
import re
import secrets
import shutil
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
PRIVATE = REPO / "workspaces" / "truongnv" / "pi_guard_pipeline"
TRAINING = PRIVATE / "training_bases"
VENDOR = TRAINING / "datasets" / "project_training" / "history" / "pi_guard_v8_english_diagnostic_20261012" / "tools" / "_vendor"
TASK_QUAL = ROOT / "source_qualification"
TENSOR_DIR = TRAINING / "datasets" / "source_datasets" / "tensor_trust_human_attacks_candidate_round01"
TRUST_DIR = TRAINING / "datasets" / "source_datasets" / "trustairlab_in_the_wild_candidate_round05"
NEURAL = TASK_QUAL / "acquired" / "neuralchemy_core_train.parquet"
NEURAL_MANIFEST = TASK_QUAL / "acquired" / "neuralchemy_core_train_manifest.json"
PROTOCOL = ROOT / "AUTONOMOUS_PROTOCOL.json"
OLD_PACKAGE = TRAINING / "datasets" / "project_training" / "versions" / "pi_guard_native_reference_round05_20261013_r03"
VERSIONS = TRAINING / "datasets" / "project_training" / "versions"
PACKAGE_ID = "pi_guard_l2_native_reference_round07_r01"
DATASET_VERSION = "0.7.0-native-reference-l2-candidate"
PACKAGE = VERSIONS / "pi_guard_native_reference_round07_20261013_r01"
STAGING = VERSIONS / (PACKAGE.name + ".building")
REPORT = ROOT / "l2_candidate_build_round07_r01.json"
SCHEMA = "pi_guard_autonomous_l2_v1"
LABEL_STATUS = "documented_native_reference_mapping_not_human_gold"
PRIVATE_SCOPE = "private_local_research_nonredistributive"
SEED = 20261013
MODEL_SHA256 = "f4f4a2c3465ca1f081541037f9cac23021d68151c2f709c55ae5eedfca522963"
REVISIONS = {
    "tensortrust": "747a75e096761ebc01bd3970158827326b4add23",
    "trustair": "a10aab8eff1c73165a442d4464dce192bd28b9c5",
    "neuralchemy": "7d70432dfcf47a821612cbf9d34e9d9e3ad20e75",
}
REPOSITORIES = {
    "tensortrust": "HumanCompatibleAI/tensor-trust-data",
    "trustair": "TrustAIRLab/in-the-wild-jailbreak-prompts",
    "hackaprompt": "neuralchemy/Prompt-injection-dataset",
}
SOURCE_PRIORITY = {"hackaprompt": 0, "trustair": 1, "tensortrust": 2}
LABEL_IDS = {"benign": 0, "PI": 1, "JB": 2}
PATTERNS = {
    "email": re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"),
    "credential_assignment": re.compile(
        r"(?i)\b(?:api[_ -]?key|access[_ -]?token|password|passwd|secret)\s*[:=]\s*[^\s,;]+"
    ),
    "ipv4": re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b"),
    "private_key": re.compile(r"(?i)-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "bearer_token": re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]{16,}"),
    "long_phone_like": re.compile(r"(?<!\w)(?:\+?\d[\d .()\-]{8,}\d)(?!\w)"),
}


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("JSON_OBJECT_REQUIRED:" + str(path))
    return value


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8", newline="\n")


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")


def norm(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def privacy_flags(text: str) -> list[str]:
    return [name for name, pattern in PATTERNS.items() if pattern.search(text)]


def hmac_id(key: bytes, namespace: str, value: str) -> str:
    digest = hmac.new(key, (namespace + "\x1f" + value).encode("utf-8"), hashlib.sha256).hexdigest()
    return namespace + "_" + digest[:32]


def family_is_validation(key: bytes, family_id: str) -> bool:
    digest = hmac.new(key, ("split-v1\x1f" + str(SEED) + "\x1f" + family_id).encode("utf-8"),
                       hashlib.sha256).digest()
    return digest[0] % 5 == 0


def get_family_key() -> bytes:
    path = TENSOR_DIR / "candidate_family_hmac.key"
    if path.exists():
        key = path.read_bytes()
        if len(key) != 32:
            raise ValueError("FAMILY_HMAC_KEY_INVALID")
        return key
    key = secrets.token_bytes(32)
    path.write_bytes(key)
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass
    return key


def language_identifier():
    sys.path.insert(0, str(VENDOR))
    import py3langid
    from py3langid.langid import LanguageIdentifier, MODEL_FILE
    model_path = Path(py3langid.__file__).resolve().parent / MODEL_FILE
    if sha_file(model_path) != MODEL_SHA256:
        raise ValueError("PINNED_LANGUAGE_MODEL_HASH_MISMATCH")
    return LanguageIdentifier.from_model_file(MODEL_FILE, norm_probs=True)


def verify_sources() -> tuple[dict, dict, dict, dict]:
    tensor = load_json(TENSOR_DIR / "SOURCE_MANIFEST.json")
    trust = load_json(TRUST_DIR / "ACQUISITION_MANIFEST.json")
    neural = load_json(NEURAL_MANIFEST)
    tensor_path = TENSOR_DIR / "raw_dump_attacks.jsonl.bz2"
    if (tensor.get("dataset_id") != REPOSITORIES["tensortrust"]
            or tensor.get("revision") != REVISIONS["tensortrust"]
            or tensor.get("source_path") != "raw-data/v2/raw_dump_attacks.jsonl.bz2"
            or sha_file(tensor_path) != tensor.get("archive_sha256")):
        raise ValueError("TENSORTRUST_PIN_OR_ARCHIVE_HASH_MISMATCH")
    if (trust.get("repository_id") != REPOSITORIES["trustair"]
            or trust.get("revision") != REVISIONS["trustair"]
            or trust.get("split_scope") != "train shards only"
            or trust.get("test_payload_opened") is not False
            or trust.get("validation_payload_opened") is not False
            or trust.get("source_eval_payload_opened") is not False):
        raise ValueError("TRUSTAIR_PIN_OR_SCOPE_MISMATCH")
    for item in trust.get("files", {}).values():
        source_path = TRUST_DIR / item["local_path"]
        if sha_file(source_path) != item["sha256"]:
            raise ValueError("TRUSTAIR_TRAIN_SHARD_HASH_MISMATCH")
    if (neural.get("dataset_id") != REPOSITORIES["hackaprompt"]
            or neural.get("revision") != REVISIONS["neuralchemy"]
            or neural.get("file") != "core/train-00000-of-00001.parquet"
            or sha_file(NEURAL) != neural.get("sha256")):
        raise ValueError("HACKAPROMPT_PIN_OR_TRAIN_HASH_MISMATCH")
    return tensor, trust, neural, load_json(PROTOCOL)


def candidate_record(source: str, repo: str, revision: str, upstream_split: str,
                     source_record_seed: str, family_id: str, native_label: str,
                     mapping_rule_id: str, label: str, text: str) -> dict:
    normalized_hash = sha_bytes(norm(text).encode("utf-8"))
    stored_text = text.strip()
    text_hash = sha_bytes(stored_text.encode("utf-8"))
    record_id = "l2r07_" + sha_bytes(
        "\x1f".join((repo, revision, family_id, normalized_hash)).encode("utf-8")
    )[:28]
    source_record_id = "src_" + sha_bytes(
        "\x1f".join((repo, revision, upstream_split, source_record_seed, normalized_hash)).encode("utf-8")
    )[:32]
    return {
        "id": record_id,
        "source": source,
        "source_repository_id": repo,
        "source_revision": revision,
        "upstream_split": upstream_split,
        "source_record_id": source_record_id,
        "source_family_id": family_id,
        "collection_lineage_id": family_id,
        "prompt_family_id": "prompt_" + normalized_hash,
        "duplicate_group_id": "duplicate_" + normalized_hash,
        "normalized_hash": normalized_hash,
        "native_label": native_label,
        "mapping_rule_id": mapping_rule_id,
        "label": label,
        "text": stored_text,
        "text_sha256": text_hash,
    }


def consider(records: list[dict], counts: collections.Counter, identifier, record: dict) -> None:
    text = record["text"]
    if not text.strip():
        counts["empty"] += 1
        return
    flags = privacy_flags(text)
    if flags:
        counts["privacy_excluded"] += 1
        for flag in flags:
            counts["privacy_flag:" + flag] += 1
        return
    language, confidence = identifier.classify(text.strip())
    if language != "en" or float(confidence) < 0.95:
        counts["language_excluded"] += 1
        return
    counts["qualified_before_global_dedup"] += 1
    records.append(record)


def collect_candidates(key: bytes, identifier, tensor_manifest: dict,
                       trust_manifest: dict) -> tuple[list[dict], dict]:
    candidates: list[dict] = []
    counts: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)

    tensor_path = TENSOR_DIR / "raw_dump_attacks.jsonl.bz2"
    tensor_seen: set[str] = set()
    tensor_counts = counts["tensortrust"]
    with bz2.open(tensor_path, "rt", encoding="utf-8") as stream:
        for ordinal, line in enumerate(stream):
            if not line.strip():
                continue
            source_row = json.loads(line)
            text = source_row.get("attacker_input")
            participant = source_row.get("attacker_id_anonymized")
            tensor_counts["raw_interaction_rows"] += 1
            if not isinstance(text, str) or not text.strip() or participant is None:
                tensor_counts["missing_attack_or_family"] += 1
                continue
            normalized_hash = sha_bytes(norm(text).encode("utf-8"))
            if normalized_hash in tensor_seen:
                tensor_counts["within_source_exact_duplicate"] += 1
                continue
            tensor_seen.add(normalized_hash)
            family_id = hmac_id(key, "tensortrust_attacker", str(participant))
            record = candidate_record(
                "tensortrust", REPOSITORIES["tensortrust"], REVISIONS["tensortrust"],
                "raw_dump_attacks", "unique_attack_" + normalized_hash,
                family_id, "attacker_submission", "tensortrust_attack_submission_to_PI_v1",
                "PI", text,
            )
            consider(candidates, tensor_counts, identifier, record)
            if ordinal and ordinal % 100000 == 0:
                print("TensorTrust raw interactions processed:", ordinal, flush=True)
    tensor_counts["unique_normalized_attack_inputs"] = len(tensor_seen)
    del tensor_seen

    trust_files = trust_manifest["files"]
    for relative, item in sorted(trust_files.items()):
        path = TRUST_DIR / item["local_path"]
        rows = pq.read_table(path, columns=["prompt", "jailbreak", "source"]).to_pylist()
        source_name = relative.split("/", 1)[0]
        for ordinal, row in enumerate(rows):
            trust_counts = counts["trustair_jailbreak" if bool(row.get("jailbreak")) else "trustair_regular"]
            text = row.get("prompt")
            family_name = row.get("source")
            if not isinstance(family_name, str) or not family_name.strip():
                trust_counts["missing_source_family"] += 1
                continue
            if not isinstance(text, str) or not text.strip():
                trust_counts["empty"] += 1
                continue
            is_jailbreak = row.get("jailbreak")
            if not isinstance(is_jailbreak, bool):
                trust_counts["invalid_native_label"] += 1
                continue
            label = "JB" if is_jailbreak else "benign"
            native = "jailbreak=true" if is_jailbreak else "jailbreak=false"
            rule = "trustair_jailbreak_true_to_JB_v1" if is_jailbreak else "trustair_jailbreak_false_to_benign_reference_v1"
            family_id = hmac_id(key, "trustair_source_family", norm(family_name))
            record = candidate_record(
                "trustair", REPOSITORIES["trustair"], REVISIONS["trustair"],
                item["upstream_split"], relative + "#" + str(ordinal),
                family_id, native, rule, label, text,
            )
            consider(candidates, trust_counts, identifier, record)
        counts["trustair_jailbreak" if "jailbreak_" in source_name else "trustair_regular"]["raw_rows"] += len(rows)

    neural_counts = counts["hackaprompt"]
    neural_rows = pq.read_table(
        NEURAL, columns=["text", "label", "category", "source", "augmented"]
    ).to_pylist()
    for ordinal, row in enumerate(neural_rows):
        if row.get("source") != "hackaprompt":
            continue
        neural_counts["source_rows"] += 1
        if row.get("category") != "direct_injection" or row.get("label") != 1 or row.get("augmented") is not False:
            neural_counts["excluded_not_unaugmented_direct_injection"] += 1
            continue
        family_id = "hackaprompt_competition_direct_injection"
        record = candidate_record(
            "hackaprompt", REPOSITORIES["hackaprompt"], REVISIONS["neuralchemy"],
            "core/train", "hackaprompt_core_train_" + str(ordinal),
            family_id, "source=hackaprompt;category=direct_injection;label=1;augmented=false",
            "hackaprompt_direct_injection_to_PI_v1", "PI", row.get("text") or "",
        )
        consider(candidates, neural_counts, identifier, record)

    return candidates, {name: dict(value) for name, value in counts.items()}


def deduplicate(candidates: list[dict]) -> tuple[list[dict], dict]:
    grouped: dict[str, list[dict]] = collections.defaultdict(list)
    for row in candidates:
        grouped[row["normalized_hash"]].append(row)
    output: list[dict] = []
    conflict_groups = 0
    same_label_duplicates = 0
    cross_source_duplicate_groups = 0
    for group in grouped.values():
        labels = {row["label"] for row in group}
        if len(labels) != 1:
            conflict_groups += 1
            continue
        sources = {row["source"] for row in group}
        if len(sources) > 1:
            cross_source_duplicate_groups += 1
        same_label_duplicates += len(group) - 1
        chosen = min(group, key=lambda row: (SOURCE_PRIORITY[row["source"]], row["source_record_id"]))
        output.append(chosen)
    output.sort(key=lambda row: row["id"])
    return output, {
        "unique_normalized_text_groups": len(grouped),
        "same_label_duplicate_rows_removed": same_label_duplicates,
        "cross_source_exact_duplicate_groups": cross_source_duplicate_groups,
        "label_conflict_groups_excluded": conflict_groups,
        "rows_after_exact_dedup": len(output),
    }


def assign_partitions(rows: list[dict], key: bytes) -> tuple[dict[str, list[dict]], dict]:
    partitions: dict[str, list[dict]] = {"train": [], "validation": []}
    for row in rows:
        if row["source"] == "hackaprompt":
            part = "train"
        else:
            part = "validation" if family_is_validation(key, row["source_family_id"]) else "train"
        row["partition"] = part
        partitions[part].append(row)
    class_families = {part: collections.defaultdict(set) for part in partitions}
    class_counts = {part: collections.Counter() for part in partitions}
    for part, part_rows in partitions.items():
        for row in part_rows:
            class_families[part][row["label"]].add(row["source_family_id"])
            class_counts[part][row["label"]] += 1
    missing = []
    for label in LABEL_IDS:
        if len(class_families["train"][label]) < 5:
            missing.append("TRAIN_FAMILY_SUPPORT_LT_5:" + label)
        if not class_families["validation"][label]:
            missing.append("VALIDATION_CLASS_MISSING:" + label)
    if missing:
        raise ValueError("SPLIT_SUPPORT_INVALID:" + ",".join(missing))
    for part in partitions:
        if not partitions[part]:
            raise ValueError("SPLIT_EMPTY:" + part)
    return partitions, {
        part: {
            "rows_by_label": dict(class_counts[part]),
            "families_by_label": {label: len(class_families[part][label]) for label in LABEL_IDS},
        }
        for part in partitions
    }


def evidence_documents(staging: Path, tensor: dict, trust: dict, neural: dict) -> dict[str, dict]:
    evidence: dict[str, dict] = {
        "tensortrust_rights": {
            "source_repository_id": REPOSITORIES["tensortrust"],
            "source_revision": REVISIONS["tensortrust"],
            "authorized_scope": PRIVATE_SCOPE,
            "redistribution_allowed": False,
            "finding": "Participant terms state consent for research use and planned public release, but the pinned repository has no dataset license. This candidate is restricted to private local research; this evidence does not establish redistribution rights.",
            "source": "https://tensortrust.ai/consent_and_terms.cfm",
        },
        "tensortrust_lineage": {
            "source_repository_id": REPOSITORIES["tensortrust"],
            "source_revision": REVISIONS["tensortrust"],
            "finding": "Pinned raw-data/v2 attack dump matches the acquisition manifest revision, Git blob identity, and SHA-256; only attacker_input and an in-memory anonymized family key are consumed.",
            "archive_sha256": tensor["archive_sha256"],
            "source_path": tensor["source_path"],
        },
        "tensortrust_privacy": {
            "source_repository_id": REPOSITORIES["tensortrust"],
            "source_revision": REVISIONS["tensortrust"],
            "finding": "Output rows retain attacker_input only; participant identifiers are HMAC-pseudonymized into family groups and never serialized. Defenses, access codes, timestamps, attack IDs, LLM outputs, and balance fields are discarded. PII-like matches and non-English/low-confidence text are excluded.",
            "finding_scope": "private local source-derived research data; automated screen is not a guarantee of no personal data",
        },
        "trustair_rights": {
            "source_repository_id": REPOSITORIES["trustair"],
            "source_revision": REVISIONS["trustair"],
            "finding": "The publisher's dataset card declares MIT for the dataset. This mapping uses only pinned train shards; licensing is attributed to the publisher declaration.",
            "source": "https://huggingface.co/datasets/TrustAIRLab/in-the-wild-jailbreak-prompts",
        },
        "trustair_lineage": {
            "source_repository_id": REPOSITORIES["trustair"],
            "source_revision": REVISIONS["trustair"],
            "finding": "Both pinned Dec-2023 train Parquet shards match acquisition-manifest SHA-256 values. Validation, test, and source-evaluation payloads were not opened.",
            "train_shards": {name: item["sha256"] for name, item in sorted(trust["files"].items())},
        },
        "trustair_privacy": {
            "source_repository_id": REPOSITORIES["trustair"],
            "source_revision": REVISIONS["trustair"],
            "finding": "Only prompt text and source-family grouping are consumed. Source/community names are HMAC-pseudonymized; timestamps and auxiliary fields are discarded. PII-like matches and non-English/low-confidence text are excluded.",
            "finding_scope": "automated screen is not a guarantee of no personal data",
        },
        "hackaprompt_rights": {
            "source_repository_id": REPOSITORIES["hackaprompt"],
            "source_revision": REVISIONS["neuralchemy"],
            "finding": "The pinned NeurAlchemy dataset card lists HackAPrompt competition data as CC BY 4.0. Only its core/train, source=hackaprompt, direct_injection, label=1, augmented=false rows are selected.",
            "source": "https://huggingface.co/datasets/neuralchemy/Prompt-injection-dataset",
        },
        "hackaprompt_lineage": {
            "source_repository_id": REPOSITORIES["hackaprompt"],
            "source_revision": REVISIONS["neuralchemy"],
            "finding": "The pinned NeurAlchemy core/train Parquet shard matches the acquisition manifest SHA-256. Source and category filters exclude all other components and augmented rows.",
            "train_shard_sha256": neural["sha256"],
        },
        "hackaprompt_privacy": {
            "source_repository_id": REPOSITORIES["hackaprompt"],
            "source_revision": REVISIONS["neuralchemy"],
            "finding": "Only text from the unaugmented HackAPrompt direct_injection component is consumed. PII-like matches and non-English/low-confidence text are excluded; group_id and all unrelated components are discarded.",
            "finding_scope": "automated screen is not a guarantee of no personal data",
        },
    }
    for name, value in evidence.items():
        write_json(staging / "evidence" / (name + ".json"), value)
    return evidence


def make_source_review(rows: list[dict], staging: Path, evidence: dict,
                       old_review: dict, test_families: list[dict]) -> dict:
    evidence_paths = {
        "tensortrust": ("evidence/tensortrust_rights.json", "evidence/tensortrust_lineage.json", "evidence/tensortrust_privacy.json"),
        "trustair": ("evidence/trustair_rights.json", "evidence/trustair_lineage.json", "evidence/trustair_privacy.json"),
        "hackaprompt": ("evidence/hackaprompt_rights.json", "evidence/hackaprompt_lineage.json", "evidence/hackaprompt_privacy.json"),
    }
    descriptions = {
        "tensortrust": {
            "rights_status": "research_only",
            "rights_notice": "Participant terms consent to research use and describe planned public data release; the data repository has no LICENSE. Local research only.",
            "license": "No repository license identified; research-use consent recorded, redistribution not authorized by this package.",
            "source_locator": "https://github.com/HumanCompatibleAI/tensor-trust-data",
            "privacy_method": "attacker_input-only extraction; in-memory participant HMAC grouping; email, credential, IP, private-key, bearer-token, phone-like, and language-confidence screens",
            "residual_limits": "No license or redistribution right established; regular-expression privacy screen can miss sensitive content; raw source remains private.",
            "rights_scope": PRIVATE_SCOPE,
            "redistribution_allowed": False,
        },
        "trustair": {
            "rights_status": "verified",
            "rights_notice": "Publisher dataset card declares MIT; pinned release metadata and train shard hashes are recorded.",
            "license": "MIT (publisher dataset-card declaration)",
            "source_locator": "https://huggingface.co/datasets/TrustAIRLab/in-the-wild-jailbreak-prompts",
            "privacy_method": "prompt-only extraction; HMAC pseudonymization of source family; PII-like and English-confidence screening",
            "residual_limits": "Publisher license attribution is not an independent rights determination for every collected upstream prompt; automated privacy screen can miss sensitive content.",
        },
        "hackaprompt": {
            "rights_status": "verified",
            "rights_notice": "Pinned NeurAlchemy card attributes CC BY 4.0 to the HackAPrompt competition component.",
            "license": "CC BY 4.0 (component-level publisher attribution)",
            "source_locator": "https://huggingface.co/datasets/neuralchemy/Prompt-injection-dataset",
            "privacy_method": "unaugmented direct_injection core/train component only; PII-like and English-confidence screening",
            "residual_limits": "Component license and authorship are attributed by the pinned dataset publisher; automated privacy screen can miss sensitive content.",
        },
    }
    sources: dict[tuple[str, str, str], dict] = {}
    by_repo = {
        REPOSITORIES["tensortrust"]: "tensortrust",
        REPOSITORIES["trustair"]: "trustair",
        REPOSITORIES["hackaprompt"]: "hackaprompt",
    }
    for row in rows:
        kind = row["source"]
        rights, lineage, privacy = evidence_paths[kind]
        spec = descriptions[kind]
        record = {
            "source_repository_id": row["source_repository_id"],
            "source_revision": row["source_revision"],
            "source_family_id": row["source_family_id"],
            "rights_status": spec["rights_status"],
            "lineage_status": "verified",
            "privacy_status": "screened",
            "rights_notice": spec["rights_notice"],
            "license": spec["license"],
            "source_locator": spec["source_locator"],
            "privacy_method": spec["privacy_method"],
            "residual_limits": spec["residual_limits"],
            "rights_evidence": {"path": rights, "sha256": sha_file(staging / rights)},
            "lineage_evidence": {"path": lineage, "sha256": sha_file(staging / lineage)},
            "privacy_evidence": {"path": privacy, "sha256": sha_file(staging / privacy)},
            "historical_locked_rows_excluded": True,
        }
        if kind == "tensortrust":
            record["rights_scope"] = PRIVATE_SCOPE
            record["redistribution_allowed"] = False
        key = (record["source_repository_id"], record["source_revision"], record["source_family_id"])
        sources[key] = record

    old_index = {
        (item.get("source_repository_id"), item.get("source_revision"), item.get("source_family_id")): item
        for item in old_review.get("sources", [])
    }
    for family in test_families:
        key = (family["source_repository_id"], family["source_revision"], family["source_family_id"])
        old = old_index.get(key)
        if old is None:
            raise ValueError("SEALED_TEST_FAMILY_REVIEW_METADATA_MISSING:" + key[0])
        for kind in ("rights", "lineage", "privacy"):
            ref = old[kind + "_evidence"]
            source_path = OLD_PACKAGE / ref["path"]
            if sha_file(source_path) != ref["sha256"]:
                raise ValueError("SEALED_TEST_EVIDENCE_HASH_MISMATCH:" + key[0] + ":" + kind)
            dest = staging / ref["path"]
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source_path, dest)
        sources[key] = copy.deepcopy(old)
    return {
        "distribution_scope": PRIVATE_SCOPE,
        "sources": sorted(sources.values(), key=lambda row: (
            row["source_repository_id"], row["source_revision"], row["source_family_id"]
        )),
    }


def main() -> int:
    if REPORT.exists() or PACKAGE.exists() or STAGING.exists():
        raise FileExistsError("ROUND07_ARTIFACT_ALREADY_EXISTS; inspect and version a new run, never overwrite")
    if not (PACKAGE.parent.resolve() == VERSIONS.resolve()):
        raise ValueError("PACKAGE_PATH_NOT_VERSION_CHILD")
    tensor, trust, neural, protocol = verify_sources()
    test_split = load_json(OLD_PACKAGE / "split_manifest.json")
    test_contract = copy.deepcopy(test_split["partitions"]["test"])
    if set(test_contract) != {"schema", "families"}:
        raise ValueError("SEALED_TEST_CONTRACT_HAS_NONFAMILY_FIELDS")
    old_review = load_json(OLD_PACKAGE / "source_review.json")
    key = get_family_key()
    identifier = language_identifier()
    candidates, source_counts = collect_candidates(key, identifier, tensor, trust)
    rows, duplicate_report = deduplicate(candidates)
    partitions, split_report = assign_partitions(rows, key)

    # The split contract includes only train/validation row metadata and the
    # previously approved family-only final-test metadata contract.
    split = {
        "schema": SCHEMA,
        "frozen": True,
        "split_policy": "Pinned train sources; deterministic HMAC family holdout by seed modulo 5; HackAPrompt competition component train-only.",
        "split_seed": SEED,
        "group_fields": ["source_family_id", "collection_lineage_id", "prompt_family_id", "duplicate_group_id"],
        "access": {"test_opened": False, "test_used_for_selection": False, "test_payload_read": False},
        "partitions": {},
    }
    row_counts: dict[str, dict[str, int]] = {}
    all_rows = []
    for part in ("train", "validation"):
        model_rows, sidecars, metadata = [], [], []
        for source_row in partitions[part]:
            row_id = source_row["id"]
            model_row = {
                "id": row_id,
                "text": source_row["text"],
                "label": source_row["label"],
                "label_id": LABEL_IDS[source_row["label"]],
            }
            sidecar = {
                "id": row_id,
                "source_repository_id": source_row["source_repository_id"],
                "source_revision": source_row["source_revision"],
                "upstream_split": source_row["upstream_split"],
                "source_record_id": source_row["source_record_id"],
                "source_family_id": source_row["source_family_id"],
                "collection_lineage_id": source_row["collection_lineage_id"],
                "prompt_family_id": source_row["prompt_family_id"],
                "duplicate_group_id": source_row["duplicate_group_id"],
                "native_label": source_row["native_label"],
                "mapping_rule_id": source_row["mapping_rule_id"],
                "language": "en",
                "partition": part,
                "text_sha256": source_row["text_sha256"],
            }
            model_rows.append(model_row)
            sidecars.append(sidecar)
            metadata.append({
                "id": row_id,
                "label": source_row["label"],
                "source_family_id": source_row["source_family_id"],
                "collection_lineage_id": source_row["collection_lineage_id"],
                "prompt_family_id": source_row["prompt_family_id"],
                "duplicate_group_id": source_row["duplicate_group_id"],
            })
            all_rows.append(source_row)
        rows_path = "corpus/rows/" + part + ".jsonl"
        prov_path = "corpus/provenance/" + part + ".jsonl"
        write_jsonl(STAGING / rows_path, model_rows)
        write_jsonl(STAGING / prov_path, sidecars)
        split["partitions"][part] = metadata
        row_counts[part] = dict(collections.Counter(row["label"] for row in model_rows))
    split["partitions"]["test"] = test_contract
    evidence = evidence_documents(STAGING, tensor, trust, neural)
    review = make_source_review(all_rows, STAGING, evidence, old_review, test_contract["families"])
    mapping = {
        "label_status": LABEL_STATUS,
        "ambiguous_or_hybrid": "exclude",
        "unsupported_harmful_request_to_JB_mapping": "forbidden",
        "rules": [
            {
                "source_repository_id": REPOSITORIES["tensortrust"],
                "native_label": "attacker_submission",
                "mapping_rule_id": "tensortrust_attack_submission_to_PI_v1",
                "label": "PI",
                "mapping_basis": "The source paper describes human game submissions as prompt-injection attacks aimed at overcoming a hidden defense; no harmful-request-only inference is used.",
            },
            {
                "source_repository_id": REPOSITORIES["trustair"],
                "native_label": "jailbreak=true",
                "mapping_rule_id": "trustair_jailbreak_true_to_JB_v1",
                "label": "JB",
                "mapping_basis": "Use the publisher's explicit jailbreak boolean from the pinned train shard as a documented native reference label.",
            },
            {
                "source_repository_id": REPOSITORIES["trustair"],
                "native_label": "jailbreak=false",
                "mapping_rule_id": "trustair_jailbreak_false_to_benign_reference_v1",
                "label": "benign",
                "mapping_basis": "Use the publisher's explicit non-jailbreak boolean as a benign reference class, not curator-reviewed gold.",
            },
            {
                "source_repository_id": REPOSITORIES["hackaprompt"],
                "native_label": "source=hackaprompt;category=direct_injection;label=1;augmented=false",
                "mapping_rule_id": "hackaprompt_direct_injection_to_PI_v1",
                "label": "PI",
                "mapping_basis": "Use only the unaugmented HackAPrompt component and its direct_injection category; no other NeurAlchemy categories are inferred into PI.",
            },
        ],
    }
    write_json(STAGING / "split_manifest.json", split)
    write_json(STAGING / "source_review.json", review)
    write_json(STAGING / "label_mapping.json", mapping)
    shutil.copyfile(PROTOCOL, STAGING / "AUTONOMOUS_PROTOCOL.json")

    refs = {}
    for name, relative in {
        "protocol": "AUTONOMOUS_PROTOCOL.json",
        "split": "split_manifest.json",
        "source_review": "source_review.json",
        "label_mapping": "label_mapping.json",
    }.items():
        refs[name] = {"path": relative, "sha256": sha_file(STAGING / relative)}
    partition_specs = {}
    for part in ("train", "validation"):
        row_relative = "corpus/rows/" + part + ".jsonl"
        prov_relative = "corpus/provenance/" + part + ".jsonl"
        partition_specs[part] = {
            "rows": {"path": row_relative, "sha256": sha_file(STAGING / row_relative)},
            "provenance": {"path": prov_relative, "sha256": sha_file(STAGING / prov_relative)},
        }
    manifest = {
        "package_id": PACKAGE_ID,
        "dataset_version": DATASET_VERSION,
        "schema": SCHEMA,
        "language": "en",
        "trainable": True,
        "label_status": LABEL_STATUS,
        "distribution_scope": PRIVATE_SCOPE,
        "historical_locked_rows_excluded": True,
        "unknown_rights_holds": 0,
        "lineage_packages": [
            REPOSITORIES["tensortrust"] + "@" + REVISIONS["tensortrust"],
            REPOSITORIES["trustair"] + "@" + REVISIONS["trustair"],
            REPOSITORIES["hackaprompt"] + "@" + REVISIONS["neuralchemy"] + "#hackaprompt-direct-injection",
        ],
        "baseline": protocol["baseline"],
        "refs": refs,
        "partitions": {
            **partition_specs,
            "test": {"sealed_contract": "split.partitions.test"},
        },
        "aggregate_counts": {
            "train": row_counts["train"],
            "validation": row_counts["validation"],
            "test_contract_only": {
                label: sum(family["label_support"][label] for family in test_contract["families"])
                for label in LABEL_IDS
            },
        },
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    status = {
        "package_id": PACKAGE_ID,
        "dataset_version": DATASET_VERSION,
        "schema": SCHEMA,
        "language": "en",
        "trainable": True,
        "frozen_split": True,
        "test_opened": False,
        "l2_run": False,
        "l3_run": False,
        "distribution_scope": PRIVATE_SCOPE,
    }
    write_json(STAGING / "DATASET_MANIFEST.json", manifest)
    write_json(STAGING / "STATUS.json", status)
    STAGING.rename(PACKAGE)

    report = {
        "report_id": "l2_candidate_build_round07_r01",
        "status": "BUILT_PRIVATE_L2_CANDIDATE",
        "package_id": PACKAGE_ID,
        "dataset_version": DATASET_VERSION,
        "private_package_path": str(PACKAGE),
        "private_only_nonredistributive": True,
        "formal_acceptance_gate": "GATE_UNSPECIFIED",
        "test_opened": False,
        "test_payload_read": False,
        "test_contract_family_count": len(test_contract["families"]),
        "test_row_ids_or_text_emitted": False,
        "model_fit_started": False,
        "l3_run": False,
        "source_counts_and_filters": source_counts,
        "deduplication": duplicate_report,
        "partition_summary": split_report,
        "rows_by_partition_and_label": row_counts,
        "source_family_review_entries": len(review["sources"]),
        "language_model_sha256": MODEL_SHA256,
        "package_manifest_sha256": sha_file(PACKAGE / "DATASET_MANIFEST.json"),
        "train_rows_sha256": manifest["partitions"]["train"]["rows"]["sha256"],
        "validation_rows_sha256": manifest["partitions"]["validation"]["rows"]["sha256"],
    }
    write_json(REPORT, report)
    print(json.dumps({
        "status": report["status"],
        "package_id": PACKAGE_ID,
        "rows_by_partition_and_label": row_counts,
        "partition_summary": split_report,
        "test_opened": False,
        "l3_run": False,
        "report": str(REPORT),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
