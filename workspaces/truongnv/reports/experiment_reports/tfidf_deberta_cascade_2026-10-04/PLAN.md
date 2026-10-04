# TF-IDF → DeBERTa cascade experiment plan

**Goal:** Produce a provenance-checked, same-split seed-42 comparison of TF-IDF + LR, DeBERTa-v3, and a local TF-IDF-first confidence-gated cascade using pinned PIDS-Bench assets.

**Architecture evaluated:** TF-IDF + LR directly decides scores outside two validation-selected confidence gates. Prompts between the gates are sent to DeBERTa-v3. The selected policy is frozen before held-out scoring.

**Task:** [`TASK.md`](TASK.md)  
**Results:** [`REPORT.md`](REPORT.md)

## Constraints followed

- [x] PIDS-Bench author commit `87dc835566b930ee921240874a4939b2c266c2fe`; source CSV hashes verified.
- [x] Seed 42, three epochs, FP32, max length 512, effective batch 16, pinned open DeBERTa base revision.
- [x] Dynamic padding retained as a disclosed runtime adaptation; source text and labels unchanged.
- [x] Thresholds/gates selected on validation only; held-out test/OOD labels used for reporting.
- [x] Work and new artifacts confined to `workspaces/truongnv/`; no pre-existing files or withdrawn Meeting 6 outputs changed.

## Tasks

### Task 1 — Author-source DeBERTa run

- [x] Verify original durable checkpoint, frozen split, source commit, and local model cache.
- [x] Resume from step 3,388 and complete training at step 5,082.
- [x] Complete author-code validation, test, hard-benign, obfuscation, OOD, and subtype evaluation.
- [x] Verify final model files and `run_config.json` status `completed`.

The first wrapper invocation hit a CP1252 console encoding error after model/checkpoint save. Recovery resumed the author wrapper from step 5,082 with UTF-8 output and completed evaluation without repeating training.

### Task 2 — Standalone models on identical frozen splits

- [x] Verify source data and model-input hashes before scoring.
- [x] Use the author-source TF-IDF + LR seed-42 fit and the locally fine-tuned author-source DeBERTa checkpoint.
- [x] Generate validation/held-out predictions and record fixed-0.5 plus validation-FPR-budget metrics.

### Task 3 — Cascade policy

- [x] Search validation-only TF-IDF gates and DeBERTa fallback threshold under validation benign FPR ≤ 1.5%.
- [x] Freeze thresholds before scoring held-out axes.
- [x] Record confusion counts, call rates, inference timing, and raw prediction rows.

### Task 4 — Report and verification

- [x] Write the scope-bounded report with provenance, results, and limitations.
- [x] Generate `comparison_matrix.csv` and `comparison_matrix.png`.
- [x] Recompute matrix counts and confusion metrics from prediction rows; confirm checkpoint, model, and dataset hashes.
- [x] State the supported conclusion accurately: call reduction at matched DeBERTa metrics on some axes, with no overall quality or robustness improvement established.
