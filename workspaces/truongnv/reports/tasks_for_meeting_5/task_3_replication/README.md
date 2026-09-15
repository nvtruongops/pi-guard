# HƯỚNG DẪN TÁI LẬP THỰC NGHIỆM TASK 3 — TRỌNG TÂM PIGUARD (ACL 2025)
**PI-Guard Capstone Project — Workspace: `workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/`**

Tài liệu này hướng dẫn đầy đủ cấu trúc thư mục, môi trường ảo Python 3.10 độc lập, mã nguồn và tập dữ liệu đã được cài đặt và kiểm định thực nghiệm phục vụ tái lập mô hình **PIGuard (ACL 2025 - DeBERTa-v3-base)** làm trọng tâm duy nhất của Task 3.

---

## 📂 1. Cấu Trúc Phân Hệ Tái Lập (Directory Structure)

```text
workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/
├── papers/                                         # [TÀI LIỆU KHOA HỌC MỎ NEO - BẢN PDF CHÍNH THỨC]
│   └── PIGuard_ACL2025_arXiv2410.22770.pdf         # Paper PIGuard (ACL 2025 Long Paper, 2.07 MB) — Mô hình lõi DeBERTa-v3
│
├── PIGuard_ACL2025/                                # [PHÂN HỆ CHÍNH: PIGuard DeBERTa-v3 — ĐÃ CÀI ĐẶT & KIỂM ĐỊNH]
│   ├── .venv/                                      # Môi trường ảo Python 3.10 riêng biệt (PyTorch, Transformers)
│   ├── quick_test_piguard.py                       # Script kiểm thử suy luận nhanh trên 5 kịch bản mẫu
│   ├── eval_hf.py                                  # Script đánh giá mô hình trực tiếp qua HuggingFace pipeline
│   ├── eval.py                                     # Script đánh giá offline qua checkpoint cục bộ
│   ├── train.py                                    # Script huấn luyện với cơ chế Mitigating Over-defense for Free (MOF)
│   ├── PIGuard.py                                  # Định nghĩa kiến trúc phân loại DeBERTa-v3
│   ├── params.py / util.py                         # Tiện ích tiền xử lý dữ liệu và cấu hình tham số
│   └── datasets/                                   # [TẬP DỮ LIỆU ĐỐI CHUẨN ĐẦY ĐỦ CÓ SẴN]
│       ├── train.json                              # Dữ liệu huấn luyện gốc (43.78 MB, thu thập từ 20 nguồn mở)
│       ├── valid.json                              # Dữ liệu validation (144 mẫu)
│       ├── NotInject_one.json                      # Kiểm thử Over-defense cấp độ 1 trigger word (26.9 KB)
│       ├── NotInject_two.json                      # Kiểm thử Over-defense cấp độ 2 trigger words (30.8 KB)
│       ├── NotInject_three.json                    # Kiểm thử Over-defense cấp độ 3 trigger words (36.8 KB)
│       ├── BIPIA_text.json                         # Tập tấn công gián tiếp qua văn bản (6.4 KB)
│       ├── BIPIA_code.json                         # Tập tấn công gián tiếp qua mã nguồn (16.4 KB)
│       └── wildguard.json                          # Tập lành tính Wildguard Benign (472.5 KB)
│
├── verify_replication_assets.py                    # Script kiểm định tự động tính toàn vẹn 100% tài nguyên
└── README.md                                       # Tài liệu hướng dẫn này
```

---

## 📑 2. Nguyên Tắc Trọng Tâm Duy Nhất & Đánh Giá Tầng 1 Sau Khi Hoàn Thành

1. **Trọng tâm tuyệt đối của Task 3 (Phần 1)**:
   - Chạy đúng, kiểm chứng thực nghiệm độc lập và đo đạc đầy đủ các chỉ số của mô hình mỏ neo cốt lõi **DeBERTa-v3-base (PIGuard ACL 2025)** trên máy cá nhân để nắm chắc cơ chế chống Over-defense (MOF).
2. **Loại bỏ Ayub (CAMLIS 2024) khỏi phân hệ Task 3**:
   - Đã loại bỏ hoàn toàn mã nguồn và bộ dữ liệu gần 600MB của Ayub khỏi Task 3 vì **chưa chắc sẽ dùng Ayub (CAMLIS 2024)**.
   - Ayub chỉ là một trong các phương án khảo sát lý thuyết, không được gán ghép sớm làm tăng kích thước và gây loãng trọng tâm thực nghiệm.
3. **Đánh giá Tầng 1 sau khi chạy xong DeBERTa-v3-base**:
   - Chỉ khi nào hoàn tất kiểm chứng DeBERTa-v3-base, nhóm mới bắt đầu đánh giá báo cáo chuyên sâu:
     👉 [`workspaces/truongnv/reports/TIER_1_CANDIDATE_MODELS_RESEARCH.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/TIER_1_CANDIDATE_MODELS_RESEARCH.md)
   - Báo cáo này khảo sát 5 ứng viên (trong đó đã chỉ ra Ayub bị nghẽn độ trễ MiniLM 8–15ms và đề xuất tối ưu là TF-IDF N-Grams + Calibrated Logistic Regression với độ trễ < 1.0ms trên CPU).

---

## 🚀 3. Hướng Dẫn Thực Thi PIGuard (ACL 2025)

### Cách 0: Khám Phá & Đối Chiếu Số Liệu Qua Jupyter Notebook (Khuyến Nghị Hàng Đầu)
Mở trực tiếp notebook trong VS Code hoặc JupyterLab để khám phá 11 phân hệ, đối chiếu bảng số liệu Table 1/Table 7 của bài báo và xem toàn bộ 4 biểu đồ trực quan hóa xuất bản:
👉 **[`PIGuard_ACL2025/PIGuard_ACL2025_Replication_and_Paper_Comparison.ipynb`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/PIGuard_ACL2025/PIGuard_ACL2025_Replication_and_Paper_Comparison.ipynb)**

* **Kernel Jupyter**: Chọn kernel đã cấu hình sẵn `Python (PIGuard ACL 2025)` (`piguard-acl2025`).
* **Tính năng chính của Notebook**:
  - Tải tức thì toàn bộ số liệu đo đạc độc lập trên 1.579 mẫu (`LOAD_PRECOMPUTED = True`) hoặc bật `LOAD_PRECOMPUTED = False` để chạy suy luận trực tiếp.
  - Bảng đối chuẩn chi tiết từng tập dữ liệu với số liệu công bố gốc trong bài báo ACL 2025 (xác nhận khớp 100% trên NotInject-2, NotInject-3 và WildGuard Benign).
  - Ma trận nhầm lẫn (Confusion Matrix) trên 144 mẫu thẩm định cân bằng.
  - 4 biểu đồ khoa học tự động lưu vào `figures/`: Biểu đồ cột đối đầu Paper vs Local, đường suy giảm độ nhạy theo từ khóa, hồ sơ độ trễ CPU và heatmap ma trận nhầm lẫn.
  - Tự động đồng bộ kết quả cấu trúc vào `PIGUARD_REPLICATION_BENCHMARK_RESULTS.json` và xuất bảng Markdown nhúng Luận văn.

### Cách 1: Chạy kiểm thử suy luận nhanh 5 kịch bản mẫu (Quick Test)
Môi trường ảo Python 3.10 đã được cấu hình sẵn trong `PIGuard_ACL2025/.venv`. Chạy trực tiếp:
```powershell
powershell -NoProfile -Command "& d:\Work\Do-an\workspaces\truongnv\reports\task_3_replication\PIGuard_ACL2025\.venv\Scripts\python.exe d:\Work\Do-an\workspaces\truongnv\reports\task_3_replication\PIGuard_ACL2025\quick_test_piguard.py"
```

### Cách 2: Chạy đánh giá toàn diện trên tập NotInject & BIPIA
```powershell
powershell -NoProfile -Command "& d:\Work\Do-an\workspaces\truongnv\reports\task_3_replication\PIGuard_ACL2025\.venv\Scripts\python.exe d:\Work\Do-an\workspaces\truongnv\reports\task_3_replication\PIGuard_ACL2025\eval_hf.py --dataset_root d:\Work\Do-an\workspaces\truongnv\reports\task_3_replication\PIGuard_ACL2025\datasets"
```

### Cách 3: Chạy kiểm định toàn bộ tài nguyên Task 3
```powershell
python d:\Work\Do-an\workspaces\truongnv\reports\task_3_replication\verify_replication_assets.py
```
