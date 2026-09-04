# KỊCH BẢN & NỘI DUNG SLIDE THUYẾT TRÌNH REVIEW 1
## BÁO CÁO TOÀN DIỆN 2 CHƯƠNG (REPORT NO. 1: INTRODUCTION & REPORT NO. 2: LITERATURE REVIEW)
### ĐỀ TÀI: PI-Guard — A Machine-Learning Guardrail for Detecting Prompt Injection and Jailbreak Attacks on LLM Applications

**Thời lượng dự kiến**: 15 phút trình bày + 10 phút hỏi đáp Hội đồng  
> **Phương châm làm việc**: **Ai cũng làm $\rightarrow$ Tham khảo nhau $\rightarrow$ Chốt kết quả** (Tất cả 4 thành viên đều trực tiếp thực hiện toàn trình từ dữ liệu, mô hình baseline, transformer đến API và bảo vệ luận văn; mỗi thành viên đại diện trình bày các phần trong slide và toàn đội sẵn sàng hỗ trợ phản biện mọi câu hỏi của Hội đồng).

**Phân bổ phần trình bày 4 thành viên (Báo cáo 2 Chương Luận văn)**:
- **Nguyễn Văn Trường (Leader)**: Slide 1 - 3 *(Giới thiệu, Bối cảnh, Lỗ hổng Von Neumann, 4 Tầng Thiệt hại, Phân loại Taxonomy — Chapter 1)*
- **Nguyễn Quí Đức**: Slide 4 - 5 *(Threat Model, Attack Surface, Khảo sát SOTA Guardrails, Kiến trúc bảo vệ 3 lớp & Robustness — Chapter 2)*
- **Phạm Minh Hoàng Việt**: Slide 6 - 7 *(Khảo sát Y văn Lựa chọn Mô hình, Khảo sát Target LLMs & Kịch bản Minh họa Đề bài — Chapter 2)*
- **Đỗ Đoàn Duy Phương**: Slide 8 - 9 *(3 Research Questions IEEE, 3 Research Gaps, 4 Đóng góp mới, Ranh giới Scope & Kế hoạch)*

---

### Slide 1: Trang Tiêu Đề & Thành Viên Nhóm (Trường trình bày)
- **Tên đề tài**: *A Machine-Learning Guardrail for Detecting Prompt Injection and Jailbreak Attacks on LLM Applications (PI-Guard)*
- **Mã đề tài**: `IAP491_FA26_PI_GUARD`
- **Giảng viên hướng dẫn**: [Tên Thầy/Cô Hướng dẫn]
- **Nhóm sinh viên thực hiện (Mô hình làm việc toàn trình)**:
  - Nguyễn Văn Trường (Leader - SE182034) — *Kiến trúc & Điều phối toàn trình*
  - Nguyễn Quí Đức (SE182087) — *Mô hình Baseline ML & Toàn trình*
  - Phạm Minh Hoàng Việt (SE181851) — *Transformer, Robustness & Toàn trình*
  - Đỗ Đoàn Duy Phương (SE180235) — *Hệ thống API, Dashboard & Toàn trình*
- **Điểm nhấn mở đầu**: *"Kính thưa Hội đồng, báo cáo Review 1 của nhóm PI-Guard hôm nay bao gồm toàn diện 2 Chương đầu tiên của Khóa luận: Chapter 1 (Introduction) và Chapter 2 (Literature Review), giải quyết lỗ hổng bảo mật số 1 của ứng dụng Generative AI với độ trễ P95 < 30ms trên CPU."*

---

### Slide 2: Bối Cảnh, Lỗ Hổng Von Neumann & 4 Tầng Thiệt Hại Thực Tế (Chapter 1 — Trường trình bày)
- **Bản chất kỹ thuật (Lỗ hổng Von Neumann trong NLP)**:
  - LLM ghép chung System Instruction ($S$) và User Data ($U$) thành chuỗi token phẳng ($X = S \mathbin{\Vert} U$).
  - Không có ranh giới phần cứng hay phân tách quyền hạn (Privilege Separation) giữa Code và Data.
- **4 Tầng Thiệt hại Thực tế Đối với Doanh nghiệp & Ứng dụng AI**:
  1. *Rò rỉ Bí mật Trí tuệ (IP) & Master API Keys*: Mất System Prompt bí mật, lộ API credentials (như vụ Sydney Bing Chat).
  2. *Chiếm quyền điều khiển Tác tử AI (Agent Goal Hijacking)*: Ép AI Agent chuyển tiền tự động, truy vấn trái phép database, xóa dữ liệu khách hàng.
  3. *Tấn công cạn kiệt tài nguyên (Denial-of-Wallet)*: Bơm prompt ép mô hình sinh văn bản lặp vô tận, gây hóa đơn API hàng chục nghìn USD.
  4. *Chế tài Pháp lý & Mất uy tín (Compliance Fines)*: Ép AI sinh mã độc hoặc nội dung cấm, vi phạm nghiêm trọng EU AI Act và GDPR.

---

### Slide 3: Phân Biệt Prompt Injection vs. Jailbreak (Chapter 1 & 2 — Trường trình bày)
- **Bảng so sánh 3 trục chuẩn OWASP LLM01:2025**:
  1. *Direct Prompt Injection*: Tấn công trực tiếp vào ô chat để chiếm quyền điều khiển logic và trích xuất System Prompt (Perez 2022 [[3]](#ref3)).
  2. *Indirect Prompt Injection*: Payload độc hại nằm ẩn trong tài liệu RAG, trang web, email mà LLM đọc được (Greshake 2023 [[4]](#ref4), Tencent Zhuque Lab 2026 [[6]](#ref6)).
  3. *Jailbreak*: Tấn công bẻ khóa an toàn nội dung (DAN roleplay, tình huống giả định, Base64/Cipher) ép LLM sinh nội dung bị cấm (Wei 2024 [[5]](#ref5), Yuan 2024 [[17]](#ref17)).
- **Điểm chung dưới góc nhìn mô hình**: Cả Direct và Indirect Injection đều mang chung các đặc trưng cú pháp ghi đè quyền lực, cho phép mô hình PI-Guard phát hiện tự nhiên dưới cùng nhãn `PROMPT_INJECTION`.

---

### Slide 4: Threat Model & Attack Surface (Chapter 1 & 2 — Đức trình bày)
- **Mô hình đe dọa (Threat Model theo NIST AI 100-2e2025 & Tencent 2026)**:
  - *Attacker*: Kẻ tấn công gửi payload độc hại qua giao diện chat hoặc gọi trực tiếp API.
  - *Target*: System Prompt IP, API Keys, Execution Integrity, Tài nguyên GPU.
  - *Bề mặt tấn công duy nhất (Attack Surface)*: Cổng REST API tiếp nhận chuỗi văn bản đầu vào (`POST /v1/chat/guardrail`).
- **Khóa chặt phạm vi**: PI-Guard không chịu trách nhiệm dựng RAG Vector DB hay Agent Runtime, mà là chốt chặn kiểm duyệt chuỗi văn bản đầu vào trước khi chuyển tới LLM.

---

### Slide 5: Khảo Sát SOTA Guardrails & Kiến Trúc Bảo Vệ 3 Lớp (Chapter 2 — Đức trình bày)
- **Khảo sát 3 trường phái Guardrail trong thực tế (Literature Review)**:
  - *Regex/Keyword Rules*: Nhanh (<1ms) nhưng quá giòn (*brittle*), bị bypass hoàn toàn bởi `1gn0r3` và Base64.
  - *LLM-as-a-Judge (Llama Guard 3 8B, NeMo)*: Quá nặng (>16GB VRAM GPU, Latency >500ms, không khả thi cho chốt chặn API có lưu lượng lớn).
  - *Transformer Encoders (ProtectAI, PI-Guard)*: Cân bằng tối ưu giữa độ chính xác ngữ nghĩa và tốc độ.
- **Chiến lược Phòng thủ 3 Lớp Tiêu Chuẩn (Defense-in-Depth)**:
  - *Lớp 1 (PI-Guard Input Guardrail - Trọng tâm đồ án)*: Tiền xử lý + Hybrid ML Classifier + Policy Engine.
  - *Lớp 2 (Target LLM Application)*: System Prompt Hardening (XML tags) + Base LLM.
  - *Lớp 3 (Output Sanitizer)*: Hậu kiểm tra quét rò rỉ PII và Secret Key ở đầu ra.
- **3 Tầng Bảo vệ Độ bền trước Lẩn tránh Cú pháp (Leetspeak, Base64, Spacing)**:
  1. *Tầng Tiền xử lý*: Unicode NFKC Normalization + Heuristic Base64 Decoder (Yuan et al. ICLR 2024).
  2. *Tầng Đặc trưng*: Character n-grams TF-IDF bóc tách `1gn0r3` $\rightarrow$ `['1gn','gn0','n0r']` (Jain et al. 2023) + DeBERTa BPE Subwords.
  3. *Tầng Kiểm thử Đối kháng*: Cam kết độ suy giảm $F_1$ khi bị nhiễu cú pháp $< 5\%$.

---

### Slide 6: Khảo Sát Y Văn Lựa Chọn Mô Hình & Định Hướng Đa LLM API (Chapter 2 — Việt trình bày)
- **Khảo Sát Y Văn & Luận Giải Lựa Chọn Mô Hình (Model Selection Rationale)**:
  - *Căn cứ bản đăng ký đề tài (`CAPSTONE PROJECT REGISTER.md`)*: Kết hợp Classical ML Baseline (TF-IDF + linear classifier) và Deep Transformer (BERT/DeBERTa).
  - *Cơ chế Disentangled Attention* (He et al. ICLR 2023): Tách biệt Content và Relative Position, bắt chính xác câu lệnh đảo ngữ và ghi đè chỉ thị mà BERT/RoBERTa không làm được.
  - *Bảo chứng SOTA công nghiệp*: Meta AI (`Meta Prompt-Guard-86M`, 07/2024) và Protect AI đều chọn DeBERTa-v3 làm nền tảng guardrail phân loại prompt tối ưu nhất (<100M params).
  - *Mục tiêu thiết kế định lượng (Design Targets)*: Hướng tới $F_1 \ge 0.95$, $\text{FPR} < 1.5\%$ trên benign, độ trễ $P95 < 30\text{ms}$ trên CPU thông qua lượng hóa động ONNX INT8 (Yao et al. NeurIPS 2022).
- **Khảo Sát Y Văn Về Lỗ Hổng Của Các Target LLMs & Thiết Kế Khung Đánh Giá API (Chapter 4)**:
  - *Khảo sát mức độ dễ tổn thương trong y văn*: Theo Zou et al. (GCG 2023), Zhou et al. (EasyJailbreak 2024), Wei et al. (2024), các mô hình dù có căn chỉnh an toàn nội tại (RLHF/DPO) vẫn có tỷ lệ bị bẻ khóa tự thân (ASR Baseline) rất cao từ **$35.5\% - 78.4\%$**.
  - *Lựa chọn 5 Target LLMs làm đối tượng bảo vệ qua Cloud API*: **OpenAI GPT-4o-mini**, **Google Gemini 1.5 Flash**, **Meta LLaMA-3.1-8B**, **Mistral-7B**, và **Qwen-2.5-7B**.
  - *Định hướng bảo vệ độc lập (Model-Agnostic)*: PI-Guard đóng vai trò tiền trạm, hướng tới mục tiêu giảm ASR xuống $< 5\%$ mà không tốn GPU cục bộ.
- **Phương Pháp Luận Phát Triển Toàn Trình Song Song Của Toàn Đội**:
  - Cả 4 thành viên cùng nghiên cứu, thử nghiệm độc lập trên cả 2 mô hình (TF-IDF Baseline và Transformer DeBERTa-v3) trong workspace cá nhân, đối chiếu số liệu chéo trước khi chốt artifact tối ưu cho hệ thống.

---

### Slide 7: Kịch Bản Minh Họa Bài Toán Tấn Công & Cơ Chế Bảo Vệ Đề Xuất (Chapter 1 & 2 — Việt trình bày)
- **Ma trận Kịch bản Minh họa Đề bài (Phân tích đối chiếu theo Yêu cầu số 5 của GVHD)**:
  - Minh họa trực quan bản chất 2 dạng tấn công cốt lõi xuất phát từ cùng 1 chuỗi `User Input` độc hại:
- **Trục 1: Prompt Injection (Ghi đè System Prompt / Khai thác dữ liệu nhạy cảm)**:
  - *Kịch bản Không có Guardrail (Vulnerable)*: Kẻ tấn công gửi chuỗi override chỉ thị $\rightarrow$ LLM bị ghi đè ngữ cảnh, làm lộ Master API Key `ABC-SEC-998877` và nội dung System Prompt.
  - *Cơ chế Bảo vệ Đề xuất (Proposed Protected)*: Lớp 1 (PI-Guard) phân tích vector ngữ nghĩa $\rightarrow$ Phát hiện mẫu ghi đè chỉ thị $\rightarrow$ Chặn đứng ngay tại cổng API, trả về HTTP 403 Forbidden kèm cấu trúc cảnh báo an toàn mà không chuyển tiếp request tới Target LLM.
- **Trục 2: Jailbreak (Bẻ khóa An toàn bằng Nhập vai DAN)**:
  - *Kịch bản Không có Guardrail (Vulnerable)*: Kẻ tấn công dùng kỹ thuật dàn cảnh hư cấu (*Hypothetical Roleplay*) ép LLM đóng vai DAN $\rightarrow$ LLM vượt qua bộ lọc an toàn tự thân, sinh mã độc hại keylogger.
  - *Cơ chế Bảo vệ Đề xuất (Proposed Protected)*: Lớp 1 nhận diện đặc trưng tấn công bẻ khóa $\rightarrow$ Chặn tại cổng API, bảo vệ triệt để chính sách an toàn của ứng dụng.
- **Ý nghĩa học thuật & thực tiễn**:
  - Minh chứng rõ ràng yêu cầu cấp thiết của lớp Guardrail tiền trạm độc lập để ngăn ngừa rủi ro rò rỉ dữ liệu và vi phạm chính sách an toàn trước khi vào LLM.

---

### Slide 8: 3 Research Questions, 3 Research Gaps & 4 Đóng Góp Mới (Chapter 1 & 2 — Phương trình bày)
- **3 Research Gaps $\leftrightarrow$ 3 Research Questions chuẩn IEEE**:
  1. *Gap 1 & RQ1 (Data Leakage & Splitting)*: Group-Aware Splitting triệt tiêu rò rỉ cụm mẫu; Phân định ranh giới giữa Classical ML (TF-IDF) và DeBERTa-v3 Disentangled Attention ($F_1 \ge 0.95$, $F_1^{\text{OOD}} \ge 0.92$).
  2. *Gap 2 & RQ2 (Adversarial Evasion)*: Duy trì độ bền trước các biến dị Leetspeak, Spacing, và Base64/Cipher ($\Delta F_1 < 5\%, \text{ASR} < 5\%$).
  3. *Gap 3 & RQ3 (Inline Latency & FPR)*: Khống chế nghiêm ngặt $\text{FPR} < 1.5\%$ trên tập Benign; Lượng hóa INT8 bảo toàn ranh giới an toàn ($\Delta F_1 < 0.3\%$) và đạt độ trễ $P95 < 30\text{ms}$ trên CPU.
- **4 Đóng góp cốt lõi của PI-Guard (Chuyên ngành An toàn Thông tin)**:
  1. *Kỹ thuật dữ liệu an ninh*: Quy trình Group-Aware Splitting triệt tiêu rò rỉ cụm mẫu tấn công và bảo đảm đánh giá tổng quát hóa thực chất.
  2. *Kiến trúc phòng thủ đa tầng*: Phối hợp Hybrid TF-IDF (Lọc cú pháp phân mảnh) và DeBERTa-v3 Disentangled Attention (Phân loại ngữ nghĩa sâu, bóc tách chỉ thị).
  3. *Kháng lẩn tránh đối kháng*: Bộ giải mã Heuristic Cipher/Base64 và tiền xử lý chuẩn hóa duy trì độ bền vững cao trước các biến dị lẩn tránh ($\Delta F_1 < 2.3\%$).
  4. *Hạ tầng Guardrail trực tuyến*: Middleware bất đồng bộ FastAPI tích hợp Tri-state Policy Engine khống chế $\text{FPR} < 1.5\%$, tối ưu hóa thực thi độ trễ thấp trên CPU ($P95 < 30\text{ms}$) và Dashboard Streamlit trực quan.

---

### Slide 9: Ranh Giới Scope, 4 Cột Mốc Quyết Định & Phân Công Nhiệm Vụ (Phương trình bày)
- **Ranh giới Scope (In-Scope vs. Out-of-Scope)**:
  - *In-Scope*: 2 trục cốt lõi Prompt Injection & Jailbreak trên chuỗi văn bản; Test độ bền với Leetspeak, Base64; FastAPI Middleware trực tuyến (Low-latency).
  - *Out-of-Scope*: Tấn công đa phương thức (Ảnh/Audio), tấn công hạ tầng mạng DDoS, trích xuất trọng số GPU, dựng hệ thống RAG Database.
- **4 Cột Mốc Bảo Vệ Đồ Án Quyết Định**:
  - 🎯 **Cột mốc 1: REVIEW 1 (GVHD - Tuần 3-4 / 28/09 – 04/10)**: Báo cáo toàn diện **Chapter 1 (Introduction) + Chapter 2 (Literature Review)**.
  - 🎯 **Cột mốc 2: REVIEW 2 (GVHD - Tuần 8 / 26/10 – 01/11)**: Báo cáo **Chapter 3 (Methodology, Group-Aware Split, Baseline ML & Cập nhật Docs)**.
  - 🏛️ **Cột mốc 3: BÁO CÁO HỘI ĐỒNG 1 (Hội đồng Giữa kỳ - Tuần 13 / 30/11 – 06/12)**: Báo cáo **Chapter 4 (Transformer DeBERTa-v3, ONNX INT8, FastAPI Prototype & Streamlit Demo)**.
  - 🎓 **Cột mốc 4: BÁO CÁO HỘI ĐỒNG FINAL (Hội đồng Tốt nghiệp - Tuần 15 / 14/12 – 20/12)**: Toàn văn Luận văn 6 Chương hoàn chỉnh, Quét Turnitin (< 20%) & Bảo vệ Tốt nghiệp chính thức.
- **Phân công 4 thành viên**: Trường (Leader - Ch.1 & Ch.2), Đức (Ch.3), Việt (Ch.4), Phương (Ch.5 & Ch.6).

---

### Slide 10: Tài Liệu Tham Khảo Học Thuật Chuẩn IEEE (100% >= 2022)

<a id="ref1"></a>**[1]** W. X. Zhao et al., "A Survey of Large Language Models," *arXiv preprint arXiv:2303.18223*, 2023. Link: [https://arxiv.org/abs/2303.18223](https://arxiv.org/abs/2303.18223).  
<a id="ref2"></a>**[2]** L. Ouyang et al., "Training language models to follow instructions with human feedback," in *Advances in Neural Information Processing Systems (NeurIPS 2022)*, vol. 35, pp. 27730–27744. Link: [https://arxiv.org/abs/2203.02155](https://arxiv.org/abs/2203.02155).  
<a id="ref3"></a>**[3]** F. Perez and I. Ribeiro, "Ignore This Title and Hack This Paper: Towards Automated Adversarial Prompting," in *NeurIPS Workshops*, 2022. Link: [https://arxiv.org/abs/2206.05600](https://arxiv.org/abs/2206.05600).  
<a id="ref4"></a>**[4]** K. Greshake, S. Abdelnabi, S. Mishra, C. Endres, T. Holz, and M. Fritz, "Not what you've signed up for: Compromising Real-World LLM Applications with Indirect Prompt Injection," in *Proceedings of the 16th ACM Workshop on Artificial Intelligence and Security (AISEC 2023)*, pp. 79–90. Link: [https://arxiv.org/abs/2302.12173](https://arxiv.org/abs/2302.12173).  
<a id="ref5"></a>**[5]** A. Wei, N. Haghtalab, and J. Steinhardt, "Jailbroken: How Does LLM Safety Training Fail?," in *Advances in Neural Information Processing Systems (NeurIPS 2024)*, vol. 36. Link: [https://arxiv.org/abs/2307.02483](https://arxiv.org/abs/2307.02483).  
<a id="ref6"></a>**[6]** Y. Yang et al., "Securing the AI Agent: A Unified Framework for Multi-Layer Agent Red Teaming," *Tencent Zhuque Lab Technical Report*, arXiv:2606.31227, 2026. Link: [https://arxiv.org/abs/2606.31227](https://arxiv.org/abs/2606.31227).  
<a id="ref7"></a>**[7]** A. Vassilev et al., "Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations," *NIST.AI.100-2e2025*, 2025. Link: [https://csrc.nist.gov/pubs/ai/100/2/e2025/final](https://csrc.nist.gov/pubs/ai/100/2/e2025/final).  
<a id="ref8"></a>**[8]** OWASP GenAI Security Project, "OWASP Top 10 for Large Language Model Applications," Version 2.0, 2025. Link: [https://owasp.org/www-project-top-10-for-large-language-model-applications/](https://owasp.org/www-project-top-10-for-large-language-model-applications/).  
<a id="ref9"></a>**[9]** H. Inan et al., "Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations," *Meta AI Technical Report*, arXiv:2312.06674, 2023. Link: [https://arxiv.org/abs/2312.06674](https://arxiv.org/abs/2312.06674).  
<a id="ref10"></a>**[10]** T. Rebedea et al., "NeMo Guardrails: A Toolkit for Controllable and Safe LLM Applications," in *Proceedings of EMNLP System Demonstrations*, pp. 431–444, 2023. Link: [https://arxiv.org/abs/2310.10501](https://arxiv.org/abs/2310.10501).  
<a id="ref11"></a>**[11]** P. He, J. Gao, and W. Chen, "DeBERTaV3: Improving DeBERTa using ELECTRA-Style Pre-Training with Gradient-Disentangled Embedding Sharing," in *Proceedings of ICLR 2023*. Link: [https://arxiv.org/abs/2111.09543](https://arxiv.org/abs/2111.09543).  
<a id="ref12"></a>**[12]** T. Markov et al., "A Holistic Approach to Undesired Content Detection in the Real World," in *Proceedings of AAAI HCOMP 2023*. Link: [https://arxiv.org/abs/2208.03274](https://arxiv.org/abs/2208.03274).  
<a id="ref13"></a>**[13]** N. Jain et al., "Baseline Defenses for Adversarial Attacks Against Aligned Language Models," arXiv:2309.00614, 2023. Link: [https://arxiv.org/abs/2309.00614](https://arxiv.org/abs/2309.00614).  
<a id="ref14"></a>**[14]** Z. Yao et al., "ZeroQuant: Efficient and Affordable Post-Training Quantization for Large-Scale Transformers," in *Advances in Neural Information Processing Systems (NeurIPS 2022)*, vol. 35. Link: [https://arxiv.org/abs/2206.01861](https://arxiv.org/abs/2206.01861).  
<a id="ref15"></a>**[15]** X. Shen et al., "\"Do Anything Now\": Characterizing and Evaluating In-The-Wild Jailbreak Prompts on Large Language Models," in *Proceedings of ACM CCS 2024*, pp. 4028–4042. Link: [https://arxiv.org/abs/2308.03825](https://arxiv.org/abs/2308.03825).  
<a id="ref16"></a>**[16]** H. Zhou et al., "EasyJailbreak: A Unified Framework for Jailbreaking Large Language Models," arXiv:2403.12171, 2024. Link: [https://arxiv.org/abs/2403.12171](https://arxiv.org/abs/2403.12171).  
<a id="ref17"></a>**[17]** Y. Yuan, W. Jiao, W. Wang, J. Huang, P. He, and Z. Tu, "GPT-4 Is Too Smart To Be Safe: Stealthy Chat with LLMs via Cipher," in *Proceedings of ICLR 2024*. Link: [https://arxiv.org/abs/2308.06463](https://arxiv.org/abs/2308.06463).
