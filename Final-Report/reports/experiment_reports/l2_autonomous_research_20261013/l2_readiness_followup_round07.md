# L2-only readiness follow-up — round07 weighting experiments

## Scope boundary

This report covers English L2 data, training, validation, and train-only source-family OOF. It does not train or run L3 or the cascade. The round07 final-test contract remains metadata-only; no test rows, IDs, text, or payload were opened. No smoke task or shortened fit was created or run.

Labels are documented native-reference mappings, not curator-reviewed human gold. The frozen private package is `pi_guard_l2_native_reference_round07_r01`, version `0.7.0-native-reference-l2-candidate`, with manifest SHA-256 `a62f09c0af686b3ad98b99dbb4dd839c32cd6b7e7513409405e29ba056a90650`. It has 115,953 train rows (benign 4,494; PI 110,575; JB 884) and 40,885 validation rows (benign 7,309; PI 33,216; JB 360). The package and its private run artifacts are not redistribution outputs.

## Experiment results

| L2 treatment | Validation macro-F1 | Validation benign FPR | Validation JB P / R / F1 | Batch-1 P95 | Train family OOF macro-F1 | OOF benign FPR | OOF JB P / R / F1 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Fixed `balanced` baseline | 0.68218 | 26.15% | 0.1369 / 0.6444 / 0.2258 | 21.94 ms | 0.82254 | 11.75% | 0.4882 / 0.7738 / 0.5987 |
| Square-root of all balanced weights, normalized to mean 1 | 0.67974 | 29.68% | 0.1513 / 0.6167 / 0.2430 | — | Not run: validation regressed | — | — |
| `balanced`, with only JB moderated to the geometric midpoint with benign; fold-local weights normalized to mean 1 | **0.68687** | **24.81%** | **0.1424 / 0.6111 / 0.2310** | **11.59 ms** | **0.82879** | **11.15%** | **0.5253 / 0.7387 / 0.6140** |

The square-root variant is rejected: validation macro-F1 and benign FPR regressed, despite a small increase in JB precision. The targeted JB variant is the current research candidate: validation macro-F1 increased by 0.00468 and benign FPR fell by 1.34 percentage points; its complete five-fold source-family OOF macro-F1 increased by 0.00625, benign FPR fell by 0.60 points, and JB F1 increased by 0.01532. JB recall fell by 0.03507 in OOF, so the gain is a precision/recall trade-off rather than an across-the-board improvement.

OOF fold macro-F1 ranged from 0.74893 to 0.81807; benign FPR ranged from 5.13% to 37.88%. This variance remains a material source-family generalization limitation. The original predeclared 7x7 cutoff grid, capped at 0.99, selected no operating pair. A supplemental, explicitly post-hoc 13x13 validation-score diagnostic found a lowest-review pair at `tau_allow=0.999`, `tau_block=0.995`: validation REVIEW 30.42%, PI early-ALLOW 0%, JB early-ALLOW 1.11%, benign early-BLOCK 1.05%, with REVIEW support of 6,654 benign / 5,470 PI / 314 JB.

That pair was then locked and applied without retuning to a separate full five-fold family-held-out OOF probability run. Pooled train OOF produced REVIEW 19.96%, PI early-ALLOW 2/110,575 (0.0018%), JB early-ALLOW 0/884, and benign early-BLOCK 24/4,494 (0.53%); each class had more than 20 OOF REVIEW rows. Fold 4 benign early-BLOCK was 4.44%, so pooled compliance does not erase family-level instability. These are diagnostic calculations under the research protocol's unapproved limits, not official acceptance evidence.

## Readiness decision

The candidate improves the matched round07 baseline on aggregate validation and pooled source-family OOF, and the fixed threshold pair met the recorded research limits on both validation and pooled family OOF. It is **not an L2 PASS**: the threshold expansion was post-hoc, one OOF family fold exceeded the exploratory benign early-BLOCK limit, the official owner declaration still has no acceptance limits (`GATE_UNSPECIFIED`), and owner-level rights/lineage/privacy and prior-use review remains incomplete. The project API FPR objective is not automatically an L2 early-BLOCK limit and is not claimed as achieved here.

No test or L3 evidence is needed for this L2-only experiment. This closes the current round07 experiment cycle with the JB-moderated candidate retained for research and the official L2 result still NOT_READY. Any later training change should use a new uniquely named run and compare against this frozen candidate and its complete OOF evidence.

## Reproducibility evidence

- [Frozen round07 package build record](file:///D:/Work/Do-an/Final-Report/reports/experiment_reports/l2_autonomous_research_20261013/l2_candidate_build_round07_r01.json)
- [Round07 fixed-baseline validation metrics](file:///D:/Work/Do-an/workspaces/truongnv/pi_guard_pipeline/training_bases/pi_guard_tfidf_tier1/runs/l2_round07_r01_full_20261013/metrics.json)
- [Round07 fixed-baseline five-fold family OOF](file:///D:/Work/Do-an/Final-Report/reports/experiment_reports/l2_autonomous_research_20261013/l2_family_oof_round07_r01.json)
- [Square-root weighting validation report](file:///D:/Work/Do-an/Final-Report/reports/experiment_reports/l2_autonomous_research_20261013/l2_sqrt_class_weight_validation_round07_r01.json)
- [JB-moderated weighting validation report](file:///D:/Work/Do-an/Final-Report/reports/experiment_reports/l2_autonomous_research_20261013/l2_jb_moderated_weight_validation_round07_r01.json)
- [JB-moderated weighting five-fold family OOF report](file:///D:/Work/Do-an/Final-Report/reports/experiment_reports/l2_autonomous_research_20261013/l2_jb_moderated_family_oof_round07_r01.json)
- [Post-hoc supplemental threshold-grid report](file:///D:/Work/Do-an/Final-Report/reports/experiment_reports/l2_autonomous_research_20261013/l2_supplemental_threshold_grid_round07_r01.json)
- [Locked-pair five-fold OOF probability report](file:///D:/Work/Do-an/Final-Report/reports/experiment_reports/l2_autonomous_research_20261013/l2_jb_moderated_probability_oof_round07_r01.json)
- [Owner gate declaration](file:///D:/Work/Do-an/Final-Report/reports/experiment_reports/l2_v9_health_check_20261013/OWNER_GATE_DECLARATION.json)
