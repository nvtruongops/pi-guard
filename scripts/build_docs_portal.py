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
    - Chuyển đổi file:// link tuyệt đối Windows thành link markdown tương đối hoặc link code.
    - Chuẩn hóa Math block và Callouts.
    """
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
    index_content = """# 🛡️ PI-Guard Documentation Portal
## Hệ Thống Phòng Thủ Máy Học Phát Hiện Tấn Công Prompt Injection & Jailbreak Cho Các Ứng Dụng LLM

<div class="grid cards" markdown>

-   :material-shield-check:{ .lg .middle } __Kiến Trúc 2 Tầng (Two-Tier Defense)__

    ---

    Kết hợp bộ lọc cú pháp siêu tốc **Tier 1 (TF-IDF + Linear Classifier)** độ trễ < 5ms với mô hình ngữ nghĩa sâu **Tier 2 (DeBERTa-v3)** phát hiện tấn công tiềm ẩn.

    [:octicons-arrow-right-24: Khám phá mô hình](models/two_tier_architecture.md)

-   :material-calendar-clock:{ .lg .middle } __Quản Lý Công Việc & Tiến Độ Tuần__

    ---

    Biên bản họp tuần, phân bổ nhiệm vụ chi tiết theo ngày (Daily TODOs), ma trận trách nhiệm RACI và checklist kiểm toán Process Report chuẩn FPT.

    [:octicons-arrow-right-24: Xem kế hoạch Sprint](work/sprint_1_todo_list.md)

-   :material-book-education:{ .lg .middle } __Luận Văn & Hồ Sơ Review 1__

    ---

    Hồ sơ bảo vệ Review 1: Phát biểu bài toán, Mô hình đe dọa (NIST AI 100-2e2025), Hệ thống 3 câu hỏi nghiên cứu IEEE (RQ1-RQ3) và Slide thuyết trình.

    [:octicons-arrow-right-24: Đọc hồ sơ Review 1](thesis/review1_threat_model.md)

-   :material-database-search:{ .lg .middle } __Khảo Sát SOTA & 18 Bài Báo IEEE__

    ---

    Đối chuẩn chuyên sâu với ProtectAI DeBERTa, Meta Llama Guard, NVIDIA NeMo Guardrails và nhật ký 18 bài báo khoa học xuất bản 2022-2026.

    [:octicons-arrow-right-24: Tra cứu thư viện bài báo](references/references_log.md)

</div>

---

### 🌟 Sơ Đồ Kiến Trúc Luồng Phòng Thủ PI-Guard (Mermaid)

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

### 👥 Đội Ngũ Thực Hiện Đề Tài (Capstone Project Team)

| STT | Thành Viên | Mã Sinh Viên | Vai Trò & Phân Công Trọng Tâm |
| :---: | :--- | :---: | :--- |
| 1 | **Nguyễn Văn Trường (Leader)** | `SE182034` | **Kiến trúc Hệ thống & Kỹ thuật Dữ liệu** — Điều phối chung, Data Curation, Threat Model, Merge Code |
| 2 | **Nguyễn Quí Đức** | `SE182087` | **Mô hình Máy học Baseline** — TF-IDF Vectorizer, Linear Classifier, Attack Surface, Robustness |
| 3 | **Phạm Minh Hoàng Việt** | `SE181851` | **Transformer & Tối ưu hóa** — DeBERTa-v3 Fine-tuning, INT8 Quantization ONNX, Target LLM Benchmark |
| 4 | **Đỗ Đoàn Duy Phương** | `SE180235` | **API Middleware & Luận văn** — FastAPI Proxy, Streamlit Dashboard, Báo cáo Chapter 1-2 & Slide PPT |

**Giảng viên hướng dẫn (Supervisor)**: Đại học FPT — Khoa An toàn Thông tin (Information Assurance).

---

### 📊 Chỉ Số Tiến Độ & Quy Chuẩn Thực Hiện

- **Mã Đồ Án**: `IAP491_FA26_PI_GUARD`
- **Mục tiêu Review 1**: Hoàn thành 100% Chapter 1 (Introduction), Chapter 2 (Literature Review), Threat Model & Slide thuyết trình.
- **Tài liệu tham khảo**: 18 bài báo khoa học chuẩn IEEE/ACM (100% từ năm 2022 đến 2026).
- **Mã nguồn**: Quản trị nghiêm ngặt theo mô hình Workspace Boundary (`workspaces/<member>/`) với kiểm toán commit tự động.
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

/* Thẻ card và bo tròn */
.md-typeset .grid.cards > ul > li {
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.md-typeset .grid.cards > ul > li:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(63, 81, 181, 0.15);
}

/* Table đẹp hơn */
.md-typeset table:not([class]) {
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.md-typeset table:not([class]) th {
  background-color: rgba(63, 81, 181, 0.08);
  color: #1a237e;
  font-weight: 600;
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
