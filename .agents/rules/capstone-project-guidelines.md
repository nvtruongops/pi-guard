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

## 🛡️ STRICT RULE: ACADEMIC TERMINOLOGY & DEFENSE BLACKLIST / WHITELIST PROTOCOL

Nhằm phòng tránh triệt để các câu hỏi bẫy và nguy cơ bị trừ điểm nặng trước Hội đồng Chấm Bảo vệ Tốt nghiệp FPT (Academic Council), tất cả thành viên và AI Agent bắt buộc phải tuân thủ bảng thuật ngữ chuẩn mực:

| Phân Loại | 🚫 Thuật Ngữ Bị Cấm Tuyệt Đối (Blacklist) | ✅ Thuật Ngữ Học Thuật Bắt Buộc (Whitelist) | Luận Giải Kỹ Thuật & Phòng Thủ Hội Đồng |
| :--- | :--- | :--- | :--- |
| **Độ trễ & Hiệu năng** | • "Thời gian thực" / "Real-time"<br>• "Real-time detection"<br>• "Hệ thống thời gian thực" | • **"Độ trễ thấp" / "Low-Latency"**<br>• **"Độ trễ suy luận (Inference Latency)"**<br>• **"Inline Guardrail Proxy"**<br>• **"Thời gian đáp ứng nhanh (P95 < 30ms)"** | Trong Khoa học Máy tính, *"Real-time"* chỉ các hệ thống nhúng có cam kết thời gian ngặt nghèo cấp microsecond (Zero Jitter). Một HTTP Guardrail Proxy không thể cam kết hard real-time; dùng từ này sẽ bị Hội đồng bắt lỗi nặng. |
| **Bản chất Hệ thống & Phạm vi** | • "Hệ thống Production thương mại"<br>• "Production-ready enterprise system"<br>• "Kiến trúc cấp doanh nghiệp"<br>• "Commercial SaaS guardrail" | • **"Nguyên Mẫu Thực Nghiệm Học Thuật (Academic Proof-of-Concept Prototype)"**<br>• **"Môi Trường Đo Đạc Độ Trễ (Inference Latency Testbed)"**<br>• **"Plug-and-Play Guardrail Middleware"** | PI-Guard là Khóa luận Tốt nghiệp Nghiên cứu (**IAP491 Research Thesis**), không phải sản phẩm Kỹ thuật Phần mềm thương mại. Khẳng định "Production" sẽ bị đòi hỏi OAuth2, RBAC, billing, multi-tenancy và load test 100k RPS. |
| **Cam kết An ninh** | • "Bảo vệ 100% tuyệt đối"<br>• "Chống hack hoàn toàn"<br>• "Unbreakable defense"<br>• "Silver bullet solution" | • **"Giảm thiểu rủi ro thực nghiệm (Empirical Risk Mitigation)"**<br>• **"Phòng thủ theo chiều sâu (Defense-in-Depth)"**<br>• **"Độ chính xác cao ($F_1 \ge 0.95$, $\text{FPR} < 1.5\%$)"**<br>• **"Khả năng chống chịu đối kháng (Adversarial Robustness)"** | Không gian token là không gian phẳng ($X = S \mathbin{\Vert} U$); về mặt toán học không thể miễn nhiễm tuyệt đối. Tuyên bố an toàn 100% là phi khoa học. |
| **Phần cứng & Triển khai** | • "Bắt buộc hạ tầng GPU đắt tiền"<br>• "Hệ thống đòi hỏi cụm máy chủ lớn" | • **"Triển khai tối ưu trên CPU tiêu chuẩn (Zero-GPU Commodity CPU)"**<br>• **"Lượng hóa động sau huấn luyện (ONNX INT8 Quantization)"** | Bản đăng ký đề tài ghi rõ triển khai trên CPU đa nhân thông thường, không phát sinh chi phí mua sắm GPU máy chủ cho nhà trường. |
| **Can thiệp Mô hình** | • "Can thiệp trọng số nội tại của GPT-4"<br>• "Retrain lại downstream LLM"<br>• "Sửa đổi KV-cache bộ nhớ" | • **"Lớp lọc đầu vào độc lập (Model-Agnostic External Input Guardrail)"**<br>• **"Kiểm tra mức văn bản (Prompt-Level Inspection)"**<br>• **"Tương thích hộp đen (Black-Box LLM Compatibility)"** | PI-Guard hoạt động như một reverse proxy kiểm tra prompt mức văn bản. Việc can thiệp vào trọng số LLM thương mại hoặc KV-cache là phi thực tế và ngoài phạm vi đề tài. |

---

## Parallel Full-Pipeline Exploration & Knowledge Convergence Paradigm

> **Phương châm làm việc toàn đội**: **Ai cũng làm $\rightarrow$ Tham khảo nhau $\rightarrow$ Chốt kết quả**  
> All 4 members work hands-on across the entire pipeline in parallel workspaces (`workspaces/<member>/`) and converge findings during weekly meetings:

1. **Parallel Full-Stack Hands-on**: Every member explores data collection, baseline training, transformer fine-tuning, adversarial testing, and API integration to build deep, end-to-end expertise.
2. **Weekly Convergence Sessions**: The team compares experimental metrics (F1, FPR, Latency), selects the champion models for `src/`, and co-authors thesis chapters.
3. **Council Defense Mastery**: Every member understands the full ecosystem end-to-end, preventing knowledge silos and enabling confident defense before the FPT Committee.
4. **Leader Governance**: Student 1 (Nguyễn Văn Trường / `nvtruongops`) supervises overall project direction, code merges, and milestone submissions.

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
