# TF-IDF literature assessment (withdrawn pending source-level correction)

## Scope Boundary Declaration

- **IN-SCOPE:** withdraw unsupported performance statements from the former Meeting 5 literature assessment and point to current evidence.
- **OUT-OF-SCOPE:** attributing local benchmark metrics to literature, claiming an unmeasured PI-Guard latency, or describing a paper's results as a local experiment.

> **Status:** the former assessment has been withdrawn. It attributed `<1 ms` latency to arXiv:2512.19011, which the current paper version does not report; it also assigned the authors to Intel Labs, which is not the affiliation shown on the paper. Its `+26% F1` statement referred to the paper's obfuscated-input comparison and was not a PI-Guard result. The paper evaluates several CPU classifier families and regimes; it does not validate this project's earlier scorecard.

## Current evidence

- The [PIDS-Bench report](../../../../replications/PIDS_Bench_Shire_IEEEAccess2026/REPORT.md) reports its locally measured word-TF-IDF + Logistic Regression baseline separately from the paper's author-reported values.
- The historical Review 2 report records local calculations on mixed-source data and has been withdrawn as current evidence under the paper-origin rule.
- The [workspace provenance audit](../../../experiment_reports/WORKSPACE_PROVENANCE_AUDIT_2026-09-30.md) is the index for verified results and withdrawn artifacts.

## Literature source

Majhi et al., “Do You Really Need a GPU to Guard Your LLM? CPU-Class Classifiers and Multi-Stage Pipelines for Safety Enforcement at Scale,” arXiv:2512.19011 (v3, 2026). The paper reports a 26.1 percentage-point F1 difference for LightGBM versus Gemma-2B LoRA on its D3 obfuscation regime. Those results are literature findings on the paper's protocol, not PI-Guard measurements.
