# PI-Guard Tier-1 Fast-Filter Replication Package

> **Scientific Grounding**: Spärck Jones (1972), Jain et al. (NeurIPS 2023 `[[15]]`), Saltzer & Schroeder (1975 `[[16]]`)  
> **Architecture**: Dual-Space TF-IDF (Word n-grams 1-3 + Char_wb n-grams 3-5) with Platt Calibration  
> **Ingress Role**: Fast Clearance (<0.15) & Fast Block (>0.85) Ingress Guardrail  

## 🔬 Directory Structure
```
PIGuard_Tier1_FastFilter/
├── README.md                                          # This documentation
├── TIER1_FASTFILTER_REPLICATION_BENCHMARK_RESULTS.json # Empirical results
├── papers/
│   └── Jain_2023_Baseline_Defenses_Adversarial_Attacks_LLMs.pdf
├── datasets/
│   ├── METADATA.json                                 # Rigorous dataset provenance
│   ├── DATASET_CARD.md                               # Schema & class distribution
│   └── tier1_fastfilter_eval_benchmark.json          # 18 routing benchmark samples
├── lib/
│   └── dual_space_tfidf.py                           # Dual-space TF-IDF & Platt scaling implementation
└── run_tier1_fastfilter_replication.py               # Independent execution runner
```

## 🚀 Reproduction Command
```bash
python workspaces/truongnv/replications/PIGuard_Tier1_FastFilter/run_tier1_fastfilter_replication.py
```
