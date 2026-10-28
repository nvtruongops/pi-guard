---
ArtifactMetadata:
  ArtifactType: task
  UserFacing: true
---
# V9 English L2 evidence and handoff task

## Scope Boundary Declaration

Source: the user's 2026-10-13 goal in attachment `f1e02700-0258-4879-af69-66f65bf10407/pasted-text-1.txt`, and the existing V9 initialization task. The user authorizes automatic work up to human evidence gates, with no commit, publication, or L3 execution.

Use `l2-health-check` for the readiness decision. Run the audit in this session. Preserve all existing dataset versions, source snapshots, and L2 runs. Write new evidence only in this report directory. No new dataset version is necessary for an audit that does not change data.

- [x] Read the attachment, AGENTS.md, governance, requested skill, and current V9 task/manifest/status.
- [x] Inspect existing L2 baseline code and curator protocol without opening locked evaluation data.
- [x] Verify V9 hashes, candidate queue/provenance alignment, blank curator decisions, language metadata, privacy screening, and duplicate-group metadata.
- [x] Verify the existing English V8 diagnostic metrics and configuration as immutable reference evidence; do not refit.
- [x] Record new public-source metadata prospects without downloading gated/evaluation payloads or repeating existing source reviews.
- [x] Prepare exact human review templates and a complete data/L2 gate table with no invented limits.
- [x] Write an English readiness report, chronological run table, limitations, and L3 handoff checklist.
- [x] Run the audit self-check, local report validators, link checks, and fresh immutability verification.

## Execution and decision rules

Reuse the V9 ingestion module's hash/path/normalization helpers and `load_pool` for source integrity. Recompute candidate-family duplicate statistics from the existing provenance index, without relabeling or regenerating datasets. Verify the English V8 `metrics.json` and saved predictions; never use V8 rows in V9.

Model fitting is dependent on canonical curator decisions, recorded rights/lineage and privacy review, verified independent family coverage (train/validation/test minimum 2/1/1 per class), duplicate handling, and frozen splits. Route acceptance additionally needs predeclared numeric risk, workload and support limits. Missing human decisions mean `BLOCKED` / health-check `NOT_READY`; missing acceptance values mean `GATE_UNSPECIFIED`. Report missing performance as `NOT AVAILABLE`.

Do not create a speculative V9 trainer while its canonical schema and gates are absent. Record the reusable baseline functions and required safeguards for a future V9 adapter. No L3 is authorized by this task.

## Final task outcome

Audit/report deliverables are complete. L2 qualification remains BLOCKED / NOT_READY at the human-label, source-review, frozen-split and acceptance-declaration gates. No model fit, test evaluation, L3 run, commit or publication was performed. See REPORT.md and VERIFICATION.json.
