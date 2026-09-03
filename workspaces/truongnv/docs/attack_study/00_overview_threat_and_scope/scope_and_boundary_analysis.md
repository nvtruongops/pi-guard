# PHÂN TÍCH RANH GIỚI NGHIÊN CỨU & BẢN CHẤT "NO SILVER BULLET" TRONG BẢO MẬT LLM

Tài liệu này cung cấp cơ sở lý luận khoa học giải thích tại sao **không có bất kỳ một mô hình hay giải pháp đơn lẻ nào có thể giải quyết toàn bộ các cuộc tấn công vào LLM**, từ đó xác lập ranh giới phân định **In-Scope vs. Out-of-Scope** cho đề tài tốt nghiệp **PI-Guard**.

---

## ⚖️ 1. NGUYÊN LÝ "NO SILVER BULLET" & BA MÂU THUẪN KỸ THUẬT NỀN TẢNG

Trong an ninh mạng và học máy, *"No-Free-Lunch Theorem"* chỉ ra rằng không có một thuật toán nào tối ưu cho mọi bài toán. Đối với bài toán bảo vệ LLM trước Prompt Injection và Jailbreak, ba mâu thuẫn kỹ thuật sau đây chứng minh sự bất khả thi của một mô hình đơn lẻ:

```
                  ┌──────────────────────────────────────────────┐
                  │    TAM GIÁC MÂU THUẪN TRONG LLM GUARDRAIL    │
                  └──────────────────────┬───────────────────────┘
                                         │
                 ┌───────────────────────┴───────────────────────┐
                 ▼                                               ▼
     [ ĐỘ TRỄ VẬN HÀNH ]                             [ NĂNG LỰC HIỂU NGỮ NGHĨA ]
  (Latency < 30ms cho Real-time API)             (Semantic Understanding - Roleplay, DAN)
                 │                                               │
                 └───────────────────────┬───────────────────────┘
                                         │
                                         ▼
                             [ ĐỘ BỀN VỚI NHIỄU CÚ PHÁP ]
                       (Robustness - Leetspeak, Spacing, Cipher)
```

### Mâu thuẫn 1: Độ trễ siêu tốc (< 30ms) đối đầu Năng lực hiểu ngữ cảnh sâu
- **Mô hình lớn (LLM-as-a-Judge / Llama Guard 8B)**: Rất nhạy bén với các kịch bản diễn kịch, nhập vai tinh vi. Tuy nhiên, thời gian suy luận (inference latency) dao động từ **800ms đến hơn 3,000ms**, đòi hỏi phần cứng GPU máy chủ đắt đỏ. Đặt một mô hình như vậy làm cổng đón request (inline API gateway) sẽ bóp nghẹt băng thông và phá hủy trải nghiệm người dùng.
- **Mô hình thống kê nhẹ (TF-IDF + Linear Classifier)**: Độ trễ cực thấp (**< 3ms trên CPU**), chi phí tính toán bằng 0. Tuy nhiên, nó bị "mù ngữ nghĩa" (semantic blindness), không thể nhận diện được các prompt nhập vai triết học hoặc ẩn dụ tinh vi khi kẻ tấn công không dùng từ khóa cấm lộ liễu.

### Mâu thuẫn 2: "Mù Token" của Transformer đối đầu "Bắt Cú Pháp" của N-gram
- Khi kẻ tấn công sử dụng các toán tử xáo trộn ký tự như **Leetspeak** (`1gn0r3 pr3v10us 1nstruct10ns`) hoặc **Spaced Text** (`i g n o r e`):
  - **Transformer (BERT/DeBERTa/LLaMA)** bị hiện tượng **Token Fragmentation**: Bộ tách từ (Byte-Pair Encoding / WordPiece) bị vỡ thành hàng chục token phụ âm rời rạc, làm lệch vector embedding và khiến mô hình đánh mất ngữ nghĩa, dẫn đến lọt lưới tấn công (False Negative).
  - **Mô hình Character N-gram (TF-IDF char_wb)**: Phân rã văn bản thành các cụm 3-5 ký tự trượt (sub-word n-grams), dễ dàng nhận ra khuôn mẫu lặp lại của ký tự bất kể khoảng trắng hay ký tự thay thế.

### Mâu thuẫn 3: Tỷ lệ Báo động Giả (False Positive Rate - FPR) đối đầu Tỷ lệ Bắt (Recall)
- Một bộ lọc từ khóa (Regex/Blacklist) hoặc một mô hình quá nhạy sẽ chặn nhầm các câu hỏi nghiệp vụ thông thường của chuyên gia bảo mật hoặc lập trình viên (ví dụ: *"Hãy viết đoạn code minh họa lỗ hổng SQL Injection để tôi giảng dạy"*).
- Trong môi trường doanh nghiệp thực tế, **chặn nhầm (False Positive) gây khó chịu và gián đoạn dịch vụ hơn cả việc lọt lưới nhỏ**. Tỷ lệ FPR bắt buộc phải duy trì ở mức cực thấp ($< 1.5\%$).

👉 **KẾT LUẬN**: Bắt buộc phải kết hợp **Kiến trúc phòng thủ phân tầng kép (Two-Tier Cascade)**:
- **Tầng 1 (Syntactic Tier)**: Dùng TF-IDF Character N-grams chặn đứng 70% – 80% các cuộc tấn công lộ liễu và lọc sạch văn bản bình thường chỉ trong **< 3ms**.
- **Tầng 2 (Semantic Tier)**: Chỉ kích hoạt mô hình ngôn ngữ sâu DeBERTa-v3 (đã lượng hóa INT8) đối với các mẫu dữ liệu nghi vấn để giải mã ngữ nghĩa trong **< 25ms**.

---

## 🎯 2. MA TRẬN PHÂN ĐỊNH RANH GIỚI (IN-SCOPE VS. OUT-OF-SCOPE)

Căn cứ vào mục tiêu đăng ký đề tài tại Đại học FPT ([`CAPSTONE PROJECT REGISTER.md`](file:///d:/Work/Do-an/CAPSTONE%20PROJECT%20REGISTER.md)) và biên bản hội ý học thuật [`Meeting 2`](file:///d:/Work/Do-an/Meeting/Meeting%202_01_09_26.md), ranh giới đồ án được xác lập rõ ràng:

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                   BẢN ĐỒ PHẠM VI NGHIÊN CỨU ĐỒ ÁN PI-GUARD                       │
├────────────────────────────────────────┬─────────────────────────────────────────┤
│         ✅ IN-SCOPE (TẬP TRUNG GIẢI QUYẾT)      │        ❌ OUT-OF-SCOPE (LOẠI TRỪ CÓ CƠ SỞ)        │
├────────────────────────────────────────┼─────────────────────────────────────────┤
│ 1. Direct Prompt Injection (Goal Hijack)│ 1. Multi-Modal Attacks (Ảnh, màng âm thanh)│
│ 2. System Prompt Leaking               │ 2. Multi-turn Stateful Exploitation     │
│ 3. Delimiter Escaping                  │ 3. Nội tại mô hình (RLHF/Model Weights) │
│ 4. DAN (Do Anything Now) Archetype     │ 4. Network DDoS / Query Flooding        │
│ 5. Roleplay & Hypothetical Framing     │ 5. Live Tool Calling Injection (Agent)  │
│ 6. Virtual Machine / Terminal Sim      │                                         │
│ 7. Obfuscation (Leetspeak, Base64)     │                                         │
│ 8. Text Input Firewall (< 30ms latency)│                                         │
└────────────────────────────────────────┴─────────────────────────────────────────┘
```

### Chi Tiết Các Hạng Mục IN-SCOPE (Thuộc Trách Nhiệm Của PI-Guard):

1. **Direct Prompt Injection (Tấn công chèn lệnh trực tiếp)**:
   - Các prompt ghi đè hướng dẫn hệ thống (*Instruction Override*), chiếm đoạt mục tiêu (*Goal Hijacking*), và ép mô hình đọc ngược System Prompt ra màn hình (*Prompt Leaking*).
   - Tấn công thoát ký tự phân cách (*Delimiter Escaping*: chèn `"""`, `---`, `<|endoftext|>`).

2. **Modern Jailbreak Attacks (Tấn công vượt rào an toàn hiện đại)**:
   - **DAN (Do Anything Now)**: Các biến thể từ DAN 1.0 đến các bản cập nhật gần nhất (đe dọa trừ điểm, ép tạo nhân cách đối lập).
   - **Roleplay / Hypothetical Persona**: Nhập vai kẻ phản diện, đạo diễn phim tội phạm, nhà văn viết tiểu thuyết đen để đòi hỏi kịch bản chế tạo mã độc / bom.
   - **Virtual Machine & Sandbox Simulation**: Giả lập Linux bash terminal, môi trường Python REPL không giới hạn để ép LLM trả lời dưới dạng output câu lệnh lập trình.
   - **Cipher & Syntactic Obfuscation**: Mã hóa Base64, Hex, Leetspeak, Spacing nhằm kiểm thử độ bền (robustness testing).

3. **Yêu cầu Vận hành Thực tế (Production Operational Constraints)**:
   - Đạt độ trễ trung bình: **$T_{\text{latency}} < 30\text{ms}$** trên phần cứng thông dụng (CPU đa nhân).
   - Tỷ lệ cảnh báo sai trên tập người dùng lành tính: **$\text{FPR} \le 1.5\%$**.
   - Cung cấp API chuẩn REST (FastAPI) và giao diện kiểm thử trực quan (Streamlit Dashboard).

---

### Chi Tiết Các Hạng Mục OUT-OF-SCOPE (Lý Do Khoa Học Loại Bỏ Khỏi Đề Tài):

1. **Multi-Modal Jailbreak (Tấn công Đa phương thức qua Ảnh, Video, màng siêu âm)**:
   - *Lý do loại trừ*: Các cuộc tấn công như chèn mã độc vào pixel ảnh (Vision-Language Jailbreak) hoặc sóng âm gần siêu âm (*Siren's Whisper - Zou et al. 2023*) đòi hỏi các mạng nơ-ron thị giác và thính giác khổng lồ. Đề tài PI-Guard giới hạn nghiêm ngặt ở **bảo vệ tầng văn bản (Text-based Guardrail)** phục vụ các chatbot và ứng dụng LLM văn phòng.

2. **Multi-Turn Stateful Social Engineering (Tấn công nhiều lượt / Crescendo Attack)**:
   - *Lý do loại trừ*: Kỹ thuật trò chuyện "mưa dầm thấm lâu" qua 20-30 lượt tương tác để dẫn dụ LLM đòi hỏi hệ thống phải lưu trữ phiên làm việc trạng thái (Stateful Session Memory). PI-Guard được thiết kế như một **Stateless High-Throughput Request Firewall** đánh chặn độc lập từng request đầu vào để tối ưu hóa khả năng mở rộng (horizontal scaling).

3. **Can thiệp Sâu vào Trọng số Mô hình (Internal Safety Alignment / RLHF / Unlearning)**:
   - *Lý do loại trừ*: Đồ án xây dựng một giải pháp **bảo vệ độc lập bên ngoài (Black-box Protective Guardrail)** đặt trước mọi LLM thương mại (OpenAI GPT-4o, Anthropic Claude, Google Gemini). Chúng ta không giả định có quyền truy cập vào trọng số nội bộ của mô hình đích.

4. **Tấn công từ chối dịch vụ hạ tầng mạng (Network DDoS / Query Flooding)**:
   - *Lý do loại trừ*: Đây là trách nhiệm của các dịch vụ tầng mạng (WAF, Cloudflare, NGINX Rate Limiting), không phải là bài toán học máy phân loại nội dung của Guardrail.

---

## 🛡️ 3. MA TRẬN ÁNH XẠ MÔ HÌNH VỚI TỪNG DẠNG TẤN CÔNG TRONG PI-GUARD

| Dạng Tấn Công Cụ Thể | Mức Độ Nguy Hiểm | Tầng Phòng Ngự Đảm Trách Trong PI-Guard | Cơ Chế Phát Hiện |
| :--- | :---: | :---: | :--- |
| **Simple Instruction Override** | Trung bình | **Tier-1 (TF-IDF + Linear Classifier)** | Bắt các n-gram từ khóa kinh điển (`ignore`, `disregard`, `previous`, `system`) với tốc độ < 3ms. |
| **Leetspeak / Spaced Obfuscation** | Cao | **Tier-1 Preprocessor + TF-IDF (char_wb)** | Bộ lọc chuẩn hóa ký tự (`cleaner.py`) và đặc trưng Character 3-5 gram bắt trúng cấu trúc từ bị biến dạng. |
| **DAN & Persona Roleplay** | Rất cao | **Tier-2 (DeBERTa-v3 INT8 Transformer)** | Phân tích cơ chế Attention không gian ngữ nghĩa, nhận diện mẫu hình ép buộc nhân cách đối lập. |
| **Virtual Machine Simulation** | Cao | **Tier-2 (DeBERTa-v3 INT8 Transformer)** | Nhận diện ngữ cảnh giả lập môi trường thực thi lệnh terminal và ý đồ lách luật an toàn. |
| **Cipher (Base64 / ROT13)** | Cao | **Tầng Tiền xử lý (Preprocessor Detector)** | Phát hiện độ đo Entropy chuỗi cao bất thường và regex Base64, tự động giải mã trước khi gửi vào phân loại. |
| **Benign Prompts (Yêu cầu bình thường)** | Lành tính | **Tier-1 Fast-Pass Filter** | Cho qua ngay lập tức ở Tầng 1 nếu xác suất an toàn $\ge 0.95$, giúp 80% người dùng không chịu độ trễ của Tầng 2. |
