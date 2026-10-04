# Ma trận phân biệt Direct PI, Indirect PI và Jailbreak

**Ngày nghiên cứu:** 2026-10-02  
**Phạm vi:** đối chiếu nguồn học thuật và cách dùng chúng để lập ma trận dữ liệu/đánh giá cho PI-Guard. Không huấn luyện hoặc chạy benchmark.

## Scope Boundary Declaration

| IN-SCOPE | OUT-OF-SCOPE |
|---|---|
| Chọn hai bài chính cho Prompt Injection và Jailbreak; bổ sung nguồn Direct PI đã có trong kho để ma trận thể hiện đủ ba hàng; đối chiếu mục tiêu, đường đưa chỉ thị, loại bằng chứng và giới hạn áp dụng. | Huấn luyện classifier; tải/chạy benchmark; tạo số liệu PI-Guard; kết luận các metric của bài báo dự đoán hiệu năng PI-Guard; đổi kiến trúc hoặc taxonomy đồ án. |

## Kết luận chọn bài

Hai bài chính nên dùng cho ma trận là **BIPIA** cho Indirect Prompt Injection và **JailbreakBench** cho Jailbreak. BIPIA xây dựng benchmark cho chỉ thị độc hại nằm trong nội dung bên ngoài; JailbreakBench chuẩn hóa đánh giá các tấn công nhằm khiến LLM tạo nội dung gây hại hoặc bị cấm. Chúng bổ sung nhau nhưng không phải benchmark cùng nhiệm vụ hay có metric so sánh trực tiếp. [[2]](#ref2) [[3]](#ref3)

Để có hàng **Direct Prompt Injection**, dùng Perez và Ribeiro (2022) làm nguồn phân loại/kỹ thuật tấn công đã có sẵn trong kho References. Vì vậy bộ ma trận có ba nguồn để phủ ba hàng; nếu giới hạn đúng hai bài, giữ BIPIA + JailbreakBench và ghi rõ Direct PI chưa được đối chiếu bằng một nguồn riêng trong cặp đó. [[1]](#ref1)

## Ma trận so sánh

| Khía cạnh | Direct Prompt Injection | Indirect Prompt Injection | Jailbreak (JB) |
|---|---|---|---|
| Trục phân loại | **Nguồn/đường đưa chỉ thị:** chỉ thị đối kháng nằm ngay trong prompt người dùng gửi trực tiếp. | **Nguồn/đường đưa chỉ thị:** chỉ thị đối kháng được nhúng trong nội dung ngoài (ví dụ trang web, email, tài liệu hoặc context được truy xuất) rồi được ứng dụng đưa vào ngữ cảnh LLM. | **Mục tiêu/kết quả:** khiến LLM vượt qua cơ chế từ chối/an toàn và sinh đầu ra có hại hoặc không được phép; thường gửi trực tiếp nhưng có thể kết hợp với PI gián tiếp. |
| Nguồn chính | Perez & Ribeiro, *Ignore Previous Prompt: Attack Techniques For Language Models* (ML Safety Workshop at NeurIPS 2022). Bài nghiên cứu goal hijacking và prompt leaking từ tương tác đầu vào độc hại. [[1]](#ref1) | Yi et al., *Benchmarking and Defending Against Indirect Prompt Injection Attacks on Large Language Models* (KDD 2025). BIPIA đánh giá chỉ thị độc hại nhúng trong external content qua năm kịch bản ứng dụng và 250 attacker goals. [[2]](#ref2) | Chao et al., *JailbreakBench: An Open Robustness Benchmark for Jailbreaking Large Language Models* (NeurIPS 2024, Datasets and Benchmarks Track). Benchmark có 100 behaviors và framework đánh giá chuẩn hóa với threat model, chat template và scoring functions. [[3]](#ref3) |
| Bằng chứng bài báo | Mô tả kỹ thuật tấn công/PromptInject và hai nhóm mục tiêu; phù hợp làm cơ sở khái niệm cho Direct PI. | Benchmark thực nghiệm chuyên về Indirect PI; paper nêu rõ attacker sửa external content để nhúng chỉ thị. | Benchmark mở chuyên về jailbreak artifacts và đánh giá robustness của LLM trước JB. |
| Dùng cho PI-Guard | Tạo lát đánh giá riêng cho prompt người dùng có yêu cầu override chỉ thị/hijack mục tiêu hoặc lấy lộ thông tin chỉ dẫn. | Tạo lát đánh giá riêng cho văn bản trích xuất từ upload hoặc external context không đáng tin. Upload tài liệu của PI-Guard không hoàn toàn giống luồng retrieval trong BIPIA, nên phải ghi rõ khác biệt nguồn và giao thức. | Tạo lát đánh giá theo mục tiêu vượt qua từ chối/an toàn. Chấm detector PI-Guard trên nội dung đầu vào; không dùng ASR của JBB như metric detector hoặc hiệu năng của PI-Guard. |
| Giới hạn khi viện dẫn | Không phải benchmark chuẩn hóa ba lớp cho PI-Guard; kết quả của bài không trực tiếp so sánh với BIPIA/JBB. | Không phải bộ đánh giá Direct PI hay Jailbreak. Không chuyển các tỷ lệ ASR/defense của bài thành kỳ vọng cho classifier ingress. | Không phải benchmark phát hiện prompt injection; nhãn/hành vi và cách chấm jailbreak khác bài toán phân loại văn bản đầu vào. Không so sánh metric ngang hàng với BIPIA. |

## Quy tắc đọc ma trận và gán nhãn

Direct/Indirect mô tả **vị trí hoặc nguồn chỉ thị đối kháng**; Jailbreak mô tả **mục tiêu/kết quả tấn công**. Do đó ba hàng này không tạo thành ba lớp loại trừ lẫn nhau. Một prompt gửi trực tiếp có thể đồng thời là Direct PI và JB nếu nó vừa cố vượt quyền chỉ thị vừa tìm cách tạo đầu ra bị cấm. [[1]](#ref1) [[3]](#ref3)

Với dữ liệu đồ án, nên lưu riêng ít nhất hai thuộc tính: `delivery_source` (direct prompt / uploaded or retrieved content) và `attack_objective` (instruction hijack or leakage / safety bypass / other). Nếu mô hình phải xuất một nhãn duy nhất `benign / prompt_injection / jailbreak`, cần chốt quy tắc ưu tiên cho trường hợp giao nhau trước khi gán nhãn; không suy ra quy tắc đó từ các benchmark trên. Đây là đề xuất quy trình dữ liệu của PI-Guard, chưa phải kết quả bài báo. [[1]](#ref1) [[2]](#ref2) [[3]](#ref3)

Với upload, chỉ gọi nội dung là **document-carried/indirect-style injection** khi nội dung trong tệp được xem là dữ liệu không đáng tin và cố chi phối hành vi LLM. Không tự động gán mọi file upload vào Indirect PI: cách ứng dụng phân vai nội dung và mục tiêu của chỉ thị cần được ghi trong annotation guideline. BIPIA kiểm tra external content do ứng dụng tích hợp/truy xuất; đó là căn cứ gần nhưng không đồng nhất với toàn bộ luồng upload của PI-Guard. [[2]](#ref2)

## Cách dùng trong báo cáo đồ án

1. Dùng **BIPIA + JailbreakBench** làm hai benchmark tham chiếu chính cho Indirect PI và JB; mô tả đúng phạm vi benchmark riêng của từng bài.
2. Dùng **Perez & Ribeiro** làm nguồn bổ trợ cho Direct PI; không gọi bài workshop này là benchmark so sánh detector.
3. Xây các lát test tách biệt Direct PI, document-carried/Indirect PI, và JB; báo cáo kết quả theo từng lát trước khi gộp. Quy tắc gán nhãn trường hợp giao nhau phải được công bố.
4. Không gộp hoặc so sánh trực tiếp ASR của BIPIA/JBB với precision, recall, F1, FPR hay latency của detector PI-Guard; nhiệm vụ, hệ thống đích và protocol khác nhau.

<a id="source-provenance"></a>
## Kiểm tra xuất xứ tài liệu

PDF của cả ba bài đã có trong `workspaces/truongnv/References/`: Perez & Ribeiro, BIPIA và JailbreakBench. Metadata toàn văn arXiv của BIPIA ghi bài thuộc **Proceedings of the 31st ACM SIGKDD Conference (KDD ’25), 2025**, DOI `10.1145/3690624.3709179`; mục BIPIA trong reference log hiện có ghi Findings of NAACL 2024 và thông tin tác giả khác. Báo cáo này dùng metadata ở toàn văn arXiv/publisher record và đánh dấu mục reference log là cần rà soát riêng; không sửa reference master trong phạm vi task này. [[2]](#ref2)

## References

<a id="ref1"></a>**[1]** F. Perez and I. Ribeiro, “Ignore Previous Prompt: Attack Techniques For Language Models,” ML Safety Workshop at NeurIPS 2022. [arXiv record and open PDF](https://arxiv.org/abs/2211.09527) · [Local PDF](../../References/Perez_2022_Ignore_This_Title_Hack_This_Paper_Prompt_Injection.pdf).

<a id="ref2"></a>**[2]** J. Yi, Y. Xie, B. Zhu, E. Kiciman, G. Sun, X. Xie, and F. Wu, “Benchmarking and Defending Against Indirect Prompt Injection Attacks on Large Language Models,” *Proceedings of the 31st ACM SIGKDD Conference on Knowledge Discovery and Data Mining (KDD ’25)*, 2025. DOI: `10.1145/3690624.3709179`. [Full text and publication metadata](https://arxiv.org/html/2312.14197) · [Local PDF](../../References/Viet_2024_BIPIA_Benchmarking_Indirect_Prompt_Injection_Attacks.pdf).

<a id="ref3"></a>**[3]** P. Chao et al., “JailbreakBench: An Open Robustness Benchmark for Jailbreaking Large Language Models,” *Advances in Neural Information Processing Systems 37 (NeurIPS 2024), Datasets and Benchmarks Track*. [Official NeurIPS proceedings](https://proceedings.neurips.cc/paper_files/paper/2024/hash/63092d79154adebd7305dfd498cbff70-Abstract-Datasets_and_Benchmarks_Track.html) · [Open PDF](https://arxiv.org/pdf/2404.01318.pdf) · [Local PDF](../../References/Chao_2024_JailbreakBench_Open_Robustness_Benchmark_NeurIPS.pdf).
