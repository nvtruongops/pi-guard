"""
scripts/build_docs_portal.py
-----------------------------
PI-Guard Documentation Portal Aggregator
Tự động thu thập, chuẩn hóa và cấu trúc tài liệu toàn dự án PI-Guard
thành thư mục 'site_docs/' để phục vụ xuất bản Web UI qua MkDocs Material.

Quy tắc bảo vệ:
- KHÔNG BAO GIỜ chỉnh sửa hoặc copy tài liệu nội bộ trong docs/fpt_capstone_guide/.
- Giữ nguyên vẹn file gốc trong Meeting/, workspaces/, References/, docs/.
"""

import re
import shutil
import sys
from pathlib import Path

# Đảm bảo in tiếng Việt và unicode an toàn trên Windows terminal
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Root project directory
ROOT_DIR = Path(__file__).resolve().parent.parent
SITE_DOCS_DIR = ROOT_DIR / "site_docs"

def clean_and_prepare_dir():
    """Khởi tạo lại thư mục site_docs sạch sẽ."""
    if SITE_DOCS_DIR.exists():
        shutil.rmtree(SITE_DOCS_DIR)
    SITE_DOCS_DIR.mkdir(parents=True, exist_ok=True)

    # Tạo các thư mục con theo kiến trúc thông tin (IA)
    for sub in ["work", "models", "research", "thesis", "references", "dev", "javascripts", "stylesheets"]:
        (SITE_DOCS_DIR / sub).mkdir(parents=True, exist_ok=True)
    print(f"📁 [INIT] Đã khởi tạo cấu trúc thư mục tại: {SITE_DOCS_DIR}")

def sanitize_content(content: str) -> str:
    """
    Chuẩn hóa nội dung markdown:
    - Loại bỏ triệt để mọi liên kết hoặc đề cập đến tài liệu bảo mật nội bộ (docs/fpt_capstone_guide).
    - Chuyển đổi file:// link tuyệt đối Windows thành link markdown tương đối hoặc link code.
    - Chuẩn hóa Math block và Callouts.
    """
    # Lọc bỏ các dòng chứa tài liệu bảo mật nội bộ
    sanitized_lines = []
    for line in content.splitlines():
        if "fpt_capstone_guide" in line or "SP26IA04" in line:
            continue
        sanitized_lines.append(line)
    content = "\n".join(sanitized_lines)

    # Thay thế file:///d:/Work/Do-an/... hoặc file:///D:/Work/Do-an/...
    content = re.sub(r"\[([^\]]+)\]\(file:///[dD]:/Work/Do-an/([^)]+)\)", r"[\1](\2)", content)
    # Thay thế file:///... còn lại
    content = re.sub(r"\(file:///[^)]+\)", r"(#)", content)

    # Chuẩn hóa callout kiểu GitHub (> [!NOTE]) thành MkDocs Admonition (!!! note)
    # MkDocs Material hỗ trợ cả 2 qua extension pymdownx.details / admonition
    return content

def copy_doc(src_path: Path, dest_path: Path, title_prefix: str = ""):
    """Đọc file nguồn, chuẩn hóa link và ghi vào thư mục site_docs."""
    if not src_path.exists():
        print(f"⚠️ [SKIP] Không tìm thấy file: {src_path}")
        return False

    try:
        with open(src_path, encoding="utf-8") as f:
            content = f.read()

        content = sanitize_content(content)
        if title_prefix:
            content = f"{title_prefix}\n\n" + content

        dest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(dest_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ [COPY] {src_path.name} -> {dest_path.relative_to(ROOT_DIR)}")
        return True
    except Exception as e:
        print(f"❌ [ERROR] Lỗi khi copy {src_path}: {e}")
        return False

def create_homepage():
    """Tạo trang chủ (index.md) với thiết kế trực quan, hiện đại, rich visuals."""
    index_content = """# PI-Guard Documentation Portal

<div class="hero-container">
  <div class="hero-badge">🎓 FPT UNIVERSITY • CAPSTONE PROJECT IAP491</div>
  <h1 class="hero-title">PI-GUARD: LLM SECURITY GUARDRAIL</h1>
  <p class="hero-subtitle">
    Hệ thống phòng thủ máy học 2 tầng (Two-Tier ML Guardrail) đặt trước các ứng dụng Large Language Model (LLM) nhằm phát hiện và ngăn chặn tấn công <strong>Prompt Injection</strong> và <strong>Jailbreak</strong> với độ trễ thấp và tỷ lệ cảnh báo sai tối thiểu.
  </p>
  <div class="hero-actions">
    <a href="work/sprint_1_todo_list/" class="btn-primary">📋 Kế Hoạch Sprint Tuần</a>
    <a href="models/two_tier_architecture/" class="btn-secondary">⚡ Kiến Trúc 2 Tầng</a>
    <a href="thesis/review1_threat_model/" class="btn-secondary">🛡️ Hồ Sơ Review 1</a>
  </div>
</div>

<div class="metrics-grid">
  <div class="metric-card">
    <div class="metric-icon">⚡</div>
    <div class="metric-value">Two-Tier</div>
    <div class="metric-label">Phòng thủ Cú pháp & Ngữ nghĩa</div>
  </div>
  <div class="metric-card">
    <div class="metric-icon">⏱️</div>
    <div class="metric-value">&lt; 15 ms</div>
    <div class="metric-label">Mục tiêu Độ trễ P95 (ONNX INT8)</div>
  </div>
  <div class="metric-card">
    <div class="metric-icon">📚</div>
    <div class="metric-value">18 Papers</div>
    <div class="metric-label">Tài liệu tham khảo IEEE (2022-2026)</div>
  </div>
  <div class="metric-card">
    <div class="metric-icon">👥</div>
    <div class="metric-value">4 Members</div>
    <div class="metric-label">Đội ngũ An toàn Thông tin FPT</div>
  </div>
</div>

## 📂 Danh Mục Tài Liệu Trọng Tâm

<div class="portal-grid">
  <a href="work/sprint_1_todo_list/" class="portal-card">
    <div class="portal-card-header">
      <span class="portal-card-tag tag-work">QUẢN LÝ CÔNG VIỆC</span>
    </div>
    <h3 class="portal-card-title">📋 Tiến Độ & Kế Hoạch Sprint</h3>
    <p class="portal-card-desc">
      Biên bản họp tuần với GVHD, bảng phân rã nhiệm vụ chi tiết theo ngày (Daily Timeline), ma trận trách nhiệm RACI và checklist tự kiểm toán Process Report.
    </p>
    <div class="portal-card-footer">Xem chi tiết &rarr;</div>
  </a>

  <a href="models/two_tier_architecture/" class="portal-card">
    <div class="portal-card-header">
      <span class="portal-card-tag tag-ai">MÔ HÌNH MÁY HỌC</span>
    </div>
    <h3 class="portal-card-title">🧠 Kiến Trúc Phòng Thủ 2 Tầng</h3>
    <p class="portal-card-desc">
      Toán học & cách triển khai Tier 1 (TF-IDF + Linear Classifier độ trễ &lt; 5ms) kết hợp Tier 2 (DeBERTa-v3 Disentangled Attention) lượng hóa ONNX INT8.
    </p>
    <div class="portal-card-footer">Xem chi tiết &rarr;</div>
  </a>

  <a href="thesis/review1_threat_model/" class="portal-card">
    <div class="portal-card-header">
      <span class="portal-card-tag tag-thesis">LUẬN VĂN & REVIEW 1</span>
    </div>
    <h3 class="portal-card-title">🛡️ Threat Model & Defense</h3>
    <p class="portal-card-desc">
      Hồ sơ bảo vệ Review 1: Phát biểu bài toán, mô hình đe dọa (NIST AI 100-2e2025), hệ thống 3 câu hỏi nghiên cứu IEEE (RQ1-RQ3) và slide thuyết trình.
    </p>
    <div class="portal-card-footer">Xem chi tiết &rarr;</div>
  </a>

  <a href="references/references_log/" class="portal-card">
    <div class="portal-card-header">
      <span class="portal-card-tag tag-ref">TÀI LIỆU KHOA HỌC</span>
    </div>
    <h3 class="portal-card-title">📚 18 Bài Báo IEEE Đỉnh Cao</h3>
    <p class="portal-card-desc">
      Nhật ký 18 công trình nghiên cứu hàng đầu thế giới (100% từ năm 2022-2026) kèm liên kết DOI/arXiv và ma trận ánh xạ vào 6 chương của luận văn.
    </p>
    <div class="portal-card-footer">Xem chi tiết &rarr;</div>
  </a>
</div>

---

## 🌟 Sơ Đồ Luồng Phòng Thủ 2 Tầng (Two-Tier Guardrail Pipeline)

```mermaid
flowchart TD
    UserPrompt(["📥 User Prompt"]) --> P1["⚙️ Tiền xử lý & Chuẩn hóa Unicode"]
    P1 --> T1{"⚡ Tier 1: TF-IDF Syntactic Gate"}

    T1 -- "Nguy hiểm rõ ràng (Score >= 0.85)" --> Block1["🚫 CHẶN NGAY LẬP TỨC (Latency < 5ms)"]
    T1 -- "Lành tính tuyệt đối (Score <= 0.15)" --> Pass1["✅ Chuyển thẳng đến Target LLM"]
    T1 -- "Vùng nghi vấn (0.15 < Score < 0.85)" --> T2["🧠 Tier 2: DeBERTa-v3 Semantic Analysis"]

    T2 -- "Phát hiện Prompt Injection / Jailbreak" --> Block2["🚫 CHẶN TẤN CÔNG NGỮ NGHĨA"]
    T2 -- "Lành tính an toàn" --> Pass2["✅ CHẤP THUẬN CHO PHÉP"]

    Pass1 --> LLM["🤖 Target LLM (GPT-4o / Claude 3.5 / Gemini)"]
    Pass2 --> LLM
    LLM --> OutFilter["🔍 Output Security Guardrail"]
    OutFilter --> SafeResponse(["📤 Safe Response To User"])

    style Block1 fill:#ff4d4f,color:#fff,stroke:#333,stroke-width:2px;
    style Block2 fill:#ff4d4f,color:#fff,stroke:#333,stroke-width:2px;
    style Pass1 fill:#52c41a,color:#fff,stroke:#333,stroke-width:2px;
    style Pass2 fill:#52c41a,color:#fff,stroke:#333,stroke-width:2px;
    style T1 fill:#1890ff,color:#fff,stroke:#333,stroke-width:2px;
    style T2 fill:#722ed1,color:#fff,stroke:#333,stroke-width:2px;
```

---

## 👥 Đội Ngũ Thực Hiện Đề Tài (Capstone Team)

| STT | Thành Viên | Mã Sinh Viên | Vai Trò & Phân Công Trọng Tâm |
| :---: | :--- | :---: | :--- |
| 1 | **Nguyễn Văn Trường (Leader)** | `SE182034` | **Kiến trúc Hệ thống & Kỹ thuật Dữ liệu** — Điều phối chung, Data Curation, Threat Model, Merge Code |
| 2 | **Nguyễn Quí Đức** | `SE182087` | **Mô hình Máy học Baseline** — TF-IDF Vectorizer, Linear Classifier, Attack Surface, Robustness |
| 3 | **Phạm Minh Hoàng Việt** | `SE181851` | **Transformer & Tối ưu hóa** — DeBERTa-v3 Fine-tuning, INT8 Quantization ONNX, Target LLM Benchmark |
| 4 | **Đỗ Đoàn Duy Phương** | `SE180235` | **API Middleware & Luận văn** — FastAPI Proxy, Streamlit Dashboard, Báo cáo Chapter 1-2 & Slide PPT |

**Giảng viên hướng dẫn (Supervisor)**: Đại học FPT — Khoa An toàn Thông tin (Information Assurance).
"""
    dest = SITE_DOCS_DIR / "index.md"
    with open(dest, "w", encoding="utf-8") as f:
        f.write(index_content)
    print("✅ [HOMEPAGE] Đã sinh trang chủ index.md thành công.")

def create_static_assets():
    """Tạo các file hỗ trợ MathJax và Custom CSS."""
    mathjax_js = """window.MathJax = {
  tex: {
    inlineMath: [["\\\\(", "\\\\)"]],
    displayMath: [["\\\\[", "\\\\]"]],
    processEscapes: true,
    processEnvironments: true
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex"
  }
};

document$.subscribe(() => {
  MathJax.typesetPromise()
})
"""
    with open(SITE_DOCS_DIR / "javascripts" / "mathjax.js", "w", encoding="utf-8") as f:
        f.write(mathjax_js)

    extra_css = """:root {
  --md-primary-fg-color: #3f51b5;
  --md-accent-fg-color: #7b1fa2;
}

/* ===== HERO CONTAINER ===== */
.hero-container {
  background: linear-gradient(135deg, rgba(63, 81, 181, 0.1) 0%, rgba(123, 31, 162, 0.12) 100%);
  border: 1px solid rgba(63, 81, 181, 0.25);
  border-radius: 16px;
  padding: 2.5rem 2rem;
  margin: 1.5rem 0 2rem 0;
  text-align: center;
  box-shadow: 0 8px 32px rgba(63, 81, 181, 0.08);
}

.hero-badge {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  padding: 0.35rem 1rem;
  border-radius: 999px;
  background: rgba(63, 81, 181, 0.15);
  color: var(--md-primary-fg-color);
  margin-bottom: 1rem;
  border: 1px solid rgba(63, 81, 181, 0.3);
}

.hero-title {
  font-size: 2.2rem !important;
  font-weight: 800 !important;
  letter-spacing: -0.02em;
  margin: 0.5rem 0 1rem 0 !important;
  background: linear-gradient(135deg, #1a237e 0%, #4a148c 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

[data-md-color-scheme="slate"] .hero-title {
  background: linear-gradient(135deg, #7986cb 0%, #ce93d8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-subtitle {
  font-size: 1.05rem;
  line-height: 1.6;
  max-width: 800px;
  margin: 0 auto 1.8rem auto;
  color: var(--md-default-fg-color--light);
}

.hero-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.65rem 1.4rem;
  background: #3f51b5;
  color: #ffffff !important;
  font-weight: 600;
  border-radius: 8px;
  text-decoration: none !important;
  box-shadow: 0 4px 14px rgba(63, 81, 181, 0.35);
  transition: all 0.2s ease;
}

.btn-primary:hover {
  background: #303f9f;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(63, 81, 181, 0.45);
}

.btn-secondary {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.65rem 1.4rem;
  background: var(--md-default-bg-color);
  color: var(--md-default-fg-color) !important;
  font-weight: 600;
  border-radius: 8px;
  border: 1px solid var(--md-default-fg-color--lighter);
  text-decoration: none !important;
  transition: all 0.2s ease;
}

.btn-secondary:hover {
  border-color: #3f51b5;
  color: #3f51b5 !important;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

/* ===== METRICS GRID ===== */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2.5rem;
}

.metric-card {
  background: var(--md-default-bg-color);
  border: 1px solid var(--md-default-fg-color--lightest);
  border-radius: 12px;
  padding: 1.2rem 1rem;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  transition: transform 0.2s ease;
}

.metric-card:hover {
  transform: translateY(-3px);
  border-color: rgba(63, 81, 181, 0.4);
}

.metric-icon {
  font-size: 1.6rem;
  margin-bottom: 0.3rem;
}

.metric-value {
  font-size: 1.4rem;
  font-weight: 800;
  color: #3f51b5;
}

[data-md-color-scheme="slate"] .metric-value {
  color: #9fa8da;
}

.metric-label {
  font-size: 0.8rem;
  color: var(--md-default-fg-color--light);
  margin-top: 0.2rem;
}

/* ===== PORTAL FEATURE CARDS ===== */
.portal-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin: 1.5rem 0 2.5rem 0;
}

.portal-card {
  background: var(--md-default-bg-color);
  border: 1px solid var(--md-default-fg-color--lightest);
  border-radius: 14px;
  padding: 1.5rem;
  text-decoration: none !important;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}

.portal-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 28px rgba(63, 81, 181, 0.15);
  border-color: #3f51b5;
}

.portal-card-header {
  margin-bottom: 0.75rem;
}

.portal-card-tag {
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  padding: 0.2rem 0.6rem;
  border-radius: 4px;
}

.tag-work { background: rgba(33, 150, 243, 0.12); color: #1976d2; }
.tag-ai { background: rgba(156, 39, 176, 0.12); color: #7b1fa2; }
.tag-thesis { background: rgba(76, 175, 80, 0.12); color: #388e3c; }
.tag-ref { background: rgba(255, 152, 0, 0.12); color: #f57c00; }

.portal-card-title {
  font-size: 1.15rem !important;
  font-weight: 700 !important;
  margin: 0 0 0.5rem 0 !important;
  color: var(--md-default-fg-color) !important;
}

.portal-card-desc {
  font-size: 0.9rem;
  line-height: 1.5;
  color: var(--md-default-fg-color--light);
  margin-bottom: 1.2rem;
  flex-grow: 1;
}

.portal-card-footer {
  font-size: 0.85rem;
  font-weight: 700;
  color: #3f51b5;
  display: flex;
  align-items: center;
}

/* ===== TABLE STYLING ===== */
.md-typeset table:not([class]) {
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04);
}

.md-typeset table:not([class]) th {
  background-color: rgba(63, 81, 181, 0.08);
  color: #1a237e;
  font-weight: 700;
}

[data-md-color-scheme="slate"] .md-typeset table:not([class]) th {
  background-color: rgba(63, 81, 181, 0.2);
  color: #c5cae9;
}
"""
    with open(SITE_DOCS_DIR / "stylesheets" / "extra.css", "w", encoding="utf-8") as f:
        f.write(extra_css)
    print("✅ [ASSETS] Đã sinh MathJax script và custom CSS.")

def aggregate_all():
    """Thu thập toàn bộ tài nguyên vào site_docs/."""
    clean_and_prepare_dir()
    create_homepage()
    create_static_assets()

    # 1. Quản lý công việc & Tiến độ
    copy_doc(ROOT_DIR / "docs" / "thesis" / "FPT_IAP491_Capstone_Guidelines_and_Rubrics_Summary.md",
             SITE_DOCS_DIR / "work" / "fpt_guidelines_and_rubrics.md")
    copy_doc(ROOT_DIR / "Meeting" / "Meeting 1_29_08_26.md",
             SITE_DOCS_DIR / "work" / "meeting_1.md")
    copy_doc(ROOT_DIR / "Meeting" / "Meeting 2_01_09_26.md",
             SITE_DOCS_DIR / "work" / "meeting_2.md")
    copy_doc(ROOT_DIR / "Meeting" / "Meeting_1_TODO_List_30_08_to_06_09_2026.md",
             SITE_DOCS_DIR / "work" / "sprint_1_todo_list.md")
    copy_doc(ROOT_DIR / "Meeting" / "PROCESS_REPORT_CHECKLIST.md",
             SITE_DOCS_DIR / "work" / "process_report_checklist.md")

    # 2. Mô hình & Nghiên cứu AI
    # Model Study
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "model_study" / "03_two_tier_pipeline_coordination" / "how_it_works_and_architecture.md",
             SITE_DOCS_DIR / "models" / "two_tier_architecture.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "model_study" / "03_two_tier_pipeline_coordination" / "benchmark_and_tradeoffs.md",
             SITE_DOCS_DIR / "models" / "two_tier_tradeoffs.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "model_study" / "01_tfidf_syntactic_baseline" / "theory_and_math.md",
             SITE_DOCS_DIR / "models" / "tfidf_theory_and_math.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "model_study" / "01_tfidf_syntactic_baseline" / "how_it_works_and_usage.md",
             SITE_DOCS_DIR / "models" / "tfidf_usage.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "model_study" / "01_tfidf_syntactic_baseline" / "resources_and_videos.md",
             SITE_DOCS_DIR / "models" / "tfidf_resources.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "model_study" / "02_deberta_v3_semantic_classifier" / "theory_and_math.md",
             SITE_DOCS_DIR / "models" / "deberta_theory_and_math.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "model_study" / "02_deberta_v3_semantic_classifier" / "how_it_works_and_usage.md",
             SITE_DOCS_DIR / "models" / "deberta_usage.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "model_study" / "02_deberta_v3_semantic_classifier" / "resources_and_videos.md",
             SITE_DOCS_DIR / "models" / "deberta_resources.md")

    # Research
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "State_of_the_Art_Guardrail_and_Jailbreak_Benchmarks_Analysis.md",
             SITE_DOCS_DIR / "research" / "sota_guardrail_benchmarks.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "Target_LLM_API_Benchmark_and_Vulnerability_Analysis.md",
             SITE_DOCS_DIR / "research" / "target_llm_vulnerabilities.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "Tencent2026_Paper_Analysis_and_Mapping_to_PIGuard.md",
             SITE_DOCS_DIR / "research" / "tencent2026_paper_analysis.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "Why_Dual_Model_Architecture_TFIDF_and_DeBERTaV3.md",
             SITE_DOCS_DIR / "research" / "why_dual_model_architecture.md")

    # 3. Luận văn & Báo cáo Review
    copy_doc(ROOT_DIR / "CAPSTONE PROJECT REGISTER.md",
             SITE_DOCS_DIR / "thesis" / "capstone_register.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "thesis" / "Review1_Problem_Definition_and_Threat_Model.md",
             SITE_DOCS_DIR / "thesis" / "review1_threat_model.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "thesis" / "Review1_Presentation_Slides_Outline.md",
             SITE_DOCS_DIR / "thesis" / "review1_slides_outline.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "thesis" / "chapters" / "01_Introduction.md",
             SITE_DOCS_DIR / "thesis" / "chapter_01_introduction.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "thesis" / "chapters" / "02_Literature_Review.md",
             SITE_DOCS_DIR / "thesis" / "chapter_02_literature_review.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "thesis" / "FINAL_THESIS.md",
             SITE_DOCS_DIR / "thesis" / "final_thesis.md")

    # 4. Thư viện bài báo khoa học
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "References" / "REFERENCES_LOG.md",
             SITE_DOCS_DIR / "references" / "references_log.md")

    # 5. Đội ngũ & Hướng dẫn kỹ thuật
    copy_doc(ROOT_DIR / "AGENTS.md",
             SITE_DOCS_DIR / "dev" / "team_governance.md")
    copy_doc(ROOT_DIR / "CONTRIBUTING.md",
             SITE_DOCS_DIR / "dev" / "contributing_guide.md")
    copy_doc(ROOT_DIR / "workspaces" / "README.md",
             SITE_DOCS_DIR / "dev" / "workspaces_overview.md")
    copy_doc(ROOT_DIR / "src" / "README.md",
             SITE_DOCS_DIR / "dev" / "src_architecture.md")

    print("\n🎉 [HOÀN TẤT] Toàn bộ tài liệu đã được chuẩn hóa và sẵn sàng cho MkDocs build!")

if __name__ == "__main__":
    aggregate_all()
