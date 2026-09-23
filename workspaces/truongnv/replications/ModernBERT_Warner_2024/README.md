# ModernBERT (Answer.AI / LightOn 2024) Replication Package

> **Paper**: *ModernBERT: Bringing Modern Transformer Innovations to Pre-trained Encoders*  
> **Authors**: Benjamin Warner, Antoine Chaffin, Benjamin Clavié et al.  
> **Model Repository**: [https://huggingface.co/answerdotai/ModernBERT-base](https://huggingface.co/answerdotai/ModernBERT-base)  
> **Paper Anchor**: `[[37]](#ref37)`  
> **Related Vulnerability**: Zhou et al. (2026) *Prompt Overflow* `[[40]](#ref40)`  

## 🔬 Directory Structure
```
ModernBERT_Warner_2024/
├── README.md                                          # This documentation
├── MODERNBERT_REPLICATION_BENCHMARK_RESULTS.json     # Empirical results
├── papers/
│   └── Warner_2024_ModernBERT_Brings_Modern_Transformers_To_Encoders.pdf
├── datasets/
│   ├── METADATA.json                                 # Rigorous dataset provenance
│   ├── DATASET_CARD.md                               # Schema & class distribution
│   └── modernbert_context_eval_benchmark.json        # 10 long-context benchmark samples
├── lib/
│   └── modernbert_classifier.py                      # ModernBERT RoPE long-context implementation
└── run_modernbert_replication.py                     # Comparative execution runner
```

## 🚀 Reproduction Command
```bash
python workspaces/truongnv/replications/ModernBERT_Warner_2024/run_modernbert_replication.py
```
