# PI-Guard Workspace Version Specification: `workspaces/truongnv/`
## RELEASE VERSION: `v2.2-baseline-freezing-meeting6`

---

- **Họ và tên**: Nguyễn Văn Trường (Trưởng nhóm / Leader)
- **Mã số sinh viên**: `SE182034`
- **GitHub Account**: `nvtruongops`
- **Thời điểm chốt phiên bản**: 2026-09-24T19:50:00+07:00
- **Cột mốc học thuật**: Báo Cáo Tiến Độ Meeting 6 (Học kỳ Fall 2026 — GVHD ThS. Trần Văn Ninh)
- **Tình trạng nghiệm thu**: **ĐỐI CHUẨN BASELINE Y VĂN HOÀN TẤT & ĐÓNG BĂNG DANH MỤC BASELINE (CHAPTER 2)**

---

### 📌 1. ĐẶC TẢ PHIÊN BẢN (VERSION CHARTER)

Phiên bản `v2.2-baseline-freezing-meeting6` là cột mốc chính thức xác lập việc **Đóng Băng Danh Mục Baseline Y Văn Phục Vụ Đối Chuẩn (Chapter 2 Literature Baseline Freezing)** và hoàn thiện **Khung Đề Xuất Kiến Trúc Hai Tầng (Proposed Two-Tier Cascade Concept)** làm tiền đề khoa học cho Chương 3 (Methodology):

1. **Đóng Băng Danh Mục Baseline Y Văn (Chapter 2 Literature Baselines Freezing)**:
   - Cố định 12 mô hình public SOTA và baselines y văn (Heuristic Regex, Dual-Space TF-IDF Jain 2023, ProtectAI DeBERTa-v3 v2, Meta Prompt-Guard 86M, PIGuard Hao Li ACL 2025, DataSentinel S&P 2025, SmoothLLM NeurIPS 2023, ModernBERT, v.v.).
   - Đo đạc thực nghiệm độc lập 100% un-mocked trên bộ 6 tập dữ liệu y văn gốc D1–D6 (520 mẫu thực tế) nhằm chỉ ra các **điểm vỡ kỹ thuật (Failure Modes)**: TF-IDF trượt 100% Jailbreak, ProtectAI DeBERTa dính 19% FPR trên code, Meta Prompt-Guard chặn nhầm 99.1% code lành tính, lỗ hổng tràn ngữ cảnh 200k ký tự Prompt Overflow.
   - Các số liệu thực nghiệm này là bằng chứng định lượng phục vụ cho **Mục 2.3 (Khoảng trống Nghiên cứu - Research Gaps)**.

2. **Khung Đề Xuất Kiến Trúc Hai Tầng Cho Chương 3 (Proposed Two-Tier Cascade Concept)**:
   - **Tầng 0 (Ingress Scrubber)**: Đề xuất pipeline chuẩn hóa Unicode NFKC, strip Zero-width spaces, bóc tách chuỗi mã hóa đa tầng (Base64/Hex/Rot13/Leetspeak), tái hợp nhất chuỗi phân mảnh qua emoji.
   - **Tầng 1 (Đề xuất ý tưởng Fast-Filter)**: Đề xuất bộ lọc sơ cấp Dual-Space Sparse TF-IDF (Word n-grams 1–3 + Char_wb n-grams 3–5) kết hợp bộ phân loại Logistic Regression hiệu chuẩn Platt trên CPU.
   - **Bộ Điều Phối (Tri-State Router)**: Đề xuất cơ chế định tuyến 3 luồng dựa trên lý thuyết nhận dạng có vùng từ chối (Chow 1970) kết hợp Cổng kiểm soát độ thưa đặc trưng (Fail-Safe OOV Density Gate).
   - **Tầng 2 (Đề xuất ý tưởng Deep Semantic Arbiter)**: Đề xuất mạng nơ-ron Transformer `microsoft/deberta-v3-base` Disentangled Attention vận hành trên CPU Native FP32, định hướng tích hợp hàm mất mát Masked Overlap Fraction (MOF Invariance - Li et al. ACL 2025) để triệt tiêu báo động giả trên mã nguồn code.

> [!IMPORTANT]
> **RANH GIỚI HỌC THUẬT BẤT BIẾN**:
> Toàn bộ kiến trúc Two-Tier Cascade của đề tài PI-Guard tại cột mốc Meeting 6 được định vị là **Khung Đề Xuất Thiết Kế Kiến Trúc Lý Thuyết (Conceptual Architectural Proposal)** làm cơ sở cho Chương 3.
> Nhóm **CHƯA** huấn luyện mô hình chính thức của đồ án và **CHƯA** công bố các chỉ số nghiệm thu F1, Accuracy, hay độ trễ phân vị cho mô hình nhóm ở giai đoạn này. Việc huấn luyện, tối ưu và nghiệm thu chính thức mô hình đồ án thuộc phạm vi **Chương 4 (Proposed Model Evaluation - Report No.4 ở Tuần 13)**.

---

### 📊 2. TIẾN TRÌNH PHIÊN BẢN (VERSION PROGRESSION)

| Phiên Bản | Cột Mốc | Trọng Tâm Nghiên Cứu | Trạng Thái Kiểm Định |
| :--- | :--- | :--- | :---: |
| **`v1.0`** | Meeting 4 (2026-09-12) | Thiết lập 4 Task nền tảng: Phân biệt PI vs Jailbreak, Khung đe dọa 5D, Khảo sát datasets AdvBench/Alpaca/DAN/BIPIA. | Hoàn thành định tính |
| **`v1.1`** | Meeting 5 (2026-09-17) | Thực nghiệm tái lập PIGuard ACL 2025, khảo sát 4 ứng viên SOTA (Meta PromptGuard, InstructDetector, Ayub, Jain). | Hoàn thành tái lập |
| **`v2.0`** | Meeting 6 Pre (2026-09-22) | Mở rộng trung tâm 12 mô hình, bộ tài liệu 8 phân hệ Task 6, thiết lập ma trận tương thích 12x14. | Phát hiện khoảng trống mock |
| **`v2.1`** | Meeting 6 Un-mocked (2026-09-23) | Triệt tiêu 100% logic mock, kiểm thử Pytest PASS, Dynamic Class-Weighted Loss, sửa sạch neo trích dẫn. | Đạt chuẩn thực chất |
| **`v2.2`** | Meeting 6 (2026-09-24) | **Bản phát hành chuẩn hóa**: Đóng băng danh mục 12 baseline y văn, tinh giản tệp dư thừa, đối chuẩn 6 tập dữ liệu gốc D1-D6, thiết lập khung đề xuất Chương 3. | **BASELINE FREEZING (100% PASS)** |

---

### ✔️ 3. BẰNG CHỨNG KIỂM ĐỊNH TỰ ĐỘNG (VERIFICATION AUDIT TRAIL)

1. **Master Workspace Audit Suite**:
   - Lệnh: `workspaces/truongnv/.venv/Scripts/python workspaces/truongnv/scripts/audit_workspace.py --all`
   - Kết quả: `Markdown files scanned`, `Citations checked`, `Zero Attribution Leak`, `Zero Blacklist Violations`, **EXIT CODE 0**.
2. **Unit & Integration Test Suite**:
   - `workspaces/truongnv/tests/`: **PASSED** trên các bài test nguyên mẫu và baselines.
3. **Workspace Boundary Auditor**:
   - Lệnh: `python Final-Report/scripts/audit_workspace_boundaries.py`
   - Kết quả: **100% PASS** (Mọi thay đổi nằm trọn vẹn trong `workspaces/truongnv/`).
