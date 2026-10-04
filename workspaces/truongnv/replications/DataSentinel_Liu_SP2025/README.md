# DataSentinel SOTA candidate package

**Status (2026-09-30): candidate source retained; no local empirical result is reportable.** The upstream repository provides public task/data loaders and points to the detector checkpoint, but this local package has no frozen DataSentinel-specific evaluation split. Pin the source tasks and protocol before a new run.

Paper: *DataSentinel: A Game-Theoretic Detection of Prompt Injection Attacks*, IEEE S&P 2025.

Upstream source: https://github.com/liu00222/Open-Prompt-Injection. The former 20-row project probe had no verified row-level provenance and was scored by a local regex/canary heuristic, not the paper’s minimax detector. That probe and its dependent results were withdrawn; the local runner is fail-closed. The adapter in `src/models/replications_adapters.py` also remains a local heuristic, not DataSentinel.
