# Experiment evidence status — 2026-09-30

## Scope Boundary Declaration

- **IN-SCOPE:** local model/data pairings and reportable measurements under this workspace.
- **OUT-OF-SCOPE:** new training, cross-paper comparisons, or treating a paper's metric as a PI-Guard result.

## Current local evidence

| Model/method | Paper-origin pairing | Evidence and boundary |
|---|---|---|
| TF-IDF + Logistic Regression | PIDS-Bench author baseline code and frozen PIDS-Bench data. | Test prediction rows match the pinned test file; primary metrics were recomputed. Binary task, one seed; no cascade. [Report](./PIDS_Bench_Shire_IEEEAccess2026/REPORT.md). |
| PIGuard DeBERTa-v3 | PIGuard checkpoint and evaluation assets from its pinned release. | Source hashes, input coverage, and saved predictions verified. Report only PIGuard's individual slices; exclude ProtectAI comparison. [Report](./02_DeBERTa_v3_Semantic_Classifier/reports/review1_paper_model_public_rerun_2026-09-30/REPORT.md). |

## Withdrawn comparisons

The Review 1 public-vector run, D1–D6 matrix, Review 2/Tier 1 mixed-source fits, ProtectAI-on-PIDS/PIGuard runs, and derived charts are withdrawn because they pair models and data from different papers. Recomputed scores do not fix that protocol mismatch. Files remain because automatic approval review blocked deletion; details are in the [provenance audit](../reports/experiment_reports/WORKSPACE_PROVENANCE_AUDIT_2026-09-30.md).

P95 < 30 ms and FPR < 1.5% are project targets. No end-to-end PI-Guard cascade has been measured.
