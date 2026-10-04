# SmoothLLM reference package — provenance status

- **Public repository:** [arobey1/smooth-llm](https://github.com/arobey1/smooth-llm).
- **Local data comparison:** `llama2_behaviors.json` and `vicuna_behaviors.json` each have the same SHA-256 as the corresponding file in the bundled `upstream/data/GCG/` snapshot. See [`DATASET_PROVENANCE.md`](../datasets/DATASET_PROVENANCE.md).
- **Revision limitation:** the local snapshot does not record a Git commit, so this is local copy-equality evidence, not a pinned remote-revision check.
- **Result status:** the project-authored flattened microbenchmark and timing outputs were withdrawn. These behavior inputs alone are not a SmoothLLM defense evaluation because the previous runner did not invoke a victim LLM.

No SmoothLLM recall, ASR reduction, or latency result is reportable from this package.
