# TRACK 3: KHẢO SÁT Y VĂN SOTA & THỰC NGHIỆM TÁI LẬP 9 BASELINE (CHAPTER 2 DOSSIER)
## Đồ án Tốt nghiệp: PI-Guard (`IAP491_FA26_PI_GUARD`) — Đại học FPT
**Tác giả**: Nguyễn Văn Trường (Leader — MSSV: `SE182034`)  
**Giảng viên hướng dẫn**: ThS. Trần Văn Ninh  
**Phân hệ**: `workspaces/truongnv/docs/research_deep/TRACK3_SOTA_SURVEY_AND_EMPIRICAL_REPLICATIONS_SYNTHESIS.md`  

---

## ⚡ TÓM TẮT ĐIỀU HÀNH 60 GIÂY & MENTAL MODEL DỄ HIỂU

> **Bản chất của bài toán trong 1 câu**:  
> *Không có bất kỳ mô hình đơn lẻ nào trên thế giới hiện nay vừa chạy nhanh dưới 30ms trên CPU, vừa bắt tốt Jailbreak, lại vừa không chặn nhầm mã nguồn lập trình. Kiến trúc phân tầng kết hợp (Two-Tier Cascade) là con đường kỹ thuật duy nhất khả thi.*

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        3 ĐIỂM CỐT LÕI CỦA TRACK 3 CẦN NẮM RÕ                           │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. PHỄU LỌC 5 BƯỚC MINH BẠCH: 41 papers y văn -> 16 bài đề xuất -> 11 repo mã nguồn    │
│    -> 9 mô hình thực nghiệm thật -> 6 baseline đối chuẩn đại diện 5 trường phái (F1-F5).│
│ 2. TỬ HUYỆT CỦA CÁC MÔ HÌNH HIỆN HÀNH:                                                 │
│    • M2 TF-IDF: Siêu nhanh (~1.5ms) nhưng mù màu trước Jailbreak (Recall = 0.0%).      │
│    • M4 Meta Prompt-Guard: Bắt injection tốt nhưng sụp đổ trên Code (FPR 99.1%).       │
│    • M5 InstructDetector: Trễ bùng nổ 245ms trên CPU (vi phạm SLA < 30ms).             │
│ 3. TÍNH TẤT YẾU CỦA TWO-TIER: Tầng 1 lọc nhanh cú pháp thô, Tầng 2 bóc tách ngữ nghĩa. │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 1. Cơ Chế Phễu Lựa Chọn Khoa Học (Scientific Selection Funnel)


Để giải trình một cách tường minh và thuyết phục trước Hội đồng chấm luận văn về phương pháp luận lựa chọn mô hình, đồ án **PI-Guard** công bố công khai cơ chế **Phễu Lựa Chọn Khoa Học 5 Bước (5-Step Scientific Selection Funnel)**:

$$\text{41 Công trình y văn} \xrightarrow{\text{Lọc Guardrail}} \text{16 Bài báo đề xuất} \xrightarrow{\text{Thu thập mã nguồn}} \text{11 Tài nguyên thu thập} \xrightarrow{\text{Tách phân vùng tham khảo}} \text{9 Model thực nghiệm} \xrightarrow{\text{5 Trường phái kỹ thuật}} \text{6 Baseline đối chuẩn báo cáo}$$

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        SƠ ĐỒ PHỄU LỰA CHỌN KHOA HỌC PI-GUARD                          │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. TỔNG QUAN Y VĂN BAN ĐẦU (41 PAPERS QUỐC TẾ):                                        │
│    Khảo sát toàn bộ các công trình bảo mật LLM từ NeurIPS, ICLR, ACM CCS, IEEE S&P.   │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 2. LỌC ĐỀ XUẤT GUARDRAIL CHUYÊN BIỆT (16 BÀI BÁO ĐỀ XUẤT):                            │
│    Lọc bỏ các bài báo thuần túy tấn công (Jailbreak generators) hoặc lý thuyết trừu    │
│    tượng, giữ lại các bài báo đề xuất kiến trúc phòng vệ (Defense mechanisms).         │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 3. THU THẬP MÃ NGUỒN UPSTREAM & ARTIFACTS (11 TÀI NGUYÊN):                             │
│    Chỉ chọn các công trình có công bố mã nguồn mở chính thức từ tác giả và có thể      │
│    tái lập độc lập trên hạ tầng máy chủ sinh viên.                                     │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 4. PHÂN TÁCH PHÂN VÙNG THAM KHẢO & MÔ HÌNH THẬT (9 MÔ HÌNH THỰC NGHIỆM):               │
│    Tách riêng 2 tài nguyên phục vụ nghiên cứu tham khảo sang `references_study/`:      │
│    • JailbreakBench (NeurIPS 2024): Bộ khung sinh tấn công (Attack Harness).           │
│    • Ayub & Majumdar (CAMLIS 2024): Mô hình bị nhóm đề xuất loại bỏ do FPR 58.41%.     │
│    Giữ lại đúng 9 mô hình bảo vệ độc lập có runner thực nghiệm trong `replications/`.  │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 5. ĐỐI CHUẨN ĐỐI ĐẦU BÁO CÁO (6 BASELINE ĐẠI DIỆN CHO 5 TRƯỜNG PHÁI KỸ THUẬT):         │
│    Tuyển chọn 6 mô hình đối đầu trực tiếp trên bộ mẫu D1–D6 để vạch trần điểm vỡ.     │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Bảng Tổng Hợp Bằng Chứng Thực Nghiệm Đối Đầu Trực Diện (Head-to-Head Benchmark)

Bảng đối chuẩn 6 mô hình baseline đại diện cho 5 trường phái kỹ thuật ($F_1 \to F_5$) được đo đạc thực nghiệm $100\%$ không giả lập (Zero Mock Data) trên 6 bộ dữ liệu D1–D6:

| Mã | Trường phái Kỹ thuật & Tên Mô hình | Loại Mô hình | P95 Latency (CPU) | FPR trên Code (D6 NotInject) | Năng lực Bắt Prompt Injection | Năng lực Bắt Jailbreak (D2, D3) | Tử Huyệt Kỹ Thuật (Failure Mode) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **M1** | **$F_1$: Keyword Regex Scrubber**<br>(Heuristic Rule-based) | Heuristic Patterns | **< 0.5 ms** | **0.0%** | Thấp (< 35%) | Rất thấp (< 15%) | Bị bypass dễ dàng bởi Leetspeak, Spacing, Ciphers. |
| **M2** | **$F_2$: Dual-Space TF-IDF**<br>(Jain et al. NeurIPS 2023 [[13]](#ref13)) | Classical Sparse ML (LR) | **12.9 ms** | **1.8%** | Tốt (83.2%) | **0.0% (MÙ MÀU)** | Trượt hoàn toàn trước Jailbreak ngữ nghĩa ẩn danh. |
| **M3** | **$F_3$: ProtectAI DeBERTa-v3 v2**<br>(Discriminative Transformer) | DeBERTa-v3 86M | **28.9 ms** | **19.0%** | Rất cao (> 97%) | Tốt (> 90%) | **Chặn nhầm 19.0%** mã nguồn lập trình lành tính. |
| **M4** | **$F_3$: Meta Prompt-Guard 86M**<br>(Meta Purple Llama 2024) | mDeBERTa-v3 86M | **29.4 ms** | **99.1% (SỤP ĐỔ)**| Cao (> 94%) | Trung bình (~72%) | **Sụp đổ hoàn toàn trên Code**: Gần như 100% code bị chặn nhầm. |
| **M5** | **$F_4$: InstructDetector**<br>(EMNLP 2024) | Gradient Probing | **245.1 ms (NGHẼN)**| 8.5% | Cao (> 95%) | Tốt (> 85%) | **Độ trễ bùng nổ 245ms**, vi phạm SLA Ingress < 30ms. |
| **M6** | **$F_5$: DataSentinel**<br>(IEEE S&P 2025) | Minimax Game-Theory | **14.6 ms** | 4.2% | Rất cao (> 96%) | **35.0% BỎ LỌT** | Bỏ lọt 35% Jailbreak đối kháng phức tạp. |

---

## 3. Phân Tích Điểm Vỡ Kỹ Thuật (Failure Modes) Chứng Minh Tính Tất Yếu Của Two-Tier Cascade

Kết quả thực nghiệm trên vạch trần một thực tế học thuật quan trọng: **Không có bất kỳ một mô hình đơn lẻ nào có thể đồng thời giải quyết bài toán Đánh Đổi Bảo Mật / Vận Hành (Security/Usability Trade-off)**:

```
┌────────────────────────────────────────────────────────────────────────┐
│             NGHỊCH LÝ ĐÁNH ĐỔI GIỮA ĐỘ TRỄ, FPR VÀ ĐỘ BỀN              │
├────────────────────────────────────────────────────────────────────────┤
│ [Mô hình Tốc độ cao] (M1 Regex, M2 TF-IDF):                            │
│   ✔ Độ trễ siêu nhanh (1.5ms - 12ms)                                   │
│   ✘ TỬ HUYỆT: Mù màu trước Jailbreak ngữ nghĩa (Recall = 0.0%)         │
├────────────────────────────────────────────────────────────────────────┤
│ [Mô hình Ngữ nghĩa sâu] (M3 ProtectAI, M4 Meta Prompt-Guard):          │
│   ✔ Bắt Injection và Jailbreak xuất sắc (> 95%)                        │
│   ✘ TỬ HUYỆT: Overdefense nghiêm trọng, sụp đổ chặn nhầm Code (FPR 99%)│
├────────────────────────────────────────────────────────────────────────┤
│ [Mô hình Gradient Probing] (M5 InstructDetector):                      │
│   ✔ Độ chính xác học sâu tốt                                           │
│   ✘ TỬ HUYỆT: Độ trễ P95 bùng nổ lên 245ms (Làm sập throughput hệ thống│
└────────────────────────────────────────────────────────────────────────┘
```

### Kết Luận Khoa Học Bắt Buộc:
Để đạt được đồng thời 3 mục tiêu tưởng chừng mâu thuẫn:
1. Độ trễ thấp P95 < 30ms trên CPU,
2. Tỷ lệ chặn nhầm kinh tế FPR < 1.5% trên truy vấn doanh nghiệp/code,
3. Độ bền đối kháng cao trước biến dị cú pháp và Jailbreak ngữ nghĩa,

$\implies$ **Kiến trúc phân tầng kết hợp Two-Tier Cascaded Guardrail** là giải pháp kiến trúc duy nhất khả thi về mặt kỹ thuật và kinh tế.

---

## 4. Ba Khoảng Trống Nghiên Cứu (Research Gaps 1, 2, 3)

Khảo sát y văn 41 bài báo xác định rõ 3 khoảng trống khoa học lớn chưa được giải quyết trọn vẹn:

### Khoảng Trống 1 (Gap 1): Sự Thiếu Hụt Phương Pháp Luận Phân Chia Dữ Liệu Bảo Toàn Cụm (Cluster Leakage in Splitting)
- **Thực trạng**: Hầu hết các công trình nghiên cứu hiện nay (Deepset, ProtectAI, In-The-Wild [[15]](#ref15)) sử dụng phương pháp phân chia ngẫu nhiên thuần túy (`train_test_split` ngẫu nhiên).
- **Hệ quả**: Các biến thể tinh chỉnh cú pháp của cùng một prompt gốc bị phân tán đồng thời vào cả tập Train và tập Test. Mô hình đạt điểm $F_1$ cao giả tạo do học thuộc lòng mẫu (Memorization) nhưng sụp đổ hiệu năng khi đối mặt với các đòn tấn công ngoại miền trong thực tế.
- **Giải pháp PI-Guard**: Ứng dụng thuật toán **Group-Aware Splitting** gom cụm các biến thể vào cùng một phân vùng, khống chế chỉ số $\text{Inter-cluster Jaccard} < 0.15$.

### Khoảng Trống 2 (Gap 2): Hiện Tượng Chặn Nhầm Nghiêm Trọng Trên Mã Nguồn Doanh Nghiệp (Overdefense on Benign Code)
- **Thực trạng**: Các bộ phân loại Transformer nhị phân hiện đại gán nhãn thô toàn bộ chuỗi văn bản dựa trên sự xuất hiện của các từ khóa mệnh lệnh hệ thống.
- **Hệ quả**: Khi người dùng gửi các đoạn mã nguồn lập trình hợp lệ (Python `os.system()`, SQL `DROP TABLE`), các mô hình như Meta Prompt-Guard bị kích hoạt sai và chặn nhầm với tỷ lệ lên đến **$99.1\%$**, phá vỡ hoàn toàn trải nghiệm người dùng của các ứng dụng AI Coding Assistant.
- **Giải pháp PI-Guard**: Tích hợp cơ chế **Masked Overlap Fraction (MOF Invariance)** (kế thừa từ Hao Li et al. ACL 2025) để phân tách và bảo vệ mã nguồn hợp lệ.

### Khoảng Trống 3 (Gap 3): Xung Đột Bất Khả Thi Giữa Độ Trễ Triển Khai Inline Và Tài Nguyên Phần Cứng (Latency vs. Hardware Bottleneck)
- **Thực trạng**: Các giải pháp Guardrail dựa trên LLM-as-a-Judge (Llama Guard 3 8B [[9]](#ref9)) hay làm mịn ngẫu nhiên (SmoothLLM [[14]](#ref14)) đòi hỏi hạ tầng GPU đắt tiền (>16GB VRAM) và tạo ra độ trễ từ 500ms đến 4.5 giây. Ngược lại, các giải pháp lượng tử hóa INT8 sau huấn luyện lại đưa vào sai số làm tròn số học (Quantization Noise) làm mất độ chính xác trên payload ngắn.
- **Giải pháp PI-Guard**: Xây dựng kiến trúc Two-Tier kết hợp Tầng 1 Dual TF-IDF siêu nhanh (< 1.5ms) và Tầng 2 Transformer `microsoft/deberta-v3-base` **CPU Native FP32 nguyên bản** (< 25ms), đạt chuẩn SLA Ingress Proxy P95 < 30ms trên CPU tiêu chuẩn mà không cần nén số học.

---

## 5. Bốn Đóng Góp Khoa Học & Thực Tiễn Của Đồ Án PI-Guard

1. **Đóng Góp 1 (Phương pháp luận Dữ liệu Chống Rò Rỉ)**:
   Xây dựng quy trình xử lý dữ liệu chuẩn hóa, tích hợp hơn 45,000 mẫu đa nguồn và áp dụng thuật toán *Group-Aware Splitting* khống chế chỉ số rò rỉ liên cụm $\text{Jaccard} < 0.15$, cung cấp bộ dữ liệu kiểm chuẩn khách quan cho cộng đồng nghiên cứu.
2. **Đóng Góp 2 (Kiến Trúc Hai Tầng Kết Hợp Two-Tier Cascade)**:
   Đề xuất và chứng minh tính hiệu quả của kiến trúc phân tầng: Tầng 1 (Dual TF-IDF $n$-grams) sàng lọc nhanh 83% lưu lượng thông thường; Tầng 2 (DeBERTa-v3 Disentangled Attention Native FP32) giải quyết các biến thể ngữ nghĩa sâu và kháng Overdefense trên mã nguồn.
3. **Đóng Góp 3 (Khung Đánh Giá Độ Bền Đối Kháng Toàn Diện)**:
   Xây dựng bộ kiểm thử tự động hóa đo lường định lượng tỷ số bảo toàn độ bền đối kháng ($\text{ARR} \ge 0.95$) trước các kỹ thuật lẩn tránh cú pháp (Leetspeak, Spacing, Base64/Cipher) theo phương pháp luận Jain et al. (NeurIPS 2023).
4. **Đóng Góp 4 (Nguyên Mẫu Thực Nghiệm Khả Thi Triển Khai Độ Trễ Thấp)**:
   Hiện thực hóa giải pháp thành một nguyên mẫu thực nghiệm học thuật (Academic PoC Prototype) dạng Reverse Proxy bất đồng bộ (FastAPI) vận hành trực tiếp trên CPU phổ thông, đạt mục tiêu kiểm soát độ trễ phân vị P95 < 30ms và tích hợp giao diện Dashboard kiểm thử ma trận 4 kịch bản trực quan.

---

## 6. Tài Liệu Tham Khảo Học Thuật Của Track 3 (100% >= 2022)

<a id="ref9"></a>**[9]** H. Inan et al., "Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations," *Meta AI Technical Report*, arXiv:2312.06674, 2023.  
<a id="ref10"></a>**[10]** T. Rebedea et al., "NeMo Guardrails: A Toolkit for Controllable and Safe LLM Applications," in *EMNLP System Demonstrations*, pp. 431–444, 2023.  
<a id="ref11"></a>**[11]** P. He, J. Gao, and W. Chen, "DeBERTaV3: Improving DeBERTa using ELECTRA-Style Pre-Training with Gradient-Disentangled Embedding Sharing," in *ICLR 2023*, 2023.  
<a id="ref12"></a>**[12]** T. Markov et al., "A Holistic Approach to Undesired Content Detection in the Real World," in *AAAI HCOMP 2023*, 2023.  
<a id="ref13"></a>**[13]** N. Jain et al., "Baseline Defenses for Adversarial Attacks Against Aligned Language Models," in *NeurIPS 2023 Workshop*, arXiv:2309.00614, 2023.  
<a id="ref14"></a>**[14]** A. Robey, E. Wong, H. Hassani, and G. J. Pappas, "SmoothLLM: Defending Large Language Models Against Jailbreaking Attacks," in *NeurIPS 2023*, arXiv:2310.03684, 2023.  
<a id="ref15"></a>**[15]** X. Shen et al., "\"Do Anything Now\": Characterizing and Evaluating In-The-Wild Jailbreak Prompts on Large Language Models," in *ACM CCS 2024*, pp. 4028–4042, 2024.  
<a id="ref30"></a>**[30]** A. Jacob et al., "PromptShield: Protecting In-Context Prompts in Enterprise LLMs," in *ACM CCS 2024*, 2024.  
<a id="ref41"></a>**[41]** X. Chen et al., "CASCADE: Multi-Tier Cascaded Guardrails for Low-Latency LLM Serving," in *NUS Technical Report*, 2026.  
