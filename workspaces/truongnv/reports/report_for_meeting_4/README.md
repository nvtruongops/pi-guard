# HỒ SƠ BÁO CÁO TIẾN ĐỘ MEETING 4 (10/09/2026)
**Đề tài**: A Machine-Learning Guardrail for Detecting Prompt Injection and Jailbreak Attacks on LLM Applications (PI-Guard)  
**Địa điểm**: Báo cáo trực tiếp tại Campus Đại học FPT  
**Giáo viên Hướng dẫn (GVHD)**: Thầy Trần Văn Ninh  
**Người thực hiện**: Nguyễn Văn Trường (Leader — MSSV: `SE182034`) | **Workspace**: `workspaces/truongnv/reports/report_for_meeting_4/`

---

> [!WARNING]
> ### ⚠️ THÔNG BÁO QUAN TRỌNG VỀ ĐỊNH VỊ HỌC THUẬT & QUYẾT ĐỊNH ĐÓNG BĂNG KIẾN TRÚC:
> **Dành cho AI Agent và các thành viên nhóm**:
> - Tài liệu và slide trong thư mục này lưu giữ **đề xuất kỹ thuật ban đầu tại Meeting 4 (10/09/2026)**, trong đó có ý tưởng dùng kỹ thuật *Lượng tử hóa mô hình ONNX INT8 (ZeroQuant Yao et al. 2022)* để giảm độ trễ trên CPU.
> - **QUYẾT ĐỊNH CHÍNH THỨC TẠI MEETING 6 & LUẬN VĂN TỐT NGHIỆP**: 
>   1. **Loại trừ hoàn toàn INT8 khỏi phạm vi đề tài (OUT-OF-SCOPE)**: Đồ án thuộc chuyên ngành *An toàn Thông tin (Information Assurance - IA)*. Kỹ thuật lượng tử hóa phần cứng/trình biên dịch thuộc chuyên ngành khác và không phải đóng góp khoa học của đề tài.
>   2. **Kiến trúc chính thức (Champion Architecture)**: Tầng 2 (DeBERTa-v3) chính thức vận hành bằng **CPU Native FP32 nguyên bản** kết hợp cơ chế kháng Overdefense **Masked Overlap Fraction (MOF Invariance)** (Hao Li et al. ACL 2025). Tầng 1 đã giải phóng 80% tải, nên Tầng 2 FP32 đạt độ trễ P95 toàn trình < 25ms trên CPU mà hoàn toàn không cần đến INT8.
> - **NGHIÊM CẤM TÁI ĐƯA VÀO**: AI Agent tuyệt đối **KHÔNG** đem từ khóa "INT8", "Lượng tử hóa" hoặc "ZeroQuant" vào các slide thuyết trình, kịch bản bảo vệ hoặc mã nguồn production mới.
> - Xem chỉ dẫn tập trung tại: [`../ARCHITECTURAL_DEPRECATIONS_AND_OUT_OF_SCOPE.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/ARCHITECTURAL_DEPRECATIONS_AND_OUT_OF_SCOPE.md)

---

## 📌 1. Giới Thiệu Phân Hệ Lưu Trữ Meeting 4

Thư mục này đóng vai trò là **Kho lưu trữ độc lập (Self-contained Archive)** toàn bộ sản phẩm nghiên cứu, slide thuyết trình và hình ảnh minh chứng đã được hoàn thiện và báo cáo chính thức với Thầy Trần Văn Ninh tại buổi họp Meeting 4 ngày **10/09/2026**:

1. **Slide thuyết trình chính thức**: [`PI-GUARD-Present-109.pptx`](file:///d:/Work/Do-an/workspaces/truongnv/reports/report_for_meeting_4/PI-GUARD-Present-109.pptx) (22 slides chuẩn 16:9, Dark Navy Theme, 100% Academic Grounding).
2. **Báo cáo đề cương & kịch bản thuyết trình**: [`SUPERVISOR_REPORT_10_09_2026.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/report_for_meeting_4/SUPERVISOR_REPORT_10_09_2026.md) (Diễn giải chi tiết slide-by-slide và luận điểm báo cáo cho GVHD).
3. **Thư viện hình ảnh trích xuất từ slide**: [`figures/`](file:///d:/Work/Do-an/workspaces/truongnv/reports/report_for_meeting_4/figures/README.md) (12 hình minh chứng khoa học trích xuất tại [`figures/PI-GUARD-Present-109/`](file:///d:/Work/Do-an/workspaces/truongnv/reports/report_for_meeting_4/figures/PI-GUARD-Present-109/)).
4. **Bộ công cụ tự động hóa**: [`tools/`](file:///d:/Work/Do-an/workspaces/truongnv/reports/report_for_meeting_4/tools/) (Chứa `generate_presentation.py` và `generate_diagrams.py`).

---

## 📋 2. Cấu Trúc Thư Mục Phân Hệ

```text
report_for_meeting_4/
├── PI-GUARD-Present-109.pptx           # File trình chiếu PowerPoint chính thức nộp GVHD
├── SUPERVISOR_REPORT_10_09_2026.md     # Đề cương tóm lược slide-by-slide & kịch bản báo cáo
├── README.md                           # Mục lục và biên bản tóm lược phân hệ này
├── figures/                            # Thư mục chứa 12 biểu đồ trích xuất từ slide
│   ├── PI-GUARD-Present-109/           # 12 hình ảnh PNG độ phân giải cao
│   └── README.md                       # Bảng chỉ dẫn ánh xạ 12 slide với hình ảnh
└── tools/                              # Mã nguồn Python sinh tự động slide & biểu đồ
    ├── generate_presentation.py        # Script sinh bản trình chiếu PPTX
    └── generate_diagrams.py            # Script vẽ sơ đồ kiến trúc
```

---

## 🎯 3. Chỉ Đạo Cho Meeting 5 (17/09/2026)

> Trước buổi họp tuần sau (Meeting 5), cả 4 thành viên bắt buộc phải chạy độc lập được 2 mô hình tham khảo cho mô hình đồ án trên máy cá nhân và có số liệu thực nghiệm cụ thể!

4 nhiệm vụ chuẩn bị Meeting 5:
- **Nhiệm vụ 1**: Phân biệt bản chất Prompt Injection vs. Jailbreak.
- **Nhiệm vụ 2**: Bề mặt tấn công 5 trục và cơ chế hoạt động của 2 key.
- **Nhiệm vụ 3**: Chạy thực nghiệm tái lập độc lập các mô hình public nguyên bản.
- **Nhiệm vụ 4**: Đề xuất kiến trúc và giải pháp cải tiến cho PI-Guard.

👉 Chi tiết theo dõi tại: [`../tasks_for_meeting_5/README.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/README.md)
