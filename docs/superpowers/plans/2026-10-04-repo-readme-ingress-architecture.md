# README and ingress architecture documentation implementation plan

> **For agentic workers:** Execute this plan task by task. Steps use checkbox syntax for progress tracking.

**Goal:** Synchronize active PI-Guard README files and the documentation landing page with current Review 2 evidence, and clarify L2/L3 routing and threshold assumptions in the proposed architecture diagram.

**Architecture:** Use Review 2 task and experiment reports as the current progress sources, while preserving frozen reports and third-party source documentation. Keep L2 route candidates distinct from final API request decisions, and make the distinction between symbolic proposal cutoffs and one-run validation-selected gates explicit.

**Tech Stack:** Markdown, Draw.io XML, Python documentation generator, MkDocs Material.

**Spec:** [`../specs/2026-10-04-repo-readme-ingress-architecture-design.md`](../specs/2026-10-04-repo-readme-ingress-architecture-design.md)

## Global Constraints

- Do not edit `CAPSTONE PROJECT REGISTER.md` or `docs/fpt_capstone_guide/`.
- Preserve previous report README files and nested upstream, paper, dataset, run-artifact, and withdrawn-evidence README files.
- Treat L2 ALLOW/BLOCK as chunk candidates; only API aggregation emits final request ALLOW/BLOCK.
- Mark architecture cutoffs as symbolic assumptions, not accepted service settings; keep experiment-specific thresholds scoped to their run.
- Preserve the existing dirty PIDS-Bench upstream submodule state.

---

### Task 1: Reconcile project state in active README indexes

**Files:**
- Modify: `README.md`, `workspaces/README.md`, `workspaces/truongnv/README.md`
- Modify: active `Final-Report/**/README.md` indexes and current `workspaces/truongnv/docs/**/README.md`, `reports/README.md`, `reports/tasks_for_review2/README.md`, `replications/README.md`, `src/README.md`, and `tests/README.md`
- Preserve: frozen meeting/review folders, external/reference repositories, datasets, and run-artifact README files

- [x] Add a consistent current-status summary: Review 2 umbrella task open; seed-42 cascade experiment complete; proposal architecture not a deployed service.
- [x] Distinguish package metadata `0.1.0`, last recorded workspace snapshot `v2.2-baseline-freezing-meeting6` (2026-09-24), and active Review 2 progress (2026-10-04).
- [x] Remove stale two-tier/ONNX/INT8-as-current, old milestone-only, nonexistent-path, and unsupported KPI claims from active README files.
- [x] Keep paper-matched local results and project proposal claims linked to their current source reports.

### Task 2: Correct and clarify the proposed ingress Draw.io routes

**Files:**
- Modify: `workspaces/truongnv/reports/report for review 1 lan 2/REVIEW1_PROPOSED_INGRESS_ML_ARCHITECTURE.drawio`

- [x] In the summary and L2 pages, make the three per-chunk candidate routes visible: ALLOW candidate to API aggregation, REVIEW to L3, and BLOCK candidate to API aggregation.
- [x] Label API aggregation as the sole source of final request ALLOW/BLOCK; never connect an L2 candidate directly to the target LLM.
- [x] Add a visible note that `τ_allow`/`τ_block` are symbolic proposal parameters, not established service cutoffs. Mention the separate seed-42 validation-selected experiment gates are run-specific.
- [x] Parse the Draw.io XML and verify the edges and labels after editing.

### Task 3: Publish the architecture image on the root README and portal home

**Files:**
- Modify: `README.md`, `Github-Page/README.md`, `Github-Page/index.md`
- Modify: `Final-Report/scripts/build_docs_portal.py` homepage/asset generation only if needed to preserve the image after regeneration
- Create: `Github-Page/assets/ingress_architecture_review1_summary_vertical.png`

- [x] Embed the supplied architecture image with descriptive alt text.
- [x] Make the generator's homepage template include the same architecture explanation and copy the source image to the portal asset path.
- [x] Do not run a portal-clean step that deletes existing topic pages while their source mapping is stale.

### Task 4: Verify the documentation result

**Files:** All files changed in Tasks 1–3.

- [x] Check relative Markdown links and local image targets in edited README files.
- [x] Run `mkdocs build --strict` against the resulting checked-in portal content.
- [x] Run `git diff --check` and inspect the final diff and status; confirm no frozen or excluded README changed.
- [x] Run `codegraph sync .` after the significant documentation/source-template changes.
