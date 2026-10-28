# Sealed Test Contract Implementation Plan

## Scope

Change only the new autonomous L2 adapter and its existing task-local verification script. Keep the frozen protocol, legacy helper, historical dataset versions, and all prompt payloads unchanged. Test data remains unopened; L3 is not executed.

## Approved contract

`split.partitions.test` is a closed metadata object with schema `pi_guard_sealed_test_families_v1` and a nonempty `families` array. Each family entry contains only `source_repository_id`, `source_revision`, `source_family_id`, `collection_lineage_id`, and `label_support` (exactly the benign/PI/JB nonnegative integer totals). No test row IDs, prompt text, per-row provenance, payload path, or test file hash may appear. The manifest's test partition is exactly `{"sealed_contract":"split.partitions.test"}`. Require test family and collection-lineage disjointness from train/validation and exact source-review evidence for every test family. Preserve current per-row train/validation checks.

## Steps and verification

1. Add a metadata-only assert check for valid sealed-family shape, invalid row-level test fields, and family/lineage overlap; run it before implementation and confirm the new contract case fails.
2. Implement the smallest validator/helper in `fit_l2_curated.py`; keep train/validation loading and fitting paths unchanged and reject test rows/provenance references in the manifest.
3. Re-run the assert check, existing V9-V12 negative-gate/config checks, Python syntax/import checks, and confirm no test payload, fitted vocabulary, fit path, or L3 path was opened.
4. Update the adapter brief and task progress with verified results; sync CodeGraph and write a short contract report.

No fit is claimed unless an eligible real, frozen package passes every data gate. No test selection or L3 readiness pass is claimed from metadata-only verification.
