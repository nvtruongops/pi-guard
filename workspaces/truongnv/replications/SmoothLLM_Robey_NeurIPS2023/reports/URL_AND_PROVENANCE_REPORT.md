# Báo Cáo Xuất Xứ & Đường Dẫn Tải Gốc: SmoothLLM_Robey_NeurIPS2023

> **Đề tài**: PI-Guard (IAP491) | **Mô hình**: `SmoothLLM_Robey_NeurIPS2023`  
> **Vai trò trong đề tài**: Randomized Defense Survey (NeurIPS 2023)  

## 1. Chuỗi Xuất Xứ Học Thuật (Academic Provenance Chain)

- **Bài báo khoa học (Paper)**: [SmoothLLM: Defending Large Language Models Against Jailbreaking Attacks](https://arxiv.org/abs/2310.03684)
- **Bản lưu trữ cục bộ (Local PDF)**: [`papers/Robey_2023_SmoothLLM_Defending_LLMs_Random_Perturbation.pdf`](../papers/Robey_2023_SmoothLLM_Defending_LLMs_Random_Perturbation.pdf)
- **Mã nguồn tác giả (Upstream Code)**: [https://github.com/arobey1/smooth-llm](https://github.com/arobey1/smooth-llm)
- **Thư mục repo gốc cục bộ**: [`upstream/`](../upstream/)
- **Tập dữ liệu kiểm thử (Datasets)**: [https://github.com/arobey1/smooth-llm/tree/main/data/GCG](https://github.com/arobey1/smooth-llm/tree/main/data/GCG)
- **Thư mục dữ liệu cục bộ**: [`datasets/`](../datasets/)

## 2. Kiểm Tra Toàn Vẹn Dữ Liệu Cục Bộ (SHA-256)

| Tên Tệp | Kích Thước (Bytes) | SHA-256 Checksum | Trạng Thái |
| :--- | :--- | :--- | :---: |
| `llama2_behaviors.json` | 2,721 | `f96d53e113bb3b83...` | **KHỚP 100%** |
| `smoothllm_eval_benchmark.json` | 5,217 | `166a3d9f43319bcd...` | **KHỚP 100%** |
| `vicuna_behaviors.json` | 2,659 | `7396b50e123775b7...` | **KHỚP 100%** |

## 3. Kết Quả Đo Đạc Thực Nghiệm

- Tệp kết quả benchmark đo đạc: [`SMOOTHLLM_REPLICATION_BENCHMARK_RESULTS.json`](./SMOOTHLLM_REPLICATION_BENCHMARK_RESULTS.json)
- Công cụ kiểm tra xuất xứ: [`workspaces/truongnv/scripts/check_replication_origin_urls.py`](../../scripts/check_replication_origin_urls.py)
