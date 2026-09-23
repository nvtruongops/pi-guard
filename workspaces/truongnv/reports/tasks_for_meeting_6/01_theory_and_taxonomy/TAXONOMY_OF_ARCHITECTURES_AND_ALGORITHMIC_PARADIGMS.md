# BÁO CÁO KHOA HỌC: BẢN CHẤT KIẾN TRÚC & TRƯỜNG PHÁI THUẬT TOÁN TRONG CÁC TÀI LIỆU THAM KHẢO PI-GUARD
## Giải Mã Khoảng Cách Trừu Tượng (The Abstraction Gap): Tại Sao 41 Công Trình Khoa Học Hội Tụ Thành 6 Họ Kiến Trúc & 7 Trường Phái Thuật Toán

---

> **Đơn vị thực hiện**: Đồ án Tốt nghiệp Kỹ sư An toàn Thông tin (IAP491) — Đại học FPT  
> **Đề tài**: *A Machine-Learning Guardrail for Detecting Prompt Injection and Jailbreak Attacks on LLM Applications (PI-Guard)*  
> **Tài liệu tham chiếu gốc**: [`workspaces/truongnv/References/REFERENCES_LOG.md`](file:///d:/Work/Do-an/workspaces/truongnv/References/REFERENCES_LOG.md)  
> **Nguyên tắc học thuật**: Tuân thủ nghiêm ngặt mô hình Phân định 4 tầng (Four-Tier Provenance), Bộ thuật ngữ phòng thủ học thuật (Academic Defense Terminology Blacklist) và Chuẩn mực nghiên cứu An toàn Thông tin (Information Assurance - IA).

---

## 📌 TÓM TẮT ĐIỀU HÀNH (EXECUTIVE SUMMARY)

Một câu hỏi mang tính phản biện cốt lõi thường được đặt ra trước Hội đồng Chấm đồ án Tốt nghiệp là:
> *"Trong kho tài liệu của nhóm có tới 41 công trình khoa học được lập chỉ mục và phân tích chuyên sâu, nhưng tại sao khi tổng hợp về mặt kỹ thuật, nhóm lại khẳng định toàn bộ hệ sinh thái này chỉ hội tụ về **6 Họ Mô hình Kiến trúc** và **7 Trường phái Thuật toán**? Liệu có sự tinh giản chủ quan hay thiếu sót các mô hình trong các bài báo hay không?"*

Báo cáo này giải quyết triệt để câu hỏi trên thông qua việc phân tích **Khoảng cách Trừu tượng (The Abstraction Gap)** và **Quy luật Phân rã Chức năng (Functional Decomposition)** của một hệ thống an ninh AI hoàn chỉnh. Trong 41 bài báo khoa học:
1. **25 bài báo không phải là mô hình phòng thủ (Defensive Models)**: Chúng thuộc về các nhóm *Nghiên cứu cơ chế tấn công (Attack Mechanics & Threat Studies)*, *Nguyên lý thiết kế an toàn hệ thống (System & Security Principles)*, *Bộ dữ liệu đối chuẩn thực nghiệm (Benchmark Datasets & Surveys)* hoặc *Nghiên cứu bị loại trừ có kiểm chứng vì vi phạm ranh giới chuyên ngành (Out-of-Scope / IA Invariant)*.
2. **16 bài báo còn lại đề xuất hoặc khảo sát trực tiếp các giải pháp phòng thủ**: Khi bóc tách bản chất toán học của không gian biểu diễn (Feature Space), cơ chế trích xuất đặc trưng (Feature Extraction) và hàm mục tiêu suy diễn (Inference Objective), toàn bộ các giải pháp này phân rã chính xác thành **6 Họ Mô hình Kiến trúc** và vận hành dựa trên **7 Trường phái Thuật toán cốt lõi**.
3. **Đóng góp của PI-Guard**: Không cố gắng tạo ra một "siêu mô hình đơn khối" (Monolithic Hyper-Model Fallacy), PI-Guard kế thừa có chọn lọc các thuật toán ưu việt nhất từ các bài báo nền tảng, tích hợp chúng vào kiến trúc phân tầng thích ứng **Two-Tier Adaptive Cascade**, đạt điểm cân bằng Pareto tối ưu giữa độ trễ cực thấp (P95 $< 30\text{ms}$ trên CPU), tỷ lệ báo động giả nghiêm ngặt ($\text{FPR} < 1.5\%$) và độ nhạy phát hiện cao ($F_1 > 0.95$).

```
┌────────────────────────────────────────────────────────────────────────────────────────────────┐
│                   HỆ SINH THÁI 41 CÔNG TRÌNH KHOA HỌC (REFERENCES_LOG.md)                     │
└───────────────────────────────────────────────┬────────────────────────────────────────────────┘
                                                │
                 ┌──────────────────────────────┴──────────────────────────────┐
                 ▼                                                             ▼
┌────────────────────────────────────────────────┐            ┌──────────────────────────────────┐
│      25 BÀI BÁO PHỤC VỤ HẠ TẦNG KHOA HỌC       │            │  16 BÀI BÁO ĐỀ XUẤT/KHẢO SÁT     │
│  (Không đề xuất giải pháp guardrail độc lập)   │            │        GIẢI PHÁP PHÒNG THỦ       │
├────────────────────────────────────────────────┤            ├──────────────────────────────────┤
│ • 11 Bài: Nghiên cứu tấn công & Mô hình đe dọa │            │ Bóc tách bản chất biểu diễn      │
│ • 6 Bài: Nguyên lý an ninh & Cơ sở lý thuyết   │            │ và không gian tham số:           │
│ • 6 Bài: Tập dữ liệu Benchmark & Khảo sát SOTA │            │                                  │
│ • 2 Bài: Loại trừ ngoài phạm vi (Hardware/White)│           │                                  │
└────────────────────────────────────────────────┘            └────────────────┬─────────────────┘
                                                                               │
                                       ┌───────────────────────────────────────┴─────────────────┐
                                       ▼                                                         ▼
                     ┌───────────────────────────────────┐                     ┌───────────────────────────────────┐
                     │         6 HỌ MÔ HÌNH KIẾN TRÚC    │                     │     7 TRƯỜNG PHÁI THUẬT TOÁN      │
                     ├───────────────────────────────────┤                     ├───────────────────────────────────┤
                     │ 1. Heuristic & Regex Scrubber     │                     │ 1. Sublinear TF-IDF + Platt Calib │
                     │ 2. Classical Sparse Statistical ML│                     │ 2. Windowed Perplexity Filter     │
                     │ 3. Dense Metric Learning / k-NN   │                     │ 3. Dense Proximity Metric Embed   │
                     │ 4. Absolute-Position Transformers │                     │ 4. Disentangled Attention + MOF   │
                     │ 5. Disentangled Modern Encoders   │                     │ 5. Randomized Smoothing (Smooth)  │
                     │ 6. Autoregressive Generative SLMs │                     │ 6. Minimax Adversarial Game Theory│
                     │                                   │                     │ 7. Conformal Risk Control (CRC)   │
                     └───────────────────────────────────┘                     └───────────────────────────────────┘
```

---

## 🔍 1. GIẢI MÃ KHOẢNG CÁCH TRỪU TƯỢNG (THE ABSTRACTION GAP)

### 1.1. Bản Chất của một Đồ Án An Toàn Thông Tin (IA vs. Pure ML)
Trong ngành An toàn Thông tin (Information Assurance), một giải pháp phòng ngự không bắt đầu bằng việc chọn bừa một mô hình học máy. Một công trình nghiên cứu hoàn chỉnh bắt buộc phải cấu thành từ 4 trụ cột học thuật:
1. **Mô hình Mối đe dọa & Bề mặt Tấn công (Threat Modeling & Attack Surface)**: Định nghĩa kẻ thù là ai, tấn công qua kênh nào, các biến thái cú pháp và ngữ nghĩa ra sao.
2. **Hệ Tiên đề & Nguyên lý Bảo mật (Security Axioms & Architectural Principles)**: Xác định vị trí đặt chốt chặn, cơ chế kiểm soát toàn diện và phân quyền.
3. **Bộ Dữ liệu Đo kiểm & Chuẩn Đánh giá (Evaluation Benchmarks & Metrics)**: Môi trường thử lửa độc lập, khách quan để đo lường độ bền vững.
4. **Cơ chế Phát hiện & Thuật toán Phòng thủ (Detection Models & Defense Algorithms)**: Các kỹ thuật toán học và mô hình thực thi nhiệm vụ phân loại.

### 1.2. Phân Rã Chức Năng 41 Bài Báo Trong `REFERENCES_LOG.md`
Khi phân tích 41 bài báo có trong kho lưu trữ cục bộ của đề tài, sự phân bổ chức năng diễn ra như sau:

| Nhóm Chức Năng Khoa Học | Số Lượng | Danh Sách Bài Báo & Mã Tham Chiếu | Vai Trò Học Thuật Cụ Thể (Tier 1 & Tier 2) |
| :--- | :---: | :--- | :--- |
| **Nhóm A: Nghiên cứu Tấn công & Bề mặt Mối đe dọa (Threat Studies)** | **11** | `[3]` Perez (2022), `[4]` Greshake (2023), `[5]` Wei (2023), `[11]` Shen (2024), `[12]` Zhou (2024), `[13]` Zou (2023), `[17]` Yuan (2024), `[31]` Hackett (2025), `[35]` Deng (2024), `[39]` Russinovich (2024), `[40]` Zhou (2026) | Định nghĩa các vector tấn công: Direct Prompt Injection, Indirect Prompt Injection, Alignment Failure, DAN In-the-wild, Mutation Fuzzing, Adversarial Suffixes GCG, Ciphers, Unicode/Emoji Evasion, Multilingual Jailbreak, Multi-turn Crescendo, Context Window Overflow. **Không đề xuất bộ phân loại bảo vệ**. |
| **Nhóm B: Nguyên lý An ninh & Cơ sở Lý thuyết (Axioms & Principles)** | **6** | `[1]` Zhao (2023), `[2]` Ouyang (2022), `[6]` Tencent (2026), `[16]` Saltzer & Schroeder (1975), `[33]` Wallace / OpenAI (2024), `[41]` Luo & Han / NUS (2026) | Cung cấp hệ tiên đề: Không gian token phẳng, Cạnh tranh chỉ thị (RLHF), Phân vùng kiểm soát Zone 0, Complete Mediation & Economy of Mechanism, Instruction Hierarchy, Định lý bác bỏ siêu mô hình đơn khối (CASCADE). |
| **Nhóm C: Tập Dữ Liệu Đối Chuẩn & Khảo Sát SOTA (Benchmarks & Surveys)** | **6** | `[23]` Yi / BIPIA (2024), `[24]` Wang / Do-Not-Answer (2023), `[26]` Xu / ACL Survey (2024), `[27]` Liu & Hu / Zscaler (2024), `[28]` Yi / Tsinghua Survey (2024), `[34]` Chao / JailbreakBench (2024) | Đóng vai trò là tập dữ liệu kiểm thử ngoại lai (OOD Evaluation Datasets), phân loại taxonomy rủi ro và khảo sát toàn cảnh hệ sinh thái. |
| **Nhóm D: Nghiên cứu Loại trừ Ngoài Phạm Vi (Out-of-Scope Invariants)** | **2** | `[22]` Yao / ZeroQuant (NeurIPS 2022), `[29]` Yang / RAP-ID (ACL 2026) | **Loại trừ có cơ sở khoa học**: `[22]` là kỹ thuật lượng hóa phần cứng (không thuộc đóng góp IA); `[29]` đòi hỏi trích xuất activation white-box (vi phạm kiến trúc Black-Box Ingress Proxy). |
| **Nhóm E: Mô Hình & Thuật Toán Phòng Thủ Thực Sự (Defense Guardrails)** | **16** | `[7]` Meta Llama Guard, `[8]` NeMo Guardrails, `[9]` DeBERTa-v3, `[10]` OpenAI Content Detection, `[14]` SmoothLLM, `[15]` Baseline Defenses, `[18]` InjecGuard / PIGuard, `[19]` InstructDetector, `[20]` Prompt Guard 86M, `[21]` Ayub CAMLIS, `[25]` JailGuard, `[30]` PromptShield, `[32]` DataSentinel, `[36]` Conformal Risk Control, `[37]` ModernBERT, `[38]` Granite Guardian | **Đây là 16 công trình thực sự chứa đựng kiến trúc mô hình và thuật toán bảo vệ**. |

Như vậy, từ **41 công trình khoa học**, chỉ có đúng **16 công trình** thực sự đề xuất hoặc thử nghiệm các mô hình và thuật toán phòng thủ. Khi phân tích sâu vào cấu trúc tầng ẩn (hidden layers), hàm kích hoạt (activation functions) và nguyên lý tối ưu hóa toán học của 16 công trình này, chúng thu gọn chính xác thành **6 Họ Mô hình Kiến trúc** và vận hành trên **7 Trường phái Thuật toán**.

---

## 🏛️ 2. BẢN CHẤT 6 HỌ MÔ HÌNH KIẾN TRÚC TRONG HỆ THỐNG PHÒNG THỦ LLM

Hệ thống phân loại dưới đây phân định rõ bản chất vật lý, cơ chế trích xuất đặc trưng và sự đánh đổi tài nguyên (Resource Trade-offs) của 6 họ mô hình xuất hiện trong y văn:

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              PHỔ ĐÁNH ĐỔI GIỮA ĐỘ TRỄ SUY DIỄN VÀ NĂNG LỰC NGỮ NGHĨA SÂU                              │
│                                                                                                                        │
│  [Họ 1] Rules/Regex    ───> [Họ 2] Sparse ML   ───> [Họ 3] Metric/k-NN ───> [Họ 5] DeBERTa-v3  ───> [Họ 6] Gen SLMs   │
│  P95: < 0.5ms               P95: 1 - 2.5ms          P95: 5 - 12ms           P95: 15 - 28ms           P95: 400 - 2500ms │
│  Bộ nhớ: ~2 MB              Bộ nhớ: ~40 MB          Bộ nhớ: ~120 MB         Bộ nhớ: ~450 MB          Bộ nhớ: 4 - 16 GB │
│  Ngữ nghĩa: Không           Ngữ nghĩa: Cú pháp/Ngram Ngữ nghĩa: Vector phẳng Ngữ nghĩa: Disentangled Ngữ nghĩa: Tự sinh│
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Bảng Đối Soánh Tổng Quan 6 Họ Mô Hình

| Tiêu Chí Kỹ Thuật | Họ 1: Heuristic & Regex Scrubber | Họ 2: Classical Sparse Statistical ML | Họ 3: Dense Metric Learning & Proximity | Họ 4: Absolute-Position Discriminative Encoders | Họ 5: Disentangled & Modern Deep Encoders | Họ 6: Autoregressive Generative Safety SLMs |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Công trình tiêu biểu** | `[16]` Saltzer, `[17]` Yuan, `[31]` Hackett | `[15]` Jain, `[21]` Ayub, `[16]` Saltzer | `[21]` Ayub & Majumdar (CAMLIS 2024) | `[15]` Jain (BERT/RoBERTa), BERT NAACL | `[9]` DeBERTaV3, `[18]` InjecGuard, `[20]` PromptGuard, `[37]` ModernBERT | `[7]` Llama Guard 3, `[8]` NeMo, `[38]` Granite Guardian |
| **Không gian đầu vào** | Ký tự thô & Chuỗi byte | Vector thưa $V \in \mathbb{R}^{50000}$ (TF-IDF) | Vector nhúng dày $e \in \mathbb{R}^{384}$ | Chuỗi Token $T \le 512$ + Absolute Pos | Chuỗi Token $T \le 512$ / $8192$ + Relative Pos | Chuỗi Prompt + System Guidelines ($T \le 4096$) |
| **Bản chất tính toán** | Khớp mẫu chuỗi DFA / Aho-Corasick | Tích vô hướng tuyến tính $w^\top x + b$ | Tích vô hướng Cosine / Khoảng cách Mahalanobis | Transformer Encoder (MHA chuẩn) | Disentangled Attention (Content $\perp$ Position) | Autoregressive Decoder (Causal Self-Attention) |
| **Độ trễ P95 (CPU)** | **$< 0.5\text{ ms}$** | **$1.0 - 2.5\text{ ms}$** | **$5.0 - 12.0\text{ ms}$** | $25.0 - 45.0\text{ ms}$ | **$15.0 - 28.0\text{ ms}$** (ModernBERT $\approx 16\text{ms}$) | **$450 - 2,500\text{ ms}$** |
| **Dung lượng RAM** | $< 5\text{ MB}$ | $\approx 40\text{ MB}$ | $\approx 120\text{ MB}$ | $\approx 420\text{ MB}$ | $\approx 450\text{ MB}$ | $4,500 - 16,000\text{ MB}$ |
| **FPR trên văn bản lành tính** | Tốt trên từ khóa, tê liệt với ẩn dụ | Cao ($10 - 15\%$) nếu dùng đơn lẻ | Rất cao ($12 - 18\%$) trên miền mở | Trung bình ($4 - 7\%$) do lệch từ khóa | **Thấp ($\le 1.5\%$) khi hiệu chuẩn** | Rất thấp ($< 1.0\%$) nhưng over-refusal cao |
| **Điểm yếu chí mạng** | Bị vượt qua bởi Leetspeak, Cipher, Diacritics | Mù hoàn toàn trước cấu trúc đảo ngữ | Nhạy cảm với trôi dạt phân phối (Domain Drift) | Suy giảm chú ý khi chuỗi dài, dính Trigger Bias | Chi phí suy luận cao gấp 15x so với Họ 2 | Độ trễ không khả thi cho Ingress Proxy độ trễ thấp (P95 < 30ms) |
| **Vai trò trong PI-Guard** | **Tầng 0 (Tiền xử lý)** | **Tầng 1 (Bộ lọc nhanh Fast-Filter)** | Đối chuẩn thực nghiệm (Rejected Baseline) | Đối chuẩn lịch sử (Baseline) | **Tầng 2 (Mô hình Ngữ nghĩa Sâu Cốt lõi)** | Đối chuẩn ngoài biên (Out-of-line Arbiter) |

---

### Phân Tích Chuyên Sâu Từng Họ Mô Hình

#### 1. Họ 1: Heuristic & Regex Pattern Scrubber (Lớp Tiền Xử Lý Chuẩn Hóa Cú Pháp)
- **Bản chất toán học**: Máy trạng thái hữu hạn tiền định (Deterministic Finite Automata - DFA).
- **Cơ chế**: Quét chuỗi tìm các mẫu ký tự đặc thù dựa trên tập biểu thức chính quy (Regular Expressions), bảng giải mã tiền trạm (Base64, Hex, URL-encoding, ROT13, Leetspeak) và chuẩn hóa Unicode (NFKC).
- **Ưu điểm**: Thực thi với độ phức tạp thời gian tuyến tính $O(N)$ theo độ dài văn bản; độ trễ suy diễn cực nhỏ ($< 0.5\text{ms}$); không yêu cầu bộ nhớ GPU.
- **Hạn chế**: Cực kỳ dễ vỡ trước các đòn biến dị ký tự nâng cao, phép ẩn dụ ngôn ngữ và hoàn toàn không có khả năng hiểu ngữ nghĩa văn cảnh.
- **Đóng góp y văn & Vị trí trong đề tài**: Được bảo chứng bởi Saltzer & Schroeder `[16]` (nguyên lý *Economy of Mechanism*), Yuan et al. `[17]` (hóa giải CipherChat) và Hackett et al. `[31]` (chặn đứng Unicode Tags / Emoji Smuggling). Trong PI-Guard, đây là **Tầng 0 (Heuristic Scrubber)**.

#### 2. Họ 2: Classical Sparse Statistical ML (Bộ Phân Loại Học Máy Thống Kê Thưa)
- **Bản chất toán học**: Chiếu văn bản vào không gian vector đặc trưng thống kê tần suất cao chiều (Bag-of-Words, Character $n$-grams, Word $n$-grams) và phân tách bằng siêu phẳng tuyến tính tối ưu (Linear Hyperplane):
  $$f(x) = \text{sign}(\mathbf{w}^\top \phi(x) + b)$$
- **Mô hình đại diện**: TF-IDF kết hợp Logistic Regression (với chuẩn hóa $L_2$), Linear Support Vector Machines (LinearSVC) hoặc Naive Bayes.
- **Ưu điểm**: Tốc độ suy luận đạt kỷ lục ($1.0 - 2.5\text{ms}$ trên CPU); khả năng bắt dính tuyệt vời các đoạn mã đối kháng lặp từ, ký tự dị thường nhờ Character $n$-grams (`char_wb`).
- **Hạn chế**: Không gian vector phân tán thưa không nắm bắt được mối quan hệ hoán vị vị trí từ, ngữ pháp phức tạp hoặc tấn công ngữ nghĩa tinh vi. Khi chạy đơn lẻ, tỷ lệ báo động giả (FPR) trên văn bản lành tính lên tới $10 - 15\%$ (được chứng minh trong nghiên cứu của Ayub `[21]`).
- **Đóng góp y văn & Vị trí trong đề tài**: Được lấy cảm hứng từ Jain et al. `[15]` (Baseline Defenses). Trong PI-Guard, đây là **Tầng 1 (Fast-Filter)** làm nhiệm vụ sàng lọc nhanh $70 - 80\%$ lưu lượng truy vấn rõ ràng.

#### 3. Họ 3: Dense Metric Learning & Proximity Classifiers (Bộ Phân Loại Không Gian Khoảng Cách Dày)
- **Bản chất toán học**: Sử dụng mô hình Bi-Encoder nhỏ (như `all-MiniLM-L6-v2`) để ánh xạ prompt vào không gian vector liên tục chiều thấp ($\mathbb{R}^{384}$), sau đó phân loại dựa trên khoảng cách hình học tới tâm cụm (Centroid) hoặc thuật toán $k$-láng giềng gần nhất ($k$-NN):
  $$\hat{y} = \arg\min_{c \in \{0, 1\}} \|\mathbf{e}_x - \boldsymbol{\mu}_c\|_2^2 \quad \text{hoặc} \quad \text{CosineSim}(\mathbf{e}_x, \boldsymbol{\mu}_c)$$
- **Mô hình đại diện**: Nghiên cứu CAMLIS 2024 của Ayub & Majumdar `[21]`.
- **Ưu điểm**: Kích thước mô hình gọn nhẹ ($\approx 80 - 120\text{MB}$); không cần huấn luyện lại toàn bộ mạng khi cập nhật thêm mẫu tấn công mới (chỉ cần thêm vector vào cơ sở dữ liệu vector).
- **Hạn chế**: Khoảng cách không gian cosine trong không gian vector phẳng bị nén ép, dễ xảy ra hiện tượng chồng lấn ranh giới (Hubness Problem). Kết quả thực nghiệm của nhóm chứng minh mô hình này đạt FPR $> 12\%$ trên tập kiểm thử mở rộng, không đáp ứng được yêu cầu kiểm soát $\text{FPR} < 1.5\%$.
- **Đóng góp y văn & Vị trí trong đề tài**: Đây là **Mô hình bị loại trừ có kiểm chứng (Academic Rejected Baseline)** trong Chuyên đề 5 và Báo cáo Meeting 5.

#### 4. Họ 4: Absolute-Positioning Discriminative Encoders (Transformer Cổ Điển Nhúng Vị Trí Tuyệt Đối)
- **Bản chất toán học**: Kiến trúc Transformer Encoder nguyên bản (BERT, RoBERTa), cộng vector nhúng vị trí tuyệt đối vào vector nhúng từ: $\mathbf{h}_i^{(0)} = \mathbf{e}_{w_i} + \mathbf{p}_i$.
- **Ưu điểm**: Khả năng nắm bắt ngữ cảnh 2 chiều (Bidirectional Context) vượt trội hơn hẳn các mô hình thống kê thưa.
- **Hạn chế**: Cơ chế cộng vị trí tuyệt đối làm mất tính tương đối giữa các từ khi prompt bị kéo dài hoặc thay đổi cấu trúc; dễ bị "nhiễm độc từ khóa" (Trigger Word Bias) dẫn đến việc một prompt chứa từ nhạy cảm trong ngữ cảnh học thuật bị chặn nhầm; hiệu quả tính toán kém hơn các kiến trúc encoder thế hệ mới.
- **Đóng góp y văn & Vị trí trong đề tài**: Xuất hiện trong các nghiên cứu đối chuẩn của Jain et al. `[15]` và được sử dụng làm **Baseline so sánh lịch sử** trong đề tài.

#### 5. Họ 5: Disentangled & Modern Deep Encoders (Transformer Tách Rời Biểu Diễn & Thế Hệ Mới)
- **Bản chất toán học**: Đột phá kiến trúc giải phóng mối liên kết cứng nhắc giữa nội dung và vị trí. Vector biểu diễn được phân tách thành hai luồng độc lập: ma trận nội dung và ma trận vị trí tương đối.
- **Mô hình đại diện**:
  - `DeBERTa-v3` (He et al., ICLR 2023 `[9]`): Cơ chế Disentangled Attention tính toán sự tương tác chéo giữa nội dung và vị trí tương đối qua 4 ma trận thành phần; huấn luyện bằng Replaced Token Detection (RTD) kiểu ELECTRA kết hợp Gradient-Disentangled Embedding Sharing (GDES).
  - `InjecGuard / PIGuard` (Li et al., ACL 2025 `[18]`): Tinh chỉnh DeBERTa-v3 bằng kỹ thuật Mitigating Over-defense for Free (MOF), loại bỏ định kiến kích hoạt từ khóa.
  - `Prompt Guard 86M` (Meta AI, 2024 `[20]`): Bộ phân loại nhúng nhẹ dựa trên `mDeBERTa-v3-base`.
  - `ModernBERT` (Warner et al., 2024 `[37]`): Tích hợp Rotary Position Embeddings (RoPE), GeGLU và FlashAttention-2, hỗ trợ native context 8,192 tokens.
- **Ưu điểm**: Năng lực phân loại ngữ nghĩa vượt trội; độ trễ P95 cực kỳ tối ưu cho CPU ($15 - 28\text{ms}$); không bị đánh lừa bởi vị trí hoán đổi của chỉ thị độc hại; kiểm soát $\text{FPR} < 1.5\%$ khi được hiệu chuẩn đúng.
- **Hạn chế**: Chi phí tài nguyên và độ trễ cao hơn khoảng 10–15 lần so với Họ 2, do đó nếu để xử lý $100\%$ lưu lượng Ingress sẽ gây nghẽn cổ chai tại các thời điểm lưu lượng truy vấn tăng đột biến.
- **Đóng góp y văn & Vị trí trong đề tài**: Đây là **Hạt nhân Khoa học Tầng 2 (Deep Semantic Classifier)** của đồ án PI-Guard.

#### 6. Họ 6: Autoregressive Generative Safety Models (Mô Hình Tự Hồi Quy Sinh Nhãn An Toàn - LLM-as-a-Judge)
- **Bản chất toán học**: Kiến trúc Decoder-only tự hồi quy (Causal Language Model) với số lượng tham số từ 2B đến 8B, sinh ra chuỗi token kết luận an toàn (Safe/Unsafe) kèm theo mã danh mục vi phạm:
  $$P(Y | X) = \prod_{t=1}^T P(y_t | y_{<t}, X, \text{SafetyTaxonomy})$$
- **Mô hình đại diện**: `Llama Guard 3 8B` (Meta `[7]`), `Granite Guardian 2B/8B` (IBM Research `[38]`), `NeMo Guardrails` (NVIDIA `[8]`).
- **Ưu điểm**: Khả năng suy luận ngữ cảnh sâu sắc nhất; có thể giải thích lý do tại sao prompt bị chặn (Interpretability); linh hoạt cập nhật chính sách an toàn chỉ bằng cách sửa System Prompt.
- **Hạn chế**: Độ trễ suy diễn cực lớn ($400 - 2,500\text{ms}$); tiêu tốn tài nguyên GPU khổng lồ; dễ bị tấn công bởi kỹ thuật Jailbreak gián tiếp nhắm vào chính mô hình thẩm phán. Hoàn toàn bất khả thi để làm Ingress Proxy đồng bộ xử lý lưu lượng trực tuyến.
- **Đóng góp y văn & Vị trí trong đề tài**: Đóng vai trò là **Mô hình Thẩm định Ngoài Biên (High-Assurance Arbiter)** trong các kịch bản ngoại tuyến hoặc đối chuẩn trần năng lực trong Chuyên đề 7.

---

## 🧮 3. BẢN CHẤT 7 TRƯỜNG PHÁI THUẬT TOÁN CỐT LÕI

Khi gạt bỏ lớp vỏ bọc tên gọi của các công cụ và framework, toàn bộ cơ chế phát hiện và ngăn chặn trong 16 bài báo phòng thủ đều vận hành dựa trên **7 Trường phái Thuật toán Cốt lõi** sau:

```
┌────────────────────────────────────────────────────────────────────────────────────────────────┐
│                           7 TRƯỜNG PHÁI THUẬT TOÁN PHÒNG THỦ TRONG Y VĂN                       │
├────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. Sublinear Term Projection & Platt Calibration  ───> Khai phá đặc trưng thống kê tần suất   │
│ 2. Sliding-Window Cross-Entropy & Perplexity      ───> Lọc chuỗi đối kháng ngẫu nhiên (GCG)   │
│ 3. Dense Metric Learning & Proximity Centroids    ───> Đo khoảng cách ngữ nghĩa hình học       │
│ 4. Disentangled Attention & Invariant Loss (MOF)  ───> Triệt tiêu định kiến từ khóa ngữ cảnh   │
│ 5. Randomized Smoothing & Majority Perturbation   ───> Làm mịn ngẫu nhiên & biểu quyết đa số   │
│ 6. Minimax Game-Theoretic Optimization            ───> Huấn luyện đối kháng cực tiểu cực đại   │
│ 7. Conformal Risk Control & Finite-Sample Bounds  ───> Bảo chứng toán học kiểm soát sai số FPR │
└────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### Thuật Toán 1: Sublinear Statistical Term Projection & Platt Scaling Calibration
- **Nguồn gốc học thuật**: Bắt nguồn từ lý thuyết Information Retrieval kinh điển (Luhn 1958, Spärck Jones 1972) và được Jain et al. `[15]` cùng Ayub `[21]` áp dụng cho bài toán an ninh LLM.
- **Cơ chế toán học**:
  1. *Biến đổi TF-IDF cận tuyến tính (Sublinear TF Scaling)* để triệt tiêu ảnh hưởng của các từ lặp lại bất thường:
     $$\text{TF}(t, d) = 1 + \ln(f_{t, d}) \quad \text{nếu } f_{t,d} > 0, \quad \text{IDF}(t) = \ln\left(1 + \frac{N}{\text{DF}(t)}\right)$$
  2. *Trích xuất đặc trưng đa tầng*: Kết hợp Word $n$-grams $(1, 2)$ và Character $n$-grams $(3, 5)$ với ranh giới từ vựng (`char_wb`), sinh ra không gian vector thưa $\mathbf{x} \in \mathbb{R}^D$ ($D \approx 50,000$).
  3. *Hiệu chuẩn xác suất Platt Scaling*: Chuyển đổi khoảng cách biên siêu phẳng $z = \mathbf{w}^\top \mathbf{x} + b$ thành xác suất hậu nghiệm chuẩn hóa:
     $$P(y=1 | z) = \frac{1}{1 + \exp(A \cdot z + B)}$$
     trong đó các tham số $A, B$ được tối ưu hóa qua hàm Cross-Entropy trên tập validation tách biệt.
- **Vai trò trong PI-Guard**: Vận hành tại **Tầng 1 (Fast-Filter)**, thực thi trong $1.2\text{ms}$ để phân loại nhanh các mẫu lành tính rõ ràng ($P < 0.15$) hoặc tấn công thô thiển rõ ràng ($P > 0.85$).

---

### Thuật Toán 2: Sliding-Window Cross-Entropy & Perplexity Filtering (PPL)
- **Nguồn gốc học thuật**: Jain et al. `[15]` (Baseline Defenses) và Zou et al. `[13]` (bẻ gãy thuật toán GCG).
- **Cơ chế toán học**:
  Đo lường mức độ "bất ngờ" của mô hình ngôn ngữ tham chiếu (như GPT-2 hoặc KenLM $n$-gram) trước chuỗi token $W = (w_1, w_2, \dots, w_N)$:
  $$\text{PPL}(W) = \exp\left( -\frac{1}{N} \sum_{i=1}^N \ln P(w_i \mid w_{<i}) \right)$$
  Đối với tài liệu dài, thuật toán áp dụng cửa sổ trượt (Sliding Window kích thước $k=32$, bước nhảy $s=16$) để phát hiện các cụm token có Perplexity dị thường:
  $$\text{PPL}_{\text{max}}(W) = \max_{j} \text{PPL}(w_{j : j+k})$$
- **Bản chất phòng ngự**: Các đòn tấn công tối ưu hóa gradient như Greedy Coordinate Gradient (GCG `[13]`) thường sinh ra các chuỗi hậu tố vô nghĩa đối với con người (như `! ! ! ! describing.\ +similarly here`), khiến chỉ số PPL vọt lên ngưỡng hàng nghìn.
- **Hạn chế**: Bị tê liệt hoàn toàn trước các đòn tấn công bằng ngôn ngữ tự nhiên trôi chảy (như DAN Jailbreak `[11]` hoặc Crescendo `[39]`).

---

### Thuật Toán 3: Dense Metric Learning & Semantic Proximity Centroids
- **Nguồn gốc học thuật**: Nghiên cứu CAMLIS 2024 của Ayub & Majumdar `[21]` và Wen et al. `[19]` (InstructDetector).
- **Cơ chế toán học**:
  Ánh xạ câu văn vào không gian Euclid chuẩn hóa bằng mạng Bi-Encoder $f_\theta$:
  $$\mathbf{z}_x = \frac{f_\theta(x)}{\|f_\theta(x)\|_2} \in \mathbb{S}^{d-1}$$
  Xây dựng ma trận tâm cụm đa tâm (Multi-Centroid Clustering) cho từng lớp nhãn độc hại $k \in \mathcal{K}$:
  $$\boldsymbol{\mu}_k^{(c)} = \frac{1}{|S_k^{(c)}|} \sum_{x \in S_k^{(c)}} \mathbf{z}_x$$
  Độ đo rủi ro được tính bằng khoảng cách Cosine cực tiểu tới các tâm độc hại:
  $$\text{RiskScore}(x) = \max_{k, c} \left( \mathbf{z}_x^\top \boldsymbol{\mu}_k^{(c)} \right)$$
- **Vai trò trong đề tài**: Được nhóm triển khai thực nghiệm độc lập làm baseline đối chuẩn; chứng minh tỷ lệ FPR cao do sự co cụm không gian vector trên các câu lệnh mệnh lệnh thông thường.

---

### Thuật Toán 4: Disentangled Representation Attention & Invariant Loss (MOF)
- **Nguồn gốc học thuật**: Đặt nền móng bởi He, Gao, Chen (ICLR 2023 `[9]`) và phát triển chuyên sâu cho an ninh bởi Li et al. (ACL 2025 `[18]`).
- **Cơ chế toán học**:
  1. *Cơ chế Chú ý Tách rời (Disentangled Attention)*: Ma trận Attention giữa hai token $i$ và $j$ được phân tách thành 3 thành phần độc lập (Content-to-Content, Content-to-Position, Position-to-Content):
     $$A_{i,j} = \mathbf{Q}_i^c \mathbf{K}_j^{c\top} + \mathbf{Q}_i^c \mathbf{K}_{\delta(i,j)}^{p\top} + \mathbf{K}_j^c \mathbf{Q}_{\delta(j,i)}^{p\top}$$
     trong đó $\delta(i, j)$ đại diện cho khoảng cách vị trí tương đối giữa token $i$ và $j$.
  2. *Hàm mất mát Bất biến Từ khóa (Mitigating Over-defense for Free - MOF Loss)*:
     Để ngăn ngừa mô hình phạt nhầm các truy vấn an toàn chứa từ khóa nhạy cảm (như *"Explain how SQL injection works"*), hàm mất mát bổ sung số hạng phân kỳ Kullback-Leibler giữa biểu diễn của prompt gốc $x$ và prompt đã được hoán đổi từ khóa trung tính $x_{\text{neutral}}$:
     $$\mathcal{L}_{\text{MOF}} = \mathcal{L}_{\text{CE}}(f_\theta(x), y) + \lambda \cdot \mathcal{D}_{\text{KL}}\left( \text{Softmax}(f_\theta(x_{\text{syn}})) \;\parallel\; \text{Softmax}(f_\theta(x_{\text{neutral}})) \right)$$
- **Vai trò trong PI-Guard**: Đây là **linh hồn thuật toán của Tầng 2**, giải quyết bài toán cốt lõi: phân biệt giữa *ý đồ tấn công thực sự* và *sự xuất hiện ngẫu nhiên của các từ khóa an ninh trong câu hỏi lành tính*.

---

### Thuật Toán 5: Randomized Smoothing & Majority Perturbation Voting
- **Nguồn gốc học thuật**: Robey et al. `[14]` (SmoothLLM) và Zhang et al. `[25]` (JailGuard, TOSEM 2025).
- **Cơ chế toán học**:
  Dựa trên lý thuyết độ bền vững chứng minh được (Certified Robustness). Với một prompt đầu vào $x$, tạo ra $M$ bản sao nhiễu bằng toán tử đột biến ngẫu nhiên $\mathcal{T}_\sigma$ (chèn, xóa, hoán đổi ký tự hoặc thay thế từ đồng nghĩa với xác suất $\sigma$):
  $$\tilde{x}^{(m)} = \mathcal{T}_\sigma(x), \quad m = 1, \dots, M$$
  Đưa toàn bộ $M$ bản sao qua bộ thẩm định cơ sở $f(x)$ và áp dụng luật biểu quyết đa số (Majority Voting):
  $$\hat{Y} = \arg\max_{c \in \{0, 1\}} \sum_{m=1}^M \mathbb{I}\left( f(\tilde{x}^{(m)}) = c \right)$$
- **Đánh giá trong đề tài**: Phương pháp này có độ bền rất cao trước các chuỗi tấn công đối kháng nhạy cảm với ký tự (như GCG), nhưng phải trả giá bằng việc nhân độ trễ lên gấp $M$ lần ($M \ge 10$), do đó không phù hợp làm Ingress Filter trực tiếp, nhưng được dùng làm công cụ sinh mẫu kiểm thử đối kháng (Fuzzing Suite).

---

### Thuật Toán 6: Game-Theoretic Minimax Adversarial Optimization
- **Nguồn gốc học thuật**: Liu et al. `[32]` (DataSentinel, IEEE S&P 2025).
- **Cơ chế toán học**:
  Mô hình hóa cuộc đối đầu giữa kẻ tấn công và hệ thống phòng thủ dưới dạng bài toán tối ưu hóa Minimax hai người chơi tổng bằng không (Zero-sum Game):
  $$\min_{\boldsymbol{\theta}} \max_{\boldsymbol{\delta} \in \Delta} \mathbb{E}_{(x, y) \sim \mathcal{D}} \left[ \mathcal{L}\left( f_{\boldsymbol{\theta}}(x \oplus \boldsymbol{\delta}), y \right) \right]$$
  1. *Pha tối đa hóa bên trong (Inner Maximization)*: Kẻ tấn công tìm kiếm nhiễu loạn đối kháng tối ưu $\boldsymbol{\delta}^*$ trong không gian biến dị cho phép $\Delta$ để tối đa hóa hàm mất mát phân loại (lừa guardrail coi tấn công là an toàn).
  2. *Pha cực tiểu hóa bên ngoài (Outer Minimization)*: Bộ bảo vệ cập nhật trọng số $\boldsymbol{\theta}$ để cực tiểu hóa sai số phân loại dưới các đòn tấn công xấu nhất đã được sinh ra.
- **Vai trò trong PI-Guard**: Cung cấp khung lý thuyết để nhóm xây dựng kịch bản kiểm thử bền vững và tạo sinh dữ liệu huấn luyện đối kháng (Adversarial Data Augmentation).

---

### Thuật Toán 7: Conformal Risk Control (CRC) & Tri-State Dynamic Calibration
- **Nguồn gốc học thuật**: Angelopoulos et al. `[36]`, kết hợp với triết lý Low-FPR của Jacob et al. `[30]` (PromptShield, ACM CCS 2024) và Markov et al. `[10]` (OpenAI).
- **Cơ chế toán học**:
  Thay vì chọn một ngưỡng cắt tĩnh $0.5$ theo cảm tính, Conformal Risk Control cung cấp một **bảo chứng thống kê hữu hạn mẫu (finite-sample statistical guarantee)**:
  Với mức ngân sách rủi ro $\alpha = 0.015$ (tương ứng $\text{FPR} \le 1.5\%$) và mức độ tin cậy $1 - \delta \ge 95\%$, xác định ngưỡng quyết định $\hat{\tau}$ trên tập hiệu chuẩn độc lập $\mathcal{D}_{\text{cal}} = \{(x_i, y_i)\}_{i=1}^n$ sao cho:
  $$\mathbb{P}\left( \mathbb{E}\left[ \ell(f(X; \hat{\tau}), Y) \right] \le \alpha \right) \ge 1 - \delta$$
  Từ đó, không gian quyết định của PI-Guard được phân chia thành 3 trạng thái rõ ràng (Tri-State Decision Engine):
  $$\text{Hành động}(x) = \begin{cases} 
  \mathbf{ALLOW} \quad (\text{Chuyển tiếp LLM tức thì}), & \text{nếu } P_{\text{risk}} < \tau_{\text{low}} \\
  \mathbf{ESCALATE} \quad (\text{Chuyển giao lên Tầng 2 Thẩm định}), & \text{nếu } \tau_{\text{low}} \le P_{\text{risk}} \le \tau_{\text{high}} \\
  \mathbf{BLOCK} \quad (\text{Ngắt kết nối & Ghi log cảnh báo}), & \text{nếu } P_{\text{risk}} > \tau_{\text{high}}
  \end{cases}$$
- **Vai trò trong PI-Guard**: Đây là **bảo chứng toán học tối thượng** giải thích tại sao kiến trúc 2 tầng của đề tài đạt được mục tiêu kép: vừa chặn đứng tấn công vừa bảo toàn trải nghiệm người dùng với $\text{FPR} < 1.5\%$.

---

## 📐 4. QUY TRÌNH SUY DẪN TOÁN HỌC & PHÂN RÃ KỸ THUẬT: TỪ CẤP VĨ MÔ SANG CẤP VI MÔ (6x7 ⟹ 12x14)

### 4.1. Bản Chất Mối Quan Hệ Giữa Cấp Vĩ Mô (6x7) và Cấp Vi Mô (12x14)

Trước Giảng viên Hướng dẫn hoặc Hội đồng Chấm Đồ án Tốt nghiệp, một câu hỏi phản biện mang tính bản chất học thuật là:
> *"Tại sao trong phân tích tổng quan, nhóm khẳng định 41 bài báo quy về **6 Họ Mô hình** và **7 Thuật toán** (Ma trận Vĩ mô 6x7), nhưng trong đánh giá kỹ thuật lại mở rộng thành **Ma trận Vi mô 12x14**? Hãy chứng minh quy trình suy dẫn từ 6x7 lên 12x14 một cách toán học và bảo toàn xuất xứ y văn!"*

Quy trình suy dẫn được hình thức hóa chặt chẽ như sau:
1. **Ma trận Vĩ mô (Macro-Level Taxonomy 6x7)**: Gom cụm theo *Không gian Biểu diễn toán học nền tảng (Fundamental Feature Spaces)* và *Nguyên lý tối ưu hóa cốt lõi*. Phù hợp cho thiết kế kiến trúc chiến lược theo tiêu chuẩn ISO/IEC/IEEE 42010 (ATAM) và NIST AI RMF 1.0.
2. **Ma trận Vi mô (Micro-Level Engineering Taxonomy 12x14)**: Phân rã chính xác từng họ vĩ mô thành các biến thể hiện thực cụ thể được y văn quốc tế nghiên cứu và kiểm thử độc lập, tương thích với các chuẩn đối chuẩn SOTA toàn cầu như **CASCADE (Luo & Han NUS 2026 [[41]](#ref41) — ma trận $19 \times 15$)** và **PromptShield (Jacob et al. UC Berkeley CCS 2024 [[30]](#ref30))**.
3. **Tính bảo toàn học thuật**: Tập hợp 12 mô hình vi mô $\mathcal{M}_{\text{Micro}} = \{M_1, \dots, M_{12}\}$ và 14 thuật toán vi mô $\mathcal{A}_{\text{Micro}} = \{A_1, \dots, A_{14}\}$ là các **phân hoạch chặt chẽ (Exact Partitions)** của 6 họ vĩ mô $\mathcal{F}_{\text{Macro}}$ và 7 trường phái vĩ mô $\mathcal{P}_{\text{Macro}}$:
   $$\mathcal{M}_{\text{Micro}} = \bigcup_{k=1}^6 \text{Decompose}(F_k) \quad \text{với} \quad \text{Decompose}(F_i) \cap \text{Decompose}(F_j) = \emptyset \quad (\forall i \neq j)$$
   $$\mathcal{A}_{\text{Micro}} = \bigcup_{k=1}^7 \text{Decompose}(P_k) \quad \text{với} \quad \text{Decompose}(P_i) \cap \text{Decompose}(P_j) = \emptyset \quad (\forall i \neq j)$$

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│               QUY TRÌNH PHÂN RÃ HỌC THUẬT TỪ CẤP VĨ MÔ SANG CẤP VI MÔ                           │
└────────────────────────────────┬────────────────────────────────────────────────────────────────┘
                                 │
                  ┌──────────────┴──────────────┐
                  ▼                             ▼
┌───────────────────────────────────┐         ┌───────────────────────────────────┐
│ 6 HỌ MÔ HÌNH VĨ MÔ (MACRO)        │         │ 7 TRƯỜNG PHÁI THUẬT TOÁN VĨ MÔ    │
│ (Không gian biểu diễn nền tảng)   │         │ (Nguyên lý toán học cốt lõi)      │
└─────────────────┬─────────────────┘         └─────────────────┬─────────────────┘
                  │ Phân rã kỹ thuật                            │ Phân rã hàm mục tiêu
                  ▼ (1-to-N Splitting)                          ▼ (1-to-N Splitting)
┌───────────────────────────────────┐         ┌───────────────────────────────────┐
│ 12 HỌ MÔ HÌNH VI MÔ (MICRO)       │         │ 14 TRƯỜNG PHÁI THUẬT TOÁN VI MÔ   │
│ • M1: Regex/DFA Sanitizer         │         │ • A1: Word TF-IDF + Platt         │
│ • M2: Toxic Lexicon Bloom Filters │         │ • A2: Sliding-Window PPL          │
│ • M3: Sparse Linear Word ML       │         │ • A3: Char Typographical Anomaly  │
│ • M4: Char N-Gram SVMs (char_wb)  │         │ • A4: Dense Metric Centroids      │
│ • M5: Shallow Tree Ensembles      │         │ • A5: Hidden-State Probing        │
│ • M6: Dense Bi-Encoders (MiniLM)  │         │ • A6: Disentangled Relative Attn  │
│ • M7: Hidden-State Probes         │         │ • A7: MOF Invariant KL Loss       │
│ • M8: Legacy Absolute BERT        │         │ • A8: Randomized Smoothing Voting │
│ • M9: Disentangled DeBERTa-v3     │         │ • A9: Minimax Adversarial Opt     │
│ • M10: Multilingual mDeBERTa/PG86M│         │ • A10: Conformal Risk Control     │
│ • M11: ModernBERT (8k Context)    │         │ • A11: Low-FPR ROC Interpolation  │
│ • M12: Generative Safety SLMs     │         │ • A12: Instruction Privilege      │
│                                   │         │ • A13: Head-and-Tail Priority     │
│                                   │         │ • A14: Multi-Turn Drift Tracking  │
└───────────────────────────────────┘         └───────────────────────────────────┘
```

---

### 4.2. Bảng Suy Dẫn Chi Tiết: 6 Họ Vĩ Mô $\implies$ 12 Lớp Vi Mô

| Họ Vĩ Mô (6 Họ) | Họ Vi Mô (12 Mô Hình) | Căn Cứ Phân Rã Kỹ Thuật (Tại sao phải tách ra?) | Bài Báo Bảo Chứng Trong `REFERENCES_LOG.md` |
| :--- | :--- | :--- | :--- |
| **$F_1$: Heuristic & Regex Scrubber** | **M1: Heuristic & Regex Sanitizer** | Xử lý biến đổi ký tự động (NFKC, zero-width, Base64/Hex/ROT13) qua máy trạng thái DFA. | Saltzer [[16]](#ref16), Yuan CipherChat [[17]](#ref17), Hackett [[31]](#ref31) |
| | **M2: Toxic Lexicon & Bloom Filters** | Kiểm tra sự hiện diện tĩnh của từ khóa độc hại qua hàm băm $O(1)$, không biến đổi chuỗi. | Lakera Guard static, Llama Guard Blocklist, Xu et al. [[26]](#ref26) |
| **$F_2$: Classical Sparse Statistical ML** | **M3: Sparse Linear Word ML (TF-IDF + LogReg)** | Không gian vector từ vựng (Word $n$-grams) + siêu phẳng tối ưu lồi, suy diễn cực nhanh $1.2\text{ms}$. | Jain et al. [[15]](#ref15), Spärck Jones |
| | **M4: Subword & Char N-Gram SVMs (`char_wb`)** | Không gian vector ký tự con ($3 - 5$ chars có biên từ), bắt dính Leetspeak và lỗi gõ ngụy trang. | Jain et al. [[15]](#ref15), Ayub [[21]](#ref21) |
| | **M5: Shallow Tree Ensembles (TF-IDF + RF)** | Cây quyết định phi tuyến tính phân tách đặc trưng thưa; minh chứng FPR cao khi chạy đơn lẻ. | Ayub & Majumdar (CAMLIS 2024 [[21]](#ref21)) |
| **$F_3$: Dense Metric Learning & Proximity** | **M6: Continuous Bi-Encoder Embeddings (MiniLM)** | Nhúng câu vào $\mathbb{R}^{384}$ đo khoảng cách Cosine tới tâm cụm độc hại ngoài biên (Black-box). | Ayub [[21]](#ref21), Sentence-BERT |
| | **M7: Hidden-State & Activation Probes** | Đặt probe tuyến tính đo biến thiên trạng thái ẩn bên trong forward pass của LLM (White-box). | Wen et al. InstructDetector [[19]](#ref19), Yang RAP-ID [[29]](#ref29) |
| **$F_4$: Absolute-Position Transformers** | **M8: Legacy Absolute Encoders (BERT/RoBERTa)** | Transformer cổ điển nhúng vị trí tuyệt đối tại layer 0; minh chứng bị dính Trigger Word Bias. | Devlin 2019, Liu 2019, Jain et al. [[15]](#ref15) |
| **$F_5$: Disentangled & Modern Deep Encoders** | **M9: Monolingual Disentangled (DeBERTa-v3-base)** | Bóc tách 3 ma trận Content-Position + RTD pretraining trên tiếng Anh; hạt nhân Tầng 2. | He et al. [[9]](#ref9), Li InjecGuard (ACL 2025 [[18]](#ref18)) |
| | **M10: Multilingual Disentangled (mDeBERTa/PG86M)** | Mở rộng từ vựng 250k tokens, tối ưu hóa phát hiện trên tiếng Việt và chuyển mã Code-switching. | Meta Prompt Guard [[20]](#ref20), Deng MultiJail [[35]](#ref35) |
| | **M11: Long-Context Modern Encoders (ModernBERT)** | RoPE + GeGLU + FlashAttention-2, native context 8,192 tokens giải quyết triệt để RAG tài liệu dài. | Warner et al. (Answer.AI / LightOn 2024 [[37]](#ref37)) |
| **$F_6$: Autoregressive Generative Safety SLMs** | **M12: Generative Safety SLMs / LLM-as-a-Judge** | Decoder tự hồi quy 2B–8B sinh nhãn rủi ro kèm giải thích; minh chứng độ trễ lớn $15 - 20\text{s}$ trên CPU. | Inan Llama Guard [[7]](#ref7), Rebedea NeMo [[8]](#ref8), Padhi Granite Guardian [[38]](#ref38) |

$$\sum_{k=1}^6 |\text{Decompose}(F_k)| = 2 + 3 + 2 + 1 + 3 + 1 = \mathbf{12\ Mô\ Hình}$$

---

### 4.3. Bảng Suy Dẫn Chi Tiết: 7 Trường Phái Vĩ Mô $\implies$ 14 Thuật Toán Vi Mô

| Thuật Toán Vĩ Mô (7 Paradigms) | Thuật Toán Vi Mô (14 Paradigms) | Căn Cứ Phân Rã Kỹ Thuật (Tại sao phải tách ra?) | Bài Báo Bảo Chứng Trong `REFERENCES_LOG.md` |
| :--- | :--- | :--- | :--- |
| **$P_1$: Sublinear Term Projection & Calibration** | **A1: Sublinear Word TF-IDF + Platt Calibration** | Khai phá tần suất từ vựng $n$-grams $(1, 3)$ và hiệu chuẩn logistic chuyển biên $z$ thành xác suất $P \in [0, 1]$. | Jain et al. [[15]](#ref15), Ayub [[21]](#ref21), Luhn, Spärck Jones |
| | **A3: Character-Level Entropy & Typographical Anomaly** | Đo entropy ký tự và bất thường bảng mã để tóm gọn Emoji Smuggling, Zero-Width, Cyrillic Homoglyphs. | Hackett et al. (ACL 2025 [[31]](#ref31)), Yuan CipherChat [[17]](#ref17) |
| **$P_2$: Sliding-Window Perplexity (PPL)** | **A2: Sliding-Window Cross-Entropy & Perplexity** | Tính độ hỗn loạn $PPL(W) = \exp(-\frac{1}{N}\sum \ln P(w_i \mid w_{<i}))$ tóm gọn chuỗi rác đối kháng GCG. | Jain et al. [[15]](#ref15), Zou et al. (GCG 2023 [[13]](#ref13)) |
| **$P_3$: Dense Metric Proximity** | **A4: Dense Metric Space Contrastive Centroids** | Ánh xạ câu vào vector $\mathbb{R}^{384}$ và đo khoảng cách Cosine tới tâm cụm độc hại $\boldsymbol{\mu}_k$. | Ayub & Majumdar (CAMLIS 2024 [[21]](#ref21)) |
| | **A5: Intermediate Hidden-State & Activation Gradient** | Phân tích vector trạng thái ẩn và gradient dòng thông tin giữa token chỉ thị và token dữ liệu. | Wen InstructDetector [[19]](#ref19), Yang RAP-ID [[29]](#ref29) |
| **$P_4$: Disentangled Attention & Invariant Loss** | **A6: Disentangled Content-Position Attention** | Tách ma trận Attention thành Content-to-Content, Content-to-Pos, Pos-to-Content ($A_{i,j}$). | He et al. (DeBERTaV3 ICLR 2023 [[9]](#ref9)) |
| | **A7: Mitigating Over-defense for Free (MOF) KL Loss** | Bổ sung số hạng phạt phân kỳ KL giữa prompt gốc và prompt thay thế từ khóa để xóa bỏ trigger bias. | Li et al. (InjecGuard ACL 2025 [[18]](#ref18)) |
| | **A12: Hierarchical Instruction Privilege Decoupling** | Phân tầng quyền hạn chỉ thị *System > User > Tool/Data*, giải quyết gốc rễ cạnh tranh chỉ thị. | Wallace et al. (OpenAI Instruction Hierarchy [[33]](#ref33)) |
| **$P_5$: Randomized Smoothing & Voting** | **A8: Stochastic Perturbation & Randomized Smoothing Voting** | Tạo $M$ bản sao nhiễu ngẫu nhiên và lấy biểu quyết đa số để đạt chứng chỉ bền vững (Certified Robustness). | Robey SmoothLLM [[14]](#ref14), Zhang JailGuard [[25]](#ref25) |
| **$P_6$: Minimax Adversarial Optimization** | **A9: Game-Theoretic Minimax Adversarial Optimization** | Tối ưu hóa cực tiểu cực đại $\min_\theta \max_{\delta \in \Delta} \mathcal{L}(f_\theta(x \oplus \delta), y)$ chống tấn công thích ứng. | Liu et al. (DataSentinel IEEE S&P 2025 [[32]](#ref32)) |
| **$P_7$: Conformal Risk Control & Dynamic Calibration** | **A10: Conformal Risk Control (CRC) Finite-Sample Bounds** | Xác định ngưỡng $\hat{\tau}$ bảo đảm toán học xác suất rủi ro $\mathbb{P}(\mathbb{E}[R(\hat{\tau})] \le \alpha) \ge 1 - \delta$ ($\text{FPR} \le 1.5\%$). | Angelopoulos et al. [[36]](#ref36), Kang C-SafeGen [[36]](#ref36) |
| | **A11: Low-FPR ROC Threshold Interpolation** | Nội suy ngưỡng vận hành tối ưu trên đường conc ROC trong phân vùng $\text{FPR} \le 1.0\%$ theo chuẩn PromptShield. | Jacob et al. (ACM CCS 2024 [[30]](#ref30)), Markov [[10]](#ref10) |
| | **A13: Sliding-Window Head-and-Tail Priority Chunking** | Băm khối 512 tokens (overlap 10%), quét ưu tiên Đuôi $\rightarrow$ Đầu $\rightarrow$ Thân chống Prompt Overflow tài liệu 200k. | Zhou Prompt Overflow 2026 [[40]](#ref40), Greshake [[4]](#ref4) |
| | **A14: Multi-Turn Contextual Drift Tracking** | Đo trôi dạt góc Cosine qua cửa sổ trượt phiên để bẻ gãy đòn leo thang đa lượt Crescendo. | Russinovich et al. (Crescendo MS Research [[39]](#ref39)) |

$$\sum_{k=1}^7 |\text{Decompose}(P_k)| = 2 + 1 + 2 + 3 + 1 + 1 + 4 = \mathbf{14\ Thuật\ Toán}$$

---

### 4.4. Bảng Tra Cứu Ánh Xạ Xuất Xứ (100% Provenance Traceability Matrix)

| Phần Tử Vi Mô | Thuộc Họ Vĩ Mô | Mã Bài Báo Gốc Trong `REFERENCES_LOG.md` | Tệp PDF Cục Bộ Được Kiểm Chứng |
| :--- | :---: | :---: | :--- |
| **M1: Heuristic Sanitizer** | $F_1$ | [[16]](#ref16), [[17]](#ref17), [[31]](#ref31) | [`Saltzer_1975`](file:///d:/Work/Do-an/workspaces/truongnv/References/Saltzer_1975_The_Protection_of_Information_in_Computer_Systems.pdf), [`Yuan_2024`](file:///d:/Work/Do-an/workspaces/truongnv/References/Yuan_2024_GPT4_Too_Smart_To_Be_Safe_Cipher_Jailbreak.pdf), [`Hackett_2025`](file:///d:/Work/Do-an/workspaces/truongnv/References/Hackett_2025_Bypassing_LLM_Guardrails_Evasion_Attacks.pdf) |
| **M2: Toxic Bloom Filter** | $F_1$ | [[7]](#ref7), [[26]](#ref26) | [`Meta_2023`](file:///d:/Work/Do-an/workspaces/truongnv/References/Meta_2023_Llama_Guard_Input_Output_Safeguard.pdf), [`Phuong_2024`](file:///d:/Work/Do-an/workspaces/truongnv/References/Phuong_2024_ACL_Comprehensive_Study_Jailbreak_Attack_Defense.pdf) |
| **M3: Linear Word ML** | $F_2$ | [[15]](#ref15) | [`Jain_2023`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_Jain_NeurIPS2023/papers/Jain_2023_Baseline_Defenses_arXiv2309.00614.pdf) |
| **M4: Char N-Gram SVM** | $F_2$ | [[15]](#ref15), [[21]](#ref21) | [`Jain_2023`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_Jain_NeurIPS2023/papers/Jain_2023_Baseline_Defenses_arXiv2309.00614.pdf), [`Ayub_2024`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_REJECTED_Ayub_CAMLIS2024/papers/Ayub_CAMLIS2024_arXiv2410.22284.pdf) |
| **M5: Shallow Tree Ensemble** | $F_2$ | [[21]](#ref21) | [`Ayub_2024_CAMLIS`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_REJECTED_Ayub_CAMLIS2024/papers/Ayub_CAMLIS2024_arXiv2410.22284.pdf) |
| **M6: Dense Bi-Encoder** | $F_3$ | [[21]](#ref21) | [`Ayub_2024_CAMLIS`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_REJECTED_Ayub_CAMLIS2024/papers/Ayub_CAMLIS2024_arXiv2410.22284.pdf) |
| **M7: Hidden-State Probing** | $F_3$ | [[19]](#ref19), [[29]](#ref29) | [`Zhao_2024_InstructDetector`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_InstructDetector_EMNLP2024/papers/Zhao_2024_InstructDetector_arXiv2402.06774.pdf), [`Viet_2026_RAP_ID`](file:///d:/Work/Do-an/workspaces/truongnv/References/Viet_2026_RAP_ID_Robust_Alignment_Preservation_Injection_Defense.pdf) |
| **M8: Legacy Absolute BERT** | $F_4$ | [[15]](#ref15) | [`Jain_2023_Baseline`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_Jain_NeurIPS2023/papers/Jain_2023_Baseline_Defenses_arXiv2309.00614.pdf) |
| **M9: DeBERTa-v3 Monolingual** | $F_5$ | [[9]](#ref9), [[18]](#ref18) | [`He_2023_DeBERTaV3`](file:///d:/Work/Do-an/workspaces/truongnv/References/He_2023_DeBERTaV3_Disentangled_Attention_ICLR.pdf), [`PIGuard_2025_ACL`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier2_PIGuard_ACL2025/papers/PIGuard_ACL2025_arXiv2410.22770.pdf) |
| **M10: mDeBERTa Multilingual** | $F_5$ | [[20]](#ref20), [[35]](#ref35) | [`Meta_2024_PG86M`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_Meta_PromptGuard2024/papers/Meta_2024_PurpleLlama_PromptGuard.pdf), [`Deng_2024_MultiJail`](file:///d:/Work/Do-an/workspaces/truongnv/References/Deng_2024_Multilingual_Jailbreak_Challenges_LLMs_ICLR.pdf) |
| **M11: ModernBERT 8k Context** | $F_5$ | [[37]](#ref37) | [`Warner_2024_ModernBERT`](file:///d:/Work/Do-an/workspaces/truongnv/References/Warner_2024_ModernBERT_Brings_Modern_Transformers_To_Encoders.pdf) |
| **M12: Generative SLM** | $F_6$ | [[7]](#ref7), [[8]](#ref8), [[38]](#ref38) | [`Meta_2023`](file:///d:/Work/Do-an/workspaces/truongnv/References/Meta_2023_Llama_Guard_Input_Output_Safeguard.pdf), [`NVIDIA_2023`](file:///d:/Work/Do-an/workspaces/truongnv/References/NVIDIA_2023_NeMo_Guardrails_Toolkit.pdf), [`Padhi_2024`](file:///d:/Work/Do-an/workspaces/truongnv/References/Padhi_2024_Granite_Guardian_Content_Safety_Risk_Detection.pdf) |
| **A1: Word TF-IDF + Platt** | $P_1$ | [[15]](#ref15), [[21]](#ref21) | [`Jain_2023`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_Jain_NeurIPS2023/papers/Jain_2023_Baseline_Defenses_arXiv2309.00614.pdf), [`Ayub_2024`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_REJECTED_Ayub_CAMLIS2024/papers/Ayub_CAMLIS2024_arXiv2410.22284.pdf) |
| **A2: Windowed Perplexity** | $P_2$ | [[13]](#ref13), [[15]](#ref15) | [`Zou_2023_GCG`](file:///d:/Work/Do-an/workspaces/truongnv/References/Zou_2023_Universal_Transferable_Adversarial_Attacks_GCG.pdf), [`Jain_2023`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_Jain_NeurIPS2023/papers/Jain_2023_Baseline_Defenses_arXiv2309.00614.pdf) |
| **A3: Char Anomaly Detection** | $P_1$ | [[17]](#ref17), [[31]](#ref31) | [`Yuan_2024`](file:///d:/Work/Do-an/workspaces/truongnv/References/Yuan_2024_GPT4_Too_Smart_To_Be_Safe_Cipher_Jailbreak.pdf), [`Hackett_2025`](file:///d:/Work/Do-an/workspaces/truongnv/References/Hackett_2025_Bypassing_LLM_Guardrails_Evasion_Attacks.pdf) |
| **A4: Dense Metric Centroids** | $P_3$ | [[21]](#ref21) | [`Ayub_2024_CAMLIS`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_REJECTED_Ayub_CAMLIS2024/papers/Ayub_CAMLIS2024_arXiv2410.22284.pdf) |
| **A5: Hidden Activation Gradient**| $P_3$ | [[19]](#ref19), [[29]](#ref29) | [`Zhao_2024_InstructDetector`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_InstructDetector_EMNLP2024/papers/Zhao_2024_InstructDetector_arXiv2402.06774.pdf), [`Viet_2026_RAP_ID`](file:///d:/Work/Do-an/workspaces/truongnv/References/Viet_2026_RAP_ID_Robust_Alignment_Preservation_Injection_Defense.pdf) |
| **A6: Disentangled Attention** | $P_4$ | [[9]](#ref9), [[18]](#ref18) | [`He_2023_DeBERTaV3`](file:///d:/Work/Do-an/workspaces/truongnv/References/He_2023_DeBERTaV3_Disentangled_Attention_ICLR.pdf), [`PIGuard_2025_ACL`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier2_PIGuard_ACL2025/papers/PIGuard_ACL2025_arXiv2410.22770.pdf) |
| **A7: MOF Invariant KL Loss** | $P_4$ | [[18]](#ref18) | [`PIGuard_2025_ACL`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier2_PIGuard_ACL2025/papers/PIGuard_ACL2025_arXiv2410.22770.pdf) |
| **A8: Randomized Smoothing** | $P_5$ | [[12]](#ref12), [[14]](#ref14), [[25]](#ref25) | [`Robey_2023_SmoothLLM`](file:///d:/Work/Do-an/workspaces/truongnv/References/Robey_2023_SmoothLLM_Defending_LLMs_Random_Perturbation.pdf), [`Zhou_2024_EasyJailbreak`](file:///d:/Work/Do-an/workspaces/truongnv/References/Zhou_2024_EasyJailbreak_Unified_Framework.pdf), [`Duc_2025_JailGuard`](file:///d:/Work/Do-an/workspaces/truongnv/References/Duc_2025_JailGuard_Universal_Detection_Framework_TOSEM.pdf) |
| **A9: Minimax Adversarial Opt**| $P_6$ | [[13]](#ref13), [[32]](#ref32) | [`Liu_2025_DataSentinel`](file:///d:/Work/Do-an/workspaces/truongnv/References/Liu_2025_DataSentinel_Game_Theoretic_Detection_Prompt_Injection.pdf), [`Zou_2023_GCG`](file:///d:/Work/Do-an/workspaces/truongnv/References/Zou_2023_Universal_Transferable_Adversarial_Attacks_GCG.pdf) |
| **A10: Conformal Risk Control** | $P_7$ | [[36]](#ref36) | [`Angelopoulos_2024`](file:///d:/Work/Do-an/workspaces/truongnv/References/Angelopoulos_2024_Conformal_Risk_Control.pdf) |
| **A11: Low-FPR ROC Interpolation**| $P_7$ | [[10]](#ref10), [[30]](#ref30) | [`Jacob_2024_PromptShield`](file:///d:/Work/Do-an/workspaces/truongnv/References/Jacob_2024_PromptShield_Deployable_Detection_Prompt_Injection_CCS.pdf), [`OpenAI_2023`](file:///d:/Work/Do-an/workspaces/truongnv/References/OpenAI_2023_Undesired_Content_Detection.pdf) |
| **A12: Instruction Privilege** | $P_4$ | [[33]](#ref33) | [`Wallace_2024`](file:///d:/Work/Do-an/workspaces/truongnv/References/Wallace_2024_Instruction_Hierarchy_Prioritize_Privileged_Instructions.pdf) |
| **A13: Head & Tail Chunking** | $P_7$ | [[4]](#ref4), [[23]](#ref23), [[40]](#ref40) | [`Zhou_2026_Prompt_Overflow`](file:///d:/Work/Do-an/workspaces/truongnv/References/Zhou_2026_Prompt_Overflow_Guardrail_Window_Mismatch.pdf), [`Greshake_2023`](file:///d:/Work/Do-an/workspaces/truongnv/References/Greshake_2023_Indirect_Prompt_Injection.pdf), [`Viet_2024_BIPIA`](file:///d:/Work/Do-an/workspaces/truongnv/References/Viet_2024_BIPIA_Benchmarking_Indirect_Prompt_Injection_Attacks.pdf) |
| **A14: Multi-Turn Drift Tracking**| $P_7$ | [[39]](#ref39) | [`Russinovich_2024_Crescendo`](file:///d:/Work/Do-an/workspaces/truongnv/References/Russinovich_2024_Crescendo_MultiTurn_Jailbreak_Attack.pdf) |

---

### 4.5. Bảng Ánh Xạ Toàn Diện 41 Bài Báo Tham Khảo (Master Attribution Matrix)

Bảng dưới đây thiết lập sự liên kết chặt chẽ giữa toàn bộ 41 công trình khoa học trong [`REFERENCES_LOG.md`](file:///d:/Work/Do-an/workspaces/truongnv/References/REFERENCES_LOG.md) với các Họ mô hình, Trường phái thuật toán và vị trí tiếp thu trong đề tài:

| STT & Mã Bài Báo | Tác Giả & Năm Xuất Bản | Bản Chất Đóng Góp Khoa Học Gốc (Tier 1) | Họ Mô Hình / Phân Loại | Trường Phái Thuật Toán Tương Ứng | Định Vị Tiếp Thu Trong Đồ Án PI-Guard (Tier 2 & Tier 3) |
| :---: | :--- | :--- | :---: | :---: | :--- |
| **[1]** | Zhao et al. (2023) | Khảo sát kiến trúc Transformer tự hồi quy & không gian token phẳng | Cơ sở lý thuyết | Không gian ngữ cảnh phẳng | Phân tích bản chất thiếu vắng security boundary trong LLM (*Chương 1, 2*) |
| **[2]** | Ouyang et al. (OpenAI 2022) | Instruction Tuning qua RLHF (InstructGPT) | Cơ sở lý thuyết | Căn chỉnh chỉ thị (Alignment) | Cơ sở phân tích xung đột quyền hạn giữa system prompt và user prompt (*Chương 1, 2*) |
| **[3]** | Perez & Ribeiro (2022) | Định nghĩa Goal Hijacking và Prompt Leaking | Nghiên cứu tấn công | Phân loại mối đe dọa trực tiếp | Xác lập định nghĩa lớp nhãn Prompt Injection và kịch bản Demo 1 (*Chương 1, 3*) |
| **[4]** | Greshake et al. (2023) | Khám phá tấn công Indirect Prompt Injection qua RAG | Nghiên cứu tấn công | Nhúng mã độc vào dữ liệu ngoài | Luận giải nhu cầu bảo vệ Ingress Proxy độc lập chặn cả dữ liệu RAG (*Chương 1, 2*) |
| **[5]** | Wei et al. (UC Berkeley 2023) | Thất bại căn chỉnh: Competing Objectives & Mismatched Gen | Nghiên cứu tấn công | Xung đột hàm mục tiêu | Chứng minh an toàn nội tại là không đủ, bắt buộc cần External Guardrail (*Chương 1, 4*) |
| **[6]** | Tencent Zhuque Lab (2026) | Mô hình bảo vệ AI Agent phân tầng Zone 0–Zone 3 | Nguyên lý an ninh | Phân tầng kiểm soát đa lớp | Định vị PI-Guard hoạt động tại Zone 0 (Prompt Gateway) (*Chương 1, 3*) |
| **[7]** | Inan et al. / Meta (2023) | Llama Guard: Mô hình LLM 7B làm trọng tài an toàn | **Họ 6 (Gen SLM)** | LLM-as-a-Judge Decoding | Baseline đối chuẩn trần; minh chứng độ trễ lớn của mô hình tự hồi quy (*Chương 2, 4*) |
| **[8]** | Rebedea et al. / NVIDIA (2023)| NeMo Guardrails: Bộ công cụ middleware lập trình bằng Colang | **Họ 6 (Gen SLM)** | Programmable Input/Output Rails | Tham khảo kiến trúc Reverse Proxy đánh chặn bất đồng bộ (*Chương 2, 3*) |
| **[9]** | He et al. / Microsoft (2023) | DeBERTaV3: Disentangled Attention & RTD pretraining | **Họ 5 (Modern Enc)** | **Thuật toán 4 (Disentangled)** | **Kiến trúc nền tảng Tầng 2** (`microsoft/deberta-v3-base`) (*Chương 3, 4*) |
| **[10]** | Markov et al. / OpenAI (2023) | Tối ưu hóa bộ lọc nội dung trong môi trường production | Nguyên lý an ninh | Đánh đổi tỷ lệ FPR / Trải nghiệm | Đặt mục tiêu ràng buộc kỹ thuật $\text{FPR} < 1.5\%$ trên tập lành tính (*Chương 2, 4*) |
| **[11]** | Shen et al. (ACM CCS 2024) | Đo lường thực nghiệm Jailbreak tự nhiên (DAN dataset) | Tập dữ liệu / Tấn công | Thu thập mẫu thực tế (In-the-wild) | Cung cấp dữ liệu kiểm thử jailbreak tự nhiên 1,405 mẫu (*Chương 3, 4*) |
| **[12]** | Zhou et al. / Fudan (2024) | EasyJailbreak: Framework đột biến prompt 4 giai đoạn | Framework tấn công | Toán tử đột biến (Fuzzing) | Sử dụng làm công cụ fuzzing kiểm thử độ suy giảm $\Delta F_1 < 5\%$ (*Chương 3, 4*) |
| **[13]** | Zou et al. / CMU (2023) | Thuật toán tối ưu hóa hậu tố đối kháng chuyển giao (GCG) | Nghiên cứu tấn công | Greedy Coordinate Gradient | Nguồn tạo sinh tập kiểm thử đối kháng ngoại lai (OOD Evaluation) (*Chương 4*) |
| **[14]** | Robey et al. / UPenn (2023) | SmoothLLM: Làm mịn ngẫu nhiên prompt và đa số biểu quyết | Khung phòng thủ | **Thuật toán 5 (SmoothLLM)** | Baseline đối chuẩn so sánh; phân tích chi phí trễ nhân bản $N$ lần (*Chương 2, 4*) |
| **[15]** | Jain et al. / UMD (2023) | Baseline Defenses: Perplexity filter & Character $n$-grams | **Họ 2 (Sparse ML)** | **Thuật toán 1 (TF-IDF) & 2 (PPL)** | **Cảm hứng thiết kế Tầng 1** (TF-IDF Word + Char N-grams) (*Chương 3, 4*) |
| **[16]** | Saltzer & Schroeder (1975) | 8 Nguyên lý thiết kế bảo vệ hệ thống thông tin | Nguyên lý kinh điển | Complete Mediation & Defense-in-Depth | **Kim chỉ nam kiến trúc**: Kiểm soát toàn diện & Phòng thủ phân tầng (*Chương 2, 3*) |
| **[17]** | Yuan et al. / Tencent (2024) | CipherChat: Vượt rào căn chỉnh bằng mã hóa ký tự | Nghiên cứu tấn công | Biến đổi bảng mã / Cipher | Minh chứng bắt buộc phải có Tầng 0 (Heuristic Decoding & Normalization) (*Chương 1, 3*) |
| **[18]** | Li et al. (ACL 2025) | InjecGuard: Giảm thiểu Over-defense bằng chiến lược MOF | **Họ 5 (Modern Enc)** | **Thuật toán 4 (MOF Loss)** | **Công trình tham chiếu trung tâm (Central Anchor)** được tái lập và nâng cấp (*Chương 3, 4*) |
| **[19]** | Wen et al. (EMNLP Findings) | InstructDetector: Phát hiện tấn công qua vector ẩn | **Họ 3 (Metric Learn)** | **Thuật toán 3 (Hidden Embeddings)** | Ứng viên mô hình đối chuẩn so sánh độ trễ và khả năng phân biệt (*Chương 4*) |
| **[20]** | Meta AI (2024) | Prompt Guard 86M: Phân loại nhúng nhẹ đa tác vụ | **Họ 5 (Modern Enc)** | Multi-task Classifier | Đối chuẩn trực tiếp về độ trễ CPU và rủi ro bị bypass bởi biến dị ký tự (*Chương 4*) |
| **[21]** | Ayub & Majumdar (CAMLIS 2024)| Bộ phân loại TF-IDF + Random Forest / Dense Embeddings | **Họ 2 & Họ 3** | **Thuật toán 1 & 3** | **Baseline bị loại bỏ có kiểm chứng** do FPR quá cao khi chạy đơn lẻ (*Chương 4*) |
| **[22]** | Yao et al. (NeurIPS 2022) | ZeroQuant: Lượng hóa sau huấn luyện PTQ INT8 | Kỹ thuật phần cứng | Lượng tử hóa ma trận trọng số | **Loại trừ ngoài phạm vi (Out-of-Scope)**: Giữ vững ranh giới chuyên ngành IA (*Chương 1*) |
| **[23]** | Yi et al. (NAACL 2024) | BIPIA: Benchmark Indirect Prompt Injection trên 5 tác vụ | Tập dữ liệu Benchmark | Đánh giá OOD gián tiếp | Cung cấp mẫu kiểm thử gián tiếp cho Chuyên đề 4 (*Chương 3, 4*) |
| **[24]** | Wang et al. (EMNLP 2023) | Do-Not-Answer: 936 prompt độc hại phân tầng rủi ro | Tập dữ liệu Benchmark | Đánh giá từ chối an toàn | Nguồn mẫu kiểm tra ranh giới từ chối và hiệu chuẩn ngưỡng an toàn (*Chương 3*) |
| **[25]** | Zhang et al. (TOSEM 2025) | JailGuard: Phát hiện jailbreak qua phân kỳ hành vi | Khung phòng thủ | **Thuật toán 5 (Behavioral Divergence)**| Đối chuẩn so sánh kỹ thuật đột biến và cơ chế đánh chặn đa tầng (*Chương 4*) |
| **[26]** | Xu et al. (ACL 2024) | Khảo sát thực nghiệm quy mô lớn Jailbreak Attack vs Defense | Khảo sát SOTA | Taxonomy so sánh đa chiều | Bổ trợ cho ma trận so sánh các phương pháp trong Chương 2 (*Chương 2*) |
| **[27]** | Liu & Hu / Zscaler (2024) | Khảo sát lỗ hổng LLM và giải pháp Security Gateway | Khảo sát công nghiệp | Ingress Gateway Architecture | Cung cấp góc nhìn thực tiễn triển khai proxy trong mạng doanh nghiệp (*Chương 2, 3*) |
| **[28]** | Yi et al. / Tsinghua (2024) | Khảo sát toàn diện kỹ thuật Jailbreak theo từng tầng | Khảo sát SOTA | Pre/In/Post-processing Taxonomy | Củng cố luận cứ lý thuyết cho kiến trúc phân tầng Ingress (*Chương 2*) |
| **[29]** | Yang et al. (ACL 2026) | RAP-ID: Phân tích trạng thái nội bộ để phát hiện injection | Nghiên cứu loại trừ | White-box Internal States | **Loại trừ ngoài phạm vi (Out-of-Scope)**: Vi phạm kiến trúc Black-Box Proxy (*Chương 1*) |
| **[30]** | Jacob et al. (ACM CCS 2024) | PromptShield: Chuẩn đánh giá Guardrail trong Low-FPR | Khung đánh giá SOTA | **Thuật toán 7 (ROC Interpolation)** | Xác lập cơ sở khoa học cho bài toán đánh đổi kinh tế $\text{FPR} < 1.5\%$ (*Chương 2, 4*) |
| **[31]** | Hackett et al. (ACL 2025) | Đánh giá đòn né tránh: Emoji Smuggling, Unicode Tags | Nghiên cứu tấn công | Ký tự biến dị & AML Evasion | **Bảo chứng Tầng 0 (Heuristic Scrubber)**: Chống mù Unicode/Emoji (*Chương 3, 4*) |
| **[32]** | Liu et al. (IEEE S&P 2025) | DataSentinel: Phát hiện injection qua lý thuyết trò chơi | Khung phòng thủ | **Thuật toán 6 (Minimax Optimization)**| Cung cấp khung tối ưu hóa đối kháng và tập benchmark Open-Prompt-Injection (*Chương 4*) |
| **[33]** | Wallace et al. (OpenAI 2024) | The Instruction Hierarchy: Phân tầng quyền hạn chỉ thị | Nguyên lý an ninh | Instruction Hierarchy Alignment | Chứng minh in-model alignment không đủ, bắt buộc có Ingress Proxy (*Chương 1, 2*) |
| **[34]** | Chao et al. (NeurIPS 2024) | JailbreakBench: Chuẩn benchmark mở (JBB-Behaviors) | Chuẩn đối chuẩn SOTA | Leaderboard tiêu chuẩn hóa | Tích hợp 100 hành vi JBB-Behaviors vào bộ kiểm thử thực nghiệm (*Chương 4*) |
| **[35]** | Deng et al. (ICLR 2024) | Multilingual Jailbreak: Rủi ro ngôn ngữ tài nguyên thấp | Nghiên cứu tấn công | Cross-lingual Safety Transfer | Luận chứng mở rộng bộ lọc sang tiếng Việt và kịch bản Code-switching (*Chương 3, 4*) |
| **[36]** | Angelopoulos / Kang (2024/25) | Conformal Risk Control & C-SafeGen | Cơ sở toán học | **Thuật toán 7 (Conformal Risk Control)**| **Bảo chứng toán học cho ngưỡng Tri-State** kiểm soát $\text{FPR} \le 1.5\%$ (*Chương 3, 4*) |
| **[37]** | Warner et al. (2024) | ModernBERT: Transformer Encoder thế hệ mới (8k context) | **Họ 5 (Modern Enc)** | RoPE + GeGLU + FlashAttention | Ứng viên nâng cấp Tầng 2, giải quyết giới hạn 512 tokens cho RAG (*Chương 3, 4*) |
| **[38]** | Padhi et al. (IBM 2024) | Granite Guardian: Dòng mô hình an toàn mở 2B/8B | **Họ 6 (Gen SLM)** | Risk Taxonomy Decoding | Đối chuẩn cho tầng thẩm định chuyên sâu ngoài biên (Tier 3) (*Chương 4*) |
| **[39]** | Russinovich et al. (MS 2024) | Crescendo: Tấn công đa lượt leo thang ngữ cảnh | Nghiên cứu tấn công | Multi-turn Contextual Drift | Luận chứng mở rộng phân tích trôi dạt ngữ cảnh qua cửa sổ trượt phiên (*Chương 3, 4*) |
| **[40]** | Zhou et al. (2026) | Prompt Overflow: Lỗ hổng bất đối xứng cửa sổ ngữ cảnh | Nghiên cứu tấn công | Context Window Mismatch Padding | Bảo chứng giải pháp Quét khối trượt ưu tiên Đuôi-Đầu cho văn bản 200k (*Chương 3*) |
| **[41]** | Luo & Han (NUS 2026) | CASCADE Against Jailbreaks: Phối hợp phòng thủ đa chặng | Nguyên lý an ninh | Đa giai đoạn & Phân tầng thích ứng | **Luận cứ tối thượng bác bỏ siêu mô hình đơn khối**, bảo chứng kiến trúc PI-Guard (*Chương 2, 3*) |

---

## 🛡️ 5. LUẬN ĐIỂM BẢO VỆ HỘI ĐỒNG: TẠI SAO HAI TẦNG PHÂN CẤP LÀ LỰA CHỌN TỐI ƯU CHO CHUYÊN NGÀNH AN TOÀN THÔNG TIN?

Khi bước vào phòng bảo vệ tốt nghiệp trước Hội đồng FPT, việc nắm vững bản chất kiến trúc và trường phái thuật toán giúp nhóm đưa ra những lập luận mang tính học thuật đanh thép:

### 5.1. Bác Bỏ Ảo Tưởng "Siêu Mô Hình Đơn Khối" (The Monolithic Hyper-Model Fallacy)
- **Câu hỏi của Hội đồng**: *"Tại sao không huấn luyện một mô hình duy nhất thật lớn (như Llama Guard 8B hoặc fine-tune một Transformer khổng lồ) để xử lý mọi loại tấn công, mà phải bày vẽ chia thành Tầng 1 và Tầng 2?"*
- **Lập luận bảo vệ**:
  1. **Định lý thực nghiệm từ CASCADE (Luo & Han, NUS 2026 `[41]`)**: Nghiên cứu đã chứng minh trên 19 đòn tấn công và 15 giải pháp phòng vệ rằng: *Không có bất kỳ một mô hình đơn lẻ nào là tối ưu toàn diện trên mọi khía cạnh*. Mô hình càng lớn thì độ trễ càng cao; mô hình nhỏ thì dễ bị lừa bởi biến dị ngữ nghĩa.
  2. **Nguyên lý Saltzer & Schroeder (1975 `[16]`)**: Nguyên lý *Economy of Mechanism* và *Defense-in-Depth* chỉ rõ: một cơ chế kiểm soát an toàn phải đơn giản nhất có thể và được tổ chức theo từng lớp phòng tuyến độc lập.
  3. **Quy luật kinh tế vận hành**: Việc kích hoạt một Transformer nặng cho $100\%$ các truy vấn thông thường (như *"Thời tiết hôm nay thế nào?"*) là sự lãng phí tài nguyên máy tính nghiêm trọng và làm tăng độ trễ hệ thống lên gấp 15–20 lần không cần thiết.

### 5.2. Luận Giải Tính Ưu Việt Của Phân Vùng Quyết Định Ba Trạng Thái (Tri-State Decision Engine)
- **Câu hỏi của Hội đồng**: *"Tại sao lại có vùng bất định $0.15 \le P_{\text{T1}} \le 0.85$ mà không phân loại nhị phân dứt khoát 0 hoặc 1 ngay tại Tầng 1?"*
- **Lập luận bảo vệ**:
  1. **Bản chất của Mô hình Thống kê Thưa (Họ 2)**: Mô hình TF-IDF có tốc độ cực nhanh ($1.2\text{ms}$) nhưng không gian vector bị thiếu vắng thông tin cấu trúc cú pháp sâu. Khi giá trị xác suất rơi vào khoảng giữa ($0.15 - 0.85$), mô hình đang ở trạng thái không chắc chắn cao (High Epistemic Uncertainty). Việc ép buộc ra quyết định nhị phân tại đây sẽ trực tiếp đẩy $\text{FPR}$ lên $10 - 15\%$ (như kết quả của Ayub `[21]`).
  2. **Cơ sở Conformal Risk Control (`[36]`) & PromptShield (`[30]`)**: PI-Guard thiết lập hai ngưỡng $\tau_{\text{low}} = 0.15$ và $\tau_{\text{high}} = 0.85$ dựa trên việc hiệu chuẩn phân vị sai số có bảo chứng xác suất. Khoảng bất định chính là vùng đệm an toàn để chuyển giao quyền phán quyết cho **Tầng 2 (DeBERTa-v3 MOF `[9, 18]`)** - nơi có cơ chế Disentangled Attention đủ sâu sắc để phân xử chính xác.
  3. **Kết quả thực nghiệm**: Tầng 1 hấp thụ và giải phóng an toàn hơn $75\%$ lưu lượng lành tính và chặn đứng các tấn công thô sơ, chỉ để khoảng $20 - 25\%$ truy vấn phức tạp đi tiếp vào Tầng 2. Nhờ đó, độ trễ trung bình của toàn hệ thống được duy trì ở mức xuất sắc ($P95 < 30\text{ms}$ trên CPU thuần túy).

### 5.3. Khẳng Định Bản Sắc Chuyên Ngành An Toàn Thông Tin (IA Identity)
- Đồ án PI-Guard kiên quyết nói **KHÔNG** với việc sa đà vào các kỹ thuật tối ưu hóa phần cứng thuần túy như Lượng tử hóa trọng số INT8 (ZeroQuant `[22]`) — vốn là địa hạt của Khoa học Máy tính và Kỹ thuật Hệ thống.
- Trọng tâm khoa học của đồ án được định vị chuẩn mực trong chuyên ngành An toàn Thông tin:
  - **Mô hình hóa đe dọa bài bản**: Phân loại theo chuẩn NIST AI 100-2e2025 và OWASP LLM01:2025.
  - **Kiến trúc phòng thủ chốt chặn**: Thiết kế Ingress Proxy đáp ứng nguyên lý Complete Mediation (Saltzer & Schroeder).
  - **Thực nghiệm đối kháng khắt khe**: Kiểm thử độ bền trước các đòn biến dị ký tự (Hackett `[31]`, Yuan `[17]`), chuỗi tối ưu hóa GCG (`[13]`) và bài toán tràn cửa sổ ngữ cảnh Prompt Overflow (`[40]`).
  - **Cân bằng kinh tế an ninh**: Tối ưu hóa đường cong ROC trong phân vùng Low-FPR ($\text{FPR} < 1.5\%$) có bảo chứng toán học Conformal Risk Control (`[36]`).

---

## 🎯 6. KẾT LUẬN & ĐỀ XUẤT HÀNH ĐỘNG

1. **Kết luận khoa học**: Toàn bộ 41 tài liệu tham khảo trong đồ án không phải là một danh sách rời rạc, mà là một **hệ sinh thái nghiên cứu an ninh LLM hoàn chỉnh**. Sự hội tụ về **6 Họ Kiến trúc** và **7 Trường phái Thuật toán** ở cấp vĩ mô, cùng với sự phân rã thành **12 Họ Mô hình** và **14 Thuật toán Hiện thực** ở cấp vi mô là quy luật khách quan của khoa học máy tính khi phân tách giữa *Hiện tượng tấn công*, *Nguyên lý thiết kế*, *Công cụ đo kiểm* và *Cơ chế toán học phát hiện*.
2. **Kế thừa vào Luận văn & Báo cáo Tiến độ**:
   - Sử dụng bảng phân rã chức năng tại Mục 1.2 và Mục 4 làm nội dung nòng cốt cho **Chương 2 (Literature Review & Related Work)** trong Luận văn chính thức.
   - Sử dụng bảng so sánh 6 họ mô hình tại Mục 2 và 12 mô hình tại Mục 4 làm Slide đối chuẩn công nghệ trong các buổi báo cáo với GVHD và Hội đồng.
   - Khẳng định tính đúng đắn và độc lập của mô hình phân tầng thích ứng Two-Tier Adaptive Cascade trước mọi câu hỏi phản biện của Hội đồng.

---

## 📚 7. TÀI LIỆU THAM KHẢO (REFERENCES)

* <a id="ref1"></a>**[1]** W. X. Zhao et al. 2023. *A Survey of Large Language Models*. arXiv preprint [arXiv:2303.18223](https://arxiv.org/abs/2303.18223). Local PDF: [`References/Zhao_2023_A_Survey_of_Large_Language_Models.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Zhao_2023_A_Survey_of_Large_Language_Models.pdf).
* <a id="ref2"></a>**[2]** L. Ouyang, J. Wu, X. Jiang, et al. 2022. *Training language models to follow instructions with human feedback*. In *NeurIPS 2022*, pages 27730–27744. Local PDF: [`References/Ouyang_2022_InstructGPT_Training_Language_Models_Follow_Instructions.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Ouyang_2022_InstructGPT_Training_Language_Models_Follow_Instructions.pdf).
* <a id="ref3"></a>**[3]** F. Perez and I. Ribeiro. 2022. *Ignore This Title and Hack This Website: Exposing Systemic Vulnerabilities in Large Language Models*. In *Black Hat USA 2022*. Local PDF: [`References/Perez_2022_Ignore_This_Title_Hack_This_Paper_Prompt_Injection.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Perez_2022_Ignore_This_Title_Hack_This_Paper_Prompt_Injection.pdf).
* <a id="ref4"></a>**[4]** K. Greshake, S. Abdelnabi, S. Mishra, et al. 2023. *Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection*. In *ACM AISec 2023*. Local PDF: [`References/Greshake_2023_Indirect_Prompt_Injection.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Greshake_2023_Indirect_Prompt_Injection.pdf).
* <a id="ref5"></a>**[5]** A. Wei, N. Haghtalab, and J. Steinhardt. 2023. *Jailbroken: How Does LLM Safety Training Fail?* In *NeurIPS 2023*. [arXiv:2307.02483](https://arxiv.org/abs/2307.02483). Local PDF: [`References/Wei_2024_Jailbroken_How_LLM_Safety_Training_Fails.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Wei_2024_Jailbroken_How_LLM_Safety_Training_Fails.pdf).
* <a id="ref6"></a>**[6]** Tencent Zhuque Lab. 2026. *LLM Security Framework & Boundary Taxonomy Report*. Local PDF: [`References/Tencent_2026_AI_Infra_Guard_MultiLayer_Agent_RedTeaming.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Tencent_2026_AI_Infra_Guard_MultiLayer_Agent_RedTeaming.pdf).
* <a id="ref7"></a>**[7]** H. Inan, K. Upasani, J. Chi, et al. 2023. *Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations*. Meta AI. [arXiv:2312.06674](https://arxiv.org/abs/2312.06674). Local PDF: [`References/Meta_2023_Llama_Guard_Input_Output_Safeguard.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Meta_2023_Llama_Guard_Input_Output_Safeguard.pdf).
* <a id="ref8"></a>**[8]** T. Rebedea, R. Dinu, F. Sgondea, et al. 2023. *NeMo Guardrails: A Toolkit for Controllable and Safe LLM Applications*. In *EMNLP 2023 System Demonstrations*. Local PDF: [`References/NVIDIA_2023_NeMo_Guardrails_Toolkit.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/NVIDIA_2023_NeMo_Guardrails_Toolkit.pdf).
* <a id="ref9"></a>**[9]** P. He, J. Yin, D. He, et al. 2023. *DeBERTaV3: Improving DeBERTa using ELECTRA-Style Pre-Training with Gradient-Disentangled Embedding*. In *ICLR 2023*. Local PDF: [`References/He_2023_DeBERTaV3_Disentangled_Attention_ICLR.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/He_2023_DeBERTaV3_Disentangled_Attention_ICLR.pdf).
* <a id="ref10"></a>**[10]** G. Markov et al. / OpenAI. 2023. *A Holistic Approach to Undesired Content Detection in the Real World*. In *AAAI 2023*. Local PDF: [`References/OpenAI_2023_Undesired_Content_Detection.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/OpenAI_2023_Undesired_Content_Detection.pdf).
* <a id="ref11"></a>**[11]** X. Shen, Z. Chen, M. Backes, et al. 2024. *\"Do Anything Now\": Characterizing and Evaluating In-The-Wild Jailbreak Prompts on Large Language Models*. In *ACM CCS 2024*. Local PDF: [`References/Shen_2024_Do_Anything_Now_Jailbreak_Prompts_In_The_Wild.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Shen_2024_Do_Anything_Now_Jailbreak_Prompts_In_The_Wild.pdf).
* <a id="ref12"></a>**[12]** W. Zhou, J. Xiao, Y. He, et al. 2024. *EasyJailbreak: A Unified Framework for Jailbreak Attacks*. arXiv preprint [arXiv:2403.12171](https://arxiv.org/abs/2403.12171). Local PDF: [`References/Zhou_2024_EasyJailbreak_Unified_Framework.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Zhou_2024_EasyJailbreak_Unified_Framework.pdf).
* <a id="ref13"></a>**[13]** A. Zou, Z. Wang, J. Z. Kolter, and M. Fredrikson. 2023. *Universal and Transferable Adversarial Attacks on Aligned Language Models*. [arXiv:2307.15043](https://arxiv.org/abs/2307.15043). Local PDF: [`References/Zou_2023_Universal_Transferable_Adversarial_Attacks_GCG.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Zou_2023_Universal_Transferable_Adversarial_Attacks_GCG.pdf).
* <a id="ref14"></a>**[14]** A. Robey, E. Wong, H. Hassani, and G. J. Pappas. 2023. *SmoothLLM: Defending Large Language Models Against Jailbreaking Attacks*. In *NeurIPS 2023*. [arXiv:2310.03684](https://arxiv.org/abs/2310.03684). Local PDF: [`References/Robey_2023_SmoothLLM_Defending_LLMs_Random_Perturbation.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Robey_2023_SmoothLLM_Defending_LLMs_Random_Perturbation.pdf).
* <a id="ref15"></a>**[15]** N. Jain, A. Schwarzschild, Y. Wen, et al. 2023. *Baseline Defenses for Adversarial Attacks Against Aligned Language Models*. In *NeurIPS 2023 Workshop*. [arXiv:2309.00614](https://arxiv.org/abs/2309.00614). Local PDF: [`replications/Tier1_Candidate_Jain_NeurIPS2023/papers/Jain_2023_Baseline_Defenses_arXiv2309.00614.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_Jain_NeurIPS2023/papers/Jain_2023_Baseline_Defenses_arXiv2309.00614.pdf).
* <a id="ref16"></a>**[16]** J. H. Saltzer and M. D. Schroeder. 1975. *The Protection of Information in Computer Systems*. In *Proceedings of the IEEE*, 63(9):1278–1308. DOI: 10.1109/PROC.1975.9939. Local PDF: [`References/Saltzer_1975_The_Protection_of_Information_in_Computer_Systems.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Saltzer_1975_The_Protection_of_Information_in_Computer_Systems.pdf).
* <a id="ref17"></a>**[17]** Y. Yuan, W. Jiao, W. Wang, J. Huang, P. He, and Z. Tu. 2024. *GPT-4 Is Too Smart To Be Safe: Stealthy Chat with LLMs via Cipher*. In *ICLR 2024*. Local PDF: [`References/Yuan_2024_GPT4_Too_Smart_To_Be_Safe_Cipher_Jailbreak.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Yuan_2024_GPT4_Too_Smart_To_Be_Safe_Cipher_Jailbreak.pdf).
* <a id="ref18"></a>**[18]** H. Li, X. Liu, N. Zhang, and C. Xiao. 2025. *PIGuard: Prompt Injection Guardrail via Mitigating Overdefense for Free*. In *ACL 2025 - Long Paper*. [arXiv:2410.22770](https://arxiv.org/abs/2410.22770). Local PDF: [`replications/Tier2_PIGuard_ACL2025/papers/PIGuard_ACL2025_arXiv2410.22770.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier2_PIGuard_ACL2025/papers/PIGuard_ACL2025_arXiv2410.22770.pdf).
* <a id="ref19"></a>**[19]** S. Zhao, D. Ge, R. Rossi, et al. 2024. *Defending against Indirect Prompt Injection by Instruction Detection*. In *Findings of EMNLP 2024*. [arXiv:2402.06774](https://arxiv.org/abs/2402.06774). Local PDF: [`replications/Tier1_Candidate_InstructDetector_EMNLP2024/papers/Zhao_2024_InstructDetector_arXiv2402.06774.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_InstructDetector_EMNLP2024/papers/Zhao_2024_InstructDetector_arXiv2402.06774.pdf).
* <a id="ref20"></a>**[20]** Meta AI. 2024. *Prompt Guard 86M: A Small Classifier for Prompt Injection and Jailbreak Detection*. Model Card and Technical Report. [arXiv:2407.21783](https://arxiv.org/abs/2407.21783). Local PDF: [`replications/Tier1_Candidate_Meta_PromptGuard2024/papers/Meta_2024_PurpleLlama_PromptGuard.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_Meta_PromptGuard2024/papers/Meta_2024_PurpleLlama_PromptGuard.pdf).
* <a id="ref21"></a>**[21]** M. R. R. Ayub and A. Majumdar. 2024. *Embedding-based classifiers can detect prompt injection attacks*. In *CAMLIS 2024*. [arXiv:2410.22284](https://arxiv.org/abs/2410.22284). Local PDF: [`replications/Tier1_REJECTED_Ayub_CAMLIS2024/papers/Ayub_CAMLIS2024_arXiv2410.22284.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_REJECTED_Ayub_CAMLIS2024/papers/Ayub_CAMLIS2024_arXiv2410.22284.pdf).
* <a id="ref22"></a>**[22]** Z. Yao, R. Y. Aminabadi, M. Zhang, et al. 2022. *ZeroQuant: Efficient and Affordable Post-Training Quantization for Large-Scale Transformers*. In *NeurIPS 2022*. Local PDF: [`References/Yao_2022_ZeroQuant_Efficient_Post_Training_Quantization_Transformers.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Yao_2022_ZeroQuant_Efficient_Post_Training_Quantization_Transformers.pdf).
* <a id="ref23"></a>**[23]** J. Yi, Y. Xie, J. Zhu, et al. 2024. *Benchmarking and Defending Against Indirect Prompt Injection Attacks on Large Language Models*. In *NAACL 2024*. Local PDF: [`References/Viet_2024_BIPIA_Benchmarking_Indirect_Prompt_Injection_Attacks.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Viet_2024_BIPIA_Benchmarking_Indirect_Prompt_Injection_Attacks.pdf).
* <a id="ref24"></a>**[24]** Y. Wang, H. Li, X. Han, et al. 2023. *Do-Not-Answer: A Dataset for Evaluating Safeguards in Large Language Models*. In *EMNLP 2023*. Local PDF: [`References/Phuong_2023_Do_Not_Answer_Dataset_Evaluating_Safeguards.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Phuong_2023_Do_Not_Answer_Dataset_Evaluating_Safeguards.pdf).
* <a id="ref25"></a>**[25]** S. Zhang et al. 2025. *JailGuard: Detecting Jailbreak Attacks on Large Language Models via Behavioral Divergence*. In *ACM TOSEM 2025*. Local PDF: [`References/Duc_2025_JailGuard_Universal_Detection_Framework_TOSEM.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Duc_2025_JailGuard_Universal_Detection_Framework_TOSEM.pdf).
* <a id="ref26"></a>**[26]** N. Xu, F. Wang, H. Zhou, et al. 2024. *A Comprehensive Study of Jailbreak Attack and Defense Techniques on Large Language Models*. In *Findings of ACL 2024*. Local PDF: [`References/Phuong_2024_ACL_Comprehensive_Study_Jailbreak_Attack_Defense.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Phuong_2024_ACL_Comprehensive_Study_Jailbreak_Attack_Defense.pdf).
* <a id="ref27"></a>**[27]** D. Liu and S. Hu. 2024. *Threat Modeling and Security Architecture for Enterprise LLM Gateways*. Zscaler Whitepaper. Local PDF: [`References/Phuong_2024_Exploring_Vulnerabilities_Protections_LLMs_Survey.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Phuong_2024_Exploring_Vulnerabilities_Protections_LLMs_Survey.pdf).
* <a id="ref28"></a>**[28]** J. Yi et al. 2024. *A Survey on Recent Advances in Jailbreak Attacks on Large Language Models*. Tsinghua Tech Report. Local PDF: [`References/Phuong_2024_Survey_Jailbreak_Attacks_Defenses_LLMs.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Phuong_2024_Survey_Jailbreak_Attacks_Defenses_LLMs.pdf).
* <a id="ref29"></a>**[29]** Y. Yang et al. 2026. *RAP-ID: Retrieval-Augmented Prompt Injection Detection via Internal State Probing*. In *ACL 2026*. Local PDF: [`References/Viet_2026_RAP_ID_Robust_Alignment_Preservation_Injection_Defense.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Viet_2026_RAP_ID_Robust_Alignment_Preservation_Injection_Defense.pdf).
* <a id="ref30"></a>**[30]** D. Jacob, H. Alzahrani, Z. Hu, B. Alomair, and D. Wagner. 2024. *PromptShield: Deployable Detection for Prompt Injection Attacks*. In *ACM CCS 2024*, pages 4247–4261. DOI: 10.1145/3714393.3726501. Local PDF: [`workspaces/truongnv/References/Jacob_2024_PromptShield_Deployable_Detection_Prompt_Injection_CCS.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Jacob_2024_PromptShield_Deployable_Detection_Prompt_Injection_CCS.pdf).
* <a id="ref31"></a>**[31]** C. Hackett, O. Kjellgren, and S. Al-Rubaie. 2025. *Bypassing LLM Guardrails: Mechanisms of Adversarial Evasion and Detection Strategies*. In *ACL 2025*. Local PDF: [`References/Hackett_2025_Bypassing_LLM_Guardrails_Evasion_Attacks.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Hackett_2025_Bypassing_LLM_Guardrails_Evasion_Attacks.pdf).
* <a id="ref32"></a>**[32]** Y. Liu, Y. Jia, J. Jia, D. Song, and N. Z. Gong. 2025. *DataSentinel: A Game-Theoretic Detection of Prompt Injection Attacks*. In *IEEE S&P 2025*. Local PDF: [`workspaces/truongnv/References/Liu_2025_DataSentinel_Game_Theoretic_Detection_Prompt_Injection.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Liu_2025_DataSentinel_Game_Theoretic_Detection_Prompt_Injection.pdf).
* <a id="ref33"></a>**[33]** E. Wallace et al. / OpenAI. 2024. *The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions*. arXiv preprint [arXiv:2404.13208](https://arxiv.org/abs/2404.13208). Local PDF: [`workspaces/truongnv/References/Wallace_2024_Instruction_Hierarchy_Prioritize_Privileged_Instructions.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Wallace_2024_Instruction_Hierarchy_Prioritize_Privileged_Instructions.pdf).
* <a id="ref34"></a>**[34]** P. Chao, E. Debenedetti, A. Robey, et al. 2024. *JailbreakBench: An Open Robustness Benchmark for Jailbreaking Large Language Models*. In *NeurIPS 2024*. [arXiv:2404.01318](https://arxiv.org/abs/2404.01318). Local PDF: [`References/Chao_2024_JailbreakBench_Open_Robustness_Benchmark_NeurIPS.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Chao_2024_JailbreakBench_Open_Robustness_Benchmark_NeurIPS.pdf).
* <a id="ref35"></a>**[35]** Y. Deng et al. 2024. *Multilingual Jailbreak Challenges in Large Language Models*. In *ICLR 2024*. [arXiv:2310.06474](https://arxiv.org/abs/2310.06474). Local PDF: [`workspaces/truongnv/References/Deng_2024_Multilingual_Jailbreak_Challenges_LLMs_ICLR.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Deng_2024_Multilingual_Jailbreak_Challenges_LLMs_ICLR.pdf).
* <a id="ref36"></a>**[36]** A. N. Angelopoulos, S. Bates, E. J. Candès, et al. 2024. *Conformal Risk Control*. arXiv preprint [arXiv:2208.02814](https://arxiv.org/abs/2208.02814). Local PDF: [`workspaces/truongnv/References/Angelopoulos_2024_Conformal_Risk_Control.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Angelopoulos_2024_Conformal_Risk_Control.pdf).
* <a id="ref37"></a>**[37]** B. Warner, A. Chaffin, B. Clavié, et al. 2024. *ModernBERT: Bringing Modern Transformer Innovations to Pre-trained Encoders*. [arXiv:2412.13663](https://arxiv.org/abs/2412.13663). Local PDF: [`workspaces/truongnv/References/Warner_2024_ModernBERT_Brings_Modern_Transformers_To_Encoders.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Warner_2024_ModernBERT_Brings_Modern_Transformers_To_Encoders.pdf).
* <a id="ref38"></a>**[38]** I. Padhi et al. 2024. *Granite Guardian: Content Safety and Risk Detection*. IBM Research. [arXiv:2412.07724](https://arxiv.org/abs/2412.07724). Local PDF: [`References/Padhi_2024_Granite_Guardian_Content_Safety_Risk_Detection.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Padhi_2024_Granite_Guardian_Content_Safety_Risk_Detection.pdf).
* <a id="ref39"></a>**[39]** M. Russinovich et al. / Microsoft. 2024. *Great, Now Write an Article About That: The Crescendo Multi-Turn Jailbreak Attack*. arXiv preprint [arXiv:2404.01833](https://arxiv.org/abs/2404.01833). Local PDF: [`workspaces/truongnv/References/Russinovich_2024_Crescendo_MultiTurn_Jailbreak_Attack.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Russinovich_2024_Crescendo_MultiTurn_Jailbreak_Attack.pdf).
* <a id="ref40"></a>**[40]** Y. Zhou et al. 2026. *Prompt Overflow: Vulnerability in Asymmetric Context Windows of LLM Applications*. Local PDF: [`workspaces/truongnv/References/Zhou_2026_Prompt_Overflow_Guardrail_Window_Mismatch.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Zhou_2026_Prompt_Overflow_Guardrail_Window_Mismatch.pdf).
* <a id="ref41"></a>**[41]** J. Luo and E. Han. 2026. *CASCADE Against Jailbreaks: Combination Across Stages with Controlled Attack-Defense Evaluation*. [arXiv:2609.21793](https://arxiv.org/abs/2609.21793). Local PDF: [`References/Luo_2026_CASCADE_Against_Jailbreaks_Evaluation.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Luo_2026_CASCADE_Against_Jailbreaks_Evaluation.pdf).

