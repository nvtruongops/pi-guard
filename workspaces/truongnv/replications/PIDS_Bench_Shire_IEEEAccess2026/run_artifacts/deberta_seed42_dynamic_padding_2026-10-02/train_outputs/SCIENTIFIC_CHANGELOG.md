# Scientific changelog

- No files under the pinned upstream checkout were edited in this task. Its only existing working-tree change is a prior two-line TF-IDF safeguard that excludes license-redacted null hard-benign rows and records the count; it was preserved.
- The staged hard-benign file excludes exactly 664 blank/redacted text rows. All other staged evaluation inputs and train/validation/test files remain byte-identical to the frozen source data. Therefore local hard-benign rates use `n=808` and are not directly comparable with the paper's full `n=1,472` results.
- Local DeBERTa uses dynamic batch padding rather than fixed padding. Every example is unchanged, remains truncated at 512 tokens, and retains the same attention mask on non-padding tokens; training remains FP32, 3 epochs, seed 42, effective batch 16, and the source optimizer/loss.
- A single local seed does not estimate run-to-run variance. Published multi-seed results remain attributed to the paper, not this run.
- No cascade, latency, P95, or achieved system FPR claim is produced.
