---
name: academic-terminology-glossary
description: Quy trình phát hiện, đánh dấu và xây dựng Bảng chú thích thuật ngữ học thuật (Academic Concept Glossary & Provenance) cho các báo cáo kỹ thuật, chuyên đề nghiên cứu và luận văn tốt nghiệp PI-Guard.
---

# Academic Terminology & Concept Glossary Skill

## 📌 Mục Đích & Phạm Vi Kỹ Thuật
Kỹ năng này hướng dẫn AI Agent và các thành viên đồ án tự động quét, phát hiện các thuật ngữ khoa học máy tính, các phép so sánh liên ngành (Prepared Statements, Von Neumann, NX-bit, Flat Token Space, Competing Objectives...) trong văn bản, gắn neo liên kết và tự động khởi tạo mục **"BẢNG THUẬT NGỮ & KHÁI NIỆM HỌC THUẬT NỀN TẢNG"** chuẩn mực 4 trường ở cuối tài liệu.

---

## 🛠️ Quy Trình 3 Bước Thực Hiện

### Bước 1: Quét và Định Danh Từ Khóa Trong Văn Bản
Rà soát văn bản kỹ thuật để nhận diện các từ khóa/phép so sánh thuộc các nhóm sau:
1. **Phép so sánh an ninh & phần mềm truyền thống**:
   - `Prepared Statements` / `Parameterized Queries`
   - `Kiến trúc Von Neumann` / `NX-bit` / `W^X (Write XOR Execute)` / `Ring 0 vs Ring 3`
2. **Cơ chế mô hình ngôn ngữ & Transformer**:
   - `Không gian token phẳng (Flat Token Space)` / `X = S || U`
   - `Self-Attention Matrix` / `Disentangled Attention`
   - `Autoregressive Generation`
3. **Lý thuyết căn chỉnh an toàn & Đối kháng**:
   - `Xung đột mục tiêu (Competing Objectives)`
   - `Tổng quát hóa lệch (Mismatched Generalization)`
   - `Ranh giới từ chối (Refusal Boundary)`
   - `Goal Hijacking` & `Prompt Leaking`
4. **Phương pháp luận tối ưu hóa của PI-Guard**:
   - `Group-Aware Splitting`
   - `Dynamic Class-Weighted Loss`
   - `Two-Tier Uncertainty Routing`
   - `Dynamic Post-Training Quantization (INT8 PTQ)`

### Bước 2: Đặt Neo Liên Kết Trong Văn Bản (In-Text Anchoring)
Thay vì để text thô, hãy gắn thẻ liên kết neo học thuật:
- Mẫu 1 (Gắn mã neo `[[TNx]]`):
  `cơ chế Prepared Statements [[TN1]](#term-prepared-statements)`
- Mẫu 2 (Gắn link trực tiếp vào từ khóa):
  `cơ chế [*Prepared Statements*](#term-prepared-statements)`

### Bước 3: Khởi Tạo Bảng Giải Nghĩa 4 Trường Ở Cuối Tài Liệu
Chèn mục sau vào cuối tài liệu (ngay trước hoặc liền kề mục Tài Liệu Tham Khảo):

```markdown
## BẢNG THUẬT NGỮ & KHÁI NIỆM HỌC THUẬT NỀN TẢNG (ACADEMIC CONCEPT GLOSSARY)

| Mã Neo | Thuật Ngữ & Khái Niệm | Định Nghĩa Khoa Học Bản Chất | Bối Cảnh & Phép Tương Quan Đối Chiếu Trong PI-Guard | Nguồn Gốc & Tài Liệu Tham Chiếu |
| :---: | :--- | :--- | :--- | :--- |
| <a id="term-prepared-statements"></a>**TN1** | **Prepared Statements (Parameterized Queries)** | Kỹ thuật trong hệ quản trị cơ sở dữ liệu (DBMS) biên dịch trước khung câu lệnh SQL và tách biệt hoàn toàn mã điều khiển với biến dữ liệu đầu vào của người dùng. | **Phép đối sánh tương phản**: Minh họa nguyên nhân gốc tại sao LLM dính Prompt Injection. Trong SQL, lệnh và dữ liệu nằm ở 2 kênh riêng biệt; ngược lại trong LLM, lệnh hệ thống ($S$) và dữ liệu người dùng ($U$) bị nối phẳng ($X = S \Vert U$) khiến không thể áp dụng Prepared Statements trực tiếp trên mô hình Transformer. | ISO/IEC 9075 SQL Standard; OWASP Top 10 SQL Injection Defense Cheat Sheet. |
```

---

## 📋 Mẫu 4 Trường Chi Tiết Chuẩn Mực

Mỗi mục giải nghĩa thuật ngữ bắt buộc phải thỏa mãn 4 câu hỏi:
1. **Nó là gì? (Định nghĩa bản chất)**: Không giải thích chung chung, phải nêu bản chất kiến trúc phần cứng/phần mềm hoặc công thức toán học.
2. **Nó được dùng ở đâu trong tài liệu này?**: Nêu vị trí đề mục hoặc ngữ cảnh xuất hiện.
3. **Tại sao lại nhắc đến nó trong đồ án PI-Guard?**: Phân tích phép đối sánh hoặc vai trò thực tiễn trong thiết kế rào chắn.
4. **Tham chiếu từ đâu?**: Trích dẫn bài báo, tiêu chuẩn hoặc tài liệu học thuật đã được lưu trữ trong `Final-Report/References/`.

---

## 🛡️ Kiểm Định Tự Động (QA Verification)
Sau khi thêm thuật ngữ:
1. Đảm bảo mọi thẻ `<a id="term-..."></a>` trùng khớp 100% với liên kết `#term-...` trong văn bản.
2. Chạy `python Final-Report/scripts/validate_local.py` để xác nhận không có lỗi cú pháp Markdown.
