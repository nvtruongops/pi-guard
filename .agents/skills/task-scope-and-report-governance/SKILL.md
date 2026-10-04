---
name: task-scope-and-report-governance
description: Hướng dẫn Agent phân tích tệp nhiệm vụ, khóa chặt ranh giới In-Scope vs Out-of-Scope, ngăn chặn scope creep và tạo báo cáo tiến độ chuẩn 3 phần bắt buộc.
---

# 🎯 Task-Scope Enclosure & Report Governance Skill

Skill này hướng dẫn AI Agent cách tiếp nhận nhiệm vụ, phân tích tệp chỉ định (Task File), khóa chặt ranh giới (Scope Bounding) và tạo báo cáo chuẩn mực, loại bỏ triệt để hiện tượng ảo giác, viết code sớm hoặc báo cáo out-of-scope.

---

## 📋 QUY TRÌNH 3 BƯỚC BẮT BUỘC KHI THỰC HIỆN NHIỆM VỤ

### Bước 1: Tiếp Nhận & Phân Tích Tệp Nhiệm Vụ (Task Parsing)
Khi người dùng giao nhiệm vụ hoặc chỉ định một tệp nhiệm vụ (ví dụ: `tasks_for_meeting_6/README.md`):
1. **Đọc tệp nhiệm vụ trước tiên**: Tuyệt đối không bắt tay vào viết mã hoặc tạo file khi chưa đọc kỹ tệp nhiệm vụ.
2. **Trích xuất các yêu cầu cụ thể**: Lập danh sách các đầu mục bàn giao bắt buộc (Deliverables).
3. **Đối chiếu danh mục Deprecations**: Đọc [Rule 02](file:///d:/Work/Do-an/.agents/rules/rule-02-task-scope-and-milestone-enclosure.md), Mục 4, để biết các công nghệ/từ khóa ngoài phạm vi (như INT8, ONNX, ZeroQuant).

### Bước 2: Thiết Lập Bảng Ranh Giới (Scope Boundary Table)
Trước khi thực hiện, Agent phải tự xác định ranh giới trong tâm thức:
- **IN-SCOPE**: Đúng các câu hỏi và thực nghiệm mà task yêu cầu (ví dụ: Task 4 là đo đạc các baseline y văn công khai).
- **OUT-OF-SCOPE**:
  - Không viết code mô hình của nhóm (`src/models/cascade/`) khi đang ở Chapter 2.
  - Không đưa ra kết quả nghiệm thu của Chapter 3/4.
  - Không đưa lại các công nghệ đã bị loại trừ.

### Bước 3: Soạn Thảo Báo Cáo Chuẩn Mẫu (Standard Report Authoring)
Mọi báo cáo nhiệm vụ phải tuân thủ nghiêm ngặt mẫu template tại:
[`templates/TASK_COMPLIANCE_REPORT_TEMPLATE.md`](file:///d:/Work/Do-an/.agents/skills/task-scope-and-report-governance/templates/TASK_COMPLIANCE_REPORT_TEMPLATE.md)

---

## 📝 CẤU TRÚC 3 PHẦN BẮT BUỘC CỦA BÁO CÁO NHIỆM VỤ

1. **Phần 1: Tuyên Bố Ranh Giới Nhiệm Vụ (Scope Boundary Declaration)**:
   - Ghi rõ tệp task nguồn và milestone.
   - Bảng phân định rõ ràng In-Scope vs. Out-of-Scope.
2. **Phần 2: Bàn Giao Kết Quả Theo Nhiệm Vụ (Empirical Deliverables)**:
   - Bám sát từng yêu cầu, trình bày súc tích.
   - 100% số liệu phải trích dẫn từ tệp JSON un-mocked tương ứng trong `04_benchmarks_and_data/`.
3. **Phần 3: Bảng Kiểm Tra Tuân Thủ Phạm Vi (Scope Compliance Checklist)**:
   - Bảng xác nhận 0% vi phạm deprecations, 0% mô hình tự tạo sớm, 0% số liệu giả mạo.
