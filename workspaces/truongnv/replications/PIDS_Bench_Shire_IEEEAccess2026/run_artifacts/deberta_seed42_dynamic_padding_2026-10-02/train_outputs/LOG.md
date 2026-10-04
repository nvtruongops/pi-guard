# Run log

- Data freeze hashes checked against `FREEZE_MANIFEST.txt`; all eight training/evaluation CSV hashes matched before staging.
- Initial DeBERTa startup stopped before training because `protobuf` was missing. Installed the repository-declared dependency and retained the failed log in `../deberta_seed42_repo_2026-10-02/training.log`.
- Fixed-padding trial started on the original script, then was stopped at 31/5,082 updates after the observed ETA exceeded 15 hours. It saved no checkpoint and is not reported as a model result.
- Dynamic-padding run used the same pinned training function and was paused at 532/5,082 updates after the user asked to release GPU resources. It exited with code 2 after interruption. No checkpoint or metric was saved; the partial run is not a result. See `status.json` and `training.log`.
- TF-IDF source run initially reached model save but hit Windows CP-1252 output encoding; rerun with `PYTHONIOENCODING=utf-8` exited 0 and wrote the complete report.
