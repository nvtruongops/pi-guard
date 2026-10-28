# Prompt Injection Detection Dataset

![Prompt Injection Detection Dataset](prompt_injection_detection_dataset-01.png)

## Dataset Overview

A synthetic dataset for prompt injection detection. The task is binary. Each
prompt is benign or malicious.

The label depends on what an instruction tries to do. An instruction that tries
to hijack the model, such as making it ignore its task or print its hidden
setup, is malicious. A normal request, or plain content, is benign. The label
does not depend on which words a prompt uses or where the instruction sits. The
test set measures whether a model handles new attacks, not whether it memorised
old ones.

## Design goal

Many prompt injection datasets are easy. A simple model detects trigger words 
such as ignore or override, making benchmark results unreliable. This
dataset removes that shortcut. The attack types here are known in the field. The
contribution is the labelled data and an evaluation that holds out unseen
attacks.

## How the data resists shortcuts

1. **Intent, not location.** Malicious and legitimate instructions can appear in the same parts of a prompt. Therefore, location alone cannot distinguish them.

2. **Shared words.** Benign rows reuse attack words such as *ignore*, *disregard*, *forget*, and *override* in safe human contexts. For example, "Please disregard the old schedule and use the times below" is benign. Therefore, word counting cannot rely on these words alone.

3. **Held-out test by construction.** The test split contains documents, attack lines, and entire attack types that do not appear in the training split. Encoded and multilingual attacks appear only in the test split, encouraging evaluation on unseen attacks rather than memorized templates.

## Train-test split

Train on `split == "train"`. Test on `split == "test"`. Never report a random
split. A random split lets the model see the same templates in train and test,
which can push the score close to 100%. The held-out split provides a realistic measure 
of performance.

The test holds out:
- unseen documents and unseen attack lines for the carrier categories,
- whole unseen attack types: obfuscation (base64, hex, rot13, leet, reversed),
  payload splitting, and a small multilingual sample.

## Files

- `prompt_injection_dataset.csv`: full dataset with labels, categories, and split column.
- `generate_dataset.py`: script used to generate the dataset.
- `LICENSE`: CC BY 4.0.

## Dataset Summary

- Rows: 5,441
- Label balance: 2,813 malicious and 2,628 benign
- Split: 4,212 train and 1,229 test
- Test-only categories: multilingual, obfuscation, and payload_split
- The dataset has 5,441 prompts across 16 categories. The plot shows 17 bars because multilingual is split into benign and malicious.

## Columns

| column | meaning |
|---|---|
| id | row id, like pi_00001 |
| prompt | the input text |
| label | benign or malicious |
| category | fine-grained type |
| technique | the construction method |
| language | en, or xx for the small non-English sample |
| split | train or test (test holds out unseen shapes and types) |
| char_len | character count |

## Categories

Malicious: indirect_injection (hijack inside the document), appended_override
(hijack after the document), authority, direct_override, persona_jailbreak,
fake_system, obfuscation, payload_split.

Benign: carrier_clean (a task tweak after the document), embedded_human (a human
instruction inside the document), qa, task, chitchat, hard_negative, security_qa.

Mixed by label: multilingual (both classes, small).


## License

This dataset is released under the CC BY 4.0 License. Please cite it if you use it.

## Citation

Mirza Akhi. (2026). *Prompt Injection Detection Dataset* (Version 1.0). Zenodo. https://doi.org/10.5281/zenodo.20817277
