# PIGuard experiment evidence status

## Scope Boundary Declaration

- **IN-SCOPE:** the PIGuard package and evidence stored within `workspaces/truongnv/replications/Paper_ACL2025_PIGuard_HaoLi/`.
- **OUT-OF-SCOPE:** other folders, including the full project report tree.

## Current status

The retained model evidence is checkpoint inference with the publicly released PIGuard checkpoint. This is not retraining from scratch and does not reproduce the unavailable PINT experiment. The official source snapshot and public data assets are documented in `reports/PROVENANCE.json` and `datasets/DATASET_PROVENANCE.md`.

The local evaluation asset counts are 144 validation records, 339 NotInject benign records across three subsets, 971 WildGuard records, 75 BIPIA text payloads, and 50 BIPIA code payloads. Total: 1,579 evaluation records. `train.json` has 76,735 records but is the authors’ training mixture and is excluded from that total.

The result JSON dated 2026-09-15 and this folder’s previous comparison report are retained as historical run artifacts. Because earlier local manifests recorded inconsistent source revisions and old documentation overstated the fidelity, the historical metric comparisons and “100% reproduction” conclusion are not endorsed here. For reportable results, model revision, inputs, and protocol, use [the current reproduction audit](../../reports/experiment_reports/reproduction_audit_2026-09-29/EXPERIMENT_REPRODUCTION_AUDIT.md).

## Dataset-size interpretation

The smaller counts belong to particular task slices (e.g., 113 benign examples per NotInject trigger subset and five BIPIA payloads per task category in these packaged files). They are not the size of PIGuard’s training corpus. The upstream paper also evaluates PINT, which is not publicly available.
