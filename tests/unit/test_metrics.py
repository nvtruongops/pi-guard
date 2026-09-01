import pytest
from src.evaluation.metrics import EvaluationMetrics

def test_evaluation_metrics_computation():
    y_true = [0, 0, 1, 1, 0]
    y_pred = [0, 0, 1, 0, 0]
    y_probs = [0.1, 0.2, 0.9, 0.4, 0.05]

    res = EvaluationMetrics.compute_all(y_true, y_pred, y_probs)
    assert "accuracy" in res
    assert "precision" in res
    assert "recall_tpr" in res
    assert "false_positive_rate_fpr" in res
    assert res["false_positive_rate_fpr"] == 0.0  # 0 false positives among 3 negatives
    assert res["accuracy"] == 0.8
