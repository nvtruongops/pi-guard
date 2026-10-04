# Exact launch record

Executed from PowerShell with the PIDS-Bench run wrapper and offline pinned Hub cache:

```powershell
$run='D:\Work\Do-an\workspaces\truongnv\replications\PIDS_Bench_Shire_IEEEAccess2026\run_artifacts\deberta_seed42_dynamic_padding_restart_2026-10-03'
$report='D:\Work\Do-an\workspaces\truongnv\reports\experiment_reports\pids_bench_two_tier_evidence_matrix_2026-10-02'
$upstream='D:\Work\Do-an\workspaces\truongnv\replications\PIDS_Bench_Shire_IEEEAccess2026\upstream'
$hf='D:\Work\Do-an\workspaces\truongnv\replications\PIDS_Bench_Shire_IEEEAccess2026\run_artifacts\deberta_seed42_repo_2026-10-02\hf-cache'
$env:HF_HOME=$hf
$env:HF_HUB_CACHE=Join-Path $hf 'hub'
$env:HF_HUB_OFFLINE='1'
$env:TOKENIZERS_PARALLELISM='false'
$py=Join-Path $env:TEMP 'pids-bench-deberta-20261002\Scripts\python.exe'
& $py -u (Join-Path $report 'run_pinned_deberta.py') --upstream $upstream --run-dir $run --stage-dir (Join-Path $run 'workdir') --seed 42 --batch-size 2 --gradient-accumulation-steps 8 --dynamic-padding
```

Runtime: Python 3.12.14, PyTorch 2.9.1+cu128, Transformers 4.57.1, Hugging Face Hub 0.36.2, CUDA on an NVIDIA RTX 3060 Laptop GPU. The run uses FP32, 512-token truncation, three epochs, effective batch size 16, and seed 42. Dynamic padding and the microbatch/accumulation split are local execution adaptations to the pinned author training source; one seed is not a reproduction of the paper's five-seed mean.

The public base checkpoint revision and downloaded file SHA-256 values are in `../PIDS_Bench_model_input_manifest_2026-10-03.json`. Input dataset checksums are checked by the wrapper before it stages data. The model hub is in offline mode for this run.

## Resume after AC power is available

The battery-limited run was interrupted at observed step 4,281/5,082. The latest durable checkpoint is `deberta_v3/trainer/checkpoint-3388` (epoch 2); work after that checkpoint is not saved. Use a fresh staging directory because the wrapper refuses to overwrite the existing frozen-data copy:

```powershell
$stage=Join-Path $run 'workdir_resume_after_power'
$checkpoint=Join-Path $run 'deberta_v3\trainer\checkpoint-3388'
& $py -u (Join-Path $report 'run_pinned_deberta.py') --upstream $upstream --run-dir $run --stage-dir $stage --seed 42 --batch-size 2 --gradient-accumulation-steps 8 --dynamic-padding --resume-from-checkpoint $checkpoint
```

The runner rechecks the pinned source commit and input hashes, resumes optimizer/scheduler state from the checkpoint, and marks the run complete only after the original training/evaluation function returns.
