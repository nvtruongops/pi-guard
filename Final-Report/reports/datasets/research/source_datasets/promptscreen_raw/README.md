# PromptScreen raw data snapshot

Upstream: [dronefreak/PromptScreen](https://github.com/dronefreak/PromptScreen), commit `496653aba7a39ae6bdcb775c067a3bdb2471acc7`. The two raw JSON files and [arXiv v1 paper](https://arxiv.org/abs/2512.19011v1) are stored in this folder; file URLs, byte sizes and SHA-256 hashes are in [`metadata.json`](metadata.json) and [`download_manifest.json`](download_manifest.json).

## Corpus v5 use status

The source contributes to the local source-stratified candidate corpus using only `metrics_train_set.json`; `metrics_test_set.json` remains excluded from that corpus. After source-conflict filtering, the primary sampling quotas are 6,667 benign, 1,953 prompt-injection, and 2,809 jailbreak examples. Exact duplicate rows retain all source references in the corpus. The paper citation is pinned to arXiv v1 because the unversioned record has since changed.

The stored paper is an arXiv preprint; no peer-reviewed venue has been verified. The repository code license does not establish a license for every aggregated prompt, and the raw rows lack row-level component provenance. Keep this use local and confirm source terms before formal training claims or redistribution. The held-out file here must also stay out of any PromptScreen-specific training/evaluation reproduction.

## Paper's three labels

Section 3.3 calls the classes mutually exclusive: **benign**, **jailbreak** (trying to coerce policy violation/prohibited content), and **prompt-injection** (manipulating system/application instructions, tools, or downstream execution). It reports source annotations plus rule-based validation and manual verification. The paper describes over 30,000 prompts and says no prompt appears in more than one split.

## Audit of the downloaded JSON

| File | Rows | benign | jailbreak | prompt-injection |
|---|---:|---:|---:|---:|
| train | 28,771 | 9,426 | 17,392 | 1,953 |
| reported test | 2,166 | 710 | 1,309 | 147 |

Local normalized exact-text audit (NFKC, case-fold, whitespace collapse) found **9 distinct prompts shared across the two files**: 10 train rows and 9 test rows. These matches have the same labels (8 jailbreak, 1 benign). The train file also has 99 repeated rows after normalization. This conflicts with the paper's no-overlap statement for the downloaded files; keep this split out of leakage-free evaluation until the authors' split protocol is reconciled.

The JSON rows expose only `classification`, `prompt`, and `type`, without source dataset identifiers. The original component-level provenance and applicable licenses therefore cannot be verified row by row from these files. The [repository's classifier training code](https://raw.githubusercontent.com/dronefreak/PromptScreen/496653aba7a39ae6bdcb775c067a3bdb2471acc7/src/promptscreen/defence/train/train_classifier.py) maps `prompt-injection` into the binary `jailbreak` class for that classifier; do not infer a published three-class model checkpoint from the paper's three-label dataset.

No training or inference was run.
