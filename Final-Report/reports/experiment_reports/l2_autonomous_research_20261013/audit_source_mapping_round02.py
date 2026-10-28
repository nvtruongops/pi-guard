#!/usr/bin/env python3
"""Summarize native source/category evidence for train sources and Mirza train only."""
from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import csv
import hashlib
import json
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import pyarrow.parquet as pq

REPORT = Path(__file__).resolve().parent
ACQUIRED = REPORT / "source_qualification" / "acquired"
TRAINING = Path(r"D:\Work\Do-an\workspaces\truongnv\pi_guard_pipeline\training_bases")
NEURAL = ACQUIRED / "neuralchemy_core_train.parquet"
WAMBO = TRAINING / "datasets" / "source_datasets" / "wambosec_prompt_injections_candidate" / "data" / "train-00000-of-00001.parquet"
MIRZA = TRAINING / "datasets" / "source_datasets" / "mirzaakhi_prompt_injection_candidate" / "prompt_injection_dataset.csv"

JB_CATEGORIES = {"jailbreak", "persona_replacement", "many_shot", "crescendo"}
PI_CATEGORIES = {"direct_injection", "indirect_injection", "prompt_injection", "instruction_override",
                 "system_extraction", "prompt_extraction", "prompt_leak", "system_manipulation",
                 "token_injection", "token_smuggling", "encoding", "encoding_obfuscation",
                 "rag_poisoning", "context_confusion", "payload_injection", "output_manipulation",
                 "response_manipulation"}
BENIGN_MIRZA = {"carrier_clean", "embedded_human", "qa", "task", "chitchat", "hard_negative", "security_qa"}
PI_MIRZA = {"indirect_injection", "appended_override", "authority", "direct_override", "fake_system"}


def normalized_hash(text: str) -> str:
    normal = " ".join(unicodedata.normalize("NFKC", text).casefold().split())
    return hashlib.sha256(normal.encode("utf-8")).hexdigest()


def main() -> int:
    neural = pq.read_table(NEURAL).to_pylist()
    neural_cross: Counter = Counter()
    neural_groups: dict[str, set[str]] = defaultdict(set)
    neural_hashes = set()
    mapped = Counter()
    excluded = Counter()
    for row in neural:
        source = str(row.get("source") or "")
        category = str(row.get("category") or "")
        label = str(row.get("label"))
        neural_cross[(source, category, label)] += 1
        text = row["text"]
        neural_hashes.add(normalized_hash(text))
        rule = None
        if source == "wildguard_judgecomp":
            excluded["source_rights_research"] += 1
        elif source == "harmbench":
            excluded["harmful_behavior_seed_not_jb_or_pi"] += 1
        elif label == "0" and category == "benign":
            rule = "neuralchemy:benign_native_category"
        elif label == "1" and category in JB_CATEGORIES:
            rule = "neuralchemy:jailbreak_native_category"
        elif label == "1" and category in PI_CATEGORIES:
            rule = "neuralchemy:prompt_injection_native_category"
        else:
            excluded[f"unmapped:{source}:{category}:{label}"] += 1
        if rule:
            mapped[(rule, source, category)] += 1

    wambo_rows = pq.read_table(WAMBO).to_pylist()
    wambo_cross: Counter = Counter()
    wambo_hashes = set()
    wambo_mapped = Counter()
    for row in wambo_rows:
        label = str(row.get("label"))
        category = str(row.get("category") or "")
        jailbreak = isinstance(category, str) and "jailbreak" in category.casefold()
        target = "benign" if label == "0" else "JB" if label == "1" and jailbreak else "PI" if label == "1" else "exclude"
        wambo_cross[(label, category, target)] += 1
        wambo_hashes.add(normalized_hash(str(row.get("prompt") or row.get("text") or "")))
        wambo_mapped[target] += 1

    mirza_rows = Counter()
    mirza_native = Counter()
    mirza_map = Counter()
    mirza_hashes = set()
    with MIRZA.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        required = {"prompt", "label", "category", "split"}
        if not required.issubset(reader.fieldnames or []):
            raise RuntimeError("Mirza source CSV schema changed")
        for row in reader:
            if row.get("split") != "train":
                continue
            text = row.get("prompt", "")
            category = str(row.get("category") or "")
            native = str(row.get("label") or "")
            if not text.strip():
                raise RuntimeError("Empty Mirza source train text")
            mirza_rows["rows"] += 1
            mirza_native[(native, category)] += 1
            mirza_hashes.add(normalized_hash(text))
            if native == "benign" and category in BENIGN_MIRZA:
                target = "benign"
            elif native == "malicious" and category == "persona_jailbreak":
                target = "JB"
            elif native == "malicious" and category in PI_MIRZA:
                target = "PI"
            else:
                target = "exclude"
            mirza_map[target] += 1

    record = {
        "audit_id": "autonomous_native_mapping_source_summary_v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "NeurAlchemy core/train, Wambo train, and Mirza upstream train rows only",
        "validation_source_test_rows_opened": False,
        "neuralchemy": {
            "source_category_label_counts": [
                {"source": k[0], "category": k[1], "native_label": k[2], "rows": n}
                for k, n in sorted(neural_cross.items())],
            "provisional_mapping_counts_by_source_category": [
                {"rule": k[0], "source": k[1], "category": k[2], "rows": n}
                for k, n in sorted(mapped.items())],
            "excluded_rows": dict(sorted(excluded.items())),
            "rows": len(neural), "unique_normalized_prompts": len(neural_hashes),
            "exact_train_overlap_wambo": len(neural_hashes & wambo_hashes),
            "exact_train_overlap_mirza_train": len(neural_hashes & mirza_hashes),
        },
        "wambosec": {"native_label_category_target_counts": [
            {"native_label": k[0], "category": k[1], "target": k[2], "rows": n}
            for k, n in sorted(wambo_cross.items())], "target_counts": dict(sorted(wambo_mapped.items())),
            "rows": len(wambo_rows), "unique_normalized_prompts": len(wambo_hashes),
            "exact_train_overlap_mirza_train": len(wambo_hashes & mirza_hashes)},
        "mirzaakhi": {"upstream_train_rows": mirza_rows["rows"],
                      "native_label_category_counts": [
                          {"native_label": k[0], "category": k[1], "rows": n}
                          for k, n in sorted(mirza_native.items())],
                      "provisional_mapping_counts": dict(sorted(mirza_map.items())),
                      "unique_normalized_prompts": len(mirza_hashes),
                      "validation_support_floor": 100,
                      "category_mapping_status": "predeclared_source_reference_mapping_not_human_gold"},
        "test_payload_opened": False,
    }
    target = REPORT / "source_qualification" / "source_mapping_audit_round02.json"
    target.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "SOURCE_MAPPING_AUDIT_COMPLETE", "report": str(target),
                      "neuralchemy_candidate_counts": record["neuralchemy"]["provisional_mapping_counts_by_source_category"],
                      "neuralchemy_excluded": record["neuralchemy"]["excluded_rows"],
                      "wambosec_target_counts": record["wambosec"]["target_counts"],
                      "mirza_train_rows": mirza_rows["rows"], "mirza_mapping_counts": dict(mirza_map),
                      "test_opened": False}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
