# PI-Guard held-out benchmark snapshots

These folders contain external evaluation data. Keep them out of model training, validation, hyperparameter selection, and threshold calibration. Lock preprocessing and thresholds using project validation data first, then report the benchmark results with its original class/category definitions and sample counts.

| Folder | Snapshot and license | Paper provenance | Local raw rows | Intended use |
|---|---|---|---:|---|
| qualifire/ | rogue-security/prompt-injections-benchmark, revision 9ef1aa46a7e5eedb096be0481be8011ede1e72e8, CC-BY-NC-4.0 | The Hub card does not cite a separate paper | 5,000 test rows | Supplementary jailbreak/benign check; it has no PI gold label. |
| over_refusal_benchmark/ | bench-llm/or-bench, revision e36d8b80e81837c8a8f264bbb2a49f1b32c7e272, CC-BY-4.0 | OR-Bench, ICML 2025 | 80,359 / 1,319 / 655 across three CSVs | Over-refusal stress check; not a PI/JB classifier benchmark. |

The local file counts and overlaps are described in each subfolder README. OR-Bench file names and paper counts are nominal descriptions; preserve all rows from the pinned snapshot and report measured counts. Local workspace files are not a blanket permission to redistribute the data.
## Integrity manifest

[benchmark_manifest.json](benchmark_manifest.json) records pinned revisions, licenses, observed CSV rows and labels/categories, SHA-256 values, duplicate checks, and OR-Bench cross-file overlap. It contains no prompt text.