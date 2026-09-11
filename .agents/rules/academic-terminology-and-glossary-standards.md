# QUY TẮC BẤT BIẾN VỀ CHÚ THÍCH & GIẢI NGHĨA THUẬT NGỮ HỌC THUẬT (ACADEMIC TERMINOLOGY & GLOSSARY STANDARDS)

---

## 🎯 1. BỐI CẢNH & MỤC ĐÍCH QUẢN TRỊ
Trong quá trình bảo vệ đồ án trước Hội đồng chấm tốt nghiệp FPT University (Academic Council) và GVHD, sinh viên thường sử dụng các phép so sánh liên ngành (Interdisciplinary Analogies) hoặc các thuật ngữ toán học/khoa học máy tính chuyên sâu như:
- **Phép so sánh an ninh hệ thống & cơ sở dữ liệu**: *Prepared Statements*, *Kiến trúc Von Neumann*, *Phân tách đặc quyền Ring 0 / Ring 3*, *Cờ phần cứng NX-bit / W^X*.
- **Cơ sở lý thuyết học máy & căn chỉnh an toàn**: *Không gian token phẳng ($X = S \Vert U$)*, *Xung đột mục tiêu (Competing Objectives)*, *Tổng quát hóa lệch (Mismatched Generalization)*, *Ranh giới từ chối (Refusal Boundary)*, *Hàm mất mát có trọng số động (Class-Weighted Loss)*.

> [!CAUTION]
> **RỦI RO HỌC THUẬT TRƯỚC HỘI ĐỒNG PHẢN BIỆN**:
> Khi đưa các thuật ngữ hoặc phép so sánh này vào báo cáo kỹ thuật mà **không chú thích rõ ràng**:
> 1. Thành viên nhóm khi bị hỏi bất ngờ sẽ lúng túng, không giải thích được cội nguồn kỹ thuật (ví dụ: *"Prepared Statements trong SQL hoạt động thế nào và tại sao LLM lại không làm được như thế?"*).
> 2. Hội đồng sẽ nghi ngờ tính trung thực học thuật hoặc coi việc dùng từ là sáo rỗng, dẫn đến trừ điểm phản biện cá nhân.

---

## 🛡️ 2. QUY TẮC BẤT BIẾN BẮT BUỘC (INVARIANT CONTRACT)

Mọi tài liệu kỹ thuật, chuyên đề nghiên cứu (`docs/`), báo cáo định kỳ (`reports/`) và chương luận văn (`thesis/`) khi xuất hiện các từ khóa/phép so sánh học thuật kinh điển BẮT BUỘC phải tuân thủ:

### 2.1. Đánh Dấu & Tạo Neo Liên Kết (In-Text Anchoring)
1. Khi thuật ngữ xuất hiện lần đầu trong văn bản, phải được định dạng nổi bật và gắn kèm mã neo thuật ngữ dạng superscript hoặc link anchor:
   - Cú pháp: `*Prepared Statements* [[TN1]](#term-prepared-statements)` hoặc `[**Prepared Statements**](#term-prepared-statements)`.
2. Neo liên kết phải trỏ thẳng xuống bảng giải nghĩa tương ứng ở cuối tài liệu (đảm bảo không có broken anchor).

### 2.2. Bảng Giải Nghĩa Bắt Buộc Ở Cuối Tài Liệu (Terminal Academic Glossary)
Mỗi tệp tài liệu có chứa thuật ngữ học thuật bắt buộc phải có một mục riêng ở phần kết (trước hoặc sau mục Tài Liệu Tham Khảo):
`## BẢNG THUẬT NGỮ & KHÁI NIỆM HỌC THUẬT NỀN TẢNG (ACADEMIC CONCEPT GLOSSARY)`

### 2.3. Cấu Trúc 4 Trường Chuẩn Mực Cho Từng Thuật Ngữ
Mỗi thuật ngữ trong bảng phải được phân rã đầy đủ theo 4 trường thông tin:
1. **Thuật ngữ (Term & Acronym)**: Tên tiếng Anh chính thức và thuật ngữ dịch chuẩn tiếng Việt.
2. **Định nghĩa khoa học bản chất (Core Scientific Definition)**: Nêu chính xác định nghĩa gốc trong khoa học máy tính hoặc toán học, không giải thích qua loa.
3. **Bối cảnh & Phép tương quan đối chiếu trong PI-Guard (Role & Analogy in PI-Guard)**: Giải thích rõ lý do xuất hiện trong bài viết, liên hệ như thế nào với Prompt Injection / Jailbreak và định vị giải pháp của PI-Guard.
4. **Nguồn gốc học thuật & Tiêu chuẩn tham chiếu (Provenance & References)**: Trích dẫn rõ tiêu chuẩn quốc tế (ISO/IEC, NIST, OWASP), bài báo sáng lập hoặc kỷ yếu công bố.

---

## 📚 3. DANH MỤC THUẬT NGỮ CỐT LÕI (CORE ACADEMIC LEXICON REGISTRY)

Khi gặp các thuật ngữ sau, AI Agent và thành viên nhóm bắt buộc phải áp dụng quy tắc này:

| Mã | Thuật Ngữ Học Thuật | Phân Lớp Kiến Thức | Tài Liệu Tham Chiếu Gốc |
| :---: | :--- | :--- | :--- |
| **TN1** | **Prepared Statements (Parameterized Queries)** | An ninh Cơ sở Dữ liệu & Công nghệ Phần mềm | ISO/IEC 9075 SQL Standard & OWASP SQLi Defense |
| **TN2** | **Von Neumann Architecture & NX-bit (W^X)** | Kiến trúc Máy tính & Hệ thống | John von Neumann (1945); AMD/Intel x86 NX-bit Hardware Feature |
| **TN3** | **Flat Token Space (Không Gian Token Phẳng)** | Xử lý Ngôn ngữ Tự nhiên & Transformer | Perez & Ribeiro (2022) `[[3]]`; Greshake et al. (2023) `[[2]]` |
| **TN4** | **Competing Objectives (Xung đột mục tiêu)** | An toàn Học máy & Căn chỉnh Alignment | Wei et al. (NeurIPS 2023) `[[5]]` |
| **TN5** | **Mismatched Generalization (Tổng quát hóa lệch)** | Thuyết Học máy & Miền Phân Phối (OOD) | Wei et al. (NeurIPS 2023) `[[5]]`; Yuan et al. (ICLR 2024) `[[17]]` |
| **TN6** | **Refusal Boundary (Ranh giới từ chối)** | An toàn Mô hình Nền tảng (Safety Tuning) | Ouyang et al. (NeurIPS 2022 InstructGPT); Shen et al. (CCS 2024) `[[11]]` |
| **TN7** | **Goal Hijacking & Prompt Leaking** | Phân loại Lỗ hổng Ứng dụng LLM | Perez & Ribeiro (2022) `[[3]]`; OWASP LLM01:2025 `[[8]]` |
| **TN8** | **Complete Mediation Principle** | Nguyên lý An toàn Thông tin Kinh điển | Saltzer & Schroeder (IEEE Proc. 1975) `[[18]]` |
| **TN9** | **Group-Aware Splitting (MD5 Clustering)** | Phương pháp luận Kỹ nghệ Dữ liệu An ninh | Shen et al. (ACM CCS 2024) `[[11]]` |
| **TN10** | **Post-Training Quantization (Dynamic INT8 PTQ)** | Tối ưu hóa & Lượng hóa Mô hình Học sâu | Zhewei Yao et al. (NeurIPS 2022 ZeroQuant) `[[16]]` |
| **TN11** | **Autoregressive Transformer (Transformer tự hồi quy)** | Xử lý Ngôn ngữ Tự nhiên & Mô hình Tạo sinh | Vaswani et al. (NeurIPS 2017) `[[20]]`; Radford et al. (2019) |

---

## 🔍 4. CÔNG CỤ TỰ ĐỘNG HÓA KIỂM ĐỊNH (AUTOMATED QA INTEGRATION)
- Tất cả các neo thuật ngữ và bảng chú thích được kiểm tra tính khớp nối và toàn vẹn tự động thông qua bộ kiểm tra cục bộ `Final-Report/scripts/validate_local.py`.
- Tuyệt đối không để xảy ra tình trạng có thuật ngữ đánh dấu `[[TN*]]` trong văn bản mà thiếu mục giải nghĩa ở cuối trang.
