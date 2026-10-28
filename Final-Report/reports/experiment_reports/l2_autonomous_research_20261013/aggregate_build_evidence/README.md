---
license: cc-by-4.0
task_categories:
  - text-classification
language:
  - en
tags:
  - red-teaming
  - llm-security
  - jailbreak
  - adversarial-prompts
  - ai-safety
  - safety-evaluation
  - guardrails
  - prompt-injection
  - owasp-llm-top10
  - mitre-atlas
size_categories:
  - 10K<n<100K
pretty_name: "LLM Red-Team Corpus (Core) — license-clean red-team prompts"
configs:
  - config_name: default
    data_files: canonical.parquet
---

# LLM Red-Team Corpus + Taxonomy — Core

> **44,681 prompts for red-teaming and safety-testing LLMs. We collected them
> from 9 public sources, checked every license, masked personal data, and saved
> where each prompt came from. Load it in one line.**

Use one clean dataset instead of downloading and fixing 9 red-team benchmarks by
hand. Every prompt keeps its **source**, **license**, and **citation**. The
`core` tier is safe to use in commercial products — every source is verified
MIT / Apache-2.0 / CC-BY-4.0.

**Other versions:** want *everything* (all 12 sources, 64,458 rows,
non-commercial)? → [`-full`](https://huggingface.co/datasets/rubyglask/llm-redteam-corpus-taxonomy-full).
Only the non-commercial sources? → [`-extended`](https://huggingface.co/datasets/rubyglask/llm-redteam-corpus-taxonomy-extended).

- ✅ **9 sources, license-verified** — checked live against each upstream repo
- ✅ **License-clean core** — safe for guardrail products and evaluations
- ✅ **PII masked** — phone numbers and street addresses replaced with tags
- ✅ **Origin on every row** — easy to reproduce and cite (`sources.json`)
- 🔜 **Mapped to OWASP LLM Top 10 / MITRE ATLAS** (Phase 2, 2026-Q4)
- ♻️ **Living dataset** — we update it every quarter (`vYYYY.QX`)

## Quick start

```python
from datasets import load_dataset

ds = load_dataset("rubyglask/llm-redteam-corpus-taxonomy-core")
print(ds["train"][0]["prompt"])
```

```python
# keep only one source, or only English
hh = ds["train"].filter(lambda r: r["source_id"] == "anthropic_hh")
en = ds["train"].filter(lambda r: r["language"] == "en")
```

Non-commercial sources (BeaverTails, ALERT, ToxicChat) are in the sibling
dataset: `rubyglask/llm-redteam-corpus-taxonomy-extended` (26,748 rows).

## What is inside

| | Core (this dataset) | Extended (sibling) |
|---|---|---|
| Rows | **44,681** | 26,748 |
| Sources | 9 | 3 |
| License | CC-BY-4.0 (commercial OK) | non-commercial |
| Biggest source | HH-RLHF red-team (37,155) | ALERT (14,032) |

**Note on the mix:** 83% of core (37,155 rows) comes from the **HH-RLHF
red-team** set. Each row is the **first human message** of a red-team
conversation. Most are direct harmful requests, but some are ordinary openers
(e.g. *"How are you?"*) — the harmful intent can appear in later turns we do not
include. The other 8 sources (7,526 rows) are curated single-turn attack
benchmarks.

**Sources** (we checked every license against the upstream repo on 2026-07-03):

| source_id | origin | license | n |
|---|---|---|---|
| anthropic_hh | HH-RLHF red-team-attempts | MIT | 37,155 |
| aart | AART (Google) | CC-BY-4.0 | 3,213 |
| harmfulqa | HarmfulQA | Apache-2.0 | 1,938 |
| do_not_answer | Do-Not-Answer | Apache-2.0 | 938 |
| advbench | AdvBench | MIT | 520 |
| harmbench | HarmBench | MIT | 393 |
| forbidden_question_set | "Do Anything Now" | MIT | 390 |
| jailbreakbench | JailbreakBench | MIT | 80 |
| tdc23 | TDC 2023 Red-Teaming | MIT | 54 |

Full per-source attribution: [`sources.json`](sources.json).

## Fields

Each row has:

| field | type | what it means |
|---|---|---|
| `scenario_id` | str | id inside this tier, like `CN_0000001` |
| `prompt` | str | the prompt, from the source (with PII masked) |
| `prompt_normalized` | str | lowercased, spaces cleaned (used to find duplicates) |
| `exact_hash` | str | SHA-256 of `prompt_normalized` |
| `language` | str | ISO code (`en`, …) |
| `source_id` | str | which source it came from |
| `source_original_id` | str | its id inside that source |
| `source_license` | str | that source's license |
| `license_tier` | str | `core` |
| `taxonomy_hints` | str | JSON string, `"{}"` for now — **filled in Phase 2** |
| `provenance` | str | JSON string `{source_url, source_citation}` |

Formats in the repo: **Parquet** (default) · **JSONL.gz** · **DuckDB**.

## When to use this

- You build or test **guardrails / safety filters** and want one clean,
  license-safe set instead of joining 9 sources by hand.
- You want to **reproduce red-team research** with the origin kept.
- You **teach or evaluate AI safety** against known attack types.

## When NOT to use this

- You need **one specific benchmark** (like only HarmBench for a paper) — use
  the original. This is a mix, not a replacement.
- You need the **biggest possible set** — single sources (like BeaverTails 330K)
  are larger. This dataset is about **clean + unified**, not size.
- You want a **pure single-turn attack set** — remember 83% here is HH-RLHF
  first turns; filter by `source_id != "anthropic_hh"` for the curated 7,526.

## Privacy (PII)

A few source prompts contained real phone numbers and street addresses (for
example, doxxing-style requests). We **mask** these with `[PHONE]` and
`[ADDRESS]` tags. Some named-person mentions may remain in the text. If you find
personal data that should be removed, open an issue.

## Ethics and dual-use

This is a dataset for **defensive research**. Every prompt is **already public**
in research or industry sources, so safety teams can test against them. Do
**not** use them to attack systems without permission. Please follow responsible
disclosure.

**Excluded on purpose:** StrongREJECT (mixes in no-license questions),
WMDP (dual-use weapons-proxy knowledge), and Persuasion (not attack prompts).
See `docs/license_matrix.md`.

## How we build it (reproducible)

```
9 public sources → PII mask → canonical schema → exact-hash dedup (−4%) → parquet / jsonl / duckdb
```

You can rebuild everything from
`github.com/rubyglask/llm-redteam-corpus-taxonomy`
(`pip install -e .` → `import_all` → `build_corpus` → `verify_checksums`).
The build is deterministic, and every release ships SHA-256 checksums.

## Roadmap

- **Now (v0.1.0):** 12 sources (9 core + 3 extended), 71,429 prompts.
- **Phase 2 (Q4):** fill `taxonomy_hints` — map each prompt across OWASP LLM
  Top 10 / MITRE ATLAS / NIST AI RMF / EU AI Act / ISO 42001 / KISA.
- **Every quarter:** add new public sources + a short changelog paper.

Not included yet: 2 sources waiting for a license check (MaliciousInstruct,
Korean UnSmile).

## Citation

```bibtex
@misc{rubyglask2026llmredteamcorpus,
  author = {rubyglask},
  title  = {LLM Red-Team Corpus + Taxonomy},
  year   = {2026},
  howpublished = {\url{https://github.com/rubyglask/llm-redteam-corpus-taxonomy}}
}
```
(Zenodo DOI + arXiv preprint: Phase 1 Week 8.) Each source also keeps its own
citation — see `provenance` on every row and `sources.json`.

---

<!-- ===== For programmatic / agent access ===================================
Machine-readable summary for tools and LLM agents:

DATASET: rubyglask/llm-redteam-corpus-taxonomy-core
PURPOSE: LLM red-team / jailbreak / safety-evaluation prompts
ROWS: 44681  | LICENSE: CC-BY-4.0 (commercial OK)  | LANG: en
SIBLING (non-commercial): rubyglask/llm-redteam-corpus-taxonomy-extended (26748 rows)
LOAD: load_dataset("rubyglask/llm-redteam-corpus-taxonomy-core")
KEY_FIELDS: prompt (str), source_id (str), source_license (str), language (str)
FILTER_BY: source_id, language, license_tier
SOURCES: advbench, harmbench, jailbreakbench, tdc23, forbidden_question_set,
         do_not_answer, harmfulqa, aart, anthropic_hh
NOTE: 83% of rows are anthropic_hh (HH-RLHF red-team first human turn);
      filter source_id != "anthropic_hh" for 7526 curated single-turn attacks.
PII: phone/address masked as [PHONE]/[ADDRESS].
USE_FOR: guardrail testing, safety benchmarking, red-team research (defensive)
NOT_FOR: single-benchmark replacement, unauthorized attacks
========================================================================= -->
