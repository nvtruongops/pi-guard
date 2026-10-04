# DistilBERT seed-42 run plan

The run directory contains a staged data copy. Seven frozen CSVs were SHA-256 checked against the pinned PIDS-Bench release; `hard_benign_test.csv` is the same 808 nonblank-row subset used for the other local matrix runs. The public DistilBERT checkpoint files and fixed Hub revision are in `../PIDS_Bench_model_input_manifest_2026-10-03.json`.

This command is retained as a reproducibility note only. The user later limited local model execution to TF-IDF; DistilBERT was not started. If that scope changes, run from the `workdir` directory shown below. It invokes the original release entry point and original baseline source from commit `87dc835566b930ee921240874a4939b2c266c2fe`; the upstream tree is read-only for this experiment.

```powershell
$upstream='D:\Work\Do-an\workspaces\truongnv\replications\PIDS_Bench_Shire_IEEEAccess2026\upstream'
$hf='D:\Work\Do-an\workspaces\truongnv\replications\PIDS_Bench_Shire_IEEEAccess2026\run_artifacts\deberta_seed42_repo_2026-10-02\hf-cache'
$env:HF_HOME=$hf
$env:HF_HUB_CACHE=Join-Path $hf 'hub'
$env:HF_HUB_OFFLINE='1'
$env:TOKENIZERS_PARALLELISM='false'
$env:PYTHONPATH=$upstream
$py=Join-Path $env:TEMP 'pids-bench-deberta-20261002\Scripts\python.exe'
& $py -u (Join-Path $upstream 'scripts\run_distilbert_5seed.py') --seed 42
```

Execution working directory: `D:\Work\Do-an\workspaces\truongnv\replications\PIDS_Bench_Shire_IEEEAccess2026\run_artifacts\distilbert_seed42_restart_2026-10-03\workdir`.

Author parameters are 2 epochs, batch size 16, learning rate `5e-5`, max length 256, and seed 42. The cache is offline and the model's `main` ref was set to the pinned revision after resolving that exact snapshot locally. The output directory from the author entry point is `outputs/multi_seed_runs/distilbert_cluster/seed_42/`; do not compare this single seed to the paper's five-seed mean as if it were a replication of the mean.
