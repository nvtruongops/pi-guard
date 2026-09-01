# THƯ MỤC MÃ NGUỒN CHÍNH THỨC CỦA DỰ ÁN (PRODUCTION SOURCE CODE)
## 🛡️ PI-Guard Core Framework Architecture

> [!IMPORTANT]
> **QUY TẮC PHÁT TRIỂN PHẦN MỀM (DEVELOPMENT RULES)**:
> 1. Thư mục `src/` là **NƠI CHỨA MÃ NGUỒN CHÍNH THỨC, HOÀN CHỈNH VÀ ĐÃ QUA KIỂM THỬ (PRODUCTION-READY)**.
> 2. Thành viên **KHÔNG ĐƯỢC CODE TRỰC TIẾP HOẶC TEST NHÁP TRONG `src/`**.
> 3. Mọi tính năng mới, thử nghiệm thuật toán phải viết trong `workspaces/<tên_bạn>/` trước $\rightarrow$ Sau khi họp nhóm cuối tuần thống nhất mới tạo Pull Request merge vào `src/`.

---

### 📂 CẤU TRÚC CÁC MODULE CHÍNH TRONG `src/`:

```
src/
├── preprocessing/                 # Tiền xử lý: Làm sạch, chuẩn hóa Unicode, bóc tách Base64
├── datasets/                      # Pipeline cào data, deduplication & Group-Aware Split
├── models/                        # Trình bao bọc suy luận (Baseline ML & DeBERTa INT8 ONNX)
│   ├── baseline/                  # Bộ phân loại TF-IDF + LogisticRegression / LinearSVC
│   └── classifier.py              # Wrapper chạy suy luận ONNX Runtime / PyTorch
├── training/                      # Pipeline huấn luyện tự động (Trainer, Callbacks, Loss)
├── evaluation/                    # Bộ đo lường chuẩn: F1, Precision, Recall, FPR, Latency
├── policy/                        # Bộ quy tắc định tuyến bảo vệ (3-Tier Layered Defense)
├── api/                           # Dịch vụ FastAPI Middleware & LLM Proxy (/v1/chat)
├── dashboard/                     # Giao diện Streamlit giám sát & kiểm thử trực quan
├── llm/                           # Kết nối Target LLM Cloud APIs (Groq, OpenAI, Gemini)
└── utils/                         # Logging, cấu hình, metrics tracker & helpers
```

