# PI-Guard L3 subtype v0.2.5 — báo cáo tìm nguồn dữ liệu, vòng 48

Ngày: 2026-10-24

## Scope Boundary Declaration

**IN-SCOPE:** tìm và sàng lọc thêm nguồn BOTH/JB; ghim revision; lưu train/validation của các nguồn được phép khảo sát; xác minh schema, license metadata, support và exact/prefix overlap với v0.2.5; ghi lại lead cho lần dataset version mới.

**OUT-OF-SCOPE:** sửa package v0.2.5; mở payload test v0.2.5 hoặc payload test của nguồn mới; nhập dữ liệu, train/chấm model, chọn threshold hoặc tạo metrics; truy cập nguồn bị loại trừ, dữ liệu gated hoặc dữ liệu trả phí. Các con số dự phóng trong báo cáo không phải support đã được chấp nhận.

## Trạng thái baseline và kiểm soát

**Kết quả thực nghiệm từ artifact hiện có:** v0.2.5 có 52 case BOTH và 52 group BOTH trong train, dưới gate 100; `fit_allowed=false`. SHA-256 train/validation vẫn khớp manifest (`ce57068f17656035e16940b5129ae5aef90b89ed4b187b615476a746c898e1b8`, `ae83709217103ef48b92c886412c23d18fbcc768bef44aa326aff894e5d7c1cd`). Metadata test có 303 dòng, gồm 35 BOTH nhưng JB=0 và OTHER_ATTACK=0; payload test không được mở. Không có dòng nào được nhập và không có lần train, test scoring hay metrics mới. [Manifest và support gate v0.2.5](../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/versions/v0.2.5/DATASET_MANIFEST.json) · [audit vòng 48](../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/candidate_screen_20261024_round48/candidate_screen_20261024_round48.json)

**Kiểm soát overlap:** script chỉ đọc v0.2.5 train/validation. Không đọc test. Các nguồn có test split chỉ tải train/validation khi cần audit. Định nghĩa BOTH dưới đây là proxy theo taxonomy nguồn, không phải nhãn gold do người gán.

## Ứng viên mới có khả năng bổ sung BOTH

### 3nesdeniz English Prompt Injection 3K

**Dữ kiện từ card nguồn:** snapshot tại revision `87f017347aff7887b1de0d9457c9ec01bf7ba8b5` khai CC BY 4.0; card mô tả 2.453 train, 286 validation, 314 test, và dữ liệu tổng hợp mở rộng xác định từ các template do người viết. [[167]](#ref167)

**Kết quả audit cục bộ:** chỉ lấy README, train và validation; hash hai Parquet trùng publisher LFS hash. Theo mapping `class=injection AND attack_family=jailbreak_persona AND label=1`, train có 177 text unique và validation 7. Exact overlap với v0.2.5 train/validation bằng 0; candidate train có 3 prefix-35 overlap với v0.2.5 train và 2 với validation. Nguồn không có ID scenario/template theo từng dòng nên không xác nhận được số group độc lập. Số người viết/publisher family trùng với bộ boundary-pairs bên dưới. [[167]](#ref167) [Audit cục bộ](../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/3nesdeniz_english_prompt_injection_3k_20261024_round48/CANDIDATE_AUDIT.json)

**Đánh giá:** nếu tạm cộng 177 train rows vào 52 BOTH hiện tại, được 229 case theo phép đếm, nhưng đây chưa phải 229 group độc lập và chưa tính qua gate. Cần xem 5 prefix hit, xác minh group/source lineage, rồi mới cân nhắc đưa vào dataset mới. Không dùng test cùng publisher family làm đánh giá source-held-out nếu train từ nguồn này.

### 3nesdeniz Agentic Prompt-Injection Boundary Pairs

**Dữ kiện từ card nguồn:** revision `a5682e7573e1c7bc4b12e64d49c0dcd90ca776cf`, CC BY 4.0, 840 train, 120 validation, 240 test; nguồn mô tả cặp benign/attack theo scenario. Card/review log nói 180/600 cặp được rà soát bởi một reviewer, nhưng không có cờ review ở từng dòng. [[165]](#ref165)

**Kết quả audit cục bộ:** 35 train và 5 validation rows thỏa mapping `category=prompt_injection AND attack_family=roleplay_jailbreak AND label=1`; mỗi dòng train có scenario ID khác nhau và không trùng scenario giữa train/validation. Exact overlap với v0.2.5 là 0. Test payload không được tải/mở. Cộng riêng nhóm train này vào support v0.2.5 chỉ được 87 case BOTH, dưới gate. [Audit cục bộ](../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/3nesdeniz_agentic_prompt_injection_boundary_pairs_20261024_round48/CANDIDATE_AUDIT.json)

**Đánh giá:** đây là ứng viên train có taxonomy hai trục rõ nhất ở vòng này, nhưng quy mô thấp; cùng tác giả/source family với English Prompt Injection 3K nên hai bộ không tạo hai publisher family độc lập.

### Cyberec Prompt Injection Mechanisms — candidate đang cách ly

**Dữ kiện từ card nguồn:** `cyberec/llm-prompt-injection-attacks` là bản sao của `Smooth-3/llm-prompt-injection-attacks`, revision `a3d05895270cac0e553206c95463061c9bfb899f`; Hub metadata khai Apache 2.0. Card mô tả 49.500 train, 5.500 validation, nhãn cơ chế nhiều nhãn và tái gán nhãn bằng luật xác định; hai nguồn đầu vào được nêu là Qualifire và jayavibhav. Card cảnh báo nhãn heuristic có thể nhiễu và ghi dữ liệu gốc không được phân phối lại. [[172]](#ref172)

**Kết quả audit cục bộ:** nhãn cùng dòng `JAILBREAK` + `INSTRUCTION_OVERRIDE` tạo proxy BOTH gồm 23.758 text unique trong train và 2.554 trong validation. Tuy nhiên schema thiếu source/template/group ID. Candidate train trùng exact 584 dòng với v0.2.5 train và 136 với validation; candidate validation trùng 62 với train và 13 với validation. Prefix-35 overlap giữa candidate train và v0.2.5 là 951 train / 416 validation. Đây là cờ rà soát near-duplicate, không khẳng định toàn bộ là trùng ngữ nghĩa. [Audit cục bộ](../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/cyberec_llm_prompt_injection_attacks_20261024_round48/CANDIDATE_AUDIT.json)

**Đánh giá:** phép cộng số học cho ra 23.810 case khi cộng candidate train vào 52 hiện tại, nhưng con số này không thể dùng làm BOTH support hợp lệ. Có exact overlap xuyên split, thiếu group/provenance từng dòng, nhãn heuristic và chưa xác minh quyền của các nguồn thành phần. Giữ snapshot cách ly; không nhập vào train và không dùng làm test source-held-out. Cần tái dựng lineage/nhóm và lọc overlap trước khi xem xét lại.

## Các nguồn được giữ ngoài train BOTH

- `pr1m8/prompt-injections`: snapshot 82 dòng; có 7 dòng `category=Jailbreak`, nhưng không có hai nhãn PI/JB độc lập trên cùng dòng; nguồn của 7 dòng này được ghi là Garak. README công bố MIT nhưng quyền từng payload upstream chưa giải quyết. Giữ ngoài support BOTH. [[166]](#ref166)
- `fahadhafeezofficial/cissp-llmbench`: 18K theo card, có `category/subcategory` và safe/unsafe variant, nhưng không có nhãn attack theo từng dòng đủ để map BOTH; giữ metadata-only. [[168]](#ref168)
- `RomanKudriavskii/jeff-guard-multilang-dataset`: một lớp đơn trên mỗi dòng và license metadata là `other`; không tạo co-label BOTH và quyền chưa rõ. [[169]](#ref169)
- `nuhmanpk/prompt-sentinel`: card ghi 156.802 mẫu, ba lớp đơn benign/jailbreak/injection và quyền truy cập gated; hữu ích để khảo sát taxonomy nhưng không thể coi một dòng là BOTH từ schema lớp đơn. Không mở payload hoặc nhận điều khoản. [[170]](#ref170)
- `rogue-security/prompt-injections-benchmark`: card mô tả 5.000 mẫu test-only với `jailbreak`/`benign`, license CC BY-NC 4.0. Có thể là cohort JB/benign đánh giá riêng trong tương lai nếu xác minh source-disjoint với mọi dữ liệu fit; không tải payload trong vòng này và không bổ sung BOTH. [[171]](#ref171)
- Turkish conversation PI của cùng publisher 3nesdeniz được giữ cho scope đa ngôn ngữ riêng. AEGINEL vẫn thiếu payload có thể xác minh; CORTYX có sáu dòng co-label từ một source group nhưng chưa có split/điều kiện license hoàn chỉnh. [[154]](#ref154) [[143]](#ref143) [[144]](#ref144) [[147]](#ref147)

## Kết luận và bước tiếp theo

Vòng 48 tìm được hai candidate BOTH có thể xem xét cho train mới, nhưng chưa có nguồn nào được nhập: boundary-pairs chỉ thêm 35 train cases; English 3K thêm 177 theo taxonomy nhưng thiếu group IDs và cùng publisher family. Cộng số học cả hai với v0.2.5 cho 264 proxy cases, nhưng không chứng minh đủ 264 group độc lập hoặc source diversity. Cyberec có support số học cao nhưng vướng overlap xuyên split, provenance thiếu và nhãn heuristic. Vì vậy v0.2.5 vẫn ở 52/100, gate train vẫn đóng; hiện không có metrics train/valid/test mới.

Tiếp theo nên ưu tiên: (1) rà 5 prefix hits và dựng group/template IDs cho English 3K; (2) xin hoặc tái dựng lineage từng dòng của Cyberec, rà các exact/prefix matches và rights của constituent sources; (3) tìm BOTH từ publisher/source family khác hoặc tự gán nhãn hai trục có reviewer độc lập; (4) xây cohort JB-only và OTHER_ATTACK source-held-out, tách riêng khỏi train. Chỉ tạo dataset version mới sau khi source lineage, split isolation và hỗ trợ độc lập đạt yêu cầu; giữ nguyên package v0.2.5 và test payload hiện tại.

Artifacts: [audit tổng hợp vòng 48](../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/candidate_screen_20261024_round48/candidate_screen_20261024_round48.json) · [audit Cyberec](../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/cyberec_llm_prompt_injection_attacks_20261024_round48/CANDIDATE_AUDIT.json) · [audit English 3K](../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/3nesdeniz_english_prompt_injection_3k_20261024_round48/CANDIDATE_AUDIT.json) · [task checklist](../../../.agents/artifacts/TASK_L3_SUBTYPE_V025_SOURCE_DISCOVERY_ROUND48_20261024.md)
