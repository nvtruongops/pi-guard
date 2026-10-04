# Task 2 — attack vectors and models (withdrawn)

## Scope Boundary Declaration

- **IN-SCOPE:** record the status of the former Meeting 5 attack/model report and direct readers to currently verifiable evidence.
- **OUT-OF-SCOPE:** the former local latency estimate, treating a project-built TF-IDF classifier as a Jain et al. reproduction, or reporting proposed cascade behavior as measured.

> **Status:** the former report has been withdrawn. It included an unsupported `2.8 ms` classifier estimate and several model claims that were not backed by a locked evaluation artifact. Its historical attack examples are not benchmark records and its model comparison is not current evidence.

## Current evidence

- The [workspace provenance audit](../../experiment_reports/WORKSPACE_PROVENANCE_AUDIT_2026-09-30.md) lists the retained source data, verifiers, and claim limits.
- Review 2 and D1–D6 local runs have been withdrawn because the evaluated model and data did not share one paper's protocol; saved checksums or recomputed scores do not make those comparisons eligible.
- The retained [PIGuard-only report](../../../replications/02_DeBERTa_v3_Semantic_Classifier/reports/review1_paper_model_public_rerun_2026-09-30/REPORT.md) covers its checkpoint on assets released with that paper.

## Claim boundary

The TF-IDF → DeBERTa cascade remains a proposal. PI-Guard Tier 2 and end-to-end cascade performance have not been evaluated.
