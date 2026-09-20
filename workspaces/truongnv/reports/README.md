# MASTER REPORTS & TECHNICAL GATEWAY — TRƯƠNGNV
**PI-Guard** | Nguyễn Văn Trường (`SE182034`) | [`workspaces/truongnv/reports/`](file:///d:/Work/Do-an/workspaces/truongnv/reports/)

---

## 🏛️ 1. Cấu Trúc Phân Hệ Báo Cáo Tiến Độ

```text
workspaces/truongnv/reports/
│
├── report_for_meeting_4/                 # [PHÂN HỆ 1: KHO HỒ SƠ ĐÃ BÁO CÁO MEETING 4 (10/09/2026)]
│   ├── README.md                         # Mục lục tổng quan, biên bản tóm lược buổi họp 10/09
│   ├── PI-GUARD-Present-109.pptx         # File slide thuyết trình 22 slides chuẩn 16:9
│   ├── SUPERVISOR_REPORT_10_09_2026.md   # Báo cáo kịch bản slide-by-slide chi tiết
│   ├── figures/                          # 12 hình ảnh minh chứng khoa học trích xuất từ slide
│   │   ├── PI-GUARD-Present-109/         # (12 tệp PNG chất lượng cao)
│   │   └── README.md                     # Bảng chỉ dẫn 12 slide minh chứng
│   └── tools/                            # Bộ script tự động sinh slide và hình ảnh
│       ├── generate_presentation.py      # Script Python sinh bản thuyết trình PPTX
│       └── generate_diagrams.py          # Script Python kết xuất hình ảnh kiến trúc
│
├── tasks_for_meeting_5/                  # [PHÂN HỆ 2: TOÀN BỘ NHIỆM VỤ CHUẨN BỊ BÁO CÁO MEETING 5 (17/09/2026)]
│   ├── README.md                         # Báo cáo Master Executive & Cổng điều phối tổng thể
│   │
│   ├── task_reports/                     # Hồ sơ 4 chuyên đề nghiên cứu chi tiết (Task 1, 2, 3, 4)
│   │   ├── README.md
│   │   ├── TASK_1_PROMPT_INJECTION_VS_JAILBREAK.md  # Task 1: Phân biệt bản chất 2 bề mặt tấn công
│   │   ├── TASK_2_ATTACK_VECTORS_AND_MODELS.md      # Task 2: Khung 5D & 2 mô hình tham khảo học thuật
│   │   ├── TASK_3_REPRODUCIBILITY_AND_DATASETS.md   # Task 3: Nghiên cứu toàn diện & tái lập y văn Task 3
│   │   └── TASK_4_PIGUARD_IMPROVEMENTS.md           # Task 4: 3 Giải pháp cải tiến của đồ án PI-Guard
│   │
│   ├── task_3_replication/               # Phân hệ thực nghiệm tái lập mô hình mỏ neo PIGuard ACL 2025
│   │   ├── README.md                     # Hướng dẫn chi tiết chạy tái lập trên máy cá nhân
│   │   ├── PIGUARD_ACL2025_REPLICATION_REPORT.md  # Báo cáo đo đạc chi tiết 1.579 mẫu
│   │   ├── PIGUARD_REPLICATION_BENCHMARK_RESULTS.json # Kết quả đo đạc JSON chuẩn hóa
│   │   ├── verify_replication_assets.py  # Script kiểm định tự động toàn vẹn tài nguyên Task 3
│   │   ├── papers/                       # Bản lưu PDF chính thức PIGuard ACL 2025
│   │   ├── figures/                      # Toàn bộ biểu đồ đối chuẩn thực nghiệm
│   │   ├── docs/                         # Chuyên đề khảo sát lý thuyết (01, 02, 03, 04)
│   │   └── PIGuard_ACL2025/              # Codebase gốc, .venv Python 3.10, Datasets, Notebook
│   │
│   └── task_3_reproducibility/           # Tài liệu bóc tách lý thuyết & Runbook tái lập Task 3
│       ├── 01_LITERATURE_ASSESSMENT_TFIDF.md
│       ├── 02_CORE_ANCHOR_PIGUARD_ACL2025.md
│       ├── 03_EMBEDDING_BASELINE_AYUB2024.md
│       ├── 04_MEMBER_REPRODUCTION_RUNBOOK.md
│       └── README.md
```

---

## 🧭 2. Chỉ Mục Phân Hệ & Đường Dẫn Nhanh

| Phân Hệ | Mục Tiêu & Phạm Vi Nghiên Cứu | Đường Dẫn Chính Thức | Trạng Thái |
| :--- | :--- | :--- | :---: |
| **Phân Hệ 1 (Meeting 4 Archive)** | Lưu trữ bản trình chiếu 22 slide, báo cáo kịch bản thuyết trình và 12 hình ảnh minh chứng đã bảo vệ trực tiếp trước GVHD ngày 10/09/2026. | [`report_for_meeting_4/`](file:///d:/Work/Do-an/workspaces/truongnv/reports/report_for_meeting_4/README.md) | **ĐÃ HOÀN THÀNH** |
| **Phân Hệ 2 (Meeting 5 Tasks)** | 4 báo cáo kỹ thuật (Task 1–4) và phân hệ thực nghiệm tái lập độc lập các mô hình y văn trên máy cá nhân. | [`tasks_for_meeting_5/`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/README.md) | **ĐÃ SẴN SÀNG** |
| **Thực Nghiệm Tái Lập (Task 3)** | Mã nguồn, dữ liệu 43MB, môi trường ảo Python 3.10, Jupyter notebook và kết quả đo đạc 1.579 mẫu tái lập PIGuard (ACL 2025). | [`tasks_for_meeting_5/task_3_replication/`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/README.md) | **SẴN SÀNG KIỂM ĐỊNH** |
