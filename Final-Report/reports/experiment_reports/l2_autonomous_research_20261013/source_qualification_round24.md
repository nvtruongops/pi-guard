# L2 independent jailbreak-source audit and experiment — round 24

## Scope boundary

This round screened the pinned WUSTL-CSPL jailbreak collection against frozen R05 train/validation data, admitted eligible rows to a new private train-only package, and completed a full fixed L2 fit plus five-fold family OOF. No test rows, IDs, text, or payload were opened; only the approved family-level test contract was retained. No L3, cascade, smoke, shortened fit, commit, or publication was used. The JB mapping is a provisional reference, not human-gold.

## Source qualification

The WUSTL repository and USENIX Security 2024 paper describe a collection of 448 jailbreak prompts gathered from online sources. The paper distinguishes this prompt corpus from a separate 92-participant study. The source collection is therefore a potentially relevant real-world JB reference; it is not a released source-disjoint train/validation package. The repository declares MIT, but that declaration does not independently establish rights to every third-party prompt collected online. Row-level upstream community ancestry is also not fully recorded. [WUSTL-CSPL/LLMJailbreak](https://github.com/WUSTL-CSPL/LLMJailbreak) · [Yu et al., USENIX Security 2024](https://www.usenix.org/conference/usenixsecurity24/presentation/yu-zhiyuan)

The pinned workbook had 448 nonempty records and 447 normalized unique prompts. Aggregate-only comparison against R05 train/validation found 154 exact overlaps, including two label conflicts; all exact-overlap records were excluded. A further 172 near-duplicate candidates at the configured 0.85 five-word-shingle Jaccard threshold and one phone-pattern candidate were excluded. The remaining 120 prompts were retained as one provisional JB train family. No WUSTL external test split was available in the reviewed workbook/manifest, and PI-Guard's final-test partition stayed closed. The configured privacy scan is incomplete and no human privacy adjudication occurred.

## R06 package and fit

R06 adds only the 120 retained WUSTL prompts to R05 train. It has 140,549 train rows: 28,970 benign, 110,575 PI, and 1,004 JB. Validation remains byte-identical to R05 at 9,756 rows. The family-only test contract is unchanged. Package manifest SHA-256: 02a3f7eb8fd3688573472102e33ad95c98987128cb2a2c81b996b832e0531eaf.

The complete balanced C=2 validation fit returned NOT_READY with no selected operating point. Macro-F1 was 0.45726, accuracy 0.45264, benign FPR 0.29679, and JB precision/recall/F1 0.33987/0.88636/0.49134. Against R05's same validation split, macro-F1 fell from 0.52664 and JB F1 fell from 0.69231; benign FPR improved slightly from 0.30110 and JB recall rose from 0.86932. This is a trade-off, not an improvement to retain as the best candidate.

Complete five-fold family OOF covered all 140,549 train rows: macro-F1 0.75550, accuracy 0.91594, benign FPR 0.31450, and JB precision/recall/F1 0.39368/0.83167/0.53440. Compared with R05 OOF, macro-F1, benign FPR, and JB precision/F1 regressed slightly. The WUSTL family was held out in one fold; aggregate-only analysis of its 120 rows yielded 75 JB predictions, 22 PI predictions, and 23 benign predictions, corresponding to JB precision 1.0, recall 0.625, and F1 0.76923 on that single family. This is a useful transfer signal, but one collection family cannot settle performance across independent online communities.

## Decision and next step

R06 is preserved as an immutable data-source experiment and is not selected as the best model candidate. It adds a second publisher collection to JB training and creates one explicit held-out source-family observation, but uncertain upstream ancestry, incomplete rights/privacy review, lower aggregate metrics, and the official GATE_UNSPECIFIED rubric prevent an L2 PASS claim. Do not run more parameter sweeps on R06. Continue L2 source qualification for a single-turn, human-authored, non-TrustAIR JB source with clear dataset rights, source lineage, privacy treatment, duplicate-family structure, and an appropriate train role.

## Records

- Candidate audit: wustl_jb_train_candidate_audit_round24.json
- Audit runner: audit_wustl_jb_train_candidate_round24.py
- Package build: l2_wustl_train_package_build_round24_r01.json
- Package builder: build_l2_wustl_jb_package_round24.py
- R06 full fit: private run l2_wustl_jb_train_c2_balanced_validation_20261013_r06
- R06 five-fold family OOF: l2_wustl_jb_train_family_oof_round24_r06.json
- R05 comparator: l2_source_qualified_family_oof_round23_r05.json and private R05 validation metrics

The reports contain aggregate counts only and intentionally omit source prompt text and row identifiers.
