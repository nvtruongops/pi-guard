# PI-Guard

A machine-learning guardrail for detecting prompt injection and jailbreak attacks on LLM applications. PI-Guard is an academic capstone project at FPT University (IAP491), currently working through Review 2.

## Current project state — 5 October 2026

Review 2 is active. Research runs and drafts in `workspaces/truongnv/` are local working material and are excluded from Git. Only results reviewed and promoted to the official deliverable folders are part of the shared repository; a completed experiment does not establish KPI acceptance or a production service.

## Proposed ingress architecture

![Review 1 proposed ingress architecture, vertical summary](Github-Page/assets/ingress_architecture_review1_summary_vertical.png)

This is the page 2 vertical-summary export from the canonical eight-page [editable Draw.io source](Final-Report/PI_GUARD_INGRESS_ARCHITECTURE.drawio). The standalone export is [PI_GUARD_INGRESS_ARCHITECTURE.png](Final-Report/PI_GUARD_INGRESS_ARCHITECTURE.png); the portal copy above is kept in sync with it.

The figure is a Review 1 proposal. L1 validates, normalizes, and splits input into identified chunks/views. L2 emits one route candidate per chunk: ALLOW candidate, REVIEW, or BLOCK candidate. The API sends REVIEW chunks to L3 and combines L2 candidates with L3 predictions by IDs and coverage. Only the API aggregation/policy stage produces a final request-level ALLOW or BLOCK; only final ALLOW is forwarded to a downstream LLM.

The diagram uses symbolic tau_allow and tau_block parameters. They are assumptions in the proposal, not established project-wide or service cutoffs. The architecture remains a proposal, not an implementation claim.

## Repository map

- [Final-Report](Final-Report/README.md): shared academic deliverables and official progress materials.
- [workspaces](workspaces/README.md): explains the local-only workspace policy; no personal workspace is published here.
- [Documentation portal](Github-Page/index.md): project introduction and research topics.
- [Project governance](AGENTS.md): scope, provenance, and repository maintenance rules.

## Repository maintainer

Nguyễn Văn Trường (`nvtruongops`) is the sole current maintainer and publisher of this repository. `Final-Report/` and `Github-Page/` contain the group capstone progress reports and research outcomes that he consolidates and publishes. Member names in those reports record project progress; they do not mean those members currently maintain or contribute to this Git repository. His research notes, experiments, and drafts stay in the ignored local workspace `workspaces/truongnv/`. Historical Git commit records remain part of the repository history.

## Documentation portal

Install the repository dependencies, then run the portal builder and strict site build from the repository root:

    python Final-Report/scripts/build_docs_portal.py
    mkdocs serve
    mkdocs build --strict

The documentation source and deployment workflow are described in [Github-Page/README.md](Github-Page/README.md).
