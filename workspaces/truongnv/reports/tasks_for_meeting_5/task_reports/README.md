# HỒ SƠ CHUYÊN ĐỀ KỸ THUẬT CHI TIẾT — MEETING 5
**Workspace**: [`workspaces/truongnv/reports/tasks_for_meeting_5/task_reports/`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_reports/)  
👉 **Báo cáo tổng hợp**: [`../README.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/README.md)

> Trước buổi họp tuần sau (Meeting 5), cả 4 thành viên bắt buộc phải chạy độc lập được 2 mô hình tham khảo cho mô hình đồ án trên máy cá nhân và có số liệu thực nghiệm cụ thể!

---

## 📑 DANH MỤC 4 BÁO CÁO KỸ THUẬT CỐT LÕI

| STT | Tên Nhiệm Vụ | Tệp Báo Cáo Chi Tiết | Trọng Tâm Nghiên Cứu & Đóng Góp Học Thuật |
| :---: | :--- | :--- | :--- |
| **1** | **Nhiệm vụ 1: Giới thiệu 2 Key Đồ Án** | [`TASK_1_PROMPT_INJECTION_VS_JAILBREAK.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_reports/TASK_1_PROMPT_INJECTION_VS_JAILBREAK.md) | Phân biệt bản chất 2 đối tượng nghiên cứu: Prompt Injection ($X = S \mathbin{\Vert} U$ phá vỡ ranh giới phẳng ứng dụng) vs. Jailbreak (phá vỡ căn chỉnh an toàn nội tại $\theta$); xác lập 4 yêu cầu kỹ thuật tối thượng (REQ-1..4). |
| **2** | **Nhiệm vụ 2: Cách Hoạt Động & Kết Quả Bị Tấn Công Của 2 Key** | [`TASK_2_ATTACK_VECTORS_AND_MODELS.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_reports/TASK_2_ATTACK_VECTORS_AND_MODELS.md) | Khung phân tích bề mặt tấn công 5 trục; luồng hoạt động chi tiết của Kênh 1 (Direct Chat) và Kênh 2 (Indirect File/RAG); dấu vết nhận diện (Footprint), chu trình dữ liệu và bán kính thiệt hại (Blast Radius). |
| **3** | **Nhiệm vụ 3: Chạy Thực Nghiệm Mô Hình Public Không Thêm Bớt Gì** | [`TASK_3_REPRODUCIBILITY_AND_DATASETS.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_reports/TASK_3_REPRODUCIBILITY_AND_DATASETS.md) | **Tái lập y văn thuần túy**: Chạy nguyên bản 100% mã nguồn và trọng số của 5 mô hình y văn công khai (PIGuard ACL 2025, Ayub CAMLIS 2024, Meta Prompt-Guard 86M, Jain NeurIPS 2023, InstructDetector EMNLP 2024), không can thiệp code riêng, đo đạc trên 5 benchmark mở. |
| **4** | **Nhiệm vụ 4: Mô Hình Đồ Án Có Thể Dùng Thế Nào Từ Thực Nghiệm Task 3** | [`TASK_4_PIGUARD_IMPROVEMENTS.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_reports/TASK_4_PIGUARD_IMPROVEMENTS.md) | **Kiến trúc đề xuất PI-Guard**: Two-Tier Cascaded (Tầng 1 TF-IDF $\le 0.5\text{ms}$ lọc $82.6\%$ lưu lượng + Tầng 2 DeBERTa-v3 MOF INT8 $18.5\text{ms}$ thẩm định vùng bất định), đưa độ trễ kỳ vọng về $3.69\text{ms}$, bảo toàn F1 $0.9416$, cùng 4 cải tiến độc quyền. |

---

### 📚 HỒ SƠ CHUYÊN ĐỀ BỔ TRỢ & CHUYÊN KHẢO KHOA HỌC (SUPPORTING TECHNICAL MONOGRAPHS)

| Mã Tài Liệu | Tên Chuyên Đề Bổ Trợ | Tệp Chi Tiết | Vai Trò Học Thuật |
| :---: | :--- | :--- | :--- |
| **MONO-2.5** | **Đánh Giá Toàn Diện SOTA & Ranh Giới Nghiên Cứu** | [`TASK_2_5_SOTA_ASSESSMENT_AND_TWO_TIER_PROPOSAL.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_reports/TASK_2_5_SOTA_ASSESSMENT_AND_TWO_TIER_PROPOSAL.md) | Cung cấp bằng chứng y văn quốc tế cho 6 trường phái SOTA (Llama Guard 3 8B, NeMo, Lakera, Prompt-Guard từ ACL 2025), chứng minh Thế lưỡng nan Pareto, và phân tích 6 khoảng trống phương pháp luận cốt tử nhằm bổ trợ cơ sở lý luận vững chắc cho Nhiệm vụ 4. |
| **SUPP-01** | **Cơ Chế Tính Điểm Tầng 1: Mô Hình Hóa Toán Học & Lý Thuyết Rủi Ro Bayes** | [`supplementary/TIER1_SCORING_MATHEMATICAL_FORMULATION_AND_BAYES_RISK.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_reports/supplementary/TIER1_SCORING_MATHEMATICAL_FORMULATION_AND_BAYES_RISK.md) | Chuyên khảo kỹ thuật chuyên sâu về công thức toán học vector thưa CSR, hiệu chuẩn Platt Scaling, lý thuyết quyết định Bayes nhạy cảm chi phí giải thích ngưỡng $[0.15, 0.85]$, 3 ví dụ tính toán số học từng bước cho 3 Key, và phân định ranh giới kiến trúc Tầng Ứng Dụng vs. External Guardrail Proxy (Springer 2026). Tránh làm phình to phạm vi (Scope Creep) của Task 4. |
| **SUPP-02** | **Chuyên Khảo Khoa Học: Khảo Sát Toàn Diện 4 Trường Phái Jailbreak (Taxonomy), Mổ Xẻ Dòng Họ DAN, 10 Ca Điển Hình & Khung Đánh Chặn Phân Tầng** | [`supplementary/JAILBREAK_TAXONOMY_CASE_STUDIES_AND_DEFENSE.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_reports/supplementary/JAILBREAK_TAXONOMY_CASE_STUDIES_AND_DEFENSE.md) | Khảo sát hệ thống 4 trường phái Jailbreak lớn (Persona/Roleplay, Automated/Gradient GCG, Obfuscation/Ciphers, Context Saturation Many-Shot); Mổ xẻ chi tiết 10 case studies thực tế kèm cấu trúc prompt nguyên bản; Tích hợp toàn diện chuyên khảo cơ chế hoạt động của archetype Jailbreak DAN kinh điển (Shen et al. ACM CCS 2024, 1.405 prompt in-the-wild, 11 quần thể tiến hóa 4 thế hệ); Đánh giá thất bại của OpenAI Moderation & NeMo-Guardrails; Cơ sở toán học Competing Objectives & Mismatched Generalization (Wei et al. NeurIPS 2023) và hàm mất mát đối kháng GCG; và Thiết kế phòng thủ phân tầng của PI-Guard (Heuristic Scrubber + Dual-Space TF-IDF N-Grams $\le 0.4\text{ms}$ + DeBERTa-v3 MOF + Group-Aware Splitting MD5). |
| **SUPP-03** | **Chiếm Quyền Điều Khiển Luồng Ứng Dụng ($X = S \mathbin{\Vert} U$), Không Gian Token Phẳng & Giải Pháp Guardrail Ngoại Vi** | [`supplementary/CONTROL_FLOW_HIJACKING_AND_FLAT_TOKEN_SPACE.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_reports/supplementary/CONTROL_FLOW_HIJACKING_AND_FLAT_TOKEN_SPACE.md) | Chuyên khảo kỹ thuật chuyên sâu mổ xẻ nguyên nhân gốc rễ của Prompt Injection: Không gian token phẳng (Flat Token Space) và hiện tượng chiếm đoạt ma trận Attention; Phân tích 3 phép đối sánh khoa học máy tính kinh điển (Kiến trúc Von Neumann & Tràn bộ đệm, SQL Injection vs. Prepared Statements, Phân quyền trang bộ nhớ NX-bit); 3 kịch bản thực tế sản xuất minh họa kèm chu trình dữ liệu và bán kính thiệt hại; Thiết lập định vị PI-Guard như giải pháp Prepared Statements cho kỷ nguyên LLM theo nguyên lý Complete Mediation (Saltzer & Schroeder 1975). |
| **SUPP-04** | **Đánh Giá Thực Trạng Y Văn Về Mô Hình TF-IDF Trong Nghiên Cứu Guardrail** | [`supplementary/LITERATURE_ASSESSMENT_TFIDF.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_reports/supplementary/LITERATURE_ASSESSMENT_TFIDF.md) | Phân tích bản chất học thuật của TF-IDF trong an toàn thông tin; mổ xẻ nghiên cứu Intel Labs (arXiv:2512.19011 [[5]](#ref5), 12/2025) về độ trễ $<1\text{ms}$ CPU và ưu thế $+26\%$ F1 khi gặp xáo trộn ký tự; ảnh minh chứng từ bài báo Neel Jain (NeurIPS 2023 [[6]](#ref6)) và đường cong suy giảm từ khóa; lý giải tại sao không có repo GitHub riêng cho TF-IDF. |
| **SUPP-05** | **Thẩm Định Toàn Diện Bài Báo Mỏ Neo Gốc PIGuard (ACL 2025) & Báo Cáo Đối Chuẩn Độc Lập** | [`supplementary/CORE_ANCHOR_PIGUARD_ACL2025.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_reports/supplementary/CORE_ANCHOR_PIGUARD_ACL2025.md) | Thẩm định toàn diện bài báo mỏ neo gốc PIGuard (Hao Li et al. ACL 2025 Long Paper [[2]](#ref2)); xác thực bộ ba công khai 100% [Paper + Code + Data + Weights]; bóc tách kiến trúc DeBERTa-v3 86M, Disentangled Attention, cơ chế MOF và tập NotInject; Báo cáo đối chuẩn độc lập 6 chiều giải trình chi tiết lý do chọn PIGuard làm mỏ neo Tầng 2 mà loại bỏ Prompt-Guard, Llama Guard 3, Ayub, Jain và InstructDetector. |
| **SUPP-06** | **Báo Cáo Thực Nghiệm Đối Chuẩn & Hồ Sơ Loại Bỏ Baseline Nhúng Câu (Ayub & Majumdar, CAMLIS 2024)** | [`supplementary/REJECTED_BASELINE_AYUB_CAMLIS2024.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_reports/supplementary/REJECTED_BASELINE_AYUB_CAMLIS2024.md) | Báo cáo thực nghiệm đối chuẩn & hồ sơ loại bỏ baseline nhúng câu (Ayub & Majumdar, CAMLIS 2024 [[1]](#ref1)); phân tích điểm nghẽn Overdefense FPR $58.41\%$ trên NotInject và độ trễ trích xuất vector $11.02\text{ms}$ CPU của MiniLM; so sánh đối chuẩn chi tiết với TF-IDF. |

![Bảng điểm tổng hợp đối soát y văn gốc và thực nghiệm độc lập](../task_3_replication/Tier2_PIGuard_ACL2025/figures/02_empirical_plots/local_vs_paper_scorecard.png)
*Hình: Bảng điểm tổng hợp đối soát trực tiếp giữa số liệu công bố trong bài báo khoa học mỏ neo (ACL 2025 [[2]](#ref2)) và kết quả đo đạc thực nghiệm độc lập tại phòng lab Task 3.*

---

## 🔬 LIÊN KẾT ĐẾN PHÒNG THÍ NGHIỆM THỰC NGHIỆM TÁI LẬP (REPLICATION LAB)

- **Phân hệ thực nghiệm tái lập mô hình lõi và Tầng 1 (kèm thực nghiệm định tuyến 2 tầng)**: [`../task_3_replication/`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/README.md)
- **Sổ tay quy trình tái lập chuẩn hóa cho 4 thành viên**: [`../task_3_replication/MEMBER_REPRODUCTION_RUNBOOK.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/MEMBER_REPRODUCTION_RUNBOOK.md)
- **Bộ công cụ script kiểm định API y văn**: [`../task_3_replication/scripts/README.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/scripts/README.md)

---

## 📚 TÀI LIỆU THAM KHẢO HỌC THUẬT (REFERENCES)

<a id="ref1"></a>
- **[[1]]** M. A. Ayub and S. Majumdar, "Embedding-based classifiers can detect prompt injection attacks," in *Proceedings of the Conference on Applied Machine Learning in Information Security (CAMLIS 2024)*, Arlington, VA, USA, Oct. 2024. [arXiv:2410.22284](https://arxiv.org/pdf/2410.22284).

<a id="ref2"></a>
- **[[2]]** H. Li, X. Liu, N. Zhang, and C. Xiao, "PIGuard: Prompt Injection Guardrail via Mitigating Overdefense for Free," in *Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (ACL 2025)*, Vienna, Austria, 2025. [arXiv:2410.22770](https://arxiv.org/pdf/2410.22770) | [ACL Anthology](https://aclanthology.org/2025.acl-long.1468.pdf).

<a id="ref5"></a>
- **[[5]]** V. Majhi, S. T. S. N. V. P. R. N., A. R. R., and S. S., "Do You Really Need a GPU to Guard Your LLM? CPU-Class Classifiers and Multi-Stage Pipelines for Safety Enforcement at Scale," *arXiv preprint arXiv:2512.19011*, Dec. 2025. [arXiv:2512.19011](https://arxiv.org/pdf/2512.19011).

<a id="ref6"></a>
- **[[6]]** N. Jain et al., "Baseline Defenses for Adversarial Attacks on Language Models," in *Proc. NeurIPS Workshop on Robustness of Few-shot and Zero-shot Learning*, 2023. [arXiv:2309.00614](https://arxiv.org/pdf/2309.00614).

