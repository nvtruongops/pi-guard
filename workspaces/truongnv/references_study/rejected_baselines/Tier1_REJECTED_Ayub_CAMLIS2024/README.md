# Ayub paper and code reference — local pilot withdrawn

**Status (2026-09-30):** this folder is retained for the paper and author-code reference. Its project-local embedding benchmark is withdrawn and must not be cited as an Ayub reproduction or as current PI-Guard evidence.

The former local training file contained 344 rows; 200 rows had no `source` value, and row-level lineage/split equivalence could not be established. Its SHA-256 at audit time was `6b3078e69a15c60620a004fbfdd2ad81ac56676a6c247e8d51decd0fc865086e`. The training file, run results, cached embeddings, generated notebook/plots, and notebook builder were removed because the local scores depended on that unverified training set. No local Ayub score is reportable from this folder.

Five files that duplicated the PIGuard bundle (`valid.json`, three NotInject files, and `wildguard.json`) were removed on 2026-09-30. No dataset is retained for an Ayub experiment; the original files remain only in the PIGuard source package. The local asset verifier checks that these Ayub paths remain absent.

The paper and author repository snapshot remain available for literature review. The snapshot does not carry a pinned upstream commit; see [`UPSTREAM_POINTER.json`](upstream/UPSTREAM_POINTER.json). The former project runner now exits with an explanation. To resume a local study, first acquire the paper's public dataset at a pinned revision and create a row-level source manifest and split audit, then make a new experiment with raw predictions.

## Scope boundary

- **IN-SCOPE:** preserve paper/code references; retain no local Ayub experiment data.
- **OUT-OF-SCOPE:** claiming a local Ayub replication, reusing withdrawn metrics, or treating paper-referenced methods as PI-Guard results.
