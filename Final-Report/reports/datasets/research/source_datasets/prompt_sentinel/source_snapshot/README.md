---
dataset_info:
  features:
  - name: id
    dtype: string
  - name: text
    dtype: string
  - name: label
    dtype: string
  - name: label_id
    dtype:
      class_label:
        names:
          '0': benign
          '1': jailbreak
          '2': injection
  - name: is_attack
    dtype: bool
  - name: harmful
    dtype: bool
  - name: role
    dtype: string
  - name: source_dataset
    dtype: string
  - name: all_sources
    dtype: string
  - name: source_config
    dtype: string
  - name: source_split
    dtype: string
  - name: source_license
    dtype: string
  - name: source_url
    dtype: string
  - name: n_chars
    dtype: int64
  - name: template_group
    dtype: string
  splits:
  - name: train
    num_bytes: 84385011
    num_examples: 116854
  - name: validation
    num_bytes: 10358317
    num_examples: 14335
  - name: test
    num_bytes: 10495155
    num_examples: 14592
  download_size: 45203696
  dataset_size: 105238483
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train-*
  - split: validation
    path: data/validation-*
  - split: test
    path: data/test-*
task_categories:
- text-classification
pretty_name: PromptSentinel
license: other
tags:
- jailbreak
- prompt-injection
- llm-security
- guardrails
- red-teaming
- safety
language:
- en
- de
---
# PromptSentinel 🛡️

A combined, cleaned and deduplicated dataset for training **lightweight detectors of jailbreak and
prompt-injection attempts** against LLMs, built from 13 public datasets. All credit goes to their authors (see below).

> ⚠️ Contains real adversarial prompts, some of which include harmful requests. Intended for building
> **defensive classifiers, guardrails and red-team evaluation**. Access is gated. Model responses from source
> datasets were deliberately **not** included.

## Labels

| label | id | meaning |
|---|---|---|
| `benign` | 0 | Normal prompts, including hard negatives: role-play ("act as…"), long system prompts, adversarially-phrased but harmless requests |
| `jailbreak` | 1 | Attempts to make the model ignore its safety rules (DAN, persona tricks, hypothetical framing, obfuscation…) |
| `injection` | 2 | Attempts to override the developer's or system instructions ("ignore previous instructions and…") |

**Direct harmful requests without any trick are labelled `benign` for attack type**: that's a content-moderation
problem, not a jailbreak. Where the source provides it, the `harmful` column flags them, so you can train both tasks.

## Stats

156,802 unique prompts: benign 90,175 · jailbreak 1,766 · injection 64,861

| split | rows | benign | jailbreak | injection |
|---|---|---|---|---|
| train | 116,854 | 66,024 | 1,019 | 49,811 |
| validation | 14,335 | 8,168 | 111 | 6,056 |
| test | 14,592 | 8,266 | 134 | 6,192 |

## How it was built

1. Loaded 13 source datasets and mapped their labels to the 3-class scheme above.
2. Dropped all model-response columns and kept prompts only.
3. Normalized whitespace and removed texts under 8 or over 20,000 characters.
4. **Exact deduplication** across all sources on normalized text; `all_sources` lists every dataset a prompt appeared in.
5. Resolved label conflicts by majority vote; ties dropped.
6. **Split by template family** (hash of the normalized first 200 characters), so variants of the same jailbreak
   template (e.g. DAN versions) never leak between train and test.

## Columns

`id`, `text`, `label`, `label_id`, `is_attack`, `harmful` (bool or null), `source_dataset`, `all_sources`,
`source_config`, `source_split`, `source_license`, `source_url`, `n_chars`, `template_group`

```python
from datasets import load_dataset
ds = load_dataset("nuhmanpk/prompt-sentinel")
```

## Credits & sources

This dataset is a **compilation**. All prompts come from the datasets below; please cite and credit the original authors.

| Dataset | Author | License | Rows used | Papers | Contribution |
|---|---|---|---|---|---|
| [TrustAIRLab/in-the-wild-jailbreak-prompts](https://huggingface.co/datasets/TrustAIRLab/in-the-wild-jailbreak-prompts) | [TrustAIRLab](https://huggingface.co/TrustAIRLab) | mit | 14,040 | train | [arXiv:2308.03825](https://arxiv.org/abs/2308.03825) | In-the-wild jailbreak and regular prompts from Reddit, Discord, websites and prompt communities. |
| [lmsys/toxic-chat](https://huggingface.co/datasets/lmsys/toxic-chat) | [lmsys](https://huggingface.co/lmsys) | cc-by-nc-4.0 | 9,516 | train | [arXiv:2310.17389](https://arxiv.org/abs/2310.17389) | Real user queries with human toxicity and jailbreaking annotations. |
| [jackhhao/jailbreak-classification](https://huggingface.co/datasets/jackhhao/jailbreak-classification) | [jackhhao](https://huggingface.co/jackhhao) | apache-2.0 | 636 | train | — | Jailbreak vs benign prompt classification. |
| [reshabhs/SPML_Chatbot_Prompt_Injection](https://huggingface.co/datasets/reshabhs/SPML_Chatbot_Prompt_Injection) | [reshabhs](https://huggingface.co/reshabhs) | mit | 15,910 | train | [arXiv:2402.11755](https://arxiv.org/abs/2402.11755) | User prompts against chatbot system prompts, labelled for injection. |
| [jayavibhav/prompt-injection](https://huggingface.co/datasets/jayavibhav/prompt-injection) | [jayavibhav](https://huggingface.co/jayavibhav) | unspecified | 79,673 | train | — | Large prompt-injection vs benign set (capped). |
| [S-Labs/prompt-injection-dataset](https://huggingface.co/datasets/S-Labs/prompt-injection-dataset) | [S-Labs](https://huggingface.co/S-Labs) | mit | 15,095 | train | — | Injection vs benign with deliberate hard negatives (security questions, trigger words in benign context). |
| [neuralchemy/Prompt-injection-dataset](https://huggingface.co/datasets/neuralchemy/Prompt-injection-dataset) | [neuralchemy](https://huggingface.co/neuralchemy) | apache-2.0 | 5,925 | train | — | Categorised injection and jailbreak prompts (original, non-augmented rows only). |
| [Lakera/gandalf_ignore_instructions](https://huggingface.co/datasets/Lakera/gandalf_ignore_instructions) | [Lakera](https://huggingface.co/Lakera) | mit | 996 | train | [arXiv:2501.07927](https://arxiv.org/abs/2501.07927) | Real prompt-injection attempts from Lakera's Gandalf game. |
| [fka/awesome-chatgpt-prompts](https://huggingface.co/datasets/fka/awesome-chatgpt-prompts) | [fka](https://huggingface.co/fka) | cc0-1.0 | 1,970 | train | — | Benign role-play / 'act as' prompts (hard negatives). |
| [OpenAssistant/oasst2](https://huggingface.co/datasets/OpenAssistant/oasst2) | [OpenAssistant](https://huggingface.co/OpenAssistant) | apache-2.0 | 5,255 | train | [arXiv:2304.07327](https://arxiv.org/abs/2304.07327) | Real human-written first messages (English), benign. |
| [leolee99/NotInject](https://huggingface.co/datasets/leolee99/NotInject) | [leolee99](https://huggingface.co/leolee99) | mit | 255 | benchmark | [arXiv:2410.22770](https://arxiv.org/abs/2410.22770) | Over-defense benchmark: benign prompts containing injection trigger words. |
| [deepset/prompt-injections](https://huggingface.co/datasets/deepset/prompt-injections) | [deepset](https://huggingface.co/deepset) | apache-2.0 | 503 | benchmark | — | Widely used prompt-injection benchmark (EN/DE). |
| [xTRam1/safe-guard-prompt-injection](https://huggingface.co/datasets/xTRam1/safe-guard-prompt-injection) | [xTRam1](https://huggingface.co/xTRam1) | unspecified | 7,028 | benchmark | [arXiv:2402.13064](https://arxiv.org/abs/2402.13064) | Prompt-injection vs benign benchmark. |

Licenses were read from each dataset's Hub metadata. **Some sources are non-commercial or share-alike**, and each row's
`source_license` tells you which terms apply. Filter by it if you need a commercially usable subset.

Sources attempted but not included in this build: allenai/wildjailbreak, allenai/wildguardmix, hackaprompt/hackaprompt-dataset, qualifire/prompt-injections-benchmark, allenai/wildguardmix

## Limitations

- Label schemes differ between sources; mapping to 3 classes involves judgment calls (documented in the build notebook).
- Mostly English (some German via deepset/prompt-injections).
- Near-duplicate variants beyond the template-family grouping may remain.
- Jailbreak techniques evolve fast, so detectors trained on this will miss novel attacks. Refresh periodically.

## Author

Compiled by **Nuhman PK**: [🤗 Hugging Face](https://huggingface.co/nuhmanpk) · [💻 GitHub](https://github.com/nuhmanpk) ·
[📊 Kaggle](https://www.kaggle.com/nuhmanpk) · [💼 LinkedIn](https://www.linkedin.com/in/nuhmanpk) ·
[🐦 X](https://twitter.com/pk__nuhman) · [✍️ Medium](https://medium.com/@nuhmanpk)
