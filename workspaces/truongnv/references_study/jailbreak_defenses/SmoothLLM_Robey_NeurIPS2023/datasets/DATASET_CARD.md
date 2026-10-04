# Dataset card — SmoothLLM behavior inputs

Two JSON behavior-input files are retained: `llama2_behaviors.json` and `vicuna_behaviors.json`. Each contains 10 records. Their Git blob IDs and SHA-256 hashes match the official repository at pinned commit `e0610114b3c2f54353e9900918ff3be2812586de`.

The upstream README identifies these as author-released GCG adversarial-suffix behavior inputs. These are not predictions or defense outcomes. They cannot establish SmoothLLM recall or attack success without running the defense against a victim LLM and evaluating its responses.

The derived project microbenchmark and its timing results were removed because its runner did not call a victim model. See [`DATASET_PROVENANCE.md`](DATASET_PROVENANCE.md).
