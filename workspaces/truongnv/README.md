# WORKSPACE CÁ NHÂN — NGUYỄN VĂN TRƯỜNG (LEADER)
## Không Gian Quản Lý Dữ Liệu, Hồ Sơ Kỹ Thuật & Bản Thảo Luận Văn Review 1

Chào Trường! Toàn bộ các tài liệu, hồ sơ kỹ thuật, dữ liệu và biên bản họp do bạn khởi tạo đã được chuyển và đồng bộ vào không gian làm việc này để bạn tiếp tục tinh chỉnh trước khi cả nhóm chốt bản Final Report Review 1.

---

### 📂 1. DANH MỤC HỒ SƠ & BÁO CÁO REVIEW 1 TRONG WORKSPACE CỦA BẠN:

- 📘 **Bản thảo Luận văn Review 1**:
  - [`docs/thesis/chapters/01_Introduction.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/thesis/chapters/01_Introduction.md): Toàn văn Chương 1 (Introduction & Threat Model).
  - [`docs/thesis/chapters/02_Literature_Review.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/thesis/chapters/02_Literature_Review.md): Toàn văn Chương 2 (Literature Review & SOTA Survey).
  - [`docs/thesis/chapters/README.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/thesis/chapters/README.md): Lộ trình biên soạn 6 chương theo chuẩn FPT IAP491.
  - [`docs/thesis/Review1_Problem_Definition_and_Threat_Model.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/thesis/Review1_Problem_Definition_and_Threat_Model.md): Hồ sơ kỹ thuật Problem Definition & Threat Model.
  - [`docs/thesis/Review1_Presentation_Slides_Outline.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/thesis/Review1_Presentation_Slides_Outline.md): Dàn ý 9 slide thuyết trình 15 phút.
  - [`docs/thesis/FPT_IAP491_Capstone_Guidelines_and_Rubrics_Summary.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/thesis/FPT_IAP491_Capstone_Guidelines_and_Rubrics_Summary.md): Tóm tắt quy chế và tiêu chí chấm điểm FPT IAP491.
  - [`docs/thesis/FINAL_THESIS.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/thesis/FINAL_THESIS.md): Bản biên dịch toàn văn các chương Review 1.

- 🛡️ **Chuyên Đề Nghiên Cứu Tấn Công (Attack Study Suite — 100% Academic Grounding)**:
  - [`docs/attack_study/00_overview_threat_and_scope/`](file:///d:/Work/Do-an/workspaces/truongnv/docs/attack_study/00_overview_threat_and_scope/): Lịch sử tiến hóa (Causal LM vs Instruction Tuning) & Phân tích ranh giới kỹ thuật.
  - [`docs/attack_study/01_prompt_injection/`](file:///d:/Work/Do-an/workspaces/truongnv/docs/attack_study/01_prompt_injection/): Cơ chế ranh giới phẳng ($X = S \mathbin{\Vert} U$) & Toàn bộ 13 biến thể Direct / Indirect Injection.
  - [`docs/attack_study/02_modern_jailbreak_attacks/`](file:///d:/Work/Do-an/workspaces/truongnv/docs/attack_study/02_modern_jailbreak_attacks/): 4 trường phái cốt lõi (DAN, Roleplay, VM, Cipher), Master Taxonomy 10 họ Jailbreak và 26 Toán tử Tencent.

- 🧱 **Chuyên Đề Nghiên Cứu Độ Bền & Lẩn Tránh (Robustness Study Suite — 100% Academic Grounding)**:
  - [`docs/robustness_study/01_theory_and_evasion_mechanisms.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/robustness_study/01_theory_and_evasion_mechanisms.md): Cơ sở lý thuyết, lỗ hổng phân mảnh token (BPE/WordPiece) và 3 kỹ thuật cốt lõi (Leetspeak, Base64, Spacing).
  - [`docs/robustness_study/02_defense_architecture_and_mitigation.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/robustness_study/02_defense_architecture_and_mitigation.md): Kiến trúc phòng thủ 3 tầng (Tầng 0: Tiền xử lý & Khử nhiễu, Tầng 1: Character n-grams TF-IDF, Tầng 2: DeBERTa-v3 tăng cường đối kháng).
  - [`docs/robustness_study/03_benchmarks_metrics_and_tradeoffs.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/robustness_study/03_benchmarks_metrics_and_tradeoffs.md): Hệ thống tiêu chí định lượng ($\Delta F_1$, ASR, FPR, Latency), bảng đối sánh thực nghiệm và phân tích đánh đổi.
  - [`docs/robustness_study/04_resources_and_papers.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/robustness_study/04_resources_and_papers.md): Tài liệu học thuật chuẩn mực, video bài giảng YouTube oEmbed và hướng dẫn chạy mã nguồn thực nghiệm.

- 🔬 **Chuyên Đề Mô Hình & Toán Học (Model Study Suite — 100% Academic Grounding)**:
  - [`docs/model_study/01_tfidf_syntactic_baseline/`](file:///d:/Work/Do-an/workspaces/truongnv/docs/model_study/01_tfidf_syntactic_baseline/): Cơ sở toán học TF-IDF, Character n-grams (`char_wb`), Luhn (1958), Spärck Jones (1972) và Jain et al. (2023).
  - [`docs/model_study/02_deberta_v3_semantic_classifier/`](file:///d:/Work/Do-an/workspaces/truongnv/docs/model_study/02_deberta_v3_semantic_classifier/): Toán học Disentangled Attention (He et al., ICLR 2023) và Lượng hóa động ONNX INT8 (Yao et al., NeurIPS 2022).
  - [`docs/model_study/03_two_tier_pipeline_coordination/`](file:///d:/Work/Do-an/workspaces/truongnv/docs/model_study/03_two_tier_pipeline_coordination/): Nguyên lý phối hợp 2 mô hình (Cascade Defense) giải quyết triệt để 3 đánh đổi kỹ thuật.

- 📚 **Tài liệu tham khảo & Nghiên cứu Đối sánh SOTA**:
  - [`References/REFERENCES_LOG.md`](file:///d:/Work/Do-an/workspaces/truongnv/References/REFERENCES_LOG.md): Bảng ma trận 17 bài báo IEEE (100% >= 2022).
  - [`docs/research/`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/): Báo cáo đối sánh đa mô hình LLM mục tiêu, Tencent 2026 và luận giải kiến trúc kép Hybrid.

- 💾 **Dữ liệu nghiên cứu**:
  - [`data/manifests/`](file:///d:/Work/Do-an/workspaces/truongnv/data/manifests/): Taxonomies và manifests dữ liệu.
  - [`data/raw/`](file:///d:/Work/Do-an/workspaces/truongnv/data/raw/), [`data/processed/`](file:///d:/Work/Do-an/workspaces/truongnv/data/processed/), [`data/splits/`](file:///d:/Work/Do-an/workspaces/truongnv/data/splits/).

---

### 📌 QUY TRÌNH KHI CHỐT FINAL REPORT:
1. Bạn có thể tự do chỉnh sửa, bổ sung, format các file trong workspace này.
2. Khi nhóm họp xong và thống nhất chốt bản Final Report Review 1 $\rightarrow$ Đồng bộ phiên bản chính thức ra thư mục chung `docs/thesis/` và `Meeting/` để nộp cho Giảng viên hướng dẫn!
