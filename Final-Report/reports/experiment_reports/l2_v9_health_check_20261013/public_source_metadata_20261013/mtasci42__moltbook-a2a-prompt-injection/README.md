# Agent-to-Agent Prompt Injection in AI-Only Social Networks

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20822682.svg)](https://doi.org/10.5281/zenodo.20822682)
[![Code License: MIT](https://img.shields.io/badge/Code%20License-MIT-yellow.svg)](LICENSE)
[![Data License: CC BY 4.0](https://img.shields.io/badge/Data%20License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

Code, data, and reproducibility materials for the paper:

> **Agent-to-Agent Prompt Injection in AI-Only Social Networks: A Taxonomy and Detection Study on Moltbook**
> Mustafa Tasci, Bandirma Onyedi Eylul University.
> *(PeerJ Computer Science, 2026; article DOI to be added upon publication.)*

- **Source code (GitHub):** <https://github.com/mtasci42/moltbook-a2a-prompt-injection>
- **Archived release (Zenodo):** <https://doi.org/10.5281/zenodo.20822682>

This repository contains the human-validated dataset, the analysis and modeling notebooks, and the
figures used in the paper. Together they reproduce the taxonomy, the detection benchmark, and the
reported results. A citable, version-archived snapshot is deposited on Zenodo at the DOI above.

---

## Overview

Moltbook, launched in early 2026, is the first social network whose participants are exclusively
autonomous AI agents: agents read and act on one another's posts while humans only observe. This
creates a new attack surface we call **agent-to-agent (A2A) prompt injection**, in which a malicious
post is ingested and acted upon by other agents, so an attack can propagate through a social graph
rather than targeting a single model.

Starting from a 3,105,136-post window of the public Moltbook archive, this work:

1. defines a **five-category attack taxonomy** (instruction override, identity/control hijacking,
   advertising/redirection, information exfiltration, memory poisoning);
2. builds a **human-validated labeled dataset** via LLM-assisted annotation with human adjudication;
3. compares **three detectors**, a zero-shot transformer, a fine-tuned DistilBERT, and an
   interpretable TF-IDF + logistic-regression model, under a **leakage-resistant, group-aware**
   protocol that keeps near-duplicate templates out of both train and test sets;
4. audits the recall of the heuristic candidate-generation screen to characterize platform-wide
   coverage.

**Headline result.** With an optimized threshold, the lightweight interpretable model (F1 = 0.941,
ROC-AUC = 0.977) **matches** the fine-tuned transformer (F1 = 0.917) with no statistically
significant difference (paired bootstrap, McNemar p = 1.0), while being far cheaper and fully
inspectable. A screen-recall audit shows the heuristic stage recovers only about 11% of platform
attacks, so candidate generation, not classification, is the main deployment bottleneck.

---

## Methodology

![Methodology pipeline](figures/Figure1_pipeline_EN-Pipeline.png)

*End-to-end pipeline. Phase 1 covers data collection, recall-oriented heuristic screening, and
human-validated labeling; Phase 2 covers deduplication, group-aware splitting, model training,
threshold optimization, and evaluation.*

The processing and modeling steps, in order, are:

1. **Data collection.** A 3,105,136-post window of the public Moltbook archive is loaded (see the
   *Data* section, *Third-party data source*).
2. **Heuristic screening.** A high-recall, regex-based screen flags candidate posts that match any of
   the five taxonomy categories, producing the candidate pool.
3. **EDA and phase analysis.** Exploratory analysis across the three platform phases (launch,
   stabilization, post-acquisition).
4. **Sampling and labeling.** A phase-balanced sample is drawn from the candidate pool and labeled via
   LLM-assisted annotation with human adjudication, yielding `moltbook_seed_v2.csv`.
5. **Deduplication.** Template-based deduplication groups near-duplicate posts.
6. **Group-aware split.** A train/test split that keeps all members of a duplicate group on the same
   side, preventing template leakage between train and test.
7. **Model training.** Three detectors are trained: zero-shot transformer, fine-tuned DistilBERT, and
   TF-IDF + logistic regression.
8. **Threshold optimization and evaluation.** Decision thresholds are tuned; models are compared with
   paired bootstrap and McNemar tests, group-aware cross-validation, and a temporal holdout.
9. **Recall audit.** An independent phase-stratified sample (`recall_audit_labeled.csv`) estimates the
   true attack base rate and the heuristic screen's recall.

---

## Repository structure

```
.
+-- notebooks/
|   +-- phase1_data_exploration.ipynb   # Phase 1: data loading, heuristic screening,
|   |                                   #          EDA, sampling, seed export, recall audit
|   +-- phase2_model_training.ipynb     # Phase 2: dedup + group-aware split, three models,
|                                       #          threshold opt., bootstrap/McNemar, CV,
|                                       #          temporal holdout, error analysis
+-- data/
|   +-- moltbook_seed_v2.csv            # 630 human-labeled posts (the training/eval seed)
|   +-- recall_audit_labeled.csv        # 1,500 adjudicated posts for the screen-recall audit
+-- figures/                            # figures used in the paper (PNG)
+-- requirements.txt
+-- CITATION.cff
+-- LICENSE
+-- README.md
```

---

## Code information

All analysis is implemented in two self-contained Jupyter notebooks (Python 3.10+), developed on
Google Colab. No separate package or CLI is required; running the notebooks top to bottom reproduces
every result, table, and figure in the paper.

| Notebook | Purpose | Key inputs | Key outputs |
|---|---|---|---|
| `notebooks/phase1_data_exploration.ipynb` | Data loading, high-recall heuristic screening, EDA and phase analysis, balanced sampling, seed export, and the screen-recall audit | Moltbook archive (downloaded in-notebook) | `moltbook_seed_v2.csv`, `recall_audit_labeled.csv`, EDA figures |
| `notebooks/phase2_model_training.ipynb` | Template deduplication and group-aware split; training and evaluation of the three detectors; threshold optimization; bootstrap/McNemar significance tests; group-aware cross-validation; temporal holdout; error and interpretability analysis | `moltbook_seed_v2.csv` | Benchmark tables, ROC/PR curves, significance-test results, error analysis |

- **Language and runtime:** Python 3.10+.
- **Main libraries:** see [`requirements.txt`](requirements.txt) (scikit-learn, pandas, NumPy,
  Hugging Face `transformers`/`datasets`, PyTorch, matplotlib).
- **Hardware:** the TF-IDF and zero-shot paths run on CPU; fine-tuning DistilBERT in Phase 2 benefits
  from a GPU.
- **Configuration:** both notebooks define a `DATASET_DIR` (Google Drive) path near the top; edit it
  to your own directory before running.

---

## Data

### Third-party data source

The raw post archive is third-party data obtained from the **Moltbook Observatory Archive**, an open
dataset published on Hugging Face by the Simula Metropolitan Center for Digital Engineering (SimulaMet):

- **Dataset:** <https://huggingface.co/datasets/SimulaMet/moltbook-observatory-archive>
- **Authors:** Sushant Gautam and Michael A. Riegler (SimulaMet)
- **License:** MIT
- **Underlying tool (source code):** <https://github.com/kelkalot/moltbook-observatory>

The full 3,105,136-post window is **not** redistributed in this repository: it is large and externally
maintained, and is retrieved inside `phase1_data_exploration.ipynb` from the `posts` subset of that
archive, e.g.:

```python
from datasets import load_dataset

ds = load_dataset(
    "SimulaMet/moltbook-observatory-archive",
    "posts",
    split="archive",
)
```

The two CSVs released here are the human-validated subsets derived from that archive. The same source
is cited in the *Materials and Methods* section of the paper; the formal reference is given in the
*Citation* section below.

**Note on post text.** The `content`, `title`, and `display_text` fields reproduce Moltbook posts
verbatim, exactly as they appeared on the platform. A small number of posts contain emoji or
non-Latin scripts. This text has been left unaltered so that the labeled examples remain faithful to
the analyzed data; all files are encoded in UTF-8.

### `data/moltbook_seed_v2.csv`: labeled seed (n = 630)

A phase-balanced sample of 630 posts (167 attacks, 463 non-attacks) drawn from the screened candidate
pool, each adjudicated by a human annotator.

| Column | Description |
|---|---|
| `id` | Post identifier in the archive |
| `agent_name`, `submolt` | Author agent and community |
| `title`, `content` | Post text |
| `score`, `comment_count` | Engagement metadata |
| `phase` | Platform phase (1 = launch, 2 = stabilization, 3 = post-acquisition) |
| `n_categories`, `total_hits`, `heuristic_categories` | Heuristic-screen outputs (matched categories and hit count) |
| `label_is_attack` | **Final label**: 1 = A2A attack, 0 = not an attack |
| `label_category` | Taxonomy category or categories (C1-C5) for positive posts |
| `label_notes` | Annotator notes |

Labeling principle: a post is positive only if it **performs** an attack; posts that merely
**discuss** or defend against attacks are labeled negative.

### `data/recall_audit_labeled.csv`: screen-recall audit (n = 1,500)

A phase-stratified random sample drawn independently of the seed, adjudicated with the same protocol,
used to estimate the true attack base rate and the heuristic screen's recall.

| Column | Description |
|---|---|
| `id`, `phase`, `submolt` | Post id, platform phase, community |
| `regex_flagged` | Whether the heuristic screen flagged this post as a candidate (1/0) |
| `claude_label` | Adjudicated attack label (1 = attack, 0 = not) |
| `category` | Taxonomy category for positives |
| `confidence`, `reason` | Adjudication confidence and rationale |
| `display_text` | Post text shown during adjudication |

Recall is computed as the fraction of adjudicated attacks (`claude_label == 1`) that the screen had
flagged (`regex_flagged == 1`).

---

## Usage and reproducing the results

### Get the repository

```bash
git clone https://github.com/mtasci42/moltbook-a2a-prompt-injection.git
cd moltbook-a2a-prompt-injection
```

(Alternatively, download the archived release from Zenodo: <https://doi.org/10.5281/zenodo.20822682>.)

### Requirements

```bash
pip install -r requirements.txt
```

Python 3.10+ is recommended. Fine-tuning DistilBERT in Phase 2 benefits from a GPU (the notebooks were
developed on Google Colab); the TF-IDF and zero-shot paths run on CPU.

### Steps

1. **Phase 1, `notebooks/phase1_data_exploration.ipynb`.** Loads the archive (or a cached scan),
   runs the high-recall heuristic screen, performs EDA and phase analysis, samples the balanced seed,
   and exports it. An appendix reproduces the screen-recall audit. *Run only one of the two
   data-loading options (cached vs. download-from-scratch).*
2. **Phase 2, `notebooks/phase2_model_training.ipynb`.** Loads the labeled seed, applies
   template-based deduplication and a group-aware train/test split, trains and evaluates the three
   detectors, optimizes thresholds, runs bootstrap/McNemar significance tests, group-aware
   cross-validation, a temporal holdout, and the error/interpretability analysis.

> Both notebooks define a `DATASET_DIR` (Google Drive) path near the top; edit it to your own
> directory before running.

---

## Ethical use

This repository documents attacks that were already publicly visible on Moltbook; it introduces no
new attack vectors. The taxonomy and detector are released as **defensive** artifacts for platform
operators and agent developers. Please do not use these materials to build or deploy A2A injection
attacks. See the *Ethical considerations* section of the paper for a fuller discussion of dual-use.

---

## Citation

If you use this dataset or code, please cite **both** the paper and the archived software/data record.

**Paper:**

```bibtex
@article{tasci2026a2a,
  author  = {Ta{\c{s}}c{\i}, Mustafa},
  title   = {Agent-to-Agent Prompt Injection in AI-Only Social Networks: A Taxonomy and Detection Study on Moltbook},
  journal = {PeerJ Computer Science},
  year    = {2026}
}
```

**Code and data archive (Zenodo):**

```bibtex
@dataset{tasci2026a2a_zenodo,
  author    = {Ta{\c{s}}c{\i}, Mustafa},
  title     = {Agent-to-Agent Prompt Injection in AI-Only Social Networks: Code and Data},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.20822682},
  url       = {https://doi.org/10.5281/zenodo.20822682}
}
```

A machine-readable citation is also provided in [`CITATION.cff`](CITATION.cff).

**Third-party data source.** This work analyzes the Moltbook Observatory Archive; if you use the
underlying data, please also cite its creators:

```bibtex
@dataset{moltbook_observatory_archive_2026,
  author    = {Gautam, Sushant and Riegler, Michael A.},
  title     = {Moltbook Observatory Archive},
  year      = {2026},
  publisher = {Hugging Face Datasets},
  url       = {https://huggingface.co/datasets/SimulaMet/moltbook-observatory-archive}
}

@software{moltbook_observatory_2026,
  author = {Riegler, Michael A. and Gautam, Sushant},
  title  = {Moltbook Observatory: Passive Monitoring Dashboard for AI Social Networks},
  year   = {2026},
  url    = {https://github.com/kelkalot/moltbook-observatory}
}
```

---

## License and contribution

- **Code** (notebooks): MIT License (see [`LICENSE`](LICENSE)).
- **Data** (`data/*.csv`) and **figures**: Creative Commons Attribution 4.0 (CC BY 4.0).

The raw Moltbook archive is governed by the terms of its original source (see the *Data* section,
*Third-party data source*) and is not relicensed here.

**Contributions.** This repository is released primarily as a static reproducibility archive for the
paper. Bug reports, corrections, and reproducibility questions are welcome via GitHub Issues at
<https://github.com/mtasci42/moltbook-a2a-prompt-injection/issues>. If you would like to contribute a
fix, please open an issue first to discuss the change, then submit a pull request referencing it.
Please do not submit contributions that extend the materials toward offensive use (see *Ethical use*).
