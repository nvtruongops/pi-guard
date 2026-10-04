# Replication candidate runbook

**Status (2026-09-30):** use the current folder audit and source-backed data inventory below. Earlier benchmark procedures and local proxy outputs are historical; do not use them as current model results.

## Scope Boundary Declaration

- **IN-SCOPE:** selecting public model/code and public dataset assets for external text-level detector evaluation.
- **OUT-OF-SCOPE:** fitting classifiers on withdrawn project probes, relabeling architecture references as detectors, and changing Meeting 6 historical content.

## Before a new experiment

1. Read [`README.md`](./README.md), [`BENCHMARK_RESULTS_DASHBOARD.md`](./BENCHMARK_RESULTS_DASHBOARD.md), and [`SHARED_DATASETS_PROVENANCE.md`](./SHARED_DATASETS_PROVENANCE.md).
2. Run `python workspaces/truongnv/replications/verify_replication_assets.py`. A pass confirms local asset hashes/counts and cleanup state, not paper-level fidelity.
3. For each model, pin the public checkpoint/repository revision, identify the public source dataset and its unit of analysis, use the author's method, save raw predictions, and compare only on compatible splits/labels.
4. Report FPR ≤ 1.5% and P95 < 30 ms as secondary operating objectives. Model inclusion depends first on detecting the required attack variants with valid evidence.
5. Do not use former 10/20/22-row project probes or their derived scores. Do not label the local DataSentinel regex/canary, Jain TF-IDF, or BIPIA TF-IDF adapters as their named paper methods.

## Current folder decisions

See [`replications_folder_audit_2026-09-30/`](../reports/experiment_reports/replications_folder_audit_2026-09-30/REPLICATIONS_FOLDER_AUDIT.md). Useful white-box, victim-LLM, encoder-only, and withdrawn pilot packages are preserved in [`references_study/`](../references_study/README.md).
