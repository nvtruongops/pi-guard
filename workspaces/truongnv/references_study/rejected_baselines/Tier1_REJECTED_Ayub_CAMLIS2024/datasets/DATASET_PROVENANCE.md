# Dataset provenance disposition — Ayub local pilot

**Current status: no dataset files are retained in this package.** The 344-row project training file could not be traced row by row; its results, feature caches, and dependent artifacts were removed. Five additional files were exact copies of PIGuard data rather than Ayub repository data and were removed on 2026-09-30. The original PIGuard files remain in the PIGuard source package.

## Withdrawn file

| File | Observed state before removal | Disposition |
|---|---|---|
| `train.json` | 344 rows; 200 rows had no `source` value; 116,149 bytes; SHA-256 `6b3078e69a15c60620a004fbfdd2ad81ac56676a6c247e8d51decd0fc865086e` | Removed because row-level provenance and split equivalence could not be established |

The run JSONs, generated notebook/plots, and cached embeddings that depended on the untraceable training file were removed. They are not current experimental evidence. The author paper and source repository remain linked in the parent [README](../README.md); the paper's complete public dataset was not verified in this folder.
