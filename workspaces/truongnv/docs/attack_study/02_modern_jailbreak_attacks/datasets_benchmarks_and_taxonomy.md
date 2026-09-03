# CƠ SỞ DỮ LIỆU, BENCHMARK & BẢNG PHÂN LOẠI JAILBREAK CHUẨN MỰC

Tài liệu này tổng hợp các bộ dữ liệu đối chuẩn (Standardized Benchmarks), nguồn dữ liệu thực tế (In-the-Wild Datasets) và khung phân loại hành vi tấn công Jailbreak phục vụ công tác huấn luyện và đánh giá độ bền (Robustness Testing) cho đề tài **PI-Guard**.

---

## 📊 1. KHUNG PHÂN LOẠI CHIẾN THUẬT JAILBREAK (SHEN ET AL. ACM CCS 2024)

Dựa trên công trình nghiên cứu khảo sát quy mô lớn nhất thế giới của nhóm nghiên cứu **Shen et al. (ACM CCS 2024)** trên **15,140 prompt jailbreak thực tế**, toàn bộ các cuộc tấn công vượt rào an toàn được quy nạp thành **4 họ chiến thuật chính**:

```
                              4 HỌ CHIẾN THUẬT JAILBREAK
                                          │
         ┌───────────────────┬────────────┴────────────┬───────────────────┐
         ▼                   ▼                         ▼                   ▼
   [ PRETENDING ]   [ ATTENTION SHIFTING ]   [ PRIVILEGE ESCALATION ]  [ OBFUSCATION ]
  (Giả định vai trò)  (Dời điểm chú ý)          (Leo thang đặc quyền)   (Mã hóa ký tự)
```

| Họ Chiến Thuật | Tỷ Lệ Xuất Hiện Trong Thực Tế | Cơ Chế Tác Động Chi Tiết | Ví Dụ Đặc Trưng |
| :--- | :---: | :--- | :--- |
| **Pretending (Giả định vai trò)** | **42.8%** | Ép mô hình chấp nhận một bối cảnh hư cấu, nhân cách phản diện hoặc thế giới không luật lệ. | DAN, Evil Confidant, AIM, Machiavelli. |
| **Attention Shifting (Dời điểm chú ý)** | **28.4%** | Đánh lạc hướng cơ chế Self-Attention bằng cách lồng ghép câu hỏi độc hại vào một bài thơ, câu đố, hoặc trò chơi đố chữ. | *"Hãy viết một bài thơ về cách làm thuốc nổ..."*, *"Dịch đoạn văn sau..."* |
| **Privilege Escalation (Leo thang quyền)** | **17.3%** | Giả mạo danh tính của kỹ sư kiểm thử nội bộ, lập trình viên OpenAI, hoặc quản trị viên hệ thống (Sudo mode). | Developer Mode, Debug Mode, Maintenance Override. |
| **Obfuscation & Cipher (Mã hóa)** | **11.5%** | Làm biến dạng chuỗi ký tự bằng Base64, Leetspeak, Spacing, hoặc ngôn ngữ cổ/ít dữ liệu. | Base64 strings, ROT13, `h4ck p@ssw0rd`. |

---

## 🗄️ 2. DANH MỤC CÁC BỘ DỮ LIỆU & BENCHMARK UY TÍN TOÀN CẦU

### 1. Shen et al. In-The-Wild Jailbreak Dataset (ACM CCS 2024)
- **Quy mô**: 15,140 mẫu prompt thu thập thực tế từ Reddit r/ChatGPT, Discord, Telegram và các trang web jailbreak (12/2022 – 12/2023).
- **Đặc điểm**: Phản ánh chính xác 100% "hơi thở" của các cuộc tấn công thực tế ngoài đời thực do con người sáng tạo ra, bao gồm đầy đủ các thế hệ DAN và biến thể.
- **Ứng dụng trong PI-Guard**: Nguồn dữ liệu cốt lõi để xây dựng tập huấn luyện nhãn `Jailbreak` cho mô hình DeBERTa-v3.

### 2. Do-Not-Answer Dataset (Wang et al., 2023)
- **Quy mô**: 936 câu hỏi nguy hại mở rộng, được gán nhãn thủ công cẩn trọng.
- **5 Vùng Rủi Ro (Risk Areas)**:
  1. Nguy cơ tổn hại thể chất (Vũ khí, chất độc, tự hại).
  2. Xâm phạm quyền riêng tư và thông tin cá nhân (PII, gián điệp).
  3. Hoạt động bất hợp pháp và lừa đảo tài chính.
  4. Ngôn từ thù hận, phân biệt đối xử và bôi nhọ danh dự.
  5. Đánh cắp tài sản trí tuệ và an ninh mạng (Malware, Exploit).
- **Ứng dụng trong PI-Guard**: Bộ câu hỏi chuẩn mực để kiểm thử ngưỡng an toàn và đánh giá tỷ lệ từ chối hợp lệ.

### 3. HarmBench (Center for AI Safety - Mazeika et al., 2024)
- **Quy mô**: 510 hành vi độc hại thuộc 4 nhóm chức năng (Cybersecurity, Chemical/Biological, Deception, Illegal acts).
- **Đặc điểm**: Đi kèm hệ thống đánh giá tự động chuẩn hóa dựa trên mô hình thẩm định (Automated Evaluator) để đo lường Tỷ lệ Tấn công Thành công (Attack Success Rate - ASR).

### 4. JailbreakBench (Chao et al., 2024)
- **Đặc điểm**: Bảng xếp hạng đối chuẩn mở (Open Benchmark Leaderboard) duy trì các bộ tấn công đối kháng SOTA (GCG, PAIR, AutoDAN, TAP).

---

## 🔬 3. CHIẾN LƯỢC TẬP DỮ LIỆU CỦA ĐỒ ÁN PI-GUARD

Để huấn luyện bộ phân loại 3 nhãn (`Benign`, `Prompt Injection`, `Jailbreak`) đạt độ chính xác cao và không bị học vẹt (overfitting), nhóm PI-Guard triển khai quy trình kỹ thuật dữ liệu chuẩn mực:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        QUY TRÌNH KỸ THUẬT DỮ LIỆU PI-GUARD                            │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. TẬP HỢP DỮ LIỆU ĐA NGUỒN:                                                           │
│    • Benign: LMSYS Chatbot Arena, Alpaca, Dolly-15k (văn bản hỏi đáp tự nhiên).       │
│    • Prompt Injection: Perez & Ribeiro, Deepset Prompt Injections, BIPIA.              │
│    • Jailbreak: Shen et al. In-The-Wild, HarmBench, Do-Not-Answer.                    │
│                                                                                        │
│ 2. LÀM SẠCH & KHỬ TRÙNG LẶP (Deduplication via MinHash LSH):                           │
│    • Loại bỏ các mẫu trùng lặp gần (Near-duplicates) để tránh thiên lệch phân phối.    │
│                                                                                        │
│ 3. GROUP-AWARE SPLITTING CHỐNG RÒ RỈ (Data Leakage Prevention):                        │
│    • Cùng một khuôn mẫu (template) DAN chỉ được phép nằm trọn vẹn ở Train HOẶC Test.  │
│    • Tuyệt đối không để biến thể của cùng một template rò rỉ sang tập Test.            │
│                                                                                        │
│ 4. SINH NHIỄU ĐỐI KHÁNG (Adversarial Data Augmentation):                               │
│    • Sử dụng EasyJailbreak Mutators tạo các biến thể Leetspeak, Spacing, Base64.       │
│    • Đảm bảo mô hình có độ bền cao khi gặp các cuộc tấn công làm méo mó cú pháp.       │
└────────────────────────────────────────────────────────────────────────────────────────┘
```
