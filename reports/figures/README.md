# Danh Mục & Cấu Trúc Hình Ảnh Báo Cáo (Reports Figures)
## Dự án: PI-Guard — A Machine-Learning Guardrail for Detecting Prompt Injection and Jailbreak Attacks on LLM Applications

---

## 📌 Nguyên Tắc Tổ Chức Thư Mục

Để phục vụ quản lý khoa học, tránh sự phân tán và chồng chéo hình ảnh giữa các bài báo cáo, thuyết trình hoặc các mốc đánh giá khác nhau, thư mục `reports/figures/` được phân cấp theo từng tài liệu nguồn cụ thể:

```
reports/figures/
├── README.md                      # Tài liệu tổng quan cấu trúc hình ảnh
└── PI-GUARD-Present-109/          # 12 hình ảnh trích xuất từ báo cáo tiến độ PI-GUARD-Present-109.pptx
    ├── slide04_promptinject_framework_perez2022.png
    ├── slide05_jailbreak_dan_structure_shen2024.png
    ├── slide08_layer1_data_exfiltration_greshake2023.png
    ├── slide09_layer2_agent_hijacking_greshake2023.png
    ├── slide10_layer3_denial_of_wallet_greshake2023.png
    ├── slide11_layer4_legal_compliance_greshake2023.png
    ├── slide12_threat_model_agent_surface_tencent2026.png
    ├── slide14_sota_guardrails_comparison_piguard.png
    ├── slide16_tier1_tfidf_ngram_mechanism_jain2023.png
    ├── slide17_tier2_deberta_disentangled_onnx_he2023.png
    ├── slide18_twotier_cascaded_architecture_saltzer1975.png
    └── slide19_matrix_2x2_unprotected_vs_piguard.png
```

Khi nhóm bổ sung các bài thuyết trình hoặc tài liệu báo cáo mới (ví dụ: `Review1-Presentation/`, `Review2-Presentation/`, v.v.), hình ảnh trích xuất sẽ được lưu trữ trong một thư mục con tương ứng mang tên tài liệu đó.

---

## 📊 Thư Mục Con Hiện Có

1. [`PI-GUARD-Present-109/`](file:///d:/Work/Do-an/reports/figures/PI-GUARD-Present-109/):
   - **Tài liệu nguồn**: [`reports/PI-GUARD-Present-109.pptx`](file:///d:/Work/Do-an/reports/PI-GUARD-Present-109.pptx)
   - **Nội dung**: 12 hình ảnh minh họa cơ chế tấn công (Prompt Injection, Jailbreak), 4 tầng thiệt hại, mô hình đe dọa (Threat Model) và kiến trúc phòng thủ 2 tầng (Two-Tier Cascaded Guardrail).
   - **Bản mô tả chi tiết**: Xem tại [`workspaces/truongnv/reports/figures/README.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/figures/README.md).
