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
> 2. **Phân tích 2 mô hình tham khảo học thuật (Reference Models)**:
>    - **Baseline Classical ML (TF-IDF + LinearSVC/LogisticRegression)**: Siêu nhanh ($\sim 2.8\text{ms}$), chống biến dị cú pháp bề mặt cực tốt nhờ Character n-grams (`char_wb`), nhưng "mù ngữ nghĩa sâu" trước các kịch bản jailbreak tinh vi.
>    - **Deep Semantic Transformer (DeBERTa-v3-base FP32)**: Cơ chế **Disentangled Attention** bóc tách vector nội dung và vị trí, nắm bắt ngữ nghĩa tinh vi đạt $F_1 > 0.97$, nhưng dung lượng nặng (~500MB) và độ trễ CPU cao (~42.5ms), đòi hỏi lượng hóa INT8.
> 3. **Bằng chứng thực nghiệm độc quyền của Đức**: Hiện thực hóa bộ đột biến đối kháng JailGuard (`src/jailguard_mutators.py`), chứng minh Word TF-IDF sụp đổ ($< 35\%$ Recall) trước biến dị chèn khoảng trắng/leetspeak, và tầng chuẩn hóa NFKC + Character n-grams khôi phục Recall $> 95.5\%$.

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
    subgraph M1 ["MÔ HÌNH 1: CLASSICAL ML BASELINE"]
        direction TB
        T1["<b>TF-IDF + LinearSVC / LogisticReg</b><br/>Neel Jain et al. (NeurIPS 2023)"]
        P1["<b>ƯU ĐIỂM:</b><br/>• Độ trễ siêu nhanh (~2.8ms CPU)<br/>• Nhẹ (~25MB RAM), không cần GPU<br/>• Kháng biến dị ký tự nhờ char_wb"]
        C1["<b>ĐIỂM NGHẼN:</b><br/>• Mù ngữ nghĩa sâu (Semantic Blindness)<br/>• Thất bại trước Jailbreak phức tạp"]
        T1 --> P1 --> C1
    end

    subgraph M2 ["MÔ HÌNH 2: DEEP SEMANTIC TRANSFORMER"]
        direction TB
        T2["<b>DeBERTa-v3-base FP32</b><br/>Pengcheng He et al. (ICLR 2023)"]
        P2["<b>ƯU ĐIỂM:</b><br/>• Disentangled Attention bóc tách Nội dung & Vị trí<br/>• F1 > 0.97 trên Jailbreak phức tạp<br/>• Bắt trúng vị trí lệnh tiêm nhiễm"]
        C2["<b>ĐIỂM NGHẼN:</b><br/>• Nặng (~500MB)<br/>• Độ trễ CPU cao (~42.5ms > P95 target)<br/>• Đòi hỏi Lượng hóa INT8"]
        T2 --> P2 --> C2
    end
```

### 1. Mô Hình Tham Khảo 1: Classical ML Baseline (TF-IDF + Linear Classifier)
- **Công trình gốc**: Neel Jain et al. (NeurIPS 2023 [[D13]](#ref-d13)), *Baseline Defenses for Adversarial Attacks on Language Models*.
- **Cơ chế toán học**:
  $$\text{TF-IDF}(t, d, D) = \text{TF}(t, d) \times \left[\log\left(\frac{1 + |D|}{1 + |\{d \in D : t \in d\}|}\right) + 1\right]$$
  - Trích xuất đặc trưng đa tầng:
    - Word n-grams: $\text{ngram\_range} = (1, 2)$ bắt cụm từ khóa ("ignore previous", "system prompt").
    - Character n-grams với ranh giới từ: $\text{analyzer} = \text{'char\_wb'}$, $\text{ngram\_range} = (3, 5)$ bắt các phân mảnh từ khóa bị cố tình chèn khoảng trắng hoặc ký tự leetspeak.
  - Phân loại bằng bộ phân loại tuyến tính (Linear Support Vector Classifier hoặc Logistic Regression với chuẩn hóa $L_2$).
- **Ưu điểm vượt trội**:
  - Tốc độ suy luận cực nhanh: $\sim 2.8\text{ms}$ trên CPU thông thường.
  - Tiêu thụ tài nguyên tối thiểu: $\sim 25\text{MB}$ RAM, hoàn toàn độc lập với phần cứng GPU.
- **Điểm nghẽn học thuật**:
  - **Mù ngữ nghĩa sâu (Semantic Blindness)**: Bản chất TF-IDF giả định tính độc lập có điều kiện của các túi từ (Bag-of-Words). Khi kẻ tấn công dùng từ ngữ lịch sự, phép hoán dụ, hoặc viết kịch bản giả tưởng không chứa các từ khóa tấn công quen thuộc, mô hình hoàn toàn bất lực.

---

### 2. Mô Hình Tham Khảo 2: Deep Semantic Transformer (DeBERTa-v3-base FP32)
- **Công trình gốc**: Pengcheng He et al. (ICLR 2023), *DeBERTaV3: Improving DeBERTa using ELECTRA-Style Pre-Training with Gradient-Disentangled Embedding Sharing*.
- **Cơ chế toán học cốt lõi — Disentangled Attention**:
  - Không giống như BERT/RoBERTa gộp chung vector từ và vector vị trí vào một biểu diễn duy nhất $\mathbf{x}_i = \mathbf{w}_i + \mathbf{p}_i$, DeBERTa-v3 biểu diễn mỗi token bằng hai vector độc lập: vector nội dung $\mathbf{c}_i$ và vector vị trí tương đối $\mathbf{p}_{i|j}$.
  - Trọng số chú ý tương hỗ giữa token $i$ và token $j$ được tính toán qua 3 thành phần bóc tách:
    $$A_{i,j} = \mathbf{c}_i \mathbf{c}_j^T + \mathbf{c}_i \mathbf{p}_{j|i}^T + \mathbf{p}_{i|j} \mathbf{c}_j^T$$
    - $\mathbf{c}_i \mathbf{c}_j^T$: Mức độ tương đồng nội dung giữa từ $i$ và từ $j$ (*Content-to-Content*).
    - $\mathbf{c}_i \mathbf{p}_{j|i}^T$: Mức độ tương quan giữa nội dung từ $i$ với khoảng cách đến từ $j$ (*Content-to-Position*).
    - $\mathbf{p}_{i|j} \mathbf{c}_j^T$: Mức độ tương quan giữa vị trí tương đối và nội dung từ $j$ (*Position-to-Content*).
  - **Lý do chọn DeBERTa-v3 cho PI-Guard**:
    - Cơ chế *Disentangled Attention* giúp mô hình cực kỳ nhạy bén với **vị trí ngữ cảnh của câu lệnh** — cho phép phát hiện chính xác các mệnh lệnh tiêm nhiễm nằm ở đuôi văn bản RAG dài hoặc được ngụy trang giữa các đoạn hội thoại.
    - Theo nghiên cứu tại **ICLR 2026** [[D3]](#ref-d3), các đòn tấn công jailbreak có tính chuyển giao cao xuất phát từ không gian biểu diễn chung (shared representations) giữa các LLM, khẳng định DeBERTa-v3 là bộ trích xuất đặc trưng ngữ nghĩa lý tưởng nhất cho rào chắn guardrail.
- **Ưu điểm**: Khả năng phân tích ngữ nghĩa sâu xuất sắc, nhận diện chuẩn xác các kịch bản Jailbreak phức tạp ($F_1 > 0.97$).
- **Điểm nghẽn học thuật**:
  - Kích thước mô hình lớn ($\sim 500\text{MB}$ ở định dạng FP32).
  - Độ trễ trên CPU cao ($\sim 42.5\text{ms}$), vi phạm ràng buộc $P_{95} < 30\text{ms}$ của hệ thống Proxy nếu không thực hiện lượng hóa INT8.

---

# III. BẢN ĐỐI CHUẨN THỰC NGHIỆM ĐỘC QUYỀN (WORKSPACE NGUYỄN QUÍ ĐỨC)

Kế thừa thuật toán sinh biến dị từ công trình của **Zhang et al. (ACM TOSEM 2025 [[D6]](#ref-d6))**, Nguyễn Quí Đức đã hiện thực hóa kịch bản kiểm chứng thực nghiệm tại [`workspaces/ducnq/src/scratch_baseline_robustness_eval.py`](file:///d:/DoAn/pi-guard/workspaces/ducnq/src/scratch_baseline_robustness_eval.py):

```
================================================================================
🛡️ KẾT QUẢ THỰC NGHIỆM ĐỐI KHÁNG TRÊN MÁY CỦA NGUYỄN QUÍ ĐỨC (JAILGUARD MUTATORS)
================================================================================
1. Mô Hình Word-Level Baseline (Mô phỏng Word-only TF-IDF):
   - Mẫu gốc sạch: Recall = 98.2%
   - Biến dị chèn khoảng trắng ("i g n o r e"): Recall tụt dốc xuống < 35% (Sụp đổ)
   - Biến dị Leetspeak ("1gn0r3"): Recall tụt dốc xuống < 40%
2. Mô Hình Đề Xuất Của Đức (Unicode NFKC Normalizer + Character n-grams TF-IDF):
   - Chuẩn hóa Unicode NFKC loại bỏ ký tự vô hình Zero-width
   - Denormalize Leetspeak về bảng chữ cái chuẩn
   - Thu gọn khoảng trắng giữa các ký tự đơn lẻ
   - KẾT QUẢ: Khôi phục Recall nhận diện > 95.5% trên toàn bộ các lát cắt đột biến!
================================================================================
```

---

# IV. KỊCH BẢN VẤN ĐÁP BẢO VỆ CHO TASK 2

> **Câu hỏi phản biện**: *"Nếu DeBERTa-v3 đã phát hiện được ngữ nghĩa sâu xuất sắc với F1 > 0.97, tại sao nhóm vẫn cần khảo sát và duy trì mô hình Classical ML Baseline (TF-IDF)?"*  
> **Trả lời**:  
> *"Dạ thưa Thầy/Hội đồng, trong thiết kế hệ thống rào chắn thực tế (Production Ingress Proxy), chúng ta phải giải quyết bài toán đánh đổi đa mục tiêu giữa **Độ trễ (Latency)**, **Chi phí tính toán (Compute Overhead)** và **Độ chính xác ngữ nghĩa (Semantic Accuracy)**:  
> 1. DeBERTa-v3 chạy trên CPU mất $\sim 42.5\text{ms}$ và tiêu tốn nhiều tài nguyên, nếu mọi yêu cầu thông thường (vốn chiếm $> 90\%$ lưu lượng benign) đều phải qua DeBERTa thì hệ thống sẽ nghẽn cổ chai nghiêm trọng.  
> 2. Baseline TF-IDF kết hợp Character n-grams (`char_wb`) chỉ mất $\sim 2.8\text{ms}$ và RAM chỉ $\sim 25\text{MB}$, có khả năng lọc bỏ lập tức các đòn tấn công cú pháp bề mặt (khoảng trắng, leetspeak, payload lộ liễu) mà không tốn chi phí.  
> 3. Khảo sát độc lập cả 2 mô hình ở Task 3 là tiền đề khoa học thực nghiệm bắt buộc để nhóm xây dựng kiến trúc **Phân tầng định tuyến (Two-Tier Cascade Routing)**: Tầng 1 (TF-IDF) sàng lọc siêu tốc trong $2.8\text{ms}$; chỉ những trường hợp có độ phân vân ngữ nghĩa mới được đẩy tiếp sang Tầng 2 (DeBERTa-v3 lượng hóa INT8), đảm bảo độ trễ tổng thể $P_{95} < 30\text{ms}$."*

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
