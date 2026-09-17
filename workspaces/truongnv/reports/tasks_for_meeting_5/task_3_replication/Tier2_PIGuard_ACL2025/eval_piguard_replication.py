#!/usr/bin/env python3
"""
Empirical Evaluation Script for PIGuard (ACL 2025) Replication
PI-Guard Capstone Project - FPT University
Compares local CPU execution against reported numbers in arXiv:2410.22770 / ACL 2025
"""

import os
import sys
import time
import json
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# Fix Windows cp1252 encoding
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def evaluate_subset(classifier, samples, target_class, name, batch_size=32):
    t_start = time.time()
    correct = 0
    total = len(samples)
    latencies = []
    misclassified = []

    for i in range(0, total, batch_size):
        batch = samples[i : i + batch_size]
        b_t0 = time.time()
        preds = classifier(batch)
        b_lat = (time.time() - b_t0) * 1000 / len(batch)
        latencies.extend([b_lat] * len(batch))

        for sample, pred in zip(batch, preds):
            is_correct = (pred["label"] == target_class)
            if is_correct:
                correct += 1
            else:
                misclassified.append({
                    "prompt": sample[:200] + "..." if len(sample) > 200 else sample,
                    "predicted_label": pred["label"],
                    "confidence": float(pred["score"])
                })

    total_time = time.time() - t_start
    acc = (correct / total) * 100.0 if total > 0 else 0.0
    avg_lat = float(np.mean(latencies)) if latencies else 0.0
    p50_lat = float(np.percentile(latencies, 50)) if latencies else 0.0
    p95_lat = float(np.percentile(latencies, 95)) if latencies else 0.0

    print(f"[{name}] Total: {total} | Correct: {correct} | Accuracy: {acc:.2f}% | Avg Latency: {avg_lat:.2f}ms | P95: {p95_lat:.2f}ms")

    return {
        "name": name,
        "total_samples": total,
        "correct_predictions": correct,
        "accuracy_pct": round(acc, 2),
        "target_class": target_class,
        "avg_latency_ms": round(avg_lat, 2),
        "p50_latency_ms": round(p50_lat, 2),
        "p95_latency_ms": round(p95_lat, 2),
        "total_time_sec": round(total_time, 2),
        "misclassified_count": len(misclassified),
        "sample_errors": misclassified[:5]
    }

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_dir = os.path.join(base_dir, "PIGuard_ACL2025", "datasets")
    output_json_path = os.path.join(base_dir, "PIGUARD_REPLICATION_BENCHMARK_RESULTS.json")

    print("=" * 75)
    print("🔬 PIGUARD (ACL 2025) EMPIRICAL BENCHMARK REPLICATION")
    print(f"Dataset Root: {dataset_dir}")
    print(f"PyTorch Version: {torch.__version__} | CUDA: {torch.cuda.is_available()}")
    print("=" * 75)

    # 1. Load Model & Tokenizer
    model_id = "leolee99/PIGuard"
    print(f"\n[*] Loading model '{model_id}'...")
    t0 = time.time()
    tokenizer = AutoTokenizer.from_pretrained(model_id, model_max_length=512)
    model = AutoModelForSequenceClassification.from_pretrained(model_id, trust_remote_code=True)
    device = "cpu"
    model.to(device)
    load_time = time.time() - t0
    print(f"[+] Model loaded in {load_time:.2f} seconds on device: {device}")

    classifier = pipeline(
        "text-classification",
        model=model,
        tokenizer=tokenizer,
        truncation=True,
        batch_size=32
    )

    results = {}

    # 2. Benchmark NotInject (Over-defense Mitigation)
    print("\n--- 1. Evaluating NotInject (Over-Defense Benchmark) ---")
    for subset in ["NotInject_one", "NotInject_two", "NotInject_three"]:
        file_path = os.path.join(dataset_dir, f"{subset}.json")
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        samples = [item["prompt"] for item in data]
        results[subset] = evaluate_subset(classifier, samples, "benign", subset)

    # Calculate overall NotInject Over-defense ACC
    total_notinject = sum(results[k]["total_samples"] for k in ["NotInject_one", "NotInject_two", "NotInject_three"])
    correct_notinject = sum(results[k]["correct_predictions"] for k in ["NotInject_one", "NotInject_two", "NotInject_three"])
    notinject_acc = (correct_notinject / total_notinject) * 100.0
    results["NotInject_overall"] = {
        "name": "NotInject_overall",
        "total_samples": total_notinject,
        "correct_predictions": correct_notinject,
        "accuracy_pct": round(notinject_acc, 2)
    }
    print(f"[NotInject Overall] Total: {total_notinject} | Accuracy: {notinject_acc:.2f}%")

    # 3. Benchmark WildGuard (Benign Prompts)
    print("\n--- 2. Evaluating WildGuard (Benign Accuracy) ---")
    wildguard_path = os.path.join(dataset_dir, "wildguard.json")
    with open(wildguard_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    wildguard_samples = [item["prompt"] for item in data]
    results["wildguard_benign"] = evaluate_subset(classifier, wildguard_samples, "benign", "WildGuard_Benign")

    # 4. Benchmark BIPIA (Indirect Prompt Injection)
    print("\n--- 3. Evaluating BIPIA (Indirect Prompt Injection) ---")
    bipia_text_path = os.path.join(dataset_dir, "BIPIA_text.json")
    with open(bipia_text_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    bipia_text_samples = []
    for k in data.keys():
        bipia_text_samples.extend(data[k])
    results["BIPIA_text"] = evaluate_subset(classifier, bipia_text_samples, "injection", "BIPIA_text")

    bipia_code_path = os.path.join(dataset_dir, "BIPIA_code.json")
    with open(bipia_code_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    bipia_code_samples = []
    for k in data.keys():
        bipia_code_samples.extend(data[k])
    results["BIPIA_code"] = evaluate_subset(classifier, bipia_code_samples, "injection", "BIPIA_code")

    total_bipia = len(bipia_text_samples) + len(bipia_code_samples)
    correct_bipia = results["BIPIA_text"]["correct_predictions"] + results["BIPIA_code"]["correct_predictions"]
    bipia_acc = (correct_bipia / total_bipia) * 100.0
    results["BIPIA_overall"] = {
        "name": "BIPIA_overall",
        "total_samples": total_bipia,
        "correct_predictions": correct_bipia,
        "accuracy_pct": round(bipia_acc, 2)
    }
    print(f"[BIPIA Overall] Total: {total_bipia} | Accuracy: {bipia_acc:.2f}%")

    # 5. Benchmark Validation Set (Mixed Benign & Injection)
    print("\n--- 4. Evaluating Validation Set (144 Mixed Samples) ---")
    valid_path = os.path.join(dataset_dir, "valid.json")
    with open(valid_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    tp, tn, fp, fn = 0, 0, 0, 0
    valid_latencies = []
    for item in data:
        prompt = item["prompt"]
        true_label = "injection" if item["label"] == 1 else "benign"
        t_sample = time.time()
        pred = classifier(prompt)[0]
        valid_latencies.append((time.time() - t_sample) * 1000)
        pred_label = pred["label"]

        if true_label == "injection" and pred_label == "injection":
            tp += 1
        elif true_label == "benign" and pred_label == "benign":
            tn += 1
        elif true_label == "benign" and pred_label == "injection":
            fp += 1
        elif true_label == "injection" and pred_label == "benign":
            fn += 1

    valid_total = len(data)
    valid_acc = (tp + tn) / valid_total * 100.0
    precision = tp / (tp + fp) * 100.0 if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) * 100.0 if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    fpr = fp / (fp + tn) * 100.0 if (fp + tn) > 0 else 0.0

    results["validation_set"] = {
        "name": "Validation_Set_144",
        "total_samples": valid_total,
        "confusion_matrix": {"TP": tp, "TN": tn, "FP": fp, "FN": fn},
        "accuracy_pct": round(valid_acc, 2),
        "precision_pct": round(precision, 2),
        "recall_pct": round(recall, 2),
        "f1_score": round(f1 / 100.0, 4),
        "fpr_pct": round(fpr, 2),
        "avg_latency_ms": round(float(np.mean(valid_latencies)), 2),
        "p95_latency_ms": round(float(np.percentile(valid_latencies, 95)), 2)
    }
    print(f"[Validation Set] TP={tp}, TN={tn}, FP={fp}, FN={fn} | Acc: {valid_acc:.2f}% | F1: {results['validation_set']['f1_score']} | FPR: {fpr:.2f}%")

    # 6. Comparison against Paper (Table 1 & Table 7)
    comparison = {
        "NotInject_one_word": {"Paper_Reported": 91.15, "Local_Empirical": results["NotInject_one"]["accuracy_pct"]},
        "NotInject_two_words": {"Paper_Reported": 89.38, "Local_Empirical": results["NotInject_two"]["accuracy_pct"]},
        "NotInject_three_words": {"Paper_Reported": 81.42, "Local_Empirical": results["NotInject_three"]["accuracy_pct"]},
        "NotInject_Overall_Overdefense": {"Paper_Reported": 87.32, "Local_Empirical": results["NotInject_overall"]["accuracy_pct"]},
        "WildGuard_Benign": {"Paper_Reported": 76.11, "Local_Empirical": results["wildguard_benign"]["accuracy_pct"]},
        "BIPIA_Injection": {"Paper_Reported": 68.34, "Local_Empirical": results["BIPIA_overall"]["accuracy_pct"]}
    }

    final_report_data = {
        "metadata": {
            "model": "leolee99/PIGuard (microsoft/deberta-v3-base fine-tuned with MOF)",
            "paper": "PIGuard: Prompt Injection Guardrail via Mitigating Overdefense for Free (ACL 2025)",
            "arxiv_id": "arXiv:2410.22770",
            "execution_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "device": device,
            "torch_version": torch.__version__
        },
        "paper_comparison": comparison,
        "detailed_results": results
    }

    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(final_report_data, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 75)
    print("📊 PAPER REPLICATION COMPARISON SCORECARD")
    print("=" * 75)
    print(f"{'Benchmark Metric':<35} | {'Paper ACL 2025':<16} | {'Local Empirical':<16} | {'Match Delta'}")
    print("-" * 75)
    for k, v in comparison.items():
        paper_val = v["Paper_Reported"]
        local_val = v["Local_Empirical"]
        delta = local_val - paper_val
        match_str = "EXACT MATCH (0.00%)" if abs(delta) < 0.05 else f"Delta: {delta:+.2f}%"
        print(f"{k:<35} | {paper_val:>14.2f}% | {local_val:>14.2f}% | {match_str}")
    print("=" * 75)
    print(f"[+] Saved structured results to: {output_json_path}")

if __name__ == "__main__":
    main()
