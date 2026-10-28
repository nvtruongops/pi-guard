# Manual Review Log

## Release reviewed

- Dataset version: 1.0.0
- Review date: 2026-07-13
- Reviewer: Enes Deniz
- Scope: 180 pairs / 360 rows, equal to 30% of the release

## Sampling design

The review sample covers:

- all 12 attack families;
- train, validation and test splits;
- all five phrasing variants used by the deterministic generator;
- 15 scenarios per family: five train, five validation and five test scenarios.

The sample can be reproduced with:

```bash
ruby scripts/review_sample.rb
```

## Checks performed

- label and boundary agreement within each pair;
- grammatical completeness and sentence flow;
- plausibility of the workflow and requested action;
- consistent use of roles, tools, approvals and assets;
- accidental duplicate or repeated wording;
- absence of customer data, credentials and personal identifiers.

## Changes made during review

- corrected article and subject-verb agreement problems in generated templates;
- removed repeated words introduced by template interpolation;
- clarified approval, retrieval, memory and delegated-agent wording;
- normalized human-readable names for source contexts;
- separated safe analysis of obfuscated text from instructions to decode and obey it;
- tightened benign rows so they preserve, rather than merely mention, the security boundary.

## Limitations

This was a single-author review. It does not provide independent adjudication or inter-annotator agreement. The remaining 70% passed automated schema, duplicate, leakage, sensitive-pattern and pair-integrity checks but was not read line by line for this release.
