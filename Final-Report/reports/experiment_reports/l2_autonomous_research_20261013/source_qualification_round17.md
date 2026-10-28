# L2 source qualification — round 17

## Scope Boundary Declaration

This round advances L2 train/validation source qualification only. It audits pinned public training-side candidate sources and their provenance, class fit, duplicates, privacy indicators, and split compatibility. PI-Guard's sealed test payload, L3, cascade, smoke execution, commits, and publication are out of scope. No new source is admitted to an L2 package by this report.

## Audited candidates

| Candidate | Aggregate-only audit result | L2 disposition |
| --- | --- | --- |
| Databricks Dolly 15k | Pinned train source: 15,011 rows. The round16 audit retained 10,354 instruction-only candidates after excluding context-bearing rows, detectable privacy indicators, review flags, source duplicates, and exact overlap with the locked train/validation package. | Best benign-train candidate, still provisional. Human-authored instruction is not a canonical benign label; screening is not a complete safety/privacy review. Do not package until the residual ambiguity and privacy evidence are resolved. |
| OpenAssistant OASST1 | Pinned train parquet: 84,437 messages; 3,482 English root prompter messages. Excluded 1,377 rows with positive native review flags and 2 rows with regex privacy indicators. After exact deduplication and exact overlap removal against round07 train/validation, 2,089 unique candidate texts remain. | Provisional benign-train candidate only. Root user role does not prove benign intent; native positive review flags and regex indicators are exclusions, not complete adjudication or privacy clearance. |
| JailbreakBench artifacts | Pinned `JailbreakBench/artifacts` revision; 24 non-test JSON files (4,282,573 bytes); all 7 `test-artifact` paths and the `evaluation.json` file excluded. The `prompt` field yielded 2,037 occurrences, 1,097 normalized unique prompts, 430 duplicate groups/940 duplicate occurrences, zero exact overlap with round07 train/validation, 105 goal/behavior ancestry keys, and zero regex privacy indicators. Attack-method counts: DSN 600, GCG 400, JBC 400, PAIR 237, and prompt-with-random-search 400. | Conditional JB-attempt reference source. Group by behavior ancestry before any split. These are empirical algorithmic attack artifacts, not naturally occurring human jailbreaks; method/model variants do not count as independent collections. Regex and exact-duplicate screening do not establish full privacy or semantic independence. |
| LLMail-Inject | Full aggregate audit is running against pinned labelled-unique Phase 1 and Phase 2 files only. The raw submission shards and the separate false-positive test file were not acquired; no row text or identifier is emitted. | Conditional PI-only candidate. Its email/tool-use challenge context and absent submitter/family identifiers in the labelled-unique export limit task and group compatibility. Do not admit before audit completion and source-level privacy/split review. |

The exact source pins, hashes, schemas, and audit counters are retained in the adjacent `*_round17.json` summaries and private ignored source-audit directory. Text, row identifiers, and per-row hashes are not copied into this report.

## Additional independent-source leads

The original HackAPrompt publisher describes a human-submission competition with separate playground and formal-submission streams, and the dataset card declares MIT. Its Hub files are gated behind agreeing to share contact information. The publisher says the released records are anonymous and no direct personal/sensitive information was intentionally released, but also says the dataset was not curated and may contain offensive material. Its challenge success field is an outcome measure, not a PI/JB taxonomy. This is a promising independent PI-attempt lead, but this round did not accept the access gate, download rows, or admit it. A safe next step needs a permitted non-gated copy or user-authorized access route, followed by prompt-field, privacy, duplicate, and challenge-family audits. [Publisher paper and data description](https://paper.hackaprompt.com/); [dataset card and access terms](https://huggingface.co/datasets/hackaprompt/hackaprompt-dataset).

The expanded TrustAIRLab/JailbreakHub collection reports 1,405 in-the-wild jailbreak prompts, but it is the same research collection lineage already represented in the current package; it can add rows or communities but does not independently solve the publisher/source-held-out gap. The General Analysis jailbreak benchmark explicitly describes its 2,795 prompts as synthetic and is excluded under this task's no-synthetic-source rule. [TrustAIRLab paper/repository](https://github.com/verazuo/jailbreak_llms); [General Analysis dataset card](https://huggingface.co/datasets/GeneralAnalysis/GA_Jailbreak_Benchmark).

MHJ remains excluded: it is a gated multi-turn red-team corpus under CC-BY-NC-4.0, so it does not fit the project's single-input L2 train/validation source contract. JailbreakDB remains conditional because its mixed-source corpus includes synthetic and automatically generated components; its aggregate license/source declaration is insufficient to admit selected rows without original-source-specific lineage and rights.

## Qualification decision and next action

Round17 improves the evidence base by auditing independent benign, algorithmic-JB, and PI candidates. It does **not** yet yield a package-ready, privacy-cleared source contribution. Dolly and OASST need stronger benign-intent/privacy qualification; JailbreakBench needs full privacy and ancestry adjudication; LLMail's full audit is pending and has a challenge-specific observation unit; HackAPrompt is gated and its outcome labels do not directly distinguish PI from JB. No new package or model run is justified by these candidates yet. Continue L2 source qualification and favor a complete source-held-out validation design over more parameter sweeps on the locked round07 package.

The official owner gate remains `GATE_UNSPECIFIED`; therefore, even a future private reference-label run can support an L2 research result but cannot establish formal L2 `PASS` without the approved rubric. Curator approval is not required to study native/reproducible mappings, per the user's instruction; this does not convert those mappings into canonical labels.

## Preview handling disclosure

Opening the LLMail-Inject Hugging Face page automatically rendered several dataset-viewer prompt rows in the browser result. Those rows were not copied, quoted, classified, selected, or used. The source audit uses only the previously pinned labelled-unique files and aggregate counters; the separate false-positive test file and PI-Guard test remain unopened.
