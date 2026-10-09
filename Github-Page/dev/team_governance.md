# AGENTS.md — PI-Guard Master Governance & Agent Dispatcher

Welcome to the **PI-Guard** Capstone Project repository. This file serves as the **Master Governance & Agent Dispatcher** for all AI pair programmers and human team members.

---

## 1. Project Identity & Academic Scope

- **Project Title**: A Machine-Learning Guardrail for Detecting Prompt Injection and Jailbreak Attacks on LLM Applications (**PI-Guard**)
- **Academic Program**: Information Assurance capstone research.
- **Supervisor**: project supervisor | **Lead Student**: repository maintainer
- **Academic Team Roster**: project participant (`student identifier`), project participant (`student identifier`), project participant (`student identifier`). This roster records the capstone team and is separate from repository access.
- **Git Repository Maintainer & Report Owner**: repository maintainer (`repository account` / `student identifier`) is the sole current maintainer and publisher of this repository. Tracked reports record group progress and research outcomes as consolidated by the leader; listed members are project participants, not current repository contributors.
- **Primary Objective**: Design, implement, and benchmark an external, API-driven, Machine-Learning and Transformer-based protective guardrail placed in front of downstream LLM applications to classify incoming user prompts (*Benign* vs. *Prompt Injection* vs. *Jailbreak*) with low latency (P95 < 30ms) and low false-positive rate (FPR < 1.5%).
- **Architectural Paradigm**: **External Guardrail Proxy** (Text-level inspection before forwarding to downstream black-box LLMs; zero access to internal model weights or KV-cache).
- **Tech Stack**: Python 3.11+, PyTorch, Hugging Face Transformers (`microsoft/deberta-v3-base` Native FP32), Scikit-Learn (Dual TF-IDF Baseline), FastAPI (PoC Proxy), Streamlit (Demo UI), Docker.

---

## 2. Master Governance Rules Registry (`.agents/rules/`)

All AI Agents **MUST STRICTLY COMPLY** with the 7 modular governance rules. Violations will cause immediate rejection by automated validation tools:

| Rule Code | Rule Title & Link | Core Invariant & Purpose | Automated QA Tool |
| :---: | :--- | :--- | :--- |
| **`RULE-02`** | **`rule-02-task-scope-and-milestone-enclosure.md`** | **Task File is the Boundary Law**: Mandatory 3-step pre-execution scope bounding; Anti-Scope Creep; deprecations in Rule 02 (no INT8/ONNX/ZeroQuant); Phase gating (Chapter 2 = baselines only). | `audit_task_scope.py` |
| **`RULE-03`** | **`rule-03-anti-hallucination-and-grounding.md`** | Zero premature model code (`AH-01`: no `src/models/cascade/` in Ch.2); Zero fabricated metrics (`AH-02`); Zero synthetic/random generators (`AH-03`); 100% empirical un-mocked JSON evidence (`AH-04`). | `audit_anti_hallucination.py` |
| **`RULE-04`** | **`rule-04-sentence-level-evidence-standards.md`** | Sentence-level evidence `[[N]](#refN)`; Zero vague attribution; 3-way epistemic decoupling (Literature Fact vs. Empirical Fact vs. Project Proposal). | `audit_claim_evidence.py` |
| **`RULE-05`** | **`rule-05-academic-defense-terminology.md`** | Council defense terminology: "Low-Latency / P95 < 30ms" (ban Real-time); "Academic PoC Prototype" (ban Production-ready); "Empirical Risk Mitigation" (ban 100% safe). | `audit_anti_hallucination.py` |
| **`RULE-06`** | **`rule-06-academic-glossary-standards.md`** | Zero unexplained analogy: In-text anchoring `[[TNx]](#term-...)` and mandatory 4-column terminal glossary table for terms TN1..TN11. | `verify_academic_glossary.py` |
| **`RULE-07`** | **`rule-07-workspace-boundary-and-governance.md`** | Single repository maintainer; private local workspace excluded from Git; official read-only paths remain protected. | `audit_workspace_boundaries.py` |

---

## 3. The Four Operational Agent Roles (`.agents/roles/`)

Defined in full detail at **`.agents/roles/ROLE_DEFINITIONS.md`**:

1. 🎯 **Role 1: Academic Defense Auditor**: Hoài nghi khoa học tuyệt đối, bắt lỗi câu khẳng định thiếu dẫn chứng `[[N]](#refN)`, loại bỏ từ ngữ tuyệt đối hóa theo Rule 05.
2. 📚 **Role 2: Literature Grounding Scholar**: Bảo vệ 4 tầng xuất xứ (Four-Tier Provenance), ưu tiên tra cứu cục bộ 18 bài báo chuẩn tại `REFERENCES_LOG.md` trước khi tìm mới.
3. 🔬 **Role 3: Empirical Testbed Engineer**: Bảo chứng 100% số liệu benchmark từ các tệp JSON un-mocked trên bộ mẫu D1–D6, ngăn chặn việc tạo mô hình sớm hoặc mock dữ liệu.
4. 🚧 **Role 4: Strict Task-Scope Guardian & Milestone Boundary Controller**: Cảnh sát ranh giới nhiệm vụ; đối chiếu mã nguồn và báo cáo với file task được giao; chặn đứng hiện tượng scope creep, cấm làm việc Chapter sau khi đang ở Chapter trước. **Lưu ý**: Ranh giới nhiệm vụ không cấm đoán hoặc ngăn chặn thao tác xóa tệp, dọn dẹp thư mục hay tái cấu trúc theo yêu cầu của người dùng.

---

## 4. Mandatory Task Execution Protocol (Pre-Execution Scope Bounding)

Whenever an agent is instructed to perform a task or generate a report:
1. **Locate & Read the Task File**: Identify the exact assignment specification (e.g. `reports/tasks_for_meeting_6/README.md`).
2. **Declare Scope Boundaries**:
   - `IN-SCOPE`: Explicit questions, baseline models, and datasets required by the task.
   - `OUT-OF-SCOPE`: Future model implementations (Chapter 3/4), deprecated technologies (INT8/ONNX/ZeroQuant), and unauthorized scope expansion.
3. **Execute & Deliver Confined Output**:
   - Produce deliverables matching the task file requirements 1:1.
   - Every report must include a **Scope Boundary Declaration** section.

---

## 5. Repository Maintenance & Workspace Privacy

1. repository maintainer (`repository account`) is the sole current Git repository maintainer and the only account with GitHub write/admin access. He maintains and publishes the tracked repository updates, including reports that consolidate progress for the capstone group. Member names in those reports describe project participation, not current Git contributions. Historical commit records remain unchanged.
2. `private workspace is local-only and ignored by Git. Do not force-add its contents. Put deliverables intended for review or publication in their official tracked locations outside `private workspace
3. The former `private workspace `private workspace and `private workspace directories are retired and must not be recreated as repository workspaces.
5. Before a commit, run `python Final-Report/scripts/validate_local.py --mode fast`.

---

## 6. Safe Check Execution & Script Lifecycle

- Use a focused `scripts/<action>_<scope>.py` or `.ps1` for complex, repeated, or batch logic when it makes the inputs, path checks, dry-run, and logs easier to review. Short read-only commands may run directly.
- A script is an auditability aid; it does **not** bypass command review, approval policy, sandbox limits, or Windows execution policy. Never hide a destructive operation behind `python script.py`, another shell/language, an encoded payload, or a subprocess to evade a review decision. Review the script's effects as well as its launcher command.
- Before a destructive or batch operation, list the exact targets and expected scope, resolve paths and confirm they remain inside the authorized root, check for unexpected symlinks/reparse points, and provide a dry-run or equivalent preflight. Execute only when the task authorizes the action and the execution channel permits it.
- If command review blocks an operation, stop. Report the refusal and the verified remaining paths; do not retry through another wrapper or tool to get around the block. Continue only after the execution policy changes or the user completes the blocked action through an authorized route.
- After an operation, verify filesystem state and run the task's relevant validators before claiming success. Remove temporary scripts only after successful verification; preserve logs/manifests needed to reproduce the result.