# THƯ MỤC DỮ LIỆU CHUẨN CỦA DỰ ÁN (CANONICAL DATASET DIRECTORY)
## 💾 PI-Guard Dataset Pipeline

> [!IMPORTANT]
> **QUY TẮC QUẢN LÝ DỮ LIỆU (DATA GOVERNANCE)**:
> 1. Thư mục `data/` cấp gốc này lưu trữ **DỮ LIỆU CHUẨN ĐÃ ĐƯỢC LÀM SẠCH, KHỬ TRÙNG LẶP VÀ CHIA CỤM GROUP-AWARE CHÍNH THỨC**.
> 2. Các file dữ liệu lớn (`.csv`, `.parquet`, `.jsonl`) được cấu hình trong `.gitignore` để không làm nặng Git repository.
> 3. Để tải và tạo dữ liệu chuẩn cho cả nhóm, chạy script:
>    ```powershell
>    python scripts/download_dataset.py
>    ```

---

### 📂 CẤU TRÚC PHÂN CẤP DỮ LIỆU:

```
data/
├── manifests/                     # Metadata, phân loại Taxonomy nhãn & danh sách nguồn HF
├── raw/                           # Dữ liệu thô tải trực tiếp từ Hugging Face
├── interim/                       # Dữ liệu trung gian đang xử lý làm sạch
├── processed/                     # Dữ liệu sạch đã chuẩn hóa và gán nhãn 3 lớp
├── splits/                        # Tập dữ liệu Train / Val / Test (Group-Aware Splitting)
├── augmentation/                  # Dữ liệu sinh tăng cường (Base64, Leetspeak, Spacing)
└── benchmarks/                    # Tập dữ liệu đối chuẩn bên ngoài (OOD Benchmarks)
```
