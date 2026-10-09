# Earlier two-scoring-stage overview — historical context

This page preserves an earlier conceptual overview. It is superseded as the current project status by [the proposed ingress architecture](ingress_architecture.md).

The current proposal has L1 input handling, L2 per-chunk TF-IDF + Logistic Regression route candidates, L3 DeBERTa scoring for REVIEW chunks, and API-level request aggregation. Only the API emits final request ALLOW or BLOCK.

Thresholds shown in older architecture sketches are not established service settings. The current seed-42 experiment selected validation gates for one run; its report is separate from this background page. Use the active task and provenance-backed report in the repository for current results.