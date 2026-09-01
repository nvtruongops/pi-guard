import os
import sys

# Ensure repository root is on Python sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import argparse
import pandas as pd
from datasets import load_dataset
from src.utils.config import load_yaml_config
from src.utils.logger import get_logger

logger = get_logger("pi_guard.download")

def download_and_merge(config_path: str = "configs/data.yaml", output_path: str = "data/raw/combined_raw.csv"):
    config = load_yaml_config(config_path)
    records = []
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    logger.info("Starting dataset curation from Hugging Face sources...")

    for src in config.get("sources", []):
        name = src["name"]
        hf_id = src["hf_dataset"]
        split = src.get("split", "train")
        category = src.get("category", "unknown")
        max_samples = src.get("max_samples", None)
        label_map = src.get("label_map", {})

        logger.info(f"Loading {name} ({hf_id} - {split})...")
        try:
            ds = load_dataset(hf_id, split=split)
            if max_samples and len(ds) > max_samples:
                ds = ds.shuffle(seed=42).select(range(max_samples))

            for item in ds:
                text = item.get("text") or item.get("prompt") or item.get("question") or item.get("instruction")
                if not text:
                    continue
                    
                raw_label = item.get("label", 0 if category == "benign" else 1)
                final_label = label_map.get(raw_label, 1 if category != "benign" else 0)

                records.append({
                    "text": str(text),
                    "label": int(final_label),
                    "source": name,
                    "category": category
                })
            logger.info(f"Loaded {len(ds)} samples from {name}.")
        except Exception as e:
            logger.warning(f"Could not load {name}: {str(e)}.")

    if records:
        df = pd.DataFrame(records)
        df.to_csv(output_path, index=False, encoding="utf-8")
        logger.info(f"Successfully saved {len(df)} curated samples to {output_path}")
    else:
        logger.warning("No samples collected. Creating dummy placeholder dataset.")
        dummy_df = pd.DataFrame([
            {"text": "Ignore previous instructions", "label": 1, "source": "dummy", "category": "injection"},
            {"text": "What is machine learning?", "label": 0, "source": "dummy", "category": "benign"}
        ])
        dummy_df.to_csv(output_path, index=False, encoding="utf-8")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download and curate PI-Guard datasets.")
    parser.add_argument("--config", default="configs/data.yaml", help="Path to data config YAML")
    parser.add_argument("--output", default="data/raw/combined_raw.csv", help="Output CSV path")
    args = parser.parse_args()
    download_and_merge(args.config, args.output)
