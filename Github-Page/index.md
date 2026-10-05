# PI-Guard: LLM Security Guardrail

## FPT University Information Assurance Capstone · IAP491 · Fall 2026

PI-Guard studies an external guardrail for detecting prompt injection and jailbreak attacks before an incoming request reaches a downstream language model.

## Current status — 4 October 2026

Review 2 is active and its umbrella task remains open. A separate seed-42 TF-IDF → DeBERTa cascade experiment is complete on one pinned PIDS-Bench split. This is local experimental evidence, not final KPI acceptance or a deployed service.

## Proposed ingress architecture

![Review 1 proposed ingress architecture, vertical summary](assets/ingress_architecture_review1_summary_vertical.png)

This is the vertical-summary export from page 2 of the canonical eight-page [Draw.io source](https://github.com/nvtruongops/pi-guard/blob/main/Final-Report/PI_GUARD_INGRESS_ARCHITECTURE.drawio). The corresponding standalone PNG is [PI_GUARD_INGRESS_ARCHITECTURE.png](https://github.com/nvtruongops/pi-guard/blob/main/Final-Report/PI_GUARD_INGRESS_ARCHITECTURE.png).

L1 validates, normalizes, and splits input into identified chunks/views. L2 scores each chunk and emits an ALLOW candidate, REVIEW, or BLOCK candidate. The API sends REVIEW chunks to L3 and joins all results by IDs and coverage. Only API aggregation/policy emits the final request-level ALLOW or BLOCK; only final ALLOW reaches the downstream LLM.

The diagram is a Review 1 proposal. Its tau_allow and tau_block are symbolic assumptions, not established project-wide or service cutoffs. A separate experiment selected gates on its validation split; those gates apply to that run alone. The proposed service flow has not been accepted as a deployed system.

## Experiment evidence and limits

The held-out results in the one-run experiment include attack F1 of 98.89% on the IID PIDS-Bench test slice (n=3,918), FPR of 43.94% on hard-benign (n=808), FPR of 79.68% on structural-OOD benign (796/999), and model-only P95 of 155.03 ms on the measured RTX 3060 laptop workload. High false positives and latency remain limitations. These results do not establish service targets.

For the current architecture explanation and evidence limits, see [Proposed ingress architecture](models/ingress_architecture.md). The active task and complete provenance remain in the repository workspace.

## Research topics

| Topic | Guide |
|---|---|
| Prompt study | [LLM foundations](prompt_study/llm_foundations.md) |
| Attack study | [Attack history and taxonomy](attacks/history_and_evolution.md) |
| Threat and defense | [Threat model](threat_defense/threat_model_and_attack_surface.md) |
| Dataset and benchmarks | [Data curation](dataset_study/data_curation.md) |
| Model study | [Ingress architecture](models/ingress_architecture.md) |
| Robustness and evasion | [Evasion mechanisms](robustness/theory_and_evasion_mechanisms.md) |
| Evaluation | [False-positive economics](evaluation_study/false_positive_economics.md) |

## Version references

Python package metadata is 0.1.0. The last recorded workspace snapshot is v2.2-baseline-freezing-meeting6, dated 24 September 2026. The active research state is Review 2 as of 4 October 2026; these references are not a new release.
