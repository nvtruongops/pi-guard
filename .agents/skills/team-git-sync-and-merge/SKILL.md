---
name: team-git-sync-and-merge
description: >-
  Quy trình đồng bộ, hợp nhất nhánh Git (Branching, Merge, Push) và phòng ngừa xung đột (Conflict-Free)
  cho nhóm đồ án PI-Guard. Đảm bảo các thành viên chỉ làm việc trong workspaces/ riêng và chỉ Leader (nvtruongops)
  mới có quyền merge code/tài liệu ra các thư mục chung.
---

# Team Git Sync, Merge & Conflict-Free Collaboration Guide

Skill này quy định và tự động hóa quy trình làm việc Git chuẩn mực cho cả 4 thành viên nhóm đồ án **PI-Guard** (FPT University Capstone Project IAP491), nhằm đảm bảo:
1. **Tuyệt đối không xảy ra xung đột mã nguồn (Zero Merge Conflicts)** giữa các thành viên.
2. **Bảo toàn phân quyền**: Thành viên chỉ chỉnh sửa trong workspace cá nhân (`workspaces/<tên_thành_viên>/`).
3. **Độc quyền xuất bản của Leader**: Chỉ có **Trưởng nhóm (`nvtruongops` / Nguyễn Văn Trường)** mới được phép đồng quy tri thức, đưa code/tài liệu từ workspace ra các thư mục chung (`src/`, `docs/`, `Meeting/`, `reports/`, `models/`, `data/`) và merge vào nhánh `main`.

---

## 👥 1. Ma Trận Phân Quyền Nhánh & Thư Mục Git

| Member | Git Username / Identifiers | Nhánh Git Cá Nhân | Thư Mục Được Phép Chỉnh Sửa | Quyền Merge vào `main` & Thư Mục Chung |
| :--- | :--- | :--- | :--- | :---: |
| **Nguyễn Văn Trường (Leader)** | `nvtruongops`, `truongnv` | `main`, `lead/truong-*` | `workspaces/truongnv/` + **Toàn bộ repo** | ✅ **TOÀN QUYỀN DUYỆT & MERGE** |
| **Nguyễn Quí Đức** | `ducnq`, `duc_baseline_ml` | `feat/duc-baseline-ml` | `workspaces/ducnq/` | ❌ *Chỉ gửi PR từ workspace* |
| **Phạm Minh Hoàng Việt** | `vietpmh`, `viet_transformer` | `feat/viet-transformer` | `workspaces/vietpmh/` | ❌ *Chỉ gửi PR từ workspace* |
| **Đỗ Đoàn Duy Phương** | `phuongddd`, `phuong_dashboard` | `feat/phuong-api-ui` | `workspaces/phuongddd/` | ❌ *Chỉ gửi PR từ workspace* |

> [!CAUTION]
> **QUY TẮC BẤT DI BẤT DỊCH (TEAM GOVERNANCE INVARIANT)**:
> - Thành viên khác ngoài Leader **KHÔNG BAO GIỜ** được commit hoặc push trực tiếp vào `src/`, `docs/`, `Meeting/`, `reports/`, `data/`, `models/`.
> - Mọi thử nghiệm của thành viên (kể cả train mô hình, viết script cào dữ liệu, viết test) **PHẢI NẰM 100% TRONG `workspaces/<tên_thành_viên>/`**.

---

## 🔄 2. Quy Trình Làm Việc Hàng Ngày Dành Cho Thành Viên (Member Workflow)

### Bước 1: Đồng bộ mã nguồn mới nhất từ `origin/main`
Trước khi bắt đầu làm việc mỗi ngày, thành viên phải rebase nhánh của mình với `main`:
```bash
git checkout feat/<tên_bạn>
git fetch origin
git rebase origin/main
```

### Bước 2: Làm việc strictly trong workspace của mình
- Đức: Chỉ tạo/sửa code trong `workspaces/ducnq/`
- Việt: Chỉ tạo/sửa code trong `workspaces/vietpmh/`
- Phương: Chỉ tạo/sửa code trong `workspaces/phuongddd/`

### Bước 3: Chạy script kiểm toán ranh giới trước khi commit (Pre-commit Audit)
Trước khi `git commit`, thành viên bắt buộc chạy kiểm tra:
```bash
python scripts/audit_workspace_boundaries.py --mode staged
```
- Nếu hiển thị `✅ PASS`: Được phép commit.
- Nếu hiển thị `🚨 FAILED`: Script sẽ chỉ rõ file nào nằm ngoài workspace. Thành viên phải di chuyển file đó vào thư mục workspace của mình trước khi commit.

### Bước 4: Commit và Push lên nhánh cá nhân trên GitHub
```bash
git add workspaces/<tên_workspace>/
git commit -m "feat(<member>): mô tả công việc hoàn thành trong sprint"
git push origin feat/<tên_bạn>
```

---

## 👑 3. Quy Trình Đồng Quy Tri Thức & Merge Dành Cho Leader (Trường)

Vào mỗi buổi họp nhóm hàng tuần (Knowledge Convergence Meeting):

### Bước 1: Kiểm tra tổng thể các nhánh thành viên
Leader chạy script kiểm toán toàn bộ thay đổi của các nhánh:
```bash
# Kiểm tra PR hoặc commit range của thành viên
python scripts/audit_workspace_boundaries.py --commit-range origin/main..origin/feat/duc-baseline-ml --author ducnq
```

### Bước 2: Chọn lọc Artifact xuất sắc nhất (Champion Code / Models)
- Đánh giá mã nguồn trong `workspaces/ducnq/`, `workspaces/vietpmh/`, `workspaces/phuongddd/`.
- Sao chép và chuẩn hóa các module đạt chuẩn sang cây thư mục chính:
  - Baseline ML tốt nhất $\rightarrow$ `src/models/`
  - Preprocessing / Obfuscation $\rightarrow$ `src/preprocessing/`
  - API / Dashboard $\rightarrow$ `src/api/` & `src/dashboard/`
  - Kết quả thực nghiệm $\rightarrow$ `docs/thesis/chapters/`

### Bước 3: Tự động biên dịch Luận văn & Cập nhật Process Report
```bash
# Biên dịch các chương mới vào bản Master Thesis
python scripts/compile_thesis.py

# Cập nhật file Excel tiến độ tuần
python scripts/generate_process_report.py
```

### Bước 4: Commit và Push vào nhánh `main`
```bash
python scripts/audit_workspace_boundaries.py --mode staged
git commit -m "chore(convergence): đồng quy tri thức Tuần X vào src/ và docs/"
git push origin main
```

---

## 🛠️ 4. Xử Lý Xung Đột (Conflict Resolution Protocol)

Do mỗi thành viên sở hữu một thư mục `workspaces/<member>/` tách biệt độc lập:
1. **Xung đột mã nguồn giữa các thành viên = 0%** (vì không ai sửa chung file trong workspace của người khác).
2. Nếu gặp xung đột khi rebase `main` (ví dụ file `requirements.txt` hoặc config):
   - Thành viên giữ nguyên phần thư viện mình cần thêm ở cuối file.
   - Chạy `git add <file>` và `git rebase --continue`.
   - Báo cho Leader trong group chat để Leader hợp nhất trong buổi họp tuần.
