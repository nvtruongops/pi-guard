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
python Final-Report/scripts/download_dataset.py

# 2. Preprocess & group-aware split (prevents leakage)
python Final-Report/scripts/preprocess.py

# 3. Train Baseline ML model
python Final-Report/scripts/train.py --model baseline

# 4. Run Adversarial Robustness Benchmark
python Final-Report/scripts/benchmark.py
```

### 3. Launching Services
```bash
# Start FastAPI Guardrail Service (Port 8000)
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload

# Start Streamlit Interactive Dashboard (Port 8501)
streamlit run Final-Report/src/dashboard/app.py
```

---

## 🧪 Local Quality Assurance & Validation Suite (Local-First QA)

Dự án PI-Guard áp dụng mô hình **Kiểm định thuần Local (Local-First Validation)**, loại bỏ hoàn toàn phụ thuộc vào GitHub Actions cloud runners để tối ưu tốc độ, đảm bảo tính độc lập và phòng ngừa lỗi môi trường:

```bash
# 1. Cài đặt Git Pre-commit Hook tự động (chặn commit vi phạm ranh giới & lỗi cú pháp)
python Final-Report/scripts/validate_local.py --install-hook

# 2. Kiểm định nhanh trước khi commit (Workspace Boundary + JSON Manifests + Ruff Lint + Benchmark Smoke Test)
python Final-Report/scripts/validate_local.py

# 3. Kiểm định toàn diện 100% (Bao gồm đầy đủ Pytest 16 bài tests + Biên dịch MkDocs Portal)
python Final-Report/scripts/validate_local.py --all

# 4. Chạy trực tiếp Pytest Suite (Unit, Integration & Adversarial Robustness)
pytest Final-Report/tests/ -v

# 5. Xem Cổng tài liệu nội bộ trên máy cục bộ (Local MkDocs Server)
python Final-Report/scripts/build_docs_portal.py
mkdocs serve   # Truy cập tại: http://127.0.0.1:8000
```

---

## 📚 Project Structure (3 Phân Hệ Độc Tôn Tại Thư Mục Gốc)

Hệ thống thư mục gốc của dự án được quy hoạch tối giản thành **đúng 3 thư mục chính**:

```
d:/Work/Do-an/
├── 📁 Final-Report/                # [PHÂN HỆ 1: BÁO CÁO TỔNG & MÃ NGUỒN SẢN PHẨM]
│   ├── src/                       # [CORE CODEBASE] Mã nguồn sản phẩm bảo vệ Guardrail chính thức
│   │   ├── api/                   # FastAPI Async Guardrail Middleware & Endpoints
│   │   ├── models/                # Model abstractions (TF-IDF Baseline, DeBERTa-v3, ONNX INT8)
│   │   ├── preprocessing/         # Unicode cleaner, normalizer & synthetic obfuscation generators
│   │   ├── datasets/              # Dataset loaders & group-aware splitters chống data leakage
│   │   ├── policy/                # 3-tier Decision Policy Engine & Dynamic Thresholds
│   │   ├── llm/                   # Downstream LLM Cloud API proxies (Groq, OpenAI, Gemini)
│   │   ├── dashboard/             # Streamlit Live Monitoring & Testing UI
│   │   └── evaluation/            # Metrics calculator, FPR computation & Latency profiler
│   ├── tests/                     # [TEST SUITE] Bộ kiểm thử tự động pytest (unit, integration, adversarial)
│   ├── scripts/                   # [TOOLING & QA] Bộ công cụ tự động hóa kiểm định Local QA & build docs portal
│   ├── thesis/                    # Toàn văn Luận văn tốt nghiệp (FINAL_THESIS.md, Review 1, Chapters 1-6)
│   ├── notebooks/                 # Toàn bộ tài nguyên thực nghiệm & Jupyter Notebooks tái lập (configs/, data/, models/)
│   ├── Meeting/                   # Biên bản các cuộc họp tiến độ với GVHD & nội bộ nhóm (Meeting 1, 2, 3)
│   ├── References/                # Toàn bộ 18 bài báo khoa học toàn văn PDF & REFERENCES_LOG.md
│   ├── PI-GUARD-Present-109.pptx  # Slide báo cáo tiến độ gặp GVHD ngày 10/09/2026 (22 slides, Dark Slate Navy)
│   ├── PI_GUARD_PROCESS_REPORT.xlsx # Sổ theo dõi tiến độ chính thức (FPT IAP491 Process Report: WBS, Nhân sự, Họp)
│   ├── FPT_IAP491_Capstone_Guidelines_and_Rubrics_Summary.md # Tóm tắt quy chuẩn & barem điểm chấm FPT IAP491
│   ├── figures/                   # Sơ đồ kiến trúc & đồ họa (gồm thư mục con PI-GUARD-Present-109/)
│   ├── tables/                    # Bảng số liệu đối chuẩn định dạng Markdown & LaTeX
│   └── experiment_reports/        # Báo cáo tóm tắt chỉ số thực nghiệm dạng JSON/Markdown
│
├── 📁 Github-Page/                 # [PHÂN HỆ 2: GITHUB PAGES] Cổng tài liệu Web UI chính thức (MkDocs Material 8 Chuyên Đề)
│   ├── index.md                   # Trang chủ cổng tài liệu Web UI (8-Pillar Academic Architecture)
│   ├── javascripts/ & stylesheets/# Cấu hình MathJax LaTeX hiển thị công thức & Custom CSS giao diện
│   └── [8 Chuyên Đề Khoa Học]/    # Prompt, Attacks, Threat & Defense, Dataset, Models, Robustness, Optimization, Evaluation
│
└── 📁 workspaces/                  # [PHÂN HỆ 3: WORKSPACE THÀNH VIÊN] Không gian thử nghiệm sandbox độc lập của 4 bạn
    ├── truongnv/                  # Workspace Leader (Trường): Chuẩn hóa dữ liệu, kiến trúc hệ thống, điều phối chung
    ├── ducnq/                     # Workspace Đức: Classical ML Baseline TF-IDF, Feature Extraction & Threat Model
    ├── vietpmh/                   # Workspace Việt: Transformer DeBERTa-v3, Quantization INT8, Robustness Testing
    ├── phuongddd/                 # Workspace Phương: FastAPI Guardrail Proxy, Streamlit Dashboard & Luận văn
    └── README.md                  # Hướng dẫn quy chuẩn bố trí không gian làm việc cá nhân
```

