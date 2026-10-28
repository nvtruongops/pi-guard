# Datasets

This folder contains our released datasets. 

| File | Rows | Description |
|---|---|---|
| `dataset.csv` | ~31.2K | Raw matched candidates with ground-truth labels (`fp=0` being TPs), inclusion methods and position, structural attributes, content categories, popularity ranking and objective taxonomy. |
| `dataset_tp.csv` | ~15.3K | Validated true-positive subset of `dataset.csv`. Adds normalized text, lexical cluster IDs, MNLI prompting-strategy labels, and target agent tags. |
| `effectiveness.csv` | ~121K | Per-trial effectiveness outcomes for 13 models × 4 page representations × prompts. |
| `prompt_lifetime.csv` | ~9.7K | Wayback Machine persistence labels at 3 / 6 / 12 months per `(url, prompt_id)`. |
| `visibility.csv` | ~7.3K | Per-injection visibility verdict, contrast ratio, color, and various visibility features (e.g., `display:none`, `1px text spam`, `clip-path`); only for injections in HTTP body, as HTTP headers are hidden by construction. |
| `ui_position.csv` | 237 | Manually labeled UI region/position for a stratified sample. |


### 4.1 `dataset.csv` Schema


**Identifiers and provenance**

| Column | Type | Description |
|---|---|---|
| `row` | int | Original row index from the upstream pandas dump (kept for traceability; not semantic). |
| `data_source` | str | Source of discovery `commoncrawl`, `censys`, `shodan` |
| `jsonl_file` | str | Path of the JSONL shard (`/<dir>/<file>.jsonl`) the record was extracted from. |
| `jsonl_index` | float | Zero-based line index inside `jsonl_file` for the specific webpage. |
| `ID` | int | Stable per-injection identifier (joins to `prompt_lifetime.csv`, `visibility.csv`, `ui_position.csv` via `id`). |
| `origin` | str | host where the injection was observed. |
| `url` | str | Full URL where the injection was observed. |
| `pattern` | str | The lowercase indicator pattern (from `indicators/indicators.json`) that triggered the match. |
| `prompt` | str | The cleaned extracted injected instruction |
| `text` | str | Surrounding context window around the matched pattern. |

**Validation labels**

| Column | Type | Description |
|---|---|---|
| `fp` | str | False-positive label — `0` = true positive, `1` = false positive, `?` = unclear. (`dataset_tp.csv` keeps only `fp == 0`.) |

**Popularity / category signals**

| Column | Type | Description |
|---|---|---|
| `tranco_ranking` | str | Tranco rank for the host, or `unknown` if not listed. |
| `crux_ranking` | str | Chrome UX Report popularity bucket (e.g., `1000`, `5000`, `1000000`, `>1,000,000`). |
| `chrome_topics` | str | Space/period-prefixed Chrome Topics-API category labels assigned to the host (e.g., `103. Business and industrial 227. Education`). |

**Inclusion / position features**

| Column | Type | Description |
|---|---|---|
| `inclusion` | str | How the injection is embedded — values include `x-ai`, `X-AI-Licence`, other AI-specific HTTP headers, `html_tag:<tag>` (e.g., `html_tag:p`, `html_tag:a`, `html_tag:b`), `html_comment`, `js_line_comment`, `json`, etc. |
| `position` | str | High-level location: `http_header` or `http_body`. |
| `display_none` | bool | Element (or an ancestor) carries `display: none`. |
| `background_color` | bool | Element has a CSS-set background color. |
| `color_css` | bool | Element has a CSS-set foreground color. |
| `font_size` | int | Tiny-font heuristic. |
| `color_prop` | int | Boolean flag for a `color` property usage. |
| `font_prop` | int | Boolean flag for a `font` property usage (e.g., zero-size font). |
| `json_ld` | int | `1` if the injection sits inside a `<script type="application/ld+json">` block. |

**Locale / network attribution**

| Column | Type | Description |
|---|---|---|
| `lang_tld` | str | Country inferred from the host's TLD (e.g., `US`, `DE`, `JP`). |
| `lang_html` | str | Language declared on the page via `<html lang="…">` (e.g., `en`, `de-DE`, `es`). |
| `cc_tld` | str | Country code derived directly from the TLD itself (e.g., `DE`, `JP`, `WS`). |
| `asn` | float | Autonomous System Number that hosts the page. |
| `asn_org` | str | Human-readable ASN owner (e.g., `Cloudflare, Inc.`, `Akamai Connected Cloud`). |

**Objective taxonomy (multi-label, `0`/`1`/NaN)**

Each column below is a binary indicator for one objective category from the paper's taxonomy. NaN means the row was not annotated for that label.

| Column | Description |
|---|---|
| `AI Bot Identification (human verification)` | Page tries to use the prompt to identify or fingerprint AI bots (CAPTCHA-style trick). |
| `Content & Reputation Manipulation\|Citation Forcing` | Forces the model to cite a particular source. |
| `Content & Reputation Manipulation\|Content / Product Promotion` | Forces promotion of a product or piece of content. |
| `Content & Reputation Manipulation\|Personal Job Candidate Promotion` | Pushes the model to recommend a specific job candidate (CVs, profile pages). |
| `Content & Reputation Manipulation\|Positive Review Forcing` | Forces a favorable review. |
| `Content & Reputation Manipulation\|SEO / Backlink Injection` | Inserts SEO/backlink instructions. |
| `Data Exfiltration\|Leak System Prompt` | Asks the model to reveal its system prompt. |
| `Data Exfiltration\|Leak Secret` | Asks the model to leak credentials, secrets, or other sensitive data. |
| `Data Protection\|social_media_bots` | Second-order prompt injection potential for social-media scraping bots. |
| `Data Protection\|non_personal_pages` | Prompt injection on on non-personal (institutional/business) pages. |
| `Data Protection\|personal_pages` | Prompt injection on personal pages (blogs, portfolios). |
| `General Instruction Manipulation` | Generic instruction override that does not fit any narrower category (underspecified). |
| `System Disruption / Degradation\|Command Injection` | Embeds shell/OS-style commands (e.g., `sudo telinit 0`). |
| `System Disruption / Degradation\|Constraint Removal` | Forces the model to drop safety/ethical constraints. |
| `System Disruption / Degradation\|Garbage Injection (Corruption)` | Injects junk to corrupt downstream model outputs. |
| `System Disruption / Degradation\|Model Self-Modification` | Asks the model to modify its own behavior or weights/training data. |
| `honeypot` | Page is a deliberate honeypot designed to trap or fingerprint AI agents. |


### 4.2 `dataset_tp.csv` — Schema

True-positive subset of `dataset.csv` (`fp == 0`) enriched with downstream analysis labels. **All columns from §4.1 are retained**, and the following columns are added:

**Normalization and clustering**

| Column | Type | Description |
|---|---|---|
| `normalized` | str | Normalized prompt text used for clustering (lowercased, punctuation stripped, numbers replaced with `<NUM>`). |
| `lexical_cluster` | int | Cluster ID from token-similarity (Jaccard ≥ 0.75) |
| `embedding_cluster` | int | Cluster ID from sentence-transformer + DBSCAN clustering. |

**Prompting-strategy labels (zero-shot MNLI with `facebook/bart-large-mnli`)**

| Column | Type | Description |
|---|---|---|
| `mnli_task_override` | int | The prompt tries to override or ignore previous instructions. |
| `mnli_conditional_logic_trigger` | int | The prompt uses conditional phrasing (e.g., "if you are an AI") to escape constraints. |
| `mnli_authority_pressure` | int | The prompt uses urgency or authority to force compliance. |
| `mnli_role_playing` | int | The prompt asks the model to act as a character or assume a role. |
| `mnli_identity_rewrite` | int | The prompt attempts to change the model's identity (e.g., "you are not an AI anymore"). |
| `mnli_jailbreak_mode` | int | The prompt enables unrestricted or "developer mode" behavior. |
| `mnli_content_injection` | int | The prompt forces inclusion of specific phrases or content in the output. |
| `mnli_forced_output_format` | int | The prompt restricts the format, language, or style of the output. |


**Hosting context**

| Column | Type | Description |
|---|---|---|
| `user_interactions` | int | `1` if the injection sits inside user-interactions content like comments. |
| `third_party_platform_hosted` | int | `1` if the page is hosted on a third-party platform (e.g., job listings, etc). |
| `first_party_content` | int | `1` if the injection is part of the site owner's own content. |

**Targeted-agent flags (multi-label)**

| Column | Type | Description |
|---|---|---|
| `agents_DS` | int | Targets data-scraping / data-collection agents. |
| `agents_SE` | int | Targets search-engine / SEO agents. |
| `agents_CS` | int | Targets customer-service / chat agents. |
| `agents_HR` | int | Targets HR / recruiting / candidate-screening agents. |
| `agents_TE` | int | Targets technical / engineering / coding agents. |


### 4.3 `effectiveness.csv` — Schema

One row per LLM trial. The grid is 13 models × 4 page representations × prompts (≈121K rows total).

| Column | Type | Description |
|---|---|---|
| `model_name` | str | Model identifier as queried (e.g., `qwen3.5-35B`, `Deepseek-v3.2`, `OpenAI: GPT-5.4`, `seed-2.0-mini`). |
| `model_category` | str | One of `Small (up to 8B)`, `Medium (from 8 to 70B)`, `Large (more than 70B)`, `Unknown/Closed source`. |
| `page_representation` | str | One of `HTML`, `Text`, `raw` (HTTP `{headers, body}` JSON), `snapshot` (Playwright `snapshotForAI` accessibility tree). |
| `prompt` | str | The exact injected prompt the trial was conditioned on. |
| `raw_from_llm` | str | Verbatim model response. |
| `is_effective` | int | `1` if the response shows the injection succeeded (the model followed the injected instruction). |
| `has_error` | int | `1` if the API/model errored or returned an unparseable response. |
| `detect_injection_attempt` | int | `1` if the model explicitly acknowledged / refused / flagged an injection attempt. |

`is_effective`, `has_error`, and `detect_injection_attempt` are **not mutually exclusive** — see the outcome-overlap table emitted by `data_analysis/effectiveness.ipynb`.


### 4.4 `prompt_lifetime.csv` — Schema

One row per `(url, prompt_id)` measured against the Wayback Machine.

| Column | Type | Description |
|---|---|---|
| `url` | str | Webpage URL the prompt was originally observed on. |
| `prompt_id` | str | Underscore-joined list of `ID`s (from `dataset.csv`) for prompts found at that URL. |
| `3M` | float | `1` if the same prompt is still present in the closest archive snapshot ~3 months earlier; `0` if absent; NaN if no snapshot available. |
| `6M` | float | Same as `3M`, ~6 months earlier. |
| `12M` | float | Same as `3M`, ~12 months earlier. |


### 4.5 `ui_position.csv` — Schema

Manually labeled UI position for a stratified sample of 237 injections.

| Column | Type | Description |
|---|---|---|
| `url` | str | URL of the page that was inspected. |
| `is_human_visible` | int | `1` if a human reader can see the prompt without DOM inspection / view-source. |
| `region` | str | Page region: `header`, `body`, `sidebar`, or `footer`. |
| `pos` | str | Free-text position within the region (e.g., `top left`, `center`, `top, center`, `center, left`). |


### 4.6 `visibility.csv` — Schema

Output of the Playwright/Chromium visibility analyzer (`visibility_analysis/`). One row per injection in HTTP body (HTTP-header injections are hidden by construction and excluded).

**Identification**

| Column | Type | Description |
|---|---|---|
| `id` | int | Injection identifier — joins to `dataset.csv.ID`. |
| `url` | str | URL probed by Playwright. |

**Verdict**

| Column | Type | Description |
|---|---|---|
| `is_visible` | int | `1` if the injection was rendered visibly to a human (no hiding heuristic triggered, contrast OK, text found). |
| `text not found` | int | `1` if the matched text could not be located in the live DOM. |
| `has_error` | int | `1` if Playwright errored while loading or analyzing the page. |
| `error_description` | str | Stringified error object (e.g., `{'name': 'TimeoutError'}`, `{'name': 'Error'}`) or `0` if none. |

**Color / contrast**

| Column | Type | Description |
|---|---|---|
| `text_color` | str | Computed text color in `rgb(...)` / `rgba(...)` notation. |
| `bg_color` | str | Computed background color. |
| `contrast_ratio` | float | WCAG contrast ratio between text and background. |
| `low contrast` | int | `1` if contrast falls below the WCAG-AA readability threshold. |

**Hiding methods (15 binary flags)**

| Column | Description |
|---|---|
| `display:none` | Element (or ancestor) sets `display: none`. |
| `visibility:hidden` | Element sets `visibility: hidden`. |
| `opacity:0` | Element has `opacity: 0`. |
| `1px text spam` | Font size collapses to ~1px (classic hidden-keyword trick). |
| `color:transparent` | Foreground color is transparent. |
| `text-indent negative (hidden text)` | Large negative `text-indent` pushes text off-screen. |
| `offscreen positioning (large negative offset)` | Element absolutely positioned far off-screen. |
| `clip property hiding text` | Legacy `clip: rect(...)` hides the element. |
| `clip-path hiding text` | `clip-path` hides the element. |
| `zero-size element` | Element has zero width/height. |
| `outside viewport` | Element is rendered outside the viewport. |
| `covered by another element` | Element is fully occluded by an overlay. |
| `z-index trap (sent behind layers)` | Element is sent behind other layers via `z-index`. |
| `same color text/background` | Text color equals background color. |
