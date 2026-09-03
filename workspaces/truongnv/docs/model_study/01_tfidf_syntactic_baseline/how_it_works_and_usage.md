# HƯỚNG DẪN CÁCH HOẠT ĐỘNG & TRIỂN KHAI: TF-IDF BASELINE TRONG PI-GUARD

---

## 🔄 1. QUY TRÌNH HOẠT ĐỘNG TỪNG BƯỚC (END-TO-END PIPELINE)

Trong kiến trúc của PI-Guard, Bộ lọc Cú pháp TF-IDF Baseline đóng vai trò là **Phòng tuyến Lọc Thô Cấp 1 (Tier 1 Coarse-Grained Filter)**:

```
[Raw User Prompt]
       │
       ▼
┌────────────────────────────────────────────────────────┐
│ BƯỚC 1: TIỀN XỬ LÝ & CHUẨN HÓA KÝ TỰ (PREPROCESSING)   │
│ • Unicode Normalization (NFC/NFKC)                     │
│ • Lowercase, loại bỏ zero-width characters (\u200b)     │
│ • Giải mã Heuristic nếu phát hiện Base64 / Hex         │
└────────────────────────────────────────────────────────┘
       │
       ▼
┌────────────────────────────────────────────────────────┐
│ BƯỚC 2: TRÍCH XUẤT ĐẶC TRƯNG LAI (FEATURE EXTRACTION) │
│ • Nhánh 1: Word n-grams (1, 2)                         │
│ • Nhánh 2: Character-with-boundary n-grams (3, 5)      │
│ • Ghép đặc trưng qua FeatureUnion -> Vector thưa thớt   │
└────────────────────────────────────────────────────────┘
       │
       ▼
┌────────────────────────────────────────────────────────┐
│ BƯỚC 3: PHÂN LOẠI TUYẾN TÍNH (CLASSIFIER INFERENCE)    │
│ • Tích vô hướng z = w^T * x + b                        │
│ • Tính xác suất qua Sigmoid: P(Injection | x)          │
│ • Thời gian thực thi: ~2.8ms - 3.5ms                   │
└────────────────────────────────────────────────────────┘
       │
       ▼
┌────────────────────────────────────────────────────────┐
│ BƯỚC 4: RA QUYẾT ĐỊNH & ĐIỀU PHỐI (DISPATCH LOGIC)     │
│ • Nếu P > 0.85: ĐÁNH CHẶN NGAY (Early Exit, 0 GPU)     │
│ • Nếu 0.15 <= P <= 0.85: Chuyển sang Tầng 2 (DeBERTa) │
│ • Nếu P < 0.15: Chuyển thẳng sang LLM                  │
└────────────────────────────────────────────────────────┘
```

---

## 🛠️ 2. CẤU HÌNH THAM SỐ TỐI ƯU TRONG SCIKIT-LEARN

Dưới đây là cấu hình tham số chuẩn được tối ưu hóa riêng cho bài toán bảo vệ an toàn LLM:

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.linear_model import LogisticRegression
import joblib

def build_pi_guard_baseline():
    # Trích xuất đặc trưng lai: kết hợp cả cụm từ và lát cắt ký tự
    features = FeatureUnion([
        ('word_level', TfidfVectorizer(
            analyzer='word',
            ngram_range=(1, 2),        # Bắt cả unigram ("ignore") và bigram ("ignore previous")
            max_features=15000,        # Giới hạn kích thước từ vựng để model nhẹ
            sublinear_tf=True,         # Thu nhỏ độ chênh lệch của từ lặp lại nhiều lần
            strip_accents='unicode'
        )),
        ('char_level', TfidfVectorizer(
            analyzer='char_wb',        # Ký tự có ranh giới từ (chống leetspeak)
            ngram_range=(3, 5),        # Lát cắt từ 3 đến 5 ký tự liên tiếp
            max_features=35000,        # Đảm bảo độ phủ rộng các biến dị ký tự
            sublinear_tf=True
        ))
    ])

    # Bộ phân loại hồi quy Logistic cân bằng trọng số
    classifier = LogisticRegression(
        C=2.0,                         # Điều chuẩn L2 tối ưu
        max_iter=1000,
        class_weight='balanced',       # Tự động cân bằng nếu dữ liệu tiêm nhiễm ít hơn
        solver='lbfgs',
        random_state=42
    )

    return Pipeline([
        ('vectorizer', features),
        ('classifier', classifier)
    ])
```

---

## 💾 3. QUẢN LÝ LƯU TRỮ VÀ TRIỂN KHAI PRODUCTION

- **Lưu mô hình**:
  ```python
  pipeline.fit(X_train, y_train)
  joblib.dump(pipeline, "models/tfidf_baseline_model.joblib", compress=3)
  ```
- **Tải và suy luận trong FastAPI**:
  ```python
  # Load model vào RAM khi khởi động API server (chỉ tốn ~15 MB RAM)
  model = joblib.load("models/tfidf_baseline_model.joblib")

  # Suy luận siêu tốc
  probs = model.predict_proba([user_prompt])[0]
  injection_risk = probs[1]
  ```

---

## ⚖️ 4. ĐÁNH GIÁ THỰC TẾ: ĐIỂM MẠNH & ĐIỂM HẠN CHẾ

| Khía Cạnh | Đánh Giá Thực Tế | Lý Do Kỹ Thuật |
| :--- | :---: | :--- |
| **Tốc độ (Latency)** | 🟢 **Siêu tốc (~3.2ms)** | Chỉ là các phép tính băm chuỗi ký tự và nhân ma trận thưa thớt trên CPU. |
| **Tài nguyên (RAM/GPU)** | 🟢 **Gần như 0 (Zero-GPU)** | Model chỉ chiếm ~15MB RAM, chạy được trên cả Raspberry Pi / CPU yếu. |
| **Chống Leetspeak/Spacing** | 🟢 **Xuất sắc (>90%)** | `char_wb` bóc tách các n-grams ký tự trùng khớp bất chấp ký tự lạ. |
| **Bắt Ngữ Cảnh Tinh Vi** | 🔴 **Kém** | Không hiểu ngữ cảnh sâu (Context-Blind). Nếu câu lệnh dài và phức tạp, TF-IDF có thể bỏ sót. |
| **Tỷ lệ Báo động Nhầm (FPR)**| 🔴 **Cao (7% - 25%)** | Nếu câu hỏi nghiên cứu bảo mật hợp lệ ("Explain prompt injection risks"), TF-IDF dễ bắt nhầm từ khóa. |

👉 **KẾT LUẬN KIẾN TRÚC**: TF-IDF không bao giờ nên đứng một mình làm giải pháp duy nhất. Nó được sinh ra để làm **Tầng 1 hỗ trợ cho DeBERTa-v3 ở Tầng 2**, tạo nên hệ thống phòng thủ 2 lớp toàn diện.
