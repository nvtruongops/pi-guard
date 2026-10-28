---
license: mit
language:
- en
tags:
- Jailbreak
- PromptInjection
- RedTeaming
- JailbreakingPrompts
- ChatGPT
- Jailbreaking
- LLM
pretty_name: Jailbreaking prompts
configs:
- config_name: default
  data_files:
  - split: Dataset_1
    path: data/Dataset1/*
  - split: Dataset_2
    path: data/Dataset2/*
---


# Independent Jailbreak Datasets for LLM Guardrail Evaluation

**Constructed for the thesis**:  
_“Contamination Effects: How Training Data Leakage Affects Red Team Evaluation of LLM Jailbreak Detection”_

The effectiveness of LLM guardrails is commonly evaluated using open-source red teaming tools. However, this study reveals that **significant data contamination** exists between the training sets of binary jailbreak classifiers (ProtectAI, Katanemo, TestSavantAI, etc.) and the test prompts used in state-of-the-art red teaming tools (Garak, PyRIT, Giskard, etc.). On average, over **65%** of red team evaluation prompts were also present in the training data of the tested classifiers. This contamination can lead to significantly inflated performance metrics for these jailbreak classifiers and other LLM guardrails.

To address this, we present two datasets consisting of independent jailbreak prompts curated to enable **contamination-free evaluation** of binary jailbreak classifiers and other LLM guardrails. All prompts have been filtered to ensure **no overlap** with the training data of widely used jailbreak classifiers. This allows for a more accurate assessment of a classifier’s generalization capabilities.


## Dataset Overview

- **Dataset 1 – Filtered High-Quality Prompts**  
  A manually selected and filtered set of structurally diverse and high-quality jailbreak prompts.

- **Dataset 2 – Broad Coverage Prompts**  
  A larger, more inclusive, non-filtered dataset constructed to mitigate selection bias. 

---

## Prompt Sources

- [Nannanzi/evaluation_jailbreak_unsafe](https://huggingface.co/datasets/Nannanzi/evaluation_jailbreak_unsafe)  
- [weijiejailbreak/r1-1776-jailbreak](https://huggingface.co/datasets/weijiejailbreak/r1-1776-jailbreak)  
- [Bravansky/compact-jailbreaks](https://huggingface.co/datasets/Bravansky/compact-jailbreaks)  
- [allenai/tulu-3-trustllm-jailbreaktrigger-eval](https://huggingface.co/datasets/allenai/tulu-3-trustllm-jailbreaktrigger-eval)  
- [tridm/jailbreak_test_v1.0](https://huggingface.co/datasets/tridm/jailbreak_test_v1.0)  
- [Mindgard/evaded-prompt-injection-and-jailbreak-samples](https://huggingface.co/datasets/Mindgard/evaded-prompt-injection-and-jailbreak-samples)  
- Reddit – [r/ChatGPTJailbreak](https://www.reddit.com/r/ChatGPTJailbreak)  
- GitHub – Various jailbreak-related repositories  
- Public articles and jailbreak write-ups

---