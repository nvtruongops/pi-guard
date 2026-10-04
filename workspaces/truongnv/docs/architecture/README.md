# PI-Guard threat model and proposed architecture

This folder contains a qualitative threat model and architecture proposals. These documents do not establish that the proposed service has been implemented or accepted.

## Current ingress proposal

See the [Review 1 architecture index](../../reports/report%20for%20review%201%20lan%202/README.md) and [Draw.io source](../../reports/report%20for%20review%201%20lan%202/REVIEW1_PROPOSED_INGRESS_ML_ARCHITECTURE.drawio). The proposal separates L1 input handling, L2 per-chunk TF-IDF + Logistic Regression scoring, L3 DeBERTa scoring for REVIEW chunks, and API coverage/aggregation/policy.

L2 ALLOW and BLOCK are per-chunk candidates. The API alone emits final request ALLOW or BLOCK after joining results and checking coverage. The symbolic tau_allow and tau_block parameters are assumptions, not established project or service cutoffs. The separate seed-42 experiment’s validation-selected gates apply only to that run.

## Architecture references

- [Threat model and attack surface](THREAT_MODEL_AND_ATTACK_SURFACE.md)
- [Multi-layer defense proposal](MULTI_LAYER_DEFENSE_ARCHITECTURE.md)
- [Comparative matrix and tradeoffs](COMPARATIVE_MATRIX_AND_TRADEOFFS.md)
- [Current scope and deprecation rules](../../../../.agents/rules/rule-02-task-scope-and-milestone-enclosure.md)
- [Current experiment report](../../reports/experiment_reports/tfidf_deberta_cascade_2026-10-04/REPORT.md)
