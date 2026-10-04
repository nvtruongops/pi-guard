# PI-Guard — Review 1 evidence status

**Project:** A Machine-Learning Guardrail for Detecting Prompt Injection and Jailbreak Attacks on LLM Applications  
**Evidence cut-off:** 30 September 2026

## Scope Boundary Declaration

- **IN-SCOPE:** current paper-matched local evidence and project limits in `workspaces/truongnv/`.
- **OUT-OF-SCOPE:** withdrawn cross-paper comparisons, a measured three-class PI-Guard model, or a two-tier cascade claim.

## 1. Project objective

PI-Guard is a proposed external text guardrail intended to classify benign prompts, prompt injection, and jailbreak attempts. The system remains a research proposal. An external checkpoint's binary flag is not a PI-Guard three-class prediction and is not evidence that an attack succeeded against a downstream model.

## 2. Evidence rule

Every local result must pair the model/method and evaluation data under the same paper's pinned repository or exact experiment protocol. Original public bytes alone do not validate a cross-paper pairing. Author-reported paper values are literature evidence and remain separate from local measurements. The workspace audit records this rule, the local checks, and residual files [[18]](../../References/REFERENCES_LOG.md#ref18) [[44]](../../References/REFERENCES_LOG.md#ref44) [[45]](../../References/REFERENCES_LOG.md#ref45).

## 3. Eligible local measurements

| Paper-matched run | Verified local result | Scope limit |
|---|---|---|
| PIDS-Bench TF-IDF + Logistic Regression | At threshold 0.5 on the source-matched 3,918-row test split: accuracy 96.4012%, macro-F1 0.9638, injection F1 0.9663, injection recall 97.6812%, benign FPR 5.0325%; confusion `[[1755,93],[48,2022]]`. | One local seed; binary benign/injection. Not a PI-Guard three-class model or cascade. [[44]](../../References/REFERENCES_LOG.md#ref44) [[45]](../../References/REFERENCES_LOG.md#ref45) |
| PIGuard DeBERTa-v3 on assets in the pinned PIGuard release | NotInject correct benign 300/339; BIPIA text payload flags 29/75, code payload flags 49/50; WildGuard benign correct 739/971. Source hashes and 1,435 prediction rows passed the local verifier. | Slice-specific results; BIPIA uses payloads rather than complete task/context prompts. Not the proposed PI-Guard model. [[18]](../../References/REFERENCES_LOG.md#ref18) |

These runs use different papers, labels, datasets, and protocols. They are presented separately and are not a model ranking. Full counts, hashes, and limitations appear in the [PIDS-Bench report](../../replications/PIDS_Bench_Shire_IEEEAccess2026/REPORT.md) and [PIGuard-only report](../../replications/02_DeBERTa_v3_Semantic_Classifier/reports/review1_paper_model_public_rerun_2026-09-30/REPORT.md).

## 4. Withdrawn historical results

The Review 1 public-vector sample, Review 2/Tier 1 mixed-source TF-IDF runs, D1–D6 checkpoint matrix, ProtectAI-on-PIDS/PIGuard outputs, and their dependent comparisons/figures are withdrawn. They pair model and dataset sources from different papers or use project-built splits. Automatic approval review blocked deletion, so those files remain on disk; they must not be cited, run, or used to regenerate evidence.

## 5. Proposed architecture and project targets

A TF-IDF stage followed by a contextual detector may be evaluated later as a design hypothesis. No current local run measures conditional routing, a joint held-out test, or end-to-end cascade latency. P95 < 30 ms and FPR < 1.5% remain project targets, not achieved results.

## 6. Terminology used in this status report

| Term | Definition | Use here | Evidence type |
|---|---|---|---|
| Binary detector | Classifier with two labels for the specified paper task. | PIDS-Bench baseline distinguishes benign from injection. | Paper protocol and local source-matched run. |
| Attack flag rate | Share of attack-labeled source examples flagged by a detector. | Used for PIGuard payload slices; not downstream attack success. | Local saved predictions and source labels. |
| Same-paper pairing | Model/method and dataset follow one paper's pinned release or exact protocol. | Eligibility condition for local metrics in this report. | Repository revision, hashes, and evaluation artifacts. |
| Cascade | Sequential system whose second detector runs conditionally after the first. | Proposed only; no cascade result is claimed. | Project design, not a measurement. |
| P95 latency | 95th percentile of measured request latency under a stated runtime protocol. | Target only; not established by either retained local run. | Project objective, not an empirical fact. |
