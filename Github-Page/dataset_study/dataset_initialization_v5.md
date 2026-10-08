# Trạng thái khởi tạo bộ dữ liệu PI-Guard v5

> Snapshot ngày 09/10/2026. Đây là trạng thái của corpus nghiên cứu nội bộ; chưa phải bằng chứng mô hình đã được huấn luyện hoặc đánh giá.

## Corpus và split

Corpus ứng viên v5 có 40.000 mẫu: 20.000 benign, 10.000 Prompt Injection (PI) và 10.000 Jailbreak (JB). SHA-256 của corpus nguồn là `2b6588e9aa091d536a25a878102df866090a2539f1bf5dbbd05d6ca6a7d09bfe`. [[1]](#ref1)

Split group-aware v5 đã được khóa ở trạng thái `frozen_local_research_split`, seed 42, với tỷ lệ mục tiêu 70/15/15. [[1]](#ref1)

| Partition | Số mẫu | SHA-256 JSONL |
|---|---:|---|
| Train | 28.280 | `cb731d3e4392ca71a9fcd931949fd2f6ea38cb5a0ae0364d6aa261402ed260b2` |
| Validation | 5.858 | `f449b92c74fd17e35ede07ce61dd8706e0965e733865226fff49364a963dfd10` |
| Test | 5.862 | `6114f589e73217393c5936f1613b4d1259953ba4518764c026428ec938435a37` |

Các JSONL và ID list vẫn là dữ liệu local-only; trang này chỉ công bố số lượng và hash, không chứa prompt. Manifest split có SHA-256 `4b16cafb42d4491ac9b2f8967330d0778a5a6db19408cddd337ef878a49f4ac1`. [[1]](#ref1)

Script `Final-Report/scripts/split_v5_dataset.py` tạo hoặc kiểm tra split từ corpus v5 đã có trong thư mục local truyền qua `--dataset-root`. Có thể dùng `--dry-run`, `--apply` hoặc `--verify`; chế độ apply từ chối ghi đè split đã tồn tại. `--verify` đã tái tạo đúng manifest frozen trên Python 3.11.16 và 3.14.7. Repository chỉ lưu script và manifest, không lưu corpus hoặc payload split. [[1]](#ref1)

## Đánh giá dataset Hugging Face

Dataset card `jackhhao/jailbreak-classification` mô tả trường `prompt` và nhãn `type` gồm `benign` hoặc `jailbreak`. Card ghi phần jailbreak lấy từ `verazuo/jailbreak_llms`, còn benign lấy từ OpenOrca và GPTeacher. Vì không có nhãn PI, đây không phải bộ ba nhãn dùng trực tiếp cho PI-Guard. [[2]](#ref2)

Trong audit local, 15.064 prompt Verazuo duy nhất sau chuẩn hóa đều trùng với TrustAIRLab. Vì vậy phần JB này không được thêm vào v5 như một nguồn độc lập. Kết quả đó không chứng minh toàn bộ dataset HF bị trùng: overlap từng dòng của phần benign chưa được kiểm tra. [[1]](#ref1)

Không tải hoặc nhập nguyên gói HF vào v5; corpus và split hiện hành không đổi. [[1]](#ref1)

## Giới hạn hiện tại

- Rà soát quyền sử dụng nguồn và chính sách phân xử nhãn ba lớp vẫn đang mở; còn caveat provenance/license theo từng dòng ở PromptScreen. [[1]](#ref1)
- Chưa có holdout benign độc lập bên ngoài v5 để ước lượng FPR. [[1]](#ref1)
- Chưa huấn luyện, chạy inference hoặc báo cáo metric từ corpus này. Hoàn tất khởi tạo dataset không đồng nghĩa Review 2 đã có demo mô hình. [[1]](#ref1)

Các trang [tuyển chọn dữ liệu](data_curation.md) và [group-aware splitting](group_aware_splitting.md) trình bày nền tảng phương pháp. Ví dụ hoặc bảng minh họa tại đó không phải kết quả đánh giá của corpus v5. [[1]](#ref1)

## Tài liệu tham chiếu

- <a id="ref1"></a>**[1]** PI-Guard local dataset handoff and audit records, 2026-10-09: `Final-Report/reports/datasets/README.md`, `research/project_training/DATASET_VERSION_LOG.md`, `research/project_training/audit/cross_dataset_overlap.md`, and `research/project_training/splits/split_manifest.json`. Corpus and split payloads are retained locally; the hashes above identify the reviewed artifacts.
- <a id="ref2"></a>**[2]** [Hugging Face dataset card: `jackhhao/jailbreak-classification`](https://huggingface.co/datasets/jackhhao/jailbreak-classification); [upstream Verazuo repository](https://github.com/verazuo/jailbreak_llms).
