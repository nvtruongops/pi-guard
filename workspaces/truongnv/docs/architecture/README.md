# PI-Guard Threat Model & Proposed Architecture

Thư mục chứa threat model định tính và các phương án kiến trúc. Tài liệu kiến trúc là đề xuất; không chứng minh cascade đã được triển khai hoặc đánh giá.

## Nguồn chuẩn cho kiến trúc ingress hiện hành

Hồ sơ [Review 1 lần 2](../../reports/report%20for%20review%201%20lan%202/README.md) cùng [TASK.md](../../reports/report%20for%20review%201%20lan%202/TASK.md) là nguồn chuẩn cho proposal L1 ingress → L2 TF-IDF + Logistic Regression → L3 classifier DeBERTa-v3 → API aggregation/policy. “Two-tier” trong tài liệu cũ nói đến hai bộ chấm điểm ML L2/L3; L1 và API không phải hai classifier bổ sung. Toàn bộ luồng vẫn là đề xuất chưa được chứng minh là đã triển khai hoặc đánh giá.

---

## 🏛️ Tài liệu kiến trúc

1. [`THREAT_MODEL_AND_ATTACK_SURFACE.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/architecture/THREAT_MODEL_AND_ATTACK_SURFACE.md)
   - Mô tả định tính bài toán, ranh giới an toàn và các nhóm tình huống cần xem xét.
   - Xác định tài sản bảo vệ và bề mặt tiếp nhận dữ liệu không tin cậy.

2. [`MULTI_LAYER_DEFENSE_ARCHITECTURE.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/architecture/MULTI_LAYER_DEFENSE_ARCHITECTURE.md)
   - Đề xuất kiến trúc nhiều tầng; chưa có kết quả local chứng minh routing hoặc hiệu năng end-to-end.

3. [`COMPARATIVE_MATRIX_AND_TRADEOFFS.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/architecture/COMPARATIVE_MATRIX_AND_TRADEOFFS.md)
   - So sánh khái niệm các phương pháp trong y văn; không xếp hạng các phép chạy local khác protocol.
   - Phân biệt mục tiêu thiết kế P95/FPR với số liệu thực nghiệm đã đạt.

4. [`ARCHITECTURAL_DEPRECATIONS_AND_OUT_OF_SCOPE.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/ARCHITECTURAL_DEPRECATIONS_AND_OUT_OF_SCOPE.md)
   - Quy định ranh giới bất biến về các công nghệ bị loại khỏi phạm vi (INT8 Quantization, ONNX Runtime, ZeroQuant, v.v.).

Trạng thái phép chạy và giới hạn bằng chứng được ghi trong [workspace provenance audit](file:///d:/Work/Do-an/workspaces/truongnv/reports/experiment_reports/WORKSPACE_PROVENANCE_AUDIT_2026-09-30.md).
