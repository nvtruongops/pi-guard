# **THƯ MỤC MÃ NGUỒN KIỂM ĐỊNH Y VĂN TASK 3 (TASK 3 AUDIT SCRIPTS)**
## ĐỀ TÀI: A MACHINE-LEARNING GUARDRAIL FOR DETECTING PROMPT INJECTION AND JAILBREAK ATTACKS ON LLM APPLICATIONS (PI-GUARD)
**Cổng điều phối chuyên đề**: [`workspaces/truongnv/reports/tasks_for_meeting_5/task_3_reproducibility/README.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_reproducibility/README.md)

---

Thư mục này chứa các script Python phục vụ mục tiêu duy nhất của Task 3: **Kiểm định và thẩm định tính sẵn sàng công khai của Bộ ba [Paper + Code + Dataset] cho 2 bài báo tham khảo**:

| STT | Tên Tệp Script | Chức Năng Kỹ Thuật | Lệnh Thực Thi |
| :---: | :--- | :--- | :--- |
| **1** | [`verify_meeting4_papers.py`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_reproducibility/scripts/verify_meeting4_papers.py) | Kiểm định trực tiếp qua HTTP API tính sẵn sàng của Bộ ba [Paper + Code + Dataset] cho cả 2 bài báo tham khảo: Ayub & Majumdar (CAMLIS 2024) và Hao Li et al. (ACL 2025). | `python workspaces/truongnv/reports/tasks_for_meeting_5/task_3_reproducibility/scripts/verify_meeting4_papers.py` |
| **2** | [`verify_piguard_paper_triad.py`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_reproducibility/scripts/verify_piguard_paper_triad.py) | Kiểm định chuyên sâu cấu trúc bên trong repo `leolee99/PIGuard`: xác thực sự tồn tại của `train.py`, `eval_hf.py`, `datasets/NotInject_one.json`, và checkpoint Hugging Face. | `python workspaces/truongnv/reports/tasks_for_meeting_5/task_3_reproducibility/scripts/verify_piguard_paper_triad.py` |

---

> [!NOTE]
> Để thực hiện chạy tái lập thực nghiệm (chạy mô hình thật), từng thành viên làm theo đúng hướng dẫn trong sổ tay:  
> 👉 [`../04_MEMBER_REPRODUCTION_RUNBOOK.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_reproducibility/04_MEMBER_REPRODUCTION_RUNBOOK.md) (Clone repo và chạy `eval_hf.py` của PIGuard hoặc `binary_classification.py` của Ayub).
