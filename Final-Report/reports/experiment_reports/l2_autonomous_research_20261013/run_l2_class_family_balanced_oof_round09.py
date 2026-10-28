#!/usr/bin/env python3
"""Full five-fold OOF for class-preserving source-family sample weights."""
from __future__ import annotations

import collections
import copy
import hashlib
import json
import math
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
OUTPUT = ADAPTER_DIR / "runs" / "l2_class_family_balanced_oof_round09_r01_full_20261013"
REPORT = ROOT / "l2_class_family_balanced_oof_round09_r01.json"
SEED = 20261013
N_SPLITS = 5
LABELS = ("benign", "PI", "JB")
LABEL_IDS = {"benign": 0, "PI": 1, "JB": 2}
ID_LABELS = {value: key for key, value in LABEL_IDS.items()}
WEIGHT_METHOD = "balanced_with_jb_geometric_midpoint_to_benign_then_unit_mean_normalization"
C_VALUE = 2.0


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


def weights_for(y: np.ndarray) -> dict[int, float]:
    counts = collections.Counter(int(value) for value in y)
    if set(counts) != set(LABEL_IDS.values()):
        raise ValueError("OOF_FIT_SPLIT_MISSING_CLASS_FOR_WEIGHTING")
    total = len(y)
    balanced = {label_id: total / (len(LABELS) * counts[label_id]) for label_id in LABEL_IDS.values()}
    balanced[LABEL_IDS["JB"]] = math.sqrt(balanced[LABEL_IDS["JB"]] * balanced[LABEL_IDS["benign"]])
    mean_weight = sum(counts[label_id] * balanced[label_id] for label_id in LABEL_IDS.values()) / total
    return {label_id: value / mean_weight for label_id, value in balanced.items()}


def within_label_family_sample_weights(y: np.ndarray, groups: np.ndarray) -> tuple[np.ndarray, dict]:
    if len(y) != len(groups) or len(y) == 0:
        raise ValueError("FAMILY_SAMPLE_WEIGHT_INPUT_LENGTH_MISMATCH")
    counts = collections.Counter(int(label) for label in y)
    if set(counts) != set(LABEL_IDS.values()):
        raise ValueError("FAMILY_SAMPLE_WEIGHT_REQUIRES_ALL_LABELS")
    family_label_counts = collections.Counter((int(label), str(group)) for label, group in zip(y, groups))
    families_by_label = {
        label_id: sorted(group for candidate_label, group in family_label_counts if candidate_label == label_id)
        for label_id in LABEL_IDS.values()
    }
    family_count_by_label = {label_id: len(families_by_label[label_id]) for label_id in LABEL_IDS.values()}
    if any(value <= 0 for value in family_count_by_label.values()):
        raise ValueError("FAMILY_SAMPLE_WEIGHT_LABEL_WITHOUT_FAMILY")
    sample_weights = np.asarray([
        counts[int(label)] / (
            family_count_by_label[int(label)] * family_label_counts[(int(label), str(group))]
        )
        for label, group in zip(y, groups)
    ], dtype=np.float64)
    mass_by_label = {}
    for label_id in LABEL_IDS.values():
        class_mask = y == label_id
        class_mass = float(sample_weights[class_mask].sum())
        if not math.isclose(class_mass, float(counts[label_id]), rel_tol=1e-10, abs_tol=1e-8):
            raise ValueError("FAMILY_SAMPLE_WEIGHT_DID_NOT_PRESERVE_CLASS_MASS")
        for group in families_by_label[label_id]:
            family_mass = float(sample_weights[(y == label_id) & (groups == group)].sum())
            expected = counts[label_id] / family_count_by_label[label_id]
            if not math.isclose(family_mass, expected, rel_tol=1e-10, abs_tol=1e-8):
                raise ValueError("FAMILY_SAMPLE_WEIGHT_NOT_EQUAL_WITHIN_LABEL")
        mass_by_label[ID_LABELS[label_id]] = class_mass
    return sample_weights, {
        "family_count_by_label": {ID_LABELS[k]: v for k, v in family_count_by_label.items()},
        "class_mass_by_label": mass_by_label,
        "row_weight_min": float(sample_weights.min()),
        "row_weight_max": float(sample_weights.max()),
        "mean_row_weight": float(sample_weights.mean()),
        "class_mass_preserved": True,
        "family_mass_equal_within_class": True,
    }


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
    if REPORT.exists() or OUTPUT.exists():
        raise FileExistsError("OOF_PATH_EXISTS; inspect it and create a new version")
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
    base_c = float(context["manifest"]["baseline"]["classifier"]["C"])
    if base_c != 2.0:
        raise ValueError(f"MATCHED_COMPARATOR_C_CHANGED:{base_c}")
    model_variant = {
        "method": "class_preserving_equal_family_mass_with_same_JB_moderated_class_weights",
        "matched_comparator_C": base_c,
        "candidate_C": C_VALUE,
        "weight_method": WEIGHT_METHOD,
        "selection_basis": "complete source-family-held-out train OOF only; validation not used for retuning",
        "family_weighting": "equal total sample weight per source family within each label; preserves class mass",
    }

    train, provenance = adapter._load_partition(context, "train")
    y = np.asarray([LABEL_IDS[row["label"]] for row in train], dtype=np.int8)
    groups = np.asarray([sidecar["source_family_id"] for sidecar in provenance], dtype=object)
    if len(train) != len(provenance) or len({row["id"] for row in train}) != len(train):
        raise ValueError("TRAIN_ROWS_OR_PROVENANCE_NOT_UNIQUE")

    family_label_support: dict[str, set[int]] = collections.defaultdict(set)
    for group, label in zip(groups, y):
        family_label_support[str(group)].add(int(label))
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
        fit_groups, held_groups = set(groups[fit_indices]), set(groups[held_indices])
        if np.intersect1d(fit_indices, held_indices).size or fit_groups & held_groups:
            raise ValueError("ROW_OR_FAMILY_OVERLAP_WITHIN_OOF_FOLD")
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
            "heldout_rows_by_label": {label: int(np.count_nonzero(y[held_indices] == LABEL_IDS[label])
                                                  ) for label in LABELS},
            "heldout_families_by_label": {
                label: int(len({groups[index] for index in held_indices if y[index] == LABEL_IDS[label]}))
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
        "baseline_config": context["manifest"]["baseline"],
        "weight_method": WEIGHT_METHOD,
        "model_variant": model_variant,
        "seed": SEED,
        "folds": fold_plan,
        "test_opened": False,
        "l3_run": False,
    }
    write_json(OUTPUT / "run_state.json", run_state)
    predictions: dict[int, int] = {}
    fold_assignment: dict[int, int] = {}
    fold_results = []
    for fold_number, (fit_indices, held_indices) in enumerate(fold_indices, start=1):
        fold_weights = weights_for(y[fit_indices])
        family_sample_weights, family_weight_summary = within_label_family_sample_weights(
            y[fit_indices], groups[fit_indices]
        )
        model_config = copy.deepcopy(context["manifest"]["baseline"])
        model_config["classifier"]["C"] = C_VALUE
        model_config["classifier"]["class_weight"] = fold_weights
        weight_record = {LABELS[label_id]: value for label_id, value in fold_weights.items()}
        print("FOLD_START", fold_number, "of", N_SPLITS, "fit_rows", len(fit_indices),
              "heldout_rows", len(held_indices), "class_weight", json.dumps(weight_record), flush=True)
        model = legacy.build_model(model_config)
        fit_texts = [train[index]["text"] for index in fit_indices]
        held_texts = [train[index]["text"] for index in held_indices]
        started = time.perf_counter()
        with warnings.catch_warnings():
            warnings.simplefilter("error", ConvergenceWarning)
            model.fit(fit_texts, y[fit_indices], classifier__sample_weight=family_sample_weights)
        fit_seconds = time.perf_counter() - started
        fold_predictions = np.asarray(model.predict(held_texts), dtype=np.int8)
        if len(fold_predictions) != len(held_indices):
            raise ValueError("OOF_PREDICTION_COUNT_MISMATCH:" + str(fold_number))
        for index, prediction in zip(held_indices, fold_predictions):
            key = int(index)
            if key in predictions:
                raise ValueError("OOF_ROW_PREDICTED_TWICE")
            predictions[key] = int(prediction)
            fold_assignment[key] = fold_number
        fold_metric = metrics(y[held_indices], fold_predictions)
        fold_result = {
            "fold": fold_number,
            "fit_seconds": float(fit_seconds),
            "class_weight_by_label": weight_record,
            "family_sample_weight_summary": family_weight_summary,
            "fit_label_counts": {label: int(np.count_nonzero(y[fit_indices] == LABEL_IDS[label]))
                                 for label in LABELS},
            "metrics": fold_metric,
            "fold_plan": fold_plan[fold_number - 1],
        }
        fold_results.append(fold_result)
        write_json(OUTPUT / ("fold_" + str(fold_number) + ".json"), fold_result)
        print("FOLD_DONE", fold_number, "macro_f1", fold_metric["macro_f1"],
              "benign_fpr", fold_metric["benign_false_positive_rate"],
              "jb_precision", fold_metric["per_class"]["JB"]["precision"],
              "fit_seconds", round(fit_seconds, 3), flush=True)
        del model, fit_texts, held_texts, fold_predictions

    if set(predictions) != set(range(len(train))):
        raise ValueError("OOF_PREDICTIONS_INCOMPLETE")
    y_pred = np.asarray([predictions[index] for index in range(len(train))], dtype=np.int8)
    aggregate = metrics(y, y_pred)
    predictions_path = OUTPUT / "oof_predictions.jsonl"
    with predictions_path.open("w", encoding="utf-8", newline="\n") as stream:
        for index, prediction in enumerate(y_pred):
            stream.write(json.dumps({
                "id": train[index]["id"],
                "fold": fold_assignment[index],
                "label": ID_LABELS[int(y[index])],
                "prediction": ID_LABELS[int(prediction)],
            }, ensure_ascii=False, separators=(",", ":")) + "\n")

    run_manifest = {
        "run_id": OUTPUT.name,
        "status": "COMPLETED_L2_SOURCE_FAMILY_OOF",
        "scope": "full five-fold family-held-out OOF on frozen train rows; no validation/test rows used",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "package_id": context["manifest"]["package_id"],
        "dataset_version": context["manifest"]["dataset_version"],
        "package_manifest_sha256": sha256(PACKAGE / "DATASET_MANIFEST.json"),
        "split_sha256": sha256(context["refs"]["split"]),
        "source_review_sha256": sha256(context["refs"]["source_review"]),
        "label_mapping_sha256": sha256(context["refs"]["label_mapping"]),
        "adapter_sha256": sha256(Path(adapter.__file__)),
        "legacy_helper_sha256": sha256(Path(legacy.__file__)),
        "runner_sha256": sha256(Path(__file__)),
        "sklearn_version": sklearn.__version__,
        "baseline_config": context["manifest"]["baseline"],
        "weight_method": WEIGHT_METHOD,
        "model_variant": model_variant,
        "seed": SEED,
        "n_splits": N_SPLITS,
        "train_rows": len(train),
        "source_families_by_label": global_families,
        "aggregate_metrics": aggregate,
        "model_variant": model_variant,
        "fold_results": fold_results,
        "oof_predictions_sha256": sha256(predictions_path),
        "test_opened": False,
        "l3_run": False,
    }
    write_json(OUTPUT / "run_manifest.json", run_manifest)
    write_json(OUTPUT / "run_state.json", {**run_state, "state": "COMPLETED",
                                            "run_manifest_sha256": sha256(OUTPUT / "run_manifest.json")})
    safe_report = {
        "report_id": "l2_class_family_balanced_oof_round09_r01",
        "status": run_manifest["status"],
        "package_id": run_manifest["package_id"],
        "dataset_version": run_manifest["dataset_version"],
        "run_path_private": str(OUTPUT),
        "scope": run_manifest["scope"],
        "train_rows": len(train),
        "source_families_by_label": global_families,
        "aggregate_metrics": aggregate,
        "model_variant": model_variant,
        "fold_summaries": [{
            "fold": item["fold"],
            "fit_rows": item["fold_plan"]["fit_rows"],
            "heldout_rows": item["fold_plan"]["heldout_rows"],
            "heldout_families_by_label": item["fold_plan"]["heldout_families_by_label"],
            "class_weight_by_label": item["class_weight_by_label"],
            "family_sample_weight_summary": item["family_sample_weight_summary"],
            "metrics": item["metrics"],
            "fit_seconds": item["fit_seconds"],
        } for item in fold_results],
        "package_manifest_sha256": run_manifest["package_manifest_sha256"],
        "runner_sha256": run_manifest["runner_sha256"],
        "run_manifest_sha256": sha256(OUTPUT / "run_manifest.json"),
        "formal_acceptance_gate": "GATE_UNSPECIFIED",
        "label_status": "documented_native_reference_mapping_not_human_gold",
        "row_ids_or_text_emitted": False,
        "test_opened": False,
        "l3_run": False,
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
