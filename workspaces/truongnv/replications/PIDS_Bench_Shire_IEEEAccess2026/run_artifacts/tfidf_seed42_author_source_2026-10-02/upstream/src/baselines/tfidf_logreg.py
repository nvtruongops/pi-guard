# src/baselines/tfidf_logreg.py
from __future__ import annotations
from pathlib import Path
import json
import random

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report, confusion_matrix, f1_score, roc_auc_score,
)
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
import joblib

DATA_DIR  = Path("data/pids_bench_v3")
EVAL_DIR  = DATA_DIR / "eval_subsets"
OOD_DIR   = DATA_DIR / "ood"
OUT_DIR   = Path("outputs/tfidf_baseline")
MODEL_DIR = Path("models/tfidf_logreg")
OUT_DIR.mkdir(parents=True, exist_ok=True)
MODEL_DIR.mkdir(parents=True, exist_ok=True)


def _load_split(name: str) -> pd.DataFrame:
    p = DATA_DIR / f"{name}.csv"
    if not p.exists():
        raise FileNotFoundError(f"Missing {p}.")
    return pd.read_csv(p)


def _build_pipeline(seed: int = 42) -> Pipeline:
    return Pipeline([
        ("tfidf", TfidfVectorizer(
            lowercase=True,
            strip_accents="unicode",
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.95,
        )),
        ("clf", LogisticRegression(
            max_iter=500,
            class_weight="balanced",
            C=1.0,
            penalty="l2",
            random_state=seed,
            n_jobs=None,
        )),
    ])


def _best_threshold_on_val(probs: np.ndarray, labels: np.ndarray,
                            grid: int = 501) -> float:
    """
    F1-maximising threshold found ONLY on validation data.
    Never call this with test or OOD labels — that would be data leakage.
    """
    thresholds      = np.linspace(0.0, 1.0, grid)
    best_t, best_f1 = 0.5, -1.0
    for t in thresholds:
        f1 = f1_score(labels, (probs >= t).astype(int), zero_division=0)
        if f1 > best_f1:
            best_f1 = f1
            best_t  = float(t)
    return best_t


def _metrics_at_threshold(probs: np.ndarray, y_true: np.ndarray,
                           threshold: float) -> dict:
    y_pred = (probs >= threshold).astype(int)
    tp = int(((y_true == 1) & (y_pred == 1)).sum())
    tn = int(((y_true == 0) & (y_pred == 0)).sum())
    fp = int(((y_true == 0) & (y_pred == 1)).sum())
    fn = int(((y_true == 1) & (y_pred == 0)).sum())
    n  = len(y_true)
    sdiv = lambda a, b: a / b if b else 0.0
    return {
        "n":         n,
        "f1":        round(f1_score(y_true, y_pred, zero_division=0), 4),
        "precision": round(sdiv(tp, tp + fp), 4),
        "recall":    round(sdiv(tp, tp + fn), 4),
        "fpr":       round(sdiv(fp, fp + tn), 4),
        "fnr":       round(sdiv(fn, fn + tp), 4),
        "threshold": round(threshold, 6),
    }


def _save_report(name: str, y_true: np.ndarray, y_pred: np.ndarray) -> Path:
    report  = classification_report(
        y_true, y_pred, target_names=["benign", "injection"], digits=4
    )
    cm      = confusion_matrix(y_true, y_pred, labels=[0, 1])
    out_txt = OUT_DIR / f"{name}_report.txt"
    with open(out_txt, "w") as f:
        f.write(report)  # type: ignore
        f.write("\nConfusion Matrix [[TN, FP],[FN, TP]]:\n")
        f.write(str(cm))
    return out_txt


def _eval_obfuscated_attacks(pipe: Pipeline, threshold: float,
                              csv_path: Path) -> dict:
    """
    obfuscated_attacks.csv is 100% injection (label=1).
    Metric: recall (detection rate) per obfuscation type.
    Threshold is passed in from val — never tuned on this data.
    """
    df    = pd.read_csv(csv_path).reset_index(drop=True)
    df["text"] = df["text"].astype(str)
    probs = pipe.predict_proba(df["text"])[:, 1]
    preds = (probs >= threshold).astype(int)

    n          = len(df)
    n_detected = int(preds.sum())

    per_obf: dict = {}
    for obf, group in df.groupby("obfuscation"):
        idx       = group.index.tolist()
        grp_preds = preds[idx]
        grp_n     = len(idx)
        grp_det   = int(grp_preds.sum())
        per_obf[str(obf)] = {
            "n":          grp_n,
            "n_detected": grp_det,
            "recall":     round(grp_det / grp_n, 6) if grp_n else 0.0,
        }

    result = {
        "n":               n,
        "n_detected":      n_detected,
        "overall_recall":  round(n_detected / n, 6) if n else 0.0,
        "overall_fnr":     round(1 - n_detected / n, 6) if n else 1.0,
        "threshold_used":  round(threshold, 6),
        "per_obfuscation": per_obf,
    }
    with open(OUT_DIR / "obfuscated_attacks_report.json", "w") as f:
        json.dump(result, f, indent=2)
    return result


def _eval_balanced_subtype(pipe: Pipeline, threshold: float,
                            csv_path: Path) -> dict:
    """
    balanced_subtype_test.csv has benign + injection with attack_type labels.
    Reports overall metrics + per-subtype breakdown.
    Threshold is passed in from val — never tuned on this data.
    """
    df     = pd.read_csv(csv_path).reset_index(drop=True)
    df["text"]  = df["text"].astype(str)
    df["label"] = df["label"].astype(int)
    probs  = pipe.predict_proba(df["text"])[:, 1]
    preds  = (probs >= threshold).astype(int)
    y_true = df["label"].values

    _save_report("balanced_subtype", y_true, preds)
    overall = _metrics_at_threshold(probs, y_true, threshold)

    sdiv = lambda a, b: a / b if b else 0.0
    per_subtype: dict = {}
    if "attack_type" in df.columns:
        for atype, group in df.groupby("attack_type"):
            idx    = group.index.tolist()
            g_true = y_true[idx]
            g_pred = preds[idx]
            g_tp   = int(((g_true == 1) & (g_pred == 1)).sum())
            g_tn   = int(((g_true == 0) & (g_pred == 0)).sum())
            g_fp   = int(((g_true == 0) & (g_pred == 1)).sum())
            g_fn   = int(((g_true == 1) & (g_pred == 0)).sum())
            per_subtype[str(atype)] = {
                "n":      len(g_true),
                "f1":     round(sdiv(2 * g_tp, 2 * g_tp + g_fp + g_fn), 4),
                "recall": round(sdiv(g_tp, g_tp + g_fn), 4),
                "fpr":    round(sdiv(g_fp, g_fp + g_tn), 4),
            }

    result = {**overall, "per_subtype": per_subtype}
    with open(OUT_DIR / "balanced_subtype_report.json", "w") as f:
        json.dump(result, f, indent=2)
    return result


def train_and_eval(grid_search: bool = False, seed: int = 42,
                   out_dir: Path | None = None,
                   output_model: Path | None = None,
                   overwrite: bool = False) -> dict:
    global OUT_DIR, MODEL_DIR
    if out_dir is not None:
        OUT_DIR   = Path(out_dir)
        MODEL_DIR = OUT_DIR / "model"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    if output_model is None:
        output_model = Path("models/tfidf_logreg.pkl")
    else:
        output_model = Path(output_model)
    if output_model.exists() and not overwrite:
        raise SystemExit(
            f"ERROR: {output_model} already exists. Pass --overwrite to replace it."
        )
    output_model.parent.mkdir(parents=True, exist_ok=True)

    random.seed(seed)
    np.random.seed(seed)

    # ── Load splits ───────────────────────────────────────────────────────────
    train_df = _load_split("train")
    val_df   = _load_split("val")
    test_df  = _load_split("test")

    X_train = train_df["text"].astype(str)
    y_train = train_df["label"].astype(int).values
    X_val   = val_df["text"].astype(str)
    y_val   = val_df["label"].astype(int).values
    X_test  = test_df["text"].astype(str)
    y_test  = test_df["label"].astype(int).values

    # ── Fit model on train only ───────────────────────────────────────────────
    pipe = _build_pipeline(seed=seed)
    if grid_search:
        param_grid = {
            "tfidf__ngram_range": [(1, 1), (1, 2)],
            "tfidf__min_df":      [1, 2, 3],
            "clf__C":             [0.25, 1.0, 2.0],
        }
        gs = GridSearchCV(pipe, param_grid, scoring="f1", cv=3, n_jobs=-1, verbose=1)
        gs.fit(X_train, y_train)  # type: ignore
        pipe = gs.best_estimator_
        with open(OUT_DIR / "grid_search_results.json", "w") as f:
            json.dump({"best_params": gs.best_params_,
                       "best_score":  gs.best_score_}, f, indent=2)
    else:
        pipe.fit(X_train, y_train)

    joblib.dump(pipe, MODEL_DIR / "tfidf_logreg.joblib")
    joblib.dump(pipe, output_model)
    print(f"Model saved → {output_model}")

    # ── Threshold tuning on val ONLY ─────────────────────────────────────────
    val_probs       = pipe.predict_proba(X_val)[:, 1]
    tuned_threshold = _best_threshold_on_val(val_probs, y_val)
    print(f"Val-tuned threshold: {tuned_threshold:.4f}")

    # ── Val report ────────────────────────────────────────────────────────────
    val_m = _metrics_at_threshold(val_probs, y_val, tuned_threshold)
    _save_report("val", y_val, (val_probs >= tuned_threshold).astype(int))
    print(f"Val  metrics  (τ={tuned_threshold:.4f}):  "
          f"F1={val_m['f1']:.4f}  P={val_m['precision']:.4f}  "
          f"R={val_m['recall']:.4f}  FPR={val_m['fpr']:.4f}")

    # ── Test (default 0.5 + tuned) ────────────────────────────────────────────
    test_probs       = pipe.predict_proba(X_test)[:, 1]
    test_res_default = _metrics_at_threshold(test_probs, y_test, 0.5)
    test_res_tuned   = _metrics_at_threshold(test_probs, y_test, tuned_threshold)
    _save_report("test", y_test, (test_probs >= tuned_threshold).astype(int))

    # ── Source-type breakdown on test ────────────────────────────────────────
    sdiv = lambda a, b: a / b if b else 0.0
    real_mask = (test_df["source_type"] == "real").values if "source_type" in test_df.columns else np.ones(len(test_df), dtype=bool)
    tmpl_mask = (test_df["source_type"] == "template").values if "source_type" in test_df.columns else np.zeros(len(test_df), dtype=bool)
    real_src_f1   = round(f1_score(y_test[real_mask], (test_probs[real_mask] >= tuned_threshold).astype(int), zero_division=0), 4)
    template_f1   = round(f1_score(y_test[tmpl_mask], (test_probs[tmpl_mask] >= tuned_threshold).astype(int), zero_division=0), 4)

    # ── ROC-AUC ───────────────────────────────────────────────────────────────
    try:
        roc_auc = round(float(roc_auc_score(y_test, test_probs)), 4)
    except Exception:
        roc_auc = None

    # ── hard_benign FPR (aggregate + by origin) ──────────────────────────────
    hb_path = EVAL_DIR / "hard_benign_test.csv"
    hard_benign_result = None
    hb_fpr_agg = hb_fpr_real = hb_fpr_curated = None
    hb_probs = hb_df = None
    if hb_path.exists():
        hb_df    = pd.read_csv(hb_path)
        hb_probs = pipe.predict_proba(hb_df["text"].astype(str))[:, 1]
        hb_n     = len(hb_df)
        hb_fpr_agg = round(float((hb_probs >= tuned_threshold).mean()), 4)

        hb_real_mask    = (hb_df["source_type"] == "real").values if "source_type" in hb_df.columns else np.ones(hb_n, dtype=bool)
        hb_curated_mask = (hb_df["source_type"] == "curated").values if "source_type" in hb_df.columns else np.zeros(hb_n, dtype=bool)
        hb_fpr_real    = round(float((hb_probs[hb_real_mask] >= tuned_threshold).mean()), 4) if hb_real_mask.any() else 0.0
        hb_fpr_curated = round(float((hb_probs[hb_curated_mask] >= tuned_threshold).mean()), 4) if hb_curated_mask.any() else 0.0

        hard_benign_result = {
            "n":               hb_n,
            "fpr_default_0.5": round(float((hb_probs >= 0.5).mean()),            6),
            "fpr_tuned":       hb_fpr_agg,
            "fpr_real_origin": hb_fpr_real,
            "fpr_curated_origin": hb_fpr_curated,
            "tuned_threshold": round(tuned_threshold, 6),
            "n_flagged_default": int((hb_probs >= 0.5).sum()),
            "n_flagged_tuned":   int((hb_probs >= tuned_threshold).sum()),
        }
        with open(OUT_DIR / "hard_benign_fpr.json", "w") as f:
            json.dump(hard_benign_result, f, indent=2)
    else:
        print(f"WARNING: skipping hard_benign_test.csv because file not found: {hb_path}")

    # ── Obfuscated attacks (detection recall) ────────────────────────────────
    obf_path = EVAL_DIR / "obfuscated_attacks.csv"
    obf_res  = None
    if obf_path.exists():
        obf_res = _eval_obfuscated_attacks(pipe, tuned_threshold, obf_path)
    else:
        print(f"WARNING: skipping obfuscated_attacks.csv because file not found: {obf_path}")

    # ── Balanced subtype test ─────────────────────────────────────────────────
    sub_path = EVAL_DIR / "balanced_subtype_test.csv"
    sub_res  = None
    if sub_path.exists():
        sub_res = _eval_balanced_subtype(pipe, tuned_threshold, sub_path)
    else:
        print(f"WARNING: skipping balanced_subtype_test.csv because file not found: {sub_path}")

    # ── Domain OOD (aggregate + per-domain) ───────────────────────────────────
    dom_path = OOD_DIR / "domain_ood.csv"
    domain_ood_result: dict | None = None
    dom_agg: dict = {}
    per_dom: dict = {}
    if dom_path.exists():
        dom_df    = pd.read_csv(dom_path)
        dom_probs = pipe.predict_proba(dom_df["text"].astype(str))[:, 1]
        dom_true  = dom_df["label"].astype(int).values
        dom_agg   = _metrics_at_threshold(dom_probs, dom_true, tuned_threshold)
        domain_ood_result = {"aggregate": dom_agg, "per_domain": {}}
        for dom_name, grp in dom_df.groupby("domain"):
            idx = grp.index.tolist()
            g_probs = dom_probs[idx]; g_true = dom_true[idx]
            benign_mask = g_true == 0; attack_mask = g_true == 1
            d_fpr    = round(float((g_probs[benign_mask] >= tuned_threshold).mean()), 4) if benign_mask.any() else 0.0
            d_recall = round(float((g_probs[attack_mask] >= tuned_threshold).mean()), 4) if attack_mask.any() else 0.0
            domain_ood_result["per_domain"][str(dom_name)] = {"fpr": d_fpr, "recall": d_recall}
        per_dom = domain_ood_result["per_domain"]
        with open(OUT_DIR / "domain_ood_report.json", "w") as f:
            json.dump(domain_ood_result, f, indent=2)
    else:
        print(f"WARNING: skipping domain_ood.csv because file not found: {dom_path}")

    # ── Structural OOD (aggregate + per-transform) ────────────────────────────
    struct_path = OOD_DIR / "structural_ood.csv"
    struct_ood_result: dict | None = None
    struct_agg: dict = {}
    per_tr: dict = {}
    if struct_path.exists():
        struct_df    = pd.read_csv(struct_path)
        struct_probs = pipe.predict_proba(struct_df["text"].astype(str))[:, 1]
        struct_true  = struct_df["label"].astype(int).values
        struct_agg   = _metrics_at_threshold(struct_probs, struct_true, tuned_threshold)
        struct_ood_result = {"aggregate": struct_agg, "per_transform": {}}
        for tr_name, grp in struct_df.groupby("transform_type"):
            idx = grp.index.tolist()
            g_probs = struct_probs[idx]; g_true = struct_true[idx]
            benign_mask = g_true == 0; attack_mask = g_true == 1
            t_fpr    = round(float((g_probs[benign_mask] >= tuned_threshold).mean()), 4) if benign_mask.any() else 0.0
            t_recall = round(float((g_probs[attack_mask] >= tuned_threshold).mean()), 4) if attack_mask.any() else 0.0
            struct_ood_result["per_transform"][str(tr_name)] = {"fpr": t_fpr, "recall": t_recall}
        per_tr = struct_ood_result["per_transform"]
        with open(OUT_DIR / "structural_ood_report.json", "w") as f:
            json.dump(struct_ood_result, f, indent=2)
    else:
        print(f"WARNING: skipping structural_ood.csv because file not found: {struct_path}")

    # ── Threshold sweep for Figure 1 ─────────────────────────────────────────
    sweep_taus = np.arange(0.0, 1.001, 0.002)
    sweep_rows = []
    for tau in sweep_taus:
        sw_f1 = round(float(f1_score(y_test, (test_probs >= tau).astype(int), zero_division=0)), 6)
        row   = {"tau": round(float(tau), 4), "test_F1": sw_f1}
        if hb_probs is not None:
            row["hb_FPR_agg"] = round(float((hb_probs >= tau).mean()), 6)
        sweep_rows.append(row)
    sweep_df = pd.DataFrame(sweep_rows)
    sweep_df.to_csv(OUT_DIR / "threshold_sweep.csv", index=False)

    # ── Save probability CSVs ─────────────────────────────────────────────────
    pd.DataFrame({"text": test_df["text"].astype(str).values,
                  "true_label": y_test,
                  "probability_score": test_probs,
                  "source_type": test_df["source_type"].values if "source_type" in test_df.columns else ""
                  }).to_csv(OUT_DIR / "test_predictions.csv", index=False)
    if hb_df is not None and hb_probs is not None:
        pd.DataFrame({"text": hb_df["text"].values,
                      "true_label": 0,
                      "probability_score": hb_probs,
                      "source_type": hb_df["source_type"].values if "source_type" in hb_df.columns else ""
                      }).to_csv(OUT_DIR / "hard_benign_predictions.csv", index=False)

    # ── Summary ───────────────────────────────────────────────────────────────
    summary = {
        "model":          "tfidf_logreg",
        "seed":           seed,
        "model_saved_to": str(output_model),
        "val_tuned_threshold": round(tuned_threshold, 6),
        "test_results": {
            "default_threshold_0.5": test_res_default,
            "val_tuned_threshold":   test_res_tuned,
        },
        "real_src_f1":   real_src_f1,
        "template_f1":   template_f1,
        "roc_auc":       roc_auc,
        "hard_benign_test_fpr": hard_benign_result,
        "obfuscated_attacks": {
            "overall_recall": obf_res["overall_recall"],
            "overall_fnr":    obf_res["overall_fnr"],
        } if obf_res is not None else None,
        "balanced_subtype": {
            "f1": sub_res["f1"], "recall": sub_res["recall"], "fpr": sub_res["fpr"]
        } if sub_res is not None else None,
        "domain_ood": domain_ood_result,
        "structural_ood": struct_ood_result,
    }
    with open(OUT_DIR / "summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print("TF-IDF + Logistic Regression complete.")
    print(f"  test F1  (tuned τ={tuned_threshold:.3f}):  {test_res_tuned['f1']:.4f}")
    print(f"  test P={test_res_tuned['precision']:.4f}  R={test_res_tuned['recall']:.4f}  FPR={test_res_tuned['fpr']:.4f}")
    if hb_fpr_agg is not None:
        print(f"  hard_benign FPR (tuned):   {hb_fpr_agg:.4f}")
    if obf_res is not None:
        print(f"  obfuscated recall:         {obf_res['overall_recall']:.4f}")
    print(f"  summary → {OUT_DIR / 'summary.json'}")

    # Return all metrics for orchestration script
    return {
        "IID_F1":           test_res_tuned["f1"],
        "real_src_F1":      real_src_f1,
        "template_F1":      template_f1,
        "IID_recall":       test_res_tuned["recall"],
        "IID_precision":    test_res_tuned["precision"],
        "test_FPR":         test_res_tuned["fpr"],
        "ROC_AUC":          roc_auc,
        "tau":              round(tuned_threshold, 6),
        "hb_FPR_agg":       hb_fpr_agg,
        "hb_FPR_real":      hb_fpr_real,
        "hb_FPR_curated":   hb_fpr_curated,
        "obf_recall":       obf_res["overall_recall"] if obf_res is not None else None,
        "domain_OOD_F1_agg":dom_agg.get("f1"),
        "medical_FPR":      per_dom.get("medical", {}).get("fpr"),
        "medical_recall":   per_dom.get("medical", {}).get("recall"),
        "legal_FPR":        per_dom.get("legal",   {}).get("fpr"),
        "legal_recall":     per_dom.get("legal",   {}).get("recall"),
        "finance_FPR":      per_dom.get("finance", {}).get("fpr"),
        "finance_recall":   per_dom.get("finance", {}).get("recall"),
        "code_FPR":         per_dom.get("code",    {}).get("fpr"),
        "code_recall":      per_dom.get("code",    {}).get("recall"),
        "struct_OOD_F1_agg":  struct_agg.get("f1"),
        "struct_OOD_FPR_agg": struct_agg.get("fpr"),
        "json_wrap_FPR":         per_tr.get("json_wrap",                {}).get("fpr"),
        "json_wrap_recall":      per_tr.get("json_wrap",                {}).get("recall"),
        "prompt_dilute_FPR":     per_tr.get("prompt_dilute",            {}).get("fpr"),
        "prompt_dilute_recall":  per_tr.get("prompt_dilute",            {}).get("recall"),
        "prefix_mimic_FPR":      per_tr.get("instruction_prefix_mimic", {}).get("fpr"),
        "prefix_mimic_recall":   per_tr.get("instruction_prefix_mimic", {}).get("recall"),
    }


def run(grid_search: bool = False) -> None:
    train_and_eval(grid_search=grid_search)


if __name__ == "__main__":
    import argparse as _ap
    _p = _ap.ArgumentParser()
    _p.add_argument("--seed",         type=int,  default=42)
    _p.add_argument("--output_model", type=str,  default="models/tfidf_logreg.pkl",
                    help="Path to save the fitted sklearn Pipeline (.pkl)")
    _p.add_argument("--overwrite",    action="store_true", default=False,
                    help="Overwrite output_model if it already exists")
    _a = _p.parse_args()
    train_and_eval(grid_search=False, seed=_a.seed,
                   output_model=Path(_a.output_model), overwrite=_a.overwrite)
