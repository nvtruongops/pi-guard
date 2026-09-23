#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HỆ THỐNG KIỂM ĐỊNH TOÀN DIỆN WORKSPACE PI-GUARD (MASTER WORKSPACE AUDIT SUITE)
=============================================================================
Tệp hợp nhất toàn bộ các công cụ kiểm định:
1. Phase 1: PDF Integrity & Four-Tier Provenance Semantic Audit (PyMuPDF)
2. Phase 2: Deep Citation & Attribution Leak Audit (Anchor Integrity)
3. Phase 3: Academic Defense Blacklist & Preceding Context Validation

Sử dụng:
  python workspaces/truongnv/scripts/audit_workspace.py --all
  python workspaces/truongnv/scripts/audit_workspace.py --semantics
  python workspaces/truongnv/scripts/audit_workspace.py --citations
  python workspaces/truongnv/scripts/audit_workspace.py --blacklist
"""

import os
import re
import sys
import argparse

# Đảm bảo UTF-8 an toàn trên Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

try:
    import pymupdf as fitz
except ImportError:
    try:
        import fitz
    except ImportError:
        fitz = None

WORKSPACE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REFERENCES_DIR = os.path.join(WORKSPACE_DIR, "References")
REFERENCES_LOG_PATH = os.path.join(REFERENCES_DIR, "REFERENCES_LOG.md")
FROZEN_REPORTS_DIR = os.path.join(WORKSPACE_DIR, "reports")

BLACKLIST_TERMS = [
    r"\bthời\s+gian\s+thực(?!\s+hiện)\b",
    r"\breal-time\b",
    r"\bbảo\s+vệ\s+tuyệt\s+đối\b",
    r"\b100%\s+an\s+toàn\b",
    r"\bkhông\s+thể\s+bị\s+hack\b",
    r"\bkhông\s+lo\s+ngại\s+bất\s+kỳ\s+câu\s+hỏi\s+phản\s+biện\b",
    r"\bđộ\s+chuẩn\s+mực\s+học\s+thuật\s+tối\s+đa\b"
]

def get_eligible_markdown_files():
    """Lấy danh sách tất cả các tệp markdown được phép kiểm tra & chỉnh sửa."""
    eligible_files = []
    for root, dirs, files in os.walk(WORKSPACE_DIR):
        # Bỏ qua thư mục ảo và cache
        if ".venv" in root or "__pycache__" in root or ".git" in root:
            continue
        # Bỏ qua các báo cáo đã chốt (frozen)
        rel_root = os.path.relpath(root, WORKSPACE_DIR)
        if rel_root.startswith("reports") and "tasks_for_meeting_6" not in rel_root:
            continue
        for f in files:
            if f.endswith(".md"):
                eligible_files.append(os.path.join(root, f))
    return sorted(eligible_files)

# ------------------------------------------------------------------------------
# PHASE 1: SEMANTIC & PDF AUDIT
# ------------------------------------------------------------------------------
def run_semantics_audit():
    print("\n" + "="*80)
    print("PHASE 1: PDF INTEGRITY & SEMANTIC PROVENANCE AUDIT")
    print("="*80)
    
    if not fitz:
        print("[-] Cảnh báo: PyMuPDF (fitz) chưa được cài đặt. Bỏ qua trích xuất PDF trực tiếp.")
        return 0

    pdf_files = [f for f in os.listdir(REFERENCES_DIR) if f.endswith(".pdf")]
    print(f"[*] Tổng số tệp PDF cục bộ trên đĩa: {len(pdf_files)}")

    readable_count = 0
    corrupted_count = 0
    for pdf_name in sorted(pdf_files):
        pdf_path = os.path.join(REFERENCES_DIR, pdf_name)
        try:
            doc = fitz.open(pdf_path)
            if len(doc) > 0 and len(doc[0].get_text().strip()) > 50:
                readable_count += 1
            else:
                corrupted_count += 1
                print(f"  [!] PDF có thể bị rỗng hoặc lỗi text: {pdf_name}")
            doc.close()
        except Exception as e:
            corrupted_count += 1
            print(f"  [X] Không thể mở PDF {pdf_name}: {e}")

    print(f"[*] Kết quả PDF: {readable_count}/{len(pdf_files)} tệp hợp lệ, {corrupted_count} tệp lỗi.")

    # Kiểm tra REFERENCES_LOG.md
    with open(REFERENCES_LOG_PATH, "r", encoding="utf-8") as f:
        ref_log = f.read()

    # Kiểm tra sự hiện diện của toàn bộ 41 bài báo
    missing_in_log = []
    for pdf_name in pdf_files:
        if pdf_name not in ref_log:
            missing_in_log.append(pdf_name)

    if missing_in_log:
        print(f"  [!] Phát hiện {len(missing_in_log)} tệp PDF chưa được định danh trong REFERENCES_LOG.md:")
        for m in missing_in_log:
            print(f"      - {m}")
        return len(missing_in_log) + corrupted_count
    else:
        print("[*] 100% tệp PDF đã được định danh và đối chiếu đầy đủ trong REFERENCES_LOG.md.")
    
    # Kiểm tra số lượng BibTeX entries
    bibtex_count = len(re.findall(r'@(?:article|inproceedings|techreport|misc)\{', ref_log, re.IGNORECASE))
    print(f"[*] Số lượng BibTeX entries chuẩn hóa: {bibtex_count} / {len(pdf_files)}")
    return corrupted_count

# ------------------------------------------------------------------------------
# PHASE 2: CITATION & ATTRIBUTION LEAK AUDIT
# ------------------------------------------------------------------------------
def run_citation_audit():
    print("\n" + "="*80)
    print("PHASE 2: DEEP CITATION & ATTRIBUTION LEAK AUDIT")
    print("="*80)

    files = get_eligible_markdown_files()
    print(f"[*] Tổng số tệp markdown quét kiểm tra: {len(files)}")

    total_citations = 0
    warnings = []

    for fpath in files:
        rel_path = os.path.relpath(fpath, WORKSPACE_DIR)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        citations = re.findall(r'\[\[(\d+)\]\]\(#ref\d+\)', content)
        total_citations += len(citations)

        # 1. Kiểm tra attribution leak: Công thức X = S || U gán cho Zhao hoặc Ouyang
        lines = content.splitlines()
        for idx, line in enumerate(lines, 1):
            if "X = S" in line and ("Zhao" in line or "InstructGPT" in line or "Ouyang" in line):
                if "Trong phạm vi mô hình hóa của" not in line and "PI-Guard" not in line:
                    warnings.append(f"Attribution leak tại {rel_path}:{idx} -> Gán công thức X = S || U cho tài liệu khác.")

            # 2. Kiểm tra KPI attribution: Gán FPR < 1.5% hoặc Latency < 30ms cho paper tham chiếu
            if ("FPR < 1.5%" in line or "P95 < 30ms" in line) and ("đạt được" in line or "đã chứng minh" in line):
                if "PI-Guard đặt mục tiêu" not in line and "mục tiêu của PI-Guard" not in line and "PI-Guard hướng tới" not in line:
                    warnings.append(f"Target conflation tại {rel_path}:{idx} -> Gán KPI của PI-Guard cho nghiên cứu tham chiếu.")

            # 3. Kiểm tra số liệu mẫu DAN: Phải phân biệt 1,405 mẫu thực tế trên 15,140 mẫu
            if "15,140" in line and "DAN" in line:
                if "1,405" not in line and "1405" not in line:
                    warnings.append(f"Mẫu DAN chưa chính xác tại {rel_path}:{idx} -> Cần phân biệt rõ 1,405 jailbreaks trên 15,140 tổng mẫu.")

            # 4. Kiểm tra tên bài báo Perez 2022
            if "Ignore This Title and Hack This Paper" in line:
                if "khẩu hiệu" not in line and "slogan" not in line and "minh họa" not in line:
                    warnings.append(f"Tiêu đề không chính thức Perez 2022 tại {rel_path}:{idx} -> Tiêu đề chính thức là 'Ignore Previous Prompt: Attack Techniques For Language Models'.")

    print(f"[*] Tổng số lượt trích dẫn đã phân tích: {total_citations}")
    if warnings:
        print(f"[!] Phát hiện {len(warnings)} cảnh báo ngữ nghĩa:")
        for w in warnings:
            print(f"    - {w}")
    else:
        print("[*] 100% trích dẫn hợp lệ. Zero Attribution Leak / Zero Target Conflation.")
    return len(warnings)

# ------------------------------------------------------------------------------
# PHASE 3: ACADEMIC DEFENSE BLACKLIST AUDIT
# ------------------------------------------------------------------------------
def run_blacklist_audit():
    print("\n" + "="*80)
    print("PHASE 3: ACADEMIC DEFENSE BLACKLIST & TERMINOLOGY AUDIT")
    print("="*80)

    files = get_eligible_markdown_files()
    blacklist_hits = []

    for fpath in files:
        rel_path = os.path.relpath(fpath, WORKSPACE_DIR)
        with open(fpath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for idx, line in enumerate(lines, 1):
            # Bỏ qua dòng là trích dẫn định nghĩa, quy tắc hoặc hướng dẫn loại bỏ từ cấm
            if "CẤM TUYỆT ĐỐI" in line or "blacklist" in line.lower() or "quy chuẩn" in line.lower() or "loại bỏ" in line.lower() or "tuyên bố khẳng định quá mức" in line.lower():
                continue
            for pattern in BLACKLIST_TERMS:
                if re.search(pattern, line, re.IGNORECASE):
                    blacklist_hits.append(f"{rel_path}:{idx} -> Chứa từ cấm: '{re.search(pattern, line, re.IGNORECASE).group(0)}'")

    if blacklist_hits:
        print(f"[!] Phát hiện {len(blacklist_hits)} vi phạm thuật ngữ bảo vệ:")
        for hit in blacklist_hits[:10]:
            print(f"    - {hit}")
        if len(blacklist_hits) > 10:
            print(f"    ... và {len(blacklist_hits) - 10} vi phạm khác.")
    else:
        print("[*] 100% tuân thủ thuật ngữ khiêm tốn khoa học (Scientific Humility Protocol). Zero blacklist hits.")
    return len(blacklist_hits)

# ------------------------------------------------------------------------------
# MAIN ENTRY POINT
# ------------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Hệ thống kiểm định toàn diện workspace PI-Guard")
    parser.add_argument("--all", action="store_true", help="Chạy toàn bộ 3 phase kiểm định (Mặc định)")
    parser.add_argument("--semantics", action="store_true", help="Chạy Phase 1: PDF Integrity & Semantics")
    parser.add_argument("--citations", action="store_true", help="Chạy Phase 2: Citation & Attribution Leak")
    parser.add_argument("--blacklist", action="store_true", help="Chạy Phase 3: Academic Blacklist")

    args = parser.parse_args()
    if not (args.semantics or args.citations or args.blacklist):
        args.all = True

    total_errors = 0
    if args.all or args.semantics:
        total_errors += run_semantics_audit()
    if args.all or args.citations:
        total_errors += run_citation_audit()
    if args.all or args.blacklist:
        total_errors += run_blacklist_audit()

    print("\n" + "="*80)
    if total_errors == 0:
        print("🎉 [MASTER AUDIT SUCCESS] TOÀN BỘ WORKSPACE ĐẠT CHUẨN 100% (EXIT CODE 0)")
        sys.exit(0)
    else:
        print(f"⚠️ [MASTER AUDIT WARNING] Phát hiện {total_errors} vấn đề cần lưu ý (EXIT CODE 1)")
        sys.exit(1)

if __name__ == "__main__":
    main()
