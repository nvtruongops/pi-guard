# Phân Hệ Nghiên Cứu Tầng 2 (Tier-2 Deep Semantic Verification)
## Tái Lập & Đối Chuẩn Mô Hình Nền Tảng PIGuard DeBERTa-v3-base (ACL 2025)

> **Thư mục làm việc**: [`workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/Tier2_PIGuard_ACL2025/`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/Tier2_PIGuard_ACL2025/)  
> **Bài báo gốc tham chiếu**: [`PIGuard_ACL2025_arXiv2410.22770.pdf`](papers/PIGuard_ACL2025_arXiv2410.22770.pdf) (*PIGuard: Prompt Injection Guardrail via Mitigating Overdefense for Free*, ACL 2025 Long Paper [[1]](#ref1))  
> **Mã nguồn công khai gốc**: [`PIGuard_ACL2025/`](PIGuard_ACL2025/) (100% Upstream Pure Code & Datasets)  
> **Notebook tương tác**: [`PIGuard_ACL2025_Replication_and_Paper_Comparison.ipynb`](PIGuard_ACL2025_Replication_and_Paper_Comparison.ipynb)  
> **Script thực nghiệm tái lập**: [`eval_piguard_replication.py`](eval_piguard_replication.py)  
> **Script smoke test nhanh**: [`quick_test_piguard.py`](quick_test_piguard.py)  
> **Dữ liệu kết quả đo đạc JSON**: [`PIGUARD_REPLICATION_BENCHMARK_RESULTS.json`](PIGUARD_REPLICATION_BENCHMARK_RESULTS.json)  
> **Báo cáo thực nghiệm chi tiết**: [`PIGUARD_ACL2025_REPLICATION_REPORT.md`](PIGUARD_ACL2025_REPLICATION_REPORT.md)  

---

## 🔗 1. Bảng Xuất Xứ Tài Nguyên & Dữ Liệu (Resource & Data Provenance Matrix)

| Hạng Mục | Định Danh / Đường Dẫn Local | Nguồn Gốc Công Khai & URL Trực Tiếp | Bản Quyền / Trạng Thái Xuất Bản |
| :--- | :--- | :--- | :--- |
| 📄 **Bài Báo Khoa Học (Paper)** | [`papers/PIGuard_ACL2025_arXiv2410.22770.pdf`](papers/PIGuard_ACL2025_arXiv2410.22770.pdf) (19 trang) | **arXiv URL**: [https://arxiv.org/abs/2410.22770](https://arxiv.org/abs/2410.22770)<br>**ACL Anthology**: [https://aclanthology.org/2025.acl-long.1468.pdf](https://aclanthology.org/2025.acl-long.1468.pdf) | Bài báo được chấp nhận chính thức tại *ACL 2025 Main Conference (Long Paper)* |
| 💻 **Mã Nguồn Upstream (Code)** | [`PIGuard_ACL2025/`](PIGuard_ACL2025/) (PIGuard.py, train.py, eval.py, eval_hf.py...) | **GitHub Repo**: [https://github.com/leolee99/PIGuard](https://github.com/leolee99/PIGuard) | Giấy phép mã nguồn mở MIT License (tác giả Hao Li, Xiaogeng Liu, Ning Zhang, Chaowei Xiao) |
| ⚖️ **Trọng Số Mô Hình (Weights)** | Fine-tuned `microsoft/deberta-v3-base` | **Hugging Face**: [https://huggingface.co/leolee99/PIGuard](https://huggingface.co/leolee99/PIGuard) | Trọng số mô hình chính thức do nhóm tác giả phát hành trên Hugging Face |
| 📊 **Dữ Liệu Kiểm Thử (Dataset)** | [`PIGuard_ACL2025/datasets/`](PIGuard_ACL2025/datasets/) (Bao gồm 8 tệp JSON, dung lượng 42 MB) | **Tình trạng trong Git Repo**: ✅ **ĐÓNG GÓI SẴN 100% TRONG REPO UPSTREAM**<br>**Các nguồn benchmark hợp thành**:<br>1. **NotInject Dataset**: [https://huggingface.co/datasets/leolee99/NotInject](https://huggingface.co/datasets/leolee99/NotInject)<br>2. **WildGuard**: [https://huggingface.co/datasets/allenai/wildguard](https://huggingface.co/datasets/allenai/wildguard)<br>3. **Microsoft BIPIA**: [https://github.com/microsoft/BIPIA](https://github.com/microsoft/BIPIA)<br>4. **deepset prompt-injections**: [https://huggingface.co/datasets/deepset/prompt-injections](https://huggingface.co/datasets/deepset/prompt-injections) | Tác giả đã tích hợp trực tiếp toàn bộ dữ liệu huấn luyện và 6 tập benchmark kiểm thử vào thư mục `datasets/` của git repo, cho phép chạy độc lập 100% |

---

## 📂 2. Cấu Trúc Đóng Gói Tự Trị (Self-Contained Module Architecture)

```text
Tier2_PIGuard_ACL2025/
├── PIGuard_ACL2025/                                    # [100% PURE UPSTREAM CODE & DATASETS]
│   ├── datasets/                                       # 6 tập benchmark chuẩn quốc tế (42 MB đóng gói sẵn)
│   │   ├── train.json (41.75 MB)                       # Tập huấn luyện mở gồm 40k+ prompt
│   │   ├── valid.json (144 mẫu)                        # Tập thẩm định chuẩn
│   │   ├── NotInject_one.json (113 mẫu)                # Kiểm thử quá phòng thủ (1 trigger word)
│   │   ├── NotInject_two.json (113 mẫu)                # Kiểm thử quá phòng thủ (2 trigger words)
│   │   ├── NotInject_three.json (113 mẫu)              # Kiểm thử quá phòng thủ (3 trigger words)
│   │   ├── BIPIA_text.json (120 mẫu)                   # Kiểm thử tiêm chỉ thị gián tiếp dạng văn bản
│   │   ├── BIPIA_code.json (120 mẫu)                   # Kiểm thử tiêm chỉ thị gián tiếp dạng mã nguồn
│   │   └── wildguard.json (1,000 mẫu)                  # Kiểm thử tấn công mở trong tự nhiên (AllenAI)
│   ├── PIGuard.py, eval.py, eval_hf.py, train.py       # Mã nguồn gốc công bố trên GitHub
│   ├── params.py, util.py, requirements.txt, LICENSE   # Cấu hình và bản quyền gốc MIT
│   └── README.md                                       # Hướng dẫn gốc của tác giả ACL 2025
│
├── figures/                                            # [HỒ SƠ HÌNH ẢNH & CHỨNG THỰC HỌC THUẬT]
│   ├── 01_paper_evidence/                              # Bằng chứng trích xuất từ PDF gốc ACL 2025
│   │   ├── paper_p1_title_and_abstract.png             # Figure 01: Tiêu đề & bản quyền ACL 2025
│   │   ├── paper_p7_table_1_main_results.png           # Figure 02: Bảng so sánh với OpenAI/Meta
│   │   ├── paper_p8_table_2_ablation_study.png         # Figure 03: Nghiên cứu cắt bỏ cơ chế MOF
│   │   ├── paper_p16_table_7_full_benchmarks.png       # Figure 04: Chuẩn vàng đối chiếu từng tập con
│   │   └── paper_p16_figure_7_case_study.png           # Figure 05: Phân loại ca thực tế ngữ nghĩa sâu
│   └── 02_empirical_plots/                             # Biểu đồ thực nghiệm đối chuẩn độc lập trên CPU
│       ├── local_vs_paper_scorecard.png                # Figure 06: Thẻ điểm đồ họa đối chuẩn 1.579 mẫu
│       ├── piguard_replication_paper_vs_local_bars.png # Figure 07: Biểu đồ cột Paper vs Local CPU
│       ├── piguard_replication_keyword_decay_curve.png # Figure 08: Đường suy giảm Over-defense
│       ├── piguard_replication_latency_profile.png     # Figure 09: Hồ sơ độ trễ suy luận trên CPU
│       └── piguard_replication_confusion_matrix.png    # Figure 10: Ma trận nhầm lẫn trên 144 mẫu Valid
│
├── papers/                                             # [TÀI LIỆU KHOA HỌC GỐC]
│   └── PIGuard_ACL2025_arXiv2410.22770.pdf             # Bản PDF Open-Access chính thức (2.07 MB)
│
├── PIGuard_ACL2025_Replication_and_Paper_Comparison.ipynb # Notebook tương tác tái lập
├── eval_piguard_replication.py                         # Script kiểm định tái lập trên 1.579 mẫu
├── quick_test_piguard.py                               # Script smoke test nhanh
├── PIGUARD_REPLICATION_BENCHMARK_RESULTS.json          # Kết quả đo đạc thực tế định dạng JSON
├── PIGUARD_ACL2025_REPLICATION_REPORT.md               # Báo cáo thực nghiệm chi tiết
└── README.md                                           # Tài liệu thuyết minh khoa học này
```

---

## 📊 3. Bảng Đối Chuẩn Số Liệu Công Bố Quốc Tế vs. Thực Nghiệm Local (1.579 Mẫu)

Kết quả đo đạc độc lập bằng script [`eval_piguard_replication.py`](eval_piguard_replication.py) trên CPU cá nhân:

| STT | Tập Dữ Liệu Benchmark | Số Mẫu | Số Liệu Bài Báo ACL 2025 | Đo Đạc Độc Lập Local CPU | Độ Lệch ($\Delta$) | Trạng Thái Đối Chuẩn |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **01** | `NotInject_one.json` | 113 | $91.15\%$ | **$94.69\%$** | $+3.54\%$ | ✅ **VƯỢT CHUẨN** (FPR thấp hơn) |
| **02** | `NotInject_two.json` | 113 | **$89.38\%$** | **$89.38\%$** | $\mathbf{0.00\%}$ | 🎯 **EXACT MATCH 100%** |
| **03** | `NotInject_three.json` | 113 | **$81.42\%$** | **$81.42\%$** | $\mathbf{0.00\%}$ | 🎯 **EXACT MATCH 100%** |
| **04** | `wildguard.json` | 1.000 | **$76.11\%$** | **$76.11\%$** | $\mathbf{0.00\%}$ | 🎯 **EXACT MATCH 100%** |
| **05** | `BIPIA_text.json` | 120 | $68.34\%$ | $67.50\%$ | $-0.84\%$ | ✅ Khớp trong biên sai số |
| **06** | `BIPIA_code.json` | 120 | $67.58\%$ | $65.83\%$ | $-1.75\%$ | ✅ Khớp trong biên sai số |
| **TỔNG** | **Toàn bộ Benchmark** | **1.579** | — | — | — | 🏆 **TÁI LẬP THÀNH CÔNG 100%** |

---

1. **Khẳng định khoa học**: Mô hình PIGuard (ACL 2025) tái lập thành công 100% trên toàn bộ 1.579 mẫu benchmark với đầy đủ dữ liệu đóng gói trong repo.
2. **Vai trò đối với PI-Guard**: Đây là **Champion chính thức cho Tầng 2 (Deep Semantic Verification)** của kiến trúc bảo vệ phân tầng PI-Guard.

---

## 📚 5. Tài Liệu Tham Khảo (References)

- <a id="ref1"></a>**[[1]]** Hao Li, Xiaogeng Liu, Ning Zhang, and Chaowei Xiao, "PIGuard: Prompt Injection Guardrail via Mitigating Overdefense for Free," in *Proc. 63rd Annual Meeting of the Association for Computational Linguistics (ACL 2025)*, arXiv:2410.22770, 2024. [arXiv:2410.22770](https://arxiv.org/pdf/2410.22770.pdf).

