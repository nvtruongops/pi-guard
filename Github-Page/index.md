# PI-Guard: LLM Security Guardrail

## PI-Guard Capstone Research

PI-Guard studies an external guardrail for detecting prompt injection and jailbreak attacks before an incoming request reaches a downstream language model.

## Current status

Review 2 is in progress. This portal presents the proposed architecture and research scope; it does not claim formal KPI acceptance or deployment.

## Proposed ingress architecture

![Review 1 proposed ingress architecture, vertical summary](https://raw.githubusercontent.com/nvtruongops/pi-guard/main/Final-Report/reports/PI_GUARD_INGRESS_ARCHITECTURE.png)

This is the vertical-summary export from page 2 of the canonical eight-page [Draw.io source](https://github.com/nvtruongops/pi-guard/blob/main/Final-Report/reports/PI_GUARD_INGRESS_ARCHITECTURE.drawio). The image above loads the single [PNG source](https://github.com/nvtruongops/pi-guard/blob/main/Final-Report/reports/PI_GUARD_INGRESS_ARCHITECTURE.png) maintained in `Final-Report/reports/`.

L1 validates, normalizes, and splits input into identified chunks/views. L2 scores each chunk and emits an ALLOW candidate, REVIEW, or BLOCK candidate. The API sends REVIEW chunks to L3 and joins all results by IDs and coverage. Proposed dashboard events show separate Benign, Prompt Injection, and Jailbreak scores for each L3 window. Only API aggregation/policy emits the final request-level ALLOW or BLOCK; only final ALLOW reaches the downstream LLM. The diagram does not establish a trained three-class model.

The diagram is a Review 1 proposal. Its thresholds are symbolic assumptions, and the proposed service flow has not been accepted as a deployed system.

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