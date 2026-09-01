# THƯ MỤC TÀI LIỆU DỰ ÁN (PROJECT DOCUMENTATION)
## 📌 Vùng Lưu Trữ Tài Liệu Chính Thức Của Toàn Dự Án PI-Guard

> [!IMPORTANT]
> **QUY TẮC BẤT DI BẤT DỊCH (TEAM RULE)**:
> 1. Thư mục `docs/` cấp gốc này chỉ dành cho **CÁC TÀI LIỆU VÀ BÁO CÁO ĐÃ ĐƯỢC CẢ NHÓM HỌP DUYỆT CHỐT CHÍNH THỨC**.
> 2. Thành viên **TUYỆT ĐỐI KHÔNG TỰ Ý ĐƯA FILE NHÁP/DRAFT CÁ NHÂN VÀO ĐÂY**.
> 3. Mọi tài liệu bản thảo đang nghiên cứu phải nằm trong `workspaces/<tên_thành_viên>/docs/`.

---

### 📂 CẤU TRÚC PHÂN CẤP THƯ MỤC:

| Thư mục con | Mục đích & Nội dung | Ghi chú & Quyền hạn |
| :--- | :--- | :--- |
| [`docs/fpt_capstone_guide/`](file:///d:/Work/Do-an/docs/fpt_capstone_guide/) | Tài liệu, biểu mẫu, rubrics hướng dẫn đồ án nội bộ FPT | **BẤT BIẾN / READ-ONLY** (Đã ignore khỏi Git) |
| [`docs/thesis/`](file:///d:/Work/Do-an/docs/thesis/) | Nơi lưu Luận văn chính thức (`FINAL_THESIS.md`) và 6 chương đã chốt | Chỉ cập nhật khi nhóm họp chốt milestone |
| [`docs/research/`](file:///d:/Work/Do-an/docs/research/) | Các bài tổng hợp nghiên cứu SOTA chính thức của nhóm | Đưa vào sau khi phản biện tuần |
| [`docs/architecture/`](file:///d:/Work/Do-an/docs/architecture/) | Tài liệu thiết kế kiến trúc hệ thống Guardrail hoàn chỉnh | Cập nhật theo từng milestone |
| [`docs/api/`](file:///d:/Work/Do-an/docs/api/) | Tài liệu đặc tả OpenAPI / Swagger cho Guardrail Proxy | Tích hợp khi hoàn thành API |
| [`docs/methodology/`](file:///d:/Work/Do-an/docs/methodology/) | Phương pháp luận thực nghiệm và giải thuật chuẩn | Đưa vào khi hoàn thành Chapter 3 |
| [`docs/experiments/`](file:///d:/Work/Do-an/docs/experiments/) | Báo cáo kết quả thử nghiệm và đối chuẩn mô hình | Đưa vào khi hoàn thành Chapter 4 |

---

### 🔄 QUY TRÌNH ĐỒNG BỘ TÀI LIỆU:
```
workspaces/<tên>/docs/  ──►  Họp Nhóm Cuối Tuần  ──►  Merge PR  ──►  docs/ (Bản Chính Thức)
```
