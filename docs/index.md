# 🛡️ PI-Guard: LLM Security Guardrail
## Hệ Thống 8 Chuyên Đề Nghiên Cứu Khoa Học & Báo Cáo Khóa Luận

> **Đồ án Khóa luận Tốt nghiệp Đại học FPT** — Chuyên ngành An toàn Thông tin (Information Assurance)<br>
> **Mã đề tài**: `IAP491_FA26_PI_GUARD` | **Năm học**: 2026<br>
> **Chủ đề**: A Machine-Learning Guardrail for Detecting Prompt Injection and Jailbreak Attacks on LLM Applications

---

## 🎯 Giới Thiệu & Mục Tiêu Đề Tài

**PI-Guard** là hệ thống bảo vệ (guardrail) trung gian đặt trước các ứng dụng mô hình ngôn ngữ lớn (LLM), hoạt động theo cơ chế **hai tầng bảo vệ (Two-Tier Cascade Architecture)**:

1. **Tier 1 (Bộ lọc Cú pháp - Syntactic Baseline)**: Sử dụng phương pháp vector hóa TF-IDF kết hợp mô hình phân loại tuyến tính siêu nhẹ (Linear Classifier) nhằm nhận diện các mẫu prompt injection phổ biến với độ trễ cực thấp (**< 1.0 ms**).
2. **Tier 2 (Bộ lọc Ngữ nghĩa Sâu - Semantic Transformer)**: Sử dụng Transformer tiên tiến (**DeBERTa-v3**) với cơ chế Disentangled Attention, được lượng hóa qua **ONNX Runtime INT8** nhằm phát hiện các biến thể tấn công tinh vi, jailbreak ẩn ngữ cảnh với độ trễ mục tiêu **P95 < 25 ms**.

---

## 🌟 Sơ Đồ Luồng Phòng Thủ 2 Tầng (Mermaid)

```mermaid
flowchart TD
    UserPrompt(["📥 User Prompt"]) --> P1["⚙️ Tiền xử lý & Chuẩn hóa Unicode"]
    P1 --> T1{"⚡ Tier 1: TF-IDF Syntactic Gate"}

    T1 -- "Nguy hiểm (Score >= 0.85)" --> Block1["🚫 Chặn ngay (< 1ms)"]
    T1 -- "Lành tính (Score <= 0.15)" --> Pass1["✅ Cho phép chuyển đến LLM"]
    T1 -- "Nghi vấn (0.15 < Score < 0.85)" --> T2["🧠 Tier 2: DeBERTa-v3 Semantic Gate"]

    T2 -- "Phát hiện Injection / Jailbreak" --> Block2["🚫 Chặn tấn công ngữ nghĩa"]
    T2 -- "Lành tính an toàn" --> Pass2["✅ Chấp thuận cho phép"]

    Pass1 --> LLM["🤖 Target LLM (GPT-4o / Claude 3.5 / Gemini)"]
    Pass2 --> LLM
    LLM --> OutFilter["🔍 Output Security Guardrail"]
    OutFilter --> SafeResponse(["📤 Phản hồi an toàn đến người dùng"])

    style Block1 fill:#ff4d4f,color:#fff,stroke:#333,stroke-width:2px;
    style Block2 fill:#ff4d4f,color:#fff,stroke:#333,stroke-width:2px;
    style Pass1 fill:#52c41a,color:#fff,stroke:#333,stroke-width:2px;
    style Pass2 fill:#52c41a,color:#fff,stroke:#333,stroke-width:2px;
    style T1 fill:#1890ff,color:#fff,stroke:#333,stroke-width:2px;
    style T2 fill:#722ed1,color:#fff,stroke:#333,stroke-width:2px;
```

---

## 📋 Hệ Thống 8 Chuyên Đề Nghiên Cứu Khoa Học Trọng Điểm

| Chuyên Đề Khoa Học | Trọng Tâm Nghiên Cứu | Đường Dẫn Tra Cứu |
| :--- | :--- | :--- |
| **1. Prompt Study** | Bản chất LLM, Attention, Ranh giới phẳng và Thất bại Phân cấp Chỉ thị (Instruction Hierarchy) | [Xem Prompt Study](prompt_study/llm_foundations.md) |
| **2. Attack Study** | Phân loại toàn diện Prompt Injection & 4 trường phái Jailbreak (DAN, Roleplay, VM, Cipher) | [Xem Attack Study](attacks/history_and_evolution.md) |
| **3. Threat & Defense** | Mô hình hóa đe dọa NIST AI 100-2e2025, STRIDE, Kiến trúc phòng thủ đa tầng (Defense-in-Depth) | [Xem Threat & Defense](threat_defense/threat_model_and_attack_surface.md) |
| **4. Dataset & Benchmark** | Tuyển chọn dữ liệu 3 lớp, Khử trùng lặp MinHash, Group-Aware Splitting & Đánh giá OOD | [Xem Dataset Study](dataset_study/data_curation.md) |
| **5. Model Study** | Toán học TF-IDF, Transformer DeBERTa-v3 Disentangled Attention & Định tuyến bất định 2 tầng | [Xem Model Study](models/two_tier_architecture.md) |
| **6. Robustness Study** | Chống chịu kỹ thuật làm mờ (Leetspeak, Homoglyphs, Base64) & Tiền xử lý chuẩn hóa 4 bước | [Xem Robustness Study](robustness/theory_and_evasion_mechanisms.md) |
| **7. Optimization Study** | Lý thuyết lượng tử hóa INT8 PTQ, Tăng tốc ONNX Runtime Graph & Phân vị độ trễ P95/P99 | [Xem Optimization Study](optimization/quantization_math.md) |
| **8. Evaluation & Trade-offs** | Kinh tế học cảnh báo sai (FPR Economics), Điểm hoạt động Recall@FPR1% & Đường cong biên Pareto | [Xem Evaluation Study](evaluation_study/false_positive_economics.md) |

---

## 👥 Đội Ngũ Thực Hiện Đề Tài

> **Phương châm làm việc toàn đội**: **Ai cũng làm $ightarrow$ Tham khảo nhau $ightarrow$ Chốt kết quả**  
> Cả 4 thành viên đều trực tiếp thực hiện toàn trình (Full-Pipeline Hands-on) từ tiền xử lý dữ liệu, thử nghiệm Baseline ML, huấn luyện Transformer, đo đạc độ bền Evasion đến tích hợp API/Dashboard và bảo vệ Luận văn.

| STT | Thành Viên | Mã Sinh Viên | Khám Phá Toàn Trình & Đầu Mối Điều Phối |
| :---: | :--- | :--- :---: | :--- |
| 1 | **Nguyễn Văn Trường (Leader)** | `SE182034` | **Toàn trình Full-Pipeline** — Điều phối chung, Chuẩn hóa dữ liệu & Kiến trúc |
| 2 | **Nguyễn Quí Đức** | `SE182087` | **Toàn trình Full-Pipeline** — Đối sánh mô hình Baseline ML & Threat Model |
| 3 | **Phạm Minh Hoàng Việt** | `SE181851` | **Toàn trình Full-Pipeline** — Tối ưu Transformer & Thực nghiệm Robustness |
| 4 | **Đỗ Đoàn Duy Phương** | `SE180235` | **Toàn trình Full-Pipeline** — Tích hợp hệ thống API/Dashboard & Luận văn |

**Giảng viên hướng dẫn**: Đại học FPT — Khoa An toàn Thông tin (Information Assurance).
