---
license: mit
task_categories:
- text-classification
language:
- en
tags:
- prompt-injection
- prompt-attack
- llm-safety
- llm-defense
- system-prompt
- malicious-user-prompt
pretty_name: SPML
size_categories:
- 10K<n<100K
---

# SPML Chatbot Prompt Injection Dataset

Upstream snapshot: [Hugging Face dataset card](https://huggingface.co/datasets/reshabhs/SPML_Chatbot_Prompt_Injection). Associated research paper: [SPML: A DSL for Defending Language Models Against Prompt Attacks](https://arxiv.org/abs/2402.11755). This source is preserved for reference and excluded from the model-ready corpus; the upstream card cautions that it is not advisable to train a prompt-injection detector on this dataset.

[Arxiv Paper](https://arxiv.org/abs/2402.11755)


Introducing the SPML Chatbot Prompt Injection Dataset: a robust collection of system prompts designed to create realistic chatbot interactions, coupled with a diverse array of annotated user prompts that attempt to carry out prompt injection attacks. While other datasets in this domain have centered on less practical chatbot scenarios or have limited themselves to "jailbreaking" – just one aspect of prompt injection – our dataset offers a more comprehensive approach. It not only features realistic chatbot definition and user prompts but also seamlessly integrates with existing prompt injection datasets.

Our primary focus is on the actual content of prompt injection payloads, as opposed to the methodologies used to execute the attacks. We are convinced that honing in on the detection of the payload content will yield a more robust defense strategy than one that merely identifies varied attack techniques.


## Dataset Description
|  | Field           | Description                                                                                                                                              |
|----|-----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1  | System Prompt   | These are the intended prompts for the chatbot, designed for use in realistic scenarios.                                                                  |
| 2  | User Prompt     | This field contains user inputs that query the chatbot with the system prompt described in (1).                                                           |
| 3  | Prompt Injection| This is set to 1 if the user input provided in (2) attempts to perform a prompt injection attack on the system prompt (1).                                 |
| 4  | Degree          | This measures the intensity of the injection attack, indicating the extent to which the user prompt violates the chatbot's expected operational parameters.|
| 5  | Source          | This entry cites the origin of the attack technique used to craft the user prompt.   |

## Dataset Generation Methodology

Our process begins with an initial set of system prompts derived from leaked system prompts from several widely-used chatbots powered by LLMs. We employ GPT-4 to extrapolate from these cases, crafting additional system prompts that emulate the style of the original seeds across diverse subject matters. These prompts are then used to create corresponding valid user input for each generated system prompt. To facilitate the creation of prompts for prompt injection attacks, we dissect each generated system prompt to identify a set of guiding principles or rules they aim to uphold, such as 'speak courteously'. GPT-4 is then tasked with producing an inverse list that semantically negates each rule; for instance, 'speak courteously' is countered with 'speak rudely'. From this inverse list, multiple rules are selected at random—the quantity of which dictates the complexity of the attack (degree)—and these are provided to GPT-4 alongside an 'attack seed prompt'. The objective is to craft a user prompt that aligns with the chosen contrarian rules but retains the stylistic nuances of the attack seed prompt. This tailored seed prompt may also integrate various other attack strategies, enhancing the sophistication and realism of the generated scenarios.

## FAQs
- Should I use this dataset to train my prompt injection detection model?
It is not advisable to train prompt injection detection models on this dataset. Typically, such models look for patterns in user prompts to detect prompt injections. However, the injection payloads in our dataset are subtle and may not be universally malicious. Training your model on the combinations of system and user prompts from our dataset will not ensure generalization until the model understands how the system prompt can be violated by the user prompt. These models require exposure to a wide range of attack techniques, and since our dataset only includes a limited selection applied to diverse payloads, it is not an ideal training source.

- Why were "jailbreak" datasets not included when jailbreaking is considered a form of prompt injection?
For the purpose of this dataset, we only considered sources like TensorTrust and Gandalf that provided precise system prompts. The jailbreak dataset is composed of user prompts designed to create LLM responses that breach ethical guidelines without accompanying system prompts. At the time of development, we lacked a clearly defined system prompt to encapsulate this, hence its exclusion.

- Why haven't attack prompts based on TensorTrust been released?
The TensorTrust dataset is not licensed for distribution, which precludes us from releasing attack prompts derived from it.

## Cite
```
@misc{sharma2024spml,
    title={SPML: A DSL for Defending Language Models Against Prompt Attacks},
    author={Reshabh K Sharma and Vinayak Gupta and Dan Grossman},
    year={2024},
    eprint={2402.11755},
    archivePrefix={arXiv},
    primaryClass={cs.LG}
}
```

### Disclaimer
Please be aware that the dataset provided herein may contain information that could be potentially used for harmful purposes. By accessing and utilizing this data, you acknowledge and agree to bear sole responsibility for any such misuse. It is expected that all users will handle the dataset ethically. We, the providers of this data, expressly disclaim any liability for any improper or illicit use of the data and for any consequences that may arise as a result thereof.
By proceeding to use this dataset, you affirm your commitment to ethical conduct and responsible use of the data provided.
