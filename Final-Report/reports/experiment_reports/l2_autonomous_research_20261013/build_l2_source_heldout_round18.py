"""Build two private L2-only packages with one frozen external validation set.

Package A reuses only the round07 train partition. Package B adds audited,
instruction-only Dolly benign references. Both use OASST1 benign, LLMail PI,
and manual JBC jailbreak-attempt references as source-held-out validation.
Only aggregates are written to the tracked report directory; prompt rows stay
inside the ignored private workspace. No test, L3, or smoke data is accessed.
"""
from __future__ import annotations

import collections
import hashlib
import json
import re
import shutil
import sys
import unicodedata
from pathlib import Path
from typing import Any, Iterator

import pyarrow.parquet as pq


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
PRIVATE = REPO / "workspaces" / "truongnv" / "pi_guard_pipeline"
TRAINING = PRIVATE / "training_bases"
ROUND07 = TRAINING / "datasets" / "project_training" / "versions" / "pi_guard_native_reference_round07_20261013_r01"
SOURCE = TRAINING / "datasets" / "source_audit"
OUTPUT_ROOT = TRAINING / "datasets" / "project_training" / "versions"
VENDOR = TRAINING / "datasets" / "project_training" / "history" / "pi_guard_v8_english_diagnostic_20261012" / "tools" / "_vendor"
REPORT = ROOT / "l2_source_heldout_package_build_round18.json"
PROTOCOL_SOURCE = ROOT / "AUTONOMOUS_PROTOCOL.json"

LABEL_STATUS = "documented_native_reference_mapping_not_human_gold"
LABEL_IDS = {"benign": 0, "PI": 1, "JB": 2}
PACKAGE_SPECS = (
    ("pi_guard_l2_source_heldout_round18_r01", "0.8.0-source-heldout-l2-reference"),
    ("pi_guard_l2_source_heldout_dolly_aug_round18_r01", "0.8.1-dolly-augmented-source-heldout-l2-reference"),
)

PII_PATTERNS = {
    "email": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "us_ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "phone_candidate": re.compile(r"(?<!\w)(?:\+?1[ .-]?)?(?:\(?\d{3}\)?[ .-]?)\d{3}[ .-]?\d{4}(?!\w)"),
    "ipv4": re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b"),
    "credential_assignment": re.compile(r"(?i)\b(?:api[_ -]?key|access[_ -]?token|password|passwd|secret)\s*[:=]\s*[^\s,;]+"),
    "private_key": re.compile(r"(?i)-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "bearer_token": re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]{16,}"),
}
DOLLY_PII_PATTERNS = {
    "email": PII_PATTERNS["email"],
    "us_ssn": PII_PATTERNS["us_ssn"],
    "phone_candidate": PII_PATTERNS["phone_candidate"],
}
OASST_PII_PATTERNS = {
    key: PII_PATTERNS[key]
    for key in ("email", "us_ssn", "phone_candidate", "ipv4", "credential_assignment")
}
JBB_PII_PATTERNS = dict(OASST_PII_PATTERNS)
LLMAIL_PII_PATTERNS = {
    "email": PII_PATTERNS["email"],
    "us_ssn": PII_PATTERNS["us_ssn"],
    "ipv4": PII_PATTERNS["ipv4"],
    "credential_assignment": PII_PATTERNS["credential_assignment"],
    "private_key": PII_PATTERNS["private_key"],
    "bearer_token": PII_PATTERNS["bearer_token"],
    "phone_candidate": re.compile(r"(?<!\w)(?:\+?\d[\d .()\-]{8,}\d)(?!\w)"),
}
DOLLY_REVIEW_PATTERNS = {
    "instruction_override": re.compile(r"\b(ignore|disregard|forget|override|bypass)\b.{0,80}\b(instructions?|rules?|system|developer|policy)\b", re.I | re.S),
    "secret_extraction": re.compile(r"\b(reveal|show|print|repeat|extract|disclose)\b.{0,80}\b(system prompt|hidden prompt|secret|api key|password)\b", re.I | re.S),
    "harmful_intent_terms": re.compile(r"\b(make a bomb|build a weapon|steal credentials|write malware|kill someone|self[- ]harm)\b", re.I),
}
OASST_REVIEW_LABELS = {"spam", "lang_mismatch", "pii", "not_appropriate", "hate_speech", "sexual_content", "violence"}

SOURCE_SPECS = {
    "dolly": {
        "repository": "databricks/databricks-dolly-15k",
        "revision": "bdd27f4d94b9c1f951818a7da7fd7aeea5dbff1a",
        "license": "CC-BY-SA-3.0",
        "locator": "https://huggingface.co/datasets/databricks/databricks-dolly-15k",
        "rule": "dolly_instruction_only_filtered_benign_r18",
        "native": "human_instruction_no_context_after_conservative_screen",
        "label": "benign",
        "source_family_id": "sf_dolly15k_human_instruction_v1",
        "collection_lineage_id": "cl_databricks_dolly15k_bdd27f4d",
        "privacy": "Email, phone, and SSN patterns were screened in instruction text; context and response were never model inputs.",
        "lineage": "Pinned Databricks Dolly train JSONL by repository revision and SHA-256; row ordinals are retained only in the private package.",
        "rights": "Dataset card declares CC-BY-SA-3.0; attribution notice is retained in this private research package.",
        "residual": "Human-authored instructions are not curated benign-safety labels. Regex and conservative intent screens are incomplete; no full privacy adjudication was performed. Private local research only; do not redistribute this package.",
    },
    "oasst": {
        "repository": "OpenAssistant/oasst1",
        "revision": "c6c1242d280bf4c487619ab08c30d43872afcf56",
        "license": "Apache-2.0",
        "locator": "https://huggingface.co/datasets/OpenAssistant/oasst1",
        "rule": "oasst1_root_prompter_screened_benign_r18",
        "native": "english_root_prompter_without_positive_review_flags",
        "label": "benign",
        "source_family_id": "sf_oasst1_train_root_prompter_v1",
        "collection_lineage_id": "cl_openassistant_oasst1_c6c1242d",
        "privacy": "English root prompter rows only; exclude deleted/unknown, synthetic/unknown, positive native moderation labels, and configured PII-pattern matches.",
        "lineage": "Pinned OASST1 train parquet by repository revision and file SHA-256; root prompts only and no upstream validation/test partitions read.",
        "rights": "Dataset card declares Apache-2.0; attribution notice is retained in this private research package.",
        "residual": "Root user messages and absence of positive review flags do not prove benign intent. Regex/native-label screening is not complete privacy or semantic adjudication. Private local research only; do not redistribute this package.",
    },
    "llmail": {
        "repository": "microsoft/llmail-inject-challenge",
        "revision": "1063bdf01ec8762b812d5e06ee768a06faa5a6f7",
        "license": "MIT (dataset card); contest submission terms also recorded",
        "locator": "https://huggingface.co/datasets/microsoft/llmail-inject-challenge",
        "rule": "llmail_native_attack_attempt_true_pi_reference_r18",
        "native": "attack_attempt=true",
        "label": "PI",
        "source_family_id": "sf_llmail_inject_phases_1_2",
        "collection_lineage_id": "cl_microsoft_llmail_inject_1063bdf0",
        "privacy": "Only labelled-unique phase 1/2 records; exclude configured PII-pattern matches and require pinned py3langid English confidence >=0.95.",
        "lineage": "Pinned labelled-unique phase 1/2 files, separate contest false-positive test file not acquired, no submitter/team key in exported records; whole collection is one family.",
        "rights": "Dataset card declares MIT; contest terms grant the organizers a right to include submissions in public datasets and research materials. Private local research only; no redistribution of this package.",
        "residual": "Challenge-specific indirect-injection attempts are not representative of all direct PI inputs. Automated PII screening is incomplete, and no participant/family IDs are supplied. Native attack_attempt mapping is not canonical PI-Guard gold.",
    },
    "jbb": {
        "repository": "JailbreakBench/artifacts",
        "revision": "909e68c01d94222b8ad2e397a017e2e12e2adb73",
        "license": "MIT (artifact repository declaration)",
        "locator": "https://github.com/JailbreakBench/artifacts/tree/909e68c01d94222b8ad2e397a017e2e12e2adb73/attack-artifacts/JBC/manual",
        "rule": "jbb_jbc_manual_attempt_reference_r18",
        "native": "attack_method=JBC/manual",
        "label": "JB",
        "source_family_id": "sf_jbb_jbc_manual_v1",
        "collection_lineage_id": "cl_jailbreakbench_artifacts_jbc_manual_909e68c0",
        "privacy": "One pinned manual JBC artifact file only; configured PII patterns screened; no response, test-artifact, or evaluation file read.",
        "lineage": "One JBC/manual artifact per unique prompt/behavior is held as a single family. JBC is a separate benchmark packaging but shares the JailbreakChat community origin represented in TrustAIR/JailbreakHub.",
        "rights": "JailbreakBench artifact repository declares MIT; private research package preserves attribution and does not redistribute source data.",
        "residual": "A method marker supports jailbreak-attempt reference mapping, not success or canonical JB gold. Only 100 unique behaviors/prompts; community-origin overlap with TrustAIR limits independence claims. Regex screen is incomplete.",
    },
}


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalized(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def has_pii(text: str) -> bool:
    return any(pattern.search(text) for pattern in PII_PATTERNS.values())


def has_source_pii(text: str, source_key: str) -> bool:
    patterns = {"dolly": DOLLY_PII_PATTERNS, "oasst": OASST_PII_PATTERNS,
                "llmail": LLMAIL_PII_PATTERNS, "jbb": JBB_PII_PATTERNS}[source_key]
    return any(pattern.search(text) for pattern in patterns.values())


def stable_id(*parts: str) -> str:
    return hashlib.sha256("\x1f".join(parts).encode("utf-8")).hexdigest()


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


def is_attack_attempt(metadata: Any) -> bool:
    if not isinstance(metadata, dict):
        return False
    value = metadata.get("attack_attempt")
    return value is True or (isinstance(value, str) and value.casefold() == "true")


def load_package() -> tuple[dict, dict, dict, dict, dict, set[str], set[str], list[dict], list[dict]]:
    manifest_path = ROUND07 / "DATASET_MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("package_id") != "pi_guard_l2_native_reference_round07_r01":
        raise ValueError("UNEXPECTED_ROUND07_PACKAGE")
    split = json.loads((ROUND07 / "split_manifest.json").read_text(encoding="utf-8"))
    review = json.loads((ROUND07 / "source_review.json").read_text(encoding="utf-8"))
    mapping = json.loads((ROUND07 / "label_mapping.json").read_text(encoding="utf-8"))
    status = json.loads((ROUND07 / "STATUS.json").read_text(encoding="utf-8"))
    train_rows: list[dict] = []
    train_prov: list[dict] = []
    base_train_keys: set[str] = set()
    old_validation_keys: set[str] = set()
    for part, rows_target, prov_target in (("train", train_rows, train_prov),):
        for kind, destination in (("rows", rows_target), ("provenance", prov_target)):
            spec = manifest["partitions"][part][kind]
            path = ROUND07 / spec["path"]
            if sha_file(path) != spec["sha256"]:
                raise ValueError(f"ROUND07_{part}_{kind}_HASH_MISMATCH")
            with path.open("r", encoding="utf-8") as stream:
                destination.extend(json.loads(line) for line in stream if line.strip())
    if len(train_rows) != len(train_prov) or len(train_rows) != len(split["partitions"]["train"]):
        raise ValueError("ROUND07_TRAIN_ALIGNMENT_MISMATCH")
    for row in train_rows:
        key = normalized(row["text"])
        if key:
            base_train_keys.add(key)
    val_spec = manifest["partitions"]["validation"]["rows"]
    val_path = ROUND07 / val_spec["path"]
    if sha_file(val_path) != val_spec["sha256"]:
        raise ValueError("ROUND07_VALIDATION_ROWS_HASH_MISMATCH")
    with val_path.open("r", encoding="utf-8") as stream:
        for line in stream:
            row = json.loads(line)
            key = normalized(row.get("text", ""))
            if key:
                old_validation_keys.add(key)
    return manifest, split, review, mapping, status, base_train_keys, old_validation_keys, train_rows, train_prov


def add_candidate(rows: list[dict], source_key: str, text: str, upstream_split: str,
                  source_record_id: str, ancestry: str = "") -> None:
    key = normalized(text)
    if not key:
        return
    spec = SOURCE_SPECS[source_key]
    rows.append({
        "source_key": source_key,
        "repository": spec["repository"],
        "revision": spec["revision"],
        "license": spec["license"],
        "locator": spec["locator"],
        "rule": spec["rule"],
        "native_label": spec["native"],
        "label": spec["label"],
        "text": text.strip(),
        "normalized": key,
        "upstream_split": upstream_split,
        "source_record_id": source_record_id,
        "ancestry_key": normalized(ancestry) if ancestry else key,
    })


def candidates_dolly(base_train: set[str], old_validation: set[str]) -> tuple[list[dict], dict]:
    path = SOURCE / "dolly15k_round16" / "databricks-dolly-15k.jsonl"
    expected_hash = "2df9083338b4abd6bceb5635764dab5d833b393b55759dffb0959b6fcbf794ec"
    if sha_file(path) != expected_hash:
        raise ValueError("DOLLY_PINNED_TRAIN_HASH_MISMATCH")
    counts: collections.Counter[str] = collections.Counter()
    selected: list[dict] = []
    seen: set[str] = set()
    for index, line in enumerate(path.open("r", encoding="utf-8")):
        row = json.loads(line)
        counts["source_rows"] += 1
        text = row.get("instruction", "")
        if not isinstance(text, str) or not text.strip():
            counts["empty_instruction"] += 1
            continue
        if isinstance(row.get("context"), str) and row["context"].strip():
            counts["nonempty_context"] += 1
            continue
        if has_source_pii(text, "dolly"):
            counts["privacy_pattern"] += 1
            continue
        if any(pattern.search(text) for pattern in DOLLY_REVIEW_PATTERNS.values()):
            counts["conservative_intent_pattern"] += 1
            continue
        key = normalized(text)
        if key in base_train or key in old_validation:
            counts["overlap_round07"] += 1
            continue
        if key in seen:
            counts["within_source_duplicate"] += 1
            continue
        seen.add(key)
        add_candidate(selected, "dolly", text, "train", f"row_ordinal_{index}")
    expected_count = json.loads((ROOT / "dolly_candidate_audit_round16.json").read_text(encoding="utf-8")) if (ROOT / "dolly_candidate_audit_round16.json").exists() else None
    if len(selected) != 10354:
        raise ValueError(f"DOLLY_REPLAY_COUNT_MISMATCH:{len(selected)}")
    counts["selected_unique"] = len(selected)
    return selected, dict(sorted(counts.items()))


def flagged_oasst(labels: Any) -> bool:
    if not isinstance(labels, dict) or not isinstance(labels.get("name"), list):
        return False
    names = labels["name"]
    values = labels.get("value") if isinstance(labels.get("value"), list) else []
    value_by_name = dict(zip(names, values))
    return any(str(name) in OASST_REVIEW_LABELS and float(value_by_name.get(name, 0.0) or 0.0) > 0.0 for name in names)


def candidates_oasst(base_train: set[str], old_validation: set[str]) -> tuple[list[dict], dict]:
    path = SOURCE / "oasst1_round17" / "train.parquet"
    expected_hash = "bbfadf5ed1278ba2208c837fdcad865adf65f5df55d80abadab2745db13fcb5e"
    if sha_file(path) != expected_hash:
        raise ValueError("OASST1_PINNED_TRAIN_HASH_MISMATCH")
    table = pq.read_table(path, columns=["message_id", "parent_id", "role", "lang", "text", "deleted", "synthetic", "labels"])
    counts: collections.Counter[str] = collections.Counter()
    selected: list[dict] = []
    seen: set[str] = set()
    for row in table.to_pylist():
        counts["source_rows"] += 1
        if row.get("role") != "prompter" or row.get("parent_id") not in (None, "") or row.get("lang") != "en":
            continue
        counts["english_root_prompter"] += 1
        if row.get("deleted") is not False or row.get("synthetic") is not False:
            counts["deleted_or_synthetic_or_unknown"] += 1
            continue
        text = row.get("text")
        if not isinstance(text, str) or not text.strip():
            counts["empty_text"] += 1
            continue
        if flagged_oasst(row.get("labels")):
            counts["native_review_flag"] += 1
            continue
        if has_source_pii(text, "oasst"):
            counts["privacy_pattern"] += 1
            continue
        key = normalized(text)
        if key in base_train or key in old_validation:
            counts["overlap_round07"] += 1
            continue
        if key in seen:
            counts["within_source_duplicate"] += 1
            continue
        seen.add(key)
        record_id = row.get("message_id") or f"train_row_{counts['source_rows']}"
        add_candidate(selected, "oasst", text, "train", str(record_id))
    if len(selected) != 2089:
        raise ValueError(f"OASST1_REPLAY_COUNT_MISMATCH:{len(selected)}")
    counts["selected_unique"] = len(selected)
    return selected, dict(sorted(counts.items()))


def candidates_llmail(base_train: set[str], old_validation: set[str]) -> tuple[list[dict], dict]:
    source_dir = SOURCE / "llmail_inject_round17"
    audit = json.loads((ROOT / "llmail_english_clean_candidate_audit_round17.json").read_text(encoding="utf-8"))
    for phase, expected in audit["source_file_sha256"].items():
        path = source_dir / f"{phase}.json"
        if sha_file(path) != expected:
            raise ValueError(f"LLMAIL_PINNED_FILE_HASH_MISMATCH:{phase}")
    sys.path.insert(0, str(VENDOR))
    from py3langid.langid import LanguageIdentifier, MODEL_FILE
    import py3langid
    model_path = Path(py3langid.__file__).resolve().parent / MODEL_FILE
    if sha_file(model_path) != audit["language_model_sha256"]:
        raise ValueError("LLMAIL_LANGUAGE_MODEL_HASH_MISMATCH")
    identifier = LanguageIdentifier.from_model_file(MODEL_FILE, norm_probs=True)
    counts: collections.Counter[str] = collections.Counter()
    selected: list[dict] = []
    seen: set[str] = set()
    record_no = 0
    for phase in ("phase1", "phase2"):
        path = source_dir / f"{phase}.json"
        with path.open("r", encoding="utf-8") as stream:
            records = json.load(stream)
        for text, metadata in records.items():
            record_no += 1
            if not is_attack_attempt(metadata):
                continue
            counts["native_attack_attempt_true"] += 1
            if has_source_pii(text, "llmail"):
                counts["privacy_pattern"] += 1
                continue
            language, confidence = identifier.classify(text.strip())
            if language != "en" or float(confidence) < 0.95:
                counts["non_english_or_uncertain"] += 1
                continue
            key = normalized(text)
            if key in base_train or key in old_validation:
                counts["overlap_round07"] += 1
                continue
            if key in seen:
                counts["within_or_cross_phase_duplicate"] += 1
                continue
            seen.add(key)
            add_candidate(selected, "llmail", text, phase, f"phase_record_{record_no}")
        del records
    if len(selected) != 7491:
        raise ValueError(f"LLMAIL_REPLAY_COUNT_MISMATCH:{len(selected)}")
    counts["selected_unique"] = len(selected)
    return selected, dict(sorted(counts.items()))


def candidates_jbb(base_train: set[str], old_validation: set[str]) -> tuple[list[dict], dict]:
    source_dir = SOURCE / "jailbreakbench_artifacts_round17" / "attack-artifacts" / "JBC" / "manual"
    path = source_dir / "gpt-4-0125-preview.json"
    expected_hash = "1785f7cf838522461b5b9af3fa606715ecf55c194581f4c8c5c9f1945b59db05"
    if sha_file(path) != expected_hash:
        raise ValueError("JBB_MANUAL_FILE_HASH_MISMATCH")
    value = json.loads(path.read_text(encoding="utf-8"))
    counts: collections.Counter[str] = collections.Counter()
    selected: list[dict] = []
    seen: set[str] = set()
    for record in prompt_records(value):
        counts["prompt_occurrences"] += 1
        text = record["prompt"]
        if has_source_pii(text, "jbb"):
            counts["privacy_pattern"] += 1
            continue
        key = normalized(text)
        if key in base_train or key in old_validation:
            counts["overlap_round07"] += 1
            continue
        if key in seen:
            counts["within_source_duplicate"] += 1
            continue
        seen.add(key)
        ancestry = record.get("goal", record.get("behavior", ""))
        record_id = record.get("index", counts["prompt_occurrences"])
        add_candidate(selected, "jbb", text, "JBC/manual", f"gpt4_behavior_{record_id}", str(ancestry))
    if len(selected) != 100:
        raise ValueError(f"JBB_MANUAL_REPLAY_COUNT_MISMATCH:{len(selected)}")
    counts["selected_unique"] = len(selected)
    counts["distinct_behavior_keys"] = len({row["ancestry_key"] for row in selected})
    return selected, dict(sorted(counts.items()))


def source_identity(source_key: str) -> tuple[str, str, str]:
    spec = SOURCE_SPECS[source_key]
    return (spec["repository"], spec["revision"], spec["source_family_id"])


def metadata_row(candidate: dict, partition: str) -> tuple[dict, dict, dict]:
    spec = SOURCE_SPECS[candidate["source_key"]]
    text_hash = sha_bytes(candidate["text"].encode("utf-8"))
    row_id = "r18_" + stable_id(candidate["repository"], candidate["revision"], candidate["source_record_id"], text_hash)[:32]
    prompt_group = "pf_" + stable_id(candidate["source_key"], candidate["ancestry_key"])[:24]
    duplicate_group = "dg_" + stable_id(candidate["normalized"])[:24]
    row = {"id": row_id, "text": candidate["text"], "label": candidate["label"], "label_id": LABEL_IDS[candidate["label"]]}
    meta = {"id": row_id, "label": candidate["label"], "source_family_id": spec["source_family_id"],
            "collection_lineage_id": spec["collection_lineage_id"], "prompt_family_id": prompt_group,
            "duplicate_group_id": duplicate_group}
    prov = {"id": row_id, "source_repository_id": candidate["repository"], "source_revision": candidate["revision"],
            "upstream_split": candidate["upstream_split"], "source_record_id": candidate["source_record_id"],
            "source_family_id": spec["source_family_id"], "collection_lineage_id": spec["collection_lineage_id"],
            "prompt_family_id": prompt_group, "duplicate_group_id": duplicate_group,
            "native_label": candidate["native_label"], "mapping_rule_id": candidate["rule"],
            "language": "en", "partition": partition, "text_sha256": text_hash}
    return row, prov, meta


def ref(path: Path, package: Path) -> dict:
    return {"path": path.relative_to(package).as_posix(), "sha256": sha_file(path)}


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, values: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        for value in values:
            stream.write(json.dumps(value, ensure_ascii=False) + "\n")


def add_source_evidence(package: Path, source_key: str, sources: list[dict]) -> None:
    spec = SOURCE_SPECS[source_key]
    repository, revision, family_id = source_identity(source_key)
    evidence_refs = {}
    findings = {
        "rights": spec["rights"],
        "lineage": spec["lineage"],
        "privacy": spec["privacy"] + " " + spec["residual"],
    }
    for kind, finding in findings.items():
        record = {"source_repository_id": repository, "source_revision": revision, "finding": finding}
        if kind == "rights":
            record.update({"authorized_scope": "private_local_research_nonredistributive", "redistribution_allowed": False})
        path = package / "evidence" / "round18" / f"{source_key}_{kind}.json"
        write_json(path, record)
        evidence_refs[f"{kind}_evidence"] = ref(path, package)
    sources.append({
        "source_repository_id": repository,
        "source_revision": revision,
        "source_family_id": family_id,
        "rights_notice": spec["rights"],
        "license": spec["license"],
        "source_locator": spec["locator"],
        "privacy_method": spec["privacy"],
        "residual_limits": spec["residual"],
        "rights_status": "research_only",
        "rights_scope": "private_local_research_nonredistributive",
        "redistribution_allowed": False,
        "lineage_status": "verified",
        "privacy_status": "screened",
        "historical_locked_rows_excluded": True,
        **evidence_refs,
    })


def write_package(package_id: str, version: str, old_manifest: dict, old_split: dict,
                  old_review: dict, old_mapping: dict, old_status: dict,
                  old_rows: list[dict], old_prov: list[dict], train_candidates: list[dict],
                  validation_candidates: list[dict], include_dolly: bool,
                  build_counters: dict) -> dict:
    package = OUTPUT_ROOT / package_id
    if package.exists():
        raise FileExistsError(f"PACKAGE_ALREADY_EXISTS:{package}")
    package.mkdir(parents=True)
    shutil.copytree(ROUND07 / "evidence", package / "evidence", dirs_exist_ok=True)
    shutil.copy2(ROUND07 / "AUTONOMOUS_PROTOCOL.json", package / "AUTONOMOUS_PROTOCOL.json")

    train_rows = list(old_rows)
    train_prov = list(old_prov)
    train_meta = list(old_split["partitions"]["train"])
    if include_dolly:
        for item in train_candidates:
            row, prov, meta = metadata_row(item, "train")
            train_rows.append(row)
            train_prov.append(prov)
            train_meta.append(meta)
    val_rows, val_prov, val_meta = [], [], []
    for item in validation_candidates:
        row, prov, meta = metadata_row(item, "validation")
        val_rows.append(row)
        val_prov.append(prov)
        val_meta.append(meta)

    sources = list(old_review["sources"])
    for source_key in (("dolly",) if include_dolly else ()) + ("oasst", "llmail", "jbb"):
        add_source_evidence(package, source_key, sources)
    review = {"distribution_scope": "private_local_research_nonredistributive", "sources": sources}

    mapping = json.loads(json.dumps(old_mapping))
    for source_key in (("dolly",) if include_dolly else ()) + ("oasst", "llmail", "jbb"):
        spec = SOURCE_SPECS[source_key]
        mapping["rules"].append({"source_repository_id": spec["repository"], "native_label": spec["native"],
                                 "mapping_rule_id": spec["rule"], "label": spec["label"],
                                 "mapping_basis": f"Provisional, source-native/reference mapping for private L2 research only: {spec['residual']}"})

    split = {
        "schema": old_split["schema"],
        "frozen": True,
        "split_seed": old_split.get("split_seed"),
        "group_fields": old_split["group_fields"],
        "split_policy": "Round18 frozen train/validation protocol. Train is the immutable round07 train partition, optionally plus the pinned Dolly instruction-only benign cohort. Validation contains only held-out OASST1 benign, LLMail-Inject PI-attempt, and JBB JBC/manual JB-attempt sources. Round07 validation rows are excluded; old test payload is absent and only its family-level contract is copied.",
        "access": {"test_opened": False, "test_used_for_selection": False},
        "partitions": {"train": train_meta, "validation": val_meta, "test": old_split["partitions"]["test"]},
    }

    train_rows_path = package / "corpus" / "rows" / "train.jsonl"
    train_prov_path = package / "corpus" / "provenance" / "train.jsonl"
    val_rows_path = package / "corpus" / "rows" / "validation.jsonl"
    val_prov_path = package / "corpus" / "provenance" / "validation.jsonl"
    write_jsonl(train_rows_path, train_rows)
    write_jsonl(train_prov_path, train_prov)
    write_jsonl(val_rows_path, val_rows)
    write_jsonl(val_prov_path, val_prov)
    write_json(package / "split_manifest.json", split)
    write_json(package / "source_review.json", review)
    write_json(package / "label_mapping.json", mapping)

    manifest = {
        "package_id": package_id,
        "dataset_version": version,
        "schema": old_manifest["schema"],
        "language": "en",
        "label_status": LABEL_STATUS,
        "distribution_scope": "private_local_research_nonredistributive",
        "historical_locked_rows_excluded": True,
        "trainable": True,
        "unknown_rights_holds": 0,
        "baseline": old_manifest["baseline"],
        "lineage_packages": list(dict.fromkeys(old_manifest["lineage_packages"] + [
            f"{SOURCE_SPECS[key]['repository']}@{SOURCE_SPECS[key]['revision']}"
            for key in ((("dolly",) if include_dolly else ()) + ("oasst", "llmail", "jbb"))
        ])),
        "partitions": {
            "train": {"rows": ref(train_rows_path, package), "provenance": ref(train_prov_path, package)},
            "validation": {"rows": ref(val_rows_path, package), "provenance": ref(val_prov_path, package)},
            "test": {"sealed_contract": "split.partitions.test"},
        },
        "refs": {
            "protocol": ref(package / "AUTONOMOUS_PROTOCOL.json", package),
            "split": ref(package / "split_manifest.json", package),
            "source_review": ref(package / "source_review.json", package),
            "label_mapping": ref(package / "label_mapping.json", package),
        },
        "aggregate_counts": {
            "train": dict(sorted(collections.Counter(row["label"] for row in train_rows).items())),
            "validation": dict(sorted(collections.Counter(row["label"] for row in val_rows).items())),
            "test_contract_only": old_manifest["aggregate_counts"].get("test_contract_only", {}),
        },
        "build_notes": {
            "round18_source_audit_counters": build_counters,
            "formal_acceptance_gate": "GATE_UNSPECIFIED",
            "test_opened": False,
            "l3_run": False,
            "smoke_run": False,
        },
    }
    write_json(package / "DATASET_MANIFEST.json", manifest)
    status = {
        "package_id": package_id,
        "dataset_version": version,
        "schema": old_status["schema"],
        "language": "en",
        "trainable": True,
        "frozen_split": True,
        "distribution_scope": "private_local_research_nonredistributive",
        "l2_run": False,
        "l3_run": False,
        "test_opened": False,
        "formal_acceptance_gate": "GATE_UNSPECIFIED",
    }
    write_json(package / "STATUS.json", status)
    return {
        "package_id": package_id,
        "dataset_version": version,
        "path": str(package),
        "manifest_sha256": sha_file(package / "DATASET_MANIFEST.json"),
        "train_rows": len(train_rows),
        "validation_rows": len(val_rows),
        "train_counts": manifest["aggregate_counts"]["train"],
        "validation_counts": manifest["aggregate_counts"]["validation"],
        "train_source_families_per_label": {label: len({row["source_family_id"] for row in train_meta if row["label"] == label}) for label in LABEL_IDS},
        "validation_source_families_per_label": {label: len({row["source_family_id"] for row in val_meta if row["label"] == label}) for label in LABEL_IDS},
        "test_opened": False,
    }


def main() -> int:
    old_manifest, old_split, old_review, old_mapping, old_status, base_train, old_validation, old_rows, old_prov = load_package()
    dolly_rows, dolly_counts = candidates_dolly(base_train, old_validation)
    oasst_rows, oasst_counts = candidates_oasst(base_train, old_validation)
    llmail_rows, llmail_counts = candidates_llmail(base_train, old_validation)
    jbb_rows, jbb_counts = candidates_jbb(base_train, old_validation)

    validation_by_key: dict[str, list[dict]] = collections.defaultdict(list)
    for group in (oasst_rows, llmail_rows, jbb_rows):
        for item in group:
            validation_by_key[item["normalized"]].append(item)
    conflict_keys = {key for key, items in validation_by_key.items() if len({item["label"] for item in items}) > 1}
    val_seen: set[str] = set()
    validation_rows = []
    duplicate_val_source = collections.Counter()
    for group in (oasst_rows, llmail_rows, jbb_rows):
        for item in group:
            key = item["normalized"]
            if key in conflict_keys:
                duplicate_val_source["cross_source_label_conflict"] += 1
                continue
            if key in val_seen:
                duplicate_val_source["cross_source_duplicate_after_first"] += 1
                continue
            val_seen.add(key)
            validation_rows.append(item)
    if any(row["normalized"] in base_train or row["normalized"] in old_validation for row in validation_rows):
        raise ValueError("ROUND07_TEXT_OVERLAP_REMAINS_IN_VALIDATION")

    val_keys = {row["normalized"] for row in validation_rows}
    dolly_before = len(dolly_rows)
    dolly_rows = [row for row in dolly_rows if row["normalized"] not in val_keys]
    dolly_counts["overlap_new_validation_sources"] = dolly_before - len(dolly_rows)
    if not dolly_rows:
        raise ValueError("NO_DOLLY_TRAIN_ROWS_REMAIN")
    packages = [
        write_package(package_id, version, old_manifest, old_split, old_review, old_mapping, old_status,
                      old_rows, old_prov, dolly_rows, validation_rows, include_dolly, {
                          "dolly": dolly_counts if include_dolly else {"selected_unique": 0, "not_added_in_comparator": len(dolly_rows)},
                          "oasst": oasst_counts, "llmail": llmail_counts, "jbb_manual": jbb_counts,
                          "validation_cross_source": dict(sorted(duplicate_val_source.items())),
                          "validation_label_conflicts": len(conflict_keys),
                      })
        for (package_id, version), include_dolly in zip(PACKAGE_SPECS, (False, True))
    ]
    result = {
        "round": 18,
        "source_audits": {"dolly": dolly_counts, "oasst": oasst_counts, "llmail": llmail_counts,
                          "jbb_manual": jbb_counts, "validation_cross_source": dict(sorted(duplicate_val_source.items())),
                          "validation_label_conflicts": len(conflict_keys)},
        "packages": packages,
        "mapping_status": "native/reference mappings for exploratory private L2 research only; no curator-reviewed gold",
        "formal_acceptance_gate": "GATE_UNSPECIFIED",
        "test_opened": False,
        "l3_run": False,
        "smoke_run": False,
    }
    write_json(REPORT, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
