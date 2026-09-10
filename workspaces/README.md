# HƯỚNG DẪN BỐ TRÍ THƯ MỤC CÁ NHÂN & LIÊN KẾT HỆ THỐNG CHUNG
## Standard Workspace Layout for Member Sandboxes

Thư mục `workspaces/` này là **vùng thử nghiệm nháp cá nhân (Sandbox)** của từng thành viên.
Khi bạn thử nghiệm thành công, kết quả chuẩn hóa sẽ được chuyển vào thư mục dùng chung của dự án.

### Cấu Trúc 3 Phân Hệ Độc Tôn Trong Repository

| Phân Hệ / Đường Dẫn | Vai Trò & Chức Năng Cốt Lõi |
| :--- | :--- |
| **`Final-Report/`**<br/>*(Phân hệ Báo cáo & Mã nguồn)* | • **`src/`**: Mã nguồn sản phẩm PoC chính thức (API, Models, Preprocessing, Dashboard)<br/>• **`tests/`**: Bộ kiểm thử tự động pytest<br/>• **`scripts/`**: Bộ công cụ tự động hóa kiểm định QA & build docs portal<br/>• **`thesis/`**: Toàn văn Luận văn tốt nghiệp (FINAL_THESIS.md, Review 1, Chapters 1-6)<br/>• **`notebooks/`**: Toàn bộ tài nguyên thực nghiệm & Jupyter Notebooks tái lập<br/>• **`Meeting/`**: Biên bản họp với GVHD & nội bộ nhóm (Meeting 1, 2, 3)<br/>• **`References/`**: 18 bài báo khoa học chuẩn (PDF) & REFERENCES_LOG.md<br/>• **`reports/`**: Sổ tiến độ (PI_GUARD_PROCESS_REPORT.xlsx), slide trình chiếu & benchmark<br/>• **`figures/`**, **`tables/`**: Sơ đồ kiến trúc & bảng biểu đối chuẩn |
| **`Github-Page/`**<br/>*(Phân hệ Cổng tài liệu)* | • **`index.md`**: Trang chủ cổng tài liệu<br/>• **8 Chuyên Đề Khoa Học**: Toàn bộ nội dung chuyên đề nghiên cứu xuất bản lên web |
| **`workspaces/`**<br/>*(Phân hệ Sandbox thành viên)* | • **`truongnv/`**: Trường (Leader) — Chuẩn hóa dữ liệu, kiến trúc hệ thống, điều phối chung<br/>• **`ducnq/`**: Đức — Baseline ML TF-IDF, Threat Model & đối sánh mô hình<br/>• **`vietpmh/`**: Việt — Transformer DeBERTa-v3, Quantization INT8, Robustness<br/>• **`phuongddd/`**: Phương — FastAPI Guardrail Proxy, Streamlit Dashboard & Luận văn |

---

### Nguyên Tắc: "Nháp Tại Workspaces — Chuẩn Hóa Vào Final-Report Chung"

1. **Khi đang nghiên cứu, thử sai, debug**: Làm việc thoải mái trong `workspaces/<tên_bạn>/`.
2. **Khi code đã chạy tốt, có kết quả đẹp**: Báo cáo Leader trong buổi họp tuần để được đưa vào `Final-Report/src/` và `Final-Report/` chung để cả nhóm cùng dùng và nghiệm thu với Giảng viên hướng dẫn!
