# Withdrawn cross-paper and project-built benchmark artifacts

## Scope Boundary Declaration

- **IN-SCOPE:** register datasets, models, metrics, and report artifacts under `workspaces/truongnv/` that fail the user's strict per-paper pairing rule.
- **OUT-OF-SCOPE:** alter canonical upstream repositories, certify literature claims, or infer paper fidelity from hashes alone.

A local metric is withdrawn when it evaluates a model/checkpoint from one paper on another paper's dataset without an exact matching protocol. This applies even when the source files are public and scores recompute. Project-created inputs/splits are also excluded unless their exact source derivation is established.

| Artifact family | Reason for withdrawal | Filesystem status |
|---|---|---|
| Review 1 public-vector suite | Multiple source-paper datasets evaluated with checkpoints from other releases. | Physically removed from `02_DeBERTa_v3_Semantic_Classifier`. |
| D1–D6 suite and six-checkpoint matrix | Six checkpoint origins paired with six dataset origins rather than each model's paper protocol. | Physically removed from `02_DeBERTa_v3_Semantic_Classifier`. |
| Meta Prompt Guard local candidate | The official checkpoint could not be loaded; a former TF-IDF proxy used project-authored rows and was not Meta Prompt Guard. | Physically removed (`Tier1_Candidate_Meta_PromptGuard2024`). |
| ProtectAI on PIGuard assets | ProtectAI checkpoint paired locally with PIGuard paper assets. | Mixed results and cross-paper artifacts removed; only PIGuard-on-PIGuard rows are retained. |
| ProtectAI on PIDS-Bench | ProtectAI checkpoint paired locally with PIDS-Bench data. | `protectai_reference` folder physically removed; runner disabled. |
| Review 2 and Tier 1 TF-IDF | Project-built fit, labels, and splits combine Deepset and TrustAIRLab data. | Fit, prediction, and mixed report folders physically removed from `01_TFIDF_Syntactic_Baseline`. |
| Meeting 4/5 generated indicators | Prior project probes or cross-paper outputs supplied chart values. | Withdrawn; ungrounded metrics and thresholds marked out of scope. |
| Meeting 6 benchmark/audit scripts | The benchmark paired models and data across papers; the old auditor checked withdrawn artifacts and printed unsupported completeness claims. | Both entry points are stop-only stubs; no benchmark or “100%” audit result is valid. |

The withdrawn artifacts listed above have been physically purged from the filesystem following the provenance cleanup audit (2026-10-01).

## Retained local evidence

Only the same-paper PIDS-Bench TF-IDF baseline and the PIGuard checkpoint on PIGuard-released assets remain eligible as local run results. See the [PIDS-Bench report](../../replications/PIDS_Bench_Shire_IEEEAccess2026/REPORT.md) and [PIGuard-only report](../../replications/02_DeBERTa_v3_Semantic_Classifier/reports/review1_paper_model_public_rerun_2026-09-30/REPORT.md). These use different tasks and protocols and are not a head-to-head comparison.
