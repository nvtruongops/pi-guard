# JailbreakBench JBB-Behaviors — local source snapshot

## Source and verification

The upstream dataset repository is [JailbreakBench/JBB-Behaviors](https://huggingface.co/datasets/JailbreakBench/JBB-Behaviors). This workspace pins the two source CSVs at revision [d8d87b8fdcb7806e3b4e45fffb2bc24aa6b17f32](https://huggingface.co/datasets/JailbreakBench/JBB-Behaviors/tree/d8d87b8fdcb7806e3b4e45fffb2bc24aa6b17f32/data).

The local CSV files are serialized copies and their bytes do **not** match the upstream files. A field-by-field comparison against the pinned CSVs found 100/100 equal records in each split; the local JSON files contain the same fields and values. Run [verify_jbb_source_rows.py](../verify_jbb_source_rows.py) to repeat that source check. Local size and SHA-256 values are recorded in [METADATA.json](./METADATA.json).

## Interpretation

The records describe harmful and benign **behavior goals**. They are not jailbreak prompt artifacts, outcomes from a victim model, or evidence of attack success. Using a prompt-injection detector to flag these goals does not measure JailbreakBench ASR or jailbreak defense effectiveness.

The former local combined JSON was a project-created wrapper and has been removed. The former ProtectAI-on-goals result and runner were withdrawn because their task/model semantics did not support the reported jailbreak claims. The source snapshots remain available for reference only.
