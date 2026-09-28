# Dataset Card & Provenance: JailbreakBench JBB-Behaviors Benchmark (100 Harmful + 100 Benign Counterparts)

## 1. Upstream Scientific Provenance (Xác Minh Nguồn Gốc Bài Báo)
- **Paper Title**: JailbreakBench: An Open Robustness Benchmark for Jailbreaking Large Language Models
- **Authors**: Patrick Chao, Edoardo Debenedetti, Alexander Robey, Maksym Andriushchenko, Francesco Croce, Vikash Sehwag, Edgar Dobriban, Nicolas Flammarion, George J. Pappas, Florian Tramer, Hamed Hassani, Eric Wong
- **Venue & Year**: NeurIPS 2024 (Datasets and Benchmarks Track) (2024)
- **arXiv Identifier**: [2404.01318](https://arxiv.org/abs/2404.01318) (Reference Anchor: `[[34]](#ref34)`)
- **Official Repository**: [https://github.com/JailbreakBench/jailbreakbench](https://github.com/JailbreakBench/jailbreakbench)
- **Remote / Upstream Source**: [https://huggingface.co/datasets/JailbreakBench/JBB-Behaviors](https://huggingface.co/datasets/JailbreakBench/JBB-Behaviors)
- **License**: `MIT`

## 2. Invariant Check: Is This Synthetic / Self-Created?
> **`is_synthetic_self_created = False`**  
> **Khẳng định kiểm định học thuật**: Toàn bộ dữ liệu trong thư mục này được trích xuất trực tiếp từ mã nguồn, kho lưu trữ và bộ dữ liệu kiểm chuẩn công khai chính thức của tác giả bài báo khoa học. Nhóm nghiên cứu tuyệt đối **KHÔNG TỰ TẠO (NON-SYNTHETIC)** dữ liệu tùy tiện hoặc sinh mẫu giả lập không có nguồn gốc kiểm chuẩn.

## 3. Local Dataset Files & Verification Hashes
Bảng thông số kiểm định toàn vẹn dữ liệu ngoại tuyến (SHA-256 Checksum):

| File Name | Size (Bytes) | Samples | SHA-256 Checksum |
|---|---|---|---|
| `jbb_behaviors_benign.csv` | 20,671 | 100 | `b198c96c550710bf...` |
| `jbb_behaviors_benign.json` | 32,018 | 100 | `fac2026f7305db38...` |
| `jbb_behaviors_harmful.csv` | 23,217 | 100 | `f985615b17b7659a...` |
| `jbb_behaviors_harmful.json` | 34,556 | 100 | `9ee1cb2aab52550f...` |
| `jbb_combined_benchmark.json` | 70,183 | 6 | `66fc6b5e4f63ea74...` |

## 4. Schema & Validation Mapping
Tệp kịch bản kiểm thử sử dụng: [`run_jailbreakbench_replication.py`](../run_jailbreakbench_replication.py)

### Schema Definition
```json
{
  "goal_field": "Goal",
  "target_field": "Target",
  "category_field": "Category",
  "source_field": "Source",
  "label_mapping": {
    "Harmful (100 behaviors)": "10 Safety Policies (CBRN, Cyberattacks, Hate Speech, etc.)",
    "Benign (100 behaviors)": "False Refusal Probes (Counterparts with high surface similarity)"
  }
}
```

## 5. Remote / Standalone Location (Nơi Lưu Trữ Dữ Liệu Đầy Đủ)
Nếu cần tải lại hoặc kiểm tra phân tách toàn bộ tập dữ liệu gốc vượt ngoài gói kiểm thử nhanh:
- **Primary Source URL**: `https://huggingface.co/datasets/JailbreakBench/JBB-Behaviors`
- **Hướng dẫn đồng bộ**: Chạy `python run_all_triad_experiments.py` hoặc sử dụng các tệp JSON/CSV nội bộ trong thư mục này. Toàn bộ kịch bản ưu tiên đọc dữ liệu cục bộ ngoại tuyến (`datasets/`), đảm bảo thực nghiệm 100% tái lập mà không cần kết nối mạng bên ngoài.
