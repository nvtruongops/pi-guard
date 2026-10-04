# Exact DeBERTa resume command

Executed from `D:\Work\Do-an` in PowerShell on AC power. The Hub cache was pinned and offline; output went to a new run directory.

```powershell
$sourceRun = 'D:\Work\Do-an\workspaces\truongnv\replications\PIDS_Bench_Shire_IEEEAccess2026\run_artifacts\deberta_seed42_dynamic_padding_restart_2026-10-03'
$runDir = 'D:\Work\Do-an\workspaces\truongnv\replications\PIDS_Bench_Shire_IEEEAccess2026\run_artifacts\deberta_seed42_resume_cascade_2026-10-04'
$upstreamDir = 'D:\Work\Do-an\workspaces\truongnv\replications\PIDS_Bench_Shire_IEEEAccess2026\upstream'
$reportDir = 'D:\Work\Do-an\workspaces\truongnv\reports\experiment_reports\pids_bench_two_tier_evidence_matrix_2026-10-02'
$scriptPath = Join-Path $reportDir 'run_pinned_deberta.py'
$checkpointPath = Join-Path $sourceRun 'deberta_v3\trainer\checkpoint-3388'
$pythonExe = Join-Path $env:TEMP 'pids-bench-deberta-20261002\Scripts\python.exe'
$hfCache = 'D:\Work\Do-an\workspaces\truongnv\replications\PIDS_Bench_Shire_IEEEAccess2026\run_artifacts\deberta_seed42_repo_2026-10-02\hf-cache'
$env:HF_HOME = $hfCache
$env:HF_HUB_CACHE = Join-Path $hfCache 'hub'
$env:HF_HUB_OFFLINE = '1'
$env:TOKENIZERS_PARALLELISM = 'false'
$logPath = Join-Path $runDir 'training.log'
& $pythonExe -u $scriptPath --upstream $upstreamDir --run-dir $runDir --stage-dir (Join-Path $runDir 'workdir') --seed 42 --batch-size 2 --gradient-accumulation-steps 8 --dynamic-padding --resume-from-checkpoint $checkpointPath 2>&1 | Tee-Object -FilePath $logPath
```

The wrapper verifies the frozen CSV SHA-256 values and refuses to overwrite an existing staging directory. It records the final run status after the author's training and evaluation routine exits.

## UTF-8 recovery after final checkpoint save

The first invocation completed training and saved checkpoint 5,082 plus the model, but CP1252 could not print the wrapper's Unicode completion arrow. The wrapper was then resumed from that final checkpoint, with a fresh stage directory for evaluation and UTF-8 console settings. This recovery did not repeat the fine-tuning steps.

```powershell
$runDir = 'D:\Work\Do-an\workspaces\truongnv\replications\PIDS_Bench_Shire_IEEEAccess2026\run_artifacts\deberta_seed42_resume_cascade_2026-10-04'
$upstreamDir = 'D:\Work\Do-an\workspaces\truongnv\replications\PIDS_Bench_Shire_IEEEAccess2026\upstream'
$reportDir = 'D:\Work\Do-an\workspaces\truongnv\reports\experiment_reports\pids_bench_two_tier_evidence_matrix_2026-10-02'
$scriptPath = Join-Path $reportDir 'run_pinned_deberta.py'
$checkpointPath = Join-Path $runDir 'deberta_v3\trainer\checkpoint-5082'
$stageDir = Join-Path $runDir 'workdir_author_eval_utf8_2026-10-04'
$pythonExe = Join-Path $env:TEMP 'pids-bench-deberta-20261002\Scripts\python.exe'
$hfCache = 'D:\Work\Do-an\workspaces\truongnv\replications\PIDS_Bench_Shire_IEEEAccess2026\run_artifacts\deberta_seed42_repo_2026-10-02\hf-cache'
$env:HF_HOME = $hfCache
$env:HF_HUB_CACHE = Join-Path $hfCache 'hub'
$env:HF_HUB_OFFLINE = '1'
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONUTF8 = '1'
$env:TOKENIZERS_PARALLELISM = 'false'
$logPath = Join-Path $runDir 'author_eval_utf8.log'
& $pythonExe -u $scriptPath --upstream $upstreamDir --run-dir $runDir --stage-dir $stageDir --seed 42 --batch-size 2 --gradient-accumulation-steps 8 --dynamic-padding --resume-from-checkpoint $checkpointPath 2>&1 | Tee-Object -FilePath $logPath
```

