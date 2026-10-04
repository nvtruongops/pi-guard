# Council defense rationale and gap audit

## Scope Boundary Declaration

- **IN-SCOPE:** current project rationale, paper-matched local evidence, and open measurement gaps.
- **OUT-OF-SCOPE:** use cross-paper results or claim the proposed cascade has been validated.

PI-Guard proposes an external guardrail for prompt injection and jailbreak inputs. The eligible local results are the PIDS-Bench same-paper TF-IDF baseline and PIGuard-only inference on PIGuard-released assets. They are separate binary/slice-specific experiments, not a combined model comparison. See the [PIDS-Bench report](../../../replications/PIDS_Bench_Shire_IEEEAccess2026/REPORT.md), [PIGuard-only report](../../../replications/02_DeBERTa_v3_Semantic_Classifier/reports/review1_paper_model_public_rerun_2026-09-30/REPORT.md), and [workspace audit](../../experiment_reports/WORKSPACE_PROVENANCE_AUDIT_2026-09-30.md).

The former Review 1 vector, mixed TF-IDF, D1–D6, and ProtectAI cross-paper outputs are withdrawn. Their folders remain because deletion was blocked. Do not cite them. The project still needs a source-matched three-class dataset, project-model training, group-aware held-out evaluation, and a separate end-to-end cascade measurement. P95 < 30 ms and FPR < 1.5% are targets only.
