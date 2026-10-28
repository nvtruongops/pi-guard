# Round 27 — JailbreakBench attack artifacts and paired L2 experiment

## Scope Boundary Declaration

This round qualifies only a private L2 train candidate and compares two complete L2 classifier fits plus the candidate's complete five-fold source-family OOF. It does not select a routing cutoff, infer canonical labels, open PI-Guard test rows or text, run L3/cascade/smoke, publish data, or commit changes. The official L2 rubric remains `GATE_UNSPECIFIED`.

## Source review

The pinned source is `JailbreakBench/artifacts` revision `909e68c01d94222b8ad2e397a017e2e12e2adb73`. The first-party artifacts README describes one final `prompt` and its `response`, with attack method/model and outcome metadata. Treating the final prompt as a single-turn JB-attempt reference is an inference from that schema and the paper's input-prompt definition; `number_of_queries` describes attack search effort, and the benchmark includes adaptive methods, so it does not establish a single-query generation process. It also does not establish that every artifact was human-authored. [Pinned artifacts README](https://github.com/JailbreakBench/artifacts/blob/909e68c01d94222b8ad2e397a017e2e12e2adb73/README.md) · [JailbreakBench paper](https://proceedings.neurips.cc/paper_files/paper/2024/file/63092d79154adebd7305dfd498cbff70-Paper-Datasets_and_Benchmarks_Track.pdf)

The README declares MIT licensing per artifact and attributes ownership to the artifact author. That is a first-party rights declaration, but individual author ownership and any upstream components were not verified. The paper's JBB-Behaviors provenance proportions apply to its behavior-seed dataset, not automatically to the separate attack-artifact repository; the artifact schema does not provide equivalent per-prompt upstream provenance. The source is restricted to private local research, with no redistribution or publication permission recorded. [Pinned artifacts README](https://github.com/JailbreakBench/artifacts/blob/909e68c01d94222b8ad2e397a017e2e12e2adb73/README.md) · [Pinned artifacts license](https://github.com/JailbreakBench/artifacts/blob/909e68c01d94222b8ad2e397a017e2e12e2adb73/LICENSE) · [JBB-Behaviors data card](https://huggingface.co/datasets/JailbreakBench/JBB-Behaviors/blob/main/README.md)

The paper describes sensitive harmful prompts and jailbreak strings as intentional dataset content. Local screening found no configured email, SSN, phone-candidate, IPv4, or credential-assignment patterns in retained candidate prompts; this is not human privacy adjudication or complete PII clearance. The external data-card page auto-rendered sample rows during browsing; they were quarantined and not copied or used. README/paper extraction also surfaced a truncated illustrative prompt/response example, which was not used in the package or metrics. PI-Guard's test payload remained unopened.

## Aggregate source audit

The local audit verified the selected artifact file hashes against the R17 pinned manifest and excluded all `JBC/manual` artifacts because that 100-row collection was used in R05 validation and carries the known JailbreakChat/TrustAIR community-lineage overlap. It also removed those 100 JBB validation rows from both paired packages. All retained JBB methods and models were treated as one collection family.

| Audit result | Count |
|---|---:|
| Selected pinned artifact files | 24 |
| Non-JBC prompt occurrences | 1,637 |
| Exact-normalized unique non-JBC prompts | 997 |
| Exact duplicates collapsed | 640 |
| Unique prompts removed for within-JBB near-duplicate pairs at ≥0.85 five-word-shingle Jaccard | 335 |
| Retained private train candidates | 662 |
| Behavior-ancestry groups retained | 105 |
| Behavior groups represented by multiple attack methods | 100 |
| Exact overlap with R05 train or validation after removing JBB validation | 0 |
| Configured privacy-pattern hits among candidates | 0 |

The retained prompts remain one source family. A family-held-out fold can test transfer to this one benchmark collection, but the split cannot establish independent-source generalization. The audit report and private candidate file are `jbb_train_candidate_audit_round27.json` and `workspaces/truongnv/pi_guard_pipeline/training_bases/datasets/source_audit/jailbreakbench_artifacts_round27/eligible_train_candidates.jsonl`.

## Paired package and L2 evidence

Both private packages were built from frozen `pi_guard_l2_source_diverse_round21_r05` (base manifest SHA-256 `bb2033181d66e40760f11eb1ea8b0efc00cac2c2eca41e816cdcace09b024321`). R05 and R06 were not modified. Both packages remove the same 100 old JBB validation rows and retain identical 9,656-row validation bytes. It contains 2,089 benign, 7,491 PI, and 76 JB rows. The 76 JB support is below the protocol's 100-row diagnostic floor, so these metrics are weaker evidence and cannot qualify as an official acceptance result. Both packages passed the adapter's metadata/hash/family preflight; the family-only test contract remained byte-identical.

The baseline uses 140,429 train rows and the candidate uses 141,091, including 662 additional JB references from 105 JBB behavior groups. Both used the unchanged fixed classifier configuration and the full validation partition. The evaluation used hard classifier predictions; no threshold or cutoff was selected.

| Full validation fit | Macro-F1 | Accuracy | Benign FPR | JB precision | JB recall | JB F1 |
|---|---:|---:|---:|---:|---:|---:|
| Clean-validation baseline | 0.4419 | 0.4562 | 0.3011 | 0.3193 | 0.6974 | 0.4380 |
| JBB train candidate | 0.2850 | 0.3674 | 0.3212 | 0.0309 | 0.7105 | 0.0592 |

The candidate lowered macro-F1 by 0.1569 and JB F1 by 0.3788; benign FPR increased by 0.0201. The added prompts raised JB recall slightly while sharply reducing precision and PI performance. The candidate is rejected as a model improvement.

The candidate's complete five-fold family OOF produced pooled macro-F1 `0.7227`, benign FPR `0.3257`, and JB F1 `0.4513`, compared with R05's historical pooled OOF `0.7638`, `0.3086`, and `0.5552`. Fold macro-F1 ranged from `0.4441` to `0.8424`. The JBB family was held out together in fold 3: 134/662 prompts were predicted JB (recall `0.2024`), 161 as PI, and 367 as benign. This is poor transfer to the held-out JBB collection and supports rejecting the source/model candidate.

The run records are `l2_jbb_round27_baseline_validation_full_20261014.json`, `l2_jbb_round27_candidate_validation_full_20261014.json`, and `l2_jbb_round27_candidate_family_oof.json`. Full private run artifacts are in the corresponding `pi_guard_tfidf_tier1/runs/` directories.

## Decision and next work

R27 does not make L2 ready. The JBB artifact collection is a conditional, benchmark-derived private reference with unresolved per-artifact ownership/upstream rights and no human privacy adjudication; its candidate fit and family-held-out result both regress. It is not counted as an independent human-authored JB source. The validation JB support also falls below the protocol's diagnostic floor after removing the overlapping JBC family. The formal owner rubric and owner-level rights/lineage/privacy decisions remain absent, so the project stays `NOT_READY / GATE_UNSPECIFIED`.

Next work remains L2-only: qualify a different independently lineaged, single-turn JB source with usable rights and privacy evidence, or improve source coverage through an authorized data path. Do not repeat this JBB augmentation, tune cutoffs on the current validation, open test payload, or run L3/cascade/smoke.

No test payload, L3, cascade, smoke task, commit, or publication was used in R27.
