#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_workspace_boundaries.py
-----------------------------
Tool kiểm toán phạm vi không gian làm việc (Workspace Boundary Audit) cho đồ án PI-Guard.

Quy tắc bất biến:
1. Thành viên nhóm (Đức, Việt, Phương) CHỈ được phép tạo, chỉnh sửa, xóa file trong thư mục
   workspace được phân công tương ứng:
   - Nguyễn Quí Đức:         workspaces/ducnq/
   - Phạm Minh Hoàng Việt:   workspaces/vietpmh/
   - Đỗ Đoàn Duy Phương:     workspaces/phuongddd/
2. CHỈ DUY NHẤT Trưởng nhóm (Leader: nvtruongops / Nguyễn Văn Trường) mới có quyền chỉnh sửa
   các thư mục chung ngoài workspaces/ (src/, docs/, Meeting/, reports/, data/, models/, scripts/, .agents/, etc.)
   để phục vụ quá trình nghiệm thu, đồng quy tri thức (Knowledge Convergence).
3. TẤT CẢ THÀNH VIÊN (kể cả Leader) TUYỆT ĐỐI KHÔNG được sửa đổi các file/thư mục bất biến (Read-Only):
   - CAPSTONE PROJECT REGISTER.md
   - docs/fpt_capstone_guide/
"""

import os
import sys
import argparse
import subprocess
from typing import List, Dict, Tuple, Optional

# Reconfigure standard output for UTF-8 on Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Danh mục định danh thành viên và workspace hợp lệ
LEADER_IDENTIFIERS = [
    'nvtruongops', 'nguyen van truong', 'nguyễn văn trường',
    'truongnv', 'truong_data_eng', 'truongnvse182034@fpt.edu.vn'
]

MEMBERS_MAP = {
    'duc': {
        'name': 'Nguyễn Quí Đức',
        'mssv': 'SE182087',
        'identifiers': ['ducnq', 'nguyen qui duc', 'nguyễn quí đức', 'duc_baseline_ml', 'ducnqse182087@fpt.edu.vn'],
        'allowed_prefix': 'workspaces/ducnq/'
    },
    'viet': {
        'name': 'Phạm Minh Hoàng Việt',
        'mssv': 'SE181851',
        'identifiers': ['vietpmh', 'pham minh hoang viet', 'phạm minh hoàng việt', 'viet_transformer_robustness', 'vietpmhse181851@fpt.edu.vn'],
        'allowed_prefix': 'workspaces/vietpmh/'
    },
    'phuong': {
        'name': 'Đỗ Đoàn Duy Phương',
        'mssv': 'SE180235',
        'identifiers': ['phuongddd', 'do doan duy phuong', 'đỗ đoàn duy phương', 'phuong_api_dashboard', 'phuongdddse180235@fpt.edu.vn'],
        'allowed_prefix': 'workspaces/phuongddd/'
    },
    'truong': {
        'name': 'Nguyễn Văn Trường (Leader)',
        'mssv': 'SE182034',
        'identifiers': LEADER_IDENTIFIERS,
        'allowed_prefix': ''  # Leader has full access outside immutable paths
    }
}

# Danh mục các file & thư mục bất biến (Strictly Read-Only cho TẤT CẢ thành viên)
STRICT_IMMUTABLE_PATHS = [
    'CAPSTONE PROJECT REGISTER.md',
    'docs/fpt_capstone_guide/'
]

def run_git_cmd(args: List[str], cwd: Optional[str] = None) -> Tuple[int, str]:
    """Chạy lệnh Git và trả về exit code cùng stdout."""
    try:
        res = subprocess.run(
            ['git'] + args,
            cwd=cwd or os.getcwd(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        return res.returncode, res.stdout.strip()
    except Exception as e:
        return -1, str(e)

def normalize_path(path: str) -> str:
    """Chuẩn hóa đường dẫn dạng forward slash, loại bỏ dấu ngoặc kép của git."""
    p = path.strip().strip('"').strip("'")
    p = p.replace('\\', '/')
    if p.startswith('./'):
        p = p[2:]
    return p

def get_current_git_user() -> Dict[str, str]:
    """Lấy thông tin Git user hiện tại."""
    _, name = run_git_cmd(['config', 'user.name'])
    _, email = run_git_cmd(['config', 'user.email'])
    _, branch = run_git_cmd(['rev-parse', '--abbrev-ref', 'HEAD'])
    return {
        'name': name,
        'email': email,
        'branch': branch
    }

def detect_member_role(user_info: Dict[str, str], override_author: Optional[str] = None) -> Tuple[str, Dict]:
    """Xác định vai trò thành viên dựa trên user info hoặc override."""
    search_str = (override_author or f"{user_info.get('name', '')} {user_info.get('email', '')} {user_info.get('branch', '')}").lower()
    
    # Kiểm tra nếu là Leader
    for ident in LEADER_IDENTIFIERS:
        if ident in search_str:
            return 'truong', MEMBERS_MAP['truong']
            
    # Kiểm tra các thành viên khác
    for key in ['duc', 'viet', 'phuong']:
        mem = MEMBERS_MAP[key]
        for ident in mem['identifiers']:
            if ident in search_str:
                return key, mem
        if key in search_str or f"feat/{key}" in search_str:
            return key, mem
            
    # Mặc định: nếu không nhận diện được và không phải leader -> gán là unknown/member
    return 'unknown', {
        'name': f"Unknown / Non-Leader User ({user_info.get('name', 'Anonymous')})",
        'mssv': 'UNKNOWN',
        'identifiers': [],
        'allowed_prefix': 'workspaces/'
    }

def get_changed_files(mode: str, commit_range: Optional[str] = None) -> List[str]:
    """Lấy danh sách các file bị thay đổi tùy theo chế độ kiểm tra."""
    files = set()
    
    if mode in ['working_tree', 'all']:
        # Untracked and modified un-staged files
        code, out = run_git_cmd(['status', '--porcelain'])
        if code == 0 and out:
            for line in out.splitlines():
                if len(line) > 3:
                    raw_path = line[3:].strip()
                    # Handle renames: R  old -> new
                    if ' -> ' in raw_path:
                        raw_path = raw_path.split(' -> ')[1].strip()
                    files.add(normalize_path(raw_path))
                    
    if mode in ['staged', 'all']:
        code, out = run_git_cmd(['diff', '--name-only', '--cached'])
        if code == 0 and out:
            for line in out.splitlines():
                if line.strip():
                    files.add(normalize_path(line.strip()))
                    
    if mode == 'commit_range' and commit_range:
        code, out = run_git_cmd(['diff', '--name-only', commit_range])
        if code == 0 and out:
            for line in out.splitlines():
                if line.strip():
                    files.add(normalize_path(line.strip()))
                    
    if mode == 'last_commit':
        code, out = run_git_cmd(['diff-tree', '--no-commit-id', '--name-only', '-r', 'HEAD'])
        if code == 0 and out:
            for line in out.splitlines():
                if line.strip():
                    files.add(normalize_path(line.strip()))
                    
    return sorted(list(files))

def check_violations(files: List[str], role_key: str, role_info: Dict, is_leader: bool) -> List[Dict[str, str]]:
    """Kiểm tra danh sách file vi phạm quy tắc workspace và file bất biến."""
    violations = []
    
    for f in files:
        if not f:
            continue
            
        # 1. Kiểm tra vi phạm file bất biến (Áp dụng cho TẤT CẢ mọi người kể cả Leader)
        is_immutable = False
        for imm in STRICT_IMMUTABLE_PATHS:
            if f == imm or f.startswith(imm):
                violations.append({
                    'file': f,
                    'type': 'IMMUTABLE_FILE_VIOLATION',
                    'severity': 'CRITICAL',
                    'reason': f"File hoặc thư mục [{imm}] là tài liệu chính thức bất biến của Nhà trường (Strictly Read-Only)."
                })
                is_immutable = True
                break
                
        if is_immutable:
            continue
            
        # 2. Kiểm tra vi phạm phân quyền Workspace
        if is_leader:
            # Leader được phép sửa các file dự án chung (src/, docs/, Meeting/, etc.)
            continue
        else:
            # Thành viên thông thường
            allowed_prefix = role_info.get('allowed_prefix', '')
            if allowed_prefix:
                if not f.startswith(allowed_prefix):
                    violations.append({
                        'file': f,
                        'type': 'WORKSPACE_BOUNDARY_VIOLATION',
                        'severity': 'ERROR',
                        'reason': (
                            f"Thành viên [{role_info['name']}] chỉ được phép tạo/sửa file trong thư mục [{allowed_prefix}]. "
                            f"Việc sửa đổi trực tiếp file [{f}] ngoài workspace là vi phạm quy định nhóm."
                        )
                    })
            else:
                # Unknown member -> Bị chặn nếu sửa file ngoài workspaces/
                if not f.startswith('workspaces/'):
                    violations.append({
                        'file': f,
                        'type': 'UNAUTHORIZED_ROOT_EDIT',
                        'severity': 'ERROR',
                        'reason': f"Tài khoản không phải Leader không được phép chỉnh sửa các thư mục nguồn chung ngoài workspaces/."
                    })
                    
    return violations

def print_banner():
    print("=" * 80)
    print(" 🛡️  PI-GUARD WORKSPACE & COMMIT BOUNDARY AUDITOR")
    print("    Kiểm toán phân quyền & ranh giới không gian làm việc nhóm")
    print("=" * 80)

def main():
    parser = argparse.ArgumentParser(
        description="Kiểm toán ranh giới Workspace và ngăn ngừa xung đột Git cho nhóm PI-Guard."
    )
    parser.add_argument(
        '--mode',
        choices=['all', 'working_tree', 'staged', 'last_commit', 'commit_range'],
        default='all',
        help="Chế độ kiểm tra file thay đổi (mặc định: 'all' - cả working tree và staged)."
    )
    parser.add_argument(
        '--commit-range',
        type=str,
        default=None,
        help="Dải commit cần kiểm tra (ví dụ: 'origin/main..HEAD')."
    )
    parser.add_argument(
        '--author',
        type=str,
        default=None,
        help="Ghi đè định danh người thực hiện commit để kiểm tra phân quyền."
    )
    parser.add_argument(
        '--install-hook',
        action='store_true',
        help="Tự động cài đặt Git Pre-commit hook vào .git/hooks/pre-commit."
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help="Hiển thị chi tiết danh sách file hợp lệ và thông tin debug."
    )

    args = parser.parse_args()

    print_banner()

    # Xử lý cài đặt hook nếu được yêu cầu
    if args.install_hook:
        install_pre_commit_hook()
        return 0

    # Lấy thông tin người dùng Git hiện tại
    user_info = get_current_git_user()
    role_key, role_info = detect_member_role(user_info, args.author)
    is_leader = (role_key == 'truong')

    print(f"👤 Người thực hiện   : {role_info['name']} (Mã SV: {role_info['mssv']})")
    print(f"🌿 Nhánh Git hiện tại: {user_info.get('branch', 'N/A')}")
    perm_desc = "Trưởng nhóm (Leader) — Toàn quyền điều phối & merge" if is_leader else f"Thành viên — Giới hạn trong [{role_info.get('allowed_prefix', 'workspaces/')}]"
    print(f"🔑 Quyền hạn         : {perm_desc}")
    print(f"🔍 Chế độ kiểm toán  : {args.mode}" + (f" ({args.commit_range})" if args.commit_range else ""))
    print("-" * 80)

    # Lấy danh sách file thay đổi
    changed_files = get_changed_files(args.mode, args.commit_range)

    if not changed_files:
        print("✅ Không phát hiện file nào bị thay đổi trong phạm vi kiểm tra.")
        print("=" * 80)
        return 0

    print(f"📁 Tổng số file phát hiện thay đổi: {len(changed_files)}")
    if args.verbose:
        for idx, f in enumerate(changed_files, start=1):
            print(f"   [{idx:02d}] {f}")
    print("-" * 80)

    # Kiểm tra vi phạm
    violations = check_violations(changed_files, role_key, role_info, is_leader)

    if not violations:
        print("🎉 KẾT QUẢ KIỂM TOÁN: HỢP LỆ (PASS)")
        print("   Tất cả các thay đổi đều nằm trong phạm vi cho phép và tuân thủ quy định nhóm.")
        print("=" * 80)
        return 0
    else:
        print(f"🚨 KẾT QUẢ KIỂM TOÁN: PHÁT HIỆN {len(violations)} VI PHẠM (FAILED)")
        print("=" * 80)
        for idx, v in enumerate(violations, start=1):
            print(f"❌ Vi phạm #{idx} [{v['severity']}]: {v['type']}")
            print(f"   📄 File       : {v['file']}")
            print(f"   ⚠️  Nguyên nhân: {v['reason']}")
            print()

        print("-" * 80)
        print("💡 HƯỚNG DẪN KHẮC PHỤC DÀNH CHO THÀNH VIÊN:")
        if not is_leader:
            allowed_p = role_info.get('allowed_prefix', 'workspaces/<tên_bạn>/')
            print(f"1. Vui lòng di chuyển hoặc sao chép các file bạn vừa tạo vào thư mục: [{allowed_p}]")
            print(f"2. Loại bỏ các file ngoài workspace khỏi Git Staging:")
            print(f"   git restore --staged <file_ngoài_workspace>")
            print(f"   git checkout -- <file_ngoài_workspace>  (hoặc git rm --cached)")
            print(f"3. Chỉ Trưởng nhóm (Leader: nvtruongops) mới có thẩm quyền đưa code/tài liệu từ workspace ra thư mục chung trong buổi họp đồng quy hàng tuần.")
        else:
            print("1. Nếu vi phạm file bất biến (CAPSTONE PROJECT REGISTER / docs/fpt_capstone_guide), vui lòng hoàn tác (git checkout / git restore) ngay lập tức.")
        print("=" * 80)
        return 1

def install_pre_commit_hook():
    """Tự động tạo hook pre-commit trong .git/hooks/."""
    git_dir = os.path.join(os.getcwd(), '.git')
    if not os.path.exists(git_dir):
        print("❌ Không tìm thấy thư mục .git. Vui lòng chạy lệnh từ thư mục gốc của repo.")
        return 1

    hooks_dir = os.path.join(git_dir, 'hooks')
    os.makedirs(hooks_dir, exist_ok=True)

    hook_file = os.path.join(hooks_dir, 'pre-commit')
    
    # Nội dung pre-commit hook (chạy trên cả Windows shell và Linux/macOS bash)
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

    with open(hook_file, 'w', encoding='utf-8', newline='\n') as f:
        f.write(hook_content)

    try:
        import stat
        os.chmod(hook_file, os.stat(hook_file).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    except Exception:
        pass

    print(f"✅ Đã cài đặt thành công Git Pre-commit Hook tại: {hook_file}")
    print("   Từ bây giờ, Git sẽ tự động chạy `python scripts/validate_local.py --mode pre-commit` mỗi khi có thành viên thực hiện `git commit`.")
    return 0

if __name__ == '__main__':
    sys.exit(main())
