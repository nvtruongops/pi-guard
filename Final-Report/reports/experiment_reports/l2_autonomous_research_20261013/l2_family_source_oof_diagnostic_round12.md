# L2 source and family OOF error diagnostic — round 12

## Scope boundary

This is a train-only diagnostic of the completed C=2 JB-moderated, five-fold source-family OOF run. It joins OOF predictions to the frozen package's train rows and train provenance in memory, then emits aggregate counts and rates only. It does not read validation or test rows, prompt text, or test metadata; it does not run training, L3, or smoke.

## Run record

- Run ID: `l2_family_source_oof_diagnostic_round12_20261013`
- Status: `COMPLETED_READ_ONLY_DIAGNOSTIC`
- Time: 2026-10-13 07:41 UTC
- Package: `pi_guard_native_reference_round07_20261013_r01`
- Package manifest SHA-256: `a62f09c0af686b3ad98b99dbb4dd839c32cd6b7e7513409405e29ba056a90650`
- Train rows SHA-256: `7f3666e01b27cfb3a1efab3527a783848328bcc854a82b3bf3fe0fd821aa4fcc`
- Train provenance SHA-256: `581b2379c997c72a4349f4cf1ff9231f356010fb56b6acf5df35b35e65b52888`
- OOF predictions SHA-256: `4b21991726d0b1cdcb457a4eff8a3168412668c7fe7c29c7e1337fb446b99b19`
- Runtime: Python 3.14.7; read-only aggregation, no model fit.
- Integrity checks: package train and provenance hashes match the manifest; OOF covers each of 115,953 train rows exactly once; labels match; no row IDs or text were emitted.

## Results

The train partition contains 115,953 rows from three source repositories. Source/class support is strongly uneven:

| Source repository | Reference class | Rows | Families | OOF result |
| --- | --- | ---: | ---: | --- |
| HumanCompatibleAI/tensor-trust-data | PI | 109,707 | 2,316 | PI recall 0.993 |
| neuralchemy/Prompt-injection-dataset | PI | 868 | 1 | PI recall 0.965 |
| TrustAIRLab/in-the-wild-jailbreak-prompts | JB | 884 | 10 | JB recall 0.739; within-source JB precision 1.000 |
| TrustAIRLab/in-the-wild-jailbreak-prompts | benign | 4,494 | 7 | benign false-alarm rate 0.111 |

Family-level recall distributions reveal additional skew hidden by pooled row metrics:

| Reference class | Families / rows | Family recall (median; min–max) | Families with zero recall / below 0.5 | Family size (min / median / max) |
| --- | --- | --- | --- | --- |
| benign | 7 / 4,494 | 0.757; 0.323–0.987 | 0 / 1 | 31 / 180 / 3,197 |
| PI | 2,317 / 110,575 | 1.000; 0–1.000 | 7 / 8 | 1 / 6 / 6,527 |
| JB | 10 / 884 | 0.736; 0–0.909 | 1 / 1 | 2 / 60 / 348 |

## Interpretation and limits

The strongest remaining evidence gap is source and family coverage, not a demonstrated compute ceiling. All benign and JB training references come from TrustAIR; almost all PI rows come from TensorTrust, while the second PI source contributes one family. The OOF split holds out families within these sources, so it does not establish generalization to an independently held-out source. Benign support is especially concentrated: one family contributes 3,197 of 4,494 rows. JB evaluation covers only ten families. These are native-reference mappings, not curator-reviewed gold labels.

Earlier full L2 comparisons already found no robust win from C=1, C=4, equal family mass within class, or a smaller character-feature cap. With the current support pattern, another parameter sweep would not resolve source-level generalization and could only optimize the same narrow reference set. The result does not establish that model research is exhausted; it identifies why more model tuning on this package has low evidential value.

## Readiness and next useful L2 work

The formal state remains `NOT_READY` / `GATE_UNSPECIFIED`; this diagnostic is not an acceptance test and does not authorize a PASS. The next high-value L2 work is to improve independently qualified source/family support and resolve the owner decisions recorded in the round-11 evidence matrix, then freeze a new versioned train/validation package before any newly justified full L2 experiment. Do not select data, labels, or operating limits from these aggregate errors alone.

Test remains sealed. No test payload, L3, smoke task/run, commit, or publication was used for this diagnostic.
