# Chunking, n-gram và backend handoff — thiết kế đề xuất

**Ngày:** 2026-10-01  
**Trạng thái:** đặc tả kiến trúc; chưa triển khai, huấn luyện hoặc đo hiệu năng.

## Scope Boundary Declaration

- **IN-SCOPE:** giải thích cách L1 trích xuất/chia chunk; L2 áp dụng word/character TF-IDF và Logistic Regression; L3 nhận phần chunk được route; mô tả object truyền giữa module trong FastAPI.
- **OUT-OF-SCOPE:** thay đổi backend, thêm dependency, chọn ngưỡng số đã được xác nhận, khẳng định lợi ích latency/accuracy, hoặc nói cascade đã được triển khai. Không đưa INT8, ONNX Runtime, ZeroQuant, white-box steering, truy cập KV-cache hay mô hình đa phương thức vào phương án.

## Đơn vị dữ liệu: chunk khác n-gram

`ChunkRecord` là một đoạn văn bản có ID/provenance do L1 tạo. `ngram_range` là độ dài feature được trích trong **mỗi** chunk ở L2: word `(1,2)` gồm unigram và bigram; char `char_wb (3,5)` gồm character n-gram dài 3–5 ký tự trong ranh giới từ. Vì vậy “3–5” không có nghĩa một chunk chỉ có 3–5 n-gram, và không đặt giới hạn độ dài chunk. Scikit-learn định nghĩa hai tham số này tách biệt. [TfidfVectorizer docs](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html)

## Cấu hình chunk khởi đầu để kiểm định

| Tham số | Đề xuất khởi đầu | Cách diễn giải / trạng thái |
|---|---:|---|
| Mục tiêu mỗi chunk | 256 DeBERTa tokenizer tokens | Ứng viên kỹ thuật để bắt đầu thử nghiệm, không phải giá trị được paper khuyến nghị. Ưu tiên ngắt tại ranh giới đoạn/trang gần giới hạn. |
| Overlap | 32 tokens | Ứng viên giúp giữ một phần ngữ cảnh qua ranh giới; overlap làm trùng lặp dữ liệu nên mọi chunk phải giữ source offsets/ID. |
| Validation sweep | target `{128, 256, 384}` × overlap `{0, 32, 64}` | Chọn trên validation theo chất lượng phân loại, coverage và chi phí; đóng băng trước test. Đây là kế hoạch thử nghiệm của dự án, không phải kết quả paper. |
| Giới hạn cửa sổ DeBERTa | 512 model positions | `microsoft/deberta-v3-base` model config công bố `max_position_embeddings=512`; tính cả special tokens khi kiểm tra input. [Model config](https://huggingface.co/microsoft/deberta-v3-base/resolve/main/config.json) |
| Giới hạn file/đầu ra trích xuất | `MAX_UPLOAD_BYTES`, `MAX_EXTRACTED_TOKENS` cấu hình | Chưa gán số vì phụ thuộc môi trường; vượt giới hạn trả lỗi rõ ràng/413, không hạ thành benign. |

Dùng tokenizer tương ứng với backbone để đếm token, không quy đổi token từ số ký tự. Ưu tiên tách theo trang/đoạn; nếu một đoạn vẫn dài hơn mục tiêu thì tách tiếp ở ranh giới câu/token. L1 không chạy DeBERTa; tokenizer chỉ dùng để đếm/cắt đoạn. L3 kiểm tra lại input sau khi thêm special tokens. Không được cắt cụt im lặng: nếu input vượt giới hạn model, chia thành cửa sổ có `window_id` và offset; mỗi cửa sổ phải được tính đủ trong coverage. Cấu hình 256/32 và validation grid trên là **đề xuất cần đo**, không phải ngưỡng cascade.

Khi chuẩn bị dữ liệu, chia train/validation/test theo prompt/file gốc trước khi tạo chunk. Không để các chunk overlap từ cùng một request xuất hiện ở nhiều split. Fit vocabulary/IDF và classifier chỉ trên train; chọn feature config và cutoff trên validation; test giữ nguyên cho đánh giá cuối.

## L2 n-gram: baseline và ablation

1. **Baseline bám bài tham khảo:** word TF-IDF với unigram + bigram (`ngram_range=(1,2)`), vocabulary tối đa 20.000 terms, sau đó Logistic Regression. Paper 2605.26999 mô tả cấu hình lexical này. [Paper, §3.3.1](https://arxiv.org/html/2605.26999)
2. **Ablation tùy chọn của PI-Guard:** thêm kênh `char_wb` với `(3,5)` để kiểm tra biến thể ký tự/obfuscation. Đây không phải cấu hình của paper và không được mặc định là tốt hơn. Chọn cap/weight của kênh trên validation.
3. L1 tạo chunk; mỗi chunk/view là một scoring unit. L2 gọi các vectorizer đã fit theo batch để tạo sparse feature rows, ghép các kênh sparse, rồi `LogisticRegression.predict_proba(X)` phát score `p_attack` theo ID. Batch size là cấu hình bộ nhớ/runtime cần profiling; batch chỉ nhóm công việc, không đổi đơn vị chấm hay thứ tự ID. TF-IDF vectorizer và classifier được fit ngoài request; request chỉ gọi `transform`/`predict_proba`.
4. Hai cutoff routing (nếu dùng) chọn trên validation, đóng băng trước test. Khi chưa validation, tắt low/high shortcut và cho toàn bộ chunk qua L3 theo chế độ đo. Paper dùng threshold/routing trên score của các mô hình/ngữ nghĩa thuộc thí nghiệm của họ; paper không xác nhận cặp cutoff cho cascade TF-IDF → DeBERTa của PI-Guard.

## Backend handoff giữa các tầng

Ba tầng là các module trong cùng ứng dụng FastAPI, không phải ba dịch vụ độc lập. API route/orchestrator gọi function và truyền DTO/Pydantic object trong bộ nhớ; không có REST nội bộ hoặc message queue trong proposal. File bytes chỉ đi vào L1.

| Handoff | Payload nội bộ | Hành vi |
|---|---|---|
| Request → L1 | `PromptRequest` hoặc `UploadBytes` | Validate loại/kích thước/signature; gọi parser theo loại file. `.py` chỉ đọc như text, không import/execute. |
| L1 → L2 | `CanonicalTextEnvelope(request_id, chunks[], coverage_status, config_version)`; mỗi chunk có `chunk_id`, `view_id`, `text_utf8`, `token_count`, `source_refs`, page/section và offsets | Không truyền byte/file gốc. L2 dùng text theo batch nhưng trả đúng một `ChunkRouteResult` cho từng ID/view. |
| L2 → API | `ChunkRouteResult(request_id, chunk_id, view_id, score_vector, p_attack, route, model_version, source_refs)` | API giữ kết quả low/high. Đây là candidate theo chunk, chưa tự kết luận toàn request ALLOW. |
| API orchestrator → L3 | `RoutedChunk[]` chỉ gồm band giữa: text + IDs/provenance + L2 score | Dùng lời gọi module cùng process; không gửi sparse matrix TF-IDF sang L3. Nếu cutoff chưa kiểm định, gửi mọi chunk đến L3. |
| L3 → API | `WindowPrediction[]` gồm chunk/window IDs, class scores, nhãn dự đoán, model version và source refs | API join kết quả với danh sách chunk/window kỳ vọng, kiểm tra coverage và tổng hợp request. |
| API → provider/dashboard | Chỉ kết quả request ALLOW gọi target LLM; BLOCK trả kết quả từ chối; dashboard nhận quyết định và response stream | REVIEW là route nội bộ L2→L3, không phải pending/HOLD. API lỗi/thiếu coverage trả lỗi fail-closed, không thành ALLOW. Streaming thật vẫn là đề xuất vì provider hiện trả chuỗi hoàn chỉnh. |

Lỗi được biểu diễn như `StageError(stage, request_id, error_code)`. L1/L2/L3 fail, output rỗng/không hợp lệ hoặc thiếu ID đều dừng request; không dùng default benign. REVIEW chỉ là L2 route state yêu cầu API chuyển chunk sang L3; không tạo pending/HOLD ở caller/dashboard.

## Tool calls thể hiện trong sơ đồ

- **L1:** `document_text_extractor.extract(...)`; text `.txt/.md/.py` đọc UTF-8 strict; JSON qua Python `json`; PDF text đề xuất PyMuPDF (`fitz`); DOCX đề xuất `python-docx`; OCR trang scan là nhánh tùy chọn qua Tesseract. Adapter lỗi thì trả lỗi có stage/code.
- **L2 offline:** `TfidfVectorizer.fit(train_chunks)` → classifier `.fit(X_train, y_train)`; chỉ fit trên train.
- **L2 request:** `.transform(batch_texts)` → sparse matrix (có thể ghép hai kênh) → `.predict_proba(X)` → `route_chunk(...)` → `ChunkRouteResult[]`.
- **L3:** DeBERTa tokenizer → window builder nếu cần → `model.eval()` + `torch.inference_mode()` → logits/softmax → `WindowPrediction[]`.
- **API:** router gọi L1/L2/L3; coverage/aggregation/policy; chỉ-ALLOW gọi provider; event/token stream tới dashboard là phần cần triển khai sau.

## Nguồn và giới hạn bằng chứng

- Akinrele & Gowda, arXiv:2605.26999, §3.3.1 mô tả TF-IDF word unigram/bigram và vocabulary tối đa 20.000. Nguồn này **không** kiểm chứng `char_wb (3,5)`, 256/32 chunking hay latency của PI-Guard cascade. [Full paper](https://arxiv.org/html/2605.26999)
- Scikit-learn mô tả `analyzer` word/char/char_wb và `ngram_range` là khoảng độ dài n-gram. [API docs](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html)
- Model config của `microsoft/deberta-v3-base` có `max_position_embeddings=512`. [Config JSON](https://huggingface.co/microsoft/deberta-v3-base/resolve/main/config.json)
- Kích thước chunk/overlap, cap upload và cutoff của dự án phải được kiểm định trên dữ liệu PI-Guard; chưa có số hiệu năng cascade đầu-cuối trong báo cáo này.
