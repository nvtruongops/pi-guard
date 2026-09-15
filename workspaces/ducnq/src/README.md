# 🛡️ BỘ CÔNG CỤ ĐỐI CHUẨN ĐỘ BỀN ĐỐI KHÁNG (ADVERSARIAL ROBUSTNESS TESTBED)
## PHÂN HỆ KHẢO SÁT SƠ BỘ — WORKSPACE NGUYỄN QUÍ ĐỨC (`workspaces/ducnq/src/`)

> [!NOTE]
> **Mục đích tài liệu**: Hướng dẫn các thành viên trong nhóm nghiên cứu (**PI-Guard**) hiểu rõ cấu trúc, công dụng của từng mô đun mã nguồn trong thư mục `src/`, và quy trình từng bước để **tự chạy tái lập 100% kết quả thực nghiệm đối chứng** (Reproducibility) trên máy cá nhân.

---

## 📂 1. Cấu Trúc & Công Dụng Từng File Mã Nguồn

| Tên File | Công Dụng Kỹ Thuật | Nguồn Gốc & Cơ Sở Lý Thuyết |
| :--- | :--- | :--- |
| [`jailguard_mutators.py`](file:///d:/DoAn/pi-guard/workspaces/ducnq/src/jailguard_mutators.py) | **Bộ toán tử đột biến đối kháng (Targeted Mutators)**:<br/>Tự động biến đổi một prompt bình thường thành các đòn tấn công lẩn tránh rào chắn (Evasion Attacks): Leetspeak (`1gn0r3`), chèn khoảng trắng (`i g n o r e`), nhét ký tự tàng hình Zero-Width, mã hóa Base64, và hoán đổi chữ Latinh bằng chữ Cyrillic (Homoglyphs). | Kế thừa trực tiếp Algorithm 1 trong bài báo **JailGuard** (*ACM Transactions on Software Engineering and Methodology - TOSEM 2025*, Tạp chí hạng A* thế giới, [arXiv:2312.10766](https://arxiv.org/pdf/2312.10766.pdf)). |
| [`adversarial_robustness_suite.py`](file:///d:/DoAn/pi-guard/workspaces/ducnq/src/adversarial_robustness_suite.py) | **Khung đo đạc độ bền đa lát cắt (Multi-slice Benchmark Harness)**:<br/>Cung cấp bộ dữ liệu kiểm thử đối kháng (10 adversarial test slices) và hàm tính toán tự động các chỉ số vàng: Accuracy, Precision, Recall (TPR), F1-Score, FPR (Over-defense), Evasion Rate ($1 - \text{Recall}$), và độ suy giảm $\Delta F_1$. Xuất báo cáo Markdown và JSON. | Chuẩn hóa theo tiêu chuẩn đánh giá rào chắn bảo vệ LLM (**NIST AI 100-2e2025** & **InjecGuard ACL 2025**). |
| [`scratch_baseline_robustness_eval.py`](file:///d:/DoAn/pi-guard/workspaces/ducnq/src/scratch_baseline_robustness_eval.py) | **Kịch bản thực nghiệm đối chứng trực tiếp**:<br/>Chạy so sánh độc lập giữa 2 cơ chế: (1) Mô hình từ khóa đơn thuần (Word-level TF-IDF mô phỏng) vs (2) Mô hình tích hợp tầng tiền xử lý chuẩn hóa (Unicode NFKC + khử Zero-width + khử Spacing + Character n-grams). | Kiểm chứng giả thuyết: *Word-level TF-IDF sụp đổ trước biến dị ký tự bề mặt, trong khi Character n-grams khôi phục khả năng nhận diện*. |
| [`test_adversarial_suite.py`](file:///d:/DoAn/pi-guard/workspaces/ducnq/src/test_adversarial_suite.py) | **Bộ kiểm thử tự động (Unit Test Suite)**:<br/>Kiểm tra tính đúng đắn của các bộ biến dị, đảm bảo chuỗi đột biến không gây crash và các công thức tính toán chỉ số TPR, FPR, F1 không bị lỗi logic. | Tiêu chuẩn chất lượng phần mềm (Software QA & Pytest Verification). |

---

## 🚀 2. Hướng Dẫn Từng Bước Để Chạy Thực Nghiệm (Step-by-Step Execution Guide)

Mọi thành viên trong nhóm đều có thể tự chạy kiểm chứng chéo trên máy của mình bằng 2 bước cực kỳ đơn giản:

### Bước 1: Kiểm thử độ toàn vẹn của các bộ biến dị (Unit Test)
Chạy lệnh sau từ thư mục gốc của repository:
```powershell
pytest workspaces/ducnq/src/test_adversarial_suite.py -v
```
*(Hoặc chạy qua python: `python -m unittest workspaces/ducnq/src/test_adversarial_suite.py`)*  
👉 **Kỳ vọng**: Toàn bộ 5 test cases đều `PASSED` 100%.

### Bước 2: Chạy thực nghiệm đối chuẩn so sánh
Chạy script thực nghiệm:
```powershell
python workspaces/ducnq/src/scratch_baseline_robustness_eval.py
```
👉 **Kỳ vọng**: 
1. Màn hình Terminal sẽ in ra **2 Bảng Markdown chi tiết**:
   - **Bảng 1 (Naive Word-level Model)**: Cho thấy Recall tụt về `0.0%` khi gặp đòn Spacing, Leetspeak, Zero-width (Evasion Rate = `100.0%`).
   - **Bảng 2 (Proposed Normalization Pipeline)**: Cho thấy F1 duy trì vững chắc ở mức `88.9%` trên mẫu sạch, Leetspeak nhẹ và Zero-width.
2. File kết quả JSON sẽ được tự động xuất ra tại: [`workspaces/ducnq/src/adversarial_benchmark_results.json`](file:///d:/DoAn/pi-guard/workspaces/ducnq/src/adversarial_benchmark_results.json).

---

## 🔌 3. Cách Cắm Mô Hình Mới Của Nhóm Vào Để Đo Đạc (Extensibility)

Khi nhóm huấn luyện xong mô hình Baseline thực tế (scikit-learn) hoặc Transformer (`DeBERTa-v3`), các bạn có thể cắm trực tiếp hàm `predict()` của mô hình vào bộ Suite này để đo đạc chỉ trong 3 dòng code:

```python
from adversarial_robustness_suite import AdversarialRobustnessSuite

# 1. Khởi tạo suite
suite = AdversarialRobustnessSuite(seed=42)

# 2. Truyền hàm dự đoán của mô hình mới vào (nhận List[str] -> trả về List[int]: 0 benign, 1 attack)
my_model_results = suite.evaluate_classifier(my_trained_model.predict)

# 3. In bảng Markdown đối chuẩn
print(suite.format_markdown_report(my_model_results))
```

---

## ⚖️ 4. Tuyên Bố Về Bản Chất Số Liệu Thực Nghiệm (Scientific Modesty)
- **Tập mẫu khảo sát sơ bộ**: Các số liệu trên được đo đạc trên tập kiểm thử đối kháng tổng hợp chuẩn hóa sơ bộ (Exploratory Synthetic Slice) nhằm minh họa định tính và định lượng cho hiện tượng sụp đổ từ vựng (Vocabulary OOV Collapse).
- **Mục tiêu hợp tác**: Đây là tài nguyên tham khảo chung để cả nhóm cùng kiểm chứng chéo (cross-check), bổ sung thêm các mẫu phức tạp hơn trong các tuần tiếp theo, trước khi đưa ra kết luận đồng quy chính thức vào `Final-Report/`.
