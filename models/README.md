# THƯ MỤC TRỌNG SỐ MÔ HÌNH (TRAINED MODEL CHECKPOINTS)
## 🧠 PI-Guard Model Artifacts & INT8 ONNX Engine

> [!IMPORTANT]
> **QUY TẮC QUẢN LÝ MÔ HÌNH (MODEL ARTIFACTS RULE)**:
> 1. Thư mục này chứa các trọng số mô hình **ĐÃ HUẤN LUYỆN VÀ TỐI ƯU HÓA HOÀN CHỈNH**.
> 2. Các file nhị phân lớn (`.bin`, `.safetensors`, `.onnx`, `.joblib`) được bỏ qua bởi `.gitignore` để không làm phình dung lượng repo Git.
> 3. Để tải hoặc xuất mô hình chuẩn, chạy pipeline trong `src/models/` hoặc `scripts/`.

---

### 📂 CẤU TRÚC LƯU TRỮ MÔ HÌNH:

```
models/
├── baseline/                      # Trọng số mô hình Scikit-Learn TF-IDF (`.joblib`, `.pkl`)
├── transformer/                   # Checkpoint PyTorch / Hugging Face DeBERTa-v3 (`best_model/`)
└── onnx/                          # Mô hình nén INT8 Dynamic Quantized (`model_quantized.onnx`)
```
