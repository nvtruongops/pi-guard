# MASTER REPORTS & TECHNICAL GATEWAY — TRƯƠNGNV
**PI-Guard** | Nguyễn Văn Trường (`SE182034`) | [`workspaces/truongnv/reports/`](file:///d:/Work/Do-an/workspaces/truongnv/reports/)

---

## 🏛️ 1. Cấu Trúc Kim Tự Tháp 3 Tầng & Cổng Nguồn Chân Lý Duy Nhất (SSOT)

Hệ thống tài liệu báo cáo của phân hệ Trưởng nhóm (`truongnv`) tuân thủ nghiêm ngặt **Kiến trúc Kim Tự Tháp 3 Tầng (3-Tier Documentation Pyramid)**:

```text
               ▲
              / \     TẦNG 1: 5 CANONICAL TECHNICAL DOSSIERS (Single Source of Truth)
             /   \    docs/research/dossiers/ (01 -> 05)
            /-----\
           /       \  TẦNG 2: BÁO CÁO CỘT MỐC HỘI ĐỒNG & REVIEW 1 (Milestones)
          /         \ reports/REVIEW_1_REPORT.md & tasks_for_meeting_5, 6
         /-----------\
        /             \ TẦNG 3: CHUYÊN ĐỀ Y VĂN CHI TIẾT & CHỨNG TÍCH LỊCH SỬ (Foundations)
       /               \ docs/research/ (8 Chuyên đề gốc) & replications/ (11 mô hình)
      /-----------------\
```

> 📜 **Bản đồ Phả hệ Dẫn xuất Học thuật**: Xem toàn bộ bằng chứng chứng minh xuất xứ và dẫn xuất tại [`../docs/DOCUMENTATION_PROVENANCE_AND_DERIVATION_MATRIX.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/DOCUMENTATION_PROVENANCE_AND_DERIVATION_MATRIX.md).

### 💎 Nguồn Chân Lý Duy Nhất (Tầng 1 - Canonical Dossiers):
1. **Dossier 01**: [`01_MATHEMATICAL_FOUNDATIONS.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/dossiers/01_MATHEMATICAL_FOUNDATIONS.md) — Cơ sở lý thuyết, Hình thức hóa toán học ranh giới phẳng $X = S \mathbin{\Vert} U$ & 3 RQs.
2. **Dossier 02**: [`02_THREAT_MODEL_AND_8KEYS.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/dossiers/02_THREAT_MODEL_AND_8KEYS.md) — Khung hiểm họa 5D NIST AI 100-2e2025, Bề mặt REST API & Ma trận 8 Key.
3. **Dossier 03**: [`03_SOTA_SURVEY_AND_6BASELINES.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/dossiers/03_SOTA_SURVEY_AND_6BASELINES.md) — Phễu lựa chọn khoa học 5 bước, 6 baseline đối chuẩn & Phân tích điểm vỡ kỹ thuật.
4. **Dossier 04**: [`04_DATA_ENGINEERING_PROVENANCE.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/dossiers/04_DATA_ENGINEERING_PROVENANCE.md) — Thu thập 45k mẫu, Kiểm toán 100% SHA-256 trên 25 tệp & Group-Aware Splitting.
5. **Dossier 05**: [`05_ARCHITECTURAL_DEPRECATIONS.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/dossiers/05_ARCHITECTURAL_DEPRECATIONS.md) — Đóng băng kiến trúc chính thức, Loại trừ INT8 & Chiến lược bảo vệ Hội đồng.

---

## 📂 2. Cấu Trúc Chi Tiết Các Thư Mục Báo Cáo Cột Mốc (Tầng 2 - Historical Milestones)
│   ├── README.md                              # Mục lục tổng quan, biên bản tóm lược buổi họp 10/09
│   ├── PI-GUARD-Present-109.pptx              # File slide thuyết trình 22 slides chuẩn 16:9
│   ├── SUPERVISOR_REPORT_10_09_2026.md        # Báo cáo kịch bản slide-by-slide chi tiết
│   ├── figures/                               # 12 hình ảnh minh chứng khoa học trích xuất từ slide
│   │   ├── PI-GUARD-Present-109/              # (12 tệp PNG chất lượng cao)
│   │   └── README.md                          # Bảng chỉ dẫn 12 slide minh chứng
│   └── tools/                                 # Bộ script tự động sinh slide và hình ảnh
│       ├── generate_presentation.py           # Script Python sinh bản thuyết trình PPTX
│       └── generate_diagrams.py               # Script Python kết xuất hình ảnh kiến trúc
│
├── tasks_for_meeting_5/                       # [PHÂN HỆ 2: TOÀN BỘ NHIỆM VỤ CHUẨN BỊ BÁO CÁO MEETING 5 (17/09/2026)]
│   ├── README.md                              # Báo cáo Master Executive & Cổng điều phối tổng thể
│   ├── MEETING_5_SLIDE_DECK_GUIDE.md          # Đề cương slide thuyết trình Meeting 5
│   ├── PI-GUARD-Present-Meeting-5.pptx        # Bản trình chiếu PPTX (Tiếng Việt)
│   ├── PI-GUARD-Present-Meeting-5-EN.pptx     # Bản trình chiếu PPTX (English)
│   ├── figures/                               # 21 sơ đồ & biểu đồ đối chuẩn thực nghiệm
│   ├── task_reports/                          # Hồ sơ 5 báo cáo kỹ thuật (Task 1, 2, 2.5, 3, 4)
│   │   ├── README.md
│   │   ├── TASK_1_PROMPT_INJECTION_VS_JAILBREAK.md          # Task 1: Phân biệt bản chất 2 bề mặt tấn công
│   │   ├── TASK_2_ATTACK_VECTORS_AND_MODELS.md              # Task 2: Khung 5D & 2 mô hình tham khảo học thuật
│   │   ├── TASK_2_5_SOTA_ASSESSMENT_AND_TWO_TIER_PROPOSAL.md # Task 2.5: Đánh giá SOTA & Kiến trúc 2 tầng
│   │   ├── TASK_3_REPRODUCIBILITY_AND_DATASETS.md           # Task 3: Nghiên cứu toàn diện & tái lập y văn Task 3
│   │   ├── TASK_4_PIGUARD_IMPROVEMENTS.md                   # Task 4: 4 Giải pháp cải tiến của đồ án PI-Guard
│   │   └── supplementary/                     # 7 chuyên khảo học thuật chuyên sâu bổ trợ
│   │       ├── CONTROL_FLOW_HIJACKING_AND_FLAT_TOKEN_SPACE.md
│   │       ├── CORE_ANCHOR_PIGUARD_ACL2025.md
│   │       ├── JAILBREAK_TAXONOMY_CASE_STUDIES_AND_DEFENSE.md
│   │       ├── LITERATURE_ASSESSMENT_TFIDF.md
│   │       ├── README.md
│   │       ├── REJECTED_BASELINE_AYUB_CAMLIS2024.md
│   │       └── TIER1_SCORING_MATHEMATICAL_FORMULATION_AND_BAYES_RISK.md
│   ├── task_3_replication/                    # Phân hệ ánh xạ ngược tới trung tâm tái lập tập trung
│   │   ├── README.md                          # Hướng dẫn chi tiết chạy tái lập trên máy cá nhân
│   │   ├── MEMBER_REPRODUCTION_RUNBOOK.md     # Sổ tay tái lập cho 4 thành viên nhóm
│   │   ├── INDEX_AND_MAPPING_TO_REPLICATIONS.md # Bảng ánh xạ 1-1 tới workspaces/truongnv/replications/
│   │   └── verify_replication_assets.py       # Script kiểm định tự động toàn vẹn tài nguyên Task 3
│   └── tools/                                 # Công cụ sinh slide, đồ họa và kiểm định PPTX
│
└── tasks_for_meeting_6/                       # [PHÂN HỆ 3: HỒ SƠ ĐỐI CHUẨN THỰC NGHIỆM & ĐÓNG BĂNG BASELINE MEETING 6]
    ├── README.md                              # Master Portal Meeting 6: Tổng hợp 12 Public Models
    ├── 01_theory_and_taxonomy/                # Phân loại học 6x7 và 12x14
    ├── 02_compatibility_and_tradeoffs/        # Ma trận tương thích & đánh đổi đa chiều
    ├── 03_reports_and_executive_briefs/       # Báo cáo tiến độ điều hành & Luận chứng bảo vệ Hội đồng
    ├── 04_benchmarks_and_data/                # Dữ liệu JSON đối chuẩn thực nghiệm trên Public Baselines
    └── figures/                               # Biểu đồ khoa học đối chuẩn
```

---

## 🧭 2. Chỉ Mục Phân Hệ & Đường Dẫn Nhanh

| Phân Hệ | Mục Tiêu & Phạm Vi Nghiên Cứu | Đường Dẫn Chính Thức | Trạng Thái |
| :--- | :--- | :--- | :---: |
| **Phân Hệ Review 1 (Report No.1 & No.2)** | Toàn văn Chapter 1 (Introduction), Chapter 2 (Literature Review) và Chuyên đề Đánh giá 7 tiêu chí cốt lõi (Problem Statement, RQs, Objectives, Proposed Solution, Boundary, Feasibility, Progress). | [`report_for_review1/`](file:///d:/Work/Do-an/workspaces/truongnv/reports/report_for_review1/README.md) | **ĐÃ HOÀN THÀNH** |
| **Báo Cáo Nghiên Cứu SOTA Toàn Diện** | Khảo sát 4 thế hệ mô hình học máy (SLM, Transformer Encoder, Metric/Anomaly, Classical ML), 5 phân nhánh đánh đổi đa chiều, và Conformal Risk Control. | [`RESEARCH_ML_GUARDRAIL_SOTA_TO_PROJECT.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/RESEARCH_ML_GUARDRAIL_SOTA_TO_PROJECT.md) | **ĐÃ HOÀN THÀNH** |
| **Phân Hệ 1 (Meeting 4 Archive)** | Lưu trữ bản trình chiếu 22 slide, báo cáo kịch bản thuyết trình và 12 hình ảnh minh chứng đã bảo vệ trực tiếp trước GVHD ngày 10/09/2026. | [`report_for_meeting_4/`](file:///d:/Work/Do-an/workspaces/truongnv/reports/report_for_meeting_4/README.md) | **ĐÃ HOÀN THÀNH** |
| **Phân Hệ 2 (Meeting 5 Tasks)** | 5 báo cáo kỹ thuật (Task 1–4, 2.5), 7 chuyên khảo bổ trợ và phân hệ thực nghiệm tái lập độc lập các mô hình y văn trên máy cá nhân. | [`tasks_for_meeting_5/`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/README.md) | **ĐÃ HOÀN THÀNH** |
| **Thực Nghiệm Tái Lập (Task 3)** | Ánh xạ ngược tới trung tâm tái lập tập trung [`workspaces/truongnv/replications/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/). | [`tasks_for_meeting_5/task_3_replication/`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/README.md) | **ĐÃ ĐỒNG BỘ** |
| **Phân Hệ 3 (Meeting 6 Tasks)** | Đối chuẩn 12 mô hình public SOTA, phân tích failure modes, quét tài liệu 200k và đề xuất kiến trúc 2 tầng (chưa train mô hình đồ án). | [`tasks_for_meeting_6/`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_6/README.md) | **ĐÃ HOÀN TẤT ĐỐI CHUẨN** |
