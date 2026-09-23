# PromptShield (ACM CCS 2024) Replication Package

> **Paper**: *PromptShield: Deployable Detection for Prompt Injection Attacks*  
> **Authors**: Dennis Jacob, Hend Alzahrani, Zhanhao Hu, Basel Alomair, David Wagner (UC Berkeley)  
> **Venue**: ACM SIGSAC Conference on Computer and Communications Security (CCS 2024) / CODASPY 2025  
> **Upstream Repository**: [https://github.com/wagner-group/PromptShield](https://github.com/wagner-group/PromptShield)  
> **Paper Anchor**: `[[30]](#ref30)`  

## 🔬 Directory Structure
```
PromptShield_Jacob_CCS2024/
├── README.md                                          # This documentation
├── PROMPTSHIELD_REPLICATION_BENCHMARK_RESULTS.json    # Empirical results
├── papers/
│   └── Jacob_2024_PromptShield_Deployable_Detection_Prompt_Injection_CCS.pdf
├── datasets/
│   ├── METADATA.json                                 # Rigorous dataset provenance
│   ├── DATASET_CARD.md                               # Schema & class distribution
│   └── promptshield_eval_benchmark.json              # 20 curated benchmark samples
├── lib/
│   └── threshold_interpolator.py                     # Low-FPR ROC interpolation implementation
└── run_promptshield_replication.py                   # Independent execution runner
```

## 🚀 Reproduction Command
```bash
python workspaces/truongnv/replications/PromptShield_Jacob_CCS2024/run_promptshield_replication.py
```
