"""Run one family-balanced L2 fit using the frozen native-reference package."""

from __future__ import annotations

import hashlib
import json
import sys
import time
import warnings
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from sklearn.exceptions import ConvergenceWarning


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
PRIVATE = REPO / "workspaces" / "truongnv" / "pi_guard_pipeline"
ADAPTER_PATH = PRIVATE / "training_bases" / "pi_guard_tfidf_tier1" / "fit_l2_curated.py"
PACKAGE = PRIVATE / "training_bases" / "datasets" / "project_training" / "versions" / "pi_guard_native_reference_round05_20261013_r03"
PROTOCOL = ROOT / "AUTONOMOUS_PROTOCOL.json"
OUTPUT = PRIVATE / "training_bases" / "pi_guard_tfidf_tier1" / "runs" / "l2_family_balanced_round07_20261013_r01"
REPORT = ROOT / "l2_family_balanced_validation_round07_r01.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    if OUTPUT.exists() or REPORT.exists():
        raise RuntimeError("Refusing to overwrite an existing family-balanced evidence artifact")
    sys.path.insert(0, str(ADAPTER_PATH.parent))
    import fit_l2_curated as adapter

    state, context = adapter.preflight(PACKAGE, PROTOCOL, OUTPUT)
    if state.get("status") != "READY_FOR_FIT" or context is None:
        raise RuntimeError("Package preflight failed: " + ";".join(state.get("blockers", [])))
    train, train_provenance = adapter._load_partition(context, "train")
    validation, validation_provenance = adapter._load_partition(context, "validation")
    family_counts = Counter(item["source_family_id"] for item in train_provenance)
    family_count = len(family_counts)
    weights = [len(train) / (family_count * family_counts[item["source_family_id"]])
               for item in train_provenance]
    family_weight_mass = Counter()
    for item, weight in zip(train_provenance, weights):
        family_weight_mass[item["source_family_id"]] += weight

    model = adapter.legacy.build_model(context["manifest"]["baseline"])
    started = time.perf_counter()
    with warnings.catch_warnings():
        warnings.simplefilter("error", ConvergenceWarning)
        model.fit([item["text"] for item in train],
                  [item["label_id"] for item in train],
                  classifier__sample_weight=weights)
    fit_seconds = time.perf_counter() - started

    _, metrics = adapter.legacy.evaluate(model, validation, validation_provenance)
    metrics["scope"] = "family_weighted_native_reference_validation_windows_only_not_human_gold"
    metrics["weighted_prf"] = adapter._weighted(metrics)
    warmup = min(20, len(validation))
    for item in validation[:warmup]:
        model.predict_proba([item["text"]])
    latency = []
    for item in validation:
        before = time.perf_counter_ns()
        model.predict_proba([item["text"]])
        latency.append((time.perf_counter_ns() - before) / 1e6)
    p50, p95, p99 = np.percentile(latency, [50, 95, 99]).tolist()
    metrics["local_batch_one_latency_ms"] = {
        "warmup_rows": warmup,
        "measurement_rows": len(validation),
        "p50": p50,
        "p95": p95,
        "p99": p99,
    }
    selected, blockers = adapter._choose_pair(metrics, context["protocol"], p95)
    metrics["routing_threshold_sweep"]["selected_pair"] = selected
    metrics["selection_blockers"] = blockers
    metrics["l2_status"] = "SELECTED_VALIDATION_CANDIDATE" if selected else "NOT_READY"
    metrics["family_weighting"] = {
        "scheme": "each represented source family receives equal aggregate sample_weight; weights sum to train rows",
        "family_row_counts": dict(sorted(family_counts.items())),
        "aggregate_weight_by_family": dict(sorted(family_weight_mass.items())),
        "class_weight": context["manifest"]["baseline"]["classifier"]["class_weight"],
    }

    import joblib

    OUTPUT.mkdir(parents=True, exist_ok=False)
    joblib.dump(model, OUTPUT / "model.joblib", compress=3)
    adapter.legacy.write_json(OUTPUT / "metrics.json", metrics)
    manifest = {
        "run_id": OUTPUT.name,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "status": metrics["l2_status"],
        "label_status": "documented_native_reference_mapping_not_human_gold",
        "package": str(PACKAGE),
        "dataset_version": context["manifest"]["dataset_version"],
        "package_manifest_sha256": sha256(PACKAGE / "DATASET_MANIFEST.json"),
        "protocol_sha256": sha256(PROTOCOL),
        "split_sha256": sha256(context["refs"]["split"]),
        "adapter_sha256": sha256(ADAPTER_PATH),
        "legacy_helper_sha256": sha256(Path(adapter.legacy.__file__)),
        "experiment": {
            "name": "equal_total_sample_weight_per_source_family",
            "baseline_hyperparameters_unchanged": True,
            "seed": context["manifest"]["baseline"]["seed"],
            "family_row_counts": dict(sorted(family_counts.items())),
            "aggregate_weight_by_family": dict(sorted(family_weight_mass.items())),
        },
        "fit_seconds": fit_seconds,
        "test_opened": False,
        "l3_run": False,
        "selected_pair": selected,
        "artifact_sha256": {
            "model.joblib": sha256(OUTPUT / "model.joblib"),
            "metrics.json": sha256(OUTPUT / "metrics.json"),
        },
    }
    adapter.legacy.write_json(OUTPUT / "run_manifest.json", manifest)
    report = {
        "audit_id": "l2_family_balanced_validation_round07_r01",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "one separate family-weighting experiment; native reference labels, not human gold",
        "run_id": OUTPUT.name,
        "run_manifest_sha256": sha256(OUTPUT / "run_manifest.json"),
        "metrics_sha256": sha256(OUTPUT / "metrics.json"),
        "metrics": metrics,
        "test_opened": False,
        "l3_run": False,
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": metrics["l2_status"],
        "run": str(OUTPUT),
        "report": str(REPORT),
        "fit_seconds": fit_seconds,
        "macro_f1": metrics["macro_f1"],
        "selected_pair": selected,
        "blockers": blockers,
        "p95_ms": p95,
        "test_opened": False,
        "l3_run": False,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
