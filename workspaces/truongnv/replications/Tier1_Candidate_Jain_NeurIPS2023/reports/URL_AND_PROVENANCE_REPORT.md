# Báo Cáo Xuất Xứ & Đường Dẫn Tải Gốc: Jain_Baseline_NeurIPS2023

> **Đề tài**: PI-Guard (IAP491) | **Mô hình**: `Jain_Baseline_NeurIPS2023`  
> **Vai trò trong đề tài**: M2 Baseline (NeurIPS 2023 Workshop)  

## 1. Chuỗi Xuất Xứ Học Thuật (Academic Provenance Chain)

- **Bài báo khoa học (Paper)**: [Baseline Defenses for Adversarial Attacks Against Aligned Language Models](https://arxiv.org/abs/2309.00614)
- **Bản lưu trữ cục bộ (Local PDF)**: [`papers/Jain_2023_Baseline_Defenses_Adversarial_Attacks_LLMs.pdf`](../papers/Jain_2023_Baseline_Defenses_Adversarial_Attacks_LLMs.pdf)
- **Mã nguồn tác giả (Upstream Code)**: [https://github.com/neelsjain/baseline-defenses](https://github.com/neelsjain/baseline-defenses)
- **Thư mục repo gốc cục bộ**: [`upstream/`](../upstream/)
- **Tập dữ liệu kiểm thử (Datasets)**: [https://github.com/neelsjain/baseline-defenses/tree/main/data](https://github.com/neelsjain/baseline-defenses/tree/main/data)
- **Thư mục dữ liệu cục bộ**: [`datasets/`](../datasets/)

## 2. Kiểm Tra Toàn Vẹn Dữ Liệu Cục Bộ (SHA-256)

| Tên Tệp | Kích Thước (Bytes) | SHA-256 Checksum | Trạng Thái |
| :--- | :--- | :--- | :---: |
| `jain_attack_samples.json` | 1,032,321 | `e68706cc2fd9fd66...` | **KHỚP 100%** |
| `jain_benign_samples.json` | 65,981 | `ebe1bbb5c3e05bd1...` | **KHỚP 100%** |
| `jain_eval_benchmark.json` | 1,098,299 | `ed546fe00cdf68a3...` | **KHỚP 100%** |

## 3. Kết Quả Đo Đạc Thực Nghiệm

- Tệp kết quả benchmark đo đạc: [`JAIN_NEURIPS2023_REPLICATION_BENCHMARK_RESULTS.json`](./JAIN_NEURIPS2023_REPLICATION_BENCHMARK_RESULTS.json)
- Công cụ kiểm tra xuất xứ: [`workspaces/truongnv/scripts/check_replication_origin_urls.py`](../../scripts/check_replication_origin_urls.py)
