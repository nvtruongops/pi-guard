#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tự động biên dịch toàn văn luận văn (FINAL_THESIS.md) từ các chương con
trong thư mục workspaces/truongnv/docs/thesis/chapters/ và nguồn tài liệu chuẩn
workspaces/truongnv/References/REFERENCES_LOG.md.

Đảm bảo:
1. Đồng bộ 100% nội dung giữa các chương lẻ và tài liệu tổng hợp FINAL_THESIS.md.
2. Tích hợp đầy đủ Bảng Chú Thích Thuật Ngữ Học Thuật Nền Tảng (Academic Concept Glossary).
3. Đầy đủ danh mục trích dẫn chuẩn IEEE và ma trận phân định Four-Tier Provenance.
4. Bảo toàn 100% neo trích dẫn <a id="refN"></a> và neo thuật ngữ <a id="term-..."></a>.
"""

import os
import re
import sys

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
THESIS_DIR = os.path.join(BASE_DIR, "docs", "thesis")
CHAPTERS_DIR = os.path.join(THESIS_DIR, "chapters")
FINAL_THESIS_PATH = os.path.join(THESIS_DIR, "FINAL_THESIS.md")
REFERENCES_LOG_PATH = os.path.join(BASE_DIR, "References", "REFERENCES_LOG.md")

FRONTMATTER = """# MINISTRY OF EDUCATION AND TRAINING
# FPT UNIVERSITY
## CAPSTONE PROJECT THESIS (IAP491)

# PI-GUARD: A MACHINE-LEARNING GUARDRAIL FOR DETECTING PROMPT INJECTION AND JAILBREAK ATTACKS ON LLM APPLICATIONS

**Academic Program**: Information Assurance (IA)  
**Academic Term**: Fall 2026  
**Capstone Code**: `IAP491_FA26_PI_GUARD`  

---

### GROUP MEMBERS:
1. **Nguyễn Văn Trường (Leader)** — Student ID: `SE182034`
2. **Nguyễn Quí Đức** — Student ID: `SE182087`
3. **Phạm Minh Hoàng Việt** — Student ID: `SE181851`
4. **Đỗ Đoàn Duy Phương** — Student ID: `SE180235`

**Supervisor**: Trần Văn Ninh  

---
"""

ACADEMIC_GLOSSARY = """## BẢNG THUẬT NGỮ & KHÁI NIỆM HỌC THUẬT NỀN TẢNG (ACADEMIC CONCEPT GLOSSARY)

> [!NOTE]
> ### 📖 Vai Trò Của Bảng Giải Nghĩa Thuật Ngữ Học Thuật
> Nhằm phục vụ tốt nhất cho việc đánh giá học thuật và bảo vệ đồ án trước Hội đồng chấm tốt nghiệp (Academic Council) theo quy chuẩn [`.agents/rules/academic-terminology-and-glossary-standards.md`](file:///d:/Work/Do-an/.agents/rules/academic-terminology-and-glossary-standards.md), bảng dưới đây phân tích chi tiết các khái niệm và phép so sánh liên ngành xuất hiện trong toàn bộ luận văn theo 4 trường thông tin chuẩn mực:

| Mã Neo | Thuật Ngữ & Khái Niệm | Định Nghĩa Khoa Học Bản Chất | Bối Cảnh & Phép Tương Quan Đối Chiếu Trong PI-Guard | Nguồn Gốc & Tài Liệu Tham Chiếu |
| :---: | :--- | :--- | :--- | :--- |
| <a id="term-von-neumann"></a>**TN1** | **Von Neumann Architecture (Kiến Trúc Von Neumann)** | Mô hình kiến trúc máy tính nền tảng nơi Dữ liệu và Mã lệnh thực thi cùng lưu trữ chung trong một không gian bộ nhớ vật lý duy nhất. | **Phép đối sánh cội nguồn**: Xuất hiện tại Chương 1 & 2 để giải thích cội nguồn lịch sử của Prompt Injection: LLM không có ranh giới phần cứng tách lệnh khỏi dữ liệu. | John von Neumann (1945), *"First Draft of a Report on the EDVAC"*; K. Thompson (1984). |
| <a id="term-nx-bit"></a>**TN2** | **NX-bit / W^X (No-Execute Bit / Write XOR Execute)** | Cơ chế bảo vệ bộ nhớ mức phần cứng CPU (Memory Page Protection) đánh dấu các phân vùng dữ liệu (`.data`, Stack, Heap) là không thể thực thi mã, ngăn chặn triệt để tấn công chèn shellcode thực thi lệnh (Buffer Overflow). | **Phép đối sánh giải pháp**: Nêu tại Chương 1 & 2. Trong hệ điều hành hiện đại, vấn đề chèn mã đã được giải quyết bằng cờ phần cứng. Ngược lại, kiến trúc Transformer hiện nay chưa có cơ chế phần cứng tương đương để đánh dấu token của người dùng $U$ là "Non-Executable Token". | AMD Enhanced Virus Protection (EVP) & Intel XD-bit (2004); OpenBSD W^X Security Policy. |
| <a id="term-prepared-statements"></a>**TN3** | **Prepared Statements (Truy Vấn Tham Số Hóa)** | Kỹ thuật trong hệ quản trị cơ sở dữ liệu quan hệ (RDBMS) tách biệt hoàn toàn pha biên dịch cú pháp câu lệnh SQL và pha truyền nạp dữ liệu người dùng qua các biến tham số hóa riêng biệt (Placeholders). | **Phép đối sánh tương phản**: Nêu tại Chương 1 & 2. Trong SQL, dữ liệu người dùng không bao giờ có thể trở thành cú pháp điều khiển nhờ Prepared Statements. Tuy nhiên trong LLM, không thể có "Prepared Prompt" vì câu lệnh hệ thống ($S$) và dữ liệu người dùng ($U$) bị nối phẳng thành một chuỗi token duy nhất ($X = S \Vert U$), bắt buộc phải dùng rào chắn ngoại vi (PI-Guard). | Tiêu chuẩn ISO/IEC 9075 (SQL); OWASP SQL Injection Prevention Cheat Sheet. |
| <a id="term-flat-token-space"></a>**TN4** | **Flat Token Space (Không Gian Token Phẳng)** | Hiện tượng chuỗi chỉ thị hệ thống ($S$) và dữ liệu người dùng ($U$) bị nối chuỗi (*concatenation*) thành một mảng token duy nhất ($X = S \mathbin{\Vert} U$) và cùng tham gia vào ma trận Self-Attention với quyền hạn tương đương. | **Căn nguyên kỹ thuật cốt lõi**: Trình bày tại Chương 1 & 2. Là gốc rễ khiến LLM bị Prompt Injection, vì các token của dữ liệu người dùng $U$ có toàn quyền tương tác ma trận chú ý ($QK^T$) để làm lu mờ hoặc ghi đè biểu diễn của token chỉ thị $S$. PI-Guard giải quyết bằng cách thanh tra $U$ độc lập trước khi nạp vào LLM. | Perez & Ribeiro (NeurIPS 2022) [[3]](#ref3); Greshake et al. (ACM AISec 2023) [[4]](#ref4). |
| <a id="term-goal-hijacking"></a>**TN5** | **Goal Hijacking (Chiếm Đoạt Mục Tiêu Ứng Dụng)** | Kỹ thuật tiêm lệnh ép LLM bỏ qua mục tiêu nghiệp vụ ban đầu để thực hiện một mục tiêu trái phép do kẻ tấn công chỉ định. | **Kịch bản thiệt hại 1**: Trình bày tại Chương 1 & 2. Gây tổn hại nghiêm trọng về tính toàn vẹn (Integrity) của ứng dụng tích hợp LLM. | Perez & Ribeiro (2022) [[3]](#ref3). |
| <a id="term-prompt-leaking"></a>**TN6** | **Prompt Leaking (Đánh Cắp Chỉ Thị Ẩn)** | Kỹ thuật tấn công ép mô hình in ra nguyên văn System Prompt, bí mật kinh doanh hoặc API keys nhúng trong bối cảnh. | **Kịch bản thiệt hại 2**: Trình bày tại Chương 1 & 2. Gây tổn hại nghiêm trọng về tính bí mật (Confidentiality) và quyền sở hữu trí tuệ của doanh nghiệp. | Perez & Ribeiro (2022) [[3]](#ref3); OWASP LLM01:2025 [[8]](#ref8). |
| <a id="term-competing-objectives"></a>**TN7** | **Competing Objectives (Xung Đột Mục Tiêu Căn Chỉnh)** | Trạng thái mâu thuẫn nội tại khi mô hình phải tối ưu hóa đồng thời hai mục tiêu đối nghịch: Tính hữu ích (*Helpfulness*) và Tính vô hại (*Harmlessness*). | **Cơ chế gốc của Jailbreak 1**: Trình bày tại Chương 1 & 2. Kẻ tấn công tạo dựng các kịch bản khẩn cấp hoặc nghiên cứu học thuật để kích hoạt tối đa tính *Helpfulness*, ép mô hình hạ thấp và vô hiệu hóa rào cản *Harmlessness*. | Alexander Wei, Nika Haghtalab, Jacob Steinhardt (NeurIPS 2023) [[5]](#ref5). |
| <a id="term-mismatched-generalization"></a>**TN8** | **Mismatched Generalization (Tổng Quát Hóa Lệch)** | Năng lực biểu diễn và giải mã ngôn ngữ tổng quát của mô hình vượt xa phạm vi dữ liệu an toàn mà mô hình được tinh chỉnh (*Safety Fine-Tuning*). | **Cơ chế gốc của Jailbreak 2**: Trình bày tại Chương 1 & 2. Khi payload được mã hóa Base64 hoặc Leetspeak, mô hình vẫn hiểu ý đồ nhưng rào cản an toàn không kích hoạt. | Wei et al. (NeurIPS 2023) [[5]](#ref5); Yuan et al. (ICLR 2024) [[17]](#ref17); Zou et al. (2023) [[24]](#ref24). |
| <a id="term-refusal-boundary"></a>**TN9** | **Refusal Boundary (Ranh Giới Từ Chối An Toàn)** | Siêu mặt phẳng quyết định (Decision Boundary) trong không gian tham số của mô hình nền tảng, xác định ngưỡng kích hoạt câu trả lời từ chối chuẩn (*Refusal Action*) trước các yêu cầu vi phạm đạo đức/pháp luật. | **Ranh giới phân biệt PI vs. Jailbreak**: Trình bày tại Chương 1 & 2. Jailbreak cố tình bẻ gãy ranh giới này; ngược lại Prompt Injection lách qua ranh giới này hoàn toàn mà không bị phát hiện vì bản thân câu lệnh tiêm nhiễm không chứa từ ngữ độc hại. | Long Ouyang et al. (InstructGPT / NeurIPS 2022); Shen et al. (ACM CCS 2024) [[15]](#ref15). |
| <a id="term-complete-mediation"></a>**TN10** | **Complete Mediation Principle (Nguyên Lý Kiểm Soát Toàn Diện)** | Nguyên lý an toàn hệ thống đòi hỏi mọi truy cập vào đối tượng được bảo vệ đều phải được kiểm tra và xác thực mà không có lối tắt ngoại lệ. | **Cơ sở kiến trúc Ingress Guardrail**: Trình bày tại Chương 1 & 2. Mọi dữ liệu đầu vào (từ người dùng trực tiếp hoặc từ các nguồn dữ liệu bên thứ ba RAG/Plugin) đều bắt buộc phải đi qua PI-Guard trước khi chạm tới LLM. | Saltzer & Schroeder, *"The Protection of Information in Computer Systems"*, IEEE 1975. |
| <a id="term-disentangled-attention"></a>**TN11** | **Disentangled Attention Mechanism (Cơ Chế Chú Ý Phân Tách)** | Cơ chế attention trong DeBERTa biểu diễn mỗi token bằng 2 vector riêng biệt: nội dung (Content) và vị trí tương đối (Relative Position). | **Cơ sở lựa chọn mô hình Tầng 2**: Trình bày tại Chương 1 & 2. Giúp PI-Guard nhận diện chính xác các cấu trúc đảo ngữ và hoán đổi vị trí câu lệnh tiêm nhiễm trong prompt mà BERT/RoBERTa truyền thống dễ bỏ sót. | Pengcheng He et al. (ICLR 2023) [[11]](#ref11). |
| <a id="term-group-aware-splitting"></a>**TN12** | **Group-Aware Splitting (Phân Tách Dữ Liệu Bảo Toàn Cụm)** | Phương pháp phân chia tập dữ liệu train/val/test theo cụm kịch bản ngữ nghĩa thay vì phân chia ngẫu nhiên, đảm bảo toàn bộ biến thể của một mẫu tấn công chỉ nằm trong một tập. | **Giải pháp kỹ thuật Gap 1**: Trình bày tại Chương 1 & 2. Triệt tiêu hiện tượng rò rỉ dữ liệu giữa train và test ($\text{Inter-cluster Jaccard} < 0.15$), bảo đảm kết quả đánh giá mô hình phản ánh đúng năng lực phát hiện tấn công Zero-day thực tế. | Shen et al. (ACM CCS 2024) [[15]](#ref15); Phương pháp luận kỹ nghệ dữ liệu PI-Guard. |
| <a id="term-autoregressive-transformer"></a>**TN13** | **Autoregressive Transformer (Mô Hình Transformer Tự Hồi Quy)** | Kiến trúc mạng nơ-ron Transformer sinh chuỗi tuần tự theo phân phối xác suất có điều kiện $P(y_t \mid y_{<t}, X)$. | **Cơ sở kiến trúc mô hình**: Trình bày tại Chương 1 & 2. Giải thích lý do tại sao LLM không thể tự kiểm tra an toàn cấu trúc như compiler: LLM chỉ dự đoán token tiếp theo có xác suất cao nhất dựa trên toàn bộ chuỗi $X$ nạp vào. | A. Vaswani et al. (NeurIPS 2017); Radford et al. (OpenAI GPT series, 2019). |
"""

def extract_chapter_body(file_path):
    """Trích xuất phần thân chương, loại bỏ phần Glossary và References ở cuối chương."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Tách phần thân trước mục Glossary hoặc References
    cutoff_match = re.search(r'\n##\s+(?:References|BẢNG THUẬT NGỮ|ACADEMIC CONCEPT GLOSSARY|📖 BẢNG THUẬT NGỮ)', content, re.IGNORECASE)
    if cutoff_match:
        body = content[:cutoff_match.start()].rstrip()
    else:
        body = content.rstrip()
    return body

def extract_master_references(ref_log_path):
    """
    Trích xuất danh mục tài liệu tham khảo IEEE từ chapters/02_Literature_Review.md
    và tích hợp toàn bộ ma trận Four-Tier Provenance từ REFERENCES_LOG.md.
    """
    ch2_path = os.path.join(CHAPTERS_DIR, "02_Literature_Review.md")
    with open(ch2_path, "r", encoding="utf-8") as f:
        ch2_content = f.read()
    
    ref_match = re.search(r'\n##\s+References[^\n]*\n(.*)', ch2_content, re.DOTALL | re.IGNORECASE)
    ieee_list = ref_match.group(1).strip() if ref_match else ""

    with open(ref_log_path, "r", encoding="utf-8") as f:
        ref_log_content = f.read()

    return f"""## References (Tài Liệu Tham Khảo Học Thuật Chuẩn IEEE)

{ieee_list}

---

{ref_log_content}"""

def build_thesis():
    print("[*] Đang biên dịch FINAL_THESIS.md từ các chương con...")
    ch1_path = os.path.join(CHAPTERS_DIR, "01_Introduction.md")
    ch2_path = os.path.join(CHAPTERS_DIR, "02_Literature_Review.md")

    if not os.path.exists(ch1_path) or not os.path.exists(ch2_path):
        print("[-] Lỗi: Không tìm thấy tệp chương trong", CHAPTERS_DIR)
        return False

    ch1_body = extract_chapter_body(ch1_path)
    ch2_body = extract_chapter_body(ch2_path)
    references_section = extract_master_references(REFERENCES_LOG_PATH)

    thesis_content = f"""{FRONTMATTER}

{ch1_body}

---

{ch2_body}

---

{ACADEMIC_GLOSSARY}

---

{references_section}
"""

    with open(FINAL_THESIS_PATH, "w", encoding="utf-8") as f:
        f.write(thesis_content)

    print(f"[+] Biên dịch thành công: {FINAL_THESIS_PATH}")
    print(f"[+] Kích thước tệp mới: {len(thesis_content):,} ký tự ({len(thesis_content.splitlines())} dòng).")
    return True

if __name__ == "__main__":
    build_thesis()
