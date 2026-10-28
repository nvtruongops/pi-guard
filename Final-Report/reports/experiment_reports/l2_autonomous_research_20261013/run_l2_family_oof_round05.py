"""Run source-family-held-out L2 diagnostics without opening any test payload."""

from __future__ import annotations

import hashlib
import json
import sys
import time
import warnings
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from sklearn.exceptions import ConvergenceWarning
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
PRIVATE = REPO / "workspaces" / "truongnv" / "pi_guard_pipeline"
ADAPTER_PATH = PRIVATE / "training_bases" / "pi_guard_tfidf_tier1" / "fit_l2_curated.py"
PACKAGE = PRIVATE / "training_bases" / "datasets" / "project_training" / "versions" / "pi_guard_native_reference_round05_20261013_r02"
PROTOCOL = ROOT / "AUTONOMOUS_PROTOCOL.json"
OUTPUT_GUARD = PRIVATE / "training_bases" / "pi_guard_tfidf_tier1" / "runs" / "l2_family_oof_round05_20261013_r01"
REPORT = ROOT / "l2_oof_family_holdout_round05_r01.json"
LABELS = ("benign", "PI", "JB")
ROUTES = ("ALLOW_CANDIDATE", "REVIEW_TO_L3", "BLOCK_CANDIDATE")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    if REPORT.exists() or OUTPUT_GUARD.exists():
        raise RuntimeError("Refusing to overwrite an existing OOF evidence artifact")
    sys.path.insert(0, str(ADAPTER_PATH.parent))
    import fit_l2_curated as adapter

    state, context = adapter.preflight(PACKAGE, PROTOCOL, OUTPUT_GUARD)
    if state.get("status") != "READY_FOR_FIT" or context is None:
        raise RuntimeError("Package preflight failed: " + ";".join(state.get("blockers", [])))
    rows, provenance = adapter._load_partition(context, "train")
    family_indices: dict[str, list[int]] = defaultdict(list)
    for index, item in enumerate(provenance):
        family_indices[item["source_family_id"]].append(index)
    if len(family_indices) < 3:
        raise RuntimeError("At least three source families are required for leave-one-family-out evidence")

    truth = [row["label_id"] for row in rows]
    pooled_scores = [None] * len(rows)
    fold_summaries = {}
    fold_seconds = {}
    model_config = context["manifest"]["baseline"]
    for held_family, held_indices in sorted(family_indices.items()):
        held = set(held_indices)
        fit_indices = [index for index in range(len(rows)) if index not in held]
        fit_counts = Counter(rows[index]["label"] for index in fit_indices)
        if set(fit_counts) != set(LABELS):
            raise RuntimeError(f"Fold {held_family} lacks a class in fold training")
        model = adapter.legacy.build_model(model_config)
        started = time.perf_counter()
        with warnings.catch_warnings():
            warnings.simplefilter("error", ConvergenceWarning)
            model.fit([rows[index]["text"] for index in fit_indices], [truth[index] for index in fit_indices])
        fold_seconds[held_family] = time.perf_counter() - started
        scores = model.predict_proba([rows[index]["text"] for index in held_indices])
        if scores.shape != (len(held_indices), len(LABELS)):
            raise RuntimeError(f"Unexpected score matrix in fold {held_family}")
        for index, score in zip(held_indices, scores):
            pooled_scores[index] = [float(value) for value in score]
        pred = scores.argmax(axis=1).tolist()
        matrix = confusion_matrix([truth[index] for index in held_indices], pred, labels=[0, 1, 2])
        precision, recall, f1, support = precision_recall_fscore_support(
            [truth[index] for index in held_indices], pred, labels=[0, 1, 2], zero_division=0
        )
        fold_summaries[held_family] = {
            "heldout_rows": len(held_indices),
            "heldout_label_counts": dict(sorted(Counter(rows[index]["label"] for index in held_indices).items())),
            "fold_train_rows": len(fit_indices),
            "fold_train_label_counts": dict(sorted(fit_counts.items())),
            "argmax_confusion_matrix": matrix.tolist(),
            "argmax_per_class_f1": {label: float(f1[i]) for i, label in enumerate(LABELS)},
        }
        print(f"completed family fold: {held_family}; heldout_rows={len(held_indices)}; fit_seconds={fold_seconds[held_family]:.1f}", flush=True)
        del model

    if any(score is None for score in pooled_scores):
        raise RuntimeError("OOF scores do not cover all train rows")
    pooled_pred = [max(range(3), key=lambda label_id: pooled_scores[i][label_id]) for i in range(len(rows))]
    pooled_matrix = confusion_matrix(truth, pooled_pred, labels=[0, 1, 2])
    precision, recall, f1, support = precision_recall_fscore_support(truth, pooled_pred, labels=[0, 1, 2], zero_division=0)

    cutoffs = context["protocol"]["cutoff_grid"]
    acceptance = context["protocol"]["acceptance"]
    pair_summaries = []
    for tau_allow in cutoffs:
        for tau_block in cutoffs:
            by_family: dict[str, dict[str, int]] = {}
            class_totals = Counter()
            route_totals = Counter()
            for family, indices in family_indices.items():
                family_counts = Counter()
                for index in indices:
                    score = pooled_scores[index]
                    benign_score = score[0]
                    attack_score = score[1] + score[2]
                    if benign_score >= tau_allow and benign_score > attack_score:
                        route = "ALLOW_CANDIDATE"
                    elif attack_score >= tau_block and attack_score > benign_score:
                        route = "BLOCK_CANDIDATE"
                    else:
                        route = "REVIEW_TO_L3"
                    family_counts[f"{rows[index]['label']}:{route}"] += 1
                    route_totals[route] += 1
                    if route == "REVIEW_TO_L3":
                        class_totals[rows[index]["label"]] += 1
                by_family[family] = {
                    label: family_counts[f"{label}:REVIEW_TO_L3"] for label in LABELS
                }
            review_families = {
                label: sum(by_family[family][label] > 0 for family in by_family) for label in LABELS
            }
            support_pass = all(
                class_totals[label] >= acceptance["min_l3_train_review_per_class"]
                and review_families[label] >= acceptance["min_l3_train_review_families_per_class"]
                for label in LABELS
            )
            pair_summaries.append({
                "tau_allow": tau_allow,
                "tau_block": tau_block,
                "review_by_label": {label: class_totals[label] for label in LABELS},
                "review_families_by_label": review_families,
                "route_totals": {route: route_totals[route] for route in ROUTES},
                "l3_train_review_support_pass": support_pass,
            })

    aggregate_counts = dict(sorted(Counter(row["label"] for row in rows).items()))
    report = {
        "audit_id": "l2_source_family_oof_round05_r01",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "source-family-held-out train OOF diagnostics; not human gold; no test rows loaded",
        "package_id": context["manifest"]["package_id"],
        "dataset_version": context["manifest"]["dataset_version"],
        "package_manifest_sha256": sha256(PACKAGE / "DATASET_MANIFEST.json"),
        "protocol_sha256": sha256(PROTOCOL),
        "baseline_helper_sha256": sha256(Path(adapter.legacy.__file__)),
        "test_opened": False,
        "l3_run": False,
        "rows": len(rows),
        "label_counts": aggregate_counts,
        "family_count": len(family_indices),
        "folds": fold_summaries,
        "fold_fit_seconds": fold_seconds,
        "pooled_argmax": {
            "confusion_matrix": pooled_matrix.tolist(),
            "accuracy": float(pooled_matrix.trace() / pooled_matrix.sum()),
            "macro_f1": float(f1.mean()),
            "per_class_f1": {label: float(f1[i]) for i, label in enumerate(LABELS)},
            "per_class_support": {label: int(support[i]) for i, label in enumerate(LABELS)},
        },
        "routing_threshold_sweep": {
            "policy": "B >= tau_allow and B > A => ALLOW; A >= tau_block and A > B => BLOCK; otherwise REVIEW; ties REVIEW",
            "score_semantics": "uncalibrated OOF probabilities; source-family-held-out per row",
            "candidate_pair_count": len(pair_summaries),
            "l3_support_requirement": {
                "min_review_rows_per_class": acceptance["min_l3_train_review_per_class"],
                "min_train_families_with_review_per_class": acceptance["min_l3_train_review_families_per_class"],
            },
            "pairs_passing_l3_support": sum(item["l3_train_review_support_pass"] for item in pair_summaries),
            "pairs": pair_summaries,
        },
        "notes": [
            "All train predictions are out-of-fold by source family; no in-sample scores contribute to REVIEW support.",
            "Cutoff pairs remain candidates because validation selected no acceptable pair; L3 training was not started.",
            "Output contains aggregate counts only; no row IDs, text, payload paths, or per-row scores are persisted.",
        ],
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": "PASS_FAMILY_HELD_OUT_OOF_DIAGNOSTICS",
        "report": str(REPORT),
        "train_rows": len(rows),
        "families": len(family_indices),
        "pairs_passing_l3_support": report["routing_threshold_sweep"]["pairs_passing_l3_support"],
        "test_opened": False,
        "l3_run": False,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
