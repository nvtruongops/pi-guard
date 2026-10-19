**CAPSTONE PROJECT REGISTER**

**Class:** …………………………          Duration time: from …/…/…… to …/…/……

**(\*) Profession:** Information Assurance        Specialty:  ☐ ES     ☒IS    ☐ JS

**(\*) Kinds of person make registers:**   ☐ Lecturer      ☒ Students

**1\. Register information for supervisor (if have)**

|  | Full name | Phone | E-Mail | Title |
| ----- | ----- | ----- | ----- | ----- |
| **Supervisor 1** |  |  |  |  |
| **Supervisor 2** |  |  |  |  |

**2\. Register information for students (if have)**

|  | Full name | Student code | Phone | E-mail | Role in Group |
| ----- | ----- | ----- | ----- | ----- | ----- |
| **Student 1** | Nguyễn Văn Trường | SE182034 | 0764648648 | truongnvse182034@fpt.edu.vn | Leader |
| **Student 2** | Nguyễn Quí Đức | SE182087 | 0792377803 | ducnqse182087@fpt.edu.vn | Member |
| **Student 3** | Phạm Minh Hoàng Việt | SE181851 | 0976236132 | vietpmhse181851@fpt.edu.vn | Member |
| **Student 4** | Đỗ Đoàn Duy Phương | SE180235 | 0983394370 | phuongdddse180235@fpt.edu.vn | Member |

**3\. Register content of Capstone Project**

**(\*) 3.1. Capstone Project name:**

**English:** A Machine-Learning Guardrail for Detecting Prompt Injection and Jailbreak Attacks on LLM Applications

**Vietnamese:** Xây dựng lớp bảo vệ (guardrail) dựa trên Học máy để phát hiện tấn công Prompt Injection và Jailbreak cho ứng dụng mô hình ngôn ngữ lớn (LLM)

**Abbreviation:** PI-Guard

**(\*) 3.2. Main proposal content (including result and product)**

**Theory and practice (document):**

**Introduction / Overview**

The rapid adoption of Large Language Model (LLM) applications such as chatbots and AI assistants has created an entirely new class of security vulnerability. In the OWASP Top 10 for LLM Applications, Prompt Injection is ranked as the number-one risk: attackers craft inputs that override the system's instructions, jailbreak its safety guidelines, extract the hidden system prompt, or bypass content moderation.

Rule-based filters are brittle — attackers evade them with obfuscation (leetspeak, base64, spacing tricks) and constantly invented new jailbreaks. Machine-Learning and NLP techniques can instead learn attack patterns and classify a user's prompt as benign or malicious before it ever reaches the LLM.

This project builds a defensive "guardrail": a classifier placed in front of an LLM that labels each incoming prompt as benign, prompt-injection, or jailbreak, and blocks or flags malicious prompts. The classifier is trained on public, labeled datasets, and results are shown on a dashboard. The goal is a protective filter for LLM applications, not an attack tool.

**Objective of the project**

General objective: Develop and implement an ML-based guardrail to proactively detect and mitigate prompt injection and jailbreak attacks in Large Language Model (LLM) applications.

**Specific objectives:**

* 1. Curate and label a comprehensive dataset of benign and malicious prompts from public sources.

* 2. Design, train, and evaluate various ML/NLP classifiers, including classical baselines and fine-tuned transformer models (e.g., BERT/DeBERTa), for prompt classification.

* 3. Integrate the trained classifier as an API-driven guardrail layer to effectively block or flag malicious prompts before they reach the LLM.

* 4. Conduct a thorough evaluation of the guardrail's performance, assessing detection accuracy, false-positive rates, and robustness against obfuscated and novel attack techniques.

**Program**

An ML-based guardrail for LLM applications: incoming prompts pass through a classifier that labels them benign, prompt-injection, or jailbreak; malicious prompts are blocked or flagged before reaching the LLM, and everything is reported on a dashboard.

**Data flow:** User Prompt → Guardrail (Preprocessing → Classifier) → Allow (to LLM) / Block \+ Alert → Dashboard.

**Main components:**

* **Preprocessing/Tokenization:** clean and encode the incoming prompt.

* **Feature Extraction:** TF-IDF for the baseline; transformer embeddings for the fine-tuned model.

* **Classifier:** a classical ML baseline plus a fine-tuned transformer (BERT/DeBERTa).

* **Guardrail API:** a FastAPI layer in front of an LLM that allows or blocks each prompt.

* **Alerting & Dashboard:** log blocked prompts and show statistics and model performance.

**Datasets and data sources (all public, from Hugging Face):**

* **deepset/prompt-injections:** a widely used benchmark of benign vs prompt-injection prompts.

* **jayavibhav/prompt-injection:** a large-scale labeled prompt-injection dataset (hundreds of thousands of samples).

* **xTRam1/safe-guard-prompt-injection:** benign vs injection prompts for guardrail training.

* **Lakera/gandalf\_ignore\_instructions:** real "ignore instructions" / jailbreak prompts from the Gandalf game.

* **TrustAIRLab/in-the-wild-jailbreak-prompts:** real-world jailbreak prompts collected from public platforms.

* **Benign prompts:** everyday legitimate prompts from open instruction/Q\&A datasets, used to balance the negative class.

The datasets are merged, de-duplicated, and split in a group-aware way (paraphrased variants kept together) to avoid data leakage. Existing guardrail models — such as ProtectAI's DeBERTa-v3 prompt-injection classifier — are used as reference baselines for comparison.

**Evaluation metrics:**

* Accuracy, precision, recall, and F1-score.

* False-positive rate on benign prompts (to measure over-defense).

* Robustness on obfuscated/evasion samples (leetspeak, base64, spacing tricks).

**Functional Requirement**

* **Prompt ingestion:** receive user prompts through an API.

* **Preprocessing & tokenization:** prepare prompts for classification.

* **ML/NLP classification:** label a prompt as benign, prompt-injection, or jailbreak.

* **Guardrail enforcement:** block or flag malicious prompts before the LLM.

* **Logging:** record blocked and suspicious prompts.

* **Dashboard:** show attack statistics, blocked prompts, and model performance.

**Tools/Platform**

* Programming language: Python

* ML/NLP: scikit-learn (TF-IDF baseline), Hugging Face Transformers (BERT/DeBERTa fine-tuning)

* Guardrail API: FastAPI

* LLM (demo target): an open-source LLM via Ollama, or an API

* Datasets: deepset/prompt-injections, jayavibhav/prompt-injection, Lakera/gandalf\_ignore\_instructions, TrustAIRLab/in-the-wild-jailbreak-prompts (Hugging Face)

* Dashboard: Streamlit — Containerization: Docker

**Hardware**

01 PC (no special devices required):

* Processor: Intel Core i5/i7 (or equivalent)

* Memory: 8 – 16 GB RAM

* Storage: ≥ 256 GB SSD

* GPU is optional — it speeds up transformer fine-tuning; the classical ML baseline runs on CPU, and free Google Colab GPUs can be used for training.

**Other products**

* A working guardrail prototype (API in front of an LLM) with the trained model.

* A comparison of the classical ML baseline and the fine-tuned transformer.

* A dashboard showing attacks, blocked prompts, and model performance.

* Dockerized deployment; capstone report/thesis, installation & user manual, and defense slides.

**4\. Other comment (propose all relative thing if have)**

**Proposed Tasks for students:**

* **Student 1:** build the dataset (collect/merge public datasets, clean, de-duplicate, label); design the architecture.

* **Student 2:** build the classical ML baseline (TF-IDF \+ classifier) and evaluate it.

* **Student 3:** fine-tune the transformer (BERT/DeBERTa), compare models, and run robustness/evasion testing.

* **Student 4:** build the guardrail API (FastAPI) \+ LLM integration \+ logging \+ dashboard; containerize with Docker; write the thesis and documentation.

**Reference**

* \[1\] OWASP, "OWASP Top 10 for Large Language Model Applications," https://owasp.org/www-project-top-10-for-large-language-model-applications/

* \[2\] deepset/prompt-injections Dataset, Hugging Face, https://huggingface.co/datasets/deepset/prompt-injections

* \[3\] Lakera/gandalf\_ignore\_instructions Dataset, Hugging Face, https://huggingface.co/datasets/Lakera/gandalf\_ignore\_instructions

* \[4\] TrustAIRLab in-the-wild-jailbreak-prompts, Hugging Face, https://huggingface.co/datasets/TrustAIRLab/in-the-wild-jailbreak-prompts

* \[5\] Hugging Face Transformers Documentation, https://huggingface.co/docs/transformers

* \[6\] Scikit-learn: Machine Learning in Python, https://scikit-learn.org/

| Supervisor (If have) *(Sign and full name)* | Tp. Hồ Chí Minh, date …/…/…… On behalf of Registers *(Sign and full name)* |
| :---: | :---: |

