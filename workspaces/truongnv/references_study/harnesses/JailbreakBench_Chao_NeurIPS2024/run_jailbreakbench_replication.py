"""
JailbreakBench (NeurIPS 2024) Replication & Empirical Benchmark Script
Paper: Chao et al., JailbreakBench: An Open Robustness Benchmark for Jailbreaking Large Language Models, NeurIPS 2024
Dataset: dedeswim/JBB-Behaviors (100 harmful behaviors across 10 categories + 100 benign behaviors)
Repository: https://github.com/JailbreakBench/jailbreakbench
Hardware Target: Commodity CPU
"""

import sys
import os
import json
import time
import numpy as np
import torch
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification

def run_jbb_replication():
    print("=== [JailbreakBench (NeurIPS 2024) Replication Benchmark] ===")
    print("Benchmark: JBB-Behaviors 100 Standard Harmful & 100 Benign Behaviors")
    print("Device: Commodity CPU\n")
    
    # 1. Load JBB-Behaviors dataset from local datasets directory
    t0 = time.time()
    ds_dir = os.path.join(os.path.dirname(__file__), "datasets")
    harmful_json = os.path.join(ds_dir, "jbb_behaviors_harmful.json")
    benign_json = os.path.join(ds_dir, "jbb_behaviors_benign.json")
    
    if os.path.exists(harmful_json) and os.path.exists(benign_json):
        with open(harmful_json, "r", encoding="utf-8") as f:
            ds_harmful = json.load(f)
        with open(benign_json, "r", encoding="utf-8") as f:
            ds_benign = json.load(f)
        print(f"[OK] Loaded {len(ds_harmful)} harmful behaviors and {len(ds_benign)} benign behaviors from local datasets/ in {time.time()-t0:.2f}s")
    else:
        ds_harmful = load_dataset("dedeswim/JBB-Behaviors", "behaviors", split="harmful")
        ds_benign = load_dataset("dedeswim/JBB-Behaviors", "behaviors", split="benign")
        print(f"[OK] Loaded {len(ds_harmful)} harmful behaviors and {len(ds_benign)} benign behaviors from HF Hub in {time.time()-t0:.2f}s")
    
    # 2. Load ProtectAI DeBERTa-v3 as standardized evaluator
    model_id = "protectai/deberta-v3-base-prompt-injection-v2"
    print(f"Loading Evaluator: {model_id} on CPU...")
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForSequenceClassification.from_pretrained(model_id)
    model.eval()
    
    # 3. Evaluate harmful behaviors (Detection / Recall test)
    print("\nEvaluating 100 Harmful JBB Behaviors...")
    harmful_results = []
    harmful_latencies = []
    category_stats = {}
    
    for item in ds_harmful:
        goal = item["Goal"]
        category = item["Category"]
        source = item.get("Source", "JBB")
        
        tokens = tokenizer(goal, return_tensors="pt", truncation=True, max_length=512)
        t_start = time.perf_counter()
        with torch.no_grad():
            outputs = model(**tokens)
            probs = torch.softmax(outputs.logits, dim=-1)[0]
            pred = torch.argmax(probs).item()
        latency_ms = (time.perf_counter() - t_start) * 1000.0
        harmful_latencies.append(latency_ms)
        
        # 1: Injection / Flagged, 0: Safe
        flagged = (pred == 1)
        prob_flagged = float(probs[1].item())
        
        if category not in category_stats:
            category_stats[category] = {"total": 0, "flagged": 0}
        category_stats[category]["total"] += 1
        if flagged:
            category_stats[category]["flagged"] += 1
            
        harmful_results.append({
            "goal": goal,
            "category": category,
            "source": source,
            "flagged": flagged,
            "prob_flagged": prob_flagged,
            "latency_ms": round(latency_ms, 2)
        })
        
    # 4. Evaluate benign behaviors (FPR test on JBB benign control)
    print("Evaluating 100 Benign JBB Behaviors...")
    benign_results = []
    benign_latencies = []
    
    for item in ds_benign:
        goal = item["Goal"]
        category = item["Category"]
        
        tokens = tokenizer(goal, return_tensors="pt", truncation=True, max_length=512)
        t_start = time.perf_counter()
        with torch.no_grad():
            outputs = model(**tokens)
            probs = torch.softmax(outputs.logits, dim=-1)[0]
            pred = torch.argmax(probs).item()
        latency_ms = (time.perf_counter() - t_start) * 1000.0
        benign_latencies.append(latency_ms)
        
        flagged = (pred == 1)
        benign_results.append({
            "goal": goal,
            "category": category,
            "flagged": flagged,
            "prob_flagged": float(probs[1].item()),
            "latency_ms": round(latency_ms, 2)
        })

    # Metrics computation
    total_harmful = len(harmful_results)
    flagged_harmful = sum(1 for r in harmful_results if r["flagged"])
    detection_rate = flagged_harmful / total_harmful
    
    total_benign = len(benign_results)
    flagged_benign = sum(1 for r in benign_results if r["flagged"])
    fpr = flagged_benign / total_benign
    
    for cat, data in category_stats.items():
        data["flagged_rate"] = round(data["flagged"] / data["total"], 4)
        
    print("\n=== [JAILBREAKBENCH EMPIRICAL RESULTS SUMMARY] ===")
    print(f"Total Harmful Behaviors: {total_harmful}")
    print(f"Harmful Behaviors Flagged (Detection Rate): {detection_rate*100:.2f}% ({flagged_harmful}/{total_harmful})")
    print(f"Total Benign Behaviors:  {total_benign}")
    print(f"Benign False Positive Rate (FPR):          {fpr*100:.2f}% ({flagged_benign}/{total_benign})")
    print(f"CPU Latency (Mean): {np.mean(harmful_latencies + benign_latencies):.2f}ms | P95: {np.percentile(harmful_latencies + benign_latencies, 95):.2f}ms")
    
    print("\n--- Harmful Category Detection Rates ---")
    for cat, data in sorted(category_stats.items(), key=lambda x: x[1]["flagged_rate"], reverse=True):
        print(f"  {cat:32}: {data['flagged_rate']*100:6.2f}% ({data['flagged']}/{data['total']})")
        
    output_path = os.path.join(os.path.dirname(__file__), "JAILBREAKBENCH_REPLICATION_BENCHMARK_RESULTS.json")
    output_payload = {
        "paper": "Chao et al., JailbreakBench: An Open Robustness Benchmark for Jailbreaking Large Language Models, NeurIPS 2024",
        "benchmark": "dedeswim/JBB-Behaviors",
        "repo": "https://github.com/JailbreakBench/jailbreakbench",
        "evaluator_model": model_id,
        "hardware": "Commodity CPU",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "overall_summary": {
            "total_harmful_behaviors": total_harmful,
            "flagged_harmful_behaviors": flagged_harmful,
            "harmful_detection_rate": round(detection_rate, 4),
            "total_benign_behaviors": total_benign,
            "flagged_benign_behaviors": flagged_benign,
            "false_positive_rate": round(fpr, 4),
            "mean_latency_ms": round(float(np.mean(harmful_latencies + benign_latencies)), 2),
            "p95_latency_ms": round(float(np.percentile(harmful_latencies + benign_latencies, 95)), 2)
        },
        "category_detection_rates": category_stats,
        "sample_harmful_results": harmful_results[:10],
        "sample_benign_results": benign_results[:10]
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_payload, f, indent=2, ensure_ascii=False)
        
    print(f"\n[OK] JailbreakBench benchmark results exported to: {output_path}")

if __name__ == "__main__":
    run_jbb_replication()
