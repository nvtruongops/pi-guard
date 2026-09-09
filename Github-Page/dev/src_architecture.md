# THƯ MỤC MÃ NGUỒN CHÍNH THỨC CỦA DỰ ÁN (PRODUCTION SOURCE CODE)
## 🛡️ PI-Guard Core Framework Architecture

> [!IMPORTANT]
> **QUY TẮC BẢO TRÌ & ĐỒNG QUY MÃ NGUỒN (CONVERGENCE INVARIANT)**:
> 1. Thư mục `Final-Report/src/` là **NƠI CHỨA MÃ NGUỒN CHÍNH THỨC, HOÀN CHỈNH VÀ ĐÃ QUA KIỂM THỬ (PRODUCTION-READY)**.
> 2. Theo quy chuẩn học thuật FPT IAP491, trong giai đoạn **Review 1 (Problem Definition & Threat Modeling)**, dự án tuân thủ nghiêm ngặt **Quy tắc 100% Nghiên cứu lý thuyết & y văn (Zero Code in Final-Report)**.
> 3. Toàn bộ quá trình thử nghiệm, tiền xử lý dữ liệu, huấn luyện mô hình (TF-IDF Baseline, DeBERTa-v3) và xây dựng API proxy được 4 thành viên thực hiện song song trong các không gian làm việc độc lập (`workspaces/<thành_viên>/`).
> 4. **CHỈ KHI HOÀN THÀNH XONG VÀ NGHIỆM THU**, mã nguồn xuất sắc nhất mới được Leader đồng quy và tích hợp vào `Final-Report/src/` tại các cột mốc Review 2 và Review 3.

---

### 📂 THIẾT KẾ CẤU TRÚC CÁC MODULE DỰ KIẾN TRONG `src/`:

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
