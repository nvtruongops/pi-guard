# Historical replication cleanup — status only

This page replaces an earlier disposition note whose file/path counts and “upstream verified” descriptions were not, by themselves, sufficient to establish source identity or experiment validity. Treat the former folder-level comparison as historical context, not a provenance certificate.

## Current findings

- The Ayub local training file was removed after review found 200 of 344 rows lacked a `source` value. Its dependent result JSONs, notebook, generated plots and feature caches were removed. No local Ayub metric is reportable; see [`Ayub package status`](../../../references_study/rejected_baselines/Tier1_REJECTED_Ayub_CAMLIS2024/README.md).
- Follow-up on 2026-09-30 removed all five remaining Ayub-folder JSON files because they were copies of PIGuard source data rather than Ayub repository data. The current verifier checks that no Ayub data files remain; the original source files remain only in the PIGuard package.
- SmoothLLM behavior files match their corresponding files in the bundled local `upstream/` snapshot. The snapshot has no pinned Git commit; this is local copy-equality only.
- Other replication decisions and limits are in the [current replication-folder audit](../replications_folder_audit_2026-09-30/REPLICATIONS_FOLDER_AUDIT.md). For workspace-wide data/document status, see the [provenance audit](../WORKSPACE_PROVENANCE_AUDIT_2026-09-30.md).

## Scope boundary

- **IN-SCOPE:** correct the status of local replication/reference artifacts and remove derived results tied to unverified data.
- **OUT-OF-SCOPE:** retrain/evaluate models or certify every upstream README and paper claim. Meeting 4 and Meeting 5 deliverables were later reviewed under the user's expanded request; unsupported slides and draft reports were withdrawn.
