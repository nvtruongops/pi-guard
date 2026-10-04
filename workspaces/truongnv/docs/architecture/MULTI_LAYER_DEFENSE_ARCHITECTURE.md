# Multi-layer defense architecture — evidence status

## Scope Boundary Declaration

- **IN-SCOPE:** design concepts for layered defense and their current measurement limits.
- **OUT-OF-SCOPE:** claim a measured TF-IDF/DeBERTa cascade from independent or cross-paper runs.

The current proposal is specified in the [Review 1 lần 2 architecture dossier](../../reports/report%20for%20review%201%20lan%202/README.md) and its [task boundary](../../reports/report%20for%20review%201%20lan%202/TASK.md): L1 extracts/normalizes/chunks input; L2 applies TF-IDF + Logistic Regression per chunk and emits route candidates; L3 is the proposed DeBERTa classifier for routed chunks/windows; the API checks coverage, aggregates request-level results, then chooses ALLOW / REVIEW / BLOCK. In older notes, “two-tier” refers only to the two ML scoring models at L2 and L3. L1 preprocessing and API orchestration are not extra classifier tiers.

This remains a design proposal, not implementation or evaluation evidence. The PIDS-Bench TF-IDF run and PIGuard-only source run are independent experiments with separate papers and protocols. The old Review 2/Tier 1 fits and ProtectAI-on-other-paper outputs are withdrawn. No local result demonstrates conditional routing, recovery of first-stage misses, or end-to-end performance. See the [provenance audit](../../reports/experiment_reports/WORKSPACE_PROVENANCE_AUDIT_2026-09-30.md).
