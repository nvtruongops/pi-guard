# Chuyên đề 01 — Threat model và bề mặt tấn công của PI-Guard

> **Trạng thái 30/09/2026:** đây là threat model định tính để định hướng thiết kế. Các điểm DREAD, xác suất, thiệt hại tài chính và mức độ rủi ro định lượng trong bản cũ đã bị rút vì không có rubric chấm điểm, dữ liệu sự cố hay đánh giá chuyên gia được ghi nhận. Các kịch bản dưới đây là tình huống cần xem xét, không phải sự kiện đã xảy ra hoặc tần suất đo được.

## 1. Mục tiêu và ranh giới

PI-Guard được nghiên cứu như một bộ phân loại văn bản đặt trước ứng dụng LLM. Threat model tập trung vào nội dung không tin cậy có thể được đưa vào ngữ cảnh của ứng dụng. Mục tiêu là đánh giá liệu detector có thể nhận diện một số dạng prompt injection/jailbreak theo label policy đã định nghĩa hay không.

Threat model này không giả định rằng detector có thể kiểm soát quyền truy cập dữ liệu, xác minh danh tính, bảo vệ secret lưu sai chỗ, ngăn mọi tool action, hay bảo đảm an toàn cho mô hình đích. Quyền tool và kiểm soát truy cập cần được thực thi riêng tại ứng dụng.

## 2. Tài sản cần bảo vệ

| Tài sản | Rủi ro cần xem xét | Giới hạn của PI-Guard |
|---|---|---|
| Chỉ thị hệ thống và cấu hình ứng dụng | Nội dung không tin cậy tìm cách làm lệch mục tiêu hoặc tiết lộ thông tin được đưa vào ngữ cảnh | Bộ phân loại đầu vào không thể chứng minh bí mật được lưu đúng cách hay ngăn mô hình đích tiết lộ mọi bí mật |
| Dữ liệu người dùng và dữ liệu truy xuất | Nội dung độc hại trong prompt hoặc tài liệu được truy xuất có thể ảnh hưởng cách mô hình xử lý dữ liệu | Cần kiểm soát nguồn dữ liệu, tenant boundary và quyền truy cập ngoài detector |
| Tính toàn vẹn của tác vụ và hành động công cụ | Nội dung có thể cố hướng mô hình gọi công cụ hoặc thực hiện tác vụ ngoài ý định | Policy engine, authorization và xác nhận hành động phải nằm ở ứng dụng/tool layer |
| Tính sẵn sàng và chi phí | Lưu lượng hoặc nội dung bất thường có thể làm tăng khối lượng xử lý | Không có số liệu thiệt hại hay mức tải thực tế trong audit này |

Các tác động trong bảng là khả năng cần phân tích theo từng ứng dụng, không phải mức thiệt hại đã quan sát hoặc định giá.

## 3. Nhóm tình huống tấn công

Các nhóm dưới đây phục vụ label policy của nghiên cứu; chúng có thể giao nhau và không nhất thiết là các lớp loại trừ lẫn nhau.

1. **Direct prompt injection:** người dùng trực tiếp đưa chỉ thị tìm cách ghi đè hoặc làm lệch yêu cầu của ứng dụng.
2. **Indirect prompt injection:** nội dung không tin cậy đến từ tài liệu, trang web, email hoặc kết quả tool được ứng dụng đưa vào ngữ cảnh. Việc có RAG/tool trong hệ thống đích phải được xác nhận theo ứng dụng thực tế.
3. **Jailbreak:** prompt tìm cách khiến mô hình bỏ qua hoặc né tránh chính sách an toàn của ứng dụng. Có thể trùng với direct injection; quy tắc gán nhãn phải nêu rõ cách xử lý.

Những ví dụ như obfuscation, nhập vai, delimiter hoặc yêu cầu tiết lộ chỉ là họ kỹ thuật cần đưa vào taxonomy/đánh giá khi nguồn dữ liệu và cách gán nhãn được ghi rõ. Không suy ra một detector bắt được kỹ thuật chỉ từ việc mô tả nó trong threat model.

## 4. Tác nhân và giả định

- **Người gửi prompt:** có thể kiểm soát nội dung gửi qua giao diện/API mà ứng dụng cho phép họ sử dụng. Không giả định có quyền xem trọng số hoặc system prompt.
- **Nhà cung cấp nội dung bên ngoài:** có thể kiểm soát văn bản mà ứng dụng lựa chọn truy xuất hoặc xử lý; chỉ thuộc threat surface nếu ứng dụng có pipeline tương ứng.
- **Người dùng có quyền hạn hợp lệ nhưng lạm dụng:** có thể thử dùng quyền được cấp để yêu cầu hành động không phù hợp. Detector không thay thế authorization.

Không gán xác suất thành công, số lần probing hoặc cấp độ quyền cụ thể nếu chưa có cấu hình triển khai và dữ liệu đo tương ứng.

## 5. Bề mặt xử lý cần xác nhận trong từng triển khai

- Prompt trực tiếp qua UI/API.
- Tài liệu và đoạn trích nếu ứng dụng dùng RAG hoặc ingestion.
- Lịch sử hội thoại nếu ứng dụng giữ và gửi lại context nhiều lượt.
- Kết quả tool/function nếu được đưa trở lại context.

Danh sách trên là checklist khảo sát, không phải khẳng định prototype hiện tại đã tích hợp các điểm này. Mọi tuyên bố về “quét toàn bộ luồng”, chặn trước khi LLM nhận dữ liệu hoặc ghi log cần được xác nhận bằng code path và một phép chạy thực tế.

## 6. Đánh giá rủi ro

Tài liệu này dùng phân tích kịch bản định tính, chưa gán DREAD/STRIDE score. Để dùng scoring định lượng cần công bố rubric cho từng tiêu chí, người đánh giá, căn cứ chấm, cách xử lý bất đồng và phạm vi hệ thống. Không lấy điểm tự chấm chưa có quy trình làm xác suất hay bằng chứng rủi ro.

## 7. Giới hạn bằng chứng hiện có

Public dataset và benchmark có thể hỗ trợ kiểm tra detector trên các mẫu thuộc nguồn, split và nhãn được mô tả trong từng báo cáo. Chúng không tự cho biết tỷ lệ tấn công ngoài đời, mức tổn thất doanh nghiệp, khả năng bảo vệ mọi ứng dụng hoặc khả năng chống mọi biến thể.

Kết quả hiện có và giới hạn của từng phép chạy được tổng hợp trong [workspace provenance audit](../../reports/experiment_reports/WORKSPACE_PROVENANCE_AUDIT_2026-09-30.md), [PIDS-Bench same-paper TF-IDF report](../../replications/PIDS_Bench_Shire_IEEEAccess2026/REPORT.md) và [PIGuard own-release report](../../replications/02_DeBERTa_v3_Semantic_Classifier/reports/review1_paper_model_public_rerun_2026-09-30/REPORT.md). Review 2 và ma trận sáu classifier đã rút khỏi bằng chứng hiện hành. Định nghĩa thuật ngữ/taxonomy phải được thống nhất với [sổ nguồn cấp dự án](../../../../Final-Report/References/REFERENCES_LOG.md) trước khi đưa vào báo cáo chính thức.

## Scope Boundary Declaration

- **IN-SCOPE:** tài sản, actor, bề mặt xử lý và kịch bản prompt injection/jailbreak cần đánh giá cho một guardrail văn bản.
- **OUT-OF-SCOPE:** xác suất tấn công, điểm DREAD, thiệt hại tài chính, tuyên bố detector chặn hoàn toàn, xác nhận API/RAG/tool flow chưa kiểm tra và đánh giá pháp lý.
