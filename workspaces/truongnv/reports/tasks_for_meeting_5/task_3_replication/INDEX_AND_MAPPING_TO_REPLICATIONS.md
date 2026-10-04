# HƯỚNG DẪN ĐIỀU HƯỚNG & ÁNH XẠ NGƯỢC (REVERSE MAPPING TO REPLICATIONS HUB)

> **Cảnh báo kiến trúc (cập nhật 30/09/2026):** đây là cổng lịch sử Meeting 5. Gói đủ điều kiện làm ứng viên so sánh được giữ trong `replications/`; các model/method chỉ phù hợp làm tài liệu tham khảo đã chuyển sang `references_study/`. Không còn một trung tâm duy nhất chứa tất cả gói.
> 
> 👉 [`workspaces/truongnv/replications/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/)

---

## 🗺️ BẢNG ÁNH XẠ ĐƯỜNG DẪN 1-TO-1 (FORWARD / REVERSE MAPPING TABLE)

| Mã Phân Hệ | Đường Dẫn Lịch Sử (Meeting 5) | Đường Dẫn Hiện Hành | Trạng Thái Mô Hình |
| :--- | :--- | :--- | :---: |
| **Ayub CAMLIS 2024** | Legacy Meeting 5 source was not present in this archive at audit time | [`references_study/rejected_baselines/Tier1_REJECTED_Ayub_CAMLIS2024/`](file:///d:/Work/Do-an/workspaces/truongnv/references_study/rejected_baselines/Tier1_REJECTED_Ayub_CAMLIS2024/) | `REFERENCE/PILOT`; see source-backed scope before reporting |
| **Jain NeurIPS 2023** | Legacy candidate folder removed; its generated pilot evidence was withdrawn | [`references_study/local_pilots/Tier1_Candidate_Jain_NeurIPS2023/`](file:///d:/Work/Do-an/workspaces/truongnv/references_study/local_pilots/Tier1_Candidate_Jain_NeurIPS2023/) | `REFERENCE ONLY`; former project TF-IDF is not a Jain reproduction |
| **Prompt Guard 86M** | Hồ sơ candidate Meeting 5 đã rút | [`replications/Tier1_Candidate_Meta_PromptGuard2024/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_Meta_PromptGuard2024/) | `WITHDRAWN`; project-authored proxy and unverified dataset removed; no inference/result |
| **InstructDetector** | Legacy candidate folder removed; local generated probe/evaluation evidence was withdrawn | [`references_study/white_box_methods/Tier1_Candidate_InstructDetector_EMNLP2024/`](file:///d:/Work/Do-an/workspaces/truongnv/references_study/white_box_methods/Tier1_Candidate_InstructDetector_EMNLP2024/) | `REFERENCE ONLY`; method requires internal hidden-state/gradient access |
| **PIGuard (Hao Li ACL 2025)** | [`tasks_for_meeting_5/task_3_replication/`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/) | [`replications/Paper_ACL2025_PIGuard_HaoLi/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Paper_ACL2025_PIGuard_HaoLi/) | Public code/data/checkpoint inference candidate; no retraining claim |
| **Embeddings Cache** | `task_3_replication/cache/` | Removed with unsupported Ayub training/result artifacts | `WITHDRAWN`; no active cache or runner |
| **Sổ Tay Tái Lập** | `task_3_replication/MEMBER_REPRODUCTION_RUNBOOK.md` | [`replications/MEMBER_REPRODUCTION_RUNBOOK.md`](file:///d:/Work/Do-an/workspaces/truongnv/replications/MEMBER_REPRODUCTION_RUNBOOK.md) | `ACTIVE` |
| **Script Kiểm Định** | `task_3_replication/verify_replication_assets.py` | [`replications/verify_replication_assets.py`](file:///d:/Work/Do-an/workspaces/truongnv/replications/verify_replication_assets.py) | `ACTIVE`; verifies local integrity and cleanup state only |

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

# Ví dụ import mô hình PIGuard ACL 2025 của Hao Li et al.
from Paper_ACL2025_PIGuard_HaoLi.PIGuard_ACL2025.PIGuard import PIGuardModel
```

### 2. Manifest dữ liệu hiện hành
Danh sách dữ liệu giữ lại, hash và nguồn chuẩn được kiểm tra bởi `replications/verify_replication_assets.py` và các manifest riêng của từng benchmark. Manifest lịch sử Meeting 5 đã rút khỏi sử dụng.
