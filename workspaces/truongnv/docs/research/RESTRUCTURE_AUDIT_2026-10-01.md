# Audit và tái cấu trúc `docs/research` — 2026-10-01

## Tuyên bố ranh giới nhiệm vụ

- **Nguồn yêu cầu:** chỉ đạo trực tiếp của người dùng trong cuộc hội thoại này.
- **IN-SCOPE:** ghi lại hướng nghiên cứu DeBERTa-v3; kiểm tra các tệp hiện có trong `workspaces/truongnv/docs/research`; chỉnh mục lục; loại demo TF-IDF không paper-matched đã được nêu; lưu demo DeBERTa giả lập ra khỏi khu vực hoạt động.
- **OUT-OF-SCOPE:** khôi phục thư mục nghiên cứu cũ đã bị xóa trước task; thay đổi báo cáo kết quả trong `reports/` hoặc dữ liệu/replication; huấn luyện hay báo cáo metric PI-Guard; triển khai nội dung Chương 3/4.
- **Ranh giới milestone:** Chương 2 chỉ lưu khảo sát, ma trận lựa chọn và đề xuất. Repo chưa có mô hình PI-Guard ba nhãn do nhóm fine-tune tại chỗ; mọi câu hỏi nghiên cứu dưới đây vẫn là đề xuất.

## Tóm tắt phát hiện

Trước khi tái cấu trúc, `docs/research` có một README, ba dossier đang dùng, ba tệp archive dạng thông báo thu hồi và hai script demo. Các thư mục chuyên đề cũ không có trong worktree tại thời điểm kiểm tra; trạng thái Git cho thấy chúng đã bị xóa trước task này, nên audit không khôi phục chúng. Worktree cũng có nhiều thay đổi sẵn có; chỉ những đường dẫn nằm trong phạm vi nêu trên được cập nhật.

| Đường dẫn / loại nội dung | Phát hiện | Quyết định |
|---|---|---|
| `dossiers/03_SOTA_SURVEY_AND_6BASELINES.md` | Tách đúng hai kết quả cục bộ được giữ lại khỏi các bảng cross-paper đã rút; ghi rõ mô hình nhóm/cascade chưa được train/evaluate. | **Giữ** làm ghi chú trạng thái bằng chứng baseline; không đưa metric đã rút trở lại. |
| `dossiers/04_DATA_ENGINEERING_PROVENANCE.md` | Ghi rõ ranh giới dữ liệu, provenance và các bundle bị rút; trỏ tới audit chuẩn. | **Giữ** làm ghi chú provenance hiện hành. |
| `dossiers/04_DEBERTA_MODEL_SELECTION_MATRIX.md` | Phân biệt base đề xuất, paper PIGuard và các model card ProtectAI/DeepSet/InjectionSentry; ghi nhãn/protocol không đồng nhất và không xếp hạng metric chéo nguồn. | **Giữ và cập nhật** bằng câu hỏi nghiên cứu, quy tắc nhãn, giao thức so sánh và chỉ số dự kiến; tất cả được đánh dấu là đề xuất chưa có kết quả. |
| `archive/01_MATHEMATICAL_FOUNDATIONS.md`, `archive/02_THREAT_MODEL_AND_8KEYS.md`, `archive/05_ARCHITECTURAL_DEPRECATIONS.md` | Là các tombstone: nói rõ bản nháp trước đã rút, không khẳng định mọi câu cũ đều sai, và chỉ dẫn tới nguồn trạng thái hiện hành. | **Giữ trong archive**; không phục hồi thành nội dung lý thuyết hoạt động nếu chưa kiểm chứng từng luận điểm. |
| `demos/demo_tfidf_syntactic_baseline.py` | Script tự fit `char_wb` TF-IDF + Logistic Regression trên 12 câu viết sẵn (6 benign, 6 attack), rồi in kết quả cho 4 câu thử; thời gian một lượt được đặt tên “inference latency benchmark”. Script không chỉ ra nguồn dữ liệu, split độc lập, paper/protocol được tái lập hay phép đo lặp. | **Đã xóa theo yêu cầu cụ thể.** Lý do là đầu ra của script không phải bằng chứng baseline có thể kiểm chứng, không phải vì phương pháp TF-IDF không có tài liệu. Baseline TF-IDF paper-matched còn được ghi tại [PIDS-Bench report](../../replications/PIDS_Bench_Shire_IEEEAccess2026/REPORT.md). SHA-256 của tệp trước khi xóa: `D7DB019F20D87A816F9D31816708A295A5BF40DF0FE34C645E873F00108836A2`. |
| `demos/demo_deberta_v3_classifier.py` | Script tạo embedding/position/weight ngẫu nhiên với NumPy để minh họa phép tính; không nạp hoặc chạy checkpoint DeBERTa. Phần sau giả lập lượng tử hóa INT8 trên ma trận ngẫu nhiên, không phải đo trên mô hình. | **Đã chuyển** thành [`archive/demo_deberta_v3_random_simulation.py`](./archive/demo_deberta_v3_random_simulation.py); README ghi rõ không dùng làm bằng chứng/benchmark. Cách này bảo toàn tệp nhưng đưa nó khỏi luồng nghiên cứu đang dùng; INT8 cũng không phù hợp phạm vi kiến trúc hiện hành. |
| `README.md` | README cũ còn nhắc đến demo và đường dẫn dossier không tồn tại. | **Viết lại thành mục lục ngắn** trỏ tới ba dossier còn hiệu lực, audit này và archive; không quảng bá demo như thực nghiệm. |

## Hướng nghiên cứu được ghi lại trong ma trận

**Đề xuất câu hỏi:** trên một bộ test cùng giao thức, có tách nguồn/nhóm prompt khỏi train, mô hình fine-tune từ `microsoft/deberta-v3-base` có phân biệt hữu ích giữa benign, Prompt Injection và jailbreak hay không, kể cả các trường hợp nhãn có thể giao nhau?

Trước khi train, nhóm cần công bố quy tắc nhãn loại trừ nhau, phân loại phân cấp hoặc đa nhãn; sau đó khóa provenance, khử trùng lặp theo nguồn/nhóm và đánh giá trên split độc lập. So sánh tối thiểu gồm baseline TF-IDF paper-matched và DeBERTa-v3-base do nhóm fine-tune; checkpoint nhị phân công khai chỉ là đối chứng nhị phân nếu ánh xạ được. Báo cáo sau này cần có macro-F1, precision/recall từng lớp, false-positive rate trên benign và confusion matrix; CPU P95 chỉ được báo cáo sau phép đo có cấu hình phần cứng/phần mềm. Các metric nêu trên là kế hoạch, không phải kết quả hiện tại. Chi tiết và neo tài liệu nằm trong [ma trận DeBERTa-v3](./dossiers/04_DEBERTA_MODEL_SELECTION_MATRIX.md).

Fine-tuning một backbone có sẵn chưa đủ làm đóng góp nghiên cứu. Đóng góp tiềm năng cần nằm ở quy tắc nhãn được biện minh, tập dữ liệu có provenance và phép so sánh/kiểm thử ngoài nguồn có thể tái lập. Đây là định vị nghiên cứu đề xuất, chưa phải kết luận về tính mới hoặc mức hiệu quả.

## Bố cục duy trì

1. `README.md` là chỉ mục, không chứa số liệu benchmark.
2. Dossier 03 là nguồn trạng thái baseline cục bộ; dossier 04 dữ liệu là nguồn trạng thái provenance; ma trận DeBERTa là nguồn đề xuất chọn mô hình.
3. `archive/` chỉ lưu thông báo thu hồi và tài liệu mô phỏng không còn hoạt động.
4. Kết quả thực nghiệm chỉ đặt tại report tương ứng trong `replications/` hoặc `reports/`, có provenance và giao thức riêng; không chép lại rồi biến thành y văn trong dossier.

## Kiểm tra và giới hạn

- CodeGraph báo không có tệp mã nào phụ thuộc vào demo TF-IDF; tìm kiếm văn bản chỉ tìm thấy liên kết cũ trong README, đã cập nhật.
- Kiểm tra link phát hiện đường dẫn cũ tới Review 2 report không còn tồn tại trong cả ba tombstone; đã thay bằng liên kết tới [withdrawn-artifact register](../../reports/tasks_for_meeting_6/WITHDRAWN_DATA_ARTIFACTS.md). Đường dẫn manifest checkpoint trong ma trận được sửa sang [manifest hiện có](../../replications/02_DeBERTa_v3_Semantic_Classifier/upstream/model_sources.lock.json).
- Các chỉnh sửa giữ trong `workspaces/truongnv/docs/research`; không khôi phục hoặc sửa những xóa/sửa có sẵn ngoài phạm vi.
- Audit này kiểm kê cấu trúc và nội dung hiện hành của các tệp trong thư mục; nó không phải xác nhận độc lập tất cả nguồn dữ liệu/checkpoint, không thay thế [workspace provenance audit](../../reports/experiment_reports/WORKSPACE_PROVENANCE_AUDIT_2026-09-30.md), và không báo cáo kết quả huấn luyện.

## Checklist tuân thủ phạm vi

- [x] Chỉ cập nhật mục lục, ma trận, tombstone và audit nằm trong `docs/research`; không sửa báo cáo thực nghiệm hoặc dữ liệu ngoài thư mục.
- [x] Không fine-tune mô hình, không thêm metric PI-Guard, không biến đề xuất thành kết quả.
- [x] Không khôi phục các artifact cross-paper đã rút; demo DeBERTa có INT8 chỉ được giữ trong archive và được đánh dấu không sử dụng.
- [x] Dẫn chứng DeBERTa-v3/PIGuard trong ma trận đã qua `audit_claim_evidence.py`; các URL mô hình/paper đã được kiểm tra bằng `verify_resource_url.py`.
