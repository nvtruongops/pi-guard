# Model study 02 — DeBERTa-v3 and public checkpoint evaluations

## Scope boundary declaration

- **IN-SCOPE:** the public-checkpoint inference runs and the D1–D6 six-checkpoint matrix moved here with their public inputs, checkpoint revisions, raw predictions, and result files.
- **OUT-OF-SCOPE:** calling any public checkpoint a PI-Guard-trained Tier 2 model, treating the D1–D6 matrix as a paper reproduction, or claiming that a two-tier cascade was tested.

## Contents

- [`datasets/`](datasets/) — public evaluation inputs and raw D1–D6 source snapshots.
- [`upstream/`](upstream/) — six downloaded Hugging Face checkpoint snapshots, source locks, and the public PIGuard code/data repository checkout at the revision used by the paper-asset rerun.
- [`papers/`](papers/) — the DeBERTa-v3 architecture paper and the PIGuard paper. Checkpoint model cards remain with their upstream snapshots.
- [`results/`](results/) — SHA-256-verified copies of the saved result tables, manifests, and prediction files, indexed by run.
- [`reports/`](reports/) — historical bundles, several of which are withdrawn under the same-paper model/data rule. Do not treat their old scores as current evidence.

The DeBERTa-v3 paper supports the architecture background; it is not a paper for every fine-tuned checkpoint in the matrix. The checkpoint IDs, revisions, model cards, and hashes are recorded in `upstream/` and in each run manifest.

The 606-row public-vector suite and D1–D6 matrix pair checkpoints with other papers' datasets and are withdrawn. The PIGuard/ProtectAI report bundle is mixed; only the PIGuard checkpoint on assets distributed with the PIGuard release is retained in the [PIGuard-only report](reports/review1_paper_model_public_rerun_2026-09-30/REPORT.md). The PIDS-Bench result is tracked separately in [its report](../PIDS_Bench_Shire_IEEEAccess2026/REPORT.md). These reports use different protocols and are not a comparison. No checkpoint was fine-tuned here, and no PI-Guard three-class model or cascade result is established.
