# PIDS-Bench: nội dung bài báo và mức độ phù hợp với PI-Guard

**Ngày đối chiếu:** 2026-10-03  
**Bản đọc:** PDF cục bộ [PIDS_Bench_IEEEAccess2026_arXiv2609.15017v1.pdf](../../../replications/PIDS_Bench_Shire_IEEEAccess2026/papers/PIDS_Bench_IEEEAccess2026_arXiv2609.15017v1.pdf), đối chiếu arXiv v1 và metadata IEEE Access.  
**Phạm vi:** diễn giải paper và ánh xạ sang câu hỏi về false positive, hard-negative, nhãn và cascade của đồ án; không phải thí nghiệm mới.

## Kết luận nhanh

PIDS-Bench rất phù hợp làm căn cứ cho **cách đánh giá detector prompt-injection**, nhất là đo false positive trên benign khó, theo provenance và dưới distribution shift. Nó cũng trực tiếp hỗ trợ thử hard-negative benign trong đồ án. Nhưng paper **không đánh giá cascade TF-IDF → DeBERTa, chunk routing, latency, hay bài toán ba lớp PI/Jailbreak/benign**. Vì vậy nó không chứng minh cascade của PI-Guard hiệu quả.

Paper gọi **NotInject** là một benchmark/tập đánh giá các benign prompt có trigger words, không phải tên của một lớp thứ ba. Trong PIDS-Bench, hard-negative được thêm vào train với **nhãn benign**; paper không thêm lớp `notinject`. Không nên dùng `not_jb` làm synonym của benign: Jailbreak là mục tiêu tấn công, còn PI là hành vi/đường tấn công; chúng có thể giao nhau. [[PIGuard / ACL 2025](https://aclanthology.org/2025.acl-long.1468/)]

## Bài báo nói gì?

Shire và Kim đề xuất PIDS-Bench vì điểm F1 trên test IID không bộc lộ đủ việc detector chặn nhầm các yêu cầu hợp lệ. Bài cô lập detector gateway nhị phân và đánh giá đồng thời hai phía lỗi: bỏ lọt injection và chặn nhầm benign. Benchmark đóng băng các split, có manifest checksum và bao gồm tập IID, hard-benign, obfuscated attack, domain shift và structural shift. [[arXiv v1](https://arxiv.org/html/2609.15017)] · [[IEEE Access](https://ieeexplore.ieee.org/document/11670335)]

- **Task và nhãn:** binary `injection / benign`. Các subtype injection dùng để phân tích lỗi, không tạo ra nhãn đầu ra ba lớp.
- **Dữ liệu:** corpus chính 35.000 hàng, chia train 27.093, validation 3.989, test 3.918. Năm lát stress có tổng 8.172 hàng; do một số lát biến đổi/tái lấy mẫu hàng test, tổng là 40.479 prompt duy nhất.
- **Hard-benign:** 1.472 prompt benign có bề mặt giống injection, trong đó 872 mẫu từ corpus bên ngoài và 600 mẫu được tuyển chọn/viết theo hướng dẫn. Hai annotator audit một mẫu phân tầng 200 hàng.
- **Detector:** TF-IDF + Logistic Regression, DistilBERT và DeBERTa-v3 được train trên cùng train split; thêm detector prompt-injection có sẵn và mô hình safety làm đối chứng. Không mô hình nào là một tầng trong cascade của paper.
- **Protocol:** threshold của detector nội bộ được chọn bằng grid search trên validation, tối ưu F1, rồi khóa khi đánh giá test/stress. Báo cáo F1 cùng hard-benign FPR, attack recall, robustness và phân rã theo domain/provenance; có năm seed cho neural models.

## Kết quả có ý nghĩa cho đồ án

Ở ngưỡng `τ=0.5`, DeBERTa-v3-FT đạt IID F1 `0.9882`, nhưng hard-benign FPR tổng là `0.3825`; FPR trên phần hard-benign từ nguồn ngoài là `0.3144`. TF-IDF + LR có IID F1 `0.9656`, hard-benign FPR tổng `0.4090`, structural-shift FPR `0.7918`. Đây là số **paper công bố**, không phải kết quả PI-Guard. [[Bảng 6 và Bảng 8 trong paper](https://arxiv.org/html/2609.15017)]

Paper thêm 419 hard-negative benign vào quá trình fine-tune hai transformer. Trên tập curated, FPR của DeBERTa giảm `0.4813 → 0.0010` và DistilBERT `0.4843 → 0.0123`; trên hard-benign nguồn ngoài, DeBERTa gần như không đổi (`0.3144 → 0.3101`) còn DistilBERT giảm vừa phải (`0.4606 → 0.3899`). Tăng pool curated từ 100 đến 419 mẫu không làm FPR nguồn ngoài giảm có hệ thống. Kết luận là hard-negative có thể giúp, nhưng lợi ích phụ thuộc provenance và chưa chứng minh sẽ tổng quát hóa. [[Ablation hard-negative](https://arxiv.org/html/2609.15017#S6.SS3)]

Quét threshold cũng không tìm thấy operating point đồng thời đạt F1 ≥ 0.95 và FPR hard-benign nguồn ngoài ≤ 0.10 cho các detector nội bộ trong benchmark. Mức 0.10 là điều kiện chẩn đoán của paper, không phải ngưỡng triển khai được xác nhận cho PI-Guard. Vì vậy không nên kỳ vọng chỉ chỉnh threshold sẽ xóa lỗi bắt nhầm; cần thử dữ liệu benign phù hợp và đo trade-off với attack recall. [[Phân tích threshold](https://arxiv.org/html/2609.15017#S6.SS2)]

## Mức phù hợp với nghiên cứu PI-Guard

| Hạng mục đồ án | Mức phù hợp | Cách dùng paper |
|---|---|---|
| Phát hiện false positive trên câu benign giống injection | Cao | Kế thừa hard-benign stress set và báo FPR riêng, không gộp vào F1 IID. |
| Bổ sung hard-negative khi huấn luyện | Cao, nhưng là giả thuyết cần thử | Gán ví dụ benign đúng nhãn benign; giữ provenance/source metadata và kiểm tra hiệu quả trên nguồn giữ lại. |
| Mô hình hai tầng TF-IDF → DeBERTa | Thấp ở mức chứng minh trực tiếp | Paper đo các detector độc lập, không router/cascade, không đo chi phí gọi L3. Chỉ mượn được baseline và cách đánh giá. |
| Chunking, upload PDF/OCR, latency/P95 | Không được kiểm tra | Cần thí nghiệm riêng theo pipeline tài liệu của PI-Guard. |
| Lớp `notinject` hoặc `not_jb` | Không được chứng minh | Paper dùng task nhị phân; NotInject là benchmark, còn hard-negative là benign examples, không phải class mới. |

### Khuyến nghị về schema và thí nghiệm

1. Với detector tầng 1 và tầng 2, bắt đầu từ nhãn nhị phân `is_injection`; các câu NotInject/hard-benign phải mang nhãn `benign` nếu thực sự không có ý đồ override/manipulate.
2. Lưu `source`, `hard_negative_type`, `delivery_path` và `attack_objective` làm metadata độc lập. Nếu đồ án cần phân loại jailbreak, định nghĩa `is_pi` và `is_jb` như hai thuộc tính có thể đồng thời đúng, hoặc đặt quy tắc nhãn đa lớp rõ ràng trước khi gán dữ liệu.
3. Không dùng tập benchmark stress làm train rồi lại tuyên bố kết quả trên chính tập đó. Tạo hard-negative train riêng; giữ nguồn/tài liệu/họ template làm holdout để đo chuyển miền.
4. So sánh TF-IDF riêng, DeBERTa riêng, cascade có routing và DeBERTa chạy mọi đầu vào trên cùng split. Chọn cutoff trên validation; báo attack recall/escape, IID FPR, hard-benign FPR theo provenance, structural/domain OOD và chi phí/tỷ lệ L3.

## Phân biệt với số liệu cục bộ của đồ án

- Paper dùng toàn bộ 1.472 hard-benign examples. Bảng evidence matrix cục bộ ghi 664 hàng bị trống text sau license cleanup, nên local hard-benign denominator chỉ còn `n=808`; FPR cục bộ `31.56%` tại `τ=0.5` và `29.08%` tại `τ=0.518` **không thể so trực tiếp** với paper trên `n=1.472`. Xem [báo cáo evidence matrix cục bộ](../../../reports/experiment_reports/pids_bench_two_tier_evidence_matrix_2026-10-02/REPORT.md).
- Báo cáo replication [PIDS-Bench TF-IDF](../../../replications/PIDS_Bench_Shire_IEEEAccess2026/REPORT.md) chỉ xác nhận baseline nhị phân trên test IID 3.918 hàng; không ghi nhận cascade hoặc toàn bộ hard-benign/OOD. IID benign FPR khoảng 5% không thay thế hard-benign FPR.
- Hồ sơ Review 1 lần 2 xác nhận ba route ALLOW candidate / REVIEW / BLOCK candidate và tầng DeBERTa là kiến trúc đề xuất; chưa có số đo cascade. Xem [README thiết kế](../../../reports/report%20for%20review%201%20lan%202/README.md).
- Hai bản ghi local hiện báo khác nhẹ về chỉ số IID `τ=0.5` (ví dụ injection F1 `0.9663` so với `0.9656`). Cần chốt run artifact/prediction CSV nào là nguồn chuẩn trước khi gọi đó là tái lập chính xác; không ảnh hưởng đến kết luận rằng hard-benign là một axis khác và cascade chưa được đo.

## Giới hạn cần giữ khi trích dẫn

PIDS-Bench là benchmark tiếng Anh, single-turn, detector đầu vào tĩnh. Một số shift/obfuscation được dựng có kiểm soát; tập curated hard-benign là stress set chứ không ước lượng tỷ lệ false positive của traffic thực tế. Paper nêu thêm giới hạn audit benign nguồn chính, template-derived attacks và external hard-negative augmentation chưa được thử. Những con số stress-set vì thế cho biết detector có thể vấp ở đâu, không phải dự báo trực tiếp FPR triển khai. [[Giới hạn và hướng tương lai](https://arxiv.org/html/2609.15017#S8)]

## Nguồn

- Shire & Kim, [PIDS-Bench, arXiv:2609.15017v1](https://arxiv.org/html/2609.15017), IEEE Access 2026, [DOI 10.1109/ACCESS.2026.3728186](https://doi.org/10.1109/ACCESS.2026.3728186).
- Li et al., [PIGuard / NotInject, ACL 2025](https://aclanthology.org/2025.acl-long.1468/); benchmark NotInject có 339 benign prompt chứa trigger words và được thiết kế để đo over-defense.
- PIDS-Bench authors' [pinned benchmark release](https://github.com/ShirePyDev/Prompt-Injection-Detection-System/tree/v1.0-pids-bench/data/pids_bench_v3).
