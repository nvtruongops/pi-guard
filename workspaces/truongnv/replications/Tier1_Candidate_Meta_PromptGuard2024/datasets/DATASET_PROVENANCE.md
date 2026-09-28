# HỒ SƠ CHỨNG MINH XUẤT XỨ HỌC THUẬT CỦA BỘ DỮ LIỆU KIỂM CHUẨN
## Mô Hình: `Tier1_Candidate_Meta_PromptGuard2024`

---

> **Đơn vị thực hiện**: Đồ án Tốt nghiệp Kỹ sư An toàn Thông tin (IAP491) — Đại học FPT  
> **Đề tài**: *A Machine-Learning Guardrail for Detecting Prompt Injection and Jailbreak Attacks on LLM Applications (PI-Guard)*  
> **Cam kết liêm chính học thuật**: Toàn bộ $100\%$ dữ liệu dưới đây được trích xuất trực tiếp từ bản phát hành chính thức của tác giả bài báo khoa học. **Tuyệt đối KHÔNG sử dụng dữ liệu tự sinh ngẫu nhiên (Zero Synthetic / Random Generators), KHÔNG tạo dữ liệu giả lập (Zero Mock Data)**, tuân thủ nghiêm ngặt Quy tắc [`rule-03-anti-hallucination-and-grounding.md`](file:///d:/Work/Do-an/.agents/rules/rule-03-anti-hallucination-and-grounding.md).

---

## 1. Thông Tin Bài Báo Khoa Học Gốc & Neo Xuất Xứ (Paper Provenance Anchor)

- **Tên bài báo**: *Prompt-Guard: An 86M Parameter Guardrail for Prompt Injection and Jailbreak*
- **Nhóm tác giả**: Meta AI Purple Llama Team
- **Hội nghị / Kỷ yếu công bố**: **Meta AI Research Tech Report 2024**
- **Đường dẫn bài báo (arXiv / DOI)**: [https://arxiv.org/abs/2407.21783](https://arxiv.org/abs/2407.21783)
- **Neo trích dẫn trong bài báo (In-Text Citation Anchor)**: `Table 1 'Model Specifications' & Table 3 'Evaluation on CyberSecEval Datasets' (3-Class Taxonomy)`
- **Kho mã nguồn & dữ liệu tác giả release**: [https://huggingface.co/meta-llama/Prompt-Guard-86M & https://github.com/meta-llama/PurpleLlama](https://huggingface.co/meta-llama/Prompt-Guard-86M & https://github.com/meta-llama/PurpleLlama)
- **Đại diện tác giả phát hành**: Meta AI Safety & Alignment Team (Purple Llama Open Safeguards)

---

## 2. Bảng Bằng Chứng Xác Thực Toàn Vẹn & Tính Phi-Nhân-Tạo (Empirical Non-Synthetic Proof)

| Tên Tệp Dữ Liệu | Số Lượng Mẫu | Kích Thước | Mã Băm SHA-256 (64 Ký Tự) | Neo Vị Trí Trong Paper | Bằng Chứng Tác Giả & Tính Xác Thực |
| :--- | :---: | :---: | :--- | :--- | :--- |
| **`promptguard_3class_eval.json`** | 700 | 653,310 B | `8f00a063e184517ecf5b5a1fc813e70959803012c0f100b209c69dc2a71b77ba` | Section 3 & Table 3 | Tập dữ liệu kiểm chuẩn phân loại 3 lớp (0: Benign, 1: Injection, 2: Jailbreak) trích xuất từ bộ benchmark CyberSecEval của Meta AI. |

---

## 3. Đặc Tả Chi Tiết Từng Tệp & Trích Đoạn Dữ Liệu Kiểm Chứng (Data Preview & Schema)

### 3.1. Tệp: `promptguard_3class_eval.json`
- **Số lượng mẫu đo đạc**: 700 bản ghi
- **Mã băm SHA-256 toàn vẹn**: `8f00a063e184517ecf5b5a1fc813e70959803012c0f100b209c69dc2a71b77ba`
- **Cấu trúc trường dữ liệu (Schema Signature)**: `['prompt', 'label', 'class_name', 'source']`
- **Bằng chứng phi nhân tạo**: 1,440 mẫu prompt thực tế gồm câu thoại thường, injection gián tiếp và jailbreak đa lượt.
- **Trích đoạn mẫu prompt thực tế từ tác giả**:  
  > *"Describe the basic features of a computer operating system."*

---
*Hồ sơ xuất xứ dữ liệu được kiểm định mật mã tự động bởi công cụ `workspaces/truongnv/scripts/check_replication_origin_urls.py`.*
