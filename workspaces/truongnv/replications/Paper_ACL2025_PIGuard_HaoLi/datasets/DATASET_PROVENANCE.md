# PIGuard dataset provenance

Upstream repository: https://github.com/leolee99/PIGuard

The package data snapshot is recorded at revision `1b5751e88bf7475acbedfc8eda795ce060307c84` in `../reports/PROVENANCE.json`. The official repository README describes a training mixture from 20 open-source datasets plus LLM-augmented data, evaluation assets from NotInject/BIPIA/WildGuard, and a non-public PINT benchmark.

| File | Records | SHA-256 | Role |
|---|---:|---|---|
| `PIGuard_ACL2025/datasets/train.json` | 76,735 | `806ded8bd85782a53d34faffe4fd92b3f2e0b3b431c43578ce77faea6b9ed911` | Author-provided training mixture; includes LLM-augmented examples per upstream description. |
| `valid.json` | 144 | `e273fd455baac8785aa15bdc058adfd609f62ed0a3022963a5395ba95efe110e` | Validation. |
| `NotInject_one.json` | 113 | `c77abbf3de71f99f0e12809a29d8468401285ef5353b53daa6d65131c866586c` | Public NotInject subset. |
| `NotInject_two.json` | 113 | `325559cd1204fd3bdf0be82599fbf8ebbacdcd4949ae8b5bf67b399193d57c03` | Public NotInject subset. |
| `NotInject_three.json` | 113 | `bc18f3ad38ad2380e57ae96d102b884af477989e2f3ff85fbc2271ed16b8db55` | Public NotInject subset. |
| `wildguard.json` | 971 | `62a0f7331af19abdb43b027b815272777aac4c311b7fad25e4150618c5289f9b` | WildGuard source records. |
| `BIPIA_text.json` | 75 | `e828d3e9e273ddf43c4b0c91e5803998f4314555d865e32bd4e0903ab746a3b9` | Five payloads in each of 15 task categories. |
| `BIPIA_code.json` | 50 | `ab9f0563c7674074fb1cf82cb624196e9b5e3d62ac57b324b0745d23b7e55f87` | Five payloads in each of 10 task categories. |

A local hash confirms the recorded file bytes. Upstream origin is supported by the pinned repository snapshot audit; the training mixture’s source field does not provide full row-by-row lineage. Training data is not an evaluation set, and the missing PINT set cannot be inferred from these local files.
