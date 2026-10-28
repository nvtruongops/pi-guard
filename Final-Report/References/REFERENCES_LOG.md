# REFERENCES LOG & APPLICATION MAPPING MATRIX
## Hệ Thống Quản Lý & Định Vị Tài Liệu Tham Khảo — Đề Tài PI-Guard (COMPREHENSIVE VERIFIED LITERATURE MATRIX)

> **Local source archive**: 40 PDF files; the portal shows metadata and source links.
> **Tiêu chuẩn học thuật**: 16 công trình khoa học đỉnh cao kỷ nguyên LLM hiện đại (2022–2026) + 1 công trình kinh điển đặt nền móng kiến trúc bảo vệ phân tầng (Saltzer & Schroeder, IEEE 1975) + 12 tài liệu chuyên đề, mô hình đối chuẩn SOTA Meeting 5 (PIGuard ACL 2025, InstructDetector, Prompt Guard, Ayub CAMLIS, ZeroQuant, BIPIA, Do-Not-Answer, v.v.) + các công trình nền tảng toán học & thông tin (Luhn 1958, Spärck Jones 1972, fastText TACL 2017, Attention NeurIPS 2017, BERT NAACL 2019).
> **Total locally archived PDFs**: **40 full-text PDFs**.
> **Last normalized**: 2026-09-30 (verified source metadata and provenance levels).
> **Mục đích**: Lưu trữ, lập chỉ mục siêu dữ liệu chuẩn xác, phân định rạch ròi 4 tầng xuất xứ học thuật và ánh xạ toàn diện vào cấu trúc luận văn, chuyên đề nghiên cứu và mã nguồn đồ án PI-Guard.

---

## Tiêu chuẩn trình bày sơ đồ (nguồn dẫn, không phải paper thực nghiệm)

- **ISO 5807:1985**, *Information processing — Documentation symbols and conventions for data, program and system flowcharts, program network charts and system resources charts*, ấn bản thứ nhất, 1985-02-15. [Hồ sơ tiêu chuẩn tại ISO](https://www.iso.org/standard/11955.html); [bản xem trước 12 trang do iTeh cung cấp](https://cdn.standards.iteh.ai/samples/11955/1b7dd254a2a54fd7a89d616dc0570e18/ISO-5807-1985.pdf).
- **Phạm vi dùng trong PI-Guard:** tham chiếu một số ký hiệu *Data* (§9.1.1.1), *Process* (§9.2.1), *Decision* (§9.2.2.4), *Line* (§9.3.1) và vùng chú giải nét đứt (§9.3.2.3) cho [sơ đồ ingress](../reports/PI_GUARD_INGRESS_ARCHITECTURE.drawio). [Bảng đối chiếu từng trang](../reports/ISO_5807_1985_SYMBOL_AUDIT.md) ghi cả các giới hạn và chỉnh sửa.
- **Giới hạn:** bản xem trước kết thúc ở trang in 8, không có phần conventions §10 và bảng ký hiệu tổng hợp. ISO 5807 là nguồn cho ký hiệu lưu đồ, **không** chứng minh kiến trúc ML ba tầng, icon, màu hay kết quả ba nhãn. PDF chỉ lưu để tra cứu trong workspace cá nhân bị Git bỏ qua; [bản quyền ISO](https://www.iso.org/copyright.html) không cho phép phân phối lại tùy ý trong repo công khai.

---

## 🔒 0. NGUYÊN TẮC BẤT BIẾN: "LOCAL REFERENCES FIRST" PROTOCOL & FOUR-TIER PROVENANCE
> [!IMPORTANT]
> **QUY TRÌNH BẮT BUỘC CHO MAINTAINER & AI AGENTS TRƯỚC KHI TÌM KIẾM BÀI BÁO MỚI**:
> 1. **TRUY LỤC TÀI LIỆU CỤC BỘ TRƯỚC TIÊN (Local References First)**:
>    - Khi cần luận chứng cho bất kỳ tuyên bố khoa học, cơ chế tấn công, kiến trúc phòng thủ hay công thức toán học nào, **BẮT BUỘC phải tra cứu bảng Ma Trận Chủ Đề (Mục 1) và Siêu Dữ Liệu Các Bài Báo (Mục 2 & Mục 3)** trong tệp này trước.
>    - Nếu luận điểm đã được bảo chứng bởi một nguồn trong danh mục, tái sử dụng đúng mã neo `[[N]](#refN)` và đọc bản PDF cục bộ nếu có hoặc liên kết nguồn đã ghi.
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

## 🗺️ 1. MA TRẬN ĐỊNH VỊ NHANH THEO CHỦ ĐỀ & 7 CHUYÊN ĐỀ (TAXONOMY LOOKUP MATRIX)

### 1.1. Nhóm 17 Công Trình Khoa Học Cốt Lõi Của Luận Văn (Core Landmark Papers)

| Chủ Đề / Chuyên Đề Nghiên Cứu | Mã Neo | Tác Giả & Năm | PDF / nguồn truy cập | Đóng Góp Gốc Của Bài Báo (Tier 1) | Định Vị Kỹ Thuật Trong Đồ Án PI-Guard (Tier 2 & 3) |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **1. Tổng quan Kiến trúc LLM & Lỗ hổng Ranh giới Phẳng** | [[1]](#ref1) | Zhao et al. (2023) | [`Zhao_2023_A_Survey_of_Large_Language_Models.pdf`](./Zhao_2023_A_Survey_of_Large_Language_Models.pdf) | Khảo sát kiến trúc Transformer tự hồi quy và không gian token ngữ cảnh phẳng. | Cơ sở phân tích: LLM xử lý ngữ cảnh dưới dạng chuỗi token và không tự cung cấp một security boundary đáng tin cậy giữa instruction và untrusted data. (*Chương 1, 2; Chuyên đề 1*) |
| **2. Instruction Tuning & Xử lý System Prompt** | [[2]](#ref2) | Ouyang et al. (2022) | [`Ouyang_2022_InstructGPT_Training_Language_Models_Follow_Instructions.pdf`](./Ouyang_2022_InstructGPT_Training_Language_Models_Follow_Instructions.pdf) | Đặt nền móng kỹ thuật Instruction Tuning qua RLHF; chứng minh khả năng căn chỉnh tuân thủ ý định người dùng. | Cung cấp nền tảng về instruction-following và alignment, được PI-Guard dùng làm cơ sở phân tích cách các chỉ thị cạnh tranh mức độ ưu tiên trong LLM. (*Chương 1, 2; Chuyên đề 1*) |
| **3. Direct Prompt Injection (Tấn công Trực tiếp)** | [[3]](#ref3) | Perez & Ribeiro (2022) | [`Perez_2022_Ignore_This_Title_Hack_This_Paper_Prompt_Injection.pdf`](./Perez_2022_Ignore_This_Title_Hack_This_Paper_Prompt_Injection.pdf) | Định nghĩa và phân loại chính thức hai dạng Direct Prompt Injection: Goal Hijacking và Prompt Leaking. | Cơ sở phân loại lớp nhãn Prompt Injection và xây dựng kịch bản kiểm thử thực nghiệm. (*Chương 1, 2, 3; Chuyên đề 2*) |
| **4. Indirect Prompt Injection (Tấn công Gián tiếp)** | [[4]](#ref4) | Greshake et al. (2023) | [`Greshake_2023_Indirect_Prompt_Injection.pdf`](./Greshake_2023_Indirect_Prompt_Injection.pdf) | Độc hại nhúng trong dữ liệu bên ngoài (Web/RAG); mô hình hóa rủi ro ứng dụng tích hợp LLM. | Luận giải nhu cầu bắt buộc phải có lớp Input Guardrail độc lập ở Ingress để kiểm soát cả dữ liệu RAG. (*Chương 1, 2, 3; Chuyên đề 2, 3*) |
| **5. Cơ chế Thất bại Căn chỉnh An toàn (Jailbreak Failures)** | [[5]](#ref5) | Wei et al. (2023) | [`Wei_2024_Jailbroken_How_LLM_Safety_Training_Fails.pdf`](./Wei_2024_Jailbroken_How_LLM_Safety_Training_Fails.pdf) | Xác lập 2 chế độ lỗi căn chỉnh: Competing Objectives & Mismatched Generalization (NeurIPS 2023). | Cơ sở chứng minh an toàn nội tại là chưa đủ, cần bộ phân loại độc lập bên ngoài. (*Chương 1, 4; Chuyên đề 2*) |
| **6. Mô hình Đe Dọa Đa Tầng Cho AI Agent** | [[6]](#ref6) | Yang et al. / Tencent (2026) | [`Tencent_2026_AI_Infra_Guard_MultiLayer_Agent_RedTeaming.pdf`](./Tencent_2026_AI_Infra_Guard_MultiLayer_Agent_RedTeaming.pdf) | Khung Red Teaming đa tầng cho Agent; phân loại 26+ toán tử tấn công hạ tầng. | PI-Guard tham khảo mô hình phân tầng Zone 0–3 để tổ chức phạm vi tấn công và vị trí của guardrail proxy. (*Chương 1, 3; Chuyên đề 2, 3*) |
| **7. Guardrail Dựa Trên LLM (LLM-as-a-Judge Baseline)** | [[7]](#ref7) | Inan et al. / Meta (2023) | [`Meta_2023_Llama_Guard_Input_Output_Safeguard.pdf`](./Meta_2023_Llama_Guard_Input_Output_Safeguard.pdf) | Mô hình LLM 7B làm trọng tài an toàn; chuẩn hóa taxonomy phân loại rủi ro nội dung. | Mô hình đối chuẩn (Baseline): PI-Guard đặt mục tiêu đánh giá liệu classifier nhỏ chạy CPU có đạt trade-off latency/accuracy tốt hơn Llama Guard hay không. (*Chương 2, 4; Chuyên đề 5, 7*) |
| **8. Kiến Trúc Guardrail Middleware Lập Trình Được** | [[8]](#ref8) | Rebedea et al. / NVIDIA (2023)| [`NVIDIA_2023_NeMo_Guardrails_Toolkit.pdf`](./NVIDIA_2023_NeMo_Guardrails_Toolkit.pdf) | Bộ công cụ kiểm soát an toàn dạng middleware lập trình được với Colang. | Cơ sở tham khảo kiến trúc Ingress Proxy bất đồng bộ đánh chặn trước LLM. (*Chương 2, 3; Chuyên đề 3*) |
| **9. Huấn Luyện Ngữ Nghĩa Sâu Với DeBERTa-v3** | [[9]](#ref9) | He, Gao, Chen (2023) | [`He_2023_DeBERTaV3_Disentangled_Attention_ICLR.pdf`](./He_2023_DeBERTaV3_Disentangled_Attention_ICLR.pdf) | Đột phá ELECTRA-style RTD và Gradient-Disentangled Embedding Sharing (GDES) tại ICLR 2023. | Lý giải việc lựa chọn DeBERTa-v3 làm bộ phân loại ngữ nghĩa sâu Tầng 2. (*Chương 3, 4; Chuyên đề 5*) |
| **10. Kiểm Soát Đánh Đổi FPR Trong Phát Hiện Độc Hại** | [[10]](#ref10) | Markov et al. / OpenAI (2023) | [`OpenAI_2023_Undesired_Content_Detection.pdf`](./OpenAI_2023_Undesired_Content_Detection.pdf) | Phương pháp luận kiểm duyệt nội dung thực tế (AAAI 2023); phân tích chi phí FPR đối với trải nghiệm người dùng. | Cung cấp bài học thực tế để PI-Guard thiết lập yêu cầu kỹ thuật: đặt mục tiêu kiểm soát $\text{FPR} < 1.5\%$ trên tập lành tính. (*Chương 2, 4; Chuyên đề 7*) |
| **11. Khảo Sát Thực Nghiệm Prompt Jailbreak Trong Tự Nhiên** | [[11]](#ref11) | Shen et al. (2024) | [`Shen_2024_Do_Anything_Now_Jailbreak_Prompts_In_The_Wild.pdf`](./Shen_2024_Do_Anything_Now_Jailbreak_Prompts_In_The_Wild.pdf) | Tập dữ liệu công bố 1,405/15,140 prompts, tương đương khoảng 9.29% (thường được báo cáo làm tròn là 9.3%); kèm ghi chú phân biệt giữa số liệu của các phiên bản/mô tả khác nhau của nghiên cứu. | Nguồn dữ liệu kiểm thử thực nghiệm jailbreak tự nhiên cho PI-Guard. (*Chương 3, 4; Chuyên đề 2, 4*) |
| **12. Khung Kiểm Thử Đối Kháng & Đột Biến Văn Bản** | [[12]](#ref12) | Zhou et al. (2024) | [`Zhou_2024_EasyJailbreak_Unified_Framework.pdf`](./Zhou_2024_EasyJailbreak_Unified_Framework.pdf) | Framework tự động hóa đột biến jailbreak 4 tầng (Initialize, Mutate, Evaluate, Select). | PI-Guard sử dụng các toán tử đột biến của framework này làm công cụ fuzzing; đặt mục tiêu kiểm thử duy trì $\Delta F_1 < 5\%$. (*Chương 3, 4; Chuyên đề 6*) |
| **13. Tấn Công Chuỗi Hậu Tố Đối Kháng Tối Ưu Hóa (GCG)** | [[13]](#ref13) | Zou et al. (2023) | [`Zou_2023_Universal_Transferable_Adversarial_Attacks_GCG.pdf`](./Zou_2023_Universal_Transferable_Adversarial_Attacks_GCG.pdf) | Thuật toán Greedy Coordinate Gradient sinh hậu tố đối kháng chuyển giao. | PI-Guard sử dụng các mẫu sinh bởi GCG như một tập kiểm thử đánh giá đối kháng ngoại lai (OOD evaluation set). (*Chương 4; Chuyên đề 6*) |
| **14. Phòng Thủ Bằng Xáo Trộn Ngẫu Nhiên (SmoothLLM)** | [[14]](#ref14) | Robey et al. (2023) | [`Robey_2023_SmoothLLM_Defending_LLMs_Random_Perturbation.pdf`](./Robey_2023_SmoothLLM_Defending_LLMs_Random_Perturbation.pdf) | Cơ chế làm mịn ngẫu nhiên qua biến dị prompt và đa số biểu quyết phản hồi LLM. | PI-Guard sử dụng làm baseline đối chuẩn để so sánh đánh đổi giữa multi-query defense và single-pass classifier. (*Chương 2, 4; Chuyên đề 3, 6*) |
| **15. Baseline Defenses for Adversarial Attacks Against Aligned Language Models** | [[15]](#ref15) | Jain et al. (2023) | [`Jain_2023_Baseline_Defenses_Adversarial_Attacks_LLMs.pdf`](./Jain_2023_Baseline_Defenses_Adversarial_Attacks_LLMs.pdf) | Thực nghiệm các baseline phòng thủ gồm lọc perplexity, paraphrase/retokenization và adversarial training trước jailbreak; bài không đánh giá bộ phân loại TF-IDF Word/Char. | Chỉ dùng làm tài liệu về baseline phòng thủ jailbreak; không trích dẫn để bảo chứng mô hình TF-IDF của Tầng 1. (*Chương 2*) |
| **16. Nguyên Lý Thiết Kế Hệ Thống Bảo Vệ Kinh Điển** | [[16]](#ref16) | Saltzer & Schroeder (1975) | [`Saltzer_1975_The_Protection_of_Information_in_Computer_Systems.pdf`](./Saltzer_1975_The_Protection_of_Information_in_Computer_Systems.pdf) | Các nguyên tắc thiết kế bảo vệ hệ thống máy tính được Saltzer và Schroeder đề xuất (Complete Mediation, Economy of Mechanism, Defense-in-Depth). | Nền tảng thiết kế hệ thống: Kiểm soát toàn diện tại Ingress (Complete Mediation) và kiến trúc phân tầng (Defense-in-Depth). (*Chương 2, 3; Chuyên đề 3*) |
| **17. Lẩn Tránh Bằng Biến Đổi Ký Tự (CipherChat & Encoding)** | [[17]](#ref17) | Yuan et al. (2024) | [`Yuan_2024_GPT4_Too_Smart_To_Be_Safe_Cipher_Jailbreak.pdf`](./Yuan_2024_GPT4_Too_Smart_To_Be_Safe_Cipher_Jailbreak.pdf) | Khung CipherChat: Nghiên cứu các phép biến đổi prompt dựa trên mật mã cổ điển/bảng mã để vượt qua căn chỉnh an toàn. | Luận chứng cho việc tích hợp mô-đun tiền xử lý chuẩn hóa chuỗi và giải mã tiền trạm. (*Chương 1, 3, 4; Chuyên đề 2, 6*) |

---

### 1.2. Nhóm Mô Hình Đối Chuẩn SOTA & Thực Nghiệm Tái Lập (Meeting 5 Replication Suite)

| Mô Hình / Nghiên Cứu | Mã Định Danh | Tác Giả & Năm | PDF / nguồn truy cập | Đóng Góp Gốc & Đặc Điểm Kỹ Thuật (Tier 1) | Vai Trò & Ứng Dụng Trong Đồ Án PI-Guard (Tier 2 & 3) |
| :--- | :---: | :--- | :--- | :--- | :--- |
| <a id="ref18"></a>**18. PIGuard (ACL 2025)** | `[ACL-PIGuard]` | Hao Li et al. (2025) | [`PIGuard_2025_Prompt_Injection_Guardrail_ACL.pdf`](./PIGuard_2025_Prompt_Injection_Guardrail_ACL.pdf) | DeBERTa-v3 guardrail và chiến lược MOF nhằm giảm over-defense; bài báo báo cáo cải thiện 30,4% so với phương pháp tốt nhất trước đó trên các benchmark được nêu. | Baseline phân loại prompt injection. Kết quả tái chạy checkpoint phải ghi rõ tập công khai và không đồng nhất với huấn luyện lại toàn bộ paper; paper gốc là bộ phân loại nhị phân. |
| <a id="ref19"></a>**19. Defending against Indirect Prompt Injection by Instruction Detection** | `[EMNLP-ID]` | Tongyu Wen et al. (2025) | [`Wen_2025_InstructDetector_Findings_EMNLP.pdf`](./Wen_2025_InstructDetector_Findings_EMNLP.pdf) | InstructDetector kết hợp hidden states và gradients từ các lớp trung gian của LLM rồi đưa đặc trưng vào MLP; đây không phải TF-IDF. | Tài liệu về phát hiện indirect prompt injection có điều kiện truy cập trạng thái nội bộ. Không phải mô hình proxy black-box của đồ án và không dùng để chứng minh TF-IDF. |
| <a id="ref20"></a>**20. Prompt Guard 86M (Meta 2024, model card)** | `[Meta-PG86M]` | Meta AI / Purple Llama (2024) | [`Meta_2024_Prompt_Guard_86M_Input_Guardrail.pdf`](./Meta_2024_Prompt_Guard_86M_Input_Guardrail.pdf); model card chính thức: [Hugging Face](https://huggingface.co/meta-llama/Prompt-Guard-86M) | Dùng mDeBERTa-v3-base; model card nêu các nhãn benign, injection, jailbreak, dữ liệu huấn luyện gồm dữ liệu mở, tổng hợp và red-team, đồng thời ghi nhận injection/jailbreak có thể chồng lấn. Toàn bộ train rows không được công bố. | Ngày 2026-10-06, authenticated Hugging Face CLI đã tải và hash kiểm tra đủ 5 inference files tại revision `1209add6ca7d9c1d815171b8e5571587fe3e7b03`; đây là access đã xác minh cho tài khoản hiện dùng, không phải checkpoint mở tự do. Áp dụng Llama 3.1 Community License và use policy; xem manifests cục bộ trước khi sử dụng/phân phối. |
| <a id="ref21"></a>**21. Embedding-based classifiers can detect prompt injection attacks** | `[CAMLIS-Ayub]` | Md. Ahsan Ayub & Subhabrata Majumdar (2024) | [arXiv:2410.22284](https://arxiv.org/abs/2410.22284); tệp PDF cục bộ có tên khác tiêu đề bài | Tạo embedding bằng ba encoder rồi huấn luyện classifier truyền thống; Random Forest và XGBoost là các kết quả tốt nhất được tác giả nêu. Đây không phải TF-IDF. | Bài CAMLIS 2024/preprint về embedding classifier nhị phân; không dùng để bảo chứng mô hình TF-IDF n-gram hoặc kết quả của runner local. |

---

### 1.3. Nhóm Tài Liệu Bổ Trợ, Lượng Hóa Mô Hình & Khảo Sát Mở Rộng

| Chủ Đề / Tài Nguyên | Mã Định Danh | Tác Giả & Năm | PDF / nguồn truy cập | Đóng Góp Gốc & Bản Chất Phương Pháp | Vai Trò & Ứng Dụng Trong Đồ Án PI-Guard |
| :--- | :---: | :--- | :--- | :--- | :--- |
| <a id="ref22"></a>**22. Lượng Hóa INT8 Mô Hình Transformers** | `[NeurIPS-ZeroQuant]` | Yao et al. / Microsoft (2022) | [PDF nguồn](https://arxiv.org/pdf/2206.01861.pdf) | Phương pháp lượng hóa sau huấn luyện (PTQ) INT8 cho Transformers, giảm 4x bộ nhớ và tăng tốc 2–3x suy diễn mà giữ nguyên độ chính xác. | ⚠️ **Ghi chú loại trừ phạm vi (Out-of-Scope / IA Discipline Invariant)**: Không sử dụng làm hướng nâng cấp kỹ thuật của đồ án. Đề tài PI-Guard thuộc chuyên ngành An toàn Thông tin (Information Assurance - IA), tập trung chuyên sâu vào mô hình hóa mối đe dọa, cơ chế tấn công Prompt Injection / Jailbreak và kiến trúc phòng thủ phân tầng, KHÔNG đi vào hướng tối ưu hóa kỹ thuật phần cứng hay lượng tử hóa mô hình. |
| <a id="ref23"></a>**23. Benchmark Indirect Prompt Injection (BIPIA)** | `[NAACL-BIPIA]` | Yi et al. / MS Research (2024) | [`Viet_2024_BIPIA_Benchmarking_Indirect_Prompt_Injection_Attacks.pdf`](./Viet_2024_BIPIA_Benchmarking_Indirect_Prompt_Injection_Attacks.pdf) | Bộ dữ liệu benchmark chuẩn hóa đánh giá Indirect Prompt Injection trên 5 tác vụ ứng dụng phổ biến (Email, Web, RAG). | Cung cấp nguồn mẫu thử gián tiếp để kiểm tra độ khái quát hóa ngoại miền (OOD evaluation). |
| <a id="ref24"></a>**24. Bộ Dữ Liệu An Toàn Do-Not-Answer** | `[EMNLP-DNA]` | Wang et al. (2023) | [`Phuong_2023_Do_Not_Answer_Dataset_Evaluating_Safeguards.pdf`](./Phuong_2023_Do_Not_Answer_Dataset_Evaluating_Safeguards.pdf) | 936 prompt độc hại có cấu trúc rủi ro 5 tầng nhằm đo lường khả năng từ chối an toàn của LLM. | Nguồn mẫu đối kháng kiểm tra độ nhạy của bộ lọc trong Chuyên đề 4 (`dataset_study`). |
| <a id="ref25"></a>**25. Universal Jailbreak Detection (JailGuard)** | `[TOSEM-JailGuard]` | Zhang et al. (2025) | [`Duc_2025_JailGuard_Universal_Detection_Framework_TOSEM.pdf`](./Duc_2025_JailGuard_Universal_Detection_Framework_TOSEM.pdf) | Framework phát hiện jailbreak dựa trên đột biến biến thể prompt và đo độ phân kỳ hành vi mô hình (TOSEM 2025). | Nghiên cứu đối chuẩn so sánh kỹ thuật đột biến và cơ chế đánh chặn đa tầng. |
| <a id="ref26"></a>**26. Khảo Sát Thực Nghiệm Toàn Diện Jailbreak** | `[ACL-JailbreakStudy]` | Xu et al. (2024) | [`Phuong_2024_ACL_Comprehensive_Study_Jailbreak_Attack_Defense.pdf`](./Phuong_2024_ACL_Comprehensive_Study_Jailbreak_Attack_Defense.pdf) | So sánh thực nghiệm quy mô lớn giữa các phương pháp tấn công jailbreak và cơ chế phòng thủ trên ACL 2024. | Bổ trợ cho phân tích Taxonomy và ma trận đối sánh trong Chương 2. |
| <a id="ref27"></a>**27. Khảo Sát Lỗ Hổng & Bảo Vệ LLM Công Nghiệp** | `[Survey-LiuHu]` | Liu & Hu / Zscaler (2024) | [`Phuong_2024_Exploring_Vulnerabilities_Protections_LLMs_Survey.pdf`](./Phuong_2024_Exploring_Vulnerabilities_Protections_LLMs_Survey.pdf) | Khảo sát các lỗ hổng an ninh LLM từ góc nhìn ứng dụng doanh nghiệp và kiến trúc Security Gateway. | Cung cấp góc nhìn thực tiễn về triển khai Ingress Proxy trong môi trường mạng thực tế. |
| <a id="ref28"></a>**28. Khảo Sát Tấn Công & Phòng Thủ Jailbreak** | `[Survey-Tsinghua]` | Yi et al. / Tsinghua (2024) | [`Phuong_2024_Survey_Jailbreak_Attacks_Defenses_LLMs.pdf`](./Phuong_2024_Survey_Jailbreak_Attacks_Defenses_LLMs.pdf) | Hệ thống hóa toàn diện các kỹ thuật tấn công và giải pháp phòng thủ theo từng tầng (Pre-processing, In-processing, Post-processing). | Củng cố luận cứ lý thuyết cho kiến trúc bảo vệ phân tầng Ingress của PI-Guard. |
| <a id="ref29"></a>**29. Nghiên Cứu Loại Trừ: RAP-ID (Lenovo 2026)** | `[ACL-RAPID-Excl]` | Yang et al. / Lenovo (2026) | [PDF nguồn](https://aclanthology.org/2026.findings-acl.738.pdf) | Phát hiện prompt injection dựa trên phân tích trạng thái nội bộ (internal model states) và attention dynamics. | **Xác định rõ là Ngoài Phạm Vi (Out-of-Scope)**: Do đòi hỏi can thiệp white-box vào forward pass của target LLM, không tương thích với mô hình External Black-Box Proxy của đề tài. |
| <a id="ref30"></a>**30. PromptShield (CODASPY 2025)** | [CODASPY-PromptShield] | Jacob et al. (2025) | [Jacob_2025_PromptShield_Deployable_Detection_CODASPY.pdf](./Jacob_2025_PromptShield_Deployable_Detection_CODASPY.pdf) | Benchmark phát hiện prompt injection trong điều kiện FPR thấp; kết quả của các bộ phát hiện chỉ áp dụng theo giao thức và tập đánh giá paper. | **Cơ sở đánh giá Low-FPR**: PI-Guard có thể tham khảo các mức FPR và cách đọc ROC; KPI của đồ án là mục tiêu riêng, chưa được paper chứng minh. |
| <a id="ref31"></a>**31. Bypassing LLM Guardrails (ACL 2025 LLMSEC)** | [LLMSEC-Hackett] | Hackett et al. (Mindgard, 2025) | [Hackett_2025_Bypassing_LLM_Guardrails_Evasion_Attacks.pdf](./Hackett_2025_Bypassing_LLM_Guardrails_Evasion_Attacks.pdf) | Đánh giá thực nghiệm 12 đòn biến dị ký tự (Emoji Smuggling, Unicode Tags) và 8 thuật toán AML Evasion; chứng minh Meta PromptGuard bị bypass 100%. | **Bảo chứng Tầng 0 (Heuristic Scrubber)**: Chứng minh các Transformer bị mù trước Unicode/Emoji; xác lập tính tất yếu của bộ lọc chuẩn hóa ký tự trước khi tokenize. |
| <a id="ref32"></a>**32. DataSentinel: A Game-Theoretic Detection of Prompt Injection Attacks (IEEE S&P 2025)** | [SP-DataSentinel] | Liu et al. (Penn State / Berkeley, 2025) | [Liu_2025_DataSentinel_Game_Theoretic_Detection_Prompt_Injection.pdf](./Liu_2025_DataSentinel_Game_Theoretic_Detection_Prompt_Injection.pdf) | Mô hình toán học Minimax Game-Theory giữa Attacker (Inner Max) và Defender (Outer Min) phát hiện Adaptive Prompt Injection. | **Nền tảng lý thuyết trò chơi & Dữ liệu OOD**: Cung cấp khung tối ưu hóa đối kháng và tập benchmark Open-Prompt-Injection cho kiểm thử độ bền. |
| <a id="ref33"></a>**33. The Instruction Hierarchy (OpenAI 2024)** | [OpenAI-InstructionHierarchy] | Wallace et al. (OpenAI, 2024) | [Wallace_2024_Instruction_Hierarchy_Prioritize_Privileged_Instructions.pdf](./Wallace_2024_Instruction_Hierarchy_Prioritize_Privileged_Instructions.pdf) | Phân tầng quyền hạn chỉ thị (System > User > Tool/Data); chứng minh in-model alignment không thể ngăn chặn triệt để tấn công đối kháng và gây over-refusal. | **Bảo chứng Ingress Guardrail Proxy**: Khẳng định in-model training không đủ; xác lập tính tất yếu của Guardrail Proxy bên ngoài theo nguyên lý Defense-in-Depth. |
| <a id="ref34"></a>**34. JailbreakBench (NeurIPS 2024)** | [NeurIPS-JailbreakBench] | Chao et al. (UPenn / EPFL / ETH, 2024) | [Chao_2024_JailbreakBench_Open_Robustness_Benchmark_NeurIPS.pdf](./Chao_2024_JailbreakBench_Open_Robustness_Benchmark_NeurIPS.pdf) | Chuẩn benchmark đối kháng mã nguồn mở đầu tiên của cộng đồng; công bố tập dữ liệu chuẩn JBB-Behaviors gồm 100 hành vi vi phạm an toàn. | **Chuẩn đối chuẩn cộng đồng**: Tích hợp JBB-Behaviors vào bộ kiểm thử thực nghiệm; đối sánh hiệu năng PI-Guard với các SOTA defenses trên leaderboard toàn cầu. |
| <a id="ref35"></a>**35. Multilingual Jailbreak Challenges (ICLR 2024)** | [ICLR-MultiJail] | Deng et al. (2024) | [Deng_2024_Multilingual_Jailbreak_Challenges_LLMs_ICLR.pdf](./Deng_2024_Multilingual_Jailbreak_Challenges_LLMs_ICLR.pdf) | MultiJail gồm 315 prompt gốc tiếng Anh được dịch sang chín ngôn ngữ khác (3.150 prompt tổng cộng) để nghiên cứu jailbreak đa ngôn ngữ đối với LLM; đây không phải benchmark phân loại prompt injection. | **Ứng dụng PI-Guard**: Có thể dùng làm nguồn kiểm thử chuyển ngôn ngữ sau khi xác minh nhãn và giao thức; không chứng minh hiệu năng tiếng Việt của bộ phân loại. |
| <a id="ref36"></a>**36. Conformal Risk Control** | [NeurIPS-ConformalGuardrail] | Angelopoulos et al. (2022 preprint; later publication metadata to verify) | [PDF nguồn](https://arxiv.org/pdf/2208.02814.pdf) | Khung CRC kiểm soát rủi ro kỳ vọng dưới các giả định và định nghĩa loss cụ thể; không tự động bảo đảm FPR của PI-Guard. | **Ứng dụng PI-Guard**: Có thể nghiên cứu hiệu chuẩn có kiểm soát rủi ro nếu xác định loss, điều kiện dữ liệu và kiểm định giả định; chưa phải bằng chứng KPI FPR hiện tại. |
| <a id="ref37"></a>**37. ModernBERT (Answer.AI / LightOn 2024)** | [arXiv-ModernBERT] | Warner et al. (2024) | [PDF nguồn](https://arxiv.org/pdf/2412.13663.pdf) | Encoder pretrained với cửa sổ ngữ cảnh tối đa 8.192 token; kết quả tốc độ trong paper phụ thuộc tác vụ, phần cứng và thiết lập so sánh. Đây không phải classifier prompt injection. | **Ứng dụng PI-Guard**: Chỉ là backbone ứng viên cần fine-tune và đo trên cùng protocol; không suy ra độ trễ hay chất lượng guardrail từ paper pretraining. |
| <a id="ref38"></a>**38. Granite Guardian (IBM Research 2024)** | [IBM-GraniteGuardian] | Padhi et al. (IBM Research, 2024) | [Padhi_2024_Granite_Guardian_Content_Safety_Risk_Detection.pdf](./Padhi_2024_Granite_Guardian_Content_Safety_Risk_Detection.pdf) | Dòng mô hình mở chuyên biệt cho an toàn nội dung và rủi ro LLM (2B/8B), bao phủ Jailbreak, Prompt Injection và RAG Hallucination. | **Mô hình tham chiếu SOTA SLM Guardrail**: Cung cấp cơ sở đối chuẩn cho tầng phân xử cấp cao (High-Assurance Arbiter) ở Tier 3. |
| <a id="ref39"></a>**39. Crescendo Multi-Turn Attack (Microsoft 2024)** | [MS-Crescendo] | Russinovich et al. (Microsoft Research, 2024) | [Russinovich_2024_Crescendo_MultiTurn_Jailbreak_Attack.pdf](./Russinovich_2024_Crescendo_MultiTurn_Jailbreak_Attack.pdf) | Phát hiện phương thức tấn công đa lượt leo thang (Crescendo Attack); chứng minh các bộ lọc đơn lượt (single-turn) hoàn toàn bất lực trước kỹ thuật khai thác ngữ cảnh tích lũy. | **Cơ sở mở rộng nhánh nghiên cứu Multi-turn State Tracking**: Luận chứng cho việc đánh đổi độ trễ để duy trì bộ nhớ phiên và phân tích trôi dạt ngữ cảnh (Contextual Drift). |
| **40. Prompt Overflow (arXiv 2026)** | [arXiv-PromptOverflow] | Zhou et al. (2026) | [Zhou_2026_Prompt_Overflow_Guardrail_Window_Mismatch.pdf](./Zhou_2026_Prompt_Overflow_Guardrail_Window_Mismatch.pdf) | Preprint nghiên cứu chênh lệch giữa phần nội dung guardrail quan sát được và nội dung LLM đích nhận trong các thiết lập được đánh giá; không khái quát rằng mọi guardrail dùng 512 token hay mọi LLM nhận 128k token. | **Ứng dụng PI-Guard**: Gợi ý kiểm thử tài liệu dài và vị trí payload; không chứng minh thiết kế chunking, độ phủ 200k ký tự hay KPI của PI-Guard. |
| <a id="ref41"></a>**41. CASCADE Against Jailbreaks (arXiv 2026)** | [arXiv-CASCADE] | Luo & Han (2026) | [Luo_2026_CASCADE_Against_Jailbreaks_Evaluation.pdf](./Luo_2026_CASCADE_Against_Jailbreaks_Evaluation.pdf) | Preprint đánh giá thực nghiệm các kết hợp tấn công/phòng thủ trong các thiết lập được mô tả; kết luận thực nghiệm không phải định lý tổng quát. | **Ứng dụng PI-Guard**: Cung cấp một điểm tham chiếu thực nghiệm cho nghiên cứu kết hợp nhiều giai đoạn; không bảo chứng kiến trúc hay KPI cụ thể của đồ án. |
| <a id="ref42"></a>**42. Hồ sơ audit thực nghiệm cục bộ (2026)** | [Local-Audit-2026] | Tài liệu nội bộ, 2026-09-29 | Tài liệu thuộc workspace cá nhân bị loại khỏi repository; không có bản chia sẻ tại đây. | Đây là hồ sơ nội bộ, không phải nguồn học thuật. Nội dung và kết quả trong đó không được viện dẫn như bằng chứng của repository. |
| <a id="ref43"></a>**43. Metadata pilot cục bộ (2026)** | [Local-Pilot-Status-2026] | Metadata nội bộ, 2026-09-29 | Metadata thuộc workspace cá nhân bị loại khỏi repository; không có bản chia sẻ tại đây. | Không nêu trạng thái chạy hay metric cục bộ trong tài liệu tham khảo được chia sẻ. |
| <a id="ref68"></a>**68. Chunk Encoding với max-pooling cho tài liệu dài (EACL 2024)** | [EACL-Chunk-MaxPool-2024] | Gomes, Coutinho & Martins (2024) | [Gomes_2024_Accurate_Well_Calibrated_ICD_Chunk_Encoding_EACL.pdf](./Gomes_2024_Accurate_Well_Calibrated_ICD_Chunk_Encoding_EACL.pdf) · [ACL Anthology](https://aclanthology.org/2024.eacl-long.141/) | Chia hồ sơ y khoa thành chunk tối đa 512 token, max-pool logits theo chunk và dùng overlap 255 token; CE tốt hơn baseline 512 token đầu trên các metric F1 của hai split được báo cáo. Tác giả cũng nêu rủi ro max-pooling làm xác suất quá cao và giảm calibration. | Bằng chứng gần cho tính khả thi của chunk-level max pooling trên văn bản dài; khác miền ICD, không bảo chứng hiệu quả PI-Guard hoặc threshold hiện tại. |
| <a id="ref69"></a>**69. So sánh Max và Noisy-or trong multiple-instance learning (Interspeech 2018)** | [ISCA-Max-NoisyOr-2018] | Wang, Li & Metze (2018) | [Wang_Li_Metze_2018_Max_Noisy_Or_Pooling_Interspeech.pdf](./Wang_Li_Metze_2018_Max_Noisy_Or_Pooling_Interspeech.pdf) · [ISCA Archive](https://www.isca-archive.org/interspeech_2018/wang18_interspeech.html) | Trong nhận dạng lời nói và phát hiện sự kiện âm thanh, max pooling định vị được sự kiện còn noisy-or thất bại trong các thiết lập nghiên cứu; tác giả phân tích tương quan giữa các bước chuỗi và giả định độc lập của noisy-or. | Nguồn nền tảng để so sánh phép gộp kiểu multiple-instance; miền âm thanh, không phải bằng chứng thực nghiệm cho văn bản hay PI-Guard. |
| <a id="ref70"></a>**70. Prompt Injection Mechanisms Dataset (Hugging Face, 2026)** | [HF-Cyberec-Mechanisms] | cyberec (2026 snapshot) | [Dataset card](https://huggingface.co/datasets/cyberec/llm-prompt-injection-attacks) | Card mô tả các nhãn cơ chế BENIGN, JAILBREAK, INSTRUCTION_OVERRIDE, ROLE_HIJACK và DATA_EXFILTRATION; nhãn heuristic. | Metadata-only screen: không có hai trục source-label PI/JB độc lập; không dùng làm BOTH. |
| <a id="ref71"></a>**71. LLM Prompt Safety Benchmark 100K (Kaggle, 2026)** | [Kaggle-Prompt-Safety-100K] | Goutam Sharma (Kaggle metadata, 2026) | [Dataset page](https://www.kaggle.com/datasets/goutamsharma12/prompt-safety-classifier-100k) | Metadata mô tả sáu lớp đơn gồm Prompt Injection, Jailbreak Attempt, Harmful Content, Social Engineering và Ambiguous Borderline. | Không có đồng nhãn PI+JB; metadata API báo CC0-1.0 nhưng mô tả nói MIT; loại khỏi L3. |
| <a id="ref72"></a>**72. LLM Prompt-Injection & Jailbreak Detection (Kaggle, 2026)** | [Kaggle-Synthetic-PI-JB] | Ahmad Zulfiqar (Kaggle metadata, 2026) | [Dataset page](https://www.kaggle.com/datasets/ahmadzulfiqar001/llm-prompt-injection-and-jailbreak-detection) | Metadata mô tả dữ liệu tổng hợp, nhãn benign hoặc một trong các kỹ thuật tấn công, cùng cờ malicious. | Kỹ thuật/cờ nhị phân không xác nhận riêng PI, JB hay BOTH; payload chưa tải. |
| <a id="ref73"></a>**73. LLM Jailbreak & Prompt-Injection Dataset (Hugging Face, 2026)** | [HF-Necent-Guardrails] | Necent (2026 snapshot) | [Dataset card](https://huggingface.co/datasets/Necent/llm-jailbreak-prompt-injection-dataset) | Card mô tả `prompt_harmful`, `prompt_adversarial` và một `prompt_type`; gated, các nguồn gốc giữ license riêng. | Không có cặp nhãn đồng thời PI+JB; prompt adversarial/harmful không tương đương taxonomy L3; không tải payload. |
| <a id="ref74"></a>**74. SALAD-Data (OpenSafetyLab, 2024)** | [HF-Salad-Data] | OpenSafetyLab (2024) | [Dataset card](https://huggingface.co/datasets/OpenSafetyLab/Salad-Data) · [paper](https://arxiv.org/abs/2402.05044) | Card mô tả base/attack-enhanced safety questions với taxonomy harm và trường phương pháp tạo tấn công. | Không có nhãn riêng PI/JB; không dùng cho subtype BOTH hoặc OTHER_ATTACK. |

| <a id="ref75"></a>**75. AgentHarm (UK AI Safety Institute, 2024)** | [HF-AgentHarm] | Andriushchenko et al. (2024; v3 2025) | [Dataset card](https://huggingface.co/datasets/ai-safety-institute/AgentHarm) · [paper](https://arxiv.org/abs/2410.09024) | Benchmark cho harmful tasks của LLM agents; card yêu cầu chỉ dùng để đánh giá và có điều khoản license bổ sung. | Không dùng train; không có source label PI+JB phù hợp L3. |
| <a id="ref76"></a>**76. LLM Jailbreak & Prompt-Injection Dataset (Hugging Face, 2026)** | [HF-Necent-Guardrails] | Necent (2026 snapshot) | [Dataset card](https://huggingface.co/datasets/Necent/llm-jailbreak-prompt-injection-dataset) | Metadata mô tả prompt_type đơn, các trục prompt_harmful/prompt_adversarial và gate yêu cầu thông tin liên hệ/người dùng. | Không có nhãn đồng thời PI+JB; không chấp thuận gate hoặc tải payload. |
| <a id="ref77"></a>**77. ToolSafe / TS-Bench (ACL Findings 2026)** | [ACL-ToolSafe] | Mou et al. (2026) | [Paper](https://aclanthology.org/2026.findings-acl.1850.pdf) · [official repo](https://github.com/MurrayTom/ToolSafe) | Benchmark gán nhãn an toàn theo bước gọi tool, kèm lịch sử tương tác và hành động dự kiến. | Không áp vào L3 prompt-only; quyền dữ liệu chưa được xác minh. |
| <a id="ref78"></a>**78. AEGINEL Guard (AEGIS Research, 2026)** | [AEGIS-AEGINEL] | Kim and AEGIS Research Team (2026) | [Technical report](https://aegis-research.yatavent.net/en/publications/aegis-tr-2026-002) · [repository](https://github.com/kwangilkimkenny/AEGINEL) | Báo cáo mô tả một bộ dữ liệu đa nhãn tự xây dựng và mô hình prompt-security. | Không có bản ghi dataset và license/provenance theo dòng được tìm thấy; không dùng dữ liệu. |
| <a id="ref79"></a>**79. ILION-Bench v2 (Zenodo, 2026)** | [Zenodo-ILION-Bench] | Chitan (2026) | [Zenodo record](https://zenodo.org/records/18929841) | Benchmark execution safety có role, trigger, proposed action, quyết định BLOCK/ALLOW và category. | Không phải tác vụ phân loại prompt PI/JB; quyền và overlap chưa kiểm toán. |
| <a id="ref80"></a>**80. L3 v0.2.1 package and trainer preflight evidence (local, 2026-10-23)** | [L3-v021-Evidence] | PI-Guard local verifier and trainer | [JSON evidence](D:/Work/Do-an/workspaces/truongnv/reports/experiment_reports/training_lessons/L3_V0_2_1_SCREENING_AND_PREFLIGHT_2026-10-23.json) | Integrity verifier passed; preflight reports train BOTH 49/100, validation BOTH 0/30, candidate BOTH 15/30. | Fit remains blocked; no candidate payload scoring or model training. |
| <a id="ref81"></a>**81. L3 v0.2.1 source-label/group support (local, 2026-10-23)** | [L3-v021-Group-Support] | PI-Guard local JSONL metadata audit | [JSON evidence](D:/Work/Do-an/workspaces/truongnv/reports/experiment_reports/training_lessons/L3_V0_2_1_SOURCE_LABEL_DISTRIBUTION_2026-10-23.json) | Counts source-mapped label rows and distinct group IDs in train/validation only. | OTHER_ATTACK validation has 36 rows from 2 CiberIA groups; row support does not imply source-diverse groups. |
| <a id="ref82"></a>**82. Bordair Multimodal Prompt Injection Dataset (Hugging Face, 2026)** | [HF-Bordair-Multimodal] | Bordair (2026 snapshot) | [Dataset card](https://huggingface.co/datasets/Bordair/bordair-multimodal) | Card describes a large multi-version corpus with binary `expected_detection` labels across PI, jailbreak, agent and multimodal scenarios. | No row-level BOTH/OTHER_ATTACK target; viewer reports incompatible columns across files and upstream component rights are not itemized per row. |
| <a id="ref83"></a>**83. AI Mitra Prompt Injection Dataset (Hugging Face, 2026)** | [HF-AIMitra-PI] | ai-mitra (2026 snapshot) | [Dataset card](https://huggingface.co/datasets/ai-mitra/prompt-injection-dataset) | Card describes a small English text corpus with binary benign/PI labels and attack-type metadata. | No separate JB or BOTH target; the card lists synthetic/template phrasing and incomplete real-world coverage as limitations. |
| <a id="ref84"></a>**84. PromptSentinel (Hugging Face, 2026)** | [HF-PromptSentinel] | Nuhman PK (2026 snapshot) | [Dataset card](https://huggingface.co/datasets/nuhmanpk/prompt-sentinel) | Card maps source datasets to mutually exclusive benign, jailbreak, and injection labels and exposes per-row source/license fields. | No BOTH class; gated access, mixed/unspecified component rights, and card-versus-split count discrepancy prevent aggregate use. |
| <a id="ref85"></a>**85. NeurAlchemy Prompt Injection and Jailbreak Dataset (Hugging Face, 2026)** | [HF-NeurAlchemy-PI-JB] | NeurAlchemy (2026 snapshot) | [Dataset card](https://huggingface.co/datasets/neuralchemy/Prompt-injection-dataset) | Card describes binary benign/malicious labels plus a single attack category such as `direct_injection` or `jailbreak`. | Existing local core train/validation audit found 13 original-source JB train rows and none in validation; mixed component rights remain unresolved. |
| <a id="ref86"></a>**86. PraneshJs Prompt_injection_safe (Hugging Face, 2026)** | [HF-Pranesh-PI-Safe] | PraneshJs (2026 snapshot) | [Dataset card](https://huggingface.co/datasets/PraneshJs/Prompt_injection_safe) | Pinned revision MIT metadata; train schema includes `label`, `topic`, `intent`; local train-only audit finds 24 PI+jailbreak pairs. | README has no collection/label method or source/group ID; validation later confirmed 9 BOTH and 21 OTHER_ATTACK candidates; test not downloaded. Used as v0.2.3 source-label proxy; support remains too low to fit. |
| <a id="ref87"></a>**87. AIDataFdn Prompt Injection Dataset (Hugging Face, 2026)** | [HF-AIDataFdn-PI] | AIDataFdn (2026 snapshot) | [Dataset card](https://huggingface.co/datasets/AIDataFdn/promptinjection) | Card reports Apache-2.0, about 734k rows, and one categorical `categories` field. | No PI+JB co-label and no tool-abuse label in the displayed taxonomy; no row-level lineage in displayed schema. |
| <a id="ref88"></a>**88. ToolSafety (EMNLP 2025)** | [ACL-ToolSafety-2025] | Xie et al. (2025) | [ACL Anthology](https://aclanthology.org/2025.emnlp-main.714/) | Dataset addresses direct harm, indirect harm, and multi-step safety in tool invocation. | Context-aware agent tool-safety task, not standalone PI/JB subtype labels. |
| <a id="ref89"></a>**89. ToolMisuseBench (arXiv, 2026)** | [arXiv-ToolMisuseBench] | Sigdel and Baral (2026) | [Paper](https://arxiv.org/abs/2604.01508) | 6,800 structured agent tasks include tool schemas, state, success criteria, fault plan, and recovery metrics. | Execution/recovery benchmark, not prompt-only attack classification. |
| <a id="ref90"></a>**90. Turkish Prompt Injection and Jailbreak Dataset (Hugging Face, 2026)** | [HF-OnerAYTAS-PI-JB] | OnerAYTAS (2026 snapshot) | [Dataset card](https://huggingface.co/datasets/OnerAYTAS/Turkish_prompt_injection_jailbreak_dataset) | Declares CC-BY-NC-SA-4.0 and bundles Turkish/English source files. | HF viewer reports incompatible CSV columns and cast failure; stable co-label schema not established. |
| <a id="ref91"></a>**91. Prompt Injection Patterns Extended (Hugging Face, 2026)** | [HF-Mukunda-Patterns] | Mukunda (2026 snapshot) | [Dataset card](https://huggingface.co/datasets/mukunda1729/prompt-injection-patterns-extended) | MIT card; 30 fixtures across labeled categories including tool-abuse and jailbreak. | Only two per category and no BOTH co-label; insufficient support. |
| <a id="ref92"></a>**92. LLM Jailbreak and Prompt-Injection Dataset (Necent, 2026)** | [HF-Necent-Guardrails] | Necent (2026 snapshot) | [Dataset card](https://huggingface.co/datasets/Necent/llm-jailbreak-prompt-injection-dataset) | Gated aggregate exposes harmful/adversarial axes and one `prompt_type`; underlying sources retain own licenses. | No separate PI/JB co-label; access gate not accepted. |
---

## 📊 2. BẢNG CHI TIẾT SIÊU DỮ LIỆU HỌC THUẬT (17 BÀI BÁO CỐT LÕI)

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
- **Tệp PDF Cục Bộ**: [`Zhao_2023_A_Survey_of_Large_Language_Models.pdf`](./Zhao_2023_A_Survey_of_Large_Language_Models.pdf) (144 trang)
- **Liên kết mở (Open-Access PDF)**: [https://arxiv.org/pdf/2303.18223.pdf](https://arxiv.org/pdf/2303.18223.pdf) | **arXiv ID**: `2303.18223`
- **Từ khóa phân loại**: `LLM Architecture`, `Autoregressive Transformers`, `Pre-training`, `Tokenization`, `Alignment`
- **Đóng góp khoa học gốc của bài báo**: Cung cấp bức tranh toàn cảnh về kiến trúc Transformer tự hồi quy, quy trình tiền huấn luyện, căn chỉnh chỉ thị và đánh giá năng lực LLM. Bài báo phân tích việc xử lý chuỗi token đồng nhất trong không gian ngôn ngữ phẳng, nơi mô hình tiếp nhận dữ liệu và chỉ thị như các token tương đương.
- **Định vị kỹ thuật & Giả thuyết thực nghiệm của PI-Guard**: **Chương 1 (Giới thiệu vấn đề)** & **Chương 2 (Cơ sở lý thuyết)** — Trong phạm vi mô hình hóa của đồ án PI-Guard, chuỗi ngữ cảnh đầu vào được biểu diễn dưới dạng chuỗi token kết hợp giữa system/instruction ($S$) và user/untrusted content ($U$), tức $X = S \mathbin{\Vert} U$. Dựa trên khảo sát của Zhao et al. về kiến trúc Transformer tự hồi quy, nhóm làm rõ bản chất mô hình: *LLM xử lý ngữ cảnh dưới dạng chuỗi token liên tục và không tự cung cấp một ranh giới an ninh đáng tin cậy (security boundary) giữa instruction và untrusted data*. Cấu trúc prompt hierarchy hay quy ước định dạng ngữ cảnh chỉ mang tính quy ước ngữ nghĩa, không tương đương với cơ chế cô lập an ninh (security isolation) cấp hệ thống, đặt ra yêu cầu tất yếu phải có giải pháp kiểm soát đầu vào độc lập đặt phía trước.

---

### <a id="ref2"></a>[2] Training Language Models to Follow Instructions with Human Feedback
- **Tên bài báo chính xác**: *Training language models to follow instructions with human feedback*
- **Tác giả**: Long Ouyang, Jeff Wu, Xu Jiang, Diogo Almeida, Carroll L. Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, John Schulman, Jacob Hilton, Fraser Kelton, Luke Miller, Maddie Simens, Amanda Askell, Peter Welinder, Paul Christiano, Jan Leike, Ryan Lowe (OpenAI)
- **Năm xuất bản**: 2022 | **Nơi công bố chính thức**: *Advances in Neural Information Processing Systems (NeurIPS 2022)*, Vol. 35, pp. 27730–27744
- **Tệp PDF Cục Bộ**: [`Ouyang_2022_InstructGPT_Training_Language_Models_Follow_Instructions.pdf`](./Ouyang_2022_InstructGPT_Training_Language_Models_Follow_Instructions.pdf) (68 trang)
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
- **Tệp PDF Cục Bộ**: [`Perez_2022_Ignore_This_Title_Hack_This_Paper_Prompt_Injection.pdf`](./Perez_2022_Ignore_This_Title_Hack_This_Paper_Prompt_Injection.pdf) (21 trang)
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
- **Tệp PDF Cục Bộ**: [`Greshake_2023_Indirect_Prompt_Injection.pdf`](./Greshake_2023_Indirect_Prompt_Injection.pdf) (28 trang)
- **Liên kết mở (Open-Access PDF)**: [https://arxiv.org/pdf/2302.12173.pdf](https://arxiv.org/pdf/2302.12173.pdf) | **arXiv ID**: `2302.12173`
- **Từ khóa phân loại**: `Indirect Prompt Injection`, `RAG Poisoning`, `Data-as-Instruction`, `Autonomous Agents Security`, `Synthetic Attacks`
- **Đóng góp khoa học gốc của bài báo**: Phát hiện và hệ thống hóa mối đe dọa *Indirect Prompt Injection*, trong đó kẻ tấn công không tương tác trực tiếp với LLM mà nhúng chỉ thị độc hại vào dữ liệu bên ngoài (trang web, email, tài liệu PDF, cơ sở tri thức RAG) mà LLM truy xuất trong quá trình xử lý, biến dữ liệu thụ động thành mã thực thi.
- **Định vị kỹ thuật & Giả thuyết thực nghiệm của PI-Guard**: **Chương 1, 2, 3** — Cơ sở khoa học chứng minh việc bảo vệ LLM không chỉ giới hạn ở prompt của người dùng cuối mà còn phải bao quát dữ liệu phi cấu trúc từ bên thứ ba. Luận giải sự cần thiết của một Guardrail Proxy đặt tại Ingress để kiểm tra mọi luồng văn bản đi vào LLM.

---

### <a id="ref5"></a>[5] Jailbroken: How Does LLM Safety Training Fail?
- **Tên bài báo chính xác**: *Jailbroken: How Does LLM Safety Training Fail?*
- **Tác giả**: Alexander Wei, Nika Haghtalab, Jacob Steinhardt (UC Berkeley)
- **Năm xuất bản**: 2023 | **Nơi công bố chính thức**: *Advances in Neural Information Processing Systems (NeurIPS 2023)*, Vol. 36
- **Tệp PDF Cục Bộ**: [`Wei_2024_Jailbroken_How_LLM_Safety_Training_Fails.pdf`](./Wei_2024_Jailbroken_How_LLM_Safety_Training_Fails.pdf) (46 trang)
- **Liên kết mở (Open-Access PDF)**: [https://arxiv.org/pdf/2307.02483.pdf](https://arxiv.org/pdf/2307.02483.pdf) | **arXiv ID**: `2307.02483`
- **Từ khóa phân loại**: `Jailbreak Failures`, `Competing Objectives`, `Mismatched Generalization`, `Safety Training Failure Modes`
- **Đóng góp khoa học gốc của bài báo**: Xác lập cơ sở lý thuyết chứng minh việc huấn luyện an toàn (Safety Fine-Tuning / RLHF) thất bại bắt nguồn từ hai nguyên nhân cốt lõi: *Competing Objectives* (xung đột giữa mục tiêu tuân thủ chỉ thị và mục tiêu an toàn) và *Mismatched Generalization* (năng lực tiền huấn luyện vượt xa phạm vi dữ liệu an toàn được căn chỉnh).
- **Định vị kỹ thuật & Giả thuyết thực nghiệm của PI-Guard**: **Chương 1** & **Chương 4** — Cung cấp bằng chứng khoa học cho thấy các biện pháp an toàn nội tại bên trong LLM luôn tồn tại điểm mù. Từ đó khẳng định tính đúng đắn của việc xây dựng lớp bảo vệ độc lập bên ngoài (External Guardrail Proxy) tách biệt khỏi quá trình sinh từ của mô hình đích.

---

### <a id="ref6"></a>[6] Securing the AI Agent: A Unified Framework for Multi-Layer Agent Red Teaming
- **Tên bài báo chính xác**: *Securing the AI Agent: A Unified Framework for Multi-Layer Agent Red Teaming*
- **Tác giả**: Yong Yang, Xing Zheng, Huiyu Wu, Huangsheng Cheng, Xiaorong Shi, Jing Guo, Bo Yang, Yi Zhou, Xiangfan Wu, Zonghao Ying (Tencent Zhuque Lab)
- **Năm xuất bản**: 2026 | **Nơi công bố chính thức**: *Tencent Technical Report* (Tháng 02/2026), *arXiv:2606.31227*
- **Tệp PDF Cục Bộ**: [`Tencent_2026_AI_Infra_Guard_MultiLayer_Agent_RedTeaming.pdf`](./Tencent_2026_AI_Infra_Guard_MultiLayer_Agent_RedTeaming.pdf) (15 trang)
- **Liên kết mở (Open-Access PDF)**: [https://arxiv.org/pdf/2606.31227.pdf](https://arxiv.org/pdf/2606.31227.pdf) | **arXiv ID**: `2606.31227`
- **Từ khóa phân loại**: `Agent Red Teaming`, `Multi-layer Architecture`, `Agent Infrastructure Security`, `Attack Operators Taxonomy`
- **Đóng góp khoa học gốc của bài báo**: Đề xuất khung kiểm thử an ninh đa tầng cho hệ thống AI Agent phân định 4 vùng (Zone 0: Prompt & Memory, Zone 1: Tool & Protocol, Zone 2: Model & Weights, Zone 3: Infrastructure) và chuẩn hóa danh mục 26 toán tử tấn công thực tế vào hạ tầng Agent.
- **Định vị kỹ thuật & Giả thuyết thực nghiệm của PI-Guard**: **Chương 1** & **Chương 3** — Đồ án PI-Guard kế thừa và khoanh vùng phạm vi bảo vệ tại Zone 0 (Prompt Gateway) nhằm chặn đứng các toán tử tấn công prompt trước khi chúng kịp tác động đến bộ nhớ ngữ cảnh và công cụ của Agent.

---

### <a id="ref7"></a>[7] Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations
- **Tên bài báo chính xác**: *Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations*
- **Tác giả**: Hakan Inan, Kartikeya Upasani, Jianfeng Chi, Rashi Rungta, Krithika Iyer, Yuning Mao, Michael Tontchev, Qing Hu, Brian Fuller, Davide Testuggine, Madian Khabsa (Meta AI)
- **Năm xuất bản**: 2023 | **Nơi công bố chính thức**: *arXiv preprint arXiv:2312.06674* (Bản tiền ấn phẩm kỹ thuật chính thức từ Meta AI)
- **Tệp PDF Cục Bộ**: [`Meta_2023_Llama_Guard_Input_Output_Safeguard.pdf`](./Meta_2023_Llama_Guard_Input_Output_Safeguard.pdf) (19 trang)
- **Liên kết mở (Open-Access PDF)**: [https://arxiv.org/pdf/2312.06674.pdf](https://arxiv.org/pdf/2312.06674.pdf) | **arXiv ID**: `2312.06674`
- **Từ khóa phân loại**: `Llama Guard`, `LLM-as-a-Judge`, `Input-Output Safeguard`, `Safety Taxonomy`, `Moderation Benchmark`
- **Đóng góp khoa học gốc của bài báo**: Giới thiệu mô hình Llama Guard (7B tham số) hoạt động như một trọng tài an toàn (LLM-as-a-Judge) kiểm duyệt cả prompt đầu vào và phản hồi đầu ra, cung cấp danh mục taxonomy an toàn chuẩn hóa gồm 6 loại rủi ro nội dung.
- **Định vị kỹ thuật & Giả thuyết thực nghiệm của PI-Guard**: **Chương 2** & **Chương 4** — Đóng vai trò là mô hình đối chuẩn cấp cao (High-end LLM Baseline). Đồ án phân tích các hạn chế của Llama Guard về độ trễ lớn (> 500ms) và tiêu tốn GPU, từ đó luận giải sự vượt trội về mặt hiệu quả kinh tế và độ trễ thấp của mô hình nhỏ tối ưu hóa trên CPU mà PI-Guard hướng tới.

---

### <a id="ref8"></a>[8] NeMo Guardrails: A Toolkit for Controllable and Safe LLM Applications with Programmable Rails
- **Tên bài báo chính xác**: *NeMo Guardrails: A Toolkit for Controllable and Safe LLM Applications with Programmable Rails*
- **Tác giả**: Traian Rebedea, Razvan Dinu, Makesh Sreedhar, Christopher Parisien, Jonathan Cohen (NVIDIA)
- **Năm xuất bản**: 2023 | **Nơi công bố chính thức**: *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing: System Demonstrations (EMNLP 2023)*, pp. 431–445
- **Tệp PDF Cục Bộ**: [`NVIDIA_2023_NeMo_Guardrails_Toolkit.pdf`](./NVIDIA_2023_NeMo_Guardrails_Toolkit.pdf) (15 trang)
- **Liên kết mở (Open-Access PDF)**: [https://arxiv.org/pdf/2310.10501.pdf](https://arxiv.org/pdf/2310.10501.pdf) | **arXiv ID**: `2310.10501`
- **Từ khóa phân loại**: `NeMo Guardrails`, `Programmable Rails`, `Colang`, `Input Rails`, `Execution Guardrails`
- **Đóng góp khoa học gốc của bài báo**: Giới thiệu bộ công cụ mã nguồn mở NeMo Guardrails cho phép định nghĩa các rào chắn an toàn (Input rails, Output rails, Dialog rails, Execution rails) bằng ngôn ngữ lập trình đặc tả Colang để kiểm soát luồng tương tác của ứng dụng LLM.
- **Định vị kỹ thuật & Giả thuyết thực nghiệm của PI-Guard**: **Chương 2** & **Chương 3** — Tham khảo mô hình kiến trúc Input Rails dạng Middleware để xây dựng Reverse Proxy đánh chặn luồng request trước khi chuyển tiếp tới LLM mục tiêu.

---

### <a id="ref9"></a>[9] DeBERTaV3: Improving DeBERTa using ELECTRA-Style Pre-Training with Gradient-Disentangled Embedding Sharing
- **Tên bài báo chính xác**: *DeBERTaV3: Improving DeBERTa using ELECTRA-Style Pre-Training with Gradient-Disentangled Embedding Sharing*
- **Tác giả**: Pengcheng He, Jianfeng Gao, Weizhu Chen (Microsoft)
- **Năm xuất bản**: 2023 | **Nơi công bố chính thức**: *The Eleventh International Conference on Learning Representations (ICLR 2023)*
- **Tệp PDF Cục Bộ**: [`He_2023_DeBERTaV3_Disentangled_Attention_ICLR.pdf`](./He_2023_DeBERTaV3_Disentangled_Attention_ICLR.pdf) (13 trang)
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
- **Tệp PDF Cục Bộ**: [`OpenAI_2023_Undesired_Content_Detection.pdf`](./OpenAI_2023_Undesired_Content_Detection.pdf) (10 trang)
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
- **Tệp PDF Cục Bộ**: [`Shen_2024_Do_Anything_Now_Jailbreak_Prompts_In_The_Wild.pdf`](./Shen_2024_Do_Anything_Now_Jailbreak_Prompts_In_The_Wild.pdf) (15 trang)
- **Liên kết mở (Open-Access PDF)**: [https://arxiv.org/pdf/2308.03825.pdf](https://arxiv.org/pdf/2308.03825.pdf) | **arXiv ID**: `2308.03825`
- **Từ khóa phân loại**: `DAN Jailbreak`, `In-the-wild Prompts`, `Jailbreak Taxonomy`, `Prohibited Scenarios`, `Empirical Measurement`
- **Đóng góp khoa học gốc của bài báo**: Nghiên cứu đo lường thực nghiệm quy mô lớn đầu tiên về các prompt jailbreak xuất hiện tự nhiên trên mạng Internet (Reddit, Discord), thu thập và công bố tập dữ liệu 1,405 prompt jailbreak thực tế trên tổng số 15,140 mẫu thu thập (~9.29% / làm tròn 9.3%), phân loại thành các họ tấn công DAN kinh điển.
- **Định vị kỹ thuật & Giả thuyết thực nghiệm của PI-Guard**: **Chương 3** & **Chương 4** — Cung cấp tập dữ liệu mẫu tấn công jailbreak thực tế chất lượng cao cho quá trình huấn luyện và kiểm thử mô hình PI-Guard.

---

### <a id="ref12"></a>[12] EasyJailbreak: A Unified Framework for Jailbreaking Large Language Models
- **Tên bài báo chính xác**: *EasyJailbreak: A Unified Framework for Jailbreaking Large Language Models*
- **Tác giả**: Weikang Zhou, Xiao Wang, Limao Xiong, Han Xia, Yingshuang Gu, Mingxu Chai, Fukang Zhu, Caishuang Huang, Shihan Dou, Zhiheng Xi, Rui Zheng, Songyang Gao, Yicheng Zou, Hang Yan, Yifan Le, Ruohui Wang, Lijun Li, Jing Shao, Tao Gui, Qi Zhang, Xuanjing Huang (Fudan University, Shanghai AI Laboratory)
- **Năm xuất bản**: 2024 | **Nơi công bố chính thức**: *arXiv preprint arXiv:2403.12171* (Đã công bố mã nguồn mở trên GitHub)
- **Tệp PDF Cục Bộ**: [`Zhou_2024_EasyJailbreak_Unified_Framework.pdf`](./Zhou_2024_EasyJailbreak_Unified_Framework.pdf) (24 trang)
- **Liên kết mở (Open-Access PDF)**: [https://arxiv.org/pdf/2403.12171.pdf](https://arxiv.org/pdf/2403.12171.pdf) | **arXiv ID**: `2403.12171`
- **Từ khóa phân loại**: `EasyJailbreak`, `Mutation Framework`, `Adversarial Robustness`, `Red Teaming Automation`, `Security Evaluation`
- **Đóng góp khoa học gốc của bài báo**: Xây dựng một framework tự động hóa quy trình jailbreak toàn diện mô phỏng 4 pha (Khởi tạo, Đột biến cấu trúc/từ vựng, Đánh giá, Chọn lọc) tích hợp 11 thuật toán jailbreak hàng đầu.
- **Định vị kỹ thuật & Giả thuyết thực nghiệm của PI-Guard**: **Chương 3** & **Chương 4** — PI-Guard sử dụng các toán tử đột biến của EasyJailbreak làm công cụ kiểm thử độ bền (fuzzing), đặt mục tiêu kiểm thử độ suy giảm hiệu năng $\Delta F_1 < 5\%$ dưới các tác vụ làm nhiễu prompt.

---

### <a id="ref13"></a>[13] Universal and Transferable Adversarial Attacks on Aligned Language Models
- **Tên bài báo chính xác**: *Universal and Transferable Adversarial Attacks on Aligned Language Models*
- **Tác giả**: Andy Zou, Zifan Wang, Nicholas Carlini, Milad Nasr, J. Zico Kolter, Matt Fredrikson (CMU, Center for AI Safety, Google DeepMind)
- **Năm xuất bản**: 2023 | **Nơi công bố chính thức**: *arXiv preprint arXiv:2307.15043* (Công trình đoạt giải Outstanding Paper Award)
- **Tệp PDF Cục Bộ**: [`Zou_2023_Universal_Transferable_Adversarial_Attacks_GCG.pdf`](./Zou_2023_Universal_Transferable_Adversarial_Attacks_GCG.pdf) (22 trang)
- **Liên kết mở (Open-Access PDF)**: [https://arxiv.org/pdf/2307.15043.pdf](https://arxiv.org/pdf/2307.15043.pdf) | **arXiv ID**: `2307.15043`
- **Từ khóa phân loại**: `Greedy Coordinate Gradient (GCG)`, `Adversarial Suffix`, `Transferable Attacks`, `Gradient-based Optimization`
- **Đóng góp khoa học gốc của bài báo**: Phát minh thuật toán Greedy Coordinate Gradient (GCG) tự động tối ưu hóa các chuỗi token hậu tố đối kháng (adversarial suffixes) có khả năng chuyển giao vạn năng (universal transferability) bẻ gãy hàng rào căn chỉnh của hầu hết các LLM thương mại lớn.
- **Định vị kỹ thuật & Giả thuyết thực nghiệm của PI-Guard**: **Chương 4** — Sử dụng các chuỗi hậu tố GCG làm tập dữ liệu kiểm thử đối kháng ngoại lai (OOD Evaluation Set) để kiểm tra khả năng phát hiện các mẫu tấn công không dựa trên ngôn ngữ tự nhiên thông thường.

---

### <a id="ref14"></a>[14] SmoothLLM: Defending Large Language Models Against Jailbreaking Attacks
- **Tên bài báo chính xác**: *SmoothLLM: Defending Large Language Models Against Jailbreaking Attacks*
- **Tác giả**: Alexander Robey, Eric Wong, Hamed Hassani, George J. Pappas (University of Pennsylvania)
- **Năm xuất bản**: 2023 | **Nơi công bố chính thức**: *arXiv preprint arXiv:2310.03684*
- **Tệp PDF Cục Bộ**: [`Robey_2023_SmoothLLM_Defending_LLMs_Random_Perturbation.pdf`](./Robey_2023_SmoothLLM_Defending_LLMs_Random_Perturbation.pdf) (36 trang)
- **Liên kết mở (Open-Access PDF)**: [https://arxiv.org/pdf/2310.03684.pdf](https://arxiv.org/pdf/2310.03684.pdf) | **arXiv ID**: `2310.03684`
- **Từ khóa phân loại**: `SmoothLLM`, `Randomized Smoothing`, `Perturbation Defense`, `Certified Robustness`, `Inference Cost Trade-off`
- **Đóng góp khoa học gốc của bài báo**: Đề xuất giải pháp phòng thủ dựa trên cơ chế làm mịn ngẫu nhiên (Randomized Smoothing): tạo ra nhiều bản sao nhiễu của prompt đầu vào, gửi truy vấn song song tới LLM và áp dụng thuật toán biểu quyết đa số để loại bỏ các tấn công đối kháng kiểu GCG.
- **Định vị kỹ thuật & Giả thuyết thực nghiệm của PI-Guard**: **Chương 2** & **Chương 4** — Là baseline đối chuẩn so sánh. Phân tích điểm yếu làm tăng độ trễ và chi phí token lên gấp $N$ lần của SmoothLLM, làm nổi bật ưu thế suy diễn một lần (single-pass) cực nhanh của mô hình PI-Guard.

---

### <a id="ref15"></a>[15] Baseline Defenses for Adversarial Attacks Against Aligned Language Models
- **Tên bài báo chính xác**: *Baseline Defenses for Adversarial Attacks Against Aligned Language Models*
- **Tác giả**: Neel Jain, Avi Schwarzschild, Yuxin Wen, Gowthami Somepalli, John Kirchenbauer, Ping-yeh Chiang, Micah Goldblum, Aniruddha Saha, Jonas Geiping, Tom Goldstein (University of Maryland)
- **Năm xuất bản**: 2023 | **Nơi công bố chính thức**: *arXiv preprint arXiv:2309.00614*
- **Tệp PDF Cục Bộ**: [`Jain_2023_Baseline_Defenses_Adversarial_Attacks_LLMs.pdf`](./Jain_2023_Baseline_Defenses_Adversarial_Attacks_LLMs.pdf) (15 trang)
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
- **Tệp PDF Cục Bộ**: [`Saltzer_1975_The_Protection_of_Information_in_Computer_Systems.pdf`](./Saltzer_1975_The_Protection_of_Information_in_Computer_Systems.pdf) (31 trang)
- **Liên kết mở (Open-Access PDF)**: [http://web.mit.edu/Saltzer/www/publications/protection/index.html](http://web.mit.edu/Saltzer/www/publications/protection/index.html)
- **Từ khóa phân loại**: `Security Principles`, `Complete Mediation`, `Economy of Mechanism`, `Defense-in-Depth`, `Open Design`
- **Đóng góp khoa học gốc của bài báo**: Công trình khoa học kinh điển của ngành An toàn Thông tin thiết lập 8 nguyên lý thiết kế hệ thống bảo vệ máy tính bất hủ (Complete Mediation, Economy of Mechanism, Least Privilege, Fail-safe Defaults, Separation of Privilege, Least Common Mechanism, Psychological Acceptability, Open Design).
- **Định vị kỹ thuật & Giả thuyết thực nghiệm của PI-Guard**: **Chương 2** & **Chương 3** — Đặt nền tảng phương pháp luận cho đề tài: Lớp bảo vệ PI-Guard đóng vai trò là cơ chế *Complete Mediation* (mọi truy vấn đầu vào đều phải được thẩm định trước khi tới LLM) và kiến trúc phân tầng *Defense-in-Depth* (kết hợp lọc cú pháp nhẹ và phân tích ngữ nghĩa sâu).

---

### <a id="ref17"></a>[17] GPT-4 Is Too Smart To Be Safe: Stealthy Chat with LLMs via Cipher
- **Tên bài báo chính xác**: *GPT-4 Is Too Smart To Be Safe: Stealthy Chat with LLMs via Cipher*
- **Tác giả**: Youliang Yuan, Wenxiang Jiao, Wenxuan Wang, Jen-tse Huang, Pinjia He, Shuming Shi, Zhaopeng Tu (Tencent AI Lab, The Chinese University of Hong Kong)
- **Năm xuất bản**: 2024 | **Nơi công bố chính thức**: *The Twelfth International Conference on Learning Representations (ICLR 2024)*
- **Tệp PDF Cục Bộ**: [`Yuan_2024_GPT4_Too_Smart_To_Be_Safe_Cipher_Jailbreak.pdf`](./Yuan_2024_GPT4_Too_Smart_To_Be_Safe_Cipher_Jailbreak.pdf) (23 trang)
- **Liên kết mở (Open-Access PDF)**: [https://arxiv.org/pdf/2308.06463.pdf](https://arxiv.org/pdf/2308.06463.pdf) | **arXiv ID**: `2308.06463`
- **Từ khóa phân loại**: `CipherChat`, `Cipher Jailbreak`, `Encoding Bypass`, `Safety Alignment Failure`, `Multilingual Safety`
- **Đóng góp khoa học gốc của bài báo**: Phát hiện lỗ hổng căn chỉnh an toàn nghiêm trọng khi sử dụng các phương pháp mã hóa phi tự nhiên (mật mã Caesar, mã Morse, Base64, ROT13) khiến LLM vượt qua cơ chế từ chối trả lời nội dung nguy hại.
- **Định vị kỹ thuật & Giả thuyết thực nghiệm của PI-Guard**: **Chương 1, 3, 4** — Minh chứng cho nhu cầu bắt buộc phải có mô-đun tiền xử lý chuẩn hóa ký tự (Unicode Normalization & Heuristic Decoding) trong PI-Guard để loại bỏ các lớp ngụy trang mã hóa trước khi đưa vào phân loại ngữ nghĩa.

---

## 🗃️ 3. KHO TÀI LIỆU MỞ RỘNG & BENCHMARK THỰC NGHIỆM ĐÃ LƯU TRỮ (12 CÔNG TRÌNH BỔ TRỢ)

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
- **Tệp PDF Cục Bộ**: [`PIGuard_2025_Prompt_Injection_Guardrail_ACL.pdf`](./PIGuard_2025_Prompt_Injection_Guardrail_ACL.pdf)
- **Bản mở toàn văn**: [ACL Anthology PDF](https://aclanthology.org/2025.acl-long.1468.pdf) | bản tiền xuất bản [arXiv:2410.22770](https://arxiv.org/pdf/2410.22770.pdf), tên cũ *InjecGuard* (chỉ lưu bản ACL 2025 trong repository).
- **Đóng góp gốc (Tier 1)**: Đề xuất PIGuard, một guardrail phát hiện prompt injection dựa trên DeBERTa-v3 và chiến lược MOF; paper báo cáo kết quả trên các benchmark được mô tả, gồm mức cải thiện 30,4% theo định nghĩa paper. Không chuyển con số này sang F1 hoặc sang protocol khác.
- **Định vị kỹ thuật & Tiếp thu của đề tài (Tier 2 & 3)**: Dùng làm baseline tham chiếu. Đồ án cần báo cáo riêng inference checkpoint, huấn luyện lại từ đầu và mọi thay đổi về dữ liệu/protocol; các mục tiêu FPR/latency là giả thuyết của đồ án.

#### 2. `InstructDetector (EMNLP Findings)`
- **Tên bài báo chính xác**: *Defending against Indirect Prompt Injection by Instruction Detection*
- **Tác giả**: Tongyu Wen, Chenglong Wang, Xiyuan Yang, Haoyu Tang, Yueqi Xie, Lingjuan Lyu, Zhicheng Dou, Fangzhao Wu
- **Venue**: *Findings of the Association for Computational Linguistics: EMNLP 2025*, pp. 19472–19487 | **DOI**: `10.18653/v1/2025.findings-emnlp.1060` | **arXiv**: `2505.06311`
- **Tệp PDF Cục Bộ**: [`Wen_2025_InstructDetector_Findings_EMNLP.pdf`](./Wen_2025_InstructDetector_Findings_EMNLP.pdf)
- **Bản mở toàn văn**: [https://arxiv.org/pdf/2505.06311.pdf](https://arxiv.org/pdf/2505.06311.pdf)
- **Đóng góp gốc (Tier 1)**: Khai thác hidden states và gradients từ các tầng của LLM instruction-tuned làm đầu vào classifier MLP để phát hiện indirect prompt injection. Phương pháp cần truy cập trạng thái bên trong mô hình.
- **Định vị kỹ thuật & Tiếp thu của đề tài (Tier 2 & 3)**: Dùng làm tài liệu tham khảo phương pháp white-box; không thể xem như guardrail proxy black-box hoặc baseline đã chạy nếu chưa có môi trường và checkpoint tương ứng.

#### 3. Prompt Guard 86M (Meta AI 2024)
- **Tên bài báo / tài liệu chính thức**: *Prompt Guard 86M: A Lightweight Input Guardrail for Jailbreak and Prompt Injection Detection* (Model Card & Technical Documentation)
- **Tác giả**: Meta AI (Purple Llama Team)
- **Venue**: *Meta AI / Purple Llama Technical Documentation & Model Card*, 2024
- **Kho lưu trữ chính thức**: [https://huggingface.co/meta-llama/Prompt-Guard-86M](https://huggingface.co/meta-llama/Prompt-Guard-86M) & [https://github.com/meta-llama/PurpleLlama/tree/main/Prompt-Guard](https://github.com/meta-llama/PurpleLlama/tree/main/Prompt-Guard)
- **Tệp PDF Cục Bộ**: [`Meta_2024_Prompt_Guard_86M_Input_Guardrail.pdf`](./Meta_2024_Prompt_Guard_86M_Input_Guardrail.pdf)
- **Bản mở toàn văn**: [https://raw.githubusercontent.com/meta-llama/PurpleLlama/main/Prompt-Guard/MODEL_CARD.md](https://raw.githubusercontent.com/meta-llama/PurpleLlama/main/Prompt-Guard/MODEL_CARD.md)
- **Đóng góp gốc (Tier 1)**: Mô hình nhúng nhẹ 86M tham số dựa trên `mDeBERTa-v3-base` huấn luyện đa tác vụ phân loại 3 lớp: Benign, Injection, Jailbreak với độ trễ thấp trên CPU.
- **Định vị kỹ thuật & Tiếp thu của đề tài (Tier 2 & 3)**: Đóng vai trò là ứng viên mô hình tham khảo Tier 2 trong Task 2 Meeting 5; PI-Guard đối chuẩn trực tiếp về kích thước mô hình, khả năng lượng hóa và tỷ lệ dương tính giả (FPR).

#### 4. `Ayub & Majumdar (CAMLIS 2024)`
- **Tên bài báo chính xác**: *Embedding-based classifiers can detect prompt injection attacks*
- **Tác giả**: Md. Ahsan Ayub, Subhabrata Majumdar (Vanderbilt University Medical Center & Vijil)
- **Venue**: *Conference on Applied Machine Learning for Information Security (CAMLIS 2024)* | **arXiv**: `2410.22284`
- **Tệp PDF Cục Bộ**: [`Ayub_2024_Towards_Robust_Detection_Prompt_Injection_CAMLIS.pdf`](./Ayub_2024_Towards_Robust_Detection_Prompt_Injection_CAMLIS.pdf)
- **Bản mở toàn văn**: [https://arxiv.org/pdf/2410.22284.pdf](https://arxiv.org/pdf/2410.22284.pdf)
- **Đóng góp gốc (Tier 1)**: Tạo embedding từ các encoder văn bản rồi huấn luyện classifier truyền thống; tác giả báo cáo Random Forest/XGBoost là các phương pháp mạnh trong thiết lập của họ. Đây không phải TF-IDF n-gram.
- **Định vị kỹ thuật & Tiếp thu của đề tài (Tier 2 & 3)**: Dùng làm bằng chứng rằng classifier truyền thống trên biểu diễn văn bản có thể được khảo sát; không gán kết quả FPR local hoặc kết luận cascade cho paper này.

---

### 3.2. Nhóm Lượng Hóa Mô Hình & Tối Ưu Hóa Độ Trễ

#### 5. `ZeroQuant (Yao et al., NeurIPS 2022)`
- **Tên bài báo**: *ZeroQuant: Efficient and Affordable Post-Training Quantization for Large-Scale Transformers*
- **Tác giả**: Zhewei Yao, Reza Yazdani Aminabadi, Minjia Zhang, Xiaoxia Wu, Conglong Li, Yuxiong He (Microsoft)
- **Venue**: *Advances in Neural Information Processing Systems (NeurIPS 2022)*, Vol. 35, pp. 27168–27183 | **arXiv**: `2206.01861`
- **PDF nguồn (không lưu cục bộ)**: [PDF nguồn](https://arxiv.org/pdf/2206.01861.pdf)
- **Bản mở toàn văn**: [https://arxiv.org/pdf/2206.01861.pdf](https://arxiv.org/pdf/2206.01861.pdf)
- **Đóng góp gốc (Tier 1)**: Khung lượng hóa phần cứng hiệu năng cao cho Transformers (PTQ INT8/FP16), nén trọng số và ma trận kích hoạt với mức suy giảm độ chính xác tối thiểu (< 0.1 perplexity).
- **Định vị kỹ thuật & Tiếp thu của đề tài (Tier 2 & 3)**: ⚠️ **GHI CHÚ LOẠI TRỪ PHẠM VI (OUT-OF-SCOPE / IA DISCIPLINE INVARIANT)**: Tài liệu tham khảo ngoài phạm vi đóng góp kỹ thuật cốt lõi của đề tài. Đồ án PI-Guard thuộc chuyên ngành An toàn Thông tin (Information Assurance - IA), tập trung nghiên cứu mô hình hóa rủi ro, phân loại phát hiện tấn công Prompt Injection / Jailbreak và kiến trúc điều phối phòng thủ phân tầng (Two-Tier Cascade), KHÔNG lựa chọn hướng tối ưu hóa kỹ thuật phần cứng hay lượng tử hóa mô hình (Hardware Quantization / Low-level Inference Optimization) làm hướng đóng góp chuyên môn.

---

### 3.3. Nhóm Dữ Liệu Benchmark, Đột Biến & Khảo Sát Mở Rộng

#### 6. `BIPIA Benchmark (Yi et al., NAACL 2024)`
- **Tên bài báo**: *Benchmarking and Defending Against Indirect Prompt Injection Attacks on Large Language Models*
- **Tác giả**: Jingwei Yi, Yueqi Xie, Bin Zhu, Keegan Hines, Emre Kiciman, Anthony Zhou, Miranda Bogen, Guangzhong Sun, Xing Xie (USTC, HKUST, Microsoft Research)
- **Venue**: *Findings of NAACL 2024*, pp. 2844–2863 | **arXiv**: `2312.14197`
- **Tệp PDF Cục Bộ**: [`Viet_2024_BIPIA_Benchmarking_Indirect_Prompt_Injection_Attacks.pdf`](./Viet_2024_BIPIA_Benchmarking_Indirect_Prompt_Injection_Attacks.pdf)
- **Bản mở toàn văn**: [https://arxiv.org/pdf/2312.14197.pdf](https://arxiv.org/pdf/2312.14197.pdf)
- **Đóng góp gốc (Tier 1)**: Bộ dữ liệu benchmark chuẩn hóa đánh giá Indirect Prompt Injection trên 5 tác vụ ứng dụng phong phú.
- **Ứng dụng PI-Guard (Tier 2 & 3)**: Cung cấp nguồn mẫu thử gián tiếp phục vụ kiểm định tính khái quát hóa và độ bền đối kháng của bộ lọc.

#### 7. `Do-Not-Answer Dataset (Wang et al., EMNLP 2023)`
- **Tên bài báo**: *Do-Not-Answer: A Dataset for Evaluating Safeguards in LLMs*
- **Tác giả**: Yuxia Wang, Haonan Li, Xudong Han, Preslav Nakov, Timothy Baldwin (LibrAI, MBZUAI, Melbourne)
- **Venue**: *Findings of EMNLP 2023*, pp. 896–908 | **arXiv**: `2308.13387`
- **Tệp PDF Cục Bộ**: [`Phuong_2023_Do_Not_Answer_Dataset_Evaluating_Safeguards.pdf`](./Phuong_2023_Do_Not_Answer_Dataset_Evaluating_Safeguards.pdf)
- **Bản mở toàn văn**: [https://arxiv.org/pdf/2308.13387.pdf](https://arxiv.org/pdf/2308.13387.pdf)
- **Đóng góp gốc (Tier 1)**: 936 prompt độc hại được phân loại theo 5 lĩnh vực rủi ro và 12 loại tác hại kiểm tra độ an toàn của guardrail.
- **Ứng dụng PI-Guard (Tier 2 & 3)**: Nguồn dữ liệu kiểm thử ranh giới từ chối và hiệu chuẩn ngưỡng phát hiện nhằm giảm tỷ lệ dương tính giả (FPR).

#### 8. `JailGuard Framework (Zhang et al., TOSEM 2025)`
- **Tên bài báo**: *JailGuard: A Universal Detection Framework for Prompt-based Attacks on LLM Systems*
- **Tác giả**: Xiaoyu Zhang, Cen Zhang, Tianlin Li, Yihao Huang, Xiaojun Jia, Ming Hu, Jie Zhang (Xi'an Jiaotong, NTU Singapore, A*STAR)
- **Venue**: *ACM Transactions on Software Engineering and Methodology (TOSEM 2025)* | **DOI**: `10.1145/3724393` | **arXiv**: `2403.02582`
- **Tệp PDF Cục Bộ**: [`Duc_2025_JailGuard_Universal_Detection_Framework_TOSEM.pdf`](./Duc_2025_JailGuard_Universal_Detection_Framework_TOSEM.pdf)
- **Bản mở toàn văn**: [https://arxiv.org/pdf/2403.02582.pdf](https://arxiv.org/pdf/2403.02582.pdf)
- **Đóng góp gốc (Tier 1)**: Framework phát hiện jailbreak dựa trên đột biến prompt và phân tích độ phân kỳ phản hồi (behavioral divergence).
- **Ứng dụng PI-Guard (Tier 2 & 3)**: Dùng làm đối chuẩn so sánh kỹ thuật đột biến và cơ chế đánh chặn đa tầng.

#### 9. `Comprehensive Study of Jailbreak Attack vs. Defense (Xu et al., ACL 2024)`
- **Tên bài báo**: *A Comprehensive Study of Jailbreak Attack versus Defense for Large Language Models*
- **Tác giả**: Zihao Xu, Yi Liu, Gelei Deng, Yuekang Li, Stjepan Picek (NTU, UNSW, TU Delft)
- **Venue**: *Findings of ACL 2024*, pp. 7432–7449 | **DOI**: `10.18653/v1/2024.findings-acl.442` | **arXiv**: `2402.13457`
- **Tệp PDF Cục Bộ**: [`Phuong_2024_ACL_Comprehensive_Study_Jailbreak_Attack_Defense.pdf`](./Phuong_2024_ACL_Comprehensive_Study_Jailbreak_Attack_Defense.pdf)
- **Bản mở toàn văn**: [https://arxiv.org/pdf/2402.13457.pdf](https://arxiv.org/pdf/2402.13457.pdf)
- **Đóng góp gốc (Tier 1)**: Nghiên cứu thực nghiệm so sánh các chiến lược tấn công jailbreak và các cơ chế phòng thủ trên nhiều mô hình LLM.
- **Ứng dụng PI-Guard (Tier 2 & 3)**: Nguồn tài liệu tham khảo đối chuẩn taxonomy các kỹ thuật jailbreak và đánh giá hiệu quả phòng vệ.

#### 10. `Exploring Vulnerabilities and Protections in LLMs Survey (Liu & Hu, 2024)`
- **Tên bài báo**: *Exploring Vulnerabilities and Protections in Large Language Models: A Survey*
- **Tác giả**: Frank Weizhen Liu, Chenhui Hu (Zscaler, Inc.)
- **Venue**: *arXiv preprint arXiv:2403.09503* (2024)
- **Tệp PDF Cục Bộ**: [`Phuong_2024_Exploring_Vulnerabilities_Protections_LLMs_Survey.pdf`](./Phuong_2024_Exploring_Vulnerabilities_Protections_LLMs_Survey.pdf)
- **Bản mở toàn văn**: [https://arxiv.org/pdf/2403.09503.pdf](https://arxiv.org/pdf/2403.09503.pdf)
- **Đóng góp gốc (Tier 1)**: Khảo sát các lỗ hổng an ninh LLM từ góc nhìn ứng dụng công nghiệp và các giải pháp bảo vệ an ninh dạng Security Gateway.
- **Ứng dụng PI-Guard (Tier 2 & 3)**: Cung cấp góc nhìn thực tiễn về triển khai Ingress Proxy và kiến trúc lọc luồng trong mạng doanh nghiệp.

#### 11. `Jailbreak Attacks and Defenses Against LLMs Survey (Yi et al., 2024)`
- **Tên bài báo**: *Jailbreak Attacks and Defenses Against Large Language Models: A Survey*
- **Tác giả**: Sibo Yi, Yule Liu, Zhen Sun, Tianshuo Cong, Xinlei He, Jiaxing Song, Ke Xu, Qi Li (Tsinghua University, HKUST)
- **Venue**: *arXiv preprint arXiv:2407.04295* (2024)
- **Tệp PDF Cục Bộ**: [`Phuong_2024_Survey_Jailbreak_Attacks_Defenses_LLMs.pdf`](./Phuong_2024_Survey_Jailbreak_Attacks_Defenses_LLMs.pdf)
- **Bản mở toàn văn**: [https://arxiv.org/pdf/2407.04295.pdf](https://arxiv.org/pdf/2407.04295.pdf)
- **Đóng góp gốc (Tier 1)**: Hệ thống hóa toàn diện bức tranh tấn công jailbreak và các giải pháp phòng thủ theo từng tầng (Pre-processing, Model Alignment, Post-processing).
- **Ứng dụng PI-Guard (Tier 2 & 3)**: Củng cố cơ sở lý luận cho kiến trúc phòng thủ phân tầng Ingress Proxy của PI-Guard trong Chương 2.

#### 12. `Phân Tích Loại Trừ Ngoài Phạm Vi: RAP-ID (Yang et al., ACL 2026)`
- **Tên bài báo**: *RAP-ID: Mechanistic Prompt Injection Detection via Impostor Behavior Analysis*
- **Tác giả**: Yuchen Yang, Lei Peng, Yujie He, Yang Yu, Zhongxin Wu, Yanlei Shi (Lenovo)
- **Venue**: *Findings of ACL 2026*, pp. 15008–15019
- **PDF nguồn (không lưu cục bộ)**: [PDF nguồn](https://aclanthology.org/2026.findings-acl.738.pdf)
- **Đánh giá của nhóm (Tier 1 & 2)**: **XÁC ĐỊNH RÕ LÀ NGOÀI PHẠM VI (OUT-OF-SCOPE)**. Do phương pháp đòi hỏi can thiệp trực tiếp vào trọng số nội bộ và forward pass của LLM đích (white-box requirement), không phù hợp với kiến trúc External Black-Box Guardrail Proxy của đồ án PI-Guard.


#### 13. PromptShield: Deployable Detection for Prompt Injection Attacks (Jacob et al., CODASPY 2025)
- **Tên bài báo**: *PromptShield: Deployable Detection for Prompt Injection Attacks*
- **Tác giả**: Dennis Jacob, Hend Alzahrani, Zhanhao Hu, Basel Alomair, David Wagner (University of California, Berkeley & KACST)
- **Venue**: *Proceedings of the 15th ACM Conference on Data and Application Security and Privacy (CODASPY 2025)*, pp. 341–352
- **DOI / URL**: DOI: 10.1145/3714393.3726501 | Open-Access: [https://arxiv.org/pdf/2501.15145.pdf](https://arxiv.org/pdf/2501.15145.pdf)
- **Tệp PDF Cục Bộ**: [Jacob_2025_PromptShield_Deployable_Detection_CODASPY.pdf](./Jacob_2025_PromptShield_Deployable_Detection_CODASPY.pdf)
- **Nguồn thẩm quyền gốc**: ACM Digital Library (CODASPY 2025 proceedings).
- **Đóng góp gốc (Tier 1)**: Thiết lập tiêu chuẩn benchmark và khung đánh giá cho các bộ phát hiện Prompt Injection có khả năng triển khai thực tế (Deployable Detection) trong phân vùng Tỷ lệ Báo động Giả cực thấp (**Low-FPR Regime**:  \le 1\%, 0.5\%, 0.1\%, 0.05\%$). Lập luận rằng ROC-AUC không phản ánh đầy đủ chất lượng detector trong vùng FPR thấp; xây dựng bộ dữ liệu PromptShield kết hợp hội thoại tự nhiên và cấu trúc ứng dụng; đề xuất kỹ thuật nội suy ngưỡng quyết định động trên ROC. Cung cấp bảng đối chuẩn thực nghiệm độc lập chỉ ra Meta PromptGuard chỉ đạt TPR 12.78% tại FPR 1% và ProtectAI v2 chỉ đạt TPR 1.97% tại FPR 1%.
- **Định vị kỹ thuật & Tiếp thu của PI-Guard (Tier 2)**: PI-Guard tiếp thu triết lý đánh giá Low-FPR của nhóm tác giả David Wagner (UC Berkeley), áp dụng kỹ thuật nội suy ngưỡng trên ROC để hiệu chuẩn ngưỡng định tuyến ba trạng thái (Tri-State Decision Engine) của Tầng 1 và Tầng 2, đảm bảo hệ thống chặn nhầm  < 1.5\%$ trước khi chuyển giao prompt đến LLM đích.
- **Mục tiêu kỹ thuật & Giả thuyết của PI-Guard (Tier 3)**: PI-Guard đặt mục tiêu đạt TPR $\ge 90\%$ tại mức FPR $\le 1.5\%$ với độ trễ suy diễn P95 $< 30\text{ms}$ trên CPU bằng kiến trúc ghép tầng (Two-Tier Cascade: Fast Syntactic Filter + Semantic Transformer).

#### 14. Bypassing LLM Guardrails: An Empirical Analysis of Evasion Attacks (Hackett et al., ACL 2025 LLMSEC)
- **Tên bài báo**: *Bypassing LLM Guardrails: An Empirical Analysis of Evasion Attacks against Prompt Injection and Jailbreak Detection Systems*
- **Tác giả**: William Hackett, Lewis Birch, Stefan Trawicki, Neeraj Suri, Peter Garraghan (Mindgard & Lancaster University)
- **Venue**: *Proceedings of The First Workshop on LLM Security (LLMSEC 2025) at ACL 2025*, pages 101–114, August 2025
- **DOI / URL**: DOI: 10.48550/arXiv.2504.11168 | Open-Access: [https://arxiv.org/pdf/2504.11168.pdf](https://arxiv.org/pdf/2504.11168.pdf) | [ACL Anthology](https://aclanthology.org/2025.llmsec-1.9/)
- **Tệp PDF Cục Bộ**: [Hackett_2025_Bypassing_LLM_Guardrails_Evasion_Attacks.pdf](./Hackett_2025_Bypassing_LLM_Guardrails_Evasion_Attacks.pdf)
- **Nguồn thẩm quyền gốc**: ACL Anthology / Workshop on LLM Security.
- **Đóng góp gốc (Tier 1)**: Đánh giá thực nghiệm toàn diện các đòn tấn công né tránh (Evasion Attacks) trên 6 hệ thống guardrail thương mại và mã nguồn mở (Azure Prompt Shield, Meta Prompt Guard 86M, ProtectAI v1 & v2, Nvidia NeMo Guard, Vijil). Khảo sát 12 kỹ thuật chèn ký tự (Emoji Smuggling, Unicode Tags, Zero-Width, Homoglyphs, Leetspeak) và 8 thuật toán AML Evasion (TextFooler, BAE, Bert-Attack, Deep Word Bug, Alzantot, PWWS, Pruthi, TextBugger). Chứng minh tỷ lệ qua mặt lên tới 100% đối với Emoji Smuggling trên cả Meta Prompt Guard và Azure Prompt Shield; chứng minh hiện tượng chuyển giao tấn công hộp đen (Transferability) từ mô hình white-box sang black-box.
- **Định vị kỹ thuật & Tiếp thu của PI-Guard (Tier 2)**: PI-Guard tiếp thu phát hiện cốt lõi về việc các mô hình dựa trên subword tokenizer bị mù trước biến dị Unicode/Emoji. Từ đó, PI-Guard chính thức thiết kế lớp tiền xử lý Heuristic Scrubber (Tầng 0) kết hợp bộ trích xuất đặc trưng Character N-Grams TF-IDF ở Tầng 1 để bắt dính các đòn biến dị ký tự trước khi đẩy vào Transformer.
- **Mục tiêu kỹ thuật & Giả thuyết của PI-Guard (Tier 3)**: PI-Guard giả định rằng sự phối hợp giữa Heuristic Scrubber + Char N-Grams (Tầng 1) và DeBERTa-v3 MOF (Tầng 2) sẽ giảm tỷ lệ tấn công né tránh thành công (ASR) của các đòn biến dị ký tự xuống $< 5\%$, triệt tiêu lỗ hổng 100% bypass của Meta Prompt Guard.

#### 15. DataSentinel: A Game-Theoretic Detection of Prompt Injection Attacks (Liu et al., IEEE S&P 2025)
- **Tên bài báo**: *DataSentinel: A Game-Theoretic Detection of Prompt Injection Attacks*
- **Tác giả**: Yupei Liu, Yuqi Jia, Jinyuan Jia, Dawn Song, Neil Zhenqiang Gong (The Pennsylvania State University, Duke University, UC Berkeley)
- **Venue**: *Proceedings of the 2025 IEEE Symposium on Security and Privacy (SP '25)*, May 2025
- **DOI / URL**: DOI: 10.1109/SP61157.2025.00250 | [Open-Prompt-Injection Code](https://github.com/liu00222/Open-Prompt-Injection)
- **Tệp PDF Cục Bộ**: [Liu_2025_DataSentinel_Game_Theoretic_Detection_Prompt_Injection.pdf](./Liu_2025_DataSentinel_Game_Theoretic_Detection_Prompt_Injection.pdf)
- **Nguồn thẩm quyền gốc**: IEEE Computer Society / IEEE S&P 2025.
- **Đóng góp gốc (Tier 1)**: Đề xuất phương pháp tiếp cận lý thuyết trò chơi Minimax để phát hiện tấn công Prompt Injection thích ứng (Adaptive Prompt Injection). Xây dựng bài toán tối ưu hóa Minimax mô phỏng trò chơi giữa kẻ tấn công thích ứng (Inner Max) và bộ phát hiện (Outer Min). Giải bài toán bằng giải thuật gradient luân phiên. Công bố bộ công cụ và benchmark Open-Prompt-Injection trên 7 nhóm tác vụ tích hợp LLM.
- **Định vị kỹ thuật & Tiếp thu của PI-Guard (Tier 2)**: PI-Guard tiếp thu cơ sở lý thuyết trò chơi Minimax của Liu et al. để mô hình hóa ranh giới an toàn đối kháng giữa Prompt Ingress và Guardrail Proxy, đồng thời tái sử dụng tập benchmark Open-Prompt-Injection làm nguồn dữ liệu kiểm thử OOD (Out-of-Distribution).
- **Mục tiêu kỹ thuật & Giả thuyết của PI-Guard (Tier 3)**: Khác với DataSentinel đòi hỏi suy diễn bằng LLM lớn (Mistral-7B, tiêu tốn tài nguyên và độ trễ cao), PI-Guard kế thừa tinh thần huấn luyện đối kháng nhưng triển khai trên kiến trúc phân loại gọn nhẹ (DeBERTa-v3 + TF-IDF) nhằm đạt mục tiêu P95 $< 30\text{ms}$ trên CPU.

#### 16. The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions (Wallace et al., OpenAI 2024 / ICLR 2025)
- **Tên bài báo**: *The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions*
- **Tác giả**: Eric Wallace, Kai Xiao, Reimar Leike, Lilian Weng, Johannes Heidecke, Alex Beutel (OpenAI)
- **Venue**: *arXiv preprint arXiv:2404.13208* (2024) | Submitted to ICLR 2025 / NeurIPS 2024 cycle
- **DOI / URL**: [https://arxiv.org/abs/2404.13208](https://arxiv.org/abs/2404.13208) | Open-Access PDF: [https://arxiv.org/pdf/2404.13208.pdf](https://arxiv.org/pdf/2404.13208.pdf)
- **Tệp PDF Cục Bộ**: [Wallace_2024_Instruction_Hierarchy_Prioritize_Privileged_Instructions.pdf](./Wallace_2024_Instruction_Hierarchy_Prioritize_Privileged_Instructions.pdf)
- **Nguồn thẩm quyền gốc**: OpenAI Technical Research / arXiv.
- **Đóng góp gốc (Tier 1)**: Hình thức hóa bài toán gốc rễ của Prompt Injection: LLM xử lý mọi chỉ thị (System Prompt, User Input, Tool Context) với quyền hạn ngang hàng. Đề xuất mô hình phân tầng quyền hạn *System > User > Tool/Data*, sử dụng dữ liệu đối kháng để huấn luyện mô hình bỏ qua chỉ thị quyền thấp khi có xung đột. Thừa nhận in-model training không thể chống lại hoàn toàn tấn công đối kháng thích ứng và làm tăng tỷ lệ từ chối quá mức (over-refusal).
- **Định vị kỹ thuật & Tiếp thu của PI-Guard (Tier 2)**: Cung cấp luận cứ khoa học then chốt chứng minh tại sao căn chỉnh nội tại trong LLM là không đủ; xác lập tính tất yếu của giải pháp Ingress Guardrail Proxy độc lập (PI-Guard) đặt bên ngoài nhằm bảo vệ mô hình theo nguyên lý Defense-in-Depth.
- **Mục tiêu kỹ thuật & Giả thuyết của PI-Guard (Tier 3)**: PI-Guard kết hợp với downstream LLM tạo nên kiến trúc phân tầng an ninh, kỳ vọng giảm thiểu over-refusal trên truy vấn an toàn và đạt tỷ lệ ngăn chặn tấn công $> 98\%$.

#### 17. JailbreakBench: An Open Robustness Benchmark for Jailbreaking Large Language Models (Chao et al., NeurIPS 2024)
- **Tên bài báo**: *JailbreakBench: An Open Robustness Benchmark for Jailbreaking Large Language Models*
- **Tác giả**: Patrick Chao, Edoardo Debenedetti, Alexander Robey, Maksym Andriushchenko, Francesco Croce, Vikash Sehwag, Edgar Dobriban, Nicolas Papernot, George J. Pappas, Florian Tramèr (UPenn, EPFL, University of Toronto, Vector Institute, ETH Zurich)
- **Venue**: *Advances in Neural Information Processing Systems 37 (NeurIPS 2024)*, Datasets and Benchmarks Track
- **DOI / URL**: [https://arxiv.org/abs/2404.01318](https://arxiv.org/abs/2404.01318) | Open-Access PDF: [https://arxiv.org/pdf/2404.01318.pdf](https://arxiv.org/pdf/2404.01318.pdf) | [GitHub](https://github.com/JailbreakBench/jailbreakbench)
- **Tệp PDF Cục Bộ**: [Chao_2024_JailbreakBench_Open_Robustness_Benchmark_NeurIPS.pdf](./Chao_2024_JailbreakBench_Open_Robustness_Benchmark_NeurIPS.pdf)
- **Nguồn thẩm quyền gốc**: NeurIPS 2024 Official Proceedings (Datasets & Benchmarks Track).
- **Đóng góp gốc (Tier 1)**: Xây dựng chuẩn benchmark mở và nhất quán đầu tiên cho jailbreaking trên LLM; công bố tập dữ liệu chuẩn JBB-Behaviors gồm 100 hành vi vi phạm an toàn; cung cấp leaderboard theo dõi các phương pháp tấn công và phòng thủ SOTA.
- **Định vị kỹ thuật & Tiếp thu của PI-Guard (Tier 2)**: PI-Guard tích hợp bộ 100 hành vi JBB-Behaviors vào quy trình kiểm thử đối chuẩn thực nghiệm, đối sánh trực tiếp với các giải pháp phòng thủ hàng đầu trên bảng xếp hạng cộng đồng.
- **Mục tiêu kỹ thuật & Giả thuyết của PI-Guard (Tier 3)**: PI-Guard đặt mục tiêu đạt độ bao phủ phát hiện (Recall) $\ge 95\%$ trên tập JBB-Behaviors dưới cả prompt gốc và biến thể đối kháng.

#### 18. Multilingual Jailbreak Challenges in Large Language Models (Deng et al., ICLR 2024)
- **Tên bài báo**: *Multilingual Jailbreak Challenges in Large Language Models*
- **Tác giả**: Yue Deng, Wenxuan Zhang, Sinno Jialin Pan, Lidong Bing (DAMO Academy, Alibaba Group, NTU Singapore)
- **Venue**: *The Twelfth International Conference on Learning Representations (ICLR 2024)*
- **DOI / URL**: [https://arxiv.org/abs/2310.06474](https://arxiv.org/abs/2310.06474) | Open-Access PDF: [https://arxiv.org/pdf/2310.06474.pdf](https://arxiv.org/pdf/2310.06474.pdf)
- **Tệp PDF Cục Bộ**: [Deng_2024_Multilingual_Jailbreak_Challenges_LLMs_ICLR.pdf](./Deng_2024_Multilingual_Jailbreak_Challenges_LLMs_ICLR.pdf)
- **Nguồn thẩm quyền gốc**: ICLR 2024 Conference Proceedings.
- **Đóng góp gốc (Tier 1)**: MultiJail có 315 prompt tiếng Anh và bản dịch tương ứng sang chín ngôn ngữ khác (3.150 prompt). Paper đo phản hồi jailbreak của LLM; tập này không phải benchmark phân loại prompt injection.
- **Định vị kỹ thuật & Tiếp thu của PI-Guard (Tier 2)**: Có thể tham khảo để thiết kế đánh giá jailbreak đa ngôn ngữ; kết quả không chứng minh bộ phân loại PI-Guard hoạt động trên tiếng Việt, và bản dịch cần được kiểm định nhãn trước khi dùng.
- **Mục tiêu kỹ thuật & Giả thuyết của PI-Guard (Tier 3)**: PI-Guard giả định rằng bộ lọc Tầng 1 (Character n-grams) kết hợp tiền xử lý chuẩn hóa duy trì mức suy giảm hiệu năng $\Delta F_1 < 5\%$ khi chuyển giao sang tập tấn công dịch thuật tiếng Việt.

#### 19. Conformal Risk Control & Certified Safe LLM Generation (Angelopoulos et al. 2024 / Kang et al., NeurIPS 2025)
- **Tên bài báo**: *Conformal Risk Control* & *C-SafeGen: Certified Safe LLM Generation with Claim-Based Streaming Guardrails*
- **Tác giả**: Anastasios N. Angelopoulos, Stephen Bates, Emmanuel J. Candès, Michael I. Jordan, Lihua Lei (Harvard, UC Berkeley, Stanford) & Mintong Kang, Zhaorun Chen, Bo Li (UIUC)
- **Venue**: *arXiv:2208.02814* (Angelopoulos et al., 2024) / *Advances in Neural Information Processing Systems (NeurIPS 2025)* (Kang et al.)
- **DOI / URL**: [https://arxiv.org/abs/2208.02814](https://arxiv.org/abs/2208.02814) | Open-Access PDF: [https://arxiv.org/pdf/2208.02814.pdf](https://arxiv.org/pdf/2208.02814.pdf)
- **PDF nguồn (không lưu cục bộ)**: [PDF nguồn](https://arxiv.org/pdf/2208.02814.pdf)
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
- **PDF nguồn (không lưu cục bộ)**: [PDF nguồn](https://arxiv.org/pdf/2412.13663.pdf)
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
- **Tệp PDF Cục Bộ**: [Padhi_2024_Granite_Guardian_Content_Safety_Risk_Detection.pdf](./Padhi_2024_Granite_Guardian_Content_Safety_Risk_Detection.pdf)
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
- **Tệp PDF Cục Bộ**: [Russinovich_2024_Crescendo_MultiTurn_Jailbreak_Attack.pdf](./Russinovich_2024_Crescendo_MultiTurn_Jailbreak_Attack.pdf)
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
- **Tệp PDF Cục Bộ**: [Zhou_2026_Prompt_Overflow_Guardrail_Window_Mismatch.pdf](./Zhou_2026_Prompt_Overflow_Guardrail_Window_Mismatch.pdf)
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
- **Tệp PDF Cục Bộ**: [Luo_2026_CASCADE_Against_Jailbreaks_Evaluation.pdf](./Luo_2026_CASCADE_Against_Jailbreaks_Evaluation.pdf)
- **Nguồn thẩm quyền gốc**: arXiv preprint / NUS Computing Technical Report.
- **Đóng góp gốc (Tier 1)**: Preprint báo cáo đánh giá thực nghiệm các tổ hợp phòng thủ qua nhiều kỹ thuật tấn công và cơ chế phòng thủ được nêu; kết luận thực nghiệm bị giới hạn bởi thiết lập nghiên cứu, không phải định lý tổng quát.
- **Định vị kỹ thuật & Tiếp thu của PI-Guard (Tier 2)**: Có thể dùng làm điểm đối chiếu khi đánh giá tổ hợp phòng thủ; paper không kiểm định hoặc bảo chứng cascade cụ thể của đồ án.
- **Mục tiêu kỹ thuật & Giả thuyết của PI-Guard (Tier 3)**: Đạt điểm cân bằng Pareto tối ưu trên CPU (P95 Latency < 30ms, FPR < 1.5%, F1 > 0.95), giải phóng trên 80% lưu lượng tại Tầng 1 và chỉ chuyển tiếp dưới 20% truy vấn bất định lên Tầng 2.

---

### <a id="ref46"></a>[46] ProtectAI DeBERTa-v3 prompt-injection model card
- **Mô hình / phiên bản**: `protectai/deberta-v3-base-prompt-injection-v2`, revision `90c9989b1a342275dd0d1a95aad283c04e075671`.
- **Nguồn thẩm quyền**: [Hugging Face model card at the pinned revision](https://huggingface.co/protectai/deberta-v3-base-prompt-injection-v2/tree/90c9989b1a342275dd0d1a95aad283c04e075671).
- **Bản sao model card cục bộ**: thuộc workspace cá nhân và không nằm trong repository này; dùng model card công khai ở trên làm nguồn.
- **Reporting note**: The pre-trained ProtectAI checkpoint was used for benign/injection inference; it is not a project-trained model.

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

### <a id="ref62"></a>[62] PromptScreen v1 — TF-IDF + Linear SVM paper and pinned code
- **Bài báo**: Akshaj Prashanth Rao, Advait Singh, Saumya Kumaar Saksena, Dhruv Kumar, *Efficient Jailbreak Mitigation Using Semantic Linear Classification in a Multi-Staged Pipeline*, arXiv:2512.19011v1 (2025), [v1 PDF](https://arxiv.org/pdf/2512.19011v1), [arXiv version record](https://arxiv.org/abs/2512.19011).
- **Mã nguồn**: [dronefreak/PromptScreen at pinned commit `496653aba7a39ae6bdcb775c067a3bdb2471acc7`](https://github.com/dronefreak/PromptScreen/tree/496653aba7a39ae6bdcb775c067a3bdb2471acc7); repository includes Apache-2.0 license.
- **Ranh giới bằng chứng**: v1 paper describes three labels, but the pinned saved-checkpoint training code maps `prompt-injection` to `jailbreak`, yielding a binary checkpoint. The current arXiv record is v3 with a different title and status “Under Review”; peer-reviewed acceptance is not verified.

### <a id="ref63"></a>[63] scikit-learn — common pitfalls: data leakage
- **Nguồn tài liệu chính thức**: [Common pitfalls and recommended practices, section 12.2](https://scikit-learn.org/stable/common_pitfalls.html#data-leakage).
- **Phạm vi áp dụng**: mô tả rò rỉ khi thông tin test ảnh hưởng đến quá trình xây dựng/chọn mô hình; khuyến nghị tách train/test trước preprocessing và không gọi `fit`/`fit_transform` trên test.

### <a id="ref64"></a>[64] scikit-learn — tuning the decision threshold
- **Nguồn tài liệu chính thức**: [Tuning the decision threshold for class prediction](https://scikit-learn.org/stable/modules/classification_threshold.html).
- **Phạm vi áp dụng**: phân biệt checkpoint đã fit với bước chọn threshold trên validation riêng; tài liệu cảnh báo không dùng lại cùng dữ liệu train để fit model và tune threshold.

### <a id="ref65"></a>[65] PyTorch — inference mode
- **Nguồn tài liệu chính thức**: [torch.inference_mode](https://docs.pytorch.org/docs/stable/generated/torch.autograd.grad_mode.inference_mode.html).
- **Phạm vi áp dụng**: inference-mode execution disables autograd recording for inference computations; it is evidence about the local execution path, not a claim about upstream checkpoint training.

### <a id="ref66"></a>[66] PyTorch — module evaluation mode
- **Nguồn tài liệu chính thức**: [torch.nn.Module.eval](https://docs.pytorch.org/docs/stable/notes/autograd.html#evaluation-mode-nn-module-eval).
- **Phạm vi áp dụng**: switches modules such as Dropout/BatchNorm into evaluation behavior; `eval()` alone does not prove weights cannot be updated, so it must be read together with the absence of optimizer/gradient updates in the runner.

### <a id="ref67"></a>[67] Microsoft DeBERTa-v3-base — official pretrained checkpoint
- **Nguồn phát hành**: [Hugging Face model card](https://huggingface.co/microsoft/deberta-v3-base) and immutable [revision `8ccc9b6f36199bec6961081d44eb72fb3f7353f3`](https://huggingface.co/microsoft/deberta-v3-base/tree/8ccc9b6f36199bec6961081d44eb72fb3f7353f3).
- **Metadata checked 2026-10-06**: public, ungated repository; model card declares MIT license. Local starting point downloads the PyTorch weights and matching config/tokenizer files only, excluding TensorFlow and Rust duplicate formats.
- **Scope boundary**: this is a pretrained base encoder, not a PI-Guard-fine-tuned checkpoint and not evidence that any project dataset has been fitted.
---

### <a id="ref57"></a>[57] Akinrele and Gowda (2026) — Prompt Injection Detection is Regime-Dependent
- **Authors**: Akindoyin Akinrele and Shreyank N. Gowda.
- **Venue/version**: arXiv:2605.26999v1, submitted 2026-05-26; open-access preprint.
- **Official record**: [arXiv abstract](https://arxiv.org/abs/2605.26999) | [HTML paper](https://arxiv.org/html/2605.26999).
- **Local PDF**: [Akinrele_Gowda_2026_Regime_Dependent_Prompt_Injection_arXiv2605.26999v1.pdf](Akinrele_Gowda_2026_Regime_Dependent_Prompt_Injection_arXiv2605.26999v1.pdf); SHA-256 `4431bfb137935b457211c5ecb3d184e975fed38b21b9fd13116c3611a9b7c62f`.
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

### <a id="ref68"></a>[68] Accurate and Well-Calibrated ICD Code Assignment Through Attention Over Diverse Label Embeddings
- **Tác giả**: Goncalo Gomes, Isabel Coutinho, Bruno Martins.
- **Năm và nơi công bố**: 2024, *Proceedings of the 18th Conference of the European Chapter of the Association for Computational Linguistics (Volume 1: Long Papers)*, trang 2302–2315.
- **DOI**: [10.18653/v1/2024.eacl-long.141](https://doi.org/10.18653/v1/2024.eacl-long.141).
- **Nguồn chính thức và PDF**: [ACL Anthology](https://aclanthology.org/2024.eacl-long.141/) · [PDF Open Access](./Gomes_2024_Accurate_Well_Calibrated_ICD_Chunk_Encoding_EACL.pdf).
- **Phạm vi phát hiện gốc**: phân loại mã ICD trên hồ sơ y khoa MIMIC-III; Chunk Encoding chạy encoder độc lập trên chunk 512 token, max-pool kết quả và dùng overlap 255 token.
- **Kết quả và giới hạn dùng trong PI-Guard**: CE có F1 cao hơn baseline 512 token đầu trong các thiết lập được báo cáo. Thay đổi bao gồm độ phủ tài liệu dài và thành phần kiến trúc; không quy toàn bộ khác biệt cho phép pooling và không suy ra hiệu năng prompt injection. Tác giả ghi nhận max-pooling có thể làm xác suất quá cao và ảnh hưởng calibration.

### <a id="ref69"></a>[69] Comparing the Max and Noisy-Or Pooling Functions in Multiple Instance Learning for Weakly Supervised Sequence Learning Tasks
- **Tác giả**: Yun Wang, Juncheng Li, Florian Metze.
- **Năm và nơi công bố**: 2018, *Proceedings of Interspeech 2018*, trang 1339–1343.
- **DOI**: [10.21437/Interspeech.2018-990](https://doi.org/10.21437/Interspeech.2018-990).
- **Nguồn chính thức và PDF**: [ISCA Archive](https://www.isca-archive.org/interspeech_2018/wang18_interspeech.html) · [PDF Open Access](./Wang_Li_Metze_2018_Max_Noisy_Or_Pooling_Interspeech.pdf).
- **Phạm vi phát hiện gốc**: so sánh phép gộp max và noisy-or trên nhận dạng lời nói và phát hiện sự kiện âm thanh với nhãn yếu.
- **Giới hạn dùng trong PI-Guard**: hỗ trợ thảo luận lựa chọn pooling ở mức multiple-instance, không chứng minh raw logit-margin max cho văn bản; noisy-or cần cách hiểu xác suất và các giả định về phụ thuộc cần được kiểm tra.
### <a id="ref70"></a>[70] Prompt Injection Mechanisms Dataset — Hugging Face
- **Nguồn chính thức**: [Hugging Face dataset card](https://huggingface.co/datasets/cyberec/llm-prompt-injection-attacks); metadata revision `a3d05895270cac0e553206c95463061c9bfb899f`.
- **Taxonomy công bố**: `BENIGN`, `JAILBREAK`, `INSTRUCTION_OVERRIDE`, `ROLE_HIJACK`, `DATA_EXFILTRATION`; card gọi đây là nhãn cơ chế được tái gán bằng heuristic.
- **Giới hạn dùng trong L3**: Không có trường nhãn PI và JB độc lập cùng co-label; không đủ bằng chứng để gán BOTH.

### <a id="ref71"></a>[71] LLM Prompt Safety Benchmark 100K — Kaggle
- **Nguồn metadata**: [Kaggle dataset page](https://www.kaggle.com/datasets/goutamsharma12/prompt-safety-classifier-100k); Kaggle API metadata và file listing được chụp cục bộ ngày 2026-10-23.
- **Schema mô tả**: sáu lớp prompt safety gồm Benign, Prompt Injection, Jailbreak Attempt, Harmful Content Request, Social Engineering và Ambiguous Borderline; mỗi dòng có một `label`.
- **Giới hạn dùng trong L3**: Không có nhãn đồng xuất PI+JB. Không ánh xạ Ambiguous Borderline thành OTHER_ATTACK vì lớp đó không biểu thị tool abuse/misuse. License bất nhất: Kaggle API trả CC0-1.0, mô tả nhúng khai MIT.

### <a id="ref72"></a>[72] LLM Prompt-Injection & Jailbreak Detection — Kaggle
- **Nguồn metadata**: [Kaggle dataset page](https://www.kaggle.com/datasets/ahmadzulfiqar001/llm-prompt-injection-and-jailbreak-detection); Kaggle API metadata và file listing được chụp cục bộ ngày 2026-10-23.
- **Schema mô tả**: dữ liệu tổng hợp với `label` benign hoặc một kỹ thuật tấn công và `is_malicious`; card liệt kê kỹ thuật như instruction override, role-play, refusal suppression, obfuscation và indirect injection.
- **Giới hạn dùng trong L3**: Nhãn kỹ thuật và cờ malicious không định nghĩa riêng hai trục PI/JB. Payload chưa tải hoặc đánh giá; license metadata CC0-1.0.

### <a id="ref73"></a>[73] LLM Jailbreak & Prompt-Injection Dataset — Hugging Face
- **Nguồn chính thức**: [Hugging Face dataset card](https://huggingface.co/datasets/Necent/llm-jailbreak-prompt-injection-dataset); metadata revision `4edfb5aeaafe58c9bf489a478a42188f239d7c1e`.
- **Schema mô tả**: `prompt_harmful`, `prompt_adversarial`, `prompt_type` và các trường đáp ứng; repo yêu cầu đăng nhập/chấp thuận gate và card nêu từng upstream source giữ license riêng.
- **Giới hạn dùng trong L3**: `prompt_harmful` kết hợp `prompt_adversarial` không biểu thị PI+JB đồng thời; không nhận gated payload.

### <a id="ref74"></a>[74] SALAD-Data — OpenSafetyLab
- **Nguồn chính thức**: [Hugging Face dataset card](https://huggingface.co/datasets/OpenSafetyLab/Salad-Data) và [SALAD-Bench paper](https://arxiv.org/abs/2402.05044); metadata revision `d21a325e276a99bd69b1fbb8aa51a9f249486b72`.
- **Schema mô tả**: safety question, attack/defense-enhanced question, phương pháp tạo và taxonomy harm nhiều cấp.
- **Giới hạn dùng trong L3**: không có nhãn nguồn riêng PI, JB hoặc tool abuse; không dùng cho subtype supervision.

---

### <a id="ref75"></a>[75] AgentHarm — UK AI Safety Institute
- **Nguồn chính thức**: [Hugging Face dataset card](https://huggingface.co/datasets/ai-safety-institute/AgentHarm) và [paper](https://arxiv.org/abs/2410.09024).
- **Giới hạn dùng trong L3**: Card yêu cầu chỉ dùng cho evaluation; benchmark đo harmfulness của agent tasks, không cung cấp nhãn nguồn PI+JB phù hợp subtype prompt-only. Không tải payload.

### <a id="ref76"></a>[76] LLM Jailbreak & Prompt-Injection Dataset — Necent
- **Nguồn chính thức**: [Hugging Face card](https://huggingface.co/datasets/Necent/llm-jailbreak-prompt-injection-dataset), metadata revision 4edfb5aeaafe58c9bf489a478a42188f239d7c1e.
- **Schema/access**: prompt_type là một category; prompt_adversarial và prompt_harmful không phân biệt PI với JB. Gate yêu cầu thông tin liên hệ và intended use. Không chấp thuận gate, không tải payload; upstream licenses khác nhau.

### <a id="ref77"></a>[77] ToolSafe / TS-Bench
- **Nguồn chính thức**: [ACL Findings paper](https://aclanthology.org/2026.findings-acl.1850.pdf) và [official repository](https://github.com/MurrayTom/ToolSafe).
- **Giới hạn dùng trong L3**: Nhãn ở mức bước gọi tool, cần interaction history/candidate action; paper không định nghĩa JB axis. Rights của data chưa được xác minh. Không tải payload.

### <a id="ref78"></a>[78] AEGINEL Guard
- **Nguồn chính thức**: AEGIS Research [technical report](https://aegis-research.yatavent.net/en/publications/aegis-tr-2026-002) và [linked public repository](https://github.com/kwangilkimkenny/AEGINEL).
- **Giới hạn dùng trong L3**: Report nói có custom multi-label dataset, nhưng public repo listing không có row-level corpus và không tìm thấy dataset license/provenance theo dòng. Không dùng dữ liệu.

### <a id="ref79"></a>[79] ILION-Bench v2
- **Nguồn chính thức**: [Zenodo record](https://zenodo.org/records/18929841).
- **Giới hạn dùng trong L3**: Benchmark quyết định cho proposed agent actions (BLOCK/ALLOW), không phải subtype label cho prompt-only PI/JB. Chưa kiểm toán license và overlap; không tải payload.

### <a id="ref80"></a>[80] Local L3 v0.2.1 package and trainer preflight evidence
- **Artifact**: [JSON verification record](D:/Work/Do-an/workspaces/truongnv/reports/experiment_reports/training_lessons/L3_V0_2_1_SCREENING_AND_PREFLIGHT_2026-10-23.json).
- **Result**: package integrity passed; support gate blocks fit because train BOTH=49/100, validation BOTH=0/30, and source-heldout candidate BOTH=15/30. Candidate remains unscored; training was not performed.

### <a id="ref81"></a>[81] Local L3 v0.2.1 source-label/group support
- **Artifact**: [Source distribution JSON](D:/Work/Do-an/workspaces/truongnv/reports/experiment_reports/training_lessons/L3_V0_2_1_SOURCE_LABEL_DISTRIBUTION_2026-10-23.json).
- **Scope**: counts source, labels, and distinct groups in train/validation only; prompt text and the source-heldout candidate were not read.
- **Finding**: OTHER_ATTACK has 180 train rows from 52 groups and 36 validation rows from only 2 CiberIA groups; BOTH validation support is zero.

### <a id="ref82"></a>[82] Bordair Multimodal Prompt Injection Dataset
- **Nguồn chính thức**: [Hugging Face dataset card](https://huggingface.co/datasets/Bordair/bordair-multimodal).
- **Giới hạn dùng trong L3**: target `expected_detection` chỉ có attack/benign; trang dataset hiện báo lỗi cast do các file có tập cột khác nhau. Không ánh xạ taxonomy rộng thành BOTH/OTHER_ATTACK.

### <a id="ref83"></a>[83] AI Mitra Prompt Injection Dataset
- **Nguồn chính thức**: [Hugging Face dataset card](https://huggingface.co/datasets/ai-mitra/prompt-injection-dataset).
- **Giới hạn dùng trong L3**: binary benign/prompt-injection; field `attack_type` không cung cấp nhãn JB hoặc BOTH.

### <a id="ref84"></a>[84] PromptSentinel
- **Nguồn chính thức**: [Hugging Face dataset card](https://huggingface.co/datasets/nuhmanpk/prompt-sentinel).
- **Giới hạn dùng trong L3**: nhãn benign, jailbreak, injection loại trừ nhau; không có co-label BOTH. Snapshot audit ghi quyền thành phần chưa rõ ở một số dòng và sai khác số lượng giữa card với splits.

### <a id="ref85"></a>[85] NeurAlchemy Prompt Injection and Jailbreak Dataset
- **Nguồn chính thức**: [Hugging Face dataset card](https://huggingface.co/datasets/neuralchemy/Prompt-injection-dataset); snapshot local revision `7d70432dfcf47a821612cbf9d34e9d9e3ad20e75`.
- **Giới hạn dùng trong L3**: `core` dùng binary target và một category mỗi dòng. Metadata subset `source=original` quá nhỏ để đáp ứng BOTH; các thành phần khác có điều khoản khác nhau.


### <a id="ref86"></a>[86] PraneshJs Prompt_injection_safe
- **Nguồn chính thức**: [Hugging Face dataset card](https://huggingface.co/datasets/PraneshJs/Prompt_injection_safe), pinned revision `3ec6843a3f7ac19d039731ecd448741287757385`; card metadata declares MIT.
- **Giới hạn dùng trong L3**: train-only audit found 24 source-labeled PI+jailbreak pairs and 93 strict tool-abuse candidates before overlap checks. README has no collection/labeling method and schema has no row or group IDs. Validation was later downloaded and screened; test was not downloaded. The 24 train and 9 validation BOTH examples plus strict tool-abuse candidates are source-label proxies, not gold. L3 v0.2.3 uses 117 train and 30 validation rows under the approved mapping; the fit gate remains closed.

### <a id="ref87"></a>[87] AIDataFdn Prompt Injection Dataset
- **Nguồn chính thức**: [Hugging Face dataset card](https://huggingface.co/datasets/AIDataFdn/promptinjection).
- **Giới hạn dùng trong L3**: one categorical field separates named categories but does not provide simultaneous PI+JB labels or a tool-abuse class in the displayed taxonomy.

### <a id="ref88"></a>[88] ToolSafety
- **Nguồn chính thức**: [ACL Anthology paper](https://aclanthology.org/2025.emnlp-main.714/).
- **Giới hạn dùng trong L3**: direct/indirect harm and multi-step tool-invocation safety target contextual agent workflows, not standalone PI/JB subtype labels.

### <a id="ref89"></a>[89] ToolMisuseBench
- **Nguồn chính thức**: [arXiv paper](https://arxiv.org/abs/2604.01508).
- **Giới hạn dùng trong L3**: structured records include agent instructions, tool schemas, state, success criteria, and fault plans; this measures tool execution/recovery rather than prompt-only attack labels.

### <a id="ref90"></a>[90] Turkish Prompt Injection and Jailbreak Dataset
- **Nguồn chính thức**: [Hugging Face dataset card](https://huggingface.co/datasets/OnerAYTAS/Turkish_prompt_injection_jailbreak_dataset).
- **Giới hạn dùng trong L3**: bundled files fail the HF schema cast because their columns differ; no stable shared co-label contract was established.

### <a id="ref91"></a>[91] Prompt Injection Patterns Extended
- **Nguồn chính thức**: [Hugging Face dataset card](https://huggingface.co/datasets/mukunda1729/prompt-injection-patterns-extended).
- **Giới hạn dùng trong L3**: only 30 rows total with two tool-abuse and two jailbreak examples; cannot support class minima.

### <a id="ref92"></a>[92] Necent LLM Jailbreak and Prompt-Injection Dataset
- **Nguồn chính thức**: [Hugging Face dataset card](https://huggingface.co/datasets/Necent/llm-jailbreak-prompt-injection-dataset).
- **Giới hạn dùng trong L3**: gated; `prompt_harmful` and `prompt_adversarial` are not independent PI/JB axes, and the aggregate retains each upstream source license.
## 📑 4. ĐẦY ĐỦ CÁC MỤC TRÍCH DẪN BIBTEX CHUẨN IEEE (FACT-CHECKED BIBTEX REPOSITORY)

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

@inproceedings{gomes2024chunkmaxpool,
  author    = {Gomes, Goncalo and Coutinho, Isabel and Martins, Bruno},
  title     = {Accurate and Well-Calibrated {ICD} Code Assignment Through Attention Over Diverse Label Embeddings},
  booktitle = {Proceedings of the 18th Conference of the European Chapter of the Association for Computational Linguistics (Volume 1: Long Papers)},
  pages     = {2302--2315},
  year      = {2024},
  publisher = {Association for Computational Linguistics},
  doi       = {10.18653/v1/2024.eacl-long.141},
  url       = {https://aclanthology.org/2024.eacl-long.141/}
}

@inproceedings{wang2018maxnoisyor,
  author    = {Wang, Yun and Li, Juncheng and Metze, Florian},
  title     = {Comparing the Max and Noisy-Or Pooling Functions in Multiple Instance Learning for Weakly Supervised Sequence Learning Tasks},
  booktitle = {Proceedings of Interspeech 2018},
  pages     = {1339--1343},
  year      = {2018},
  doi       = {10.21437/Interspeech.2018-990},
  url       = {https://www.isca-archive.org/interspeech_2018/wang18_interspeech.html}
}
```


## Supplementary Dataset Sources for L3 Screening (2026-10-23)

These numbered dataset and benchmark sources support local round-11 screening claims. They are source cards/API metadata, not academic papers, and none was admitted to an L3 split.

<a id="ref93"></a>[93] Hugging Face [AI Agent Evasion Dataset](https://huggingface.co/datasets/darkknight25/AI_Agent_Evasion_Dataset); malicious/benign and one attack-type field; MIT declared.

<a id="ref94"></a>[94] Hugging Face [Rogue Security Coding-Agent Security Benchmark](https://huggingface.co/datasets/rogue-security/coding-agent-security-benchmark); mixed-role test messages; CC-BY-NC-4.0.

<a id="ref95"></a>[95] Tencent/CUHK-Shenzhen [SkillTrustBench](https://matrix.tencent.com/skilltrustbench/dataset); malicious skill artifacts, not user prompts.

<a id="ref96"></a>[96] GitHub [Bordair Multimodal Prompt Injection Dataset](https://github.com/n1ps/bordair-dataset); binary expected-detection target; license unresolved in this screen.

<a id="ref97"></a>[97] Hugging Face [AgentInjectionBench](https://huggingface.co/datasets/sincpp/AgentInjectionBench); agentic conversation and tool-output injection benchmark.

<a id="ref98"></a>[98] Hugging Face [Cyberec Prompt-injection-dataset](https://huggingface.co/datasets/cyberec/Prompt-injection-dataset); binary target and one attack-mechanism category per row.

<a id="ref99"></a>[99] Hugging Face [Realistic Prompt Injections](https://huggingface.co/datasets/treycsa/realistic-prompt-injections); 17-row detector probe.

<a id="ref100"></a>[100] Hugging Face [Mindgard evaded prompt-injection and jailbreak samples](https://huggingface.co/datasets/Mindgard/evaded-prompt-injection-and-jailbreak-samples); gated; CC-BY-NC-4.0.

<a id="ref101"></a>[101] Hugging Face [Horizon-Labs prompt-injection-eval-suite](https://huggingface.co/datasets/Horizon-Labs/prompt-injection-eval-suite); mixed per-config license and evaluation subsets.

<a id="ref102"></a>[102] Hugging Face [Rogue Security prompt-injections benchmark](https://huggingface.co/datasets/rogue-security/prompt-injections-benchmark); jailbreak/benign; CC-BY-NC-4.0.

<a id="ref103"></a>[103] Kaggle [Prompt Injection & Jailbreak Detection Dataset](https://www.kaggle.com/datasets/krishnayadav456wrsty/prompt-injection-and-jailbreak-detection-dataset); Kaggle API metadata and file listing in round 11.

<a id="ref104"></a>[104] Kaggle [LLM Prompt-Injection & Jailbreak Detection](https://www.kaggle.com/datasets/ahmadzulfiqar001/llm-prompt-injection-and-jailbreak-detection); round-11 metadata reconfirms the round-7 screen.

<a id="ref105"></a>[105] Kaggle [AI Agent Cybersecurity Dataset 2026](https://www.kaggle.com/datasets/chuneeb/ai-agent-cybersecurity-dataset-2026); API metadata and file listing in round 11.

<a id="ref106"></a>[106] Kaggle [LLM Agent Failure Analysis Benchmark](https://www.kaggle.com/datasets/sunil123kumar/ai-agent-failure-benchmark-dataset); API metadata and file listing in round 11.

<a id="ref107"></a>[107] Hugging Face [SCAS](https://huggingface.co/datasets/saibhossain/SCAS) and Kaggle [SCAS](https://www.kaggle.com/datasets/saibhossain/scas-signed-context-attack-suite); context/action scenario schema; licensing evidence requires clarification.

## Supplemental Dataset Sources for L3 Screening (round 12, 2026-10-23)

These dataset cards, metadata snapshots, and benchmark repositories support the local round-12 screening record. One AgentExploitDB JSONL was quarantined for aggregate duplication analysis; no screened source was admitted to an L3 split.

<a id="ref108"></a>[108] Kaggle [AgentExploitDB AI Agent Security Benchmark 2026](https://www.kaggle.com/datasets/beatsprom/agentexploitdb-ai-agent-security-benchmark-2026); metadata, file listing, quarantined JSONL, and template-group audit captured locally.

<a id="ref109"></a>[109] Kaggle [Prompt Safety Agent Guardrail Classifier 100k](https://www.kaggle.com/datasets/goutamsharma12/prompt-safety-classifier-100k); metadata and local README/schema/annotation-guideline snapshots; Kaggle and README license statements differ.

<a id="ref110"></a>[110] Kaggle [X-Guard-Bench](https://www.kaggle.com/datasets/nidalshahin/x-guard-bench); evaluation-set metadata and CC-BY-NC-SA-4.0 declaration.

<a id="ref111"></a>[111] Kaggle [AI Safety Dataset](https://www.kaggle.com/datasets/mmumairkhattak/ai-safety-dataset); dataset metadata and file listing.

<a id="ref112"></a>[112] Kaggle [Fine-tuning Dataset for LLM Security](https://www.kaggle.com/datasets/hilalkavas/fine-tuning-dataset-for-llm-security); dataset metadata and file listing.

<a id="ref113"></a>[113] Kaggle [OpenAI Red Team Dataset](https://www.kaggle.com/datasets/jjlye6/openai-red-team-dataset); dataset metadata and file listing.

<a id="ref114"></a>[114] Kaggle [Prompt Risk Dataset](https://www.kaggle.com/datasets/ziya07/prompt-risk-dataset); dataset metadata and file listing.

<a id="ref115"></a>[115] Kaggle [LLM Red-Team Probes](https://www.kaggle.com/datasets/alimurtazabhutto/llm-red-team-probes); metadata, file listing, and license discrepancy captured locally.

<a id="ref116"></a>[116] Kaggle [LLM Jailbreaks: Prompt Fruit Injection Analysis](https://www.kaggle.com/datasets/chrissyserb/redteam-playback-prompt-fruit-jailbreak); metadata and CC-BY-NC-4.0 declaration.

<a id="ref117"></a>[117] Hugging Face [Catch the prompt injection or jailbreak or benign](https://huggingface.co/datasets/bogdanminko/Catch_the_prompt_injection_or_jailbreak_or_benign); gated card and repository file tree; access condition not accepted.

<a id="ref118"></a>[118] Hugging Face [ToolMisuseBench](https://huggingface.co/datasets/sigdelakshey/ToolMisuseBench); public card and schema for tool-use task/recovery benchmark.

<a id="ref119"></a>[119] Hugging Face [agent-security-datasets](https://huggingface.co/datasets/promptprotection/agent-security-datasets); public card and repository file tree for mixed-role agent-turn scenarios.

<a id="ref120"></a>[120] Hugging Face [AgentHarm](https://huggingface.co/datasets/ai-safety-institute/AgentHarm); public task/card description for agent-interaction harm scenarios.

<a id="ref121"></a>[121] Hugging Face [Cogensec Jailbreak Corpus](https://huggingface.co/datasets/Cogensec/jailbreak-corpus); gated dataset card, mixed-source provenance, weak technique labels, and stated limitations.

<a id="ref122"></a>[122] Hugging Face [AIDataFdn promptinjection](https://huggingface.co/datasets/AIDataFdn/promptinjection); public card and repository file tree reconfirm single-category labels.

<a id="ref123"></a>[123] GitHub [AgentShield Benchmark](https://github.com/doronp/agentshield-benchmark); benchmark corpus categories, Apache-2.0 license, and stated limitations.

<a id="ref124"></a>[124] GitHub [Agent Security Bench](https://github.com/mattpartida/agent-security-bench); benchmark categories for prompt injection, tool misuse, exfiltration, persistence, and approval bypass.

<a id="ref125"></a>[125] Local round-12 screening report, verification and checksums, together with the fresh v0.2.1 trainer preflight output and support-gate manifest.

## Supplemental Dataset Sources for L3 Screening (round 13, 2026-10-23)

These source cards, metadata, and schema records support the local round-13 screening report. The multilingual candidate is quarantined only; no new source was admitted to an L3 split.

<a id="ref126"></a>[126] Hugging Face [Multilingual Prompt Injection](https://huggingface.co/datasets/fevziegeyurtsevenler/multilingual-prompt-injection); pinned revision `9cfe5ab6c61da76f1292f6f91cd7894a40010f55`, 217 rows, CC-BY-4.0 metadata, and quarantined screening hash.

<a id="ref127"></a>[127] Kaggle [Prompt Safety Agent Guardrail Classifier 100k](https://www.kaggle.com/datasets/goutamsharma12/prompt-safety-classifier-100k); metadata, README, annotation guidelines, schema, file listing, and license discrepancy captured in round 13.

<a id="ref128"></a>[128] Kaggle [SCAS: Signed Context Attack Suite](https://www.kaggle.com/datasets/saibhossain/scas-signed-context-attack-suite); metadata and schema for context/task-level authorization evaluation.

<a id="ref129"></a>[129] Kaggle [LLM Prompt-Injection & Jailbreak Detection](https://www.kaggle.com/datasets/ahmadzulfiqar001/llm-prompt-injection-and-jailbreak-detection); CC0 metadata and file listing for a synthetic single-technique corpus.

<a id="ref130"></a>[130] Kaggle [LLM Agent Failure Analysis Benchmark Dataset](https://www.kaggle.com/datasets/sunil123kumar/ai-agent-failure-benchmark-dataset); metadata and file listing for failure-attribution records.

<a id="ref131"></a>[131] Kaggle [AI Agent Security & Real-World Incidents](https://www.kaggle.com/datasets/muhammadahmerkhan/ai-agent-security-and-real-world-incidents-2024-26); metadata and incident-file listing.

<a id="ref132"></a>[132] Hugging Face [Necent LLM Jailbreak & Prompt-Injection Dataset](https://huggingface.co/datasets/Necent/llm-jailbreak-prompt-injection-dataset); gated access and source-specific license note on the official card.

<a id="ref133"></a>[133] Hugging Face [Mindgard evaded prompt-injection and jailbreak samples](https://huggingface.co/datasets/Mindgard/evaded-prompt-injection-and-jailbreak-samples); gated card, CC-BY-NC-4.0 metadata, and mixed source prompts.

<a id="ref134"></a>[134] GitHub [Sentinel-SLM data card](https://github.com/abdulmunimjemal/Sentinel-SLM/blob/main/DATACARD.md); combined binary Prompt Attacks rail and eight-class taxonomy.

<a id="ref135"></a>[135] [Prompt Injection Techniques dataset documentation](https://prompt-injections.readthedocs.io/en/latest/dataset.html) and [MIT license page](https://prompt-injections.readthedocs.io/en/latest/license.html); linked source is the already-screened `pr1m8/prompt-injections` family.

## Supplemental Dataset Sources for L3 v0.2.3 (round 14, 2026-10-23)

<a id="ref136"></a>[136] WUSTL-CSPL [LLMJailbreak](https://github.com/WUSTL-CSPL/LLMJailbreak) and Yu et al., [USENIX Security 2024 paper](https://www.usenix.org/conference/usenixsecurity24/presentation/yu-zhiyuan); pinned repository snapshot and collected jailbreak-prompt source. Repository MIT metadata does not settle third-party prompt rights.

<a id="ref137"></a>[137] JailBreakV-28K [Hugging Face dataset card](https://huggingface.co/datasets/JailbreakV-28K/JailBreakV-28k) and Luo et al., [COLM 2024 paper](https://arxiv.org/abs/2404.03027); source field/schema and pinned dataset snapshot. Dataset-card MIT metadata does not settle third-party prompt rights.

## Supplemental Dataset Sources for L3 v0.2.5 (round 15, 2026-10-23)

<a id="ref138"></a>[138] Hugging Face [CORTYX Safety Dataset](https://huggingface.co/datasets/QuantaSparkLabs/cortyx-safety-dataset/tree/abac2c21250510993025796f6f29a7b3cecf6147); pinned card and 610-row Gold Core snapshot, CC BY 4.0 card declaration, source labels and taxonomy.

<a id="ref139"></a>[139] Hugging Face [Quickium Prompt Security v0](https://huggingface.co/datasets/quickium/prompt-security-v0/tree/8d67314bd5c08497ed1f20a62009bec58e7c5eb0); pinned card and `train_nc` split schema, per-row source and license posture, limitations, and class/source counts.

<a id="ref140"></a>[140] Hugging Face [Governance AI Guardrail ES Dataset](https://huggingface.co/datasets/governanceai/governance-ai-guardrail-es-dataset); gated card describing Spanish label fields, source ancestry metadata, transformations, and access requirement.

<a id="ref141"></a>[141] Mendeley Data [PromptShield: A Human-Annotated Dataset for Prompt Injection Safety Classification](https://data.mendeley.com/datasets/n6wdvz5n3d/1); dataset record with 3,000 samples, three annotators, risk categories, attack types, and CC BY 4.0 declaration.

<a id="ref142"></a>[142] GitHub [Mirza Akhi Prompt Injection Detection Dataset](https://github.com/mirzaakhi/prompt-injection-detection-dataset); dataset card, train/test contract, synthetic category schema, and CC BY 4.0 declaration.

## Supplemental Dataset Sources for L3 v0.2.5 (round 22, 2026-10-24)

<a id="ref143"></a>[143] GitHub [AEGINEL Guard model research report](https://github.com/kwangilkimkenny/AEGINEL/blob/main/docs/AEGINEL_Guard_Model_Research.md); author-reported 188,109 multilingual rows, 21,544 multi-label rows, label schema, split method, example co-label and synthetic-data limitation.

<a id="ref144"></a>[144] GitHub [AEGINEL repository](https://github.com/kwangilkimkenny/AEGINEL); public repository tree and Apache-2.0 project license. The reported training JSONL is absent from the inspected public tree; no separate dataset license is stated there.

<a id="ref145"></a>[145] Hugging Face [AEGIS Multilingual Guard Dataset v0.1 public sample](https://huggingface.co/datasets/YATAV-ENT/aegis-multilingual-guard-dataset-v0.1-samples/tree/b91b6fbd53d255cb2c4610f888622c450395d0fe); pinned 1,200-row sample, single technique field, llm_gen provenance, split tags, native-review flag, and custom responsible-AI-use license.

<a id="ref146"></a>[146] Hugging Face [Neuralchemy Prompt Injection & Jailbreak Detection Dataset](https://huggingface.co/datasets/neuralchemy/Prompt-injection-dataset); binary label plus single category schema, published category/source notes, configurations, and mixed upstream license caveat.

<a id="ref147"></a>[147] Hugging Face [CORTYX full combined JSONL at pinned revision](https://huggingface.co/datasets/QuantaSparkLabs/cortyx-safety-dataset/blob/abac2c21250510993025796f6f29a7b3cecf6147/data/cortyx_combined.jsonl); complete file listing and full combined snapshot used to verify row counts and direct co-label support.

## Supplemental Dataset Sources for L3 v0.2.5 (round 23, 2026-10-24)

<a id="ref148"></a>[148] Hugging Face [cyberec Prompt Injection Mechanisms Dataset at pinned revision](https://huggingface.co/datasets/cyberec/llm-prompt-injection-attacks/tree/a3d05895270cac0e553206c95463061c9bfb899f); dataset card and pinned train/validation Parquet schema, labels and heuristic limitation.

<a id="ref149"></a>[149] Hugging Face [Smooth-3 Prompt Injection Mechanisms Dataset](https://huggingface.co/datasets/Smooth-3/llm-prompt-injection-attacks); upstream dataset card naming the two sources and stating original datasets are not redistributed.

<a id="ref150"></a>[150] Hugging Face [Qualifire Prompt Injections Benchmark](https://huggingface.co/datasets/qualifire/prompt-injections-benchmark) and [Jayavibhav Prompt Injection Safety](https://huggingface.co/datasets/jayavibhav/prompt-injection-safety); source metadata used to check gated/non-commercial access and whether a data license is declared.

<a id="ref151"></a>[151] Hugging Face [Quickium Prompt Security v0 at pinned revision](https://huggingface.co/datasets/quickium/prompt-security-v0/tree/8d67314bd5c08497ed1f20a62009bec58e7c5eb0); card with per-row provenance/license, split counts, domain support and no-compound-row statement.

<a id="ref152"></a>[152] Hugging Face [PromptSentinel](https://huggingface.co/datasets/nuhmanpk/prompt-sentinel); gated access notice, three-class label scheme, source/license fields and publisher-reported split counts.

<a id="ref153"></a>[153] Hugging Face [Necent LLM Jailbreak & Prompt-Injection Dataset](https://huggingface.co/datasets/Necent/llm-jailbreak-prompt-injection-dataset); gated access notice, source aggregation and orthogonal prompt_harmful/prompt_adversarial schema.

<a id="ref154"></a>[154] Hugging Face [Turkish Conversation Prompt-Injection Dataset v1.0.2](https://huggingface.co/datasets/3nesdeniz/turkish-conversation-prompt-injection); CC-BY-4.0 card, 750 curated synthetic rows, attack-family taxonomy, and disjoint train/validation/test counts.

<a id="ref155"></a>[155] GitHub raw [AEGINEL Guard research report](https://raw.githubusercontent.com/kwangilkimkenny/AEGINEL/main/docs/AEGINEL_Guard_Model_Research.md); verified raw source URL used when the GitHub blob endpoint returned HTTP 429.


## Supplemental Dataset Sources for L3 v0.2.5 (round 46, 2026-10-24)

<a id="ref156"></a>[156] Hugging Face [JailbreakBench JBB-Behaviors at pinned revision](https://huggingface.co/datasets/JailbreakBench/JBB-Behaviors/tree/886acc352a31533ffbcf4ef22c744658688086fc/data); official MIT release files and schema for the judge-comparison and behavior cohorts.

<a id="ref157"></a>[157] Zhang et al., ACM TOSEM, “JailGuard: A Universal Detection Framework for Prompt-based Attacks on LLM Systems” (DOI 10.1145/3724393), [institutional repository PDF](https://dr.ntu.edu.sg/server/api/core/bitstreams/42a37690-2f3b-4f00-b856-605a72d1ec0f/content) and the authors' [dataset page](https://sites.google.com/view/jailguard/dataset); text attack-family coverage, reported validated attack cohorts, and 6,000 benign prompts.

<a id="ref158"></a>[158] GitHub [JailGuard repository at pinned commit](https://github.com/shiningrain/JailGuard/tree/419e1d3d08f4d02998a11a687f925518d2d5dd0c); repository tree used to verify text payload filenames and absence of a declared repository license file.

<a id="ref159"></a>[159] Mendeley Data [PromptShield v2: A Human-Annotated Dataset for Prompt Injection Safety Classification](https://data.mendeley.com/datasets/n6wdvz5n3d/2); publisher-reported 3,000 rows, 3-way risk labels, attack_type metadata, and CC BY 4.0.

<a id="ref160"></a>[160] Mendeley Data [Lying to LLMs: A Corpus-assisted Pragmatic Study about the Linguistic Features of Deceptive Jailbreak Prompts](https://data.mendeley.com/datasets/t99msf9hbn/1); public prompt and benign text files and CC BY 4.0 release metadata.


<a id="ref161"></a>[161] Hugging Face [Mindgard evaded prompt-injection and jailbreak samples](https://huggingface.co/datasets/Mindgard/evaded-prompt-injection-and-jailbreak-samples); public card reports gated file access, CC BY-NC-4.0, original/modified prompt pairs, an attack_name technique field, and an upstream Safe-Guard Prompt Injection source.

<a id="ref162"></a>[162] Hugging Face [jackhhao jailbreak-classification](https://huggingface.co/datasets/jackhhao/jailbreak-classification) and the upstream [verazuo/jailbreak_llms repository](https://github.com/verazuo/jailbreak_llms); source lineage, label schema and pinned CSV release reviewed for round 47.

<a id="ref163"></a>[163] Cogensec [Jailbreak Corpus v0.3](https://huggingface.co/datasets/Cogensec/jailbreak-corpus) and [dataset overview](https://cogensec.com/datasets); publisher-reported source composition, schema, licensing, weak-rule labeling and gated access, reviewed metadata-only for round 47.

<a id="ref164"></a>[164] GitHub [Manteclaw LLM Safety and Red Teaming](https://github.com/manteclaw/llm-safety) at pinned revision `072d11c7394289707da8ecd437949e06663b0541`; public sample schema, synthetic flags, paid full-data notice, README license declaration and repository LICENSE reviewed for round 47.

## Supplemental Dataset Sources for L3 v0.2.5 (round 48, 2026-10-24)

<a id="ref165"></a>[165] Hugging Face [3nesdeniz Agentic Prompt-Injection Boundary Pairs](https://huggingface.co/datasets/3nesdeniz/agentic-prompt-injection-boundary-pairs/tree/a5682e7573e1c7bc4b12e64d49c0dcd90ca776cf); pinned CC BY 4.0 snapshot, row taxonomy, split counts, scenario grouping, and review-log claim.

<a id="ref166"></a>[166] GitHub [pr1m8/prompt-injections](https://github.com/pr1m8/prompt-injections/tree/a0ee668c48793f40350489e34727a47d24eeb21f) at pinned commit; repository MIT declaration, source/category/target schema, and dataset/license documentation reviewed for round 48.

<a id="ref167"></a>[167] Hugging Face [3nesdeniz English Prompt Injection 3K](https://huggingface.co/datasets/3nesdeniz/english-prompt-injection-3k/tree/87f017347aff7887b1de0d9457c9ec01bf7ba8b5); pinned CC BY 4.0 card, split and family counts, synthetic template construction and LFS hashes.

<a id="ref168"></a>[168] Hugging Face [CISSP LLMBench](https://huggingface.co/datasets/fahadhafeezofficial/cissp-llmbench); publisher card fields for category, subcategory and safe/unsafe variants, and CC BY 4.0 metadata.

<a id="ref169"></a>[169] Hugging Face [Jeff-Guard Multilingual Dataset](https://huggingface.co/datasets/RomanKudriavskii/jeff-guard-multilang-dataset); publisher card row schema, single-label classes, size, and `other` license metadata.

<a id="ref170"></a>[170] Hugging Face [PromptSentinel](https://huggingface.co/datasets/nuhmanpk/prompt-sentinel); publisher card split counts, three-class label mapping, 13 source lineages, gated-access notice, source licenses, and grouping method.

<a id="ref171"></a>[171] Hugging Face [Rogue Security Prompt Injections Benchmark](https://huggingface.co/datasets/rogue-security/prompt-injections-benchmark); publisher card's test-only 5,000-row jailbreak/benign schema and CC BY-NC 4.0 metadata.

<a id="ref172"></a>[172] Hugging Face [Cyberec Prompt Injection Mechanisms Dataset](https://huggingface.co/datasets/cyberec/llm-prompt-injection-attacks/tree/a3d05895270cac0e553206c95463061c9bfb899f), duplicated from [Smooth-3](https://huggingface.co/datasets/Smooth-3/llm-prompt-injection-attacks/tree/main); pinned Apache 2.0 metadata, multi-label mechanism schema, split counts, source card lineage and heuristic-label caveat.


## Supplemental Dataset Sources for L3 v0.2.5 (round 50, 2026-10-24)

<a id="ref173"></a>[173] Hugging Face [Bordair Multimodal Prompt Injection Dataset at pinned revision](https://huggingface.co/datasets/Bordair/bordair-multimodal/tree/398e3f875ffd32ec2e6817a95feebfcbae41643a) and authors' [repository documentation](https://github.com/n1ps/bordair-dataset); dataset scope, category/seed taxonomy, expansion method, live cohort, source lineage, MIT card claim and review limitations.

<a id="ref174"></a>[174] Hugging Face [AIDataFdn Prompt Injection v3 at pinned revision](https://huggingface.co/datasets/AIDataFdn/promptinjection/tree/99426e65f23ddfb4e19efe1984618a8c61e2d1c6); Apache-2.0 Hub metadata, publisher-reported size and exclusive attack-category schema.

<a id="ref175"></a>[175] Hugging Face [CatBarks pi_c0_to_c8_sampled at pinned revision](https://huggingface.co/datasets/CatBarks/pi_c0_to_c8_sampled/tree/4d05e26c9bf3525650f43a38f52509d3db5f64df); split/schema metadata, source aggregation and absent Hub license declaration reviewed metadata-only.

## Supplemental Dataset Sources for L3 v0.2.5 (round 51, 2026-10-24)

<a id="ref176"></a>[176] Hugging Face [TrustAIRLab In-the-Wild Jailbreak Prompts at pinned revision](https://huggingface.co/datasets/TrustAIRLab/in-the-wild-jailbreak-prompts/tree/a10aab8eff1c73165a442d4464dce192bd28b9c5); MIT metadata and public configuration/schema showing a `jailbreak` boolean without an explicit same-row prompt-injection co-label.

<a id="ref177"></a>[177] Hugging Face [impacte/bunker-laya at pinned revision](https://huggingface.co/impacte/bunker-laya/tree/fe23fc44e9d2418371ac7ac5ec848121027a3e84); publisher-reported source/question counts, partial-gold policy, and notice that source training data are not redistributed.

<a id="ref178"></a>[178] Hugging Face [QuantaSparkLabs CORTYX Safety Dataset at pinned revision](https://huggingface.co/datasets/QuantaSparkLabs/cortyx-safety-dataset/tree/abac2c21250510993025796f6f29a7b3cecf6147); CC BY 4.0 Hub metadata, Gold Core description, source field and multi-label schema.

<a id="ref179"></a>[179] Hugging Face [Smooth-3 Prompt Injection Mechanisms Dataset at pinned revision](https://huggingface.co/datasets/Smooth-3/llm-prompt-injection-attacks/tree/dd47798b64ebf0e833ecdbff6b1d73be3e440581), its [Cyberec duplicate](https://huggingface.co/datasets/cyberec/llm-prompt-injection-attacks/tree/a3d05895270cac0e553206c95463061c9bfb899f), and upstream [Qualifire](https://huggingface.co/datasets/qualifire/prompt-injections-benchmark) and [Jayavibhav](https://huggingface.co/datasets/jayavibhav/prompt-injection-safety) cards; pinned label schema, rule-based reannotation, source lineage and license declarations.

<a id="ref180"></a>[180] Hugging Face [Goutam112 Prompt Safety Classifier 100K at pinned revision](https://huggingface.co/datasets/Goutam112/prompt-safety-classifier-100k/tree/cc19496a37a02f9b97a8381c97d758c9f7f05144); MIT metadata, publisher-reported six-class schema and row count.

<a id="ref181"></a>[181] Hugging Face [JailbreakDB at pinned revision](https://huggingface.co/datasets/youbin2014/JailbreakDB/tree/2c2141bf74ebbe1fd3666a4b38be8856f6e47a92) and [maintainer discussion on `tactic`](https://huggingface.co/datasets/youbin2014/JailbreakDB/discussions/2); CC BY 4.0 metadata, prompt corpus schema, and clarification that the tactic field is roughly binary rather than a specific method label.

<a id="ref182"></a>[182] Hong et al., [“SoK: Taxonomy and Evaluation of Prompt Security in Large Language Models”](https://arxiv.org/abs/2510.15476); paper-reported JailbreakDB and benign corpus sizes, compared with the current Hub card during round 51.

<a id="ref183"></a>[183] NVIDIA [Nemotron Safety Guard Dataset v3 at pinned revision](https://huggingface.co/datasets/nvidia/Nemotron-Safety-Guard-Dataset-v3/tree/a3f7ecb3433d1933701a83f18de16c36934a7f51); CC BY 4.0 metadata, multilingual schema, `jailbreaking` tag, publisher-reported size and synthetic-labeling disclosure.

## Supplemental Dataset Sources for L3 v0.2.5 (round 52, 2026-10-24)

<a id="ref184"></a>[184] ETH Zurich SPY Lab [SaTML 2024 CTF dataset at pinned revision](https://huggingface.co/datasets/ethz-spylab/ctf-satml24/tree/11426babe61ee16b0efe7b55e0430359e0fc4235); MIT metadata, 137,151 multi-turn attack chats, and the secret-extraction task description.

<a id="ref185"></a>[185] Debenedetti et al., [Dataset and Lessons Learned from the 2024 SaTML LLM Capture-the-Flag Competition](https://arxiv.org/abs/2406.07954); paper description of the system-prompt secret-extraction threat model and public 137k-chat release.

<a id="ref186"></a>[186] Hugging Face [PromptSentinel at pinned revision](https://huggingface.co/datasets/nuhmanpk/prompt-sentinel/tree/a932b3ef5982c97ec2c5c635bf61b9cbb4bd1a5b); gated notice, three exclusive labels, source/license fields, aggregation lineage and published class/split counts.

<a id="ref187"></a>[187] GitHub [Aegis classifier v1 results at pinned commit](https://github.com/espirado/Aegis/blob/782812efcb01301d2c3acd240c4054551e2e71ff/docs/analysis/classifier-v1-results.md); five exclusive output classes, source composition and the maintainer's note on jailbreak-style samples labeled as injection.

<a id="ref188"></a>[188] Hugging Face [Mindgard evaded prompt-injection and jailbreak samples at pinned revision](https://huggingface.co/datasets/Mindgard/evaded-prompt-injection-and-jailbreak-samples/tree/ec63ffb26ba6f29ca1095fabb2e9f9be5f8b9d34); CC BY-NC 4.0 metadata, mixed source description, original/modified prompt fields and technique-only attack_name.



## Supplemental Dataset Sources for L3 v0.2.5 (round 53, 2026-10-24)

<a id="ref189"></a>[189] Hugging Face [9mark9 LLM Red-Team OWASP Prompts at pinned revision](https://huggingface.co/datasets/9mark9/llm-redteam-owasp-prompts/tree/cac5cb5801964011295c1926b927506e81f2802d); publisher MIT metadata, train-only schema, category and OWASP tags, source/generated fields, and seed IDs.

<a id="ref190"></a>[190] Hugging Face [NEPI Prompts Dataset at pinned revision](https://huggingface.co/datasets/Vaibhav-GOAT/nepi-prompts-dataset/tree/391139f74fc50d09b5593eb387505ab5844b0bc9); publisher MIT metadata, synthetic-template train description, label, attack-family and target-goal schema.

<a id="ref191"></a>[191] Hugging Face [Necent jailbreak and prompt-injection dataset card](https://huggingface.co/datasets/Necent/llm-jailbreak-prompt-injection-dataset); gated access notice, aggregated-source scope, singular prompt-type schema and upstream-license caveat; metadata only.

<a id="ref192"></a>[192] Hugging Face [Fujitsu ART-SafeBench v2 dataset card](https://huggingface.co/datasets/Fujitsu/agentic-rag-redteam-bench); gated access and use terms, publisher CC-BY-4.0 metadata, benchmark configurations and mixed source list; metadata only.

<a id="ref193"></a>[193] Xia et al., Findings of ACL 2025, [“The Threat of PROMPTS in Large Language Models: A System and User Prompt Perspective”](https://aclanthology.org/2025.findings-acl.675/) ([open-access PDF](https://aclanthology.org/2025.findings-acl.675.pdf), DOI 10.18653/v1/2025.findings-acl.675); distinguishes prompt leakage and jailbreak goals and discusses prompt injection as an attack method that can support either.

<a id="ref194"></a>[194] Muhammad Saeed Anwar, [Prompt Injection Attacks in Large Language Models benchmark repository at pinned commit](https://github.com/MuhammadSaeedAnwar/prompt-injection-llm-benchmark/tree/b44898ab1700eec850ee68eeb687a40f86406ef8) and [Zenodo dataset DOI](https://doi.org/10.5281/zenodo.19364462); publisher-reported 250-row attack benchmark, category and target_behavior schema, MIT declaration, and absence of a released split, reviewed metadata-only.

<a id="ref195"></a>[195] GitHub [Mirza Akhi Prompt Injection Detection Dataset at pinned commit](https://github.com/mirzaakhi/prompt-injection-detection-dataset/tree/011a9ae25b31feb48d23f837fdcbc3a6a4ee3b4e); combined CSV train/test contract, binary labels, synthetic category schema and repository CC BY 4.0 claim; only train rows were persisted for round 54 and compared with v0.2.5 train/validation.



## Supplemental Dataset Sources for L3 v0.2.5 (round 55, 2026-10-24)

<a id="ref196"></a>[196] Muhammad Saeed Anwar, [Prompt Injection Attacks benchmark repository at pinned commit](https://github.com/MuhammadSaeedAnwar/prompt-injection-llm-benchmark/tree/b44898ab1700eec850ee68eeb687a40f86406ef8), [pinned CSV](https://raw.githubusercontent.com/MuhammadSaeedAnwar/prompt-injection-llm-benchmark/b44898ab1700eec850ee68eeb687a40f86406ef8/prompt_injection_dataset_250.csv), and [Zenodo record](https://doi.org/10.5281/zenodo.19364462); benchmark purpose, MIT claim, row schema, and publisher-described category counts, compared with the pinned CSV snapshot during round 55.

<a id="ref197"></a>[197] ICARO Lab, [Adversarial Humanities Benchmark repository at pinned commit](https://github.com/icaro-lab/ahb/tree/36f626847d59b8c256d3e70d534f34f3c4681e81) and Galisai et al., [“Adversarial Humanities Benchmark: Results on Stylistic Robustness in Frontier Model Safety”](https://arxiv.org/abs/2604.18487); metadata-only review of its benchmark-only/canary restriction and MLCommons AILuminate prompt provenance.

<a id="ref198"></a>[198] Zhang et al., [JailGuard: A Universal Detection Framework for Prompt-based Attacks on LLM Systems](https://doi.org/10.1145/3724393) and [official repository at pinned commit](https://github.com/shiningrain/JailGuard/tree/419e1d3d08f4d02998a11a687f925518d2d5dd0c); publisher-reported 11,000 text/image attack examples across 15 methods, with payload distributed by external link and no repository license file observed in the pinned tree listing.
