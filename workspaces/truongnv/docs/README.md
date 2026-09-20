# Cổng Tài Liệu Khoa Học & Luận Văn PI-Guard (TruongNV Docs Hub)

Hệ thống tài liệu tại thư mục [`workspaces/truongnv/docs/`](file:///d:/Work/Do-an/workspaces/truongnv/docs/) được cấu trúc chặt chẽ thành **2 Phân Hệ Độc Tôn** nhằm đảm bảo tính phân tách trách nhiệm (Separation of Concerns) giữa nền tảng nghiên cứu khoa học kỹ thuật và hồ sơ luận văn bảo vệ tốt nghiệp:

```text
workspaces/truongnv/docs/
├── research/    # [PHÂN HỆ 1] TẤT CẢ CHUYÊN ĐỀ NGHIÊN CỨU KHOA HỌC KỸ THUẬT (100% ACADEMIC GROUNDING)
└── thesis/      # [PHÂN HỆ 2] LUẬN VĂN TỐT NGHIỆP & HỒ SƠ BẢO VỆ CHÍNH THỨC TRƯỚC HỘI ĐỒNG FPT
```

---

## 🔬 Phân Hệ 1: Nghiên Cứu Khoa Học Kỹ Thuật ([`docs/research/`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/README.md))

Tập hợp toàn bộ cơ sở lý thuyết toán học, phân tích cơ chế tấn công, mô hình hóa đe dọa, thiết kế kiến trúc phân loại hai tầng (Two-Tier Guardrail), và các thực nghiệm đối sánh chuẩn mực:

1. **[`prompt_study/`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/prompt_study/)**: Chuyên đề 1 — Cơ sở LLM, Không gian Token phẳng & Xung đột chỉ thị.
2. **[`attack_study/`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/attack_study/)**: Chuyên đề 2 — Cơ chế Prompt Injection ($X = S \mathbin{\Vert} U$) & Taxonomy Jailbreak DAN.
3. **[`threat_and_defense_study/`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/threat_and_defense_study/)**: Chuyên đề 3 — Mô hình hóa đe dọa (NIST AI 100-2e2025, OWASP LLM01) & Phòng thủ 3 lớp Saltzer & Schroeder.
4. **[`dataset_and_benchmark_study/`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/dataset_and_benchmark_study/)**: Chuyên đề 4 — Tuyển chọn dữ liệu, Cân bằng lớp & Phân chia mẫu chống rò rỉ (Group-Aware Splitting).
5. **[`model_study/`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/model_study/)**: Chuyên đề 5 — Mô hình cơ sở cú pháp TF-IDF n-grams, Transformer ngữ nghĩa DeBERTa-v3 & Cơ chế phối hợp Cascade.
6. **[`robustness_study/`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/robustness_study/)**: Chuyên đề 6 — Độ bền đối kháng, Phân mảnh token BPE & Kỹ thuật lẩn tránh (Base64, Leetspeak, Spacing).
7. **[`evaluation_and_tradeoff_study/`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/evaluation_and_tradeoff_study/)**: Chuyên đề 7 — Kinh tế học False Positive Rate (FPR < 1.5%), Pareto Frontier & Đánh đổi kỹ thuật.
8. **[`comparative_analysis/`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/comparative_analysis/)**: Nghiên cứu đối chuẩn SOTA Guardrail, Lỗ hổng Target LLM APIs và Phân tích chuyên sâu công trình Tencent Zhuque Lab 2026.

👉 *Xem chi tiết mục lục và tóm tắt từng chuyên đề tại [`docs/research/README.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/README.md).*

---

## 🎓 Phân Hệ 2: Luận Văn & Hồ Sơ Bảo Vệ ([`docs/thesis/`](file:///d:/Work/Do-an/workspaces/truongnv/docs/thesis/README.md))

Tập hợp toàn văn các chương luận văn tốt nghiệp ngành An toàn Thông tin (IAP491) theo khung chuẩn 6 chương của Đại học FPT và hồ sơ bảo vệ từng giai đoạn (Review 1–4):

- **[`FINAL_THESIS.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/thesis/FINAL_THESIS.md)**: Bản biên dịch tích hợp toàn văn các chương luận văn tốt nghiệp.
- **[`Review1_Problem_Definition_and_Threat_Model.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/thesis/Review1_Problem_Definition_and_Threat_Model.md)**: Hồ sơ bảo vệ giai đoạn Review 1 (Mô hình bài toán, Phân tích đe dọa, Kiến trúc 3 lớp & Ma trận đối sánh).
- **[`chapters/`](file:///d:/Work/Do-an/workspaces/truongnv/docs/thesis/chapters/)**:
  - `01_Introduction.md`: Bối cảnh đề tài, Động lực nghiên cứu, 6 câu hỏi nghiên cứu (RQ1–RQ6) & Phạm vi đề tài.
  - `02_Literature_Review.md`: Tổng quan nghiên cứu học thuật theo 4 tầng xuất xứ (Tier 0–Tier 3) và 18 bài báo cốt lõi.
