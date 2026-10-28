# PI-Guard L3 subtype v0.2.5 — báo cáo tìm nguồn dữ liệu, vòng 47

Ngày: 2026-10-24

## Scope Boundary Declaration

**IN-SCOPE:** tìm nguồn công khai có thể bổ sung JB/BOTH; ghim phiên bản, kiểm tra schema, quyền sử dụng, support và exact overlap với train/validation v0.2.5; lưu metadata để quyết định cho dataset version sau.

**OUT-OF-SCOPE:** sửa package v0.2.5; mở payload test; train/chấm model; mua dataset trả phí; chấp nhận điều khoản gated; dùng dữ liệu từ nguồn bị loại trừ. Test v0.2.5 vẫn là evaluation-only và không được mở trong vòng này.

## Trạng thái v0.2.5

Train hiện có 54.244 dòng, 52 case BOTH theo số đếm package và 24 dòng có bằng chứng hai trục trực tiếp theo sổ sàng lọc vòng 46; mục tiêu fit là 100 BOTH. Validation có 13.530 dòng, BOTH=30. Metadata test có 303 dòng, nhưng JB=0 và OTHER_ATTACK=0. Gate vẫn `fit_allowed=false` và `test_scoring_allowed=false`; payload test không được mở. [Support gate](../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/versions/v0.2.5/SUPPORT_GATE.json) [Metadata vòng 46](../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/candidate_screen_20261024_round46/SOURCE_SCREENING_ROUND46_METADATA.json)

Train và validation được băm trước khi so exact overlap; SHA-256 giữ nguyên lần lượt `ce57068f17656035e16940b5129ae5aef90b89ed4b187b615476a746c898e1b8` và `ae83709217103ef48b92c886412c23d18fbcc768bef44aa326aff894e5d7c1cd`. Không có dòng nào được nhập vào v0.2.5, không train/chấm model và không tạo metrics mới.

## Ứng viên JB: Quickium Prompt Security v0

Snapshot `train_nc.parquet` tại revision `8d67314bd5c08497ed1f20a62009bec58e7c5eb0` có 293.907 dòng: 146.359 JB unsafe, 2.503 PI unsafe và 145.045 SAFE. Audit thấy 0 dòng domain ghép `JB+PI`; card cũng nói v0 không có compound rows. Split này mang điều kiện CC BY-NC, chỉ dùng cho nghiên cứu phi thương mại; WildJailbreak chiếm phần lớn JB và là dữ liệu synthetic, WildGuardMix cũng chủ yếu synthetic. Dataset không có eval split và chỉ dedup exact text. [[151]](#ref151)

Sau exact dedup với package hiện tại, có 136.922 JB unsafe text duy nhất chưa thấy trong train/validation. Tuy nhiên, exact overlap đã có 15.839 dòng train và 4.073 validation; provenance package cho thấy 18.408 overlap đã mang source family Quickium, 1.503 mang `JailbreakDB`, và 1 mang `mirzaakhi`. Vì vậy đây là pool JB-only có thể cân nhắc cho train tương lai, nhưng không bổ sung source-family diversity, không tạo BOTH và không thể làm cohort test độc lập. [Audit Quickium](../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/quickium_prompt_security_v0_20261024/CANDIDATE_AUDIT.json)

## Ứng viên JB: jackhhao jailbreak classification

Tại revision `2f2ceeb39658696fd3f462403562b6eea5306287`, file full CSV cục bộ có 1.998 dòng, 1.971 text unique sau chuẩn hóa và 648 JB unique trước exact overlap. Card ghi jailbreak rows có nguồn từ `verazuo/jailbreak_llms`; benign rows đến từ OpenOrca và GPTeacher. [[162]](#ref162)

Trong 1.971 text unique, 197 JB trùng exact với train v0.2.5 và không có overlap validation; các exact overlap hiện được gắn `WUSTL-CSPL/LLMJailbreak` trong package. Còn 451 JB unique sau exact dedup train/validation, nhưng source-family/near-duplicate review chưa xong nên không dùng làm test độc lập. Hub card hiển thị 1.306 dòng trong khi file full CSV tải từ revision ghim có 1.998; cần làm rõ file/split nào là release chính thức trước khi tích hợp. [Audit jackhhao](../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/jackhhao_jailbreak_classification_20261024/CANDIDATE_AUDIT.json)

## Mẫu Manteclaw và nguồn cần quyền truy cập

Mẫu Manteclaw công khai gồm 100 dòng, tất cả đánh dấu synthetic; có 13 dòng cùng lúc mang giá trị ở `injection_technique` và `jailbreak_pattern`. Cả 13 text unique này đã trùng exact với train/validation v0.2.5. Các trường là kỹ thuật/pattern, chưa phải hai nhãn PI và JB độc lập, nên không tính là BOTH. README công bố bản 2.000 dòng trả phí; file `LICENSE` ghi MIT trong khi README ghi CC-BY-SA-4.0, vì vậy snapshot được quarantine chờ xác minh quyền. [[164]](#ref164) [Audit mẫu](../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/manteclaw_llm_safety_20261024/CANDIDATE_AUDIT.json)

Cogensec Jailbreak Corpus v0.3 công bố 59.508 dòng, gồm 43.026 seed thật và 16.482 mẫu synthetic từ 14 nguồn; dữ liệu gated, dùng license mixed-source và không mở payload/không chấp nhận điều khoản. Card mô tả nhãn technique/harm rule-based với độ bao phủ yếu; các trường này không tạo co-label PI+JB trực tiếp. [[163]](#ref163)

AEGINEL vẫn là lead BOTH đáng chú ý trên metadata: báo cáo nêu 188.109 mẫu, 21.544 mẫu multi-label và các nhóm Jailbreak/Prompt Injection, nhưng dataset payload và license riêng chưa thấy trong repo công khai đã kiểm tra. Sáu co-label trực tiếp CORTYX từ vòng 46 vẫn tập trung trong một source group. [[143]](#ref143) [[144]](#ref144) [[147]](#ref147)

## Kết luận và bước tiếp theo

Vòng 47 tìm được thêm JB-only pool để cân nhắc cho train tương lai, nhưng **không bổ sung BOTH hợp lệ**. Quickium lặp source family đã có trong v0.2.5; jackhhao còn source lineage/near-duplicate và release-count cần xử lý; mẫu Manteclaw không có BOTH mới và vướng license conflict; Cogensec gated. Vì vậy train BOTH vẫn 52/100, direct two-axis evidence vẫn 24, fit gate còn đóng và chưa có metrics train/valid/test mới.

Giữ package v0.2.5 nguyên trạng. Nếu chọn tích hợp thêm data, tạo dataset version mới (v0.2.6) sau khi có tối thiểu 48 BOTH co-label độc lập còn thiếu, được hỗ trợ trên cùng dòng bởi hai nhãn trực tiếp và đến từ nhiều source family; các lớp test còn thiếu cũng cần source-held-out, chưa đụng tới test v0.2.5. Các candidate JB-only trên chỉ hỗ trợ train sau khi rà near-duplicate, provenance và licensing. Nhãn vẫn là proxy theo taxonomy nguồn, không phải gold do người gán.

Artifacts: [metadata sàng lọc vòng 47](../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/candidate_screen_20261024_round47/SOURCE_SCREENING_ROUND47_METADATA.json) · [audit Quickium](../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/quickium_prompt_security_v0_20261024/CANDIDATE_AUDIT.json) · [audit jackhhao](../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/jackhhao_jailbreak_classification_20261024/CANDIDATE_AUDIT.json) · [audit Manteclaw](../../../workspaces/truongnv/shared_data/pi_guard_datasets/l3_subtype/source_datasets/manteclaw_llm_safety_20261024/CANDIDATE_AUDIT.json) · [task checklist](../../../.agents/artifacts/TASK_L3_SUBTYPE_V025_SOURCE_DISCOVERY_ROUND47_20261024.md)
