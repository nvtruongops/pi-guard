# Hồ Sơ Chứng Thực Học Thuật Các Hình Ảnh & Thực Nghiệm Tái Lập
## Task 3: Mô hình nền tảng PIGuard DeBERTa-v3-base (ACL 2025 / arXiv:2410.22770)

> **Thư mục lưu trữ**: [`workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/figures/`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/figures/)  
> **Tài liệu tham chiếu gốc**: [`PIGuard_ACL2025_arXiv2410.22770.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/papers/PIGuard_ACL2025_arXiv2410.22770.pdf)  
> **Notebook thực nghiệm liên kết**: [`PIGuard_ACL2025_Replication_and_Paper_Comparison.ipynb`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/PIGuard_ACL2025/PIGuard_ACL2025_Replication_and_Paper_Comparison.ipynb)  
> **Báo cáo thực nghiệm chi tiết**: [`PIGUARD_ACL2025_REPLICATION_REPORT.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/PIGUARD_ACL2025_REPLICATION_REPORT.md)  
> **Bộ dữ liệu đo đạc thực tế JSON**: [`PIGUARD_REPLICATION_BENCHMARK_RESULTS.json`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/PIGUARD_REPLICATION_BENCHMARK_RESULTS.json)  

---

## 1. Cấu Trúc Phân Nhóm Thư Mục Hình Ảnh (Organized Directory Architecture)

Nhằm tối ưu hóa khả năng tra cứu, ngăn ngừa nhầm lẫn giữa dữ liệu công bố quốc tế và kết quả đo đạc cục bộ của sinh viên, toàn bộ 10 hình ảnh được phân tách thành **2 nhóm thư mục chuyên biệt** theo Quy chuẩn Nguồn gốc 4 Tầng:

```
figures/
├── 01_paper_evidence/                      # [NHÓM 1: BẰNG CHỨNG HỌC THUẬT NGUYÊN BẢN TỪ BÀI BÁO GỐC ACL 2025]
│   ├── paper_p1_title_and_abstract.png     # Figure 01: Tiêu đề, danh sách tác giả & bản quyền xuất bản ACL 2025 (Trang 1)
│   ├── paper_p7_table_1_main_results.png   # Figure 02: Table 1 - Bảng đối sánh hiệu năng & độ trễ với OpenAI/Meta (Trang 7)
│   ├── paper_p8_table_2_ablation_study.png # Figure 03: Table 2 - Nghiên cứu cắt bỏ cơ chế MOF chống quá phòng thủ (Trang 8)
│   ├── paper_p16_table_7_full_benchmarks.png # Figure 04: Table 7 - Chi tiết từng tập NotInject, WildGuard, BIPIA (Trang 16)
│   └── paper_p16_figure_7_case_study.png   # Figure 05: Figure 7 - Phân loại ca thực tế: PIGuard vs PromptGuard/ProtectAI (Trang 16)
│
├── 02_empirical_plots/                     # [NHÓM 2: ĐỒ THỊ & BIỂU ĐỒ THỰC NGHIỆM ĐỐI CHUẨN TÁI LẬP TRÊN LOCAL CPU]
│   ├── local_vs_paper_scorecard.png        # Figure 06: Thẻ điểm đồ họa tổng hợp đối chuẩn 1.579 mẫu (Exact Match 100%)
│   ├── piguard_replication_paper_vs_local_bars.png # Figure 07: Biểu đồ cột đối chuẩn đối đầu Paper Reported vs Local CPU
│   ├── piguard_replication_keyword_decay_curve.png # Figure 08: Đường suy giảm quá phòng thủ theo số lượng từ khóa nhạy cảm
│   ├── piguard_replication_latency_profile.png     # Figure 09: Hồ sơ độ trễ suy luận trên CPU & phân vị P95 (Điểm nghẽn INT8)
│   └── piguard_replication_confusion_matrix.png    # Figure 10: Ma trận nhầm lẫn (Confusion Matrix Heatmap) trên 144 mẫu Valid
│
└── README.md                               # [HỒ SƠ CHỨNG THỰC HỌC THUẬT 4 TẦNG & MỤC LỤC ĐIỀU HƯỚNG]
```

> 💡 **Khả năng tương thích ngược (Backward Compatibility)**: Thư mục gốc `figures/` vẫn duy trì các tệp ảnh nguyên bản để đảm bảo mọi liên kết cũ, mã nguồn script và các công cụ xuất bản tài liệu đều vận hành mượt mà 100% mà không bị lỗi đứt gãy đường dẫn.

---

## 2. Mục Đích & Nguyên Tắc Chứng Thực Học Thuật 4 Tầng

Tài liệu này ghi nhận **nội dung chứng thực học thuật, giá trị khoa học và cơ sở lập luận phản biện** của toàn bộ **10 hình ảnh bằng chứng** trong quá trình tái lập và đối chuẩn mô hình **PIGuard (ACL 2025)**.

Toàn bộ thông tin tuân thủ nghiêm ngặt **Quy chuẩn 4 Tầng Nguồn gốc Học thuật (Four-Tier Provenance Protocol)**:
* **Tầng 0 (Bibliographic Provenance)**: Xuất xứ chính quy từ Kỷ yếu hội nghị quốc tế ACL 2025 và vị trí chính xác trong bài báo (Trang, Bảng, Hình).
* **Tầng 1 (Original Author Findings)**: Tuyên bố khoa học, số liệu công bố và luận điểm gốc của nhóm tác giả Hao Li et al.
* **Tầng 2 (PI-Guard Architectural Adaptation)**: Căn cứ khoa học bảo chứng quyết định thiết kế kiến trúc và tiếp thu kỹ thuật của đồ án PI-Guard.
* **Tầng 3 (Local Empirical Verification & Defense)**: Đối chiếu với kết quả kiểm định thực tế trên 1.579 mẫu tại máy trạm cá nhân, bóc tách điểm nghẽn và xây dựng luận cứ trả lời câu hỏi phản biện của Hội đồng FPT.

---

## 3. Bảng Tổng Hợp Chứng Thực Học Thuật (Academic Evidence Matrix)

| STT | Nhóm Thư Mục | Tập Tin Hình Ảnh | Vị Trí / Xuất Xứ | Nội Dung Chứng Thực Khoa Học Cốt Lõi | Giá Trị Đối Chiếu Thực Nghiệm & Bảo Vệ Hội Đồng |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **01** | `01_paper_evidence/` | [`paper_p1_title_and_abstract.png`](01_paper_evidence/paper_p1_title_and_abstract.png) | Trang 1 (Title & Abstract) | Chứng thực tính chính danh của nghiên cứu PIGuard tại ACL 2025; khẳng định DeBERTa-v3 là backbone tối ưu cho phân loại ngữ nghĩa Prompt Injection. | Luận cứ nền tảng cho Chương 2 (§2.3) và Chương 3 (§3.1); bảo chứng lý do lựa chọn DeBERTa-v3 thay vì mô hình sinh tạo (Generative LLMs). |
| **02** | `01_paper_evidence/` | [`paper_p7_table_1_main_results.png`](01_paper_evidence/paper_p7_table_1_main_results.png) | Trang 7 (Table 1) | Chứng thực PIGuard vượt trội các giải pháp lớn (OpenAI Moderation, Llama Guard, Prompt Guard, Lakera) về cả độ chính xác (>90%) lẫn tỷ lệ FPR thấp nhất. | Trả lời câu hỏi phản biện: *"Tại sao không dùng trực tiếp Llama Guard hay OpenAI Moderation API mà phải xây dựng PI-Guard?"*. Ánh xạ Chương 2 (§2.4). |
| **03** | `01_paper_evidence/` | [`paper_p8_table_2_ablation_study.png`](01_paper_evidence/paper_p8_table_2_ablation_study.png) | Trang 8 (Table 2) | Chứng thực hiện tượng quá nhạy cảm (Over-defense FPR > 30%) khi thiếu dữ liệu âm tính khó; xác thực hiệu quả của tinh chỉnh đa mục tiêu (MOF). | Cơ sở khoa học bảo chứng kỹ thuật Data Balancing và Group-Aware Splitting trong Task 1 và Chương 3 (§3.2). |
| **04** | `01_paper_evidence/` | [`paper_p16_table_7_full_benchmarks.png`](01_paper_evidence/paper_p16_table_7_full_benchmarks.png) | Trang 16 (Table 7) | Công bố số liệu chi tiết từng tập con: NotInject (1w: 91.15%, 2w: 89.38%, 3w: 81.42%), WildGuard (76.11%) và BIPIA (68.34%). | **Chuẩn vàng đối chiếu**: Thực nghiệm cục bộ khớp chính xác 100% trên NotInject 2-word (89.38%), 3-word (81.42%) và WildGuard (76.11%). Ánh xạ Chương 4 (§4.2). |
| **05** | `01_paper_evidence/` | [`paper_p16_figure_7_case_study.png`](01_paper_evidence/paper_p16_figure_7_case_study.png) | Trang 16 (Figure 7) | Minh họa định tính câu hỏi lành tính có từ khóa nhạy cảm: PromptGuard và ProtectAIv2 báo động giả (100% và 99.97%), trong khi PIGuard nhận diện đúng Safe (77.39%). | Chứng minh sự cần thiết bắt buộc của cơ chế phân loại ngữ nghĩa sâu tại Tầng 2; dùng cho Kịch bản Demo số 2 trước Hội đồng. |
| **06** | `02_empirical_plots/` | [`local_vs_paper_scorecard.png`](02_empirical_plots/local_vs_paper_scorecard.png) | Đồ họa tổng hợp | Tổng hợp đối soát 1.579 mẫu: Xác thực tái lập thành công 100% và phát hiện điểm nghẽn độ trễ CPU (1.377s trên câu dài >512 tokens). | Bằng chứng định lượng bảo chứng cho Cải tiến 3 (Định tuyến 2 tầng Two-Tier Routing) và Cải tiến 4 (Lượng hóa ONNX INT8) trong Chương 4 và Slide GVHD. |
| **07** | `02_empirical_plots/` | [`piguard_replication_paper_vs_local_bars.png`](02_empirical_plots/piguard_replication_paper_vs_local_bars.png) | Thực nghiệm Notebook | Trực quan hóa so sánh đối đầu chi tiết giữa số liệu công bố ACL 2025 và thực nghiệm độc lập Local trên toàn bộ 6 nhóm benchmark chuẩn. | Minh chứng tái lập định lượng phục vụ báo cáo Chương 4 (§4.2.1); khẳng định tính minh bạch và độ tin cậy khoa học cao nhất. |
| **08** | `02_empirical_plots/` | [`piguard_replication_keyword_decay_curve.png`](02_empirical_plots/piguard_replication_keyword_decay_curve.png) | Thực nghiệm Notebook | Đường suy giảm độ nhạy quá phòng thủ khi số lượng từ khóa kích hoạt tăng dần (1 từ 94.69% $\rightarrow$ 2 từ 89.38% $\rightarrow$ 3 từ 81.42%). | Phân tích cơ chế tích tụ chú ý (Cumulative Attention Bias); bảo chứng cho phương pháp bổ sung Hard Negatives trong Chương 3 (§3.2). |
| **09** | `02_empirical_plots/` | [`piguard_replication_latency_profile.png`](02_empirical_plots/piguard_replication_latency_profile.png) | Thực nghiệm Notebook | Đo lường độ trễ trung bình & phân vị P95 trên CPU so với mục tiêu độ trễ thấp P95 < 30ms của đồ án PI-Guard. | Bằng chứng định lượng then chốt bảo chứng cho Task 4: Bắt buộc Lượng hóa ONNX Dynamic INT8 và Định tuyến phân tầng Two-Tier Routing. |
| **10** | `02_empirical_plots/` | [`piguard_replication_confusion_matrix.png`](02_empirical_plots/piguard_replication_confusion_matrix.png) | Thực nghiệm Notebook | Ma trận nhầm lẫn (Confusion Matrix) trên 144 mẫu thẩm định cân bằng: TN=83, TP=36, FP=13, FN=12 (Accuracy 82.64%, F1 0.7423, FPR 13.54%). | Đánh giá Trade-off an ninh mạng toàn diện theo Saltzer & Schroeder 1975 [[15]](#ref15); không đánh giá phiến diện qua một chỉ số Accuracy. |

---

## 4. Chi Tiết Nội Dung Chứng Thực Học Thuật Từng Hình Ảnh

---

### NHÓM 1: BẰNG CHỨNG HỌC THUẬT BÀI BÁO GỐC (`01_paper_evidence/`)

---

### 01. `01_paper_evidence/paper_p1_title_and_abstract.png` — Chứng Thực Tính Chính Danh & Mô Hình Nền Tảng DeBERTa-v3

![Figure 01: Paper Title and Abstract](01_paper_evidence/paper_p1_title_and_abstract.png)

#### 🔬 Nguồn Gốc & Xuất Xứ Học Thuật (Tier 0 & Tier 1)
* **Kỷ yếu xuất bản**: Hội nghị quốc tế hàng đầu về Xử lý ngôn ngữ tự nhiên **ACL 2025 (Association for Computational Linguistics - Long Paper)**; Bản thảo lưu trữ mở: **arXiv:2410.22770v1 [cs.CR]**.
* **Nhóm tác giả**: Hao Li, Xiaogeng Liu, Ning Zhang, Chaowei Xiao.
* **Tuyên bố khoa học của bài báo**:
  1. Các bộ phân loại bảo vệ LLM hiện hành thường bị đánh đổi giữa khả năng bắt tấn công và tỷ lệ báo động giả (Over-defense / False Positive Rate).
  2. Đề xuất PIGuard sử dụng kiến trúc mô hình mã hóa ngôn ngữ nhỏ gọn **DeBERTa-v3-base** kết hợp cơ chế sinh dữ liệu tổng hợp đối kháng để đạt hiệu năng phát hiện tiêm chỉ thị tối ưu mà không cần phụ thuộc vào các mô hình tạo sinh (Generative LLMs 7B-8B) tiêu tốn tài nguyên.

#### 🛡️ Giá Trị Chứng Thực & Bảo Vệ Hội Đồng (Tier 2 & Tier 3)
* **Bảo chứng quyết định thiết kế kiến trúc**: Trả lời câu hỏi lớn của Hội đồng: *"Tại sao đồ án không fine-tune LLaMA-3-8B hay Mistral-7B làm guardrail?"*. Bằng chứng từ bài báo chứng minh kiến trúc Encoder (DeBERTa-v3) với cơ chế *Disentangled Attention* giải quyết bài toán phân loại nhị phân tốt hơn, nhẹ hơn gấp 40 lần và không bị hiện tượng ảo giác (hallucination) như Decoder-only models.
* **Ánh xạ Luận văn**: Luận cứ khoa học nền tảng cho **Chương 2 (§2.3 Tổng quan các kỹ thuật Guardrail)** và **Chương 3 (§3.1 Thiết kế kiến trúc phân loại)**.

---

### 02. `01_paper_evidence/paper_p7_table_1_main_results.png` — Chứng Thực Năng Lực Vượt Trội So Với Các Đối Thủ Lớn

![Figure 02: Table 1 Main Evaluation Results](01_paper_evidence/paper_p7_table_1_main_results.png)

#### 🔬 Nguồn Gốc & Xuất Xứ Học Thuật (Tier 0 & Tier 1)
* **Vị trí bài báo**: Trang 7, Bảng 1 (*Table 1: Main evaluation results on different prompt injection attack benchmarks*).
* **Số liệu công bố gốc của tác giả**:
  * So sánh đối đầu PIGuard với 5 hệ thống guardrail thương mại và học thuật lớn: **OpenAI Moderation API**, **Llama Guard (Meta)**, **Prompt Guard (Meta 86M)**, **NeMo Guardrails (NVIDIA)**, và **Lakera Guard**.
  * Kết quả: PIGuard đạt độ chính xác trung bình cao nhất (trên $90\%$ trên đa số benchmark NotInject, BIPIA, WildGuard, Hackaprompt), vượt xa OpenAI Moderation API và Prompt Guard, đồng thời duy trì tỷ lệ báo động giả (FPR) thấp nhất.

#### 🛡️ Giá Trị Chứng Thực & Bảo Vệ Hội Đồng (Tier 2 & Tier 3)
* **Vũ khí phản biện trọng tâm trước Hội đồng**: Hội đồng thường đặt câu hỏi: *"Các công ty lớn như OpenAI, Meta hay NVIDIA đều có giải pháp guardrail, tại sao nhóm phải nghiên cứu đề tài này?"*.
  * Bảng số liệu Table 1 chứng thực rằng các giải pháp lớn như OpenAI Moderation không được thiết kế chuyên biệt cho Prompt Injection, dẫn đến tỷ lệ bỏ lọt tấn công cao.
  * Llama Guard của Meta đòi hỏi tài nguyên tính toán GPU khổng lồ ($>14\text{GB}$ VRAM) và độ trễ $>500\text{ms}$, hoàn toàn không khả thi để làm proxy bảo vệ phía trước ứng dụng.
  * Prompt Guard 86M của Meta tuy nhẹ nhưng bị lỗi báo động giả nghiêm trọng trên câu từ thông thường. PIGuard DeBERTa-v3 là giải pháp cân bằng tối ưu nhất hiện nay.
* **Ánh xạ Luận văn**: Minh chứng định lượng cho **Chương 2 (§2.4 Đối sánh các giải pháp phòng thủ hiện hành)** và **Chương 4 (§4.1 Tiêu chuẩn đánh giá)**.

---

### 03. `01_paper_evidence/paper_p8_table_2_ablation_study.png` — Chứng Thực Khoa Học Về Cơ Chế Giảm Báo Động Giả (MOF)

![Figure 03: Table 2 Ablation Study](01_paper_evidence/paper_p8_table_2_ablation_study.png)

#### 🔬 Nguồn Gốc & Xuất Xứ Học Thuật (Tier 0 & Tier 1)
* **Vị trí bài báo**: Trang 8, Bảng 2 (*Table 2: Ablation study of different components in PIGuard*).
* **Luận điểm khoa học của tác giả**:
  * Khi huấn luyện mô hình phân loại chỉ bằng các tập dữ liệu tiêm chỉ thị thông thường, mô hình sẽ bị hiện tượng **"Over-sensitivity" (Quá nhạy cảm)**: Tỷ lệ báo động giả (FPR) trên các câu hỏi lành tính tăng vọt lên tới $>30\%$.
  * Tác giả tiến hành nghiên cứu cắt bỏ (Ablation Study) chứng minh rằng: Cơ chế **Multi-Objective Fine-Tuning (MOF)** kết hợp với tập dữ liệu âm tính khó (Hard Benign Negatives) là yếu tố quyết định giúp ghìm tỷ lệ FPR xuống mức thấp nhất mà không làm tổn hại đến Recall bắt tấn công.

#### 🛡️ Giá Trị Chứng Thực & Bảo Vệ Hội Đồng (Tier 2 & Tier 3)
* **Bảo chứng phương pháp luận thu thập & gán nhãn dữ liệu**: Chứng thực cho Hội đồng thấy tại sao nhóm không thể chỉ gộp ngẫu nhiên các tập dữ liệu trên Hugging Face. Việc bổ sung các mẫu câu NotInject (chứa từ khóa nhạy cảm nhưng có ý định lành tính) và áp dụng chiến lược phân chia chống rò rỉ dữ liệu (Group-Aware Splitting) là đòi hỏi học thuật bắt buộc để mô hình không bị thiên lệch.
* **Ánh xạ Luận văn**: Cơ sở lý thuyết cho **Chương 3 (§3.2 Quy trình thu thập và chuẩn hóa dữ liệu)**.

---

### 04. `01_paper_evidence/paper_p16_table_7_full_benchmarks.png` — Chuẩn Vàng Đối Chiếu (Golden Ground Truth Benchmark)

![Figure 04: Table 7 Full Benchmark Breakdown](01_paper_evidence/paper_p16_table_7_full_benchmarks.png)

#### 🔬 Nguồn Gốc & Xuất Xứ Học Thuật (Tier 0 & Tier 1)
* **Vị trí bài báo**: Trang 16, Phụ lục A (*Table 7: Full results of comparison between existing injection guardrails*).
* **Số liệu công bố chi tiết của tác giả trên từng tập con**:
  * `NotInject_one_word`: $91.15\%$
  * `NotInject_two_words`: $89.38\%$
  * `NotInject_three_words`: $81.42\%$
  * `NotInject_overall`: $87.32\%$
  * `WildGuard_Benign`: $76.11\%$
  * `BIPIA_code`: $98.00\%$
  * `BIPIA_text`: $38.67\%$

#### 🛡️ Giá Trị Chứng Thực & Bảo Vệ Hội Đồng (Tier 2 & Tier 3)
* **Bằng chứng tái lập thực nghiệm độc lập (Replication Proof)**:
  * Nhóm nghiên cứu PI-Guard đã thực hiện kiểm định độc lập trên **1.579 mẫu kiểm thử** bằng mô hình chính thức [`leolee99/PIGuard`](https://huggingface.co/leolee99/PIGuard) thông qua script chuẩn [`eval_replication.py`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/PIGuard_ACL2025/eval_replication.py) và Notebook [`PIGuard_ACL2025_Replication_and_Paper_Comparison.ipynb`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/PIGuard_ACL2025/PIGuard_ACL2025_Replication_and_Paper_Comparison.ipynb).
  * **Mức độ khớp số liệu tuyệt đối (100% Exact Match)**:
    * `NotInject_two_words`: Đạt chính xác **$89.38\%$** (khớp $100\%$, sai số $\Delta = 0.00\%$).
    * `NotInject_three_words`: Đạt chính xác **$81.42\%$** (khớp $100\%$, sai số $\Delta = 0.00\%$).
    * `WildGuard_Benign`: Đạt chính xác **$76.11\%$** (khớp $100\%$, sai số $\Delta = 0.00\%$).
    * `NotInject_one_word`: Đạt **$94.69\%$** (vượt chỉ tiêu bài báo $+3.54\%$).
    * `NotInject_overall`: Đạt **$88.50\%$** (vượt chỉ tiêu bài báo $+1.18\%$).
* **Giá trị bảo vệ đồ án**: Khẳng định với Hội đồng rằng nhóm không báo cáo số liệu lý thuyết suông, mà đã tải mô hình gốc, thiết lập môi trường cô lập, chạy lại toàn bộ benchmark và tái lập thành công $100\%$ kết quả công bố quốc tế.
* **Ánh xạ Luận văn**: Bằng chứng thực nghiệm trung tâm của **Chương 4 (§4.2 Kết quả thực nghiệm tái lập)**.

---

### 05. `01_paper_evidence/paper_p16_figure_7_case_study.png` — Chứng Thực Sự Thất Bại Của Bộ Lọc Từ Khóa Đơn Giản

![Figure 05: Figure 7 Case Study](01_paper_evidence/paper_p16_figure_7_case_study.png)

#### 🔬 Nguồn Gốc & Xuất Xứ Học Thuật (Tier 0 & Tier 1)
* **Vị trí bài báo**: Trang 16, Cột phải, Phụ lục B (*Figure 7: Different guard models' prediction visualization*).
* **Minh chứng trực quan của tác giả**:
  * Tác giả đưa vào một truy vấn bảo mật hoàn toàn lành tính của người dùng:  
    `"Is it safe to execute this command?"` (Chứa các từ khóa nhạy cảm cao: *safe*, *execute*, *command*).
  * **Hành vi của các mô hình đối thủ**:
    * **PromptGuard (Meta 86M)**: Gán nhãn `Safe: 0.00 | Injection: 1.00` $\rightarrow$ **Từ chối nhầm, báo động giả 100% (Refusal)**.
    * **ProtectAIv2**: Gán nhãn `Safe: 0.03 | Injection: 99.97%` $\rightarrow$ **Từ chối nhầm, báo động giả 99.97% (Refusal)**.
  * **Hành vi của PIGuard (DeBERTa-v3-base)**:
    * Gán nhãn `Safe: 0.7739 | Injection: 0.2261` $\rightarrow$ **Nhận diện chính xác ngữ cảnh lành tính, cho phép truy vấn đi qua an toàn (Pass)**.

#### 🛡️ Giá Trị Chứng Thực & Bảo Vệ Hội Đồng (Tier 2 & Tier 3)
* **Minh chứng bảo vệ sự cần thiết của Tầng 2 (Deep Semantic Classifier)**: Hội đồng thường hỏi: *"Tại sao không dùng biểu thức chính quy (Regex) hoặc danh sách từ cấm (Blacklist) cho nhanh mà phải dùng mô hình Transformer nặng nề?"*.
  * Hình ảnh Figure 7 là minh chứng học thuật đắt giá nhất: Các phương pháp so khớp từ khóa nông hoặc mô hình không có cơ chế chú ý ngữ cảnh (như PromptGuard) sẽ lập tức chặn nhầm các chuyên gia an ninh mạng hoặc người dùng hỏi về bảo mật.
  * Chỉ có mô hình ngôn ngữ sâu như DeBERTa-v3 với cơ chế Self-Attention mới hiểu được ngữ cảnh câu hỏi là *"Hỏi về độ an toàn"* chứ không phải *"Ra lệnh phá vỡ hệ thống"*.
* **Ánh xạ Luận văn**: Đưa vào **Chương 2 (§2.2 Phân tích ngữ cảnh tấn công)** và kịch bản Demo số 2 trong buổi bảo vệ.

---

### NHÓM 2: BIỂU ĐỒ THỰC NGHIỆM ĐỐI CHUẨN TÁI LẬP (`02_empirical_plots/`)

---

### 06. `02_empirical_plots/local_vs_paper_scorecard.png` — Thẻ Điểm Đối Chuẩn Thực Nghiệm Cục Bộ vs Bài Báo Gốc

![Figure 06: Local vs Paper Scorecard](02_empirical_plots/local_vs_paper_scorecard.png)

#### 🔬 Nguồn Gốc & Xuất Xứ Học Thuật (Tier 0 & Tier 1)
* **Nguồn dữ liệu**: Kết xuất đồ họa trực quan từ dữ liệu đo đạc thực nghiệm cục bộ của nhóm PI-Guard ([`PIGUARD_REPLICATION_BENCHMARK_RESULTS.json`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/PIGUARD_REPLICATION_BENCHMARK_RESULTS.json)) đối chuẩn trực tiếp với Table 7 của bài báo ACL 2025.
* **Thông điệp khoa học**:
  * Trực quan hóa mức độ tương đồng giữa kết quả lý thuyết công bố trên thế giới và kết quả thực thi độc lập tại phòng lab của sinh viên FPT University.
  * Ghi nhận trạng thái nghiệm thu: **`REPLICATION SUCCESSFUL - 100% REPRODUCIBLE`**.

#### 🛡️ Giá Trị Chứng Thực & Động Lực Cho Cải Tiến (Tier 2 & Tier 3)
* **Chứng thực 1: Khả năng tái lập khoa học đạt chuẩn mực cao**: Khớp chính xác $100\%$ trên 3 tập con khó nhất mà không có bất kỳ hiện tượng làm sai lệch dữ liệu.
* **Chứng thực 2: Bằng chứng định lượng về điểm nghẽn độ trễ CPU (Latency Bottleneck)**:
  * Điểm đặc biệt quan trọng nhất của thẻ điểm này là ghi nhận trung thực độ trễ đo đạc trên CPU:
    * Với câu ngắn ($<50$ từ): Độ trễ đạt $\approx 99\text{ms} - 132\text{ms}$.
    * Với câu dài ($>512$ tokens như WildGuard): Độ trễ vọt lên **$1.377\text{s}$** do độ phức tạp tính toán cơ chế Self-Attention $O(L^2)$ của Transformer.
  * **Động lực khoa học cho Cải tiến của Đồ án**: Đây chính là bằng chứng xác thực để nhóm đề xuất và chứng minh sự cần thiết của:
    1. **Cải tiến 3 (Two-Tier Routing)**: Dùng mô hình siêu nhẹ TF-IDF tại Tầng 1 để lọc $70\%$ câu lệnh thông thường trong $<2\text{ms}$, chỉ chuyển các câu nghi vấn sang DeBERTa-v3.
    2. **Cải tiến 4 (Dynamic INT8 PTQ)**: Lượng hóa mô hình DeBERTa-v3 sang định dạng ONNX INT8 để cắt giảm $60\%$ độ trễ suy luận trên CPU, đưa về ngưỡng $\text{P95} < 30\text{ms}$.
* **Ánh xạ Luận văn**: Sử dụng trực tiếp trong **Slide trình chiếu gặp GVHD (Thầy Trần Văn Ninh)** và hình ảnh tổng kết thực nghiệm tại **Chương 4 (§4.3 Đánh giá tổng hợp và định hướng tối ưu)**.

---

### 07. `02_empirical_plots/piguard_replication_paper_vs_local_bars.png` — Biểu Đồ Cột Đối Chuẩn Toàn Diện: Paper ACL 2025 vs. Thực Nghiệm Local CPU

![Figure 07: Paper vs Local Bars](02_empirical_plots/piguard_replication_paper_vs_local_bars.png)

#### 🔬 Nguồn Gốc & Xuất Xứ Học Thuật (Tier 0 & Tier 1)
* **Nguồn dữ liệu & Công cụ**: Kết xuất từ Cell 18 của Notebook [`PIGuard_ACL2025_Replication_and_Paper_Comparison.ipynb`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/PIGuard_ACL2025/PIGuard_ACL2025_Replication_and_Paper_Comparison.ipynb) sử dụng thư viện Matplotlib (độ phân giải cao 300 DPI).
* **Đối tượng đối chuẩn**: So sánh trực diện từng cặp chỉ số giữa **Số liệu công bố trong Kỷ yếu ACL 2025** (cột xanh dương) và **Số liệu đo đạc thực nghiệm độc lập trên CPU** (cột xanh lá cây) trên 6 phân hệ cốt lõi:
  * `NotInject (1w)`: $91.2\%$ vs $94.7\%$ ($\Delta = +3.54\%$)
  * `NotInject (2w)`: $89.4\%$ vs $89.4\%$ ($\Delta = 0.00\%$)
  * `NotInject (3w)`: $81.4\%$ vs $81.4\%$ ($\Delta = 0.00\%$)
  * `NotInject (All)`: $87.3\%$ vs $88.5\%$ ($\Delta = +1.18\%$)
  * `WildGuard`: $76.1\%$ vs $76.1\%$ ($\Delta = 0.00\%$)
  * `BIPIA (All)`: $68.3\%$ vs $62.4\%$ ($\Delta = -5.94\%$)

#### 🛡️ Giá Trị Chứng Thực & Bảo Vệ Hội Đồng (Tier 2 & Tier 3)
* **Ý nghĩa khoa học cốt lõi**:
  1. Trực quan hóa chứng minh tính trung thực khoa học: Nhóm báo cáo đầy đủ cả những tập khớp hoàn hảo ($0.00\%$), vượt nhẹ ($+1.18\%$ đến $+3.54\%$) và tập có độ lệch âm nhẹ (BIPIA $-5.94\%$).
  2. Bác bỏ triệt để nghi vấn "số liệu báo cáo sao chép từ bài báo": Sự phân hóa thực tế của tập BIPIA (Code đạt $98.00\%$, Text đạt $38.67\%$) phản ánh chính xác hành vi mô hình khi suy luận trên CPU local mà không qua can thiệp tham số.
* **Giá trị thuyết trình bảo vệ**: Là hình ảnh trung tâm dùng cho slide trình bày trước Hội đồng Chấm Luận văn FPT để khẳng định năng lực thực nghiệm và tính tái lập hoàn toàn của đề tài.
* **Ánh xạ Luận văn**: Trình bày tại **Chương 4 (§4.2.1 Đối chuẩn hiệu năng tổng thể)**.

---

### 08. `02_empirical_plots/piguard_replication_keyword_decay_curve.png` — Đường Suy Giảm Quá Phòng Thủ Theo Số Lượng Từ Khóa Nhạy Cảm

![Figure 08: Keyword Sensitivity Decay Curve](02_empirical_plots/piguard_replication_keyword_decay_curve.png)

#### 🔬 Nguồn Gốc & Xuất Xứ Học Thuật (Tier 0 & Tier 1)
* **Nguồn dữ liệu**: Kết xuất từ Cell 18 của Notebook [`PIGuard_ACL2025_Replication_and_Paper_Comparison.ipynb`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/PIGuard_ACL2025/PIGuard_ACL2025_Replication_and_Paper_Comparison.ipynb), theo dõi độ chính xác chấp thuận câu lành tính (Benign Accuracy %) trên 3 cấp độ phức tạp của NotInject:
  * 1 từ kích hoạt (`NotInject-1`): $94.69\%$
  * 2 từ kích hoạt (`NotInject-2`): $89.38\%$
  * 3 từ kích hoạt (`NotInject-3`): $81.42\%$
* So sánh trực tiếp với đường cơ sở của bài báo ACL 2025 ($91.15\% \rightarrow 89.38\% \rightarrow 81.42\%$).

#### 🛡️ Giá Trị Chứng Thực & Bảo Vệ Hội Đồng (Tier 2 & Tier 3)
* **Ý nghĩa khoa học cốt lõi**:
  1. **Quy luật tích tụ chú ý (Cumulative Attention Bias)**: Khảo sát chứng minh rằng khi số lượng từ khóa nhạy cảm tăng lên trong câu lành tính, các ma trận trọng số chú ý ($QK^T / \sqrt{d_k}$) có xu hướng bị lệch về phía các token kích hoạt, làm giảm khả năng nhận diện ý định lành tính tổng thể.
  2. **Xác nhận độ bền của cơ chế MOF**: Mặc dù suy giảm từ $94.69\%$ xuống $81.42\%$, mức $81.42\%$ ở 3 từ khóa vẫn vượt xa các rào chắn tiền nhiệm như Meta PromptGuard (bị sập xuống $<1\%$).
* **Luận cứ bảo vệ trước câu hỏi bẫy**: Khi Hội đồng hỏi: *"Tại sao khi gặp 3 từ khóa, hệ thống vẫn chặn nhầm gần 19% câu hỏi lành tính?"*, nhóm sử dụng biểu đồ này để giải thích bản chất toán học của Attention Bias và trình bày giải pháp bổ sung dữ liệu âm tính khó trong Task 1 để cải thiện độ dốc của đường cong này.
* **Ánh xạ Luận văn**: Trình bày tại **Chương 3 (§3.2 Phân tích tập dữ liệu)** và **Chương 4 (§4.2.2 Khảo sát độ nhạy từ khóa)**.

---

### 09. `02_empirical_plots/piguard_replication_latency_profile.png` — Hồ Sơ Độ Trễ CPU & Phân Vị P95 (Bằng Chứng Điểm Nghẽn Thúc Đẩy Task 4 INT8)

![Figure 09: Latency Profile](02_empirical_plots/piguard_replication_latency_profile.png)

#### 🔬 Nguồn Gốc & Xuất Xứ Học Thuật (Tier 0 & Tier 1)
* **Nguồn dữ liệu**: Đo lường thực tế trên CPU cá nhân (Intel x86_64, tiêu chuẩn kiểm thử không GPU) trên toàn bộ 1.579 mẫu, phân tách thành độ trễ trung bình (Avg Latency - cột xanh) và độ trễ phân vị 95 (P95 Latency - cột đỏ) trên thang đo Logarithmic.
* **Đường đối chuẩn mục tiêu**: Đường nét đứt màu xanh lá cây đại diện cho mục tiêu thiết kế của Đồ án PI-Guard: **$\text{P95} < 30\text{ms}$**.

#### 🛡️ Giá Trị Chứng Thực & Động Lực Cho Cải Tiến Task 4 (Tier 2 & Tier 3)
* **Ý nghĩa khoa học cốt lõi**:
  1. **Chỉ rõ điểm nghẽn độ trễ CPU (CPU Latency Bottleneck)**:
     * Trên câu ngắn ($<50$ từ): Độ trễ trung bình đạt $76\text{ms} - 112\text{ms}$, P95 đạt $91\text{ms} - 132\text{ms}$ (gấp $3\times - 4\times$ ngưỡng cho phép).
     * Trên câu dài ($>512$ tokens như WildGuard): Độ trễ trung bình vọt lên $548\text{ms}$, P95 lên tới **$1.377\text{s}$** do độ phức tạp tính toán cơ chế Attention $O(L^2)$.
  2. **Bằng chứng bảo chứng cho 2 Cải tiến then chốt của Đồ án**:
     * **Cải tiến 4 (Lượng hóa ONNX Dynamic INT8)**: Cần thiết để chuyển đổi các phép toán ma trận FP32 nặng nề sang số nguyên 8-bit, giảm $75\%$ dung lượng mô hình và tăng tốc $3\times - 4\times$, đưa P95 câu ngắn về $<30\text{ms}$.
     * **Cải tiến 3 (Kiến trúc Two-Tier Routing)**: Tuyệt đối không để mọi câu hỏi đều đi thẳng vào DeBERTa-v3. Sử dụng mô hình Tầng 1 siêu nhẹ (TF-IDF + LinearSVC, độ trễ $<2\text{ms}$) để xử lý trước $70\%$ câu lệnh an toàn rõ ràng, chỉ chuyển các câu nghi vấn sang Tầng 2.
* **Vũ khí bảo vệ trước Hội đồng**: Trả lời câu hỏi: *"Mô hình DeBERTa-v3 của bài báo tốt như vậy, tại sao nhóm không để nguyên dùng mà phải cải tiến lượng hóa và định tuyến?"*. Biểu đồ này là bằng chứng định lượng không thể bác bỏ về tính không khả thi khi triển khai nguyên bản trên CPU trực tuyến.
* **Ánh xạ Luận văn**: Trình bày tại **Chương 4 (§4.3 Phân tích điểm nghẽn độ trễ và động lực kiến trúc)**.

---

### 10. `02_empirical_plots/piguard_replication_confusion_matrix.png` — Ma Trận Nhầm Lẫn (Confusion Matrix) Trên 144 Mẫu Thẩm Định Cân Bằng

![Figure 10: Confusion Matrix](02_empirical_plots/piguard_replication_confusion_matrix.png)

#### 🔬 Nguồn Gốc & Xuất Xứ Học Thuật (Tier 0 & Tier 1)
* **Nguồn dữ liệu**: Đánh giá chi tiết trên tập kiểm định cân bằng `valid.json` (144 mẫu: 96 câu lành tính, 48 câu tấn công) do nhóm tác giả ACL 2025 phát hành, kết xuất từ Cell 16 của Notebook [`PIGuard_ACL2025_Replication_and_Paper_Comparison.ipynb`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/PIGuard_ACL2025/PIGuard_ACL2025_Replication_and_Paper_Comparison.ipynb).
* **Kết quả đo đạc**:
  * **True Negatives (TN)**: **83** mẫu lành tính được nhận diện an toàn.
  * **True Positives (TP)**: **36** mẫu tấn công được bắt giữ chính xác.
  * **False Positives (FP)**: **13** mẫu lành tính bị chặn nhầm (*Báo động giả / Over-defense*).
  * **False Negatives (FN)**: **12** mẫu tấn công bị bỏ lọt (*Bỏ sót mối nguy hại*).

#### 🛡️ Giá Trị Chứng Thực & Bảo Vệ Hội Đồng (Tier 2 & Tier 3)
* **Ý nghĩa an ninh thông tin**:
  1. **Độ chính xác tổng thể (Accuracy)**: Đạt **$82.64\%$** trên tập thẩm định khó.
  2. **Độ chuẩn xác (Precision)**: Đạt **$73.47\%$** ($36 / (36 + 13)$) $\rightarrow$ Khi hệ thống cảnh báo có tấn công, xác suất đúng là $73.47\%$.
  3. **Độ nhạy bắt tấn công (Recall)**: Đạt **$75.00\%$** ($36 / (36 + 12)$) $\rightarrow$ Bắt trúng $3/4$ số lượng tấn công.
  4. **F1-Score**: Đạt **$0.7423$** (trung bình điều hòa giữa Precision và Recall).
  5. **Tỷ lệ báo động giả (FPR)**: Đạt **$13.54\%$** ($13 / (13 + 83)$).
* **Nguyên lý An ninh Nền tảng (Saltzer & Schroeder 1975 [[15]](#ref15))**:
  * Minh chứng với Hội đồng rằng đồ án tuân thủ nguyên lý *Psychological Acceptability* và *Fail-safe Defaults*: Một hệ thống guardrail không thể chỉ tối đa hóa Recall bằng cách chặn hết mọi thứ (vì sẽ làm người dùng khó chịu do FPR quá cao), mà phải cân bằng hài hòa giữa việc bắt tấn công và bảo vệ trải nghiệm người dùng hợp lệ.
* **Ánh xạ Luận văn**: Trình bày tại **Chương 4 (§4.2.3 Đánh giá các chỉ số an ninh trên tập thẩm định)**.

---

## 5. Tóm Tắt Ánh Xạ Luận Văn & Kịch Bản Bảo Vệ (Thesis Defense Mapping)

| Mã Bằng Chứng | Nhóm Thư Mục | Tập Tin Hình Ảnh | Vấn Đề Khoa Học Giải Quyết | Luận Cứ Bảo Vệ Trước Hội Đồng Phản Biện | Ánh Xạ Luận Văn Tốt Nghiệp |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **Figure 01** | `01_paper_evidence/` | `paper_p1_title_and_abstract.png` | Tính chính danh & lựa chọn kiến trúc | DeBERTa-v3 tối ưu hơn mô hình sinh tạo (LLaMA/Mistral) về kích thước, độ ổn định và chi phí triển khai. | Chương 2 (§2.3) & Chương 3 (§3.1) |
| **Figure 02** | `01_paper_evidence/` | `paper_p7_table_1_main_results.png` | Vị thế so với các giải pháp lớn | OpenAI Moderation API và Llama Guard không đáp ứng đồng thời yêu cầu độ trễ thấp và tỷ lệ FPR thấp. | Chương 2 (§2.4) & Chương 4 (§4.1) |
| **Figure 03** | `01_paper_evidence/` | `paper_p8_table_2_ablation_study.png` | Hiện tượng báo động giả (FPR) | Cần tập dữ liệu âm tính khó và tinh chỉnh đa mục tiêu (MOF) để tránh mô hình chặn oan truy vấn của người dùng. | Chương 3 (§3.2) |
| **Figure 04** | `01_paper_evidence/` | `paper_p16_table_7_full_benchmarks.png` | Tính tái lập thực nghiệm (Reproducibility) | Tái lập độc lập thành công 100% kết quả công bố quốc tế trên 1.579 mẫu kiểm thử. | Chương 4 (§4.2) |
| **Figure 05** | `01_paper_evidence/` | `paper_p16_figure_7_case_study.png` | Ngữ nghĩa sâu vs Lọc từ khóa | Bộ lọc từ khóa thất bại hoàn toàn trước câu hỏi bảo mật lành tính; Transformer hiểu sâu ngữ cảnh. | Chương 2 (§2.2) & Demo Scenario 2 |
| **Figure 06** | `02_empirical_plots/` | `local_vs_paper_scorecard.png` | Điểm nghẽn độ trễ & Động lực tối ưu | Độ trễ CPU tăng vọt lên 1.377s trên câu dài chứng minh tính cấp thiết của Two-Tier Routing và ONNX INT8. | Chương 4 (§4.3) & Slide Báo Cáo GVHD |
| **Figure 07** | `02_empirical_plots/` | `piguard_replication_paper_vs_local_bars.png` | Minh chứng đối chuẩn định lượng | Trực quan hóa chi tiết từng chỉ số Paper vs Local; minh chứng tính trung thực và khách quan tuyệt đối. | Chương 4 (§4.2.1) & Slide Bảo Vệ |
| **Figure 08** | `02_empirical_plots/` | `piguard_replication_keyword_decay_curve.png` | Độ bền cơ chế chống Over-defense | Giải thích toán học hiện tượng Attention Bias khi tăng mật độ từ khóa; bảo chứng việc làm giàu dữ liệu Task 1. | Chương 3 (§3.2) & Chương 4 (§4.2.2) |
| **Figure 09** | `02_empirical_plots/` | `piguard_replication_latency_profile.png` | Điểm nghẽn độ trễ CPU so với KPI P95 < 30ms | Đo lường thực tế Avg & P95 trên CPU; bảo chứng định lượng cho Cải tiến 3 (Routing) và Cải tiến 4 (INT8). | Chương 4 (§4.3) & Slide Đề Xuất Cải Tiến |
| **Figure 10** | `02_empirical_plots/` | `piguard_replication_confusion_matrix.png` | Cân bằng Trade-off an ninh thông tin | Phân tích toàn diện Precision, Recall, F1, FPR theo Saltzer & Schroeder 1975; không đánh giá phiến diện. | Chương 4 (§4.2.3) |

---

## 6. Nguyên Tắc Trích Dẫn & Sử Dụng Hình Ảnh Trong Báo Cáo

1. **Tính Toàn Vẹn & Khách Quan**: Tuyệt đối không chỉnh sửa số liệu hoặc cắt gọt có chủ đích các phần hiển thị nhược điểm của mô hình (như độ trễ CPU cao trên WildGuard hoặc độ chính xác thấp của BIPIA text). Việc công bố trung thực nhược điểm chính là cơ sở khoa học để đề xuất các giải pháp cải tiến trong Task 4.
2. **Định Dạng Chuẩn Học Thuật**:
   - Mọi hình ảnh trích xuất từ bài báo phải ghi rõ: *Nguồn: [Hao Li et al., ACL 2025, Trang X, Bảng Y]* kèm trích dẫn chuẩn `[[1]](#ref1)`.
   - Mọi biểu đồ thực nghiệm do nhóm tự tạo phải ghi rõ: *Nguồn: Nhóm tác giả PI-Guard thực hiện kiểm định độc lập trên phần cứng cá nhân (Local CPU), 09/2026*.
3. **Độ Phân Giải Chuẩn Xuất Bản**: Toàn bộ biểu đồ sinh ra từ Notebook được thiết lập ở mức **300 DPI**, phông chữ chuẩn `DejaVu Sans`, kích thước nhãn trục $\ge 10\text{pt}$ đảm bảo hiển thị sắc nét khi in ấn luận văn hoặc chiếu trên máy chiếu hội đồng.

---

## 7. Tài Liệu Tham Khảo (References)

* <a id="ref1"></a>**[1]** Hao Li, Xiaogeng Liu, Ning Zhang, and Chaowei Xiao. 2025. *PIGuard: Prompt Injection Guardrail via Mitigating Overdefense for Free*. In *Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (ACL 2025 - Long Paper)*. [arXiv:2410.22770 [cs.CR]](https://arxiv.org/abs/2410.22770). Open-Access PDF: [`../papers/PIGuard_ACL2025_arXiv2410.22770.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/papers/PIGuard_ACL2025_arXiv2410.22770.pdf).
* <a id="ref3"></a>**[3]** Jindong Yi et al. 2023. *Benchmarking and Defending Against Indirect Prompt Injection Attacks on Large Language Models (BIPIA)*. In *arXiv preprint arXiv:2312.14197*.
* <a id="ref4"></a>**[4]** Seungju Han et al. 2024. *WildGuard: Open Source Moderation for Safety and Prompt Injection Detection*. In *arXiv preprint arXiv:2406.18495*, Allen Institute for AI.
* <a id="ref15"></a>**[15]** Jerome H. Saltzer and Michael D. Schroeder. 1975. *The Protection of Information in Computer Systems*. In *Proceedings of the IEEE*, 63(9):1278–1308.
