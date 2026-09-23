# Dataset Card & Provenance: ProtectAI DeBERTa-v3 Benchmark & NotInject Robustness Suite

## 1. Upstream Scientific Provenance (Xác Minh Nguồn Gốc Bài Báo)
- **Paper Title**: Protect AI DeBERTa-v3 Base Prompt Injection Classifier v2
- **Authors**: Protect AI Security Research
- **Venue & Year**: Hugging Face Model Hub & AI Security Benchmark (2024)
- **arXiv Identifier**: [N/A (Industry SOTA Open-Weights)](https://arxiv.org/abs/N/A (Industry SOTA Open-Weights)) (Reference Anchor: `[[15]](#ref15) / Hugging Face SOTA`)
- **Official Repository**: [https://huggingface.co/protectai/deberta-v3-base-prompt-injection-v2](https://huggingface.co/protectai/deberta-v3-base-prompt-injection-v2)
- **Remote / Upstream Source**: [https://huggingface.co/datasets/deepset/prompt-injections & https://huggingface.co/datasets/protectai/prompt-injection-benchmark](https://huggingface.co/datasets/deepset/prompt-injections & https://huggingface.co/datasets/protectai/prompt-injection-benchmark)
- **License**: `Apache-2.0`

## 2. Invariant Check: Is This Synthetic / Self-Created?
> **`is_synthetic_self_created = False`**  
> **Khẳng định kiểm định học thuật**: Toàn bộ dữ liệu trong thư mục này được trích xuất trực tiếp từ mã nguồn, kho lưu trữ và bộ dữ liệu kiểm chuẩn công khai chính thức của tác giả bài báo khoa học. Nhóm nghiên cứu tuyệt đối **KHÔNG TỰ TẠO (NON-SYNTHETIC)** dữ liệu tùy tiện hoặc sinh mẫu giả lập không có nguồn gốc kiểm chuẩn.

## 3. Local Dataset Files & Verification Hashes
Bảng thông số kiểm định toàn vẹn dữ liệu ngoại tuyến (SHA-256 Checksum):

| File Name | Size (Bytes) | Samples | SHA-256 Checksum |
|---|---|---|---|
| `notinject_sample.json` | 26,909 | 113 | `c77abbf3de71f99f...` |
| `protectai_eval_benchmark.json` | 3,699 | 22 | `251e55a4ebeeb721...` |

## 4. Schema & Validation Mapping
Tệp kịch bản kiểm thử sử dụng: [`run_protectai_replication.py`](../run_protectai_replication.py)

### Schema Definition
```json
{
  "prompt_field": "text / prompt",
  "label_field": "label",
  "label_mapping": {
    "0 / SAFE": "Benign Query / False Positive Probe",
    "1 / INJECTION": "Direct / Indirect Prompt Injection Attack"
  }
}
```

## 5. Remote / Standalone Location (Nơi Lưu Trữ Dữ Liệu Đầy Đủ)
Nếu cần tải lại hoặc kiểm tra phân tách toàn bộ tập dữ liệu gốc vượt ngoài gói kiểm thử nhanh:
- **Primary Source URL**: `https://huggingface.co/datasets/deepset/prompt-injections & https://huggingface.co/datasets/protectai/prompt-injection-benchmark`
- **Hướng dẫn đồng bộ**: Chạy `python run_all_triad_experiments.py` hoặc sử dụng các tệp JSON/CSV nội bộ trong thư mục này. Toàn bộ kịch bản ưu tiên đọc dữ liệu cục bộ ngoại tuyến (`datasets/`), đảm bảo thực nghiệm 100% tái lập mà không cần kết nối mạng bên ngoài.
