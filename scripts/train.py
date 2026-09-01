import os
import sys

# Ensure repository root is on Python sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import argparse
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

from src.utils.config import load_yaml_config
from src.utils.logger import get_logger

logger = get_logger("pi_guard.train")

def train_baseline(
    splits_dir: str = "data/splits",
    config_path: str = "configs/training.yaml",
    output_model_path: str = "models/baseline/baseline_tfidf.joblib"
):
    train_path = os.path.join(splits_dir, "train.csv")
    val_path = os.path.join(splits_dir, "val.csv")

    if not os.path.exists(train_path):
        logger.error(f"Train split not found at {train_path}. Run preprocess.py first.")
        return

    config = load_yaml_config(config_path)["baseline"]
    os.makedirs(os.path.dirname(output_model_path), exist_ok=True)

    train_df = pd.read_csv(train_path)
    val_df = pd.read_csv(val_path)

    logger.info(f"Building Baseline Feature Pipeline (Word + Char TF-IDF)...")
    word_vec = TfidfVectorizer(
        ngram_range=tuple(config["word_ngram_range"]),
        max_features=config["word_max_features"],
        sublinear_tf=config["sublinear_tf"]
    )
    char_vec = TfidfVectorizer(
        analyzer="char_wb",
        ngram_range=tuple(config["char_ngram_range"]),
        max_features=config["char_max_features"],
        sublinear_tf=config["sublinear_tf"]
    )
    features = FeatureUnion([("word_tfidf", word_vec), ("char_tfidf", char_vec)])

    clf_cfg = config["classifier"]
    classifier = LogisticRegression(
        C=clf_cfg["C"],
        max_iter=clf_cfg["max_iter"],
        class_weight=clf_cfg["class_weight"],
        solver=clf_cfg["solver"]
    )

    pipeline = Pipeline([("features", features), ("classifier", classifier)])

    logger.info(f"Training Logistic Regression Baseline on {len(train_df)} samples...")
    pipeline.fit(train_df["text"].astype(str), train_df["label"].astype(int))

    logger.info("Evaluating on validation split...")
    val_preds = pipeline.predict(val_df["text"].astype(str))
    print(classification_report(val_df["label"].astype(int), val_preds))

    joblib.dump(pipeline, output_model_path)
    logger.info(f"Baseline model checkpoint successfully saved to {output_model_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train PI-Guard models.")
    parser.add_argument("--model", default="baseline", choices=["baseline", "transformer"])
    parser.add_argument("--config", default="configs/training.yaml")
    parser.add_argument("--splits_dir", default="data/splits")
    parser.add_argument("--output", default="models/baseline/baseline_tfidf.joblib")
    args = parser.parse_args()

    if args.model == "baseline":
        train_baseline(args.splits_dir, args.config, args.output)
    else:
        logger.info("Transformer training should be invoked via notebooks/03_transformer_training.ipynb or dedicated GPU trainer.")
