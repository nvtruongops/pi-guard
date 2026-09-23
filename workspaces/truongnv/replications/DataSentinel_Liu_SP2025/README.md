# DataSentinel (IEEE S&P 2025) Replication Package

> **Paper**: *DataSentinel: A Game-Theoretic Detection of Prompt Injection Attacks*  
> **Authors**: Yupei Liu, Yuqi Jia, Jinyuan Jia, Dawn Song, Neil Zhenqiang Gong  
> **Venue**: 46th IEEE Symposium on Security and Privacy (S&P 2025) — **Distinguished Paper Award**  
> **Upstream Repository**: [https://github.com/liu00222/Open-Prompt-Injection](https://github.com/liu00222/Open-Prompt-Injection)  
> **Paper Anchor**: `[[32]](#ref32)`  

## 🔬 Directory Structure
```
DataSentinel_Liu_SP2025/
├── README.md                                          # This documentation
├── DATASENTINEL_REPLICATION_BENCHMARK_RESULTS.json     # Empirical results
├── papers/
│   └── Liu_2025_DataSentinel_Game_Theoretic_Detection_Prompt_Injection.pdf
├── datasets/
│   ├── METADATA.json                                 # Rigorous dataset provenance
│   ├── DATASET_CARD.md                               # Schema & class distribution
│   └── datasentinel_eval_benchmark.json              # 20 curated benchmark samples
├── lib/
│   └── minimax_detector.py                           # Minimax detector implementation
└── run_datasentinel_replication.py                    # Independent execution runner
```

## 🚀 Reproduction Command
```bash
python workspaces/truongnv/replications/DataSentinel_Liu_SP2025/run_datasentinel_replication.py
```
