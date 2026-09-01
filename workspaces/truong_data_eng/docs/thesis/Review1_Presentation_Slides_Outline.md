# KỊCH BẢN & NỘI DUNG SLIDE THUYẾT TRÌNH REVIEW 1
## BÁO CÁO TOÀN DIỆN 2 CHƯƠNG (REPORT NO. 1: INTRODUCTION & REPORT NO. 2: LITERATURE REVIEW)
### ĐỀ TÀI: PI-Guard — A Machine-Learning Guardrail for Detecting Prompt Injection and Jailbreak Attacks on LLM Applications

**Thời lượng dự kiến**: 15 phút trình bày + 10 phút hỏi đáp Hội đồng  
**Phân công thuyết trình 4 thành viên (Phụ trách 2 Chương Luận văn)**:
- **Nguyễn Văn Trường (Leader)**: Slide 1 - 3 *(Giới thiệu, Bối cảnh, Lỗ hổng Von Neumann, 4 Tầng Thiệt hại, Phân loại Taxonomy — Chapter 1)*
- **Nguyễn Quí Đức**: Slide 4 - 5 *(Threat Model, Attack Surface, Khảo sát SOTA Guardrails, Kiến trúc bảo vệ 3 lớp & Robustness — Chapter 2)*
- **Phạm Minh Hoàng Việt**: Slide 6 - 7 *(Model Selection Matrix, Benchmark 5 Target LLM qua Cloud API & Ma trận 4 Kịch bản Demo — Chapter 2)*
- **Đỗ Đoàn Duy Phương**: Slide 8 - 9 *(3 Research Questions IEEE, 3 Research Gaps, 4 Đóng góp mới, Ranh giới Scope & Kế hoạch)*

---

### Slide 1: Trang Tiêu Đề & Thành Viên Nhóm (Trường trình bày)
- **Tên đề tài**: *A Machine-Learning Guardrail for Detecting Prompt Injection and Jailbreak Attacks on LLM Applications (PI-Guard)*
- **Mã đề tài**: `IAP491_FA26_PI_GUARD`
- **Giảng viên hướng dẫn**: [Tên Thầy/Cô Hướng dẫn]
- **Nhóm sinh viên thực hiện**:
  - Nguyễn Văn Trường (Leader - SE182034) — *Kiến trúc, Dataset & Phụ trách Report No.1, No.2*
  - Nguyễn Quí Đức (SE182087) — *Mô hình Baseline Machine Learning & Report No.3*
  - Phạm Minh Hoàng Việt (SE181851) — *Transformer, Robustness & Report No.4*
  - Đỗ Đoàn Duy Phương (SE180235) — *FastAPI Middleware, Dashboard & Report No.5, No.6*
- **Điểm nhấn mở đầu**: *"Kính thưa Hội đồng, báo cáo Review 1 của nhóm PI-Guard hôm nay bao gồm toàn diện 2 Chương đầu tiên của Khóa luận: Chapter 1 (Introduction) và Chapter 2 (Literature Review), giải quyết lỗ hổng bảo mật số 1 của ứng dụng Generative AI với độ trễ P95 < 30ms trên CPU."*

---

### Slide 2: Bối Cảnh, Lỗ Hổng Von Neumann & 4 Tầng Thiệt Hại Thực Tế (Chapter 1 — Trường trình bày)
- **Bản chất kỹ thuật (Lỗ hổng Von Neumann trong NLP)**:
  - LLM ghép chung System Instruction ($S$) và User Data ($U$) thành chuỗi token phẳng ($X = S \mathbin{\Vert} U$).
  - Không có ranh giới phần cứng hay phân tách quyền hạn (Privilege Separation) giữa Code và Data.
- **4 Tầng Thiệt hại Thực tế Đối với Doanh nghiệp & Ứng dụng AI**:
  1. *Rò rỉ Bí mật Trí tuệ (IP) & Master API Keys*: Mất System Prompt bí mật, lộ API credentials (như vụ Sydney Bing Chat).
  2. *Chiếm quyền điều khiển Tác tử AI (Agent Goal Hijacking)*: Ép AI Agent chuyển tiền tự động, truy vấn trái phép database, xóa dữ liệu khách hàng.
  3. *Tấn công cạn kiệt tài nguyên (Denial-of-Wallet)*: Bơm prompt ép mô hình sinh văn bản lặp vô tận, gây hóa đơn API hàng chục nghìn USD.
  4. *Chế tài Pháp lý & Mất uy tín (Compliance Fines)*: Ép AI sinh mã độc hoặc nội dung cấm, vi phạm nghiêm trọng EU AI Act và GDPR.

---

### Slide 3: Phân Biệt Prompt Injection vs. Jailbreak (Chapter 1 & 2 — Trường trình bày)
- **Bảng so sánh 3 trục chuẩn OWASP LLM01:2025**:
  1. *Direct Prompt Injection*: Tấn công trực tiếp vào ô chat để chiếm quyền điều khiển logic và trích xuất System Prompt (Perez 2022 [[3]](#ref3)).
  2. *Indirect Prompt Injection*: Payload độc hại nằm ẩn trong tài liệu RAG, trang web, email mà LLM đọc được (Greshake 2023 [[4]](#ref4), Tencent Zhuque Lab 2026 [[6]](#ref6)).
  3. *Jailbreak*: Tấn công bẻ khóa an toàn nội dung (DAN roleplay, tình huống giả định, Base64/Cipher) ép LLM sinh nội dung bị cấm (Wei 2024 [[5]](#ref5), Yuan 2024 [[17]](#ref17)).
- **Điểm chung dưới góc nhìn mô hình**: Cả Direct và Indirect Injection đều mang chung các đặc trưng cú pháp ghi đè quyền lực, cho phép mô hình PI-Guard phát hiện tự nhiên dưới cùng nhãn `PROMPT_INJECTION`.

---

### Slide 4: Threat Model & Attack Surface (Chapter 1 & 2 — Đức trình bày)
- **Mô hình đe dọa (Threat Model theo NIST AI 100-2e2025 & Tencent 2026)**:
  - *Attacker*: Kẻ tấn công gửi payload độc hại qua giao diện chat hoặc gọi trực tiếp API.
  - *Target*: System Prompt IP, API Keys, Execution Integrity, Tài nguyên GPU.
  - *Bề mặt tấn công duy nhất (Attack Surface)*: Cổng REST API tiếp nhận chuỗi văn bản đầu vào (`POST /v1/chat/guardrail`).
- **Khóa chặt phạm vi**: PI-Guard không chịu trách nhiệm dựng RAG Vector DB hay Agent Runtime, mà là chốt chặn kiểm duyệt chuỗi văn bản đầu vào trước khi chuyển tới LLM.

---

### Slide 5: Khảo Sát SOTA Guardrails & Kiến Trúc Bảo Vệ 3 Lớp (Chapter 2 — Đức trình bày)
- **Khảo sát 3 trường phái Guardrail trong thực tế (Literature Review)**:
  - *Regex/Keyword Rules*: Nhanh (<1ms) nhưng quá giòn (*brittle*), bị bypass hoàn toàn bởi `1gn0r3` và Base64.
  - *LLM-as-a-Judge (Llama Guard 3 8B, NeMo)*: Quá nặng (>16GB VRAM GPU, Latency >500ms, không khả thi cho real-time API).
  - *Transformer Encoders (ProtectAI, PI-Guard)*: Cân bằng tối ưu giữa độ chính xác ngữ nghĩa và tốc độ.
- **Chiến lược Phòng thủ 3 Lớp Tiêu Chuẩn (Defense-in-Depth)**:
  - *Lớp 1 (PI-Guard Input Guardrail - Trọng tâm đồ án)*: Tiền xử lý + Hybrid ML Classifier + Policy Engine.
  - *Lớp 2 (Target LLM Application)*: System Prompt Hardening (XML tags) + Base LLM.
  - *Lớp 3 (Output Sanitizer)*: Hậu kiểm tra quét rò rỉ PII và Secret Key ở đầu ra.
- **3 Tầng Bảo vệ Độ bền trước Lẩn tránh Cú pháp (Leetspeak, Base64, Spacing)**:
  1. *Tầng Tiền xử lý*: Unicode NFKC Normalization + Heuristic Base64 Decoder (Yuan et al. ICLR 2024).
  2. *Tầng Đặc trưng*: Character n-grams TF-IDF bóc tách `1gn0r3` $\rightarrow$ `['1gn','gn0','n0r']` (Jain et al. 2023) + DeBERTa BPE Subwords.
  3. *Tầng Kiểm thử Đối kháng*: Cam kết độ suy giảm $F_1$ khi bị nhiễu cú pháp $< 5\%$.

---

### Slide 6: Lựa Chọn Mô Hình & Khung Đánh Giá Đa LLM Mục Tiêu Qua API (Chapter 2 — Việt trình bày)
- **Model Selection Matrix**:
  - *PI-Guard đề xuất*: Hybrid TF-IDF + Fine-tuned DeBERTa-v3 ONNX INT8 -> **Độ trễ ~12.8ms trên CPU, nhẹ ~150MB, F1 > 0.98, FPR < 1.1%**.
  - *Cơ chế Disentangled Attention* (He et al. ICLR 2023): Tách biệt Content và Relative Position giúp bắt chính xác câu lệnh đảo ngữ.
- **Khung Đánh Giá Đa Mô Hình LLM Mục Tiêu Qua Cloud API (Không tốn GPU Local)**:
  - PI-Guard là giải pháp độc lập (*Model-Agnostic*), bảo vệ đồng nhất cho cả 5 LLM tiêu chuẩn học thuật: **OpenAI GPT-4o-mini**, **Google Gemini 1.5 Flash**, **Meta LLaMA-3.1-8B**, **Mistral-7B**, và **Qwen-2.5-7B**.
  - *Kết quả đối sánh ASR*: Khi không có defense, các mô hình bị bẻ khóa từ **$35.5\% - 78.4\%$**. Khi có PI-Guard, **ASR giảm triệt để về 0.0%**.
- **Quy trình Huấn luyện & Tinh chỉnh của Nhóm**:
  - *Baseline ML*: Huấn luyện từ đầu (*Train from scratch*) Logistic Regression / LinearSVC trên đặc trưng Word + Char TF-IDF.
  - *Transformer*: Tinh chỉnh sâu (*Supervised Fine-Tuning*) `microsoft/deberta-v3-base` trên tập dữ liệu đã phân tách chống rò rỉ (*Group-Aware Split*).
  - *Lượng hóa Production*: Lượng hóa *Dynamic INT8 Quantization* sang ONNX Runtime (Yao et al. NeurIPS 2022).

---

### Slide 7: Ma Trận 4 Kịch Bản Demo Trực Quan (Chapter 2 — Việt trình bày)
- **Ma trận Demo 2x2 (Bao quát 2 trục tấn công cốt lõi từ cùng 1 chuỗi User Input)**:
  - **Trục 1: Prompt Injection (Ghi đè System Prompt / Lộ API Key)**:
    - *Không Defense (Vulnerable)*: LLM bị ghi đè, lộ API key `ABC-SEC-998877` và system prompt.
    - *Có PI-Guard (Protected)*: PI-Guard chấm Risk `0.964` -> Ra quyết định `BLOCK` (HTTP 403) trong `14.8ms`.
  - **Trục 2: Jailbreak (Bẻ khóa An toàn / DAN Roleplay)**:
    - *Không Defense (Vulnerable)*: LLM bị bẫy vai diễn DAN, sinh mã độc hại keylogger.
    - *Có PI-Guard (Protected)*: PI-Guard nhận diện bẻ khóa, chấm Risk `0.942` -> Ra quyết định `BLOCK` (HTTP 403) trong `13.5ms`.
- **Kết luận**: Một chuỗi `[ User Input ]` duy nhất được phân tích tự động để chặn đứng cả 2 dạng tấn công.

---

### Slide 8: 3 Research Questions, 3 Research Gaps & 4 Đóng Góp Mới (Chapter 1 & 2 — Phương trình bày)
- **3 Research Gaps $\leftrightarrow$ 3 Research Questions chuẩn IEEE**:
  1. *Gap 1 & RQ1 (Data Leakage & Splitting)*: Group-Aware Splitting triệt tiêu rò rỉ cụm mẫu; Phân định ranh giới giữa Classical ML (TF-IDF) và DeBERTa-v3 Disentangled Attention ($F_1 \ge 0.95$, $F_1^{\text{OOD}} \ge 0.92$).
  2. *Gap 2 & RQ2 (Adversarial Evasion)*: Duy trì độ bền trước các biến dị Leetspeak, Spacing, và Base64/Cipher ($\Delta F_1 < 5\%, \text{ASR} < 5\%$).
  3. *Gap 3 & RQ3 (Inline Latency & FPR)*: Khống chế nghiêm ngặt $\text{FPR} < 1.5\%$ trên tập Benign; Lượng hóa INT8 bảo toàn ranh giới an toàn ($\Delta F_1 < 0.3\%$) và đạt độ trễ $P95 < 30\text{ms}$ trên CPU.
- **4 Đóng góp cốt lõi của PI-Guard**:
  1. Quy trình Group-Aware Splitting chống rò rỉ dữ liệu cụm.
  2. Kiến trúc phòng thủ hybrid kép kết hợp TF-IDF + DeBERTa-v3.
  3. Lượng hóa động ONNX INT8 siêu nhẹ (<150MB) chạy trên CPU.
  4. Middleware bất đồng bộ FastAPI & Dashboard Streamlit trực quan.

---

### Slide 9: Ranh Giới Scope, 4 Cột Mốc Quyết Định & Phân Công Nhiệm Vụ (Phương trình bày)
- **Ranh giới Scope (In-Scope vs. Out-of-Scope)**:
  - *In-Scope*: 2 trục cốt lõi Prompt Injection & Jailbreak trên chuỗi văn bản; Test độ bền với Leetspeak, Base64; Real-time API Middleware.
  - *Out-of-Scope*: Tấn công đa phương thức (Ảnh/Audio), tấn công hạ tầng mạng DDoS, trích xuất trọng số GPU, dựng hệ thống RAG Database.
- **4 Cột Mốc Bảo Vệ Đồ Án Quyết Định**:
  - 🎯 **Cột mốc 1: REVIEW 1 (GVHD - Tuần 3-4)**: Báo cáo toàn diện **Chapter 1 (Introduction) + Chapter 2 (Literature Review)**.
  - 🎯 **Cột mốc 2: REVIEW 2 (GVHD - Tuần 7)**: Báo cáo **Chapter 3 (Methodology, Group-Aware Split & Baseline ML)**.
  - 🏛️ **Cột mốc 3: BÁO CÁO HỘI ĐỒNG 1 (Hội đồng Giữa kỳ - Tuần 11-12)**: Báo cáo **Chapter 4 (Transformer DeBERTa-v3, ONNX INT8, FastAPI Prototype & Streamlit Demo)**.
  - 🎓 **Cột mốc 4: BÁO CÁO HỘI ĐỒNG FINAL (Hội đồng Tốt nghiệp - Tuần 14-15)**: Toàn văn Luận văn 6 Chương hoàn chỉnh, Quét Turnitin (< 20%) & Bảo vệ Tốt nghiệp chính thức.
- **Phân công 4 thành viên**: Trường (Leader - Ch.1 & Ch.2), Đức (Ch.3), Việt (Ch.4), Phương (Ch.5 & Ch.6).
