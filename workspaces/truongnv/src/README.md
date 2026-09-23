# THƯ MỤC MÃ NGUỒN CHÍNH THỨC CỦA DỰ ÁN (ACADEMIC POC & PRODUCT BENCHMARK SOURCE CODE)
## 🛡️ PI-Guard Core Framework Architecture

> [!IMPORTANT]
> **QUY TẮC PHÂN HỆ VÀ RANH GIỚI BẤT BIẾN**:
> 1. Thư mục `Final-Report/src/` là **NƠI CHỨA MÃ NGUỒN CHÍNH THỨC, HOÀN CHỈNH VÀ ĐÃ QUA KIỂM THỬ (ACADEMIC-POC-PROTOTYPE)**.
> 2. Thành viên **KHÔNG ĐƯỢC CODE TRỰC TIẾP HOẶC TEST NHÁP TRONG `Final-Report/src/`**.
> 3. Mọi tính năng mới, thử nghiệm thuật toán phải viết trong `workspaces/<tên_bạn>/` trước $\rightarrow$ Sau khi họp nhóm cuối tuần thống nhất mới tạo Pull Request merge vào `Final-Report/src/`.

---

### 📂 CẤU TRÚC CÁC MODULE CHÍNH TRONG `src/`:

```
src/
├── preprocessing/                 # Tiền xử lý: Làm sạch, chuẩn hóa Unicode, bóc tách Base64
├── models/                        # Trình bao bọc suy luận (Baseline ML & Transformer INT8 ONNX)
│   ├── classifier.py              # Wrapper chạy suy luận ONNX Runtime / PyTorch
│   ├── frontier_tradeoff_guardrails.py # Đối chuẩn các mô hình guardrail
│   └── transformer_models.py      # Các lớp nạp kiến trúc Transformer
├── evaluation/                    # Bộ đo lường chuẩn: F1, Precision, Recall, FPR, Latency
├── policy/                        # Bộ quy tắc định tuyến bảo vệ (Layered Defense Routing)
├── api/                           # Dịch vụ FastAPI Middleware & LLM Proxy (/v1/chat)
├── dashboard/                     # Giao diện Streamlit giám sát & kiểm thử trực quan
├── llm/                           # Kết nối Target LLM Cloud APIs (Groq, OpenAI, Gemini)
└── utils/                         # Logging, cấu hình, metrics tracker & helpers
```

