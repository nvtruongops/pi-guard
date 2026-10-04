# PIGuard ACL 2025 reference and checkpoint evaluation

**Current claim boundary (2026-09-29):** the retained evidence supports inference with the released PIGuard checkpoint. It does not show retraining from scratch or a complete reproduction of every paper experiment. The local 2026-09-15 result package is historical; earlier manifests recorded conflicting upstream revisions, so use the current [reproduction audit](../../reports/experiment_reports/reproduction_audit_2026-09-29/EXPERIMENT_REPRODUCTION_AUDIT.md) for reportable results and do not rely on the old “100% reproduction” claims below it.

## Retained source and data

- Official source snapshot: `PIGuard_ACL2025/`, pinned to revision `1b5751e88bf7475acbedfc8eda795ce060307c84` in [the local provenance record](reports/PROVENANCE.json). The retained `train.py` and `datasets/train.json` match the recorded upstream Git blob/SHA-256 values.
- `datasets/train.json` contains 76,735 training records. The upstream README says the authors collected the training mixture from 20 open-source datasets and LLM-augmented data. It is training input, not a test set.
- Public evaluation assets retained: `valid.json` (144), NotInject one/two/three (113 each), `wildguard.json` (971), BIPIA text (75 payloads) and BIPIA code (50 payloads). PINT is not public.
- BIPIA files contain five payloads per task category (15 text categories; 10 code categories). Older local documentation incorrectly called these 120 records each.

## Evidence

The raw local result JSON and older comparison report are retained as historical run artifacts, but their old accuracy-match and full-reproduction claims are not current reportable conclusions. See the reproduction audit and [benchmark dashboard](../BENCHMARK_RESULTS_DASHBOARD.md) for claims supported by current checks.

The [dataset provenance card](datasets/DATASET_PROVENANCE.md) lists retained file counts and hashes. Run `python workspaces/truongnv/replications/verify_replication_assets.py` for a read-only local count/hash check. A hash check establishes byte identity against the recorded value; upstream origin is established separately by the pinned source audit.
