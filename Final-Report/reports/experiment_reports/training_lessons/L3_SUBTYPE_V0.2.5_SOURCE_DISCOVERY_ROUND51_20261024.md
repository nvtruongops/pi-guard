# L3 Subtype v0.2.5 — Nghiên cứu nguồn dữ liệu, round 51

**Ngày:** 2026-10-24
**Trạng thái:** nghiên cứu/staging ứng viên; chưa thay đổi dataset version hoặc train model

## Scope boundary declaration

- **IN-SCOPE:** rà metadata, schema, nhãn, provenance và license của các nguồn công khai; stage snapshot CORTYX Gold Core có revision cố định; so khớp fingerprint ứng viên chỉ với `train.jsonl` và `validation.jsonl` hiện có; cập nhật inventory và sổ tham khảo.
- **OUT-OF-SCOPE:** sửa package v0.2.5, đọc hoặc dùng test payload, tạo version dataset mới, fit model, chọn threshold/checkpoint, và truy cập nguồn bị cấm theo `DATA_SOURCE_EXCLUSION_POLICY.md`.

## Tiêu chí BOTH

Chỉ tính BOTH khi cùng một dòng có nhãn hoặc taxonomy nguồn trực tiếp cho thấy cả phương thức prompt injection và mục tiêu jailbreak. Nhãn “attack” chung, nhãn harmfulness, hoặc crosswalk do bên thứ ba gán ở cấp nguồn không được cộng vào support. Nhãn vẫn là proxy theo taxonomy nguồn, không phải gold do PI-Guard gán.

## Kết quả nguồn mới

### CORTYX Gold Core — sáu dòng co-label, ứng viên chưa nhận

Tại revision `abac2c21250510993025796f6f29a7b3cecf6147`, file `data/cortyx_gold_core.jsonl` có 610 dòng; 6 dòng đồng thời mang `prompt_injection` và `jailbreak_attempt`. Toàn bộ 6 dòng nằm trong một source bucket Gold Core. Hub khai báo CC BY 4.0; card mô tả Gold Core là dữ liệu nội bộ được hand-curate, nhưng không ghi source family hoặc citation riêng theo từng dòng. [[178]](#ref178)

Đã stage file và card gốc tại `workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/candidate_screen_20261024_round51/`. Fingerprint so với 54.244 dòng train và 13.530 dòng validation hiện có cho thấy 0 exact normalized-text overlap; 3/6 BOTH có normalized prefix-35 trùng và cần rà near-duplicate trước khi xét nhận. Test không được truy cập. SHA-256 của file staged: `493ac097c21e2518cc449278899ce1e913b2933d7f359c6e2ff7296da662bc2a`.

**Quyết định:** giữ ở trạng thái candidate. Chỉ có tối đa 6 dòng thô từ một source bucket; chưa cộng vào support train. Cần kiểm tra nguồn gốc/điều khoản của Gold Core, đánh giá độc lập các nhãn và xử lý 3 prefix match trước khi dùng trong một dataset version mới.

### Smooth-3 / Cyberec Mechanisms — nhiều co-label nhưng chưa chứng minh BOTH

Tại revision Smooth-3 `dd47798b64ebf0e833ecdbff6b1d73be3e440581`, phép đếm trên cột `labels` của train parquet cho thấy 49.500 dòng; 23.770 có đồng thời `JAILBREAK` + `INSTRUCTION_OVERRIDE`, 1.873 có `JAILBREAK` + `ROLE_HIJACK`, tổng 25.608 dòng có `JAILBREAK` cùng một nhãn mechanism trong hai nhóm đó. Card mô tả đây là taxonomy mechanism được tái gán bằng quy tắc xác định, nhưng không định nghĩa `JAILBREAK` là mục tiêu riêng biệt hay là nhãn bao trùm cho mọi attack. [[179]](#ref179)

Card nêu hai upstream: Qualifire Prompt Injections Benchmark và Jayavibhav Prompt Injection Safety; source schema không giữ lineage từng dòng. Một upstream khai báo CC BY-NC 4.0, upstream còn lại không khai báo license trên Hub; bản sao Cyberec ghi Apache 2.0 nhưng cũng nêu rằng upstream gốc không được phân phối lại. Vì vậy các dòng không thể tách đáng tin cậy theo quyền sử dụng và không được tính vào BOTH. [[179]](#ref179)

**Quyết định:** quarantine khỏi dataset build hiện tại. Cần publisher cung cấp định nghĩa nhãn, lineage row-level và quyền sử dụng tương thích trước khi xem xét lại.

### TrustAIRLab × Bunker Laya — crosswalk không đủ làm source co-label

TrustAIRLab tại revision `a10aab8eff1c73165a442d4464dce192bd28b9c5` có cấu hình jailbreak với trường `jailbreak` dạng boolean; schema công khai không có nhãn prompt-injection cùng dòng. [[176]](#ref176)

Model card Bunker Laya báo cáo 653+5.485 dòng TrustAIRLab được dùng cho câu hỏi `jailbreak_attempt` và `injection_present`, nhưng không phát hành dữ liệu huấn luyện hay bảng ánh xạ row-level; mỗi nguồn chỉ gán những câu hỏi nguồn đó có thể trả lời. Đây là crosswalk của pipeline bên thứ ba, không phải co-label gốc được công bố trên từng dòng TrustAIRLab. Không cộng 653 dòng này vào support. [[177]](#ref177)

### Các nguồn mới khác được loại khỏi BOTH

- Goutam112 Prompt Safety Classifier 100K công bố sáu lớp đơn, trong đó `prompt_injection` và `jailbreak_attempt` là hai lớp riêng; schema không thể hiện compound label. Nguồn có thể hữu ích cho từng lớp sau audit riêng, không tạo BOTH support theo contract hiện tại. [[180]](#ref180)
- Necent tiếp tục không đủ: `prompt_adversarial` không tách PI khỏi JB và `prompt_harmful` mô tả harmfulness, không phải mục tiêu jailbreak; quyền nguồn giữ theo dataset upstream và file bị gated. [[153]](#ref153)

### JailbreakDB — nguồn JB-only tiềm năng, không bổ sung BOTH

JailbreakDB tại revision `2c2141bf74ebbe1fd3666a4b38be8856f6e47a92` khai báo CC BY 4.0 và có trường `jailbreak`, `source`, `tactic`. Card hiện tại báo khoảng 6,6 triệu jailbreak/adversarial rows và 5,7 triệu benign rows; maintainer giải thích `tactic` là cờ xấp xỉ nhị phân về việc có dùng tactic, không phải nhãn PI cụ thể. Vì vậy nguồn này chưa biểu diễn BOTH. [[181]](#ref181)

Bài SoK đi kèm công bố 445.752 jailbreak prompt pairs và 1.094.122 benign prompts, khác quy mô được ghi trên card hiện tại. Chỉ xem đây là nguồn JB-only tiềm năng sau khi xác định đúng snapshot, nguồn con, split, overlap và số dòng thực tế; không cộng support trong round này. [[182]](#ref182)

### NVIDIA Nemotron Safety Guard v3 — ứng viên JB-only đa ngôn ngữ

Snapshot `a3f7ecb3433d1933701a83f18de16c36934a7f51` có license CC BY 4.0; card báo khoảng 514.617 dòng, 12 ngôn ngữ và trường `tag` gồm `jailbreaking`. Nhãn prompt chính vẫn chỉ là safe/unsafe, không có nhãn phương thức PI. Card mô tả dữ liệu mới là synthetic và không có human curation mới; `id` còn liên kết về Aegis 2.0. Số dòng `jailbreaking` theo từng split và overlap với các nguồn train hiện có chưa được xác minh, vì vậy chỉ giữ làm ứng viên JB-only, không tính vào BOTH. [[183]](#ref183)

## Tác động tới support gate

Gate v0.2.5 được ghi nhận ở mức 52/100 package BOTH rows, với 24 dòng strict direct-evidence theo [support gate](../../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/versions/v0.2.5/SUPPORT_GATE.json) và [source support audit](../../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/versions/v0.2.5/SOURCE_SUPPORT_AUDIT.json). Các candidate round 48–50 đưa trần lập kế hoạch lên 83 trước dedup/admission; nếu tính thêm 6 CORTYX thô thì trần lý thuyết là 89/100, còn thiếu ít nhất 11. Nếu loại cả ba prefix-35 match, trần giảm tối đa xuống 86/100. Đây chỉ là phép cộng candidate trước thẩm định, không phải support đã nhận. [[165]](#ref165), [[166]](#ref166), [[173]](#ref173)

**Kết luận:** gate vẫn đóng; chưa tạo version dataset mới và chưa train. Nguồn mới có thể kiểm đếm trực tiếp chỉ thêm sáu dòng thô, chưa đủ để mở gate. Test v0.2.5 không được đọc; theo hồ sơ trước, test cũ đã mất trạng thái blind cho phát triển tiếp theo, nên một fit đủ điều kiện sau này cần test source-held-out mới.

## Bước tiếp theo

1. Rà 6 dòng CORTYX Gold Core và 3 prefix match trong staging, ghi quyết định từng dòng mà không mở test.
2. Hoàn tất license, source-family, exact/near-duplicate và grouped split audit cho candidate 3nesdeniz, pr1m8, Bordair; hiện chưa candidate nào được nhận.
3. Tiếp tục tìm nguồn có taxonomy row-level cùng biểu diễn method PI và objective JB. Không nới nhãn thành harmfulness hoặc suy nhãn từ tên dataset.
4. Chỉ tạo dataset version mới khi support đạt gate sau dedup/review; dựng test source-held-out mới đủ năm lớp, rồi mới train và báo cáo đủ train/validation/test.

