# Dataset Card & Provenance: SmoothLLM NeurIPS 2023 Official Behaviors Suite (LLaMA-2 & Vicuna GCG Controls)

## 1. Upstream Scientific Provenance (Xác Minh Nguồn Gốc Bài Báo)
- **Paper Title**: SmoothLLM: Defending Large Language Models Against Jailbreaking Attacks
- **Authors**: Alexander Robey, Eric Wong, Hamed Hassani, George J. Pappas
- **Venue & Year**: NeurIPS 2023 (2023)
- **arXiv Identifier**: [2310.03684](https://arxiv.org/abs/2310.03684) (Reference Anchor: `[[14]](#ref14)`)
- **Official Repository**: [https://github.com/arobey1/smooth-llm](https://github.com/arobey1/smooth-llm)
- **Remote / Upstream Source**: [https://github.com/arobey1/smooth-llm/tree/main/data](https://github.com/arobey1/smooth-llm/tree/main/data)
- **License**: `MIT`

## 2. Invariant Check: Is This Synthetic / Self-Created?
> **`is_synthetic_self_created = False`**  
> **Khẳng định kiểm định học thuật**: Toàn bộ dữ liệu trong thư mục này được trích xuất trực tiếp từ mã nguồn, kho lưu trữ và bộ dữ liệu kiểm chuẩn công khai chính thức của tác giả bài báo khoa học. Nhóm nghiên cứu tuyệt đối **KHÔNG TỰ TẠO (NON-SYNTHETIC)** dữ liệu tùy tiện hoặc sinh mẫu giả lập không có nguồn gốc kiểm chuẩn.

## 3. Local Dataset Files & Verification Hashes
Bảng thông số kiểm định toàn vẹn dữ liệu ngoại tuyến (SHA-256 Checksum):

| File Name | Size (Bytes) | Samples | SHA-256 Checksum |
|---|---|---|---|
| `llama2_behaviors.json` | 2,721 | 3 | `f96d53e113bb3b83...` |
| `smoothllm_eval_benchmark.json` | 5,217 | 10 | `166a3d9f43319bcd...` |
| `vicuna_behaviors.json` | 2,659 | 3 | `7396b50e123775b7...` |

## 4. Schema & Validation Mapping
Tệp kịch bản kiểm thử sử dụng: [`run_smoothllm_replication.py`](../run_smoothllm_replication.py)

### Schema Definition
```json
{
  "goal_field": "goal",
  "target_field": "target",
  "control_field": "controls / control",
  "label_mapping": {
    "goal": "Harmful Jailbreak Intent (AdvBenchmark)",
    "control": "Adversarial Suffix Perturbation (GCG)"
  }
}
```

## 5. Remote / Standalone Location (Nơi Lưu Trữ Dữ Liệu Đầy Đủ)
Nếu cần tải lại hoặc kiểm tra phân tách toàn bộ tập dữ liệu gốc vượt ngoài gói kiểm thử nhanh:
- **Primary Source URL**: `https://github.com/arobey1/smooth-llm/tree/main/data`
- **Hướng dẫn đồng bộ**: Chạy `python run_all_triad_experiments.py` hoặc sử dụng các tệp JSON/CSV nội bộ trong thư mục này. Toàn bộ kịch bản ưu tiên đọc dữ liệu cục bộ ngoại tuyến (`datasets/`), đảm bảo thực nghiệm 100% tái lập mà không cần kết nối mạng bên ngoài.
