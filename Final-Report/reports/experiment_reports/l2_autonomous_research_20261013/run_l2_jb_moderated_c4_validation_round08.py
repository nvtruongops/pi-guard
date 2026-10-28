#!/usr/bin/env python3
"""Run full L2 train/validation fit of JB-moderated weights at C=4.0."""
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
OUTPUT = ADAPTER_DIR / "runs" / "l2_jb_moderated_c4_validation_round08_r01_full_20261013"
REPORT = ROOT / "l2_jb_moderated_c4_validation_round08_r01.json"
LABELS = ("benign", "PI", "JB")
LABEL_IDS = {"benign": 0, "PI": 1, "JB": 2}
BASELINE_METRICS = ADAPTER_DIR / "runs" / "l2_round07_r01_full_20261013" / "metrics.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def moderated_balanced(counts: dict[int, int]) -> dict[int, float]:
    total = sum(counts.values())
    if total <= 0 or set(counts) != set(LABEL_IDS.values()) or any(v <= 0 for v in counts.values()):
        raise ValueError("MODERATED_WEIGHT_REQUIRES_POSITIVE_SUPPORT_FOR_ALL_CLASSES")
    balanced = {label_id: total / (len(counts) * count)
                for label_id, count in counts.items()}
    # Keep the baseline benign:PI ratio, but reduce JB to the geometric midpoint
    # between its balanced weight and the benign balanced weight.
    balanced[LABEL_IDS["JB"]] = math.sqrt(balanced[LABEL_IDS["JB"]] * balanced[LABEL_IDS["benign"]])
    mean_weight = sum(counts[label_id] * balanced[label_id] for label_id in counts) / total
    return {label_id: value / mean_weight for label_id, value in balanced.items()}


def metric_summary(metrics: dict) -> dict:
    return {
        "macro_f1": metrics["macro_f1"],
        "accuracy": metrics["accuracy"],
        "benign_fpr": metrics["benign_fpr"]["value"],
        "per_class": metrics["per_class"],
        "p95_ms": metrics["local_batch_one_latency_ms"]["p95"],
        "selected_pair": metrics["routing_threshold_sweep"]["selected_pair"],
        "selection_blockers": metrics["selection_blockers"],
    }


def main() -> int:
    if REPORT.exists() or OUTPUT.exists():
        raise FileExistsError("EXPERIMENT_PATH_EXISTS; inspect it and create a new version")
    if not OUTPUT.resolve(strict=False).is_relative_to(PRIVATE.resolve(strict=True)):
        raise ValueError("OUTPUT_OUTSIDE_PRIVATE_WORKSPACE")
    if not BASELINE_METRICS.is_file():
        raise FileNotFoundError("MATCHED_ROUND07_BASELINE_METRICS_MISSING")

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
    class_weight = moderated_balanced(counts)
    base_config = copy.deepcopy(context["manifest"]["baseline"])
    variant_config = copy.deepcopy(base_config)
    variant_config["classifier"]["class_weight"] = class_weight
    variant_config["classifier"]["C"] = 4.0
    context["manifest"]["baseline"] = variant_config
    variant = {
        "method": "balanced_with_jb_geometric_midpoint_to_benign_then_unit_mean_normalization",
        "candidate_C": 4.0,
        "selection_basis": "preselected from complete five-fold source-family OOF; fixed thresholds",
        "label_counts": {label: counts[label_id] for label, label_id in LABEL_IDS.items()},
        "base_class_weight": base_config["classifier"]["class_weight"],
        "class_weight_by_label": {LABELS[label_id]: value for label_id, value in class_weight.items()},
        "preserved_benign_to_pi_weight_ratio": class_weight[LABEL_IDS["benign"]] / class_weight[LABEL_IDS["PI"]],
    }
    print("VARIANT", json.dumps({**variant, "test_opened": False, "l3_run": False}), flush=True)

    result = adapter.fit(context)
    run_dir = Path(result["run"])
    run_manifest_path = run_dir / "run_manifest.json"
    run_manifest = json.loads(run_manifest_path.read_text(encoding="utf-8"))
    run_manifest["model_variant"] = {
        **variant,
        "baseline_config": base_config,
        "variant_config": variant_config,
    }
    run_manifest_path.write_text(json.dumps(run_manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                                 encoding="utf-8", newline="\n")

    metrics = json.loads((run_dir / "metrics.json").read_text(encoding="utf-8"))
    baseline = json.loads(BASELINE_METRICS.read_text(encoding="utf-8"))
    report = {
        "report_id": "l2_jb_moderated_c4_validation_round08_r01",
        "status": result["status"],
        "scope": "full fixed-package train/validation L2 fit; native reference labels, not human gold",
        "package_id": context["manifest"]["package_id"],
        "dataset_version": context["manifest"]["dataset_version"],
        "package_manifest_sha256": sha256(PACKAGE / "DATASET_MANIFEST.json"),
        "adapter_sha256": sha256(ADAPTER_PATH),
        "legacy_helper_sha256": sha256(LEGACY_PATH),
        "runner_sha256": sha256(Path(__file__)),
        "run_manifest_sha256": sha256(run_manifest_path),
        "run_path_private": str(run_dir),
        "sklearn_version": sklearn.__version__,
        "model_variant": run_manifest["model_variant"],
        "matched_baseline": metric_summary(baseline),
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
        "baseline": metric_summary(baseline),
        "candidate": metric_summary(metrics),
        "test_opened": False,
        "l3_run": False,
        "report": str(REPORT),
    }, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
