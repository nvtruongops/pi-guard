# Restarted DeBERTa seed-42 run

- Upstream repository commit: `87dc835566b930ee921240874a4939b2c266c2fe`.
- Upstream training source blob: `1918aee0fafd9a7700d73aa6a6c4305820403b63`.
- Public initial checkpoint: `microsoft/deberta-v3-base`, revision `8ccc9b6f36199bec6961081d44eb72fb3f7353f3`; see `../PIDS_Bench_model_input_manifest_2026-10-03.json` for the SHA-256 manifest.
- Dataset SHA-256 checks are enforced by `run_pinned_deberta.py` before staging. The hard-benign split drops only 664 blank/redacted rows (1,472 -> 808).
- Training: original PIDS-Bench function, seed 42, 3 epochs, lr 2e-5, max length 512, FP32, microbatch 2 x gradient accumulation 8 (effective batch 16); dynamic padding execution adaptation.
- HF hub is offline and the local `main` ref resolves to the pinned checkpoint revision.

The exact launch invocation and environment are recorded in `COMMANDS.md`; the generated `run_config.json` is authoritative for runtime/data settings. Training has started from scratch in this run directory; the earlier paused attempt is preserved separately and is not treated as a result.
