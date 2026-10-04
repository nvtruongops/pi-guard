# Earlier rationale for combining lexical and contextual models

This page replaces the earlier Review 1 rationale draft as a current project-status guide. Older versions contained unsupported local performance claims and should not be used as evidence.

The project proposes a lexical L2 scorer and a DeBERTa L3 reviewer to study complementary signals. That design remains a proposal. It is not established as the unique or optimal architecture. The current flow and candidate/decision boundaries are described in [Proposed ingress architecture](../models/ingress_architecture.md).

## Evidence available as of 4 October 2026

One seed-42 cascade experiment was completed on a pinned PIDS-Bench split. On held-out slices, it recorded attack F1 98.89% on IID test (n=3,918), hard-benign FPR 43.94% (n=808), structural-OOD benign FPR 79.68% (796/999), and model-only P95 155.03 ms on the measured RTX 3060 laptop workload. This is one run; false-positive rates remain high, and timing is not end-to-end service latency.

Review 2’s umbrella task remains open. The validation-selected gates from this run are not project-wide or service cutoffs. Read the [full experiment report](https://github.com/nvtruongops/pi-guard/blob/main/workspaces/truongnv/reports/experiment_reports/tfidf_deberta_cascade_2026-10-04/REPORT.md) for methods, provenance, and additional slices.
