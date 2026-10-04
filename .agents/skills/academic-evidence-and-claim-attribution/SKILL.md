---
name: academic-evidence-and-claim-attribution
description: >-
  Quy trình và kỹ thuật kiểm toán câu khẳng định học thuật (Sentence-Level Evidence Grounding), bắt buộc mọi
  nhận định kỹ thuật, cơ chế tấn công/phòng thủ, thuật toán và số liệu đo đạc phải có neo trích dẫn khoa học
  chính xác [[N]](#refN) từ kho 38 bài báo trong REFERENCES_LOG.md hoặc tệp dữ liệu đo đạc un-mocked JSON.
---

# 🔬 Academic Evidence & Claim Attribution Skill (Sentence-Level Grounding Protocol)

Skill này cung cấp tiêu chuẩn, phương pháp luận và quy trình kiểm toán tự động nhằm **loại bỏ triệt để tình trạng AI Agent sinh câu khẳng định kỹ thuật hoặc số liệu võ đoán không có dẫn chứng hay trích dẫn khoa học** trong toàn bộ đồ án **PI-Guard**.

---

## 🎯 1. NGUYÊN TẮC BẤT BIẾN: "MỌI CÂU KHẲNG ĐỊNH ĐỀU PHẢI CÓ CHỨNG CỨ"

Mọi câu văn trong luận văn, tài liệu nghiên cứu chuyên đề, slide thuyết trình hoặc báo cáo tiến độ khi đề cập đến một sự thật khách quan (objective fact), cơ chế thuật toán, lỗ hổng hay số liệu đo đạc **PHẢI** thuộc một trong 3 cấu trúc chuẩn mực sau:

### Cấu Trúc 1: Khẳng Định Dựa Trên Y Văn Khoa Học (Literature Grounded Claim)
- **Quy chuẩn**: Phải nêu rõ tên tác giả chính (hoặc tổ chức), năm công bố và neo HTML `[[N]](#refN)` trỏ trực tiếp đến mục References cuối trang.
- **Ví dụ đúng**:
  > *"Theo Perez và Ribeiro (2022) [[3]](#ref3), tấn công Direct Prompt Injection được phân loại thành hai mục tiêu chính: Goal Hijacking (chiếm đoạt luồng thực thi) và Prompt Leaking (đánh cắp system prompt)."*
  > *"He et al. (ICLR 2023) [[9]](#ref9) chứng minh rằng cơ chế chú ý phân tách (Disentangled Attention) giúp mô hình biểu diễn độc lập ma trận nội dung và ma trận vị trí tương đối, cải thiện đáng kể khả năng phân biệt ngữ nghĩa."*
- **Ví dụ sai (BỊ CẤM)**:
  > ❌ *"Prompt Injection gồm có Goal Hijacking và Prompt Leaking."* (Thiếu tác giả và nguồn).
  > ❌ *"Theo các nghiên cứu gần đây, Disentangled Attention giúp tăng độ chính xác."* (Văn phong mơ hồ, không neo nguồn).

### Cấu Trúc 2: Khẳng Định Dựa Trên Số Liệu Thực Nghiệm (Empirical Grounded Claim)
- **Quy chuẩn**: Mọi số liệu đo đạc (Recall %, FPR %, F1, CPU Latency ms) phải trỏ rõ ràng tới tệp kết quả JSON un-mocked trong thư mục `04_benchmarks_and_data/` hoặc tập dữ liệu kiểm thử D1–D6.
- **Ví dụ đúng**:
  > Chỉ nêu số liệu thực nghiệm khi có tệp kết quả và provenance trong deliverable được phép chia sẻ; kết quả còn trong workspace local-only không được trích dẫn như bằng chứng chung.
- **Ví dụ sai (BỊ CẤM)**:
  > ❌ *"Meta Prompt Guard chặn nhầm rất nhiều code lành tính."* (Không có định lượng và không có tệp dẫn chứng).
  > ❌ *"PI-Guard đạt độ trễ 12ms và F1 0.98."* (Làm giả số liệu khi chưa huấn luyện chính thức).

### Cấu Trúc 3: Đề Xuất / Giả Thuyết Của Đồ Án (PI-Guard Architectural Proposal)
- **Quy chuẩn**: Phải gắn nhãn nhận thức (Epistemic Labeling) để người đọc và Hội đồng phản biện không nhầm lẫn giữa định lý y văn với ý tưởng thiết kế của nhóm.
- **Ví dụ đúng**:
  > *"Trong phạm vi thiết kế kiến trúc đề xuất của đề tài PI-Guard (Chương 3), nhóm định hướng kết hợp Tầng 1 (Fast-Filter n-grams) và Tầng 2 (Deep Semantic Arbiter) nhằm hướng tới chỉ tiêu thiết kế SLA: $\text{FPR} \le 1.5\%$ và độ trễ CPU Native $P95 < 30\text{ms}$."*
- **Ví dụ sai (BỊ CẤM)**:
  > ❌ *"Hệ thống PI-Guard hai tầng đã đạt được FPR < 1.5% và P95 < 30ms."* (Khẳng định sai thực tế tiến độ).

---

## 🗺️ 2. MA TRẬN TRA CỨU NHANH TRÍCH DẪN Y VĂN CỐT LÕI (CORE PAPERS LOOKUP)

Trước khi viết câu, Agent phải tra cứu bảng này để lấy đúng tác giả, năm và neo `[[N]](#refN)` đã lưu PDF trong `Final-Report/References/`:

| Chủ Đề / Hiện Tượng Kỹ Thuật | Tác Giả & Năm | Mã Neo Chuẩn | Tệp PDF Cục Bộ Trong `References/` |
| :--- | :--- | :---: | :--- |
| **Không gian ngữ cảnh phẳng ($X = S \mathbin{\Vert} U$)** | Zhao et al. (2023) | `[[1]](#ref1)` | `Zhao_2023_A_Survey_of_Large_Language_Models.pdf` |
| **Instruction Tuning & Competing Priority** | Ouyang et al. (2022) | `[[2]](#ref2)` | `Ouyang_2022_InstructGPT_Training_Language_Models_Follow_Instructions.pdf` |
| **Direct Prompt Injection (Goal Hijacking / Leaking)** | Perez & Ribeiro (2022) | `[[3]](#ref3)` | `Perez_2022_Ignore_This_Title_Hack_This_Paper_Prompt_Injection.pdf` |
| **Indirect Prompt Injection (RAG / Data Poisoning)** | Greshake et al. (2023) | `[[4]](#ref4)` | `Greshake_2023_Indirect_Prompt_Injection.pdf` |
| **Competing Objectives & Mismatched Generalization** | Wei et al. (NeurIPS 2023) | `[[5]](#ref5)` | `Wei_2024_Jailbroken_How_LLM_Safety_Training_Fails.pdf` |
| **Mô hình đe dọa Red Teaming 26+ toán tử** | Tencent AI Infra (2026) | `[[6]](#ref6)` | `Tencent_2026_AI_Infra_Guard_MultiLayer_Agent_RedTeaming.pdf` |
| **Llama Guard (LLM-as-a-Judge Baseline)** | Inan et al. / Meta (2023) | `[[7]](#ref7)` | `Meta_2023_Llama_Guard_Input_Output_Safeguard.pdf` |
| **Kiến trúc Guardrail Ingress Proxy** | Rebedea et al. / NVIDIA (2023) | `[[8]](#ref8)` | `NVIDIA_2023_NeMo_Guardrails_Toolkit.pdf` |
| **DeBERTa-v3 Disentangled Attention & GDES** | He, Gao, Chen (ICLR 2023) | `[[9]](#ref9)` | `He_2023_DeBERTaV3_Disentangled_Attention_ICLR.pdf` |
| **Dual-Space TF-IDF N-grams Baseline** | Jain et al. (NeurIPS 2023) | `[[11]](#ref11)`| `Jain_2023_Baseline_Defenses_Adversarial_Attacks.pdf` |
| **Độ bền đối kháng đa ngôn ngữ & Code-Switching** | Deng et al. (ICLR 2024) | `[[13]](#ref13)`| `Deng_2024_Multilingual_Jailbreak_Challenges.pdf` |
| **SmoothLLM (Random Perturbation Defense)** | Robey et al. (NeurIPS 2023) | `[[14]](#ref14)`| `Robey_2023_SmoothLLM_Defending_Against_Jailbreaking.pdf` |
| **Kinh tế học False Positive Rate ($\text{FPR} \le 1.5\%$)** | Xu et al. (2024) | `[[16]](#ref16)`| `Xu_2024_False_Positive_Rate_Economics_LLM_Guardrails.pdf` |
| **Nguyên tắc bảo vệ phân tầng kinh điển** | Saltzer & Schroeder (IEEE 1975) | `[[17]](#ref17)`| `Saltzer_Schroeder_1975_The_Protection_of_Information_in_Computer_Systems.pdf` |
| **PIGuard MOF Invariance & Overdefense Mitigation**| Hao Li et al. (ACL 2025) | `[[18]](#ref18)`| `Le_2025_PIGuard_Protecting_LLMs_Against_Prompt_Injections.pdf` |
| **Meta Prompt-Guard 86M Model** | Meta AI Technical Report (2024)| `[[20]](#ref20)`| `Meta_2024_Prompt_Guard_86M_Technical_Report.pdf` |
| **DataSentinel Canary Token Defense** | IEEE S&P (2025) | `[[32]](#ref32)`| `DataSentinel_2025_Canary_Token_Defense.pdf` |
| **PromptShield Defense Evaluation** | Jacob et al. (ACM CCS 2024) | `[[30]](#ref30)`| `Jacob_2024_PromptShield_CCS.pdf` |
| **JailbreakBench Standardized Evaluation** | Chao et al. (NeurIPS 2024) | `[[34]](#ref34)`| `Chao_2024_JailbreakBench_An_Open_Robustness_Benchmark.pdf` |

---

## 🚫 3. DANH SÁCH CỤM TỪ BỊ CẤM TUYỆT ĐỐI (VAGUE ATTRIBUTION BLACKLIST)

Agent **KHÔNG BAO GIỜ** được xuất xưởng các câu văn chứa những cụm từ dẫn nguồn mơ hồ sau đây nếu không gắn neo cụ thể:

| Cụm Từ Bị Cấm (Vague Phrases) | Lý Do Bị Hội Đồng Bắt Lỗi | Cách Sửa Đúng Chuẩn Học Thuật |
| :--- | :--- | :--- |
| *"theo các nghiên cứu gần đây..."* | Không chỉ rõ ai, năm nào, hội nghị nào. | *"Theo khảo sát của Zhao et al. (2023) [[1]](#ref1)..."* |
| *"các chuyên gia bảo mật chỉ ra rằng..."* | Khẳng định truyền miệng, thiếu tính học thuật. | *"Báo cáo kỹ thuật của Tencent AI Infra (2026) [[6]](#ref6) chỉ ra rằng..."* |
| *"thực tế cho thấy / như đã biết..."* | Khẳng định chủ quan, coi giả định là chân lý. | *"Thực nghiệm đối chuẩn trên tập D6 tại `cross_dataset_empirical_matrix.json` cho thấy..."* |
| *"theo y văn / theo lý thuyết..."* | Không có địa chỉ đối chiếu. | *"Theo mô hình lỗi căn chỉnh của Wei et al. (NeurIPS 2023) [[5]](#ref5)..."* |
| *"tuyên bố mô hình đạt độ chính xác cao"* | Tự khen võ đoán khi chưa nghiệm thu Chương 4. | *"Mục tiêu thiết kế kiến trúc Chương 3 hướng tới $F_1 \ge 0.95$."* |

---

## 📋 4. CHECKLIST TỰ KIỂM TOÁN CÂU TRƯỚC KHI TRẢ LỜI (PRE-OUTPUT AUDIT)

Trước khi gửi câu trả lời hoặc lưu file Markdown, Agent tự rà soát:
- [ ] Mọi nhận định kỹ thuật (về transformer, attention, injection, jailbreak) đều có neo `[[N]](#refN)`.
- [ ] Tất cả các neo `[[N]]` trong văn bản đều có neo đối ứng `<a id="refN"></a>` trong mục References cuối file.
- [ ] Không có bất kỳ câu nào sử dụng cụm từ trong bảng Vague Attribution Blacklist.
- [ ] Không có số liệu đo đạc nào được gán cho mô hình đề xuất khi chưa đến Chương 4.
- [ ] Chạy `python Final-Report/scripts/audit_claim_evidence.py --file <file.md>` để đảm bảo script trả về **PASS**.
