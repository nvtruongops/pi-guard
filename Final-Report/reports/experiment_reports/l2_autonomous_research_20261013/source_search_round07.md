# Source search — round07 (English JB family candidates)

## Scope and result

This was a metadata/card-only screen for an additional, independently lineaged English jailbreak training family. No new dataset payload was downloaded, no candidate was added to the frozen package, and the approved sealed test-family contract was not changed. No source cleared the combination of compatible labels, traceable row-level ancestry, and safe family separation needed for this round.

## Candidates

| Candidate | Publisher evidence | Decision |
|---|---|---|
| [JailbreakDB](https://huggingface.co/datasets/rux22/JailbreakDB) | Its card describes separate deduplicated jailbreak/adversarial and regular corpora and fields for binary jailbreak label, `source`, and `tactic`; it does not define a task-ready train/validation/test partition. The related SoK describes a compilation across many upstream sources. | Do not add in round07. A source field could support a later row-level ancestry audit, but the mixed parent corpus and lack of compatible 3-way labels mean it cannot be treated as an independent family without resolving overlap against current train, validation, and sealed-test families. No rows were loaded. |
| [General Analysis GA Jailbreak Benchmark](https://huggingface.co/datasets/GeneralAnalysis/GA_Jailbreak_Benchmark) | The publisher describes 2,795 synthetic jailbreak attempts and boundary-compliant safety prompts; labels encode policy violation versus compliance, not PI-Guard's PI/JB distinction. | Exclude: synthetic prompts are outside the current candidate policy and labels do not map natively to PI/JB. |
| [AllenAI WildJailbreak](https://huggingface.co/datasets/allenai/wildjailbreak) | Its card describes adversarial prompts composed through WildTeaming and a separate adversarial evaluation set. | Exclude: generated adversarial rows and evaluation split do not provide a clean new native-reference family for this experiment. |
| [JailJudge](https://huggingface.co/datasets/zdxnlp/JailJudge) | Its card describes a mixed training set with synthetic and in-the-wild prompt categories, prompt-response pairs, model-assisted judging, and a separately human-annotated evaluation set. | Exclude: the train labels and source-family ancestry are not directly compatible with the fixed prompt-only PI/JB task; evaluating it would also require resolving parent overlap before any payload use. |

## Decision

Keep dataset version `0.6.0-native-reference-candidate` unchanged. Round07 instead tests one bounded training-side hypothesis against the already frozen English train/validation package: equal total sample weight per represented training family may reduce the dominance of TrustAIR in the pooled fit. The frozen unweighted baseline and all earlier package versions remain intact.

## References

- Hong et al., [SoK: Taxonomy and Evaluation of Prompt Security in Large Language Models](https://arxiv.org/abs/2510.15476), describes JailbreakDB as an aggregation of many upstream sources.
- Dataset facts above are publisher-card statements, not independent rights opinions or evidence of human-gold PI-Guard labels.
