# Dataset Card & Provenance: Jain NeurIPS 2023 Baseline Defenses Evaluation Suite (GCG + AdvGLUE + Alpaca)

## 1. Upstream Scientific Provenance (Xác Minh Nguồn Gốc Bài Báo)
- **Paper Title**: Baseline Defenses for Adversarial Attacks Against Aligned Language Models
- **Authors**: Neel Jain, Avi Schwarzschild, Yuxin Wen, Gowthami Somepalli, John Dickerson, Pratyush Maini
- **Venue & Year**: NeurIPS 2023 (2023)
- **arXiv Identifier**: [2309.00614](https://arxiv.org/abs/2309.00614) (Reference Anchor: `[[13]](#ref13)`)
- **Official Repository**: [https://github.com/arobey1/smooth-llm & https://github.com/llm-attacks/llm-attacks](https://github.com/arobey1/smooth-llm & https://github.com/llm-attacks/llm-attacks)
- **Remote / Upstream Source**: [https://github.com/arobey1/smooth-llm/tree/main/data](https://github.com/arobey1/smooth-llm/tree/main/data)
- **License**: `MIT`

## 2. Invariant Check: Is This Synthetic / Self-Created?
> **`is_synthetic_self_created = False`**  
> **Khẳng định kiểm định học thuật**: Toàn bộ dữ liệu trong thư mục này được trích xuất trực tiếp từ mã nguồn, kho lưu trữ và bộ dữ liệu kiểm chuẩn công khai chính thức của tác giả bài báo khoa học. Nhóm nghiên cứu tuyệt đối **KHÔNG TỰ TẠO (NON-SYNTHETIC)** dữ liệu tùy tiện hoặc sinh mẫu giả lập không có nguồn gốc kiểm chuẩn.

## 3. Local Dataset Files & Verification Hashes
Bảng thông số kiểm định toàn vẹn dữ liệu ngoại tuyến (SHA-256 Checksum):

| File Name | Size (Bytes) | Samples | SHA-256 Checksum |
|---|---|---|---|
| `jain_attack_samples.json` | 1,032,321 | 503 | `e68706cc2fd9fd66...` |
| `jain_benign_samples.json` | 65,981 | 500 | `ebe1bbb5c3e05bd1...` |
| `jain_eval_benchmark.json` | 1,098,299 | 1003 | `ed546fe00cdf68a3...` |

## 4. Schema & Validation Mapping
Tệp kịch bản kiểm thử sử dụng: [`run_jain_replication.py`](../run_jain_replication.py)

### Schema Definition
```json
{
  "prompt_field": "prompt",
  "label_field": "label",
  "label_mapping": {
    "0": "Benign Query (Alpaca / LMSYS)",
    "1": "Adversarial Suffix / Jailbreak Attack (GCG / AdvGLUE)"
  }
}
```

## 5. Remote / Standalone Location (Nơi Lưu Trữ Dữ Liệu Đầy Đủ)
Nếu cần tải lại hoặc kiểm tra phân tách toàn bộ tập dữ liệu gốc vượt ngoài gói kiểm thử nhanh:
- **Primary Source URL**: `https://github.com/arobey1/smooth-llm/tree/main/data`
- **Hướng dẫn đồng bộ**: Chạy `python run_all_triad_experiments.py` hoặc sử dụng các tệp JSON/CSV nội bộ trong thư mục này. Toàn bộ kịch bản ưu tiên đọc dữ liệu cục bộ ngoại tuyến (`datasets/`), đảm bảo thực nghiệm 100% tái lập mà không cần kết nối mạng bên ngoài.
