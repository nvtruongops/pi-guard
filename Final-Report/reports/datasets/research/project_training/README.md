# PI-Guard project-training corpus — documentation copy

> This report package contains research docs and metadata. The original 40,000-row corpus, review workbook, raw source snapshots and split payloads are not included. Split JSONL and ID files are local-only under Final-Report/notebooks/data/splits and Git ignores them. The versioned split script operates on an existing local v5 corpus; it does not bundle source data. Source rights and final label policy remain pending; no model was trained or evaluated.

Tài liệu này mô tả corpus ứng viên v5 và split nghiên cứu nội bộ. Lịch sử thay đổi được ghi trong [DATASET_VERSION_LOG.md](DATASET_VERSION_LOG.md); payload gốc không nằm trong bản sao báo cáo.

## Phạm vi

- **Bao gồm:** ánh xạ nhãn theo nguồn, giữ provenance, exact dedup, loại nhóm xung đột, lấy mẫu không hoàn lại theo nhãn và source strata; split nội bộ train/validation/test từ đúng corpus v5.
- **Chưa bao gồm:** phân xử toàn bộ nhãn mơ hồ, kiểm toán semantic near-duplicate đầy đủ, huấn luyện hoặc nghiệm thu mô hình.
- Corpus và raw snapshots hiện dùng cho nghiên cứu nội bộ; PromptScreen còn thiếu provenance/license theo từng prompt.

## Corpus hiện hành — v5.0.0

File chuẩn là balanced_three_label.jsonl (corpus nguồn; payload không được sao chép vào report package). Mỗi dòng có `id`, `text`, `label`, `label_id` và `sources` để truy nguyên về revision, file và dòng trong snapshot gốc.

| Nhãn | Số mẫu | Tỷ lệ |
|---|---:|---:|
| benign | 20.000 | 50% |
| PI | 10.000 | 25% |
| JB | 10.000 | 25% |
| **Tổng** | **40.000** | **100%** |

Đây là corpus ứng viên 2:1:1, không phải train split hay bằng chứng rằng tỷ lệ này tối ưu. Nó được lấy từ pool 67.251 prompt sau exact dedup và loại xung đột: benign 27.376, PI 11.282, JB 28.593. Không lặp hoặc sinh prompt.

### Quota lấy mẫu theo source strata

Quota là số dòng được chọn vào corpus theo primary source stratum; đây không phải kích thước toàn bộ dataset nguồn. Một dòng có thể giữ thêm provenance từ nguồn khác sau khi exact dedup.

| Nhãn | Primary source stratum | Mẫu | Tỷ lệ trong nhãn |
|---|---|---:|---:|
| benign | PromptScreen | 6.667 | 33,34% |
| benign | PromptShield | 6.667 | 33,34% |
| benign | TrustAIRLab | 6.666 | 33,33% |
| PI | PromptScreen | 1.953 | 19,53% |
| PI | PromptShield | 8.047 | 80,47% |
| JB | JailBreakV-28K | 2.809 | 28,09% |
| JB | PromptScreen | 2.809 | 28,09% |
| JB | TrustAIRLab + WUSTL | 1.573 | 15,73% |
| JB | WhatFeatures | 2.809 | 28,09% |

Quota dùng capped equal allocation: chia đều giữa các nhóm nguồn đến khi một nhóm chạm sức chứa; phần còn lại phân bổ đều cho các nhóm còn sức chứa. Vì PI chỉ có 1.953 mẫu PromptScreen, 10.000 PI lấy thêm 8.047 từ pool PI của PromptShield. Cân bằng số nhãn không loại bỏ ảnh hưởng nguồn.

### Ý nghĩa nhãn PromptShield trong corpus ba lớp

Builder dùng `train.json` của snapshot [`hendzh/PromptShield`](../source_datasets/promptshield_hendzh/README.md), revision `a5234cb1f5cdb256600cab64b8c961195b5e8404`. Card nguồn mô tả bài toán nhị phân: `1` là prompt injection attempt và `0` là benign; paper cũng đặt câu hỏi nhị phân có/không có prompt injection. Builder ánh xạ `1 → PI` và `0 → benign` theo nhãn nguồn.

`8.047` là quota PI của PromptShield trong corpus v5, không phải số mẫu của dataset hay số được paper báo cáo: pool sau dedup và loại xung đột có sức chứa 9.329 PI từ PromptShield; PromptScreen đóng góp 1.953 PI; hai quota cộng thành 10.000. Dataset link trong câu hỏi là một repository ID khác, [`gaurav-nimbalkar/PromptShield`](https://huggingface.co/datasets/gaurav-nimbalkar/PromptShield). Corpus hiện tại truy nguyên tới `hendzh/PromptShield`; chưa xác minh hai snapshot đồng nhất theo revision/hash.

Nhãn `0` chỉ có nghĩa theo bài toán PromptShield là không có prompt injection; nguồn không có nhãn jailbreak riêng để phân xử ranh giới ba lớp của đồ án. Vì vậy 6.667 dòng PromptShield được ánh xạ vào `benign` phải được hiểu là **benign theo mapping nguồn**, chưa được adjudicate độc lập để loại trừ JB. Corpus v5 vẫn là corpus ứng viên, không phải gold labels đã phân xử toàn bộ. Xem [dataset card](https://huggingface.co/datasets/hendzh/PromptShield) và [paper PromptShield](https://arxiv.org/abs/2501.15145).

### Đánh giá FPR và giới hạn

Corpus gốc không phải một holdout độc lập. Split nội bộ v5 có 3.034 dòng `benign` trong test, nhưng các dòng này vẫn thuộc pool nguồn của corpus; trong đó có mapping PromptShield `0 → benign` chưa được phân xử riêng với JB. Vì vậy chưa có **holdout benign độc lập bên ngoài v5**. Pool còn 7.376 benign sau khi lấy mẫu; chỉ nên lập holdout ngoài sau khi gom nhóm prompt/template và kiểm tra near-duplicate. Khi đánh giá, tính `FPR = (benign dự đoán PI + benign dự đoán JB) / tổng mẫu có nhãn benign trong tập đánh giá`, nêu rõ nguồn và trạng thái adjudication, và báo khoảng tin cậy nhị thức. NIST trình bày cách ước lượng tỷ lệ false alarm và khoảng tin cậy [tại đây](https://nvlpubs.nist.gov/nistpubs/TechnicalNotes/NIST.TN.2119.pdf).

Exact dedup dùng Unicode NFKC, casefold và gộp whitespace. Semantic near-duplicates chưa được tự động loại; WhatFeatures giữ `prompt_name`/`jailbreak_prompt_name` trong provenance để hỗ trợ nhóm prompt sau này. Nên chia theo nhóm, giữ prompt cùng family trong cùng một partition, và báo cáo metric theo nguồn; `StratifiedGroupKFold` giữ nhóm không chồng lấn và cố gắng bảo toàn tỷ lệ lớp [theo tài liệu scikit-learn](https://scikit-learn.org/stable/modules/cross_validation.html?highlight=cross_validate).

PromptScreen là arXiv preprint; dữ liệu tổng hợp thiếu provenance/license ở mức từng prompt. Vì vậy corpus được giữ local; chưa tuyên bố quyền phát hành hoặc tổng quát hóa qua nguồn.

## Split nghiên cứu nội bộ của v5

Theo chỉ đạo ngày 08/10/2026, corpus v5 đủ để **tạo split nội bộ**. [Manifest split](splits/split_manifest.json) khóa SHA-256 của corpus/manifest nguồn, seed 42, ba tệp JSONL và ba danh sách ID; mỗi dòng gốc xuất hiện đúng một lần. Tỷ lệ mục tiêu là 70/15/15; tỷ lệ thực tế lệch nhẹ vì không cắt nhóm prompt:

| Tập | Tổng | benign | PI | JB |
|---|---:|---:|---:|---:|
| Train — Final-Report/notebooks/data/splits/train.jsonl (local-only) | 28.280 | 13.931 | 6.966 | 7.383 |
| Validation — Final-Report/notebooks/data/splits/validation.jsonl (local-only) | 5.858 | 3.035 | 1.517 | 1.306 |
| Test — Final-Report/notebooks/data/splits/test.jsonl (local-only) | 5.862 | 3.034 | 1.517 | 1.311 |

Nhóm dùng `prompt_name` khi WhatFeatures có metadata đó và tìm ứng viên gần trùng bằng 5-word shingles/LSH; cặp ứng viên chỉ nối khi Jaccard ít nhất 0,85. Đây là phép tìm **xấp xỉ**, không chứng minh hết trùng lặp ngữ nghĩa. Có 105 nhóm chứa hơn một nhãn; nhóm lớn nhất có 2.834 dòng. Do không tách nhóm này, **primary source stratum** WhatFeatures có 2.675/62/72 dòng trong train/validation/test: cần nêu lệch nguồn khi báo metric. Không mẫu nào bị loại thêm khỏi v5. Split không giải quyết quyền sử dụng của PromptScreen hay quy tắc phân xử nhãn chính thức.

Split được xác minh trên workspace nguồn ngày 2026-10-09; các tệp split và manifest trong bản sao giữ nguyên hash đã khóa. Mã sinh/kiểm tra split được lưu tại [split_v5_dataset.py](../../../../scripts/split_v5_dataset.py). Lệnh `--verify` chỉ đọc; `--apply` từ chối ghi đè thư mục split đã tồn tại. Replay của manifest frozen đã PASS trên Python 3.11.16 và 3.14.7.

## Tệp xem dữ liệu

balanced_three_label_review.xlsx (workbook nguồn không được sao chép vào report package) đồng bộ với corpus v5. Sheet `Data` có header; `Data Dictionary` mô tả các cột; prompt vượt giới hạn Excel được nối ở `Text Continuation`. JSONL vẫn là bản chuẩn.

## Kiểm chứng và giới hạn của bản sao

Tại workspace nguồn, corpus verifier xác nhận 40.000 dòng và source provenance; bundle verifier xác nhận hash/links; split verifier xác nhận hash, coverage ID và text-family disjointness. Script split công khai cần corpus v5 cùng `manifest.json` trong một thư mục local được truyền bằng `--dataset-root`; payload corpus, workbook, raw snapshots và các file split không được sao chép vào report package. Bộ tính cost cộng tuần tự để phép replay giữ cùng assignment trên các runtime Python đã kiểm tra.

Ví dụ kiểm tra split local (đường dẫn dưới đây là placeholder, không phải dữ liệu trong repository):

```bash
python Final-Report/scripts/split_v5_dataset.py --dataset-root "<LOCAL_PROJECT_TRAINING_DIR>" --verify
```

[manifest.json](manifest.json) ghi source hashes, pool counts, quota theo source và output hashes. [Split manifest](splits/split_manifest.json) ghi trạng thái split, row counts và giới hạn. Các thư mục [source_datasets](../source_datasets/) và [benchmarks](../benchmarks/) ở đây chỉ chứa tài liệu nghiên cứu; raw payloads vẫn ở ngoài report package.
