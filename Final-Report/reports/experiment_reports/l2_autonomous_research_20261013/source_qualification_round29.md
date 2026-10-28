# Round 29 — NeurAlchemy original attack_db JB component and L2 diagnostics

## Scope Boundary Declaration

This round qualifies one pinned, single-prompt JB-reference component, builds a private train-only L2 successor, and runs one fixed-config train/validation fit plus complete five-fold source-family OOF. Labels remain provisional; the formal acceptance rubric remains `GATE_UNSPECIFIED`. No threshold was selected. PI-Guard test payload, L3/cascade, smoke, commit, and publication stayed out of scope.

## Source, label, rights, lineage, and privacy

The audit used only `neuralchemy/Prompt-injection-dataset` revision `7d70432dfcf47a821612cbf9d34e9d9e3ad20e75`, `core/train`. The pinned publisher card assigns Apache-2.0 to its `neuralchemy_v1 original attack_db` component and describes the dataset's mixed source components; the card does not provide row-level license values or resolve record-level upstream authorship. The retained prompts therefore remain private, non-redistributive research references pending owner review. [Pinned NeurAlchemy dataset card](https://huggingface.co/datasets/neuralchemy/Prompt-injection-dataset/tree/7d70432dfcf47a821612cbf9d34e9d9e3ad20e75)

The source audit found 2,568 records in the component, of which 124 were explicitly `category=jailbreak`, native binary label `1`, and `augmented=false`. The binary malicious label alone was not mapped to JB. The observation is one prompt field per original train record; multi-turn categories and all other components were excluded. The publisher component supplies one source family, not 124 independent examples or 124 independent sources.

| Aggregate screen | Result |
| --- | ---: |
| Explicit jailbreak candidates | 124 |
| Exact duplicates collapsed within candidates | 0 |
| Exact overlap with baseline train / validation | 0 / 0 |
| Near-duplicate overlap with baseline train / validation | 0 |
| Within-source near-duplicate candidates excluded | 10 |
| Configured privacy-pattern hits | 0 |
| Retained unique train candidates / prompt groups | 114 / 114 |

Configured email, SSN, phone-candidate, IPv4, credential-assignment, private-key, and bearer-token patterns were screened. The screen is incomplete and is not human privacy clearance. Source component membership is traceable to the pinned train shard, but deeper upstream ancestry and human authorship are undocumented. The native `jailbreak` category is used only as a provisional JB-attempt reference, not as canonical PI-Guard gold. Source validation/test and PI-Guard test payloads were not opened. Aggregate evidence is in [R29 source audit](neuralchemy_jb_component_audit_round29.json); private candidate rows remain under `workspaces/truongnv/pi_guard_pipeline/training_bases/datasets/source_audit/neuralchemy_jb_round29/`.

## Package and full validation fit

The private package `pi_guard_l2_neuralchemy_jb_round29_candidate_20261014` (version `0.8.13-r29-neuralchemy-jb-provisional`) adds the 114 rows as one family to the R27 clean-validation baseline. It contains 140,543 train rows and 9,656 validation rows. Validation is byte-identical to R27, with 76 JB validation rows; this remains below the protocol's 100-row diagnostic-support floor. The approved family-only test metadata contract is unchanged. Preflight returned `READY_FOR_FIT` with no row payloads opened; the first attempt used an invalid output location and was blocked before fit.

The complete baseline-config fit used train rows and hard argmax predictions on the shared validation partition. There was no cutoff selection.

| Validation | Macro-F1 | Accuracy | Benign FPR | JB precision | JB recall | JB F1 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| R27 clean-validation baseline | 0.4419 | 0.4562 | 0.3011 | 0.3193 | 0.6974 | 0.4380 |
| R29 NeurAlchemy JB candidate | 0.2920 | 0.3652 | 0.2877 | 0.0722 | 0.6579 | 0.1300 |

Macro-F1 fell by 0.1499 and JB F1 by 0.3079. Benign FPR improved by 0.0134, but the candidate predicted many non-JB validation prompts as JB, reducing JB precision to 0.0722. Reject this augmentation as a validation improvement.

## Five-fold family-held-out OOF

The full OOF used only frozen train rows. Each source family, collection lineage, prompt family, and duplicate group was held out by the shared runner. Validation and test payloads were not used.

| Train-only OOF | Macro-F1 | Benign FPR | JB precision | JB recall | JB F1 |
| --- | ---: | ---: | ---: | ---: | ---: |
| R05 historical comparator | 0.7638 | 0.3086 | 0.4162 | 0.8337 | 0.5552 |
| R29 NeurAlchemy JB candidate | 0.7483 | 0.3166 | 0.3947 | 0.7395 | 0.5146 |

R29 has 11 JB families after adding this component, but the added data contributes only one publisher-defined family. Fold macro-F1 was 0.5892, 0.8367, 0.6953, 0.6623, and 0.7258; benign FPR was 0.5022, 0.0814, 0.3277, 0.5309, and 0.1821. The fold spread and imperfect source independence limit generalization claims. See the [validation result](l2_neuralchemy_jb_round29_candidate_fit_20261014.json) and [OOF result](l2_neuralchemy_jb_family_oof_round29.json); full fit outputs remain private.

## Decision and next research

Reject R29 as a model improvement and do not reuse it for parameter tuning. Its validation and pooled OOF metrics regress against R05/R27 comparators, and the 76-row JB validation support is too small for a confident class-level conclusion. The source improves nominal JB family count but does not close independent upstream lineage, row-level rights, human privacy, or owner-review gaps. Continue first-party metadata qualification for a genuinely independent, single-turn JB train source. Keep the official gate `GATE_UNSPECIFIED`; these diagnostic results cannot establish L2 PASS.

No test payload was opened; no L3, cascade, smoke, commit, or publication occurred in R29.
