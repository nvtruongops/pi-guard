# V10 bounded curator handoff

## Scope Boundary Declaration

English candidate review only. This packet is not a training corpus or evaluation set. The human curator supplies decisions under the existing single-curator protocol. Assistant/native labels are excluded.

Open only the [96-row blind pilot](../../../../workspaces/truongnv/pi_guard_pipeline/training_bases/datasets/project_training/versions/pi_guard_v10_english_readiness_20261013/annotation/source_blind_pilot.csv) for labeling. Save a reviewed copy outside the immutable V10 package. Do not inspect the provenance key, source-review template, native labels, assistant proposals or model outputs while labeling. Text and context must stay unchanged; the intake checker rejects altered bindings and missing/extra IDs.

Follow the [approved rubric](../../../../workspaces/truongnv/pi_guard_pipeline/training_bases/datasets/project_training/history/pi_guard_v8_source_gate_20261010/LABEL_ADJUDICATION_PROTOCOL.md). Fill curator/final label, the injection and safety-bypass flags, confidence, rationale code, context sufficiency, rubric version, timestamp and curator alias. Use `single_curator_reviewed` only for a clear canonical-class annotation. Keep hybrid, uncertain and missing-context cases quarantined. A direct harmful request alone does not establish jailbreak intent.

The pilot is selected for bounded review work, not representativeness. Its results will identify actual class-by-family support and guide the next acquisition round. A separate source reviewer saves a reviewed copy of the V10 source-review template outside the immutable package; this material unblinds source identities and must remain separate from labeling. Privacy and rights decisions are not supplied by the assistant. Accepted data changes require another dataset version.

Run the [intake checker](../../../../workspaces/truongnv/pi_guard_pipeline/training_bases/pi_guard_tfidf_tier1/check_curated_candidate.py) on the reviewed copy with `--annotations` and a new `--output` audit path. The optional human attestation file records the annotation-file SHA-256, `annotation_actor=human`, rubric version and curator alias; it is not inferred from CSV field values. This stage emits no canonical model rows and does not authorize training. Resolve all data gates before adapting the fixed baseline runner.

The [owner gate declaration](../l2_v9_health_check_20261013/OWNER_GATE_DECLARATION.json) remains a separate pending decision before validation cutoff selection. It must not be filled from favorable observed metrics.
