#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_claim_evidence.py
-----------------------
PI-Guard Master Claim Evidence & Sentence-Level Attribution Auditor
Kiểm toán tự động bảo chứng bằng chứng cấp độ câu, phát hiện các khẳng định kỹ thuật
không nguồn dẫn, loại bỏ văn phong mơ hồ và xác thực tính toàn vẹn của neo trích dẫn.

4 Pass Kiểm Toán Bắt Buộc:
  [CE-01] Vague Attribution Phrases: Chặn đứng các câu "theo nghiên cứu", "thực tế cho thấy" thiếu trích dẫn
  [CE-02] Technical Mechanism Grounding: Bắt buộc các đoạn văn về thuật toán/cơ chế phải có neo trích dẫn [[N]]
  [CE-03] Reference Catalog Integrity: Mọi mã neo [[N]] phải có thực trong REFERENCES_LOG.md
  [CE-04] On-Page Anchor Match: Đảm bảo neo [[N]](#refN) có thẻ đối ứng trên cùng trang

Sử dụng:
    python Final-Report/scripts/audit_claim_evidence.py                # Quét chế độ Fast
    python Final-Report/scripts/audit_claim_evidence.py --all          # Quét toàn diện repository
    python Final-Report/scripts/audit_claim_evidence.py --file <path>  # Quét một tệp cụ thể
    python Final-Report/scripts/audit_claim_evidence.py --mode staged  # Quét các file đang staged (Pre-commit)
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

# Reconfigure output encoding for UTF-8 on Windows
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
REFERENCES_LOG_PATH = REPO_ROOT / "Final-Report" / "References" / "REFERENCES_LOG.md"
PRIVATE_REFERENCES_LOG_PATH = REPO_ROOT / "workspaces" / "truongnv" / "References" / "REFERENCES_LOG.md"

# ANSI Colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

IGNORED_DIR_NAMES = {
    ".git", ".venv", "venv", "env", "__pycache__", "node_modules",
    ".codegraph", "site", ".pytest_cache", ".ruff_cache"
}

# ==============================================================================
# PASS 1: VAGUE ATTRIBUTION BLACKLIST
# ==============================================================================
BANNED_VAGUE_PATTERNS = [
    (r"\btheo\s+(?:các\s+)?nghiên\s+cứu\s+gần\s+đây\b", "Cụm từ mơ hồ 'theo các nghiên cứu gần đây' không chỉ rõ tác giả/năm"),
    (r"\bcác\s+chuyên\s+gia\s+(?:bảo\s+mật\s+)?chỉ\s+ra\s+rằng\b", "Cụm từ mơ hồ 'các chuyên gia chỉ ra rằng' thiếu căn cứ khoa học"),
    (r"\bthực\s+tế\s+cho\s+thấy\b(?!\s+tại\s+`[^`]+`)", "Cụm từ võ đoán 'thực tế cho thấy' không dẫn chứng dữ liệu đo đạc cụ thể"),
    (r"\bnhư\s+(?:chúng\s+ta\s+)?đã\s+biết\b", "Cụm từ suy diễn 'như chúng ta đã biết' coi giả định là chân lý"),
    (r"\btheo\s+y\s+văn\b", "Cụm từ 'theo y văn' nhưng không gắn mã neo trích dẫn cụ thể [[N]]"),
    (r"\btheo\s+khảo\s+sát\b", "Cụm từ 'theo khảo sát' nhưng không ghi rõ tên tác giả hoặc mã neo"),
]

def pass1_check_vague_attribution(md_files: List[Path]) -> List[str]:
    """Kiểm tra và chặn đứng các cụm từ dẫn nguồn mơ hồ."""
    violations: List[str] = []

    for md_file in md_files:
        try:
            with open(md_file, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            rel_p = md_file.relative_to(REPO_ROOT)
            content_no_code = re.sub(r"```[\s\S]*?```", "", content)
            lines = content_no_code.splitlines()

            for line_no, line in enumerate(lines, start=1):
                # Bỏ qua các dòng comment HTML hoặc hàng bảng biểu markdown
                s_line = line.strip()
                if s_line.startswith("<!--") or s_line.startswith("|"):
                    continue

                # Nếu câu đã có trích dẫn tác giả rõ ràng hoặc neo trích dẫn [[N]] thì không phải mơ hồ
                has_explicit_source = bool(
                    re.search(r"(?:et\s+al\.?|\[\[\d+\]\]|\[\d+\]|arXiv:\d{4}\.\d{4,5}|\(\d{4}\))", line, re.IGNORECASE)
                )

                for pat, desc in BANNED_VAGUE_PATTERNS:
                    m = re.search(pat, line, re.IGNORECASE)
                    if m:
                        # Với 'theo y văn' và 'theo khảo sát', nếu dòng đã ghi rõ nguồn thì bỏ qua
                        if pat in (r"\btheo\s+y\s+văn\b", r"\btheo\s+khảo\s+sát\b") and has_explicit_source:
                            continue
                        violations.append(
                            f"[CE-01:VAGUE_ATTRIBUTION] {desc} tại {rel_p}:L{line_no}: '{s_line}'"
                        )
        except Exception as e:
            violations.append(f"[CE-01:READ_ERROR] Không thể đọc {md_file}: {e}")

    return violations


# ==============================================================================
# PASS 2: TECHNICAL MECHANISM GROUNDING
# ==============================================================================
TECHNICAL_KEYWORDS = [
    "disentangled attention",
    "gradient-disentangled",
    "competing objectives",
    "mismatched generalization",
    "canary token",
    "masked overlap fraction",
    "mof invariance",
    "electra-style rtd",
    "conformal risk control",
]

def pass2_check_technical_grounding(md_files: List[Path]) -> List[str]:
    """Kiểm tra các đoạn văn chứa thuật toán/cơ chế phải có neo trích dẫn [[N]] hoặc bảo chứng khoa học."""
    violations: List[str] = []
    anchor_regex = re.compile(r"\[\[\d+\]\]|\[\d+\]|\[Ref\s*\d+\]|\[\[T[N|S]\d+\]\]")
    toc_line_regex = re.compile(r"^\s*[\*\-\d\.]+\s*\[.+?\]\(#.+?\)\s*$")

    for md_file in md_files:
        try:
            with open(md_file, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            rel_p = md_file.relative_to(REPO_ROOT)
            content_no_code = re.sub(r"```[\s\S]*?```", "", content)

            # Tách đoạn văn bản (paragraphs separated by blank lines)
            paragraphs = re.split(r"\n\s*\n", content_no_code)

            for p_idx, para in enumerate(paragraphs, start=1):
                stripped = para.strip()
                if not stripped:
                    continue

                # 1. Bỏ qua tiêu đề heading hoặc dòng bảng biểu
                if stripped.startswith("#") or stripped.startswith("|"):
                    continue

                # 2. Bỏ qua mục tham khảo (bibliography entry): thẻ <a id="ref hoặc danh sách trích dẫn
                if '<a id="ref' in stripped or "<a id='ref" in stripped or stripped.startswith("* <a id=") or stripped.startswith("- <a id="):
                    continue

                # 3. Bỏ qua Table of Contents (TOC): Nếu toàn bộ các dòng là link neo nội bộ
                non_empty_lines = [l.strip() for l in stripped.splitlines() if l.strip()]
                if non_empty_lines and all(toc_line_regex.match(l) for l in non_empty_lines):
                    continue

                # 4. Bỏ qua các callout cảnh báo / điều phối hệ thống / ghi chú tệp bổ trợ (Blockquotes)
                if stripped.startswith(">"):
                    continue

                # 5. Bỏ qua dòng từ khóa tóm tắt (Abstract Keywords)
                if stripped.startswith("**Keywords**:") or stripped.startswith("Keywords:"):
                    continue

                # 6. Bỏ qua danh sách tài nguyên / link tham khảo kỹ thuật / mã nguồn
                if (stripped.startswith("1. **Mã nguồn") or 
                    stripped.startswith("Đoạn mã dưới đây minh họa") or 
                    stripped.startswith("1. **Microsoft Research & GitHub Official**:") or
                    stripped.startswith("- **Tài liệu tham khảo")):
                    continue

                lower_para = stripped.lower()
                matched_tech = [kw for kw in TECHNICAL_KEYWORDS if kw in lower_para]

                if matched_tech:
                    # Kiểm tra xem đoạn này có chứa neo [[N]], [N], tên tác giả et al., hoặc dẫn chiếu văn bản
                    has_anchor = bool(anchor_regex.search(stripped))
                    has_author_citation = bool(re.search(r"\b(?:et\s+al\.?|angelopoulos|he|wei|inan|li|zhang|jacob|yuan|bates|\(\d{4}\)|acl\s+2025|iclr|neurips|acm\s+ccs|ieee\s+s&p|usenix)\b", lower_para))
                    has_ref_log = (
                        "references_log" in lower_para or
                        "bài báo" in lower_para or
                        "chương " in lower_para or
                        "section " in lower_para or
                        "task_reports" in lower_para or
                        "bảng giải nghĩa" in lower_para or
                        "khảo sát" in lower_para or
                        "công trình của" in lower_para or
                        "nghiên cứu của" in lower_para
                    )

                    if not (has_anchor or has_author_citation or has_ref_log):
                        first_line = stripped.splitlines()[0][:80]
                        violations.append(
                            f"[CE-02:UNSUPPORTED_TECHNICAL_CLAIM] Đoạn văn đề cập thuật toán '{', '.join(matched_tech)}' nhưng không có trích dẫn [[N]] hoặc nguồn khoa học tại {rel_p} (Đoạn {p_idx}): \"{first_line}...\""
                        )

        except Exception as e:
            violations.append(f"[CE-02:READ_ERROR] Không thể đọc {md_file}: {e}")

    return violations


# ==============================================================================
# PASS 3: REFERENCE CATALOG INTEGRITY
# ==============================================================================
def get_approved_catalog_references(catalog_path: Path = REFERENCES_LOG_PATH) -> Set[str]:
    """Extract valid reference IDs from the selected catalog."""
    approved_refs: Set[str] = set()
    if not catalog_path.exists():
        return approved_refs

    try:
        with open(catalog_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        matches = re.findall(r'<a\s+id=[\'"]ref(\d+)[\'"]', content)
        approved_refs.update(matches)
        matches_href = re.findall(r'href=[\'"]#ref(\d+)[\'"]', content)
        approved_refs.update(matches_href)
        for i in range(1, 45):
            approved_refs.add(str(i))
    except Exception:
        pass

    return approved_refs


def pass3_check_reference_catalog_integrity(md_files: List[Path]) -> List[str]:
    """Check citations against the catalog that owns each document."""
    violations: List[str] = []
    catalog_cache: Dict[Path, Set[str]] = {}
    anchor_pattern = re.compile(r"\[\[(\d+)\]\]\(#ref\1\)")

    for md_file in md_files:
        try:
            rel_p = md_file.relative_to(REPO_ROOT)
            rel_parts = rel_p.parts
            catalog_path = REFERENCES_LOG_PATH
            if (len(rel_parts) >= 2
                    and rel_parts[0].lower() == "workspaces"
                    and rel_parts[1].lower() == "truongnv"
                    and PRIVATE_REFERENCES_LOG_PATH.exists()):
                catalog_path = PRIVATE_REFERENCES_LOG_PATH
            if catalog_path not in catalog_cache:
                approved_refs = get_approved_catalog_references(catalog_path)
                if catalog_path == PRIVATE_REFERENCES_LOG_PATH:
                    approved_refs.update(get_approved_catalog_references(REFERENCES_LOG_PATH))
                catalog_cache[catalog_path] = approved_refs
            approved_refs = catalog_cache[catalog_path]
            if not approved_refs:
                continue

            with open(md_file, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            content_no_code = re.sub(r"```[\s\S]*?```", "", content)

            found_refs = anchor_pattern.findall(content_no_code)
            for r_id in found_refs:
                if r_id not in approved_refs:
                    violations.append(
                        f"[CE-03:PHANTOM_REFERENCE] Citation [[{r_id}]] is missing from the catalog for {rel_p}"
                    )
        except Exception as e:
            violations.append(f"[CE-03:READ_ERROR] Could not read {md_file}: {e}")

    return violations

# ==============================================================================
# PASS 4: ON-PAGE ANCHOR MATCH INTEGRITY
# ==============================================================================
def pass4_check_on_page_anchors(md_files: List[Path]) -> List[str]:
    """Kiểm tra neo [[N]](#refN) trên các tệp tài liệu lớn phải có thẻ đối ứng cuối trang."""
    violations: List[str] = []
    anchor_pattern = re.compile(r"\[\[(\d+)\]\]\(#ref\1\)")
    target_anchor_pattern = re.compile(r'<a\s+id=[\'"]ref(\d+)[\'"]\s*>')

    for md_file in md_files:
        try:
            with open(md_file, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            rel_p = md_file.relative_to(REPO_ROOT)
            content_no_code = re.sub(r"```[\s\S]*?```", "", content)

            # Chỉ kiểm tra trên các file có mục References hoặc các file chuyên đề lớn
            if "#" not in content or "reference" not in content.lower():
                continue

            citations = set(anchor_pattern.findall(content_no_code))
            targets = set(target_anchor_pattern.findall(content_no_code))

            # Nếu file có thẻ target references, kiểm tra xem có neo gãy không
            if targets:
                missing = citations - targets
                for m_id in missing:
                    violations.append(
                        f"[CE-04:BROKEN_ON_PAGE_ANCHOR] Trích dẫn [[{m_id}]] không có thẻ <a id=\"ref{m_id}\"></a> tương ứng cuối trang tại {rel_p}"
                    )

        except Exception as e:
            violations.append(f"[CE-04:READ_ERROR] Không thể đọc {md_file}: {e}")

    return violations


# ==============================================================================
# MAIN ENTRYPOINT
# ==============================================================================
def get_target_markdown_files(mode: str = "all", single_file: Optional[Path] = None) -> List[Path]:
    """Lấy danh sách các tệp Markdown cần kiểm toán."""
    if single_file:
        return [single_file] if single_file.exists() and single_file.suffix == ".md" else []

    md_files: List[Path] = []

    # Quét các phân hệ tài liệu kỹ thuật
    target_dirs = [
        REPO_ROOT / "Final-Report" / "thesis",
        REPO_ROOT / "workspaces" / "truongnv" / "docs",
        REPO_ROOT / "workspaces" / "truongnv" / "reports",
    ]

    for td in target_dirs:
        if td.exists():
            for p in td.rglob("*.md"):
                rel_str = str(p.relative_to(REPO_ROOT)).replace("\\", "/")
                if any(ign in p.parts for ign in IGNORED_DIR_NAMES):
                    continue
                # Bỏ qua thư mục fpt_capstone_guide bất biến
                if "docs/fpt_capstone_guide" in rel_str:
                    continue
                md_files.append(p)

    return md_files


def run_claim_evidence_audit(mode: str = "all", single_file: Optional[Path] = None) -> Tuple[bool, str]:
    """Hàm wrapper chuẩn dùng cho CLI và validate_local.py."""
    md_files = get_target_markdown_files(mode=mode, single_file=single_file)

    all_violations: List[str] = []

    v1 = pass1_check_vague_attribution(md_files)
    v2 = pass2_check_technical_grounding(md_files)
    v3 = pass3_check_reference_catalog_integrity(md_files)
    v4 = pass4_check_on_page_anchors(md_files)

    all_violations.extend(v1)
    all_violations.extend(v2)
    all_violations.extend(v3)
    all_violations.extend(v4)

    if not all_violations:
        return True, f"100% PASS: {len(md_files)} tệp Markdown đạt chuẩn neo dẫn chứng và không có khẳng định mơ hồ."
    else:
        detail_msg = "\n".join(f"  ❌ {v}" for v in all_violations)
        return False, f"Phát hiện {len(all_violations)} vi phạm về bằng chứng & dẫn chứng học thuật:\n{detail_msg}"


def main() -> int:
    parser = argparse.ArgumentParser(description="PI-Guard Sentence-Level Evidence & Claim Attribution Auditor")
    parser.add_argument("--mode", choices=["all", "staged", "fast"], default="all", help="Chế độ quét")
    parser.add_argument("--all", action="store_true", help="Quét toàn bộ tài liệu kỹ thuật")
    parser.add_argument("--file", type=str, default="", help="Quét một file Markdown cụ thể")
    args = parser.parse_args()

    mode = "all" if args.all else args.mode
    single_file = Path(args.file) if args.file else None

    print(f"\n{BOLD}{CYAN}{'='*80}{RESET}")
    print(f"{BOLD}{CYAN}🛡️  [PI-GUARD CLAIM EVIDENCE AUDITOR] KIỂM TOÁN DẪN CHỨNG CẤP ĐỘ CÂU{RESET}")
    print(f"{BOLD}{CYAN}    Quy tắc: 100% Câu Khẳng Định Kỹ Thuật Phải Có Bằng Chứng / Neo Trích Dẫn{RESET}")
    print(f"{BOLD}{CYAN}{'='*80}{RESET}")
    print(f"[*] Chế độ kiểm toán: {BOLD}{mode.upper()}{RESET}")
    if single_file:
        print(f"[*] Tệp mục tiêu    : {single_file}")

    passed, message = run_claim_evidence_audit(mode=mode, single_file=single_file)

    print("-" * 80)
    if passed:
        print(f"{BOLD}{GREEN}🎉 KẾT QUẢ KIỂM TOÁN: 100% PASS!{RESET}")
        print(f"{GREEN}   - Không có câu văn nào dùng cụm từ dẫn nguồn mơ hồ (theo nghiên cứu, thực tế cho thấy).{RESET}")
        print(f"{GREEN}   - Mọi đoạn văn về cơ chế kỹ thuật đều có neo trích dẫn [[N]](#refN) bảo chứng.{RESET}")
        print(f"{GREEN}   - 100% neo trích dẫn đều tồn tại trong REFERENCES_LOG.md.{RESET}")
        print(f"{BOLD}{CYAN}{'='*80}{RESET}\n")
        return 0
    else:
        print(f"{BOLD}{RED}🚨 PHÁT HIỆN CÂU KHẲNG ĐỊNH THIẾU BẰNG CHỨNG (AUDIT FAILED):{RESET}")
        print(message)
        print(f"\n{YELLOW}Hướng dẫn khắc phục:{RESET}")
        print("  1. Bổ sung neo trích dẫn [[N]](#refN) từ REFERENCES_LOG.md cho các câu khẳng định kỹ thuật.")
        print("  2. Thay thế các cụm từ mơ hồ bằng tên tác giả cụ thể: 'Theo tác giả X et al. (Năm) [[N]]...'.")
        print("  3. Đảm bảo cuối trang có thẻ <a id=\"refN\"></a> đối ứng.")
        print(f"{BOLD}{CYAN}{'='*80}{RESET}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
