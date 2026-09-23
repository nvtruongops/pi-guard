# DATASET CARD: DataSentinel Open-Prompt-Injection Evaluation Suite

## 1. Overview & Provenance
- **Dataset Name**: Open-Prompt-Injection Evaluation Benchmark
- **Paper**: *DataSentinel: A Game-Theoretic Detection of Prompt Injection Attacks* (IEEE S&P 2025 - Distinguished Paper Award)
- **Authors**: Yupei Liu, Yuqi Jia, Jinyuan Jia, Dawn Song, Neil Zhenqiang Gong
- **Upstream Repository**: [https://github.com/liu00222/Open-Prompt-Injection](https://github.com/liu00222/Open-Prompt-Injection)
- **Local Location**: `workspaces/truongnv/replications/DataSentinel_Liu_SP2025/datasets/datasentinel_eval_benchmark.json`
- **SHA-256**: `b084ca210db226a166b9dfbbd5bba9f0cad71570cf152663a39744e4a40fd4c0`
- **Sample Count**: 20 items

## 2. Taxonomy & Class Distribution
- **Direct Injection**: 5 samples (Standard instruction overrides, system dump commands)
- **Adaptive Injection**: 5 samples (Minimax evasive prompts, academic wrapping, reverse strings)
- **Benign Standard**: 5 samples (Multi-turn conversations, coding, general knowledge)
- **Benign Overdefense**: 5 samples (NotInject-style safe programming code containing 'ignore', 'override')

## 3. Grounded Academic Role in PI-Guard
Demonstrates how minimax game-theoretic optimization maintains high recall on adaptive evasion attacks while preserving near-zero FPR on benign engineering contexts.
