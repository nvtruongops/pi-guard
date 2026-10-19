# Dataset version log

Ghi lại lịch sử các lần thêm, gỡ, thay thế, cập nhật hoặc biến đổi corpus. Bản sao Final-Report giữ version log và manifests; corpus gốc, raw snapshots và benchmark payloads không được sao chép. Split payload local-only nằm tại Final-Report/notebooks/data/splits.

Mỗi phiên bản ghi nguồn/paper/revision, hash dữ liệu, số lượng theo nhãn, quy tắc dedup/lấy mẫu và kết quả xác minh. Không ghi prompt thô vào log.

## Lịch sử

### v1.0.0 — 2026-10-07 — sắp xếp thư mục

- Loại thay đổi: RESTRUCTURE.
- Đưa dữ liệu tổng hợp vào project_training/, raw snapshots vào source_datasets/ và benchmark vào benchmarks/.
- Không thay đổi dòng dữ liệu. Bản thân bước sắp xếp không thêm/xóa nhãn hay thay đổi số lượng.
- Đã bỏ TASK.md theo yêu cầu.

### v2.0.0 — 2026-10-07 — corpus nguồn tự nhiên trước khi cân bằng (đã bỏ)

- Loại thay đổi: ADD.
- Nguồn: hendzh/PromptShield, revision a5234cb1f5cdb256600cab64b8c961195b5e8404; TrustAIRLab/in-the-wild-jailbreak-prompts, revision a10aab8eff1c73165a442d4464dce192bd28b9c5.
- Raw đầu vào: 34.049 dòng; dedup chính xác cùng nhãn gộp 713 dòng; 42 nhóm xung đột (115 dòng nguồn) bị loại; còn 33.221 prompt.
- Phân phối: benign 22.578, PI 9.329, JB 1.314. Bản này được chia train/validation/test 80/10/10; đó là cấu hình lịch sử, không phải cách chia của corpus hiện hành.
- SHA-256 artifact lịch sử:
  - train.jsonl: 3f5a0a46d579b7a3bae59e514b7249dac981b28084a5b6a9ff9a4c79f0ccba98
  - validation.jsonl: 7dc51c0f4cdbaf16f3eaa6f53ae690f4fc7ea561eac9f260cc0655437fbe39a8
  - test.jsonl: f4f0073fb34047e4878dcb94c7e36274339d0e1bc3b09909155d86e87de36d4a
  - train_balanced.jsonl (chỉ train, 1.051 mỗi nhãn): 53c2ffee0313102ba88e921faaffbe8496c2e8a1a5aeea8bddb781a9bab4034c2
  - label_conflicts.jsonl: 48aa0999c49bdf39c6006b99476aa26678745d65fb9068e2ac555370bd58f6f7
- Ba thư mục model_ready_three_label_v1, model_ready_three_label_v1_rebuild và model_ready_three_label_v2 đã bị bỏ sau khi tạo corpus hiện hành. Hai thư mục v1 và v1_rebuild giữ bản sao cùng payload split với v2; manifest/README của chúng khác nhau.

### v3.0.0 — 2026-10-07 — gộp nguồn JB và cân bằng ba nhãn (superseded)

- Loại thay đổi: ADD + TRANSFORM + RESTRUCTURE.
- Base giữ lại: PromptShield train và TrustAIRLab configs 2023-12-25. Đã gộp thêm JailBreakV-28K text, WUSTL LLMJailbreak và What Features.
- Nguồn bổ sung và revision:
  - JailBreakV-28K, Hugging Face revision f949ca582fff13d396ac8fce59596afafb2b78d3; paper COLM 2024, https://arxiv.org/abs/2404.03027.
  - WUSTL-CSPL/LLMJailbreak, revision 2a9e665769de1bbfa657b6e6a9f88d9d427bc57c; paper USENIX Security 2024, https://www.usenix.org/conference/usenixsecurity24/presentation/yu-zhiyuan.
  - sevdeawesome/jailbreak_success, Hugging Face revision 12bad235ee184287bc5f41ec2341489501a30049; paper BlackboxNLP 2025, https://aclanthology.org/2025.blackboxnlp-1.28/.
- Hash các file nguồn được dùng:
  - PromptShield train.json: aa33c3ffcc27bd07c0a233b52f1b8c3cbdb30606ce2412da06a88b5290cdc7b6.
  - TrustAIRLab jailbreak_2023_12_25 Parquet: 55bbc5e2be771ee16ed67aed4edb5ecef5f44ac69cea317a67e5405c5c6057a4.
  - TrustAIRLab regular_2023_12_25 Parquet: 23e90010ccbc85574bf46678528cddce5b02abc86d9a047209218af65cb37c68.
  - JailBreakV_28K.csv: 72fb8beb9eb1c1a23745f4bd56430da9dff36ba42c6f5d699e68a47e14fc87c5.
  - JailbreakPrompts.xlsx: 93863bcfd217f8a47c694e5d57ed4cb6bba43f30d596ccaf6eacebb65c14051a.
  - What Features latest.csv: 0ce7838e56f4e4f292e0c74a742d26a911c7cec2da7436d2ae387204db348922.
- Pool tự nhiên sau dedup và gộp provenance: 48.372 prompt — benign 22.578, PI 9.329, JB 16.465. Trùng cùng nhãn được gộp; 178 WUSTL match đã có JB chỉ bổ sung provenance; 2 WUSTL match có nhãn benign/PI bị loại khỏi phần JB mới. Các 42 nhóm xung đột cũ tiếp tục bị loại.
- Cân bằng bằng undersampling xác định, không hoàn lại, seed 42: giữ 9.329 benign, toàn bộ 9.329 PI và 9.329 JB. JB giữ 1.581 nhóm TrustAIRLab/WUSTL, lấy 2.603 JailBreakV và 5.145 What Features. Tổng cuối: 27.987 dòng; không có split train/validation/test.
- File đầu ra hiện hành:
  - balanced_three_label.jsonl — 47.690.536 bytes; SHA-256 d4f6dc9a3c21e5eb01fc61619fd95fc4d1d30027784539fb59e21fb8fb6f4b85.
  - label_conflicts.jsonl — 47.300 bytes; SHA-256 7baa4e02511508fe9b2ec70c3fb692deae89ff5fa378a6ca797f2c657226259a.
  - manifest.json — SHA-256 3daa6afad7d52a78520ee52b5d4d61da59d1711aada9cfbd63aecdd7e2386959.
- Raw files không bị sửa. PromptScreen, PromptSentinel, ShieldLM và SPML tiếp tục audit-only. Các benchmark vẫn nằm ngoài corpus train.
- Xác minh: build hoàn tất; verifier corpus và verifier bundle đã chạy thành công sau khi xóa ba thư mục version cũ.

### v3.1.0 — 2026-10-07 — hoàn tất tái cấu trúc paper/, xóa folder version cũ và thêm validation rule

- Loại thay đổi: RESTRUCTURE + CLEANUP.
- Tái cấu trúc thư mục paper/ cho cả 10 nguồn trong `source_datasets/`:
  - 3 PDF có sẵn đã được chuẩn hóa vào `paper/`: `jailbreak_features_blackboxnlp2025` (Kirch et al., BlackboxNLP 2025), `jailbreakv28k_colm2024` (Luo et al., COLM 2024), `wustl_llm_jailbreak_usenix2024` (Yu et al., USENIX Security 2024).
  - 4 PDF toàn văn công khai mới được tải về và kiểm định header `%PDF-` hợp lệ:
    - PromptShield: `Jacob_et_al_CODASPY_2025.pdf` (958.870 bytes, SHA-256 `a15431187a14153ccba6618fec51c74362f393e6d66c05507965221a8a62f492`).
    - SPML: `Sharma_et_al_SPML_arXiv_2024.pdf` (699.698 bytes, SHA-256 `504a8561c7bf727bb6bde556558bce99cbc8fbec23e9fd4439135ac1c6d52b37`).
    - TrustAIRLab: `Shen_et_al_CCS_2024.pdf` (2.624.350 bytes, SHA-256 `0f50aa08140ca8c0c3d803a3d6d34cf006cf22456c967987839262d6a2a43154`).
    - WildJailbreak: `Jiang_et_al_NeurIPS_2024.pdf` (14.314.856 bytes, SHA-256 `0b911b9cccc13b67b4350459453bc8c1fedfecda854b9f3a67da6d8cb512202d`).
  - Đã làm phẳng toàn bộ cấu trúc lồng `paper/papers/` thành `paper/` tại `prompt_sentinel`, `promptscreen_raw` và `shieldlm`; xóa bỏ thư mục rỗng `papers/`.
  - Cập nhật toàn bộ `metadata.json`, `README.md` và `verify_dataset_bundle.py` theo đường dẫn mới `paper/`.
- Dọn dẹp thư mục version và script phân chia (split):
  - Đã xóa dứt điểm 3 thư mục version cũ trong `project_training/`: `model_ready_three_label_v1/`, `model_ready_three_label_v1_rebuild/`, `model_ready_three_label_v2/`. Corpus hiện hành `balanced_three_label.jsonl` vẫn nằm ngoài bản sao tài liệu Final-Report.
  - Đã loại bỏ 3 script split cũ: `build_three_label_corpus.py`, `create_balanced_training_view.py`, `verify_model_ready_corpus.py`.
- Bổ sung quy tắc kiểm tra (Validation rule):
  - Tích hợp hàm kiểm tra tự động `verify_source_papers()` vào `build_balanced_corpus.py` và `verify_balanced_corpus.py`: ngăn chặn triệt để việc build hoặc verify corpus nếu bất kỳ nguồn nào thiếu thư mục `paper/` hoặc thiếu PDF hợp lệ (kiểm định header `%PDF-`).
- Kết quả xác minh (Fresh verification):
  - `verify_dataset_bundle.py`: PASS (19 files by size/SHA-256, 51 relative Markdown links).
  - `verify_balanced_corpus.py`: PASS (27.987 rows cân bằng, 100% hash khớp, provenance PASS, paper PDF check PASS).

### 2026-10-07 — workbook kiểm kê (không đổi phiên bản corpus)

- Tạo `balanced_three_label_review.xlsx` để lọc và đọc corpus bằng Excel; JSONL gốc không bị sửa.
- Sheet `Data` giữ đủ 27.987 dòng với các cột `id`, `text`, `label`, `label_id`, `sources`; `Data Dictionary` mô tả ý nghĩa và vai trò từng cột. Có 8 prompt vượt giới hạn 32.767 ký tự/ô Excel, được nối nguyên văn qua 10 phần trong `Text Continuation`.
- Ký tự điều khiển không được Excel/XML hỗ trợ và chuỗi escape `_xHHHH_` được biểu diễn theo cách đảo ngược được trong workbook; đối chiếu round-trip xác nhận khôi phục đúng text, nhãn và provenance.
- Kích thước 14.053.623 bytes; SHA-256 `e51bbc2dfa117d914d73e48a1fd3c20f7f4c5cb3678625fd0336934dd94a8152`.
- Xác minh workbook: `officecli validate` PASS; `officecli view ... issues` báo 0 lỗi; kiểm tra round-trip toàn bộ 27.987 dòng PASS.

### 2026-10-07 — đăng ký thêm raw source snapshots (không đổi phiên bản corpus)

- Loại thay đổi: ADD raw source + provenance/audit. `balanced_three_label.jsonl` không được build lại hoặc chỉnh sửa; version corpus giữ nguyên v3.0.0.
- `verazuo/jailbreak_llms`: clone gốc tại commit `4f4031bf8be187f4478c7f94f42b08714722c12e`; paper CCS 2024 DOI `10.1145/3658644.3670388`; repo license MIT. Bốn CSV có 21.527 dòng vật lý (19.456 regular, 2.071 JB), 15.064 prompt unique sau NFKC/casefold/whitespace. Overlap với TrustAIRLab là 15.064/15.064 (100%); có 43 nhóm khác nhãn giữa các snapshot ngày khác nhau. Do đó snapshot được giữ để provenance, không tính như nguồn độc lập.
  - `jailbreak_prompts_2023_05_07.csv`: 1.392.506 bytes, SHA-256 `da0f4adcc40f736ad98ad5337a7521e05f680dd43e937c3b86731329e9fe6e2c`.
  - `jailbreak_prompts_2023_12_25.csv`: 3.803.571 bytes, SHA-256 `0260874b108193ca8c9010ef9cf7bff8fe8cc18b6d1a74fa48228f77c21c806f`.
  - `regular_prompts_2023_05_07.csv`: 6.507.175 bytes, SHA-256 `2286158d3078ac9624bf5f10e679c8db9d7549c882608638e4923a62fd7b6031`.
  - `regular_prompts_2023_12_25.csv`: 24.307.583 bytes, SHA-256 `fb82e3f88fbd5d9c6edf8927b138510f339b85012cab24d41d13e1665a9c5819`.
  - Bản PDF local `Shen_et_al_CCS_2024.pdf`: 2.624.350 bytes, SHA-256 `0f50aa08140ca8c0c3d803a3d6d34cf006cf22456c967987839262d6a2a43154`.
- `youbin2014/JailbreakDB`: snapshot Hugging Face revision `63912b8f9e66e87d8fdffde340391b79503c8e0d`, license CC-BY-4.0; giữ paper arXiv `2510.15476` trong `paper/`. Python CSV và DuckDB cùng xác nhận 1.094.122 regular (benign candidate) và 445.752 positive gộp `jailbreak/adversarial` (chưa ánh xạ PI/JB); 1.528.462 normalized `user_prompt` unique, 11.412 CSV record lặp, 14 nhóm có cả hai nhãn native. README HF nêu xấp xỉ 5,7M/6,6M, gần khớp newline vật lý 5.651.873/6.565.678; prompt nhiều dòng làm physical line count lớn hơn record count. SHA-256 raw khớp LFS.
  - `text_jailbreak_unique.csv`: 598.493.153 bytes, SHA-256 `fac95fd66e1c1669f0ed673018dd8ba22bab422c9b4663f92faf4912892e6885`.
  - `text_regular_unique.csv`: 745.423.829 bytes, SHA-256 `868f3cb83ca060eeada1200779f36c76ff2eba79fae0540086f4305d6c3945e1`.
  - Upstream `README.md`: 3.053 bytes, SHA-256 `d7877023f3026da50e7d4e1cdecf235c9e4c5638155b1979cc79ef810b48e6ef`; paper PDF local: 761.385 bytes, SHA-256 `5ed1ea89108158bd4a6de54699c487f49e1ac385226905f2d19741a156a3b378`.
- JailbreakDB overlap audit so theo `user_prompt`: 15.064 với TrustAIRLab, 14.348 PromptSentinel, 6.457 PromptScreen, 5.618 ShieldLM; có các regular prompt trùng nguồn khác nhưng nhãn không-benign cần rà soát. Positive JailbreakDB vẫn unmapped do taxonomy gộp; không dùng trong corpus.
- `SPML_Chatbot_Prompt_Injection` đã có sẵn trong `source_datasets/spml_prompt_injection/` cùng raw CSV và `paper/`; xác minh lại, không tải hoặc tạo bản sao mới.
- Audit cấu trúc nguồn hiện có phát hiện `shieldlm/paper/` chỉ chứa README, chưa có PDF paper riêng; ghi rõ trong source index và giữ audit-only, không đưa nguồn này vào corpus.
- Cập nhật `urldata.md`, source index, README/metadata từng nguồn, `jb_dataset_research.md`, báo cáo JSON/Markdown overlap và `verify_dataset_bundle.py`. Audit overlap PASS: chuẩn hóa label map 10 snapshot thành 45 cặp; JailbreakDB audit riêng, không ép nhãn.
- Corpus v3 giữ 27.987 dòng (9.329 mỗi nhãn), SHA-256 `d4f6dc9a3c21e5eb01fc61619fd95fc4d1d30027784539fb59e21fb8fb6f4b85` tại thời điểm ghi log; đã được thay bằng v4 bên dưới.

### v4.0.0 — 2026-10-07 — cân bằng theo nhãn và source strata (superseded by v5.0.0)

- Loại thay đổi: ADD + TRANSFORM. Raw snapshots và URL nguồn không bị ghi đè; corpus vẫn ở một file duy nhất, không có thư mục version.
- Thêm `dronefreak/PromptScreen` vào pool ứng viên dựa trên nhãn `classification` của paper. Chỉ dùng `metrics_train_set.json`; `metrics_test_set.json` được giữ ngoài corpus. Paper cục bộ là arXiv:2512.19011v1 preprint; venue phản biện và license/provenance theo từng prompt chưa xác minh. Giữ corpus local, chưa tuyên bố quyền phát hành hoặc khả năng tổng quát hóa.
- Nguồn trong v4: PromptShield, TrustAIRLab, PromptScreen-train, JailBreakV-28K, WUSTL LLMJailbreak và WhatFeatures. `verazuo/jailbreak_llms` không được cộng thêm vì trùng TrustAIRLab; SPML và JailbreakDB không nhập vì cảnh báo/nhãn gốc chưa tương đương.
- Sau dedup và loại conflict, pool tự nhiên có 67.251 prompt: benign 27.376, PI 11.282, JB 28.593. Có 4.646 nhóm conflict trong pool cơ sở + PromptScreen và 10 bản ghi xung đột khi xét JB bổ sung; `label_conflicts.jsonl` có 4.656 bản ghi, chỉ giữ hash/provenance.
- Lấy mẫu không hoàn lại theo primary source strata; quota mỗi nhãn 3.906. Benign: 1.302 PromptScreen, 1.302 PromptShield, 1.302 TrustAIRLab. PI: 1.953 PromptScreen và 1.953 PromptShield. JB: 977 JailBreakV-28K, 977 PromptScreen, 976 TrustAIRLab+WUSTL, 976 WhatFeatures.
- Tổng corpus: 11.718 dòng, 3.906 mỗi nhãn; không tạo train/validation/test split, không chạy huấn luyện hoặc inference.
- SHA-256 artifact:
  - `balanced_three_label.jsonl`: `2d86c9a95b7f33b56b87670b9dbec17f00c250ad9648131c2326eb19c9a41709` (17.638.744 bytes).
  - `label_conflicts.jsonl`: `76e0fdfee7f37d1f72223c4f281fa6ea704c4c1c47a552d78bb5a15d752f1619` (4.062.095 bytes).
- Cập nhật builder, verifiers, README, source index, overlap/JB audit, source README và `urldata.md`; workbook kiểm tra được đồng bộ theo v4.
- Workbook v4 `balanced_three_label_review.xlsx`: 5.226.058 bytes, SHA-256 `23e15050d3b60c7c1532772f7c6de28aeb09a5249438daaddfcd8eac8237d5fa`; 3 sheet gồm Data (11.718 dòng dữ liệu + header), Text Continuation (3 prompt dài) và Data Dictionary. Round-trip toàn bộ 11.718 dòng và các cột `id`, `text`, `label`, `label_id`, `sources` đã PASS; `officecli validate` PASS, `view issues` = 0; quét workbook không có cell lỗi hoặc công thức.
- Xác minh: `verify_balanced_corpus.py` và `verify_dataset_bundle.py` PASS; chi tiết hash/quota nằm trong `manifest.json`.

### 2026-10-08 — làm rõ nguồn và xóa folder WildJailbreak tham chiếu (corpus không đổi)

- Xóa `source_datasets/wildjailbreak_allenai/` theo yêu cầu. Preflight xác nhận folder nằm trong `source_datasets/`, không có symlink/reparse point và không chứa payload dữ liệu; có 5 file gồm README/cache và PDF paper. PDF đã xóa: 14.314.856 bytes, SHA-256 `0b911b9cccc13b67b4350459453bc8c1fedfecda854b9f3a67da6d8cb512202d`; README: SHA-256 `4b2b07ab6095ff56b1a853c6d3dd44ddad9b314d581d5c5a3fe6f92d51f82698`. URL HF, paper NeurIPS 2024 và trạng thái gated vẫn được giữ trong inventory.
- Không thay đổi raw data totals, corpus v4, manifest, nhãn hoặc sampling. Sửa `urldata.md`, source index, overlap report/generator và JB research report để không trỏ tới folder đã xóa.
- Ghi rõ PromptSentinel có 1.264 JB tổng thể và 1.019 JB train (0,87%), gated, 61.781 train rows có license chưa xác định, không có paper riêng cho bộ tổng hợp. Khuyến nghị tiếp tục audit-only; không xóa chỉ vì JB ít. Nếu yêu cầu lưu/train chỉ nguồn có paper riêng và license rõ, cần quyết định riêng trước khi xóa raw snapshot vì nó còn nhiều prompt riêng.
- Corpus version vẫn `4.0.0`; verifier bundle kiểm tra lại các folder bắt buộc, hash và liên kết sau cập nhật.

### 2026-10-08 — làm rõ bảng raw, trạng thái sử dụng nguồn và đề xuất 30k (corpus không đổi)

- Sửa `urldata.md` để gọi số lượng là bản ghi logic, thêm cột trạng thái từng nguồn trong corpus v4, và giải thích `Khác / Chưa ánh xạ` là bucket loại trừ chứ không phải nhãn thứ tư.
- Nêu rõ các trường JailBreakV dùng/loại: v4 chọn `jailbreak_query` theo format `Template`, `Persuade`, `Logic`; 8.000 dòng còn lại gồm format `SD`, `SD_typo`, `figstep`, `typo` (không phải tất cả đều là ảnh), còn `RedTeam_2K.csv.question` là harmful query seed chứ không phải jailbreak wrapper.
- Ghi rõ 1.094.122 bản ghi JailbreakDB `regular` chỉ là ứng viên Benign, không được xem là mẫu đã thẩm định hoặc đã đưa vào v4. Kiểm tra lại tổng raw: 1.914.493 bản ghi ở 11 folder có payload; tổng các cột khớp, nhưng gồm mirror verazuo/TrustAIRLab và không phải số prompt độc lập.
- Thêm đánh giá đề xuất candidate 30.000 (10.000 mỗi nhãn): khả thi theo pool hiện có nhưng PI sẽ gồm 1.953 PromptScreen + 8.047 PromptShield (19,5%/80,5%). Chưa tạo corpus 30k, chưa chia split và chưa chạy huấn luyện; giữ v4 11.718 làm tham chiếu.
- Đề xuất giữ raw audit-only theo mặc định; verazuo là candidate giảm payload vì prompt unique trùng TrustAIRLab 100%, nhưng cần bảo toàn revision/hash/43 nhóm khác nhãn trước khi xóa. Không xóa folder nguồn trong lần cập nhật này.
- Làm rõ pool PI v4 chỉ có PromptScreen-train và PromptShield-train dù các snapshot khác cũng mang PI: thêm số lượng và lý do audit-only cho ShieldLM, SPML, PromptSentinel, JailbreakDB. Mục tiêu 30k được gắn rõ với pool đủ điều kiện hiện tại, không phải toàn bộ raw folders.
- Kiểm tra filesystem: `source_datasets/wildjailbreak_allenai/` không tồn tại. Corpus và raw snapshots không đổi; xác minh mới nhất: `verify_dataset_bundle.py` PASS (28 files, 63 relative links), `verify_balanced_corpus.py` PASS (11.718 dòng, 3.906 mỗi nhãn).
### 2026-10-08 — đề xuất xử lý component và hiệu chỉnh mapping JailbreakDB (corpus không đổi)

- Sửa đề xuất xử lý folder trong `urldata.md`: ShieldLM cần được phân rã theo `source`; sau khi tạo và kiểm hash các component đủ paper/terms thì đề xuất xóa payload Parquet aggregate, giữ manifest/audit provenance. PromptSentinel không xóa nguyên khối; đề xuất phân rã theo `source_dataset`, giữ `all_sources`, loại/quarantine phần không paper hoặc license chưa rõ. Không có lệnh xóa hoặc extraction nào được thực hiện.
- Ghi candidate PromptSentinel train theo primary source: Lakera 801 PI; SPML 10.077 PI + 2.684 Benign; TrustAIRLab 606 JB + 10.044 Benign; ToxicChat 116 JB + 7.583 Benign; OpenAssistant 4.138 Benign. Các số chưa dedup xuyên nguồn và chưa được nhập vào v4. Jayavibhav chiếm 61.781 train rows có `source_license=unspecified`; giữ ngoài corpus theo gate paper/license hiện tại.
- Với ShieldLM, audit train theo `source` ghi nhận SPML 8.798 PI + 2.341 Benign, TrustAIRLab 702 JB, InjecAgent 738 PI + 24 Benign, JailbreakBench 135 Benign. Component papers: arXiv:2402.11755, 2308.03825, 2403.02691, 2404.01318. Ghi nhận license SPML và TrustAIRLab không khớp giữa card ShieldLM và snapshot nguồn trực tiếp; chưa chấp nhận các dòng này để train.
- Hiệu chỉnh inventory JailbreakDB: paper SoK arXiv:2510.15476 mô tả positive là jailbreak system–user pairs; mapping đề xuất là 445.752 JB candidate, 0 PI. `regular` 1.094.122 vẫn là Benign candidate. Có 14 nhóm normalized `user_prompt` nằm ở cả hai nhãn; overlap TrustAIRLab 15.064 unique prompts. Chưa thêm vào corpus.
- Vì mapping inventory trên, tổng source raw (có mirror và candidate) được cập nhật từ Benign 1.291.279 / PI 111.089 / JB 56.373 / Other 455.752 thành Benign 1.291.279 / PI 111.089 / JB candidate 502.125 / Other 10.000; tổng vẫn 1.914.493. Tổng với benchmark CSV Qualifire và OR-Bench vẫn 2.001.826, nhưng cột JB candidate là 504.124 và Other là 10.655.
- Đề xuất giảm trùng: xóa bốn CSV payload trong `verazuo_jailbreak_llms` sau khi giữ commit, hash, 43 nhóm khác nhãn và overlap report; mọi prompt unique chuẩn hóa đã trùng TrustAIRLab (15.064/15.064). Chưa xóa folder hay payload.
- Không thay đổi corpus v4, manifest, workbook hoặc split; không huấn luyện/inference. Cập nhật `urldata.md`, `source_datasets/README.md`, README của PromptSentinel, ShieldLM và JailbreakDB để phân biệt đề xuất với dữ liệu đã thực hiện.

### v5.0.0 — 2026-10-08 — corpus 40.000 mẫu, tỷ lệ benign:PI:JB = 2:1:1

- Loại thay đổi: TRANSFORM + RESAMPLE. Không tải hoặc sửa raw snapshots; không có thư mục version riêng. Thay corpus hiện hành v4 bằng một corpus 40.000 dòng tại `balanced_three_label.jsonl`.
- Pool sau ánh xạ nhãn, exact dedup và loại nhóm xung đột: 67.251 prompt (benign 27.376, PI 11.282, JB 28.593). Giữ 20.000 benign, 10.000 PI và 10.000 JB bằng lấy mẫu không hoàn lại, capped-equal theo source strata; seed cho từng stratum nằm trong `manifest.json`.
- Phân bổ nguồn đã chọn: benign—PromptScreen 6.667, PromptShield 6.667, TrustAIRLab 6.666; PI—PromptScreen 1.953, PromptShield 8.047; JB—JailBreakV-28K 2.809, PromptScreen 2.809, TrustAIRLab+WUSTL 1.573, WhatFeatures 2.809.
- Pool còn ngoài corpus: benign 7.376, PI 1.282, JB 18.593. PI vẫn lệch nguồn (19,53% PromptScreen, 80,47% PromptShield); kích thước lớp cân bằng không chứng minh độc lập nguồn hay khả năng tổng quát hóa.
- Exact duplicate và conflict processing giữ theo manifest hiện hành; `label_conflicts.jsonl` gồm 4.656 bản ghi, không đổi. Near-duplicate theo họ/ngữ nghĩa chưa được loại tự động. Chưa tạo train/validation/test split hoặc holdout FPR; 2.500–3.000 benign độc lập là phương án đánh giá tiếp theo sau khi xác định nhóm prompt và kiểm overlap.
- Artifact SHA-256: `balanced_three_label.jsonl` 58.649.314 bytes, `2b6588e9aa091d536a25a878102df866090a2539f1bf5dbbd05d6ca6a7d09bfe`; `label_conflicts.jsonl` 4.062.095 bytes, `76e0fdfee7f37d1f72223c4f281fa6ea704c4c1c47a552d78bb5a15d752f1619`.
- Đồng bộ `balanced_three_label_review.xlsx`: 40.000 dòng, cột `id`, `text`, `label`, `label_id`, `sources`; có `Data Dictionary` và `Text Continuation` để giữ prompt dài vượt giới hạn ô Excel. Workbook có 17.846.693 bytes, SHA-256 `743f22446b86db86e3b1f7172c6aeb9189aed9846b203b4c1dad95ad69e4a3fa`.
- Cập nhật README, `urldata.md`, manifest, builder, verifiers và các audit liên quan.
- Xác minh corpus tại thời điểm tạo v5: `verify_balanced_corpus.py` PASS (40.000 dòng; 20.000 benign, 10.000 PI, 10.000 JB; 40.000 ID chuẩn hóa duy nhất; source provenance, source hashes và artifact hashes PASS; 4.656 conflict groups; lúc này chưa tạo split). `verify_dataset_bundle.py` PASS (28 file, hash và 61 liên kết Markdown). `officecli validate balanced_three_label_review.xlsx` PASS; round-trip 40.000 dòng workbook PASS; hash bản được promote trùng với workbook đã kiểm tra.


### 2026-10-08 — tạo split nghiên cứu nội bộ cho v5 (corpus không đổi)

- Tạo train/validation/test group-aware từ corpus v5, seed 42, mục tiêu 70/15/15; lần lượt có 28.280, 5.858 và 5.862 dòng. Không loại dòng khỏi corpus.
- Trạng thái split: `frozen_local_research_split`. Manifest khóa SHA-256 corpus và manifest nguồn; chi tiết nhóm, số dòng theo nhãn/nguồn và giới hạn nằm trong [split manifest](splits/split_manifest.json).
- Đây là split local research; chưa có holdout benign độc lập ngoài v5. Không huấn luyện hoặc inference trong bước này.

### 2026-10-08 — kiểm toán lại semantics và trạng thái README (không đổi corpus)

- Làm rõ PromptShield dùng trong builder là `hendzh/PromptShield` tại revision `a5234cb1f5cdb256600cab64b8c961195b5e8404`; nhãn nhị phân `1 → PI`, `0 → benign` là mapping theo bài toán nguồn. `8.047` là quota PI của corpus v5 sau xử lý pool, không phải quy mô dataset hay số liệu paper. Nhãn `0` chưa được adjudicate riêng để loại trừ JB theo taxonomy ba lớp. Repository `gaurav-nimbalkar/PromptShield` có ID khác; chưa xác minh tương đương revision/hash với snapshot được dùng.
- Đồng bộ README nguồn và audit JB sang trạng thái/quota v5; PromptScreen paper được pin ở arXiv v1. Các con số v4/v3 giữ nguyên ở vị trí lịch sử.
- Chỉ sửa tài liệu; không thay đổi raw snapshots, JSONL corpus, workbook, manifest nguồn, split JSONL hoặc split manifest.
- Xác minh sau cập nhật: `verify_balanced_corpus.py`, `verify_dataset_bundle.py`, `split_balanced_corpus.py --verify`; không chạy training/inference.


### 2026-10-09 — đánh giá jackhhao/jailbreak-classification (corpus và split không đổi)

- Data card HF mô tả hai nhãn benign/jailbreak, không có nhãn PI; phần jailbreak có lineage Verazuo. Snapshot Verazuo local có 15.064 prompt duy nhất sau chuẩn hóa và toàn bộ đều trùng TrustAIRLab, nên không nhập thêm phần JB này như một nguồn độc lập.
- Không tải hoặc nhập nguyên gói HF vào v5. Card nêu OpenOrca và GPTeacher là nguồn benign, nhưng chưa có audit overlap từng dòng; kết luận không nhập nguyên gói không đồng nghĩa đã chứng minh toàn bộ dữ liệu HF bị trùng. Audit candidate hiện ghi nhận jackhhao là component trong aggregate PromptSentinel và ShieldLM; hai aggregate này chưa được dùng trong v5.
- Câu “chưa tạo split” trong mục tạo corpus v5 là trạng thái tại thời điểm tạo corpus; mục tạo split nội bộ phía sau ghi nhận split frozen_local_research_split đã được tạo. Cập nhật urldata.md để trỏ tới split manifest và phân biệt split nội bộ với holdout benign/FPR ngoài v5.
- Chỉ cập nhật tài liệu; không tải dữ liệu, không thay đổi raw snapshots, corpus JSONL, workbook, manifest nguồn, split files hoặc split manifest. HF card: https://huggingface.co/datasets/jackhhao/jailbreak-classification.

### 2026-10-09 — version hóa mã split (corpus và split không đổi)

- Đưa script chuẩn thư viện Python [split_v5_dataset.py](../../../../scripts/split_v5_dataset.py) vào repository. Script nhận `--dataset-root` local, hỗ trợ `--dry-run`, `--apply`, `--verify`; không chứa corpus, prompt hoặc đường dẫn máy cá nhân. `--apply` từ chối ghi đè split đã khóa.
- Dùng cộng tuần tự cho cost chia nhóm để replay không phụ thuộc thay đổi thuật toán `sum()` giữa runtime Python. `--verify` PASS trên Python 3.11.16 và 3.14.7: 40.000 ID, hash, coverage, phân bố và tách prompt-family đều khớp; 0 replay mismatch.
- Các manifest và payload split đã khóa không thay đổi. Bản Git chỉ lưu code, metadata và tài liệu; không lưu JSONL/ID split, workbook hoặc raw snapshots.
- Đây là mốc version hóa công cụ cho split nội bộ, không phải phiên bản corpus mới, phê duyệt quyền dữ liệu, xác nhận nhãn gold, huấn luyện hoặc đánh giá mô hình.
## Quy tắc cho phiên bản sau

Mỗi thay đổi dữ liệu phải ghi: ngày và version; loại thay đổi; nguồn, URL/paper/revision; file nguồn và SHA-256; tổng/số lượng từng nhãn trước-sau; quy tắc mapping/dedup/balancing; file đầu ra và SHA-256; kết quả verifier. Không tạo thư mục version mới trừ khi người dùng yêu cầu rõ.
