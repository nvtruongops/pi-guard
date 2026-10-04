# Đánh giá hướng nghiên cứu sau Review 1 lần 2

**Ngày đánh giá:** 2026-10-03  
**Phạm vi:** so sánh bộ hồ sơ `report for review 1 lan 2` với các báo cáo Review/meeting trước; đánh giá bằng chứng hiện có và tiềm năng phát triển mô hình. Đây là đánh giá tài liệu và nguồn nghiên cứu, không phải kết quả huấn luyện mới.

## Kết luận

Bộ Review 1 lần 2 ngày 2026-10-02 **tốt hơn về chất lượng mô hình nghiên cứu và cách trình bày**: tách rõ hiện trạng với kiến trúc đề xuất, mô tả đúng vai trò L2/L3/API, giới hạn phát biểu theo paper, đặt quy trình chọn ngưỡng trên validation và làm rõ nhãn PI/Jailbreak có thể giao nhau. Tuy nhiên, **chưa có bằng chứng mô hình/cascade tốt hơn**: không có checkpoint PI-Guard đã huấn luyện, không có đo lường routing có điều kiện hay đánh giá cascade end-to-end.

Đánh giá tiềm năng: **tốt cho một đồ án ứng dụng nếu thu hẹp câu hỏi và hoàn tất kiểm định; đóng góp phương pháp hiện ở mức giả thuyết, chưa thể gọi là mới hoặc đã có hiệu quả**. Ghép TF-IDF, DeBERTa, chunking và hai cutoff tự nó chưa chứng minh được đóng góp. Điểm có thể tạo giá trị nghiên cứu là kiểm tra có kiểm soát lỗi benign bị chặn nhầm, lỗi theo nguồn tài liệu, và lợi ích thật của việc chỉ chuyển một số chunk sang mô hình ngữ nghĩa.

## So sánh với các báo cáo trước

| Giai đoạn | Nội dung có thể xác nhận trong repo | So với bộ hiện tại |
|---|---|---|
| Báo cáo Meeting 4/5 và một số đề xuất trước audit | Các bản đang lưu đã được thay bằng ghi chú rút lại: chúng từng chứa metric/latency/cascade ước tính hoặc chưa có protocol khóa nguồn. Các số đó không còn là bằng chứng hợp lệ. | Bộ 2/10 tiến bộ rõ về provenance và không lặp lại các claim đã rút. Không nên nói mô hình mới “đạt điểm cao hơn” các con số cũ. |
| Review 1 đã hiệu chỉnh ngày 2026-09-30 | Đã giới hạn bằng chứng ở baseline TF-IDF trên PIDS-Bench và PIGuard trên dữ liệu của chính PIGuard; đã nói rõ chưa có mô hình ba lớp hay cascade được đo. | Đây đã là nền tảng có kỷ luật. Bộ 2/10 bổ sung kiến trúc ingress/chunk/API, cutoff, hợp đồng luồng và taxonomy; đó là tiến bộ về thiết kế, chưa phải tiến bộ thực nghiệm. |
| Review 1 lần 2 ngày 2026-10-02 | README và các mục 01–08 phân định paper, kết quả cục bộ và giả thuyết PI-Guard; L2 phát route-candidate, L3 xử lý vùng REVIEW, API quyết định cuối. | Đây là bộ mô tả rõ nhất hiện có về hướng mô hình, nhưng bản thân nó vẫn là đề xuất chưa được chạy. |

Các báo cáo Meeting 4/5/6 hiện hành cũng ghi rằng mục tiêu P95/FPR trước đây chưa đạt bằng chứng và không có cascade PI-Guard được huấn luyện, đánh giá. Vì vậy so sánh hợp lệ là “bản mới chặt chẽ hơn về nghiên cứu và kiến trúc”, không phải “kết quả mô hình mới tốt hơn kết quả cũ”. [Trạng thái Review 1 đã hiệu chỉnh](file:///D:/Work/Do-an/workspaces/truongnv/reports/report_for_review1/REVIEW_1_REPORT.md#L7) · [Audit provenance](file:///D:/Work/Do-an/workspaces/truongnv/reports/experiment_reports/WORKSPACE_PROVENANCE_AUDIT_2026-09-30.md#L10) · [Ghi chú rút lại Meeting 5](file:///D:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_reports/TASK_2_5_SOTA_ASSESSMENT_AND_TWO_TIER_PROPOSAL.md#L9)

## Những điểm đã được cải thiện

1. **Ranh giới giữa thiết kế và hiện trạng rõ hơn.** README nói rõ DeBERTa-v3-base mới là backbone tổng quát cần classification head được huấn luyện; chunk routing, upload và cascade chưa phải chức năng hiện có. L2 chỉ phát ALLOW candidate / REVIEW→L3 / BLOCK candidate; API mới là nơi tổng hợp kết quả cuối.
2. **Threshold được đặt đúng vị trí.** Hai cutoff là quy tắc hậu huấn luyện được chọn trên validation, không phải một classifier thứ ba. Tài liệu không lấy số threshold của paper để gán cho PI-Guard và không dùng test để chọn ngưỡng.
3. **Nguồn và nhãn được phân biệt cẩn thận hơn.** Ma trận giải thích Direct/Indirect PI là trục nguồn/đường đưa chỉ thị, còn Jailbreak là trục mục tiêu; hai thuộc tính có thể đồng thời đúng. Đây là bước cần thiết trước khi chốt schema huấn luyện.
4. **Ứng viên chunk và feature có giới hạn.** 256 token/overlap 32 và `char_wb` được ghi là cấu hình cần kiểm định hoặc ablation, không phải kết quả đã được paper chứng minh.

Các điểm này được ghi tại [README thiết kế](file:///D:/Work/Do-an/workspaces/truongnv/reports/report%20for%20review%201%20lan%202/README.md#L20), [protocol threshold](file:///D:/Work/Do-an/workspaces/truongnv/reports/report%20for%20review%201%20lan%202/06_TFIDF_THRESHOLD_ROUTING_PAPER_AUDIT.md#L35) và [taxonomy PI/Jailbreak](file:///D:/Work/Do-an/workspaces/truongnv/reports/report%20for%20review%201%20lan%202/08_PI_JB_ATTACK_TAXONOMY_MATRIX.md#L28).

## Bằng chứng hiện có và giới hạn

- Báo cáo PIDS-Bench ghi nhận baseline TF-IDF + Logistic Regression cục bộ có hard-benign FPR 31.56% trên 808 mẫu văn bản dùng được ở `τ=0.5`; ở cutoff validation-selected `τ=0.518`, chỉ số này là 29.08%, còn structural-OOD benign FPR là 79.18%. Đây là kết quả baseline trên protocol PIDS-Bench, **không phải** số đo cascade hoặc mô hình PI-Guard.
- Báo cáo PIDS-Bench hiện ghi DeBERTa/DistilBERT local matrix còn pending tại thời điểm báo cáo; dù các bảng paper có giá trị tham khảo, không thay chúng bằng kết quả đồ án.
- Audit workspace chỉ giữ các thí nghiệm ghép model–data cùng nguồn paper; các suite cross-paper và fit TF-IDF tự ghép trước đây bị rút. PIGuard NotInject/BIPIA/WildGuard được giữ như lát đánh giá của bản phát hành PIGuard, không phải tập huấn luyện PI-Guard.
- README ngày 2/10 nói rõ chưa có cascade đầu-cuối hoặc conditional routing được đo; upload/parser/OCR và các module huấn luyện trong sơ đồ cũng chưa được triển khai.

Nguồn cục bộ: [PIDS-Bench matrix](file:///D:/Work/Do-an/workspaces/truongnv/reports/experiment_reports/pids_bench_two_tier_evidence_matrix_2026-10-02/REPORT.md#L40) · [giới hạn cascade](file:///D:/Work/Do-an/workspaces/truongnv/reports/experiment_reports/pids_bench_two_tier_evidence_matrix_2026-10-02/REPORT.md#L70) · [README trạng thái mô hình](file:///D:/Work/Do-an/workspaces/truongnv/reports/report%20for%20review%201%20lan%202/README.md#L57) · [provenance và kết quả được giữ](file:///D:/Work/Do-an/workspaces/truongnv/reports/experiment_reports/WORKSPACE_PROVENANCE_AUDIT_2026-09-30.md#L16)

## Tiềm năng và rủi ro nghiên cứu

**Tiềm năng ứng dụng là có thật:** một lớp lexical nhẹ có thể sàng lọc nhanh, còn DeBERTa xử lý những trường hợp khó hơn; chunk/source map có thể giúp giữ vị trí nguồn trong tài liệu; mục tiêu đo false-positive trên hard-benign có ý nghĩa vận hành. Nhưng bằng chứng literature hiện tại yêu cầu kết luận dè dặt:

- Akinrele và Gowda báo cáo hiệu quả detector thay đổi theo regime; paper dùng TF-IDF và DeBERTa làm các baseline, và selective routing của họ không phải phép thử chính xác cho cascade TF-IDF→DeBERTa của PI-Guard. Do đó cascade này là giả thuyết hợp lý để thử, chưa phải phương pháp đã được xác nhận. [Paper arXiv 2605.26999](https://arxiv.org/abs/2605.26999)
- PIDS-Bench cho thấy hard-negative augmentation cải thiện mạnh false positive trên mẫu curated nhưng lợi ích chuyển kém sang mẫu benign lấy từ nguồn ngoài. Thêm “hard negatives” vì thế không đảm bảo tăng điểm trên miền triển khai; phải chia và báo cáo theo nguồn. [Paper PIDS-Bench](https://arxiv.org/abs/2609.15017)
- CrackedPDFs cho thấy detector chỉ đọc text có thể học shortcut: TF-IDF đạt điểm held-out hoàn hảo trên benchmark PDF đó nhưng không qua shortcut audit; mô hình kết hợp đặc trưng tài liệu tốt hơn trong thử nghiệm kiểm soát, nhưng tác giả không tuyên bố đã giải quyết tổng quát hóa sang PDF thật, nguồn chưa thấy hoặc OCR. Điều này làm hướng ingress tài liệu đáng nghiên cứu, đồng thời cho thấy chunk text đơn thuần có thể bỏ mất dấu hiệu bố cục/khả năng hiển thị. [Paper CrackedPDFs](https://arxiv.org/abs/2607.19396)

Vì vậy, **đóng góp tiềm năng không nên được mô tả là “mô hình mới kết hợp hai tầng”**. Một câu hỏi nghiên cứu kiểm chứng được hơn là: *Với cùng tập dữ liệu và cùng operating constraints, cascade theo chunk có giảm lượng gọi DeBERTa mà vẫn giữ attack recall và giới hạn benign FPR so với chạy DeBERTa cho mọi đầu vào không; hiệu quả có giữ được trên nguồn tài liệu chưa thấy hay không?* Đây là giả thuyết, không phải kết luận novelty.

## Lộ trình đề xuất

1. **Chốt task/nhãn trước khi train.** Chọn PI-only binary hoặc mô hình có hai thuộc tính `is_pi` và `is_jb`; không ép Direct PI, Indirect PI và Jailbreak thành ba lớp loại trừ nhau nếu chưa có quy tắc giao nhau. Ghi `delivery_source`, `attack_objective` và loại hard-negative thành metadata.
2. **Đóng băng tập dữ liệu và nguồn.** Tạo train/validation/test theo source, tài liệu gốc và họ attack; tránh near-duplicate hoặc biến thể cùng template đi qua nhiều split. Chỉ dùng hard-benign ở train nếu được phép và giữ các stress set làm holdout.
3. **Lập baseline công bằng.** Đo L2 TF-IDF riêng, L3 DeBERTa riêng, cascade có routing, và DeBERTa chạy toàn bộ đầu vào. Chọn cutoff trên validation rồi khóa trước test; so sánh cùng preprocessing, split, nhãn và thiết lập tài nguyên.
4. **Báo cáo lỗi hai phía, không chỉ một điểm.** Tối thiểu gồm attack recall/attack escape, hard-benign FPR theo provenance, macro-F1, tỷ lệ REVIEW→L3, số lần gọi L3 và latency end-to-end (P50/P95). Dùng nhiều seed hoặc khoảng bất định nếu quy mô cho phép.
5. **Mở rộng sang file/OCR sau khi baseline text ổn định.** Giữ text offset/page/source map và nhãn visibility/placement nếu muốn nghiên cứu hidden document injection; tách bài toán đó khỏi kết quả binary text-only.

**Đề nghị chốt hướng:** bắt đầu bằng baseline nhị phân và ablation hard-negative trên nguồn tách biệt; chỉ giữ cascade làm đóng góp chính nếu nó thắng mô hình đơn ở ràng buộc FPR/recall hoặc chi phí đã định trước. Nếu chỉ tăng macro-F1 IID nhưng không cải thiện false-positive và source-shift behavior, kết quả chưa chứng minh lợi ích triển khai.

## Nguồn chính

- Akinrele & Gowda, [Prompt Injection Detection is Regime-Dependent](https://arxiv.org/abs/2605.26999), arXiv 2026.
- Shire & Kim, [PIDS-Bench](https://arxiv.org/abs/2609.15017), IEEE Access 2026; xem thêm báo cáo protocol cục bộ ở trên.
- Thienpreecha, [CrackedPDFs: A Controlled Benchmark for Hidden Prompt Injection in PDFs](https://arxiv.org/abs/2607.19396), arXiv 2026.
- Tài liệu nội bộ dùng để đối chiếu: [Review 1 đã hiệu chỉnh](file:///D:/Work/Do-an/workspaces/truongnv/reports/report_for_review1/REVIEW_1_REPORT.md#L10), [README Review 1 lần 2](file:///D:/Work/Do-an/workspaces/truongnv/reports/report%20for%20review%201%20lan%202/README.md#L54), [audit provenance](file:///D:/Work/Do-an/workspaces/truongnv/reports/experiment_reports/WORKSPACE_PROVENANCE_AUDIT_2026-09-30.md#L10).
