# THƯ MỤC DỮ LIỆU CHUẨN CỦA DỰ ÁN (CANONICAL DATASET DIRECTORY)
## 💾 PI-Guard Dataset Pipeline

> [!IMPORTANT]
> **QUY TẮC QUẢN LÝ DỮ LIỆU (DATA GOVERNANCE)**:
> 1. Thư mục `data/` cấp gốc này lưu trữ **DỮ LIỆU CHUẨN ĐÃ ĐƯỢC CHỐT VÀ XUẤT BẢN CHÍNH THỨC** sau các kỳ đánh giá milestone.
> 2. **Trạng thái hiện tại (Review 1)**: Đang ở chế độ HOLD. Toàn bộ hoạt động thử nghiệm, thu thập mẫu và phân loại dữ liệu diễn ra độc lập trong các workspace cá nhân (`workspaces/<member>/data/`).
> 3. **Cột mốc xuất bản dữ liệu (Review 2 — Tuần 7–8)**: Sau khi nhóm chốt các nguồn benchmark và pipeline tiền xử lý, Trưởng nhóm (`nvtruongops`) sẽ chính thức merge dữ liệu chuẩn ra cây thư mục gốc `data/`.
> 4. Các file dữ liệu lớn (`.csv`, `.parquet`, `.jsonl`) được cấu hình trong `.gitignore` để không làm nặng Git repository.

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
