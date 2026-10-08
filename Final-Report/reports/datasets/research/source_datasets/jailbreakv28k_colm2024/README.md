# JailBreakV-28K — COLM 2024

## Provenance

- Dataset: https://huggingface.co/datasets/JailbreakV-28K/JailBreakV-28k
- Pinned Hugging Face revision: f949ca582fff13d396ac8fce59596afafb2b78d3
- Official project: https://github.com/SaFo-Lab/JailBreakV_28K
- Paper: Weidi Luo, Siyuan Ma, Xiaogeng Liu, Xiaoyu Guo, and Chaowei Xiao. JailBreakV-28K: A Benchmark for Assessing the Robustness of MultiModal Large Language Models against Jailbreak Attacks. COLM 2024.
- Paper page: https://2024.colmweb.org/AcceptedPapers.html
- Open-access paper: https://arxiv.org/abs/2404.03027
- Dataset card declares MIT. Third-party content rights still need review before redistribution.

## Downloaded raw files

- JailBreakV_28K/JailBreakV_28K.csv — 28,000 benchmark rows containing text and image-related attacks.
- JailBreakV_28K/RedTeam_2K.csv — 2,000 harmful-request seed prompts. Kept for provenance; excluded from JB mapping.
- UPSTREAM_README.md — upstream dataset/project documentation captured with the snapshot.
- Luo_et_al_COLM_2024.pdf — open-access paper copy.

## JB mapping and measured text subset

For a text-only detector, use jailbreak_query only for formats Template, Persuade, and Logic. These account for 20,000 rows and 5,000 distinct prompts under Unicode NFKC, case-folding, and whitespace-collapse exact normalization. The 15,000 repeated rows are exact repeats across benchmark pairings. Assign JB from the source task meaning: these rows are attack prompts. This is a project mapping, not a native three-class label.

Exclude the 8,000 image-oriented or other-format rows from this text-only view. Do not map redteam_query or RedTeam_2K.csv to JB: they are the underlying harmful requests, not jailbreak wrappers. The overlap audit found zero exact-normalized matches between the 5,000 unique text prompts and the pre-addition base corpus. Corpus v5 selects 2,809 prompts as the JailBreakV-28K primary JB stratum; the deterministic seed is recorded in the manifest.

This benchmark was designed for attack-transfer evaluation. Since 977 prompts now contribute to the training candidate, do not report the same snapshot as an independent held-out test. Source provenance and format metadata remain in each included row.

## Status in this workspace

Raw snapshot retained separately from the combined corpus. The selected prompts are in ../../project_training/balanced_three_label.jsonl; provenance and sampling details are in ../../project_training/manifest.json and ../../project_training/audit/additional_jb_sources.md. Keep the snapshot local pending source-content rights review.
