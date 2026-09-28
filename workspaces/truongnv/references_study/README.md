# PHÂN VÙNG TÀI NGUYÊN NGHIÊN CỨU THAM KHẢO (REFERENCES STUDY & HARNESSES)
## Bộ Khung Kiểm Thử Đối Kháng & Hồ Sơ Bằng Chứng Phủ Định Bổ Trợ

- **Đơn vị thực hiện**: Nhóm nghiên cứu sinh viên Đề tài PI-Guard (IAP491) — Đại học FPT
- **Tác giả**: Nguyễn Văn Trường (Leader — MSSV: `SE182034`)
- **Giảng viên hướng dẫn**: ThS. Trần Văn Ninh
- **Vị trí lưu trữ**: [`workspaces/truongnv/references_study/`](file:///d:/Work/Do-an/workspaces/truongnv/references_study/)
- **Thời điểm hoàn thiện**: 28/09/2026

---

> [!NOTE]
> **Tuyên bố về Tình trạng Học thuật & Mục đích Phân vùng**:  
> Thư mục này được thiết lập nhằm phân định rạch ròi giữa **Kho Mô hình Thực nghiệm Đối chuẩn Trực tiếp ([`workspaces/truongnv/replications/`](file:///d:/Work/Do-an/workspaces/truongnv/replications/))** và **Các Tài nguyên Phục vụ Nghiên cứu Bổ trợ (References Study)**.  
> Việc tách bạch này đảm bảo đồ án tuân thủ nghiêm ngặt phương pháp luận nghiên cứu:
> 1. Tránh lỗi phân loại danh mục (**Category Error**): Không xếp lẫn công cụ sinh tấn công (attack harness) với bộ phân loại phòng thủ (guardrail classifier).
> 2. Bảo tồn hồ sơ khoa học (**Scientific Transparency**): Lưu giữ đầy đủ mã nguồn và kết quả đo đạc của các mô hình bị nhóm đề xuất loại bỏ (Negative Baseline Dossier) làm vũ khí phản biện khi bảo vệ đồ án tốt nghiệp trước Hội đồng.

---

## 📂 CẤU TRÚC PHÂN VÙNG NGHIÊN CỨU THAM KHẢO

```text
references_study/
├── README.md               # Văn kiện định danh và hướng dẫn tra cứu phân vùng
├── harnesses/              # Bộ khung sinh tấn công & sinh dữ liệu kiểm chuẩn đối kháng
│   └── JailbreakBench_Chao_NeurIPS2024/
│       ├── papers/         # Paper gốc NeurIPS 2024 (Patrick Chao et al.)
│       ├── upstream/       # Mã nguồn chính thức từ repo JailbreakBench
│       ├── datasets/       # Dữ liệu kiểm chuẩn D3 (100 harmful prompts)
│       └── reports/        # Báo cáo xuất xứ dữ liệu PROVENANCE.json
└── rejected_baselines/     # Hồ sơ các mô hình do nhóm đề xuất loại bỏ (Negative Baselines)
    └── Tier1_REJECTED_Ayub_CAMLIS2024/
        ├── papers/         # Paper gốc CAMLIS 2024 (Ahsan Ayub et al.)
        ├── upstream/       # Mã nguồn gốc character n-gram + sentence embedding
        ├── datasets/       # Tập dữ liệu kiểm thử NotInject & WildGuard
        └── reports/        # Kết quả đo đạc thực tế chứng minh FPR 58.41%
```

---

## 🔬 CHI TIẾT TỪNG TÀI NGUYÊN NGHIÊN CỨU THAM KHẢO

### 1. Phân mục `harnesses/` — Khung Sinh Tấn Công & Kiểm Thử Đối Kháng
- **Tài nguyên**: [`JailbreakBench_Chao_NeurIPS2024/`](file:///d:/Work/Do-an/workspaces/truongnv/references_study/harnesses/JailbreakBench_Chao_NeurIPS2024/)
- **Bài báo gốc**: Patrick Chao et al., *"JailbreakBench: An Open Robustness Benchmark for Jailbreaking Large Language Models"*, NeurIPS 2024 Datasets and Benchmarks Track.
- **Vai trò học thuật**:
  - `JailbreakBench` **không phải là một mô hình phân loại bảo vệ (Classifier)**.
  - Đây là một **Evaluation Harness** chuẩn mực quốc tế dùng để sinh ra các cuộc tấn công đối kháng (PAIR, GCG, TAP) và cung cấp bộ dữ liệu 100 hành vi nguy hiểm có gắn nhãn (*JBB-Behaviors*).
  - Nhóm nghiên cứu sử dụng tài nguyên này để trích xuất tập dữ liệu **$D_3$ (Jailbreak Benchmark)** phục vụ kiểm thử sức bền cho toàn bộ các mô hình thực nghiệm tại `replications/`.
  - Việc đặt JailbreakBench tại `references_study/harnesses/` giúp tránh tuyệt đối lỗi Category Error.

---

### 2. Phân mục `rejected_baselines/` — Hồ Sơ Bằng Chứng Phủ Định (Negative Baseline Dossiers)
- **Tài nguyên**: [`Tier1_REJECTED_Ayub_CAMLIS2024/`](file:///d:/Work/Do-an/workspaces/truongnv/references_study/rejected_baselines/Tier1_REJECTED_Ayub_CAMLIS2024/)
- **Bài báo gốc**: Ahsan Ayub & Subash Majumdar, *"Towards Robust Detection of Prompt Injection Attacks: An Empirical Study"*, CAMLIS 2024.
- **Vai trò học thuật**:
  - Mô hình kết hợp Character n-gram và Sentence Embedding (MiniLM) với bộ phân loại Random Forest.
  - Kết quả thực nghiệm đo đạc thực tế của nhóm tại Meeting 5 chỉ ra 2 tử huyệt:
    1. **Tử huyệt Overdefense**: Chặn nhầm tới **$58.41\%$** trên tập dữ liệu lành tính NotInject (FPR quá cao, vi phạm tiêu chuẩn thiết kế $\text{FPR} < 1.5\%$).
    2. **Tử huyệt độ trễ**: Thời gian trích xuất vector embedding bằng MiniLM trên CPU mất **$11.02\text{ms}$**, quá chậm cho bộ lọc tầng 1 (FastFilter SLA $\le 2.0\text{ms}$).
  - Nhóm sinh viên đã đề xuất loại bỏ mô hình này khỏi danh mục ứng viên chính thức trong báo cáo gửi GVHD (ThS. Trần Văn Ninh).
  - Hồ sơ này được bảo tồn nguyên vẹn 100% tại `references_study/rejected_baselines/` để làm luận chứng phản biện trước Hội đồng khi được chất vấn: *"Tại sao nhóm dùng TF-IDF mà không dùng Sentence Embedding của Ayub 2024?"*.

---

## 🛠️ CÔNG CỤ TỰ ĐỘNG HỖ TRỢ TRA CỨU ĐA ĐƯỜNG DẪN

Hệ sinh thái công cụ kiểm toán của nhóm được lập trình sẵn cơ chế tra cứu kép (Dual-Path Fallback):
- [`audit_6_vs_11_models_integrity.py`](file:///d:/Work/Do-an/workspaces/truongnv/scripts/audit_6_vs_11_models_integrity.py): Tự động phát hiện vị trí của `JailbreakBench` và `Tier1_REJECTED_Ayub` tại `references_study/` và xác thực $100\%$ tính toàn vẹn (Zero Mock Data).
- [`prepare_cross_dataset_suite.py`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_6/scripts/prepare_cross_dataset_suite.py): Tự động nạp bộ mẫu $D_3$ từ `references_study/harnesses/JailbreakBench_Chao_NeurIPS2024/datasets/`.
- [`verify_replication_assets.py`](file:///d:/Work/Do-an/workspaces/truongnv/replications/verify_replication_assets.py): Xác thực 243 assets và mã băm SHA-256 trên cả hai phân vùng.
