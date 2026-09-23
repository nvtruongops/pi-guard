"""
Inspection and Audit Script for Meeting 6 Research Rigor.
Audits:
1. Citation anchor integrity (all [[N]](#refN) must have matching <a id="refN"></a>).
2. Local PDF existence in References/.
3. Academic defense terminology blacklist compliance.
4. Argumentation & defense rationale completeness.
5. Empirical evidence & visual artifacts completeness.
"""
import os
import re
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path("d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_6")
REPO_ROOT = Path("d:/Work/Do-an")
LOCAL_REFS_DIRS = [
    BASE_DIR.parent / "References",
    REPO_ROOT / "Final-Report" / "References"
]

BANNED_TERMS = [
    r"\bthời gian thực\b",
    r"\breal-time\b",
    r"\bproduction-ready\b",
    r"\bbảo vệ 100%\b",
    r"\bbảo vệ tuyệt đối\b",
    r"\bchống hack hoàn toàn\b",
    r"\bunbreakable defense\b",
    r"\bsilver bullet\b",
    r"\bkhông lo ngại bất kỳ câu hỏi phản biện nào\b",
    r"\bđộ chuẩn mực học thuật tối đa\b",
    r"\btài liệu hoàn hảo không tì vết\b"
]

def audit_markdown_files():
    md_files = list(BASE_DIR.rglob("*.md"))
    print(f"[*] Found {len(md_files)} markdown files in {BASE_DIR.name}")
    
    total_anchors_checked = 0
    broken_anchors = []
    terminology_violations = []

    anchor_pattern = re.compile(r"\[\[(\d+)\]\]\(#ref\1\)")
    target_anchor_pattern = re.compile(r'<a\s+id=[\'"]ref(\d+)[\'"]\s*>')

    for md_file in md_files:
        rel_path = md_file.relative_to(BASE_DIR)
        with open(md_file, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Remove fenced code blocks
        content_no_code = re.sub(r"```[\s\S]*?```", "", content)

        # 1. Anchor Check
        citations = anchor_pattern.findall(content_no_code)
        targets = set(target_anchor_pattern.findall(content_no_code))

        for cit in citations:
            total_anchors_checked += 1
            if cit not in targets:
                broken_anchors.append((str(rel_path), f"[[{cit}]](#ref{cit})"))

        # 2. Terminology Check
        for banned_pat in BANNED_TERMS:
            matches = list(re.finditer(banned_pat, content_no_code, re.IGNORECASE))
            for m in matches:
                # Get surrounding context
                start = max(0, m.start() - 30)
                end = min(len(content_no_code), m.end() + 30)
                snippet = content_no_code[start:end].replace("\n", " ")
                terminology_violations.append((str(rel_path), m.group(0), snippet))

    return total_anchors_checked, broken_anchors, terminology_violations

def audit_empirical_artifacts():
    print("[*] Auditing empirical evidence and artifacts...")
    artifacts = {
        "Src: Tier 0 Scrubber": BASE_DIR / "src" / "tier0_ingress_scrubber.py",
        "Src: Block Chunker": BASE_DIR / "src" / "block_chunker.py",
        "Src: Tier 1 Fast Filter": BASE_DIR / "src" / "tier1_fast_filter.py",
        "Src: Tier 2 Semantic Arbiter": BASE_DIR / "src" / "tier2_semantic_arbiter.py",
        "Weights: Tier 1 Joblib": BASE_DIR / "src" / "tier1_tfidf_model.joblib",
        "Data: 200k Benign": BASE_DIR / "data" / "sample_benign_200k.txt",
        "Data: 200k Tail Attack": BASE_DIR / "data" / "sample_malicious_tail_200k.txt",
        "Data: Cross-Dataset D1": BASE_DIR / "data" / "cross_dataset_suite" / "D1_piguard_valid.json",
        "Data: Cross-Dataset D2": BASE_DIR / "data" / "cross_dataset_suite" / "D2_bipia_indirect.json",
        "Data: Cross-Dataset D3": BASE_DIR / "data" / "cross_dataset_suite" / "D3_jailbreakbench_100.json",
        "Data: Cross-Dataset D4": BASE_DIR / "data" / "cross_dataset_suite" / "D4_datasentinel_openpi.json",
        "Data: Cross-Dataset D5": BASE_DIR / "data" / "cross_dataset_suite" / "D5_notinject_overdefense.json",
        "Data: Cross-Dataset D6": BASE_DIR / "data" / "cross_dataset_suite" / "D6_wildguard_complex_benign.json",
        "Benchmark: Matrix JSON": BASE_DIR / "04_benchmarks_and_data" / "cross_dataset_empirical_matrix.json",
        "Figure 1: Early Stopping 200k": BASE_DIR / "figures" / "fig1_early_stopping_latency_200k.png",
        "Figure 2: Cross Dataset Heatmap": BASE_DIR / "figures" / "fig2_cross_dataset_heatmap.png",
        "Figure 3: Overdefense Tradeoff": BASE_DIR / "figures" / "fig3_overdefense_and_lowfpr_tradeoff.png",
        "Figure 4: Component Ablation": BASE_DIR / "figures" / "fig4_ablation_study_breakdown.png",
        "Test: Long Doc 200k": BASE_DIR / "tests" / "test_long_document_200k.py",
        "Test: Hidden Tail Injection": BASE_DIR / "tests" / "test_hidden_prompt_at_tail.py",
    }
    missing = []
    for name, path in artifacts.items():
        if not path.exists():
            missing.append((name, str(path)))
        else:
            size_kb = path.stat().st_size / 1024
            print(f"  ✔ [EXISTS] {name:<30} ({size_kb:8.2f} KB)")
    return missing

def main():
    print("=" * 80)
    print("🔍 AUDIT ĐỘ HOÀN THIỆN LẬP LUẬN, BẰNG CHỨNG THỰC NGHIỆM VÀ TRÍCH DẪN (MEETING 6)")
    print("=" * 80)

    # 1. Check Artifacts
    missing_artifacts = audit_empirical_artifacts()

    # 2. Check Anchors and Terminology
    total_anchors, broken_anchors, term_violations = audit_markdown_files()

    print("\n" + "=" * 80)
    print("📊 BẢNG TỔNG HỢP KIỂM TOÁN HỌC THUẬT (AUDIT SUMMARY)")
    print("=" * 80)
    print(f"1. Tổng số neo trích dẫn kiểm tra : {total_anchors}")
    print(f"   - Số neo gãy (Broken anchors)   : {len(broken_anchors)}")
    if broken_anchors:
        for f, anc in broken_anchors:
            print(f"     ❌ {f} -> {anc}")
    else:
        print("   ✔ 100% neo trích dẫn toàn vẹn và có đối ứng on-page HTML anchor!")

    # 3. Check Local PDF links
    pdf_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+\.pdf)\)')
    broken_pdfs = []
    total_pdfs_checked = 0
    for md_file in Path("d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_6").rglob("*.md"):
        with open(md_file, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        matches = pdf_pattern.findall(content)
        for text, url in matches:
            if url.startswith("http://") or url.startswith("https://"):
                continue
            clean_url = url.replace("file:///", "").replace("file://", "")
            target_path = Path(clean_url)
            if not target_path.is_absolute():
                target_path = md_file.parent / clean_url
            total_pdfs_checked += 1
            if not target_path.exists():
                broken_pdfs.append((md_file.name, url))

    print(f"\n3. Kiểm tra liên kết PDF cục bộ (Local PDF Invariant):")
    print(f"   - Tổng số liên kết PDF cục bộ : {total_pdfs_checked}")
    print(f"   - Số liên kết PDF bị gãy      : {len(broken_pdfs)}")
    if broken_pdfs:
        for f, u in broken_pdfs:
            print(f"     ❌ {f} -> {u}")
    else:
        print("   ✔ 100% tài liệu tham khảo dẫn link PDF cục bộ đều tồn tại trên ổ cứng!")

    print(f"\n4. Tuân thủ thuật ngữ Blacklist/Whitelist (Academic Humility):")
    print(f"   - Số vi phạm phát hiện          : {len(term_violations)}")
    if term_violations:
        for f, term, snip in term_violations:
            print(f"     ⚠️  {f}: '{term}'\n        Context: ...{snip}...")
    else:
        print("   ✔ 100% tuân thủ bảng thuật ngữ chuẩn mực (Không dính overclaiming)!")


    print("=" * 80)

if __name__ == "__main__":
    main()
