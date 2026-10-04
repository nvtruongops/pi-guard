# PIGuard source and data status

The code snapshot is recorded at revision `1b5751e88bf7475acbedfc8eda795ce060307c84`; the local source/data byte hashes are recorded in `reports/PROVENANCE.json`. The author repository says `train.json` is a training mixture drawn from 20 open-source datasets and LLM-augmented data. It must not be counted as evaluation data.

Retained evaluation sizes are valid 144, NotInject 113 each for three subsets, WildGuard 971, BIPIA text 75, and BIPIA code 50. Older local README claims of 120 per BIPIA file and 1,000 WildGuard records were incorrect for the files retained here. PINT is not public.

The 2026-09-15 result JSON is a historical checkpoint-inference artifact. Its former full-reproduction/exact-match claims are superseded by the current [reproduction audit](../../../reports/experiment_reports/reproduction_audit_2026-09-29/EXPERIMENT_REPRODUCTION_AUDIT.md).
