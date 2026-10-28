# L2 source qualification and source-held-out experiment — round 18

## Scope Boundary Declaration

This report covers English-only L2 data qualification, versioned train/validation packages, complete L2 train/validation fits, and train-only family-held-out OOF. It does not analyze, train, evaluate, or invoke L3 or the cascade. It does not open any final-test row, text, identifier, or payload; package manifests retain only the pre-existing family-level test contract. No smoke task or shortened fit ran. Outputs are local/private and were not committed or published.

## Research question

Round12 showed that round07's seven benign and ten jailbreak training families all came from TrustAIR, while PI was dominated by TensorTrust. Round17 audited possible additions but had not finished the LLMail-Inject audit. This round asks whether adding one separately authored benign source and validating on publisher-held-out benign, PI-attempt, and manual jailbreak-attempt cohorts improves L2 evidence.

## Source qualifications and limits

| Source | Pinned role and screened rows | Reference mapping | Remaining limit |
| --- | --- | --- | --- |
| Databricks Dolly 15k | Pinned `databricks/databricks-dolly-15k` train JSONL; 15,011 total. 10,354 instruction-only candidates survived context, conservative attack/harm-intent, PII-pattern, exact-duplicate, and round07-overlap filters; 8 more exact overlaps with the new validation set were excluded from package B, leaving 10,346 added train rows. | Human-authored instruction, treated as provisional benign reference. Dataset categories are not safety labels. | One source family only. Regex screening is incomplete, and lack of adversarial phrases does not establish benign intent or complete privacy clearance. The card declares CC-BY-SA-3.0; attribution is carried in private package evidence. [Dataset card](https://huggingface.co/datasets/databricks/databricks-dolly-15k). |
| OpenAssistant OASST1 | Pinned train parquet; 84,437 messages, 3,482 English root prompter messages. Excluded 1,377 with positive native moderation labels, two with configured privacy-pattern matches, eight exact overlaps with round07, and six within-source duplicates; 2,089 unique rows remain. | English root prompter message without positive native review flags, provisional benign reference. | A root user message is not proof of benign intent; absent review flags are not positive safety adjudication. Privacy screening is incomplete. The card declares Apache-2.0. [Dataset card](https://huggingface.co/datasets/OpenAssistant/oasst1). |
| Microsoft LLMail-Inject | Pinned labelled-unique Phase 1/2 only: 148,383 native `attack_attempt=true`; 138,383 hit at least one configured privacy pattern; 10,000 had no configured hit; 7,737 were English at confidence >=0.95; after 206 normalized duplicate groups/246 duplicate rows, 7,491 unique rows remain. Zero exact overlap with round07 and no cross-phase duplicate after the filters. Raw submissions and `emails_for_fp_tests.jsonl` were not requested. | Native attack-attempt boolean, treated as provisional PI-attempt reference in this email/tool-use challenge. | The export has no participant/team/family key; hold all rows as one family. Challenge-specific indirect injection is not all PI. Regex screening is not a full privacy review, and attempt metadata is not curator-reviewed PI-Guard gold. Dataset card declares MIT and the challenge has separate submission terms. [Dataset card](https://huggingface.co/datasets/microsoft/llmail-inject-challenge). |
| JailbreakBench JBC/manual | Pinned `JailbreakBench/artifacts` revision; one manual GPT-4 artifact file was used. It has 100 unique prompts across 100 behavior-ancestry keys, zero configured PII-pattern hits, and zero exact overlap with round07. The four model files represented 400 occurrences of the same 100 normalized prompts; the other three files were not copied into package validation. Test-artifact paths and `evaluation.json` remained unopened. | `attack_method=JBC/manual`, treated as provisional JB-attempt reference; attack-success outcome is not the input label. | One family of 100 prompts, no prevalence inference, and regex screening is incomplete. It is separately packaged by JBB but comes from the JailbreakChat community, which also appears in TrustAIR/JailbreakHub; it therefore does not establish independent community-origin generalization. JBB declares MIT for artifacts. [Artifacts](https://github.com/JailbreakBench/artifacts), [benchmark paper](https://arxiv.org/abs/2404.01318). |

The 655-prompt “Human Mark in the Wild” lead was rejected for independent-source evidence: its own methods describe it as derived from Shen et al. (2023), the same underlying in-the-wild collection lineage represented by TrustAIR/JailbreakHub. A different repository or annotation layer does not create a new source lineage. [Corpus methods](https://gyrogovernance.com/docs/tools/The_Human_Mark/THM_InTheWild/), [Shen et al.](https://arxiv.org/abs/2308.03825).

## Frozen round18 package design

Two isolated private packages share the same validation rows and fixed model configuration:

| Package | Train | Validation | Purpose |
| --- | ---: | ---: | --- |
| `pi_guard_l2_source_heldout_round18_r01` | 115,953: unchanged round07 train | 9,680: OASST1 benign 2,089; LLMail PI-attempt 7,491; JBB JBC/manual JB-attempt 100 | External-source diagnostic comparator; round07 validation rows are excluded. |
| `pi_guard_l2_source_heldout_dolly_aug_round18_r01` | 126,299: same round07 train plus 10,346 Dolly benign rows | The same 9,680 source-held-out validation rows | One preselected data-addition experiment. |

The validation cohorts have one source family per class; training has respectively 7/8 benign, 2,317 PI, and 10 JB families. Exact normalized cross-source duplicates and cross-label conflicts among the new validation candidates were zero. Package-builder checks also remove exact overlap with round07 train/validation. Similarity screening and human intent/privacy adjudication are still incomplete; row-level references remain provisional. Both packages passed the adapter's complete metadata/hash/family preflight with `READY_FOR_FIT`; preflight opened no row payload. Their official status remains `GATE_UNSPECIFIED`.

## Complete L2 results

Both fits use the unchanged dual-TF-IDF + balanced Logistic Regression C=2 configuration, full train rows, and full 9,680-row validation. No threshold was selected by the current exploratory sweep.

| Measure | Package A: round07 train | Package B: + Dolly | Change |
| --- | ---: | ---: | ---: |
| Validation macro-F1 | 0.4631 | 0.5159 | +0.0528 |
| Accuracy | 0.4195 | 0.4150 | -0.0045 |
| Benign FPR | 82.14% (1,716/2,089) | 10.77% (225/2,089) | -71.37 pp |
| Benign F1 / recall | 0.1184 / 0.1786 | 0.3998 / 0.8923 | higher |
| PI F1 / recall | 0.5617 / 0.4790 | 0.4207 / 0.2741 | lower |
| JB F1 / recall | 0.7092 / 1.0000 | 0.7273 / 1.0000 | small increase; n=100 |
| Local batch-one P95 | 8.95 ms | 8.90 ms | similar local diagnostic |
| Adapter status / selected pair | `NOT_READY` / none | `NOT_READY` / none | no local diagnostic pair |

The Dolly augmentation improves the OASST benign metric but transfers a large portion of errors to the LLMail PI cohort. That class trade-off means the macro-F1 gain is not a stable, all-class improvement. The 100 JBB prompts provide only a small, single-family JB diagnostic.

### Full five-fold family OOF for package B

The round07 five-fold OOF is a valid package-A comparator because A reuses exactly the same round07 train rows, source-family groups, baseline config, and five-fold seed. Package A's existing pooled OOF macro-F1 was 0.8225 and benign FPR 11.75% over 115,953 rows.

Package B completed a full five-fold `StratifiedGroupKFold` OOF over all 126,299 train rows. Pooled macro-F1 was 0.6431, benign FPR 72.40%, benign recall 27.60%, PI recall 98.06%, and JB recall 80.54%. Fold macro-F1 / benign FPR were: F1 0.4694 / 96.24%; F2 0.7205 / 24.35%; F3 0.6265 / 6.45%; F4 0.7553 / 10.92%; F5 0.6566 / 47.78%.

The high-variance fold results expose the source-family limitation: the added Dolly corpus is one large benign family, so a held-out-family fold removes all Dolly examples from training and its held-out benign rows are almost entirely flagged. The favorable OASST validation FPR and poor pooled/fold OOF evidence do not support retaining this single-source augmentation as a robust L2 candidate. The OOF result remains family-held-out evidence, not source-independent generalization.

## Readiness decision and next L2 work

**Round18 does not pass L2.** Both full fits are `NOT_READY`; neither selects an exploratory operating point. The official owner gate remains `GATE_UNSPECIFIED`, so no local diagnostic threshold can establish formal PASS. Source rights are scoped to private local research only, and label/privacy reviews are screening-level rather than canonical/human clearance.

Reject package B as a retained candidate, while preserving it as a reproducible negative/diagnostic experiment. Do not tune additional parameters against this same validation. The next evidence that could change readiness is a second independent, privacy-screened benign collection for train plus a non-TrustAIR, non-synthetic human-authored JB-attempt collection with explicit provenance and rights; its validation/source families must be held out before fit. The exact official L2 rubric and owner-level decisions remain missing.

No L3, cascade, smoke, final-test payload, commit, or publication was used. The sealed test remains represented only by the original family-level metadata contract.
