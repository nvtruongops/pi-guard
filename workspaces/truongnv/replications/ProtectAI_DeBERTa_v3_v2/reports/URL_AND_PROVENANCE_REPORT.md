# Báo Cáo Xuất Xứ & Đường Dẫn Tải Gốc: ProtectAI_DeBERTa_v3_v2

> **Đề tài**: PI-Guard (IAP491) | **Mô hình**: `ProtectAI_DeBERTa_v3_v2`  
> **Vai trò trong đề tài**: M3 Baseline (He et al. ICLR 2023 / ProtectAI 2024)  

## 1. Chuỗi Xuất Xứ Học Thuật (Academic Provenance Chain)

- **Bài báo khoa học (Paper)**: [DeBERTaV3: Improving DeBERTa using ELECTRA-Style Pre-Training](https://arxiv.org/abs/2111.09543)
- **Bản lưu trữ cục bộ (Local PDF)**: [`papers/He_2023_DeBERTaV3_Disentangled_Attention_ICLR.pdf`](../papers/He_2023_DeBERTaV3_Disentangled_Attention_ICLR.pdf)
- **Mã nguồn tác giả (Upstream Code)**: [https://huggingface.co/protectai/deberta-v3-base-prompt-injection-v2](https://huggingface.co/protectai/deberta-v3-base-prompt-injection-v2)
- **Thư mục repo gốc cục bộ**: [`upstream/`](../upstream/)
- **Tập dữ liệu kiểm thử (Datasets)**: [https://huggingface.co/datasets/protectai/prompt-injection-benchmark](https://huggingface.co/datasets/protectai/prompt-injection-benchmark)
- **Thư mục dữ liệu cục bộ**: [`datasets/`](../datasets/)

## 2. Kiểm Tra Toàn Vẹn Dữ Liệu Cục Bộ (SHA-256)

| Tên Tệp | Kích Thước (Bytes) | SHA-256 Checksum | Trạng Thái |
| :--- | :--- | :--- | :---: |
| `notinject_sample.json` | 26,909 | `c77abbf3de71f99f...` | **KHỚP 100%** |
| `protectai_eval_benchmark.json` | 3,699 | `251e55a4ebeeb721...` | **KHỚP 100%** |

## 3. Kết Quả Đo Đạc Thực Nghiệm

- Tệp kết quả benchmark đo đạc: [`PROTECTAI_REPLICATION_BENCHMARK_RESULTS.json`](./PROTECTAI_REPLICATION_BENCHMARK_RESULTS.json)
- Công cụ kiểm tra xuất xứ: [`workspaces/truongnv/scripts/check_replication_origin_urls.py`](../../scripts/check_replication_origin_urls.py)
