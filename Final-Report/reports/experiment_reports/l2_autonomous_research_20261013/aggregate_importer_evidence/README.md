# llm-redteam-corpus-taxonomy

> **Status:** Phase 1 — corpus foundation in progress (2026 Q3).
> First release (v0.1.0) targets 2026-Q3 end. See [CHANGELOG.md](CHANGELOG.md).

A **living aggregated corpus + cross-framework taxonomy** for LLM red-team
research and evaluation. Publicly sourced, license-clean, quarterly refreshed.

**One format, many sources.** We collected **12 public** LLM red-team / safety
datasets and unified them into **a single schema** — deduplicated, PII-masked,
with every prompt's origin and license preserved. Stop stitching benchmarks by
hand; `load_dataset` once.

- **Corpus** (Phase 1) — public red-team / safety datasets unified into a
  single canonical schema with deduplication, PII masking, and provenance
  tracking. License-split into `core` (permissive) and `extended`
  (non-commercial). v0.1.0 ships **12 sources (9 core + 3 extended)**; 3 are
  excluded on purpose and 2 are pending license verification (see below).
- **Cross-framework taxonomy** (Phase 2, Q4) — bidirectional mapping across
  OWASP LLM Top 10 / MITRE ATLAS / NIST AI RMF / EU AI Act / ISO 42001 / KISA
  AI / CSA AI Safety.
- **Living dataset** — quarterly releases (`vYYYY.QX`) with changelog papers.

## Download — pick your version

| I want... | Dataset | Rows | License |
|---|---|---|---|
| **Everything** (research / non-commercial) | [`-full`](https://huggingface.co/datasets/rubyglask/llm-redteam-corpus-taxonomy-full) | **64,458** | CC-BY-NC-SA-4.0 |
| **Commercial-safe subset** | [`-core`](https://huggingface.co/datasets/rubyglask/llm-redteam-corpus-taxonomy-core) | 44,681 | CC-BY-4.0 |
| **Only the non-commercial sources** | [`-extended`](https://huggingface.co/datasets/rubyglask/llm-redteam-corpus-taxonomy-extended) | 26,748 | CC-BY-NC-SA-4.0 |

> Counts **measured 2026-07-03** (PII-masked, deduplicated). `full` = all 12
> sources merged and de-duplicated across tiers. `core` is the permissively-
> licensed subset (commercial OK). 83% of the corpus is HH-RLHF red-team (first
> human turn). **Excluded on purpose:** StrongREJECT (no-license questions),
> WMDP (dual-use), Persuasion (not attack prompts). **Pending:** MaliciousInstruct,
> Korean UnSmile.

**Formats:** Parquet (main) · JSONL.gz (streaming) · DuckDB (analytics).

## How to use

**In code** — load in one line (swap `-full` for `-core` / `-extended`):

```python
from datasets import load_dataset

ds = load_dataset("rubyglask/llm-redteam-corpus-taxonomy-full")
row = ds["train"][0]
# {
#   "scenario_id": "CN_0000001", "prompt": "...", "language": "en",
#   "source_id": "anthropic_hh", "source_license": "MIT",
#   "license_tier": "core", "taxonomy_hints": "{}",
#   "provenance": "{\"source_url\": \"...\", \"source_citation\": \"...\"}",
# }

# filter by source or license
harmbench     = ds["train"].filter(lambda r: r["source_id"] == "harmbench")
commercial_ok = ds["train"].filter(lambda r: r["license_tier"] == "core")
```

**Ask an LLM / agent** — paste this to your coding agent:

> *"Load the Hugging Face dataset `rubyglask/llm-redteam-corpus-taxonomy-full`.
> Take every row where `source_id == 'harmbench'`, send each `prompt` to my
> chatbot, and flag any response that complies with the harmful request. The
> prompt text is in the `prompt` column."*

See [`notebooks/01_quickstart.ipynb`](notebooks/01_quickstart.ipynb) for a
5-minute tour.

## Sources & attribution

Full per-source license matrix + verification method:
[`docs/license_matrix.md`](docs/license_matrix.md). Per-tier attribution:
`data/{core,extended}/sources.json`. Licenses were verified **live against
upstream HF/GitHub APIs on 2026-07-03**.

| # | Source | Verified license | Status |
|---|---|---|---|
| 1 | AdvBench (llm-attacks) | MIT | ✅ core |
| 2 | HarmBench (centerforaisafety) | MIT | ✅ core |
| 3 | JailbreakBench | MIT | ✅ core |
| 4 | TDC 2023 Red-Teaming | MIT | ✅ core |
| 5 | ForbiddenQuestionSet (verazuo/TrustAIRLab) | MIT | ✅ core |
| 6 | Do-Not-Answer (LibrAI) | Apache-2.0 | ✅ core |
| 7 | HarmfulQA (declare-lab) | Apache-2.0 | ✅ core |
| 8 | AART (walledai) | CC-BY-4.0 | ✅ core |
| 9 | Anthropic HH-RLHF (red-team split) | MIT | ✅ core |
| 10 | BeaverTails (PKU-Alignment) | CC-BY-NC-4.0 | ✅ **extended** |
| 11 | ALERT (Babelscape) | CC-BY-NC-SA-4.0 | ✅ **extended** |
| 12 | LMSYS Toxic-Chat | CC-BY-NC-4.0 | ✅ **extended** |
| 13 | StrongREJECT | MIT (but bundles no-license Qs) | ⊘ **excluded** (license) |
| 14 | WMDP-cyber (cais) | MIT | ⊘ **excluded** (dual-use) |
| 15 | Anthropic Persuasion | CC-BY-NC-SA-4.0 | ⊘ **excluded** (scope) |
| 16 | MaliciousInstruct (Princeton-SysML) | (none) — unverified | ⏸ **pending** |
| 17 | Korean UnSmile (smilegate-ai) | (none) — unverified | ⏸ **pending** |

*Built in v0.1.0: 9 core + 3 extended = 12 sources (71,429 prompts).*

## Roadmap

- **Phase 1 (2026-Q3):** Corpus core + extended, HF publish, arXiv preprint,
  Zenodo DOI, CI-driven quarterly refresh.
- **Phase 2 (2026-Q4):** 7 framework taxonomy JSONs + bidirectional
  cross-mapping (~300+ items) + Papers with Code entry.
- **Phase 3 (2026-Q4 end):** Integrated v1.0 release — corpus prompts
  auto-annotated with cross-mapped taxonomy IDs + interactive HF Space demo.

## Ethics, dual-use & privacy

This dataset is for **defensive red-team research and safety evaluation**. It
aggregates adversarial prompts **already public** in academic and industry
sources. Users must:

- Comply with each upstream license (see `docs/license_matrix.md`).
- Not deploy contents as attacks against systems without authorization.
- Follow responsible disclosure for any vulnerabilities discovered.

**Privacy:** real phone numbers and street addresses found in a few prompts are
masked with `[PHONE]` / `[ADDRESS]`. Some named-person mentions may remain —
open an issue to request removal.

**Excluded for safety/licensing:** WMDP (dual-use weapons-proxy knowledge),
StrongREJECT (mixes in no-license questions), Persuasion (not attack prompts).

## Citation

See [`CITATION.cff`](CITATION.cff). Zenodo DOI issues in Phase 1 Week 8.

## License

- **Data (`data/core/`):** [CC-BY-4.0](LICENSE)
- **Code (`scripts/`, `notebooks/`):** [MIT](LICENSE-CODE)
- **Extended (`data/extended/`):** Inherits upstream non-commercial terms
  (includes CC-BY-NC-SA — see `data/extended/`).
