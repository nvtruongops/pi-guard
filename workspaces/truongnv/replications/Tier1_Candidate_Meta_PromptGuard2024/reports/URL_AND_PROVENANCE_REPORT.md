# Báo Cáo Xuất Xứ & Đường Dẫn Tải Gốc: Meta_PromptGuard2024

> **Đề tài**: PI-Guard (IAP491) | **Mô hình**: `Meta_PromptGuard2024`  
> **Vai trò trong đề tài**: M4 Baseline (Meta AI Purple Llama 2024)  

## 1. Chuỗi Xuất Xứ Học Thuật (Academic Provenance Chain)

- **Bài báo khoa học (Paper)**: [Prompt-Guard: An 86M Parameter Guardrail for Prompt Injection and Jailbreak](https://arxiv.org/abs/2407.21783)
- **Bản lưu trữ cục bộ (Local PDF)**: [`papers/Meta_2024_Prompt_Guard_86M_Input_Guardrail.pdf`](../papers/Meta_2024_Prompt_Guard_86M_Input_Guardrail.pdf)
- **Mã nguồn tác giả (Upstream Code)**: [https://github.com/meta-llama/PurpleLlama](https://github.com/meta-llama/PurpleLlama)
- **Thư mục repo gốc cục bộ**: [`upstream/`](../upstream/)
- **Tập dữ liệu kiểm thử (Datasets)**: [https://huggingface.co/meta-llama/Prompt-Guard-86M](https://huggingface.co/meta-llama/Prompt-Guard-86M)
- **Thư mục dữ liệu cục bộ**: [`datasets/`](../datasets/)

## 2. Kiểm Tra Toàn Vẹn Dữ Liệu Cục Bộ (SHA-256)

| Tên Tệp | Kích Thước (Bytes) | SHA-256 Checksum | Trạng Thái |
| :--- | :--- | :--- | :---: |
| `promptguard_3class_eval.json` | 653,310 | `8f00a063e184517e...` | **KHỚP 100%** |

## 3. Kết Quả Đo Đạc Thực Nghiệm

- Tệp kết quả benchmark đo đạc: [`META_PROMPTGUARD_REPLICATION_BENCHMARK_RESULTS.json`](./META_PROMPTGUARD_REPLICATION_BENCHMARK_RESULTS.json)
- Công cụ kiểm tra xuất xứ: [`workspaces/truongnv/scripts/check_replication_origin_urls.py`](../../scripts/check_replication_origin_urls.py)
