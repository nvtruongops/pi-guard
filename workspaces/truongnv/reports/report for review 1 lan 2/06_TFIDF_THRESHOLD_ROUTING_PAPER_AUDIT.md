# 06 — Kiểm tra ngưỡng TF-IDF và selective routing trong arXiv 2605.26999

**Ngày:** 2026-10-01  
**Trạng thái:** Phân tích tài liệu; chưa huấn luyện hoặc đo cascade PI-Guard.

## Scope Boundary Declaration

- **IN-SCOPE:** xác định bài arXiv 2605.26999 thực sự làm gì với TF-IDF + Logistic Regression, threshold và selective routing; đề xuất cách dùng phương pháp đó để chọn hai cutoff cho tầng L2 của PI-Guard.
- **OUT-OF-SCOPE:** sao chép ngưỡng số của paper; khẳng định paper đã thử `TF-IDF → DeBERTa`; gán ngưỡng cụ thể cho PI-Guard; huấn luyện/triển khai mô hình; báo cáo hiệu năng hoặc độ trễ chưa đo; đưa INT8, ONNX Runtime, ZeroQuant, white-box steering, KV-cache hay mô hình đa phương thức vào phương án.

## Kết luận trực tiếp

**Có thể tham khảo paper để xây dựng protocol hiệu chỉnh, nhưng không thể lấy nguyên cutoff hay tuyên bố paper chứng minh cascade TF-IDF → DeBERTa.** Bài dùng TF-IDF với Logistic Regression như mô hình lexical riêng và chọn một ngưỡng nhị phân hậu huấn luyện cho từng mô hình bằng score trên validation, tối đa hóa validation Macro-F1; ngưỡng đó được giữ cố định trước test/OOD. [[1]](#ref1)

Paper cũng mô tả ba vùng `confident benign / uncertain / confident harmful`, nhưng score được chia vùng là score của **semantic model**; chỉ vùng uncertain được chuyển cho fallback expert hoặc shallow fusion. Đó không phải ba vùng của `TF-IDF + Logistic Regression`, và paper không đánh giá đúng tuyến `L2 TF-IDF → vùng giữa sang DeBERTa-v3 của PI-Guard`. [[1]](#ref1)

Trong toàn văn arXiv v1, phần selective routing mô tả ý nghĩa ba vùng nhưng không công bố cặp cutoff số có thể chuyển sang PI-Guard. Các mức `FPR = 1%, 5%, 10%` của paper là các operating point dùng để đọc TPR trên ROC, không phải `τ_allow`, `τ_block` hoặc ranh giới score cho ba vùng. [[1]](#ref1)

## Paper đã kiểm nghiệm gì?

| Thành phần trong paper | Score/model liên quan | Cách chọn hoặc sử dụng ngưỡng | Có thể dùng cho PI-Guard? |
|---|---|---|---|
| TF-IDF + Logistic Regression | Score của lexical classifier | Một cutoff nhị phân được quét trên validation để tối đa hóa Macro-F1, rồi cố định trước đánh giá held-out. | **Có:** tham khảo quy trình validation-only, khóa cutoff trước test. **Không:** lấy cutoff paper làm ngưỡng L2. [[1]](#ref1) |
| Selective routing ba vùng | Score của semantic model | Chia confident-benign / uncertain / confident-harmful; chỉ vùng uncertain qua fallback expert hoặc shallow fusion. | **Có:** tham khảo khái niệm selective prediction. **Không:** xem đây là bằng chứng cho ba vùng trên score TF-IDF hoặc cho TF-IDF→DeBERTa. [[1]](#ref1) |
| TPR tại FPR 1%, 5%, 10% | ROC của từng detector | Báo cáo TPR tại các mức FPR định trước; đây là cách so operating point, không phải các cutoff xác suất được báo cáo. | **Có:** tham khảo cách báo cáo hành vi ở mức FPR thấp. **Không:** đổi 1/5/10% thành `τ` hay route band. [[1]](#ref1) |

### Quy mô dữ liệu paper — chỉ để hiểu phạm vi

Paper báo cáo mỗi split ID có 694 mẫu train, 149 validation (108 adversarial, 41 benign) và 149 test; ba regime OOD được giữ cho đánh giá cuối. Những số lượng này mô tả thí nghiệm của tác giả, không phải khuyến nghị cỡ mẫu cho PI-Guard và cũng không cung cấp ngưỡng chuyển tầng cho dữ liệu đồ án. [[1]](#ref1)

Paper còn cho thấy lựa chọn detector phụ thuộc regime và operating point: ở hard-negative injection OOD, TF-IDF-only có Macro-F1 cao hơn DeBERTa-base, trong khi tại FPR 1% DeBERTa có TPR cao hơn TF-IDF. Vì vậy kết quả của một regime không đủ để suy ra L2 luôn an toàn để fast-pass hoặc direct-block ở regime khác. [[1]](#ref1)

## Cách áp dụng cho L2 của PI-Guard

### 1. Huấn luyện mô hình; không huấn luyện bộ chia ba nhánh riêng

Train một pipeline `TF-IDF → Logistic Regression` bằng dữ liệu train có nhãn `benign / attack`. `predict_proba` của scikit-learn trả probability estimate theo thứ tự lớp trong `classes_`; với từng chunk chuẩn hóa từ L1, lấy score của lớp attack: [[4]](#ref4)

```text
p_attack = LogisticRegression.predict_proba(TFIDF(chunk))[attack]
```

Hai cutoff là tham số quyết định hậu huấn luyện trên score của mô hình đã fit; chúng không tạo classifier mới và không cập nhật trọng số Logistic Regression. Scikit-learn nêu rõ decision threshold có thể được tuning sau khi classifier đã fit theo metric mục tiêu. [[2]](#ref2)

### 2. Chọn hai cutoff trên validation

Định nghĩa `τ_allow < τ_block` trên score `p_attack` của chunk:

```text
p_attack ≤ τ_allow                 → ứng viên bypass L3 (fast-pass)
τ_allow < p_attack < τ_block       → chuyển chunk sang L3
p_attack ≥ τ_block                 → ứng viên block
```

Đây là **đề xuất PI-Guard cần kiểm định**, không phải kết quả được paper xác nhận. L2 phát route-candidate theo chunk; API vẫn kiểm tra coverage và tổng hợp kết quả ở mức request trước khi quyết định. Không xem một chunk score thấp là bằng chứng tuyệt đối rằng toàn request benign.

Trên validation, quét các cặp cutoff ứng viên và ghi ít nhất:

| Chỉ số validation | Định nghĩa ở mức chunk | Ràng buộc cần xác lập trước khi xem kết quả |
|---|---|---|
| `allow_attack_escape_rate` | Tỷ lệ chunk attack rơi vào `p_attack ≤ τ_allow`. | Không vượt mức rủi ro attack lọt qua mà nhóm đã xác định trước. |
| `block_benign_rate` | Tỷ lệ chunk benign rơi vào `p_attack ≥ τ_block`. | Không vượt mức chặn nhầm benign mà nhóm đã xác định trước. |
| `direct_block_attack_recall` | Tỷ lệ chunk attack rơi vào vùng `p_attack ≥ τ_block`. | Báo cáo để cho biết vùng block trực tiếp phát hiện được bao nhiêu attack. |
| `fast_pass_coverage` | Tỷ lệ toàn bộ chunk rơi vào vùng `p_attack ≤ τ_allow`. | Tối đa hóa trong các cặp cutoff thỏa ràng buộc an toàn. |
| `l3_escalation_rate` | Tỷ lệ toàn bộ chunk nằm trong vùng giữa. | Báo cáo để định lượng lượng việc còn chuyển sang L3. |

Chọn cặp cutoff chỉ sau khi định trước các giới hạn chấp nhận được cho attack lọt qua và benign bị block nhầm; trong các cặp đáp ứng giới hạn, ưu tiên cặp giảm lượng chunk phải gọi L3. Đánh giá thêm ở mức request vì các chunk của một prompt không phải các request độc lập. Đây là tiêu chí thiết kế đề xuất của đồ án, không phải metric hay ngưỡng số do paper đưa ra.

### 3. Giữ tách biệt train, hiệu chuẩn, validation và test

- Fit TF-IDF vocabulary/IDF và Logistic Regression trên **train**.
- Nếu cần diễn giải `predict_proba` như xác suất thực tế, kiểm tra reliability/calibration; nếu hiệu chuẩn, fit calibrator bằng dữ liệu riêng hoặc dự đoán cross-validation, không dùng test. Scikit-learn lưu ý calibration đánh giá mức score xác suất phù hợp với tần suất quan sát và cung cấp quy trình calibration riêng. [[3]](#ref3)
- Chọn `(τ_allow, τ_block)` bằng **validation**; lưu lại protocol, metric, cặp cutoff và phiên bản mô hình rồi đóng băng chúng.
- Chỉ sau đó chạy **test/OOD** một lần để báo cáo kết quả. Không quay lại chọn cutoff theo test/OOD.
- Báo cáo độ bất định/độ ổn định của các tỷ lệ và ngưỡng; nếu mẫu validation quá ít hoặc cặp cutoff không thỏa ràng buộc, không bật shortcut tự động.

`predict_proba` trả score xác suất do classifier ước lượng; việc score có dạng từ 0 đến 1 không tự chứng minh rằng nó calibrated. Do đó, có thể dùng validation để chọn cutoff theo score ngay cả khi chưa chứng minh calibration, nhưng khi diễn giải score là xác suất rủi ro thì phải đánh giá calibration riêng. [[2]](#ref2) [[3]](#ref3)

### 4. Nhánh dự phòng khi không tìm được cặp cutoff phù hợp

Nếu không có cặp `(τ_allow, τ_block)` nào đạt đồng thời giới hạn rủi ro đã định trước, tắt fast-pass và direct-block shortcut trong đánh giá cascade; chuyển mọi chunk sang L3, đồng thời vẫn báo cáo L2 như baseline độc lập. Không tự nới ràng buộc sau khi nhìn test để tạo ra kết quả thuận lợi. Đây là quy tắc vận hành đề xuất cho PI-Guard.

## Trả lời câu hỏi “lấy phạm vi/ngưỡng paper rồi hiệu chuẩn sau được không?”

- **Lấy phương pháp được:** score trên validation → chọn operating point → đóng băng → đánh giá held-out; đồng thời báo cáo kết quả ở các operating point FPR phù hợp. [[1]](#ref1) [[2]](#ref2)
- **Lấy phạm vi ba vùng làm cảm hứng được:** thiết kế ba vùng để cho qua / chuyển tiếp / chặn là selective-routing hypothesis có thể thử nghiệm.
- **Không lấy giá trị số từ paper được:** paper không công bố `τ_allow`, `τ_block` cho score TF-IDF; các vùng semantic routing cũng không có cutoff số được báo cáo trong toàn văn arXiv v1. Mức FPR 1/5/10% không thay thế được các cutoff đó. [[1]](#ref1)
- **Không gọi “hiệu chuẩn sau” là chọn trên test:** cutoff phải được chọn bằng validation (và calibration, nếu cần, có dữ liệu/OOF riêng), sau đó đóng băng trước khi test.

## Mệnh đề phù hợp để bảo vệ đồ án

> “Akinrele và Gowda (2026) dùng TF-IDF + Logistic Regression như lexical baseline, chọn decision threshold bằng score validation và cố định trước đánh giá held-out; paper cũng thử selective routing ba vùng trên score semantic model. PI-Guard kế thừa protocol tách validation/test và đặt giả thuyết riêng rằng score `p_attack` của L2 có thể dùng để chọn fast-pass, vùng chuyển L3 và direct-block. Hai cutoff của PI-Guard sẽ được chọn theo ràng buộc attack escape/benign false block trên validation; paper không cung cấp cutoff số hoặc bằng chứng trực tiếp cho cascade TF-IDF→DeBERTa.” [[1]](#ref1)

## References

<a id="ref1"></a>**[1]** A. Akinrele and S. N. Gowda, “Prompt Injection Detection is Regime-Dependent: A Deployment-Aware Evaluation with Interpretable Structural Signals,” arXiv:2605.26999v1, 2026. [Full text](https://arxiv.org/html/2605.26999) · [Abstract/version](https://arxiv.org/abs/2605.26999).

<a id="ref2"></a>**[2]** scikit-learn developers, “Tuning the decision threshold for class prediction,” User Guide. [Documentation](https://scikit-learn.org/stable/modules/classification_threshold.html).

<a id="ref3"></a>**[3]** scikit-learn developers, “Probability calibration,” User Guide. [Documentation](https://scikit-learn.org/stable/modules/calibration.html).

<a id="ref4"></a>**[4]** scikit-learn developers, “LogisticRegression,” API Reference. [Documentation](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html).
