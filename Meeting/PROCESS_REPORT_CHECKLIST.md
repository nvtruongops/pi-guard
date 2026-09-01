# DANH MỤC CÔNG VIỆC CHI TIẾT & CHECKLIST TIẾN ĐỘ ĐỒ ÁN PI-GUARD
## BÁO CÁO QUÁ TRÌNH THỰC HIỆN THEO TUẦN (FPT IAP491 PROCESS REPORT)

**Mã đồ án**: `IAP491_FA26_PI_GUARD` — Ngành An toàn Thông tin (Information Assurance)  
**File Excel chính thức**: [`Meeting/PI_GUARD_PROCESS_REPORT.xlsx`](file:///d:/Work/Do-an/Meeting/PI_GUARD_PROCESS_REPORT.xlsx) hoặc [`reports/PI_GUARD_PROCESS_REPORT.xlsx`](file:///d:/Work/Do-an/reports/PI_GUARD_PROCESS_REPORT.xlsx)  
**File Kế hoạch hành động 1 tuần**: [`Meeting/Meeting_1_TODO_List_30_08_to_06_09_2026.md`](file:///d:/Work/Do-an/Meeting/Meeting_1_TODO_List_30_08_to_06_09_2026.md)  

---

## 👥 PHÂN CÔNG TRÁCH NHIỆM 4 THÀNH VIÊN

- **Trường (Leader)**: Kiến trúc, Curation Dataset, Report No.1 (Introduction), Report No.2 (Literature Review).
- **Đức**: Classical ML Baseline (Word/Char TF-IDF, LR, SVC, XGBoost), Report No.3 (Methodology).
- **Việt**: Transformer Fine-Tuning (DeBERTa-v3, ONNX INT8), Robustness Test, Report No.4 (Experimental & Results).
- **Phương**: FastAPI Middleware, Streamlit Dashboard, Report No.5 (Discussion), Report No.6 (Conclusion) & Luận văn.

---

## 📋 BẢNG CHECKLIST CÔNG VIỆC CHI TIẾT TỪNG TUẦN

### GIAI ĐOẠN 1: REVIEW 1 & XÁC ĐỊNH BÀI TOÁN (TUẦN 1 - TUẦN 3)

#### Tuần 1 (23/08/2026 – 29/08/2026): Khởi Động & Đăng Ký Đề Tài
- [x] **T01**: Họp với Giáo viên hướng dẫn (GVHD) và xác định mục tiêu ban đầu của đề tài (Biên bản [`Meeting/Meeting 1_29_08_26.md`](file:///d:/Work/Do-an/Meeting/Meeting%201_29_08_26.md)). — *Phụ trách: Trường (Leader)*
- [ ] **T02**: Khảo sát tài liệu nghiên cứu và thu thập 17 papers chuẩn IEEE >= 2022 vào [`References/`](file:///d:/Work/Do-an/References/) và [`References/REFERENCES_LOG.md`](file:///d:/Work/Do-an/References/REFERENCES_LOG.md). — *Phụ trách: Trường*
- [ ] **T03**: Thiết lập môi trường Python 3.11, Git repo, và cài đặt các thư viện lõi. — *Phụ trách: Cả 4 thành viên*

#### Tuần 2 (30/08/2026 – 05/09/2026): Chuẩn Bị Hồ Sơ Review 1 (2 Chapters: Report No.1 & Report No.2)
- [ ] **T04**: Soạn thảo Bối cảnh (Background) & Phát biểu bài toán (Problem Statement - Lỗ hổng Von Neumann NLP) — *Chapter 1*. — *Phụ trách: Trường*
- [ ] **T05**: Soạn thảo Bảng phân loại mối đe dọa (Threat Taxonomy: Direct/Indirect Injection vs Jailbreak theo OWASP LLM01:2025) — *Chapter 1 & 2*. — *Phụ trách: Trường & Đức*
- [ ] **T06**: Xây dựng sơ đồ Threat Model (NIST AI 100-2e2025) & Khóa chặt Attack Surface tại REST API `/v1/chat` — *Chapter 1 & 2*. — *Phụ trách: Đức*
- [ ] **T07**: Phân tích Kiến trúc bảo vệ 3 lớp (Input Guardrail, Target LLM, Output Sanitizer) & Cơ chế phòng thủ độ bền Robustness — *Chapter 2*. — *Phụ trách: Đức*
- [ ] **T08**: Soạn thảo 3 Câu hỏi nghiên cứu cốt lõi chuẩn IEEE (RQ1-RQ3), 3 Research Gaps & 4 Đóng góp mới — *Chapter 1 & 2*. — *Phụ trách: Phương*
- [ ] **T09**: Khảo sát SOTA Guardrails (ProtectAI, Llama Guard, NeMo), Model Selection Matrix & Benchmark 5 Target LLMs qua API — *Chapter 2*. — *Phụ trách: Việt*
- [ ] **T10**: Thiết kế & kiểm thử Ma trận 4 Kịch bản Demo ($2 \times 2$: Vulnerable vs. Protected) — *Chapter 2*. — *Phụ trách: Việt & Phương*
- [ ] **T11**: Soạn thảo và hoàn thiện toàn văn [`docs/thesis/chapters/01_Introduction.md`](file:///d:/Work/Do-an/docs/thesis/chapters/01_Introduction.md) (**Report No.1** — 10% Process Mark). — *Phụ trách: Trường (Leader)*
- [ ] **T12**: Soạn thảo và hoàn thiện toàn văn [`docs/thesis/chapters/02_Literature_Review.md`](file:///d:/Work/Do-an/docs/thesis/chapters/02_Literature_Review.md) (**Report No.2** — 25% Process Mark). — *Phụ trách: Trường & Phương*
- [ ] **T13**: Soạn thảo dàn ý 9 slide thuyết trình [`docs/thesis/Review1_Presentation_Slides_Outline.md`](file:///d:/Work/Do-an/docs/thesis/Review1_Presentation_Slides_Outline.md) (Trình bày 2 Chương). — *Phụ trách: Phương*
- [ ] **T14**: Thiết kế slide PowerPoint (.pptx) chuẩn nhận diện FPT University & Ghép nối kịch bản 15 phút. — *Phụ trách: Phương & Trường*
- [ ] **T15**: Họp tổng kết tuần, cập nhật file Excel tiến độ [`PI_GUARD_PROCESS_REPORT.xlsx`](file:///d:/Work/Do-an/Meeting/PI_GUARD_PROCESS_REPORT.xlsx) và nộp Report No.1 & No.2 cho GVHD. — *Phụ trách: Trường (Leader)*

#### Tuần 3 - 4 (06/09/2026 – 19/09/2026): CỘT MỐC 1 — REVIEW 1 (GVHD)
- [ ] **T16**: **BẢO VỆ REVIEW 1: XÁC ĐỊNH BÀI TOÁN & KHẢO SÁT NGHIÊN CỨU (CHAPTERS 1 & 2)** trước GVHD. — *Phụ trách: Cả 4 thành viên*
- [ ] **T17**: Tiếp thu ý kiến góp ý của GVHD và hoàn thiện toàn diện Chapter 1 & Chapter 2. — *Phụ trách: Cả 4 thành viên*

---

### GIAI ĐOẠN 2: METHODOLOGY & BASELINE MACHINE LEARNING (TUẦN 5 - TUẦN 7)

#### Tuần 5 - 6 (20/09/2026 – 03/10/2026): Data Engineering & Baseline ML
- [ ] **T18**: Thu thập dữ liệu đa nguồn từ Hugging Face (Deepset, Gandalf, In-the-Wild, Benign). — *Phụ trách: Trường*
- [ ] **T19**: Cài đặt thuật toán *Group-Aware Splitting* khử rò rỉ dữ liệu cụm. — *Phụ trách: Trường*
- [ ] **T20**: Xây dựng module trích xuất đặc trưng kết hợp (Word + Char n-grams TF-IDF). — *Phụ trách: Đức*
- [ ] **T21**: Huấn luyện các mô hình Baseline: Logistic Regression, LinearSVC, Naive Bayes, XGBoost. — *Phụ trách: Đức*

#### Tuần 7 (04/10/2026 – 10/10/2026): CỘT MỐC 2 — REVIEW 2 (GVHD)
- [ ] **T22**: Hoàn thiện toàn văn [`docs/thesis/chapters/03_Methodology.md`](file:///d:/Work/Do-an/docs/thesis/chapters/03_Methodology.md) (**Report No.3** — 20% Process Mark). — *Phụ trách: Đức & Trường*
- [ ] **T23**: **BẢO VỆ REVIEW 2: METHODOLOGY & BASELINE ML (CHAPTER 3)** trước GVHD. — *Phụ trách: Cả 4 thành viên*

---

### GIAI ĐOẠN 3: TRANSFORMER, LƯỢNG HÓA & PROTOTYPE (TUẦN 8 - TUẦN 12)

#### Tuần 8 - 9 (11/10/2026 – 24/10/2026): Fine-Tuning Transformer & Đo Đạc Độ Bền
- [ ] **T24**: Fine-tuning mô hình `microsoft/deberta-v3-base` trên tập dữ liệu đã phân tách. — *Phụ trách: Việt*
- [ ] **T25**: Lượng hóa động ONNX INT8 (ZeroQuant) tối ưu độ trễ P95 < 30ms trên CPU. — *Phụ trách: Việt*
- [ ] **T26**: Đánh giá thực nghiệm: Confusion Matrix, ROC-AUC, Test độ bền Leetspeak/Base64 Heuristic Decoder. — *Phụ trách: Việt & Đức*
- [ ] **T27**: Hoàn thiện toàn văn [`docs/thesis/chapters/04_Experimental_and_Results.md`](file:///d:/Work/Do-an/docs/thesis/chapters/04_Experimental_and_Results.md) (**Report No.4** — 25% Process Mark). — *Phụ trách: Việt*

#### Tuần 10 - 12 (25/10/2026 – 14/11/2026): API Middleware, Dashboard & CỘT MỐC 3 — BÁO CÁO HỘI ĐỒNG 1
- [ ] **T28**: Xây dựng Asynchronous FastAPI Middleware tích hợp mô hình ONNX INT8 & LLM Proxy. — *Phụ trách: Phương*
- [ ] **T29**: Xây dựng Streamlit Testing Dashboard trực quan với ma trận 4 kịch bản demo. — *Phụ trách: Phương*
- [ ] **T30**: **BÁO CÁO TIẾN ĐỘ TRƯỚC HỘI ĐỒNG 1 (HỘI ĐỒNG GIỮA KỲ — INTERIM DEFENSE)**: Trình diễn Prototype thực tế & kết quả đo đạc. — *Phụ trách: Cả 4 thành viên*

---

### GIAI ĐOẠN 4: THẢO LUẬN, HOÀN THIỆN LUẬN VĂN & CỘT MỐC 4 — BÁO CÁO HỘI ĐỒNG FINAL (TUẦN 13 - TUẦN 15)

#### Tuần 13 (15/11/2026 – 21/11/2026): Báo Cáo No. 5 & No. 6
- [ ] **T31**: Soạn thảo [`docs/thesis/chapters/05_Discussion.md`](file:///d:/Work/Do-an/docs/thesis/chapters/05_Discussion.md) (**Report No.5** — 15% Process Mark). — *Phụ trách: Phương*
- [ ] **T32**: Soạn thảo [`docs/thesis/chapters/06_Conclusion_and_Future_Work.md`](file:///d:/Work/Do-an/docs/thesis/chapters/06_Conclusion_and_Future_Work.md) (**Report No.6** — 5% Process Mark). — *Phụ trách: Phương & Trường*

#### Tuần 14 - 15 (22/11/2026 – 05/12/2026): Final Thesis & BẢO VỆ TỐT NGHIỆP TRƯỚC HỘI ĐỒNG FINAL
- [ ] **T33**: Chạy `python scripts/compile_thesis.py` tổng hợp toàn bộ 6 chương thành [`FINAL_THESIS.md`](file:///d:/Work/Do-an/docs/thesis/FINAL_THESIS.md) và kiểm tra đạo văn Turnitin (< 20%). — *Phụ trách: Cả 4 thành viên*
- [ ] **T34**: Hoàn thiện Slide thuyết trình bảo vệ tốt nghiệp (Final Defense Deck). — *Phụ trách: Cả 4 thành viên*
- [ ] **T35**: **BẢO VỆ TỐT NGHIỆP CHÍNH THỨC TRƯỚC HỘI ĐỒNG CHẤM KHÓA LUẬN FINAL**. — *Phụ trách: Cả 4 thành viên*
