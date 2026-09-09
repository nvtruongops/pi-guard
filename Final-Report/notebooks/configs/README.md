# THƯ MỤC CẤU HÌNH THỰC NGHIỆM (EXPERIMENT CONFIGURATIONS)
## ⚙️ Declarative YAML Configurations for Reproducibility

Thư mục này chứa các tệp cấu hình siêu tham số và pipeline chuẩn hóa:
- `data.yaml`: Cấu hình nguồn dữ liệu Hugging Face, nhãn và group-aware split.
- `evaluation.yaml`: Ngưỡng chặn an toàn, lát cắt đối kháng và latency profiling budget.
- `models.yaml`: Đặc tả kiến trúc Baseline (TF-IDF) và DeBERTa-v3 INT8 ONNX Engine.
- `training.yaml`: Siêu tham số huấn luyện (learning rate, epochs, batch size, weight decay).
