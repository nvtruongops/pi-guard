# DANH MỤC CÔNG VIỆC CHI TIẾT & CHECKLIST TIẾN ĐỘ ĐỒ ÁN PI-GUARD
## BÁO CÁO QUÁ TRÌNH THỰC HIỆN THEO TUẦN (FPT IAP491 PROCESS REPORT)

**Mã đồ án**: `IAP491_FA26_PI_GUARD` — Ngành An toàn Thông tin (Information Assurance), Đại học FPT  
**Đề tài**: A Machine-Learning Guardrail for Detecting Prompt Injection and Jailbreak Attacks on LLM Applications (**PI-Guard**)  
**Thời gian khởi động & Sprint Tiền đề Review 1**: 29/08/2026 – 06/09/2026  
**Thời gian học kỳ chính thức Fall 2026 (15 Tuần)**: 07/09/2026 – 20/12/2026  
**File Excel chính thức**: [`Meeting/PI_GUARD_PROCESS_REPORT.xlsx`](file:///d:/Work/Do-an/Meeting/PI_GUARD_PROCESS_REPORT.xlsx)  
**Biên bản Họp với GVHD & Kế hoạch Sprint 1 (Meeting 1)**: [`Meeting/Meeting 1_29_08_26.md`](file:///d:/Work/Do-an/Meeting/Meeting%201_29_08_26.md) *(29/08/2026)*  
**Biên bản Họp Nhóm Sàng Lọc Papers & Nghiên Cứu Mô Hình (Meeting 2)**: [`Meeting/Meeting 2_01_09_26.md`](file:///d:/Work/Do-an/Meeting/Meeting%202_01_09_26.md) *(01/09/2026)*  

---

## 👥 I. PHÂN CÔNG TRÁCH NHIỆM & MA TRẬN RACI 4 THÀNH VIÊN

| Thành Viên | Mã SV | Vai Trò & Module Dẫn Đầu | Trách Nhiệm Cốt Lõi Trong Dự Án | Workspace & Branch Git |
| :--- | :---: | :--- | :--- | :--- |
| **Nguyễn Văn Trường (Leader)** | `SE182034` | **Kiến Trúc Hệ Thống & Data Engineering** | • Điều phối tiến độ chung, kiểm toán ranh giới Git và merge độc quyền ra root.<br>• Phụ trách Curation, Deduplication và Group-Aware Splitting cho Dataset.<br>• Chủ biên Report No. 1 (Introduction) & Report No. 2 (Literature Review).<br>• Cập nhật file Excel tiến độ hàng tuần nộp cho Giảng viên hướng dẫn (GVHD). | `workspaces/truongnv/`<br>Branch: `main`, `lead/truong-*` |
| **Nguyễn Quí Đức** | `SE182087` | **Classical ML Baseline & Threat Modeling** | • Xây dựng mô hình Threat Model (NIST AI 100-2e2025) và khóa chặt Attack Surface tại API `/v1/chat`.<br>• Xây dựng pipeline trích xuất đặc trưng kết hợp (Word + Char n-grams TF-IDF).<br>• Huấn luyện, tối ưu các mô hình Baseline (Logistic Regression, LinearSVC, Naive Bayes, XGBoost).<br>• Chủ biên Report No. 3 (Methodology - Baseline ML & Feature Engineering). | `workspaces/ducnq/`<br>Branch: `feat/duc-baseline-ml` |
| **Phạm Minh Hoàng Việt** | `SE181851` | **Transformer Fine-Tuning & Quantization** | • Nghiên cứu cơ chế Disentangled Attention của `microsoft/deberta-v3-base`.<br>• Huấn luyện Supervised Fine-Tuning Transformer và tối ưu hóa hàm mất mát.<br>• Lượng hóa động ONNX INT8 (ZeroQuant) tối ưu độ trễ P95 $< 30\text{ms}$ trên CPU.<br>• Chủ biên Report No. 4 (Experimental and Results - Training & Adversarial Tests). | `workspaces/vietpmh/`<br>Branch: `feat/viet-transformer` |
| **Đỗ Đoàn Duy Phương** | `SE180235` | **API Middleware, Dashboard & Luận Văn** | • Phát triển Asynchronous FastAPI Middleware tích hợp mô hình ONNX & LLM Proxy.<br>• Xây dựng giao diện Streamlit Dashboard phục vụ trực quan hóa 4 kịch bản demo.<br>• Định dạng, biên tập toàn văn Luận văn 6 chương theo chuẩn FPT IAP491.<br>• Chủ biên Report No. 5 (Discussion), Report No. 6 (Conclusion) & Slide PPTX. | `workspaces/phuongddd/`<br>Branch: `feat/phuong-api-ui` |

---

## 📅 II. TIẾN TRÌNH THỰC HIỆN TỪ KHI BẮT ĐẦU HỌP (29/08/2026) ĐẾN KẾT THÚC HỌC KỲ

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                          DÒNG THỜI GIAN TOÀN DIỆN CỦA ĐỒ ÁN PI-GUARD (16 TUẦN)                          │
├────────────────────────────────┬───────────────────────────────────────┬───────────────────────────────┤
│ Giai Đoạn Dự Án                │ Thời Gian Thực Hiện                   │ Trọng Tâm & Cột Mốc Nghiệm Thu│
├────────────────────────────────┼───────────────────────────────────────┼───────────────────────────────┤
│ 🚀 GIAI ĐOẠN 0: SPRINT TIỀN ĐỀ │ 29/08/2026 – 06/09/2026 (9 ngày)      │ Họp GVHD, Lọc 18 Papers,      │
│    (Chuẩn Bị Toàn Diện Review 1)│                                       │ Chuyên Đề Tấn Công, Robustness│
├────────────────────────────────┼───────────────────────────────────────┼───────────────────────────────┤
│ 🎯 GIAI ĐOẠN 1: REVIEW 1       │ Tuần 1 – Tuần 4 (07/09 – 04/10/2026)  │ CỘT MỐC 1: BẢO VỆ REVIEW 1    │
│    (Xác Định Bài Toán & Khảo Sát)│                                       │ (Report No.1 & Report No.2)   │
├────────────────────────────────┼───────────────────────────────────────┼───────────────────────────────┤
│ 🔬 GIAI ĐOẠN 2: REVIEW 2       │ Tuần 5 – Tuần 8 (05/10 – 01/11/2026)  │ CỘT MỐC 2: BẢO VỆ REVIEW 2    │
│    (Data & Classical ML Baseline│                                       │ (Report No.3 — Methodology)   │
├────────────────────────────────┼───────────────────────────────────────┼───────────────────────────────┤
│ ⚡ GIAI ĐOẠN 3: REVIEW 3 (GIỮA KỲ)│ Tuần 9 – Tuần 13 (02/11 – 06/12/2026) │ CỘT MỐC 3: HỘI ĐỒNG GIỮA KỲ   │
│    (Transformer, ONNX, Prototype│                                       │ (Report No.4 & Demo Prototype)│
├────────────────────────────────┼───────────────────────────────────────┼───────────────────────────────┤
│ 🏆 GIAI ĐOẠN 4: REVIEW 4 (FINAL)│ Tuần 14 – Tuần 15 (07/12 – 20/12/2026)│ CỘT MỐC 4: BẢO VỆ TỐT NGHIỆP  │
│    (Hoàn Thiện Luận Văn 6 Chương│                                       │ (Report No.5, No.6 & Defense) │
└────────────────────────────────┴───────────────────────────────────────┴───────────────────────────────┘
```

---

## 📋 III. BẢNG CHECKLIST CÔNG VIỆC CHI TIẾT TỪNG NGÀY & TỪNG TUẦN

### 🚀 GIAI ĐOẠN 0: SPRINT TIỀN ĐỀ REVIEW 1 — TỪ KHI BẮT ĐẦU HỌP (29/08/2026 – 06/09/2026)

#### 📌 Ngày 29/08/2026 (Thứ Bảy): Khởi Động Đề Tài & Họp Meeting 1 Với GVHD
- [x] **P01**: Tiến hành buổi họp đầu tiên (Meeting 1) với Giảng viên hướng dẫn để tiếp nhận định hướng và 8 yêu cầu kết quả bắt buộc của Review 1. — *Phụ trách: Cả 4 thành viên*
- [x] **P02**: Soạn thảo và lưu trữ biên bản cuộc họp: [`Meeting/Meeting 1_29_08_26.md`](file:///d:/Work/Do-an/Meeting/Meeting%201_29_08_26.md). — *Phụ trách: Trường (Leader)*

#### 📌 Ngày 30/08 – 31/08/2026 (Chủ Nhật – Thứ Hai): Lập Kế Hoạch Sprint & Thiết Lập Hệ Thống
- [x] **P03**: Phân rã 8 yêu cầu của GVHD thành Kế hoạch hành động Sprint 1 chi tiết được tích hợp trong: [`Meeting/Meeting 1_29_08_26.md`](file:///d:/Work/Do-an/Meeting/Meeting%201_29_08_26.md). — *Phụ trách: Trường (Leader)*
- [x] **P04**: Khởi tạo cấu trúc Git Repository, xây dựng 4 workspace cá nhân độc lập (`workspaces/<member>/`) để triển khai mô hình làm việc song song không xung đột. — *Phụ trách: Trường*
- [x] **P05**: Viết công cụ tự động kiểm toán phân quyền và ranh giới thư mục: [`scripts/audit_workspace_boundaries.py`](file:///d:/Work/Do-an/scripts/audit_workspace_boundaries.py), cài đặt Git Pre-commit Hook. — *Phụ trách: Trường*
- [x] **P06**: Rà soát bản đăng ký đề tài [`CAPSTONE PROJECT REGISTER.md`](file:///d:/Work/Do-an/CAPSTONE%20PROJECT%20REGISTER.md) và thiết lập quy tắc bảo vệ file bất biến. — *Phụ trách: Cả 4 thành viên*

#### 📌 Ngày 01/09/2026 (Thứ Ba): Họp Meeting 2 — Đọc Hiểu, Phân Tích & Thẩm Định 10 Bài Báo Khoa Học
- [x] **P07**: Cả nhóm họp Meeting 2 đọc hiểu, phản biện và thẩm định 10 bài báo khoa học theo đề tài:
  - *Việt*: Thẩm định RAP-ID (ACL 2026) & BIPIA (ACM KDD 2025) $\rightarrow$ Giữ lại làm cơ sở Attention Shift và benchmark Indirect Injection.
  - *Phương*: Thẩm định Greshake (2023), Do-Not-Answer (2023), Survey (2024), Zou GCG (2023) $\rightarrow$ Giữ lại làm cơ sở ranh giới phẳng $X = S \mathbin{\Vert} U$ và luận điểm mô hình < 600M tham số; Loại bỏ phần đào tạo lại nội tại của Wei et al.
  - *Đức*: Thẩm định JailGuard (ACM TOSEM 2025) $\rightarrow$ Tiếp thu Algorithm 1 Targeted Mutators để làm test độ bền; loại bỏ phần xử lý ảnh/video đa phương thức.
  - *Trường*: Thẩm định DeBERTa-v3 (ICLR 2023) và ZeroQuant (NeurIPS 2022).
- [x] **P08**: Soạn thảo biên bản cuộc họp: [`Meeting/Meeting 2_01_09_26.md`](file:///d:/Work/Do-an/Meeting/Meeting%202_01_09_26.md). — *Phụ trách: Cả 4 thành viên*

#### 📌 Ngày 02/09/2026 (Thứ Tư): Xây Dựng Chuyên Đề Attack Study & Model Study
- [x] **P09**: Xây dựng chuyên đề Biên niên sử tiến hóa (Causal LM vs. Instruction Tuning) giải thích lý do tại sao trước năm 2022 chưa có Prompt Injection: [`docs/attack_study/00_overview_threat_and_scope/history_and_evolution.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/attack_study/00_overview_threat_and_scope/history_and_evolution.md). — *Phụ trách: Trường*
- [x] **P10**: Phân tích cơ chế ranh giới phẳng và phân loại toàn diện 13 biến thể Prompt Injection: [`docs/attack_study/01_prompt_injection/`](file:///d:/Work/Do-an/workspaces/truongnv/docs/attack_study/01_prompt_injection/). — *Phụ trách: Trường & Đức*
- [x] **P11**: Nghiên cứu sâu cơ sở toán học TF-IDF, Character n-grams (`char_wb`), Luhn (1958), Spärck Jones (1972) và DeBERTa-v3 Disentangled Attention (He et al., 2023): [`docs/model_study/`](file:///d:/Work/Do-an/workspaces/truongnv/docs/model_study/). — *Phụ trách: Đức & Việt*

#### 📌 Ngày 03/09/2026 (Thứ Năm): Xây Dựng Chuyên Đề Modern Jailbreak & Ma Trận 4 Kịch Bản Demo
- [x] **P12**: Nghiên cứu 4 trường phái Jailbreak hiện đại (DAN, Roleplay, Virtual Machine, Cipher), 10 họ chiến thuật và 26 toán tử Tencent 2026: [`docs/attack_study/02_modern_jailbreak_attacks/`](file:///d:/Work/Do-an/workspaces/truongnv/docs/attack_study/02_modern_jailbreak_attacks/). — *Phụ trách: Việt & Phương*
- [x] **P13**: Thiết kế & kiểm thử ma trận 4 kịch bản Demo ($2 \times 2$: Vulnerable vs Protected) đo đạc độ trễ P95 $< 18\text{ms}$ trên CPU. — *Phụ trách: Phương & Việt*
- [x] **P14**: Xây dựng bộ công cụ kiểm toán URL và tự động tra cứu Open-Access PDF từ DOI: [`scripts/verify_resource_url.py`](file:///d:/Work/Do-an/scripts/verify_resource_url.py). — *Phụ trách: Trường*

#### 📌 Ngày 04/09/2026 (Thứ Sáu - Hôm Nay): Nghiên Cứu Độ Bền Robustness, Nâng Cấp Cleaner & Test Đối Kháng
- [x] **P15**: Thực hiện nghiên cứu chuyên sâu phần **Robustness on obfuscated/evasion samples (leetspeak, base64, spacing tricks)** theo đúng bản đăng ký đề tài:
  - Phân tích hiện tượng vỡ vụn token (Token Fragmentation) trong thuật toán BPE/WordPiece.
  - Phân tích cơ chế vượt rào Base64 (Yuan et al., ICLR 2024) và Spacing tricks.
  - Thiết kế kiến trúc phòng thủ 3 tầng kháng lẩn tránh của PI-Guard (Tầng 0 Tiền xử lý, Tầng 1 Character n-grams TF-IDF, Tầng 2 DeBERTa-v3 INT8).
  - Xuất bản bộ chuyên đề 4 tài liệu tại [`workspaces/truongnv/docs/robustness_study/`](file:///d:/Work/Do-an/workspaces/truongnv/docs/robustness_study/). — *Phụ trách: Trường (Leader)*
- [x] **P16**: Nâng cấp module [`src/preprocessing/cleaner.py`](file:///d:/Work/Do-an/src/preprocessing/cleaner.py) tự động loại bỏ các ký tự vô hình (`\u200B-\u200D\uFEFF`) và chuẩn hóa Fullwidth homoglyphs. — *Phụ trách: Đức & Trường*
- [x] **P17**: Xây dựng bộ kiểm thử đối kháng tự động [`tests/adversarial/test_obfuscation_robustness.py`](file:///d:/Work/Do-an/tests/adversarial/test_obfuscation_robustness.py) chứng minh Character n-grams vượt trội gấp $> 2.8\times$ so với Word-level. **16/16 tests toàn dự án đạt PASS 100%**. — *Phụ trách: Việt & Trường*
- [x] **P18**: Chuẩn hóa 100% cơ sở học thuật (18 papers IEEE $\ge 2022$ + foundational works), bảo đảm zero dead links và neo HTML nội trang toàn vẹn. — *Phụ trách: Trường*
- [x] **P19**: Cập nhật Cổng Thông Tin Web UI [`scripts/build_docs_portal.py`](file:///d:/Work/Do-an/scripts/build_docs_portal.py) và `mkdocs.yml`, tích hợp trọn vẹn Chuyên đề Robustness & Evasion. — *Phụ trách: Phương & Trường*

#### 📌 Ngày 05/09/2026 (Thứ Bảy): Thiết Kế Slide PPTX & Tập Dượt Thuyết Trình (Dry Run)
- [ ] **P20**: Thiết kế hoàn thiện bộ slide trình chiếu PowerPoint `.pptx` chuẩn nhận diện FPT University dựa trên dàn ý 9 slide tại [`docs/thesis/Review1_Presentation_Slides_Outline.md`](file:///d:/Work/Do-an/docs/thesis/Review1_Presentation_Slides_Outline.md). — *Phụ trách: Phương & Trường*
- [ ] **P21**: Cả 4 thành viên tiến hành buổi tập dượt thuyết trình nội bộ (Dry Run):
  - Khống chế thời lượng chính xác **15 phút trình bày** (mỗi thành viên phụ trách 3.5 – 4 phút).
  - Chuẩn bị sẵn kịch bản trả lời các câu hỏi phản biện tiềm năng từ GVHD/Hội đồng (**10 phút Q&A**). — *Phụ trách: Cả 4 thành viên*

#### 📌 Ngày 06/09/2026 (Chủ Nhật): Tổng Duyệt Cuối Cùng, Cập Nhật Nhật Ký & Nộp Cho GVHD
- [ ] **P22**: Quay video clip ngắn (Screen Recording ~2 phút) ghi lại quá trình chạy 4 kịch bản demo trên giao diện Streamlit/FastAPI làm phương án dự phòng (*Offline Backup Demo*). — *Phụ trách: Việt & Phương*
- [ ] **P23**: Cập nhật nhật ký tuần của 4 thành viên vào file Excel theo dõi tiến độ: [`Meeting/PI_GUARD_PROCESS_REPORT.xlsx`](file:///d:/Work/Do-an/Meeting/PI_GUARD_PROCESS_REPORT.xlsx). — *Phụ trách: Trường (Leader)*
- [ ] **P24**: Đóng gói và gửi toàn bộ hồ sơ cho Giảng viên hướng dẫn:
  1. Báo cáo **Report No. 1 (Introduction)** & **Report No. 2 (Literature Review)**.
  2. Hồ sơ kỹ thuật tổng hợp [`Review1_Problem_Definition_and_Threat_Model.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/thesis/Review1_Problem_Definition_and_Threat_Model.md).
  3. Dàn ý và file trình chiếu **Slide PPT Review 1** (`.pptx`).
  4. Bảng tiến độ làm việc tuần ([`PI_GUARD_PROCESS_REPORT.xlsx`](file:///d:/Work/Do-an/Meeting/PI_GUARD_PROCESS_REPORT.xlsx)). — *Phụ trách: Trường (Leader)*
- [ ] **P25**: Chốt lịch bảo vệ Review 1 chính thức với GVHD và sẵn sàng tâm lý tự tin bảo vệ trước Hội đồng. — *Phụ trách: Cả 4 thành viên*

---

### 🎯 GIAI ĐOẠN 1: HỌC KỲ CHÍNH THỨC — BẢO VỆ REVIEW 1 (TUẦN 1 - TUẦN 4: 07/09/2026 – 04/10/2026)

#### Tuần 1 (07/09/2026 – 13/09/2026): Khởi Động Học Kỳ Chính Thức & Hoàn Thiện Hồ Sơ Đăng Ký
- [ ] **T01**: Họp khởi động học kỳ chính thức Fall 2026 với GVHD, báo cáo kết quả hoàn thành của Sprint Tiền đề (Pre-Sprint). — *Phụ trách: Cả 4 thành viên*
- [ ] **T02**: Hoàn thiện và ký duyệt văn bản đăng ký đề tài chính thức với Khoa ATTT: [`CAPSTONE PROJECT REGISTER.md`](file:///d:/Work/Do-an/CAPSTONE%20PROJECT%20REGISTER.md). — *Phụ trách: Trường (Leader)*
- [ ] **T03**: Đồng bộ toàn bộ các tài liệu nghiên cứu đã hoàn thành từ workspace cá nhân vào thư mục gốc `docs/thesis/chapters/`. — *Phụ trách: Trường (Leader)*

#### Tuần 2 (14/09/2026 – 20/09/2026): Tinh Chỉnh Chương 1 (Introduction & Threat Modeling)
- [ ] **T04**: Rà soát, chuẩn hóa toàn văn [`docs/thesis/chapters/01_Introduction.md`](file:///d:/Work/Do-an/docs/thesis/chapters/01_Introduction.md) (**Report No.1** — 10% Điểm quá trình):
  - Mục 1.1 Bối cảnh & Mục 1.2 Phát biểu bài toán (Lỗ hổng Von Neumann trong Transformer).
  - Mục 1.3 Hệ thống 3 Research Questions chuẩn IEEE (RQ1-RQ3) & 4 Đóng góp mới của đề tài.
  - Mục 1.4 Ý nghĩa thực tiễn (4 tầng thiệt hại) & Mục 1.5 Phạm vi ranh giới In-Scope vs. Out-of-Scope. — *Phụ trách: Trường & Phương*
- [ ] **T05**: Chuẩn hóa sơ đồ Threat Model (NIST AI 100-2e2025) và kiến trúc phòng thủ 3 lớp trong Chapter 1. — *Phụ trách: Đức*

#### Tuần 3 (21/09/2026 – 27/09/2026): Tinh Chỉnh Chương 2 (Literature Review & SOTA Survey)
- [ ] **T06**: Rà soát, chuẩn hóa toàn văn [`docs/thesis/chapters/02_Literature_Review.md`](file:///d:/Work/Do-an/docs/thesis/chapters/02_Literature_Review.md) (**Report No.2** — 25% Điểm quá trình):
  - Khảo sát 3 nhóm giải pháp Guardrail (Regex, LLM-as-a-Judge Llama Guard 3, Small Transformer DeBERTa-v3).
  - 3 Khoảng trống nghiên cứu (Research Gaps) cốt lõi của chuyên ngành ATTT.
  - Bảng đối sánh Model Selection Matrix và khảo sát 5 Target LLM APIs.
  - Phân tích phòng thủ độ bền trước Leetspeak, Base64 và Spacing tricks. — *Phụ trách: Trường & Việt*
- [ ] **T07**: Tổng duyệt kịch bản 4 bài toán Demo trên môi trường thực nghiệm. — *Phụ trách: Việt & Phương*

#### Tuần 4 (28/09/2026 – 04/10/2026): CỘT MỐC 1 — BẢO VỆ REVIEW 1 CHÍNH THỨC TRƯỚC GVHD
- [ ] **T08**: Nộp chính thức **Report No. 1 (Introduction)** và **Report No. 2 (Literature Review)** cho GVHD (Chiếm tổng cộng 35% Điểm đánh giá quá trình). — *Phụ trách: Trường (Leader)*
- [ ] **T09**: **BẢO VỆ REVIEW 1 CHÍNH THỨC TRƯỚC GVHD**: Thuyết trình 15 phút, trình diễn 4 kịch bản demo và trả lời phản biện 10 phút. — *Phụ trách: Cả 4 thành viên*
- [ ] **T10**: Tiếp thu ý kiến góp ý của GVHD tại buổi bảo vệ, cập nhật hoàn thiện toàn diện Chapter 1 & Chapter 2, cập nhật nhật ký tuần vào file Excel. — *Phụ trách: Cả 4 thành viên*

---

### 🔬 GIAI ĐOẠN 2: METHODOLOGY & BASELINE MACHINE LEARNING (TUẦN 5 - TUẦN 8: 05/10/2026 – 01/11/2026)

#### Tuần 5 (05/10/2026 – 11/10/2026): Thu Thập, Làm Sạch & Curation Dataset
- [ ] **T11**: Thu thập dữ liệu thô từ 5 nguồn Hugging Face công khai: `deepset/prompt-injections`, `jayavibhav/prompt-injection`, `Lakera/gandalf_ignore_instructions`, `TrustAIRLab/in-the-wild-jailbreak-prompts`, và `xTRam1/safe-guard-prompt-injection`. — *Phụ trách: Trường (Leader)*
- [ ] **T12**: Thu thập tập dữ liệu lành tính (Benign Prompts) từ OpenAssistant & Alpaca để cân bằng tỷ lệ nhãn lớp. — *Phụ trách: Phương*
- [ ] **T13**: Khử trùng lặp (Deduplication) bằng MinHash LSH và chuẩn hóa văn bản qua `TextCleaner`. — *Phụ trách: Trường*

#### Tuần 6 (12/10/2026 – 18/10/2026): Group-Aware Splitting & Huấn Luyện Baseline ML
- [ ] **T14**: Cài đặt và thực thi thuật toán **Group-Aware Splitting** (gom cụm các biến thể diễn giải cùng nguồn vào cùng 1 split) để triệt tiêu hoàn toàn rò rỉ dữ liệu cụm (Cluster Data Leakage). — *Phụ trách: Trường*
- [ ] **T15**: Xây dựng pipeline trích xuất đặc trưng kết hợp: Word TF-IDF ($n \in [1, 2]$) + Character n-grams TF-IDF (`char_wb`, $n \in [3, 5]$). — *Phụ trách: Đức*
- [ ] **T16**: Huấn luyện các mô hình Baseline phân loại: Logistic Regression, LinearSVC, Complement Naive Bayes, XGBoost. — *Phụ trách: Đức*
- [ ] **T17**: Đo đạc độ chính xác, F1-score, FPR trên tập Benign và thời gian suy luận trên CPU. — *Phụ trách: Đức & Việt*

#### Tuần 7 (19/10/2026 – 25/10/2026): Soạn Thảo Chapter 3 (Methodology) & Thiết Kế Slide Review 2
- [ ] **T18**: Soạn thảo toàn văn [`docs/thesis/chapters/03_Methodology.md`](file:///d:/Work/Do-an/docs/thesis/chapters/03_Methodology.md) (**Report No.3** — 20% Điểm quá trình):
  - Phương pháp luận thu thập, lọc nhiễu và thuật toán Group-Aware Splitting.
  - Cơ sở toán học TF-IDF Character n-grams và phương pháp huấn luyện Baseline ML.
  - Kiến trúc phân tầng 2 Phase (Offline Training vs. Online Inference). — *Phụ trách: Đức & Trường*
- [ ] **T19**: Thiết kế slide thuyết trình Review 2 (Methodology & Baseline ML). — *Phụ trách: Phương*

#### Tuần 8 (26/10/2026 – 01/11/2026): CỘT MỐC 2 — BẢO VỆ REVIEW 2 TRƯỚC GVHD
- [ ] **T20**: Nộp **Report No. 3 (Methodology)** cho GVHD (20% Điểm đánh giá quá trình). — *Phụ trách: Trường (Leader)*
- [ ] **T21**: **BẢO VỆ REVIEW 2 TRƯỚC GVHD**: Báo cáo phương pháp luận kỹ thuật dữ liệu, chứng minh hiệu quả thuật toán Group-Aware Splitting và kết quả Baseline ML. — *Phụ trách: Cả 4 thành viên*
- [ ] **T22**: Tiếp thu góp ý của GVHD, cập nhật file Excel tiến độ tuần và chuẩn bị bước vào Giai đoạn Transformer. — *Phụ trách: Cả 4 thành viên*

---

### ⚡ GIAI ĐOẠN 3: TRANSFORMER, LƯỢNG HÓA INT8 & PROTOTYPE (TUẦN 9 - TUẦN 13: 02/11/2026 – 06/12/2026)

#### Tuần 9 (02/11/2026 – 08/11/2026): Fine-Tuning Transformer DeBERTa-v3
- [ ] **T23**: Thiết lập pipeline Supervised Fine-Tuning mô hình `microsoft/deberta-v3-base` sử dụng PyTorch & Hugging Face Transformers. — *Phụ trách: Việt*
- [ ] **T24**: Tích hợp module tăng cường đối kháng (`ObfuscationGenerator`) trong quá trình huấn luyện: tiêm Leetspeak, Spacing và Base64 vào tập Train. — *Phụ trách: Việt & Trường*
- [ ] **T25**: Tinh chỉnh siêu tham số (Learning Rate, Warmup Steps, Weight Decay, Dropout) và hàm mất mát `BCEWithLogitsLoss`. — *Phụ trách: Việt*

#### Tuần 10 (09/11/2026 – 15/11/2026): Lượng Hóa Động ONNX INT8 & Kiểm Thử Độ Bền Evasion
- [ ] **T26**: Xuất mô hình sang định dạng ONNX và thực hiện lượng hóa động Post-Training Quantization sang INT8 (ZeroQuant). — *Phụ trách: Việt*
- [ ] **T27**: Đo đạc thời gian suy luận (Latency Profiling): Khẳng định độ trễ P95 $< 18\text{ms}$ trên CPU thương mại, kích thước mô hình $< 150\text{MB}$. — *Phụ trách: Việt & Đức*
- [ ] **T28**: Chạy bộ kiểm thử đối kháng ngoại tuyến: Đo đạc ASR trước Leetspeak, Base64 và Spacing tricks, xác nhận $\Delta F_1 < 5\%$. — *Phụ trách: Việt*
- [ ] **T29**: Soạn thảo toàn văn [`docs/thesis/chapters/04_Experimental_and_Results.md`](file:///d:/Work/Do-an/docs/thesis/chapters/04_Experimental_and_Results.md) (**Report No.4** — 25% Điểm quá trình). — *Phụ trách: Việt & Đức*

#### Tuần 11 (16/11/2026 – 22/11/2026): Phát Triển FastAPI Guardrail Middleware & LLM Proxy
- [ ] **T30**: Xây dựng dịch vụ FastAPI bất đồng bộ (`async def`) đóng vai trò chốt chặn bảo vệ trước LLM. — *Phụ trách: Phương*
- [ ] **T31**: Hiện thực hóa cơ chế Early-Exit 2 tầng: Tầng 1 (TF-IDF Char n-grams) xử lý $85\%$ traffic siêu tốc ($< 3\text{ms}$); Tầng 2 (DeBERTa-v3 INT8) xử lý các mẫu nghi vấn. — *Phụ trách: Phương & Đức*
- [ ] **T32**: Tích hợp module giải mã ngầm Heuristic Base64 và tiền xử lý Unicode NFKC tại cổng vào API. — *Phụ trách: Phương & Trường*
- [ ] **T33**: Kết nối gọi API thực tế tới 5 Target LLMs (GPT-4o-mini, Gemini Flash, LLaMA-3.1, Mistral, Qwen). — *Phụ trách: Phương*

#### Tuần 12 (23/11/2026 – 29/11/2026): Phát Triển Streamlit Dashboard & Đóng Gói Docker
- [ ] **T34**: Xây dựng giao diện Dashboard tương tác trực quan bằng Streamlit:
  - Tab 1: Live Attack Testing (Thử nghiệm trực tiếp với ma trận 4 kịch bản demo).
  - Tab 2: Threat Monitoring & Audit Logs (Thống kê tấn công, xem log các prompt bị block).
  - Tab 3: Model Performance & Latency Metrics (Biểu đồ so sánh F1, ASR, Confusion Matrix, và đồng hồ đo độ trễ ms). — *Phụ trách: Phương*
- [ ] **T35**: Đóng gói toàn bộ hệ thống vào Docker Container (`docker-compose.yml` gồm FastAPI backend, Streamlit frontend và Ollama/API proxy). — *Phụ trách: Phương*
- [ ] **T36**: Chạy Stress-test và diễn tập kịch bản demo trực tiếp chuẩn bị cho Hội đồng Giữa kỳ. — *Phụ trách: Cả 4 thành viên*

#### Tuần 13 (30/11/2026 – 06/12/2026): CỘT MỐC 3 — BÁO CÁO HỘI ĐỒNG 1 (HỘI ĐỒNG GIỮA KỲ — INTERIM DEFENSE)
- [ ] **T37**: Nộp **Report No. 4 (Experimental and Results)** cho Hội đồng (25% Điểm đánh giá quá trình). — *Phụ trách: Trường (Leader)*
- [ ] **T38**: **BÁO CÁO TIẾN ĐỘ TRƯỚC HỘI ĐỒNG 1 (INTERIM DEFENSE)**:
  - Báo cáo kết quả huấn luyện Transformer DeBERTa-v3 và kết quả lượng hóa INT8.
  - Trình diễn Prototype thực tế trên giao diện Streamlit/FastAPI trước Hội đồng. — *Phụ trách: Cả 4 thành viên*
- [ ] **T39**: Tiếp thu ý kiến đóng góp của Hội đồng Giữa kỳ để định hướng hoàn thiện Luận văn tốt nghiệp. — *Phụ trách: Cả 4 thành viên*

---

### 🏆 GIAI ĐOẠN 4: THẢO LUẬN, HOÀN THIỆN LUẬN VĂN & CỘT MỐC 4 — BẢO VỆ TỐT NGHIỆP FINAL (TUẦN 14 - TUẦN 15: 07/12/2026 – 20/12/2026)

#### Tuần 14 (07/12/2026 – 13/12/2026): Soạn Thảo Report No. 5 & No. 6, Tổng Hợp Luận Văn 6 Chương
- [ ] **T40**: Soạn thảo toàn văn [`docs/thesis/chapters/05_Discussion.md`](file:///d:/Work/Do-an/docs/thesis/chapters/05_Discussion.md) (**Report No.5** — 15% Điểm quá trình): Phân tích sâu 3 đánh đổi kỹ thuật (Safety vs FPR, Latency vs Accuracy, Cost vs Resource) và bài học thực tiễn. — *Phụ trách: Phương & Đức*
- [ ] **T41**: Soạn thảo toàn văn [`docs/thesis/chapters/06_Conclusion_and_Future_Work.md`](file:///d:/Work/Do-an/docs/thesis/chapters/06_Conclusion_and_Future_Work.md) (**Report No.6** — 5% Điểm quá trình): Tổng kết các đóng góp mới, trả lời triệt để 3 RQs và định hướng phát triển trong tương lai. — *Phụ trách: Phương & Trường*
- [ ] **T42**: Chạy công cụ tổng hợp toàn văn Luận văn: `python scripts/compile_thesis.py` để xuất bản [`docs/thesis/FINAL_THESIS.md`](file:///d:/Work/Do-an/docs/thesis/FINAL_THESIS.md). — *Phụ trách: Trường (Leader)*
- [ ] **T43**: Kiểm tra tính toàn vẹn trích dẫn học thuật, rà soát đạo văn qua Turnitin (đảm bảo Similarity Index $< 20\%$). — *Phụ trách: Cả 4 thành viên*
- [ ] **T44**: Thiết kế bộ Slide bảo vệ tốt nghiệp chính thức (Final Defense Deck 25–30 slide). — *Phụ trách: Cả 4 thành viên*

#### Tuần 15 (14/12/2026 – 20/12/2026): CỘT MỐC 4 — BẢO VỆ TỐT NGHIỆP CHÍNH THỨC TRƯỚC HỘI ĐỒNG FINAL
- [ ] **T45**: Nộp toàn bộ hồ sơ khóa luận hoàn chỉnh (Báo cáo Luận văn 6 chương đóng bìa, đĩa CD/Source code, biên bản đánh giá của GVHD) về Văn phòng Khoa ATTT. — *Phụ trách: Trường (Leader)*
- [ ] **T46**: Tiến hành tập dượt tổng duyệt bảo vệ tốt nghiệp (Final Rehearsal 20 phút thuyết trình + 15 phút Q&A). — *Phụ trách: Cả 4 thành viên*
- [ ] **T47**: **BẢO VỆ TỐT NGHIỆP CHÍNH THỨC TRƯỚC HỘI ĐỒNG CHẤM KHÓA LUẬN FINAL** (Chiếm 50% Tổng điểm Khóa luận tốt nghiệp). — *Phụ trách: Cả 4 thành viên*
- [ ] **T48**: Tiếp thu góp ý cuối cùng của Hội đồng, nộp bản lưu chiểu chính thức và hoàn tất học phần tốt nghiệp IAP491. — *Phụ trách: Trường (Leader)*

---

## 📊 IV. BẢNG CHECKLIST KIỂM TOÁN CHẤT LƯỢNG NGHIỆM THU REVIEW 1 (NGÀY CHỐT: 06/09/2026)

Trước khi đóng tuần tiền đề vào ngày 06/09/2026 để bước vào học kỳ chính thức, nhóm trưởng và từng thành viên kiểm tra đủ 10 tiêu chí nghiệm thu:

| STT | Tiêu Chí Kiểm Toán Chất Lượng | Tiêu Chuẩn Nghiệm Thu Cụ Thể | Người Phụ Trách | Trạng Thái Thực Tế |
| :---: | :--- | :--- | :---: | :---: |
| 1 | **Problem Statement** | Nêu rõ bản chất Lỗ hổng Von Neumann trong Transformer ($X = S \mathbin{\Vert} U$). | Trường | [x] **ĐẠT (PASS)** |
| 2 | **Threat Taxonomy** | Bảng phân biệt 3 trục Direct Injection vs Indirect Injection vs Jailbreak theo OWASP LLM01:2025. | Trường | [x] **ĐẠT (PASS)** |
| 3 | **Threat Model & Surface** | Sơ đồ luồng tấn công NIST AI 100-2e2025; khóa chặt Attack Surface tại REST API `/v1/chat`. | Đức | [x] **ĐẠT (PASS)** |
| 4 | **3-Tier Layered Defense** | Thể hiện rõ Lớp 1 (Input Guardrail - trọng tâm đồ án), Lớp 2 (LLM), Lớp 3 (Output Sanitizer). | Đức | [x] **ĐẠT (PASS)** |
| 5 | **Robustness Design** | 3 tầng phòng thủ chống lẩn tránh cú pháp Leetspeak, Spacing tricks, Base64/Cipher. | Đức | [x] **ĐẠT (PASS)** |
| 6 | **Research Questions** | 3 RQs chuẩn IEEE và chuyên ngành ATTT (RQ1, RQ2, RQ3) gắn liền 3 Research Gaps. | Phương | [x] **ĐẠT (PASS)** |
| 7 | **Model Selection Matrix** | So sánh 4 hướng Guardrail + Lý do chọn 5 Target LLM Cloud API (kèm trích dẫn $\ge 2022$). | Việt | [x] **ĐẠT (PASS)** |
| 8 | **4 Demo Scenarios** | Ma trận $2 \times 2$ có đầy đủ prompt đầu vào, phản hồi vulnerable, JSON block và latency ms. | Việt | [x] **ĐẠT (PASS)** |
| 9 | **Slide PPTX Review 1** | Bộ slide hoàn chỉnh phân bổ 4 người trình bày trong 15 phút, thiết kế nhận diện FPT. | Phương | [ ] *Đang thực hiện (05/09)* |
| 10 | **Process Report & Nộp bài** | Cập nhật `PI_GUARD_PROCESS_REPORT.xlsx` và nộp Report No. 1 đúng hạn cho GVHD. | Trường | [ ] *Đang thực hiện (06/09)* |

---
*Tài liệu này là căn cứ pháp lý và quản trị nội bộ chính thức của nhóm PI-Guard, được xây dựng dựa trên biên bản họp `Meeting 1_29_08_26.md`, `Meeting 2_01_09_26.md` và tuân thủ 100% Quy chế Khóa luận Tốt nghiệp IAP491 Đại học FPT.*
