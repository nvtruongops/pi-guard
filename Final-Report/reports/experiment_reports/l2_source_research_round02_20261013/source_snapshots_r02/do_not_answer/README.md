---
license: apache-2.0
task_categories:
- text-generation
language:
- en
tags:
- safety
- large language model
pretty_name: do-not-answer
size_categories:
- n<1K
dataset_info:
  features:
  - name: id
    dtype: int64
  - name: risk_area
    dtype: string
  - name: types_of_harm
    dtype: string
  - name: specific_harms
    dtype: string
  - name: question
    dtype: string
  - name: GPT4_response
    dtype: string
  - name: GPT4_harmful
    dtype: int64
  - name: GPT4_action
    dtype: int64
  - name: ChatGPT_response
    dtype: string
  - name: ChatGPT_harmful
    dtype: int64
  - name: ChatGPT_action
    dtype: int64
  - name: Claude_response
    dtype: string
  - name: Claude_harmful
    dtype: int64
  - name: Claude_action
    dtype: int64
  - name: ChatGLM2_response
    dtype: string
  - name: ChatGLM2_harmful
    dtype: int64
  - name: ChatGLM2_action
    dtype: int64
  - name: llama2-7b-chat_response
    dtype: string
  - name: llama2-7b-chat_harmful
    dtype: int64
  - name: llama2-7b-chat_action
    dtype: int64
  - name: vicuna-7b_response
    dtype: string
  - name: vicuna-7b_harmful
    dtype: int64
  - name: vicuna-7b_action
    dtype: int64
  splits:
  - name: train
    num_bytes: 3997193
    num_examples: 939
  download_size: 1709142
  dataset_size: 3997193
---


# Do-Not-Answer: A Dataset for Evaluating Safeguards in LLMs

## Overview

*Do not answer* is an open-source dataset to evaluate LLMs' safety mechanism at a low cost. The dataset is curated and filtered to consist only of prompts to which responsible language models do not answer. 
Besides human annotations, *Do not answer* also implements model-based evaluation, where a 600M fine-tuned BERT-like evaluator achieves comparable results with human and GPT-4. 


## Instruction Taxonomy
Instructions are organized by a three-level hierarchical taxonomy, covering 61 specific harms. 
![taxonomy](assets/dna.png)

*Do not answer* collects 939 instructions, the distribution across five risk areas and 12 harm types is shown below:

![risk_area](assets/instruction_dist.png)


## Response Assessment
We assess six models' responses (GPT-4, ChatGPT, Claude, LLaMA-2, Vicuna, ChatGLM2) from two levels.
* Harmfulness: whether a response is harmful (a binary label).
* Action category: responses are categorized into six distinct groups, each representing a specific response type. 

![action](assets/action.png)


### Human Evaluation
High percentage of safe responses across five risk areas for six models demonstrates that they are basically safe. 
LLaMA-2 ranks the first, followed by ChatGPT, Claude, GPT-4, and Vicuna, with ChatGLM2 ranking the last by 85 harmful responses among 939.

* Harmlessness Rank 

![harmful_num](assets/harmful_num.png)


* Action Category Distribution
* 
![action_distribution](assets/action_dist.png)


### Automatic Evaluation
Longformer evaluators achieve comparable results with human and GPT-4. 
* GPT-4 evaluation
* Fine-tuned Longformer classifier (600M) 

| Model          |   Human |   GPT-4 |   Longformer |
|:---------------|--------:|--------:|-------------:|
| LLaMA-2        |    99.7 |    99.4 |         99.3 |
| ChatGPT        |    98.5 |    97.7 |         97.9 |
| Claude         |    98.3 |    98.3 |         97.6 |
| GPT-4          |    97.6 |    96.5 |         97.2 |
| vicuna         |    94.5 |    94.9 |         95.0 |
| ChatGLM2       |    90.9 |    92.9 |         92.9 |

## Citation
If our work is useful for your own, you can cite us with the following BibTex entry:
```bibtex
@misc{wang2023donotanswer,
    author = {Wang, Yuxia, and 
        Li, Haonan and 
        Han, Xudong and 
        Nakov, Preslav 
        and Baldwin, Timothy},
    title = {Do-Not-Answer: A Dataset for Evaluating Safeguards in LLMs},
    year = {2023},
    howpublished = {arXiv preprint arXiv:2308.13387},
}
```
## License
All datasets in this repository are released under the
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/). All source files in this repository are released under the Apache 2.0 license, the text of which can be found in the LICENSE file.