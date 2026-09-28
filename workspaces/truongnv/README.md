# WORKSPACE CÁ NHÂN — NGUYỄN VĂN TRƯỜNG (LEADER)
**PI-Guard Capstone Project** | Quản lý dữ liệu, hồ sơ kỹ thuật và đồng quy thực nghiệm toàn nhóm.

---

### 🏛️ 1. HỆ THỐNG TÀI LIỆU KIM TỰ THÁP 3 TẦNG & NGUỒN CHÂN LÝ DUY NHẤT (SSOT):

Toàn bộ tài liệu báo cáo và nghiên cứu sâu được tổ chức theo kiến trúc Kim Tự Tháp 3 Tầng, bảo đảm không trùng lặp và có thể truy xuất nguồn gốc học thuật 100%:

> 📜 **Bản đồ Phả hệ Dẫn xuất Học thuật**: [`docs/DOCUMENTATION_PROVENANCE_AND_DERIVATION_MATRIX.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/DOCUMENTATION_PROVENANCE_AND_DERIVATION_MATRIX.md)  
> 💎 **5 Canonical Technical Dossiers (Tầng 1 SSOT)**:
> 1. [`01_MATHEMATICAL_FOUNDATIONS.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/dossiers/01_MATHEMATICAL_FOUNDATIONS.md): Hình thức hóa toán học ranh giới phẳng $X = S \mathbin{\Vert} U$ & 3 RQs.
> 2. [`02_THREAT_MODEL_AND_8KEYS.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/dossiers/02_THREAT_MODEL_AND_8KEYS.md): Khung mô hình hiểm họa 5D NIST AI 100-2e2025 & Ma trận 8 Key.
> 3. [`03_SOTA_SURVEY_AND_6BASELINES.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/dossiers/03_SOTA_SURVEY_AND_6BASELINES.md): Phễu khoa học 5 bước & 6 Baseline thực nghiệm đối đầu trên D1–D6.
> 4. [`04_DATA_ENGINEERING_PROVENANCE.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/dossiers/04_DATA_ENGINEERING_PROVENANCE.md): Thu thập 45k mẫu, Kiểm toán 100% SHA-256 trên 25 tệp & Group-Aware Splitter.
> 5. [`05_ARCHITECTURAL_DEPRECATIONS.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/dossiers/05_ARCHITECTURAL_DEPRECATIONS.md): Đóng băng kiến trúc chính thức, Loại trừ INT8 & Chiến lược bảo vệ Hội đồng.

---

### 📂 2. DANH MỤC HỒ SƠ & BÁO CÁO REVIEW 1 TRONG WORKSPACE CỦA BẠN:

- 📘 **Bản thảo Luận văn & Báo cáo Review 1**:
  - [`reports/REVIEW_1_REPORT.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/REVIEW_1_REPORT.md): **BÁO CÁO REVIEW 1 TOÀN DIỆN** (Chapter 1, Chapter 2 & Đánh giá 7 tiêu chí cốt lõi).
  - [`reports/REVIEW_1_PRESENTATION_AND_QA_SCRIPT.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/REVIEW_1_PRESENTATION_AND_QA_SCRIPT.md): Kịch bản thuyết trình 15 phút & Bộ 10 câu hỏi phản biện Hội đồng.
  - [`docs/thesis/chapters/01_Introduction.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/thesis/chapters/01_Introduction.md): Toàn văn Chương 1 (Introduction & Threat Model).
  - [`docs/thesis/chapters/02_Literature_Review.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/thesis/chapters/02_Literature_Review.md): Toàn văn Chương 2 (Literature Review & SOTA Survey).
  - [`reports/ARCHITECTURAL_DEPRECATIONS_AND_OUT_OF_SCOPE.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/ARCHITECTURAL_DEPRECATIONS_AND_OUT_OF_SCOPE.md): Văn kiện đóng băng kiến trúc chính thức & loại bỏ INT8.
  - [`reports/tasks_for_meeting_5/README.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/README.md): **Hồ sơ lưu trữ lịch sử Meeting 5** (Có banner dẫn chiếu SSOT).
  - [`reports/tasks_for_meeting_6/README.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_6/README.md): **Hồ sơ lưu trữ lịch sử Meeting 6** (Có banner dẫn chiếu SSOT).

- 🔬 **Phân Hệ Nghiên Cứu Khoa Học Kỹ Thuật ([`docs/research/`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/README.md) — 100% Academic Grounding)**:
  - 🔤 [`docs/research/prompt_study/`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/prompt_study/): Chuyên đề 1 — Cơ sở LLM, Cấu trúc Prompt, Phân cấp chỉ thị & Ranh giới phẳng ($X = S \mathbin{\Vert} U$).
  - 🛡️ [`docs/research/attack_study/`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/attack_study/): Chuyên đề 2 — Cơ chế Prompt Injection (Direct/Indirect) & Modern Jailbreak Taxonomy (DAN, VM, 26 Toán tử Tencent).
  - 🎯 [`docs/research/threat_and_defense_study/`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/threat_and_defense_study/): Chuyên đề 3 — Threat Model (NIST AI 100-2e2025, OWASP LLM01, STRIDE) & Kiến trúc phòng thủ 3 lớp Saltzer-Schroeder.
  - 📊 [`docs/research/dataset_and_benchmark_study/`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/dataset_and_benchmark_study/): Chuyên đề 4 — Data Curation, Cân bằng lớp & Group-Aware Splitting chống rò rỉ dữ liệu.
  - 🔬 [`docs/research/model_study/`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/model_study/): Chuyên đề 5 — TF-IDF Baseline (char_wb), DeBERTa-v3 Transformer & Kiến trúc phối hợp Cascade Two-Tier.
  - 🧱 [`docs/research/robustness_study/`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/robustness_study/): Chuyên đề 6 — Độ bền đối kháng, Phân mảnh tokenizer BPE & Kỹ thuật lẩn tránh (Base64, Leetspeak, Spacing).
  - ⚖️ [`docs/research/evaluation_and_tradeoff_study/`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/evaluation_and_tradeoff_study/): Chuyên đề 7 — Kinh tế học False Positive Rate ($\text{FPR} < 1.5\%$), Pareto Frontier & Đánh đổi kỹ thuật.
  - 🔍 [`docs/research/comparative_analysis/`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/comparative_analysis/): Chuyên khảo đối chuẩn SOTA Guardrails, Lỗ hổng Target LLM APIs & Báo cáo Tencent 2026.

- 🧪 **Trung Tâm Tái Lập Y Văn & Baselines ([`replications/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/README.md))**:
  - Quản lý tập trung **100% các mô hình tái lập y văn upstream nguyên bản** có đầy đủ Bộ Ba Công Khai (Public Code + Paper + Dataset): `Paper_ACL2025_PIGuard_HaoLi`, `Baseline_DualSpace_TFIDF_Jain2023`, `Meta PromptGuard 2024`, `ProtectAI DeBERTa-v3`, `DataSentinel S&P 2025`, `SmoothLLM NeurIPS 2023`, v.v.
  - Đi kèm toàn bộ Interactive Notebooks, Datasets, Scripts kiểm định và Sổ tay tái lập (`MEMBER_REPRODUCTION_RUNBOOK.md`).

- 🏛️ **Phân Hệ Báo Cáo Tiến Độ & Cột Mốc ([`reports/`](file:///d:/Work/Do-an/workspaces/truongnv/reports/README.md))**:
  - Lưu trữ hồ sơ nghiên cứu và sản phẩm thực nghiệm qua các cột mốc:
    - [`reports/report_for_meeting_4/`](file:///d:/Work/Do-an/workspaces/truongnv/reports/report_for_meeting_4/): Cột mốc Meeting 4 (4 Task nghiên cứu mối đe dọa 5D, tính tái lập dữ liệu, cải tiến phòng thủ).
    - [`reports/tasks_for_meeting_5/`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/): Cột mốc Meeting 5 (Tái lập thực nghiệm PIGuard ACL 2025, đối chuẩn 4 mô hình ứng viên).
    - [`reports/tasks_for_meeting_6/`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_6/): Cột mốc Meeting 6 Đóng Băng Danh Mục Baseline Y Văn & Đối Chuẩn 12 Mô Hình Public (Benchmark 520 samples, Khung Đề Xuất Kiến Trúc 2 Tầng Two-Tier Cascade cho Chương 3; Chưa huấn luyện mô hình đồ án).

- 📚 **Tài liệu tham khảo & Thư viện Nghiên cứu**:
  - [`References/REFERENCES_LOG.md`](file:///d:/Work/Do-an/workspaces/truongnv/References/REFERENCES_LOG.md): Bảng ma trận 18 bài báo chuẩn (100% >= 2022).
  - [`docs/README.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/README.md): Cổng tài liệu tổng quan phân định 2 phân hệ `research/` và `thesis/`.

---

### 📌 QUY TRÌNH KHI CHỐT FINAL REPORT:
1. Bạn có thể tự do chỉnh sửa, bổ sung, format các file trong workspace này.
2. Khi nhóm họp xong và thống nhất chốt bản Final Report Review 1 $\rightarrow$ Đồng bộ phiên bản chính thức ra thư mục chung `Final-Report/` và `Github-Page/` để nộp cho Giảng viên hướng dẫn và xuất bản cổng tài liệu!
