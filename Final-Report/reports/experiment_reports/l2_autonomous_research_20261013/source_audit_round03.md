# Source qualification — continuation round 03

**Status:** no package qualified; no fit was authorized by the data gates.  
**Data boundary:** reviewed pinned cards and existing aggregate audits; where source data were read, only previously acquired upstream train shards were used. No new upstream validation/test payload was opened. No prompt text or matched privacy-pattern content is reproduced here.

## Scope Boundary Declaration

The user removed the curator-approval dependency and approved a family-level sealed test contract. Native source labels and explicit reproducible mappings may therefore be research reference labels, but they are not human gold. Rights, provenance, privacy, independent-family, duplicate, and frozen-split gates still apply. This round did not run L2 or L3 and did not open a final test payload.

## Candidate findings

| Candidate | Verified train-only evidence | Disposition |
|---|---|---|
| CiberIA PromptRisk v1 | Pinned train shard: 2,448 rows, 2,448 unique prompts, declared CC BY 4.0, one synthetic collection family. Applying the pinned py3langid model and 0.95 threshold yields 771 accepted-English rows: 394 benign, 100 PI from direct/indirect injection categories, and 51 JB from the explicit jailbreak category; 226 other attack rows remain unmapped. | Useful reference-label candidate, but a single family and only 51 clear English JB rows. It cannot independently meet the 100-per-class validation or L3-train REVIEW floors. The pinned provenance note also lacks original templates and a complete generation log. [[2]](#ref2) [[9]](#ref9) [[13]](#ref13) |
| NeurAlchemy core | Only `core/train` was audited: 4,391 rows. Native category/source cross-tab shows 124 `jailbreak` rows in `neuralchemy_v1` and 13 in `original`; HackAPrompt contributes 1,383 `direct_injection` rows. The source card assigns component-specific terms, including Research for WildGuard/JudgeComparison; 211 train rows use that source. Aggregate privacy scan flags 8 email-pattern, 1 credential-assignment-pattern, and 7 IPv4-pattern rows; matched content was not emitted. | Do not use the full shard. Source-component licensing and category mapping must be applied row by row, ambiguous/HarmBench behavior-goal rows quarantined, and privacy matches resolved or excluded. Source values alone do not prove independent lineages. Validation and test shards remain unopened. [[1]](#ref1) [[8]](#ref8) [[10]](#ref10) |
| Wambo prompt-injections | Existing `train` only: 5,189 rows, 2,109 benign and 3,080 native binary malicious; 218 malicious rows have a category containing “jailbreak.” The pinned README declares MIT and says prompts were LLM-generated, but does not identify model/version, generation prompts/seeds, or upstream component sources; no standalone license file was found in the pinned repository tree. | Keep outside a trainable package until the declared license and generation/source lineage are sufficiently evidenced. A category substring is not itself a PI-Guard label. The upstream test shard was not opened. [[6]](#ref6) [[7]](#ref7) |
| Mirzaakhi Prompt Injection | Existing upstream train only: 4,212 rows; 2,210 benign, 1,966 provisional PI, and 36 `persona_jailbreak` reference rows. It is one source family and has seven exact normalized overlaps with NeurAlchemy train. | The native category supports a transparent provisional rule, but 36 JB rows are insufficient alone for validation/L3 support. Resolve cross-source overlaps and record licensing/lineage/privacy evidence before use. No upstream test was opened. [[10]](#ref10) |
| 3nesdeniz boundary pairs | Pinned upstream train: 840 English rows, 420 `benign_boundary` and 420 `prompt_injection`; deterministic publisher build artifacts and source hashes are recorded. The native target remains binary; `roleplay_jailbreak` is an attack-family value under the source's `prompt_injection` target, not a native JB label. | Clean PI/benign reference candidate, but it supplies no independent JB class. Keep all other split payloads closed until selection is locked. [[5]](#ref5) [[11]](#ref11) |
| JackHhao jailbreak classification | The card declares Apache 2.0 and describes jailbreak prompts from Verazuo plus benign prompts from OpenOrca and GPTeacher; its listed row schema has only `prompt` and `type`, with no per-row source field. | Cannot bind each row to its upstream source/license or prove row-level lineage from the available release metadata. Do not mix it into a source-qualified split. [[4]](#ref4) |
| PromptSentinel | The publisher reports 156,802 prompts and three labels, but the repository requires contact-information sharing for access and declares license `other`. Its source table includes non-commercial and unspecified component licenses; its release split groups by template family, not source family. | Do not accept the access terms or acquire payloads. The card itself is insufficient to clear component rights and source-family partitioning. [[3]](#ref3) |
| JailbreakDB | Its native corpus distinguishes jailbreak/adversarial from benign and records `source` and `tactic`; it does not supply a native PI class. Earlier research opened this corpus, so it is ineligible as a sealed final-test source. | Possible train/validation reference only after per-source rights/privacy review and a strict tactic rule; not a current package source and not a final test. [[12]](#ref12) |

Local aggregate evidence is preserved in [the NeurAlchemy train audit](source_qualification/neuralchemy_core_train_audit.json), [the source mapping audit](source_qualification/source_mapping_audit_round02.json), [the CiberIA candidate audit](../../../../workspaces/truongnv/pi_guard_pipeline/training_bases/datasets/source_datasets/ciberia_promptrisk_candidate/CANDIDATE_AUDIT.json), [the CiberIA source review](../../../../workspaces/truongnv/pi_guard_pipeline/training_bases/datasets/source_datasets/ciberia_promptrisk_candidate/SOURCE_REVIEW.md), [the CiberIA English/category screen](source_qualification/ciberia_english_mapping_screen_round03.json), and [the 3nesdeniz train acquisition manifest](source_qualification/acquisition_manifest.json). These records contain counts and provenance, not prompt samples.

## Gate result and next state

The current V9–V12 package set still fails metadata preflight. The approved contract is test-family metadata only; it does not waive source proof or allow test-payload access before the model/configuration and thresholds are locked. For the strongest presently clean-looking English mapping, CiberIA plus Mirza contributes at most 87 explicit JB train rows before OOF REVIEW routing; that is already below the protocol's 100-row L3-train REVIEW floor, and neither source by itself provides disjoint train/validation/test families. No source combination has yet been shown to satisfy all gates.

Therefore the next valid step is to qualify another independently lineaged JB source and close the remaining rights/privacy/source-attribution findings, then freeze train/validation row manifests and test-family aggregate metadata. Only after that may the adapter fit the fixed L2 baseline. No curator signoff is listed as a blocker.

## References

<a id="ref1"></a>**[1]** NeurAlchemy, [Prompt Injection and Jailbreak Detection Dataset card](https://huggingface.co/datasets/neuralchemy/Prompt-injection-dataset), including source-specific license table, taxonomy, and group-level split description. Local pinned revision: `7d70432dfcf47a821612cbf9d34e9d9e3ad20e75`.

<a id="ref2"></a>**[2]** CiberIA, [CiberIA PromptRisk v1 dataset card](https://huggingface.co/datasets/gcjordi/CiberIA-PromptRisk-v1), pinned revision `d25fd20437a757cd47a473d9139947d9de227323`.

<a id="ref3"></a>**[3]** Nuhman PK, [PromptSentinel dataset card](https://huggingface.co/datasets/nuhmanpk/prompt-sentinel), access and component-source terms reviewed 2026-10-13.

<a id="ref4"></a>**[4]** JackHhao, [Jailbreak Classification dataset card](https://huggingface.co/datasets/jackhhao/jailbreak-classification), source and row-schema description.

<a id="ref5"></a>**[5]** Enes Deniz, [Agentic Prompt-Injection Boundary Pairs](https://huggingface.co/datasets/3nesdeniz/agentic-prompt-injection-boundary-pairs/tree/a5682e7573e1c7bc4b12e64d49c0dcd90ca776cf), pinned revision and published build artifacts.

<a id="ref6"></a>**[6]** WamboSec, [prompt-injections dataset card](https://huggingface.co/datasets/wambosec/prompt-injections/tree/071ee17a60112b7f9f808398156b430aadfaf1d2), pinned revision.

<a id="ref7"></a>**[7]** Local WamboSec [source review](../../../../workspaces/truongnv/pi_guard_pipeline/training_bases/datasets/source_datasets/wambosec_prompt_injections_candidate/SOURCE_REVIEW.md), train-only counts and unresolved lineage/licensing notes.

<a id="ref8"></a>**[8]** Local [NeurAlchemy core/train audit](source_qualification/neuralchemy_core_train_audit.json), train-only source/category/license/privacy aggregates.

<a id="ref9"></a>**[9]** Local CiberIA [candidate audit](../../../../workspaces/truongnv/pi_guard_pipeline/training_bases/datasets/source_datasets/ciberia_promptrisk_candidate/CANDIDATE_AUDIT.json) and [source review](../../../../workspaces/truongnv/pi_guard_pipeline/training_bases/datasets/source_datasets/ciberia_promptrisk_candidate/SOURCE_REVIEW.md).

<a id="ref10"></a>**[10]** Local [source mapping audit](source_qualification/source_mapping_audit_round02.json), train-only native-category mappings and exact-overlap aggregates for NeurAlchemy, Wambo, and Mirza.

<a id="ref11"></a>**[11]** Local [3nesdeniz train acquisition manifest](source_qualification/acquisition_manifest.json) and [train structure audit](source_qualification/train_structure_audit.json); upstream train only.

<a id="ref12"></a>**[12]** PromptSecurity, [JailbreakDB dataset card](https://huggingface.co/datasets/youbin2014/JailbreakDB), field definitions for `jailbreak`, `source`, and `tactic`.

<a id="ref13"></a>**[13]** Local [CiberIA English/category screen script](source_qualification/audit_ciberia_english_mapping_round03.py) and [aggregate result](source_qualification/ciberia_english_mapping_screen_round03.json). It verifies the pinned train hash, applies the py3langid model SHA-256 and 0.95 threshold, and emits no prompt text.
