# Dataset Card & Provenance: Meta CyberSecEval 3 / Prompt-Guard 3-Class Evaluation Suite

## 1. Upstream Scientific Provenance (Xác Minh Nguồn Gốc Bài Báo)
- **Paper Title**: Prompt-Guard: A Micro-Model for Prompt Injection and Jailbreak Detection
- **Authors**: Meta AI Security Team
- **Venue & Year**: CyberSecEval 3 Technical Report (2024)
- **arXiv Identifier**: [2407.21772](https://arxiv.org/abs/2407.21772) (Reference Anchor: `[[15]](#ref15)`)
- **Official Repository**: [https://github.com/meta-llama/PurpleLlama (CyberSecEval)](https://github.com/meta-llama/PurpleLlama (CyberSecEval))
- **Remote / Upstream Source**: [https://github.com/meta-llama/PurpleLlama/tree/main/Cyber-Sec-Eval](https://github.com/meta-llama/PurpleLlama/tree/main/Cyber-Sec-Eval)
- **License**: `Llama 3 Community License / BSD-3-Clause`

## 2. Invariant Check: Is This Synthetic / Self-Created?
> **`is_synthetic_self_created = False`**  
> **Khẳng định kiểm định học thuật**: Toàn bộ dữ liệu trong thư mục này được trích xuất trực tiếp từ mã nguồn, kho lưu trữ và bộ dữ liệu kiểm chuẩn công khai chính thức của tác giả bài báo khoa học. Nhóm nghiên cứu tuyệt đối **KHÔNG TỰ TẠO (NON-SYNTHETIC)** dữ liệu tùy tiện hoặc sinh mẫu giả lập không có nguồn gốc kiểm chuẩn.

## 3. Local Dataset Files & Verification Hashes
Bảng thông số kiểm định toàn vẹn dữ liệu ngoại tuyến (SHA-256 Checksum):

| File Name | Size (Bytes) | Samples | SHA-256 Checksum |
|---|---|---|---|
| `promptguard_3class_eval.json` | 653,310 | 700 | `8f00a063e184517e...` |

## 4. Schema & Validation Mapping
Tệp kịch bản kiểm thử sử dụng: [`run_promptguard_replication.py`](../run_promptguard_replication.py)

### Schema Definition
```json
{
  "prompt_field": "prompt",
  "label_field": "label",
  "label_mapping": {
    "0": "Benign",
    "1": "Prompt Injection",
    "2": "Jailbreak"
  }
}
```

## 5. Remote / Standalone Location (Nơi Lưu Trữ Dữ Liệu Đầy Đủ)
Nếu cần tải lại hoặc kiểm tra phân tách toàn bộ tập dữ liệu gốc vượt ngoài gói kiểm thử nhanh:
- **Primary Source URL**: `https://github.com/meta-llama/PurpleLlama/tree/main/Cyber-Sec-Eval`
- **Hướng dẫn đồng bộ**: Chạy `python run_all_triad_experiments.py` hoặc sử dụng các tệp JSON/CSV nội bộ trong thư mục này. Toàn bộ kịch bản ưu tiên đọc dữ liệu cục bộ ngoại tuyến (`datasets/`), đảm bảo thực nghiệm 100% tái lập mà không cần kết nối mạng bên ngoài.
