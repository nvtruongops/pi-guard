---
language:
- en
license: cc-by-4.0
pretty_name: JailbreakDB
task_categories:
- text-classification
tags:
- llm-safety
- jailbreak
- prompts
- security
configs:
- config_name: prompt_corpus
  default: true
  data_files:
  - split: jailbreak
    path: text_jailbreak_unique.csv
  - split: regular
    path: text_regular_unique.csv
---

# JailbreakDB

JailbreakDB is a large-scale prompt corpus for LLM safety and prompt-security
research. It contains two deduplicated, text-only CSV files:

- `text_jailbreak_unique.csv` (~6.6M rows): jailbreak and adversarial prompts.
- `text_regular_unique.csv` (~5.7M rows): benign prompts.

Each row stores the prompt text and lightweight source metadata. The associated
PromptSecurity evaluation measurements are maintained as a separate Hugging Face
dataset: https://huggingface.co/datasets/youbin2014/PromptSecurity-Eval.

Related resources:
- Code: https://github.com/datasec-lab/PromptSecurity
- Leaderboard: https://datasec-lab.github.io/PromptSecurityLeaderboard/

## Data Files

| Split | File | Description |
|---|---|---|
| `jailbreak` | `text_jailbreak_unique.csv` | Jailbreak and adversarial prompts. |
| `regular` | `text_regular_unique.csv` | Benign prompts. |

## CSV Field Reference

The prompt-corpus CSV files use the following fields:

| Field | Meaning |
|---|---|
| `system_prompt` | Optional system-side instruction associated with the prompt. |
| `user_prompt` | User-side prompt text. |
| `jailbreak` | Binary prompt label; `1` denotes jailbreak/adversarial prompt and `0` denotes benign prompt. |
| `source` | Source corpus or collection from which the prompt was collected. |
| `tactic` | Prompt tactic or category when available. |

## Loading

```python
from datasets import load_dataset

corpus = load_dataset("youbin2014/JailbreakDB", "prompt_corpus")
print(corpus)
```

The CSV files can also be loaded directly:

```python
from datasets import load_dataset

files = {
    "jailbreak": "hf://datasets/youbin2014/JailbreakDB/text_jailbreak_unique.csv",
    "regular": "hf://datasets/youbin2014/JailbreakDB/text_regular_unique.csv",
}
corpus = load_dataset("csv", data_files=files)
print(corpus)
```

## Paper

If you use JailbreakDB, please cite the PromptSecurity paper accepted at the
2027 IEEE Symposium on Security and Privacy (S&P / Oakland):

```bibtex
@inproceedings{hong2027sokpromptsecurity,
  title = {{SoK}: Systematizing {LLM} Prompt Security: Taxonomies, Datasets, and Unified Evaluation of Attacks and Defenses},
  author = {Hong, Hanbin and Wu, Shuang and Feng, Shuya and Naderloui, Nima and Yan, Shenao and Zhang, Jingyu and Arastehfard, Ali and Huang, Heqing and Hong, Yuan},
  booktitle = {2027 IEEE Symposium on Security and Privacy (SP)},
  year = {2027},
  note = {To appear}
}
```

## Safety Notice

This dataset may contain harmful, offensive, or disturbing prompts. It is
intended strictly for research on model safety, jailbreak robustness, defense
evaluation, and prompt-security analysis. Please review your institutional and
legal requirements before use.
