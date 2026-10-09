# Final-Report — shared academic deliverables

This folder holds tracked capstone materials, the official progress workbook, thesis files, and QA/documentation tools. Nguyễn Văn Trường (`nvtruongops`) is the sole current maintainer and publisher of these files. The progress reports summarize the group project and its research outcomes as consolidated by the leader; team names and assignments are project records, not current repository contributions. Historical Git records remain unchanged.

## Project status — 5 October 2026

Review 1 progress is recorded as complete. Review 2 is active and its umbrella task remains open. Personal experiment reports and run artifacts under `workspaces/truongnv/` are local-only and are not part of these shared deliverables. No Review 2 metrics are asserted here without a tracked, provenance-backed report.

The ingress architecture available as an editable [eight-page Draw.io source](reports/PI_GUARD_INGRESS_ARCHITECTURE.drawio) and [PNG preview](reports/PI_GUARD_INGRESS_ARCHITECTURE.png) is a research proposal. The PNG is the vertical-summary preview from page 2. Both files are maintained once in `reports/`; the documentation portal references the same published PNG. It does not claim that every component is implemented or that project KPIs have been accepted. L2 emits per-chunk ALLOW/REVIEW/BLOCK candidates; the API routes REVIEW chunks to L3, retains the other candidates, verifies coverage, and alone emits the final request ALLOW/BLOCK decision. Planned dashboard events show Benign, Prompt Injection, and Jailbreak scores for each L3 window, apart from the API's final status. Only final ALLOW reaches the target LLM. Training, label-overlap rules, and evaluation are separate research steps; the figure is not a trained three-label result.

The [ISO 5807:1985 symbol audit](reports/ISO_5807_1985_SYMBOL_AUDIT.md) explains which basic flowchart shapes informed the diagram. It records that icons, colors, the L1/L2/L3 design, and the three-class model proposal are project choices rather than claims established by the notation standard.

## Contents

- [Thesis and chapter files](thesis/README.md): shared academic deliverable drafts.
- [References](References/README.md): canonical tracked literature index and open-access PDFs.
- [Reports](reports/README.md): official process workbook and canonical ingress architecture files.
- [Research notebooks](notebooks/README.md): tracked template/scaffold status and configuration boundaries.
- [Source status](src/README.md) and [test scaffold](tests/README.md).
- [Scripts](scripts/): local validation, report generation, and documentation portal tooling.

Place material intended for review or publication in its task-designated tracked location. The local-only workspace is not a source of committed reports. The maintainer retains full authority to manage and update repository files.
