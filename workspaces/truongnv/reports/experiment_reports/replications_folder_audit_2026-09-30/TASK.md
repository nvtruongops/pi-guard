# Task — replication-folder public dataset audit (2026-09-30)

Source: current user request. No separate task file was supplied. Prior replications_validation_2026-09-29 reports are context, not authority to retain folders.

## Scope Boundary Declaration

**IN-SCOPE:** inspect every top-level model/support folder in workspaces/truongnv/replications; verify public data/code provenance from official sources; move useful SOTA/reference-only folders without a public prompt-injection dataset or incompatible with the external text-level guardrail to references_study; move the Ayub embedding cache beside its consuming reference runner; update current indexes, affected code paths, and the dashboard so it cannot present withdrawn/proxy numbers as paper results; record blocked cleanup accurately.

**OUT-OF-SCOPE:** retrain or benchmark models; reconstruct project-authored probes; change Meeting 6 empirical claims; modify shared/root/FPT-controlled files.

**Follow-up disposition (2026-09-30):** a later workspace provenance audit supersedes the cache-retention item below. The Ayub training file had incomplete row lineage, so it and dependent local results/caches were removed; the local runner is now fail-closed. See [`WORKSPACE_PROVENANCE_AUDIT_2026-09-30.md`](../WORKSPACE_PROVENANCE_AUDIT_2026-09-30.md).

## Checklist

- [x] Inventory all model and support folders, local dataset files, and path consumers.
- [x] Verify official paper/repository/dataset sources; distinguish released rows from official loaders and project-generated probes.
- [x] Move only folders that lack a suitable public detector dataset or are architecturally outside the external guardrail; preserve all moved files.
- [x] Update workspace indexes, affected adapter paths, dashboard labels, and legacy audit entry points.
- [x] Verify source/destination state, hashes for retained/moved assets, and report limitations including the prior Meta deletion block.
