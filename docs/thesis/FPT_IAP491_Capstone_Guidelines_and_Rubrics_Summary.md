# HƯỚNG DẪN & TIÊU CHÍ ĐÁNH GIÁ KHÓA LUẬN TỐT NGHIỆP FPT UNIVERSITY
## 🎓 Quy Chuẩn Học Thuật IAP491 (Research-Based Thesis) Cho Ngành An Toàn Thông Tin

> **Tài liệu căn cứ & trích xuất chính thức**:
> - Tài liệu gốc: `docs/fpt_capstone_guide/IAP491_CP_StudentsGuideForm for Research Based Thesis.docx`
> - Biểu mẫu & Báo cáo tham khảo: `docs/fpt_capstone_guide/Tham Khảo/` (Biểu mẫu Báo cáo tiến độ `PROCESS_REPORT.xlsx`, Slide thuyết trình Review & Final Thesis).
> - **Áp dụng cho**: Đồ án **PI-Guard** (`IAP491_FA26_PI_GUARD`) — Ngành An toàn Thông tin (Information Assurance), Đại học FPT.  
> - **Cập nhật ngày**: 2026-09-04  

---

## 📜 I. QUY ĐỊNH CHUNG & ĐIỀU KIỆN THỰC HIỆN ĐỒ ÁN (COMMON REGULATIONS)

Căn cứ quy định đào tạo bậc Đại học của Trường Đại học FPT cho học phần Khóa luận Tốt nghiệp (Capstone Project - CP):

1. **Điều kiện tốt nghiệp**: Khóa luận tốt nghiệp là học phần bắt buộc (10 Tín chỉ) để sinh viên đủ điều kiện nhận bằng Cử nhân/Kỹ sư An toàn Thông tin.
2. **Quy mô & Tổ chức**:
   - Học phần được tổ chức theo lớp chuyên đề, mỗi lớp do Giảng viên Hướng dẫn (Supervisor / Mentor) phụ trách và chia thành các nhóm từ 3 đến 5 sinh viên (nhóm tiêu chuẩn: 4 – 5 thành viên).
   - Thời gian thực hiện: Trọn vẹn 1 học kỳ chính thức (**15 Tuần thực học**, net duration 12–15 tuần).
3. **Ngôn ngữ chính thức**: **100% Tiếng Anh (English)** cho toàn bộ tài liệu hồ sơ, báo cáo luận văn và buổi thuyết trình bảo vệ trước Hội đồng.
4. **Tham gia họp tiến độ bắt buộc**: Sinh viên bắt buộc phải tham gia đầy đủ tất cả các buổi họp định kỳ và đột xuất với Giảng viên Hướng dẫn theo lịch hẹn trước.
5. **Điều kiện tiên quyết để làm đồ án**:
   - Tích lũy tối thiểu **80% tổng số tín chỉ** của chương trình đào tạo (không tính GDTC, GDQP và OJT).
   - Hoàn thành kỳ thực tập doanh nghiệp (**On-the-Job-Training - OJT**).
   - Đã qua các môn học tiên quyết bắt buộc: `IAP301` (Policy Development in Information Assurance) hoặc `SPM401`; môn mạng nâng cao `NWC302`/`NWC204`; và tối thiểu một môn chuyên sâu ngành (`IAM302`, `FRS401(c)`, `HOD401`, `DBS401`).

---

## 🏆 II. CƠ CHẾ ĐÁNH GIÁ & CÔNG THỨC TÍNH ĐIỂM (EVALUATION SYSTEM)

Khóa luận được đánh giá toàn diện qua hai trụ cột: **Điểm Quá Trình (50%)** và **Điểm Bảo Vệ Hội Đồng (50%)** trên **Thang điểm 10 (làm tròn 1 chữ số thập phân)**.

$$\text{Final Project Mark} = (\text{Process Mark / Continuous Assessment} \times 50\%) + (\text{Presentation Mark} \times 50\%)$$

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                             TỔNG ĐIỂM ĐỒ ÁN TỐT NGHIỆP (PROJECT MARK: 100%)                       │
├──────────────────────────────────────────────────┬───────────────────────────────────────────────┤
│ 📝 ĐIỂM QUÁ TRÌNH (PROCESS MARK: 50%)            │ 🏛️ ĐIỂM BẢO VỆ HỘI ĐỒNG (PRESENTATION: 50%)   │
│ - Do Giảng viên Hướng dẫn (Supervisor) đánh giá  │ - Do Hội đồng Chấm Tốt nghiệp (Committee)     │
│ - Chấm điểm liên tục qua 6 Báo cáo tiến độ       │   chấm điểm độc lập từng sinh viên            │
│ - Cá nhân hóa theo mức độ đóng góp (GM ± 20%)    │ - Lấy điểm trung bình của tất cả thành viên HĐ│
└──────────────────────────────────────────────────┴───────────────────────────────────────────────┘
```

### 📊 1. Trọng Số Chi Tiết 6 Báo Cáo Tiến Độ (Continuous Assessment / Process Mark)

| Báo Cáo | Tên Chương / Nội Dung Báo Cáo | Thời Gian Nộp Dự Kiến | Trọng Số Trong Process Mark | Trọng Số Trong Tổng Điểm Đồ Án |
| :---: | :--- | :---: | :---: | :---: |
| **Report No.1** | **Introduction** (Bối cảnh, Bài toán, Mục tiêu RQ1–RQ3, Ý nghĩa, Phạm vi) | Đầu Tuần 3 | **10%** | 5.0% |
| **Report No.2** | **Literature Review** (Khảo sát y văn, Phân loại tấn công, SOTA Guardrails) | Đầu Tuần 4 | **25%** | 12.5% |
| **Report No.3** | **Methodology** (Thiết kế nghiên cứu, Dữ liệu, Trích xuất đặc trưng & Mô hình) | Đầu Tuần 7 | **20%** | 10.0% |
| **Report No.4** | **Experimental and Results** (Môi trường, Thực nghiệm, Đối sánh & Robustness) | Đầu Tuần 9 | **25%** | 12.5% |
| **Report No.5** | **Discussion** (Thảo luận ý nghĩa phát hiện, Trade-offs & Giới hạn thực tiễn) | Đầu Tuần 13 | **15%** | 7.5% |
| **Report No.6** | **Conclusion and Future Work** (Tổng kết đóng góp kỹ thuật & Hướng mở rộng) | Đầu Tuần 13 | **5%** | 2.5% |
| **TỔNG** | **Toàn Bộ 6 Báo Cáo Đánh Giá Quá Trình** | **Tuần 1 – 13** | **100%** | **50.0%** |

### 👤 2. Quy Tắc Phân Bổ Điểm Cá Nhân (Personal Mark Formula)
- Trên mỗi giai đoạn báo cáo, Giảng viên Hướng dẫn sẽ chấm **Điểm Nhóm (Group Mark - GM)**.
- Điểm cá nhân của từng sinh viên (**Personal Mark**) được xác định linh hoạt dựa trên khối lượng công việc và mức độ đóng góp thực tế:
  $$\text{Personal Mark} \in [100\% \text{ GM} - 20\% \text{ GM}, \; 100\% \text{ GM} + 20\% \text{ GM}]$$
- Sự đóng góp của từng thành viên được minh chứng rõ ràng qua file theo dõi tiến độ hàng tuần [`Meeting/PI_GUARD_PROCESS_REPORT.xlsx`](file:///d:/Work/Do-an/Meeting/PI_GUARD_PROCESS_REPORT.xlsx).

---

## 📅 III. LỘ TRÌNH THỰC HIỆN & 4 CỘT MỐC CHÍNH (MILESTONE TIMELINE HỌC KỲ FALL 2026)

Quy trình bảo vệ đồ án tốt nghiệp Khóa luận IAP491 trong học kỳ mới (Fall 2026: 15 Tuần từ 07/09 đến 20/12/2026) được chuẩn hóa thành **4 Cột Mốc Quyết Định**:

1. 🎯 **CỘT MỐC 1: REVIEW 1 (với GVHD — Tuần 3-4 / 28/09 – 04/10/2026)**:
   - **Nội dung**: Bối cảnh, Lỗ hổng Von Neumann NLP, Phát biểu bài toán, 3 RQ cốt lõi, Threat Model NIST AI 100-2e2025, Khảo sát y văn quốc tế và Đối sánh các trường phái Guardrails SOTA.
   - **Hồ sơ nghiệm thu**: **Report No.1 (Chapter 1: Introduction)** & **Report No.2 (Chapter 2: Literature Review)** + Slide PPT Review 1.
   - **Quy tắc bất biến**: 100% Nghiên cứu lý thuyết & y văn (Zero Code / Không tạo mô hình trong Review 1).
   - **Trọng số**: Chiếm **35% Process Mark** (17.5% tổng điểm đồ án).

2. 🎯 **CỘT MỐC 2: REVIEW 2 (với GVHD — Tuần 8 / 26/10 – 01/11/2026)**:
   - **Nội dung**: Phương pháp luận nghiên cứu, Thu thập và khử trùng lặp Dataset, Group-Aware Splitting, Trích xuất đặc trưng TF-IDF (Word/Char n-grams) và Huấn luyện mô hình Classical ML Baseline.
   - **Hồ sơ nghiệm thu**: **Report No.3 (Chapter 3: Methodology)** + Mã nguồn Baseline ML & Báo cáo tiến độ cập nhật.
   - **Trọng số**: Chiếm **20% Process Mark** (10.0% tổng điểm đồ án).

3. 🏛️ **CỘT MỐC 3: BÁO CÁO HỘI ĐỒNG 1 / HỘI ĐỒNG GIỮA KỲ (Tuần 13 / 30/11 – 06/12/2026)**:
   - **Nội dung**: Kết quả thực nghiệm Transformer DeBERTa-v3, Lượng hóa động Post-Training Quantization (ONNX INT8), Đo đạc thực nghiệm độ bền (Robustness on Leetspeak/Base64/Spacing) và Demo Prototype API Middleware + Dashboard Streamlit.
   - **Hồ sơ nghiệm thu**: **Report No.4 (Chapter 4: Experimental and Results)** + Hệ thống Prototype Demo hoạt động trực tiếp.
   - **Trọng số**: Chiếm **25% Process Mark** (12.5% tổng điểm đồ án).

4. 🎓 **CỘT MỐC 4: BÁO CÁO HỘI ĐỒNG FINAL / BẢO VỆ TỐT NGHIỆP (Tuần 15 / 14/12 – 20/12/2026)**:
   - **Nội dung**: Hoàn thiện toàn văn Luận văn 6 Chương, Thảo luận ý nghĩa an ninh & giới hạn (Chapter 5), Kết luận & Hướng phát triển tương lai (Chapter 6), Kiểm tra đạo văn Turnitin (< 20%) và Thuyết trình bảo vệ tốt nghiệp chính thức trước Hội đồng FPT.
   - **Hồ sơ nghiệm thu**: **Report No.5 (Discussion)** + **Report No.6 (Conclusion)** + **Toàn văn Luận văn Final Thesis PDF** + Slide PPT Bảo vệ Tốt nghiệp.
   - **Trọng số**: Chiếm **20% Process Mark còn lại + 50% Presentation Mark** (60.0% tổng điểm đồ án).

```
29/08 - 06/09 ─► [ SPRINT TIỀN ĐỀ ] ──────► Họp GVHD (Meeting 1), Lọc Papers (Meeting 2), Setup Workspace
Tuần 1 - 2 ────► Khảo sát y văn, chuẩn hóa Threat Model, soạn thảo Chapter 1 & Chapter 2
Tuần 3 - 4 ────► [ CỘT MỐC 1: REVIEW 1 (GVHD) ] ──────────► Report No.1 (Intro) & Report No.2 (Lit Review)
Tuần 5 - 7 ────► Data Engineering, Group-Aware Split, Baseline ML (TF-IDF) & Soạn thảo Chapter 3
Tuần 8 ────────► [ CỘT MỐC 2: REVIEW 2 (GVHD) ] ──────────► Report No.3 (Methodology & Baseline ML)
Tuần 9 - 12 ───► Fine-tuning DeBERTa-v3, ONNX INT8, Test Robustness, FastAPI & Dashboard Streamlit
Tuần 13 ───────► [ CỘT MỐC 3: BÁO CÁO HỘI ĐỒNG 1 ] ──────► Report No.4 (Experimental, INT8 & Prototype)
Tuần 14 ───────► Hoàn thiện toàn văn Luận văn 6 Chương (Final Thesis PDF), Quét Turnitin (< 20%)
Tuần 15 ───────► [ CỘT MỐC 4: BẢO VỆ TỐT NGHIỆP FINAL ] ───► Report No.5, No.6 & BẢO VỆ TỐT NGHIỆP CHÍNH THỨC
```

### 📋 Bảng Chi Tiết Tiến Trình 15 Tuần & Hạng Mục Bàn Giao:

| Giai Đoạn & Tuần | Thời Gian Cụ Thể | Cột Mốc / Sự Kiện | Sản Phẩm Bàn Giao Cụ Thể | Trọng Số Điểm |
| :--- | :---: | :--- | :--- | :---: |
| **Sprint Tiền Đề** | 29/08 – 06/09/2026 | Khởi động & Họp GVHD | Biên bản Meeting 1, Meeting 2, Bản đăng ký [`CAPSTONE PROJECT REGISTER.md`](file:///d:/Work/Do-an/CAPSTONE%20PROJECT%20REGISTER.md) | Duyệt đề tài |
| **Tuần 1 – Tuần 4** | 07/09 – 04/10/2026 | **🎯 CỘT MỐC 1: REVIEW 1** *(với GVHD)* | **Report No.1** (Intro - 10%) + **Report No.2** (Lit Review - 25%) + PPT Review 1 | **35% Process** |
| **Tuần 5 – Tuần 8** | 05/10 – 01/11/2026 | **🎯 CỘT MỐC 2: REVIEW 2** *(với GVHD)* | **Report No.3** (Methodology - 20%) + Baseline ML Code | **20% Process** |
| **Tuần 9 – Tuần 13**| 02/11 – 06/12/2026 | **🏛️ CỘT MỐC 3: HỘI ĐỒNG GIỮA KỲ** | **Report No.4** (Experimental - 25%) + Demo Prototype (API/UI) | **25% Process** |
| **Tuần 14** | 07/12 – 13/12/2026 | Tổng duyệt Luận văn Final | **Report No.5** (Discussion - 15%) + **Report No.6** (Conclusion - 5%) + Turnitin < 20% | **20% Process** |
| **Tuần 15** | 14/12 – 20/12/2026 | **🎓 CỘT MỐC 4: BẢO VỆ TỐT NGHIỆP** | Toàn văn Final Thesis PDF + Thuyết trình bảo vệ trước Hội đồng chấm FPT | **50% Presentation** |

---

## 📚 IV. CẤU TRÚC CHUẨN TOÀN VĂN LUẬN VĂN HỌC THUẬT (6 CHƯƠNG)

Mỗi cuốn Luận văn Khóa luận Tốt nghiệp IAP491 tại Đại học FPT bắt buộc tuân thủ chặt chẽ cấu trúc chuẩn sau:

```
TRANG BÌA NGOÀI & TRANG TIÊU ĐỀ (Title Page - Ministry of Education and Training, FPT University)
BẢN CAM ĐOAN TÁC QUYỀN (Declaration of Authorship)
LỜI CẢM ƠN (Acknowledgement - Tùy chọn)
TÓM TẮT LUẬN VĂN (Abstract - 200 đến 300 từ: Background, Methods, Results, Conclusions)
DANH MỤC TỪ KHÓA (Keywords: 3 - 10 từ khóa học thuật)
MỤC LỤC (Table of Contents - Đánh số trang tự động)
DANH MỤC HÌNH ẢNH (List of Figures)
DANH MỤC BẢNG BIỂU (List of Tables)
DANH MỤC VIẾT TẮT (List of Abbreviations - Acronym & Full Meaning)

CHAPTER 1: INTRODUCTION
  1.1. Background (Bối cảnh GenAI, Prompting và sự bùng nổ của các ứng dụng LLM)
  1.2. Problem Statement (Phát biểu bài toán: Lỗ hổng Von Neumann trong NLP, Threat Model)
  1.3. Research Objectives (Hệ thống 3 Câu hỏi Nghiên cứu RQ1–RQ3 chuẩn IEEE)
  1.4. Significance of the Study (Ý nghĩa khoa học, tính cấp thiết và giá trị thực tiễn)
  1.5. Scope and Limitations (Phạm vi đề tài: In-Scope vs. Out-of-Scope)
  1.6. Thesis Structure (Bố cục tổng quan các chương của cuốn Luận văn)

CHAPTER 2: LITERATURE REVIEW
  2.1. Review of Previous Studies (Khảo sát toàn diện các nghiên cứu Prompt Injection, Jailbreak & Guardrail SOTA)
  2.2. Summary of the Literature Review (Bảng tổng hợp đối chuẩn các trường phái tiếp cận trong y văn)
  2.3. Contribution of Research (3 Research Gaps & Các đóng góp mới của đề tài PI-Guard)

CHAPTER 3: METHODOLOGY
  3.1. Research Design (Thiết kế nghiên cứu tổng thể: Offline Training Pipeline vs Online Guardrail Inference)
  3.2. Data Collection Methods (Thu thập, làm sạch, khử trùng lặp và gán nhãn dataset công khai)
  3.3. Sampling & Data Analysis Techniques (Group-Aware Splitting, Trích xuất TF-IDF & Kiến trúc DeBERTa-v3)
  3.4. Limitations of the Methodology (Các giới hạn về độ trễ, tài nguyên tính toán và ranh giới phương pháp)

CHAPTER 4: EXPERIMENTAL AND RESULTS
  4.1. Introduction & Setup (Môi trường thực nghiệm, Siêu tham số, Cấu hình phần cứng)
  4.2. Presentation of Data (Phân bố lớp dữ liệu, phân tích đặc trưng các mẫu tấn công)
  4.3. Analysis of Results (Kết quả phân loại: Baseline ML vs DeBERTa-v3 vs SOTA ProtectAI)
  4.4. Interpretation of Results (Ma trận nhầm lẫn Confusion Matrix, Đường cong ROC-AUC, FPR)
  4.5. Comparison with Literature (So sánh đối chuẩn với Llama Guard 3, NeMo Guardrails, v.v.)
  4.6. Implications of the Results (Đánh giá độ bền Robustness trước kỹ thuật lẩn tránh Leetspeak/Base64)

CHAPTER 5: DISCUSSION
  5.1. Restate the Research Problem or Objectives (Khẳng định lại bài toán và mục tiêu ban đầu)
  5.2. Summarize Key Findings (Tổng kết các phát hiện định lượng: F1 > 0.98, FPR < 1.1%, Latency < 15ms)
  5.3. Security Implications & Trade-offs (Phân tích đánh đổi giữa Độ an toàn và Trải nghiệm người dùng)
  5.4. Practical Limitations & Challenges (Hạn chế thực tế trong môi trường sản xuất thực tế)

CHAPTER 6: CONCLUSION AND FUTURE WORK
  6.1. Conclusion (Tổng kết toàn diện các kết quả và đóng góp của đồ án)
  6.2. Future Work (Hướng phát triển mở rộng: Đa ngôn ngữ tiếng Việt, Multimodal Injection, Active Learning)

TÀI LIỆU THAM KHẢO (References - Định dạng chuẩn IEEE, đánh số theo thứ tự xuất hiện [1], [2]...)
PHỤ LỤC (Appendices - Mẫu prompt đối kháng, tài liệu API Endpoints, Code snippets minh họa)
```

---

## ✍️ V. QUY CHUẨN ĐỊNH DẠNG & TRÌNH BÀY HỌC THUẬT (FORMATTING STANDARDS)

### 📌 1. Yêu Cầu Đối Với Phần Tóm Tắt (Abstract)
- **Độ dài**: Bắt buộc trong khoảng **200 đến 300 từ**.
- **Tính chất**: Phải là một văn bản độc lập hoàn chỉnh (**stand-alone text**): không viết tắt chưa giải thích, không dẫn nguồn URL, không dùng citation tham chiếu `[N]`, không dùng khái niệm chưa định nghĩa.
- **Cấu trúc 4 phần chuẩn mực (Structured Abstract without headings)**:
  1. *(1) Background*: Đặt bài toán trong bối cảnh rộng của ngành an toàn thông tin và nêu rõ mục đích nghiên cứu.
  2. *(2) Methods*: Mô tả ngắn gọn phương pháp nghiên cứu, thuật toán và mô hình đã áp dụng.
  3. *(3) Results*: Tóm tắt các kết quả thực nghiệm định lượng nổi bật nhất.
  4. *(4) Conclusions*: Nêu các kết luận then chốt và ý nghĩa ứng dụng thực tiễn của đề tài.
- **Từ khóa (Keywords)**: Cung cấp từ **3 đến 10 từ khóa** học thuật chuẩn quốc tế.

### 📌 2. Yêu Cầu Về Danh Mục Tài Liệu Tham Khảo (References)
- **Chuẩn trích dẫn**: Sử dụng định dạng chuẩn **IEEE Style**.
- **Đánh số**: Tài liệu tham khảo được đánh số theo đúng thứ tự xuất hiện trong toàn văn bài viết `[1], [2], [3]...` (bao gồm cả trong chú thích hình ảnh và bảng biểu).
- **Nguyên tắc Invariant**: Toàn bộ tài liệu tham khảo phải có tính kiểm chứng học thuật (Peer-reviewed Papers, Tech Reports từ 2022 trở lại đây) và bắt buộc dẫn kèm bản mở Open-Access PDF (Zero Dead Links).

### 📌 3. Bảng Biểu & Hình Ảnh (Figures & Tables)
- Mỗi hình ảnh/bảng biểu bắt buộc có số thứ tự, tiêu đề rõ ràng và danh mục tự động ở đầu luận văn:
  - Hình ảnh: Ghi chú phía dưới hình (ví dụ: *Figure 1. The Multi-Layer Defense Architecture of PI-Guard.*).
  - Bảng biểu: Tiêu đề phía trên bảng (ví dụ: *Table 1. Comparative Matrix of SOTA Guardrail Approaches.*).

---

## 👥 VI. PHƯƠNG CHÂM LÀM VIỆC ĐỒNG QUY & PHÂN VAI TRÁCH NHIỆM

Nhằm tối ưu hóa năng lực của tất cả thành viên và đảm bảo từng cá nhân tự tin bảo vệ 100% nội dung trước Hội đồng, nhóm duy trì phương châm:

> **AI CŨNG LÀM $\rightarrow$ THAM KHẢO NHAU $\rightarrow$ CHỐT KẾT QUẢ**

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                        QUY TRÌNH ĐỒNG QUY TRI THỨC TOÀN DIỆN (FULL-PIPELINE CONVERGENCE)                 │
├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. AI CŨNG LÀM (Parallel Hands-on) : 4 Thành viên cùng nghiên cứu toàn trình trong workspace cá nhân   │
│ 2. THAM KHẢO NHAU (Cross-Review)   : Đọc hiểu, đối chiếu code, soi chéo tài liệu và phản biện số liệu  │
│ 3. CHỐT KẾT QUẢ (Leader Consensus) : Họp hàng tuần, chọn champion artifact và merge vào thư mục chung  │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

| Thành Viên | Không Gian Khám Phá | Trọng Tâm Chuyên Sâu Đóng Góp | Vai Trò Chủ Trì Báo Cáo FPT |
| :--- | :--- | :--- | :--- |
| **Nguyễn Văn Trường (Leader)** | `workspaces/truongnv/` | Kiến trúc tổng thể, Chuẩn hóa Dữ liệu Group-Aware Split & Điều phối Luận văn | Chủ trì **Report No.1** (Intro) & **Report No.2** (Lit Review) |
| **Nguyễn Quí Đức** | `workspaces/ducnq/` | Classical ML Baseline (TF-IDF Word/Char, Logistic, SVC, XGBoost) & Bề mặt tấn công | Phản biện Threat Model & Chủ trì **Report No.3** (Methodology) |
| **Phạm Minh Hoàng Việt** | `workspaces/vietpmh/` | Transformer Fine-Tuning (DeBERTa-v3), Lượng hóa INT8 ONNX & Evasion Robustness | Phản biện Deep Learning & Chủ trì **Report No.4** (Experimental) |
| **Đỗ Đoàn Duy Phương** | `workspaces/phuongddd/` | FastAPI Guardrail Middleware, Streamlit Dashboard, Kịch bản Demo & Tổng hợp Luận văn | Phản biện Attack Taxonomy & Chủ trì **Report No.5** + **Report No.6** |


