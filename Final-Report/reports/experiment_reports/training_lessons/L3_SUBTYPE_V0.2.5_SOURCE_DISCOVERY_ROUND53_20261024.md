# L3 subtype v0.2.5 — nghiên cứu bổ sung nguồn dữ liệu, round 53

**Ngày:** 2026-10-24  
**Trạng thái:** đã audit hai train snapshot mới; chưa nhận dòng nào vào package, chưa tạo dataset version mới, chưa train.

## Scope boundary declaration

- **IN-SCOPE:** rà metadata nguồn công khai và train split tại revision cố định; so khớp ứng viên chỉ với train/validation v0.2.5; kiểm tra nhãn, seed/group, trùng lặp, lineage và license; cập nhật inventory, reference log và báo cáo.
- **OUT-OF-SCOPE:** đọc test payload v0.2.5 hoặc test upstream; ghi dòng vào package v0.2.5; chấm test, chọn threshold/checkpoint, huấn luyện model; truy cập nguồn bị loại trừ.

## Kết quả chính

### 9mark9 — 30 co-tag BOTH ứng viên, nhưng thiếu bằng chứng đa dạng

Đã tải riêng train parquet tại revision `cac5cb5801964011295c1926b927506e81f2802d`; SHA-256 `AA1913F1CF4A7E6E0E1F3A08FF3094B9D3353D7985C79C2B261408A056D507C0`. Publisher khai báo MIT. Điều kiện `category=JAILBREAK AND owasp=LLM01: Prompt Injection` khớp 30/150 dòng, tương ứng 26 văn bản chuẩn hóa duy nhất. Exact overlap với train và validation v0.2.5: 0. [[189]](#ref189)

Có 20 dòng do mutation engine tạo, truy ngược được tới hai `seed_id`; 10 dòng thuộc attack library không có seed ID. Dataset chỉ có một train split. Co-tag là BOTH proxy theo taxonomy nguồn, chưa phải nhãn gold PI-Guard. Hai seed cùng 10 dòng không có group key chưa chứng minh đủ kịch bản độc lập. Nếu chỉ nhận 30 dòng, raw support tăng 52→82, vẫn dưới mục tiêu 100. Candidate được giữ ở trạng thái HOLD.

### NEPI — nhiều dòng PI ứng viên, không có co-tag BOTH

Đã stage train parquet tại revision `391139f74fc50d09b5593eb387505ab5844b0bc9`; SHA-256 `82E2E24FF270317E0FD0097381470D9CB73548F843C96AB37D12808922B4DCBD`. Publisher khai báo MIT. Card mô tả một split train tổng hợp từ template và tách NEPI thành họ riêng với traditional jailbreak. [[190]](#ref190)

Audit có 4.000 dòng nhưng 514 văn bản chuẩn hóa duy nhất. NEPI có 2.700 dòng, gồm 2.500 malicious, nhưng chỉ 285 văn bản duy nhất. Traditional jailbreak có 300 dòng nhưng 8 văn bản duy nhất. Không có dòng nào đồng thời là NEPI và `policy_bypass`; 300 dòng `policy_bypass` nằm dưới traditional jailbreak. Exact overlap với train/validation v0.2.5 là 0. Nguồn này không bổ sung BOTH; có thể xem xét riêng cho train lớp đơn sau khi rà chất lượng, lineage và template groups.

## Các nguồn gated chỉ rà metadata

- **Necent jailbreak/prompt-injection collection:** yêu cầu quyền truy cập; schema dùng `prompt_type` đơn và tập hợp hơn 30 nguồn với license upstream khác nhau. Chưa tải payload hoặc chấp thuận điều khoản; metadata công khai chưa chứng minh co-label theo dòng. [[191]](#ref191)
- **Fujitsu ART-SafeBench v2:** thẻ nêu CC-BY-4.0 cùng `LICENSE-USE` riêng và yêu cầu thỏa thuận truy cập; benchmark trộn nhiều nguồn agent/RAG. Chưa tải payload hay chấp thuận điều khoản; metadata chưa xác nhận một prompt có đồng thời nhãn PI và JB. [[192]](#ref192)

## Gate, dự phóng và quyết định

Gate hiện tại báo train BOTH 52/100 (audit direct-evidence: 24), `fit_allowed=false`. Validation có 30 BOTH. Test giữ 303 dòng: BOTH 35, PI 165, benign 103, JB 0, OTHER_ATTACK 0; `test_scoring_allowed=false`. Không đọc test payload trong round này.

Nếu 35 dòng candidate từ 3nesdeniz Boundary Pairs ở round trước và 30 dòng 9mark9 cùng được nhận, phép cộng thô là 52+35+30=117 BOTH. Đây chỉ là dự phóng; hai candidate chưa được duyệt, và cần kiểm tra độc lập nhóm, semantics và điều kiện sử dụng. Audit trước ghi nhận 35 scenario ID cho candidate 3nesdeniz. [[165]](#ref165) Ngay cả khi train gate sau này đạt, test hiện vẫn thiếu JB-only và OTHER_ATTACK để đánh giá đủ năm lớp.

**Quyết định:** giữ nguyên package v0.2.5; chưa tạo v0.2.6, chưa train. Tiếp tục tìm nguồn độc lập có co-label PI/JB minh bạch theo dòng, nhóm kịch bản truy vết được và quyền sử dụng rõ ràng; đồng thời tìm cohort test source-held-out có đủ BOTH, PI, JB, OTHER_ATTACK và benign.

## Artifacts

- [Candidate inventory round 53](../../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/candidate_screen_20261024_round53/candidate_screen_20261024_round53.json)
- [9mark9 audit](../../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/candidate_screen_20261024_round53/9mark9_CANDIDATE_AUDIT_ROUND53.json)
- [NEPI audit](../../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/candidate_screen_20261024_round53/nepi_CANDIDATE_AUDIT_ROUND53.json)
- [9mark9 train snapshot](../../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/9mark9_llm_redteam_owasp_prompts_20261024_round53/train.parquet)
- [NEPI train snapshot](../../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/vaibhav_goat_nepi_prompts_20261024_round53/train.parquet)
- [Support gate v0.2.5](../../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/versions/v0.2.5/SUPPORT_GATE.json)

## References used

[[165]](#ref165), [[189]](#ref189), [[190]](#ref190), [[191]](#ref191), [[192]](#ref192).
