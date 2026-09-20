# ĐỀ XUẤT PHỔ MÔ HÌNH THỰC NGHIỆM SOTA MỞ RỘNG (BEYOND TF-IDF & DEBERTA)
## Dự án: PI-Guard (External Guardrail Proxy for LLM Applications)
### Tác giả: Nguyễn Văn Trường (Leader) — Workspace: `workspaces/truongnv/`

---

## 1. TỔNG QUAN & ĐỘNG LỰC HỌC THUẬT

Trong các nghiên cứu phòng thủ LLM giai đoạn 2023–2024, hai thái cực thường được sử dụng làm đại diện:
1. **Thái cực cổ điển (Lexical Baseline)**: TF-IDF kết hợp LinearSVC / LogisticRegression (tốc độ cao $< 1\text{ms}$, nhưng mù ngữ nghĩa và dễ bị bypass bởi từ đồng nghĩa, paraphrase).
2. **Thái cực Transformer tiền huấn luyện (Pre-trained Encoder)**: DeBERTa-v3-base (He et al., ICLR 2023) (hiểu ngữ nghĩa sâu sắc qua Disentangled Attention, nhưng chi phí suy luận CPU đạt ~20–30ms và giới hạn độ dài ngữ cảnh 512 tokens).

Tuy nhiên, bức tranh công nghệ phòng thủ AI thế giới (SOTA 2024–2026) đã xuất hiện nhiều bước tiến đột phá, cung cấp các giải pháp vượt trội hơn hẳn cả về **tốc độ suy luận**, **độ dài ngữ cảnh**, **khả năng phát hiện tấn công đối kháng (Adversarial Robustness)** và **khả năng phân định xung đột chỉ thị ($S \leftrightarrow U$)**.

Tài liệu này đề xuất phổ mô hình thực nghiệm mở rộng toàn diện cho đồ án **PI-Guard**, phân tầng từ các mô hình **SOTA hàng đầu thế giới** xuống đến **nguyên mẫu thực nghiệm (Academic PoC Prototype)** của đồ án, bảo đảm tuyệt đối:
- Tuân thủ mô hình **External Guardrail Proxy** (chỉ phân tích văn bản đầu vào, không can thiệp trọng số hay KV-cache của LLM đích).
- Thỏa mãn ràng buộc độ trễ thấp (**P95 < 30ms** trên CPU cho phân tầng trực tiếp).
- Tuân thủ quy chuẩn thuật ngữ phòng thủ học thuật (**Academic Defense Terminology Blacklist**).

---

## 2. MA TRẬN ĐỐI CHUẨN KỸ THUẬT 4 THẾ HỆ MÔ HÌNH (SOTA $\rightarrow$ BASELINE)

| Thế hệ / Họ mô hình | Mô hình đại diện tiêu biểu | Kích thước tham số | Ngữ cảnh tối đa (Context) | Độ trễ CPU (P95) | Khả năng phát hiện Prompt Injection / Jailbreak | Độ bền đối kháng (Adversarial Suffix / GCG) | Vị trí tối ưu trong kiến trúc PI-Guard |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Thế hệ 1: SLM Guardrail Chuyên biệt (Generative Small LM)** | **Llama Guard 3 1B** (Meta, 2024) <br> **Granite Guardian 3.0 2B** (IBM, 2024) | 1.0B – 2.0B (INT4: ~0.8 – 1.5GB) | 8,192 – 131,072 tokens | 50 – 150ms (CPU/INT4) <br> 15 – 30ms (GPU) | **Rất cao**: Hiểu sâu sắc sắc thái chỉ thị, ngữ cảnh hội thoại đa lượt | **Trung bình - Cao**: Khả năng suy luận ngữ cảnh tốt nhưng vẫn có thể bị jailbreak phức tạp | **Tier 3 (High-Assurance Arbitration)**: Thẩm định bất đồng bộ hoặc xác thực các ca biên (borderline cases). |
| **Thế hệ 2: Next-Gen Encoder Transformers** | **ModernBERT-base** (Answer.AI/LightOn, 2024) <br> **DeBERTa-v3-base** (ICLR 2023) <br> **BGE-Reranker-v2-m3** (BAAI, 2024) | 110M – 149M (FP16: ~250 – 300MB) | **8,192 tokens** (ModernBERT) <br> 512 tokens (DeBERTa) | **8 – 18ms** (ModernBERT CPU) <br> 20 – 30ms (DeBERTa CPU) | **Rất cao**: Nắm bắt cú pháp phân tách chỉ thị, instruction override | **Cao**: Khi được fine-tune với dữ liệu đối kháng và Loss weighting | **Tier 2 (Core Semantic Guardrail)**: Phân loại chính cho toàn bộ lưu lượng trước khi chuyển tiếp tới LLM. |
| **Thế hệ 3: Biểu diễn Ngữ nghĩa & Bất thường (Representation & Anomaly)** | **Dense k-NN Centroid Filter** (`all-MiniLM-L6-v2` + FAISS) <br> **Windowed Perplexity Filter** (TinyLlama / GPT-2) <br> **FastText** (TACL 2017) | 22M – 120M <br> FastText: ~10MB | 512 – 2,048 tokens | **0.2 – 2.0ms** (CPU) | **Khá**: Nhận diện tương đồng với các mẫu tấn công đã biết; phát hiện nhiễu ký tự | **Rất cao** (với Perplexity): Bắt trọn vẹn các chuỗi ký tự rác GCG/AutoDAN | **Tier 1 (Ultra-Fast Inline Gatekeeper)**: Lọc tức thì các chuỗi nhiễu và mẫu tấn công phổ biến trong $< 2\text{ms}$. |
| **Thế hệ 4: Baseline Thống kê Từ vựng** | **TF-IDF (Word + Char n-gram)** + LinearSVC / LogisticRegression | Không tham số mạng (~2MB) | Không giới hạn | **< 0.5ms** (CPU) | **Cơ bản**: Bắt các từ khóa nhạy cảm, chỉ thị ép buộc lộ liễu | **Thấp**: Dễ bị qua mặt bởi homoglyphs, tách từ, từ đồng nghĩa | **Thực nghiệm đối chuẩn (Empirical Baseline)**: Điểm tựa tối thiểu để đo lường mức cải thiện của các mô hình học sâu. |

---

## 3. CHI TIẾT TỪNG TRƯỜNG PHÁI MÔ HÌNH SOTA MỞ RỘNG

### 3.1. Thế hệ 1: SLM Guardrail Chuyên biệt (Generative Small Language Models)

#### A. Llama Guard 3 1B (Meta AI, 09/2024)
- **Nguồn gốc khoa học**: Meta AI Technical Report (2024), phát triển trên nền tảng Llama 3.2 1B Instruction-tuned.
- **Đặc trưng kiến trúc**:
  - Tối ưu hóa chuyên biệt cho nhiệm vụ phân loại an toàn theo chuẩn MLCommons AI Safety Taxonomy (Hazard categories: Prompt Injection, Harmful Content, Software Attacks).
  - Kích thước siêu nhỏ gọn (1 tỷ tham số), khi lượng tử hóa INT4 / GGUF chỉ chiếm ~700MB RAM, có khả năng chạy cục bộ trên thiết bị biên (edge devices) hoặc máy chủ CPU thông thường.
- **Giá trị ứng dụng cho PI-Guard**:
  - Không cần phân loại toàn bộ 100% request bằng Llama Guard 3 1B. Sử dụng mô hình này như một **"Trọng tài cấp cao (High-Assurance Arbiter)"** ở Tier 3: Khi Tier 2 (ModernBERT) đưa ra xác suất nằm trong khoảng bất định (uncertainty range $[0.35, 0.65]$), request sẽ được chuyển sang Llama Guard 3 1B để thẩm định sâu.

#### B. Granite Guardian 3.0 / 3.1 2B (IBM Research, 12/2024 — arXiv:2412.07724)
- **Nguồn gốc khoa học**: Padhi et al., *"Granite Guardian: A Family of Open Models for Content Safety and Risk Detection"*, arXiv:2412.07724, 2024.
- **Đặc trưng kiến trúc**:
  - Được huấn luyện chuyên biệt trên tập dữ liệu rủi ro toàn diện: Jailbreak, Direct/Indirect Prompt Injection, RAG Hallucination, Ungrounded Claims.
  - Hỗ trợ cả hai chế độ: Trả về nhãn phân loại (Risk / Safe) và giải thích nguyên nhân rủi ro (Risk reasoning).

---

### 3.2. Thế hệ 2: Next-Gen Encoder-Only Transformers (Ứng viên thay thế hoàn hảo cho DeBERTa)

#### A. ModernBERT-base (Answer.AI & LightOn, 12/2024 — arXiv:2412.13663)
- **Nguồn gốc khoa học**: Warner et al., *"ModernBERT: Bringing Modern Transformer Innovations to Pre-trained Encoders"*, arXiv:2412.13663, 2024.
- **Đặc trưng kiến trúc đột phá**:
  1. **Ngữ cảnh bản địa 8,192 tokens** (so với 512 của BERT/DeBERTa): Giúp phân tích trọn vẹn các payload gián tiếp (Indirect Prompt Injection) ẩn sâu trong tài liệu RAG dài mà không bị cắt cụt (truncation).
  2. **Tốc độ suy luận vượt trội**: Tích hợp Rotary Position Embeddings (RoPE), GeGLU activations, FlashAttention-2 và Unpadding. Cho thông lượng (throughput) trên GPU gấp **2.0x – 2.5x** và trên CPU nhanh hơn **40% – 60%** so với DeBERTa-v3-base ở cùng kích thước (~149M tham số).
  3. **Độ chính xác cao hơn**: Đạt điểm GLUE trung bình cao hơn DeBERTa-v3 trên hầu hết các tác vụ phân loại văn bản.
- **Định vị trong PI-Guard**: **Mô hình vô địch tiềm năng (Primary Champion Candidate)** tại Tier 2, thay thế hoặc đối sánh trực tiếp với `microsoft/deberta-v3-base`.

#### B. BGE-Reranker-v2-m3 / Cross-Encoder Interaction ($S \leftrightarrow U$)
- **Nguồn gốc khoa học**: Chen et al., *"BGE M3-Embedding: Multi-Lingual, Multi-Functionality, Multi-Granularity Text Embeddings"*, arXiv:2402.03216, 2024.
- **Đặc trưng kiến trúc**:
  - Thay vì chỉ đưa prompt người dùng $U$ vào mô hình, kiến trúc Cross-Encoder nhận đồng thời cặp:
    $$\text{Input} = [\text{CLS}] \mathbin{\Vert} S \mathbin{\Vert} [\text{SEP}] \mathbin{\Vert} U \mathbin{\Vert} [\text{EOS}]$$
  - Cơ chế Full Self-Attention giữa từng token của $S$ (System Prompt) và từng token của $U$ (User Prompt) cho phép mô hình tính toán trực tiếp **mức độ xung đột ngữ nghĩa (Semantic Contradiction)** giữa chỉ thị của hệ thống và yêu cầu của người dùng.
- **Định vị trong PI-Guard**: Mô hình chuyên biệt giải quyết bài toán phân định quyền ưu tiên chỉ thị (**Instruction Hierarchy** — Wallace et al., 2024).

---

### 3.3. Thế hệ 3: Biểu diễn Ngữ nghĩa Nhanh & Phát hiện Bất thường (Non-Generative, < 2ms)

#### A. Windowed Perplexity & Token Likelihood Anomaly Filter
- **Nguồn gốc khoa học**: 
  - Alon & Kamfonas, *"Detecting Language Model Attacks with Perplexity"*, arXiv:2308.14132, 2023.
  - Jain et al., *"Baseline Defenses for Adversarial Attacks on Large Language Models"*, NeurIPS 2023.
- **Cơ chế hoạt động**:
  - Các cuộc tấn công tối ưu hóa đối kháng (như GCG — Zou et al., 2023; AutoDAN — Liu et al., 2024) thường tạo ra các chuỗi hậu tố (adversarial suffixes) có tính chất ngữ pháp dị thường (ví dụ: `! ! ! == == describe tutorial ...`).
  - Sử dụng một mô hình ngôn ngữ kích thước siêu nhỏ (như GPT-2 124M hoặc TinyLlama 1.1B INT4) tính toán Perplexity (PPL) trượt trên từng cửa sổ $k$ tokens.
  - Nếu $\text{PPL}_{\text{window}} > \tau_{\text{ppl}}$, chuỗi bị đánh dấu là đối kháng ngay lập tức trong $< 1.5\text{ms}$.

#### B. Dense Semantic Distance Centroid Filter (Vector Space k-NN)
- **Nguồn gốc khoa học**: Reimers & Gurevych, *"Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks"*, EMNLP 2019; Johnson et al., *"Billion-scale similarity search with FAISS"*, IEEE TBD 2019.
- **Cơ chế hoạt động**:
  - Trích xuất vector embedding 384 chiều bằng mô hình siêu nhẹ `sentence-transformers/all-MiniLM-L6-v2` (~22M tham số, suy luận CPU ~1.2ms).
  - Dùng FAISS tìm kiếm khoảng cách Cosine / Mahalanobis tới tâm cụm (centroids) của các họ tấn công đã biết (DAN, Jailbreak, System Override).
  - Độ trễ truy vấn vector $< 0.1\text{ms}$, loại trừ 70% các đợt tấn công lặp lại hoặc biến thể bề mặt.

#### C. FastText (Bojanowski et al., TACL 2017)
- **Cơ chế hoạt động**: Sử dụng túi ký tự n-gram (bag of character n-grams) kết hợp cây phân cấp softmax (Hierarchical Softmax).
- **Ưu thế**: Miễn nhiễm hoàn toàn với lỗi tràn từ vựng (Out-of-Vocabulary / OOV) khi kẻ tấn công chèn ký tự lạ, khoảng trắng ẩn hoặc lỗi chính tả cố ý. Độ trễ suy luận $< 0.2\text{ms}$ trên CPU.

---

## 4. ĐỀ XUẤT KIẾN TRÚC PHÂN TẦNG TỔNG THỂ CHO ĐỒ ÁN PI-GUARD

Thay vì phụ thuộc đơn lẻ vào TF-IDF hoặc DeBERTa, kiến trúc đề xuất cho **PI-Guard** là một hệ thống **Phòng thủ Đa tầng (Multi-Tier Defense-in-Depth Cascade)** với cơ chế kiểm soát rủi ro tuân thủ toán học:

```mermaid
graph TD
    UserPrompt["Incoming User Prompt (U)"] --> Tier0["Tier 0: Pre-processing & Heuristic Decoders<br>(Unicode NFKC, Homoglyph, Base64/Hex/Rot13)"]
    Tier0 --> Tier1["Tier 1: Ultra-Fast Inline Filter (< 2ms)<br>FastText / TF-IDF + Windowed Perplexity"]
    
    Tier1 -->|Known Attack / High PPL Anomaly| Block1["Block: Attack Detected (Fast-Path)"]
    Tier1 -->|Ambiguous / Benign| Tier2["Tier 2: Deep Semantic Guardrail (10-20ms)<br>ModernBERT-base / DeBERTa-v3-base"]
    
    Tier2 -->|High Confidence Attack Score > T_high| Block2["Block: Prompt Injection / Jailbreak"]
    Tier2 -->|High Confidence Benign Score < T_low| Allow["Allow: Forward to Downstream LLM"]
    Tier2 -->|Borderline / Uncertain [T_low, T_high]| Tier3["Tier 3: High-Assurance Arbiter (50-100ms - Async/Edge)<br>Llama Guard 3 1B (INT4) / Granite Guardian 2B"]
    
    Tier3 -->|Flagged| Block3["Block: Policy Violation"]
    Tier3 -->|Safe| Allow
    
    CRC["Conformal Risk Control<br>(Angelopoulos et al. 2024)<br>Guarantees FPR <= 1.5%"] -.->|Calibrates Thresholds| Tier2
```

### Ưu điểm vượt trội của kiến trúc mở rộng:
1. **Tiết kiệm tài nguyên tối đa**: 60–80% yêu cầu thông thường hoặc tấn công lộ liễu được xử lý triệt để tại Tier 1 ($< 2\text{ms}$), không tốn chi phí chạy qua mạng Transformer sâu.
2. **Khắc phục triệt để điểm yếu của DeBERTa**: ModernBERT mở rộng cửa sổ ngữ cảnh lên **8,192 tokens** và tăng tốc độ xử lý gấp đôi, giải quyết trọn vẹn rủi ro cắt cụt dữ liệu trong các ứng dụng RAG.
3. **Ngăn chặn triệt để tấn công đối kháng sinh tự động**: Tầng Perplexity Filter xử lý các chuỗi GCG/AutoDAN mà các bộ phân loại ngữ nghĩa thông thường thường bị đánh lừa.
4. **Bảo đảm độ tin cậy khoa học có chứng minh**: Ngưỡng quyết định $\hat{\tau}$ được hiệu chuẩn bằng thuật toán Conformal Risk Control, bảo đảm tỷ lệ báo động nhầm trên tập dữ liệu lành tính $\text{FPR} \le 1.5\%$ với độ tin cậy thống kê $1 - \alpha$.

---

## 5. LỘ TRÌNH THỰC NGHIỆM ĐỀ XUẤT CHO NHÓM

1. **Giai đoạn 1 (Hiện tại — Baseline & Validation)**:
   - Duy trì `TF-IDF + LinearSVC` và `DeBERTa-v3-base` làm mốc đối chuẩn tối thiểu (Benchmark Baselines) trong báo cáo học thuật.
   - Hoàn thiện bộ sinh nhãn và đo lường độ trễ trên CPU tại `workspaces/truongnv/src/models/transformer_models.py`.
2. **Giai đoạn 2 (Mở rộng SOTA — ModernBERT & Perplexity)**:
   - Tích hợp `ModernBERT-base` (`answerdotai/ModernBERT-base`) vào pipeline phân loại nhị phân / đa nhãn.
   - Thử nghiệm bổ sung `WindowedPerplexityDetector` để kiểm thử độ bền trước tập tấn công đối kháng `JailbreakBench` (Chao et al., NeurIPS 2024).
3. **Giai đoạn 3 (Hiệu chuẩn & Tích hợp Proxy)**:
   - Ứng dụng `ConformalRiskCalibrator` trên điểm số đầu ra của ModernBERT để tìm ngưỡng tối ưu đạt $\text{FPR} \le 1.5\%$.
   - Đóng gói pipeline đa tầng vào FastAPI proxy server với thời gian phản hồi P95 $< 30\text{ms}$.
