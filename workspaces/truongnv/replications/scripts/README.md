# Replication workspace verification scripts

## Current checks

- [`verify_replication_assets.py`](../verify_replication_assets.py) checks retained source-data hashes/counts, absence of non-origin copies and withdrawn project artifacts, disabled legacy runners, and moved-folder state. A pass confirms local files/state only; it does not certify model fidelity or upstream authorship.
- [`verify_review2_source_rows.py`](../01_TFIDF_Syntactic_Baseline/reports/review2_baselines_2026-09-29/verify_review2_source_rows.py) and [`verify_review2_saved_metrics.py`](../01_TFIDF_Syntactic_Baseline/reports/review2_baselines_2026-09-29/verify_review2_saved_metrics.py) can audit row mapping and arithmetic in the historical Review 2 artifacts. They do not establish same-paper model/data provenance, so Review 2/Tier 1 results remain withdrawn and must not be reported as current evidence.

Only the [PIDS-Bench same-paper TF-IDF report](../PIDS_Bench_Shire_IEEEAccess2026/REPORT.md) and [PIGuard-on-own-release report](../02_DeBERTa_v3_Semantic_Classifier/reports/review1_paper_model_public_rerun_2026-09-30/REPORT.md) are retained as local empirical evidence under the current paper-origin rule.

For the current source/data decisions and audit limits, see [`REPLICATIONS_FOLDER_AUDIT.md`](../../reports/experiment_reports/replications_folder_audit_2026-09-30/REPLICATIONS_FOLDER_AUDIT.md) and [`WORKSPACE_PROVENANCE_AUDIT_2026-09-30.md`](../../reports/experiment_reports/WORKSPACE_PROVENANCE_AUDIT_2026-09-30.md).

Historical one-off source checks from the Meeting 5 task folder are not current provenance certificates. That task folder is preserved as requested.
