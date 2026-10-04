# Meeting 6 — archive and evidence status

## Scope Boundary Declaration

- **IN-SCOPE:** status of Meeting 6 records, withdrawn artifacts, and local results that pass the same-paper pairing rule.
- **OUT-OF-SCOPE:** restoring cross-paper benchmarks, using project-created inputs, or claiming the cascade was measured.

> **Status:** the old Meeting 6 benchmark tables and D1–D6 matrix are withdrawn. They combine models and datasets from different papers, so they are not valid paper-matched results. Automatic approval review blocked deletion; the folders remain on disk and must not be cited or rerun. See [WITHDRAWN_DATA_ARTIFACTS.md](./WITHDRAWN_DATA_ARTIFACTS.md).

## Current evidence

- [Workspace provenance and metric audit](../experiment_reports/WORKSPACE_PROVENANCE_AUDIT_2026-09-30.md) lists checks, retained metrics, and residual folders.
- [PIDS-Bench TF-IDF](../../replications/PIDS_Bench_Shire_IEEEAccess2026/REPORT.md) uses the same paper's baseline method and pinned data; test rows were matched to source.
- [PIGuard-only run](../../replications/02_DeBERTa_v3_Semantic_Classifier/reports/review1_paper_model_public_rerun_2026-09-30/REPORT.md) retains only the checkpoint's results on assets released with PIGuard. The ProtectAI comparison is withdrawn.

No local result establishes a three-class PI-Guard model, a two-tier cascade, or achieved system P95/FPR targets.
