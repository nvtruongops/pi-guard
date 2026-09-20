import os
import json
import glob
import re
import hashlib
from collections import Counter, defaultdict
import numpy as np

DATASET_DIR = r"D:\Work\Do-an\workspaces\truongnv\reports\tasks_for_meeting_5\task_3_replication\Tier2_PIGuard_ACL2025\PIGuard_ACL2025\datasets"
OUT_DIR = r"D:\Work\Do-an\workspaces\truongnv\reports\tasks_for_meeting_5\task_3_replication\Tier2_PIGuard_ACL2025"

def hash_text(text):
    norm = " ".join(text.strip().lower().split())
    return hashlib.sha256(norm.encode('utf-8')).hexdigest()

def analyze():
    print("=== STARTING COMPREHENSIVE DATASET AUDIT ===")
    
    files = {
        "train": os.path.join(DATASET_DIR, "train.json"),
        "valid": os.path.join(DATASET_DIR, "valid.json"),
        "wildguard": os.path.join(DATASET_DIR, "wildguard.json"),
        "NotInject_one": os.path.join(DATASET_DIR, "NotInject_one.json"),
        "NotInject_two": os.path.join(DATASET_DIR, "NotInject_two.json"),
        "NotInject_three": os.path.join(DATASET_DIR, "NotInject_three.json"),
        "BIPIA_text": os.path.join(DATASET_DIR, "BIPIA_text.json"),
        "BIPIA_code": os.path.join(DATASET_DIR, "BIPIA_code.json"),
    }
    
    audit_results = {}
    
    # 1. File size & technical check
    file_info = {}
    for name, path in files.items():
        size_bytes = os.path.getsize(path)
        file_info[name] = {
            "path": path,
            "size_kb": round(size_bytes / 1024, 2),
            "size_mb": round(size_bytes / (1024 * 1024), 2),
        }
    audit_results["file_info"] = file_info
    
    # 2. Load and parse all files
    loaded_data = {}
    for name, path in files.items():
        with open(path, "r", encoding="utf-8") as f:
            loaded_data[name] = json.load(f)
            
    # Flatten datasets into standardized format: list of {"prompt": str, "label": int, "source": str, "extra": dict}
    standardized = {}
    
    # train.json
    train_records = []
    for idx, item in enumerate(loaded_data["train"]):
        train_records.append({
            "prompt": item.get("prompt", ""),
            "label": item.get("label"),
            "source": item.get("source", "UNKNOWN"),
            "orig_file": "train.json",
            "index": idx
        })
    standardized["train"] = train_records
    
    # valid.json
    valid_records = []
    for idx, item in enumerate(loaded_data["valid"]):
        valid_records.append({
            "prompt": item.get("prompt", ""),
            "label": item.get("label"),
            "source": item.get("source", "UNKNOWN"),
            "orig_file": "valid.json",
            "index": idx
        })
    standardized["valid"] = valid_records

    # wildguard.json
    wild_records = []
    for idx, item in enumerate(loaded_data["wildguard"]):
        wild_records.append({
            "prompt": item.get("prompt", ""),
            "label": item.get("label"),
            "source": "WildGuard_Benign",
            "orig_file": "wildguard.json",
            "index": idx
        })
    standardized["wildguard"] = wild_records

    # NotInject_one/two/three
    for ni_name in ["NotInject_one", "NotInject_two", "NotInject_three"]:
        records = []
        for idx, item in enumerate(loaded_data[ni_name]):
            records.append({
                "prompt": item.get("prompt", ""),
                "label": 0, # Ground truth benign
                "source": ni_name,
                "category": item.get("category"),
                "word_list": item.get("word_list"),
                "orig_file": f"{ni_name}.json",
                "index": idx
            })
        standardized[ni_name] = records

    # BIPIA_text
    bipia_text_records = []
    for cat, items in loaded_data["BIPIA_text"].items():
        for idx, prompt in enumerate(items):
            bipia_text_records.append({
                "prompt": prompt,
                "label": 1, # Ground truth injection
                "source": "BIPIA_text",
                "category": cat,
                "orig_file": "BIPIA_text.json",
                "index": idx
            })
    standardized["BIPIA_text"] = bipia_text_records

    # BIPIA_code
    bipia_code_records = []
    for cat, items in loaded_data["BIPIA_code"].items():
        for idx, prompt in enumerate(items):
            bipia_code_records.append({
                "prompt": prompt,
                "label": 1, # Ground truth injection
                "source": "BIPIA_code",
                "category": cat,
                "orig_file": "BIPIA_code.json",
                "index": idx
            })
    standardized["BIPIA_code"] = bipia_code_records

    # 3. Statistical Profiling
    stats = {}
    for name, records in standardized.items():
        total = len(records)
        labels = Counter(r["label"] for r in records)
        char_lens = [len(r["prompt"]) for r in records]
        word_lens = [len(r["prompt"].split()) for r in records]
        
        stats[name] = {
            "total_samples": total,
            "label_dist": dict(labels),
            "benign_count": labels.get(0, 0),
            "malicious_count": labels.get(1, 0),
            "benign_pct": round(labels.get(0, 0) / total * 100, 2) if total > 0 else 0,
            "malicious_pct": round(labels.get(1, 0) / total * 100, 2) if total > 0 else 0,
            "char_len": {
                "min": int(np.min(char_lens)) if total > 0 else 0,
                "mean": round(float(np.mean(char_lens)), 2) if total > 0 else 0,
                "median": float(np.median(char_lens)) if total > 0 else 0,
                "p95": float(np.percentile(char_lens, 95)) if total > 0 else 0,
                "max": int(np.max(char_lens)) if total > 0 else 0,
            },
            "word_len": {
                "min": int(np.min(word_lens)) if total > 0 else 0,
                "mean": round(float(np.mean(word_lens)), 2) if total > 0 else 0,
                "median": float(np.median(word_lens)) if total > 0 else 0,
                "p95": float(np.percentile(word_lens, 95)) if total > 0 else 0,
                "max": int(np.max(word_lens)) if total > 0 else 0,
            }
        }
    audit_results["dataset_stats"] = stats
    
    # 4. train.json detailed sub-source profiling
    train_source_stats = {}
    train_by_source = defaultdict(list)
    for r in standardized["train"]:
        train_by_source[r["source"]].append(r)
        
    for src, src_records in train_by_source.items():
        total = len(src_records)
        labels = Counter(r["label"] for r in src_records)
        char_lens = [len(r["prompt"]) for r in src_records]
        word_lens = [len(r["prompt"].split()) for r in src_records]
        train_source_stats[src] = {
            "total": total,
            "benign": labels.get(0, 0),
            "malicious": labels.get(1, 0),
            "pct_of_train": round(total / len(standardized["train"]) * 100, 2),
            "char_mean": round(float(np.mean(char_lens)), 1),
            "char_max": int(np.max(char_lens)),
            "word_mean": round(float(np.mean(word_lens)), 1),
            "word_max": int(np.max(word_lens)),
        }
    audit_results["train_sources"] = train_source_stats
    
    # 5. valid.json detailed sub-source profiling
    valid_source_stats = {}
    valid_by_source = defaultdict(list)
    for r in standardized["valid"]:
        valid_by_source[r["source"]].append(r)
    for src, src_records in valid_by_source.items():
        total = len(src_records)
        labels = Counter(r["label"] for r in src_records)
        valid_source_stats[src] = {
            "total": total,
            "benign": labels.get(0, 0),
            "malicious": labels.get(1, 0),
            "pct_of_valid": round(total / len(standardized["valid"]) * 100, 2),
        }
    audit_results["valid_sources"] = valid_source_stats
    
    # 6. Duplication and Data Quality checks
    empty_prompts = {}
    for name, records in standardized.items():
        empty_count = sum(1 for r in records if not r["prompt"] or not r["prompt"].strip())
        empty_prompts[name] = empty_count
    audit_results["empty_prompts"] = empty_prompts
    
    # Internal exact duplicates
    internal_dups = {}
    for name, records in standardized.items():
        seen = Counter(hash_text(r["prompt"]) for r in records)
        dups = sum(cnt - 1 for cnt in seen.values() if cnt > 1)
        internal_dups[name] = {
            "total_records": len(records),
            "unique_prompts": len(seen),
            "duplicate_records": dups,
            "duplication_rate_pct": round(dups / len(records) * 100, 3) if len(records) > 0 else 0
        }
    audit_results["internal_duplication"] = internal_dups

    # Internal conflicting labels in train.json
    train_hash_to_labels = defaultdict(set)
    for r in standardized["train"]:
        h = hash_text(r["prompt"])
        train_hash_to_labels[h].add(r["label"])
    
    conflicting_train = {h: list(lbls) for h, lbls in train_hash_to_labels.items() if len(lbls) > 1}
    audit_results["train_label_conflicts"] = {
        "conflicting_prompts_count": len(conflicting_train),
    }

    # 7. Data Leakage & Cross-Contamination Analysis
    train_hashes = set(hash_text(r["prompt"]) for r in standardized["train"])
    valid_hashes = set(hash_text(r["prompt"]) for r in standardized["valid"])
    train_valid_overlap = train_hashes.intersection(valid_hashes)
    
    train_valid_leak_examples = []
    if train_valid_overlap:
        for r in standardized["valid"]:
            h = hash_text(r["prompt"])
            if h in train_valid_overlap:
                train_valid_leak_examples.append({
                    "source_in_valid": r["source"],
                    "label_in_valid": r["label"],
                    "prompt_snippet": r["prompt"][:100]
                })

    benchmark_overlaps = {}
    for test_name in ["NotInject_one", "NotInject_two", "NotInject_three", "wildguard", "BIPIA_text", "BIPIA_code"]:
        test_h = set(hash_text(r["prompt"]) for r in standardized[test_name])
        overlap = train_hashes.intersection(test_h)
        overlap_examples = []
        for r in standardized[test_name]:
            h = hash_text(r["prompt"])
            if h in overlap:
                overlap_examples.append({
                    "source": r.get("source"),
                    "label": r.get("label"),
                    "prompt_snippet": r["prompt"][:100]
                })
        benchmark_overlaps[test_name] = {
            "test_total": len(standardized[test_name]),
            "overlap_with_train": len(overlap),
            "leakage_rate_pct": round(len(overlap) / len(standardized[test_name]) * 100, 2),
            "examples": overlap_examples[:5]
        }
        
    valid_benchmark_overlaps = {}
    for test_name in ["NotInject_one", "NotInject_two", "NotInject_three", "wildguard", "BIPIA_text", "BIPIA_code"]:
        test_h = set(hash_text(r["prompt"]) for r in standardized[test_name])
        overlap = valid_hashes.intersection(test_h)
        valid_benchmark_overlaps[test_name] = {
            "test_total": len(standardized[test_name]),
            "overlap_with_valid": len(overlap),
            "leakage_rate_pct": round(len(overlap) / len(standardized[test_name]) * 100, 2),
        }

    audit_results["leakage_audit"] = {
        "train_vs_valid": {
            "train_unique": len(train_hashes),
            "valid_unique": len(valid_hashes),
            "overlap_count": len(train_valid_overlap),
            "leakage_rate_pct": round(len(train_valid_overlap) / len(valid_hashes) * 100, 2),
            "sample_leaks": train_valid_leak_examples[:5]
        },
        "train_vs_test_benchmarks": benchmark_overlaps,
        "valid_vs_test_benchmarks": valid_benchmark_overlaps
    }

    # 8. NotInject Specific Audit
    notinject_stats = {
        "trigger_word_frequency": Counter(),
        "categories": Counter(),
        "word_count_distribution": Counter()
    }
    for ni_name in ["NotInject_one", "NotInject_two", "NotInject_three"]:
        for r in standardized[ni_name]:
            notinject_stats["categories"][r["category"]] += 1
            words = r.get("word_list", [])
            notinject_stats["word_count_distribution"][len(words)] += 1
            for w in words:
                notinject_stats["trigger_word_frequency"][w] += 1
    audit_results["notinject_profile"] = {
        "categories": dict(notinject_stats["categories"]),
        "word_counts": dict(notinject_stats["word_count_distribution"]),
        "top_trigger_words": dict(notinject_stats["trigger_word_frequency"].most_common(20))
    }

    # Save complete audit json
    out_json = os.path.join(OUT_DIR, "PIGUARD_DATASET_AUDIT_RESULTS.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(audit_results, f, indent=2, ensure_ascii=False)
    print(f"[OK] Audit complete! Saved full results to: {out_json}")
    
    # Print high-level summary
    print("\n" + "="*70)
    print("                 PIGUARD DATASET AUDIT SUMMARY SCORECARD")
    print("="*70)
    print(f"Total Datasets Analyzed: {len(standardized)}")
    print(f"Train samples: {len(standardized['train'])} ({stats['train']['benign_pct']}% Benign, {stats['train']['malicious_pct']}% Malicious)")
    print(f"Valid samples: {len(standardized['valid'])} ({stats['valid']['benign_pct']}% Benign, {stats['valid']['malicious_pct']}% Malicious)")
    print(f"Test Benchmarks: WildGuard({len(standardized['wildguard'])}), NotInject(339), BIPIA(125)")
    print(f"Train vs Valid Leakage: {audit_results['leakage_audit']['train_vs_valid']['overlap_count']} overlapping prompts ({audit_results['leakage_audit']['train_vs_valid']['leakage_rate_pct']}%)")
    print("\nTrain vs Test Benchmarks Overlap:")
    for k, v in benchmark_overlaps.items():
        print(f"  - {k}: {v['overlap_with_train']} overlaps / {v['test_total']} samples ({v['leakage_rate_pct']}%)")
    print("\nValid vs Test Benchmarks Overlap:")
    for k, v in valid_benchmark_overlaps.items():
        print(f"  - {k}: {v['overlap_with_valid']} overlaps / {v['test_total']} samples ({v['leakage_rate_pct']}%)")
    print("="*70)

if __name__ == "__main__":
    analyze()
