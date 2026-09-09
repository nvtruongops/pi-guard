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
Curated from public benchmarks on Hugging Face and deduplicated with **Group-Aware Splitting** (clustering attack families to prevent data leakage) as specified in [`CAPSTONE PROJECT REGISTER.md`](CAPSTONE%20PROJECT%20REGISTER.md):
- `deepset/prompt-injections` (Standard benchmark of benign vs. injection prompts)
- `jayavibhav/prompt-injection` (Large-scale labeled prompt injection collection)
- `xTRam1/safe-guard-prompt-injection` (Benign vs. injection prompts for guardrail training)
- `Lakera/gandalf_ignore_instructions` (Real-world Gandalf game user attacks)
- `TrustAIRLab/in-the-wild-jailbreak-prompts` (Community in-the-wild jailbreaks)
- Benign everyday instruction & Q&A prompts from open datasets to balance the negative class.

### 5. What Models are Compared?
1. **Classical ML Baseline**: Hybrid Word (1-3) & Char (3-5) n-gram TF-IDF + Logistic Regression / LinearSVC.
2. **Fine-Tuned Transformer**: `microsoft/deberta-v3-base` with sequence classification head.
3. **Quantized Production Engine**: DeBERTa-v3 with ONNX INT8 Dynamic Quantization for low-latency CPU inference.
4. **Reference SOTA**: `ProtectAI/deberta-v3-base-prompt-injection`.

### 6. What are the Target Evaluation Metrics? (Benchmarking In Progress)
In accordance with the approved [`CAPSTONE PROJECT REGISTER.md`](CAPSTONE%20PROJECT%20REGISTER.md), PI-Guard is evaluated across four core performance dimensions (full comparative empirical benchmarking scheduled for Review 2 / Milestone 2):
1. **Detection Performance**: Accuracy, Precision, Recall, and F1-score on held-out test splits. Target F1-Score: **> 0.95**.
2. **False Positive Rate (FPR) on Benign Prompts**: Minimizing false alarms on legitimate everyday user queries to prevent over-defense. Target FPR: **< 1.5%**.
3. **Robustness Against Obfuscated Attacks**: Evaluating defense capabilities against evasion transformations (Leetspeak, Base64 encoding, character spacing tricks).
4. **Low Inference Latency**: Ensuring minimal overhead for inline proxying before target LLMs. Target P95 Latency: **< 30 ms** on multi-core CPU via ONNX INT8.

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
> All 4 members work hands-on across the entire pipeline in parallel sandbox workspaces (`workspaces/<member>/`), cross-review each other's code and experimental metrics, and converge weekly to select champion models and documentation merged by the Leader.

| Student | Full Name | Student Code | Role in Group | Workspace Sandbox |
| :--- | :--- | :--- | :--- | :--- |
| **Student 1** | Nguyễn Văn Trường | SE182034 | Leader | [`workspaces/truongnv/`](workspaces/truongnv/) |
| **Student 2** | Nguyễn Quí Đức | SE182087 | Member | [`workspaces/ducnq/`](workspaces/ducnq/) |
| **Student 3** | Phạm Minh Hoàng Việt | SE181851 | Member | [`workspaces/vietpmh/`](workspaces/vietpmh/) |
| **Student 4** | Đỗ Đoàn Duy Phương | SE180235 | Member | [`workspaces/phuongddd/`](workspaces/phuongddd/) |

---

## 🚀 Quick Start Guide (Coming Soon — Under Active Development)

> [!NOTE]
> The full automated dataset curation, transformer fine-tuning, and production deployment pipeline are currently under active development for **Review 2 (Methodology & Baseline)**. The commands below demonstrate the environment setup and developer preview tools available in the current milestone.

### 1. Environment Setup (Developer Preview)
```bash
# Clone repository
git clone https://github.com/nvtruongops/pi-guard.git
cd pi-guard

# Install dependencies (Self-contained in Final-Report/)
pip install -r Final-Report/requirements.txt
# Alternatively, install development & documentation dependencies:
pip install -r Final-Report/requirements-dev.txt

# Configure environment variables
cp Final-Report/.env.example .env
```

### 2. Dataset Pipeline & Model Training (Coming Soon — Scheduled for Review 2)
> [!TIP]
> The complete end-to-end dataset engineering and model training pipelines are scheduled for Review 2 according to the project roadmap. The planned workflow includes:
> - **Dataset Collection & Curation**: Merging Hugging Face datasets (`deepset`, `jayavibhav`, `xTRam1`, `Lakera`, `TrustAIRLab`) and benign instruction sets.
> - **Group-Aware Splitting**: Clustering paraphrased attack families to prevent test-set data leakage.
> - **Model Training**: Baseline TF-IDF (LinearSVC / LogisticRegression) and Transformer Fine-Tuning (`microsoft/deberta-v3-base`).

```bash
# Planned Workflow (Under Active Development):
# python Final-Report/scripts/download_dataset.py
# python Final-Report/scripts/preprocess.py
# python Final-Report/scripts/train.py --model baseline
# python Final-Report/scripts/benchmark.py
```

### 3. Prototype Services & Local Verification (Available in Current Preview)
```bash
# Run Prototype FastAPI Guardrail Service (Port 8000)
uvicorn Final-Report.src.api.main:app --host 0.0.0.0 --port 8000 --reload

# Run Prototype Streamlit Dashboard (Port 8501)
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
│   ├── reports/                   # [PERIODIC REPORTS & METRICS] Sổ tiến độ, slide trình chiếu & benchmark
│   │   ├── PI-GUARD-Present-109.pptx  # Slide báo cáo tiến độ gặp GVHD ngày 10/09/2026 (22 slides, Dark Slate Navy)
│   │   ├── PI_GUARD_PROCESS_REPORT.xlsx # Sổ theo dõi tiến độ chính thức (FPT IAP491 Process Report: WBS, Nhân sự, Họp)
│   │   ├── experiment_reports/    # Báo cáo tóm tắt chỉ số thực nghiệm dạng JSON/Markdown
│   │   └── README.md              # Hướng dẫn tra cứu & cập nhật các báo cáo
│   ├── figures/                   # Sơ đồ kiến trúc & đồ họa (gồm thư mục con PI-GUARD-Present-109/)
│   ├── tables/                    # Bảng số liệu đối chuẩn định dạng Markdown & LaTeX
│   ├── requirements.txt           # Master Production Dependencies (Core ML, FastAPI, Streamlit, Jupyter)
│   ├── requirements-dev.txt       # Master Dev Dependencies (Pytest, Ruff, Pre-commit, MkDocs)
│   └── .env.example               # Master Environment Configuration Template
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

