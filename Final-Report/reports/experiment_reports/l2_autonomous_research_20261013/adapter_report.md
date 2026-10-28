# Native-reference L2 adapter — verification report

## Scope Boundary Declaration

This report covers the new adapter and metadata-only candidate checks. It does not claim human-gold labels, a fitted model, validation metrics, L2 readiness, L3 training, or a final-test result. The family-level sealed test contract follows the user's approval; test payloads remain unopened.

## Interface and data contract

`fit_l2_curated.py` accepts required `--package`, `--protocol`, and `--output` paths. Its default mode performs a metadata-only preflight; `--fit` may load only train and validation after every gate passes. Outputs must be new paths outside dataset versions and history. The adapter reuses the frozen legacy model builder and evaluator.

Train and validation retain row-level split metadata and hashed row/provenance references, with row IDs and all grouping keys checked across those partitions. Test uses only `split.partitions.test` with schema `pi_guard_sealed_test_families_v1`; each family contains source repository, revision, family ID, collection lineage ID, and aggregate benign/PI/JB support. The manifest test partition is exactly `{"sealed_contract":"split.partitions.test"}`. Test row IDs, text, provenance, payload path, and payload hash are rejected. Test family IDs and collection lineages must be disjoint from train and validation.

## Fresh verification

Command: `uv run --no-project python -B -X utf8 Final-Report/reports/experiment_reports/l2_autonomous_research_20261013/check_adapter.py`.

Result: `PASS_NEGATIVE_GATE_AND_FIXED_CONFIG_CHECKS`. Eight V9–V12 invocations (metadata-only and `--fit`) returned `BLOCKED` before fitting or row access; outputs were not created. The check asserts `fit_started=false`, no row payload opened, `test_opened=false`, and `l3_run=false` for every command.

Metadata-only assertions cover a valid family contract, rejection of row-level test fields, family/lineage overlap, missing JB support, and malformed access/partition containers. The fixed Logistic Regression configuration is C=2, balanced class weights, 1,000 iterations, lbfgs and seed 42; word/character vectorizers remain unfitted. `fit_l2_curated.py` SHA-256 is `a41cb3f9e0d0c07d076dd7d8fbb50d4d626a57bd1e307cd20666d33a42017dba`; protocol SHA-256 is `66bf12d217d87a57341a149d7de5fb4c571155a9f1ae1c387caf648fb2796e0f`. Full command outputs are in [adapter_gate_check_20261012T232227Z.json](adapter_runs/adapter_gate_check_20261012T232227Z.json).

## Continuation addendum — 2026-10-13

The earlier “no positive fit path” statement above describes the round03 state and is superseded by the user-authorized round06 continuation. Package r03 passed adapter preflight and the fixed baseline fit completed; it returned `NOT_READY` with no selected pair. Four-family train OOF and one separate equal-family-weight treatment are recorded in [l2_l3_readiness_report_round07.md](l2_l3_readiness_report_round07.md). The test contract remains metadata-only and unopened. The adapter does not claim L2 readiness or handoff to L3; L3 training is blocked because validation selected no L2 route pair.
