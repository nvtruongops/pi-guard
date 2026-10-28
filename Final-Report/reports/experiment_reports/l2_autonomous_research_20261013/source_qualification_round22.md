# L2 source qualification and experiment record — round 22

## Scope boundary

This record covers only L2 source qualification, train/validation package evidence, and full L2 diagnostics. PI-Guard's final-test row IDs/text/payload remained sealed; the approved family-only test metadata contract was preserved. No L3, cascade, smoke, shortened fit, commit, or publication was used. Labels are provisional research references, not curator-reviewed gold.

## Decision

Banking77 was admitted to a private research-only successor as a provisional benign reference after a pinned train-only audit. The added benign source improved aggregate five-fold family OOF relative to the round21 package, but the full validation fit remained NOT_READY and JB quality remained weak. The formal project gate is still GATE_UNSPECIFIED.

The first package artifact labeled R03 was rejected at metadata preflight. Its output directory was named r03 while STATUS.json retained the R02 identity; preflight also found incomplete PolyAI source-rights metadata. No fit started and no row payload was opened. The corrected R04 package was built separately; the historical R03 failure is recorded in l2_source_heldout_package_build_round22_r03.json.

## Source and package evidence

PolyAI's publisher repository provides Banking77 as a train split under CC BY 4.0, and the associated paper describes English customer-service utterances across 77 banking intents. Only the pinned publisher train CSV was used; the upstream test split was not acquired or opened. [PolyAI task-specific datasets](https://github.com/PolyAI-LDN/task-specific-datasets) · [Casanueva et al., ConvAI 2020](https://aclanthology.org/2020.nlp4convai-1.5.pdf)

The aggregate audit screened 10,003 publisher train rows and retained 9,937 after exact and near-duplicate checks against the frozen R21 train/validation package. One exact overlap and three near-duplicate candidates were excluded; no configured PII-pattern match was observed. This is a screening result, not proof that the corpus contains no personal information. Banking intent labels map only to provisional benign references for this project.

R04 contains 142,670 train rows: 28,970 benign, 110,575 PI, and 3,125 JB. Validation is unchanged at 9,756 rows, including 2,089 benign, 7,491 PI, and 176 JB. Test remains metadata-only by family.

## Full L2 evidence

The fixed balanced C=2 validation fit returned NOT_READY with no selected operating point. Validation macro-F1 was 0.31778, benign FPR 0.51364, PI recall 0.35069, and JB precision/recall/F1 0.09287/0.90341/0.16843.

Complete five-fold family OOF covered all 142,670 train rows. Pooled macro-F1 was 0.56976, accuracy 0.86697, benign FPR 0.47453, and JB precision/recall/F1 0.07080/0.23008/0.10828. Relative to R21 R02 OOF, aggregate macro-F1 and benign FPR improved; this is evidence about the added source mix, not source-independent generalization or an L2 pass.

## Limits and next step

Banking77 is one additional benign collection family, and the project mapping remains provisional. The regex privacy screen is incomplete; human privacy review and owner-level rights/lineage evidence remain partial. The run does not qualify the model for L2 PASS. Keep the package immutable and continue source qualification rather than retuning this same data.

## Records

- R03 preflight correction: l2_source_heldout_package_build_round22_r03.json
- R04 build: l2_source_heldout_package_build_round22_r04.json
- R04 five-fold family OOF: l2_source_diverse_family_oof_round22_r04.json
- R03 source audit/build implementation: audit_banking77_train_round22.py and build_l2_source_heldout_round22.py
