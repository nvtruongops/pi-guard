#!/usr/bin/env python3
"""Aggregate-only English and native-category screen for the pinned CiberIA train shard."""
from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import collections
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parent
PRIVATE = Path(r"D:\Work\Do-an\workspaces\truongnv\pi_guard_pipeline")
SOURCE = PRIVATE / "training_bases" / "datasets" / "source_datasets" / "ciberia_promptrisk_candidate"
TRAIN = SOURCE / "data" / "train-00000-of-00001.parquet"
AUDIT = SOURCE / "CANDIDATE_AUDIT.json"
VENDOR = PRIVATE / "training_bases" / "datasets" / "project_training" / "history" / "pi_guard_v8_english_diagnostic_20261012" / "tools" / "_vendor"
EXPECTED_MODEL_SHA256 = "f4f4a2c3465ca1f081541037f9cac23021d68151c2f709c55ae5eedfca522963"
PI_CATEGORIES = {"direct_prompt_injection", "indirect_prompt_injection"}


def main() -> int:
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    source_sha = hashlib.sha256(TRAIN.read_bytes()).hexdigest()
    if source_sha != audit["candidate"]["sha256"]:
        raise RuntimeError("Pinned CiberIA train SHA-256 mismatch")

    sys.path.insert(0, str(VENDOR))
    import py3langid
    from py3langid.langid import LanguageIdentifier, MODEL_FILE

    model_path = Path(py3langid.__file__).resolve().parent / MODEL_FILE
    model_sha = hashlib.sha256(model_path.read_bytes()).hexdigest()
    if model_sha != EXPECTED_MODEL_SHA256:
        raise RuntimeError("Pinned py3langid model SHA-256 mismatch")
    identifier = LanguageIdentifier.from_model_file(MODEL_FILE, norm_probs=True)

    rows = pq.read_table(TRAIN, columns=["text", "language", "category", "class_name", "split"]).to_pylist()
    if len(rows) != audit["candidate"]["rows"] or any(row["split"] != "train" for row in rows):
        raise RuntimeError("Unexpected CiberIA split or row count")

    language_counts: collections.Counter[tuple[str, str]] = collections.Counter()
    mapped_counts: collections.Counter[str] = collections.Counter()
    category_counts: collections.Counter[tuple[str, str, str]] = collections.Counter()
    for row in rows:
        predicted, confidence = identifier.classify(row["text"].strip())
        accepted = predicted == "en" and float(confidence) >= 0.95
        language_counts[(predicted, "accepted_en" if accepted else "excluded")] += 1
        if not accepted:
            continue
        category = str(row["category"])
        source_class = str(row["class_name"])
        category_counts[(category, source_class, "accepted_en")] += 1
        if source_class == "BENIGN":
            mapped_counts["benign"] += 1
        elif category in PI_CATEGORIES:
            mapped_counts["PI"] += 1
        elif category == "jailbreak":
            mapped_counts["JB"] += 1
        else:
            mapped_counts["quarantined_unmapped_attack"] += 1

    result = {
        "audit_id": "ciberia_english_native_category_screen_round03_v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "dataset_id": audit["candidate"]["dataset_id"],
        "revision": audit["candidate"]["revision"],
        "input": "pinned upstream train shard only",
        "source_sha256": source_sha,
        "language_filter": {"package": "py3langid", "model_sha256": model_sha,
                            "rule": "predicted_language == en and normalized confidence >= 0.95"},
        "mapping_status": "explicit_native_category_reference_screen_not_human_gold",
        "mapping_rules": {"benign": "source class BENIGN",
                           "PI": "ATTACK with category direct_prompt_injection or indirect_prompt_injection",
                           "JB": "ATTACK with category jailbreak",
                           "otherwise": "quarantine"},
        "accepted_language_counts": {f"{lang}:{state}": count for (lang, state), count in sorted(language_counts.items())},
        "english_category_source_class_counts": [
            {"category": category, "source_class": source_class, "rows": count}
            for (category, source_class, _), count in sorted(category_counts.items())
        ],
        "english_mapped_reference_counts": dict(sorted(mapped_counts.items())),
        "test_opened": False,
        "prompt_text_emitted": False,
    }
    output = ROOT / "ciberia_english_mapping_screen_round03.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"result": "PASS_TRAIN_ONLY_AGGREGATE", "rows": len(rows),
                      "mapped_counts": result["english_mapped_reference_counts"],
                      "test_opened": False, "report": str(output)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
