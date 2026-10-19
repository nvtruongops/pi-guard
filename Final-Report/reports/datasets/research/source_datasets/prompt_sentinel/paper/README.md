# PromptSentinel source papers

There is no standalone PromptSentinel research paper listed by its dataset card. The card asks users to credit these source datasets and papers. PDFs in this folder are downloaded from arXiv; titles and identifiers are pinned in `download_manifest.json`.

| Source dataset | Cited paper | Relevance and limits |
|---|---|---|
| TrustAIRLab/in-the-wild-jailbreak-prompts | [arXiv:2308.03825](https://arxiv.org/abs/2308.03825) | In-the-wild jailbreak source; not a paper defining the PromptSentinel mapping. |
| lmsys/toxic-chat | [arXiv:2310.17389](https://arxiv.org/abs/2310.17389) | Real user-AI toxicity/jailbreak annotation source; the curation labels are not equivalent to PI/JB by default. |
| reshabhs/SPML_Chatbot_Prompt_Injection | [arXiv:2402.11755](https://arxiv.org/abs/2402.11755) | Prompt-attack and instruction injection source. |
| Lakera/gandalf_ignore_instructions | [arXiv:2501.07927](https://arxiv.org/abs/2501.07927) | Gandalf security challenge source. |
| OpenAssistant/oasst2 | [arXiv:2304.07327](https://arxiv.org/abs/2304.07327) | Benign conversation source; not a prompt-injection label paper. |
| leolee99/NotInject | [arXiv:2410.22770](https://arxiv.org/abs/2410.22770) | InjecGuard paper introduces NotInject over-defense examples; the card uses 255 rows. |

The source card also lists no paper for the other contributed datasets. It associates xTRam1/Safe-Guard with [arXiv:2402.13064](https://arxiv.org/abs/2402.13064), whose title is *Synthetic Data (Almost) from Scratch: Generalized Instruction Tuning for Language Models*. The Safe-Guard card says GLAN inspired its synthetic generation; it is not a dedicated Safe-Guard dataset paper. Do not cite that arXiv ID as the Safe-Guard dataset's research paper.
