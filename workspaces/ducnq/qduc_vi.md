# 🎯 CÁC CÂU HỎI NGHIÊN CỨU & PHƯƠNG PHÁP GIẢI QUYẾT (RQ SOLUTION)

---

### 🔹 RQ1 — KHẢ NĂNG KHÁI QUÁT HÓA & TÍNH TOÀN VẸN DỮ LIỆU (GENERALIZATION & DATA INTEGRITY)

> **Câu hỏi nghiên cứu**:  
> *"Phương pháp phân chia dữ liệu theo nhóm (Group-Aware Splitting) giảm thiểu hiện tượng lạc quan ảo của bộ chuẩn đối sánh (Benchmark Optimism) và phản ánh chính xác khả năng khái quát hóa ngoài phân phối (OOD) của các bộ phân loại Guardrail ở mức độ nào?"*

* **Giả thuyết khoa học ($H_1$)**:  
  Việc chia dữ liệu ngẫu nhiên truyền thống (Random Split) sẽ gây ra hiện tượng rò rỉ dữ liệu (Data Leakage) do các mẫu câu (prompt templates) bị lặp lại ngữ nghĩa giữa tập huấn luyện và tập kiểm thử, từ đó thổi phồng các chỉ số đánh giá một cách ảo tưởng. Ngược lại, phương pháp chia theo nhóm (Group-Aware / Cluster-based Split) sẽ phơi bày chính xác mức độ sụt giảm hiệu năng khi mô hình đối mặt với dữ liệu ngoài phân phối (OOD).
* **Quy trình thực nghiệm đánh giá (Evaluation Protocol)**:
  - So sánh thực nghiệm: **Phân chia ngẫu nhiên (Random Split)** đối sánh với **Phân chia theo nhóm/cụm (Group-Aware Split)**.
  - Đánh giá khả năng phát hiện trên các họ tấn công hoàn toàn mới chưa từng thấy (Tập kiểm thử OOD).
  - Các chỉ số đo lường: Macro-$F_1$, Precision, Recall, và Khoảng cách suy giảm hiệu năng ($\Delta F_1 = F_1^{\text{Random}} - F_1^{\text{Group}}$).

---

### 🔹 RQ2 — HIỆU QUẢ PHÒNG THỦ (GIẢ THUYẾT PHÒNG THỦ ĐA TẦNG - THE LAYERED HYPOTHESIS)

> **Câu hỏi nghiên cứu**:  
> *"Kiến trúc phòng thủ đa tầng (Multi-layer Defense) có mang lại khả năng chống chịu vượt trội trước các cuộc tấn công Prompt Injection và Jailbreak đa dạng so với các cơ chế phòng thủ đơn tầng riêng lẻ hay không?"*

* **Giả thuyết khoa học ($H_2$)**:  
  Một kiến trúc phòng thủ đa tầng (kết hợp chuẩn hóa cú pháp, bộ phân loại Baseline mức ký tự, và mô hình Transformer hiểu ngữ nghĩa sâu) sẽ đạt được tỷ lệ tấn công thành công ($ASR$) thấp hơn và tỷ lệ bắt tấn công (Recall) cao hơn hẳn so với việc chỉ sử dụng đơn lẻ một tầng phòng thủ, trên cả các mẫu tấn công trực tiếp lẫn các biến thể lẩn tránh tinh vi.
* **Quy trình thực nghiệm đánh giá (Evaluation Protocol)**:
  - So sánh đối chứng: **Phòng thủ đơn tầng** (ví dụ: Chỉ dùng Regex, Chỉ dùng TF-IDF, hoặc Chỉ dùng DeBERTa) đối sánh với **Phòng thủ đa tầng (PI-Guard)**.
  - Phân tích chi tiết trên phổ tấn công đa dạng:
    - *Tấn công trực tiếp (Direct Attacks)*: Các câu lệnh chèn mã và đóng vai Jailbreak (DAN mode) tiêu chuẩn.
    - *Tấn công làm rối cú pháp (Obfuscated Attacks)*: Kỹ thuật Leetspeak, chèn khoảng trắng phân tách từ (Spacing) thông qua bộ mutator của JailGuard.
    - *Tấn công mã hóa (Encoded Attacks)*: Giấu mã độc trong payload Base64 (Base64 Smuggling).
  - Các chỉ số đo lường: Tỷ lệ tấn công thành công ($ASR \downarrow$), Độ nhạy/Tỷ lệ bắt trúng ($Recall / TPR \uparrow$), Tỷ lệ cảnh báo sai ($FPR \downarrow$).

---

### 🔹 RQ3 — TÍNH THỰC TIỄN KHI TRIỂN KHAI & CÂN ĐỐI HIỆU NĂNG (DEPLOYMENT PRACTICALITY)

> **Câu hỏi nghiên cứu**:  
> *"Liệu hệ thống Guardrail đề xuất có thể thỏa mãn đồng thời bộ ba tiêu chuẩn vận hành: tỷ lệ lọt lưới thấp, mức độ chặn nhầm người dùng hợp lệ không đáng kể, và độ trễ suy luận cực thấp để triển khai bảo vệ trực tuyến (Inline Deployment) hay không?"*

* **Giả thuyết khoa học ($H_3$)**:  
  Hệ thống Guardrail đề xuất có thể duy trì đồng thời năng lực phòng thủ vững chắc và đạt độ trễ phân vị $P_{95} < 30\text{ms}$ khi chạy trên phần cứng CPU đa nhân phổ thông mà không bắt buộc phải phụ thuộc vào hạ tầng GPU đắt đỏ.
* **Các chỉ số mục tiêu bất biến (Operational Invariants)**:
  - **Mức độ an toàn (Giới hạn lọt lưới)**: $ASR_{guardrail} < 5.0\%$ (tương đương tỷ lệ bắt trúng $\text{Recall} > 95.0\%$).
  - **Trải nghiệm người dùng (Giới hạn chặn nhầm)**: $FPR < 1.5\%$ trên cả các câu hỏi hợp lệ thông thường và câu hỏi có lỗi chính tả/nhiễu vô hại.
  - **Độ trễ suy luận khi vận hành**: Độ trễ phân vị $P_{95} < 30\text{ ms}$ trên CPU đa nhân tiêu chuẩn.
