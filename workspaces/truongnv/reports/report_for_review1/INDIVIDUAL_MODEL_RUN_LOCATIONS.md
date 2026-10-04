# Vị trí run hợp lệ và các run đã rút

## Scope Boundary Declaration

- **IN-SCOPE:** xác định paper, model, data, artifact và giới hạn của run trong workspace `truongnv`.
- **OUT-OF-SCOPE:** ghép model với data từ paper khác hoặc gán baseline/checkpoint cho cascade PI-Guard.

| Run | Pairing nguồn | Trạng thái |
|---|---|---|
| PIDS-Bench TF-IDF + Logistic Regression | Code baseline và split cùng paper PIDS-Bench. 3.918 prediction rows đã đối chiếu với test split gốc. | Giữ metric test ngưỡng 0,5 sau khi tính lại từ prediction. [Report](../../replications/PIDS_Bench_Shire_IEEEAccess2026/REPORT.md). |
| PIGuard DeBERTa-v3 riêng lẻ | Checkpoint và public evaluation assets trong pinned PIGuard release. | Giữ metric theo slice, có denominator và giới hạn payload. [Report](../../replications/02_DeBERTa_v3_Semantic_Classifier/reports/review1_paper_model_public_rerun_2026-09-30/REPORT.md). |
| ProtectAI trên PIDS-Bench/PIGuard data | Checkpoint ProtectAI ghép với data paper khác. | Rút local metrics và comparisons. |
| Public vectors, D1–D6, Review 2, Tier 1 TF-IDF | Suite/split ghép nhiều nguồn paper. | Rút metrics, latency, chart, recommendation; thư mục vẫn còn vì lệnh xóa bị chặn. |

Xem [workspace audit](../experiment_reports/WORKSPACE_PROVENANCE_AUDIT_2026-09-30.md) để biết residual folders và verification record.
