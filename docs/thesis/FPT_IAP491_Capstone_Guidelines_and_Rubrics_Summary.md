# HƯỚNG DẪN & TIÊU CHÍ ĐÁNH GIÁ KHÓA LUẬN TỐT NGHIỆP FPT UNIVERSITY
## Quy Chuẩn IAP491 (Research-Based Thesis) Cho Ngành An Toàn Thông Tin

> **Tài liệu gốc tham chiếu**: [`docs/fpt_capstone_guide/IAP491_CP_StudentsGuideForm for Research Based Thesis.docx`](file:///d:/Work/Do-an/docs/fpt_capstone_guide/IAP491_CP_StudentsGuideForm%20for%20Research%20Based%20Thesis.docx)  
> **Áp dụng cho**: Đồ án **PI-Guard** (Information Assurance - FPT University)  
> **Cập nhật ngày**: 2026-09-01  

---

## 🏆 1. CƠ CHẾ TÍNH ĐIỂM TỔNG KẾT (PROJECT MARK BREAKDOWN)

Theo quy định chính thức của Đại học FPT cho học phần Khóa luận tốt nghiệp (10 Tín chỉ):

$$\text{Final Project Mark} = (\text{Process Mark} \times 50\%) + (\text{Presentation Mark} \times 50\%)$$

Trong đó:
- **Process Mark (50% tổng điểm)**: Do Giảng viên Hướng dẫn (Supervisor) chấm điểm quá trình liên tục qua **6 Báo Cáo (Reports No.1 - No.6)**.
- **Presentation Mark (50% tổng điểm)**: Do **Hội đồng Chấm Tốt nghiệp (Committee)** chấm điểm độc lập trong buổi Bảo vệ Tốt nghiệp tại Tuần 15.
- **Điểm cá nhân (Personal Mark)**: Nằm trong khoảng $[100\% \text{ Group Mark} \pm 20\%]$ tùy thuộc vào mức độ đóng góp thực tế của từng sinh viên.

### 📊 Trọng Số 6 Báo Cáo Tiến Độ (Process Mark)

| Báo Cáo | Tên Báo Cáo | Trọng số trong Process Mark | Trọng số trong Tổng điểm Đồ án |
| :---: | :--- | :---: | :---: |
| **Report No.1** | **Introduction** (Bối cảnh, Bài toán, Mục tiêu, Phạm vi) | **10%** | 5.0% |
| **Report No.2** | **Literature Review** (Khảo sát các nghiên cứu & SOTA) | **25%** | 12.5% |
| **Report No.3** | **Methodology** (Thiết kế nghiên cứu, Dữ liệu, Mô hình) | **20%** | 10.0% |
| **Report No.4** | **Experimental and Results** (Thực nghiệm & Kết quả) | **25%** | 12.5% |
| **Report No.5** | **Discussion** (Thảo luận ý nghĩa, So sánh, Giới hạn) | **15%** | 7.5% |
| **Report No.6** | **Conclusion and Future Work** (Kết luận & Hướng phát triển)| **5%** | 2.5% |
| **TỔNG** | **Toàn bộ 6 Báo Cáo Quá Trình** | **100%** | **50.0%** |

---

## 📅 2. LỘ TRÌNH THỰC HIỆN & 4 CỘT MỐC CHÍNH (MILESTONE TIMELINE)

Quy trình bảo vệ đồ án được chuẩn hóa thành **4 Cột Mốc Quyết Định**:
1. 🎯 **CỘT MỐC 1: REVIEW 1** *(với GVHD - Tuần 3-4 / 28/09 – 04/10)*: Xác định bài toán & Khảo sát nghiên cứu SOTA (**Chapter 1 & Chapter 2**).
2. 🎯 **CỘT MỐC 2: REVIEW 2** *(với GVHD - Tuần 8 / 26/10 – 01/11)*: Phương pháp luận, Dữ liệu Group-Aware Split, Baseline ML & Cập nhật Docs (**Chapter 3 & Report No.3**).
3. 🏛️ **CỘT MỐC 3: BÁO CÁO HỘI ĐỒNG 1** *(Hội đồng Giữa kỳ - Tuần 13 / 30/11 – 06/12)*: Kết quả thực nghiệm Transformer DeBERTa-v3, ONNX INT8 & Prototype FastAPI/Streamlit (**Chapter 4 & Report No.4**).
4. 🎓 **CỘT MỐC 4: BÁO CÁO HỘI ĐỒNG FINAL** *(Hội đồng Tốt nghiệp - Tuần 15 / 14/12 – 20/12)*: Toàn văn Luận văn 6 Chương hoàn chỉnh, Quét Turnitin (< 20%) & Bảo vệ Tốt nghiệp chính thức (**Chapters 1 – 6**).

```
Tuần 1 ────► Chốt nhóm & Đề tài với GVHD (CAPSTONE PROJECT REGISTER)
Tuần 3-4 ──► [ CỘT MỐC 1: REVIEW 1 (GVHD) ] ──────────► Report No.1 (Intro) & Report No.2 (Lit Review)
Tuần 5-7 ──► Data Engineering, Baseline ML & Soạn thảo, Cập nhật Docs Chapter 3
Tuần 8 ────► [ CỘT MỐC 2: REVIEW 2 (GVHD) ] ──────────► Report No.3 (Methodology & Baseline ML)
Tuần 9-12 ─► Nghiên cứu Transformer DeBERTa-v3, ONNX INT8, FastAPI Middleware & Prototype Demo
Tuần 13 ───► [ CỘT MỐC 3: BÁO CÁO HỘI ĐỒNG 1 ] ──────► Report No.4 (Experimental, INT8 & Prototype)
Tuần 14 ───► Hoàn thiện toàn văn Luận văn (Final Thesis PDF) & Check đạo văn Turnitin (< 20%)
Tuần 15 ───► [ CỘT MỐC 4: BÁO CÁO HỘI ĐỒNG FINAL ] ───► Report No.5, No.6 & BẢO VỆ TỐT NGHIỆP CHÍNH THỨC
```

---

## 📚 3. CẤU TRÚC CHUẨN LUẬN VĂN HỌC THUẬT IAP491 (6 CHƯƠNG)

Mỗi cuốn Khóa luận Tốt nghiệp tại FPT University bắt buộc tuân thủ bố cục chuẩn 6 chương:

```
TRANG BÌA (Cover Page & Title Page)
BẢN CAM ĐOAN TÁC QUYỀN (Declaration of Authorship)
LỜI CẢM ƠN (Acknowledgement)
TÓM TẮT LUẬN VĂN (Abstract - 200 đến 300 từ: Background, Methods, Results, Conclusions)
DANH MỤC TỪ KHÓA (Keywords: 3-10 từ khóa)
MỤC LỤC (Table of Contents)
DANH MỤC BẢNG BIỂU (List of Tables)
DANH MỤC HÌNH ẢNH (List of Figures)
DANH MỤC VIẾT TẮT (List of Abbreviations)

CHAPTER 1: INTRODUCTION
  1.1. Background
  1.2. Problem Statement
  1.3. Research Objectives
  1.4. Significance of the Study
  1.5. Scope and Limitations
  1.6. Thesis Structure

CHAPTER 2: LITERATURE REVIEW
  2.1. Review of Previous Studies (Khảo sát các kỹ thuật Prompt Injection, Jailbreak & Guardrails)
  2.2. Summary of the Literature Review
  2.3. Contribution of Research (Đóng góp mới của nhóm)

CHAPTER 3: METHODOLOGY
  3.1. Research Design (Kiến trúc tổng thể 2 pha Offline Training / Online Inference)
  3.2. Data Collection Methods (Curation, Deduplication, Hugging Face sources)
  3.3. Sampling & Data Analysis Techniques (Group-Aware Splitting, TF-IDF + DeBERTa-v3)
  3.4. Limitations of the Methodology

CHAPTER 4: EXPERIMENTAL AND RESULTS
  4.1. Introduction & Setup (Môi trường, Siêu tham số)
  4.2. Presentation of Data (Phân bố nhãn, cụm dữ liệu)
  4.3. Analysis of Results (Baseline vs DeBERTa-v3 vs SOTA ProtectAI)
  4.4. Interpretation of Results (Confusion Matrix, ROC-AUC)
  4.5. Comparison with Literature (So sánh với Llama Guard, NeMo)
  4.6. Implications of the Results (Độ bền với Leetspeak/Base64)

CHAPTER 5: DISCUSSION
  5.1. Restate the Research Problem or Objectives
  5.2. Summarize Key Findings (Đạt P95 Latency < 15ms, FPR < 1.1%, F1 > 0.98)
  5.3. Security Implications & Trade-offs (Cân bằng giữa Bảo mật và Trải nghiệm người dùng)
  5.4. Practical Limitations & Challenges

CHAPTER 6: CONCLUSION AND FUTURE WORK
  6.1. Conclusion (Tổng kết đóng góp đồ án)
  6.2. Future Work (Mở rộng đa ngôn ngữ, multimodal injection, online continuous learning)

TÀI LIỆU THAM KHẢO (References - Đánh số theo thứ tự xuất hiện chuẩn IEEE [1], [2]...)
PHỤ LỤC (Appendices - Code snippets, API documentation, Prompt samples)
```

---

## 👥 4. PHÂN CÔNG VAI TRÒ 4 THÀNH VIÊN THEO 6 BÁO CÁO FPT

| Thành viên | Trách nhiệm chính trong Đồ án | Phụ trách Báo Cáo Tiến Độ |
| :--- | :--- | :--- |
| **Nguyễn Văn Trường (Leader)** | Kiến trúc tổng thể, Thu thập Dataset & Group-Aware Split | **Report No.1** (Introduction) + **Report No.2** (Literature Review) |
| **Nguyễn Quí Đức** | Classical ML Baseline (Word/Char TF-IDF, Logistic, SVC, XGBoost) | **Report No.3** (Methodology - Baseline ML & Feature Engineering) |
| **Phạm Minh Hoàng Việt** | Transformer Fine-Tuning (DeBERTa-v3), Lượng hóa ONNX & Robustness | **Report No.4** (Experimental & Results - Training & Adversarial Tests) |
| **Đỗ Đoàn Duy Phương** | FastAPI Guardrail Middleware, Streamlit Dashboard & Viết Luận văn | **Report No.5** (Discussion) + **Report No.6** (Conclusion & Slide Deck) |

---

## 📑 5. BẢN ĐỒ TÀI LIỆU THAM KHẢO CỦA TRƯỜNG (`docs/fpt_capstone_guide/`)

Toàn bộ tài liệu gốc của Trường đã được tích hợp trực tiếp vào repo:

| Thư mục / File | Mô tả nội dung | Vị trí áp dụng |
| :--- | :--- | :--- |
| [`IAP491_CP_StudentsGuideForm for Research Based Thesis.docx`](file:///d:/Work/Do-an/docs/fpt_capstone_guide/IAP491_CP_StudentsGuideForm%20for%20Research%20Based%20Thesis.docx) | Mẫu chuẩn văn bản luận văn nghiên cứu IA | Dùng làm khung chuẩn cho toàn bộ tài liệu luận văn |
| [`Tham Khảo/SP26IA04_GSP04_FINAL_THESIS.pdf`](file:///d:/Work/Do-an/docs/fpt_capstone_guide/Tham%20Kh%E1%BA%A3o/SP26IA04_GSP04_FINAL_THESIS.pdf) | Luận văn mẫu của nhóm khóa trước đạt điểm cao | Mẫu trình bày học thuật, bảng biểu, trích dẫn |
| [`Tham Khảo/SP26IA04_GSP04_CAPSTONE_PROJECT_PRESENTATION.pptx`](file:///d:/Work/Do-an/docs/fpt_capstone_guide/Tham%20Kh%E1%BA%A3o/SP26IA04_GSP04_CAPSTONE_PROJECT_PRESENTATION.pptx) | Mẫu slide thuyết trình PowerPoint bảo vệ tốt nghiệp | Mẫu thiết kế slide cho Review 1 - Review 4 |
| [`Tham Khảo/SP26IA04_GSP04_PROCESS_REPORT.xlsx`](file:///d:/Work/Do-an/docs/fpt_capstone_guide/Tham%20Kh%E1%BA%A3o/SP26IA04_GSP04_PROCESS_REPORT.xlsx) | Bảng theo dõi tiến độ hàng tuần nộp cho GVHD | Dùng để cập nhật nhật ký làm việc của 4 thành viên |
| [`Viết Báo/Paper_2.pdf`](file:///d:/Work/Do-an/docs/fpt_capstone_guide/Vi%E1%BA%BFt%20B%C3%A1o/Paper_2.pdf) | Mẫu bài báo khoa học chuẩn IEEE/ACM | Dùng nếu nhóm viết bài báo khoa học xuất bản hội nghị |
