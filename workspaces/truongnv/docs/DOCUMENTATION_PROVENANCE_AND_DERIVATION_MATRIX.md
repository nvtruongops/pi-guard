# MA TRẬN NGUỒN GỐC XUẤT XỨ & PHẢ HỆ TÁI CẤU TRÚC TÀI LIỆU
## (DOCUMENTATION PROVENANCE & DERIVATION MATRIX)
### Đồ án Tốt nghiệp: PI-Guard (`IAP491_FA26_PI_GUARD`) — Đại học FPT
**Trưởng nhóm nghiên cứu**: Nguyễn Văn Trường (Leader — `SE182034`)  
**Giảng viên hướng dẫn**: ThS. Trần Văn Ninh  
**Mục đích**: Cung cấp bằng chứng khoa học tường minh về phả hệ kế thừa, xuất xứ nguồn gốc và dữ liệu thực nghiệm bảo chứng cho từng tài liệu sau khi tái cấu trúc.

---

## 1. Sơ Đồ Phả Hệ Tiến Hóa Tài Liệu (Documentation Evolution Lineage)

Hệ thống tài liệu của phân hệ `workspaces/truongnv/` được phát triển liên tục qua các cột mốc tuần họp, sau đó được hợp nhất và chuẩn hóa theo mô hình Kim tự tháp tài liệu 3 tầng:

```mermaid
graph TD
    subgraph S1["GIAI ĐOẠN 1: CÁC CỘT MỐC TUẦN HỌP (HISTORICAL MILESTONES)"]
        M4["Meeting 4 (10/09/2026)<br/>report_for_meeting_4/<br/>• Khảo sát ban đầu<br/>• Báo cáo Supervisor"]
        M5["Meeting 5 (19/09/2026)<br/>tasks_for_meeting_5/<br/>• Task 1: Injection vs Jailbreak<br/>• Task 2: 8 Attack Vectors<br/>• Task 2.5: SOTA & Two-Tier<br/>• Task 3: 5 Upstream Models<br/>• Task 4: PIGuard Improvements"]
        M6["Meeting 6 (26/09/2026)<br/>tasks_for_meeting_6/<br/>• 01: Taxonomy & Paradigms<br/>• 02: Compatibility 12x14<br/>• 03: Council Defense Briefs<br/>• 04: Cross-Dataset Benchmarks"]
    end

    subgraph S2["GIAI ĐOẠN 2: 5 HỒ SƠ CHUYÊN SÂU GỐC (TECHNICAL DOSSIERS - SSOT)"]
        D1["Dossier 01: MATHEMATICAL FOUNDATIONS<br/>(Lý thuyết Von Neumann, Attention Inversion, 4 Tiers, 3 RQs)"]
        D2["Dossier 02: THREAT MODEL & 8 KEYS<br/>(Khung 5D NIST AI 100-2e2025, Bề mặt REST API, 8 Keys)"]
        D3["Dossier 03: SOTA SURVEY & 6 BASELINES<br/>(Phễu 41 papers -> 6 Baselines trên D1-D6, Điểm vỡ mô hình)"]
        D4["Dossier 04: DATA ENGINEERING & PROVENANCE<br/>(100% SHA-256 trên 25 tệp, Group-Aware Splitting MinHash/LSH)"]
        D5["Dossier 05: ARCHITECTURAL DEPRECATIONS<br/>(Luận giải loại trừ INT8/ONNX/ZeroQuant, Llama Guard 8B)"]
    end

    subgraph S3["GIAI ĐOẠN 3: BỘ SẢN PHẨM BÁO CÁO CHÍNH THỨC (CANONICAL DELIVERABLES)"]
        R1["BÁO CÁO REVIEW 1<br/>reports/report_for_review1/<br/>• README.md (5-Min Fast-Track)<br/>• REVIEW_1_REPORT.md (Toàn văn Master)<br/>• REVIEW_1_PRESENTATION_AND_QA_SCRIPT.md"]
        TH["KHÓA LUẬN TỐT NGHIỆP<br/>docs/thesis/chapters/<br/>• 01_Introduction.md<br/>• 02_Literature_Review.md"]
    end

    M4 --> M5
    M5 --> M6
    
    M5 -.->|Kế thừa & Nâng cấp| D1
    M5 -.->|Kế thừa & Nâng cấp| D2
    M5 -.->|Kế thừa & Nâng cấp| D3
    M5 -.->|Kế thừa & Nâng cấp| D4
    
    M6 -.->|Kế thừa & Nâng cấp| D2
    M6 -.->|Kế thừa & Nâng cấp| D3
    M6 -.->|Kế thừa & Nâng cấp| D5
    
    D1 --> R1
    D2 --> R1
    D3 --> R1
    D4 --> R1
    D5 --> R1
    
    D1 --> TH
    D2 --> TH
    D3 --> TH

    style S1 fill:#f5f5f5,stroke:#9e9e9e,stroke-width:1px
    style S2 fill:#e8f5e9,stroke:#4caf50,stroke-width:2px
    style S3 fill:#e3f2fd,stroke:#2196f3,stroke-width:2px
```

---

## 2. Bảng Ma Trận Nguồn Gốc & Bằng Chứng Kế Thừa Chi Tiết (Provenance Matrix)

Bảng đối chiếu minh chứng cụ thể từng tài liệu sau tái cấu trúc được tổng hợp, nâng cấp từ những tài liệu nào của các tuần họp trước và được bảo chứng bởi các bài báo / bằng chứng dữ liệu nào:

| Tài Liệu Sau Tái Cấu Trúc (Canonical Document) | Nguồn Tài Liệu Tiền Thân Được Kế Thừa (Precursor Sources) | Bằng Chứng Dữ Liệu & Mã Nguồn Thực Nghiệm (Empirical Evidence) | Cơ Sở Học Thuật & Tiêu Chuẩn Quốc Tế (Academic Standards) | Giá Trị Gia Tăng Sau Tái Cấu Trúc (Restructuring Value-Add) |
| :--- | :--- | :--- | :--- | :--- |
| **Dossier 01: Mathematical Foundations**<br>[`docs/research/dossiers/01_MATHEMATICAL_FOUNDATIONS.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/dossiers/01_MATHEMATICAL_FOUNDATIONS.md) | • `tasks_for_meeting_5/task_reports/TASK_1_PROMPT_INJECTION_VS_JAILBREAK.md`<br>• `tasks_for_meeting_5/.../CONTROL_FLOW_HIJACKING_AND_FLAT_TOKEN_SPACE.md`<br>• `docs/research_deep/TRACK1_...` | • Biểu thức ma trận Softmax Attention.<br>• Phân tích hội tụ Softmax khi độ dài prompt tăng.<br>• Bộ chỉ số nghiệm thu 3 RQs (Jaccard, ARR, P95). | • Perez & Ribeiro (NeurIPS 2022 [[3]](#ref3))<br>• Greshake et al. (ACM CCS 2023 [[4]](#ref4))<br>• Vaswani et al. (NeurIPS 2017 [[1]](#ref1)) | Hình thức hóa toán học chặt chẽ $X = S \mathbin{\Vert} U$, chứng minh hiện tượng Attention Allocation Inversion, bổ sung so sánh SQL Injection vs Prompt Injection. |
| **Dossier 02: Threat Model & 8 Keys**<br>[`docs/research/dossiers/02_THREAT_MODEL_AND_8KEYS.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/dossiers/02_THREAT_MODEL_AND_8KEYS.md) | • `tasks_for_meeting_5/task_reports/TASK_2_ATTACK_VECTORS_AND_MODELS.md`<br>• `tasks_for_meeting_6/01_theory_and_taxonomy/KEY_ATTACK_VECTORS...md`<br>• `docs/research_deep/TRACK2_...` | • `audit_project_keys_coverage.py` (8/8 Key đạt 100%).<br>• `key_coverage_matrix_report.json`<br>• Bộ 40 mẫu tiếng Việt VMLU thực nghiệm. | • NIST AI 100-2e2025 [[7]](#ref7)<br>• OWASP Top 10 for LLM 2025 [[8]](#ref8)<br>• Saltzer & Schroeder (1975 — Complete Mediation) | Áp dụng đầy đủ Khung 5 trục NIST AI 100-2e2025, định vị bề mặt duy nhất cổng REST API, phân định nghiêm ngặt In/Out-of-Scope. |
| **Dossier 03: SOTA Survey & 6 Baselines**<br>[`docs/research/dossiers/03_SOTA_SURVEY_AND_6BASELINES.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/dossiers/03_SOTA_SURVEY_AND_6BASELINES.md) | • `tasks_for_meeting_5/task_reports/TASK_2_5_SOTA_ASSESSMENT...md`<br>• `tasks_for_meeting_6/01_theory.../TAXONOMY_OF_ARCHITECTURES...md`<br>• `tasks_for_meeting_6/02_compatibility...md`<br>• `docs/research_deep/TRACK3_...` | • `comprehensive_empirical_benchmark_suite.json`<br>• Số liệu đối chuẩn D1–D6 thật trên 6 mô hình.<br>• Bằng chứng Prompt-Guard FPR 99.1% trên code. | • He et al. (DeBERTa-v3 ICLR 2023 [[11]](#ref11))<br>• Inan et al. (Llama Guard 2023 [[9]](#ref9))<br>• Jain et al. (NeurIPS 2023 [[13]](#ref13))<br>• Robey et al. (SmoothLLM 2023 [[14]](#ref14)) | Thiết lập Phễu khoa học 5 bước (41 $\to$ 16 $\to$ 11 $\to$ 9 $\to$ 6), luận giải phân tích tử huyệt kỹ thuật chứng minh tính tất yếu của Two-Tier Cascade. |
| **Dossier 04: Data Engineering & Provenance**<br>[`docs/research/dossiers/04_DATA_ENGINEERING_PROVENANCE.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/dossiers/04_DATA_ENGINEERING_PROVENANCE.md) | • `tasks_for_meeting_5/task_reports/TASK_3_REPRODUCIBILITY_AND_DATASETS.md`<br>• `tasks_for_meeting_6/04_benchmarks_and_data/all_11_replications...json`<br>• `docs/research_deep/TRACK4_...` | • `audit_datasets_provenance_deep.py` (25 tệp SHA-256).<br>• `dataset_readiness_for_piguard_training.json`<br>• MinHash LSH Group-Aware Splitter script. | • Broder (1997 — MinHash Shingling)<br>• Hao Li et al. (PIGuard ACL 2025 [[18]](#ref18))<br>• Shen et al. (ACM CCS 2024 [[15]](#ref15)) | Cung cấp bảng chứng minh 100% SHA-256 không giả lập, giải thuật khử rò rỉ dữ liệu cụm Jaccard < 0.15 và vai trò NotInject D6. |
| **Dossier 05: Architectural Deprecations**<br>[`docs/research/dossiers/05_ARCHITECTURAL_DEPRECATIONS.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/dossiers/05_ARCHITECTURAL_DEPRECATIONS.md) | • `reports/ARCHITECTURAL_DEPRECATIONS_AND_OUT_OF_SCOPE.md`<br>• `tasks_for_meeting_5/.../REJECTED_BASELINE_AYUB_CAMLIS2024.md`<br>• `tasks_for_meeting_6/03_reports.../COUNCIL_DEFENSE_RATIONALE...md` | • Thực nghiệm sụt giảm FPR khi lượng tử hóa.<br>• Benchmark Ayub CAMLIS 2024 (FPR 58.41% bị loại).<br>• Đo đạc RAM và CPU latency FP32 Native. | • Nguyên lý kỹ thuật YAGNI<br>• Dettmers et al. (LLM.int8() 2022)<br>• Angelopoulos et al. (CRC 2024 [[22]](#ref22)) | Hệ thống hóa toàn bộ các công nghệ bị loại trừ (INT8, ONNX, ZeroQuant, Llama Guard 8B, Ayub baseline) cùng lý do kỹ thuật và toán học rõ ràng. |
| **Review 1 Master Report**<br>[`reports/report_for_review1/REVIEW_1_REPORT.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/report_for_review1/REVIEW_1_REPORT.md) | • Toàn bộ 5 Dossiers trên.<br>• `tasks_for_meeting_5/README.md`<br>• `tasks_for_meeting_6/README.md` | • Tổng hợp kết quả thực nghiệm toàn hệ thống.<br>• Bảng Latency Budget Breakdown.<br>• Xác nhận kiểm định 100% PASS trên 8 module QA. | • 18 Tài liệu tham khảo chuẩn IEEE tại `REFERENCES_LOG.md`.<br>• Chuẩn thẩm định Review 1 Đại học FPT. | Tích hợp thành báo cáo toàn văn 95+ KB đáp ứng trọn vẹn Chapter 1, Chapter 2 và 7 tiêu chí đánh giá của Hội đồng chấm. |

---

## 3. Quy Tắc Duy Trì Tính Toàn Vẹn Của Các Thư Mục Lịch Sử

Để bảo đảm tính khách quan học thuật và không làm gãy các liên kết kiểm thử tự động:
1. **Các thư mục tuần họp cũ (`tasks_for_meeting_5/`, `tasks_for_meeting_6/`, `report_for_meeting_4/`)**:
   - Được bảo tồn nguyên vẹn 100% tại đường dẫn gốc trong `workspaces/truongnv/reports/`.
   - Mỗi thư mục được gắn biểu ngữ **Historical Milestone Archive Banner** tại file `README.md` để dẫn chiếu người đọc sang các Dossiers chuẩn hóa và Báo cáo Review 1 chính thức.
   - Các script kiểm định tự động (`Final-Report/scripts/validate_local.py`, `verify_academic_glossary.py`) tiếp tục chạy mượt mà mà không gặp bất kỳ lỗi thiếu file hay sai đường dẫn nào.
2. **Khử trùng lặp tại phân hệ Replications**:
   - Thay vì sao chép 11 bảng mã hash SHA-256 vào 11 thư mục con riêng biệt, phân hệ thiết lập tệp trung tâm [`replications/SHARED_DATASETS_PROVENANCE.md`](file:///d:/Work/Do-an/workspaces/truongnv/replications/SHARED_DATASETS_PROVENANCE.md) làm Single Source of Truth.
   - Các file `DATASET_PROVENANCE.md` cục bộ giữ vai trò cổng liên kết dẫn về bảng trung tâm.

---

## 4. Kết Luận
Việc tái cấu trúc tài liệu theo ma trận nguồn gốc này đã giải quyết triệt để vấn đề "mật độ file quá dày đặc và trùng lặp nội dung", biến kho tài liệu phân tán thành một **hệ thống tri thức có phả hệ minh bạch (Traceable Knowledge Base)**, sẵn sàng phục vụ công tác thanh tra học thuật của Giảng viên hướng dẫn và Hội đồng thẩm định đồ án tốt nghiệp.
