# HƯỚNG DẪN BỐ TRÍ THƯ MỤC CÁ NHÂN & LIÊN KẾT HỆ THỐNG CHUNG
## Standard Workspace Layout for Member Sandboxes

Thư mục `workspaces/` này là **vùng thử nghiệm nháp cá nhân (Sandbox)** của từng thành viên.
Khi bạn thử nghiệm thành công, kết quả chuẩn hóa sẽ được chuyển vào thư mục dùng chung của dự án.

```
d:/Work/Do-an/
├── notebooks/                     # [CHUNG] Thực nghiệm tái lập (01_eda..05_errors, configs/, data/, models/)
│   ├── configs/                   # Siêu tham số và cấu hình pipeline
│   ├── data/                      # Dữ liệu chuẩn thức của cả nhóm (raw, processed, splits)
│   └── models/                    # Trọng số mô hình sau huấn luyện (baseline, onnx, transformer)
├── src/                           # [CHUNG] Mã nguồn sản phẩm chính thức (API, Models, Preprocessing)
├── reports/                       # [CHUNG] Báo cáo tiến độ, slides, figures, tables & kết quả thực nghiệm
├── References/                    # [CHUNG] 18 bài báo khoa học chuẩn (PDF) & REFERENCES_LOG.md
│
└── workspaces/                    # [RIÊNG] Không gian thử nghiệm nháp cá nhân của 4 bạn
    ├── truongnv/                  # • Trường (Leader): Thử nghiệm cào data, thuật toán split, EDA nháp & điều phối
    ├── ducnq/                     # • Đức: Thử nghiệm trích xuất TF-IDF, so sánh mô hình ML nháp
    ├── vietpmh/                   # • Việt: Thử nghiệm fine-tune DeBERTa, nén INT8, test payload nháp
    └── phuongddd/                 # • Phương: Thử nghiệm dựng API endpoint, UI Streamlit nháp
```

### 💡 NGUYÊN TẮC: "NHÁP TẠI WORKSPACES — CHUẨN HÓA VÀO SRC & NOTEBOOKS CHUNG"
1. **Khi đang nghiên cứu, thử sai, debug**: Làm việc thoải mái trong `workspaces/<tên_bạn>/`.
2. **Khi code đã chạy tốt, có kết quả đẹp**: Đưa vào `src/` và `notebooks/` chung để cả nhóm cùng dùng và nghiệm thu với Giảng viên hướng dẫn!
