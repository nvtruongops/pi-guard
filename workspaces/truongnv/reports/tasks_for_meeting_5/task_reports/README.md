# HỒ SƠ CÁC CHUYÊN ĐỀ KỸ THUẬT CHI TIẾT — NHIỆM VỤ MEETING 5
**PI-Guard Capstone Project — Workspace: `workspaces/truongnv/reports/tasks_for_meeting_5/task_reports/`**

Thư mục này lưu trữ toàn bộ 7 báo cáo chuyên đề khoa học và kỹ thuật chuyên sâu phục vụ buổi họp **Meeting 5 (17/09/2026)** với GVHD Thầy Trần Văn Ninh.

> 📌 **Báo Cáo Tổng Hợp Điều Hành**:  
> Xem báo cáo tóm tắt tổng thể dành cho GVHD tại: 👉 [`../README.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/README.md)

---

## 📑 DANH MỤC 4 BÁO CÁO KỸ THUẬT CỐT LÕI (4 CORE TASKS CHO MEETING 5)

Theo đúng yêu cầu và chỉ đạo của GVHD Thầy Trần Văn Ninh tại Meeting 4, hồ sơ báo cáo chính thức phục vụ Meeting 5 gồm **ĐÚNG 4 NHIỆM VỤ CỐT LÕI**:

| STT | Tên Nhiệm Vụ | Tệp Báo Cáo Chi Tiết | Trọng Tâm Nghiên Cứu & Đóng Góp Học Thuật |
| :---: | :--- | :--- | :--- |
| **1** | **Nhiệm vụ 1: Giới thiệu 2 Key Đồ Án** | [`TASK_1_PROMPT_INJECTION_VS_JAILBREAK.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_reports/TASK_1_PROMPT_INJECTION_VS_JAILBREAK.md) | Phân biệt bản chất 2 đối tượng nghiên cứu: Prompt Injection ($X = S \mathbin{\Vert} U$ phá vỡ ranh giới phẳng ứng dụng) vs. Jailbreak (phá vỡ căn chỉnh an toàn nội tại $\theta$); xác lập 4 yêu cầu kỹ thuật tối thượng (REQ-1..4). |
| **2** | **Nhiệm vụ 2: Cách Hoạt Động & Kết Quả Bị Tấn Công Của 2 Key** | [`TASK_2_ATTACK_VECTORS_AND_MODELS.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_reports/TASK_2_ATTACK_VECTORS_AND_MODELS.md) | Khung phân tích bề mặt tấn công 5 trục; luồng hoạt động chi tiết của Kênh 1 (Direct Chat) và Kênh 2 (Indirect File/RAG); dấu vết nhận diện (Footprint), chu trình dữ liệu và bán kính thiệt hại (Blast Radius). |
| **3** | **Nhiệm vụ 3: Chạy Thực Nghiệm Mô Hình Public Không Thêm Bớt Gì** | [`TASK_3_REPRODUCIBILITY_AND_DATASETS.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_reports/TASK_3_REPRODUCIBILITY_AND_DATASETS.md) | **Tái lập y văn thuần túy (Pure Literature Replication)**: Tải và chạy nguyên bản 100% mã nguồn và trọng số của 5 mô hình y văn công khai (PIGuard ACL 2025, Ayub CAMLIS 2024, Meta Prompt-Guard 86M, Jain NeurIPS 2023, InstructDetector EMNLP 2024); tuyệt đối không can thiệp code riêng của nhóm, đo đạc trung thực trên 5 tập benchmark mở. |
| **4** | **Nhiệm vụ 4: Mô Hình Đồ Án Có Thể Dùng Thế Nào Từ Thực Nghiệm Task 3** | [`TASK_4_PIGUARD_IMPROVEMENTS.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_reports/TASK_4_PIGUARD_IMPROVEMENTS.md) | **Giải pháp kiến trúc đề xuất của PI-Guard**: Kế thừa bài học Task 3 để đề xuất mô hình phân tầng Two-Tier Cascaded (Tầng 1 lọc nhanh CPU $\le 0.5\text{ms}$ giải phóng $82.6\%$ lưu lượng + Tầng 2 DeBERTa-v3 MOF INT8 $18.5\text{ms}$ thẩm định vùng bất định), đưa độ trễ kỳ vọng về $3.69\text{ms}$, bảo toàn F1 $0.9416$, cùng 4 cải tiến độc quyền và đối chuẩn SOTA. |

---

### 📚 HỒ SƠ CHUYÊN ĐỀ BỔ TRỢ & CHUYÊN KHẢO KHOA HỌC (SUPPORTING TECHNICAL MONOGRAPHS)

| Mã Tài Liệu | Tên Chuyên Đề Bổ Trợ | Tệp Chi Tiết | Vai Trò Học Thuật |
| :---: | :--- | :--- | :--- |
| **MONO-2.5** | **Đánh Giá Toàn Diện SOTA & Ranh Giới Nghiên Cứu** | [`TASK_2_5_SOTA_ASSESSMENT_AND_TWO_TIER_PROPOSAL.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_reports/TASK_2_5_SOTA_ASSESSMENT_AND_TWO_TIER_PROPOSAL.md) | Cung cấp bằng chứng y văn quốc tế cho 6 trường phái SOTA (Llama Guard 3 8B, NeMo, Lakera, Prompt-Guard từ ACL 2025), chứng minh Thế lưỡng nan Pareto, và phân tích 6 khoảng trống phương pháp luận cốt tử nhằm bổ trợ cơ sở lý luận vững chắc cho Nhiệm vụ 4. |
| **SUPP-01** | **Cơ Chế Tính Điểm Tầng 1: Mô Hình Hóa Toán Học & Lý Thuyết Rủi Ro Bayes** | [`supplementary/TIER1_SCORING_MATHEMATICAL_FORMULATION_AND_BAYES_RISK.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_reports/supplementary/TIER1_SCORING_MATHEMATICAL_FORMULATION_AND_BAYES_RISK.md) | Chuyên khảo kỹ thuật chuyên sâu về công thức toán học vector thưa CSR, hiệu chuẩn Platt Scaling, lý thuyết quyết định Bayes nhạy cảm chi phí giải thích ngưỡng $[0.15, 0.85]$, 3 ví dụ tính toán số học từng bước cho 3 Key, và phân định ranh giới kiến trúc Tầng Ứng Dụng vs. External Guardrail Proxy (Springer 2026). Tránh làm phình to phạm vi (Scope Creep) của Task 4. |
| **SUPP-02** | **Chuyên Khảo Khoa Học: Mổ Xẻ Cơ Chế Tấn Công DAN (Do Anything Now), Cấu Trúc Ngữ Nghĩa & Chiến Lược Đánh Chặn** | [`supplementary/DAN_JAILBREAK_ATTACK_MECHANISMS_AND_DEFENSE.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_reports/supplementary/DAN_JAILBREAK_ATTACK_MECHANISMS_AND_DEFENSE.md) | Mổ xẻ toàn diện cơ chế hoạt động của archetype Jailbreak DAN kinh điển: 2 nguyên lý lỗi căn chỉnh cố hữu Competing Objectives & Mismatched Generalization (Wei et al. NeurIPS 2023); Giải phẫu 5 khối chức năng ngữ nghĩa của prompt DAN; Khảo sát thực nghiệm 1,405 prompt in-the-wild và 11 quần thể tiến hóa 4 thế hệ (Shen et al. ACM CCS 2024); Đánh giá nguyên nhân thất bại của OpenAI Moderation & NeMo-Guardrails; và Thiết kế phòng thủ phân tầng của PI-Guard (Heuristic Scrubber + Dual-Space TF-IDF N-Grams $\le 0.4\text{ms}$ + DeBERTa-v3 MOF + Group-Aware Splitting MD5). |
| **SUPP-03** | **Chiếm Quyền Điều Khiển Luồng Ứng Dụng ($X = S \mathbin{\Vert} U$), Không Gian Token Phẳng & Giải Pháp Guardrail Ngoại Vi** | [`supplementary/CONTROL_FLOW_HIJACKING_AND_FLAT_TOKEN_SPACE.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_reports/supplementary/CONTROL_FLOW_HIJACKING_AND_FLAT_TOKEN_SPACE.md) | Chuyên khảo kỹ thuật chuyên sâu mổ xẻ nguyên nhân gốc rễ của Prompt Injection: Không gian token phẳng (Flat Token Space) và hiện tượng chiếm đoạt ma trận Attention; Phân tích 3 phép đối sánh khoa học máy tính kinh điển (Kiến trúc Von Neumann & Tràn bộ đệm, SQL Injection vs. Prepared Statements, Phân quyền trang bộ nhớ NX-bit); 3 kịch bản thực tế sản xuất minh họa kèm chu trình dữ liệu và bán kính thiệt hại; Thiết lập định vị PI-Guard như giải pháp Prepared Statements cho kỷ nguyên LLM theo nguyên lý Complete Mediation (Saltzer & Schroeder 1975). |

---

## 🔬 LIÊN KẾT ĐẾN CÁC PHÂN HỆ THỰC NGHIỆM LIÊN QUAN

- **Phân hệ thực nghiệm tái lập mô hình lõi và Tầng 1 (kèm thực nghiệm định tuyến 2 tầng)**: [`../task_3_replication/`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/README.md)
- **Hồ sơ y văn và runbook thành viên Task 3**: [`../task_3_reproducibility/`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_reproducibility/README.md)
