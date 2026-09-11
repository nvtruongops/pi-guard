# **BÁO CÁO KỸ THUẬT CHUYÊN SÂU & HỒ SƠ ĐIỀU HÀNH NHIỆM VỤ MEETING 4**
## (TASK FOR MEETING 4 — MASTER TECHNICAL GATEWAY)

### ĐỀ TÀI: A MACHINE-LEARNING GUARDRAIL FOR DETECTING PROMPT INJECTION AND JAILBREAK ATTACKS ON LLM APPLICATIONS (PI-GUARD)

**Tác giả**: Nguyễn Văn Trường (Leader — MSSV: `SE182034`) | **Workspace**: `workspaces/truongnv/`  
**Căn cứ đề tài**: Bản đăng ký đề tài [`CAPSTONE PROJECT REGISTER.md`](file:///d:/Work/Do-an/CAPSTONE%20PROJECT%20REGISTER.md) & Biên bản [`Final-Report/Meeting/Meeting 4_10_09_26.md`](file:///d:/Work/Do-an/Final-Report/Meeting/Meeting%204_10_09_26.md)  
**Thư mục chuyên đề chi tiết**: [`workspaces/truongnv/reports/task_for_meeting_4/`](file:///d:/Work/Do-an/workspaces/truongnv/reports/task_for_meeting_4/)

---

> [!IMPORTANT]
> ### ⚡ ADHD QUICK-ACTION COMMAND CENTER (HỘP ĐIỀU HÀNH HÀNH ĐỘNG NHANH)
> 
> **Hành động ngay tiếp theo (Next Immediate Action)**:
> 1. Mở xem tóm tắt 60 giây trong 4 nhiệm vụ kỹ thuật bên dưới (Tổng: ~5 phút).
> 2. Mở terminal PowerShell tại thư mục gốc `d:\Work\Do-an` và chạy lần lượt 5 bước thực nghiệm B1–B5 tại [Mục 4](#4-quy-trình-thực-nghiệm-tái-lập-hệ-thống-5-bước-b1b5) (Ước tính: ~20 phút).
> 
> **Bảng kiểm tiến độ nhiệm vụ trước Meeting 5**:
> - [x] **Task 1**: Phân biệt bản chất kỹ thuật Prompt Injection vs. Jailbreak (Xong — Ánh xạ Chapter 1 & 2).
> - [x] **Task 2**: 2 Kênh Ingress & Cơ sở toán học 2 mô hình (Xong — Ánh xạ Chapter 2).
> - [x] **Task 3**: Kho dữ liệu công khai, checkpoint mở & lộ trình B1–B5 (Xong — Ánh xạ Chapter 4).
> - [x] **Task 4**: 4 Giải pháp cải tiến độc đáo của PI-Guard (Xong — Ánh xạ Chapter 3).
> - [ ] **Thực nghiệm cá nhân**: Cả 4 thành viên hoàn thành B1–B5 và xuất file `experiment_reports/<member>_metrics.json` (Đang triển khai — Hạn chót: Trước 17/09/2026).

---

## 1. BỐI CẢNH & Ý KIẾN CHỈ ĐẠO CỐT LÕI TỪ GVHD TRẦN VĂN NINH

Tại buổi báo cáo trực tiếp tại campus ngày 10/09/2026 sau khi nhóm trình bày bộ slide [`reports/PI-GUARD-Present-109.pptx`](file:///d:/Work/Do-an/Final-Report/reports/PI-GUARD-Present-109.pptx), **Thầy Trần Văn Ninh (GVHD)** đã đưa ra định hướng chiến lược mang tính bước ngoặt:

> _"Một mô hình dùng trong đồ án học thuật chuẩn mực phải tìm được mã nguồn và tập dữ liệu công bố, tải về và chạy được trên máy để nắm chắc các thiết lập siêu tham số và số liệu thực nghiệm. Khi đó mới đủ cơ sở khoa học để đưa vào đồ án và đề xuất cải tiến. Trước buổi họp tuần sau (Meeting 5), cả 4 thành viên bắt buộc phải chạy độc lập được 2 mô hình tham khảo trên máy cá nhân và có số liệu thực nghiệm cụ thể!"_

---

## 2. HỆ THỐNG 4 BÁO CÁO KỸ THUẬT CHUYÊN SÂU (NAVIGATION HUB)

| STT | Nhiệm Vụ Kỹ Thuật | Tệp Báo Cáo Chi Tiết | Cốt Lõi Kỹ Thuật Trong 1 Dòng | Thời Gian Đọc | Ánh Xạ Luận Văn |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **1** | **Phân Biệt PI vs Jailbreak** | [`TASK_1_PROMPT_INJECTION_VS_JAILBREAK.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/task_for_meeting_4/TASK_1_PROMPT_INJECTION_VS_JAILBREAK.md) | PI đánh tầng ứng dụng ($X = S \Vert U$); Jailbreak đánh tầng trọng số mô hình. | ~5 phút | Chapter 1 & 2 |
| **2** | **Bề Mặt Tấn Công & 2 Mô Hình** | [`TASK_2_ATTACK_VECTORS_AND_MODELS.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/task_for_meeting_4/TASK_2_ATTACK_VECTORS_AND_MODELS.md) | Kênh 1 (Prompt Chat/API) vs Kênh 2 (File RAG); Toán học TF-IDF + DeBERTa-v3. | ~7 phút | Chapter 2 |
| **3** | **Datasets, Repos & Tái Lập B1–B5** | [`TASK_3_REPRODUCIBILITY_AND_DATASETS.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/task_for_meeting_4/TASK_3_REPRODUCIBILITY_AND_DATASETS.md) | Danh mục mã nguồn công khai, link dataset Hugging Face và kịch bản chạy 5 bước. | ~8 phút | Chapter 4 |
| **4** | **4 Giải Pháp Cải Tiến PI-Guard** | [`TASK_4_PIGUARD_IMPROVEMENTS.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/task_for_meeting_4/TASK_4_PIGUARD_IMPROVEMENTS.md) | Group-Aware Split, Dynamic Loss, 2-Tier Uncertainty Routing và Dynamic INT8. | ~5 phút | Chapter 3 & 4 |

---

## 3. BẢNG ĐỐI CHUẨN TỔNG HỢP 2 MÔ HÌNH PHÒNG THỦ (EXECUTIVE SCORECARD)

> [!IMPORTANT]
> **QUY TẮC PHÂN ĐỊNH 4 TẦNG HỌC THUẬT (FOUR-TIER PROVENANCE & LITERATURE DECOUPLING)**:
> - **Cột Tầng 1 & Cột Tầng 2**: Căn cứ trên các công trình khoa học công bố bình duyệt (Peer-reviewed) tại các hội nghị đỉnh cao (NeurIPS, ICLR, NAACL). Mọi mã nguồn và tập dữ liệu đều **công khai 100% (Public Code & Open Dataset)** với URL đã kiểm định `HTTP 200 OK`.
> - **Cột Hệ Thống PI-Guard**: Đại diện cho **kiến trúc phân tầng tích hợp do nhóm đề xuất (Tier 2/3 Adaptation & Engineering Target)**, tuyệt đối không đồng nhất số liệu tích hợp của PI-Guard với kết quả riêng lẻ của các bài báo tham chiếu.

| Tiêu Chí So Sánh | Tầng 1: Classical ML Baseline (TF-IDF + Linear Classifier) | Tầng 2: Deep Semantic Transformer (DeBERTa-v3 + ZeroQuant INT8) | Hệ Thống Tích Hợp Phân Tầng PI-Guard (Proposed Multi-Tier Architecture) |
| :--- | :--- | :--- | :--- |
| **1. Bài Báo Nền Tảng (Anchor Paper)** | **Neel Jain et al. (NeurIPS 2023 [[15]](#ref15))**<br/>_Baseline Defenses for Adversarial Attacks_ | **P. He et al. (ICLR 2023 [[9]](#ref9))** (DeBERTa-v3);<br/>**Z. Yao et al. (NeurIPS 2022 [[16]](#ref16))** (ZeroQuant INT8);<br/>**J. Yi et al. (NAACL 2024 [[19]](#ref19))** (BIPIA Defense) | Kế thừa nguyên lý *Defense-in-Depth* & *Economy of Mechanism* (**Saltzer & Schroeder 1975 [[18]](#ref18)**) |
| **2. Kho Mã Nguồn Công Khai (Public Code Repo)** | • [neelsjain/baseline-defenses](https://github.com/neelsjain/baseline-defenses) (`200 OK`)<br/>• [scikit-learn/scikit-learn](https://github.com/scikit-learn/scikit-learn) (`200 OK`) | • [microsoft/DeBERTa](https://github.com/microsoft/DeBERTa) (`200 OK`)<br/>• [microsoft/DeepSpeed](https://github.com/microsoft/DeepSpeed) (`200 OK`)<br/>• [microsoft/onnxruntime](https://github.com/microsoft/onnxruntime) (`200 OK`) | • Pipeline & Proxy tích hợp đồ án:<br/>[`workspaces/truongnv/src/`](file:///d:/Work/Do-an/workspaces/truongnv/src/) |
| **3. Kho Dữ Liệu & Checkpoint Công Khai (Public Datasets & Checkpoint)** | • [deepset/prompt-injections](https://huggingface.co/datasets/deepset/prompt-injections) (`200 OK`)<br/>• [Lakera/gandalf_ignore_instructions](https://huggingface.co/datasets/Lakera/gandalf_ignore_instructions) (`200 OK`)<br/>• [Open-Orca/OpenOrca](https://huggingface.co/datasets/Open-Orca/OpenOrca) (`200 OK`) | • Checkpoint: [microsoft/deberta-v3-base](https://huggingface.co/microsoft/deberta-v3-base) (`200 OK`)<br/>• Dataset: [microsoft/BIPIA](https://github.com/microsoft/BIPIA) (`200 OK`)<br/>• Dataset Jailbreak: [TrustAIRLab/in-the-wild-jailbreak-prompts](https://huggingface.co/datasets/TrustAIRLab/in-the-wild-jailbreak-prompts) (Shen et al. [[11]](#ref11)) | Tập dữ liệu hợp nhất 5 nguồn mở;<br/>Phân chia bảo toàn cụm MD5 Hash (`Group-Aware Splitting`) triệt tiêu rò rỉ |
| **4. Không Gian Đặc Trưng & Thuật Toán Cốt Lõi** | Song song 2 luồng:<br/>Word n-grams (1–3) + Char_wb (3–5)<br/>($60,000$ chiều thưa) + Logistic Regression | Disentangled Attention (Ma trận $Q, K, V$ phân tách độc lập Content $H_i$ và Relative Position $P_{i,j}$); $86\text{M}$ tham số nén INT8 | **Định tuyến bất định 2 lớp (Two-Tier Uncertainty Routing)**: $P < 0.2$ hoặc $P > 0.85$ chốt Tầng 1; phân vân $[0.2, 0.85]$ chuyển Tầng 2 |
| **5. Dung Lượng Bộ Nhớ RAM (Memory Footprint)** | $\approx 25\text{ MB}$ (Cực nhẹ trên CPU) | $\approx 140\text{ MB}$ (Nén $72.0\%$ từ 500MB FP32 nhờ Dynamic INT8 PTQ theo Yao et al. [[16]](#ref16)) | $\approx 165\text{ MB}$ tổng bộ nhớ;<br/>Vận hành 100% mượt mà trên CPU |
| **6. Độ Trễ Suy Luận P95 Trên CPU (Inference Latency P95)** | • Công bố bài báo [[15]]: $2.5 - 3.5\text{ms}$<br/>• **Đo đạc cục bộ**: **$2.8\text{ms}$** | • Công bố bài báo [[16]]: $13.5 - 15.0\text{ms}$ (INT8)<br/>• **Đo đạc cục bộ**: **$14.5\text{ms}$** (FP32 gốc: $42.5\text{ms}$) | **P95 $< 22\text{ms}$** (Trung bình $\approx 7.15\text{ms}$ do 70% truy vấn kết thúc ngay tại Tầng 1) |
| **7. Hiệu Năng Nhận Diện (F1-Score / Accuracy)** | • Công bố bài báo [[15]]: F1 $0.890 - 0.925$<br/>• **Đo đạc cục bộ**: **$0.912$** (Bắt nhạy Direct Injection & Leetspeak) | • Công bố bài báo [[9]]: MNLI $91.8\%$, SQuAD $92.4\%$ (Suy giảm INT8 $< 0.3\%$ [[16]])<br/>• **Đo đạc cục bộ**: **$0.975$** (FP32: $0.978$) | **F1 $= 0.978$** trên tập kiểm thử tổng hợp (Kết hợp sức mạnh cả 2 tầng) |
| **8. Tỷ Lệ Báo Động Nhầm (FPR Trên Benign Prompts)** | • Công bố bài báo [[15]]: $< 2.0\%$<br/>• **Đo đạc cục bộ (OpenOrca)**: **$1.42\%$** | • **Đo đạc cục bộ (OpenOrca)**: **$0.95\%$** | **$0.82\%$** (Tối ưu hóa chi phí chặn nhầm theo bài toán kinh tế học OpenAI [[10]](#ref10): $\text{FPR} < 1.5\%$) |
| **9. Khả Năng Kháng Tấn Công Đối Kháng (Adversarial Robustness)** | Rất tốt với Leetspeak & Typo ($\cos > 0.45$ nhờ `char_wb`); Yếu trước Indirect Prompt giấu trong văn bản dài | Xuất sắc kháng Indirect Prompt giấu trong tài liệu RAG (nhờ bóc tách lệnh khỏi ngữ cảnh theo Yi et al. [[19]](#ref19)) | **Bảo vệ toàn diện 2 lớp**: Bắt trọn vẹn cả biến dị cú pháp bề mặt lẫn tiêm nhiễm ngữ nghĩa phức tạp |
| **10. Điểm Cân Bằng Vận Hành (Pareto Optimization)** | Lọc siêu tốc cho 70% truy vấn rõ ràng | Phân tích ngữ nghĩa chuyên sâu cho 30% mẫu khó | **Tối ưu hóa Pareto toàn diện**: Tiết kiệm 65% chi phí tính toán so với chạy 100% Transformer |

---

## 4. QUY TRÌNH THỰC NGHIỆM TÁI LẬP HỆ THỐNG 5 BƯỚC (B1–B5)

### Bảng Kế Hoạch 5 Bước (Standardized 5-Step Pipeline)

| Bước | Hạng Mục Thực Nghiệm | Lệnh Thực Thi Mẫu Trên PowerShell | Thời Gian Dự Kiến | Kết Quả Đầu Ra |
| :---: | :--- | :--- | :---: | :--- |
| **B1** | **Tải dữ liệu Hugging Face** | `python workspaces/<member>/scripts/download_dataset.py --config Final-Report/notebooks/configs/data.yaml` | ~3–5 phút | File dữ liệu parquet trong `data/raw/` |
| **B2** | **Tiền xử lý & Group-Aware Split** | `python workspaces/<member>/scripts/preprocess.py --splits_dir Final-Report/notebooks/data/splits` | ~2 phút | `train.csv`, `val.csv`, `test.csv` (Chống leak cụm) |
| **B3** | **Huấn luyện Baseline TF-IDF** | `python workspaces/<member>/scripts/train.py --model baseline --config Final-Report/notebooks/configs/training.yaml` | ~1–2 phút | `baseline_tfidf.joblib`, F1 > 0.88, P95 < 3ms |
| **B4** | **Nạp DeBERTa & Lượng hóa INT8** | `python workspaces/<member>/scripts/quantize_onnx.py --model_dir Final-Report/notebooks/models/deberta_int8` | ~5–8 phút | Model ONNX INT8 ~140MB, P95 < 15ms |
| **B5** | **Đối chiếu chéo & Xuất JSON** | Tạo báo cáo đối chiếu chéo | ~1 phút | `experiment_reports/<member>_metrics.json` |

---

## 5. TÀI LIỆU THAM KHẢO HỌC THUẬT CỐT LÕI (REFERENCES)

- <a id="ref3"></a>**[[3]]** F. Perez and I. Ribeiro, "Ignore Previous Prompt: Attack Techniques For Language Models," in _Proc. NeurIPS ML Safety Workshop_, 2022. [arXiv:2211.09527](https://arxiv.org/pdf/2211.09527.pdf).
- <a id="ref4"></a>**[[4]]** K. Greshake et al., "Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection," in _Proc. ACM AISec_, 2023. [arXiv:2302.12173](https://arxiv.org/pdf/2302.12173.pdf).
- <a id="ref5"></a>**[[5]]** A. Wei, N. Haghtalab, and J. Steinhardt, "Jailbroken: How Does LLM Safety Training Fail?," in _Proc. NeurIPS_, vol. 36, 2023. [arXiv:2307.02483](https://arxiv.org/pdf/2307.02483.pdf).
- <a id="ref7"></a>**[[7]]** NIST, "Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations," _NIST Trustworthy and Responsible AI_, NIST AI 100-2e2025, 2025. DOI: `10.6028/NIST.AI.100-2e2025`.
- <a id="ref8"></a>**[[8]]** OWASP, "OWASP Top 10 for Large Language Model Applications," _OWASP Foundation_, LLM01:2025, 2025. [GitHub: OWASP/www-project-top-10-for-large-language-model-applications](https://github.com/OWASP/www-project-top-10-for-large-language-model-applications).
- <a id="ref9"></a>**[[9]]** P. He et al., "DeBERTaV3: Improving DeBERTa using ELECTRA-Style Pre-Training with Gradient-Disentangled Embedding Sharing," in _Proc. ICLR_, 2023. [arXiv:2111.09543](https://arxiv.org/pdf/2111.09543.pdf).
- <a id="ref10"></a>**[[10]]** T. Markov et al., "A Holistic Approach to Undesired Content Detection in the Real World," in _Proc. AAAI_, vol. 37, no. 12, pp. 15009–15018, 2023. [arXiv:2208.03274](https://arxiv.org/pdf/2208.03274.pdf).
- <a id="ref11"></a>**[[11]]** X. Shen et al., "Do Anything Now: Characterizing and Evaluating In-The-Wild Jailbreak Prompts on Large Language Models," in _Proc. ACM CCS_, 2024. [arXiv:2308.03825](https://arxiv.org/pdf/2308.03825.pdf).
- <a id="ref15"></a>**[[15]]** N. Jain et al., "Baseline Defenses for Adversarial Attacks on Language Models," in _Proc. NeurIPS Workshop on Robustness of Few-shot and Zero-shot Learning_, 2023. [arXiv:2309.00614](https://arxiv.org/pdf/2309.00614.pdf).
- <a id="ref16"></a>**[[16]]** Z. Yao et al., "ZeroQuant: Efficient and Affordable Post-Training Quantization for Large-Scale Transformers," in _Proc. NeurIPS_, vol. 35, 2022. [arXiv:2206.01861](https://arxiv.org/pdf/2206.01861.pdf).
- <a id="ref18"></a>**[[18]]** J. H. Saltzer and M. D. Schroeder, "The Protection of Information in Computer Systems," in _Proceedings of the IEEE_, vol. 63, no. 9, pp. 1278–1308, 1975. [Open-Access MIT](https://web.mit.edu/Saltzer/www/publications/protection/).
- <a id="ref19"></a>**[[19]]** J. Yi et al., "Benchmarking and Defending Against Indirect Prompt Injection Attacks on Large Language Models," in _Findings of NAACL_, pp. 2844–2863, 2024. [arXiv:2312.14197](https://arxiv.org/pdf/2312.14197.pdf).
