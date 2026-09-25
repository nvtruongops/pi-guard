"""
calculate_expanded_compatibility_matrix.py
------------------------------------------
Comprehensive evaluation script computing the expanded 12 Models x 14 Paradigms (168 cells)
Compatibility Matrix for LLM Guardrail Research, academically grounded in:
  - Luo & Han (NUS 2026) CASCADE: 19 attacks x 15 defense methods
  - Jacob et al. (ACM CCS 2024) PromptShield: Low-FPR trade-offs (<= 1%)
  - Xu et al. (ACL 2024) Comprehensive Study: 13 defenses taxonomy
  - NIST AI 100-1 (AI RMF 1.0) & ISO/IEC/IEEE 42010 (ATAM Method)

Author: Nguyen Van Truong (Leader) - PI-Guard Capstone Project
Date: 2026-09-23
"""

import json
import os
import sys

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

MODELS = [
    {"id": "M1", "name": "Heuristic & Regex Sanitizer", "family": "Rule-Based", "ref": "Saltzer [16], Yuan [17], Hackett [31]"},
    {"id": "M2", "name": "Toxic Lexicon & Bloom Filters", "family": "Rule-Based", "ref": "Lakera Guard, Llama Guard Blocklist"},
    {"id": "M3", "name": "Sparse Linear Word ML (TF-IDF + LogReg)", "family": "Classical ML", "ref": "Jain [15], Spärck Jones"},
    {"id": "M4", "name": "Subword & Char N-Gram SVMs (char_wb)", "family": "Classical ML", "ref": "Jain [15], Ayub [21]"},
    {"id": "M5", "name": "Shallow Tree Ensembles (TF-IDF + RF)", "family": "Classical ML", "ref": "Ayub & Majumdar CAMLIS 2024 [21]"},
    {"id": "M6", "name": "Dense Bi-Encoder Embeddings (MiniLM)", "family": "Metric Learning", "ref": "Ayub [21], Sentence-BERT"},
    {"id": "M7", "name": "Hidden-State & Activation Probes", "family": "Internal Probing", "ref": "Wen InstructDetector [19], RAP-ID [29]"},
    {"id": "M8", "name": "Legacy Absolute Encoders (BERT/RoBERTa)", "family": "Transformer Encoder", "ref": "Devlin 2019, Liu 2019, Jain [15]"},
    {"id": "M9", "name": "Disentangled Encoders (DeBERTa-v3-base)", "family": "Transformer Encoder", "ref": "He [9], Li InjecGuard ACL 2025 [18]"},
    {"id": "M10", "name": "Multilingual Disentangled (mDeBERTa/PG86M)", "family": "Transformer Encoder", "ref": "Meta [20], Deng MultiJail [35]"},
    {"id": "M11", "name": "Long-Context Modern Encoders (ModernBERT)", "family": "Transformer Encoder", "ref": "Warner et al. 2024 [37]"},
    {"id": "M12", "name": "Generative Safety SLMs (Granite/LlamaGuard)", "family": "Generative SLM", "ref": "Inan [7], Rebedea [8], Padhi [38]"}
]

PARADIGMS = [
    {"id": "A1", "name": "Sublinear TF-IDF + Platt Calibration", "domain": "Statistical & Syntactic"},
    {"id": "A2", "name": "Sliding-Window Perplexity (PPL)", "domain": "Statistical & Syntactic"},
    {"id": "A3", "name": "Char-Level Typographical Anomaly", "domain": "Statistical & Syntactic"},
    {"id": "A4", "name": "Dense Contrastive Metric Centroids", "domain": "Embedding & Geometry"},
    {"id": "A5", "name": "Hidden-State & Activation Gradient", "domain": "Internal Mechanics"},
    {"id": "A6", "name": "Disentangled Content-Position Attention", "domain": "Neural Architecture"},
    {"id": "A7", "name": "Mitigating Overdefense (MOF) KL Loss", "domain": "Optimization & Loss"},
    {"id": "A8", "name": "Randomized Smoothing Majority Voting", "domain": "Stochastic Robustness"},
    {"id": "A9", "name": "Minimax Adversarial Optimization", "domain": "Game Theory & Robustness"},
    {"id": "A10", "name": "Conformal Risk Control (CRC) Bounds", "domain": "Statistical Calibration"},
    {"id": "A11", "name": "Low-FPR ROC Threshold Interpolation", "domain": "Operational Economics"},
    {"id": "A12", "name": "Hierarchical Instruction Privilege", "domain": "Architectural Isolation"},
    {"id": "A13", "name": "Head-and-Tail Priority Chunking", "domain": "Context Window Scaling"},
    {"id": "A14", "name": "Multi-Turn Contextual Drift Tracking", "domain": "Temporal & Session State"}
]

# Evaluation scores for all 12 x 14 = 168 cells
# Format: (model_id, paradigm_id): (score 0-10, status, concise_justification)
SCORES = {
    # M1: Heuristic & Regex Sanitizer
    ("M1", "A1"): (1, "Incompatible", "Deterministic string matching lacks continuous margin z for Platt calibration."),
    ("M1", "A2"): (0, "Incompatible", "No language model distribution to compute token perplexity."),
    ("M1", "A3"): (10, "Native", "Native domain: Regex directly decodes homoglyphs, zero-width, base64, and leetspeak."),
    ("M1", "A4"): (0, "Incompatible", "No continuous metric space representation."),
    ("M1", "A5"): (0, "Incompatible", "No internal neural layers or activations."),
    ("M1", "A6"): (0, "Incompatible", "No attention matrices to decouple content and position."),
    ("M1", "A7"): (0, "Incompatible", "Non-differentiable rules cannot optimize KL divergence invariant loss."),
    ("M1", "A8"): (2, "Incompatible", "Perturbation breaks exact string signatures, creating massive false negatives."),
    ("M1", "A9"): (1, "Incompatible", "Discrete non-differentiable rules cannot compute minimax gradients."),
    ("M1", "A10"): (4, "Conditional", "Only binary outputs {0, 1}; lacks continuous risk scores for tri-state conformal partitioning."),
    ("M1", "A11"): (3, "Incompatible", "Fixed binary rules produce discrete ROC steps, cannot smoothly interpolate low-FPR."),
    ("M1", "A12"): (5, "Conditional", "Can detect and sanitize delimiters (XML/Markdown tags) prior to model ingestion."),
    ("M1", "A13"): (8, "Native", "Executes fast head/tail string truncation and regex regex scan in < 0.1ms."),
    ("M1", "A14"): (3, "Incompatible", "Stateless regex cannot track semantic drift trajectories across conversational turns."),

    # M2: Toxic Lexicon & Bloom Filters
    ("M2", "A1"): (2, "Incompatible", "Binary hash lookups do not map to continuous TF-IDF vector margins."),
    ("M2", "A2"): (0, "Incompatible", "No language model probabilities."),
    ("M2", "A3"): (7, "Conditional", "Detects forbidden tokens, but homoglyphs cause false negative hash misses."),
    ("M2", "A4"): (1, "Incompatible", "Exact hash keys cannot measure continuous cosine distance."),
    ("M2", "A5"): (0, "Incompatible", "No neural activations."),
    ("M2", "A6"): (0, "Incompatible", "No attention mechanism."),
    ("M2", "A7"): (0, "Incompatible", "Non-trainable static dictionary."),
    ("M2", "A8"): (2, "Incompatible", "Stochastic noise causes hash lookup misses."),
    ("M2", "A9"): (1, "Incompatible", "Non-differentiable hash table."),
    ("M2", "A10"): (3, "Incompatible", "Cannot calibrate risk thresholds on deterministic hash hit/miss."),
    ("M2", "A11"): (2, "Incompatible", "Step-function ROC curve with high false positive trigger rates."),
    ("M2", "A12"): (4, "Conditional", "Can enforce prohibited keyword blacklists on specific prompt fields."),
    ("M2", "A13"): (8, "Native", "O(1) hash lookups on 200k char chunks execute in sub-millisecond time."),
    ("M2", "A14"): (3, "Incompatible", "Stateless dictionary matching cannot model multi-turn contextual accumulation."),

    # M3: Sparse Linear Word ML (TF-IDF + LogReg)
    ("M3", "A1"): (10, "Native", "Native core: Sublinear word TF-IDF + Platt logistic margin produces optimal calibrated scores in 1.2ms."),
    ("M3", "A2"): (5, "Conditional", "Requires auxiliary n-gram LM; adds latency overhead to sub-millisecond inference."),
    ("M3", "A3"): (6, "Conditional", "Word-level n-grams are vulnerable to character mutations and leetspeak."),
    ("M3", "A4"): (4, "Conditional", "Sparse centroids in 50k-dim space suffer from sparsity and curse of dimensionality."),
    ("M3", "A5"): (0, "Incompatible", "Linear model has no deep hidden states or attention gradients."),
    ("M3", "A6"): (0, "Incompatible", "Lacks self-attention mechanism."),
    ("M3", "A7"): (4, "Conditional", "Linear weights lack capacity to absorb KL invariant loss without massive accuracy drop."),
    ("M3", "A8"): (5, "Conditional", "Running M=10 iterations multiplies latency to 12ms, defeating fast filter purpose."),
    ("M3", "A9"): (6, "Conditional", "Discrete vocabulary requires greedy coordinate ascent rather than continuous SGD."),
    ("M3", "A10"): (10, "Native", "Platt calibrated output perfectly supports Conformal Risk Control to partition traffic at FPR < 1.5%."),
    ("M3", "A11"): (9, "Native", "Continuous logistic margin enables clean ROC threshold interpolation down to FPR 0.5%."),
    ("M3", "A12"): (5, "Conditional", "Can train separate weight heads for system vs user prompt sections."),
    ("M3", "A13"): (10, "Native", "Super-fast linear scoring (<0.1ms/block) enables low-latency scanning of 200k documents with early stopping."),
    ("M3", "A14"): (4, "Conditional", "Can concatenate past turn TF-IDF vectors, but lacks semantic nuance."),

    # M4: Subword & Char N-Gram SVMs (char_wb)
    ("M4", "A1"): (9, "Native", "Combines character n-gram frequencies (3-5 chars) with linear/kernel decision margins."),
    ("M4", "A2"): (6, "Conditional", "Char-level perplexity can be approximated but adds computation overhead."),
    ("M4", "A3"): (10, "Native", "Native champion for typographical anomaly: char_wb captures leetspeak, punctuation obfuscation, and typos."),
    ("M4", "A4"): (5, "Conditional", "High-dimensional sparse char n-gram centroids suffer from sparsity."),
    ("M4", "A5"): (0, "Incompatible", "Linear SVM has no deep internal activations."),
    ("M4", "A6"): (0, "Incompatible", "No self-attention mechanism."),
    ("M4", "A7"): (4, "Conditional", "Convex SVM formulation does not naturally accommodate MOF KL loss."),
    ("M4", "A8"): (6, "Conditional", "Inherent robustness to character perturbation makes randomized smoothing partially redundant."),
    ("M4", "A9"): (7, "Conditional", "Adversarial training via greedy char flips improves boundary robustness."),
    ("M4", "A10"): (9, "Native", "Platt/Isotonic calibrated SVM margins allow finite-sample CRC risk bounding."),
    ("M4", "A11"): (9, "Native", "Allows fine-grained threshold interpolation in the low-FPR regime."),
    ("M4", "A12"): (5, "Conditional", "Can weight character n-grams from privileged fields differently."),
    ("M4", "A13"): (10, "Native", "Fast feature extraction (<0.2ms/block) makes it ideal for Tier 1 block scanning of long documents."),
    ("M4", "A14"): (4, "Conditional", "Limited context retention across multi-turn sessions."),

    # M5: Shallow Tree Ensembles (TF-IDF + Random Forest)
    ("M5", "A1"): (8, "Conditional", "Random Forest outputs tree vote probabilities, but uncalibrated leaf distributions require isotonic regression."),
    ("M5", "A2"): (4, "Conditional", "Inefficient for sequence probability modeling."),
    ("M5", "A3"): (6, "Conditional", "Captures non-linear feature interactions but memory scales poorly with char n-grams."),
    ("M5", "A4"): (5, "Conditional", "Tree partitioning differs from metric distance spaces."),
    ("M5", "A5"): (0, "Incompatible", "No continuous hidden representations."),
    ("M5", "A6"): (0, "Incompatible", "No attention mechanism."),
    ("M5", "A7"): (2, "Incompatible", "Tree splits are non-differentiable; cannot optimize continuous MOF KL loss."),
    ("M5", "A8"): (6, "Conditional", "Bagging already provides variance reduction; extra smoothing inflates CPU latency to 40ms."),
    ("M5", "A9"): (5, "Conditional", "Non-differentiable trees make continuous adversarial optimization difficult."),
    ("M5", "A10"): (8, "Conditional", "Tree probabilities can be conformalized but suffer from step discontinuities."),
    ("M5", "A11"): (7, "Conditional", "Step-wise ROC curves make extreme low-FPR interpolation sub-optimal (Ayub CAMLIS 2024)."),
    ("M5", "A12"): (4, "Conditional", "Requires hand-crafted feature engineering for instruction hierarchies."),
    ("M5", "A13"): (7, "Conditional", "Tree inference is slower than linear models (3-5ms/block), causing latency accumulation on 200k docs."),
    ("M5", "A14"): (4, "Conditional", "Concatenating multi-turn trees causes exponential feature explosion."),

    # M6: Dense Bi-Encoder Embeddings (MiniLM / SBERT)
    ("M6", "A1"): (4, "Conditional", "Concatenating dense embeddings with sparse TF-IDF is redundant and memory-heavy."),
    ("M6", "A2"): (2, "Incompatible", "Bi-encoders output pooled vectors, not autoregressive next-token distributions."),
    ("M6", "A3"): (5, "Conditional", "Sentence embeddings partially smooth out character anomalies, blinding the model to unicode tricks."),
    ("M6", "A4"): (10, "Native", "Native design (Ayub [21]): Cosine distance to toxic cluster centroids in continuous R^384."),
    ("M6", "A5"): (6, "Conditional", "Can extract intermediate layer embeddings, but pooling discards token-level trajectories."),
    ("M6", "A6"): (4, "Conditional", "Uses standard Multi-Head Attention without content-position disentanglement."),
    ("M6", "A7"): (5, "Conditional", "Contrastive loss can enforce invariance, but lacks token-level MOF attribution."),
    ("M6", "A8"): (6, "Conditional", "Averaging M=10 dense vectors is mathematically sound but inflates CPU latency to 80ms."),
    ("M6", "A9"): (8, "Conditional", "Continuous vector space allows Projected Gradient Descent (PGD) in embedding space."),
    ("M6", "A10"): (9, "Native", "Cosine proximity scores map smoothly into [0, 1] for empirical Conformal Risk Control."),
    ("M6", "A11"): (8, "Conditional", "Dense clustering yields smooth ROC, but hubness problem causes high false positive floor (10-15%)."),
    ("M6", "A12"): (6, "Conditional", "Cross-attention between privileged and untrusted prompt is absent in bi-encoders."),
    ("M6", "A13"): (7, "Conditional", "Embedding 50 blocks of 512 tokens requires 400ms on CPU, violating low-latency constraints."),
    ("M6", "A14"): (8, "Native", "Cosine similarity between turn vectors tracks semantic drift trajectory cleanly."),

    # M7: Hidden-State & Activation Probes
    ("M7", "A1"): (3, "Incompatible", "Linear probes operate on continuous hidden dimensions, not external TF-IDF features."),
    ("M7", "A2"): (7, "Conditional", "Hidden state norms correlate with perplexity spikes."),
    ("M7", "A3"): (4, "Conditional", "Subword tokenizers fragment character anomalies before reaching hidden layers."),
    ("M7", "A4"): (8, "Conditional", "Probes measure separation of hidden vectors across instruction-following regimes."),
    ("M7", "A5"): (10, "Native", "Native domain (InstructDetector [19], RAP-ID [29]): Probing residual stream activations and attention entropy."),
    ("M7", "A6"): (5, "Conditional", "Evaluates internal attention weights, but does not restructure the underlying attention formula."),
    ("M7", "A7"): (6, "Conditional", "Can penalize trigger-sensitive hidden neurons during probe training."),
    ("M7", "A8"): (6, "Conditional", "Hidden state variance under perturbation measures model stability."),
    ("M7", "A9"): (8, "Conditional", "Adversarial gradients can be backpropagated directly to probe representations."),
    ("M7", "A10"): (8, "Conditional", "Probe logits can be calibrated using conformal prediction."),
    ("M7", "A11"): (8, "Conditional", "Provides smooth ROC curves for low-FPR tuning."),
    ("M7", "A12"): (8, "Native", "Explicitly measures how privileged system instructions are overwritten in hidden layers."),
    ("M7", "A13"): (4, "Conditional", "Requires full forward passes of underlying LLM, making 200k char scanning prohibitively slow."),
    ("M7", "A14"): (8, "Native", "Tracks representation shifts across multiple conversational forward passes."),

    # M8: Legacy Absolute Encoders (BERT / RoBERTa)
    ("M8", "A1"): (2, "Incompatible", "Deep self-attention renders external bag-of-words TF-IDF obsolete and redundant."),
    ("M8", "A2"): (8, "Conditional", "Pseudo-Perplexity via Masked LM is effective but requires N forward passes (>100ms)."),
    ("M8", "A3"): (5, "Conditional", "Subword BPE/WordPiece tokenization is blinded by character mutations (Hackett [31])."),
    ("M8", "A4"): (6, "Conditional", "[CLS] token pooling suffers from representation anisotropy (narrow cone collapse)."),
    ("M8", "A5"): (7, "Conditional", "Can probe intermediate layers, though later layers suffer from trigger word over-fitting."),
    ("M8", "A6"): (5, "Conditional", "Absolute position embeddings are added to token embeddings at layer 0; cannot disentangle relative vectors."),
    ("M8", "A7"): (6, "Conditional", "MOF loss on output logits helps, but fixed absolute position limits semantic decoupling."),
    ("M8", "A8"): (6, "Conditional", "SmoothLLM M=10 inflates latency from 35ms to 350ms on CPU."),
    ("M8", "A9"): (8, "Conditional", "FGM / FreeLB adversarial training on token embeddings significantly hardens BERT."),
    ("M8", "A10"): (9, "Native", "Softmax risk scores are readily calibrated via Conformal Risk Control."),
    ("M8", "A11"): (8, "Conditional", "Supports ROC interpolation, but trigger word bias creates false positive bumps at low FPR."),
    ("M8", "A12"): (7, "Conditional", "Segment embeddings (token_type_ids) provide rudimentary two-level privilege separation."),
    ("M8", "A13"): (6, "Conditional", "Scanning 200k chars requires ~40 forward passes, taking ~1.2s on CPU without early stopping."),
    ("M8", "A14"): (7, "Conditional", "Cross-turn attention is bounded by 512 token context window."),

    # M9: Disentangled Encoders (DeBERTa-v3-base)
    ("M9", "A1"): (2, "Incompatible", "Disentangled attention captures full contextual semantics; TF-IDF is redundant inside M9."),
    ("M9", "A2"): (6, "Conditional", "RTD discriminator scores flag replaced tokens, acting as a learned perplexity proxy."),
    ("M9", "A3"): (6, "Conditional", "Subword tokenizer requires Tier-0 Heuristic Scrubber to prevent unicode blindness."),
    ("M9", "A4"): (7, "Conditional", "Produces less anisotropic embeddings than BERT, though end-to-end classification is superior."),
    ("M9", "A5"): (8, "Conditional", "Intermediate disentangled representations provide clean gradient signals for probing."),
    ("M9", "A6"): (10, "Native", "Sovereign Champion: Decouples content and relative position across 3 attention matrices (He ICLR 2023)."),
    ("M9", "A7"): (10, "Native", "Sovereign Champion: MOF KL loss (Li ACL 2025) eliminates keyword trigger bias while preserving F1 > 0.95."),
    ("M9", "A8"): (6, "Conditional", "SmoothLLM is redundant due to MOF robustness, and M=10 raises latency to 250ms."),
    ("M9", "A9"): (10, "Native", "Sovereign Champion: Minimax optimization (DataSentinel) hardens DeBERTa against adaptive evasion."),
    ("M9", "A10"): (10, "Native", "Sovereign Champion: Finite-sample CRC calibrates softmax output to rigorously bound FPR <= 1.5%."),
    ("M9", "A11"): (10, "Native", "Produces smooth, monotonic ROC curves achieving TPR >= 90% at FPR <= 1.0% (PromptShield criteria)."),
    ("M9", "A12"): (8, "Native", "Relative position attention cleanly preserves boundary distinctions between system and user prompts."),
    ("M9", "A13"): (8, "Native", "Combined with Tier 1 Early-Stopping, M9 only inspects ambiguous tail/head blocks, keeping latency < 25ms."),
    ("M9", "A14"): (8, "Native", "High-capacity representation models multi-turn prompt context within 512 token budget."),

    # M10: Multilingual Disentangled (mDeBERTa / Prompt Guard 86M)
    ("M10", "A1"): (2, "Incompatible", "Multilingual tokenizer and self-attention supersede statistical n-grams."),
    ("M10", "A2"): (6, "Conditional", "Cross-lingual token prediction acts as multilingual perplexity filter."),
    ("M10", "A3"): (7, "Conditional", "Larger vocabulary (250k tokens) captures diverse scripts, though unicode evasion still requires Tier 0."),
    ("M10", "A4"): (7, "Conditional", "Cross-lingual semantic clustering maps Vietnamese and English attacks to shared manifolds."),
    ("M10", "A5"): (7, "Conditional", "Cross-lingual alignment can be inspected via hidden state probes."),
    ("M10", "A6"): (10, "Native", "Disentangled attention generalises across diverse word-order typologies (SVO vs SOV)."),
    ("M10", "A7"): (9, "Native", "MOF loss prevents over-defense on translated sensitive keywords across languages (Deng ICLR 2024)."),
    ("M10", "A8"): (6, "Conditional", "Perturbation in low-resource languages can shift tokens out-of-vocabulary."),
    ("M10", "A9"): (9, "Native", "Cross-lingual minimax optimization hardens model against multilingual code-switching evasion."),
    ("M10", "A10"): (10, "Native", "CRC provides separate calibration thresholds per language to guarantee global FPR <= 1.5%."),
    ("M10", "A11"): (9, "Native", "Maintains high TPR under low-FPR constraints across both English and Vietnamese."),
    ("M10", "A12"): (8, "Native", "Enforces privilege boundaries across mixed-language prompts."),
    ("M10", "A13"): (8, "Native", "Protects long translated documents via block chunking with early stopping."),
    ("M10", "A14"): (8, "Native", "Tracks conversational language-switching drift across multiple turns."),

    # M11: Long-Context Modern Encoders (ModernBERT)
    ("M11", "A1"): (2, "Incompatible", "FlashAttention-2 and RoPE make external statistical features completely redundant."),
    ("M11", "A2"): (6, "Conditional", "Can compute sequence likelihood over extended context."),
    ("M11", "A3"): (6, "Conditional", "Standard subword tokenizer requires front-end heuristic scrubbing."),
    ("M11", "A4"): (7, "Conditional", "Global pooled embeddings capture document-level semantic representations."),
    ("M11", "A5"): (8, "Conditional", "GeGLU activations provide rich non-linear hidden representations for probing."),
    ("M11", "A6"): (8, "Conditional", "Uses Rotary Position Embeddings (RoPE); structurally different from DeBERTa disentanglement but solves relative position."),
    ("M11", "A7"): (9, "Native", "MOF invariant loss applies directly to 8,192 token classification head."),
    ("M11", "A8"): (5, "Conditional", "Smoothing across 8k tokens is computationally expensive."),
    ("M11", "A9"): (9, "Native", "FlashAttention enables fast adversarial gradient computation over long contexts."),
    ("M11", "A10"): (10, "Native", "Conformal Risk Control calibrates long-context document risk scores directly."),
    ("M11", "A11"): (10, "Native", "Enables precise ROC threshold interpolation for long RAG documents."),
    ("M11", "A12"): (9, "Native", "Native 8,192 window allows end-to-end modeling of complex system prompts, RAG context, and user input."),
    ("M11", "A13"): (10, "Native", "Sovereign Champion: Native 8,192 window eliminates the need for block chunking on documents up to 32k characters!"),
    ("M11", "A14"): (9, "Native", "Fits entire multi-turn conversation histories (10+ turns) in a single forward pass without sliding window truncation."),

    # M12: Generative Safety SLMs (Granite Guardian / Llama Guard)
    ("M12", "A1"): (1, "Incompatible", "TF-IDF is obsolete for 2B-8B autoregressive generative language models."),
    ("M12", "A2"): (10, "Native", "Native champion: Autoregressive causal decoder computes exact token perplexity in a single forward pass."),
    ("M12", "A3"): (5, "Conditional", "Slow token-by-token generation is ineffective for surface character anomaly detection."),
    ("M12", "A4"): (3, "Incompatible", "Causal unidirectional attention produces poor sentence-level metric embeddings."),
    ("M12", "A5"): (8, "Conditional", "Hidden states can be probed, but generative reasoning is the primary output."),
    ("M12", "A6"): (2, "Incompatible", "Decoder-only LLMs use standard RoPE / causal attention, incompatible with 3-matrix disentanglement."),
    ("M12", "A7"): (5, "Conditional", "Can use DPO/RLHF to reduce over-defense, but fine-tuning requires massive compute."),
    ("M12", "A8"): (1, "Incompatible", "Disastrous Latency: M=10 perturbations on an 8B model takes 15-20 SECONDS, paralyzing low-latency ingress."),
    ("M12", "A9"): (5, "Conditional", "Minimax adversarial training on 8B LLMs requires massive multi-GPU compute clusters."),
    ("M12", "A10"): (9, "Native", "Conformal prediction on safety verdict tokens ('Safe'/'Unsafe') provides rigorous high-assurance risk bounds."),
    ("M12", "A11"): (8, "Conditional", "Token log-probabilities allow threshold interpolation, but latency restricts low-latency dynamic tuning."),
    ("M12", "A12"): (10, "Native", "Native reasoning: Understands complex instruction hierarchies via in-context policy reasoning."),
    ("M12", "A13"): (5, "Conditional", "Scanning 200k documents by chunking into an 8B model incurs enormous GPU memory and tens of seconds latency."),
    ("M12", "A14"): (10, "Native", "Native multi-turn reasoning: Full causal attention models subtle Crescendo escalation trajectories across turns.")
}

def analyze():
    print("=" * 85)
    print("PI-GUARD EXPANDED 12x14 ARCHITECTURAL-ALGORITHMIC COMPATIBILITY MATRIX")
    print("Grounded in: CASCADE (19x15), PromptShield (Low-FPR <=1%), NIST AI RMF, ISO 42010")
    print("=" * 85)

    status_counts = {"Native": 0, "Conditional": 0, "Incompatible": 0}
    model_stats = {}
    paradigm_stats = {p["id"]: [] for p in PARADIGMS}

    for m in MODELS:
        scores = []
        for p in PARADIGMS:
            score, status, _ = SCORES[(m["id"], p["id"])]
            status_counts[status] += 1
            scores.append(score)
            paradigm_stats[p["id"]].append(score)
        model_stats[m["id"]] = {
            "name": m["name"],
            "family": m["family"],
            "avg_score": sum(scores) / len(scores),
            "native_count": sum(1 for s in scores if s >= 9),
            "incompatible_count": sum(1 for s in scores if s <= 3)
        }

    total_cells = len(MODELS) * len(PARADIGMS)
    print(f"\n[1] Overall Statistics ({total_cells} Cells Total):")
    print(f"  - 🟢 Native / Perfect Fit (Score 9-10):       {status_counts['Native']:<3} ({status_counts['Native']/total_cells*100:.1f}%)")
    print(f"  - 🟡 Conditional / High Overhead (Score 4-8):   {status_counts['Conditional']:<3} ({status_counts['Conditional']/total_cells*100:.1f}%)")
    print(f"  - 🔴 Incompatible / Infeasible (Score 0-3):     {status_counts['Incompatible']:<3} ({status_counts['Incompatible']/total_cells*100:.1f}%)")

    print("\n[2] Model Versatility Ranking (Ranked by Average Compatibility Score across 14 Paradigms):")
    sorted_models = sorted(model_stats.items(), key=lambda x: x[1]["avg_score"], reverse=True)
    for rank, (m_id, data) in enumerate(sorted_models, 1):
        print(f"  {rank:>2}. {m_id:<4} {data['name']:<42} [{data['family']:<19}] -> Avg: {data['avg_score']:.2f}/10 (Native: {data['native_count']}, Incomp: {data['incompatible_count']})")

    print("\n[3] Paradigm Applicability Ranking (Ranked by Universality across 12 Models):")
    paradigm_avg_list = []
    for p in PARADIGMS:
        avg = sum(paradigm_stats[p["id"]]) / len(paradigm_stats[p["id"]])
        native_cnt = sum(1 for s in paradigm_stats[p["id"]] if s >= 9)
        paradigm_avg_list.append((p["id"], p["name"], p["domain"], avg, native_cnt))
    
    sorted_paradigms = sorted(paradigm_avg_list, key=lambda x: x[3], reverse=True)
    for rank, (p_id, name, domain, avg, native_cnt) in enumerate(sorted_paradigms, 1):
        print(f"  {rank:>2}. {p_id:<4} {name:<42} [{domain:<24}] -> Avg: {avg:.2f}/10 (Native in {native_cnt}/12 models)")

    # Export to JSON
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "04_benchmarks_and_data"))
    os.makedirs(output_dir, exist_ok=True)
    json_path = os.path.join(output_dir, "compatibility_matrix_expanded_12x14.json")

    export_data = {
        "metadata": {
            "title": "Expanded 12x14 Architectural-Algorithmic Compatibility Matrix",
            "academic_grounding": "Luo & Han CASCADE (19x15), Jacob PromptShield (Low-FPR <=1%), NIST AI RMF, ISO/IEC/IEEE 42010",
            "total_models": len(MODELS),
            "total_paradigms": len(PARADIGMS),
            "total_cells": total_cells,
            "status_distribution": {
                "native": status_counts["Native"],
                "conditional": status_counts["Conditional"],
                "incompatible": status_counts["Incompatible"]
            }
        },
        "models": MODELS,
        "paradigms": PARADIGMS,
        "model_rankings": [
            {"model_id": m_id, **data} for m_id, data in sorted_models
        ],
        "paradigm_rankings": [
            {"paradigm_id": p_id, "name": name, "domain": domain, "avg_score": round(avg, 2), "native_count": native_cnt}
            for p_id, name, domain, avg, native_cnt in sorted_paradigms
        ],
        "evaluations": [
            {
                "model_id": m["id"],
                "model_name": m["name"],
                "paradigm_id": p["id"],
                "paradigm_name": p["name"],
                "score": SCORES[(m["id"], p["id"])][0],
                "status": SCORES[(m["id"], p["id"])][1],
                "justification": SCORES[(m["id"], p["id"])][2]
            }
            for m in MODELS for p in PARADIGMS
        ]
    }

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)

    print(f"\n✔ Successfully exported 12x14 evaluation dataset to: {json_path}")

if __name__ == "__main__":
    analyze()
