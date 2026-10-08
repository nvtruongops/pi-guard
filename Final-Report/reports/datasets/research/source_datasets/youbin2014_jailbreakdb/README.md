# youbin2014/JailbreakDB - raw Hugging Face snapshot

## Provenance

- Dataset card: [youbin2014/JailbreakDB](https://huggingface.co/datasets/youbin2014/JailbreakDB)
- Pinned revision: [`63912b8f9e66e87d8fdffde340391b79503c8e0d`](https://huggingface.co/datasets/youbin2014/JailbreakDB/tree/63912b8f9e66e87d8fdffde340391b79503c8e0d)
- Declared dataset license: CC-BY-4.0.
- Paper: Hong et al., “SoK: Taxonomy and Evaluation of Prompt Security in Large Language Models,” [arXiv:2510.15476](https://arxiv.org/abs/2510.15476). The Hugging Face README at this revision says the paper was accepted at IEEE S&P 2027 “to appear.” Since that venue is future-dated relative to this audit (2026-10-07), the local record treats the available paper as an arXiv preprint and records the venue statement without presenting proceedings as already published.

## Files and verified row counts

Raw files and the upstream README are retained under [`raw_snapshot/`](raw_snapshot/). File SHA-256 values and row counts are in [`metadata.json`](metadata.json). Parsed with Python `csv.DictReader` at the pinned revision:

| File / native split | CSV records | Unique normalized `user_prompt` | Native label meaning | PI-Guard mapping now |
|---|---:|---:|---|---|
| `text_regular_unique.csv` | 1,094,122 | 1,088,959 | `jailbreak=0`, regular | Benign candidate |
| `text_jailbreak_unique.csv` | 445,752 | 439,517 | `jailbreak=1`, jailbreak/adversarial | JB candidate, not PI |
| **Total** | **1,539,874** | **1,528,462** | 14 normalized user-prompt groups occur under both native labels | - |

The README's approximate “6.6M” and “5.7M” figures align with the files' physical newline counts (6,565,678 and 5,651,873). Python `csv.DictReader` and DuckDB both count the lower totals in the table as logical CSV records. Prompt fields contain embedded line breaks, so physical lines are not dataset records. Both downloaded files match the SHA-256 LFS hashes at the pinned revision.

The rows also contain `system_prompt`, `user_prompt`, `source`, and `tactic`. The SoK paper describes JailbreakDB's positive set as jailbreak system–user prompt pairs; that supports mapping `jailbreak=1` to a **JB candidate** under PI-Guard's label taxonomy. It does not support a PI label: the files have no separate PI class. This is a source-level mapping proposal, not confirmation that every positive row is ready for the corpus.

## Duplicate and label-overlap audit

Normalization is Unicode NFKC, casefold, and whitespace collapse. Across all locally audited snapshots, JailbreakDB shares 15,064 unique `user_prompt` values with TrustAIRLab and its original GitHub distribution; that is 100% of the TrustAIRLab unique set and 0.99% of JailbreakDB's unique user prompts. It also shares 14,348 with PromptSentinel, 6,457 with PromptScreen, and 5,618 with ShieldLM. Fourteen normalized user prompts appear under both native JailbreakDB labels. For a prompt-only classifier, inspect these conflicts and either use available system context to adjudicate them or exclude unresolved groups; deduplicate against other sources before sampling. Some regular rows overlap other snapshots with a non-benign label and also need review. The [full overlap report](../../project_training/audit/cross_dataset_overlap.md) has per-source counts and label-conflict totals.

This source remains outside the current corpus pending context, conflict, license, and overlap review. Its 445,752 positive rows are JB candidates and its 1,094,122 regular rows are Benign candidates; neither set is PI-Guard-validated. No JailbreakDB row was added to balanced_three_label.jsonl (payload not copied into this report package); see the [version log](../../project_training/DATASET_VERSION_LOG.md).
