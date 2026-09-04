---
trigger: always_on
---

# Capstone Project PI-Guard Guidelines & Rules

## Project Identity
- **Title**: A Machine-Learning Guardrail for Detecting Prompt Injection and Jailbreak Attacks on LLM Applications
- **Abbreviation**: PI-Guard
- **Institution**: FPT University - Information Assurance (IS) Capstone Project

---

## 🚫 IMMUTABLE / READ-ONLY FILES & DIRECTORIES (STRICT MODIFICATION PROHIBITION)

> [!CAUTION]
> **STRICT RULE FOR ALL AGENTS**:
> 1. The file [`CAPSTONE PROJECT REGISTER.md`](file:///d:/Work/Do-an/CAPSTONE%20PROJECT%20REGISTER.md) is the official, signed topic registration document approved by the Supervisor and FPT University.
> 2. The directory [`docs/fpt_capstone_guide/`](file:///d:/Work/Do-an/docs/fpt_capstone_guide/) contains internal university guidelines, rubrics, and templates.
>
> **AGENTS ARE STRICTLY PROHIBITED FROM MODIFYING, EDITING, OVERWRITING, OR DELETING `CAPSTONE PROJECT REGISTER.md` OR ANY FILE IN `docs/fpt_capstone_guide/` UNDER ANY CIRCUMSTANCES.**
> Agents must ONLY READ these files for reference. They are 100% immutable and read-only.

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
> 3. **LOCAL PDF AVAILABILITY**: Mọi tài liệu khoa học được phê duyệt sử dụng trong đồ án BẮT BUỘC phải có bản sao PDF lưu trữ cục bộ trong thư mục `References/` và `workspaces/<thành_viên>/References/`.

---

## ⏱️ STRICT RULE: PROHIBITION OF "THỜI GIAN THỰC" (REAL-TIME) TERMINOLOGY FOR LATENCY

> [!IMPORTANT]
> **QUY TẮC BẮT BUỘC VỀ THUẬT NGỮ ĐỘ TRỄ & HIỆU NĂNG**:
> 1. **TUYỆT ĐỐI KHÔNG DÙNG CỤM TỪ "VẬN HÀNH THỜI GIAN THỰC" HOẶC "THỜI GIAN THỰC" (REAL-TIME)** để miêu tả độ trễ hay hiệu năng của Guardrail API, vì "thời gian thực" (Hard/Soft Real-Time System) là thuật ngữ kỹ thuật đặc thù cho các hệ thống điều khiển nhúng với cam kết microsecond nghiêm ngặt.
> 2. **THUẬT NGỮ BẮT BUỘC SỬ DỤNG**:
>    - **"Độ trễ thấp" / "Low-Latency"** (ví dụ: *P95 < 30ms trên CPU đa nhân*).
>    - **"Bảo vệ trực tuyến" / "Inline Guardrail Proxy"**.
>    - **"Thời gian đáp ứng nhanh" / "Độ trễ suy luận (Inference Latency)"**.

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
   - Direct edits to common directories (`src/`, `docs/`, `Meeting/`, `reports/`, `models/`, `data/`) by non-leader members are strictly prohibited.
2. **Leader Sole Merge Authorization**:
   - Only the Leader (`nvtruongops`) is authorized to merge champion artifacts from `workspaces/` into root production directories during weekly convergence sessions.
3. **Automated Commit Audit Enforcement**:
   - All commits and PRs must pass `python scripts/validate_local.py` or `python scripts/audit_workspace_boundaries.py`.
   - Pre-commit hook (`scripts/validate_local.py --install-hook`) must be installed on all member environments.

---

## Directory & Architectural Standards

```
d:/Work/Do-an/
├── .agents/
│   ├── mcp_config.json          # Workspace MCP servers (arxiv, jupyter, search, playwright, memory)
│   ├── rules/                   # Project guidelines & agent behavior rules
│   └── skills/                  # Domain-specific Agent Skills
├── data/                        # Datasets (raw, processed, splits, adversarial_tests)
├── notebooks/                   # Jupyter Notebooks for exploration and training
├── src/
│   ├── preprocessing/           # Cleaners, normalizers, and obfuscation generators
│   ├── models/                  # ML baseline and Transformer inference wrappers
│   ├── api/                     # FastAPI guardrail service and LLM proxy
│   ├── dashboard/               # Streamlit interactive testing & metrics dashboard
│   └── evaluation/              # Benchmark scripts, metrics calculators, and latency profiler
├── models/                      # Saved trained models (.joblib, PyTorch checkpoints, ONNX)
├── Meeting/                     # Meeting minutes and supervisor notes
├── References/                  # Academic papers, PDFs, and literature references
├── requirements.txt             # Python dependencies
└── AGENTS.md                    # Agent operating standards
```
