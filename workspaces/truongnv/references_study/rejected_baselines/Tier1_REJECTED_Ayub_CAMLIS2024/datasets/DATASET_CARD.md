# Dataset status — Ayub local pilot

The former local Ayub training/evaluation bundle is not retained as an active experiment. The 344-row `train.json` had 200 records without a source field, so row-level lineage and split equivalence were not established. That file and all metrics derived from fitting it were withdrawn on 2026-09-30.

The duplicate JSON files that were previously copied from `replications/Paper_ACL2025_PIGuard_HaoLi/PIGuard_ACL2025/datasets/` were removed on 2026-09-30 (recorded in [`METADATA.json`](METADATA.json) and [`DATASET_PROVENANCE.md`](DATASET_PROVENANCE.md)). Currently, this folder retains only documentation cards, provenance, and metadata; no JSON dataset files are retained.

The author paper describes a separate public dataset. This folder does not contain a verified copy of that complete dataset. A future study must retrieve it from the cited public source at a pinned revision, preserve row identifiers/source fields and document the split before training.

See [`DATASET_PROVENANCE.md`](DATASET_PROVENANCE.md) and the [folder status](../README.md).
