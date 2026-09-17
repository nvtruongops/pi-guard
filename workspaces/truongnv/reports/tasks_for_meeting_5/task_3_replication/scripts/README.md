# **THƯ MỤC MÃ NGUỒN KIỂM ĐỊNH Y VĂN TASK 3 (TASK 3 AUDIT SCRIPTS)**
## ĐỀ TÀI: A MACHINE-LEARNING GUARDRAIL FOR DETECTING PROMPT INJECTION AND JAILBREAK ATTACKS ON LLM APPLICATIONS (PI-GUARD)
**Cổng điều phối phòng thí nghiệm**: [`workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/README.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/README.md)

---

Thư mục này chứa các script Python phục vụ kiểm định và thẩm định tính sẵn sàng công khai của Bộ ba [Paper + Code + Dataset] cho 2 bài báo tham khảo: Ayub & Majumdar (CAMLIS 2024) [[18]](#ref18) và Hao Li et al. (ACL 2025) [[1]](#ref1):

<div align="center">

![Bằng chứng xác thực Bộ ba Công Khai PIGuard ACL 2025](../Tier2_PIGuard_ACL2025/figures/01_paper_evidence/paper_p1_title_and_abstract.png)
*Hình 1: Tiêu đề và tóm tắt bài báo mỏ neo PIGuard ACL 2025 (Hao Li et al.) được thẩm định qua script.*

</div>

| STT | Tên Tệp Script | Chức Năng Kỹ Thuật | Lệnh Thực Thi |
| :---: | :--- | :--- | :--- |
| **1** | [`verify_meeting4_papers.py`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/scripts/verify_meeting4_papers.py) | Kiểm định trực tiếp qua HTTP API tính sẵn sàng của Bộ ba [Paper + Code + Dataset] cho cả 2 bài báo tham khảo: Ayub & Majumdar (CAMLIS 2024) [[18]](#ref18) và Hao Li et al. (ACL 2025) [[1]](#ref1). | `python workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/scripts/verify_meeting4_papers.py` |
| **2** | [`verify_piguard_paper_triad.py`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/scripts/verify_piguard_paper_triad.py) | Kiểm định chuyên sâu cấu trúc bên trong repo `leolee99/PIGuard`: xác thực sự tồn tại của `train.py`, `eval_hf.py`, `datasets/NotInject_one.json`, và checkpoint Hugging Face. | `python workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/scripts/verify_piguard_paper_triad.py` |

---

> [!NOTE]
> Để thực hiện chạy tái lập thực nghiệm (chạy mô hình thật), từng thành viên làm theo đúng hướng dẫn trong sổ tay:  
> 👉 [`../MEMBER_REPRODUCTION_RUNBOOK.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/MEMBER_REPRODUCTION_RUNBOOK.md) (Clone repo và chạy `eval_hf.py` của PIGuard hoặc `binary_classification.py` của Ayub).

---

## 📚 Tài Liệu Tham Khảo (References)

* <a id="ref1"></a>**[1]** Hao Li, Xiaogeng Liu, Ning Zhang, and Chaowei Xiao. 2025. *PIGuard: Prompt Injection Guardrail via Mitigating Overdefense for Free*. In *Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (ACL 2025 - Long Paper)*. [arXiv:2410.22770 [cs.CR]](https://arxiv.org/abs/2410.22770). Open-Access PDF: [`../Tier2_PIGuard_ACL2025/papers/PIGuard_ACL2025_arXiv2410.22770.pdf`](../Tier2_PIGuard_ACL2025/papers/PIGuard_ACL2025_arXiv2410.22770.pdf).
* <a id="ref18"></a>**[18]** Md Rayhanur Rahman Ayub and Adrish Majumdar. 2024. *Embedding-based classifiers can detect prompt injection attacks*. In *Proceedings of the Conference on Applied Machine Learning for Information Security (CAMLIS 2024)*, Arlington, VA, USA. [arXiv:2410.22284 [cs.CR]](https://arxiv.org/abs/2410.22284). Open-Access PDF: [`../Tier1_REJECTED_Ayub_CAMLIS2024/papers/Ayub_CAMLIS2024_arXiv2410.22284.pdf`](../Tier1_REJECTED_Ayub_CAMLIS2024/papers/Ayub_CAMLIS2024_arXiv2410.22284.pdf).
