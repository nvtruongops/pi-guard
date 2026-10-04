# Ayub reference package — provenance status

**Status: local benchmark withdrawn on 2026-09-30.** The paper and a local author-code snapshot remain for literature review. The project-local score files, notebook, plots and cached embeddings have been removed.

## Public references

- Paper: Md. Ahsan Ayub and Subhabrata Majumdar, *Embedding-based classifiers can detect prompt injection attacks*, [arXiv:2410.22284](https://arxiv.org/abs/2410.22284).
- Author repository: [AhsanAyub/malicious-prompt-detection](https://github.com/AhsanAyub/malicious-prompt-detection). The local snapshot is not pinned to a repository commit; see [`UPSTREAM_POINTER.json`](../upstream/UPSTREAM_POINTER.json).
- The paper-referenced dataset: [ahsanayub/malicious-prompts](https://huggingface.co/datasets/ahsanayub/malicious-prompts). A complete, revision-pinned copy of this dataset was not verified here.

## Data and result disposition

- The former local `train.json` had 344 rows, of which 200 had no `source` value. Exact paper-split equivalence was not established. It was removed; its pre-removal hash and observed counts are recorded in [`DATASET_PROVENANCE.md`](../datasets/DATASET_PROVENANCE.md).
- Five files that duplicated the PIGuard bundle were removed on 2026-09-30. No dataset is retained in this Ayub reference package; the original data remain only in the PIGuard source package.
- The two copies of the local run JSON, generated notebook/plots and three cached feature arrays were removed because the reported fit depended on the unverified train split. No local Ayub metrics are reportable from this package.
- The runner now fails closed. It does not train a model or regenerate withdrawn output.

The file hashes are integrity checks, not proof of paper fidelity. For the active dataset evidence, see [PIGuard's data provenance](../../../../replications/Paper_ACL2025_PIGuard_HaoLi/PIGuard_ACL2025/datasets/).
