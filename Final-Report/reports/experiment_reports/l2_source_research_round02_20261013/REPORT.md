# English L2 source research, round 02 — 2026-10-13

## Scope Boundary Declaration

This round continues the attached English L2 research goal: acquire traceable public candidates, investigate component provenance, preserve immutable versions, and prepare human annotation intake. It implements the [round task](TASK.md), following the [V10 research report](../l2_readiness_research_20261013/REPORT.md). It does not authorize canonical labeling by the assistant, model fitting before data gates, L3, commit or publication. No upstream validation/test payload or locked historical evaluation file was opened during these operations.[[1]](#ref1)[[2]](#ref2)

## Research outcome

V11 adds **492 English, pattern-clear Gandalf candidates** to the 56,498 parent candidates, producing **56,990 candidate records across 11 provisional families**. V12 references that immutable index and places **554 Do-Not-Answer-derived records under an explicit rights hold**. Neither version has canonical training rows or a frozen split. Current overall status is **BLOCKED / L2 NOT_READY**; acceptance criteria remain `GATE_UNSPECIFIED` where numeric limits have not been supplied.[[2]](#ref2)[[3]](#ref3)[[4]](#ref4)

| Version | Manifest SHA-256 | Actual change |
|---|---|---|
| V11 `11.0.0-candidate-english-gandalf` | `94f4a2a79f76682be16feaf35d8074b66a9f5d11c8e08962b7781ea9949b838a` | New source intake and restored original aggregate IDs; 56,990 candidates |
| V12 `12.0.0-candidate-english-rights-overlay` | `20562180cc6e854f95c562cdce59955c9db8769295ffe5b2de354f0420497101` | Sparse rights ledger over V11; 554 held records; no prompt or index copy |

The V11 identity above is recorded exactly in the builder output and parent reference in V12; all immutable parent files are checked against stored hashes. The V12 count of **56,436 records outside this particular hold is not an eligibility count**. Other rights, privacy, label, independence and split gates remain open.[[2]](#ref2)[[3]](#ref3)

## New public source: publisher facts and local intake

The [pinned Gandalf publisher card](https://huggingface.co/datasets/Lakera/gandalf_ignore_instructions/blob/04737b65e90a6794ec227012e4a255a7def6344b/README.md) describes human game submissions from July 2023, filtered with embedding similarity, an automatic PII detector and near-duplicate removal. It declares MIT. These are publisher statements, not independent privacy or submitter-rights findings. Native similarity is retained only as provenance and never converted into a PI-Guard label. The source's selection process may bias the examples toward the publisher's similarity criterion.

Only publisher **train** was downloaded: revision `04737b65e90a6794ec227012e4a255a7def6344b`, file `data/train-00000-of-00001-ded53be747ff55cd.parquet`, SHA-256 `5b6acf3e5a5998d21f8e1222bb45bbdec25a14408747b1cd63bebef4a75fa439`. All 777 downloaded rows were accounted for: 492 accepted by the existing English filter and 285 excluded for non-English prediction or normalized confidence below 0.95. No accepted row matched the existing email/credential patterns. This limited pattern result does not establish full privacy clearance.[[1]](#ref1)[[2]](#ref2)

The 492-row annotation sheet contains unchanged accepted source text with blank curator decisions. Its legacy filename includes “pilot”, but it is the entire accepted new-source queue, conditioned on one source, not a representative or independently blinded validation sample. Source identifiers and similarity scores are omitted from the sheet. Per-record system/task context and participant identifiers are absent from the publisher payload; no context was invented. A human must mark inadequate context, uncertain or hybrid intent for quarantine under the existing rubric.[[2]](#ref2)[[4]](#ref4)

## Original component research and rights discrepancy

Nine source identities were pinned: Gandalf plus eight original aggregate components. Component payloads were not downloaded. The source manifest records full revisions, document hashes, URLs, access timestamps and declaration scope. These current publisher revisions do not establish the aggregate's original ingestion revision or native split.[[1]](#ref1)

| Component | Restored original IDs | Pinned documentation finding and limit |
|---|---:|---|
| AART | 1,851 | Card metadata declares CC BY 4.0 and describes AI-assisted adversarial evaluation; it does not establish independent human-authored PI/JB labels. |
| HarmfulQA | 1,114 | Card describes ChatGPT-distilled material and declares Apache-2.0; it does not establish that all underlying questions were human authored. |
| Do-Not-Answer | 554 | Metadata declares Apache-2.0; the body distinguishes dataset and code terms. Explicit rights hold added. |
| forbidden_question_set | 326 | Publisher metadata declares MIT; original aggregate collection revision/split remains unknown. |
| AdvBench | 322 | Original repository README and MIT license pinned; software terms do not independently adjudicate every underlying data right. |
| HarmBench | 222 | Original repository README and MIT license pinned; current revision is supplemental evidence only. |
| JailbreakBench | 56 | MIT declaration and configuration metadata pinned; original IDs do not justify assigning a train split. |
| TDC23 | 31 | Publisher metadata declares MIT and a native train configuration; this does not prove the aggregate used that revision/split. |

These are document findings, not new class labels or approved source reviews. The local restoration recovers **4,476 original record IDs** from a hash-verified historical candidate provenance file. Original component revision and split remain unresolved for all 4,476 records. That candidate provenance file is distinct from locked historical evaluation data.[[1]](#ref1)[[2]](#ref2)

The [pinned Do-Not-Answer card](https://huggingface.co/datasets/LibrAI/do-not-answer/blob/74e74f2e4507ef256fe536f78a776f4a1ff67955/README.md) has Apache-2.0 metadata, while its License section assigns CC BY-NC-SA 4.0 to datasets and Apache-2.0 to source files. **Research inference:** an aggregate's Apache-2.0 field does not resolve this distinct dataset notice. V12 therefore records a rights-review hold on the 554 affected IDs. This is not a conclusion that a particular use is illegal, nor legal clearance. Releasing the hold requires a source reviewer to record a supported use basis and obligations in a new version.[[3]](#ref3)

V12 is a sparse metadata overlay, not a full annotation packet or a model input. Future canonicalization must resolve the pinned V11 parent and V12 rights ledger together. Ten V10 pilot records from this family also require that hold to be resolved. Three other-family records share duplicate groups with held records and require group review; changing a source name must not bypass the recorded constraint. No such rows are declared eligible.[[3]](#ref3)[[5]](#ref5)

## Duplicate and source-independence evidence

Joint grouping over 56,990 records retained all inherited duplicate-group constraints. The existing exact/approximate policy found 1,178 nonsingleton groups containing 3,131 rows, including 25 cross-family groups containing 78 rows. None of those cross-family groups contains the new Gandalf source. This is a result of the specified normalization and shingle heuristic, not proof of semantic uniqueness or independent collection. Duplicate groups must remain co-partitioned or excluded when a future split is frozen.[[2]](#ref2)[[5]](#ref5)

## Data and L2 health gates

| Gate | Current evidence | Status |
|---|---|---|
| Human canonical labels | New sheet: 492 unreviewed; canonical train/validation/test rows: 0/0/0 | BLOCKED |
| Rights, lineage and privacy | Explicit rights hold: 554; original component revision/split unknown: 4,476; full privacy review absent | BLOCKED |
| Independent source coverage | 11 provisional families; no verified per-class train/validation/test coverage of at least 2/1/1 | BLOCKED |
| Duplicates and frozen split | Groups retained; no approved group resolutions, partition assignment or split hash | BLOCKED |
| L2 error, support and workload limits | No owner-predeclared numeric risk, class-support or REVIEW limits | GATE_UNSPECIFIED |
| Baseline and validation | Fixed Dual TF-IDF + balanced LR, C=2, max_iter=1000, lbfgs, seed=42 retained as configuration; no fit | NOT_RUN |
| Test and L3 | No new test access, test selection or L3 run | NOT_RUN |

These gate conclusions follow the recorded candidate statuses and annotation intake; an artifact verification PASS is not an L2 acceptance PASS. No new F1, risk/coverage, classwise REVIEW, latency or generalization metric exists for these versions.[[2]](#ref2)[[3]](#ref3)[[4]](#ref4)

For an eventual authorized L2 run, fit features and model on train only and select on validation only. Retain separate `tau_allow` and `tau_block`: B is benign support and A is PI+JB support; route ALLOW when B meets its cutoff and B>A, BLOCK when A meets its cutoff and A>B, otherwise REVIEW, including ties. These are per-window candidate routes, not final API decisions. Acceptance requires predeclared numeric limits and classwise support evidence; the final test remains separately controlled. The historical V8 runner must not be executed directly against a new package.

## Chronological execution and pipeline changes

| Recorded run | Actual outcome |
|---|---|
| `public_sources_gandalf_components_20261013_r01` | Exit 1 before payload download: overly literal MIT-text assertion missed Markdown formatting. Exact failing code and partial documents retained. |
| `public_sources_gandalf_components_20261013_r02` | Exit 0 after a bounded assertion correction; nine identities pinned and only Gandalf train downloaded. |
| `v11_gandalf_english_candidate_ingest_20261013_r01` | Exit 0; 492 added, 285 language exclusions, 4,476 original IDs restored, joint duplicate constraints recorded. |
| `v11_curator_intake_20261013_r01` | Exit 0; assessment BLOCKED, 492 unreviewed, zero canonical output. |
| `v12_dataset_rights_quarantine_20261013_r01` | Exit 0; 554 explicit holds recorded without changing parent files. |
| V10/V11 curator self-checks and round verification | Fresh results, executed code hashes, timestamps and full outputs retained in the verification evidence. |

The first round verifier stopped at a local link check because an unnormalized Windows path exceeded the legacy path length. The evidence file existed. The verifier now resolves the path before checking; the failed source, log and earlier self-check outputs are retained, and recovery uses new output names.

The r02 verifier incorrectly counted held V10 pilot records by comparing regenerated blind IDs directly. Its result is retained and superseded by r03, which validates the pinned parent-ID/candidate-ID crosswalk and confirms ten affected pilot records. This correction changes the audit count, not any candidate version or label.

The sole reusable intake-code change admits the full V11 packet alongside V10. Its previous source snapshot is retained. Fresh self-checks use actual blank packets and reject partial decisions and provenance-sidecar substitution; the sparse V12 overlay is rejected by this full-packet intake. No version-specific trainer or canonicalization adapter is represented as complete.[[4]](#ref4)[[5]](#ref5)[[6]](#ref6)

## Remaining weaknesses and next bounded work

The new source does not itself establish PI/JB/benign coverage, independent families or sufficient L3 training support. Publisher filtering, language confidence on short prompts, missing game context and the single-curator protocol limit inference. Native safety/attack tags and similarity scores remain separate from approved canonical intent. The public-data acquisition stage has progressed; the missing human decisions cannot be supplied through further automated queue growth.[[1]](#ref1)[[2]](#ref2)[[4]](#ref4)

The next informative step is to review a saved copy of the existing V10 mixed-source pilot and a bounded portion of V11, while applying the V12 rights hold. Record canonical decisions only through the human rubric and receipt, record actual class-by-family support, and quarantine ambiguous/context-incomplete cases. Resolve or exclude the original component lineage gaps before partitioning. Numeric L2 acceptance criteria must be specified before validation selection; these remain required inputs, not assumed thresholds.

## L3 handoff status

- [ ] Human canonical labels and annotation provenance recorded.
- [ ] Rights, lineage and privacy reviews approved; V12 hold resolved or affected groups excluded.
- [ ] Independent per-class train/validation/test families >=2/1/1 demonstrated.
- [ ] Duplicate resolution and source-disjoint split frozen with hashes.
- [ ] Authorized L2 baseline validation meets predeclared numeric gates, including classwise REVIEW support.
- [ ] Intended L3 training support and L1/window contract demonstrated.
- [ ] Final-test access controlled separately and L3 initiation explicitly authorized.

**L3 handoff remains blocked.** This round adds traceable candidates and a concrete rights quarantine; it does not establish L2 readiness.[[2]](#ref2)[[3]](#ref3)[[4]](#ref4)

## Evidence

<a id="ref1"></a>1. [Source manifest and pinned document URLs](source_snapshots_r02/MANIFEST.json), [acquisition command](pin_sources_r02.command.json), [full output](pin_sources_r02.log), [initial failure](pin_sources.log), [exact initial code](pin_sources_r01_failed_snapshot.py).

<a id="ref2"></a>2. [V11 builder command](build_v11.command.json), [full output](build_v11.log), [ingest/lineage report](../../../../workspaces/truongnv/pi_guard_pipeline/training_bases/datasets/project_training/versions/pi_guard_v11_english_gandalf_20261013/reports/INGEST_AND_LINEAGE.json), [V11 manifest](../../../../workspaces/truongnv/pi_guard_pipeline/training_bases/datasets/project_training/versions/pi_guard_v11_english_gandalf_20261013/DATASET_MANIFEST.json).

<a id="ref3"></a>3. [Rights overlay command](quarantine_rights_v12.command.json), [full output](quarantine_rights_v12.log), [rights evidence](../../../../workspaces/truongnv/pi_guard_pipeline/training_bases/datasets/project_training/versions/pi_guard_v12_english_rights_overlay_20261013/provenance/RIGHTS_EVIDENCE.json), [V12 manifest](../../../../workspaces/truongnv/pi_guard_pipeline/training_bases/datasets/project_training/versions/pi_guard_v12_english_rights_overlay_20261013/DATASET_MANIFEST.json).

<a id="ref4"></a>4. [Annotation intake assessment](curator_intake_v11.json), [command](curator_intake_v11.command.json), [full output](curator_intake_v11.log).

<a id="ref5"></a>5. [Round verification](VERIFICATION_r03.json), [verification script](verify_round.py), [V10 compatibility check](curator_self_check_v10_r03.json), [V11 compatibility check](curator_self_check_v11_r03.json).

<a id="ref6"></a>6. [Run ledger](RUN_LEDGER_r03.json), [pre-change intake snapshot](check_curated_candidate_pre_v11.py), [task checklist](TASK.md).
