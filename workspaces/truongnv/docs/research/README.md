# Phân Hệ Nghiên Cứu Khoa Học Kỹ Thuật (PI-Guard Research Hub)

Chào mừng bạn đến với **Phân hệ Nghiên cứu Khoa học Kỹ thuật (Research Hub)** của đồ án **PI-Guard** tại [`workspaces/truongnv/docs/research/`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/).

Toàn bộ các tài liệu trong phân hệ này được xây dựng theo nguyên tắc **100% Academic Grounding**, bám sát 18 bài báo khoa học bình duyệt chuẩn mực (NeurIPS, ICLR, ACM CCS, IEEE S&P) và các tiêu chuẩn bảo mật AI quốc tế (**NIST AI 100-2e2025**, **OWASP LLM01:2025**).

---

## 🗺️ Bản Đồ 7 Chuyên Đề Nghiên Cứu Chuyên Sâu (7 Scientific Study Suites)

```text
research/
├── prompt_study/                   # [CHUYÊN ĐỀ 1] LLM Foundations, Token Generation & Flat Boundary
├── attack_study/                   # [CHUYÊN ĐỀ 2] Prompt Injection & Modern Jailbreak Taxonomy
├── threat_and_defense_study/       # [CHUYÊN ĐỀ 3] NIST/OWASP Threat Model & 3-Tier Layered Defense
├── dataset_and_benchmark_study/    # [CHUYÊN ĐỀ 4] Data Curation, Balance & Group-Aware Splitting
├── model_study/                    # [CHUYÊN ĐỀ 5] TF-IDF Baseline, DeBERTa-v3 & Two-Tier Architecture
├── robustness_study/               # [CHUYÊN ĐỀ 6] Adversarial Obfuscation, Tokenizer Fragility & Evasion
├── evaluation_and_tradeoff_study/  # [CHUYÊN ĐỀ 7] False Positive Economics, Pareto Frontier & Trade-offs
└── comparative_analysis/           # [CHUYÊN KHẢO ĐỐI CHUẨN] SOTA Guardrails, Target LLMs & Tencent 2026
```

---

### 1. 🔤 Chuyên Đề 1: Prompt Study ([`prompt_study/`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/prompt_study/))
Nghiên cứu bản chất vật lý của LLM, cơ chế sinh token tự hồi quy và lỗ hổng ranh giới phẳng:
- [`01_llm_foundations_and_token_generation.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/prompt_study/01_llm_foundations_and_token_generation.md): Cơ sở toán học Transformer Causal Decoder, Cross-entropy Loss và ranh giới không phân tách giữa mã lệnh và dữ liệu.
- [`02_prompt_structure_and_chat_formats.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/prompt_study/02_prompt_structure_and_chat_formats.md): Cấu trúc prompt tiêu chuẩn, các định dạng hội thoại (ChatML, Llama-3 Template) và phân tích nguy cơ vượt rào qua token đặc biệt (`<|im_start|>`).
- [`03_instruction_hierarchy_and_flat_boundary.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/prompt_study/03_instruction_hierarchy_and_flat_boundary.md): Lý thuyết phân cấp chỉ thị (Instruction Hierarchy), lỗ hổng Flat Token Space và mô hình hóa xung đột $X = S \mathbin{\Vert} U$.
- [`04_resources_and_papers.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/prompt_study/04_resources_and_papers.md): Danh mục tài liệu học thuật và bài báo gốc về Transformer & Instruction Tuning.

---

### 2. 🛡️ Chuyên Đề 2: Attack Study ([`attack_study/`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/attack_study/))
Nghiên cứu toàn diện về cơ chế tấn công Prompt Injection và bẻ khóa Jailbreak:
- **`00_overview_threat_and_scope/`**:
  - [`history_and_evolution.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/attack_study/00_overview_threat_and_scope/history_and_evolution.md): Lịch sử tiến hóa từ Causal LM thuần túy đến Instruction-Tuned RLHF và sự xuất hiện của các vector tấn công prompt.
  - [`scope_and_boundary_analysis.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/attack_study/00_overview_threat_and_scope/scope_and_boundary_analysis.md): Phân định phạm vi đề tài, ranh giới giữa kiểm tra văn bản đầu vào (Text-level Guardrail) và các tấn công trọng số/phần cứng.
- **`01_prompt_injection/`**:
  - [`how_it_works_and_mechanisms.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/attack_study/01_prompt_injection/how_it_works_and_mechanisms.md): Cơ chế ghi đè mục tiêu (Goal Hijacking), rò rỉ dữ liệu (Prompt Leaking) qua phép nối chuỗi $X = S \mathbin{\Vert} U$.
  - [`taxonomy_and_variants.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/attack_study/01_prompt_injection/taxonomy_and_variants.md): Phân loại 13 biến thể Direct vs. Indirect Prompt Injection (Web, PDF, API, SQL).
  - [`resources_and_papers.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/attack_study/01_prompt_injection/resources_and_papers.md): Danh mục bài báo bình duyệt về Prompt Injection (Greshake et al., Perez & Ribeiro).
- **`02_modern_jailbreak_attacks/`**:
  - [`archetypes_and_mechanisms.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/attack_study/02_modern_jailbreak_attacks/archetypes_and_mechanisms.md): 4 trường phái Jailbreak kinh điển: DAN (Do Anything Now), Nhập vai đối lập (Roleplay), Giả lập máy ảo Linux (VM), và Biến đổi mật mã (Cipher).
  - [`datasets_benchmarks_and_taxonomy.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/attack_study/02_modern_jailbreak_attacks/datasets_benchmarks_and_taxonomy.md): Master Taxonomy 10 họ Jailbreak, bộ dữ liệu chuẩn Shen et al. và AdvGLUE.
  - [`advanced_variants_and_operators.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/attack_study/02_modern_jailbreak_attacks/advanced_variants_and_operators.md): Kỹ thuật tấn công tiên tiến: Many-shot Jailbreaking (Anthropic), GCG tự động (Zou et al.) và 26 Toán tử tấn công của Tencent Zhuque Lab (2026).
  - [`resources_and_papers.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/attack_study/02_modern_jailbreak_attacks/resources_and_papers.md): Tài liệu học thuật và open-access PDF về Jailbreak.

---

### 3. 🎯 Chuyên Đề 3: Threat & Defense Study ([`threat_and_defense_study/`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/threat_and_defense_study/))
Mô hình hóa đe dọa và kiến trúc bảo vệ đa tầng:
- [`01_threat_model_and_attack_surface.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/threat_and_defense_study/01_threat_model_and_attack_surface.md): Mô hình đe dọa chuẩn mực (NIST AI 100-2e2025, OWASP LLM01:2025, STRIDE / DREAD định lượng), 3 hồ sơ Attacker và 4 điểm chạm Attack Surface.
- [`02_multi_layer_defense_architecture.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/threat_and_defense_study/02_multi_layer_defense_architecture.md): Phân tích chi tiết 3 lớp phòng thủ (Lớp 1 PI-Guard Input Gateway, Lớp 2 Target LLM Enclosure, Lớp 3 Output Sanitizer & Canary Token) tuân thủ nguyên lý Saltzer & Schroeder (1975).
- [`03_comparative_matrix_and_tradeoffs.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/threat_and_defense_study/03_comparative_matrix_and_tradeoffs.md): Ma trận so sánh định lượng 6 giải pháp bảo vệ và phân tích sâu 3 đánh đổi cốt lõi (Bảo mật vs Độ trễ vs False Positive Rate).
- [`04_resources_and_papers.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/threat_and_defense_study/04_resources_and_papers.md): Bảng 10 công trình khoa học nền tảng, video bài giảng oEmbed và mã nguồn Python mẫu thực nghiệm 3 lớp phòng thủ.

---

### 4. 📊 Chuyên Đề 4: Dataset & Benchmark Study ([`dataset_and_benchmark_study/`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/dataset_and_benchmark_study/))
Kỹ thuật dữ liệu, chống rò rỉ và phân chia mẫu đánh giá:
- [`01_data_curation_and_class_balance.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/dataset_and_benchmark_study/01_data_curation_and_class_balance.md): Thu thập đa nguồn (Deepset, JailbreakBench, BeaverTails), lọc trùng lặp ngữ nghĩa (MinHash LSH), cân bằng tỷ lệ nhãn và chiến lược dữ liệu thực tế.
- [`02_group_aware_splitting_and_ood.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/dataset_and_benchmark_study/02_group_aware_splitting_and_ood.md): Kỹ thuật Group-Aware Splitting ngăn ngừa Data Leakage giữa các biến thể prompt diễn giải (paraphrases) và thiết lập tập kiểm thử ngoại miền (OOD Test Set).
- [`03_resources_and_papers.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/dataset_and_benchmark_study/03_resources_and_papers.md): Danh mục bộ dữ liệu công khai, liên kết Hugging Face và chuẩn đánh giá.

---

### 5. 🔬 Chuyên Đề 5: Model Study ([`model_study/`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/model_study/))
Toán học và cơ chế hoạt động của mô hình cơ sở cú pháp và Transformer ngữ nghĩa:
- **`01_tfidf_syntactic_baseline/`**:
  - [`theory_and_math.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/model_study/01_tfidf_syntactic_baseline/theory_and_math.md): Cơ sở toán học TF-IDF, Character n-grams (`char_wb`), định lý Luhn (1958), Spärck Jones (1972) và Jain et al. (2023).
  - [`how_it_works_and_usage.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/model_study/01_tfidf_syntactic_baseline/how_it_works_and_usage.md): Hướng dẫn tiền xử lý, trích xuất đặc trưng và tối ưu hóa bộ phân loại tuyến tính (LogisticRegression / LinearSVC).
  - [`resources_and_videos.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/model_study/01_tfidf_syntactic_baseline/resources_and_videos.md): Tài liệu tham khảo và video bài giảng về TF-IDF.
- **`02_deberta_v3_semantic_classifier/`**:
  - [`theory_and_math.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/model_study/02_deberta_v3_semantic_classifier/theory_and_math.md): Toán học Disentangled Attention (He et al., ICLR 2023), Enhanced Mask Decoder và Lượng hóa động ONNX INT8 (Yao et al., NeurIPS 2022).
  - [`how_it_works_and_usage.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/model_study/02_deberta_v3_semantic_classifier/how_it_works_and_usage.md): Fine-tuning chiến lược với Weighted Cross-Entropy Loss và xuất mô hình ONNX Runtime.
  - [`resources_and_videos.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/model_study/02_deberta_v3_semantic_classifier/resources_and_videos.md): Tài liệu học thuật và tài nguyên trực quan về DeBERTa-v3.
- **`03_two_tier_pipeline_coordination/`**:
  - [`how_it_works_and_architecture.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/model_study/03_two_tier_pipeline_coordination/how_it_works_and_architecture.md): Nguyên lý kiến trúc phối hợp Cascade: Tier 1 Fast Filter (< 2ms) chặn 70-80% truy vấn rõ ràng, Tier 2 Deep Semantic Resolver (< 25ms) thẩm định vùng nghi vấn.
  - [`benchmark_and_tradeoffs.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/model_study/03_two_tier_pipeline_coordination/benchmark_and_tradeoffs.md): Bảng phân tích thực nghiệm so sánh phương án đơn lẻ vs. kiến trúc kép phối hợp.

---

### 6. 🧱 Chuyên Đề 6: Robustness Study ([`robustness_study/`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/robustness_study/))
Nghiên cứu độ bền đối kháng và các kỹ thuật lẩn tránh bộ lọc:
- [`01_theory_and_evasion_mechanisms.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/robustness_study/01_theory_and_evasion_mechanisms.md): Cơ sở lý thuyết lỗ hổng phân mảnh token (BPE / WordPiece) và 3 kỹ thuật lẩn tránh cốt lõi: Leetspeak, Base64/Hex encoding, và Zero-width Spacing.
- [`02_defense_architecture_and_mitigation.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/robustness_study/02_defense_architecture_and_mitigation.md): Kiến trúc phòng thủ đối kháng 3 tầng: Tầng 0 Tiền xử lý chuẩn hóa Unicode & Heuristic decoder, Tầng 1 Sub-word n-grams, Tầng 2 Huấn luyện tăng cường mẫu đối kháng (Adversarial Data Augmentation).
- [`03_benchmarks_metrics_and_tradeoffs.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/robustness_study/03_benchmarks_metrics_and_tradeoffs.md): Hệ thống chỉ số đánh giá độ bền ($\Delta F_1$, Attack Success Rate under Perturbation - ASR, FPR Shift) và bảng đối sánh định lượng.
- [`04_resources_and_papers.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/robustness_study/04_resources_and_papers.md): Tài liệu học thuật chuẩn mực và hướng dẫn chạy mã nguồn kiểm thử độ bền.

---

### 7. ⚖️ Chuyên Đề 7: Evaluation & Trade-off Study ([`evaluation_and_tradeoff_study/`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/evaluation_and_tradeoff_study/))
Kinh tế học False Positive và tối ưu hóa đa mục tiêu:
- [`01_false_positive_economics_and_ux.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/evaluation_and_tradeoff_study/01_false_positive_economics_and_ux.md): Phân tích thiệt hại kinh tế của False Positive trong môi trường doanh nghiệp (User Churn, Support Ticket Cost) và luận giải khoa học cho ngưỡng bắt buộc $\text{FPR} < 1.5\%$.
- [`02_pareto_frontier_and_system_tradeoffs.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/evaluation_and_tradeoff_study/02_pareto_frontier_and_system_tradeoffs.md): Mô hình hóa đường biên Pareto tối ưu 3 chiều giữa Độ chính xác phát hiện (F1 / Recall), Tỷ lệ báo động giả (FPR) và Độ trễ tính toán (P95 Latency).
- [`03_resources_and_papers.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/evaluation_and_tradeoff_study/03_resources_and_papers.md): Tài nguyên nghiên cứu về Pareto Optimization và phân tích chi phí an ninh thông tin.

---

### 8. 🔍 Chuyên Khảo Đối Chuẩn SOTA ([`comparative_analysis/`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/comparative_analysis/))
Các báo cáo phân tích chuyên sâu hỗ trợ quyết định kiến trúc:
- [`State_of_the_Art_Guardrail_and_Jailbreak_Benchmarks_Analysis.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/comparative_analysis/State_of_the_Art_Guardrail_and_Jailbreak_Benchmarks_Analysis.md): Phân tích toàn cảnh các giải pháp Guardrail hàng đầu thế giới (Llama Guard, NeMo Guardrails, Guardrails AI, Lakera Guard) và chỉ rõ khoảng trống công nghệ mà PI-Guard lấp đầy.
- [`Target_LLM_API_Benchmark_and_Vulnerability_Analysis.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/comparative_analysis/Target_LLM_API_Benchmark_and_Vulnerability_Analysis.md): Đánh giá lỗ hổng thực nghiệm trên các API LLM phổ biến (OpenAI GPT-4o, Anthropic Claude 3.5, Google Gemini 1.5, Meta Llama 3) khi chưa có lớp bảo vệ.
- [`Tencent2026_Paper_Analysis_and_Mapping_to_PIGuard.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/comparative_analysis/Tencent2026_Paper_Analysis_and_Mapping_to_PIGuard.md): Phân tích chuyên sâu công trình nghiên cứu của Tencent Zhuque Lab (2026) về 26 Toán tử tấn công Jailbreak và ánh xạ vào tập luật đánh giá của PI-Guard.
- [`Why_Dual_Model_Architecture_TFIDF_and_DeBERTaV3.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/comparative_analysis/Why_Dual_Model_Architecture_TFIDF_and_DeBERTaV3.md): Luận giải khoa học và thực nghiệm chứng minh vì sao kiến trúc phối hợp Hybrid TF-IDF + DeBERTa-v3 vượt trội so với các kiến trúc đơn lẻ.
