# Proposed PI-Guard ingress architecture

![Review 1 proposed ingress architecture, vertical summary](../assets/ingress_architecture_review1_summary_vertical.png)

This diagram summarizes the Review 1 architecture proposal. It is not evidence that an end-to-end service has been integrated or accepted.

## Request flow

1. L1 validates input, normalizes text, creates bounded chunks/views, and preserves their IDs and source references.
2. L2 uses a TF-IDF + Logistic Regression scorer to emit one per-chunk route candidate: ALLOW, REVIEW, or BLOCK.
3. The API sends REVIEW chunks to L3 DeBERTa. During full-path validation, the proposal allows sending every chunk to L3.
4. API aggregation joins L2 candidates and L3 predictions by IDs and checks complete coverage. Only this stage emits final request-level ALLOW or BLOCK; incomplete coverage fails closed.
5. The target LLM is called only after final request ALLOW.

An L2 ALLOW or BLOCK is a chunk-level candidate, not a final request decision. REVIEW is an internal route to L3, not a user-facing or final API decision.

## Threshold status

The diagram’s tau_allow and tau_block are symbolic proposal parameters. No project-wide or service cutoff is established. A separate seed-42 experiment selected gates on its validation split; those gates are specific to the model, data, and split used in that run and do not establish a service policy.

## Current evidence boundary

As of 4 October 2026, the Review 2 umbrella task remains open. The completed seed-42 cascade experiment used one pinned PIDS-Bench split. Its report records held-out attack F1 of 98.89% on the IID test slice (n=3,918), hard-benign FPR of 43.94% (n=808), structural-OOD benign FPR of 79.68% (796/999), and model-only P95 of 155.03 ms on the measured RTX 3060 laptop workload. The hard-benign and structural-OOD false-positive rates remain high, and the measured timing is not end-to-end service latency.

The experiment report and raw provenance remain in the active lead workspace; the portal summary is not a replacement for those artifacts.

## Background reading

- [TF-IDF theory](tfidf_theory_and_math.md)
- [DeBERTa theory](deberta_theory_and_math.md)
- [Earlier two-stage model discussion](two_tier_tradeoffs.md)

The earlier theory pages are background material and do not define validated routing cutoffs or the current service implementation.
