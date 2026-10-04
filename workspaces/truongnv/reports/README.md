# PI-Guard Master Report Registry & Navigation Index

Thư mục tổng hợp toàn bộ các báo cáo kỹ thuật, hồ sơ bảo vệ hội đồng, biên bản họp định kỳ và kiểm toán xuất xứ dữ liệu của workspace `truongnv`.

---

## 📂 1. Phân loại cấu trúc Báo cáo (Report Taxonomy)

```
reports/
├── README.md                                      # Bản đồ điều hướng và trạng thái bằng chứng
├── experiment_reports/                            # Hồ sơ thực nghiệm, kiểm toán xuất xứ & governance
│   ├── WORKSPACE_PROVENANCE_AUDIT_2026-09-30.md   # Hồ sơ chuẩn về bằng chứng và các phép chạy thu hồi
│   ├── REPO_GOVERNANCE_AND_RESEARCH_MCP_AUDIT_2026-09-28.md # Kiểm toán governance và cấu hình MCP
│   ├── replications_folder_audit_2026-09-30/     # Audit nguồn và vị trí replication
│   └── reproduction_audit_2026-09-29/             # Hồ sơ lịch sử; kết quả cũ đã thu hồi
├── report_for_meeting_4/                           # Hồ sơ Meeting 4 đã lưu trữ
├── report_for_review1/                            # Hồ sơ Review 1 và trạng thái bằng chứng
├── tasks_for_meeting_5/                           # Hồ sơ Meeting 5 đã lưu trữ
├── tasks_for_meeting_6/                           # Hồ sơ Meeting 6; benchmark cross-paper đã thu hồi
└── tasks_for_review2/                              # Nhiệm vụ nghiên cứu và demo cho Review 2
```

Danh mục deprecation và giới hạn phạm vi hiện hành nằm trong [Rule 02](file:///d:/Work/Do-an/.agents/rules/rule-02-task-scope-and-milestone-enclosure.md).

> [!NOTE]
> Toàn bộ biên bản họp định kỳ chung của nhóm với GVHD được quản lý tập trung tại [`Final-Report/Meeting/`](file:///d:/Work/Do-an/Final-Report/Meeting/). Các thư mục `report_for_meeting_*`, `tasks_for_meeting_*` và `tasks_for_review*` tại đây lưu tài liệu kỹ thuật cá nhân theo từng đợt review/meeting.

## Review 1 và Review 2

- Báo cáo tổng kết Review 1 hoàn tất ngày 04/10/2026: [REVIEW_1_COMPLETION_REPORT_2026-10-04.md](report_for_review1/REVIEW_1_COMPLETION_REPORT_2026-10-04.md).
- Task Review 2 — nghiên cứu mô hình đề xuất và demo hoạt động: [tasks_for_review2/TASK.md](tasks_for_review2/TASK.md). Task thực nghiệm cascade liên quan được theo dõi riêng tại [experiment_reports/tfidf_deberta_cascade_2026-10-04/TASK.md](experiment_reports/tfidf_deberta_cascade_2026-10-04/TASK.md).


---

## 🔬 2. Hiện trạng bằng chứng thực nghiệm hợp lệ (Eligible Empirical Evidence)

Theo Quy tắc Ranh giới Xuất xứ Cặp Mô hình - Dữ liệu cùng bài báo (Same-Paper Pairing Rule):

| Phép đo / Mô hình | Trạng thái kiểm chứng | Giới hạn & Lưu ý | Báo cáo chi tiết |
| :--- | :--- | :--- | :---: |
| **PIDS-Bench TF-IDF + Logistic Regression** | **Hợp lệ (Pass)** | Mô hình baseline cú pháp tác giả công bố, đối chuẩn trên tập test 3.918 mẫu PIDS-Bench v3. | [REPORT.md](file:///d:/Work/Do-an/workspaces/truongnv/replications/PIDS_Bench_Shire_IEEEAccess2026/REPORT.md) |
| **PIGuard Checkpoint (DeBERTa-v3)** | **Hợp lệ (Pass)** | Đánh giá checkpoint gốc của Hao Li trên đúng các tập con được phát hành kèm bài báo PIGuard. | [REPORT.md](file:///d:/Work/Do-an/workspaces/truongnv/replications/02_DeBERTa_v3_Semantic_Classifier/reports/review1_paper_model_public_rerun_2026-09-30/REPORT.md) |

---

## ⚠️ 3. Bằng chứng thực nghiệm đã thu hồi (Withdrawn Artifacts)

- Các bộ vector cross-source Review 1, ma trận 6 checkpoint D1–D6, các lượt fit TF-IDF trộn nguồn Review 2/Tier 1, và so sánh ProtectAI trên dữ liệu PIDS-Bench đã bị thu hồi do vi phạm quy tắc ghép cặp chéo bài báo.
- Chi tiết danh mục tệp thu hồi xem tại: [`tasks_for_meeting_6/WITHDRAWN_DATA_ARTIFACTS.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_6/WITHDRAWN_DATA_ARTIFACTS.md) và [`experiment_reports/WORKSPACE_PROVENANCE_AUDIT_2026-09-30.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/experiment_reports/WORKSPACE_PROVENANCE_AUDIT_2026-09-30.md).
