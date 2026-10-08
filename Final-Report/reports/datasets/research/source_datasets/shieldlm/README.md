# ShieldLM Prompt Injection snapshot

Source: [Abdennebi/shieldlm-prompt-injection](https://huggingface.co/datasets/Abdennebi/shieldlm-prompt-injection), pinned revision `23330588198f0143120e93b7d7b31cc164cd5403`. The authenticated `hf` CLI read metadata and downloaded train/validation/test Parquet files.

## Label taxonomy and rationale

The card stores four mutually exclusive `label_category` values under a hierarchical scheme: benign, direct injection, indirect injection, and jailbreak. For comparison with a three-output PI-Guard model, this folder proposes grouping direct and indirect injection under PI, retaining jailbreak as JB, and benign as benign. Original category and contextual fields remain unchanged. Indirect injection is context-dependent, so future normalization must retain the provided context rather than classify an isolated payload as PI automatically.

The card's key labeling argument is that JailbreakBench harmful-goal prompts are marked benign because they describe harmful topics but do not themselves use an injection/jailbreak technique. It also includes clean structured tool responses to avoid learning that JSON/application format alone implies an attack. The card says the split is random stratified by category (seed 42); the local snapshot audit found no exact-text overlap across splits.

## Local split counts after proposed mapping

| Split | Rows | benign | PI | JB |
|---|---:|---:|---:|---:|
| train | 37,913 | 24,638 | 12,563 | 712 |
| validation | 8,124 | 5,279 | 2,692 | 153 |
| test | 8,125 | 5,280 | 2,692 | 153 |

JB is 1.88% of train (PI:JB = 17.6:1), so JB is still a minority class. After mapping, this is a useful three-label candidate but should be evaluated with per-class recall/F1 and a source-wise breakdown. The card says it has 11 source datasets; the downloaded `source` field contains 13 distinct values because sources such as InjecAgent are represented by granular configurations. The count is therefore not directly comparable until source IDs are normalized.

Train JB is also concentrated in one source: 702/712 rows (98.6%) are from TrustAIRLab and the remaining 10 are from jackhhao. SPML contributes 8,798/12,563 PI rows (70.0%). Since the card describes a random stratified split, the same source styles can appear on both sides of the split. Treat the official split as an in-corpus evaluation; add source-held-out results to support cross-source generalization claims.

The card lists MIT for the curation, but the raw rows do not carry per-row license metadata. Its source table includes a CC-BY-NC-SA source and other terms; do not treat every row as MIT-relicensed. Resolve component-level terms before redistributing or training on a filtered subset. The card also says the data is English-dominant (>98%) and single-turn.

## Papers and source code

The dataset card provides a software citation, not a dedicated peer-reviewed paper for ShieldLM itself. See [`paper/README.md`](paper/README.md) for source-paper links and label rationale. No model fit or inference was run.

## Proposed component-level disposition

The Parquet rows contain `source`, so a component-level audit is possible. The candidate counts below are from the pinned local **train** split, before overlap filtering; they are not accepted PI-Guard training counts.

| Source field | Train rows by proposed label | Component paper | Conditions before use |
|---|---:|---|---|
| `spml/chatbot-prompt-injection` | 8,798 PI; 2,341 benign | [arXiv:2402.11755](https://arxiv.org/abs/2402.11755) | Preserve `context`; source card says injection is relative to system prompt and discourages prompt-only detector training. Resolve license conflict: ShieldLM card says CC-BY-4.0, direct SPML snapshot declares MIT. |
| `trustailab/in-the-wild-jailbreak-prompts` | 702 JB | [arXiv:2308.03825](https://arxiv.org/abs/2308.03825) | Resolve license conflict: ShieldLM card says CC-BY-NC-SA-4.0, direct TrustAIRLab snapshot declares MIT. Deduplicate against the direct source already stored in this workspace. |
| `injecagent/*` | 738 PI; 24 benign | [arXiv:2403.02691](https://arxiv.org/abs/2403.02691) | Preserve tool/application context. The card's 1,054 attack cases and the aggregate's split row totals are not the same denominator; reconcile before copying. |
| `jailbreakbench/jbb-behaviors` | 135 benign | [arXiv:2404.01318](https://arxiv.org/abs/2404.01318) | Keep, if needed, as a hard-benign stress stratum; do not count as attack data. |

The other source fields remain outside the candidate set until an exact component paper, source revision, and applicable license are recorded. The aggregate card lists 11 source datasets but the local `source` field has 13 values; the listed source counts also do not reconcile exactly to the aggregate total. For these reasons, the proposal is to split by `source`, preserve each original category/context and hash, create standalone component folders with their own `paper/` and README only after terms are confirmed, and then remove the aggregate Parquet payload. Keep a compact provenance/audit record for the aggregate. **This is a proposal only; no rows were extracted and no folder was deleted.**
