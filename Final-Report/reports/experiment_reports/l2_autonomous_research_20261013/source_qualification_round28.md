# Round 28 — BlackboxNLP jailbreak-attempt source and L2 diagnostics

## Scope Boundary Declaration

This round audits one candidate JB source, builds a private train-only L2 successor, and runs a complete fixed-config validation fit plus five-fold source-family OOF. The formal L2 rubric remains `GATE_UNSPECIFIED`; all labels are provisional references, not curator-approved gold. No cutoff was selected. PI-Guard test payload, L3/cascade, smoke, commit, and publication stayed out of scope.

## Source and rights review

The candidate is `sevdeawesome/jailbreak_success` at pinned revision `12bad235ee184287bc5f41ec2341489501a30049`; its associated author repository is pinned in the local source manifest. The authors describe 10,800 attempts produced by 35 attack methods over 300 harmful seed prompts, and report poor transfer between held-out attack methods. This establishes one algorithmic benchmark family, not 35 independent sources or human-authored jailbreaks. [Author repository and paper summary](https://github.com/NLie2/what_features_jailbreak_LLMs/tree/8b23d26deebe5c5428af9333c880af8ed4c70ea2) · [BlackboxNLP paper](https://aclanthology.org/2025.blackboxnlp-1.28/)

The dataset card declares MIT, but that declaration does not establish rights to the 300 upstream seed prompts or each transformation. The prompts are retained only in a private local L2 diagnostic package; redistribution and publication are not cleared. The selected observation is the final `jailbreak_prompt_text`; `original_prompt_text` and the benchmark success outcome are excluded. The mapping to JB is based on attack intent only and is explicitly provisional.

The source card/paper and local audit support the benchmark-level provenance above, but do not establish record-level seed authorship, independent source ancestry, or human privacy adjudication. Configured privacy patterns found no hits in retained candidates; that automated screen is incomplete. Attack text is sensitive by design. A public author-repository preview automatically displayed illustrative harmful examples during source research; none was copied into the package, report, or metrics, and the preview content was quarantined.

## Aggregate-only audit

The audit used the pinned source-file hash and compared only against the clean R05 train/validation partitions. It excluded the seed field, kept candidate text out of the report, and emitted aggregate counts and hashes only.

| Audit result | Count |
| --- | ---: |
| Input attempts | 10,800 |
| Seed-prompt groups | 300 |
| Attack methods | 35 |
| Normalized unique transformed prompts | 9,884 |
| Exact duplicate rows collapsed | 916 |
| Exact overlaps with clean R05 train/validation | 0 |
| Ambiguous prompts linked to multiple seed groups | 1 |
| Near-duplicate candidates against clean R05 train/validation | 295 |
| Within-source near-duplicate candidates excluded | 3,037 |
| Configured privacy-pattern hits among unique candidates | 0 |
| Retained private train candidates | 6,551 |
| Retained seed groups | 300 |

The audit also used NFKC/casefold normalization and a 0.85 five-word-shingle Jaccard screen. These screens reduce known duplicate and configured-pattern risk; they do not resolve lineage, rights, or human privacy review. The candidate audit is [blackboxnlp_jb_candidate_audit_round28.json](blackboxnlp_jb_candidate_audit_round28.json), and the private candidate rows are stored under `workspaces/truongnv/pi_guard_pipeline/training_bases/datasets/source_audit/blackboxnlp_jb_round28/`.

## Package and run evidence

The final package is private `pi_guard_l2_blackboxnlp_round28_candidate_r03_20261014` (version `0.8.12-r28-blackboxnlp-provisional-r03`), built from the R27 cleaned-validation baseline. It adds 6,551 provisional JB rows from one family to 140,429 existing train rows, producing 146,980 train rows. The 9,656-row validation partition is byte-identical to the baseline and contains only 76 JB rows, below the protocol's 100-row diagnostic support floor. The approved family-only test contract is unchanged.

Two earlier package drafts were rejected at preflight because the `rights_scope` and embedded rights-evidence scope did not exactly match the package schema. They did not start a fit. The corrected R03 package passed `READY_FOR_FIT`. This schema correction records private research-only scope; it does not upgrade the source's rights or lineage status.

The full fixed-config fit used hard argmax predictions on the complete shared validation partition, with no cutoff selection.

| Validation fit | Macro-F1 | Accuracy | Benign FPR | JB precision | JB recall | JB F1 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| R27 clean-validation baseline | 0.4419 | 0.4562 | 0.3011 | 0.3193 | 0.6974 | 0.4380 |
| R28 BlackboxNLP candidate | 0.3104 | 0.4137 | 0.3576 | 0.0510 | 0.5789 | 0.0938 |

The candidate reduced validation macro-F1 by 0.1315 and JB F1 by 0.3442, while benign FPR rose by 0.0565. Reject it as a model improvement.

The complete five-fold OOF used the frozen train rows only. Source-family, collection-lineage, prompt-family, and duplicate groups were held out by the shared runner; validation and test payloads were not used.

| Train-only OOF | Macro-F1 | Benign FPR | JB precision | JB recall | JB F1 |
| --- | ---: | ---: | ---: | ---: | ---: |
| R05 historical comparator | 0.7638 | 0.3086 | 0.4162 | 0.8337 | 0.5552 |
| R28 BlackboxNLP candidate | 0.6068 | 0.3454 | 0.2801 | 0.1072 | 0.1551 |

R28 fold macro-F1 ranged from 0.3504 to 0.7896 and benign FPR ranged from 0.0802 to 0.5352. The package has 11 JB families after adding this source, but the candidate contributes only one new family; its held-out performance is not independent-source coverage. See [package build](l2_blackboxnlp_package_build_round28.json), [validation fit](l2_blackboxnlp_round28_candidate_r03_fit_20261014.json), and [family OOF](l2_blackboxnlp_family_oof_round28.json). Full fit artifacts remain in the private workspace.

## Decision and next work

R28 is rejected. It worsens both full-validation and pooled family-OOF evidence; the JB source is an algorithmic benchmark family with unresolved upstream seed rights, record-level lineage, and human privacy review. Do not reuse this augmentation for further parameter tuning. Continue L2 source qualification for an independently lineaged, rights-cleared, single-turn JB source and close owner-level privacy/lineage decisions. The official rubric and owner limits remain `GATE_UNSPECIFIED`, so these exploratory metrics cannot establish L2 PASS.

No test payload was opened; no L3, cascade, smoke, commit, or publication occurred in R28.
