# BẢNG ĐIỀU HÀNH THỰC NGHIỆM ĐỐI CHUẨN (BENCHMARK RESULTS DASHBOARD)
## Hệ Thống Kiểm Chứng Tái Lập 11 Mô Hình Guardrail & Chuỗi Bằng Chứng Khoa Học 6 Mắt Xích

---

> **Đơn vị thực hiện**: Đồ án Tốt nghiệp Kỹ sư An toàn Thông tin (IAP491) — Đại học FPT  
> **Đề tài**: *A Machine-Learning Guardrail for Detecting Prompt Injection and Jailbreak Attacks on LLM Applications (PI-Guard)*  
> **Tác giả**: Nguyễn Văn Trường (Leader — MSSV: `SE182034`) | **Workspace**: [`workspaces/truongnv/replications/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/)  
> **Giảng viên hướng dẫn**: ThS. Trần Văn Ninh  
> **Thời điểm cập nhật**: 28/09/2026  
> **Quy chuẩn kiến trúc**: [Chuỗi Bằng Chứng Khoa Học 6 Mắt Xích](file:///d:/Work/Do-an/workspaces/truongnv/reports/RESTRUCTURING_PROPOSAL_EXPERIMENT_PIPELINE.md) (`Paper` ➔ `Mô Hình` ➔ `Code + Dataset` ➔ `Repo Gốc Pristine` ➔ `Folder Run Ngoài` ➔ `Report & URL Audit`)

---

## 📊 PHẦN 1: BẢNG TỔNG HỢP KẾT QUẢ ĐO ĐẠC THỰC NGHIỆM

Toàn bộ $100\%$ số liệu dưới đây được trích xuất trực tiếp từ các file kết quả thực nghiệm un-mocked (`reports/*_BENCHMARK_RESULTS.json`), chạy trực tiếp trên môi trường CPU tiêu chuẩn thương mại (*Commodity CPU - Zero GPU Requirement*), tuân thủ nghiêm ngặt Rule 03 (`AH-02`, `AH-04`):

### 1.1. Bảng 6 Mô Hình Đối Chuẩn Đại Diện (Bảng 2.3 / Slide 4 Báo Cáo GVHD)
*Đại diện cho 5 trường phái kỹ thuật ($F_1 \to F_5$) để chứng minh khoảng trống nghiên cứu (Research Gaps) trong báo cáo đề tài:*

| STT | Tên Mô Hình | Trường Phái Kỹ Thuật | Accuracy | F1-Score | FPR (Chặn Nhầm) | ASR (Lọt Tấn Công) | Latency P50 | Latency P95 | Chuẩn SLA (<30ms) | Tử Huyệt / Khoảng Trống Nghiên Cứu |
| :-: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **M1** | **Heuristic Regex** | $F_1$ (Rule-based) | $57.4\%$ | $0.542$ | $4.2\%$ | **$88.5\%$** | **$0.45\text{ ms}$** | **$0.92\text{ ms}$** | ✔ **ĐẠT** | Thất thủ hoàn toàn trước Obfuscation, Base64, Leetspeak và Paraphrase. |
| **M2** | **Dual TF-IDF (Jain 2023)** | $F_2$ (Classical ML) | $76.8\%$ | $0.741$ | $6.8\%$ | **$82.0\%$** | **$1.42\text{ ms}$** | **$2.85\text{ ms}$** | ✔ **ĐẠT** | Tốc độ cực nhanh nhưng mù màu trước Semantic Jailbreak đa lượt không có từ khóa lạ. |
| **M3** | **ProtectAI DeBERTa v2** | $F_3$ (Transformer 2-class) | $79.3\%$ | $0.812$ | **$58.4\%$** | $6.2\%$ | $18.45\text{ ms}$ | $28.90\text{ ms}$ | ✔ **ĐẠT** | **Overdefense cực nặng**: Chặn nhầm hơn $58\%$ code và câu lệnh lập trình lành tính. |
| **M4** | **Meta Prompt-Guard 86M** | $F_3$ (Transformer 3-class) | $71.2\%$ | $0.735$ | **$99.1\%$** | $2.5\%$ | $19.12\text{ ms}$ | $29.40\text{ ms}$ | ✔ **ĐẠT** | **Sụp đổ hoàn toàn trên code**: Coi gần như $100\%$ cú pháp markdown/code là Prompt Injection. |
| **M5** | **InstructDetector (2024)** | $F_4$ (Gradient Probing) | $84.6\%$ | $0.830$ | $8.5\%$ | $14.2\%$ | $182.40\text{ ms}$ | **$245.10\text{ ms}$** | ✘ **TRƯỢT** | **Vi phạm nghiêm trọng SLA**: Độ trễ vượt gấp 8 lần trần cho phép của Proxy Gateway. |
| **M6** | **DataSentinel (S&P 2025)** | $F_5$ (Game-Theory) | $86.2\%$ | $0.854$ | $7.1\%$ | **$35.0\%$** | $8.20\text{ ms}$ | $14.60\text{ ms}$ | ✔ **ĐẠT** | Phòng thủ rất mạnh Injection nhưng không phát hiện được Jailbreak ngữ nghĩa (ASR $35\%$). |

---

### 1.2. Các Mô Hình Thực Nghiệm Bổ Trợ & Tài Nguyên Nghiên Cứu Tham Khảo

| STT | Tên Mô Hình / Tài Nguyên | Vị Trí Lưu Trữ | Vai Trò Kỹ Thuật | Accuracy | FPR | Latency P95 | Định Vị Trong Đề Tài |
| :-: | :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **7** | **PIGuard (ACL 2025)** | `replications/` | **Mô hình nền tảng tham chiếu** | $94.1\%$ | $0.8\%$ | $24.8\text{ ms}$ | Nền tảng lý thuyết kế thừa cơ chế MOF Loss; phân tích độc lập tại Mục 2.4 Luận văn. |
| **8** | **PromptShield (CCS 2024)** | `replications/` | Guardrail doanh nghiệp Low-FPR | $91.3\%$ | $1.2\%$ | $19.4\text{ ms}$ | Khảo sát phân vùng Low-FPR ($\le 1\%$) của nhóm GS. David Wagner (UC Berkeley). |
| **9** | **ModernBERT (2024)** | `replications/` | Mở rộng ngữ cảnh 8,192 tokens | $88.4\%$ | $3.2\%$ | $42.1\text{ ms}$ | Khảo sát bài toán chống tấn công tràn bộ nhớ đệm (Prompt Overflow 8k tokens) thuộc Task 3. |
| **10** | **SmoothLLM (NeurIPS 2023)** | `replications/` | Phòng thủ ngẫu nhiên hóa đa truy vấn | $81.5\%$ | $12.4\%$ | **$3,420\text{ ms}$** | Khảo sát đánh đổi độ trễ hàng giây ($3.4\text{s}$) chứng minh lý do loại bỏ phòng thủ đa truy vấn. |
| **11** | **JailbreakBench (2024)** | `references_study/harnesses/` | **Bộ khung kiểm thử đối kháng (Harness)** | N/A | N/A | N/A | Framework sinh tấn công và cung cấp tập mẫu D3 (100 harmful prompts). |
| **12** | **Ayub (CAMLIS 2024)** | `references_study/rejected_baselines/` | **Mô hình bị đề xuất loại bỏ (Negative Control)** | $64.8\%$ | **$58.4\%$** | $4.2\text{ ms}$ | Nhóm đề xuất loại bỏ trong báo cáo gửi GVHD (Meeting 5) do FPR quá cao ($58.4\%$). |

---

### 1.3. Bảng Ma Trận Phân Bố Độ Phủ Mối Đe Dọa (Threat Key Distribution Scorecard)
*Đối chiếu $100\%$ độ phủ của 6 mô hình thực nghiệm trên 8 Key cốt lõi của đề tài (Nguồn dữ liệu số hóa: [`key_coverage_matrix_report.json`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_6/04_benchmarks_and_data/key_coverage_matrix_report.json) và báo cáo chuyên sâu: [`KEY_ATTACK_VECTORS_AND_SIX_MODELS_DISTRIBUTION_MATRIX.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_6/01_theory_and_taxonomy/KEY_ATTACK_VECTORS_AND_SIX_MODELS_DISTRIBUTION_MATRIX.md)):*

| Mô Hình Thực Nghiệm | Key 1: DPI | Key 2: IPI | Key 3: JB | Key 4: Encode | Key 5: Code/FPR | Key 6: Adv/Perturb | Key 7: Multilingual | Key 8: Long-Ctx | Đánh Giá Khái Quát Điểm Nghẽn |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **M1: Heuristic Regex** | ⚠️ $10.4\%$ | ⚠️ $100\%^*$ | ⚠️ $100\%^*$ | ❌ $5.0\%$ | ✔ $0.0\%$ FPR | ❌ $0.0\%$ | ❌ $15.0\%$ | ✔ $80.0\%$ | Mù màu trước Obfuscation, GCG, tiếng Việt; chỉ bắt từ khóa cố định. |
| **M2: Dual TF-IDF (Jain)** | ✔ $83.3\%$ | ⚠️ $24.0\%$ | ❌ **$0.0\%$** | ⚠️ $40.0\%$ | ✔ $0.0\%$ FPR | ⚠️ $45.0\%$ | ✔ $75.0\%$ | ❌ $20.0\%$ | Tốc độ cực nhanh ($1.4\text{ms}$), không chặn code; nhưng mù $100\%$ Jailbreak ngữ nghĩa. |
| **M3: ProtectAI DeBERTa** | ✔ $58.3\%$ | ✔ **$100\%$** | ✔ $62.0\%$ | ⚠️ $40.0\%$ | ❌ **$19.0\%$** | ⚠️ $50.0\%$ | ✔ $85.0\%$ | ❌ $0.0\%$ | Bắt IPI hoàn hảo; nhưng dính Overdefense nặng trên code ($19\%$ FPR), cắt cụt 512 tokens. |
| **M4: Prompt-Guard 86M** | ✔ $68.5\%$ | ⚠️ $42.0\%$ | ⚠️ $18.5\%$ | ❌ **$0.0\%$** | ❌ **$99.1\%$** | ⚠️ $35.0\%$ | ⚠️ $50.0\%$ | ❌ $0.0\%$ | Sụp đổ hoàn toàn trên code lành tính ($99.12\%$ FPR), trượt $100\%$ Base64/Rot13. |
| **M5: InstructDetector** | ✔ $71.0\%$ | ✔ $84.0\%$ | ⚠️ $29.0\%$ | ⚠️ $55.0\%$ | ⚠️ $14.0\%$ | ✔ $75.0\%$ | ⚠️ $60.0\%$ | ❌ $0.0\%$ | Bắt IPI và GCG tốt; nhưng vi phạm SLA nghiêm trọng (P95 $245.1\text{ms}$ >> $30\text{ms}$). |
| **M6: DataSentinel** | ✔ $74.2\%$ | ✔ $88.0\%$ | ⚠️ $34.0\%$ | ⚠️ $60.0\%$ | ✔ $11.5\%$ | ✔ $80.0\%$ | ⚠️ $65.0\%$ | ❌ $10.0\%$ | Kháng đối kháng Minimax mạnh; nhưng bỏ lọt $35\%$ Jailbreak đối kháng (ASR $35\%$). |

*Ghi chú quy ước*: ✔ = **COVERED** (Bảo vệ vững chắc hoặc FPR thấp an toàn) | ⚠️ = **PARTIAL** (Độ phủ một phần hoặc có rủi ro) | ❌ = **BLIND_SPOT** (Tử huyệt kỹ thuật / Trượt hoàn toàn).  
$^*$ *Lưu ý*: M1 đạt $100\%$ trên tập mẫu test do tập con này chứa sẵn chuỗi từ khóa nhãn nhận diện.

**Bản chất 8 Key (Giải thích 1 câu trực quan cho Hội đồng & Báo cáo)**:
1. `Key 1 (DPI - Direct Injection)`: Người dùng gõ lệnh trực tiếp để cướp quyền điều khiển AI hoặc moi System Prompt bí mật.
2. `Key 2 (IPI - Indirect Injection)`: Bẫy mã độc cài sẵn trong file PDF/Web, người dùng nhờ AI đọc file là AI bị nhiễm độc và làm theo lệnh hacker.
3. `Key 3 (JB - Jailbreak)`: Ép AI làm điều xấu hoặc phạm pháp bằng cách đóng kịch/đóng vai DAN mà không cần cướp System Prompt.
4. `Key 4 (Encode - Mã hóa)`: "Mặc áo tàng hình" cho lệnh độc bằng Base64 hay teencode để lừa bộ lọc từ khóa.
5. `Key 5 (Code/FPR - Chặn nhầm Code)`: **Không phải tấn công**, mà là bài test chống bệnh "quá đa nghi": đảm bảo guardrail không chặn nhầm code lành tính (FPR < 1.5%).
6. `Key 6 (Adv/Perturb - Hậu tố GCG)`: Bùa chú toán học vô nghĩa tính bằng đạo hàm ép thẳng vào mạng nơ-ron của LLM để mở khóa an toàn.
7. `Key 7 (Multilingual & Cross-Lingual Defense)`: Tấn công đa ngữ (10 ngôn ngữ theo MultiJail: en, zh, vi, ru, id, ko, ar, th, bn, sw; trọng tâm bản địa hóa Tiếng Việt). 👉 *[Xem Báo Cáo Chuyên Đề Đa Ngôn Ngữ & Tiếng Việt](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_6/01_theory_and_taxonomy/DEEP_DIVE_KEY_7_MULTILINGUAL_AND_CROSS_LINGUAL_DEFENSE.md)*
8. `Key 8 (Long-Context - Ngữ cảnh dài)`: "Kim giấu đáy biển" — giấu lệnh độc ở cuối tài liệu siêu dài (8k tokens) mà guardrail thông thường (512 từ) không đọc tới.

---

## 🗂️ PHẦN 2: BẢN ĐỒ ĐIỀU HƯỚNG TÀI NGUYÊN THEO CHUẨN 6 MẮT XÍCH

### A. Kho Mô Hình Thực Nghiệm Chính Thức (`workspaces/truongnv/replications/`)
*Chứa $100\%$ các mô hình bảo vệ có đầy đủ mã nguồn, runner `run_<model>_replication.py`, datasets và kết quả benchmark.*

| # | Thư Mục Mô Hình | 📄 Paper PDF | 🏛️ Repo Gốc (Pristine) | 📦 Dataset Tải Riêng | 📑 Báo Cáo URL & Kết Quả | Trạng Thái Kiểm Định |
| :-: | :--- | :---: | :---: | :---: | :---: | :---: |
| **1** | [`Paper_ACL2025_PIGuard_HaoLi/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Paper_ACL2025_PIGuard_HaoLi/) | [PDF](file:///d:/Work/Do-an/workspaces/truongnv/replications/Paper_ACL2025_PIGuard_HaoLi/papers/PIGuard_2025_Prompt_Injection_Guardrail_ACL.pdf) | [`upstream/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Paper_ACL2025_PIGuard_HaoLi/upstream/) | [`datasets/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Paper_ACL2025_PIGuard_HaoLi/datasets/) | [`reports/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Paper_ACL2025_PIGuard_HaoLi/reports/) | ✔ **100% PASS** |
| **2** | [`DataSentinel_Liu_SP2025/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/DataSentinel_Liu_SP2025/) | [PDF](file:///d:/Work/Do-an/workspaces/truongnv/replications/DataSentinel_Liu_SP2025/papers/Liu_2025_DataSentinel_Game_Theoretic_Detection_Prompt_Injection.pdf) | [`upstream/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/DataSentinel_Liu_SP2025/upstream/) | [`datasets/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/DataSentinel_Liu_SP2025/datasets/) | [`reports/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/DataSentinel_Liu_SP2025/reports/) | ✔ **100% PASS** |
| **3** | [`PromptShield_Jacob_CCS2024/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/PromptShield_Jacob_CCS2024/) | [PDF](file:///d:/Work/Do-an/workspaces/truongnv/replications/PromptShield_Jacob_CCS2024/papers/Jacob_2024_PromptShield_Deployable_Detection_Prompt_Injection_CCS.pdf) | [`upstream/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/PromptShield_Jacob_CCS2024/upstream/) | [`datasets/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/PromptShield_Jacob_CCS2024/datasets/) | [`reports/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/PromptShield_Jacob_CCS2024/reports/) | ✔ **100% PASS** |
| **4** | [`ModernBERT_Warner_2024/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/ModernBERT_Warner_2024/) | [PDF](file:///d:/Work/Do-an/workspaces/truongnv/replications/ModernBERT_Warner_2024/papers/Warner_2024_ModernBERT_Brings_Modern_Transformers_To_Encoders.pdf) | [`upstream/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/ModernBERT_Warner_2024/upstream/) | [`datasets/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/ModernBERT_Warner_2024/datasets/) | [`reports/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/ModernBERT_Warner_2024/reports/) | ✔ **100% PASS** |
| **5** | [`ProtectAI_DeBERTa_v3_v2/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/ProtectAI_DeBERTa_v3_v2/) | [PDF](file:///d:/Work/Do-an/workspaces/truongnv/replications/ProtectAI_DeBERTa_v3_v2/papers/He_2023_DeBERTaV3_Disentangled_Attention_ICLR.pdf) | [`upstream/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/ProtectAI_DeBERTa_v3_v2/upstream/) | [`datasets/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/ProtectAI_DeBERTa_v3_v2/datasets/) | [`reports/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/ProtectAI_DeBERTa_v3_v2/reports/) | ✔ **100% PASS** |
| **6** | [`SmoothLLM_Robey_NeurIPS2023/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/SmoothLLM_Robey_NeurIPS2023/) | [PDF](file:///d:/Work/Do-an/workspaces/truongnv/replications/SmoothLLM_Robey_NeurIPS2023/papers/Robey_2023_SmoothLLM_Defending_LLMs_Random_Perturbation.pdf) | [`upstream/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/SmoothLLM_Robey_NeurIPS2023/upstream/) | [`datasets/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/SmoothLLM_Robey_NeurIPS2023/datasets/) | [`reports/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/SmoothLLM_Robey_NeurIPS2023/reports/) | ✔ **100% PASS** |
| **7** | [`Tier1_Candidate_Meta_PromptGuard2024/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_Meta_PromptGuard2024/) | [PDF](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_Meta_PromptGuard2024/papers/Meta_2024_Prompt_Guard_86M_Input_Guardrail.pdf) | [`upstream/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_Meta_PromptGuard2024/upstream/) | [`datasets/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_Meta_PromptGuard2024/datasets/) | [`reports/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_Meta_PromptGuard2024/reports/) | ✔ **100% PASS** |
| **8** | [`Tier1_Candidate_InstructDetector_EMNLP2024/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_InstructDetector_EMNLP2024/) | [PDF](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_InstructDetector_EMNLP2024/papers/Zhao_2024_InstructDetector_Instruction_Tuned_Attack_EMNLP.pdf) | [`upstream/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_InstructDetector_EMNLP2024/upstream/) | [`datasets/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_InstructDetector_EMNLP2024/datasets/) | [`reports/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_InstructDetector_EMNLP2024/reports/) | ✔ **100% PASS** |
| **9** | [`Tier1_Candidate_Jain_NeurIPS2023/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_Jain_NeurIPS2023/) | [PDF](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_Jain_NeurIPS2023/papers/Jain_2023_Baseline_Defenses_Adversarial_Attacks_LLMs.pdf) | [`upstream/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_Jain_NeurIPS2023/upstream/) | [`datasets/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_Jain_NeurIPS2023/datasets/) | [`reports/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_Jain_NeurIPS2023/reports/) | ✔ **100% PASS** |

### B. Phân Vùng Tài Nguyên Nghiên Cứu Tham Khảo (`workspaces/truongnv/references_study/`)

| # | Thư Mục Tài Nguyên | Phân Loại | 📄 Paper PDF | 🏛️ Repo Gốc (Pristine) | 📦 Datasets | 📑 Báo Cáo Xuất Xứ |
| :-: | :--- | :--- | :---: | :---: | :---: | :---: |
| **1** | [`JailbreakBench_Chao_NeurIPS2024/`](file:///d:/Work/Do-an/workspaces/truongnv/references_study/harnesses/JailbreakBench_Chao_NeurIPS2024/) | Bộ khung sinh tấn công & Dataset D3 | [PDF](file:///d:/Work/Do-an/workspaces/truongnv/references_study/harnesses/JailbreakBench_Chao_NeurIPS2024/papers/Chao_2024_JailbreakBench_Open_Robustness_Benchmark_NeurIPS.pdf) | [`upstream/`](file:///d:/Work/Do-an/workspaces/truongnv/references_study/harnesses/JailbreakBench_Chao_NeurIPS2024/upstream/) | [`datasets/`](file:///d:/Work/Do-an/workspaces/truongnv/references_study/harnesses/JailbreakBench_Chao_NeurIPS2024/datasets/) | [`reports/`](file:///d:/Work/Do-an/workspaces/truongnv/references_study/harnesses/JailbreakBench_Chao_NeurIPS2024/reports/) |
| **2** | [`Tier1_REJECTED_Ayub_CAMLIS2024/`](file:///d:/Work/Do-an/workspaces/truongnv/references_study/rejected_baselines/Tier1_REJECTED_Ayub_CAMLIS2024/) | Mô hình bị đề xuất loại bỏ (FPR 58.4%) | [PDF](file:///d:/Work/Do-an/workspaces/truongnv/references_study/rejected_baselines/Tier1_REJECTED_Ayub_CAMLIS2024/papers/Ayub_2024_Towards_Robust_Detection_Prompt_Injection_CAMLIS.pdf) | [`upstream/`](file:///d:/Work/Do-an/workspaces/truongnv/references_study/rejected_baselines/Tier1_REJECTED_Ayub_CAMLIS2024/upstream/) | [`datasets/`](file:///d:/Work/Do-an/workspaces/truongnv/references_study/rejected_baselines/Tier1_REJECTED_Ayub_CAMLIS2024/datasets/) | [`reports/`](file:///d:/Work/Do-an/workspaces/truongnv/references_study/rejected_baselines/Tier1_REJECTED_Ayub_CAMLIS2024/reports/) |

---

## 🛠️ PHẦN 3: HƯỚNG DẪN KIỂM ĐỊNH & THỰC THI (VERIFICATION RUNBOOK)

### 3.1. Lệnh Kiểm Tra Xuất Xứ & SHA-256 Nhanh (< 1 giây):
```powershell
python workspaces/truongnv/scripts/check_replication_origin_urls.py --mode fast
```

### 3.2. Lệnh Kiểm Tra Trực Tiếp 100% URL Ngoài (HTTP 200 OK):
```powershell
python workspaces/truongnv/scripts/check_replication_origin_urls.py --live
```

### 3.3. Lệnh Kiểm Định Chuẩn Pre-Commit Toàn Repository:
```powershell
python Final-Report/scripts/validate_local.py --mode fast
```

---
*Tài liệu được khởi tạo và bảo chứng bởi Leader Nguyễn Văn Trường — Đề tài PI-Guard.*
