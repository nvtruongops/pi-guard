# L2 source and label-mapping decision — round 23

## Scope boundary

This round audited whether Anthropic HH-RLHF red-team attempts support a jailbreak label and built a train-only successor after resolving that mapping conservatively. Work remained in L2. No PI-Guard test payload, L3, cascade, smoke, shortened fit, commit, or publication was used.

## Decision

Exclude all 2,241 Anthropic red-team-attempt turns from JB training. Their source-native task identifies attempts submitted to a red-team conversation, but that alone does not establish that each turn attempts to bypass an LLM safety policy. The data were not relabeled. This is a label-validity exclusion, not a claim that the source authors' labels are incorrect.

## R05 package

R05 removes those 2,241 rows from the R04 lineage and retains 140,429 train rows: 28,970 benign, 110,575 PI, and 884 JB. The 9,756-row validation split is unchanged. The final-test contract remains family-only metadata.

The fixed balanced C=2 validation fit returned NOT_READY, with no selected operating point. Validation macro-F1 was 0.52664, benign FPR 0.30110, PI recall 0.38606, and JB precision/recall/F1 0.57519/0.86932/0.69231. The comparable R04 fit had macro-F1 0.31778 and JB F1 0.16843. This sizeable change after removing an unsupported JB mapping is evidence that the prior mapping damaged the classifier; it does not establish human-gold labels or a formal pass.

Complete five-fold family OOF covered 140,429 rows: macro-F1 0.76383, accuracy 0.91760, benign FPR 0.30860, and JB precision/recall/F1 0.41615/0.83371/0.55518. These results improve over R04, but JB source support still traces to the TrustAIR collection and the local acceptance rubric remains unspecified.

## Limits and next step

Keep R05 immutable as a historical comparator. Do not restore the excluded Anthropic rows under a different mapping. Continue looking for an independently lineaged, non-synthetic human jailbreak-attempt source and keep class semantics, rights, privacy, and source overlap separate from model metrics.

## Records

- Candidate audit: anthropic_redteam_candidate_audit_round19.json
- R05 build: l2_semantic_exclusion_package_build_round23_r01.json
- R05 full fit: private run l2_source_qualified_c2_balanced_validation_20261013_r05
- R05 five-fold family OOF: l2_source_qualified_family_oof_round23_r05.json
- Related source review: source_qualification_round19.md
