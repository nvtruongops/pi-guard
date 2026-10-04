# Proposed Two-Tier Architecture — Evidence Audit

## Scope Boundary Declaration

- **IN-SCOPE:** separate paper-specific results from PI-Guard's proposed design.
- **OUT-OF-SCOPE:** cross-paper model/dataset comparisons, trained-cascade claims, and achieved system targets.

The verified local evidence consists of the PIDS-Bench author TF-IDF + Logistic Regression baseline on pinned PIDS-Bench data and a PIGuard checkpoint on assets distributed with the PIGuard release. Their data, labels, and protocols differ, so they must not be combined into a ranking or cascade. See the [PIDS-Bench report](../../replications/PIDS_Bench_Shire_IEEEAccess2026/REPORT.md), the [PIGuard-only report](../../replications/02_DeBERTa_v3_Semantic_Classifier/reports/review1_paper_model_public_rerun_2026-09-30/REPORT.md), and sources [[18]](../../References/REFERENCES_LOG.md#ref18) [[44]](../../References/REFERENCES_LOG.md#ref44) [[45]](../../References/REFERENCES_LOG.md#ref45).

The public-vector suite, D1–D6 matrix, mixed-source TF-IDF fits, ProtectAI-on-PIDS/PIGuard outputs, and dependent figures are withdrawn because their local model/data pairings cross paper origins. The folders remain because automatic approval review blocked deletion. Do not quote their old scores.

PI-Guard's sequential classifier remains a design proposal. Neither eligible run measures conditional routing, a joint held-out set, or end-to-end cascade behavior. P95 < 30 ms and FPR < 1.5% remain targets only.
