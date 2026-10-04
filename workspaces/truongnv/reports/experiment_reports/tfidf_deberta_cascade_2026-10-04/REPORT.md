# TF-IDF → DeBERTa: local cascade experiment

## Scope Boundary Declaration

This report records one local seed-42 experiment that implements a confidence-gated TF-IDF + Logistic Regression → DeBERTa-v3 cascade. The cascade is a project proposal developed here; it is not attributed to PIDS-Bench or to another paper. This work uses the PIDS-Bench authors' code and pinned data to compare the proposal with its two standalone components. It does not compare these results numerically with results from other papers. The withdrawn Meeting 6 D1–D6 matrix remains outside scope.

## Question and result

Does routing confident cases through TF-IDF and sending uncertain cases to DeBERTa improve the trade-off among detection, benign false positives, and transformer calls on a common held-out split?

On this one seed and split, the cascade matched the standalone DeBERTa metrics on IID test, obfuscated attacks, and domain OOD while reducing DeBERTa calls. It did not improve robustness on the hard-benign or structural-OOD sets: its hard-benign FPR was slightly higher than DeBERTa's, and its structural-OOD FPR was also higher. The result supports the cascade as a candidate for reducing transformer load on these measured distributions. It does not show that the cascade is a higher-quality detector overall.

## Scope and provenance

- **Author source:** PIDS-Bench v3 at upstream commit `87dc835566b930ee921240874a4939b2c266c2fe`; the model and data input manifest is pinned in `outputs/seed42/evaluation_provenance.json`.
- **TF-IDF + LR:** seed-42 model fitted by the PIDS-Bench author baseline code on its pinned training split. This is a locally fitted sklearn baseline, not a downloaded TF-IDF checkpoint.
- **DeBERTa-v3:** locally fine-tuned using the PIDS-Bench author training/evaluation code, seed 42, three epochs, FP32, max length 512, microbatch 2, accumulation 8 (effective batch 16), and dynamic padding. Training completed at step 5,082. The public base is `microsoft/deberta-v3-base`, pinned to revision `8ccc9b6f36199bec6961081d44eb72fb3f7353f3`, license MIT.
- **Resume and logging:** training resumed from the durable step-3,388 checkpoint. The first post-training wrapper invocation saved the model/checkpoint and then stopped on a Windows CP1252 encoding error while printing an arrow character. The same author wrapper resumed from the completed step-5,082 checkpoint with UTF-8 output; it performed evaluation and finalized the run without repeating training steps. The final run status is `completed`.
- **Data:** train, validation, test, and evaluation-source CSV checksums are recorded and verified. The hard-benign file contains 1,472 source rows; 664 blank/license-redacted rows cannot be scored, so the measured denominator is 808 retained rows.
- **No paper claim:** the router gates and its validation search were implemented for this project. No paper is claimed to have proposed this exact cascade.

## Evaluation protocol

The evaluator scores TF-IDF + LR, the local DeBERTa fine-tune, and the cascade against the same rows. Standalone operating thresholds and the cascade's gates were chosen on validation only. The validation constraint was benign FPR ≤ 1.5%; held-out labels were used only to calculate the reported metrics.

For the cascade, TF-IDF scores at or below `0.0494935` receive a direct benign decision; scores at or above `0.9174386` receive a direct attack decision; intermediate scores go to DeBERTa, whose fallback threshold is `0.8660782`. The finite validation search uses 31 quantile candidates for each TF-IDF gate and 201 for the DeBERTa threshold. It maximizes validation attack recall subject to the FPR constraint, then prefers higher macro-F1 and fewer DeBERTa calls. This is a disclosed grid search, not a global optimum guarantee.

All held-out methods below use their validation-selected threshold. The heatmap shows a different metric on each axis, so read the axis labels with the cells. Raw counts, precision/recall, confusion matrices, and fixed-0.5 results are in `outputs/seed42/metrics_long.csv` and the row-level prediction files.

## Held-out comparison

| Method | IID test attack F1 (n=3,918) | Hard-benign FPR (n=808) | Obfuscated attack recall (n=405) | Domain-OOD attack F1 (n=2,000) | Structural-OOD FPR (n=1,998) |
|---|---:|---:|---:|---:|---:|
| TF-IDF + LR | 95.86% | **15.22%** | 79.75% | 91.80% | **64.66%** |
| DeBERTa-v3 fine-tuned | 98.89% | 43.56% | 98.27% | 97.54% | 78.58% |
| TF-IDF → DeBERTa cascade | 98.89% | 43.94% | 98.27% | 97.54% | 79.68% |

**DeBERTa call rate for the cascade:** IID test 42.01%, hard-benign 96.78%, obfuscated attacks 45.43%, domain OOD 78.25%, structural OOD 78.93%. Standalone TF-IDF makes no DeBERTa calls; standalone DeBERTa calls it for every row.

The cascade's IID confusion counts equal standalone DeBERTa's on this split: 1,826 TN, 22 FP, 24 FN, 2,046 TP. It handled the same number of obfuscated attacks and reached the same domain-OOD confusion counts while calling DeBERTa for fewer rows. On hard-benign it flagged 355/808 rows, versus 352/808 for DeBERTa and 123/808 for TF-IDF. On structural OOD it flagged 796/999 benign rows, versus 785/999 for DeBERTa and 646/999 for TF-IDF. The cascade routing therefore saves calls on several axes but does not solve the shifted-benign false-positive problem.

## Local inference timing

| Method | p50 (ms) | p95 (ms) | p99 (ms) | Mean (ms) |
|---|---:|---:|---:|---:|
| TF-IDF + LR | 1.62 | 3.01 | 3.66 | 1.80 |
| DeBERTa-v3 fine-tuned | 109.76 | 169.51 | 241.99 | 116.89 |
| TF-IDF → DeBERTa cascade | 3.18 | 155.03 | 184.87 | 50.37 |

Timing used 200 deterministic, class-balanced IID-test prompts on the RTX 3060 Laptop, with 10 warmups per method. It measures local model inference only; it excludes HTTP, serialization, queueing, and any downstream model. This sample does not establish the project's service P95 target.

## Interpretation

The experiment gives a concrete, limited rationale for continuing the two-stage proposal: on IID test it retained DeBERTa's measured attack F1 and FPR while sending 57.99% fewer prompts to DeBERTa. It also matched DeBERTa's obfuscated-attack recall and domain-OOD F1 at lower call rates on those axes.

The experiment does **not** justify saying the cascade has better detection quality overall. It was slightly worse than DeBERTa on hard-benign FPR (43.94% vs. 43.56%) and structural-OOD FPR (79.68% vs. 78.58%). The standalone TF-IDF model had lower FPR on both benign stress sets, while also having lower attack detection on IID and obfuscated attacks. These large axis differences show that the current router needs another validation-led design iteration before a broader quality claim.

This is one seed on one pinned dataset split. It does not measure variation across seeds or machines, establish three-class prompt-injection/jailbreak performance, or meet a service-level claim. No number here is a cross-paper comparison.

## Artifacts

- Evaluation implementation: [`evaluate_cascade.py`](evaluate_cascade.py)
- Full raw metric rows and confusion counts: [`metrics_long.csv`](outputs/seed42/metrics_long.csv)
- Compact comparison matrix: [`comparison_matrix.csv`](outputs/seed42/comparison_matrix.csv)
- Matrix figure: [`comparison_matrix.png`](outputs/seed42/comparison_matrix.png)
- Frozen thresholds: [`thresholds.json`](outputs/seed42/thresholds.json)
- Data/model hashes and prediction sources: [`evaluation_provenance.json`](outputs/seed42/evaluation_provenance.json)
- Per-row predictions and route decisions: [`predictions/`](outputs/seed42/predictions/)
- Author-code DeBERTa outputs: [`summary.json`](../../../replications/PIDS_Bench_Shire_IEEEAccess2026/run_artifacts/deberta_seed42_resume_cascade_2026-10-04/deberta_v3/summary.json)
