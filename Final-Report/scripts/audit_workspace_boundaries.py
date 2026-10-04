#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_workspace_boundaries.py
-----------------------------
Kiểm tra các đường dẫn hồ sơ học thuật bất biến của PI-Guard.

Repository hiện có một maintainer. Phân quyền thành viên theo workspace đã nghỉ.
Các đường dẫn read-only được duy trì theo Rule 01:
- CAPSTONE PROJECT REGISTER.md
- docs/fpt_capstone_guide/
"""

import argparse
import os
import subprocess
import sys
from typing import Dict, List, Optional, Tuple

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

STRICT_IMMUTABLE_PATHS = [
    "CAPSTONE PROJECT REGISTER.md",
    "docs/fpt_capstone_guide/",
]


def run_git_cmd(args: List[str], cwd: Optional[str] = None) -> Tuple[int, str]:
    """Run Git and return its exit code and stdout."""
    try:
        res = subprocess.run(
            ["git", *args],
            cwd=cwd or os.getcwd(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        return res.returncode, res.stdout.strip()
    except Exception as exc:
        return -1, str(exc)


def normalize_path(path: str) -> str:
    """Normalize Git paths to forward slashes."""
    path = path.strip().strip('"').strip("'").replace("\\", "/")
    return path[2:] if path.startswith("./") else path


def get_current_git_user() -> Dict[str, str]:
    """Read the configured Git identity and current branch."""
    _, name = run_git_cmd(["config", "user.name"])
    _, branch = run_git_cmd(["rev-parse", "--abbrev-ref", "HEAD"])
    return {"name": name, "branch": branch}


def get_changed_files(mode: str, commit_range: Optional[str] = None) -> List[str]:
    """List paths changed in the selected Git scope."""
    files = set()

    if mode in ["working_tree", "all"]:
        code, out = run_git_cmd(["status", "--porcelain"])
        if code == 0 and out:
            for line in out.splitlines():
                if len(line) > 3:
                    raw_path = line[3:].strip()
                    if " -> " in raw_path:
                        raw_path = raw_path.split(" -> ", 1)[1].strip()
                    files.add(normalize_path(raw_path))

    if mode in ["staged", "all"]:
        code, out = run_git_cmd(["diff", "--name-only", "--cached"])
        if code == 0 and out:
            files.update(normalize_path(line) for line in out.splitlines() if line.strip())

    if mode == "commit_range" and commit_range:
        code, out = run_git_cmd(["diff", "--name-only", commit_range])
        if code == 0 and out:
            files.update(normalize_path(line) for line in out.splitlines() if line.strip())

    if mode == "last_commit":
        code, out = run_git_cmd(["diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"])
        if code == 0 and out:
            files.update(normalize_path(line) for line in out.splitlines() if line.strip())

    return sorted(files)


def check_violations(files: List[str]) -> List[Dict[str, str]]:
    """Reject changes to protected academic records."""
    violations = []
    for path in files:
        if not path:
            continue
        for immutable in STRICT_IMMUTABLE_PATHS:
            if path == immutable or path.startswith(immutable):
                violations.append(
                    {
                        "file": path,
                        "type": "IMMUTABLE_FILE_VIOLATION",
                        "severity": "CRITICAL",
                        "reason": f"{immutable} is a protected read-only project record.",
                    }
                )
                break
    return violations


def print_banner() -> None:
    print("=" * 80)
    print(" PI-GUARD PROTECTED-PATH AUDITOR")
    print(" Kiểm tra các hồ sơ học thuật bất biến")
    print("=" * 80)


def install_pre_commit_hook() -> int:
    """Install the local validation hook in .git/hooks."""
    git_dir = os.path.join(os.getcwd(), ".git")
    if not os.path.isdir(git_dir):
        print("Không tìm thấy thư mục .git. Hãy chạy lệnh từ thư mục gốc repository.")
        return 1

    hooks_dir = os.path.join(git_dir, "hooks")
    os.makedirs(hooks_dir, exist_ok=True)
    hook_file = os.path.join(hooks_dir, "pre-commit")
    hook_content = """#!/bin/sh
echo \"[Local-QA] Running pre-commit validation...\"
python Final-Report/scripts/validate_local.py --mode pre-commit
VALIDATION_EXIT=$?
if [ $VALIDATION_EXIT -ne 0 ]; then
    echo \"[Pre-commit Blocked] Fix the reported validation errors before committing.\"
    exit 1
fi
echo \"[Pre-commit Passed] Validation completed successfully.\"
exit 0
"""
    with open(hook_file, "w", encoding="utf-8", newline="\n") as hook:
        hook.write(hook_content)
    try:
        import stat

        os.chmod(hook_file, os.stat(hook_file).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    except Exception:
        pass
    print(f"Installed Git pre-commit hook at: {hook_file}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check PI-Guard changes against protected academic project records."
    )
    parser.add_argument(
        "--mode",
        choices=["all", "working_tree", "staged", "last_commit", "commit_range"],
        default="all",
        help="Git change scope to audit (default: all).",
    )
    parser.add_argument(
        "--commit-range",
        default=None,
        help="Commit range to inspect, for example origin/main..HEAD.",
    )
    parser.add_argument(
        "--install-hook",
        action="store_true",
        help="Install a Git pre-commit hook that runs local validation.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="List every changed path.",
    )
    args = parser.parse_args()

    print_banner()
    if args.install_hook:
        return install_pre_commit_hook()

    user_info = get_current_git_user()
    print(f"Git user: {user_info.get('name') or 'not configured'}")
    print(f"Branch: {user_info.get('branch') or 'N/A'}")
    print(f"Mode: {args.mode}" + (f" ({args.commit_range})" if args.commit_range else ""))
    print("-" * 80)

    changed_files = get_changed_files(args.mode, args.commit_range)
    if not changed_files:
        print("No changed paths found in the selected scope.")
        return 0

    print(f"Changed paths: {len(changed_files)}")
    if args.verbose:
        for path in changed_files:
            print(f"  {path}")

    violations = check_violations(changed_files)
    if not violations:
        print("PASS: no protected paths were changed.")
        return 0

    print(f"FAIL: {len(violations)} protected-path violation(s).")
    for violation in violations:
        print(
            f"{violation['severity']} {violation['type']}: "
            f"{violation['file']} — {violation['reason']}"
        )
    print("Restore the protected paths, then run the audit again.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
