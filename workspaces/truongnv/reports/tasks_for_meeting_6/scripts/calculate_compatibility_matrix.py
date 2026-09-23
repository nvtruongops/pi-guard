"""
calculate_compatibility_matrix.py
---------------------------------
Evaluation script to compute and validate the 6x7 Architectural-Algorithmic 
Compatibility Matrix for PI-Guard's Literature Taxonomy.

Models (Rows - M1 to M6):
  M1: Heuristic & Regex Scrubber (Tier 0)
  M2: Classical Sparse Statistical ML (Tier 1)
  M3: Dense Metric Learning & Proximity Classifiers
  M4: Absolute-Positioning Discriminative Encoders (Legacy BERT/RoBERTa)
  M5: Disentangled & Modern Deep Encoders (Tier 2 Core - DeBERTa-v3 / ModernBERT)
  M6: Autoregressive Generative Safety SLMs (LLM-as-a-Judge)

Paradigms (Columns - A1 to A7):
  A1: Sublinear Statistical Term Projection + Platt Calibration
  A2: Sliding-Window Cross-Entropy & Perplexity Filtering (PPL)
  A3: Dense Metric Learning & Semantic Proximity Centroids
  A4: Disentangled Representation Attention + Invariant Loss (MOF)
  A5: Randomized Smoothing & Majority Perturbation Voting
  A6: Game-Theoretic Minimax Adversarial Optimization
  A7: Conformal Risk Control (CRC) & Tri-State Dynamic Calibration

Author: Nguyen Van Truong (Leader) - PI-Guard Capstone Project
Date: 2026-09-23
"""

import json
import os
import sys

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

MODELS = [
    {"id": "M1", "name": "Heuristic & Regex Scrubber (Tier 0)", "category": "Rule-based & Deterministic"},
    {"id": "M2", "name": "Classical Sparse Statistical ML (Tier 1)", "category": "Linear High-Dimensional Sparse"},
    {"id": "M3", "name": "Dense Metric Learning & Proximity", "category": "Bi-Encoder Embedding Space"},
    {"id": "M4", "name": "Absolute-Positioning Transformers", "category": "Legacy Bidirectional Attention"},
    {"id": "M5", "name": "Disentangled & Modern Encoders (Tier 2)", "category": "Disentangled Deep Bidirectional"},
    {"id": "M6", "name": "Autoregressive Generative SLMs", "category": "Causal Autoregressive Decoder"}
]

PARADIGMS = [
    {"id": "A1", "name": "Sublinear TF-IDF + Platt Calibration", "math_nature": "Frequency statistics + Platt logistic margin"},
    {"id": "A2", "name": "Sliding-Window Perplexity (PPL)", "math_nature": "Language model token surprise & cross-entropy"},
    {"id": "A3", "name": "Dense Proximity Centroids", "math_nature": "Cosine / Euclidean metric clustering"},
    {"id": "A4", "name": "Disentangled Attention + MOF Loss", "math_nature": "Content-position decoupling + KL invariant loss"},
    {"id": "A5", "name": "Randomized Smoothing & Voting", "math_nature": "Empirical stochastic averaging under perturbation"},
    {"id": "A6", "name": "Minimax Adversarial Optimization", "math_nature": "Game-theoretic inner max / outer min gradient game"},
    {"id": "A7", "name": "Conformal Risk Control & Tri-State", "math_nature": "Finite-sample risk bound calibration"}
]

# Compatibility Matrix Data: 42 cells
# Score: 0-10, Status: Native (9-10), Conditional (4-8), Incompatible (0-3)
MATRIX_EVALUATIONS = {
    ("M1", "A1"): {"score": 1, "status": "Incompatible", "reason": "M1 uses deterministic string rules; lacks continuous decision margins or feature vectors for Platt scaling."},
    ("M1", "A2"): {"score": 0, "status": "Incompatible", "reason": "M1 has no probabilistic language model to compute token cross-entropy or perplexity."},
    ("M1", "A3"): {"score": 0, "status": "Incompatible", "reason": "M1 does not project inputs into continuous Euclidean or Cosine metric spaces."},
    ("M1", "A4"): {"score": 0, "status": "Incompatible", "reason": "M1 lacks neural attention matrices, making content-position disentanglement mathematically impossible."},
    ("M1", "A5"): {"score": 2, "status": "Incompatible", "reason": "Random string perturbation breaks exact regex patterns, causing massive false negatives."},
    ("M1", "A6"): {"score": 1, "status": "Incompatible", "reason": "Discrete non-differentiable regex patterns cannot compute gradients for minimax optimization."},
    ("M1", "A7"): {"score": 4, "status": "Conditional", "reason": "Only outputs binary {0, 1}; cannot support continuous tri-state risk partitioning."},

    ("M2", "A1"): {"score": 10, "status": "Native", "reason": "Native foundation of M2: sublinear term scaling + Platt scaling for calibrated probabilities in < 2ms."},
    ("M2", "A2"): {"score": 5, "status": "Conditional", "reason": "Requires auxiliary n-gram LM (e.g. KenLM); adds 2-3ms overhead to a sub-millisecond classifier."},
    ("M2", "A3"): {"score": 4, "status": "Conditional", "reason": "Rocchio centroids in 50k-dim sparse space suffer from the curse of dimensionality and sparsity."},
    ("M2", "A4"): {"score": 0, "status": "Incompatible", "reason": "M2 lacks self-attention mechanisms; cannot decouple content from relative position."},
    ("M2", "A5"): {"score": 5, "status": "Conditional", "reason": "Running M=10 perturbations multiplies latency to 15ms, eliminating the sub-2ms speed advantage of Tier 1."},
    ("M2", "A6"): {"score": 6, "status": "Conditional", "reason": "Discrete sparse vocabulary requires greedy coordinate descent rather than continuous gradient ascent."},
    ("M2", "A7"): {"score": 10, "status": "Native", "reason": "Perfect match: Platt calibrated probabilities enable finite-sample CRC bounds to split traffic tri-state."},

    ("M3", "A1"): {"score": 4, "status": "Conditional", "reason": "Hybrid dense-sparse concatenation is feasible but redundant and increases memory footprint."},
    ("M3", "A2"): {"score": 2, "status": "Incompatible", "reason": "Bi-encoders produce sentence embeddings, not token-level autoregressive probability distributions."},
    ("M3", "A3"): {"score": 10, "status": "Native", "reason": "Native design of M3 (Ayub CAMLIS 2024): cosine similarity to toxic cluster centroids."},
    ("M3", "A4"): {"score": 4, "status": "Conditional", "reason": "Small bi-encoders lack decoupled relative position matrices; MOF loss on pooled embeddings is ineffective."},
    ("M3", "A5"): {"score": 6, "status": "Conditional", "reason": "Averaging M=10 dense vectors is mathematically sound but inflates CPU latency from 8ms to 80ms."},
    ("M3", "A6"): {"score": 8, "status": "Conditional", "reason": "Continuous vector space allows Projected Gradient Descent (PGD) in embedding space for adversarial training."},
    ("M3", "A7"): {"score": 9, "status": "Native", "reason": "Cosine proximity scores map smoothly into [0, 1] for empirical Conformal Risk Control calibration."},

    ("M4", "A1"): {"score": 2, "status": "Incompatible", "reason": "BERT tokenizers (WordPiece) and deep self-attention make external sparse TF-IDF features redundant."},
    ("M4", "A2"): {"score": 8, "status": "Conditional", "reason": "Masked LM Pseudo-Perplexity (PLL) works but requires N forward passes, yielding unacceptable latency (>100ms)."},
    ("M4", "A3"): {"score": 6, "status": "Conditional", "reason": "BERT CLS pooling suffers from representation anisotropy (vectors collapse into a narrow cone)."},
    ("M4", "A4"): {"score": 5, "status": "Conditional", "reason": "M4 adds absolute positional embeddings at layer 0; cannot perform DeBERTa-style 3-matrix disentanglement."},
    ("M4", "A5"): {"score": 6, "status": "Conditional", "reason": "Feasible but multiplies latency from 35ms to 350ms, rendering it useless for ingress proxy."},
    ("M4", "A6"): {"score": 8, "status": "Conditional", "reason": "Adversarial training (FGM / FreeLB) on token embeddings is well-proven for BERT."},
    ("M4", "A7"): {"score": 9, "status": "Native", "reason": "Calibrated sigmoid/softmax outputs are readily partitioned via Conformal Risk Control."},

    ("M5", "A1"): {"score": 2, "status": "Incompatible", "reason": "DeBERTa-v3 / ModernBERT self-attention captures semantics natively; TF-IDF is redundant inside M5."},
    ("M5", "A2"): {"score": 6, "status": "Conditional", "reason": "RTD discriminator scores can flag replaced/adversarial tokens, but cross-attention is the primary task."},
    ("M5", "A3"): {"score": 7, "status": "Conditional", "reason": "Less anisotropic than BERT; can serve as a strong metric backbone, though direct classification is superior."},
    ("M5", "A4"): {"score": 10, "status": "Native", "reason": "Sovereign Champion: Disentangled Attention (content vs relative pos) + MOF loss eliminates keyword trigger bias."},
    ("M5", "A5"): {"score": 6, "status": "Conditional", "reason": "High latency overhead (25ms -> 250ms); best reserved for offline fuzzing rather than online inference."},
    ("M5", "A6"): {"score": 10, "status": "Native", "reason": "Sovereign Champion: Minimax adversarial optimization (DataSentinel) hardens DeBERTa against adaptive evasion."},
    ("M5", "A7"): {"score": 10, "status": "Native", "reason": "Sovereign Champion: CRC calibrates softmax risk to guarantee FPR <= 1.5% with 95% statistical confidence."},

    ("M6", "A1"): {"score": 1, "status": "Incompatible", "reason": "Applying classical bag-of-words TF-IDF to an 8B autoregressive model is architecturally obsolete."},
    ("M6", "A2"): {"score": 10, "status": "Native", "reason": "Autoregressive Causal LLM is the native generator of perplexity; computes input sequence PPL in a single pass."},
    ("M6", "A3"): {"score": 3, "status": "Incompatible", "reason": "Causal unidirectional attention makes generative SLMs inferior metric extractors compared to bi-encoders."},
    ("M6", "A4"): {"score": 2, "status": "Incompatible", "reason": "Decoder-only LLMs use standard RoPE/causal attention, incompatible with DeBERTa's 3-component disentanglement."},
    ("M6", "A5"): {"score": 1, "status": "Incompatible", "reason": "Running SmoothLLM (M=10) on an 8B model inflates latency to 15-20 SECONDS, completely paralyzing proxy throughput."},
    ("M6", "A6"): {"score": 5, "status": "Conditional", "reason": "Minimax adversarial training on 8B LLMs requires massive multi-GPU compute clusters (impractical for PoC)."},
    ("M6", "A7"): {"score": 9, "status": "Native", "reason": "Conformal prediction on safety verdict tokens ('Safe'/'Unsafe') provides rigorous high-assurance risk bounds."}
}

def analyze_matrix():
    print("=" * 80)
    print("PI-GUARD 6x7 ARCHITECTURAL-ALGORITHMIC COMPATIBILITY MATRIX EVALUATION")
    print("=" * 80)
    
    status_counts = {"Native": 0, "Conditional": 0, "Incompatible": 0}
    model_averages = {}
    paradigm_averages = {p["id"]: [] for p in PARADIGMS}
    
    for m in MODELS:
        scores = []
        for p in PARADIGMS:
            eval_data = MATRIX_EVALUATIONS[(m["id"], p["id"])]
            score = eval_data["score"]
            status = eval_data["status"]
            status_counts[status] += 1
            scores.append(score)
            paradigm_averages[p["id"]].append(score)
        model_averages[m["id"]] = sum(scores) / len(scores)
    
    print("\n[1] Overall Compatibility Statistics across 42 Cells:")
    print(f"  - 🟢 Native / Optimal Fit (Score 9-10):     {status_counts['Native']} cells ({status_counts['Native']/42*100:.1f}%)")
    print(f"  - 🟡 Conditional / High Overhead (Score 4-8): {status_counts['Conditional']} cells ({status_counts['Conditional']/42*100:.1f}%)")
    print(f"  - 🔴 Incompatible / Infeasible (Score 0-3):   {status_counts['Incompatible']} cells ({status_counts['Incompatible']/42*100:.1f}%)")
    
    print("\n[2] Model Versatility Score (Average Compatibility across 7 Paradigms):")
    for m in MODELS:
        print(f"  - {m['id']}: {m['name']:<45} -> Avg Score: {model_averages[m['id']]:.2f} / 10")
    
    print("\n[3] Paradigm Applicability Score (Average across 6 Models):")
    for p in PARADIGMS:
        avg_score = sum(paradigm_averages[p["id"]]) / len(paradigm_averages[p["id"]])
        print(f"  - {p['id']}: {p['name']:<45} -> Avg Score: {avg_score:.2f} / 10")
        
    # Export full matrix to JSON
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "04_benchmarks_and_data"))
    os.makedirs(output_dir, exist_ok=True)
    json_path = os.path.join(output_dir, "compatibility_matrix_6x7.json")
    
    export_data = {
        "models": MODELS,
        "paradigms": PARADIGMS,
        "evaluations": [
            {
                "model_id": m["id"],
                "model_name": m["name"],
                "paradigm_id": p["id"],
                "paradigm_name": p["name"],
                "score": MATRIX_EVALUATIONS[(m["id"], p["id"])]["score"],
                "status": MATRIX_EVALUATIONS[(m["id"], p["id"])]["status"],
                "reason": MATRIX_EVALUATIONS[(m["id"], p["id"])]["reason"]
            }
            for m in MODELS for p in PARADIGMS
        ],
        "summary": {
            "native_cells": status_counts["Native"],
            "conditional_cells": status_counts["Conditional"],
            "incompatible_cells": status_counts["Incompatible"],
            "model_averages": model_averages,
            "paradigm_averages": {p["id"]: sum(paradigm_averages[p["id"]])/len(paradigm_averages[p["id"]]) for p in PARADIGMS}
        }
    }
    
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
        
    print(f"\n✔ Successfully exported 6x7 matrix evaluation to: {json_path}")

if __name__ == "__main__":
    analyze_matrix()
