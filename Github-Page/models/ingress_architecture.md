# Proposed PI-Guard ingress architecture

![Review 1 proposed ingress architecture, vertical summary](https://raw.githubusercontent.com/nvtruongops/pi-guard/main/Final-Report/reports/PI_GUARD_INGRESS_ARCHITECTURE.png)

This is the vertical-summary export from page 2 of the canonical eight-page [Draw.io source](https://github.com/nvtruongops/pi-guard/blob/main/Final-Report/reports/PI_GUARD_INGRESS_ARCHITECTURE.drawio). The image above loads the single [PNG source](https://github.com/nvtruongops/pi-guard/blob/main/Final-Report/reports/PI_GUARD_INGRESS_ARCHITECTURE.png) maintained in `Final-Report/reports/`.

This diagram summarizes the Review 1 research architecture proposal. It does not report an integrated service or a trained three-label PI-Guard model.

## Request flow

1. L1 validates input, normalizes text, creates bounded chunks/views, and preserves their IDs and source references.
2. L2 uses a TF-IDF + Logistic Regression scorer to emit one per-chunk route candidate: ALLOW, REVIEW, or BLOCK.
3. The API sends only REVIEW chunks to L3 DeBERTa.
4. API aggregation joins L2 candidates and L3 predictions by IDs and checks complete coverage. Only this stage emits final request-level ALLOW or BLOCK; incomplete coverage fails closed.
5. The target LLM is called only after final request ALLOW.

The proposed dashboard sketches Benign, Prompt Injection, and Jailbreak score fields for each L3 window while showing the API's final ALLOW/BLOCK status separately. Training, label-overlap rules, and evaluation are separate research steps; the diagram reports no measured three-label PI-Guard result.

An L2 ALLOW or BLOCK is a chunk-level candidate, not a final request decision. REVIEW is an internal route to L3, not a user-facing or final API decision.

## Diagram notation and icon provenance

The figure uses selected data, process, decision, and line symbols described in [ISO 5807:1985](https://www.iso.org/standard/11955.html). Its dashed outlines group stages and external systems; solid arrows show data or control flow. Color and pictograms help identify PI-Guard components and are not ISO symbols. The [page-by-page symbol audit](https://github.com/nvtruongops/pi-guard/blob/main/Final-Report/reports/ISO_5807_1985_SYMBOL_AUDIT.md) cites the clauses available in the [12-page preview](https://cdn.standards.iteh.ai/samples/11955/1b7dd254a2a54fd7a89d616dc0570e18/ISO-5807-1985.pdf) and explains why it cannot establish full-standard compliance or validate the proposed ML architecture.

## Evidence boundary

This page describes a proposed architecture. It does not claim formal KPI acceptance or deployment.

## Background reading

- [TF-IDF theory](tfidf_theory_and_math.md)
- [DeBERTa theory](deberta_theory_and_math.md)
- [Earlier two-stage model discussion](two_tier_tradeoffs.md)

The earlier theory pages are background material; the current diagram remains a proposal rather than evidence of an integrated service.