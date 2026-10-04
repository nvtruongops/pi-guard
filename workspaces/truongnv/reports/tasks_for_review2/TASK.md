# Task — Review 2: nghiên cứu mô hình đề xuất và demo hoạt động

- **Milestone:** Review 2 / Meetings 7–10, Chương 3
- **Nguồn giao việc:** chỉ đạo của người dùng ngày 04/10/2026: nghiên cứu mô hình đề xuất và chuẩn bị demo để xác nhận model hoạt động.
- **Task nguồn cho kiến trúc:** [Review 1 lần 2](../report%20for%20review%201%20lan%202/TASK.md).
- **Task thực nghiệm liên quan:** [TF-IDF → DeBERTa Cascade Experiment](../experiment_reports/tfidf_deberta_cascade_2026-10-04/TASK.md).

## 1. Tuyên bố ranh giới nhiệm vụ

| IN-SCOPE | OUT-OF-SCOPE |
|---|---|
| (1) Nghiên cứu và giải thích mô hình ingress ba tầng/API đã đề xuất ở Review 1; gắn từng khẳng định với paper, model card hoặc bằng chứng cục bộ phù hợp. (2) Hoàn thiện đặc tả dữ liệu vào/ra, L2 TF-IDF + Logistic Regression, L3 DeBERTa-v3-base Native FP32, route/chunk/handoff, lỗi và API aggregation. (3) Dùng inference/model thật để demo L2, L3 và đường cascade theo protocol đã được giao; lưu lệnh chạy, cấu hình, provenance, output JSON un-mocked và ví dụ route. (4) Nêu lỗi, giới hạn, metric/denominator và việc nào còn pending. | (1) Tuyên bố demo là kết quả nghiệm thu cuối, hoặc tuyên bố P95 < 30 ms/FPR < 1.5% đã đạt nếu task không có phép đo tương ứng. (2) Dùng mock/random output hoặc số liệu tổng hợp không truy được JSON. (3) Ghép model/checkpoint với dataset của paper khác; khôi phục hoặc viện dẫn artifact đã thu hồi. (4) Sửa backend/product API, thêm parser/OCR/upload, hoặc mở rộng sang production. (5) INT8, ONNX Runtime, ZeroQuant, white-box steering/KV-cache. |

### Quy tắc đóng phạm vi

- Task Review 1 xác lập proposal và loại trừ việc triển khai cascade. Việc chạy thực nghiệm cascade ở Review 2 chỉ theo task thực nghiệm riêng đã có ở trên; task này không tự mở rộng protocol hoặc dữ liệu của task đó.
- Protocol thực nghiệm hiện có khóa ở PIDS-Bench cùng nguồn, seed-42, splits và author commit được ghi trong task thực nghiệm. Kết quả một seed chỉ mô tả lượt chạy đó; không được khái quát thành kết quả đa seed hoặc KPI cuối kỳ.
- Đặt script/demo ở thư mục thực nghiệm, ngoài product source tree. Không tạo `src/models/cascade/` trong task này.
- Chọn cutoff chỉ trên validation, đóng băng trước test. Nếu cutoff chưa được chọn/kiểm chứng, demo phải ghi rõ chế độ chạy; không bật shortcut như tính năng đã xác nhận.
- REVIEW là route nội bộ từ L2 sang L3; API kết thúc request bằng ALLOW hoặc BLOCK. Lỗi kỹ thuật không được đổi thành benign.

## 2. Bàn giao theo nhiệm vụ

### A. Nghiên cứu mô hình

- [ ] Tạo báo cáo ngắn giải thích mục tiêu và giả thuyết của cascade TF-IDF + Logistic Regression → DeBERTa-v3-base; phân biệt căn cứ paper, kết quả cục bộ và đề xuất PI-Guard.
- [ ] Mô tả chính xác input/output và trách nhiệm của L1, L2, L3, API aggregation; nêu rõ `p_attack`, route state, `τ_allow`, `τ_block`, chunk/window và nguồn gốc từng tham số.
- [ ] Chốt protocol dữ liệu/nhãn và provenance bằng cách tham chiếu task thực nghiệm; không tự đưa thêm data, checkpoint, hoặc nhãn mới.
- [ ] Nêu cách chọn threshold chỉ trên validation, baseline đối chiếu được yêu cầu, denominator của từng metric, và giới hạn của seed-42.

### B. Demo model chạy thật

- [ ] Chạy model L2 đã lưu và checkpoint L3 bằng inference không mock; ghi lại lệnh, môi trường, commit/config, file nguồn dữ liệu và hash checkpoint/dataset.
- [ ] Chạy đường xử lý cascade/handoff bằng output thật của model; lưu raw predictions và route counts ở JSON un-mocked. Một ví dụ minh họa không thay cho denominator hoặc đánh giá tập dữ liệu.
- [ ] Thể hiện nhánh REVIEW gọi L3; nhánh cuối ALLOW/BLOCK do API aggregation tạo ra nếu harness thực nghiệm hiện thực bước đó. Không mô tả route candidate L2 như quyết định cuối của request.
- [ ] Ghi trường hợp lỗi, output không hợp lệ, model không load được và giới hạn runtime. Không dùng giá trị giả để che lỗi hoặc thiếu checkpoint.
- [ ] Tạo hướng dẫn chạy lại demo và báo cáo trạng thái thực tế: PASS, FAIL hoặc BLOCKED kèm bằng chứng.

### C. Phạm vi kết luận

- [ ] Chỉ báo cáo số liệu có thể tính lại từ prediction/output thô và nêu rõ tập, split, nhãn, seed, denominator.
- [ ] Tách demo hoạt động (functional evidence) khỏi hiệu năng phân loại, lợi ích routing, latency và KPI của dự án.
- [ ] Dẫn chiếu task thực nghiệm hiện có thay vì tạo bản benchmark thứ hai hoặc sao chép bảng metric không có nguồn.

## 3. Scope compliance checklist

| Mã | Điều kiện hoàn tất | Trạng thái khi giao task |
|---|---|---|
| R2-01 | Báo cáo phân biệt Literature Fact / Local Empirical Fact / PI-Guard Proposal | Chưa thực hiện |
| R2-02 | Có lệnh và bằng chứng inference thật cho L2, L3 và handoff | Chưa thực hiện |
| R2-03 | Output JSON un-mocked, provenance/hash và denominator truy được | Chưa thực hiện |
| R2-04 | Threshold chỉ chọn trên validation; test giữ độc lập | Chưa thực hiện |
| R2-05 | Không tuyên bố KPI, multi-seed, production hoặc cascade ngoài phạm vi | Bắt buộc |
| R2-06 | Không dùng công nghệ deprecate hoặc artifact đã thu hồi | Bắt buộc |

**Tiêu chí hoàn tất:** có báo cáo nghiên cứu, hướng dẫn demo tái lập, raw output un-mocked và checklist hoàn tất; nếu model/checkpoint hoặc protocol không chạy được, báo cáo phải lưu lỗi và đánh dấu BLOCKED thay vì thay bằng mock.
