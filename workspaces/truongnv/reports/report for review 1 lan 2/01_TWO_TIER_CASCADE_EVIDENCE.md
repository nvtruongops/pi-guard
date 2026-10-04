# 01 — Căn cứ cho TF-IDF và routing theo ngưỡng

## Scope Boundary Declaration

- **Nguồn nhiệm vụ:** [TASK.md](TASK.md), Review 1 lần 2, 2026-10-01.
- **IN-SCOPE:** xác định bài 2605.26999 hỗ trợ gì cho TF-IDF + Logistic Regression, threshold và selective routing; chuyển phần phù hợp thành giả thuyết có ranh giới cho kiến trúc.
- **OUT-OF-SCOPE:** nhận kết quả paper làm kết quả PI-Guard; đặt ngưỡng số; khẳng định cascade đã giảm latency/tăng recall; huấn luyện hay triển khai detector.

## Kết luận ngắn

Có bài paper trong phạm vi tham khảo cho tầng lexical: Akinrele và Gowda dùng **TF-IDF + Logistic Regression** làm sparse lexical baseline và fine-tune DeBERTa-base để so sánh trong nhiều regime. Paper còn khảo sát routing ba vùng dựa trên điểm của detector ngữ nghĩa. Đây là nguồn phù hợp để biện minh rằng TF-IDF là một baseline có thể đánh giá và selective routing là hướng thử nghiệm; paper **không** đánh giá chính xác kiến trúc `TF-IDF → threshold → DeBERTa` của PI-Guard. [[1]](#ref1)

## Threshold: điều gì có thể và không thể kế thừa

1. Paper chọn ngưỡng theo validation-only protocol rồi giữ cố định khi đánh giá test/OOD. Đây là quy trình tham khảo cho thiết kế thử nghiệm, không phải giá trị ngưỡng dùng lại cho dữ liệu PI-Guard. [[1]](#ref1)
2. Paper mô tả semantic-centred routing thành confident-benign, uncertain và confident-harmful; các mẫu uncertain mới qua fallback expert/shallow fusion. Score bộ định tuyến là score của semantic model, không phải TF-IDF score. [[1]](#ref1)
3. Hiệu quả không ổn định qua các regime. Chẳng hạn, ở Primary OOD, biến thể semantic expert gate có Macro-F1 0.7157 và TPR@1% FPR 0.0000, trong khi BGE + Logistic Regression đạt Macro-F1 0.7168 và TPR@1% FPR 0.1866. Đây là metric tác giả báo cáo cho benchmark của họ, không phải số liệu PI-Guard; kết quả không ủng hộ việc tuyên bố mọi cách chia vùng đều cải thiện detector. [[1]](#ref1)
4. Paper có kết quả TF-IDF tốt ở một hard-negative regime nhưng không thống trị các regime khác; do đó không thể suy ra vùng score hoặc ngưỡng fast-pass/block áp dụng chung. [[1]](#ref1)

**Quyết định cho sơ đồ:** vẽ `τ_allow` / vùng uncertain / `τ_block` như **nhánh proposal để kiểm định**. Không ghi `0.25`, `0.5`, `0.85` hay một khoảng paper lên đồ án. Trong giai đoạn dựng mô hình, ngưỡng được chọn trên validation theo mục tiêu FPR/TPR, kiểm tra độ hiệu chuẩn và đánh giá lại theo từng regime. Nếu chưa có threshold đủ bằng chứng, tắt fast-pass và direct-block; chuyển toàn bộ chunk sang L3 để đánh giá. [[1]](#ref1)

Với L2 Logistic Regression, score định tuyến có thể là `p_attack = predict_proba(TFIDF(chunk))[attack]`. Fit TF-IDF vocabulary/IDF và trọng số classifier bằng tập train; hai ngưỡng là cutoff hậu huấn luyện được chọn trên validation, không phải một tầng classifier mới. `τ_allow` cần kiểm soát rủi ro attack nằm trong vùng bypass; `τ_block` cần kiểm soát benign bị đưa vào vùng block. Đánh giá cặp ngưỡng trên validation, freeze trước test; nếu calibration của probability yếu thì hiệu chuẩn bằng dữ liệu/cross-validation tách khỏi test. [[3]](#ref3) [[4]](#ref4)

## L2/L3/API — trách nhiệm đề xuất

| Thành phần | Việc làm | Đầu ra |
|---|---|---|
| L1 ingress | Parse text/upload, chuẩn hóa UTF-8, tạo ordered chunks, lưu page/offset/source refs và expected count. | `CanonicalTextEnvelope` |
| L2 lexical screen | `TfidfVectorizer.transform(chunk.text_utf8)` → sparse features → Logistic Regression score cho từng chunk. Phân lớp sơ bộ `benign` / `suspect`; không quyết định cuối request. | `chunk_id`, score, route candidate, model version |
| L2 route states | ALLOW candidate: fast path sau validation; REVIEW: chỉ chuyển chunk vùng giữa sang L3; BLOCK candidate: chặn sớm sau validation. | chunk result + route state |
| L3 contextual classifier | Tokenize chunk/window mang trạng thái REVIEW; chạy project DeBERTa-v3-base classifier; trả score-vector và nhãn theo chunk/window. | `chunk_id`, `window_id`, class scores/label |
| API request aggregator | So expected-vs-processed IDs; dùng rule đã validation để tổng hợp toàn request thành ALLOW hoặc BLOCK. REVIEW không phải đầu ra cuối; thiếu coverage/lỗi kỹ thuật trả fail-closed riêng. | ALLOW / BLOCK hoặc lỗi kỹ thuật |
| Target LLM/dashboard | Chỉ API ALLOW gọi LLM; BLOCK trả kết quả từ chối; dashboard nhận trạng thái và token stream sau khi provider/API hỗ trợ. | response stream / block result / error |

## Tool-call contract cần thể hiện trên sơ đồ

- L2 đề xuất: `vectorizer.transform(texts)`; `linear_classifier.predict_proba(X)`; `route_chunk(score, tau_allow, tau_block)`; `aggregate_chunk_routes(expected_ids, results)`.
- L3 đề xuất: `tokenizer(chunk_text, ...)`; `sequence_classifier(**token_batch)`; trả `logits`/scores cùng `chunk_id` và `window_id`.
- L1/L2/L3 đều có error exit với `stage` và `error_code`; không biến lỗi, text rỗng hoặc thiếu coverage thành benign.
- Đây là tên giao diện minh họa để đọc kiến trúc, không phải hàm đã có trong backend.
- REVIEW chỉ là route state của L2 để API chuyển chunk sang L3. L3 xử lý rồi API tổng hợp thành ALLOW/BLOCK; không có pending, HOLD hay luồng duyệt thủ công. Lỗi hệ thống được trả dưới dạng lỗi kỹ thuật fail-closed, không phải route REVIEW.

## Điều kiện để gọi đây là cascade có lợi

Đánh giá trên cùng dataset/splits: L2 riêng; L3 riêng; cascade có route; và đối chứng chạy L3 cho mọi prompt. Chọn threshold trên validation, freeze trước test, đo benign FPR, attack recall/TPR tại operating point, macro-F1 theo regime, tỷ lệ mỗi nhánh và latency end-to-end. Cần chứng minh L3 sửa được một phần lỗi do L2 để bù chi phí phân tầng. Không có phép đo đủ điều kiện nào hiện xác nhận điều này cho PI-Guard. [[2]](#ref2)

## References

<a id="ref1"></a>**[1]** A. Akinrele and S. N. Gowda, “Prompt Injection Detection is Regime-Dependent: A Deployment-Aware Evaluation with Interpretable Structural Signals,” arXiv:2605.26999v1, 2026. [Full text](https://arxiv.org/html/2605.26999).

<a id="ref2"></a>**[2]** PI-Guard workspace, “Workspace provenance and metric audit — 2026-09-30.” [Local audit](../experiment_reports/WORKSPACE_PROVENANCE_AUDIT_2026-09-30.md).

<a id="ref3"></a>**[3]** scikit-learn, “Tuning the decision threshold for class prediction.” [User guide](https://scikit-learn.org/stable/modules/classification_threshold.html).

<a id="ref4"></a>**[4]** scikit-learn, “Probability calibration.” [User guide](https://scikit-learn.org/stable/modules/calibration.html).
