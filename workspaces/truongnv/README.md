# PI-Guard — Workspace Kiến trúc & Nghiên cứu (Nguyễn Văn Trường)

## Bản thảo luận văn hiện hành

- [Chapter 1 — Introduction](docs/thesis/chapters/01_Introduction.md)
- [Chapter 2 — Literature Review](docs/thesis/chapters/02_Literature_Review.md)
- [Hướng dẫn đọc và nguồn](docs/thesis/README.md)

Chào mừng đến với workspace chính của Trưởng nhóm Nghiên cứu (**Nguyễn Văn Trường** - `nvtruongops` / `SE182034`) thuộc đề tài Khóa luận Tốt nghiệp **PI-Guard** (FPT University - `IAP491`).

---

## 🏛️ 1. Bản đồ Kiến trúc Workspace (Architecture Map)

```
workspaces/truongnv/
├── docs/                                          # Tài liệu học thuật & đặc tả hệ thống
│   ├── architecture/                              # Threat model định tính & phương án kiến trúc
│   │   ├── THREAT_MODEL_AND_ATTACK_SURFACE.md     # Mô hình mối đe dọa, tài sản và bề mặt tấn công
│   │   ├── MULTI_LAYER_DEFENSE_ARCHITECTURE.md    # Đề xuất nhiều tầng; chưa được đánh giá end-to-end
│   │   └── COMPARATIVE_MATRIX_AND_TRADEOFFS.md    # So sánh khái niệm; không xếp hạng phép chạy local
│   ├── thesis/                                    # Cấu trúc Luận văn tốt nghiệp (Chapters 1–6)
│   │   ├── README.md                              # Khung luận văn & tiêu chuẩn đánh giá FPT Capstone
│   │   └── chapters/                              # Bản thảo hiện hành Chương 1–2
│   │       ├── 01_Introduction.md                 # Bối cảnh, bài toán, mục tiêu và phạm vi
│   │       ├── 02_Literature_Review.md            # Nghiên cứu trước, tổng hợp và đóng góp dự kiến
│   │       └── README.md                          # Quy tắc đọc và nguồn của hai chương
│   └── research/                                  # Nghiên cứu chuyên đề & kịch bản demo
│       ├── dossiers/                              # 2 ghi chú trạng thái; không phải 5 dossier SSOT
│       ├── archive/                               # Thông báo cho các bản nháp nghiên cứu đã thu hồi
│       └── demos/                                 # Kịch bản demo kiểm thử TF-IDF & DeBERTa-v3
│
├── reports/                                       # Hệ thống Báo cáo & Hồ sơ Milestone
│   ├── README.md                                  # Mục lục điều hướng tổng thể các báo cáo
│   ├── report_for_meeting_4/                       # Hồ sơ Meeting 4 đã lưu trữ
│   ├── report_for_review1/                        # Hồ sơ bảo vệ Hội đồng đợt 1 (Review 1 Submission)
│   │   ├── REVIEW_1_COUNCIL_SUBMISSION_REPORT.docx# Báo cáo chính thức nộp Hội đồng (.docx)
│   │   ├── REVIEW_1_COUNCIL_SUBMISSION_DRAFT.md   # Bản thảo chi tiết Review 1 (.md)
│   │   └── REVIEW_1_PRESENTATION_AND_QA_SCRIPT.md # Kịch bản thuyết trình & trả lời phản biện
│   ├── experiment_reports/                        # Kết quả thực nghiệm, kiểm toán xuất xứ & governance
│   │   ├── WORKSPACE_PROVENANCE_AUDIT_2026-09-30.md# Nguồn chuẩn về bằng chứng và phép chạy thu hồi
│   │   └── REPO_GOVERNANCE_AND_RESEARCH_MCP_AUDIT_2026-09-28.md # Kiểm toán governance & cấu hình MCP
│   ├── tasks_for_meeting_5/                       # Hồ sơ nhiệm vụ Meeting 5 đã lưu trữ
│   ├── tasks_for_meeting_6/                       # Hồ sơ Meeting 6; benchmark cross-paper đã thu hồi
│
├── src/                                           # Mã nguồn triển khai Guardrail Proxy (Clean Architecture)
│   ├── api/                                       # FastAPI Guardrail Proxy Service (`main.py`)
│   ├── dashboard/                                 # Streamlit Evaluation & Live Demo UI (`app.py`)
│   ├── evaluation/                                # Module tính toán độ đo benchmark & ROC-AUC (`metrics.py`)
│   ├── models/                                    # Bộ phân loại & replication adapters
│   ├── policy/                                    # Decision Engine & phân luồng ngưỡng (`policy_engine.py`)
│   ├── preprocessing/                             # Tiền xử lý, Scrubber tiếng Việt & phát hiện Obfuscation
│   └── utils/                                     # Logging, configuration & helpers
│
├── tests/                                         # Bộ kiểm thử tự động hóa (Pytest Suite)
│   ├── unit/                                      # Kiểm thử đơn vị (Metrics, Policy, Models, Scrubber)
│   ├── integration/                               # Kiểm thử tích hợp FastAPI Endpoints
│   └── adversarial/                               # Kiểm thử độ bền vững trước Evasion & Tiếng Việt biến thể
│
├── replications/                                  # Tái lập thực nghiệm các mô hình SOTA từ bài báo gốc
│   ├── 02_DeBERTa_v3_Semantic_Classifier/         # Gói nghiên cứu DeBERTa-v3 (chỉ giữ snapshot PIGuard paper-matched)
│   ├── PIDS_Bench_Shire_IEEEAccess2026/           # Baseline TF-IDF + Logistic Regression chuẩn paper-matched (IEEE Access 2026)
│   ├── DataSentinel_Liu_SP2025/                   # Tài liệu tham khảo mã nguồn DataSentinel (IEEE S&P 2025)
│   └── PromptShield_Jacob_CCS2024/                # Tài liệu tham khảo mã nguồn PromptShield (CODASPY 2025)
│
├── References/                                    # 38+ Bài báo khoa học chuẩn (PDF) & REFERENCES_LOG.md
├── references_study/                              # Phân tích sâu kiến trúc mã nguồn tham chiếu
├── Meeting/                                       # Chứa file theo dõi tiến độ tuần `PI_GUARD_PROCESS_REPORT.xlsx`
└── VERSION.md                                     # Quy định phiên bản phát hành workspace
```

---

## 🚀 2. Hướng dẫn Chạy Thử nghiệm & Kiểm thử (Quickstart)

### Kiểm thử bộ Test Suite (Pytest)
```powershell
# Chạy toàn bộ test suite từ thư mục gốc dự án
$env:PYTHONPATH="workspaces\truongnv;."
workspaces\truongnv\.venv\Scripts\python.exe -m pytest workspaces\truongnv\tests\unit workspaces\truongnv\tests\adversarial workspaces\truongnv\tests\integration -q
```

### Chạy Giao diện Trực quan Hóa (Streamlit Dashboard)
```powershell
$env:PYTHONPATH="workspaces\truongnv;."
workspaces\truongnv\.venv\Scripts\streamlit.exe run workspaces\truongnv\src\dashboard\app.py
```

### Khởi động API Guardrail Proxy (FastAPI)
```powershell
$env:PYTHONPATH="workspaces\truongnv;."
workspaces\truongnv\.venv\Scripts\uvicorn.exe src.api.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 🔬 3. Hiện trạng Bằng chứng Thực nghiệm & Ranh giới (Evidence Status)

- **Bằng chứng hợp lệ cấp bài báo (Eligible):**
  1. [`PIDS_Bench TF-IDF Baseline`](replications/PIDS_Bench_Shire_IEEEAccess2026/REPORT.md): Khớp 100% dữ liệu gốc tác giả với 3.918 mẫu kiểm thử.
  2. [`PIGuard Checkpoint`](replications/02_DeBERTa_v3_Semantic_Classifier/reports/review1_paper_model_public_rerun_2026-09-30/REPORT.md): Đánh giá checkpoint gốc của tác giả trên tập test đính kèm bài báo.
- **Ranh giới đề xuất:** Kiến trúc hai tầng nối tiếp (Two-Tier Cascade) của PI-Guard hiện đang ở giai đoạn thiết kế phương pháp luận (Review 2). Các mục tiêu P95 < 30ms và FPR < 1.5% là mục tiêu thiết kế cần đạt, chưa phải số liệu công bố sau cùng.
