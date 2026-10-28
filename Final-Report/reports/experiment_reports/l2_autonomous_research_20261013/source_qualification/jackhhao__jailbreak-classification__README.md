---
license: apache-2.0
task_categories:
- text-classification
language:
- en
tags:
- jailbreak
- security
- moderation
pretty_name: Jailbreak Classification
size_categories:
- 10K<n<100K
configs:
- config_name: default
  data_files:
  - split: train
    path: "balanced/jailbreak_dataset_train_balanced.csv"
  - split: test
    path: "balanced/jailbreak_dataset_test_balanced.csv"
---

# Jailbreak Classification

### Dataset Summary

Dataset used to classify prompts as jailbreak vs. benign.

## Dataset Structure

### Data Fields

- `prompt`: an LLM prompt
- `type`: classification label, either `jailbreak` or `benign`

## Dataset Creation

### Curation Rationale
Created to help detect & prevent harmful jailbreak prompts when users interact with LLMs.

### Source Data

Jailbreak prompts sourced from: <https://github.com/verazuo/jailbreak_llms>

Benign prompts sourced from:
- [OpenOrca](https://huggingface.co/datasets/Open-Orca/OpenOrca)
- <https://github.com/teknium1/GPTeacher>