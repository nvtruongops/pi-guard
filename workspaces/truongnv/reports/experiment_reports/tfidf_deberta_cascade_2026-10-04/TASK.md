# Task — TF-IDF → DeBERTa Cascade Experiment

## Scope Boundary Declaration

- **Source:** the user's instruction in this conversation to stop searching for a paper with this exact architecture and move to implementing and evaluating a TF-IDF → DeBERTa design.
- **IN-SCOPE:** finish the resumable seed-42 DeBERTa-v3 PIDS-Bench author-code run; implement an experimental confidence-gated TF-IDF → DeBERTa cascade outside the product source tree; evaluate TF-IDF alone, DeBERTa alone, and the cascade on the same pinned PIDS-Bench validation/test/OOD files; publish metrics, routing counts, provenance, and a comparison matrix.
- **OUT-OF-SCOPE:** further searches for a paper proposing this exact cascade; mixing other papers' datasets/checkpoints into the local matrix; reopening withdrawn Meeting 6 D1–D6 artifacts; three-class or production claims; deployment/SLA claims not measured by this experiment; INT8, ONNX, or ZeroQuant.

## Experimental protocol

- Use pinned PIDS-Bench author commit `87dc835566b930ee921240874a4939b2c266c2fe` and its checksum-verified binary splits.
- Reuse the completed author-source TF-IDF+LR seed-42 checkpoint and resume the author-source DeBERTa-v3 seed-42 training from durable checkpoint 3,388, preserving the original training settings and frozen train/validation/test split.
- Treat TF-IDF and DeBERTa as standalone references and the cascade as a separate local experimental method. The TF-IDF score routes confident cases directly; uncertain cases go to DeBERTa.
- Select standalone and cascade operating thresholds using validation only, maximizing attack recall subject to validation benign FPR ≤ 1.5%; among equally scoring cascade policies, prefer fewer DeBERTa calls. Retain fixed-threshold 0.5 results as a separate reference.
- Report held-out IID, hard-benign, obfuscated-attack, domain-OOD, and structural-OOD results. Preserve row-level predictions, counts, source/checkpoint/data hashes, and routing fractions. Report unavailable values as N/A.
- A single seed-42 experiment is evidence for this run only; do not generalize it as a multi-seed result or claim the project KPI is achieved.

