# THƯ MỤC MÃ NGUỒN THỰC NGHIỆM CHÍNH THỨC (ACADEMIC RESEARCH & PoC PROTOTYPE)
## PI-Guard Research Codebase & Evaluation Testbed Architecture

> [!IMPORTANT]
> **QUY CHUẨN MÃ NGUỒN NGHIÊN CỨU KHOA HỌC (RESEARCH ARTIFACT INVARIANTS)**:
> 1. Thư mục `Final-Report/src/` là **NƠI LƯU TRỮ MÃ NGUỒN THỰC NGHIỆM ĐÃ QUA KIỂM ĐỊNH (VERIFIED RESEARCH ARTIFACTS & PoC PROTOTYPE)** phục vụ tính tái lập khoa học (Research Reproducibility) theo chuẩn Papers with Code.
> 2. **Trạng thái Review 1 (Tuần 1–4)**: Duy trì khung cấu trúc phân hệ (module scaffolding) với các thư mục chức năng và `.gitkeep`. Tuyệt đối tuân thủ nguyên tắc 100% nghiên cứu lý thuyết & y văn (Zero Code in Final-Report).
> 3. Thành viên **KHÔNG ĐƯỢC CODE TRỰC TIẾP HOẶC TEST NHÁP TRONG `Final-Report/src/`**. Mọi thử nghiệm diễn ra trong `workspaces/<tên_bạn>/` và chỉ được Leader đồng quy tích hợp vào `Final-Report/src/` tại các cột mốc Review 2 và Review 3.
> 4. **Bản chất đề tài Nghiên cứu Khoa học (Research-Based Thesis IAP491)**: Lớp `api/` (FastAPI) và `dashboard/` (Streamlit) được thiết kế như một **Nguyên Mẫu Thực Nghiệm (Proof-of-Concept Prototype)** và **Môi Trường Đo Đạc Độ Trễ (Inference Latency Testbed)** nhằm phục vụ đánh giá thực nghiệm (RQ3: P95 < 20ms) và bảo vệ trước Hội đồng chấm FPT theo đúng bản đăng ký [`CAPSTONE PROJECT REGISTER.md`](file:///d:/Work/Do-an/CAPSTONE%20PROJECT%20REGISTER.md).
> 5. **Cam kết chống phình phạm vi (Anti-Scope Creep Blacklist)**: Đề tài **TUYỆT ĐỐI KHÔNG** mở rộng sang các bài toán hạ tầng phần mềm thương mại / enterprise production (không làm cơ sở dữ liệu tài khoản người dùng, không làm OAuth2/JWT/RBAC, không làm kiểm thử tải phân tán 100k RPS, không triển khai Kubernetes hay Cloud CI/CD phức tạp).

---

### Cấu Trúc Các Module Chính Trong `src/`

| Thư Mục / Module | Chức Năng & Nhiệm Vụ |
| :--- | :--- |
| `src/preprocessing/` | Tiền xử lý: Làm sạch, chuẩn hóa Unicode, bóc tách Base64 |
| `src/datasets/` | Pipeline thu thập dữ liệu, semantic deduplication & Group-Aware Split |
| `src/models/baseline/` | Bộ phân loại TF-IDF (Word/Char N-Grams) + LogisticRegression / LinearSVC |
| `src/models/classifier.py` | Wrapper chạy suy luận ONNX Runtime / PyTorch |
| `src/training/` | Pipeline huấn luyện tự động (Trainer, Callbacks, Loss) |
| `src/evaluation/` | Bộ đo lường chuẩn: F1, Precision, Recall, FPR, Latency |
| `src/policy/` | Bộ quy tắc định tuyến bảo vệ (3-Tier Layered Defense) |
| `src/api/` | Dịch vụ FastAPI Middleware & LLM Proxy (/v1/chat) |
| `src/dashboard/` | Giao diện Streamlit giám sát & kiểm thử trực quan |
| `src/llm/` | Kết nối Target LLM Cloud APIs (Groq, OpenAI, Gemini) |
| `src/utils/` | Logging, cấu hình, metrics tracker & helpers |

