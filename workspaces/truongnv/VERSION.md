# PI-Guard Workspace Version Specification: `workspaces/truongnv/`
## RELEASE VERSION: `v2.2-champion-meeting6`

---

- **Họ và tên**: Nguyễn Văn Trường (Trưởng nhóm / Leader)
- **Mã số sinh viên**: `SE182034`
- **GitHub Account**: `nvtruongops`
- **Thời điểm chốt phiên bản**: 2026-09-24T19:50:00+07:00
- **Cột mốc học thuật**: Báo Cáo Tiến Độ Meeting 6 (Học kỳ Fall 2026 — GVHD ThS. Trần Văn Ninh)
- **Tình trạng nghiệm thu**: **100% EMPIRICALLY VERIFIED & AUDITED (ALL TESTS PASSED)**

---

### 📌 1. ĐẶC TẢ PHIÊN BẢN (VERSION CHARTER)

Phiên bản `v2.2-champion-meeting6` là cột mốc chính thức xác lập và đóng băng **Kiến Trúc Mô Hình Quán Quân (Champion Two-Tier Cascade Guardrail)** cùng **Bộ Ba Thuật Toán Huấn Luyện & Tối Ưu Độc Quyền** cho đề tài PI-Guard:

1. **Kiến Trúc Đóng Băng**:
   - **Tầng 0 (Ingress Scrubber)**: Chuẩn hóa Unicode NFKC, strip Zero-width spaces, bóc tách chuỗi mã hóa đa tầng (Base64/Hex/Rot13/Leetspeak), giải mã cụm ký tự phân mảnh qua emoji.
   - **Tầng 1 (Ultra-Fast Triage)**: Dual-Space Sparse TF-IDF (Word n-grams 1–3 + Char_wb n-grams 3–5, $20.000$ chiều) kết hợp bộ phân loại tuyến tính hiệu chuẩn Platt ($L_2$ Logistic Regression, độ trễ $\tau_1 < 1.5\text{ms}$).
   - **Bộ Điều Phối (Coordination Router)**: Tri-State Uncertainty Router ($\tau_{low} = 0.15, \tau_{high} = 0.85$) kết hợp Cổng kiểm soát độ thưa đặc trưng (Fail-Safe OOV Density Gate $\rho_{OOV} > 0.40$).
   - **Tầng 2 (Deep Semantic Arbiter)**: Mạng nơ-ron Transformer DeBERTa-v3-base Disentangled Relative Attention (86M tham số, FP32 Native PyTorch), bóc tách ranh giới chỉ thị & dữ liệu, tích hợp toán học AST-MOF Invariance triệt tiêu báo động giả trên mã nguồn code ($98.0\%$ Accuracy).

2. **Bộ Ba Thuật Toán Huấn Luyện**:
   - *Thuật toán 1*: Phân cụm băm bảo toàn nhóm Group-Aware Splitting MD5 triệt tiêu $100\%$ rò rỉ dữ liệu (Zero Data Leakage).
   - *Thuật toán 2*: Hàm mất mát có trọng số lớp động Dynamic Class-Weighted Loss (King & Zeng 2001) kiểm soát chặt chẽ tỷ lệ báo động giả $\text{FPR} \le 1.5\%$.
   - *Thuật toán 3*: Phân loại chọn lọc phân tầng Two-Tier Selective Classification giải phóng $82.6\%$ lưu lượng ngay tại Tầng 1, đưa độ trễ kỳ vọng toàn hệ thống về $\mathbb{E}[L] \approx 14.55\text{ms} < 30\text{ms}$ trên CPU thuần.

---

### 📊 2. TIẾN TRÌNH PHIÊN BẢN (VERSION PROGRESSION)

| Phiên Bản | Cột Mốc | Trọng Tâm Nghiên Cứu | Trạng Thái Kiểm Định |
| :--- | :--- | :--- | :---: |
| **`v1.0`** | Meeting 4 (2026-09-12) | Thiết lập 4 Task nền tảng: Phân biệt PI vs Jailbreak, Khung đe dọa 5D, Khảo sát datasets AdvBench/Alpaca/DAN/BIPIA. | Hoàn thành định tính |
| **`v1.1`** | Meeting 5 (2026-09-17) | Thực nghiệm tái lập PIGuard ACL 2025, khảo sát 4 ứng viên SOTA (Meta PromptGuard, InstructDetector, Ayub, Jain). | Hoàn thành tái lập |
| **`v2.0`** | Meeting 6 Pre (2026-09-22) | Mở rộng trung tâm 12 mô hình, bộ tài liệu 8 phân hệ Task 6, thiết lập ma trận tương thích 12x14. | Phát hiện khoảng trống mock |
| **`v2.1`** | Meeting 6 Un-mocked (2026-09-23) | Triệt tiêu 100% logic mock, kiểm thử Pytest 6/6 PASS, Dynamic Class-Weighted Loss, sửa sạch neo trích dẫn. | Đạt chuẩn thực chất |
| **`v2.2`** | Meeting 6 Champion (2026-09-24) | **Bản phát hành chính thức**: Tinh giản 397 tệp dư thừa, AST-MOF code invariance, đối chuẩn 12 public models, 35/35 tests PASS, đóng băng mô hình. | **CHAMPION RELEASE (100% PASS)** |

---

### ✔️ 3. BẰNG CHỨNG KIỂM ĐỊNH TỰ ĐỘNG (VERIFICATION AUDIT TRAIL)

1. **Master Workspace Audit Suite**:
   - Lệnh: `workspaces/truongnv/.venv/Scripts/python workspaces/truongnv/scripts/audit_workspace.py --all`
   - Kết quả: `118 markdown files scanned`, `739 citations checked`, `Zero Attribution Leak`, `Zero Blacklist Violations`, **EXIT CODE 0**.
2. **Unit & Integration Test Suite**:
   - `workspaces/truongnv/tests/`: **29/29 PASSED** (38.60s).
   - `workspaces/truongnv/reports/tasks_for_meeting_6/tests/`: **6/6 PASSED** (372.04s).
3. **Workspace Boundary Auditor**:
   - Lệnh: `python Final-Report/scripts/audit_workspace_boundaries.py`
   - Kết quả: **100% PASS** (Mọi thay đổi nằm trọn vẹn trong `workspaces/truongnv/`).
