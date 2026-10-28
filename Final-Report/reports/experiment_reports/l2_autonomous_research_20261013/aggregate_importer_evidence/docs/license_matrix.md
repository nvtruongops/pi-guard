# License Matrix — Upstream Sources

> **Status:** Verified against upstream HF/GitHub APIs on **2026-07-02** (GATE 0).
> Each `license` value below was fetched live (HF `cardData.license` or GitHub
> license API), not transcribed from memory. Re-verified every release.

Each upstream dataset is classified by **verified** license into:
- **core** — permissively licensed (MIT / Apache-2.0 / CC-BY-4.0), commercially
  usable → aggregated under CC-BY-4.0.
- **extended** — non-commercial (CC-BY-NC / -NC-SA) → separate distribution.
- **pending** — upstream declares **no machine-readable license**; redistribution
  right is unconfirmed. **Excluded from v0.1.0** until the source's README/paper
  is manually verified (Phase 1 Week 2).

## Verification method

For every source, license was fetched programmatically:
- HF datasets: `GET https://huggingface.co/api/datasets/{repo}` → `cardData.license`
- GitHub-only: `GET https://api.github.com/repos/{repo}/license` → `spdx_id`

Result recorded below. A value of "(none)" means the upstream ships no SPDX
license identifier — this is a redistribution risk, not a green light.

## Core tier — license-verified, permissive (9 sources)

| # | Source | Upstream | Verified license (2026-07-02) | Tier |
|---|---|---|---|---|
| 1 | **AdvBench** | github: llm-attacks/llm-attacks | MIT | core |
| 2 | **HarmBench** | github: centerforaisafety/HarmBench | MIT | core |
| 3 | **JailbreakBench** | HF: JailbreakBench/JBB-Behaviors | MIT | core |
| 4 | **TDC 2023 Red-Teaming** | HF: walledai/TDC23-RedTeaming | MIT | core |
| 5 | **ForbiddenQuestionSet** | HF: TrustAIRLab/forbidden_question_set | MIT | core |
| 6 | **Do-Not-Answer** | HF: LibrAI/do-not-answer | Apache-2.0 | core |
| 7 | **HarmfulQA** | HF: declare-lab/HarmfulQA | Apache-2.0 | core |
| 8 | **AART** | HF: walledai/AART | CC-BY-4.0 | core |
| 9 | **Anthropic HH-RLHF (red-team split)** | HF: Anthropic/hh-rlhf | MIT | core |

## Extended tier — non-commercial (3 sources)

| # | Source | Upstream | Verified license (2026-07-02) | Tier |
|---|---|---|---|---|
| 10 | **BeaverTails** | HF: PKU-Alignment/BeaverTails | CC-BY-NC-4.0 | extended |
| 11 | **ALERT** | HF: Babelscape/ALERT | CC-BY-NC-SA-4.0 | extended |
| 12 | **LMSYS Toxic-Chat** | HF: lmsys/toxic-chat | CC-BY-NC-4.0 | extended |

## Excluded — kept out of v0.1.0 on purpose (3 sources)

| # | Source | Upstream | License | Reason |
|---|---|---|---|---|
| 13 | **StrongREJECT** | github: alexandrasouly/strongreject | MIT (custom) + **borrowed no-license Qs** | README: custom data is MIT, but questions sourced from prior work keep their original license — including **MaliciousInstruct / HarmfulQ / OpenAI System Card = "no license"**. Cannot be cleanly relicensed to CC-BY-4.0 core. Excluded 2026-07-03 until per-question provenance is verified. |
| 14 | **WMDP-cyber** | HF: cais/wmdp | MIT | **Dual-use** weapons-proxy knowledge; upstream says benchmark data should never enter training corpora; rows are MCQ stems, not attack prompts. Excluded from a commercial-OK core 2026-07-03. |
| 15 | **Anthropic Persuasion** | HF: Anthropic/persuasion | CC-BY-NC-SA-4.0 | The `argument` column is persuasive prose, not an attack prompt. Out of red-team scope. |

## Pending — license unconfirmed, EXCLUDED from v0.1.0 (2 sources)

| # | Source | Upstream | API result | Action required |
|---|---|---|---|---|
| 16 | **MaliciousInstruct** | github: Princeton-SysML/Jailbreak_LLM | **(none)** — no SPDX license | Manually read repo/paper (Week 2). If no clear license → keep excluded. |
| 17 | **Korean UnSmile** | github: smilegate-ai/korean_unsmile_dataset | **(none)** — no SPDX license | Manually read repo/paper (Week 2). Was previously assumed CC-BY-SA-4.0 with no verified source. |

> **Total: 17 sources = 9 core + 3 extended + 3 excluded + 2 pending.**
> v0.1.0 ships **9 core + 3 extended = 12 sources** (71,429 prompts, measured
> 2026-07-03). Excluded: StrongREJECT (license), WMDP (dual-use), Persuasion
> (scope). Pending: MaliciousInstruct, Korean UnSmile (no SPDX license).
> Note: AdvBench/HarmBench are built from their **original GitHub CSVs**
> (llm-attacks / HarmBench); their HF mirrors are gated.

## Tier separation rationale

- **core (CC-BY-4.0 aggregation)** — every included source is verified
  permissive. NC data would contaminate the aggregate license and block
  commercial reuse (vendor guardrails, MLOps, paid evals), so NC is split out.
- **extended (separate distribution)** — non-commercial sources, distributed as
  a sibling HF dataset with clear NC labeling. Not co-mingled with core.
- **pending** — sources with no machine-readable license are **not shipped**.
  A "license-clean core" claim requires that every row has a confirmed
  redistribution right; unverified sources are excluded rather than assumed.

## Special handling notes

- **AART (CC-BY-4.0)** — kept in core (CC-BY-4.0 is compatible with the core
  aggregate license). Attribution preserved per-row.
- **WMDP-cyber (MIT + dual-use advisory)** — retained in core but DATASET_CARD
  and per-row provenance carry the cais/wmdp dual-use warning. Under review for
  whether a hazardous-knowledge subset belongs in a commercially-labeled tier
  (revisit at Week 2).
- **Anthropic Persuasion (CC-BY-NC-SA-4.0)** — the SA term propagates to
  derivatives within the extended tier; documented per-row.
- **No CC-BY-SA in core.** If any future source is CC-BY-SA, it goes to a
  dedicated SA-tier, never mixed into the CC-BY-4.0 core aggregate (SA is not
  one-way compatible with CC-BY-4.0).

## Attribution instructions

When redistributing subsets:

```
llm-redteam-corpus-taxonomy contributors. (2026-Q3).
LLM Red-Team Corpus + Taxonomy. Core tier under CC-BY-4.0, derived from 11
license-verified upstream sources (see data/core/sources.json for per-source
citations). DOI: (Zenodo DOI, Phase 1 Week 8)
```

Each upstream source retains its own citation — see `data/core/sources.json`
(generated Week 3-4) for the full per-source list.
