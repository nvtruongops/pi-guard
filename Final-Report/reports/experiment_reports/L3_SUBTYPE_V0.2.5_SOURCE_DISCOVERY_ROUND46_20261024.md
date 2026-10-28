# PI-Guard L3 subtype v0.2.5 — báo cáo tìm nguồn dữ liệu, vòng 46

Ngày: 2026-10-24

## Scope Boundary Declaration

**IN-SCOPE:** tìm và ghim nguồn công khai có thể bổ sung BOTH/JB; kiểm tra license, schema, support, trùng lặp chính xác với train/validation v0.2.5; lưu audit để quyết định cho dataset version kế tiếp.

**OUT-OF-SCOPE:** sửa dataset/support gate v0.2.5; thêm dòng dữ liệu vào bất kỳ split nào; mở payload test; train hoặc chấm model; nhận điều khoản truy cập gated; truy cập nguồn bị loại trừ.

## Trạng thái v0.2.5

Train có 54.244 dòng và 52 case BOTH, thấp hơn gate 100; validation có 13.530 dòng và 30 BOTH. Metadata test có 303 dòng với BOTH=35, PI=165, JB=0 và OTHER_ATTACK=0; `fit_allowed=false`, `test_scoring_allowed=false`. [Manifest](../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/versions/v0.2.5/DATASET_MANIFEST.json) · [Support gate](../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/versions/v0.2.5/SUPPORT_GATE.json)

Train và validation được băm trước khi so trùng; SHA-256 lần lượt là `ce57068f17656035e16940b5129ae5aef90b89ed4b187b615476a746c898e1b8` và `ae83709217103ef48b92c886412c23d18fbcc768bef44aa326aff894e5d7c1cd`. Payload test không được mở; không có dòng nào được nhập vào v0.2.5 và không train/chấm điểm trong vòng này. [Round 46 metadata](../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/candidate_screen_20261024_round46/SOURCE_SCREENING_ROUND46_METADATA.json)

## Ứng viên ưu tiên cho JB-only

### Lying to LLMs — corpus jailbreak và benign

Mendeley Data công bố corpus nghiên cứu “Lying to LLMs” theo CC BY 4.0, gồm file riêng cho deceptive jailbreak prompts và benign prompts. [[160]](#ref160)

Trong snapshot v1, file jailbreak có 1.061 dòng không rỗng, 972 chuỗi khác nhau sau chuẩn hóa, 89 dòng trùng; 80 chuỗi trùng chính xác với train v0.2.5 và không có chuỗi trùng validation. Sau loại trùng exact với train/validation, còn 892 chuỗi JB tiềm năng. File benign có 4.251 chuỗi khác nhau; 4 trùng train và 2 trùng validation, còn 4.245 chuỗi không trùng exact hai split. Đây là kết quả audit cục bộ, không phải support được nhận vào dataset. [Audit corpus](../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/lying_to_llms_mendeley_v1_20261024/CANDIDATE_AUDIT.json)

Nguồn này có thể tăng JB support ở một dataset version sau, nhưng metadata không cung cấp nguồn gốc từng prompt, rubric gán nhãn hay quy trình kiểm chứng; file cũng có một số dòng rất ngắn và 89 bản lặp trong tập jailbreak. Cần rà chất lượng dòng và lineage/near-duplicate trước khi chọn train hay đánh giá; chưa thể gọi đây là test độc lập theo source family. [[160]](#ref160) [Audit corpus](../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/lying_to_llms_mendeley_v1_20261024/CANDIDATE_AUDIT.json)

### JailbreakBench — cohort đánh giá chẩn đoán

Bản JailbreakBench ghim ở commit `886acc352a31533ffbcf4ef22c744658688086fc` có license MIT. File judge-comparison có 300 prompt duy nhất; README mô tả 200 attack prompts cùng 100 benign XS-Test controls. [[156]](#ref156)

Exact overlap audit tìm thấy 1 prompt trùng train và 0 trùng validation; sau loại trùng exact còn tối đa 199 attack prompts có thể xem xét làm cohort JB chẩn đoán ở một dataset version mới. Đây chưa phải kết luận tách biệt theo họ nguồn: cần rà nguồn của behavior/attack và near-duplicate trước khi đóng băng split. [JBB audit](../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/jbb_judge_comparison_20261024/CANDIDATE_AUDIT.json)

Hai file behavior riêng có 100 harmful goals và 100 benign goals; harmful goals gồm 55 `Original`, 18 `AdvBench`, 27 `TDC/HarmBench`. Đây là goal/request data, không tự động là PI, JB hay OTHER_ATTACK; không dùng để bổ sung lớp L3 nếu không có rubric gán nhãn phù hợp. [JBB audit](../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/jbb_judge_comparison_20261024/CANDIDATE_AUDIT.json)

## Ứng viên BOTH và các nguồn bị loại

### CORTYX

Snapshot CORTYX đã ghim trước đó có 6 dòng mang cả `jailbreak_attempt` và `prompt_injection`, không trùng exact với train/validation; cả sáu co-label nằm trong cùng một source group. Sáu dòng không đủ thay thế 48 case BOTH còn thiếu theo gate, và chưa chứng minh độ đa dạng theo nguồn. [[147]](#ref147) [CORTYX audit](../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/quanta_cortyx_full_combined_20261023/CANDIDATE_AUDIT_FULL_COMBINED.json)

Card, viewer và file snapshot công bố số dòng khác nhau, nên cần xác minh release contract trước khi dùng; round này giữ CORTYX ở trạng thái chưa nhận vào train. [[147]](#ref147)

### PromptShield

PromptShield v2 công bố 3.000 dòng, ba annotator và nhãn risk `benign/suspicious/malicious` cùng `attack_type`; schema này không có hai trục PI/JB độc lập hay co-label BOTH. [[159]](#ref159)

Audit CSV phát hiện 3.000 ID nhưng chỉ có 30 prompt text duy nhất; 2.970 dòng lặp lại prompt đã có. Vì vậy, dù dữ liệu khai báo CC BY 4.0 và có thông tin người gán nhãn, snapshot này bị quarantine do trùng lặp lớn và nhãn không khớp taxonomy L3. [[159]](#ref159) [PromptShield audit](../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/promptshield_mendeley_v2_20261024/CANDIDATE_AUDIT.json)

### JailGuard

JailGuard là lead về đa dạng phương thức: bài báo và trang dữ liệu mô tả 4.000 text attack queries cùng 6.000 benign queries, với các nhóm jailbreak và hijacking/injection. Tuy nhiên, repo ghim tại `419e1d3d08f4d02998a11a687f925518d2d5dd0c` có pickle payload nhưng không khai báo license ở repo; payload chưa được tải. [[157]](#ref157) [[158]](#ref158)

Chưa dùng JailGuard cho tới khi quyền dữ liệu được làm rõ; metadata công khai hiện chưa cho thấy co-label BOTH trực tiếp. [[157]](#ref157) [[158]](#ref158)

### Mindgard — metadata-only

Mindgard công bố các cặp prompt gốc/đã biến đổi, gồm injection và jailbreak, với `attack_name` mô tả kỹ thuật biến đổi; card nêu nguồn injection gốc là Safe-Guard Prompt Injection. File hiện yêu cầu chấp nhận điều kiện chia sẻ thông tin tài khoản Hugging Face và khai báo CC BY-NC-4.0; không tải payload, không chấp nhận điều kiện, và không xem đây là nguồn co-label BOTH. [[161]](#ref161)
## Kết luận và bước tiếp theo

Vòng 46 tìm được dữ liệu JB-only có thể dùng sau rà soát: Lying to LLMs có tối đa 892 dòng mới sau exact dedup; JBB có tối đa 199 attack prompts để cân nhắc làm cohort đánh giá chẩn đoán. Không nguồn nào đủ điều kiện tự động nhập vào v0.2.5; nguồn BOTH mới chỉ có 6 dòng CORTYX từ một source group. [Round 46 metadata](../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/candidate_screen_20261024_round46/SOURCE_SCREENING_ROUND46_METADATA.json)

Khuyến nghị giữ v0.2.5 là package data-only chưa train. Trước dataset version kế tiếp, ưu tiên tạo thêm BOTH được gán hai trục rõ ràng từ nhiều source độc lập; đồng thời giữ JBB như một cohort JB chẩn đoán riêng nếu qua rà soát lineage/near-duplicate. Giữ cố định rubric nhãn và split contract; tiếp tục ghi rõ nhãn là proxy theo taxonomy nguồn, chưa phải gold do người gán cho taxonomy năm lớp. [[156]](#ref156) [[160]](#ref160)

Artifacts: [metadata sàng lọc vòng 46](../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/candidate_screen_20261024_round46/SOURCE_SCREENING_ROUND46_METADATA.json) · [audit Lying to LLMs](../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/lying_to_llms_mendeley_v1_20261024/CANDIDATE_AUDIT.json) · [audit JBB](../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/jbb_judge_comparison_20261024/CANDIDATE_AUDIT.json) · [task checklist](../../../.agents/artifacts/TASK_L3_SUBTYPE_V025_SOURCE_DISCOVERY_ROUND46_20261024.md).



