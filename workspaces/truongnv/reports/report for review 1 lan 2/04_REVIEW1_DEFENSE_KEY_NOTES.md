# 04 — Luận điểm ngắn cho buổi Review 1 lần 2

## Scope Boundary Declaration

- **Nguồn nhiệm vụ:** [TASK.md](TASK.md), Review 1 lần 2, 2026-10-01.
- **IN-SCOPE:** câu trả lời về baseline TF-IDF, chia tầng, ngưỡng, DeBERTa-base và bốn detector đối chuẩn.
- **OUT-OF-SCOPE:** tuyên bố cascade có metric/latency tốt hơn; khẳng định threshold đã chốt; trình bày model card/paper numbers thành kết quả thực nghiệm PI-Guard.

## Cách trình bày mô hình

> “PI-Guard đề xuất L2 dùng TF-IDF + Logistic Regression để sàng lọc từng chunk thành ba route: ALLOW candidate, REVIEW→L3, hoặc BLOCK candidate. REVIEW chỉ là lệnh chuyển chunk sang L3, không giữ prompt chờ người xử lý. DeBERTa-v3-base phân loại chunk REVIEW; API tổng hợp kết quả cuối thành ALLOW hoặc BLOCK. Chỉ ALLOW gọi LLM.”

Câu tiếp theo phải nêu giới hạn:

> “Bài Akinrele–Gowda dùng TF-IDF + Logistic Regression và có thử selective routing theo điểm ngữ nghĩa, nhưng không kiểm nghiệm trực tiếp TF-IDF→DeBERTa của PI-Guard. Kết quả routing thay đổi theo regime nên ngưỡng của PI-Guard vẫn phải được chọn/đánh giá trên validation.” [[1]](#ref1)

## Câu hỏi có thể gặp

### Có paper nào dùng TF-IDF + Logistic Regression không?

Có. Akinrele và Gowda ghi sparse lexical baseline là TF-IDF + Logistic Regression. “TF-IDF only” là ablation chỉ dùng đặc trưng TF-IDF thay vì thêm flags/IBVS; nó vẫn có estimator. Đây là căn cứ cho baseline L2, không phải kết quả cascade của PI-Guard. [[1]](#ref1)

### Nếu bài không chứng minh TF-IDF→DeBERTa, tại sao vẫn vẽ ba vùng ngưỡng?

Ba vùng là cấu trúc giả thuyết để đánh giá: score thấp có thể bỏ qua L3; score giữa cần ngữ cảnh của L3; score cao có thể được API chặn nếu validation chứng minh đủ an toàn. Paper chỉ cung cấp mẫu tham khảo selective routing trên score ngữ nghĩa và threshold validation; nó không xác nhận ngưỡng cho TF-IDF. Không dùng số paper để gán `τ_allow`/`τ_block`. Nếu chưa hiệu chỉnh, tắt nhánh shortcut và chạy tất cả chunk qua L3 trong chế độ đo. [[1]](#ref1)

### Có phải huấn luyện một mô hình riêng để học ngưỡng?

Không. TF-IDF và Logistic Regression được fit trên train; ở inference, `predict_proba` tạo `p_attack` cho từng chunk. `τ_allow` và `τ_block` là hai cutoff hậu xử lý trên score đó, được chọn theo tiêu chí bảo mật trên validation rồi đóng băng trước test. Nếu calibration kém, cần hiệu chuẩn score bằng dữ liệu tách riêng; không đưa test vào chọn threshold. Không có cặp ngưỡng đạt yêu cầu thì tắt shortcut, không tự đặt `0.5`. [[6]](#ref6) [[7]](#ref7)

### REVIEW có phải trạng thái giữ prompt không?

Không. REVIEW chỉ là route state vùng giữa ở L2: API chuyển chunk đó sang L3 để phân loại ngữ cảnh. L3 trả score/nhãn; API áp dụng rule đã validation và phát kết quả cuối ALLOW hoặc BLOCK. Không có trạng thái pending, HOLD hoặc xử lý thủ công. Lỗi kỹ thuật trả lỗi fail-closed riêng, không đổi thành benign.

### Meta Prompt Guard có phải model base của đồ án?

Không. Base đồ án được chốt là `microsoft/deberta-v3-base`, một pretrained backbone tổng quát cần thêm classification head và fine-tune theo dữ liệu đồ án. Meta Prompt Guard là một detector đã fine-tune từ mDeBERTa-v3-base, dùng làm baseline đối chuẩn nếu truy cập và điều khoản phù hợp. [[2]](#ref2) [[3]](#ref3)

### Bốn mô hình nào có thể thử so sánh sau này?

Meta Prompt Guard 86M, PIGuard, PromptShield DeBERTa và Llama Prompt Guard 2 86M là bốn ứng viên có model/checkpoint khác vai trò/nhãn. PIGuard, PromptShield và Prompt Guard 2 86M chủ yếu là binary; chỉ Meta Prompt Guard 86M có taxonomy benign/injection/jailbreak gần với đầu ra 3 lớp dự kiến. Cần xây protocol label chung trước khi so. [[3]](#ref3) [[4]](#ref4)

### Cascade đã chứng minh tiết kiệm latency chưa?

Chưa. Cascade chỉ giảm khối lượng L3 khi fast-pass thật sự bỏ qua được L3 trên một phần request và kết quả bảo mật vẫn đạt tiêu chí. PI-Guard chưa có phép đo conditional routing/end-to-end; P95 là mục tiêu, không phải kết quả. [[5]](#ref5)

## Chuỗi xử lý cần chỉ trên sơ đồ

1. L1 giao `CanonicalTextEnvelope` gồm ordered chunks, `chunk_id`, view, source/page và offsets.
2. L2 gọi `vectorizer.transform(...)` → `LogisticRegression.predict_proba(...)` cho từng chunk; giữ score và route reason.
3. L2 route state: thấp → ALLOW candidate; giữa → REVIEW→L3; cao → BLOCK candidate. Khi cutoff chưa validation, mọi chunk đi theo REVIEW→L3.
4. L3 gọi tokenizer → token windows nếu vượt giới hạn → DeBERTa classifier → score-vector/label theo chunk/window.
5. API đối chiếu expected/processed IDs, tổng hợp và phát ALLOW hoặc BLOCK; REVIEW đã được giải quyết ở bước chuyển L2→L3.
6. Chỉ ALLOW gọi LLM. Dashboard stream trạng thái và token khi API/provider có cơ chế streaming; hiện trạng provider trả nguyên response dạng string nên token streaming vẫn là proposal. [[5]](#ref5)

## References

<a id="ref1"></a>**[1]** A. Akinrele and S. N. Gowda, “Prompt Injection Detection is Regime-Dependent: A Deployment-Aware Evaluation with Interpretable Structural Signals,” arXiv:2605.26999v1, 2026. [Full text](https://arxiv.org/html/2605.26999).

<a id="ref2"></a>**[2]** Microsoft, `microsoft/deberta-v3-base` model card. [Hugging Face](https://huggingface.co/microsoft/deberta-v3-base).

<a id="ref3"></a>**[3]** Meta Prompt Guard 86M model card. [Model card](https://github.com/meta-llama/PurpleLlama/blob/main/Prompt-Guard/MODEL_CARD.md).

<a id="ref4"></a>**[4]** PI-Guard workspace, “DeBERTa reference model candidates.” [05_DEBERTA_REFERENCE_MODELS.md](05_DEBERTA_REFERENCE_MODELS.md).

<a id="ref5"></a>**[5]** PI-Guard workspace, “Workspace provenance and metric audit — 2026-09-30.” [Local audit](../experiment_reports/WORKSPACE_PROVENANCE_AUDIT_2026-09-30.md).

<a id="ref6"></a>**[6]** scikit-learn, “Tuning the decision threshold for class prediction.” [User guide](https://scikit-learn.org/stable/modules/classification_threshold.html).

<a id="ref7"></a>**[7]** scikit-learn, “Probability calibration.” [User guide](https://scikit-learn.org/stable/modules/calibration.html).
