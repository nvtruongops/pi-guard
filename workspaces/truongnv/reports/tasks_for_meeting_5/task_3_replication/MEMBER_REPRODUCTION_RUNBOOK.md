# **SỔ TAY QUY TRÌNH TÁI LẬP THỰC NGHIỆM CHUẨN HÓA CHO 4 THÀNH VIÊN**
## (MEMBER REPRODUCTION RUNBOOK — BEFORE MEETING 5)
### ĐỀ TÀI: A MACHINE-LEARNING GUARDRAIL FOR DETECTING PROMPT INJECTION AND JAILBREAK ATTACKS ON LLM APPLICATIONS (PI-GUARD)
**Tác giả**: Nguyễn Văn Trường (Leader — MSSV: `SE182034`) | **Workspace**: `workspaces/truongnv/`  
**Đối tượng áp dụng**: Cả 4 thành viên nhóm (Nguyễn Văn Trường, Nguyễn Quí Đức, Phạm Minh Hoàng Việt, Đỗ Đoàn Duy Phương)  
**Căn cứ chỉ đạo**: Kết luận cuộc họp Meeting 4 ngày 10/09/2026 [`Final-Report/Meeting/Meeting 4_10_09_26.md`](file:///d:/Work/Do-an/Final-Report/Meeting/Meeting%204_10_09_26.md)  
**Cổng điều phối phòng thí nghiệm**: [`workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/README.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/README.md) | **Báo cáo kỹ thuật gốc**: [`../task_reports/TASK_3_REPRODUCIBILITY_AND_DATASETS.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_reports/TASK_3_REPRODUCIBILITY_AND_DATASETS.md)

---

> [!IMPORTANT]
> ### ⚡ CHỈ ĐẠO CỐT LÕI TỪ GVHD TRẦN VĂN NINH (HỌP MEETING 4 NGÀY 10/09/2026)
> > *"Trước buổi họp tuần sau (Meeting 5), cả 4 thành viên bắt buộc phải chạy độc lập được 2 mô hình tham khảo trên máy cá nhân và có số liệu thực nghiệm cụ thể!"*
> 
> Sổ tay này cung cấp hướng dẫn từng bước chi tiết (Copy & Paste) để từng thành viên chạy thực nghiệm trong sandbox cá nhân (`workspaces/<member>/`), ghi nhận số liệu và xuất tệp báo cáo JSON chuẩn phục vụ báo cáo với Thầy Ninh.

---

## 1. KỊCH BẢN A: TÁI LẬP MÔ HÌNH 2 — PIGUARD DEBERTA-V3 (HAO LI ET AL., ACL 2025 [[2]](#ref2))

### Bước 1: Di chuyển vào sandbox cá nhân & Clone repo
```powershell
# Chú ý: Thay <member> bằng thư mục cá nhân của mình (truongnv, ducnq, vietpmh, phuongddd)
cd d:\Work\Do-an\workspaces\<member>\

# Clone repo mã nguồn chính thức của bài báo ACL 2025
git clone https://github.com/leolee99/PIGuard.git
cd PIGuard

# Cài đặt thư viện phụ thuộc
pip install torch transformers datasets scikit-learn
```

### Bước 2: Chạy đánh giá Checkpoint Hugging Face trên dữ liệu benchmark
```powershell
# Chạy script đánh giá chính thức của bài báo
python eval_hf.py --dataset_root datasets
```

### Bước 3: Quan sát & Ghi nhận kết quả
Màn hình console sẽ xuất ra bảng kết quả chính thức:
- **Over-defense ACC**: Đối chiếu xem có đạt xấp xỉ **$88.3\%$** như công bố trong bài báo hay không.
- **Benign ACC**: Đối chiếu xem có đạt xấp xỉ **$97.2\%$** hay không.
- **Injection ACC**: Đối chiếu xem có đạt xấp xỉ **$98.7\%$** hay không.
- **Độ trễ CPU FP32**: Ghi nhận thời gian suy luận trên CPU cá nhân (thường dao động khoảng **$35 - 50\text{ms}$**).

---

## 2. KỊCH BẢN B: TÁI LẬP MÔ HÌNH 1 — EMBEDDING ML BASELINE (AYUB & MAJUMDAR, CAMLIS 2024 [[1]](#ref1))

### Bước 1: Di chuyển vào sandbox cá nhân & Clone repo
```powershell
cd d:\Work\Do-an\workspaces\<member>\

# Clone repo mã nguồn chính thức của bài báo CAMLIS 2024
git clone https://github.com/AhsanAyub/malicious-prompt-detection.git
cd malicious-prompt-detection

# Cài đặt thư viện phụ thuộc
pip install pandas scikit-learn xgboost sentence-transformers
```

### Bước 2: Chạy trích xuất vector nhúng MiniLM và phân loại
```powershell
# Chạy kịch bản phân loại nhị phân
python binary_classification.py
```

### Bước 3: Quan sát & Ghi nhận kết quả
- Đối chiếu **Accuracy (99.4%)** và **F1-Score (0.987)** với Bảng 2 của bài báo.
- Ghi nhận thời gian trích xuất embedding và huấn luyện Random Forest trên CPU.

---

## 3. KỊCH BẢN C (KHUYẾN NGHỊ NHANH): SỬ DỤNG PHÒNG THÍ NGHIỆM ĐÓNG GÓI SẴN NGAY TẠI ĐÂY (`task_3_replication/`)

Để tiết kiệm thời gian tải model và tránh lỗi xung đột thư viện, nhóm trưởng đã đóng gói sẵn toàn bộ môi trường ảo `.venv`, 5 repo public nguyên bản và 89/89 assets cục bộ ngay tại thư mục [`task_3_replication/`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/).

Các thành viên chỉ cần kích hoạt môi trường và chạy script kiểm định tự động:
```powershell
# 1. Di chuyển vào phòng thí nghiệm tái lập
cd d:\Work\Do-an\workspaces\truongnv\reports\tasks_for_meeting_5\task_3_replication

# 2. Kích hoạt môi trường ảo dùng chung
.\.venv\Scripts\Activate.ps1

# 3. Chạy kiểm định toàn bộ 89 tài nguyên thực nghiệm
python verify_replication_assets.py

# 4. Chạy kiểm thử nhanh mô hình PIGuard DeBERTa-v3 trên CPU
python Tier2_PIGuard_ACL2025\quick_test_piguard.py

# 5. Chạy benchmark đối chuẩn PIGuard trên 5 tập dữ liệu
python Tier2_PIGuard_ACL2025\eval_piguard_replication.py
```

### 📸 Bằng chứng kết quả mong đợi khi tái lập thành công:
Khi chạy thành công, kết quả của thành viên phải khớp chính xác với Bảng đối chuẩn dưới đây:

![Bảng đối chuẩn kết quả đo đạc cục bộ vs bài báo](Tier2_PIGuard_ACL2025/figures/02_empirical_plots/local_vs_paper_scorecard.png)
*Hình 1: Bảng kết quả chuẩn mong đợi khi thành viên chạy tái lập PIGuard DeBERTa-v3 (NotInject Acc đạt $88.3\%$, Malicious Injection Acc đạt $98.7\%$).*

![Biểu đồ cột so sánh Paper vs Local](Tier2_PIGuard_ACL2025/figures/02_empirical_plots/piguard_replication_paper_vs_local_bars.png)
*Hình 2: Biểu đồ trực quan hóa đối chiếu giữa số liệu bài báo và số liệu đo đạc thực tế trên máy cá nhân.*

---

## 4. XUẤT TỆP BÁO CÁO KẾT QUẢ ĐO ĐẠC CÁ NHÂN (JSON REPORT)

Mỗi thành viên sau khi chạy xong sẽ lưu số liệu vào file JSON cá nhân tại thư mục:  
`Final-Report/reports/experiment_reports/<member>_metrics.json` theo mẫu chuẩn sau:

```json
{
  "member_id": "<Mã SV>",
  "member_name": "<Họ và Tên>",
  "hardware_specs": {
    "cpu": "Intel Core i7-12700H / AMD Ryzen 7",
    "ram_gb": 16,
    "os": "Windows 11 64-bit"
  },
  "ayub_embedding_results": {
    "accuracy": 0.994,
    "f1_score": 0.987,
    "precision": 0.989,
    "recall": 0.985
  },
  "piguard_deberta_results": {
    "notinject_overdefense_accuracy": 0.883,
    "malicious_detection_accuracy": 0.987,
    "benign_accuracy": 0.972,
    "cpu_fp32_latency_ms": 42.50
  },
  "verification_status": "PASS",
  "ready_for_meeting_5": true
}
```

---

## 5. CHECKLIST ĐỐI CHIẾU CHÉO NỘI BỘ TRƯỚC CUỘC HỌP MEETING 5

- [ ] Thành viên đã clone hoặc chạy được cả 2 bài báo refer trên máy cá nhân (`PIGuard` và `malicious-prompt-detection`).
- [ ] Thành viên đã chụp ảnh màn hình terminal xuất ra số liệu đo đạc (accuracy và latency).
- [ ] Thành viên đã nắm chắc các bộ siêu tham số của 2 mô hình (backbone, learning rate, epochs, batch size).
- [ ] Tệp JSON báo cáo đo đạc đã được commit vào thư mục cá nhân.

---

## 6. TÀI LIỆU THAM KHẢO HỌC THUẬT (REFERENCES)

<a id="ref1"></a>
- **[[1]]** M. A. Ayub and S. Majumdar, "Embedding-based classifiers can detect prompt injection attacks," in *Proceedings of the Conference on Applied Machine Learning in Information Security (CAMLIS 2024)*, Arlington, VA, USA, Oct. 2024. [arXiv:2410.22284](https://arxiv.org/pdf/2410.22284).

<a id="ref2"></a>
- **[[2]]** H. Li, X. Liu, N. Zhang, and C. Xiao, "PIGuard: Prompt Injection Guardrail via Mitigating Overdefense for Free," in *Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (ACL 2025)*, Vienna, Austria, 2025. [arXiv:2410.22770](https://arxiv.org/pdf/2410.22770) | [ACL Anthology](https://aclanthology.org/2025.acl-long.1468.pdf).
