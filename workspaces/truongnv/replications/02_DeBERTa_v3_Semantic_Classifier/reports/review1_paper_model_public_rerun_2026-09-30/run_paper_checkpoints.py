#!/usr/bin/env python3
"""Run pinned public detector checkpoints over the PIGuard paper's public assets."""

from __future__ import annotations

import gzip
import hashlib
import json
import platform
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import torch
import transformers
from transformers import AutoModelForSequenceClassification, AutoTokenizer

ROOT = Path(__file__).resolve().parents[4]
PAPER_ROOT = ROOT / "replications" / "Paper_ACL2025_PIGuard_HaoLi" / "PIGuard_ACL2025"
DATA_ROOT = PAPER_ROOT / "datasets"
OUT = Path(__file__).resolve().parent
BATCH_SIZE = 16
MAX_BATCHES_PER_MODEL = None
MODEL_KEY = "piguard_acl2025"
MODEL_REPO = "leolee99/PIGuard"
MODEL_REVISION = "dd78b24e330193a22d2293ac66922dd4f982f563"
MAX_LENGTH = 2048


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_rows() -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    manifests: dict[str, dict[str, Any]] = {}
    sources = [
        ("NotInject_one", "NotInject_one.json", "notinject", 0),
        ("NotInject_two", "NotInject_two.json", "notinject", 0),
        ("NotInject_three", "NotInject_three.json", "notinject", 0),
        ("BIPIA_text", "BIPIA_text.json", "bipia_payload", 1),
        ("BIPIA_code", "BIPIA_code.json", "bipia_payload", 1),
        ("WildGuard_benign", "wildguard.json", "wildguard_benign", 0),
    ]
    for group, filename, benchmark, label in sources:
        path = DATA_ROOT / filename
        value = json.loads(path.read_text(encoding="utf-8"))
        manifests[filename] = {"path": str(path.relative_to(ROOT)), "sha256": sha256(path)}
        if group.startswith("NotInject"):
            for index, item in enumerate(value):
                rows.append({"id": f"{group}:{index}", "benchmark": "NotInject", "subset": group, "text": item["prompt"], "label": label})
        elif group.startswith("BIPIA"):
            for category, payloads in value.items():
                for index, payload in enumerate(payloads):
                    rows.append({"id": f"{group}:{category}:{index}", "benchmark": "BIPIA_payload", "subset": group, "category": category, "text": payload, "label": label})
        else:
            for index, item in enumerate(value):
                rows.append({"id": f"{group}:{index}", "benchmark": "WildGuard_benign", "subset": group, "text": item["prompt"], "label": label})
    return rows, manifests


def normalized_label(value: str) -> str:
    return " ".join(value.strip().lower().replace("_", " ").replace("-", " ").split())


def positive_label_id(model: Any) -> int:
    labels = {int(key): str(value) for key, value in model.config.id2label.items()}
    positive = [idx for idx, label in labels.items() if normalized_label(label) in {"injection", "prompt injection", "jailbreak", "unsafe", "malicious"}]
    negative = [idx for idx, label in labels.items() if normalized_label(label) in {"safe", "benign", "clean"}]
    if len(positive) != 1 or len(negative) != 1:
        raise ValueError(f"Unrecognized or ambiguous label schema: {labels!r}")
    return positive[0]


def compute_metrics(predictions: list[dict[str, Any]]) -> dict[str, Any]:
    groups: dict[str, list[dict[str, Any]]] = {}
    for prediction in predictions:
        groups.setdefault(prediction["benchmark"], []).append(prediction)
    output: dict[str, Any] = {}
    for benchmark, group in groups.items():
        tp = sum(row["label"] == 1 and row["prediction"] == 1 for row in group)
        tn = sum(row["label"] == 0 and row["prediction"] == 0 for row in group)
        fp = sum(row["label"] == 0 and row["prediction"] == 1 for row in group)
        fn = sum(row["label"] == 1 and row["prediction"] == 0 for row in group)
        output[benchmark] = {
            "n": len(group), "tp": tp, "tn": tn, "fp": fp, "fn": fn,
            "accuracy": (tp + tn) / len(group),
            "attack_recall": tp / (tp + fn) if tp + fn else None,
            "benign_accuracy": tn / (tn + fp) if tn + fp else None,
        }
    notinject_subsets: dict[str, Any] = {}
    for subset in ("NotInject_one", "NotInject_two", "NotInject_three"):
        group = [row for row in predictions if row["subset"] == subset]
        tn = sum(row["prediction"] == 0 for row in group)
        notinject_subsets[subset] = {"n": len(group), "benign_accuracy": tn / len(group)}
    bipia_subsets: dict[str, Any] = {}
    for subset in ("BIPIA_text", "BIPIA_code"):
        group = [row for row in predictions if row["subset"] == subset]
        tp = sum(row["prediction"] == 1 for row in group)
        bipia_subsets[subset] = {"n": len(group), "attack_recall": tp / len(group)}
    output["NotInject_subsets"] = notinject_subsets
    output["BIPIA_subsets"] = bipia_subsets
    return output


def run_model(rows: list[dict[str, Any]]) -> dict[str, Any]:
    started = datetime.now(timezone.utc).isoformat()
    repo_id, revision = MODEL_REPO, MODEL_REVISION
    print(f"[{MODEL_KEY}] loading {repo_id}@{revision}", flush=True)
    tokenizer = AutoTokenizer.from_pretrained(
        repo_id, revision=revision, model_max_length=MAX_LENGTH
    )
    model = AutoModelForSequenceClassification.from_pretrained(
        repo_id, revision=revision, trust_remote_code=True
    )
    model.to("cpu")
    model.eval()
    pos_id = positive_label_id(model)
    id2label = {int(index): str(label) for index, label in model.config.id2label.items()}
    max_length = MAX_LENGTH
    torch.set_num_threads(min(8, torch.get_num_threads()))
    outputs: list[dict[str, Any]] = []
    elapsed = 0.0
    batches = 0
    for start in range(0, len(rows), BATCH_SIZE):
        if MAX_BATCHES_PER_MODEL is not None and batches >= MAX_BATCHES_PER_MODEL:
            break
        batch = rows[start : start + BATCH_SIZE]
        begin = time.perf_counter()
        inputs = tokenizer([row["text"] for row in batch], padding=True, truncation=True, max_length=max_length, return_tensors="pt")
        with torch.inference_mode():
            logits = model(**inputs).logits.float()
            probabilities = torch.softmax(logits, dim=-1).cpu().tolist()
        elapsed += time.perf_counter() - begin
        for row, probs in zip(batch, probabilities):
            prediction = int(max(range(len(probs)), key=lambda index: probs[index]))
            outputs.append({
                "id": row["id"], "benchmark": row["benchmark"], "subset": row["subset"],
                "category": row.get("category"), "label": row["label"], "prediction": int(prediction == pos_id),
                "attack_probability": round(float(probs[pos_id]), 8), "predicted_class_id": prediction,
            })
        batches += 1
        if batches % 10 == 0 or start + len(batch) == len(rows):
            print(f"[{MODEL_KEY}] {len(outputs)}/{len(rows)} rows", flush=True)
    result = {
        "model_id": repo_id, "requested_revision": revision,
        "resolved_revision": getattr(model.config, "_commit_hash", None),
        "id2label": {str(key): value for key, value in id2label.items()},
        "positive_class_id": pos_id, "max_length": max_length,
        "parameter_count": sum(parameter.numel() for parameter in model.parameters()),
        "model_type": getattr(model.config, "model_type", None),
        "device": "CPU", "batch_size": BATCH_SIZE, "torch_threads": torch.get_num_threads(),
        "row_count": len(outputs), "expected_row_count": len(rows),
        "inference_seconds_batch_amortized": round(elapsed, 4),
        "rows_per_second_batch_amortized": round(len(outputs) / elapsed, 4) if elapsed else None,
        "metrics": compute_metrics(outputs), "predictions": outputs,
        "started_at_utc": started, "finished_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    del model, tokenizer
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return result


def main() -> None:
    rows, dataset_manifest = load_rows()
    manifest_path = OUT / "run_manifest.json"
    manifest = {
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(), "torch": torch.__version__,
        "transformers": transformers.__version__, "device": "CPU",
        "paper_code_upstream_repo": "https://github.com/leolee99/PIGuard",
        "paper_code_upstream_revision": "1b5751e88bf7475acbedfc8eda795ce060307c84",
        "paper_code_files": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (PAPER_ROOT / "eval_hf.py", PAPER_ROOT / "PIGuard.py")
        },
        "paper_pdf_path": str((ROOT / "replications" / "Paper_ACL2025_PIGuard_HaoLi" / "papers" / "PIGuard_2025_Prompt_Injection_Guardrail_ACL.pdf").relative_to(ROOT)),
        "paper_pdf_sha256": sha256(ROOT / "replications" / "Paper_ACL2025_PIGuard_HaoLi" / "papers" / "PIGuard_2025_Prompt_Injection_Guardrail_ACL.pdf"),
        "runner_path": str(Path(__file__).resolve().relative_to(ROOT)),
        "runner_sha256": sha256(Path(__file__).resolve()),
        "dataset_files": dataset_manifest, "input_rows": len(rows), "batch_size": BATCH_SIZE,
        "model_runs": {},
        "protocol_limitations": [
            "PINT is unavailable in the public source bundle and is omitted; the paper's full composite score cannot be reproduced.",
            "BIPIA rows are the released payload strings used by the paper code, not task+context concatenations.",
            "These public assets include no Direct or original JailbreakBench test examples.",
            "This is single-checkpoint inference; no cascade or routing behavior is measured.",
            "The official PIGuard Hugging Face runner explicitly sets tokenizer model_max_length=2048.",
        ],
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    run = run_model(rows)
    prediction_path = OUT / f"predictions_{MODEL_KEY}_maxlen{run['max_length']}.jsonl.gz"
    with gzip.open(prediction_path, "wt", encoding="utf-8", newline="\n") as stream:
        for prediction in run.pop("predictions"):
            stream.write(json.dumps(prediction, ensure_ascii=False, separators=(",", ":")) + "\n")
    run["predictions_path"] = prediction_path.name
    run["predictions_sha256"] = sha256(prediction_path)
    manifest["model_runs"][MODEL_KEY] = run
    manifest["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[{MODEL_KEY}] completed; rows={run['row_count']} hash={run['predictions_sha256']}", flush=True)
    print(f"wrote {manifest_path}", flush=True)


if __name__ == "__main__":
    main()
