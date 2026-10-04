# Run log summary

- Initial resumed training: step 3,388 → 5,082, seed 42, CUDA, FP32, three epochs, max length 512, effective batch 16, dynamic padding.
- Author training-time final validation: accuracy 0.9922286, precision 0.9893152, recall 0.9956012, F1 0.9924482, loss 0.0453902.
- The first wrapper invocation saved `deberta_v3/model/` and `checkpoint-5082`, then hit a CP1252 `UnicodeEncodeError` while printing its completion arrow. This was a console encoding issue after training, not a model/checkpoint write failure.
- Recovery resumed from `deberta_v3/trainer/checkpoint-5082` with UTF-8 output and a new stage directory. No optimizer steps were repeated. The full author evaluation completed and the run configuration now says `completed`.
- Author summary: test F1 0.9891 at threshold 0.5; test F1 0.9889 at validation-tuned threshold 0.866; hard-benign FPR 0.436881 on 808 retained rows; obfuscated recall 0.982716; domain-OOD F1 0.9754; structural-OOD FPR 0.7868.
- Cascade evaluation completed on CUDA. Its thresholds were selected using `val.csv`; the selected validation benign FPR is 0.008749 and DeBERTa call rate 0.433191.
- Matrix, row predictions, thresholds, latency, and hashes are under `../outputs/seed42/`. Verification recomputed all 25 metric rows' confusion counts, the five prediction-axis counts, model/data hashes, and cascade call rates.
- See [`REPORT.md`](../REPORT.md) for the held-out interpretation and limitations. Full unbuffered run output: [`training.log`](../../../../replications/PIDS_Bench_Shire_IEEEAccess2026/run_artifacts/deberta_seed42_resume_cascade_2026-10-04/training.log).
