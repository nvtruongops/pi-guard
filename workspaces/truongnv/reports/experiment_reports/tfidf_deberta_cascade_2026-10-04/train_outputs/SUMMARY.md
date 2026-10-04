# Training and author-code evaluation — PIDS-Bench DeBERTa-v3 seed 42

## Final status

The author-source PIDS-Bench DeBERTa-v3 run completed at global step 5,082. Training resumed from durable checkpoint 3,388 and used CUDA on the RTX 3060 Laptop. Final model files, Trainer checkpoint, author evaluation outputs, and `run_config.json` status `completed` are present in the isolated run directory.

The initial wrapper invocation saved the model and checkpoint, then hit a CP1252 console `UnicodeEncodeError` while printing an arrow character. The same wrapper was relaunched from checkpoint 5,082 with UTF-8 output, completed the author evaluation routine, and did not repeat training steps. Both the original error and the recovery are recorded in `SCIENTIFIC_CHANGELOG.md` and `LOG.md`.

## Reproducibility facts

- Upstream repository commit: `87dc835566b930ee921240874a4939b2c266c2fe`.
- Public base model: `microsoft/deberta-v3-base`, revision `8ccc9b6f36199bec6961081d44eb72fb3f7353f3`, license MIT.
- Seed 42; epochs 3; learning rate `2e-5`; FP32; maximum length 512.
- Microbatch 2 × gradient accumulation 8 = effective batch size 16.
- Dynamic padding is a runtime adaptation; input text and labels remain unchanged.
- Final run configuration: [`run_config.json`](../../../../replications/PIDS_Bench_Shire_IEEEAccess2026/run_artifacts/deberta_seed42_resume_cascade_2026-10-04/run_config.json).
- Author-code model summary: [`summary.json`](../../../../replications/PIDS_Bench_Shire_IEEEAccess2026/run_artifacts/deberta_seed42_resume_cascade_2026-10-04/deberta_v3/summary.json).
- Full run log: [`training.log`](../../../../replications/PIDS_Bench_Shire_IEEEAccess2026/run_artifacts/deberta_seed42_resume_cascade_2026-10-04/training.log).

## Author-code results

- Validation during final training: accuracy `0.99223`, precision `0.98932`, recall `0.99560`, F1 `0.99245`, loss `0.04539`.
- Author evaluation on IID test: F1 `0.9891` at fixed threshold 0.5; F1 `0.9889`, recall `0.9884`, FPR `0.0119` at its author-reported validation-tuned threshold `0.866`.
- Hard-benign retained rows: 808; tuned FPR `0.4369` (353 flagged). Source file had 1,472 rows; 664 blank/license-redacted rows were omitted from scoring.
- Obfuscated-attack recall: `0.9827` on 405 prompts.
- Domain-OOD aggregate: F1 `0.9754`, recall `0.9710`, FPR `0.0200`.
- Structural-OOD aggregate: F1 `0.7093`, recall `0.9820`, FPR `0.7868`.
- Balanced-subtype sample: F1 `0.9877`, recall `0.9881`, FPR `0.0117`.

These are results of one local seed-42 author-code run. The cascade evaluator recalculates its operating thresholds from saved validation scores and records its own results separately in `../outputs/seed42/`.
