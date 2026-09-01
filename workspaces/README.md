# HƯỚNG DẪN BỐ TRÍ THƯ MỤC CÁ NHÂN & LIÊN KẾT HỆ THỐNG CHUNG
## Standard Workspace Layout for Member Sandboxes

Thư mục `workspaces/` này là **vùng thử nghiệm nháp cá nhân (Sandbox)** của từng thành viên.
Khi bạn thử nghiệm thành công, kết quả chuẩn hóa sẽ được chuyển vào thư mục dùng chung của dự án.

```
d:/Work/Do-an/
├── data/                          # [CHUNG] Dữ liệu chuẩn thức của cả nhóm (raw, processed, splits)
├── src/                           # [CHUNG] Mã nguồn sản phẩm chính thức (API, Models, Preprocessing)
├── notebooks/                     # [CHUNG] 5 Jupyter Notebooks chuẩn hóa, có thể chạy tái lập (Reproducible)
│   ├── 01_dataset_analysis.ipynb
│   ├── 02_baseline.ipynb
│   ├── 03_transformer_training.ipynb
│   ├── 04_ablation.ipynb
│   └── 05_error_analysis.ipynb
├── experiments/                   # [CHUNG] Kết quả đo đạc chính thức nhúng vào Luận văn (runs, metrics, plots)
│
└── workspaces/                    # [RIÊNG] Không gian thử nghiệm nháp cá nhân của 4 bạn
    ├── truong_data_eng/           # • Trường: Thử nghiệm cào data, thuật toán split, EDA nháp
    ├── duc_baseline_ml/           # • Đức: Thử nghiệm trích xuất TF-IDF, so sánh mô hình ML nháp
    ├── viet_transformer_robustness/ # • Việt: Thử nghiệm fine-tune DeBERTa, nén INT8, test payload nháp
    └── phuong_api_dashboard/      # • Phương: Thử nghiệm dựng API endpoint, UI Streamlit nháp
```

### 💡 NGUYÊN TẮC: "NHÁP TẠI WORKSPACES — CHUẨN HÓA VÀO SRC & NOTEBOOKS CHUNG"
1. **Khi đang nghiên cứu, thử sai, debug**: Làm việc thoải mái trong `workspaces/<tên_bạn>/`.
2. **Khi code đã chạy tốt, có kết quả đẹp**: Đưa vào `src/` và `notebooks/` chung để cả nhóm cùng dùng và nghiệm thu với Giảng viên hướng dẫn!
