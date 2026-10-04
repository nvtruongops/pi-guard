# Model trade-offs and current local evidence

## Design question

The project proposes combining a fast lexical scorer with a contextual transformer so that uncertain chunks can receive deeper review. This is a research question to evaluate, not proof that a cascade is always better or that the proposed service meets its targets.

See [the current ingress proposal](ingress_architecture.md) for the L1/L2/L3/API flow. L2 ALLOW and BLOCK are chunk-level candidates. REVIEW is routed to L3. Only API aggregation makes the final request-level ALLOW or BLOCK decision.

## One-run Review 2 evidence

A seed-42 experiment on one pinned PIDS-Bench split recorded:

| Held-out slice | Cascade result |
|---|---:|
| IID attack test, n=3,918 | Attack F1 98.89% |
| Hard-benign, n=808 | FPR 43.94% |
| Obfuscated attacks, n=405 | Recall 98.27% |
| Domain-OOD attacks, n=2,000 | Attack F1 97.54% |
| Structural-OOD benign, n=999 | FPR 79.68% (796/999) |
| Model inference, 200 balanced prompts | P95 155.03 ms |

The hard-benign and structural-OOD false-positive rates are high. The timing is model inference on the measured RTX 3060 laptop workload, not end-to-end service latency. The experiment uses one seed and one split; these results do not establish final project KPI acceptance or service policy.

The full source-of-truth report is [the seed-42 cascade experiment](https://github.com/nvtruongops/pi-guard/blob/main/workspaces/truongnv/reports/experiment_reports/tfidf_deberta_cascade_2026-10-04/REPORT.md). Its validation-selected gates are specific to that run. The symbolic tau_allow and tau_block in the architecture proposal are not established service cutoffs.
