# AGENTS.md - PI-Guard Capstone Project Workspace

Welcome to the **PI-Guard** Capstone Project repository. This file defines the operational context, active tools, custom skills, academic terminology constraints, and governance protocols for AI pair programmers assisting the project team.

---

## Project Overview
- **Project Title**: A Machine-Learning Guardrail for Detecting Prompt Injection and Jailbreak Attacks on LLM Applications (**PI-Guard**)
- **Academic Program**: Bachelor of Science in Information Assurance (IA), FPT University (Course Code: `IAP491`, Fall 2026 Semester)
- **Primary Objective**: Design, implement, and benchmark an external, API-driven, Machine-Learning and Transformer-based protective guardrail placed in front of downstream LLM applications to classify incoming user prompts (*Benign* vs. *Prompt Injection* vs. *Jailbreak*) with low latency and low false-positive rate.
- **Tech Stack**: Python 3.11+, PyTorch, Hugging Face Transformers (`microsoft/deberta-v3-base`), Scikit-Learn (TF-IDF Baseline), ONNX Runtime (INT8 Quantization), FastAPI (PoC Proxy), Streamlit (Demo UI), Docker, JupyterLab.

---

## STRICT RULE: IMMUTABLE / READ-ONLY & CONFIDENTIAL UNIVERSITY RESOURCES
> [!CAUTION]
> **CRITICAL INVARIANTS FOR ALL AI AGENTS**:
> 1. The document **`CAPSTONE PROJECT REGISTER.md`** is the official, signed topic registration agreement approved by the Supervisor and FPT University Academic Department.
>
> - **Extracted Reference Summary**: The academic rubrics, continuous assessment mechanism (50% Process / 50% Presentation), and 6-chapter thesis structure are officially synthesized into **`Final-Report/thesis/FPT_IAP491_Capstone_Guidelines_and_Rubrics_Summary.md`**.

---

## STRICT RULE: RESOURCE & LITERATURE VALIDATION PROTOCOL (ZERO DEAD LINKS / OPEN-ACCESS PDF INVARIANT)
> [!IMPORTANT]
> **MANDATORY PROTOCOL FOR CITATIONS, URLS, AND MEDIA**:
> 1. **ZERO DEAD LINKS**: Every URL (website, GitHub repository, academic paper, documentation) written into the repository MUST be validated for live existence (HTTP 200/302). Speculative or hallucinated URLs are strictly prohibited.
> 2. **YOUTUBE OEMBED VERIFICATION**: All YouTube videos MUST be pre-validated via `https://www.youtube.com/oembed?url=...&format=json` to confirm the video exists, is publicly accessible, and is not deleted or private.
> 3. **MANDATORY OPEN-ACCESS PDF**: For scientific papers, **NEVER PROVIDE ONLY A PAYWALLED DOI** (which yields *"You do not currently have access to this content"*). Always locate and attach an open-access PDF link from arXiv, OpenAlex, Semantic Scholar, or author university repositories.
> 4. **VALIDATION TOOLING**: Run `python Final-Report/scripts/verify_resource_url.py --url <URL>`, `--doi <DOI>`, or `--file <file.md>` to verify links automatically before committing.

---

## STRICT RULE: MANDATORY ACADEMIC GROUNDING & ANCHOR INTEGRITY INVARIANT (100% CITED RESEARCH DOCS)
> [!IMPORTANT]
> **MANDATORY SCIENTIFIC RIGOR FOR RESEARCH & THESIS DOCUMENTS**:
> 1. **100% ACADEMIC GROUNDING (ZERO UNSUPPORTED CLAIMS)**:
>    - Every technical assertion, mathematical formulation, attack mechanism, defense architecture, and benchmark figure in research documents (`docs/research/`, `docs/attack_study/`, `docs/model_study/`, `docs/thesis/`) MUST be grounded in peer-reviewed literature (NeurIPS, ICLR, ACM CCS, IEEE S&P), official industry technical reports (OpenAI, Meta, Microsoft, Tencent), or international standards (NIST AI 100-2e2025, OWASP LLM01:2025).
>    - Speculative claims without scientific citations are strictly rejected.
> 2. **ON-PAGE CITATION ANCHOR INTEGRITY (ZERO BROKEN ANCHORS)**:
>    - In-text citation anchors like `[[N]](#refN)` MUST correspond to an identical HTML anchor tag `<a id="refN"></a>` within the References section on the exact same page.
>    - Ensure MkDocs Material compiles with zero missing anchor warnings (`--strict`).
> 3. **SAFE HANDLING OF PAYWALLED DOIS**:
>    - For publisher DOIs protected by paywalls/bot-blocks (ACM, IEEE, Springer): format the DOI as inline code/text (e.g., `DOI: 10.1145/xxxx`) and attach the verified Open-Access PDF link.

---

## STRICT RULE: LITERATURE SCOPING & ARCHITECTURAL COMPATIBILITY INVARIANT (ZERO CITATION BLOAT)
> [!IMPORTANT]
> **SCOPE BOUNDARY FOR LITERATURE & SYSTEM DESIGN**:
> 1. **EXTERNAL GUARDRAIL SCOPE COMPATIBILITY**: All cited scientific works used to justify system architecture MUST be compatible with an **External Guardrail Proxy** paradigm (text-level prompt classification before dispatching to downstream LLMs, requiring zero access to model weights or internal KV-cache).
> 2. **ZERO CITATION BLOAT**: Eliminate out-of-scope papers focusing on hardware tampering, model backdoors, weight data poisoning, or side-channel attacks.
> 3. **LOCAL PDF ARCHIVE**: Every approved academic paper cited in the thesis MUST have a local PDF copy archived in `Final-Report/References/` and indexed in `REFERENCES_LOG.md`.

---

## STRICT RULE: LOCAL REFERENCES FIRST & LITERATURE REUSE PROTOCOL (ZERO REDUNDANT SEARCH)
> [!IMPORTANT]
> **MANDATORY INVARIANT: REUSE ARCHIVED LITERATURE BEFORE DISCOVERY**:
> 1. **INSPECT REFERENCES_LOG.md FIRST**: Before calling any literature MCP tool (`arxiv`, `openalex`, `semanticscholar`, `scholar-feed`) or searching external web/databases for citations, all AI Agents and team members MUST first inspect **`Final-Report/References/REFERENCES_LOG.md`**.
> 2. **PRIORITIZE 18 CORE ARCHIVED PAPERS**: The repository already contains 18 approved, peer-reviewed academic papers covering all core topics (Direct/Indirect Prompt Injection, DAN Jailbreak, TF-IDF N-Grams, DeBERTa-v3, ONNX INT8 Quantization, Low FPR Economics, Adversarial Robustness, and Saltzer & Schroeder 1975). If a claim or topic is already covered, reuse the existing reference and anchor (`[[N]](#refN)`).
> 3. **STRICT THRESHOLD FOR NEW LITERATURE**: External searches are permitted ONLY when researching a newly discovered attack variant or novel method genuinely not addressed in the 18 archived papers.
> 4. **MANDATORY INGESTION PIPELINE**: Any newly accepted paper must be verified for Open-Access PDF, archived in `Final-Report/References/<filename>.pdf`, and indexed in `REFERENCES_LOG.md` with full metadata and BibTeX.

---

## STRICT RULE: FOUR-TIER PROVENANCE & LITERATURE ATTRIBUTION INVARIANT (ZERO CITATION ATTRIBUTION OVERREACH)
> [!IMPORTANT]
> **MANDATORY ACADEMIC RIGOR FOR SCIENTIFIC CITATIONS & PROVENANCE MAPPING**:
> 1. **MANDATORY FOUR-TIER PROVENANCE & DECOUPLING**: Every scientific citation in the thesis, literature review, and reports MUST strictly adhere to 4 distinct tiers:
>    - **Tier 0: Bibliographic Provenance (Baseline Foundation)**: Title, Authors, Venue, Volume/Issue, Year, Pages, DOI, Publication Status, and Primary Authoritative Source. (Errors at Tier 0 invalidate all subsequent analysis).
>    - **Tier 1: Original Author Findings**: Accurately state only what the paper's authors proved, observed, or proposed.
>    - **Tier 2: PI-Guard Design Choice & Adaptation**: Explicitly explain how PI-Guard adopts, inherits, or is inspired by the finding (use semicolons or dedicated sub-bullets).
>    - **Tier 3: PI-Guard Engineering Target & Hypotheses**: Under no circumstances present KPIs, benchmark results, latency, FPR, F1, or performance measurements of PI-Guard as experimental results of the referenced paper, unless that document actually reported the exact same measurement under the exact same conditions.
> 2. **ZERO EQUATION & NOTATION ATTRIBUTION LEAK**: Never attribute project-specific mathematical notations (e.g., $X = S \mathbin{\Vert} U$) or project threat boundaries to general survey or alignment papers (e.g., Zhao et al., InstructGPT). State clearly: *"Within the modeling scope of PI-Guard..."*.
> 3. **AUTHORITATIVE METADATA HIERARCHY**: Before citing any paper, follow this strict verification order:
>    `Publisher/proceedings page -> official conference/journal metadata -> DOI/Crossref -> arXiv/DBLP/OpenReview (when available)`.
>    Do not cite informal demo slogans as official paper titles, and do not conflate conference volumes (e.g., NeurIPS 2023 Vol. 36 vs NeurIPS 2024 Vol. 37).
> 4. **DATASET SAMPLE RIGOR**: Clearly distinguish total corpus size from actual positive attack samples (e.g., Shen et al. DAN dataset: 1,405/15,140 prompts, ~9.29% / rounded 9.3% jailbreaks).

---

## STRICT RULE: ACADEMIC DEFENSE TERMINOLOGY & OVERCLAIMING BLACKLIST PROTOCOL
> [!CAUTION]
> **MANDATORY GOVERNANCE & DEFENSE TERMINOLOGY INVARIANTS**:
> To prevent severe challenges and score deductions before the FPT Academic Council, all team members and AI Agents MUST strictly adhere to the comprehensive terminology blacklist and academic humility protocol defined in **`.agents/rules/academic-defense-terminology-blacklist.md`**.
>
> **Summary of Core Invariants**:
> - **Latency & Performance**: Use **"Low-Latency"** / **"P95 < 30ms"**; strictly ban **"Real-time" / "Thời gian thực"**.
> - **System Identity**: Use **"Academic PoC Prototype"** / **"Latency Testbed"**; strictly ban **"Production-ready enterprise system"**.
> - **Security Guarantees**: Use **"Empirical Risk Mitigation"** / **"Defense-in-Depth"**; strictly ban **"100% unbreakable" / "Bảo vệ tuyệt đối"**.
> - **Scientific Humility & Overclaiming**: Use **"Đủ độ tin cậy làm nền tảng cho Chapter 2"** and **"Automated repository validation: 100% PASS; Academic literature verification: VERIFIED / REVIEWED"**; strictly ban **"Không lo ngại bất kỳ câu hỏi phản biện nào"** or **"Độ chuẩn mực học thuật tối đa"**.

---

## Configured MCP Servers (Model Context Protocol)

The workspace is configured with 11 integrated Model Context Protocol (MCP) servers defined in **`.vscode/mcp.json`**:

1. 📚 **`arxiv`**: Search academic papers, fetch full abstracts, build citation graphs, and perform deep research directly on arXiv preprints.
2. 📖 **`scholar-feed`**: Query scholarly literature across 600k+ CS/AI/ML papers, trace citation lineages, extract full text, and retrieve clean BibTeX entries.
3. 🏛️ **`openalex`**: Global academic index (250M+ works) with automated Open-Access PDF discovery, citation metrics, and peer-reviewed paper resolution across top security venues (ACM CCS, IEEE S&P, USENIX, NeurIPS).
4. 🧠 **`semanticscholar`**: Semantic Scholar API integration featuring AI-powered one-sentence summaries (TLDRs), influential citation analysis, and semantic similarity search from the Allen Institute for AI.
5. ⚡ **`kaggle`**: Official Kaggle MCP server for discovering community security datasets, exploring public prompt injection / transformer notebooks, and executing GPU cloud training experiments (30h/week free T4/P100 GPUs).
6. 🌐 **`duckduckgo-search`**: Web search access for retrieving latest AI security advisories, benchmark datasets, Hugging Face repositories, and technical error code troubleshooting.
7. 📓 **`jupyter`**: Inspect, edit, and execute Jupyter Notebook (.ipynb) cells with active Python kernels and network connectivity.
8. 🎭 **`playwright`**: Headless browser automation and web scraping for dataset verification and online documentation parsing.
9. 💾 **`memory`**: Persistent Knowledge Graph Memory to track experimental benchmarks, architectural decisions, and metric progressions.
10. 💡 **`sequential-thinking`**: Structured multi-step reasoning for algorithm design, adversarial evasion analysis, and bug troubleshooting.
11. 📄 **`officecli`**: Read, edit, generate, and validate Office documents (`.docx`, `.xlsx`, `.pptx`) for thesis compilation and defense slide preparation.

### Research, Lab & Debugging MCP Usage Guide
- **Academic Literature Discovery**: Leverage the golden quartet (`arxiv` for newest preprints, `openalex` for verified open-access PDFs, `semanticscholar` for quick TLDR screening and influential citation graphs, and `scholar-feed` for BibTeX citation trees).
- **GPU Cloud Labs & Dataset Exploration**: Utilize `kaggle` to search reference transformer classification notebooks, access supplementary jailbreak datasets, and manage long-running GPU training jobs without local hardware constraints.
- **Error Code & Technical Troubleshooting**: Use `duckduckgo-search` for PyTorch, Transformers, ONNX Runtime, and FastAPI exceptions; use `jupyter` for interactive debugging in experimental notebooks.
- **Strict Scope Guard**: All tooling and literature queries MUST strictly align with the scope defined in **`CAPSTONE PROJECT REGISTER.md`** (Text-based Prompt Injection, Jailbreak, Classical ML Baselines, DeBERTa-v3, ONNX INT8, and Lightweight FastAPI/Streamlit PoC). Out-of-scope domains (bio/medical tools, cloud enterprise BigQuery data pipelines, hardware attacks) are strictly prohibited.

---

## Available Custom Agent Skills (`.agents/skills/`)

The repository provides 12 specialized, domain-specific agent skills:

1. **`review1-threat-model-and-defense`**: Comprehensive deliverables for Review 1 (Problem definition, Threat modeling under NIST AI 100-2e2025, Attack surface analysis, Demo scenarios, and Slide deck outline).
2. **`llm-security-research`**: OWASP LLM01:2025 taxonomy, threat taxonomy, direct vs. indirect prompt injection, jailbreak archetypes, and SOTA guardrail comparison.
3. **`guardrail-dataset-engineering`**: Data collection, semantic deduplication, Group-Aware Splitting (preventing data leakage across paraphrases), and class balancing across public Hugging Face sources.
4. **`ml-classifier-training`**: Training and optimization workflows for Classical ML baselines (TF-IDF Word/Char + LogisticRegression / LinearSVC) and Transformer Fine-Tuning (`microsoft/deberta-v3-base`) with dynamic loss weighting.
5. **`guardrail-evaluation-metrics`**: Empirical metric evaluation (Precision, Recall, F1, FPR on benign queries, ROC-AUC, Confusion Matrix), adversarial robustness testing against obfuscation, and P95 latency profiling.
6. **`guardrail-api-and-dashboard`**: Lightweight FastAPI guardrail middleware, downstream LLM proxy integration, security logging, and Streamlit interactive live testing dashboard.
7. **`capstone-thesis-and-defense`**: Academic writing assistant for the FPT University Capstone Thesis (IAP491 Chapters 1–6), IEEE citation formatting, and Graduation Defense presentation slide preparation.
8. **`fpt-capstone-rubrics-and-process`**: FPT IAP491 milestone management, weekly process tracking (`PI_GUARD_PROCESS_REPORT.xlsx`), continuous assessment rubrics (Reports 1–6), and committee defense preparation.
9. **`team-git-sync-and-merge`**: Conflict-free Git synchronization protocol, sandboxed workspace isolation, and Leader exclusive merge governance into the main branch.
10. **`team-commit-and-workspace-audit`**: Automated commit and PR auditing tool to detect and prevent unauthorized edits outside designated member sandboxes.
11. **`resource-and-literature-validation`**: Automated verification suite for URLs, YouTube oEmbed endpoints, and Open-Access PDF lookups to prevent broken links and paywalls.
12. **`docs-portal-sync-and-deploy`**: Automated documentation portal builder, synthesizing 8 research dossiers into the MkDocs Material GitHub Pages web portal.

---

## Collaboration Paradigm: Parallel Full-Pipeline Exploration & Knowledge Convergence

> **Team Core Principle**: **Everyone Explores $\rightarrow$ Cross-Review Findings $\rightarrow$ Consensus Finalization**  
> Instead of a fragmented assembly line, all 4 members explore the entire pipeline hands-on in parallel within their individual sandboxes (`workspaces/<member>/`). Weekly convergence meetings consolidate the best empirical results into `Final-Report/src/` and `Final-Report/thesis/chapters/`:

- **Full-Stack Competency**: Every member gains hands-on expertise across Data Engineering, Baseline ML, Transformer Fine-Tuning, Quantization, Adversarial Robustness, and API Integration.
- **Weekly Convergence Sessions**: The team compares empirical metrics (F1, FPR, Latency P95), selects champion modules for `Final-Report/src/`, and compiles thesis chapters collaboratively.
- **Defense Mastery**: Every member understands the complete ecosystem end-to-end, ensuring confident performance during individual committee oral examinations.

| Member | Full-Pipeline Sandbox (100% End-to-End Pipeline) | Workspace Directory |
| :--- | :--- | :--- |
| **Nguyễn Văn Trường (Leader / `nvtruongops`)** | Full Pipeline (Data, Baseline, Transformer, INT8, Proxy) & Overall Architecture | `workspaces/truongnv/` |
| **Nguyễn Quí Đức** | Full Pipeline (Data, Baseline, Transformer, INT8, Proxy) & Empirical Cross-Validation | `workspaces/ducnq/` |
| **Phạm Minh Hoàng Việt** | Full Pipeline (Data, Baseline, Transformer, INT8, Proxy) & Empirical Cross-Validation | `workspaces/vietpmh/` |
| **Đỗ Đoàn Duy Phương** | Full Pipeline (Data, Baseline, Transformer, INT8, Proxy) & Empirical Cross-Validation | `workspaces/phuongddd/` |

---

## STRICT RULE: TÁCH BẠCH HỒ SƠ KỸ THUẬT VÀ QUẢN TRỊ NỘI BỘ (ZERO SILOING & ZERO GOVERNANCE POLLUTION)
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

## Strict Workspace Boundary & Leader Merge Governance Rule

> [!IMPORTANT]
> **ACCESS CONTROL & WORKSPACE BOUNDARY INVARIANTS**:
> 1. **Member Sandbox Isolation**: Members (Đức, Việt, Phương) are authorized to create, modify, and commit files **STRICTLY WITHIN** their assigned personal directory (`workspaces/<member_name>/`). Direct modifications to shared directories (`Final-Report/`, `Github-Page/`, `.agents/`) are strictly prohibited.
> 2. **Leader Sole Merge Authorization**: The Team Leader (`nvtruongops` / Nguyễn Văn Trường) holds exclusive authority to consolidate validated artifacts from member sandboxes into shared production branches during weekly convergence sessions.
> 3. **Automated Audit Verification**: All commits and pull requests must pass `python Final-Report/scripts/validate_local.py` and `python Final-Report/scripts/audit_workspace_boundaries.py`. Unauthorized boundary violations are automatically blocked by the local pre-commit hook.