# Source datasets

Thư mục này lưu các snapshot có payload tại máy. Nguồn chỉ có paper/card nhưng chưa có payload được ghi dạng tham chiếu ngoài máy, không tạo folder giả.

| Bộ nguồn | Nguồn/paper | README cục bộ | Vai trò hiện tại |
|---|---|---|---|
| jailbreak_features_blackboxnlp2025 | [ACL Anthology 2025](https://aclanthology.org/2025.blackboxnlp-1.28/) | [README](jailbreak_features_blackboxnlp2025/README.md) | JB primary source stratum: 2.809 dòng trong corpus v5 |
| jailbreakv28k_colm2024 | [COLM 2024 paper](https://arxiv.org/abs/2404.03027) | [README](jailbreakv28k_colm2024/README.md) | JB primary source stratum: 2.809 dòng trong corpus v5 |
| prompt_sentinel | [Hugging Face dataset](https://huggingface.co/datasets/nuhmanpk/prompt-sentinel) | [README](prompt_sentinel/README.md) | Không dùng nguyên aggregate; đề xuất tách theo `source_dataset`, giữ `all_sources`; 61.781 train rows license unspecified; papered components cần audit riêng |
| promptscreen_raw | [Repository](https://github.com/dronefreak/PromptScreen), [arXiv v1](https://arxiv.org/abs/2512.19011v1) | [README](promptscreen_raw/README.md) | Nguồn có ba nhãn; quota v5: 6.667 benign, 1.953 PI, 2.809 JB; paper/license và provenance theo dòng còn caveat |
| promptshield_hendzh | [PromptShield dataset](https://huggingface.co/datasets/hendzh/PromptShield), [CODASPY 2025](https://doi.org/10.1145/3714393.3726501) | [README](promptshield_hendzh/README.md) | Nguồn nhị phân: `1 → PI`, `0 → benign` theo card; v5 lấy 8.047 PI và 6.667 benign-mapped; nhãn 0 chưa adjudicate với JB |
| shieldlm | [Hugging Face dataset](https://huggingface.co/datasets/Abdennebi/shieldlm-prompt-injection) | [README](shieldlm/README.md) | Không dùng aggregate; đề xuất phân rã theo `source`, kiểm paper/license thành phần, sau đó xóa payload aggregate nếu các component được đóng gói và audit |
| spml_prompt_injection | [SPML paper](https://arxiv.org/abs/2402.11755) | [README](spml_prompt_injection/README.md) | Prompt injection; audit-only |
| trustairlab_in_the_wild_jailbreak_prompts | [CCS 2024 paper](https://arxiv.org/abs/2308.03825), upstream [verazuo/jailbreak_llms](https://github.com/verazuo/jailbreak_llms) | [README](trustairlab_in_the_wild_jailbreak_prompts/README.md) | v5: 6.666 benign primary quota; JB nằm trong stratum gộp TrustAIRLab+WUSTL 1.573 mẫu |
| verazuo_jailbreak_llms | [GitHub snapshot](https://github.com/verazuo/jailbreak_llms), [CCS 2024 paper](https://doi.org/10.1145/3658644.3670388) | [README](verazuo_jailbreak_llms/README.md) | Đề xuất xóa 4 CSV payload sau khi lưu revision/hash/conflict report; 15.064/15.064 prompt unique trùng TrustAIRLab; chưa xóa |
| youbin2014_jailbreakdb | [Hugging Face dataset](https://huggingface.co/datasets/youbin2014/JailbreakDB), [SoK paper](https://arxiv.org/abs/2510.15476) | [README](youbin2014_jailbreakdb/README.md) | 445.752 positive là JB candidate theo paper, 1.094.122 regular là Benign candidate; ngoài corpus v5 đến khi xử lý context/conflict/overlap |
| allenai/wildjailbreak *(không có folder local)* | [NeurIPS 2024 paper](https://proceedings.neurips.cc/paper_files/paper/2024/hash/54024fca0cef9911be36319e622cde38-Abstract-Conference.html), [HF access gate](https://huggingface.co/datasets/allenai/wildjailbreak) | — | Chỉ tham chiếu; không có payload local; folder metadata/paper đã xóa 2026-10-08 |
| wustl_llm_jailbreak_usenix2024 | [USENIX Security 2024 paper](https://www.usenix.org/conference/usenixsecurity24/presentation/yu-zhiyuan) | [README](wustl_llm_jailbreak_usenix2024/README.md) | JB source membership trong stratum TrustAIRLab+WUSTL v5: 437 dòng; quota gộp 1.573 |

## Báo cáo liên quan

- [Audit số lượng nhãn/split và snapshot ứng viên](../project_training/audit/three_label_candidate_audit.json)
- [Overlap giữa các nguồn](../project_training/audit/cross_dataset_overlap.md)
- [Nghiên cứu nguồn JB bổ sung](../project_training/audit/jb_dataset_research.md)
- [Lịch sử phiên bản dữ liệu](../project_training/DATASET_VERSION_LOG.md)

Tên nguồn và paper chỉ mô tả provenance; không có nghĩa mọi dòng trong một bộ đều tương đương nhãn PI/JB của đồ án. Corpus v5 là bản ứng viên tỷ lệ 2:1:1; split nội bộ đã có nhưng không thay thế việc adjudicate nhãn hoặc tạo holdout độc lập. PromptScreen vẫn có vấn đề license/provenance theo dòng. Xem README từng nguồn, manifest và audit trước khi dùng để huấn luyện chính thức hoặc chia sẻ.
