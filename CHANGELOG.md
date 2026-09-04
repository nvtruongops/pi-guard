# Changelog

All notable changes to the **PI-Guard** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.2.0] - 2026-09-04

### Changed
- **Local-Only Validation Suite**: Transitioned from GitHub Actions cloud runners to a high-speed, local-first Quality Assurance suite ([`scripts/validate_local.py`](file:///d:/Work/Do-an/scripts/validate_local.py)).
- **Git Pre-commit Hook**: Upgraded hook to enforce workspace boundaries, immutable file invariants, JSON manifest schemas, and code linting locally before every commit.

### Removed
- **GitHub Actions Workflows**: Removed all `.github/workflows/` (`ci.yml`, `deploy-docs.yml`, `evaluation.yml`) to eliminate external cloud CI dependencies and avoid runner quota consumption.

### Fixed
- **Linter & Test Polish**: Resolved unused imports and variables in [`tests/adversarial/test_obfuscation_robustness.py`](file:///d:/Work/Do-an/tests/adversarial/test_obfuscation_robustness.py) to achieve 100% clean Ruff checks.

---

## [0.1.0] - 2026-09-01

### Added
- **Project Structure**: Initialized research-grade Capstone repository structure (`src/`, `configs/`, `data/`, `experiments/`, `tests/`, `reports/`, `docs/`).
- **MCP Integration**: Configured 6 development MCP servers (`arxiv`, `jupyter`, `duckduckgo-search`, `playwright`, `memory`, `sequential-thinking`).
- **Agent Skills**: Developed 6 specialized skills covering research, dataset engineering, model training, evaluation, API, and thesis writing.
- **Architecture Refactoring**: Decoupled Classifier, Policy Engine, Guardrail Middleware, and LLM Proxy layers.
- **Adversarial Benchmark Suite**: Added structured test slices for Direct Injection, Indirect Injection, Jailbreak, Obfuscation, Multilingual, and Encoding attacks.
- **Collective Code Ownership**: Configured [`.github/CODEOWNERS`](file:///d:/Work/Do-an/.github/CODEOWNERS) for 4-member peer reviews.
