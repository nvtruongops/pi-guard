# SLIDE DECK: BÁO CÁO TIẾN ĐỘ THỰC HIỆN ĐỒ ÁN (MEETING 6)
## Kết Quả Đối Chuẩn Thực Nghiệm Độc Lập & Đề Xuất Mô Hình Nghiên Cứu Lõi Hai Tầng (Two-Tier Cascade) Cho PI-Guard

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
- **Tài liệu chi tiết**: [`EXECUTIVE_PROGRESS_REPORT_MEETING_6.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_6/03_reports_and_executive_briefs/EXECUTIVE_PROGRESS_REPORT_MEETING_6.md)
- **Bản trình chiếu PowerPoint chính thức (50 Slide)**: [`../PI-GUARD-Present-Meeting-6.pptx`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_6/PI-GUARD-Present-Meeting-6.pptx) (Được biên dịch từ [`workspaces/truongnv/scripts/build_presentation_deck.py`](file:///d:/Work/Do-an/workspaces/truongnv/scripts/build_presentation_deck.py))

---

## 🗺️ CẤU TRÚC 5 PHẦN CHÍNH THỨC CỦA BỘ SLIDE (50 SLIDES WIDESCREEN 16:9)

> [!IMPORTANT]
> **QUY CHUẨN TRÌNH TỰ BÁO CÁO KHOA HỌC THỰC NGHIỆM (EVIDENCE-FIRST PARADIGM)**:
> - **Nguyên tắc cốt lõi**: Khác với cấu trúc cuốn Luận văn tĩnh (Chương 3 Thiết kế mô hình $\to$ Chương 4 Thực nghiệm kiểm chứng mô hình nhóm), báo cáo tiến độ tuần bắt buộc phải theo **quy nạp dựa trên bằng chứng (Evidence-First)**: Thực nghiệm đo đạc chỉ ra điểm vỡ của Baseline y văn trước (phục vụ Chương 2: Literature Review & Research Gaps) $\to$ làm luận cứ bắt buộc để dẫn sang Đề xuất Mô hình Kiến trúc của nhóm (Chương 3: Methodology).
> - **Phần 01 (Slide 01 - 12)**: Tổng quan đề tài, Khủng hoảng bảo mật Von Neumann, Kênh tấn công Direct/Indirect, Jailbreak & Mô hình đe dọa 5 trục NIST.
> - **Phần 02 (Slide 13 - 20)**: Khảo sát SOTA, Giới hạn lý thuyết của rào chắn đơn tầng, Đánh đổi biên độ Pareto & Kinh tế học bảo mật Low-FPR.
> - **Phần 03 (Slide 21 - 29)**: **KẾT QUẢ THỰC NGHIỆM ĐỐI CHIẾU BASELINE Y VĂN, KIỂM THỬ CHÉO & PHÂN TÍCH ĐIỂM NGHẼN BẢO MẬT** (Đo đạc 6 bộ dữ liệu D1-D6 trên các mô hình có sẵn M1-M4: TF-IDF trượt 100% Jailbreak, DeBERTa dính 19% FPR trên code, Meta chặn nhầm 99% benign code, tràn ngữ cảnh 200k).
> - **Phần 04 (Slide 30 - 39)**: **ĐỀ XUẤT KIẾN TRÚC RÀO CHẮN PHÂN TẦNG (TWO-TIER CASCADE) & GIẢI PHÁP ĐỘT PHÁ** (Kế thừa nguyên lý Saltzer-Schroeder 1975, Sơ đồ tổng thể, Bộ định tuyến 3 luồng Chow 1970, Tầng 0 Scrubber, Tầng 1 Dual TF-IDF, Tầng 2 DeBERTa-v3 CPU FP32 + MOF Invariance, Head-and-Tail Chunker khắc phục triệt để các lỗi vỡ ở Phần 03).
> - **Phần 05 (Slide 40 - 50)**: Hồ sơ Hội đồng phản biện, Gap Audit 8 bước, Loại trừ Llama Guard 7B, 5 Đột phá cốt lõi, 3 Ranh giới khiêm tốn khoa học, Model Freezing Gate & Kế hoạch Review 2.

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
| **5. Hồ sơ Phản biện & Đóng băng mô hình**| Xây dựng Council Defense Playbook & Đóng băng | [`COUNCIL_DEFENSE_RATIONALE_AND_GAP_AUDIT.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_6/03_reports_and_executive_briefs/COUNCIL_DEFENSE_RATIONALE_AND_GAP_AUDIT.md) |

---

### SLIDE 3: BÁC BỎ ẢO TƯỞNG SIÊU MÔ HÌNH ĐƠN KHỐI (THE GUARDRAIL TRILEMMA)

- **Tam giác bất khả thi của Guardrail**:
  1. Độ trễ cực thấp ($< 1.0\text{ms}$);
  2. Hiểu ngữ nghĩa sâu & Kháng đối kháng;
  3. Tỷ lệ dương tính giả gần bằng 0 ($< 1.0\%$).
- **Bài học từ các giải pháp đơn khối**:
  - *Regex/Perplexity*: Rất nhanh ($< 0.1\text{ms}$) nhưng mù ngữ nghĩa (Recall chỉ $18 - 31\%$).
  - *Generative LLM 7B/8B (Llama Guard)*: Ngữ nghĩa tốt nhưng độ trễ bùng nổ $> 1.5\text{s}$ và đòi hỏi GPU đắt tiền.
  - *Meta Prompt-Guard 86M*: Quá phòng thủ, sụp đổ trên mã nguồn (chặn nhầm $99.12\%$ code NotInject).
- **Kết luận**: Bắt buộc phải tiến hành thực nghiệm đối chuẩn độc lập để định lượng các điểm nghẽn trước khi thiết kế giải pháp.

---

### SLIDE 4: BẢNG KẾT QUẢ ĐỐI CHUẨN THỰC NGHIỆM ĐỘC LẬP CÁC MÔ HÌNH Y VĂN (D1–D6)

- **Phễu Lựa Chọn Mô Hình Thực Nghiệm Đối Chuẩn**:
  41 Công trình y văn $\to$ 16 Bài báo đề xuất Guardrail $\to$ 11 Gói mã nguồn $\to$ **6 Mô hình Champion** đại diện 6 trường phái thuật toán ($F_1 - F_5$) nạp vào Adapter Runner ([`replications_adapters.py`](file:///d:/Work/Do-an/workspaces/truongnv/src/models/replications_adapters.py)).
- **Mục Đích**: Đo lường định lượng các điểm vỡ kỹ thuật (*Failure Modes*) trên bộ dữ liệu D1–D6 phục vụ bằng chứng thực nghiệm cho **Mục 2.3 (Khoảng trống Nghiên cứu - Research Gaps)**.

| Mô hình Champion / Baseline Y Văn | Direct Recall (D1) | Indirect Recall (D2) | Jailbreak Recall (D3) | Code Acc (D5 - NotInject) | Benign FPR (D6) | Độ trễ P95 CPU | Điểm Yếu / Failure Mode Thực Nghiệm |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **M1: Baseline Keyword Regex** | $10.4\%$ | $100.0\%$ | $100.0\%$ | $100.0\%$ | $0.0\%$ | $< 0.5\text{ms}$ | Bất lực trước biến thể mới ($10.4\%$ recall D1) |
| **M2: Dual-Space TF-IDF (Jain et al. 2023)** | $83.3\%$ | $24.0\%$ | **$0.0\%$** | $100.0\%$ | $0.0\%$ | **$12.9\text{ms}$** | Trượt hoàn toàn Jailbreak ngữ nghĩa ($0.0\%$ recall) |
| **M3: ProtectAI DeBERTa-v3 v2** | $58.3\%$ | $100.0\%$ | $62.0\%$ | **$81.0\%$** | $6.0\%$ | $414.1\text{ms}$ | Quá phòng thủ mã nguồn (**$19.0\%$ FPR** trên code D5) |
| **M4: Meta Prompt-Guard 86M (Meta 2024)** | $68.5\%$ | $42.0\%$ | $18.5\%$ | **$0.9\%$** | $28.5\%$ | $38.5\text{ms}$ | Sụp đổ quá phòng thủ (chặn nhầm $99.1\%$ code) |
| **M5: InstructDetector (Zhao et al. 2024)** | $71.0\%$ | $84.0\%$ | $29.0\%$ | $86.0\%$ | $5.5\%$ | $245.0\text{ms}$ | Chi phí tính toán gradient lớn khi phục vụ |
| **M6: DataSentinel (Liu et al. S&P 2025)** | $74.2\%$ | $88.0\%$ | $34.0\%$ | $88.5\%$ | $4.2\%$ | $180.0\text{ms}$ | Kháng Jailbreak đối kháng phức tạp còn hạn chế |

*(Ghi chú: Toàn bộ chỉ số đo đạc thực tế 100% trên các checkpoint tải về từ y văn công khai, phục vụ Chương 2: Literature Replication & Research Gaps)*

---

### SLIDE 5: ĐÁNH GIÁ KHOẢNG TRỐNG NGHIÊN CỨU & CÁC THÁCH THỨC ĐỐI KHÁNG TỪ Y VĂN

- **Khoảng trống Nghiên cứu Thực nghiệm (Empirical Research Gaps)**:
  - *Mô hình nông (TF-IDF / N-gram)*: Bắt từ khóa nhanh nhưng mù ngữ nghĩa đối kháng ($0.0\%$ Jailbreak recall).
  - *Mô hình sâu đơn khối (DeBERTa / Prompt-Guard)*: Độ trễ P95 cao, dính overdefense nặng trên code lập trình lành tính (FPR $19.0\% - 99.1\%$).
- **Thách thức Đối kháng Cần Giải Quyết**:
  - **Token Dilution**: Bọc câu lệnh độc hại trong văn bản dài nhằm pha loãng phân phối n-gram.
  - **Ký tự rác & Biến dị cú pháp**: Sử dụng ký tự OOV, leetspeak, khoảng trắng zero-width để lách bộ lọc từ điển.
  - **Tràn ngữ cảnh (Prompt Overflow)**: Giấu payload ở đuôi văn bản dài 200k ký tự vượt qua cửa sổ 512 tokens.
- **Ý nghĩa định hướng cho Chương 3**: Các điểm vỡ thực nghiệm trên là bằng chứng khoa học bắt buộc phải thiết kế kiến trúc phân tầng (Two-Tier Cascade) có cơ chế lọc rác Tier 0 và xử lý dừng sớm BlockChunker.

---

### SLIDE 6: KIẾN TRÚC PHÂN TẦNG ĐỀ XUẤT (TWO-TIER CASCADE ARCHITECTURE) & MINH CHỨNG KHOA HỌC

- **Bản Chất Đề Xuất (Novel Synthesis Kế Thừa Từ 9 Công Trình Khoa Học)**:
  - Bác bỏ ngộ nhận "chỉ ghép từ 2 bài báo"; kiến trúc Two-Tier Cascade là công trình tổng hợp nguyên bản kế thừa có chọn lọc từ **9 bài báo khoa học** trên 4 tầng vận hành (Hackett 2025 & Yuan 2024 tại Lớp 0; Jain 2023, Chow 1970 [[15]](#ref15) & Platt 1999 tại Tầng 1; Luo & Han 2026 [[41]](#ref41), Angelopoulos 2024 & Jacob 2024 tại Router; He 2023 & Hao Li 2025 tại Tầng 2; Zhou 2026 & Saltzer & Schroeder 1975 [[27]](#ref27) tại hạ tầng hệ thống).
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

---

### SLIDE 7: MÔ HÌNH HÓA TOÁN HỌC & CÔNG THỨC LÕI

- **Mối đe dọa chuỗi ghép**:
  $$X = S \mathbin{\Vert} U \quad (S: \text{System/RAG}, \; U: \text{User Query})$$
- **Hiệu chuẩn xác suất Tầng 1 (Platt Scaling)**:
  $$P(\text{Malicious} \mid X) = \frac{1}{1 + \exp(-(\mathbf{w}^T \mathbf{z} + b))} \quad \text{với } \mathbf{z} = [\mathbf{z}_{\text{word}} \mathbin{\Vert} \mathbf{z}_{\text{char}}]$$
- **Mật độ dị biệt ký tự (OOV Entropy Density)**:
  $$\rho_{\text{OOV}}(X) = \frac{N_{\text{irregular}}}{L} + 0.5 \cdot \frac{N_{\text{single}}}{N_{\text{tokens}}}$$
- **Bất biến che phủ mã lệnh (Masked Overlap Fraction - MOF)**:
  $$S_{\text{final}} = S_{\text{raw}} \cdot (1.0 - \text{MOF}(X)) \quad \text{khi } \text{MOF} > 0.50 \land \neg \text{HasExplicitAttack}$$

---

### SLIDE 8: GIẢI PHÁP ĐỘT PHÁ VĂN BẢN DÀI 200,000 KÝ TỰ & CHỐNG OVERDEFENSE

- **Tầng 2 DeBERTa-v3 & Cơ chế Kháng Overdefense MOF**:
  - Disentangled Attention 3 ma trận (Content-Content, Content-Position, Position-Content) và Dynamic Class-Weighted Loss.
  - Chiết khấu ngưỡng động $\tau_{\text{eff}} = \tau_0 + \gamma \cdot \text{MOF}(X)$ bảo vệ mã nguồn NotInject trên phần cứng CPU Native FP32.
- **Thuật toán Chunker Văn bản dài 200k (Figure: `fig_chunker_head_and_tail_algorithm.png`)**:
  - Quét ưu tiên vị trí Head-and-Tail dừng sớm tại Block 1.
  - Bắt đòn tấn công giấu ở đuôi (Tail Injection trên 200k ký tự) ngay tại Block đầu tiên quét (tiêu thụ RAM $< 1.8\text{GB}$, ZERO OOM).

---

### SLIDE 9: ĐỊNH VỊ RANH GIỚI HỌC THUẬT: ĐÓNG BĂNG KIẾN TRÚC FP32 & LOẠI TRỪ LƯỢNG TỬ HÓA PHẦN CỨNG

- **Tôn chỉ bảo vệ đồ án chuyên ngành An toàn Thông tin (IA)**:
  - Kiên quyết loại trừ các kỹ thuật tối ưu hóa phần cứng/trình biên dịch như lượng tử hóa mô hình (ZeroQuant Yao et al. NeurIPS 2022) khỏi đóng góp khoa học cốt lõi.
  - Giữ vững trọng tâm nghiên cứu: Mô hình hóa mối đe dọa $X = S \mathbin{\Vert} U$, Phân tầng phòng thủ Two-Tier Cascade, Kháng đối kháng thích ứng MOF Invariance và Tối ưu hóa điểm vận hành Low-FPR < 1.5%.
- **Vai trò của ZeroQuant trong đồ án**:
  - Được lưu giữ trong Kho tài liệu (`References/`) và Ma trận tương thích $12 \times 14$ như một Baseline đối chuẩn kỹ thuật minh bạch để phản biện trước Hội đồng.
  - Khẳng định Tầng 2 Native FP32 của PI-Guard đạt P95 < 25ms trên CPU mà không cần nén số học, triệt tiêu hoàn toàn sai số làm tròn.

---

### SLIDE 10: TUYÊN BỐ ĐÓNG BĂNG MÔ HÌNH & KẾ HOẠCH BÀN GIAO REVIEW 2

- **Tuyên bố Đóng Băng (Model Freezing)**:
  - Đóng băng kiến trúc Champion Two-Tier Cascade (Tier 0 Scrubber + Tier 1 Dual TF-IDF + Tri-State Router + Tier 2 DeBERTa-v3 MOF).
  - Đóng băng các siêu tham số: $\theta_{\text{low}}=0.15, \theta_{\text{high}}=0.85, \rho_{\text{OOV}}=0.40, \tau=0.60$.
- **Kế hoạch giai đoạn tiếp theo (Hướng tới Review 2 & Meeting 7)**:
  1. Bàn giao bộ trọng số và script tái lập cho các thành viên nhóm (Đức, Việt, Phương) để chạy kiểm chứng chéo trong sandbox cá nhân;
  2. Tích hợp pipeline mô hình vào tầng Proxy trung gian (FastAPI Ingress Middleware);
  3. Chuyển ngữ và đồng bộ các phát hiện thực nghiệm vào Chương 2 và Chương 3 của Luận văn tốt nghiệp (`Final-Report/thesis/`).

---

## 📚 TÀI LIỆU THAM KHẢO CHÍNH THỨC (REFERENCES)

- <a id="ref1"></a>**[[1]]** OWASP Top 10 for Large Language Model Applications, "LLM01: Prompt Injection," _OWASP Foundation_, Tech. Rep., 2025.
- <a id="ref2"></a>**[[2]]** A. Vassilev et al., "Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations," _NIST AI 100-2e2025_, 2024. [DOI: 10.6028/NIST.AI.100-2e2025](https://doi.org/10.6028/NIST.AI.100-2e2025).
- <a id="ref15"></a>**[[15]]** C. K. Chow, "On optimum recognition error and reject tradeoff," _IEEE Transactions on Information Theory_, vol. 16, no. 1, pp. 41–46, 1970.
- <a id="ref27"></a>**[[27]]** J. H. Saltzer and M. D. Schroeder, "The protection of information in computer systems," _Proceedings of the IEEE_, vol. 63, no. 9, pp. 1278–1308, 1975.
- <a id="ref41"></a>**[[41]]** Z. Luo and J. Han, "CASCADE: Efficient and Accurate Guardrails for Large Language Models via Adaptive Routing," _arXiv preprint arXiv:2602.04987_, 2026.
