# 🎓 PI-Guard Final Thesis & Academic Reports (Luận Văn Tốt Nghiệp)

Thư mục này là **nơi lưu trữ bản gốc có thẩm quyền cao nhất (Single Source of Truth)** của Luận văn Tốt nghiệp Đồ án Capstone (IAP491) - Đại học FPT.

---

## 📂 Cấu Trúc Tài Liệu

```
Final-Report/thesis/
├── FINAL_THESIS.md                                      # Toàn văn Khóa luận Tốt nghiệp (Được biên dịch tự động)
├── Review1_Problem_Definition_and_Threat_Model.md        # Báo cáo Chuyên đề Đợt 1 (Định nghĩa bài toán & Threat Model)
├── FPT_IAP491_Capstone_Guidelines_and_Rubrics_Summary.md # Tóm tắt tiêu chuẩn đánh giá & Rubric IAP491 ĐH FPT
├── chapters/                                            # Các chương riêng biệt của Luận văn
│   ├── 01_Introduction.md                               # Chương 1: Giới thiệu & Bối cảnh bài toán
│   ├── 02_Literature_Review.md                          # Chương 2: Tổng quan nghiên cứu & Cơ sở lý thuyết
│   └── README.md                                        # Quy chuẩn viết từng chương
└── README.md                                            # Hướng dẫn này
```

---

## ⚙️ Quy Trình Biên Dịch & Xuất Bản

1. **Biên dịch Luận văn**:
   Chạy lệnh:
   ```bash
   python scripts/compile_thesis.py
   ```
   Lệnh này sẽ tự động gộp các chương từ `chapters/`, chèn trang bìa chuẩn FPT University, chèn danh mục tài liệu tham khảo từ `Final-Report/References/REFERENCES_LOG.md` và xuất ra `FINAL_THESIS.md`.

2. **Đồng bộ lên Cổng Web GitHub Pages**:
   Chạy lệnh:
   ```bash
   python scripts/build_docs_portal.py
   ```
   Script sẽ tự động đọc từ `Final-Report/thesis/`, chuẩn hóa liên kết và sao chép sang `docs/thesis/` để hiển thị trên cổng web GitHub Pages (MkDocs Material).

---

## 🔬 Lưu Ý Phương Pháp Luận: Phân Biệt 2 Giai Đoạn Thực Nghiệm
- **Thực nghiệm Tái lập Y văn (Chương 2)**: Đo đạc giới hạn/điểm vỡ của các mô hình có sẵn (TF-IDF, ProtectAI, Meta Prompt-Guard) để làm bằng chứng khoa học cho 3 Research Gaps $\to$ tiền đề mở ra Chương 3 Đề xuất Mô hình.
- **Thực nghiệm Nghiệm thu Mô hình Nhóm (Chương 4 / Report No.4)**: Chạy đối chuẩn trên mô hình Champion của nhóm (Two-Tier Cascade) để chứng minh tính vượt trội so với các baselines ở Chương 2.
- **Luồng Slide Báo cáo Tiến độ (Meeting Deck)**: Luôn đi theo logic quy nạp (*Evidence-First*): Thực nghiệm Baseline trước $\to$ Đề xuất Mô hình nhóm sau.
