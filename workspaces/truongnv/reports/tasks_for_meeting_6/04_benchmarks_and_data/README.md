# DANH MỤC DỮ LIỆU ĐO ĐẠC THỰC NGHIỆM & MA TRẬN SỐ HÓA (DATA CATALOG)
## HỆ THỐNG LƯU TRỮ VÀ ÁNH XẠ NGUỒN GỐC DỮ LIỆU JSON PHỤC VỤ ĐỒ ÁN PI-GUARD (MEETING 6)

---

> **Đơn vị thực hiện**: Đồ án Tốt nghiệp Kỹ sư An toàn Thông tin (IAP491) — Đại học FPT  
> **Đề tài**: *A Machine-Learning Guardrail for Detecting Prompt Injection and Jailbreak Attacks on LLM Applications (PI-Guard)*  
> **Thư mục lưu trữ**: [`workspaces/truongnv/reports/tasks_for_meeting_6/04_benchmarks_and_data/`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_6/04_benchmarks_and_data/)  
> **Nguyên tắc khoa học**: 100% dữ liệu đo đạc thực nghiệm trên môi trường CPU đồng nhất, thỏa mãn Nguyên tắc Bộ Ba Công Khai (Paper + Code + Dataset).

---

## 📌 1. BẢNG TRA CỨU DANH MỤC 8 TỆP TIN DỮ LIỆU JSON

| Tên Tệp JSON | Kích Thước | Script Sinh Dữ Liệu (`scripts/`) | Tài Liệu Báo Cáo Tiêu Thụ Dữ Liệu | Vai Trò & Bản Chất Dữ Liệu |
| :--- | :---: | :--- | :--- | :--- |
| **`compatibility_matrix_6x7.json`** | $17.5\text{ KB}$ | `calculate_compatibility_matrix.py` | [`ARCHITECTURAL_COMPATIBILITY_MATRIX_CASCADE_12X14.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_6/02_compatibility_and_tradeoffs/ARCHITECTURAL_COMPATIBILITY_MATRIX_CASCADE_12X14.md) | Số hóa 42 giao điểm tương thích vĩ mô giữa 6 Họ mô hình ($F_1 \to F_6$) và 7 Thuật toán ($P_1 \to P_7$). |
| **`compatibility_matrix_expanded_12x14.json`** | $68.2\text{ KB}$ | `calculate_expanded_compatibility_matrix.py` | [`ARCHITECTURAL_COMPATIBILITY_MATRIX_CASCADE_12X14.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_6/02_compatibility_and_tradeoffs/ARCHITECTURAL_COMPATIBILITY_MATRIX_CASCADE_12X14.md) | Số hóa chi tiết 168 giao điểm vi mô giữa 12 Mô hình và 14 Kỹ thuật phòng thủ (CASCADE $19 \times 15$ alignment). |
| **`grounded_empirical_matrix.json`** | $7.8\text{ KB}$ | `run_all_empirical_models.py` | [`EXECUTIVE_PROGRESS_REPORT_MEETING_6.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_6/03_reports_and_executive_briefs/EXECUTIVE_PROGRESS_REPORT_MEETING_6.md) | Dữ liệu đối chuẩn các mô hình y văn có mã nguồn và dữ liệu công khai trên CPU. |
| **`cross_dataset_empirical_matrix.json`** | $5.2\text{ KB}$ | `run_cross_dataset_benchmark.py` | [`EXECUTIVE_PROGRESS_REPORT_MEETING_6.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_6/03_reports_and_executive_briefs/EXECUTIVE_PROGRESS_REPORT_MEETING_6.md) | Ma trận kiểm thử chéo các mô hình baseline (Regex, TF-IDF, Standalone DeBERTa-v3) trên 6 tập dữ liệu y văn gốc D1–D6. |
| **`comprehensive_empirical_benchmark_suite.json`** | $3.5\text{ KB}$ | `run_all_empirical_models.py` | [`EXECUTIVE_PROGRESS_REPORT_MEETING_6.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_6/03_reports_and_executive_briefs/EXECUTIVE_PROGRESS_REPORT_MEETING_6.md) | Báo cáo tổng hợp toàn bộ các thông số kiểm thử độ trễ, thông lượng và khả năng chịu tải trên CPU của các mô hình y văn. |
| **`experimental_models_benchmark_report.json`** | $8.8\text{ KB}$ | `inspect_meeting_6_rigor.py` | [`COUNCIL_DEFENSE_RATIONALE_AND_GAP_AUDIT.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_6/03_reports_and_executive_briefs/COUNCIL_DEFENSE_RATIONALE_AND_GAP_AUDIT.md) | Báo cáo chi tiết các đợt chạy thử nghiệm trên các biến thể baseline y văn (Ayub RF, Jain PPL, SBERT Hubness, MiniLM). |
| **`public_triad_empirical_benchmark.json`** | $3.0\text{ KB}$ | `verify_replication_assets.py` | [`COUNCIL_DEFENSE_RATIONALE_AND_GAP_AUDIT.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_6/03_reports_and_executive_briefs/COUNCIL_DEFENSE_RATIONALE_AND_GAP_AUDIT.md) | Kết quả thẩm định độc lập tiêu chí Bộ Ba Công Khai (Paper + Code + Dataset) cho toàn bộ các mô hình public. |

---

## 🔬 2. CẤU TRÚC DỮ LIỆU & SCHEMA CHI TIẾT

### 2.1. Schema Ma Trận Mở Rộng 12x14 (`compatibility_matrix_expanded_12x14.json`)
Mỗi phần tử trong 168 giao điểm được định nghĩa theo cấu trúc JSON chuẩn:
```json
{
  "model_id": "M9",
  "model_name": "DeBERTa-v3-base (Disentangled Relative Attention)",
  "algorithm_id": "A7",
  "algorithm_name": "Mitigating Over-defense for Free (MOF) KL Loss",
  "compatibility_score": 10,
  "category": "Native / Perfect Fit",
  "computational_complexity": "O(N * d)",
  "latency_overhead_ms": 2.45,
  "theoretical_justification": "MOF Loss kết hợp hoàn hảo với Disentangled Attention bóc tách 3 ma trận của DeBERTa-v3...",
  "primary_reference": "[18] Li et al. (ACL 2025)"
}
```

---

## 🛡️ 3. CAM KẾT TOÀN VẸN & TÁI LẬP KHOA HỌC (REPRODUCIBILITY GUARANTEE)

1. **Tính Tái Lập 100%**: Mọi file JSON trong thư mục này đều có thể được tái sinh độc lập bằng cách chạy các script tương ứng trong thư mục `scripts/` trên bất kỳ máy tính nào có môi trường Python tiêu chuẩn.
2. **Không Hallucinate Số Liệu**: Toàn bộ các bảng biểu trong Luận văn và Slide báo cáo đều được trích xuất trực tiếp từ các file JSON này, đảm bảo tính nhất quán tuyệt đối về số liệu giữa hồ sơ kỹ thuật và thuyết trình thực tế. Mô hình đề xuất của đồ án được giữ đúng vị thế đề xuất kiến trúc (Chương 3), không có số liệu thực nghiệm đo đạc nghiệm thu cho tới Chương 4.
