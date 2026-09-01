# Changelog

All notable changes to the **PI-Guard** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.0] - 2026-09-01

### Added
- **Project Structure**: Initialized research-grade Capstone repository structure (`src/`, `configs/`, `data/`, `experiments/`, `tests/`, `reports/`, `docs/`).
- **MCP Integration**: Configured 6 development MCP servers (`arxiv`, `jupyter`, `duckduckgo-search`, `playwright`, `memory`, `sequential-thinking`).
- **Agent Skills**: Developed 6 specialized skills covering research, dataset engineering, model training, evaluation, API, and thesis writing.
- **Architecture Refactoring**: Decoupled Classifier, Policy Engine, Guardrail Middleware, and LLM Proxy layers.
- **Adversarial Benchmark Suite**: Added structured test slices for Direct Injection, Indirect Injection, Jailbreak, Obfuscation, Multilingual, and Encoding attacks.
- **CI/CD**: GitHub Actions workflows for continuous integration, linting, testing, and model evaluation smoke testing.
