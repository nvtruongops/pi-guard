# L2 Health Check — V9 English readiness

**Task outcome: BLOCKED. Health-check status: NOT_READY. L3 handoff: NOT READY.**

## Scope Boundary Declaration

This report fulfills the user's 2026-10-13 L2 goal, using the loaded `l2-health-check` skill and the existing [V9 task](../../../../workspaces/truongnv/pi_guard_pipeline/training_bases/datasets/project_training/versions/pi_guard_v9_english_source_heldout_20261013/V9_ENGLISH_DATASET_INITIALIZATION_TASK_20261013.md). The source goal is attachment `f1e02700-0258-4879-af69-66f65bf10407/pasted-text-1.txt`; its hash is retained in [execution records](EXECUTION_RECORDS.json). The project task, rather than a historical Chapter 2 prohibition, authorizes this bounded L2 research. [1](#local-evidence)

| In scope | Out of scope / not inspected |
|---|---|
| English candidate-data and readiness audit; saved English L2 validation evidence; public-source metadata research; exact human-review package; reproducible logs and handoff | Multilingual experiments; assistant-curated canonical labels; dataset/history edits; test/source-evaluation payloads; model fitting while data gates fail; L3/cascade execution; commit or publication |

The current dataset is `pi_guard_v9_english_source_heldout_20261013`, version `9.0.0-candidate-english`. No dataset bytes changed, so this audit creates a new evidence run rather than a new dataset version. The manifest hash is `ed96d043bfd870759271b4809cb03858d1a48840a4aed628abfec64a74d991d9`. The V8 English package is an immutable diagnostic reference only; its validation records were not added to V9. [1](#local-evidence)

## Decision

**BLOCKED / NOT_READY**: canonical curator labels, source privacy/independence review, class-specific source coverage, duplicate partition decisions, and frozen splits are absent. Numeric route-risk/workload/support acceptance limits are `GATE_UNSPECIFIED`. This is an evidence/readiness decision, not a failed V9 model measurement. No V9 model was trained or tested, and L3 training is not authorized. [1](#local-evidence)

The requested [project skill](../../../../.agents/skills/l2-health-check/SKILL.md) was loaded and its readiness rules and the user's additional training/data gates were applied. Existing pipelines were inspected; no new cutoff, model variant, or canonical label was chosen. [1](#local-evidence)

## Fresh empirical deliverables

The [verified audit](run_20261013_round04_verified/audit.json) checked all 23 current V9 package files before/after, recorded artifact hashes, candidate/provenance IDs and normalized input hashes, original blank curator fields, selected candidate-source artifacts, language-model hash, screening metadata, and duplicate-group counts. It also verified the saved English V8 model/metrics/prediction hashes and rebuilt its confusion matrix from saved predictions. This was an audit, not model inference or an ingestion rerun. [1](#local-evidence)

| Quantity | Fresh result | Interpretation |
|---|---:|---|
| Source candidate records checked | 81,208 | Five existing pinned source pools; no duplicate download |
| English/pattern-clear candidates | 56,498 | Candidate status only |
| Round 01 unique review rows | 43 | Nonrepresentative pilot |
| Round 02 additional review rows | 56,455 | Disjoint from Round 01 |
| Round 03 review rows | 20 | Subset of Round 02; adds zero distinct candidates |
| Filled curator decision fields | 0 in all three sheets | Zero canonical train/validation/test rows |
| Language exclusions | 24,564 | Counts only; no multilingual evaluation |
| Pattern-screen quarantines | 146 | Not a complete privacy review |
| Source-level privacy-review pending | 18,283 | LLMail 8; TrustAIRLab 13,799; Rubyglask 4,476 |
| Provisional family IDs | 10 | Zero verified eligible class/partition families |
| Non-singleton duplicate groups / rows | 1,178 / 3,131 | Existing grouping recomputed from metadata |
| Cross-family groups / rows | 25 / 78 | Partition handling unresolved |

All numbers in this table are from [audit.json](run_20261013_round04_verified/audit.json); the 20-row pilot must not be added again to the 56,498 total. [1](#local-evidence)

## Data gates

| Gate | Status | Evidence and counts | Limitation / next evidence |
|---|---|---|---|
| Selected source artifact integrity | PASS | Five pool manifests and their candidate/annotation references hash-checked; 81,208 aligned records | Does not revalidate every original remote raw payload |
| Rights/lineage metadata for candidate intake | PASS WITH LIMITS | Pinned source notices, record locators and license references present | Not legal clearance; canonical use and parent/component lineage need review |
| Original upstream split lineage | NEEDS RECONCILIATION | Source manifests preserve original release/split evidence; V9 index has no explicit `upstream_split` column | Carry original split/unsplit status into a reviewed successor with evidence |
| English filter | PASS FOR RECORDED POLICY/INTEGRITY | py3langid 0.4.0; `en` and score >=0.95; model hash `f4f4a2c3465ca1f081541037f9cac23021d68151c2f709c55ae5eedfca522963` | Model/metadata verified; no language reclassification rerun; heuristic errors remain possible |
| Privacy pattern screening | PASS WITH QUARANTINES | Review texts match their recorded hashes and pass existing email/credential patterns; 146 excluded | Pattern absence is not complete privacy clearance |
| Source-level privacy review | BLOCKED | 18,283 pending candidate IDs indexed separately | Human review record and exclusions required |
| Human canonical labels | BLOCKED | 0 filled curator fields; 0 canonical rows | Return completed copies under the single-curator rubric |
| Independent source families | BLOCKED | 10 provisional IDs only | Review lineage, collection parents and component overlap |
| Per-class family floor | BLOCKED | Train/validation/test eligible coverage currently 0/0/0 for benign, PI and JB | At least 2/1/1 independent families per class, disjoint by partition |
| Duplicate computation | PASS FOR RECORDED GROUPS | 1,178 groups; 3,131 rows | No exhaustive semantic-overlap claim; grouping policy remains a limitation |
| Cross-family duplicate disposition | BLOCKED | 25 groups, 78 rows | Keep each group together or record exclusions before partitioning |
| Frozen source-disjoint splits | BLOCKED | No V9 model rows or split manifest | New immutable reviewed version with partition IDs/hashes |
| V8 locked-data exclusion | NOT PROVEN BY INDEPENDENT ACCESS RECORD | Inspected V9 task/run metadata reports no locked-data use | Do not inspect locked payloads; establish from authorized lineage/access evidence |

Evidence: [audit JSON](run_20261013_round04_verified/audit.json), [family worksheet](run_20261013_round04_verified/family_lineage_review.csv), [privacy index](run_20261013_round04_verified/privacy_review_index.csv), and [cross-family duplicate review](run_20261013_round04_verified/cross_family_duplicate_review.json). [1](#local-evidence)

## L2 gates

| Gate | Status | Evidence / required next result |
|---|---|---|
| Fixed baseline configuration | RECORDED | Dual TF-IDF + balanced Logistic Regression, C=2, max_iter=1000, lbfgs; existing English baseline has seed 42 and word 1–3 / char_wb 3–5 |
| V9 input/context/window contract | NOT RECORDED | Adopt a precise contract before materializing model rows; do not silently drop required email/host-task context |
| V9 fit, classwise validation metrics, family/slice errors | NOT RUN | Data gates fail; precision/recall/F1, confusion matrix, macro/weighted summaries and benign FPR are NOT AVAILABLE |
| Predeclared route-risk and workload caps | GATE_UNSPECIFIED | Max PI/JB early-ALLOW, benign early-BLOCK, REVIEW load/capacity absent |
| Minimum classwise REVIEW and training support | GATE_UNSPECIFIED | Owner must predeclare integer supports and source scope before selection |
| Complete validation sweep / selected operating point | NOT AVAILABLE | V9 has no validation or selected pair; V8's 49 diagnostic pairs are not V9 acceptance |
| L2 latency P50/P95/P99 | NOT AVAILABLE; FORMAL GATE UNSPECIFIED | Specify hardware, units, warmup/runs and measurement boundary before using latency for PASS |
| One-time frozen V9 test evaluation | NOT RUN | Only after data gates, validation selection and model/policy lock; never choose readiness or thresholds on test |
| L3 readiness / execution | NOT READY / NOT RUN | Separate future authorization required |

The [owner declaration template](OWNER_GATE_DECLARATION.json) intentionally leaves values null. The inspected [checkpoint](../../../../workspaces/truongnv/pi_guard_pipeline/training_bases/datasets/project_training/history/pi_guard_v8_english_diagnostic_20261012/L2_TO_L3_TRAINING_GATE_CHECKPOINT_20261012.md) explicitly sets no numeric acceptance caps. Project final API FPR <1.5% and P95 <30 ms remain design objectives, not inferred L2 limits or measured cascade results. [1](#local-evidence)

## Chronological run/evidence table

Dates below use Asia/Bangkok (UTC+7). V9 historical round manifests do not record exact execution timestamps or complete command/environment logs; their artifact date and logical round order are shown without inventing timestamps. Full identities and hashes are in [RUN_LEDGER.json](RUN_LEDGER.json). [1](#local-evidence)

| Time / round | Dataset / code evidence | Rows / measured progress | Outcome |
|---|---|---|---|
| 2026-10-12 13:07:40 — saved English V8 L2 | 8.0.1-candidate-english-diagnostic; saved runner hash `91062a707107…`; split `e8949076251b…` | Train 17,746; validation 153; macro-F1 0.429946; benign FPR 14/51 | Existing diagnostic, freshly hash-verified; not rerun |
| 2026-10-13 artifact date — V9 Round 01 | 9.0.0-candidate-english; pilot manifest/hash verified | 43 blank review rows; 0 canonical | Candidate review only |
| Same artifact date — V9 Round 02 | Same dataset; pinned ingest config and current helper hash retained | 56,455 additional candidates; 1,178 duplicate groups | Candidate review only |
| Same artifact date — V9 Round 03 | Same dataset; pilot manifest/hash verified | 20-row subset; separate assistant sidecar unused as canonical | Awaiting human review |
| 2026-10-13 02:00:06 — audit attempt 04 | Same dataset; initial audit source snapshot/hash preserved | Verified candidate counts; noticed import-created bytecode caches, removed only those new files | Superseded audit implementation; no fit |
| After attempt 04 — archive-bundle assertion | Same dataset; read-only verification | Detected two historical document hash discrepancies | Exit 1; evidence limitation retained, archive not repaired |
| Fresh verified Round 04 | Same dataset; current audit script + git HEAD + environment in audit JSON | V9 and current English V8 files unchanged before/after; reference metrics/predictions verified | Audit exit 0; L2 outcome BLOCKED |
| Fresh public metadata screen | Two pinned new repository revisions; documentation/tree hashes retained | 0 prompt payloads; 0 eligible families | Metadata-only quarantine |

## Saved English V8 diagnostics — limited comparison evidence

These are saved validation-window results, freshly tied to their original run through hashes and integer prediction counts. They use inherited source mappings, not V9 curator labels. Validation is 153 windows from one source family, with 51 per class. They establish neither V9 performance nor a passing operating point. [1](#local-evidence)

| True class | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| benign | 0.445783 | 37/51 = 0.725490 | 0.552239 | 51 |
| PI | 0.410714 | 23/51 = 0.450980 | 0.429907 | 51 |
| JB | 0.714286 | 10/51 = 0.196078 | 0.307692 | 51 |

Confusion matrix (rows=true, columns=predicted; order benign, PI, JB): `[[37,14,0],[24,23,4],[22,19,10]]`. Macro-F1 is 0.429946; weighted-F1 has the same value because supports are equal; accuracy is 70/153 = 0.457516. Argmax benign FPR is 14/51 = 27.450980%, a class-error metric rather than the route early-BLOCK rate. Weighted-F1 is arithmetic derived here from saved class F1/support, not a newly stored training result. [1](#local-evidence)

### L2 route summary

The following table describes the illustrative, **unselected** V8 `tau_allow=0.90`, `tau_block=0.90` pair. There are two cutoff parameters, 49 evaluated candidate pairs, and zero selected operating points. Ties route to REVIEW; candidate routes are separate from final API outcomes. [1](#local-evidence)

| True label | ALLOW count/rate | REVIEW count/rate | BLOCK count/rate | Unit |
|---|---:|---:|---:|---|
| benign | 4/51 (7.843137%) | 46/51 (90.196078%) | 1/51 (1.960784%) | Saved validation windows |
| PI | 0/51 (0%) | 49/51 (96.078431%) | 2/51 (3.921569%) | Saved validation windows |
| JB | 0/51 (0%) | 46/51 (90.196078%) | 5/51 (9.803922%) | Saved validation windows |

Pooled attack early-ALLOW is 0/102; total REVIEW is 141/153 (92.156863%). REVIEW is potential traffic only: no L3 invocation was observed. This single-family example is not a chosen risk/capacity trade-off and must not be used to declare readiness. [1](#local-evidence)

## Public-source research this round

The existing candidate registry and eligibility matrix were consulted first. Two new prospects were pinned using only publisher documentation and repository-tree metadata; no dataset payload, access agreement, or upstream evaluation split was fetched. Exact revisions, download times, HTTP status and hashes are in the [metadata manifest](public_source_metadata_20261013/manifest.json). [1](#local-evidence)

| Prospect / pinned revision | Publisher evidence | Local screening decision |
|---|---|---|
| In-page injection artifact / `0a04d1762cf60957f954f16a6cb9525ab32d6bca` | Publisher distinguishes sanitized CC BY 4.0 public data from identifying full data requiring a separate access agreement; accompanying software is AGPL-3.0. [Pinned notice](https://raw.githubusercontent.com/SoheilKhodayari/in_page_prompt_injection_pub/0a04d1762cf60957f954f16a6cb9525ab32d6bca/README.md). | QUARANTINE_METADATA_ONLY. Need public-file/schema consistency, row lineage, context suitability, privacy and curator review. No access request and no family credit. |
| Moltbook A2A artifact / `bfc84672cfac45bc8e06f9d4df87ebf16f651918` | Publisher declares CC BY 4.0 for derived data and separate original-archive terms; posts originate from AI agents, with human-reviewed binary attack labels. [Pinned notice](https://raw.githubusercontent.com/mtasci42/moltbook-a2a-prompt-injection/bfc84672cfac45bc8e06f9d4df87ebf16f651918/README.md). | QUARANTINE_METADATA_ONLY. Different agent-post context and derived-source rights/lineage; original labels cannot substitute for PI-Guard curator decisions. No family credit or payload download. |

Neither prospect resolves the current human gates. More unreviewed rows cannot establish canonical class/source coverage; no speculative ingestion or dataset version was created. This is a local workflow decision, not a claim that the public sources are unusable. [1](#local-evidence)

## Remaining weaknesses and evidence limits

- Candidate counts are not class supports. The 20-row pilot is nonrepresentative and overlaps the main queue; assistant proposals remain noncanonical. Single-curator decisions also will not establish independent multi-annotator agreement. [1](#local-evidence)
- Source independence and related collection parents are unresolved. Exact/lexical groups do not rule out unobserved semantic/template leakage. Original split lineage must survive into a reviewed successor. [1](#local-evidence)
- Privacy pattern screening covers only the recorded email/credential patterns; source-level residual personal information has not been reviewed. [1](#local-evidence)
- The original English V8 bundle lists stale hashes for `README.md` and `V8_ENGLISH_INITIALIZATION_TASK_20261012.md`. The model/metrics/prediction hashes match the run manifest. Current archived files were unchanged by the verified audit; the entire archive cannot be called identical to its original bundle manifest. Both discrepancies are recorded, not repaired. [1](#local-evidence)
- The first audit import created three new `.pyc` cache files; exact paths/timestamps were checked and those new files removed. The verified runner globally disables bytecode writes. This operational correction did not alter data or trained model bytes. [1](#local-evidence)
- Historic V9 rounds lack complete execution timestamps/command logs, and no independent complete prior-use access log was supplied. This audit records its own code/environment/commands and preserves these limitations. No test payload was opened to compensate. [1](#local-evidence)

## Blockers and next evidence

Follow [HUMAN_REVIEW_HANDOFF.md](HUMAN_REVIEW_HANDOFF.md): return separate completed curator and source-review records, resolve parent/duplicate independence, and predeclare numeric limits. Then create a new immutable reviewed dataset version; verify 2/1/1 class/family coverage, freeze splits and the input contract, and execute the fixed L2 validation experiment. Hypothesis for the next meaningful experiment: replacing inherited mappings and narrow validation with reviewed, source-disjoint labels may change the observed class/route errors. This is a proposal, not a predicted improvement. [1](#local-evidence)

The current V8 CLI is hard-coded to its old version path and V8-specific gate schema. It is unsuitable for direct V9 execution. Its `build_model` and validation evaluator can be reused in a V9 adapter after canonical schema, privacy/curator gates and split identities exist; the adapter must add missing weighted summaries/latency if required. No duplicate training pipeline was built while these contracts are unresolved. [1](#local-evidence)

## L3 handoff checklist

- [x] English-only scope, rubric, fixed L2 configuration, existing evidence and human-review queues located.
- [x] Fresh candidate integrity/count audit and bounded historical diagnostics recorded.
- [ ] Canonical human labels and adequate per-class/source training support.
- [ ] Rights/lineage and source-level privacy review recorded for accepted rows.
- [ ] Independent source families and per-class 2/1/1 source-disjoint coverage.
- [ ] Duplicate and parent-group decisions; immutable frozen split IDs/hashes and input contract.
- [ ] Numeric early-ALLOW/early-BLOCK/REVIEW/support limits declared before validation selection.
- [ ] Validation-selected operating point meets every official limit, with classwise/sourcewise evidence.
- [ ] Adequate per-class validation REVIEW support and separately adequate intended L3 training support.
- [ ] Prior-use/test boundary supported by authorized records; one-time V9 test only after freeze.
- [ ] Separate explicit authorization for any future L3 training.

**Not enough evidence to begin L3. No L3 was executed.** [1](#local-evidence)

## Test boundary

- Test/source-evaluation payload inspected by this check: **No**.
- Prior use for model or cutoff selection: historical V8 run metadata reports no; an independent complete access record for V9 selection is **unknown**, and no V9 split exists. Readiness is not established.
- No V8 locked payload was read to check overlap. Saved English V8 validation predictions were used only to verify its diagnostic metrics; they were not copied into V9 or used for selection. [1](#local-evidence)

## Scope Compliance Checklist

| Check | Status | Evidence |
|---|---|---|
| Task scope and English-only artifacts | PASS | Current task, report and audit scope |
| No dataset relabeling, synthetic generation, or old-version repair | PASS FOR THIS RUN | Before/after hashes and closed fitting flags |
| No locked evaluation payload / L3 access | PASS FOR THIS RUN | Audited command flow and execution records |
| No commit or publication | PASS FOR THIS RUN | Task execution record |
| Fresh validation of report/artifacts | See verification records | [VERIFICATION.json](VERIFICATION.json) |
| Official L2 readiness | BLOCKED | Human data gates and unspecified acceptance limits |

## Local evidence

<a id="local-evidence"></a>**[1]** Fresh local [audit JSON](run_20261013_round04_verified/audit.json), [audit command/exit record](audit_round04_verified_command.json), [full audit stdout/stderr](audit_round04_verified.log), [self-check log](self_check.log), [execution records](EXECUTION_RECORDS.json), [run ledger](RUN_LEDGER.json), [verification records](VERIFICATION.json), and linked source task/protocol/checkpoint. These are empirical local records and project requirements; no literature performance claim is made.
