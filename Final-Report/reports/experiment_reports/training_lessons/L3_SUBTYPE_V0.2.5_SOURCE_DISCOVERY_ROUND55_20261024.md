# L3 Subtype v0.2.5 — Source Discovery Round 55

**Date:** 2026-10-24  
**Purpose:** Continue searching for external data that can add independent PI/JB coverage, especially trustworthy BOTH examples.

## Scope boundary declaration

**In scope:** Review public dataset records and metadata; pin the Anwar benchmark; compare its prompts only with v0.2.5 train and validation; record candidate evidence, provenance limits, and rights signals.  
**Out of scope:** Modifying v0.2.5, reading its frozen test payload, creating v0.2.6, assigning L3 labels without adjudication, training, model scoring, or using the prohibited PIDS-Bench source.

## Current gate

The v0.2.5 support gate remains blocked: train BOTH support is 52 against a target of 100, validation BOTH support is 30, and `fit_allowed=false`, as recorded in [SUPPORT_GATE.json](../../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/versions/v0.2.5/SUPPORT_GATE.json). I read gate metadata only; I did not open the v0.2.5 test payload.

## Anwar benchmark: useful future evaluation candidate, not training data

I pinned `MuhammadSaeedAnwar/prompt-injection-llm-benchmark` to commit `b44898ab1700eec850ee68eeb687a40f86406ef8` and staged its 250-row CSV for review. The pinned file has 250 unique IDs and 250 unique normalized prompts. Its repository presents the release as a benchmark and reports a category breakdown, but the pinned CSV differs from that table: the CSV has 49 Direct, 42 Indirect, 62 Jailbreak, 57 Multi-Turn, and 40 Encoding rows; the README reports 60, 55, 70, 40, and 25, respectively. The README documents `primary_category`, while the CSV header is `category`. [[196]](#ref196)

The CSV includes `target_behavior`, but it has no separate PI and JB Boolean labels and no per-row source field. Prompt injection is an attack method, while jailbreak is a goal; the source category and target text therefore do not establish the L3 BOTH contract automatically without row-level adjudication. [[193]](#ref193), [[196]](#ref196). The candidate also has no upstream train/validation/test partition; I kept the full benchmark out of training. [[196]](#ref196)

After verifying the v0.2.5 train and validation hashes, exact normalized overlap was 0/250 against train and 0/250 against validation. A 35-character normalized-prefix screen found candidate IDs `ATK001` and `ATK066`; I excluded both conservatively. That leaves 248 possible future evaluation rows before row-level L3 mapping and per-row lineage review. The row counts and overlap record are in the [candidate audit JSON](../../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/anwar_prompt_injection_llm_benchmark_20261024_round55/CANDIDATE_AUDIT_ROUND55.json). No v0.2.5 test payload was read. [[196]](#ref196)

**Disposition:** hold the 248 rows as a future evaluation candidate only. They do not add BOTH training support and do not unblock `fit_allowed`.

## Additional leads

- **Adversarial Humanities Benchmark (AHB):** the authors publish it as a test benchmark, include a canary, and state that benchmark data must not enter training corpora. Its prompts are transformed from MLCommons AILuminate prompts. I reviewed metadata only and acquired no payload. It could be considered for a later jailbreak-style evaluation after label and overlap review; it is not training data and does not establish BOTH. [[197]](#ref197)
- **JailGuard:** its paper and repository report 11,000 text/image examples across 15 prompt-based attack methods. The repository directs users to an external Google Drive download; I did not acquire payload, and no license file appeared in the pinned repository listing. Row-level L3 co-labels and data rights need review before considering it. [[198]](#ref198)

## Decision and next step

No rows were admitted to train or BOTH support. No dataset version was created, no model was trained or scored, and no train/validation/test model metrics were produced. v0.2.5 remains a blocked diagnostic package. Continue searching for an ungated, rights-clear, source-independent training release with row-level evidence of both the PI method and the jailbreak goal; keep benchmark releases out of training.

## Artifacts

- [Round 55 candidate inventory](../../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/candidate_screen_20261024_round55/candidate_screen_20261024_round55.json)
- [Anwar benchmark candidate CSV](../../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/anwar_prompt_injection_llm_benchmark_20261024_round55/ANWAR_EVAL_CANDIDATE.csv)
- [Anwar audit JSON](../../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/anwar_prompt_injection_llm_benchmark_20261024_round55/CANDIDATE_AUDIT_ROUND55.json)
- [Anwar reproducible audit script](../../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/anwar_prompt_injection_llm_benchmark_20261024_round55/audit_anwar_eval_candidate_round55.py)
- [v0.2.5 support gate](../../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/versions/v0.2.5/SUPPORT_GATE.json)

## References used

[[193]](#ref193), [[196]](#ref196), [[197]](#ref197), [[198]](#ref198).
