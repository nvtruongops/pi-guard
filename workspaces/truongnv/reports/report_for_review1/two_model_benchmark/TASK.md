# Nhiệm vụ — Gói bằng chứng hai baseline PIDS-Bench

**Nguồn yêu cầu:** chỉ đạo của người dùng ngày 2026-09-30. **Phạm vi:** sắp xếp hai kết quả đã chạy thành một gói Review 1 có thể rà soát; không chạy lại hay huấn luyện mô hình mới.

## Scope Boundary Declaration

- **IN-SCOPE:** đặt báo cáo riêng cho TF-IDF + Logistic Regression và ProtectAI DeBERTa-v3; lưu bản PDF paper trong từng thư mục; đóng gói JSON kết quả, dự đoán, dữ liệu đã dùng và thông tin nguồn/giấy phép; làm ma trận recall theo loại tấn công của PIDS-Bench.
- **OUT-OF-SCOPE:** cascade PI-Guard; fine-tune DeBERTa tại chỗ; gán kết quả nhị phân thành phân loại ba lớp Prompt Injection/Jailbreak/Benign; tái sử dụng số liệu của bundle cũ đã rút; sửa hoặc xóa các bundle cũ.

## Bàn giao và kiểm tra phạm vi

- [x] Tạo thư mục gói mới dưới `reports/report_for_review1/two_model_benchmark/`.
- [x] Có paper, báo cáo, kết quả, mô tả dữ liệu và hướng dẫn truy nguồn cho từng mô hình.
- [x] Giữ chung một bản dữ liệu đóng băng để hai lần chạy cùng đầu vào.
- [x] Ghi rõ số liệu là lần chạy độc lập tại chỗ; DeBERTa chỉ inference checkpoint ProtectAI.
- [x] Đối chiếu SHA-256 của dữ liệu đóng gói với manifest nguồn và kiểm tra liên kết nội bộ.

## Tuyên bố phạm vi

Gói này tổ chức lại bằng chứng của hai lần chạy PIDS-Bench đã có trong `replications/PIDS_Bench_Shire_IEEEAccess2026/`. Nó không tạo ra kết quả mới cho mô hình cascade hay classifier ba nhãn.
