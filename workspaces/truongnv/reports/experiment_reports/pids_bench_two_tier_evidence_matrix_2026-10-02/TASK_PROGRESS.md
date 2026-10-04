# Work log — PIDS-Bench evidence matrix

## Scope Boundary Declaration

- **IN-SCOPE:** Reproduce the pinned same-release TF-IDF+LR baseline on PIDS-Bench v3; distinguish local measurements from the paper's published transformer baselines; audit the withdrawn Meeting 6 figures.
- **OUT-OF-SCOPE:** Local transformer training/evaluation, a PI-Guard cascade, restoring D1–D6, three-class claims, cross-paper model/dataset pairings, and achieved P95/FPR system targets.

## Checklist

- [x] Confirm PIDS-Bench task boundary, pinned source commit, and frozen-data checksums.
- [x] Audit the suggested arXiv paper as related literature only; archive its open-access PDF and record that arXiv v1 promises code but links no official experiment repository. No paper scores were imported into the local matrix.
- [x] Re-run pristine original TF-IDF+LR source blob from the pinned commit on the same staged frozen data (seed 42, no grid search; Git blob hash verified).
- [x] Generate a CSV and PNG visualization of the pinned authors' published same-release baseline table, explicitly labeled as literature results.
- [x] Write the provenance-labeled report separating the published three-model table from the one completed local TF-IDF run.
- [x] Resolve public DeBERTa-v3-base and DistilBERT base checkpoints at pinned Hub revisions, record file SHA-256 values, and verify DistilBERT resolves from the offline cache.
- [x] Stop DeBERTa at the user's instruction to run only TF-IDF because of device performance. The resumed process reached an observed step 3,697/5,082 before stopping; checkpoint 3,388 is the latest durable checkpoint. No final DeBERTa test result exists.
- [x] Do not start DistilBERT under the user's TF-IDF-only instruction. Its data and public checkpoint remain staged/pinned, but there are no local DistilBERT results.
- [ ] Full local three-model matrix and cascade inference not performed; superseded by the user's updated TF-IDF-only scope. Do not claim local two-tier validation.
- [x] Verify unsupported Meeting 6 images are absent and no Markdown image embeds remain.

## Run note

The official DeBERTa training script was retained unchanged. A wrapper runs it from the pinned checkout; dynamic padding is an explicit local efficiency adaptation that preserves text, truncation at 512 tokens, FP32, seed, 3 epochs, and effective batch 16. The first fixed-padding run stopped before a checkpoint because measured speed implied over 15 hours. The initial dynamic-padding run stopped at 532/5,082 without a checkpoint. Its fresh seed-42 restart reached 4,281/5,082, but battery operation activated NVIDIA software power capping; the job was interrupted to preserve remaining battery. Durable checkpoints at steps 1,694 and 3,388 remain; the latest checkpoint's validation F1 is 0.9889135. No final DeBERTa test result is available. The wrapper now supports resuming from a saved checkpoint; the exact command is in that run directory's `COMMANDS.md`. The first TF-IDF trial used a pre-existing modified checkout file; it is superseded by the successful isolated run from the pristine pinned blob `776cd95b5be0bff687e13a537794b590b131f6d9`.

On 2026-10-03, resume startup exposed missing Python source files in the temporary training environment and stopped before model training. Recorded package versions were restored into that environment, including Python 3.12-compatible wheels; pandas, PyTorch CUDA, Transformers, Trainer, tokenizer, requests, and dateutil imports then passed. The failed startup attempts did not alter the frozen data or checkpoint; after repair, the resume ran and was stopped at the user's later instruction, as recorded below.

After AC power became available, the user directed that no DeBERTa be run and only TF-IDF be used because of device performance. The resumed DeBERTa process was stopped at observed step 3,697/5,082; the run config is marked `stopped_by_user`, and the durable checkpoint remains step 3,388. The attempted unsaved steps after that checkpoint are not reported as a completed model result. DistilBERT was not started. This update supersedes earlier notes saying to resume after AC power becomes available.

The requested `tasks_for_meeting_6/figures/` directory was already absent at inspection time. Fresh filesystem verification found 0 remaining image files and 0 Markdown image embeds; Git shows 26 tracked image deletions already present in the working tree. No files were deleted by this run.

The generated `pids_bench_author_published_matrix.csv` and `.png` in the experiment report directory are transcribed from the pinned authors' README table. They provide published standalone-model context only; they do not complete a local three-model comparison or validate a cascade.

The transformer starting points are public base checkpoints pinned to fixed Hub revisions. Their model/config/tokenizer SHA-256 values and the upstream training-source blob IDs are recorded in `replications/PIDS_Bench_Shire_IEEEAccess2026/run_artifacts/PIDS_Bench_model_input_manifest_2026-10-03.json`. The stopped DeBERTa attempt used microbatch 2 × accumulation 8 with the same effective batch 16 and dynamic padding; it produced no final test metrics. Transformer literature values remain separate from local TF-IDF results.

## Verification note

- Re-ran `build_published_matrix.py`; it read commit `87dc835566b930ee921240874a4939b2c266c2fe` and emitted 24 model-metric rows covering the three author-published baselines.
- `audit_claim_evidence.py --file REPORT.md` reports phantom `ref44`–`ref57` IDs because that repository-wide auditor hardcodes `Final-Report/References/REFERENCES_LOG.md`, while this member report follows the task's member-local `References/REFERENCES_LOG.md`. The source file confirms that fixed path; a local-catalog citation check is recorded separately. No root-owned catalog or auditor was edited.
