# 🔒 Rule 07: Workspace Boundary Isolation & Team Git Governance

> **Quy định bất biến về cách ly không gian làm việc (Sandbox Isolation), phân quyền chỉnh sửa và thẩm quyền hợp nhất Git độc quyền của Leader**  
> **Cơ chế thực thi**: Tự động kiểm toán qua `python Final-Report/scripts/audit_workspace_boundaries.py` và Git Pre-commit Hook.

---

## 🛡️ 1. PHÂN QUYỀN VÙNG LÀM VIỆC CÁ NHÂN (MEMBER SANDBOX ISOLATION)

1. **Ranh Giới Bất Khả Xâm Phạm**:
   - Thành viên nhóm (Đức, Việt, Phương) **CHỈ ĐƯỢC PHÉP** tạo, sửa, xóa file trong không gian sandbox được chỉ định:
     - Nguyễn Quí Đức: `workspaces/ducnq/`
     - Phạm Minh Hoàng Việt: `workspaces/vietpmh/`
     - Đỗ Đoàn Duy Phương: `workspaces/phuongddd/`
   - Nghiêm cấm tuyệt đối mọi thao tác chỉnh sửa trực tiếp vào các phân hệ chung (`Final-Report/`, `Github-Page/`, `.agents/`, root markdown files) từ nhánh hoặc môi trường làm việc của thành viên.

2. **Agent Scratch Theo Đúng Workspace Thành Viên**:
   - Mỗi agent đặt audit nội bộ, ghi chú, kế hoạch và bản nháp không phải deliverable trong thư mục `.agent-work/` thuộc đúng sandbox được giao; tạo thư mục khi cần.
   - Ánh xạ hiện hành:

     | Người/workspace | Thư mục scratch riêng |
     | --- | --- |
     | Leader Nguyễn Văn Trường | `workspaces/truongnv/.agent-work/` |
     | Nguyễn Quí Đức | `workspaces/ducnq/.agent-work/` |
     | Phạm Minh Hoàng Việt | `workspaces/vietpmh/.agent-work/` |
     | Đỗ Đoàn Duy Phương | `workspaces/phuongddd/.agent-work/` |

   - Không dùng đường dẫn scratch của Leader cho task đang chạy trong workspace thành viên khác; không ghi scratch vào workspace của thành viên khác.
   - Các thư mục này bị ignore bởi quy tắc chung `workspaces/*/.agent-work/` ở root `.gitignore`. Deliverable được task/người dùng yêu cầu vẫn phải được ghi tại đường dẫn deliverable được chỉ định, không đưa vào thư mục ignored.

---

## 👑 2. THẨM QUYỀN HỢP NHẤT ĐỘC QUYỀN CỦA LEADER (LEADER SOLE MERGE AUTHORIZATION)

1. **Quyền Hạn Duy Nhất**: Chỉ Trưởng nhóm Nguyễn Văn Trường (`nvtruongops`) có thẩm quyền hợp nhất (merge/integrate) các kết quả nghiên cứu, mô hình và tài liệu từ các sandbox nhánh cá nhân vào phân hệ chính thức của đề tài (`Final-Report/`, `Github-Page/`).
2. **Quy Trình Hội Tụ Tuần (Weekly Convergence)**:
   - Các thành viên báo cáo tiến độ và demo kết quả trong sandbox cá nhân tại buổi họp tuần.
   - Trưởng nhóm kiểm định chất lượng, rà soát xung đột và thực hiện merge theo đúng quy trình Git chuẩn mực.

---

## 🔍 3. CƠ CHẾ KIỂM TOÁN TỰ ĐỘNG & GIT HOOK

1. **Kiểm Toán Tự Động Trước Khi Commit**:
   - Mọi commit và Pull Request đều được kiểm toán tự động qua:
     `python Final-Report/scripts/audit_workspace_boundaries.py`
   - Bất kỳ vi phạm nào (sửa file ngoài sandbox) sẽ bị chặn ngay lập tức với mã lỗi `EXIT CODE 1`.
2. **Cài Đặt Hook Bắt Buộc**:
   - Mọi thành viên bắt buộc phải chạy `python Final-Report/scripts/validate_local.py --install-hook` sau khi clone repository.
