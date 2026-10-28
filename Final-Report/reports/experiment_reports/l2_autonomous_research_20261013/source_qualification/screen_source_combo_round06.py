#!/usr/bin/env python3
"""Aggregate-only train-shard screen for five pinned PI-Guard source families."""
from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import collections
import hashlib
import json
import numpy as np
import re
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

import pyarrow.parquet as pq
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

ROOT = Path(__file__).resolve().parent
PRIVATE = Path(r"D:\Work\Do-an\workspaces\truongnv\pi_guard_pipeline")
TRAINING = PRIVATE / "training_bases"
CIBERIA_DIR = TRAINING / "datasets" / "source_datasets" / "ciberia_promptrisk_candidate"
NEURAL_DIR = ROOT / "acquired"
WAMBO_DIR = TRAINING / "datasets" / "source_datasets" / "wambosec_prompt_injections_candidate"
TRUST_DIR = TRAINING / "datasets" / "source_datasets" / "trustairlab_in_the_wild_candidate_round05"
THREE_FILE = ROOT / "acquired" / "train.jsonl"
CIBERIA = CIBERIA_DIR / "data" / "train-00000-of-00001.parquet"
NEURAL = NEURAL_DIR / "neuralchemy_core_train.parquet"
WAMBO = WAMBO_DIR / "data" / "train-00000-of-00001.parquet"
TRUST_FILES = (
    TRUST_DIR / "data" / "jailbreak_2023_12_25" / "train-00000-of-00001.parquet",
    TRUST_DIR / "data" / "regular_2023_12_25" / "train-00000-of-00001.parquet",
)
VENDOR = PRIVATE / "training_bases" / "datasets" / "project_training" / "history" / "pi_guard_v8_english_diagnostic_20261012" / "tools" / "_vendor"
MODEL_SHA = "f4f4a2c3465ca1f081541037f9cac23021d68151c2f709c55ae5eedfca522963"
REVISION = {
    "ciberia": None,
    "neuralchemy_v1": None,
    "wambo": "071ee17a60112b7f9f808398156b430aadfaf1d2",
    "trustairlab_2023_12_25": "a10aab8eff1c73165a442d4464dce192bd28b9c5",
}
PI_CATEGORIES = {"direct_prompt_injection", "indirect_prompt_injection"}
NEURAL_PI_CATEGORIES = {"instruction_override", "prompt_injection"}
PATTERNS = {
    "email": re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"),
    "credential_assignment": re.compile(r"(?i)\b(?:api[_ -]?key|access[_ -]?token|password|passwd|secret)\s*[:=]\s*[^\s,;]+"),
    "ipv4": re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b"),
}


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def norm(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def pii_flags(text: str) -> list[str]:
    return [name for name, pattern in PATTERNS.items() if pattern.search(text)]


def main() -> int:
    c_audit = json.loads((CIBERIA_DIR / "CANDIDATE_AUDIT.json").read_text(encoding="utf-8"))
    n_audit = json.loads((NEURAL_DIR / "neuralchemy_core_train_manifest.json").read_text(encoding="utf-8"))
    t_manifest = json.loads((TRUST_DIR / "ACQUISITION_MANIFEST.json").read_text(encoding="utf-8"))
    three_manifest = json.loads((ROOT / "acquisition_manifest.json").read_text(encoding="utf-8"))
    w_review = (WAMBO_DIR / "SOURCE_REVIEW.md").read_text(encoding="utf-8")
    w_hash_match = re.search(r"Train payload SHA-256: `([0-9a-f]{64})`", w_review)
    if not w_hash_match:
        raise RuntimeError("Pinned Wambo train hash missing from source review")
    if sha(CIBERIA) != c_audit["candidate"]["sha256"]:
        raise RuntimeError("Pinned CiberIA train SHA-256 mismatch")
    if sha(NEURAL) != n_audit["sha256"]:
        raise RuntimeError("Pinned NeurAlchemy core/train SHA-256 mismatch")
    if sha(WAMBO) != w_hash_match.group(1):
        raise RuntimeError("Pinned Wambo train SHA-256 mismatch")
    if t_manifest.get("revision") != REVISION["trustairlab_2023_12_25"] or t_manifest.get("test_payload_opened") is not False:
        raise RuntimeError("TrustAIRLab acquisition is not the pinned train-only snapshot")
    if (three_manifest.get("dataset_id") != "3nesdeniz/agentic-prompt-injection-boundary-pairs"
            or three_manifest.get("revision") != "a5682e7573e1c7bc4b12e64d49c0dcd90ca776cf"
            or three_manifest.get("train_path") != "acquired/train.jsonl"
            or three_manifest.get("publisher_checksum_match") is not True
            or three_manifest.get("row_count") != 840
            or sha(THREE_FILE) != three_manifest.get("train_sha256")):
        raise RuntimeError("3nesdeniz pinned train-only acquisition mismatch")
    for relative, item in t_manifest["files"].items():
        source_path = TRUST_DIR / item["local_path"]
        if sha(source_path) != item["sha256"]:
            raise RuntimeError(f"TrustAIRLab pinned shard hash mismatch: {relative}")
    trust_rows_expected = {"jailbreak_2023_12_25": 1405, "regular_2023_12_25": 13735}
    for path in TRUST_FILES:
        if path.stem not in {"train-00000-of-00001"}:
            raise RuntimeError("Unexpected TrustAIRLab shard name")
        if pq.ParquetFile(path).metadata.num_rows != trust_rows_expected[path.parent.name]:
            raise RuntimeError(f"TrustAIRLab row count mismatch: {path.parent.name}")

    sys.path.insert(0, str(VENDOR))
    import py3langid
    from py3langid.langid import LanguageIdentifier, MODEL_FILE
    model_path = Path(py3langid.__file__).resolve().parent / MODEL_FILE
    if sha(model_path) != MODEL_SHA:
        raise RuntimeError("Pinned English model SHA-256 mismatch")
    identifier = LanguageIdentifier.from_model_file(MODEL_FILE, norm_probs=True)

    candidates: list[dict] = []
    by_source: dict[str, list[dict]] = collections.defaultdict(list)
    language_counts: dict[str, collections.Counter[str]] = collections.defaultdict(collections.Counter)
    mapped_counts: dict[str, collections.Counter[str]] = collections.defaultdict(collections.Counter)
    quarantine_counts: dict[str, collections.Counter[str]] = collections.defaultdict(collections.Counter)

    def add(source: str, text: str, label: str, identity: str, native_label: str, rule: str) -> None:
        language, confidence = identifier.classify(text.strip())
        language_counts[source][f"{language}@0.95={float(confidence) >= 0.95}"] += 1
        if language != "en" or float(confidence) < 0.95:
            quarantine_counts[source]["language_or_confidence"] += 1
            return
        flags = pii_flags(text)
        item = {"source": source, "text": text, "label": label, "identity": identity,
                "native_label": native_label, "mapping_rule_id": rule,
                "normalized_sha256": hashlib.sha256(norm(text).encode("utf-8")).hexdigest(),
                "pii_flags": flags}
        mapped_counts[source][label] += 1
        by_source[source].append(item)
        if flags:
            quarantine_counts[source]["privacy_pattern"] += 1
            return
        candidates.append(item)

    c_rows = pq.read_table(CIBERIA, columns=["text", "category", "class_name", "id", "split"]).to_pylist()
    for row in c_rows:
        if row["split"] != "train":
            raise RuntimeError("Non-train CiberIA row in pinned train shard")
        category, source_class = str(row["category"]), str(row["class_name"])
        if source_class == "BENIGN":
            label, rule = "benign", "ciberia_native_class_benign_v1"
        elif category in PI_CATEGORIES:
            label, rule = "PI", "ciberia_category_explicit_prompt_injection_v1"
        elif category == "jailbreak":
            label, rule = "JB", "ciberia_category_jailbreak_v1"
        else:
            quarantine_counts["ciberia"]["unmapped_category"] += 1
            continue
        add("ciberia", row["text"], label, str(row["id"]), f"{source_class}:{category}", rule)

    n_rows = pq.read_table(NEURAL, columns=["text", "category", "label", "source", "group_id"]).to_pylist()
    for row in n_rows:
        if row["source"] != "neuralchemy_v1":
            continue
        category, native = str(row["category"] or ""), str(row["label"])
        if category == "benign" and native == "0":
            label, rule = "benign", "neuralchemy_v1_native_benign_v1"
        elif category == "jailbreak" and native == "1":
            label, rule = "JB", "neuralchemy_v1_native_jailbreak_v1"
        elif category in NEURAL_PI_CATEGORIES and native == "1":
            label, rule = "PI", "neuralchemy_v1_explicit_pi_category_v1"
        else:
            quarantine_counts["neuralchemy_v1"]["unmapped_category"] += 1
            continue
        add("neuralchemy_v1", row["text"], label, str(row["group_id"]), f"{native}:{category}", rule)

    w_rows = pq.read_table(WAMBO, columns=["prompt", "label", "category"]).to_pylist()
    for index, row in enumerate(w_rows):
        native, category = str(row["label"]), str(row.get("category") or "").strip().casefold()
        if native == "0":
            label, rule = "benign", "wambo_native_label_0_benign_v1"
        elif native == "1" and "jailbreak" in category:
            label, rule = "JB", "wambo_category_jailbreak_v1"
        elif native == "1":
            label, rule = "PI", "wambo_native_malicious_non_jailbreak_reference_pi_v1"
        else:
            quarantine_counts["wambo"]["unexpected_native_label"] += 1
            continue
        add("wambo", row["prompt"], label, str(index), f"{native}:{category}", rule)

    trust_native_counts = collections.Counter()
    trust_identity = 0
    for path in TRUST_FILES:
        table = pq.read_table(path, columns=["prompt", "jailbreak"])
        for row in table.to_pylist():
            native = row["jailbreak"]
            if not isinstance(native, bool):
                raise RuntimeError("TrustAIRLab native jailbreak flag is not boolean")
            label = "JB" if native else "benign"
            trust_native_counts[str(native)] += 1
            family = "trustairlab_2023_12_25"
            identity = f"{path.parent.name}:{trust_identity}"
            trust_identity += 1
            add(family, row["prompt"], label, identity, str(native),
                "trustairlab_native_jailbreak_true_jb_false_benign_reference_v1")

    with THREE_FILE.open(encoding="utf-8") as stream:
        three_rows = [json.loads(line) for line in stream if line.strip()]
    if len(three_rows) != 840:
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
            quarantine_counts["3nesdeniz_agentic_boundary"]["unmapped_native_label_or_category"] += 1
            continue
        add("3nesdeniz_agentic_boundary", row["text"], label, str(row["id"]),
            f"{native}:{category}", rule)

    # Report raw mapped support, privacy exclusions, and the final post-filter support.
    all_sources = ("ciberia", "neuralchemy_v1", "trustairlab_2023_12_25", "3nesdeniz_agentic_boundary", "wambo")
    counts_by_source = {}
    clean_texts = {}
    for source in all_sources:
        raw = by_source[source]
        clean = [row for row in raw if not row["pii_flags"]]
        counts_by_source[source] = {
            "mapped_after_language_filter": dict(sorted(mapped_counts[source].items())),
            "rows_quarantined": dict(sorted(quarantine_counts[source].items())),
            "post_privacy_counts": dict(sorted(collections.Counter(row["label"] for row in clean).items())),
        }
        clean_texts[source] = [row["text"] for row in clean]

    exact_overlap = {}
    pairs = [(all_sources[i], all_sources[j]) for i in range(len(all_sources)) for j in range(i + 1, len(all_sources))]
    for first, second in pairs:
        left = {row["normalized_sha256"]: row["label"] for row in by_source[first] if not row["pii_flags"]}
        right = {row["normalized_sha256"]: row["label"] for row in by_source[second] if not row["pii_flags"]}
        common = set(left) & set(right)
        exact_overlap[f"{first}__{second}"] = {
            "shared_normalized_texts": len(common),
            "conflicting_reference_labels": sum(left[key] != right[key] for key in common),
        }

    all_clean_text = [text for source in all_sources for text in clean_texts[source]]
    vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), min_df=2,
                                 max_features=100_000, binary=True, dtype=np.float32)
    vectorizer.fit(all_clean_text)

    def near_summary(first: str, second: str) -> dict:
        left, right = clean_texts[first], clean_texts[second]
        matrix = vectorizer.transform(left + right)
        left_matrix, right_matrix = matrix[:len(left)], matrix[len(left):]
        forward = NearestNeighbors(n_neighbors=1, metric="cosine", algorithm="brute", n_jobs=-1).fit(right_matrix)
        reverse = NearestNeighbors(n_neighbors=1, metric="cosine", algorithm="brute", n_jobs=-1).fit(left_matrix)
        f = 1.0 - forward.kneighbors(left_matrix, return_distance=True)[0][:, 0]
        r = 1.0 - reverse.kneighbors(right_matrix, return_distance=True)[0][:, 0]
        return {"first_rows": len(left), "second_rows": len(right),
                "first_to_second_ge_0_90": int((f >= 0.90).sum()),
                "first_to_second_ge_0_95": int((f >= 0.95).sum()),
                "second_to_first_ge_0_90": int((r >= 0.90).sum()),
                "second_to_first_ge_0_95": int((r >= 0.95).sum()),
                "maximum_char_ngram_cosine": max(float(f.max()), float(r.max())) if len(f) and len(r) else None}

    train_sources = ("ciberia", "neuralchemy_v1", "trustairlab_2023_12_25", "3nesdeniz_agentic_boundary")
    validation_source = "wambo"
    split_boundary_pairs = [(source, validation_source) for source in train_sources]
    print("Checking char-ngram near duplicates across train/validation family boundary", flush=True)
    near_overlap = {f"{first}__{second}": near_summary(first, second)
                    for first, second in split_boundary_pairs}
    source_meta = {
        "ciberia": {"repository_id": c_audit["candidate"]["dataset_id"],
                    "revision": c_audit["candidate"]["revision"], "split_read": "train only",
                    "family_count": 1, "generation_lineage_limit": "model, prompt, and seed lineage not fully disclosed"},
        "neuralchemy_v1": {"repository_id": n_audit["dataset_id"], "revision": n_audit["revision"],
                           "split_read": "core/train only; source == neuralchemy_v1",
                           "family_count": 1, "component_license": "Apache-2.0 per publisher source table"},
        "trustairlab_2023_12_25": {"repository_id": t_manifest["repository_id"], "revision": t_manifest["revision"],
                                   "split_read": "jailbreak_2023_12_25/train and regular_2023_12_25/train only",
                                   "family_count": 1, "license_declared_by_publisher": t_manifest["license_declared_by_publisher"]},
        "3nesdeniz_agentic_boundary": {"repository_id": three_manifest["dataset_id"], "revision": three_manifest["revision"],
                                       "split_read": "train only; 840 rows; validation and test unopened",
                                       "family_count": 1, "license": three_manifest["license"],
                                       "lineage_limit": "Publisher labels the material synthetic and manually reviewed a stratified 180 of 600 pairs; generator model/prompt/seed and independent-review status are not established."},
        "wambo": {"repository_id": "wambosec/prompt-injections", "revision": REVISION["wambo"],
                  "split_read": "train only; designated internal validation family",
                  "family_count": 1, "generation_lineage_limit": "LLM model, prompt, and seed not disclosed"},
    }
    result = {
        "audit_id": "l2_l3_narrow_source_combo_train_only_screen_round06_v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "sources": source_meta,
        "source_roles": {"train_candidate_families": ["ciberia", "neuralchemy_v1", "trustairlab_2023_12_25", "3nesdeniz_agentic_boundary"],
                         "validation_candidate_family": "wambo"},
        "mapping_rules": {
            "ciberia": {"benign": "source class BENIGN", "PI": sorted(PI_CATEGORIES), "JB": "category == jailbreak", "otherwise": "quarantine"},
            "neuralchemy_v1": {"benign": "category benign with native label 0", "PI": sorted(NEURAL_PI_CATEGORIES), "JB": "category jailbreak with native label 1", "otherwise": "quarantine"},
            "trustairlab_2023_12_25": {"JB": "native jailbreak == true", "benign": "native jailbreak == false", "PI": "unsupported/not present"},
            "3nesdeniz_agentic_boundary": {"benign": "native target label 0 and category benign_boundary", "PI": "native binary task target label 1 and category prompt_injection; roleplay_jailbreak remains a source attack-family value, not a project JB label", "otherwise": "quarantine"},
            "wambo": {"benign": "native label 0", "JB": "native label 1 and category contains jailbreak", "PI": "native label 1 and category does not contain jailbreak; project reference mapping, not gold"},
        },
        "mapped_counts_by_source": counts_by_source,
        "trustair_native_counts": dict(sorted(trust_native_counts.items())),
        "language_filter": {"model_sha256": MODEL_SHA, "minimum_confidence": 0.95,
                             "counts": {source: dict(sorted(counts.items())) for source, counts in sorted(language_counts.items())}},
        "exact_normalized_overlap": exact_overlap,
        "near_duplicate_screen": {"method": "char_wb TF-IDF 3-5 gram cosine; all train-family to validation-family nearest pairs; text and pair identities not emitted",
                                  "thresholds": [0.90, 0.95], "counts": near_overlap},
        "privacy_patterns": sorted(PATTERNS),
        "privacy_screen_scope_limit": "Pattern screen only; not a guarantee that all personal or sensitive information is absent",
        "source_test_splits_opened_for_screen": False,
        "final_test_selected": False,
        "external_candidate_preview_exposure": {"dataset": "Horizon-Labs/prompt-injection-eval-suite",
                                                "configuration": "agentic5k_test",
                                                "source_family": "3nesdeniz_5k",
                                                "excluded_from_final_test_candidates": True},
        "prompt_text_emitted": False,
    }
    output = ROOT / "source_combo_screen_round06.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"result": "PASS_TRAIN_ONLY_SOURCE_SCREEN", "mapped_counts_by_source": counts_by_source,
                      "exact_overlap": exact_overlap, "near_overlap": near_overlap,
                      "test_payload_opened": False, "report": str(output)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
