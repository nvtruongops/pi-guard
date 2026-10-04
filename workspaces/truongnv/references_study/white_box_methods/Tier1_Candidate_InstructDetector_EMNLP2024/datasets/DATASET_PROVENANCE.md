# Dataset provenance — InstructDetector

No project-authored evaluation subset is retained. The prior local `bipia_text_eval.json` and `bipia_code_eval.json` files could not be verified row by row against the official BIPIA files or the paper’s evaluation split; both copies and their dependent proxy outputs were removed on 2026-09-29.

Upstream references: https://github.com/microsoft/BIPIA and https://github.com/MYVAE/Instruction-detection. The upstream paper is Wen et al., Findings of EMNLP 2025, DOI `10.18653/v1/2025.findings-emnlp.1060`. The former local TF-IDF model did not implement InstructDetector’s hidden-state/gradient method.
