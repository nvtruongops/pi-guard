# L2 independent-source qualification — round 14

## Scope Boundary Declaration

- Task: continue English-only L2 research and identify a source that can improve independent source/family coverage.
- In scope: source-card/paper metadata, rights and lineage screening, L2 class compatibility, and recording the lessons from prior rounds.
- Out of scope: L3, cascade, smoke tasks, fitting another model without a newly qualified source, and opening PI-Guard's sealed final-test payload. Test evidence remains limited to the approved family-level metadata contract.
- No dataset file was downloaded or opened in this round, and no source row was used for selection or a model run.

## Candidate findings

| Candidate | Primary-source evidence | L2 role | Disposition |
| --- | --- | --- | --- |
| [Microsoft LLMail-Inject paper](https://arxiv.org/html/2506.09956v2), [official repository](https://github.com/microsoft/llmail-inject-challenge) | The authors report 208,095 distinct human-written attack prompts from 839 participants. Records include team ID and phase; the authors recommend team/phase splits to reduce near-duplicate and adaptation leakage. About 29K tool-triggering prompts are behaviorally verified positive examples; the much larger LLM-annotated remainder is not human-gold. The release is MIT-licensed. | Strong conditional PI-only source lead. Team IDs could support grouped split construction, subject to language, duplicate, privacy, and mapping audits. | **Not admitted.** It adds neither benign nor JB. The paper does not provide an English-only partition or prompt-level mapping to its 12-family taxonomy. PI-Guard V9's source-level privacy review still lists LLMail as pending. The Hugging Face card also auto-rendered a row preview during this screen; the preview was excluded from selection and must not be used as evidence. |
| [AI Data Foundation Prompt Injection v3 repository](https://github.com/promptinjection/promptinjection.github.io), [hosted dataset metadata](https://huggingface.co/datasets/AIDataFdn/promptinjection) | The project describes a large mixed prompt-injection/jailbreak/benign corpus, while the hosted metadata declares Apache-2.0 and the project repository says MIT. The hosted README is empty and the viewer exposes a single train split, without reviewed row-level lineage or family/split records. | Mixed classes in headline statistics could appear useful. | **Exclude pending source reconciliation.** License declarations conflict; build lineage, eligible English subset, family IDs, and independent split roles are not established. The viewer auto-rendered row text; no preview content was used. |
| [Horizon-Labs evaluation suite](https://huggingface.co/datasets/Horizon-Labs/prompt-injection-eval-suite) | Its publisher page describes a suite assembled from upstream evaluation datasets, including upstream test partitions; the card's license metadata is `other`. | Evaluation-only discovery index, not a new training source. | **Exclude from L2 train/validation.** Reusing upstream evaluation rows would violate the data/split boundary; source rights and independent family lineage are not qualified. |
| [JailbreakDB](https://huggingface.co/datasets/youbin2014/JailbreakDB) | Its card exposes a binary jailbreak/regular schema and CC-BY-4.0 metadata, but the prior source audit already found incompatible three-class mapping and unresolved parent overlap for this task. | Potential JB/benign lead only. | **Do not reconsider for this package.** The page auto-rendered row text during this screen; all preview content was excluded from selection. See the prior [source audit](source_audit_round03.md) and [round 13 search](source_search_round13.md). |
| [JailbreakBench](https://arxiv.org/abs/2404.01318) | The existing local reference record distinguishes its 100 JBB-Behaviors (behavior seeds) from its separate attack-artifact collection. | Possible JB-only artifact lead, not a three-class source. | **No new source admission.** The local literature record already covers this benchmark; a method/artifact split would need separate prompt-level lineage and overlap qualification. |

For LLMail, “tool-triggering” supports a positive label for the challenge's indirect-injection objective; it does not label the full release, establish human-curator adjudication, or provide benign/JB samples. The paper also describes synthetic benign emails as challenge context; those contextual emails are not standalone benign prompts and were not mapped to the benign class.

## Current package and gate impact

- The official V9 candidate remains `trainable=false` with zero canonical train/validation/test rows. Its status records source-level privacy review as pending for LLMail, TrustAIRLab, and Rubyglask.
- The frozen round07 private research package remains the best model comparator, but its labels are documented native-reference mappings, not curator-reviewed gold. Its source/family OOF does not replace evidence from independent source collections.
- `OWNER_GATE_DECLARATION.json` still has null owner, selection rule, route unit, operating limits, support floors, and latency requirement fields. `GATE_UNSPECIFIED` therefore remains the formal L2 status; local diagnostic limits cannot be promoted to the official rubric.
- No new source cleared all-class support, lineage, rights, privacy, and split gates. No training or validation run was justified by this round.

## Preview exposure and containment

Dataset Viewer previews were automatically included when the AI Data Foundation and JailbreakDB cards were opened; the LLMail card preview was opened by the read-only source researcher. A paper-search excerpt also returned the LLMail data-card example-record section. No prompt text, IDs, or preview-derived feature was copied into the repository, package, split, or model-selection evidence. These previews are excluded from source selection. PI-Guard's sealed final-test payload remains unopened. Future card checks should use publisher documentation or metadata APIs that do not render rows.

## Result and next step

Round 14 improves source knowledge but does not qualify a new L2 dataset. The most useful lead is LLMail as a possible grouped PI-only supplement after the pending source-level privacy review and local language/duplicate audits; it cannot solve the benign/JB source gap by itself. Continue original-publisher screening for independent, non-synthetic benign and JB sources. Do not run another parameter sweep on the frozen package or claim L2 PASS until the data/source gates and owner-declared rubric are satisfied.

## Sources

- [LLMail-Inject paper, authors' data and curation sections](https://arxiv.org/html/2506.09956v2)
- [LLMail-Inject official repository](https://github.com/microsoft/llmail-inject-challenge)
- [Microsoft MSRC announcement of the LLMail-Inject challenge](https://www.microsoft.com/en-us/msrc/blog/2024/12/announcing-the-adaptive-prompt-injection-challenge-llmail-inject/)
- [PI-Guard V9 status](../../../../workspaces/truongnv/pi_guard_pipeline/training_bases/datasets/project_training/versions/pi_guard_v9_english_source_heldout_20261013/STATUS.json) (local-only metadata; not a public link)
