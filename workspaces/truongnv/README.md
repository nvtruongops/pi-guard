# Nguyễn Văn Trường — PI-Guard workspace

This is the lead workspace for current research coordination, architecture notes, replications, and reports. It is separate from the shared official deliverables under Final-Report.

## Current status — 4 October 2026

- Review 2 umbrella task: open; see [task and handoff](reports/tasks_for_review2/README.md) and [TASK.md](reports/tasks_for_review2/TASK.md).
- Seed-42 TF-IDF → DeBERTa cascade experiment: completed for one pinned PIDS-Bench split; see [report](reports/experiment_reports/tfidf_deberta_cascade_2026-10-04/REPORT.md) and [progress log](reports/experiment_reports/tfidf_deberta_cascade_2026-10-04/TASK_PROGRESS.md).
- The ingress architecture is still a proposal. L2 emits per-chunk route candidates, L3 receives REVIEW chunks, and API aggregation alone decides final request ALLOW/BLOCK.
- No reported one-seed result establishes project-wide thresholds, target FPR, service P95, or final model acceptance.

## Navigation

- [Reports: active task and historical references](reports/README.md)
- [Research and evidence notes](docs/research/README.md)
- [Architecture and threat model](docs/architecture/README.md)
- [Thesis drafts](docs/thesis/README.md)
- [Paper-matched replications and local experiment index](replications/README.md)
- [Source tree status](src/README.md)
- [Test tree status](tests/README.md)
- [References index](References/README.md)
- [Meeting and progress materials](Meeting/README.md)

## Version references

Python package metadata is 0.1.0. The last recorded workspace snapshot in VERSION.md is v2.2-baseline-freezing-meeting6 dated 24 September 2026. This README describes active Review 2 progress as of 4 October 2026; it does not create a new release version.
