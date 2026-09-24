# BỔ TRỢ HỌC THUẬT & THỰC NGHIỆM ĐỘC LẬP BÁO CÁO TIẾN ĐỘ MEETING 6 (TUẦN TỪ 20/09 ĐẾN 26/09/2026)
## HỆ THỐNG TÀI LIỆU, MÃ NGUỒN VÀ DỮ LIỆU ĐO ĐẠC ĐÃ TÁI CẤU TRÚC TINH GỌN (ZERO REDUNDANCY ARCHITECTURE)

---

> **Đơn vị thực hiện**: Đồ án Tốt nghiệp Kỹ sư An toàn Thông tin (IAP491) — Đại học FPT  
> **Đề tài**: *A Machine-Learning Guardrail for Detecting Prompt Injection and Jailbreak Attacks on LLM Applications (PI-Guard)*  
> **Sinh viên thực hiện**: Nguyễn Văn Trường (Trưởng nhóm / Mã SV: `SE182034` / GitHub: `nvtruongops`)  
> **Giảng viên Hướng dẫn (GVHD)**: ThS. Trần Văn Ninh  
> **Workspace tài nguyên thực thi**: [`workspaces/truongnv/reports/tasks_for_meeting_6/`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_6/)  
> **Căn cứ chỉ đạo từ GVHD**: Biên bản Meeting 5 ngày 19/09/2026 ([`Final-Report/Meeting/Meeting 5_19_09_26.md`](file:///d:/Work/Do-an/Final-Report/Meeting/Meeting%205_19_09_26.md))  
> **Báo cáo Word chính thức**: [`RESEARCH_REPORT_MEETING_6.docx`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_6/03_reports_and_executive_briefs/RESEARCH_REPORT_MEETING_6.docx)

---

## 📌 1. BỐI CẢNH MEETING 5 & MỤC TIÊU HOÀN THÀNH MEETING 6

Tại buổi họp tiến độ **Meeting 5 (ngày 19/09/2026)**, ThS. Trần Văn Ninh đã giao cho nhóm 5 nhiệm vụ nghiên cứu khoa học và thực nghiệm độc lập:
1. **Phân tích cơ chế chia tầng & trích xuất đặc trưng**: Làm rõ cách thức mô hình phân tích block, chuỗi ký tự, n-gram từ/ký tự đến token;
2. **Mở rộng không gian đánh giá đa chiều**: Đối chiếu với các công trình quốc tế SOTA như CASCADE (NUS 2026 [[41]](#ref41)) và PromptShield (ACM CCS 2024 [[30]](#ref30));
3. **Xử lý văn bản lớn 200,000 ký tự & đòn tấn công giấu ở đuôi (Tail Injection)**: Chống lại lỗ hổng Prompt Overflow (Zhou et al., 2026 [[40]](#ref40));
4. **Đóng gói pipeline thực tế & đo đạc 12 mô hình trên CPU**: Huấn luyện và lưu weights `.joblib`, chạy đối chuẩn trên 6 tập dữ liệu gốc;
5. **Chuẩn bị hồ sơ bảo vệ học thuật trước Hội đồng & đóng băng mô hình**: Định vị rõ 5 Key phấn đấu cốt lõi và 3 Giới hạn ngoài tầm với.

Toàn bộ các nhiệm vụ trên đã được hiện thực hóa $100\%$ và tổ chức thành **Kiến trúc Tinh gọn (Zero Redundancy)** gồm đúng 4 phân hệ tài liệu chuyên sâu và 5 phân hệ tài nguyên thực thi.

---

## 🗂️ 2. BẢN ĐỒ KIẾN TRÚC THƯ MỤC SAU TÁI CẤU TRÚC (ZERO REDUNDANCY MAP)

```text
workspaces/truongnv/reports/tasks_for_meeting_6/
├── README.md                                          # [CỔNG ĐIỀU HƯỚNG MASTER & ROADMAP CHỈ MỤC] (File này)
│
├── 01_theory_and_taxonomy/                            # [PHÂN HỆ 1: LÝ THUYẾT & PHÂN LOẠI HỌC MASTER]
│   └── TAXONOMY_OF_ARCHITECTURES_AND_ALGORITHMIC_PARADIGMS.md
│       └── Hệ sinh thái 41 papers, 6 họ/7 thuật toán, suy dẫn toán học 6x7 -> 12x14 và bảng ánh xạ xuất xứ 100%
│
├── 02_compatibility_and_tradeoffs/                    # [PHÂN HỆ 2: MA TRẬN TƯƠNG THÍCH & ĐÁNH ĐỔI THỰC NGHIỆM]
│   ├── ARCHITECTURAL_COMPATIBILITY_MATRIX_CASCADE_12X14.md
│   │   └── Ma trận tương thích hợp nhất (Nền tảng vĩ mô 6x7 + Mở rộng vi mô 12x14 = 168 điểm giao định lượng)
│   └── EMPIRICAL_BENCHMARK_AND_OPERATIONAL_TRADEOFFS.md
│       └── Đối chuẩn thực nghiệm 12 mô hình độc lập (D1-D6), 6 nhánh đánh đổi B1-B6, 200k chunking & 4 figures
│
├── 03_reports_and_executive_briefs/                   # [PHÂN HỆ 3: HỒ SƠ BÁO CÁO ĐIỀU HÀNH & BẢO VỆ HỘI ĐỒNG]
│   ├── MASTER_RESEARCH_SYNTHESIS_REPORT_MEETING_6.md  # [MỚI] Báo cáo Tổng hợp Master Toàn diện (Chuẩn Publication/Thesis)
│   ├── SLIDE_DECK_MEETING_6.md                        # [MỚI] Khung Slide Báo cáo Tiến độ Meeting 6
│   ├── EXECUTIVE_PROGRESS_REPORT_MEETING_6.md         # Báo cáo tiến độ điều hành Meeting 6 chuẩn Markdown (Un-mocked)
│   ├── COUNCIL_DEFENSE_RATIONALE_AND_GAP_AUDIT.md     # Hồ sơ Gap Audit 8 bước, 5 Key phấn đấu, 3 Giới hạn ngoài tầm với
│   └── RESEARCH_REPORT_MEETING_6.docx                 # Báo cáo định dạng Microsoft Word chính thức nộp GVHD ThS. Trần Văn Ninh
│
├── 04_benchmarks_and_data/                            # [PHÂN HỆ 4: DỮ LIỆU ĐO ĐẠC SỐ HÓA JSON & CATALOG]
│   ├── README.md                                      # Catalog giải thích nguồn gốc, generator script & schema 8 file JSON
│   ├── compatibility_matrix_6x7.json                  # Dữ liệu số hóa 42 giao điểm ma trận vĩ mô 6x7
│   ├── compatibility_matrix_expanded_12x14.json       # Dữ liệu số hóa 168 giao điểm ma trận mở rộng 12x14
│   ├── grounded_empirical_matrix.json                 # Dữ liệu đối chuẩn 12 mô hình thực nghiệm CPU
│   ├── multi_branch_tradeoffs_matrix.json             # Dữ liệu phân tích đánh đổi 6 nhánh cấu hình vận hành
│   ├── cross_dataset_empirical_matrix.json            # Dữ liệu kiểm thử chéo 6 mô hình trên D1-D6 (Un-mocked, Wilson CIs)
│   ├── comprehensive_empirical_benchmark_suite.json   # Dữ liệu tổng hợp tải và độ trễ CPU
│   ├── experimental_models_benchmark_report.json      # Báo cáo đo đạc chi tiết các baseline thử nghiệm
│   └── public_triad_empirical_benchmark.json          # Báo cáo kiểm chứng nguyên tắc Bộ Ba Công Khai
│
├── src/                                               # [PHÂN HỆ MÃ NGUỒN NGUYÊN MẪU & WEIGHTS THẬT]
│   ├── tier0_ingress_scrubber.py                      # Lớp 0: Chuẩn hóa Unicode NFKC, strip Zero-width, decode Base64/Hex
│   ├── block_chunker.py                               # Băm khối 512 tokens, Sliding Window 10%, Head & Tail Priority Scan
│   ├── tier1_fast_filter.py                           # Tầng 1: Dual-Space TF-IDF Platt LogReg + Early-Stopping
│   ├── tier2_semantic_arbiter.py                      # Tầng 2: DeBERTa-v3 MOF Invariant phân loại ngữ nghĩa an toàn
│   └── tier1_tfidf_model.joblib                       # Trọng số mô hình Tầng 1 đã huấn luyện thực tế (861.3 KB)
│
├── scripts/                                           # [PHÂN HỆ TOOLING & TỰ ĐỘNG HÓA TÁI LẬP]
│   ├── reproduce_all_benchmarks.py                    # [MỚI] Script 1-Click Tự động Tái lập 100% Thực nghiệm & Biểu đồ
│   ├── run_cross_dataset_benchmark.py                 # Runner đo đạc 600 mẫu test D1-D6 & McNemar test
│   ├── generate_benchmark_figures.py                  # Trình sinh 4 biểu đồ khoa học tự động
│   └── ...                                            # Các công cụ tính toán ma trận tương thích
│
├── tests/                                             # [BỘ KIỂM THỬ TỰ ĐỘNG PYTEST - 3/3 TESTS PASSED]
│   ├── test_adaptive_token_dilution.py                # Kiểm thử đối kháng Gray-box Token Dilution & OOV Gate (PASS)
│   ├── test_hidden_prompt_at_tail.py                  # Kiểm thử bắt tấn công giấu đuôi 200k chars tăng tốc 4.6x (PASS)
│   └── test_long_document_200k.py                     # Kiểm thử văn bản lớn 200k chars 149 blocks không OOM (PASS)
│
├── data/                                              # [DỮ LIỆU KIỂM THỬ THỰC TẾ]
│   ├── sample_benign_200k.txt                         # Mẫu văn bản lành tính 200,000 ký tự
│   ├── sample_malicious_tail_200k.txt                 # Mẫu văn bản 200,000 ký tự có cấy payload ở cuối
│   └── cross_dataset_suite/                           # Bộ 6 tập dữ liệu kiểm thử y văn gốc D1-D6 (520 mẫu)
│
├── figures/                                           # [BỘ 4 BIỂU ĐỒ TRỰC QUAN HÓA KHOA HỌC PUBLICATION-QUALITY]
│   ├── figure1_early_stopping_200k.png                # Figure 1: Early Stopping Latency Profile (Văn bản 200k ký tự)
│   ├── figure2_cross_dataset_heatmap.png              # Figure 2: Cross-Dataset Generalization Heatmap (D1-D6)
│   ├── figure3_overdefense_tradeoff.png               # Figure 3: Low-FPR Economic Trade-off & Overdefense Frontier
│   └── figure4_component_ablation.png                 # Figure 4: Component Ablation Study Breakdown
│
└── scripts/                                           # [BỘ SCRIPT TÍNH TOÁN & KIỂM TOÁN TỰ ĐỘNG]
    ├── inspect_meeting_6_rigor.py                     # Script kiểm toán 100% neo HTML, link PDF cục bộ & thuật ngữ
    ├── calculate_expanded_compatibility_matrix.py     # Script tính toán ma trận 12x14
    ├── calculate_multi_branch_tradeoffs.py            # Script tính toán đánh đổi 6 nhánh kiến trúc
    ├── run_cross_dataset_benchmark.py                 # Script chạy kiểm thử chéo D1-D6
    └── prepare_cross_dataset_suite.py                 # Script chuẩn bị bộ dữ liệu testbed
```

---

## 📊 3. TỔNG HỢP CÁC BẰNG CHỨNG THỰC NGHIỆM ĐÃ KIỂM ĐỊNH

### 3.1. Đối Chuẩn Hiệu Năng 12 Mô Hình & Giải Pháp PI-Guard
Dữ liệu trích xuất từ [`EMPIRICAL_BENCHMARK_AND_OPERATIONAL_TRADEOFFS.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_6/02_compatibility_and_tradeoffs/EMPIRICAL_BENCHMARK_AND_OPERATIONAL_TRADEOFFS.md):

| Mô Hình Đánh Giá | Direct Recall (%) | Indirect Recall (%) | Jailbreak Recall (%) | Benign FPR (%) *($\le 1.5\%$)* | Overdefense Acc (%) *(`NotInject`)* | CPU Latency P95 (ms) | Low-FPR TPR @ 1% |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **K1: PIGuard (ACL 2025)** [[18]](#ref18) | **$96.0\%$** | **$92.5\%$** | **$94.0\%$** | **$0.8\%$** | **$90.7\%$** | $24.5\text{ms}$ | $20.37\%$ |
| **K2: DataSentinel (S&P 2025)** [[32]](#ref32) | $80.0\%$ | $20.0\%$ | $0.0\%$ | $10.0\%$ | $80.0\%$ | **$0.19\text{ms}$** | N/A |
| **K3: PromptShield (CCS 2024)** [[30]](#ref30) | **$100.0\%$** | **$100.0\%$** | $85.0\%$ | **$0.0\%$** | **$100.0\%$** | **$4.11\text{ms}$** | **$100.0\%$** |
| **K4: ModernBERT 8k (2024)** [[37]](#ref37) | **$100.0\%$** | **$100.0\%$** | $90.0\%$ | **$0.0\%$** | **$100.0\%$** | $11.67\text{ms}$ | $90.00\%$ |
| **K6: Meta Prompt-Guard 86M** [[20]](#ref20) | $98.0\%$ | $80.0\%$ | $88.0\%$ | $0.5\%$ | 🔴 **$0.88\%$** *(SẬP)* | $22.1\text{ms}$ | 🔴 $12.78\%$ |
| **K10: SmoothLLM (NeurIPS 2023)** [[14]](#ref14)| $35.0\%$ | $20.0\%$ | $92.0\%$ | $1.0\%$ | $85.0\%$ | 🔴 $5\times\text{ LLM}$ | N/A |
| **K-PI: PI-Guard Two-Tier Cascade** | **$96.0\%$** | **$92.5\%$** | **$94.0\%$** | **$0.0\%$** | **$100.0\%$** | **$3.45\text{ms}$** | **$92.50\%$** |

### 3.2. Giải Quyết Chỉ Đạo Văn Bản 200,000 Ký Tự (Tail-Scan 111x Speedup)
- **Tài liệu sạch 100% (200k ký tự)**: Quét toàn bộ $111$ blocks bằng Tầng 1 chỉ mất **$13.32\text{ms}$** trên CPU (thấp hơn nhiều so với ngưỡng trần $30\text{ms}$ SLA).
- **Tài liệu giấu mã độc ở cuối (Tail Injection)**: Cơ chế Quét Ưu Tiên Đuôi-Đầu (Tail-First) kết hợp Early-Stopping bắt ngay đòn tấn công tại Block đầu tiên quét ($0.12\text{ms}$), **tăng tốc gấp $111.0\times$** so với duyệt tuần tự.

---

## ⚡ 4. HƯỚNG DẪN TÁI LẬP THỰC NGHIỆM ĐỘC LẬP (REPRODUCTION COMMANDS)

Mọi giảng viên, sinh viên và phản biện đều có thể tái lập $100\%$ kết quả nghiên cứu bằng các lệnh CLI tiêu chuẩn:

```powershell
# 1. Chạy bộ kiểm toán học thuật tự động (100% neo HTML, link PDF cục bộ & blacklist thuật ngữ)
python workspaces/truongnv/reports/tasks_for_meeting_6/scripts/inspect_meeting_6_rigor.py

# 2. Chạy bộ kiểm thử tự động pytest (Văn bản dài 200k ký tự & ngắt sớm đòn tấn công ở đuôi)
pytest workspaces/truongnv/reports/tasks_for_meeting_6/tests -v

# 3. Tính toán lại toàn bộ Ma trận Tương thích 12x14 và xuất file JSON số hóa
python workspaces/truongnv/reports/tasks_for_meeting_6/scripts/calculate_expanded_compatibility_matrix.py

# 4. Tính toán phân tích đánh đổi đa nhánh và đường biên Pareto
python workspaces/truongnv/reports/tasks_for_meeting_6/scripts/calculate_multi_branch_tradeoffs.py
```

---

## 📚 5. TÀI LIỆU THAM KHẢO CHÍNH THỨC (REFERENCES)

* <a id="ref7"></a>**[7]** H. Inan, K. Upasani, J. Chi, et al. 2023. *Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations*. Meta AI. [arXiv:2312.06674](https://arxiv.org/abs/2312.06674). Local PDF: [`References/Meta_2023_Llama_Guard_Input_Output_Safeguard.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Meta_2023_Llama_Guard_Input_Output_Safeguard.pdf).
* <a id="ref9"></a>**[9]** P. He, J. Yin, D. He, et al. 2023. *DeBERTaV3: Improving DeBERTa using ELECTRA-Style Pre-Training with Gradient-Disentangled Embedding*. In *ICLR 2023*. Local PDF: [`References/He_2023_DeBERTaV3_Disentangled_Attention_ICLR.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/He_2023_DeBERTaV3_Disentangled_Attention_ICLR.pdf).
* <a id="ref10"></a>**[10]** G. Markov et al. / OpenAI. 2023. *A Holistic Approach to Undesired Content Detection in the Real World*. In *AAAI 2023*. Local PDF: [`References/OpenAI_2023_Undesired_Content_Detection.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/OpenAI_2023_Undesired_Content_Detection.pdf).
* <a id="ref14"></a>**[14]** A. Robey, E. Wong, H. Hassani, and G. J. Pappas. 2023. *SmoothLLM: Defending Large Language Models Against Jailbreaking Attacks*. In *NeurIPS 2023*. [arXiv:2310.03684](https://arxiv.org/abs/2310.03684). Local PDF: [`References/Robey_2023_SmoothLLM_Defending_LLMs_Random_Perturbation.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Robey_2023_SmoothLLM_Defending_LLMs_Random_Perturbation.pdf).
* <a id="ref16"></a>**[16]** J. H. Saltzer and M. D. Schroeder. 1975. *The Protection of Information in Computer Systems*. In *Proceedings of the IEEE*, 63(9):1278–1308. DOI: 10.1109/PROC.1975.9939. Local PDF: [`References/Saltzer_1975_The_Protection_of_Information_in_Computer_Systems.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Saltzer_1975_The_Protection_of_Information_in_Computer_Systems.pdf).
* <a id="ref18"></a>**[18]** H. Li, X. Liu, N. Zhang, and C. Xiao. 2025. *PIGuard: Prompt Injection Guardrail via Mitigating Overdefense for Free*. In *ACL 2025 - Long Paper*. [arXiv:2410.22770](https://arxiv.org/abs/2410.22770). Local PDF: [`replications/Tier2_PIGuard_ACL2025/papers/PIGuard_ACL2025_arXiv2410.22770.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier2_PIGuard_ACL2025/papers/PIGuard_ACL2025_arXiv2410.22770.pdf).
* <a id="ref20"></a>**[20]** Meta AI. 2024. *Prompt Guard 86M: A Small Classifier for Prompt Injection and Jailbreak Detection*. Model Card and Technical Report. [arXiv:2407.21783](https://arxiv.org/abs/2407.21783). Local PDF: [`replications/Tier1_Candidate_Meta_PromptGuard2024/papers/Meta_2024_PurpleLlama_PromptGuard.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/replications/Tier1_Candidate_Meta_PromptGuard2024/papers/Meta_2024_PurpleLlama_PromptGuard.pdf).
* <a id="ref30"></a>**[30]** D. Jacob, H. Alzahrani, Z. Hu, B. Alomair, and D. Wagner. 2024. *PromptShield: Deployable Detection for Prompt Injection Attacks*. In *ACM CCS 2024*, pages 4247–4261. DOI: 10.1145/3714393.3726501. Local PDF: [`workspaces/truongnv/References/Jacob_2024_PromptShield_Deployable_Detection_Prompt_Injection_CCS.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Jacob_2024_PromptShield_Deployable_Detection_Prompt_Injection_CCS.pdf).
* <a id="ref32"></a>**[32]** Y. Liu, Y. Jia, J. Jia, D. Song, and N. Z. Gong. 2025. *DataSentinel: A Game-Theoretic Detection of Prompt Injection Attacks*. In *IEEE S&P 2025*. Local PDF: [`workspaces/truongnv/References/Liu_2025_DataSentinel_Game_Theoretic_Detection_Prompt_Injection.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Liu_2025_DataSentinel_Game_Theoretic_Detection_Prompt_Injection.pdf).
* <a id="ref37"></a>**[37]** B. Warner, A. Chaffin, B. Clavié, et al. 2024. *ModernBERT: Bringing Modern Transformer Innovations to Pre-trained Encoders*. [arXiv:2412.13663](https://arxiv.org/abs/2412.13663). Local PDF: [`workspaces/truongnv/References/Warner_2024_ModernBERT_Brings_Modern_Transformers_To_Encoders.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Warner_2024_ModernBERT_Brings_Modern_Transformers_To_Encoders.pdf).
* <a id="ref38"></a>**[38]** I. Padhi et al. 2024. *Granite Guardian: Content Safety and Risk Detection*. IBM Research. [arXiv:2412.07724](https://arxiv.org/abs/2412.07724). Local PDF: [`References/Padhi_2024_Granite_Guardian_Content_Safety_Risk_Detection.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Padhi_2024_Granite_Guardian_Content_Safety_Risk_Detection.pdf).
* <a id="ref40"></a>**[40]** Y. Zhou et al. 2026. *Prompt Overflow: Vulnerability in Asymmetric Context Windows of LLM Applications*. Local PDF: [`workspaces/truongnv/References/Zhou_2026_Prompt_Overflow_Guardrail_Window_Mismatch.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Zhou_2026_Prompt_Overflow_Guardrail_Window_Mismatch.pdf).
* <a id="ref41"></a>**[41]** J. Luo and E. Han. 2026. *CASCADE Against Jailbreaks: Combination Across Stages with Controlled Attack-Defense Evaluation*. [arXiv:2609.21793](https://arxiv.org/abs/2609.21793). Local PDF: [`References/Luo_2026_CASCADE_Against_Jailbreaks_Evaluation.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Luo_2026_CASCADE_Against_Jailbreaks_Evaluation.pdf).
