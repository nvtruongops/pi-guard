#!/usr/bin/env python3
"""Train-only aggregate screen for a narrow CiberIA/NeurAlchemy/Wambo mapping."""
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
    c_rows = pq.read_table(CIBERIA, columns=["text", "category", "class_name", "id", "split"]).to_pylist()
    for row in c_rows:
        if row["split"] != "train":
            raise RuntimeError("Non-train CiberIA row in pinned train shard")
        language, confidence = identifier.classify(row["text"].strip())
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

    n_rows = pq.read_table(NEURAL, columns=["text", "category", "label", "source", "group_id"]).to_pylist()
    for row in n_rows:
        if row["source"] != "neuralchemy_v1":
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

    validation: list[dict] = []
    w_rows = pq.read_table(WAMBO, columns=["prompt", "label", "category"]).to_pylist()
    w_category_counts: collections.Counter[str] = collections.Counter()
    for index, row in enumerate(w_rows):
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

    result = {
        "audit_id": "l2_narrow_source_combo_train_only_screen_round03_v1",
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
        "exact_normalized_train_overlap_counts": overlaps,
        "wambo_jailbreak_tag_category_count": sum(n for category, n in w_category_counts.items() if "jailbreak" in category),
        "wambo_category_unique_count": len(w_category_counts),
        "test_opened": False,
        "prompt_text_emitted": False,
    }
    output = ROOT / "source_combo_screen_round03.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"result": "PASS_TRAIN_ONLY_SOURCE_SCREEN", "mapped_rows_by_source": by_source,
                      "exact_overlaps": overlaps, "test_opened": False, "report": str(output)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
