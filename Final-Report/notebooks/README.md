# THƯ MỤC JUPYTER NOTEBOOKS THỰC NGHIỆM (REPRODUCIBLE EXPERIMENT ROADMAP)
## 📓 Kế Hoạch 5 Notebooks Thực Nghiệm Tái Lập & Tài Nguyên Tương Ứng — Dự Án PI-Guard

> [!NOTE]
> **TRẠNG THÁI HIỆN TẠI (PHASE 1: REVIEW 1)**:
> - Dự án hiện đang trong giai đoạn **Review 1 (Tuần 1 – Tuần 4)**: Tập trung vào *Xác định bài toán (Problem Statement)*, *Mô hình hóa mối đe dọa (Threat Modeling)* và *Khảo sát các giải pháp SOTA (Literature Review)*.
> - Các file notebooks chuẩn trong thư mục này sẽ được cả 4 thành viên phát triển và hoàn thiện tuần tự từ **Review 2 (Tuần 5)** và **Báo cáo Hội đồng 1 (Tuần 8 – 12)**.

---

### 📂 CẤU TRÚC THƯ MỤC TÀI NGUYÊN THỰC NGHIỆM (`notebooks/`)

Để tinh gọn tầng gốc repository và gom toàn bộ tài nguyên huấn luyện / thực nghiệm vào một không gian khép kín, thư mục `notebooks/` quản lý trực tiếp 3 phân hệ tài nguyên phục vụ các thí nghiệm:

```
notebooks/
├── README.md                      # Kế hoạch thực nghiệm và quy chế vận hành
├── configs/                       # Cấu hình siêu tham số và pipeline thực nghiệm
│   ├── data.yaml                  # Cấu hình nguồn dữ liệu, nhãn và group-aware split
│   ├── evaluation.yaml            # Ngưỡng chặn an toàn, lát cắt đối kháng và latency budget
│   ├── models.yaml                # Cấu hình kiến trúc Baseline và DeBERTa-v3
│   └── training.yaml              # Hyperparameters huấn luyện (LR, epochs, batch size)
├── data/                          # Kho dữ liệu thực nghiệm tái lập (Datasets)
│   ├── augmentation/              # Dữ liệu tăng cường (Obfuscation, Leetspeak, DAN)
│   ├── benchmarks/                # Dữ liệu đối chuẩn bảo mật SOTA
│   ├── interim/                   # Dữ liệu trung gian sau tiền xử lý
│   ├── manifests/                 # Tệp JSON manifest kiểm kê nguồn gốc dữ liệu
│   ├── processed/                 # Dữ liệu sạch đã chuẩn hóa và loại bỏ trùng lặp
│   ├── raw/                       # Dữ liệu thô tải từ Hugging Face
│   └── splits/                    # Phân chia dữ liệu (train.csv, val.csv, test.csv)
└── models/                        # Trọng số và artifact mô hình sau huấn luyện
    ├── baseline/                  # Checkpoint TF-IDF + Logistic Regression/SVM (.joblib)
    ├── onnx/                      # Mô hình lượng hóa INT8 ONNX Engine (P95 < 18.5ms)
    └── transformer/               # Trọng số PyTorch DeBERTa-v3 fine-tuned
```

---

### 🗺️ LỘ TRÌNH 5 NOTEBOOKS SẼ ĐƯỢC XÂY DỰNG TRONG CÁC GIAI ĐOẠN TỚI:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│               LỘ TRÌNH 5 JUPYTER NOTEBOOKS TÁI LẬP KẾT QUẢ THỰC NGHIỆM                  │
├──────┬─────────────────────────────────┬─────────────────┬─────────────────────────────┤
│ STT  │ Tên Notebook (Chuẩn hóa)        │ Cột Mốc Triển   │ Mục Đích Nghiên Cứu         │
├──────┼─────────────────────────────────┼─────────────────┼─────────────────────────────┤
│ 01   │ `01_dataset_analysis.ipynb`     │ 🎯 Review 2     │ Khám phá dữ liệu (EDA), đo  │
│      │                                 │ (Tuần 5 - 6)    │ phân phối token & rò rỉ     │
├──────┼─────────────────────────────────┼─────────────────┼─────────────────────────────┤
│ 02   │ `02_baseline.ipynb`             │ 🎯 Review 2     │ Huấn luyện Baseline ML:     │
│      │                                 │ (Tuần 6 - 7)    │ TF-IDF + Logistic / SVM     │
├──────┼─────────────────────────────────┼─────────────────┼─────────────────────────────┤
│ 03   │ `03_transformer_training.ipynb` │ 🏛️ Hội Đồng 1   │ Fine-tune DeBERTa-v3 & nén  │
│      │                                 │ (Tuần 8 - 10)   │ lượng hóa INT8 ONNX Engine  │
├──────┼─────────────────────────────────┼─────────────────┼─────────────────────────────┤
│ 04   │ `04_ablation.ipynb`             │ 🏛️ Hội Đồng 1   │ Nghiên cứu triệt tiêu: đo   │
│      │                                 │ (Tuần 11 - 12)  │ vai trò Base64 & 3L Defense │
├──────┼─────────────────────────────────┼─────────────────┼─────────────────────────────┤
│ 05   │ `05_error_analysis.ipynb`       │ 🎓 Hội Đồng     │ Phân tích ca chặn nhầm FPR  │
│      │                                 │ Final (Tuần 14) │ & lọt lưới False Negatives  │
└──────┴─────────────────────────────────┴─────────────────┴─────────────────────────────┘
```

---

### 🛡️ QUY CHẾ VẬN HÀNH:
1. **Giai đoạn thử nghiệm nháp**: Từng thành viên code nháp trong `workspaces/<tên_thành_viên>/`.
2. **Giai đoạn nghiệm thu chuẩn hóa**: Khi code chạy ổn định và đạt kết quả tốt, cả nhóm họp thống nhất và đưa vào notebook chuẩn tương ứng tại thư mục này để Giảng viên hướng dẫn & Hội đồng chạy nghiệm thu tái lập kết quả!
