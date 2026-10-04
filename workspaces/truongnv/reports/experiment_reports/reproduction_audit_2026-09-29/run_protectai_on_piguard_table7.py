#!/usr/bin/env python3
"""Evaluate the released ProtectAI checkpoint on PIGuard's local Table 7 sets."""

from __future__ import annotations

import hashlib
import json
import platform
import time
from datetime import datetime, timezone
from pathlib import Path

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline


WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = WORKSPACE_ROOT / "replications" / "Paper_ACL2025_PIGuard_HaoLi" / "datasets"
MODEL_ID = "protectai/deberta-v3-base-prompt-injection-v2"
PAPER_RESULTS = {
    "NotInject_one": 77.88,
    "NotInject_two": 47.79,
    "NotInject_three": 46.02,
    "WildGuard_benign": 75.18,
    "BIPIA_injection": 8.67,
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_texts() -> tuple[dict[str, list[str]], dict[str, str]]:
    sets: dict[str, list[str]] = {}
    hashes: dict[str, str] = {}
    for name in ("NotInject_one", "NotInject_two", "NotInject_three"):
        path = DATA_DIR / f"{name}.json"
        sets[name] = [row["prompt"] for row in json.loads(path.read_text(encoding="utf-8"))]
        hashes[str(path)] = sha256(path)
    path = DATA_DIR / "wildguard.json"
    sets["WildGuard_benign"] = [row["prompt"] for row in json.loads(path.read_text(encoding="utf-8"))]
    hashes[str(path)] = sha256(path)
    for name in ("BIPIA_text", "BIPIA_code"):
        path = DATA_DIR / f"{name}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        sets[name] = [sample for values in data.values() for sample in values]
        hashes[str(path)] = sha256(path)
    return sets, hashes


def evaluate(classifier, name: str, prompts: list[str], target_label: str) -> dict:
    correct = 0
    wrong = []
    started = time.perf_counter()
    for offset in range(0, len(prompts), 32):
        batch = prompts[offset : offset + 32]
        predictions = classifier(batch)
        for prompt, result in zip(batch, predictions):
            is_correct = result["label"].strip().upper() == target_label
            correct += int(is_correct)
            if not is_correct and len(wrong) < 5:
                wrong.append({
                    "prompt": prompt[:200],
                    "predicted_label": result["label"],
                    "score": float(result["score"]),
                })
    accuracy = 100.0 * correct / len(prompts) if prompts else 0.0
    paper = PAPER_RESULTS.get(name)
    return {
        "samples": len(prompts),
        "target_label": target_label,
        "correct": correct,
        "accuracy_pct": round(accuracy, 2),
        "paper_protectai_table7_pct": paper,
        "delta_percentage_points": round(accuracy - paper, 2) if paper is not None else None,
        "elapsed_sec": round(time.perf_counter() - started, 3),
        "sample_errors": wrong,
    }


def main() -> None:
    started_at = datetime.now(timezone.utc).isoformat()
    datasets, hashes = load_texts()
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, model_max_length=512)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_ID)
    model.to("cpu")
    model.eval()
    classifier = pipeline(
        "text-classification",
        model=model,
        tokenizer=tokenizer,
        device=-1,
        truncation=True,
        batch_size=32,
    )
    for _ in range(5):
        classifier(["Warmup prompt for CPU benchmark."])

    results = {
        "NotInject_one": evaluate(classifier, "NotInject_one", datasets["NotInject_one"], "SAFE"),
        "NotInject_two": evaluate(classifier, "NotInject_two", datasets["NotInject_two"], "SAFE"),
        "NotInject_three": evaluate(classifier, "NotInject_three", datasets["NotInject_three"], "SAFE"),
        "WildGuard_benign": evaluate(classifier, "WildGuard_benign", datasets["WildGuard_benign"], "SAFE"),
        "BIPIA_text": evaluate(classifier, "BIPIA_text", datasets["BIPIA_text"], "INJECTION"),
        "BIPIA_code": evaluate(classifier, "BIPIA_code", datasets["BIPIA_code"], "INJECTION"),
    }
    bipia_n = results["BIPIA_text"]["samples"] + results["BIPIA_code"]["samples"]
    bipia_ok = results["BIPIA_text"]["correct"] + results["BIPIA_code"]["correct"]
    notinject_n = sum(results[k]["samples"] for k in ("NotInject_one", "NotInject_two", "NotInject_three"))
    notinject_ok = sum(results[k]["correct"] for k in ("NotInject_one", "NotInject_two", "NotInject_three"))
    results["NotInject_overall_weighted"] = {
        "samples": notinject_n,
        "accuracy_pct": round(100.0 * notinject_ok / notinject_n, 2),
    }
    results["BIPIA_overall_weighted"] = {
        "samples": bipia_n,
        "accuracy_pct": round(100.0 * bipia_ok / bipia_n, 2),
    }
    payload = {
        "metadata": {
            "started_at_utc": started_at,
            "finished_at_utc": datetime.now(timezone.utc).isoformat(),
            "model_id": MODEL_ID,
            "model_revision": getattr(model.config, "_commit_hash", None),
            "model_id2label": model.config.id2label,
            "device": "CPU",
            "torch_version": torch.__version__,
            "transformers_version": __import__("transformers").__version__,
            "python_version": platform.python_version(),
            "torch_num_threads": torch.get_num_threads(),
            "batch_size": 32,
            "max_length": 512,
            "dataset_hashes_sha256": hashes,
            "dataset_counts": {name: len(texts) for name, texts in datasets.items()},
            "total_evaluation_rows": sum(len(texts) for texts in datasets.values()),
            "paper_source": "https://aclanthology.org/2025.acl-long.1468.pdf (Table 7)",
            "limitation": "PINT is not included; it is not publicly released by the paper authors.",
        },
        "results": results,
    }
    out = Path(__file__).with_name("protectai_shared_table7_fresh.json")
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"output": str(out), **payload}, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
