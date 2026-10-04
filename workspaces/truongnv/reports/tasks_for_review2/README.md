# Review 2 — task and handoff

## Scope Boundary Declaration

- IN-SCOPE: develop the proposed ingress model study and a demo with real inference; keep logs, raw outputs, and provenance; report failures and limits.
- OUT-OF-SCOPE: claiming final KPI acceptance, using mock predictions, mixing checkpoints and datasets across papers, changing the immutable project register, or implementing a production API. INT8, ONNX, and ZeroQuant remain out of scope under Rule 02.

The authoritative task boundary and open checklist are in [TASK.md](TASK.md).

## Progress

The umbrella Review 2 task is still open. A separate experiment has completed seed-42 TF-IDF → DeBERTa fine-tuning/evaluation on one pinned PIDS-Bench split. Its [task](../experiment_reports/tfidf_deberta_cascade_2026-10-04/TASK.md), [progress log](../experiment_reports/tfidf_deberta_cascade_2026-10-04/TASK_PROGRESS.md), and [report](../experiment_reports/tfidf_deberta_cascade_2026-10-04/REPORT.md) record the run-specific gates, held-out results, provenance, and limitations.

The run found high false-positive rates on hard-benign and structural-OOD benign slices. Its model-only P95 timing was 155.03 ms on the measured RTX 3060 laptop workload; it does not establish service latency. Completing this experiment does not close the umbrella task or accept project targets.
