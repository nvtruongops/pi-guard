---
name: team-commit-and-workspace-audit
description: >-
  Kiểm toán tự động lịch sử commit, git diff, staging area và Pull Requests để phát hiện và ngăn chặn
  các vi phạm phân quyền Workspace (thành viên tạo/sửa file ngoài workspaces/ hoặc xâm phạm file bất biến).
---

# Team Commit & Workspace Boundary Audit Guide

Skill này cung cấp cơ chế và công cụ tự động để **kiểm toán (audit) toàn bộ commit, staging area và pull request** của các thành viên trong nhóm đồ án **PI-Guard**, bảo vệ tính toàn vẹn của repository.

---

## 🛡️ 1. Nguyên Tắc Kiểm Toán Ranh Giới (Boundary Audit Rules)

### Quy Tắc 1: Phân Quyền Theo Workspace Cá Nhân
- Mỗi thành viên (Đức, Việt, Phương) chỉ được phép tạo, sửa, xóa file trong đúng thư mục workspace của mình:
  - `workspaces/ducnq/` $\rightarrow$ Chỉ `ducnq`
  - `workspaces/vietpmh/` $\rightarrow$ Chỉ `vietpmh`
  - `workspaces/phuongddd/` $\rightarrow$ Chỉ `phuongddd`
- Bất kỳ commit nào của thành viên chứa file nằm ngoài thư mục workspace của họ (ví dụ sửa trực tiếp `src/`, `docs/`, `Meeting/`, `reports/`, `models/`, `data/`) đều bị đánh dấu là **🚨 VIOLATION: WORKSPACE_BOUNDARY_VIOLATION**.

### Quy Tắc 2: Độc Quyền Quản Trị Của Leader (Trường)
- Chỉ có Trưởng nhóm (`nvtruongops` / Nguyễn Văn Trường) mới có quyền chỉnh sửa các file thuộc cây thư mục gốc ngoài `workspaces/`.

### Quy Tắc 3: Bất Biến Tuyệt Đối (Strictly Read-Only) Cho Tất Cả Mọi Người
- Bất kỳ ai (kể cả Leader) có commit chỉnh sửa vào các file sau đều bị chặn với mức độ nghiêm trọng **🚨 CRITICAL**:
  - `CAPSTONE PROJECT REGISTER.md`
  - `docs/fpt_capstone_guide/` (Toàn bộ thư mục)

---

## 💻 2. Công Cụ Kiểm Toán: `scripts/audit_workspace_boundaries.py`

Nhóm đã trang bị script Python [`scripts/audit_workspace_boundaries.py`](file:///d:/Work/Do-an/scripts/audit_workspace_boundaries.py) để tự động hóa toàn bộ việc kiểm tra.

### 📌 Các Lệnh Thực Thi Phổ Biến:

#### 1. Kiểm tra toàn bộ thay đổi hiện tại (Working Tree + Staging Area):
```bash
python scripts/audit_workspace_boundaries.py --mode all
```

#### 2. Kiểm tra các file đã `git add` trước khi commit (Staged Only):
```bash
python scripts/audit_workspace_boundaries.py --mode staged
```

#### 3. Kiểm tra commit vừa tạo gần nhất:
```bash
python scripts/audit_workspace_boundaries.py --mode last_commit
```

#### 4. Kiểm tra một dải commit / Pull Request của thành viên:
```bash
# Kiểm tra PR của Đức
python scripts/audit_workspace_boundaries.py --commit-range origin/main..HEAD --author ducnq

# Kiểm tra PR của Việt
python scripts/audit_workspace_boundaries.py --commit-range origin/main..HEAD --author vietpmh

# Kiểm tra PR của Phương
python scripts/audit_workspace_boundaries.py --commit-range origin/main..HEAD --author phuongddd
```

#### 5. Xem chi tiết danh sách file (Verbose):
```bash
python scripts/audit_workspace_boundaries.py --mode all --verbose
```

---

## 🔒 3. Tự Động Hóa Bằng Git Pre-Commit Hook

Để ngăn chặn commit sai quy tắc ngay từ máy của thành viên, mỗi thành viên chỉ cần chạy lệnh cài đặt 1 lần duy nhất:

```bash
python scripts/audit_workspace_boundaries.py --install-hook
```

Sau khi cài đặt:
- Mỗi khi thành viên gõ `git commit`, Git sẽ tự động gọi `scripts/audit_workspace_boundaries.py --mode staged`.
- Nếu phát hiện vi phạm: Git sẽ **tự động hủy bỏ commit (Abort)** và in ra hướng dẫn sửa file.
- Nếu hợp lệ: Git cho phép commit tiếp tục bình thường.

---

## 🚨 4. Bảng Tra Cứu Mã Lỗi & Cách Khắc Phục

| Mã Lỗi (Violation Type) | Mức Độ | Nguyên Nhân | Cách Khắc Phục |
| :--- | :---: | :--- | :--- |
| `IMMUTABLE_FILE_VIOLATION` | 🔴 **CRITICAL** | Chỉnh sửa `CAPSTONE REGISTER` hoặc `docs/fpt_capstone_guide/` | Chạy `git restore <file>` hoặc `git checkout -- <file>` để hủy thay đổi ngay lập tức. |
| `WORKSPACE_BOUNDARY_VIOLATION` | 🟠 **ERROR** | Thành viên sửa/tạo file ngoài thư mục workspace của mình | Di chuyển file vào `workspaces/<tên_workspace>/` và bỏ file cũ khỏi Git (`git reset HEAD <file>`). |
| `UNAUTHORIZED_ROOT_EDIT` | 🟠 **ERROR** | Tài khoản không xác định sửa trực tiếp vào `src/` hoặc `docs/` | Đảm bảo cấu hình đúng `git config user.name` hoặc đẩy code qua workspace. |
