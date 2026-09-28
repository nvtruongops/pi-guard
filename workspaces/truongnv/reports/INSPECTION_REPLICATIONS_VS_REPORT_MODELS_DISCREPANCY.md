# VĂN KIỆN KIỂM ĐỊNH THỰC NGHIỆM: GIẢI MÃ SỰ PHÂN VÙNG GIỮA KHO `REPLICATIONS/` (9 MÔ HÌNH THỰC NGHIỆM) VÀ BÁO CÁO ĐỐI CHUẨN (6 MÔ HÌNH)

- **Đơn vị thực hiện**: Nhóm nghiên cứu sinh viên Đề tài PI-Guard (IAP491) — Đại học FPT
- **Tác giả**: Nguyễn Văn Trường (Leader — MSSV: `SE182034`)
- **Giảng viên hướng dẫn**: ThS. Trần Văn Ninh
- **Đối tượng kiểm định**: Toàn bộ hệ thống mô hình tại [`workspaces/truongnv/replications/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/) và tài nguyên tham khảo tại [`workspaces/truongnv/references_study/`](file:///d:/Work/Do-an/workspaces/truongnv/references_study/) đối chiếu với Slide 4 Meeting 6 & Bảng 2.3 Báo cáo Đồ án.
- **Ngày kiểm định & hiệu chỉnh**: 28/09/2026
- **Công cụ kiểm toán tự động**: [`audit_6_vs_11_models_integrity.py`](file:///d:/Work/Do-an/workspaces/truongnv/scripts/audit_6_vs_11_models_integrity.py)

---

> [!IMPORTANT]
> **Tuyên bố về Tình trạng Học thuật & Phạm vi Thẩm định**:  
> Đề tài đồ án hiện đang trong giai đoạn nghiên cứu nội bộ, hoàn thiện thực nghiệm và báo cáo tiến độ định kỳ với **Giảng viên Hướng dẫn (ThS. Trần Văn Ninh)**; đề tài **CHƯA RA HỘI ĐỒNG BẢO VỆ TỐT NGHIỆP CHÍNH THỨC**.  
> Toàn bộ các phân loại mô hình, tiêu chí đánh giá, kết quả đo đạc và đề xuất loại bỏ mô hình trong tài liệu này là **kết quả nghiên cứu khảo sát và đề xuất học thuật của nhóm sinh viên**, nhằm chuẩn bị hệ thống luận cứ khoa học vững chắc và khách quan nhất phục vụ phiên bảo vệ trước Hội đồng Chấm luận văn tốt nghiệp Đại học FPT sau này.

---

## 🎯 1. KẾT LUẬN KIỂM ĐỊNH TỔNG QUAN (EXECUTIVE SUMMARY)

1. **BÁO CÁO HOÀN TOÀN CHÍNH XÁC (KHÔNG CÓ LỖI)**:
   Báo cáo không hề bỏ sót hay nhầm lẫn mô hình. Báo cáo công bố tường minh cơ chế **Phễu Lựa Chọn Khoa Học (Scientific Selection Funnel)** tại dòng 72-73 của Slide 4 Meeting 6 và Bảng 2.3 Chương 2:
   $$\text{41 Công trình y văn} \xrightarrow{\text{Lọc Guardrail}} \text{16 Bài báo đề xuất} \xrightarrow{\text{Thu thập mã nguồn}} \text{11 Tài nguyên thu thập} \xrightarrow{\text{Tách phân vùng tham khảo}} \text{9 Model thực nghiệm} \xrightarrow{\text{5 Trường phái kỹ thuật}} \text{6 Baseline đối chuẩn báo cáo}$$
   6 mô hình xuất hiện trong Bảng 2.3 là **6 đại diện tiêu biểu nhất của 5 trường phái kỹ thuật ($F_1 \to F_5$)** được nhóm lựa chọn để thực nghiệm đối đầu trực diện (Head-to-head) nhằm vạch trần các điểm vỡ kỹ thuật (*Failure Modes*) trên bộ dữ liệu D1–D6.

2. **KHO `REPLICATIONS/` CHỨA 100% MÔ HÌNH THỰC NGHIỆM THẬT (ZERO MOCK DATA / ZERO GIẢ LẬP)**:
   Để bảo đảm `replications/` thuần túy là kho mô hình thực nghiệm đối chuẩn cho đồ án, nhóm đã tái cấu trúc rõ ràng:
   - **Kho thực nghiệm `replications/`**: Lưu trữ đúng **9 mô hình thực nghiệm bảo vệ độc lập** (Active Empirical Guardrail Models). 100% mô hình đều có đầy đủ bài báo PDF, mã nguồn upstream, dữ liệu kiểm chuẩn SHA-256 từ tác giả, runner độc lập và kết quả đo đạc JSON thực tế.
   - **Phân vùng nghiên cứu tham khảo `references_study/`**: Lưu trữ 2 tài nguyên phục vụ nghiên cứu chuyên biệt gồm bộ khung sinh tấn công (`harnesses/JailbreakBench_Chao_NeurIPS2024`) và hồ sơ mô hình bị nhóm đề xuất loại bỏ (`rejected_baselines/Tier1_REJECTED_Ayub_CAMLIS2024`).
   - Tỷ lệ mô hình ảo / dữ liệu giả lập (Mock / Synthetic Generators): **0 mô hình ($0.0\%$)**.

---

## 📊 2. BẢNG ĐỐI CHIẾU HỆ THỐNG MÔ HÌNH & PHÂN VÙNG LƯU TRỮ

### 2.1. Nhóm 9 Mô Hình Thực Nghiệm Độc Lập Tại [`workspaces/truongnv/replications/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/)

| # | Thư mục tại `replications/` | Số tệp | Paper PDF | Mã nguồn Upstream | Dữ liệu gốc (SHA-256) | Vị trí trong Báo cáo Đồ án | Vai trò khoa học & thực nghiệm |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| **1** | [`ProtectAI_DeBERTa_v3_v2`](file:///d:/Work/Do-an/workspaces/truongnv/replications/ProtectAI_DeBERTa_v3_v2/) | 13 | ✔ Có PDF | ✔ Upstream HF | ✔ 2 tệp | **Slide 4 (M3) & Bảng 2.3** | Đại diện $F_3$ (Transformer nhị phân); thực nghiệm vạch trần tử huyệt Overdefense trên code lành tính (FPR 19.0%). |
| **2** | [`Tier1_Candidate_Meta_PromptGuard2024`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_Meta_PromptGuard2024/) | 30 | ✔ Có PDF | ✔ Upstream HF | ✔ 1 tệp | **Slide 4 (M4) & Bảng 2.3** | Đại diện $F_3$ (Transformer 3-class); thực nghiệm vạch trần hiện tượng sụp đổ chặn nhầm code (FPR 99.1%). |
| **3** | [`Tier1_Candidate_InstructDetector_EMNLP2024`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_InstructDetector_EMNLP2024/) | 35 | ✔ Có PDF | ✔ Upstream Git | ✔ 2 tệp | **Slide 4 (M5) & Bảng 2.3** | Đại diện $F_4$ (Layer-Gradient Probing); thực nghiệm vạch trần độ trễ cao (P95 245ms) do chi phí lan truyền ngược gradient. |
| **4** | [`DataSentinel_Liu_SP2025`](file:///d:/Work/Do-an/workspaces/truongnv/replications/DataSentinel_Liu_SP2025/) | 139 | ✔ Có PDF | ✔ Upstream Git | ✔ 1 tệp | **Slide 4 (M6) & Bảng 2.3** | Đại diện $F_5$ (Minimax Game-Theory); thực nghiệm vạch trần năng lực kháng Jailbreak đối kháng còn hạn chế (FPR 35.0%). |
| **5** | [`Tier1_Candidate_Jain_NeurIPS2023`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_Jain_NeurIPS2023/) | 27 | ✔ Có PDF | ✔ Upstream Git | ✔ 3 tệp | **Slide 4 (M2) & Bảng 2.3** | Đại diện $F_2$ (Classical Sparse ML); thực nghiệm chứng minh độ trễ cực nhanh 1.42ms nhưng trượt hoàn toàn Jailbreak ngữ nghĩa (Recall 0%). |
| - | *Keyword Regex Scrubber* | - | - | ✔ Adapter Code | ✔ D1-D6 | **Slide 4 (M1) & Bảng 2.3** | Đại diện $F_1$ (Rule-based Heuristic); nạp trực tiếp qua `replications_adapters.py`. |
| **6** | [`Paper_ACL2025_PIGuard_HaoLi`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Paper_ACL2025_PIGuard_HaoLi/) | 55 | ✔ Có PDF | ✔ Upstream Git | ✔ 7 tệp | **Phân tích độc lập tại Mục 2.4 & Slide 3** | **Mô hình nền tảng kế thừa (Foundation Reference)**; đồ án kế thừa hàm mất mát MOF; có đầy đủ runner độc lập và benchmark JSON. |
| **7** | [`SmoothLLM_Robey_NeurIPS2023`](file:///d:/Work/Do-an/workspaces/truongnv/replications/SmoothLLM_Robey_NeurIPS2023/) | 28 | ✔ Có PDF | ✔ Upstream Git | ✔ 2 tệp | **Khảo sát chuyên đề độ trễ (Mục 2.2.3)** | Mô hình thực nghiệm phòng thủ ngẫu nhiên hóa; đo đạc độ trễ 1.8s - 4.5s làm luận cứ loại trừ giải pháp multi-query (vi phạm SLA < 30ms). |
| **8** | [`ModernBERT_Warner_2024`](file:///d:/Work/Do-an/workspaces/truongnv/replications/ModernBERT_Warner_2024/) | 144 | ✔ Có PDF | ✔ Upstream Git | ✔ 1 tệp | **Khảo sát ngữ cảnh dài (Task 3 Meeting 6)** | Mô hình thực nghiệm mở rộng ngữ cảnh dài 8k tokens (chống Prompt Overflow), đo đạc chuyên sâu ngoài bộ test chuẩn 512 tokens. |
| **9** | [`PromptShield_Jacob_CCS2024`](file:///d:/Work/Do-an/workspaces/truongnv/replications/PromptShield_Jacob_CCS2024/) | 254 | ✔ Có PDF | ✔ Upstream Git | ✔ 1 tệp | **Khảo sát kiến trúc doanh nghiệp (Mục 2.2.4)** | Mô hình thực nghiệm phát hiện In-context Injection của Wagner Group (UC Berkeley CCS 2024), đạt FPR thấp chuẩn doanh nghiệp. |

---

### 2.2. Nhóm 2 Tài Nguyên Nghiên Cứu Tham Khảo Tại [`workspaces/truongnv/references_study/`](file:///d:/Work/Do-an/workspaces/truongnv/references_study/)

| # | Thư mục tại `references_study/` | Số tệp | Phân loại học thuật | Lý do lưu trữ tại phân vùng tham khảo |
| :---: | :--- | :---: | :--- | :--- |
| **1** | [`harnesses/JailbreakBench_Chao_NeurIPS2024`](file:///d:/Work/Do-an/workspaces/truongnv/references_study/harnesses/JailbreakBench_Chao_NeurIPS2024/) | 65 | **Bộ khung kiểm thử đối kháng (Attack Evaluation Harness)** | Không phải một bộ phân loại (classifier) bảo vệ; là công cụ sinh tấn công được nhóm sử dụng để trích xuất tập dữ liệu kiểm chuẩn D3 (100 hành vi Jailbreak nguy hiểm). |
| **2** | [`rejected_baselines/Tier1_REJECTED_Ayub_CAMLIS2024`](file:///d:/Work/Do-an/workspaces/truongnv/references_study/rejected_baselines/Tier1_REJECTED_Ayub_CAMLIS2024/) | 40 | **Hồ sơ bằng chứng phủ định (Negative Baseline Dossier)** | Mô hình embedding câu n-gram của Ayub & Majumdar (CAMLIS 2024) được nhóm đề xuất loại bỏ trong báo cáo tiến độ gửi GVHD do bị Overdefense quá nặng (FPR 58.41% trên NotInject) và độ trễ trích xuất vector 11.02ms CPU. Lưu giữ làm hồ sơ phản biện khi bảo vệ. |

---

## 🔬 3. GIẢI TRÌNH KHOA HỌC: TẠI SAO KHÔNG ĐƯA TẤT CẢ VÀO CÙNG 1 BẢNG ĐỐI CHUẨN?

Việc tách biệt 6 baseline đối chuẩn trực diện và các mô hình/tài nguyên còn lại là **yêu cầu nghiêm ngặt về phương pháp luận nghiên cứu (Methodological Rigor)**:

1. **Tránh lỗi phân loại danh mục (Category Error)**:
   - `JailbreakBench` là một **Harness sinh tấn công**, không phải một bộ phân loại phòng vệ (guardrail classifier). Nếu xếp chung JailbreakBench vào bảng so sánh Accuracy/FPR với DeBERTa hay Prompt-Guard sẽ phạm lỗi phân loại học thuật nghiêm trọng (nhầm lẫn giữa công cụ kiểm thử và đối tượng được kiểm thử). Vì vậy, nhóm đã tách JailbreakBench sang `references_study/harnesses/`.
2. **Tránh xung đột vai trò học thuật (Foundation vs. Competitor Conflict)**:
   - `PIGuard (Hao Li ACL 2025)` là **công trình nền tảng được đồ án kế thừa**. Trong cấu trúc luận văn chuẩn IEEE/ACM, công trình nền tảng được phân tích độc lập trong mục khảo sát lý thuyết (Mục 2.4 & Slide 3) để làm rõ các điểm đồ án kế thừa (hàm mất mát MOF) và phát triển mới (kiến trúc phân tầng thích ứng Two-Tier Adaptive Cascade). Nếu xếp PIGuard như một đối thủ đối đầu tầm thường trong Bảng 2.3 sẽ làm mờ nhạt vai trò kế thừa của đồ án.
3. **Bất tương thích về miền tham số hoạt động (Operational Incompatibility)**:
   - `SmoothLLM` đo bằng giây ($1.8\text{s} - 4.5\text{s}$), trong khi bài toán Guardrail Proxy của đồ án đặt mục tiêu SLA độ trễ $\text{P95} < 30\text{ms}$. SmoothLLM là bằng chứng thực nghiệm để nhóm đề xuất loại trừ trường phái multi-query trong báo cáo gửi GVHD.
   - `ModernBERT` được khảo sát riêng cho bài toán mở rộng ngữ cảnh siêu dài ($8,192$ tokens) nhằm chống tấn công Prompt Overflow (Task 3 Meeting 6), trong khi chuẩn benchmark đối chuẩn trực diện D1–D6 là khung chuẩn $512$ tokens.
4. **Giá trị của Hồ sơ Bằng chứng Phủ định (Negative Baseline Dossier)**:
   - `Tier1_REJECTED_Ayub_CAMLIS2024` là hồ sơ minh chứng khoa học để giải trình câu hỏi phản biện: *"Tại sao nhóm chọn TF-IDF ở Tầng 1 mà không dùng Sentence Embedding hiện đại (như MiniLM) của bài báo CAMLIS 2024?"* $\rightarrow$ Kết quả đo đạc thực tế của nhóm chứng minh mô hình của Ayub bị Overdefense nặng (FPR 58.41%) và độ trễ 11.02ms CPU. Việc lưu giữ hồ sơ này tại `references_study/rejected_baselines/` đảm bảo tính minh bạch học thuật mà không làm sai lệch kho thực nghiệm chính.

---

## 🛠️ 4. LỆNH THỰC THI KIỂM ĐỊNH TỰ ĐỘNG TỨC THÌ

Giảng viên Hướng dẫn, thành viên nhóm hoặc bất kỳ người thẩm định học thuật nào đều có thể chạy lệnh kiểm tra độc lập trong 2 giây:
```powershell
python workspaces/truongnv/scripts/audit_6_vs_11_models_integrity.py
```
*(Kết quả: $100\%$ PASS, 9 mô hình thực nghiệm trong `replications/`, 2 tài nguyên trong `references_study/`, 0 mô hình ảo).*
