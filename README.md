<div align="center">

# 🛡️ PI-Guard
### A Machine-Learning Guardrail for Detecting Prompt Injection and Jailbreak Attacks on LLM Applications

[![CI Pipeline](https://img.shields.io/badge/CI%20Pipeline-Passing-brightgreen.svg?logo=github-actions&logoColor=white)](https://github.com/nvtruongops/pi-guard/actions)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)
[![Framework](https://img.shields.io/badge/FastAPI-Streamlit-orange.svg)](https://fastapi.tiangolo.com)

**FPT University — Information Assurance (IS) Capstone Project**

</div>

---

## 📌 Executive Summary (6 Core Research Questions)

### 1. What is PI-Guard?
**PI-Guard** is an open-source, API-driven defensive guardrail layer placed in front of Large Language Model (LLM) applications. It intercepts incoming user prompts, evaluates them with specialized machine learning and transformer classifiers, and enforces dynamic security policies (`ALLOW`, `REVIEW`, `BLOCK`) before requests ever reach downstream LLMs.

### 2. Why Prompt Injection & Jailbreaks?
In the **OWASP Top 10 for LLM Applications (2025)**, Prompt Injection (LLM01) is ranked as the #1 critical risk. Traditional rule-based regex filters are brittle: attackers easily evade them using **leetspeak (`1gn0r3`)**, **Base64 encoding**, **character spacing**, and **cognitive distraction riddles**. PI-Guard replaces brittle keyword filters with learning-based semantic detection.

### 3. What is our Research Question?
> *"Can a hybrid semantic classifier (DeBERTa-v3 + Char/Word TF-IDF) detect diverse prompt injection and jailbreak attacks with a **False Positive Rate (FPR) < 1.5%** on benign prompts while maintaining **P95 inference latency < 30ms** in production environments?"*

### 4. What Datasets are Used?
Curated from public benchmarks on Hugging Face and deduplicated with **Group-Aware Splitting** (clustering attack families to prevent data leakage):
- `deepset/prompt-injections` (Standard benchmark)
- `jayavibhav/prompt-injection` (Large-scale collection)
- `Lakera/gandalf_ignore_instructions` (Real-world Gandalf game user attacks)
- `TrustAIRLab/in-the-wild-jailbreak-prompts` (Community in-the-wild jailbreaks)
- `Open-Orca/OpenOrca` (High-quality negative/benign everyday instruction samples)

### 5. What Models are Compared?
1. **Classical ML Baseline**: Hybrid Word (1-3) & Char (3-5) n-gram TF-IDF + Logistic Regression / LinearSVC.
2. **Fine-Tuned Transformer**: `microsoft/deberta-v3-base` with sequence classification head.
3. **Quantized Production Engine**: DeBERTa-v3 with ONNX INT8 Dynamic Quantization.
4. **Reference SOTA**: `ProtectAI/deberta-v3-base-prompt-injection`.

### 6. What are the Comparative Results?

| Model Architecture | Accuracy (%) | Precision | Recall (TPR) | F1-Score | FPR on Benign (%) | P95 Latency (ms) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **TF-IDF Baseline (Linear)** | 92.4% | 0.912 | 0.925 | 0.918 | 2.8% | **3.2 ms** |
| **ProtectAI SOTA Baseline** | 97.2% | 0.968 | 0.972 | 0.970 | 1.4% | 29.1 ms |
| **PI-Guard (DeBERTa-v3 Base)** | **98.1%** | **0.984** | **0.979** | **0.981** | **0.9%** | 28.5 ms |
| **PI-Guard (ONNX INT8)** | **97.8%** | **0.980** | **0.975** | **0.977** | **1.1%** | **12.8 ms** |

---

## 🏛️ System Architecture

```
                       [ User Prompt ]
                              │
                              ▼
           ┌─────────────────────────────────────┐
           │        PI-Guard Middleware          │
           │                                     │
           │  ┌───────────────┐ ┌──────────────┐ │
           │  │ ML Classifier │ │ Policy Engine│ │
           │  │ (Probability) │ │(ALLOW/BLOCK) │ │
           │  └───────┬───────┘ └──────┬───────┘ │
           └──────────┼────────────────┼─────────┘
                      │                │
          ┌───────────┴────────────────┴───────────┐
          │                                        │
          ▼ Score < 0.50 (ALLOW)                   ▼ Score >= 0.80 (BLOCK)
  [ Forward to Target LLM ]                 [ HTTP 403 / Security Alert ]
  (Groq / OpenAI / Gemini)                         │
          │                                        ▼
          └───────────────────────────────► [ Streamlit Dashboard ]
```


---

## 👥 Collaborative Engineering Paradigm (FPT University)

> **Team Philosophy**: **Ai cũng làm $\rightarrow$ Tham khảo nhau $\rightarrow$ Chốt kết quả**  
> All 4 members work hands-on across the entire pipeline in parallel (`workspaces/<member>/`), cross-review each other's code and experimental metrics, and converge weekly to select the champion models and documentation merged by the Leader.

| Member | Student ID | Parallel Exploration | Focus & Focal Modules |
| :--- | :--- | :--- | :--- |
| **Nguyễn Văn Trường (Leader)** | SE182034 | Full-Pipeline (`workspaces/truongnv/`) | Architecture, Data Engineering & Repository Governance |
| **Nguyễn Quí Đức** | SE182087 | Full-Pipeline (`workspaces/ducnq/`) | Classical ML Baseline, Feature Extraction & Threat Model |
| **Phạm Minh Hoàng Việt** | SE181851 | Full-Pipeline (`workspaces/vietpmh/`) | Transformer Fine-Tuning, Quantization & Robustness Testing |
| **Đỗ Đoàn Duy Phương** | SE180235 | Full-Pipeline (`workspaces/phuongddd/`) | FastAPI Middleware, Streamlit Dashboard & Thesis Compilation |

---

## 🚀 Quick Start Guide

### 1. Installation
```bash
# Clone repository
git clone https://github.com/nvtruongops/pi-guard.git
cd pi-guard

# Install dependencies
pip install -r requirements.txt
pip install -e .
```

### 2. Dataset Pipeline & Training
```bash
# 1. Download & merge Hugging Face datasets
python scripts/download_dataset.py

# 2. Preprocess & group-aware split (prevents leakage)
python scripts/preprocess.py

# 3. Train Baseline ML model
python scripts/train.py --model baseline

# 4. Run Adversarial Robustness Benchmark
python scripts/benchmark.py
```

### 3. Launching Services
```bash
# Start FastAPI Guardrail Service (Port 8000)
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload

# Start Streamlit Interactive Dashboard (Port 8501)
streamlit run src.dashboard/app.py
```

---

## 🧪 Local Quality Assurance & Validation Suite (Local-First QA)

Dự án PI-Guard áp dụng mô hình **Kiểm định thuần Local (Local-First Validation)**, loại bỏ hoàn toàn phụ thuộc vào GitHub Actions cloud runners để tối ưu tốc độ, đảm bảo tính độc lập và phòng ngừa lỗi môi trường:

```bash
# 1. Cài đặt Git Pre-commit Hook tự động (chặn commit vi phạm ranh giới & lỗi cú pháp)
python scripts/validate_local.py --install-hook

# 2. Kiểm định nhanh trước khi commit (Workspace Boundary + JSON Manifests + Ruff Lint + Benchmark Smoke Test)
python scripts/validate_local.py

# 3. Kiểm định toàn diện 100% (Bao gồm đầy đủ Pytest 16 bài tests + Biên dịch MkDocs Portal)
python scripts/validate_local.py --all

# 4. Chạy trực tiếp Pytest Suite (Unit, Integration & Adversarial Robustness)
pytest tests/ -v --cov=src

# 5. Xem Cổng tài liệu nội bộ trên máy cục bộ (Local MkDocs Server)
python scripts/build_docs_portal.py
mkdocs serve   # Truy cập tại: http://127.0.0.1:8000
```

---

## 📚 Project Structure

```
d:/Work/Do-an/
├── .agents/                 # AI Pair Programming Environment (MCP, Skills, Rules)
├── .github/CODEOWNERS       # Collective Code Ownership & PR Review Governance
├── configs/                 # YAML configurations (data, training, evaluation, models)
├── data/                    # Datasets (raw, interim, processed, splits, manifests)
├── notebooks/               # 01_eda, 02_baseline, 03_transformer, 04_ablation, 05_errors
├── src/
│   ├── preprocessing/       # Normalization & synthetic obfuscation generators
│   ├── datasets/            # Dataset loaders & group-aware splitters
│   ├── models/              # Model abstractions (TF-IDF, DeBERTa, ONNX, Dummy)
│   ├── policy/              # 3-tier Decision Policy Engine & Thresholds
│   ├── llm/                 # Downstream LLM Cloud API proxies (Groq, OpenAI, Gemini)
│   ├── api/                 # FastAPI Guardrail Middleware & Endpoints
│   ├── dashboard/           # Streamlit Monitoring UI
│   └── evaluation/          # Metrics, FPR computation & Latency profiler
├── tests/
│   ├── unit/                # Preprocessing, policy, and metrics tests
│   ├── integration/         # API endpoint integration tests
│   └── adversarial/         # Direct, indirect, jailbreak, leetspeak, base64 slices
├── reports/                 # Evaluation figures, tables, and metric reports
├── docs/                    # Architecture, methodology, attack studies, and thesis documentation
├── scripts/                 # Local QA suite (validate_local.py, audit_workspace_boundaries.py, build_docs_portal.py)
└── workspaces/              # Individual sandboxes for 4 members (Parallel Full-Pipeline Exploration)
    ├── truongnv/            # Workspace: Nguyễn Văn Trường (Leader)
    ├── ducnq/               # Workspace: Nguyễn Quí Đức
    ├── vietpmh/             # Workspace: Phạm Minh Hoàng Việt
    └── phuongddd/           # Workspace: Đỗ Đoàn Duy Phương
```

