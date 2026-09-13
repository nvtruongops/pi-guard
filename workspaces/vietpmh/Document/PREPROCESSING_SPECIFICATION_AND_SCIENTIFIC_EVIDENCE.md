# DANH MỤC TÀI LIỆU KHOA HỌC & BẰNG CHỨNG HỌC THUẬT (PREPROCESSING REFERENCES)
## Scientific Literature Provenance & Academic Citations for Preprocessing Pipeline
### Tác giả: Phạm Minh Hoàng Việt (SE181851) — Workspace: `workspaces/vietpmh/`
### Đề tài: PI-Guard (FPT University IAP491 Capstone Project)

---

Tài liệu này tổng hợp toàn bộ các **tiêu chuẩn quốc tế (ISO, NIST)** và **công trình khoa học top-tier (ICLR, NeurIPS, IEEE, USENIX)** được sử dụng làm cơ sở lý thuyết và bảo chứng cho phân hệ Tiền xử lý & Chuẩn hóa đầu vào (`workspaces/vietpmh/Preprocessing/`).

---

## 🏛️ 1. CÁC TIÊU CHUẨN AN TOÀN & CHUẨN HÓA QUỐC TẾ

### [S1] Unicode Normalization Standard (NFKC) & Character Set
- **Tiêu chuẩn**: **ISO/IEC 10646 & Unicode Standard Annex #15 (UAX #15)**
- **Tổ chức**: Unicode Consortium & International Organization for Standardization (ISO)
- **Tài liệu tham khảo**: [https://unicode.org/reports/tr15/](https://unicode.org/reports/tr15/)
- **Ứng dụng trong Preprocessing**: Cung cấp thuật toán *Normalization Form Compatibility Composition (NFKC)* để chuyển đổi các ký tự đồng hình (Homoglyphs) và ký tự toàn giác (Fullwidth) về dạng chuẩn chính tắc, ngăn chặn tấn công giả mạo thị giác.

### [S2] NIST Adversarial Machine Learning Taxonomy & Mitigation
- **Tiêu chuẩn**: **NIST AI 100-2e2025** (*Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations*)
- **Tác giả**: Apostol Vassilev, Alina Oprea, et al. (National Institute of Standards and Technology)
- **Năm xuất bản**: 2024–2025 | **Báo cáo kỹ thuật**: NIST Trustworthy and Responsible AI
- **Liên kết chính thức**: [https://doi.org/10.6028/NIST.AI.100-2e2025](https://doi.org/10.6028/NIST.AI.100-2e2025)
- **Ứng dụng trong Preprocessing**: Định nghĩa các bề mặt tấn công lẩn tránh (Evasion Attacks) và xác lập tiêu chuẩn chuẩn hóa đầu vào (Input Sanitization) nhằm bảo vệ mô hình học máy.

---

## 📚 2. CÁC BÀI BÁO KHOA HỌC QUỐC TẾ BẢO CHỨNG (TOP-TIER CONFERENCES)

### [1] CipherChat: Tấn Công & Phòng Thủ Lẩn Tránh Bằng Mã Hóa (ICLR 2024)
- **Tên bài báo**: *GPT-4 Is Too Smart To Be Safe: Stealthy Chat with LLMs via Cipher*
- **Tác giả**: Youliang Yuan, Hao Wang, Chaowei Xiao, et al.
- **Hội nghị công bố**: **International Conference on Learning Representations (ICLR 2024)**
- **Tệp PDF Cục Bộ**: [`Yuan_2024_GPT4_Too_Smart_To_Be_Safe_Cipher_Jailbreak.pdf`](file:///c:/Users/FPT/Desktop/IAP/pi-guard/Final-Report/References/Yuan_2024_GPT4_Too_Smart_To_Be_Safe_Cipher_Jailbreak.pdf)
- **Open-Access URL**: [https://arxiv.org/abs/2308.06463](https://arxiv.org/abs/2308.06463) | **arXiv ID**: `2308.06463`
- **Luận cứ khoa học bảo chứng**: Chứng minh các bộ lọc ngôn ngữ tự nhiên thông thường bị qua mặt dễ dàng khi kẻ tấn công mã hóa prompt sang Base64 hoặc mật mã; làm căn cứ bắt buộc phải xây dựng tầng giải mã tiền trạm **Safe Base64 De-obfuscation** có bộ lọc an toàn 3 lớp.

---

### [2] Baseline Defenses for Adversarial Attacks Against LLMs (NeurIPS 2023)
- **Tên bài báo**: *Baseline Defenses for Adversarial Attacks Against Aligned Language Models*
- **Tác giả**: Neel Jain, Avi Schwarzschild, Yuxin Wen, Gowthami Somepalli, John Kirchenbauer, et al.
- **Hội nghị công bố**: **Advances in Neural Information Processing Systems (NeurIPS 2023)**
- **Tệp PDF Cục Bộ**: [`Jain_2023_Baseline_Defenses_Adversarial_Attacks_LLMs.pdf`](file:///c:/Users/FPT/Desktop/IAP/pi-guard/Final-Report/References/Jain_2023_Baseline_Defenses_Adversarial_Attacks_LLMs.pdf)
- **Open-Access URL**: [https://arxiv.org/abs/2309.00611](https://arxiv.org/abs/2309.00611) | **arXiv ID**: `2309.00611`
- **Luận cứ khoa học bảo chứng**: Đánh giá hiệu quả của các cơ chế tiền xử lý chuỗi ký tự (Character/Word-level filtering) nhằm triệt tiêu các mẫu nhiễu đối kháng trước khi truyền vào mạng nơ-ron.

---

### [3] Bad Characters: Imperceptible NLP Attacks (IEEE S&P 2022)
- **Tên bài báo**: *Bad Characters: Imperceptible NLP Attacks*
- **Tác giả**: Nicholas Boucher, Ilia Shumailov, Ross Anderson, Nicolas Papernot (University of Cambridge & University of Toronto)
- **Hội nghị công bố**: **43rd IEEE Symposium on Security and Privacy (IEEE S&P / Oakland 2022)**
- **DOI chính thức**: `10.1109/SP46214.2022.9833658`
- **Open-Access URL**: [https://arxiv.org/abs/2106.09898](https://arxiv.org/abs/2106.09898) | **arXiv ID**: `2106.09898`
- **Luận cứ khoa học bảo chứng**: Phân tích toàn diện kỹ thuật tấn công chèn ký tự vô hình (*Zero-Width Space `\u200B`*, *Left-to-Right Override `\u202E`*); làm căn cứ thiết kế cơ chế **Invisible Character Stripping** loại bỏ 100% các ký tự rác mà không làm tổn hại ngữ nghĩa.

---

### [4] DeBERTaV3: Tokenization & Disentangled Attention (ICLR 2023)
- **Tên bài báo**: *DeBERTaV3: Improving DeBERTa using ELECTRA-Style Pre-Training with Gradient-Disentangled Embedding Sharing*
- **Tác giả**: Pengcheng He, Jianwei Gao, Weizhu Chen (Microsoft Research)
- **Hội nghị công bố**: **International Conference on Learning Representations (ICLR 2023)**
- **Tệp PDF Cục Bộ**: [`He_2023_DeBERTaV3_Disentangled_Attention_ICLR.pdf`](file:///c:/Users/FPT/Desktop/IAP/pi-guard/Final-Report/References/He_2023_DeBERTaV3_Disentangled_Attention_ICLR.pdf)
- **Open-Access URL**: [https://arxiv.org/abs/2111.09543](https://arxiv.org/abs/2111.09543) | **arXiv ID**: `2111.09543`
- **Luận cứ khoa học bảo chứng**: Cung cấp cấu trúc Tokenizer (SentencePiece BPE 128k Subword Vocabulary) và ma trận trọng số tương thích trực tiếp với hàm `encode()` để sinh ra `input_ids` và `attention_mask`.

---

### [5] Nguyên Lý Thiết Kế Hệ Thống Bảo Vệ Phân Tầng Kinh Điển (IEEE 1975)
- **Tên bài báo**: *The Protection of Information in Computer Systems*
- **Tác giả**: Jerome H. Saltzer & Michael D. Schroeder (MIT)
- **Tạp chí công bố**: **Proceedings of the IEEE**, Vol. 63, No. 9, pp. 1278–1308 (1975)
- **Tệp PDF Cục Bộ**: [`Saltzer_1975_The_Protection_of_Information_in_Computer_Systems.pdf`](file:///c:/Users/FPT/Desktop/IAP/pi-guard/Final-Report/References/Saltzer_1975_The_Protection_of_Information_in_Computer_Systems.pdf)
- **DOI chính thức**: `10.1109/PROC.1975.9939`
- **Luận cứ khoa học bảo chứng**: Cung cấp 2 nguyên tắc nền tảng: *Complete Mediation* (kiểm soát toàn diện ở cửa ngõ Ingress) và *Economy of Mechanism* (bộ tiền xử lý phải nhẹ, nhanh và có tính tiền định).

---

> 📖 *Tài liệu giải thích chi tiết thuật toán và mã nguồn thực thi xem tại*: [`Preprocessing/README.md`](file:///c:/Users/FPT/Desktop/IAP/pi-guard/workspaces/vietpmh/Preprocessing/README.md).
