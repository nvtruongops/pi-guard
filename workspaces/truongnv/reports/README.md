# PI-Guard reports — active work and references

## Current work

The active report process is Review 2. Its umbrella task remains open; see [task overview](tasks_for_review2/README.md) and [TASK.md](tasks_for_review2/TASK.md).

A separate seed-42 TF-IDF → DeBERTa experiment is complete on one pinned PIDS-Bench split: [report](experiment_reports/tfidf_deberta_cascade_2026-10-04/REPORT.md), [progress](experiment_reports/tfidf_deberta_cascade_2026-10-04/TASK_PROGRESS.md). It is local experimental evidence, not final model/KPI acceptance or a deployed API.

## Historical reference folders

The following folders are retained as references: report_for_meeting_4, report_for_review1, tasks_for_meeting_5, and tasks_for_meeting_6. Use their original task context; do not treat them as the current work queue.

Older provenance, withdrawn-artifact, and paper-alignment audits are indexed under experiment_reports. Withdrawn artifacts may still exist on disk; the withdrawal record is not proof of deletion.

## Kiến trúc ingress dùng chung cho đồ án

Bản chuẩn có thể chỉnh sửa: [PI_GUARD_INGRESS_ARCHITECTURE.drawio](PI_GUARD_INGRESS_ARCHITECTURE.drawio). Ảnh xem nhanh trang luồng hoạt động: [PI_GUARD_INGRESS_ARCHITECTURE.png](PI_GUARD_INGRESS_ARCHITECTURE.png).

Đây là **baseline kiến trúc đề xuất** dùng làm kiến trúc tham chiếu chung trong các báo cáo đến cuối đồ án. Nó mô tả thiết kế mục tiêu; không xác nhận mọi khối đã được triển khai hoặc đạt KPI. Khi có quyết định kiến trúc mới, cập nhật bản chuẩn này và ghi lại thay đổi trong báo cáo/mốc liên quan.

### Các trang trong sơ đồ

1. **Detailed Architecture** — toàn cảnh các tầng, API, DTO, biên hệ thống ngoài và các nhánh lỗi.
2. **Architecture Summary — Vertical** — UML Activity Diagram ở mức request, từ đầu vào đến trạng thái cuối.
3. **L1 — Minimal Flow** — luồng tiếp nhận prompt/tệp, kiểm tra hợp lệ, trích xuất và chuẩn hóa.
4. **L2 — Minimal Flow** — chấm điểm từng chunk/view và phát ứng viên ALLOW, REVIEW hoặc BLOCK.
5. **L3 + API — Minimal Flow** — bàn giao REVIEW cho L3, ghép dự đoán và quyết định request ở API.
6. **L1 — Ingress & Preprocessing (Detailed)** — nhánh prompt/tệp, bộ trích xuất, kiểm tra coverage và `CanonicalTextEnvelope`.
7. **L2 — TF-IDF + LR Routing (Detailed)** — TF-IDF/LR, điểm `p_attack`, ứng viên tuyến, DTO và điều kiện lỗi.
8. **L3 — DeBERTa → API → Streaming (Detailed)** — đầu vào/đầu ra L3, API, provider, LLM ngoài và dashboard.

### Loại sơ đồ và quy ước ký hiệu

Trang 2 là **UML Activity Diagram** cho vòng đời xử lý một request. Trang 1 và các trang chi tiết là sơ đồ khối/luồng dữ liệu để giải thích thành phần và hợp đồng trao đổi; không nên đọc chúng như một UML Activity Diagram duy nhất.

| Ký hiệu | Ý nghĩa trong sơ đồ |
|---|---|
| Hình tròn đặc | Điểm bắt đầu hoạt động. |
| Hình tròn kép | Điểm kết thúc hoạt động UML. |
| Hình chữ nhật bo góc | Hành động/xử lý như L1, L2, L3, API, ALLOW hoặc BLOCK. |
| Hình thoi | Điểm rẽ nhánh hoặc quyết định; nhãn cạnh chỉ điều kiện/nhánh. Chỉ hình thoi của API tạo quyết định cuối cho request. |
| Hình chữ nhật góc vuông | Dữ liệu/DTO, đầu vào/đầu ra, hoặc hệ thống ngoài; tên trong ô cho biết loại cụ thể. |
| Khung nét đứt | Biên/nhóm hệ thống, không phải một bước xử lý. |
| Mũi tên có nhãn | Hướng chuyển dữ liệu hoặc điều khiển; đọc tên DTO/điều kiện trên cạnh. |

Không dùng hình bình hành trong bản chuẩn này. Màu sắc chỉ giúp phân biệt tầng và nhánh khi đọc; ý nghĩa quyết định nằm ở nhãn, hình dạng và hướng mũi tên.

### Vai trò các khối và hợp đồng quyết định

| Khối | Chức năng và đầu ra |
|---|---|
| **L1 — Ingress & preprocessing** | Kiểm tra đầu vào, trích xuất nội dung tệp được hỗ trợ, chuẩn hóa/chia chunk và tạo `CanonicalTextEnvelope` có ID/nguồn gốc. |
| **L2 — Word TF-IDF + Logistic Regression** | Chấm điểm từng chunk/view, trả `p_attack` cùng ID và đúng một ứng viên tuyến: ALLOW, REVIEW hoặc BLOCK. |
| **API router / orchestrator** | Nhận mọi kết quả L2 và ID dự kiến; chỉ chuyển chunk REVIEW sang L3, đồng thời giữ lại ứng viên ALLOW/BLOCK để tổng hợp. |
| **`RoutedChunk[]`** | Hợp đồng bàn giao các chunk thuộc REVIEW cho L3; mang ID và nội dung cần thiết để ghép kết quả. |
| **L3 — Project DeBERTa classifier** | Phân loại các chunk/window được API chuyển đến và trả `WindowPrediction[]`; L3 không tự kết luận trạng thái request. |
| **API coverage + request aggregation** | Ghép ứng viên L2 và dự đoán L3 theo ID, kiểm tra đủ coverage và lỗi. Thiếu kết quả/lỗi thì fail closed. |
| **Final request decision** | API áp dụng policy trên kết quả đầy đủ và duy nhất phát trạng thái cuối ALLOW hoặc BLOCK. |
| **Target LLM / dashboard** | Chỉ gọi Target LLM sau final ALLOW; dashboard nhận trạng thái cuối và câu trả lời nếu request được ALLOW. BLOCK không gọi LLM. |

Các ngưỡng `τ_allow`/`τ_block` trên sơ đồ là **giả định của đề xuất**, chưa phải ngưỡng dịch vụ đã được xác lập. Ngưỡng được chọn trên validation trong phép chạy seed-42 chỉ có hiệu lực cho lần chạy đó. Một số trang chi tiết có thể ghi rõ chế độ kiểm định offline (ví dụ chấm toàn bộ chunk) hoặc trạng thái cổng dịch vụ chưa cấu hình; các ghi chú đó không thay đổi luồng mục tiêu REVIEW-only ở trên.

## Scope Boundary Declaration

- IN-SCOPE: current Review 2 task and separately documented experiment evidence.
- OUT-OF-SCOPE: reviving frozen historical claims, representing one run as final acceptance, or editing shared official deliverables without an explicit consolidation task.
