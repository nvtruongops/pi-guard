# Round 30 — first-party metadata screen for independent JB sources

## Scope Boundary Declaration

This round screens public publisher cards and source documentation for independent, single-turn JB train data. It does not download source data or open any source split payload. One public card viewer automatically displayed example rows; that content was quarantined and excluded. PI-Guard test payload, L3/cascade, smoke, commit, and publication remained out of scope.

## Findings

| Candidate | First-party evidence | L2 disposition |
| --- | --- | --- |
| `jackhhao/jailbreak-classification` | The card declares Apache-2.0, describes a 1,306-row prompt classifier, and identifies `verazuo/jailbreak_llms` as the JB prompt source and OpenOrca/GPTeacher as benign sources. The upstream jailbreak collection is the TrustAIR in-the-wild release, which reports prompts collected from four public platforms and carries MIT; the aggregator's Apache declaration does not establish separate rights or record-level source lineage for each upstream sample. [Dataset card](https://huggingface.co/datasets/jackhhao/jailbreak-classification) · [TrustAIRLab source repository](https://github.com/TrustAIRLab/JailbreakLLMs/tree/main) · [GPTeacher source](https://github.com/teknium1/GPTeacher) | Not independent of the existing TrustAIR JB family. No acquisition or fit. Viewer examples were automatically shown while reading the card and were quarantined; none was copied or used. |
| Jailbreak Control Benchmark v1 | The public package is explicitly prompt-free. Its card says the legacy payload was withdrawn pending source-rights and high-risk-content review; MIT covers only public metadata, documentation, and tooling. [Public metadata package](https://huggingface.co/datasets/invarra/jailbreak-control-benchmark-v1-metadata) | Not train data and no payload access. It does not clear the current source-rights/privacy gap. |
| Giskard Phare jailbreak module | Its publisher license file describes modified, translated, and combined test cases seeded from multiple upstream datasets, with per-sample attribution and license fields. [Phare license and provenance](https://huggingface.co/datasets/giskardai/phare/blob/403c55308968d52c049c5ec1ea17024d9c049858/jailbreak/LICENSE.md) | A derived evaluation module, not a clean independent single-turn train source. No acquisition. |

The `jackhhao` card viewer was the only automatic example exposure in this screen. The examples are not reproduced, hashed, classified, or used in any package. No source dataset train, validation, or test payload was deliberately opened.

## Decision and next work

No candidate clears all of independent-source lineage, compatible single-turn JB semantics, rights, privacy, and train-role evidence. No package or model run was justified. Continue searching publisher documentation for a source whose record ancestry and rights are explicit; keep the formal L2 acceptance gate `GATE_UNSPECIFIED`. Do not reuse R29's NeurAlchemy augmentation or conduct parameter sweeps on rejected R27–R29 additions.

PI-Guard test payload stayed closed; no L3, cascade, smoke, commit, or publication occurred in R30.
