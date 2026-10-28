#!/usr/bin/env python3
"""Full five-fold source-family-held-out OOF diagnostics for the L2 train split."""
from __future__ import annotations

import collections
import hashlib
import json
import sys
import time
import warnings
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from sklearn.exceptions import ConvergenceWarning
from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support
from sklearn.model_selection import StratifiedGroupKFold

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
PRIVATE = REPO / "workspaces" / "truongnv" / "pi_guard_pipeline"
TRAINING = PRIVATE / "training_bases"
ADAPTER_DIR = TRAINING / "pi_guard_tfidf_tier1"
PACKAGE = TRAINING / "datasets" / "project_training" / "versions" / "pi_guard_native_reference_round07_20261013_r01"
PROTOCOL = ROOT / "AUTONOMOUS_PROTOCOL.json"
OUTPUT = ADAPTER_DIR / "runs" / "l2_family_oof_round07_r01_full_20261013"
REPORT = ROOT / "l2_family_oof_round07_r01.json"
SEED = 20261013
N_SPLITS = 5
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
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8", newline="\n")


def metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    p, r, f, support = precision_recall_fscore_support(
        y_true, y_pred, labels=[0, 1, 2], zero_division=0
    )
    matrix = confusion_matrix(y_true, y_pred, labels=[0, 1, 2])
    per_class = {
        label: {
            "precision": float(p[index]),
            "recall": float(r[index]),
            "f1": float(f[index]),
            "support": int(support[index]),
        }
        for index, label in enumerate(LABELS)
    }
    benign_fpr = float((matrix[0, 1] + matrix[0, 2]) / matrix[0].sum()) if matrix[0].sum() else None
    return {
        "rows": int(len(y_true)),
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "macro_f1": float(np.mean(f)),
        "per_class": per_class,
        "confusion_matrix": matrix.tolist(),
        "benign_false_positive_rate": benign_fpr,
        "pi_recall": per_class["PI"]["recall"],
        "jb_recall": per_class["JB"]["recall"],
    }


def main() -> int:
    if REPORT.exists():
        raise FileExistsError("OOF_REPORT_EXISTS; create a new version rather than overwriting")
    if OUTPUT.exists():
        raise FileExistsError("OOF_OUTPUT_EXISTS; inspect existing run and choose a new run id")
    if not OUTPUT.resolve(strict=False).is_relative_to(PRIVATE.resolve(strict=True)):
        raise ValueError("OOF_OUTPUT_OUTSIDE_PRIVATE_WORKSPACE")

    sys.path.insert(0, str(ADAPTER_DIR))
    import fit_l2_curated as adapter
    import fit_l2_v8 as legacy
    import sklearn

    preflight, context = adapter.preflight(PACKAGE, PROTOCOL, OUTPUT)
    print("PREFLIGHT", preflight["status"], json.dumps(preflight["blockers"]), flush=True)
    if context is None:
        raise RuntimeError("OOF_PREFLIGHT_BLOCKED")
    train, provenance = adapter._load_partition(context, "train")
    y = np.asarray([LABEL_IDS[row["label"]] for row in train], dtype=np.int8)
    groups = np.asarray([sidecar["source_family_id"] for sidecar in provenance], dtype=object)
    if len(train) != len(provenance) or len(set(row["id"] for row in train)) != len(train):
        raise ValueError("TRAIN_ROWS_OR_PROVENANCE_NOT_UNIQUE")
    family_label_support: dict[str, set[int]] = collections.defaultdict(set)
    family_counts = collections.Counter()
    for group, label in zip(groups, y):
        family_label_support[str(group)].add(int(label))
        family_counts[(str(group), int(label))] += 1
    global_families = {
        label: len({family for family, labels in family_label_support.items()
                    if LABEL_IDS[label] in labels})
        for label in LABELS
    }
    if any(value < N_SPLITS for value in global_families.values()):
        raise ValueError("INSUFFICIENT_TRAIN_FAMILIES_FOR_FIVE_FOLD_OOF")

    splitter = StratifiedGroupKFold(n_splits=N_SPLITS, shuffle=True, random_state=SEED)
    fold_indices = list(splitter.split(np.zeros(len(train), dtype=np.uint8), y, groups))
    seen_validation: list[int] = []
    fold_plan = []
    for fold_number, (fit_indices, held_indices) in enumerate(fold_indices, start=1):
        if np.intersect1d(fit_indices, held_indices).size:
            raise ValueError("ROW_OVERLAP_WITHIN_OOF_FOLD")
        fit_groups = set(groups[fit_indices])
        held_groups = set(groups[held_indices])
        if fit_groups & held_groups:
            raise ValueError("SOURCE_FAMILY_OVERLAP_WITHIN_OOF_FOLD")
        for field in ("collection_lineage_id", "prompt_family_id", "duplicate_group_id"):
            fit_values = {provenance[index][field] for index in fit_indices}
            held_values = {provenance[index][field] for index in held_indices}
            if fit_values & held_values:
                raise ValueError("GROUP_OVERLAP_WITHIN_OOF_FOLD:" + field)
        if set(y[fit_indices]) != {0, 1, 2} or set(y[held_indices]) != {0, 1, 2}:
            raise ValueError("OOF_FOLD_CLASS_MISSING:" + str(fold_number))
        seen_validation.extend(int(index) for index in held_indices)
        fold_plan.append({
            "fold": fold_number,
            "fit_rows": int(len(fit_indices)),
            "heldout_rows": int(len(held_indices)),
            "fit_families": int(len(fit_groups)),
            "heldout_families": int(len(held_groups)),
            "heldout_rows_by_label": {
                label: int(np.count_nonzero(y[held_indices] == LABEL_IDS[label]))
                for label in LABELS
            },
            "heldout_families_by_label": {
                label: int(len({groups[index] for index in held_indices
                                if y[index] == LABEL_IDS[label]}))
                for label in LABELS
            },
        })
    if sorted(seen_validation) != list(range(len(train))):
        raise ValueError("OOF_FOLDS_DO_NOT_COVER_EVERY_TRAIN_ROW_EXACTLY_ONCE")

    OUTPUT.mkdir(parents=True, exist_ok=False)
    run_state = {
        "run_id": OUTPUT.name,
        "state": "RUNNING",
        "package_manifest_sha256": sha256(PACKAGE / "DATASET_MANIFEST.json"),
        "split_sha256": sha256(context["refs"]["split"]),
        "baseline": context["manifest"]["baseline"],
        "seed": SEED,
        "folds": fold_plan,
        "test_opened": False,
        "l3_run": False,
    }
    write_json(OUTPUT / "run_state.json", run_state)
    oof_predictions: dict[int, int] = {}
    oof_fold_assignment: dict[int, int] = {}
    fold_results = []
    for fold_number, (fit_indices, held_indices) in enumerate(fold_indices, start=1):
        print("FOLD_START", fold_number, "of", N_SPLITS, "fit_rows", len(fit_indices),
              "heldout_rows", len(held_indices), flush=True)
        model = legacy.build_model(context["manifest"]["baseline"])
        fit_texts = [train[index]["text"] for index in fit_indices]
        held_texts = [train[index]["text"] for index in held_indices]
        started = time.perf_counter()
        with warnings.catch_warnings():
            warnings.simplefilter("error", ConvergenceWarning)
            model.fit(fit_texts, y[fit_indices])
        fit_seconds = time.perf_counter() - started
        predictions = np.asarray(model.predict(held_texts), dtype=np.int8)
        if len(predictions) != len(held_indices):
            raise ValueError("OOF_PREDICTION_COUNT_MISMATCH:" + str(fold_number))
        for index, prediction in zip(held_indices, predictions):
            key = int(index)
            if key in oof_predictions:
                raise ValueError("OOF_ROW_PREDICTED_TWICE")
            oof_predictions[key] = int(prediction)
            oof_fold_assignment[key] = fold_number
        fold_metric = metrics(y[held_indices], predictions)
        result = {
            "fold": fold_number,
            "fit_seconds": float(fit_seconds),
            "metrics": fold_metric,
            "fold_plan": fold_plan[fold_number - 1],
        }
        fold_results.append(result)
        write_json(OUTPUT / ("fold_" + str(fold_number) + ".json"), result)
        print("FOLD_DONE", fold_number, "macro_f1", fold_metric["macro_f1"],
              "benign_fpr", fold_metric["benign_false_positive_rate"],
              "fit_seconds", round(fit_seconds, 3), flush=True)
        del model, fit_texts, held_texts, predictions

    if set(oof_predictions) != set(range(len(train))):
        raise ValueError("OOF_PREDICTIONS_INCOMPLETE")
    y_pred = np.asarray([oof_predictions[index] for index in range(len(train))], dtype=np.int8)
    aggregate = metrics(y, y_pred)
    predictions_path = OUTPUT / "oof_predictions.jsonl"
    with predictions_path.open("w", encoding="utf-8", newline="\n") as stream:
        for index, prediction in enumerate(y_pred):
            stream.write(json.dumps({
                "id": train[index]["id"],
                "fold": oof_fold_assignment[index],
                "label": ID_LABELS[int(y[index])],
                "prediction": ID_LABELS[int(prediction)],
            }, ensure_ascii=False, separators=(",", ":")) + "\n")
    run_manifest = {
        "run_id": OUTPUT.name,
        "status": "COMPLETED_L2_SOURCE_FAMILY_OOF",
        "scope": "full five-fold OOF on frozen training rows; each source family held out once; validation and test rows not used",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "package_id": context["manifest"]["package_id"],
        "dataset_version": context["manifest"]["dataset_version"],
        "package_manifest_sha256": sha256(PACKAGE / "DATASET_MANIFEST.json"),
        "split_sha256": sha256(context["refs"]["split"]),
        "source_review_sha256": sha256(context["refs"]["source_review"]),
        "label_mapping_sha256": sha256(context["refs"]["label_mapping"]),
        "adapter_sha256": sha256(Path(adapter.__file__)),
        "legacy_helper_sha256": sha256(Path(legacy.__file__)),
        "sklearn_version": sklearn.__version__,
        "baseline": context["manifest"]["baseline"],
        "seed": SEED,
        "n_splits": N_SPLITS,
        "train_rows": len(train),
        "source_families_by_label": global_families,
        "aggregate_metrics": aggregate,
        "fold_results": fold_results,
        "oof_predictions_sha256": sha256(predictions_path),
        "test_opened": False,
        "l3_run": False,
    }
    write_json(OUTPUT / "run_manifest.json", run_manifest)
    write_json(OUTPUT / "run_state.json", {**run_state, "state": "COMPLETED",
                                           "run_manifest_sha256": sha256(OUTPUT / "run_manifest.json")})
    safe_report = {
        "report_id": "l2_family_oof_round07_r01",
        "status": run_manifest["status"],
        "package_id": run_manifest["package_id"],
        "dataset_version": run_manifest["dataset_version"],
        "run_path_private": str(OUTPUT),
        "scope": run_manifest["scope"],
        "train_rows": len(train),
        "source_families_by_label": global_families,
        "aggregate_metrics": aggregate,
        "fold_summaries": [{
            "fold": item["fold"],
            "fit_rows": item["fold_plan"]["fit_rows"],
            "heldout_rows": item["fold_plan"]["heldout_rows"],
            "heldout_families_by_label": item["fold_plan"]["heldout_families_by_label"],
            "metrics": item["metrics"],
            "fit_seconds": item["fit_seconds"],
        } for item in fold_results],
        "package_manifest_sha256": run_manifest["package_manifest_sha256"],
        "run_manifest_sha256": sha256(OUTPUT / "run_manifest.json"),
        "test_opened": False,
        "l3_run": False,
        "formal_acceptance_gate": "GATE_UNSPECIFIED",
        "label_status": "documented_native_reference_mapping_not_human_gold",
        "row_ids_or_text_emitted": False,
    }
    write_json(REPORT, safe_report)
    print("OOF_COMPLETE", json.dumps({
        "status": run_manifest["status"],
        "aggregate_metrics": aggregate,
        "test_opened": False,
        "l3_run": False,
        "report": str(REPORT),
    }, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
