# L3 subtype v0.2.5 — nghiên cứu bổ sung nguồn dữ liệu, round 52

**Ngày:** 2026-10-24
**Trạng thái:** đã kiểm toán thêm một tập train ứng viên; chưa nhận dòng nào vào package, chưa tạo dataset version mới, chưa train.

## Scope boundary declaration

- **IN-SCOPE:** rà dữ liệu train công khai đã ghim revision; đối chiếu chỉ với train/validation v0.2.5; đọc metadata nguồn, nhãn, lineage và license; cập nhật inventory, reference log và báo cáo.
- **OUT-OF-SCOPE:** đọc test payload v0.2.5 hoặc test payload upstream của ứng viên; ghi vào package v0.2.5; chấm điểm test, chọn threshold/checkpoint, huấn luyện model; truy cập nguồn bị loại trừ.

## Kết quả đáng chú ý: thêm một ứng viên train 177 dòng

Đã stage riêng train split của 3nesdeniz/english-prompt-injection-3k tại revision 87f017347aff7887b1de0d9457c9ec01bf7ba8b5. SHA-256 file khớp publisher LFS hash: f419b218dc4a8e9e879d02e7caef5fa424dbc71ae025a173f277cad6e7c65a12. Chỉ tải README và train.parquet; không tải validation/test upstream.

Card phân lớp mẫu theo class và attack_family, mô tả tám họ tấn công prompt injection, trong đó có jailbreak_persona, đồng thời ghi dữ liệu được mở rộng xác định từ template do người thiết kế. Phép lọc label=1, class=injection, attack_family=jailbreak_persona cho 177 dòng, cả 177 đều có văn bản chuẩn hóa duy nhất. Đây là proxy BOTH theo taxonomy nguồn, chưa phải nhãn gold PI-Guard. [[167]](#ref167)

So khớp exact normalized text với train/validation hiện tại cho 0/177 overlap. So khớp chính xác prefix 35 ký tự với cùng hai split cũng cho 0/177. Khi rà toàn bộ 2.453 dòng source train thay vì chỉ 177 ứng viên, có 5 prefix trùng với train và 2 với validation; các dòng đó thuộc instruction_override, system_prompt_extraction hoặc benign, không nằm trong nhóm 177. Đây là bộ lọc gần trùng bảo thủ, không chứng minh độc lập ngữ nghĩa.

Nguồn không có trường template_id, scenario_id hay group_id. Dù card mô tả split theo scenario và template, không thể đếm số kịch bản độc lập chỉ từ schema đã phát hành. Nguồn cũng cùng tác giả/source family với 3nesdeniz Agentic Prompt-Injection Boundary Pairs. Vì vậy giữ 177 dòng ở trạng thái candidate; chưa tính vào support và không dùng test split của cùng source family làm test held-out sau khi train từ nguồn này.

Nếu sau review được nhận, số BOTH train theo dòng có thể tăng từ 52 lên 229. Con số 229 là phép cộng có điều kiện; chưa chứng minh có 229 nhóm độc lập và chưa thay đổi trạng thái gate.

## Các nguồn được rà thêm

### SaTML 2024 CTF — dữ liệu lớn nhưng là hội thoại nhiều lượt

ETH Zurich SPY Lab phát hành 137.151 attack chats, giấy phép MIT. Nhiệm vụ là tìm secret được giấu trong system prompt; bản ghi là hội thoại tấn công nhiều lượt kèm defense và secret guesses. Đây là nguồn triển vọng cho nghiên cứu prompt attack theo hội thoại, nhưng card/schema công khai không gán nhãn riêng từng bản ghi theo hai trục PI method và JB objective, không có cohort benign đầu vào tương ứng, và đơn vị dữ liệu không khớp classifier một prompt mỗi dòng. Không tính vào BOTH hay support v0.2.5. [[184]](#ref184), [[185]](#ref185)

### PromptSentinel — ba lớp riêng, không có BOTH

Snapshot hiện tại báo 156.802 prompt duy nhất, với ba lớp benign, jailbreak và injection; schema có source_dataset, all_sources và source_license. Dataset được tổng hợp từ 13 nguồn, có cả nguồn đã xuất hiện trong các vòng audit PI-Guard. Hub đánh dấu gated và license là other; một số nguồn con không thương mại hoặc chưa rõ điều khoản. Không có lớp co-label BOTH. Chỉ xem xét riêng cho lớp đơn sau khi có quyền truy cập, lọc license theo dòng, lineage và overlap. [[186]](#ref186)

### Aegis classifier và Mindgard — tách nhãn hoặc chỉ ghi kỹ thuật

Aegis classifier v1 dùng năm lớp mutually exclusive: benign, direct/indirect injection, jailbreak và PHI extraction. Báo cáo ghi một số mẫu HackAPrompt có phong cách jailbreak nhưng được gán injection; đây là bằng chứng về ranh giới nhãn chưa ổn định, không phải co-label theo dòng. [[187]](#ref187)

Mindgard công bố một hỗn hợp prompt injection và jailbreak đã biến đổi để kiểm tra né guardrail, nhưng trường attack_name mô tả kỹ thuật biến đổi; card không cung cấp hai nhãn PI/JB riêng cho từng prompt. License là CC BY-NC 4.0. Không cộng vào BOTH. [[188]](#ref188)

## Trạng thái gate và quyết định

Package hiện tại không đổi: train BOTH 52/100, trong đó audit direct-evidence xác nhận 24 dòng; validation BOTH 30/30. Test có 303 dòng nhưng không có JB hoặc OTHER_ATTACK. Fit và test scoring vẫn bị chặn theo SUPPORT_GATE.json. Test payload không được đọc trong round này.

**Quyết định:** chưa nhận candidate 3nesdeniz, chưa tạo dataset version mới, chưa train. Snapshot 177 dòng tăng đáng kể tiềm năng support theo dòng, nhưng cần truy vết nhóm template/scenario và lập test source-held-out mới đủ năm lớp. CTF SaTML không thể thay thế bước đó do dữ liệu nhiều lượt và chưa có taxonomy hai trục theo bản ghi.

## Bước tiếp theo

1. Xin publisher cung cấp template/scenario IDs cho English Prompt Injection 3K hoặc tái dựng và review nhóm template từ train split; không mở test split.
2. Hoàn tất audit độc lập license, lineage và exact/near-duplicate cho các candidate còn lại trước khi nhận vào dataset version mới.
3. Tìm hoặc xin quyền truy cập một nguồn có co-label PI method + JB objective theo dòng để tạo test source-held-out; bảo đảm đủ BOTH, PI, JB, OTHER_ATTACK và benign.
4. Chỉ sau khi các gate train, validation và test mới đạt mới fit và báo cáo metrics train/validation/test.

## Artifacts

- [Candidate inventory round 52](../../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/candidate_screen_20261024_round52/candidate_screen_20261024_round52.json)
- [Candidate audit 3nesdeniz English 3K](../../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/3nesdeniz_english_prompt_injection_3k_20261024_round52/CANDIDATE_AUDIT_ROUND52.json)
- [Train snapshot](../../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/3nesdeniz_english_prompt_injection_3k_20261024_round52/train.parquet)
- [Support gate v0.2.5](../../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/versions/v0.2.5/SUPPORT_GATE.json)

## References used

[[167]](#ref167), [[184]](#ref184), [[185]](#ref185), [[186]](#ref186), [[187]](#ref187), [[188]](#ref188).
