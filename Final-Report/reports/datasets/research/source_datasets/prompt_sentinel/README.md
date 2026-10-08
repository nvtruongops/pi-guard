# PromptSentinel snapshot

Source: [nuhmanpk/prompt-sentinel](https://huggingface.co/datasets/nuhmanpk/prompt-sentinel), pinned revision `f5218824e24fbb6cd383b55aee61c71b1919a6c8`. The CLI successfully read repository metadata and downloaded README plus the train, validation, and test Parquet files. Access is gated; the Hub card asks users to share contact information. This records successful access for this account, not unrestricted public access.

## Label definitions and how the card says it was assembled

The card defines `benign` to include ordinary requests and hard negatives, `jailbreak` as attempts to make the model ignore safety rules, and `injection` as attempts to override developer/system instructions. It says direct harmful requests without an override trick are `benign` for attack type and may instead be flagged in the separate `harmful` field. It reports mapping labels from 13 listed source datasets, exact normalized-text deduplication with majority-vote resolution of conflicts, and splitting by a hash of the normalized first 200 characters (`template_group`). The local proposal maps the original values to {`benign`, injection→PI, jailbreak→JB}; it does not change the saved data.

## Local snapshot audit

| Split | Rows | benign | PI | JB |
|---|---:|---:|---:|---:|
| train | 116,854 | 66,024 | 49,811 | 1,019 |
| validation | 14,335 | 8,168 | 6,056 | 111 |
| test | 14,592 | 8,266 | 6,192 | 134 |

JB is only 0.872% of train; PI:JB is 48.9:1. This is a serious three-class imbalance for JB. The train split also has 61,781/116,854 rows (`source_license=unspecified`), so license eligibility is unresolved for over half the training records.

There are snapshot/card discrepancies that must be resolved before treating the bundle as a clean training source: the three Parquet splits total 145,781 rows, 11,021 fewer than the card's claimed 156,802; the downloaded rows expose 10 primary `source_dataset` IDs and 11 IDs across `all_sources`, while the card lists 13 source datasets. The audit records these gaps without inventing missing rows.

The train labels also track source origin strongly. Of 1,019 JB rows, 606 (59.5%) come from TrustAIRLab, 297 (29.1%) from Neuralchemy, and 116 (11.4%) from ToxicChat. Of 49,811 PI rows, 30,999 (62.2%) come from jayavibhav, 10,077 (20.2%) from SPML, and 5,489 (11.0%) from S-Labs. This is not proof of leakage, but it creates a source-style confound risk: the provided template split keeps exact/template groups apart, while the same source datasets are present across splits. Report per-source results and add a source-held-out evaluation before claiming generalization to new data sources.

The audit found no exact-text or `template_group` overlap across the downloaded train/validation/test files. This verifies only those two keys in this pinned snapshot; it does not validate the original labels or prove semantic independence.

## Papers and source provenance

PromptSentinel itself has no standalone paper listed in its card. Source-paper PDFs cited by the card and the source-to-paper mapping are in [`paper/README.md`](paper/README.md) and [`metadata.json`](metadata.json). The card's arXiv:2402.13064 association for xTRam1 is mismatched: that identifier is the GLAN paper, which the xTRam1 model card describes as inspiration, not a paper for the dataset.

## Proposed component-level disposition

Do not treat the component papers as a paper for the PromptSentinel aggregate. The local Parquet rows have `source_dataset` as a primary attribution and `all_sources` as multi-source lineage. A derived component view should partition on `source_dataset`, retain `all_sources`, and quarantine any row whose contributing lineage, terms, label, or context is unresolved. Counts below are the pinned local **train** rows before cross-source deduplication; these are candidates for review, not accepted training counts.

| Primary source | Train label counts | Paper and card license | Proposed status |
|---|---:|---|---|
| `Lakera/gandalf_ignore_instructions` | 801 PI | [arXiv:2501.07927](https://arxiv.org/abs/2501.07927), MIT | PI candidate after source/hash and overlap checks. |
| `reshabhs/SPML_Chatbot_Prompt_Injection` | 10,077 PI; 2,684 benign | [arXiv:2402.11755](https://arxiv.org/abs/2402.11755), MIT | Hold for a context-aware task. This snapshot exposes only `text`; the source paper defines injection relative to a system prompt and the source card discourages training a prompt-only detector. |
| `TrustAIRLab/in-the-wild-jailbreak-prompts` | 606 JB; 10,044 benign | [arXiv:2308.03825](https://arxiv.org/abs/2308.03825), MIT | Candidate after dedup against the direct TrustAIRLab snapshot; do not count it as an independent source. |
| `lmsys/toxic-chat` | 116 JB; 7,583 benign | [arXiv:2310.17389](https://arxiv.org/abs/2310.17389), CC-BY-NC-4.0 | Non-commercial candidate only, after confirming the source jailbreak annotation matches PI-Guard's JB definition. |
| `OpenAssistant/oasst2` | 4,138 benign | [arXiv:2304.07327](https://arxiv.org/abs/2304.07327), Apache-2.0 | Benign candidate after exact/near-duplicate and source checks. |

Examples to exclude or quarantine under the current paper rule include Jayavibhav (30,999 PI + 30,782 benign train rows; `source_license=unspecified`), S-Labs (5,489 PI rows), and Neuralchemy (2,445 PI rows); the PromptSentinel card does not cite a dataset paper for those components. Their rows should not be accepted just because the aggregate lists them. After component files and their paper/license records are verified, the aggregate Parquet payload can be proposed for removal while preserving its README, metadata, revision, hashes, and discrepancy/overlap audit. No extraction or deletion has been performed.

## Use status

**Candidate only; do not use as the sole three-label training set yet.** First settle source license restrictions and the card/snapshot count/source discrepancies. Keep the supplied labels and source metadata; any later remapping or resampling needs a separate versioned preprocessing manifest. No fitting or inference was performed.
