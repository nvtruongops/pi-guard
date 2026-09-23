# DATASET CARD: PromptShield Low-FPR Evaluation Benchmark

## 1. Overview & Provenance
- **Dataset Name**: PromptShield Low-FPR Benchmark Suite
- **Paper**: *PromptShield: Deployable Detection for Prompt Injection Attacks* (ACM CCS 2024)
- **Authors**: Dennis Jacob, Hend Alzahrani, Zhanhao Hu, Basel Alomair, David Wagner (UC Berkeley)
- **Upstream Repository**: [https://github.com/wagner-group/PromptShield](https://github.com/wagner-group/PromptShield)
- **HuggingFace Dataset**: [https://huggingface.co/datasets/hendzh/PromptShield](https://huggingface.co/datasets/hendzh/PromptShield)
- **Local Location**: `workspaces/truongnv/replications/PromptShield_Jacob_CCS2024/datasets/promptshield_eval_benchmark.json`
- **SHA-256**: `8a21503129d5c2caebac131a3a58bbf8e44f96351f8a51653fb8c0feb503443c`
- **Sample Count**: 20 items

## 2. Taxonomy & Class Distribution
- **Direct Injection**: 5 samples (Standard instruction overrides, system dump commands)
- **Indirect Injection**: 5 samples (Payloads disguised in emails, articles, and resumes)
- **Benign Standard**: 5 samples (Technical explanations, literature, everyday Q&A)
- **Benign Overdefense**: 5 samples (Valid programming code containing method overriding, Git ignore)

## 3. Grounded Academic Role in PI-Guard
Serves as the empirical foundation for calibrating detection thresholds in the Low-FPR regime (FPR <= 1.0%), proving that simple detectors collapse under low FPR without multi-tier routing.
