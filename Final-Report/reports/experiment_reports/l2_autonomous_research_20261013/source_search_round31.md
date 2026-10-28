# Round 31 — metadata screen for BELLS-O and Persuasive Jailbreaker

## Scope Boundary Declaration

This round reviews first-party cards and repositories only to screen potential L2 JB train sources. No dataset rows, train/validation/test splits, or prompt payloads were opened or downloaded. PI-Guard test payload, L3/cascade, smoke, commit, and publication stayed out of scope.

## Findings

| Candidate | First-party metadata | Disposition |
| --- | --- | --- |
| BELLS-O Jailbreak Dataset | The publisher describes 6,406 automatically transformed prompts derived from 720 BELLS base prompts, using 35 techniques in nine technique families; the base set itself mixes handcrafted and AI-generated samples. The card declares CC-BY-NC-SA-4.0 and requires a gated access request with use restrictions. [Publisher dataset card](https://huggingface.co/datasets/centrepourlasecuriteia/jailbreak-dataset) | Not an independent human JB source: transformed cases share 720 base groups and a generated attack process. Access gate and noncommercial/share-alike terms are unresolved for the project. No request or acquisition. |
| Persuasive Jailbreaker / PAP | The authors describe a method that automatically constructs persuasive adversarial prompts from an AdvBench sub-dataset; release of the dataset is available only after signing a release form and remains at author discretion. The repository's Apache-2.0 license covers the public repository content, not necessarily the gated payload. [Author repository and access terms](https://github.com/CHATS-lab/persuasive_jailbreaker) · [paper](https://arxiv.org/abs/2401.06373) | Not independent original human prompt data; generated from an existing benchmark and gated. No request or acquisition. |
| TrustAIR in-the-wild source | The authors report 6,387 prompts from Reddit, Discord, websites, and open-source datasets, including 666 jailbreak-labeled prompts; the repository is MIT-licensed. [Author repository](https://github.com/TrustAIRLab/JailbreakLLMs) | Already the existing JB source family. Repackaging the same collection does not add independent source coverage. |

## Decision and next work

No candidate clears independent source ancestry, standalone single-turn semantics, rights, privacy, and train-role gates. BELLS-O and PAP may support later controlled research only if their access and terms become explicitly eligible; their benchmark transformations do not establish an independent human JB family. No source payload was opened, no package was created, and no model run was justified. Continue metadata-only discovery for separately lineaged public JB attempts and preserve the official L2 gate as `GATE_UNSPECIFIED`.

No test payload, L3, cascade, smoke, commit, or publication occurred in R31.
