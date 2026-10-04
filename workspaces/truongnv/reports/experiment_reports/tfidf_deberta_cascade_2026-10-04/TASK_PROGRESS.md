# Task progress — TF-IDF → DeBERTa cascade

## Scope Boundary Declaration

Source: the current user's instruction to move from literature search to building and evaluating a local TF-IDF → DeBERTa proposal. This is separate from the withdrawn Meeting 6 matrix and does not revive its artifacts.

- [x] Keep work and outputs inside `workspaces/truongnv/`.
- [x] Use the pinned PIDS-Bench author repository, matching code/data/checkpoint provenance, and the same seed-42 split for standalone and cascade comparisons.
- [x] Implement the local cascade without claiming that a paper proposed it.
- [x] Exclude cross-paper scores, three-class claims, deployment claims, and unsupported optimization methods.

## Completion record

- [x] Confirm pinned upstream commit, open base checkpoint revision/license, TF-IDF checkpoint, frozen data hashes, and the final DeBERTa checkpoint.
- [x] Finish seed-42 DeBERTa fine-tuning at global step 5,082 and complete the author evaluation routine.
- [x] Select standalone thresholds and the TF-IDF direct-decision gates/fallback threshold from validation data only, with validation benign FPR ≤ 1.5%.
- [x] Generate held-out predictions and metrics for IID test, hard-benign, obfuscated attacks, domain OOD, and structural OOD.
- [x] Generate the comparison CSV/heatmap, local inference timing, and model/data provenance.
- [x] Recompute prediction counts, confusion cells, FPR/recall, and cascade call rates from row-level prediction CSVs; verify model and data hashes.
- [x] Update `REPORT.md`, the plan, task progress, and training notes with observed results and limitations.

## Execution notes

DeBERTa resumed from durable checkpoint 3,388 and reached step 5,082. The first wrapper invocation saved the final model/checkpoint but exited while printing a Unicode arrow to a CP1252 console. The author wrapper was relaunched from checkpoint 5,082 with UTF-8 output; it completed evaluation without repeating training steps. Final `run_config.json` status is `completed`.

The final comparison supports this cascade as a local candidate for reducing DeBERTa calls on the measured IID, obfuscated, and domain-OOD rows while matching the standalone DeBERTa metrics there. Hard-benign and structural-OOD false-positive rates remain high; this run does not establish that the cascade improves detector quality overall.
