# Retained dataset provenance inventory

**Scope Boundary Declaration**

- **IN-SCOPE:** source-backed data assets retained in `replications/` and moved to `references_study/` by the 2026-09-30 folder audit.
- **OUT-OF-SCOPE:** withdrawn project probes, non-dataset files embedded in upstream source trees, and unrelated workspace folders.

**Audit date:** 2026-09-30. This table lists the retained source-backed training/evaluation assets referenced by the model and reference inventory. It is not a recursive inventory of every data file inside upstream code copies. Record counts and SHA-256 values were read from the current local files. A hash identifies local bytes; provenance statements rely on the cited upstream source or exact-copy comparison, not on the hash alone.

| # | Retained file | Records | Bytes | SHA-256 | Provenance/use |
|---:|---|---:|---:|---|---|
| 1 | `Paper_ACL2025_PIGuard_HaoLi/PIGuard_ACL2025/datasets/train.json` | 76,735 | 43,398,735 | `806ded8bd85782a53d34faffe4fd92b3f2e0b3b431c43578ce77faea6b9ed911` | Official PIGuard training mixture; includes open-source and LLM-augmented data per upstream README; training only |
| 2 | `Paper_ACL2025_PIGuard_HaoLi/PIGuard_ACL2025/datasets/valid.json` | 144 | 91,222 | `e273fd455baac8785aa15bdc058adfd609f62ed0a3022963a5395ba95efe110e` | PIGuard public validation set |
| 3 | `Paper_ACL2025_PIGuard_HaoLi/PIGuard_ACL2025/datasets/NotInject_one.json` | 113 | 26,909 | `c77abbf3de71f99f0e12809a29d8468401285ef5353b53daa6d65131c866586c` | NotInject public-source subset |
| 4 | `Paper_ACL2025_PIGuard_HaoLi/PIGuard_ACL2025/datasets/NotInject_two.json` | 113 | 30,807 | `325559cd1204fd3bdf0be82599fbf8ebbacdcd4949ae8b5bf67b399193d57c03` | NotInject public-source subset |
| 5 | `Paper_ACL2025_PIGuard_HaoLi/PIGuard_ACL2025/datasets/NotInject_three.json` | 113 | 36,783 | `bc18f3ad38ad2380e57ae96d102b884af477989e2f3ff85fbc2271ed16b8db55` | NotInject public-source subset |
| 6 | `Paper_ACL2025_PIGuard_HaoLi/PIGuard_ACL2025/datasets/wildguard.json` | 971 | 472,515 | `62a0f7331af19abdb43b027b815272777aac4c311b7fad25e4150618c5289f9b` | WildGuard public-source file |
| 7 | `Paper_ACL2025_PIGuard_HaoLi/PIGuard_ACL2025/datasets/BIPIA_text.json` | 75 | 6,428 | `e828d3e9e273ddf43c4b0c91e5803998f4314555d865e32bd4e0903ab746a3b9` | BIPIA text payload records across 15 categories (5 each) |
| 8 | `Paper_ACL2025_PIGuard_HaoLi/PIGuard_ACL2025/datasets/BIPIA_code.json` | 50 | 16,427 | `ab9f0563c7674074fb1cf82cb624196e9b5e3d62ac57b324b0745d23b7e55f87` | BIPIA code payload records across 10 categories (5 each) |
| 9 | `references_study/jailbreak_defenses/SmoothLLM_Robey_NeurIPS2023/datasets/llama2_behaviors.json` | 10 | 2,721 | `f96d53e113bb3b839c6d0c9d4b2f3ab611e5b8fb4fd4a1cc68fb852f271cf286` | Official SmoothLLM LLaMA-2 behavior inputs; not detector evaluation labels |
| 10 | `references_study/jailbreak_defenses/SmoothLLM_Robey_NeurIPS2023/datasets/vicuna_behaviors.json` | 10 | 2,659 | `7396b50e123775b7d7080b2c475240401fb8e41ff1f91f9d0491663a01cb4ead` | Official SmoothLLM Vicuna behavior inputs; not detector evaluation labels |
| 11 | `PromptShield_Jacob_CCS2024/PromptShield/camera_ready_datasets/en_dataset_no_dups/2024-11-28_evaluation_benchmark_en.json` | 23,369 | 23,394,814 | `8b7e18426afdb4c7219d8f1a39ccfde347bc5125efb31ce4b2fb4acb2851cc16` | Author-released PromptShield camera-ready English evaluation benchmark |

## Interpreting the counts

- `train.json` is a 76,735-record PIGuard training mixture from the pinned official source snapshot. The upstream repository says it combines 20 open-source datasets with LLM-augmented data. It is training data, not a held-out evaluation set.
- The PIGuard evaluation assets include 144 validation rows, three NotInject subsets of 113 rows each, 971 WildGuard records, 75 BIPIA text payloads across 15 task categories, and 50 BIPIA code payloads across 10 categories. BIPIA category counts are not payload-record counts. PINT is not publicly available.
- A former copy of PIGuard `NotInject_one.json` was removed from the ProtectAI package because it was not part of the ProtectAI source repository.
- SmoothLLM’s two files contain 10 upstream behavior records each. They are attack/behavior inputs, not a standalone classifier benchmark; defense effectiveness requires victim-model evaluation.
- PromptShield’s 23,369-record author benchmark is retained in its upstream package. The former local 20-row subset was not that benchmark.

## Withdrawn local probes

Project-authored or unverified local datasets and dependent outputs were withdrawn from DataSentinel, ModernBERT, PromptShield, ProtectAI, the Jain-related baseline, InstructDetector, SmoothLLM, and the Meta Prompt Guard candidate. Their former counts (10, 20, 22, 700, or other project-selected subsets) must not be cited as paper dataset sizes. The Meta candidate is excluded from the active model registry; its unverified probe data and dependent outputs are absent. The current audit report distinguishes fixed public data releases from upstream loaders and behavior-only inputs.
