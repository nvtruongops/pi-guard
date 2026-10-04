# Task — paper-backed TF-IDF and DeBERTa reference runs

**Source:** user follow-up on 2026-09-30. This request supersedes the earlier audit task's `OUT-OF-SCOPE` restriction on model runs.

## Scope Boundary Declaration

- **IN-SCOPE:** retain the paper and pinned author code; verify frozen data provenance; run TF-IDF and DeBERTa-v3 as independent models; record model files, per-model results, confusion matrices, and attack-subtype diagnostics where supported; identify whether the earlier word/character n-gram choice came from a paper; remove withdrawn project-fitted TF-IDF artifacts and correct current Review 1 references.
- **OUT-OF-SCOPE:** training or reporting a PI-Guard cascade; claiming three-way Benign/Prompt Injection/Jailbreak classification from this binary paper; editing shared/root files, `Final-Report/`, FPT-controlled materials, or another member's workspace.

## Checklist

- [x] Verify the IEEE Access paper, author repository tag, and dataset manifest.
- [x] Save the paper PDF and pinned upstream repository under this model-study folder.
- [x] Verify the frozen CSV hashes and identify the 664 license-redacted hard-benign rows.
- [x] Fit and evaluate TF-IDF + Logistic Regression on the paper's binary train/validation/test splits.
- [x] Run the paper's external ProtectAI DeBERTa-v3 comparator on the same frozen evaluation splits; record that the paper's internal DeBERTa-v3-FT model was not locally reproduced.
- [x] Finish the comparison report and record implementation deviations.
- [x] Mark old locally fitted TF-IDF artifacts withdrawn and repair current Review 1 report links/claims. Recursive deletion was blocked by automatic approval review; the files remain on disk.
- [x] Synchronize CodeGraph and verify frozen-data hashes, model/checkpoint hashes, confusion counts, prediction files, and touched Markdown links.
