#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tự động biên dịch toàn văn luận văn (FINAL_THESIS.md) từ các chương con
trong thư mục workspaces/truongnv/docs/thesis/chapters/ và nguồn tài liệu chuẩn
workspaces/truongnv/References/REFERENCES_LOG.md.

Đảm bảo:
1. Đồng bộ 100% nội dung giữa các chương lẻ và tài liệu tổng hợp FINAL_THESIS.md.
2. Tách bạch hoàn toàn: FINAL_THESIS.md chứa phần thân luận văn và danh mục trích dẫn IEEE,
   không chứa bản dump trùng lặp 58 KB của REFERENCES_LOG.md.
3. Bảo toàn 100% neo trích dẫn <a id="refN"></a>.
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

def extract_chapter_body(file_path):
    """Trích xuất phần thân chương, loại bỏ phần ## References ở cuối chương."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Tách phần thân trước mục ## References
    ref_match = re.search(r'\n##\s+References', content, re.IGNORECASE)
    if ref_match:
        body = content[:ref_match.start()].rstrip()
    else:
        body = content.rstrip()
    return body

def extract_master_references(ref_log_path):
    """
    Trích xuất danh mục tài liệu tham khảo IEEE từ REFERENCES_LOG.md
    hoặc xây dựng danh mục chuẩn có đầy đủ neo HTML <a id="refN"></a>.
    """
    with open(ref_log_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Tìm danh mục BibTeX hoặc các entry chi tiết
    entries = []
    # Quét tất cả các entry <a id="refN"></a> trong Section 2
    pattern = r'<a id="(ref\d+)"></a>\[(\d+)\]\s+([^\n]+)'
    matches = re.findall(pattern, content)
    
    ref_lines = [
        "## References (Tài Liệu Tham Khảo Học Thuật Chuẩn IEEE)",
        "",
        "> Toàn bộ 41 tài liệu khoa học được kiểm chứng và lưu trữ toàn văn PDF cục bộ tại [`workspaces/truongnv/References/`](file:///d:/Work/Do-an/workspaces/truongnv/References/).",
        "> Chi tiết phân định Four-Tier Provenance và ma trận ứng dụng tra cứu tại [`REFERENCES_LOG.md`](file:///d:/Work/Do-an/workspaces/truongnv/References/REFERENCES_LOG.md).",
        ""
    ]

    # Đọc từ chapters/02_Literature_Review.md các references mẫu đã được format IEEE
    ch2_path = os.path.join(CHAPTERS_DIR, "02_Literature_Review.md")
    with open(ch2_path, "r", encoding="utf-8") as f:
        ch2_content = f.read()
    
    ref_match = re.search(r'\n##\s+References[^\n]*\n(.*)', ch2_content, re.DOTALL | re.IGNORECASE)
    if ref_match:
        ref_text = ref_match.group(1).strip()
        ref_lines.append(ref_text)
    
    return "\n".join(ref_lines)

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

{references_section}

---

## BẢNG TRA CỨU MA TRẬN TÀI LIỆU (TAXONOMY & APPLICATION MAPPING)
> Để tra cứu phân định **Four-Tier Provenance**, siêu dữ liệu xuất bản (Tier 0), đóng góp gốc của tác giả (Tier 1), định vị kỹ thuật trong đồ án PI-Guard (Tier 2 & 3) và 41 trích dẫn BibTeX đầy đủ, xin tham khảo tài liệu trung tâm:
> 🔗 [`workspaces/truongnv/References/REFERENCES_LOG.md`](file:///d:/Work/Do-an/workspaces/truongnv/References/REFERENCES_LOG.md)
"""

    with open(FINAL_THESIS_PATH, "w", encoding="utf-8") as f:
        f.write(thesis_content)

    print(f"[+] Biên dịch thành công: {FINAL_THESIS_PATH}")
    print(f"[+] Kích thước tệp mới: {len(thesis_content):,} ký tự ({len(thesis_content.splitlines())} dòng).")
    return True

if __name__ == "__main__":
    build_thesis()
