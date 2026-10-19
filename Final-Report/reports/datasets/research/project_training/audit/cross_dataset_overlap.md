# Báo cáo trùng lặp và tổng kết các snapshot dataset

Tạo lúc `2026-10-07T15:30:51.942759+00:00`. Báo cáo chỉ dùng thống kê, hash file và nhãn; không ghi prompt gốc hoặc hash từng prompt.

## Phạm vi và cách so sánh

Audit chuẩn hóa label map của 10 snapshot để so sánh: PromptShield, TrustAIRLab, bản GitHub verazuo/jailbreak_llms, SPML, PromptScreen, PromptSentinel, ShieldLM, JailBreakV-28K, WUSTL LLMJailbreak và WhatFeatures. JailbreakDB được audit riêng, không tham gia ma trận pairwise này. Follow-up đọc paper SoK hỗ trợ xem positive là JB candidate (không phải PI); tuy nhiên conflict và overlap vẫn chưa được xử lý để nhập corpus. WildJailbreak/MHJ không có dữ liệu đã tải; Qualifire và OR-Bench là benchmark giữ riêng, không nhập vào corpus train.

Một prompt được xem là trùng khi giống sau chuẩn hóa Unicode NFKC, chuyển chữ thường, và gộp whitespace. Đây là exact normalized match; audit không đo paraphrase hoặc gần trùng ngữ nghĩa. PromptSentinel và ShieldLM là bộ tổng hợp nên overlap với nguồn thành phần là điều dự kiến, không phải các nguồn độc lập.

Label map audit: PromptShield 0=benign/1=PI; TrustAIRLab and VerazuoGitHub false=benign/true=JB; SPML 0=benign/1=PI on User Prompt; PromptScreen benign/prompt-injection/jailbreak=benign/PI/JB; PromptSentinel benign/injection/jailbreak=benign/PI/JB; ShieldLM benign/direct_injection/indirect_injection/jailbreak=benign/PI/PI/JB; JailBreakV text formats=JB; WUSTL Prompt column=JB; WhatFeatures jailbreak_prompt_text=JB. Seed harmful requests are excluded. These maps normalize source tasks and do not overwrite native labels.

## Tổng kết từng snapshot

| Snapshot | Dòng raw | Dòng dùng | Prompt duy nhất | Lặp thêm | Bỏ qua | benign / PI / JB |
|---|---:|---:|---:|---:|---:|---:|
| PromptShield | 43,425 | 43,425 | 43,115 | 310 | 0 | 26,984 / 16,441 / 0 |
| TrustAIRLab | 21,527 | 21,527 | 15,064 | 6,463 | 0 | 19,456 / 0 / 2,071 |
| VerazuoGitHub | 21,527 | 21,527 | 15,064 | 6,463 | 0 | 19,456 / 0 / 2,071 |
| SPML | 16,012 | 16,011 | 15,913 | 98 | 1 | 3,470 / 12,541 / 0 |
| PromptScreen | 30,937 | 30,937 | 30,829 | 108 | 0 | 10,136 / 2,100 / 18,701 |
| PromptSentinel | 145,781 | 145,781 | 145,781 | 0 | 0 | 82,458 / 62,059 / 1,264 |
| ShieldLM | 54,162 | 54,162 | 54,153 | 9 | 0 | 35,197 / 17,947 / 1,018 |
| JailBreakV-28K | 28,000 | 20,000 | 5,000 | 15,000 | 8,000 | 0 / 0 / 20,000 |
| WUSTL_LLMJailbreak | 448 | 448 | 447 | 1 | 0 | 0 / 0 / 448 |
| WhatFeatures | 10,800 | 10,800 | 9,884 | 916 | 0 | 0 / 0 / 10,800 |

## Overlap giữa từng cặp snapshot

`Shared` là số prompt chuẩn hóa duy nhất xuất hiện ở cả hai snapshot. Tỉ lệ A/B tính trên số prompt duy nhất của từng snapshot; disagreement đếm nhóm prompt mà hai nguồn gán nhãn khác nhau sau mapping ba nhãn. Khác nhãn cho thấy taxonomy/mapping không tương thích tại prompt đó; không tự kết luận nhãn nguồn sai.

| Nguồn A | Nguồn B | Shared | A khớp | B khớp | Jaccard | Khác nhãn |
|---|---|---:|---:|---:|---:|---:|
| PromptSentinel | ShieldLM | 17,377 | 11.92% | 32.09% | 9.52% | 104 |
| SPML | ShieldLM | 15,913 | 100.00% | 29.39% | 29.39% | 0 |
| SPML | PromptSentinel | 15,909 | 99.97% | 10.91% | 10.91% | 0 |
| TrustAIRLab | VerazuoGitHub | 15,064 | 100.00% | 100.00% | 100.00% | 43 |
| TrustAIRLab | PromptSentinel | 13,387 | 88.87% | 9.18% | 9.08% | 11 |
| VerazuoGitHub | PromptSentinel | 13,387 | 88.87% | 9.18% | 9.08% | 11 |
| TrustAIRLab | PromptScreen | 6,111 | 40.57% | 19.82% | 15.36% | 5,482 |
| VerazuoGitHub | PromptScreen | 6,111 | 40.57% | 19.82% | 15.36% | 5,482 |
| PromptScreen | PromptSentinel | 5,887 | 19.10% | 4.04% | 3.45% | 5,111 |
| PromptScreen | ShieldLM | 1,718 | 5.57% | 3.17% | 2.06% | 546 |
| TrustAIRLab | ShieldLM | 1,544 | 10.25% | 2.85% | 2.28% | 444 |
| VerazuoGitHub | ShieldLM | 1,544 | 10.25% | 2.85% | 2.28% | 444 |
| PromptShield | PromptScreen | 1,432 | 3.32% | 4.64% | 1.97% | 4 |
| PromptShield | ShieldLM | 458 | 1.06% | 0.85% | 0.47% | 1 |
| TrustAIRLab | WUSTL_LLMJailbreak | 206 | 1.37% | 46.09% | 1.35% | 10 |
| VerazuoGitHub | WUSTL_LLMJailbreak | 206 | 1.37% | 46.09% | 1.35% | 10 |
| ShieldLM | WUSTL_LLMJailbreak | 205 | 0.38% | 45.86% | 0.38% | 136 |
| PromptScreen | WUSTL_LLMJailbreak | 203 | 0.66% | 45.41% | 0.65% | 0 |
| PromptShield | PromptSentinel | 57 | 0.13% | 0.04% | 0.03% | 0 |
| PromptSentinel | WUSTL_LLMJailbreak | 39 | 0.03% | 8.72% | 0.03% | 1 |
| PromptShield | TrustAIRLab | 6 | 0.01% | 0.04% | 0.01% | 1 |
| PromptShield | VerazuoGitHub | 6 | 0.01% | 0.04% | 0.01% | 1 |
| JailBreakV-28K | WUSTL_LLMJailbreak | 0 | 0.00% | 0.00% | 0.00% | 0 |
| JailBreakV-28K | WhatFeatures | 0 | 0.00% | 0.00% | 0.00% | 0 |
| PromptScreen | JailBreakV-28K | 0 | 0.00% | 0.00% | 0.00% | 0 |
| PromptScreen | WhatFeatures | 0 | 0.00% | 0.00% | 0.00% | 0 |
| PromptSentinel | JailBreakV-28K | 0 | 0.00% | 0.00% | 0.00% | 0 |
| PromptSentinel | WhatFeatures | 0 | 0.00% | 0.00% | 0.00% | 0 |
| PromptShield | JailBreakV-28K | 0 | 0.00% | 0.00% | 0.00% | 0 |
| PromptShield | SPML | 0 | 0.00% | 0.00% | 0.00% | 0 |
| PromptShield | WUSTL_LLMJailbreak | 0 | 0.00% | 0.00% | 0.00% | 0 |
| PromptShield | WhatFeatures | 0 | 0.00% | 0.00% | 0.00% | 0 |
| SPML | JailBreakV-28K | 0 | 0.00% | 0.00% | 0.00% | 0 |
| SPML | PromptScreen | 0 | 0.00% | 0.00% | 0.00% | 0 |
| SPML | WUSTL_LLMJailbreak | 0 | 0.00% | 0.00% | 0.00% | 0 |
| SPML | WhatFeatures | 0 | 0.00% | 0.00% | 0.00% | 0 |
| ShieldLM | JailBreakV-28K | 0 | 0.00% | 0.00% | 0.00% | 0 |
| ShieldLM | WhatFeatures | 0 | 0.00% | 0.00% | 0.00% | 0 |
| TrustAIRLab | JailBreakV-28K | 0 | 0.00% | 0.00% | 0.00% | 0 |
| TrustAIRLab | SPML | 0 | 0.00% | 0.00% | 0.00% | 0 |
| TrustAIRLab | WhatFeatures | 0 | 0.00% | 0.00% | 0.00% | 0 |
| VerazuoGitHub | JailBreakV-28K | 0 | 0.00% | 0.00% | 0.00% | 0 |
| VerazuoGitHub | SPML | 0 | 0.00% | 0.00% | 0.00% | 0 |
| VerazuoGitHub | WhatFeatures | 0 | 0.00% | 0.00% | 0.00% | 0 |
| WUSTL_LLMJailbreak | WhatFeatures | 0 | 0.00% | 0.00% | 0.00% | 0 |

## JailbreakDB: giữ nguyên nhãn gốc và overlap theo user prompt

`jailbreak=1` được giữ là `ambiguous_attack` do card gộp jailbreak và adversarial; không ép thành nhãn JB. Overlap chuẩn hóa chỉ so `user_prompt`; `system_prompt` vẫn được giữ trong raw snapshot nhưng không nằm trong khóa so sánh. `regular_prompts_with_nonbenign_source_label` là trường hợp cần rà soát, không tự kết luận sai nhãn.

Tổng 1,539,874 CSV records; 1,528,462 user prompt duy nhất sau NFKC/casefold/gộp whitespace; 11,412 record lặp theo khóa này. Nhãn gốc: benign=1,094,122, jailbreak/adversarial chưa phân giải=445,752; 14 nhóm user prompt xuất hiện dưới cả hai nhãn gốc. Newline vật lý: regular=5,651,873, attack=6,565,678; nhiều prompt có newline trong trường quote nên physical line count không bằng CSV record count.

| Snapshot cũ | Shared user prompts | JailbreakDB khớp | Snapshot cũ khớp | Regular gốc gặp nhãn khác benign |
|---|---:|---:|---:|---:|
| TrustAIRLab | 15,064 | 0.99% | 100.00% | 10 |
| VerazuoGitHub | 15,064 | 0.99% | 100.00% | 10 |
| PromptSentinel | 14,348 | 0.94% | 9.84% | 1 |
| PromptScreen | 6,457 | 0.42% | 20.94% | 5,467 |
| ShieldLM | 5,618 | 0.37% | 10.37% | 13 |
| PromptShield | 3,953 | 0.26% | 9.17% | 0 |
| WUSTL_LLMJailbreak | 445 | 0.03% | 99.55% | 3 |
| WhatFeatures | 3 | 0.00% | 0.03% | 0 |
| SPML | 2 | 0.00% | 0.01% | 0 |
| JailBreakV-28K | 1 | 0.00% | 0.02% | 0 |

## Pool nguồn cơ sở trước khi thêm các nguồn JB

| Chỉ số | Giá trị |
|---|---:|
| Dòng đầu vào (PromptShield train + TrustAIRLab config 2023-12-25) | 34,049 |
| Nhóm prompt chuẩn hóa duy nhất | 33,263 |
| Dòng lặp cùng nhãn có thể gộp | 713 |
| Nhóm nhãn xung đột bị loại | 42 (115 dòng) |
| Dòng duy nhất còn lại | 33,221 |

| Nhãn còn lại | Số prompt | Tỉ lệ |
|---|---:|---:|
| benign | 22,578 | 67.96% |
| PI | 9,329 | 28.08% |
| JB | 1,314 | 3.96% |

Pool nguồn cơ sở trước khi thêm các nguồn JB có tỉ lệ lớp lớn nhất/nhỏ nhất **17.18:1**; đây là thống kê lịch sử, không phải phân phối của corpus hiện hành.
Corpus hiện hành được cân bằng nhãn trên một file duy nhất; đây không phải các split train/validation/test.

## Thư mục nguồn và giới hạn sử dụng

- Được dùng cho corpus hiện tại: [PromptShield README](../../source_datasets/promptshield_hendzh/README.md) và [TrustAIRLab README](../../source_datasets/trustairlab_in_the_wild_jailbreak_prompts/README.md). Hai README có URL nguồn, paper/citation, revision và ý nghĩa nhãn.
- [SPML README](../../source_datasets/spml_prompt_injection/README.md): có paper arXiv và nguồn URL; chỉ audit vì card gốc không khuyến nghị dùng corpus này để train detector, đồng thời mỗi dòng có cả System Prompt và User Prompt.
- [PromptScreen README](../../source_datasets/promptscreen_raw/README.md): v4 sử dụng `metrics_train_set.json` làm source stratum; reported-test không vào corpus. Paper là arXiv preprint, license/provenance theo prompt còn chưa xác minh.
- [PromptSentinel README](../../source_datasets/prompt_sentinel/README.md): JB chỉ 1.019/116.854 dòng train; 61.781 dòng train license unspecified, gated và không có paper riêng cho bộ tổng hợp. Giữ audit-only; không đưa vào v4.
- [ShieldLM README](../../source_datasets/shieldlm/README.md): bộ tổng hợp không có paper peer-reviewed riêng theo hồ sơ hiện có; thư mục paper/ chỉ chứa README, chưa có PDF. License nguồn thành phần cần rà soát nên vẫn audit-only.
- WildJailbreak: [NeurIPS paper](https://proceedings.neurips.cc/paper_files/paper/2024/hash/54024fca0cef9911be36319e622cde38-Abstract-Conference.html), [HF access gate](https://huggingface.co/datasets/allenai/wildjailbreak); không có payload local, folder tham chiếu đã xóa 2026-10-08. Không có dòng nào được audit.
- Các nguồn JB JailBreakV-28K, WUSTL LLMJailbreak và WhatFeatures được lưu raw riêng và có mẫu trong corpus cân bằng; xem README từng nguồn và [báo cáo nghiên cứu](jb_dataset_research.md).
- Corpus hiện hành: balanced_three_label.jsonl (corpus nguồn; payload không có trong report package), cùng [manifest](../manifest.json) và [version log](../DATASET_VERSION_LOG.md). Snapshot raw vẫn nằm riêng trong source_datasets/.

### Cập nhật kho nguồn — 2026-10-08

Đã xóa folder `source_datasets/wildjailbreak_allenai/` theo yêu cầu. Folder chỉ chứa README, cache và PDF paper, không có payload; URL card và paper vẫn được ghi trong `urldata.md`. Tổng số dòng dữ liệu tải về không đổi. PromptSentinel vẫn là audit-only: JB ít là một hạn chế, nhưng lý do không dùng còn gồm gated access, license chưa rõ và thiếu paper riêng cho bộ tổng hợp.
## Tái tạo audit

Từ repository root: `uv run --no-project --with duckdb python workspaces/truongnv/training_bases/datasets/project_training/tools/audit_cross_dataset_overlap.py`.

Chạy builder và verifier riêng để tái tạo corpus; audit overlap không tải thêm dữ liệu và không huấn luyện mô hình.

## Corpus hiện hành — v5.0.0

balanced_three_label.jsonl có 40.000 dòng: 20.000 benign, 10.000 PI và 10.000 JB. Pool sau exact dedup và conflict filtering có 67.251 dòng: benign 27.376, PI 11.282, JB 28.593. Split group-aware nội bộ đã được đóng băng tại [split manifest](../splits/split_manifest.json): train 28.280, validation 5.858, test 5.862; chưa có holdout benign/FPR độc lập ngoài v5.

| Nhãn | Source stratum | Số prompt | Tỷ lệ nhãn |
|---|---|---:|---:|
| benign | PromptScreen | 6.667 | 33,34% |
| benign | PromptShield | 6.667 | 33,34% |
| benign | TrustAIRLab | 6.666 | 33,33% |
| PI | PromptScreen | 1.953 | 19,53% |
| PI | PromptShield | 8.047 | 80,47% |
| JB | JailBreakV-28K | 2.809 | 28,09% |
| JB | PromptScreen | 2.809 | 28,09% |
| JB | TrustAIRLab + WUSTL | 1.573 | 15,73% |
| JB | WhatFeatures | 2.809 | 28,09% |

Quota dùng capped-equal source-stratified sampling không hoàn lại. PI vẫn lệch nguồn vì PromptScreen chỉ có 1.953 PI; cân bằng nhãn không loại bỏ khả năng mô hình học dấu hiệu riêng của nguồn. PromptScreen chỉ đóng góp từ `metrics_train_set.json`; file `metrics_test_set.json` được giữ ngoài corpus. PromptScreen là arXiv preprint, chưa có license/provenance theo prompt, nên corpus vẫn là ứng viên nghiên cứu nội bộ.
