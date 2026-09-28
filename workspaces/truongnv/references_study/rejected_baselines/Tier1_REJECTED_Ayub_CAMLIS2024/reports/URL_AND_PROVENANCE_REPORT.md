# Báo Cáo Xuất Xứ & Đường Dẫn Tải Gốc: Ayub_CAMLIS2024_Rejected

> **Đề tài**: PI-Guard (IAP491) | **Mô hình**: `Ayub_CAMLIS2024_Rejected`  
> **Vai trò trong đề tài**: Rejected Candidate (CAMLIS 2024 - 58.4% Overdefense FPR)  

## 1. Chuỗi Xuất Xứ Học Thuật (Academic Provenance Chain)

- **Bài báo khoa học (Paper)**: [Towards Robust Detection of Prompt Injection Attacks on Large Language Models](https://arxiv.org/abs/2402.15570)
- **Bản lưu trữ cục bộ (Local PDF)**: [`papers/Ayub_2024_Towards_Robust_Detection_Prompt_Injection_CAMLIS.pdf`](../papers/Ayub_2024_Towards_Robust_Detection_Prompt_Injection_CAMLIS.pdf)
- **Mã nguồn tác giả (Upstream Code)**: [https://github.com/AhsanAyub/malicious-prompt-detection](https://github.com/AhsanAyub/malicious-prompt-detection)
- **Thư mục repo gốc cục bộ**: [`upstream/`](../upstream/)
- **Tập dữ liệu kiểm thử (Datasets)**: [https://github.com/AhsanAyub/malicious-prompt-detection/tree/main/dataset](https://github.com/AhsanAyub/malicious-prompt-detection/tree/main/dataset)
- **Thư mục dữ liệu cục bộ**: [`datasets/`](../datasets/)

## 2. Kiểm Tra Toàn Vẹn Dữ Liệu Cục Bộ (SHA-256)

| Tên Tệp | Kích Thước (Bytes) | SHA-256 Checksum | Trạng Thái |
| :--- | :--- | :--- | :---: |
| `NotInject_one.json` | 26,909 | `c77abbf3de71f99f...` | **KHỚP 100%** |
| `NotInject_three.json` | 36,783 | `bc18f3ad38ad2380...` | **KHỚP 100%** |
| `NotInject_two.json` | 30,807 | `325559cd1204fd3b...` | **KHỚP 100%** |
| `train.json` | 116,149 | `6b3078e69a15c606...` | **KHỚP 100%** |
| `valid.json` | 91,222 | `e273fd455baac878...` | **KHỚP 100%** |
| `wildguard.json` | 472,515 | `62a0f7331af19abd...` | **KHỚP 100%** |

## 3. Kết Quả Đo Đạc Thực Nghiệm

- Tệp kết quả benchmark đo đạc: [`AYUB_CAMLIS2024_REPLICATION_BENCHMARK_RESULTS.json`](./AYUB_CAMLIS2024_REPLICATION_BENCHMARK_RESULTS.json)
- Công cụ kiểm tra xuất xứ: [`workspaces/truongnv/scripts/check_replication_origin_urls.py`](../../scripts/check_replication_origin_urls.py)
