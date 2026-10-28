---
language:
- en
license: mit
size_categories:
- 1K<n<10K
dataset_info:
  features:
  - name: text
    dtype: string
  - name: similarity
    dtype: float64
  splits:
  - name: train
    num_bytes: 66400
    num_examples: 777
  - name: validation
    num_bytes: 9633
    num_examples: 111
  - name: test
    num_bytes: 9747
    num_examples: 112
  download_size: 51515
  dataset_size: 85780
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train-*
  - split: validation
    path: data/validation-*
  - split: test
    path: data/test-*
tags:
- prompt injection
---


# gandalf_ignore_instructions

![](https://gandalf.lakera.ai/level-images/word-blacklist.jpg)

This is a dataset of prompt injections from [Gandalf](https://gandalf.lakera.ai/) by [Lakera](https://www.lakera.ai/).

Note that we might update the dataset occasionally by cleaning the data or adding more samples.

## How the data was obtained

There are millions of prompts and many of them are not actual prompt injections (people ask Gandalf all kinds of things).

We used the following process to obtain relevant data:
- Start with all prompts submitted to Gandalf in July 2023.
- Use [OpenAI text embeddings](https://platform.openai.com/docs/guides/embeddings/what-are-embeddings) (`text-embedding-ada-002`) to compute the similarity between the prompts and the phrase "Ignore all previous instructions".
- Filter to those prompts that have similarity of at least 0.825.
- Use [Lakera Guard](https://platform.lakera.ai/docs)'s personally identifiable  information detector to filter out prompts that potentially contain PII data.
- Remove near-duplicates from the data (prompts that differ only by a few letters) using an approximate algorithm. This helps reduce leakage between the data splits.
- Sample 1000 prompts.
- Split the data into train-val-test with an 80/10/10 ratio. Each sample is assigned independently so the size of the train split is not _exactly_ 80% and so on.

Note that there is a small amount of noise in the data since an automatic method was used to obtain it: a few of the samples might not be real prompt injections.

## Citation

If you use this dataset in your research, please cite our paper introducing the game [Gandalf the Red: Adaptive Security for LLMs](https://arxiv.org/abs/2501.07927):

```
@article{gandalf_paper,
  title={Gandalf the Red: Adaptive Security for LLMs},
  author={Pfister, Niklas and Volhejn, V{\'a}clav and Knott, Manuel and Arias, Santiago and Bazi{\'n}ska, Julia and Bichurin, Mykhailo and Commike, Alan and Darling, Janet and Dienes, Peter and Fiedler, Matthew and others},
  journal={arXiv preprint arXiv:2501.07927},
  year={2025}
}
```

## Licensing Information

gandalf_ignore_instructions is distributed under the [MIT License](https://opensource.org/license/mit/).