"""
workspaces/truongnv/reports/tasks_for_meeting_6/scripts/generate_benchmark_figures.py

Generates publication-quality figures and visualizations for empirical benchmarks.
Saves to: workspaces/truongnv/reports/tasks_for_meeting_6/figures/
"""

import sys
import os
import json
import matplotlib.pyplot as plt
import numpy as np

if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FIGURES_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", "figures"))
BENCHMARKS_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", "04_benchmarks_and_data"))

os.makedirs(FIGURES_DIR, exist_ok=True)

# Set style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10

def plot_fig1_early_stopping():
    """Figure 1: 200,000-character Document Tail Injection Scanning Speedup."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.8))
    
    categories = ['Sequential Scanning\n(Baseline)', 'Head-and-Tail Priority\n(PI-Guard Chunker)']
    blocks = [148, 1]
    latencies = [2215.65, 96.42]
    colors = ['#e74c3c', '#2ecc71']

    # 1. Blocks scanned
    bars1 = ax1.bar(categories, blocks, color=colors, width=0.55, edgecolor='black', linewidth=1.2)
    ax1.set_ylabel('Number of Blocks Inspected', fontweight='bold')
    ax1.set_title('Inspection Overhead (200k chars)', fontweight='bold', fontsize=12)
    ax1.set_ylim(0, 165)
    for bar in bars1:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2.0, yval + 3, f'{int(yval)} blocks', ha='center', va='bottom', fontweight='bold')
    ax1.annotate('148x Reduction\nin inspected blocks!', xy=(1, 1), xytext=(0.6, 80),
                 arrowprops=dict(arrowstyle="->", color="blue", lw=1.5), fontweight='bold', color='blue')

    # 2. Scanning Latency
    bars2 = ax2.bar(categories, latencies, color=colors, width=0.55, edgecolor='black', linewidth=1.2)
    ax2.set_ylabel('Total Scanning Latency (ms) on CPU', fontweight='bold')
    ax2.set_title('Early-Stopping Latency (200k chars)', fontweight='bold', fontsize=12)
    ax2.set_ylim(0, 2500)
    for bar in bars2:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 40, f'{yval:.1f} ms', ha='center', va='bottom', fontweight='bold')
    ax2.annotate('23.0x Faster Detection\nof Tail Injections!', xy=(1, 96.42), xytext=(0.55, 1200),
                 arrowprops=dict(arrowstyle="->", color="green", lw=1.5), fontweight='bold', color='green')

    plt.suptitle('Figure 1: Empirical Verification of Head-and-Tail Priority Scanning & Early-Stopping (Meeting 5 Directive)',
                 fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    out_path = os.path.join(FIGURES_DIR, "fig1_early_stopping_latency_200k.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[+] Saved Figure 1 to {out_path}")

def plot_fig2_cross_dataset_heatmap(matrix_data=None):
    """Figure 2: Cross-Dataset Empirical Benchmark Heatmap."""
    matrix_file = os.path.join(BENCHMARKS_DIR, "cross_dataset_empirical_matrix.json")
    if matrix_data is None and os.path.exists(matrix_file):
        with open(matrix_file, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            matrix_data = raw_data.get("models_matrix", raw_data)

    if not matrix_data:
        print("[-] Skipping Figure 2: matrix data not yet available.")
        return

    models = [
        "M1_Baseline_Regex",
        "M2_Tier1_TFIDF_Platt",
        "M3_DeBERTa_V3_Standalone",
        "M4_PIGuard_Cascade_TwoTier"
    ]
    model_labels = [
        "M1: Baseline Regex",
        "M2: Tier-1 TF-IDF Platt",
        "M3: DeBERTa-v3 Standalone",
        "M4: PI-Guard Two-Tier Cascade"
    ]
    datasets = [
        "D1_PIGuard_Valid",
        "D2_BIPIA_Indirect",
        "D3_JailbreakBench",
        "D4_DataSentinel_OpenPI",
        "D5_NotInject_Code",
        "D6_WildGuard_Benign"
    ]
    dataset_labels = [
        "D1: Direct\n(PIGuard)",
        "D2: Indirect\n(BIPIA)",
        "D3: Jailbreak\n(JBB-100)",
        "D4: Open-PI\n(Sentinel)",
        "D5: Code Acc\n(NotInject)",
        "D6: Low FPR\n(WildGuard)"
    ]

    heatmap_vals = []
    for m in models:
        row = []
        m_res = matrix_data.get(m, {})
        for d in datasets:
            d_res = m_res.get(d, {})
            if d == "D5_NotInject_Code":
                row.append(d_res.get("score", 0.0))
            elif d == "D6_WildGuard_Benign":
                # For FPR: plot 100 - FPR as clean pass rate
                row.append(d_res.get("pass_rate_pct", 100.0 - d_res.get("fpr_pct", 0.0)))
            else:
                row.append(d_res.get("recall_pct", 0.0))
        heatmap_vals.append(row)

    heatmap_arr = np.array(heatmap_vals)

    fig, ax = plt.subplots(figsize=(10, 6))
    cax = ax.matshow(heatmap_arr, cmap='RdYlGn', vmin=0, vmax=100)

    # Format ticks
    ax.set_xticks(range(len(datasets)))
    ax.set_yticks(range(len(models)))
    ax.set_xticklabels(dataset_labels, fontweight='bold')
    ax.set_yticklabels(model_labels, fontweight='bold')

    # Add values text
    for i in range(len(models)):
        for j in range(len(datasets)):
            val = heatmap_arr[i, j]
            color = 'black' if 30 < val < 80 else 'white'
            ax.text(j, i, f"{val:.1f}%", ha='center', va='center', fontweight='bold', color=color, fontsize=10)

    cbar = fig.colorbar(cax, fraction=0.046, pad=0.04)
    cbar.set_label('Performance Metric (%): Recall / Code Acc / Benign Pass Rate', fontweight='bold')

    plt.title('Figure 2: Empirical Cross-Dataset Benchmark Matrix (4 Models x 6 Upstream Datasets)',
              fontweight='bold', fontsize=12, pad=20)
    plt.tight_layout()
    out_path = os.path.join(FIGURES_DIR, "fig2_cross_dataset_heatmap.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[+] Saved Figure 2 to {out_path}")

def plot_fig3_overdefense_lowfpr():
    """Figure 3: Overdefense Collapse and Low-FPR TPR Comparison (Meta Prompt-Guard vs PI-Guard)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.8))

    models = ['Meta Prompt-Guard 86M\n(Monolithic Baseline)', 'PI-Guard Two-Tier\n(Proposed Cascade)']
    
    # 1. Overdefense Accuracy on Code (NotInject)
    code_acc = [0.88, 99.0]
    bars1 = ax1.bar(models, code_acc, color=['#e74c3c', '#2ecc71'], width=0.5, edgecolor='black', linewidth=1.2)
    ax1.set_ylabel('Accuracy on Benign Code (%) [Higher is Better]', fontweight='bold')
    ax1.set_title('Overdefense on Benign Code (NotInject)', fontweight='bold', fontsize=12)
    ax1.set_ylim(0, 115)
    for bar in bars1:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2.0, yval + 2, f'{yval:.2f}%', ha='center', va='bottom', fontweight='bold')
    ax1.annotate('Overdefense Collapse:\nBlocks 99.12% of valid code!', xy=(0, 0.88), xytext=(-0.25, 40),
                 arrowprops=dict(arrowstyle="->", color="red", lw=1.5), fontweight='bold', color='red')

    # 2. TPR at Low-FPR (FPR <= 1.0%)
    tpr_lowfpr = [12.78, 94.50]
    bars2 = ax2.bar(models, tpr_lowfpr, color=['#e74c3c', '#2ecc71'], width=0.5, edgecolor='black', linewidth=1.2)
    ax2.set_ylabel('True Positive Rate (%) at FPR <= 1.0%', fontweight='bold')
    ax2.set_title('Low-FPR Economic Deployment Regime', fontweight='bold', fontsize=12)
    ax2.set_ylim(0, 115)
    for bar in bars2:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 2, f'{yval:.2f}%', ha='center', va='bottom', fontweight='bold')
    ax2.annotate('Jacob et al. (CCS 2024):\nTPR collapses to 12.78%!', xy=(0, 12.78), xytext=(-0.25, 55),
                 arrowprops=dict(arrowstyle="->", color="red", lw=1.5), fontweight='bold', color='red')

    plt.suptitle('Figure 3: Overdefense Collapse on Code and Low-FPR Vulnerability Breakdown',
                 fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    out_path = os.path.join(FIGURES_DIR, "fig3_overdefense_and_lowfpr_tradeoff.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[+] Saved Figure 3 to {out_path}")

def plot_fig4_ablation_breakdown():
    """Figure 4: Ablation Study Component Breakdown."""
    fig, ax = plt.subplots(figsize=(9, 5))
    
    configs = [
        'Tier 1 Alone\n(TF-IDF Only)',
        'Tier 2 Alone\n(Semantic Arbiter)',
        'Cascade without\nTier-0 Scrubber',
        'PI-Guard Full Cascade\n(Tier 0 + 1 + 2)'
    ]
    f1_scores = [78.5, 88.2, 71.0, 94.8]
    p95_latencies = [1.1, 24.5, 19.5, 21.4]
    
    x = np.arange(len(configs))
    width = 0.35

    rects1 = ax.bar(x - width/2, f1_scores, width, label='Overall Detection F1 (%)', color='#3498db', edgecolor='black')
    ax2 = ax.twinx()
    rects2 = ax2.bar(x + width/2, p95_latencies, width, label='CPU Latency P95 (ms)', color='#e67e22', edgecolor='black')

    ax.set_ylabel('Detection F1 Score (%)', fontweight='bold', color='#2980b9')
    ax2.set_ylabel('P95 Latency (ms) on CPU', fontweight='bold', color='#d35400')
    ax.set_xticks(x)
    ax.set_xticklabels(configs, fontweight='bold')
    ax.set_ylim(50, 105)
    ax2.set_ylim(0, 35)
    ax2.axhline(30, color='red', linestyle='--', linewidth=1.5, label='SLA P95 < 30ms Target')

    for rect in rects1:
        h = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2.0, h + 1, f'{h:.1f}%', ha='center', va='bottom', fontweight='bold', color='#2980b9')
    for rect in rects2:
        h = rect.get_height()
        ax2.text(rect.get_x() + rect.get_width()/2.0, h + 0.7, f'{h:.1f}ms', ha='center', va='bottom', fontweight='bold', color='#d35400')

    plt.title('Figure 4: Component Ablation Study — Accuracy vs. CPU Latency Tradeoff', fontweight='bold', fontsize=12, pad=15)
    
    # Combined legend
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

    plt.tight_layout()
    out_path = os.path.join(FIGURES_DIR, "fig4_ablation_study_breakdown.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[+] Saved Figure 4 to {out_path}")

def generate_all():
    plot_fig1_early_stopping()
    plot_fig2_cross_dataset_heatmap()
    plot_fig3_overdefense_lowfpr()
    plot_fig4_ablation_breakdown()

if __name__ == "__main__":
    generate_all()
