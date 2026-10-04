# Dataset provenance — SmoothLLM behavior inputs

The two retained JSON files match the official `arobey1/smooth-llm` repository at commit `e0610114b3c2f54353e9900918ff3be2812586de`. Their Git blob IDs were checked against the repository history and their SHA-256 values match the files served from that commit. The author README describes the `data/` files as ten adversarial suffixes generated with GCG for Vicuna and Llama 2. They are source-authored attack inputs, not project-generated prompts or detector outputs.

| Retained file | Records | SHA-256 | Pinned upstream file |
|---|---:|---|---|
| `llama2_behaviors.json` | 10 | `f96d53e113bb3b839c6d0c9d4b2f3ab611e5b8fb4fd4a1cc68fb852f271cf286` | [`data/GCG/llama2_behaviors.json`](https://github.com/arobey1/smooth-llm/blob/e0610114b3c2f54353e9900918ff3be2812586de/data/GCG/llama2_behaviors.json) |
| `vicuna_behaviors.json` | 10 | `7396b50e123775b7d7080b2c475240401fb8e41ff1f91f9d0491663a01cb4ead` | [`data/GCG/vicuna_behaviors.json`](https://github.com/arobey1/smooth-llm/blob/e0610114b3c2f54353e9900918ff3be2812586de/data/GCG/vicuna_behaviors.json) |

The flattened project microbenchmark and dependent timing output were removed on 2026-09-29 because the prior runner did not invoke a victim LLM. Behavior goals alone do not provide defense-recall or attack-success measurements. See [`DATASET_CARD.md`](DATASET_CARD.md) and the [reference package status](../README.md).
