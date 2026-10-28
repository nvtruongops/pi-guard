# L2 source qualification — round 20

## Scope Boundary Declaration

This round screens newly discovered primary-source leads for L2 source coverage. It does not acquire source data, modify a train/validation package, inspect any PI-Guard final-test payload, train/evaluate L2 or L3, run smoke work, or contact a source owner. Labels remain provisional references, not curator-reviewed gold.

## Decision

**No new source is admitted. No training run is justified by this screen.** The strongest new leads are prompt-injection collections, not independent human-authored jailbreak-attempt collections. Rights, privacy, task-unit, family, and source-composition gates remain unresolved for the attack data.

## Candidate findings

| Candidate | First-party evidence | L2 disposition |
| --- | --- | --- |
| Gandalf RCT / *Gandalf the Red* | The ICML paper describes a crowd-sourced, gamified red-teaming platform and a release of 279k prompt attacks. The associated RCT card describes one combined 339k-row interaction log with prompt/guess kinds, a random session identifier that may change after browser restarts, and fields for passwords, answers, and outcomes; its declared license is `other` with a custom license file. [ICML paper](https://proceedings.mlr.press/v267/pfister25a.html) · [dataset card](https://huggingface.co/datasets/Lakera/gandalf-rct) | **Not admitted.** Attempts to extract an application secret are closer to prompt injection/exfiltration than jailbreaks against model safety policy. The card does not supply a clean L2 train/validation partition or establish person-level family independence, reuse rights, or complete privacy review. The interaction log also contains outcome/response/secret fields that would require strict filtering and review before any future use. |
| Gandalf summarization subset | The publisher documents 140 indirect-injection items across train/validation/test (114/13/13), filtered from one Adventure 4 collection, with a random 80/10/10 row split and an MIT license. [publisher dataset card](https://huggingface.co/datasets/Lakera/gandalf_summarization) | **Not admitted.** This is PI, not JB; it is one narrow collection family and the random row split is not source-family held-out evidence. Its scale and one-adventure context do not close the project’s independent JB-source gap. |
| Cogensec Jailbreak Corpus v0.3 | The publisher declares 59,508 records, including 43,026 real seeds aggregated from 14 public datasets and 16,482 synthetic augmentations. It reports group-aware splits, mixed-source attribution, a request-access gate, concentrated sources, mostly unspecified provenance, and weak rule-based labels/outcomes. [publisher dataset card](https://huggingface.co/datasets/Cogensec/jailbreak-corpus) · [publisher release page](https://cogensec.com/datasets) | **Not admitted; no access request made.** The “real seed” subset is not equivalent to independently verified human-authored JB. The card names constituent datasets but does not establish a qualified non-TrustAIR human JB family with component-level rights, privacy, and role evidence. The access form requires a named requester, affiliation, intended use, and acceptance of a responsible-use policy; this research did not submit it. Synthetic rows are disallowed by the task. |

## L2 consequence and next step

The source-family gate in the attached task requires at least two independent train families per class and separate validation and test families per class. Round20 contributes no qualified JB family. The earlier pinned CLINC audit remains a possible additional benign train family, but it is still a provisional mapping with incomplete privacy review and only one collection family. Thus the current NOT_READY decision is unchanged; no parameter sweep on the existing package would resolve the missing source evidence.

Continue searching first-party publications and repositories for a separately released, non-TrustAIR, non-synthetic, human-authored JB-attempt corpus with clear reuse rights, privacy treatment, native attempt semantics, family/duplicate structure, and an eligible L2 train role. Do not infer jailbreak labels from harmful requests, model responses, challenge success, or the first turn of a multi-turn conversation.

## Exposure quarantine note

An official Gandalf RCT dataset page automatically rendered record previews, including identifiers and prompt/response fields. A search result for the official Gandalf summarization card also surfaced example content. Those preview contents were not copied into this report, saved as research data, or used to select rows. Quarantine the exposures and do not inspect the candidate payloads in a future turn without an explicitly safe review protocol. This concerned external source previews, not PI-Guard's sealed final-test payload, which remained unopened.
