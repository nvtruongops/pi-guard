# Workspace provenance and metric audit — 2026-09-30

## Scope Boundary Declaration

- **IN-SCOPE:** files, folders, model assets, datasets, metrics, references, and reports under `workspaces/truongnv/`.
- **OUT-OF-SCOPE:** other member workspaces, shared production files, and canonical upstream repositories outside this workspace.

## Governing provenance rule

A locally reported result is eligible only when the evaluated method/model and data protocol belong to the same paper's pinned release or exact paper-defined experiment. Do not combine a checkpoint from Paper A with a dataset or suite assembled for Papers B/C/D and present the result as evidence. Public file hashes establish file origin; they do not validate a cross-paper experiment. Project-created prompts, labels, or splits are not source evidence. Literature values must be labeled and cited separately from local measurements.

## Current metric disposition

| Run family | Provenance check | Current disposition |
|---|---|---|
| PIDS-Bench TF-IDF + Logistic Regression | Same-paper author baseline code and pinned data. All 3,918 saved test text/label pairs match the pinned test split. Recalculation at threshold 0.5 gives confusion `[[1755,93],[48,2022]]`, accuracy 96.4012%, macro-F1 0.9638, injection F1 0.9663, recall 97.6812%, benign FPR 5.0325%, ROC-AUC 0.9942. Model SHA-256: `031b37152cc9401a436cb734224f69e361329a2c66aa8d1b8d811fdd19b702fc`. | Retain this same-paper TF-IDF result only. Sources: [[44]](../../References/REFERENCES_LOG.md#ref44) [[45]](../../References/REFERENCES_LOG.md#ref45). |
| PIGuard checkpoint on PIGuard-released public evaluation assets | Source verifier passed six data-file hashes and 1,435 input rows. PIGuard checkpoint revision is pinned; its saved predictions recompute the listed NotInject/BIPIA/WildGuard slices. | Retain PIGuard-only slice results. BIPIA inputs are payloads, not full task/context prompts. Source: [[18]](../../References/REFERENCES_LOG.md#ref18). |
| ProtectAI checkpoint on PIGuard or PIDS-Bench data | Checkpoint and data belong to different papers under the user's strict pairing rule. | Withdraw local metrics, tables, and dependent figures. |
| Review 1 public-vector suite | Multiple public source families were assembled and evaluated with checkpoints from other releases. | Withdraw corpus/sample counts as experimental evidence, predictions, latency, charts, and offline replay. |
| D1–D6 six-checkpoint matrix | Six checkpoints were paired with six dataset origins rather than each paper's own protocol. | Withdraw all matrix metrics and recommendations. |
| Review 2 and Tier 1 TF-IDF bundles | Project-built fits/splits combine Deepset and TrustAIRLab data rather than one matching paper protocol. | Withdraw metrics, models, predictions, charts, and dependent claims. |
| Meeting 4/5/6 legacy indicators | Prior audit found project-built or cross-paper inputs and unsupported protocol attribution. | Do not use as empirical claims; references are replaced with status notices. |

## Metric reconciliation

The PIDS-Bench test prediction file was matched to the pinned test CSV by exact text/label multiset: 3,918/3,918. Confusion counts and rates above were recomputed from saved scores at threshold 0.5. The isolated run's summary agrees. Its test_report.txt had counts for the validation-selected threshold 0.502 but omitted the threshold label; it is being relabeled to avoid confusion. No prompt text was authored for this retained evaluation.

The PIGuard rerun verifier returned `status=verified`, six source hashes, and 1,435 matched input IDs. That mixed bundle also contains ProtectAI predictions and a two-checkpoint offline replay; those outputs are cross-paper and withdrawn. Only the PIGuard checkpoint results on PIGuard-released assets are eligible. No retained result establishes a PI-Guard three-class model, cascade, production readiness, or system-wide latency/FPR target.

## Requested cleanup and current filesystem state

The user authorized removal of data/result folders that combine a model from one paper with other papers' datasets. Automatic approval review rejected the recursive deletion operation; that rejected operation removed no files. Physical cleanup is therefore incomplete. The following identified folders remain and must not be cited, run, or used to regenerate evidence:

| Remaining folder | Current inventory | Disposition |
|---|---:|---|
| `replications/02_DeBERTa_v3_Semantic_Classifier/datasets/D1_D6_raw/` | 54 files, 22.46 MiB | Mixed paper-origin evaluation inputs for withdrawn matrix; remove when deletion is allowed. |
| `replications/02_DeBERTa_v3_Semantic_Classifier/reports/review1_public_vector_benchmark_2026-09-29/` and `results/review1_public_vector_benchmark_2026-09-29/` | 77 / 14.51 MiB and 12 / 0.20 MiB | Cross-paper public-vector inputs, predictions, and metrics; withdrawn. |
| `replications/02_DeBERTa_v3_Semantic_Classifier/reports/d1_d6_six_model_matrix_2026-09-30/` and `results/d1_d6_six_model_matrix_2026-09-30/` | 110 / 72.37 MiB and 40 / 49.59 MiB | Six checkpoints paired with other papers' datasets; withdrawn. |
| `replications/02_DeBERTa_v3_Semantic_Classifier/reports/review1_paper_model_public_rerun_2026-09-30/` and `results/review1_paper_model_public_rerun_2026-09-30/` | 19 / 0.67 MiB and 6 / 0.04 MiB | Mixed outputs. PIGuard-on-PIGuard rows are eligible; ProtectAI/joint rows are withdrawn, so the bundle needs separation before deletion. |
| `replications/02_DeBERTa_v3_Semantic_Classifier/upstream/checkpoints/` | 52 files, 3,679.94 MiB; six checkpoint directories | Original model-source snapshots for DeepSetDeBERTa, FMOPSDistilBERT, InjectionSentry, PIGuard, ProtectAI, and WolfDefenderSmall. These are not fabricated datasets, but the bundle supported withdrawn cross-paper comparisons and must not be used to rerun them. |
| `replications/01_TFIDF_Syntactic_Baseline/datasets/public_sources/` | 7 files, 13.86 MiB | Mixed Deepset/TrustAIRLab source snapshots used by withdrawn project-built fits. |
| `replications/01_TFIDF_Syntactic_Baseline/reports/review2_baselines_2026-09-29/` and `results/review2_baselines_2026-09-29_WITHDRAWN/` | 39 / 63.61 MiB and 12 / 15.17 MiB | Project-built mixed-source fits, models, predictions, and metrics; withdrawn. |
| `replications/01_TFIDF_Syntactic_Baseline/reports/tier1_tfidf_public_evidence_2026-09-30/` and `results/tier1_tfidf_public_evidence_2026-09-30_WITHDRAWN/` | 18 / 17.24 MiB and 10 / 3.39 MiB | Mixed-source TF-IDF fit and dependent artifacts; withdrawn. |
| `replications/Tier1_Candidate_Meta_PromptGuard2024/` | 23 files, 2.16 MiB | Disabled candidate; official checkpoint was gated and its former proxy used project-authored rows. Folder removal was separately authorized but blocked; no Meta result is valid. |
| `reports/report_for_review1/two_model_benchmark/` | 43 files, 25.69 MiB | PIDS-Bench data and valid PIDS artifacts are mixed with withdrawn ProtectAI outputs; retain no comparison from this bundle. |
| `reports/report_for_review1/section4_images/` and `replications/02_DeBERTa_v3_Semantic_Classifier/report_for_review1/section4_images/` | 5 files each, 0.48 MiB each | Duplicate proposal/evidence images; images 03/04 contain withdrawn project-fit or cross-paper outputs. |
| `replications/PIDS_Bench_Shire_IEEEAccess2026/run_artifacts/protectai_reference/` | 15 files, 0.88 MiB | ProtectAI-on-PIDS output and copied files; withdrawn. The isolated PIDS TF-IDF run remains at `run_artifacts/tfidf_seed42/`. |
| `reports/experiment_reports/reproduction_audit_2026-09-29/` | 46 files, 23.06 MiB | Historical cross-paper suites and results; withdrawn. |
| `reports/tasks_for_meeting_5/figures/` | 21 images, 2.30 MiB (22 files including README) | Includes local-vs-paper comparison charts and figures derived from withdrawn metrics; do not use or regenerate. |
| `reports/tasks_for_meeting_5/tools/generate_diagrams.py` and `generate_meeting_5_presentation.py` | Both files remain | Generators for historical slides/figures; do not run against withdrawn benchmark artifacts. |
| `reports/report_for_meeting_4/tools/generate_diagrams.py`, `generate_presentation.py`, and `figures/PI-GUARD-Present-109/slide16_tier1_tfidf_ngram_mechanism_jain2023.png` | Both generators and the image remain | Historical generated material associated with the withdrawn Tier 1 report. |
| `reports/tasks_for_meeting_6/scripts/run_cross_dataset_benchmark.py` and `inspect_meeting_6_rigor.py` | Two Python stop-only stubs | The benchmark runner and old artifact auditor are retired; the former auditor's “100%” artifact/completeness checks were not valid evidence. |

Source-origin PIGuard evaluation assets at `replications/02_DeBERTa_v3_Semantic_Classifier/datasets/public_evaluation_assets/` (8 files, 0.56 MiB) and the isolated PIDS-Bench `tfidf_seed42` run are retained as same-paper evidence. Other canonical paper/code references remain reference material, not local experiment results. This audit does not claim the listed folders were deleted.

The retired `reports/tasks_for_meeting_6/data/cross_dataset_suite/` directory currently contains only its README (one file); the dataset payloads are absent. That status stub is not evidence that the other listed experiment/result folders were removed.

## Verification record

| Check | Result |
|---|---|
| PIDS-Bench TF-IDF source alignment | PASS — exact text/label match for 3,918 test rows. |
| PIDS-Bench TF-IDF metric recomputation | PASS — counts/rates recomputed from saved row scores at threshold 0.5. |
| PIDS-Bench TF-IDF model identity | PASS — file hash matches the retained model artifact. |
| PIGuard source/prediction verifier | PASS — six dataset hashes; 1,435 rows; PIGuard output metrics recomputed. |
| Cross-paper Review 1, D1–D6, Review 2 bundles | WITHDRAWN — provenance rule fails even where prior saved metrics recomputed. |
| Physical cleanup | INCOMPLETE — automatic approval review rejected deletion; no files removed by the rejected operation. |
