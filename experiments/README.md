# THƯ MỤC KẾT QUẢ THỰC NGHIỆM ĐỐI CHUẨN (EXPERIMENT BENCHMARKS & RUNS)
## 📊 PI-Guard Metrics, Confusion Matrices & Ablation Logs

> [!IMPORTANT]
> **QUY TẮC LƯU TRỮ THỰC NGHIỆM (EXPERIMENT LOGGING)**:
> 1. Thư mục `experiments/` này là **NƠI LƯU TRỮ KẾT QUẢ ĐO ĐẠC CHÍNH THỨC DÙNG ĐỂ NHÚNG VÀO LUẬN VĂN (`FINAL_THESIS.md`)**.
> 2. Các file log tạm thời, wandb cache cá nhân phải để trong `workspaces/<tên_bạn>/` hoặc được cấu hình trong `.gitignore`.

---

### 📂 CẤU TRÚC PHÂN CẤP THỰC NGHIỆM:

```
experiments/
├── runs/                          # Log tham số huấn luyện chính thức (loss curves, learning rates)
├── benchmarks/                    # Bảng so sánh chỉ số F1, Precision, Recall, FPR, Latency giữa các model
├── ablations/                     # Kết quả đo đạc đóng góp của từng thành phần (Ablation Results)
└── error_analysis/                # Danh sách các ca dự đoán sai và ma trận nhầm lẫn (Confusion Matrices)
```
