# Nghiên cứu bổ sung nguồn dữ liệu Jailbreak (JB)

## Phạm vi

Tìm nguồn có paper, file tải được, provenance và định nghĩa mẫu đủ rõ để xem xét gán nhãn JB cho detector văn bản. Bảng overlap dùng corpus v2 lịch sử làm mốc; corpus v3/v4 là lịch sử, còn v5 hiện hành lấy mẫu theo source strata và có split nội bộ. Raw snapshots vẫn được giữ nguyên trong từng thư mục nguồn riêng.

## Nguồn mới đã tải và kiểm tra

| Nguồn | Paper / loại nguồn | Dòng phù hợp | Duy nhất sau exact dedup | Overlap với base v2 | Quota/provenance trong corpus v5 | Nhận xét |
|---|---|---:|---:|---:|---:|---|
| JailBreakV-28K | COLM 2024, benchmark text và multimodal | 20.000 văn bản; bỏ 8.000 dòng ảnh/format khác | 5.000 | 0 | 2.809 primary JB | Chỉ dùng trường jailbreak_query với Template, Persuade, Logic. 15.000 dòng là lặp exact sau chuẩn hóa. Không dùng RedTeam_2K hoặc redteam_query vì đó là harmful-request seeds. |
| What Features in Prompts Jailbreak LLMs? | BlackboxNLP/ACL 2025; 35 phương pháp trên 300 seed | 10.800 attack attempts | 9.884 | 0 | 2.809 primary JB | Trường jailbreak_prompt_text là payload. Không dùng original_prompt_text làm JB. File không có nhãn thành công/thất bại; JB ở đây nghĩa là ý đồ tấn công. |
| WUSTL-CSPL/LLMJailbreak | USENIX Security 2024; prompt thu thập từ thực tế | 448 | 447 | 180, trong đó 2 conflict nhãn với base lịch sử | 437 WUSTL memberships; combined stratum quota 1.573 | 178 khớp JB đã có và gộp provenance; các prompt khớp cùng nhãn vẫn giữ nguồn gốc. |
| verazuo/jailbreak_llms | CCS 2024; bản GitHub gốc của TrustAIRLab | 21.527 dòng trên 4 snapshot; 2.071 dòng jailbreak | 15.064 | 15.064 trùng bộ TrustAIRLab đủ 4 snapshot | 0 | 100% exact-normalized overlap với TrustAIRLab; có 43 nhóm nhãn khác nhau giữa các bản snapshot; không phải nguồn độc lập. |
| youbin2014/JailbreakDB | SoK arXiv:2510.15476; HF README nói accepted IEEE S&P 2027 (to appear) | 1.539.874 | 1.528.462 `user_prompt` | 15.064 trùng bộ TrustAIRLab đủ 4 snapshot | 0 | Paper mô tả positive là jailbreak system–user pairs, nên 445.752 positive là JB candidate; không có class PI. `regular` là Benign candidate. 14 nhóm user prompt có cả hai nhãn cần adjudicate. Số dòng local không khớp mô tả xấp xỉ trên card. |

Mỗi nguồn có README provenance và source_manifest.json tại thư mục riêng trong source_datasets/. Xem [audit định lượng](additional_jb_sources.md) và [JSON audit](additional_jb_sources.json). Audit chỉ đếm exact match theo Unicode NFKC, casefold và gộp whitespace; không nhận diện paraphrase hay gần trùng ngữ nghĩa.

## Vì sao JB trong corpus v2 lịch sử quá ít

Repo [verazuo/jailbreak_llms](https://github.com/verazuo/jailbreak_llms) là nguồn CCS 2024 đã đi vào pool cơ sở qua bản Hugging Face `TrustAIRLab/in-the-wild-jailbreak-prompts`. Đã lưu thêm snapshot GitHub gốc ở revision `4f4031bf8be187f4478c7f94f42b08714722c12e` để tham khảo provenance. Audit exact-normalized xác nhận 15.064 prompt duy nhất của GitHub trùng toàn bộ với TrustAIRLab (100% coverage); có 43 nhóm prompt khác nhãn giữa các snapshot theo thời điểm. Đây không phải nguồn độc lập và không làm tăng số mẫu; dùng bản GitHub để kiểm tra lineage/revision.

Manifest của pool cơ sở lịch sử ghi nhận đủ 1.405 dòng từ cấu hình `jailbreak_2023_12_25` và 13.735 dòng từ `regular_2023_12_25`. Sau gộp trùng và cách ly xung đột, pool v2 còn 1.314 mẫu JB. Corpus v3 đã thêm các nguồn JB có paper; corpus v4 tiếp tục gộp PromptScreen từ file train và lấy mẫu đều theo nguồn. Không nối riêng file GitHub `JB` lần nữa vì đó là cùng nguồn đã dùng qua Hugging Face.

Một số nguồn khác được gọi chung là “jailbreak dataset” lại chứa harmful goal/query, prompt-response evaluation hoặc nội dung multimodal; tên bộ không đủ để ánh xạ mọi dòng sang JB.

## Trùng lặp với các snapshot nguồn cũ

Báo cáo [cross_dataset_overlap.md](cross_dataset_overlap.md) so sánh 10 snapshot theo mapping ba nhãn và báo JailbreakDB riêng. SoK hỗ trợ mapping positive của JailbreakDB thành JB candidate, nhưng audit này chưa chạy phân tích conflict theo system context và do đó chưa nhập nguồn vào corpus. GitHub verazuo trùng 15.064 prompt chuẩn hóa với TrustAIRLab (100% hai chiều), nhưng 43 nhóm prompt khác nhãn giữa các snapshot. JailbreakDB trùng `user_prompt` với TrustAIRLab 15.064 dòng, PromptSentinel 14.348, PromptScreen 6.457 và ShieldLM 5.618; các regular prompt có khác nhãn nguồn cần rà soát, không tự kết luận sai nhãn.

Các con số này phân biệt độ mới của nguồn với độ mới so với một corpus cụ thể: WUSTL chỉ thêm 267 prompt so với v2, dù kho tổng hợp ShieldLM/PromptScreen có nhiều prompt trùng hoặc gán nhãn khác. V5 dùng PromptScreen như source stratum sau khi loại conflict chính xác; paper v1 là preprint và license/provenance theo dòng còn mở. Không dùng các bộ tổng hợp khác nếu chưa xử lý xung đột nhãn và lineage.

## Pool sau gộp và corpus cân bằng hiện hành

Ở v3, ba nguồn JB mới có 15.331 prompt duy nhất sau gộp trùng giữa nguồn. Trong số này, 178 đã có cùng nhãn JB trong v2, 2 khớp prompt nhưng xung đột nhãn cần quarantine, và 15.151 là JB mới chưa xuất hiện trong v2. Đây là số liệu lịch sử trước khi gộp PromptScreen vào v4.

| Trạng thái | benign | PI | JB | Tổng | Lớp lớn nhất / nhỏ nhất |
|---|---:|---:|---:|---:|---:|
| Pool tự nhiên sau gộp/dedup v3, trước cân bằng | 22.578 | 9.329 | 16.465 | 48.372 | 2,42:1 |
| Corpus v3 (superseded) | 9.329 | 9.329 | 9.329 | 27.987 | 1:1 |
| Pool tự nhiên v4 sau conflict filtering | 27.376 | 11.282 | 28.593 | 67.251 | 2,53:1 |
| Corpus v4 (superseded) | 3.906 | 3.906 | 3.906 | 11.718 | 1:1 |
| Corpus v5 hiện hành | 20.000 | 10.000 | 10.000 | 40.000 | 2:1:1 |

Corpus v5 lấy mẫu không hoàn lại theo tỷ lệ 2:1:1 và quota capped-equal theo source strata: benign 6.667/6.667/6.666; PI 1.953 PromptScreen + 8.047 PromptShield; JB 2.809 JailBreakV-28K, 2.809 PromptScreen, 1.573 TrustAIRLab+WUSTL và 2.809 WhatFeatures. PI vẫn lệch nguồn 19,5%/80,5%. PromptScreen chỉ dùng file source train; file reported-test giữ ngoài corpus. Các file và hash được ghi trong [manifest](../manifest.json), [split manifest](../splits/split_manifest.json) và [version log](../DATASET_VERSION_LOG.md). Split v5 là phân hoạch nội bộ group-aware; chưa có holdout benign độc lập bên ngoài v5. Metadata base prompt và attack method được giữ để báo metric theo nhóm và nguồn.

## Nguồn đã rà soát nhưng chưa đưa vào số liệu

- WildJailbreak: NeurIPS 2024 công bố 262.000 prompt-response pairs, gồm vanilla harmful, adversarial harmful và benign. Hugging Face yêu cầu đồng ý chia sẻ thông tin liên hệ; yêu cầu truy cập trước đó bị từ chối. Folder tham chiếu local đã xóa ngày 2026-10-08 vì không chứa payload; giữ paper/card URLs ở `urldata.md`. Nếu được cấp quyền sau này, chỉ map rõ adversarial harmful sang JB; vanilla harmful không tự động là JB.
- MHJ: 2.912 lượt prompt trong 537 hội thoại jailbreak nhiều lượt, giấy phép CC BY-NC 4.0 nhưng Hugging Face cũng yêu cầu chia sẻ thông tin liên hệ. Cấu trúc đa lượt không tương đương input một lượt của corpus hiện tại; chưa tải.
- JailbreakDB: đã tải raw snapshot tại revision `63912b8f9e66e87d8fdffde340391b79503c8e0d` vào thư mục riêng. Python CSV và DuckDB cùng đếm được 445.752 record `jailbreak=1` và 1.094.122 record `jailbreak=0` (regular); 1.528.462 user prompt duy nhất sau exact-normalized và 14 nhóm xuất hiện dưới cả hai nhãn gốc. Card ghi xấp xỉ 6,6M/5,7M; số này gần khớp newline vật lý (6.565.678/5.651.873), không phải CSV record count do prompt có newline nội bộ; SHA-256 của hai file khớp revision. Paper [SoK: Taxonomy and Evaluation of Prompt Security in Large Language Models](https://arxiv.org/abs/2510.15476) có bản arXiv công khai; README HF hiện nói bài được nhận tại IEEE S&P 2027 “to appear”, nhưng proceedings là sự kiện tương lai ở ngày audit 2026-10-07. Paper mô tả positive là jailbreak system–user pairs, vì vậy mapping hợp lý là JB candidate, không phải PI; 14 nhóm prompt conflict và overlap vẫn phải lọc trước khi dùng. Exact overlap theo `user_prompt` gồm 15.064 với TrustAIRLab, 14.348 với PromptSentinel, 6.457 với PromptScreen và 5.618 với ShieldLM; xem bảng đầy đủ trong [cross_dataset_overlap.md](cross_dataset_overlap.md). Nguồn vẫn ngoài corpus.
- JailbreakBench artifacts: paper benchmark NeurIPS 2024 và kho attack artifacts riêng có MIT. Đây là prompt tấn công thực, khác với JBB-Behaviors vốn là behavior seeds. Lệnh tải snapshot bị command review chặn trước khi thực thi; thư mục đích đã xác minh không tồn tại. Theo quy tắc workspace, không thử lại qua đường khác nên nguồn này chưa nằm trong audit cục bộ.

## Lưu ý sử dụng corpus

Các nguồn JB hiện có đã được dùng theo quota trong manifest. Split v5 hiện chia nhóm prompt-family thành train/validation/test; phải chọn checkpoint/ngưỡng trên train/validation theo vai trò đã định và chỉ dùng test cho đánh giá cuối. Split không xác nhận quyền dữ liệu, adjudicate lại nhãn nguồn hay tạo holdout benign độc lập.

Không dùng các prompt mới làm bằng chứng đánh giá độc lập nếu chúng đã được đưa vào train. Không tự gán harmful request thành JB chỉ vì nó xuất hiện trong paper về jailbreak. Mọi nhãn JB trong nguồn mới là mapping theo định nghĩa detector “ý đồ tấn công”, không phải khẳng định mọi attack đều thành công.

## Nguồn chính

- [JailBreakV-28K dataset card](https://huggingface.co/datasets/JailbreakV-28K/JailBreakV-28k) và [paper](https://arxiv.org/abs/2404.03027).
- [WUSTL-CSPL/LLMJailbreak](https://github.com/WUSTL-CSPL/LLMJailbreak) và [paper USENIX Security 2024](https://www.usenix.org/conference/usenixsecurity24/presentation/yu-zhiyuan).
- [What Features paper, ACL Anthology 2025](https://aclanthology.org/2025.blackboxnlp-1.28/) và [dataset card](https://huggingface.co/datasets/sevdeawesome/jailbreak_success).
- [WildJailbreak NeurIPS 2024 paper](https://proceedings.neurips.cc/paper_files/paper/2024/hash/54024fca0cef9911be36319e622cde38-Abstract-Conference.html) và [access gate](https://huggingface.co/datasets/allenai/wildjailbreak).
- [MHJ card and access conditions](https://huggingface.co/datasets/ScaleAI/mhj).
- [JailbreakDB card](https://huggingface.co/datasets/youbin2014/JailbreakDB) and cited [arXiv paper](https://arxiv.org/abs/2510.15476).
- [JailbreakBench artifacts repository](https://github.com/JailbreakBench/artifacts) and [NeurIPS 2024 paper](https://arxiv.org/abs/2404.01318).

The existing `shieldlm/paper/` folder currently contains a provenance README but no PDF paper dedicated to that dataset; keep ShieldLM audit-only until a suitable source paper and component-level license lineage are established.
