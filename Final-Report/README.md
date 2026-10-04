# Final-Report — shared academic deliverables

This folder holds tracked capstone materials, the official progress workbook, thesis files, and QA/documentation tools. The academic team history belongs to the project record; this repository itself has one maintainer.

## Project status — 5 October 2026

Review 1 progress is recorded as complete. Review 2 is active and its umbrella task remains open. Personal experiment reports and run artifacts under `workspaces/truongnv/` are local-only and are not part of these shared deliverables. No Review 2 metrics are asserted here without a tracked, provenance-backed report.

The ingress architecture available as an editable [Draw.io source](PI_GUARD_INGRESS_ARCHITECTURE.drawio) and [PNG preview](PI_GUARD_INGRESS_ARCHITECTURE.png) is a proposal. It does not claim that every component is implemented or that project KPIs have been accepted. L2 emits per-chunk ALLOW/REVIEW/BLOCK candidates; the API routes REVIEW chunks to L3, retains the other candidates, verifies coverage, and alone emits the final request ALLOW/BLOCK decision. Only final ALLOW reaches the target LLM. The `τ` values remain proposal assumptions.

## Contents

- [Thesis and chapter files](thesis/README.md): shared academic deliverable drafts.
- [References](References/README.md): canonical tracked literature index and open-access PDFs.
- [Reports](reports/README.md): official process workbook and supervisor presentation.
- [Research notebooks](notebooks/README.md): tracked template/scaffold status and configuration boundaries.
- [Source scaffold](src/README.md) and [test scaffold](tests/README.md).
- [Scripts](scripts/): local validation, report generation, and documentation portal tooling.

Place material intended for review or publication in its task-designated tracked location. The local-only workspace is not a source of committed reports. Do not edit the immutable project register or the FPT capstone guide.
