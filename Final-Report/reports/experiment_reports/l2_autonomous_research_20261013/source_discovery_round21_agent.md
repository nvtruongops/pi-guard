# L2 source discovery — Round 21

## Scope

This is a metadata-only screen for a non-TrustAIR, non-synthetic, human-authored, single-turn English jailbreak-attempt source that might serve as an L2 training family. It assesses publisher papers, repository cards, release metadata, license declarations, and documented privacy controls. No dataset row files were downloaded or opened, and no prompt text or IDs were used for selection, deduplication, or labeling. This is a source qualification note, not a canonical-label decision or an L2 PASS declaration.

## Closest candidate: Anthropic HH-RLHF red-team attempts

Anthropic’s 2022 red-team collection is a substantial independent lead: the paper reports 38,961 red-team transcripts, and the release card describes human-generated and annotated adversarial dialogues. The paper says participants were asked to try to elicit harmful or problematic model outputs. The dataset card lists transcript-level metadata including a human success rating, a task description, and a red-team-member identifier. The repository declares MIT licensing. ([Anthropic paper](https://arxiv.org/abs/2209.07858), [publisher dataset card](https://huggingface.co/datasets/Anthropic/hh-rlhf/blob/main/README.md), [release license](https://github.com/anthropics/hh-rlhf/blob/master/LICENSE))

| Qualification dimension | Evidence and limitation |
| --- | --- |
| Human authorship / language | The publisher paper describes manual red-teaming with crowdworkers, and the SelfDefend paper characterizes the source as English. This supports human-origin prompts, but not that every first message is itself a jailbreak attempt. |
| Single-turn semantics | The original release consists of conversations. A later paper derives a single-turn set by retaining each transcript’s initial human prompt and dropping assistant and later turns. That is a documented transformation, not a native single-turn split. The source’s attempt-success rating applies to the red-team interaction; it does not establish that the first message alone expresses the attempt or succeeded. ([SelfDefend, §6.2](https://www.usenix.org/conference/usenixsecurity25/presentation/wang-xunguang)) |
| Row lineage | The release card documents transcript, task-description, rating, and participant-ID fields, which provide useful provenance. The card does not document a dedicated stable row ID or a row-level binary `jailbreak` label. A pinned file plus deterministic row mapping would still be needed for a reproducible derivative. |
| Rights | The first-party repository declares MIT. This is comparatively clear for research reuse, subject to retaining the notice and the project’s own privacy/rights review. |
| Privacy | The source paper documents notice and consent for public release of unattributed transcripts, warns participants against including their own PII, and describes regex filtering plus manual review. It also says sensitive/possible PII may remain unintentionally. Thus the upstream process is documented but does not replace a local privacy scan and quarantine. ([Anthropic paper, Datasheet and PII filtering](https://arxiv.org/abs/2209.07858)) |
| Split / family | The release card describes a red-team-attempts corpus, not a canonical train/validation/test partition. SelfDefend creates its own 80/20 split after its processing; that is not an upstream split contract for reuse. The participant identifier may help with grouping, but collection-level and participant-level family semantics need to be specified without exposing worker identities. |
| Overlap | SelfDefend states the 2022 corpus predates and does not overlap its named 2023–2024 JailbreakHub, JailbreakBench, and MultiJail sources. This is useful lineage evidence, not an exact or semantic overlap audit against PI-Guard’s current package. No row-level overlap check was performed here. |

**Disposition:** retain as a conditional source-review lead, not as an admitted L2 JB family yet. It has real human red-team provenance, an open license, and documented privacy measures. The unresolved gate is whether a traceable subset of initial turns has native enough attempt semantics for PI-Guard’s JB class. The source metadata supports “human red-team interaction” at the transcript level, but does not certify each extracted first turn as a standalone jailbreak. The source also has no native row-level split contract. Do not promote SelfDefend’s derived labels or its 80/20 partition into source-native annotations or a PI-Guard split.

## Screened alternatives

| Candidate | Why it does not qualify for this L2 family request |
| --- | --- |
| Multi-Turn Human Jailbreaks (MHJ) | Its publisher describes human jailbreaks as multi-turn conversations. Taking a first turn alone would discard the interactional evidence that defines the source; it is not an independently released single-turn human-attempt family. ([Scale Labs paper](https://arxiv.org/abs/2408.15221)) |
| Bot-Adversarial Dialogue (BAD) | The first-party paper defines it as conversations where humans adversarially talk to bots to elicit unsafe behavior. It is a multi-turn dialogue source, so it does not establish a standalone single-turn attack row for this request. ([NAACL paper](https://aclanthology.org/2021.naacl-main.235/)) |
| TDC 2023 Red-Teaming Track | The release card identifies the 100-row artifact as a combined development/test set and says some data overlap with HarmBench. The HarmBench paper describes the associated items as harmful-behavior strings, which are not by themselves evidence of jailbreak-attempt framing. It is therefore neither a clean train source nor a proven JB-attempt source. ([release card](https://huggingface.co/datasets/walledai/TDC23-RedTeaming), [HarmBench paper](https://arxiv.org/abs/2402.04249)) |
| WildJailbreak | Its authors and official repository explicitly call it a synthetic safety dataset; it fails the human-authored requirement. ([paper](https://arxiv.org/abs/2406.18510), [official repository](https://github.com/allenai/wildteaming)) |
| AART | The paper’s defining contribution is AI-assisted red-team data generation and augmentation. The metadata reviewed here does not establish a separately attributable human-authored jailbreak-attempt subset suitable as a new source family. ([EMNLP paper](https://aclanthology.org/2023.emnlp-industry.37/)) |

## L2 implication

This search did not establish a source that clears all requested conditions at once. Anthropic HH-RLHF is the strongest independent lead, but admitting it requires a row-level qualification rule that distinguishes standalone human jailbreak attempts from benign or context-dependent openings, followed by the authorized local rights/privacy, provenance, split, and overlap checks. Until those checks are supported, it should not be counted as a new JB family or used to claim independent-source coverage. No L3, test-payload access, model run, or smoke activity is part of this finding.

## Exposure quarantine

Automatic external search/open snippets surfaced example-bearing material from candidate pages and a paper figure while only metadata was being sought. No preview content was copied into the workspace, reported, or used for candidate selection; those snippets are quarantined and excluded from this assessment.
