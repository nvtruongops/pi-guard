#!/usr/bin/env python3
"""Compare the released PIGuard and ProtectAI checkpoints on one local split.

Measures one prompt per classifier call on CPU, including tokenization and
pipeline post-processing. The script intentionally writes only beside itself.
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import statistics
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline


WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
DATA_PATH = (
    WORKSPACE_ROOT
    / "replications"
    / "Paper_ACL2025_PIGuard_HaoLi"
    / "datasets"
    / "valid.json"
)
MODELS = (
    ("PIGuard", "leolee99/PIGuard", True),
    ("ProtectAI", "protectai/deberta-v3-base-prompt-injection-v2", False),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def predicted_class(label: str) -> int:
    value = label.strip().lower()
    if value in {"injection", "malicious", "unsafe", "label_1"}:
        return 1
    if value in {"benign", "safe", "label_0"}:
        return 0
    raise ValueError(f"Unrecognized model output label: {label!r}")


def evaluate(name: str, model_id: str, trust_remote_code: bool, samples: list[dict]) -> dict:
    tokenizer = AutoTokenizer.from_pretrained(model_id, model_max_length=512)
    model = AutoModelForSequenceClassification.from_pretrained(
        model_id, trust_remote_code=trust_remote_code
    )
    model.to("cpu")
    model.eval()
    classifier = pipeline(
        "text-classification",
        model=model,
        tokenizer=tokenizer,
        device=-1,
        truncation=True,
        batch_size=1,
    )

    for _ in range(5):
        classifier("Warmup prompt for CPU latency measurement.")

    y_true: list[int] = []
    y_pred: list[int] = []
    latencies_ms: list[float] = []
    raw_labels: dict[str, int] = {}
    for item in samples:
        started = time.perf_counter()
        output = classifier(item["prompt"])[0]
        latencies_ms.append((time.perf_counter() - started) * 1000.0)
        y_true.append(1 if item["label"] == 1 else 0)
        y_pred.append(predicted_class(output["label"]))
        raw_labels[output["label"]] = raw_labels.get(output["label"], 0) + 1

    tp = sum(y == 1 and p == 1 for y, p in zip(y_true, y_pred))
    tn = sum(y == 0 and p == 0 for y, p in zip(y_true, y_pred))
    fp = sum(y == 0 and p == 1 for y, p in zip(y_true, y_pred))
    fn = sum(y == 1 and p == 0 for y, p in zip(y_true, y_pred))
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0

    return {
        "name": name,
        "model_id": model_id,
        "model_revision": getattr(model.config, "_commit_hash", None),
        "model_id2label": model.config.id2label,
        "samples": len(samples),
        "confusion_matrix": {"TP": tp, "TN": tn, "FP": fp, "FN": fn},
        "accuracy": (tp + tn) / len(samples) if samples else 0.0,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "fpr": fp / (fp + tn) if fp + tn else 0.0,
        "latency_ms": {
            "scope": "single prompt call; tokenizer + model + pipeline post-processing",
            "mean": statistics.fmean(latencies_ms) if latencies_ms else 0.0,
            "median": statistics.median(latencies_ms) if latencies_ms else 0.0,
            "p95": float(np.percentile(latencies_ms, 95)) if latencies_ms else 0.0,
            "raw_per_sample": latencies_ms,
        },
        "raw_label_counts": raw_labels,
    }


def main() -> None:
    started_at = datetime.now(timezone.utc).isoformat()
    samples = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    results = [evaluate(name, model_id, remote, samples) for name, model_id, remote in MODELS]
    payload = {
        "metadata": {
            "started_at_utc": started_at,
            "finished_at_utc": datetime.now(timezone.utc).isoformat(),
            "device": "CPU",
            "torch_version": torch.__version__,
            "transformers_version": __import__("transformers").__version__,
            "python_version": platform.python_version(),
            "torch_num_threads": torch.get_num_threads(),
            "dataset_path": str(DATA_PATH),
            "dataset_sha256": sha256(DATA_PATH),
            "dataset_samples": len(samples),
            "dataset_labels": {
                str(label): sum(1 for row in samples if row["label"] == label)
                for label in sorted({row["label"] for row in samples})
            },
            "max_length": 512,
            "warmup_calls_per_model": 5,
            "offline_mode": os.environ.get("HF_HUB_OFFLINE", "0"),
        },
        "results": results,
    }
    out = Path(__file__).with_name("shared_validation_single_request_fresh.json")
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"output": str(out), "metadata": payload["metadata"], "results": [
        {k: v for k, v in r.items() if k != "latency_ms"} | {"latency_ms": {k: v for k, v in r["latency_ms"].items() if k != "raw_per_sample"}}
        for r in results
    ]}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
