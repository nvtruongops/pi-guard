# A License-Clean, Deduplicated Corpus and Cross-Framework Taxonomy for LLM Red-Teaming

> **Preprint draft — v0.1 (2026-07-03).** Target: arXiv `cs.CR` + `cs.CL`.
> Author identity, Zenodo DOI, and arXiv id are filled at submission (Phase 1
> Week 8). Numbers below are measured from the v0.1.0 build and match the
> published datasets and `CHANGELOG.md`. This is a working draft to refine, not
> a final manuscript.

**Author:** rubyglask (see note on author identity before submission)

---

## Abstract

Red-team and safety datasets for large language models (LLMs) are scattered
across many repositories, use incompatible formats, and carry a mix of licenses
that makes lawful reuse — especially in commercial safety tooling — difficult.
We present a unified corpus of **71,429** adversarial prompts aggregated from
**12 public sources**, split by verified license into a commercially usable
**core** tier (44,681 prompts, CC-BY-4.0) and a non-commercial **extended** tier
(26,748 prompts). Every prompt retains its source, license, and citation; phone
numbers and street addresses are masked; and the build is deterministic and
checksum-verified. We deliberately exclude three sources for licensing,
dual-use, and scope reasons, and we document this. Alongside the corpus we
release a v0.1 **cross-framework taxonomy** anchoring the OWASP LLM Top 10 (2025)
to the NIST AI RMF, MITRE ATLAS, and the EU AI Act, with per-mapping confidence
labels. We discuss the corpus's main limitation — 83% of the core tier is a
single source (HH-RLHF red-team) whose first turns are not all adversarial — and
position the contribution as *clean aggregation + crosswalk*, not novel data.

## 1. Introduction

Practitioners who build or evaluate LLM guardrails repeatedly re-solve the same
plumbing: find the relevant red-team benchmarks, download each, reconcile
formats, and hope the licenses permit their use. The datasets themselves are
valuable and well-cited; what is missing is a **clean, unified, license-aware**
starting point, and a **mapping** from prompts to the compliance frameworks
teams must answer to (OWASP LLM Top 10, NIST AI RMF, EU AI Act, ...).

This work contributes:

1. A **deduplicated, provenance-tracked** corpus of 71,429 prompts from 12
   public sources, in Parquet / JSONL / DuckDB, loadable in one line.
2. A **license-clean core tier** (CC-BY-4.0) usable in commercial safety
   products, kept separate from a non-commercial extended tier.
3. A reproducible, deterministic **build pipeline** with per-file checksums.
4. A v0.1 **cross-framework taxonomy** with explicit confidence labels.

We do **not** claim novel prompts or the largest set; individual sources are
larger. Our claim is that *clean aggregation + crosswalk* is itself useful and,
today, absent.

## 2. Related Work

Individual red-team / safety datasets — AdvBench, HarmBench, JailbreakBench,
HarmfulQA, Do-Not-Answer, AART, the HH-RLHF red-team split, BeaverTails, ALERT,
ToxicChat, and others — each target a slice of the problem. Prior *aggregations*
exist but typically mix licenses and do not provide a compliance crosswalk. The
OWASP LLM Top 10, NIST AI RMF, MITRE ATLAS, and EU AI Act define the governance
vocabulary; to our knowledge no public artifact maps a prompt corpus onto all of
them.

## 3. Corpus Construction

**Sources.** 12 shipped sources (9 core, 3 extended). Three further sources are
excluded: StrongREJECT (its README shows it bundles questions from no-license
upstreams, so it cannot be relicensed to a CC-BY-4.0 core cleanly), WMDP-cyber
(dual-use weapons-proxy knowledge whose upstream forbids training-corpus
inclusion), and Anthropic Persuasion (persuasive essays, not attack prompts).
Two more are pending license verification (MaliciousInstruct, Korean UnSmile).

**License verification.** Each source's license was fetched live from the HF Hub
or GitHub API and recorded in `docs/license_matrix.md`. Sources with no
machine-readable license are not shipped.

**Schema.** Each row carries `prompt`, a normalized form, a SHA-256 `exact_hash`,
`language`, `source_id`, `source_original_id`, `source_license`, `license_tier`,
a `taxonomy_hints` field (filled in Phase 2), and `provenance`.

**PII.** Phone numbers and street addresses (e.g. in doxxing-style prompts) are
masked with `[PHONE]` / `[ADDRESS]` (33 rows). Named-person mentions may remain.

**Deduplication.** Exact-hash dedup on the normalized prompt: core −4.2%,
extended −43.1% (driven by BeaverTails answer-rows collapsing to prompts),
−23.2% globally. Near-duplicate detection is future work.

**Reproducibility.** Deterministic outputs (fixed row order, gzip mtime=0) and
per-file SHA-256 in a manifest let anyone reconstruct and verify a release.

## 4. Statistics

| Tier | Rows | Sources | License |
|---|---|---|---|
| core | 44,681 | 9 | CC-BY-4.0 |
| extended | 26,748 | 3 | CC-BY-NC-SA-4.0 |

Core is **83% HH-RLHF red-team** (37,155 rows; first human turn of each
transcript). The remaining 8 core sources contribute 7,526 curated single-turn
prompts. Largest extended source: ALERT (14,032). Language is ~99.99% English.

## 5. Cross-Framework Taxonomy (v0.1)

We anchor on the OWASP LLM Top 10 (2025) and map each item to NIST AI RMF
functions (high confidence), MITRE ATLAS tactics (high) and candidate technique
ids (to verify), and EU AI Act articles (coarse). Each mapping carries a
`confidence` label; nothing is presented as authoritative. A source→OWASP map
records that all sources primarily exercise LLM01 (Prompt Injection / jailbreak),
with documented secondary harms where applicable. Per-prompt classification to
fill `taxonomy_hints` is future work.

## 6. Ethical Considerations and Dual-Use

The corpus aggregates prompts already public in research and industry. It is
intended for defensive use: building guardrails, benchmarking safety, and
reproducing red-team research. We exclude the WMDP dual-use subset from the
commercial tier, mask PII, and document responsible-use expectations. Releasing
adversarial prompts carries risk; we judge the aggregate risk low because all
content is already public, and we mitigate the specific risks we found (PII,
dual-use knowledge, license contamination).

## 7. Limitations

- **Single-source dominance.** 83% of core is HH-RLHF; its first turns include
  benign openers, so "44,681 adversarial prompts" overstates adversarial density
  for that subset. Users wanting curated single-turn attacks can filter it out
  (7,526 rows remain).
- **Aggregation, not novel data.** Individual sources are independently citable
  and larger; our value is cleanliness and the crosswalk.
- **Exact-hash dedup only.** Near-duplicate variants remain.
- **Taxonomy is v0.1.** Confidence-tagged; ATLAS technique ids and the other
  frameworks need expert review.
- **English-dominant.** Non-English coverage is minimal.

## 8. Availability

- Datasets: `rubyglask/llm-redteam-corpus-taxonomy-{core,extended}` (Hugging Face)
- Code + build pipeline: github.com/rubyglask/llm-redteam-corpus-taxonomy
- Zenodo DOI: _to be issued_

## Author identity note (remove before submission)

The public dataset/GitHub use the handle `rubyglask` for privacy. For citation
attribution (and any immigration-evidence use), consider submitting the arXiv
preprint and Zenodo record under the real legal name, while keeping the handle
on the repos. Decide at submission time.
