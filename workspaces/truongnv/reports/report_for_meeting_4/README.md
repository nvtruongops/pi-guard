# HỒ SƠ BÁO CÁO TIẾN ĐỘ MEETING 4 (10/09/2026)
**Đề tài**: A Machine-Learning Guardrail for Detecting Prompt Injection and Jailbreak Attacks on LLM Applications (PI-Guard)  
**Địa điểm**: Báo cáo trực tiếp tại Campus Đại học FPT  
**Giáo viên Hướng dẫn (GVHD)**: Thầy Trần Văn Ninh  
**Người thực hiện**: Nguyễn Văn Trường (Leader — MSSV: `SE182034`) | **Workspace**: `workspaces/truongnv/reports/report_for_meeting_4/`

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

## 🎯 3. Ý Kiến Chỉ Đạo Của GVHD Tại Meeting 4 & Chuyển Giao Sang Meeting 5

Sau khi nghe nhóm thuyết trình bộ slide tại Meeting 4, Thầy Trần Văn Ninh đã ghi nhận tiến độ và giao cho cả 4 thành viên giải quyết triệt để **4 nhiệm vụ then chốt** trong tuần để báo cáo tại **Meeting 5 (17/09/2026)**:

- **Nhiệm vụ 1**: Phân biệt bản chất 2 khái niệm Prompt Injection vs. Jailbreak.
- **Nhiệm vụ 2**: Phân tích chi tiết 5 trục tấn công và cơ sở toán học của 2 mô hình tham khảo (TF-IDF Baseline và DeBERTa-v3).
- **Nhiệm vụ 3 (Trọng tâm tối thượng)**: Tải mã nguồn công khai, dataset chuẩn, chạy thực nghiệm tái lập độc lập mô hình mỏ neo PIGuard (ACL 2025) trên máy cá nhân để nắm chắc số liệu.
- **Nhiệm vụ 4**: Đề xuất 4 giải pháp cải tiến kỹ thuật cho đồ án PI-Guard.

👉 Toàn bộ 4 nhiệm vụ trên được tổ chức và theo dõi tập trung tại phân hệ:  
**[`../tasks_for_meeting_5/README.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/README.md)**
