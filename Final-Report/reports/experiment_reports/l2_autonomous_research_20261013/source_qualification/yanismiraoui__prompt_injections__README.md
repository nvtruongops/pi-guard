---
license: apache-2.0
annotations_creators:
- no-annotation
language:
- en
- fr
- de
- es
- pt
- it
- ro
multilinguality:
- multilingual
source_datasets:
- original
tags:
- prompt
- prompt injection
- jailbreak
- prompt leaking
- mode switching
---

# Dataset Card for Prompt Injections by <a  style="display: inline;"  href="https://yanismiraoui.github.io/"> Yanis Miraoui </a> 👋

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
- [Considerations for Using the Data](#considerations-for-using-the-data)
  - [Prompts to handle with care](#prompts-to-handle-with-care)
)

## Dataset Description

This dataset of prompt injections enriches Large Language Models (LLMs) by providing task-specific examples and prompts, helping improve LLMs' performance and control their behavior.

### Dataset Summary

This dataset contains over 1000 rows of prompt injections in multiple languages. It contains examples of prompt injections using different techniques such as: prompt leaking, jailbreaking, and mode switching. 

### Languages

The text in the dataset is in English, French, German, Spanish, Italian, Portuguese and Romanian.

## Dataset Structure

It consists of one column with the prompt injections examples.

## Considerations for Using the Data

### Prompts to handle with care

This dataset of prompts has to be handled with care as it contains examples of prompts meant to harm, mislead or jailbreak LLMs. The goal of this dataset is to mainly help better finetune and control LLMs.