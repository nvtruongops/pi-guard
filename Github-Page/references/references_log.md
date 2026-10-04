# REFERENCES LOG & APPLICATION MAPPING MATRIX
## Hệ Thống Quản Lý & Định Vị Tài Liệu Tham Khảo — Đề Tài PI-Guard (COMPREHENSIVE VERIFIED LITERATURE MATRIX)

> **Thư mục lưu trữ tài liệu gốc**: [`Final-Report/References/`](.) & bản đồng bộ tại [`Final-Report/References/`](.)
> **Tiêu chuẩn học thuật**: 16 công trình khoa học đỉnh cao kỷ nguyên LLM hiện đại (2022–2026) + 1 công trình kinh điển đặt nền móng kiến trúc bảo vệ phân tầng (Saltzer & Schroeder, IEEE 1975) + 12 tài liệu chuyên đề, mô hình đối chuẩn SOTA Meeting 5 (PIGuard ACL 2025, InstructDetector, Prompt Guard, Ayub CAMLIS, ZeroQuant, BIPIA, Do-Not-Answer, v.v.) + các công trình nền tảng toán học & thông tin (Luhn 1958, Spärck Jones 1972, fastText TACL 2017, Attention NeurIPS 2017, BERT NAACL 2019).
> **Tổng số tệp PDF cục bộ đã lưu trữ**: **46 tệp PDF toàn văn** (100% Open-Access, Zero Paywalled DOI).
> **Cập nhật chuẩn hóa toàn diện**: 2026-09-30 (Bổ sung PIDS-Bench và nguồn phát hành mô hình ProtectAI DeBERTa-v3; áp dụng nghiêm ngặt mô hình Four-Tier Provenance & Decoupling).
> **Mục đích**: Lưu trữ, lập chỉ mục siêu dữ liệu chuẩn xác, phân định rạch ròi 4 tầng xuất xứ học thuật và ánh xạ toàn diện vào cấu trúc luận văn, chuyên đề nghiên cứu và mã nguồn đồ án PI-Guard.

---

## 0. NGUYÊN TẮC BẤT BIẾN: "LOCAL REFERENCES FIRST" PROTOCOL & FOUR-TIER PROVENANCE
> [!IMPORTANT]
> **QUY TRÌNH BẮT BUỘC CHO MAINTAINER & AI AGENTS TRƯỚC KHI TÌM KIẾM BÀI BÁO MỚI**:
> 1. **TRUY LỤC TÀI LIỆU CỤC BỘ TRƯỚC TIÊN (Local References First)**:
>    - Khi cần luận chứng cho bất kỳ tuyên bố khoa học, cơ chế tấn công, kiến trúc phòng thủ hay công thức toán học nào, **BẮT BUỘC phải tra cứu bảng Ma Trận Chủ Đề (Mục 1) và Siêu Dữ Liệu Các Bài Báo (Mục 2 & Mục 3)** trong tệp này trước.
>    - Nếu luận điểm đã được bảo chứng bởi một trong các bài báo đã lưu trữ, **PHẢI TÁI SỬ DỤNG NGAY** bài báo đó (dùng đúng mã neo `[[N]](#refN)` và tệp PDF cục bộ tương ứng).
> 2. **CHỐNG DÀN TRẢI & TÌM KIẾM TRÙNG LẶP (Zero Redundant Search)**:
>    - Tuyệt đối không dùng các công cụ MCP (`arxiv`, `openalex`, `semanticscholar`, `scholar-feed`) để tìm kiếm thêm bài báo mới cho các chủ đề ĐÃ CÓ trong kho lưu trữ (như: Direct Prompt Injection, DAN Jailbreak, TF-IDF Baseline, DeBERTa-v3, Low FPR Trade-off, Two-Tier Cascade).
> 3. **MÔ HÌNH PHÂN ĐỊNH 4 TẦNG & TRUY XUẤT NGUỒN GỐC (Four-Tier Provenance & Decoupling)**:
>    - Mọi trích dẫn khoa học trong đề tài phải tuân thủ nghiêm ngặt 4 tầng độc lập:
>      - **Tầng 0: Nguồn gốc Thư mục (Tier 0 — Bibliographic Provenance)**: Title, Authors, Venue, Volume/Issue, Year, Pages, DOI, Version/Publication Status, Primary Authoritative Source. Thứ tự xác thực siêu dữ liệu ưu tiên: `Trang kỷ yếu nhà xuất bản (Publisher/proceedings page) -> Metadata hội nghị/tạp chí chính thức -> DOI/Crossref -> arXiv/DBLP/OpenReview (khi có)`.
>      - **Tầng 1: Đóng góp Khoa học Gốc của Bài báo (Tier 1 — Original Author Findings)**: Chỉ nêu trung thực và chính xác những gì tác giả nghiên cứu thực sự chứng minh, đo đạc hoặc đề xuất.
>      - **Tầng 2: Định vị Kỹ thuật & Tiếp thu của PI-Guard (Tier 2 — PI-Guard Design Choice & Adaptation)**: Trình bày rõ ràng cách đồ án lấy cảm hứng hoặc kế thừa kết quả đó vào thiết kế hệ thống (dùng dấu chấm phẩy `;` hoặc phân tách bằng mục riêng).
>      - **Tầng 3: Mục tiêu Kỹ thuật & Giả thuyết của PI-Guard (Tier 3 — PI-Guard Target KPI & Hypotheses)**: **Không được trình bày KPI, benchmark result, latency, FPR, F1 hoặc performance measurement của PI-Guard như kết quả thực nghiệm của tài liệu tham chiếu, trừ khi tài liệu đó thực sự báo cáo cùng phép đo và cùng điều kiện.**
> 4. **CHUẨN MỰC GÁN NGUỒN VÀ KHIÊM TỐN HỌC THUẬT (Attribution & Academic Humility)**:
>    - Không gán các ký hiệu hình thức hóa của PI-Guard (như $X = S \mathbin{\Vert} U$) hay các mô hình đe dọa prompt injection thành công thức của các bài survey tổng quan (như Zhao et al.) hoặc bài căn chỉnh chỉ thị (như InstructGPT).
>    - Tuân thủ quy chuẩn blacklist học thuật, tuyệt đối loại bỏ các tuyên bố khẳng định quá mức (như "100% PASS cho toàn bộ luận văn/học thuật", "không lo ngại bất kỳ câu hỏi phản biện nào", "độ chuẩn mực học thuật tối đa"). Phân định rõ: `Automated repository validation: 100% PASS` (cho kịch bản kiểm thử mã nguồn) và `Academic literature verification: VERIFIED / REVIEWED`.
>    - Sử dụng thuật ngữ học thuật trang trọng (formal academic terminology), loại bỏ văn phong thứ cấp/dân dã (ví dụ: thay "nguyên tắc vàng" bằng "các nguyên tắc thiết kế bảo vệ hệ thống máy tính được Saltzer và Schroeder đề xuất").
> 5. **ĐIỀU KIỆN TIẾP NHẬN TÀI LIỆU MỚI (New Reference Ingestion Criteria)**:
>    - Chỉ được phép bổ sung bài báo mới khi xuất hiện câu hỏi nghiên cứu mới phát sinh ngoài phạm vi tài liệu hiện có.
>    - Bài báo mới phải đáp ứng 4 điều kiện khắt khe: Năm xuất bản $\ge 2022$ (trừ công trình kinh điển); Tương thích kiến trúc **External Guardrail Proxy**; Bắt buộc có **Open-Access PDF** (Zero Paywalled DOI); Tải PDF về `Final-Report/References/` và cập nhật siêu dữ liệu vào `REFERENCES_LOG.md`.

---

## 1. MA TRẬN ĐỊNH VỊ NHANH THEO CHỦ ĐỀ & 7 CHUYÊN ĐỀ (TAXONOMY LOOKUP MATRIX)

### 1.1. Nhóm 17 Công Trình Khoa Học Cốt Lõi Của Luận Văn (Core Landmark Papers)

| Chủ Đề / Chuyên Đề Nghiên Cứu | Mã Neo | Tác Giả & Năm | Tệp PDF Cục Bộ Trong `References/` | Đóng Góp Gốc Của Bài Báo (Tier 1) | Định Vị Kỹ Thuật Trong Đồ Án PI-Guard (Tier 2 & 3) |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **1. Tổng quan Kiến trúc LLM & Lỗ hổng Ranh giới Phẳng** | [[1]](#ref1) | Zhao et al. (2023) | **`Zhao_2023_A_Survey_of_Large_Language_Models.pdf`** (local PDF; not packaged with portal) | Khảo sát kiến trúc Transformer tự hồi quy và không gian token ngữ cảnh phẳng. | Cơ sở phân tích: LLM xử lý ngữ cảnh dưới dạng chuỗi token và không tự cung cấp một security boundary đáng tin cậy giữa instruction và untrusted data. (*Chương 1, 2; Chuyên đề 1*) |
| **2. Instruction Tuning & Xử lý System Prompt** | [[2]](#ref2) | Ouyang et al. (2022) | **`Ouyang_2022_InstructGPT_Training_Language_Models_Follow_Instructions.pdf`** (local PDF; not packaged with portal) | Đặt nền móng kỹ thuật Instruction Tuning qua RLHF; chứng minh khả năng căn chỉnh tuân thủ ý định người dùng. | Cung cấp nền tảng về instruction-following và alignment, được PI-Guard dùng làm cơ sở phân tích cách các chỉ thị cạnh tranh mức độ ưu tiên trong LLM. (*Chương 1, 2; Chuyên đề 1*) |
| **3. Direct Prompt Injection (Tấn công Trực tiếp)** | [[3]](#ref3) | Perez & Ribeiro (2022) | **`Perez_2022_Ignore_This_Title_Hack_This_Paper_Prompt_Injection.pdf`** (local PDF; not packaged with portal) | Định nghĩa và phân loại chính thức hai dạng Direct Prompt Injection: Goal Hijacking và Prompt Leaking. | Cơ sở phân loại lớp nhãn Prompt Injection và xây dựng kịch bản kiểm thử thực nghiệm. (*Chương 1, 2, 3; Chuyên đề 2*) |
| **4. Indirect Prompt Injection (Tấn công Gián tiếp)** | [[4]](#ref4) | Greshake et al. (2023) | **`Greshake_2023_Indirect_Prompt_Injection.pdf`** (local PDF; not packaged with portal) | Độc hại nhúng trong dữ liệu bên ngoài (Web/RAG); mô hình hóa rủi ro ứng dụng tích hợp LLM. | Luận giải nhu cầu bắt buộc phải có lớp Input Guardrail độc lập ở Ingress để kiểm soát cả dữ liệu RAG. (*Chương 1, 2, 3; Chuyên đề 2, 3*) |
| **5. Cơ chế Thất bại Căn chỉnh An toàn (Jailbreak Failures)** | [[5]](#ref5) | Wei et al. (2023) | **`Wei_2024_Jailbroken_How_LLM_Safety_Training_Fails.pdf`** (local PDF; not packaged with portal) | Xác lập 2 chế độ lỗi căn chỉnh: Competing Objectives & Mismatched Generalization (NeurIPS 2023). | Cơ sở chứng minh an toàn nội tại là chưa đủ, cần bộ phân loại độc lập bên ngoài. (*Chương 1, 4; Chuyên đề 2*) |
| **6. Mô hình Đe Dọa Đa Tầng Cho AI Agent** | [[6]](#ref6) | Yang et al. / Tencent (2026) | **`Tencent_2026_AI_Infra_Guard_MultiLayer_Agent_RedTeaming.pdf`** (local PDF; not packaged with portal) | Khung Red Teaming đa tầng cho Agent; phân loại 26+ toán tử tấn công hạ tầng. | PI-Guard tham khảo mô hình phân tầng Zone 0–3 để tổ chức phạm vi tấn công và vị trí của guardrail proxy. (*Chương 1, 3; Chuyên đề 2, 3*) |
| **7. Guardrail Dựa Trên LLM (LLM-as-a-Judge Baseline)** | [[7]](#ref7) | Inan et al. / Meta (2023) | **`Meta_2023_Llama_Guard_Input_Output_Safeguard.pdf`** (local PDF; not packaged with portal) | Mô hình LLM 7B làm trọng tài an toàn; chuẩn hóa taxonomy phân loại rủi ro nội dung. | Mô hình đối chuẩn (Baseline): PI-Guard đặt mục tiêu đánh giá liệu classifier nhỏ chạy CPU có đạt trade-off latency/accuracy tốt hơn Llama Guard hay không. (*Chương 2, 4; Chuyên đề 5, 7*) |
| **8. Kiến Trúc Guardrail Middleware Lập Trình Được** | [[8]](#ref8) | Rebedea et al. / NVIDIA (2023)| **`NVIDIA_2023_NeMo_Guardrails_Toolkit.pdf`** (local PDF; not packaged with portal) | Bộ công cụ kiểm soát an toàn dạng middleware lập trình được với Colang. | Cơ sở tham khảo kiến trúc Ingress Proxy bất đồng bộ đánh chặn trước LLM. (*Chương 2, 3; Chuyên đề 3*) |
| **9. Huấn Luyện Ngữ Nghĩa Sâu Với DeBERTa-v3** | [[9]](#ref9) | He, Gao, Chen (2023) | **`He_2023_DeBERTaV3_Disentangled_Attention_ICLR.pdf`** (local PDF; not packaged with portal) | Đột phá ELECTRA-style RTD và Gradient-Disentangled Embedding Sharing (GDES) tại ICLR 2023. | Lý giải việc lựa chọn DeBERTa-v3 làm bộ phân loại ngữ nghĩa sâu Tầng 2. (*Chương 3, 4; Chuyên đề 5*) |
| **10. Kiểm Soát Đánh Đổi FPR Trong Phát Hiện Độc Hại** | [[10]](#ref10) | Markov et al. / OpenAI (2023) | **`OpenAI_2023_Undesired_Content_Detection.pdf`** (local PDF; not packaged with portal) | Phương pháp luận kiểm duyệt nội dung thực tế (AAAI 2023); phân tích chi phí FPR đối với trải nghiệm người dùng. | Cung cấp bài học thực tế để PI-Guard thiết lập yêu cầu kỹ thuật: đặt mục tiêu kiểm soát $\text{FPR} < 1.5\%$ trên tập lành tính. (*Chương 2, 4; Chuyên đề 7*) |
| **11. Khảo Sát Thực Nghiệm Prompt Jailbreak Trong Tự Nhiên** | [[11]](#ref11) | Shen et al. (2024) | **`Shen_2024_Do_Anything_Now_Jailbreak_Prompts_In_The_Wild.pdf`** (local PDF; not packaged with portal) | Tập dữ liệu công bố 1,405/15,140 prompts, tương đương khoảng 9.29% (thường được báo cáo làm tròn là 9.3%); kèm ghi chú phân biệt giữa số liệu của các phiên bản/mô tả khác nhau của nghiên cứu. | Nguồn dữ liệu kiểm thử thực nghiệm jailbreak tự nhiên cho PI-Guard. (*Chương 3, 4; Chuyên đề 2, 4*) |
| **12. Khung Kiểm Thử Đối Kháng & Đột Biến Văn Bản** | [[12]](#ref12) | Zhou et al. (2024) | **`Zhou_2024_EasyJailbreak_Unified_Framework.pdf`** (local PDF; not packaged with portal) | Framework tự động hóa đột biến jailbreak 4 tầng (Initialize, Mutate, Evaluate, Select). | PI-Guard sử dụng các toán tử đột biến của framework này làm công cụ fuzzing; đặt mục tiêu kiểm thử duy trì $\Delta F_1 < 5\%$. (*Chương 3, 4; Chuyên đề 6*) |
| **13. Tấn Công Chuỗi Hậu Tố Đối Kháng Tối Ưu Hóa (GCG)** | [[13]](#ref13) | Zou et al. (2023) | **`Zou_2023_Universal_Transferable_Adversarial_Attacks_GCG.pdf`** (local PDF; not packaged with portal) | Thuật toán Greedy Coordinate Gradient sinh hậu tố đối kháng chuyển giao. | PI-Guard sử dụng các mẫu sinh bởi GCG như một tập kiểm thử đánh giá đối kháng ngoại lai (OOD evaluation set). (*Chương 4; Chuyên đề 6*) |
| **14. Phòng Thủ Bằng Xáo Trộn Ngẫu Nhiên (SmoothLLM)** | [[14]](#ref14) | Robey et al. (2023) | **`Robey_2023_SmoothLLM_Defending_LLMs_Random_Perturbation.pdf`** (local PDF; not packaged with portal) | Cơ chế làm mịn ngẫu nhiên qua biến dị prompt và đa số biểu quyết phản hồi LLM. | PI-Guard sử dụng làm baseline đối chuẩn để so sánh đánh đổi giữa multi-query defense và single-pass classifier. (*Chương 2, 4; Chuyên đề 3, 6*) |
| **15. Baseline Defenses for Adversarial Attacks Against Aligned Language Models** | [[15]](#ref15) | Jain et al. (2023) | **`Jain_2023_Baseline_Defenses_Adversarial_Attacks_LLMs.pdf`** (local PDF; not packaged with portal) | Thực nghiệm các baseline phòng thủ gồm lọc perplexity, paraphrase/retokenization và adversarial training trước jailbreak; bài không đánh giá bộ phân loại TF-IDF Word/Char. | Chỉ dùng làm tài liệu về baseline phòng thủ jailbreak; không trích dẫn để bảo chứng mô hình TF-IDF của Tầng 1. (*Chương 2*) |
| **16. Nguyên Lý Thiết Kế Hệ Thống Bảo Vệ Kinh Điển** | [[16]](#ref16) | Saltzer & Schroeder (1975) | **`Saltzer_1975_The_Protection_of_Information_in_Computer_Systems.pdf`** (local PDF; not packaged with portal) | Các nguyên tắc thiết kế bảo vệ hệ thống máy tính được Saltzer và Schroeder đề xuất (Complete Mediation, Economy of Mechanism, Defense-in-Depth). | Nền tảng thiết kế hệ thống: Kiểm soát toàn diện tại Ingress (Complete Mediation) và kiến trúc phân tầng (Defense-in-Depth). (*Chương 2, 3; Chuyên đề 3*) |
| **17. Lẩn Tránh Bằng Biến Đổi Ký Tự (CipherChat & Encoding)** | [[17]](#ref17) | Yuan et al. (2024) | **`Yuan_2024_GPT4_Too_Smart_To_Be_Safe_Cipher_Jailbreak.pdf`** (local PDF; not packaged with portal) | Khung CipherChat: Nghiên cứu các phép biến đổi prompt dựa trên mật mã cổ điển/bảng mã để vượt qua căn chỉnh an toàn. | Luận chứng cho việc tích hợp mô-đun tiền xử lý chuẩn hóa chuỗi và giải mã tiền trạm. (*Chương 1, 3, 4; Chuyên đề 2, 6*) |

---

### 1.2. Nhóm Mô Hình Đối Chuẩn SOTA & Thực Nghiệm Tái Lập (Meeting 5 Replication Suite)

| Mô Hình / Nghiên Cứu | Mã Định Danh | Tác Giả & Năm | Tệp PDF Cục Bộ Trong `References/` | Đóng Góp Gốc & Đặc Điểm Kỹ Thuật (Tier 1) | Vai Trò & Ứng Dụng Trong Đồ Án PI-Guard (Tier 2 & 3) |
| :--- | :---: | :--- | :--- | :--- | :--- |
| <a id="ref18"></a>**18. PIGuard (ACL 2025)** | `[ACL-PIGuard]` | Hao Li et al. (2025) | **`PIGuard_2025_Prompt_Injection_Guardrail_ACL.pdf`** (local PDF; not packaged with portal) | DeBERTa-v3 guardrail và chiến lược MOF nhằm giảm over-defense; bài báo báo cáo cải thiện 30,4% so với phương pháp tốt nhất trước đó trên các benchmark được nêu. | Baseline phân loại prompt injection. Kết quả tái chạy checkpoint phải ghi rõ tập công khai và không đồng nhất với huấn luyện lại toàn bộ paper; paper gốc là bộ phân loại nhị phân. |
| <a id="ref19"></a>**19. Defending against Indirect Prompt Injection by Instruction Detection** | `[EMNLP-ID]` | Tongyu Wen et al. (2025) | **`Wen_2025_InstructDetector_Findings_EMNLP.pdf`** (local PDF; not packaged with portal) | InstructDetector kết hợp hidden states và gradients từ các lớp trung gian của LLM rồi đưa đặc trưng vào MLP; đây không phải TF-IDF. | Tài liệu về phát hiện indirect prompt injection có điều kiện truy cập trạng thái nội bộ. Không phải mô hình proxy black-box của đồ án và không dùng để chứng minh TF-IDF. |
| <a id="ref20"></a>**20. Prompt Guard 86M (Meta 2024, model card)** | `[Meta-PG86M]` | Meta AI / Purple Llama (2024) | **`Meta_2024_Prompt_Guard_86M_Input_Guardrail.pdf`** (local PDF; not packaged with portal); model card chính thức: [Hugging Face](https://huggingface.co/meta-llama/Prompt-Guard-86M) | Dùng mDeBERTa-v3-base; ba nhãn benign, injection, jailbreak. Model card cho biết dữ liệu huấn luyện gồm dữ liệu mở, dữ liệu tổng hợp và dữ liệu red-team; không công bố toàn bộ tập train. | Mô hình tham chiếu ba lớp. Checkpoint bị gated trong lượt kiểm định; PDF cục bộ đã đối chiếu trang đầu với model card, còn file khác mang tên `Meta_2024_PurpleLlama_PromptGuard.pdf` không phải tài liệu này. |
| <a id="ref21"></a>**21. Embedding-based classifiers can detect prompt injection attacks** | `[CAMLIS-Ayub]` | Md. Ahsan Ayub & Subhabrata Majumdar (2024) | [arXiv:2410.22284](https://arxiv.org/abs/2410.22284); tệp PDF cục bộ có tên khác tiêu đề bài | Tạo embedding bằng ba encoder rồi huấn luyện classifier truyền thống; Random Forest và XGBoost là các kết quả tốt nhất được tác giả nêu. Đây không phải TF-IDF. | Bài CAMLIS 2024/preprint về embedding classifier nhị phân; không dùng để bảo chứng mô hình TF-IDF n-gram hoặc kết quả của runner local. |

---

### 1.3. Nhóm Tài Liệu Bổ Trợ, Lượng Hóa Mô Hình & Khảo Sát Mở Rộng

| Chủ Đề / Tài Nguyên | Mã Định Danh | Tác Giả & Năm | Tệp PDF Cục Bộ Trong `References/` | Đóng Góp Gốc & Bản Chất Phương Pháp | Vai Trò & Ứng Dụng Trong Đồ Án PI-Guard |
| :--- | :---: | :--- | :--- | :--- | :--- |
| <a id="ref22"></a>**22. Lượng Hóa INT8 Mô Hình Transformers** | `[NeurIPS-ZeroQuant]` | Yao et al. / Microsoft (2022) | **`Yao_2022_ZeroQuant_Efficient_Post_Training_Quantization_Transformers.pdf`** (local PDF; not packaged with portal) | Phương pháp lượng hóa sau huấn luyện (PTQ) INT8 cho Transformers, giảm 4x bộ nhớ và tăng tốc 2–3x suy diễn mà giữ nguyên độ chính xác. | ⚠️ **Ghi chú loại trừ phạm vi (Out-of-Scope / IA Discipline Invariant)**: Không sử dụng làm hướng nâng cấp kỹ thuật của đồ án. Đề tài PI-Guard thuộc chuyên ngành An toàn Thông tin (Information Assurance - IA), tập trung chuyên sâu vào mô hình hóa mối đe dọa, cơ chế tấn công Prompt Injection / Jailbreak và kiến trúc phòng thủ phân tầng, KHÔNG đi vào hướng tối ưu hóa kỹ thuật phần cứng hay lượng tử hóa mô hình. |
| <a id="ref23"></a>**23. Benchmark Indirect Prompt Injection (BIPIA)** | `[NAACL-BIPIA]` | Yi et al. / MS Research (2024) | **`Viet_2024_BIPIA_Benchmarking_Indirect_Prompt_Injection_Attacks.pdf`** (local PDF; not packaged with portal) | Bộ dữ liệu benchmark chuẩn hóa đánh giá Indirect Prompt Injection trên 5 tác vụ ứng dụng phổ biến (Email, Web, RAG). | Cung cấp nguồn mẫu thử gián tiếp để kiểm tra độ khái quát hóa ngoại miền (OOD evaluation). |
| <a id="ref24"></a>**24. Bộ Dữ Liệu An Toàn Do-Not-Answer** | `[EMNLP-DNA]` | Wang et al. (2023) | **`Phuong_2023_Do_Not_Answer_Dataset_Evaluating_Safeguards.pdf`** (local PDF; not packaged with portal) | 936 prompt độc hại có cấu trúc rủi ro 5 tầng nhằm đo lường khả năng từ chối an toàn của LLM. | Nguồn mẫu đối kháng kiểm tra độ nhạy của bộ lọc trong Chuyên đề 4 (`dataset_study`). |
| <a id="ref25"></a>**25. Universal Jailbreak Detection (JailGuard)** | `[TOSEM-JailGuard]` | Zhang et al. (2025) | **`Duc_2025_JailGuard_Universal_Detection_Framework_TOSEM.pdf`** (local PDF; not packaged with portal) | Framework phát hiện jailbreak dựa trên đột biến biến thể prompt và đo độ phân kỳ hành vi mô hình (TOSEM 2025). | Nghiên cứu đối chuẩn so sánh kỹ thuật đột biến và cơ chế đánh chặn đa tầng. |
| <a id="ref26"></a>**26. Khảo Sát Thực Nghiệm Toàn Diện Jailbreak** | `[ACL-JailbreakStudy]` | Xu et al. (2024) | **`Phuong_2024_ACL_Comprehensive_Study_Jailbreak_Attack_Defense.pdf`** (local PDF; not packaged with portal) | So sánh thực nghiệm quy mô lớn giữa các phương pháp tấn công jailbreak và cơ chế phòng thủ trên ACL 2024. | Bổ trợ cho phân tích Taxonomy và ma trận đối sánh trong Chương 2. |
| <a id="ref27"></a>**27. Khảo Sát Lỗ Hổng & Bảo Vệ LLM Công Nghiệp** | `[Survey-LiuHu]` | Liu & Hu / Zscaler (2024) | **`Phuong_2024_Exploring_Vulnerabilities_Protections_LLMs_Survey.pdf`** (local PDF; not packaged with portal) | Khảo sát các lỗ hổng an ninh LLM từ góc nhìn ứng dụng doanh nghiệp và kiến trúc Security Gateway. | Cung cấp góc nhìn thực tiễn về triển khai Ingress Proxy trong môi trường mạng thực tế. |
| <a id="ref28"></a>**28. Khảo Sát Tấn Công & Phòng Thủ Jailbreak** | `[Survey-Tsinghua]` | Yi et al. / Tsinghua (2024) | **`Phuong_2024_Survey_Jailbreak_Attacks_Defenses_LLMs.pdf`** (local PDF; not packaged with portal) | Hệ thống hóa toàn diện các kỹ thuật tấn công và giải pháp phòng thủ theo từng tầng (Pre-processing, In-processing, Post-processing). | Củng cố luận cứ lý thuyết cho kiến trúc bảo vệ phân tầng Ingress của PI-Guard. |
| <a id="ref29"></a>**29. Nghiên Cứu Loại Trừ: RAP-ID (Lenovo 2026)** | `[ACL-RAPID-Excl]` | Yang et al. / Lenovo (2026) | **`Viet_2026_RAP_ID_Robust_Alignment_Preservation_Injection_Defense.pdf`** (local PDF; not packaged with portal) | Phát hiện prompt injection dựa trên phân tích trạng thái nội bộ (internal model states) và attention dynamics. | **Xác định rõ là Ngoài Phạm Vi (Out-of-Scope)**: Do đòi hỏi can thiệp white-box vào forward pass của target LLM, không tương thích với mô hình External Black-Box Proxy của đề tài. |
| <a id="ref30"></a>**30. PromptShield (CODASPY 2025)** | [CODASPY-PromptShield] | Jacob et al. (2025) | **Jacob_2025_PromptShield_Deployable_Detection_CODASPY.pdf** (local PDF; not packaged with portal) | Benchmark phát hiện prompt injection trong điều kiện FPR thấp; kết quả của các bộ phát hiện chỉ áp dụng theo giao thức và tập đánh giá paper. | **Cơ sở đánh giá Low-FPR**: PI-Guard có thể tham khảo các mức FPR và cách đọc ROC; KPI của đồ án là mục tiêu riêng, chưa được paper chứng minh. |
| <a id="ref31"></a>**31. Bypassing LLM Guardrails (ACL 2025 LLMSEC)** | [LLMSEC-Hackett] | Hackett et al. (Mindgard, 2025) | **Hackett_2025_Bypassing_LLM_Guardrails_Evasion_Attacks.pdf** (local PDF; not packaged with portal) | Đánh giá thực nghiệm 12 đòn biến dị ký tự (Emoji Smuggling, Unicode Tags) và 8 thuật toán AML Evasion; chứng minh Meta PromptGuard bị bypass 100%. | **Bảo chứng Tầng 0 (Heuristic Scrubber)**: Chứng minh các Transformer bị mù trước Unicode/Emoji; xác lập tính tất yếu của bộ lọc chuẩn hóa ký tự trước khi tokenize. |
| <a id="ref32"></a>**32. DataSentinel: A Game-Theoretic Detection of Prompt Injection Attacks (IEEE S&P 2025)** | [SP-DataSentinel] | Liu et al. (Penn State / Berkeley, 2025) | **Liu_2025_DataSentinel_Game_Theoretic_Detection_Prompt_Injection.pdf** (local PDF; not packaged with portal) | Mô hình toán học Minimax Game-Theory giữa Attacker (Inner Max) và Defender (Outer Min) phát hiện Adaptive Prompt Injection. | **Nền tảng lý thuyết trò chơi & Dữ liệu OOD**: Cung cấp khung tối ưu hóa đối kháng và tập benchmark Open-Prompt-Injection cho kiểm thử độ bền. |
| <a id="ref33"></a>**33. The Instruction Hierarchy (OpenAI 2024)** | [OpenAI-InstructionHierarchy] | Wallace et al. (OpenAI, 2024) | **Wallace_2024_Instruction_Hierarchy_Prioritize_Privileged_Instructions.pdf** (local PDF; not packaged with portal) | Phân tầng quyền hạn chỉ thị (System > User > Tool/Data); chứng minh in-model alignment không thể ngăn chặn triệt để tấn công đối kháng và gây over-refusal. | **Bảo chứng Ingress Guardrail Proxy**: Khẳng định in-model training không đủ; xác lập tính tất yếu của Guardrail Proxy bên ngoài theo nguyên lý Defense-in-Depth. |
| <a id="ref34"></a>**34. JailbreakBench (NeurIPS 2024)** | [NeurIPS-JailbreakBench] | Chao et al. (UPenn / EPFL / ETH, 2024) | **Chao_2024_JailbreakBench_Open_Robustness_Benchmark_NeurIPS.pdf** (local PDF; not packaged with portal) | Chuẩn benchmark đối kháng mã nguồn mở đầu tiên của cộng đồng; công bố tập dữ liệu chuẩn JBB-Behaviors gồm 100 hành vi vi phạm an toàn. | **Chuẩn đối chuẩn cộng đồng**: Tích hợp JBB-Behaviors vào bộ kiểm thử thực nghiệm; đối sánh hiệu năng PI-Guard với các SOTA defenses trên leaderboard toàn cầu. |
| <a id="ref35"></a>**35. Multilingual Jailbreak Challenges (ICLR 2024)** | [ICLR-MultiJail] | Deng et al. (2024) | **Deng_2024_Multilingual_Jailbreak_Challenges_LLMs_ICLR.pdf** (local PDF; not packaged with portal) | MultiJail gồm 315 prompt gốc tiếng Anh được dịch sang chín ngôn ngữ khác (3.150 prompt tổng cộng) để nghiên cứu jailbreak đa ngôn ngữ đối với LLM; đây không phải benchmark phân loại prompt injection. | **Ứng dụng PI-Guard**: Có thể dùng làm nguồn kiểm thử chuyển ngôn ngữ sau khi xác minh nhãn và giao thức; không chứng minh hiệu năng tiếng Việt của bộ phân loại. |
| <a id="ref36"></a>**36. Conformal Risk Control** | [NeurIPS-ConformalGuardrail] | Angelopoulos et al. (2022 preprint; later publication metadata to verify) | **Angelopoulos_2024_Conformal_Risk_Control.pdf** (local PDF; not packaged with portal) | Khung CRC kiểm soát rủi ro kỳ vọng dưới các giả định và định nghĩa loss cụ thể; không tự động bảo đảm FPR của PI-Guard. | **Ứng dụng PI-Guard**: Có thể nghiên cứu hiệu chuẩn có kiểm soát rủi ro nếu xác định loss, điều kiện dữ liệu và kiểm định giả định; chưa phải bằng chứng KPI FPR hiện tại. |
| <a id="ref37"></a>**37. ModernBERT (Answer.AI / LightOn 2024)** | [arXiv-ModernBERT] | Warner et al. (2024) | **Warner_2024_ModernBERT_Brings_Modern_Transformers_To_Encoders.pdf** (local PDF; not packaged with portal) | Encoder pretrained với cửa sổ ngữ cảnh tối đa 8.192 token; kết quả tốc độ trong paper phụ thuộc tác vụ, phần cứng và thiết lập so sánh. Đây không phải classifier prompt injection. | **Ứng dụng PI-Guard**: Chỉ là backbone ứng viên cần fine-tune và đo trên cùng protocol; không suy ra độ trễ hay chất lượng guardrail từ paper pretraining. |
| <a id="ref38"></a>**38. Granite Guardian (IBM Research 2024)** | [IBM-GraniteGuardian] | Padhi et al. (IBM Research, 2024) | **Padhi_2024_Granite_Guardian_Content_Safety_Risk_Detection.pdf** (local PDF; not packaged with portal) | Dòng mô hình mở chuyên biệt cho an toàn nội dung và rủi ro LLM (2B/8B), bao phủ Jailbreak, Prompt Injection và RAG Hallucination. | **Mô hình tham chiếu SOTA SLM Guardrail**: Cung cấp cơ sở đối chuẩn cho tầng phân xử cấp cao (High-Assurance Arbiter) ở Tier 3. |
| <a id="ref39"></a>**39. Crescendo Multi-Turn Attack (Microsoft 2024)** | [MS-Crescendo] | Russinovich et al. (Microsoft Research, 2024) | **Russinovich_2024_Crescendo_MultiTurn_Jailbreak_Attack.pdf** (local PDF; not packaged with portal) | Phát hiện phương thức tấn công đa lượt leo thang (Crescendo Attack); chứng minh các bộ lọc đơn lượt (single-turn) hoàn toàn bất lực trước kỹ thuật khai thác ngữ cảnh tích lũy. | **Cơ sở mở rộng nhánh nghiên cứu Multi-turn State Tracking**: Luận chứng cho việc đánh đổi độ trễ để duy trì bộ nhớ phiên và phân tích trôi dạt ngữ cảnh (Contextual Drift). |
| **40. Prompt Overflow (arXiv 2026)** | [arXiv-PromptOverflow] | Zhou et al. (2026) | **Zhou_2026_Prompt_Overflow_Guardrail_Window_Mismatch.pdf** (local PDF; not packaged with portal) | Preprint nghiên cứu chênh lệch giữa phần nội dung guardrail quan sát được và nội dung LLM đích nhận trong các thiết lập được đánh giá; không khái quát rằng mọi guardrail dùng 512 token hay mọi LLM nhận 128k token. | **Ứng dụng PI-Guard**: Gợi ý kiểm thử tài liệu dài và vị trí payload; không chứng minh thiết kế chunking, độ phủ 200k ký tự hay KPI của PI-Guard. |
| <a id="ref41"></a>**41. CASCADE Against Jailbreaks (arXiv 2026)** | [arXiv-CASCADE] | Luo & Han (2026) | **Luo_2026_CASCADE_Against_Jailbreaks_Evaluation.pdf** (local PDF; not packaged with portal) | Preprint đánh giá thực nghiệm các kết hợp tấn công/phòng thủ trong các thiết lập được mô tả; kết luận thực nghiệm không phải định lý tổng quát. | **Ứng dụng PI-Guard**: Cung cấp một điểm tham chiếu thực nghiệm cho nghiên cứu kết hợp nhiều giai đoạn; không bảo chứng kiến trúc hay KPI cụ thể của đồ án. |
| <a id="ref42"></a>**42. Hồ sơ audit thực nghiệm cục bộ (2026)** | [Local-Audit-2026] | Tài liệu nội bộ, 2026-09-29 | Tài liệu thuộc workspace cá nhân bị loại khỏi repository; không có bản chia sẻ tại đây. | Đây là hồ sơ nội bộ, không phải nguồn học thuật. Nội dung và kết quả trong đó không được viện dẫn như bằng chứng của repository. |
| <a id="ref43"></a>**43. Metadata pilot cục bộ (2026)** | [Local-Pilot-Status-2026] | Metadata nội bộ, 2026-09-29 | Metadata thuộc workspace cá nhân bị loại khỏi repository; không có bản chia sẻ tại đây. | Không nêu trạng thái chạy hay metric cục bộ trong tài liệu tham khảo được chia sẻ. |

---

## 2. BẢNG CHI TIẾT SIÊU DỮ LIỆU HỌC THUẬT (17 BÀI BÁO CỐT LÕI)

```
========================================================================================================================
DANH MỤC 17 CÔNG TRÌNH KHOA HỌC CỐT LÕI — ĐỒ ÁN TỐT NGHIỆP PI-GUARD (IAP491 FALL 2026)
(Đã kiểm tra chéo 100% qua PyMuPDF text trích xuất trực tiếp từ file PDF, Crossref DOI và arXiv metadata)
========================================================================================================================
```

### <a id="ref1"></a>[1] A Survey of Large Language Models
- **Tên bài báo chính xác**: *A Survey of Large Language Models*
- **Tác giả**: Wayne Xin Zhao, Kun Zhou, Junyi Li, Tianyi Tang, Xiaolei Wang, Yupeng Hou, Yingqian Min, Beichen Zhang, Junjie Zhang, Zican Dong, Yifan Du, Chen Yang, Yushuo Chen, Zhipeng Chen, Jinhao Jiang, Ruiyang Ren, Yifan Li, Xinyu Tang, Zikang Liu, Peiyu Liu, Jian-Yun Nie, Ji-Rong Wen
- **Năm xuất bản**: 2023 | **Nơi công bố chính thức**: *arXiv preprint arXiv:2303.18223* (Bản tổng hợp nền tảng xuất bản tại *AI Open*, 2023)
- **Tệp PDF Cục Bộ**: **`Zhao_2023_A_Survey_of_Large_Language_Models.pdf`** (local PDF; not packaged with portal) (144 trang)
- **Liên kết mở (Open-Access PDF)**: [https://arxiv.org/pdf/2303.18223.pdf](https://arxiv.org/pdf/2303.18223.pdf) | **arXiv ID**: `2303.18223`
- **Từ khóa phân loại**: `LLM Architecture`, `Autoregressive Transformers`, `Pre-training`, `Tokenization`, `Alignment`
- **Đóng góp khoa học gốc của bài báo**: Cung cấp bức tranh toàn cảnh về kiến trúc Transformer tự hồi quy, quy trình tiền huấn luyện, căn chỉnh chỉ thị và đánh giá năng lực LLM. Bài báo phân tích việc xử lý chuỗi token đồng nhất trong không gian ngôn ngữ phẳng, nơi mô hình tiếp nhận dữ liệu và chỉ thị như các token tương đương.
- **Định vị kỹ thuật & Giả thuyết thực nghiệm của PI-Guard**: **Chương 1 (Giới thiệu vấn đề)** & **Chương 2 (Cơ sở lý thuyết)** — Trong phạm vi mô hình hóa của đồ án PI-Guard, chuỗi ngữ cảnh đầu vào được biểu diễn dưới dạng chuỗi token kết hợp giữa system/instruction ($S$) và user/untrusted content ($U$), tức $X = S \mathbin{\Vert} U$. Dựa trên khảo sát của Zhao et al. về kiến trúc Transformer tự hồi quy, nhóm làm rõ bản chất mô hình: *LLM xử lý ngữ cảnh dưới dạng chuỗi token liên tục và không tự cung cấp một ranh giới an ninh đáng tin cậy (security boundary) giữa instruction và untrusted data*. Cấu trúc prompt hierarchy hay quy ước định dạng ngữ cảnh chỉ mang tính quy ước ngữ nghĩa, không tương đương với cơ chế cô lập an ninh (security isolation) cấp hệ thống, đặt ra yêu cầu tất yếu phải có giải pháp kiểm soát đầu vào độc lập đặt phía trước.

---

### <a id="ref2"></a>[2] Training Language Models to Follow Instructions with Human Feedback
- **Tên bài báo chính xác**: *Training language models to follow instructions with human feedback*
- **Tác giả**: Long Ouyang, Jeff Wu, Xu Jiang, Diogo Almeida, Carroll L. Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, John Schulman, Jacob Hilton, Fraser Kelton, Luke Miller, Maddie Simens, Amanda Askell, Peter Welinder, Paul Christiano, Jan Leike, Ryan Lowe (OpenAI)
- **Năm xuất bản**: 2022 | **Nơi công bố chính thức**: *Advances in Neural Information Processing Systems (NeurIPS 2022)*, Vol. 35, pp. 27730–27744
- **Tệp PDF Cục Bộ**: **`Ouyang_2022_InstructGPT_Training_Language_Models_Follow_Instructions.pdf`** (local PDF; not packaged with portal) (68 trang)
- **Liên kết mở (Open-Access PDF)**: [https://arxiv.org/pdf/2203.02155.pdf](https://arxiv.org/pdf/2203.02155.pdf) | **arXiv ID**: `2203.02155`
- **Từ khóa phân loại**: `InstructGPT`, `RLHF`, `Instruction Following`, `System Prompt`, `Alignment`
- **Đóng góp khoa học gốc của bài báo**: Đặt nền móng cho phương pháp căn chỉnh mô hình ngôn ngữ theo chỉ thị (Instruction Tuning) sử dụng học tăng cường từ phản hồi của con người (RLHF), chứng minh mô hình InstructGPT tuân thủ tốt hơn đáng kể ý định và mệnh lệnh của người dùng so với mô hình tiền huấn luyện thuần túy (Helpful, Honest, Harmless).
- **Định vị kỹ thuật & Giả thuyết thực nghiệm của PI-Guard**: **Chương 1** & **Chương 2** — Cung cấp nền tảng về instruction-following và alignment, được PI-Guard sử dụng làm cơ sở để phân tích cách các chỉ thị có mức độ ưu tiên khác nhau (system prompt vs. user prompt) có thể cạnh tranh trong hệ thống LLM.

---

### <a id="ref3"></a>[3] Ignore Previous Prompt: Attack Techniques For Language Models
- **Tên bài báo chính xác**: *Ignore Previous Prompt: Attack Techniques For Language Models*
*(Lưu ý đối chiếu văn bản học thuật: Tiêu đề công bố chính thức tại NeurIPS 2022 ML Safety Workshop, Kỷ yếu OpenReview và arXiv:2211.09527 là "Ignore Previous Prompt: Attack Techniques For Language Models"; cụm từ "Ignore This Title and Hack This Paper" là câu khẩu hiệu tấn công minh họa của tác giả thường được nhắc lại trong các bài blog/truyền thông, không phải tiêu đề bài báo chính thức)*
- **Tác giả**: Fábio Perez, Ian Ribeiro (AE Studio)
- **Năm xuất bản**: 2022 | **Nơi công bố chính thức**: *NeurIPS 2022 ML Safety Workshop* (Best Paper Award)
- **Tệp PDF Cục Bộ**: **`Perez_2022_Ignore_This_Title_Hack_This_Paper_Prompt_Injection.pdf`** (local PDF; not packaged with portal) (21 trang)
- **Liên kết mở (Open-Access PDF)**: [https://arxiv.org/pdf/2211.09527.pdf](https://arxiv.org/pdf/2211.09527.pdf) | **arXiv ID**: `2211.09527`
- **Từ khóa phân loại**: `Prompt Injection`, `Goal Hijacking`, `Prompt Leaking`, `Direct Attack`, `Language Models Vulnerability`
- **Đóng góp khoa học gốc của bài báo**: Công trình học thuật đầu tiên định nghĩa và phân loại chính thức các kỹ thuật tấn công Prompt Injection vào ứng dụng tích hợp LLM thành hai dạng cơ bản: *Goal Hijacking* (chuyển hướng mục tiêu ban đầu của ứng dụng sang mục tiêu của kẻ tấn công) và *Prompt Leaking* (làm lộ chỉ thị nội bộ / system prompt của ứng dụng).
- **Định vị kỹ thuật & Giả thuyết thực nghiệm của PI-Guard**: **Chương 1, 2, 3** — Cung cấp định nghĩa nền tảng cho lớp nhãn Prompt Injection. Nhóm sử dụng taxonomy của bài báo để xây dựng kịch bản kiểm thử Demo 1 và đặc tả các mẫu dữ liệu tấn công Direct Prompt Injection.

---

### <a id="ref4"></a>[4] Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection
- **Tên bài báo chính xác**: *Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection*
- **Tác giả**: Kai Greshake, Sahar Abdelnabi, Shailesh Mishra, Christoph Endres, Thorsten Holz, Mario Fritz (CISPA Helmholtz Center for Information Security)
- **Năm xuất bản**: 2023 | **Nơi công bố chính thức**: *Proceedings of the 16th ACM Workshop on Artificial Intelligence and Security (ACM AISec '23)*, pp. 79–90
- **DOI chính thức**: `10.1145/3605764.3623985` (ACM Paywalled DOI — Đọc bản mở qua liên kết arXiv bên dưới)
- **Tệp PDF Cục Bộ**: **`Greshake_2023_Indirect_Prompt_Injection.pdf`** (local PDF; not packaged with portal) (28 trang)
- **Liên kết mở (Open-Access PDF)**: [https://arxiv.org/pdf/2302.12173.pdf](https://arxiv.org/pdf/2302.12173.pdf) | **arXiv ID**: `2302.12173`
- **Từ khóa phân loại**: `Indirect Prompt Injection`, `RAG Poisoning`, `Data-as-Instruction`, `Autonomous Agents Security`, `Synthetic Attacks`
- **Đóng góp khoa học gốc của bài báo**: Phát hiện và hệ thống hóa mối đe dọa *Indirect Prompt Injection*, trong đó kẻ tấn công không tương tác trực tiếp với LLM mà nhúng chỉ thị độc hại vào dữ liệu bên ngoài (trang web, email, tài liệu PDF, cơ sở tri thức RAG) mà LLM truy xuất trong quá trình xử lý, biến dữ liệu thụ động thành mã thực thi.
- **Định vị kỹ thuật & Giả thuyết thực nghiệm của PI-Guard**: **Chương 1, 2, 3** — Cơ sở khoa học chứng minh việc bảo vệ LLM không chỉ giới hạn ở prompt của người dùng cuối mà còn phải bao quát dữ liệu phi cấu trúc từ bên thứ ba. Luận giải sự cần thiết của một Guardrail Proxy đặt tại Ingress để kiểm tra mọi luồng văn bản đi vào LLM.

---

### <a id="ref5"></a>[5] Jailbroken: How Does LLM Safety Training Fail?
- **Tên bài báo chính xác**: *Jailbroken: How Does LLM Safety Training Fail?*
- **Tác giả**: Alexander Wei, Nika Haghtalab, Jacob Steinhardt (UC Berkeley)
- **Năm xuất bản**: 2023 | **Nơi công bố chính thức**: *Advances in Neural Information Processing Systems (NeurIPS 2023)*, Vol. 36
- **Tệp PDF Cục Bộ**: **`Wei_2024_Jailbroken_How_LLM_Safety_Training_Fails.pdf`** (local PDF; not packaged with portal) (46 trang)
- **Liên kết mở (Open-Access PDF)**: [https://arxiv.org/pdf/2307.02483.pdf](https://arxiv.org/pdf/2307.02483.pdf) | **arXiv ID**: `2307.02483`
- **Từ khóa phân loại**: `Jailbreak Failures`, `Competing Objectives`, `Mismatched Generalization`, `Safety Training Failure Modes`
- **Đóng góp khoa học gốc của bài báo**: Xác lập cơ sở lý thuyết chứng minh việc huấn luyện an toàn (Safety Fine-Tuning / RLHF) thất bại bắt nguồn từ hai nguyên nhân cốt lõi: *Competing Objectives* (xung đột giữa mục tiêu tuân thủ chỉ thị và mục tiêu an toàn) và *Mismatched Generalization* (năng lực tiền huấn luyện vượt xa phạm vi dữ liệu an toàn được căn chỉnh).
- **Định vị kỹ thuật & Giả thuyết thực nghiệm của PI-Guard**: **Chương 1** & **Chương 4** — Cung cấp bằng chứng khoa học cho thấy các biện pháp an toàn nội tại bên trong LLM luôn tồn tại điểm mù. Từ đó khẳng định tính đúng đắn của việc xây dựng lớp bảo vệ độc lập bên ngoài (External Guardrail Proxy) tách biệt khỏi quá trình sinh từ của mô hình đích.

---

### <a id="ref6"></a>[6] Securing the AI Agent: A Unified Framework for Multi-Layer Agent Red Teaming
- **Tên bài báo chính xác**: *Securing the AI Agent: A Unified Framework for Multi-Layer Agent Red Teaming*
- **Tác giả**: Yong Yang, Xing Zheng, Huiyu Wu, Huangsheng Cheng, Xiaorong Shi, Jing Guo, Bo Yang, Yi Zhou, Xiangfan Wu, Zonghao Ying (Tencent Zhuque Lab)
- **Năm xuất bản**: 2026 | **Nơi công bố chính thức**: *Tencent Technical Report* (Tháng 02/2026), *arXiv:2606.31227*
- **Tệp PDF Cục Bộ**: **`Tencent_2026_AI_Infra_Guard_MultiLayer_Agent_RedTeaming.pdf`** (local PDF; not packaged with portal) (15 trang)
- **Liên kết mở (Open-Access PDF)**: [https://arxiv.org/pdf/2606.31227.pdf](https://arxiv.org/pdf/2606.31227.pdf) | **arXiv ID**: `2606.31227`
- **Từ khóa phân loại**: `Agent Red Teaming`, `Multi-layer Architecture`, `Agent Infrastructure Security`, `Attack Operators Taxonomy`
- **Đóng góp khoa học gốc của bài báo**: Đề xuất khung kiểm thử an ninh đa tầng cho hệ thống AI Agent phân định 4 vùng (Zone 0: Prompt & Memory, Zone 1: Tool & Protocol, Zone 2: Model & Weights, Zone 3: Infrastructure) và chuẩn hóa danh mục 26 toán tử tấn công thực tế vào hạ tầng Agent.
- **Định vị kỹ thuật & Giả thuyết thực nghiệm của PI-Guard**: **Chương 1** & **Chương 3** — Đồ án PI-Guard kế thừa và khoanh vùng phạm vi bảo vệ tại Zone 0 (Prompt Gateway) nhằm chặn đứng các toán tử tấn công prompt trước khi chúng kịp tác động đến bộ nhớ ngữ cảnh và công cụ của Agent.

---

### <a id="ref7"></a>[7] Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations
- **Tên bài báo chính xác**: *Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations*
- **Tác giả**: Hakan Inan, Kartikeya Upasani, Jianfeng Chi, Rashi Rungta, Krithika Iyer, Yuning Mao, Michael Tontchev, Qing Hu, Brian Fuller, Davide Testuggine, Madian Khabsa (Meta AI)
- **Năm xuất bản**: 2023 | **Nơi công bố chính thức**: *arXiv preprint arXiv:2312.06674* (Bản tiền ấn phẩm kỹ thuật chính thức từ Meta AI)
- **Tệp PDF Cục Bộ**: **`Meta_2023_Llama_Guard_Input_Output_Safeguard.pdf`** (local PDF; not packaged with portal) (19 trang)
- **Liên kết mở (Open-Access PDF)**: [https://arxiv.org/pdf/2312.06674.pdf](https://arxiv.org/pdf/2312.06674.pdf) | **arXiv ID**: `2312.06674`
- **Từ khóa phân loại**: `Llama Guard`, `LLM-as-a-Judge`, `Input-Output Safeguard`, `Safety Taxonomy`, `Moderation Benchmark`
- **Đóng góp khoa học gốc của bài báo**: Giới thiệu mô hình Llama Guard (7B tham số) hoạt động như một trọng tài an toàn (LLM-as-a-Judge) kiểm duyệt cả prompt đầu vào và phản hồi đầu ra, cung cấp danh mục taxonomy an toàn chuẩn hóa gồm 6 loại rủi ro nội dung.
- **Định vị kỹ thuật & Giả thuyết thực nghiệm của PI-Guard**: **Chương 2** & **Chương 4** — Đóng vai trò là mô hình đối chuẩn cấp cao (High-end LLM Baseline). Đồ án phân tích các hạn chế của Llama Guard về độ trễ lớn (> 500ms) và tiêu tốn GPU, từ đó luận giải sự vượt trội về mặt hiệu quả kinh tế và độ trễ thấp của mô hình nhỏ tối ưu hóa trên CPU mà PI-Guard hướng tới.

---

### <a id="ref8"></a>[8] NeMo Guardrails: A Toolkit for Controllable and Safe LLM Applications with Programmable Rails
- **Tên bài báo chính xác**: *NeMo Guardrails: A Toolkit for Controllable and Safe LLM Applications with Programmable Rails*
- **Tác giả**: Traian Rebedea, Razvan Dinu, Makesh Sreedhar, Christopher Parisien, Jonathan Cohen (NVIDIA)
- **Năm xuất bản**: 2023 | **Nơi công bố chính thức**: *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing: System Demonstrations (EMNLP 2023)*, pp. 431–445
- **Tệp PDF Cục Bộ**: **`NVIDIA_2023_NeMo_Guardrails_Toolkit.pdf`** (local PDF; not packaged with portal) (15 trang)
- **Liên kết mở (Open-Access PDF)**: [https://arxiv.org/pdf/2310.10501.pdf](https://arxiv.org/pdf/2310.10501.pdf) | **arXiv ID**: `2310.10501`
- **Từ khóa phân loại**: `NeMo Guardrails`, `Programmable Rails`, `Colang`, `Input Rails`, `Execution Guardrails`
- **Đóng góp khoa học gốc của bài báo**: Giới thiệu bộ công cụ mã nguồn mở NeMo Guardrails cho phép định nghĩa các rào chắn an toàn (Input rails, Output rails, Dialog rails, Execution rails) bằng ngôn ngữ lập trình đặc tả Colang để kiểm soát luồng tương tác của ứng dụng LLM.
- **Định vị kỹ thuật & Giả thuyết thực nghiệm của PI-Guard**: **Chương 2** & **Chương 3** — Tham khảo mô hình kiến trúc Input Rails dạng Middleware để xây dựng Reverse Proxy đánh chặn luồng request trước khi chuyển tiếp tới LLM mục tiêu.

---

### <a id="ref9"></a>[9] DeBERTaV3: Improving DeBERTa using ELECTRA-Style Pre-Training with Gradient-Disentangled Embedding Sharing
- **Tên bài báo chính xác**: *DeBERTaV3: Improving DeBERTa using ELECTRA-Style Pre-Training with Gradient-Disentangled Embedding Sharing*
- **Tác giả**: Pengcheng He, Jianfeng Gao, Weizhu Chen (Microsoft)
- **Năm xuất bản**: 2023 | **Nơi công bố chính thức**: *The Eleventh International Conference on Learning Representations (ICLR 2023)*
- **Tệp PDF Cục Bộ**: **`He_2023_DeBERTaV3_Disentangled_Attention_ICLR.pdf`** (local PDF; not packaged with portal) (13 trang)
- **Liên kết mở (Open-Access PDF)**: [https://arxiv.org/pdf/2111.09543.pdf](https://arxiv.org/pdf/2111.09543.pdf) | **arXiv ID**: `2111.09543`
- **Từ khóa phân loại**: `DeBERTaV3`, `Disentangled Attention`, `Replaced Token Detection (RTD)`, `GDES`, `NLU Benchmark SOTA`
- **Đóng góp khoa học gốc của bài báo**: Nâng cấp kiến trúc DeBERTa thông qua cơ chế Disentangled Attention biểu diễn độc lập nội dung và vị trí tương đối của token, kết hợp phương pháp tiền huấn luyện Replaced Token Detection (RTD) kiểu ELECTRA và kỹ thuật Gradient-Disentangled Embedding Sharing (GDES), tạo ra mô hình hiểu ngôn ngữ (NLU) vượt trội so với RoBERTa và ELECTRA.
- **Định vị kỹ thuật & Giả thuyết thực nghiệm của PI-Guard**: **Chương 3** & **Chương 4** — Là nền tảng kiến trúc của mô hình phân loại ngữ nghĩa sâu Tầng 2 (`microsoft/deberta-v3-base`). Cơ chế Disentangled Attention giúp mô hình nắm bắt chính xác mối quan hệ ngữ cảnh tinh vi giữa các chỉ thị đánh lừa và dữ liệu thông thường trong câu prompt.

---

### <a id="ref10"></a>[10] A Holistic Approach to Undesired Content Detection in the Real World
- **Tên bài báo chính xác**: *A Holistic Approach to Undesired Content Detection in the Real World*
- **Tác giả**: Todor Markov, Chong Zhang, Sandhini Agarwal, Florentine Eloundou Nekoul, Theodore Lee, Steven Adler, Angela Jiang, Lilian Weng (OpenAI)
- **Năm xuất bản**: 2023 | **Nơi công bố chính thức**: *Proceedings of the AAAI Conference on Artificial Intelligence (AAAI 2023)*, Vol. 37, No. 12, pp. 15009–15018
- **DOI chính thức**: `10.1609/aaai.v37i12.26752`
- **Tệp PDF Cục Bộ**: **`OpenAI_2023_Undesired_Content_Detection.pdf`** (local PDF; not packaged with portal) (10 trang)
- **Liên kết mở (Open-Access PDF)**: [https://arxiv.org/pdf/2208.03274.pdf](https://arxiv.org/pdf/2208.03274.pdf) | **arXiv ID**: `2208.03274`
- **Từ khóa phân loại**: `Content Moderation`, `False Positive Rate Trade-off`, `User Experience`, `Production Guardrails`, `Threshold Calibration`
- **Đóng góp khoa học gốc của bài báo**: Đúc kết kinh nghiệm triển khai hệ thống kiểm duyệt nội dung thực tế phục vụ hàng triệu người dùng tại OpenAI, chứng minh bài toán đánh đổi cốt lõi: việc kiểm soát tỷ lệ dương tính giả (FPR) ở mức cực thấp là yếu tố quyết định sống còn đối với sự hài lòng của người dùng và tính khả dụng của ứng dụng.
- **Định vị kỹ thuật & Giả thuyết thực nghiệm của PI-Guard**: **Chương 2** & **Chương 4** — Cung cấp bài học thực tiễn để PI-Guard thiết lập yêu cầu kỹ thuật: đặt mục tiêu kiểm soát $\text{FPR} < 1.5\%$ trên tập truy vấn lành tính để không làm gián đoạn trải nghiệm người dùng thực tế.

---

### <a id="ref11"></a>[11] "Do Anything Now": Characterizing and Evaluating In-The-Wild Jailbreak Prompts on Large Language Models
- **Tên bài báo chính xác**: *"Do Anything Now": Characterizing and Evaluating In-The-Wild Jailbreak Prompts on Large Language Models*
- **Tác giả**: Xinyue Shen, Zeyuan Chen, Michael Backes, Yun Shen, Yang Zhang (CISPA Helmholtz Center for Information Security)
- **Năm xuất bản**: 2024 | **Nơi công bố chính thức**: *Proceedings of the 2024 ACM SIGSAC Conference on Computer and Communications Security (ACM CCS '24)*, pp. 4172–4186
- **DOI chính thức**: `10.1145/3658644.3670388` (ACM Paywalled DOI — Đọc bản mở qua liên kết arXiv bên dưới)
- **Tệp PDF Cục Bộ**: **`Shen_2024_Do_Anything_Now_Jailbreak_Prompts_In_The_Wild.pdf`** (local PDF; not packaged with portal) (15 trang)
- **Liên kết mở (Open-Access PDF)**: [https://arxiv.org/pdf/2308.03825.pdf](https://arxiv.org/pdf/2308.03825.pdf) | **arXiv ID**: `2308.03825`
- **Từ khóa phân loại**: `DAN Jailbreak`, `In-the-wild Prompts`, `Jailbreak Taxonomy`, `Prohibited Scenarios`, `Empirical Measurement`
- **Đóng góp khoa học gốc của bài báo**: Nghiên cứu đo lường thực nghiệm quy mô lớn đầu tiên về các prompt jailbreak xuất hiện tự nhiên trên mạng Internet (Reddit, Discord), thu thập và công bố tập dữ liệu 1,405 prompt jailbreak thực tế trên tổng số 15,140 mẫu thu thập (~9.29% / làm tròn 9.3%), phân loại thành các họ tấn công DAN kinh điển.
- **Định vị kỹ thuật & Giả thuyết thực nghiệm của PI-Guard**: **Chương 3** & **Chương 4** — Cung cấp tập dữ liệu mẫu tấn công jailbreak thực tế chất lượng cao cho quá trình huấn luyện và kiểm thử mô hình PI-Guard.

---

### <a id="ref12"></a>[12] EasyJailbreak: A Unified Framework for Jailbreaking Large Language Models
- **Tên bài báo chính xác**: *EasyJailbreak: A Unified Framework for Jailbreaking Large Language Models*
- **Tác giả**: Weikang Zhou, Xiao Wang, Limao Xiong, Han Xia, Yingshuang Gu, Mingxu Chai, Fukang Zhu, Caishuang Huang, Shihan Dou, Zhiheng Xi, Rui Zheng, Songyang Gao, Yicheng Zou, Hang Yan, Yifan Le, Ruohui Wang, Lijun Li, Jing Shao, Tao Gui, Qi Zhang, Xuanjing Huang (Fudan University, Shanghai AI Laboratory)
- **Năm xuất bản**: 2024 | **Nơi công bố chính thức**: *arXiv preprint arXiv:2403.12171* (Đã công bố mã nguồn mở trên GitHub)
- **Tệp PDF Cục Bộ**: **`Zhou_2024_EasyJailbreak_Unified_Framework.pdf`** (local PDF; not packaged with portal) (24 trang)
- **Liên kết mở (Open-Access PDF)**: [https://arxiv.org/pdf/2403.12171.pdf](https://arxiv.org/pdf/2403.12171.pdf) | **arXiv ID**: `2403.12171`
- **Từ khóa phân loại**: `EasyJailbreak`, `Mutation Framework`, `Adversarial Robustness`, `Red Teaming Automation`, `Security Evaluation`
- **Đóng góp khoa học gốc của bài báo**: Xây dựng một framework tự động hóa quy trình jailbreak toàn diện mô phỏng 4 pha (Khởi tạo, Đột biến cấu trúc/từ vựng, Đánh giá, Chọn lọc) tích hợp 11 thuật toán jailbreak hàng đầu.
- **Định vị kỹ thuật & Giả thuyết thực nghiệm của PI-Guard**: **Chương 3** & **Chương 4** — PI-Guard sử dụng các toán tử đột biến của EasyJailbreak làm công cụ kiểm thử độ bền (fuzzing), đặt mục tiêu kiểm thử độ suy giảm hiệu năng $\Delta F_1 < 5\%$ dưới các tác vụ làm nhiễu prompt.

---

### <a id="ref13"></a>[13] Universal and Transferable Adversarial Attacks on Aligned Language Models
- **Tên bài báo chính xác**: *Universal and Transferable Adversarial Attacks on Aligned Language Models*
- **Tác giả**: Andy Zou, Zifan Wang, Nicholas Carlini, Milad Nasr, J. Zico Kolter, Matt Fredrikson (CMU, Center for AI Safety, Google DeepMind)
- **Năm xuất bản**: 2023 | **Nơi công bố chính thức**: *arXiv preprint arXiv:2307.15043* (Công trình đoạt giải Outstanding Paper Award)
- **Tệp PDF Cục Bộ**: **`Zou_2023_Universal_Transferable_Adversarial_Attacks_GCG.pdf`** (local PDF; not packaged with portal) (22 trang)
- **Liên kết mở (Open-Access PDF)**: [https://arxiv.org/pdf/2307.15043.pdf](https://arxiv.org/pdf/2307.15043.pdf) | **arXiv ID**: `2307.15043`
- **Từ khóa phân loại**: `Greedy Coordinate Gradient (GCG)`, `Adversarial Suffix`, `Transferable Attacks`, `Gradient-based Optimization`
- **Đóng góp khoa học gốc của bài báo**: Phát minh thuật toán Greedy Coordinate Gradient (GCG) tự động tối ưu hóa các chuỗi token hậu tố đối kháng (adversarial suffixes) có khả năng chuyển giao vạn năng (universal transferability) bẻ gãy hàng rào căn chỉnh của hầu hết các LLM thương mại lớn.
- **Định vị kỹ thuật & Giả thuyết thực nghiệm của PI-Guard**: **Chương 4** — Sử dụng các chuỗi hậu tố GCG làm tập dữ liệu kiểm thử đối kháng ngoại lai (OOD Evaluation Set) để kiểm tra khả năng phát hiện các mẫu tấn công không dựa trên ngôn ngữ tự nhiên thông thường.

---

### <a id="ref14"></a>[14] SmoothLLM: Defending Large Language Models Against Jailbreaking Attacks
- **Tên bài báo chính xác**: *SmoothLLM: Defending Large Language Models Against Jailbreaking Attacks*
- **Tác giả**: Alexander Robey, Eric Wong, Hamed Hassani, George J. Pappas (University of Pennsylvania)
- **Năm xuất bản**: 2023 | **Nơi công bố chính thức**: *arXiv preprint arXiv:2310.03684*
- **Tệp PDF Cục Bộ**: **`Robey_2023_SmoothLLM_Defending_LLMs_Random_Perturbation.pdf`** (local PDF; not packaged with portal) (36 trang)
- **Liên kết mở (Open-Access PDF)**: [https://arxiv.org/pdf/2310.03684.pdf](https://arxiv.org/pdf/2310.03684.pdf) | **arXiv ID**: `2310.03684`
- **Từ khóa phân loại**: `SmoothLLM`, `Randomized Smoothing`, `Perturbation Defense`, `Certified Robustness`, `Inference Cost Trade-off`
- **Đóng góp khoa học gốc của bài báo**: Đề xuất giải pháp phòng thủ dựa trên cơ chế làm mịn ngẫu nhiên (Randomized Smoothing): tạo ra nhiều bản sao nhiễu của prompt đầu vào, gửi truy vấn song song tới LLM và áp dụng thuật toán biểu quyết đa số để loại bỏ các tấn công đối kháng kiểu GCG.
- **Định vị kỹ thuật & Giả thuyết thực nghiệm của PI-Guard**: **Chương 2** & **Chương 4** — Là baseline đối chuẩn so sánh. Phân tích điểm yếu làm tăng độ trễ và chi phí token lên gấp $N$ lần của SmoothLLM, làm nổi bật ưu thế suy diễn một lần (single-pass) cực nhanh của mô hình PI-Guard.

---

### <a id="ref15"></a>[15] Baseline Defenses for Adversarial Attacks Against Aligned Language Models
- **Tên bài báo chính xác**: *Baseline Defenses for Adversarial Attacks Against Aligned Language Models*
- **Tác giả**: Neel Jain, Avi Schwarzschild, Yuxin Wen, Gowthami Somepalli, John Kirchenbauer, Ping-yeh Chiang, Micah Goldblum, Aniruddha Saha, Jonas Geiping, Tom Goldstein (University of Maryland)
- **Năm xuất bản**: 2023 | **Nơi công bố chính thức**: *arXiv preprint arXiv:2309.00614*
- **Tệp PDF Cục Bộ**: **`Jain_2023_Baseline_Defenses_Adversarial_Attacks_LLMs.pdf`** (local PDF; not packaged with portal) (15 trang)
- **Liên kết mở (Open-Access PDF)**: [https://arxiv.org/pdf/2309.00614.pdf](https://arxiv.org/pdf/2309.00614.pdf) | **arXiv ID**: `2309.00614`
- **Từ khóa phân loại**: `Baseline Defenses`, `Perplexity Filter`, `Character n-grams`, `Paraphrasing`, `Input Sanitization`
- **Đóng góp khoa học gốc của bài báo**: Đánh giá một cách có hệ thống các kỹ thuật phòng thủ cơ bản (lọc Perplexity, n-grams ký tự, Paraphrasing, Retokenization) trong việc ngăn chặn các tấn công tối ưu hóa đối kháng vào LLM.
- **Định vị kỹ thuật & Giả thuyết thực nghiệm của PI-Guard**: **Chương 3** & **Chương 4** — Kế thừa ý tưởng sử dụng đặc trưng cú pháp và Character n-grams (`char_wb`) để xây dựng bộ phân loại Baseline Tầng 1 (TF-IDF + Linear Classifier) với độ trễ cực thấp (< 2ms).

---

### <a id="ref16"></a>[16] The Protection of Information in Computer Systems
- **Tên bài báo chính xác**: *The Protection of Information in Computer Systems*
- **Tác giả**: Jerome H. Saltzer, Michael D. Schroeder (Massachusetts Institute of Technology - MIT)
- **Năm xuất bản**: 1975 | **Nơi công bố chính thức**: *Proceedings of the IEEE*, Vol. 63, No. 9, pp. 1278–1308
- **DOI chính thức**: `10.1109/PROC.1975.9939`
- **Tệp PDF Cục Bộ**: **`Saltzer_1975_The_Protection_of_Information_in_Computer_Systems.pdf`** (local PDF; not packaged with portal) (31 trang)
- **Liên kết mở (Open-Access PDF)**: [http://web.mit.edu/Saltzer/www/publications/protection/index.html](http://web.mit.edu/Saltzer/www/publications/protection/index.html)
- **Từ khóa phân loại**: `Security Principles`, `Complete Mediation`, `Economy of Mechanism`, `Defense-in-Depth`, `Open Design`
- **Đóng góp khoa học gốc của bài báo**: Công trình khoa học kinh điển của ngành An toàn Thông tin thiết lập 8 nguyên lý thiết kế hệ thống bảo vệ máy tính bất hủ (Complete Mediation, Economy of Mechanism, Least Privilege, Fail-safe Defaults, Separation of Privilege, Least Common Mechanism, Psychological Acceptability, Open Design).
- **Định vị kỹ thuật & Giả thuyết thực nghiệm của PI-Guard**: **Chương 2** & **Chương 3** — Đặt nền tảng phương pháp luận cho đề tài: Lớp bảo vệ PI-Guard đóng vai trò là cơ chế *Complete Mediation* (mọi truy vấn đầu vào đều phải được thẩm định trước khi tới LLM) và kiến trúc phân tầng *Defense-in-Depth* (kết hợp lọc cú pháp nhẹ và phân tích ngữ nghĩa sâu).

---

### <a id="ref17"></a>[17] GPT-4 Is Too Smart To Be Safe: Stealthy Chat with LLMs via Cipher
- **Tên bài báo chính xác**: *GPT-4 Is Too Smart To Be Safe: Stealthy Chat with LLMs via Cipher*
- **Tác giả**: Youliang Yuan, Wenxiang Jiao, Wenxuan Wang, Jen-tse Huang, Pinjia He, Shuming Shi, Zhaopeng Tu (Tencent AI Lab, The Chinese University of Hong Kong)
- **Năm xuất bản**: 2024 | **Nơi công bố chính thức**: *The Twelfth International Conference on Learning Representations (ICLR 2024)*
- **Tệp PDF Cục Bộ**: **`Yuan_2024_GPT4_Too_Smart_To_Be_Safe_Cipher_Jailbreak.pdf`** (local PDF; not packaged with portal) (23 trang)
- **Liên kết mở (Open-Access PDF)**: [https://arxiv.org/pdf/2308.06463.pdf](https://arxiv.org/pdf/2308.06463.pdf) | **arXiv ID**: `2308.06463`
- **Từ khóa phân loại**: `CipherChat`, `Cipher Jailbreak`, `Encoding Bypass`, `Safety Alignment Failure`, `Multilingual Safety`
- **Đóng góp khoa học gốc của bài báo**: Phát hiện lỗ hổng căn chỉnh an toàn nghiêm trọng khi sử dụng các phương pháp mã hóa phi tự nhiên (mật mã Caesar, mã Morse, Base64, ROT13) khiến LLM vượt qua cơ chế từ chối trả lời nội dung nguy hại.
- **Định vị kỹ thuật & Giả thuyết thực nghiệm của PI-Guard**: **Chương 1, 3, 4** — Minh chứng cho nhu cầu bắt buộc phải có mô-đun tiền xử lý chuẩn hóa ký tự (Unicode Normalization & Heuristic Decoding) trong PI-Guard để loại bỏ các lớp ngụy trang mã hóa trước khi đưa vào phân loại ngữ nghĩa.

---

## 3. KHO TÀI LIỆU MỞ RỘNG & BENCHMARK THỰC NGHIỆM ĐÃ LƯU TRỮ (12 CÔNG TRÌNH BỔ TRỢ)

```
========================================================================================================================
DANH MỤC 12 CÔNG TRÌNH BỔ TRỢ & ĐỐI CHUẨN THỰC NGHIỆM — ĐỒ ÁN PI-GUARD (IAP491)
(100% tài liệu được lưu trữ PDF cục bộ tại Final-Report/References/ và Final-Report/References/)
========================================================================================================================
```

### 3.1. Nhóm Mô Hình Đối Chuẩn SOTA & Thực Nghiệm Tái Lập (Meeting 5 Replication Suite)

#### 1. `PIGuard (ACL 2025)`
- **Tên bài báo chính xác**: *PIGuard: Prompt Injection Guardrail via Mitigating Overdefense for Free*
- **Tác giả**: Hao Li, Xiaogeng Liu, Ning Zhang, Chaowei Xiao (Washington University in St. Louis & University of Wisconsin-Madison)
- **Venue**: *Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (ACL 2025)*, pp. 30420–30437 | **DOI**: `10.18653/v1/2025.acl-long.1468` | bản tiền xuất bản: `arXiv:2410.22770`
- **Mã nguồn & Trọng số**: `https://github.com/leolee99/PIGuard` (xác minh revision trong hồ sơ chạy; repository có thể tiến hóa sau thời điểm tái lập)
- **Tệp PDF Cục Bộ**: **`PIGuard_2025_Prompt_Injection_Guardrail_ACL.pdf`** (local PDF; not packaged with portal)
- **Bản mở toàn văn**: [ACL Anthology PDF](https://aclanthology.org/2025.acl-long.1468.pdf) | bản tiền xuất bản [arXiv:2410.22770](https://arxiv.org/pdf/2410.22770.pdf), tên cũ *InjecGuard* (được lưu riêng).
- **Đóng góp gốc (Tier 1)**: Đề xuất PIGuard, một guardrail phát hiện prompt injection dựa trên DeBERTa-v3 và chiến lược MOF; paper báo cáo kết quả trên các benchmark được mô tả, gồm mức cải thiện 30,4% theo định nghĩa paper. Không chuyển con số này sang F1 hoặc sang protocol khác.
- **Định vị kỹ thuật & Tiếp thu của đề tài (Tier 2 & 3)**: Dùng làm baseline tham chiếu. Đồ án cần báo cáo riêng inference checkpoint, huấn luyện lại từ đầu và mọi thay đổi về dữ liệu/protocol; các mục tiêu FPR/latency là giả thuyết của đồ án.

#### 2. `InstructDetector (EMNLP Findings)`
- **Tên bài báo chính xác**: *Defending against Indirect Prompt Injection by Instruction Detection*
- **Tác giả**: Tongyu Wen, Chenglong Wang, Xiyuan Yang, Haoyu Tang, Yueqi Xie, Lingjuan Lyu, Zhicheng Dou, Fangzhao Wu
- **Venue**: *Findings of the Association for Computational Linguistics: EMNLP 2025*, pp. 19472–19487 | **DOI**: `10.18653/v1/2025.findings-emnlp.1060` | **arXiv**: `2505.06311`
- **Tệp PDF Cục Bộ**: **`Wen_2025_InstructDetector_Findings_EMNLP.pdf`** (local PDF; not packaged with portal)
- **Bản mở toàn văn**: [https://arxiv.org/pdf/2505.06311.pdf](https://arxiv.org/pdf/2505.06311.pdf)
- **Đóng góp gốc (Tier 1)**: Khai thác hidden states và gradients từ các tầng của LLM instruction-tuned làm đầu vào classifier MLP để phát hiện indirect prompt injection. Phương pháp cần truy cập trạng thái bên trong mô hình.
- **Định vị kỹ thuật & Tiếp thu của đề tài (Tier 2 & 3)**: Dùng làm tài liệu tham khảo phương pháp white-box; không thể xem như guardrail proxy black-box hoặc baseline đã chạy nếu chưa có môi trường và checkpoint tương ứng.

#### 3. Prompt Guard 86M (Meta AI 2024)
- **Tên bài báo / tài liệu chính thức**: *Prompt Guard 86M: A Lightweight Input Guardrail for Jailbreak and Prompt Injection Detection* (Model Card & Technical Documentation)
- **Tác giả**: Meta AI (Purple Llama Team)
- **Venue**: *Meta AI / Purple Llama Technical Documentation & Model Card*, 2024
- **Kho lưu trữ chính thức**: [https://huggingface.co/meta-llama/Prompt-Guard-86M](https://huggingface.co/meta-llama/Prompt-Guard-86M) & [https://github.com/meta-llama/PurpleLlama/tree/main/Prompt-Guard](https://github.com/meta-llama/PurpleLlama/tree/main/Prompt-Guard)
- **Tệp PDF Cục Bộ**: **`Meta_2024_Prompt_Guard_86M_Input_Guardrail.pdf`** (local PDF; not packaged with portal)
- **Bản mở toàn văn**: [https://raw.githubusercontent.com/meta-llama/PurpleLlama/main/Prompt-Guard/MODEL_CARD.md](https://raw.githubusercontent.com/meta-llama/PurpleLlama/main/Prompt-Guard/MODEL_CARD.md)
- **Đóng góp gốc (Tier 1)**: Mô hình nhúng nhẹ 86M tham số dựa trên `mDeBERTa-v3-base` huấn luyện đa tác vụ phân loại 3 lớp: Benign, Injection, Jailbreak với độ trễ thấp trên CPU.
- **Định vị kỹ thuật & Tiếp thu của đề tài (Tier 2 & 3)**: Đóng vai trò là ứng viên mô hình tham khảo Tier 2 trong Task 2 Meeting 5; PI-Guard đối chuẩn trực tiếp về kích thước mô hình, khả năng lượng hóa và tỷ lệ dương tính giả (FPR).

#### 4. `Ayub & Majumdar (CAMLIS 2024)`
- **Tên bài báo chính xác**: *Embedding-based classifiers can detect prompt injection attacks*
- **Tác giả**: Md. Ahsan Ayub, Subhabrata Majumdar (Vanderbilt University Medical Center & Vijil)
- **Venue**: *Conference on Applied Machine Learning for Information Security (CAMLIS 2024)* | **arXiv**: `2410.22284`
- **Tệp PDF Cục Bộ**: **`Ayub_2024_Towards_Robust_Detection_Prompt_Injection_CAMLIS.pdf`** (local PDF; not packaged with portal)
- **Bản mở toàn văn**: [https://arxiv.org/pdf/2410.22284.pdf](https://arxiv.org/pdf/2410.22284.pdf)
- **Đóng góp gốc (Tier 1)**: Tạo embedding từ các encoder văn bản rồi huấn luyện classifier truyền thống; tác giả báo cáo Random Forest/XGBoost là các phương pháp mạnh trong thiết lập của họ. Đây không phải TF-IDF n-gram.
- **Định vị kỹ thuật & Tiếp thu của đề tài (Tier 2 & 3)**: Dùng làm bằng chứng rằng classifier truyền thống trên biểu diễn văn bản có thể được khảo sát; không gán kết quả FPR local hoặc kết luận cascade cho paper này.

---

### 3.2. Nhóm Lượng Hóa Mô Hình & Tối Ưu Hóa Độ Trễ

#### 5. `ZeroQuant (Yao et al., NeurIPS 2022)`
- **Tên bài báo**: *ZeroQuant: Efficient and Affordable Post-Training Quantization for Large-Scale Transformers*
- **Tác giả**: Zhewei Yao, Reza Yazdani Aminabadi, Minjia Zhang, Xiaoxia Wu, Conglong Li, Yuxiong He (Microsoft)
- **Venue**: *Advances in Neural Information Processing Systems (NeurIPS 2022)*, Vol. 35, pp. 27168–27183 | **arXiv**: `2206.01861`
- **Tệp PDF Cục Bộ**: **`Yao_2022_ZeroQuant_Efficient_Post_Training_Quantization_Transformers.pdf`** (local PDF; not packaged with portal)
- **Bản mở toàn văn**: [https://arxiv.org/pdf/2206.01861.pdf](https://arxiv.org/pdf/2206.01861.pdf)
- **Đóng góp gốc (Tier 1)**: Khung lượng hóa phần cứng hiệu năng cao cho Transformers (PTQ INT8/FP16), nén trọng số và ma trận kích hoạt với mức suy giảm độ chính xác tối thiểu (< 0.1 perplexity).
- **Định vị kỹ thuật & Tiếp thu của đề tài (Tier 2 & 3)**: ⚠️ **GHI CHÚ LOẠI TRỪ PHẠM VI (OUT-OF-SCOPE / IA DISCIPLINE INVARIANT)**: Tài liệu tham khảo ngoài phạm vi đóng góp kỹ thuật cốt lõi của đề tài. Đồ án PI-Guard thuộc chuyên ngành An toàn Thông tin (Information Assurance - IA), tập trung nghiên cứu mô hình hóa rủi ro, phân loại phát hiện tấn công Prompt Injection / Jailbreak và kiến trúc điều phối phòng thủ phân tầng (Two-Tier Cascade), KHÔNG lựa chọn hướng tối ưu hóa kỹ thuật phần cứng hay lượng tử hóa mô hình (Hardware Quantization / Low-level Inference Optimization) làm hướng đóng góp chuyên môn.

---

### 3.3. Nhóm Dữ Liệu Benchmark, Đột Biến & Khảo Sát Mở Rộng

#### 6. `BIPIA Benchmark (Yi et al., NAACL 2024)`
- **Tên bài báo**: *Benchmarking and Defending Against Indirect Prompt Injection Attacks on Large Language Models*
- **Tác giả**: Jingwei Yi, Yueqi Xie, Bin Zhu, Keegan Hines, Emre Kiciman, Anthony Zhou, Miranda Bogen, Guangzhong Sun, Xing Xie (USTC, HKUST, Microsoft Research)
- **Venue**: *Findings of NAACL 2024*, pp. 2844–2863 | **arXiv**: `2312.14197`
- **Tệp PDF Cục Bộ**: **`Viet_2024_BIPIA_Benchmarking_Indirect_Prompt_Injection_Attacks.pdf`** (local PDF; not packaged with portal)
- **Bản mở toàn văn**: [https://arxiv.org/pdf/2312.14197.pdf](https://arxiv.org/pdf/2312.14197.pdf)
- **Đóng góp gốc (Tier 1)**: Bộ dữ liệu benchmark chuẩn hóa đánh giá Indirect Prompt Injection trên 5 tác vụ ứng dụng phong phú.
- **Ứng dụng PI-Guard (Tier 2 & 3)**: Cung cấp nguồn mẫu thử gián tiếp phục vụ kiểm định tính khái quát hóa và độ bền đối kháng của bộ lọc.

#### 7. `Do-Not-Answer Dataset (Wang et al., EMNLP 2023)`
- **Tên bài báo**: *Do-Not-Answer: A Dataset for Evaluating Safeguards in LLMs*
- **Tác giả**: Yuxia Wang, Haonan Li, Xudong Han, Preslav Nakov, Timothy Baldwin (LibrAI, MBZUAI, Melbourne)
- **Venue**: *Findings of EMNLP 2023*, pp. 896–908 | **arXiv**: `2308.13387`
- **Tệp PDF Cục Bộ**: **`Phuong_2023_Do_Not_Answer_Dataset_Evaluating_Safeguards.pdf`** (local PDF; not packaged with portal)
- **Bản mở toàn văn**: [https://arxiv.org/pdf/2308.13387.pdf](https://arxiv.org/pdf/2308.13387.pdf)
- **Đóng góp gốc (Tier 1)**: 936 prompt độc hại được phân loại theo 5 lĩnh vực rủi ro và 12 loại tác hại kiểm tra độ an toàn của guardrail.
- **Ứng dụng PI-Guard (Tier 2 & 3)**: Nguồn dữ liệu kiểm thử ranh giới từ chối và hiệu chuẩn ngưỡng phát hiện nhằm giảm tỷ lệ dương tính giả (FPR).

#### 8. `JailGuard Framework (Zhang et al., TOSEM 2025)`
- **Tên bài báo**: *JailGuard: A Universal Detection Framework for Prompt-based Attacks on LLM Systems*
- **Tác giả**: Xiaoyu Zhang, Cen Zhang, Tianlin Li, Yihao Huang, Xiaojun Jia, Ming Hu, Jie Zhang (Xi'an Jiaotong, NTU Singapore, A*STAR)
- **Venue**: *ACM Transactions on Software Engineering and Methodology (TOSEM 2025)* | **DOI**: `10.1145/3724393` | **arXiv**: `2403.02582`
- **Tệp PDF Cục Bộ**: **`Duc_2025_JailGuard_Universal_Detection_Framework_TOSEM.pdf`** (local PDF; not packaged with portal)
- **Bản mở toàn văn**: [https://arxiv.org/pdf/2403.02582.pdf](https://arxiv.org/pdf/2403.02582.pdf)
- **Đóng góp gốc (Tier 1)**: Framework phát hiện jailbreak dựa trên đột biến prompt và phân tích độ phân kỳ phản hồi (behavioral divergence).
- **Ứng dụng PI-Guard (Tier 2 & 3)**: Dùng làm đối chuẩn so sánh kỹ thuật đột biến và cơ chế đánh chặn đa tầng.

#### 9. `Comprehensive Study of Jailbreak Attack vs. Defense (Xu et al., ACL 2024)`
- **Tên bài báo**: *A Comprehensive Study of Jailbreak Attack versus Defense for Large Language Models*
- **Tác giả**: Zihao Xu, Yi Liu, Gelei Deng, Yuekang Li, Stjepan Picek (NTU, UNSW, TU Delft)
- **Venue**: *Findings of ACL 2024*, pp. 7432–7449 | **DOI**: `10.18653/v1/2024.findings-acl.442` | **arXiv**: `2402.13457`
- **Tệp PDF Cục Bộ**: **`Phuong_2024_ACL_Comprehensive_Study_Jailbreak_Attack_Defense.pdf`** (local PDF; not packaged with portal)
- **Bản mở toàn văn**: [https://arxiv.org/pdf/2402.13457.pdf](https://arxiv.org/pdf/2402.13457.pdf)
- **Đóng góp gốc (Tier 1)**: Nghiên cứu thực nghiệm so sánh các chiến lược tấn công jailbreak và các cơ chế phòng thủ trên nhiều mô hình LLM.
- **Ứng dụng PI-Guard (Tier 2 & 3)**: Nguồn tài liệu tham khảo đối chuẩn taxonomy các kỹ thuật jailbreak và đánh giá hiệu quả phòng vệ.

#### 10. `Exploring Vulnerabilities and Protections in LLMs Survey (Liu & Hu, 2024)`
- **Tên bài báo**: *Exploring Vulnerabilities and Protections in Large Language Models: A Survey*
- **Tác giả**: Frank Weizhen Liu, Chenhui Hu (Zscaler, Inc.)
- **Venue**: *arXiv preprint arXiv:2403.09503* (2024)
- **Tệp PDF Cục Bộ**: **`Phuong_2024_Exploring_Vulnerabilities_Protections_LLMs_Survey.pdf`** (local PDF; not packaged with portal)
- **Bản mở toàn văn**: [https://arxiv.org/pdf/2403.09503.pdf](https://arxiv.org/pdf/2403.09503.pdf)
- **Đóng góp gốc (Tier 1)**: Khảo sát các lỗ hổng an ninh LLM từ góc nhìn ứng dụng công nghiệp và các giải pháp bảo vệ an ninh dạng Security Gateway.
- **Ứng dụng PI-Guard (Tier 2 & 3)**: Cung cấp góc nhìn thực tiễn về triển khai Ingress Proxy và kiến trúc lọc luồng trong mạng doanh nghiệp.

#### 11. `Jailbreak Attacks and Defenses Against LLMs Survey (Yi et al., 2024)`
- **Tên bài báo**: *Jailbreak Attacks and Defenses Against Large Language Models: A Survey*
- **Tác giả**: Sibo Yi, Yule Liu, Zhen Sun, Tianshuo Cong, Xinlei He, Jiaxing Song, Ke Xu, Qi Li (Tsinghua University, HKUST)
- **Venue**: *arXiv preprint arXiv:2407.04295* (2024)
- **Tệp PDF Cục Bộ**: **`Phuong_2024_Survey_Jailbreak_Attacks_Defenses_LLMs.pdf`** (local PDF; not packaged with portal)
- **Bản mở toàn văn**: [https://arxiv.org/pdf/2407.04295.pdf](https://arxiv.org/pdf/2407.04295.pdf)
- **Đóng góp gốc (Tier 1)**: Hệ thống hóa toàn diện bức tranh tấn công jailbreak và các giải pháp phòng thủ theo từng tầng (Pre-processing, Model Alignment, Post-processing).
- **Ứng dụng PI-Guard (Tier 2 & 3)**: Củng cố cơ sở lý luận cho kiến trúc phòng thủ phân tầng Ingress Proxy của PI-Guard trong Chương 2.

#### 12. `Phân Tích Loại Trừ Ngoài Phạm Vi: RAP-ID (Yang et al., ACL 2026)`
- **Tên bài báo**: *RAP-ID: Mechanistic Prompt Injection Detection via Impostor Behavior Analysis*
- **Tác giả**: Yuchen Yang, Lei Peng, Yujie He, Yang Yu, Zhongxin Wu, Yanlei Shi (Lenovo)
- **Venue**: *Findings of ACL 2026*, pp. 15008–15019
- **Tệp PDF Cục Bộ**: **`Viet_2026_RAP_ID_Robust_Alignment_Preservation_Injection_Defense.pdf`** (local PDF; not packaged with portal)
- **Đánh giá của nhóm (Tier 1 & 2)**: **XÁC ĐỊNH RÕ LÀ NGOÀI PHẠM VI (OUT-OF-SCOPE)**. Do phương pháp đòi hỏi can thiệp trực tiếp vào trọng số nội bộ và forward pass của LLM đích (white-box requirement), không phù hợp với kiến trúc External Black-Box Guardrail Proxy của đồ án PI-Guard.


#### 13. PromptShield: Deployable Detection for Prompt Injection Attacks (Jacob et al., CODASPY 2025)
- **Tên bài báo**: *PromptShield: Deployable Detection for Prompt Injection Attacks*
- **Tác giả**: Dennis Jacob, Hend Alzahrani, Zhanhao Hu, Basel Alomair, David Wagner (University of California, Berkeley & KACST)
- **Venue**: *Proceedings of the 15th ACM Conference on Data and Application Security and Privacy (CODASPY 2025)*, pp. 341–352
- **DOI / URL**: DOI: 10.1145/3714393.3726501 | Open-Access: [https://arxiv.org/pdf/2501.15145.pdf](https://arxiv.org/pdf/2501.15145.pdf)
- **Tệp PDF Cục Bộ**: **Jacob_2025_PromptShield_Deployable_Detection_CODASPY.pdf** (local PDF; not packaged with portal)
- **Nguồn thẩm quyền gốc**: ACM Digital Library (CODASPY 2025 proceedings).
- **Đóng góp gốc (Tier 1)**: Thiết lập tiêu chuẩn benchmark và khung đánh giá cho các bộ phát hiện Prompt Injection có khả năng triển khai thực tế (Deployable Detection) trong phân vùng Tỷ lệ Báo động Giả cực thấp (**Low-FPR Regime**:  \le 1\%, 0.5\%, 0.1\%, 0.05\%$). Lập luận rằng ROC-AUC không phản ánh đầy đủ chất lượng detector trong vùng FPR thấp; xây dựng bộ dữ liệu PromptShield kết hợp hội thoại tự nhiên và cấu trúc ứng dụng; đề xuất kỹ thuật nội suy ngưỡng quyết định động trên ROC. Cung cấp bảng đối chuẩn thực nghiệm độc lập chỉ ra Meta PromptGuard chỉ đạt TPR 12.78% tại FPR 1% và ProtectAI v2 chỉ đạt TPR 1.97% tại FPR 1%.
- **Định vị kỹ thuật & Tiếp thu của PI-Guard (Tier 2)**: PI-Guard tiếp thu triết lý đánh giá Low-FPR của nhóm tác giả David Wagner (UC Berkeley), áp dụng kỹ thuật nội suy ngưỡng trên ROC để hiệu chuẩn ngưỡng định tuyến ba trạng thái (Tri-State Decision Engine) của Tầng 1 và Tầng 2, đảm bảo hệ thống chặn nhầm  < 1.5\%$ trước khi chuyển giao prompt đến LLM đích.
- **Mục tiêu kỹ thuật & Giả thuyết của PI-Guard (Tier 3)**: PI-Guard đặt mục tiêu đạt TPR $\ge 90\%$ tại mức FPR $\le 1.5\%$ với độ trễ suy diễn P95 $< 30\text{ms}$ trên CPU bằng kiến trúc ghép tầng (Two-Tier Cascade: Fast Syntactic Filter + Semantic Transformer).

#### 14. Bypassing LLM Guardrails: An Empirical Analysis of Evasion Attacks (Hackett et al., ACL 2025 LLMSEC)
- **Tên bài báo**: *Bypassing LLM Guardrails: An Empirical Analysis of Evasion Attacks against Prompt Injection and Jailbreak Detection Systems*
- **Tác giả**: William Hackett, Lewis Birch, Stefan Trawicki, Neeraj Suri, Peter Garraghan (Mindgard & Lancaster University)
- **Venue**: *Proceedings of The First Workshop on LLM Security (LLMSEC 2025) at ACL 2025*, pages 101–114, August 2025
- **DOI / URL**: DOI: 10.48550/arXiv.2504.11168 | Open-Access: [https://arxiv.org/pdf/2504.11168.pdf](https://arxiv.org/pdf/2504.11168.pdf) | [ACL Anthology](https://aclanthology.org/2025.llmsec-1.9/)
- **Tệp PDF Cục Bộ**: **Hackett_2025_Bypassing_LLM_Guardrails_Evasion_Attacks.pdf** (local PDF; not packaged with portal)
- **Nguồn thẩm quyền gốc**: ACL Anthology / Workshop on LLM Security.
- **Đóng góp gốc (Tier 1)**: Đánh giá thực nghiệm toàn diện các đòn tấn công né tránh (Evasion Attacks) trên 6 hệ thống guardrail thương mại và mã nguồn mở (Azure Prompt Shield, Meta Prompt Guard 86M, ProtectAI v1 & v2, Nvidia NeMo Guard, Vijil). Khảo sát 12 kỹ thuật chèn ký tự (Emoji Smuggling, Unicode Tags, Zero-Width, Homoglyphs, Leetspeak) và 8 thuật toán AML Evasion (TextFooler, BAE, Bert-Attack, Deep Word Bug, Alzantot, PWWS, Pruthi, TextBugger). Chứng minh tỷ lệ qua mặt lên tới 100% đối với Emoji Smuggling trên cả Meta Prompt Guard và Azure Prompt Shield; chứng minh hiện tượng chuyển giao tấn công hộp đen (Transferability) từ mô hình white-box sang black-box.
- **Định vị kỹ thuật & Tiếp thu của PI-Guard (Tier 2)**: PI-Guard tiếp thu phát hiện cốt lõi về việc các mô hình dựa trên subword tokenizer bị mù trước biến dị Unicode/Emoji. Từ đó, PI-Guard chính thức thiết kế lớp tiền xử lý Heuristic Scrubber (Tầng 0) kết hợp bộ trích xuất đặc trưng Character N-Grams TF-IDF ở Tầng 1 để bắt dính các đòn biến dị ký tự trước khi đẩy vào Transformer.
- **Mục tiêu kỹ thuật & Giả thuyết của PI-Guard (Tier 3)**: PI-Guard giả định rằng sự phối hợp giữa Heuristic Scrubber + Char N-Grams (Tầng 1) và DeBERTa-v3 MOF (Tầng 2) sẽ giảm tỷ lệ tấn công né tránh thành công (ASR) của các đòn biến dị ký tự xuống $< 5\%$, triệt tiêu lỗ hổng 100% bypass của Meta Prompt Guard.

#### 15. DataSentinel: A Game-Theoretic Detection of Prompt Injection Attacks (Liu et al., IEEE S&P 2025)
- **Tên bài báo**: *DataSentinel: A Game-Theoretic Detection of Prompt Injection Attacks*
- **Tác giả**: Yupei Liu, Yuqi Jia, Jinyuan Jia, Dawn Song, Neil Zhenqiang Gong (The Pennsylvania State University, Duke University, UC Berkeley)
- **Venue**: *Proceedings of the 2025 IEEE Symposium on Security and Privacy (SP '25)*, May 2025
- **DOI / URL**: DOI: 10.1109/SP61157.2025.00250 | [Open-Prompt-Injection Code](https://github.com/liu00222/Open-Prompt-Injection)
- **Tệp PDF Cục Bộ**: **Liu_2025_DataSentinel_Game_Theoretic_Detection_Prompt_Injection.pdf** (local PDF; not packaged with portal)
- **Nguồn thẩm quyền gốc**: IEEE Computer Society / IEEE S&P 2025.
- **Đóng góp gốc (Tier 1)**: Đề xuất phương pháp tiếp cận lý thuyết trò chơi Minimax để phát hiện tấn công Prompt Injection thích ứng (Adaptive Prompt Injection). Xây dựng bài toán tối ưu hóa Minimax mô phỏng trò chơi giữa kẻ tấn công thích ứng (Inner Max) và bộ phát hiện (Outer Min). Giải bài toán bằng giải thuật gradient luân phiên. Công bố bộ công cụ và benchmark Open-Prompt-Injection trên 7 nhóm tác vụ tích hợp LLM.
- **Định vị kỹ thuật & Tiếp thu của PI-Guard (Tier 2)**: PI-Guard tiếp thu cơ sở lý thuyết trò chơi Minimax của Liu et al. để mô hình hóa ranh giới an toàn đối kháng giữa Prompt Ingress và Guardrail Proxy, đồng thời tái sử dụng tập benchmark Open-Prompt-Injection làm nguồn dữ liệu kiểm thử OOD (Out-of-Distribution).
- **Mục tiêu kỹ thuật & Giả thuyết của PI-Guard (Tier 3)**: Khác với DataSentinel đòi hỏi suy diễn bằng LLM lớn (Mistral-7B, tiêu tốn tài nguyên và độ trễ cao), PI-Guard kế thừa tinh thần huấn luyện đối kháng nhưng triển khai trên kiến trúc phân loại gọn nhẹ (DeBERTa-v3 + TF-IDF) nhằm đạt mục tiêu P95 $< 30\text{ms}$ trên CPU.

#### 16. The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions (Wallace et al., OpenAI 2024 / ICLR 2025)
- **Tên bài báo**: *The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions*
- **Tác giả**: Eric Wallace, Kai Xiao, Reimar Leike, Lilian Weng, Johannes Heidecke, Alex Beutel (OpenAI)
- **Venue**: *arXiv preprint arXiv:2404.13208* (2024) | Submitted to ICLR 2025 / NeurIPS 2024 cycle
- **DOI / URL**: [https://arxiv.org/abs/2404.13208](https://arxiv.org/abs/2404.13208) | Open-Access PDF: [https://arxiv.org/pdf/2404.13208.pdf](https://arxiv.org/pdf/2404.13208.pdf)
- **Tệp PDF Cục Bộ**: **Wallace_2024_Instruction_Hierarchy_Prioritize_Privileged_Instructions.pdf** (local PDF; not packaged with portal)
- **Nguồn thẩm quyền gốc**: OpenAI Technical Research / arXiv.
- **Đóng góp gốc (Tier 1)**: Hình thức hóa bài toán gốc rễ của Prompt Injection: LLM xử lý mọi chỉ thị (System Prompt, User Input, Tool Context) với quyền hạn ngang hàng. Đề xuất mô hình phân tầng quyền hạn *System > User > Tool/Data*, sử dụng dữ liệu đối kháng để huấn luyện mô hình bỏ qua chỉ thị quyền thấp khi có xung đột. Thừa nhận in-model training không thể chống lại hoàn toàn tấn công đối kháng thích ứng và làm tăng tỷ lệ từ chối quá mức (over-refusal).
- **Định vị kỹ thuật & Tiếp thu của PI-Guard (Tier 2)**: Cung cấp luận cứ khoa học then chốt chứng minh tại sao căn chỉnh nội tại trong LLM là không đủ; xác lập tính tất yếu của giải pháp Ingress Guardrail Proxy độc lập (PI-Guard) đặt bên ngoài nhằm bảo vệ mô hình theo nguyên lý Defense-in-Depth.
- **Mục tiêu kỹ thuật & Giả thuyết của PI-Guard (Tier 3)**: PI-Guard kết hợp với downstream LLM tạo nên kiến trúc phân tầng an ninh, kỳ vọng giảm thiểu over-refusal trên truy vấn an toàn và đạt tỷ lệ ngăn chặn tấn công $> 98\%$.

#### 17. JailbreakBench: An Open Robustness Benchmark for Jailbreaking Large Language Models (Chao et al., NeurIPS 2024)
- **Tên bài báo**: *JailbreakBench: An Open Robustness Benchmark for Jailbreaking Large Language Models*
- **Tác giả**: Patrick Chao, Edoardo Debenedetti, Alexander Robey, Maksym Andriushchenko, Francesco Croce, Vikash Sehwag, Edgar Dobriban, Nicolas Papernot, George J. Pappas, Florian Tramèr (UPenn, EPFL, University of Toronto, Vector Institute, ETH Zurich)
- **Venue**: *Advances in Neural Information Processing Systems 37 (NeurIPS 2024)*, Datasets and Benchmarks Track
- **DOI / URL**: [https://arxiv.org/abs/2404.01318](https://arxiv.org/abs/2404.01318) | Open-Access PDF: [https://arxiv.org/pdf/2404.01318.pdf](https://arxiv.org/pdf/2404.01318.pdf) | [GitHub](https://github.com/JailbreakBench/jailbreakbench)
- **Tệp PDF Cục Bộ**: **Chao_2024_JailbreakBench_Open_Robustness_Benchmark_NeurIPS.pdf** (local PDF; not packaged with portal)
- **Nguồn thẩm quyền gốc**: NeurIPS 2024 Official Proceedings (Datasets & Benchmarks Track).
- **Đóng góp gốc (Tier 1)**: Xây dựng chuẩn benchmark mở và nhất quán đầu tiên cho jailbreaking trên LLM; công bố tập dữ liệu chuẩn JBB-Behaviors gồm 100 hành vi vi phạm an toàn; cung cấp leaderboard theo dõi các phương pháp tấn công và phòng thủ SOTA.
- **Định vị kỹ thuật & Tiếp thu của PI-Guard (Tier 2)**: PI-Guard tích hợp bộ 100 hành vi JBB-Behaviors vào quy trình kiểm thử đối chuẩn thực nghiệm, đối sánh trực tiếp với các giải pháp phòng thủ hàng đầu trên bảng xếp hạng cộng đồng.
- **Mục tiêu kỹ thuật & Giả thuyết của PI-Guard (Tier 3)**: PI-Guard đặt mục tiêu đạt độ bao phủ phát hiện (Recall) $\ge 95\%$ trên tập JBB-Behaviors dưới cả prompt gốc và biến thể đối kháng.

#### 18. Multilingual Jailbreak Challenges in Large Language Models (Deng et al., ICLR 2024)
- **Tên bài báo**: *Multilingual Jailbreak Challenges in Large Language Models*
- **Tác giả**: Yue Deng, Wenxuan Zhang, Sinno Jialin Pan, Lidong Bing (DAMO Academy, Alibaba Group, NTU Singapore)
- **Venue**: *The Twelfth International Conference on Learning Representations (ICLR 2024)*
- **DOI / URL**: [https://arxiv.org/abs/2310.06474](https://arxiv.org/abs/2310.06474) | Open-Access PDF: [https://arxiv.org/pdf/2310.06474.pdf](https://arxiv.org/pdf/2310.06474.pdf)
- **Tệp PDF Cục Bộ**: **Deng_2024_Multilingual_Jailbreak_Challenges_LLMs_ICLR.pdf** (local PDF; not packaged with portal)
- **Nguồn thẩm quyền gốc**: ICLR 2024 Conference Proceedings.
- **Đóng góp gốc (Tier 1)**: MultiJail có 315 prompt tiếng Anh và bản dịch tương ứng sang chín ngôn ngữ khác (3.150 prompt). Paper đo phản hồi jailbreak của LLM; tập này không phải benchmark phân loại prompt injection.
- **Định vị kỹ thuật & Tiếp thu của PI-Guard (Tier 2)**: Có thể tham khảo để thiết kế đánh giá jailbreak đa ngôn ngữ; kết quả không chứng minh bộ phân loại PI-Guard hoạt động trên tiếng Việt, và bản dịch cần được kiểm định nhãn trước khi dùng.
- **Mục tiêu kỹ thuật & Giả thuyết của PI-Guard (Tier 3)**: PI-Guard giả định rằng bộ lọc Tầng 1 (Character n-grams) kết hợp tiền xử lý chuẩn hóa duy trì mức suy giảm hiệu năng $\Delta F_1 < 5\%$ khi chuyển giao sang tập tấn công dịch thuật tiếng Việt.

#### 19. Conformal Risk Control & Certified Safe LLM Generation (Angelopoulos et al. 2024 / Kang et al., NeurIPS 2025)
- **Tên bài báo**: *Conformal Risk Control* & *C-SafeGen: Certified Safe LLM Generation with Claim-Based Streaming Guardrails*
- **Tác giả**: Anastasios N. Angelopoulos, Stephen Bates, Emmanuel J. Candès, Michael I. Jordan, Lihua Lei (Harvard, UC Berkeley, Stanford) & Mintong Kang, Zhaorun Chen, Bo Li (UIUC)
- **Venue**: *arXiv:2208.02814* (Angelopoulos et al., 2024) / *Advances in Neural Information Processing Systems (NeurIPS 2025)* (Kang et al.)
- **DOI / URL**: [https://arxiv.org/abs/2208.02814](https://arxiv.org/abs/2208.02814) | Open-Access PDF: [https://arxiv.org/pdf/2208.02814.pdf](https://arxiv.org/pdf/2208.02814.pdf)
- **Tệp PDF Cục Bộ**: **Angelopoulos_2024_Conformal_Risk_Control.pdf** (local PDF; not packaged with portal)
- **Nguồn thẩm quyền gốc**: arXiv / NeurIPS 2025 Proceedings.
- **Đóng góp gốc (Tier 1)**: Đề xuất Conformal Risk Control để giới hạn rủi ro kỳ vọng với các giả định và loss function được nêu trong bài. Kết quả không tự động tạo ra bảo đảm FPR cho classifier PI-Guard.
- **Định vị kỹ thuật & Tiếp thu của PI-Guard (Tier 2)**: Có thể khảo sát CRC sau khi xác định loss, dữ liệu calibration và giả định; chưa có bảo chứng FPR 1,5% cho hệ thống của đồ án.
- **Mục tiêu kỹ thuật & Giả thuyết của PI-Guard (Tier 3)**: Mọi tuyên bố FPR/độ tin cậy phải dựa trên một phép hiệu chuẩn và protocol kiểm định riêng của đồ án.

---

### 37. ModernBERT: Bringing Modern Transformer Innovations to Pre-trained Encoders (Warner et al., Answer.AI / LightOn 2024)
- **Tên bài báo**: *ModernBERT: Bringing Modern Transformer Innovations to Pre-trained Encoders*
- **Tác giả**: Benjamin Warner, Antoine Chaffin, Benjamin Clavié, Orion Weller, Oskar Hallström, Shraddha Vasanth, Nikhil Patry, Colin Raffel, Luke Zettlemoyer
- **Venue**: *arXiv preprint arXiv:2412.13663* (2024)
- **DOI / URL**: [https://arxiv.org/abs/2412.13663](https://arxiv.org/abs/2412.13663) | Open-Access PDF: [https://arxiv.org/pdf/2412.13663.pdf](https://arxiv.org/pdf/2412.13663.pdf)
- **Tệp PDF Cục Bộ**: **Warner_2024_ModernBERT_Brings_Modern_Transformers_To_Encoders.pdf** (local PDF; not packaged with portal)
- **Nguồn thẩm quyền gốc**: arXiv / Answer.AI & LightOn Technical Report.
- **Đóng góp gốc (Tier 1)**: Hiện đại hóa encoder với các thay đổi kiến trúc và pretraining; hỗ trợ context 8.192 token. Các kết quả throughput trong paper gắn với tác vụ/phần cứng/thiết lập cụ thể, không phải phép đo trực tiếp so với DeBERTa-v3 trong hệ thống PI-Guard.
- **Định vị kỹ thuật & Tiếp thu của PI-Guard (Tier 2)**: Có thể chọn làm backbone ứng viên sau fine-tuning và đánh giá cùng protocol; cửa sổ dài hơn không tự khắc phục mọi kiểu cắt cụt hay chứng minh hiệu quả phân loại guardrail.
- **Mục tiêu kỹ thuật & Giả thuyết của PI-Guard (Tier 3)**: Đạt độ trễ P95 < 18ms trên CPU với ngữ cảnh 512 tokens và duy trì F1 > 0.92 trong việc phân loại Benign vs. Prompt Injection vs. Jailbreak.

---

### 38. Granite Guardian: A Family of Open Models for Content Safety and Risk Detection (Padhi et al., IBM Research 2024)
- **Tên bài báo**: *Granite Guardian: A Family of Open Models for Content Safety and Risk Detection*
- **Tác giả**: Inkit Padhi, Manish Nagireddy, Giandomenico Cornacchia, Subhro Das, Tejaswini Pedapati, Hima Patel, et al. (IBM Research)
- **Venue**: *arXiv preprint arXiv:2412.07724* (2024)
- **DOI / URL**: [https://arxiv.org/abs/2412.07724](https://arxiv.org/abs/2412.07724) | Open-Access PDF: [https://arxiv.org/pdf/2412.07724.pdf](https://arxiv.org/pdf/2412.07724.pdf)
- **Tệp PDF Cục Bộ**: **Padhi_2024_Granite_Guardian_Content_Safety_Risk_Detection.pdf** (local PDF; not packaged with portal)
- **Nguồn thẩm quyền gốc**: arXiv / IBM Research Technical Report.
- **Đóng góp gốc (Tier 1)**: Thiết kế và huấn luyện dòng mô hình an toàn chuyên biệt (2B và 8B) dựa trên Granite, bao phủ toàn diện các rủi ro: Jailbreak, Direct/Indirect Prompt Injection, Context Relevance, Groundedness và Answer Relevance. Cung cấp cả nhãn rủi ro nhị phân và giải thích nguyên nhân rủi ro.
- **Định vị kỹ thuật & Tiếp thu của PI-Guard (Tier 2)**: Cung cấp bằng chứng thực nghiệm và cơ sở đối chuẩn cho phân tầng SLM Guardrail (Thế hệ 1) tại Tier 3 (High-Assurance Arbiter), hỗ trợ phân xử các prompt có độ bất định cao.
- **Mục tiêu kỹ thuật & Giả thuyết của PI-Guard (Tier 3)**: Sử dụng phiên bản lượng tử hóa INT4 của mô hình 2B làm trọng tài thẩm định sâu với độ trễ P95 < 120ms trên CPU.

---

### 39. Great, Now Write an Article About That: The Crescendo Multi-Turn LLM Jailbreak Attack (Russinovich et al., Microsoft Research 2024)
- **Tên bài báo**: *Great, Now Write an Article About That: The Crescendo Multi-Turn LLM Jailbreak Attack*
- **Tác giả**: Mark Russinovich, Ahmed Salem, Ronen Eldan (Microsoft Research & Azure)
- **Venue**: *arXiv preprint arXiv:2404.01833* (2024)
- **DOI / URL**: [https://arxiv.org/abs/2404.01833](https://arxiv.org/abs/2404.01833) | Open-Access PDF: [https://arxiv.org/pdf/2404.01833.pdf](https://arxiv.org/pdf/2404.01833.pdf)
- **Tệp PDF Cục Bộ**: **Russinovich_2024_Crescendo_MultiTurn_Jailbreak_Attack.pdf** (local PDF; not packaged with portal)
- **Nguồn thẩm quyền gốc**: Microsoft Research Technical Report / arXiv.
- **Đóng góp gốc (Tier 1)**: Phát hiện và hình thức hóa kỹ thuật tấn công đa lượt Crescendo: kẻ tấn công bắt đầu bằng các câu hỏi hoàn toàn vô hại, sau đó từng bước hướng dẫn LLM tạo ra các khối nội dung nhỏ và cuối cùng kết hợp thành mã độc hoặc vũ khí nguy hại. Bài báo chứng minh tỷ lệ thành công của Crescendo đạt trên 80% trên GPT-4, Claude 3, Llama-2-70B và Gemini Pro, đồng thời làm tê liệt hoàn toàn mọi bộ lọc Ingress đơn lượt.
- **Định vị kỹ thuật & Tiếp thu của PI-Guard (Tier 2)**: Luận chứng mang tính nền tảng cho việc mở rộng PI-Guard ra ngoài giới hạn đơn lượt của Low-Latency: chấp nhận đánh đổi thêm ~15–25ms độ trễ để duy trì bộ nhớ phiên (Session Sliding Window) và tính toán độ trôi dạt ngữ nghĩa (Semantic Drift Trajectory).
- **Mục tiêu kỹ thuật & Giả thuyết của PI-Guard (Tier 3)**: Thiết kế mô-đun `MultiTurnCrescendoGuardrail` có khả năng chặn các đợt tấn công leo thang đa lượt với tỷ lệ phát hiện > 85% sau 3-5 lượt hội thoại.

---

### 40. Prompt Overflow: What the Guardrail Inspects Is Not What the Model Infers (Zhou et al., 2026)
- **Tên bài báo**: *Prompt Overflow: What the Guardrail Inspects Is Not What the Model Infers*
- **Tác giả**: Yuanbo Zhou, Changjia Zhu, Junyu Wang, Xu He, Yan Zhai, Kun Sun, Mingkui Wei, Junjie Xiong (Missouri S&T, University of South Florida, Visa Inc., George Mason University)
- **Venue**: *arXiv preprint arXiv:2605.23196* (2026)
- **DOI / URL**: [https://arxiv.org/abs/2605.23196](https://arxiv.org/abs/2605.23196) | Open-Access PDF: [https://arxiv.org/pdf/2605.23196.pdf](https://arxiv.org/pdf/2605.23196.pdf)
- **Tệp PDF Cục Bộ**: **Zhou_2026_Prompt_Overflow_Guardrail_Window_Mismatch.pdf** (local PDF; not packaged with portal)
- **Nguồn thẩm quyền gốc**: arXiv preprint / Academic Research.
- **Đóng góp gốc (Tier 1)**: Preprint nghiên cứu chênh lệch giữa nội dung guardrail kiểm tra và phần nội dung LLM đích xử lý trong các cấu hình được đánh giá; không khái quát rằng mọi guardrail dùng 512 token hay mọi LLM nhận 128k token.
- **Định vị kỹ thuật & Tiếp thu của PI-Guard (Tier 2)**: Gợi ý kiểm thử nội dung dài và vị trí payload; không chứng minh thiết kế chunking hay độ phủ 200.000 ký tự của PI-Guard.
- **Mục tiêu kỹ thuật & Giả thuyết của PI-Guard (Tier 3)**: Phải kiểm tra độ phủ tài liệu dài và vị trí payload bằng đánh giá riêng; chưa có kết quả hoặc bảo đảm này trong đồ án.

---

### 41. CASCADE Against Jailbreaks: Combination Across Stages with Controlled Attack-Defense Evaluation (Luo & Han, 2026)
- **Tên bài báo**: *CASCADE Against Jailbreaks: Combination Across Stages with Controlled Attack-Defense Evaluation*
- **Tác giả**: Jiale Luo, Eric Han (School of Computing, National University of Singapore)
- **Venue**: *arXiv preprint arXiv:2609.21793* (2026)
- **DOI / URL**: [https://arxiv.org/abs/2609.21793](https://arxiv.org/abs/2609.21793) | Open-Access PDF: [https://arxiv.org/pdf/2609.21793.pdf](https://arxiv.org/pdf/2609.21793.pdf)
- **Tệp PDF Cục Bộ**: **Luo_2026_CASCADE_Against_Jailbreaks_Evaluation.pdf** (local PDF; not packaged with portal)
- **Nguồn thẩm quyền gốc**: arXiv preprint / NUS Computing Technical Report.
- **Đóng góp gốc (Tier 1)**: Preprint báo cáo đánh giá thực nghiệm các tổ hợp phòng thủ qua nhiều kỹ thuật tấn công và cơ chế phòng thủ được nêu; kết luận thực nghiệm bị giới hạn bởi thiết lập nghiên cứu, không phải định lý tổng quát.
- **Định vị kỹ thuật & Tiếp thu của PI-Guard (Tier 2)**: Có thể dùng làm điểm đối chiếu khi đánh giá tổ hợp phòng thủ; paper không kiểm định hoặc bảo chứng cascade cụ thể của đồ án.
- **Mục tiêu kỹ thuật & Giả thuyết của PI-Guard (Tier 3)**: Đạt điểm cân bằng Pareto tối ưu trên CPU (P95 Latency < 30ms, FPR < 1.5%, F1 > 0.95), giải phóng trên 80% lưu lượng tại Tầng 1 và chỉ chuyển tiếp dưới 20% truy vấn bất định lên Tầng 2.

---

### <a id="ref44"></a>[44] PIDS-Bench: Evaluating Prompt-Injection Detectors Under Over-Defense, Obfuscation, and Distribution Shift
- **Tên bài báo**: *PIDS-Bench: Evaluating Prompt-Injection Detectors Under Over-Defense, Obfuscation, and Distribution Shift*
- **Tác giả**: Yusuf Khalid Shire, Sang-Chul Kim
- **Venue**: *IEEE Access*, vol. 14, pp. 134184–134205 (2026)
- **DOI / URL**: [10.1109/ACCESS.2026.3728186](https://doi.org/10.1109/ACCESS.2026.3728186) | [arXiv:2609.15017](https://arxiv.org/abs/2609.15017)
- **Tệp PDF cục bộ**: **PIDS_Bench_2026_arXiv2609.15017v1.pdf** — bản arXiv v1; tiêu đề trùng với tiêu đề bài IEEE Access.
- **Nguồn thẩm quyền gốc**: IEEE Xplore DOI page; arXiv record/PDF for the locally archived version.
- **Đóng góp gốc (Tier 1)**: Đề xuất benchmark nhị phân đa trục để đánh giá detector prompt injection trên test IID, hard-benign, obfuscation, domain shift và structural shift. Mục này chỉ mô tả đóng góp của paper; không công bố metric từ các lượt chạy cục bộ.
- **Định vị kỹ thuật & Tiếp thu của PI-Guard (Tier 2)**: Dùng các baseline paper và bộ dữ liệu để tham khảo/đối chiếu nhị phân Benign–Injection; không diễn giải các nhãn attack subtype thành lớp Jailbreak của PI-Guard.
- **Mục tiêu kỹ thuật & Giả thuyết của PI-Guard (Tier 3)**: Kết quả này không đo cascade PI-Guard, latency P95 hay khả năng phân lớp ba nhãn.

### <a id="ref45"></a>[45] PIDS-Bench v3 — pinned author code and dataset release
- **Tác giả / Chủ sở hữu**: Yusuf Khalid Shire, Sang-Chul Kim / ShirePyDev
- **Nguồn**: [Repository tag `v1.0-pids-bench`](https://github.com/ShirePyDev/Prompt-Injection-Detection-System/tree/v1.0-pids-bench), commit `87dc835566b930ee921240874a4939b2c266c2fe`
- **Bản sao mã nguồn/dữ liệu cục bộ**: được giữ trong workspace cá nhân và không nằm trong repository này; tham chiếu dữ liệu theo nguồn gốc và điều khoản tại upstream.
- **Giấy phép / giới hạn**: Mã nguồn MIT; dữ liệu giữ điều khoản của nguồn gốc và được đánh dấu research/non-commercial trong `DATA_LICENSES.md`. Văn bản LMSYS bị loại bỏ khỏi bản phát hành và các dòng rỗng đó không được thay bằng văn bản tổng hợp.

### <a id="ref46"></a>[46] ProtectAI DeBERTa-v3 prompt-injection model card
- **Mô hình / phiên bản**: `protectai/deberta-v3-base-prompt-injection-v2`, revision `90c9989b1a342275dd0d1a95aad283c04e075671`.
- **Nguồn thẩm quyền**: [Hugging Face model card at the pinned revision](https://huggingface.co/protectai/deberta-v3-base-prompt-injection-v2/tree/90c9989b1a342275dd0d1a95aad283c04e075671).
- **Bản sao model card cục bộ**: thuộc workspace cá nhân và không nằm trong repository này; dùng model card công khai ở trên làm nguồn.
- **Thông tin dùng trong báo cáo**: ProtectAI fine-tuned checkpoint này cho nhiệm vụ benign/injection tiếng Anh; đây là checkpoint có sẵn được chạy inference, không phải DeBERTa được nhóm fine-tune trên PIDS-Bench.

### <a id="ref47"></a>[47] Hồ sơ metric thực nghiệm cục bộ — không phát hành trong repository
- Hồ sơ, model và row-level predictions thuộc workspace cá nhân đã loại khỏi repository.
- Tài liệu này không công bố metric thực nghiệm cục bộ hoặc dùng hồ sơ đó làm bằng chứng dùng chung.

### <a id="ref48"></a>[48] DeepSet DeBERTa prompt-injection checkpoint — model card
- **Model/revision**: deepset/deberta-v3-base-injection, revision 80dda00d0b0d9a03917a7685e2ddbcd28e04dbb1.
- **Nguồn công khai**: [Hugging Face model card](https://huggingface.co/deepset/deberta-v3-base-injection/tree/80dda00d0b0d9a03917a7685e2ddbcd28e04dbb1).
- **Giới hạn audit**: model card mô tả checkpoint fine-tuned và dữ liệu, nhưng không xác định một paper và repository huấn luyện của chính checkpoint này.

### <a id="ref49"></a>[49] FMOPS DistilBERT prompt-injection checkpoint — model card
- **Model/revision**: fmops/distilbert-prompt-injection, revision c5da1fefd33c98c447b50dd806fe86aeb9e8c26c.
- **Nguồn công khai**: [Hugging Face model card](https://huggingface.co/fmops/distilbert-prompt-injection/tree/c5da1fefd33c98c447b50dd806fe86aeb9e8c26c).
- **Giới hạn audit**: model card không nêu paper gốc hoặc repository huấn luyện khớp với checkpoint.

### <a id="ref50"></a>[50] Injection Sentry DeBERTa-v2 component — model card and code
- **Model/revision**: Verm1ion/injection-sentry-deberta-v2, revision 956b7e581e08615c824abbc877cb6461fcd8fa28.
- **Nguồn công khai**: [Hugging Face model card](https://huggingface.co/Verm1ion/injection-sentry-deberta-v2/tree/956b7e581e08615c824abbc877cb6461fcd8fa28); [public code repository](https://github.com/Verm1lion/InjectionSentry).
- **Giới hạn audit**: citation trên model card trỏ tới một GitHub pull request; đây chưa phải paper nghiên cứu gốc cho checkpoint.

### <a id="ref51"></a>[51] Wolf Defender Small prompt-injection checkpoint — model card
- **Model/revision**: patronus-studio/wolf-defender-prompt-injection-small, revision bcab2eff97bcabd7227849639e2d0d7a61b46c92.
- **Nguồn công khai**: [Hugging Face model card](https://huggingface.co/patronus-studio/wolf-defender-prompt-injection-small/tree/bcab2eff97bcabd7227849639e2d0d7a61b46c92); [Patronus release post](https://patronus.studio/en/posts/today-we%E2%80%99re-releasing-our-first-security-model-wolf-defender).
- **Giới hạn audit**: card trích dẫn chính card đó và mô tả dữ liệu tạo/tăng cường nội bộ; audit chưa xác minh paper nghiên cứu và repository huấn luyện của checkpoint.

### <a id="ref52"></a>[52] PromptShield: Deployable Detection for Prompt Injection Attacks — paper and author code
- **Bài báo**: Dennis Jacob et al., CODASPY 2025, arXiv:2501.15145, [open-access paper](https://arxiv.org/abs/2501.15145).
- **Mã nguồn tác giả**: [wagner-group/PromptShield](https://github.com/wagner-group/PromptShield).
- **Ghi chú định danh**: tên thư mục cũ ghi CCS2024 không khớp venue/năm của bài báo.

### <a id="ref53"></a>[53] DataSentinel — paper and author code
- **Bài báo**: Yupei Liu et al., *DataSentinel: A Game-Theoretic Detection of Prompt Injection Attacks*, IEEE S&P 2025, [arXiv:2504.11358](https://arxiv.org/abs/2504.11358).
- **Mã nguồn tác giả**: [liu00222/Open-Prompt-Injection](https://github.com/liu00222/Open-Prompt-Injection).
- **Ranh giới bằng chứng**: nguồn này xác minh paper/repo; không xác minh adapter heuristic cục bộ là implementation của DataSentinel.

### <a id="ref54"></a>[54] ProtectAI prompt-injection scanner — official implementation documentation
- **Nguồn**: [ProtectAI LLM Guard prompt-injection scanner](https://github.com/protectai/llm-guard/blob/main/docs/input_scanners/prompt_injection.md).
- **Ghi chú định danh**: tài liệu trỏ tới checkpoint ProtectAI và mô tả inference integration; không phải paper gốc của fine-tuned checkpoint.

### <a id="ref55"></a>[55] Jain et al. Baseline Defenses — official code repository
- **Bài báo tương ứng**: Jain et al. (2023), *Baseline Defenses for Adversarial Attacks Against Aligned Language Models*, [arXiv:2309.00614](https://arxiv.org/abs/2309.00614).
- **Mã nguồn tác giả**: [neelsjain/baseline-defenses](https://github.com/neelsjain/baseline-defenses).
- **Ranh giới bằng chứng**: paper/repository này không phải nguồn gốc của local TF-IDF classifier đã bị rút khỏi bộ bằng chứng.
---

### <a id="ref56"></a>[56] Hồ sơ so sánh mô hình PIDS-Bench cục bộ — không phát hành trong repository
- Báo cáo, protocol, checkpoint, manifests và các artifact phát sinh thuộc workspace cá nhân đã loại khỏi repository.
- Không công bố trạng thái huấn luyện hoặc kết quả đánh giá cục bộ trong tài liệu tham khảo dùng chung. Kết quả do paper công bố vẫn được trình bày riêng theo nguồn paper.
---

### <a id="ref57"></a>[57] Akinrele and Gowda (2026) — Prompt Injection Detection is Regime-Dependent
- **Authors**: Akindoyin Akinrele and Shreyank N. Gowda.
- **Venue/version**: arXiv:2605.26999v1, submitted 2026-05-26; open-access preprint.
- **Official record**: [arXiv abstract](https://arxiv.org/abs/2605.26999) | [HTML paper](https://arxiv.org/html/2605.26999).
- **Local PDF**: **Akinrele_Gowda_2026_Regime_Dependent_Prompt_Injection_arXiv2605.26999v1.pdf** (local PDF; not packaged with portal); SHA-256 `4431bfb137935b457211c5ecb3d184e975fed38b21b9fd13116c3611a9b7c62f`.
- **Literature fact**: the paper evaluates lexical TF-IDF, structural signals, semantic models, and transformer/hybrid configurations across several regimes. The arXiv record still says code will be released and contains no official experiment-repository link (checked 2026-10-03); use it as literature context only, not as a local reproduction or source of PI-Guard empirical metrics.
- **Relevance and boundary**: supports the general observation that results vary by regime and that lexical and encoder families may have different strengths. It does not establish the PI-Guard TF-IDF→DeBERTa gate, its compute benefit, or its end-to-end performance.
---

### <a id="ref58"></a>[58] Microsoft DeBERTa-v3-base — public base checkpoint
- **Model repository**: [microsoft/deberta-v3-base](https://huggingface.co/microsoft/deberta-v3-base).
- **Pinned revision**: `8ccc9b6f36199bec6961081d44eb72fb3f7353f3` (MIT license as listed on the model card).
- **Local input manifest**: thuộc workspace cá nhân và không nằm trong repository này.
- **Provenance boundary**: đây là checkpoint khởi tạo công khai; tài liệu này không báo cáo kết quả fine-tuning cục bộ hoặc kết quả PI-Guard.

### <a id="ref59"></a>[59] DistilBERT-base-uncased — public base checkpoint
- **Model repository**: [distilbert/distilbert-base-uncased](https://huggingface.co/distilbert/distilbert-base-uncased).
- **Pinned revision**: `12040accade4e8a0f71eabdb258fecc2e7e948be` (Apache-2.0 license as listed on the model card).
- **Local input manifest**: thuộc workspace cá nhân và không nằm trong repository này.
- **Provenance boundary**: đây là checkpoint khởi tạo công khai; tài liệu này không báo cáo kết quả fine-tuning cục bộ hoặc kết quả PI-Guard.
---

## 4. ĐẦY ĐỦ CÁC MỤC TRÍCH DẪN BIBTEX CHUẨN IEEE (FACT-CHECKED BIBTEX REPOSITORY)

```bibtex
% ======================================================================================================================
% PHẦN I: 17 CÔNG TRÌNH KHOA HỌC CỐT LÕI CỦA LUẬN VĂN (CORE THESIS REFERENCES)
% ======================================================================================================================

@article{zhao2023survey,
  title     = {A Survey of Large Language Models},
  author    = {Zhao, Wayne Xin and Zhou, Kun and Li, Junyi and Tang, Tianyi and Wang, Xiaolei and Hou, Yupeng and Min, Yingqian and Zhang, Beichen and Zhang, Junjie and Dong, Zican and Du, Yifan and Yang, Chen and Chen, Yushuo and Chen, Zhipeng and Jiang, Jinhao and Ren, Ruiyang and Li, Yifan and Tang, Xinyu and Liu, Zikang and Liu, Peiyu and Nie, Jian-Yun and Wen, Ji-Rong},
  journal   = {arXiv preprint arXiv:2303.18223},
  year      = {2023}
}

@inproceedings{ouyang2022instructgpt,
  title     = {Training Language Models to Follow Instructions with Human Feedback},
  author    = {Ouyang, Long and Wu, Jeff and Jiang, Xu and Almeida, Diogo and Wainwright, Carroll L. and Mishkin, Pamela and Zhang, Chong and Agarwal, Sandhini and Slama, Katarina and Ray, Alex and Schulman, John and Hilton, Jacob and Kelton, Fraser and Miller, Luke and Simens, Maddie and Askell, Amanda and Welinder, Peter and Christiano, Paul and Leike, Jan and Lowe, Ryan},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS 2022)},
  volume    = {35},
  pages     = {27730--27744},
  year      = {2022}
}

@inproceedings{perez2022ignore,
  title     = {Ignore Previous Prompt: Attack Techniques For Language Models},
  author    = {Perez, F{\'a}bio and Ribeiro, Ian},
  booktitle = {NeurIPS 2022 ML Safety Workshop},
  year      = {2022},
  url       = {https://arxiv.org/abs/2211.09527}
}

@inproceedings{greshake2023indirect,
  title     = {Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection},
  author    = {Greshake, Kai and Abdelnabi, Sahar and Mishra, Shailesh and Endres, Christoph and Holz, Thorsten and Fritz, Mario},
  booktitle = {Proceedings of the 16th ACM Workshop on Artificial Intelligence and Security (ACM AISec '23)},
  pages     = {79--90},
  year      = {2023},
  doi       = {10.1145/3605764.3623985}
}

@inproceedings{wei2023jailbroken,
  title     = {Jailbroken: How Does LLM Safety Training Fail?},
  author    = {Wei, Alexander and Haghtalab, Nika and Steinhardt, Jacob},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS 2023)},
  volume    = {36},
  year      = {2023},
  url       = {https://arxiv.org/abs/2307.02483}
}

@techreport{yang2026securing,
  title       = {Securing the AI Agent: A Unified Framework for Multi-Layer Agent Red Teaming},
  author      = {Yang, Yong and Zheng, Xing and Wu, Huiyu and Cheng, Huangsheng and Shi, Xiaorong and Guo, Jing and Yang, Bo and Zhou, Yi and Wu, Xiangfan and Ying, Zonghao},
  institution = {Tencent Zhuque Lab},
  number      = {arXiv:2606.31227},
  year        = {2026},
  url         = {https://arxiv.org/abs/2606.31227}
}

@article{meta2023llamaguard,
  title     = {Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations},
  author    = {Inan, Hakan and Upasani, Kartikeya and Chi, Jianfeng and Rungta, Rashi and Iyer, Krithika and Mao, Yuning and Tontchev, Michael and Hu, Qing and Fuller, Brian and Testuggine, Davide and Khabsa, Madian},
  journal   = {arXiv preprint arXiv:2312.06674},
  year      = {2023}
}

@inproceedings{rebedea2023nemo,
  title     = {NeMo Guardrails: A Toolkit for Controllable and Safe LLM Applications with Programmable Rails},
  author    = {Rebedea, Traian and Dinu, Razvan and Sreedhar, Makesh and Parisien, Christopher and Cohen, Jonathan},
  booktitle = {Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing: System Demonstrations (EMNLP 2023)},
  pages     = {431--445},
  year      = {2023}
}

@inproceedings{he2023debertav3,
  title     = {DeBERTaV3: Improving DeBERTa using ELECTRA-Style Pre-Training with Gradient-Disentangled Embedding Sharing},
  author    = {He, Pengcheng and Gao, Jianfeng and Chen, Weizhu},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year      = {2023},
  url       = {https://arxiv.org/abs/2111.09543}
}

@inproceedings{markov2023openai,
  title     = {A Holistic Approach to Undesired Content Detection in the Real World},
  author    = {Markov, Todor and Zhang, Chong and Agarwal, Sandhini and Nekoul, Florentine Eloundou and Lee, Theodore and Adler, Steven and Jiang, Angela and Weng, Lilian},
  booktitle = {Proceedings of the AAAI Conference on Artificial Intelligence (AAAI 2023)},
  volume    = {37},
  number    = {12},
  pages     = {15009--15018},
  year      = {2023},
  doi       = {10.1609/aaai.v37i12.26752}
}

@inproceedings{shen2024dan,
  title     = {{"}Do Anything Now{"}: Characterizing and Evaluating In-The-Wild Jailbreak Prompts on Large Language Models},
  author    = {Shen, Xinyue and Chen, Zeyuan and Backes, Michael and Shen, Yun and Zhang, Yang},
  booktitle = {Proceedings of the 2024 ACM SIGSAC Conference on Computer and Communications Security (ACM CCS '24)},
  pages     = {4172--4186},
  year      = {2024},
  doi       = {10.1145/3658644.3670388}
}

@article{zhou2024easyjailbreak,
  title     = {EasyJailbreak: A Unified Framework for Jailbreaking Large Language Models},
  author    = {Zhou, Weikang and Wang, Xiao and Xiong, Limao and Xia, Han and Gu, Yingshuang and Chai, Mingxu and Zhu, Fukang and Huang, Caishuang and Dou, Shihan and Xi, Zhiheng and Zheng, Rui and Gao, Songyang and Zou, Yicheng and Yan, Hang and Le, Yifan and Wang, Ruohui and Li, Lijun and Shao, Jing and Gui, Tao and Zhang, Qi and Huang, Xuanjing},
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
  author    = {Jain, Neel and Schwarzschild, Avi and Wen, Yuxin and Somepalli, Gowthami and Kirchenbauer, John and Chiang, Ping-yeh and Goldblum, Micah and Saha, Aniruddha and Geiping, Jonas and Goldstein, Tom},
  journal   = {arXiv preprint arXiv:2309.00614},
  year      = {2023}
}

@inproceedings{yuan2024cipher,
  title     = {GPT-4 Is Too Smart To Be Safe: Stealthy Chat with LLMs via Cipher},
  author    = {Yuan, Youliang and Jiao, Wenxiang and Wang, Wenxuan and Huang, Jen-tse and He, Pinjia and Shi, Shuming and Tu, Zhaopeng},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year      = {2024},
  url       = {https://arxiv.org/abs/2308.06463}
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

% ======================================================================================================================
% PHẦN II: MÔ HÌNH ĐỐI CHUẨN SOTA & THỰC NGHIỆM TÁI LẬP (MEETING 5 REPLICATION SUITE)
% ======================================================================================================================

@inproceedings{li2025piguard,
  title     = {PIGuard: Prompt Injection Guardrail via Mitigating Over-defense for Free},
  author    = {Li, Hao and Liu, Xiaogeng and Zhang, Ning and Xiao, Chaowei},
  booktitle = {Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (ACL 2025)},
  pages     = {30420--30437},
  year      = {2025},
  doi       = {10.18653/v1/2025.acl-long.1468},
  url       = {https://aclanthology.org/2025.acl-long.1468/}
}

@inproceedings{wen2025instructdetector,
  title     = {Defending against Indirect Prompt Injection by Instruction Detection},
  author    = {Wen, Tongyu and Wang, Chenglong and Yang, Xiyuan and Tang, Haoyu and Xie, Yueqi and Lyu, Lingjuan and Dou, Zhicheng and Wu, Fangzhao},
  booktitle = {Findings of the Association for Computational Linguistics: EMNLP 2025},
  pages     = {19472--19487},
  year      = {2025},
  doi       = {10.18653/v1/2025.findings-emnlp.1060},
  url       = {https://aclanthology.org/2025.findings-emnlp.1060/}
}

@misc{meta2024promptguard,
  title        = {Prompt Guard 86M Model Card},
  author       = {{Meta AI}},
  year         = {2024},
  howpublished = {Hugging Face model card},
  url          = {https://huggingface.co/meta-llama/Prompt-Guard-86M}
}

@inproceedings{ayub2024camlis,
  title     = {Embedding-Based Classifiers Can Detect Prompt Injection Attacks},
  author    = {Ayub, Md. Ahsan and Majumdar, Subhabrata},
  booktitle = {Conference on Applied Machine Learning for Information Security (CAMLIS 2024)},
  year      = {2024},
  url       = {https://arxiv.org/abs/2410.22284}
}

% ======================================================================================================================
% PHẦN III: TÀI LIỆU LƯỢNG HÓA, DỮ LIỆU BENCHMARK & KHẢO SÁT MỞ RỘNG (SUPPLEMENTARY PAPERS)
% ======================================================================================================================

@inproceedings{yao2022zeroquant,
  title     = {ZeroQuant: Efficient and Affordable Post-Training Quantization for Large-Scale Transformers},
  author    = {Yao, Zhewei and Aminabadi, Reza Yazdani and Zhang, Minjia and Wu, Xiaoxia and Li, Conglong and He, Yuxiong},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS 2022)},
  volume    = {35},
  pages     = {27168--27183},
  year      = {2022},
  url       = {https://arxiv.org/abs/2206.01861}
}

@inproceedings{yi2024bipia,
  title     = {Benchmarking and Defending Against Indirect Prompt Injection Attacks on Large Language Models},
  author    = {Yi, Jingwei and Xie, Yueqi and Zhu, Bin and Hines, Keegan and Kiciman, Emre and Zhou, Anthony and Bogen, Miranda and Sun, Guangzhong and Xie, Xing},
  booktitle = {Findings of the Association for Computational Linguistics: NAACL 2024},
  pages     = {2844--2863},
  year      = {2024},
  url       = {https://arxiv.org/abs/2312.14197}
}

@inproceedings{wang2023donotanswer,
  title     = {Do-Not-Answer: A Dataset for Evaluating Safeguards in LLMs},
  author    = {Wang, Yuxia and Li, Haonan and Han, Xudong and Nakov, Preslav and Baldwin, Timothy},
  booktitle = {Findings of the Association for Computational Linguistics: EMNLP 2023},
  pages     = {896--908},
  year      = {2023},
  url       = {https://arxiv.org/abs/2308.13387}
}

@article{zhang2025jailguard,
  title     = {JailGuard: A Universal Detection Framework for Prompt-based Attacks on LLM Systems},
  author    = {Zhang, Xiaoyu and Zhang, Cen and Li, Tianlin and Huang, Yihao and Jia, Xiaojun and Hu, Ming and Zhang, Jie},
  journal   = {ACM Transactions on Software Engineering and Methodology (TOSEM)},
  year      = {2025},
  doi       = {10.1145/3724393}
}

@inproceedings{xu2024comprehensive,
  title     = {A Comprehensive Study of Jailbreak Attack versus Defense for Large Language Models},
  author    = {Xu, Zihao and Liu, Yi and Deng, Gelei and Li, Yuekang and Picek, Stjepan},
  booktitle = {Findings of the Association for Computational Linguistics: ACL 2024},
  pages     = {7432--7449},
  year      = {2024},
  doi       = {10.18653/v1/2024.findings-acl.442}
}

@article{liu2024exploring,
  title     = {Exploring Vulnerabilities and Protections in Large Language Models: A Survey},
  author    = {Liu, Frank Weizhen and Hu, Chenhui},
  journal   = {arXiv preprint arXiv:2403.09503},
  year      = {2024}
}

@article{yi2024jailbreak,
  title     = {Jailbreak Attacks and Defenses Against Large Language Models: A Survey},
  author    = {Yi, Sibo and Liu, Yule and Sun, Zhen and Cong, Tianshuo and He, Xinlei and Song, Jiaxing and Xu, Ke and Li, Qi},
  journal   = {arXiv preprint arXiv:2407.04295},
  year      = {2024}
}

@inproceedings{yang2026rapid,
  title     = {RAP-ID: Mechanistic Prompt Injection Detection via Impostor Behavior Analysis},
  author    = {Yang, Yuchen and Peng, Lei and He, Yujie and Yu, Yang and Wu, Zhongxin and Shi, Yanlei},
  booktitle = {Findings of the Association for Computational Linguistics: ACL 2026},
  pages     = {15008--15019},
  year      = {2026}
}
@inproceedings{jacob2025promptshield,
  title     = {PromptShield: Deployable Detection for Prompt Injection Attacks},
  author    = {Jacob, Dennis and Alzahrani, Hend and Hu, Zhanhao and Alomair, Basel and Wagner, David},
  booktitle = {Proceedings of the 15th ACM Conference on Data and Application Security and Privacy (CODASPY 2025)},
  pages     = {341--352},
  year      = {2025},
  doi       = {10.1145/3714393.3726501}
}

@inproceedings{hackett2025bypassing,
  title     = {Bypassing LLM Guardrails: An Empirical Analysis of Evasion Attacks against Prompt Injection and Jailbreak Detection Systems},
  author    = {Hackett, William and Birch, Lewis and Trawicki, Stefan and Suri, Neeraj and Garraghan, Peter},
  booktitle = {Proceedings of the The First Workshop on LLM Security (LLMSEC 2025) at ACL 2025},
  pages     = {101--114},
  year      = {2025},
  url       = {https://aclanthology.org/2025.llmsec-1.9/}
}

@inproceedings{liu2025datasentinel,
  title     = {DataSentinel: A Game-Theoretic Detection of Prompt Injection Attacks},
  author    = {Liu, Yupei and Jia, Yuqi and Jia, Jinyuan and Song, Dawn and Gong, Neil Zhenqiang},
  booktitle = {2025 IEEE Symposium on Security and Privacy (SP)},
  year      = {2025},
  doi       = {10.1109/SP61157.2025.00250}
}

@article{wallace2024instruction,
  title     = {The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions},
  author    = {Wallace, Eric and Xiao, Kai and Leike, Reimar and Weng, Lilian and Heidecke, Johannes and Beutel, Alex},
  journal   = {arXiv preprint arXiv:2404.13208},
  year      = {2024}
}

@inproceedings{chao2024jailbreakbench,
  title     = {JailbreakBench: An Open Robustness Benchmark for Jailbreaking Large Language Models},
  author    = {Chao, Patrick and Debenedetti, Edoardo and Robey, Alexander and Andriushchenko, Maksym and Croce, Francesco and Sehwag, Vikash and Dobriban, Edgar and Papernot, Nicolas and Pappas, George J. and Tram{\`e}r, Florian},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS 2024)},
  volume    = {37},
  year      = {2024}
}

@inproceedings{deng2024multilingual,
  title     = {Multilingual Jailbreak Challenges in Large Language Models},
  author    = {Deng, Yue and Zhang, Wenxuan and Pan, Sinno Jialin and Bing, Lidong},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year      = {2024}
}

@article{angelopoulos2024conformal,
  title     = {Conformal Risk Control},
  author    = {Angelopoulos, Anastasios N. and Bates, Stephen and Cand{\`e}s, Emmanuel J. and Jordan, Michael I. and Lei, Lihua},
  journal   = {arXiv preprint arXiv:2208.02814},
  year      = {2024}
}

@article{warner2024modernbert,
  title     = {ModernBERT: Bringing Modern Transformer Innovations to Pre-trained Encoders},
  author    = {Warner, Benjamin and Chaffin, Antoine and Clavi{\`e}, Benjamin and Weller, Orion and Hallstr{\"o}m, Oskar and Vasanth, Shraddha and Patry, Nikhil and Raffel, Colin and Zettlemoyer, Luke},
  journal   = {arXiv preprint arXiv:2412.13663},
  year      = {2024}
}

@article{padhi2024granite,
  title     = {Granite Guardian: A Family of Open Models for Content Safety and Risk Detection},
  author    = {Padhi, Inkit and Nagireddy, Manish and Cornacchia, Giandomenico and Das, Subhro and Pedapati, Tejaswini and Patel, Hima and others},
  journal   = {arXiv preprint arXiv:2412.07724},
  year      = {2024}
}

@article{russinovich2024crescendo,
  title     = {Great, Now Write an Article About That: The Crescendo Multi-Turn LLM Jailbreak Attack},
  author    = {Russinovich, Mark and Salem, Ahmed and Eldan, Ronen},
  journal   = {arXiv preprint arXiv:2404.01833},
  year      = {2024}
}

@article{zhou2026promptoverflow,
  title   = {Prompt Overflow: What the Guardrail Inspects Is Not What the Model Infers},
  author  = {Zhou, Yuanbo and Zhu, Changjia and Wang, Junyu and He, Xu and Zhai, Yan and Sun, Kun and Wei, Mingkui and Xiong, Junjie},
  journal = {arXiv preprint arXiv:2605.23196},
  year    = {2026}
}

@article{luo2026cascade,
  title   = {CASCADE Against Jailbreaks: Combination Across Stages with Controlled Attack-Defense Evaluation},
  author  = {Luo, Jiale and Han, Eric},
  journal = {arXiv preprint arXiv:2609.21793},
  year    = {2026}
}

@article{shire2026pidsbench,
  title   = {PIDS-Bench: Evaluating Prompt-Injection Detectors Under Over-Defense, Obfuscation, and Distribution Shift},
  author  = {Shire, Yusuf Khalid and Kim, Sang-Chul},
  journal = {IEEE Access},
  volume  = {14},
  pages   = {134184--134205},
  year    = {2026},
  doi     = {10.1109/ACCESS.2026.3728186}
}

@misc{akinrele2026regimedependent,
  author        = {Akinrele, Akindoyin and Gowda, Shreyank N.},
  title         = {Prompt Injection Detection is Regime-Dependent: A Deployment-Aware Evaluation with Interpretable Structural Signals},
  year          = {2026},
  eprint        = {2605.26999},
  archivePrefix = {arXiv},
  primaryClass  = {cs.CL},
  doi           = {10.48550/arXiv.2605.26999},
  url           = {https://arxiv.org/abs/2605.26999}
}

@misc{protectai2024deberta,
  author    = {{ProtectAI}},
  title     = {Fine-Tuned DeBERTa-v3-base for Prompt Injection Detection},
  year      = {2024},
  publisher = {Hugging Face},
  url       = {https://huggingface.co/protectai/deberta-v3-base-prompt-injection-v2}
}
```