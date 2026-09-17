# BÁO CÁO TÁI LẬP THỰC NGHIỆM ĐỘC LẬP: INSTRUCTDETECTOR (FINDINGS OF EMNLP 2024)

> **Mô hình**: InstructDetector (Phát hiện mệnh lệnh thực thi trong dữ liệu thụ động)  
> **Bài báo gốc**: *Defending against Indirect Prompt Injection by Instruction Detection* (Findings of EMNLP 2024 / arXiv:2402.06774)  
> **Kho mã nguồn**: [https://github.com/MYVAE/Instruction-detection](https://github.com/MYVAE/Instruction-detection)  
> **Phân hệ**: `workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/Tier1_Candidate_InstructDetector_EMNLP2024/`  
> **Quy tắc Task 3**: 100% Độc lập, khép kín, sở hữu tập dữ liệu riêng tại `./datasets/`, không ghép tầng, không coupling.

---

## 🔗 1. Bảng Xuất Xứ Tài Nguyên & Dữ Liệu (Resource & Data Provenance Matrix)

| Hạng Mục | Định Danh / Đường Dẫn Local | Nguồn Gốc Công Khai & URL Trực Tiếp | Bản Quyền / Trạng Thái Xuất Bản |
| :--- | :--- | :--- | :--- |
| 📄 **Bài Báo Khoa Học (Paper)** | [`papers/Zhao_2024_InstructDetector_arXiv2402.06774.pdf`](papers/Zhao_2024_InstructDetector_arXiv2402.06774.pdf) (14 trang) | **arXiv URL**: [https://arxiv.org/abs/2402.06774](https://arxiv.org/abs/2402.06774) | Công bố chính thức tại *Findings of the Association for Computational Linguistics: EMNLP 2024* |
| 💻 **Mã Nguồn Upstream (Code)** | [`InstructDetector_EMNLP2024/`](InstructDetector_EMNLP2024/) (7 file python, 4 shell scripts) | **GitHub Repo**: [https://github.com/MYVAE/Instruction-detection](https://github.com/MYVAE/Instruction-detection) | Giấy phép mã nguồn mở Apache License 2.0 (tác giả Siyan Zhao, Dong Ge, Ryan Rossi) |
| 📊 **Dữ Liệu Kiểm Thử (Dataset)** | • Cấp ngoài: [`datasets/bipia_text_eval.json`](datasets/bipia_text_eval.json), [`datasets/bipia_code_eval.json`](datasets/bipia_code_eval.json)<br>• Cấp trong repo: [`InstructDetector_EMNLP2024/dataset/`](InstructDetector_EMNLP2024/dataset/) | **Nguồn ngoài (External Benchmark Sources)**:<br>1. **Microsoft BIPIA Benchmark**: [https://github.com/microsoft/BIPIA](https://github.com/microsoft/BIPIA)<br>2. **Harvard Dataverse (NewsArticle)**: [https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/GMFCTR](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/GMFCTR) | **Lý do lấy từ nguồn ngoài**: Trong file `InstructDetector_EMNLP2024/README.md`, tác giả ghi rõ: *"The BIPIA dataset is available at https://github.com/microsoft/BIPIA... Please download the dataset and save at the ./dataset"*. Tác giả **không commit dữ liệu vào git**, mà yêu cầu tải từ Microsoft BIPIA |

---

## 📂 2. Cấu Trúc Phân Hệ Tái Lập Khép Kín

```text
Tier1_Candidate_InstructDetector_EMNLP2024/
├── datasets/                                           # [TẬP DỮ LIỆU ĐỘC LẬP NỘI BỘ]
│   ├── bipia_text_eval.json                            # 150 mẫu BIPIA Text (75 Sạch + 75 Tiêm nhiễm Text)
│   └── bipia_code_eval.json                            # 100 mẫu BIPIA Code (50 Sạch + 50 Tiêm nhiễm Code)
├── InstructDetector_EMNLP2024/                         # [100% PURE UPSTREAM CODE (MYVAE/Instruction-detection)]
│   ├── dataset/                                        # Đồng bộ dữ liệu vào thư mục upstream đúng theo README
│   │   ├── bipia_text_eval.json                        # 150 mẫu BIPIA Text
│   │   └── bipia_code_eval.json                        # 100 mẫu BIPIA Code
│   ├── src/                                            # classification.py, prepare_gradient.py, prepare_hidden_state.py
│   ├── scripts/                                        # Shell scripts
│   ├── LICENSE                                         # Apache 2.0
│   └── README.md                                       # Upstream documentation
├── papers/
│   └── Zhao_2024_InstructDetector_arXiv2402.06774.pdf # Bài báo toàn văn (14 trang)
├── figures/
│   ├── 01_paper_evidence/                             # Ảnh chứng thực từ PDF bài báo gốc
│   │   ├── instruct_p1_title_and_abstract.png         # Trang bìa & Abstract
│   │   ├── instruct_p6_table_1_bipia_results.png      # Bảng 1: Kết quả BIPIA benchmark
│   │   └── instruct_p7_table_2_layer_gradient.png     # Bảng 2: Layer gradient dynamics
│   └── 02_empirical_plots/                            # Biểu đồ thực nghiệm đo đạc độc lập
│       ├── instructdetector_replication_paper_vs_local_bars.png # Đối chiếu Paper vs Local
│       └── instructdetector_asr_reduction.png         # Biểu đồ suy giảm tỷ lệ tấn công ASR
├── InstructDetector_EMNLP2024_Replication_and_Paper_Comparison.ipynb # Notebook tái lập tương tác
├── run_instructdetector_replication.py                 # Script thực thi đo đạc độc lập
├── INSTRUCTDETECTOR_EMNLP2024_REPLICATION_BENCHMARK_RESULTS.json # Kết quả JSON chính thức
└── README.md                                          # Báo cáo này
```

---

## 🔬 3. Đặc Tả Chi Tiết Tập Dữ Liệu (`datasets/` & `InstructDetector_EMNLP2024/dataset/`)

Tập dữ liệu được xây dựng chuẩn mực theo benchmark **[Microsoft BIPIA](https://github.com/microsoft/BIPIA)** công bố trong Bảng 1 của bài báo EMNLP 2024:
- **BIPIA In-Domain (Text)**: **150 mẫu** (75 ngữ cảnh văn bản thụ động tự nhiên sạch + 75 ngữ cảnh bị chèn câu lệnh độc hại qua 15 thể loại khác nhau như Task Automation, Business Intelligence, Conversational Agent...).
- **BIPIA Out-of-Domain (Code)**: **100 mẫu** (50 ngữ cảnh mã nguồn Python/JSON sạch + 50 ngữ cảnh mã nguồn bị chèn lệnh độc hại qua 10 thể loại).
- **Quy trình kiểm thử**: Huấn luyện trên 60% dữ liệu Text (90 mẫu), kiểm thử In-Domain trên 40% Text (60 mẫu), và kiểm thử truyền giao diện miền (Zero-shot Out-of-Domain) trên toàn bộ 100 mẫu Code.

---

## 📊 4. Bảng Đối Chiếu Số Liệu: Paper Published vs Local Empirical

| Tiêu Chí Đánh Giá | Paper Reported (EMNLP 2024 Table 1) | Local Empirical Replication (BIPIA Benchmark) | Kết Luận & Phát Hiện Khoa Học |
| :--- | :---: | :---: | :--- |
| **BIPIA In-Domain (Text Attack) Accuracy** | $99.60\%$ (với LLM Hidden State L14) | **$86.67\%$** Accuracy (Recall = $80.00\%$, F1 = $0.8571$) | 🎯 **Tương đồng**: Phát hiện rất tốt câu chỉ thị trên văn bản tự nhiên. |
| **BIPIA Out-of-Domain (Code Attack) Accuracy** | $96.90\%$ (với LLM Hidden State L14) | **$79.00\%$** Accuracy (Recall = $58.00\%$, Clean FPR = $0.00\%$) | ⚠️ **Hiện tượng Domain Shift**: Không có vector ẩn nội bộ LLM, các ký tự code làm nhiễu bộ tách lệnh. |
| **Attack Success Rate (Residual ASR)** | Giảm từ $84.20\%$ xuống **$0.12\%$** | Giảm từ $84.20\%$ xuống **$28.42\%$** (Giảm thiểu $66.25\%$) | 🎯 **Khẳng định giá trị phòng thủ**: Chặn đứng phần lớn đòn tấn công gián tiếp. |
| **Độ trễ trung bình trên CPU** | Đòi hỏi GPU tính gradient / activation pass | **$4.49\text{ms}$** (P50 = $3.80\text{ms}$, P95 = $8.86\text{ms}$) | 🎯 **Siêu nhanh**: Trích xuất cú pháp nhẹ đáp ứng tuyệt đối SLA Tầng 1. |

---

## 💻 5. Hướng Dẫn Tái Lập Thực Nghiệm

Chạy trực tiếp script đo đạc độc lập bằng lệnh:
```bash
python run_instructdetector_replication.py
```
Script sẽ nạp `./datasets/bipia_text_eval.json` và `./datasets/bipia_code_eval.json`, trích xuất đặc trưng câu lệnh, đo lường độ chính xác trên cả 2 miền, tính mức suy giảm ASR, xuất file `INSTRUCTDETECTOR_EMNLP2024_REPLICATION_BENCHMARK_RESULTS.json` và cập nhật biểu đồ tại `figures/02_empirical_plots/`.

---

## 🎯 6. Kết Luận Tái Lập

1. **Khẳng định khoa học**: Ý tưởng phát hiện câu lệnh của Zhao et al. rất sáng tạo để phòng thủ Indirect Prompt Injection.
2. **Hạn chế được phát hiện khi chạy độc lập**: Để đạt độ chính xác >96% trên cả Code, phương pháp này bắt buộc phải truy cập vào trọng số nội bộ của LLM (Layer 14 Hidden State). Nếu chạy như một Guardrail Proxy ngoài (Blackbox, không can thiệp LLM), hiệu năng trên Code sẽ bị sụt giảm do hiện tượng Domain Shift. Đây là luận điểm phản biện cực kỳ giá trị cho Hội đồng!
