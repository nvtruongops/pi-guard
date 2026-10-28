# L2-only research progress — round10

## Scope boundary declaration

This round continues on the frozen English round07 native-reference train/validation package. It reports a full five-fold family-held-out train OOF test of one feature change; it does not use validation for that comparison. No test row, ID, text, or payload was opened. No L3 or cascade was run. No smoke task or shortened fit was created or run. No commit or publication was made.

## New result

With C=2 and the same JB-moderated fold-local class weights, reducing char-TF-IDF `max_features` from 30,000 to 15,000 yielded OOF macro-F1 0.82219, benign FPR 11.26%, and JB precision/recall/F1 0.5027/0.7387/0.5983. Against the matched 30,000-feature candidate (0.82879 macro-F1, 11.15% benign FPR, 0.5253/0.7387/0.6140 JB P/R/F1), macro-F1 fell 0.00660, benign FPR rose 0.11 percentage points, and JB F1 fell 0.01575. The reduced feature cap is rejected; the matched C=2/30,000-feature candidate remains the strongest tested round07 variant.

The new OOF report passed integrity checks: all 115,953 train rows received one prediction, the package hash and five-fold plan match the C=2 comparator, run and prediction hashes validate, and `test_opened=false` / `l3_run=false`.

## Readiness

L2 remains **NOT_READY**, not PASS. The best candidate still has no operating pair selected under the exploratory diagnostic limits; the official owner rubric remains `GATE_UNSPECIFIED`, and the rights/lineage/privacy owner review is incomplete. The round07 supplementary threshold result remains post-hoc and is not promoted to acceptance criteria. The next step is to prepare an evidence matrix from train/validation package metadata and the existing source-review artifacts so the unresolved owner items are concrete; the owner declaration itself will remain unchanged until the owner supplies its decisions.

The task remains L2-only. No L3 run or handoff is required to complete this research scope.

## Reproducibility

- [Round09 comparison and previous full experiments](file:///D:/Work/Do-an/Final-Report/reports/experiment_reports/l2_autonomous_research_20261013/l2_readiness_followup_round09.md)
- [Round10 char-feature-cap OOF report](file:///D:/Work/Do-an/Final-Report/reports/experiment_reports/l2_autonomous_research_20261013/l2_char_feature_cap_oof_round10_r01.json)
- [Round10 full five-fold runner](file:///D:/Work/Do-an/Final-Report/reports/experiment_reports/l2_autonomous_research_20261013/run_l2_char_feature_cap_oof_round10.py)
- [Official owner gate declaration](file:///D:/Work/Do-an/Final-Report/reports/experiment_reports/l2_v9_health_check_20261013/OWNER_GATE_DECLARATION.json)
