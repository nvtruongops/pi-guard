#!/usr/bin/env python3
"""Run a full L2 validation experiment with normalized sqrt-balanced weights."""
from __future__ import annotations

import copy
import hashlib
import json
import math
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
PRIVATE = REPO / "workspaces" / "truongnv" / "pi_guard_pipeline"
TRAINING = PRIVATE / "training_bases"
ADAPTER_DIR = TRAINING / "pi_guard_tfidf_tier1"
ADAPTER_PATH = ADAPTER_DIR / "fit_l2_curated.py"
LEGACY_PATH = ADAPTER_DIR / "fit_l2_v8.py"
PACKAGE = TRAINING / "datasets" / "project_training" / "versions" / "pi_guard_native_reference_round07_20261013_r01"
PROTOCOL = ROOT / "AUTONOMOUS_PROTOCOL.json"
OUTPUT = ADAPTER_DIR / "runs" / "l2_sqrt_class_weight_round07_r01_full_20261013"
REPORT = ROOT / "l2_sqrt_class_weight_validation_round07_r01.json"
LABELS = ("benign", "PI", "JB")
LABEL_IDS = {"benign": 0, "PI": 1, "JB": 2}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalized_sqrt_balanced(counts: dict[int, int]) -> dict[int, float]:
    total = sum(counts.values())
    if total <= 0 or set(counts) != set(LABEL_IDS.values()) or any(v <= 0 for v in counts.values()):
        raise ValueError("SQRT_BALANCED_REQUIRES_POSITIVE_SUPPORT_FOR_ALL_CLASSES")
    raw = {label_id: math.sqrt(total / (len(counts) * count))
           for label_id, count in counts.items()}
    mean_weight = sum(counts[label_id] * raw[label_id] for label_id in counts) / total
    return {label_id: value / mean_weight for label_id, value in raw.items()}


def main() -> int:
    if REPORT.exists() or OUTPUT.exists():
        raise FileExistsError("EXPERIMENT_PATH_EXISTS; inspect it and create a new version")
    if not OUTPUT.resolve(strict=False).is_relative_to(PRIVATE.resolve(strict=True)):
        raise ValueError("OUTPUT_OUTSIDE_PRIVATE_WORKSPACE")

    sys.path.insert(0, str(ADAPTER_DIR))
    import fit_l2_curated as adapter
    import sklearn

    preflight, context = adapter.preflight(PACKAGE, PROTOCOL, OUTPUT)
    print("PREFLIGHT", preflight["status"], json.dumps(preflight["blockers"]), flush=True)
    if context is None:
        raise RuntimeError("L2_PREFLIGHT_BLOCKED")

    train_meta = context["split"]["partitions"]["train"]
    counts = {label_id: sum(item["label"] == label for item in train_meta)
              for label, label_id in LABEL_IDS.items()}
    class_weight = normalized_sqrt_balanced(counts)
    base_config = copy.deepcopy(context["manifest"]["baseline"])
    variant_config = copy.deepcopy(base_config)
    variant_config["classifier"]["class_weight"] = class_weight
    context["manifest"]["baseline"] = variant_config

    print("VARIANT", json.dumps({
        "method": "sqrt_of_sklearn_balanced_weights_normalized_to_unit_train_mean",
        "label_counts": {label: counts[label_id] for label, label_id in LABEL_IDS.items()},
        "base_class_weight": base_config["classifier"]["class_weight"],
        "variant_class_weight": {LABELS[label_id]: value for label_id, value in class_weight.items()},
        "test_opened": False,
        "l3_run": False,
    }), flush=True)

    result = adapter.fit(context)
    run_dir = Path(result["run"])
    run_manifest_path = run_dir / "run_manifest.json"
    run_manifest = json.loads(run_manifest_path.read_text(encoding="utf-8"))
    run_manifest["model_variant"] = {
        "method": "sqrt_of_sklearn_balanced_weights_normalized_to_unit_train_mean",
        "baseline_config": base_config,
        "variant_config": variant_config,
        "train_label_counts": {label: counts[label_id] for label, label_id in LABEL_IDS.items()},
        "class_weight_by_label": {LABELS[label_id]: value for label_id, value in class_weight.items()},
    }
    run_manifest_path.write_text(json.dumps(run_manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                                 encoding="utf-8", newline="\n")

    metrics = json.loads((run_dir / "metrics.json").read_text(encoding="utf-8"))
    report = {
        "report_id": "l2_sqrt_class_weight_validation_round07_r01",
        "status": result["status"],
        "scope": "full fixed-package train/validation L2 fit; native reference labels, not human gold",
        "package_id": context["manifest"]["package_id"],
        "dataset_version": context["manifest"]["dataset_version"],
        "package_manifest_sha256": sha256(PACKAGE / "DATASET_MANIFEST.json"),
        "adapter_sha256": sha256(ADAPTER_PATH),
        "legacy_helper_sha256": sha256(LEGACY_PATH),
        "run_manifest_sha256": sha256(run_manifest_path),
        "run_path_private": str(run_dir),
        "sklearn_version": sklearn.__version__,
        "model_variant": run_manifest["model_variant"],
        "metrics": metrics,
        "formal_acceptance_gate": "GATE_UNSPECIFIED",
        "test_opened": False,
        "l3_run": False,
        "row_ids_or_text_emitted": False,
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                      encoding="utf-8", newline="\n")
    print("EXPERIMENT_COMPLETE", json.dumps({
        "status": result["status"],
        "macro_f1": metrics["macro_f1"],
        "benign_fpr": metrics["benign_fpr"]["value"],
        "per_class": metrics["per_class"],
        "selected_pair": metrics["routing_threshold_sweep"]["selected_pair"],
        "test_opened": False,
        "l3_run": False,
        "report": str(REPORT),
    }, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
