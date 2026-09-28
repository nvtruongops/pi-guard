# DANH MỤC MÔ HÌNH THỰC NGHIỆM ĐỐI CHUẨN (REPLICATIONS REPO & DATASET HUB)
## Hệ Thống 9 Mô Hình Thực Nghiệm Độc Lập Theo Chuỗi Bằng Chứng Khoa Học 6 Mắt Xích

Chào mừng đến với phân hệ thực nghiệm đối chuẩn của Leader **Nguyễn Văn Trường** (`workspaces/truongnv/replications/`). Thư mục này lưu trữ toàn bộ các mô hình y văn đã được tái lập (replicated), mã nguồn tác giả gốc, tập dữ liệu kiểm thử độc lập và kết quả benchmark phục vụ bảo vệ đồ án tốt nghiệp **PI-Guard** (IAP491).

---

> [!NOTE]
> **Tuyên bố về Tình trạng Học thuật & Phạm vi Thẩm định**:  
> Đề tài đồ án hiện đang trong giai đoạn nghiên cứu nội bộ, hoàn thiện thực nghiệm và báo cáo tiến độ định kỳ với **Giảng viên Hướng dẫn (ThS. Trần Văn Ninh)**; đề tài **CHƯA RA HỘI ĐỒNG BẢO VỆ TỐT NGHIỆP CHÍNH THỨC**.  
> Toàn bộ các phân loại mô hình, tiêu chí đánh giá, kết quả đo đạc và đề xuất loại bỏ mô hình trong tài liệu này là **kết quả nghiên cứu khảo sát và đề xuất học thuật của nhóm sinh viên**, nhằm chuẩn bị hệ thống luận cứ khoa học vững chắc và khách quan nhất phục vụ phiên bảo vệ trước Hội đồng Chấm luận văn tốt nghiệp Đại học FPT sau này.

---

> 🚀 **TRUY CẬP NHANH BẢNG KẾT QUẢ ĐO ĐẠC & NGUỒN GỐC DỮ LIỆU TOÀN DIỆN**:  
> 📊 [**`BENCHMARK_RESULTS_DASHBOARD.md`**](file:///d:/Work/Do-an/workspaces/truongnv/replications/BENCHMARK_RESULTS_DASHBOARD.md)  
> 📦 [**Sổ Bộ Nguồn Gốc Dữ Liệu 25 Tệp SHA-256 (`SHARED_DATASETS_PROVENANCE.md`)**](file:///d:/Work/Do-an/workspaces/truongnv/replications/SHARED_DATASETS_PROVENANCE.md)  
> 📜 [**Văn Kiện Kiểm Định Phân Vùng 9 Mô Hình vs Báo Cáo**](file:///d:/Work/Do-an/workspaces/truongnv/reports/INSPECTION_REPLICATIONS_VS_REPORT_MODELS_DISCREPANCY.md)  
> 📂 [**Phân Vùng Nghiên Cứu Tham Khảo `references_study/`**](file:///d:/Work/Do-an/workspaces/truongnv/references_study/README.md)

---

## 🏛️ QUY CHUẨN KIẾN TRÚC MỖI MÔ HÌNH (THE 6-KEY ARCHITECTURE)

Mỗi thư mục mô hình thực nghiệm bên dưới đều được chuẩn hóa theo cấu trúc cô lập tuyệt đối gồm 5 thành phần bắt buộc:
```text
<model_directory>/
├── papers/       # [Key 1] Tệp PDF bài báo khoa học chuẩn đối chiếu từ y văn
├── upstream/     # [Key 4] Mã nguồn gốc của tác giả (100% nguyên bản, read-only, không pycache/log)
├── datasets/     # [Key 3] Tập dữ liệu kiểm thử tải riêng + DATASET_PROVENANCE.md đối soát SHA-256
├── reports/      # [Key 5 & 6] Kết quả JSON đo đạc thật + PROVENANCE.json + URL_AND_PROVENANCE_REPORT.md
└── README.md     # Hướng dẫn chi tiết cách chạy và đặc tả kỹ thuật mô hình
```

---

## 📌 BẢNG TỔNG HỢP 9 MÔ HÌNH THỰC NGHIỆM ĐỘC LẬP TẠI `replications/`

### Nhóm 1: 6 Baseline Đối Chuẩn Trực Diện Trong Báo Cáo Đồ Án (Slide 4 / Table 2.3)
| STT | Tên Mô Hình & Thư Mục | Trường Phái Kỹ Thuật | 📄 Paper PDF | 🏛️ Repo Gốc (Pristine) | 📦 Dataset Tải Riêng | 📑 Báo Cáo & Kết Quả |
| :-: | :--- | :---: | :---: | :---: | :---: | :---: |
| **M1** | **Heuristic Keyword Regex**<br>*(Được tích hợp qua harness)* | $F_1$ (Rule-based) | N/A (Standard) | [`src/models/`](file:///d:/Work/Do-an/workspaces/truongnv/src/models/) | [`reports/tasks_for_meeting_6/data/`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_6/data/) | [Bảng 2.3](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_6/01_executive_summary/README.md) |
| **M2** | **Dual TF-IDF (Jain NeurIPS 2023)**<br>[`Tier1_Candidate_Jain_NeurIPS2023/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_Jain_NeurIPS2023/) | $F_2$ (Classical ML) | [PDF](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_Jain_NeurIPS2023/papers/Jain_2023_Baseline_Defenses_Adversarial_Attacks_LLMs.pdf) | [`upstream/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_Jain_NeurIPS2023/upstream/) | [`datasets/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_Jain_NeurIPS2023/datasets/) | [`reports/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_Jain_NeurIPS2023/reports/) |
| **M3** | **ProtectAI DeBERTa-v3 v2**<br>[`ProtectAI_DeBERTa_v3_v2/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/ProtectAI_DeBERTa_v3_v2/) | $F_3$ (Transformer 2-class) | [PDF](file:///d:/Work/Do-an/workspaces/truongnv/replications/ProtectAI_DeBERTa_v3_v2/papers/He_2023_DeBERTaV3_Disentangled_Attention_ICLR.pdf) | [`upstream/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/ProtectAI_DeBERTa_v3_v2/upstream/) | [`datasets/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/ProtectAI_DeBERTa_v3_v2/datasets/) | [`reports/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/ProtectAI_DeBERTa_v3_v2/reports/) |
| **M4** | **Meta Prompt-Guard 86M (2024)**<br>[`Tier1_Candidate_Meta_PromptGuard2024/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_Meta_PromptGuard2024/) | $F_3$ (Transformer 3-class) | [PDF](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_Meta_PromptGuard2024/papers/Meta_2024_Prompt_Guard_86M_Input_Guardrail.pdf) | [`upstream/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_Meta_PromptGuard2024/upstream/) | [`datasets/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_Meta_PromptGuard2024/datasets/) | [`reports/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_Meta_PromptGuard2024/reports/) |
| **M5** | **InstructDetector (EMNLP 2024)**<br>[`Tier1_Candidate_InstructDetector_EMNLP2024/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_InstructDetector_EMNLP2024/) | $F_4$ (Gradient Probing) | [PDF](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_InstructDetector_EMNLP2024/papers/Zhao_2024_InstructDetector_Instruction_Tuned_Attack_EMNLP.pdf) | [`upstream/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_InstructDetector_EMNLP2024/upstream/) | [`datasets/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_InstructDetector_EMNLP2024/datasets/) | [`reports/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_InstructDetector_EMNLP2024/reports/) |
| **M6** | **DataSentinel (IEEE S&P 2025)**<br>[`DataSentinel_Liu_SP2025/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/DataSentinel_Liu_SP2025/) | $F_5$ (Game-Theory) | [PDF](file:///d:/Work/Do-an/workspaces/truongnv/replications/DataSentinel_Liu_SP2025/papers/Liu_2025_DataSentinel_Game_Theoretic_Detection_Prompt_Injection.pdf) | [`upstream/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/DataSentinel_Liu_SP2025/upstream/) | [`datasets/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/DataSentinel_Liu_SP2025/datasets/) | [`reports/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/DataSentinel_Liu_SP2025/reports/) |

---

### Nhóm 2: Các Mô Hình Thực Nghiệm Chuyên Sâu Khác Tại `replications/`
| STT | Tên Mô Hình & Thư Mục | Vai Trò Học Thuật & Thực Nghiệm | 📄 Paper PDF | 🏛️ Repo Gốc (Pristine) | 📦 Dataset Tải Riêng | 📑 Báo Cáo & Kết Quả |
| :-: | :--- | :--- | :---: | :---: | :---: | :---: |
| **M7** | **PIGuard (Hao Li et al. ACL 2025)**<br>[`Paper_ACL2025_PIGuard_HaoLi/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Paper_ACL2025_PIGuard_HaoLi/) | **Foundation Reference** (Kế thừa MOF Loss; trang bị runner độc lập) | [PDF](file:///d:/Work/Do-an/workspaces/truongnv/replications/Paper_ACL2025_PIGuard_HaoLi/papers/PIGuard_2025_Prompt_Injection_Guardrail_ACL.pdf) | [`upstream/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Paper_ACL2025_PIGuard_HaoLi/upstream/) | [`datasets/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Paper_ACL2025_PIGuard_HaoLi/datasets/) | [`reports/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Paper_ACL2025_PIGuard_HaoLi/reports/) |
| **M8** | **SmoothLLM (Robey NeurIPS 2023)**<br>[`SmoothLLM_Robey_NeurIPS2023/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/SmoothLLM_Robey_NeurIPS2023/) | Randomized Smoothing (Khảo sát độ trễ đa truy vấn) | [PDF](file:///d:/Work/Do-an/workspaces/truongnv/replications/SmoothLLM_Robey_NeurIPS2023/papers/Robey_2023_SmoothLLM_Defending_LLMs_Random_Perturbation.pdf) | [`upstream/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/SmoothLLM_Robey_NeurIPS2023/upstream/) | [`datasets/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/SmoothLLM_Robey_NeurIPS2023/datasets/) | [`reports/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/SmoothLLM_Robey_NeurIPS2023/reports/) |
| **M10** | **ModernBERT (Answer.AI 2024)**<br>[`ModernBERT_Warner_2024/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/ModernBERT_Warner_2024/) | Long-Context 8k (Prompt Overflow Baseline) | [PDF](file:///d:/Work/Do-an/workspaces/truongnv/replications/ModernBERT_Warner_2024/papers/Warner_2024_ModernBERT_Brings_Modern_Transformers_To_Encoders.pdf) | [`upstream/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/ModernBERT_Warner_2024/upstream/) | [`datasets/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/ModernBERT_Warner_2024/datasets/) | [`reports/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/ModernBERT_Warner_2024/reports/) |
| - | **PromptShield (Jacob et al. CCS 2024)**<br>[`PromptShield_Jacob_CCS2024/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/PromptShield_Jacob_CCS2024/) | In-Context Guardrail (Mô hình doanh nghiệp UC Berkeley) | [PDF](file:///d:/Work/Do-an/workspaces/truongnv/replications/PromptShield_Jacob_CCS2024/papers/Jacob_2024_PromptShield_In_Context_Defense_CCS.pdf) | [`upstream/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/PromptShield_Jacob_CCS2024/upstream/) | [`datasets/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/PromptShield_Jacob_CCS2024/datasets/) | [`reports/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/PromptShield_Jacob_CCS2024/reports/) |

---

### Phân Vùng Nghiên Cứu Tham Khảo (Đã Di Chuyển Sang `workspaces/truongnv/references_study/`)
Để bảo đảm thư mục `replications/` thuần túy là kho mô hình thực nghiệm đối chuẩn, 2 tài nguyên phục vụ nghiên cứu tham khảo đã được chuyển sang phân vùng độc lập:
1. [`references_study/harnesses/JailbreakBench_Chao_NeurIPS2024/`](file:///d:/Work/Do-an/workspaces/truongnv/references_study/harnesses/JailbreakBench_Chao_NeurIPS2024/): Bộ khung sinh tấn công & nguồn trích xuất dataset D3.
2. [`references_study/rejected_baselines/Tier1_REJECTED_Ayub_CAMLIS2024/`](file:///d:/Work/Do-an/workspaces/truongnv/references_study/rejected_baselines/Tier1_REJECTED_Ayub_CAMLIS2024/): Bằng chứng phủ định (Negative Baseline Dossier) do FPR quá cao ($58.41\%$).

---

## ⚡ HƯỚNG DẪN KHỞI CHẠY THỰC NGHIỆM & KIỂM ĐỊNH

### 1. Kiểm tra toàn vẹn xuất xứ & SHA-256 tự động (< 1s):
```powershell
python workspaces/truongnv/scripts/check_replication_origin_urls.py --mode fast
```

### 2. Kiểm định tính có thật và phân vùng 9 mô hình thực nghiệm vs 2 tài nguyên tham khảo:
```powershell
python workspaces/truongnv/scripts/audit_6_vs_11_models_integrity.py
```

### 3. Chạy kiểm tra tổng thể mã nguồn và ranh giới theo chuẩn đề tài:
```powershell
python Final-Report/scripts/validate_local.py --mode fast
```
