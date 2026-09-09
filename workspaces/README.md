# HƯỚNG DẪN BỐ TRÍ THƯ MỤC CÁ NHÂN & LIÊN KẾT HỆ THỐNG CHUNG
## Standard Workspace Layout for Member Sandboxes

Thư mục `workspaces/` này là **vùng thử nghiệm nháp cá nhân (Sandbox)** của từng thành viên.
Khi bạn thử nghiệm thành công, kết quả chuẩn hóa sẽ được chuyển vào thư mục dùng chung của dự án.

```
d:/Work/Do-an/
├── reports/                       # [1. BÁO CÁO TỔNG] Báo cáo tiến độ, slides, figures, tables, Meeting/ & References/
│   ├── Meeting/                   # Biên bản họp với GVHD & nội bộ nhóm (Meeting 1, 2, 3)
│   ├── References/                # 18 bài báo khoa học chuẩn (PDF) & REFERENCES_LOG.md
│   ├── PI-GUARD-Present-109.pptx  # Slide báo cáo tiến độ gặp GVHD ngày 10/09/2026
│   ├── PI_GUARD_PROCESS_REPORT.xlsx # Sổ theo dõi tiến độ chính thức (Process Report)
│   ├── figures/                   # Sơ đồ kiến trúc & hình ảnh trích xuất
│   ├── tables/                    # Bảng biểu đối chuẩn
│   └── experiment_reports/        # Kết quả thực nghiệm
│
├── workspaces/                    # [2. WORKSPACE THÀNH VIÊN] Không gian thử nghiệm sandbox cá nhân của 4 bạn
│   ├── truongnv/                  # • Trường (Leader): Chuẩn hóa dữ liệu, kiến trúc hệ thống, điều phối chung
│   ├── ducnq/                     # • Đức: Baseline ML TF-IDF, Threat Model & đối sánh mô hình
│   ├── vietpmh/                   # • Việt: Transformer DeBERTa-v3, Quantization INT8, Robustness
│   └── phuongddd/                 # • Phương: FastAPI Guardrail Proxy, Streamlit Dashboard & Luận văn
│
├── docs/                          # [3. GITHUB PAGES] Cổng tài liệu Web UI chính thức (MkDocs Material 8 Chuyên Đề)
│   ├── index.md                   # Trang chủ cổng tài liệu
│   ├── fpt_capstone_guide/        # Tài liệu nội bộ FPT (BẤT BIẾN / READ-ONLY)
│   └── [8 Chuyên Đề Khoa Học]/    # Prompt, Attacks, Threat & Defense, Dataset, Models, Robustness, Optimization, Evaluation
│
├── src/                           # [CORE CODEBASE] Mã nguồn sản phẩm chính thức (API, Models, Preprocessing, Dashboard)
├── notebooks/                     # [EXPERIMENTS] Jupyter Notebooks (01_eda..05_errors, configs/, data/, models/)
├── tests/                         # [AUTOMATION TEST] Bộ kiểm thử tự động pytest
└── scripts/                       # [DEVOPS & UTILITIES] Bộ công cụ tự động hóa kiểm định QA & build docs portal
```

### 💡 NGUYÊN TẮC: "NHÁP TẠI WORKSPACES — CHUẨN HÓA VÀO SRC & NOTEBOOKS CHUNG"
1. **Khi đang nghiên cứu, thử sai, debug**: Làm việc thoải mái trong `workspaces/<tên_bạn>/`.
2. **Khi code đã chạy tốt, có kết quả đẹp**: Đưa vào `src/` và `notebooks/` chung để cả nhóm cùng dùng và nghiệm thu với Giảng viên hướng dẫn!
