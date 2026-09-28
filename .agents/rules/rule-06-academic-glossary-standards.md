# 📖 Rule 06: Academic Concept Glossary & Provenance Standards

> **Quy định bất biến về chú thích và giải nghĩa thuật ngữ học thuật (Zero Unexplained Analogy)**  
> **Cơ chế thực thi**: Tự động kiểm toán qua `python Final-Report/scripts/verify_academic_glossary.py` và tích hợp vào `validate_local.py`.

---

## 🎯 1. BỐI CẢNH & MỤC ĐÍCH QUẢN TRỊ

Khi sử dụng các phép so sánh liên ngành (Prepared Statements, Von Neumann, Ring 0/Ring 3, NX-bit) hoặc thuật ngữ toán học/khoa học máy tính chuyên sâu ($X = S \mathbin{\Vert} U$, Competing Objectives, Mismatched Generalization, Refusal Boundary, Group-Aware Splitting):
- Nếu **không chú thích rõ ràng**, sinh viên sẽ lúng túng khi bị Hội đồng hỏi cội nguồn kỹ thuật, dẫn đến bị nghi ngờ về tính trung thực hoặc bị trừ điểm nặng.

---

## 🛡️ 2. QUY TẮC BẤT BIẾN BẮT BUỘC (INVARIANT CONTRACT)

Mọi tài liệu kỹ thuật, chuyên đề nghiên cứu (`docs/`), báo cáo định kỳ (`reports/`) và chương luận văn (`thesis/`) khi xuất hiện thuật ngữ học thuật kinh điển BẮT BUỘC phải tuân thủ:

### 2.1. Đánh Dấu & Tạo Neo Liên Kết (In-Text Anchoring)
1. Khi thuật ngữ xuất hiện lần đầu trong văn bản, phải được định dạng nổi bật và gắn kèm mã neo dạng superscript hoặc link anchor:
   - Cú pháp: `*Prepared Statements* [[TN1]](#term-prepared-statements)` hoặc `[**Prepared Statements**](#term-prepared-statements)`.
2. Neo liên kết phải trỏ thẳng xuống bảng giải nghĩa tương ứng ở cuối tài liệu (đảm bảo không có broken anchor).

### 2.2. Bảng Giải Nghĩa Bắt Buộc Ở Cuối Tài Liệu (Terminal Academic Glossary)
Mỗi tệp tài liệu có chứa thuật ngữ học thuật bắt buộc phải có một mục riêng ở phần kết (trước hoặc sau mục Tài Liệu Tham Khảo):
`## BẢNG THUẬT NGỮ & KHÁI NIỆM HỌC THUẬT NỀN TẢNG (ACADEMIC CONCEPT GLOSSARY)`

### 2.3. Cấu Trúc 4 Trường Chuẩn Mực Cho Từng Thuật Ngữ
Mỗi thuật ngữ trong bảng phải được phân rã đầy đủ theo 4 trường thông tin:
1. **Thuật ngữ (Term & Acronym)**: Tên tiếng Anh chính thức và thuật ngữ dịch chuẩn tiếng Việt.
2. **Định nghĩa khoa học bản chất (Core Scientific Definition)**: Nêu chính xác định nghĩa gốc trong khoa học máy tính hoặc toán học.
3. **Bối cảnh & Phép tương quan đối chiếu trong PI-Guard (Role & Analogy in PI-Guard)**: Giải thích rõ lý do xuất hiện trong bài viết, liên hệ như thế nào với Prompt Injection / Jailbreak và định vị giải pháp của PI-Guard.
4. **Nguồn gốc học thuật & Tiêu chuẩn tham chiếu (Provenance & References)**: Trích dẫn rõ tiêu chuẩn quốc tế (ISO/IEC, NIST, OWASP), bài báo sáng lập hoặc kỷ yếu công bố.

---

## 📚 3. DANH MỤC THUẬT NGỮ CỐT LÕI (CORE ACADEMIC LEXICON REGISTRY)

| Mã | Thuật Ngữ Học Thuật | Phân Lớp Kiến Thức | Tài Liệu Tham Chiếu Gốc |
| :---: | :--- | :--- | :--- |
| **TN1** | **Prepared Statements (Parameterized Queries)** | An ninh Cơ sở Dữ liệu & Công nghệ Phần mềm | ISO/IEC 9075 SQL Standard & OWASP SQLi Defense |
| **TN2** | **Von Neumann Architecture & NX-bit (W^X)** | Kiến trúc Máy tính & Hệ thống | John von Neumann (1945); AMD/Intel x86 NX-bit Feature |
| **TN3** | **Flat Token Space (Không Gian Token Phẳng)** | Xử lý Ngôn ngữ Tự nhiên & Transformer | Perez & Ribeiro (2022) `[[3]]`; Greshake et al. (2023) `[[2]]` |
| **TN4** | **Competing Objectives (Xung đột mục tiêu)** | An toàn Học máy & Căn chỉnh Alignment | Wei et al. (NeurIPS 2023) `[[5]]` |
| **TN5** | **Mismatched Generalization (Tổng quát hóa lệch)** | Thuyết Học máy & Miền Phân Phối (OOD) | Wei et al. (NeurIPS 2023) `[[5]]`; Yuan et al. (ICLR 2024) `[[17]]` |
| **TN6** | **Refusal Boundary (Ranh giới từ chối)** | An toàn Mô hình Nền tảng (Safety Tuning) | Ouyang et al. (NeurIPS 2022 InstructGPT); Shen et al. (CCS 2024) `[[11]]` |
| **TN7** | **Goal Hijacking & Prompt Leaking** | Phân loại Lỗ hổng Ứng dụng LLM | Perez & Ribeiro (2022) `[[3]]`; OWASP LLM01:2025 `[[8]]` |
| **TN8** | **Complete Mediation Principle** | Nguyên lý An toàn Thông tin Kinh điển | Saltzer & Schroeder (IEEE Proc. 1975) `[[18]]` |
| **TN9** | **Group-Aware Splitting (MD5 Clustering)** | Phương pháp luận Kỹ nghệ Dữ liệu An ninh | Shen et al. (ACM CCS 2024) `[[11]]` |
| **TN10**| **Masked Overlap Fraction (MOF Invariance)** | Kháng Overdefense Trên Code Lập Trình | Hao Li et al. (ACL 2025) `[[18]]` |
| **TN11**| **Autoregressive Transformer (Transformer tự hồi quy)** | Xử lý Ngôn ngữ Tự nhiên & Mô hình Tạo sinh | Vaswani et al. (NeurIPS 2017) `[[20]]`; Radford et al. (2019) |
