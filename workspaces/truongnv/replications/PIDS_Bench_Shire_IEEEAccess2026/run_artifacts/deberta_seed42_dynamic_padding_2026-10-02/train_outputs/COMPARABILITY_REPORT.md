# Comparability

- **Source pairing:** TF-IDF+LR, DistilBERT, and DeBERTa-v3-FT are the in-repository learned baselines from the same PIDS-Bench release and task. The transformers are fine-tuned from `distilbert-base-uncased` and `microsoft/deberta-v3-base`, respectively. DistilBERT is a comparator, not a proposed cascade tier.
- **Code/data:** author repository commit `87dc835566b930ee921240874a4939b2c266c2fe`; source data checksums match the release freeze manifest. Thresholds are derived only from `val.csv` by the same 501-point F1 grid.
- **Threshold conventions:** report fixed `τ=0.5` metrics separately from validation-F1-selected metrics. Do not compare a fixed-threshold value for one model with a tuned-threshold value for the other.
- **Evaluation pairing:** both models score IID test, unredacted hard-benign, obfuscated attacks, domain OOD, and structural OOD. Hard-benign comparisons use only the 808 retained rows.
- **Limits:** local DeBERTa is one seed with a recorded dynamic-padding adaptation. It is evidence for baseline behavior, not a five-seed reproduction, a cascade experiment, or proof of deployment latency/FPR targets.

Official references: [PIDS-Bench paper](https://doi.org/10.1109/ACCESS.2026.3728186), [pinned author repository](https://github.com/ShirePyDev/Prompt-Injection-Detection-System/tree/87dc835566b930ee921240874a4939b2c266c2fe), and [DeBERTa-v3-base model card](https://huggingface.co/microsoft/deberta-v3-base).
