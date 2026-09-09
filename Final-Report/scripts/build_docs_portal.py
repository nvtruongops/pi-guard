"""
scripts/build_docs_portal.py
-----------------------------
PI-Guard Documentation Portal Aggregator (8-Pillar Academic Architecture)
Tự động thu thập, chuẩn hóa và cấu trúc tài liệu toàn dự án PI-Guard
thành thư mục 'docs/' để phục vụ xuất bản Web UI qua GitHub Pages (MkDocs Material).

Quy tắc bảo vệ:
- KHÔNG BAO GIỜ chỉnh sửa hoặc xóa tài liệu nội bộ trong docs/fpt_capstone_guide/.
- Giữ nguyên vẹn file gốc trong reports/Meeting/, workspaces/, reports/References/, docs/.
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
FINAL_REPORT_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = FINAL_REPORT_DIR.parent
DOCS_DIR = ROOT_DIR / "Github-Page"

def clean_and_prepare_dir():
    """Khởi tạo và làm sạch các thư mục chuyên đề trong docs/ phục vụ MkDocs (BẢO VỆ TUYỆT ĐỐI docs/fpt_capstone_guide/)."""
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    # Tạo và làm sạch các thư mục con theo kiến trúc thông tin 8 Chuyên Đề Khoa Học
    subdirs = [
        "work", "prompt_study", "attacks", "threat_defense", 
        "dataset_study", "models", "robustness", "optimization", 
        "evaluation_study", "research", "thesis", "references", 
        "dev", "javascripts", "stylesheets"
    ]
    for sub in subdirs:
        sub_path = DOCS_DIR / sub
        if sub_path.exists():
            shutil.rmtree(sub_path)
        sub_path.mkdir(parents=True, exist_ok=True)

    # Xóa index.md cũ nếu có để tạo mới
    if (DOCS_DIR / "index.md").exists():
        (DOCS_DIR / "index.md").unlink()

    # Dọn dẹp các thư mục rỗng cũ không còn dùng trong docs nếu có
    for old_dir in ["api", "architecture", "experiments", "methodology"]:
        old_p = DOCS_DIR / old_dir
        if old_p.exists():
            try:
                if not any(old_p.iterdir()):
                    old_p.rmdir()
            except Exception:
                pass

    print(f"📁 [INIT] Đã khởi tạo cấu trúc thư mục tài liệu GitHub Pages tại: {DOCS_DIR}")

def sanitize_content(content: str) -> str:
    """
    Chuẩn hóa nội dung markdown:
    - Loại bỏ triệt để mọi liên kết hoặc đề cập đến tài liệu bảo mật nội bộ (docs/fpt_capstone_guide).
    - Chuyển đổi file:// link tuyệt đối Windows thành văn bản chuẩn hoặc link hợp lệ.
    - Chuẩn hóa Math block và Callouts.
    """
    sanitized_lines = []
    for line in content.splitlines():
        if "fpt_capstone_guide" in line or "SP26IA04" in line:
            continue
        sanitized_lines.append(line)
    content = "\n".join(sanitized_lines)

    # Chuyển đổi link PDF nội bộ và link file ngoài thành inline code hoặc text đậm
    content = re.sub(r"\[([^\]]+)\]\((?:file:///[^)]*|Final-Report(?:/[^)]*)?|workspaces(?:/[^)]*)?|reports/(?:References|Meeting)/[^)]*|References/[^)]*|Meeting/[^)]*|CAPSTONE%20PROJECT%20REGISTER\.md|Github-Page/[^)]*|docs/[^)]*)\)", r"**\1**", content)

    # Thay thế file:///... còn lại
    content = re.sub(r"\(file:///[^)]+\)", r"(#)", content)

    # Sửa lỗi ký tự gạch chéo ngược \_ trong link URL
    content = re.sub(r"https?://[^\s\)]+", lambda m: m.group(0).replace(r"\_", "_"), content)
    content = content.replace("https://genai.owasp.org/llm-top-10/", "https://owasp.org/www-project-top-10-for-large-language-model-applications/")
    content = content.replace("https://dl.acm.org/doi/epdf/10.1145/3724393", "https://doi.org/10.1145/3724393")

    return content

def copy_doc(src_path: Path, dest_path: Path, title_prefix: str = ""):
    """Đọc file nguồn, chuẩn hóa link và ghi vào thư mục docs."""
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
## Hệ Thống 8 Chuyên Đề Nghiên Cứu Khoa Học & Báo Cáo Khóa Luận

> **Đồ án Khóa luận Tốt nghiệp Đại học FPT** — Chuyên ngành An toàn Thông tin (Information Assurance)<br>
> **Mã đề tài**: `IAP491_FA26_PI_GUARD` | **Năm học**: 2026<br>
> **Chủ đề**: A Machine-Learning Guardrail for Detecting Prompt Injection and Jailbreak Attacks on LLM Applications

---

## 🎯 Giới Thiệu & Mục Tiêu Đề Tài

**PI-Guard** là hệ thống bảo vệ (guardrail) trung gian đặt trước các ứng dụng mô hình ngôn ngữ lớn (LLM), hoạt động theo cơ chế **hai tầng bảo vệ (Two-Tier Cascade Architecture)**:

1. **Tier 1 (Bộ lọc Cú pháp - Syntactic Baseline)**: Sử dụng phương pháp vector hóa TF-IDF kết hợp mô hình phân loại tuyến tính siêu nhẹ (Linear Classifier) nhằm nhận diện các mẫu prompt injection phổ biến với độ trễ cực thấp (**< 1.0 ms**).
2. **Tier 2 (Bộ lọc Ngữ nghĩa Sâu - Semantic Transformer)**: Sử dụng Transformer tiên tiến (**DeBERTa-v3**) với cơ chế Disentangled Attention, được lượng hóa qua **ONNX Runtime INT8** nhằm phát hiện các biến thể tấn công tinh vi, jailbreak ẩn ngữ cảnh với độ trễ mục tiêu **P95 < 25 ms**.

---

## 🌟 Sơ Đồ Luồng Phòng Thủ 2 Tầng (Mermaid)

```mermaid
flowchart TD
    UserPrompt(["📥 User Prompt"]) --> P1["⚙️ Tiền xử lý & Chuẩn hóa Unicode"]
    P1 --> T1{"⚡ Tier 1: TF-IDF Syntactic Gate"}

    T1 -- "Nguy hiểm (Score >= 0.85)" --> Block1["🚫 Chặn ngay (< 1ms)"]
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

## 📋 Hệ Thống 8 Chuyên Đề Nghiên Cứu Khoa Học Trọng Điểm

| Chuyên Đề Khoa Học | Trọng Tâm Nghiên Cứu | Đường Dẫn Tra Cứu |
| :--- | :--- | :--- |
| **1. Prompt Study** | Bản chất LLM, Attention, Ranh giới phẳng và Thất bại Phân cấp Chỉ thị (Instruction Hierarchy) | [Xem Prompt Study](prompt_study/llm_foundations.md) |
| **2. Attack Study** | Phân loại toàn diện Prompt Injection & 4 trường phái Jailbreak (DAN, Roleplay, VM, Cipher) | [Xem Attack Study](attacks/history_and_evolution.md) |
| **3. Threat & Defense** | Mô hình hóa đe dọa NIST AI 100-2e2025, STRIDE, Kiến trúc phòng thủ đa tầng (Defense-in-Depth) | [Xem Threat & Defense](threat_defense/threat_model_and_attack_surface.md) |
| **4. Dataset & Benchmark** | Tuyển chọn dữ liệu 3 lớp, Khử trùng lặp MinHash, Group-Aware Splitting & Đánh giá OOD | [Xem Dataset Study](dataset_study/data_curation.md) |
| **5. Model Study** | Toán học TF-IDF, Transformer DeBERTa-v3 Disentangled Attention & Định tuyến bất định 2 tầng | [Xem Model Study](models/two_tier_architecture.md) |
| **6. Robustness Study** | Chống chịu kỹ thuật làm mờ (Leetspeak, Homoglyphs, Base64) & Tiền xử lý chuẩn hóa 4 bước | [Xem Robustness Study](robustness/theory_and_evasion_mechanisms.md) |
| **7. Optimization Study** | Lý thuyết lượng tử hóa INT8 PTQ, Tăng tốc ONNX Runtime Graph & Phân vị độ trễ P95/P99 | [Xem Optimization Study](optimization/quantization_math.md) |
| **8. Evaluation & Trade-offs** | Kinh tế học cảnh báo sai (FPR Economics), Điểm hoạt động Recall@FPR1% & Đường cong biên Pareto | [Xem Evaluation Study](evaluation_study/false_positive_economics.md) |

---

## 👥 Đội Ngũ Thực Hiện Đề Tài

> **Phương châm làm việc toàn đội**: **Ai cũng làm $\rightarrow$ Tham khảo nhau $\rightarrow$ Chốt kết quả**  
> Cả 4 thành viên đều trực tiếp thực hiện toàn trình (Full-Pipeline Hands-on) từ tiền xử lý dữ liệu, thử nghiệm Baseline ML, huấn luyện Transformer, đo đạc độ bền Evasion đến tích hợp API/Dashboard và bảo vệ Luận văn.

| STT | Thành Viên | Mã Sinh Viên | Khám Phá Toàn Trình & Đầu Mối Điều Phối |
| :---: | :--- | :--- :---: | :--- |
| 1 | **Nguyễn Văn Trường (Leader)** | `SE182034` | **Toàn trình Full-Pipeline** — Điều phối chung, Chuẩn hóa dữ liệu & Kiến trúc |
| 2 | **Nguyễn Quí Đức** | `SE182087` | **Toàn trình Full-Pipeline** — Đối sánh mô hình Baseline ML & Threat Model |
| 3 | **Phạm Minh Hoàng Việt** | `SE181851` | **Toàn trình Full-Pipeline** — Tối ưu Transformer & Thực nghiệm Robustness |
| 4 | **Đỗ Đoàn Duy Phương** | `SE180235` | **Toàn trình Full-Pipeline** — Tích hợp hệ thống API/Dashboard & Luận văn |

**Giảng viên hướng dẫn**: Đại học FPT — Khoa An toàn Thông tin (Information Assurance).
"""
    dest = DOCS_DIR / "index.md"
    with open(dest, "w", encoding="utf-8") as f:
        f.write(index_content)
    print("✅ [HOMEPAGE] Đã sinh trang chủ index.md thành công.")

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
    with open(DOCS_DIR / "javascripts" / "mathjax.js", "w", encoding="utf-8") as f:
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
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "prompt_study" / "01_llm_foundations_and_token_generation.md",
             DOCS_DIR / "prompt_study" / "llm_foundations.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "prompt_study" / "02_prompt_structure_and_chat_formats.md",
             DOCS_DIR / "prompt_study" / "prompt_structure.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "prompt_study" / "03_instruction_hierarchy_and_flat_boundary.md",
             DOCS_DIR / "prompt_study" / "instruction_hierarchy.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "prompt_study" / "04_resources_and_papers.md",
             DOCS_DIR / "prompt_study" / "resources_and_papers.md")

    # 3. Chuyên Đề 2: Attack Study
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "attack_study" / "00_overview_threat_and_scope" / "history_and_evolution.md",
             DOCS_DIR / "attacks" / "history_and_evolution.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "attack_study" / "00_overview_threat_and_scope" / "scope_and_boundary_analysis.md",
             DOCS_DIR / "attacks" / "scope_and_boundary_analysis.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "attack_study" / "01_prompt_injection" / "how_it_works_and_mechanisms.md",
             DOCS_DIR / "attacks" / "pi_how_it_works.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "attack_study" / "01_prompt_injection" / "taxonomy_and_variants.md",
             DOCS_DIR / "attacks" / "pi_taxonomy_and_variants.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "attack_study" / "01_prompt_injection" / "resources_and_papers.md",
             DOCS_DIR / "attacks" / "pi_resources_and_papers.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "attack_study" / "02_modern_jailbreak_attacks" / "archetypes_and_mechanisms.md",
             DOCS_DIR / "attacks" / "jb_archetypes_and_mechanisms.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "attack_study" / "02_modern_jailbreak_attacks" / "datasets_benchmarks_and_taxonomy.md",
             DOCS_DIR / "attacks" / "jb_datasets_and_benchmarks.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "attack_study" / "02_modern_jailbreak_attacks" / "advanced_variants_and_operators.md",
             DOCS_DIR / "attacks" / "jb_advanced_variants_and_operators.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "attack_study" / "02_modern_jailbreak_attacks" / "resources_and_papers.md",
             DOCS_DIR / "attacks" / "jb_resources_and_papers.md")

    # 4. Chuyên Đề 3: Threat & Defense Study
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "threat_and_defense_study" / "01_threat_model_and_attack_surface.md",
             DOCS_DIR / "threat_defense" / "threat_model_and_attack_surface.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "threat_and_defense_study" / "02_multi_layer_defense_architecture.md",
             DOCS_DIR / "threat_defense" / "multi_layer_defense_architecture.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "threat_and_defense_study" / "03_comparative_matrix_and_tradeoffs.md",
             DOCS_DIR / "threat_defense" / "comparative_matrix_and_tradeoffs.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "threat_and_defense_study" / "04_resources_and_papers.md",
             DOCS_DIR / "threat_defense" / "resources_and_papers.md")

    # 5. Chuyên Đề 4: Dataset & Benchmark Study
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "dataset_and_benchmark_study" / "01_data_curation_and_class_balance.md",
             DOCS_DIR / "dataset_study" / "data_curation.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "dataset_and_benchmark_study" / "02_group_aware_splitting_and_ood.md",
             DOCS_DIR / "dataset_study" / "group_aware_splitting.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "dataset_and_benchmark_study" / "03_resources_and_papers.md",
             DOCS_DIR / "dataset_study" / "resources_and_papers.md")

    # 6. Chuyên Đề 5: Model Study
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "model_study" / "03_two_tier_pipeline_coordination" / "how_it_works_and_architecture.md",
             DOCS_DIR / "models" / "two_tier_architecture.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "model_study" / "03_two_tier_pipeline_coordination" / "benchmark_and_tradeoffs.md",
             DOCS_DIR / "models" / "two_tier_tradeoffs.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "model_study" / "01_tfidf_syntactic_baseline" / "theory_and_math.md",
             DOCS_DIR / "models" / "tfidf_theory_and_math.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "model_study" / "01_tfidf_syntactic_baseline" / "how_it_works_and_usage.md",
             DOCS_DIR / "models" / "tfidf_usage.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "model_study" / "01_tfidf_syntactic_baseline" / "resources_and_videos.md",
             DOCS_DIR / "models" / "tfidf_resources.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "model_study" / "02_deberta_v3_semantic_classifier" / "theory_and_math.md",
             DOCS_DIR / "models" / "deberta_theory_and_math.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "model_study" / "02_deberta_v3_semantic_classifier" / "how_it_works_and_usage.md",
             DOCS_DIR / "models" / "deberta_usage.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "model_study" / "02_deberta_v3_semantic_classifier" / "resources_and_videos.md",
             DOCS_DIR / "models" / "deberta_resources.md")

    # 7. Chuyên Đề 6: Robustness & Evasion Study
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "robustness_study" / "01_theory_and_evasion_mechanisms.md",
             DOCS_DIR / "robustness" / "theory_and_evasion_mechanisms.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "robustness_study" / "02_defense_architecture_and_mitigation.md",
             DOCS_DIR / "robustness" / "defense_architecture_and_mitigation.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "robustness_study" / "03_benchmarks_metrics_and_tradeoffs.md",
             DOCS_DIR / "robustness" / "benchmarks_metrics_and_tradeoffs.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "robustness_study" / "04_resources_and_papers.md",
             DOCS_DIR / "robustness" / "resources_and_papers.md")

    # 8. Chuyên Đề 7: Optimization Study
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "optimization_study" / "01_quantization_theory_and_ptq_math.md",
             DOCS_DIR / "optimization" / "quantization_math.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "optimization_study" / "02_onnx_runtime_and_graph_optimizations.md",
             DOCS_DIR / "optimization" / "onnx_runtime.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "optimization_study" / "03_inference_acceleration_and_system_design.md",
             DOCS_DIR / "optimization" / "inference_acceleration.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "optimization_study" / "04_benchmarks_metrics_and_tradeoffs.md",
             DOCS_DIR / "optimization" / "benchmarks_tradeoffs.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "optimization_study" / "05_resources_and_papers.md",
             DOCS_DIR / "optimization" / "resources_and_papers.md")

    # 9. Chuyên Đề 8: Evaluation & Trade-off Study
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "evaluation_and_tradeoff_study" / "01_false_positive_economics_and_ux.md",
             DOCS_DIR / "evaluation_study" / "false_positive_economics.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "evaluation_and_tradeoff_study" / "02_pareto_frontier_and_system_tradeoffs.md",
             DOCS_DIR / "evaluation_study" / "pareto_frontier.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "evaluation_and_tradeoff_study" / "03_resources_and_papers.md",
             DOCS_DIR / "evaluation_study" / "resources_and_papers.md")

    # Research Docs
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "State_of_the_Art_Guardrail_and_Jailbreak_Benchmarks_Analysis.md",
             DOCS_DIR / "research" / "sota_guardrail_benchmarks.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "Target_LLM_API_Benchmark_and_Vulnerability_Analysis.md",
             DOCS_DIR / "research" / "target_llm_vulnerabilities.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "Tencent2026_Paper_Analysis_and_Mapping_to_PIGuard.md",
             DOCS_DIR / "research" / "tencent2026_paper_analysis.md")
    copy_doc(ROOT_DIR / "workspaces" / "truongnv" / "docs" / "research" / "Why_Dual_Model_Architecture_TFIDF_and_DeBERTaV3.md",
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

    print("\n🎉 [HOÀN TẤT] Toàn bộ 8 chuyên đề khoa học đã được chuẩn hóa và sẵn sàng cho MkDocs build!")

def create_src_architecture_doc(dest_path: Path):
    """Tạo tài liệu kiến trúc mã nguồn chuẩn cho giai đoạn Review 1 (Zero-Code in Final-Report)."""
    content = """# THƯ MỤC MÃ NGUỒN CHÍNH THỨC CỦA DỰ ÁN (PRODUCTION SOURCE CODE)
## 🛡️ PI-Guard Core Framework Architecture

> [!IMPORTANT]
> **QUY TẮC BẢO TRÌ & ĐỒNG QUY MÃ NGUỒN (CONVERGENCE INVARIANT)**:
> 1. Thư mục `Final-Report/src/` là **NƠI CHỨA MÃ NGUỒN CHÍNH THỨC, HOÀN CHỈNH VÀ ĐÃ QUA KIỂM THỬ (PRODUCTION-READY)**.
> 2. Theo quy chuẩn học thuật FPT IAP491, trong giai đoạn **Review 1 (Problem Definition & Threat Modeling)**, dự án tuân thủ nghiêm ngặt **Quy tắc 100% Nghiên cứu lý thuyết & y văn (Zero Code in Final-Report)**.
> 3. Toàn bộ quá trình thử nghiệm, tiền xử lý dữ liệu, huấn luyện mô hình (TF-IDF Baseline, DeBERTa-v3) và xây dựng API proxy được 4 thành viên thực hiện song song trong các không gian làm việc độc lập (`workspaces/<thành_viên>/`).
> 4. **CHỈ KHI HOÀN THÀNH XONG VÀ NGHIỆM THU**, mã nguồn xuất sắc nhất mới được Leader đồng quy và tích hợp vào `Final-Report/src/` tại các cột mốc Review 2 và Review 3.

---

### 📂 THIẾT KẾ CẤU TRÚC CÁC MODULE DỰ KIẾN TRONG `src/`:

```
src/
├── preprocessing/                 # Tiền xử lý: Làm sạch, chuẩn hóa Unicode, bóc tách Base64
├── datasets/                      # Pipeline cào data, deduplication & Group-Aware Split
├── models/                        # Trình bao bọc suy luận (Baseline ML & DeBERTa INT8 ONNX)
│   ├── baseline/                  # Bộ phân loại TF-IDF + LogisticRegression / LinearSVC
│   └── classifier.py              # Wrapper chạy suy luận ONNX Runtime / PyTorch
├── training/                      # Pipeline huấn luyện tự động (Trainer, Callbacks, Loss)
├── evaluation/                    # Bộ đo lường chuẩn: F1, Precision, Recall, FPR, Latency
├── policy/                        # Bộ quy tắc định tuyến bảo vệ (3-Tier Layered Defense)
├── api/                           # Dịch vụ FastAPI Middleware & LLM Proxy (/v1/chat)
├── dashboard/                     # Giao diện Streamlit giám sát & kiểm thử trực quan
├── llm/                           # Kết nối Target LLM Cloud APIs (Groq, OpenAI, Gemini)
└── utils/                         # Logging, cấu hình, metrics tracker & helpers
```
"""
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ [GEN] Đã sinh tài liệu kiến trúc {dest_path.relative_to(ROOT_DIR)}")

if __name__ == "__main__":
    aggregate_all()

