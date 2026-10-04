# Dataset provenance — JailbreakBench JBB-Behaviors

**Status 30/09/2026:** local source rows were checked against a pinned public source. This is a data-content check, not a detector benchmark.

| Split | Upstream file at pinned revision | Upstream bytes / SHA-256 | Local CSV bytes / SHA-256 | Local JSON records | Row result |
|---|---|---|---|---:|---|
| Harmful | `data/harmful-behaviors.csv` | 23,116 / `4a8ec6832056b631eb092dccc60d37a61c3d441268268888b3d006288afeffa1` | 23,217 / `f985615b17b7659a7598f751a3c1fe0704e80d4f966d6ba36b6777d53ad18150` | 100 | all fields match |
| Benign | `data/benign-behaviors.csv` | 20,570 / `3cda234d21a991fa309bbfea4b6d9dae31ccdf8e9d452424b6a983e4fdc33468` | 20,671 / `b198c96c550710bfcdb6e6b9e567003e0c7c12c94bd25c47b09412909f2a6ab2` | 100 | all fields match |

The source revision is [d8d87b8fdcb7806e3b4e45fffb2bc24aa6b17f32](https://huggingface.co/datasets/JailbreakBench/JBB-Behaviors/tree/d8d87b8fdcb7806e3b4e45fffb2bc24aa6b17f32/data). Local byte counts differ, so these are not byte-for-byte mirrors. The local CSVs parse to 100 records per split; the JSON files also match every source field/value. The comparison was performed against the pinned source with [verify_jbb_source_rows.py](../verify_jbb_source_rows.py).

The former `jbb_combined_benchmark.json` was a local derived wrapper, not an upstream file; it has been removed. The old runner classified raw behavior goals with a prompt-injection detector and called the flags “jailbreak detection.” Its result artifacts were withdrawn. No current benchmark or ASR claim is based on these files.

## Scope Boundary Declaration

- **IN-SCOPE:** preserve source-backed behavior-goal records and describe the exact row-level comparison.
- **OUT-OF-SCOPE:** infer jailbreak prompts or outcomes from behavior goals; claim byte identity; report ProtectAI flags as jailbreak success or defense effectiveness.
