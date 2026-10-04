# PIGuard dataset card

## Retained assets

| File | Records | Role |
|---|---:|---|
| `PIGuard_ACL2025/datasets/train.json` | 76,735 | Official training mixture; not used as held-out evaluation. |
| `valid.json` | 144 | Validation set. |
| `NotInject_one.json` | 113 | Benign over-defense slice, one trigger word. |
| `NotInject_two.json` | 113 | Benign over-defense slice, two trigger words. |
| `NotInject_three.json` | 113 | Benign over-defense slice, three trigger words. |
| `wildguard.json` | 971 | WildGuard source records. |
| `BIPIA_text.json` | 75 | Indirect-injection payloads across 15 task categories (five each). |
| `BIPIA_code.json` | 50 | Code-injection payloads across 10 task categories (five each). |

The PIGuard evaluation assets total 1,579 records when the 144 validation records are included. This total excludes the 76,735-row training mixture. PINT is not publicly available. The authors’ upstream README describes the training mixture as collected from 20 open-source datasets plus LLM-augmented examples; individual training rows should not be assumed to have independent source annotations.

Local sizes and SHA-256 values are recorded in `METADATA.json`. The read-only verifier checks local byte identity and counts, not authorship on its own.
