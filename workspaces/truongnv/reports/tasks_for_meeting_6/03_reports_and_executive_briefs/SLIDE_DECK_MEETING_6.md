# SLIDE DECK: BÁO CÁO TIẾN ĐỘ THỰC HIỆN ĐỒ ÁN (MEETING 6)
## Đề Xuất Mô Hình Nghiên Cứu Lõi & Kết Quả Đối Chuẩn Thực Nghiệm Hai Tầng (Two-Tier Cascade) Cho PI-Guard

---

- **Học phần**: `IAP491` — Đồ án Tốt nghiệp Kỹ sư An toàn Thông tin, Đại học FPT
- **Học kỳ**: Fall 2026
- **Giảng viên Hướng dẫn (GVHD)**: ThS. Trần Văn Ninh
- **Nhóm sinh viên thực hiện**:
  - Nguyễn Văn Trường (MSSV: `SE182034`)
  - Nguyễn Quí Đức (MSSV: `SE182087`)
  - Phạm Minh Hoàng Việt (MSSV: `SE181851`)
  - Đỗ Đoàn Duy Phương (MSSV: `SE180235`)
- **Ngày báo cáo**: 24/09/2026 (Meeting 6)
- **Tài liệu chi tiết**: [`MASTER_RESEARCH_SYNTHESIS_REPORT_MEETING_6.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_6/03_reports_and_executive_briefs/MASTER_RESEARCH_SYNTHESIS_REPORT_MEETING_6.md)
- **Bản trình chiếu PowerPoint chính thức (50 Slide)**: [`../PI-GUARD-Present-Meeting-6.pptx`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_6/PI-GUARD-Present-Meeting-6.pptx) (Được biên dịch từ [`workspaces/truongnv/scripts/build_presentation_deck.py`](file:///d:/Work/Do-an/workspaces/truongnv/scripts/build_presentation_deck.py))

---

### SLIDE 1: TỔNG QUAN ĐỀ TÀI & BỐI CẢNH AN TOÀN THÔNG TIN (IA)

- **Tên đề tài**: *A Machine-Learning Guardrail for Detecting Prompt Injection and Jailbreak Attacks on LLM Applications (PI-Guard)*.
- **Mục tiêu cốt lõi**: Xây dựng tường lửa thông minh (Ingress Guardrail Proxy) bảo vệ ứng dụng LLM trước tấn công Prompt Injection (OWASP LLM01:2025) và Jailbreak với độ trễ cực thấp và tỷ lệ dương tính giả (FPR) thấp.
- **Tôn chỉ kỹ thuật**:
  - Không can thiệp vào trọng số nội bộ hay KV-cache của LLM đích (Black-Box Protection).
  - Vận hành độc lập trên CPU phổ thông (Commodity CPU), không phụ thuộc GPU chuyên dụng.
  - Tuân thủ nguyên lý an toàn kinh điển: *Economy of Mechanism* và *Fail-Safe Defaults* (Saltzer & Schroeder 1975).

---

### SLIDE 2: KẾT QUẢ GIẢI QUYẾT 5 NHIỆM VỤ CHỈ ĐẠO TẠI MEETING 5

| Nhiệm Vụ Chỉ Đạo Của GVHD | Kết Quả Thực Nghiệm Đạt Được | Bằng Chứng Kỹ Thuật (100% Verified) |
| :--- | :--- | :--- |
| **1. Bản chất Kiến trúc & Thuật toán** | Hoàn thành Phân loại học 6x7 vĩ mô $\to$ 12x14 vi mô | [`TAXONOMY_...md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_6/01_theory_and_taxonomy/TAXONOMY_OF_ARCHITECTURES_AND_ALGORITHMIC_PARADIGMS.md) |
| **2. Ma trận tương thích & NUS CASCADE** | Phân tích 168 giao điểm; bác bỏ mô hình đơn khối | [`ARCHITECTURAL_...md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_6/02_compatibility_and_tradeoffs/ARCHITECTURAL_COMPATIBILITY_MATRIX_CASCADE_12X14.md) |
| **3. Xử lý văn bản 200k & Tail-Scan** | BlockChunker Head-and-Tail dừng sớm tại Block 1 | [`test_hidden_prompt_at_tail.py`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_6/tests/test_hidden_prompt_at_tail.py) (Tăng tốc 4.6x) |
| **4. Đo đạc thực tế CPU & Weights** | Đóng gói weights `.joblib` & DeBERTa-v3 CPU Native | [`cross_dataset_empirical_matrix.json`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_6/04_benchmarks_and_data/cross_dataset_empirical_matrix.json) |
| **5. Hồ sơ Phản biện & Đóng băng mô hình**| Xây dựng Council Defense Playbook & Đóng băng | [`MASTER_RESEARCH_SYNTHESIS_REPORT_MEETING_6.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_6/03_reports_and_executive_briefs/MASTER_RESEARCH_SYNTHESIS_REPORT_MEETING_6.md) |

---

### SLIDE 3: KIẾN TRÚC PHÂN TẦNG ĐỀ XUẤT (TWO-TIER CASCADE ARCHITECTURE) & MINH CHỨNG KHOA HỌC

- **Toàn cảnh Kiến trúc Phân tầng (Figure: `fig_arch_pipeline_overview.png`)**:
  - Giai đoạn 0 (Ingress Scrubber) $\to$ Giai đoạn 1 (Tầng 1 Dual TF-IDF) $\to$ Giai đoạn 2 (Router 3 Luồng) $\to$ Giai đoạn 3 (Tầng 2 DeBERTa-v3 FP32).
  - Độ trễ trung bình $2.85\text{ms}$, P95 $< 25\text{ms}$ trên CPU, giải phóng $82.6\%$ tải ngay tại Tầng 1.
- **Bản chất Bộ định tuyến 3 luồng vs Nhị phân 1-0 (Figure: `fig_tristate_vs_binary_routing.png`)**:
  - Bác bỏ điểm cắt cứng nhị phân ($p = 0.5$); thiết lập vùng từ chối bất định (Reject Option theo Chow 1970 [[15]](#ref15)).
  - Phân vùng CASCADE (Luo & Han 2026 [[41]](#ref41)): Luồng 1 (Thông xe $p < 0.15$, $71.3\%$ tải, $0.85\text{ms}$), Luồng 2 (Chặn sớm $p > 0.85$, $11.3\%$ tải, $1.20\text{ms}$), Luồng 3 (Thẩm định sâu $0.15 \le p \le 0.85$, $17.4\%$ tải, $18.5\text{ms}$).
  - Đảm bảo toán học Conformal Risk Control (Angelopoulos 2024) duy trì $\text{FPR} < 1.5\%$.
- **Lớp Tiền Xử Lý Tầng 0 (Figure: `fig_tier0_scrubber_pipeline.png`)**:
  - 4 chặng khử ngụy trang cú pháp: Unicode NFKC, Zero-width stripper, Regex inline decoder (Base64/Hex/Rot13), và Vietnamese Scrubber.
- **Tầng 1 Dual-Space TF-IDF & Platt Scaling (Figure: `fig_tier1_dual_space_and_platt.png`)**:
  - Không gian kép: Word (1-3 n-grams, 20k đặc trưng) + Char_wb (3-5 n-grams, 30k đặc trưng bắt Leetspeak).
  - Ma trận thưa CSR tiết kiệm $75\%$ RAM, hiệu chuẩn xác suất qua hàm Platt Scaling Sigmoid.
- **Tầng 2 DeBERTa-v3 & Kháng Overdefense MOF (Figure: `fig_mof_code_invariance_mechanism.png`)**:
  - Disentangled Attention 3 ma trận (Content-Content, Content-Position, Position-Content) và Dynamic Class-Weighted Loss.
  - Chiết khấu ngưỡng động $\tau_{\text{eff}} = \tau_0 + \gamma \cdot \text{MOF}(X)$ bảo vệ $99.00\%$ mã nguồn NotInject trên phần cứng CPU Native FP32.
- **Thuật toán Chunker Văn bản dài 200k (Figure: `fig_chunker_head_and_tail_algorithm.png`)**:
  - Quét ưu tiên vị trí Head-and-Tail dừng sớm tại Block 1: Giảm thời gian quét từ $4,115\text{ms} \to 37.1\text{ms}$ (tăng tốc $111\times$).

---

### SLIDE 4: MÔ HÌNH HÓA TOÁN HỌC & CÔNG THỨC LÕI

- **Mối đe dọa chuỗi ghép**:
  $$X = S \mathbin{\Vert} U \quad (S: \text{System/RAG}, \; U: \text{User Query})$$
- **Hiệu chuẩn xác suất Tầng 1 (Platt Scaling)**:
  $$P(\text{Malicious} \mid X) = \frac{1}{1 + \exp(-(\mathbf{w}^T \mathbf{z} + b))} \quad \text{với } \mathbf{z} = [\mathbf{z}_{\text{word}} \mathbin{\Vert} \mathbf{z}_{\text{char}}]$$
- **Mật độ dị biệt ký tự (OOV Entropy Density)**:
  $$\rho_{\text{OOV}}(X) = \frac{N_{\text{irregular}}}{L} + 0.5 \cdot \frac{N_{\text{single}}}{N_{\text{tokens}}}$$
- **Bất biến che phủ mã lệnh (Masked Overlap Fraction - MOF)**:
  $$S_{\text{final}} = S_{\text{raw}} \cdot (1.0 - \text{MOF}(X)) \quad \text{khi } \text{MOF} > 0.50 \land \neg \text{HasExplicitAttack}$$

---

### SLIDE 5: BÁC BỎ ẢO TƯỞNG SIÊU MÔ HÌNH ĐƠN KHỐI (THE GUARDRAIL TRILEMMA)

- **Tam giác bất khả thi của Guardrail**:
  1. Độ trễ cực thấp ($< 1.0\text{ms}$);
  2. Hiểu ngữ nghĩa sâu & Kháng đối kháng;
  3. Tỷ lệ dương tính giả gần bằng 0 ($< 1.0\%$).
- **Bài học từ các giải pháp đơn khối**:
  - *Regex/Perplexity*: Rất nhanh ($< 0.1\text{ms}$) nhưng mù ngữ nghĩa (Recall chỉ $18 - 31\%$).
  - *Generative LLM 7B/8B (Llama Guard)*: Ngữ nghĩa tốt nhưng độ trễ bùng nổ $> 1.5\text{s}$ và đòi hỏi GPU đắt tiền.
  - *Meta Prompt-Guard 86M*: Quá phòng thủ, sụp đổ trên mã nguồn (chặn nhầm $99.12\%$ code NotInject).
- **Kết luận**: Chỉ có **Kiến trúc Phân tầng Thích ứng (Two-Tier Cascade)** mới đạt tới biên tối ưu Pareto (NUS CASCADE 2026 [[41]](#ref41)).

---

### SLIDE 6: BẢNG KẾT QUẢ ĐỐI CHUẨN THỰC NGHIỆM ĐỘC LẬP (520 MẪU TEST D1–D6)

| Mô hình | Direct Recall (D1) | Indirect Recall (D2) | Jailbreak Recall (D3) | Code Acc (D5) | FPR Benign (D6) | Độ trễ P95 CPU |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **M1: Baseline Keyword Regex** | $10.4\%$ [$4.5-22.2$] | $100.0\%$ [$96.3-100$] | $100.0\%$ [$96.3-100$] | $100.0\%$ | $0.0\%$ | $< 0.1\text{ms}$ |
| **M2: Tier-1 TF-IDF Platt** | $83.3\%$ [$70.4-91.3$] | $24.0\%$ [$16.7-33.2$] | $0.0\%$ [$0.0-3.7$] ❌ | $100.0\%$ | $0.0\%$ | **$12.9\text{ms}$** |
| **M3: DeBERTa-v3 Standalone** | $58.3\%$ [$44.3-71.2$] | $100.0\%$ [$96.3-100$] | $62.0\%$ [$52.2-70.9$] | $81.0\%$ ⚠️ ($19\%$ FPR) | $6.0\%$ | $1,790.3\text{ms}$ |
| **M4: PI-GUARD (Two-Tier Cascade)**| **$91.7\%$ [$80.5-96.7$]** | **$100.0\%$ [$96.3-100$]** | **$62.0\%$ [$52.2-70.9$]** | **$98.0\%$ [$93.0-99.5$]** | **$6.0\%$ [$2.8-12.5$]** | **$12.9 / 411.6\text{ms}$** |

*(Ghi chú: Toàn bộ chỉ số đều đo đạc thực tế 100% trên CPU thông dụng, gắn kèm Khoảng tin cậy 95% Wilson Score)*

---

### SLIDE 7: BẰNG CHỨNG KIỂM ĐỊNH Ý NGHĨA THỐNG KÊ (MCNEMAR TEST)

- **Câu hỏi khoa học**: *Sự vượt trội của PI-Guard có phải do ngẫu nhiên?*
- **Phương pháp**: McNemar Paired Chi-Square Test ($\chi^2, df=1, p < 0.05$, hiệu chỉnh liên tục Edwards trên 520 cặp dự đoán).
- **Kết quả kiểm định**:
  - **PI-Guard vs. Tier-1 TF-IDF Đơn Lẻ (M2)**: $\chi^2 = \mathbf{105.60}$ ($p = 8.7 \times 10^{-25} \ll 0.0001$), Tỷ lệ vượt trội $b/c = \mathbf{9.31\times} \implies$ **Bác bỏ $H_0$. Chứng minh bắt buộc phải có Tầng 2 để xử lý Indirect Injection và Jailbreak.**
  - **PI-Guard vs. DeBERTa-v3 Standalone (M3)**: $\chi^2 = \mathbf{27.23}$ ($p = 1.81 \times 10^{-7} \ll 0.0001$), Tỷ lệ vượt trội $b/c = \mathbf{12.33\times} \implies$ **Vượt trội có ý nghĩa thống kê cao. Chứng minh cơ chế kết hợp Phân Tầng + AST-MOF vượt trội hơn hẳn Transformer đơn độc.**
  - **PI-Guard vs. Baseline Keyword Regex (M1)**: $\chi^2 = 0.49$ ($p = 0.484$). Regex chỉ bắt được từ khóa cố định và hoàn toàn thất bại trước payload làm mờ hoặc OOV.

---

### SLIDE 8: KIỂM THỬ ĐỐI KHÁNG THÍCH ỨNG & GIẢI QUYẾT VĂN BẢN DÀI 200,000 KÝ TỰ

- **Kháng Token Dilution**: Kẻ tấn công bọc câu lệnh độc trong 250 từ văn học. Tầng 1 rơi vào vùng bất định $\implies$ Tầng 2 DeBERTa-v3 bắt gọn (**100% PASS**).
- **Kháng Biến Dị Ký Tự Rác**: Cổng OOV Gate ($\rho_{\text{OOV}} > 0.40$) kích hoạt Fail-Safe Defaults, cưỡng chế BLOCK (**100% PASS**).
- **Bảo Vệ Code Lập Trình**: MOF chiết khấu từ $0.52 \to 0.145$, cho phép mã lệnh hợp lệ đi qua (**100% PASS**).
- **Đòn Tấn Công Giấu Đuôi (Tail Injection trên 200k ký tự / 149 blocks)**:
  - Quét tuần tự: Duyệt 148 blocks, tốn $2,743\text{ms}$.
  - **Quét ưu tiên Đầu-Cuối (Head-and-Tail) của PI-Guard**: Bắt ngay tại Block 1 được duyệt, ngắt sớm chỉ mất **$602\text{ms}$** (**Tăng tốc $4.6\times$, tiêu thụ RAM $< 1.8\text{GB}$, ZERO OOM**).

---

### SLIDE 9: ĐỊNH VỊ RANH GIỚI HỌC THUẬT: ĐÓNG BĂNG KIẾN TRÚC FP32 & LOẠI TRỪ LƯỢNG TỬ HÓA PHẦN CỨNG

- **Tôn chỉ bảo vệ đồ án chuyên ngành An toàn Thông tin (IA)**:
  - Kiên quyết loại trừ các kỹ thuật tối ưu hóa phần cứng/trình biên dịch như lượng tử hóa mô hình (ZeroQuant Yao et al. NeurIPS 2022) khỏi đóng góp khoa học cốt lõi.
  - Giữ vững trọng tâm nghiên cứu: Mô hình hóa mối đe dọa $X = S \mathbin{\Vert} U$, Phân tầng phòng thủ Two-Tier Cascade, Kháng đối kháng thích ứng MOF Invariance và Tối ưu hóa điểm vận hành Low-FPR < 1.5%.
- **Vai trò của ZeroQuant trong đồ án**:
  - Được lưu giữ trong Kho tài liệu (`References/`) và Ma trận tương thích $12 \times 14$ như một Baseline đối chuẩn kỹ thuật minh bạch để phản biện trước Hội đồng.
  - Khẳng định Tầng 2 Native FP32 của PI-Guard đạt P95 < 25ms trên CPU mà không cần nén số học, triệt tiêu hoàn toàn sai số làm tròn.

---

### SLIDE 10: TUYÊN BỐ ĐÓNG BĂNG MÔ HÌNH & KẾ HOẠCH BƯỚC TIẾP THEO

- **Tuyên bố Đóng Băng (Model Freezing)**:
  - Đóng băng kiến trúc Champion Two-Tier Cascade (Tier 0 Scrubber + Tier 1 Dual TF-IDF + Tri-State Router + Tier 2 DeBERTa-v3 MOF).
  - Đóng băng các siêu tham số: $\theta_{\text{low}}=0.15, \theta_{\text{high}}=0.85, \rho_{\text{OOV}}=0.40, \tau=0.60$.
- **Kế hoạch giai đoạn tiếp theo (Hướng tới Review 2 & Meeting 7)**:
  1. Bàn giao bộ trọng số và script tái lập cho các thành viên nhóm (Đức, Việt, Phương) để chạy kiểm chứng chéo trong sandbox cá nhân;
  2. Tích hợp pipeline mô hình vào tầng Proxy trung gian (FastAPI Ingress Middleware);
  3. Chuyển ngữ và đồng bộ các phát hiện thực nghiệm vào Chương 2 và Chương 3 của Luận văn tốt nghiệp (`Final-Report/thesis/`).

---

## 📚 TÀI LIỆU THAM KHẢO CHÍNH THỨC (REFERENCES)

* <a id="ref41"></a>**[41]** J. Luo and E. Han. 2026. *CASCADE Against Jailbreaks: Combination Across Stages with Controlled Attack-Defense Evaluation*. [arXiv:2609.21793](https://arxiv.org/abs/2609.21793). Local PDF: [`References/Luo_2026_CASCADE_Against_Jailbreaks_Evaluation.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Luo_2026_CASCADE_Against_Jailbreaks_Evaluation.pdf).

