# PI-Guard L3 subtype v0.2.5 — báo cáo tìm nguồn dữ liệu, vòng 45

Ngày: 2026-10-24

## Scope Boundary Declaration

**IN-SCOPE:** rà các nguồn công khai có tiềm năng bổ sung dữ liệu PI/JB, xác minh schema, split, provenance, license và exact overlap với train/validation v0.2.5; lưu audit để quyết định cho một dataset version mới.

**OUT-OF-SCOPE:** sửa package hoặc support gate v0.2.5; thêm bất kỳ dòng nào vào train/validation/test; mở payload test; chấm test; train/tune model; chấp nhận điều khoản gated; truy cập nguồn bị loại trừ.

## Trạng thái v0.2.5

Manifest hiện ghi train 54.244 dòng, BOTH số học 52/100 và BOTH có căn cứ hai trục 24; validation có 13.530 dòng và 30 BOTH. Metadata test ghi 303 dòng, gồm 35 BOTH nhưng không có JB hoặc OTHER_ATTACK; payload test không được mở trong vòng này. Gate vẫn `fit_allowed=false`, `test_scoring_allowed=false`; không tạo model hay metrics mới. [Manifest](../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/versions/v0.2.5/DATASET_MANIFEST.json) [Support gate](../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/versions/v0.2.5/SUPPORT_GATE.json)

## Ứng viên đã tải và audit: cyberec multi-label

Đã ghim revision `a3d05895270cac0e553206c95463061c9bfb899f` của `cyberec/llm-prompt-injection-attacks`; card mô tả tập tiếng Anh 55.000 dòng với hai split, các nhãn `BENIGN`, `JAILBREAK`, `INSTRUCTION_OVERRIDE`, `ROLE_HIJACK`, `DATA_EXFILTRATION`, cùng cách gán heuristic theo rule. File chứa hai trường `text` và `labels`, không có trường source theo từng dòng. [[148]](#ref148)

Đếm Parquet trực tiếp cho thấy train có 49.500 dòng và validation 5.500 dòng. Nếu tạm ánh xạ `INSTRUCTION_OVERRIDE`, `ROLE_HIJACK`, `DATA_EXFILTRATION` thành PI mechanism rồi ghép với `JAILBREAK`, có 25.792 dòng train và 2.793 dòng validation đồng xuất hiện hai tên nhãn; đây là thống kê theo cách ánh xạ giả định, không phải support BOTH được chấp nhận. Mọi tập nhãn tấn công quan sát được đều ghép `JAILBREAK` với một hoặc nhiều mechanism label, nên schema chưa chứng minh hai trục PI/JB được gán độc lập. [[148]](#ref148) [Audit candidate](../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/cyberec_prompt_injection_mechanisms_20261024/CANDIDATE_AUDIT.json)

Card nêu hai upstream là Qualifire Prompt Injections Benchmark và `jayavibhav/prompt-injection-safety`, nhưng nói các tập gốc không được phân phối lại. Metadata hiện hành của Qualifire ghi CC-BY-NC-4.0 và trạng thái gated; card của Jayavibhav không khai license. Vì merged file không lưu provenance theo dòng, declaration Apache-2.0 trên card tổng hợp chưa giải quyết được rights của từng prompt. [[148]](#ref148) [[149]](#ref149) [[150]](#ref150)

Exact overlap audit tìm thấy 796 dòng của candidate trùng normalized text với train/validation v0.2.5; riêng candidate cũng có 3 text trùng giữa train và validation, và train có 19 dòng trùng normalized text nội bộ. Không có test payload nào được kiểm tra overlap. Do thiếu row-level source, quyền upstream chưa rõ và taxonomy không tách hai trục, quyết định là quarantine; không cộng 28.585 đồng xuất hiện nhãn giả định vào BOTH support. [Audit candidate](../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/cyberec_prompt_injection_mechanisms_20261024/CANDIDATE_AUDIT.json)

## Các lead hữu ích nhưng chưa giải quyết BOTH

Quickium Prompt Security v0 công bố 71.117 dòng trong split `train` có source và license theo từng dòng, cùng 293.907 dòng `train_nc`; schema cho phép nhãn domain ghép nhưng card nói chưa có compound row nào. Card báo split `train` chỉ có 4 JB unsafe, còn `train_nc` có 146.359 JB unsafe và 2.503 PI unsafe; dữ liệu JB của `train_nc` tập trung chủ yếu ở WildJailbreak tổng hợp và mang CC-BY-NC. Đây là lead cho JB/PI đơn nhãn nếu license và overlap được rà tiếp, không phải nguồn BOTH hay benchmark test. [[151]](#ref151)

PromptSentinel công bố 156.802 prompts, ba lớp loại trừ nhau (`benign`, `jailbreak`, `injection`) và metadata nguồn/license theo dòng, nhưng trang yêu cầu đồng ý chia sẻ thông tin trước khi truy cập file. Không tải payload hoặc chấp nhận điều kiện; ngay cả khi được tiếp cận, schema ba lớp vẫn không tạo support BOTH trực tiếp. [[152]](#ref152)

Necent công bố schema `prompt_harmful`/`prompt_adversarial` và hơn 30 nguồn, nhưng dataset đang gated; trường adversarial gộp jailbreak, PI và obfuscation nên không phân lớp năm nhãn L3. Không tải payload hoặc chấp nhận điều kiện. [[153]](#ref153)

Turkish Conversation Prompt-Injection Dataset công bố 750 ví dụ tổng hợp có CC-BY-4.0, gồm split train/validation/test và một nhãn prompt-injection/security attack; `roleplay_jailbreak` là một attack family trong taxonomy, không phải nhãn JB độc lập. Có thể cân nhắc sau cho nghiên cứu tiếng Thổ Nhĩ Kỳ và hard-negative, nhưng không bổ sung BOTH cho taxonomy hiện tại. [[154]](#ref154)

## Kết luận và bước tiếp theo

Vòng 45 không tìm được nguồn mới đủ điều kiện để bổ sung direct BOTH: số co-occurrence lớn nhất thuộc bộ heuristic có rights/provenance chưa rõ và không có hai trục nhãn độc lập. Giữ nguyên gate và không train v0.2.5. Ưu tiên tìm tập có nhãn PI và JB được đánh giá riêng trên cùng prompt, rubric công khai, provenance/license theo dòng, và nhiều source family độc lập; AEGINEL vẫn là lead về quy mô nhưng cần payload cùng quyền dữ liệu riêng trước khi xét tiếp. [[143]](#ref143) [[144]](#ref144) [[155]](#ref155)

Artifacts vòng 45: [metadata sàng lọc](../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/candidate_screen_20261024_round45/SOURCE_SCREENING_ROUND45_METADATA.json) · [candidate audit](../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/cyberec_prompt_injection_mechanisms_20261024/CANDIDATE_AUDIT.json) · [task checklist](../../../.agents/artifacts/TASK_L3_SUBTYPE_V025_SOURCE_DISCOVERY_ROUND45_20261024.md).
