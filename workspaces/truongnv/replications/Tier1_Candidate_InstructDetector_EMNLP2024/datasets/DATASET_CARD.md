# Dataset Card & Provenance: BIPIA Benchmark (Indirect Prompt Injection Attacks - Text & Code)

## 1. Upstream Scientific Provenance (Xác Minh Nguồn Gốc Bài Báo)
- **Paper Title**: InstructDetector: Defending against Indirect Prompt Injection through Instruction-Tuned Classifier
- **Authors**: Zhao et al.
- **Venue & Year**: EMNLP 2024 Findings (2024)
- **arXiv Identifier**: [2402.06774](https://arxiv.org/abs/2402.06774) (Reference Anchor: `[[18]](#ref18)`)
- **Official Repository**: [https://github.com/ebsi-ai/BIPIA & https://huggingface.co/datasets/EBSI/BIPIA](https://github.com/ebsi-ai/BIPIA & https://huggingface.co/datasets/EBSI/BIPIA)
- **Remote / Upstream Source**: [https://huggingface.co/datasets/EBSI/BIPIA](https://huggingface.co/datasets/EBSI/BIPIA)
- **License**: `MIT`

## 2. Invariant Check: Is This Synthetic / Self-Created?
> **`is_synthetic_self_created = False`**  
> **Khẳng định kiểm định học thuật**: Toàn bộ dữ liệu trong thư mục này được trích xuất trực tiếp từ mã nguồn, kho lưu trữ và bộ dữ liệu kiểm chuẩn công khai chính thức của tác giả bài báo khoa học. Nhóm nghiên cứu tuyệt đối **KHÔNG TỰ TẠO (NON-SYNTHETIC)** dữ liệu tùy tiện hoặc sinh mẫu giả lập không có nguồn gốc kiểm chuẩn.

## 3. Local Dataset Files & Verification Hashes
Bảng thông số kiểm định toàn vẹn dữ liệu ngoại tuyến (SHA-256 Checksum):

| File Name | Size (Bytes) | Samples | SHA-256 Checksum |
|---|---|---|---|
| `bipia_code_eval.json` | 29,293 | 100 | `58b29ce192d9f9f5...` |
| `bipia_text_eval.json` | 25,308 | 150 | `174df93cce696572...` |

## 4. Schema & Validation Mapping
Tệp kịch bản kiểm thử sử dụng: [`run_instructdetector_replication.py`](../run_instructdetector_replication.py)

### Schema Definition
```json
{
  "prompt_field": "prompt",
  "label_field": "label",
  "domain_field": "domain",
  "label_mapping": {
    "0": "Clean / Benign Task",
    "1": "Indirect Prompt Injection (Eavesdropping, Fingerprinting, Exfiltration)"
  }
}
```

## 5. Remote / Standalone Location (Nơi Lưu Trữ Dữ Liệu Đầy Đủ)
Nếu cần tải lại hoặc kiểm tra phân tách toàn bộ tập dữ liệu gốc vượt ngoài gói kiểm thử nhanh:
- **Primary Source URL**: `https://huggingface.co/datasets/EBSI/BIPIA`
- **Hướng dẫn đồng bộ**: Chạy `python run_all_triad_experiments.py` hoặc sử dụng các tệp JSON/CSV nội bộ trong thư mục này. Toàn bộ kịch bản ưu tiên đọc dữ liệu cục bộ ngoại tuyến (`datasets/`), đảm bảo thực nghiệm 100% tái lập mà không cần kết nối mạng bên ngoài.
