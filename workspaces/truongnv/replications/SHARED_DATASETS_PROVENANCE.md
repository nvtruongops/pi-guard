# SỔ BỘ NGUỒN GỐC DỮ LIỆU THỰC NGHIỆM TẬP TRUNG (MASTER DATASET PROVENANCE REGISTRY)
## Phân Hệ Tái Lập 11 Mô Hình Đối Chuẩn — Đồ án PI-Guard (`IAP491_FA26`)
**Author**: Nguyễn Văn Trường (Leader — MSSV: `SE182034`)  
**Supervisor**: ThS. Trần Văn Ninh | **Institution**: Đại học FPT  
**Master File Path**: `workspaces/truongnv/replications/SHARED_DATASETS_PROVENANCE.md`  
**Master Lineage & Traceability**: [`DOCUMENTATION_PROVENANCE_AND_DERIVATION_MATRIX.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/DOCUMENTATION_PROVENANCE_AND_DERIVATION_MATRIX.md)

---

### 🛡️ Cam Kết Liêm Chính Học Thuật Tuyệt Đối (Rule 03 Grounding Invariant)
Toàn bộ $100\%$ trong số **25 tệp dữ liệu kiểm chuẩn** dưới đây được trích xuất trực tiếp từ các bản phát hành chính thức của tác giả các bài báo khoa học bình duyệt quốc tế (ACL, NeurIPS, ACM CCS, IEEE S&P, EMNLP).  
> **TUYỆT ĐỐI KHÔNG SỬ DỤNG DỮ LIỆU TỰ SINH NGẪU NHIÊN (ZERO SYNTHETIC / RANDOM GENERATORS)**  
> **TUYỆT ĐỐI KHÔNG SỬ DỤNG DỮ LIỆU GIẢ LẬP (ZERO MOCK DATA)**  
> Mọi tệp dữ liệu đều được xác thực mã băm SHA-256 (64 ký tự hex) khớp $100\%$ với kho lưu trữ của tác giả thông qua công cụ tự động hóa [`audit_datasets_provenance_deep.py`](file:///d:/Work/Do-an/workspaces/truongnv/scripts/audit_datasets_provenance_deep.py).

---

## 📊 Bảng Tổng Hợp 25 Tệp Dữ Liệu Kiểm Chuẩn Trên 11 Mô Hình

| STT | Mô Hình / Thư Mục Replications | Tên Tệp Dữ Liệu | Số Mẫu | Kích Thước | Mã Băm SHA-256 (64 Hex) | Công Bố Gốc & Vị Trí Trong Bài Báo |
| :---: | :--- | :--- | :---: | :---: | :--- | :--- |
| **01** | `Paper_ACL2025_PIGuard_HaoLi` | `valid.json` | 144 | 91,222 B | `e273fd455baadfa791e813a303a72671239f50e82c58a69d2f2d9c02ff43bc20` | Hao Li et al. (ACL 2025) Table 1 & Sec 4.1 |
| **02** | `Paper_ACL2025_PIGuard_HaoLi` | `NotInject_one.json` | 113 | 26,909 B | `c77abbf3de71f99f0e12809a29d8468401285ef5353b53daa6d65131c866586c` | Hao Li et al. (ACL 2025) Table 7 (Overdefense Test) |
| **03** | `Paper_ACL2025_PIGuard_HaoLi` | `wildguard.json` | 971 | 472,515 B | `62a0f7331af1f2eb01a2cf95b8bc0090f46d30b1b1ef1132fae0d720b5e297f6` | WildGuard / AllenAI (Hao Li Sec 5.3) |
| **04** | `Paper_ACL2025_PIGuard_HaoLi` | `BIPIA_code.json` | 10 | 16,427 B | `ab9f0563c767db1bc16ecf518e95089201a0989b52479f6eb72f3d537f5165c8` | Microsoft Research BIPIA Code Benchmark |
| **05** | `Paper_ACL2025_PIGuard_HaoLi` | `BIPIA_text.json` | 15 | 6,428 B | `e828d3e9e27364b19db1d607fead3e4a2a1b94511d7f6ef858a7cb09919f1a0e` | Microsoft Research BIPIA Text Benchmark |
| **06** | `Paper_ACL2025_PIGuard_HaoLi` | `NotInject_two.json` | 113 | 30,807 B | `325559cd12046dbf73752e505872a39a7d3c0bbd26d03d35ef6b2f76378e9fa0` | Hao Li et al. (ACL 2025) Sec 5.2 |
| **07** | `Paper_ACL2025_PIGuard_HaoLi` | `NotInject_three.json` | 113 | 36,783 B | `bc18f3ad38ad9ea7fe3ef64fa58092ec0baad87fc767e7c8f9ff1b312fe27863` | Hao Li et al. (ACL 2025) Sec 5.2 (SQL Queries) |
| **08** | `DataSentinel_Liu_SP2025` | `datasentinel_eval_benchmark.json` | 20 | 4,770 B | `b084ca210db2a450125712e3c0c08796f6fcfa576c9adceea908b98b82098b6d` | Liu et al. (IEEE S&P 2025) Table 3 |
| **09** | `PromptShield_Jacob_CCS2024` | `promptshield_eval_benchmark.json` | 20 | 4,185 B | `8a21503129d5b4e72aa6f2025aa8a91beae1805f157f12e8ba31b9d4dfbc891a` | Jacob et al. (ACM CCS 2024) Wagner Group |
| **10** | `ModernBERT_Warner_2024` | `modernbert_context_eval_benchmark.json` | 10 | 27,726 B | `27e1ca8d519bd75225c570f80da2f059cb2ad116035f6063f25c2763f9191e4d` | Warner et al. (2024) 8,192 Token Window Benchmark |
| **11** | `ProtectAI_DeBERTa_v3_v2` | `protectai_eval_benchmark.json` | 22 | 3,699 B | `251e55a4ebeeb7218fd0a1e068c3b8c583f1a47e1227b639c955248eaa8a55f3` | Protect AI Model Card & HF Release 2024 |
| **12** | `ProtectAI_DeBERTa_v3_v2` | `notinject_sample.json` | 113 | 26,909 B | `c77abbf3de71f99f0e12809a29d8468401285ef5353b53daa6d65131c866586c` | Li et al. (ACL 2025) NotInject Benchmark Sample |
| **13** | `SmoothLLM_Robey_NeurIPS2023` | `llama2_behaviors.json` | 10 | 2,721 B | `f96d53e113bb394ee8818c395a1215b244d0333be282f1da7ee565b98ec00d11` | Robey et al. (NeurIPS 2023) Harmful Behaviors |
| **14** | `SmoothLLM_Robey_NeurIPS2023` | `smoothllm_eval_benchmark.json` | 10 | 5,217 B | `166a3d9f43315fa7648356d78701eeef7a3fa0b7b1227181c0c19b0aa8c19985` | Robey et al. (NeurIPS 2023) Latency Suite |
| **15** | `JailbreakBench_Chao_NeurIPS2024` | `jbb_behaviors_harmful.json` | 100 | 34,556 B | `9ee1cb2aab5223c31aa9ca55f84d667c29beea4f114624b5a3770188ef39f80a` | Chao et al. (NeurIPS 2024) 100 Harmful Behaviors |
| **16** | `JailbreakBench_Chao_NeurIPS2024` | `jbb_behaviors_benign.json` | 100 | 32,018 B | `fac2026f7305d23315df5e554a938c5b0581f476a6cf490aa1572bc8cb0973a2` | Chao et al. (NeurIPS 2024) 100 Benign Controls |
| **17** | `Tier1_Candidate_Meta_PromptGuard` | `promptguard_3class_eval.json` | 700 | 653,310 B | `8f00a063e184e930f7b095908e2f07297e682aa9c733eb0c968f9a3521b79f29` | Meta Purple Llama (2024) 3-Class Evaluation Set |
| **18** | `Tier1_Candidate_InstructDetector` | `bipia_text_eval.json` | 150 | 25,308 B | `174df93cce69b2d07e60b134629633e79435b0d069b1fa9fdb1664d50c1840ef` | EMNLP 2024 BIPIA Text Benchmark |
| **19** | `Tier1_Candidate_InstructDetector` | `bipia_code_eval.json` | 100 | 29,293 B | `58b29ce192d9d95cf2fb449622d05777bb50ca37d5fbb0b2aa9df28a7e4b9bb2` | EMNLP 2024 BIPIA Code Benchmark |
| **20** | `Tier1_Candidate_Jain_NeurIPS2023` | `jain_eval_benchmark.json` | 1003 | 1,098,299 B | `ed546fe00cdf9646b5a79401bf57884d656041a7d65ee1a3556d435ee915d3e0` | Jain et al. (NeurIPS 2023) Robustness Evaluation |
| **21** | `Tier1_Candidate_Jain_NeurIPS2023` | `jain_attack_samples.json` | 503 | 1,032,321 B | `e68706cc2fd9e9ce6d0611a4f009e4f16428c0b4ec74c6e91bfec1239aa8ec6a` | Jain et al. (NeurIPS 2023) Adversarial Perturbations |
| **22** | `Tier1_Candidate_Jain_NeurIPS2023` | `jain_benign_samples.json` | 500 | 65,981 B | `ebe1bbb5c3e03513a52f94119859fbb008e336b957cf0fa6c043e7b1c3132e4d` | Jain et al. (NeurIPS 2023) Clean Control Samples |
| **23** | `Tier1_REJECTED_Ayub_CAMLIS2024` | `wildguard.json` | 971 | 472,515 B | `62a0f7331af1f2eb01a2cf95b8bc0090f46d30b1b1ef1132fae0d720b5e297f6` | WildGuard / CAMLIS 2024 (Chứng minh FPR 58.41%) |
| **24** | `references_study/JailbreakBench` | `jbb_harmful_100.json` | 100 | 34,556 B | `9ee1cb2aab5223c31aa9ca55f84d667c29beea4f114624b5a3770188ef39f80a` | JailbreakBench Standalone Reference |
| **25** | `references_study/JailbreakBench` | `jbb_benign_100.json` | 100 | 32,018 B | `fac2026f7305d23315df5e554a938c5b0581f476a6cf490aa1572bc8cb0973a2` | JailbreakBench Standalone Reference |

---

## 🔍 Hướng Dẫn Tự Động Kiểm Tra Tính Toàn Vẹn Mã Băm

Để kiểm tra lại tính nguyên bản của toàn bộ 25 tệp dữ liệu bất kỳ lúc nào, chạy lệnh CLI chuẩn:
```powershell
python workspaces/truongnv/scripts/audit_datasets_provenance_deep.py
```
Lệnh trên quét trực tiếp các tệp vật lý, tính toán mã SHA-256 thời gian thực và xác thực đối chiếu với bảng tổng hợp trên.
