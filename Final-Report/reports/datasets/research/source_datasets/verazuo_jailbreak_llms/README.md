# verazuo/jailbreak_llms - raw GitHub snapshot

## Provenance

- Official repository: [verazuo/jailbreak_llms](https://github.com/verazuo/jailbreak_llms)
- Pinned commit: [`4f4031bf8be187f4478c7f94f42b08714722c12e`](https://github.com/verazuo/jailbreak_llms/tree/4f4031bf8be187f4478c7f94f42b08714722c12e)
- Paper: Shen et al., “Do Anything Now: Characterizing and Evaluating In-The-Wild Jailbreak Prompts on Large Language Models,” ACM CCS 2024; [DOI](https://doi.org/10.1145/3658644.3670388), [arXiv](https://arxiv.org/abs/2308.03825).
- Upstream repo license: MIT. Prompt sources include material aggregated from third parties; check source-specific rights before redistribution.

## Local snapshot and labels

The complete upstream checkout is retained in the private source workspace and was not copied here. Its four prompt CSV snapshots contain 21,527 physical rows: 19,456 regular/benign and 2,071 rows labeled jailbreak across the older and newer snapshots. The latest 2023-12-25 pair has 15,140 rows: 13,735 regular and 1,405 jailbreak. The 390-question forbidden-question set and its prompt-expanded auxiliary file are evaluation artifacts and are not included in these counts.

Native `jailbreak=true` maps to the project's JB candidate label by attack intent; `false` maps to regular/benign. This snapshot has no PI label. These labels are preserved in the source files.

## Overlap and use

An exact normalized-text audit (Unicode NFKC, casefold, whitespace collapse) found 15,064 unique prompts in this GitHub snapshot, all also present in the four local TrustAIRLab Parquet snapshots (100% overlap in both directions). It is the original distribution of the same CCS 2024 source, not an independent dataset. The two distributions disagree on labels for 43 normalized prompt groups across dated snapshots. See [cross-dataset overlap audit](../../project_training/audit/cross_dataset_overlap.md) for the comparison.

This folder is retained to preserve the requested original GitHub source and paper provenance. It is audit-only and adds no rows to the current balanced corpus v5 (raw corpus payload not copied into this report package).
