# What Features in Prompts Jailbreak LLMs? — BlackboxNLP 2025

## Provenance

- Dataset file: https://huggingface.co/datasets/sevdeawesome/jailbreak_success
- Pinned dataset revision: 12bad235ee184287bc5f41ec2341489501a30049
- Official paper/code repository: https://github.com/NLie2/what_features_jailbreak_LLMs
- Pinned repository revision for the captured README: 8b23d26deebe5c5428af9333c880af8ed4c70ea2
- Published paper: Nathalie Maria Kirch, Constantin Niko Weisser, Severin Field, Helen Yannakoudakis, and Stephen Casper. What Features in Prompts Jailbreak LLMs? Investigating the Mechanisms Behind Attacks. Proceedings of the 8th BlackboxNLP Workshop, ACL, 2025, pp. 480–520.
- Official publication: https://aclanthology.org/2025.blackboxnlp-1.28/
- DOI: https://doi.org/10.18653/v1/2025.blackboxnlp-1.28
- HF dataset card declares MIT. The paper describes the source as 300 harmful prompts transformed by 35 attack methods. Keep the original prompt and attack method metadata.

## Downloaded raw files

- latest.csv — 10,800 rows and four columns: prompt_name, jailbreak_prompt_name, jailbreak_prompt_text, original_prompt_text.
- HF_DATASET_CARD.md — the pinned Hugging Face card content; it declares the MIT license.
- UPSTREAM_README.md — captured from the official GitHub repository.
- GITHUB_REVISION.txt — GitHub revision used for that README.
- Kirch_et_al_BlackboxNLP_2025.pdf — ACL Anthology paper copy.

The CSV has 300 distinct base prompt IDs and 35 distinct attack method names. It contains 9,884 unique jailbreak_prompt_text values after Unicode NFKC, case-folding, and whitespace-collapse exact normalization; 916 rows repeat an exact normalized attack prompt.

## JB mapping and limitations

Use jailbreak_prompt_text as the JB attack attempt. Do not use original_prompt_text as JB: it is the underlying harmful request seed, not the jailbreak transformation. The published work studies whether attempts succeeded against target models, but this released CSV has no attack-outcome column. The project label therefore means attack intent regardless of whether the attack succeeded.

The 35 attack methods are applied to only 300 base requests. Keep prompt_name and jailbreak_prompt_name as grouping metadata for any later evaluation split. The exact-normalized overlap audit found no matches with the pre-addition base corpus or the other two newly audited sources. Corpus v5 selects 2,809 prompts as the WhatFeatures primary JB stratum; the deterministic seed is recorded in the manifest.

## Status in this workspace

Raw snapshot retained separately from the combined corpus. The selected prompts are in ../../project_training/balanced_three_label.jsonl; provenance and sampling details are in ../../project_training/manifest.json and ../../project_training/audit/additional_jb_sources.md. Keep local pending review of the base-prompt lineage and third-party content rights.
