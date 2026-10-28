#!/usr/bin/env python3
"""Train-only language, mapping, privacy and overlap screen for three pinned sources."""
from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import collections
import hashlib
import json
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
CIBERIA = CIBERIA_DIR / "data" / "train-00000-of-00001.parquet"
NEURAL = NEURAL_DIR / "neuralchemy_core_train.parquet"
WAMBO = WAMBO_DIR / "data" / "train-00000-of-00001.parquet"
VENDOR = PRIVATE / "training_bases" / "datasets" / "project_training" / "history" / "pi_guard_v8_english_diagnostic_20261012" / "tools" / "_vendor"
MODEL_SHA = "f4f4a2c3465ca1f081541037f9cac23021d68151c2f709c55ae5eedfca522963"
PI_CATEGORIES = {"direct_prompt_injection", "indirect_prompt_injection"}
NEURAL_PI_CATEGORIES = {"instruction_override", "prompt_injection"}
PATTERNS = {
    "email": re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"),
    "credential_assignment": re.compile(r"(?i)\b(?:api[_ -]?key|access[_ -]?token|password|passwd|secret)\s*[:=]\s*[^\s,;]+"),
    "ipv4": re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b"),
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def norm(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def pii_flags(text: str) -> list[str]:
    return [name for name, pattern in PATTERNS.items() if pattern.search(text)]


def row_record(source: str, text: str, label: str, identity: str) -> dict:
    normalized = norm(text)
    return {"source": source, "label": label, "identity": identity,
            "normalized_sha256": hashlib.sha256(normalized.encode("utf-8")).hexdigest(),
            "pii_flags": pii_flags(text)}


def main() -> int:
    c_audit = json.loads((CIBERIA_DIR / "CANDIDATE_AUDIT.json").read_text(encoding="utf-8"))
    n_audit = json.loads((NEURAL_DIR / "neuralchemy_core_train_manifest.json").read_text(encoding="utf-8"))
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

    sys.path.insert(0, str(VENDOR))
    import py3langid
    from py3langid.langid import LanguageIdentifier, MODEL_FILE
    model_path = Path(py3langid.__file__).resolve().parent / MODEL_FILE
    if sha(model_path) != MODEL_SHA:
        raise RuntimeError("Pinned English model SHA-256 mismatch")
    identifier = LanguageIdentifier.from_model_file(MODEL_FILE, norm_probs=True)

    candidates: list[dict] = []
    candidate_texts: dict[str, list[str]] = collections.defaultdict(list)
    language_counts: dict[str, collections.Counter[str]] = collections.defaultdict(collections.Counter)
    c_rows = pq.read_table(CIBERIA, columns=["text", "category", "class_name", "id", "split"]).to_pylist()
    for row in c_rows:
        if row["split"] != "train":
            raise RuntimeError("Non-train CiberIA row in pinned train shard")
        language, confidence = identifier.classify(row["text"].strip())
        language_counts["ciberia"][f"{language}@0.95={float(confidence) >= 0.95}"] += 1
        if language != "en" or float(confidence) < 0.95:
            continue
        category, source_class = str(row["category"]), str(row["class_name"])
        if source_class == "BENIGN":
            label = "benign"
        elif category in PI_CATEGORIES:
            label = "PI"
        elif category == "jailbreak":
            label = "JB"
        else:
            continue
        candidates.append(row_record("ciberia", row["text"], label, str(row["id"])))
        candidate_texts["ciberia"].append(row["text"])

    n_rows = pq.read_table(NEURAL, columns=["text", "category", "label", "source", "group_id"]).to_pylist()
    for row in n_rows:
        if row["source"] != "neuralchemy_v1":
            continue
        language, confidence = identifier.classify(row["text"].strip())
        language_counts["neuralchemy_v1"][f"{language}@0.95={float(confidence) >= 0.95}"] += 1
        if language != "en" or float(confidence) < 0.95:
            continue
        category = str(row["category"] or "")
        if category == "benign" and str(row["label"]) == "0":
            label = "benign"
        elif category == "jailbreak" and str(row["label"]) == "1":
            label = "JB"
        elif category in NEURAL_PI_CATEGORIES and str(row["label"]) == "1":
            label = "PI"
        else:
            continue
        candidates.append(row_record("neuralchemy_v1", row["text"], label, str(row["group_id"])))
        candidate_texts["neuralchemy_v1"].append(row["text"])

    validation: list[dict] = []
    validation_texts: list[str] = []
    w_rows = pq.read_table(WAMBO, columns=["prompt", "label", "category"]).to_pylist()
    w_category_counts: collections.Counter[str] = collections.Counter()
    for index, row in enumerate(w_rows):
        language, confidence = identifier.classify(row["prompt"].strip())
        language_counts["wambo"][f"{language}@0.95={float(confidence) >= 0.95}"] += 1
        if language != "en" or float(confidence) < 0.95:
            continue
        category = str(row.get("category") or "").strip().casefold()
        w_category_counts[category] += 1
        if str(row["label"]) == "0":
            label = "benign"
        elif "jailbreak" in category:
            label = "JB"
        elif str(row["label"]) == "1":
            label = "PI"
        else:
            raise RuntimeError("Unexpected Wambo native label")
        validation.append(row_record("wambo", row["prompt"], label, str(index)))
        validation_texts.append(row["prompt"])

    def summarize(rows: list[dict]) -> dict:
        counts = collections.Counter(row["label"] for row in rows)
        kept = [row for row in rows if not row["pii_flags"]]
        kept_counts = collections.Counter(row["label"] for row in kept)
        flagged = collections.Counter(flag for row in rows for flag in row["pii_flags"])
        return {"raw_mapped_rows": dict(sorted(counts.items())),
                "pattern_flagged_rows": sum(bool(row["pii_flags"]) for row in rows),
                "pattern_flag_counts_nonexclusive": dict(sorted(flagged.items())),
                "rows_after_pattern_quarantine": len(kept),
                "mapped_counts_after_pattern_quarantine": dict(sorted(kept_counts.items()))}

    by_source = {source: summarize([row for row in candidates if row["source"] == source])
                 for source in ("ciberia", "neuralchemy_v1")}
    by_source["wambo_validation"] = summarize(validation)
    hashes_by_source = {source: {row["normalized_sha256"] for row in rows}
                        for source, rows in (("ciberia", [r for r in candidates if r["source"] == "ciberia"]),
                                             ("neuralchemy_v1", [r for r in candidates if r["source"] == "neuralchemy_v1"]),
                                             ("wambo", validation))}
    overlaps = {}
    for first, second in (("ciberia", "neuralchemy_v1"), ("ciberia", "wambo"),
                          ("neuralchemy_v1", "wambo")):
        overlaps[f"{first}__{second}"] = len(hashes_by_source[first] & hashes_by_source[second])

    kept_texts = {
        "ciberia": [text for row, text in zip([r for r in candidates if r["source"] == "ciberia"], candidate_texts["ciberia"]) if not row["pii_flags"]],
        "neuralchemy_v1": [text for row, text in zip([r for r in candidates if r["source"] == "neuralchemy_v1"], candidate_texts["neuralchemy_v1"]) if not row["pii_flags"]],
        "wambo": [text for row, text in zip(validation, validation_texts) if not row["pii_flags"]],
    }
    all_clean_text = [text for source in kept_texts.values() for text in source]
    char_vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), min_df=2,
                                      max_features=100_000, binary=True, dtype="float32")
    char_vectorizer.fit(all_clean_text)

    def near_summary(first: str, second: str) -> dict:
        left, right = kept_texts[first], kept_texts[second]
        matrix = char_vectorizer.transform(left + right)
        left_matrix, right_matrix = matrix[:len(left)], matrix[len(left):]
        forward = NearestNeighbors(n_neighbors=1, metric="cosine", algorithm="brute", n_jobs=-1)
        forward.fit(right_matrix)
        forward_distances, _ = forward.kneighbors(left_matrix, return_distance=True)
        reverse = NearestNeighbors(n_neighbors=1, metric="cosine", algorithm="brute", n_jobs=-1)
        reverse.fit(left_matrix)
        reverse_distances, _ = reverse.kneighbors(right_matrix, return_distance=True)
        forward_best = 1.0 - forward_distances[:, 0]
        reverse_best = 1.0 - reverse_distances[:, 0]
        return {"first_source_rows": len(left), "second_source_rows": len(right),
                "first_to_second_nearest_ge_0_90": int((forward_best >= 0.90).sum()),
                "first_to_second_nearest_ge_0_95": int((forward_best >= 0.95).sum()),
                "second_to_first_nearest_ge_0_90": int((reverse_best >= 0.90).sum()),
                "second_to_first_nearest_ge_0_95": int((reverse_best >= 0.95).sum()),
                "maximum_char_ngram_cosine": max(float(forward_best.max()), float(reverse_best.max()))
                if len(forward_best) and len(reverse_best) else None}

    near_overlaps = {f"{first}__{second}": near_summary(first, second)
                     for first, second in (("ciberia", "neuralchemy_v1"),
                                           ("ciberia", "wambo"),
                                           ("neuralchemy_v1", "wambo"))}

    result = {
        "audit_id": "l2_narrow_source_combo_train_only_screen_round04_v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "sources": {
            "ciberia": {"repo_id": c_audit["candidate"]["dataset_id"], "revision": c_audit["candidate"]["revision"],
                        "split_read": "train only", "sha256": sha(CIBERIA), "family_count": 1,
                        "language_filter_model_sha256": MODEL_SHA},
            "neuralchemy_v1": {"repo_id": n_audit["dataset_id"], "revision": n_audit["revision"],
                               "split_read": "core/train only; source == neuralchemy_v1", "sha256": sha(NEURAL),
                               "family_count": 1},
            "wambo": {"repo_id": "wambosec/prompt-injections", "revision": "071ee17a60112b7f9f808398156b430aadfaf1d2",
                      "split_read": "train only", "sha256": sha(WAMBO), "family_count": 1,
                      "validation_label_rule": "label 0 => benign; label 1 with category containing jailbreak => JB; other label 1 => PI"},
        },
        "mapping_rules": {"ciberia": {"benign": "source class BENIGN", "PI": sorted(PI_CATEGORIES),
                                       "JB": "category == jailbreak", "otherwise": "quarantine"},
                          "neuralchemy_v1": {"benign": "category == benign and native label == 0",
                                             "PI": sorted(NEURAL_PI_CATEGORIES), "JB": "category == jailbreak and native label == 1",
                                             "otherwise": "quarantine"}},
        "mapped_rows_by_source": by_source,
        "language_filter": {"model_sha256": MODEL_SHA, "minimum_confidence": 0.95,
                             "counts": {source: dict(sorted(counts.items()))
                                        for source, counts in sorted(language_counts.items())}},
        "exact_normalized_train_overlap_counts": overlaps,
        "near_duplicate_screen": {"method": "char_wb TF-IDF 3-5 gram cosine; nearest cross-source row; thresholds 0.90 and 0.95",
                                  "text_emitted": False, "counts": near_overlaps},
        "wambo_jailbreak_tag_category_count": sum(n for category, n in w_category_counts.items() if "jailbreak" in category),
        "wambo_category_unique_count": len(w_category_counts),
        "source_test_splits_opened_for_screen": False,
        "final_test_selected": False,
        "external_candidate_preview_exposure": {"dataset": "Horizon-Labs/prompt-injection-eval-suite",
                                                "configuration": "agentic5k_test",
                                                "source_family": "3nesdeniz_5k",
                                                "excluded_from_final_test_candidates": True},
        "prompt_text_emitted": False,
    }
    output = ROOT / "source_combo_screen_round04.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"result": "PASS_TRAIN_ONLY_SOURCE_SCREEN", "mapped_rows_by_source": by_source,
                      "language_counts": result["language_filter"]["counts"],
                      "exact_overlaps": overlaps, "near_duplicate_screen": near_overlaps,
                      "source_test_splits_opened_for_screen": False,
                      "report": str(output)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
