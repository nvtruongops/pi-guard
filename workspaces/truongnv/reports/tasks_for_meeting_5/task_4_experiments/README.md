# **THỰC NGHIỆM ĐỘNG LỰC KHOA HỌC CHO NHIỆM VỤ 4 (TASK 4 EXPERIMENTAL PoC)**
## ĐỀ TÀI: A MACHINE-LEARNING GUARDRAIL FOR DETECTING PROMPT INJECTION AND JAILBREAK ATTACKS ON LLM APPLICATIONS (PI-GUARD)
**Căn cứ báo cáo**: [`workspaces/truongnv/reports/tasks_for_meeting_5/TASK_4_PIGUARD_IMPROVEMENTS.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/TASK_4_PIGUARD_IMPROVEMENTS.md)

---

Thư mục này chứa mã nguồn thực nghiệm PoC độc lập nhằm **chứng minh động lực khoa học và tính tất yếu** của các giải pháp cải tiến được đề xuất trong Task 4:

| Tệp Script | Mục Tiêu Kỹ Thuật | Vai Trò Trong Báo Cáo Task 4 |
| :--- | :--- | :--- |
| [`run_two_tier_routing_poc.py`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_4_experiments/run_two_tier_routing_poc.py) | Đo đạc sự đánh đổi giữa Tốc độ của TF-IDF và Năng lực ngữ nghĩa của DeBERTa-v3 trên tập kiểm thử Over-defense. | **Minh chứng thực nghiệm cho Cải tiến 3 (Two-Tier Routing) và Cải tiến 4 (ZeroQuant INT8)**: Chứng minh TF-IDF tuy nhanh (<10ms) nhưng chặn oan 40% câu NotInject; DeBERTa-v3 giải quyết được (88.3%) nhưng cồng kềnh (500MB, 42.5ms). Do đó cần phối hợp cả hai! |

### Lệnh thực thi:
```powershell
python workspaces/truongnv/reports/tasks_for_meeting_5/task_4_experiments/run_two_tier_routing_poc.py
```
