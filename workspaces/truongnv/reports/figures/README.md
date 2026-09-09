# HỒ SƠ METADATA & DANH MỤC HÌNH ẢNH HỌC THUẬT (SLIDE GẶP GVHD 10/09/2026)
## TẬP TIN TRÌNH CHIẾU GỐC: [`PI-GUARD-Present-109.pptx`](file:///d:/Work/Do-an/reports/PI-GUARD-Present-109.pptx)
### Dự án: PI-Guard — A Machine-Learning Guardrail for Detecting Prompt Injection and Jailbreak Attacks on LLM Applications
**Mã Đề Tài**: `IAP491_FA26_PI_GUARD` | **Ngày Báo Cáo GVHD**: 10/09/2026 | **Leader**: Nguyễn Văn Trường

---

> [!IMPORTANT]
> **TIÊU CHUẨN ĐỒNG BỘ DỮ LIỆU HÌNH ẢNH & MỤC ĐÍCH TÀI LIỆU**:
> - Toàn bộ 12 tệp hình ảnh kỹ thuật trong thư mục này được trích xuất trực tiếp từ bản trình chiếu PowerPoint báo cáo tiến độ gặp Giáo viên Hướng dẫn ngày 10/09/2026 ([`reports/PI-GUARD-Present-109.pptx`](file:///d:/Work/Do-an/reports/PI-GUARD-Present-109.pptx)).
> - **LƯU Ý QUAN TRỌNG**: Bộ slide này phục vụ **buổi báo cáo tiến độ định kỳ với GVHD ngày 10/09/2026**, **KHÔNG PHẢI slide báo cáo bảo vệ Review 1 trước Hội đồng**. Slide Review 1 chính thức sẽ được nhóm hoàn thiện và đóng gói riêng sau khi tiếp thu ý kiến định hướng từ GVHD.
> - **NGUYÊN TẮC KHÔNG TRÙNG LẶP HÌNH ẢNH (ZERO DUPLICATE INVARIANT)**: Slide 6 trong bài thuyết trình là slide đối sánh trực quan đặt song song 2 hình ảnh minh chứng từ Slide 4 và Slide 5. Nhóm giữ đúng 12 tệp ảnh độc nhất tương ứng với các hình gốc, không tạo tệp ảnh lặp lại nhằm đảm bảo sự tinh gọn và minh bạch của kho tài nguyên.
> - Danh mục tài liệu tham khảo được chuẩn hóa đồng bộ 100% với Slide 21 của bài thuyết trình, bao gồm đúng 8 công trình học thuật cốt lõi từ [1] đến [8].

---

## 📊 BẢNG TỔNG HỢP METADATA 12 HÌNH ẢNH KỸ THUẬT ĐỘC NHẤT

| STT | Tên Tệp Hình Ảnh | Slide | Định Dạng & Kích Thước | Nguồn Gốc Học Thuật (Tác Giả & Năm) | Tác Dụng & Vai Trò Kỹ Thuật Trong PI-Guard |
| :---: | :--- | :---: | :---: | :--- | :--- |
| **1** | [`slide04_promptinject_framework_perez2022.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/PI-GUARD-Present-109/slide04_promptinject_framework_perez2022.png) | Slide 4 | PNG ($927 \times 420$) | Perez & Ribeiro (NeurIPS 2022 [[1]](#ref1)) | Minh chứng tấn công Prompt Injection: Chiếm quyền điều khiển luồng lệnh (Control-Flow Hijacking) & Trích xuất System Prompt. |
| **2** | [`slide05_jailbreak_dan_structure_shen2024.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/PI-GUARD-Present-109/slide05_jailbreak_dan_structure_shen2024.png) | Slide 5 | PNG ($865 \times 708$) | Shen et al. (ACM CCS 2024 [[2]](#ref2)) | Minh chứng tấn công Jailbreak: Bẻ khóa chính sách an toàn (Safety Policy Bypass) bằng cấu trúc nhập vai DAN (Do Anything Now). |
| *--* | *(Slide 6: Đối sánh song song 2 họ tấn công)* | Slide 6 | *(Tích hợp Slide 4 & 5)* | Perez & Ribeiro (2022 [[1]](#ref1)) & Shen et al. (2024 [[2]](#ref2)) | Trực quan hóa đối sánh song song 2 họ tấn công: Tích hợp trực tiếp 2 hình ảnh tại Slide 4 và Slide 5, không tạo thêm tệp ảnh trùng. |
| **3** | [`slide08_layer1_data_exfiltration_greshake2023.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/PI-GUARD-Present-109/slide08_layer1_data_exfiltration_greshake2023.png) | Slide 8 | PNG ($848 \times 545$) | Greshake et al. (ACM AISec 2023 [[3]](#ref3)) | Phân tích Tầng Thiệt hại 1: Rò rỉ dữ liệu qua kênh phụ (Side-Channel Exfiltration), đánh cắp IP bí mật và Master API Key. |
| **4** | [`slide09_layer2_agent_hijacking_greshake2023.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/PI-GUARD-Present-109/slide09_layer2_agent_hijacking_greshake2023.png) | Slide 9 | PNG ($848 \times 545$) | Greshake et al. (ACM AISec 2023 [[3]](#ref3)) | Phân tích Tầng Thiệt hại 2: Chiếm đoạt tác tử tự hành (Autonomous Agent Hijacking), biến LLM thành mã độc nội bộ khi có quyền Tool Calling. |
| **5** | [`slide10_layer3_denial_of_wallet_greshake2023.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/PI-GUARD-Present-109/slide10_layer3_denial_of_wallet_greshake2023.png) | Slide 10 | PNG ($848 \times 545$) | Greshake et al. (ACM AISec 2023 [[3]](#ref3)) | Phân tích Tầng Thiệt hại 3: Tấn công từ chối ví tiền (Denial of Wallet — DoW), kích hoạt vòng lặp sinh token vô tận làm cạn kiệt ngân sách API. |
| **6** | [`slide11_layer4_legal_compliance_greshake2023.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/PI-GUARD-Present-109/slide11_layer4_legal_compliance_greshake2023.png) | Slide 11 | PNG ($848 \times 545$) | Greshake et al. (ACM AISec 2023 [[3]](#ref3)) | Phân tích Tầng Thiệt hại 4: Trách nhiệm pháp lý & chế tài EU AI Act (phạt 35M EUR) khi LLM bị thao túng đưa ra phát ngôn vi phạm chính sách. |
| **7** | [`slide12_threat_model_agent_surface_tencent2026.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/PI-GUARD-Present-109/slide12_threat_model_agent_surface_tencent2026.png) | Slide 12 | PNG ($848 \times 545$) | Tencent Zhuque Lab (2026 [[4]](#ref4)) | Thiết lập Threat Model 4 Vùng ranh giới tin cậy (Zone 0 - Zone 3) và vị trí đặt vành đai kiểm duyệt độc lập PI-Guard tại Zone 1. |
| **8** | [`slide14_sota_guardrails_comparison_piguard.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/PI-GUARD-Present-109/slide14_sota_guardrails_comparison_piguard.png) | Slide 14 | PNG ($2045 \times 692$) | Đề tài PI-Guard (Khảo sát SOTA) | Đối sánh 3 trường phái bảo vệ (Regex vs. Llama Guard 3 vs. ProtectAI vs. PI-Guard Encoder Transformers) về Độ trễ, Chi phí GPU và Độ bền vững. |
| **9** | [`slide16_tier1_tfidf_ngram_mechanism_jain2023.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/PI-GUARD-Present-109/slide16_tier1_tfidf_ngram_mechanism_jain2023.png) | Slide 16 | PNG ($848 \times 545$) | Jain et al. (arXiv 2023 [[5]](#ref5)) | Cơ chế Tầng 1: Trích xuất Character N-Grams ($n=3..5$) quét xuyên qua Leetspeak (`1gn0r3`) trong $< 1\text{ms}$ trên CPU thông thường. |
| **10** | [`slide17_tier2_deberta_disentangled_onnx_he2023.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/PI-GUARD-Present-109/slide17_tier2_deberta_disentangled_onnx_he2023.png) | Slide 17 | PNG ($848 \times 545$) | He et al. (ICLR 2023 [[6]](#ref6)) & Yao et al. (NeurIPS 2022 [[7]](#ref7)) | Cơ chế Tầng 2: Disentangled Attention tách biệt vector nội dung & vị trí tương đối, kết hợp lượng hóa ONNX INT8 đạt P95 $< 18.5\text{ms}$. |
| **11** | [`slide18_twotier_cascaded_architecture_saltzer1975.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/PI-GUARD-Present-109/slide18_twotier_cascaded_architecture_saltzer1975.png) | Slide 18 | PNG ($1128 \times 893$) | PI-Guard Architecture & Saltzer-Schroeder (1975 [[8]](#ref8)) | Kiến trúc phối hợp 2 tầng (Two-Tier Cascaded Guardrail) sử dụng Uncertainty Routing ($0.15 < P < 0.85$), đạt tối ưu Pareto (Zero-GPU). |
| **12** | [`slide19_matrix_2x2_unprotected_vs_piguard.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/PI-GUARD-Present-109/slide19_matrix_2x2_unprotected_vs_piguard.png) | Slide 19 | PNG ($2045 \times 751$) | Đề tài PI-Guard (Ma trận thực nghiệm) | Ma trận đánh giá thực nghiệm $2 \times 2$ Scenarios: Demo 1A/1B (Prompt Injection) & Demo 2A/2B (Jailbreak) so sánh Không Bảo Vệ vs. Có PI-Guard. |

---

## 🔍 CHI TIẾT TỪNG HÌNH ẢNH & TÁC DỤNG HỌC THUẬT

### 1. Slide 4: Khung Tấn Công PromptInject
![Slide 04: Khung Tấn Công PromptInject (Perez & Ribeiro, NeurIPS 2022)](./PI-GUARD-Present-109/slide04_promptinject_framework_perez2022.png)
- **Tên tệp**: [`slide04_promptinject_framework_perez2022.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/PI-GUARD-Present-109/slide04_promptinject_framework_perez2022.png)
- **Nguồn gốc**: F. Perez và I. Ribeiro, *"Ignore Previous Prompt: Attack Techniques For Language Models,"* in *NeurIPS ML Safety Workshop*, 2022 [[1]](#ref1).
- **Kích thước**: $927 \times 420$ px | Dung lượng: $69.5\text{ KB}$ | Định dạng: PNG.
- **Tác dụng đối với đề tài**: Minh chứng bản chất của tấn công **Prompt Injection** là tấn công chiếm quyền luồng điều khiển (Control-Flow Hijacking). Kẻ tấn công lợi dụng việc LLM hòa trộn System Instruction và User Data thành chuỗi token phẳng để ghi đè chỉ thị ban đầu, ép LLM in ra mã nguồn/prompt bí mật.

---

### 2. Slide 5: Cấu Trúc Câu Lệnh Bẻ Khóa DAN (Do Anything Now)
![Slide 05: Cấu Trúc Câu Lệnh Bẻ Khóa DAN (Shen et al., ACM CCS 2024)](./PI-GUARD-Present-109/slide05_jailbreak_dan_structure_shen2024.png)
- **Tên tệp**: [`slide05_jailbreak_dan_structure_shen2024.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/PI-GUARD-Present-109/slide05_jailbreak_dan_structure_shen2024.png)
- **Nguồn gốc**: X. Shen, Z. Chen, M. Backes, Y. Shen, và Y. Zhang, *"\"Do Anything Now\": Characterizing and Evaluating In-The-Wild Jailbreak Prompts on Large Language Models,"* in *ACM CCS 2024* [[2]](#ref2).
- **Kích thước**: $865 \times 708$ px | Dung lượng: $126.8\text{ KB}$ | Định dạng: PNG.
- **Tác dụng đối với đề tài**: Minh chứng bản chất của **Jailbreak** là bẻ khóa căn chỉnh an toàn nội tại (Safety Alignment / RLHF). Bằng cách tạo dựng nhân vật ảo "DAN" không bị ràng buộc đạo đức, câu lệnh ép LLM vi phạm chính sách nội dung (vũ khí, mã độc) mà không cần thay đổi logic ứng dụng.

---

### * (Slide 6): Đối Sánh Song Song 2 Họ Tấn Công (Tích Hợp Slide 4 & 5)
*Slide 6 đặt song song 2 hình ảnh minh chứng từ Slide 4 ([`slide04_promptinject_framework_perez2022.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/PI-GUARD-Present-109/slide04_promptinject_framework_perez2022.png)) và Slide 5 ([`slide05_jailbreak_dan_structure_shen2024.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/PI-GUARD-Present-109/slide05_jailbreak_dan_structure_shen2024.png)) để làm nổi bật sự khác biệt giữa hai bề mặt tấn công. Để tránh dư thừa dữ liệu, không tạo tệp hình ảnh riêng cho Slide 6.*

---

### 3. Slide 8: Tầng Thiệt Hại 1 — Đánh Cắp Dữ Liệu Qua Kênh Phụ (Side-Channel Exfiltration)
![Slide 08: Tầng Thiệt Hại 1 — Đánh Cắp Dữ Liệu Qua Kênh Phụ (Greshake et al., ACM AISec 2023)](./PI-GUARD-Present-109/slide08_layer1_data_exfiltration_greshake2023.png)
- **Tên tệp**: [`slide08_layer1_data_exfiltration_greshake2023.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/PI-GUARD-Present-109/slide08_layer1_data_exfiltration_greshake2023.png)
- **Nguồn gốc**: K. Greshake et al., *"Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection,"* in *ACM AISec 2023* (Figure 4) [[3]](#ref3).
- **Kích thước**: $848 \times 545$ px | Dung lượng: $240.6\text{ KB}$ | Định dạng: PNG.
- **Tác dụng đối với đề tài**: Cung cấp bằng chứng thực nghiệm về cơ chế trích xuất dữ liệu nhạy cảm thông qua việc ép LLM sinh đường link Markdown chứa dữ liệu mật đính kèm truy vấn HTTP GET ra máy chủ kẻ tấn công.

---

### 4. Slide 9: Tầng Thiệt Hại 2 — Chiếm Đoạt Tác Tử AI Tự Hành (Agent Hijacking)
![Slide 09: Tầng Thiệt Hại 2 — Chiếm Đoạt Tác Tử AI Tự Hành (Greshake et al., ACM AISec 2023)](./PI-GUARD-Present-109/slide09_layer2_agent_hijacking_greshake2023.png)
- **Tên tệp**: [`slide09_layer2_agent_hijacking_greshake2023.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/PI-GUARD-Present-109/slide09_layer2_agent_hijacking_greshake2023.png)
- **Nguồn gốc**: K. Greshake et al., *ACM AISec 2023* (Figures 6 & 8: Remote Control Intrusion) [[3]](#ref3).
- **Kích thước**: $848 \times 545$ px | Dung lượng: $181.4\text{ KB}$ | Định dạng: PNG.
- **Tác dụng đối với đề tài**: Chứng minh khi LLM được tích hợp các công cụ tự hành (Tool Calling: gửi email, truy vấn database, chuyển tiền), một câu lệnh prompt injection có thể biến AI Agent thành backdoor độc hại thực thi lệnh tùy ý của tin tặc.

---

### 5. Slide 10: Tầng Thiệt Hại 3 — Tấn Công Cạn Kiệt Tài Nguyên & Chi Phí (Denial of Wallet — DoW)
![Slide 10: Tầng Thiệt Hại 3 — Denial of Wallet (Greshake et al., ACM AISec 2023)](./PI-GUARD-Present-109/slide10_layer3_denial_of_wallet_greshake2023.png)
- **Tên tệp**: [`slide10_layer3_denial_of_wallet_greshake2023.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/PI-GUARD-Present-109/slide10_layer3_denial_of_wallet_greshake2023.png)
- **Nguồn gốc**: K. Greshake et al., *ACM AISec 2023* (Figures 11 & 12: Availability Attacks) [[3]](#ref3).
- **Kích thước**: $848 \times 545$ px | Dung lượng: $217.1\text{ KB}$ | Định dạng: PNG.
- **Tác dụng đối với đề tài**: Minh chứng rủi ro tài chính trực tiếp khi kẻ tấn công ép mô hình sinh văn bản lặp đệ quy đạt giới hạn context window ($128\text{k tokens}$), gây nghẽn tài nguyên máy chủ và phát sinh hóa đơn API khổng lồ cho doanh nghiệp.

---

### 6. Slide 11: Tầng Thiệt Hại 4 — Trách Nhiệm Pháp Lý & Chế Tài EU AI Act
![Slide 11: Tầng Thiệt Hại 4 — Trách Nhiệm Pháp Lý & Chế Tài EU AI Act (Greshake et al., ACM AISec 2023)](./PI-GUARD-Present-109/slide11_layer4_legal_compliance_greshake2023.png)
- **Tên tệp**: [`slide11_layer4_legal_compliance_greshake2023.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/PI-GUARD-Present-109/slide11_layer4_legal_compliance_greshake2023.png)
- **Nguồn gốc**: K. Greshake et al., *ACM AISec 2023* (Section 4.2.5: Content Manipulation Attacks) [[3]](#ref3).
- **Kích thước**: $848 \times 545$ px | Dung lượng: $338.5\text{ KB}$ | Định dạng: PNG.
- **Tác dụng đối với đề tài**: Nêu rõ rủi ro pháp lý khi chatbot bị lừa cam kết thông tin sai lệch (như tiền lệ tòa án xử phạt Air Canada năm 2024) và mức chế tài phạt lên tới $35\text{ triệu EUR}$ theo quy chế EU AI Act đối với các hệ thống AI tiềm ẩn rủi ro cao.

---

### 7. Slide 12: Threat Model & Ranh Giới Kiểm Duyệt Độc Lập Cho AI Agent
![Slide 12: Threat Model & Ranh Giới Kiểm Duyệt Độc Lập (Tencent Zhuque Lab 2026)](./PI-GUARD-Present-109/slide12_threat_model_agent_surface_tencent2026.png)
- **Tên tệp**: [`slide12_threat_model_agent_surface_tencent2026.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/PI-GUARD-Present-109/slide12_threat_model_agent_surface_tencent2026.png)
- **Nguồn gốc**: C. Xiao et al. and Tencent Zhuque Lab, *"Securing the AI Agent: A Unified Framework for Multi-Layer Agent Red Teaming,"* *Tencent Security Technical Report / arXiv:2606.31227*, 2026 (Figure 1) [[4]](#ref4).
- **Kích thước**: $848 \times 545$ px | Dung lượng: $460.1\text{ KB}$ | Định dạng: PNG.
- **Tác dụng đối với đề tài**: Thiết lập mô hình hóa đe dọa đa tầng chuẩn mực cho toàn bộ đồ án: Định vị Zone 0 (Vùng không tin cậy), Zone 1 (Vành đai PI-Guard), Zone 2 (Lõi ứng dụng) và Zone 3 (Target LLM), đảm bảo nguyên lý Không Tin Tưởng Mặc Định (Zero-Trust Invariant).

---

### 8. Slide 14: Đối Sánh 3 Trường Phái Phòng Thủ SOTA Guardrails
![Slide 14: Đối Sánh 3 Trường Phái Phòng Thủ SOTA Guardrails (PI-Guard Survey)](./PI-GUARD-Present-109/slide14_sota_guardrails_comparison_piguard.png)
- **Tên tệp**: [`slide14_sota_guardrails_comparison_piguard.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/PI-GUARD-Present-109/slide14_sota_guardrails_comparison_piguard.png)
- **Nguồn gốc**: Nhóm nghiên cứu PI-Guard (Khảo sát đối chuẩn Literature Review).
- **Kích thước**: $2045 \times 692$ px | Dung lượng: $58.5\text{ KB}$ | Định dạng: PNG.
- **Tác dụng đối với đề tài**: Phân tích sự sụp đổ của Regex trước Leetspeak/Base64, sự quá tải tài nguyên và độ trễ cao của LLM-as-a-Judge (Llama Guard 3 cần GPU $>16\text{GB}$, độ trễ $>2\text{s}$), từ đó khẳng định ưu thế vượt trội của giải pháp Encoder Transformer (PI-Guard).

---

### 9. Slide 16: Tầng 1 — Cơ Chế Character N-Grams TF-IDF Baseline
![Slide 16: Tầng 1 — Cơ Chế Character N-Grams TF-IDF Baseline (Jain et al., 2023)](./PI-GUARD-Present-109/slide16_tier1_tfidf_ngram_mechanism_jain2023.png)
- **Tên tệp**: [`slide16_tier1_tfidf_ngram_mechanism_jain2023.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/PI-GUARD-Present-109/slide16_tier1_tfidf_ngram_mechanism_jain2023.png)
- **Nguồn gốc**: N. Jain et al., *"Baseline Defenses for Adversarial Attacks Against Aligned Language Models,"* *arXiv:2309.00614, 2023* [[5]](#ref5).
- **Kích thước**: $848 \times 545$ px | Dung lượng: $195.2\text{ KB}$ | Định dạng: PNG.
- **Tác dụng đối với đề tài**: Minh chứng cơ chế trích xuất $n$-grams ký tự con ($n=3,4,5$) giải quyết triệt để điểm mù phân mảnh từ vựng (Token Fragmentation) của Tokenizer BPE, phát hiện leetspeak (`1gn0r3`) trong $< 1\text{ms}$ trên CPU.

---

### 10. Slide 17: Tầng 2 — Cơ Chế Disentangled Attention DeBERTa-v3 & Lượng Hóa INT8
![Slide 17: Tầng 2 — Cơ Chế Disentangled Attention DeBERTa-v3 & ONNX INT8 (He et al., ICLR 2023)](./PI-GUARD-Present-109/slide17_tier2_deberta_disentangled_onnx_he2023.png)
- **Tên tệp**: [`slide17_tier2_deberta_disentangled_onnx_he2023.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/PI-GUARD-Present-109/slide17_tier2_deberta_disentangled_onnx_he2023.png)
- **Nguồn gốc**: P. He et al., *ICLR 2023* [[6]](#ref6) & Z. Yao et al., *NeurIPS 2022* [[7]](#ref7).
- **Kích thước**: $848 \times 545$ px | Dung lượng: $235.4\text{ KB}$ | Định dạng: PNG.
- **Tác dụng đối với đề tài**: Giải thích công thức tách biệt ma trận chú ý thành 2 vector (Nội dung $\mathbf{H}$ và Vị trí tương đối $\mathbf{P}$), giúp mô hình hiểu sâu ngữ nghĩa câu lệnh đảo ngữ và bẫy DAN phức tạp, đồng thời nén INT8 4x để đạt tốc độ suy luận CPU P95 $< 18.5\text{ms}$.

---

### 11. Slide 18: Kiến Trúc Phối Hợp 2 Tầng & Cơ Chế Định Tuyến Bất Định (Two-Tier Cascade)
![Slide 18: Kiến Trúc Phối Hợp 2 Tầng (Two-Tier Cascaded Architecture)](./PI-GUARD-Present-109/slide18_twotier_cascaded_architecture_saltzer1975.png)
- **Tên tệp**: [`slide18_twotier_cascaded_architecture_saltzer1975.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/PI-GUARD-Present-109/slide18_twotier_cascaded_architecture_saltzer1975.png)
- **Nguồn gốc**: Nhóm tác giả PI-Guard & Nguyên lý Saltzer-Schroeder (*Proc. IEEE 1975* [[8]](#ref8)).
- **Kích thước**: $1128 \times 893$ px | Dung lượng: $1.14\text{ MB}$ | Định dạng: PNG.
- **Tác dụng đối với đề tài**: Sơ đồ kiến trúc cốt lõi của toàn bộ hệ thống PI-Guard: Kỹ thuật Uncertainty Routing ($0.15 < P < 0.85$) và cơ chế Early Block/Fast Pass giúp tiết kiệm $80\%$ tải CPU, đạt trạng thái tối ưu Pareto (P95 $< 22\text{ms}$, FPR $< 1.0\%$, Zero-GPU).

---

### 12. Slide 19: Ma Trận Đánh Giá Thực Nghiệm 4 Kịch Bản ($2 \times 2$ Evaluation Matrix)
![Slide 19: Ma Trận Thực Nghiệm 2x2 (Unprotected vs. PI-Guard Protected)](./PI-GUARD-Present-109/slide19_matrix_2x2_unprotected_vs_piguard.png)
- **Tên tệp**: [`slide19_matrix_2x2_unprotected_vs_piguard.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/PI-GUARD-Present-109/slide19_matrix_2x2_unprotected_vs_piguard.png)
- **Nguồn gốc**: Nhóm tác giả PI-Guard (Bảng kịch bản thực nghiệm Slide 19).
- **Kích thước**: $2045 \times 751$ px | Dung lượng: $168.7\text{ KB}$ | Định dạng: PNG.
- **Tác dụng đối với đề tài**: Minh chứng sự đối lập rõ ràng giữa hai trạng thái hệ thống:
  - **Kịch bản 1 (Prompt Injection)**: Demo 1A bị khai thác (lộ Master Key `ABC-SEC-998877`) $\leftrightarrow$ Demo 1B được PI-Guard bảo vệ an toàn (chặn bằng HTTP 403 Forbidden trong $14.8\text{ms}$, Risk Score $0.964$).
  - **Kịch bản 2 (Jailbreak DAN Mode)**: Demo 2A bị bẻ khóa (sinh mã độc tống tiền Ransomware) $\leftrightarrow$ Demo 2B bị PI-Guard vô hiệu hóa tại vành đai ngoài (Risk Score $0.942$, chặn trong $13.5\text{ms}$).

---

## 📚 TÀI LIỆU THAM KHẢO HỌC THUẬT BẢO CHỨNG HÌNH ẢNH (REFERENCES)

- <a id="ref1"></a>**[1]** F. Perez and I. Ribeiro, *"Ignore Previous Prompt: Attack Techniques For Language Models,"* in *NeurIPS ML Safety Workshop*, 2022. [arXiv:2211.09527](https://arxiv.org/abs/2211.09527).
- <a id="ref2"></a>**[2]** X. Shen, Z. Chen, M. Backes, Y. Shen, and Y. Zhang, *"\"Do Anything Now\": Characterizing and Evaluating In-The-Wild Jailbreak Prompts on Large Language Models,"* in *Proceedings of the 2024 ACM SIGSAC Conference on Computer and Communications Security (ACM CCS '24)*, 2024, pp. 4172–4186. DOI: 10.1145/3658644.3670390. [PDF Open-Access](https://arxiv.org/abs/2308.03825).
- <a id="ref3"></a>**[3]** K. Greshake, S. Abdelnabi, S. Mishra, C. Endres, T. Holz, and M. Fritz, *"Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection,"* in *Proceedings of the 16th ACM Workshop on Artificial Intelligence and Security (ACM AISec '23)*, 2023, pp. 79–90. DOI: 10.1145/3605764.3623982. [PDF Open-Access](https://arxiv.org/abs/2302.12173).
- <a id="ref4"></a>**[4]** C. Xiao et al. and Tencent Zhuque Lab, *"Securing the AI Agent: A Unified Framework for Multi-Layer Agent Red Teaming,"* *Tencent Security Technical Report / arXiv:2606.31227*, 2026. [arXiv:2606.31227](https://arxiv.org/abs/2606.31227).
- <a id="ref5"></a>**[5]** N. Jain, A. Schwarzschild, Y. Wen, G. Thattai, J. Thickstun, and T. Goldstein, *"Baseline Defenses for Adversarial Attacks Against Aligned Language Models,"* *arXiv preprint arXiv:2309.00614*, 2023. [arXiv:2309.00614](https://arxiv.org/abs/2309.00614).
- <a id="ref6"></a>**[6]** P. He, X. Liu, J. Gao, and W. Chen, *"DeBERTa: Decoding-enhanced BERT with Disentangled Attention,"* in *International Conference on Learning Representations (ICLR)*, 2021/2023. [arXiv:2006.03654](https://arxiv.org/abs/2006.03654).
- <a id="ref7"></a>**[7]** Z. Yao, R. Y. Aminabadi, M. Zhang, X. Wu, C. Li, and Y. He, *"ZeroQuant: Efficient and Affordable Post-Training Quantization for Large-Scale Transformers,"* in *Advances in Neural Information Processing Systems (NeurIPS)*, vol. 35, 2022, pp. 27168–27183. [arXiv:2206.01861](https://arxiv.org/abs/2206.01861).
- <a id="ref8"></a>**[8]** J. H. Saltzer and M. D. Schroeder, *"The Protection of Information in Computer Systems,"* in *Proceedings of the IEEE*, vol. 63, no. 9, pp. 1278–1308, Sept. 1975. DOI: 10.1109/PROC.1975.9939. [IEEE Xplore Open-Access](https://web.mit.edu/Saltzer/www/publications/protection/).
