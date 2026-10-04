# Data engineering and provenance status

## Scope Boundary Declaration

- **IN-SCOPE:** local dataset and result bundles in the `truongnv` workspace after per-paper provenance review.
- **OUT-OF-SCOPE:** present a project-assembled cross-paper suite as one paper's data, or claim project-wide key coverage from file counts.

The retained local metric set is limited to the PIDS-Bench same-paper TF-IDF baseline and PIGuard-only inference on PIGuard-released assets. The PIDS-Bench prediction rows match the pinned test split; the PIGuard verifier checks the source-release hashes. See the [workspace audit](../../../reports/experiment_reports/WORKSPACE_PROVENANCE_AUDIT_2026-09-30.md), [PIDS-Bench report](../../../replications/PIDS_Bench_Shire_IEEEAccess2026/REPORT.md), and [PIGuard-only report](../../../replications/02_DeBERTa_v3_Semantic_Classifier/reports/review1_paper_model_public_rerun_2026-09-30/REPORT.md).

The Review 1 public-vector suite, Review 2/Tier 1 mixed-source fits, D1–D6 matrix, and ProtectAI-on-other-paper evaluations are withdrawn. They combine dataset sources or pair model and data from different papers. Their source bytes may be public, but they are not current PI-Guard evidence. The withdrawn folders and snapshots have been purged from disk; see the [withdrawal register](../../../reports/tasks_for_meeting_6/WITHDRAWN_DATA_ARTIFACTS.md) and [model-paper alignment audit](../../../reports/experiment_reports/MODEL_PAPER_CODE_ALIGNMENT_AUDIT_2026-10-02.md).

No merged PI-Guard training corpus, three-class model, or two-tier cascade is certified by these files. Published paper results are literature claims and must retain their citations and labels.
