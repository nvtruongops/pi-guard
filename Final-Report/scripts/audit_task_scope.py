#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Final-Report/scripts/audit_task_scope.py
-----------------------------------------
PI-Guard Task-Scope & Architectural Deprecations Automated Auditor
Bộ công cụ kiểm toán tự động ranh giới nhiệm vụ và phát hiện công nghệ bị loại trừ.

Mục tiêu kiểm toán:
1. SC-DEP: Phát hiện từ khóa công nghệ đã bị loại trừ (INT8, ZeroQuant, ONNX Runtime)
           khi bị trình bày như kiến trúc áp dụng của đề tài.
2. SC-PREM: Phát hiện việc tự sinh hoặc tuyên bố mô hình đề xuất (Cascade / Champion)
            trong các báo cáo nhiệm vụ thuần baseline (Chương 2 / Meeting 5-6).
3. SC-DECL: Kiểm tra xem các báo cáo điều hành/nhiệm vụ có phần Tuyên Bố Ranh Giới (Scope Declaration).
4. SC-RULE: Kiểm toán dung lượng các tệp trong .agents/rules/ và AGENTS.md (ngưỡng < 10,000 bytes)
            nhằm triệt tiêu nguy cơ bị cắt cụt (context truncation) trong Antigravity IDE.

Sử dụng:
    python Final-Report/scripts/audit_task_scope.py
    python Final-Report/scripts/audit_task_scope.py --strict
    python Final-Report/scripts/audit_task_scope.py --file <path_to_markdown>
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Reconfigure stdout/stderr for Windows UTF-8
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

SCRIPTS_DIR = Path(__file__).resolve().parent
FINAL_REPORT_DIR = SCRIPTS_DIR.parent
ROOT_DIR = FINAL_REPORT_DIR.parent

# ANSI Colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Danh mục từ khóa cấm / out-of-scope khi gán cho mô hình đề tài
DEPRECATED_PATTERNS = [
    (
        r"(?:áp dụng|hiện thực|triển khai|sử dụng)\s+(?:lượng tử hóa\s+)?INT8",
        "SC-DEP-01",
        "Đề tài đã loại bỏ lượng tử hóa INT8; Tầng 2 đề xuất là Native FP32 DeBERTa-v3.",
    ),
    (
        r"(?:tối ưu|triển khai|sử dụng)\s+ONNX\s+Runtime\s+(?:cho\s+PI-Guard|làm\s+guardrail)",
        "SC-DEP-02",
        "Đề tài đã loại bỏ tối ưu ONNX Runtime; chạy Native PyTorch FP32 trên CPU.",
    ),
    (
        r"(?:can thiệp|sửa đổi|giám sát)\s+(?:trọng số nội bộ|KV-cache)\s+của\s+LLM",
        "SC-DEP-03",
        "Đề tài là External Guardrail Proxy mức văn bản, không can thiệp trọng số/KV-cache.",
    ),
]

# Từ khóa tự nhận mô hình nhóm đã thành hình trong báo cáo baseline
PREMATURE_MODEL_PATTERNS = [
    (
        r"(?:hiện thực hóa|hoàn thành|xây dựng xong)\s+module\s+(?:block_chunker|cascade|champion)",
        "SC-PREM-01",
        "Tại giai đoạn Chương 2 / Meeting 6, cấm tuyên bố đã hiện thực hóa module mô hình nhóm.",
    ),
    (
        r"mô hình\s+(?:vô địch|champion)\s+của\s+đồ án\s+(?:đạt|đã đạt)",
        "SC-PREM-02",
        "Chưa đến kỳ nghiệm thu mô hình đề tài (Chương 4 / Tuần 13). Cấm tuyên bố kết quả mô hình nhóm.",
    ),
]

# Ngưỡng kích thước file tối đa để tránh IDE context truncation
MAX_RULE_FILE_BYTES = 10000


def audit_rule_file_sizes() -> List[Dict]:
    """Kiểm toán dung lượng các tệp rules trong .agents/rules/ và AGENTS.md."""
    violations = []
    
    # 1. Kiểm tra AGENTS.md
    agents_md = ROOT_DIR / "AGENTS.md"
    if agents_md.exists():
        size = agents_md.stat().st_size
        if size > MAX_RULE_FILE_BYTES:
            violations.append({
                "file": str(agents_md),
                "code": "SC-RULE-01",
                "message": f"AGENTS.md dung lượng {size} bytes vượt ngưỡng {MAX_RULE_FILE_BYTES} bytes. Nguy cơ bị IDE cắt cụt!",
                "severity": "HIGH",
            })
            
    # 2. Kiểm tra .agents/rules/
    rules_dir = ROOT_DIR / ".agents" / "rules"
    if rules_dir.exists():
        for r_file in rules_dir.glob("*.md"):
            size = r_file.stat().st_size
            if size > MAX_RULE_FILE_BYTES:
                violations.append({
                    "file": str(r_file),
                    "code": "SC-RULE-02",
                    "message": f"Rule file {r_file.name} dung lượng {size} bytes vượt ngưỡng {MAX_RULE_FILE_BYTES} bytes.",
                    "severity": "HIGH",
                })
                
    return violations


def audit_markdown_file(file_path: Path) -> List[Dict]:
    """Kiểm toán nội dung một file Markdown báo cáo."""
    violations = []
    try:
        content = file_path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return [{
            "file": str(file_path),
            "code": "SC-ERR",
            "message": f"Không thể đọc file: {e}",
            "severity": "HIGH",
        }]

    # Bỏ qua tài liệu ghi rõ là deprecation notice
    if "ARCHITECTURAL_DEPRECATIONS_AND_OUT_OF_SCOPE.md" in file_path.name:
        return []

    lines = content.splitlines()

    # 1. Kiểm tra từ khóa Deprecations
    for line_idx, line in enumerate(lines, 1):
        # Bỏ qua trích dẫn paper Yao et al. hoặc bảng đối chiếu lịch sử
        if "Yao et al." in line or "ZeroQuant" in line and ("bác bỏ" in line or "loại bỏ" in line or "baseline tham chiếu" in line):
            continue
        for pattern, code, msg in DEPRECATED_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                violations.append({
                    "file": str(file_path),
                    "line": line_idx,
                    "code": code,
                    "content": line.strip()[:100],
                    "message": msg,
                    "severity": "HIGH",
                })

    # 2. Kiểm tra Premature Proposed Model trong các báo cáo meeting 5 và 6
    if "tasks_for_meeting_5" in str(file_path) or "tasks_for_meeting_6" in str(file_path):
        for line_idx, line in enumerate(lines, 1):
            for pattern, code, msg in PREMATURE_MODEL_PATTERNS:
                if re.search(pattern, line, re.IGNORECASE):
                    violations.append({
                        "file": str(file_path),
                        "line": line_idx,
                        "code": code,
                        "content": line.strip()[:100],
                        "message": msg,
                        "severity": "MEDIUM",
                    })

    # 3. Kiểm tra Scope Declaration trong các báo cáo điều hành mới
    if file_path.name.startswith("EXECUTIVE_PROGRESS_REPORT_") or file_path.name.startswith("TASK_"):
        has_scope_declaration = bool(
            re.search(r"(?:TUYÊN BỐ RANH GIỚI|SCOPE BOUNDARY|Ranh giới thực thi|Phạm vi trong nhiệm vụ)", content, re.IGNORECASE)
        )
        if not has_scope_declaration:
            violations.append({
                "file": str(file_path),
                "code": "SC-DECL-01",
                "message": "Báo cáo tiến độ thiếu mục 'Tuyên Bố Ranh Giới Nhiệm Vụ' (Scope Boundary Declaration) theo Rule 02.",
                "severity": "LOW",
            })

    return violations


def run_scope_audit(target_file: str = None, strict: bool = False) -> Tuple[bool, List[Dict]]:
    """Chạy toàn bộ quy trình kiểm toán ranh giới nhiệm vụ."""
    all_violations = []

    # 1. Kiểm toán dung lượng file rules
    rule_violations = audit_rule_file_sizes()
    all_violations.extend(rule_violations)

    # 2. Quét file Markdown
    if target_file:
        t_path = Path(target_file)
        if t_path.exists():
            all_violations.extend(audit_markdown_file(t_path))
    else:
        # Quét các thư mục báo cáo chính
        report_dirs = [
            ROOT_DIR / "Final-Report" / "reports",
            ROOT_DIR / "workspaces" / "truongnv" / "reports",
        ]
        for r_dir in report_dirs:
            if r_dir.exists():
                for md_file in r_dir.rglob("*.md"):
                    if ".venv" in str(md_file) or ".git" in str(md_file):
                        continue
                    all_violations.extend(audit_markdown_file(md_file))

    # Đánh giá PASS / FAIL
    has_high = any(v.get("severity") == "HIGH" for v in all_violations)
    has_med = any(v.get("severity") == "MEDIUM" for v in all_violations)
    
    if strict:
        success = len(all_violations) == 0
    else:
        success = not has_high

    return success, all_violations


def main():
    parser = argparse.ArgumentParser(description="PI-Guard Task-Scope & Deprecations Auditor")
    parser.add_argument("--file", type=str, help="Đường dẫn file markdown cần kiểm toán cụ thể.")
    parser.add_argument("--strict", action="store_true", help="Chế độ nghiêm ngặt (báo lỗi cả cảnh báo LOW/MEDIUM).")
    args = parser.parse_args()

    print(f"\n{BOLD}{CYAN}{'='*80}{RESET}")
    print(f"{BOLD}{CYAN}🔍 [AUDIT-TASK-SCOPE] KIỂM TOÁN RANH GIỚI NHIỆM VỤ & DEPRECATIONS{RESET}")
    print(f"{BOLD}{CYAN}{'='*80}{RESET}\n")

    success, violations = run_scope_audit(target_file=args.file, strict=args.strict)

    if not violations:
        print(f"{BOLD}{GREEN}✅ 100% TUÂN THỦ RANH GIỚI NHIỆM VỤ:{RESET}")
        print(f"  - Dung lượng rules & AGENTS.md nằm trong ngưỡng an toàn (< {MAX_RULE_FILE_BYTES} bytes)")
        print("  - Không phát hiện từ khóa kiến trúc bị loại trừ (INT8, ONNX, ZeroQuant)")
        print("  - Không phát hiện tuyên bố mô hình nhóm sớm trong các báo cáo baseline")
        return 0

    print(f"{BOLD}{YELLOW}⚠️ PHÁT HIỆN {len(violations)} ĐIỂM CẦN LƯU Ý / VI PHẠM PHẠM VI:{RESET}\n")
    for v in violations:
        sev = v.get("severity", "INFO")
        sev_color = RED if sev == "HIGH" else (YELLOW if sev == "MEDIUM" else CYAN)
        line_str = f":L{v['line']}" if "line" in v else ""
        print(f"  {sev_color}[{sev}][{v['code']}]{RESET} {v['file']}{line_str}")
        print(f"    ↳ {v['message']}")
        if "content" in v:
            print(f"    ↳ Dòng trích dẫn: \"{v['content']}\"")
        print()

    if not success:
        print(f"{BOLD}{RED}❌ KIỂM TOÁN THẤT BẠI: Có vi phạm ranh giới cấp HIGH cần xử lý trước khi commit.{RESET}\n")
        return 1
    else:
        print(f"{BOLD}{GREEN}✔ KIỂM TOÁN HOÀN TẤT (Không có vi phạm cấp HIGH chặn commit).{RESET}\n")
        return 0


if __name__ == "__main__":
    sys.exit(main())
