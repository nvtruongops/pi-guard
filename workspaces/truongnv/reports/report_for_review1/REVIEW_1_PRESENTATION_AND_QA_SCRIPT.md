# Review 1 presentation and Q&A — evidence-bounded version

## Scope Boundary Declaration

- **IN-SCOPE:** trình bày local results đã qua pairing audit và tách chúng khỏi đề xuất.
- **OUT-OF-SCOPE:** dùng lại cross-paper metrics hoặc claim cascade đã đo.

PI-Guard là đề xuất guardrail văn bản bên ngoài, hướng tới ba nhãn Benign, Prompt Injection và Jailbreak. Hiện chưa có kết quả cho model ba lớp hay cascade PI-Guard.

Hai run độc lập được giữ lại: PIDS-Bench TF-IDF + Logistic Regression theo method và dữ liệu cùng paper; và checkpoint PIGuard trên public evaluation assets phát hành cùng PIGuard. PIDS-Bench có 3.918 prediction rows được đối chiếu test split và metric được tính lại. PIGuard có sáu source hashes và 1.435 input rows qua verifier. Hai giao thức khác nhau, không so sánh trực tiếp. Xem [PIDS-Bench](../../replications/PIDS_Bench_Shire_IEEEAccess2026/REPORT.md), [PIGuard-only](../../replications/02_DeBERTa_v3_Semantic_Classifier/reports/review1_paper_model_public_rerun_2026-09-30/REPORT.md), refs [[18]](../../References/REFERENCES_LOG.md#ref18) [[44]](../../References/REFERENCES_LOG.md#ref44) [[45]](../../References/REFERENCES_LOG.md#ref45).

Public-vector, Review 2/Tier 1, D1–D6, and ProtectAI cross-paper runs are withdrawn. Deletion was blocked and their files remain, but they are not current evidence. P95 < 30 ms and FPR < 1.5% are project targets. No formal Review 1 acceptance is established here.

## Q&A

**What is measured locally?** Two individual paper-matched runs listed above, each with its own dataset and protocol.

**Can the two models be ranked?** No. Their labels, datasets, and protocols differ.

**Is the two-tier system validated?** No. No current run measures conditional routing or end-to-end cascade behavior.

**Why are older benchmark tables omitted?** Their local model/data pairs cross paper origins or use project-built splits. The strict provenance audit withdrew them; the folders remain after deletion was blocked.
