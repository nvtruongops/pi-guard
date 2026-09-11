# **BÁO CÁO KỸ THUẬT CHUYÊN SÂU & HỒ SƠ ĐIỀU HÀNH NHIỆM VỤ MEETING 4**

## (TASK FOR MEETING 4 — MASTER TECHNICAL GATEWAY)

### ĐỀ TÀI: A MACHINE-LEARNING GUARDRAIL FOR DETECTING PROMPT INJECTION AND JAILBREAK ATTACKS ON LLM APPLICATIONS (PI-GUARD)

**Tác giả**: Nguyễn Văn Trường (Leader — MSSV: `SE182034`) | **Workspace**: `workspaces/truongnv/`
**Căn cứ đề tài**: Bản đăng ký đề tài [`CAPSTONE PROJECT REGISTER.md`](file:///d:/Work/Do-an/CAPSTONE%20PROJECT%20REGISTER.md) & Biên bản [`Final-Report/Meeting/Meeting 4_10_09_26.md`](file:///d:/Work/Do-an/Final-Report/Meeting/Meeting%204_10_09_26.md)
**Thư mục chuyên đề chi tiết**: [`workspaces/truongnv/reports/task_for_meeting_4/`](file:///d:/Work/Do-an/workspaces/truongnv/reports/task_for_meeting_4/)

---

## 📑 MỤC LỤC ĐIỀU PHỐI TRUNG TÂM

1. [BỐI CẢNH &amp; Ý KIẾN CHỈ ĐẠO CỐT LÕI TỪ GVHD TRẦN VĂN NINH](#1-bối-cảnh--ý-kiến-chỉ-đạo-cốt-lõi-từ-gvhd-trần-văn-ninh)
2. [HỆ THỐNG 4 BÁO CÁO KỸ THUẬT CHUYÊN SÂU (NAVIGATION HUB)](#2-hệ-thống-4-báo-cáo-kỹ-thuật-chuyên-sâu-navigation-hub)
3. [BẢNG ĐỐI CHUẨN TỔNG HỢP 2 MÔ HÌNH PHÒNG THỦ (EXECUTIVE SCORECARD)](#3-bảng-đối-chuẩn-tổng-hợp-2-mô-hình-phòng-thủ-executive-scorecard)
4. [QUY TRÌNH THỰC NGHIỆM TÁI LẬP HỆ THỐNG 5 BƯỚC (B1–B5)](#4-quy-trình-thực-nghiệm-tái-lập-hệ-thống-5-bước-b1b5)
5. [TÀI LIỆU THAM KHẢO HỌC THUẬT CỐT LÕI (REFERENCES)](#5-tài-liệu-tham-khảo-học-thuật-cốt-lõi-references)

---

## 1. BỐI CẢNH & Ý KIẾN CHỈ ĐẠO CỐT LÕI TỪ GVHD TRẦN VĂN NINH

Tại buổi báo cáo trực tiếp tại campus ngày 10/09/2026 sau khi nhóm trình bày bộ slide [`reports/PI-GUARD-Present-109.pptx`](file:///d:/Work/Do-an/Final-Report/reports/PI-GUARD-Present-109.pptx), **Thầy Trần Văn Ninh (GVHD)** đã đưa ra định hướng chiến lược mang tính bước ngoặt:

> _"Một mô hình dùng trong đồ án học thuật chuẩn mực phải tìm được mã nguồn và tập dữ liệu công bố, tải về và chạy được trên máy để nắm chắc các thiết lập siêu tham số và số liệu thực nghiệm. Khi đó mới đủ cơ sở khoa học để đưa vào đồ án và đề xuất cải tiến. Trước buổi họp tuần sau (Meeting 5), cả 4 thành viên bắt buộc phải chạy độc lập được 2 mô hình tham khảo trên máy cá nhân và có số liệu thực nghiệm cụ thể!"_

Để giải quyết triệt để 4 yêu cầu của Thầy đồng thời tối ưu hóa khả năng theo dõi độc lập, hồ sơ kỹ thuật Meeting 4 được tổ chức theo kiến trúc **Master Gateway** kết hợp cùng **4 Báo cáo kỹ thuật chuyên sâu** trong thư mục [`workspaces/truongnv/reports/task_for_meeting_4/`](file:///d:/Work/Do-an/workspaces/truongnv/reports/task_for_meeting_4/).

---

## 2. HỆ THỐNG 4 BÁO CÁO KỸ THUẬT CHUYÊN SÂU (NAVIGATION HUB)

Quý Thầy Cô và các thành viên nhóm có thể truy cập trực tiếp vào từng báo cáo chuyên đề chi tiết dưới đây:

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                 BẢNG ĐIỀU HƯỚNG 4 NHIỆM VỤ KỸ THUẬT CHUYÊN SÂU                                                   │
├──────┬──────────────────────────────────────────┬────────────────────────────────────────────────────────┬───────────────────────────────────────┤
│ STT  │ Tên Nhiệm Vụ Kỹ Thuật (Chuyên Đề)        │ Tệp Báo Cáo Chi Tiết                                   │ Ánh Xạ Chương Luận Văn Tốt Nghiệp     │
├──────┼──────────────────────────────────────────┼────────────────────────────────────────────────────────┼───────────────────────────────────────┤
│ **1**│ **Phân Biệt Prompt Injection vs Jailbreak**│ [`TASK_1_PROMPT_INJECTION_VS_JAILBREAK.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/task_for_meeting_4/TASK_1_PROMPT_INJECTION_VS_JAILBREAK.md) │ **Chapter 1** (Intro) & **Chapter 2** (Lit)│
│      │ • Phân biệt tầng ứng dụng vs mô hình     │                                                        │ • Bối cảnh lỗ hổng bảo mật LLM        │
│      │ • Không gian token phẳng $X = S \Vert U$ │                                                        │ • Cơ sở lý thuyết phân loại học       │
│      │ • Ma trận so sánh 6 tiêu chí toàn diện   │                                                        │                                       │
├──────┼──────────────────────────────────────────┼────────────────────────────────────────────────────────┼───────────────────────────────────────┤
│ **2**│ **Phương Thức Tấn Công & 2 Mô Hình**     │ [`TASK_2_ATTACK_VECTORS_AND_MODELS.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/task_for_meeting_4/TASK_2_ATTACK_VECTORS_AND_MODELS.md)     │ **Chapter 2** (Background & Models)   │
│      │ • 2 Kênh Ingress: Prompt Text vs File RAG│                                                        │ • Bề mặt tấn công Ingress             │
│      │ • Toán học song song 2 luồng TF-IDF      │                                                        │ • Khảo sát các mô hình phòng thủ      │
│      │ • DeBERTa-v3 Disentangled Attention      │                                                        │                                       │
├──────┼──────────────────────────────────────────┼────────────────────────────────────────────────────────┼───────────────────────────────────────┤
│ **3**│ **Datasets, Checkpoints & Tái Lập B1–B5**│ [`TASK_3_REPRODUCIBILITY_AND_DATASETS.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/task_for_meeting_4/TASK_3_REPRODUCIBILITY_AND_DATASETS.md) │ **Chapter 4** (Experimental Setup)    │
│      │ • Kho dữ liệu, Checkpoint & Repos mở     │                                                        │ • Môi trường thực nghiệm              │
│      │ • Lộ trình 5 bước thực nghiệm cá nhân    │                                                        │ • Bảng đối chuẩn kết quả tái lập      │
│      │ • Bảng đối chuẩn đo đạc vs bài báo gốc   │                                                        │                                       │
├──────┼──────────────────────────────────────────┼────────────────────────────────────────────────────────┼───────────────────────────────────────┤
│ **4**│ **Các Giải Pháp Cải Tiến Của PI-Guard**  │ [`TASK_4_PIGUARD_IMPROVEMENTS.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/task_for_meeting_4/TASK_4_PIGUARD_IMPROVEMENTS.md)         │ **Chapter 3** (Proposed Methodology)  │
│      │ • Group-Aware Splitting (MD5 Hash)       │                                                        │ • Thiết kế kiến trúc phân tầng        │
│      │ • Dynamic Class-Weighted Loss            │                                                        │ • Thuật toán định tuyến bất định      │
│      │ • Two-Tier Uncertainty Routing           │                                                        │                                       │
└──────┴──────────────────────────────────────────┴────────────────────────────────────────────────────────┴───────────────────────────────────────┘
```

---

## 3. BẢNG ĐỐI CHUẨN TỔNG HỢP 2 MÔ HÌNH PHÒNG THỦ (EXECUTIVE SCORECARD)

Bảng tổng hợp đối chuẩn giữa Mô hình Baseline Tầng 1 và Mô hình Deep Semantic Tầng 2:

| Tiêu Chí So Sánh                 |   Tầng 1: Classical ML Baseline (TF-IDF)   | Tầng 2: Deep Transformer (DeBERTa-v3 INT8) |           Hệ Thống Tích Hợp Phân Tầng PI-Guard           |
| :------------------------------- | :----------------------------------------: | :----------------------------------------: | :------------------------------------------------------: | --- | --- |
| **Không gian đặc trưng**         |  Dual-stream: Word (1–3) + Char_wb (3–5)   | Disentangled Attention (Content + Rel-Pos) |                 Hai lớp bổ trợ lẫn nhau                  |
| **Số chiều / Tham số**           |         $60,000$ chiều vector thưa         |  $86\text{M}$ tham số (Đã lượng hóa INT8)  |                Tối ưu hóa bộ nhớ kết hợp                 |
| **Dung lượng bộ nhớ RAM**        |           $\approx 25\text{ MB}$           | $\approx 140\text{ MB}$ (Nén 72% từ 500MB) |        $\approx 165\text{ MB}$ (Cực nhẹ trên CPU)        |
| **Độ trễ suy luận P95 (CPU)**    |             **$2.8\text{ms}$**             |            **$14.5\text{ms}$**             | **$< 22\text{ms}$** (Trung bình $\approx 7.15\text{ms}$) |     |     |
| **Khả năng kháng Leetspeak**     |   Rất tốt ($\cos > 0.45$ nhờ `char_wb`)    |     Xuất sắc (BPE Tokenizer + Context)     |                Đa tầng bảo vệ chuyên sâu                 |
| **Kháng Indirect Injection RAG** | Trung bình (Dễ bị vượt qua khi đảo vị trí) |  Xuất sắc (Bóc tách Content-to-Position)   |           Bắt trọn vẹn mọi vị trí chèn mã độc            |
| **Điểm cân bằng vận hành**       |    Tốc độ cực nhanh cho 70% mẫu rõ ràng    |  Phân tích ngữ nghĩa sâu cho 30% mẫu khó   |               **Tối ưu Pareto toàn diện**                |

---

## 4. QUY TRÌNH THỰC NGHIỆM TÁI LẬP HỆ THỐNG 5 BƯỚC (B1–B5)

Quy trình thực nghiệm 5 bước chuẩn hóa (Standardized 5-Step Experimental Pipeline) được thiết kế khép kín nhằm bảo đảm tính độc lập và khả năng tái lập 100% kết quả trên môi trường cục bộ:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│      LỘ TRÌNH 5 BƯỚC THỰC NGHIỆM TÁI LẬP TOÀN BỘ PIPELINE ĐỒ ÁN PI-GUARD               │
│            (Đảm bảo tính độc lập, khả năng tái lập 100% trên môi trường cục bộ)        │
├──────┬───────────────────────────────────┬─────────────────────────────────────────────┤
│ Bước │ Hạng mục thực nghiệm bắt buộc     │ Lệnh thực thi mẫu trên PowerShell           │
├──────┼───────────────────────────────────┼─────────────────────────────────────────────┤
│ B1   │ **Tải dữ liệu từ Hugging Face**   │ `python workspaces/<member>/scripts/download_dataset.py --config Final-Report/notebooks/configs/data.yaml` │
├──────┼───────────────────────────────────┼─────────────────────────────────────────────┤
│ B2   │ **Tiền xử lý & Group-Aware Split**│ `python workspaces/<member>/scripts/preprocess.py --splits_dir Final-Report/notebooks/data/splits`        │
├──────┼───────────────────────────────────┼─────────────────────────────────────────────┤
│ B3   │ **Huấn luyện Baseline TF-IDF**    │ `python workspaces/<member>/scripts/train.py --model baseline --config Final-Report/notebooks/configs/training.yaml` │
├──────┼───────────────────────────────────┼─────────────────────────────────────────────┤
│ B4   │ **Nạp DeBERTa & Lượng hóa INT8**  │ `python workspaces/<member>/scripts/quantize_onnx.py --model_dir Final-Report/notebooks/models/deberta_int8`       │
├──────┼───────────────────────────────────┼─────────────────────────────────────────────┤
│ B5   │ **Đối chiếu chéo & Xuất JSON**    │ Xuất file `experiment_reports/<member>_metrics.json` để so sánh độ ổn định tại Meeting 5.   │
└──────┴───────────────────────────────────┴─────────────────────────────────────────────┘
```

## 5. TÀI LIỆU THAM KHẢO HỌC THUẬT CỐT LÕI (REFERENCES)

- <a id="ref3"></a>**[[3]]** F. Perez and I. Ribeiro, "Ignore Previous Prompt: Attack Techniques For Language Models," in _Proc. NeurIPS ML Safety Workshop_, 2022. [arXiv:2211.09527](https://arxiv.org/pdf/2211.09527.pdf).
- <a id="ref4"></a>**[[4]]** K. Greshake et al., "Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection," in _Proc. ACM AISec_, 2023. [arXiv:2302.12173](https://arxiv.org/pdf/2302.12173.pdf).
- <a id="ref5"></a>**[[5]]** A. Wei, N. Haghtalab, and J. Steinhardt, "Jailbroken: How Does LLM Safety Training Fail?," in _Proc. NeurIPS_, vol. 36, 2023. [arXiv:2307.02483](https://arxiv.org/pdf/2307.02483.pdf).
- <a id="ref7"></a>**[[7]]** NIST, "Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations," _NIST Trustworthy and Responsible AI_, NIST AI 100-2e2025, 2025. DOI: `10.6028/NIST.AI.100-2e2025`.
- <a id="ref8"></a>**[[8]]** OWASP, "OWASP Top 10 for Large Language Model Applications," _OWASP Foundation_, LLM01:2025, 2025. [GitHub: OWASP/www-project-top-10-for-large-language-model-applications](https://github.com/OWASP/www-project-top-10-for-large-language-model-applications).
- <a id="ref9"></a>**[[9]]** P. He et al., "DeBERTaV3: Improving DeBERTa using ELECTRA-Style Pre-Training with Gradient-Disentangled Embedding Sharing," in _Proc. ICLR_, 2023. [arXiv:2111.09543](https://arxiv.org/pdf/2111.09543.pdf).
- <a id="ref11"></a>**[[11]]** X. Shen et al., "Do Anything Now: Characterizing and Evaluating In-The-Wild Jailbreak Prompts on Large Language Models," in _Proc. ACM CCS_, 2024. [arXiv:2308.03825](https://arxiv.org/pdf/2308.03825.pdf).
- <a id="ref15"></a>**[[15]]** N. Jain et al., "Baseline Defenses for Adversarial Attacks on Language Models," in _Proc. NeurIPS Workshop on Robustness of Few-shot and Zero-shot Learning_, 2023. [arXiv:2309.00614](https://arxiv.org/pdf/2309.00614.pdf).
- <a id="ref16"></a>**[[16]]** Z. Yao et al., "ZeroQuant: Efficient and Affordable Post-Training Quantization for Large-Scale Transformers," in _Proc. NeurIPS_, vol. 35, 2022. [arXiv:2206.01861](https://arxiv.org/pdf/2206.01861.pdf).
- <a id="ref19"></a>**[[19]]** J. Yi et al., "Benchmarking and Defending Against Indirect Prompt Injection Attacks on Large Language Models," in _Proc. ACM KDD_, 2025. [arXiv:2312.14197](https://arxiv.org/pdf/2312.14197.pdf).
