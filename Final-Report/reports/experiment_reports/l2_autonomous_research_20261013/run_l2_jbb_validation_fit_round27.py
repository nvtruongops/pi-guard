"""Run one complete fixed-config L2 classifier fit without cutoff selection."""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
import time
import warnings
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import sklearn
from sklearn.exceptions import ConvergenceWarning
from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
PRIVATE = REPO / "workspaces" / "truongnv" / "pi_guard_pipeline"
TRAINING = PRIVATE / "training_bases"
ADAPTER_DIR = TRAINING / "pi_guard_tfidf_tier1"
PROTOCOL = ROOT / "AUTONOMOUS_PROTOCOL.json"
LABELS = ("benign", "PI", "JB")
LABEL_IDS = {"benign": 0, "PI": 1, "JB": 2}
ID_LABELS = {value: key for key, value in LABEL_IDS.items()}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8", newline="\n")


def score(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    precision, recall, f1, support = precision_recall_fscore_support(
        y_true, y_pred, labels=[0, 1, 2], zero_division=0
    )
    matrix = confusion_matrix(y_true, y_pred, labels=[0, 1, 2])
    per_class = {
        label: {
            "precision": float(precision[index]),
            "recall": float(recall[index]),
            "f1": float(f1[index]),
            "support": int(support[index]),
        }
        for index, label in enumerate(LABELS)
    }
    benign_support = int(matrix[0].sum())
    return {
        "rows": int(len(y_true)),
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "macro_f1": float(np.mean(f1)),
        "per_class": per_class,
        "confusion_matrix_labels": list(LABELS),
        "confusion_matrix": matrix.tolist(),
        "benign_false_positive_rate": float((matrix[0, 1] + matrix[0, 2]) / benign_support) if benign_support else None,
        "predicted_label_counts": {label: int(np.count_nonzero(y_pred == LABEL_IDS[label])) for label in LABELS},
    }


def run(package: Path, output: Path) -> dict:
    sys.path.insert(0, str(ADAPTER_DIR))
    import fit_l2_curated as adapter
    import fit_l2_v8 as legacy

    preflight, context = adapter.preflight(package.resolve(), PROTOCOL.resolve(), output.resolve(strict=False))
    if context is None or preflight.get("status") != "READY_FOR_FIT":
        raise RuntimeError("R27_FIT_PREFLIGHT_BLOCKED:" + json.dumps(preflight.get("blockers", [])))
    train, train_prov = adapter._load_partition(context, "train")
    validation, validation_prov = adapter._load_partition(context, "validation")
    if len(train) != len(train_prov) or len(validation) != len(validation_prov):
        raise ValueError("R27_FIT_ROW_PROVENANCE_ALIGNMENT")
    y_train = np.asarray([LABEL_IDS[row["label"]] for row in train], dtype=np.int8)
    y_validation = np.asarray([LABEL_IDS[row["label"]] for row in validation], dtype=np.int8)
    if set(y_train.tolist()) != {0, 1, 2} or set(y_validation.tolist()) != {0, 1, 2}:
        raise ValueError("R27_FIT_CLASS_SUPPORT_MISSING")
    if output.exists():
        raise FileExistsError("R27_FIT_OUTPUT_EXISTS")
    output.mkdir(parents=True)

    model = legacy.build_model(context["manifest"]["baseline"])
    started = time.perf_counter()
    with warnings.catch_warnings():
        warnings.simplefilter("error", ConvergenceWarning)
        model.fit([row["text"] for row in train], y_train)
    fit_seconds = time.perf_counter() - started
    y_pred = np.asarray(model.predict([row["text"] for row in validation]), dtype=np.int8)
    if len(y_pred) != len(validation):
        raise ValueError("R27_FIT_PREDICTION_COUNT_MISMATCH")
    metrics = score(y_validation, y_pred)
    metrics.update({
        "evaluation_scope": "full validation partition; fixed classifier argmax; no threshold/cutoff selection",
        "l2_status": "DIAGNOSTIC_ONLY_GATE_UNSPECIFIED",
        "validation_jb_support_diagnostic_floor": 100,
        "validation_jb_support_floor_met": metrics["per_class"]["JB"]["support"] >= 100,
        "fit_seconds": fit_seconds,
    })
    import joblib
    joblib.dump(model, output / "model.joblib", compress=3)
    with (output / "validation_predictions.jsonl").open("w", encoding="utf-8", newline="\n") as stream:
        for row, predicted in zip(validation, y_pred):
            stream.write(json.dumps({"id": row["id"], "label": row["label"],
                                     "prediction": ID_LABELS[int(predicted)]},
                                    ensure_ascii=False, separators=(",", ":")) + "\n")
    write_json(output / "metrics.json", metrics)
    run_manifest = {
        "run_id": output.name,
        "status": metrics["l2_status"],
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "package_id": context["manifest"]["package_id"],
        "dataset_version": context["manifest"]["dataset_version"],
        "package_manifest_sha256": sha256(package / "DATASET_MANIFEST.json"),
        "protocol_sha256": sha256(PROTOCOL),
        "input_sha256": {
            f"{part}_{kind}": context["manifest"]["partitions"][part][kind]["sha256"]
            for part in ("train", "validation") for kind in ("rows", "provenance")
        },
        "adapter_sha256": sha256(Path(adapter.__file__)),
        "legacy_helper_sha256": sha256(Path(legacy.__file__)),
        "baseline": context["manifest"]["baseline"],
        "train_rows": len(train),
        "validation_rows": len(validation),
        "train_class_counts": {label: int(np.count_nonzero(y_train == LABEL_IDS[label])) for label in LABELS},
        "validation_class_counts": {label: int(np.count_nonzero(y_validation == LABEL_IDS[label])) for label in LABELS},
        "fit_seconds": fit_seconds,
        "environment": {"python": platform.python_version(), "numpy": np.__version__, "sklearn": sklearn.__version__},
        "cutoff_selection": False,
        "test_opened": False,
        "l3_run": False,
        "smoke_run": False,
        "artifact_sha256": {name: sha256(output / name) for name in ("model.joblib", "metrics.json", "validation_predictions.jsonl")},
    }
    write_json(output / "run_manifest.json", run_manifest)
    result = {
        "status": metrics["l2_status"],
        "run_id": output.name,
        "package_id": run_manifest["package_id"],
        "train_rows": len(train),
        "validation_rows": len(validation),
        "validation_class_counts": run_manifest["validation_class_counts"],
        "macro_f1": metrics["macro_f1"],
        "accuracy": metrics["accuracy"],
        "benign_fpr": metrics["benign_false_positive_rate"],
        "per_class": metrics["per_class"],
        "confusion_matrix": metrics["confusion_matrix"],
        "cutoff_selection": False,
        "test_opened": False,
        "l3_run": False,
        "smoke_run": False,
        "run_path_private": str(output),
    }
    write_json(ROOT / (output.name + ".json"), result)
    print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.package, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
