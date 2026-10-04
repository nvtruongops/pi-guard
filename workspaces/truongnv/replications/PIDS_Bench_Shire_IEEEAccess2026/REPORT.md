# PIDS-Bench same-paper TF-IDF baseline — local result

**Status:** eligible same-paper local baseline; one seed; binary benign/injection task. No PI-Guard cascade was run.

## Scope Boundary Declaration

- **IN-SCOPE:** verify the PIDS-Bench author TF-IDF + Logistic Regression baseline on the pinned PIDS-Bench release and report primary test metrics from saved predictions.
- **OUT-OF-SCOPE:** external checkpoints from another paper, model-to-model comparison, a three-class PI-Guard result, or a full reproduction of every PIDS-Bench experiment.

## Paper, code, and data

The selected paper is Shire and Kim, *PIDS-Bench: Evaluating Prompt-Injection Detectors Under Over-Defense, Obfuscation, and Distribution Shift*, IEEE Access 2026 [[44]](../../References/REFERENCES_LOG.md#ref44). The author repository is pinned to tag `v1.0-pids-bench`, commit `87dc835566b930ee921240874a4939b2c266c2fe`; it supplies the frozen data and word-unigram/bigram TF-IDF + Logistic Regression baseline code [[45]](../../References/REFERENCES_LOG.md#ref45). This report does not use the ProtectAI checkpoint or Deepset/TrustAIRLab snapshots.

The local model is `run_artifacts/tfidf_seed42/model/tfidf_logreg.joblib`, SHA-256 `031b37152cc9401a436cb734224f69e361329a2c66aa8d1b8d811fdd19b702fc`. The local fit uses seed 42 and the paper's baseline implementation. The primary test split is the paper's pinned `upstream/data/pids_bench_v3/test.csv`.

## Verification and primary test metrics

The saved prediction file contains 3,918 rows. An independent check found an exact 3,918/3,918 multiset match for text and binary labels against the pinned test split. Confusion counts and rates below were recomputed from saved probabilities at fixed threshold 0.5; no score was copied from another checkpoint or dataset.

| Metric | Recomputed local value |
|---|---:|
| Accuracy | 96.4012% |
| Macro-F1 | 0.9638 |
| Injection F1 | 0.9663 |
| Injection precision | 95.6028% |
| Injection recall | 97.6812% |
| Benign FPR | 5.0325% |
| ROC-AUC | 0.9942 |
| Confusion matrix `[[TN,FP],[FN,TP]]` | `[[1755,93],[48,2022]]` |

These are local single-seed measurements on the paper's binary test split. They are not a three-class PI-Guard score and do not measure a cascade or production service. PIDS-Bench author-reported aggregate values remain literature results and are not presented here as local measurements [[44]](../../References/REFERENCES_LOG.md#ref44).

## Metric reconciliation

The isolated output's `summary.json` agrees with direct recalculation at threshold 0.5. Its `test_report.txt` contained counts for the validation-selected threshold 0.502 without stating that threshold; the file is relabeled to prevent mixing it with the fixed-threshold table. This report uses threshold 0.5 only.

## Artifacts

- Local fitted model and outputs: [`run_artifacts/tfidf_seed42/`](run_artifacts/tfidf_seed42/).
- Pinned paper code and source release: [`upstream/`](upstream/).
- Withdrawn ProtectAI-on-PIDS-Bench outputs: [`run_artifacts/protectai_reference/`](run_artifacts/protectai_reference/) remain because deletion was blocked. Do not use or cite that mixed-model output folder.
- Workspace-level pairing and residual-folder inventory: [provenance audit](../../reports/experiment_reports/WORKSPACE_PROVENANCE_AUDIT_2026-09-30.md).
