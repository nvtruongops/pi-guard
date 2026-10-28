# L3 subtype v0.2.5 — nghiên cứu bổ sung nguồn dữ liệu, round 54

**Ngày:** 2026-10-24  
**Trạng thái:** đã audit một train candidate ghim revision và sàng lọc thêm nguồn đánh giá; chưa nhận dòng nào vào package, chưa tạo dataset version mới, chưa train.

## Scope boundary declaration

- **IN-SCOPE:** rà metadata và train split công khai; so khớp candidate chỉ với train/validation v0.2.5; kiểm tra taxonomy, overlap, lineage và quyền sử dụng; cập nhật inventory, reference log và báo cáo.
- **OUT-OF-SCOPE:** đọc test payload v0.2.5; dùng payload test upstream để train hoặc chấm; ghi dòng vào package v0.2.5; chọn threshold/checkpoint; huấn luyện model; truy cập nguồn bị loại trừ.

## Quy tắc nhãn BOTH

Xia et al. (Findings of ACL 2025) phân biệt prompt leakage và jailbreak là hai mục tiêu khác nhau; prompt injection là phương thức có thể phục vụ một trong các mục tiêu đó. Vì vậy, một tên kỹ thuật như `jailbreak_template`, hay một cờ `prompt_adversarial`, tự nó chưa đủ để gán BOTH. Cần bằng chứng cùng dòng cho phương thức PI và mục tiêu JB; prompt leakage hoặc chỉ có nội dung độc hại không tự động thành JB. [[193]](#ref193)

## Kết quả audit train candidate: Mirza Akhi

Đã ghim repository tại commit `011a9ae25b31feb48d23f837fdcbc3a6a4ee3b4e` và chỉ lưu split train. CSV upstream gộp train/test trong cùng một file; script đếm split test rồi bỏ qua, chỉ ghi 4.212 dòng train ra candidate. SHA-256 snapshot upstream: `eb748eb8104f0a736934bf4f3c96335801010b09e17467fd4aadc1c1ae7bbced`. Repository công bố CC BY 4.0. [[195]](#ref195)

Train candidate có 2.210 benign và 2.002 malicious; 36 dòng thuộc category `persona_jailbreak`. Không có trường `target_behavior` hoặc hai nhãn PI/JB độc lập. So khớp văn bản chuẩn hóa cho thấy 4.195/4.212 dòng trùng train v0.2.5 và 16 dòng trùng validation; chỉ còn 1 dòng mới. Do vậy, nguồn này không bổ sung lượng dữ liệu độc lập đáng kể và không đóng góp dòng BOTH nào. Đây là exact overlap trên train/validation theo [audit JSON](../../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/mirzaakhi_prompt_injection_detection_dataset_20261024_round54/CANDIDATE_AUDIT_ROUND54.json); test v0.2.5 không được mở. [[195]](#ref195)

## Bordair: template expansion không giải quyết thiếu co-label

Snapshot round 54 có 8.100 văn bản từ 50 nhóm `seed_payload`, mỗi nhóm được mở rộng thành 162 dòng. Audit thấy 159 giá trị `template_name` khác nhau; chênh lệch với con số 162 templates trên card vẫn chưa được giải thích. Số biến thể văn bản không phải số mục tiêu độc lập. [[173]](#ref173) Số liệu này nằm trong [audit JSON](../../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/bordair_bordair_multimodal_20261024_round54/CANDIDATE_AUDIT_ROUND54.json).

Rà sơ bộ trường seed cho thấy 18 nhóm có nội dung có thể là mục tiêu vô hiệu hóa safety/tuân thủ không giới hạn, 31 nhóm chủ yếu yêu cầu lộ system prompt, cấu hình, credential hoặc secret, và 1 nhóm còn mơ hồ. Đây là triage của trợ lý từ seed field, không phải annotation gold hay duyệt đầy đủ từng dòng. Nguồn không có trường mục tiêu hoặc co-label PI/JB theo dòng; vì vậy số BOTH được nhận vẫn bằng 0. Quyền sử dụng cũng cần xem lại vì Hub license metadata trống, card MIT là một khai báo của publisher, và lineage gồm nhiều nguồn ngoài. [[173]](#ref173) Chi tiết triage ở [summary JSON](../../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/bordair_bordair_multimodal_20261024_round54/BORDIAR_SEED_GOAL_TRIAGE_ROUND54.json).

## Ứng viên cho test source-held-out trong version sau

Repository của Muhammad Saeed Anwar báo cáo benchmark 250 mẫu tấn công, gồm 60 direct injection, 55 indirect injection, 70 jailbreak, 40 multi-turn và 25 encoding/obfuscation. Schema có `primary_category`, `target_behavior` và `prompt_text`; repository công bố MIT và nói khoảng 15–20% mẫu được tạo theo template. Không có train/validation/test split công bố, nên giữ toàn bộ release ở vai trò benchmark đánh giá, không lấy làm train. `target_behavior` có thể hỗ trợ rà phương thức và mục tiêu theo từng dòng, nhưng chưa có audit payload, overlap hay số BOTH. Tập này cũng không có benign control, nên riêng nó không thể cung cấp FPR hoặc macro-F1 đủ năm lớp. Các số liệu và điều khoản trên là tuyên bố trong repository, chưa được xác nhận độc lập qua quy trình phản biện khác. [[194]](#ref194)

## Các lead metadata-only

- **Necent:** card hiện có `prompt_harmful`, `prompt_adversarial`, `prompt_type` và `attack_technique`. Đây là lead gần với hai trục hơn, nhưng `prompt_adversarial` gộp jailbreak, PI và obfuscation; không thể suy ra số BOTH từ schema. Dataset gated và mỗi nguồn con giữ license riêng; không truy cập payload hay chấp thuận điều khoản. [[191]](#ref191)
- **Cogensec Jailbreak Corpus v0.3:** card nêu 59.508 dòng và hai trường kỹ thuật/tác hại, nhưng khoảng 51% technique là `other`, khoảng 92% harm là `unknown`, nhãn hiện tại rule-based và dữ liệu gated. Chưa có số dòng co-label đủ tin cậy. [[163]](#ref163)
- **PromptSentinel:** card nêu 156.802 prompt duy nhất trong ba lớp mutually exclusive `benign`, `jailbreak`, `injection`; không có lớp BOTH và payload gated. Đây là dữ liệu gộp nhiều nguồn, không chứng minh thêm nguồn độc lập. [[186]](#ref186)

## Trạng thái gate và quyết định

Package v0.2.5 không đổi: train BOTH là 52/100, validation BOTH là 30/30; test giữ 303 dòng với BOTH 35, PI 165, `NO_L3_ATTACK` 103, JB 0 và OTHER_ATTACK 0. `fit_allowed=false`, `test_scoring_allowed=false` theo [SUPPORT_GATE.json](../../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/versions/v0.2.5/SUPPORT_GATE.json). Không đọc test payload v0.2.5 và không tạo metrics mới trong vòng này.

**Quyết định:** không nhận Mirza hoặc Bordair vào support BOTH; không tạo v0.2.6 và không train. Tiếp tục tìm nguồn train không gated, khác lineage và có nhãn cùng dòng cho PI method + JB goal. Rà Anwar như ứng viên test-only trong một dataset version sau, sau khi đối chiếu overlap với train/validation và duyệt `target_behavior`; giữ nguồn benchmark nguyên vẹn để đánh giá.

## Artifacts

- [Candidate inventory round 54](../../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/candidate_screen_20261024_round54/candidate_screen_20261024_round54.json)
- [Mirza train candidate audit](../../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/mirzaakhi_prompt_injection_detection_dataset_20261024_round54/CANDIDATE_AUDIT_ROUND54.json)
- [Mirza train candidate JSONL](../../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/mirzaakhi_prompt_injection_detection_dataset_20261024_round54/TRAIN_CANDIDATE.jsonl)
- [Bordair source audit](../../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/bordair_bordair_multimodal_20261024_round54/CANDIDATE_AUDIT_ROUND54.json)
- [Bordair seed triage summary](../../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/bordair_bordair_multimodal_20261024_round54/BORDIAR_SEED_GOAL_TRIAGE_ROUND54.json)
- [Support gate v0.2.5](../../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/versions/v0.2.5/SUPPORT_GATE.json)

## References used

[[163]](#ref163), [[173]](#ref173), [[186]](#ref186), [[191]](#ref191), [[193]](#ref193), [[194]](#ref194), [[195]](#ref195).
