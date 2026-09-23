# Dataset Card & Provenance: Ayub CAMLIS 2024 Evaluation Suite (WildGuard + NotInject + Split)

## 1. Upstream Scientific Provenance (Xác Minh Nguồn Gốc Bài Báo)
- **Paper Title**: Model-Agnostic Detection of Prompt Injection Attacks Using Sentence Embeddings
- **Authors**: Md. Ahsan Ayub, et al.
- **Venue & Year**: CAMLIS 2024 (Conference on Applied Machine Learning for Information Security) (2024)
- **arXiv Identifier**: [2410.22284](https://arxiv.org/abs/2410.22284) (Reference Anchor: `[[24]](#ref24)`)
- **Official Repository**: [https://github.com/chawins/PIGuard (Benchmark Suite) & https://huggingface.co/datasets/allenai/wildguard](https://github.com/chawins/PIGuard (Benchmark Suite) & https://huggingface.co/datasets/allenai/wildguard)
- **Remote / Upstream Source**: [https://huggingface.co/datasets/allenai/wildguard](https://huggingface.co/datasets/allenai/wildguard)
- **License**: `Apache-2.0 / MIT`

## 2. Invariant Check: Is This Synthetic / Self-Created?
> **`is_synthetic_self_created = False`**  
> **Khẳng định kiểm định học thuật**: Toàn bộ dữ liệu trong thư mục này được trích xuất trực tiếp từ mã nguồn, kho lưu trữ và bộ dữ liệu kiểm chuẩn công khai chính thức của tác giả bài báo khoa học. Nhóm nghiên cứu tuyệt đối **KHÔNG TỰ TẠO (NON-SYNTHETIC)** dữ liệu tùy tiện hoặc sinh mẫu giả lập không có nguồn gốc kiểm chuẩn.

## 3. Local Dataset Files & Verification Hashes
Bảng thông số kiểm định toàn vẹn dữ liệu ngoại tuyến (SHA-256 Checksum):

| File Name | Size (Bytes) | Samples | SHA-256 Checksum |
|---|---|---|---|
| `NotInject_one.json` | 26,909 | 113 | `c77abbf3de71f99f...` |
| `NotInject_three.json` | 36,783 | 113 | `bc18f3ad38ad2380...` |
| `NotInject_two.json` | 30,807 | 113 | `325559cd1204fd3b...` |
| `train.json` | 116,149 | 344 | `6b3078e69a15c606...` |
| `valid.json` | 91,222 | 144 | `e273fd455baac878...` |
| `wildguard.json` | 472,515 | 971 | `62a0f7331af19abd...` |

## 4. Schema & Validation Mapping
Tệp kịch bản kiểm thử sử dụng: [`run_ayub_tier1_benchmark.py`](../run_ayub_tier1_benchmark.py)

### Schema Definition
```json
{
  "prompt_field": "prompt",
  "label_field": "label",
  "label_mapping": {
    "0": "Benign / Not-Injected",
    "1": "Prompt Injection Attack"
  }
}
```

## 5. Remote / Standalone Location (Nơi Lưu Trữ Dữ Liệu Đầy Đủ)
Nếu cần tải lại hoặc kiểm tra phân tách toàn bộ tập dữ liệu gốc vượt ngoài gói kiểm thử nhanh:
- **Primary Source URL**: `https://huggingface.co/datasets/allenai/wildguard`
- **Hướng dẫn đồng bộ**: Chạy `python run_all_triad_experiments.py` hoặc sử dụng các tệp JSON/CSV nội bộ trong thư mục này. Toàn bộ kịch bản ưu tiên đọc dữ liệu cục bộ ngoại tuyến (`datasets/`), đảm bảo thực nghiệm 100% tái lập mà không cần kết nối mạng bên ngoài.
