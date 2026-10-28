# L2-only research progress — round09

## Scope boundary declaration

This continuation uses the frozen English round07 native-reference train/validation package only. Labels remain documented source-native mappings, not curator-reviewed gold. It changes no historical dataset or baseline helper. It uses five-fold source-family OOF for train diagnostics; validation is used only for the one preselected C=4 confirmation. No test row, ID, text, or payload was opened. No L3 or cascade was run. No smoke task or shortened fit was created or run. Nothing was committed or published.

The package is `pi_guard_l2_native_reference_round07_r01`, manifest SHA-256 `a62f09c0af686b3ad98b99dbb4dd839c32cd6b7e7513409405e29ba056a90650`.

## Results

The current comparator is the round07 JB-moderated weighting with the baseline `C=2.0`. All new OOF runs use the same five family folds and package manifest.

| Variant | OOF macro-F1 | OOF benign FPR | OOF JB precision / recall / F1 | Validation macro-F1 | Validation benign FPR | Validation JB precision / recall / F1 | Decision |
|---|---:|---:|---:|---:|---:|---:|---|
| Fixed balanced baseline, C=2 | 0.82254 | 11.75% | 0.4882 / 0.7738 / 0.5987 | 0.68218 | 26.15% | 0.1369 / 0.6444 / 0.2258 | Reference |
| JB-moderated class weights, C=2 | **0.82879** | 11.15% | **0.5253 / 0.7387 / 0.6140** | **0.68687** | **24.81%** | **0.1424 / 0.6111 / 0.2310** | Retained research candidate |
| Same weights, C=1 | 0.82146 | 10.37% | 0.4929 / 0.7455 / 0.5934 | Not run | Not run | Not run | Rejected: lower macro-F1 and JB F1 |
| Same weights, C=4 | 0.82929 | 11.53% | 0.5359 / 0.7353 / 0.6199 | 0.68439 | 25.31% | 0.1413 / 0.5861 / 0.2277 | Rejected: OOF gain did not carry to validation |
| C=2 with equal source-family mass within each label | 0.81355 | **9.97%** | 0.5161 / 0.6900 / 0.5905 | Not run | Not run | Not run | Rejected: lower macro-F1 and JB F1 |

The C=4 OOF gain over C=2 was marginal: +0.00050 macro-F1 and +0.00592 JB F1, while benign FPR increased 0.38 percentage points. Its complete train/validation fit then lost 0.00248 macro-F1, increased benign FPR by 0.51 points, and lowered JB F1 by 0.00326 versus C=2. Batch-one validation P95 was 6.95 ms, but that local measurement does not establish API latency or an L2 acceptance result.

The class-preserving family weighting lowered pooled OOF benign FPR by 1.18 points, but reduced macro-F1 by 0.01524, JB F1 by 0.02350, and JB recall by 0.04864. The earlier equal-total-family run on round06/r03 also performed poorly (OOF macro-F1 0.30641), but that four-family package included sources now excluded from round07. It is historical context only; the round09 family×class run is the current-package comparison.

OOF integrity checks passed for all four candidate reports: each covers 115,953 unique train rows exactly once, all share the frozen package hash, fold plans match, and run/prediction hashes validate. The family×class run's per-fold checks confirmed family mass is equal within each class while class mass is preserved. Test-opened and L3-run flags remain false.

## Readiness decision

The C=2 JB-moderated variant remains the best current research candidate among the tested round07 configurations. L2 remains **NOT_READY**, not PASS. The C=4 run selected no operating pair; the earlier expanded cutoff sweep remains post-hoc. The official acceptance declaration still says `GATE_UNSPECIFIED`, and owner-level rights/lineage/privacy review is incomplete. Research thresholds cannot substitute for an owner-approved rubric, and this report does not promote them to acceptance criteria.

Next L2 work should focus on feature/source-family generalization under the same frozen train OOF design. Any new candidate remains diagnostic until the official owner gate and required rights/lineage/privacy review are recorded. The scope still ends at L2; no L3 work is needed for this task.

## Reproducibility

- [Round07 readiness and baseline evidence](file:///D:/Work/Do-an/Final-Report/reports/experiment_reports/l2_autonomous_research_20261013/l2_readiness_followup_round07.md)
- [C=1 full five-fold family OOF](file:///D:/Work/Do-an/Final-Report/reports/experiment_reports/l2_autonomous_research_20261013/l2_jb_moderated_c1_family_oof_round08_r01.json)
- [C=4 full five-fold family OOF](file:///D:/Work/Do-an/Final-Report/reports/experiment_reports/l2_autonomous_research_20261013/l2_jb_moderated_c4_family_oof_round08_r01.json)
- [C=4 full train/validation fit summary](file:///D:/Work/Do-an/Final-Report/reports/experiment_reports/l2_autonomous_research_20261013/l2_jb_moderated_c4_validation_round08_r01.json)
- [Class-preserving family-weight OOF](file:///D:/Work/Do-an/Final-Report/reports/experiment_reports/l2_autonomous_research_20261013/l2_class_family_balanced_oof_round09_r01.json)
- [Owner gate declaration](file:///D:/Work/Do-an/Final-Report/reports/experiment_reports/l2_v9_health_check_20261013/OWNER_GATE_DECLARATION.json)
