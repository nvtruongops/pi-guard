# Commands

Environment: Python 3.12.14 venv at `%TEMP%\pids-bench-deberta-20261002`; PyTorch `2.9.1+cu128`, Transformers `4.57.1`, Datasets `4.4.1`, Accelerate `1.15.0`, protobuf `7.36.2`.

Run from the workspace root (the script invokes `upstream/src/baselines/deberta_v3.py` directly):

```powershell
$run='D:\Work\Do-an\workspaces\truongnv\replications\PIDS_Bench_Shire_IEEEAccess2026\run_artifacts\deberta_seed42_dynamic_padding_2026-10-02'
$report='D:\Work\Do-an\workspaces\truongnv\reports\experiment_reports\pids_bench_two_tier_evidence_matrix_2026-10-02'
$env:HF_HOME='D:\Work\Do-an\workspaces\truongnv\replications\PIDS_Bench_Shire_IEEEAccess2026\run_artifacts\deberta_seed42_repo_2026-10-02\hf-cache'
$env:TOKENIZERS_PARALLELISM='false'
& "$env:TEMP\pids-bench-deberta-20261002\Scripts\python.exe" -u "$report\run_pinned_deberta.py" `
  --upstream 'D:\Work\Do-an\workspaces\truongnv\replications\PIDS_Bench_Shire_IEEEAccess2026\upstream' `
  --run-dir $run --stage-dir "$run\workdir" --seed 42 --batch-size 2 `
  --gradient-accumulation-steps 8 --dynamic-padding
```

TF-IDF+LR was run from the same pinned checkout against the staged data, seed 42, without grid search; its exact invocation is recorded in the paired experiment report.
