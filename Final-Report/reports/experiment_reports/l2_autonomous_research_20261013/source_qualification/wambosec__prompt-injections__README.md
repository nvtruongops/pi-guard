---
license: mit
task_categories:
  - text-classification
language:
  - en
tags:
  - prompt-injection
  - security
  - llm-safety
  - classification
size_categories:
  - 1K<n<10K
---

# wambosec/prompt-injections

A dataset of prompts for training prompt injection detection models.

## Dataset Description

This dataset contains prompts labeled as either benign (normal user requests) or malicious (prompt injection attacks).

### Dataset Statistics

- **Total prompts**: 5,766
- **Benign prompts**: 2,340
- **Malicious prompts**: 3,426
- **Malicious ratio**: 59.4%

## Dataset Structure

```python
{
    "prompt": str,           # The prompt text
    "label": int,            # 0 = benign, 1 = malicious
    "is_malicious": bool,    # True if prompt injection
    "category": str | None,  # Attack category (for malicious)
    "goal": str | None,      # Attack objective (for malicious)
    "length_type": str,      # "short" or "long"
}
```

## Usage

```python
from datasets import load_dataset

dataset = load_dataset("wambosec/prompt-injections")

# Access splits
train_data = dataset["train"]
test_data = dataset["test"]

# Example
print(train_data[0])
```

## Intended Use

This dataset is intended for:
- Training prompt injection detection classifiers
- Evaluating LLM safety measures
- Security research and red-teaming

## Generation

Prompts were generated using LLMs with carefully crafted prompts to ensure diversity across:
- Multiple attack techniques (semantic camouflage, context manipulation, encoding tricks, etc.)
- Various sophistication levels (subtle to obvious)
- Different domains and topics

## License

MIT License
