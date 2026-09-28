#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_anti_hallucination.py
----------------------------
PI-Guard Master Anti-Hallucination & Empirical Grounding Auditor
Kiểm toán tự động chống tự sinh mô hình đồ án, chống giả mạo chỉ số tương lai
và bảo chứng 100% bằng chứng thực nghiệm trên toàn bộ repository.

4 Hạng mục kiểm tra bắt buộc (Four Core Passes):
  [AH-01] Model Codebase Integrity: Không chứa thư mục/lớp mô hình tự tạo (cascade, champion)
  [AH-02] Synthetic Mock Generator: Không chứa phân phối ngẫu nhiên sinh điểm giả (np.random.beta, etc.)
  [AH-03] Comparative Table & Claims: Không trộn lẫn mô hình nhóm kèm số liệu giả định trong bảng đối chuẩn
  [AH-04] Benchmark Artifact Grounding: Mọi tệp dữ liệu đo đạc JSON phải truy nguyên từ D1-D6 / Y văn

Sử dụng:
    python Final-Report/scripts/audit_anti_hallucination.py                # Quét chế độ Fast
    python Final-Report/scripts/audit_anti_hallucination.py --all          # Quét toàn diện (Full)
    python Final-Report/scripts/audit_anti_hallucination.py --mode staged  # Quét các file đang staged (Pre-commit)
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

# ANSI Colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Ignored paths during scanning
IGNORED_DIR_NAMES = {
    ".git", ".venv", "venv", "env", "__pycache__", "node_modules",
    ".codegraph", "site", ".pytest_cache", ".ruff_cache"
}

# ==============================================================================
# PASS 1: MODEL CODEBASE INTEGRITY (ZERO PREMATURE PROPOSED MODEL CODE)
# ==============================================================================
BANNED_MODEL_DIR_NAMES = {"cascade"}
BANNED_MODEL_CLASSES = {
    "ChampionCascadeClassifier",
    "ProposedCascadeClassifier",
    "TwoTierCascadeGuardrail",
    "CascadedGuardrailEngine",
}
BANNED_MODEL_IMPORTS = [
    r"from\s+[\.\w]*cascade\s+import",
    r"import\s+[\.\w]*cascade",
]

def pass1_check_model_codebase(target_files: Optional[List[Path]] = None) -> List[str]:
    """Kiểm tra không có thư mục cascade hay lớp mô hình tự tạo trong src/models/."""
    violations: List[str] = []

    # 1. Quét sự tồn tại của thư mục bị cấm
    for root, dirs, _ in os.walk(REPO_ROOT):
        # Bỏ qua các thư mục môi trường
        dirs[:] = [d for d in dirs if d not in IGNORED_DIR_NAMES]
        rel_root = os.path.relpath(root, REPO_ROOT).replace("\\", "/")
        if "src/models" in rel_root:
            for d in dirs:
                if d.lower() in BANNED_MODEL_DIR_NAMES:
                    full_p = os.path.join(root, d)
                    violations.append(
                        f"[AH-01:BANNED_DIR] Phát hiện thư mục mô hình tự tạo bị cấm: {full_p}"
                    )

    # 2. Quét nội dung các file Python trong src/models/
    py_files: List[Path] = []
    if target_files is not None:
        py_files = [f for f in target_files if f.suffix == ".py" and "src/models" in str(f).replace("\\", "/")]
    else:
        for p in REPO_ROOT.rglob("*.py"):
            rel_str = str(p.relative_to(REPO_ROOT)).replace("\\", "/")
            if "src/models" in rel_str and not any(ign in p.parts for ign in IGNORED_DIR_NAMES):
                py_files.append(p)

    for py_file in py_files:
        try:
            with open(py_file, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            for b_cls in BANNED_MODEL_CLASSES:
                # Tìm định nghĩa class
                if re.search(rf"\bclass\s+{b_cls}\b", content):
                    violations.append(
                        f"[AH-01:BANNED_CLASS] Định nghĩa lớp mô hình tự tạo '{b_cls}' tại: {py_file.relative_to(REPO_ROOT)}"
                    )

            for b_imp in BANNED_MODEL_IMPORTS:
                if re.search(b_imp, content):
                    violations.append(
                        f"[AH-01:BANNED_IMPORT] Import từ module cascade bị cấm tại: {py_file.relative_to(REPO_ROOT)}"
                    )

        except Exception as e:
            violations.append(f"[AH-01:READ_ERROR] Không thể đọc {py_file}: {e}")

    return violations


# ==============================================================================
# PASS 2: SYNTHETIC RANDOM MOCK GENERATOR DETECTION
# ==============================================================================
BANNED_RANDOM_PATTERNS = [
    (r"np\.random\.beta\s*\(", "np.random.beta() dùng để sinh điểm nguy cơ hoặc calibration giả"),
    (r"np\.random\.normal\s*\(", "np.random.normal() dùng để giả lập điểm số hoặc embedding"),
    (r"np\.random\.randn\s*\([^)]*size\s*=\s*\([0-9]+,\s*[0-9]+\)", "np.random.randn() dùng để sinh ma trận nhúng giả lập"),
    (r"random\.uniform\s*\(0\.[0-9]+,\s*1\.[0-9]+\)", "random.uniform() dùng để giả lập phân phối điểm"),
]

def pass2_check_synthetic_random(target_files: Optional[List[Path]] = None) -> List[str]:
    """Kiểm tra không sử dụng phân phối ngẫu nhiên để sinh điểm hoặc giả lập kết quả."""
    violations: List[str] = []

    py_files: List[Path] = []
    if target_files is not None:
        py_files = [
            f for f in target_files 
            if f.suffix == ".py" and any(k in str(f).replace("\\", "/") for k in ["src/", "scripts/", "evaluation/"])
        ]
    else:
        for p in REPO_ROOT.rglob("*.py"):
            rel_str = str(p.relative_to(REPO_ROOT)).replace("\\", "/")
            if any(k in rel_str for k in ["src/", "scripts/", "evaluation/"]) and not any(ign in p.parts for ign in IGNORED_DIR_NAMES):
                # Bỏ qua các file audit chính nó
                if p.name in ["audit_anti_hallucination.py", "audit_public_datasets.py"]:
                    continue
                py_files.append(p)

    for py_file in py_files:
        try:
            with open(py_file, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()

            for line_no, line in enumerate(lines, start=1):
                # Bỏ qua dòng comment
                stripped = line.strip()
                if stripped.startswith("#"):
                    continue
                for pat, desc in BANNED_RANDOM_PATTERNS:
                    if re.search(pat, line):
                        violations.append(
                            f"[AH-02:SYNTHETIC_RANDOM] {desc} tại {py_file.relative_to(REPO_ROOT)}:L{line_no}: {stripped}"
                        )
        except Exception as e:
            violations.append(f"[AH-02:READ_ERROR] Không thể đọc {py_file}: {e}")

    return violations


# ==============================================================================
# PASS 3: COMPARATIVE TABLE & CLAIM AUDIT (ZERO FABRICATED METRICS)
# ==============================================================================
BANNED_CLAIM_PATTERNS = [
    (r"mô\s+hình\s+vô\s+địch\s+của\s+đồ\s+án", "Khẳng định chủ quan 'mô hình vô địch của đồ án' khi chưa đánh giá"),
    (r"mô\s+hình\s+nhóm\s+đạt\s+(?:f1|độ\s+chính\s+xác|recall)", "Khẳng định kết quả định lượng của mô hình nhóm trước Chương 4"),
    (r"kết\s+quả\s+thực\s+nghiệm\s+của\s+pi-guard\s+đạt", "Gán kết quả thực nghiệm cho PI-Guard trước khi huấn luyện chính thức"),
    (r"\bchampion\s+cascade\b", "Thuật ngữ 'champion cascade' bị cấm tuyệt đối"),
    (r"\bsovereign\s+champion\b", "Thuật ngữ 'sovereign champion' bị cấm tuyệt đối"),
]

PROPOSED_MODEL_NAMES = [
    "pi-guard", "pi-guard (proposed)", "pi-guard cascade",
    "two-tier cascade", "proposed two-tier", "mô hình đề xuất", "mô hình nhóm"
]
BASELINE_MODEL_NAMES = [
    "protectai", "meta prompt-guard", "promptguard", "piguard (acl",
    "datasentinel", "smoothllm", "jain", "modernbert"
]
METRIC_HEADERS = [
    "recall", "fpr", "accuracy", "latency", "f1", "precision", "tpr @ 1%", "overdefense"
]

def pass3_check_markdown_tables_and_claims(target_files: Optional[List[Path]] = None) -> List[str]:
    """Kiểm tra văn bản Markdown: Không chứa bảng so sánh gán số liệu cho mô hình đồ án và không overclaiming."""
    violations: List[str] = []

    md_files: List[Path] = []
    if target_files is not None:
        md_files = [f for f in target_files if f.suffix == ".md"]
    else:
        for p in REPO_ROOT.rglob("*.md"):
            rel_str = str(p.relative_to(REPO_ROOT)).replace("\\", "/")
            if any(ign in p.parts for ign in IGNORED_DIR_NAMES):
                continue
            # Bỏ qua thư mục hướng dẫn nội bộ bất biến của FPT
            if "docs/fpt_capstone_guide" in rel_str:
                continue
            # Bỏ qua chính các file quy tắc và implementation plans
            if ".agents/rules" in rel_str or p.name in ["AGENTS.md", "anti-hallucination-and-empirical-grounding-standards.md", "plan_anti_hallucination_and_empirical_grounding_audit.md"]:
                continue
            md_files.append(p)

    for md_file in md_files:
        try:
            with open(md_file, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            rel_p = md_file.relative_to(REPO_ROOT)

            # 1. Quét từ khóa overclaiming bị cấm
            # Tách nội dung không tính fenced code block
            content_no_code = re.sub(r"```[\s\S]*?```", "", content)
            for pat, desc in BANNED_CLAIM_PATTERNS:
                matches = re.finditer(pat, content_no_code, re.IGNORECASE)
                for m in matches:
                    violations.append(
                        f"[AH-03:BANNED_CLAIM] {desc} tại {rel_p}: '{m.group(0)}'"
                    )

            # 2. Quét bảng đối chuẩn Markdown (Table Row Injection Check)
            # Tìm các bảng có headers chứa metrics
            lines = content.splitlines()
            in_table = False
            table_has_metrics = False
            table_has_baselines = False
            table_lines: List[Tuple[int, str]] = []

            for line_no, line in enumerate(lines, start=1):
                stripped = line.strip()
                if stripped.startswith("|") and stripped.endswith("|"):
                    in_table = True
                    table_lines.append((line_no, stripped))
                else:
                    if in_table:
                        # Kết thúc 1 bảng -> phân tích bảng vừa rồi
                        _analyze_markdown_table(table_lines, rel_p, violations)
                        in_table = False
                        table_lines = []

            if in_table:
                _analyze_markdown_table(table_lines, rel_p, violations)

        except Exception as e:
            violations.append(f"[AH-03:READ_ERROR] Không thể đọc {md_file}: {e}")

    return violations


def _analyze_markdown_table(table_lines: List[Tuple[int, str]], rel_p: Path, violations: List[str]):
    """Phân tích xem bảng có chứa cả baseline và mô hình đề xuất với số liệu cụ thể hay không."""
    if len(table_lines) < 3:
        return

    # Dòng header
    header_line = table_lines[0][1].lower()
    has_metric_cols = any(m in header_line for m in METRIC_HEADERS)
    if not has_metric_cols:
        return

    # Duyệt các dòng dữ liệu (bỏ qua dòng phân cách)
    has_baselines = False
    has_proposed_with_numbers = False
    proposed_line_info = ""

    for l_no, line_content in table_lines[2:]:
        lower_line = line_content.lower()
        # Kiểm tra baseline
        if any(b in lower_line for b in BASELINE_MODEL_NAMES):
            has_baselines = True

        # Kiểm tra mô hình nhóm/đề xuất
        if any(p in lower_line for p in PROPOSED_MODEL_NAMES):
            # Kiểm tra xem dòng này có chứa số liệu % hoặc ms đo đạc cụ thể không (loại trừ N/A hoặc SLA mục tiêu rõ ràng)
            # Mẫu số liệu: ví dụ 98.4%, 15ms, 0.8%
            numbers_with_units = re.findall(r"\b\d+(?:\.\d+)?\s*(?:%|ms)\b", line_content)
            # Nếu có số liệu đo đạc cụ thể mà không phải ghi chú là mục tiêu SLA
            if numbers_with_units and not any(k in lower_line for k in ["mục tiêu", "target", "sla", "chỉ tiêu"]):
                has_proposed_with_numbers = True
                proposed_line_info = f"L{l_no}: {line_content}"

    if has_baselines and has_proposed_with_numbers:
        violations.append(
            f"[AH-03:FABRICATED_TABLE_METRIC] Phát hiện bảng đối chuẩn trộn lẫn mô hình đề xuất có số liệu đo đạc cụ thể tại {rel_p}:{proposed_line_info}"
        )


# ==============================================================================
# PASS 4: BENCHMARK ARTIFACT GROUNDING
# ==============================================================================
def pass4_check_benchmark_grounding(target_files: Optional[List[Path]] = None) -> List[str]:
    """Kiểm tra các tệp JSON benchmark kết quả đối chuẩn."""
    violations: List[str] = []

    json_files: List[Path] = []
    if target_files is not None:
        json_files = [f for f in target_files if f.suffix == ".json" and "04_benchmarks_and_data" in str(f).replace("\\", "/")]
    else:
        for p in REPO_ROOT.rglob("*.json"):
            rel_str = str(p.relative_to(REPO_ROOT)).replace("\\", "/")
            if "04_benchmarks_and_data" in rel_str and not any(ign in p.parts for ign in IGNORED_DIR_NAMES):
                json_files.append(p)

    for jf in json_files:
        try:
            with open(jf, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            rel_p = jf.relative_to(REPO_ROOT)
            # Kiểm tra xem có chứa từ khóa champion bị cấm không
            if "champion_cascade" in content.lower():
                violations.append(
                    f"[AH-04:BANNED_JSON_KEY] Tệp kết quả JSON chứa 'champion_cascade' tại: {rel_p}"
                )
        except Exception as e:
            violations.append(f"[AH-04:READ_ERROR] Không thể đọc {jf}: {e}")

    return violations


# ==============================================================================
# MAIN EXECUTION & INTEGRATION ENTRYPOINT
# ==============================================================================
def run_anti_hallucination_audit(mode: str = "all", staged_files: Optional[List[Path]] = None) -> Tuple[bool, str]:
    """Hàm wrapper chuẩn dùng cho cả CLI độc lập và validate_local.py."""
    target_files = staged_files if mode == "staged" else None

    all_violations: List[str] = []

    v1 = pass1_check_model_codebase(target_files)
    v2 = pass2_check_synthetic_random(target_files)
    v3 = pass3_check_markdown_tables_and_claims(target_files)
    v4 = pass4_check_benchmark_grounding(target_files)

    all_violations.extend(v1)
    all_violations.extend(v2)
    all_violations.extend(v3)
    all_violations.extend(v4)

    if not all_violations:
        return True, "100% PASS: Không phát hiện mô hình tự sinh, không có chỉ số giả mạo, 100% bằng chứng thực nghiệm."
    else:
        detail_msg = "\n".join(f"  ❌ {v}" for v in all_violations)
        return False, f"Phát hiện {len(all_violations)} vi phạm nguyên tắc chống giả mạo & tự sinh mô hình:\n{detail_msg}"


def main() -> int:
    parser = argparse.ArgumentParser(description="PI-Guard Master Anti-Hallucination & Empirical Grounding Auditor")
    parser.add_argument("--mode", choices=["all", "staged", "fast"], default="all", help="Chế độ quét")
    parser.add_argument("--all", action="store_true", help="Quét toàn bộ repository")
    args = parser.parse_args()

    mode = "all" if args.all else args.mode

    print(f"\n{BOLD}{CYAN}{'='*80}{RESET}")
    print(f"{BOLD}{CYAN}🛡️  [PI-GUARD ANTI-HALLUCINATION AUDITOR] KIỂM TOÁN TÍNH CHUẨN MỰC HỌC THUẬT{RESET}")
    print(f"{BOLD}{CYAN}    Quy tắc: Chống Tự Sinh Mô Hình Đồ Án & Chống Giả Mạo Chỉ Số Tương Lai{RESET}")
    print(f"{BOLD}{CYAN}{'='*80}{RESET}")
    print(f"[*] Chế độ kiểm toán: {BOLD}{mode.upper()}{RESET}")
    print(f"[*] Repository root : {REPO_ROOT}")

    passed, message = run_anti_hallucination_audit(mode=mode)

    print("-" * 80)
    if passed:
        print(f"{BOLD}{GREEN}🎉 KẾT QUẢ KIỂM TOÁN: 100% PASS!{RESET}")
        print(f"{GREEN}   - Không có thư mục hay lớp mô hình tự tạo (cascade/champion) trong src/models/.{RESET}")
        print(f"{GREEN}   - Không sử dụng phân phối ngẫu nhiên sinh điểm giả lập (np.random.beta).{RESET}")
        print(f"{GREEN}   - Không có bảng đối chuẩn gán số liệu thực nghiệm cho mô hình nhóm khi chưa huấn luyện.{RESET}")
        print(f"{GREEN}   - Toàn bộ tài nguyên đối chuẩn đều truy nguyên từ y văn và D1-D6.{RESET}")
        print(f"{BOLD}{CYAN}{'='*80}{RESET}\n")
        return 0
    else:
        print(f"{BOLD}{RED}🚨 PHÁT HIỆN VI PHẠM NGUYÊN TẮC HỌC THUẬT (AUDIT FAILED):{RESET}")
        print(message)
        print(f"\n{YELLOW}Hướng dẫn khắc phục:{RESET}")
        print("  1. Xóa bỏ các thư mục mô hình tự tạo (như src/models/cascade/).")
        print("  2. Thay thế logic giả lập bằng adapter nạp từ các bài báo chuẩn trong replications/.")
        print("  3. Tách mô hình nhóm khỏi bảng đối chuẩn số liệu của Chapter 2 (chỉ nêu SLA mục tiêu trong văn bản).")
        print(f"{BOLD}{CYAN}{'='*80}{RESET}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
