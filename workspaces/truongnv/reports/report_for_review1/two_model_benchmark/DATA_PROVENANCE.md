# Nguồn dữ liệu và điều kiện sử dụng

## Scope Boundary Declaration

- **IN-SCOPE:** dữ liệu đầu vào cho lần fit TF-IDF và dữ liệu đánh giá dùng cho cả hai mô hình trong gói này.
- **OUT-OF-SCOPE:** dữ liệu huấn luyện gốc của checkpoint ProtectAI (được mô tả riêng trong model card), dòng LMSYS bị redacted và bất kỳ tập dữ liệu nào của cascade PI-Guard [[45]](../../../References/REFERENCES_LOG.md#ref45) [[46]](../../../References/REFERENCES_LOG.md#ref46).

## Nguồn và phiên bản

Dữ liệu trong gói là [frozen split](#term-frozen-split) PIDS-Bench v3 lấy từ thư mục `data/pids_bench_v3/` của kho mã tác giả, tag `v1.0-pids-bench`, commit `87dc835566b930ee921240874a4939b2c266c2fe` [[45]](../../../References/REFERENCES_LOG.md#ref45). Bản gốc trong workspace nằm ở `workspaces/truongnv/replications/PIDS_Bench_Shire_IEEEAccess2026/upstream/data/pids_bench_v3/`; bản đã dùng cho gói này được sao chép vào [`shared_data/pids_bench_v3/`](shared_data/pids_bench_v3/). `FREEZE_MANIFEST.txt` ghi SHA-256 và số dòng của từng split [[45]](../../../References/REFERENCES_LOG.md#ref45).

## Split đã được giữ trong gói

| File | Số dòng nguồn | Vai trò trong lần chạy |
|---|---:|---|
| `train.csv` | 27.093 | Dữ liệu fit baseline TF-IDF + Logistic Regression. |
| `val.csv` | 3.989 | Dữ liệu validation của pipeline baseline tác giả; kết quả trong bảng so sánh chính dùng ngưỡng cố định 0,5. |
| `test.csv` | 3.918 | Đánh giá chính IID cho cả hai mô hình. |
| `eval_subsets/balanced_subtype_test.csv` | 2.297 | Chẩn đoán theo `attack_type` và FPR benign trên cùng split. |
| `eval_subsets/hard_benign_test.csv` | 1.472 | Đánh giá false positive trên prompt benign khó; 664 dòng không có text trong bản công khai. |
| `eval_subsets/obfuscated_attacks.csv` | 405 | Kiểm tra recall theo kiểu obfuscation. |
| [`ood`](#term-ood)/`domain_ood.csv` | 2.000 | Đánh giá chuyển dịch miền. |
| `ood/structural_ood.csv` | 1.998 | Đánh giá chuyển dịch cấu trúc. |

Tên tập, nhãn và số dòng trên lấy từ manifest của PIDS-Bench v3 [[45]](../../../References/REFERENCES_LOG.md#ref45). Các bản sao dữ liệu trong `shared_data/pids_bench_v3/` đã được đối chiếu SHA-256 với manifest; [SHA256SUMS.txt](SHA256SUMS.txt) còn liệt kê hash của các kết quả/model artifact được đóng gói. File license ghi rõ dữ liệu gộp kế thừa điều khoản của từng nguồn và cần được coi là chỉ dùng cho nghiên cứu/phi thương mại [[45]](../../../References/REFERENCES_LOG.md#ref45).

Trong gói này, `train.csv` được dùng để fit TF-IDF; ProtectAI DeBERTa không được huấn luyện trên các CSV PIDS-Bench và chỉ chạy inference trên các split đánh giá. Model card tách riêng nguồn huấn luyện checkpoint ProtectAI [[45]](../../../References/REFERENCES_LOG.md#ref45) [[46]](../../../References/REFERENCES_LOG.md#ref46).

## [Redaction](#term-redaction) và mẫu số hard-benign

Tập `hard_benign_test.csv` có 1.472 dòng trong manifest, nhưng 664 dòng không có văn bản vì bản phát hành không phân phối nội dung hội thoại LMSYS; không thay các dòng này bằng chuỗi rỗng hoặc dữ liệu tạo mới. Hai lần chạy bỏ 664 dòng redacted và tính FPR trên 808 dòng có text, nên FPR hard-benign ở đây không thể so trực tiếp với FPR dùng đủ 1.472 dòng [[45]](../../../References/REFERENCES_LOG.md#ref45).

## BẢNG THUẬT NGỮ & KHÁI NIỆM HỌC THUẬT NỀN TẢNG (ACADEMIC CONCEPT GLOSSARY)

| Thuật ngữ | Định nghĩa khoa học bản chất | Bối cảnh trong báo cáo PI-Guard | Nguồn gốc / tham chiếu |
|---|---|---|---|
| <a id="term-frozen-split"></a>**Frozen split** | Tập dữ liệu được cố định phiên bản để các lần đánh giá dùng cùng bản ghi và có thể kiểm tra bằng checksum. | PIDS-Bench cung cấp manifest SHA-256 cho tập train/validation/test và các bộ đánh giá. | Manifest và kho dữ liệu PIDS-Bench v3 [[45]](../../../References/REFERENCES_LOG.md#ref45). |
| <a id="term-ood"></a>**Out-of-distribution (OOD)** | Đánh giá trên phân phối đầu vào khác với phân phối dùng để fit hoặc hiệu chỉnh mô hình. | Hai tập OOD kiểm tra chuyển dịch miền và cấu trúc; không thay cho test IID. | Định nghĩa và thiết kế benchmark PIDS-Bench [[44]](../../../References/REFERENCES_LOG.md#ref44). |
| <a id="term-redaction"></a>**Redaction** | Loại bỏ nội dung bị hạn chế khỏi bản phát hành trong khi giữ các trường phi văn bản cần cho kiểm toán. | 664 text LMSYS không được phân phối; giữ nguyên giá trị thiếu và loại khỏi phép đo văn bản. | Quy định dữ liệu trong `DATA_LICENSES.md` [[45]](../../../References/REFERENCES_LOG.md#ref45). |
