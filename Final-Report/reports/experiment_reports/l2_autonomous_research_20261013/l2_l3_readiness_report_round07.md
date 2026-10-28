# PI-Guard English L2 readiness and L3 handoff assessment — round07

**Run date:** 2026-10-13  
**Overall result:** `BLOCKED`  
**Dataset:** `pi_guard_native_reference_round06_r03`, version `0.6.0-native-reference-candidate`  
**Test access:** family-level aggregate metadata only; no test rows were opened.

## Scope boundary declaration

**IN-SCOPE:** English-only source qualification and versioned train/validation data; reproducible native-label mappings used as research references; L2 baseline training and justified L2-only experiments; validation and source-family-held-out diagnostics; and an assessment of L2 evidence against the requirements for a later, separately authorized L3 task.

**OUT-OF-SCOPE:** L3 training, deployment, or cascade execution; changing old dataset versions or V8 locked evaluations; treating native mappings as curator-reviewed human gold; using assistant-generated prompts; opening test row IDs, text, paths, or payloads; selecting a threshold from test evidence; committing or publishing.

The user removed the wait for curator approval for research-reference experiments and approved the sealed test-family metadata contract. This report uses explicitly documented native labels/mappings only as research references. It does not relabel them as human gold or waive the remaining rights, lineage, privacy, duplicate, split, or metric gates.

During continuation, an out-of-scope L3 diagnostic was mistakenly launched. It was stopped after the user clarified the L2-only boundary; its runner, routed inputs, smoke output and partial run output were removed. Those outputs are not used as evidence, no checkpoint was produced, and no test payload was accessed.

## Outcome

The fixed L2 baseline and one evidence-motivated family-weighting variant both returned `NOT_READY` under the local diagnostic protocol; neither identified an operating point from the 49-pair frozen grid. For both matched-environment fits, 10 pairs met the protocol's provisional PI/JB early-ALLOW and benign early-BLOCK limits, but the lowest REVIEW load among those pairs was 61.97% for the unweighted baseline and 58.97% for family weighting, above the protocol's 50% diagnostic cap. The family-weighted run slightly improved Wambo validation scores but reduced pooled family-held-out OOF macro-F1. No further L2 hypothesis is supported by these runs.

The exploratory protocol limits were recorded before the round06 sweep, but they are engineering assumptions rather than an owner-approved project rubric. The formal L2 acceptance status is therefore `GATE_UNSPECIFIED`; this report cannot call the result an official L2 `PASS` or `FAIL`. The project target of benign API false-positive rate below 1.5% has not been evaluated at API level. L2 validation argmax benign FPR was 2.90–3.06%, a separate window-level diagnostic; local batch-one L2 P95 latency was below 30 ms.

## Data gates

| Gate | Status | Evidence and boundary |
|---|---|---|
| English-only candidate data | PASS for this research package | Pinned language model SHA-256 `f4f4a2c3465ca1f081541037f9cac23021d68151c2f709c55ae5eedfca522963`, confidence floor 0.95. Round06 added 3nesdeniz train rows only; its other splits stayed closed. |
| Research labels | PASS for reference-label diagnostics; not human gold | Native source labels and explicit mapping rules are versioned in the package. No curator decision is claimed. `roleplay_jailbreak` in 3nesdeniz remains an attack-family value under its binary `prompt_injection` target and was not mapped to project JB. |
| Train support by source family | PASS for minimum counts | Train: benign 13,486, PI 501, JB 1,444. PI occurs in CiberIA (88), NeurAlchemy (14), and 3nesdeniz (399); JB occurs in CiberIA (45), NeurAlchemy (48), and TrustAIR (1,351); benign occurs in all four train families. |
| Validation support and family | PASS for provisional support floor | Wambo validation: benign 1,929, PI 1,760, JB 218; one held-out source family. The source is publisher-described as MIT, but no standalone LICENSE file was found in the pinned tree and the generation/upstream lineage is incomplete. |
| Test family contract | PASS at metadata level only | The approved `pi_guard_sealed_test_families_v1` records deepset support B56/PI60/JB0 and Simsonsun support B0/PI0/JB2,426. It contains no row IDs, text, payload path, or payload hash. These are source-family support counts, not test metrics. |
| Pinned rights and lineage records | PARTIAL | The package records source repositories, revisions, publisher notices, family IDs, and lineage evidence. Publisher license notices are not independent legal opinions. Wambo lineage and generation details remain incomplete; source attribution limits are recorded. |
| Privacy review | PARTIAL | English filtering and email, credential-assignment, and IPv4 pattern quarantines ran. The screen explicitly says this is partial and cannot guarantee absence of personal or sensitive information. 3nesdeniz is synthetic and publisher-reports only a subset manually reviewed; that does not replace a full independent privacy review. |
| Duplicate/split checks | PASS for recorded train/validation checks; PARTIAL for sealed test | Round06 found zero exact normalized overlaps across its source pairs and zero train-to-Wambo near-duplicate pairs at char-ngram cosine ≥0.90. The split and row/provenance hashes are frozen. No row-level duplicate check was run against sealed test, by design. |
| External preview quarantine | PASS as an exclusion control | The recorded `Horizon-Labs/prompt-injection-eval-suite` / `agentic5k_test` preview family `3nesdeniz_5k` is excluded from final-test candidates. The current package test partition remains family metadata only. |

Source counts and filters are in [source_combo_screen_round06.json](source_qualification/source_combo_screen_round06.json), provenance and licenses in the package `source_review.json`, and the immutable package/split manifests in the private workspace. The compact candidate review for this round is [source_search_round07.md](source_search_round07.md).

## Run ledger

All metric rows below are local empirical results on the documented native-reference mappings, not human-gold estimates. `P/R/F1` is per class; validation denominator is 3,907 windows. The baseline is Dual TF-IDF (word 1–3, char 3–5, sublinear TF) + balanced Logistic Regression (`C=2`, `max_iter=1000`, `lbfgs`, seed 42). The family-weighted variant changes only `sample_weight`: each represented train family receives equal total weight; all baseline hyperparameters remain fixed.

| UTC time / run | Data and treatment | Validation metrics | OOF / readiness result |
|---|---|---|---|
| 2026-10-13 00:57 — `l2_native_reference_round05_20261013_r03` | v0.6.0; unweighted fixed baseline; Python 3.11.16 / sklearn 1.9.1 | Macro-F1 .4626, accuracy .5933; benign P/R/F1 .717/.969/.824; PI .992/.140/.245; JB .192/.927/.318; weighted P/R/F1 .812/.593/.535; benign FPR 59/1,929 = 3.06%; P50/P95/P99 4.01/7.28/10.20 ms. | `NOT_READY`; no pair selected. |
| 2026-10-13 01:06 — `l2_oof_family_holdout_round06_r01` | Same package; four source-family-held-out folds; original unweighted baseline | Pooled OOF macro-F1 .3222; per-class F1 benign .576, PI .130, JB .261. TrustAIR held-out fold has 13,796 rows and F1 benign .549 / JB .262. | 37/49 cutoff pairs meet train OOF L3-support counts across ≥2 families; this does not select an L2 route. |
| 2026-10-13 01:17 — `l2_family_balanced_round07_20261013_r01` | Same v0.6.0 package; equal total fit weight per train family; Python 3.14.7 / sklearn 1.9.0 | Macro-F1 .4682, accuracy .5984; benign .782/.971/.866; PI .992/.144/.252; JB .168/.968/.286; weighted P/R/F1 .842/.598/.557; benign FPR 56/1,929 = 2.90%; P50/P95/P99 3.75/6.89/9.40 ms. | `NOT_READY`; no pair selected. |
| 2026-10-13 01:23 — `l2_oof_family_holdout_round07_weighted_r01` | Same family-weighted treatment; four held-out source families | Pooled OOF macro-F1 .3064; per-class F1 benign .541, PI .123, JB .255. | 38/49 pairs meet train OOF L3-support counts; pooled macro-F1 is lower than the environment-matched unweighted baseline. |
| 2026-10-13 01:28 — `l2_native_reference_envmatch_round07_20261013_r01` | Same v0.6.0 package; unweighted baseline rerun under Python 3.14.7 / sklearn 1.9.0 for a fair comparison | Metrics exactly match the earlier baseline: macro-F1 .4626, accuracy .5933, PI recall .1398, JB recall .9266, FPR .03059; P50/P95/P99 3.81/7.45/9.86 ms. | `NOT_READY`; no pair selected. |
| 2026-10-13 01:34 — `l2_oof_family_holdout_round08_envmatched_r01` | Same unweighted baseline under the family-weighted run's Python/sklearn environment | Pooled OOF macro-F1 .3222; per-class F1 benign .576, PI .130, JB .261. | 37/49 train OOF-support pairs; confirms the weighting result is not explained by the runtime version change. |

Run manifests bind package, split, protocol, adapter/helper hashes, seed, environment, and model/metric artifact hashes where applicable. The family-weighted run's manifest omitted environment fields; [execution_environment_round07.json](execution_environment_round07.json) supplies the interpreter, dependency versions, command, and code hashes for that run and its OOF report.

### Threshold result

The protocol grid is `{0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99}` for both `tau_allow` and `tau_block`. The policy sends input to REVIEW unless benign or aggregate attack probability clears its own threshold and strictly dominates the other. The frozen research limits are PI/JB early-ALLOW ≤1.5% each, benign early-BLOCK ≤1.5%, REVIEW ≤50%, and validation support/review floors.

For both the unweighted and family-weighted environment-matched validation fits, 10 pairs meet the three risk-rate limits, but zero also meet the REVIEW cap. The best risk-feasible unweighted pair is `.95/.70`: REVIEW 2,421/3,907 = 61.97%, PI early-ALLOW 19/1,760 = 1.08%, JB early-ALLOW 0/218, benign early-BLOCK 15/1,929 = 0.78%. The best risk-feasible family-weighted pair is also `.95/.70`: REVIEW 2,304/3,907 = 58.97%, PI early-ALLOW 9/1,760 = 0.51%, JB early-ALLOW 0/218, benign early-BLOCK 19/1,929 = 0.98%. The family-weighted result lowers REVIEW by 2.99 percentage points but remains 8.97 points above the cap. By contrast, the unweighted `.80/.90` pair keeps REVIEW at 47.76% but allows 191/1,760 PI windows early (10.85%), violating the attack limit.

The complete per-class metrics, confusion matrices, and all 49 routing pairs are retained in the private run `metrics.json` files; no threshold was selected from test data.

## L2 handoff assessment (no L3 execution)

Train OOF REVIEW support was sufficient for conditional handoff diagnostics for 37 unweighted and 38 family-weighted grid pairs, with per-class counts and at least two supporting source families. However, none of the matching validation operating points met the local diagnostic limits, and the formal acceptance limits remain unspecified. No L2 operating point is selected for handoff. L3 execution is outside this task.

The existing L3 trainer compatibility/runtime items belong to a later, separately authorized task and were not investigated further here. The mistaken diagnostic launch described above produced no accepted L3 evidence; its generated files were removed.

## Required handoff checklist

- [x] English train candidate has pinned revisions, explicit source mappings, and a frozen v0.6.0 manifest.
- [x] Minimum train support is present in at least two source families per label; validation has all three labels in its own family.
- [x] Train/validation exact-overlap and recorded near-duplicate checks pass; test remains metadata-only and unopened.
- [x] Fixed L2 baseline, 49-pair validation sweep, four-family OOF, and one evidence-based family-weighting trial are recorded.
- [x] Local latency P95 is below 30 ms for both environment-matched validation fits.
- [ ] Official L2 `PASS` rubric is established; it is currently `GATE_UNSPECIFIED`, and the local protocol limits are only diagnostics.
- [ ] Evaluate the project benign API FPR target `<1.5%` at API level after an authorized, frozen cascade evaluation; L2 argmax FPR of 2.90–3.06% is a distinct metric.
- [ ] Rights/lineage and full privacy review are closed to the level required for the intended use; current source notices and pattern scans do not establish that.
- [ ] A validation-selected L2 threshold pair is locked; none exists, so L3 routing is undefined.
- [ ] Adapt the L3 input contract to package v0.6.0 and provision a compatible CUDA/PyTorch runtime after the L2 route is locked.
- [ ] Open the single sealed final test only after all model, threshold, and evaluation choices are locked under the approved procedure.

## Final status

`BLOCKED` / health-check `NOT_READY`. The data package supports reproducible research-reference L2 experiments, but the formal project acceptance rubric is `GATE_UNSPECIFIED`, no operating point meets the local diagnostic limits, and source privacy review is partial. API-level FPR was not measured. This task stops at L2; the sealed test remains unopened, and no L3 result is accepted or used.

## Local evidence

- [Owner L2 gate declaration template — limits remain null](../l2_v9_health_check_20261013/OWNER_GATE_DECLARATION.json)
- [PI-Guard L2 Health Check criteria](../../../../.agents/skills/l2-health-check/SKILL.md)
- [Round06 source qualification screen](source_qualification/source_combo_screen_round06.json)
- [Round07 source search](source_search_round07.md)
- [Unweighted OOF, environment matched](l2_oof_family_holdout_round08_envmatched_r01.json)
- [Family-weighted validation metrics](l2_family_balanced_validation_round07_r01.json)
- [Family-weighted OOF metrics](l2_oof_family_holdout_round07_weighted_r01.json)
- [Environment and execution addendum](execution_environment_round07.json)
- [Private package manifest](../../../../workspaces/truongnv/pi_guard_pipeline/training_bases/datasets/project_training/versions/pi_guard_native_reference_round05_20261013_r03/DATASET_MANIFEST.json)
- [Private unweighted validation run](../../../../workspaces/truongnv/pi_guard_pipeline/training_bases/pi_guard_tfidf_tier1/runs/l2_native_reference_envmatch_round07_20261013_r01/run_manifest.json)
- [Private family-weighted validation run](../../../../workspaces/truongnv/pi_guard_pipeline/training_bases/pi_guard_tfidf_tier1/runs/l2_family_balanced_round07_20261013_r01/run_manifest.json)

## Publisher and literature references

- [CiberIA PromptRisk v1](https://huggingface.co/datasets/gcjordi/CiberIA-PromptRisk-v1)
- [NeurAlchemy Prompt Injection and Jailbreak Detection Dataset](https://huggingface.co/datasets/neuralchemy/Prompt-injection-dataset)
- [TrustAIRLab in-the-wild jailbreak prompts](https://huggingface.co/datasets/TrustAIRLab/in-the-wild-jailbreak-prompts)
- [3nesdeniz Agentic Prompt-Injection Boundary Pairs](https://huggingface.co/datasets/3nesdeniz/agentic-prompt-injection-boundary-pairs)
- [Wambo prompt injections](https://huggingface.co/datasets/wambosec/prompt-injections)
- [deepset prompt injections](https://huggingface.co/datasets/deepset/prompt-injections)
- [Simsonsun JailbreakPrompts](https://huggingface.co/datasets/Simsonsun/JailbreakPrompts)
- [JailbreakDB publisher card](https://huggingface.co/datasets/rux22/JailbreakDB); [SoK paper](https://arxiv.org/html/2510.15476)
- [GA Jailbreak Benchmark](https://huggingface.co/datasets/GeneralAnalysis/GA_Jailbreak_Benchmark)
- [WildJailbreak](https://huggingface.co/datasets/allenai/wildjailbreak)
- [JailJudge](https://huggingface.co/datasets/zdxnlp/JailJudge)
