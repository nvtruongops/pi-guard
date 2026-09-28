# Báo Cáo Xuất Xứ & Đường Dẫn Tải Gốc: JailbreakBench_Chao_NeurIPS2024

> **Đề tài**: PI-Guard (IAP491) | **Mô hình**: `JailbreakBench_Chao_NeurIPS2024`  
> **Vai trò trong đề tài**: Evaluation Harness & D3 Source (NeurIPS 2024)  

## 1. Chuỗi Xuất Xứ Học Thuật (Academic Provenance Chain)

- **Bài báo khoa học (Paper)**: [JailbreakBench: An Open Robustness Benchmark for Jailbreaking Large Language Models](https://arxiv.org/abs/2404.01318)
- **Bản lưu trữ cục bộ (Local PDF)**: [`papers/Chao_2024_JailbreakBench_Open_Robustness_Benchmark_NeurIPS.pdf`](../papers/Chao_2024_JailbreakBench_Open_Robustness_Benchmark_NeurIPS.pdf)
- **Mã nguồn tác giả (Upstream Code)**: [https://github.com/JailbreakBench/jailbreakbench](https://github.com/JailbreakBench/jailbreakbench)
- **Thư mục repo gốc cục bộ**: [`upstream/`](../upstream/)
- **Tập dữ liệu kiểm thử (Datasets)**: [https://huggingface.co/datasets/JailbreakBench/JBB-Behaviors](https://huggingface.co/datasets/JailbreakBench/JBB-Behaviors)
- **Thư mục dữ liệu cục bộ**: [`datasets/`](../datasets/)

## 2. Kiểm Tra Toàn Vẹn Dữ Liệu Cục Bộ (SHA-256)

| Tên Tệp | Kích Thước (Bytes) | SHA-256 Checksum | Trạng Thái |
| :--- | :--- | :--- | :---: |
| `jbb_behaviors_benign.json` | 32,018 | `fac2026f7305db38...` | **KHỚP 100%** |
| `jbb_behaviors_harmful.json` | 34,556 | `9ee1cb2aab52550f...` | **KHỚP 100%** |
| `jbb_combined_benchmark.json` | 70,183 | `66fc6b5e4f63ea74...` | **KHỚP 100%** |

## 3. Kết Quả Đo Đạc Thực Nghiệm

- Tệp kết quả benchmark đo đạc: [`JAILBREAKBENCH_REPLICATION_BENCHMARK_RESULTS.json`](./JAILBREAKBENCH_REPLICATION_BENCHMARK_RESULTS.json)
- Công cụ kiểm tra xuất xứ: [`workspaces/truongnv/scripts/check_replication_origin_urls.py`](../../scripts/check_replication_origin_urls.py)
