# Training status — PIDS-Bench DeBERTa-v3-FT

**Status: paused by user.** The run stopped after 532/5,082 optimizer steps (10.47%) to release GPU resources. No checkpoint or metric was saved, and this partial run is not a DeBERTa result.

- Source: author repository, commit `87dc835566b930ee921240874a4939b2c266c2fe`.
- Seed 42; 3 epochs; LR `2e-5`; FP32; max length 512; microbatch 2 × accumulation 8 (effective batch 16).
- Same frozen train/validation/test and evaluation data. Only blank, license-redacted hard-benign text is omitted (664/1,472); local hard-benign `n=808`.
- Runtime adaptation: dynamic padding avoids computing trailing pad tokens. No labels, examples, truncation limit, model, loss, or optimizer settings changed.
- Fixed-padding attempt: stopped after 31/5,082 updates due measured runtime; it produced no checkpoint and is not evidence.

See `training.log`, `run_config.json`, and `workdir/data/pids_bench_v3` for run evidence.
