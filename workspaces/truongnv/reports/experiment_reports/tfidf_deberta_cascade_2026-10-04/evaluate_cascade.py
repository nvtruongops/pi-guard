"""Evaluate a validation-tuned TF-IDF -> DeBERTa cascade on frozen PIDS-Bench data."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from transformers import AutoModelForSequenceClassification, AutoTokenizer


EXPECTED_DATA_HASHES = {
    "train.csv": "859124bfffe20483b337956efcb11c6bdaf6191835150f51a5e6da272ee5a2eb",
    "val.csv": "1445c0b33c220078d967fa34bb4da5e2981842ce288925b8f2542a4f9352cc64",
    "test.csv": "149092dc6a7a83d3da73e8c7b413ea5e215e3f96c5565767b6db56b3b7835d96",
    "eval_subsets/hard_benign_test.csv": "e3ddb1e6e9e04e1097b7bcf9a6f5e05b0a8d73e8d71b8d867f7ed85b89472cee",
    "eval_subsets/balanced_subtype_test.csv": "210e339329081b97ce95d2dfe4f4581e19bc83dd16a23b86cd36bd15b9ff2023",
    "eval_subsets/obfuscated_attacks.csv": "b151322f05ef83922c734c589804fc7eab53331b61b5ad153c72aaf683f7c691",
    "ood/domain_ood.csv": "d14acb99a69ac10559fde9ee22d0f20aa7a5816c4f48f279838d12ed0a6944f0",
    "ood/structural_ood.csv": "63d56a8ebbd0639404158b51b35863fc87b02e9869ee2526f5f90eaa48108dad",
}
EXPECTED_DEBERTA_BASE_REVISION = "8ccc9b6f36199bec6961081d44eb72fb3f7353f3"

AXES = {
    "iid_test": "test.csv",
    "hard_benign": "eval_subsets/hard_benign_test.csv",
    "obfuscated_attacks": "eval_subsets/obfuscated_attacks.csv",
    "domain_ood": "ood/domain_ood.csv",
    "structural_ood": "ood/structural_ood.csv",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_data(raw_root: Path, eval_root: Path) -> dict:
    hashes: dict[str, object] = {}
    for relative, expected in EXPECTED_DATA_HASHES.items():
        path = raw_root / relative
        observed = sha256(path)
        if observed != expected:
            raise SystemExit(f"Frozen source-data hash mismatch: {relative}: {observed} != {expected}")
        hashes[relative] = observed

    for relative in ("val.csv", "test.csv", *AXES.values()):
        if relative == "eval_subsets/hard_benign_test.csv":
            continue
        raw_path = raw_root / relative
        eval_path = eval_root / relative
        if sha256(raw_path) != sha256(eval_path):
            raise SystemExit(f"Evaluation copy differs from frozen source: {relative}")

    raw_hard = pd.read_csv(raw_root / AXES["hard_benign"])
    staged_hard = pd.read_csv(eval_root / AXES["hard_benign"])
    expected_hard = raw_hard[raw_hard["text"].fillna("").astype(str).str.strip().ne("")]
    if len(raw_hard) != 1472 or len(staged_hard) != 808 or len(expected_hard) != 808:
        raise SystemExit("Unexpected hard-benign source/staged row counts")
    if expected_hard.reset_index(drop=True).astype(str).to_dict("records") != staged_hard.reset_index(drop=True).astype(str).to_dict("records"):
        raise SystemExit("Staged hard-benign rows do not exactly match nonblank source rows")
    if staged_hard["label"].astype(int).ne(0).any():
        raise SystemExit("Hard-benign evaluation file contains a non-benign label")
    hashes["hard_benign_staged_csv_sha256"] = sha256(eval_root / AXES["hard_benign"])
    hashes["hard_benign_original_rows"] = len(raw_hard)
    hashes["hard_benign_retained_nonblank_rows"] = len(staged_hard)
    return hashes


def read_frame(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path)
    if not {"text", "label"}.issubset(frame.columns):
        raise SystemExit(f"Expected text and label columns in {path}")
    frame["text"] = frame["text"].fillna("").astype(str)
    frame["label"] = frame["label"].astype(int)
    if not set(frame["label"].unique()).issubset({0, 1}):
        raise SystemExit(f"Expected binary labels in {path}")
    return frame


def transformer_scores(model, tokenizer, texts: list[str], batch_size: int, device: torch.device) -> np.ndarray:
    scores: list[np.ndarray] = []
    model.eval()
    with torch.inference_mode():
        for start in range(0, len(texts), batch_size):
            batch = texts[start : start + batch_size]
            encoded = tokenizer(
                batch,
                truncation=True,
                padding=True,
                max_length=512,
                return_tensors="pt",
            )
            encoded = {key: value.to(device) for key, value in encoded.items()}
            logits = model(**encoded).logits
            scores.append(torch.softmax(logits.float(), dim=1)[:, 1].cpu().numpy())
    return np.concatenate(scores) if scores else np.empty(0, dtype=float)


def load_author_predictions(path: Path, frame: pd.DataFrame) -> np.ndarray:
    predictions = pd.read_csv(path)
    if len(predictions) != len(frame):
        raise SystemExit(f"Author prediction row count mismatch: {path}")
    labels = predictions.get("true_label", predictions.get("label"))
    if labels is None or not np.array_equal(labels.astype(int).to_numpy(), frame["label"].to_numpy()):
        raise SystemExit(f"Author prediction labels/order mismatch: {path}")
    if "text" in predictions and predictions["text"].fillna("").astype(str).tolist() != frame["text"].tolist():
        raise SystemExit(f"Author prediction texts/order mismatch: {path}")
    score_column = "probability_score" if "probability_score" in predictions else "deberta_score"
    if score_column not in predictions:
        raise SystemExit(f"No probability score in author predictions: {path}")
    return predictions[score_column].astype(float).to_numpy()


def compute_metrics(y: np.ndarray, pred: np.ndarray, score: np.ndarray | None, threshold: float | None,
                    method: str, axis: str, route_counts: dict[str, int], n_deberta_calls: int) -> dict:
    tn = int(((y == 0) & (pred == 0)).sum())
    fp = int(((y == 0) & (pred == 1)).sum())
    fn = int(((y == 1) & (pred == 0)).sum())
    tp = int(((y == 1) & (pred == 1)).sum())
    return {
        "method": method,
        "axis": axis,
        "threshold": threshold,
        "n": int(len(y)),
        "accuracy": float(accuracy_score(y, pred)),
        "macro_f1": float(f1_score(y, pred, labels=[0, 1], average="macro", zero_division=0)),
        "attack_f1": float(f1_score(y, pred, pos_label=1, zero_division=0)),
        "attack_precision": float(precision_score(y, pred, pos_label=1, zero_division=0)),
        "attack_recall": float(recall_score(y, pred, pos_label=1, zero_division=0)),
        "benign_fpr": float(fp / (fp + tn)) if fp + tn else None,
        "attack_fnr": float(fn / (fn + tp)) if fn + tp else None,
        "roc_auc": float(roc_auc_score(y, score)) if score is not None and len(np.unique(y)) == 2 else None,
        "tn": tn,
        "fp": fp,
        "fn": fn,
        "tp": tp,
        "tfidf_direct_benign": int(route_counts.get("tfidf_direct_benign", 0)),
        "tfidf_direct_attack": int(route_counts.get("tfidf_direct_attack", 0)),
        "deberta_calls": int(n_deberta_calls),
        "deberta_call_rate": float(n_deberta_calls / len(y)) if len(y) else None,
    }


def choose_fpr_threshold(y: np.ndarray, scores: np.ndarray, max_fpr: float) -> float:
    thresholds = np.unique(np.concatenate(([-1.0], scores, [np.nextafter(float(scores.max()), np.inf)])))
    total_benign = max(1, int((y == 0).sum()))
    total_attack = max(1, int((y == 1).sum()))
    best_key: tuple[float, float, float, float] | None = None
    best_threshold = float(thresholds[-1])
    for threshold in thresholds:
        pred = scores >= threshold
        fp = int(((y == 0) & pred).sum())
        if fp / total_benign > max_fpr:
            continue
        tp = int(((y == 1) & pred).sum())
        recall = tp / total_attack
        precision = tp / max(1, tp + fp)
        f1 = 2 * precision * recall / max(1e-15, precision + recall)
        key = (recall, f1, -(fp / total_benign), float(threshold))
        if best_key is None or key > best_key:
            best_key = key
            best_threshold = float(threshold)
    return best_threshold


def choose_cascade_policy(y: np.ndarray, tf_scores: np.ndarray, deb_scores: np.ndarray,
                          max_fpr: float) -> dict:
    low_gates = np.unique(np.concatenate(([-1.0], np.quantile(tf_scores, np.linspace(0.0, 0.5, 31)))))
    high_gates = np.unique(np.concatenate((np.quantile(tf_scores, np.linspace(0.5, 1.0, 31)),
                                           [np.nextafter(float(tf_scores.max()), np.inf)])))
    fallback_thresholds = np.unique(np.concatenate(([-1.0], np.quantile(deb_scores, np.linspace(0.0, 1.0, 201)),
                                                     [np.nextafter(float(deb_scores.max()), np.inf)])))
    n_benign = max(1, int((y == 0).sum()))
    n_attack = max(1, int((y == 1).sum()))
    best: tuple[tuple[float, float, float, float], dict] | None = None

    for low in low_gates:
        direct_benign = tf_scores <= low
        for high in high_gates:
            if high <= low:
                continue
            direct_attack = tf_scores >= high
            deferred = ~(direct_benign | direct_attack)
            base_tp = int((direct_attack & (y == 1)).sum())
            base_fp = int((direct_attack & (y == 0)).sum())
            deferred_attack_scores = np.sort(deb_scores[deferred & (y == 1)])
            deferred_benign_scores = np.sort(deb_scores[deferred & (y == 0)])
            for fallback in fallback_thresholds:
                tp = base_tp + len(deferred_attack_scores) - int(np.searchsorted(deferred_attack_scores, fallback, side="left"))
                fp = base_fp + len(deferred_benign_scores) - int(np.searchsorted(deferred_benign_scores, fallback, side="left"))
                fpr = fp / n_benign
                if fpr > max_fpr:
                    continue
                recall = tp / n_attack
                precision = tp / max(1, tp + fp)
                attack_f1 = 2 * precision * recall / max(1e-15, precision + recall)
                tn = n_benign - fp
                fn = n_attack - tp
                benign_f1 = 2 * tn / max(1, 2 * tn + fp + fn)
                macro_f1 = (attack_f1 + benign_f1) / 2.0
                call_rate = float(deferred.mean())
                key = (recall, macro_f1, -call_rate, -fpr)
                policy = {
                    "tfidf_benign_max_inclusive": float(low),
                    "tfidf_attack_min_inclusive": float(high),
                    "deberta_attack_threshold": float(fallback),
                    "validation_attack_recall": float(recall),
                    "validation_macro_f1": float(macro_f1),
                    "validation_benign_fpr": float(fpr),
                    "validation_deberta_call_rate": call_rate,
                    "search": "31 quantile candidates per TF-IDF gate; 201 quantile candidates for fallback; maximize validation attack recall under FPR budget, then macro-F1, then minimize DeBERTa calls",
                }
                if best is None or key > best[0]:
                    best = (key, policy)
    if best is None:
        raise SystemExit("Cascade threshold search found no policy within the validation FPR budget")
    return best[1]


def cascade_predict(tf_scores: np.ndarray, deb_scores: np.ndarray, policy: dict) -> tuple[np.ndarray, dict[str, int]]:
    direct_benign = tf_scores <= policy["tfidf_benign_max_inclusive"]
    direct_attack = tf_scores >= policy["tfidf_attack_min_inclusive"]
    deferred = ~(direct_benign | direct_attack)
    pred = direct_attack.astype(int)
    pred[deferred] = (deb_scores[deferred] >= policy["deberta_attack_threshold"]).astype(int)
    counts = {
        "tfidf_direct_benign": int(direct_benign.sum()),
        "tfidf_direct_attack": int(direct_attack.sum()),
        "deberta_calls": int(deferred.sum()),
    }
    return pred, counts


def model_files_hashes(model_dir: Path) -> dict[str, str]:
    candidates = [path for path in model_dir.iterdir() if path.is_file() and path.name in {
        "config.json", "model.safetensors", "pytorch_model.bin", "tokenizer.json", "spm.model",
        "tokenizer_config.json", "special_tokens_map.json"
    }]
    if not candidates:
        raise SystemExit(f"No model/tokenizer files found at the root of {model_dir}")
    return {str(path.relative_to(model_dir)): sha256(path) for path in sorted(candidates)}


def benchmark_latency(predict_fn, texts: list[str], device: torch.device, warmups: int, runs: int) -> dict:
    if not texts:
        return {"p50_ms": None, "p95_ms": None, "p99_ms": None, "mean_ms": None, "runs": 0}
    for index in range(warmups):
        predict_fn(texts[index % len(texts)])
    if device.type == "cuda":
        torch.cuda.synchronize(device)
    elapsed: list[float] = []
    for index in range(min(runs, len(texts))):
        if device.type == "cuda":
            torch.cuda.synchronize(device)
        start = time.perf_counter()
        predict_fn(texts[index])
        if device.type == "cuda":
            torch.cuda.synchronize(device)
        elapsed.append((time.perf_counter() - start) * 1000.0)
    return {
        "p50_ms": float(np.percentile(elapsed, 50)),
        "p95_ms": float(np.percentile(elapsed, 95)),
        "p99_ms": float(np.percentile(elapsed, 99)),
        "mean_ms": float(np.mean(elapsed)),
        "runs": len(elapsed),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-data", type=Path, required=True, help="Unmodified PIDS-Bench v3 author data root")
    parser.add_argument("--data", type=Path, required=True, help="Evaluation copy with blank hard-benign rows filtered")
    parser.add_argument("--tfidf-model", type=Path, required=True)
    parser.add_argument("--deberta-model", type=Path, required=True)
    parser.add_argument("--model-input-manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-fpr", type=float, default=0.015)
    parser.add_argument("--batch-size", type=int, default=2)
    parser.add_argument("--latency-runs", type=int, default=200)
    args = parser.parse_args()
    if not 0.0 < args.max_fpr < 1.0:
        raise SystemExit("--max-fpr must be between 0 and 1")

    raw_root = args.raw_data.resolve()
    eval_root = args.data.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    model_manifest_path = args.model_input_manifest.resolve()
    model_manifest = json.loads(model_manifest_path.read_text(encoding="utf-8"))
    if model_manifest.get("pids_bench_upstream_commit") != "87dc835566b930ee921240874a4939b2c266c2fe":
        raise SystemExit("Model input manifest does not match the pinned PIDS-Bench release")
    deberta_entries = [model for model in model_manifest.get("models", [])
                       if model.get("model_id") == "microsoft/deberta-v3-base"]
    if len(deberta_entries) != 1:
        raise SystemExit("Expected exactly one pinned microsoft/deberta-v3-base input entry")
    base_checkpoint = deberta_entries[0]
    if base_checkpoint.get("revision") != EXPECTED_DEBERTA_BASE_REVISION:
        raise SystemExit("DeBERTa base revision differs from the pinned open checkpoint")
    data_hashes = verify_data(raw_root, eval_root)
    frames = {axis: read_frame(eval_root / relative) for axis, relative in AXES.items()}
    validation = read_frame(eval_root / "val.csv")
    tfidf = joblib.load(args.tfidf_model.resolve())
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    deberta_path = args.deberta_model.resolve()
    tokenizer = AutoTokenizer.from_pretrained(str(deberta_path), use_fast=True, local_files_only=True)
    deberta = AutoModelForSequenceClassification.from_pretrained(
        str(deberta_path), local_files_only=True
    ).to(device)
    deberta.float().eval()

    scored: dict[str, dict[str, np.ndarray]] = {"TF-IDF + LR": {}, "DeBERTa-v3-FT": {}}
    all_frames = {"validation": validation, **frames}
    output_predictions = output / "predictions"
    output_predictions.mkdir(exist_ok=True)
    author_output_dir = deberta_path.parent
    cached_deberta_predictions = {
        "validation": author_output_dir / "val_predictions.csv",
        "iid_test": author_output_dir / "test_predictions.csv",
        "hard_benign": author_output_dir / "hard_benign_predictions.csv",
    }
    deberta_prediction_sources: dict[str, str] = {}
    for axis, frame in all_frames.items():
        texts = frame["text"].tolist()
        scored["TF-IDF + LR"][axis] = tfidf.predict_proba(texts)[:, 1]
        cached_path = cached_deberta_predictions.get(axis)
        if cached_path is not None and cached_path.is_file():
            scored["DeBERTa-v3-FT"][axis] = load_author_predictions(cached_path, frame)
            deberta_prediction_sources[axis] = str(cached_path)
        else:
            scored["DeBERTa-v3-FT"][axis] = transformer_scores(
                deberta, tokenizer, texts, args.batch_size, device
            )
            deberta_prediction_sources[axis] = "re-inferred from the saved local DeBERTa checkpoint"
        if not np.isfinite(scored["TF-IDF + LR"][axis]).all():
            raise SystemExit(f"Non-finite TF-IDF scores on {axis}")
        if not np.isfinite(scored["DeBERTa-v3-FT"][axis]).all():
            raise SystemExit(f"Non-finite DeBERTa scores on {axis}")

    val_labels = validation["label"].to_numpy()
    tf_threshold = choose_fpr_threshold(val_labels, scored["TF-IDF + LR"]["validation"], args.max_fpr)
    deb_threshold = choose_fpr_threshold(val_labels, scored["DeBERTa-v3-FT"]["validation"], args.max_fpr)
    cascade_policy = choose_cascade_policy(
        val_labels, scored["TF-IDF + LR"]["validation"], scored["DeBERTa-v3-FT"]["validation"], args.max_fpr
    )
    thresholds = {
        "max_validation_benign_fpr": args.max_fpr,
        "tfidf_attack_threshold": tf_threshold,
        "deberta_attack_threshold": deb_threshold,
        "cascade": cascade_policy,
        "selection_data": "val.csv only",
    }
    (output / "thresholds.json").write_text(json.dumps(thresholds, indent=2), encoding="utf-8")

    for axis, frame in all_frames.items():
        tf_scores = scored["TF-IDF + LR"][axis]
        deb_scores = scored["DeBERTa-v3-FT"][axis]
        cascade_pred, _route_counts = cascade_predict(tf_scores, deb_scores, cascade_policy)
        direct_benign = tf_scores <= cascade_policy["tfidf_benign_max_inclusive"]
        direct_attack = tf_scores >= cascade_policy["tfidf_attack_min_inclusive"]
        route = np.full(len(frame), "deberta_fallback", dtype=object)
        route[direct_benign] = "tfidf_direct_benign"
        route[direct_attack] = "tfidf_direct_attack"
        pd.DataFrame({
            "row_index": np.arange(len(frame)),
            "label": frame["label"].to_numpy(),
            "tfidf_score": tf_scores,
            "deberta_score": deb_scores,
            "tfidf_prediction_0_5": (tf_scores >= 0.5).astype(int),
            "deberta_prediction_0_5": (deb_scores >= 0.5).astype(int),
            "tfidf_prediction_fpr_budget": (tf_scores >= tf_threshold).astype(int),
            "deberta_prediction_fpr_budget": (deb_scores >= deb_threshold).astype(int),
            "cascade_prediction": cascade_pred,
            "cascade_route": route,
        }).to_csv(output_predictions / f"predictions_{axis}.csv", index=False, float_format="%.9f")

    metric_rows: list[dict] = []
    for axis, frame in frames.items():
        y = frame["label"].to_numpy()
        tf_scores = scored["TF-IDF + LR"][axis]
        deb_scores = scored["DeBERTa-v3-FT"][axis]
        empty_counts = {"tfidf_direct_benign": 0, "tfidf_direct_attack": 0, "deberta_calls": 0}
        for method, scores in (("TF-IDF + LR", tf_scores), ("DeBERTa-v3-FT", deb_scores)):
            fixed = (scores >= 0.5).astype(int)
            val_tuned = (scores >= (tf_threshold if method == "TF-IDF + LR" else deb_threshold)).astype(int)
            calls = len(y) if method == "DeBERTa-v3-FT" else 0
            metric_rows.append(compute_metrics(y, fixed, scores, 0.5, f"{method} fixed_0.5", axis, empty_counts, calls))
            metric_rows.append(compute_metrics(
                y, val_tuned, scores, tf_threshold if method == "TF-IDF + LR" else deb_threshold,
                f"{method} validation_fpr_budget", axis, empty_counts, calls
            ))
        cascade_pred, route_counts = cascade_predict(tf_scores, deb_scores, cascade_policy)
        metric_rows.append(compute_metrics(
            y, cascade_pred, None, None, "TF-IDF → DeBERTa cascade validation_fpr_budget",
            axis, route_counts, route_counts["deberta_calls"]
        ))

    metrics = pd.DataFrame(metric_rows)
    metrics.to_csv(output / "metrics_long.csv", index=False, float_format="%.9f")
    selected = metrics[metrics["method"].isin([
        "TF-IDF + LR validation_fpr_budget",
        "DeBERTa-v3-FT validation_fpr_budget",
        "TF-IDF → DeBERTa cascade validation_fpr_budget",
    ])]
    matrix = selected.pivot(index="method", columns="axis", values=[
        "attack_f1", "macro_f1", "attack_recall", "benign_fpr", "deberta_call_rate", "n"
    ])
    matrix.columns = [f"{metric}__{axis}" for metric, axis in matrix.columns]
    matrix.reset_index().to_csv(output / "comparison_matrix.csv", index=False, float_format="%.9f")

    display_metrics = [
        ("iid_test", "attack_f1", "IID Attack F1 ↑"),
        ("hard_benign", "benign_fpr", "Hard Benign FPR ↓"),
        ("obfuscated_attacks", "attack_recall", "Obfuscated Recall ↑"),
        ("domain_ood", "attack_f1", "Domain OOD Attack F1 ↑"),
        ("structural_ood", "benign_fpr", "Structural OOD FPR ↓"),
    ]
    methods = [
        "TF-IDF + LR validation_fpr_budget",
        "DeBERTa-v3-FT validation_fpr_budget",
        "TF-IDF → DeBERTa cascade validation_fpr_budget",
    ]
    raw = np.zeros((len(methods), len(display_metrics)))
    direction_adjusted = np.zeros((len(methods), len(display_metrics)))
    labels: list[list[str]] = []
    for row_index, method in enumerate(methods):
        row_labels = []
        for col_index, (axis, metric_name, _label) in enumerate(display_metrics):
            result = selected[(selected["method"] == method) & (selected["axis"] == axis)].iloc[0]
            value = float(result[metric_name])
            direction_adjusted[row_index, col_index] = 1.0 - value if metric_name == "benign_fpr" else value
            row_labels.append(f"{value:.1%}\nn={int(result['n'])}")
        labels.append(row_labels)
    fig, ax = plt.subplots(figsize=(12.0, 4.5), constrained_layout=True)
    image = ax.imshow(direction_adjusted, cmap="RdYlGn", vmin=0, vmax=1, aspect="auto")
    ax.set_xticks(range(len(display_metrics)), [entry[2] for entry in display_metrics], fontsize=10)
    ax.set_yticks(range(len(methods)), ["TF-IDF + LR", "DeBERTa-v3-FT", "TF-IDF → DeBERTa"], fontsize=10)
    for i in range(len(methods)):
        for j in range(len(display_metrics)):
            color = "black" if 0.2 < direction_adjusted[i, j] < 0.85 else "white"
            ax.text(j, i, labels[i][j], ha="center", va="center", fontsize=9, color=color)
    ax.set_title("PIDS-Bench v3 · seed 42 · thresholds selected on validation (FPR ≤ 1.5%)", fontsize=12)
    ax.set_xlabel("Metrics shown at each axis; numbers are raw rates")
    fig.colorbar(image, ax=ax, fraction=0.025, pad=0.02, label="Direction-adjusted score (higher is better)")
    fig.savefig(output / "comparison_matrix.png", dpi=200)
    plt.close(fig)

    # Balance benign and attack prompts so the timing sample does not depend on CSV row order.
    test_frame = frames["iid_test"]
    latency_count = min(args.latency_runs, len(test_frame))
    per_class = latency_count // 2
    latency_parts = [
        test_frame[test_frame["label"] == label].sample(n=per_class, random_state=42)
        for label in (0, 1)
    ]
    if latency_count % 2:
        remainder = test_frame[~test_frame.index.isin(pd.concat(latency_parts).index)]
        latency_parts.append(remainder.sample(n=1, random_state=42))
    latency_frame = pd.concat(latency_parts).sample(frac=1, random_state=42).reset_index(drop=True)
    latency_texts = latency_frame["text"].tolist()

    def tf_one(text: str) -> None:
        tfidf.predict_proba([text])

    def deb_one(text: str) -> None:
        transformer_scores(deberta, tokenizer, [text], 1, device)

    def cascade_one(text: str) -> None:
        tf_score = float(tfidf.predict_proba([text])[0, 1])
        if cascade_policy["tfidf_benign_max_inclusive"] < tf_score < cascade_policy["tfidf_attack_min_inclusive"]:
            transformer_scores(deberta, tokenizer, [text], 1, device)

    latency = {
        "device": str(device),
        "single_prompt_no_http": True,
        "iid_test_stratified_rows": len(latency_texts),
        "iid_test_stratified_label_counts": {
            str(int(label)): int(count) for label, count in latency_frame["label"].value_counts().sort_index().items()
        },
        "warmups_per_method": 10,
        "TF-IDF + LR": benchmark_latency(tf_one, latency_texts, device, 10, args.latency_runs),
        "DeBERTa-v3-FT": benchmark_latency(deb_one, latency_texts, device, 10, args.latency_runs),
        "TF-IDF → DeBERTa cascade": benchmark_latency(cascade_one, latency_texts, device, 10, args.latency_runs),
    }
    (output / "latency.json").write_text(json.dumps(latency, indent=2), encoding="utf-8")

    provenance = {
        "upstream_commit": "87dc835566b930ee921240874a4939b2c266c2fe",
        "seed": 42,
        "device": str(device),
        "model_input_manifest": str(model_manifest_path),
        "model_input_manifest_sha256": sha256(model_manifest_path),
        "deberta_base_checkpoint": {
            "model_id": base_checkpoint["model_id"],
            "revision": base_checkpoint["revision"],
            "license": base_checkpoint["license"],
            "files": base_checkpoint["files"],
        },
        "threshold_policy": thresholds,
        "dataset_hashes_and_counts": data_hashes,
        "tfidf_model_sha256": sha256(args.tfidf_model.resolve()),
        "deberta_model_file_sha256": model_files_hashes(deberta_path),
        "deberta_prediction_sources": deberta_prediction_sources,
        "evaluation_batch_size": args.batch_size,
        "latency_protocol": latency,
        "caveat": "Single local seed; hard-benign axis omits 664 blank license-redacted rows; latency is model inference only, not end-to-end HTTP proxy latency.",
    }
    (output / "evaluation_provenance.json").write_text(json.dumps(provenance, indent=2), encoding="utf-8")
    print(json.dumps({"thresholds": thresholds, "device": str(device), "metrics": selected.to_dict("records"), "latency": latency}, indent=2))


if __name__ == "__main__":
    main()
