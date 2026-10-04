"""
scripts/build_docs_portal.py
-----------------------------
PI-Guard documentation portal builder
Tự động thu thập, chuẩn hóa và cấu trúc tài liệu toàn dự án PI-Guard
thành thư mục 'docs/' để phục vụ xuất bản Web UI qua GitHub Pages (MkDocs Material).

Quy tắc bảo vệ:
- KHÔNG BAO GIỜ chỉnh sửa hoặc xóa tài liệu nội bộ trong docs/fpt_capstone_guide/.
- Giữ nguyên vẹn file gốc trong reports/Meeting/, workspaces/, reports/References/, docs/.
"""

import re
import sys
from pathlib import Path

# Đảm bảo in tiếng Việt và unicode an toàn trên Windows terminal
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Root project directory
FINAL_REPORT_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = FINAL_REPORT_DIR.parent
DOCS_DIR = ROOT_DIR / "Github-Page"

def clean_and_prepare_dir():
    """Create portal folders without deleting existing checked-in pages or assets."""
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    subdirs = [
        "work", "prompt_study", "attacks", "threat_defense",
        "dataset_study", "models", "robustness",
        "evaluation_study", "research", "thesis", "references",
        "dev", "javascripts", "stylesheets", "assets",
    ]
    for sub in subdirs:
        (DOCS_DIR / sub).mkdir(parents=True, exist_ok=True)

    print(f"📁 [INIT] Portal folders ready; existing pages are preserved: {DOCS_DIR}")

def sanitize_content(content: str) -> str:
    """
    Chuẩn hóa nội dung markdown:
    - Loại bỏ triệt để mọi liên kết hoặc đề cập đến tài liệu bảo mật nội bộ (docs/fpt_capstone_guide).
    - Chuyển đổi file:// link tuyệt đối Windows thành văn bản chuẩn hoặc link hợp lệ.
    - Chuẩn hóa Math block và Callouts.
    - Loại bỏ emoji rườm rà ở tiêu đề đề mục.
    """
    sanitized_lines = []
    for line in content.splitlines():
        if "fpt_capstone_guide" in line or "SP26IA04" in line:
            continue
        # Loại bỏ emoji trang trí ở đầu tiêu đề markdown (# 🛡️ -> # )
        line = re.sub(r'^(#{1,6})\s*[\U00010000-\U0010ffff\u2600-\u27bf\u2300-\u23ff\u2b00-\u2bff\ufe00-\ufe0f\s]*[\U00010000-\U0010ffff\u2600-\u27bf\u2300-\u23ff\u2b00-\u2bff\ufe00-\ufe0f]\s*', r'\1 ', line)
        sanitized_lines.append(line)
    content = "\n".join(sanitized_lines)

    # Source reports and the generated portal have different relative link roots.
    content = content.replace("(REFERENCES_LOG.md)", "(references_log.md)")
    content = content.replace("(../../Github-Page/", "(../")

    # Chuyển đổi link PDF nội bộ và link file ngoài thành inline code hoặc text đậm
    content = re.sub(r"\[([^\]]+)\]\((?:file:///[^)]*|Final-Report(?:/[^)]*)?|workspaces(?:/[^)]*)?|reports/(?:References|Meeting)/[^)]*|References/[^)]*|Meeting/[^)]*|CAPSTONE%20PROJECT%20REGISTER\.md|Github-Page/[^)]*|docs/[^)]*)\)", r"**\1**", content)

    content = re.sub(r"\[([^\]]+)\]\((?!https?://|mailto:|#)[^)]*\.pdf(?:#[^)]*)?\)", r"**\1** (local PDF; not packaged with portal)", content, flags=re.IGNORECASE)
    # Thay thế file:///... còn lại
    content = re.sub(r"\(file:///[^)]+\)", r"(#)", content)
    content = re.sub(r"file:///[^\s\)\"\'>]+", "#", content)

    # Sửa lỗi ký tự gạch chéo ngược \_ trong link URL
    content = re.sub(r"https?://[^\s\)]+", lambda m: m.group(0).replace(r"\_", "_"), content)
    content = content.replace("https://genai.owasp.org/llm-top-10/", "https://owasp.org/www-project-top-10-for-large-language-model-applications/")
    content = content.replace("https://dl.acm.org/doi/epdf/10.1145/3724393", "https://doi.org/10.1145/3724393")

    # =========================================================================
    # TUÂN THỦ QUY CHUẨN KIẾN TRÚC & LOẠI TRỪ (ARCHITECTURAL DEPRECATIONS):
    # Thay thế các thuật ngữ INT8 / ONNX cũ thành Native FP32 theo quy chuẩn Meeting 6
    # =========================================================================
    content = re.sub(r"DeBERTa-v3\s+INT8\s+Transformer", "DeBERTa-v3 Native FP32 Transformer", content)
    content = re.sub(r"Adversarially Augmented DeBERTa-v3 INT8", "Adversarially Augmented DeBERTa-v3 Native FP32", content)
    content = re.sub(r"DeBERTa-v3\s+INT8", "DeBERTa-v3 Native FP32", content)
    content = re.sub(r"DeBERTa\s+INT8", "DeBERTa Native FP32", content)
    content = re.sub(r"DeBERTa-v3\s*\(đã lượng hóa INT8\)", "DeBERTa-v3 (Native FP32 CPU)", content)
    content = re.sub(r"Fine-tuned DeBERTa-v3 Base \(ONNX INT8\)", "Fine-tuned DeBERTa-v3 Base (Native FP32)", content)
    content = re.sub(r"ONNX Runtime INT8 \(Yao et al\., NeurIPS 2022\)", "PyTorch Native FP32 CPU Inference (He et al., ICLR 2023)", content)
    content = re.sub(r"\|\s*`Final-Report/src/models/classifier\.py`\s*\|\s*Mô hình phân loại 2 tầng:\s*Hybrid TF-IDF \+ DeBERTa INT8\s*\|\s*He et al\. \(ICLR 2023\) & Yao et al\. \(NeurIPS 2022\)\s*\|",
                     "| `Final-Report/src/models/classifier.py` | Mô hình phân loại 2 tầng: Hybrid TF-IDF + DeBERTa FP32 | He et al. (ICLR 2023) |", content)
    content = re.sub(r"ONNX Runtime INT8 đóng vai trò là giải pháp kỹ thuật phụ trợ triển khai giúp hệ thống chạy mượt trên CPU thông thường\.",
                     "PyTorch Native FP32 đóng vai trò là giải pháp kiến trúc cốt lõi giúp hệ thống chạy mượt trên CPU thông thường với độ trễ thấp.", content)
    content = re.sub(r"lượng hóa động ONNX INT8 Runtime chạy tối ưu trên CPU", "tối ưu phân bổ luồng PyTorch Native FP32 chạy hiệu quả trên CPU", content)
    content = re.sub(r"lượng hóa nhẹ ONNX Runtime INT8 cho suy luận CPU", "tối ưu hóa luồng PyTorch Native FP32 cho suy luận CPU", content)
    content = re.sub(r"lượng hóa ONNX INT8", "tối ưu Native FP32 CPU", content)
    content = re.sub(r"ONNX INT8 Runtime", "PyTorch Native FP32 Runtime", content)
    content = re.sub(r"ONNX Runtime INT8", "PyTorch Native FP32", content)
    content = re.sub(r"ONNX INT8", "Native FP32", content)
    content = re.sub(r"~15 MB \(TF\) \+ 140 MB \(INT8\)", "~15 MB (TF) + ~440 MB (FP32)", content)
    content = re.sub(r"<\s*150\s*MB\s*\(ONNX INT8\)", "< 500MB (Native FP32)", content)

    return content

def copy_doc(src_path: Path, dest_path: Path, title_prefix: str = ""):
    """Đọc nguồn tracked, chuẩn hóa link và ghi vào thư mục docs."""
    try:
        source_relative = src_path.resolve().relative_to(ROOT_DIR.resolve())
    except ValueError:
        source_relative = None
    if source_relative and source_relative.parts[0].lower() == "workspaces":
        print(f"🔒 [PRIVATE] Giữ nguyên trang đã kiểm tra; không đồng bộ trực tiếp từ workspace: {src_path}")
        return False

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
    """Preserve the checked-in portal home page maintained at Github-Page/index.md."""
    dest = DOCS_DIR / "index.md"
    if not dest.is_file():
        raise FileNotFoundError(f"Required checked-in portal homepage is missing: {dest}")
    print("✅ [HOMEPAGE] Preserved checked-in Github-Page/index.md.")


def create_static_assets():
    """Tạo các file hỗ trợ MathJax và Custom CSS tối giản."""
    image_dir = DOCS_DIR / "assets"
    image_dir.mkdir(parents=True, exist_ok=True)
    published_image = image_dir / "ingress_architecture_review1_summary_vertical.png"
    if published_image.is_file():
        print(f"✅ [ASSETS] Preserved checked-in portal image: {published_image}")
    else:
        print(f"⚠️ [ASSETS] Checked-in architecture image is missing: {published_image}")
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
    with open(DOCS_DIR / "javascripts" / "mathjax.js", "w", encoding="utf-8") as f:
        f.write(mathjax_js)

    extra_css = """/* Tối giản bảng biểu và kiểu dáng chuẩn */
.md-typeset table:not([class]) {
  border-radius: 6px;
  overflow: hidden;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
  display: table;
  width: 100%;
}

.md-typeset table:not([class]) th {
  background-color: rgba(63, 81, 181, 0.08);
  font-weight: 700;
}

[data-md-color-scheme="slate"] .md-typeset table:not([class]) th {
  background-color: rgba(63, 81, 181, 0.2);
}

.md-typeset .mermaid {
  display: flex;
  justify-content: center;
  margin: 1.5em 0;
  background-color: transparent;
}
"""
    with open(DOCS_DIR / "stylesheets" / "extra.css", "w", encoding="utf-8") as f:
        f.write(extra_css)
    print("✅ [ASSETS] Đã sinh MathJax script và custom CSS tối giản.")

def aggregate_all():
    """Thu thập toàn bộ tài nguyên vào docs/."""
    clean_and_prepare_dir()
    create_homepage()
    create_static_assets()

    # 1. Quản lý công việc & Tiến độ
    copy_doc(ROOT_DIR / "Final-Report" / "thesis" / "FPT_IAP491_Capstone_Guidelines_and_Rubrics_Summary.md",
             DOCS_DIR / "work" / "fpt_guidelines_and_rubrics.md")
    copy_doc(ROOT_DIR / "Final-Report" / "Meeting" / "Meeting 1_29_08_26.md",
             DOCS_DIR / "work" / "meeting_1.md")
    copy_doc(ROOT_DIR / "Final-Report" / "Meeting" / "Meeting 2_01_09_26.md",
             DOCS_DIR / "work" / "meeting_2.md")
    copy_doc(ROOT_DIR / "Final-Report" / "Meeting" / "Meeting 3_08_09_26.md",
             DOCS_DIR / "work" / "meeting_3.md")

    # 2. Chuyên Đề 1: Prompt Study
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "prompt_study" / "01_llm_foundations_and_token_generation.md",
             DOCS_DIR / "prompt_study" / "llm_foundations.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "prompt_study" / "02_prompt_structure_and_chat_formats.md",
             DOCS_DIR / "prompt_study" / "prompt_structure.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "prompt_study" / "03_instruction_hierarchy_and_flat_boundary.md",
             DOCS_DIR / "prompt_study" / "instruction_hierarchy.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "prompt_study" / "04_resources_and_papers.md",
             DOCS_DIR / "prompt_study" / "resources_and_papers.md")

    # 3. Chuyên Đề 2: Attack Study
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "attack_study" / "00_overview_threat_and_scope" / "history_and_evolution.md",
             DOCS_DIR / "attacks" / "history_and_evolution.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "attack_study" / "00_overview_threat_and_scope" / "scope_and_boundary_analysis.md",
             DOCS_DIR / "attacks" / "scope_and_boundary_analysis.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "attack_study" / "01_prompt_injection" / "how_it_works_and_mechanisms.md",
             DOCS_DIR / "attacks" / "pi_how_it_works.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "attack_study" / "01_prompt_injection" / "taxonomy_and_variants.md",
             DOCS_DIR / "attacks" / "pi_taxonomy_and_variants.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "attack_study" / "01_prompt_injection" / "resources_and_papers.md",
             DOCS_DIR / "attacks" / "pi_resources_and_papers.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "attack_study" / "02_modern_jailbreak_attacks" / "archetypes_and_mechanisms.md",
             DOCS_DIR / "attacks" / "jb_archetypes_and_mechanisms.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "attack_study" / "02_modern_jailbreak_attacks" / "datasets_benchmarks_and_taxonomy.md",
             DOCS_DIR / "attacks" / "jb_datasets_and_benchmarks.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "attack_study" / "02_modern_jailbreak_attacks" / "advanced_variants_and_operators.md",
             DOCS_DIR / "attacks" / "jb_advanced_variants_and_operators.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "attack_study" / "02_modern_jailbreak_attacks" / "resources_and_papers.md",
             DOCS_DIR / "attacks" / "jb_resources_and_papers.md")

    # 4. Chuyên Đề 3: Threat & Defense Study
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "threat_and_defense_study" / "01_threat_model_and_attack_surface.md",
             DOCS_DIR / "threat_defense" / "threat_model_and_attack_surface.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "threat_and_defense_study" / "02_multi_layer_defense_architecture.md",
             DOCS_DIR / "threat_defense" / "multi_layer_defense_architecture.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "threat_and_defense_study" / "03_comparative_matrix_and_tradeoffs.md",
             DOCS_DIR / "threat_defense" / "comparative_matrix_and_tradeoffs.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "threat_and_defense_study" / "04_resources_and_papers.md",
             DOCS_DIR / "threat_defense" / "resources_and_papers.md")

    # 5. Chuyên Đề 4: Dataset & Benchmark Study
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "dataset_and_benchmark_study" / "01_data_curation_and_class_balance.md",
             DOCS_DIR / "dataset_study" / "data_curation.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "dataset_and_benchmark_study" / "02_group_aware_splitting_and_ood.md",
             DOCS_DIR / "dataset_study" / "group_aware_splitting.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "dataset_and_benchmark_study" / "03_resources_and_papers.md",
             DOCS_DIR / "dataset_study" / "resources_and_papers.md")

    # 6. Chuyên Đề 5: Model Study
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "model_study" / "03_two_tier_pipeline_coordination" / "how_it_works_and_architecture.md",
             DOCS_DIR / "models" / "two_tier_architecture.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "model_study" / "03_two_tier_pipeline_coordination" / "benchmark_and_tradeoffs.md",
             DOCS_DIR / "models" / "two_tier_tradeoffs.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "model_study" / "01_tfidf_syntactic_baseline" / "theory_and_math.md",
             DOCS_DIR / "models" / "tfidf_theory_and_math.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "model_study" / "01_tfidf_syntactic_baseline" / "how_it_works_and_usage.md",
             DOCS_DIR / "models" / "tfidf_usage.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "model_study" / "01_tfidf_syntactic_baseline" / "resources_and_videos.md",
             DOCS_DIR / "models" / "tfidf_resources.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "model_study" / "02_deberta_v3_semantic_classifier" / "theory_and_math.md",
             DOCS_DIR / "models" / "deberta_theory_and_math.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "model_study" / "02_deberta_v3_semantic_classifier" / "how_it_works_and_usage.md",
             DOCS_DIR / "models" / "deberta_usage.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "model_study" / "02_deberta_v3_semantic_classifier" / "resources_and_videos.md",
             DOCS_DIR / "models" / "deberta_resources.md")

    # 7. Chuyên Đề 6: Robustness & Evasion Study
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "robustness_study" / "01_theory_and_evasion_mechanisms.md",
             DOCS_DIR / "robustness" / "theory_and_evasion_mechanisms.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "robustness_study" / "02_defense_architecture_and_mitigation.md",
             DOCS_DIR / "robustness" / "defense_architecture_and_mitigation.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "robustness_study" / "03_benchmarks_metrics_and_tradeoffs.md",
             DOCS_DIR / "robustness" / "benchmarks_metrics_and_tradeoffs.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "robustness_study" / "04_resources_and_papers.md",
             DOCS_DIR / "robustness" / "resources_and_papers.md")

    # 8. Chuyên Đề 7: Evaluation & Trade-off Study
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "evaluation_and_tradeoff_study" / "01_false_positive_economics_and_ux.md",
             DOCS_DIR / "evaluation_study" / "false_positive_economics.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "evaluation_and_tradeoff_study" / "02_pareto_frontier_and_system_tradeoffs.md",
             DOCS_DIR / "evaluation_study" / "pareto_frontier.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "evaluation_and_tradeoff_study" / "03_resources_and_papers.md",
             DOCS_DIR / "evaluation_study" / "resources_and_papers.md")

    # Research Docs & Comparative Analysis
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "comparative_analysis" / "State_of_the_Art_Guardrail_and_Jailbreak_Benchmarks_Analysis.md",
             DOCS_DIR / "research" / "sota_guardrail_benchmarks.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "comparative_analysis" / "Target_LLM_API_Benchmark_and_Vulnerability_Analysis.md",
             DOCS_DIR / "research" / "target_llm_vulnerabilities.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "comparative_analysis" / "Tencent2026_Paper_Analysis_and_Mapping_to_PIGuard.md",
             DOCS_DIR / "research" / "tencent2026_paper_analysis.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "comparative_analysis" / "Why_Dual_Model_Architecture_TFIDF_and_DeBERTaV3.md",
             DOCS_DIR / "research" / "why_dual_model_architecture.md")

    # Luận văn & Báo cáo Review
    copy_doc(ROOT_DIR / "CAPSTONE PROJECT REGISTER.md",
             DOCS_DIR / "thesis" / "capstone_register.md")
    copy_doc(ROOT_DIR / "Final-Report" / "thesis" / "Review1_Problem_Definition_and_Threat_Model.md",
             DOCS_DIR / "thesis" / "review1_threat_model.md")
    copy_doc(ROOT_DIR / "Final-Report" / "thesis" / "chapters" / "01_Introduction.md",
             DOCS_DIR / "thesis" / "chapter_01_introduction.md")
    copy_doc(ROOT_DIR / "Final-Report" / "thesis" / "chapters" / "02_Literature_Review.md",
             DOCS_DIR / "thesis" / "chapter_02_literature_review.md")
    copy_doc(ROOT_DIR / "Final-Report" / "thesis" / "FINAL_THESIS.md",
             DOCS_DIR / "thesis" / "final_thesis.md")

    # Thư viện bài báo khoa học
    copy_doc(ROOT_DIR / "Final-Report" / "References" / "README.md",
             DOCS_DIR / "references" / "references_overview.md")
    copy_doc(ROOT_DIR / "Final-Report" / "References" / "REFERENCES_LOG.md",
             DOCS_DIR / "references" / "references_log.md")

    # Đội ngũ & Hướng dẫn kỹ thuật
    copy_doc(ROOT_DIR / "AGENTS.md",
             DOCS_DIR / "dev" / "team_governance.md")
    copy_doc(ROOT_DIR / "CONTRIBUTING.md",
             DOCS_DIR / "dev" / "contributing_guide.md")
    copy_doc(ROOT_DIR / "workspaces" / "README.md",
             DOCS_DIR / "dev" / "workspaces_overview.md")
    # Kiến trúc mã nguồn & quy chuẩn tích hợp
    src_readme = FINAL_REPORT_DIR / "src" / "README.md" if (FINAL_REPORT_DIR / "src" / "README.md").exists() else ROOT_DIR / "src" / "README.md"
    if src_readme.exists():
        copy_doc(src_readme, DOCS_DIR / "dev" / "src_architecture.md")
    else:
        create_src_architecture_doc(DOCS_DIR / "dev" / "src_architecture.md")

    print("\n🎉 [HOÀN TẤT] Toàn bộ 7 chuyên đề khoa học đã được chuẩn hóa và sẵn sàng cho MkDocs build!")

def create_src_architecture_doc(dest_path: Path):
    """Create a status-only description if no shared source README exists."""
    content = """# Shared source scaffold

This folder is a module scaffold. Personal Review 2 runs remain local-only and are not shared evidence. This scaffold does not establish final KPI acceptance or a deployed service.

The proposed flow separates L1 input handling, L2 per-chunk route candidates, L3 REVIEW scoring, and API request aggregation. L2 ALLOW/BLOCK are candidates; only API aggregation emits final request ALLOW/BLOCK. Symbolic thresholds are not established service settings.
"""
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ [GEN] Wrote source scaffold status to {dest_path.relative_to(ROOT_DIR)}")

if __name__ == "__main__":
    aggregate_all()

