# HƯỚNG DẪN ĐIỀU HƯỚNG & ÁNH XẠ NGƯỢC (REVERSE MAPPING TO REPLICATIONS HUB)

> **Cảnh báo Kiến trúc**: Phân hệ này là **Cổng Báo Cáo Lịch Sử (Historical Milestone Portal)** của Meeting 5.  
> Để phục vụ các nhiệm vụ nghiên cứu tiếp theo (Meeting 6, Meeting 7, Luận văn Chương 4), toàn bộ mã nguồn upstream, dataset, notebook thực nghiệm và model baseline đã được di chuyển và chuẩn hóa tại trung tâm tái lập tập trung:
> 
> 👉 [`workspaces/truongnv/replications/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/)

---

## 🗺️ BẢNG ÁNH XẠ ĐƯỜNG DẪN 1-TO-1 (FORWARD / REVERSE MAPPING TABLE)

| Mã Phân Hệ | Đường Dẫn Lịch Sử (Meeting 5) | Đường Dẫn Chuẩn Hóa Mới (Canonical Hub) | Trạng Thái Mô Hình |
| :--- | :--- | :--- | :---: |
| **Ayub CAMLIS 2024** | [`tasks_for_meeting_5/task_3_replication/Tier1_REJECTED_Ayub_CAMLIS2024/`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/Tier1_REJECTED_Ayub_CAMLIS2024/) | [`replications/Tier1_REJECTED_Ayub_CAMLIS2024/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_REJECTED_Ayub_CAMLIS2024/) | `REJECTED` (Overfitting) |
| **Jain NeurIPS 2023** | [`tasks_for_meeting_5/task_3_replication/Tier1_Candidate_Jain_NeurIPS2023/`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/Tier1_Candidate_Jain_NeurIPS2023/) | [`replications/Tier1_Candidate_Jain_NeurIPS2023/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_Jain_NeurIPS2023/) | `EVALUATED` (Perplexity) |
| **PromptGuard 86M** | [`tasks_for_meeting_5/task_3_replication/Tier1_Candidate_Meta_PromptGuard2024/`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/Tier1_Candidate_Meta_PromptGuard2024/) | [`replications/Tier1_Candidate_Meta_PromptGuard2024/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_Meta_PromptGuard2024/) | `EVALUATED` (Industry SOTA) |
| **InstructDetector** | [`tasks_for_meeting_5/task_3_replication/Tier1_Candidate_InstructDetector_EMNLP2024/`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/Tier1_Candidate_InstructDetector_EMNLP2024/) | [`replications/Tier1_Candidate_InstructDetector_EMNLP2024/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_InstructDetector_EMNLP2024/) | `EVALUATED` (Gradient) |
| **PIGuard ACL 2025** | [`tasks_for_meeting_5/task_3_replication/Tier2_PIGuard_ACL2025/`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/Tier2_PIGuard_ACL2025/) | [`replications/Tier2_PIGuard_ACL2025/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier2_PIGuard_ACL2025/) | **CORE ANCHOR (TIER 2)** |
| **Embeddings Cache** | `task_3_replication/cache/` | [`replications/cache/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/cache/) | `ACTIVE` |
| **Sổ Tay Tái Lập** | `task_3_replication/MEMBER_REPRODUCTION_RUNBOOK.md` | [`replications/MEMBER_REPRODUCTION_RUNBOOK.md`](file:///d:/Work/Do-an/workspaces/truongnv/replications/MEMBER_REPRODUCTION_RUNBOOK.md) | `ACTIVE` |
| **Script Kiểm Định** | `task_3_replication/verify_replication_assets.py` | [`replications/verify_replication_assets.py`](file:///d:/Work/Do-an/workspaces/truongnv/replications/verify_replication_assets.py) | `ACTIVE (100% PASS)` |

---

## 📌 HƯỚNG DẪN IMPORT & TRUY CẬP CHO CÁC TASK TƯƠNG LAI

### 1. Khi viết script trong `tasks_for_meeting_6/` hoặc `src/`:
Tuyệt đối không tham chiếu qua đường dẫn lịch sử `tasks_for_meeting_5/task_3_replication`. Hãy tham chiếu trực tiếp qua `workspaces/truongnv/replications/`:
```python
import sys
from pathlib import Path

# Thêm đường dẫn tới Canonical Replications Hub
REPLICATIONS_DIR = Path(__file__).resolve().parents[3] / "replications"
sys.path.insert(0, str(REPLICATIONS_DIR))

# Ví dụ import mô hình PIGuard ACL 2025
from Tier2_PIGuard_ACL2025.PIGuard_ACL2025.PIGuard import PIGuardModel
```

### 2. Dữ liệu Manifest máy đọc (Machine-Readable Manifest):
Thông tin chi tiết về từng tệp tin và metadata được lưu trữ tại [`backward_mapping.json`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/backward_mapping.json).
