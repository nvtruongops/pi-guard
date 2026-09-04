#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/validate_local.py
-------------------------
PI-Guard Unified Local Quality Assurance & Validation Suite
Bộ công cụ kiểm định chất lượng, an toàn mã nguồn và tài liệu nội bộ thuần Local.

Thay thế hoàn toàn GitHub Actions CI/CD bằng quy trình kiểm thử cục bộ:
1. Workspace Boundaries & Immutable Invariant Audit (Kiểm toán phân quyền & file bất biến)
2. JSON Manifests Schema & Syntax Validation (Kiểm định tệp manifest dữ liệu)
3. Code Quality & Linting (Ruff linting trên src/ và tests/)
4. Automated Test Suite (Pytest: unit, integration, adversarial)
5. Adversarial Benchmark Smoke Test (Benchmark độ trễ P50/P95/P99)
6. Documentation Portal Aggregation & Static Site Build (MkDocs Material)
7. Git Pre-commit Hook Integration (Tự động cài đặt và chặn commit vi phạm)

Sử dụng:
    python scripts/validate_local.py                # Chế độ Fast (mặc định: boundaries + manifests + lint + benchmark)
    python scripts/validate_local.py --mode pre-commit # Chế độ Pre-commit (chạy siêu tốc cho staged files)
    python scripts/validate_local.py --all          # Chế độ Full (chạy 100% tất cả các khâu kiểm thử và build docs)
    python scripts/validate_local.py --install-hook # Cài đặt / cập nhật Git Pre-commit Hook
"""

import argparse
import glob
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Reconfigure standard output for UTF-8 on Windows
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

ROOT_DIR = Path(__file__).resolve().parent.parent

# ANSI Colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Danh mục file & folder bất biến tuyệt đối
STRICT_IMMUTABLE_PATHS = [
    "CAPSTONE PROJECT REGISTER.md",
    "docs/fpt_capstone_guide/",
]


def log_header(title: str):
    print(f"\n{BOLD}{CYAN}{'='*80}{RESET}")
    print(f"{BOLD}{CYAN}🚀 [LOCAL-QA] {title.upper()}{RESET}")
    print(f"{BOLD}{CYAN}{'='*80}{RESET}")


def run_cmd(
    cmd: List[str], cwd: Optional[Path] = None, timeout: int = 120
) -> Tuple[int, str, str]:
    """Chạy lệnh subprocess an toàn và trả về (exit_code, stdout, stderr)."""
    try:
        res = subprocess.run(
            cmd,
            cwd=str(cwd or ROOT_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
        return res.returncode, res.stdout.strip(), res.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", f"Command timed out after {timeout} seconds."
    except Exception as e:
        return -1, "", str(e)


# ==============================================================================
# 1. KIỂM TOÁN PHÂN QUYỀN WORKSPACE & FILE BẤT BIẾN
# ==============================================================================
def step_workspace_boundary_audit(mode: str = "staged") -> Tuple[bool, str]:
    """Kiểm toán ranh giới workspace và phân quyền commit qua audit_workspace_boundaries.py."""
    audit_script = ROOT_DIR / "scripts" / "audit_workspace_boundaries.py"
    if not audit_script.exists():
        return False, "Không tìm thấy scripts/audit_workspace_boundaries.py"

    code, out, err = run_cmd([sys.executable, str(audit_script), "--mode", mode])
    output = out if out else err
    if code == 0:
        return True, "Workspace boundaries and immutable invariants verified successfully."
    else:
        return False, output


# ==============================================================================
# 2. KIỂM TRA TÍNH TOÀN VẸN CỦA JSON MANIFESTS
# ==============================================================================
def step_validate_manifests(staged_only: bool = False) -> Tuple[bool, str]:
    """Kiểm tra tính hợp lệ cú pháp của tất cả các file JSON manifest trong data/ và workspaces/."""
    manifest_files: List[Path] = []

    if staged_only:
        code, out, _ = run_cmd(["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"])
        if code == 0 and out:
            for line in out.splitlines():
                line = line.strip().strip('"').replace("\\", "/")
                if line.endswith(".json") and ("manifests" in line or "data/" in line):
                    p = ROOT_DIR / line
                    if p.exists():
                        manifest_files.append(p)
    else:
        root_manifests = glob.glob(str(ROOT_DIR / "data" / "manifests" / "*.json"))
        ws_manifests = glob.glob(str(ROOT_DIR / "workspaces" / "*" / "data" / "manifests" / "*.json"))
        manifest_files = [Path(f) for f in root_manifests + ws_manifests]

    if not manifest_files:
        msg = "No JSON manifests to validate in this changeset. Skipped."
        return True, msg

    valid_count = 0
    errors: List[str] = []

    for mf in manifest_files:
        try:
            with open(mf, "r", encoding="utf-8") as fp:
                data = json.load(fp)
            if not isinstance(data, (dict, list)):
                errors.append(f"{mf.relative_to(ROOT_DIR)}: Root element must be JSON object or array.")
            else:
                valid_count += 1
        except Exception as e:
            errors.append(f"{mf.relative_to(ROOT_DIR)}: JSON Parse Error: {e}")

    if errors:
        return False, "\n".join(errors)
    return True, f"Validated {valid_count} JSON manifest(s) successfully."


# ==============================================================================
# 3. CODE QUALITY & LINTING (RUFF / AST SYNTAX)
# ==============================================================================
def step_code_linting(staged_only: bool = False) -> tuple[bool, str]:
    """Chạy linter Ruff hoặc kiểm tra cú pháp Python AST trên src/ và tests/."""
    has_ruff = shutil.which("ruff") is not None
    if not has_ruff:
        try:
            import ruff  # noqa: F401
            has_ruff = True
        except ImportError:
            has_ruff = False

    if has_ruff:
        if staged_only:
            code, out, _ = run_cmd(["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"])
            py_files: list[str] = []
            if code == 0 and out:
                for line in out.splitlines():
                    line = line.strip().strip('"').replace("\\", "/")
                    if line.endswith(".py") and line.startswith(("src/", "tests/")):
                        p = ROOT_DIR / line
                        if p.exists():
                            py_files.append(str(p))
            if not py_files:
                return True, "No staged Python files in src/ or tests/ to lint."
            code, out, err = run_cmd(["ruff", "check"] + py_files)
        else:
            targets = []
            for t in ["src", "tests"]:
                if (ROOT_DIR / t).exists():
                    targets.append(t)
            code, out, err = run_cmd(["ruff", "check"] + targets)

        if code == 0:
            return True, "Ruff linting passed cleanly with 0 errors."
        else:
            return False, out or err
    else:
        # Fallback: Python AST Compile Check
        py_files_ast: list[Path] = []
        if staged_only:
            code, out, _ = run_cmd(["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"])
            if code == 0 and out:
                for line in out.splitlines():
                    line = line.strip().strip('"').replace("\\", "/")
                    if line.endswith(".py") and line.startswith(("src/", "tests/")):
                        p = ROOT_DIR / line
                        if p.exists():
                            py_files_ast.append(p)
        else:
            for t in ["src", "tests"]:
                py_files_ast.extend(list((ROOT_DIR / t).rglob("*.py")))

        errors = []
        for pf in py_files_ast:
            try:
                with open(pf, encoding="utf-8") as f:
                    compile(f.read(), str(pf), "exec")
            except SyntaxError as e:
                errors.append(f"{pf.relative_to(ROOT_DIR)}:{e.lineno} SyntaxError: {e.msg}")

        if errors:
            return False, "\n".join(errors)
        return True, f"Python AST syntax validated across {len(py_files_ast)} files (Ruff not installed)."


# ==============================================================================
# 4. AUTOMATED TESTS (PYTEST)
# ==============================================================================
def step_automated_tests(fast_only: bool = False) -> Tuple[bool, str]:
    """Chạy bộ kiểm thử tự động với Pytest."""
    has_pytest = shutil.which("pytest") is not None
    if not has_pytest:
        try:
            import pytest  # noqa: F401
            has_pytest = True
        except ImportError:
            has_pytest = False

    if not has_pytest:
        return True, "Pytest is not installed in current environment. Skipped."

    if fast_only:
        test_paths = ["tests/unit"]
    else:
        test_paths = ["tests/unit", "tests/integration", "tests/adversarial"]

    valid_paths = [p for p in test_paths if (ROOT_DIR / p).exists()]
    if not valid_paths:
        return True, "No test paths found. Skipped."

    code, out, err = run_cmd([sys.executable, "-m", "pytest"] + valid_paths + ["-q"])
    if code == 0:
        summary_line = [line for line in out.splitlines() if "passed" in line]
        msg = summary_line[-1] if summary_line else "All tests passed successfully."
        return True, msg
    else:
        return False, out or err


# ==============================================================================
# 5. ADVERSARIAL BENCHMARK SMOKE TEST
# ==============================================================================
def step_benchmark_smoke_test() -> Tuple[bool, str]:
    """Chạy thử nghiệm Adversarial Smoke Benchmark đo độ trễ P50/P95/P99."""
    benchmark_script = ROOT_DIR / "scripts" / "benchmark.py"
    if not benchmark_script.exists():
        return True, "scripts/benchmark.py not found. Skipped."

    code, out, err = run_cmd([sys.executable, str(benchmark_script), "--mock"])
    if code == 0:
        latency_line = [line for line in out.splitlines() if "Latency:" in line]
        msg = latency_line[-1] if latency_line else "Adversarial benchmark smoke test completed."
        return True, msg
    else:
        return False, err or out


# ==============================================================================
# 6. DOCUMENTATION PORTAL BUILD (MKDOCS)
# ==============================================================================
def step_docs_portal_build() -> Tuple[bool, str]:
    """Chạy script tổng hợp tài liệu và biên dịch MkDocs Material cục bộ."""
    build_script = ROOT_DIR / "scripts" / "build_docs_portal.py"
    if not build_script.exists():
        return True, "scripts/build_docs_portal.py not found. Skipped."

    # 1. Aggregate content
    code, out, err = run_cmd([sys.executable, str(build_script)])
    if code != 0:
        return False, f"Docs aggregator failed: {err or out}"

    # 2. Check mkdocs build
    has_mkdocs = shutil.which("mkdocs") is not None
    if not has_mkdocs:
        try:
            import mkdocs  # noqa: F401
            has_mkdocs = True
        except ImportError:
            has_mkdocs = False

    if not has_mkdocs:
        return True, "Content aggregated. mkdocs package not installed, skipped static site compilation."

    code, out, err = run_cmd(["mkdocs", "build"])
    if code == 0:
        return True, "MkDocs static site built successfully in ./site (100% clean)."
    else:
        return False, f"MkDocs build error: {err or out}"


# ==============================================================================
# 7. GIT PRE-COMMIT HOOK INSTALLER
# ==============================================================================
def install_pre_commit_hook() -> int:
    """Tự động cài đặt hoặc cập nhật Git Pre-commit Hook để chạy validate_local.py --mode pre-commit."""
    git_dir = ROOT_DIR / ".git"
    if not git_dir.exists():
        print(f"{RED}❌ Không tìm thấy thư mục .git. Vui lòng chạy lệnh từ thư mục gốc dự án.{RESET}")
        return 1

    hooks_dir = git_dir / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)
    hook_file = hooks_dir / "pre-commit"

    hook_content = """#!/bin/sh
# PI-Guard Local Quality Assurance Pre-commit Hook
# Tự động kiểm tra ranh giới Workspace, file bất biến, cú pháp JSON và Linting trước khi commit.

echo "🛡️ [Local-QA] Đang chạy kiểm định trước khi commit (Pre-commit Validation)..."

python scripts/validate_local.py --mode pre-commit
VALIDATION_EXIT=$?

if [ $VALIDATION_EXIT -ne 0 ]; then
    echo ""
    echo "❌ [Pre-commit Blocked] Commit bị chặn do phát hiện lỗi vi phạm quy chuẩn dự án!"
    echo "👉 Vui lòng đọc chi tiết lỗi ở trên và khắc phục trước khi commit lại."
    exit 1
fi

echo "✅ [Pre-commit Passed] Tất cả các điều kiện kiểm định đều đạt chuẩn."
exit 0
"""

    with open(hook_file, "w", encoding="utf-8", newline="\n") as f:
        f.write(hook_content)

    try:
        import stat
        os.chmod(hook_file, os.stat(hook_file).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    except Exception:
        pass

    print(f"\n{GREEN}✅ Đã cài đặt thành công Git Pre-commit Hook tại: {hook_file}{RESET}")
    print(f"{CYAN}   Mỗi khi thực hiện `git commit`, Git sẽ tự động chạy: `python scripts/validate_local.py --mode pre-commit`{RESET}\n")
    return 0


# ==============================================================================
# MAIN EXECUTION CONTROLLER
# ==============================================================================
def main() -> int:
    parser = argparse.ArgumentParser(
        description="PI-Guard Unified Local Quality Assurance & Validation Suite (Local-First QA)."
    )
    parser.add_argument(
        "--mode",
        choices=["pre-commit", "fast", "full"],
        default="fast",
        help="Chế độ kiểm tra: 'pre-commit' (chạy nhanh trên staged files), 'fast' (mặc định), 'full' (toàn diện).",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Chạy toàn bộ các bước kiểm tra (tương đương --mode full).",
    )
    parser.add_argument(
        "--install-hook",
        action="store_true",
        help="Cài đặt Git Pre-commit hook để tự động chạy kiểm định cục bộ trước mỗi commit.",
    )
    parser.add_argument(
        "--check-boundaries",
        action="store_true",
        help="Chỉ chạy kiểm toán ranh giới workspace và file bất biến.",
    )
    parser.add_argument(
        "--check-manifests",
        action="store_true",
        help="Chỉ chạy kiểm định cú pháp các file JSON manifest.",
    )
    parser.add_argument(
        "--check-lint",
        action="store_true",
        help="Chỉ chạy kiểm tra code linting với Ruff.",
    )
    parser.add_argument(
        "--check-tests",
        action="store_true",
        help="Chỉ chạy kiểm thử tự động với Pytest.",
    )
    parser.add_argument(
        "--check-benchmark",
        action="store_true",
        help="Chỉ chạy benchmark đối kháng smoke test.",
    )
    parser.add_argument(
        "--check-docs",
        action="store_true",
        help="Chỉ chạy tổng hợp và build static site MkDocs.",
    )

    args = parser.parse_args()

    if args.install_hook:
        return install_pre_commit_hook()

    mode = "full" if args.all else args.mode

    individual_run = any(
        [
            args.check_boundaries,
            args.check_manifests,
            args.check_lint,
            args.check_tests,
            args.check_benchmark,
            args.check_docs,
        ]
    )

    start_time = time.time()
    log_header(f"Bắt Đầu Kiểm Định Chất Lượng Cục Bộ (Mode: {mode.upper()})")

    steps_to_run: List[Tuple[str, callable, tuple]] = []

    if individual_run:
        if args.check_boundaries:
            steps_to_run.append(("Workspace Boundaries Audit", step_workspace_boundary_audit, ("staged",)))
        if args.check_manifests:
            steps_to_run.append(("JSON Manifests Validation", step_validate_manifests, (False,)))
        if args.check_lint:
            steps_to_run.append(("Code Quality & Linting", step_code_linting, (False,)))
        if args.check_tests:
            steps_to_run.append(("Automated Tests (Pytest)", step_automated_tests, (False,)))
        if args.check_benchmark:
            steps_to_run.append(("Adversarial Benchmark Smoke Test", step_benchmark_smoke_test, ()))
        if args.check_docs:
            steps_to_run.append(("Documentation Portal & MkDocs Build", step_docs_portal_build, ()))
    elif mode == "pre-commit":
        steps_to_run = [
            ("Workspace Boundaries Audit (Staged)", step_workspace_boundary_audit, ("staged",)),
            ("JSON Manifests Validation (Staged)", step_validate_manifests, (True,)),
            ("Code Quality & Linting (Staged)", step_code_linting, (True,)),
        ]
    elif mode == "fast":
        steps_to_run = [
            ("Workspace Boundaries Audit", step_workspace_boundary_audit, ("staged",)),
            ("JSON Manifests Validation", step_validate_manifests, (False,)),
            ("Code Quality & Linting (src/ tests/)", step_code_linting, (False,)),
            ("Adversarial Benchmark Smoke Test", step_benchmark_smoke_test, ()),
        ]
    elif mode == "full":
        steps_to_run = [
            ("Workspace Boundaries Audit", step_workspace_boundary_audit, ("staged",)),
            ("JSON Manifests Validation", step_validate_manifests, (False,)),
            ("Code Quality & Linting (src/ tests/)", step_code_linting, (False,)),
            ("Automated Tests (Pytest Suite)", step_automated_tests, (False,)),
            ("Adversarial Benchmark Smoke Test", step_benchmark_smoke_test, ()),
            ("Documentation Portal & MkDocs Build", step_docs_portal_build, ()),
        ]

    results: List[Dict[str, any]] = []
    overall_pass = True

    for name, func, f_args in steps_to_run:
        step_start = time.time()
        print(f"\n{BOLD}▶ Đang kiểm tra: {BLUE}{name}{RESET}...")
        passed, msg = func(*f_args)
        elapsed = time.time() - step_start

        if passed:
            print(f"  {GREEN}✔ [PASS]{RESET} {msg} ({elapsed:.2f}s)")
        else:
            print(f"  {RED}✖ [FAIL]{RESET} {name} thất bại! ({elapsed:.2f}s)")
            print(f"    {YELLOW}Chi tiết lỗi:{RESET}\n{msg}")
            overall_pass = False

        results.append({
            "name": name,
            "passed": passed,
            "message": msg,
            "elapsed": elapsed
        })

    total_time = time.time() - start_time

    # BẢNG TỔNG KẾT
    print(f"\n{BOLD}{CYAN}{'='*80}{RESET}")
    print(f"{BOLD}{CYAN}📊 BẢNG TỔNG KẾT KIỂM ĐỊNH CHẤT LƯỢNG LOCAL (LOCAL QA SCORECARD){RESET}")
    print(f"{BOLD}{CYAN}{'='*80}{RESET}")
    print(f"{'STT':<4} | {'Hạng Mục Kiểm Tra':<45} | {'Kết Quả':<10} | {'Thời Gian'}")
    print("-" * 80)

    for idx, r in enumerate(results, start=1):
        status_str = f"{GREEN}PASS{RESET}" if r["passed"] else f"{RED}FAIL{RESET}"
        print(f"{idx:<4} | {r['name']:<45} | {status_str:<19} | {r['elapsed']:.2f}s")

    print("-" * 80)
    print(f"Tổng thời gian kiểm định: {total_time:.2f}s")

    if overall_pass:
        print(f"\n{BOLD}{GREEN}🎉 TẤT CẢ CÁC ĐIỀU KIỆN KIỂM ĐỊNH CỤC BỘ ĐỀU ĐẠT CHUẨN (100% PASS)!{RESET}")
        print(f"{GREEN}   Mã nguồn, ranh giới thư mục và tài liệu sẵn sàng an toàn cho commit và tích hợp.{RESET}")
        print(f"{BOLD}{CYAN}{'='*80}{RESET}\n")
        return 0
    else:
        print(f"\n{BOLD}{RED}🚨 PHÁT HIỆN LỖI TRONG QUÁ TRÌNH KIỂM ĐỊNH (FAILED)!{RESET}")
        print(f"{RED}   Vui lòng sửa các lỗi được liệt kê ở trên trước khi commit hoặc merge.{RESET}")
        print(f"{BOLD}{CYAN}{'='*80}{RESET}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
