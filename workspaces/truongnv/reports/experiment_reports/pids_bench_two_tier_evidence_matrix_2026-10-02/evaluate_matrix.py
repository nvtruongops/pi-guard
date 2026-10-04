"""Score both pinned PIDS-Bench models on the same frozen evaluation axes."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from transformers import AutoModelForSequenceClassification, AutoTokenizer


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def best_threshold(y: np.ndarray, p: np.ndarray) -> float:
    grid = np.linspace(0.0, 1.0, 501)
    scores = [f1_score(y, p >= t, zero_division=0) for t in grid]
    return float(grid[int(np.argmax(scores))])


def metric_row(model: str, axis: str, y: np.ndarray, p: np.ndarray, threshold: float, mode: str) -> dict:
    pred = (p >= threshold).astype(int)
    tn = int(((y == 0) & (pred == 0)).sum())
    fp = int(((y == 0) & (pred == 1)).sum())
    fn = int(((y == 1) & (pred == 0)).sum())
    tp = int(((y == 1) & (pred == 1)).sum())
    return {
        "model": model,
        "axis": axis,
        "threshold_mode": mode,
        "threshold": threshold,
        "n": len(y),
        "accuracy": float(accuracy_score(y, pred)),
        "attack_f1": float(f1_score(y, pred, zero_division=0)),
        "macro_f1": float(f1_score(y, pred, average="macro", zero_division=0)),
        "attack_precision": float(precision_score(y, pred, zero_division=0)),
        "attack_recall": float(recall_score(y, pred, zero_division=0)),
        "benign_fpr": float(fp / (fp + tn)) if fp + tn else None,
        "attack_fnr": float(fn / (fn + tp)) if fn + tp else None,
        "roc_auc": float(roc_auc_score(y, p)) if len(np.unique(y)) == 2 else None,
        "tn": tn,
        "fp": fp,
        "fn": fn,
        "tp": tp,
    }


def transformer_scores(model, tokenizer, texts: list[str], max_length: int,
                       batch_size: int, device: torch.device) -> np.ndarray:
    scores: list[np.ndarray] = []
    model.eval()
    with torch.inference_mode():
        for start in range(0, len(texts), batch_size):
            batch = texts[start : start + batch_size]
            encoded = tokenizer(
                batch,
                truncation=True,
                padding="max_length",
                max_length=max_length,
                return_tensors="pt",
            )
            encoded = {key: value.to(device) for key, value in encoded.items()}
            logits = model(**encoded).logits
            scores.append(torch.softmax(logits.float(), dim=1)[:, 1].cpu().numpy())
    return np.concatenate(scores)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True, help="Staged frozen PIDS-Bench data root")
    parser.add_argument("--tfidf-model", type=Path, required=True)
    parser.add_argument("--distil-model", type=Path, required=True)
    parser.add_argument("--deberta-model", type=Path, required=True)
    parser.add_argument("--tfidf-summary", type=Path, required=True)
    parser.add_argument("--distil-summary", type=Path, required=True)
    parser.add_argument("--deberta-summary", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--batch-size", type=int, default=1)
    args = parser.parse_args()

    data = args.data.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    axes = {
        "iid_test": data / "test.csv",
        "hard_benign": data / "eval_subsets" / "hard_benign_test.csv",
        "obfuscated_attacks": data / "eval_subsets" / "obfuscated_attacks.csv",
        "domain_ood": data / "ood" / "domain_ood.csv",
        "structural_ood": data / "ood" / "structural_ood.csv",
    }
    frames = {axis: pd.read_csv(path).reset_index(drop=True) for axis, path in axes.items()}
    if frames["hard_benign"]["text"].isna().any() or len(frames["hard_benign"]) != 808:
        raise SystemExit("Expected only 808 non-redacted hard-benign rows")
    val = pd.read_csv(data / "val.csv")
    tfidf = joblib.load(args.tfidf_model.resolve())
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    distil_path = args.distil_model.resolve()
    distil_tokenizer = AutoTokenizer.from_pretrained(str(distil_path), use_fast=True)
    distil = AutoModelForSequenceClassification.from_pretrained(
        str(distil_path), num_labels=2
    ).to(device)
    distil.float().eval()
    deberta_tokenizer = AutoTokenizer.from_pretrained(str(args.deberta_model.resolve()), use_fast=True)
    deberta = AutoModelForSequenceClassification.from_pretrained(
        str(args.deberta_model.resolve()), num_labels=2
    ).to(device)
    deberta.float().eval()

    scored: dict[str, dict[str, np.ndarray]] = {
        "TF-IDF + LR": {}, "DistilBERT": {}, "DeBERTa-v3-FT": {}
    }
    model_predictions = output / "predictions"
    model_predictions.mkdir(exist_ok=True)
    all_frames = {"validation": val, **frames}
    for axis, frame in all_frames.items():
        texts = frame["text"].fillna("").astype(str).tolist()
        scored["TF-IDF + LR"][axis] = tfidf.predict_proba(texts)[:, 1]
        scored["DistilBERT"][axis] = transformer_scores(
            distil, distil_tokenizer, texts, 256, args.batch_size, device
        )
        scored["DeBERTa-v3-FT"][axis] = transformer_scores(
            deberta, deberta_tokenizer, texts, 512, args.batch_size, device
        )
        if axis != "validation":
            for model_name, model_scores in scored.items():
                prediction = frame.copy()
                prediction.insert(0, "row_index", np.arange(len(frame)))
                prediction["probability_score"] = model_scores[axis]
                prediction.to_csv(
                    model_predictions / f"{model_name.lower().replace(' ', '_').replace('+', 'lr').replace('-', '_')}_{axis}.csv",
                    index=False,
                )
        del texts

    thresholds = {}
    rows = []
    for model_name, model_scores in scored.items():
        threshold = best_threshold(val["label"].to_numpy(), model_scores["validation"])
        thresholds[model_name] = threshold
        for axis, frame in frames.items():
            y = frame["label"].astype(int).to_numpy()
            p = model_scores[axis]
            rows.append(metric_row(model_name, axis, y, p, 0.5, "fixed_0.5"))
            rows.append(metric_row(model_name, axis, y, p, threshold, "validation_f1_max"))

    metrics = pd.DataFrame(rows)
    metrics.to_csv(output / "evidence_matrix_all_metrics.csv", index=False, float_format="%.8f")
    (output / "thresholds.json").write_text(json.dumps(thresholds, indent=2), encoding="utf-8")

    # Compare standalone held-out errors to quantify complementarity without
    # simulating a routing policy or claiming cascade performance.
    pairwise_rows = []
    model_pairs = [
        ("TF-IDF + LR", "DeBERTa-v3-FT"),
        ("TF-IDF + LR", "DistilBERT"),
        ("DistilBERT", "DeBERTa-v3-FT"),
    ]
    for axis, frame in frames.items():
        y = frame["label"].astype(int).to_numpy()
        for threshold_mode in ("fixed_0.5", "validation_f1_max"):
            selected_thresholds = {
                model_name: 0.5 if threshold_mode == "fixed_0.5" else thresholds[model_name]
                for model_name in scored
            }
            predictions = {
                model_name: scored[model_name][axis] >= selected_thresholds[model_name]
                for model_name in scored
            }
            for left, right in model_pairs:
                left_wrong = predictions[left] != y
                right_wrong = predictions[right] != y
                left_only = left_wrong & ~right_wrong
                right_only = right_wrong & ~left_wrong
                both_wrong = left_wrong & right_wrong
                union_wrong = left_wrong | right_wrong
                left_missed = (y == 1) & ~predictions[left]
                right_missed = (y == 1) & ~predictions[right]
                left_false_alarm = (y == 0) & predictions[left]
                right_false_alarm = (y == 0) & predictions[right]
                pairwise_rows.append({
                    "axis": axis,
                    "threshold_mode": threshold_mode,
                    "left_model": left,
                    "left_threshold": selected_thresholds[left],
                    "right_model": right,
                    "right_threshold": selected_thresholds[right],
                    "n": len(y),
                    "left_wrong_right_correct": int(left_only.sum()),
                    "right_wrong_left_correct": int(right_only.sum()),
                    "both_wrong": int(both_wrong.sum()),
                    "both_correct": int((~left_wrong & ~right_wrong).sum()),
                    "left_misses_caught_by_right": int((left_missed & predictions[right]).sum()),
                    "right_misses_caught_by_left": int((right_missed & predictions[left]).sum()),
                    "both_missed_attacks": int((left_missed & right_missed).sum()),
                    "left_false_alarms_caught_by_right": int((left_false_alarm & ~predictions[right]).sum()),
                    "right_false_alarms_caught_by_left": int((right_false_alarm & ~predictions[left]).sum()),
                    "both_false_alarms": int((left_false_alarm & right_false_alarm).sum()),
                    "wrong_error_jaccard": float(both_wrong.sum() / union_wrong.sum()) if union_wrong.any() else 1.0,
                    "left_errors_recovered_by_right_fraction": float(left_only.sum() / left_wrong.sum()) if left_wrong.any() else 0.0,
                    "right_errors_recovered_by_left_fraction": float(right_only.sum() / right_wrong.sum()) if right_wrong.any() else 0.0,
                })
    pd.DataFrame(pairwise_rows).to_csv(
        output / "pairwise_error_overlap.csv", index=False, float_format="%.8f"
    )

    axes_order = ["iid_test", "hard_benign", "obfuscated_attacks", "domain_ood", "structural_ood"]
    labels = [
        "IID test\nAttack F1",
        "Hard benign\nFPR ↓",
        "Obfuscated attack\nRecall",
        "Domain OOD\nAttack F1",
        "Structural OOD\nFPR ↓",
    ]
    models = list(scored)
    values = np.zeros((len(models), len(axes_order)))
    display = np.zeros_like(values)
    selected_rows = []
    for mi, model_name in enumerate(models):
        for ai, axis in enumerate(axes_order):
            row = metrics[
                (metrics.model == model_name)
                & (metrics.axis == axis)
                & (metrics.threshold_mode == "validation_f1_max")
            ].iloc[0].to_dict()
            selected_rows.append(row)
            metric = "benign_fpr" if axis in ("hard_benign", "structural_ood") else (
                "attack_recall" if axis == "obfuscated_attacks" else "attack_f1"
            )
            values[mi, ai] = row[metric]
            display[mi, ai] = 1.0 - row[metric] if metric == "benign_fpr" else row[metric]
    pd.DataFrame(selected_rows).to_csv(output / "evidence_matrix_val_tuned.csv", index=False, float_format="%.8f")

    fig, ax = plt.subplots(figsize=(12.2, 5.2), constrained_layout=True)
    image = ax.imshow(display, cmap="RdYlGn", vmin=0, vmax=1, aspect="auto")
    ax.set_xticks(range(len(labels)), labels=labels, fontsize=10)
    ax.set_yticks(range(len(models)), labels=models, fontsize=11, fontweight="bold")
    for mi, model_name in enumerate(models):
        for ai, axis in enumerate(axes_order):
            row = metrics[
                (metrics.model == model_name)
                & (metrics.axis == axis)
                & (metrics.threshold_mode == "fixed_0.5")
            ].iloc[0]
            metric = "benign_fpr" if axis in ("hard_benign", "structural_ood") else (
                "attack_recall" if axis == "obfuscated_attacks" else "attack_f1"
            )
            val = float(row[metric])
            ax.text(ai, mi, f"{val:.1%}\nn={int(row.n)}", ha="center", va="center", fontsize=10,
                    color="black" if 0.2 < display[mi, ai] < 0.85 else "white")
    ax.set_title("PIDS-Bench v3 • same release, seed 42 • fixed τ=0.5", fontsize=13, pad=12)
    ax.set_xlabel("Green direction means higher F1/recall or lower FPR; numbers show raw rates", labelpad=10)
    fig.colorbar(image, ax=ax, fraction=0.025, pad=0.02, label="Direction-adjusted score (higher is better)")
    fig.savefig(output / "pids_bench_model_comparison.png", dpi=200)
    plt.close(fig)

    provenance = {
        "device": str(device),
        "seed": 42,
        "thresholds_validation_f1_max": thresholds,
        "threshold_method": "501-point grid from 0.0 to 1.0 in 0.002 increments on val.csv only",
        "hard_benign_rows": len(frames["hard_benign"]),
        "hard_benign_blank_rows_omitted": 664,
        "model_artifact_hashes": {
            "tfidf": sha256(args.tfidf_model.resolve()),
            "distil_config": sha256(distil_path / "config.json"),
            "distil_weights": sha256(distil_path / "model.safetensors"),
            "deberta_config": sha256(args.deberta_model.resolve() / "config.json"),
            "deberta_weights": sha256(args.deberta_model.resolve() / "model.safetensors"),
        },
        "dataset_file_hashes": {axis: sha256(path) for axis, path in axes.items()},
    }
    (output / "evaluation_provenance.json").write_text(
        json.dumps(provenance, indent=2), encoding="utf-8"
    )

    source_summaries = {
        "TF-IDF + LR": json.loads(args.tfidf_summary.resolve().read_text(encoding="utf-8")),
        "DistilBERT": json.loads(args.distil_summary.resolve().read_text(encoding="utf-8")),
        "DeBERTa-v3-FT": json.loads(args.deberta_summary.resolve().read_text(encoding="utf-8")),
    }
    crosschecks = []
    for model_name, summary in source_summaries.items():
        expected_threshold = float(summary["val_tuned_threshold"])
        if abs(expected_threshold - thresholds[model_name]) > 1e-6:
            raise SystemExit(f"Validation threshold mismatch for {model_name}")
        checks = [
            ("test_f1_tau_0.5", "iid_test", "fixed_0.5", "attack_f1", summary["test_results"]["default_threshold_0.5"]["f1"]),
            ("test_f1_val_tuned", "iid_test", "validation_f1_max", "attack_f1", summary["test_results"]["val_tuned_threshold"]["f1"]),
            ("test_fpr_tau_0.5", "iid_test", "fixed_0.5", "benign_fpr", summary["test_results"]["default_threshold_0.5"]["fpr"]),
            ("test_fpr_val_tuned", "iid_test", "validation_f1_max", "benign_fpr", summary["test_results"]["val_tuned_threshold"]["fpr"]),
            ("hard_benign_fpr_tau_0.5", "hard_benign", "fixed_0.5", "benign_fpr", summary["hard_benign_test_fpr"]["fpr_default_0.5"]),
            ("hard_benign_fpr_val_tuned", "hard_benign", "validation_f1_max", "benign_fpr", summary["hard_benign_test_fpr"]["fpr_tuned"]),
            ("obfuscation_recall_val_tuned", "obfuscated_attacks", "validation_f1_max", "attack_recall", summary["obfuscated_attacks"]["overall_recall"]),
            ("domain_ood_f1_val_tuned", "domain_ood", "validation_f1_max", "attack_f1", summary["domain_ood"]["aggregate"]["f1"]),
            ("structural_ood_fpr_val_tuned", "structural_ood", "validation_f1_max", "benign_fpr", summary["structural_ood"]["aggregate"]["fpr"]),
        ]
        for name, axis, mode, metric, expected in checks:
            observed = float(metrics[
                (metrics.model == model_name)
                & (metrics.axis == axis)
                & (metrics.threshold_mode == mode)
            ].iloc[0][metric])
            expected = float(expected)
            matches = abs(observed - expected) <= 0.00011
            crosschecks.append({
                "model": model_name,
                "check": name,
                "observed": observed,
                "source_summary": expected,
                "absolute_difference": abs(observed - expected),
                "tolerance": 0.00011,
                "matches": matches,
            })
            if not matches:
                raise SystemExit(f"Prediction cross-check failed: {model_name} {name}")
    (output / "source_output_crosschecks.json").write_text(
        json.dumps(crosschecks, indent=2), encoding="utf-8"
    )
    print(json.dumps(provenance, indent=2))
    print(f"Cross-checks passed: {len(crosschecks)}")
    print(metrics[metrics.threshold_mode == "validation_f1_max"].to_string(index=False))


if __name__ == "__main__":
    main()
