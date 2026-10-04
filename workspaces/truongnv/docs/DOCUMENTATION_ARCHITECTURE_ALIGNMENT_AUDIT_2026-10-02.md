# Audit đồng bộ `docs/` với kiến trúc Review 1 lần 2 — 2026-10-02

## 1. Scope Boundary Declaration

- **Nguồn chuẩn:** [TASK.md của hồ sơ Review 1 lần 2](../reports/report%20for%20review%201%20lan%202/TASK.md), [README kiến trúc](../reports/report%20for%20review%201%20lan%202/README.md), [căn cứ routing](../reports/report%20for%20review%201%20lan%202/01_TWO_TIER_CASCADE_EVIDENCE.md) và [thiết kế chunk/backend handoff](../reports/report%20for%20review%201%20lan%202/07_CHUNKING_AND_BACKEND_HANDOFF_DESIGN.md).
- **IN-SCOPE:** đối chiếu các tài liệu hiện có trong `workspaces/truongnv/docs/` với kiến trúc, thuật ngữ và trạng thái bằng chứng của hồ sơ trên; sửa link hỏng và cách diễn đạt có thể khiến người đọc nhầm proposal với hệ thống đã làm.
- **OUT-OF-SCOPE:** sửa nguồn chuẩn trong `reports/`, triển khai backend, huấn luyện/đánh giá mô hình, bổ sung metric, hoặc xác nhận proposal đã được hội đồng thông qua.

## 2. Kết quả kiểm định và xử lý

| Nhóm kiểm tra | Phát hiện có thể gây nhầm | Xử lý trong `docs/` |
|---|---|---|
| Tên tầng và số mô hình | Một số tài liệu dùng “two-tier” cạnh pipeline L1/L2/L3/API mà chưa nói rõ L1 và API không phải các bộ phân loại bổ sung. | Ghi rõ L1 là ingress preprocessing, L2 là TF-IDF + Logistic Regression, L3 là classifier DeBERTa dự kiến, còn API kiểm tra coverage/tổng hợp/chọn trạng thái request. “Two-tier” chỉ hai bộ chấm điểm ML L2/L3. |
| Proposal và bằng chứng | Chỉ mục docs ghi chưa có cascade nhưng chưa trỏ tới proposal hiện hành, khiến người đọc có thể hiểu nhầm là chưa có thiết kế hoặc ngược lại coi bản thiết kế là kết quả. | Tách mục kiến trúc đề xuất khỏi hai báo cáo thực nghiệm còn được giữ; thêm provenance proposal vào ma trận; gắn rõ trạng thái “chưa triển khai/đánh giá”. |
| DeBERTa tại L3 | Ma trận checkpoint nói về ứng viên mô hình nhưng chưa nối rõ với vị trí L3 trong proposal. | Thêm liên kết và ghi rõ backbone/classification head, fine-tuning PI-Guard chưa được triển khai hoặc đánh giá. |
| Hồ sơ Review 1 | README luận văn không phân biệt rõ thư mục hồ sơ Review 1 đã lưu với vòng hồ sơ “Review 1 lần 2”; cũng mô tả một rubric đã rút như tài liệu hiện hành. | Tách hai hồ sơ theo mục đích; đổi nhãn rubric thành bản cũ đã rút, không phải quy định chính thức của FPT. |
| Liên kết nội bộ | Kiểm tra ban đầu phát hiện 10 đường dẫn sai/hỏng trong ma trận provenance và ba trang kiến trúc; nguyên nhân gồm trỏ tới artifact đã rút hoặc đi sai số cấp thư mục. | Đổi các notice đã mất sang withdrawal register còn tồn tại; sửa đường dẫn tới report, provenance audit và reference log. |
| Snapshot lịch sử | Audit tái cấu trúc `docs/research` ngày 01/10 ghi nhận một thời điểm trước hồ sơ kiến trúc hiện tại. | Giữ nguyên nội dung lịch sử; README research gắn nhãn snapshot và chỉ tới proposal hiện hành riêng. |

Các tài liệu về threat model, so sánh phương pháp, provenance dữ liệu, hồ sơ luận văn rút và archive đã được rà. Nội dung phân biệt kết quả paper, phép chạy local và artifact bị rút được giữ lại; tombstone không được phục hồi thành bằng chứng. Xem [ma trận provenance tài liệu](./DOCUMENTATION_PROVENANCE_AND_DERIVATION_MATRIX.md) và [audit cấu trúc research ngày 01/10](./research/RESTRUCTURE_AUDIT_2026-10-01.md) với đúng phạm vi từng tài liệu.

### Tài liệu được đồng bộ trực tiếp

- Chỉ mục: [docs/README](./README.md), [research/README](./research/README.md), [architecture/README](./architecture/README.md), [thesis/README](./thesis/README.md).
- Kiến trúc và provenance: [ma trận provenance](./DOCUMENTATION_PROVENANCE_AND_DERIVATION_MATRIX.md), [multi-layer status](./architecture/MULTI_LAYER_DEFENSE_ARCHITECTURE.md), [comparative matrix](./architecture/COMPARATIVE_MATRIX_AND_TRADEOFFS.md), [threat model](./architecture/THREAT_MODEL_AND_ATTACK_SURFACE.md).
- Nghiên cứu mô hình: [SOTA/baseline status](./research/dossiers/03_SOTA_SURVEY_AND_6BASELINES.md), [DeBERTa model selection](./research/dossiers/04_DEBERTA_MODEL_SELECTION_MATRIX.md).

### Tài liệu đã rà và giữ nguyên

[Dossier provenance dữ liệu](./research/dossiers/04_DATA_ENGINEERING_PROVENANCE.md), [trang trạng thái luận văn](./thesis/FINAL_THESIS.md), [trạng thái chương 1–2](./thesis/chapters/README.md) và các tombstone/archive vẫn phân biệt đúng metric paper, phép chạy local và artifact bị rút; chúng không cần sửa để khớp proposal hiện tại.

## 3. Trạng thái kiến trúc cần giữ nhất quán

1. **L1:** tiếp nhận/trích xuất, chuẩn hóa, chia chunk và giữ định danh/source map.
2. **L2:** TF-IDF + Logistic Regression chấm từng chunk; route là candidate theo score và chỉ được tự động bật sau validation.
3. **L3:** classifier DeBERTa-v3 của đồ án được đề xuất cho phần chunk/window được chuyển tới; đầu ra là score/nhãn, không phải quyết định cuối request.
4. **API:** kiểm tra coverage, tổng hợp kết quả cấp request và chọn ALLOW / REVIEW / BLOCK. REVIEW/HOLD là trạng thái API; chỉ nhánh ALLOW được proposal chuyển tới target LLM.
5. Đây là **thiết kế đề xuất**. Threshold/chunk config vẫn cần validation; tài liệu không xác nhận DeBERTa ba nhãn đã fine-tune, cascade đã triển khai, hoặc metric/latency đã đạt. Trạng thái nguồn được ghi trong [README hồ sơ](../reports/report%20for%20review%201%20lan%202/README.md) và [TASK.md](../reports/report%20for%20review%201%20lan%202/TASK.md).

## 4. Checklist tuân thủ phạm vi

- [x] Chỉ sửa/tạo tài liệu bên trong `workspaces/truongnv/docs/`; giữ nguyên source report, code và dữ liệu.
- [x] Không thêm metric, kết quả chạy, hay khẳng định hiệu quả cascade.
- [x] Không biến model card/paper evidence thành kết quả PI-Guard.
- [x] Không đưa công nghệ nằm ngoài kiến trúc đã chốt vào proposal.
- [x] Tách proposal Review 1 lần 2 khỏi hồ sơ Review 1 đã lưu và khỏi các snapshot lịch sử.
- [x] Kiểm tra lại liên kết Markdown nội bộ: không còn đường dẫn trực tiếp bị hỏng trong 23 tài liệu `.md` dưới `docs/`.
- [x] Chạy claim-evidence và glossary audit trên 23 tài liệu `.md` dưới `docs/`: cả hai lượt đều 23/23 exit code 0.

## 5. Giới hạn

Đây là kiểm định tài liệu cục bộ, không phải đánh giá độc lập tính đúng đắn của mọi paper/model card, xác nhận trạng thái nộp hội đồng, hay xác minh triển khai bằng runtime. Nguồn cho thiết kế và ranh giới nhiệm vụ vẫn là hồ sơ Review 1 lần 2 được liên kết ở phần đầu.
