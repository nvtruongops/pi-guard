#!/usr/bin/env python3
"""Post-hoc aggregate threshold diagnostic on the full round07 validation scores."""
from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
PRIVATE = REPO / "workspaces" / "truongnv" / "pi_guard_pipeline"
SCORES = PRIVATE / "training_bases" / "pi_guard_tfidf_tier1" / "runs" / "l2_jb_moderated_weight_round07_r01_full_20261013" / "validation_predictions.jsonl"
PROTOCOL = ROOT / "AUTONOMOUS_PROTOCOL.json"
RUNNER = ROOT / "run_l2_jb_moderated_weight_round07.py"
REPORT = ROOT / "l2_supplemental_threshold_grid_round07_r01.json"
LABELS = ("benign", "PI", "JB")
GRID = (0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99, 0.995, 0.9975, 0.999, 0.9995, 0.9999, 0.99999)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    if REPORT.exists():
        raise FileExistsError("THRESHOLD_REPORT_EXISTS; create a new version")
    rows = []
    with SCORES.open(encoding="utf-8") as stream:
        for line in stream:
            item = json.loads(line)
            scores = item["scores_uncalibrated"]
            rows.append((item["true_label"], float(scores["benign"]),
                         max(float(scores["PI"]), float(scores["JB"]))))
    if not rows:
        raise ValueError("VALIDATION_SCORE_FILE_EMPTY")
    support = Counter(label for label, _, _ in rows)
    if set(support) != set(LABELS):
        raise ValueError("VALIDATION_SCORE_CLASS_SUPPORT_INVALID")

    diagnostics = []
    for tau_allow, tau_block in itertools.product(GRID, repeat=2):
        counts = {label: Counter() for label in LABELS}
        total = Counter()
        for label, benign_score, attack_score in rows:
            if benign_score >= tau_allow and benign_score > attack_score:
                route = "ALLOW_CANDIDATE"
            elif attack_score >= tau_block and attack_score > benign_score:
                route = "BLOCK_CANDIDATE"
            else:
                route = "REVIEW_TO_L3"
            counts[label][route] += 1
            total[route] += 1
        summary = {
            "tau_allow": tau_allow,
            "tau_block": tau_block,
            "review_rate": total["REVIEW_TO_L3"] / len(rows),
            "review_counts_by_label": {label: counts[label]["REVIEW_TO_L3"] for label in LABELS},
            "pi_early_allow_rate": counts["PI"]["ALLOW_CANDIDATE"] / support["PI"],
            "jb_early_allow_rate": counts["JB"]["ALLOW_CANDIDATE"] / support["JB"],
            "benign_early_block_rate": counts["benign"]["BLOCK_CANDIDATE"] / support["benign"],
            "counts_by_label_and_route": {label: dict(counts[label]) for label in LABELS},
        }
        diagnostics.append(summary)

    limits = json.loads(PROTOCOL.read_text(encoding="utf-8"))["acceptance"]
    feasible = [item for item in diagnostics
                if item["review_rate"] <= limits["max_review_rate"]
                and min(item["review_counts_by_label"].values()) >= limits["min_validation_review_per_class"]
                and item["pi_early_allow_rate"] <= limits["max_pi_early_allow_rate"]
                and item["jb_early_allow_rate"] <= limits["max_jb_early_allow_rate"]
                and item["benign_early_block_rate"] <= limits["max_benign_early_block_rate"]]
    best = min(feasible, key=lambda item: (
        item["review_counts_by_label"]["benign"] + item["review_counts_by_label"]["PI"] + item["review_counts_by_label"]["JB"],
        item["counts_by_label_and_route"]["PI"].get("ALLOW_CANDIDATE", 0)
        + item["counts_by_label_and_route"]["JB"].get("ALLOW_CANDIDATE", 0),
        item["counts_by_label_and_route"]["benign"].get("BLOCK_CANDIDATE", 0),
        -item["tau_allow"], -item["tau_block"],
    )) if feasible else None
    original_grid = set(json.loads(PROTOCOL.read_text(encoding="utf-8"))["cutoff_grid"])
    report = {
        "report_id": "l2_supplemental_threshold_grid_round07_r01",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "POSTHOC_EXPLORATORY_VALIDATION_DIAGNOSTIC_ONLY",
        "scope": "all validation prediction scores for the retained JB-moderated L2 candidate; aggregate routes only",
        "rows": len(rows),
        "label_support": dict(support),
        "original_predeclared_grid": sorted(original_grid),
        "supplemental_grid": list(GRID),
        "pair_count": len(diagnostics),
        "feasible_pair_count_under_exploratory_limits": len(feasible),
        "best_pair_under_existing_exploratory_selection_order": best,
        "selection_limitations": [
            "This threshold grid was expanded after observing the retained candidate's validation diagnostics; it is post-hoc.",
            "The numerical acceptance limits are engineering assumptions in the research protocol, not owner-approved L2 rubric values.",
            "This validation-only result is not an L2 PASS and must be checked on independent train-only family OOF scores before being retained.",
        ],
        "limits_source_protocol_sha256": sha256(PROTOCOL),
        "score_artifact_sha256": sha256(SCORES),
        "candidate_runner_sha256": sha256(RUNNER),
        "formal_acceptance_gate": "GATE_UNSPECIFIED",
        "test_opened": False,
        "l3_run": False,
        "row_ids_or_text_emitted": False,
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                      encoding="utf-8", newline="\n")
    print(json.dumps({
        "status": report["status"],
        "pair_count": report["pair_count"],
        "feasible_pair_count": report["feasible_pair_count_under_exploratory_limits"],
        "best_pair": best,
        "test_opened": False,
        "l3_run": False,
        "report": str(REPORT),
    }, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
