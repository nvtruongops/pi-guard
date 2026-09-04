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
    for sub in ["work", "models", "attacks", "threat_defense", "robustness", "research", "thesis", "references", "dev", "javascripts", "stylesheets"]:
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
    # Sửa lỗi ký tự gạch chéo ngược \_ trong link URL
    content = re.sub(r"https?://[^\s\)]+", lambda m: m.group(0).replace(r"\_", "_"), content)
    # Chuẩn hóa link OWASP và ACM
    content = content.replace("https://genai.owasp.org/llm-top-10/", "https://owasp.org/www-project-top-10-for-large-language-model-applications/")
    content = content.replace("https://dl.acm.org/doi/epdf/10.1145/3724393", "https://doi.org/10.1145/3724393")

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
    """Tạo trang chủ (index.md) chuẩn mực, tối giản, thuần Markdown."""
    index_content = """# 🛡️ PI-Guard: LLM Security Guardrail

> **Đồ án Khóa luận Tốt nghiệp Đại học FPT** — Chuyên ngành An toàn Thông tin (Information Assurance)<br>
> **Mã đề tài**: `IAP491_FA26_PI_GUARD` | **Năm học**: 2026<br>
> **Chủ đề**: A Machine-Learning Guardrail for Detecting Prompt Injection and Jailbreak Attacks on LLM Applications

---

## 🎯 Giới Thiệu & Mục Tiêu Đề Tài

**PI-Guard** là hệ thống bảo vệ (guardrail) trung gian đặt trước các ứng dụng mô hình ngôn ngữ lớn (LLM), hoạt động theo cơ chế **hai tầng bảo vệ (Two-Tier Architecture)**:

1. **Tier 1 (Bộ lọc Cú pháp - Syntactic Baseline)**: Sử dụng phương pháp vector hóa TF-IDF kết hợp mô hình phân loại tuyến tính siêu nhẹ (Linear Classifier) nhằm nhận diện các mẫu prompt injection phổ biến với độ trễ cực thấp (**< 5 ms**).
2. **Tier 2 (Bộ lọc Ngữ nghĩa Sâu - Semantic Transformer)**: Sử dụng Transformer tiên tiến (**DeBERTa-v3**) với cơ chế Disentangled Attention, được lượng hóa qua **ONNX Runtime INT8** nhằm phát hiện các biến thể tấn công tinh vi, jailbreak ẩn ngữ cảnh với độ trễ mục tiêu **P95 < 15 ms**.

---

## 🌟 Sơ Đồ Luồng Phòng Thủ 2 Tầng (Mermaid)

```mermaid
flowchart TD
    UserPrompt(["📥 User Prompt"]) --> P1["⚙️ Tiền xử lý & Chuẩn hóa Unicode"]
    P1 --> T1{"⚡ Tier 1: TF-IDF Syntactic Gate"}

    T1 -- "Nguy hiểm (Score >= 0.85)" --> Block1["🚫 Chặn ngay (< 5ms)"]
    T1 -- "Lành tính (Score <= 0.15)" --> Pass1["✅ Cho phép chuyển đến LLM"]
    T1 -- "Nghi vấn (0.15 < Score < 0.85)" --> T2["🧠 Tier 2: DeBERTa-v3 Semantic Gate"]

    T2 -- "Phát hiện Injection / Jailbreak" --> Block2["🚫 Chặn tấn công ngữ nghĩa"]
    T2 -- "Lành tính an toàn" --> Pass2["✅ Chấp thuận cho phép"]

    Pass1 --> LLM["🤖 Target LLM (GPT-4o / Claude 3.5 / Gemini)"]
    Pass2 --> LLM
    LLM --> OutFilter["🔍 Output Security Guardrail"]
    OutFilter --> SafeResponse(["📤 Phản hồi an toàn đến người dùng"])

    style Block1 fill:#ff4d4f,color:#fff,stroke:#333,stroke-width:2px;
    style Block2 fill:#ff4d4f,color:#fff,stroke:#333,stroke-width:2px;
    style Pass1 fill:#52c41a,color:#fff,stroke:#333,stroke-width:2px;
    style Pass2 fill:#52c41a,color:#fff,stroke:#333,stroke-width:2px;
    style T1 fill:#1890ff,color:#fff,stroke:#333,stroke-width:2px;
    style T2 fill:#722ed1,color:#fff,stroke:#333,stroke-width:2px;
```

---

## 📋 Mục Lục Tài Liệu Toàn Dự Án

| Khu vực tài liệu | Nội dung trọng tâm | Đường dẫn tra cứu |
| **Quản Lý Công Việc** | Lộ trình IAP491, Biên bản họp 1 & 2 kèm TODO Sprint, Ma trận RACI | [Xem Biên Bản Họp 1 & Kế Hoạch Sprint](work/meeting_1.md) |
| **Chuyên Đề Tấn Công** | Lịch sử tiến hóa (2022–2026), Ranh giới In/Out-scope, Prompt Injection & 4 trường phái Jailbreak (DAN, Roleplay, VM, Cipher) | [Khám Phá Chuyên Đề Tấn Công](attacks/history_and_evolution.md) |
| **Threat Model & Phòng Thủ Đa Tầng** | NIST AI 100-2e2025, STRIDE/DREAD, 3 Lớp bảo vệ (Saltzer & Schroeder), Canary Token | [Khám Phá Threat & Defense](threat_defense/threat_model_and_attack_surface.md) |
| **Độ Bền & Lẩn Tránh (Robustness)** | Cơ chế phân mảnh BPE, Leetspeak, Base64 Unmasking, Character n-grams TF-IDF, Đột biến EasyJailbreak | [Khám Phá Chuyên Đề Robustness](robustness/theory_and_evasion_mechanisms.md) |
| **Mô Hình & Nghiên Cứu** | Toán học TF-IDF, Transformer DeBERTa-v3, Phối hợp 2 tầng, Khảo sát SOTA | [Khám Phá Mô Hình](models/two_tier_architecture.md) |
| **Luận Văn & Review 1** | Hồ sơ Threat Model (NIST), Hệ thống 3 câu hỏi IEEE (RQ1-RQ3), Dàn ý slide | [Xem Hồ Sơ Review 1](thesis/review1_threat_model.md) |
| **Tài Liệu Tham Khảo** | Nhật ký 18 bài báo khoa học chuẩn IEEE (2022–2026) kèm DOI | [Xem Thư Viện Bài Báo](references/references_log.md) |
| **Đội Ngũ & Quy Chế** | Quy chuẩn Workspace Boundary, Kiểm toán Commit tự động | [Xem Hướng Dẫn Nhóm](dev/team_governance.md) |

---

## 👥 Đội Ngũ Thực Hiện Đề Tài

> **Phương châm làm việc toàn đội**: **Ai cũng làm $\rightarrow$ Tham khảo nhau $\rightarrow$ Chốt kết quả**  
> Cả 4 thành viên đều trực tiếp thực hiện toàn trình (Full-Pipeline Hands-on) từ tiền xử lý dữ liệu, thử nghiệm Baseline ML, huấn luyện Transformer, đo đạc độ bền Evasion đến tích hợp API/Dashboard và bảo vệ Luận văn.

| STT | Thành Viên | Mã Sinh Viên | Khám Phá Toàn Trình & Đầu Mối Điều Phối |
| :---: | :--- | :---: | :--- |
| 1 | **Nguyễn Văn Trường (Leader)** | `SE182034` | **Toàn trình Full-Pipeline** — Điều phối chung, Chuẩn hóa dữ liệu & Kiến trúc |
| 2 | **Nguyễn Quí Đức** | `SE182087` | **Toàn trình Full-Pipeline** — Đối sánh mô hình Baseline ML & Threat Model |
| 3 | **Phạm Minh Hoàng Việt** | `SE181851` | **Toàn trình Full-Pipeline** — Tối ưu Transformer & Thực nghiệm Robustness |
| 4 | **Đỗ Đoàn Duy Phương** | `SE180235` | **Toàn trình Full-Pipeline** — Tích hợp hệ thống API/Dashboard & Luận văn |

**Giảng viên hướng dẫn**: Đại học FPT — Khoa An toàn Thông tin (Information Assurance).
"""
    dest = SITE_DOCS_DIR / "index.md"
    with open(dest, "w", encoding="utf-8") as f:
        f.write(index_content)
    print("✅ [HOMEPAGE] Đã sinh trang chủ index.md tối giản thành công.")

def create_static_assets():
    """Tạo các file hỗ trợ MathJax và Custom CSS tối giản."""
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

    extra_css = """/* Tối giản bảng biểu và kiểu dáng chuẩn */
.md-typeset table:not([class]) {
  border-radius: 6px;
  overflow: hidden;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
}

.md-typeset table:not([class]) th {
  background-color: rgba(63, 81, 181, 0.08);
  font-weight: 700;
}

[data-md-color-scheme="slate"] .md-typeset table:not([class]) th {
  background-color: rgba(63, 81, 181, 0.2);
}
"""
    with open(SITE_DOCS_DIR / "stylesheets" / "extra.css", "w", encoding="utf-8") as f:
        f.write(extra_css)
    print("✅ [ASSETS] Đã sinh MathJax script và custom CSS tối giản.")

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

    # 2.5. Chuyên Đề Tấn Công (Attack Study)
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "attack_study" / "00_overview_threat_and_scope" / "history_and_evolution.md",
             SITE_DOCS_DIR / "attacks" / "history_and_evolution.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "attack_study" / "00_overview_threat_and_scope" / "scope_and_boundary_analysis.md",
             SITE_DOCS_DIR / "attacks" / "scope_and_boundary_analysis.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "attack_study" / "01_prompt_injection" / "how_it_works_and_mechanisms.md",
             SITE_DOCS_DIR / "attacks" / "pi_how_it_works.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "attack_study" / "01_prompt_injection" / "taxonomy_and_variants.md",
             SITE_DOCS_DIR / "attacks" / "pi_taxonomy_and_variants.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "attack_study" / "01_prompt_injection" / "resources_and_papers.md",
             SITE_DOCS_DIR / "attacks" / "pi_resources_and_papers.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "attack_study" / "02_modern_jailbreak_attacks" / "archetypes_and_mechanisms.md",
             SITE_DOCS_DIR / "attacks" / "jb_archetypes_and_mechanisms.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "attack_study" / "02_modern_jailbreak_attacks" / "datasets_benchmarks_and_taxonomy.md",
             SITE_DOCS_DIR / "attacks" / "jb_datasets_and_benchmarks.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "attack_study" / "02_modern_jailbreak_attacks" / "advanced_variants_and_operators.md",
             SITE_DOCS_DIR / "attacks" / "jb_advanced_variants_and_operators.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "attack_study" / "02_modern_jailbreak_attacks" / "resources_and_papers.md",
             SITE_DOCS_DIR / "attacks" / "jb_resources_and_papers.md")

    # 2.6. Chuyên Đề Robustness & Evasion Study
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "robustness_study" / "01_theory_and_evasion_mechanisms.md",
             SITE_DOCS_DIR / "robustness" / "theory_and_evasion_mechanisms.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "robustness_study" / "02_defense_architecture_and_mitigation.md",
             SITE_DOCS_DIR / "robustness" / "defense_architecture_and_mitigation.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "robustness_study" / "03_benchmarks_metrics_and_tradeoffs.md",
             SITE_DOCS_DIR / "robustness" / "benchmarks_metrics_and_tradeoffs.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "robustness_study" / "04_resources_and_papers.md",
             SITE_DOCS_DIR / "robustness" / "resources_and_papers.md")

    # 2.7. Chuyên Đề Threat Model & Multi-Layer Defense Study
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "threat_and_defense_study" / "01_threat_model_and_attack_surface.md",
             SITE_DOCS_DIR / "threat_defense" / "threat_model_and_attack_surface.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "threat_and_defense_study" / "02_multi_layer_defense_architecture.md",
             SITE_DOCS_DIR / "threat_defense" / "multi_layer_defense_architecture.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "threat_and_defense_study" / "03_comparative_matrix_and_tradeoffs.md",
             SITE_DOCS_DIR / "threat_defense" / "comparative_matrix_and_tradeoffs.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "threat_and_defense_study" / "04_resources_and_papers.md",
             SITE_DOCS_DIR / "threat_defense" / "resources_and_papers.md")

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
