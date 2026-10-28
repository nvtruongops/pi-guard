# Human review handoff — V9 English L2

## Scope Boundary Declaration

This is the review package required by the user's 2026-10-13 goal. It records pending human decisions and creates no canonical labels or dataset partitions. No L3 is authorized.

## 1. Curator decisions

Start with the existing [20-row Round 03 pilot](../../../../workspaces/truongnv/pi_guard_pipeline/training_bases/datasets/project_training/versions/pi_guard_v9_english_source_heldout_20261013/annotation/round03_source_blind_curator_review.csv). Read the [single-curator protocol](../../../../workspaces/truongnv/pi_guard_pipeline/training_bases/datasets/project_training/history/pi_guard_v8_source_gate_20261010/LABEL_ADJUDICATION_PROTOCOL.md). Preserve the blank original; save decisions in a separate completed copy. The pilot is a subset of Round 02 and is not representative. It cannot establish adequate per-class training or evaluation support. [1](#evidence)

Assign `curator_label`, the two intent flags, confidence, reason, context sufficiency, curator code, rubric version, UTC timestamp, and final status. Use a canonical final label only for a clear `benign`, `PI`, or `JB` judgment. Keep `hybrid`, `uncertain`, missing-context, privacy-concern and unreviewed rows quarantined. These are task rules, not assistant label proposals.

Do not open provenance keys, source labels, model results, or assistant suggestions before completing the blind decisions. The following files are for a separate source/privacy review after labeling; showing their source identifiers beforehand can weaken blinding.

## 2. Source/privacy review

The [privacy review index](run_20261013_round04_verified/privacy_review_index.csv) identifies 18,283 candidates requiring the already-declared source-level review: LLMail 8, TrustAIRLab 13,799, and Rubyglask 4,476. It contains IDs and grouping metadata, with no prompt text. Inspect only the corresponding private review-sheet content; avoid copying personal information into review notes or logs. Record reviewer identity, UTC time, reviewed scope, evidence, exclusions, residual limitations and a decision. A pattern scan cannot supply this decision. [1](#evidence)

Review the [10-family lineage worksheet](run_20261013_round04_verified/family_lineage_review.csv). Confirm original source/revision/record, original split or unsplit status, content-use basis and source notice, collection time, parent/component relationships, and independence. Several families share an aggregate parent; a component name alone is insufficient evidence. The V9 candidate index does not have an explicit `upstream_split` field; recover that provenance from the pinned source manifests/sidecars when creating a reviewed successor. Do not repair V9 in place. [1](#evidence)

Resolve the [25 cross-family duplicate groups](run_20261013_round04_verified/cross_family_duplicate_review.json): keep each entire group in one partition or record which cross-family copies are excluded. These groups cover 78 candidate rows. Do not interpret a duplicate-connected component as proof of shared authorship or of source independence. [1](#evidence)

## 3. Owner acceptance declaration

Complete a new version of [OWNER_GATE_DECLARATION.json](OWNER_GATE_DECLARATION.json) before V9 validation selection. Declare route units, the input/window contract, cutoff grid, maximum per-class attack early-ALLOW, benign early-BLOCK, REVIEW capacity, minimum per-class REVIEW support, and class/source training support. Record the selection rule and whether L2 latency is a formal gate. Values currently remain null because no approved numeric limits were found in the inspected task/checkpoint. [1](#evidence)

The inherited routing contract uses two score cutoffs: `B=score(benign)` and `A=score(PI)+score(JB)`; ALLOW requires `B>=tau_allow` and `B>A`, BLOCK requires `A>=tau_block` and `A>B`, and all remaining cases, including ties, go to REVIEW. The owner must explicitly adopt or replace the candidate grid for the new task. Candidate routes are window outputs and are separate from final API request decisions. [1](#evidence)

## 4. Next automated work after review

Create a new immutable dataset version from accepted decisions and source-review records. Verify independent source-family support for each class: at least two train families, a separate validation family, and a separate test family. Resolve duplicates, freeze all IDs/hashes, and record exclusion of V8 locked evaluation rows through authorized metadata/access records. Do not open V8 locked payloads to establish exclusion.

Adapt the existing `build_model` and validation evaluator with strict V9 curator/privacy/lineage gates, instead of executing the V8-specific CLI. Fit the fixed baseline only after data gates pass; select on validation only under predeclared limits, then lock model/policy before the one authorized V9 test evaluation. L3 remains a separate future authorization.

## Evidence

<a id="evidence"></a>**[1]** Fresh local [audit JSON](run_20261013_round04_verified/audit.json), [readiness report](REPORT.md), and the linked current task/protocol. All counts describe candidates or saved diagnostic evidence; none are V9 training results.
