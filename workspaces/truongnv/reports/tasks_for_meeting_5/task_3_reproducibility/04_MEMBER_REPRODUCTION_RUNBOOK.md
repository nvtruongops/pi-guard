# **CHUYÊN ĐỀ 4: SỔ TAY QUY TRÌNH TÁI LẬP THỰC NGHIỆM CHUẨN HÓA CHO 4 THÀNH VIÊN**
## (MEMBER REPRODUCTION RUNBOOK — BEFORE MEETING 5)
### ĐỀ TÀI: A MACHINE-LEARNING GUARDRAIL FOR DETECTING PROMPT INJECTION AND JAILBREAK ATTACKS ON LLM APPLICATIONS (PI-GUARD)
**Tác giả**: Nguyễn Văn Trường (Leader — MSSV: `SE182034`) | **Workspace**: `workspaces/truongnv/`  
**Đối tượng áp dụng**: Cả 4 thành viên nhóm (Nguyễn Văn Trường, Nguyễn Quí Đức, Phạm Minh Hoàng Việt, Đỗ Đoàn Duy Phương)  
**Căn cứ chỉ đạo**: Biên bản cuộc họp Meeting 4 ngày 10/09/2026 [`Final-Report/Meeting/Meeting 4_10_09_26.md`](file:///d:/Work/Do-an/Final-Report/Meeting/Meeting%204_10_09_26.md)  
**Cổng điều phối chuyên đề Task 3**: [`workspaces/truongnv/reports/tasks_for_meeting_5/task_3_reproducibility/README.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_reproducibility/README.md)

---

> [!IMPORTANT]
> ### ⚡ CHỈ ĐẠO CỐT LÕI TỪ GVHD TRẦN VĂN NINH (HỌP MEETING 4 NGÀY 10/09/2026)
> > *"Trước buổi họp tuần sau (Meeting 5), cả 4 thành viên bắt buộc phải chạy độc lập được 2 mô hình tham khảo trên máy cá nhân và có số liệu thực nghiệm cụ thể!"*
> 
> Sổ tay này cung cấp hướng dẫn từng bước chi tiết (Copy & Paste) để từng thành viên chạy thực nghiệm trong sandbox cá nhân (`workspaces/<member>/`), ghi nhận số liệu và xuất tệp báo cáo JSON chuẩn phục vụ báo cáo với Thầy Ninh.

---

## 1. KỊCH BẢN A: TÁI LẬP MÔ HÌNH 2 — PIGUARD DEBERTA-V3 (HAO LI ET AL., ACL 2025)

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

## 2. KỊCH BẢN B: TÁI LẬP MÔ HÌNH 1 — EMBEDDING ML BASELINE (AYUB & MAJUMDAR, CAMLIS 2024)

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

## 3. XUẤT TỆP BÁO CÁO KẾT QUẢ ĐO ĐẠC CÁ NHÂN (JSON REPORT)

Mỗi thành viên sau khi chạy xong 2 kịch bản trên sẽ lưu số liệu vào file JSON cá nhân tại thư mục:  
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

## 4. CHECKLIST ĐỐI CHIẾU CHÉO NỘI BỘ TRƯỚC CUỘC HỌP MEETING 5

- [ ] Thành viên đã clone và chạy được cả 2 bài báo refer trên máy cá nhân (`PIGuard` và `malicious-prompt-detection`).
- [ ] Thành viên đã chụp ảnh màn hình terminal xuất ra số liệu đo đạc (accuracy và latency).
- [ ] Thành viên đã nắm chắc các bộ siêu tham số của 2 mô hình (backbone, learning rate, epochs, batch size).
- [ ] Tệp JSON báo cáo đo đạc đã được commit vào thư mục cá nhân.
