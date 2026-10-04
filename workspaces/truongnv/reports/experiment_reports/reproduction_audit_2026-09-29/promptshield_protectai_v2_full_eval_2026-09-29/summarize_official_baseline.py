import json
import sys
from pathlib import Path

import numpy as np
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support

promptshield_root = Path(
    r"D:/Work/Do-an/workspaces/truongnv/replications/PromptShield_Jacob_CCS2024/PromptShield"
)
sys.path.insert(0, str(promptshield_root))
from utils.metrics import computeROC, interpolateROC, interpolateThre

run_root = Path(__file__).resolve().parent
npz_path = (
    run_root
    / "baseline_evals/protectai-v2/evaluation_benchmark/2026-09-29/trial_1/evaluation_benchmark_outputs.npz"
)
dataset_path = run_root / "data/evaluation_data/2024-11-28/2024-11-28_evaluation_benchmark.json"
order_path = run_root / "promptshield_eval_row_order.json"

with np.load(npz_path) as result:
    scores = np.asarray(result["scores_prompt_injection"], dtype=np.float64)
    predictions = np.asarray(result["preds"], dtype=np.int64)
    labels = np.asarray(result["labels"], dtype=np.int64)
    model_name = str(result["model_name"].item())
    dataset_name = str(result["dataset_name"].item())

rows = json.loads(dataset_path.read_text(encoding="utf-8"))
order = json.loads(order_path.read_text(encoding="utf-8"))
source_labels = np.asarray([row["flag"] for row in rows], dtype=np.int64)
expected_sorted_labels = source_labels[np.asarray(order, dtype=np.int64)]

if not (len(scores) == len(predictions) == len(labels) == len(rows) == len(order)):
    raise ValueError("Output, label, and source row counts do not agree")
if sorted(order) != list(range(len(rows))):
    raise ValueError("Recorded row order is not a complete permutation")
if not np.array_equal(labels, expected_sorted_labels):
    raise ValueError("Saved output labels do not align with source rows via the recorded permutation")

cm = confusion_matrix(labels, predictions, labels=[0, 1])
tn, fp, fn, tp = (int(value) for value in cm.ravel())
precision, recall, f1, _ = precision_recall_fscore_support(
    labels, predictions, average="binary", zero_division=0
)
fpr_curve, tpr_curve, thresholds, auc = computeROC(scores, labels)

targets = [0.01, 0.005, 0.001, 0.0005]
low_fpr = {}
for target in targets:
    key = f"{target * 100:g}%"
    low_fpr[key] = {
        "target_fpr": target,
        "interpolated_tpr": float(interpolateROC(target, fpr_curve, tpr_curve)),
        "interpolated_threshold": float(interpolateThre(target, fpr_curve, thresholds)),
    }

summary = {
    "status": "completed",
    "model_name": model_name,
    "dataset_name": dataset_name,
    "sample_count": len(rows),
    "class_counts": {
        "benign": int(np.count_nonzero(labels == 0)),
        "injection": int(np.count_nonzero(labels == 1)),
    },
    "argmax_confusion_matrix": {"tn": tn, "fp": fp, "fn": fn, "tp": tp},
    "argmax_metrics": {
        "accuracy": float((tn + tp) / len(labels)),
        "precision": float(precision),
        "recall": float(recall),
        "f1": float(f1),
        "fpr": float(fp / (fp + tn)),
    },
    "roc_auc": float(auc),
    "low_fpr_interpolated_metrics": low_fpr,
    "alignment_validation": {
        "source_rows": len(rows),
        "saved_rows": len(labels),
        "row_order_is_permutation": True,
        "saved_labels_match_source_rows_in_recorded_order": True,
    },
}

output_path = run_root / "summary.json"
output_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
print(json.dumps(summary, indent=2))
