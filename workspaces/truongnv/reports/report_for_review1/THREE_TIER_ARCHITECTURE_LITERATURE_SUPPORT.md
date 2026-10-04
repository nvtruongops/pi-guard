# Bằng chứng văn liệu cho kiến trúc ingress ba tầng PI-Guard

**Ngày rà soát:** 2026-10-03  
**Phạm vi:** tìm nguồn học thuật để biện minh cho kiến trúc đề xuất L1 trích xuất/chuẩn hóa → L2 TF-IDF + Logistic Regression định tuyến → L3 DeBERTa xử lý các trường hợp REVIEW. Đây là rà soát tài liệu, không phải bằng chứng cascade PI-Guard đã triển khai hay đã tăng hiệu năng.

## Kết luận

- Không còn chính xác nếu nói “chưa có bài báo nào theo hướng nhiều tầng/cascade cho prompt injection”. Có tiền lệ trực tiếp: MCP-Guard mô tả pipeline ba giai đoạn; RAPIDS đánh giá cascade hai giai đoạn cho phát hiện prompt injection.
- Trong các nguồn rà soát, chưa thấy bài nào đánh giá đúng tổ hợp PI-Guard: L1 trích xuất tài liệu và chuẩn hóa, L2 TF-IDF/LR với ba route, rồi L3 DeBERTa chỉ nhận vùng REVIEW. Không nên tuyên bố đã rà soát hết mọi công trình.
- Có thể lập luận kiến trúc PI-Guard bằng cách kết hợp các nhánh văn liệu: đổi cấu trúc đầu vào cần được kiểm định; front-end có thể giữ ranh giới giữa dữ liệu và chỉ thị; classifier có thể defer/cascade ca khó; các paper prompt-injection đã có tiền lệ cascade.
- Các paper này biện minh cho **động cơ và hình dạng thiết kế**, không chứng minh chính mô hình PI-Guard sẽ tăng F1, giảm FPR hoặc đạt latency mục tiêu. Phần đó cần đo trên cùng tập dữ liệu và bằng ablation.

## Bản đồ nguồn theo tầng

| Nguồn | Phần hỗ trợ cho PI-Guard | Ranh giới khi trích dẫn |
|---|---|---|
| Shire & Kim, [PIDS-Bench, IEEE Access 2026](https://ieeexplore.ieee.org/document/11670335), [toàn văn](https://arxiv.org/html/2609.15017) | Đo hard-benign, obfuscation, domain shift và structural shift; structural shift gồm JSON wrapping, prompt dilution và tiền tố giống system instruction. Hỗ trợ lập luận rằng chỉ số IID không đủ và pipeline phải được kiểm định trên nhiều cách đóng gói. | Paper đánh giá detector đơn đầu vào, không đánh giá router hay cascade. Các stress-set không phải dự báo FPR cho traffic sản xuất. |
| Chen et al., [StruQ, USENIX Security 2025](https://www.usenix.org/conference/usenixsecurity25/presentation/chen-sizhe) | Tách front-end định dạng prompt và dữ liệu khỏi mô hình downstream; ủng hộ ranh giới rõ giữa xử lý/biểu diễn đầu vào và xử lý bằng mô hình. | Front-end StruQ tạo structured query và mô hình được huấn luyện để tôn trọng hai kênh; đây không phải parser PDF/JSON cho detector PI-Guard và không phải cascade ba classifier. |
| Xing et al., [MCP-Guard, Findings of ACL 2026](https://aclanthology.org/2026.findings-acl.240/) | Tiền lệ gần nhất về **số tầng**: static scanning → detector neural E5 → LLM arbitration cho các trường hợp mơ hồ. Chỉ tầng arbitration đắt hơn chạy có điều kiện. | Phạm vi là prompt/tool threats trong MCP; tầng đầu là rule scanner, tầng cuối là LLM. Không kiểm định L1 tài liệu → TF-IDF/LR → DeBERTa. Benchmark do paper xây dựng và có dữ liệu GPT-4 augmentation; không nên suy rộng kết quả sang đồ án. |
| Augey et al., [RAPIDS, ACL 2026 Industry Track](https://aclanthology.org/2026.acl-industry.127/) | Tiền lệ trực tiếp cho **cascade phát hiện prompt injection**: SLM tinh chỉnh để recall cao ở lượt đầu, sau đó chuyển nghi vấn sang LLM verifier. Paper báo cáo recall đầu-cuối ≥98% trên hai tập đánh giá và giảm latency so với gọi frontier LLM cho toàn bộ đầu vào. | Chỉ có hai tầng phân loại, miền là hồ sơ tuyển dụng, Stage 1 là SLM chứ không phải TF-IDF, Stage 2 là LLM chứ không phải DeBERTa. Paper cũng ghi nhận giới hạn với Base64/Rot13, tiếng Anh và quy mô holdout thực tế. Không chuyển các con số hiệu năng sang PI-Guard. |
| Varshney & Baral, [Model Cascading, EMNLP 2022](https://aclanthology.org/2022.emnlp-main.756/) | Nền tảng cascade tổng quát cho NLP: dùng mô hình nhỏ cho ca dễ và chuyển một phần đầu vào tới mô hình năng lực cao hơn; hỗ trợ luận điểm về efficiency/accuracy cần cân bằng. | Không phải prompt-injection. Mức tiết kiệm tính toán/tăng accuracy của paper không phải kỳ vọng hay kết quả của PI-Guard. |
| Verma et al., [Learning to Defer to Multiple Experts, AISTATS 2023](https://proceedings.mlr.press/v206/verma23a.html) | Cơ sở phương pháp cho quyết định “tự dự đoán hay defer cho expert”, và lựa chọn nơi chuyển ca khó. Có thể dùng để giải thích khái niệm REVIEW/định tuyến. | Bài toán gốc có expert demonstrations, thường là người; không chứng minh threshold routing TF-IDF → DeBERTa hiệu quả nếu không huấn luyện/đánh giá router thích hợp. |

## Lập luận có thể đưa vào báo cáo

> Các nghiên cứu trước gợi ý ba yêu cầu thiết kế liên quan: (1) đầu vào có thể đổi cấu trúc trong khi ý định và nhãn giữ nguyên; (2) front-end có thể chuẩn hóa hoặc giữ ranh giới giữa chỉ thị và dữ liệu trước khi gọi mô hình; và (3) các hệ thống cascade có thể chuyển ca khó từ bộ phát hiện nhẹ sang bộ xử lý năng lực cao hơn. Trên cơ sở đó, đồ án **đề xuất** L1 trích xuất/chuẩn hóa nội dung, L2 TF-IDF + Logistic Regression sàng lọc và định tuyến, L3 DeBERTa phân loại các đoạn REVIEW. Đây là kiến trúc riêng cần được kiểm chứng đầu-cuối, không phải kiến trúc được PIDS-Bench hay RAPIDS đánh giá nguyên trạng.

## Kiểm định cần có trước khi kết luận mô hình tốt hơn

So sánh trên cùng split và nhãn: L2 đơn; L3 chạy cho mọi đầu vào; L2→L3; và toàn pipeline L1→L2→L3. Chọn các ngưỡng ALLOW/REVIEW/BLOCK trên validation, không điều chỉnh bằng tập test. Báo cáo kết quả IID, hard-benign theo nguồn, JSON wrapping, prompt dilution, prefix mimicry, domain shift và obfuscated attack. Ngoài F1, cần ghi recall/false negative, FPR, tỷ lệ chuyển REVIEW, lỗi/độ phủ trích xuất ở L1, latency end-to-end và số lượt gọi L3.

JSON wrapping hoặc cách trình bày khác nên là các biến thể đầu vào giữ nhãn tương ứng; không tự tạo lớp nhãn mới chỉ vì một mẫu được đóng gói thành JSON. Nếu lớp đầu ra L3 gồm Benign/Prompt Injection/Jailbreak, cần định nghĩa riêng quy tắc nhãn và đánh giá cho bài toán đó.

## Liên kết nguồn

- PIDS-Bench (IEEE Access): https://ieeexplore.ieee.org/document/11670335
- PIDS-Bench full text: https://arxiv.org/html/2609.15017
- StruQ (USENIX Security 2025): https://www.usenix.org/conference/usenixsecurity25/presentation/chen-sizhe
- MCP-Guard (Findings ACL 2026): https://aclanthology.org/2026.findings-acl.240/
- RAPIDS (ACL 2026 Industry Track): https://aclanthology.org/2026.acl-industry.127/
- Model Cascading (EMNLP 2022): https://aclanthology.org/2022.emnlp-main.756/
- Learning to Defer to Multiple Experts (AISTATS 2023): https://proceedings.mlr.press/v206/verma23a.html
