# PI-Guard Research Notes

Thư mục này chứa ma trận lựa chọn mô hình, ghi chú trạng thái bằng chứng và các bản lưu trữ. Nó không thay thế báo cáo thực nghiệm chuẩn trong `reports/` hoặc `replications/`.

## Tài liệu đang dùng

- [Kiến trúc ingress Review 1 lần 2](../../reports/report%20for%20review%201%20lan%202/README.md): nguồn chuẩn cho đề xuất L1/L2/L3/API; không phải bằng chứng triển khai hoặc đánh giá.
- [Ma trận lựa chọn DeBERTa-v3](./dossiers/04_DEBERTA_MODEL_SELECTION_MATRIX.md): tách thông tin từ model card/paper khỏi đề xuất mô hình của nhóm; chưa có kết quả fine-tune PI-Guard.
- [Trạng thái SOTA và bằng chứng baseline](./dossiers/03_SOTA_SURVEY_AND_6BASELINES.md): giới hạn các kết quả cục bộ được giữ lại; các bảng sáu baseline/D1–D6 cũ đã bị rút.
- [Trạng thái provenance dữ liệu](./dossiers/04_DATA_ENGINEERING_PROVENANCE.md): ghi lại nguồn dữ liệu, kết quả và những gói đã bị rút.
- [PIDS-Bench: paper và mức phù hợp với PI-Guard](./dossiers/05_PIDS_BENCH_PAPER_FIT.md): hard-benign, hard-negative, provenance và giới hạn khi suy rộng sang cascade.
- [Audit cấu trúc thư mục research (snapshot 01/10/2026)](./RESTRUCTURE_AUDIT_2026-10-01.md): chỉ ghi nhận cấu trúc research tại ngày đó; không thay thế proposal kiến trúc hiện hành.

## Tài liệu lưu trữ

Các tệp trong [`archive/`](./archive/) là thông báo thu hồi bản nháp cũ và demo mô phỏng đã rút khỏi luồng hoạt động; không dùng chúng làm nguồn lý thuyết hoặc bằng chứng hiệu năng. Chỉ khôi phục một luận điểm sau khi đối chiếu paper gốc hoặc bằng chứng thực nghiệm tương ứng.

## Demo đã rút khỏi luồng hoạt động

- [demo_deberta_v3_random_simulation.py](./archive/demo_deberta_v3_random_simulation.py) chỉ tạo ma trận ngẫu nhiên để minh họa và mô phỏng INT8; nó không nạp hay chạy DeBERTa thật, còn INT8 nằm ngoài phạm vi kiến trúc hiện hành. Không dùng file này làm benchmark, dẫn chứng hoặc hướng dẫn huấn luyện.

Demo TF-IDF dùng 12 câu viết sẵn và tự fit một cấu hình `char_wb`/Logistic Regression đã được gỡ vì không tái lập giao thức của một benchmark/paper cụ thể. Điều này không có nghĩa TF-IDF thiếu tài liệu tham khảo: baseline TF-IDF có paper-matched evidence vẫn được ghi tại [báo cáo PIDS-Bench](../../replications/PIDS_Bench_Shire_IEEEAccess2026/REPORT.md).
