# AGENTS.md - PI-Guard Capstone Project Workspace

Welcome to the **PI-Guard** Capstone Project repository. This file defines the operational context, available tools, skills, and role assignments for AI pair programmers assisting the project team.

---

## 🛡️ Project Overview
- **Name**: A Machine-Learning Guardrail for Detecting Prompt Injection and Jailbreak Attacks on LLM Applications (**PI-Guard**)
- **Objective**: Develop an API-driven, ML/Transformer-based protective guardrail placed in front of LLM applications to classify user prompts (Benign vs. Prompt Injection vs. Jailbreak) with low latency and low false-positive rate.
- **Tech Stack**: Python 3.11+, PyTorch, Hugging Face Transformers (`microsoft/deberta-v3-base`), Scikit-Learn (TF-IDF Baseline), FastAPI, Streamlit, Docker, JupyterLab.

---

## 🚫 STRICT RULE: IMMUTABLE / READ-ONLY FILES & DIRECTORIES
> **CRITICAL RULES FOR ALL AI AGENTS**:
> 1. The file [`CAPSTONE PROJECT REGISTER.md`](file:///d:/Work/Do-an/CAPSTONE%20PROJECT%20REGISTER.md) is the official, signed topic registration document approved by the Supervisor and FPT University.
> 2. The directory [`docs/fpt_capstone_guide/`](file:///d:/Work/Do-an/docs/fpt_capstone_guide/) contains internal university thesis guidelines, rubrics, and reference forms.
>
> **AGENTS MUST ONLY READ AND NEVER MODIFY, EDIT, OVERWRITE, OR DELETE ANY FILES IN `docs/fpt_capstone_guide/` OR `CAPSTONE PROJECT REGISTER.md` UNDER ANY CIRCUMSTANCES.**
> These resources are strictly immutable and read-only.

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

## 🛠️ Configured MCP Servers (Model Context Protocol)

The workspace has 7 integrated MCP servers:
1. 📚 **`arxiv`**: Search academic papers, fetch abstracts, build citation graphs, and perform literature reviews directly.
2. 📓 **`jupyter`**: Run, inspect, and execute Jupyter Notebooks (.ipynb) with Python kernels and internet access.
3. 🌐 **`duckduckgo-search`**: Search for latest benchmarks, Hugging Face repos, and LLM security advisories.
4. 🎭 **`playwright`**: Headless web automation and scraping for datasets and documentation.
5. 🧠 **`memory`**: Persistent Knowledge Graph Memory to track experimental results and architectural decisions.
6. 💡 **`sequential-thinking`**: Structured multi-step reasoning for algorithm design and troubleshooting.
7. 📄 **`officecli`**: Read, edit, generate, and validate Office documents (.docx, .xlsx, .pptx) for thesis reporting and presentations.

---

## 🧠 Available Custom Agent Skills (`.agents/skills/`)

- [`review1-threat-model-and-defense`](file:///d:/Work/Do-an/.agents/skills/review1-threat-model-and-defense/SKILL.md): Deliverables for Review 1 (Problem definition, Threat modeling, Attack surface, Demo scenarios, Slide outline).
- [`llm-security-research`](file:///d:/Work/Do-an/.agents/skills/llm-security-research/SKILL.md): OWASP LLM01 taxonomy, threat classification, and SOTA comparison.
- [`guardrail-dataset-engineering`](file:///d:/Work/Do-an/.agents/skills/guardrail-dataset-engineering/SKILL.md): Dataset curation, deduplication, group-aware splitting, and class balancing.
- [`ml-classifier-training`](file:///d:/Work/Do-an/.agents/skills/ml-classifier-training/SKILL.md): TF-IDF baseline + DeBERTa-v3 Transformer training and ONNX quantization.
- [`guardrail-evaluation-metrics`](file:///d:/Work/Do-an/.agents/skills/guardrail-evaluation-metrics/SKILL.md): Precision, Recall, F1, FPR on benign inputs, and latency profiling.
- [`guardrail-api-and-dashboard`](file:///d:/Work/Do-an/.agents/skills/guardrail-api-and-dashboard/SKILL.md): FastAPI async middleware + Streamlit live testing dashboard.
- [`capstone-thesis-and-defense`](file:///d:/Work/Do-an/.agents/skills/capstone-thesis-and-defense/SKILL.md): Academic thesis writing structure (FPT IAP491 Chapters 1-6) and defense presentation deck.
- [`fpt-capstone-rubrics-and-process`](file:///d:/Work/Do-an/.agents/skills/fpt-capstone-rubrics-and-process/SKILL.md): FPT IAP491 milestone tracking, weekly process reports (PROCESS_REPORT.xlsx), and grading rubrics.
- [`team-git-sync-and-merge`](file:///d:/Work/Do-an/.agents/skills/team-git-sync-and-merge/SKILL.md): Quy trình Git phân nhánh, đồng bộ không xung đột và độc quyền merge vào cây thư mục chính dành cho Leader.
- [`team-commit-and-workspace-audit`](file:///d:/Work/Do-an/.agents/skills/team-commit-and-workspace-audit/SKILL.md): Công cụ tự động kiểm toán commit/PR, phát hiện và ngăn chặn vi phạm chỉnh sửa ngoài `workspaces/`.
- [`resource-and-literature-validation`](file:///d:/Work/Do-an/.agents/skills/resource-and-literature-validation/SKILL.md): Tiêu chuẩn và công cụ kiểm định URL, video YouTube oEmbed và tự động tra cứu Open-Access PDF từ DOI chống paywall.

---

## 👥 Collaboration Paradigm: Parallel Full-Pipeline Exploration & Knowledge Convergence

> **Phương châm làm việc toàn đội**: **Ai cũng làm $\rightarrow$ Tham khảo nhau $\rightarrow$ Chốt kết quả**  
> Instead of a siloed assembly-line, all 4 members explore the entire pipeline hands-on in parallel (`workspaces/<member>/`) and consolidate the best findings during weekly convergence meetings into `src/` and `docs/thesis/chapters/`:

- **All 4 members gain full-stack AI security experience** (Dataset Curation, Baseline ML, Transformer INT8, Adversarial Testing, FastAPI Middleware).
- **Weekly Convergence Sessions**: The team compares experimental metrics (F1, FPR, Latency), selects the champion models/code for `src/`, and compiles thesis chapters seamlessly.
- **Council Defense Preparedness**: Every member understands the full ecosystem end-to-end and can answer any committee question confidently.

| Member | Full-Pipeline Sandbox & Focus Area | Workspace Directory | Git Feature Branch |
| :--- | :--- | :--- | :--- |
| **Nguyễn Văn Trường (Leader / `nvtruongops`)** | Architecture, Data Engineering & Repository Governance | `workspaces/truongnv/` | `main`, `lead/truong-*` |
| **Nguyễn Quí Đức** | Classical ML Baseline, Feature Extraction & Methodology | `workspaces/ducnq/` | `feat/duc-baseline-ml` |
| **Phạm Minh Hoàng Việt** | Transformer Fine-Tuning, Quantization & Robustness | `workspaces/vietpmh/` | `feat/viet-transformer` |
| **Đỗ Đoàn Duy Phương** | FastAPI Middleware, Dashboard & Thesis Compilation | `workspaces/phuongddd/` | `feat/phuong-api-ui` |

---

## 🔒 Strict Workspace Boundary & Leader Merge Governance Rule

> [!IMPORTANT]
> **QUY ĐỊNH PHÂN QUYỀN GIT & RANH GIỚI WORKSPACE BẤT BIẾN**:
> 1. **Thành viên (Đức, Việt, Phương)**: CHỈ ĐƯỢC PHÉP tạo, sửa đổi và commit các file nằm bên trong thư mục workspace cá nhân được chỉ định (`workspaces/<tên_thành_viên>/`). Tuyệt đối không được sửa đổi trực tiếp các file chung (`src/`, `docs/`, `Meeting/`, `reports/`, `models/`, `data/`, etc.).
> 2. **Trưởng nhóm (Leader: `nvtruongops` / Nguyễn Văn Trường)**: Là NGƯỜI DUY NHẤT có thẩm quyền đồng quy tri thức, chọn lọc module xuất sắc nhất từ `workspaces/` của các thành viên để merge ra cây thư mục chung và xuất bản vào nhánh `main`.
> 3. **Kiểm toán tự động**: Sử dụng `python scripts/validate_local.py` hoặc `python scripts/audit_workspace_boundaries.py` trước khi commit hoặc merge. Mọi commit vi phạm ranh giới sẽ bị chặn tự động bởi Git Pre-commit Hook (`python scripts/validate_local.py --install-hook`).

