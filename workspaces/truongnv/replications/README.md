# Replication candidates and data provenance

**Audit date:** 2026-09-30. Every local metric must pair a method/model and dataset from the same paper's pinned release or exact experiment. Public files and source hashes alone do not validate a mixed cross-paper run.

## Scope Boundary Declaration

- **IN-SCOPE:** source/model packages, paper-matched runs, withdrawn runs, and support scripts in this directory.
- **OUT-OF-SCOPE:** cross-paper checkpoint/data evaluation, full-reproduction claims without protocol evidence, and a PI-Guard cascade claim.

## Current reportable runs

| Bundle | Pairing and boundary |
|---|---|
| [`PIDS_Bench_Shire_IEEEAccess2026`](./PIDS_Bench_Shire_IEEEAccess2026/) | Keep the PIDS-Bench author TF-IDF + Logistic Regression fit on pinned PIDS-Bench data. All 3,918 test predictions were matched to the source test split and metrics recomputed. The local ProtectAI comparison is withdrawn. |
| [`Paper_ACL2025_PIGuard_HaoLi`](./Paper_ACL2025_PIGuard_HaoLi/) | Preserve original paper assets. The local PIGuard report keeps only the PIGuard checkpoint on PIGuard-released evaluation assets. |

## Cleaned & Removed Assets (Audit 2026-10-02)

- `01_TFIDF_Syntactic_Baseline`: Đã xóa toàn bộ vào ngày 2026-10-02 theo quyết định kiểm định căn chỉnh paper–model–code; thay thế hoàn toàn bằng baseline chuẩn có paper và mã nguồn tác giả trong [`PIDS_Bench_Shire_IEEEAccess2026`](./PIDS_Bench_Shire_IEEEAccess2026/).
- `02_DeBERTa_v3_Semantic_Classifier`: Năm snapshot không đạt chuẩn paper gốc và repository chính thức (`DeepSetDeBERTa`, `FMOPSDistilBERT`, `InjectionSentry`, `ProtectAI`, `WolfDefenderSmall`) đã được xóa khỏi `upstream/checkpoints/` (thu hồi 2,968.13 MiB). Duy nhất snapshot chính thức của `PIGuard` được lưu giữ.
- `ProtectAI_DeBERTa_v3_v2`: Đã xóa gói wrapper riêng vào ngày 2026-10-02 do thiếu paper nghiên cứu gốc và training repository chính thức.
- Báo cáo kết quả hỗn hợp Review 1 và các phép ghép chéo checkpoint không cùng provenance tiếp tục được ghi nhận đã rút.

Original source repositories, model cards, and source-origin files remain indexed for provenance; their presence does not endorse a withdrawn experiment. See [`BENCHMARK_RESULTS_DASHBOARD.md`](./BENCHMARK_RESULTS_DASHBOARD.md).
