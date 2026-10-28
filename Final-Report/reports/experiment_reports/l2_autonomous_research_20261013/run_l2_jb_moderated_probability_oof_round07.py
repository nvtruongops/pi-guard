#!/usr/bin/env python3
"""Full family-held-out OOF probabilities for one validation-locked L2 pair."""
from __future__ import annotations

import collections
import copy
import json
import sys
import time
import warnings
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from sklearn.exceptions import ConvergenceWarning
from sklearn.model_selection import StratifiedGroupKFold

import run_l2_jb_moderated_family_oof_round07 as base


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
PRIVATE = REPO / "workspaces" / "truongnv" / "pi_guard_pipeline"
TRAINING = PRIVATE / "training_bases"
ADAPTER_DIR = TRAINING / "pi_guard_tfidf_tier1"
PACKAGE = TRAINING / "datasets" / "project_training" / "versions" / "pi_guard_native_reference_round07_20261013_r01"
PROTOCOL = ROOT / "AUTONOMOUS_PROTOCOL.json"
THRESHOLD_REPORT = ROOT / "l2_supplemental_threshold_grid_round07_r01.json"
OUTPUT = ADAPTER_DIR / "runs" / "l2_jb_moderated_probability_oof_round07_r01_full_20261013"
REPORT = ROOT / "l2_jb_moderated_probability_oof_round07_r01.json"
TAU_ALLOW = 0.999
TAU_BLOCK = 0.995


def route_summary(y_true: np.ndarray, probabilities: np.ndarray) -> dict:
    counts = {label: collections.Counter() for label in base.LABELS}
    total = collections.Counter()
    for label_id, scores in zip(y_true, probabilities):
        benign_score = float(scores[base.LABEL_IDS["benign"]])
        attack_score = max(float(scores[base.LABEL_IDS["PI"]]), float(scores[base.LABEL_IDS["JB"]]))
        if benign_score >= TAU_ALLOW and benign_score > attack_score:
            route = "ALLOW_CANDIDATE"
        elif attack_score >= TAU_BLOCK and attack_score > benign_score:
            route = "BLOCK_CANDIDATE"
        else:
            route = "REVIEW_TO_L3"
        label = base.ID_LABELS[int(label_id)]
        counts[label][route] += 1
        total[route] += 1
    rows = len(y_true)
    support = {label: int(np.count_nonzero(y_true == base.LABEL_IDS[label])) for label in base.LABELS}
    per_class = {}
    for label in base.LABELS:
        denominator = support[label]
        per_class[label] = {
            "support": denominator,
            "routes": {route: counts[label][route] for route in
                       ("ALLOW_CANDIDATE", "REVIEW_TO_L3", "BLOCK_CANDIDATE")},
        }
    return {
        "rows": rows,
        "routes": {route: total[route] for route in
                   ("ALLOW_CANDIDATE", "REVIEW_TO_L3", "BLOCK_CANDIDATE")},
        "review_rate": total["REVIEW_TO_L3"] / rows if rows else None,
        "by_true_label": per_class,
        "pi_early_allow_rate": counts["PI"]["ALLOW_CANDIDATE"] / support["PI"],
        "jb_early_allow_rate": counts["JB"]["ALLOW_CANDIDATE"] / support["JB"],
        "benign_early_block_rate": counts["benign"]["BLOCK_CANDIDATE"] / support["benign"],
    }


def main() -> int:
    if REPORT.exists() or OUTPUT.exists():
        raise FileExistsError("OOF_PATH_EXISTS; inspect it and create a new version")
    if not OUTPUT.resolve(strict=False).is_relative_to(PRIVATE.resolve(strict=True)):
        raise ValueError("OOF_OUTPUT_OUTSIDE_PRIVATE_WORKSPACE")
    if not THRESHOLD_REPORT.is_file():
        raise FileNotFoundError("VALIDATION_THRESHOLD_SOURCE_REPORT_MISSING")
    threshold_source = json.loads(THRESHOLD_REPORT.read_text(encoding="utf-8"))
    expected = threshold_source.get("best_pair_under_existing_exploratory_selection_order")
    if (expected is None or expected.get("tau_allow") != TAU_ALLOW
            or expected.get("tau_block") != TAU_BLOCK):
        raise ValueError("OOF_THRESHOLD_PAIR_DIFFERS_FROM_VALIDATION_LOCKED_PAIR")

    sys.path.insert(0, str(ADAPTER_DIR))
    import fit_l2_curated as adapter
    import fit_l2_v8 as legacy
    import sklearn

    preflight, context = adapter.preflight(PACKAGE, PROTOCOL, OUTPUT)
    print("PREFLIGHT", preflight["status"], json.dumps(preflight["blockers"]), flush=True)
    if context is None:
        raise RuntimeError("OOF_PREFLIGHT_BLOCKED")
    train, provenance = adapter._load_partition(context, "train")
    y = np.asarray([base.LABEL_IDS[row["label"]] for row in train], dtype=np.int8)
    groups = np.asarray([sidecar["source_family_id"] for sidecar in provenance], dtype=object)
    if len(train) != len(provenance) or len({row["id"] for row in train}) != len(train):
        raise ValueError("TRAIN_ROWS_OR_PROVENANCE_NOT_UNIQUE")

    family_support: dict[str, set[int]] = collections.defaultdict(set)
    for family, label in zip(groups, y):
        family_support[str(family)].add(int(label))
    global_families = {
        label: len({family for family, labels in family_support.items()
                    if base.LABEL_IDS[label] in labels})
        for label in base.LABELS
    }
    if any(count < base.N_SPLITS for count in global_families.values()):
        raise ValueError("INSUFFICIENT_TRAIN_FAMILIES_FOR_FIVE_FOLD_OOF")

    splitter = StratifiedGroupKFold(n_splits=base.N_SPLITS, shuffle=True, random_state=base.SEED)
    fold_indices = list(splitter.split(np.zeros(len(train), dtype=np.uint8), y, groups))
    seen_heldout: list[int] = []
    plans = []
    for fold, (fit_indices, held_indices) in enumerate(fold_indices, start=1):
        fit_families, held_families = set(groups[fit_indices]), set(groups[held_indices])
        if np.intersect1d(fit_indices, held_indices).size or fit_families & held_families:
            raise ValueError("ROW_OR_FAMILY_OVERLAP_WITHIN_OOF_FOLD")
        for field in ("collection_lineage_id", "prompt_family_id", "duplicate_group_id"):
            fit_values = {provenance[i][field] for i in fit_indices}
            held_values = {provenance[i][field] for i in held_indices}
            if fit_values & held_values:
                raise ValueError("GROUP_OVERLAP_WITHIN_OOF_FOLD:" + field)
        if set(y[fit_indices]) != {0, 1, 2} or set(y[held_indices]) != {0, 1, 2}:
            raise ValueError("OOF_FOLD_CLASS_MISSING:" + str(fold))
        seen_heldout.extend(int(i) for i in held_indices)
        plans.append({
            "fold": fold,
            "fit_rows": int(len(fit_indices)),
            "heldout_rows": int(len(held_indices)),
            "fit_families": len(fit_families),
            "heldout_families": len(held_families),
            "heldout_rows_by_label": {label: int(np.count_nonzero(y[held_indices] == base.LABEL_IDS[label]))
                                       for label in base.LABELS},
            "heldout_families_by_label": {
                label: len({groups[i] for i in held_indices if y[i] == base.LABEL_IDS[label]})
                for label in base.LABELS
            },
        })
    if sorted(seen_heldout) != list(range(len(train))):
        raise ValueError("OOF_FOLDS_DO_NOT_COVER_EVERY_TRAIN_ROW_EXACTLY_ONCE")

    OUTPUT.mkdir(parents=True, exist_ok=False)
    run_state = {
        "run_id": OUTPUT.name,
        "state": "RUNNING",
        "package_manifest_sha256": base.sha256(PACKAGE / "DATASET_MANIFEST.json"),
        "split_sha256": base.sha256(context["refs"]["split"]),
        "weight_method": base.WEIGHT_METHOD,
        "tau_allow": TAU_ALLOW,
        "tau_block": TAU_BLOCK,
        "threshold_source_report_sha256": base.sha256(THRESHOLD_REPORT),
        "seed": base.SEED,
        "folds": plans,
        "test_opened": False,
        "l3_run": False,
    }
    base.write_json(OUTPUT / "run_state.json", run_state)
    all_predictions: dict[int, int] = {}
    all_probabilities: dict[int, list[float]] = {}
    fold_for_row: dict[int, int] = {}
    fold_results = []
    for fold, (fit_indices, held_indices) in enumerate(fold_indices, start=1):
        fold_weights = base.weights_for(y[fit_indices])
        config = copy.deepcopy(context["manifest"]["baseline"])
        config["classifier"]["class_weight"] = fold_weights
        print("FOLD_START", fold, "of", base.N_SPLITS, "fit_rows", len(fit_indices),
              "heldout_rows", len(held_indices), flush=True)
        model = legacy.build_model(config)
        fit_texts = [train[i]["text"] for i in fit_indices]
        held_texts = [train[i]["text"] for i in held_indices]
        started = time.perf_counter()
        with warnings.catch_warnings():
            warnings.simplefilter("error", ConvergenceWarning)
            model.fit(fit_texts, y[fit_indices])
        fit_seconds = time.perf_counter() - started
        if list(model.classes_) != [0, 1, 2]:
            raise ValueError("OOF_MODEL_CLASS_ORDER_INVALID")
        fold_scores = model.predict_proba(held_texts)
        fold_predictions = np.asarray(model.predict(held_texts), dtype=np.int8)
        if len(fold_predictions) != len(held_indices) or fold_scores.shape != (len(held_indices), 3):
            raise ValueError("OOF_PREDICTION_SHAPE_MISMATCH:" + str(fold))
        for index, prediction, scores in zip(held_indices, fold_predictions, fold_scores):
            key = int(index)
            if key in all_predictions or key in all_probabilities:
                raise ValueError("OOF_ROW_PREDICTED_TWICE")
            all_predictions[key] = int(prediction)
            all_probabilities[key] = [float(value) for value in scores]
            fold_for_row[key] = fold
        fold_metric = base.metrics(y[held_indices], fold_predictions)
        fold_routes = route_summary(y[held_indices], fold_scores)
        result = {
            "fold": fold,
            "fit_seconds": float(fit_seconds),
            "class_weight_by_label": {base.LABELS[label_id]: value
                                       for label_id, value in fold_weights.items()},
            "metrics": fold_metric,
            "routing_at_validation_locked_pair": fold_routes,
            "fold_plan": plans[fold - 1],
        }
        fold_results.append(result)
        base.write_json(OUTPUT / ("fold_" + str(fold) + ".json"), result)
        print("FOLD_DONE", fold, "macro_f1", fold_metric["macro_f1"],
              "review_rate", fold_routes["review_rate"],
              "jb_early_allow", fold_routes["jb_early_allow_rate"],
              "benign_early_block", fold_routes["benign_early_block_rate"],
              "fit_seconds", round(fit_seconds, 3), flush=True)
        del model, fit_texts, held_texts, fold_scores, fold_predictions

    if set(all_predictions) != set(range(len(train))) or set(all_probabilities) != set(range(len(train))):
        raise ValueError("OOF_PREDICTIONS_INCOMPLETE")
    y_pred = np.asarray([all_predictions[i] for i in range(len(train))], dtype=np.int8)
    scores = np.asarray([all_probabilities[i] for i in range(len(train))], dtype=np.float64)
    aggregate = base.metrics(y, y_pred)
    route_aggregate = route_summary(y, scores)
    score_path = OUTPUT / "oof_probabilities.jsonl"
    with score_path.open("w", encoding="utf-8", newline="\n") as stream:
        for index in range(len(train)):
            stream.write(json.dumps({
                "id": train[index]["id"],
                "fold": fold_for_row[index],
                "label": base.ID_LABELS[int(y[index])],
                "prediction": base.ID_LABELS[int(y_pred[index])],
                "scores_uncalibrated": {label: float(scores[index, base.LABEL_IDS[label]])
                                         for label in base.LABELS},
            }, ensure_ascii=False, separators=(",", ":")) + "\n")

    run_manifest = {
        "run_id": OUTPUT.name,
        "status": "COMPLETED_L2_SOURCE_FAMILY_OOF_PROBABILITIES",
        "scope": "full five-fold family-held-out OOF probabilities on frozen train rows; no validation/test rows used for fit",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "package_id": context["manifest"]["package_id"],
        "dataset_version": context["manifest"]["dataset_version"],
        "package_manifest_sha256": base.sha256(PACKAGE / "DATASET_MANIFEST.json"),
        "split_sha256": base.sha256(context["refs"]["split"]),
        "source_review_sha256": base.sha256(context["refs"]["source_review"]),
        "label_mapping_sha256": base.sha256(context["refs"]["label_mapping"]),
        "runner_sha256": base.sha256(Path(__file__)),
        "base_probability_oof_runner_sha256": base.sha256(ROOT / "run_l2_jb_moderated_family_oof_round07.py"),
        "sklearn_version": sklearn.__version__,
        "weight_method": base.WEIGHT_METHOD,
        "seed": base.SEED,
        "n_splits": base.N_SPLITS,
        "train_rows": len(train),
        "source_families_by_label": global_families,
        "aggregate_metrics": aggregate,
        "validation_locked_threshold_pair": {"tau_allow": TAU_ALLOW, "tau_block": TAU_BLOCK},
        "threshold_source_report_sha256": base.sha256(THRESHOLD_REPORT),
        "threshold_routing_oof": route_aggregate,
        "fold_results": fold_results,
        "oof_probabilities_sha256": base.sha256(score_path),
        "test_opened": False,
        "l3_run": False,
    }
    base.write_json(OUTPUT / "run_manifest.json", run_manifest)
    base.write_json(OUTPUT / "run_state.json", {**run_state, "state": "COMPLETED",
                                                 "run_manifest_sha256": base.sha256(OUTPUT / "run_manifest.json")})
    report = {
        "report_id": "l2_jb_moderated_probability_oof_round07_r01",
        "status": run_manifest["status"],
        "scope": run_manifest["scope"],
        "package_id": run_manifest["package_id"],
        "dataset_version": run_manifest["dataset_version"],
        "run_path_private": str(OUTPUT),
        "train_rows": len(train),
        "source_families_by_label": global_families,
        "aggregate_metrics": aggregate,
        "validation_locked_threshold_pair": run_manifest["validation_locked_threshold_pair"],
        "threshold_source_report_sha256": run_manifest["threshold_source_report_sha256"],
        "threshold_routing_oof": route_aggregate,
        "fold_summaries": [{
            "fold": item["fold"],
            "fit_rows": item["fold_plan"]["fit_rows"],
            "heldout_rows": item["fold_plan"]["heldout_rows"],
            "heldout_families_by_label": item["fold_plan"]["heldout_families_by_label"],
            "metrics": item["metrics"],
            "routing_at_validation_locked_pair": item["routing_at_validation_locked_pair"],
            "fit_seconds": item["fit_seconds"],
        } for item in fold_results],
        "package_manifest_sha256": run_manifest["package_manifest_sha256"],
        "runner_sha256": run_manifest["runner_sha256"],
        "oof_probabilities_sha256": run_manifest["oof_probabilities_sha256"],
        "run_manifest_sha256": base.sha256(OUTPUT / "run_manifest.json"),
        "formal_acceptance_gate": "GATE_UNSPECIFIED",
        "label_status": "documented_native_reference_mapping_not_human_gold",
        "row_ids_or_text_emitted": False,
        "test_opened": False,
        "l3_run": False,
    }
    base.write_json(REPORT, report)
    print("OOF_PROBABILITY_COMPLETE", json.dumps({
        "status": run_manifest["status"],
        "aggregate_metrics": aggregate,
        "threshold_routing_oof": route_aggregate,
        "test_opened": False,
        "l3_run": False,
        "report": str(REPORT),
    }, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
