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

## Parallel Full-Pipeline Exploration & Knowledge Convergence Paradigm

All 4 members work hands-on across the entire pipeline in parallel workspaces (`workspaces/<member>/`) and converge findings during weekly meetings:

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
   - All commits and PRs must pass `python scripts/audit_workspace_boundaries.py`.
   - Pre-commit hook (`scripts/audit_workspace_boundaries.py --install-hook`) must be installed on all member environments.

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
