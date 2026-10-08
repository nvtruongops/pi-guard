# ShieldLM source papers and attribution

The dataset card cites ShieldLM as software (`https://github.com/dvm81/shieldlm`); it does not identify a dataset-specific peer-reviewed paper. The rationale below follows the dataset card, while source papers provide background for source datasets and are not evidence that the ShieldLM aggregation labels were independently validated.

| Source | Paper / primary source | Labeling relevance |
|---|---|---|
| TrustAIRLab in-the-wild jailbreaks | [arXiv:2308.03825](https://arxiv.org/abs/2308.03825) | Real jailbreak prompts; ShieldLM maps them to jailbreak. |
| SPML | [arXiv:2402.11755](https://arxiv.org/abs/2402.11755) | Prompt-injection source; supports source context, not the aggregated four-label curation. |
| JailbreakBench | [Project and dataset](https://jailbreakbench.github.io/) | ShieldLM labels harmful-goal prompts benign when they describe goals rather than attack techniques. |
| InjecAgent | [Project repository](https://github.com/uiuc-kang-lab/InjecAgent) | Indirect injection needs the surrounding tool/application context. |

The card's sources table and its stated source count differ in granularity: the card says 11 datasets, while the Parquet source field contains 13 distinct strings, including several InjecAgent configurations. See `../metadata.json` and `../source_snapshot/README.md` for pinned source details.
