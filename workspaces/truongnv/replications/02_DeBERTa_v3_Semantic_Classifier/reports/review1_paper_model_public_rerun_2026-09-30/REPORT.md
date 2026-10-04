# PIGuard checkpoint on PIGuard-released evaluation assets

**Status:** eligible as an individual same-paper run on pinned PIGuard release assets. The former ProtectAI comparison and joint report are withdrawn.

## Scope Boundary Declaration

- **IN-SCOPE:** PIGuard model revision `dd78b24e330193a22d2293ac66922dd4f982f563` on public evaluation assets distributed with PIGuard source revision `1b5751e88bf7475acbedfc8eda795ce060307c84`.
- **OUT-OF-SCOPE:** ProtectAI checkpoint results, other-paper datasets, a full reproduction of all PIGuard experiments, three-class PI-Guard results, or a cascade.

## Verification

The local verifier checked six source-file hashes, 1,435 input rows, prediction identity, labels, and recomputed model metrics. The PIGuard checkpoint prediction file has SHA-256 `ac4c3fe98b61a1f3102bedf0f403bd30e7831fcd70dfcdd746dd00bc0fff9689`. The paper and source repository are cited at [[18]](../../../../References/REFERENCES_LOG.md#ref18).

## Retained PIGuard-only measurements

| Source slice | Result | Meaning |
|---|---:|---|
| NotInject overall | 300/339 = 88.50% | Correct benign classifications |
| NotInject subset one | 107/113 = 94.69% | Correct benign classifications |
| NotInject subset two | 101/113 = 89.38% | Correct benign classifications |
| NotInject subset three | 92/113 = 81.42% | Correct benign classifications |
| BIPIA text payload | 29/75 = 38.67% | Attack payloads flagged |
| BIPIA code payload | 49/50 = 98.00% | Attack payloads flagged |
| BIPIA equal-subset macro | 68.33% | Mean of text and code payload attack recall |
| BIPIA pooled payload recall | 62.40% | Combined flagged payloads over 125 rows |
| WildGuard benign | 739/971 = 76.11% | Correct benign classifications |

These are local results on the listed release slices. BIPIA rows are payload strings, not full task-plus-context inputs, so they are not interchangeable with full BIPIA benchmark results. The exact predictions and verifier remain in this folder.

## Withdrawn cross-paper artifacts

This run folder also contains ProtectAI predictions on PIGuard assets and a two-checkpoint offline replay. Those pair a ProtectAI model with another paper's data and are withdrawn under the user's rule. Do not cite ProtectAI metrics, the joint comparison, or the replay. The old generator/verifier files remain because deletion was blocked; do not rerun the mixed path.

## Project limits

This is not a locally trained PI-Guard model, a three-class result, a full reproduction, or an end-to-end cascade measurement. P95/FPR values remain project targets.
