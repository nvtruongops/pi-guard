# AGENTS.md - PI-Guard Capstone Project Workspace

Welcome to the **PI-Guard** Capstone Project repository. This file defines the operational context, active tools, custom skills, academic terminology constraints, and governance protocols for AI pair programmers assisting the project team.

---

## 🛡️ Project Overview
- **Project Title**: A Machine-Learning Guardrail for Detecting Prompt Injection and Jailbreak Attacks on LLM Applications (**PI-Guard**)
- **Academic Program**: Bachelor of Science in Information Assurance (IA), FPT University (Course Code: `IAP491`, Fall 2026 Semester)
- **Primary Objective**: Design, implement, and benchmark an external, API-driven, Machine-Learning and Transformer-based protective guardrail placed in front of downstream LLM applications to classify incoming user prompts (*Benign* vs. *Prompt Injection* vs. *Jailbreak*) with low latency and low false-positive rate.
- **Tech Stack**: Python 3.11+, PyTorch, Hugging Face Transformers (`microsoft/deberta-v3-base`), Scikit-Learn (TF-IDF Baseline), ONNX Runtime (INT8 Quantization), FastAPI (PoC Proxy), Streamlit (Demo UI), Docker, JupyterLab.

---

## 🚫 STRICT RULE: IMMUTABLE / READ-ONLY & CONFIDENTIAL UNIVERSITY RESOURCES
> [!CAUTION]
> **CRITICAL INVARIANTS FOR ALL AI AGENTS**:
> 1. The document [`CAPSTONE PROJECT REGISTER.md`](file:///d:/Work/Do-an/CAPSTONE%20PROJECT%20REGISTER.md) is the official, signed topic registration agreement approved by the Supervisor and FPT University Academic Department.
> 2. The directory [`docs/fpt_capstone_guide/`](file:///d:/Work/Do-an/docs/fpt_capstone_guide/) contains internal, confidential university guidelines, rubrics, and evaluation templates (strictly local, protected by `.gitignore`).
>
> **AGENTS MUST ONLY READ AND NEVER MODIFY, OVERWRITE, DELETE, COMMIT, OR EXPOSE ANY FILES IN `docs/fpt_capstone_guide/` OR `CAPSTONE PROJECT REGISTER.md` UNDER ANY CIRCUMSTANCES.**
> - **Confidentiality & Zero Public Leakage**: Never copy or publish files from `docs/fpt_capstone_guide/` into `Github-Page/` or any public repository path.
> - **Extracted Reference Summary**: The academic rubrics, continuous assessment mechanism (50% Process / 50% Presentation), and 6-chapter thesis structure are officially synthesized into [`Final-Report/thesis/FPT_IAP491_Capstone_Guidelines_and_Rubrics_Summary.md`](file:///d:/Work/Do-an/Final-Report/thesis/FPT_IAP491_Capstone_Guidelines_and_Rubrics_Summary.md).
> - **Fall 2026 Milestone Independence**: The **4 Main Milestones & 15-Week Timeline (Fall 2026)** is established specifically for the Fall 2026 schedule with Supervisor Trần Văn Ninh, and is **NOT** derived from legacy timelines in `docs/fpt_capstone_guide/`.

---

## 🔗 STRICT RULE: RESOURCE & LITERATURE VALIDATION PROTOCOL (ZERO DEAD LINKS / OPEN-ACCESS PDF INVARIANT)
> [!IMPORTANT]
> **MANDATORY PROTOCOL FOR CITATIONS, URLS, AND MEDIA**:
> 1. **ZERO DEAD LINKS**: Every URL (website, GitHub repository, academic paper, documentation) written into the repository MUST be validated for live existence (HTTP 200/302). Speculative or hallucinated URLs are strictly prohibited.
> 2. **YOUTUBE OEMBED VERIFICATION**: All YouTube videos MUST be pre-validated via `https://www.youtube.com/oembed?url=...&format=json` to confirm the video exists, is publicly accessible, and is not deleted or private.
> 3. **MANDATORY OPEN-ACCESS PDF**: For scientific papers, **NEVER PROVIDE ONLY A PAYWALLED DOI** (which yields *"You do not currently have access to this content"*). Always locate and attach an open-access PDF link from arXiv, OpenAlex, Semantic Scholar, or author university repositories.
> 4. **VALIDATION TOOLING**: Run `python Final-Report/scripts/verify_resource_url.py --url <URL>`, `--doi <DOI>`, or `--file <file.md>` to verify links automatically before committing.

---

## 🔬 STRICT RULE: MANDATORY ACADEMIC GROUNDING & ANCHOR INTEGRITY INVARIANT (100% CITED RESEARCH DOCS)
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

## 📚 STRICT RULE: LITERATURE SCOPING & ARCHITECTURAL COMPATIBILITY INVARIANT (ZERO CITATION BLOAT)
> [!IMPORTANT]
> **SCOPE BOUNDARY FOR LITERATURE & SYSTEM DESIGN**:
> 1. **EXTERNAL GUARDRAIL SCOPE COMPATIBILITY**: All cited scientific works used to justify system architecture MUST be compatible with an **External Guardrail Proxy** paradigm (text-level prompt classification before dispatching to downstream LLMs, requiring zero access to model weights or internal KV-cache).
> 2. **ZERO CITATION BLOAT**: Eliminate out-of-scope papers focusing on hardware tampering, model backdoors, weight data poisoning, or side-channel attacks.
> 3. **LOCAL PDF ARCHIVE**: Every approved academic paper cited in the thesis MUST have a local PDF copy archived in `Final-Report/References/` and indexed in `REFERENCES_LOG.md`.

---

## 🛡️ STRICT RULE: ACADEMIC TERMINOLOGY & DEFENSE BLACKLIST / WHITELIST PROTOCOL

To prevent severe challenges and score deductions during committee defenses before the FPT Academic Council, all team members and AI Agents must strictly adhere to the following terminology blacklist/whitelist:

| Category | 🚫 Banned Terminology (Blacklist) | ✅ Mandatory Academic Terms (Whitelist) | Technical & Defense Rationale |
| :--- | :--- | :--- | :--- |
| **Latency & Performance** | • "Thời gian thực" / "Real-time"<br>• "Real-time detection"<br>• "Hệ thống thời gian thực" | • **"Độ trễ thấp" / "Low-Latency"**<br>• **"Độ trễ suy luận (Inference Latency)"**<br>• **"Inline Guardrail Proxy"**<br>• **"Thời gian đáp ứng nhanh (P95 < 30ms)"** | In Computer Science and Embedded Systems, *"Real-time"* denotes deterministic sub-millisecond hard deadlines with zero jitter. HTTP guardrail proxies cannot offer hard real-time guarantees; using "real-time" invites severe council criticism. |
| **System Identity & Scope** | • "Hệ thống Production thương mại"<br>• "Production-ready enterprise system"<br>• "Kiến trúc cấp doanh nghiệp"<br>• "Commercial SaaS guardrail" | • **"Nguyên Mẫu Thực Nghiệm Học Thuật (Academic Proof-of-Concept Prototype)"**<br>• **"Môi Trường Đo Đạc Độ Trễ (Inference Latency Testbed)"**<br>• **"Plug-and-Play Guardrail Middleware"** | PI-Guard is an **IAP491 Research-Based Thesis**, not a commercial Software Engineering product. Claiming "Production" triggers demands for OAuth2, RBAC, billing, multi-tenancy, and distributed 100k RPS load tests. |
| **Security Guarantees** | • "Bảo vệ 100% tuyệt đối"<br>• "Chống hack hoàn toàn"<br>• "Unbreakable defense"<br>• "Silver bullet solution" | • **"Giảm thiểu rủi ro thực nghiệm (Empirical Risk Mitigation)"**<br>• **"Phòng thủ theo chiều sâu (Defense-in-Depth)"**<br>• **"Độ chính xác cao ($F_1 \ge 0.95$, $\text{FPR} < 1.5\%$)"**<br>• **"Khả năng chống chịu đối kháng (Adversarial Robustness)"** | Prompt injection operates in a flat token space ($X = S \mathbin{\Vert} U$); mathematical proof of absolute immunity is non-existent. Promising 100% defense is scientifically invalid. |
| **Hardware & Deployment** | • "Bắt buộc hạ tầng GPU đắt tiền"<br>• "Hệ thống đòi hỏi cụm máy chủ lớn" | • **"Triển khai tối ưu trên CPU tiêu chuẩn (Zero-GPU Commodity CPU)"**<br>• **"Lượng hóa động sau huấn luyện (ONNX INT8 Quantization)"** | The project registration explicitly specifies commodity multi-core CPU deployment with zero hardware purchase overhead for inference. |
| **Model Intervention** | • "Can thiệp trọng số nội tại của GPT-4"<br>• "Retrain lại downstream LLM"<br>• "Sửa đổi KV-cache bộ nhớ" | • **"Lớp lọc đầu vào độc lập (Model-Agnostic External Input Guardrail)"**<br>• **"Kiểm tra mức văn bản (Prompt-Level Inspection)"**<br>• **"Tương thích hộp đen (Black-Box LLM Compatibility)"** | PI-Guard protects downstream LLMs as an external reverse proxy. Modifying closed-source or third-party LLM weights is completely outside the threat model. |

---

## 🛠️ Configured MCP Servers (Model Context Protocol)

The workspace is configured with 8 integrated Model Context Protocol (MCP) servers defined in [`.vscode/mcp.json`](file:///d:/Work/Do-an/.vscode/mcp.json):

1. 📚 **`arxiv`**: Search academic papers, fetch full abstracts, build citation graphs, and perform deep research directly on arXiv.
2. 📖 **`scholar-feed`**: Query scholarly literature across 600k+ CS/AI/ML papers, trace citation lineages, extract full text, and retrieve clean BibTeX entries.
3. 🌐 **`duckduckgo-search`**: Web search access for retrieving latest AI security advisories, benchmark datasets, Hugging Face repositories, and technical error code troubleshooting.
4. 📓 **`jupyter`**: Inspect, edit, and execute Jupyter Notebook (.ipynb) cells with active Python kernels and network connectivity.
5. 🎭 **`playwright`**: Headless browser automation and web scraping for dataset verification and online documentation parsing.
6. 🧠 **`memory`**: Persistent Knowledge Graph Memory to track experimental benchmarks, architectural decisions, and metric progressions.
7. 💡 **`sequential-thinking`**: Structured multi-step reasoning for algorithm design, adversarial evasion analysis, and bug troubleshooting.
8. 📄 **`officecli`**: Read, edit, generate, and validate Office documents (`.docx`, `.xlsx`, `.pptx`) for thesis compilation and defense slide preparation.

### 🎯 Research & Debugging MCP Usage Guide
- **Academic Literature Discovery**: Prefer `arxiv` and `scholar-feed` for finding peer-reviewed papers (2022–2026), followed by `duckduckgo-search` for conference proceedings (ACM CCS, NeurIPS, ICLR, IEEE S&P).
- **Error Code & Technical Troubleshooting**: Use `duckduckgo-search` for PyTorch, Transformers, ONNX Runtime, and FastAPI exceptions; use `jupyter` for interactive debugging in experimental notebooks.
- **Strict Scope Guard**: All tooling and literature queries MUST strictly align with the scope defined in [`CAPSTONE PROJECT REGISTER.md`](file:///d:/Work/Do-an/CAPSTONE%20PROJECT%20REGISTER.md) (Text-based Prompt Injection, Jailbreak, Classical ML Baselines, DeBERTa-v3, ONNX INT8, and Lightweight FastAPI/Streamlit PoC).

---

## 🧠 Available Custom Agent Skills (`.agents/skills/`)

The repository provides 12 specialized, domain-specific agent skills:

1. [`review1-threat-model-and-defense`](file:///d:/Work/Do-an/.agents/skills/review1-threat-model-and-defense/SKILL.md): Comprehensive deliverables for Review 1 (Problem definition, Threat modeling under NIST AI 100-2e2025, Attack surface analysis, Demo scenarios, and Slide deck outline).
2. [`llm-security-research`](file:///d:/Work/Do-an/.agents/skills/llm-security-research/SKILL.md): OWASP LLM01:2025 taxonomy, threat taxonomy, direct vs. indirect prompt injection, jailbreak archetypes, and SOTA guardrail comparison.
3. [`guardrail-dataset-engineering`](file:///d:/Work/Do-an/.agents/skills/guardrail-dataset-engineering/SKILL.md): Data collection, semantic deduplication, Group-Aware Splitting (preventing data leakage across paraphrases), and class balancing across public Hugging Face sources.
4. [`ml-classifier-training`](file:///d:/Work/Do-an/.agents/skills/ml-classifier-training/SKILL.md): Training and optimization workflows for Classical ML baselines (TF-IDF Word/Char + LogisticRegression / LinearSVC) and Transformer Fine-Tuning (`microsoft/deberta-v3-base`) with dynamic loss weighting.
5. [`guardrail-evaluation-metrics`](file:///d:/Work/Do-an/.agents/skills/guardrail-evaluation-metrics/SKILL.md): Empirical metric evaluation (Precision, Recall, F1, FPR on benign queries, ROC-AUC, Confusion Matrix), adversarial robustness testing against obfuscation, and P95 latency profiling.
6. [`guardrail-api-and-dashboard`](file:///d:/Work/Do-an/.agents/skills/guardrail-api-and-dashboard/SKILL.md): Lightweight FastAPI guardrail middleware, downstream LLM proxy integration, security logging, and Streamlit interactive live testing dashboard.
7. [`capstone-thesis-and-defense`](file:///d:/Work/Do-an/.agents/skills/capstone-thesis-and-defense/SKILL.md): Academic writing assistant for the FPT University Capstone Thesis (IAP491 Chapters 1–6), IEEE citation formatting, and Graduation Defense presentation slide preparation.
8. [`fpt-capstone-rubrics-and-process`](file:///d:/Work/Do-an/.agents/skills/fpt-capstone-rubrics-and-process/SKILL.md): FPT IAP491 milestone management, weekly process tracking (`PI_GUARD_PROCESS_REPORT.xlsx`), continuous assessment rubrics (Reports 1–6), and committee defense preparation.
9. [`team-git-sync-and-merge`](file:///d:/Work/Do-an/.agents/skills/team-git-sync-and-merge/SKILL.md): Conflict-free Git synchronization protocol, sandboxed workspace isolation, and Leader exclusive merge governance into the main branch.
10. [`team-commit-and-workspace-audit`](file:///d:/Work/Do-an/.agents/skills/team-commit-and-workspace-audit/SKILL.md): Automated commit and PR auditing tool to detect and prevent unauthorized edits outside designated member sandboxes.
11. [`resource-and-literature-validation`](file:///d:/Work/Do-an/.agents/skills/resource-and-literature-validation/SKILL.md): Automated verification suite for URLs, YouTube oEmbed endpoints, and Open-Access PDF lookups to prevent broken links and paywalls.
12. [`docs-portal-sync-and-deploy`](file:///d:/Work/Do-an/.agents/skills/docs-portal-sync-and-deploy/SKILL.md): Automated documentation portal builder, synthesizing 8 research dossiers into the MkDocs Material GitHub Pages web portal.

---

## 👥 Collaboration Paradigm: Parallel Full-Pipeline Exploration & Knowledge Convergence

> **Team Core Principle**: **Everyone Explores $\rightarrow$ Cross-Review Findings $\rightarrow$ Consensus Finalization**  
> Instead of a fragmented assembly line, all 4 members explore the entire pipeline hands-on in parallel within their individual sandboxes (`workspaces/<member>/`). Weekly convergence meetings consolidate the best empirical results into `Final-Report/src/` and `Final-Report/thesis/chapters/`:

- **Full-Stack Competency**: Every member gains hands-on expertise across Data Engineering, Baseline ML, Transformer Fine-Tuning, Quantization, Adversarial Robustness, and API Integration.
- **Weekly Convergence Sessions**: The team compares empirical metrics (F1, FPR, Latency P95), selects champion modules for `Final-Report/src/`, and compiles thesis chapters collaboratively.
- **Defense Mastery**: Every member understands the complete ecosystem end-to-end, ensuring confident performance during individual committee oral examinations.

| Member | Full-Pipeline Sandbox & Focus Area | Workspace Directory |
| :--- | :--- | :--- |
| **Nguyễn Văn Trường (Leader / `nvtruongops`)** | Overall Architecture, Data Engineering, Group-Aware Splitting & Repository Governance | `workspaces/truongnv/` |
| **Nguyễn Quí Đức** | Classical ML Baseline (TF-IDF Word/Char N-Grams), Feature Extraction & Threat Surface Modeling | `workspaces/ducnq/` |
| **Phạm Minh Hoàng Việt** | Transformer Fine-Tuning (`microsoft/deberta-v3-base`), ONNX INT8 Quantization & Adversarial Robustness | `workspaces/vietpmh/` |
| **Đỗ Đoàn Duy Phương** | FastAPI Guardrail Middleware Proxy, Streamlit Dashboard, Demo Testbed & Thesis Compilation | `workspaces/phuongddd/` |

---

## 🔒 Strict Workspace Boundary & Leader Merge Governance Rule

> [!IMPORTANT]
> **ACCESS CONTROL & WORKSPACE BOUNDARY INVARIANTS**:
> 1. **Member Sandbox Isolation**: Members (Đức, Việt, Phương) are authorized to create, modify, and commit files **STRICTLY WITHIN** their assigned personal directory (`workspaces/<member_name>/`). Direct modifications to shared directories (`Final-Report/`, `Github-Page/`, `.agents/`) are strictly prohibited.
> 2. **Leader Sole Merge Authorization**: The Team Leader (`nvtruongops` / Nguyễn Văn Trường) holds exclusive authority to consolidate validated artifacts from member sandboxes into shared production branches during weekly convergence sessions.
> 3. **Automated Audit Verification**: All commits and pull requests must pass `python Final-Report/scripts/validate_local.py` and `python Final-Report/scripts/audit_workspace_boundaries.py`. Unauthorized boundary violations are automatically blocked by the local pre-commit hook.
