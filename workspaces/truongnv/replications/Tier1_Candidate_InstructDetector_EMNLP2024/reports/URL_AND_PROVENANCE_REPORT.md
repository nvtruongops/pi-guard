# Báo Cáo Xuất Xứ & Đường Dẫn Tải Gốc: InstructDetector_Zhao_EMNLP2024

> **Đề tài**: PI-Guard (IAP491) | **Mô hình**: `InstructDetector_Zhao_EMNLP2024`  
> **Vai trò trong đề tài**: M5 Baseline (Findings of EMNLP 2024)  

## 1. Chuỗi Xuất Xứ Học Thuật (Academic Provenance Chain)

- **Bài báo khoa học (Paper)**: [InstructDetector: Identifying Instruction-Tuned Evasion Attacks](https://arxiv.org/abs/2402.06774)
- **Bản lưu trữ cục bộ (Local PDF)**: [`papers/Zhao_2024_InstructDetector_Instruction_Tuned_Attack_EMNLP.pdf`](../papers/Zhao_2024_InstructDetector_Instruction_Tuned_Attack_EMNLP.pdf)
- **Mã nguồn tác giả (Upstream Code)**: [https://github.com/MYVAE/Instruction-detection](https://github.com/MYVAE/Instruction-detection)
- **Thư mục repo gốc cục bộ**: [`upstream/`](../upstream/)
- **Tập dữ liệu kiểm thử (Datasets)**: [https://github.com/microsoft/BIPIA](https://github.com/microsoft/BIPIA)
- **Thư mục dữ liệu cục bộ**: [`datasets/`](../datasets/)

## 2. Kiểm Tra Toàn Vẹn Dữ Liệu Cục Bộ (SHA-256)

| Tên Tệp | Kích Thước (Bytes) | SHA-256 Checksum | Trạng Thái |
| :--- | :--- | :--- | :---: |
| `bipia_code_eval.json` | 29,293 | `58b29ce192d9f9f5...` | **KHỚP 100%** |
| `bipia_text_eval.json` | 25,308 | `174df93cce696572...` | **KHỚP 100%** |

## 3. Kết Quả Đo Đạc Thực Nghiệm

- Tệp kết quả benchmark đo đạc: [`INSTRUCTDETECTOR_EMNLP2024_REPLICATION_BENCHMARK_RESULTS.json`](./INSTRUCTDETECTOR_EMNLP2024_REPLICATION_BENCHMARK_RESULTS.json)
- Công cụ kiểm tra xuất xứ: [`workspaces/truongnv/scripts/check_replication_origin_urls.py`](../../scripts/check_replication_origin_urls.py)
