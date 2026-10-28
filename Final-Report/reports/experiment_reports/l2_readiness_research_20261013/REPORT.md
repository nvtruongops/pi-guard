# English L2 readiness research — execution round

## Scope Boundary Declaration

This report continues the user's attached L2 research goal under [TASK.md](TASK.md). It covers English candidate provenance recovery, review-packet preparation, curator-intake pipeline checks and public-source documentation research. V9 and historical source artifacts remain read-only. Canonical labeling, source-review approval and acceptance limits belong to their designated human owners. Historical locked evaluation payloads, L3, commit and publication are outside this round.

## Decision and concrete progress

L2 outcome: **BLOCKED**. Health-check outcome: **NOT_READY**. Research execution produced a new candidate version and an executable annotation intake stage. These are completed preparation steps, not an L2 performance pass. L3 training is not authorized. The earlier health check is preserved as an audit record; this task addresses deficiencies it identified.[1](#local-evidence)

The new [V10 manifest](../../../../workspaces/truongnv/pi_guard_pipeline/training_bases/datasets/project_training/versions/pi_guard_v10_english_readiness_20261013/DATASET_MANIFEST.json) binds 56,498 unchanged V9 candidate inputs to recovered split/file and collection-group metadata. All 56,498 rows now expose the source's recorded split. For 4,476 aggregate rows, that marker describes the aggregate container; the original component split remains explicitly unknown. Recovering these fields strengthens provenance without declaring family independence or assigning labels.[1](#local-evidence)

The focused pilot contains 96 existing records across 10 provisional families: ten per family except six eligible LLMail records. Selection used stable hash ordering, excluded earlier pilot IDs and cross-family duplicate groups, retained one row per duplicate group and limited prompt plus context to 8,000 characters. This is a non-representative diagnostic review packet, not a validation sample. Every decision field remains blank. The pilot excludes cross-family groups for curator efficiency; the full corpus still contains 25 unresolved cross-family duplicate groups involving 78 rows.[1](#local-evidence)

The [curator intake checker](../../../../workspaces/truongnv/pi_guard_pipeline/training_bases/pi_guard_tfidf_tier1/check_curated_candidate.py) checks manifest hashes, exact prompt/context binding, ID coverage, the blind sheet schema, rubric version, decision completeness and flag consistency. Hybrid, uncertain and insufficient-context decisions remain quarantined. Duplicate-group label conflicts block intake. The checker emits evidence only; it does not emit training rows or fit a model. A human receipt, when supplied, records authorship provenance; field values alone do not prove human authorship. Fresh execution found 96 unreviewed records and zero canonical model rows.[2](#local-evidence)

## Data and L2 gates

| Gate | Current evidence | Outcome / next requirement |
|---|---|---|
| Public candidate identity and content binding | V9 and source hashes checked; unchanged candidate text bound in V10 | PASS for candidate reconstruction only |
| English filter | Inherited pinned py3langid 0.4.0 model, English confidence >=0.95; input binding and metadata checked | PASS for unchanged candidate policy; detector not rerun |
| Original split/file provenance | Source split recorded for 56,498; original component split unknown for 4,476 | PARTIAL; resolve component provenance or exclude affected rows |
| Privacy | Existing email/credential patterns rechecked; source-level reviews remain open | NOT READY; pattern scan is not full privacy review |
| Canonical curator labels | 96/96 pilot rows unreviewed; zero model rows emitted | NOT READY; human decisions required |
| Independent source families | Ten provisional families, not ten verified independent families | NOT READY; source reviewer must resolve lineage and parent overlap |
| Per-class family coverage | True label support unavailable before review | NOT READY; require train/validation/test families >=2/1/1 for each class |
| Duplicate handling | 25 cross-family groups / 78 rows retained in full index | NOT READY; co-partition or document exclusions before freeze |
| Frozen source-disjoint split | No partition generated | NOT READY |
| Baseline training | No eligible frozen corpus, no fit attempted | NOT AVAILABLE |
| L2 numeric acceptance / cutoff selection | Owner declaration still unspecified | GATE_UNSPECIFIED; predeclare before fresh validation selection |
| Validation class metrics / route sweep / latency | No new trained L2 or validation set | NOT AVAILABLE |
| Final API targets | Separate from L2 window routing gates | Not evaluated in this round |

Gate observations above derive from the candidate manifest, lineage report and actual intake output.[1](#local-evidence)[2](#local-evidence) The required gate sequence and route semantics follow the project [L2 Health Check skill](../../../../.agents/skills/l2-health-check/SKILL.md). Two cutoff parameters define ALLOW/BLOCK candidate routes; REVIEW is residual, and per-window candidate routes do not constitute final API outcomes.

## Public source follow-up

Three additional primary dataset records were pinned. No source payloads were downloaded or terms accepted, and no eligible family was added. The first script stopped at an HTTP 401 for a gated card. Its log and exact code snapshot are preserved; the follow-up records per-source access failures and completes the remaining metadata screening.[3](#local-evidence)

| Prospect | Pinned evidence and finding | Research disposition |
|---|---|---|
| ai-mitra/prompt-injection-dataset | Publisher describes training data as synthetic/template-generated; separately authored examples are in a test split. [Pinned card](https://huggingface.co/datasets/ai-mitra/prompt-injection-dataset/raw/82baf561be4496f6e38620d33fe9ffdfc7d8d706/README.md) | Does not establish an additional independent human-authored train family. Deprioritized for the current coverage gap; test not accessed. This is a source-selection judgment, not a claim that all public synthetic data are prohibited. |
| ScaleAI/mhj | Pinned API revision `ad6e928f5c2823f53fbb828f6d60dd4137fd43e7`; recorded gating `auto`, license `cc-by-nc-4.0`; pinned card returned 401. [Publisher dataset](https://huggingface.co/datasets/ScaleAI/mhj) | Access and multi-turn input-contract review required; no access agreement accepted. |
| Mindgard/evaded-prompt-injection-and-jailbreak-samples | Pinned API revision `ec63ffb26ba6f29ca1095fabb2e9f9be5f8b9d34`; recorded gating `auto`, license `cc-by-nc-4.0`; pinned card returned 401. [Publisher dataset](https://huggingface.co/datasets/Mindgard/evaded-prompt-injection-and-jailbreak-samples) | Remains an unqualified prospect; no payload access or independence claim. |

For the previously pinned in-page injection prospect, the root README describes a sanitized public release, while the data schema documents URL/origin and surrounding context fields. This documentation difference leaves the public payload's privacy/sanitization scope unresolved. The dataset is also webpage content, requiring a defensible L1/L2 trust-boundary contract before use. It remains metadata-only; no effectiveness or other evaluation payload was opened. This is an inference from the [pinned release notice](https://raw.githubusercontent.com/SoheilKhodayari/in_page_prompt_injection_pub/0a04d1762cf60957f954f16a6cb9525ab32d6bca/README.md) and [pinned schema](https://raw.githubusercontent.com/SoheilKhodayari/in_page_prompt_injection_pub/0a04d1762cf60957f954f16a6cb9525ab32d6bca/data/README.md), not a claim that its actual payload contains identifying data.

## Chronological execution evidence

| Run | Dataset/code identity | Actual outcome | Metrics / progress |
|---|---|---|---|
| `v10_lineage_candidate_20261013_r01` | V10 manifest `e7ec79fb79185748a9989895c45968e4386da1f5fcf722b7905453656aeaa7c6`; builder hash in command record | Exit 0 | 56,498 candidate provenance records; 96 pilot rows; zero canonical rows |
| `v10_curator_intake_20261013_r01` | Same V10; checker hash `0323b83954d8ea002ae52832f0338b74b9a0f886524c666582d2281305c3b824` | Exit 0, assessment BLOCKED | 96 unreviewed, zero fit/test/L3; successful execution is not data readiness |
| `public_source_followup_20261013_r02` | Exact initial code snapshot and command hash retained | Exit 1, HTTP 401 | Partial metadata only; no payload |
| `public_source_followup_20261013_r03` | Revised metadata collector hash in command record | Exit 0 | Three prospect identities recorded; two card-access failures retained |
| Curator intake self-check r01 | Same checker and V10 hashes | Exit 0, self-check PASS | Real blank pilot stays blocked; partial decision and source-sidecar substitution rejected |

Full outputs, timestamps and exit codes are retained next to this report. There are no new trained-model metrics. Existing V8 diagnostic evidence remains in the [prior health-check report](../l2_v9_health_check_20261013/REPORT.md); it has not been refit or promoted into evidence for V10.[1](#local-evidence)[2](#local-evidence)[3](#local-evidence)

## Remaining weaknesses and next experiment

The pilot deliberately limits annotation work; it cannot establish class balance, rare attack coverage or accuracy. Published harmful/safety labels cannot establish PI/JB intent, and the original single-curator limitation remains. Recovering collection IDs does not establish independent sources; inherited approximate duplicate detection does not guarantee semantic separation.[1](#local-evidence)

The next testable hypothesis is that reviewing a bounded mixture of source families will reveal which existing families actually supply clear Benign, PI or JB examples under the approved rubric. The evidence is the completed pilot's class-by-family support and quarantine reasons. This should guide targeted acquisition or exclusion, rather than expanding a large unreviewed queue. No class outcome is predicted here.

The pipeline stage completed in this round is annotation intake, not a finished V10 trainer. The reusable baseline remains `fit_l2_v8.build_model` / `evaluate`; direct execution of its historical V8 CLI is inappropriate for V10. After canonical schema, source review and frozen split exist, adapt that runner with train-only feature fitting, validation-only selection, weighted summaries, required latency measurements and an independently controlled final test step. These dependent steps remain pending, rather than being reported as implemented.

## L3 handoff checklist

- [ ] Canonical English labels supplied by the human curator, with annotation provenance.
- [ ] Rights/lineage/privacy decisions recorded; unresolved original component splits resolved or excluded.
- [ ] Independent train/validation/test source coverage >=2/1/1 per class demonstrated.
- [ ] Duplicate groups resolved and source-disjoint split frozen with hashes.
- [ ] Authorized L2 baseline trained and validation evidence meets owner-predeclared numeric gates.
- [ ] Classwise REVIEW support and intended L3 training support demonstrated under the L1/window contract.
- [ ] Prior test-selection use excluded through access records; final test controlled separately.
- [ ] Separate human authorization to begin L3.

Current status: **not ready to request L3**. Research preparation progressed; fitting and readiness claims remain dependent on missing human evidence and downstream gates.

<a id="local-evidence"></a>
## Local evidence

1. [Builder command](prepare_v10.command.json), [full output](prepare_v10.log), [V10 lineage/duplicate report](../../../../workspaces/truongnv/pi_guard_pipeline/training_bases/datasets/project_training/versions/pi_guard_v10_english_readiness_20261013/reports/LINEAGE_AND_DUPLICATE_REPORT.json), [parent/source integrity](../../../../workspaces/truongnv/pi_guard_pipeline/training_bases/datasets/project_training/versions/pi_guard_v10_english_readiness_20261013/provenance/PARENT_INTEGRITY.json).
2. [Intake run](curator_intake_r01.json), [command](curator_intake_r01.command.json), [full output](curator_intake_r01.log), [self-check](curator_self_check_r01.json), [self-check output](curator_self_check_r01.log).
3. [Initial source command](source_followup.command.json), [failure log](source_followup.log), [exact initial code](screen_source_followup_r01_failed_snapshot.py), [recovery command](source_followup_r02.command.json), [pinned records](source_followup_r02/manifest.json), [full output](source_followup_r02.log).
