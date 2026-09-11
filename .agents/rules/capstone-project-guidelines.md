---
trigger: always_on
---

# Capstone Project PI-Guard Guidelines & Rules

## Project Identity
- **Title**: A Machine-Learning Guardrail for Detecting Prompt Injection and Jailbreak Attacks on LLM Applications
- **Abbreviation**: PI-Guard
- **Institution**: FPT University - Information Assurance (IS) Capstone Project

---

## 🚫 IMMUTABLE / READ-ONLY & CONFIDENTIAL UNIVERSITY RESOURCES (STRICT MODIFICATION PROHIBITION)

> [!CAUTION]
> **STRICT RULE FOR ALL AGENTS**:
> 1. The file [`CAPSTONE PROJECT REGISTER.md`](file:///d:/Work/Do-an/CAPSTONE%20PROJECT%20REGISTER.md) is the official, signed topic registration document approved by the Supervisor and FPT University.
> 2. The directory [`docs/fpt_capstone_guide/`](file:///d:/Work/Do-an/docs/fpt_capstone_guide/) contains internal university guidelines, rubrics, and reference forms.
>
> **AGENTS ARE STRICTLY PROHIBITED FROM MODIFYING, EDITING, OVERWRITING, DELETING, COMMITTING, OR EXPOSING `CAPSTONE PROJECT REGISTER.md` OR ANY FILE IN `docs/fpt_capstone_guide/` UNDER ANY CIRCUMSTANCES.**
> - **Confidentiality Invariant**: `docs/fpt_capstone_guide/` is protected by `.gitignore` and must NEVER be copied to `Github-Page/` or made public.
> - **Extracted Reference**: Academic rubrics and thesis structure are officially extracted into [`Final-Report/thesis/FPT_IAP491_Capstone_Guidelines_and_Rubrics_Summary.md`](file:///d:/Work/Do-an/Final-Report/thesis/FPT_IAP491_Capstone_Guidelines_and_Rubrics_Summary.md).
> - **Fall 2026 Milestone Independence**: The **LỘ TRÌNH THỰC HIỆN & 4 CỘT MỐC CHÍNH (MILESTONE TIMELINE HỌC KỲ FALL 2026)** is defined specifically for Fall 2026 with Supervisor Trần Văn Ninh, and is **NOT** taken from the legacy timelines in `docs/fpt_capstone_guide/`.


---

## 🔗 STRICT RULE: RESOURCE & LITERATURE VALIDATION PROTOCOL (ZERO DEAD LINKS / OPEN-ACCESS PDF INVARIANT)

> [!IMPORTANT]
> **QUY TẮC BẮT BUỘC KHI TÌM KIẾM TÀI NGUYÊN, TÀI LIỆU & VIDEO**:
> 1. **ZERO DEAD LINKS**: Mọi URL (website, GitHub, bài báo, tài liệu) trước khi ghi vào repo PHẢI được xác minh tồn tại thực tế (HTTP 200/302). Tuyệt đối không đưa URL suy đoán hoặc hallucinate.
> 2. **YOUTUBE OEMBED VERIFICATION**: Mọi video YouTube PHẢI được kiểm tra qua `https://www.youtube.com/oembed?url=...&format=json` để xác nhận ID video tồn tại, đang mở công khai và không bị xóa/khóa riêng tư.
> 3. **MANDATORY OPEN-ACCESS PDF**: Đối với các bài báo khoa học, tuyệt đối **KHÔNG ĐƯỢC CHỈ CUNG CẤP DOI BỊ PAYWALL** (khiến người đọc bị chặn bởi thông báo *"You do not currently have access to this content"*). Bắt buộc phải tìm và dẫn kèm liên kết tải/đọc PDF bản mở (Open-Access) từ arXiv, OpenAlex, Semantic Scholar hoặc kho tài liệu mở của trường đại học tác giả.
> 4. **CÔNG CỤ KIỂM TRA**: Sử dụng `python scripts/verify_resource_url.py --url <URL>` hoặc `--doi <DOI>` hoặc `--file <file.md>` để tự động xác minh trước khi commit.

---

## 🔬 STRICT RULE: MANDATORY ACADEMIC GROUNDING & ANCHOR INTEGRITY INVARIANT (100% CITED RESEARCH DOCS)

> [!IMPORTANT]
> **QUY TẮC BẮT BUỘC KHI TẠO & CẬP NHẬT TÀI LIỆU NGHIÊN CỨU, CHUYÊN ĐỀ & LUẬN VĂN**:
> 1. **100% ACADEMIC GROUNDING (ZERO UNSUPPORTED CLAIMS)**:
>    - Mọi khẳng định kỹ thuật, công thức toán học, cơ chế tấn công, kiến trúc phòng thủ và số liệu đối sánh trong các tài liệu nghiên cứu (`docs/research/`, `docs/attack_study/`, `docs/model_study/`, `docs/thesis/`) PHẢI được bảo chứng bởi các công trình khoa học đã được bình duyệt (Peer-reviewed Papers tại NeurIPS, ICLR, ACM CCS, IEEE S&P), báo cáo kỹ thuật chính thức (OpenAI, Meta, Microsoft, Tencent) hoặc tiêu chuẩn quốc tế (NIST AI 100-2e2025, OWASP LLM01:2025).
>    - Tuyệt đối không đưa ra các nhận định lý thuyết suông hoặc suy diễn không có trích dẫn khoa học kiểm chứng.
> 2. **ON-PAGE CITATION ANCHOR INTEGRITY (ZERO BROKEN ANCHORS)**:
>    - Khi sử dụng trích dẫn trong văn bản dạng `[[N]](#refN)`, trang tài liệu đó BẮT BUỘC phải có mục Tài Liệu Tham Khảo (References) với neo HTML chuẩn `<a id="refN"></a>` tương ứng trên cùng trang.
>    - Đảm bảo trình biên dịch MkDocs Material biên dịch sạch 100% không có cảnh báo missing anchor.
> 3. **SAFE HANDLING OF PAYWALLED DOIS (OPEN-ACCESS PDF INVARIANT)**:
>    - Đối với các bài báo thuộc nhà xuất bản có tường phí/chặn bot (ACM, Emerald, IEEE): KHÔNG đặt link hyperlink trực tiếp vào DOI để tránh mã lỗi HTTP 403 bot-block.
>    - Định dạng chuẩn: Ghi DOI dạng inline code/text (ví dụ: `DOI: 10.1145/xxxx`) và BẮT BUỘC dẫn kèm link đọc/tải bản mở Open-Access PDF (arXiv, Semantic Scholar, Cambridge/Stanford tech report).
> 4. **DOCS PORTAL AGGREGATION & AUDIT SYNCHRONIZATION**:
>    - Khi tạo mới bất kỳ folder chuyên đề nào, phải lập tức cập nhật `scripts/build_docs_portal.py` và `mkdocs.yml` để cổng Web UI tổng hợp tự động.
>    - Trước khi commit, bắt buộc chạy `python scripts/verify_resource_url.py --file <file>` và `python scripts/audit_workspace_boundaries.py`.

---

## 📚 STRICT RULE: LITERATURE SCOPING & ARCHITECTURAL COMPATIBILITY INVARIANT (ZERO CITATION BLOAT)

> [!IMPORTANT]
> **QUY TẮC SÀNG LỌC TÀI LIỆU NGHIÊN CỨU & CHỐNG DÀN TRẢI TRÍCH DẪN**:
> 1. **EXTERNAL GUARDRAIL SCOPE COMPATIBILITY**: Mọi công trình khoa học được trích dẫn làm cơ sở thiết kế hệ thống PHẢI tương thích với kiến trúc External Guardrail Proxy (phân loại prompt mức văn bản trước khi gọi LLM, không đòi hỏi can thiệp vào trọng số nội bộ hay KV-cache của LLM đích).
> 2. **ZERO CITATION BLOAT**: Kiên quyết loại bỏ các bài báo khảo sát trùng lặp hoặc có phạm vi quá rộng/ngoài phạm vi đề tài (như tấn công phần cứng, backdoor, data poisoning).
> 3. **LOCAL PDF AVAILABILITY**: Mọi tài liệu khoa học được phê duyệt sử dụng trong đồ án BẮT BUỘC phải có bản sao PDF lưu trữ cục bộ trong thư mục `Final-Report/References/` và được định danh trong `REFERENCES_LOG.md`.

---

## 📖 STRICT RULE: LOCAL REFERENCES FIRST & LITERATURE REUSE PROTOCOL (TRUY LỤC TÀI LIỆU CỤC BỘ TRƯỚC TIÊN)

> [!IMPORTANT]
> **QUY TẮC BẮT BUỘC: TÁI SỬ DỤNG TÀI LIỆU CỐT LÕI ĐÃ LƯU TRỮ TRƯỚC KHI TÌM MỚI**:
> 1. **BẮT BUỘC TRA CỨU REFERENCES_LOG.md TRƯỚC TIÊN**: Trước khi gọi bất kỳ công cụ MCP học thuật nào (`arxiv`, `openalex`, `semanticscholar`, `scholar-feed`) hoặc tìm kiếm tài liệu trên mạng, tất cả AI Agent và thành viên nhóm BẮT BUỘC phải tra cứu tệp [`Final-Report/References/REFERENCES_LOG.md`](file:///d:/Work/Do-an/Final-Report/References/REFERENCES_LOG.md).
> 2. **ƯU TIÊN TUYỆT ĐỐI 18 BÀI BÁO CỐT LÕI**: Repository đã tích hợp sẵn 18 công trình khoa học đỉnh cao (được GVHD và Hội đồng phê duyệt) bao quát đầy đủ mọi khía cạnh: Direct/Indirect Prompt Injection, DAN Jailbreak, TF-IDF N-Grams, DeBERTa-v3, Lượng hóa ONNX INT8, Đánh đổi FPR < 1.5%, Kiểm thử Độ bền Đối kháng và Nguyên lý An toàn Thông tin (Saltzer & Schroeder 1975). Khi cần dẫn chứng, BẮT BUỘC tái sử dụng các bài này kèm neo trích dẫn `[[N]](#refN)`.
> 3. **TIÊU CHUẨN KHẮT KHE CHO BÀI BÁO MỚI**: Chỉ tìm kiếm bài báo mới khi xuất hiện kỹ thuật tấn công hoặc phương pháp phòng thủ hoàn toàn mới chưa có trong 18 bài. Mọi bài báo mới phải có bản Open-Access PDF, tải về `Final-Report/References/` và cập nhật đầy đủ metadata vào `REFERENCES_LOG.md`.

---

## 🔬 STRICT RULE: FOUR-TIER PROVENANCE & LITERATURE ATTRIBUTION INVARIANT (QUY TẮC BẤT BIẾN 4 TẦNG & TRUY NGUYÊN HỌC THUẬT)

> [!IMPORTANT]
> **QUY TẮC BẮT BUỘC KHI TRÍCH DẪN & ÁNH XẠ TÀI LIỆU KHOA HỌC**:
> 1. **PHÂN ĐỊNH 4 TẦNG BẮT BUỘC (FOUR-TIER PROVENANCE & DECOUPLING)**:
>    Mọi trích dẫn và phân tích bài báo khoa học trong luận văn và tài liệu chuyên đề PHẢI tuân thủ nghiêm ngặt 4 tầng độc lập:
>    - **Tầng 0: Nguồn Gốc & Siêu Dữ Liệu Xuất Bản (Tier 0 — Bibliographic Provenance)**: Tiêu đề chính thức, Danh sách tác giả, Hội nghị/Tạp chí, Số tập (Volume), Niên giám kỷ yếu (Year), Trang (Pages), DOI/arXiv, Trạng thái xuất bản và Nguồn thẩm quyền gốc (Proceedings/Anthology). *Lỗi tại Tầng 0 sẽ làm vô hiệu hóa toàn bộ các tầng phân tích phía sau*.
>    - **Tầng 1: Đóng góp khoa học gốc của bài báo (Original Author Findings)**: Chỉ nêu chính xác những gì tác giả bài báo thực sự chứng minh, quan sát hoặc đề xuất.
>    - **Tầng 2: Định vị kỹ thuật & Tiếp thu của PI-Guard (PI-Guard Design Choice & Adaptation)**: Trình bày rõ ràng cách đồ án lấy cảm hứng hoặc kế thừa kết quả đó vào thiết kế hệ thống (dùng dấu chấm phẩy `;` hoặc phân tách bằng mục riêng).
>    - **Tầng 3: Mục tiêu kỹ thuật & Giả thuyết của PI-Guard (PI-Guard Target KPI & Hypotheses)**: Không được trình bày KPI, benchmark result, latency, FPR, F1 hoặc performance measurement của PI-Guard như kết quả thực nghiệm của tài liệu tham chiếu, trừ khi tài liệu đó thực sự báo cáo cùng phép đo và cùng điều kiện.
> 2. **CẤM GÁN NGUỒN CÔNG THỨC & MÔ HÌNH HÓA (ZERO EQUATION ATTRIBUTION LEAK)**:
>    - Các công thức toán học và ký hiệu mô hình hóa do nhóm tự đề xuất (như $X = S \mathbin{\Vert} U$) phải được định danh rõ: *"Trong phạm vi mô hình hóa của PI-Guard..."*, tuyệt đối không viết như thể đó là định lý hay ký hiệu từ các bài báo khảo sát (như Zhao et al.).
> 3. **THỨ BẬC NGUỒN XÁC MINH SIÊU DỮ LIỆU CHÍNH THỨC (AUTHORITATIVE METADATA HIERARCHY)**:
>    - Thứ tự tra cứu bắt buộc: `Trang kỷ yếu/nhà xuất bản chính thức (Publisher/Proceedings page) -> Siêu dữ liệu hội nghị/tạp chí (Official Conference/Journal Metadata) -> DOI/Crossref -> arXiv/DBLP/OpenReview (khi có)`.
>    - Tuyệt đối không lấy slogan minh họa làm tiêu đề bài báo, và không nhầm lẫn số tập kỷ yếu (như NeurIPS 2023 Vol. 36 vs NeurIPS 2024 Vol. 37).
> 4. **CHÍNH XÁC HỌC THUẬT VỀ SỐ LIỆU TẬP DỮ LIỆU**:
>    - Khi dẫn số liệu từ các tập dữ liệu thực tế (như Shen et al. DAN dataset), phải phân biệt chính xác giữa kích thước tập dữ liệu tổng quát (15,140 prompts) và số lượng mẫu tấn công thực tế (1,405/15,140 prompts, ~9.29% / làm tròn 9.3%).

---

## 🛡️ STRICT RULE: ACADEMIC DEFENSE TERMINOLOGY & OVERCLAIMING BLACKLIST PROTOCOL

> [!CAUTION]
> **QUY CHUẨN THUẬT NGỮ PHÒNG THỦ HỘI ĐỒNG & CHỐNG KHẲNG ĐỊNH TUYỆT ĐỐI HÓA**:
> Nhằm phòng tránh triệt để các câu hỏi bẫy và nguy cơ bị trừ điểm nặng trước Hội đồng Chấm Bảo vệ Tốt nghiệp FPT (Academic Council), tất cả thành viên và AI Agent bắt buộc phải tuân thủ bảng thuật ngữ chuẩn mực được quy định chi tiết tại [`.agents/rules/academic-defense-terminology-blacklist.md`](file:///d:/Work/Do-an/.agents/rules/academic-defense-terminology-blacklist.md).
>
> **Tóm tắt các bất biến cốt lõi**:
> - **Độ trễ**: Dùng **"Độ trễ thấp" / "P95 < 30ms"**; CẤM TUYỆT ĐỐI **"Thời gian thực" / "Real-time"**.
> - **Phạm vi**: Dùng **"Nguyên mẫu thực nghiệm (Academic PoC Prototype)"**; CẤM TUYỆT ĐỐI **"Hệ thống Production thương mại"**.
> - **An ninh**: Dùng **"Giảm thiểu rủi ro thực nghiệm (Empirical Risk Mitigation)"**; CẤM TUYỆT ĐỐI **"Bảo vệ 100% tuyệt đối" / "Chống hack hoàn toàn"**.
> - **Khiêm tốn khoa học (Scientific Humility)**: Dùng **"Đủ độ tin cậy làm nền tảng cho Chapter 2"** và **"Automated validation: 100% PASS; Literature verification: VERIFIED / REVIEWED"**; CẤM TUYỆT ĐỐI các câu khẳng định chủ quan như **"Không lo ngại bất kỳ câu hỏi phản biện nào"** hay **"Độ chuẩn mực học thuật tối đa"**.

---

## 📖 STRICT RULE: ACADEMIC TERMINOLOGY & CONCEPT GLOSSARY INVARIANT (ZERO UNEXPLAINED ANALOGY)

> [!IMPORTANT]
> **QUY TẮC BẮT BUỘC VỀ CHÚ THÍCH & GIẢI NGHĨA THUẬT NGỮ HỌC THUẬT NỀN TẢNG**:
> Nhằm trang bị đầy đủ cơ sở khoa học để bảo vệ miệng tự tin trước Hội đồng phản biện khi sử dụng các phép so sánh liên ngành (Prepared Statements, Von Neumann, NX-bit, Flat Token Space, Competing Objectives), toàn bộ tài liệu BẮT BUỘC tuân thủ [`.agents/rules/academic-terminology-and-glossary-standards.md`](file:///d:/Work/Do-an/.agents/rules/academic-terminology-and-glossary-standards.md):
> 1. **Gắn neo trong văn bản**: Đánh dấu rõ ràng bằng `[[TNx]](#term-...)`.
> 2. **Bảng giải nghĩa ở cuối**: Bắt buộc có mục `BẢNG THUẬT NGỮ & KHÁI NIỆM HỌC THUẬT NỀN TẢNG` chuẩn hóa 4 trường (`Khái niệm`, `Định nghĩa gốc`, `Phép đối sánh trong PI-Guard`, `Tài liệu tham chiếu`).
> 3. **Kiểm định tự động**: Xác nhận qua `python Final-Report/scripts/verify_academic_glossary.py` tích hợp trong `validate_local.py`.

---

## Parallel Full-Pipeline Exploration & Knowledge Convergence Paradigm

> **Phương châm làm việc toàn đội**: **Ai cũng làm $\rightarrow$ Tham khảo nhau $\rightarrow$ Chốt kết quả**  
> All 4 members work hands-on across the entire pipeline in parallel workspaces (`workspaces/<member>/`) and converge findings during weekly meetings:

1. **Parallel Full-Stack Hands-on**: Every member explores data collection, baseline training, transformer fine-tuning, adversarial testing, and API integration to build deep, end-to-end expertise.
2. **Weekly Convergence Sessions**: The team compares empirical metrics (F1, FPR, Latency), selects the champion models for `src/`, and co-authors thesis chapters.
3. **Council Defense Mastery**: Every member understands the full ecosystem end-to-end, preventing knowledge silos and enabling confident defense before the FPT Committee.
4. **Leader Governance**: Student 1 (Nguyễn Văn Trường / `nvtruongops`) supervises overall project direction, code merges, and milestone submissions.

---

## ⚖️ STRICT RULE: TÁCH BẠCH HỒ SƠ KỸ THUẬT VÀ QUẢN TRỊ NỘI BỘ (ZERO SILOING & ZERO GOVERNANCE POLLUTION)

> [!CAUTION]
> **QUY TẮC BẢO VỆ PHÒNG THỦ HỌC THUẬT & CHỐNG PHÂN MẢNH MÔ ĐUN (ANTI-SILOING INVARIANT)**:
> 1. **QUẢN TRỊ NỘI BỘ (TEAM TỰ BIẾT, CẤM HÔ HÀO TRONG TÀI LIỆU KỸ THUẬT)**:
>    - Phương châm "Ai cũng làm toàn bộ pipeline" là nguyên tắc nội bộ giúp cả 4 thành viên làm chủ toàn diện hệ thống để tự tin bảo vệ trước Hội đồng. Nhóm tự biết và quản lý qua `AGENTS.md` cùng Sổ tiến độ `PI_GUARD_PROCESS_REPORT.xlsx`.
>    - Tuyệt đối **KHÔNG** đưa các câu khẩu hiệu sinh hoạt nhóm vào tài liệu kỹ thuật, chuyên đề nghiên cứu (`docs/`, `reports/`, `thesis/`). Mọi tài liệu kỹ thuật phải giữ văn phong khoa học, khách quan 100%.
> 2. **CẤM TUYỆT ĐỐI TẠO BẢNG PHÂN CÔNG CHIA CẮT MÔ ĐUN (ZERO SILOING ASSIGNMENT)**:
>    - Tuyệt đối **KHÔNG** tạo các bảng "Phân công trách nhiệm cá nhân" kiểu chia rẽ module (như gán Đức chỉ làm Baseline, Việt chỉ làm Transformer, Phương chỉ làm Web/API) trong các tài liệu kỹ thuật nộp cho GVHD hoặc Hội đồng.
>    - **Nguy cơ phòng thủ học thuật**: Hội đồng FPT sẽ coi việc chia module này là làm việc kiểu dây chuyền phân mảnh (siloing), dẫn đến việc thành viên bị coi là không tham gia vào phần lõi khoa học của đồ án (AI/ML) và bị trừ điểm nặng.
> 3. **CHUẨN HÓA QUY TRÌNH THỰC NGHIỆM TÁI LẬP HỆ THỐNG**:
>    - Mọi quy trình thực nghiệm B1–B5 phải được trình bày như một **"Quy trình thực nghiệm tái lập hệ thống (Standardized Reproducibility Pipeline)"** khách quan, cho phép bất kỳ ai (sinh viên, nhà nghiên cứu hay phản biện) cũng có thể chạy độc lập để tái lập 100% kết quả.

---

## 🔒 Strict Workspace Boundary & Commit Audit Rules

1. **Member Boundary Isolation**:
   - Members (Đức, Việt, Phương) MUST ONLY create/edit files inside their designated workspace folder:
     - `workspaces/ducnq/`
     - `workspaces/vietpmh/`
     - `workspaces/phuongddd/`
   - Direct edits to common directories (`Final-Report/`, `Github-Page/`, `.agents/`) by non-leader members are strictly prohibited.
2. **Leader Sole Merge Authorization**:
   - Only the Leader (`nvtruongops`) is authorized to merge champion artifacts from `workspaces/` into root production directories during weekly convergence sessions.
3. **Automated Commit Audit Enforcement**:
   - All commits and PRs must pass `python Final-Report/scripts/validate_local.py` or `python Final-Report/scripts/audit_workspace_boundaries.py`.
   - Pre-commit hook (`Final-Report/scripts/validate_local.py --install-hook`) must be installed on all member environments.

---

## Directory & Architectural Standards (Đúng 3 Phân Hệ Độc Tôn Tại Thư Mục Gốc)

```
d:/Work/Do-an/
├── Final-Report/                # [1. BÁO CÁO TỔNG & MÃ NGUỒN SẢN PHẨM] Luận văn, mã nguồn, tests, scripts, tài nguyên thực nghiệm
│   ├── src/                     # [CORE CODEBASE] API, models, preprocessing, dashboard, evaluation
│   ├── tests/                   # [TEST SUITE] Bộ kiểm thử tự động pytest
│   ├── scripts/                 # [TOOLING & QA] Bộ công cụ kiểm định Local QA & build docs portal
│   ├── thesis/                  # Luận văn tốt nghiệp (FINAL_THESIS.md, Review 1, Chapters 1-6)
│   ├── notebooks/               # Toàn bộ tài nguyên thực nghiệm & Jupyter Notebooks tái lập (configs/, data/, models/)
│   ├── Meeting/                 # Biên bản họp với GVHD & nội bộ nhóm (Meeting 1, 2, 3)
│   ├── References/              # 18 bài báo khoa học chuẩn (PDF) & REFERENCES_LOG.md
│   ├── reports/                 # [PERIODIC REPORTS & METRICS] Sổ tiến độ, slide trình chiếu & benchmark
│   │   ├── PI-GUARD-Present-109.pptx # Slide báo cáo tiến độ gặp GVHD ngày 10/09/2026
│   │   ├── PI_GUARD_PROCESS_REPORT.xlsx # Sổ theo dõi tiến độ chính thức (Process Report)
│   │   ├── experiment_reports/  # Kết quả thực nghiệm tự động (JSON)
│   │   └── README.md            # Hướng dẫn chi tiết phân hệ báo cáo định kỳ
│   ├── figures/                 # Sơ đồ kiến trúc & hình ảnh trích xuất
│   ├── tables/                  # Bảng biểu đối chuẩn
│   ├── requirements.txt         # Master Production Dependencies
│   ├── requirements-dev.txt     # Master Development Dependencies
│   └── .env.example             # Master Environment Configuration Template
├── Github-Page/                 # [2. GITHUB PAGES] Cổng tài liệu Web UI chính thức (MkDocs Material 8 Chuyên Đề)
│   ├── index.md                 # Trang chủ cổng tài liệu
│   └── [8 Chuyên Đề Khoa Học]/  # Toàn bộ nội dung chuyên đề xuất bản lên web
└── workspaces/                  # [3. WORKSPACE THÀNH VIÊN] Sandbox cá nhân của 4 thành viên (truongnv, ducnq, vietpmh, phuongddd)
```
