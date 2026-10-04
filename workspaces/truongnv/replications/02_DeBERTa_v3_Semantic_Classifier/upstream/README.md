# Downloaded public checkpoint snapshots

`checkpoints/PIGuard/<revision>/` contains the public Hugging Face files for PIGuard, copied from the Hub cache and verified against original file byte counts and SHA-256 values. PIGuard is the sole retained checkpoint snapshot under the paper+repo criterion (audit date: 2026-10-02). Five other snapshots (ProtectAI, FMOPSDistilBERT, DeepSetDeBERTa, InjectionSentry, WolfDefenderSmall) were withdrawn and physically removed.

| Key | Public checkpoint | Revision | Status |
|---|---|---|---|
| PIGuard | [leolee99/PIGuard](https://huggingface.co/leolee99/PIGuard/tree/dd78b24e330193a22d2293ac66922dd4f982f563) | `dd78b24e330193a22d2293ac66922dd4f982f563` | Retained (paper ACL 2025 + official repo) |
| ProtectAI | [protectai/deberta-v3-base-prompt-injection-v2](https://huggingface.co/protectai/deberta-v3-base-prompt-injection-v2) | `90c9989b1a342275dd0d1a95aad283c04e075671` | Withdrawn & removed (lacks original paper) |
| FMOPSDistilBERT | [fmops/distilbert-prompt-injection](https://huggingface.co/fmops/distilbert-prompt-injection) | `c5da1fefd33c98c447b50dd806fe86aeb9e8c26c` | Withdrawn & removed (lacks paper/training repo) |
| DeepSetDeBERTa | [deepset/deberta-v3-base-injection](https://huggingface.co/deepset/deberta-v3-base-injection) | `80dda00d0b0d9a03917a7685e2ddbcd28e04dbb1` | Withdrawn & removed (lacks paper/training repo) |
| InjectionSentry | [Verm1ion/injection-sentry-deberta-v2](https://huggingface.co/Verm1ion/injection-sentry-deberta-v2) | `956b7e581e08615c824abbc877cb6461fcd8fa28` | Withdrawn & removed (cites GitHub PR, not paper) |
| WolfDefenderSmall | [patronus-studio/wolf-defender-prompt-injection-small](https://huggingface.co/patronus-studio/wolf-defender-prompt-injection-small) | `bcab2eff97bcabd7227849639e2d0d7a61b46c92` | Withdrawn & removed (ModernBERT, lacks paper) |

See [`model_sources.lock.json`](model_sources.lock.json), [`model_download_manifest.original.json`](model_download_manifest.original.json), and [`bundled_checkpoint_manifest.json`](bundled_checkpoint_manifest.json) for historical repository IDs, pinned revisions, cache origin, and verified file hashes.

The public PIGuard GitHub source root is checked out locally at [`public_repositories/PIGuard/`](public_repositories/PIGuard/) at revision `1b5751e88bf7475acbedfc8eda795ce060307c84`. The PIGuard checkpoint remains under `checkpoints/PIGuard/<revision>/`; it is a reference baseline, not the PI-Guard project's own trained model.
