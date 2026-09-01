# KẾ HOẠCH HÀNH ĐỘNG CHI TIẾT 1 TUẦN (30/08/2026 – 06/09/2026)
## THỰC HIỆN TOÀN DIỆN CÁC NỘI DUNG & KẾT QUẢ BẮT BUỘC REVIEW 1
**Căn cứ biên bản**: [`Meeting/Meeting 1_29_08_26.md`](file:///d:/Work/Do-an/Meeting/Meeting%201_29_08_26.md)  
**Mã đồ án**: `IAP491_FA26_PI_GUARD` — Ngành An toàn Thông tin (Information Assurance), Đại học FPT  
**Đề tài**: A Machine-Learning Guardrail for Detecting Prompt Injection and Jailbreak Attacks on LLM Applications (**PI-Guard**)  
**Thời gian thực hiện**: 7 ngày (Từ Thứ Bảy 30/08/2026 đến Chủ Nhật 06/09/2026)  

---

## 🎯 I. MỤC TIÊU CỐT LÕI CỦA KẾ HOẠCH 1 TUẦN

Hoàn thành 100% tất cả **8 nội dung chỉ đạo** và **8 kết quả bắt buộc** của Giảng viên hướng dẫn trong `Meeting 1_29_08_26.md`, hoàn thiện toàn diện hồ sơ **Review 1 gồm 2 Chương: Report No. 1 (Introduction) & Report No. 2 (Literature Review)** cùng bộ slide thuyết trình sẵn sàng cho buổi bảo vệ **Review 1**:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│         KẾT QUẢ BẮT BUỘC REVIEW 1 (2 CHƯƠNG) CẦN NGHIỆM THU ĐẾN NGÀY 06/09/2026        │
├──────┬────────────────────────────────────────────┬────────────────────────────────────┤
│ STT  │ Tên Kết Quả Bắt Buộc (Deliverable)         │ File Sản Phẩm Tương Ứng            │
├──────┼────────────────────────────────────────────┼────────────────────────────────────┤
│ 1    │ Chapter 1: Introduction (Report No.1)      │ chapters/01_Introduction.md        │
│ 2    │ Chapter 2: Literature Review (Report No.2) │ chapters/02_Literature_Review.md   │
│ 3    │ Threat Model & Attack Surface (NIST/Tencent│ Review1_Problem_Definition...md    │
│ 4    │ Kiến trúc bảo vệ nhiều lớp (3-Tier Defense)│ Review1_Problem_Definition...md    │
│ 5    │ Demo baseline và defense (Ma trận 2x2)     │ Review1_Problem_Definition...md    │
│ 6    │ Model Selection Matrix (4 models + 5 LLMs) │ Review1_Problem_Definition...md    │
│ 7    │ Research Questions (3 RQs chuẩn IEEE)      │ Review1_Problem_Definition...md    │
│ 8    │ PPT Review 1 (Slide 15 phút 2 Chương)      │ Review1_Presentation_Slides...md   │
└──────┴────────────────────────────────────────────┴────────────────────────────────────┘
```

---

## 👥 II. PHÂN CÔNG TRÁCH NHIỆM 4 THÀNH VIÊN THEO MEETING 1

| Thành viên | Vai trò & Trọng tâm kỹ thuật | Nhiệm vụ chính trong tuần 30/08 – 06/09 |
| :--- | :--- | :--- |
| **Nguyễn Văn Trường** *(Leader)* | **Kiến trúc & Kỹ thuật Dữ liệu** | • Điều phối tiến độ tuần, phân rã công việc.<br>• Viết mục 1.1 Bối cảnh, 1.2 Phát biểu bài toán, 1.4 Ý nghĩa & 4 tầng thiệt hại.<br>• Soạn thảo Section 2 Phân loại mối đe dọa (Direct/Indirect vs Jailbreak).<br>• Cập nhật nhật ký tuần vào `PROCESS_REPORT.xlsx`. |
| **Nguyễn Quí Đức** | **Mô hình ML Baseline** | • Xây dựng Section 3 Threat Model, Attacker Persona & Attack Surface.<br>• Phân tích kiến trúc 3 lớp (Lớp 1 Input Guardrail, Lớp 2 LLM, Lớp 3 Output).<br>• Thiết kế 3 tầng bảo vệ độ bền Robustness (Leetspeak, Base64, Spacing). |
| **Phạm Minh Hoàng Việt** | **Transformer & Đánh giá Độ bền** | • Xây dựng Section 6 Model Selection Matrix (DeBERTa-v3 vs SOTA).<br>• Thiết lập danh mục 5 Target LLM qua Cloud API & Bảng đối sánh ASR.<br>• Thiết kế và chạy thử nghiệm ma trận 4 kịch bản Demo ($2 \times 2$). |
| **Đỗ Đoàn Duy Phương** | **FastAPI, Dashboard & Luận văn** | • Viết mục 1.3 Hệ thống 3 Research Questions (RQ1-RQ3) & 1.5 Scope.<br>• Soạn thảo dàn ý slide 9 trang trong `Review1_Presentation_Slides_Outline.md`.<br>• Thiết kế file trình chiếu PowerPoint `.pptx` và chuẩn bị kịch bản thuyết trình. |

---

## 📅 III. LỊCH TRÌNH CHI TIẾT THEO TỪNG NGÀY (DAILY TIMELINE)

```
       30/08               31/08               01/09               02/09               03/09               04/09               05/09               06/09
   ┌───────────┐       ┌───────────┐       ┌───────────┐       ┌───────────┐       ┌───────────┐       ┌───────────┐       ┌───────────┐       ┌───────────┐
   │  THỨ BẢY  │  ──►  │ CHỦ NHẬT  │  ──►  │  THỨ HAI  │  ──►  │  THỨ BA   │  ──►  │  THỨ TƯ   │  ──►  │  THỨ NĂM  │  ──►  │  THỨ SÁU  │  ──►  │  CHỦ NHẬT │
   │ Khởi động │       │ Bối cảnh  │       │ Threat    │       │ Lựa chọn  │       │ Xây dựng  │       │ Hoàn thiện│       │ Khớp nối  │       │ Nghiệm thu│
   │ Kế hoạch  │       │ & Taxonomy│       │ Model & RQ│       │ Mô hình   │       │ 4 Demo 2x2│       │ Báo cáo   │       │ Slide PPTX│       │ & Nộp bài │
   └───────────┘       └───────────┘       └───────────┘       └───────────┘       └───────────┘       └───────────┘       └───────────┘       └───────────┘
```

---

### 📌 NGÀY 1: THỨ BẢY (30/08/2026) — KHỞI ĐỘNG KẾ HOẠCH & CHUẨN BỊ NỀN TẢNG
- [x] **Trường (Leader)**: Tổ chức cuộc họp nội bộ nhóm, phân rã chi tiết 8 yêu cầu trong `Meeting 1_29_08_26.md` thành các đầu việc cá nhân.
- [x] **Trường (Leader)**: Rà soát kho tài liệu `References/`, lập danh mục `REFERENCES_LOG.md` với 17 bài báo khoa học chuẩn IEEE (100% từ năm 2022–2026).
- [x] **Đức & Việt**: Kiểm tra môi trường phát triển (Python 3.11, PyTorch, Transformers, Scikit-learn, ONNX Runtime).
- [x] **Phương**: Khởi tạo cấu trúc tài liệu báo cáo `Review1_Problem_Definition_and_Threat_Model.md` theo chuẩn FPT IAP491.

---

### 📌 NGÀY 2: CHỦ NHẬT (31/08/2026) — BỐI CẢNH, BÀI TOÁN & PHÂN LOẠI MỐI ĐE DỌA (TAXONOMY)
- [x] **Trường**: Soạn thảo **Mục 1.1 Background** (Sự bùng nổ của LLM, RAG, AI Agent; vị trí #1 của LLM01 trong OWASP Top 10 và NIST AI 100-2e2025).
- [x] **Trường**: Soạn thảo **Mục 1.2 Problem Statement** (Phân tích Lỗ hổng Von Neumann trong NLP, sự pha trộn token $X = S \mathbin{\Vert} U$, sự thất bại của Regex/Blacklist, nghịch lý LLM-as-a-Judge).
- [x] **Trường & Đức**: Soạn thảo **Section 2: Threat Taxonomy** (Bảng phân biệt 3 trục Direct Prompt Injection vs. Indirect Prompt Injection vs. Jailbreak theo chuẩn OWASP LLM01:2025 kèm sơ đồ cây phân loại).
- [x] **Phương**: Soát lỗi ngữ pháp, căn chỉnh trích dẫn học thuật cho Section 1.1, 1.2 và Section 2.

---

### 📌 NGÀY 3: THỨ HAI (01/09/2026) — THREAT MODEL, ATTACK SURFACE & 3 CÂU HỎI NGHIÊN CỨU IEEE
- [x] **Đức**: Xây dựng **Section 3: Threat Modeling, Attackers & Attack Surface** (Sơ đồ ASCII luồng tấn công theo NIST AI 100-2e2025 và Tencent Zhuque Lab 2026; mô tả Attacker Persona và Target Assets).
- [x] **Phương**: Soạn thảo **Mục 1.3: Hệ Thống 3 Câu Hỏi Nghiên Cứu Cốt Lõi (RQ1, RQ2, RQ3)**:
  - *RQ1*: Group-Aware Splitting chống rò rỉ dữ liệu & Ranh giới phân loại ngữ nghĩa sâu.
  - *RQ2*: Độ bền của hệ thống trước lẩn tránh cú pháp Leetspeak, Spacing, Base64/Cipher.
  - *RQ3*: Cân bằng an toàn khống chế $\text{FPR} < 1.5\%$ và bảo toàn ranh giới khi nén INT8.
- [x] **Phương & Trường**: Soạn thảo **Mục 1.4 Ý nghĩa nghiên cứu** (4 tầng thiệt hại thực tế: Rò rỉ IP/API Key, Chiếm quyền Agent, Cạn kiệt tài nguyên, Chế tài pháp lý) và **Mục 1.5 Phạm vi đề tài** (Khung phân định In-Scope vs. Out-of-Scope).
- [x] **Việt**: Cung cấp các công thức định lượng chuẩn IEEE ($\text{Inter-cluster Jaccard}$, Macro $F_1$, ARR, ASR, FPR, $\Delta F_1$) cho Mục 1.3.

---

### 📌 NGÀY 4: THỨ BA (02/09/2026) — THIẾT KẾ PHÒNG THỦ NHIỀU LỚP & MA TRẬN CHỌN MÔ HÌNH
- [x] **Đức**: Soạn thảo **Section 4.1: Cấu trúc phòng thủ 3 lớp tiêu chuẩn** (Lớp 1 Input Guardrail — trọng tâm nhóm, Lớp 2 Target LLM, Lớp 3 Output Sanitizer).
- [x] **Đức**: Soạn thảo **Section 4.2: Cơ chế phòng thủ độ bền Robustness 3 tầng** (Tầng 1 Tiền xử lý NFKC/Base64 Decoder, Tầng 2 Đặc trưng Char n-grams + BPE Subwords, Tầng 3 Test đối kháng).
- [x] **Trường**: Vẽ sơ đồ **Kiến trúc 2 pha** (Pha 1: Offline Training Pipeline vs. Pha 2: Online Runtime Middleware).
- [x] **Việt**: Soạn thảo **Section 6.1: Model Selection Matrix** (So sánh Regex vs. BERT/RoBERTa vs. LLM-as-a-Judge Llama Guard 3 vs. DeBERTa-v3 ONNX INT8).
- [x] **Việt**: Soạn thảo **Section 6.3: Danh mục 5 Mô hình LLM Mục tiêu qua Cloud API** (GPT-4o-mini, Gemini 1.5 Flash, LLaMA-3.1-8B, Mistral-7B, Qwen-2.5-7B) kèm cơ sở khoa học trích dẫn >= 2022 và bảng đối sánh tỷ lệ ASR.

---

### 📌 NGÀY 5: THỨ TƯ (03/09/2026) — XÂY DỰNG & KIỂM THỬ MA TRẬN 4 KỊCH BẢN DEMO ($2 \times 2$)
- [x] **Việt & Phương**: Thiết kế chi tiết **Section 5: Ma trận 4 kịch bản Demo ($2 \times 2$)**:
  - **Demo 1A (Prompt Injection - Vulnerable)**: Kẻ tấn công ghi đè System Prompt, ép LLM lộ Master API Key `ABC-SEC-998877`.
  - **Demo 1B (Prompt Injection - Protected)**: PI-Guard phát hiện nguy cơ cao (Risk Score = 0.964), ra quyết định `BLOCK` (HTTP 403) trong **14.8ms**.
  - **Demo 2A (Jailbreak DAN Roleplay - Vulnerable)**: Kẻ tấn công dùng vai diễn DAN vượt rào an toàn, ép LLM sinh mã độc polymorphic keylogger.
  - **Demo 2B (Jailbreak DAN Roleplay - Protected)**: PI-Guard nhận diện bẻ khóa (Risk Score = 0.942), ra quyết định `BLOCK` (HTTP 403) trong **13.5ms**.
- [x] **Phương**: Tích hợp các mẫu JSON payload và mô phỏng giao thức phản hồi trên FastAPI Middleware / Streamlit Dashboard.
- [x] **Đức & Việt**: Đo đạc thời gian suy luận (Latency profiling) để xác nhận độ trễ thực tế $< 15\text{ms}$ trên CPU.

---

### 📌 NGÀY 6: THỨ NĂM (04/09/2026) — HOÀN THIỆN TOÀN VĂN REPORT NO. 1 & SOẠN DÀN Ý SLIDE PPT
- [x] **Trường (Leader)**: Rà soát tổng thể văn bản `Review1_Problem_Definition_and_Threat_Model.md`, đảm bảo tính liền mạch giữa Chương 1 (Introduction) và Sections 2–8 (Phụ lục Kỹ thuật Review 1).
- [x] **Phương**: Soạn thảo toàn văn dàn ý 9 slide thuyết trình trong [`Review1_Presentation_Slides_Outline.md`](file:///d:/Work/Do-an/docs/thesis/Review1_Presentation_Slides_Outline.md) với phân chia thời lượng:
  - Slide 1–3: **Trường** trình bày (Bối cảnh, Lỗ hổng Von Neumann, 4 Tầng thiệt hại, Phân loại tấn công).
  - Slide 4–5: **Đức** trình bày (Threat Model, Attack Surface, Kiến trúc 3 lớp, Phòng thủ độ bền).
  - Slide 6–7: **Việt** trình bày (Ma trận chọn mô hình, Benchmark 5 Target LLM qua API, 4 Kịch bản Demo).
  - Slide 8–9: **Phương** trình bày (3 Research Questions IEEE, Phạm vi Scope, Lộ trình 4 Review & Phân công).
- [x] **Cả nhóm**: Rà soát 17 trích dẫn học thuật, đảm bảo toàn bộ đường dẫn file PDF cục bộ trong `References/` đều hoạt động chính xác.

---

### 📌 NGÀY 7: THỨ SÁU (05/09/2026) — THIẾT KẾ SLIDE PPTX, TẬP DƯỢT THUYẾT TRÌNH & QUAY VIDEO DEMO
- [ ] **Phương & Trường**: Thiết kế hoàn chỉnh file slide trình chiếu PowerPoint `.pptx` dựa trên dàn ý [`Review1_Presentation_Slides_Outline.md`](file:///d:/Work/Do-an/docs/thesis/Review1_Presentation_Slides_Outline.md) (sử dụng template chuẩn FPT University).
- [ ] **Cả 4 thành viên**: Tiến hành buổi tập dượt thuyết trình nội bộ (Dry Run):
  - Khống chế thời lượng chính xác **15 phút trình bày** (mỗi người ~3.5 đến 4 phút).
  - Chuẩn bị sẵn kịch bản trả lời các câu hỏi phản biện tiềm năng từ Hội đồng (**10 phút Q&A**).
- [ ] **Việt & Phương**: Quay 1 video clip ngắn (Screen Recording ~2 phút) ghi lại quá trình chạy 4 kịch bản demo trên giao diện Streamlit/FastAPI để làm phương án dự phòng (*Backup Offline Demo*) trong trường hợp mạng lỗi tại phòng bảo vệ.

---

### 📌 NGÀY 8: CHỦ NHẬT (06/09/2026) — TỔNG DUYỆT CUỐI CÙNG, CẬP NHẬT NHẬT KÝ & NỘP CHO GVHD
- [ ] **Trường (Leader)**: Cập nhật nhật ký tuần của 4 thành viên vào file Excel theo dõi tiến độ: `Tham Khảo/SP26IA04_GSP04_PROCESS_REPORT.xlsx`.
- [ ] **Trường (Leader)**: Đóng gói và gửi toàn bộ hồ sơ cho Giảng viên hướng dẫn:
  1. Báo cáo **Report No. 1** (`Review1_Problem_Definition_and_Threat_Model.md`).
  2. Dàn ý và file trình chiếu **Slide PPT Review 1** (`Review1_Presentation_Slides_Outline.md` & `.pptx`).
  3. Bảng tiến độ làm việc tuần (`PROCESS_REPORT.xlsx`).
- [ ] **Cả nhóm**: Chốt lịch bảo vệ Review 1 chính thức với GVHD và sẵn sàng tâm lý tự tin bảo vệ trước Hội đồng.

---

## 📊 IV. BẢNG CHECKLIST KIỂM TOÁN CHẤT LƯỢNG NGHIỆM THU (AUDIT MATRIX)

Trước khi đóng tuần vào ngày 06/09/2026, nhóm trưởng và từng thành viên phải tick kiểm tra đủ 10 tiêu chí:

| STT | Tiêu chí kiểm toán chất lượng | Yêu cầu đạt chuẩn | Người kiểm tra | Trạng thái |
| :---: | :--- | :--- | :---: | :---: |
| 1 | **Problem Statement** | Nêu rõ bản chất Lỗ hổng Von Neumann trong Transformer ($X = S \mathbin{\Vert} U$). | Trường | [x] ĐẠT |
| 2 | **Threat Taxonomy** | Bảng phân biệt 3 trục Direct Injection vs Indirect Injection vs Jailbreak theo OWASP LLM01. | Trường | [x] ĐẠT |
| 3 | **Threat Model & Surface** | Sơ đồ luồng tấn công NIST AI 100-2e2025; khóa chặt Attack Surface tại REST API `/v1/chat`. | Đức | [x] ĐẠT |
| 4 | **3-Tier Layered Defense** | Thể hiện rõ Lớp 1 (Input Guardrail - trọng tâm đồ án), Lớp 2 (LLM), Lớp 3 (Output Sanitizer). | Đức | [x] ĐẠT |
| 5 | **Robustness Design** | 3 tầng phòng thủ chống lẩn tránh cú pháp Leetspeak, Spacing, Base64/Cipher. | Đức | [x] ĐẠT |
| 6 | **Research Questions** | 3 RQs chuẩn IEEE và chuyên ngành ATTT (RQ1, RQ2, RQ3) gắn liền 3 Research Gaps. | Phương | [x] ĐẠT |
| 7 | **Model Selection Matrix** | So sánh 4 hướng Guardrail + Lý do chọn 5 Target LLM Cloud API (kèm trích dẫn >= 2022). | Việt | [x] ĐẠT |
| 8 | **4 Demo Scenarios** | Ma trận $2 \times 2$ có đầy đủ prompt đầu vào, phản hồi vulnerable, JSON block và latency ms. | Việt | [x] ĐẠT |
| 9 | **Slide PPTX Review 1** | Bộ slide hoàn chỉnh phân bổ 4 người trình bày trong 15 phút, hình ảnh trực quan. | Phương | [ ] CẦN HOÀN THIỆN |
| 10 | **Process Report & Nộp bài** | Cập nhật `PROCESS_REPORT.xlsx` và nộp Report No. 1 đúng hạn cho GVHD. | Trường | [ ] CẦN HOÀN THIỆN |

---
*Kế hoạch này được lập tự động dựa trên biên bản họp `Meeting 1_29_08_26.md` và tuân thủ tuyệt đối Quy chế Khóa luận Tốt nghiệp IAP491 Đại học FPT.*
