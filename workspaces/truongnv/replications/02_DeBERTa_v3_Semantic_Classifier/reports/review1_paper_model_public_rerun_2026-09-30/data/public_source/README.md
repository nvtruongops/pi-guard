# Public evaluation inputs — byte-for-byte source snapshot

These six files were copied without modification from the local checkout of the public PIGuard paper repository:

- Upstream repository: <https://github.com/leolee99/PIGuard>
- Pinned upstream revision: `1b5751e88bf7475acbedfc8eda795ce060307c84`
- Canonical local source folder: `workspaces/truongnv/replications/Paper_ACL2025_PIGuard_HaoLi/PIGuard_ACL2025/datasets/`
- Copied inputs: `NotInject_one.json`, `NotInject_two.json`, `NotInject_three.json`, `BIPIA_text.json`, `BIPIA_code.json`, and `wildguard.json`
- `LICENSE` is copied from the same upstream checkout.

The parent [`run_manifest.json`](../../run_manifest.json) records the SHA-256 for every evaluated input and the exact Hugging Face model IDs/revisions. The parent [`verification_results.json`](../../verification_results.json) contains recomputed per-checkpoint metrics; the `predictions_*.jsonl.gz` files contain row-level outputs.

These are public external checkpoints run separately. They are not a PI-Guard-fine-tuned DeBERTa model or a conditional two-stage cascade.
