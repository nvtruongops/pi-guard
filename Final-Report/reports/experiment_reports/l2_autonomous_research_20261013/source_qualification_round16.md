# L2 source qualification leads — round 16

## Scope Boundary Declaration

- Task: identify actionable, independently sourced benign and jailbreak inputs after the round12 diagnosis.
- In scope: official source-card/repository metadata, publisher-authorship, license, split structure, source-family metadata, and the minimum audit needed before creating a new private L2 package.
- Out of scope: L3/cascade, smoke tasks, downloading or opening source rows in this metadata pass, and PI-Guard's sealed final-test payload. No source is admitted by this report.

## New leads

| Source | Publisher-backed facts | Potential use | Remaining qualification before any package/run |
| --- | --- | --- | --- |
| [Databricks Dolly 15k](https://huggingface.co/datasets/databricks/databricks-dolly-15k), [author description](https://www.databricks.com/blog/2023/04/12/dolly-first-open-commercially-viable-instruction-tuned-llm) | English instruction-following prompts authored by more than 5,000 Databricks employees; the card has one `train` split and a CC-BY-SA-3.0 data license. The card says contributors were instructed not to use generative AI. The publisher says, to its knowledge, the data contains no PII about non-public figures, but notes possible typos/factual errors and Wikipedia context passages in some rows. | **Best current benign training lead.** Use the `instruction` field only; do not turn a response or reference passage into an L2 input. | Pin the Hub commit and file hash; audit English, exact/near duplicates against current package, injection/JB/unsafe intent, PII indicators, and context-field eligibility. Native task categories are not safety labels, so keep any mapping explicitly provisional and exclude ambiguous prompts. Carry CC-BY-SA attribution/notice into the private package and its documentation. Categories are task types, not independent source collections. |
| [JailbreakBench artifact repository](https://github.com/JailbreakBench/artifacts), [benchmark paper](https://arxiv.org/abs/2404.01318) | The artifact publisher says each artifact is released under MIT by its author. Artifacts are attack prompts/responses with method, target-model, query, and attack-success metadata; the benchmark distinguishes the artifact repository from its harmful/benign behavior seeds. | **Conditional JB attack-artifact lead** for source-aware L2 training or validation. Method/model fields could support grouped analysis and the success flag can support a conservative attack-attempt reference mapping. | Pin the artifact revision and per-author metadata; use only the prompt field; audit source/behavior overlaps with existing package, duplicates across attack methods, family grouping, and unsafe content. Keep algorithmically produced attacks distinct from naturally occurring human jailbreaks; do not claim population prevalence. Confirm the task permits this empirical attack-artifact arm before admission. Behavior seeds alone are not jailbreak prompts. |

## Fit with the source-coverage problem

Dolly can add an independent, human-authored benign stream without synthetic prompt generation, while the JailbreakBench artifacts can add empirically submitted attack-method families if their lineage and source role pass audit. Together they are more actionable than another model-parameter sweep, but neither metadata card alone proves label compatibility, privacy clearance, source-disjoint validation, or L2 readiness. The current package must remain frozen until those audits produce an exact, versioned source component.

The candidate package design, if the audits pass, is to keep the original round07 package byte-identical and create a new private package version with explicitly attributed source components. Compare the original C=2 JB-moderated run to one full L2 run on the expanded data, then use complete family/source-aware held-out evidence. Avoid counting Dolly's task categories as distinct source collections, and group JBB artifacts by behavior ancestry to prevent the same harmful seed leaking across partitions. Preserve `GATE_UNSPECIFIED` unless the owner declaration is formally changed.

## Current blockers

- Dolly is an instruction-following corpus, not a benign safety-labeled dataset. Mapping its rows to benign is a research reference only and must exclude adversarial, harmful, ambiguous, duplicate, context-only, or privacy-flagged entries.
- JBB attack artifacts are benchmark submissions whose strings were produced by named attacks and target models. They are useful as an attack-method robustness stream, but they are not human in-the-wild examples and may share underlying behaviors with existing sources.
- PI-Guard's existing train/validation families, manifest hashes, source roles, and results must remain unchanged; candidate data belongs in a new package and unique run path only.
- Official L2 acceptance remains `GATE_UNSPECIFIED`; improved source coverage alone cannot supply missing acceptance criteria.

## Sources

- [Databricks Dolly dataset card](https://huggingface.co/datasets/databricks/databricks-dolly-15k)
- [Databricks' dataset release and authoring/licensing description](https://www.databricks.com/blog/2023/04/12/dolly-first-open-commercially-viable-instruction-tuned-llm)
- [Databricks Dolly repository notes on dataset limitations](https://github.com/databrickslabs/dolly/blob/master/README.md)
- [JailbreakBench artifact repository](https://github.com/JailbreakBench/artifacts)
- [JailbreakBench paper](https://arxiv.org/abs/2404.01318)
- [Earlier source rounds 13–15](source_search_round13.md), (source_search_round14.md), and (source_search_round15.md)
