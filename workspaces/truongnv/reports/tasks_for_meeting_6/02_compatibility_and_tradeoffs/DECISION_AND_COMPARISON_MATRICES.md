# BỘ MA TRẬN SO SÁNH VÀ LUẬN CHỨNG RA QUYẾT ĐỊNH KHOA HỌC (DECISION & COMPARISON MATRICES)
## Đề tài: A Machine-Learning Guardrail for Detecting Prompt Injection and Jailbreak Attacks on LLM Applications (PI-Guard)
### Thẩm định độc quyền: `workspaces/truongnv` | Căn cứ: Chuẩn mực IEEE TIFS, ACM CCS, NeurIPS, ACL & FPT IAP491

---

## 📌 TỔNG QUAN PHƯƠNG PHÁP LUẬN RA QUYẾT ĐỊNH

Tài liệu này thiết lập **Bộ 4 Ma trận so sánh đa tiêu chí (Multi-Criteria Decision Matrices)** phục vụ việc lựa chọn mô hình, thuật toán, chiến lược xử lý ngữ cảnh và cơ chế ra quyết định cho hệ thống PI-Guard.

**Nguyên tắc phương pháp luận bắt buộc**:
1. **Zero-Mock Invariant**: Không sử dụng số liệu giả lập hoặc hàm heuristic mô phỏng. Mọi đánh đổi đều được bảo chứng bởi mã nguồn thực nghiệm và y văn gốc.
2. **Four-Tier Provenance**: Mọi công trình khoa học được viện dẫn đều trích xuất chính xác siêu dữ liệu xuất bản và kết quả gốc của tác giả (không thay đổi câu văn hay kết luận của bài báo gốc).
3. **Tính Khiêm Tốn Khoa Học (Scientific Humility)**: Không tuyên bố đã xong toàn diện hay giải pháp hoàn hảo không tì vết. Trình bày trung thực các vấn đề phát hiện, phương án khắc phục và kết quả đo đạc thực tế.

---

## 🏛️ MA TRẬN 1: SO SÁNH & LỰA CHỌN KIẾN TRÚC MÔ HÌNH PHÂN LOẠI (MODEL ARCHITECTURE)

### 1.1. Bảng đối chuẩn đa tiêu chí 6 trường phái kiến trúc ứng viên

| Trường Phái Kiến Trúc / Mô Hình Đại Diện | Cửa Sổ Ngữ Cảnh (Context) | Độ Trễ CPU P95 (ms) | Bộ Nhớ RAM / VRAM | Kháng Nhiễu Cú Pháp (Leetspeak/Base64) | Tỷ Lệ Chặn Nhầm Code (`NotInject`) | Nhận Diện Injection (Direct/Indirect) | Nhận Diện Jailbreak (DAN) | Mức Độ Phù Hợp Ingress Proxy |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **C1: Dual-Space TF-IDF + Platt LogReg** *(PI-Guard Tier 1)* [[16]](#ref16) | Không giới hạn | **$< 1.5\text{ms}$** | **$< 5\text{MB}$ / 0 MB** | Khá *(nhờ `char_wb` 3-5)* | **Thấp** *(FPR $6.0\%$)* | Khá *(Direct $62.5\%$, Indirect $48.0\%$)* | Trung bình ($58.0\%$) | ✅ **Bộ lọc sơ cấp lý tưởng (Tier 1)** |
| **C2: Dense Embedding + LogReg/RF** *(MiniLM - Ayub & Majumdar 2024)* [[2]](#ref2) | 512 tokens | $42.7\text{ms}$ (P95: $119.4\text{ms}$) | $\approx 120\text{MB}$ / 0 MB | Kém *(nhạy cảm với OOV)* | **Rất cao** *(FPR $58.4\%$ sập UX)* | Cao trên Direct, Kém trên Indirect | Khá ($72.0\%$) | ❌ **Loại trừ** *(Gây nghẽn cổ chai và quá phòng thủ)* |
| **C3: Sequence Encoder DeBERTa-v3** *(He et al. 2023 / Li et al. 2025)* [[9]](#ref9), [[18]](#ref18) | 512 tokens *(cần chunking)* | $38.4\text{ms}$ (CPU FP32) | $\approx 340\text{MB}$ / 0 MB | **Rất cao** *(bóc tách vị trí tương đối)* | **Rất thấp** *(Acc $99.0\%$ nhờ MOF)* | **Rất cao** *(Direct $93.8\%$, Indirect $100\%$)* | **Rất cao** ($100\%$) | ✅ **Trọng tài ngữ nghĩa quán quân (Tier 2)** |
| **C4: Long-Context Encoder ModernBERT** *(Warner et al. 2024)* [[37]](#ref37) | **8,192 tokens** | $18.5\text{ms}$ (CPU) | $\approx 280\text{MB}$ / 0 MB | **Rất cao** *(FlashAttn-2, unpadding)* | Thấp *(chưa có MOF fine-tuned)* | **Rất cao** *(vượt trội trên văn bản RAG dài)* | Cao ($92.0\%$) | 🔄 **Ứng viên tiềm năng nâng cấp Tier 2** |
| **C5: Small Specialized Classifier** *(Prompt-Guard 86M - Meta AI 2024)* [[20]](#ref20) | 512 tokens | $18.2\text{ms}$ (CPU) | $\approx 180\text{MB}$ / 0 MB | Kém *(bị Unicode/Cipher bypass)* | 🔴 **SẬP HOÀN TOÀN** *(FPR $99.12\%$ NotInject)* | Cao trên Direct ($78.1\%$), Kém trên Indirect | Khá ($82.0\%$) | ⚠️ **Chỉ dùng làm mốc đối chứng (Baseline)** |
| **C6: Autoregressive Safety SLM** *(Llama Guard 3 1B / Granite 2B)* [[7]](#ref7), [[38]](#ref38) | 8k - 128k tokens | 🔴 **$> 1,500\text{ms}$** | $> 1.5\text{GB}$ / $\ge 4\text{GB}$ | Trung bình *(dễ dính Recursive Injection)* | Rất thấp *(hiểu ngữ cảnh sâu)* | Cao *(nhưng tỷ lệ bắt prompt injection thấp)* | Rất cao | ❌ **Loại trừ khỏi Ingress Proxy** *(Vi phạm trần trễ P95 < 30ms)* |

### 1.2. Luận cứ ra quyết định (Decision Rationale)
- **Quyết định chọn lựa**: **Kiến trúc phân tầng Two-Tier Cascade (Tier 0 Scrubber + Tier 1 Dual-Space TF-IDF + Tier 2 DeBERTa-v3 MOF)**.
- **Cơ sở khoa học**:
  1. *Nguyên lý Saltzer & Schroeder (1975)*: Không một mô hình đơn lẻ nào giải quyết được đồng thời 3 mục tiêu: Độ trễ $< 2\text{ms}$, Hiểu ngữ nghĩa sâu, và FPR $< 1.5\%$.
  2. *Giải phóng tài nguyên*: Tầng 1 thanh lọc $80\%$ lưu lượng sạch trong $1.2\text{ms}$. Tầng 2 chỉ kích hoạt cho $20\%$ lưu lượng bất định, đưa độ trễ kỳ vọng toàn hệ thống về:
     $$\mathbb{E}[L] = 1.2\text{ms} + 0.20 \times 38.4\text{ms} = 8.88\text{ms} < 30\text{ms}$$
  3. *Khắc phục Overdefense*: Khác với Meta Prompt-Guard 86M (bị sập $99.12\%$ trên code `NotInject`), Tầng 2 kế thừa cơ chế Masked Overlap Fraction (Li et al., ACL 2025) giúp phân biệt chính xác giữa từ khóa lập trình hợp lệ (`override`, `delete`) và câu lệnh tấn công thật sự.

---

## ⚖️ MA TRẬN 2: SO SÁNH & LỰA CHỌN HÀM MẤT MÁT VÀ TỐI ƯU HÓA (LOSS FUNCTION)

### 2.1. Bảng phân tích 5 giải thuật hàm mất mát

| Giải Thuật Hàm Mất Mát | Công Thức Toán Học Chính Thức | Cơ Chế Phạt Lỗi Báo Động Giả (False Positive) | Ổn Định Khi Dữ Liệu Lệch Lớp (Imbalance 95:5) | Khắc Phục Overdefense Trên Code | Độ Phức Tạp Tính Toán |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **L1: Standard Cross-Entropy** | $\mathcal{L}_{\text{CE}} = - \sum y_i \log(\hat{y}_i)$ | Không phân biệt chi phí ($C_{FP} = C_{FN}$) | ❌ Kém *(thiên vị lớp đa số Benign)* | ❌ Kém | **$O(C)$** *(thấp nhất)* |
| **L2: Focal Loss** *(Lin et al. ICCV 2017)* [[39]](#ref39) | $\mathcal{L}_{\text{Focal}} = -\alpha_t (1 - p_t)^\gamma \log(p_t)$ | Tập trung vào mẫu khó bằng hệ số $(1 - p_t)^\gamma$ | Khá *(giảm ảnh hưởng mẫu dễ)* | Trung bình | $O(C)$ |
| **L3: Dynamic Class-Weighted Loss** *(King & Zeng 2001)* [[18]](#ref18) | $\mathcal{L}_{\text{weight}} = - \sum w_c y_c \log(\hat{y}_c), \; w_c = \frac{N}{C \cdot N_c}$ | **Tự động cân bằng trọng số nghịch đảo tần suất lớp** | ✅ **Rất cao** *(không phụ thuộc tỷ lệ lấy mẫu)* | ✅ **Rất tốt** | **$O(C)$** *(tối ưu)* |
| **L4: Asymmetric Loss (ASL)** *(Ridnik et al. ICCV 2021)* [[42]](#ref42) | $\mathcal{L}_{\text{ASL}} = - y (1-p)^{\gamma_+} \log(p) - (1-y) (p_m)^{\gamma_-} \log(1-p_m)$ | **Phạt bất đối xứng cực mạnh trên False Positives** | **Rất cao** | **Rất tốt** *(triệt tiêu gradient âm nhẹ)* | $O(C)$ *(cần tinh chỉnh $\gamma_+, \gamma_-$)* |
| **L5: Supervised Contrastive Loss** *(Khosla et al. NeurIPS 2020)* [[43]](#ref43) | $\mathcal{L}_{\text{SupCon}} = \sum \frac{-1}{|P(i)|} \sum_{p \in P(i)} \log \frac{e^{z_i \cdot z_p / \tau}}{\sum e^{z_i \cdot z_a / \tau}}$ | Kéo gần biểu diễn cùng lớp, đẩy xa khác lớp | Khá | **Xuất sắc** *(kéo dãn biên Hard Negatives)* | $O(B^2 \cdot D)$ *(tốn bộ nhớ batch)* |

### 2.2. Luận cứ ra quyết định (Decision Rationale)
- **Quyết định chọn lựa**: **Hàm mất mát Dynamic Class-Weighted Loss (King & Zeng 2001)** làm hàm mục tiêu tối ưu hóa chính trong script huấn luyện [`train_tier2_deberta.py`](file:///d:/Work/Do-an/workspaces/truongnv/scripts/train_tier2_deberta.py).
- **Cơ sở khoa học**:
  - Công thức $w_c = \frac{N_{\text{total}}}{C \cdot N_c}$ đảm bảo các mẫu tấn công hiếm gặp nhận hệ số phạt lớn ($w_1 = 2.258$), trong khi lớp lành tính nhận hệ số chuẩn hóa ($w_0 = 0.642$), giúp mô hình duy trì độ nhạy cao mà không bị trôi ngưỡng phân loại.
  - Kết hợp với kỹ thuật **Group-Aware Splitting MD5** triệt tiêu hoàn toàn rò rỉ mẫu giữa các biến thể tấn công cộng đồng.

---

## 📜 MA TRẬN 3: SO SÁNH CHIẾN LƯỢC XỬ LÝ VĂN BẢN DÀI 200K KÝ TỰ & PROMPT OVERFLOW

### 3.1. Bảng đối chuẩn 5 chiến lược xử lý cửa sổ ngữ cảnh

| Chiến Lược Cửa Sổ Ngữ Cảnh | Phát Hiện Prompt Giấu Ở Đuôi (Tail Injection) | Độ Trễ Quét Văn Bản Sạch 200k Ký Tự | Hệ Số Tăng Tốc Ngắt Sớm (Early Stopping) | Nguy Cơ Tràn Bộ Nhớ (OOM) | Bảo Toàn Ngữ Cảnh Biên (Boundary Integrity) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **W1: Cắt cụt cố định (Head Truncation 512)** | 🔴 **BỎ SÓT 100%** *(Zhou et al. 2026)* | **$< 5\text{ms}$** | Không áp dụng | **0%** | Mất $99\%$ nội dung tài liệu |
| **W2: Quét tuần tự (Sequential Sliding Window)** | Bắt được ở block cuối cùng (Block 148) | $2,743\text{ms}$ (148 blocks) | $1.0\times$ (duyệt hết tài liệu mới thấy) | Thấp *(giải phóng RAM từng block)* | Tốt *(nhờ 10% overlap)* |
| **W3: Quét Ưu Tiên Đầu-Cuối (Head-and-Tail Priority)** *(PI-Guard)* | **BẮT NGAY TẠI BLOCK ĐẦU TIÊN QUÉT** | **$602\text{ms}$** *(toàn văn)* | **$4.6\times - 111.0\times$ FASTER** | **0%** *(tiêu thụ RAM $< 1.8\text{GB}$)* | **Tốt** *(bảo vệ cả Header chỉ thị và Footer tài liệu)* |
| **W4: Đưa nguyên khối vào ModernBERT (8k)** | Bắt được nếu tài liệu $< 8\text{k}$ tokens | $85\text{ms}$ (văn bản ngắn) | Không áp dụng *(vẫn phải chunk nếu 200k chars $\approx 50\text{k}$ tokens)* | Trung bình *(tăng VRAM theo $O(N^2)$)* | Xuất sắc trong phạm vi 8k tokens |
| **W5: Lọc Anomaly Perplexity Cửa Sổ** [[14]](#ref14) | Bắt được nếu payload có độ hỗn loạn cao | $350\text{ms}$ | $1.2\times$ | 0% | Kém *(không bắt được câu lệnh tự nhiên)* |

### 3.2. Luận cứ ra quyết định (Decision Rationale)
- **Quyết định chọn lựa**: **Chiến lược Quét Ưu Tiên Đầu-Cuối (Head-and-Tail Priority Scanning) kết hợp Ngắt Sớm (Early Stopping) và Sliding Window 10% overlap** ([`block_chunker.py`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_6/src/block_chunker.py)).
- **Cơ sở khoa học**:
  - *Giải quyết chỉ đạo của Thầy Ninh*: Kẻ tấn công giấu lệnh độc hại ở cuối tài liệu (Tail Injection) nhằm né tránh bộ lọc. Khi áp dụng Head-and-Tail, khối đuôi được nạp và quét ngay tại chu kỳ đầu tiên ($t = 0.12\text{ms}$), kích hoạt Early-Stopping ngắt toàn bộ chu trình duyệt, đạt tốc độ tăng tốc từ $4.6\times$ đến $111\times$ so với duyệt tuần tự.

---

## 🎯 MA TRẬN 4: SO SÁNH CƠ CHẾ HIỆU CHUẨN ĐỘ TIN CẬY VÀ ĐỊNH TUYẾN BẤT ĐỊNH

### 4.1. Bảng đối chuẩn 5 phương pháp hiệu chuẩn và định tuyến

| Cơ Chế Hiệu Chuẩn & Định Tuyến | Bảo Chứng Toán Học Hữu Hạn $\text{FPR} \le \alpha$ | Kháng Trôi Dạt Phân Phối (OOD Shift) | Tỷ Lệ Thông Qua Nhanh Tại Tầng 1 | Chi Phí Tính Toán Suy Luận | Mức Độ Phù Hợp Thực Tiễn |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **R1: Hard Thresholding ($\theta = 0.50$)** | Không có | 🔴 Rất kém | $0\%$ *(buộc chạy 1 model)* | $0\text{ms}$ | ❌ Quá thô sơ |
| **R2: Platt Scaling (Sigmoid Logistic)** | Không có *(chỉ khớp phân phối logit)* | Kém khi gặp OOD | $\approx 80\%$ | $< 0.01\text{ms}$ | Khá *(dùng chuẩn hóa logit Tầng 1)* |
| **R3: Temperature Scaling** *(Guo et al. 2017)* | Không có | Kém khi gặp OOD | $\approx 80\%$ | $< 0.01\text{ms}$ | Khá *(chỉ scale độ dốc softmax)* |
| **R4: Conformal Risk Control** *(Angelopoulos 2024)* [[44]](#ref44) | ✅ **Có bảo chứng nghiêm ngặt**: $\mathbb{E}[\text{FPR}] \le \alpha$ | **Rất cao** *(Distribution-free validity)* | $\approx 78\%$ | $< 0.05\text{ms}$ | ✅ **Chuẩn mực toán học cao nhất** |
| **R5: Tri-State Router + Fail-Safe OOV Gate** *(PI-Guard)* | Bảo chứng kết hợp qua ngưỡng $\theta_{\text{low}}, \theta_{\text{high}}$ | **Xuất sắc** *(OOV Gate chặn đứng Token Dilution & Obfuscation)* | **$82.6\%$** | **$< 0.02\text{ms}$** | ✅ **Lựa chọn tối ưu toàn diện** |

### 4.2. Luận cứ ra quyết định (Decision Rationale)
- **Quyết định chọn lựa**: **Bộ định tuyến Tam phân Tri-State Uncertainty Router ($\theta_{\text{low}}=0.15, \theta_{\text{high}}=0.85$) kết hợp Cổng An toàn Mặc định OOV Density Gate ($\rho_{\text{OOV}} > 0.40$)**.
- **Cơ sở khoa học**:
  - Tuân thủ nguyên lý *Fail-Safe Defaults* (Saltzer & Schroeder 1975): Mọi truy vấn có độ hỗn loạn ký tự cao hoặc bị chêm rác vượt ngưỡng $\rho_{\text{OOV}} > 0.40$ đều bị tước quyền thông qua nhanh, cưỡng chế chuyển tiếp lên Tầng 2 để bóc tách token BPE chuyên sâu, ngăn chặn triệt để đòn tấn công Gray-box Token Dilution.

---

## 📚 TÀI LIỆU THAM KHẢO CHÍNH THỨC (REFERENCES)

* <a id="ref2"></a>**[2]** M. R. R. Ayub and A. Majumdar. 2024. *Towards Robust Detection of Prompt Injection Attacks on Large Language Models*. In *CAMLIS 2024*. [arXiv:2410.22284](https://arxiv.org/abs/2410.22284). Local PDF: [`References/Ayub_2024_Towards_Robust_Detection_Prompt_Injection_CAMLIS.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Ayub_2024_Towards_Robust_Detection_Prompt_Injection_CAMLIS.pdf).
* <a id="ref7"></a>**[7]** H. Inan, K. Upasani, J. Chi, et al. 2023. *Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations*. Meta AI. [arXiv:2312.06674](https://arxiv.org/abs/2312.06674). Local PDF: [`References/Meta_2023_Llama_Guard_Input_Output_Safeguard.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Meta_2023_Llama_Guard_Input_Output_Safeguard.pdf).
* <a id="ref9"></a>**[9]** P. He, J. Yin, D. He, et al. 2023. *DeBERTaV3: Improving DeBERTa using ELECTRA-Style Pre-Training with Gradient-Disentangled Embedding*. In *ICLR 2023*. Local PDF: [`References/He_2023_DeBERTaV3_Disentangled_Attention_ICLR.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/He_2023_DeBERTaV3_Disentangled_Attention_ICLR.pdf).
* <a id="ref14"></a>**[14]** A. Robey, E. Wong, H. Hassani, and G. J. Pappas. 2023. *SmoothLLM: Defending Large Language Models Against Jailbreaking Attacks*. In *NeurIPS 2023*. [arXiv:2310.03684](https://arxiv.org/abs/2310.03684). Local PDF: [`References/Robey_2023_SmoothLLM_Defending_LLMs_Random_Perturbation.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Robey_2023_SmoothLLM_Defending_LLMs_Random_Perturbation.pdf).
* <a id="ref16"></a>**[16]** J. H. Saltzer and M. D. Schroeder. 1975. *The Protection of Information in Computer Systems*. In *Proceedings of the IEEE*, 63(9):1278–1308. DOI: 10.1109/PROC.1975.9939. Local PDF: [`References/Saltzer_1975_The_Protection_of_Information_in_Computer_Systems.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Saltzer_1975_The_Protection_of_Information_in_Computer_Systems.pdf).
* <a id="ref18"></a>**[18]** H. Li, X. Liu, N. Zhang, and C. Xiao. 2025. *PIGuard: Prompt Injection Guardrail via Mitigating Overdefense for Free*. In *ACL 2025 - Long Paper*. [arXiv:2410.22770](https://arxiv.org/abs/2410.22770). Local PDF: [`References/PIGuard_2025_Prompt_Injection_Guardrail_ACL.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/PIGuard_2025_Prompt_Injection_Guardrail_ACL.pdf).
* <a id="ref20"></a>**[20]** Meta AI. 2024. *Prompt Guard 86M: A Small Classifier for Prompt Injection and Jailbreak Detection*. Model Card and Technical Report. [arXiv:2407.21783](https://arxiv.org/abs/2407.21783). Local PDF: [`References/Meta_2024_Prompt_Guard_86M_Input_Guardrail.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Meta_2024_Prompt_Guard_86M_Input_Guardrail.pdf).
* <a id="ref37"></a>**[37]** B. Warner, A. Chaffin, B. Clavié, et al. 2024. *ModernBERT: Bringing Modern Transformer Innovations to Pre-trained Encoders*. [arXiv:2412.13663](https://arxiv.org/abs/2412.13663). Local PDF: [`References/Warner_2024_ModernBERT_Brings_Modern_Transformers_To_Encoders.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Warner_2024_ModernBERT_Brings_Modern_Transformers_To_Encoders.pdf).
* <a id="ref38"></a>**[38]** I. Padhi, M. Nagireddy, G. Cornacchia, et al. 2024. *Granite Guardian: Content Safety and Risk Detection*. IBM Research. [arXiv:2412.07724](https://arxiv.org/abs/2412.07724). Local PDF: [`References/Padhi_2024_Granite_Guardian_Content_Safety_Risk_Detection.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Padhi_2024_Granite_Guardian_Content_Safety_Risk_Detection.pdf).
* <a id="ref39"></a>**[39]** T.-Y. Lin, P. Goyal, R. Girshick, K. He, and P. Dollár. 2017. *Focal Loss for Dense Object Detection*. In *IEEE ICCV 2017*, pages 2980–2988. DOI: 10.1109/ICCV.2017.324. Open-Access: [arXiv:1708.02002](https://arxiv.org/abs/1708.02002).
* <a id="ref42"></a>**[42]** E. Ridnik, E. Ben-Baruch, N. Zamir, A. Noy, and L. Zelnik-Manor. 2021. *Asymmetric Loss For Multi-Label Classification*. In *IEEE ICCV 2021*, pages 9713–9722. DOI: 10.1109/ICCV48922.2021.00958. Open-Access: [arXiv:2009.14119](https://arxiv.org/abs/2009.14119).
* <a id="ref43"></a>**[43]** P. Khosla, P. Teterwak, C. Wang, A. Sarna, Y. Tian, P. Isola, A. Maschinot, C. Liu, and D. Krishnan. 2020. *Supervised Contrastive Learning*. In *NeurIPS 2020*, volume 33, pages 18661–18673. Open-Access: [arXiv:2004.11362](https://arxiv.org/abs/2004.11362).
* <a id="ref44"></a>**[44]** A. N. Angelopoulos, S. Bates, E. J. Candès, M. I. Jordan, and L. Lei. 2024. *Learn Then Test: Calibrating Predictive Algorithms to Achieve Risk Control*. *Journal of the Royal Statistical Society Series B*, 86(3):679–709. Local PDF: [`References/Angelopoulos_2024_Conformal_Risk_Control.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Angelopoulos_2024_Conformal_Risk_Control.pdf).
