import os
import sys

# Ensure repository root is on Python sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import argparse
import hashlib
import pandas as pd
from src.preprocessing.cleaner import TextCleaner
from src.datasets.splitter import DatasetSplitter
from src.utils.config import load_yaml_config
from src.utils.logger import get_logger

logger = get_logger("pi_guard.preprocess")

def preprocess_and_split(
    input_path: str = "data/raw/combined_raw.csv",
    splits_dir: str = "data/splits",
    config_path: str = "configs/data.yaml"
):
    if not os.path.exists(input_path):
        logger.error(f"Input file not found: {input_path}. Please run download_dataset.py first.")
        return

    config = load_yaml_config(config_path)
    os.makedirs(splits_dir, exist_ok=True)

    logger.info(f"Loading raw dataset from {input_path}...")
    df = pd.read_csv(input_path)

    # 1. Clean & normalize
    df["text"] = df["text"].astype(str).apply(TextCleaner.normalize)
    df = df[df["text"].apply(lambda x: TextCleaner.is_valid_sample(x, min_len=4))].copy()

    # 2. Deduplication
    initial_len = len(df)
    df = df.drop_duplicates(subset=["text"]).reset_index(drop=True)
    logger.info(f"Deduplicated {initial_len} -> {len(df)} unique samples.")

    # 3. Create clustering group key
    df["cluster_id"] = df["text"].apply(lambda x: hashlib.md5(x[:35].encode()).hexdigest()[:8])

    # 4. Group-aware splitting
    train_df, val_df, test_df = DatasetSplitter.split_group_aware(
        df,
        group_col="cluster_id",
        test_size=config["splitting"].get("test_ratio", 0.15),
        val_size=config["splitting"].get("val_ratio", 0.15)
    )

    # 5. Save splits
    train_df.to_csv(os.path.join(splits_dir, "train.csv"), index=False, encoding="utf-8")
    val_df.to_csv(os.path.join(splits_dir, "val.csv"), index=False, encoding="utf-8")
    test_df.to_csv(os.path.join(splits_dir, "test.csv"), index=False, encoding="utf-8")

    logger.info(f"Splits saved: Train={len(train_df)}, Val={len(val_df)}, Test={len(test_df)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preprocess and split datasets.")
    parser.add_argument("--input", default="data/raw/combined_raw.csv")
    parser.add_argument("--splits_dir", default="data/splits")
    parser.add_argument("--config", default="configs/data.yaml")
    args = parser.parse_args()
    preprocess_and_split(args.input, args.splits_dir, args.config)
