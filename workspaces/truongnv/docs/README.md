# PI-Guard documentation index

## Scope Boundary Declaration

- IN-SCOPE: active Review 2 status, paper-matched local evidence, and the proposed ingress architecture.
- OUT-OF-SCOPE: treating withdrawn artifacts or older reports as current metrics; claiming service acceptance from a research run.

## Current project status

The Review 2 umbrella task remains open. A separate seed-42 TF-IDF → DeBERTa cascade experiment is complete on one pinned PIDS-Bench split. See the [experiment report](../reports/experiment_reports/tfidf_deberta_cascade_2026-10-04/REPORT.md) and [task](../reports/tasks_for_review2/TASK.md). The report documents high false-positive rates on hard-benign and structural-OOD slices and model-only P95 timing above the design target.

The [Review 1 ingress architecture](../reports/report%20for%20review%201%20lan%202/README.md) remains a proposal: L1 input handling, L2 route candidates, L3 REVIEW scoring, and API request aggregation. Only API aggregation emits final request ALLOW/BLOCK. Proposal cutoffs are not established service settings; experiment-selected gates are specific to their run.

## Local evidence

- [PIDS-Bench author TF-IDF replication](../replications/PIDS_Bench_Shire_IEEEAccess2026/REPORT.md)
- [PIGuard checkpoint on PIGuard assets](../replications/02_DeBERTa_v3_Semantic_Classifier/reports/review1_paper_model_public_rerun_2026-09-30/REPORT.md)
- [Local seed-42 cascade experiment](../reports/experiment_reports/tfidf_deberta_cascade_2026-10-04/REPORT.md)

Withdrawn files may remain in historical folders. Consult the [withdrawal register](../reports/tasks_for_meeting_6/WITHDRAWN_DATA_ARTIFACTS.md) and provenance audit; do not describe them as deleted unless the filesystem confirms it.
