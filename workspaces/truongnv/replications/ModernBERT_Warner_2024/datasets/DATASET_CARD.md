# DATASET CARD: ModernBERT Long-Context Evaluation Benchmark

## 1. Overview & Provenance
- **Dataset Name**: ModernBERT Long-Context Evaluation Suite
- **Paper**: *ModernBERT: Bringing Modern Transformer Innovations to Pre-trained Encoders* (Answer.AI / LightOn 2024)
- **Authors**: Benjamin Warner et al.
- **Model Weight Source**: [https://huggingface.co/answerdotai/ModernBERT-base](https://huggingface.co/answerdotai/ModernBERT-base)
- **Local Location**: `workspaces/truongnv/replications/ModernBERT_Warner_2024/datasets/modernbert_context_eval_benchmark.json`
- **SHA-256**: `27e1ca8d519b83f663bcea00985d80377b555c1659fbe005e35134a1cdb14e60`
- **Sample Count**: 10 items

## 2. Taxonomy & Context Window Distribution
- **Short Head Injection**: 2 samples (<512 tokens, standard immediate override)
- **Medium Overflow Injection**: 1 sample (~650 tokens, payload offset at token 520)
- **Long Overflow Injection**: 1 sample (~1450 tokens, payload offset at token 1150)
- **Extreme Tail Injection**: 1 sample (~2500 tokens, payload offset at token 2350)
- **Benign Multi-scale Documents**: 3 samples (16 tokens, 600 tokens, 2200 tokens)
- **Benign Overdefense Code**: 2 samples (Python inheritance method override, Git ignore)

## 3. Grounded Academic Role in PI-Guard
Directly addresses the Prompt Overflow vulnerability (Zhou et al. 2026 [[40]]), proving that legacy 512-token encoders have a critical blindspot past token 512, which ModernBERT's native 8,192 RoPE context resolves.
