# 02 — Chọn estimator cho L2: Logistic Regression trước, LinearSVC là ablation

## Scope Boundary Declaration

- **Nguồn nhiệm vụ:** [TASK.md](TASK.md), Review 1 lần 2, 2026-10-01.
- **IN-SCOPE:** phân biệt TF-IDF với classifier; xác định baseline đề xuất và cách dùng score cho routing.
- **OUT-OF-SCOPE:** khẳng định LinearSVC tốt/nhanh hơn khi chưa so sánh cùng protocol; gán metric của paper hoặc Logistic Regression cho LinearSVC; đặt ngưỡng số.

## Trả lời trực tiếp

Có mô hình trong bài được chọn làm căn cứ: Akinrele và Gowda mô tả sparse lexical baseline là **TF-IDF + Logistic Regression**. “TF-IDF only” trong bảng của bài là tên ablation về loại đặc trưng; estimator vẫn là Logistic Regression. TF-IDF tự nó chỉ biến văn bản thành vector, không dự đoán nhãn nếu thiếu classifier. [[1]](#ref1)

Do đó, cấu hình L2 bám bài để bắt đầu là:

```text
per-chunk text → word/character TF-IDF → Logistic Regression → attack-risk score
```

Phân lớp L2 là screening sơ bộ `benign` / `suspect`; nó dùng để tạo route-candidate, chưa phải policy cuối request.

## Route của L2 và ranh giới quyết định

L2 tạo đúng ba route state theo từng chunk: ALLOW candidate ở điểm thấp, REVIEW→L3 ở vùng giữa, BLOCK candidate ở điểm cao. REVIEW chỉ yêu cầu API chuyển chunk sang L3, không phải trạng thái request chờ người xử lý. L3 trả score/nhãn; API kiểm tra coverage và tổng hợp kết quả cuối thành ALLOW hoặc BLOCK. Lỗi kỹ thuật là error/fail-closed riêng.

## Logistic Regression và LinearSVC

| Điểm so sánh | Logistic Regression | LinearSVC |
|---|---|---|
| Vai trò trong bản đề xuất | Baseline L2 bám bài 2605.26999. | Ablation/biến thể của đồ án, nếu muốn so sánh sau. |
| Output | `predict_proba` cho xác suất ước lượng; cần đánh giá calibration trước khi dùng như risk probability. | `decision_function` cho signed margin; margin không tự là xác suất. |
| Điều kiện chia vùng | Chọn ngưỡng trên score đã kiểm tra bằng validation. | Chọn ngưỡng riêng trên margin; calibration là bước riêng nếu cần diễn giải như xác suất. |
| Có được kế thừa kết quả paper? | Chỉ các kết quả paper báo cáo cho đúng Logistic Regression và protocol của họ. | Không. Phải chạy và báo cáo riêng. |

Bản thân việc cần threshold không làm LinearSVC hợp lý hơn: margin vẫn có thể chia vùng nhưng không cho `p(attack)` trực tiếp. Mọi ngưỡng của cả hai biến thể đều phải được chọn riêng trên validation, không lấy từ paper. [[1]](#ref1) [[2]](#ref2) [[3]](#ref3)

## Hai ngưỡng được tạo thế nào?

Ngưỡng **không phải một mô hình thứ hai cần huấn luyện**. Quy trình là:

1. Gắn nhãn train cho L2 ở mức `benign` và `attack/suspect`; fit vocabulary/IDF của TF-IDF và hệ số Logistic Regression trên train.
2. Với mỗi chunk mới, dùng vectorizer đã fit để tính `Xᵢ = TFIDF(chunkᵢ)`, rồi lấy `pᵢ = predict_proba(Xᵢ)[attack]`. Đây là score đầu vào cho bộ route.
3. Trên validation riêng, chọn hai điểm cắt cho cùng score: `pᵢ ≤ τ_allow` → fast-pass candidate; `τ_allow < pᵢ < τ_block` → chuyển chunk sang L3; `pᵢ ≥ τ_block` → block candidate.
4. Đánh giá các cặp ngưỡng theo mục tiêu đã định: vùng fast-pass phải có lượng attack lọt qua đủ thấp; vùng block phải giữ benign false-positive trong giới hạn chấp nhận được. Sau đó freeze ngưỡng trước khi chạy test.

Vì vậy mô hình học **vectorizer + trọng số Logistic Regression** từ dữ liệu train; bước ngưỡng là **quy tắc hậu xử lý xác định** trên score của mô hình. Mốc mặc định `0.5` chỉ là cutoff mặc định cho phân loại nhị phân; nó không tự tạo ra hai ngưỡng cascade. Tuning threshold có thể thay đổi cutoff mà không thay hệ số đã fit. [[4]](#ref4)

`predict_proba` của Logistic Regression thường có xu hướng hiệu chuẩn tốt hơn nhiều classifier khác, nhưng vẫn phải kiểm tra reliability/calibration trên dữ liệu giữ riêng. Nếu cần hiệu chuẩn, fit calibrator bằng cross-validation trên train hoặc dữ liệu calibration tách biệt; không fit calibrator bằng test. [[5]](#ref5)

**Chưa có căn cứ để ghi số cho `τ_allow` / `τ_block`.** Nếu không tìm được cặp ngưỡng đáp ứng mục tiêu trên validation, không bật fast-pass/block shortcut; cho mọi chunk qua L3 trong phép đo cascade đối chứng. Không dò ngưỡng trên test. [[1]](#ref1) [[4]](#ref4)

## Khuyến nghị chốt cho Review 1

1. Ghi **TF-IDF + Logistic Regression** là baseline tham khảo ở L2, dùng đúng bài 2605.26999 làm nguồn học thuật cho lựa chọn này.
2. Không yêu cầu thêm một paper TF-IDF khác cho lập luận hiện tại. PIDS-Bench local result, nếu được nêu, phải giữ riêng là phép chạy cục bộ paper-matched, không phải chứng cứ cho cascade.
3. LinearSVC chỉ là nhánh ablation tương lai; so cùng vectorizer, split và quy trình tuning nếu có đủ phạm vi.
4. Không đặt ngưỡng định lượng trong kiến trúc hiện tại. `τ_allow` và `τ_block` là ký hiệu để hiệu chỉnh/đánh giá sau.

## References

<a id="ref1"></a>**[1]** A. Akinrele and S. N. Gowda, “Prompt Injection Detection is Regime-Dependent: A Deployment-Aware Evaluation with Interpretable Structural Signals,” arXiv:2605.26999v1, 2026. [Full text](https://arxiv.org/html/2605.26999).

<a id="ref2"></a>**[2]** scikit-learn, `LogisticRegression` API. [Documentation](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html).

<a id="ref3"></a>**[3]** scikit-learn, `LinearSVC` and `CalibratedClassifierCV` APIs. [LinearSVC](https://scikit-learn.org/stable/modules/generated/sklearn.svm.LinearSVC.html) · [CalibratedClassifierCV](https://scikit-learn.org/stable/modules/generated/sklearn.calibration.CalibratedClassifierCV.html).

<a id="ref4"></a>**[4]** scikit-learn, “Tuning the decision threshold for class prediction.” [User guide](https://scikit-learn.org/stable/modules/classification_threshold.html).

<a id="ref5"></a>**[5]** scikit-learn, “Probability calibration.” [User guide](https://scikit-learn.org/stable/modules/calibration.html).
