#!/usr/bin/env python3
"""
Verification Script for Task 3 Replication Assets (Focused on PIGuard ACL 2025)
PI-Guard Capstone Project - FPT University
Workspace: workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication
"""

import os
import sys

def check_file(path, min_bytes=100, is_pdf=False):
    if not os.path.exists(path):
        return False, f"MISSING: {path}"
    size = os.path.getsize(path)
    if size < min_bytes:
        return False, f"TOO SMALL ({size} bytes): {path}"
    if is_pdf:
        with open(path, "rb") as f:
            header = f.read(4)
        if header != b"%PDF":
            return False, f"INVALID PDF HEADER: {path}"
    return True, f"OK ({size / (1024*1024):.2f} MB): {os.path.basename(path)}"

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    print("=" * 70)
    print("PI-GUARD TASK 3 REPLICATION ASSETS VERIFICATION (PIGUARD FOCUS)")
    print(f"Base Directory: {base_dir}")
    print("=" * 70)

    assets = [
        # Core SOTA Anchor Paper (PIGuard ACL 2025)
        ("papers/PIGuard_ACL2025_arXiv2410.22770.pdf", 500_000, True),
        # PIGuard Virtual Environment & Scripts
        ("PIGuard_ACL2025/.venv/Scripts/python.exe", 10_000, False),
        ("PIGuard_ACL2025/quick_test_piguard.py", 500, False),
        ("PIGuard_ACL2025/eval_hf.py", 1000, False),
        ("PIGuard_ACL2025/eval.py", 1000, False),
        ("PIGuard_ACL2025/train.py", 1000, False),
        ("PIGuard_ACL2025/PIGuard.py", 500, False),
        ("PIGuard_ACL2025/params.py", 500, False),
        ("PIGuard_ACL2025/PIGuard_ACL2025_Replication_and_Paper_Comparison.ipynb", 10_000, False),
        # PIGuard Datasets
        ("PIGuard_ACL2025/datasets/train.json", 10_000_000, False),
        ("PIGuard_ACL2025/datasets/valid.json", 10_000, False),
        ("PIGuard_ACL2025/datasets/NotInject_one.json", 5_000, False),
        ("PIGuard_ACL2025/datasets/NotInject_two.json", 5_000, False),
        ("PIGuard_ACL2025/datasets/NotInject_three.json", 5_000, False),
        ("PIGuard_ACL2025/datasets/BIPIA_text.json", 1_000, False),
        ("PIGuard_ACL2025/datasets/BIPIA_code.json", 1_000, False),
        ("PIGuard_ACL2025/datasets/wildguard.json", 50_000, False),
        # Documentation & Replication Benchmark Deliverables
        ("README.md", 500, False),
        ("PIGUARD_ACL2025_REPLICATION_REPORT.md", 1000, False),
        ("PIGUARD_REPLICATION_BENCHMARK_RESULTS.json", 1000, False),
        # Authentic Paper Evidence Screenshots (Root mirror & 01_paper_evidence/)
        ("figures/README.md", 1000, False),
        ("figures/paper_p1_title_and_abstract.png", 50_000, False),
        ("figures/paper_p7_table_1_main_results.png", 50_000, False),
        ("figures/paper_p16_table_7_full_benchmarks.png", 30_000, False),
        ("figures/paper_p8_table_2_ablation_study.png", 30_000, False),
        ("figures/paper_p16_figure_7_case_study.png", 10_000, False),
        ("figures/local_vs_paper_scorecard.png", 30_000, False),
        ("figures/piguard_replication_paper_vs_local_bars.png", 30_000, False),
        ("figures/piguard_replication_keyword_decay_curve.png", 30_000, False),
        ("figures/piguard_replication_latency_profile.png", 30_000, False),
        ("figures/piguard_replication_confusion_matrix.png", 30_000, False),
        # Categorized Subfolder Figures
        ("figures/01_paper_evidence/paper_p1_title_and_abstract.png", 50_000, False),
        ("figures/01_paper_evidence/paper_p7_table_1_main_results.png", 50_000, False),
        ("figures/01_paper_evidence/paper_p16_table_7_full_benchmarks.png", 30_000, False),
        ("figures/01_paper_evidence/paper_p8_table_2_ablation_study.png", 30_000, False),
        ("figures/01_paper_evidence/paper_p16_figure_7_case_study.png", 10_000, False),
        ("figures/02_empirical_plots/local_vs_paper_scorecard.png", 30_000, False),
        ("figures/02_empirical_plots/piguard_replication_paper_vs_local_bars.png", 30_000, False),
        ("figures/02_empirical_plots/piguard_replication_keyword_decay_curve.png", 30_000, False),
        ("figures/02_empirical_plots/piguard_replication_latency_profile.png", 30_000, False),
        ("figures/02_empirical_plots/piguard_replication_confusion_matrix.png", 30_000, False),
        ("../TIER_1_CANDIDATE_MODELS_RESEARCH.md", 1000, False)
    ]

    all_passed = True
    for rel_path, min_b, is_pdf in assets:
        full_path = os.path.normpath(os.path.join(base_dir, rel_path))
        passed, msg = check_file(full_path, min_b, is_pdf)
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{status:7} {msg}")
        if not passed:
            all_passed = False

    print("=" * 70)
    if all_passed:
        print("RESULT: ALL ASSETS VERIFIED 100% INTACT & READY FOR REPLICATION!")
        sys.exit(0)
    else:
        print("RESULT: VERIFICATION FAILED FOR ONE OR MORE ASSETS.")
        sys.exit(1)

if __name__ == "__main__":
    main()
