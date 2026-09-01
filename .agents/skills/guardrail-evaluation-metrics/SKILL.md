---
name: guardrail-evaluation-metrics
description: >-
  Comprehensive evaluation methodology, metric calculations (F1, FPR, ROC-AUC, Confusion Matrix),
  robustness testing against adversarial obfuscation, and inference latency benchmarking for PI-Guard.
---

# Guardrail Evaluation & Metrics Guide

This skill defines the evaluation standards, metrics computation, and comparative benchmarking required for the **PI-Guard** Capstone Project.

---

## 1. Core Evaluation Metrics

Guardrail evaluation requires balancing security (high recall on attacks) against user experience (low false-positive rate on benign inputs).

### A. Mathematical Definitions
- **Accuracy**: $\frac{TP + TN}{TP + TN + FP + FN}$
- **Precision**: $\frac{TP}{TP + FP}$ (Proportion of flagged prompts that are actually malicious)
- **Recall (Detection Rate)**: $\frac{TP}{TP + FN}$ (Proportion of attacks successfully caught)
- **F1-Score**: $2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$
- **False Positive Rate (FPR - Over-defense)**: $\frac{FP}{FP + TN}$ (Percentage of legitimate user queries mistakenly blocked)
- **ROC-AUC & PR-AUC**: Area Under the ROC Curve and Precision-Recall Curve.

### B. Standard Metric Calculation Function
```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix, classification_report
)
import numpy as np

def evaluate_guardrail(y_true, y_pred, y_probs=None):
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    
    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred),
        "recall (TPR)": recall_score(y_true, y_pred),
        "f1_score": f1_score(y_true, y_pred),
        "false_positive_rate (FPR)": fp / (fp + tn) if (fp + tn) > 0 else 0.0,
        "true_negatives": int(tn),
        "false_positives": int(fp),
        "false_negatives": int(fn),
        "true_positives": int(tp)
    }
    
    if y_probs is not None:
        metrics["roc_auc"] = roc_auc_score(y_true, y_probs)
        
    return metrics
```

---

## 2. Adversarial Obfuscation Robustness Suite

Evaluate both Baseline ML and Fine-tuned Transformer models against a dedicated adversarial test set:

| Test Slice | Description | Target Evaluation |
| :--- | :--- | :--- |
| **Clean Injections** | Standard English prompt injections & jailbreaks | Baseline Detection Rate |
| **Leetspeak Injections** | Vowels/consonants replaced with digits/symbols (`1gn0r3`) | Char-level robustness |
| **Base64 Injections** | Payloads encoded in Base64 wrapped in decode instructions | Semantic decoding capability |
| **Spaced Text** | Tokens spaced out (`i g n o r e`) | Tokenizer resilience |
| **Clean Benign** | Complex everyday questions, coding tasks, math problems | False Positive Rate (< 1.5% target) |

```python
def run_robustness_benchmark(model_predict_fn, test_slices_dict):
    results = {}
    for slice_name, (texts, labels) in test_slices_dict.items():
        preds = model_predict_fn(texts)
        score = accuracy_score(labels, preds)
        results[slice_name] = score
        print(f"Slice [{slice_name}]: Accuracy = {score * 100:.2f}%")
    return results
```

---

## 3. Latency & Throughput Benchmarking

Measure inference speed in milliseconds per request ($ms/req$) to ensure real-time readiness:

```python
import time
import numpy as np

def benchmark_latency(predict_fn, sample_texts, warmups=50, runs=200):
    # Warmup
    for i in range(warmups):
        predict_fn([sample_texts[i % len(sample_texts)]])
        
    latencies = []
    for i in range(runs):
        text = sample_texts[i % len(sample_texts)]
        start = time.perf_counter()
        predict_fn([text])
        duration_ms = (time.perf_counter() - start) * 1000.0
        latencies.append(duration_ms)
        
    return {
        "p50_ms": np.percentile(latencies, 50),
        "p95_ms": np.percentile(latencies, 95),
        "p99_ms": np.percentile(latencies, 99),
        "mean_ms": np.mean(latencies)
    }
```
