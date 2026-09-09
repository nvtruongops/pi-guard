# CHAPTER 1: INTRODUCTION

## 1.1. Background (Bối Cảnh Nghiên Cứu)
Sự bùng nổ của các Mô hình Ngôn ngữ Lớn (Large Language Models - LLMs) như GPT-4, LLaMA-3, Claude, và Gemini đã định hình lại toàn bộ hệ sinh thái phần mềm hiện đại [[1]](#ref1). LLM hiện được tích hợp sâu vào các ứng dụng doanh nghiệp: từ chatbot chăm sóc khách hàng, hệ thống trích xuất thông tin tự động (Retrieval-Augmented Generation - RAG), đến các tác tử AI tự trị (Autonomous AI Agents) có khả năng gọi hàm (tool execution) và truy cập cơ sở dữ liệu nội bộ [[2]](#ref2).

Tuy nhiên, việc triển khai LLM trong thực tế làm phát sinh những lỗ hổng bảo mật hoàn toàn mới mà các giải pháp tường lửa (WAF), IDS/IPS truyền thống không thể phát hiện. Trong bảng xếp hạng bảo mật quốc tế **OWASP Top 10 for Large Language Model Applications (2025)** [[8]](#ref8) và báo cáo **NIST AI 100-2e2025** [[7]](#ref7), lỗ hổng **Prompt Injection và Jailbreak (LLM01)** được xếp ở vị trí nguy hiểm số 1. Kẻ tấn công có thể thao túng mô hình ngôn ngữ chỉ bằng các câu lệnh văn bản tự nhiên được thiết kế tinh vi, dẫn đến rò rỉ bí mật kinh doanh nhúng trong System Prompt, chiếm quyền điều khiển luồng thực thi (Goal Hijacking), hoặc ép mô hình vượt qua các rào cản đạo đức để sinh mã độc.

---

## 1.2. Problem Statement (Phát Biểu Bài Toán)
Vấn đề cốt lõi của các mô hình Transformer hiện nay bắt nguồn từ sự tương đồng với **"Lỗ hổng kiến trúc Von Neumann trong xử lý ngôn ngữ tự nhiên"** [[1]](#ref1), [[3]](#ref3):

```
┌─────────────────────────────────────────────────────────────┐
│                       INPUT CONTEXT                         │
│  ┌─────────────────────────────────┐ ┌───────────────────┐  │
│  │ System Prompt (Chỉ thị/Rules)  │ │ User Prompt (Data)│  │
│  └─────────────────────────────────┘ └───────────────────┘  │
└──────────────────────────────┬──────────────────────────────┘
                               │ Ghép chung thành 1 chuỗi Token phẳng
                               ▼
             ┌──────────────────────────────────────┐
             │   LLM Transformer Next-Token Engine  │
             │   (Không có ranh giới phần cứng)     │
             └──────────────────────────────────────┘
```

1. **Lẫn lộn giữa Lệnh và Dữ liệu (Instruction/Data Ambiguity)**: Trong cơ chế Self-Attention của Transformer, System Instruction (chỉ thị điều khiển) và User Input (dữ liệu đầu vào) bị ghép chung thành một chuỗi token phẳng ($X = S \mathbin{\Vert} U$). Mô hình không có cơ chế phân tách phần cứng hay quyền hạn (Privilege Separation) giữa dữ liệu và câu lệnh.
2. **Sự thất bại của các bộ lọc từ khóa tĩnh (Keyword Blacklist Failure)**: Các bộ quy tắc Regex/Blacklist thông thường dễ dàng bị kẻ tấn công vô hiệu hóa thông qua các kỹ thuật đột biến cú pháp: chèn ký tự leetspeak (`1gn0r3`), phân tách khoảng trắng (`i g n o r e`), mã hóa Base64/Cipher [[17]](#ref17), hoặc bọc trong các kịch bản nhập vai phức tạp (DAN / Roleplay Jailbreak) [[12]](#ref12), [[15]](#ref15).
3. **Nghịch lý của giải pháp LLM-as-a-Judge**: Việc sử dụng một LLM lớn khác (ví dụ: Llama Guard 3 8B) để kiểm tra prompt gây ra độ trễ quá lớn (>500ms đến 1.5s), tiêu tốn tài nguyên phần cứng (>16GB VRAM GPU) và chi phí vận hành API quá cao, không khả thi cho môi trường sản xuất có lưu lượng truy cập lớn [[9]](#ref9), [[10]](#ref10).

Do đó, bài toán cấp thiết đặt ra là: **Cần xây dựng một cơ chế Guardrail chuyên biệt sử dụng Machine Learning / Transformer nhỏ gọn, đặt ngay tại cổng API, có khả năng phân loại ngữ nghĩa sâu với độ trễ thấp (P95 < 30ms trên CPU), tỷ lệ chặn nhầm cực thấp (FPR < 1.5%), và có độ bền cao trước các kỹ thuật lẩn tránh cú pháp (Leetspeak, Base64, Spacing).**

---

## 1.3. Research Objectives & Research Questions (Mục Tiêu & 3 Câu Hỏi Nghiên Cứu)

### 1.3.1. Mục Tiêu Tổng Quát:
Thiết kế, huấn luyện, lượng hóa và triển khai hệ thống **PI-Guard** — Lớp phòng thủ Guardrail dạng API Middleware trực tuyến đặt trước các ứng dụng LLM để phát hiện và ngăn chặn hai vector tấn công chính: **Prompt Injection** và **Jailbreak**.

### 1.3.2. Các Mục Tiêu Cụ Thể (Specific Deliverables):
1. **Bộ dữ liệu chuẩn hóa**: Xây dựng tập dữ liệu đa nguồn (Deepset, Gandalf, In-The-Wild, Benign) áp dụng thuật toán *Group-Aware Splitting* chống rò rỉ dữ liệu.
2. **Mô hình học máy kép**: Phát triển mô hình Baseline ML (Word/Char TF-IDF) và mô hình Transformer tinh chỉnh (`microsoft/deberta-v3-base` Disentangled Attention).
3. **Độ bền trước lẩn tránh cú pháp**: Xây dựng cơ chế chuẩn hóa chuỗi và bộ kiểm thử độ bền (Adversarial Robustness Testing Suite) kháng Leetspeak, Base64, Spacing.
4. **Tối ưu hóa triển khai thực tế**: Ứng dụng kỹ thuật lượng hóa nhẹ (Post-Training Dynamic INT8 Quantization với ONNX Runtime) như một giải pháp phụ trợ kỹ thuật, đảm bảo Guardrail vận hành hiệu quả trên hạ tầng CPU tiêu chuẩn với độ trễ thấp.
5. **Hạ tầng API & Dashboard**: Xây dựng Asynchronous Middleware (FastAPI) và Dashboard kiểm thử trực quan (Streamlit) với ma trận 4 kịch bản demo.

### 1.3.3. Hệ Thống 3 Câu Hỏi Nghiên Cứu Cốt Lõi (RQ1 - RQ3):

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│               HỆ THỐNG 3 CÂU HỎI NGHIÊN CỨU CỐT LÕI (CHUYÊN NGÀNH ATTT)                │
├──────┬──────────────────────────────────────────┬──────────────────────────────────────┤
│ Mã   │ Tên Trọng Tâm Nghiên Cứu                 │ Khoảng Trống Nghiên Cứu Cốt Lõi      │
├──────┼──────────────────────────────────────────┼──────────────────────────────────────┤
│ RQ1  │ Phân Loại Mối Đe Dọa & Chống Rò Rỉ Dữ Liệu│ Rò rỉ cụm mẫu & Ranh giới phân loại  │
│      │ (Threat Modeling & Representation)       │ giữa cú pháp tĩnh và ngữ nghĩa sâu   │
├──────┼──────────────────────────────────────────┼──────────────────────────────────────┤
│ RQ2  │ Độ Bền Kháng Lẩn Tránh & Mã Hóa Đối Kháng │ Sự sụp đổ của mô hình trước biến dị  │
│      │ (Adversarial Robustness & Ciphers)       │ cú pháp Leetspeak, Spacing & Base64  │
├──────┼──────────────────────────────────────────┼──────────────────────────────────────┤
│ RQ3  │ Cân Bằng An Toàn & Khả Thi Triển Khai    │ Đánh đổi Security/Usability (FPR) và │
│      │ (Security Trade-off & Inline Feasibility)│ bảo toàn ranh giới an toàn khi nén   │
└──────┴──────────────────────────────────────────┴──────────────────────────────────────┘
```

#### 📌 RQ1 — Biểu Diễn Mối Đe Dọa, Khử Rò Rỉ Dữ Liệu & Ranh Giới Phân Loại Ngữ Nghĩa:
- **Câu hỏi**: *Làm thế nào để xây dựng một phương pháp luận phân chia dữ liệu bảo toàn cụm (Group-Aware Splitting) nhằm triệt tiêu hiện tượng rò rỉ dữ liệu giữa các biến thể tấn công, và sự kết hợp giữa mô hình học máy cổ điển (TF-IDF) với Transformer phân tách vị trí ngữ nghĩa (DeBERTa-v3) nâng cao khả năng phát hiện các đòn tấn công Prompt Injection và Jailbreak vượt trội hơn các mô hình phòng thủ SOTA hiện nay ở mức độ nào?*
- **Chỉ số đo lường**: $\text{Inter-cluster Jaccard} < 0.15$, $\text{Macro } F_1^{\text{OOD}} \ge 0.92$, $\text{Macro } F_1 \ge 0.95$ (kỳ vọng $> 0.98$), $\text{PR-AUC} \ge 0.98$.

#### 📌 RQ2 — Độ Bền Của Hệ Thống Trước Các Kỹ Thuật Lẩn Tránh & Mã Hóa Đối Kháng:
- **Câu hỏi**: *Hệ thống phòng thủ đa tầng (kết hợp tiền xử lý chuẩn hóa chuỗi, biểu diễn n-gram ký tự và token hóa subword) duy trì độ bền và độ chính xác như thế nào trước các kỹ thuật lẩn tránh đối kháng có cấu trúc (gồm thay thế ký tự Leetspeak, phân tách khoảng trắng và mã hóa Base64/Cipher), và mức độ suy giảm hiệu năng tối đa có thể định lượng được là bao nhiêu?*
- **Chỉ số đo lường**: $\text{ARR} = \frac{F_1^{\text{Adversarial}}}{F_1^{\text{Clean}}} \ge 0.95$, $\text{ASR} < 5\%$, $\Delta F_1 = |F_1^{\text{Clean}} - F_1^{\text{Adv}}| < 5\%$.

#### 📌 RQ3 — Cân Bằng An Toàn, Khống Chế Tỷ Lệ Chặn Nhầm & Bảo Toàn Ranh Giới Khi Lượng Hóa:
- **Câu hỏi**: *Làm thế nào để tối ưu hóa cơ chế thiết lập ngưỡng chính sách nhằm khống chế nghiêm ngặt Tỷ lệ Chặn Nhầm (FPR < 1.5%) trên các truy vấn hợp lệ của doanh nghiệp, và quá trình lượng hóa động INT8 cùng kiến trúc proxy bất đồng bộ có thể bảo toàn ranh giới quyết định an toàn trong khi duy trì độ trễ thấp tối ưu (P95 < 30ms trên CPU) mà không tạo ra điểm nghẽn từ chối dịch vụ (DoS)?*
- **Chỉ số đo lường**: $\text{FPR} < 1.5\%$ (kỳ vọng $< 1.1\%$), $\Delta \text{Decision Boundary (KL)} < 0.05$, $\Delta F_1^{\text{Quant}} < 0.3\%$, $\text{P95 Latency} < 30\text{ms}$ trên CPU.

---

## 1.4. Significance of the Study & Threat Impact Analysis (Ý Nghĩa & Phân Tích Thiệt Hại)

### 1.4.1. 4 Tầng Thiệt Hại Thực Tế Của Các Cuộc Tấn Công LLM
1. **Thiệt hại 1: Rò rỉ Bí mật Trí tuệ (IP) & Master API Key**: System prompt chứa logic nghiệp vụ độc quyền và API credential nội bộ. Khi bị trích xuất, doanh nghiệp mất hoàn toàn lợi thế cạnh tranh và bị tin tặc lợi dụng API key.
2. **Thiệt hại 2: Chiếm quyền điều khiển Tác tử AI (Goal Hijacking & Unauthorized Actions)**: Khi LLM Agent có quyền gọi tool, một câu lệnh indirect injection ẩn trong tài liệu có thể ép Agent chuyển tiền trái phép hoặc xóa sạch database của khách hàng.
3. **Thiệt hại 3: Tấn công cạn kiệt tài nguyên & Chi phí ví tiền (Denial-of-Wallet / Compute Exhaustion)**: Bơm prompt ép mô hình sinh văn bản lặp vô tận, gây hóa đơn API hàng chục nghìn USD mỗi ngày.
4. **Thiệt hại 4: Vi phạm chế tài pháp lý & Mất uy tín thương hiệu (Regulatory Compliance Fines)**: Ép AI sinh mã độc hoặc nội dung cấm dẫn đến vi phạm EU AI Act, GDPR và sụp đổ niềm tin người dùng.

### 1.4.2. Ý Nghĩa Khoa Học & Thực Tiễn Của PI-Guard
- **Khoa học**: Chứng minh tính ưu việt của cơ chế *Disentangled Attention* trong nhận diện trật tự đảo câu, giải quyết bài toán chống rò rỉ dữ liệu qua *Group-Aware Splitting*, và chứng minh tính hiệu quả của *Character n-grams* trong kháng nhiễu Leetspeak.
- **Thực tiễn**: Đóng gói thành giải pháp Plug-and-Play (FastAPI Middleware) chi phí $0, độ trễ thấp <30ms trên CPU, đánh chặn các đòn tấn công trước khi chạm vào LLM.

---

## 1.5. Scope and Limitations (Ranh Giới Phạm Vi & Giới Hạn Đề Tài)

```
┌──────────────────────────────────────────────────────────────────────────┐
│                   IN-SCOPE (TRỌNG TÂM NGHIÊN CỨU)                        │
│  - 2 Bài toán cốt lõi: Prompt Injection (Direct/Indirect) & Jailbreak    │
│  - Chuỗi văn bản đầu vào: English Text Prompts (Tiêu chuẩn nghiên cứu)   │
│  - Kỹ thuật lẩn tránh cú pháp: Leetspeak, Base64, Spacing (Test độ bền)  │
│  - Độ trễ thấp (Low-latency): P95 Latency < 30ms trên CPU thông thường   │
│  - An toàn vận hành: False Positive Rate (FPR) < 1.5% trên tập Benign    │
│  - Kiến trúc: Hybrid TF-IDF Baseline + Fine-tuned DeBERTa-v3 + ONNX INT8 │
└──────────────────────────────────────────────────────────────────────────┘
                                     ▲
                                     │ RANH GIỚI BẢO VỆ
                                     ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                   OUT-OF-SCOPE (NẰM NGOÀI PHẠM VI)                       │
│  - Tấn công đa phương thức: Image / Audio / Video Jailbreaks             │
│  - Tấn công hạ tầng mạng: DDoS, trích xuất trọng số GPU, Side-channel    │
│  - Quét lỗ hổng hệ điều hành máy chủ / CVE của Linux/Docker              │
│  - Xây dựng hệ thống cơ sở dữ liệu Vector RAG hoặc Agent Tool Runtime    │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 1.6. Thesis Structure (Bố Cục 6 Chương Của Toàn Văn Luận Văn)
Tuân thủ nghiêm ngặt theo Hướng dẫn Khóa luận Tốt nghiệp FPT University IAP491:
- **Chapter 1: Introduction** *(Bối cảnh, Bài toán, Mục tiêu, Ý nghĩa, Phạm vi, Cấu trúc).*
- **Chapter 2: Literature Review** *(Khảo sát nghiên cứu liên quan, SOTA Guardrails, Đóng góp mới của nhóm).*
- **Chapter 3: Methodology** *(Thiết kế nghiên cứu, Thu thập dữ liệu, Group-Aware Splitting, Baseline ML & DeBERTa-v3).*
- **Chapter 4: Experimental and Results** *(Môi trường thử nghiệm, Kết quả đối sánh SOTA, Ma trận nhầm lẫn, Test độ bền).*
- **Chapter 5: Discussion** *(Thảo luận kết quả, Đánh giá cân bằng An toàn/Trải nghiệm người dùng, Giới hạn thực tiễn).*
- **Chapter 6: Conclusion and Future Work** *(Tổng kết đóng góp và Hướng nghiên cứu mở rộng).*
- **References & Appendices** *(17 Tài liệu tham khảo chuẩn IEEE và Phụ lục mã nguồn).*

---

## References (Tài Liệu Tham Khảo Học Thuật)

<a id="ref1"></a>**[1]** W. X. Zhao et al., "A Survey of Large Language Models," *arXiv preprint arXiv:2303.18223*, 2023. Link: [https://arxiv.org/abs/2303.18223](https://arxiv.org/abs/2303.18223).

<a id="ref2"></a>**[2]** L. Ouyang et al., "Training language models to follow instructions with human feedback," in *Advances in Neural Information Processing Systems (NeurIPS 2022)*, vol. 35, pp. 27730–27744. Link: [https://arxiv.org/abs/2203.02155](https://arxiv.org/abs/2203.02155).

<a id="ref3"></a>**[3]** F. Perez and I. Ribeiro, "Ignore This Title and Hack This Paper: Towards Automated Adversarial Prompting," in *NeurIPS Workshops*, 2022. Link: [https://arxiv.org/abs/2206.05600](https://arxiv.org/abs/2206.05600).

<a id="ref4"></a>**[4]** K. Greshake, S. Abdelnabi, S. Mishra, C. Endres, T. Holz, and M. Fritz, "Not what you've signed up for: Compromising Real-World LLM Applications with Indirect Prompt Injection," in *Proceedings of the 16th ACM Workshop on Artificial Intelligence and Security (AISEC 2023)*, pp. 79–90. Link: [https://arxiv.org/abs/2302.12173](https://arxiv.org/abs/2302.12173).

<a id="ref5"></a>**[5]** A. Wei, N. Haghtalab, and J. Steinhardt, "Jailbroken: How Does LLM Safety Training Fail?," in *Advances in Neural Information Processing Systems (NeurIPS 2024)*, vol. 36. Link: [https://arxiv.org/abs/2307.02483](https://arxiv.org/abs/2307.02483).

<a id="ref6"></a>**[6]** Y. Yang et al., "Securing the AI Agent: A Unified Framework for Multi-Layer Agent Red Teaming," *Tencent Zhuque Lab Technical Report*, arXiv:2606.31227, 2026. Link: [https://arxiv.org/abs/2606.31227](https://arxiv.org/abs/2606.31227).

<a id="ref7"></a>**[7]** A. Vassilev et al., "Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations," *National Institute of Standards and Technology (NIST)*, NIST.AI.100-2e2025, 2025. Link: [https://csrc.nist.gov/pubs/ai/100/2/e2025/final](https://csrc.nist.gov/pubs/ai/100/2/e2025/final).

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
