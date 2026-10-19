# Dataset workspace documentation

> This is a documentation mirror in Final-Report. Raw source snapshots and the unsplit corpus are not included here. Local v5 split files are staged under Final-Report/notebooks/data/splits and are excluded from Git.

Thư mục dataset cục bộ của PI-Guard được chia thành ba khu vực theo mục đích sử dụng. Dữ liệu này là workspace nghiên cứu riêng trong `workspaces/truongnv`; không dùng các thư mục này để phát hành lại dữ liệu nguồn.

| Thư mục | Nội dung | Quy tắc sử dụng |
|---|---|---|
| [`benchmarks/`](benchmarks/) | Snapshot benchmark dành cho đánh giá riêng. | Giữ tách khỏi train corpus. |
| [`project_training/`](project_training/README.md) | Corpus đã tổng hợp cho đồ án, báo cáo audit, công cụ tái tạo và version log. | Mọi thay đổi dữ liệu phải ghi vào `DATASET_VERSION_LOG.md`. |
| [`source_datasets/`](source_datasets/README.md) | Snapshot nguồn thô để giữ provenance và audit; một số nguồn chỉ là ứng viên, không dùng cho corpus. | Giữ nguyên raw payload; ghi revision, URL, paper và tình trạng nhãn/license trong README từng nguồn. |

## Luồng dữ liệu

`source_datasets/` giữ snapshot gốc theo từng nguồn. `project_training/` chứa các bản tổng hợp và biến đổi có manifest/audit riêng. `benchmarks/` chỉ dùng làm tập đánh giá. Thay đổi cách chia nhãn, khử trùng lặp, split hoặc thêm/bớt nguồn cần có phiên bản mới và mục tương ứng trong version log.
