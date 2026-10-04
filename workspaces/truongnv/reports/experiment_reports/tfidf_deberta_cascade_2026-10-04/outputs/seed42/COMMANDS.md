# Evaluation command

Run from `D:\Work\Do-an` after `run_config.json` records `status: completed`. The run uses the already-installed pinned environment and cached local model files; Hugging Face Hub access stays offline. In this experiment, the final author evaluation wrapper was recovered from checkpoint 5,082 with UTF-8 console settings after a CP1252 print error; it did not repeat training.

```powershell
$experiment = 'D:\Work\Do-an\workspaces\truongnv\reports\experiment_reports\tfidf_deberta_cascade_2026-10-04'
$replication = 'D:\Work\Do-an\workspaces\truongnv\replications\PIDS_Bench_Shire_IEEEAccess2026'
$run = Join-Path $replication 'run_artifacts\deberta_seed42_resume_cascade_2026-10-04'
$pythonExe = Join-Path $env:TEMP 'pids-bench-deberta-20261002\Scripts\python.exe'
$hfCache = Join-Path $replication 'run_artifacts\deberta_seed42_repo_2026-10-02\hf-cache'
$env:HF_HOME = $hfCache
$env:HF_HUB_CACHE = Join-Path $hfCache 'hub'
$env:HF_HUB_OFFLINE = '1'
$env:TOKENIZERS_PARALLELISM = 'false'
& $pythonExe (Join-Path $experiment 'evaluate_cascade.py') `
  --raw-data (Join-Path $replication 'upstream\data\pids_bench_v3') `
  --data (Join-Path $run 'workdir\data\pids_bench_v3') `
  --tfidf-model (Join-Path $replication 'run_artifacts\tfidf_seed42_author_source_2026-10-02\models\tfidf_logreg.pkl') `
  --deberta-model (Join-Path $run 'deberta_v3\model') `
  --model-input-manifest (Join-Path $replication 'run_artifacts\PIDS_Bench_model_input_manifest_2026-10-03.json') `
  --output (Join-Path $experiment 'outputs\seed42') `
  --max-fpr 0.015 --batch-size 2 --latency-runs 200
```
