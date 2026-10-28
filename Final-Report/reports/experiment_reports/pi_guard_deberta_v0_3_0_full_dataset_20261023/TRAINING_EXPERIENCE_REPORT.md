# PI-Guard DeBERTa v0.3.0: full dataset và đánh giá trước training

**Ngày:** 2026-10-23  
**Trạng thái:** Đã tạo đủ train/validation/test và xác minh nguồn; chưa training, chưa tạo checkpoint, chưa chạy inference v0.3.0 trên test.

## Scope boundary declaration

**Trong phạm vi:** đóng gói source-mapped dataset v0.3.0 từ lineage của `D:\Work\Do-an\workspaces\truongnv\shared_data\pi_guard_datasets`; giữ train/validation đã đóng băng; thêm test nguyên trạng để so sánh version; xác minh nhãn, hash, provenance và split; đánh giá sơ bộ dựa trên kết quả test v0.2.0 đã lưu.

**Ngoài phạm vi:** training, tạo checkpoint, inference v0.3.0 trên test, điều chỉnh threshold theo test, hoặc duyệt nhãn thủ công. `human_review_used=false`; nhãn source-mapped là candidate labels, không phải gold labels. [[2]](#ref2) [[3]](#ref3)

## Dataset v0.3.0

Full package: `pi_guard_deberta_3class_source_mapped_v0_3_0`. Trainer tiếp tục dùng package fit-only riêng `pi_guard_deberta_3class_source_mapped_fit_v0_3_0`, không đọc test. [[2]](#ref2) [[6]](#ref6)

| Split | Số dòng | Benign | PI | JB | Source IDs |
|---|---:|---:|---:|---:|---:|
| Train | 33.382 | 8.323 | 14.901 | 10.158 | 9 |
| Validation | 14.971 | 7.692 | 1.381 | 5.898 | 3 |
| Test | 4.200 | 1.500 | 1.500 | 1.200 | 6 |

Ba split có đủ Benign/PI/JB. Kiểm tra độc lập xác nhận không giao row ID, source ID, `group_id` hoặc canonical prompt hash giữa bất kỳ cặp split nào. Test có SHA-256 `890b388a5f5cd3a784c83a3850bd49d4af8046ea893d80209763018daaad1474`, trùng byte-for-byte với test source-family-heldout v0.2.0. [[2]](#ref2) [[3]](#ref3)

### Nguồn và lineage

Manifest gắn dataset với shared data root mà người dùng chỉ định. Lần xác minh này đối chiếu hash các file nguồn trong lineage: 13 snapshot raw theo build manifest v0.2.0; 8 file raw theo build manifest v0.1.1; 2 file PromptScreen theo build manifest v0.1.2; và 5 file TrustAIR theo source provenance. Năm artifact dẫn xuất v0.1.2 cũng khớp hash mà v0.2.0 đã ghi. Chuỗi manifest v0.1.1→v0.1.2 được kiểm tra cùng các file nguồn. Train/validation được lấy từ fit-only package v0.3.0; test được sao chép từ test package v0.2.0. Đây là package dẫn xuất có lineage hash-bound, không phải lần dựng lại toàn bộ dữ liệu từ raw files. [[2]](#ref2) [[3]](#ref3)

Các nhãn giữ nguyên source-native taxonomy mapping. Không có human review hoặc gold-label adjudication; metadata quyền sử dụng vẫn ở trạng thái mô tả/pending. Năm artifact v0.1.2 được ghi riêng là input dẫn xuất để provenance không nhầm chúng với raw snapshot. [[3]](#ref3)

Test đã được dùng để chấm v0.2.0 trước đó. So sánh v0.3.0 với v0.2.0 trên cùng test có thể dùng cho chẩn đoán version, nhưng không phải blind acceptance test. Không có model inference trong quá trình đóng gói. [[1]](#ref1) [[2]](#ref2)

## Bằng chứng test v0.2.0 và đánh giá trước training

Bảng dưới chỉ dùng test native v0.2.0, `N=4.200` mỗi checkpoint: Benign=1.500, PI=1.500, JB=1.200. Các metric là mean ± sample SD của năm baseline checkpoint thuộc version v0.2.0; đây là tóm tắt version đã lưu, không phải coi năm dự đoán trên cùng dòng là năm mẫu độc lập. Chưa có metric test v0.3.0 vì chưa có checkpoint. [[1]](#ref1)

| Version | Benign FPR | Attack Recall | PI Recall | JB Recall | PI→JB | JB→PI | Trạng thái |
|---|---:|---:|---:|---:|---:|---:|---|
| v0.2.0 | 16,33% ± 1,53 điểm % | 86,67% ± 0,96 điểm % | 42,55% ± 2,61 điểm % | 76,95% ± 1,52 điểm % | 44,87% | 8,80% | Đã chấm trên test native |
| v0.3.0 | Chưa có | Chưa có | Chưa có | Chưa có | Chưa có | Chưa có | Chưa training/inference |

Trên năm confusion matrix v0.2.0 cộng lại, PI→JB là `3.365/7.500 = 44,87%`, JB→PI là `528/6.000 = 8,80%`, tổng nhầm PI↔JB là `3.893/13.500 = 28,84%`. Đây là lỗi subtype theo hướng không cân bằng; pooled Attack Recall không mô tả đủ chất lượng ba lớp. [[1]](#ref1)

### Điều v0.3.0 được thiết kế để cải thiện

- **Ưu tiên giảm Benign FPR ở operating point được chọn:** v0.3.0 chọn checkpoint theo Attack Recall trên validation dưới giới hạn Benign FPR ≤1%; v0.2.0 chọn checkpoint theo validation Macro-F1 rồi áp dụng policy threshold có FPR cap. Đây là thay đổi policy chọn checkpoint, không phải bằng chứng test rằng FPR v0.3.0 sẽ thấp hơn 16,33%. [[4]](#ref4) [[5]](#ref5)
- **Có cơ hội giảm nhầm PI/JB:** v0.3.0 dùng lỗi PI/JB làm tie-break trên validation khi Attack Recall bằng nhau. Test v0.2.0 có PI→JB 44,87%, nhưng không có loss hoặc reweight riêng cho subtype; mức giảm trên test vẫn chưa biết. [[1]](#ref1) [[4]](#ref4)
- **Validation kiểm tra source shift rõ hơn:** validation v0.3.0 giữ riêng 3 source IDs khỏi train; test gồm 6 source IDs khác. Cách chia này cho thông tin selection theo nguồn mới, nhưng train giảm từ 48.353 dòng của v0.2.0 xuống 33.382 dòng, nên có rủi ro mất dữ liệu fit và giảm recall. [[2]](#ref2) [[5]](#ref5)
- **Trọng số Benign `[2,1,1]` chưa phải ý tưởng mới trong ma trận:** v0.2.0 đã có một profile dùng trọng số này. Vì vậy không quy mọi khác biệt tương lai cho class weight; v0.3.0 chỉ có một pilot seed 4 và không cho phép kết luận về độ ổn định giữa seed. [[4]](#ref4) [[5]](#ref5)

**Đánh giá sơ bộ:** mục tiêu có căn cứ nhất của v0.3.0 là chọn operating point/checkpoint thiên về giảm báo động nhầm Benign; giảm PI↔JB là mục tiêu phụ, chưa chắc đạt. Attack Recall có thể thấp hơn trên test nếu giữ FPR thấp dưới source shift. Trước training chưa thể kết luận v0.3.0 tốt hơn v0.2.0 ở metric nào; đây là giả thuyết thiết kế, không phải kết quả thực nghiệm v0.3.0.

## Kiểm tra đã chạy

| Kiểm tra | Kết quả |
|---|---|
| `python datasets/scripts/build_source_mapped_v0_2_0.py --verify` | PASS, exit 0; package v0.2.0 giữ nguyên manifest SHA-256 `d6782f4e…acbab38`. |
| `python datasets/scripts/package_source_mapped_full_v0_3_0.py --verify-existing` | PASS, exit 0; ba split, counts, schema, canonical hash và source/group disjoint đều đúng. |
| `python training/code_versions/v0.3.0/train_3class_deberta.py --preflight-only --dataset-dir datasets/versions/pi_guard_deberta_3class_source_mapped_fit_v0_3_0` | PASS, exit 0; preflight xác nhận fit-only manifest và train/validation hash; test không thuộc package fit. |
| `python -m py_compile datasets/scripts/package_source_mapped_full_v0_3_0.py` | PASS, exit 0. |
| Training/run/checkpoint v0.3.0 | Không chạy; không tạo checkpoint hoặc test prediction. |

Verifier v0.2.0 ban đầu không nhận một số ID `sm_` dù row schema cho phép cả `sm_` và `smv020_`. Đã sửa đúng regex của verifier để khớp schema rồi chạy lại `--verify`; không sửa JSONL, manifest hay test v0.2.0. [[7]](#ref7)

## Bước tiếp theo

Khi bắt đầu training, dùng duy nhất package fit-only v0.3.0 và recipe seed 4 đã khai báo. Sau khi checkpoint và threshold được khóa bằng validation, mới chấm một lần trên test đã đóng băng; báo riêng Benign FPR, Attack Recall, PI/JB recall, hai hướng PI↔JB và confusion matrix. Không chọn lại checkpoint/threshold từ test. [[4]](#ref4)

## Evidence references

<a id="ref1"></a>
1. **Test version report v0.1.7/v0.2.0**, kết quả native test N=4.200, mean±SD và confusion counts: [TRAINING_EXPERIENCE_REPORT.md](file:///D:/Work/Do-an/workspaces/truongnv/reports/experiment_reports/training_lessons/pi_guard_deberta_v0_1_7_v0_2_0_test_version_lessons_20261023/TRAINING_EXPERIENCE_REPORT.md).

<a id="ref2"></a>
2. **Full v0.3.0 dataset manifest**, split counts, hashes, test policy: [DATASET_MANIFEST.json](file:///D:/Work/Do-an/workspaces/truongnv/pi_guard_3class_deberta_candidate/datasets/versions/pi_guard_deberta_3class_source_mapped_v0_3_0/DATASET_MANIFEST.json).

<a id="ref3"></a>
3. **Source inputs and provenance**, shared-data root and verified snapshot hash bindings: [SOURCE_INPUTS.json](file:///D:/Work/Do-an/workspaces/truongnv/pi_guard_3class_deberta_candidate/datasets/versions/pi_guard_deberta_3class_source_mapped_v0_3_0/SOURCE_INPUTS.json), [SOURCE_PROVENANCE.json](file:///D:/Work/Do-an/workspaces/truongnv/pi_guard_3class_deberta_candidate/datasets/versions/pi_guard_deberta_3class_source_mapped_v0_3_0/SOURCE_PROVENANCE.json).

<a id="ref4"></a>
4. **v0.3.0 recipe**, one-seed pilot, checkpoint/threshold selection and class weights: [TRAINING_CONFIG.json](file:///D:/Work/Do-an/workspaces/truongnv/pi_guard_3class_deberta_candidate/training/training_versions/v0.3.0/TRAINING_CONFIG.json).

<a id="ref5"></a>
5. **v0.2.0 recipe and run matrix**, prior Macro-F1 selection and `[2,1,1]` profile: [TRAINING_CONFIG.json](file:///D:/Work/Do-an/workspaces/truongnv/pi_guard_3class_deberta_candidate/training/training_versions/v0.2.0/TRAINING_CONFIG.json).

<a id="ref6"></a>
6. **v0.3.0 fit-only manifest**, train/validation only and explicit absence of test payload: [DATASET_MANIFEST.json](file:///D:/Work/Do-an/workspaces/truongnv/pi_guard_3class_deberta_candidate/datasets/versions/pi_guard_deberta_3class_source_mapped_fit_v0_3_0/DATASET_MANIFEST.json).

<a id="ref7"></a>
7. **v0.2.0 verifier and row schema**, ID pattern compatibility fix: [build_source_mapped_v0_2_0.py](file:///D:/Work/Do-an/workspaces/truongnv/pi_guard_3class_deberta_candidate/datasets/scripts/build_source_mapped_v0_2_0.py), [source_mapped_three_class_row_v2.schema.json](file:///D:/Work/Do-an/workspaces/truongnv/pi_guard_3class_deberta_candidate/datasets/schemas/source_mapped_three_class_row_v2.schema.json).
