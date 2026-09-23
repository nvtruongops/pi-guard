# ProtectAI DeBERTa-v3 (Prompt Injection Classifier v2) — Replication Package
## Public Triad: 100% Code, Weights & Public Benchmark Dataset

**Mô hình**: `protectai/deberta-v3-base-prompt-injection-v2`  
**Kiến trúc**: `DebertaV2ForSequenceClassification` (86M parameters, Disentangled Attention)  
**Nhà phát triển**: Protect AI Research (2024)  
**Hugging Face Hub**: [https://huggingface.co/protectai/deberta-v3-base-prompt-injection-v2](https://huggingface.co/protectai/deberta-v3-base-prompt-injection-v2)  
**Tài liệu khoa học liên quan**: He et al. (ICLR 2023 [[11]](#ref11)); Protect AI Open Threat Intelligence Report 2024.

---

### 1. Giới thiệu & Định vị trong Đồ án PI-Guard
Mô hình `protectai/deberta-v3-base-prompt-injection-v2` là mô hình SOTA mã nguồn mở phổ biến nhất hiện nay trên Hugging Face cho tác vụ phát hiện Prompt Injection (hơn 100,000 lượt tải/tháng). Mô hình được huấn luyện bằng cách tinh chỉnh `microsoft/deberta-v3-base` trên tập dữ liệu tổng hợp gồm Direct Prompt Injections, Jailbreaks, và các câu hỏi lành tính đa miền.

Trong đồ án PI-Guard, mô hình này đóng vai trò:
1. **Mốc đối chuẩn SOTA độc lập (Independent SOTA Baseline)**: Đánh giá xem mô hình tinh chỉnh nội bộ của nhóm có đạt hoặc vượt độ chính xác $F_1 \ge 0.95$ so với Protect AI hay không.
2. **Kiểm chứng tính khả thi trên CPU**: Đo đạc độ trễ suy luận thực tế (P95 Latency) của kiến trúc DeBERTa-v3 trên hạ tầng CPU không có GPU.
3. **Kiểm thử độ bền đối kháng**: Đánh giá độ suy giảm hiệu năng của Protect AI trước các biến dị cú pháp (Leetspeak, Spacing, Base64, Emoji smuggling) để làm rõ vì sao PI-Guard cần thiết kế bộ lọc 3 tầng có Tier-0 Scrubber và TF-IDF Baseline.

---

### 2. Cấu trúc Thư mục

```
ProtectAI_DeBERTa_v3_v2/
├── README.md                                 # Tài liệu đặc tả kỹ thuật mô hình
├── run_protectai_replication.py              # Script chạy thực nghiệm phân loại & đo độ trễ trên CPU
└── PROTECTAI_REPLICATION_BENCHMARK_RESULTS.json # Kết quả đo đạc thực nghiệm tự động
```

---

### 3. Hướng dẫn Tái lập Thực nghiệm (Reproducibility Command)

```powershell
d:\Work\Do-an\.venv\Scripts\python.exe workspaces/truongnv/replications/ProtectAI_DeBERTa_v3_v2/run_protectai_replication.py
```
