# **BÁO CÁO ĐIỀU HƯỚNG & THAM CHIẾU NHIỆM VỤ 3 (TASK 3 MASTER REFERRAL)**
## ĐỀ TÀI: A MACHINE-LEARNING GUARDRAIL FOR DETECTING PROMPT INJECTION AND JAILBREAK ATTACKS ON LLM APPLICATIONS (PI-GUARD)
### Báo Cáo Điều Hướng: Khảo Sát Tái Lập Học Thuật, Thẩm Định Bộ Ba [Paper + Code + Dataset] Cho 2 Bài Báo Tham Khảo
**Tác giả**: Nguyễn Văn Trường (Leader — MSSV: `SE182034`) | **Workspace**: `workspaces/truongnv/`  
**Căn cứ chỉ đạo**: Biên bản họp GVHD Trần Văn Ninh [`Final-Report/Meeting/Meeting 4_10_09_26.md`](file:///d:/Work/Do-an/Final-Report/Meeting/Meeting%204_10_09_26.md)  
**Thư mục chuyên đề chi tiết**: [`task_3_reproducibility/`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_reproducibility/README.md)

---

> [!IMPORTANT]
> ### ⚡ 4 NGUYÊN TẮC CỐT LÕI CỦA TASK 3 TỪ GVHD TRẦN VĂN NINH
> 1. **Bản chất Task 3 là Tái lập Y văn Tham khảo (Pure Literature Replication)**:
>    - Nhiệm vụ này tập trung 100% vào việc: **Khảo sát, tải về và chạy thực nghiệm tái lập 2 bài báo tham khảo đã xuất bản có đầy đủ Bộ ba [Paper + Code + Dataset] công khai**.
>    - Nhóm tải đúng mã nguồn và dữ liệu của tác giả về máy cá nhân, chạy lệnh đánh giá của tác giả để nắm chắc siêu tham số trước Meeting 5.
> 2. **Xác lập 2 Bài báo Tham khảo phục vụ Tái lập**:
>    - **Mô hình Tham khảo 1 (Baseline)**: Ayub & Majumdar (CAMLIS 2024 [[1]](#ref1)) — Mô hình học máy nhẹ nhúng câu MiniLM + Random Forest / XGBoost (GitHub + 467k mẫu dữ liệu Hugging Face).
>    - **Mô hình Tham khảo 2 (SOTA Anchor)**: Hao Li et al. (ACL 2025 Long Paper [[2]](#ref2)) — PIGuard DeBERTa-v3 (GitHub + benchmark NotInject đóng gói sẵn + pre-trained checkpoint).
> 3. **Ranh giới dứt khoát giữa Task 3 và Task 4**:
>    - **Task 3**: Chỉ tải và chạy 2 mô hình tham khảo để tái lập kết quả của tác giả.
>    - **Task 4**: Mới là nơi phân tích sự đánh đổi, giải thích lý do không dùng TF-IDF đơn lẻ và đề xuất 4 giải pháp cải tiến mới của đồ án (xem tại [`TASK_4_PIGUARD_IMPROVEMENTS.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/TASK_4_PIGUARD_IMPROVEMENTS.md)).
> 4. **Tách biệt ranh giới dữ liệu**: Tập dữ liệu đăng ký trong [`CAPSTONE PROJECT REGISTER.md`](file:///d:/Work/Do-an/CAPSTONE%20PROJECT%20REGISTER.md) thuộc về giai đoạn huấn luyện mô hình đồ án sau này (Review 2). Không tải lan man các dataset ngoài trong Task 3.

---

## 🧭 MA TRẬN THAM CHIẾU HỒ SƠ CHUYÊN ĐỀ `task_3_reproducibility/`

Toàn bộ tài liệu bóc tách chi tiết và mã nguồn kiểm định được chuẩn hóa thành 4 chuyên đề độc lập trong thư mục [`task_3_reproducibility/`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_reproducibility/README.md):

| STT | Hồ Sơ Chuyên Đề | Tệp Tham Chiếu Trực Tiếp | Trọng Tâm Báo Cáo Kỹ Thuật Task 3 |
| :---: | :--- | :--- | :--- |
| **01** | **Thực Trạng Y Văn TF-IDF** | [`01_LITERATURE_ASSESSMENT_TFIDF.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_reproducibility/01_LITERATURE_ASSESSMENT_TFIDF.md) | Lý giải vì sao không có repo độc lập cho TF-IDF; mổ xẻ nghiên cứu Intel Labs (arXiv:2512.19011 [[5]](#ref5)) về độ trễ $<1\text{ms}$ CPU và ưu thế +26% F1 khi gặp xáo trộn ký tự. |
| **02** | **Thẩm Định Mỏ Neo PIGuard** | [`02_CORE_ANCHOR_PIGUARD_ACL2025.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_reproducibility/02_CORE_ANCHOR_PIGUARD_ACL2025.md) | Thẩm định bộ ba [Paper + Code + Dataset + Checkpoint] của PIGuard (ACL 2025 [[2]](#ref2)); bóc tách DeBERTa-v3, cơ chế MOF, tập NotInject đóng gói sẵn và cấu hình siêu tham số (`lr=2e-5`, `batch=32`). |
| **03** | **Baseline Nhúng Câu Ayub** | [`03_EMBEDDING_BASELINE_AYUB2024.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_reproducibility/03_EMBEDDING_BASELINE_AYUB2024.md) | Khảo sát mô hình Baseline MiniLM + ML cổ điển (CAMLIS 2024 [[1]](#ref1)); repo GitHub `malicious-prompt-detection` và 467k mẫu dữ liệu mở trên Hugging Face. |
| **04** | **Sổ Tay Chạy Tái Lập** | [`04_MEMBER_REPRODUCTION_RUNBOOK.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_reproducibility/04_MEMBER_REPRODUCTION_RUNBOOK.md) | Sổ tay hướng dẫn từng bước lệnh PowerShell copy-paste cho 4 thành viên clone repo và chạy lệnh đánh giá của tác giả trên máy cá nhân trước Meeting 5. |
| **📁** | **Mã Nguồn Kiểm Định Y Văn** | [`scripts/README.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_reproducibility/scripts/README.md) | Bộ script tự động kiểm định tính sẵn sàng công khai HTTP của 2 bài báo qua [`verify_meeting4_papers.py`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_reproducibility/scripts/verify_meeting4_papers.py) và [`verify_piguard_paper_triad.py`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_reproducibility/scripts/verify_piguard_paper_triad.py). |

---

## 📊 BẢNG ĐỐI CHUẨN 2 MÔ HÌNH THAM KHẢO GỐC (REFERENCE MODELS SCORECARD)

Bảng đối chiếu thông số công bố và tính khả thi tái lập của 2 mô hình tham khảo phục vụ báo cáo Thầy Ninh:

| Tiêu Chí Đối Chuẩn | Mô Hình Tham Khảo 1: Ayub & Majumdar (CAMLIS 2024 [[1]](#ref1)) | Mô Hình Tham Khảo 2: PIGuard DeBERTa-v3 (ACL 2025 [[2]](#ref2)) |
| :--- | :--- | :--- |
| **Bản chất kiến trúc** | Sentence Embedding (`all-MiniLM-L6-v2`, 384d) + Random Forest / XGBoost | Deep Transformer Disentangled Attention (`microsoft/deberta-v3-base`, 86M params) |
| **Trạng thái Mã nguồn (Code)** | Công khai: [GitHub AhsanAyub/malicious-prompt-detection](https://github.com/AhsanAyub/malicious-prompt-detection) (`200 OK`) | Công khai: [GitHub leolee99/PIGuard](https://github.com/leolee99/PIGuard) (`200 OK`) |
| **Trạng thái Dữ liệu (Dataset)** | Công khai: [Hugging Face ahsanayub/malicious-prompts](https://huggingface.co/datasets/ahsanayub/malicious-prompts) (467k mẫu) | Công khai: Đóng gói sẵn trong repo tại thư mục `datasets/` (`NotInject`, `BIPIA`, `train.json`) |
| **Trạng thái Trọng số (Weights)** | Trọng số mở Hugging Face cho `all-MiniLM-L6-v2` | Checkpoint mở trên Hugging Face: [leolee99/PIGuard](https://huggingface.co/leolee99/PIGuard) (`200 OK`) |
| **Độ chính xác công bố (Reported)** | **Accuracy 99.4%**, **F1-Score 0.987** trên tập kiểm thử 467k | **Detection 98.7%**, **NotInject Accuracy 88.3%** (Chống Over-defense) |
| **Lệnh chạy tái lập trên máy cá nhân** | `python binary_classification.py` (chạy trên CPU) | `python eval_hf.py --dataset_root datasets` (chạy trên CPU) |

> 📌 **Ghi chú chuyển giao sang Task 4**:  
> Việc so sánh chuyên sâu sự đánh đổi giữa TF-IDF và DeBERTa-v3 để trả lời câu hỏi *"Tại sao không dùng luôn TF-IDF cho nhẹ?"* cùng thực nghiệm PoC định tuyến phân tầng được trình bày độc lập tại:  
> 👉 [`TASK_4_PIGUARD_IMPROVEMENTS.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/TASK_4_PIGUARD_IMPROVEMENTS.md) & mã nguồn PoC: [`task_4_experiments/run_two_tier_routing_poc.py`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_4_experiments/run_two_tier_routing_poc.py).

---

## 🚀 HƯỚNG DẪN THỰC THI NHANH CHO THÀNH VIÊN TRƯỚC MEETING 5
Để clone repo và chạy lệnh đánh giá tái lập 2 bài báo trên máy cá nhân, thành viên thực hiện theo hướng dẫn:  
👉 [`task_3_reproducibility/04_MEMBER_REPRODUCTION_RUNBOOK.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_reproducibility/04_MEMBER_REPRODUCTION_RUNBOOK.md)

---

## 📚 TÀI LIỆU THAM KHẢO HỌC THUẬT (REFERENCES)

<a id="ref1"></a>
- **[[1]]** M. A. Ayub and S. Majumdar, "Embedding-based classifiers can detect prompt injection attacks," in *Proc. CAMLIS 2024*, Arlington, VA, USA, Oct. 2024. [arXiv:2410.22284](https://arxiv.org/pdf/2410.22284).

<a id="ref2"></a>
- **[[2]]** H. Li, X. Liu, N. Zhang, and C. Xiao, "PIGuard: Prompt Injection Guardrail via Mitigating Overdefense for Free," in *Proc. ACL 2025*, Vienna, Austria, 2025. [arXiv:2410.22770](https://arxiv.org/pdf/2410.22770) | [ACL Anthology](https://aclanthology.org/2025.acl-long.1468.pdf).

<a id="ref4"></a>
- **[[4]]** P. He, J. Gao, and W. Chen, "DeBERTaV3: Improving DeBERTa using ELECTRA-Style Pre-Training with Gradient-Disentangled Embedding Sharing," in *Proc. ICLR 2023*, Kigali, Rwanda, 2023. [arXiv:2111.09543](https://arxiv.org/pdf/2111.09543).

<a id="ref5"></a>
- **[[5]]** V. Majhi et al., "Do You Really Need a GPU to Guard Your LLM? CPU-Class Classifiers and Multi-Stage Pipelines for Safety Enforcement at Scale," *arXiv preprint arXiv:2512.19011*, Dec. 2025. [arXiv:2512.19011](https://arxiv.org/pdf/2512.19011).
