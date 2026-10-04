# PI-Guard documentation index

## Scope Boundary Declaration

- **IN-SCOPE:** documentation status, paper-matched local evidence, and the current ingress-architecture proposal.
- **OUT-OF-SCOPE:** present withdrawn cross-paper results as current metrics.

The Review 1 public-vector, Review 2/Tier 1 mixed-source, D1–D6, and ProtectAI-on-other-paper runs are withdrawn and their artifacts have been purged from disk. See the [withdrawal register](../reports/tasks_for_meeting_6/WITHDRAWN_DATA_ARTIFACTS.md) and [model-paper alignment audit](../reports/experiment_reports/MODEL_PAPER_CODE_ALIGNMENT_AUDIT_2026-10-02.md).

Current local evidence:

- [PIDS-Bench same-paper TF-IDF baseline](../replications/PIDS_Bench_Shire_IEEEAccess2026/REPORT.md)
- [PIGuard-only evaluation on PIGuard assets](../replications/02_DeBERTa_v3_Semantic_Classifier/reports/review1_paper_model_public_rerun_2026-09-30/REPORT.md)

## Kiến trúc ingress hiện hành — trạng thái đề xuất

- [Hồ sơ Review 1 lần 2](../reports/report%20for%20review%201%20lan%202/README.md) là nguồn mô tả proposal: L1 trích xuất/chuẩn hóa/chia chunk; L2 TF-IDF + Logistic Regression chấm từng chunk; L3 là classifier DeBERTa-v3 dự kiến; API kiểm tra coverage, tổng hợp request và chọn ALLOW / REVIEW / BLOCK.
- [TASK.md](../reports/report%20for%20review%201%20lan%202/TASK.md) khóa phạm vi và trạng thái. Cụm “two-tier” trong ghi chú cũ chỉ hai bộ chấm điểm ML ở L2/L3; L1 là ingress preprocessing và API là tầng orchestration/policy.
- Đây là thiết kế đề xuất, không chứng minh classifier PI-Guard đã fine-tune, cascade đã triển khai/đánh giá, hay mục tiêu metric/latency đã đạt. Các ghi chú research là tài liệu khái niệm/y văn trừ khi trỏ rõ tới một phép chạy hiện hành.

Xem thêm [audit đồng bộ tài liệu với kiến trúc](./DOCUMENTATION_ARCHITECTURE_ALIGNMENT_AUDIT_2026-10-02.md).
