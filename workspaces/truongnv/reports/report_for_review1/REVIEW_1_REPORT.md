# PI-Guard — Review 1 evidence status

**Evidence cut-off:** 30 September 2026. This report follows the strict paper-origin audit.

## Scope Boundary Declaration

- **IN-SCOPE:** current paper-matched local metrics and their limits under `workspaces/truongnv/`.
- **OUT-OF-SCOPE:** withdrawn cross-paper metrics, a measured three-class PI-Guard model, or a two-tier cascade claim.

## Current empirical evidence

Two individual runs remain in the local evidence set. First, the PIDS-Bench author TF-IDF + Logistic Regression baseline was fit on its pinned train split and evaluated on its pinned binary test split. All 3,918 saved test text/label pairs match the source test split; the report's metric values were recomputed from saved scores. This is a single-seed binary result, not PI-Guard's three-class performance [[44]](../../References/REFERENCES_LOG.md#ref44) [[45]](../../References/REFERENCES_LOG.md#ref45). See the [PIDS-Bench report](../../replications/PIDS_Bench_Shire_IEEEAccess2026/REPORT.md).

Second, the PIGuard checkpoint was evaluated on public assets distributed with its own pinned release. Six source hashes and 1,435 input rows passed the local verifier. The report retains only PIGuard's slice results; BIPIA rows are payload strings, not full task/context inputs [[18]](../../References/REFERENCES_LOG.md#ref18). See the [PIGuard-only report](../../replications/02_DeBERTa_v3_Semantic_Classifier/reports/review1_paper_model_public_rerun_2026-09-30/REPORT.md).

These two runs use different papers, labels, data, and protocols. They are not a head-to-head comparison.

## Withdrawn local claims

The former 606-row public-vector benchmark, mixed-source Review 2/Tier 1 fits, D1–D6 checkpoint matrix, ProtectAI-on-PIDS/PIGuard outputs, and dependent metrics, latency values, charts, and recommendations are withdrawn because they pair models and data from different papers. Their folders remain on disk because automatic approval review blocked deletion. Do not cite, run, or use them to regenerate evidence. See the [withdrawn-artifact register](../tasks_for_meeting_6/WITHDRAWN_DATA_ARTIFACTS.md) and [workspace audit](../experiment_reports/WORKSPACE_PROVENANCE_AUDIT_2026-09-30.md).

## Architecture and project status

PI-Guard's three-class guardrail and two-tier cascade remain proposals. Neither retained run measures conditional routing or an end-to-end service. P95 < 30 ms and FPR < 1.5% remain project targets, not achieved results. The Review 1 completion date is recorded in the [dated completion report](REVIEW_1_COMPLETION_REPORT_2026-10-04.md); this evidence-status report does not serve as a council acceptance record.
