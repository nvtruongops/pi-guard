# Methodology

> **Status:** draft — full version issued with v0.1.0 (Phase 1 Week 7).
>
> **Authoritative figures (2026-07-03):** for the current source count, row
> counts, tiers, and licenses, see [`README.md`](README.md),
> [`CHANGELOG.md`](CHANGELOG.md), and [`docs/license_matrix.md`](docs/license_matrix.md).
> v0.1.0 = **12 sources** (9 core / 3 extended), **71,429 prompts**. Some legacy
> estimates in this draft (e.g. "~95K", older source lists, "Korean subset")
> predate the build and are superseded; `provenance` fields are
> `{source_url, source_citation}`. This doc is rewritten in full at Week 7.

## Overview

`llm-redteam-corpus-taxonomy` unifies publicly sourced red-team and safety
datasets into a canonical schema with deduplication, license-aware splitting,
and cross-framework taxonomy hints.

Every choice below is optimized for **reproducibility** — any researcher
should be able to reconstruct the release from public sources using scripts
in this repository.

## Pipeline

```
[17 upstream sources — 15 shipped in v0.1.0, 2 pending license verification]
    ↓  (scripts/import_all.py — per-source downloader)
data/raw/{source_id}/*.jsonl        # SHA-256 recorded
    ↓  (scripts/build_corpus.py --stage canonicalize)
Canonical schema v1.0
    ↓  (--stage dedup)
Exact-hash dedup (prompt_normalized)
    ↓  (--stage tier-split)
core (~95K) | extended (~34K)
    ↓  (--stage build-distributions)
canonical.parquet + canonical.jsonl.gz + canonical.duckdb + manifest.json
```

## Canonical schema (v1.0)

See `DATASET_CARD.md` for full schema. Design decisions:

- **`prompt`** kept unchanged from source (verbatim reproduction).
- **`prompt_normalized`** used only for dedup (lowercase + whitespace collapse).
- **`exact_hash`** = SHA-256 of `prompt_normalized` — enables near-identical
  detection while preserving casing/whitespace in `prompt`.
- **`taxonomy_hints`** — per-source annotations copied from upstream where
  available; not authoritative. Cross-framework mapping added in Phase 2.
- **`provenance`** — verbatim source citation, license, URL, import timestamp.

## License tier decision

Each upstream dataset assigned to a tier by license type:

| Upstream license | Tier |
|---|---|
| MIT | `core` |
| Apache-2.0 | `core` |
| CC-BY-4.0 | `core` (attribution preserved) |
| CC-BY-NC-4.0 | `extended` |
| CC-BY-NC-SA-4.0 | `extended` (ShareAlike propagates to the tier) |

**No CC-BY-SA in core.** ShareAlike is not one-way compatible with the CC-BY-4.0
core aggregate, so any SA source would need its own SA-tier (none in v0.1.0).

Rationale: `core` is a genuinely commercially usable aggregation. `extended`
is provided as a separate distribution so users can opt in with awareness of
NC constraints.

Full per-source table: `docs/license_matrix.md`.

## Dedup

**Stage 1 — Exact hash (v0.1.0):**
Group by `exact_hash`; select representative by source priority:

```python
_SOURCE_PRIORITY = [
    "harmbench",       # curated + well-tested
    "advbench",        # foundational
    "jailbreakbench",  # standardized benchmark
    "anthropic_hh_redteam",
    # ... (see scripts/build_corpus.py for full order)
]
```

Priority is by source curation quality — highest-quality source becomes the
canonical row, others become "linked" duplicates in `sources.json`.

**Stage 2 — Near-dup (v0.2.0+):**
Embedding-based cosine similarity for future release (out of scope for v0.1.0).

## Language classification

`langdetect` (heuristic) applied to `prompt`. Categorized as:
`en`, `ko`, `ja`, `zh`, or `other`.

Manual verification: first 100 rows per language spot-checked. Non-English
detection accuracy expected to be ~95% on this corpus size.

## Reproducibility

```bash
git clone https://github.com/rubyglask/llm-redteam-corpus-taxonomy
cd llm-redteam-corpus-taxonomy
python -m venv .venv && source .venv/bin/activate
pip install -e .[dev]

# rebuild from raw sources
python scripts/import_all.py               # downloads all shipped sources → data/raw/
python scripts/build_corpus.py --tier core       --out data/core/
python scripts/build_corpus.py --tier extended   --out data/extended/

# verify against release checksums
bash scripts/verify_checksums.sh
```

Each release version is tagged in git (`v0.1.0`, `v2026.Q3`, …) and pinned
to specific upstream commit SHAs / dataset versions where the source supports
versioning.

## Ethical process

Dataset construction follows the practices in:

- Mitchell et al., 2019 — Model Cards for Model Reporting.
- Gebru et al., 2018 — Datasheets for Datasets.
- Bommasani et al., 2021 — Foundation models & responsible release.

Each release ships with:
- Full license matrix (`docs/license_matrix.md`)
- Provenance for every row (verbatim upstream citation)
- Dual-use advisory (`DATASET_CARD.md` ethical section)
- Quarterly changelog paper documenting additions/removals

## Limitations

Explicitly acknowledged (non-exhaustive):

1. **Language coverage** — English-dominant. Korean subset present; other
   Asian languages limited.
2. **Taxonomy hints are per-source**, not adjudicated. Authoritative
   cross-framework mapping ships in Phase 2.
3. **Adversarial prompt shelf-life** — attacks that worked in 2023-2024 may
   already be patched. Recency ≠ effectiveness.
4. **Source bias** — upstream selection biased toward English-language
   academic red-team literature.

## Change log

- **2026-Q3** — v0.1.0-dev — initial pipeline established, scaffolding, docs.
- (future) 2026-Q3 end — v0.1.0 first public release.
