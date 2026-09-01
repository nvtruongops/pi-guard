import os
import sys

# Ensure repository root is on Python sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
import argparse
import joblib
import pandas as pd
from src.evaluation.metrics import EvaluationMetrics
from src.utils.logger import get_logger

logger = get_logger("pi_guard.evaluate")

def evaluate_model(
    model_path: str = "models/baseline/baseline_tfidf.joblib",
    test_path: str = "data/splits/test.csv",
    output_report_path: str = "reports/experiment_reports/baseline_test_metrics.json"
):
    if not os.path.exists(model_path) or not os.path.exists(test_path):
        logger.error("Model or test split not found. Ensure training has completed.")
        return

    os.makedirs(os.path.dirname(output_report_path), exist_ok=True)
    logger.info(f"Loading model from {model_path} and test set from {test_path}...")

    model = joblib.load(model_path)
    test_df = pd.read_csv(test_path)

    y_true = test_df["label"].astype(int).tolist()
    y_pred = model.predict(test_df["text"].astype(str)).tolist()
    
    y_probs = None
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(test_df["text"].astype(str))
        y_probs = [float(p[1]) for p in probs]

    metrics = EvaluationMetrics.compute_all(y_true, y_pred, y_probs)
    
    with open(output_report_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    logger.info(f"Evaluation Results:\nAccuracy: {metrics['accuracy']:.4f}\nF1-Score: {metrics['f1_score']:.4f}\nFPR: {metrics['false_positive_rate_fpr']:.4f}")
    logger.info(f"Report saved to {output_report_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate trained PI-Guard models.")
    parser.add_argument("--model", default="models/baseline/baseline_tfidf.joblib")
    parser.add_argument("--test", default="data/splits/test.csv")
    parser.add_argument("--output", default="reports/experiment_reports/baseline_test_metrics.json")
    args = parser.parse_args()
    evaluate_model(args.model, args.test, args.output)
