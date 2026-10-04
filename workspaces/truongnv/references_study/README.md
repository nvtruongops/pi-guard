# References study and supporting research assets

**Audit date:** 2026-10-02. This area holds useful public research code/data that is not currently a comparable, runnable external text-classifier experiment for the PI-Guard benchmark.

## Scope Boundary Declaration

- **IN-SCOPE:** reference models, attack/evaluation harnesses, historical project pilots, and caches used only by those reference runners.
- **OUT-OF-SCOPE:** claiming a moved artifact as a completed reproduction, restoring withdrawn synthetic/unmapped probes, or modifying the historical Meeting 6 record.

## Directory map

```text
references_study/
├── encoder_architectures/ModernBERT_Warner_2024/
├── encoder_architectures/BERT_from_scratch_UmarJamil_2023/
├── encoder_architectures/HuggingFace_DeBERTa_SequenceClassification/
├── harnesses/JailbreakBench_Chao_NeurIPS2024/
├── jailbreak_defenses/SmoothLLM_Robey_NeurIPS2023/
├── jailbreak_defenses/Jain_NeurIPS2023/
├── rejected_baselines/Tier1_REJECTED_Ayub_CAMLIS2024/
└── white_box_methods/Tier1_Candidate_InstructDetector_EMNLP2024/
```

## Model and method references

| Asset | What its public material supports | Why it is reference-only here |
|---|---|---|
| [`SmoothLLM_Robey_NeurIPS2023`](./jailbreak_defenses/SmoothLLM_Robey_NeurIPS2023/) | Behavior inputs and randomized-smoothing code. The two retained JSON files are byte-identical to the files in the bundled `upstream/data/GCG/` snapshot (10 records each; hashes recorded in the local provenance report). | The evaluated outcome depends on a victim LLM's response/attack success; these inputs do not measure external text-classifier recall or defense effectiveness. [Author repository](https://github.com/arobey1/smooth-llm). |
| [`Jain_NeurIPS2023`](./jailbreak_defenses/Jain_NeurIPS2023/) | Paper gốc và mã nguồn chính thức của tác giả cho baseline lọc perplexity và paraphrase (NeurIPS 2023; arXiv:2309.00614). | Giữ làm tài liệu tham khảo phương pháp và code chuẩn. Toàn bộ pilot tự dựng cũ (runner TF-IDF, dữ liệu tự ghép, biểu đồ/báo cáo) đã bị xóa ngày 2026-10-02; không báo cáo như mô hình tái lập của PI-Guard. [Official code](https://github.com/neelsjain/baseline-defenses), [paper](https://arxiv.org/abs/2309.00614). |
| [`Tier1_Candidate_InstructDetector_EMNLP2024`](./white_box_methods/Tier1_Candidate_InstructDetector_EMNLP2024/) | Official instruction-detection implementation; BIPIA is a public benchmark. The folder suffix is a legacy path label; the paper was published in Findings of EMNLP 2025. [Paper](https://aclanthology.org/2025.findings-emnlp.1060/). | The paper method probes internal model representations/gradients. The old project adapter fitted TF-IDF and was not InstructDetector; local subsets/results were withdrawn. [Method code](https://github.com/MYVAE/Instruction-detection), [BIPIA](https://github.com/microsoft/BIPIA). |
| [`ModernBERT_Warner_2024`](./encoder_architectures/ModernBERT_Warner_2024/) | Public encoder architecture, pretraining code, and model checkpoints. | No prompt-injection classifier or public prompt-injection evaluation dataset was found in this package. [Official code](https://github.com/AnswerDotAI/ModernBERT). |
| [`BERT_from_scratch_UmarJamil_2023`](./encoder_architectures/BERT_from_scratch_UmarJamil_2023/) | BERT/Transformer foundations, plus high-level fine-tuning and text-classification examples. | Theory-only BERT slides; no DeBERTa-v3 details or executable training/evaluation recipe, and not evidence PI-Guard trained a model. The deck states CC BY-NC 4.0 and links to [Umar Jamil's source repository](https://github.com/hkproj/bert-from-scratch). |
| [`HuggingFace_DeBERTa_SequenceClassification`](./encoder_architectures/HuggingFace_DeBERTa_SequenceClassification/) | Official API references for DeBERTa and DeBERTa-v2 sequence-classification heads, including inputs, labels, loss, and outputs. | Saved HTML snapshots fetched 2026-10-02; check the online docs and target checkpoint configuration when implementing. [DeBERTa docs](https://huggingface.co/docs/transformers/model_doc/deberta), [DeBERTa-v2 docs](https://huggingface.co/docs/transformers/model_doc/deberta-v2). |

## Existing supplementary resources

- [`JailbreakBench_Chao_NeurIPS2024`](./harnesses/JailbreakBench_Chao_NeurIPS2024/) is a benchmark/harness. Behavior goals are not jailbreak artifacts; a classifier run on goals cannot be described as jailbreak-artifact recall. [Official project](https://github.com/JailbreakBench/jailbreakbench).
- [`Tier1_REJECTED_Ayub_CAMLIS2024`](./rejected_baselines/Tier1_REJECTED_Ayub_CAMLIS2024/) retains paper/code references and provenance documentation of source-data overlap with the PIGuard bundle; no local Ayub dataset JSON is retained. The withdrawn run had 200/344 training rows without a `source` value, so its scores, notebook, plots and caches were removed. Only the dataset card, provenance record and metadata remain in `datasets/`; the runner is disabled and no local Ayub metric is reportable.

## Reporting rule

Use `replications/` only for candidates with usable public detector/model material and a pinned, source-backed dataset protocol. Use this area for architecture/method references, harnesses, victim-LLM defenses, and project pilots that do not meet that comparison standard. The audit report records exact decisions and current limitations: [`replications_folder_audit_2026-09-30/`](../reports/experiment_reports/replications_folder_audit_2026-09-30/).
