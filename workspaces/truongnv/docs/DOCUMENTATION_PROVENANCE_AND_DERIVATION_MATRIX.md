# Documentation provenance and derivation matrix

## Scope Boundary Declaration

- **IN-SCOPE:** trace current reportable local metrics, withdrawn report families, and the provenance of the current architecture proposal in `workspaces/truongnv/`.
- **OUT-OF-SCOPE:** certify literature claims without their original citations or treat hashes as paper fidelity.

| Evidence family | Current entrypoint | Provenance status |
|---|---|---|
| PIDS-Bench TF-IDF baseline | [Canonical report](../replications/PIDS_Bench_Shire_IEEEAccess2026/REPORT.md) | Same-paper author code/data; 3,918 test text/label pairs matched and metrics recomputed from saved predictions. |
| PIGuard checkpoint on PIGuard assets | [PIGuard-only report](../replications/02_DeBERTa_v3_Semantic_Classifier/reports/review1_paper_model_public_rerun_2026-09-30/REPORT.md) | PIGuard source hashes and input coverage verified; only the PIGuard model's slices are retained. |
| Review 1 public-vector suite | [Withdrawal register](../reports/tasks_for_meeting_6/WITHDRAWN_DATA_ARTIFACTS.md) | Cross-paper dataset/checkpoint pairing; withdrawn, not current evidence. |
| Review 2/Tier 1 TF-IDF | [Withdrawal register](../reports/tasks_for_meeting_6/WITHDRAWN_DATA_ARTIFACTS.md) | Project-built mixed-source fits and splits; not a paper-matched result. |
| D1–D6 matrix | [Withdrawal register](../reports/tasks_for_meeting_6/WITHDRAWN_DATA_ARTIFACTS.md) | Cross-paper model/dataset pairing; withdrawn, not current evidence. |
| ProtectAI comparisons on PIDS/PIGuard data | [Withdrawal register](../reports/tasks_for_meeting_6/WITHDRAWN_DATA_ARTIFACTS.md) | Model and data belong to different paper origins under the user's rule. |
| Review 1 lần 2 ingress architecture | [Proposal README](../reports/report%20for%20review%201%20lan%202/README.md) · [task boundary](../reports/report%20for%20review%201%20lan%202/TASK.md) | User-directed design proposal; describes L1/L2/L3 plus API aggregation. It is not a model run, implementation proof, or achieved metric. |

The withdrawn cross-paper and project-built artifacts listed above have been physically purged following the provenance cleanup audit. They must not be cited or rerun. Details are in the [withdrawal register](../reports/tasks_for_meeting_6/WITHDRAWN_DATA_ARTIFACTS.md) and [model-paper alignment audit](../reports/experiment_reports/MODEL_PAPER_CODE_ALIGNMENT_AUDIT_2026-10-02.md).

