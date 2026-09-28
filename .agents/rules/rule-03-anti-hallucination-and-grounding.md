# 🛡️ Rule 03: Anti-Hallucination & Empirical Grounding Standards

> **Quy định bất biến về chống tự sinh mô hình đồ án, chống giả mạo chỉ số tương lai và bảo chứng 100% bằng chứng thực nghiệm**  
> **Cơ chế thực thi**: Tự động kiểm toán qua `python Final-Report/scripts/audit_anti_hallucination.py` và tích hợp vào `validate_local.py`.

---

## 🚫 1. BỐN NGUYÊN TẮC BẤT BIẾN CỐT LÕI (FOUR NON-NEGOTIABLE INVARIANTS)

### 🔴 Nguyên Tắc 1: CẤM TỰ SINH MÔ HÌNH ĐỒ ÁN KHI CHƯA ĐẾN GIAI ĐOẠN HUẤN LUYỆN (Zero Premature Proposed Model Code)
1. **Phân định Cột mốc**:
   - **Giai đoạn Hiện tại (Chương 2 / Meeting 6)**: Trọng tâm duy nhất là **Tái lập Thực nghiệm Y văn (Literature Baseline Replication)** và phân tích **Khoảng trống Nghiên cứu (Research Gaps - Mục 2.3)** trên các mô hình công khai (Meta Prompt-Guard, ProtectAI DeBERTa-v3, PIGuard ACL 2025, DataSentinel, PromptShield).
   - **Mô hình của nhóm (Two-Tier Cascade)**: Chỉ là **Đề xuất Kiến trúc Lý thuyết** làm tiền đề cho **Chương 3 (Methodology)**.
   - **Huấn luyện & Đánh giá Chính thức**: Thuộc phạm vi **Chương 4 (Proposed Model Evaluation - Tuần 13)**.
2. **Cấm Đoán Tuyệt Đối Trong Mã Nguồn**:
   - Tuyệt đối **KHÔNG** tự ý tạo mới, sinh mã nguồn hoặc duy trì các lớp mô hình tự xưng là mô hình đồ án / mô hình champion (như thư mục `src/models/cascade/`, lớp `ChampionCascadeClassifier`, `ProposedCascadeClassifier`, `TwoTierCascadeGuardrail`, `CascadedGuardrailEngine`).
   - Phân hệ `src/models/` tại giai đoạn này chỉ được phép đóng gói bộ chuyển tiếp (adapters) để gọi các mô hình y văn chuẩn (`LiteratureBaselineClassifier`, `ReplicationModelRegistry`).

---

### 🔴 Nguyên Tắc 2: CẤM ĐƯA MÔ HÌNH NHÓM VÀO BẢNG ĐỐI CHUẨN KÈM SỐ LIỆU THỰC NGHIỆM GIẢ ĐỊNH (Zero Fabricated Metrics)
1. **Cấm Bảng Đối Chuẩn Trộn Lẫn Số Liệu Tương Lai**:
   - Tuyệt đối **KHÔNG** đưa dòng "PI-Guard (Proposed)", "PI-Guard Cascade", "Mô hình nhóm" vào các bảng số liệu đối chuẩn cạnh các mô hình y văn với các con số đo đạc cụ thể (Recall %, FPR %, Accuracy %, CPU Latency ms) khi nhóm **chưa huấn luyện và chưa đo đạc thực tế**.
   - Việc đưa ra các số liệu như *"PI-Guard: Recall 98.4%, FPR 0.8%, Latency 14.5ms"* trong bảng đối chuẩn ở giai đoạn Chương 2 là **HÀNH VI LÀM GIẢ SỐ LIỆU KHOA HỌC (ACADEMIC FRAUD)**, sẽ bị Hội đồng FPT đánh trượt ngay lập tức.
2. **Cách Trình Bày Chuẩn Mực Học Thuật**:
   - Chỉ được trình bày các chỉ số của đồ án dưới dạng **Chỉ Tiêu Thiết Kế Kỹ Thuật (Target Engineering KPI / SLA Objectives)** trong văn bản lý thuyết (prose), ví dụ:
     > *"Mục tiêu thiết kế kiến trúc Chương 3 hướng tới thỏa mãn SLA: Độ trễ CPU Native FP32 $P95 < 30\text{ms}$ và $\text{FPR} \le 1.5\%$."*
   - Tuyệt đối không dùng các từ: *"kết quả thực nghiệm của PI-Guard đạt"*, *"mô hình đồ án đã đạt được"*, *"mô hình vô địch toàn diện"*.

---

### 🔴 Nguyên Tắc 3: CẤM SINH ĐIỂM HOẶC DỮ LIỆU BẰNG PHÂN PHỐI NGẪU NHIÊN / MOCK (Zero Synthetic Random Generators)
1. **Cấm Thuật Toán Sinh Điểm Ngẫu Nhiên**:
   - Tuyệt đối **KHÔNG** sử dụng `np.random.beta`, `np.random.normal`, `random.uniform`, `np.random.randn` để sinh điểm nguy cơ (risk scores), mô phỏng ma trận tương đồng, hay tạo dữ liệu hiệu chuẩn giả.
2. **Cấm Centroids & Dữ Liệu Thử Nghiệm Mock**:
   - Mọi phân tích nhúng (embeddings) hoặc centroid phải được tính toán tất định hoặc nạp từ mô hình công khai đã được chứng minh.
   - Mọi tập dữ liệu kiểm thử phải là dữ liệu công khai gốc D1–D6 (PIGuard, BIPIA, JailbreakBench, DataSentinel, NotInject, PromptShield). Cấm tuyệt đối các dataset tự chế.

---

### 🔴 Nguyên Tắc 4: BẢO CHỨNG BẰNG CHỨNG THỰC TẾ 100% (100% Empirical Evidence & Provenance Grounding)
1. **Nguồn Gốc Số Liệu Rõ Ràng (Double-Anchored Provenance)**:
   - Mọi con số trong báo cáo, bảng biểu, slide thuyết trình PHẢI truy nguyên được từ một trong hai nguồn:
     - **Nguồn 1: Bài báo khoa học chuẩn**: Trích dẫn neo HTML `[[N]](#refN)` khớp với bài báo trong `Final-Report/References/REFERENCES_LOG.md`.
     - **Nguồn 2: Tệp dữ liệu đo đạc un-mocked thực tế**: Tệp JSON/CSV được sinh ra bởi script đo đạc độc lập trong `04_benchmarks_and_data/` trên bộ mẫu D1–D6.
2. **Không Khẳng Định Ngoài Tầm Bằng Chứng**:
   - Nếu một bài báo không công bố chỉ số, phải ghi rõ `N/A`, không được tự ý điền số ước lượng.

---

## 🔍 2. DANH MỤC MÃ QUÉT KIỂM TOÁN TỰ ĐỘNG (AUTOMATED AUDIT SIGNATURES)

Bộ công cụ `audit_anti_hallucination.py` quét và tự động chặn các mẫu sau:

| Mã Kiểm Tra | Đối Tượng Quét | 🚫 Mẫu Phát Hiện Vi Phạm | Hành Động Xử Lý |
| :--- | :--- | :--- | :--- |
| **`AH-01`** | `src/models/`, `workspaces/*/src/` | `src/models/cascade/`, `ChampionCascadeClassifier`, `ProposedCascadeClassifier`, `TwoTierCascadeGuardrail`, `CascadedGuardrailEngine` | Báo lỗi ngay lập tức; Yêu cầu xóa bỏ thư mục/lớp tự tạo. |
| **`AH-02`** | Python files (`src/`, `tests/`, `scripts/`) | `np.random.beta(`, `np.random.normal(`, `random.uniform(` dùng để sinh điểm hoặc giả lập kết quả benchmark | Báo lỗi AST; Yêu cầu dùng dữ liệu un-mocked hoặc test case tất định. |
| **`AH-03`** | Markdown tables (`reports/`, `docs/`, `thesis/`) | Bảng Markdown chứa cả tên mô hình baseline y văn và tên mô hình đề xuất (`PI-Guard`, `Two-Tier`, `Cascade`) kèm các cột số liệu đo đạc (%) | Báo lỗi cấu trúc bảng; Yêu cầu tách riêng bảng đề xuất kiến trúc lý thuyết. |
| **`AH-04`** | Toàn bộ Markdown | *"mô hình vô địch của đồ án"*, *"mô hình nhóm đạt F1"*, *"kết quả thực nghiệm của PI-Guard đạt"*, *"champion cascade"* | Báo lỗi từ khóa overclaiming; Yêu cầu sửa thành ngôn ngữ khiêm tốn học thuật. |
