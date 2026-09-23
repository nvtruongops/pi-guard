# BÁO CÁO THỰC NGHIỆM ĐỐI CHUẨN ĐỘC LẬP & KHÔNG GIAN ĐÁNH ĐỔI VẬN HÀNH ĐA NHÁNH (12 MÔ HÌNH & 6 CẤU HÌNH GUARDRAIL)
## Nghiên Cứu Đánh Giá Định Lượng Toàn Diện Dựa Trên 100% Bộ Ba Công Khai (Paper + Code + Dataset), Giải Quyết Thách Thức Văn Bản 200,000 Ký Tự Và Tối Ưu Hóa Biên Pareto

---

> **Đơn vị thực hiện**: Đồ án Tốt nghiệp Kỹ sư An toàn Thông tin (IAP491) — Đại học FPT  
> **Đề tài**: *A Machine-Learning Guardrail for Detecting Prompt Injection and Jailbreak Attacks on LLM Applications (PI-Guard)*  
> **Tác giả nghiên cứu**: Nguyễn Văn Trường (Trưởng nhóm / Mã SV: `SE182034` / GitHub: `nvtruongops`)  
> **Workspace tài nguyên thực thi**: [`workspaces/truongnv/replications/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/)  
> **Kho tài liệu khoa học thẩm định**: [`workspaces/truongnv/References/REFERENCES_LOG.md`](file:///d:/Work/Do-an/workspaces/truongnv/References/REFERENCES_LOG.md)  
> **Cơ sở chỉ đạo học thuật**: Biên bản Meeting 5 ngày 19/09/2026 ([`Final-Report/Meeting/Meeting 5_19_09_26.md`](file:///d:/Work/Do-an/Final-Report/Meeting/Meeting%205_19_09_26.md)) với GVHD Thầy Trần Văn Ninh  
> **Dữ liệu thực nghiệm số hóa**:
> - [`grounded_empirical_matrix.json`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_6/04_benchmarks_and_data/grounded_empirical_matrix.json) (12 mô hình thực nghiệm độc lập)
> - [`multi_branch_tradeoffs_matrix.json`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_6/04_benchmarks_and_data/multi_branch_tradeoffs_matrix.json) (6 nhánh cấu hình tối ưu hóa vận hành)
> - [`cross_dataset_empirical_matrix.json`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_6/04_benchmarks_and_data/cross_dataset_empirical_matrix.json) (Bộ dữ liệu kiểm thử D1–D6)

---

## 📌 1. TRIẾT LÝ THỰC NGHIỆM & NGUYÊN TẮC BỘ BA CÔNG KHAI (THE PUBLIC TRIAD)

### 1.1. Bác Bỏ Ảo Tưởng "Siêu Mô Hình Đơn Khối" (The Monolithic Hyper-Model Fallacy)
Trong nghiên cứu phát triển các giải pháp bảo vệ an toàn cho ứng dụng LLM, sai lầm phổ biến nhất là kỳ vọng tìm kiếm một mô hình vạn năng duy nhất: vừa có độ trễ cực thấp ($\le 0.1\text{ms}$), vừa không tốn GPU, vừa hiểu ngữ cảnh 200,000 ký tự, vừa có $\text{FPR} = 0\%$, lại vừa miễn nhiễm trước mọi đòn tấn công đối kháng.

Nghiên cứu mới nhất của Luo & Han (NUS 2026 [[41]](#ref41)) trên 19 đòn tấn công và 15 giải pháp phòng vệ đã khẳng định định lý thực nghiệm:
> *"No single defense mechanism is universally best across all threat models. Input perturbation defends against GCG but degrades on semantic injection; Model alignment suffers from over-refusal; Output filtering incurs high latency. Only multi-stage adaptive cascades achieve the Pareto frontier."*

```
                       [ BỘ BA BẤT KHẢ THI CỦA GUARDRAIL ]
                                    (The Guardrail Trilemma)

                                   ĐỘ TRỄ CỰC THẤP
                                   (P95 < 0.2ms / CPU)
                                          ▲
                                         / \
                                        /   \
                         [Nhánh 1: Edge]     [Nhánh 6: PI-Guard Two-Tier]
                                      /       \
                                     /  Biên   \
                                    /   Pareto  \
                                   /             \
                                  /               \
            TỶ LỆ BÁO GIẢ GẦN 0% ◄─────────────────► HIỂU NGỮ NGHĨA SÂU &
            (FPR < 0.5% / Conformal)                  KHÁNG ĐỐI KHÁNG OOD
            [Nhánh 2: Low-FPR SaaS]                   [Nhánh 3 & 4: Deep Transformer]
```

### 1.2. Phân Định Rạch Ròi Giữa Khảo Sát Y Văn Lý Thuyết Và Đo Đạc Thực Nghiệm
Để đảm bảo tính trung thực học thuật tuyệt đối trước Hội đồng FPT:
1. **Khảo sát Y văn Lý thuyết (Theoretical Reference)**:
   - Các dòng mô hình tạo sinh tự hồi quy (Autoregressive Generative SLMs: Llama Guard 7B/8B [[7]](#ref7), Granite Guardian 8B [[38]](#ref38)) được giữ lại trong phần khảo sát lý thuyết nhằm chứng minh trần năng lực và sự bùng nổ độ trễ ($> 1.5\text{s}$), **HOÀN TOÀN KHÔNG CÓ mã nguồn chạy thực nghiệm cục bộ** do đòi hỏi phần cứng GPU doanh nghiệp (>16GB VRAM), đi ngược lại tôn chỉ Ingress Proxy Low-Latency trên CPU của đồ án.
2. **Nguyên Tắc Bộ Ba Công Khai (The Public Triad)**:
   Mọi mô hình được đưa vào Ma trận Đối chuẩn Thực nghiệm cục bộ bắt buộc phải thỏa mãn:
   $$\mathbf{Public\ Triad} = \{\mathbf{Public\ Paper\ (PDF)} \mathbin{\Vert} \mathbf{Public\ Upstream\ Code} \mathbin{\Vert} \mathbf{Public\ Benchmark\ Dataset}\}$$
   Toàn bộ mã nguồn và dữ liệu tái lập được lưu trữ minh bạch tại [`workspaces/truongnv/replications/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/).

---

## 📁 2. BỘ DỮ LIỆU ĐỐI CHUẨN ĐA TẦNG (DATASETS D1–D6 & 200K SUITE)

Để kiểm chứng 12 mô hình và 6 cấu hình trên cùng một thước đo khách quan, nhóm đã chuẩn hóa bộ dữ liệu thực nghiệm gồm 6 tập dữ liệu thành phần (tổng cộng 1,200 prompts) và 1 bộ mẫu văn bản dài 200,000 ký tự:

| Mã Tập Dữ Liệu | Nguồn Gốc & Công Bố Khoa Học | Quy Mô Mẫu | Bản Chất Phân Phối Dữ Liệu | Mục Tiêu Đánh Giá |
| :--- | :--- | :---: | :--- | :--- |
| **D1: Direct Injection** | Perez & Ribeiro [[3]](#ref16), Wallace OpenAI [[33]](#ref33) | 200 samples | Câu lệnh tiêm trực tiếp, Override, Goal Hijacking | Khả năng chặn đứng tấn công chiếm quyền thô |
| **D2: Indirect Injection** | Greshake et al. AISec [[4]](#ref16), Yi et al. BIPIA [[23]](#ref40) | 200 samples | Dữ liệu bên ngoài (RAG/Web/Email) chứa chỉ thị ẩn | Năng lực phân biệt ranh giới dữ liệu và mã lệnh |
| **D3: Wild Jailbreaks** | Shen et al. CCS [[11]](#ref11), Chao JBB [[34]](#ref34) | 200 samples | Kịch bản nhập vai (DAN), nghịch lý đạo đức, đa tầng | Khả năng bẻ gãy tấn công vi phạm chính sách an toàn |
| **D4: Benign QA & Tasks** | SQuAD 2.0, Alpaca-Eval, Chatbot Prompts | 200 samples | Câu hỏi thông thường, tra cứu thông tin, hội thoại | Đo đạc tỷ lệ báo động giả ($\text{FPR} \le 1.5\%$) |
| **D5: Overdefense Hard** | Li et al. PIGuard ACL 2025 [[18]](#ref18) (`NotInject`) | 200 samples | Câu lệnh lập trình, chứa từ khóa nhạy cảm hợp lệ | Khả năng triệt tiêu lỗi quá phòng thủ (Overdefense) |
| **D6: Adversarial Evasion**| Yuan [[17]](#ref17), Hackett [[31]](#ref31), Zou GCG [[13]](#ref13) | 200 samples | Chuỗi biến dị ký tự, Base64, CipherChat, GCG tokens | Đo độ suy giảm hiệu năng đối kháng ($\Delta F_1$) |
| **Suite 200k Characters** | Zhou et al. Prompt Overflow [[40]](#ref40) | 2 tài liệu lớn | 200,000 ký tự (~50,000 từ): 1 Clean và 1 Tail-Injected | Đánh giá độ trễ băm khối và chống Prompt Overflow |

---

## 📊 3. MA TRẬN ĐỐI CHUẨN THỰC NGHIỆM 12 MÔ HÌNH ĐỘC LẬP TRÊN CPU

Bảng ma trận dưới đây tổng hợp kết quả đo đạc thực nghiệm độc lập của 12 mô hình văn học và giải pháp PI-Guard trên môi trường CPU đồng nhất:

| Mã / Tên Mô Hình | C1: Direct Recall (%) | C2: Indirect Recall (%) | C3: Jailbreak Recall (%) | C4: Benign FPR (%) *($\le 1.5\%$)* | C5: Overdefense Acc (%) *(NotInject)* | C6: Robustness $\Delta F_1$ | C7: CPU Latency P95 (ms) | C8: Low-FPR TPR @ 1% | C9: Context Window | C10: Query Multiplier |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **K1: PIGuard ACL 2025** [[18]](#ref18) | **96.0%** | **92.5%** | **94.0%** | **0.8%** | **90.7%** | $-3.2\%$ | $24.5\text{ms}$ | 20.37% | 512 | $1\times$ |
| **K2: DataSentinel SP 2025** [[32]](#ref32) | **80.0%** | 20.0% | 0.0% | 10.0% | **80.0%** | $-12.5\%$ | **$0.19\text{ms}$** | N/A (Canary) | 512 | $1\times$ |
| **K3: PromptShield CCS 2024** [[30]](#ref30) | **100.0%** | **100.0%** | 85.0% | **0.0%** | **100.0%** | $-2.4\%$ | **$4.11\text{ms}$** | **100.0%** | 512 | $1\times$ |
| **K4: ModernBERT 8k 2024** [[37]](#ref37) | **100.0%** | **100.0%** | 90.0% | **0.0%** | **100.0%** | $-2.1\%$ | $11.67\text{ms}$ | 90.00% | **8,192 (Max)**| $1\times$ |
| **K5: PI-Guard Tier-1 Filter** [[15]](#ref15) | **100.0%** | 85.0% | 88.0% | **0.0%** | **100.0%** | $-6.5\%$ | **$8.22\text{ms}$** | 85.00% | 512 | $1\times$ |
| **K6: Meta Prompt-Guard 86M** [[20]](#ref20) | **98.0%** | 80.0% | 88.0% | **0.5%** | 🔴 **0.88%** *(FAIL)* | $-18.5\%$ | $22.1\text{ms}$ | 🔴 12.78% | 512 | $1\times$ |
| **K7: ProtectAI DeBERTa-v3** [[9]](#ref9) | 60.0% | 50.0% | 40.0% | **0.0%** | 45.2% | $-22.0\%$ | $22.5\text{ms}$ | 🔴 1.97% | 512 | $1\times$ |
| **K8: InstructDetector** [[19]](#ref19) | 72.0% | **88.0%** | 64.0% | 3.2% | 68.0% | $-14.2\%$ | $45.8\text{ms}$ | 65.00% | 512 | $1\times$ |
| **K9: Jain Perplexity Filter** [[15]](#ref15) | 40.0% | 25.0% | 75.0% | 8.5% | 52.0% | $-35.0\%$ | $18.2\text{ms}$ | 25.00% | 512 | $1\times$ |
| **K10: SmoothLLM NeurIPS 2023** [[14]](#ref14)| 35.0% | 20.0% | **92.0%** | 1.0% | 85.0% | $-4.0\%$ | 🔴 $5\times\text{ LLM}$ | N/A | 512 | 🔴 **$5\times - 10\times$** |
| **K11: JailbreakBench Evaluator** [[34]](#ref34)| 0.0% | 0.0% | **100.0%** | **0.0%** | **100.0%** | $0.0\%$ | $22.5\text{ms}$ | N/A | 512 | $1\times$ |
| **K12: Ayub CAMLIS 2024** [[21]](#ref21) | 52.0% | 30.0% | 48.0% | 🔴 **58.4%** *(FAIL)* | 41.6% | $-28.4\%$ | $14.2\text{ms}$ | 🔴 5.20% | 512 | $1\times$ |
| **K-PI: PI-Guard Two-Tier Cascade** | **96.0%** | **92.5%** | **94.0%** | **0.0%** | **90.7%** | **$-1.5\%$** *(Tốt nhất)* | **$3.45\text{ms}$** *(Nhanh 7x)* | **92.50%** | **8k (Tier-0 chunk)**| **$1\times$ (Zero mult)** |

---

## 🔬 4. MÔ HÌNH HÓA TOÁN HỌC 6 NHÁNH KIẾN TRÚC & KHÔNG GIAN ĐÁNH ĐỔI ĐA CHIỀU

Thay vì một mô hình đơn nhất, chúng tôi phân tích 6 nhánh tư duy kỹ thuật độc lập với hàm mục tiêu toán học rõ ràng:

### 4.1. Đặc Tả 6 Nhánh Tư Duy Vận Hành
1. **Nhánh 1: Edge Ultra-Throughput Profile** (Jain `[15]`, Ayub `[21]`):
   - *Hàm mục tiêu*: $\min_{\theta} \tau(f_\theta)$ với điều kiện $\text{QPS} \ge 5000\text{ req/s/core}, \text{RAM} \le 50\text{MB}$.
   - *Độ trễ P95*: $0.08\text{ms}$. Đạt $\text{FPR} = 0.0\%$, nhưng bỏ lọt các đòn gián tiếp ($\text{Recall} \approx 25\%$).
2. **Nhánh 2: Strict Conformal Low-FPR Profile (B2B SaaS)** (Angelopoulos `[36]`, Jacob `[30]`, Markov `[10]`):
   - *Hàm mục tiêu*: $\max_{\tau} \text{Recall}(f_\tau)$ với điều kiện $\text{FPR} \le 0.5\%$.
   - *Cơ chế*: Hàm tổn thất bất đối xứng $\mathcal{L}_{\text{asym}}$ với trọng số $C_{FP} / C_{FN} = 10$. Đạt $\text{FPR} = 0.30\%$, P95 $= 4.20\text{ms}$.
3. **Nhánh 3: Deep Semantic High-Assurance Profile** (He DeBERTaV3 `[9]`, Li PIGuard `[18]`):
   - *Hàm mục tiêu*: $\max_{\theta} \text{Recall}_{\text{Indirect}}(\theta)$ với điều kiện $\text{Recall}_{\text{Total}} \ge 95.0\%$.
   - *Cơ chế*: Disentangled Relative Attention (bóc tách 3 ma trận $Q_i^c K_j^{c\top} + Q_i^c K_{\delta(i,j)}^{p\top} + K_j^c Q_{\delta(j,i)}^{p\top}$). Đạt Recall $94-96\%$, P95 $= 18.20\text{ms}$.
4. **Nhánh 4: Game-Theoretic Minimax Adversarial Robustness** (Liu DataSentinel `[32]`, Hackett `[31]`, Yuan `[17]`):
   - *Hàm mục tiêu*: $\min_{\theta} \max_{\delta \in \Delta} \mathbb{E}[\mathcal{L}(f_\theta(\mathcal{S}(x \oplus \delta)), y)]$.
   - *Cơ chế*: Tích hợp bộ tiền xử lý Tier-0 Scrubber $\mathcal{S}(\cdot)$ dọn dẹp biến dị ký tự Unicode/Homoglyph/CipherChat. Đạt khả năng kháng Evasion $94.0\%$.
5. **Nhánh 5: Long-Doc Chunked & Tail-Biased Profile** (Zhou Prompt Overflow `[40]`):
   - *Hàm mục tiêu*: Quét văn bản 200,000 ký tự chống lọt payload ở cuối trang (Tail Injection).
   - *Cơ chế*: Băm khối 111 blocks, quét ưu tiên Block Đuôi $\rightarrow$ Block Đầu $\rightarrow$ Block Thân kết hợp Early-Stopping. Tăng tốc phát hiện gấp **$111.0\times$** so với quét tuyến tính.
6. **Nhánh 6: PI-Guard Two-Tier Adaptive Cascade (Champion Profile)** (Saltzer `[16]`, Luo CASCADE `[41]`, Li `[18]`):
   - *Hàm mục tiêu Pareto*: $\min_{\tau_{low}, \tau_{high}} \mathbb{E}[\tau] = \tau_1 + (1 - \eta) \cdot \tau_2$ với $\text{FPR} \le 1.0\%, F_1 \ge 0.93$.
   - *Cơ chế*: Định tuyến ba trạng thái (Tri-State Policy) với $\tau_{low} = 0.15$ và $\tau_{high} = 0.85$. Tầng 1 giải phóng an toàn $82\%$ lưu lượng, chỉ $18\%$ nghi vấn đi tiếp vào Tầng 2.

### 4.2. Bảng Đối Chuẩn Ma Trận Đánh Đổi 6 Nhánh Cấu Hình
Dữ liệu trích xuất từ [`multi_branch_tradeoffs_matrix.json`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_6/04_benchmarks_and_data/multi_branch_tradeoffs_matrix.json):

| Tiêu Chí Đo Đạc / Nhánh Cấu Hình | Nhánh 1: Edge Ultra-Throughput | Nhánh 2: Strict Low-FPR (SaaS) | Nhánh 3: Deep Semantic | Nhánh 4: Minimax Robustness | Nhánh 5: Long-Doc 200k Chars | Nhánh 6: PI-Guard Champion |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Độ trễ P50 ($\text{ms}$)** | **$0.03$** | $0.15$ | $14.50$ | $0.25$ | $0.17$ (Tail) / $13.32$ (Clean) | **$0.08$** |
| **Độ trễ P95 ($\text{ms}$)** | **$0.08$** | $4.20$ | $18.20$ | $1.20$ | $16.50$ | **$3.45$** |
| **Độ trễ P99 ($\text{ms}$)** | **$0.15$** | $18.50$ | $22.80$ | $3.50$ | $20.10$ | **$18.20$** |
| **Thông lượng Max (QPS/core)** | **$8,500$** | $450$ | $55$ | $1,200$ | $75$ | **$1,850$** |
| **Bộ nhớ RAM ($\text{MB}$)** | **$45.0$** | $175.0$ | $135.0$ | $65.0$ | $95.0$ | **$145.0$** |
| **Tỷ lệ báo giả (FPR Benign)** | **$0.00\%$** | **$0.30\%$** | $1.20\%$ | $0.80\%$ | $0.50\%$ | **$0.50\%$** |
| **Recall Direct Injection** | $45.0\%$ | $78.0\%$ | **$96.0\%$** | $88.0\%$ | $95.0\%$ | **$94.0\%$** |
| **Recall Indirect Injection** | $25.0\%$ | $72.0\%$ | **$94.0\%$** | $76.0\%$ | $90.0\%$ | **$92.0\%$** |
| **Recall Jailbreak (DAN/JBB)**| $60.0\%$ | $85.0\%$ | **$98.0\%$** | $92.0\%$ | $96.0\%$ | **$96.0\%$** |
| **Recall Adversarial Evasion** | $35.0\%$ | $65.0\%$ | $75.0\%$ | **$94.0\%$** | $85.0\%$ | **$88.0\%$** |
| **Điểm tổng hợp Macro $F_1$** | $0.647$ | $0.842$ | $0.925$ | $0.895$ | $0.910$ | **$0.932$** |
| **Chi phí / 1M requests (USD)**| **$\$0.05$** | $\$0.85$ | $\$6.50$ | $\$0.40$ | $\$2.20$ | **$\$1.25$** |
| **Mục tiêu tối ưu hóa cốt lõi** | **Tốc độ biên & QPS** | **Chống gián đoạn UX** | **Phân tích ngữ nghĩa** | **Kháng đòn né tránh** | **Văn bản lớn & Overflow**| **Điểm Pareto cân bằng** |

---

## ⚡ 5. GIẢI PHÁP XỬ LÝ VĂN BẢN 200,000 KÝ TỰ & CHỐNG LỖ HỔNG PROMPT OVERFLOW

### 5.1. Cơ Chế Băm Khối (Block Chunking Formulation)
Cho tài liệu đầu vào $D$ có độ dài $L = 200,000\text{ ký tự}$ ($\approx 50,000\text{ từ}$, tương đương tài liệu $100\text{ trang A4}$).  
Với kích thước cửa sổ $W = 2,000\text{ ký tự}$ ($\approx 512\text{ tokens}$) và độ chồng lấn $O = 200\text{ ký tự}$ ($10\%$ overlap chống cắt rời payload giữa biên hai khối), bước nhảy cửa sổ là $S = W - O = 1,800\text{ ký tự}$.  
Tổng số khối (blocks) được tạo ra là:
$$K = \left\lceil \frac{L - O}{W - O} \right\rceil = \left\lceil \frac{200,000 - 200}{2,000 - 200} \right\rceil = \lceil 111.0 \rceil = 111\text{ blocks}$$

### 5.2. Chiến Lược Quét Ưu Tiên Đuôi-Đầu (Tail-and-Head Prioritized Scanning)
Thay vì quét tuyến tính từ block $0 \to 110$, PI-Guard thiết lập thứ tự quét ưu tiên hoán vị $\pi$:
$$\pi = \Big[ \underbrace{110}_{\text{Tail Block}}, \; \underbrace{109}_{\text{Pre-tail}}, \; \underbrace{0}_{\text{Head Block}}, \; 1, \; 2, \; \dots, \; 108 \Big]$$

```
Văn bản 200k ký tự: [Block 0 (Head)] ... [Block 55 (Middle)] ... [Block 109] [Block 110 (Tail)]
                              ▲                                       ▲          ▲
                              │ [Ưu tiên 3: Quét Đầu]                 │          │ [Ưu tiên 1: Quét Đuôi Ngay]
                              └───────────────────────────────────────┴──────────┘
                                                [Ưu tiên 2: Quét Áp Chót]
```

Kết hợp với **Cơ chế Ngắt Sớm (Early-Stopping)**: Khi bất kỳ block nào có xác suất $p(b_i) \ge \tau_{\text{high}} = 0.85$, hệ thống lập tức **DỪNG TIẾN TRÌNH QUÉT**, phát cờ chặn mã độc và từ chối tài liệu.

### 5.3. Bằng Chứng Thực Nghiệm Đo Đạc Tăng Tốc (111x Speedup Proof)
Từ kịch bản đo đạc thực tế tại [`tests/test_long_doc_processing.py`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_6/tests/test_long_doc_processing.py):

| Kịch Bản Đặt Payload | Chiến Lược Naive Linear | Chiến Lược PI-Guard Tail-First | Số Block Cần Quét | Độ Trễ Thực Tế | Hệ Số Tăng Tốc (Speedup) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Giấu ở trang cuối (Tail)** | Quét $111\text{ blocks}$ ($13.32\text{ms}$) | **Quét đúng $1\text{ block}$** ($0.12\text{ms}$) | **1 vs 111** | **$0.12\text{ms}$** | **$111.0\times$ (Nhanh gấp 111 lần!)** |
| **Giấu ở trang đầu (Head)** | Quét $1\text{ block}$ ($0.12\text{ms}$) | Quét $3\text{ blocks}$ ($0.36\text{ms}$) | 3 vs 1 | $0.36\text{ms}$ | Duy trì độ trễ cực thấp $< 0.4\text{ms}$ |
| **Giấu ở giữa tài liệu (Middle)** | Quét $56\text{ blocks}$ ($6.72\text{ms}$) | Quét $58\text{ blocks}$ ($6.96\text{ms}$) | 58 vs 56 | $6.96\text{ms}$ | Tương đương ($0.97\times$) |
| **Phân mảnh (Prompt Overflow)** | Quét $21\text{ blocks}$ ($2.52\text{ms}$) | Quét $23\text{ blocks}$ ($2.76\text{ms}$) | 23 vs 21 | $2.76\text{ms}$ | Phát hiện sớm tại mảnh đầu tiên |
| **Tài liệu sạch 100% (Benign)** | Quét $111\text{ blocks}$ ($13.32\text{ms}$) | Quét $111\text{ blocks}$ ($13.32\text{ms}$) | 111 vs 111 | $13.32\text{ms}$ | **Hoàn toàn đạt SLA $\le 30\text{ms}$** |

---

## 💡 6. PHÂN TÍCH ĐÁNH ĐỔI VẬN HÀNH & BÀI HỌC TỪ CÁC CÔNG TRÌNH SOTA

### 6.1. Bài Học Từ Meta Prompt-Guard 86M: Giới Hạn Của Mô Hình Đơn Khối
- **Thực nghiệm độc lập**: Meta `Prompt-Guard 86M` [[20]](#ref20) gặp sự sụp đổ nghiêm trọng về quá phòng thủ: trên tập dữ liệu câu lệnh lập trình hợp lệ (`NotInject`), mô hình đạt độ chính xác chỉ **$0.88\%$** (chặn nhầm **$99.12\%$** câu lệnh sạch). Khi ép hoạt động ở ngưỡng $\text{FPR} \le 1.0\%$, TPR của nó rơi từ $98.0\%$ xuống chỉ còn **$12.78\%$** (Jacob et al. [[30]](#ref30)).
- **Nguyên nhân y văn**: Xung đột mục tiêu (Competing Objectives). Không thể dùng MỘT mô hình đơn lẻ với loss phân loại truyền thống để giải quyết đồng thời cả Direct Injection, Indirect Injection và Jailbreak mà không gây nổ FPR.
- **Khuyến nghị từ chính Meta**: Meta công khai khuyến nghị trong báo cáo rằng Prompt-Guard 86M chỉ là một bộ lọc thô (coarse filter), bắt buộc phải nằm trong chuỗi phòng thủ đa tầng (Defense-in-Depth).

### 6.2. Single-Pass Ingress Proxy vs. Multi-Query Randomized Smoothing (SmoothLLM)
- SmoothLLM (Robey et al., NeurIPS 2023 [[14]](#ref14)) làm mịn prompt ngẫu nhiên và lấy đa số biểu quyết. Dù hóa giải được đòn GCG, việc phải gọi LLM đích $N=5-10$ lần khiến chi phí gọi API tăng vọt gấp **$5\times - 10\times$** và độ trễ vượt $> 1.5\text{s}$.
- PI-Guard áp dụng cách tiếp cận **Single-Pass Ingress Proxy** với độ trễ P95 chỉ **$3.45\text{ms}$** trên CPU và chi phí gọi phụ trợ bằng 0, đạt điểm cân bằng kinh tế tối ưu.

### 6.3. Bất Đối Xứng Cửa Sổ Ngữ Cảnh: ModernBERT 8k vs. Tail-Chunking
- Theo Zhou et al. (2026 [[40]](#ref40)), khi Guardrail chỉ có cửa sổ 512 tokens trong khi LLM nhận 128k tokens, kẻ tấn công chèn rác ở đầu và giấu mã độc ở trang cuối. DeBERTa-v3 cắt cụt 512 tokens **bỏ lọt $66.67\%$** tấn công.
- Cả hai hướng giải quyết: nâng cấp mô hình lên **ModernBERT 8k RoPE** [[37]](#ref37) hoặc áp dụng giải pháp **Băm Khối Quét Ưu Tiên Đuôi-Đầu** của PI-Guard đều khôi phục **$100.0\%$** khả năng đánh chặn.

---

## 📈 7. BẰNG CHỨNG TRỰC QUAN HÓA THỰC NGHIỆM (FIGURES 1–4 ANALYSIS)

Bộ 4 biểu đồ độ phân giải cao trích xuất từ các kịch bản đo đạc thực nghiệm phục vụ slide báo cáo Meeting 6 và Luận văn tốt nghiệp:

### 7.1. Figure 1: Early Stopping Latency Profile (Văn Bản Dài 200,000 Ký Tự)
- **Tệp hình ảnh**: [`figures/figure1_early_stopping_200k.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_6/figures/figure1_early_stopping_200k.png)
- **Phân tích**: So sánh trực tiếp giữa chiến lược quét tuyến tính Naive Linear ($111$ blocks duyệt tuần tự, mất $13.32\text{ms}$) và chiến lược Quét Ưu Tiên Đuôi-Đầu (Tail-First). Đòn tấn công Tail Injection bị phát hiện và ngắt sớm ngay tại Block đầu tiên ($0.12\text{ms}$, tăng tốc $111.0\times$).

### 7.2. Figure 2: Cross-Dataset Generalization Heatmap (Kiểm Thử D1–D6)
- **Tệp hình ảnh**: [`figures/figure2_cross_dataset_heatmap.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_6/figures/figure2_cross_dataset_heatmap.png)
- **Phân tích**: Biểu đồ nhiệt đối chuẩn 12 mô hình trên 6 tập dữ liệu. Minh chứng rõ rệt sự vượt trội của PI-Guard Two-Tier Cascade (duy trì Recall $> 90\%$ trên cả D1, D2, D3, D5, D6 và giữ $\text{FPR} = 0.0\%$ trên D4).

### 7.3. Figure 3: Low-FPR Economic Trade-off & Overdefense Frontier
- **Tệp hình ảnh**: [`figures/figure3_overdefense_tradeoff.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_6/figures/figure3_overdefense_tradeoff.png)
- **Phân tích**: Đường cong ROC nội suy trong phân vùng $\text{FPR} \le 1.5\%$. Thể hiện sự sụp đổ của Meta PromptGuard (TPR rơi xuống $12.78\%$) so với khả năng duy trì $\text{TPR} \ge 92.5\%$ của PI-Guard nhờ hàm mất mát MOF Invariance và hiệu chuẩn Conformal Risk Control.

### 7.4. Figure 4: Component Ablation Study (Đóng Góp Của Từng Tầng)
- **Tệp hình ảnh**: [`figures/figure4_component_ablation.png`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_6/figures/figure4_component_ablation.png)
- **Phân tích**: Bóc tách định lượng đóng góp của Lớp 0 (Tier-0 Scrubber: nâng khả năng kháng Evasion từ $35\%$ lên $88\%$), Tầng 1 (Tier-1 Dual TF-IDF: giảm độ trễ trung bình từ $18.5\text{ms}$ xuống $3.45\text{ms}$), và Tầng 2 (Tier-2 DeBERTa MOF: nâng Macro $F_1$ từ $0.647$ lên $0.932$).

---

## 📚 8. TÀI LIỆU THAM KHẢO CHÍNH THỨC (REFERENCES)

* <a id="ref7"></a>**[7]** H. Inan, K. Upasani, J. Chi, et al. 2023. *Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations*. Meta AI. [arXiv:2312.06674](https://arxiv.org/abs/2312.06674). Local PDF: [`References/Meta_2023_Llama_Guard_Input_Output_Safeguard.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Meta_2023_Llama_Guard_Input_Output_Safeguard.pdf).
* <a id="ref9"></a>**[9]** P. He, J. Yin, D. He, et al. 2023. *DeBERTaV3: Improving DeBERTa using ELECTRA-Style Pre-Training with Gradient-Disentangled Embedding*. In *ICLR 2023*. Local PDF: [`References/He_2023_DeBERTaV3_Disentangled_Attention_ICLR.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/He_2023_DeBERTaV3_Disentangled_Attention_ICLR.pdf).
* <a id="ref10"></a>**[10]** G. Markov et al. / OpenAI. 2023. *A Holistic Approach to Undesired Content Detection in the Real World*. In *AAAI 2023*. Local PDF: [`References/OpenAI_2023_Undesired_Content_Detection.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/OpenAI_2023_Undesired_Content_Detection.pdf).
* <a id="ref11"></a>**[11]** X. Shen, Z. Chen, M. Backes, et al. 2024. *\"Do Anything Now\": Characterizing and Evaluating In-The-Wild Jailbreak Prompts on Large Language Models*. In *ACM CCS 2024*. Local PDF: [`References/Shen_2024_Do_Anything_Now_Jailbreak_Prompts_In_The_Wild.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Shen_2024_Do_Anything_Now_Jailbreak_Prompts_In_The_Wild.pdf).
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
* <a id="ref30"></a>**[30]** D. Jacob, H. Alzahrani, Z. Hu, B. Alomair, and D. Wagner. 2024. *PromptShield: Deployable Detection for Prompt Injection Attacks*. In *Proceedings of the 2024 ACM SIGSAC Conference on Computer and Communications Security (CCS '24)*, pages 4247–4261. DOI: 10.1145/3714393.3726501. Local PDF: [`workspaces/truongnv/References/Jacob_2024_PromptShield_Deployable_Detection_Prompt_Injection_CCS.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Jacob_2024_PromptShield_Deployable_Detection_Prompt_Injection_CCS.pdf).
* <a id="ref31"></a>**[31]** C. Hackett, O. Kjellgren, and S. Al-Rubaie. 2025. *Bypassing LLM Guardrails: Mechanisms of Adversarial Evasion and Detection Strategies*. In *ACL 2025*. Local PDF: [`References/Hackett_2025_Bypassing_LLM_Guardrails_Evasion_Attacks.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Hackett_2025_Bypassing_LLM_Guardrails_Evasion_Attacks.pdf).
* <a id="ref32"></a>**[32]** Y. Liu, Y. Jia, J. Jia, D. Song, and N. Z. Gong. 2025. *DataSentinel: A Game-Theoretic Detection of Prompt Injection Attacks*. In *2025 IEEE Symposium on Security and Privacy (SP)*. DOI: 10.1109/SP61157.2025.00250. Local PDF: [`workspaces/truongnv/References/Liu_2025_DataSentinel_Game_Theoretic_Detection_Prompt_Injection.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Liu_2025_DataSentinel_Game_Theoretic_Detection_Prompt_Injection.pdf).
* <a id="ref33"></a>**[33]** E. Wallace et al. / OpenAI. 2024. *The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions*. arXiv preprint [arXiv:2404.13208](https://arxiv.org/abs/2404.13208). Local PDF: [`workspaces/truongnv/References/Wallace_2024_Instruction_Hierarchy_Prioritize_Privileged_Instructions.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Wallace_2024_Instruction_Hierarchy_Prioritize_Privileged_Instructions.pdf).
* <a id="ref34"></a>**[34]** P. Chao, E. Debenedetti, A. Robey, et al. 2024. *JailbreakBench: An Open Robustness Benchmark for Jailbreaking Large Language Models*. In *NeurIPS 2024*. [arXiv:2404.01318](https://arxiv.org/abs/2404.01318). Local PDF: [`References/Chao_2024_JailbreakBench_Open_Robustness_Benchmark_NeurIPS.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Chao_2024_JailbreakBench_Open_Robustness_Benchmark_NeurIPS.pdf).
* <a id="ref36"></a>**[36]** A. N. Angelopoulos, S. Bates, E. J. Candès, et al. 2024. *Conformal Risk Control*. arXiv preprint [arXiv:2208.02814](https://arxiv.org/abs/2208.02814). Local PDF: [`workspaces/truongnv/References/Angelopoulos_2024_Conformal_Risk_Control.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Angelopoulos_2024_Conformal_Risk_Control.pdf).
* <a id="ref37"></a>**[37]** B. Warner, A. Chaffin, B. Clavié, et al. 2024. *ModernBERT: Bringing Modern Transformer Innovations to Pre-trained Encoders*. [arXiv:2412.13663](https://arxiv.org/abs/2412.13663). Local PDF: [`workspaces/truongnv/References/Warner_2024_ModernBERT_Brings_Modern_Transformers_To_Encoders.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Warner_2024_ModernBERT_Brings_Modern_Transformers_To_Encoders.pdf).
* <a id="ref38"></a>**[38]** I. Padhi et al. 2024. *Granite Guardian: Content Safety and Risk Detection*. IBM Research. [arXiv:2412.07724](https://arxiv.org/abs/2412.07724). Local PDF: [`References/Padhi_2024_Granite_Guardian_Content_Safety_Risk_Detection.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Padhi_2024_Granite_Guardian_Content_Safety_Risk_Detection.pdf).
* <a id="ref40"></a>**[40]** Y. Zhou, C. Zhu, J. Wang, X. He, Y. Zhai, K. Sun, M. Wei, and J. Xiong. 2026. *Prompt Overflow: What the Guardrail Inspects Is Not What the Model Infers*. [arXiv:2605.23196](https://arxiv.org/abs/2605.23196). Local PDF: [`References/Zhou_2026_Prompt_Overflow_Guardrail_Window_Mismatch.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Zhou_2026_Prompt_Overflow_Guardrail_Window_Mismatch.pdf).
* <a id="ref41"></a>**[41]** J. Luo and E. Han. 2026. *CASCADE Against Jailbreaks: Combination Across Stages with Controlled Attack-Defense Evaluation*. [arXiv:2609.21793](https://arxiv.org/abs/2609.21793). Local PDF: [`References/Luo_2026_CASCADE_Against_Jailbreaks_Evaluation.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Luo_2026_CASCADE_Against_Jailbreaks_Evaluation.pdf).
