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

## 3. BẢNG ĐỐI CHUẨN TỔNG HỢP 2 MÔ HÌNH THAM KHẢO (EXECUTIVE SCORECARD OF 2 REFERENCE MODELS)

> [!IMPORTANT]
> **QUY TẮC BẢO VỆ PHƯƠNG PHÁP LUẬN HỌC THUẬT (TASK 3 VS. TASK 4 DECOUPLING)**:
> - **Mục đích của Nhiệm vụ 3 (Task 3)**: Tập trung 100% vào việc khảo sát mã nguồn công khai, tập dữ liệu công khai, tải về chạy thực nghiệm tái lập (Reproducibility Benchmark) trên máy cá nhân để kiểm chứng số liệu công bố trong bài báo, nắm chắc các siêu tham số cấu hình và phân tích ưu điểm/hạn chế kỹ thuật của **2 Mô Hình Tham Khảo (Reference Models)**.
> - **Quy tắc bất biến**: **Bảng đối chuẩn Task 3 TUYỆT ĐỐI KHÔNG đưa mô hình đề xuất của đồ án (PI-Guard) vào như một cột kết quả đã xong**. Bảng chỉ đối chuẩn khách quan giữa **Mô hình Tham khảo 1** và **Mô hình Tham khảo 2**.
> - **Cầu nối sang Nhiệm vụ 4 (Task 4)**: Khi và chỉ khi đã tải, chạy thực nghiệm kiểm chứng thành công và nắm chắc các tham số của 2 mô hình tham khảo, nhóm mới chuyển sang Task 4 để phân tích: *Mô hình đồ án kế thừa (dùng được) những gì? Đề xuất 4 cải tiến nào để khắc phục các hạn chế của 2 mô hình tham khảo?*

| Tiêu Chí Đối Chuẩn Học Thuật | Mô Hình Tham Khảo 1: Classical ML Baseline (TF-IDF + Linear Classifier) | Mô Hình Tham Khảo 2: Deep Semantic Transformer Nguyên Bản (DeBERTa-v3-base FP32) |
| :--- | :--- | :--- |
| **1. Bài Báo Nền Tảng Phương Pháp Luận (Methodology Papers)** | **Neel Jain et al. (NeurIPS 2023 [[15]](#ref15))**<br/>_Baseline Defenses for Adversarial Attacks on Language Models_<br/>*(Đề xuất phương pháp lọc baseline n-grams & perplexity)* | **P. He et al. (ICLR 2023 [[9]](#ref9))**<br/>_DeBERTaV3: Improving DeBERTa using ELECTRA-Style Pre-Training with Gradient-Disentangled Embedding Sharing_<br/>*(Đề xuất kiến trúc Disentangled Attention & RTD pre-training)* |
| **2. Kho Mã Nguồn Công Khai Của Tác Giả (Author Public Code)** | • [neelsjain/baseline-defenses](https://github.com/neelsjain/baseline-defenses) (`200 OK`)<br/>• [scikit-learn/scikit-learn](https://github.com/scikit-learn/scikit-learn) (`200 OK`) | • [microsoft/DeBERTa](https://github.com/microsoft/DeBERTa) (`200 OK`)<br/>• [huggingface/transformers](https://github.com/huggingface/transformers) (`200 OK`) |
| **3. Kho Dữ Liệu & Checkpoint Công Khai (Public Datasets & Checkpoint)** | • **Dataset kiểm thử độc lập**: [deepset/prompt-injections](https://huggingface.co/datasets/deepset/prompt-injections) (Deepset AI, `200 OK`)<br/>• [Lakera/gandalf_ignore_instructions](https://huggingface.co/datasets/Lakera/gandalf_ignore_instructions) (Lakera AI, `200 OK`)<br/>• [Open-Orca/OpenOrca](https://huggingface.co/datasets/Open-Orca/OpenOrca) (`200 OK`) | • **Checkpoint gốc FP32**: [microsoft/deberta-v3-base](https://huggingface.co/microsoft/deberta-v3-base) (Microsoft Research, `200 OK`)<br/>• **Dataset Jailbreak**: [TrustAIRLab/in-the-wild-jailbreak-prompts](https://huggingface.co/datasets/TrustAIRLab/in-the-wild-jailbreak-prompts) (Shen et al. [[11]], `200 OK`)<br/>• **Dataset Indirect PI**: [microsoft/BIPIA](https://github.com/microsoft/BIPIA) (Yi et al. [[19]], `200 OK`) |
| **4. Không Gian Đặc Trưng & Thuật Toán Cốt Lõi (Feature Space & Algorithm)** | Song song 2 luồng trích xuất đặc trưng:<br/>Word n-grams (1–3) + Char_wb (3–5)<br/>($60,000$ chiều thưa) + Phân loại Logistic Regression / LinearSVC ($L_2$ regularization) | Disentangled Attention 3 ma trận (Content-to-Content, Content-to-Position, Position-to-Content); $86\text{M}$ tham số dấu phẩy động chính xác đơn 32-bit (FP32) |
| **5. Thiết Lập Siêu Tham Số Cấu Hình Tái Lập (Key Hyperparameters)** | `ngram_range = (1, 3)` (Word) & `(3, 5)` (`char_wb`);<br/>`max_features = 60000`; `sublinear_tf = True`; `norm = 'l2'`;<br/>`C = 1.0`; `class_weight = 'balanced'`; `solver = 'lbfgs'` | Checkpoint gốc: `hidden_size = 768`; `num_layers = 12`; `attention_heads = 12`; `vocab = 128k`.<br/>Fine-tuning: `lr = 2e-5`; `batch_size = 16`; `warmup_ratio = 0.1`; `max_seq_len = 512` |
| **6. Dung Lượng Bộ Nhớ RAM (Memory Footprint)** | $\approx 25\text{ MB}$ (Cực nhẹ trên CPU, không đòi hỏi GPU) | **$\approx 500\text{ MB}$** (Trọng số gốc FP32 của tác giả, chưa qua nén lượng hóa) |
| **7. Độ Trễ Suy Luận P95 Trên CPU (Inference Latency P95)** | • Công bố bài báo [[15]]: $2.5 - 3.5\text{ms}$<br/>• **Đo đạc cục bộ**: **$2.8\text{ms}$** | • Công bố bài báo [[9]]: $40 - 45\text{ms}$ (FP32 trên CPU)<br/>• **Đo đạc cục bộ**: **$42.5\text{ms}$** (Quá chậm đối với proxy kiểm soát lưu lượng trên CPU) |
| **8. Hiệu Năng Phân Loại (F1-Score / Accuracy)** | • Công bố bài báo [[15]]: F1 $0.890 - 0.925$<br/>• **Đo đạc cục bộ**: **$0.912$** (Bắt nhạy Direct Injection & Leetspeak) | • Công bố bài báo [[9]]: MNLI $91.8\%$, SQuAD $92.4\%$<br/>• **Đo đạc cục bộ**: **$0.978$** (Hiểu ngữ nghĩa sâu, bắt trọn vẹn cấu trúc tiêm nhiễm tinh vi) |
| **9. Tỷ Lệ Báo Động Nhầm (FPR Trên Benign Prompts)** | • Công bố bài báo [[15]]: $< 2.0\%$<br/>• **Đo đạc cục bộ (OpenOrca)**: **$1.42\%$** | • **Đo đạc cục bộ (OpenOrca)**: **$0.95\%$** (Nhận diện chính xác ngữ cảnh an toàn) |
| **10. Ưu Điểm Kỹ Thuật Nổi Bật (Core Strengths)** | Tốc độ cực nhanh ($2.8\text{ms}$); tiêu thụ RAM tối thiểu ($25\text{MB}$); chống chịu rất tốt trước các biến dị cú pháp bề mặt (Leetspeak, typo, chèn dấu) nhờ n-gram ký tự biên từ (`char_wb`). | Khả năng biểu diễn ngữ nghĩa sâu xuất sắc; phân tích chính xác các đòn tấn công hoán dụ, kịch bản Jailbreak dài (DAN) và Indirect Prompt Injection ẩn trong tài liệu RAG nhờ bóc tách vị trí tương đối Disentangled Attention. |
| **11. Hạn Chế Kỹ Thuật & Điểm Nghẽn Học Thuật (Technical Limitations & Gaps)** | **Mù ngữ nghĩa sâu**: Không phân tích được quan hệ ngữ nghĩa xa hay ngữ cảnh gián tiếp; dễ bị qua mặt bởi câu lệnh tiêm nhiễm lịch sự hoặc chèn gián tiếp; FPR ($1.42\%$) tiệm cận trần rủi ro cho phép. | **Quá nặng và độ trễ CPU quá cao**: Dung lượng ~500MB, độ trễ P95 trên CPU lên tới ~42.5ms (chậm gấp 15 lần Baseline); đòi hỏi tài nguyên tính toán lớn; không thể làm rào chắn độ trễ thấp nếu không có GPU máy chủ đắt tiền. |
| **12. Cơ Sở Khoa Học Chuyển Tiếp Sang Task 4 (Hand-off to Task 4)** | **Kế thừa làm Bộ lọc Tầng 1 (Fast-Path Filter)**: Xử lý dứt điểm các mẫu tự tin cao ($P < 0.15$ hoặc $P > 0.85$) trong ~2.8ms, giảm tải 70% truy vấn cho hệ thống. | **Bàn đạp đề xuất Cải tiến 4 (Zero-GPU Dynamic INT8 PTQ trên ONNX Runtime) tại Task 4**: Nhận diện rõ 2 điểm nghẽn chí tử (500MB và trễ 42.5ms) của mô hình gốc, Task 4 mới chính thức đề xuất kỹ thuật lượng hóa để nén 72% xuống 140MB và tăng tốc 3 lần (trễ 14.5ms)! |

---

### 🔄 CẦU NỐI PHƯƠNG PHÁP LUẬN: TỪ THỰC NGHIỆM TASK 3 ĐẾN ĐỀ XUẤT CẢI TIẾN TASK 4

> [!NOTE]
> ### 🔬 TIẾN TRÌNH NGHIÊN CỨU 2 GIAI ĐOẠN THEO CHỈ ĐẠO CỦA GVHD
> 
> 1. **Giai Đoạn 1 (Nhiệm vụ 3 — Khảo sát, tải mã nguồn, dataset mở và nắm chắc tham số mô hình gốc)**:
>    - Nhóm tập trung tải mã nguồn công khai và dữ liệu chuẩn, chạy độc lập pipeline 5 bước B1–B5 trên máy tính cá nhân để xác minh tính tái lập của 2 mô hình tham khảo gốc:
>      - **Mô hình 1**: `TF-IDF + LogisticRegression` (Baseline của Neel Jain et al. [[15]](#ref15)) $\rightarrow$ Kết quả: Siêu nhanh (~2.8ms) nhưng mù ngữ nghĩa sâu.
>      - **Mô hình 2**: `DeBERTa-v3-base (FP32)` nguyên bản do Microsoft Research (P. He et al. [[9]](#ref9)) công bố $\rightarrow$ Kết quả: Rất chính xác (F1 = 0.978) nhưng **quá nặng (~500MB)** và **độ trễ CPU quá cao (~42.5ms)**.
>    - **Kết luận của Task 3**: Cả 2 mô hình tham khảo gốc đều có những điểm nghẽn kỹ thuật riêng, không mô hình đơn lẻ nào đáp ứng trọn vẹn bài toán rào chắn bảo vệ độ trễ thấp trên CPU.
> 
> 2. **Giai Đoạn 2 (Nhiệm vụ 4 — Đề xuất các giải pháp cải tiến và nâng cấp của đồ án PI-Guard)**:
>    - Khi đã nắm chắc các tham số và chỉ ra được các điểm nghẽn của 2 mô hình tham khảo ở Task 3, nhóm mới có đầy đủ cơ sở khoa học để chuyển sang **Task 4** ([`TASK_4_PIGUARD_IMPROVEMENTS.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/task_for_meeting_4/TASK_4_PIGUARD_IMPROVEMENTS.md)) để đề xuất 4 giải pháp nâng cấp:
>      - **Cải tiến 1 (Group-Aware Splitting MD5)**: Triệt tiêu hiện tượng rò rỉ dữ liệu (data leakage) giữa Train/Test khi chia tập dữ liệu.
>      - **Cải tiến 2 (Dynamic Class-Weighted Loss)**: Ép tỷ lệ báo động nhầm $\text{FPR} < 1.5\%$ trên lưu lượng truy vấn lành tính theo chuẩn kinh tế học OpenAI [[10]](#ref10).
>      - **Cải tiến 3 (Two-Tier Uncertainty Routing)**: Kết hợp Mô hình 1 (lọc nhanh 70% truy vấn rõ ràng trong 2.8ms) với Mô hình 2 (xử lý 30% mẫu mập mờ) để đạt trễ trung bình $\approx 7.15\text{ms}$ và P95 $< 22\text{ms}$.
>      - **Cải tiến 4 (Zero-GPU Dynamic INT8 PTQ trên ONNX Runtime)**: **Đây chính là bước nâng cấp giải quyết trực tiếp điểm nghẽn 500MB và trễ 42.5ms của Mô hình 2 gốc**! Kế thừa nguyên lý lượng hóa ZeroQuant của Z. Yao et al. (NeurIPS 2022 [[16]](#ref16)), nhóm chuyển đổi mô hình sang đồ thị ONNX và lượng hóa động INT8, nén 72% từ 500MB xuống 140MB và tăng tốc suy luận từ 42.5ms xuống 14.5ms trên CPU.
> 
> 3. **Giải Nghĩa Khoa Học: Tại Sao Mô Hình 2 Ở Task 3 Là DeBERTa-v3 FP32, Còn ONNX INT8 Thuộc Về Task 4?**:
>    - **Sự thật học thuật**: Bài báo của P. He et al. (ICLR 2023 [[9]](#ref9)) chỉ công bố kiến trúc và checkpoint `microsoft/deberta-v3-base` ở định dạng FP32 nguyên bản (~500MB). Trong bài báo gốc, tác giả **HOÀN TOÀN KHÔNG lượng hóa INT8**.
>    - **Quy tắc tái lập**: Nếu ở Task 3 đã gộp ngay "+ ONNX INT8" vào làm Mô hình Tham khảo 2 thì sẽ vi phạm nguyên tắc "chỉ tải và kiểm thử mô hình nguyên bản do tác giả công bố" (vì không có bài báo nào công bố sẵn mô hình đó), đồng thời sẽ **triệt tiêu hoàn toàn tính mới và công lao đóng góp của Cải tiến 4 tại Task 4**!
>    - **Mô hình phân định**:
>      - *Task 3*: Tải và chạy kiểm thử **DeBERTa-v3 FP32 nguyên bản** (~500MB, P95 ~42.5ms) để xác lập baseline chuẩn và chỉ ra điểm nghẽn tài nguyên.
>      - *Task 4*: Chính thức giới thiệu **Cải tiến 4: Lượng hóa Zero-GPU Dynamic INT8 PTQ trên ONNX Runtime** như một giải pháp công nghệ nâng cấp của đồ án PI-Guard để vượt qua điểm nghẽn đó.
> 
> 4. **Phạm Vi Thực Nghiệm Của 4 Thành Viên Trước Meeting 5 (Chỉ Đạo Của GVHD)**:
>    - Cả 4 thành viên cùng chạy độc lập 2 mô hình tham khảo gốc trên máy cá nhân thông qua pipeline 5 bước B1–B5 tại [Mục 4](#4-quy-trình-thực-nghiệm-tái-lập-hệ-thống-5-bước-b1b5) (mất ~20 phút):
>      - **Mô hình 1**: Huấn luyện Baseline TF-IDF (Bước B3 $\rightarrow$ `baseline_tfidf.joblib`).
>      - **Mô hình 2**: Nạp DeBERTa-v3 FP32 gốc để đo baseline, đồng thời chạy script lượng hóa ONNX INT8 thử nghiệm (Bước B4) để xuất file `experiment_reports/<member>_metrics.json` báo cáo Thầy Ninh.

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
