# THƯ MỤC BÁO CÁO TỔNG, LUẬN VĂN & TÀI NGUYÊN THỰC NGHIỆM (`Final-Report/`)
## 📈 PI-Guard Final Report, Thesis & Experimentation Deliverables Hub

> [!NOTE]
> Thư mục `Final-Report/` là **phân hệ Báo Cáo Tổng** của dự án PI-Guard. Đây là nơi lưu trữ tập trung toàn bộ sản phẩm học thuật, hồ sơ bảo vệ, tài liệu luận văn và tài nguyên thực nghiệm phục vụ việc nghiệm thu với Giáo viên Hướng dẫn và Hội đồng Chấm Đồ án ĐH FPT (IAP491).

---

### 📂 CẤU TRÚC PHÂN HỆ BÁO CÁO TỔNG & NGHIỆM THU (`Final-Report/`):

> [!IMPORTANT]
> **QUY CHUẨN GIAI ĐOẠN REVIEW 1 (ZERO-CODE INVARIANT IN FINAL-REPORT)**:
> - Theo quy chế học thuật ĐH FPT (IAP491), giai đoạn **Review 1 (Tuần 1–4)** là giai đoạn **100% Nghiên cứu lý thuyết, Khảo sát y văn, Mô hình hóa đe dọa (Threat Modeling) và Thiết kế kiến trúc**.
> - Thư mục `Final-Report/` là phân hệ Nghiệm thu chính thức, tuân thủ nguyên tắc: **"Chỉ khi hoàn thành xong và nghiệm thu mới có code hay tài liệu chính thức ở Final-Report/"**.
> - Các module mã nguồn sản phẩm (`src/`), bộ kiểm thử tự động (`tests/`), và tài nguyên thực nghiệm (`notebooks/`) hiện đang được 4 thành viên phát triển song song trong các không gian làm việc độc lập (`workspaces/<thành_viên>/`) và sẽ được Leader đồng quy tích hợp vào `Final-Report/` tại cột mốc **Review 2 & Hội đồng Giữa kỳ**.

```
Final-Report/
├── thesis/                        # Toàn bộ hồ sơ Luận văn tốt nghiệp chính thức (Single Source of Truth)
│   ├── FINAL_THESIS.md            # Toàn văn Khóa luận tốt nghiệp (Chapters 1-6 + References)
│   ├── Review1_Problem_Definition_and_Threat_Model.md # Báo cáo Chuyên đề Đợt 1 (Định nghĩa bài toán & Threat Model)
│   ├── FPT_IAP491_Capstone_Guidelines_and_Rubrics_Summary.md # Tóm tắt quy chế & tiêu chí chấm điểm IAP491
│   ├── chapters/                  # Các chương riêng biệt (01_Introduction, 02_Literature_Review)
│   └── README.md                  # Quy chuẩn viết và biên dịch Luận văn
├── Meeting/                       # Biên bản các cuộc họp tiến độ với GVHD & nội bộ nhóm (Meeting 1, 2, 3)
│   ├── Meeting 1_29_08_26.md      # Họp khởi động đề tài & phân công Sprint 1
│   ├── Meeting 2_01_09_26.md      # Khảo sát & sàng lọc 10 bài báo khoa học, định hướng 2 mô hình
│   ├── Meeting 3_08_09_26.md      # Thống nhất nội dung & thiết kế Slide báo cáo tiến độ GVHD ngày 10/09
│   └── README.md
├── References/                    # Toàn bộ 18 bài báo khoa học toàn văn PDF & sổ nhật ký tra cứu
│   ├── *.pdf                      # 18 file PDF toàn văn các bài báo học thuật chuẩn IEEE/ACM/NeurIPS/ICLR
│   ├── REFERENCES_LOG.md          # Bảng tra cứu & ma trận ánh xạ 18 bài báo vào các module trong đề tài
│   └── README.md
├── reports/                       # [PERIODIC REPORTS & METRICS] Sổ tiến độ, slide trình chiếu & benchmark
│   ├── PI-GUARD-Present-109.pptx  # Slide báo cáo tiến độ gặp GVHD ngày 10/09/2026 (22 slides, Dark Slate Navy)
│   ├── PI_GUARD_PROCESS_REPORT.xlsx # Sổ theo dõi tiến độ công việc chính thức (FPT IAP491 Process Report)
│   ├── experiment_reports/        # Thư mục lưu trữ kết quả thực nghiệm tự động (khi hoàn thành Review 2/3)
│   └── README.md                  # Hướng dẫn chi tiết phân hệ báo cáo định kỳ
├── figures/                       # Sơ đồ kiến trúc, biểu đồ ROC-AUC, biểu đồ độ trễ dạng PNG chất lượng cao
│   └── PI-GUARD-Present-109/      # 12 ảnh sơ đồ, biểu đồ trích xuất từ slide trình chiếu ngày 10/09/2026
├── tables/                        # Bảng số liệu đối chuẩn định dạng Markdown và LaTeX
├── scripts/                       # [TOOLING & QA] Bộ công cụ kiểm định Local QA, xuất bản tài liệu & quy trình
│   ├── validate_local.py          # Unified Local QA Suite (Boundaries, Manifests, Lint, Pytest, Docs)
│   ├── audit_workspace_boundaries.py # Kiểm toán phân quyền workspace & commit
│   ├── build_docs_portal.py       # Tự động tổng hợp và biên dịch tài liệu MkDocs
│   ├── compile_thesis.py          # Biên dịch các chương thành luận văn hoàn chỉnh
│   ├── verify_resource_url.py     # Công cụ kiểm định URL, video YouTube và tra cứu Open-Access PDF
│   ├── audit_urls.py              # Quét toàn diện tính hợp lệ của tất cả URL trong repo
│   ├── generate_process_report.py # Sinh sổ theo dõi tiến độ chính thức PI_GUARD_PROCESS_REPORT.xlsx
│   ├── generate_personal_process_report.py # Sinh báo cáo tiến độ cá nhân hóa từng thành viên
│   └── sync_google_sheet.py       # Đồng bộ dữ liệu tiến độ lên Google Sheet phục vụ GVHD
├── requirements.txt               # Master Production Dependencies
├── requirements-dev.txt           # Master Dev Dependencies (Pytest, Ruff, Pre-commit, MkDocs)
└── .env.example                   # Master Environment Configuration Template
```


---

### 📢 LƯU Ý VỀ TÀI LIỆU TRÌNH CHIẾU:
> [!IMPORTANT]
> - Tệp [`PI-GUARD-Present-109.pptx`](file:///d:/Work/Do-an/Final-Report/reports/PI-GUARD-Present-109.pptx) là **SLIDE BÁO CÁO TIẾN ĐỘ ĐỊNH KỲ VỚI GIÁO VIÊN HƯỚNG DẪN (GVHD) TRONG BUỔI GẶP NGÀY 10/09/2026**.
> - Tài liệu này được nhóm sử dụng để báo cáo tình hình nghiên cứu, cơ sở lý thuyết chọn mô hình và kiến trúc đề xuất nhằm xin ý kiến chỉ đạo, định hướng chuyên môn từ GVHD.
> - **ĐÂY KHÔNG PHẢI LÀ SLIDE BÁO CÁO REVIEW 1 TRƯỚC HỘI ĐỒNG**: Buổi bảo vệ Review 1 chính thức trước Hội đồng FPT University sẽ diễn ra ở cột mốc sau; slide Review 1 chính thức sẽ được nhóm hoàn thiện và đóng gói riêng sau khi tiếp thu các nhận xét của GVHD.
