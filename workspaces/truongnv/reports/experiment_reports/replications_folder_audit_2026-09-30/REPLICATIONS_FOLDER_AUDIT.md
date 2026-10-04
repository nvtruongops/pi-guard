# Replications folder audit — current provenance disposition

## Scope Boundary Declaration

- **IN-SCOPE:** model/dataset pairing eligibility and local result folders under `workspaces/truongnv/replications/`.
- **OUT-OF-SCOPE:** new evaluation, altering other workspaces, or interpreting exact source hashes as proof of a valid cross-paper experiment.

## Current decision

A local metric is retained only when the model/method and data follow the same paper's pinned release or exact protocol. This rule supersedes earlier folder-audit decisions that retained public cross-paper comparisons.

Retain two individual run records: PIDS-Bench TF-IDF + Logistic Regression on PIDS-Bench data, and the PIGuard checkpoint on PIGuard-released public evaluation assets. The first has 3,918 test prediction rows matched to the source split and metrics recomputed. The second passed six source hashes and 1,435 input-row checks. The protocols differ and the results are not a ranking. See the [workspace provenance audit](../WORKSPACE_PROVENANCE_AUDIT_2026-09-30.md).

Withdraw the Review 1 public-vector suite, D1–D6 checkpoint matrix, mixed Deepset/TrustAIRLab TF-IDF fits, and ProtectAI-on-PIDS/PIGuard outputs. The cross-paper rule applies even when all data files are public and old metric verifiers passed. The recursive deletion operation was blocked by automatic approval review; the affected folders remain on disk and must not be cited or rerun. Exact paths and sizes are in the workspace audit.

Original source packages and source-origin checkpoint files remain as provenance references. Their presence does not authorize reuse of a withdrawn model/data pairing.
