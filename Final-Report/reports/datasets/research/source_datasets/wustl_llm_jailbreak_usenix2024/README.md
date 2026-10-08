# WUSTL-CSPL/LLMJailbreak — USENIX Security 2024

## Provenance

- Official repository: https://github.com/WUSTL-CSPL/LLMJailbreak
- Pinned repository revision: 2a9e665769de1bbfa657b6e6a9f88d9d427bc57c
- Paper: Zhiyuan Yu et al. Don’t Listen To Me: Understanding and Exploring Jailbreak Prompts of Large Language Models. 33rd USENIX Security Symposium, 2024.
- Paper page: https://www.usenix.org/conference/usenixsecurity24/presentation/yu-zhiyuan
- Open-access paper: https://www.usenix.org/system/files/usenixsecurity24-yu-zhiyuan.pdf
- The repository license file declares MIT. Individual online prompt origins are not traced per row.

## Downloaded raw files

- JailbreakPrompts.xlsx — the paper artifact identifies 448 jailbreak prompts in this workbook.
- LICENSE — upstream repository license.
- UPSTREAM_README.md — repository documentation.
- Yu_et_al_USENIX_Security_2024.pdf — published paper copy.

The upstream repository also describes 161 malicious-query seeds and separate response/annotation files. They are not part of the downloaded workbook snapshot used here. Do not classify those seed requests as JB: they are harmful goals without jailbreak wrappers.

## JB mapping and measured overlap

Use the workbook Prompt column as JB attack attempts. It contains 448 rows and 447 unique prompts after Unicode NFKC, case-folding, and whitespace-collapse exact normalization. Against the historical pre-addition base corpus, 180 unique prompts match exactly: 178 already have JB labels and have their WUSTL provenance merged; 2 conflict with the existing benign/PI mapping. In v5, 1,573 rows are selected in the combined TrustAIRLab+WUSTL primary JB stratum; 437 selected rows have WUSTL provenance after exact-text source merging.

Keep the source and prompt-family metadata in the corpus. These human-collected prompts can contain multiple strategies or long role-play contexts.

## Status in this workspace

Raw snapshot retained separately from the combined corpus. The prompts are represented in ../../project_training/balanced_three_label.jsonl; provenance and overlap details are in ../../project_training/manifest.json and ../../project_training/audit/additional_jb_sources.md. Keep local pending source-content rights review.
