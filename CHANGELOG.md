# Changelog

All notable changes to the **PI-Guard** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.4.0] - 2026-09-10

### Added
- **Directory Scaffolding in `Final-Report/`**: Reconstructed standardized folder skeletons for `notebooks/` (`configs/`, `data/`, `models/`), `src/` (10 functional modules), and `tests/` (unit, integration, adversarial) with `.gitkeep` and `README.md` files, adhering to the Review 1 Zero-Code Invariant.
- **Declarative Experiment Configurations**: Integrated 4 canonical YAML configuration files in [`Final-Report/notebooks/configs/`](Final-Report/notebooks/configs/):
  - `data.yaml`: Hugging Face benchmark data sources, label taxonomy, and Group-Aware Splitting parameters (70/15/15).
  - `evaluation.yaml`: Safety thresholds, adversarial test slices, and latency budgets ($P95 < 30\text{ ms}$).
  - `models.yaml`: Architecture specifications for TF-IDF Baseline and DeBERTa-v3 ONNX INT8 Engine.
  - `training.yaml`: Hyperparameters for baseline classifiers and transformer fine-tuning.
- **Supervisor Presentation & Process Tracking**: Added the official 22-slide deck [`PI-GUARD-Present-109.pptx`](Final-Report/reports/PI-GUARD-Present-109.pptx) and the official semester tracking ledger [`PI_GUARD_PROCESS_REPORT.xlsx`](Final-Report/reports/PI_GUARD_PROCESS_REPORT.xlsx) in `Final-Report/reports/`.
- **Supervisor & Internal Meeting Minutes**: Archived official meeting records for Sprint 1 kick-off, literature screening, and presentation preparation in [`Final-Report/Meeting/`](Final-Report/Meeting/) (`Meeting 1`, `Meeting 2`, `Meeting 3`).
- **Docs Portal Synchronization Skill**: Registered `.agents/skills/docs-portal-sync-and-deploy/` and updated `AGENTS.md` to automate documentation aggregation and GitHub Pages continuous deployment.

### Changed
- **Root `README.md` Internationalization & Polish**: Translated the entire landing documentation to academic/enterprise English standard, purged all emoji icons, collapsed `thesis/` to a concise single-line representation, and redesigned the System Architecture Mermaid diagram with an un-nested, high-contrast Dark Navy layout (`#0f172a`).
- **Local QA Suite Validation (`validate_local.py`)**: Enhanced `step_code_linting` and `step_automated_tests` to guard against empty scaffold directories, ensuring 100% PASS scores during Review 1 zero-code state.
- **Contributing Guidelines (`CONTRIBUTING.md`)**: Realigned the 4-member parallel action plan and evaluation milestones strictly with [`FPT_IAP491_Capstone_Guidelines_and_Rubrics_Summary.md`](Final-Report/thesis/FPT_IAP491_Capstone_Guidelines_and_Rubrics_Summary.md) (Sprint Tiền Đề, Review 1 [Report 1 & 2: 35%], Review 2 [Report 3: 20%], Hội Đồng 1 / Giữa Kỳ [Report 4: 25%], Hội Đồng Final / Bảo Vệ Tốt Nghiệp [Report 5 & 6: 20% + 50% Presentation]), assigned formal reporting lead roles to all 4 members, and strictly limited Review 1 deliverables to existing artifacts in `Final-Report/`.
- **Documentation Link Hygiene**: Removed hardcoded localhost (`http://127.0.0.1:8000`) references across `README.md`, `CONTRIBUTING.md`, and documentation portal build outputs in favor of clean CLI instructions and official GitHub Pages deployment links.
- **Academic Metadata & Supervisor Alignment**: Standardized academic program to `IA`, term to `Fall 2026`, purged legacy `Location & Year: Hanoi, 2026`, and designated MSc. Trần Văn Ninh (`ninhtv2@fpt.edu.vn`) as official Supervisor across all thesis dossiers, report templates, meeting records, and documentation portals.
- **Purged Git Feature Branch Column**: Removed the `Nhánh Git Feature` / `Git Feature Branch` column from member allocation and governance tables across `CONTRIBUTING.md`, `AGENTS.md`, and all generated documentation pages, focusing collaboration directly on sandboxed workspace directories.
- **Sanitized Documentation Portal & Purged Internal Guidelines**: Completely removed internal university confidential materials (`fpt_capstone_guide`) from the public documentation portal directory (`Github-Page/`), relocating local copies strictly to gitignored `docs/fpt_capstone_guide/`, updated `mkdocs.yml`, `validate_local.py`, and `audit_workspace_boundaries.py` to ensure zero internal guidelines are exposed or tracked in Git.

---

## [0.3.0] - 2026-09-08

### Added
- **Three-Tier Subsystem Realignment**: Consolidated the root workspace into exactly three primary subsystems:
  - `Final-Report/`: Master thesis, official reports, slides, references, and deliverables hub.
  - `Github-Page/`: Web documentation portal powered by MkDocs Material.
  - `workspaces/`: Sandboxed development environments for members (`truongnv`, `ducnq`, `vietpmh`, `phuongddd`).
- **Academic Grounding & Literature Repository**: Downloaded full-text PDFs for 18 peer-reviewed scientific papers (IEEE S&P, ACM CCS, NeurIPS, ICLR) stored in [`Final-Report/References/`](Final-Report/References/) alongside [`REFERENCES_LOG.md`](Final-Report/References/REFERENCES_LOG.md).
- **Review 1 Academic Dossier**: Finalized [`Review1_Problem_Definition_and_Threat_Model.md`](Final-Report/thesis/Review1_Problem_Definition_and_Threat_Model.md) and compiled draft chapters 1 and 2 in [`FINAL_THESIS.md`](Final-Report/thesis/FINAL_THESIS.md).
- **8-Pillar Documentation Web Portal**: Implemented MkDocs Material documentation aggregating 8 research pillars (Prompt Study, Attacks, Threat & Defense, Datasets, Models, Robustness, Optimization, Evaluation) deployed to GitHub Pages (`gh-pages`).

---

## [0.2.0] - 2026-09-04

### Changed
- **Local-Only Validation Suite**: Transitioned from GitHub Actions cloud runners to a high-speed, local-first Quality Assurance suite ([`Final-Report/scripts/validate_local.py`](Final-Report/scripts/validate_local.py)).
- **Git Pre-commit Hook**: Upgraded hook to enforce workspace boundaries, immutable file invariants, JSON manifest schemas, and code linting locally before every commit.

### Removed
- **GitHub Actions Cloud CI Workflows**: Removed legacy CI/CD runners to prevent external quota consumption, adopting local-first pre-commit and pre-merge validation.

### Fixed
- **Linter & Test Polish**: Resolved unused imports and variables in adversarial test modules to achieve 100% clean Ruff checks.

---

## [0.1.0] - 2026-09-01

### Added
- **Project Structure**: Initialized research-grade Capstone repository structure (`src/`, `configs/`, `data/`, `experiments/`, `tests/`, `reports/`, `docs/`).
- **MCP Integration**: Configured development MCP servers (`arxiv`, `jupyter`, `duckduckgo-search`, `playwright`, `memory`, `sequential-thinking`).
- **Agent Skills**: Developed specialized skills covering research, dataset engineering, model training, evaluation, API, and thesis writing.
- **Architecture Refactoring**: Decoupled Classifier, Policy Engine, Guardrail Middleware, and LLM Proxy layers.
- **Adversarial Benchmark Suite**: Added structured test slices for Direct Injection, Indirect Injection, Jailbreak, Obfuscation, Multilingual, and Encoding attacks.
- **Collective Code Ownership**: Configured [`.github/CODEOWNERS`](.github/CODEOWNERS) for 4-member peer reviews.
