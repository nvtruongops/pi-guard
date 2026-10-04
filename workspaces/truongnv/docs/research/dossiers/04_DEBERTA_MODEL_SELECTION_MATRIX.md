# Ma trận bằng chứng lựa chọn mô hình DeBERTa-v3 cho PI-Guard

## Scope Boundary Declaration

- **IN-SCOPE:** so sánh tài liệu phát hành và bài báo của các checkpoint DeBERTa-v3 đang được lưu trong manifest; đề xuất ứng viên cho mục tiêu phân loại PI-Guard.
- **OUT-OF-SCOPE:** fine-tune hoặc đánh giá mô hình PI-Guard trong tài liệu này; khôi phục kết quả ma trận D1–D6 đã rút; xếp hạng mô hình bằng metric lấy từ các bộ test khác nhau.

## Mục đích và cách đọc bằng chứng

PI-Guard đặt mục tiêu nghiên cứu bộ phân loại **Benign / Prompt Injection / Jailbreak**. Bảng dưới dùng model card và bài báo để đánh giá mức phù hợp của checkpoint, độ công khai của dữ liệu và giới hạn đã được công bố. Bằng chứng từ model card được ghi là thông tin do bên phát hành tự công bố; nó không tương đương với xác nhận độc lập hoặc kết quả chạy của PI-Guard.

Các model ID và revision được lấy từ [manifest khóa nguồn checkpoint](../../../replications/02_DeBERTa_v3_Semantic_Classifier/upstream/model_sources.lock.json). Manifest chỉ hỗ trợ nhận diện nguồn và phiên bản; các dự đoán/metric trong ma trận D1–D6 không được dùng ở đây vì hồ sơ hiện hành đã rút các so sánh chéo paper đó. Xem thêm [trạng thái bằng chứng SOTA](./03_SOTA_SURVEY_AND_6BASELINES.md).

Trong [đề xuất ingress Review 1 lần 2](../../../reports/report%20for%20review%201%20lan%202/README.md), `microsoft/deberta-v3-base` là backbone dự kiến cho classifier tại L3; classification head và fine-tuning theo nhãn PI-Guard chưa được triển khai hay đánh giá. L1/L2/API có trách nhiệm riêng theo hồ sơ kiến trúc, nên không diễn giải ma trận checkpoint này như đặc tả đầy đủ của cascade.

## Ma trận mô hình

| Ứng viên | Backbone, tác vụ và nhãn | Dữ liệu huấn luyện được công bố | Bằng chứng và giới hạn | Mức phù hợp với PI-Guard |
|---|---|---|---|---|
| **DeBERTa-v3-base — ứng viên fine-tune của nhóm** | Model nền của Microsoft; đề xuất gắn đầu phân loại cho ba nhãn của đồ án. Model card nền mô tả checkpoint là mô hình DeBERTa-v3-base, giấy phép MIT ([Microsoft model card](https://huggingface.co/microsoft/deberta-v3-base)); kiến trúc được mô tả trong paper DeBERTa-v3. [[9]](#ref9) | Nhóm cần dùng tập dữ liệu đã gán nhãn theo quy tắc PI-Guard. Quy mô và metric của mô hình nhóm **chưa được xác lập**. | Đây là **đề xuất phương pháp** của nhóm, chưa phải kết quả thực nghiệm. Có thể kiểm soát nhãn, split và nguồn dữ liệu ngay từ đầu. | **Phù hợp nhất với mục tiêu ba nhãn**, nếu nhóm làm rõ ranh giới nhãn và có tập train/validation/test độc lập. Không có căn cứ để khẳng định trước rằng nó sẽ đạt metric cao hơn checkpoint công khai. |
| **PIGuard** ([model card](https://huggingface.co/leolee99/PIGuard)) | Model card chỉ `microsoft/deberta-v3-base` làm model nền. Bài báo mô tả phân loại benign và malicious; không phải bộ phân loại ba nhãn PI-Guard. [[18]](#ref18) | Bài báo báo cáo tập cuối gồm **61.089 benign** và **15.666 prompt-injection/malicious** mẫu; có dữ liệu tăng cường cho các định dạng dài đuôi. [[18]](#ref18) | Có bài ACL và mã/tập dữ liệu công khai. Kết quả trong bài gắn với benchmark và giao thức của chính bài; không chuyển thẳng thành metric PI-Guard. [[18]](#ref18) | **Checkpoint tham khảo gần nhất về kiến trúc và nghiên cứu prompt guard.** Hữu ích để đối chiếu cách xử lý over-defense, nhưng nhãn benign/malicious không tách riêng Jailbreak thành lớp thứ ba. |
| **Meta Prompt Guard 86M** ([model card](https://huggingface.co/meta-llama/Prompt-Guard-86M)) | Backbone multilingual `mDeBERTa-v3-base`; phân loại ba lớp benign / injection / jailbreak. [[20]](#ref20) | Model card mô tả dữ liệu gồm nguồn mở, dữ liệu tổng hợp và tập red-team; không công bố toàn bộ tập huấn luyện. [[20]](#ref20) | Có báo cáo kỹ thuật CyberSecEval 3 [[20]](#ref20) và repository PurpleLlama của Meta. Checkpoint có gate truy cập. | **Tham khảo đa lớp gần taxonomy đồ án nhất.** Thích hợp làm baseline đối chuẩn ba lớp nếu điều khoản và quyền truy cập cho phép. |
| **PromptShield DeBERTa** ([mã tác giả](https://github.com/wagner-group/PromptShield)) | Fine-tune từ `microsoft/deberta-v3-base`; paper CODASPY 2025 [[30]](#ref30) công bố mã fine-tuning `finetuning_deberta.py`. | Bài báo công bố dữ liệu benchmark kết hợp hội thoại tự nhiên và kịch bản ứng dụng, tập trung vào vùng FPR thấp (Low-FPR regime). | Có bài báo CODASPY 2025 [[30]](#ref30) và repository mã nguồn của nhóm tác giả (Wagner group). Không dùng checkpoint tự tạo không rõ nguồn. | **Baseline nghiên cứu DeBERTa-v3-base có paper và mã fine-tuning công khai.** Phù hợp làm chuẩn đối chiếu cho đánh giá trong vùng FPR thấp. |
| **Llama Prompt Guard 2 86M** ([model card](https://huggingface.co/meta-llama/Llama-Prompt-Guard-2-86M)) | Backbone `mDeBERTa-base`; detector phân loại benign / malicious trong bộ giải pháp LlamaFirewall (Meta, 2025; arXiv:2505.03574). | Model card và paper LlamaFirewall mô tả cơ chế phòng thủ đa tầng; Meta công bố mã scanner/inference trong PurpleLlama. | Có bài báo LlamaFirewall (Meta, 2025; arXiv:2505.03574) và mã scanner chính thức. Bản 86M dùng mDeBERTa-base (khác bản 22M dùng DeBERTa-xsmall). | **Baseline đối chuẩn cập nhật từ Meta.** Cùng kích cỡ backbone 86M, đại diện cho thế hệ guardrail công nghiệp mới nhất của Meta. |

### Các ứng viên đã rút (Withdrawn Candidates)

Các checkpoint snapshot từng lưu cục bộ gồm **ProtectAI DeBERTa-v3 v2**, **DeepSet DeBERTa**, và **InjectionSentry** (cùng FMOPS DistilBERT và WolfDefender) đã bị xóa ngày 2026-10-02 theo [MODEL_PAPER_CODE_ALIGNMENT_AUDIT_2026-10-02.md](../../../reports/experiment_reports/MODEL_PAPER_CODE_ALIGNMENT_AUDIT_2026-10-02.md) vì không đáp ứng tiêu chuẩn bắt buộc: *phải có cặp bài báo nghiên cứu gốc và repository mã nguồn chính thức của chính checkpoint*. Cụ thể:
- ProtectAI chỉ dẫn nguồn `@misc` trên Hugging Face, dự án đã lưu trữ và không có paper gốc tương ứng.
- DeepSet thiếu paper nghiên cứu và training repository cho checkpoint.
- InjectionSentry chỉ trích dẫn PR GitHub Lakera PINT #35, không phải paper học thuật.

## Đề xuất lựa chọn

1. **Mô hình nghiên cứu chính:** fine-tune `microsoft/deberta-v3-base` trên dữ liệu PI-Guard đã gán nhãn, vì hướng này cho phép huấn luyện đúng schema ba nhãn mà đồ án đặt ra. Đây là đề xuất thiết kế, chưa phải kết luận về hiệu năng. DeBERTa-v3 được dùng làm backbone trong các nghiên cứu và checkpoint tham khảo nêu trên. [[9]](#ref9) [[18]](#ref18)
2. **Bốn mô hình tham khảo/đối chuẩn đáp ứng chuẩn paper + repo:** PIGuard [[18]](#ref18), Meta Prompt Guard 86M [[20]](#ref20), PromptShield DeBERTa [[30]](#ref30), và Llama Prompt Guard 2 86M (Meta, 2025; arXiv:2505.03574). Chúng đại diện cho các phương pháp bảo vệ prompt dựa trên DeBERTa-family có đầy đủ bằng chứng y văn và mã nguồn công khai.
3. **Điều kiện trước khi train:** định nghĩa nhãn sao cho nhất quán. Nếu Jailbreak có thể đồng thời là Prompt Injection, bộ phân loại softmax ba lớp cần quy tắc gán lớp chính rõ ràng; nếu giữ nhãn chồng lấp, cần cân nhắc thiết kế phân cấp hoặc đa nhãn.
4. **Đánh giá sau này:** chỉ kết luận mô hình nào phù hợp hơn sau khi chạy trên cùng split độc lập, có khử trùng lặp theo nguồn/nhóm prompt và báo cáo metric theo từng lớp. Các kết quả hiện hành của đồ án chỉ gồm những báo cáo được giữ lại theo quy tắc cùng nguồn paper; PI-Guard DeBERTa ba lớp chưa được fine-tune hoặc đánh giá tại chỗ. [SOTA survey](./03_SOTA_SURVEY_AND_6BASELINES.md) · [báo cáo phạm vi và deprecations](../../../reports/ARCHITECTURAL_DEPRECATIONS_AND_OUT_OF_SCOPE.md)

## Định hướng câu hỏi nghiên cứu của PI-Guard

> **Trạng thái: đề xuất nghiên cứu, chưa huấn luyện và chưa có kết quả thực nghiệm của nhóm.**

DeBERTa-v3 là encoder tiền huấn luyện cho các tác vụ hiểu ngôn ngữ; paper gốc đánh giá năng lực NLU tổng quát, không chứng minh hiệu năng phát hiện Prompt Injection của PI-Guard. [[9]](#ref9) PIGuard đặt trọng tâm riêng vào giảm over-defense và giới thiệu NotInject để đánh giá false positive trên mẫu benign có trigger word. [[18]](#ref18) Đây là hai hướng dẫn nguồn khác nhau: backbone NLU làm điểm khởi đầu và thiết kế đánh giá false positive làm tham khảo cho tác vụ guardrail.

**Câu hỏi nghiên cứu đề xuất:** Khi đánh giá trên cùng bộ kiểm thử có provenance và các nguồn/nhóm prompt được tách khỏi train, mô hình fine-tune từ `microsoft/deberta-v3-base` có phân biệt hữu ích giữa benign, Prompt Injection và jailbreak hay không, đặc biệt khi quy tắc phân lớp phải xử lý các trường hợp có thể mang đồng thời đặc điểm của hai kiểu tấn công?

Trước khi huấn luyện, nhóm cần chọn một quy tắc nhãn có thể tái lập: (a) ba lớp loại trừ nhau cùng quy tắc ưu tiên được công bố, hoặc (b) phân loại phân cấp/đa nhãn nếu cách gán nhãn cho phép các nhãn chồng lấn. Với phép so sánh, cần cố định nguồn dữ liệu, khử trùng lặp theo prompt/nhóm, giữ tập kiểm thử ngoài nguồn hoặc ngoài nhóm, và dùng cùng giao thức cho baseline TF-IDF cùng mô hình nhóm. Checkpoint nhị phân công khai chỉ có thể làm đối chứng nhị phân sau khi xác định rõ cách ánh xạ; chúng không thể cung cấp dự đoán tách riêng Prompt Injection và jailbreak nếu đầu ra của checkpoint không có hai lớp đó.

Báo cáo thực nghiệm sau này nên nêu macro-F1, precision/recall theo lớp, false-positive rate trên benign và confusion matrix; độ trễ CPU P95 chỉ được báo cáo sau khi đo trên cấu hình phần cứng/phần mềm được ghi rõ. Các chỉ số này hiện là kế hoạch đo, không phải kết quả PI-Guard. Fine-tune backbone tự nó chưa xác định được đóng góp nghiên cứu; đóng góp cần được chứng minh qua schema nhãn, dữ liệu có provenance, giao thức đánh giá chung và phân tích lỗi. Theo ranh giới Chương 2, nội dung ở đây chỉ là ma trận y văn và đề xuất; huấn luyện/đo đạc thuộc milestone thực nghiệm sau.

## References (Tài liệu tham khảo)

<a id="ref9"></a>**[9]** P. He, J. Gao, and W. Chen, “DeBERTaV3: Improving DeBERTa using ELECTRA-Style Pre-Training with Gradient-Disentangled Embedding Sharing,” 2023. Thông tin và PDF cục bộ: [REFERENCES_LOG.md, mục 9](../../../References/REFERENCES_LOG.md#ref9).

<a id="ref18"></a>**[18]** H. Li, X. Liu, N. Zhang, and C. Xiao, “PIGuard: Prompt Injection Guardrail via Mitigating Overdefense for Free,” *Proceedings of ACL 2025*, pp. 30420–30437. [ACL Anthology](https://aclanthology.org/2025.acl-long.1468/) · [PDF mở](https://aclanthology.org/2025.acl-long.1468.pdf) · [REFERENCES_LOG.md, mục 18](../../../References/REFERENCES_LOG.md#ref18).

<a id="ref20"></a>**[20]** Meta AI / Purple Llama, “Prompt Guard 86M Input Guardrail,” 2024. [Hugging Face](https://huggingface.co/meta-llama/Prompt-Guard-86M) · [REFERENCES_LOG.md, mục 20](../../../References/REFERENCES_LOG.md#ref20).

<a id="ref30"></a>**[30]** M. Jacob et al., “PromptShield: Deployable Detection for Prompt Injection Attacks,” *ACM CODASPY 2025*, pp. 341–352. [arXiv:2501.15145](https://arxiv.org/abs/2501.15145) · [Mã tác giả](https://github.com/wagner-group/PromptShield) · [REFERENCES_LOG.md, mục 30](../../../References/REFERENCES_LOG.md#ref30).

### Model-card and public repository sources

- PIGuard, revision `dd78b24e330193a22d2293ac66922dd4f982f563`: [Hugging Face](https://huggingface.co/leolee99/PIGuard) · [GitHub](https://github.com/leolee99/PIGuard).
- Meta Prompt Guard 86M: [Hugging Face](https://huggingface.co/meta-llama/Prompt-Guard-86M) · [GitHub](https://github.com/meta-llama/PurpleLlama/tree/main/Prompt-Guard).
- PromptShield DeBERTa: [GitHub](https://github.com/wagner-group/PromptShield) (Jacob et al., CODASPY 2025).
- Llama Prompt Guard 2 86M: [Hugging Face](https://huggingface.co/meta-llama/Llama-Prompt-Guard-2-86M) · [GitHub](https://github.com/meta-llama/PurpleLlama/tree/main/LlamaFirewall) (Meta, 2025; arXiv:2505.03574).
- DeBERTa-v3-base, model card và giấy phép: [Hugging Face](https://huggingface.co/microsoft/deberta-v3-base).
