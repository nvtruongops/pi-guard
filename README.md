# PI-Guard

A machine-learning guardrail for detecting prompt injection and jailbreak attacks on LLM applications. PI-Guard is an academic capstone project at FPT University (IAP491), currently working through Review 2.

## Current project state — 5 October 2026

Review 2 is active. Research runs and drafts in `workspaces/truongnv/` are local working material and are excluded from Git. Only results reviewed and promoted to the official deliverable folders are part of the shared repository; a completed experiment does not establish KPI acceptance or a production service.

## Proposed ingress architecture

![Review 1 proposed ingress architecture, vertical summary](Github-Page/assets/ingress_architecture_review1_summary_vertical.png)

The figure is a Review 1 proposal. L1 validates, normalizes, and splits input into identified chunks/views. L2 emits one route candidate per chunk: ALLOW candidate, REVIEW, or BLOCK candidate. The API sends REVIEW chunks to L3 and combines L2 candidates with L3 predictions by IDs and coverage. Only the API aggregation/policy stage produces a final request-level ALLOW or BLOCK; only final ALLOW is forwarded to a downstream LLM.

The diagram uses symbolic tau_allow and tau_block parameters. They are assumptions in the proposal, not established project-wide or service cutoffs. The architecture remains a proposal, not an implementation claim.

## Repository map

- [Final-Report](Final-Report/README.md): shared academic deliverables and official progress materials.
- [workspaces](workspaces/README.md): explains the local-only workspace policy; no personal workspace is published here.
- [Documentation portal](Github-Page/index.md): project introduction and research topics.
- [Project governance](AGENTS.md): scope, provenance, and repository maintenance rules.

## Repository maintainer

The Git repository is maintained by Nguyễn Văn Trường (`nvtruongops`). `workspaces/truongnv/` is ignored and remains local; place deliverables intended for review or publication in their official locations outside `workspaces/`. The academic capstone roster is recorded separately and does not define Git repository access.

## Documentation portal

Install the repository dependencies, then run the portal builder and strict site build from the repository root:

    python Final-Report/scripts/build_docs_portal.py
    mkdocs serve
    mkdocs build --strict

The documentation source and deployment workflow are described in [Github-Page/README.md](Github-Page/README.md).
