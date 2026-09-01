---
name: capstone-thesis-and-defense
description: >-
  Academic writing assistant for FPT University Capstone Thesis report (IAP491 Research-Based Thesis, Chapters 1-6),
  LaTeX/Markdown structuring, IEEE citation formatting, and Graduation Defense presentation slide preparation for PI-Guard.
---

# Capstone Thesis & Defense Preparation Guide (FPT IAP491 Standard)

This skill guides the team in writing the formal **Capstone Graduation Thesis Report** and preparing the **Defense Presentation Slides** according to official FPT University IAP491 Research-Based Thesis guidelines.

> 📚 **Official FPT Template & Guidelines**: [`docs/fpt_capstone_guide/IAP491_CP_StudentsGuideForm for Research Based Thesis.docx`](file:///d:/Work/Do-an/docs/fpt_capstone_guide/IAP491_CP_StudentsGuideForm%20for%20Research%20Based%20Thesis.docx)  
> 📑 **Full Rubrics & Timeline Breakdown**: [`docs/thesis/FPT_IAP491_Capstone_Guidelines_and_Rubrics_Summary.md`](file:///d:/Work/Do-an/docs/thesis/FPT_IAP491_Capstone_Guidelines_and_Rubrics_Summary.md)  
> 📂 **17 Standard Research Papers (100% >= 2022)**: [`References/REFERENCES_LOG.md`](file:///d:/Work/Do-an/References/REFERENCES_LOG.md)  

---

## 1. Official FPT IAP491 Thesis Structure (6 Chapters)

### Chapter 1: Introduction (Report No.1 - 10% Process Mark)
- **1.1 Background**: Rise of LLM applications, OWASP Top 10 for LLM (LLM01: Prompt Injection), failure of rule-based keyword filters.
- **1.2 Problem Statement**: Vulnerabilities of Prompt Injection and Jailbreaks, Flat Data/Instruction boundaries in Transformer self-attention.
- **1.3 Research Objectives**: Build a proactive, low-latency, low-FPR ML guardrail classifier.
- **1.4 Significance of the Study**: Enterprise LLM security, preventing System Prompt leaks, data theft, and compute resource abuse.
- **1.5 Scope and Limitations**: Focus on direct text input guardrail layer for English prompts (with obfuscation resilience).
- **1.6 Thesis Structure**: Roadmap of the 6 chapters.

### Chapter 2: Literature Review (Report No.2 - 25% Process Mark)
- **2.1 Review of Previous Studies**:
  - Prompt Injection & Jailbreak Taxonomies (Perez 2022, Greshake 2023, Wei 2024, Shen 2024 ACM CCS).
  - Existing Guardrails: ProtectAI DeBERTa, Lakera Gandalf, Meta Llama Guard 3, NVIDIA NeMo Guardrails.
  - NLP Techniques: TF-IDF, N-grams, BERT, RoBERTa, DeBERTa-v3 (He et al. 2021).
  - Adversarial Attacks & Evasion: EasyJailbreak (Zhou 2024), GCG (Zou 2023), SmoothLLM (Robey 2023).
- **2.2 Summary of the Literature Review**: Comparative synthesis matrix.
- **2.3 Contribution of Research**: Hybrid ML + DeBERTa-v3 ONNX INT8 architecture achieving P95 latency < 15ms and FPR < 1.1%.

### Chapter 3: Methodology (Report No.3 - 20% Process Mark)
- **3.1 Research Design**: 2-Phase architecture (Offline Training Pipeline & Online Runtime Middleware).
- **3.2 Data Collection Methods**: Multi-source curation (Deepset, Gandalf, In-The-Wild Shen 2024, OpenOrca Benign), deduplication.
- **3.3 Sampling & Data Analysis Techniques**:
  - Group-Aware Splitting (cluster_id) to eliminate Data Leakage between train/val/test splits.
  - Baseline ML: Hybrid Word/Char TF-IDF + Logistic Regression / LinearSVC / XGBoost.
  - Deep Learning: Supervised Fine-Tuning of `microsoft/deberta-v3-base` + Dynamic INT8 ONNX Quantization.
- **3.4 Limitations of the Methodology**: English text focus, reliance on labeled datasets.

### Chapter 4: Experimental and Results (Report No.4 - 25% Process Mark)
- **4.1 Introduction & Setup**: Hardware specs (CPU/GPU), software stack, hyperparameter tables.
- **4.2 Presentation of Data**: Data distribution, class balance, semantic clusters.
- **4.3 Analysis of Results**: Baseline ML vs DeBERTa-v3 vs SOTA ProtectAI (Accuracy, Precision, Recall, F1, FPR, ROC-AUC).
- **4.4 Interpretation of Results**: Confusion matrix analysis, threshold calibration curves.
- **4.5 Comparison with Literature**: Latency and resource comparison against Llama Guard 3 (8B) and NeMo Guardrails.
- **4.6 Implications of the Results**: Robustness stress testing against Leetspeak, Base64, Spaced text, and GCG suffixes.

### Chapter 5: Discussion (Report No.5 - 15% Process Mark)
- **5.1 Restate the Research Problem or Objectives**.
- **5.2 Summarize Key Findings**: Meeting all target metrics (P95 Latency < 15ms on CPU, FPR < 1.1%, F1 > 0.98).
- **5.3 Security Implications & Trade-offs**: Balances Security vs Usability (over-defense prevention).
- **5.4 Practical Limitations & Challenges**: Handling multilingual inputs, token length limitations.

### Chapter 6: Conclusion and Future Work (Report No.6 - 5% Process Mark)
- **6.1 Conclusion**: Summary of technical contributions and engineering deliverables.
- **6.2 Future Work**: Multimodal injection detection (Vision-Language Models), Agent tool-call sandboxing, online continuous learning.

---

## 2. Process Mark vs. Defense Presentation Mark

$$\text{Final Project Mark} = (\text{Process Mark } [6 \text{ Reports}] \times 50\%) + (\text{Presentation Mark } [\text{Committee}] \times 50\%)$$

---

## 3. Defense Slide Structure (15 - 20 Minutes Presentation)

| Slide # | Title | Presenter | Core Content |
| :--- | :--- | :--- | :--- |
| 1 | Title Slide | Leader (Trường) | Project Name, Team Members, Supervisor, FPT University |
| 2 | Motivation & Threat Context | Leader (Trường) | OWASP LLM01, rise of LLM attacks, loss of System Prompt IP |
| 3 | Project Objectives & Scope | Leader (Trường) | Target metrics: 2 core keys, P95 < 30ms, FPR < 1.5%, F1 > 0.95 |
| 4 | Threat Model & 3-Tier Defense | Đức | NIST / Tencent Threat Model, 3-Tier Defense-in-Depth |
| 5 | Dataset Curation & Leakage Prevention | Trường | HF Datasets, Group-Aware Splitting, Class balancing |
| 6 | Classical ML Baseline | Đức | Hybrid Word/Char TF-IDF + Classifier training & results |
| 7 | Transformer Fine-Tuning & Quantization | Việt | DeBERTa-v3 architecture, Supervised Fine-Tuning, ONNX INT8 |
| 8 | Comparative Results & Robustness | Việt | Baseline vs DeBERTa vs SOTA table, Leetspeak/Base64 stress tests |
| 9 | 4-Scenario Live Demo | Phương | FastAPI Guardrail + Streamlit blocking Injection & Jailbreak in <15ms |
| 10 | Conclusion & Future Work | Phương | Summary of contributions and future research directions |
| 11 | Q&A | All Team | Answering Council Questions |
