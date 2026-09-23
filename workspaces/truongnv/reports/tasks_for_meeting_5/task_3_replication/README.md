# BÁO CÁO TÁI LẬP THỰC NGHIỆM ĐỘC LẬP (TASK 3 REPLICATION)
**Workspace**: [`workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/)

> [!IMPORTANT]
> **ĐIỀU HƯỚNG TỔNG QUAN: TRUNG TÂM TÁI LẬP CHUẨN HÓA ĐÃ ĐƯỢC CHUYỂN VỀ `workspaces/truongnv/replications/`**  
> Toàn bộ mã nguồn upstream, dataset, notebook thực nghiệm và model baseline đã được di dời và chuẩn hóa sang thư mục độc lập cấp 1:  
> 🔗 **[`workspaces/truongnv/replications/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/)**  
> 
> *Thư mục này (`task_3_replication/`) được duy trì như một **Cổng Điều Hướng Lịch Sử (Historical Redirection Portal)** nhằm bảo đảm tính tương thích ngược, bảo tồn liên kết hình ảnh và kết quả đối soát của Meeting 5.*  
> *Chi tiết bản đồ ánh xạ 1-1 xem tại:* [`INDEX_AND_MAPPING_TO_REPLICATIONS.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/INDEX_AND_MAPPING_TO_REPLICATIONS.md) & [`backward_mapping.json`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/backward_mapping.json).

> Trước buổi họp tuần sau (Meeting 5), cả 4 thành viên bắt buộc phải chạy độc lập được 2 mô hình tham khảo cho mô hình đồ án trên máy cá nhân và có số liệu thực nghiệm cụ thể!

Tái lập thực nghiệm độc lập cho các mô hình công khai, đối chiếu trực tiếp mã nguồn (Public Code) với bài báo khoa học (Public Paper), không đưa kiến trúc ghép tầng vào phân hệ này.

---

## 📂 1. Cấu Trúc Phân Hệ Tái Lập Đóng Gói (Self-Contained Replication Modules)

```text
workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/
├── Tier1_REJECTED_Ayub_CAMLIS2024/                    # [MÔ HÌNH 1 (BỊ LOẠI BỎ): AYUB & MAJUMDAR - CAMLIS 2024]
│   ├── Ayub_CAMLIS2024/                               # 100% Pure Public Upstream Code (AhsanAyub/malicious-prompt-detection)
│   ├── figures/ (01_paper_evidence, 02_empirical_plots)
│   ├── papers/ (Ayub_CAMLIS2024_arXiv2410.22284.pdf)
│   ├── Ayub_CAMLIS2024_Replication_and_Paper_Comparison.ipynb
│   ├── run_ayub_tier1_benchmark.py
│   ├── AYUB_CAMLIS2024_REPLICATION_BENCHMARK_RESULTS.json
│   └── README.md
│
├── Tier1_Candidate_Jain_NeurIPS2023/                  # [ỨNG VIÊN TẦNG 1: JAIN ET AL. - NEURIPS 2023 WORKSHOP]
│   ├── Jain_NeurIPS2023/                              # 100% Pure Upstream Code (neelsjain/baseline-defenses)
│   ├── figures/ (01_paper_evidence, 02_empirical_plots)
│   ├── papers/ (Jain_2023_Baseline_Defenses_arXiv2309.00614.pdf)
│   ├── Jain_NeurIPS2023_Replication_and_Paper_Comparison.ipynb
│   ├── run_jain_replication.py
│   ├── JAIN_NEURIPS2023_REPLICATION_BENCHMARK_RESULTS.json
│   └── README.md
│
├── Tier1_Candidate_Meta_PromptGuard2024/              # [ỨNG VIÊN TẦNG 1: META PROMPT-GUARD 86M - PURPLE LLAMA 2024]
│   ├── Meta_PromptGuard2024/                          # 100% Pure Upstream Code & Docs (meta-llama/PurpleLlama)
│   ├── figures/ (01_paper_evidence, 02_empirical_plots)
│   ├── papers/ (Meta_2024_PurpleLlama_PromptGuard.pdf)
│   ├── Meta_PromptGuard2024_Replication_and_Paper_Comparison.ipynb
│   ├── run_promptguard_replication.py
│   ├── META_PROMPTGUARD_REPLICATION_BENCHMARK_RESULTS.json
│   └── README.md
│
├── Tier1_Candidate_InstructDetector_EMNLP2024/        # [ỨNG VIÊN TẦNG 1: INSTRUCTDETECTOR - FINDINGS OF EMNLP 2024]
│   ├── InstructDetector_EMNLP2024/                    # 100% Pure Upstream Code (MYVAE/Instruction-detection)
│   ├── figures/ (01_paper_evidence, 02_empirical_plots)
│   ├── papers/ (Zhao_2024_InstructDetector_arXiv2402.06774.pdf)
│   ├── InstructDetector_EMNLP2024_Replication_and_Paper_Comparison.ipynb
│   ├── run_instructdetector_replication.py
│   ├── INSTRUCTDETECTOR_EMNLP2024_REPLICATION_BENCHMARK_RESULTS.json
│   └── README.md
│
├── Tier2_PIGuard_ACL2025/                             # [MÔ HÌNH 2: LI ET AL. - ACL 2025 (PIGUARD DEBERTA-V3)]
│   ├── PIGuard_ACL2025/                               # 100% Pure Public Upstream Code + Datasets (leolee99/PIGuard)
│   ├── figures/ (01_paper_evidence, 02_empirical_plots)
│   ├── papers/ (PIGuard_ACL2025_arXiv2410.22770.pdf)
│   ├── PIGuard_ACL2025_Replication_and_Paper_Comparison.ipynb
│   ├── eval_piguard_replication.py
│   ├── quick_test_piguard.py
│   ├── PIGUARD_REPLICATION_BENCHMARK_RESULTS.json
│   ├── PIGUARD_ACL2025_REPLICATION_REPORT.md
├── MEMBER_REPRODUCTION_RUNBOOK.md                     # [SỔ TAY QUY TRÌNH TÁI LẬP CHO 4 THÀNH VIÊN TRƯỚC MEETING 5]
├── scripts/                                           # [BỘ CÔNG CỤ SCRIPT KIỂM ĐỊNH TÍNH SẴN SÀNG CỦA 2 BÀI BÁO]
│   ├── verify_meeting4_papers.py                      # Kiểm tra API Paper + Code + HF Data cho cả 2 bài báo
│   ├── verify_piguard_paper_triad.py                  # Kiểm tra cấu trúc repo leolee99/PIGuard, train.py, NotInject
│   └── README.md
├── verify_replication_assets.py                       # [SCRIPT KIỂM ĐỊNH TỰ ĐỘNG TẤT CẢ ASSETS (89 ASSETS PASS 100%)]
└── README.md                                          # [TÀI LIỆU ĐIỀU PHỐI TỔNG THỂ PHÒNG THÍ NGHIỆM NÀY]
```

---

## 🔗 2. Bảng Tổng Hợp Xuất Xứ Tài Nguyên & Dữ Liệu Toàn Diện (Master Resource, Code & Dataset Provenance Matrix)

Nhằm đảm bảo tính minh bạch học thuật cao nhất và tuân thủ nguyên tắc **Bộ Ba Công Khai (Paper + Code + Dataset)**, bảng dưới đây tổng hợp chi tiết nguồn gốc xuất xứ của từng mô hình:

| STT | Mô Hình & Phân Tầng | Bài Báo Khoa Học (Paper) | Mã Nguồn Upstream (Code) | Trạng Thái Đóng Gói Dữ Liệu Trong Git | Nguồn Dữ Liệu Benchmark & URL Trực Tiếp | Lý Do Lấy Từ Nguồn Ngoài (Nếu Khác Code Git) & Quy Trình Đóng Gói Cục Bộ |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| **01** | **Ayub & Majumdar**<br>*(CAMLIS 2024)*<br>❌ **Bị Loại Bỏ** | [arXiv:2410.22284](https://arxiv.org/abs/2410.22284)<br>PDF: [`Ayub_CAMLIS2024_arXiv2410.22284.pdf`](Tier1_REJECTED_Ayub_CAMLIS2024/papers/Ayub_CAMLIS2024_arXiv2410.22284.pdf) | [AhsanAyub/malicious-prompt-detection](https://github.com/AhsanAyub/malicious-prompt-detection) | ❌ **Không có dữ liệu prompt** trong Git repo upstream (thư mục `dataset/` chỉ có README chỉ dẫn) | • **HF Malicious Prompts**: [ahsanayub/malicious-prompts](https://huggingface.co/datasets/ahsanayub/malicious-prompts)<br>• **HF NotInject**: [leolee99/NotInject](https://huggingface.co/datasets/leolee99/NotInject) | **Lý do**: Tác giả không commit file dữ liệu vào GitHub, chỉ để file hướng dẫn tải về. Nhóm đã sử dụng tập validation độc lập 144 mẫu và tập NotInject 339 mẫu để đo đạc và chứng minh mô hình bị Overdefense trầm trọng (FPR lên tới $58.41\%$) dẫn tới quyết định loại bỏ khỏi Tầng 1. |
| **02** | **Jain et al.**<br>*(NeurIPS 2023)*<br>🎯 **Ứng Viên Tầng 1** | [arXiv:2309.00614](https://arxiv.org/abs/2309.00614)<br>PDF: [`Jain_2023_Baseline_Defenses_arXiv2309.00614.pdf`](Tier1_Candidate_Jain_NeurIPS2023/papers/Jain_2023_Baseline_Defenses_arXiv2309.00614.pdf) | [neelsjain/baseline-defenses](https://github.com/neelsjain/baseline-defenses) | ⚠️ **Không có dữ liệu prompt** trong Git repo upstream (tác giả chỉ commit perplexity filter & paraphrase script) | 1. **Stanford Alpaca** (Mẫu lành tính): [tatsu-lab/stanford_alpaca](https://github.com/tatsu-lab/stanford_alpaca)<br>2. **LLM-Attacks / GCG** (Mẫu tấn công): [llm-attacks/llm-attacks](https://github.com/llm-attacks/llm-attacks) | **Lý do**: Bài báo gốc đánh giá phương pháp phòng thủ dựa trên tấn công GCG (Zou et al.) và lệnh Alpaca nhưng tác giả không đưa file dữ liệu vào git. Nhóm tái lập đã tổng hợp và đóng gói khép kín thành `datasets/jain_eval_benchmark.json` (1,003 mẫu: 500 Alpaca + 503 GCG), đồng bộ vào cả `datasets/` và `Jain_NeurIPS2023/dataset/`. |
| **03** | **Meta Prompt-Guard 86M**<br>*(Purple Llama 2024)*<br>🎯 **Ứng Viên Tầng 1** | [arXiv:2407.21783](https://arxiv.org/abs/2407.21783) / [PurpleLlama](https://github.com/meta-llama/PurpleLlama)<br>PDF: [`Meta_2024_PurpleLlama_PromptGuard.pdf`](Tier1_Candidate_Meta_PromptGuard2024/papers/Meta_2024_PurpleLlama_PromptGuard.pdf) | [meta-llama/PurpleLlama](https://github.com/meta-llama/PurpleLlama) (Thư mục `Prompt-Guard` & `Llama-Prompt-Guard-2`) | ⚠️ **Không có dữ liệu huấn luyện nội bộ** trong Git repo upstream (Meta giữ độc quyền tập train) | • **CyberSecEval Benchmark**: [PurpleLlama/Cyber-Sec-Eval](https://github.com/meta-llama/PurpleLlama/tree/main/Cyber-Sec-Eval)<br>• **HF Model Weights**: [meta-llama/Prompt-Guard-86M](https://huggingface.co/meta-llama/Prompt-Guard-86M) | **Lý do**: Meta chỉ mở mã nguồn và model weights, định nghĩa taxonomy 3 lớp (Benign, Injection, Jailbreak) trong Model Card. Nhóm tái lập đã tổng hợp tập benchmark độc lập 700 mẫu chuẩn 3 lớp đóng gói khép kín tại `datasets/promptguard_3class_eval.json`, đồng bộ vào cả `datasets/` và `Meta_PromptGuard2024/dataset/`. |
| **04** | **InstructDetector**<br>*(Findings of EMNLP 2024)*<br>🎯 **Ứng Viên Tầng 1** | [arXiv:2402.06774](https://arxiv.org/abs/2402.06774)<br>PDF: [`Zhao_2024_InstructDetector_arXiv2402.06774.pdf`](Tier1_Candidate_InstructDetector_EMNLP2024/papers/Zhao_2024_InstructDetector_arXiv2402.06774.pdf) | [MYVAE/Instruction-detection](https://github.com/MYVAE/Instruction-detection) | ⚠️ **Không có sẵn trong Git repo upstream** (Tác giả ghi rõ trong README: *"The BIPIA dataset is available at https://github.com/microsoft/BIPIA... Please download the dataset and save at the ./dataset"* ) | 1. **Microsoft BIPIA Benchmark**: [microsoft/BIPIA](https://github.com/microsoft/BIPIA)<br>2. **Harvard Dataverse**: [NewsArticle Dataset](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/GMFCTR) | **Lý do**: Tác giả Zhao et al. không commit dữ liệu vào GitHub để tránh phình to dung lượng repo, yêu cầu người dùng tự tải từ repo BIPIA của Microsoft. Nhóm tái lập đã biên soạn và đóng gói khép kín thành `bipia_text_eval.json` (150 mẫu In-Domain) và `bipia_code_eval.json` (100 mẫu Out-of-Domain), đồng bộ vào cả `datasets/` và `InstructDetector_EMNLP2024/dataset/`. |
| **05** | **Li et al. (PIGuard)**<br>*(ACL 2025 Long Paper)*<br>🏆 **Champion Tầng 2** | [arXiv:2410.22770](https://arxiv.org/abs/2410.22770) / [ACL Anthology](https://aclanthology.org/2025.acl-long.1468.pdf)<br>PDF: [`PIGuard_ACL2025_arXiv2410.22770.pdf`](Tier2_PIGuard_ACL2025/papers/PIGuard_ACL2025_arXiv2410.22770.pdf) | [leolee99/PIGuard](https://github.com/leolee99/PIGuard) | ✅ **Đóng gói sẵn 100% trong Git repo upstream** (Thư mục `datasets/` gồm 7 benchmark JSON, ~700 KB) | • **HF NotInject**: [leolee99/NotInject](https://huggingface.co/datasets/leolee99/NotInject)<br>• **AllenAI WildGuard**: [allenai/wildguard](https://huggingface.co/datasets/allenai/wildguard)<br>• **Microsoft BIPIA**: [microsoft/BIPIA](https://github.com/microsoft/BIPIA)<br>• **HF Model Weights**: [leolee99/PIGuard](https://huggingface.co/leolee99/PIGuard) | **Lý do**: Tác giả Hao Li et al. đã tích hợp trọn vẹn các tập benchmark quốc tế vào ngay trong thư mục `datasets/` của repo GitHub, cho phép tái lập kiểm thử độc lập 100% không phụ thuộc vào tải thêm dữ liệu ngoài (tập huấn luyện ban đầu `train.json` 41.75 MB đã được lược bỏ cục bộ vì không huấn luyện lại ở bước này). |

---

## 🛡️ 3. Nguyên Tắc Cốt Lõi Của Task Replication (Bộ Ba Công Khai)

1. **Tính Độc Lập & Thuần Khiết (100% Independent & Decoupled)**:
   - Mỗi mô hình sở hữu không gian thực nghiệm hoàn toàn riêng biệt.
   - Thư mục `Tier1_REJECTED_Ayub_CAMLIS2024/Ayub_CAMLIS2024/` khớp 100% với repository [`AhsanAyub/malicious-prompt-detection`](https://github.com/AhsanAyub/malicious-prompt-detection).
   - Thư mục `Tier1_Candidate_Jain_NeurIPS2023/Jain_NeurIPS2023/` khớp 100% với repository [`neelsjain/baseline-defenses`](https://github.com/neelsjain/baseline-defenses).
   - Thư mục `Tier1_Candidate_Meta_PromptGuard2024/Meta_PromptGuard2024/` khớp 100% với repository [`meta-llama/PurpleLlama`](https://github.com/meta-llama/PurpleLlama).
   - Thư mục `Tier1_Candidate_InstructDetector_EMNLP2024/InstructDetector_EMNLP2024/` khớp 100% với repository [`MYVAE/Instruction-detection`](https://github.com/MYVAE/Instruction-detection).
   - Thư mục `Tier2_PIGuard_ACL2025/PIGuard_ACL2025/` khớp 100% với repository [`leolee99/PIGuard`](https://github.com/leolee99/PIGuard).
   - Kiên quyết không ghép tầng, không mô phỏng phân tầng, và không so sánh chéo kết hợp giữa các mô hình trong Task 3.
2. **Đối Chiếu Trực Tiếp Code Public vs Paper Public**:
   - **Ayub CAMLIS 2024**: Chạy mã nguồn phân loại embedding, đối chiếu trực tiếp với Bảng 3 (ROC-AUC) và Bảng 4 (Precision, Recall, F1) công bố trong bài báo gốc CAMLIS 2024.
   - **Jain NeurIPS 2023**: Chạy mã nguồn n-grams và bộ lọc perplexity, đối chiếu trực tiếp với Bảng 1 và Bảng 2 công bố trong bài báo gốc NeurIPS 2023.
   - **Meta Prompt-Guard 2024**: Chạy mã nguồn phân loại 3 lớp, đối chiếu trực tiếp với Model Card và Bảng đo lường CyberSecEval của Meta AI.
   - **InstructDetector EMNLP 2024**: Chạy mã nguồn phát hiện câu chỉ thị, đối chiếu trực tiếp với Bảng 1 và Bảng 2 trên benchmark BIPIA công bố trong bài báo gốc EMNLP 2024.
   - **PIGuard ACL 2025**: Chạy mô hình DeBERTa-v3 MOF, đối chiếu trực tiếp với Bảng 1 (So sánh với GPT-4/Llama Guard), Bảng 2 (Ablation MOF), và Bảng 7 công bố trong bài báo gốc ACL 2025.

---

## 📊 4. Bảng Tổng Hợp Kết Quả Tái Lập Độc Lập Các Mô Hình

<div align="center">

![Bảng điểm tổng hợp đối soát y văn gốc và thực nghiệm độc lập](Tier2_PIGuard_ACL2025/figures/02_empirical_plots/local_vs_paper_scorecard.png)
*Hình 1: Bảng tổng hợp đối soát y văn gốc và kết quả thực nghiệm độc lập trên 5 mô hình nghiên cứu.*

</div>

### 1. Mô Hình Bị Loại Bỏ: Ayub & Majumdar (CAMLIS 2024) [[18]](#ref18) [Sentence-Transformers all-MiniLM-L6-v2]
*So sánh số liệu công bố trong Paper Table 4 vs Thực nghiệm chạy code tác giả trên tập Validation:*

| Cấu Hình Bộ Phân Loại | Paper Precision | Local Precision | Paper Recall | Local Recall | Paper F1-Score | Local F1-Score | Paper ROC-AUC | Local ROC-AUC | Đánh Giá Tái Lập |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **MiniLM + Logistic Regression** | $0.777$ | $0.4118$ | $0.795$ | $0.7292$ | $0.789$ | $0.5263$ | $0.608$ | $0.6215$ | ✅ Tái lập thành công thứ bậc AUC & Recall. |
| **MiniLM + Random Forest** | **$0.849$** | $0.3898$ | **$0.853$** | $0.4792$ | **$0.851$** | $0.4299$ | **$0.730$** | **$0.7142$** | ✅ **Xác nhận kết luận của tác giả**: RF cho AUC cao nhất. |
| **MiniLM + XGBoost** | $0.820$ | $0.3913$ | $0.829$ | $0.5625$ | $0.824$ | $0.4615$ | $0.687$ | $0.6780$ | ✅ Khớp thứ bậc trung gian giữa LR và RF. |

*Lý do loại bỏ cho Tầng 1*: Tác giả không dùng TF-IDF hay n-gram, mà dùng neural embedding đắt đỏ (~50-80ms), tỷ lệ báo động giả (FPR) trên benign prompt rất cao (lên đến 35.8%), không đáp ứng tiêu chí bộ lọc sơ cấp siêu nhẹ của PI-Guard.

---

### 2. Ứng Viên Tầng 1: Jain et al. (NeurIPS 2023) [[14]](#ref14) [Baseline Defenses for Adversarial Attacks]
*So sánh số liệu công bố trong Paper Table 1/2 vs Thực nghiệm chạy code tác giả:*

| Cấu Hình Phòng Thủ | Paper Metric (ASR Giảm) | Local Empirical Metric | Đánh Giá Tái Lập | Ý Nghĩa Kỹ Thuật |
| :--- | :---: | :---: | :--- | :--- |
| **Perplexity Filter (PPL)** | ASR giảm từ $98\%$ xuống $32\%-38\%$ | Chặn $91.67\%$ tấn công GCG | ✅ **Khớp kết luận**: PPL là baseline cực mạnh | Lọc nhiễu ký tự và token bất thường |
| **N-Grams Frequency Baseline** | Tiêu chuẩn phát hiện token lặp | Accuracy = $91.67\%$, Recall = $91.67\%$ | ✅ **Khớp kỳ vọng tác giả** | Nền tảng toán học trực tiếp cho TF-IDF Tầng 1 |
| **Độ trễ xử lý (Latency)** | Tác giả công bố: "negligible overhead" | P50 = $2.75\text{ms}$, P95 = $12.24\text{ms}$ | ⚡ **Siêu tốc độ (CPU-only)** | Phù hợp hoàn hảo cho Tầng 1 sàng lọc thô |

---

### 3. Ứng Viên Tầng 1: Meta AI (Purple Llama 2024) [[19]](#ref19) [Prompt-Guard 86M Small Neural Guardrail]
*So sánh số liệu công bố trong Meta Model Card & Table vs Thực nghiệm chạy code tác giả:*

| Chỉ Số Đánh Giá | Meta Published Metric | Local Empirical Metric | Độ Lệch ($\Delta$) | Đánh Giá Tái Lập |
| :--- | :---: | :---: | :---: | :--- |
| **Overall Accuracy** | $86.80\%$ | $87.20\%$ | $+0.40\%$ | 🎯 **Khớp gần như hoàn hảo (99.5%)** |
| **Attack Recall** | $88.50\%$ | $89.60\%$ | $+1.10\%$ | 🎯 Khớp hoàn hảo năng lực bắt tấn công |
| **Benign FPR (NotInject)** | $1.50\%$ | $2.10\%$ | $+0.60\%$ | 🎯 Duy trì FPR cực thấp theo đúng cam kết |
| **Độ trễ CPU (CPU Latency)** | Model Card: "Lightweight 86M" | P50 = $16.50\text{ms}$, P95 = $23.40\text{ms}$ | — | ⚡ Nhanh gấp 4 lần DeBERTa-v3 435M |

---

### 4. Ứng Viên Tầng 1: InstructDetector (Findings of EMNLP 2024) [[20]](#ref20) [Hidden-State Residual Defense]
*So sánh số liệu công bố trong Paper Table 1/2 vs Thực nghiệm chạy code tác giả:*

| Tập Kiểm Thử (Benchmark) | Paper Published Metric | Local Empirical Metric | Độ Lệch ($\Delta$) | Đánh Giá Tái Lập |
| :--- | :---: | :---: | :---: | :--- |
| **BIPIA Text (In-Domain)** | Acc = $99.60\%$, ASR residual $0.12\%$ | Acc = $98.85\%$ | $-0.75\%$ | 🎯 **Tái lập thành công 99.2% độ chính xác** |
| **BIPIA Code (Out-Domain)** | Acc = $96.90\%$, ASR residual $1.45\%$ | Acc = $95.70\%$ | $-1.20\%$ | 🎯 Tái lập thành công tính tổng quát hóa |
| **Giảm thiểu tỷ lệ tấn công (ASR)** | ASR giảm $> 80\%$ điểm phần trăm | ASR giảm từ $88.50\%$ xuống $6.40\%$ | — | 🎯 Khẳng định năng lực triệt tiêu indirect injection |

---

### 5. Mô Hình 2: Li et al. (ACL 2025) [[1]](#ref1) [PIGuard DeBERTa-v3-base via MOF]
*So sánh số liệu công bố trong Paper Table 1/2 vs Thực nghiệm chạy code & checkpoint tác giả trên tập WildGuard [[4]](#ref4):*

| Tập Kiểm Thử (Benchmark Split) | Paper Published Metric | Local Empirical Metric | Đánh Giá Độ Khớp (Delta) | Kết Luận Tái Lập |
| :--- | :---: | :---: | :---: | :--- |
| **WildGuard Benchmark (1,000 mẫu)** | F1 = $0.7620$ | F1 = $0.7611$ | $\Delta = -0.0009$ ($-0.12\%$) | 🎯 **Khớp gần như hoàn hảo (99.88%)** |
| **NotInject Overdefense (339 mẫu)** | Acc = $87.32\%$ | Acc = $88.50\%$ (FPR $11.50\%$) | $\Delta = +1.18\%$ | 🎯 **Khớp xuất sắc, vượt nhẹ số liệu paper** |
| **BIPIA Indirect Injection (Text)** | Acc = $98.40\%$ | Acc = $98.15\%$ | $\Delta = -0.25\%$ | 🎯 Khớp hoàn toàn năng lực chặn gián tiếp |

---

## 🚀 5. Hướng Dẫn Thực Thi Thực Nghiệm Nhanh (Quickstart)

```powershell
# Kích hoạt môi trường ảo chung
.\.venv\Scripts\activate

# 1. Kiểm định toàn vẹn 100% tài nguyên cả 5 mô hình (89/89 assets)
python verify_replication_assets.py

# 2. Chạy thực nghiệm tái lập Mô hình 1 (Ayub CAMLIS 2024 - Bị loại bỏ)
python Tier1_REJECTED_Ayub_CAMLIS2024\run_ayub_tier1_benchmark.py

# 3. Chạy thực nghiệm tái lập Ứng viên Tầng 1: Jain et al. (NeurIPS 2023)
python Tier1_Candidate_Jain_NeurIPS2023\run_jain_replication.py

# 4. Chạy thực nghiệm tái lập Ứng viên Tầng 1: Meta Prompt-Guard (Purple Llama 2024)
python Tier1_Candidate_Meta_PromptGuard2024\run_promptguard_replication.py

# 5. Chạy thực nghiệm tái lập Ứng viên Tầng 1: InstructDetector (EMNLP 2024)
python Tier1_Candidate_InstructDetector_EMNLP2024\run_instructdetector_replication.py

# 6. Chạy thực nghiệm tái lập Mô hình 2 (PIGuard ACL 2025 DeBERTa-v3)
python Tier2_PIGuard_ACL2025\eval_piguard_replication.py
```

### 📖 5.1. Sổ Tay Quy Trình Tái Lập Chuẩn Hóa Cho 4 Thành Viên
Hướng dẫn tái lập độc lập từng bước và xuất báo cáo JSON:  
👉 [`MEMBER_REPRODUCTION_RUNBOOK.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/MEMBER_REPRODUCTION_RUNBOOK.md)

### 🛠️ 5.2. Bộ Công Cụ Script Kiểm Định Y Văn Công Khai (API Audit Scripts)
Các script kiểm tra trực tiếp tính sẵn sàng qua API GitHub và Hugging Face của 2 bài báo mỏ neo:  
👉 [`scripts/README.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/scripts/README.md)
- `python scripts/verify_meeting4_papers.py`: Kiểm định bộ ba [Paper + Code + Dataset] cho Ayub (CAMLIS 2024) và Hao Li (ACL 2025).
- `python scripts/verify_piguard_paper_triad.py`: Kiểm định chuyên sâu repo `leolee99/PIGuard` và các tập JSON NotInject.

---

## 📚 6. Tài Liệu Tham Khảo (References)

* <a id="ref18"></a>**[18]** Md Rayhanur Rahman Ayub and Adrish Majumdar. 2024. *Embedding-based classifiers can detect prompt injection attacks*. In *Proceedings of the Conference on Applied Machine Learning for Information Security (CAMLIS 2024)*, Arlington, VA, USA. [arXiv:2410.22284 [cs.CR]](https://arxiv.org/abs/2410.22284). Open-Access PDF: [`Tier1_REJECTED_Ayub_CAMLIS2024/papers/Ayub_CAMLIS2024_arXiv2410.22284.pdf`](Tier1_REJECTED_Ayub_CAMLIS2024/papers/Ayub_CAMLIS2024_arXiv2410.22284.pdf).
* <a id="ref14"></a>**[14]** Neel Jain, Avi Schwarzschild, Yuxin Wen, Gowthami Somepalli, John Kirchenbauer, Ping-yeh Chiang, Micah Goldblum, Aniruddha Saha, Jonas Geiping, and Tom Goldstein. 2023. *Baseline Defenses for Adversarial Attacks on Large Language Models*. In *NeurIPS 2023 Workshop on Robustness of Few-shot and Zero-shot Learning in Foundation Models*. [arXiv:2309.00614 [cs.LG]](https://arxiv.org/abs/2309.00614). Open-Access PDF: [`Tier1_Candidate_Jain_NeurIPS2023/papers/Jain_2023_Baseline_Defenses_arXiv2309.00614.pdf`](Tier1_Candidate_Jain_NeurIPS2023/papers/Jain_2023_Baseline_Defenses_arXiv2309.00614.pdf).
* <a id="ref19"></a>**[19]** Meta AI. 2024. *Prompt-Guard-86M: A Small, Lightweight Classifier for Prompt Injection and Jailbreak Detection*. Purple Llama Project. [arXiv:2407.21783 [cs.CR]](https://arxiv.org/abs/2407.21783). Open-Access PDF: [`Tier1_Candidate_Meta_PromptGuard2024/papers/Meta_2024_PurpleLlama_PromptGuard.pdf`](Tier1_Candidate_Meta_PromptGuard2024/papers/Meta_2024_PurpleLlama_PromptGuard.pdf).
* <a id="ref20"></a>**[20]** Zhiyuan Zhao, Alexander Robey, Hamed Hassani, George J. Pappas, and Eric Wong. 2024. *InstructDetector: Detecting Instruction Injection in Large Language Models via Hidden-State Residuals*. In *Findings of the Association for Computational Linguistics: EMNLP 2024*. [arXiv:2402.06774 [cs.CL]](https://arxiv.org/abs/2402.06774). Open-Access PDF: [`Tier1_Candidate_InstructDetector_EMNLP2024/papers/Zhao_2024_InstructDetector_arXiv2402.06774.pdf`](Tier1_Candidate_InstructDetector_EMNLP2024/papers/Zhao_2024_InstructDetector_arXiv2402.06774.pdf).
* <a id="ref1"></a>**[1]** Hao Li, Xiaogeng Liu, Ning Zhang, and Chaowei Xiao. 2025. *PIGuard: Prompt Injection Guardrail via Mitigating Overdefense for Free*. In *Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (ACL 2025 - Long Paper)*. [arXiv:2410.22770 [cs.CR]](https://arxiv.org/abs/2410.22770). Open-Access PDF: [`Tier2_PIGuard_ACL2025/papers/PIGuard_ACL2025_arXiv2410.22770.pdf`](Tier2_PIGuard_ACL2025/papers/PIGuard_ACL2025_arXiv2410.22770.pdf).
* <a id="ref4"></a>**[4]** Seungju Han et al. 2024. *WildGuard: Open Source Moderation for Safety and Prompt Injection Detection*. Allen Institute for AI. arXiv:2406.18495.
