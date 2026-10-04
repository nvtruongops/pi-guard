# Final-Report — shared academic deliverables

This folder holds shared capstone materials, the official progress workbook, thesis files, and QA/documentation tools. It is separate from each member’s active workspace.

## Project status — 4 October 2026

Review 1 progress is recorded as complete. Review 2 is now active and its umbrella task remains open. The completed seed-42 cascade experiment and raw provenance are currently in the lead workspace; they have not been consolidated into this shared deliverable. See the [active Review 2 task](../workspaces/truongnv/reports/tasks_for_review2/TASK.md) and [experiment report](../workspaces/truongnv/reports/experiment_reports/tfidf_deberta_cascade_2026-10-04/REPORT.md).

The experiment is one local run on one pinned PIDS-Bench split. Its validation-selected gates are run-specific; high hard-benign and structural-OOD false-positive rates and model-only P95 of 155.03 ms remain reported limitations. It does not constitute final KPI acceptance or service implementation.

## Final ingress architecture for the report

The final architecture package selected for this report is available as an editable [Draw.io source](PI_GUARD_INGRESS_ARCHITECTURE.drawio) and [PNG preview](PI_GUARD_INGRESS_ARCHITECTURE.png). The Draw.io file is the canonical source; the PNG previews its request-level UML Activity Diagram.

This is the report's final **proposed architecture artifact**. It does not claim that every component is implemented or that project KPIs have been accepted. L2 emits per-chunk ALLOW/REVIEW/BLOCK candidates; the API routes REVIEW chunks to L3, retains the other candidates, verifies coverage, and alone emits the final request ALLOW/BLOCK decision. Only final ALLOW reaches the target LLM. The `τ` values remain proposal assumptions, and validation-selected gates from seed-42 apply only to that run.

## Contents

- [Thesis and chapter files](thesis/README.md): shared academic deliverable drafts.
- [References](References/README.md): literature index and local reference collection.
- [Reports](reports/README.md): official process workbook and supervisor presentation.
- [Research notebooks](notebooks/README.md): current template/scaffold status and configuration boundaries.
- [Source scaffold](src/README.md) and [test scaffold](tests/README.md).
- [Scripts](scripts/): local validation, report generation, and documentation portal tooling.

The shared source, test, notebook, data, and model directories are not the active location of the Review 2 cascade artifacts. Consolidate only through the project’s task and workspace governance. Do not edit the immutable project register or the FPT capstone guide.
