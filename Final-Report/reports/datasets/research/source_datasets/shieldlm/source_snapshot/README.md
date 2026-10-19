---
language:
  - en
  - fr
  - de
  - es
  - it
  - pt
  - ro
  - ca
license: mit
task_categories:
  - text-classification
tags:
  - prompt-injection
  - ai-safety
  - llm-security
  - jailbreak
  - adversarial
size_categories:
  - 10K<n<100K
dataset_info:
  features:
    - name: id
      dtype: string
    - name: text
      dtype: string
    - name: label_binary
      dtype: int64
    - name: label_category
      dtype: string
    - name: label_intent
      dtype: string
    - name: source
      dtype: string
    - name: language
      dtype: string
    - name: context
      dtype: string
    - name: metadata
      dtype: string
  splits:
    - name: train
      num_examples: 37913
    - name: validation
      num_examples: 8124
    - name: test
      num_examples: 8125
---

# ShieldLM Prompt Injection Dataset

A unified prompt injection detection dataset with **54,162 samples** spanning **three attack categories**: direct injection, indirect injection, and jailbreak. Curated from 11 source datasets with a 3-level hierarchical label schema.

## Dataset Description

### Purpose

Training and evaluating prompt injection classifiers for production deployment. Designed to address gaps in existing datasets:

- **Indirect injection** coverage (via InjecAgent tool-embedded attacks)
- **Jailbreak techniques** (via TrustAIRLab in-the-wild prompts + jackhhao classification)
- **Application-structured benign data** (prevents format-based false positives)
- **Sensitive-topic stress tests** (via JailbreakBench — topics != techniques)

### Statistics

| Metric | Value |
|--------|-------|
| Total samples | 54,162 |
| Train / Val / Test | 37,913 / 8,124 / 8,125 |
| Benign | 35,197 (65.0%) |
| Attack | 18,965 (35.0%) |
| Languages | 8 (en, fr, es, it, de, pt, ro, ca) |
| Sources | 11 datasets |

**Category breakdown:**

| Category | Count | % |
|----------|-------|---|
| benign | 35,197 | 65.0% |
| direct_injection | 16,893 | 31.2% |
| indirect_injection | 1,054 | 1.9% |
| jailbreak | 1,018 | 1.9% |

### Label Schema

| Level | Field | Values |
|-------|-------|--------|
| 1 (Binary) | `label_binary` | 0 (BENIGN), 1 (ATTACK) |
| 2 (Category) | `label_category` | benign, direct_injection, indirect_injection, jailbreak |
| 3 (Intent) | `label_intent` | goal_hijacking, data_exfiltration, financial_harm, ... |

### Source Datasets

| Source | License | Category | Samples |
|--------|---------|----------|---------|
| alespalla/chatbot_instruction_prompts | Apache-2.0 | benign (conversational) | 24,804 |
| reshabhs/SPML_Chatbot_Prompt_Injection | CC-BY-4.0 | direct_injection + benign | 15,913 |
| xTRam1/safe-guard-prompt-injection | Apache-2.0 | direct_injection + benign | 8,118 |
| TrustAIRLab/in-the-wild-jailbreak-prompts | CC-BY-NC-SA-4.0 | jailbreak | 1,002 |
| Harelix/Prompt-Injection-Mixed-Techniques-2024 | Apache-2.0 | direct_injection + benign | 987 |
| yanismiraoui/prompt_injections | Apache-2.0 | direct_injection (multilingual) | 974 |
| deepset/prompt-injections | Apache-2.0 | direct_injection + benign | 546 |
| InjecAgent (UIUC) | MIT | indirect_injection + benign | 1,054 |
| jackhhao/jailbreak-classification | MIT | jailbreak + benign | 531 |
| JailbreakBench/JBB-Behaviors | MIT | benign (FP stress test) | 200 |

*Note: Harelix data recovered from ahsanayub/malicious-prompts (original dataset removed from HuggingFace).*

### Key Design Decisions

1. **JailbreakBench Goals are labeled BENIGN** — they describe harmful topics, not injection techniques. Used as a false-positive stress test.
2. **No isolated attacker payloads** from InjecAgent — context determines injection (PromptShield insight).
3. **Benign data includes application-structured samples** — clean tool responses from InjecAgent prevent the classifier from learning "JSON format = attack."
4. **In-the-wild jailbreaks** — real DAN, persona switching, and role-play attacks collected from Reddit, Discord, and jailbreak forums.

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Deterministic unique ID: `{source}_{index}_{hash}` |
| `text` | string | Text to classify |
| `label_binary` | int | 0 (BENIGN) or 1 (ATTACK) |
| `label_category` | string | One of 4 categories |
| `label_intent` | string (nullable) | Fine-grained attack intent |
| `source` | string | Origin dataset |
| `language` | string | ISO 639-1 language code |
| `context` | string (nullable) | System prompt or user instruction |
| `metadata` | dict | Source-specific metadata |

### Splits

| Split | Samples | Purpose |
|-------|---------|---------|
| train | 37,913 | Model training (70%) |
| validation | 8,124 | Threshold calibration and model selection (15%) |
| test | 8,125 | Final evaluation (15%) |

Stratified by `label_category`, random seed 42.

## Intended Use

- Training prompt injection detection classifiers
- Benchmarking detection systems at low-FPR operating points
- Research on adversarial robustness of LLM safety filters

## Limitations

- **English-dominant**: >98% English; multilingual samples limited to 7 other languages
- **Text-only**: No multimodal or visual prompt injection
- **Synthetic benign tool responses**: Generated by stripping injections from InjecAgent
- **Static benchmark**: Does not capture evolving attack techniques
- **No multi-turn**: All samples are single-turn

## Citation

```bibtex
@software{shieldlm2026,
  author = {Milushev, Dimiter},
  title = {ShieldLM: Unified Prompt Injection Detection Dataset},
  year = {2026},
  url = {https://github.com/dvm81/shieldlm}
}
```

## License

MIT (this curation). Source datasets retain their original licenses (see table above).
Note: TrustAIRLab/in-the-wild-jailbreak-prompts uses CC-BY-NC-SA-4.0; all other sources are Apache-2.0, CC-BY-4.0, or MIT.
