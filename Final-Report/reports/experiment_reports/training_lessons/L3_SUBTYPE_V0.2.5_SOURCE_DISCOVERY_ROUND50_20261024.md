# L3 subtype v0.2.5 — rà soát nguồn dữ liệu, round 50

**Ngày:** 2026-10-24  
**Trạng thái:** nghiên cứu nguồn; chưa tạo dataset version mới, chưa train.

## Scope Boundary Declaration

- **IN-SCOPE:** rà soát card/schema, revision, nhãn, nguồn gốc, giấy phép, split và bằng chứng cho nhãn BOTH; lập danh sách candidate và tính mức hỗ trợ tối đa có điều kiện.
- **OUT-OF-SCOPE:** tải hoặc nhập candidate vào dataset v0.2.5, thay đổi split/test đã đóng băng, huấn luyện model, tính metrics, truy cập nguồn bị loại trừ.
- Round này không mở nội dung file local `test.jsonl`. Tuy nhiên, test v0.2.5 không còn được xem là blind cho phát triển tiếp theo sau sự cố truy cập nguồn đã ghi ở phần 5.

## 1. Tiêu chí và trạng thái gate

Chỉ xác nhận BOTH khi cùng một dòng hoặc một nhóm taxonomy có căn cứ trực tiếp cho cả **phương thức prompt injection** và **mục tiêu jailbreak**. Nhãn harmful/unsafe, một category đơn, hoặc cụm từ “jailbreak/prompt injection” ở mô tả chung không đủ để tự gán BOTH. Các biến thể được sinh từ cùng seed không được cộng như các kịch bản độc lập.

Gate hiện tại của gói v0.2.5 vẫn là `BLOCKED_LOW_SUPPORT`: train có 52 BOTH trên mục tiêu 100; validation có 30/30; `fit_allowed=false`. Test có 303 dòng nhưng không có JB hoặc OTHER_ATTACK, vì vậy thiếu coverage năm lớp để chấm sau train. Audit nguồn hiện xác nhận trực tiếp 24 dòng train có co-label hai trục; phần còn lại của 52 dòng là nhãn proxy theo taxonomy nguồn, chưa có human review. Không có model hay metrics v0.2.5.

## 2. Nguồn mới có tiềm năng

### Bordair/bordair-multimodal

Đã ghim metadata Hugging Face tại revision `398e3f875ffd32ec2e6817a95feebfcbae41643a`. Card định nghĩa tập là runtime prompt injection và loại pure jailbreak không hijack task; taxonomy v1 có nhóm `dan_jailbreak` với 20 seed. Đây là candidate BOTH theo thiết kế nguồn, nhưng chưa phải 20 dòng train đã xác minh: chưa kiểm tra từng record, chưa phân bổ split theo source/seed, chưa khử trùng lặp với v0.2.5 hay các candidate khác. Các file v1/v2 mở rộng seed qua template và phương thức đa phương thức; số biến thể không tương đương số kịch bản độc lập. Card mô tả thêm 13.230 lượt tấn công từ game red-team, nhưng chỉ có nhãn phát hiện nhị phân và không công bố nhãn mục tiêu theo từng dòng nên không cộng chúng vào BOTH. [[173]](#ref173)

Card HF ghi tổng 516.588 dòng khi tính cohort live; bảng version trong repository ghi 503.358 dòng cho v1–v5 và nguồn external, phần chênh đúng 13.230 dòng live. Đây là khác biệt phạm vi cộng cohort, không phải bằng chứng về 13.230 BOTH. Card ghi MIT, nhưng metadata API của Hub không có SPDX license và cây file được liệt kê không có LICENSE riêng; cần xác minh điều khoản và quyền của nguồn thành phần trước khi dùng. Card cũng nêu nhãn theo category/seed, không có human review từng dòng và không có chỉ số inter-rater agreement. Vì thế chưa nhập dữ liệu.

### AIDataFdn/promptinjection

Đã ghim revision `99426e65f23ddfb4e19efe1984618a8c61e2d1c6`; Hub metadata ghi Apache-2.0. Card báo cáo 731.908 dòng và 107.156 attack rows trong 13 category. Schema có một category cho mỗi dòng, như Jailbreak, Override, RoleHijack hoặc Indirect/CrossPrompt; không có co-label phương thức PI × mục tiêu JB. Vì vậy nguồn này không bổ sung BOTH trực tiếp. Có thể đánh giá riêng cho PI/JB đơn trục sau khi kiểm tra lineage và overlap. [[174]](#ref174)

## 3. Nguồn chờ quyền truy cập hoặc kiểm chứng

| Nguồn | Tín hiệu metadata | Quyết định hiện tại |
|---|---|---|
| Cogensec Jailbreak Corpus v0.3 | Card báo cáo 1.175 dòng có `technique_primary=prompt_injection` trong corpus jailbreak 59.508 dòng; không công bố count này theo split. Publisher nói nhãn technique/harm dựa trên rule yếu; 51% technique là `other`, 92% harm là `unknown`; nguồn tổng hợp 14 dataset. | Candidate BOTH tiềm năng lớn nhất, nhưng không cộng vào support: gated, chưa chấp nhận điều khoản; cần split-level count, row review và kiểm toán overlap/lineage. [[163]](#ref163) |
| AEGIS Multilingual Guard | Báo cáo tác giả nêu 188.109 dòng, trong đó 21.544 dòng multi-label; chưa nêu bao nhiêu dòng có đồng thời PI và JB. Bản preview công khai có 1.200 dòng, nhưng schema chỉ có một `technique` mỗi dòng (87 `jailbreak`, 63 `prompt_injection`). Full dataset cần yêu cầu từ tác giả; preview dùng giấy phép responsible-AI tùy chỉnh và nhãn mẫu phần lớn sinh bởi LLM, chưa native-reviewed. | Candidate tiềm năng nhưng không cộng 21.544 vào BOTH. Cần full row-level label counts, điều khoản sử dụng, split/provenance và overlap audit. [[143]](#ref143), [[145]](#ref145) |
| CatBarks/pi_c0_to_c8_sampled | Viewer công bố 2.570 dòng train, 13 nguồn, `source_label` cùng `primary_label`; thống kê schema cho biết `multi_labels` rỗng. Hub không khai báo license; provenance có thể chồng lên các nguồn đã dùng. | Không cộng support: chưa có license, chưa có quy ước co-label hai trục, và lineage tổng hợp cần kiểm tra. [[175]](#ref175) |
| Necent LLM Jailbreak & Prompt-Injection | Có `prompt_adversarial` và `prompt_harmful` độc lập; nguồn 30+ dataset. | Không đủ để xác nhận BOTH: harmful prompt không đồng nghĩa mục tiêu jailbreak; gated và giữ nguyên giấy phép từng nguồn. [[153]](#ref153) |
| Quickium Prompt Security v0 | Có domain PI/JB riêng; card nêu không có dòng JB+PI compound trong release. | Không bổ sung BOTH trong snapshot đã rà. [[151]](#ref151) |
| AIDataFdn Prompt Injection v3 | Nhiều lớp PI/JB và 107.156 attack rows theo card. | Có thể hữu ích cho từng lớp riêng, không có co-label hai trục. [[174]](#ref174) |

## 4. Mức tăng support có điều kiện

Từ nguồn đã staged ở các round trước: 24 dòng direct-evidence hiện có + 35 candidate của 3nesdeniz + 4 candidate của pr1m8 = tối đa 63 trước dedup giữa các candidate và bước nhận dữ liệu. Nếu thêm 20 seed `dan_jailbreak` của Bordair, tổng trần sơ bộ là 83/100, còn thiếu ít nhất 17 ngay cả khi mọi candidate đều đạt kiểm tra. Đây chỉ là trần để lập kế hoạch; 35, 4 và 20 chưa được nhập, 3nesdeniz/pr1m8 chưa qua kiểm tra license/split đầy đủ cho version mới, và cross-source overlap chưa được kết luận. Các biến thể template của Bordair không được dùng để bù khoảng thiếu.

3nesdeniz có 35 dòng train ở category prompt injection + attack family roleplay jailbreak, có target boundary và nhóm scenario; audit round 48 ghi không exact-overlap với train/validation hiện tại. pr1m8 có 4 dòng ứng viên với category/target cho thấy injection hướng tới jailbreak, nhưng snapshot không có split chính thức và audit round 49 ghi một prefix-35 near-duplicate cần xử lý. Hai nguồn này vẫn là candidate, chưa phải support đã nhận.

## 5. Test boundary và sự cố truy cập

Source map của gói hiện dùng `zachz/prompt-injection-benchmark` làm test-only source với revision `dc0072ad6af8d1be049cdb60959e3ff51df4bcae`. Ở round trước, một lệnh tìm kiếm local quá rộng đã phát ra tên/path của `test.jsonl` nhưng không phát nội dung dòng; sau đó public viewer của đúng upstream source hiển thị một số prompt và category. Vì test local được dựng từ chính source này, không thể đảm bảo test còn blind cho các quyết định phát triển sau này. Exact overlap giữa những ví dụ hiển thị và 303 dòng local chưa được kiểm tra; không có metrics, threshold hay kết quả train nào được tính từ chúng.

Giữ package hiện tại nguyên trạng như hồ sơ data-only. Bất kỳ model fit đủ gate nào về sau cần một test mới source-held-out, chứa đủ năm lớp; không dùng test cũ để lựa chọn model/threshold.

## 6. Kết luận và bước tiếp theo

Round này chưa bổ sung dòng dữ liệu vào v0.2.5. Nguồn thực tế mới có tiềm năng đo được là 20 seed BOTH theo taxonomy của Bordair; mức trần cộng dồn mới là 83/100 trước dedup và review. Vì vậy gate train vẫn đóng.

Thứ tự hợp lý cho lượt intake kế tiếp: (1) xin/thiết lập quyền truy cập và xác nhận terms cho Cogensec nếu người dùng chọn nguồn này; (2) snapshot Bordair tại revision đã ghim, kiểm tra license/lineage và đếm theo seed độc lập, chỉ nhận candidate có evidence hai trục; (3) kiểm tra split, near-duplicate và source-family overlap với v0.2.5 cùng 3nesdeniz/pr1m8; (4) nếu đủ 100 BOTH train hợp lệ, tạo dataset version mới với test source-held-out mới rồi chạy preflight trước khi train. Không đánh giá test hoặc huấn luyện trong round nghiên cứu này.

## Artifacts

- [Candidate screen round 50](file:///D:/Work/Do-an/workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/candidate_screen_20261024_round50/candidate_screen_20261024_round50.json)
- [Support gate v0.2.5](file:///D:/Work/Do-an/workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/versions/v0.2.5/SUPPORT_GATE.json)
- [Source support audit v0.2.5](file:///D:/Work/Do-an/workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/versions/v0.2.5/SOURCE_SUPPORT_AUDIT.json)
- [References log](file:///D:/Work/Do-an/Final-Report/References/REFERENCES_LOG.md)

## References used

[[143]](#ref143), [[145]](#ref145), [[151]](#ref151), [[153]](#ref153), [[163]](#ref163), [[165]](#ref165), [[166]](#ref166), [[173]](#ref173), [[174]](#ref174), [[175]](#ref175).
