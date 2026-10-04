# PIDS-Bench v3 Dataset Card

This folder contains the public benchmark release used by the repository.

## Included In The Public Release

- `train.csv`, `val.csv`, `test.csv`: main benchmark splits
- `eval_subsets/hard_benign_test.csv`: benign over-defense stress set
- `eval_subsets/balanced_subtype_test.csv`: subtype-balanced evaluation slice
- `eval_subsets/obfuscated_attacks.csv`: cleaned obfuscation stress set
- `ood/domain_ood.csv`, `ood/structural_ood.csv`: distribution-shift stress sets
- `FREEZE_MANIFEST.txt`: authoritative row counts and SHA-256 checksums

## Not Part Of The Public Frozen Release

These files may exist locally for research workflow support, but they are not part of the public benchmark release and should not be pushed as dataset artifacts:

- `adaptive_pilot/`: local seed selection for adaptive pilot experiments
- `eval_subsets/hard_benign_audit_sample.csv`: label-audit working sample
- `hard_negative_train.csv`, `hard_negative_val.csv`: optional training augmentation files
- `_cache_paraphrase/`, `_paraphrases/`, `eval_subsets/_staging/`: build caches and staging outputs

## Core Columns

Main split files use these columns:

- `parent_seed_id`: source family identifier for leakage and family-level analysis
- `text`: prompt text
- `label`: `0` for benign, `1` for injection
- `source`: source dataset or template origin
- `attack_type`: attack subtype label, or `none` for benign rows
- `language`: language tag
- `generator_model`: paraphrase model used during construction when applicable
- `paraphrase_round`: construction-stage paraphrase index
- `source_type`: `real` or `template`
- `obfuscation`: obfuscation transform name, or `none`

## Release Notes

- Treat `FREEZE_MANIFEST.txt` as the source of truth for public counts and checksums.
- The benchmark release is the frozen static dataset. Experimental adaptive-attack runs and local build intermediates are intentionally excluded.
