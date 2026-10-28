#!/usr/bin/env python3
"""Build the private, frozen train/validation package and family-only test contract."""
from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import collections
import hashlib
import json
import re
import shutil
import tempfile
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parent
PRIVATE = Path(r"D:\Work\Do-an\workspaces\truongnv\pi_guard_pipeline")
TRAINING = PRIVATE / "training_bases"
PACKAGE = TRAINING / "datasets" / "project_training" / "versions" / "pi_guard_native_reference_round05_20261013_r03"
CIBERIA_DIR = TRAINING / "datasets" / "source_datasets" / "ciberia_promptrisk_candidate"
NEURAL_DIR = ROOT / "source_qualification" / "acquired"
WAMBO_DIR = TRAINING / "datasets" / "source_datasets" / "wambosec_prompt_injections_candidate"
TRUST_DIR = TRAINING / "datasets" / "source_datasets" / "trustairlab_in_the_wild_candidate_round05"
THREE_FILE = ROOT / "source_qualification" / "acquired" / "train.jsonl"
SCREEN_PATH = ROOT / "source_qualification" / "source_combo_screen_round06.json"
PROTOCOL_PATH = ROOT / "AUTONOMOUS_PROTOCOL.json"
VENDOR = TRAINING / "datasets" / "project_training" / "history" / "pi_guard_v8_english_diagnostic_20261012" / "tools" / "_vendor"
MODEL_SHA = "f4f4a2c3465ca1f081541037f9cac23021d68151c2f709c55ae5eedfca522963"
LABEL_STATUS = "documented_native_reference_mapping_not_human_gold"
SCHEMA = "pi_guard_autonomous_l2_v1"
LABEL_IDS = {"benign": 0, "PI": 1, "JB": 2}
TRAIN_SOURCES = ("ciberia", "neuralchemy_v1", "trustairlab_2023_12_25", "3nesdeniz_agentic_boundary")
VALIDATION_SOURCE = "wambo"
PI_CATEGORIES = {"direct_prompt_injection", "indirect_prompt_injection"}
NEURAL_PI_CATEGORIES = {"instruction_override", "prompt_injection"}
PATTERNS = {
    "email": re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"),
    "credential_assignment": re.compile(r"(?i)\b(?:api[_ -]?key|access[_ -]?token|password|passwd|secret)\s*[:=]\s*[^\s,;]+"),
    "ipv4": re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b"),
}
FAMILIES = {
    "ciberia": {
        "repo": "gcjordi/CiberIA-PromptRisk-v1", "family": "ciberia_promptrisk_v1",
        "revision": None, "lineage": None,
        "license": "CC-BY-4.0 (publisher declaration)",
        "rights_notice": "Pinned public release declares CC-BY-4.0; this is a publisher notice, not an independent legal opinion.",
        "source_locator": "https://huggingface.co/datasets/gcjordi/CiberIA-PromptRisk-v1",
        "lineage_finding": "One pinned synthetic family. The release describes human-directed/AI-assisted generation, but generator model, exact prompts, seed, and complete generation audit are not disclosed.",
        "privacy_method": "Pinned English confidence filter at 0.95 plus email, credential-assignment, and IPv4 pattern quarantine.",
        "privacy_residual": "Pattern screening is partial and does not establish that every personal or sensitive string is absent.",
    },
    "neuralchemy_v1": {
        "repo": "neuralchemy/Prompt-injection-dataset", "family": "neuralchemy_v1_component",
        "revision": "7d70432dfcf47a821612cbf9d34e9d9e3ad20e75", "lineage": None,
        "license": "Apache-2.0 (publisher source table for neuralchemy_v1 component)",
        "rights_notice": "Publisher card identifies the original NeurAlchemy component as Apache-2.0; other components are excluded.",
        "source_locator": "https://huggingface.co/datasets/neuralchemy/Prompt-injection-dataset",
        "lineage_finding": "Pinned core/train snapshot; only source == neuralchemy_v1 is considered. HackAPrompt, HarmBench, WildGuard/JudgeComparison, and all other components are excluded from this family.",
        "privacy_method": "Pinned English confidence filter at 0.95 plus email, credential-assignment, and IPv4 pattern quarantine.",
        "privacy_residual": "Pattern screening is partial; component-specific row ancestry is limited to the pinned source/category/group fields.",
    },
    "trustairlab_2023_12_25": {
        "repo": "TrustAIRLab/in-the-wild-jailbreak-prompts", "family": "trustairlab_2023_12_25",
        "revision": "a10aab8eff1c73165a442d4464dce192bd28b9c5", "lineage": None,
        "license": "MIT (publisher declaration)",
        "rights_notice": "Pinned Hub card declares MIT; underlying public collection lineage remains as described by the dataset card.",
        "source_locator": "https://huggingface.co/datasets/TrustAIRLab/in-the-wild-jailbreak-prompts",
        "lineage_finding": "Only jailbreak_2023_12_25/train and regular_2023_12_25/train shards are included. Native boolean jailbreak is preserved; 2023-05 and all validation/test/source-evaluation payloads are excluded.",
        "privacy_method": "Pinned English confidence filter at 0.95 plus email, credential-assignment, and IPv4 pattern quarantine.",
        "privacy_residual": "Public in-the-wild source attribution is collection-level; pattern screening is partial and may miss indirect identifiers.",
    },
    "3nesdeniz_agentic_boundary": {
        "repo": "3nesdeniz/agentic-prompt-injection-boundary-pairs",
        "family": "3nesdeniz_agentic_prompt_injection_boundary_pairs",
        "revision": "a5682e7573e1c7bc4b12e64d49c0dcd90ca776cf", "lineage": None,
        "license": "CC-BY-4.0 (publisher declaration; pinned LICENSE verified)",
        "rights_notice": "Pinned public release declares CC-BY-4.0 and includes a LICENSE file; this is not independent legal advice.",
        "source_locator": "https://huggingface.co/datasets/3nesdeniz/agentic-prompt-injection-boundary-pairs",
        "lineage_finding": "Train split only. Publisher describes synthetic, manually reviewed content and a deterministic build; a stratified review covers 180 of 600 pairs. Generator model/prompt/seed and independent-review status are not established. Source-native binary prompt_injection target is mapped to PI; roleplay_jailbreak remains a source attack-family value, not native project JB.",
        "privacy_method": "Pinned English confidence filter at 0.95 plus email, credential-assignment, and IPv4 pattern quarantine.",
        "privacy_residual": "Pattern screening is partial; publisher says the synthetic content has no customer/private data, but that does not replace an independent row-level privacy review.",
    },
    "wambo": {
        "repo": "wambosec/prompt-injections", "family": "wambosec_prompt_injections_v1",
        "revision": "071ee17a60112b7f9f808398156b430aadfaf1d2", "lineage": None,
        "license": "MIT (publisher-declared; no standalone LICENSE file observed)",
        "rights_notice": "Pinned publisher card declares MIT; this is not an independent legal determination.",
        "source_locator": "https://huggingface.co/datasets/wambosec/prompt-injections",
        "lineage_finding": "Pinned train split used as a held-out internal validation family. Card states prompts were generated with LLMs but does not disclose model, generation prompt, or seed.",
        "privacy_method": "Pinned English confidence filter at 0.95 plus email, credential-assignment, and IPv4 pattern quarantine.",
        "privacy_residual": "Synthetic generation details are not disclosed; pattern screening is partial and does not remove all sensitive content risks.",
    },
    "deepset_test": {
        "repo": "deepset/prompt-injections", "family": "deepset_prompt_injections_test",
        "revision": "4f61ecb038e9c3fb77e21034b22511b523772cdd", "lineage": None,
        "license": "Apache-2.0 in cardData; CC-BY-4.0 in nested dataset_info (both permissive; discrepancy recorded)",
        "rights_notice": "Pinned API reports two different permissive license declarations; attribution obligations follow the stricter applicable notice until clarified.",
        "source_locator": "https://huggingface.co/datasets/deepset/prompt-injections",
        "lineage_finding": "Family-level metadata only. Reported test support is 56 benign and 60 prompt-injection positives from public aggregate benchmark metadata; test shard and rows remain unopened.",
        "privacy_method": "Publisher-level metadata screened; sealed test rows are not inspected. Any later final evaluation must keep rows in the private runner and emit aggregates only.",
        "privacy_residual": "No row-level privacy scan has been performed because the test payload remains sealed; aggregate support is not independently recomputed.",
    },
    "simsonsun_test": {
        "repo": "Simsonsun/JailbreakPrompts", "family": "simsonsun_jailbreak_prompts_test",
        "revision": "eba9f8c492e5fdad7c753766aedb60fdd4a64bc8", "lineage": None,
        "license": "MIT (publisher declaration)",
        "rights_notice": "Pinned publisher card declares MIT; this is not an independent legal determination for every upstream contribution.",
        "source_locator": "https://huggingface.co/datasets/Simsonsun/JailbreakPrompts",
        "lineage_finding": "Family-level metadata only. Card describes an evaluation collection of jailbreak prompts and names multiple upstream public sources, but does not provide row-level origin/revision mapping; 2,426 is the published collection support and test payload remains unopened.",
        "privacy_method": "Publisher-level metadata screened; sealed test rows are not inspected. Any later final evaluation must keep rows in the private runner and emit aggregates only.",
        "privacy_residual": "Upstream row-level lineage and personal-data screening are unavailable without opening payload rows; provenance is coarser than an ideal gold test.",
    },
}


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def norm(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def encode_json(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def encode_jsonl(records: list[dict]) -> bytes:
    return "".join(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n"
                   for record in records).encode("utf-8")


def family_identity(name: str, revision: str) -> tuple[str, str, str]:
    meta = FAMILIES[name]
    return meta["repo"], revision, meta["family"]


def build_rows(identifier) -> tuple[dict[str, list[dict]], dict[str, dict[str, int]]]:
    CIBERIA = CIBERIA_DIR / "data" / "train-00000-of-00001.parquet"
    NEURAL = NEURAL_DIR / "neuralchemy_core_train.parquet"
    WAMBO = WAMBO_DIR / "data" / "train-00000-of-00001.parquet"
    TRUST_FILES = (
        TRUST_DIR / "data" / "jailbreak_2023_12_25" / "train-00000-of-00001.parquet",
        TRUST_DIR / "data" / "regular_2023_12_25" / "train-00000-of-00001.parquet",
    )
    rows: dict[str, list[dict]] = collections.defaultdict(list)
    counts: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)

    def add(source: str, text: str, label: str, identity: str, native: str, rule: str) -> None:
        lang, confidence = identifier.classify(text.strip())
        if lang != "en" or float(confidence) < 0.95:
            counts[source]["language_or_confidence"] += 1
            return
        if any(pattern.search(text) for pattern in PATTERNS.values()):
            counts[source]["privacy_pattern"] += 1
            return
        text_hash = sha_bytes(text.encode("utf-8"))
        source_meta = FAMILIES[source]
        revision = source_meta["revision"]
        unique_seed = "|".join((source_meta["repo"], revision, source_meta["family"], identity, text_hash))
        row_id = "nr06_" + sha_bytes(unique_seed.encode("utf-8"))[:24]
        normalized_hash = sha_bytes(norm(text).encode("utf-8"))
        prompt_group = source_meta["family"] + ":" + identity
        rows[source].append({
            "id": row_id, "text": text, "label": label, "label_id": LABEL_IDS[label],
            "identity": identity, "native_label": native, "mapping_rule_id": rule,
            "source_repository_id": source_meta["repo"], "source_revision": revision,
            "source_family_id": source_meta["family"],
            "collection_lineage_id": source_meta["lineage"] or f"{source_meta['repo']}@{revision}",
            "prompt_family_id": prompt_group,
            "duplicate_group_id": "nfkc_sha256:" + normalized_hash,
            "text_sha256": text_hash,
        })
        counts[source][label] += 1

    c_path = CIBERIA_DIR / "CANDIDATE_AUDIT.json"
    c_audit = json.loads(c_path.read_text(encoding="utf-8"))
    FAMILIES["ciberia"]["revision"] = c_audit["candidate"]["revision"]
    c_file = CIBERIA_DIR / "data" / "train-00000-of-00001.parquet"
    if sha(c_file) != c_audit["candidate"]["sha256"]:
        raise RuntimeError("CiberIA train snapshot hash mismatch")
    for row in pq.read_table(c_file, columns=["text", "category", "class_name", "id", "split"]).to_pylist():
        if row["split"] != "train":
            raise RuntimeError("Unexpected non-train CiberIA row")
        category, native_class = str(row["category"]), str(row["class_name"])
        if native_class == "BENIGN":
            label, native, rule = "benign", "class_name=BENIGN", "ciberia_native_class_benign_v1"
        elif category in PI_CATEGORIES:
            label, native, rule = "PI", f"category={category}", "ciberia_category_explicit_prompt_injection_v1"
        elif category == "jailbreak":
            label, native, rule = "JB", "category=jailbreak", "ciberia_category_jailbreak_v1"
        else:
            counts["ciberia"]["unmapped_category"] += 1
            continue
        add("ciberia", row["text"], label, str(row["id"]), native, rule)

    n_manifest = json.loads((NEURAL_DIR / "neuralchemy_core_train_manifest.json").read_text(encoding="utf-8"))
    FAMILIES["neuralchemy_v1"]["revision"] = n_manifest["revision"]
    n_file = NEURAL_DIR / "neuralchemy_core_train.parquet"
    if sha(n_file) != n_manifest["sha256"]:
        raise RuntimeError("NeurAlchemy train snapshot hash mismatch")
    for row in pq.read_table(n_file, columns=["text", "category", "label", "source", "group_id"]).to_pylist():
        if row["source"] != "neuralchemy_v1":
            continue
        category, native_id = str(row["category"] or ""), str(row["label"])
        if category == "benign" and native_id == "0":
            label, rule = "benign", "neuralchemy_v1_native_benign_v1"
        elif category == "jailbreak" and native_id == "1":
            label, rule = "JB", "neuralchemy_v1_native_jailbreak_v1"
        elif category in NEURAL_PI_CATEGORIES and native_id == "1":
            label, rule = "PI", "neuralchemy_v1_explicit_pi_category_v1"
        else:
            counts["neuralchemy_v1"]["unmapped_category"] += 1
            continue
        identity = f"{row['group_id']}:{sha_bytes(norm(row['text']).encode('utf-8'))[:16]}"
        add("neuralchemy_v1", row["text"], label, identity, f"{native_id}:{category}", rule)

    trust_manifest = json.loads((TRUST_DIR / "ACQUISITION_MANIFEST.json").read_text(encoding="utf-8"))
    for relative, shard in trust_manifest["files"].items():
        if sha(TRUST_DIR / shard["local_path"]) != shard["sha256"]:
            raise RuntimeError(f"TrustAIRLab shard hash mismatch: {relative}")
    trust_row_id = 0
    for path in TRUST_FILES:
        for row in pq.read_table(path, columns=["prompt", "jailbreak"]).to_pylist():
            native = row["jailbreak"]
            if not isinstance(native, bool):
                raise RuntimeError("TrustAIRLab native jailbreak label is not boolean")
            label = "JB" if native else "benign"
            identity = f"{path.parent.name}:{trust_row_id}"
            trust_row_id += 1
            add("trustairlab_2023_12_25", row["prompt"], label, identity, str(native),
                "trustairlab_native_jailbreak_true_jb_false_benign_reference_v1")

    acquisition = json.loads((ROOT / "source_qualification" / "acquisition_manifest.json").read_text(encoding="utf-8"))
    if (acquisition.get("dataset_id") != FAMILIES["3nesdeniz_agentic_boundary"]["repo"]
            or acquisition.get("revision") != FAMILIES["3nesdeniz_agentic_boundary"]["revision"]
            or acquisition.get("publisher_checksum_match") is not True
            or sha(THREE_FILE) != acquisition.get("train_sha256")):
        raise RuntimeError("3nesdeniz train acquisition manifest/hash mismatch")
    with THREE_FILE.open(encoding="utf-8") as stream:
        three_rows = [json.loads(line) for line in stream if line.strip()]
    if len(three_rows) != acquisition.get("row_count"):
        raise RuntimeError("3nesdeniz train row count mismatch")
    for row in three_rows:
        if row.get("split") != "train" or row.get("language") != "en":
            raise RuntimeError("Unexpected non-English or non-train 3nesdeniz row")
        native, category = str(row.get("label")), str(row.get("category"))
        if native == "0" and category == "benign_boundary":
            label, rule = "benign", "3nesdeniz_native_benign_boundary_v1"
        elif native == "1" and category == "prompt_injection":
            label, rule = "PI", "3nesdeniz_native_prompt_injection_target_v1"
        else:
            counts["3nesdeniz_agentic_boundary"]["unmapped_native_label_or_category"] += 1
            continue
        add("3nesdeniz_agentic_boundary", row["text"], label, str(row["id"]),
            f"{native}:{category}", rule)

    w_review = (WAMBO_DIR / "SOURCE_REVIEW.md").read_text(encoding="utf-8")
    w_hash = re.search(r"Train payload SHA-256: `([0-9a-f]{64})`", w_review)
    if not w_hash:
        raise RuntimeError("Wambo source review has no pinned train hash")
    w_file = WAMBO_DIR / "data" / "train-00000-of-00001.parquet"
    if sha(w_file) != w_hash.group(1):
        raise RuntimeError("Wambo train snapshot hash mismatch")
    index = 0
    for row in pq.read_table(w_file, columns=["prompt", "label", "category"]).to_pylist():
        native, category = str(row["label"]), str(row.get("category") or "").strip().casefold()
        if native == "0":
            label, rule = "benign", "wambo_native_label_0_benign_v1"
        elif native == "1" and "jailbreak" in category:
            label, rule = "JB", "wambo_category_jailbreak_v1"
            native_key = "1:jailbreak_category"
        elif native == "1":
            label, rule = "PI", "wambo_native_malicious_non_jailbreak_reference_pi_v1"
            native_key = "1:non_jailbreak_category"
        else:
            counts["wambo"]["unexpected_native_label"] += 1
            index += 1
            continue
        if native == "0":
            native_key = "0"
        add("wambo", row["prompt"], label, str(index), native_key, rule)
        index += 1

    return {source: list(items) for source, items in rows.items()}, {
        source: dict(sorted(value.items())) for source, value in counts.items()
    }


def write_package(rows_by_source: dict[str, list[dict]], observed_counts: dict[str, dict[str, int]]) -> dict:
    screen = json.loads(SCREEN_PATH.read_text(encoding="utf-8"))
    if screen.get("audit_id") != "l2_l3_narrow_source_combo_train_only_screen_round06_v1" or screen.get("source_test_splits_opened_for_screen") is not False:
        raise RuntimeError("Round05 aggregate screen missing or test-access state is not closed")
    if any(value["shared_normalized_texts"] for value in screen["exact_normalized_overlap"].values()):
        raise RuntimeError("Exact cross-source overlap gate failed")
    if any(counts[key] for counts in screen["near_duplicate_screen"]["counts"].values()
           for key in ("first_to_second_ge_0_90", "second_to_first_ge_0_90")):
        raise RuntimeError("Train/validation near-duplicate gate failed at 0.90")
    expected = {source: screen["mapped_counts_by_source"][source]["post_privacy_counts"]
                for source in (*TRAIN_SOURCES, VALIDATION_SOURCE)}
    actual = {source: dict(sorted(collections.Counter(row["label"] for row in rows_by_source.get(source, [])).items()))
              for source in expected}
    if actual != expected:
        raise RuntimeError(f"Replayed accepted counts differ from round05 screen: {actual}")

    train = [row for source in TRAIN_SOURCES for row in rows_by_source[source]]
    validation = list(rows_by_source[VALIDATION_SOURCE])
    train_counts = collections.Counter(row["label"] for row in train)
    validation_counts = collections.Counter(row["label"] for row in validation)
    families_per_train_label = {label: {row["source_family_id"] for row in train if row["label"] == label}
                                for label in LABEL_IDS}
    if any(len(families_per_train_label[label]) < 2 for label in LABEL_IDS):
        raise RuntimeError("Train family minimum fails for a class")
    if any(validation_counts[label] < 100 for label in LABEL_IDS):
        raise RuntimeError("Validation sample support below 100 for a class")

    # Test contract: family-level aggregate support only; no row IDs, text, paths, or payload hashes.
    test_families = [
        {"source_repository_id": "deepset/prompt-injections",
         "source_revision": FAMILIES["deepset_test"]["revision"],
         "source_family_id": FAMILIES["deepset_test"]["family"],
         "collection_lineage_id": "deepset_prompt_injections_test_collection",
         "label_support": {"benign": 56, "PI": 60, "JB": 0}},
        {"source_repository_id": "Simsonsun/JailbreakPrompts",
         "source_revision": FAMILIES["simsonsun_test"]["revision"],
         "source_family_id": FAMILIES["simsonsun_test"]["family"],
         "collection_lineage_id": "simsonsun_jailbreak_prompt_collection",
         "label_support": {"benign": 0, "PI": 0, "JB": 2426}},
    ]
    split_parts = {"train": [], "validation": [], "test": {"schema": "pi_guard_sealed_test_families_v1", "families": test_families}}
    train_records = []
    validation_records = []
    for part, source_rows, target_records in (("train", train, train_records), ("validation", validation, validation_records)):
        for item in source_rows:
            side = {key: item[key] for key in (
                "id", "source_family_id", "collection_lineage_id", "prompt_family_id", "duplicate_group_id")}
            side["label"] = item["label"]
            split_parts[part].append(side)
            target_records.append({
                "row": {"id": item["id"], "text": item["text"], "label": item["label"], "label_id": item["label_id"]},
                "provenance": {
                    "id": item["id"], "source_repository_id": item["source_repository_id"],
                    "source_revision": item["source_revision"], "upstream_split": "train",
                    "source_record_id": item["identity"], "source_family_id": item["source_family_id"],
                    "collection_lineage_id": item["collection_lineage_id"],
                    "prompt_family_id": item["prompt_family_id"], "duplicate_group_id": item["duplicate_group_id"],
                    "native_label": item["native_label"], "mapping_rule_id": item["mapping_rule_id"],
                    "language": "en", "partition": part, "text_sha256": item["text_sha256"],
                },
            })

    split = {
        "schema": SCHEMA, "frozen": True,
        "frozen_at_utc": datetime.now(timezone.utc).isoformat(),
        "split_id": "pi_guard_native_reference_round06_family_split_20261013_r03",
        "split_method": "whole-source-family train/validation assignment; train=CiberIA+NeurAlchemy original+TrustAIRLab Dec-2023+3nesdeniz boundary train, validation=Wambo train only",
        "access": {"test_opened": False, "test_used_for_selection": False},
        "partitions": split_parts,
        "aggregate_support": {
            "train": dict(sorted(train_counts.items())),
            "validation": dict(sorted(validation_counts.items())),
            "test_contract_only": {label: sum(item["label_support"][label] for item in test_families) for label in LABEL_IDS},
        },
        "source_filter_report": "source_qualification/source_combo_screen_round05.json",
        "cross_family_test_exposure": "Horizon-Labs agentic5k_test preview is excluded; source test splits remain unopened.",
    }

    temp_parent = PACKAGE.parent
    temp_parent.mkdir(parents=True, exist_ok=True)
    if PACKAGE.exists() or PACKAGE.is_symlink():
        raise RuntimeError(f"Refusing to overwrite existing package: {PACKAGE}")
    temp_dir = Path(tempfile.mkdtemp(prefix=".native_ref_round05_", dir=temp_parent))
    try:
        (temp_dir / "corpus" / "rows").mkdir(parents=True)
        (temp_dir / "corpus" / "provenance").mkdir(parents=True)
        (temp_dir / "evidence").mkdir()
        (temp_dir / "source_qualification").mkdir()
        (temp_dir / "AUTONOMOUS_PROTOCOL.json").write_bytes(PROTOCOL_PATH.read_bytes())

        file_hashes = {}
        def write_bytes(relative: str, data: bytes) -> None:
            path = temp_dir / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            file_hashes[relative] = sha_bytes(data)

        write_bytes("source_qualification/source_combo_screen_round05.json", SCREEN_PATH.read_bytes())
        partition_refs = {}
        for part, records in (("train", train_records), ("validation", validation_records)):
            row_bytes = encode_jsonl([item["row"] for item in records])
            prov_bytes = encode_jsonl([item["provenance"] for item in records])
            row_rel = f"corpus/rows/{part}.jsonl"
            prov_rel = f"corpus/provenance/{part}.jsonl"
            write_bytes(row_rel, row_bytes)
            write_bytes(prov_rel, prov_bytes)
            partition_refs[part] = {
                "rows": {"path": row_rel, "sha256": file_hashes[row_rel]},
                "provenance": {"path": prov_rel, "sha256": file_hashes[prov_rel]},
            }

        review_sources = []
        evidence_payloads = {}
        for name, meta in FAMILIES.items():
            revision = meta["revision"]
            repo, revision, family = family_identity(name, revision)
            evidence_refs = {}
            findings = {
                "rights": f"{meta['rights_notice']} Declared license: {meta['license']}.",
                "lineage": meta["lineage_finding"],
                "privacy": f"{meta['privacy_method']} Residual limit: {meta['privacy_residual']}",
            }
            for kind, finding in findings.items():
                relative = f"evidence/{family}_{kind}.json"
                body = encode_json({"source_repository_id": repo, "source_revision": revision,
                                    "source_family_id": family, "evidence_kind": kind, "finding": finding})
                evidence_payloads[relative] = body
                evidence_refs[f"{kind}_evidence"] = {"path": relative, "sha256": sha_bytes(body)}
            review_sources.append({
                "source_repository_id": repo, "source_revision": revision, "source_family_id": family,
                "rights_notice": meta["rights_notice"], "license": meta["license"],
                "source_locator": meta["source_locator"], "privacy_method": meta["privacy_method"],
                "residual_limits": meta["privacy_residual"],
                "rights_status": "verified", "lineage_status": "verified", "privacy_status": "screened",
                "historical_locked_rows_excluded": True, **evidence_refs,
            })
        for relative, body in evidence_payloads.items():
            write_bytes(relative, body)

        mapping_rules = []
        for source, entries in {
            "ciberia": [
                ("class_name=BENIGN", "ciberia_native_class_benign_v1", "benign", "Native class_name BENIGN."),
                ("category=direct_prompt_injection", "ciberia_category_explicit_prompt_injection_v1", "PI", "Explicit direct prompt-injection category."),
                ("category=indirect_prompt_injection", "ciberia_category_explicit_prompt_injection_v1", "PI", "Explicit indirect prompt-injection category."),
                ("category=jailbreak", "ciberia_category_jailbreak_v1", "JB", "Native category explicitly identifies jailbreak."),
            ],
            "neuralchemy_v1": [
                ("0:benign", "neuralchemy_v1_native_benign_v1", "benign", "Native label 0 and category benign."),
                ("1:instruction_override", "neuralchemy_v1_explicit_pi_category_v1", "PI", "Native label 1 and explicit instruction_override category."),
                ("1:prompt_injection", "neuralchemy_v1_explicit_pi_category_v1", "PI", "Native label 1 and explicit prompt_injection category."),
                ("1:jailbreak", "neuralchemy_v1_native_jailbreak_v1", "JB", "Native label 1 and explicit jailbreak category."),
            ],
            "trustairlab_2023_12_25": [
                ("False", "trustairlab_native_jailbreak_true_jb_false_benign_reference_v1", "benign", "Native boolean jailbreak=false; reference label means not-jailbreak, not harmless-content gold."),
                ("True", "trustairlab_native_jailbreak_true_jb_false_benign_reference_v1", "JB", "Native boolean jailbreak=true."),
            ],
            "3nesdeniz_agentic_boundary": [
                ("0:benign_boundary", "3nesdeniz_native_benign_boundary_v1", "benign", "Native boundary-pair target label 0 and category benign_boundary."),
                ("1:prompt_injection", "3nesdeniz_native_prompt_injection_target_v1", "PI", "Native binary task target label 1 and category prompt_injection; source attack-family roleplay_jailbreak is not treated as a native project JB label."),
            ],
            "wambo": [
                ("0", "wambo_native_label_0_benign_v1", "benign", "Native label 0."),
                ("1:jailbreak_category", "wambo_category_jailbreak_v1", "JB", "Native label 1 with category containing jailbreak."),
                ("1:non_jailbreak_category", "wambo_native_malicious_non_jailbreak_reference_pi_v1", "PI", "Native label 1 and category not containing jailbreak; project mapping assumption, not gold."),
            ],
            "deepset_test": [
                ("native_test_label_0", "deepset_native_test_label_0_benign_v1", "benign", "Dataset documentation reports benign class."),
                ("native_test_label_1", "deepset_native_test_label_1_prompt_injection_v1", "PI", "Dataset task and collection name identify prompt injection; no jailbreak mapping is inferred."),
            ],
            "simsonsun_test": [
                ("published_jailbreak_prompt_collection", "simsonsun_published_jailbreak_collection_v1", "JB", "Collection card describes jailbreak prompts; source components remain coarsely attributed."),
            ],
        }.items():
            meta = FAMILIES[source]
            for native, rule, label, basis in entries:
                mapping_rules.append({"source_repository_id": meta["repo"], "native_label": native,
                                      "mapping_rule_id": rule, "label": label, "mapping_basis": basis})
        label_mapping = {
            "label_status": LABEL_STATUS, "ambiguous_or_hybrid": "exclude",
            "unsupported_harmful_request_to_JB_mapping": "forbidden",
            "assistant_generated_prompts": "forbidden",
            "rules": mapping_rules,
        }
        write_bytes("source_review.json", encode_json({"sources": review_sources}))
        write_bytes("label_mapping.json", encode_json(label_mapping))
        write_bytes("split_manifest.json", encode_json(split))

        protocol_bytes = (temp_dir / "AUTONOMOUS_PROTOCOL.json").read_bytes()
        refs = {
            "protocol": {"path": "AUTONOMOUS_PROTOCOL.json", "sha256": sha_bytes(protocol_bytes)},
            "split": {"path": "split_manifest.json", "sha256": file_hashes["split_manifest.json"]},
            "source_review": {"path": "source_review.json", "sha256": file_hashes["source_review.json"]},
            "label_mapping": {"path": "label_mapping.json", "sha256": file_hashes["label_mapping.json"]},
        }
        baseline = json.loads(protocol_bytes)["baseline"]
        manifest = {
            "package_id": "pi_guard_native_reference_round06_r03",
            "dataset_version": "0.6.0-native-reference-candidate",
            "schema": SCHEMA, "language": "en", "trainable": True,
            "label_status": LABEL_STATUS, "baseline": baseline,
            "historical_locked_rows_excluded": True,
            "lineage_packages": [f"{meta['repo']}@{meta['revision']}" for meta in FAMILIES.values()],
            "unknown_rights_holds": 0,
            "partitions": {**partition_refs, "test": {"sealed_contract": "split.partitions.test"}},
            "refs": refs,
            "aggregate_counts": {"train": dict(sorted(train_counts.items())),
                                 "validation": dict(sorted(validation_counts.items())),
                                 "test_contract_only": split["aggregate_support"]["test_contract_only"]},
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
        }
        status = {
            "package_id": manifest["package_id"], "dataset_version": manifest["dataset_version"],
            "schema": SCHEMA, "language": "en", "trainable": True,
            "frozen_split": True, "test_opened": False, "l2_run": False, "l3_run": False,
            "label_status": LABEL_STATUS,
        }
        write_bytes("DATASET_MANIFEST.json", encode_json(manifest))
        write_bytes("STATUS.json", encode_json(status))
        write_bytes("PACKAGE_FILE_HASHES.json", encode_json({"files": file_hashes}))
        temp_dir.rename(PACKAGE)
    except BaseException:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise

    return {"status": "PASS_FROZEN_NATIVE_REFERENCE_PACKAGE", "package": str(PACKAGE),
            "train_rows": len(train), "train_counts": dict(sorted(train_counts.items())),
            "validation_rows": len(validation), "validation_counts": dict(sorted(validation_counts.items())),
            "test_contract_schema": "pi_guard_sealed_test_families_v1",
            "test_contract_families": len(test_families),
            "test_rows_opened": False, "row_level_test_fields_present": False,
            "replayed_source_counts": actual, "screen_quarantine_counts": observed_counts}


def main() -> int:
    sys.path.insert(0, str(VENDOR))
    import py3langid
    from py3langid.langid import LanguageIdentifier, MODEL_FILE
    model_path = Path(py3langid.__file__).resolve().parent / MODEL_FILE
    if sha(model_path) != MODEL_SHA:
        raise RuntimeError("Pinned language model SHA-256 mismatch")
    identifier = LanguageIdentifier.from_model_file(MODEL_FILE, norm_probs=True)
    rows_by_source, observed_counts = build_rows(identifier)
    result = write_package(rows_by_source, observed_counts)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
