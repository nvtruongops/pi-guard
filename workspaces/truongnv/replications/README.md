# Replications and local experiment index

This folder contains paper-matched replication packages and source snapshots. Every result must be read with its model/data pairing, protocol, and source report. Presence of upstream code does not validate a local experiment.

## Retained paper-matched evidence

| Package | Evidence boundary |
|---|---|
| [PIDS-Bench, Shire et al.](PIDS_Bench_Shire_IEEEAccess2026/REPORT.md) | Author TF-IDF + Logistic Regression and the pinned PIDS-Bench test split; 3,918 source test rows matched. |
| [PIGuard, Hao Li et al.](02_DeBERTa_v3_Semantic_Classifier/reports/review1_paper_model_public_rerun_2026-09-30/REPORT.md) | Author checkpoint evaluated on PIGuard-released assets. |

## Current PI-Guard experiment

The [seed-42 TF-IDF → DeBERTa cascade report](../reports/experiment_reports/tfidf_deberta_cascade_2026-10-04/REPORT.md) is a separate local experiment, not a paper replication. It uses one pinned PIDS-Bench split and one seed; high hard-benign/structural-OOD false-positive rates and model-only P95 of 155.03 ms are part of the result. Its validation-selected gates are run-specific.

## Withdrawn results and source audits

Cross-paper checkpoint/data comparisons and mixed-source runs listed in the [withdrawal register](../reports/tasks_for_meeting_6/WITHDRAWN_DATA_ARTIFACTS.md) are not reportable current metrics. Some preserved files can remain on disk. See the [workspace provenance audit](../reports/experiment_reports/WORKSPACE_PROVENANCE_AUDIT_2026-09-30.md) for the recorded scope and status.
