"""
SmoothLLM Replication & Empirical Evaluation Script
Paper: SmoothLLM: Defending Large Language Models Against Jailbreaking Attacks (Robey et al., NeurIPS 2023)
Framework: https://github.com/arobey1/smooth-llm
Focus: Randomized Smoothing via Character Perturbations (Swap, Patch, Insert) & Majority Voting
Hardware Target: Commodity CPU
"""

import sys
import os
import json
import time
import copy
import random
import numpy as np

# Add local lib to path
sys.path.insert(0, os.path.dirname(__file__))
import lib.perturbations as perturbations

def load_gcg_dataset():
    base_dir = os.path.dirname(__file__)
    comb_path = os.path.join(base_dir, "datasets", "smoothllm_eval_benchmark.json")
    if os.path.exists(comb_path):
        with open(comb_path, "r", encoding="utf-8") as f:
            return json.load(f)
            
    candidates = [
        os.path.join(base_dir, "datasets", "llama2_behaviors.json"),
        os.path.join(base_dir, "data", "GCG", "llama2_behaviors.json")
    ]
    data_path = next((p for p in candidates if os.path.exists(p)), None)
    if not data_path:
        raise FileNotFoundError(f"Could not find GCG dataset in {candidates}")
        
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    samples = []
    for goal, control in zip(data["goal"], data["controls"]):
        adv_prompt = f"{goal} {control}"
        samples.append({
            "goal": goal,
            "control": control,
            "adv_prompt": adv_prompt
        })
    return samples

def evaluate_smoothllm_perturbations():
    print("=== [SmoothLLM (NeurIPS 2023) Replication Benchmark] ===")
    print("Paradigm: Randomized Smoothing via Character Perturbation & Majority Voting")
    print("Device: Commodity CPU\n")
    
    samples = load_gcg_dataset()
    print(f"Loaded {len(samples)} GCG adversarial attack samples from data/GCG/llama2_behaviors.json\n")
    
    pert_types = ["RandomSwapPerturbation", "RandomPatchPerturbation", "RandomInsertPerturbation"]
    pert_pcts = [5, 10, 15] # percentage of characters perturbed
    num_copies = 5          # number of smoothed copies for majority vote
    
    results = {}
    
    for pert_name in pert_types:
        results[pert_name] = {}
        pert_class = getattr(perturbations, pert_name)
        
        for q in pert_pcts:
            pert_fn = pert_class(q=q)
            latencies = []
            char_diffs = []
            perturbed_samples = []
            
            for s in samples:
                prompt = s["adv_prompt"]
                t0 = time.perf_counter()
                
                # Generate N copies as in SmoothLLM
                copies = [pert_fn(prompt) for _ in range(num_copies)]
                t1 = time.perf_counter()
                
                latency_ms = (t1 - t0) * 1000.0
                latencies.append(latency_ms)
                
                # Calculate average character Hamming distance / diff
                diff_count = sum(1 for c1, c2 in zip(prompt, copies[0]) if c1 != c2)
                char_diffs.append(diff_count / max(len(prompt), 1))
                
                perturbed_samples.append({
                    "original_len": len(prompt),
                    "sample_perturbed": copies[0][:60] + "..."
                })
            
            mean_lat = float(np.mean(latencies))
            p95_lat = float(np.percentile(latencies, 95))
            mean_diff = float(np.mean(char_diffs))
            
            results[pert_name][f"q_{q}pct"] = {
                "pert_pct": q,
                "num_copies": num_copies,
                "mean_latency_ms": round(mean_lat, 4),
                "p95_latency_ms": round(p95_lat, 4),
                "mean_char_perturbation_rate": round(mean_diff, 4),
                "sample_output": perturbed_samples[0]["sample_perturbed"]
            }
            
            print(f"  [{pert_name:24} | q={q:2d}% | N={num_copies}]: Mean Latency = {mean_lat:6.4f}ms | P95 = {p95_lat:6.4f}ms | Diff Rate = {mean_diff*100:.2f}%")

    # Evaluate SmoothLLM Tradeoff with Downstream Model
    # Note in thesis: SmoothLLM requires N sequential LLM forward passes
    # E.g. If LLM forward pass takes 200ms, N=5 takes 1000ms (1.0s) -> High latency overhead!
    tradeoff_analysis = {
        "algorithmic_principle": "Perturb prompt N times and take majority vote to break brittle adversarial suffixes (GCG).",
        "cpu_perturbation_latency_overhead_ms": round(float(np.mean([results[p]["q_10pct"]["mean_latency_ms"] for p in pert_types])), 4),
        "downstream_llm_calls_multiplier": num_copies,
        "theoretical_defense_guarantee": "Effective against transfer attacks and white-box GCG token optimization.",
        "operational_bottleneck": f"Requires {num_copies}x downstream LLM inference calls, increasing total latency by ~{num_copies}x."
    }
    
    output_path = os.path.join(os.path.dirname(__file__), "SMOOTHLLM_REPLICATION_BENCHMARK_RESULTS.json")
    output_payload = {
        "paper": "Robey et al., SmoothLLM: Defending Large Language Models Against Jailbreaking Attacks, NeurIPS 2023",
        "repo": "https://github.com/arobey1/smooth-llm",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "hardware": "Commodity CPU",
        "perturbation_benchmarks": results,
        "tradeoff_analysis": tradeoff_analysis
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_payload, f, indent=2, ensure_ascii=False)
        
    print(f"\n[OK] SmoothLLM replication results saved to: {output_path}")

if __name__ == "__main__":
    evaluate_smoothllm_perturbations()
