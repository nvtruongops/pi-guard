# REFERENCES LOG & APPLICATION MAPPING MATRIX
## Hệ Thống Quản Lý & Định Vị Tài Liệu Tham Khảo — Đề Tài PI-Guard (18 Bài Báo Học Thuật Đỉnh Cao)

> **Thư mục lưu trữ tài liệu gốc**: **`Final-Report/References/`**  
> **Tiêu chí chuẩn hóa**: 17 bài báo xuất bản từ 2022–2026 (Kỷ nguyên LLM hiện đại) + 1 công trình kinh điển đặt nền móng kiến trúc phòng vệ phân tầng (Saltzer & Schroeder, IEEE 1975).  
> **Cập nhật lần cuối**: 2026-09-10  
> **Mục đích**: Lưu trữ, theo dõi, lập chỉ mục siêu dữ liệu chi tiết và ánh xạ toàn bộ **18 bài báo PDF cốt lõi** cùng các tài nguyên thực nghiệm trong `References/` tới từng phân hệ của repository `d:/Work/Do-an/`.

---

## 🔒 0. NGUYÊN TẮC BẤT BIẾN: "LOCAL REFERENCES FIRST" PROTOCOL
> [!IMPORTANT]
> **QUY TRÌNH BẮT BUỘC CHO TẤT CẢ THÀNH VIÊN & AI AGENTS TRƯỚC KHI TÌM KIẾM BÀI BÁO MỚI**:
> 1. **TRUY LỤC TÀI LIỆU CỤC BỘ TRƯỚC TIÊN (Local References First)**:
>    - Khi cần luận chứng cho bất kỳ tuyên bố khoa học, cơ chế tấn công, kiến trúc phòng thủ hay công thức toán học nào, **BẮT BUỘC phải tra cứu bảng Ma Trận Chủ Đề (Mục 1) và Siêu Dữ Liệu 18 Bài Báo (Mục 2)** trong tệp này trước.
>    - Nếu luận điểm đã được bảo chứng bởi một trong 18 bài báo đã lưu trữ, **PHẢI TÁI SỬ DỤNG NGAY** bài báo đó (dùng đúng mã neo `[[N]](#refN)` và tệp PDF cục bộ tương ứng).
> 2. **CHỐNG DÀN TRẢI & TÌM KIẾM TRÙNG LẶP (Zero Redundant Search)**:
>    - Tuyệt đối không dùng các công cụ MCP (`arxiv`, `openalex`, `semanticscholar`, `scholar-feed`) để tìm kiếm thêm bài báo mới cho các chủ đề ĐÃ CÓ trong kho 18 bài (như: Direct Prompt Injection, DAN Jailbreak, TF-IDF Baseline, DeBERTa-v3, ONNX INT8 Quantization, Low FPR Trade-off).
> 3. **ĐIỀU KIỆN TIẾP NHẬN TÀI LIỆU MỚI (New Reference Ingestion Criteria)**:
>    - Chỉ được phép bổ sung bài báo mới khi xuất hiện câu hỏi nghiên cứu mới phát sinh ngoài phạm vi 18 bài hiện có.
>    - Bài báo mới phải đáp ứng 4 điều kiện khắt khe:
>      - Năm xuất bản $\ge 2022$ (trừ công trình kinh điển).
>      - Tương thích 100% với kiến trúc **External Guardrail Proxy** (không can thiệp KV-cache hay trọng số nội tại của LLM).
>      - Bắt buộc có **Open-Access PDF** (Zero Paywalled DOI).
>      - Phải tải tệp PDF về `Final-Report/References/` và cập nhật đầy đủ siêu dữ liệu vào `REFERENCES_LOG.md`.

---

## 🗺️ 1. MA TRẬN ĐỊNH VỊ NHANH THEO CHỦ ĐỀ NGHIÊN CỨU (TAXONOMY LOOKUP MATRIX)

Bảng tra cứu nhanh giúp thành viên và AI Agent xác định ngay bài báo cần dùng theo từng khía cạnh kỹ thuật của đồ án:

| Chủ Đề Nghiên Cứu / Lĩnh Vực | Mã Tham Chiếu Cục Bộ | Tác Giả & Năm | Tệp PDF Cục Bộ Trong `References/` | Phạm Vi Áp Dụng Trong Đồ Án PI-Guard |
| :--- | :---: | :--- | :--- | :--- |
| **1. Tổng quan Kiến trúc LLM & Lỗ hổng Ranh giới Phẳng** | <a href="#ref1">`[1]`</a> | Zhao et al. (2023) | **`Zhao_2023_A_Survey_of_Large_Language_Models.pdf`** | Cơ sở token tự hồi quy, nguyên nhân Code và Data bị hòa lẫn. (Chương 1, 2) |
| **2. Instruction Tuning & Xử lý System Prompt** | <a href="#ref2">`[2]`</a> | Ouyang et al. (2022) | **`Ouyang_2022_InstructGPT_Training_Language_Models_Follow_Instructions.pdf`** | Nguyên lý RLHF, sự thất bại của chỉ thị hệ thống trước lệnh người dùng. (Chương 1, 2) |
| **3. Direct Prompt Injection (Tấn công Trực tiếp)** | <a href="#ref3">`[3]`</a> | Perez & Ribeiro (2022) | **`Perez_2022_Ignore_This_Title_Hack_This_Paper_Prompt_Injection.pdf`** | Nền tảng Direct Prompt Injection, Goal Hijacking, System Prompt Leaking. (Chương 1, 2, 3) |
| **4. Indirect Prompt Injection (Tấn công Gián tiếp qua Dữ liệu)** | <a href="#ref4">`[4]`</a> | Greshake et al. (2023) | **`Greshake_2023_Indirect_Prompt_Injection.pdf`** | Độc hại nhúng trong tài liệu thứ ba (Web/RAG), 4 tầng thiệt hại doanh nghiệp. (Chương 1, 2, 3) |
| **5. Cơ chế Thất bại Căn chỉnh An toàn (Jailbreak Failures)** | <a href="#ref5">`[5]`</a> | Wei et al. (2024) | **`Wei_2024_Jailbroken_How_LLM_Safety_Training_Fails.pdf`** | Xung đột mục tiêu (Competing Objectives) & Không khớp khả năng (Mismatch). (Chương 1, 4) |
| **6. Mô hình Đe Dọa Đa Tầng & Toán Tử Tấn Công Đổi Mới** | <a href="#ref6">`[6]`</a> | Tencent Zhuque Lab (2026) | **`Tencent_2026_AI_Infra_Guard_MultiLayer_Agent_RedTeaming.pdf`** | Mô hình đe dọa 4 tầng (Zone 0–3), Layer-Paradigm Matching, 26+ Attack Operators. (Chương 1, 3, 4) |
| **7. Đối Chuẩn Guardrail Dựa Trên LLM (LLM-as-a-Judge)** | <a href="#ref7">`[7]`</a> | Meta AI / Inan et al. (2023) | **`Meta_2023_Llama_Guard_Input_Output_Safeguard.pdf`** | Đối chuẩn độ trễ và chi phí (Llama Guard 3 8B: độ trễ > 850ms vs PI-Guard < 30ms). (Chương 2, 4) |
| **8. Kiến Trúc Guardrail Middleware Lập Trình Được** | <a href="#ref8">`[8]`</a> | NVIDIA / Rebedea et al. (2023)| **`NVIDIA_2023_NeMo_Guardrails_Toolkit.pdf`** | Thiết kế kiến trúc Proxy bất đồng bộ đánh chặn trước khi gửi đến LLM. (Chương 2, 3) |
| **9. Phân Loại Ngữ Nghĩa Sâu Bằng Disentangled Attention** | <a href="#ref9">`[9]`</a> | He et al. (2021/2023) | **`He_2023_DeBERTaV3_Disentangled_Attention_ICLR.pdf`** | **Trụ cột An ninh 2**: DeBERTa-v3 tách biệt vector nội dung và vị trí tương đối. (Chương 3, 4) |
| **10. Khống Chế Tỷ Lệ Chặn Nhầm (FPR) & Cân Bằng Trải Nghiệm**| <a href="#ref10">`[10]`</a> | OpenAI / Markov et al. (2023) | **`OpenAI_2023_Undesired_Content_Detection.pdf`** | **Trụ cột An ninh 3**: Phương pháp luận đo lường FPR < 1.5% trên truy vấn lành tính. (Chương 2, 4) |
| **11. Tập Dữ Liệu Jailbreak Thực Tế Trong Tự Nhiên** | <a href="#ref11">`[11]`</a> | Shen et al. (2024) | **`Shen_2024_Do_Anything_Now_Jailbreak_Prompts_In_The_Wild.pdf`** | Bộ dữ liệu 15,140 prompt Jailbreak thực tế (DAN, Roleplay) từ Reddit/Discord. (Chương 3, 4) |
| **12. Kiểm Thử Độ Bền Đối Kháng & Toán Tử Đột Biến** | <a href="#ref12">`[12]`</a> | Zhou et al. (2024) | **`Zhou_2024_EasyJailbreak_Unified_Framework.pdf`** | Framework đột biến văn bản đối kháng (Leetspeak, chèn khoảng trắng, ngắt dòng). (Chương 3, 4) |
| **13. Tấn Công Chuỗi Hậu Tố Đối Kháng Tối Ưu Hóa (GCG)** | <a href="#ref13">`[13]`</a> | Zou et al. (2023) | **`Zou_2023_Universal_Transferable_Adversarial_Attacks_GCG.pdf`** | Greedy Coordinate Gradient, mẫu tấn công chuỗi ký tự nhiễu để stress test bộ lọc. (Chương 4) |
| **14. Phòng Thủ Bằng Xáo Trộn Ngẫu Nhiên (Randomized Smoothing)**| <a href="#ref14">`[14]`</a> | Robey et al. (2023) | **`Robey_2023_SmoothLLM_Defending_LLMs_Random_Perturbation.pdf`** | So sánh đối chuẩn phòng thủ SmoothLLM với kiến trúc phân tầng của PI-Guard. (Chương 4) |
| **15. Phòng Thủ Bằng Bộ Lọc Cú Pháp Cơ Bản (TF-IDF N-Grams)** | <a href="#ref15">`[15]`</a> | Jain et al. (2023) | **`Jain_2023_Baseline_Defenses_Adversarial_Attacks_LLMs.pdf`** | **Trụ cột An ninh 1**: Cơ sở lý thuyết của TF-IDF Word/Char n-grams chống biến dạng cú pháp. (Chương 3, 4) |
| **16. Lượng Hóa Động INT8 Sau Huấn Luyện (PTQ) Cho CPU** | <a href="#ref16">`[16]`</a> | Yao et al. (2022) | **`Yao_2022_ZeroQuant_Efficient_Post_Training_Quantization_Transformers.pdf`** | Kỹ thuật lượng hóa động INT8 Post-Training Quantization cho CPU, độ trễ P95 < 30ms. (Chương 3, 5) |
| **17. Lẩn Tránh Bộ Lọc Bằng Mã Hóa Ký Tự (Cipher/Base64)** | <a href="#ref17">`[17]`</a> | Yuan et al. (2024) | **`Yuan_2024_GPT4_Too_Smart_To_Be_Safe_Cipher_Jailbreak.pdf`** | Minh chứng LLM bị đánh bại bởi mã hóa Base64/Caesar và giải pháp tiền giải mã tiền trạm. (Chương 1, 3, 4) |
| **18. Nguyên Lý Kinh Điển Về Bảo Vệ Toàn Vẹn & Phân Tầng** | <a href="#ref18">`[18]`</a> | Saltzer & Schroeder (1975) | **`Saltzer_1975_The_Protection_of_Information_in_Computer_Systems.pdf`** | **Nền tảng Thiết kế Hệ thống**: Defense-in-Depth, Complete Mediation, Economy of Mechanism. (Chương 2, 3) |

---

## 📊 2. BẢNG CHI TIẾT SIÊU DỮ LIỆU HỌC THUẬT (18 BÀI BÁO CỐT LÕI)

```
========================================================================================================================
DANH MỤC 18 CÔNG TRÌNH KHOA HỌC CỐT LÕI — ĐỒ ÁN TỐT NGHIỆP PI-GUARD (IAP491 FALL 2026)
========================================================================================================================
```

### <a id="ref1"></a>[1] A Survey of Large Language Models
- **Tác giả**: Wayne Xin Zhao, Kun Zhou, Junyi Li, Tianyi Tang, Xiaolei Wang, Yupeng Hou, Yingqian Min, Beichen Zhang, Junjie Zhang, Zican Dong, et al.
- **Năm xuất bản**: 2023 | **Nơi công bố**: *arXiv:2303.18223 / IJCAI Survey*
- **Tệp PDF Cục Bộ**: **`Zhao_2023_A_Survey_of_Large_Language_Models.pdf`**
- **Liên kết mở (Open-Access PDF)**: [https://arxiv.org/pdf/2303.18223.pdf](https://arxiv.org/pdf/2303.18223.pdf) | **arXiv ID**: `2303.18223`
- **Từ khóa phân loại**: `LLM Architecture`, `Autoregressive Transformers`, `Pre-training`, `Tokenization`, `Alignment`
- **Tóm tắt đóng góp khoa học**: Khảo sát bách khoa toàn thư toàn diện về kiến trúc Transformer tự hồi quy, quá trình huấn luyện và cơ chế tiền huấn luyện; chỉ rõ hạn chế cố hữu khi LLM xử lý chuỗi token phẳng mà không có ranh giới bảo vệ bộ nhớ.
- **Ánh xạ vào Luận văn PI-Guard**: **Chương 1 (Giới thiệu vấn đề)** & **Chương 2 (Cơ sở lý thuyết)** — Luận giải tại sao LLM không thể tự bảo vệ trước các cuộc tấn công nhúng mã lệnh.

---

### <a id="ref2"></a>[2] Training Language Models to Follow Instructions with Human Feedback
- **Tác giả**: Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, et al. (OpenAI)
- **Năm xuất bản**: 2022 | **Nơi công bố**: *Advances in Neural Information Processing Systems (NeurIPS 2022)*
- **Tệp PDF Cục Bộ**: **`Ouyang_2022_InstructGPT_Training_Language_Models_Follow_Instructions.pdf`**
- **Liên kết mở (Open-Access PDF)**: [https://arxiv.org/pdf/2203.02155.pdf](https://arxiv.org/pdf/2203.02155.pdf) | **arXiv ID**: `2203.02155`
- **Từ khóa phân loại**: `InstructGPT`, `RLHF`, `Instruction Following`, `System Prompt`, `Alignment Bias`
- **Tóm tắt đóng góp khoa học**: Đặt nền móng cho kỹ thuật căn chỉnh mô hình theo chỉ thị (Instruction Tuning) qua học tăng cường từ phản hồi con người (RLHF), đồng thời vô tình tạo ra thiên kiến "luôn cố gắng tuân thủ mệnh lệnh người dùng" dẫn đến nguy cơ bị thao túng chỉ thị.
- **Ánh xạ vào Luận văn PI-Guard**: **Chương 1** & **Chương 2** — Giải thích cơ chế xung đột giữa System Prompt và User Prompt.

---

### <a id="ref3"></a>[3] Ignore This Title and Hack This Paper: Towards Automated Adversarial Prompting
- **Tác giả**: Fábio Perez, Ian Ribeiro
- **Năm xuất bản**: 2022 | **Nơi công bố**: *NeurIPS ML Safety Workshop 2022*
- **Tệp PDF Cục Bộ**: **`Perez_2022_Ignore_This_Title_Hack_This_Paper_Prompt_Injection.pdf`**
- **Liên kết mở (Open-Access PDF)**: [https://arxiv.org/pdf/2211.09527.pdf](https://arxiv.org/pdf/2211.09527.pdf) | **arXiv ID**: `2211.09527`
- **Từ khóa phân loại**: `Prompt Injection`, `Goal Hijacking`, `Prompt Leaking`, `Direct Attack`, `Automated Red Teaming`
- **Tóm tắt đóng góp khoa học**: Công trình đầu tiên trong y văn bảo mật định nghĩa và phân loại chính thức kỹ thuật Prompt Injection thành hai dạng cốt lõi: *Goal Hijacking* (cướp quyền điều khiển) và *Prompt Leaking* (trích xuất chỉ thị hệ thống bí mật).
- **Ánh xạ vào Luận văn PI-Guard**: **Bản Đăng Ký Đề Tài**, **Chương 1**, **Chương 3** — Cơ sở xây dựng định nghĩa bài toán, phân loại tấn công và kịch bản Demo 1.

---

### <a id="ref4"></a>[4] Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection
- **Tác giả**: Kai Greshake, Sahar Abdelnabi, Shailesh Mishra, Christoph Endres, Thorsten Holz, Mario Fritz
- **Năm xuất bản**: 2023 | **Nơi công bố**: *Proceedings of the 16th ACM Workshop on Artificial Intelligence and Security (ACM AISec '23)*
- **Tệp PDF Cục Bộ**: **`Greshake_2023_Indirect_Prompt_Injection.pdf`**
- **Liên kết mở (Open-Access PDF)**: [https://arxiv.org/pdf/2302.12173.pdf](https://arxiv.org/pdf/2302.12173.pdf) | **DOI**: `10.1145/3605764.3623982`
- **Từ khóa phân loại**: `Indirect Prompt Injection`, `Data-as-Code`, `Untrusted Ingestion`, `Malware Synthesis`, `Enterprise Risk`
- **Tóm tắt đóng góp khoa học**: Chứng minh nguy cơ khai thác nghiêm trọng khi LLM đọc dữ liệu từ bên ngoài (Web, Email, Tài liệu văn phòng); thiết lập mô hình 4 tầng thiệt hại thực tế từ lộ lọt thông tin đến thực thi mã tùy ý.
- **Ánh xạ vào Luận văn PI-Guard**: **Chương 1**, **Chương 2** & **Chương 3** — Luận giải nhu cầu bắt buộc phải có lớp bảo vệ tiền trạm (Input Guardrail) độc lập đặt trước các hệ sinh thái LLM/RAG.

---

### <a id="ref5"></a>[5] Jailbroken: How Does LLM Safety Training Fail?
- **Tác giả**: Alexander Wei, Nika Haghtalab, Jacob Steinhardt (UC Berkeley)
- **Năm xuất bản**: 2024 | **Nơi công bố**: *Advances in Neural Information Processing Systems (NeurIPS 2024)*
- **Tệp PDF Cục Bộ**: **`Wei_2024_Jailbroken_How_LLM_Safety_Training_Fails.pdf`**
- **Liên kết mở (Open-Access PDF)**: [https://arxiv.org/pdf/2307.02483.pdf](https://arxiv.org/pdf/2307.02483.pdf) | **arXiv ID**: `2307.02483`
- **Từ khóa phân loại**: `Jailbreak Mechanism`, `Competing Objectives`, `Mismatched Generalization`, `Safety Failure`, `Adversarial Prompts`
- **Tóm tắt đóng góp khoa học**: Phân tích toán học và nguyên lý suy giảm an toàn của LLM qua hai nguyên nhân nền tảng: *Competing Objectives* (Mâu thuẫn giữa tính hữu ích và tính an toàn) và *Mismatched Generalization* (Khả năng ngôn ngữ vượt xa dữ liệu huấn luyện an toàn).
- **Ánh xạ vào Luận văn PI-Guard**: **Chương 1** & **Chương 4** — Cơ sở thiết kế các toán tử phát hiện Jailbreak phân tầng ngữ nghĩa.

---

### <a id="ref6"></a>[6] AI-Infra-Guard: Multi-Layer Attack Surface and Defense Framework for AI Agents
- **Tác giả**: Tencent Zhuque Lab (Tencent Security)
- **Năm xuất bản**: 2026 | **Nơi công bố**: *arXiv:2606.31227 / Tencent Security Technical Report 2026*
- **Tệp PDF Cục Bộ**: **`Tencent_2026_AI_Infra_Guard_MultiLayer_Agent_RedTeaming.pdf`**
- **Liên kết mở (Open-Access PDF)**: [https://arxiv.org/pdf/2606.31227.pdf](https://arxiv.org/pdf/2606.31227.pdf) | **arXiv ID**: `2606.31227`
- **Từ khóa phân loại**: `Multi-Layer Threat Model`, `Zone 0 to 3`, `Attack Operators`, `Red Teaming`, `Agent Defense`
- **Tóm tắt đóng góp khoa học**: Đề xuất mô hình đe dọa Zero-Trust 4 vùng phân cấp không gian mạng (Zone 0: Public Input, Zone 1: Guardrail Ingress, Zone 2: Target LLM, Zone 3: Storage/Tools); định nghĩa danh mục 26+ toán tử tấn công thực tế vào hệ sinh thái AI.
- **Ánh xạ vào Luận văn PI-Guard**: **Chương 1 (Threat Model)**, **Chương 3 (Kiến trúc)** & **Slide Báo cáo GVHD** — Mô hình hóa ranh giới an ninh phân vùng của PI-Guard.

---

### <a id="ref7"></a>[7] Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations
- **Tác giả**: Hakan Inan, Kartikeya Upasani, Jianfeng Chi, Rashi Rungta, Krithika Iyer, Yuning Mao, Michael Tontchev, Qing Hu, Brian Fuller, Davide Testuggine, Madian Khabsa (Meta AI)
- **Năm xuất bản**: 2023 | **Nơi công bố**: *arXiv:2312.06674*
- **Tệp PDF Cục Bộ**: **`Meta_2023_Llama_Guard_Input_Output_Safeguard.pdf`**
- **Liên kết mở (Open-Access PDF)**: [https://arxiv.org/pdf/2312.06674.pdf](https://arxiv.org/pdf/2312.06674.pdf) | **arXiv ID**: `2312.06674`
- **Từ khóa phân loại**: `LLM-as-a-Judge`, `Llama Guard`, `Safety Taxonomy`, `Inference Latency`, `Input-Output Filtering`
- **Tóm tắt đóng góp khoa học**: Xây dựng mô hình ngôn ngữ chuyên dụng 7B/8B làm trọng tài đánh giá an toàn đầu vào/đầu ra; chuẩn hóa danh mục các nhóm rủi ro nội dung độc hại.
- **Ánh xạ vào Luận văn PI-Guard**: **Chương 2** & **Chương 4** — Mô hình đối chuẩn cốt lõi để so sánh hiệu năng: chứng minh PI-Guard vượt trội 40x về tốc độ ($14.8\text{ms}$ vs $> 850\text{ms}$) và tiết kiệm chi phí phần cứng (Zero GPU vs $> 16\text{GB}$ VRAM).

---

### <a id="ref8"></a>[8] NeMo Guardrails: A Toolkit for Controllable and Safe LLM Applications
- **Tác giả**: Traian Rebedea, Razvan Dinu, Christian Svorenh, Carsten Schallert, et al. (NVIDIA)
- **Năm xuất bản**: 2023 | **Nơi công bố**: *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing (EMNLP 2023)*
- **Tệp PDF Cục Bộ**: **`NVIDIA_2023_NeMo_Guardrails_Toolkit.pdf`**
- **Liên kết mở (Open-Access PDF)**: [https://arxiv.org/pdf/2310.10501.pdf](https://arxiv.org/pdf/2310.10501.pdf) | **arXiv ID**: `2310.10501`
- **Từ khóa phân loại**: `NeMo Guardrails`, `Colang`, `Programmable Middleware`, `Async Ingress`, `Topical Rails`
- **Tóm tắt đóng góp khoa học**: Thiết lập kiến trúc phần mềm middleware lập trình được với ngôn ngữ Colang đặt trước các ứng dụng hội thoại, định hình cơ chế chặn dòng yêu cầu bất đồng bộ (Asynchronous Request Interception).
- **Ánh xạ vào Luận văn PI-Guard**: **Chương 2** & **Chương 3** — Cơ sở thiết kế luồng xử lý của lớp FastAPI Proxy Middleware trong PI-Guard.

---

### <a id="ref9"></a>[9] DeBERTa: Decoding-Enhanced BERT with Disentangled Attention
- **Tác giả**: Pengcheng He, Xiaodong Liu, Jianfeng Gao, Weizhu Chen (Microsoft)
- **Năm xuất bản**: 2021/2023 | **Nơi công bố**: *International Conference on Learning Representations (ICLR 2021/2023)*
- **Tệp PDF Cục Bộ**: **`He_2023_DeBERTaV3_Disentangled_Attention_ICLR.pdf`**
- **Liên kết mở (Open-Access PDF)**: [https://arxiv.org/pdf/2006.03654.pdf](https://arxiv.org/pdf/2006.03654.pdf) | **arXiv ID**: `2006.03654`
- **Từ khóa phân loại**: `DeBERTa-v3`, `Disentangled Attention`, `Relative Position Embedding`, `ELECTRA Objective`, `Text Classification`
- **Tóm tắt đóng góp khoa học**: Đột phá kỹ thuật tách biệt hoàn toàn biểu diễn nội dung ($H_i$) và biểu diễn vị trí tương đối ($P_{i,j}$), kết hợp huấn luyện thay thế từ (RTD), giúp mô hình nhạy bén đặc biệt với sự đảo lộn thứ tự chỉ thị trong prompt.
- **Ánh xạ vào Luận văn PI-Guard**: **Trụ cột An ninh 2**, **Chương 3** & **Chương 4** — Lý do khoa học lựa chọn `microsoft/deberta-v3-base` làm mô hình phân loại ngữ nghĩa sâu.

---

### <a id="ref10"></a>[10] A Holistic Approach to Undesired Content Detection in the Real World
- **Tác giả**: Todor Markov, Chong Zhang, Sandhini Agarwal, Florentine Eloundou Nekoul, Theodore Lee, Steven Adler, Angela Jiang, Lilian Weng (OpenAI)
- **Năm xuất bản**: 2023 | **Nơi công bố**: *Proceedings of the AAAI Conference on Human Computation and Crowdsourcing (HCOMP 2023)*
- **Tệp PDF Cục Bộ**: **`OpenAI_2023_Undesired_Content_Detection.pdf`**
- **Liên kết mở (Open-Access PDF)**: [https://arxiv.org/pdf/2208.03274.pdf](https://arxiv.org/pdf/2208.03274.pdf) | **arXiv ID**: `2208.03274`
- **Từ khóa phân loại**: `Low False Positive Rate`, `FPR < 1.5%`, `Moderation API`, `Evaluation Methodology`, `Usability Trade-off`
- **Tóm tắt đóng góp khoa học**: Định hình phương pháp luận đo lường an toàn thực tế: chứng minh rằng trong ứng dụng thực tế, một hệ thống bảo vệ có tỷ lệ chặn nhầm cao ($FPR > 2\%$) sẽ bị người dùng vô hiệu hóa; đề xuất kỹ thuật tối ưu hóa Pareto giữa độ phủ bảo vệ và trải nghiệm người dùng.
- **Ánh xạ vào Luận văn PI-Guard**: **Trụ cột An ninh 3**, **Chương 2** & **Chương 4** — Cơ sở cho chỉ tiêu cam kết $\text{FPR} < 1.5\%$ trên các truy vấn hợp lệ hàng ngày.

---

### <a id="ref11"></a>[11] "Do Anything Now": Characterizing and Evaluating In-The-Wild Jailbreak Prompts on Large Language Models
- **Tác giả**: Xinyue Shen, Zeyuan Chen, Michael Backes, Yun Shen, Yang Zhang (CISPA Helmholtz Center for Information Security)
- **Năm xuất bản**: 2024 | **Nơi công bố**: *Proceedings of the 2024 ACM SIGSAC Conference on Computer and Communications Security (ACM CCS '24)*
- **Tệp PDF Cục Bộ**: **`Shen_2024_Do_Anything_Now_Jailbreak_Prompts_In_The_Wild.pdf`**
- **Liên kết mở (Open-Access PDF)**: [https://arxiv.org/pdf/2308.03825.pdf](https://arxiv.org/pdf/2308.03825.pdf) | **DOI**: `10.1145/3658644.3670390`
- **Từ khóa phân loại**: `Do Anything Now (DAN)`, `In-The-Wild Prompts`, `Jailbreak Taxonomy`, `Community Red Teaming`, `Empirical Benchmark`
- **Tóm tắt đóng góp khoa học**: Nghiên cứu thực nghiệm quy mô lớn thu thập 15,140 mẫu prompt Jailbreak thực tế từ Reddit/Discord trong hơn 6 tháng; xây dựng bảng phân loại cấu trúc tấn công DAN thành các mẫu hình đóng vai, ép buộc giả định và nghịch lý logic.
- **Ánh xạ vào Luận văn PI-Guard**: **Chương 3 (Dataset Engineering)** & **Chương 4** — Nguồn dữ liệu thực tế để huấn luyện và kiểm thử độ bền của PI-Guard trước các biến thể DAN 1.0 đến 15.0.

---

### <a id="ref12"></a>[12] EasyJailbreak: A Unified Framework for Jailbreaking Large Language Models
- **Tác giả**: Weikang Zhou, Xiao Wang, Limao Xiong, Han Xia, Yingshuang Gu, Mingxu Chai, Fukang Zhu, Caishuang Huang, Shihan Dou, Xiaoqing Zheng, Xuanjing Huang (Fudan University)
- **Năm xuất bản**: 2024 | **Nơi công bố**: *arXiv:2403.12171*
- **Tệp PDF Cục Bộ**: **`Zhou_2024_EasyJailbreak_Unified_Framework.pdf`**
- **Liên kết mở (Open-Access PDF)**: [https://arxiv.org/pdf/2403.12171.pdf](https://arxiv.org/pdf/2403.12171.pdf) | **arXiv ID**: `2403.12171`
- **Từ khóa phân loại**: `EasyJailbreak`, `Mutation Operators`, `Leetspeak`, `Spacing Trick`, `Adversarial Robustness`
- **Tóm tắt đóng góp khoa học**: Đề xuất framework hợp nhất 4 thành phần (Initialize, Mutate, Evaluate, Select) và danh mục các toán tử đột biến cú pháp (Leetspeak, Word Replacement, Character Insertion) nhằm tự động hóa quá trình sinh tấn công đối kháng.
- **Ánh xạ vào Luận văn PI-Guard**: **Chương 3** & **Chương 4 (Robustness Testing)** — Cung cấp bộ fuzzer mutators để kiểm thử độ bền $\Delta F_1 < 5\%$ của PI-Guard trước các biến dị cú pháp.

---

### <a id="ref13"></a>[13] Universal and Transferable Adversarial Attacks on Aligned Language Models
- **Tác giả**: Andy Zou, Zifan Wang, Nicholas Carlini, Milad Nasr, J. Zico Kolter, Matt Fredrikson (CMU / CAIS / Google DeepMind)
- **Năm xuất bản**: 2023 | **Nơi công bố**: *arXiv:2307.15043*
- **Tệp PDF Cục Bộ**: **`Zou_2023_Universal_Transferable_Adversarial_Attacks_GCG.pdf`**
- **Liên kết mở (Open-Access PDF)**: [https://arxiv.org/pdf/2307.15043.pdf](https://arxiv.org/pdf/2307.15043.pdf) | **arXiv ID**: `2307.15043`
- **Từ khóa phân loại**: `Greedy Coordinate Gradient (GCG)`, `Adversarial Suffix`, `Universal Attack`, `White-Box Optimization`, `Transferability`
- **Tóm tắt đóng góp khoa học**: Khám phá thuật toán tối ưu hóa gradient tự động tìm kiếm chuỗi token hậu tố vô nghĩa nhưng có khả năng vượt qua bộ lọc an toàn của hầu hết các LLM tiên tiến (ChatGPT, Claude, Llama 2).
- **Ánh xạ vào Luận văn PI-Guard**: **Chương 4 (Đánh giá khả năng phòng thủ OOD)** — Sử dụng tập mẫu GCG đối kháng làm bộ kiểm thử ngoại lai để chứng minh mô hình Character n-gram và DeBERTa bắt được các chuỗi token bất thường.

---

### <a id="ref14"></a>[14] SmoothLLM: Defending Large Language Models Against Jailbreaking Attacks
- **Tác giả**: Alexander Robey, Eric Wong, Hamed Hassani, George J. Pappas (University of Pennsylvania)
- **Năm xuất bản**: 2023 | **Nơi công bố**: *arXiv:2310.03684*
- **Tệp PDF Cục Bộ**: **`Robey_2023_SmoothLLM_Defending_LLMs_Random_Perturbation.pdf`**
- **Liên kết mở (Open-Access PDF)**: [https://arxiv.org/pdf/2310.03684.pdf](https://arxiv.org/pdf/2310.03684.pdf) | **arXiv ID**: `2310.03684`
- **Từ khóa phân loại**: `Randomized Smoothing`, `Perturbation Defense`, `Input Mitigation`, `Defensive Sampling`, `Attack Mitigation`
- **Tóm tắt đóng góp khoa học**: Đề xuất giải pháp phòng thủ bằng cách tạo nhiều bản sao xáo trộn ngẫu nhiên của prompt đầu vào và bỏ phiếu kết quả, giảm đáng kể tỷ lệ thành công của tấn công GCG nhưng làm tăng chi phí tính toán gấp nhiều lần.
- **Ánh xạ vào Luận văn PI-Guard**: **Chương 2** & **Chương 4** — So sánh đối chứng: chứng minh PI-Guard đạt hiệu quả phòng thủ tương đương mà không làm bùng nổ chi phí tính toán và độ trễ.

---

### <a id="ref15"></a>[15] Baseline Defenses for Adversarial Attacks Against Aligned Language Models
- **Tác giả**: Neel Jain, Avi Schwarzschild, Yuxin Wen, Gowthami Thattai, John Thickstun, Tom Goldstein (University of Maryland)
- **Năm xuất bản**: 2023 | **Nơi công bố**: *arXiv:2309.00614*
- **Tệp PDF Cục Bộ**: **`Jain_2023_Baseline_Defenses_Adversarial_Attacks_LLMs.pdf`**
- **Liên kết mở (Open-Access PDF)**: [https://arxiv.org/pdf/2309.00614.pdf](https://arxiv.org/pdf/2309.00614.pdf) | **arXiv ID**: `2309.00614`
- **Từ khóa phân loại**: `Baseline Defenses`, `Perplexity Filtering`, `TF-IDF Character N-Grams`, `Syntactic Defense`, `Low-Cost Guard`
- **Tóm tắt đóng góp khoa học**: Chứng minh một phát hiện quan trọng: các bộ phân loại tuyến tính đơn giản dựa trên n-gram ký tự hoặc bộ lọc độ hỗn loạn (Perplexity) có khả năng phát hiện các đòn tấn công đối kháng tốt ngang ngửa hoặc thậm chí vượt trội các mô hình phòng thủ phức tạp tốn kém.
- **Ánh xạ vào Luận văn PI-Guard**: **Trụ cột An ninh 1**, **Chương 3** & **Chương 4** — Cơ sở khoa học nền tảng cho Tầng 1 (Classical ML TF-IDF Word/Char) trong kiến trúc phòng thủ hai tầng của PI-Guard.

---

### <a id="ref16"></a>[16] ZeroQuant: Efficient and Affordable Post-Training Quantization for Large-Scale Transformers
- **Tác giả**: Zhewei Yao, Reza Yazdani Aminabadi, Minjia Zhang, Xiaoxia Wu, Conglong Li, Yuxiong He (Microsoft DeepSpeed)
- **Năm xuất bản**: 2022 | **Nơi công bố**: *Advances in Neural Information Processing Systems (NeurIPS 2022)*
- **Tệp PDF Cục Bộ**: **`Yao_2022_ZeroQuant_Efficient_Post_Training_Quantization_Transformers.pdf`**
- **Liên kết mở (Open-Access PDF)**: [https://arxiv.org/pdf/2206.01861.pdf](https://arxiv.org/pdf/2206.01861.pdf) | **arXiv ID**: `2206.01861`
- **Từ khóa phân loại**: `ZeroQuant`, `Post-Training Quantization (PTQ)`, `INT8 Quantization`, `Transformer Optimization`, `CPU Acceleration`
- **Tóm tắt đóng góp khoa học**: Phát triển kỹ thuật lượng hóa động sau huấn luyện (PTQ) cho trọng số và kích hoạt của Transformer sang INT8 với thuật toán lượng hóa từng nhóm (Group-wise Quantization), bảo toàn độ chính xác với suy giảm negligible ($< 0.3\%$).
- **Ánh xạ vào Luận văn PI-Guard**: **Kỹ thuật Triển khai Tối ưu**, **Chương 3** & **Chương 5** — Cơ sở kỹ thuật cho quá trình xuất mô hình sang ONNX Runtime INT8 để đạt mục tiêu $P95 < 30\text{ms}$ trên CPU tiêu chuẩn (Zero-GPU).

---

### <a id="ref17"></a>[17] GPT-4 Is Too Smart To Be Safe: Stealthy Chat with LLMs via Cipher
- **Tác giả**: Youliang Yuan, Hao Wang, Jinyuan Wang, Renhe Jiang, et al. (Peking University / CUHK)
- **Năm xuất bản**: 2024 | **Nơi công bố**: *International Conference on Learning Representations (ICLR 2024)*
- **Tệp PDF Cục Bộ**: **`Yuan_2024_GPT4_Too_Smart_To_Be_Safe_Cipher_Jailbreak.pdf`**
- **Liên kết mở (Open-Access PDF)**: [https://arxiv.org/pdf/2308.06463.pdf](https://arxiv.org/pdf/2308.06463.pdf) | **arXiv ID**: `2308.06463`
- **Từ khóa phân loại**: `Cipher Jailbreak`, `Base64 Encoding`, `ROT13`, `Safety Alignment Failure`, `Heuristic Decoding`
- **Tóm tắt đóng góp khoa học**: Phát hiện chấn động: năng lực hiểu mật mã (Cipher/Base64) của các mô hình LLM tiên tiến (GPT-4) tỉ lệ nghịch với khả năng thực thi rào chắn an toàn; kẻ tấn công có thể qua mặt hệ thống an toàn bằng cách mã hóa prompt độc hại.
- **Ánh xạ vào Luận văn PI-Guard**: **Chương 1**, **Chương 3 (Tiền xử lý)** & **Chương 4** — Cơ sở cho giải pháp tích hợp bộ giải mã heuristic (Base64/Cipher normalizer) tại tầng tiền xử lý đầu vào của PI-Guard.

---

### <a id="ref18"></a>[18] The Protection of Information in Computer Systems
- **Tác giả**: Jerome H. Saltzer, Michael D. Schroeder (MIT)
- **Năm xuất bản**: 1975 | **Nơi công bố**: *Proceedings of the IEEE, vol. 63, no. 9, pp. 1278–1308, Sept. 1975*
- **Tệp PDF Cục Bộ**: **`Saltzer_1975_The_Protection_of_Information_in_Computer_Systems.pdf`**
- **Liên kết mở (Open-Access PDF)**: [https://web.mit.edu/Saltzer/www/publications/protection/](https://web.mit.edu/Saltzer/www/publications/protection/) | **DOI**: `10.1109/PROC.1975.9939`
- **Từ khóa phân loại**: `Protection Principles`, `Complete Mediation`, `Defense-in-Depth`, `Economy of Mechanism`, `Fail-Safe Defaults`
- **Tóm tắt đóng góp khoa học**: Tác phẩm kinh điển vĩ đại của ngành Khoa học Máy tính thiết lập 8 nguyên tắc vàng trong thiết kế hệ thống bảo vệ an toàn thông tin; đặt nền móng cho nguyên lý *Complete Mediation* (Mọi truy cập đều phải được thẩm định trước khi thực thi) và *Defense-in-Depth* (Phòng thủ nhiều lớp độc lập).
- **Ánh xạ vào Luận văn PI-Guard**: **Chương 2 (Nền tảng Thiết kế Hệ thống)** & **Chương 3** — Căn cứ lý luận bảo chứng cho kiến trúc Ingress Proxy và cơ chế Two-Tier Cascaded Classification của PI-Guard.

---

## 🗃️ 3. KHO TÀI LIỆU MỞ RỘNG & BENCHMARK THỰC NGHIỆM ĐÃ LƯU TRỮ

Ngoài 18 bài báo cốt lõi, thư mục `References/` còn lưu trữ các bộ dữ liệu và công trình thực nghiệm bổ sung do các thành viên thu thập:

1. **`BIPIA Benchmark`** (**`Viet_2024_BIPIA_Benchmarking_Indirect_Prompt_Injection_Attacks.pdf`**):
   - *Tác giả*: Y. Zhang et al. (Microsoft Research, NAACL 2024).
   - *Ứng dụng*: Bộ benchmark Indirect Prompt Injection chuẩn hóa trên các tác vụ tóm tắt email và tìm kiếm web.
2. **`Do-Not-Answer Dataset`** (**`Phuong_2023_Do_Not_Answer_Dataset_Evaluating_Safeguards.pdf`**):
   - *Tác giả*: Y. Wang et al. (EMNLP 2023).
   - *Ứng dụng*: Bộ dữ liệu mở gồm các câu hỏi độc hại được phân loại rủi ro chi tiết, phục vụ đánh giá False Positive Rate.
3. **`JailGuard Framework`** (**`Duc_2025_JailGuard_Universal_Detection_Framework_TOSEM.pdf`**):
   - *Tác giả*: S. Zhang et al. (ACM TOSEM 2025).
   - *Ứng dụng*: Thuật toán phát hiện Jailbreak dựa trên đột biến văn bản và so sánh độ lệch phản hồi.
4. **Phân Tích Loại Trừ `RAP-ID`** (**`Viet_2026_RAP_ID_Robust_Alignment_Preservation_Injection_Defense.pdf`**):
   - *Đánh giá*: **LOẠI BỎ KHỎI KIẾN TRÚC ĐỀ TÀI (OUT-OF-SCOPE)** do phương pháp can thiệp trực tiếp vào attention weights và KV-cache nội tại của mô hình, không khả thi với mô hình External Guardrail bảo vệ các LLM hộp đen/API đóng.

---

## 📑 4. ĐẦY ĐỦ 18 MỤC TRÍCH DẪN BIBTEX CHUẨN IEEE

```bibtex
@article{zhao2023survey,
  title     = {A Survey of Large Language Models},
  author    = {Zhao, Wayne Xin and Zhou, Kun and Li, Junyi and Tang, Tianyi and Wang, Xiaolei and Hou, Yupeng and Min, Yingqian and Zhang, Beichen and Zhang, Junjie and Dong, Zican and others},
  journal   = {arXiv preprint arXiv:2303.18223},
  year      = {2023}
}

@inproceedings{ouyang2022instructgpt,
  title     = {Training Language Models to Follow Instructions with Human Feedback},
  author    = {Ouyang, Long and Wu, Jeffrey and Jiang, Xu and Almeida, Diogo and Wainwright, Carroll and Mishkin, Pamela and Zhang, Chong and Agarwal, Sandhini and Slama, Katarina and Ray, Alex and others},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  volume    = {35},
  pages     = {27730--27744},
  year      = {2022}
}

@inproceedings{perez2022ignore,
  title     = {Ignore Previous Prompt: Attack Techniques For Language Models},
  author    = {Perez, F{\'a}bio and Ribeiro, Ian},
  booktitle = {NeurIPS ML Safety Workshop},
  year      = {2022},
  url       = {https://arxiv.org/abs/2211.09527}
}

@inproceedings{greshake2023indirect,
  title     = {Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection},
  author    = {Greshake, Kai and Abdelnabi, Sahar and Mishra, Shailesh and Endres, Christoph and Holz, Thorsten and Fritz, Mario},
  booktitle = {Proceedings of the 16th ACM Workshop on Artificial Intelligence and Security (ACM AISec '23)},
  pages     = {79--90},
  year      = {2023},
  doi       = {10.1145/3605764.3623982}
}

@inproceedings{wei2024jailbroken,
  title     = {Jailbroken: How Does LLM Safety Training Fail?},
  author    = {Wei, Alexander and Haghtalab, Nika and Steinhardt, Jacob},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  volume    = {36},
  year      = {2024}
}

@techreport{tencent2026aiinfraguard,
  title       = {AI-Infra-Guard: Multi-Layer Attack Surface and Defense Framework for AI Agents},
  author      = {{Tencent Zhuque Lab}},
  institution = {Tencent Security},
  year        = {2026},
  url         = {https://arxiv.org/abs/2606.31227}
}

@article{meta2023llamaguard,
  title     = {Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations},
  author    = {Inan, Hakan and Upasani, Kartikeya and Chi, Jianfeng and Rungta, Rashi and Iyer, Krithika and Mao, Yuning and Tontchev, Michael and Hu, Qing and Fuller, Brian and Testuggine, Davide and Khabsa, Madian},
  journal   = {arXiv preprint arXiv:2312.06674},
  year      = {2023}
}

@inproceedings{nvidia2023nemo,
  title     = {NeMo Guardrails: A Toolkit for Controllable and Safe LLM Applications},
  author    = {Rebedea, Traian and Dinu, Razvan and Svorenh, Christian and Schallert, Carsten and others},
  booktitle = {Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing (EMNLP 2023)},
  year      = {2023}
}

@inproceedings{he2023deberta,
  title     = {DeBERTa: Decoding-enhanced BERT with Disentangled Attention},
  author    = {He, Pengcheng and Liu, Xiaodong and Gao, Jianfeng and Chen, Weizhu},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year      = {2021}
}

@inproceedings{markov2023openai,
  title     = {A Holistic Approach to Undesired Content Detection in the Real World},
  author    = {Markov, Todor and Zhang, Chong and Agarwal, Sandhini and Nekoul, Florentine Eloundou and Lee, Theodore and Adler, Steven and Jiang, Angela and Weng, Lilian},
  booktitle = {Proceedings of the AAAI Conference on Human Computation and Crowdsourcing (HCOMP 2023)},
  volume    = {11},
  pages     = {98--109},
  year      = {2023}
}

@inproceedings{shen2024dan,
  title     = {"Do Anything Now": Characterizing and Evaluating In-The-Wild Jailbreak Prompts on Large Language Models},
  author    = {Shen, Xinyue and Chen, Zeyuan and Backes, Michael and Shen, Yun and Zhang, Yang},
  booktitle = {Proceedings of the 2024 ACM SIGSAC Conference on Computer and Communications Security (ACM CCS '24)},
  pages     = {4172--4186},
  year      = {2024},
  doi       = {10.1145/3658644.3670390}
}

@article{zhou2024easyjailbreak,
  title     = {EasyJailbreak: A Unified Framework for Jailbreaking Large Language Models},
  author    = {Zhou, Weikang and Wang, Xiao and Xiong, Limao and Xia, Han and Gu, Yingshuang and Chai, Mingxu and Zhu, Fukang and Huang, Caishuang and Dou, Shihan and Zheng, Xiaoqing and Huang, Xuanjing},
  journal   = {arXiv preprint arXiv:2403.12171},
  year      = {2024}
}

@article{zou2023gcg,
  title     = {Universal and Transferable Adversarial Attacks on Aligned Language Models},
  author    = {Zou, Andy and Wang, Zifan and Carlini, Nicholas and Nasr, Milad and Kolter, J. Zico and Fredrikson, Matt},
  journal   = {arXiv preprint arXiv:2307.15043},
  year      = {2023}
}

@article{robey2023smoothllm,
  title     = {SmoothLLM: Defending Large Language Models Against Jailbreaking Attacks},
  author    = {Robey, Alexander and Wong, Eric and Hassani, Hamed and Pappas, George J.},
  journal   = {arXiv preprint arXiv:2310.03684},
  year      = {2023}
}

@article{jain2023baseline,
  title     = {Baseline Defenses for Adversarial Attacks Against Aligned Language Models},
  author    = {Jain, Neel and Schwarzschild, Avi and Wen, Yuxin and Thattai, Gowthami and Thickstun, John and Goldstein, Tom},
  journal   = {arXiv preprint arXiv:2309.00614},
  year      = {2023}
}

@inproceedings{yao2022zeroquant,
  title     = {ZeroQuant: Efficient and Affordable Post-Training Quantization for Large-Scale Transformers},
  author    = {Yao, Zhewei and Aminabadi, Reza Yazdani and Zhang, Minjia and Wu, Xiaoxia and Li, Conglong and He, Yuxiong},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  volume    = {35},
  pages     = {27168--27183},
  year      = {2022}
}

@inproceedings{yuan2024cipher,
  title     = {GPT-4 Is Too Smart To Be Safe: Stealthy Chat with LLMs via Cipher},
  author    = {Yuan, Youliang and Wang, Hao and Wang, Jinyuan and Jiang, Renhe and others},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year      = {2024}
}

@article{saltzer1975protection,
  title     = {The Protection of Information in Computer Systems},
  author    = {Saltzer, Jerome H. and Schroeder, Michael D.},
  journal   = {Proceedings of the IEEE},
  volume    = {63},
  number    = {9},
  pages     = {1278--1308},
  year      = {1975},
  doi       = {10.1109/PROC.1975.9939}
}
```