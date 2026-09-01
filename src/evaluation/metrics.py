from typing import Any

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


class EvaluationMetrics:
    """Standardized metric calculation and error analysis for PI-Guard models."""

    @staticmethod
    def compute_all(
        y_true: list[int],
        y_pred: list[int],
        y_probs: list[float] | None = None
    ) -> dict[str, Any]:
        y_t = np.array(y_true)
        y_p = np.array(y_pred)

        tn, fp, fn, tp = confusion_matrix(y_t, y_p).ravel()
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0

        metrics = {
            "accuracy": float(accuracy_score(y_t, y_p)),
            "precision": float(precision_score(y_t, y_p, zero_division=0)),
            "recall_tpr": float(recall_score(y_t, y_p, zero_division=0)),
            "f1_score": float(f1_score(y_t, y_p, zero_division=0)),
            "false_positive_rate_fpr": float(fpr),
            "confusion_matrix": {
                "true_negatives": int(tn),
                "false_positives": int(fp),
                "false_negatives": int(fn),
                "true_positives": int(tp)
            }
        }

        if y_probs is not None:
            try:
                metrics["roc_auc"] = float(roc_auc_score(y_t, y_probs))
            except Exception:
                metrics["roc_auc"] = None

        return metrics
