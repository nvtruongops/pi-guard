# Báo Cáo Xuất Xứ & Đường Dẫn Tải Gốc: PIGuard_HaoLi_ACL2025

> **Đề tài**: PI-Guard (IAP491) | **Mô hình**: `PIGuard_HaoLi_ACL2025`  
> **Vai trò trong đề tài**: Foundation Reference (ACL 2025)  

## 1. Chuỗi Xuất Xứ Học Thuật (Academic Provenance Chain)

- **Bài báo khoa học (Paper)**: [PIGuard: Protecting Language Models against Prompt Injection with MOF](https://arxiv.org/abs/2410.22770)
- **Bản lưu trữ cục bộ (Local PDF)**: [`papers/PIGuard_2025_Prompt_Injection_Guardrail_ACL.pdf`](../papers/PIGuard_2025_Prompt_Injection_Guardrail_ACL.pdf)
- **Mã nguồn tác giả (Upstream Code)**: [https://github.com/leolee99/PIGuard](https://github.com/leolee99/PIGuard)
- **Thư mục repo gốc cục bộ**: [`upstream/`](../upstream/)
- **Tập dữ liệu kiểm thử (Datasets)**: [https://github.com/leolee99/PIGuard/tree/main/datasets](https://github.com/leolee99/PIGuard/tree/main/datasets)
- **Thư mục dữ liệu cục bộ**: [`datasets/`](../datasets/)

## 2. Kiểm Tra Toàn Vẹn Dữ Liệu Cục Bộ (SHA-256)

| Tên Tệp | Kích Thước (Bytes) | SHA-256 Checksum | Trạng Thái |
| :--- | :--- | :--- | :---: |
| `BIPIA_code.json` | 16,427 | `ab9f0563c7674074...` | **KHỚP 100%** |
| `BIPIA_text.json` | 6,428 | `e828d3e9e273ddf4...` | **KHỚP 100%** |
| `NotInject_one.json` | 26,909 | `c77abbf3de71f99f...` | **KHỚP 100%** |
| `NotInject_three.json` | 36,783 | `bc18f3ad38ad2380...` | **KHỚP 100%** |
| `NotInject_two.json` | 30,807 | `325559cd1204fd3b...` | **KHỚP 100%** |
| `valid.json` | 91,222 | `e273fd455baac878...` | **KHỚP 100%** |
| `wildguard.json` | 472,515 | `62a0f7331af19abd...` | **KHỚP 100%** |

## 3. Kết Quả Đo Đạc Thực Nghiệm

- Tệp kết quả benchmark đo đạc: [`PIGUARD_REPLICATION_BENCHMARK_RESULTS.json`](./PIGUARD_REPLICATION_BENCHMARK_RESULTS.json)
- Công cụ kiểm tra xuất xứ: [`workspaces/truongnv/scripts/check_replication_origin_urls.py`](../../scripts/check_replication_origin_urls.py)
