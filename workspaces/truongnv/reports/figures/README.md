# HỒ SƠ METADATA & DANH MỤC HÌNH ẢNH HỌC THUẬT (SLIDE GẶP GVHD 10/09/2026)
## TẬP TIN TRÌNH CHIẾU GỐC: [`PI-GUARD-Present-109.pptx`](file:///d:/Work/Do-an/reports/PI-GUARD-Present-109.pptx)
### Dự án: PI-Guard — A Machine-Learning Guardrail for Detecting Prompt Injection and Jailbreak Attacks on LLM Applications
**Mã Đề Tài**: `IAP491_FA26_PI_GUARD` | **Ngày Báo Cáo GVHD**: 10/09/2026 | **Leader**: Nguyễn Văn Trường

---

> [!IMPORTANT]
> **TIÊU CHUẨN ĐỒNG BỘ DỮ LIỆU HÌNH ẢNH & MỤC ĐÍCH TÀI LIỆU**:
> - Toàn bộ 13 tệp hình ảnh trong thư mục này được trích xuất trực tiếp từ bản trình chiếu PowerPoint báo cáo tiến độ gặp Giáo viên Hướng dẫn ngày 10/09/2026 ([`reports/PI-GUARD-Present-109.pptx`](file:///d:/Work/Do-an/reports/PI-GUARD-Present-109.pptx)).
> - **LƯU Ý QUAN TRỌNG**: Bộ slide này phục vụ **buổi báo cáo tiến độ định kỳ với GVHD ngày 10/09/2026**, **KHÔNG PHẢI slide báo cáo bảo vệ Review 1 trước Hội đồng**. Slide Review 1 chính thức sẽ được nhóm hoàn thiện và đóng gói riêng sau khi tiếp thu ý kiến định hướng từ GVHD.
> - Tên tệp được chuẩn hóa theo quy ước `slide<NN>_<chủ_đề>_<tác_giả_nguồn_năm>.png` với bảo chứng học thuật 100% từ các hội nghị bình duyệt đỉnh cao (NeurIPS, ACM CCS, ACL, ICLR) và báo cáo chuyên gia quốc tế (Tencent Zhuque Lab 2026).

---

## 📊 BẢNG TỔNG HỢP METADATA 13 HÌNH ẢNH

| STT | Tên Tệp Hình Ảnh | Slide | Định Dạng & Kích Thước | Nguồn Gốc Học Thuật (Tác Giả & Năm) | Tác Dụng & Vai Trò Kỹ Thuật Trong PI-Guard |
| :---: | :--- | :---: | :---: | :--- | :--- |
| **1** | [`slide04_promptinject_framework_perez2022.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/slide04_promptinject_framework_perez2022.png) | Slide 4 | PNG ($927 \times 420$) | Perez & Ribeiro (NeurIPS 2022 [[1]](#ref1)) | Minh chứng tấn công Prompt Injection: Chiếm quyền điều khiển luồng lệnh (Control-Flow Hijacking) & Trích xuất System Prompt. |
| **2** | [`slide05_jailbreak_dan_structure_shen2024.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/slide05_jailbreak_dan_structure_shen2024.png) | Slide 5 | PNG ($865 \times 708$) | Shen et al. (ACM CCS 2024 [[2]](#ref2)) | Minh chứng tấn công Jailbreak: Bẻ khóa chính sách an toàn (Safety Policy Bypass) bằng cấu trúc nhập vai DAN (Do Anything Now). |
| **3** | [`slide06_indirect_prompt_injection_bipia_yi2024.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/slide06_indirect_prompt_injection_bipia_yi2024.png) | Slide 6 | PNG ($927 \times 420$) | Yi et al. (BIPIA - ACL 2024 [[3]](#ref3)) | Trực quan hóa rủi ro tấn công gián tiếp (Indirect Injection) khi LLM đọc dữ liệu web nhiễm độc ngầm trong các ứng dụng RAG/Agent. |
| **4** | [`slide08_layer1_data_exfiltration_greshake2023.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/slide08_layer1_data_exfiltration_greshake2023.png) | Slide 8 | PNG ($848 \times 545$) | Greshake et al. (ACM AISec 2023 [[4]](#ref4)) | Phân tích Tầng Thiệt hại 1: Rò rỉ dữ liệu qua kênh phụ (Side-Channel Exfiltration), đánh cắp IP bí mật và Master API Key. |
| **5** | [`slide09_layer2_agent_hijacking_greshake2023.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/slide09_layer2_agent_hijacking_greshake2023.png) | Slide 9 | PNG ($848 \times 545$) | Greshake et al. (ACM AISec 2023 [[4]](#ref4)) | Phân tích Tầng Thiệt hại 2: Chiếm đoạt tác tử tự hành (Autonomous Agent Hijacking), biến LLM thành mã độc nội bộ khi có quyền Tool Calling. |
| **6** | [`slide10_layer3_denial_of_wallet_greshake2023.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/slide10_layer3_denial_of_wallet_greshake2023.png) | Slide 10 | PNG ($848 \times 545$) | Greshake et al. (ACM AISec 2023 [[4]](#ref4)) | Phân tích Tầng Thiệt hại 3: Tấn công từ chối ví tiền (Denial of Wallet — DoW), kích hoạt vòng lặp sinh token vô tận làm cạn kiệt ngân sách API. |
| **7** | [`slide11_layer4_legal_compliance_greshake2023.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/slide11_layer4_legal_compliance_greshake2023.png) | Slide 11 | PNG ($848 \times 545$) | Greshake et al. (ACM AISec 2023 [[4]](#ref4)) | Phân tích Tầng Thiệt hại 4: Trách nhiệm pháp lý & chế tài EU AI Act (phạt 35M EUR) khi LLM bị thao túng đưa ra phát ngôn vi phạm chính sách. |
| **8** | [`slide12_threat_model_agent_surface_tencent2026.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/slide12_threat_model_agent_surface_tencent2026.png) | Slide 12 | PNG ($848 \times 545$) | Tencent Zhuque Lab (arXiv 2026 [[5]](#ref5)) | Thiết lập Threat Model 4 Vùng ranh giới tin cậy (Zone 0 - Zone 3) và vị trí đặt vành đai kiểm duyệt độc lập PI-Guard tại Zone 1. |
| **9** | [`slide14_sota_guardrails_comparison_piguard.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/slide14_sota_guardrails_comparison_piguard.png) | Slide 14 | PNG ($2045 \times 692$) | Đề tài PI-Guard (Khảo sát SOTA) | Đối sánh 3 trường phái bảo vệ (Regex vs. LLM-as-a-Judge vs. PI-Guard Encoder Transformers) về Độ trễ, Chi phí GPU và Độ bền vững. |
| **10** | [`slide16_tier1_tfidf_ngram_mechanism_jain2023.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/slide16_tier1_tfidf_ngram_mechanism_jain2023.png) | Slide 16 | PNG ($848 \times 545$) | Jain et al. (arXiv 2023 [[6]](#ref6)) | Cơ chế Tầng 1: Trích xuất Character N-Grams ($n=3..5$) quét xuyên qua Leetspeak (`1gn0r3`) trong $< 1\text{ms}$ trên CPU thông thường. |
| **11** | [`slide17_tier2_deberta_disentangled_onnx_he2023.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/slide17_tier2_deberta_disentangled_onnx_he2023.png) | Slide 17 | PNG ($848 \times 545$) | He et al. (ICLR 2023 [[7]](#ref7)), Yao (NeurIPS 2022 [[8]](#ref8)) | Cơ chế Tầng 2: Disentangled Attention tách biệt vector nội dung & vị trí tương đối, kết hợp lượng hóa ONNX INT8 đạt P95 $< 18.5\text{ms}$. |
| **12** | [`slide18_twotier_cascaded_architecture_saltzer1975.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/slide18_twotier_cascaded_architecture_saltzer1975.png) | Slide 18 | PNG ($1128 \times 893$) | PI-Guard Architecture & Saltzer-Schroeder (1975 [[9]](#ref9)) | Kiến trúc phối hợp 2 tầng (Two-Tier Cascaded Guardrail) sử dụng Uncertainty Routing ($0.15 < P < 0.85$), đạt tối ưu Pareto (Zero-GPU). |
| **13** | [`slide19_bipia_table2_asr_llms_yi2024.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/slide19_bipia_table2_asr_llms_yi2024.png) | Slide 19 | PNG ($2045 \times 751$) | Yi et al. (BIPIA - ACL 2024, Table 2 [[3]](#ref3)) | Bằng chứng thực nghiệm: Tỷ lệ tấn công thành công ASR $\ge 80\%$ trên cả GPT-4, Claude, PaLM khi không có cơ chế bảo vệ chuyên dụng. |

---

## 🔍 CHI TIẾT TỪNG HÌNH ẢNH & TÁC DỤNG HỌC THUẬT

### 1. Slide 4: Khung Tấn Công PromptInject
![Slide 04: Khung Tấn Công PromptInject (Perez & Ribeiro, NeurIPS 2022)](./slide04_promptinject_framework_perez2022.png)
- **Tên tệp**: [`slide04_promptinject_framework_perez2022.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/slide04_promptinject_framework_perez2022.png)
- **Nguồn gốc**: F. Perez và I. Ribeiro, *"Ignore Previous Prompt: Attack Techniques For Language Models,"* in *NeurIPS ML Safety Workshop*, 2022 [[1]](#ref1).
- **Kích thước**: $927 \times 420$ px | Dung lượng: $69.5\text{ KB}$ | Định dạng: PNG.
- **Tác dụng đối với đề tài**: Minh chứng bản chất của tấn công **Prompt Injection** là tấn công chiếm quyền luồng điều khiển (Control-Flow Hijacking). Kẻ tấn công lợi dụng việc LLM hòa trộn System Instruction và User Data thành chuỗi token phẳng để ghi đè chỉ thị ban đầu, ép LLM in ra mã nguồn/prompt bí mật.

---

### 2. Slide 5: Cấu Trúc Câu Lệnh Bẻ Khóa DAN (Do Anything Now)
![Slide 05: Cấu Trúc Câu Lệnh Bẻ Khóa DAN (Shen et al., ACM CCS 2024)](./slide05_jailbreak_dan_structure_shen2024.png)
- **Tên tệp**: [`slide05_jailbreak_dan_structure_shen2024.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/slide05_jailbreak_dan_structure_shen2024.png)
- **Nguồn gốc**: X. Shen, Z. Chen, M. Backes, Y. Shen, và Y. Zhang, *"\"Do Anything Now\": Characterizing and Evaluating In-The-Wild Jailbreak Prompts on Large Language Models,"* in *ACM CCS 2024* [[2]](#ref2).
- **Kích thước**: $865 \times 708$ px | Dung lượng: $126.8\text{ KB}$ | Định dạng: PNG.
- **Tác dụng đối với đề tài**: Minh chứng bản chất của **Jailbreak** là bẻ khóa căn chỉnh an toàn nội tại (Safety Alignment / RLHF). Bằng cách tạo dựng nhân vật ảo "DAN" không bị ràng buộc đạo đức, câu lệnh ép LLM vi phạm chính sách nội dung (vũ khí, mã độc) mà không cần thay đổi logic ứng dụng.

---

### 3. Slide 6: Tấn Công Gián Tiếp Indirect Prompt Injection (BIPIA)
![Slide 06: Tấn Công Gián Tiếp Indirect Prompt Injection (Yi et al., ACL 2024)](./slide06_indirect_prompt_injection_bipia_yi2024.png)
- **Tên tệp**: [`slide06_indirect_prompt_injection_bipia_yi2024.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/slide06_indirect_prompt_injection_bipia_yi2024.png)
- **Nguồn gốc**: J. Yi et al., *"Benchmarking and Defending Against Indirect Prompt Injection Attacks on Large Language Models,"* in *Findings of ACL 2024* (Figure 1) [[3]](#ref3).
- **Kích thước**: $927 \times 420$ px | Dung lượng: $62.1\text{ KB}$ | Định dạng: PNG.
- **Tác dụng đối với đề tài**: Trực quan hóa rủi ro của hệ thống RAG và AI Agent khi nạp dữ liệu từ bên thứ ba (web, email). Dữ liệu chứa câu lệnh độc hại giấu kín sẽ kích hoạt tấn công ngay khi LLM đọc vào ngữ cảnh, chứng minh sự cần thiết phải có bộ lọc PI-Guard kiểm duyệt đầu vào độc lập.

---

### 4. Slide 8: Tầng Thiệt Hại 1 — Đánh Cắp Dữ Liệu Qua Kênh Phụ (Side-Channel Exfiltration)
![Slide 08: Tầng Thiệt Hại 1 — Đánh Cắp Dữ Liệu Qua Kênh Phụ (Greshake et al., ACM AISec 2023)](./slide08_layer1_data_exfiltration_greshake2023.png)
- **Tên tệp**: [`slide08_layer1_data_exfiltration_greshake2023.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/slide08_layer1_data_exfiltration_greshake2023.png)
- **Nguồn gốc**: K. Greshake et al., *"Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection,"* in *ACM AISec 2023* (Figure 4) [[4]](#ref4).
- **Kích thước**: $848 \times 545$ px | Dung lượng: $240.6\text{ KB}$ | Định dạng: PNG.
- **Tác dụng đối với đề tài**: Cung cấp bằng chứng thực nghiệm về cơ chế trích xuất dữ liệu nhạy cảm thông qua việc ép LLM sinh đường link Markdown chứa dữ liệu mật đính kèm truy vấn HTTP GET ra máy chủ kẻ tấn công.

---

### 5. Slide 9: Tầng Thiệt Hại 2 — Chiếm Đoạt Tác Tử AI Tự Hành (Agent Hijacking)
![Slide 09: Tầng Thiệt Hại 2 — Chiếm Đoạt Tác Tử AI Tự Hành (Greshake et al., ACM AISec 2023)](./slide09_layer2_agent_hijacking_greshake2023.png)
- **Tên tệp**: [`slide09_layer2_agent_hijacking_greshake2023.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/slide09_layer2_agent_hijacking_greshake2023.png)
- **Nguồn gốc**: K. Greshake et al., *ACM AISec 2023* (Figure 7: Remote Control Intrusion) [[4]](#ref4).
- **Kích thước**: $848 \times 545$ px | Dung lượng: $181.4\text{ KB}$ | Định dạng: PNG.
- **Tác dụng đối với đề tài**: Chứng minh khi LLM được tích hợp các công cụ tự hành (Tool Calling: gửi email, truy vấn database, chuyển tiền), một câu lệnh prompt injection có thể biến AI Agent thành backdoor độc hại thực thi lệnh tùy ý của tin tặc.

---

### 6. Slide 10: Tầng Thiệt Hại 3 — Tấn Công Cạn Kiệt Tài Nguyên & Chi Phí (Denial of Wallet — DoW)
![Slide 10: Tầng Thiệt Hại 3 — Denial of Wallet (Greshake et al., ACM AISec 2023)](./slide10_layer3_denial_of_wallet_greshake2023.png)
- **Tên tệp**: [`slide10_layer3_denial_of_wallet_greshake2023.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/slide10_layer3_denial_of_wallet_greshake2023.png)
- **Nguồn gốc**: K. Greshake et al., *ACM AISec 2023* (Figure 11: Availability Attacks) [[4]](#ref4).
- **Kích thước**: $848 \times 545$ px | Dung lượng: $217.1\text{ KB}$ | Định dạng: PNG.
- **Tác dụng đối với đề tài**: Minh chứng rủi ro tài chính trực tiếp khi kẻ tấn công ép mô hình sinh văn bản lặp đệ quy đạt giới hạn context window ($128\text{k tokens}$), gây nghẽn tài nguyên máy chủ và phát sinh hóa đơn API khổng lồ cho doanh nghiệp.

---

### 7. Slide 11: Tầng Thiệt Hại 4 — Trách Nhiệm Pháp Lý & Chế Tài EU AI Act
![Slide 11: Tầng Thiệt Hại 4 — Trách Nhiệm Pháp Lý & Chế Tài EU AI Act (Greshake et al., ACM AISec 2023)](./slide11_layer4_legal_compliance_greshake2023.png)
- **Tên tệp**: [`slide11_layer4_legal_compliance_greshake2023.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/slide11_layer4_legal_compliance_greshake2023.png)
- **Nguồn gốc**: K. Greshake et al., *ACM AISec 2023* (Figure 10: Content Manipulation Attacks) [[4]](#ref4).
- **Kích thước**: $848 \times 545$ px | Dung lượng: $338.5\text{ KB}$ | Định dạng: PNG.
- **Tác dụng đối với đề tài**: Nêu rõ rủi ro pháp lý khi chatbot bị lừa cam kết thông tin sai lệch (như tiền lệ tòa án xử phạt Air Canada năm 2024) và mức chế tài phạt lên tới $35\text{ triệu EUR}$ theo quy chế EU AI Act đối với các hệ thống AI tiềm ẩn rủi ro cao.

---

### 8. Slide 12: Threat Model & Ranh Giới Kiểm Duyệt Độc Lập Cho AI Agent
![Slide 12: Threat Model & Ranh Giới Kiểm Duyệt Độc Lập (Tencent Zhuque Lab 2026)](./slide12_threat_model_agent_surface_tencent2026.png)
- **Tên tệp**: [`slide12_threat_model_agent_surface_tencent2026.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/slide12_threat_model_agent_surface_tencent2026.png)
- **Nguồn gốc**: Tencent Zhuque Lab, *"AI-Infra-Guard: Multi-Layer Attack Surface and Defense Framework for AI Agents,"* *arXiv 2026* (Figure 1) [[5]](#ref5).
- **Kích thước**: $848 \times 545$ px | Dung lượng: $460.1\text{ KB}$ | Định dạng: PNG.
- **Tác dụng đối với đề tài**: Thiết lập mô hình hóa đe dọa đa tầng chuẩn mực cho toàn bộ đồ án: Định vị Zone 0 (Vùng không tin cậy), Zone 1 (Vành đai PI-Guard), Zone 2 (Lõi ứng dụng) và Zone 3 (Target LLM), đảm bảo nguyên lý Không Tin Tưởng Mặc Định (Zero-Trust Invariant).

---

### 9. Slide 14: Đối Sánh 3 Trường Phái Phòng Thủ SOTA Guardrails
![Slide 14: Đối Sánh 3 Trường Phái Phòng Thủ SOTA Guardrails (PI-Guard Survey)](./slide14_sota_guardrails_comparison_piguard.png)
- **Tên tệp**: [`slide14_sota_guardrails_comparison_piguard.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/slide14_sota_guardrails_comparison_piguard.png)
- **Nguồn gốc**: Nhóm nghiên cứu PI-Guard (Khảo sát đối chuẩn Literature Review).
- **Kích thước**: $2045 \times 692$ px | Dung lượng: $58.5\text{ KB}$ | Định dạng: PNG.
- **Tác dụng đối với đề tài**: Phân tích sự sụp đổ của Regex trước Leetspeak/Base64, sự quá tải tài nguyên và độ trễ cao của LLM-as-a-Judge (Llama Guard 3 cần GPU $>16\text{GB}$, độ trễ $>2\text{s}$), từ đó khẳng định ưu thế vượt trội của giải pháp Encoder Transformer (PI-Guard).

---

### 10. Slide 16: Tầng 1 — Cơ Chế Character N-Grams TF-IDF Baseline
![Slide 16: Tầng 1 — Cơ Chế Character N-Grams TF-IDF Baseline (Jain et al., 2023)](./slide16_tier1_tfidf_ngram_mechanism_jain2023.png)
- **Tên tệp**: [`slide16_tier1_tfidf_ngram_mechanism_jain2023.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/slide16_tier1_tfidf_ngram_mechanism_jain2023.png)
- **Nguồn gốc**: N. Jain et al., *"Baseline Defenses for Adversarial Attacks Against Aligned Language Models,"* *arXiv:2309.00614, 2023* [[6]](#ref6).
- **Kích thước**: $848 \times 545$ px | Dung lượng: $195.2\text{ KB}$ | Định dạng: PNG.
- **Tác dụng đối với đề tài**: Minh chứng cơ chế trích xuất $n$-grams ký tự con ($n=3,4,5$) giải quyết triệt để điểm mù phân mảnh từ vựng (Token Fragmentation) của Tokenizer BPE, phát hiện leetspeak (`1gn0r3`) trong $< 1\text{ms}$ trên CPU.

---

### 11. Slide 17: Tầng 2 — Cơ Chế Disentangled Attention DeBERTa-v3 & Lượng Hóa INT8
![Slide 17: Tầng 2 — Cơ Chế Disentangled Attention DeBERTa-v3 & ONNX INT8 (He et al., ICLR 2023)](./slide17_tier2_deberta_disentangled_onnx_he2023.png)
- **Tên tệp**: [`slide17_tier2_deberta_disentangled_onnx_he2023.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/slide17_tier2_deberta_disentangled_onnx_he2023.png)
- **Nguồn gốc**: P. He et al., *ICLR 2023* [[7]](#ref7) & Z. Yao et al., *NeurIPS 2022* [[8]](#ref8).
- **Kích thước**: $848 \times 545$ px | Dung lượng: $235.4\text{ KB}$ | Định dạng: PNG.
- **Tác dụng đối với đề tài**: Giải thích công thức tách biệt ma trận chú ý thành 2 vector (Nội dung $\mathbf{H}$ và Vị trí tương đối $\mathbf{P}$), giúp mô hình hiểu sâu ngữ nghĩa câu lệnh đảo ngữ và bẫy DAN phức tạp, đồng thời nén INT8 4x để đạt tốc độ suy luận CPU P95 $< 18.5\text{ms}$.

---

### 12. Slide 18: Kiến Trúc Phối Hợp 2 Tầng & Cơ Chế Định Tuyến Bất Định (Two-Tier Cascade)
![Slide 18: Kiến Trúc Phối Hợp 2 Tầng (Two-Tier Cascaded Architecture)](./slide18_twotier_cascaded_architecture_saltzer1975.png)
- **Tên tệp**: [`slide18_twotier_cascaded_architecture_saltzer1975.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/slide18_twotier_cascaded_architecture_saltzer1975.png)
- **Nguồn gốc**: Nhóm tác giả PI-Guard & Nguyên lý Saltzer-Schroeder (*Proc. IEEE 1975* [[9]](#ref9)).
- **Kích thước**: $1128 \times 893$ px | Dung lượng: $1.14\text{ MB}$ | Định dạng: PNG.
- **Tác dụng đối với đề tài**: Sơ đồ kiến trúc cốt lõi của toàn bộ hệ thống PI-Guard: Kỹ thuật Uncertainty Routing ($0.15 < P < 0.85$) và cơ chế Early Block/Fast Pass giúp tiết kiệm $80\%$ tải CPU, đạt trạng thái tối ưu Pareto (P95 $< 22\text{ms}$, FPR $< 1.0\%$, Zero-GPU).

---

### 13. Slide 19: Bảng Đối Sánh Thực Nghiệm ASR Trên Các Dòng LLM Thương Mại (BIPIA Table 2)
![Slide 19: Bảng Đối Sánh Thực Nghiệm ASR (Yi et al., ACL 2024 Table 2)](./slide19_bipia_table2_asr_llms_yi2024.png)
- **Tên tệp**: [`slide19_bipia_table2_asr_llms_yi2024.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/slide19_bipia_table2_asr_llms_yi2024.png)
- **Nguồn gốc**: J. Yi et al., *Findings of ACL 2024* (Table 2: Attack Success Rate across Commercial LLMs) [[3]](#ref3).
- **Kích thước**: $2045 \times 751$ px | Dung lượng: $168.7\text{ KB}$ | Định dạng: PNG.
- **Tác dụng đối với đề tài**: Cung cấp số liệu định lượng chứng minh ngay cả các mô hình tiên tiến nhất như GPT-4 hay Claude-2 đều có tỷ lệ sụp đổ an toàn ASR $> 80\%$ khi gặp tấn công tiêm prompt gián tiếp, khẳng định tính cấp thiết thực tiễn của đề tài PI-Guard.

---

## 📚 TÀI LIỆU THAM KHẢO HỌC THUẬT BẢO CHỨNG HÌNH ẢNH (REFERENCES)

- <a id="ref1"></a>**[1]** F. Perez and I. Ribeiro, *"Ignore Previous Prompt: Attack Techniques For Language Models,"* in *NeurIPS ML Safety Workshop*, 2022. [arXiv:2211.09527](https://arxiv.org/abs/2211.09527).
- <a id="ref2"></a>**[2]** X. Shen, Z. Chen, M. Backes, Y. Shen, and Y. Zhang, *"\"Do Anything Now\": Characterizing and Evaluating In-The-Wild Jailbreak Prompts on Large Language Models,"* in *Proceedings of the 2024 ACM SIGSAC Conference on Computer and Communications Security (ACM CCS '24)*, 2024, pp. 4172–4186. DOI: 10.1145/3658644.3670390. [PDF Open-Access](https://arxiv.org/abs/2308.03825).
- <a id="ref3"></a>**[3]** J. Yi, Y. Xie, L. Zhu, K. Chen, B. Chen, and Z. Sun, *"Benchmarking and Defending Against Indirect Prompt Injection Attacks on Large Language Models,"* in *Findings of the Association for Computational Linguistics (ACL 2024)*, 2024, pp. 10452–10471. [ACL Anthology](https://aclanthology.org/2024.findings-acl.621/).
- <a id="ref4"></a>**[4]** K. Greshake, S. Abdelnabi, S. Mishra, C. Endres, T. Holz, and M. Fritz, *"Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection,"* in *Proceedings of the 16th ACM Workshop on Artificial Intelligence and Security (ACM AISec '23)*, 2023, pp. 79–90. DOI: 10.1145/3605764.3623982. [PDF Open-Access](https://arxiv.org/abs/2302.12173).
- <a id="ref5"></a>**[5]** Tencent Zhuque Lab, *"AI-Infra-Guard: Multi-Layer Attack Surface and Defense Framework for AI Agents,"* *Tencent Security Technical Report*, 2026. [arXiv:2606.31227](https://arxiv.org/abs/2606.31227).
- <a id="ref6"></a>**[6]** N. Jain, A. Schwarzschild, Y. Wen, G. Thattai, J. Thickstun, and T. Goldstein, *"Baseline Defenses for Adversarial Attacks Against Aligned Language Models,"* *arXiv preprint arXiv:2309.00614*, 2023. [arXiv:2309.00614](https://arxiv.org/abs/2309.00614).
- <a id="ref7"></a>**[7]** P. He, X. Liu, J. Gao, and W. Chen, *"DeBERTa: Decoding-enhanced BERT with Disentangled Attention,"* in *International Conference on Learning Representations (ICLR)*, 2021/2023. [arXiv:2006.03654](https://arxiv.org/abs/2006.03654).
- <a id="ref8"></a>**[8]** Z. Yao, R. Y. Aminabadi, M. Zhang, X. Wu, C. Li, and Y. He, *"ZeroQuant: Efficient and Affordable Post-Training Quantization for Large-Scale Transformers,"* in *Advances in Neural Information Processing Systems (NeurIPS)*, vol. 35, 2022, pp. 27168–27183. [arXiv:2206.01861](https://arxiv.org/abs/2206.01861).
- <a id="ref9"></a>**[9]** J. H. Saltzer and M. D. Schroeder, *"The Protection of Information in Computer Systems,"* in *Proceedings of the IEEE*, vol. 63, no. 9, pp. 1278–1308, Sept. 1975. DOI: 10.1109/PROC.1975.9939. [IEEE Xplore Open-Access](https://web.mit.edu/Saltzer/www/publications/protection/).
