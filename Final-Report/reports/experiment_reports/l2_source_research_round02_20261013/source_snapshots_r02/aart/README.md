---
language:
- en
dataset_info:
  features:
  - name: region_specific_topic
    dtype: string
  - name: region
    dtype: string
  - name: why_prompt_tailored_for_region
    dtype: string
  - name: medium_keyword
    dtype: string
  - name: why_prompt_harmful
    dtype: string
  - name: why_prompt_contains_instruction_keyword
    dtype: string
  - name: prompt
    dtype: string
  - name: crime
    dtype: string
  - name: use_case
    dtype: string
  splits:
  - name: train
    num_bytes: 2024893
    num_examples: 3269
  download_size: 453726
  dataset_size: 2024893
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train-*
license: cc-by-4.0
---

# AART
AART: AI-Assisted Red-Teaming with Diverse Data Generation for New LLM-powered Applications (Radharapu et al. 2023)

## Abstract
Adversarial testing of large language models (LLMs) is crucial for their safe and responsible deployment. We introduce a novel approach for automated generation of adversarial evaluation datasets to test the safety of LLM generations on new downstream applications. We call it AI-assisted Red-Teaming (AART) - an automated alternative to current manual red-teaming efforts. AART offers a data generation and augmentation pipeline of reusable and customizable recipes that reduce human effort significantly and enable integration of adversarial testing earlier in new product development. AART generates evaluation datasets with high diversity of content characteristics critical for effective adversarial testing (e.g. sensitive and harmful concepts, specific to a wide range of cultural and geographic regions and application scenarios). The data generation is steered by AI-assisted recipes to define, scope and prioritize diversity within the application context. This feeds into a structured LLM-generation process that scales up evaluation priorities. Compared to some state-of-the-art tools, AART shows promising results in terms of concept coverage and data quality.

## This repository
This repository contains the demonstration dataset described in [the paper](https://arxiv.org/abs/2311.08592).

## Citation
If you find this dataset useful, please cite the following paper:
```
@inproceedings{radharapu-etal-2023-aart,
    title = "{AART}: {AI}-Assisted Red-Teaming with Diverse Data Generation for New {LLM}-powered Applications",
    author = "Radharapu, Bhaktipriya  and
      Robinson, Kevin  and
      Aroyo, Lora  and
      Lahoti, Preethi",
    editor = "Wang, Mingxuan  and
      Zitouni, Imed",
    booktitle = "Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing: Industry Track",
    month = dec,
    year = "2023",
    address = "Singapore",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.emnlp-industry.37",
    doi = "10.18653/v1/2023.emnlp-industry.37",
    pages = "380--395",
    abstract = "Adversarially testing large language models (LLMs) is crucial for their safe and responsible deployment in practice. We introduce an AI-assisted approach for automated generation of adversarial evaluation datasets to test the safety of LLM generations on new downstream applications. We call it AART AI-assisted Red-Teaming - an automated alternative to current manual red-teaming efforts. AART offers a data generation and augmentation pipeline of reusable and customizable recipes that reduce significantly human effort and enable integration of adversarial testing earlier in new product development. AART generates evaluation datasets with high diversity of content characteristics critical for effective adversarial testing (e.g. sensitive and harmful concepts, specific to a wide range of cultural and geographic regions and application scenarios). The data generation is steered by AI-assisted recipes to define, scope and prioritize diversity within a new application context. This feeds into a structured LLM-generation process that scales up evaluation priorities. This provides transparency of developers evaluation intentions and enables quick adaptation to new use cases and newly discovered model weaknesses. Compared to some of the state-of-the-art tools AART shows promising results in terms of concept coverage and data quality.",
}
```