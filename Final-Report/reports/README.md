# THƯ MỤC CÁC BÁO CÁO ĐỊNH KỲ & KẾT QUẢ THỰC NGHIỆM (`Final-Report/reports/`)
## 📊 PI-Guard Periodic Reports, Presentation Decks & Benchmark Metrics

> [!NOTE]
> Thư mục `Final-Report/reports/` là nơi lưu trữ tập trung các sản phẩm báo cáo định kỳ, slide thuyết trình báo cáo tiến độ với Giáo viên Hướng dẫn, sổ theo dõi tiến độ chính thức ĐH FPT (Process Report), và các tệp dữ liệu kết quả thực nghiệm tự động.

---

### 📂 CẤU TRÚC THƯ MỤC `Final-Report/reports/`:

```
Final-Report/reports/
├── PI-GUARD-Present-109.pptx       # Slide báo cáo tiến độ gặp Giáo viên Hướng dẫn ngày 10/09/2026
├── PI_GUARD_PROCESS_REPORT.xlsx   # Sổ theo dõi tiến độ công việc chính thức (FPT IAP491 Process Report)
├── experiment_reports/            # Dữ liệu kết quả thực nghiệm tự động (JSON / Markdown)
│   ├── adversarial_benchmark.json # Kết quả đo độ trễ P50/P95/P99 và độ chính xác trên tập đối kháng
│   └── baseline_test_metrics.json # Kết quả đánh giá mô hình Baseline TF-IDF trên tập test split
└── README.md                      # Hướng dẫn tra cứu & cập nhật các báo cáo
```

---

### 📑 CHI TIẾT TỪNG BÁO CÁO & TÀI LIỆU:

#### 1. Slide Thuyết Trình Tiến Độ (`PI-GUARD-Present-109.pptx`)
- **Mục đích**: Slide báo cáo tiến độ định kỳ phục vụ buổi làm việc trực tiếp với Giáo viên Hướng dẫn (GVHD) vào ngày 10/09/2026.
- **Quy cách**: 22 slides, tỷ lệ 16:9, phong cách thiết kế Dark Slate Navy hiện đại, 100% Academic Grounding (đối chiếu 18 bài báo khoa học).
- **Phân vai**: Do Nguyễn Văn Trường (Leader) và Nguyễn Quí Đức trực tiếp biên soạn và hoàn thiện.
- **Hình ảnh trích xuất**: Toàn bộ 12 sơ đồ kiến trúc và biểu đồ trong slide được lưu trữ chất lượng cao tại [`Final-Report/figures/PI-GUARD-Present-109/`](file:///d:/Work/Do-an/Final-Report/figures/PI-GUARD-Present-109/).

#### 2. Sổ Theo Dõi Tiến Độ FPT IAP491 (`PI_GUARD_PROCESS_REPORT.xlsx`)
- **Mục đích**: Bảng tính Excel chính thức theo mẫu chuẩn của Bộ môn An toàn Thông tin ĐH FPT (IAP491) dùng để nghiệm thu tiến độ hàng tuần với GVHD.
- **Cấu trúc gồm 3 Sheet**:
  1. `Process_Report`: Bảng phân rã công việc WBS gồm 20 đầu việc chuẩn qua 4 cột mốc (Review 1, Review 2, Hội đồng Giữa kỳ, Bảo vệ Tốt nghiệp).
  2. `Personnel_Allocation`: Ma trận phân bổ trách nhiệm chi tiết của 4 thành viên (Trường, Đức, Việt, Phương).
  3. `Meeting_Log`: Nhật ký các cuộc họp với GVHD và nội bộ nhóm.
- **Lệnh cập nhật tự động**:
  ```bash
  python Final-Report/scripts/generate_process_report.py
  ```

#### 3. Báo Cáo Kết Quả Thực Nghiệm (`experiment_reports/`)
- **`adversarial_benchmark.json`**: Ghi nhận độ trễ suy luận (P50, P95, P99) và độ chính xác khi đối mặt với các kỹ thuật làm mờ (Obfuscation: Base64, Leetspeak, Spacing).
  - Lệnh sinh: `python Final-Report/scripts/benchmark.py`
- **`baseline_test_metrics.json`**: Chỉ số Precision, Recall, F1-score và FPR trên tập kiểm thử độc lập.
  - Lệnh sinh: `python Final-Report/scripts/evaluate.py`

---

### 🔄 QUY TRÌNH CẬP NHẬT & ĐỒNG BỘ:

1. **Khi có số liệu benchmark mới**: Chạy `python Final-Report/scripts/benchmark.py` $\rightarrow$ kết quả tự động ghi vào `Final-Report/reports/experiment_reports/adversarial_benchmark.json`.
2. **Khi họp tiến độ xong**: Leader chạy `python Final-Report/scripts/generate_process_report.py` $\rightarrow$ sinh sổ Excel mới tại `Final-Report/reports/PI_GUARD_PROCESS_REPORT.xlsx`.
3. **Đồng bộ Google Sheet**: Chạy `python Final-Report/scripts/sync_google_sheet.py` để đẩy số liệu lên Google Drive phục vụ GVHD theo dõi trực tuyến.
