# In-Page Prompt Injection in the Wild — Artifact

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow?logo=javascript)
![Playwright](https://img.shields.io/badge/Playwright-Testing-green?logo=playwright)


This repository contains the artifacts for our paper **"A Large-scale Measurement of In-Page Prompt Injections Against LLM Web Agents"**. It contains both data and code needed to reproduce measurements reported in the paper.

**Overview:** We construct a comprehensive dataset by analyzing 1.2 billion URLs across 24.8 million hosts**, identify 15.3K validated in-page prompt-injections spanning 11.7K webpages.

We characterize in-page prompt injections along the following dimensions:

- prevalence and structure
- stakeholders and objectives
- targeted agents
- delivery mechanisms (e.g., position, inclusion method, etc)
- temporal persistence
- Effectiveness


**Datasets:** See the details [here](./data/README.md)

**Paper:** See [here](https://arxiv.org/abs/2604.27202)

**Licence Notice:** We release a sanitized public dataset under CC BY 4.0, while the accompanying software and analysis code are released under AGPL-3.0. The full dataset containing URLs, domains, and other identifying metadata is available only to approved applicants under additional confidentiality and data-use conditions subject to signing a DUA [here](https://docs.google.com/forms/d/e/1FAIpQLSe1td1xhGtm8-Svv-RlhHd7Gxgp1ma9t9WOAmp05L4F_C4x3w/viewform).

---

## 1. Repository Layout

```
prompt_injection_artifact/
├── data/                      # Released datasets (CSV)
├── indicators/                # Prompt-injection search patterns
├── data_collection/           # Web-scale collection (CommonCrawl, Censys, Shodan)
├── feature_extraction/        # Context extraction + structural features
├── visibility_analysis/       # Visibility analysis pipeline with Playwright
├── lifetime_analysis/         # Temporal persistence analysis with Internet-Archive
├── ranking/                   # Tranco / CrUX rank lookup
├── effectiveness/             # Effectiveness evaluation on LLMs
├── data_analysis/             # Jupyter notebooks (clustering, NLI, analyses)
├── settings.py                # Central configuration (paths, env vars)
└── .env.example               # Env template for API keys
```

---

## 2. Installation

```bash
# Python (tested with 3.11)
pip install -r requirements.txt

# Playwright (required for visibility + snapshot generation)
pip install playwright
playwright install chromium

# Node (required for visibility_analysis/index.js)
cd visibility_analysis && npm install
```

Copy `.env.example` to `.env` and fill in any API credentials, such as Shodan and Censys.

---

## 3. Pipeline Overview

The artifact is organized as a linear pipeline. Each stage's outputs feed the next.

```
indicators/  →  data_collection/  →  feature_extraction/  →  visibility_analysis/
                                                          →  lifetime_analysis/
                                                          →  ranking/
                                                          →  effectiveness/
                                                          →  data_analysis/
```

---

## 4. Datasets ([`data/`](./data))

All released datasets are CSV and indexed by per-instance `ID` and per-page `url`/`origin`.

| File | Rows | Description |
|---|---|---|
| `dataset.csv` | ~31.2K | Raw matched candidates with ground-truth labels (`fp=0` being TPs), inclusion methods and position, structural attributes, content categories, popularity ranking and objective taxonomy. |
| `dataset_tp.csv` | ~15.3K | Validated true-positive subset of `dataset.csv`. Adds normalized text, lexical cluster IDs, MNLI prompting-strategy labels, and target agent tags. |
| `effectiveness.csv` | ~121K | Per-trial effectiveness outcomes for 13 models × 4 page representations × prompts. |
| `prompt_lifetime.csv` | ~9.7K | Wayback Machine persistence labels at 3 / 6 / 12 months per `(url, prompt_id)`. |
| `visibility.csv` | ~7.3K | Per-injection visibility verdict, contrast ratio, color, and various visibility features (e.g., `display:none`, `1px text spam`, `clip-path`); only for injections in HTTP body, as HTTP headers are hidden by construction. |
| `ui_position.csv` | 237 | Manually labeled UI region/position for a stratified sample. |


---

## 5. Indicators ([`indicators/`](./indicators))

`indicators.json` contains the curated prompt-injection patterns used for web-scale matching.

`generate.py` programmatically expands various prompt templates over a dictionary of substitution values (verbs, identities, restriction types, ...). It writes the deduplicated cartesian product to `indicators/indicators.json`.

```bash
python -m indicators.generate
```

---

## 6. Data Collection ([`data_collection/`](./data_collection))

Collects in-the-wild webpage snapshots and searches them for the indicator patterns using
Aho–Corasick automata. All collectors write JSON/JSONL under `outputs/<source>/`.

| Script | Purpose |
|---|---|
| `commoncrawl.py` | Stream the configured CommonCrawl release (default `CC-MAIN-2025-43`), extract `(url, headers, body)` from response records, and shard them into JSONL files (1K records/file, 100 files/dir). |
| `commoncrawl_search.py` | Aho–Corasick scan over the collected JSONL with thread-pooled workers; emits `commoncrawl_matches.json`. |
| `commoncrawl_celery.py` | Distributed variant of `commoncrawl.py`. Implements WARC sharding (`--shard_index`/`--total_shards`), checkpointed resumption, and submits search jobs to Celery. |
| `commoncrawl_celery_search_task.py` | Celery task definitions for parallel pattern search; persists progress in `search_task_tracker.json` (completed / failed / pending files, total matches). |
| `celery_config.py` | Celery app + Redis broker/back-end configuration (queues, retry policy, JSON serializer). |
| `censys_search.py` | Queries the Censys Global Search v3 API for indicators|
| `shodan_search.py` | Queries the Shodan host search API for indicators |

Run examples:

```bash
# CommonCrawl single-host
python -m data_collection.commoncrawl
python -m data_collection.commoncrawl_search

# CommonCrawl distributed (one shell per shard, plus celery workers)
python -m data_collection.commoncrawl_celery --shard_index 0 --total_shards 14

# Censys / Shodan
python -m data_collection.censys_search --api_key $CENSYS_API_KEY --org_id $CENSYS_ORG_ID
python -m data_collection.shodan_search  --api_key $SHODAN_API_KEY
```

---

## 7. Feature Extraction ([`feature_extraction/`](./feature_extraction/))

Turns raw matches into the per-injection feature rows that populate `data/dataset.csv`.

| Script | Purpose |
|---|---|
| `commoncrawl_extract_context.py` | Walks every CommonCrawl JSONL match, slices a context window around the matched pattern, and records position (header vs. body), URL, and host. |
| `censys_extract_context.py` | Same context-window extraction for Censys results |
| `shodan_extract_context.py` | Same context-window extraction for Shodan results |
| `extract_features.py` | Computes the structural feature set: position, presence of AI-specific HTTP headers (`x-chatgpt`, `x-ai`, ...), surrounding HTML tag and context, CSS properties. |
| `deduplicate_df.py` | CLI helper that drops duplicate rows from any extracted-context CSV. |

```bash
python -m feature_extraction.commoncrawl_extract_context
python -m feature_extraction.extract_features --input_file outputs/contexts.csv \
                                              --out_file   outputs/features.csv
python feature_extraction/deduplicate_df.py -i outputs/features.csv -o outputs/features_unique.csv
```

---

## 8. Visibility Analysis ([`visibility_analysis/`](./visibility_analysis/))

Pipeline to determine whether an injected in-page prompt is visible to a human reader.

- `index.js` — Playwright script that loads each URL, locates the matched pattern in the live DOM,
  computes WCAG contrast ratio, and tests 15 visibility attributes (`display:none`, `visibility:hidden`,
  `opacity:0`, `1px text spam`, `color:transparent`, `text-indent` off-screen, `clip` / `clip-path`,
  zero-size element, off-viewport positioning, occluding overlays, `z-index` traps, close text/background color).
- `summarize.py` — Aggregates per-URL JSON outputs from `index.js` into the columnar `data/visibility.csv`.

- `example.input.csv` — Minimal `(ID, url, pattern)` csv for demonstration purposes.

```bash
node visibility_analysis/index.js --csv=example.input.csv --headless=true --wait=10000
python visibility_analysis/summarize.py -i outputs/ -o data/visibility.csv
```

---

## 9. Lifetime Analysis ([`lifetime_analysis/`](./lifetime_analysis/))

Measures how long an in-page prompt injection persists in the wild.

- `wayback.py` — For each `(url, ID, pattern)`, queries the Wayback Availability API at four offsets
  (3 / 6 / 9 / 12 months), downloads the closest snapshot, and stores `{label, snapshot_url, response}` JSONs.
- `summarize.py` — Collapses the result into
  a per-URL row containing presence labels — the basis of `data/prompt_lifetime.csv`.

```bash
python lifetime_analysis/wayback.py    -I matches.tsv -D outputs/
python lifetime_analysis/summarize.py  -I matches.tsv -D outputs/ -O data/prompt_lifetime.csv
```

---

## 10. Ranking ([`ranking/`](.ranking/))

Maps each injecting host to a global popularity rank.

- `find_ranking.py` — Find Tranco rank of a given domain (`tranco_ZWZ5G.csv` — is the Tranco list snapshot used for the paper).

- `tranco/tranco_checker.py` — Lookup + cross-list comparison utility (overlap, version diff). See
  `tranco/README.md`.
- `crux/crux_rank_finder.py` — Resolves Chrome UX Report ranks via BigQuery, with a CSV cache to minimize
  query cost. See `crux/README.md`.

```bash
python ranking/find_ranking.py --input urls.csv --tranco ranking/tranco_ZWZ5G.csv --output ranks.txt
python ranking/crux/crux_rank_finder.py --input urls.csv --cache cache.csv --date 202502
```

---

## 11. Effectiveness Evaluation ([`effectiveness/`](./effectiveness))

Quantifies how often an injection actually changes model behavior. The evaluation grid is **13 models ×
4 page representations ≈ 5,200 trial runs**, the source of `data/effectiveness.csv`.

```
effectiveness/
├── snaps_generator/   # Build accessibility snapshots from raw HTTP responses
├── local_checker/     # Run trials against a local vLLM / OpenAI-compatible server
└── open_checker/      # Run trials against OpenRouter (closed and hosted models)
```

| Representation | What the model sees |
|---|---|
| **HTML (full)** | Raw page source, optionally minified. |
| **Text** | Visible text only (script/style stripped, whitespace collapsed). |
| **Raw response** | JSON `{headers, body}` returned by the server. |
| **Snapshot** | Playwright `snapshotForAI` accessibility tree. |


### 11.1 `snaps_generator/snapshot_generator.py`

Loads each raw response in `example_responses/` into a routed Playwright page, calls the internal
`snapshotForAI` channel, and writes the accessibility snapshot to `output_snapshots/`. Used to
construct the `Snapshot` representation column in the evaluation grid.

### 11.2 `local_checker/` (vLLM / OpenAI-compatible)

| Script | Representation | Output column |
|---|---|---|
| `local_html_checker.py` | HTML + Text-only | `response_<model>` |
| `local_raw_data_checker.py` | Raw JSON response | `response_req_<model>` |
| `local_snapshot_checker.py` | Accessibility snapshot | `snapshot_<model>` |

```bash
python local_html_checker.py     --model "Qwen/Qwen2.5-7B-Instruct"
python local_raw_data_checker.py --model "Qwen/Qwen2.5-7B-Instruct"
python local_snapshot_checker.py --model "Qwen/Qwen2.5-7B-Instruct"
```

### 11.3 `open_checker/` (OpenRouter)

Mirror of `local_checker/` but routed through the OpenRouter API to cover closed-source
and hosted-only models (e.g., GPT, Gemini, Claude families).

```bash
python open_html_checker.py     --api_key $OPENROUTER_API_KEY --model "google/gemini-pro-1.5"
python open_raw_data_checker.py --api_key $OPENROUTER_API_KEY --model "google/gemini-pro-1.5"
python open_snapshot_checker.py --api_key $OPENROUTER_API_KEY --model "google/gemini-pro-1.5"
```

Each `example_data/` directory ships two reference cases (IDs `0` and `1`) with HTML, raw response,
and snapshot artefacts so the entire evaluation can be smoke-tested without API keys.

---

## 12. Data Analysis ([`data_analysis/`](./data_analysis/))

We include several notebooks for data analysis. 

### `main.ipynb` — Dataset Characterization
- Dataset stats: unique injections, pages, hosts  
- Prompt distribution across hosts, instances, pages  
- Inclusion methods (HTTP headers, CSS, JSON-LD, etc.)  
- Objectives (e.g., Data Exfiltration, System Disruption)  
- Visibility analysis (`visibility.csv`, UpSet plot)  
- UI position analysis (`ui_position.csv`)  
- Lifetime analysis (`prompt_lifetime.csv`, survival curves)  

### `clustering_and_nli.ipynb` — Clustering & Prompt Strategies
- Lexical clustering (token similarity)  
- Semantic clustering (embeddings + DBSCAN)  
- NLI classification (zero-shot, 8 strategy labels)  
- Output: enriched dataset `dataset_tp.csv`  

### `ecosystem.ipynb` — Ecosystem Analysis
- Prompts-per-domain distributions (CDF, histogram)  
- Ranking analysis
- Topic/category breakdown  

### `effectiveness.ipynb` — Model Effectiveness
- Validation & summary tables (balance checks, outcome overlap)  
- Model comparison across representations  
- Category analysis (Small / Medium / Large / Closed-source)  
- Representation effects by model size  


---

## 13. Reproducing the Paper Figures

```bash
# starting from the released CSVs in data/, run the notebooks
jupyter lab data_analysis/main.ipynb
jupyter lab data_analysis/clustering_and_nli.ipynb
jupyter lab data_analysis/ecosystem.ipynb
jupyter lab data_analysis/effectiveness.ipynb
```

All figures and tables in the paper can be regenerated end-to-end from the shipped CSVs in `data/` without re-executing the multi-day data collection and effectiveness trials.

---

## 14. Shared Utilities

| File | Purpose |
|---|---|
| [`settings.py`](settings.py) | Single source of truth for all paths (`OUT_DIR`, `DATA_DIR_COMMONCRAWL`, ...), pattern file location, and `TASK_ID`-keyed sub-namespaces for distributed runs. |
| `io_module.py` | Thin JSON / JSONL read+write wrappers with optional I/O logging. |
| `logger.py` | Returns a configured `logging.Logger` (rotating 5×5 MB file handler + stdout). |

---

## 15. Licensing and Terms of Use

### Public Dataset

The publicly released dataset, including sanitized prompt injection strings, derived labels, and accompanying documentation, is made available under the Creative Commons Attribution 4.0 International (CC BY 4.0) licence. Under this licence, users may copy, redistribute, adapt, and build upon the material for any purpose, including commercial use, provided appropriate attribution is given to the original authors.

### Source Code

The software, scripts, and analysis code accompanying this project are released under the GNU Affero General Public License v3 (AGPLv3). Users may use, modify, and redistribute the software in accordance with the terms of the licence. Any modified versions or network-accessible services based on the software must make their corresponding source code available under the same licence.

### Full Dataset Access

The complete dataset, including URLs, domains, and other identifying metadata, is not publicly released. Access to this version is provided only to approved applicants for legitimate research or defensive security purposes.

Recipients of the full dataset must agree not to redistribute the data, publish identifying metadata, attempt to identify or contact affected website operators based on the dataset, or use the data for offensive security activities. Access is granted at the discretion of the dataset maintainers and may be revoked in cases of misuse or violation of these conditions.

To request access, complete the form [here](https://docs.google.com/forms/d/e/1FAIpQLSe1td1xhGtm8-Svv-RlhHd7Gxgp1ma9t9WOAmp05L4F_C4x3w/viewform)


## 16. Publication

You can checkout a pre-print of our paper [here](https://arxiv.org/abs/2604.27202).

```
@inproceedings{InPagePromptInjection,
  title = {A Large-scale Measurement of In-Page Prompt Injections Against LLM Web Agents},
  author= {Soheil Khodayari, Xuenan Zhang, Bhupendra Acharya, and Giancarlo Pellegrino},
  booktitle = {In Proceedings of the ACM Conference on Computer and Communications Security (CCS '26)},
  year = {2026}
}   
```
