# SOTA survey and local baseline status

## Scope boundary declaration

- **IN-SCOPE:** separate literature references, public checkpoint evaluations, classical local baselines, and the proposed two-tier architecture.
- **OUT-OF-SCOPE:** use historical Meeting 6 scores as paper results, state that six classifiers reproduce six papers, or claim the project cascade has been evaluated.

The former six-baseline tables in this dossier used incompatible model rosters and included proxy outputs. They were removed from current evidence. See the [Meeting 6 withdrawn-artifact register](../../../reports/tasks_for_meeting_6/WITHDRAWN_DATA_ARTIFACTS.md).

## Evidence currently available

| Retained local evidence | What it supports | What it does not support |
|---|---|---|
| PIDS-Bench TF-IDF + Logistic Regression | Same-paper binary baseline on the pinned PIDS-Bench test split; source rows and saved predictions were matched and metrics recomputed | Three-class PI-Guard performance, other-paper data, or a cascade |
| PIGuard checkpoint on PIGuard-released assets | PIGuard checkpoint outputs on its own release assets, with source hashes and row counts verified | PIDS-Bench results, a head-to-head ranking, or Vietnamese performance |

The former Review 1 public-vector, Review 2/Tier 1 and D1–D6 local comparisons are withdrawn under the paper-origin rule. Their report and result bundles remain listed in the [withdrawn-artifact register](../../../reports/tasks_for_meeting_6/WITHDRAWN_DATA_ARTIFACTS.md). Literature metrics must be quoted from their source papers and must not be mixed with local runs.

## Đề xuất hai bộ chấm điểm ML trong pipeline ingress

The current proposal is specified in the [Review 1 lần 2 dossier](../../../reports/report%20for%20review%201%20lan%202/README.md). Here, “two-tier” means two ML scoring models only: L2 TF-IDF + Logistic Regression, then L3 DeBERTa for chunks routed for contextual classification. L1 handles ingress extraction/normalization/chunking; the API checks coverage, aggregates chunk/window predictions, and applies request-level policy. These are not additional classifier tiers.

The arrangement remains a design hypothesis. The retained PIDS-Bench run is a paper-specific binary Logistic Regression baseline; it is not evidence for the proposed routing gate. The PI-Guard DeBERTa and complete cascade have not been trained/evaluated in this workspace.
