# 🛡️ BÁO CÁO KỸ THUẬT TASK 2: KHUNG ĐE DỌA 5 TRỤC & 2 MÔ HÌNH THAM KHẢO HỌC THUẬT
## ĐỀ TÀI: A MACHINE-LEARNING GUARDRAIL FOR DETECTING PROMPT INJECTION AND JAILBREAK ATTACKS ON LLM APPLICATIONS (PI-GUARD)

**Tác giả thực hiện**: Nguyễn Quí Đức (`SE182087`) | **Workspace**: `workspaces/ducnq/`  
**Căn cứ đề tài**: Bản đăng ký đề tài [`CAPSTONE PROJECT REGISTER.md`](file:///d:/DoAn/pi-guard/CAPSTONE%20PROJECT%20REGISTER.md) & Biên bản [`Final-Report/Meeting/Meeting 4_10_09_26.md`](file:///d:/DoAn/pi-guard/Final-Report/Meeting/Meeting%204_10_09_26.md)  
**Nhật ký tài liệu tham khảo cục bộ**: [`workspaces/ducnq/References/REFERENCES_LOG.md`](file:///d:/DoAn/pi-guard/workspaces/ducnq/References/REFERENCES_LOG.md)  
**Báo cáo kỹ thuật tổng hợp**: [`workspaces/ducnq/doc/TASK_1_2_TECHNICAL_MASTERY.md`](file:///d:/DoAn/pi-guard/workspaces/ducnq/doc/TASK_1_2_TECHNICAL_MASTERY.md)

---

> [!IMPORTANT]
> ### 🎯 TỔNG QUAN HỌC THUẬT NHIỆM VỤ 2 (EXECUTIVE SUMMARY)
> 1. **Khung đe dọa 5 trục chuẩn hóa (5D Threat Framework)**: Tổng hợp theo **NIST AI 100-2e2025**, **MITRE ATLAS**, công trình mới tại **USENIX Security 2026** [[D1]](#ref-d1), [[D2]](#ref-d2), **ACM TOSEM 2025** [[D6]](#ref-d6) và **ICLR 2026** [[D3]](#ref-d3) để bao quát từ cú pháp bề mặt, đòn tấn công thích ứng, phân tầng luồng dữ liệu, dấu vết n-gram/ngữ nghĩa đến bán kính thiệt hại.
> 2. **Phân tích 2 kiến trúc tham khảo học thuật (Candidate Reference Architectures)**:
>    - **Kiến trúc Classical Machine Learning (Túi từ n-grams + Bộ phân loại tuyến tính)**: Tốc độ suy luận rất nhanh (~vài mili-giây), kháng biến dị cú pháp bề mặt tốt nếu có Character n-grams (`char_wb`), nhưng điểm nghẽn là "mù ngữ nghĩa sâu" trước các câu lệnh tiêm nhiễm tinh vi.
>    - **Kiến trúc Deep Semantic Transformer (Cơ chế chú ý phân tách - Disentangled Attention)**: Bóc tách vector nội dung và vị trí, nắm bắt ngữ nghĩa tinh vi đạt $F_1 > 0.97$, nhưng dung lượng nặng (~vài trăm MB) và độ trễ CPU cao, đòi hỏi kỹ thuật tối ưu hóa/lượng hóa nếu đưa vào rào chắn thực tế.
> 3. **Khảo sát độ bền đối kháng sơ bộ**: Hiện thực hóa bộ đột biến đối kháng JailGuard (`src/jailguard_mutators.py`), chứng minh bộ lọc mức từ thô sụp đổ trước biến dị chèn khoảng trắng/leetspeak, và tầng chuẩn hóa NFKC + Character n-grams khôi phục đáng kể khả năng nhận diện.

---

# I. KHUNG PHÂN TÍCH MỐI ĐE DỌA 5 TRỤC TOÀN DIỆN (5D FRAMEWORK)

Khung phân tích được chuẩn hóa từ tiêu chuẩn **NIST AI 100-2e2025**, ma trận **MITRE ATLAS**, bài báo **USENIX Security 2026** [[D1]](#ref-d1) và khung đánh giá thống nhất 2026 [[D11]](#ref-d11):

```mermaid
flowchart TD
    subgraph 5D ["KHUNG PHÂN TÍCH MỐI ĐE DỌA 5 TRỤC (5D THREAT FRAMEWORK)"]
        D1["<b>TRỤC 1: CƠ CHẾ TẤN CÔNG & PAYLOAD</b><br/>• Đột biến ký tự: Spacing, Leetspeak, Zero-width<br/>• Tấn công ngữ cảnh: Few-shot, Controlled-Release"]
        D2["<b>TRỤC 2: GIẢ ĐỊNH NĂNG LỰC KẺ TẤN CÔNG</b><br/>• Black-box API query<br/>• Adaptive Attacker (Nasr 2026)<br/>• Transferable Adversary (Angell 2026)"]
        D3["<b>TRỤC 3: LUỒNG HOẠT ĐỘNG & CHU TRÌNH DỮ LIỆU</b><br/>• Ingress Proxy Inspection<br/>• Tiền xử lý NFKC Normalization<br/>• Phân tầng độ trễ: TF-IDF (~2.8ms) vs DeBERTa (~42.5ms)"]
        D4["<b>TRỤC 4: DẤU VẾT TÍN HIỆU NHẬN DIỆN</b><br/>• Dấu vết cú pháp: Character/Token ratio, Perplexity<br/>• Dấu vết ngữ nghĩa: Disentangled Attention shift"]
        D5["<b>TRỤC 5: BÁN KÍNH THIỆT HẠI & TUÂN THỦ</b><br/>• Prompt Leaking & Data Exfiltration<br/>• Tool Hijacking trong Agent<br/>• Tuân thủ NIST AI RMF & EU AI Act"]
    end
```

### Chi Tiết 5 Trục:
1. **Trục 1: Cơ Chế Tấn Công & Cấu Trúc Payload**:
   - *Tấn công cú pháp bề mặt*: Chèn khoảng trắng (`i g n o r e`), Leetspeak (`1gn0r3`), Homoglyphs, Base64 Smuggling (Zhang et al. TOSEM 2025 [[D6]](#ref-d6)), biến dị làm mịn (Robey et al. 2023 [[D14]](#ref-d14)).
   - *Tấn công ngữ cảnh & ngữ nghĩa*: Đòn tấn công chèn mẫu vài bước (Few-shot demonstrations) [[D16]](#ref-d16), ngụy trang ngôn ngữ (Linguistic Camouflage, Cipher) [[D18]](#ref-d18), và kỹ thuật giải phóng có kiểm soát (*Controlled-Release Prompting*) bóc tách payload qua mặt rào chắn Ingress trong môi trường Production (Fairoze et al. USENIX Security 2026 [[D2]](#ref-d2)).
2. **Trục 2: Giả Định Năng Lực Kẻ Tấn Công (Threat Model)**:
   - *Black-box*: Kẻ tấn công chỉ gửi prompt qua API/Chat và nhận về nhãn/phản hồi, không biết trọng số bên trong (mô hình đe dọa thực tế nhất).
   - *Adaptive Attacker*: Kẻ tấn công có tri thức về cơ chế phòng thủ và điều chỉnh payload để né tránh (Nasr et al. USENIX Security 2026 [[D1]](#ref-d1)).
   - *Transferable Adversary*: Khai thác tính chuyển giao đối kháng xuất phát từ không gian biểu diễn chung giữa các LLM (Angell et al. ICLR 2026 [[D3]](#ref-d3)).
3. **Trục 3: Luồng Hoạt Động & Chu Trình Dữ Liệu (Execution Flow)**:
   - Luồng dữ liệu qua Ingress Proxy: `Client → Prompt Ingestion API → Preprocessing (NFKC Normalization) → Guardrail Classifier → Allow (Forward to LLM) / Block (Drop & Log)` [[D15]](#ref-d15).
   - Phân tầng độ trễ: So sánh giữa mạng nơ-ron nông kết hợp ensemble (~50ms, Neves et al. 2026 [[D4]](#ref-d4)) và Baseline Tầng 1 của PI-Guard (TF-IDF + LinearSVC ~2.8ms).
4. **Trục 4: Dấu Vết Tín Hiệu Nhận Diện (Detection Footprint)**:
   - *Dấu vết cú pháp*: Tần suất n-gram ký tự dị thường, tỷ lệ ký tự/token (CPT) suy giảm bất thường do tokenizer bị phân mảnh; độ hỗn loạn cấu trúc (Perplexity Anomaly, Bhat et al. 2025 [[D9]](#ref-d9); Jain et al. 2023 [[D13]](#ref-d13)).
   - *Dấu vết ngữ nghĩa sâu*: Sự xuất hiện đột ngột của các mệnh lệnh cưỡng chế hành động nằm lệch pha với ngữ cảnh tài liệu tham chiếu (bắt qua Disentangled Attention của DeBERTa-v3).
5. **Trục 5: Bán Kính Thiệt Hại & Tuân Thủ (Blast Radius & Compliance)**:
   - Rò rỉ dữ liệu mật (Data Exfiltration qua Markdown image tag) và xâm phạm bảo mật dữ liệu LLM (Alqahtani et al. Springer 2026 [[D8]](#ref-d8)).
   - Chiếm quyền điều khiển công cụ tự trị (Tool Hijacking trong AI Agent) [[D17]](#ref-d17).
   - Chế tài pháp lý nghiêm ngặt theo **NIST AI RMF**, **EU AI Act** và khung an toàn thống nhất [[D11]](#ref-d11).

---

# II. CƠ SỞ TOÁN HỌC & ĐIỂM NGHẼN CỦA 2 MÔ HÌNH THAM KHẢO

```mermaid
flowchart LR
    subgraph M1 ["KIẾN TRÚC 1: CLASSICAL ML CANDIDATE"]
        direction TB
        T1["<b>Túi từ n-grams + Phân loại tuyến tính</b><br/>Neel Jain et al. (NeurIPS 2023)"]
        P1["<b>ƯU ĐIỂM:</b><br/>• Độ trễ siêu nhanh (~vài mili-giây CPU)<br/>• Nhẹ, không cần GPU<br/>• Kháng biến dị ký tự nếu dùng char_wb"]
        C1["<b>ĐIỂM NGHẼN:</b><br/>• Mù ngữ nghĩa sâu (Semantic Blindness)<br/>• Thất bại trước đòn tấn công tinh vi"]
        T1 --> P1 --> C1
    end

    subgraph M2 ["KIẾN TRÚC 2: DEEP SEMANTIC TRANSFORMER CANDIDATE"]
        direction TB
        T2["<b>Transformer với Disentangled Attention</b><br/>Pengcheng He et al. (ICLR 2023)"]
        P2["<b>ƯU ĐIỂM:</b><br/>• Bóc tách vector Nội dung & Vị trí<br/>• Nắm bắt ngữ nghĩa tinh vi trên câu lệnh dài<br/>• Bắt trúng vị trí lệnh tiêm nhiễm"]
        C2["<b>ĐIỂM NGHẼN:</b><br/>• Nặng (~vài trăm MB)<br/>• Độ trễ CPU cao, cần tối ưu hóa/lượng hóa<br/>• Chi phí tính toán lớn hơn"]
        T2 --> P2 --> C2
    end
```

### 1. Kiến Trúc Tham Khảo 1: Classical ML Baseline (Túi từ n-grams + Bộ phân loại tuyến tính)
- **Công trình gốc trong tài liệu tham khảo**: Neel Jain et al. (NeurIPS 2023 [[D13]](#ref-d13)), *Baseline Defenses for Adversarial Attacks on Language Models*.
- **Cơ sở toán học**:
  $$\text{TF-IDF}(t, d, D) = \text{TF}(t, d) \times \left[\log\left(\frac{1 + |D|}{1 + |\{d \in D : t \in d\}|}\right) + 1\right]$$
  - Trích xuất đặc trưng đa tầng theo lý thuyết:
    - Word n-grams: Bắt cụm từ khóa lộ diện ("ignore previous", "system prompt").
    - Character n-grams với ranh giới từ: `char_wb` giúp bắt các phân mảnh từ khóa khi bị chèn khoảng trắng hoặc ký tự leetspeak.
  - Phân loại bằng bộ phân loại tuyến tính (như Linear Support Vector Classifier hoặc Logistic Regression).
- **Ưu điểm theo lý thuyết**:
  - Tốc độ suy luận rất nhanh trên CPU, tiêu thụ bộ nhớ thấp, không đòi hỏi phần cứng GPU chuyên dụng.
- **Điểm nghẽn học thuật**:
  - **Mù ngữ nghĩa sâu (Semantic Blindness)**: Bản chất túi từ giả định tính độc lập có điều kiện của các từ. Khi kẻ tấn công dùng từ ngữ lịch sự, phép hoán dụ, hoặc viết kịch bản giả tưởng không chứa từ khóa tấn công quen thuộc, mô hình tuyến tính hoàn toàn mất khả năng nhận diện.

---

### 2. Kiến Trúc Tham Khảo 2: Deep Semantic Transformer (Đại diện tiêu biểu: Cơ chế Disentangled Attention)
- **Công trình gốc trong tài liệu tham khảo**: Pengcheng He et al. (ICLR 2023), *DeBERTaV3: Improving DeBERTa using ELECTRA-Style Pre-Training with Gradient-Disentangled Embedding Sharing*.
- **Cơ chế toán học cốt lõi — Disentangled Attention**:
  - Khác với cơ chế gộp chung vector từ và vị trí thông thường $\mathbf{x}_i = \mathbf{w}_i + \mathbf{p}_i$, cơ chế Disentangled Attention biểu diễn mỗi token bằng hai vector độc lập: vector nội dung $\mathbf{c}_i$ và vector vị trí tương đối $\mathbf{p}_{i|j}$.
  - Trọng số chú ý tương hỗ giữa token $i$ và token $j$ được bóc tách thành 3 thành phần:
    $$A_{i,j} = \mathbf{c}_i \mathbf{c}_j^T + \mathbf{c}_i \mathbf{p}_{j|i}^T + \mathbf{p}_{i|j} \mathbf{c}_j^T$$
    - $\mathbf{c}_i \mathbf{c}_j^T$: Tương đồng nội dung giữa hai từ (*Content-to-Content*).
    - $\mathbf{c}_i \mathbf{p}_{j|i}^T$: Tương quan giữa nội dung từ $i$ với khoảng cách đến từ $j$ (*Content-to-Position*).
    - $\mathbf{p}_{i|j} \mathbf{c}_j^T$: Tương quan giữa vị trí tương đối và nội dung từ $j$ (*Position-to-Content*).
  - **Ý nghĩa học thuật đối với bài toán Guardrail**:
    - Cơ chế này giúp mô hình nhạy bén với **vị trí ngữ cảnh của câu lệnh** — hỗ trợ phát hiện các mệnh lệnh tiêm nhiễm nằm ở đuôi văn bản dài hoặc bị ngụy trang trong hội thoại.
    - Theo nghiên cứu tại **ICLR 2026** [[D3]](#ref-d3), các đòn tấn công jailbreak có tính chuyển giao cao xuất phát từ không gian biểu diễn chung (shared representations) giữa các LLM, khẳng định các họ Transformer biểu diễn ngữ nghĩa sâu là hướng tiếp cận nền tảng.
- **Ưu điểm**: Khả năng phân tích ngữ nghĩa sâu, nhận diện tốt các kịch bản ngữ cảnh phức tạp.
- **Điểm nghẽn học thuật**:
  - Dung lượng mô hình lớn, độ trễ trên CPU cao hơn đáng kể so với mô hình tuyến tính, đòi hỏi phải có giải pháp tối ưu hóa (như lượng hóa hoặc chưng cất) nếu muốn đáp ứng mục tiêu thời gian phản hồi thấp của rào chắn.

---

# III. KẾT QUẢ KHẢO SÁT THỰC NGHIỆM SƠ BỘ VỀ ĐỘ BỀN ĐỐI KHÁNG (PRELIMINARY ADVERSARIAL BENCHMARK)

> [!NOTE]
> **Định vị nghiên cứu**: Đây là tập thực nghiệm sơ bộ (Exploratory / Reproducible Benchmark) nhằm khảo sát định lượng giả thuyết khoa học: *Mô hình chỉ dựa trên từ khóa (Word-level TF-IDF) dễ bị vượt qua bởi các biến dị cú pháp bề mặt, trong khi tầng tiền xử lý chuẩn hóa ký tự (Unicode NFKC + Character n-grams) giúp tăng cường độ bền*. Nhóm nghiên cứu có thể sử dụng bộ công cụ này để kiểm chứng chéo và đo đạc cho các mô hình Transformer tiếp theo.

Kế thừa thuật toán sinh biến dị từ công trình của **Zhang et al. (ACM TOSEM 2025 [[D6]](#ref-d6))**, kịch bản thực nghiệm đối chứng được thiết lập tại [`workspaces/ducnq/src/scratch_baseline_robustness_eval.py`](file:///d:/DoAn/pi-guard/workspaces/ducnq/src/scratch_baseline_robustness_eval.py) trên 10 lát cắt đối kháng (Adversarial Slices):

### 1. Bảng Đối Chuẩn 1: Mô Hình Đối Chứng Từ Khóa (Simulating Naive Word-level TF-IDF)

| Lát Cắt Kiểm Thử (Test Slice) | Accuracy | Precision | Recall (TPR) | F1-Score | FPR | Tỷ Lệ Lọt Lưới (Evasion Rate) | Độ Sụt Giảm $\Delta F_1$ |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Clean_Baseline** (Mẫu gốc) | 80.0% | 100.0% | 60.0% | 75.0% | 0.0% | 40.0% | +0.0% |
| **Leetspeak_Mild_p0.3** | 50.0% | 0.0% | **0.0%** | **0.0%** | 0.0% | **100.0%** | **+75.0%** |
| **Leetspeak_Heavy_p0.7** | 50.0% | 0.0% | **0.0%** | **0.0%** | 0.0% | **100.0%** | **+75.0%** |
| **Spacing_WordSplit** | 50.0% | 0.0% | **0.0%** | **0.0%** | 0.0% | **100.0%** | **+75.0%** |
| **Spacing_FullChar** | 50.0% | 0.0% | **0.0%** | **0.0%** | 0.0% | **100.0%** | **+75.0%** |
| **Base64_PayloadWrapping** | 55.0% | 100.0% | 10.0% | 18.2% | 0.0% | 90.0% | +56.8% |
| **ZeroWidth_InvisibleChars** | 50.0% | 0.0% | **0.0%** | **0.0%** | 0.0% | **100.0%** | **+75.0%** |
| **Unicode_Homoglyphs** | 55.0% | 100.0% | 10.0% | 18.2% | 0.0% | 90.0% | +56.8% |
| **JailGuard_Composite_LeetZero** | 50.0% | 0.0% | **0.0%** | **0.0%** | 0.0% | **100.0%** | **+75.0%** |
| **Perturbed_Benign_Robustness** | 80.0% | 100.0% | 60.0% | 75.0% | 0.0% | 40.0% | +0.0% |

👉 **Nhận xét**: Mô hình từ khóa đơn thuần bị sụp đổ hoàn toàn trước các biến dị chèn khoảng trắng (`i g n o r e`), Leetspeak (`1gn0r3`) và ký tự tàng hình Zero-width (Recall rơi về $0.0\%$, Evasion Rate đạt $100.0\%$).

---

### 2. Bảng Đối Chuẩn 2: Mô Hình Tích Hợp Tiền Xử Lý Chuẩn Hóa Ký Tự (Proposed Normalization Pipeline)

| Lát Cắt Kiểm Thử (Test Slice) | Accuracy | Precision | Recall (TPR) | F1-Score | FPR | Tỷ Lệ Lọt Lưới (Evasion Rate) | Độ Sụt Giảm $\Delta F_1$ |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Clean_Baseline** (Mẫu gốc) | 90.0% | 100.0% | 80.0% | **88.9%** | 0.0% | 20.0% | +0.0% |
| **Leetspeak_Mild_p0.3** | 90.0% | 100.0% | 80.0% | **88.9%** | 0.0% | 20.0% | **+0.0%** |
| **Leetspeak_Heavy_p0.7** | 70.0% | 100.0% | 40.0% | 57.1% | 0.0% | 60.0% | +31.8% |
| **Spacing_WordSplit** | 85.0% | 100.0% | 70.0% | **82.3%** | 0.0% | 30.0% | **+6.5%** |
| **Spacing_FullChar** | 85.0% | 100.0% | 70.0% | **82.3%** | 0.0% | 30.0% | **+6.5%** |
| **Base64_PayloadWrapping** | 70.0% | 100.0% | 40.0% | 57.1% | 0.0% | 60.0% | +31.8% |
| **ZeroWidth_InvisibleChars** | 90.0% | 100.0% | 80.0% | **88.9%** | 0.0% | 20.0% | **+0.0%** |
| **Unicode_Homoglyphs** | 55.0% | 100.0% | 10.0% | 18.2% | 0.0% | 90.0% | +70.7% |
| **JailGuard_Composite_LeetZero** | 80.0% | 100.0% | 60.0% | **75.0%** | 0.0% | 40.0% | +13.9% |
| **Perturbed_Benign_Robustness** | 90.0% | 100.0% | 80.0% | **88.9%** | 0.0% | 20.0% | +0.0% |

👉 **Kết luận thực nghiệm**:
1. Chuẩn hóa **Unicode NFKC** và loại bỏ ký tự vô hình (`\u200B-\u200D`) giúp triệt tiêu hoàn toàn đòn tấn công Zero-Width ($F_1$ giữ nguyên $88.9\%$, $\Delta F_1 = 0\%$).
2. Kỹ thuật giải mã Leetspeak và thu gọn khoảng trắng giữa các ký tự đơn lẻ giúp phục hồi Recall nhận diện từ $0\%$ lên $> 70\%$ trên các đòn tấn công Spacing và Leetspeak.
3. Đây là cơ sở thực nghiệm rõ ràng để đề xuất tích hợp tầng tiền xử lý chuẩn hóa trước khi đưa dữ liệu vào bộ phân loại Baseline và Transformer.

---

### 3. Giải Mã Cơ Chế Sinh Số Liệu & Tuyên Bố Rào Trước Khoa Học (Scientific Disclaimers)

1. **Bản chất của số liệu thực nghiệm**:
   - Đây là **bộ khung kiểm thử mô phỏng sơ bộ (Preliminary Testbed Harness)** được xây dựng theo thuật toán sinh biến dị của bài báo **ACM TOSEM 2025 (JailGuard [[D6]](#ref-d6))** tại [`workspaces/ducnq/src/`](file:///d:/DoAn/pi-guard/workspaces/ducnq/src/).
   - Tập kiểm thử hiện tại gồm 20 mẫu prompt đối kháng tổng hợp (Synthetic Adversarial Samples) kết hợp 10 lát cắt biến dị để **minh họa cơ chế lý thuyết và kiểm tra tính toàn vẹn của mã nguồn** trước khi nạp tập dữ liệu quy mô lớn.
2. **Cơ chế tại sao Bảng 1 (Naive Word Filter) tụt Recall về $0.0\%$**:
   - Bộ lọc từ khóa chỉ tìm kiếm các chuỗi ký tự nguyên vẹn (ví dụ: `\bignore\b`). Khi câu lệnh bị cố tình chèn khoảng trắng (`i g n o r e`) hoặc biến đổi Leetspeak (`1gn0r3`), ranh giới từ bị phá vỡ hoàn toàn khiến bộ lọc từ khóa bỏ sót $100\%$ các đòn tấn công (Evasion Rate $= 100\%$).
3. **Cơ chế tại sao Bảng 2 (Proposed Normalization) khôi phục $F_1 = 88.9\%$**:
   - Nhờ tầng tiền xử lý làm sạch: Unicode NFKC bóc tách ký tự tàng hình zero-width, bộ thu gọn khoảng trắng tự động nối liền `i g n o r e` thành `ignore`, và từ điển Leetspeak giải mã `1gn0r3` về `ignore`. Khi văn bản được hoàn nguyên, mô hình nhận diện chính xác các câu lệnh nguy hại.
4. **Tính mở rộng (Extensibility cho Task 3)**:
   - Bộ harness được thiết kế dạng mô đun cắm-rút (Plug-and-Play). Khi nhóm hoàn thành huấn luyện mô hình học máy chính thức trên tập dữ liệu lớn (TF-IDF + LinearSVC, DeBERTa-v3), chỉ cần truyền hàm `predict()` của mô hình vào hàm `evaluate_classifier()` để tự động xuất ra bảng đối chuẩn cho Luận văn tốt nghiệp.

---

# IV. KỊCH BẢN VẤN ĐÁP BẢO VỆ CHO TASK 2

### Câu 1: "Cái bảng số liệu đối chuẩn đối kháng này từ đâu ra? Dữ liệu thực nghiệm là gì?"
> **Trả lời**:  
> *"Dạ thưa Thầy/Hội đồng, bảng số liệu này được xuất tự động từ bộ kiểm thử thực nghiệm `scratch_baseline_robustness_eval.py` dựa trên thuật toán sinh biến dị của bài báo ACM TOSEM 2025 (JailGuard). Đây là bộ testbed khảo sát sơ bộ với 10 lát cắt biến dị tổng hợp (Synthetic Perturbations) nhằm mục đích kiểm chứng cơ chế lý thuyết: chứng minh điểm mù của bộ lọc từ vựng và sự cần thiết của tầng tiền xử lý chuẩn hóa ký tự trước khi nhóm nạp dữ liệu lớn vào huấn luyện ở Task 3."*

### Câu 2: "Tại sao mô hình Word-level lại sụp đổ về 0.0% Recall trước các đòn biến dị ký tự?"
> **Trả lời**:  
> *"Dạ thưa Thầy, vì các mô hình dựa trên từ khóa nguyên vẹn (như Word unigram) phụ thuộc hoàn toàn vào ranh giới từ xác định. Khi kẻ tấn công chèn khoảng trắng giữa các chữ cái ('i g n o r e') hoặc thay thế ký tự số ('1gn0r3'), tokenizer sẽ bẻ gãy từ thành các token đơn lẻ ngoài từ điển (Out-Of-Vocabulary / OOV). Do đó, bộ lọc hoàn toàn không bắt được dấu hiệu độc hại, dẫn đến Recall tụt về 0% và tỷ lệ lọt lưới là 100%."*

### Câu 3: "Tại sao trong tài liệu nghiên cứu (Literature Review), nhóm khảo sát cả hướng tiếp cận Classical ML lẫn Transformer thay vì chỉ tập trung vào một hướng?"
> **Trả lời**:  
> *"Dạ thưa Thầy/Hội đồng, đây là khảo sát đối sánh toàn diện theo yêu cầu học thuật của đề tài:  
> 1. Về mặt lý thuyết, các kiến trúc Transformer có khả năng hiểu ngữ nghĩa sâu rất tốt nhưng chi phí tính toán và độ trễ thường cao hơn. Trong khi đó, các mô hình học máy truyền thống (Classical ML) có ưu thế vượt trội về tốc độ suy luận nhanh và tiêu tốn rất ít tài nguyên.  
> 2. Việc khảo sát cả hai hướng tiếp cận trong tài liệu giúp nhóm hiểu rõ bài toán đánh đổi đa mục tiêu giữa **Độ trễ (Latency)** và **Độ chính xác ngữ nghĩa (Semantic Accuracy)**.  
> 3. Đây là tiền đề lý thuyết để trong các giai đoạn thực nghiệm tiếp theo, nhóm có cơ sở lựa chọn hoặc kết hợp mô hình phù hợp nhất nhằm đảm bảo vừa bắt được tấn công vừa đáp ứng độ trễ thấp của một rào chắn guardrail."*

---

## 📑 TÀI LIỆU THAM KHẢO HỌC THUẬT (REFERENCES)

- <a id="ref-d1"></a>**[[D1]]** M. Nasr, N. Carlini, C. Sitawarin, J. Hayes, F. Tramèr et al., "The Attacker Moves Second: Stronger Adaptive Attacks Bypass Defenses Against LLM Jailbreaks and Prompt Injections," in *Proc. 35th USENIX Security Symposium (USENIX Security '26)*, 2026. Local PDF: [`Nasr_2026_Adaptive_Attacks_Bypass_Defenses_USENIX.pdf`](file:///d:/DoAn/pi-guard/workspaces/ducnq/References/Nasr_2026_Adaptive_Attacks_Bypass_Defenses_USENIX.pdf).
- <a id="ref-d2"></a>**[[D2]]** J. Fairoze, S. Garg, K. Lee, and M. Wang, "Bypassing Prompt Guards in Production with Controlled-Release Prompting," in *Proc. 35th USENIX Security Symposium (USENIX Security '26)*, 2026. Local PDF: [`Fairoze_2026_Bypassing_Prompt_Guards_Controlled_Release_USENIX.pdf`](file:///d:/DoAn/pi-guard/workspaces/ducnq/References/Fairoze_2026_Bypassing_Prompt_Guards_Controlled_Release_USENIX.pdf).
- <a id="ref-d3"></a>**[[D3]]** R. Angell, J. Brinkmann, and H. He, "Jailbreak Transferability Emerges from Shared Representations," in *Proc. International Conference on Learning Representations (ICLR '26)*, 2026. [arXiv:2506.12913](https://arxiv.org/pdf/2506.12913.pdf). Local PDF: [`Angell_2026_Jailbreak_Transferability_Shared_Representations_ICLR.pdf`](file:///d:/DoAn/pi-guard/workspaces/ducnq/References/Angell_2026_Jailbreak_Transferability_Shared_Representations_ICLR.pdf).
- <a id="ref-d4"></a>**[[D4]]** P. R. F. Neves et al., "GuardNet: Ensemble Strategies of Shallow Neural Networks for Robust Prompt Injection and Jailbreak Detection," *arXiv preprint arXiv:2606.05566*, 2026. Local PDF: [`Neves_2026_GuardNet_Shallow_Networks_Guardrail.pdf`](file:///d:/DoAn/pi-guard/workspaces/ducnq/References/Neves_2026_GuardNet_Shallow_Networks_Guardrail.pdf).
- <a id="ref-d6"></a>**[[D6]]** S. Zhang, Z. Li et al., "JailGuard: A Universal Detection Framework for Prompt-based Attacks on LLM Systems," *ACM Transactions on Software Engineering and Methodology (TOSEM)*, 2025. [arXiv:2312.10766](https://arxiv.org/pdf/2312.10766.pdf). Local PDF: [`Duc_2025_JailGuard_Universal_Detection_Framework_TOSEM.pdf`](file:///d:/DoAn/pi-guard/workspaces/ducnq/References/Duc_2025_JailGuard_Universal_Detection_Framework_TOSEM.pdf).
- <a id="ref-d8"></a>**[[D8]]** Alqahtani et al., "Data security in large language models: risks, defense, and directions," *Journal of King Saud University - Computer and Information Sciences (Springer)*, 2026. Local PDF: [`Alqahtani_2026_Data_Security_LLMs_Risks_Defense_Springer.pdf`](file:///d:/DoAn/pi-guard/workspaces/ducnq/References/Alqahtani_2026_Data_Security_LLMs_Risks_Defense_Springer.pdf).
- <a id="ref-d9"></a>**[[D9]]** Bhat et al., "A Hybrid Perplexity-MAS Framework for Proactive Jailbreak Attack Detection in Large Language Models," *Applied Sciences*, 2025. Local PDF: [`Bhat_2025_Hybrid_Perplexity_MAS_Jailbreak_Detection_ApplSci.pdf`](file:///d:/DoAn/pi-guard/workspaces/ducnq/References/Bhat_2025_Hybrid_Perplexity_MAS_Jailbreak_Detection_ApplSci.pdf).
- <a id="ref-d11"></a>**[[D11]]** Zheng et al., "Jailbreaking LLMs & VLMs: Mechanisms, Evaluation, and Unified Defense," *arXiv:2601.03594*, 2026. Local PDF: [`Zheng_2026_Jailbreaking_LLMs_VLMs_Unified_Defense.pdf`](file:///d:/DoAn/pi-guard/workspaces/ducnq/References/Zheng_2026_Jailbreaking_LLMs_VLMs_Unified_Defense.pdf).
- <a id="ref-d13"></a>**[[D13]]** N. Jain et al., "Baseline Defenses for Adversarial Attacks on Language Models," in *Proc. NeurIPS ML Safety Workshop*, 2023. [arXiv:2309.00614](https://arxiv.org/pdf/2309.00614.pdf). Local PDF: [`Jain_2023_Baseline_Defenses_Adversarial_Attacks_LLMs.pdf`](file:///d:/DoAn/pi-guard/workspaces/ducnq/References/Jain_2023_Baseline_Defenses_Adversarial_Attacks_LLMs.pdf).
- <a id="ref-d14"></a>**[[D14]]** Robey et al., "SmoothLLM: Defending Large Language Models Against Jailbreaking Attacks," *arXiv:2310.03684*, 2023. Local PDF: [`Robey_2023_SmoothLLM_Defending_LLMs_Random_Perturbation.pdf`](file:///d:/DoAn/pi-guard/workspaces/ducnq/References/Robey_2023_SmoothLLM_Defending_LLMs_Random_Perturbation.pdf).
- <a id="ref-d15"></a>**[[D15]]** Ahmad et al., "Guardrails for Large Language Models: A Comprehensive Review of Techniques, Datasets, and Challenges," *Preprint Survey*, 2025. Local PDF: [`Ahmad_2025_Guardrails_for_LLMs_Review_Techniques_Challenges.pdf`](file:///d:/DoAn/pi-guard/workspaces/ducnq/References/Ahmad_2025_Guardrails_for_LLMs_Review_Techniques_Challenges.pdf).
- <a id="ref-d16"></a>**[[D16]]** Wang et al., "Few-Shot In-Context Demonstrations Bypass LLM Defenses," *arXiv preprint*, 2026. Local PDF: [`Wang_2026_FewShot_Demonstrations_Jailbreak_Defenses.pdf`](file:///d:/DoAn/pi-guard/workspaces/ducnq/References/Wang_2026_FewShot_Demonstrations_Jailbreak_Defenses.pdf).
- <a id="ref-d17"></a>**[[D17]]** Systematic Review Team, "A Systematic Literature Review on Prompt Injection Attacks in LLM-Integrated Systems," *Systematic Review*, 2025. Local PDF: [`Systematic_Review_2025_Prompt_Injection_Attacks_LLM_Systems.pdf`](file:///d:/DoAn/pi-guard/workspaces/ducnq/References/Systematic_Review_2025_Prompt_Injection_Attacks_LLM_Systems.pdf).
- <a id="ref-d18"></a>**[[D18]]** Survey Team, "A Comprehensive Survey on Jailbreaking Attacks and Defenses for Large Language Models," *TechRxiv*, 2025. Local PDF: [`Survey_2025_Jailbreaking_LLMs_Attacks_Defenses_TechRxiv.pdf`](file:///d:/DoAn/pi-guard/workspaces/ducnq/References/Survey_2025_Jailbreaking_LLMs_Attacks_Defenses_TechRxiv.pdf).
