# Audit bổ sung: nguồn JB có paper và overlap

Cập nhật UTC: 2026-10-07T10:28:38.318822+00:00

## Phạm vi

Audit đối chiếu ba snapshot JB với nhau và với pool nguồn cơ sở trước khi thêm JB. Pool cơ sở được tái tạo từ các raw source đã pin; các số liệu overlap dưới đây vẫn là phép so sánh lịch sử trước khi gộp. Trạng thái lấy mẫu hiện hành được đồng bộ theo corpus v5 ngày 2026-10-08.

Trùng lặp là exact match sau Unicode NFKC, casefold và gộp whitespace. Không đo gần trùng hoặc cùng template về ngữ nghĩa. Báo cáo không ghi prompt gốc hoặc hash từng prompt.

## Đếm nguồn

| Nguồn | Dòng đầu vào | Dòng văn bản dùng | Prompt duy nhất sau chuẩn hóa | Lặp thêm | Ghi chú về trường được dùng |
|---|---:|---:|---:|---:|---|
| JailBreakV-28K_text | 20,000 | 20,000 | 5,000 | 15,000 | jailbreak_query; chỉ Template/Persuade/Logic |
| WUSTL_LLMJailbreak | 448 | 448 | 447 | 1 | cột Prompt |
| WhatFeatures_jailbreak_success | 10,800 | 10,800 | 9,884 | 916 | jailbreak_prompt_text |

## Overlap từng cặp

| Nguồn A | Nguồn B | Prompt trùng duy nhất | Tỉ lệ A | Tỉ lệ B | Jaccard | Khác nhãn |
|---|---|---:|---:|---:|---:|---:|
| JailBreakV-28K_text | historical_base_v2 | 0 | 0.00% | 0.00% | 0.00% | 0 |
| WUSTL_LLMJailbreak | historical_base_v2 | 180 | 40.27% | 0.54% | 0.54% | 2 |
| WhatFeatures_jailbreak_success | historical_base_v2 | 0 | 0.00% | 0.00% | 0.00% | 0 |
| JailBreakV-28K_text | WUSTL_LLMJailbreak | 0 | 0.00% | 0.00% | 0.00% | 0 |
| JailBreakV-28K_text | WhatFeatures_jailbreak_success | 0 | 0.00% | 0.00% | 0.00% | 0 |
| WUSTL_LLMJailbreak | WhatFeatures_jailbreak_success | 0 | 0.00% | 0.00% | 0.00% | 0 |

## Pool tự nhiên sau gộp và corpus cân bằng hiện hành

Các số ở bảng dưới phân biệt rõ corpus v3/v4 lịch sử với v5 hiện hành.

| Chỉ số | Giá trị |
|---|---:|
| Pool cơ sở trước khi thêm JB | 33,221 |
| Nhãn pool cơ sở, benign / PI / JB | 22,578 / 9,329 / 1,314 |
| JB mới duy nhất được thêm ở v3 trước khi nhập PromptScreen | 15,151 |
| Trùng với benign/PI ở base lịch sử, mẫu JB mới bị cách ly | 2 |
| Trùng JB đã có, chỉ gộp provenance ở v3 | 178 |
| Pool tự nhiên lịch sử sau gộp, benign / PI / JB | 22,578 / 9,329 / 16,465 |
| Corpus v3 (superseded) | 27,987 (9,329 mỗi nhãn) |
| Corpus v4 (superseded) | 11,718 (3,906 mỗi nhãn) |
| Pool tự nhiên dùng cho v5, benign / PI / JB | 27,376 / 11,282 / 28,593 |
| Tỉ lệ lớp lớn nhất/nhỏ nhất trong pool tự nhiên v5 | 2.53:1 |
| Corpus v5 hiện hành | 40,000 (20,000 benign / 10,000 PI / 10,000 JB) |

Pool tự nhiên được khử trùng lặp trước khi lấy mẫu. Corpus v5 dùng undersampling không hoàn lại, capped-equal theo source stratum và đã có split nội bộ group-aware; xem [README corpus](../README.md) và [split manifest](../splits/split_manifest.json). Quota JB hiện hành: JailBreakV-28K 2.809, PromptScreen 2.809, TrustAIRLab+WUSTL 1.573, WhatFeatures 2.809. Metadata nguồn được giữ trong từng dòng, còn các lần cập nhật được ghi trong [version log](../DATASET_VERSION_LOG.md). Split là phân hoạch nghiên cứu nội bộ, chưa phải holdout benign độc lập ngoài v5.

## Giới hạn ánh xạ

- JailBreakV: chỉ các hàng văn bản thuộc Template, Persuade, Logic; loại các format ảnh. Không dùng redteam_query hoặc RedTeam_2K.csv vì đó là yêu cầu gốc, không phải prompt tấn công. Corpus v5 lấy mẫu primary stratum 2.809 prompt duy nhất từ nguồn này.
- WUSTL: cột Prompt là các jailbreak prompt trong paper. Không gán file MaliciousQueries riêng thành JB. Source stratum TrustAIRLab+WUSTL lấy 1.573 mẫu; 437 dòng corpus giữ WUSTL provenance.
- What Features: jailbreak_prompt_text là attack attempt. original_prompt_text là seed harmful request nên không dùng làm JB. CSV không có trường success/failure; định nghĩa JB ở đây là có ý đồ tấn công, không phải tấn công thành công. Corpus v5 lấy mẫu primary stratum 2.809 prompt từ nguồn này.
- WildJailbreak và MHJ có giới hạn truy cập được ghi trong hồ sơ; không tải dữ liệu gated.

## Tái chạy

Từ thư mục gốc repository:

~~~powershell
uv run --no-project python workspaces/truongnv/training_bases/datasets/project_training/tools/audit_additional_jb_sources.py
~~~
