# PI-Guard

A machine-learning guardrail for detecting prompt injection and jailbreak attacks on LLM applications. PI-Guard is an academic capstone project at FPT University (IAP491), currently working through Review 2.

## Current project state — 4 October 2026

- The Review 2 umbrella task is open. Its scope is a real inference demo and traceable experiment evidence; completion does not imply final KPI acceptance or a production service.
- The seed-42 TF-IDF → DeBERTa cascade experiment is complete on one pinned PIDS-Bench split. It is local experimental evidence, not a validated service policy.
- The proposed ingress design has L1 input handling, L2 TF-IDF + Logistic Regression scoring, L3 DeBERTa review, and API-level request aggregation. The proposed service/API flow is not integrated as a deployed cascade.
- Version references have different meanings: Python package metadata is 0.1.0; the last recorded workspace snapshot is v2.2-baseline-freezing-meeting6 dated 24 September 2026; active research progress is Review 2 as of 4 October 2026. No new formal release is recorded here.

## Proposed ingress architecture

![Review 1 proposed ingress architecture, vertical summary](Github-Page/assets/ingress_architecture_review1_summary_vertical.png)

The figure is a Review 1 proposal. L1 validates, normalizes, and splits input into identified chunks/views. L2 emits one route candidate per chunk: ALLOW candidate, REVIEW, or BLOCK candidate. The API sends REVIEW chunks to L3 and combines L2 candidates with L3 predictions by IDs and coverage. Only the API aggregation/policy stage produces a final request-level ALLOW or BLOCK; only final ALLOW is forwarded to a downstream LLM.

The diagram uses symbolic tau_allow and tau_block parameters. They are assumptions in the proposal, not established project-wide or service cutoffs. A separate seed-42 experiment selected gates on its validation split; those gates are specific to that run and do not define service policy. The architecture remains a proposal, not an implementation claim.

## Review 2 experiment evidence

The [cascade report](workspaces/truongnv/reports/experiment_reports/tfidf_deberta_cascade_2026-10-04/REPORT.md) records one seed, one pinned split, and held-out predictions. Selected held-out results:

| Slice | Local result | Limit |
|---|---:|---|
| PIDS-Bench IID attack test, n=3,918 | Cascade attack F1 98.89% | Same as the local DeBERTa model on this run |
| Hard-benign, n=808 | Cascade FPR 43.94% | High false-positive rate on this slice |
| Obfuscated attacks, n=405 | Cascade recall 98.27% | One reported attack slice |
| Domain-OOD attacks, n=2,000 | Cascade attack F1 97.54% | One reported OOD slice |
| Structural-OOD benign, n=999 | Cascade FPR 79.68% (796/999) | Severe false positives on this slice |
| Model inference timing, 200 balanced prompts | Cascade P95 155.03 ms | RTX 3060 laptop; model inference only, not end-to-end service latency |

These results do not establish the project FPR or latency targets. Read the [Review 2 task](workspaces/truongnv/reports/tasks_for_review2/TASK.md) and the experiment report for protocol, provenance, and limits.

## Repository map

- [Final-Report](Final-Report/README.md): shared academic deliverables and official progress materials. Current experiment artifacts remain in the leader workspace until they are explicitly consolidated.
- [workspaces](workspaces/README.md): member workspaces and ownership boundaries.
- [Active Review 2 reports](workspaces/truongnv/reports/README.md): current task, experiment, and evidence indexes. Older report folders are retained as references.
- [Documentation portal](Github-Page/index.md): project introduction and research topics.
- [Project governance](AGENTS.md): scope, provenance, workspace, and review rules.

## Documentation portal

Install the repository dependencies, then run the portal builder and strict site build from the repository root:

    python Final-Report/scripts/build_docs_portal.py
    mkdocs serve
    mkdocs build --strict

The documentation source and deployment workflow are described in [Github-Page/README.md](Github-Page/README.md).

## Team

| Member | Student ID | Workspace |
|---|---|---|
| Nguyễn Văn Trường, lead | SE182034 | [truongnv](workspaces/truongnv/) |
| Nguyễn Quí Đức | SE182087 | [ducnq](workspaces/ducnq/) |
| Phạm Minh Hoàng Việt | SE181851 | [vietpmh](workspaces/vietpmh/) |
| Đỗ Đoàn Duy Phương | SE180235 | [phuongddd](workspaces/phuongddd/) |
