"""
workspaces/truongnv/reports/tasks_for_meeting_6/scripts/reproduce_all_benchmarks.py

PI-Guard Master 1-Click Reproducibility Script.
Standardized Reproducibility Pipeline (Quy trình thực nghiệm tái lập hệ thống):
Executes the complete empirical verification pipeline and generates all benchmark metrics,
adversarial tests, and publication-quality figures with zero manual intervention.

Pipeline Steps:
1. Gray-Box Adaptive Adversarial Evaluation (Token Dilution, OOV Gate, MOF Invariance)
2. Prioritized Tail-and-Head Scanning & Early Stopping Benchmark (Prompt Overflow resistance)
3. Cross-Dataset Master Benchmark (600 samples, 95% Wilson Score CIs, McNemar Chi-Square Tests)
4. Scientific Publication Figure Generation (4 PNG charts)
5. Comprehensive Executive Verification Summary

Usage:
    .\\.venv\\Scripts\\python.exe workspaces/truongnv/reports/tasks_for_meeting_6/scripts/reproduce_all_benchmarks.py
"""

import sys
import os
import subprocess
import time
import json

if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
PYTHON_EXE = sys.executable

def print_banner(title: str):
    width = 80
    print("\n" + "=" * width)
    print(f" {title.center(width - 2)}")
    print("=" * width)

def run_step(step_num: int, step_name: str, cmd: list) -> bool:
    print_banner(f"[STEP {step_num}] {step_name}")
    print(f"Executing: {' '.join(cmd)}")
    t0 = time.perf_counter()
    try:
        result = subprocess.run(cmd, cwd=BASE_DIR, capture_output=True, text=True, encoding='utf-8')
        elapsed = time.perf_counter() - t0
        print(result.stdout)
        if result.stderr:
            print("[STDERR / WARNINGS]:", result.stderr[-500:])
        if result.returncode == 0:
            print(f"✔ [PASS] {step_name} completed successfully in {elapsed:.2f}s (Exit code 0)")
            return True
        else:
            print(f"✖ [FAIL] {step_name} failed with exit code {result.returncode} in {elapsed:.2f}s")
            return False
    except Exception as e:
        print(f"✖ [ERROR] Exception executing {step_name}: {e}")
        return False

def main():
    print_banner("PI-GUARD MASTER 1-CLICK EMPIRICAL REPRODUCIBILITY SUITE")
    print("Academic Program: Bachelor of Science in Information Assurance (IAP491), FPT University")
    print(f"Python Runtime:   {PYTHON_EXE}")
    print(f"Base Directory:   {BASE_DIR}")
    start_all = time.perf_counter()

    test_script_1 = os.path.join(BASE_DIR, "tests", "test_adaptive_token_dilution.py")
    test_script_2 = os.path.join(BASE_DIR, "tests", "test_hidden_prompt_at_tail.py")
    bench_script  = os.path.join(BASE_DIR, "scripts", "run_cross_dataset_benchmark.py")
    figure_script = os.path.join(BASE_DIR, "scripts", "generate_benchmark_figures.py")

    results = {}

    # Step 1: Adaptive Adversarial Tests
    results["Step 1: Gray-Box Adaptive Adversarial Tests"] = run_step(
        1, "Gray-Box Adaptive Adversarial Evaluation", [PYTHON_EXE, test_script_1]
    )

    # Step 2: Tail-and-Head Scanning Test (Uses --fast to avoid 2.5 minute sequential scan unless --full is requested)
    fast_flag = [] if "--full" in sys.argv else ["--fast"]
    results["Step 2: Head-and-Tail Priority Scanning"] = run_step(
        2, "Tail Injection Early-Stopping Benchmark", [PYTHON_EXE, test_script_2] + fast_flag
    )

    # Step 3: Cross-Dataset Master Benchmark
    results["Step 3: Cross-Dataset Master Benchmark (600 Samples)"] = run_step(
        3, "Cross-Dataset Empirical Matrix & McNemar Tests", [PYTHON_EXE, bench_script]
    )

    # Step 4: Publication Figures
    results["Step 4: Publication Figure Generation"] = run_step(
        4, "Scientific Figure Generation (4 PNGs)", [PYTHON_EXE, figure_script]
    )

    # Final Summary
    total_time = time.perf_counter() - start_all
    print_banner("MASTER REPRODUCIBILITY VERIFICATION SUMMARY")
    all_passed = True
    for name, passed in results.items():
        status_str = "✔ PASS" if passed else "✖ FAIL"
        if not passed:
            all_passed = False
        print(f"  {name:<60} : {status_str}")

    print("-" * 80)
    print(f"Total Execution Time: {total_time:.2f} seconds")

    # Load matrix results to display final key indicators
    matrix_file = os.path.join(BASE_DIR, "04_benchmarks_and_data", "cross_dataset_empirical_matrix.json")
    if os.path.exists(matrix_file):
        with open(matrix_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        piguard = data.get("models_matrix", {}).get("M_PI_PIGuard_Cascade", {})
        d1 = piguard.get("D1_PIGuard_Valid", {})
        d2 = piguard.get("D2_BIPIA_Indirect", {})
        d3 = piguard.get("D3_JailbreakBench", {})
        d5 = piguard.get("D5_NotInject_Code", {})
        d6 = piguard.get("D6_WildGuard_Benign", {})

        print("\n[KEY EMPIRICAL METRICS - PI-GUARD CHAMPION ARCHITECTURE]:")
        print(f"  • Direct Injection Recall (D1):   {d1.get('recall_pct', 'N/A')}% [95% CI: {d1.get('ci_95', [])}]")
        print(f"  • Indirect Injection Recall (D2): {d2.get('recall_pct', 'N/A')}% [95% CI: {d2.get('ci_95', [])}]")
        print(f"  • Jailbreak Recall (D3):          {d3.get('recall_pct', 'N/A')}% [95% CI: {d3.get('ci_95', [])}]")
        print(f"  • Code Benign Preservation (D5):  {d5.get('score', 'N/A')}% [95% CI: {d5.get('ci_95', [])}]")
        print(f"  • Benign False Positive Rate (D6):{d6.get('fpr_pct', 'N/A')}% [95% CI: {d6.get('ci_95', [])}]")
        print(f"  • CPU Mean Latency (D1):          {d1.get('mean_latency_ms', 'N/A')} ms (P95: {d1.get('p95_latency_ms', 'N/A')} ms)")

    if all_passed:
        print("\n🎉 ALL 4 REPRODUCIBILITY PHASES PASSED 100%! READY FOR CAPSTONE DEFENSE.")
        sys.exit(0)
    else:
        print("\n⚠️ SOME REPRODUCIBILITY PHASES FAILED. PLEASE INSPECT LOGS ABOVE.")
        sys.exit(1)

if __name__ == "__main__":
    main()
