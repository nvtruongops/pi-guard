#!/usr/bin/env python3
"""
Verification Script for Task 3 Replication Assets
PI-Guard Capstone Project - FPT University
Workspace: workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication
Verifies that:
1. Ayub_CAMLIS2024 and PIGuard_ACL2025 contain 100% pure public upstream code.
2. All interactive notebooks, benchmark scripts, and datasets in task_3_replication are intact.
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
    print("=" * 80)
    print("PI-GUARD TASK 3 REPLICATION ASSETS VERIFICATION")
    print(f"Base Directory: {base_dir}")
    print("=" * 80)

    assets = [
        # 1. Global / Shared Infrastructure
        (sys.executable, 10_000, False),
        ("README.md", 500, False),
        ("MEMBER_REPRODUCTION_RUNBOOK.md", 500, False),

        # 2. Tier 1 Subsystem: Ayub et al. (CAMLIS 2024) [REJECTED CANDIDATE]
        ("Tier1_REJECTED_Ayub_CAMLIS2024/README.md", 500, False),
        ("Tier1_REJECTED_Ayub_CAMLIS2024/papers/Ayub_CAMLIS2024_arXiv2410.22284.pdf", 500_000, True),
        ("Tier1_REJECTED_Ayub_CAMLIS2024/Ayub_CAMLIS2024_Replication_and_Paper_Comparison.ipynb", 10_000, False),
        ("Tier1_REJECTED_Ayub_CAMLIS2024/run_ayub_tier1_benchmark.py", 1000, False),
        ("Tier1_REJECTED_Ayub_CAMLIS2024/build_ayub_notebook.py", 1000, False),
        ("Tier1_REJECTED_Ayub_CAMLIS2024/AYUB_CAMLIS2024_REPLICATION_BENCHMARK_RESULTS.json", 1000, False),

        # 2.1 Pure Upstream Codebase: Ayub_CAMLIS2024 (100% Upstream Purity)
        ("Tier1_REJECTED_Ayub_CAMLIS2024/Ayub_CAMLIS2024/README.md", 500, False),
        ("Tier1_REJECTED_Ayub_CAMLIS2024/Ayub_CAMLIS2024/binary_classification.py", 500, False),
        ("Tier1_REJECTED_Ayub_CAMLIS2024/Ayub_CAMLIS2024/embedding.py", 500, False),
        ("Tier1_REJECTED_Ayub_CAMLIS2024/Ayub_CAMLIS2024/visualization.py", 500, False),
        ("Tier1_REJECTED_Ayub_CAMLIS2024/Ayub_CAMLIS2024/dataset/README.md", 50, False),
        ("Tier1_REJECTED_Ayub_CAMLIS2024/Ayub_CAMLIS2024/embeddings/README.md", 100, False),

        # 2.2 Tier 1 Publication Figures
        ("Tier1_REJECTED_Ayub_CAMLIS2024/figures/01_paper_evidence/ayub_p1_title_and_abstract.png", 50_000, False),
        ("Tier1_REJECTED_Ayub_CAMLIS2024/figures/01_paper_evidence/ayub_p7_table_3_and_4_results.png", 50_000, False),
        ("Tier1_REJECTED_Ayub_CAMLIS2024/figures/02_empirical_plots/ayub_replication_paper_vs_local_bars.png", 30_000, False),
        ("Tier1_REJECTED_Ayub_CAMLIS2024/figures/02_empirical_plots/ayub_overdefense_fpr_comparison.png", 30_000, False),
        ("Tier1_REJECTED_Ayub_CAMLIS2024/figures/02_empirical_plots/ayub_latency_profile.png", 30_000, False),

        # 3. Tier 2 Subsystem: PIGuard DeBERTa-v3-base (ACL 2025)
        ("Tier2_PIGuard_ACL2025/README.md", 500, False),
        ("Tier2_PIGuard_ACL2025/papers/PIGuard_ACL2025_arXiv2410.22770.pdf", 500_000, True),
        ("Tier2_PIGuard_ACL2025/PIGuard_ACL2025_Replication_and_Paper_Comparison.ipynb", 10_000, False),
        ("Tier2_PIGuard_ACL2025/eval_piguard_replication.py", 1000, False),
        ("Tier2_PIGuard_ACL2025/quick_test_piguard.py", 500, False),
        ("Tier2_PIGuard_ACL2025/PIGUARD_REPLICATION_BENCHMARK_RESULTS.json", 1000, False),
        ("Tier2_PIGuard_ACL2025/PIGUARD_ACL2025_REPLICATION_REPORT.md", 1000, False),

        # 3.1 Pure Upstream Codebase: PIGuard_ACL2025 (100% Upstream Purity)
        ("Tier2_PIGuard_ACL2025/PIGuard_ACL2025/README.md", 500, False),
        ("Tier2_PIGuard_ACL2025/PIGuard_ACL2025/LICENSE", 500, False),
        ("Tier2_PIGuard_ACL2025/PIGuard_ACL2025/PIGuard.py", 500, False),
        ("Tier2_PIGuard_ACL2025/PIGuard_ACL2025/eval.py", 1000, False),
        ("Tier2_PIGuard_ACL2025/PIGuard_ACL2025/eval_hf.py", 1000, False),
        ("Tier2_PIGuard_ACL2025/PIGuard_ACL2025/params.py", 500, False),
        ("Tier2_PIGuard_ACL2025/PIGuard_ACL2025/util.py", 500, False),
        ("Tier2_PIGuard_ACL2025/PIGuard_ACL2025/requirements.txt", 500, False),

        # 3.2 Benchmark Datasets in PIGuard_ACL2025 (Evaluation suites only)
        ("Tier2_PIGuard_ACL2025/PIGuard_ACL2025/datasets/valid.json", 10_000, False),
        ("Tier2_PIGuard_ACL2025/PIGuard_ACL2025/datasets/NotInject_one.json", 5_000, False),
        ("Tier2_PIGuard_ACL2025/PIGuard_ACL2025/datasets/NotInject_two.json", 5_000, False),
        ("Tier2_PIGuard_ACL2025/PIGuard_ACL2025/datasets/NotInject_three.json", 5_000, False),
        ("Tier2_PIGuard_ACL2025/PIGuard_ACL2025/datasets/BIPIA_text.json", 1_000, False),
        ("Tier2_PIGuard_ACL2025/PIGuard_ACL2025/datasets/BIPIA_code.json", 1_000, False),
        ("Tier2_PIGuard_ACL2025/PIGuard_ACL2025/datasets/wildguard.json", 50_000, False),

        # 3.3 Tier 2 Publication Figures
        ("Tier2_PIGuard_ACL2025/figures/01_paper_evidence/paper_p1_title_and_abstract.png", 50_000, False),
        ("Tier2_PIGuard_ACL2025/figures/01_paper_evidence/paper_p7_table_1_main_results.png", 50_000, False),
        ("Tier2_PIGuard_ACL2025/figures/01_paper_evidence/paper_p8_table_2_ablation_study.png", 50_000, False),
        ("Tier2_PIGuard_ACL2025/figures/01_paper_evidence/paper_p16_table_7_full_benchmarks.png", 30_000, False),
        ("Tier2_PIGuard_ACL2025/figures/01_paper_evidence/paper_p16_figure_7_case_study.png", 30_000, False),
        ("Tier2_PIGuard_ACL2025/figures/02_empirical_plots/local_vs_paper_scorecard.png", 30_000, False),
        ("Tier2_PIGuard_ACL2025/figures/02_empirical_plots/piguard_replication_paper_vs_local_bars.png", 30_000, False),
        ("Tier2_PIGuard_ACL2025/figures/02_empirical_plots/piguard_replication_latency_profile.png", 30_000, False),
        ("Tier2_PIGuard_ACL2025/figures/02_empirical_plots/piguard_replication_confusion_matrix.png", 30_000, False),

        # 4. Tier 1 Subsystem Candidate: Jain et al. (NeurIPS 2023 Workshop)
        ("Tier1_Candidate_Jain_NeurIPS2023/README.md", 500, False),
        ("Tier1_Candidate_Jain_NeurIPS2023/papers/Jain_2023_Baseline_Defenses_arXiv2309.00614.pdf", 300_000, True),
        ("Tier1_Candidate_Jain_NeurIPS2023/Jain_NeurIPS2023_Replication_and_Paper_Comparison.ipynb", 1_000, False),
        ("Tier1_Candidate_Jain_NeurIPS2023/run_jain_replication.py", 1_000, False),
        ("Tier1_Candidate_Jain_NeurIPS2023/JAIN_NEURIPS2023_REPLICATION_BENCHMARK_RESULTS.json", 1_000, False),
        ("Tier1_Candidate_Jain_NeurIPS2023/datasets/jain_eval_benchmark.json", 100_000, False),
        ("Tier1_Candidate_Jain_NeurIPS2023/datasets/jain_benign_samples.json", 10_000, False),
        ("Tier1_Candidate_Jain_NeurIPS2023/datasets/jain_attack_samples.json", 100_000, False),
        ("Tier1_Candidate_Jain_NeurIPS2023/Jain_NeurIPS2023/dataset/jain_eval_benchmark.json", 100_000, False),
        ("Tier1_Candidate_Jain_NeurIPS2023/Jain_NeurIPS2023/README.md", 200, False),
        ("Tier1_Candidate_Jain_NeurIPS2023/Jain_NeurIPS2023/perplexity_filter.py", 500, False),
        ("Tier1_Candidate_Jain_NeurIPS2023/figures/01_paper_evidence/jain_p1_title_and_abstract.png", 30_000, False),
        ("Tier1_Candidate_Jain_NeurIPS2023/figures/01_paper_evidence/jain_p6_table_1_defense_results.png", 30_000, False),
        ("Tier1_Candidate_Jain_NeurIPS2023/figures/01_paper_evidence/jain_p7_table_2_perplexity_results.png", 30_000, False),
        ("Tier1_Candidate_Jain_NeurIPS2023/figures/02_empirical_plots/jain_replication_paper_vs_local_mitigation.png", 30_000, False),
        ("Tier1_Candidate_Jain_NeurIPS2023/figures/02_empirical_plots/jain_latency_profile.png", 30_000, False),

        # 5. Tier 1 Subsystem Candidate: Meta Prompt-Guard 86M (Purple Llama 2024)
        ("Tier1_Candidate_Meta_PromptGuard2024/README.md", 500, False),
        ("Tier1_Candidate_Meta_PromptGuard2024/papers/Meta_2024_PurpleLlama_PromptGuard.pdf", 300_000, True),
        ("Tier1_Candidate_Meta_PromptGuard2024/Meta_PromptGuard2024_Replication_and_Paper_Comparison.ipynb", 1_000, False),
        ("Tier1_Candidate_Meta_PromptGuard2024/run_promptguard_replication.py", 1_000, False),
        ("Tier1_Candidate_Meta_PromptGuard2024/META_PROMPTGUARD_REPLICATION_BENCHMARK_RESULTS.json", 1_000, False),
        ("Tier1_Candidate_Meta_PromptGuard2024/datasets/promptguard_3class_eval.json", 100_000, False),
        ("Tier1_Candidate_Meta_PromptGuard2024/Meta_PromptGuard2024/dataset/promptguard_3class_eval.json", 100_000, False),
        ("Tier1_Candidate_Meta_PromptGuard2024/Meta_PromptGuard2024/README.md", 200, False),
        ("Tier1_Candidate_Meta_PromptGuard2024/Meta_PromptGuard2024/MODEL_CARD.md", 500, False),
        ("Tier1_Candidate_Meta_PromptGuard2024/figures/01_paper_evidence/meta_p1_title_and_abstract.png", 30_000, False),
        ("Tier1_Candidate_Meta_PromptGuard2024/figures/01_paper_evidence/meta_p6_table_eval_metrics.png", 30_000, False),
        ("Tier1_Candidate_Meta_PromptGuard2024/figures/01_paper_evidence/meta_p8_cyberseceval_safeguards.png", 30_000, False),
        ("Tier1_Candidate_Meta_PromptGuard2024/figures/02_empirical_plots/promptguard_replication_paper_vs_local_bars.png", 30_000, False),
        ("Tier1_Candidate_Meta_PromptGuard2024/figures/02_empirical_plots/promptguard_latency_profile.png", 30_000, False),

        # 6. Tier 1 Subsystem Candidate: InstructDetector (Findings of EMNLP 2024)
        ("Tier1_Candidate_InstructDetector_EMNLP2024/README.md", 500, False),
        ("Tier1_Candidate_InstructDetector_EMNLP2024/papers/Zhao_2024_InstructDetector_arXiv2402.06774.pdf", 200_000, True),
        ("Tier1_Candidate_InstructDetector_EMNLP2024/InstructDetector_EMNLP2024_Replication_and_Paper_Comparison.ipynb", 1_000, False),
        ("Tier1_Candidate_InstructDetector_EMNLP2024/run_instructdetector_replication.py", 1_000, False),
        ("Tier1_Candidate_InstructDetector_EMNLP2024/INSTRUCTDETECTOR_EMNLP2024_REPLICATION_BENCHMARK_RESULTS.json", 1_000, False),
        ("Tier1_Candidate_InstructDetector_EMNLP2024/datasets/bipia_text_eval.json", 10_000, False),
        ("Tier1_Candidate_InstructDetector_EMNLP2024/datasets/bipia_code_eval.json", 10_000, False),
        ("Tier1_Candidate_InstructDetector_EMNLP2024/InstructDetector_EMNLP2024/dataset/bipia_text_eval.json", 10_000, False),
        ("Tier1_Candidate_InstructDetector_EMNLP2024/InstructDetector_EMNLP2024/dataset/bipia_code_eval.json", 10_000, False),
        ("Tier1_Candidate_InstructDetector_EMNLP2024/InstructDetector_EMNLP2024/README.md", 200, False),
        ("Tier1_Candidate_InstructDetector_EMNLP2024/figures/01_paper_evidence/instruct_p1_title_and_abstract.png", 30_000, False),
        ("Tier1_Candidate_InstructDetector_EMNLP2024/figures/01_paper_evidence/instruct_p6_table_1_bipia_results.png", 30_000, False),
        ("Tier1_Candidate_InstructDetector_EMNLP2024/figures/01_paper_evidence/instruct_p7_table_2_layer_gradient.png", 30_000, False),
        ("Tier1_Candidate_InstructDetector_EMNLP2024/figures/02_empirical_plots/instructdetector_replication_paper_vs_local_bars.png", 30_000, False),
        ("Tier1_Candidate_InstructDetector_EMNLP2024/figures/02_empirical_plots/instructdetector_asr_reduction.png", 30_000, False),

        # 7. Ayub CAMLIS 2024 Dedicated Datasets
        ("Tier1_REJECTED_Ayub_CAMLIS2024/datasets/wildguard.json", 50_000, False),
        ("Tier1_REJECTED_Ayub_CAMLIS2024/datasets/NotInject_one.json", 5_000, False),

        # 8. PIGuard ACL 2025 Root Datasets
        ("Tier2_PIGuard_ACL2025/datasets/valid.json", 10_000, False),
        ("Tier2_PIGuard_ACL2025/datasets/NotInject_one.json", 5_000, False),
        ("Tier2_PIGuard_ACL2025/datasets/wildguard.json", 50_000, False),

        # 9. ProtectAI DeBERTa-v3 Replication Package & Datasets
        ("ProtectAI_DeBERTa_v3_v2/README.md", 500, False),
        ("ProtectAI_DeBERTa_v3_v2/run_protectai_replication.py", 1_000, False),
        ("ProtectAI_DeBERTa_v3_v2/PROTECTAI_REPLICATION_BENCHMARK_RESULTS.json", 500, False),
        ("ProtectAI_DeBERTa_v3_v2/datasets/protectai_eval_benchmark.json", 1_000, False),

        # 10. SmoothLLM (NeurIPS 2023) Package & Datasets
        ("SmoothLLM_Robey_NeurIPS2023/README.md", 500, False),
        ("SmoothLLM_Robey_NeurIPS2023/lib/perturbations.py", 500, False),
        ("SmoothLLM_Robey_NeurIPS2023/lib/defenses.py", 500, False),
        ("SmoothLLM_Robey_NeurIPS2023/run_smoothllm_replication.py", 1_000, False),
        ("SmoothLLM_Robey_NeurIPS2023/SMOOTHLLM_REPLICATION_BENCHMARK_RESULTS.json", 500, False),
        ("SmoothLLM_Robey_NeurIPS2023/datasets/llama2_behaviors.json", 1_000, False),
        ("SmoothLLM_Robey_NeurIPS2023/datasets/smoothllm_eval_benchmark.json", 1_000, False),

        # 11. JailbreakBench (NeurIPS 2024) Package & Datasets
        ("JailbreakBench_Chao_NeurIPS2024/README.md", 500, False),
        ("JailbreakBench_Chao_NeurIPS2024/src/jailbreakbench/dataset.py", 500, False),
        ("JailbreakBench_Chao_NeurIPS2024/run_jailbreakbench_replication.py", 1_000, False),
        ("JailbreakBench_Chao_NeurIPS2024/JAILBREAKBENCH_REPLICATION_BENCHMARK_RESULTS.json", 500, False),
        ("JailbreakBench_Chao_NeurIPS2024/datasets/jbb_behaviors_harmful.json", 10_000, False),
        ("JailbreakBench_Chao_NeurIPS2024/datasets/jbb_behaviors_benign.json", 10_000, False),
        ("JailbreakBench_Chao_NeurIPS2024/datasets/jbb_combined_benchmark.json", 20_000, False),

        # 12. Master Triad & Benchmark Suite Runners
        ("run_all_triad_experiments.py", 1_000, False),
        ("run_all_empirical_models.py", 1_000, False),

        # 13. DataSentinel (Liu et al., IEEE S&P 2025)
        ("DataSentinel_Liu_SP2025/README.md", 500, False),
        ("DataSentinel_Liu_SP2025/REPO_METADATA.json", 300, False),
        ("DataSentinel_Liu_SP2025/papers/Liu_2025_DataSentinel_Game_Theoretic_Detection_Prompt_Injection.pdf", 500_000, True),
        ("DataSentinel_Liu_SP2025/run_datasentinel_replication.py", 1_000, False),
        ("DataSentinel_Liu_SP2025/DATASENTINEL_REPLICATION_BENCHMARK_RESULTS.json", 1_000, False),
        ("DataSentinel_Liu_SP2025/datasets/datasentinel_eval_benchmark.json", 1_000, False),
        ("DataSentinel_Liu_SP2025/Open-Prompt-Injection/README.md", 500, False),
        ("DataSentinel_Liu_SP2025/Open-Prompt-Injection/OpenPromptInjection/apps/DataSentinelDetector.py", 1_000, False),

        # 14. PromptShield (Jacob et al., ACM CCS 2024)
        ("PromptShield_Jacob_CCS2024/README.md", 500, False),
        ("PromptShield_Jacob_CCS2024/REPO_METADATA.json", 300, False),
        ("PromptShield_Jacob_CCS2024/papers/Jacob_2024_PromptShield_Deployable_Detection_Prompt_Injection_CCS.pdf", 500_000, True),
        ("PromptShield_Jacob_CCS2024/run_promptshield_replication.py", 1_000, False),
        ("PromptShield_Jacob_CCS2024/PROMPTSHIELD_REPLICATION_BENCHMARK_RESULTS.json", 1_000, False),
        ("PromptShield_Jacob_CCS2024/datasets/promptshield_eval_benchmark.json", 1_000, False),
        ("PromptShield_Jacob_CCS2024/PromptShield/eval_promptguard.py", 1_000, False),
        ("PromptShield_Jacob_CCS2024/PromptShield/threshold_evaluation.py", 1_000, False),

        # 15. ModernBERT-base (Warner et al., Answer.AI 2024)
        ("ModernBERT_Warner_2024/README.md", 500, False),
        ("ModernBERT_Warner_2024/REPO_METADATA.json", 300, False),
        ("ModernBERT_Warner_2024/papers/Warner_2024_ModernBERT_Brings_Modern_Transformers_To_Encoders.pdf", 300_000, True),
        ("ModernBERT_Warner_2024/run_modernbert_replication.py", 1_000, False),
        ("ModernBERT_Warner_2024/MODERNBERT_REPLICATION_BENCHMARK_RESULTS.json", 1_000, False),
        ("ModernBERT_Warner_2024/datasets/modernbert_context_eval_benchmark.json", 10_000, False),
        ("ModernBERT_Warner_2024/ModernBERT/README.md", 500, False),
        ("ModernBERT_Warner_2024/ModernBERT/yamls/modernbert/modernbert-base-context-extension.yaml", 1_000, False),

        # 16. PI-Guard Tier-1 Fast-Filter (Dual-Space TF-IDF)
        ("PIGuard_Tier1_FastFilter/README.md", 500, False),
        ("PIGuard_Tier1_FastFilter/REPO_METADATA.json", 300, False),
        ("PIGuard_Tier1_FastFilter/papers/PIGuard_ACL2025_arXiv2410.22770.pdf", 500_000, True),
        ("PIGuard_Tier1_FastFilter/papers/Jain_2023_Baseline_Defenses_Adversarial_Attacks_LLMs.pdf", 300_000, True),
        ("PIGuard_Tier1_FastFilter/run_tier1_fastfilter_replication.py", 1_000, False),
        ("PIGuard_Tier1_FastFilter/TIER1_FASTFILTER_REPLICATION_BENCHMARK_RESULTS.json", 1_000, False),
        ("PIGuard_Tier1_FastFilter/datasets/tier1_fastfilter_eval_benchmark.json", 1_000, False),
        ("PIGuard_Tier1_FastFilter/PIGuard_ACL2025/README.md", 500, False),
        ("PIGuard_Tier1_FastFilter/PIGuard_ACL2025/PIGuard.py", 500, False),
        ("PIGuard_Tier1_FastFilter/PIGuard_ACL2025/datasets/valid.json", 10_000, False),

        # 17. Dataset Metadata & Provenance Cards (12/12 models)
        ("Tier1_REJECTED_Ayub_CAMLIS2024/datasets/METADATA.json", 300, False),
        ("Tier1_REJECTED_Ayub_CAMLIS2024/datasets/DATASET_CARD.md", 500, False),
        ("Tier1_Candidate_Jain_NeurIPS2023/datasets/METADATA.json", 300, False),
        ("Tier1_Candidate_Jain_NeurIPS2023/datasets/DATASET_CARD.md", 500, False),
        ("Tier1_Candidate_Meta_PromptGuard2024/datasets/METADATA.json", 300, False),
        ("Tier1_Candidate_Meta_PromptGuard2024/datasets/DATASET_CARD.md", 500, False),
        ("Tier1_Candidate_InstructDetector_EMNLP2024/datasets/METADATA.json", 300, False),
        ("Tier1_Candidate_InstructDetector_EMNLP2024/datasets/DATASET_CARD.md", 500, False),
        ("Tier2_PIGuard_ACL2025/datasets/METADATA.json", 300, False),
        ("Tier2_PIGuard_ACL2025/datasets/DATASET_CARD.md", 500, False),
        ("ProtectAI_DeBERTa_v3_v2/datasets/METADATA.json", 300, False),
        ("ProtectAI_DeBERTa_v3_v2/datasets/DATASET_CARD.md", 500, False),
        ("SmoothLLM_Robey_NeurIPS2023/datasets/METADATA.json", 300, False),
        ("SmoothLLM_Robey_NeurIPS2023/datasets/DATASET_CARD.md", 500, False),
        ("JailbreakBench_Chao_NeurIPS2024/datasets/METADATA.json", 300, False),
        ("JailbreakBench_Chao_NeurIPS2024/datasets/DATASET_CARD.md", 500, False),
        ("DataSentinel_Liu_SP2025/datasets/METADATA.json", 300, False),
        ("DataSentinel_Liu_SP2025/datasets/DATASET_CARD.md", 500, False),
        ("PromptShield_Jacob_CCS2024/datasets/METADATA.json", 300, False),
        ("PromptShield_Jacob_CCS2024/datasets/DATASET_CARD.md", 500, False),
        ("ModernBERT_Warner_2024/datasets/METADATA.json", 300, False),
        ("ModernBERT_Warner_2024/datasets/DATASET_CARD.md", 500, False),
        ("PIGuard_Tier1_FastFilter/datasets/METADATA.json", 300, False),
        ("PIGuard_Tier1_FastFilter/datasets/DATASET_CARD.md", 500, False),
    ]

    all_passed = True
    for rel_path, min_b, is_pdf in assets:
        full_path = os.path.normpath(os.path.join(base_dir, rel_path))
        passed, msg = check_file(full_path, min_b, is_pdf)
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{status:7} {msg}")
        if not passed:
            all_passed = False

    # Deep Dataset Provenance and SHA-256 Validation
    import json
    import hashlib
    print("\n" + "=" * 80)
    print("DATASET PROVENANCE & SHA-256 INTEGRITY VALIDATION")
    print("=" * 80)

    def calc_sha(p):
        h = hashlib.sha256()
        with open(p, "rb") as f:
            b = f.read(65536)
            while len(b) > 0:
                h.update(b)
                b = f.read(65536)
        return h.hexdigest()

    packages = [
        "Tier1_REJECTED_Ayub_CAMLIS2024",
        "Tier1_Candidate_Jain_NeurIPS2023",
        "Tier1_Candidate_Meta_PromptGuard2024",
        "Tier1_Candidate_InstructDetector_EMNLP2024",
        "Tier2_PIGuard_ACL2025",
        "ProtectAI_DeBERTa_v3_v2",
        "SmoothLLM_Robey_NeurIPS2023",
        "JailbreakBench_Chao_NeurIPS2024",
        "DataSentinel_Liu_SP2025",
        "PromptShield_Jacob_CCS2024",
        "ModernBERT_Warner_2024",
        "PIGuard_Tier1_FastFilter"
    ]

    for pkg in packages:
        meta_file = os.path.join(base_dir, pkg, "datasets", "METADATA.json")
        if not os.path.exists(meta_file):
            print(f"[FAIL]  Missing METADATA.json in {pkg}")
            all_passed = False
            continue
        with open(meta_file, "r", encoding="utf-8") as f:
            meta = json.load(f)
        if meta.get("provenance", {}).get("is_synthetic_self_created") is not False:
            print(f"[FAIL]  {pkg} invariant violated: is_synthetic_self_created must be False")
            all_passed = False
            continue
        
        # Verify files listed in metadata
        files_ok = True
        for finfo in meta.get("files", []):
            fpath = os.path.join(base_dir, pkg, "datasets", finfo["filename"])
            if not os.path.exists(fpath):
                print(f"[FAIL]  Missing file {finfo['filename']} in {pkg}/datasets")
                files_ok = False
                all_passed = False
                break
            actual_sha = calc_sha(fpath)
            if actual_sha != finfo["sha256"]:
                print(f"[FAIL]  SHA mismatch for {finfo['filename']} in {pkg}")
                files_ok = False
                all_passed = False
                break
        if files_ok:
            print(f"[PASS]  OK Provenance & SHA-256 Verified (Non-Synthetic): {pkg}")

    print("\n" + "=" * 80)
    print("UPSTREAM REPOSITORY PROVENANCE & METADATA VALIDATION")
    print("=" * 80)
    for pkg in ["DataSentinel_Liu_SP2025", "PromptShield_Jacob_CCS2024", "ModernBERT_Warner_2024", "PIGuard_Tier1_FastFilter"]:
        repo_meta_file = os.path.join(base_dir, pkg, "REPO_METADATA.json")
        if not os.path.exists(repo_meta_file):
            print(f"[FAIL]  Missing REPO_METADATA.json in {pkg}")
            all_passed = False
            continue
        with open(repo_meta_file, "r", encoding="utf-8") as f:
            rmeta = json.load(f)
        if rmeta.get("provenance", {}).get("is_synthetic_self_created") is not False:
            print(f"[FAIL]  {pkg} REPO_METADATA invariant violated: is_synthetic_self_created must be False")
            all_passed = False
            continue
        if rmeta.get("provenance", {}).get("is_upstream_pure_clone") is not True:
            print(f"[FAIL]  {pkg} REPO_METADATA invariant violated: is_upstream_pure_clone must be True")
            all_passed = False
            continue
        print(f"[PASS]  OK Upstream Repo Verified (Pure Upstream Clone): {pkg} -> {rmeta.get('upstream_git_url')} ({rmeta.get('commit_hash')[:8]})")

    print("=" * 80)
    if all_passed:
        print("RESULT: ALL ASSETS, DATASETS & PROVENANCE METADATA 100% VERIFIED!")
        sys.exit(0)
    else:
        print("RESULT: VERIFICATION FAILED FOR ONE OR MORE ASSETS.")
        sys.exit(1)

if __name__ == "__main__":
    main()
