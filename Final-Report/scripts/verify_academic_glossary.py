#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_academic_glossary.py - Automated Validator for Academic Terminology & Concept Glossaries

Kiểm tra tính toàn vẹn của các neo thuật ngữ học thuật (academic terms)
và bảng giải nghĩa cuối tài liệu (Academic Concept Glossary) trong các báo cáo kỹ thuật.
"""

import sys
import re
import argparse
from pathlib import Path

# Đảm bảo UTF-8 trên console Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

CORE_ACADEMIC_TERMS = [
    "Prepared Statements",
    "Von Neumann",
    "NX-bit",
    "W^X",
    "Flat Token Space",
    "Competing Objectives",
    "Mismatched Generalization",
    "Refusal Boundary",
    "Goal Hijacking",
    "Prompt Leaking",
    "Complete Mediation",
    "Group-Aware Splitting",
    "ZeroQuant",
    "Transformer tự hồi quy",
    "Autoregressive Transformer"
]

def verify_file_glossary(file_path: Path) -> bool:
    if not file_path.exists():
        print(f"❌ File không tồn tại: {file_path}")
        return False

    content = file_path.read_text(encoding="utf-8")
    
    # Kiểm tra xem file có chứa thuật ngữ học thuật không
    detected_terms = [t for t in CORE_ACADEMIC_TERMS if t.lower() in content.lower()]
    
    if not detected_terms:
        # File không chứa thuật ngữ cần kiểm tra
        return True

    print(f"\n📄 Đang kiểm tra file: {file_path.name}")
    print(f"   🔍 Tìm thấy {len(detected_terms)} thuật ngữ học thuật nền tảng: {', '.join(detected_terms)}")

    # 1. Kiểm tra sự tồn tại của mục Glossary
    has_glossary = bool(re.search(r'##\s+.*(?:BẢNG THUẬT NGỮ|ACADEMIC CONCEPT GLOSSARY|THUẬT NGỮ KỸ THUẬT)', content, re.IGNORECASE))
    
    # 2. Kiểm tra các anchor dạng #term-...
    term_links = re.findall(r'\[(?:[^\]]+)\]\((#term-[a-zA-Z0-9_-]+)\)', content)
    term_anchors = re.findall(r'<a\s+id=[\'"](term-[a-zA-Z0-9_-]+)[\'"]\s*>', content)

    missing_anchors = []
    for link in set(term_links):
        anchor_id = link.lstrip("#")
        if anchor_id not in term_anchors:
            missing_anchors.append(anchor_id)

    if not has_glossary and len(detected_terms) >= 3:
        print(f"   ⚠️  [CẢNH BÁO] File xuất hiện {len(detected_terms)} thuật ngữ học thuật nhưng chưa có mục BẢNG THUẬT NGỮ & KHÁI NIỆM HỌC THUẬT NỀN TẢNG ở cuối!")
        return False

    if missing_anchors:
        print(f"   ❌ [LỖI] Tìm thấy các liên kết thuật ngữ trỏ tới neo không tồn tại trên trang: {missing_anchors}")
        return False

    print(f"   ✔ [PASS] Cấu trúc chú thích thuật ngữ hợp lệ! ({len(term_anchors)} neo thuật ngữ đã định nghĩa)")
    return True

def main():
    parser = argparse.ArgumentParser(description="Kiểm tra neo và bảng chú thích thuật ngữ học thuật")
    parser.add_argument("--file", type=str, help="Đường dẫn tệp Markdown cần kiểm tra")
    parser.add_argument("--all", action="store_true", help="Quét toàn bộ thư mục workspaces và reports")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent.parent

    if args.file:
        target = Path(args.file)
        if not target.is_absolute():
            target = repo_root / target
        success = verify_file_glossary(target)
        sys.exit(0 if success else 1)

    # Nếu quét toàn bộ các file báo cáo Task Meeting 4
    task_dir = repo_root / "workspaces" / "truongnv" / "reports" / "task_for_meeting_4"
    if task_dir.exists():
        all_passed = True
        for md_file in task_dir.glob("TASK_*.md"):
            if not verify_file_glossary(md_file):
                all_passed = False
        sys.exit(0 if all_passed else 1)

if __name__ == "__main__":
    main()
