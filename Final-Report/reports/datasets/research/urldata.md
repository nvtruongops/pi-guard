# Báo cáo Kiểm kê URL & Số lượng Dữ liệu Nguồn (Dataset Inventory)

> **Dự án**: PI-Guard — A Machine-Learning Guardrail for Detecting Prompt Injection and Jailbreak Attacks
> **Ngày kiểm kê**: 2026-10-09
> **Thư mục tài liệu**: Final-Report/reports/datasets/research
> **Dữ liệu split cục bộ**: Final-Report/notebooks/data/splits; payload bị Git ignore và bản sao tài liệu không chứa snapshot raw hoặc corpus gốc.
> **Mục đích**: Danh mục nguồn, số lượng, provenance và trạng thái sử dụng trong corpus PI-Guard.
> **Phạm vi**: Thống kê snapshot raw phản ánh workspace nghiên cứu nguồn; bản sao Final-Report giữ tài liệu và audit metadata, còn các tệp split được đặt riêng trong thư mục data cục bộ. Chưa có kết quả huấn luyện hay đánh giá mô hình.

---

## 1. Quy ước Đếm & Phân loại

1. **Phạm vi tính toán**: Đếm số lượng bản ghi logic (records/rows) thực tế trong các tệp dữ liệu đã tải về máy tại hai không gian lưu trữ:
   - `source_datasets/`: Snapshot raw giữ provenance và audit; không phải mọi nguồn đều đủ điều kiện đưa vào corpus.
   - `benchmarks/`: Dữ liệu held-out phục vụ kiểm thử và đánh giá độc lập.
   *(Không tính các file phụ trợ như README, bài báo khoa học, metadata, cache hoặc script tải)*.
2. **Nguyên tắc bản ghi gốc (Raw Payloads)**: Số lượng được ghi nhận trước khi thực hiện khử trùng lặp (deduplication) hoặc lấy mẫu cân bằng (balanced sampling). Các bản ghi lặp nội tại trong từng split/file vẫn được giữ nguyên. Với CSV có newline bên trong prompt, một bản ghi CSV có thể chiếm nhiều dòng vật lý; báo cáo này đếm bản ghi CSV, không đếm newline.
3. **Ánh xạ 3 nhãn chuẩn hóa**:
   - `Benign (0)`: Câu hỏi/chỉ dẫn thông thường, văn bản hội thoại chuẩn, các mẫu hard-benign hoặc over-refusal benign.
   - `PI (1)`: Tấn công Prompt Injection (System Prompt Leakage, Direct Injection, Indirect Injection, Goal Hijacking).
   - `JB (2)`: Tấn công Jailbreak (DAN, Roleplay, Dual-Persona, Opposing Multi-Turn, Adversarial Attacks).
    - `Khác / Chưa ánh xạ (không vào 3 lớp)`: Bản ghi chưa được nhận vào một trong ba lớp theo chính sách ánh xạ hiện tại. Ví dụ: JailBreakV có các format ngoài tập text được chọn và các query hại gốc. Paper SoK mô tả positive của JailbreakDB là các cặp jailbreak, nên positive được ghi là **ứng viên JB**, không phải PI; vẫn cần xử lý context, conflict và overlap trước khi dùng. Đây là bucket kiểm kê/loại trừ, không phải nhãn thứ tư.
4. **Tính độc lập giữa các nguồn**: Tổng theo nguồn là tổng số bản ghi logic trong các tệp tải về, không đồng nhất với số lượng prompt duy nhất trên toàn tập (do có thể có prompt lặp nội bộ, snapshot cùng nguồn hoặc mirror giữa repo).

---

## 2. Nguồn Dataset Tải về (`source_datasets/`; nguồn train candidate và audit-only)

### 2.1. Bảng Phân bố Định lượng Bản ghi Raw (Quantitative Distribution)

| STT | Kho Dữ Liệu Nguồn (`source_datasets/`) | Tổng bản ghi raw | Benign (0; gồm ứng viên) | Prompt Injection (1) | Jailbreak (2) | Khác / Chưa ánh xạ | Tỷ trọng & nhãn trọng tâm | Dùng trong corpus v5 / tình trạng folder |
| :---: | :---| ---:| ---:| ---:| ---:| ---:| :---| :---|
| 1 | `sevdeawesome/jailbreak_success` | 10.800 | 0 | 0 | 10.800 | 0 | 100% JB (`jailbreak_prompt_text`) | **Có** — JB source stratum (`WhatFeatures`). |
| 2 | `JailBreakV-28K/JailBreakV-28k` | 30.000 | 0 | 0 | 20.000 | 10.000 | 66,7% JB theo format được chọn; 33,3% format/seed bị loại | **Có một phần** — v5 chỉ dùng `jailbreak_query` với format `Template`, `Persuade`, `Logic`; 8.000 dòng ở format khác và 2.000 query hại gốc không nhập v5. |
| 3 | `nuhmanpk/prompt-sentinel` | 145.781 | 82.458 | 62.059 | 1.264 | 0 | JB 0,87% snapshot; train 1.019/116.854 (0,87%) | **Không dùng nguyên khối; đề xuất tách theo `source_dataset`** — giữ `all_sources`; tạo component candidate có paper/terms, loại hoặc quarantine phần chưa đạt. Chưa xóa raw snapshot. |
| 4 | `dronefreak/PromptScreen` | 30.937 | 10.136 | 2.100 | 18.701 | 0 | 60,5% JB · 32,8% Benign · 6,7% PI | **Có một phần** — v5 chỉ dùng train; paper là preprint và provenance/license từng prompt còn mở. |
| 5 | `hendzh/PromptShield` | 43.425 | 26.984 | 16.441 | 0 | 0 | 62,1% Benign · 37,9% PI | **Có một phần** — v5 dùng train split; raw total ở đây cộng train/val/test. |
| 6 | `Abdennebi/shieldlm-prompt-injection` | 54.162 | 35.197 | 17.947 | 1.018 | 0 | 65,0% Benign · 33,1% PI · 1,9% JB | **Không dùng nguyên khối; đề xuất tách theo `source`** — paper của thành phần không chứng minh bộ tổng hợp; sau khi đóng gói component có paper/terms và xác minh hash, đề xuất xóa payload aggregate. Chưa xóa. |
| 7 | `reshabhs/SPML_Chatbot_Prompt_Injection` | 16.012 | 3.470 | 12.542 | 0 | 0 | 78,3% PI · 21,7% Benign | **Không, audit-only** — nhãn gốc nhị phân, không có JB; prompt trùng ShieldLM không đồng nghĩa toàn bộ record có cùng system context. |
| 8 | `TrustAIRLab/in-the-wild-jailbreak-prompts` | 21.527 | 19.456 | 0 | 2.071 | 0 | 4 snapshot config; có prompt lặp giữa các ngày | **Có** — benign/JB strata trong v5; raw count cộng cả bốn config, không phải số prompt cuối duy nhất. |
| 9 | `WUSTL-CSPL/LLMJailbreak` | 448 | 0 | 0 | 448 | 0 | 100% JB (USENIX Security 2024) | **Có** — JB strata gộp với TrustAIRLab. |
| 10 | `allenai/wildjailbreak` *(tham chiếu ngoài máy)* | *0* | — | — | — | — | Gated; payload local không có | **Không có folder local** — đã xóa 2026-10-08; chỉ giữ link paper/card. |
| 11 | `verazuo/jailbreak_llms` (GitHub snapshot gốc) | 21.527 | 19.456 | 0 | 2.071 | 0 | 15.064 prompt unique trùng TrustAIRLab; có 43 nhóm khác nhãn | **Không tính vào v5** — giữ để truy nguyên mirror/khác nhãn; là ứng viên giảm dung lượng payload sau khi lưu audit và hash. |
| 12 | `youbin2014/JailbreakDB` | 1.539.874 bản ghi CSV | 1.094.122* | 0 | 445.752† | 0 | Positive được paper mô tả là jailbreak/adversarial system–user pairs; ứng viên JB, không có PI riêng | **Audit-only / JB candidate** — regular là Benign candidate; positive là JB candidate theo paper, chưa vào v5. Cần xử lý 14 nhóm prompt trùng khác nhãn, context và overlap. |
| **Σ** | **Tổng 11 repo có payload cục bộ** | **1.914.493** | **1.291.279*** | **111.089** | **502.125†** | **10.000** | **67,45% Benign/regular candidate · 5,80% PI · 26,23% JB candidate · 0,52% chưa ánh xạ; tổng có mirror** | **Tổng kiểm kê raw, không phải số prompt độc lập hoặc corpus train.** |

\* JailbreakDB `regular` là Benign candidate, chưa phải benign đã thẩm định. † Positive là JB candidate theo paper, chưa nhập vào corpus.

“Khác / Chưa ánh xạ” là bucket loại trừ, không phải nhãn thứ tư; 10.000 dòng hiện là JailBreakV chưa được nhận theo mapping của đồ án. Cách đọc field và mapping chi tiết ở Mục 2.2.

Tổng raw gồm bản ghi lặp nội bộ, snapshot và mirror; không phải số prompt độc lập. Cột “Dùng trong corpus” chỉ mô tả phần được chọn, không phải toàn bộ payload của repo.

### 2.2. Bảng Thông tin Truy nguyên, URL & Quy ước Ánh xạ Nhãn (Provenance & Links)

| STT | Kho Dữ Liệu | Nền Tảng & Snapshot | Liên Kết Tải Nguồn | Quy Ước Ánh Xạ Nhãn & Ghi Chú Kỹ Thuật |
| :---: | :---| :---| :---| :---|
| 1 | `sevdeawesome/jailbreak_success` | Hugging Face<br>`tree/12bad23` | [HF Snapshot Tree](https://huggingface.co/datasets/sevdeawesome/jailbreak_success/tree/12bad235ee184287bc5f41ec2341489501a30049) | Dùng trường `jailbreak_prompt_text` làm nhãn JB (thể hiện ý định tấn công, bất kể thành công/thất bại). 916 dòng lặp chính xác được giữ nguyên số gốc. |
| 2 | `JailBreakV-28K/JailBreakV-28k` | Hugging Face<br>GitHub (`SaFo-Lab`) | [HF Snapshot](https://huggingface.co/datasets/JailbreakV-28K/JailBreakV-28k/tree/f949ca582fff13d396ac8fce59596afafb2b78d3)<br>[GitHub SaFo-Lab](https://github.com/SaFo-Lab/JailBreakV_28K) | `JailBreakV_28K.csv` có cột `jailbreak_query`, `redteam_query`, `format`, `image_path`. Mapping v5 lấy `jailbreak_query` khi `format` là `Template`, `Persuade` hoặc `Logic` (20.000 dòng, 5.000 prompt unique). 8.000 dòng format còn lại (`SD`, `SD_typo`, `figstep`, `typo`) chưa được nhận vào corpus text-only; ba format đầu có nội dung ảnh. `RedTeam_2K.csv` có cột `question` là query hại gốc, không phải jailbreak wrapper; loại khỏi nhãn JB. |
| 3 | `nuhmanpk/prompt-sentinel` | Hugging Face<br>`tree/f521882` | [HF Snapshot Tree](https://huggingface.co/datasets/nuhmanpk/prompt-sentinel/tree/f5218824e24fbb6cd383b55aee61c71b1919a6c8) | Snapshot gated, paper folder chứa nguồn thành phần chứ không có paper cho aggregate. Đề xuất phân rã theo `source_dataset`, giữ `all_sources`; 61.781 train rows `source_license=unspecified` và các phần không paper ở trạng thái loại/quarantine. |
| 4 | `dronefreak/PromptScreen` | GitHub Raw<br>`commit/496653a` | [Train JSON](https://raw.githubusercontent.com/dronefreak/PromptScreen/496653aba7a39ae6bdcb775c067a3bdb2471acc7/offence/metrics_train_set.json)<br>[Test JSON](https://raw.githubusercontent.com/dronefreak/PromptScreen/496653aba7a39ae6bdcb775c067a3bdb2471acc7/offence/metrics_test_set.json) | Snapshot raw có train (28.771) + reported-test (2.166); paper là arXiv preprint và chưa xác minh peer review. v5 chỉ dùng train JSON, không dùng reported-test. Ánh xạ theo nhãn gốc `classification`; license/provenance theo từng prompt còn chưa xác minh. |
| 5 | `hendzh/PromptShield` | Hugging Face<br>`tree/a5234cb` | [HF Snapshot Tree](https://huggingface.co/datasets/hendzh/PromptShield/tree/a5234cb1f5cdb256600cab64b8c961195b5e8404) | Cộng gộp 3 split: train (18.909), val (1.000), test (23.516). Nhãn nhị phân: `0 = Benign`, `1 = Prompt Injection`. |
| 6 | `Abdennebi/shieldlm-prompt-injection` | Hugging Face<br>`tree/2333058` | [HF Snapshot Tree](https://huggingface.co/datasets/Abdennebi/shieldlm-prompt-injection/tree/23330588198f0143120e93b7d7b31cc164cd5403) | Cộng gộp 3 split. Đề xuất phân rã theo `source`; direct/indirect injection → PI, `jailbreak` → JB, `benign` → Benign chỉ sau kiểm tra source paper, context và terms. Aggregate không có paper riêng. |
| 7 | `reshabhs/SPML_Chatbot_Prompt_Injection` | Hugging Face Hub | [HF Dataset Card](https://huggingface.co/datasets/reshabhs/SPML_Chatbot_Prompt_Injection) | Nhãn nhị phân gốc: `Prompt injection = 0` $\rightarrow$ Benign, `1` $\rightarrow$ PI. Repo không có nhãn JB riêng. |
| 8 | `TrustAIRLab/in-the-wild-jailbreak-prompts` | Hugging Face Hub<br>GitHub (`verazuo`) | [HF Dataset](https://huggingface.co/datasets/TrustAIRLab/in-the-wild-jailbreak-prompts)<br>[GitHub verazuo](https://github.com/verazuo/jailbreak_llms/tree/main/data) | Cộng gộp 4 Parquet snapshot/config (`regular_*`, `jailbreak_*`): 21.527 raw records, có prompt lặp giữa các ngày; README nguồn báo 15.140 prompt cho bộ công bố. `regular` là Benign candidate, `jailbreak=True` là JB. |
| 9 | `WUSTL-CSPL/LLMJailbreak` | GitHub (`WUSTL-CSPL`)<br>`commit/2a9e665` | [GitHub Tree](https://github.com/WUSTL-CSPL/LLMJailbreak/tree/2a9e665769de1bbfa657b6e6a9f88d9d427bc57c) | Đọc 448 dòng trong cột Prompt của workbook nghiên cứu USENIX Security 2024. Một prompt lặp chính xác vẫn được tính trong số lượng thô. |
| 10 | `allenai/wildjailbreak` *(tham chiếu ngoài máy; folder local đã xóa 2026-10-08)* | Hugging Face Hub | [HF Dataset Card](https://huggingface.co/datasets/allenai/wildjailbreak)<br>[NeurIPS 2024 paper](https://proceedings.neurips.cc/paper_files/paper/2024/hash/54024fca0cef9911be36319e622cde38-Abstract-Conference.html) | Upstream báo khoảng 261.534 cặp prompt-response; gated, không có payload local. Vanilla harmful không tự động là JB; không cộng vào tổng. |
| 11 | `verazuo/jailbreak_llms` | GitHub<br>`commit/4f4031bf` | [GitHub commit](https://github.com/verazuo/jailbreak_llms/tree/4f4031bf8be187f4478c7f94f42b08714722c12e)<br>[CCS 2024 paper](https://doi.org/10.1145/3658644.3670388) | Snapshot gốc có 21.527 dòng qua bốn file/snapshot; 15.064 prompt duy nhất chuẩn hóa trùng toàn bộ TrustAIRLab. Giữ riêng để tham khảo provenance, không cộng như nguồn độc lập. |
| 12 | `youbin2014/JailbreakDB` | Hugging Face<br>`revision/63912b8` | [HF snapshot](https://huggingface.co/datasets/youbin2014/JailbreakDB/tree/63912b8f9e66e87d8fdffde340391b79503c8e0d)<br>[SoK arXiv paper](https://arxiv.org/abs/2510.15476) | Python CSV và DuckDB cùng đếm 1.094.122 `regular` records, 445.752 `jailbreak=1` records. Paper mô tả positive là jailbreak system–user pairs: map thành **JB candidate**, không phải PI. Trước khi dùng cần xử lý 14 nhóm `user_prompt` có cả hai nhãn, giữ context và dedup overlap. |

---

## 3. Repo Benchmark Độc lập (`benchmarks/`)

Các tập dữ liệu dưới đây được **cô lập hoàn toàn** khỏi quá trình huấn luyện, tiền xử lý và tinh chỉnh tham số của mô hình PI-Guard, chỉ dùng để đánh giá độ bền vững ngoại suy (held-out evaluation).

| Benchmark / Dataset | Snapshot & Provenance | Liên Kết Tải Nguồn | Dòng Tải Cục Bộ | Phân Bố Nhãn Ghi Nhận | Mục Đích Đánh Giá |
| :---| :---| :---| ---:| :---| :---|
| `bench-llm/or-bench` | ICML 2025<br>Revision `e36d8b8` | [HF Dataset](https://huggingface.co/datasets/bench-llm/or-bench)<br>[ICML 2025 Paper](https://proceedings.mlr.press/v267/cui25a.html) | 82.333 dòng file | **Benign**: 81.678<br>**PI**: 0<br>**JB**: 0<br>**Khác (Toxic)**: 655 | Kiểm thử hiện tượng từ chối quá mức (Over-refusal stress test). Hợp 3 tệp (`80k`, `hard-1k`, `toxic`) có 81.015 prompt duy nhất (80.360 Benign, 655 Toxic/Khác). |
| `rogue-security/prompt-injections-benchmark` (Qualifire) | Qualifire Benchmark<br>Revision `9ef1aa4` | [HF Dataset](https://huggingface.co/datasets/rogue-security/prompt-injections-benchmark) | 5.000 prompt<br>*(Bản CSV & Parquet là 2 dạng mirror)* | **CSV**: 3.001 Benign / 1.999 JB<br>**Parquet**: 2.997 Benign / 2.003 JB | Đánh giá độc lập khả năng phát hiện Jailbreak đối kháng. Có sai khác 8 nhãn giữa hai định dạng file tải. |

---

## 4. Tổng hợp Toàn bộ Dữ liệu Tải về

| Phạm Vi Dữ Liệu | Số bản ghi / prompt tính toán | Benign (0; gồm ứng viên) | Prompt Injection (1) | Jailbreak (2) | Khác / Chưa Ánh Xạ |
| :---| ---:| ---:| ---:| ---:| ---:|
| **11 repo raw có payload (`source_datasets/`, gồm nguồn audit-only)** | 1.914.493 | 1.291.279 | 111.089 | 502.125† | 10.000 |
| **Benchmark OR-Bench** | 82.333 | 81.678 | 0 | 0 | 655 |
| **Benchmark Qualifire (Bản chuẩn CSV)** | 5.000 | 3.001 | 0 | 1.999 | 0 |
| **Tổng tải về thực tế (Không cộng trùng mirror Qualifire)** | **2.001.826** | **1.375.958** | **111.089** | **504.124†** | **10.655** |

> [!WARNING]
> Số lượng là bản ghi logic raw, không phải prompt độc lập; tổng có mirror verazuo/TrustAIRLab và các dòng lặp giữa split. Qualifire CSV và Parquet là hai biểu diễn của 5.000 prompt nhưng khác 8 nhãn; bảng chỉ tính CSV để tránh cộng đôi.

---
## 5. Corpus dẫn xuất phục vụ đồ án (`project_training/`)

### Phạm vi và số lượng

Corpus v5.0.0 là tập ứng viên cho bước chuẩn bị huấn luyện. Split group-aware nội bộ đã được đóng băng cho nghiên cứu theo tỷ lệ 70/15/15 (28.280 train, 5.858 validation, 5.862 test; xem [split manifest](project_training/splits/split_manifest.json)); đây chưa phải holdout độc lập ngoài corpus và chưa có mô hình được huấn luyện/đánh giá. Số lượng raw, URL tải và ánh xạ gốc theo repo ở Mục 2; các con số dưới đây là corpus sau lọc và lấy mẫu.

| Corpus | Đường dẫn | Tổng | Benign | PI | JB | Tỷ lệ |
|---|---|---:|---:|---:|---:|---:|
| v5.0.0 | Final-Report/notebooks/data/splits/{train,validation,test}.jsonl | 40.000 | 20.000 | 10.000 | 10.000 | 2:1:1 |

| Pool sau exact dedup/conflict filtering | Benign | PI | JB | Tổng |
|---|---:|---:|---:|---:|
| Trước lấy mẫu | 27.376 | 11.282 | 28.593 | 67.251 |
| Giữ trong v5 | 20.000 | 10.000 | 10.000 | 40.000 |
| Còn ngoài corpus | 7.376 | 1.282 | 18.593 | 27.251 |

### Phân bổ nguồn trong v5

Quota được lấy không hoàn lại theo source strata; seed và provenance nằm trong [manifest](project_training/manifest.json).

| Nhãn | Source stratum | Mẫu | Tỷ lệ trong nhãn |
|---|---|---:|---:|
| Benign | PromptScreen | 6.667 | 33,34% |
| Benign | PromptShield | 6.667 | 33,34% |
| Benign | TrustAIRLab | 6.666 | 33,33% |
| PI | PromptScreen | 1.953 | 19,53% |
| PI | PromptShield | 8.047 | 80,47% |
| JB | JailBreakV-28K | 2.809 | 28,09% |
| JB | PromptScreen | 2.809 | 28,09% |
| JB | TrustAIRLab + WUSTL | 1.573 | 15,73% |
| JB | WhatFeatures | 2.809 | 28,09% |

PI trong corpus vẫn tập trung ở PromptShield (80,47%); PromptScreen chỉ có 1.953 PI đủ điều kiện. Cân bằng số lượng lớp vì thế không loại được khả năng mô hình học dấu hiệu riêng của nguồn.

### Trạng thái nguồn và đề xuất xử lý

Folder raw có nhiều hơn hai nguồn PI, nhưng chỉ PromptScreen và PromptShield được chấp nhận vào pool PI hiện tại. Các nguồn còn lại cần xử lý nhãn, context, paper, license hoặc overlap trước khi nhập.

| Nguồn | Trạng thái / đề xuất | Lý do chính |
|---|---|---|
| PromptScreen | Dùng train split | Có nhãn ba lớp; paper là preprint, license/provenance theo prompt còn mở. Test split để ngoài corpus. |
| PromptShield | Dùng train split | Nhãn Benign/PI rõ; các split khác không được cộng toàn bộ vào v5. |
| TrustAIRLab / verazuo | Dùng TrustAIRLab; không cộng verazuo lần nữa | Hai snapshot cùng lineage; prompt unique verazuo trùng TrustAIRLab. Giữ revision và overlap để truy nguyên. |
| jackhhao/jailbreak-classification | Không nhập nguyên gói vào v5; không thêm phần JB từ nguồn này | [HF card](https://huggingface.co/datasets/jackhhao/jailbreak-classification) mô tả bộ nhị phân benign/jailbreak, không có nhãn PI, và lineage jailbreak từ Verazuo. Audit local cho thấy 15.064/15.064 prompt Verazuo duy nhất đã trùng TrustAIRLab, nên phần JB không tạo thêm nguồn độc lập. Card nêu OpenOrca/GPTeacher là nguồn benign nhưng các dòng benign chưa được audit overlap từng mẫu; không kết luận toàn bộ gói HF bị trùng. Audit candidate đã ghi nhận jackhhao như component trong aggregate PromptSentinel/ShieldLM; hai aggregate này vẫn ngoài v5. |
| PromptSentinel | Không dùng aggregate; đề xuất tách theo `source_dataset` | Không có paper riêng cho aggregate; 61.781 train rows có license unspecified. Giữ `all_sources`, chỉ xét component sau khi xác minh paper, license, nhãn và context. |
| ShieldLM | Không dùng aggregate; đề xuất phân rã theo `source` | Paper của component không chứng minh aggregate; license/context giữa card và nguồn trực tiếp còn khác biệt. |
| SPML | Audit-only | Nhãn phụ thuộc cặp `system_prompt`/`user_prompt`; cần giữ context và xác minh điều khoản. |
| JailbreakDB | Giữ raw ở trạng thái JB candidate | Positive là JB candidate theo paper, không có PI riêng; còn conflict và overlap theo `user_prompt`. Chưa nhập v5. |
| JailBreakV-28K, WUSTL, WhatFeatures | Dùng theo quota JB trong bảng trên | JailBreakV chỉ nhận các format text được nêu ở Mục 2.2; nguồn và revision chi tiết ở README từng folder. |

Đề xuất giảm payload `verazuo` là xóa bốn CSV sau khi lưu commit, hash, các nhóm khác nhãn và audit overlap. Đây mới là đề xuất; folder raw chưa bị xóa. Chi tiết thành phần có paper, license và candidate counts xem [audit nguồn ba nhãn](project_training/audit/three_label_candidate_audit.json), [audit overlap](project_training/audit/cross_dataset_overlap.md), [nghiên cứu nguồn JB](project_training/audit/jb_dataset_research.md) và [source index](source_datasets/README.md).

### Holdout benign/FPR

Chưa tạo file holdout benign/FPR độc lập ngoài v5. Split test nội bộ có 3.034 mẫu benign nhưng vẫn thuộc corpus v5. Pool còn 7.376 benign; cần gom và kiểm tra prompt cùng họ trước khi dành mẫu ngoài corpus, để near-duplicate không rơi vào cả tập train và holdout. Sau bước đó có thể dành 2.500–3.000 benign để ước lượng FPR; báo cáo FPR cần kèm khoảng tin cậy. Trong bài toán ba nhãn, FPR = (benign dự đoán PI + benign dự đoán JB) / tổng mẫu benign trong tập đánh giá. Tham khảo [StratifiedGroupKFold](https://scikit-learn.org/stable/modules/cross_validation.html?highlight=cross_validate) và [NIST TN 2119](https://nvlpubs.nist.gov/nistpubs/TechnicalNotes/NIST.TN.2119.pdf).

### Kiểm toán và giới hạn

- `label_conflicts.jsonl` lưu hash/provenance của 4.656 bản ghi xung đột; không lưu prompt thô.
- Exact dedup chuẩn hóa Unicode NFKC, casefold và whitespace. Semantic near-duplicate chưa được phát hiện tự động.
- Chỉ dùng PromptScreen train; các benchmark giữ ngoài corpus. Dataset là corpus nội bộ ứng viên, chưa khẳng định quyền phát hành hoặc khả năng tổng quát hóa qua nguồn.
- Mọi thay đổi số lượng, file và hash ghi trong [version log](project_training/DATASET_VERSION_LOG.md).

## 6. Phạm vi và giới hạn diễn giải

Thống kê trong báo cáo là số bản ghi raw hoặc số dòng corpus theo đúng bảng, không đồng nghĩa số prompt độc lập. Nhãn PI/JB/Benign là mapping theo chính sách của đồ án, không phải taxonomy chung cho mọi paper. Corpus v5 đã có split group-aware train/validation/test nội bộ; chưa có kết quả mô hình hoặc holdout benign/FPR độc lập ngoài v5, và còn các vấn đề provenance/license/near-duplicate được nêu ở trên.
