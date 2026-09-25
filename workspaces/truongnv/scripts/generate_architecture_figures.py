"""
workspaces/truongnv/scripts/generate_architecture_figures.py

Generates professional, publication-grade architectural diagrams and empirical
algorithm illustrations for Section 03 of the PI-Guard presentation deck.
Saves figures to: workspaces/truongnv/reports/tasks_for_meeting_6/figures/

Audit Fixes:
1. Removed all dark blue/black background palettes (#0F172A). Applied clean, high-contrast academic light palette.
2. Eliminated all line/arrow/text collisions:
   - Fig 1: Separated Router branch routes cleanly so arrows never cross Tier 2 box or text.
   - Fig 2: Repositioned callout boxes to empty zones away from vertical threshold lines and curve intersections.
   - Fig 3: Replaced dark banner with light academic card; clean inter-box arrows.
   - Fig 4: Moved legend to upper left; shifted ECE callout away from Platt red curve.
   - Fig 5: Moved MOF formula callout to top-left empty zone away from purple diagonal line; eliminated cross-bar annotations.
   - Fig 6: Separated annotation arrow and text box in Subplot 2 so arrow never cuts through text.
"""

import sys
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FIGURES_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", "reports", "tasks_for_meeting_6", "figures"))
os.makedirs(FIGURES_DIR, exist_ok=True)

# Styling setup
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.edgecolor'] = '#CBD5E1'
plt.rcParams['axes.linewidth'] = 1.0


# -----------------------------------------------------------------------------
# FIGURE 1: Master Architecture Pipeline Diagram (Overview)
# -----------------------------------------------------------------------------
def generate_fig_arch_pipeline_overview():
    fig, ax = plt.subplots(figsize=(12, 5.2), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Color Palette (Academic Light)
    c_blue = '#1E3A8A'    # Navy
    c_amber = '#D97706'   # Amber
    c_green = '#15803D'   # Green
    c_purple = '#7E22CE'  # Purple
    c_red = '#B91C1C'     # Red

    # Title Banner
    ax.text(50, 95.5, "PI-GUARD TWO-TIER CASCADED INGRESS GUARDRAIL PIPELINE", 
            ha='center', va='center', fontsize=13, fontweight='bold', color=c_blue)
    ax.text(50, 91, "End-to-End Processing: Dual TF-IDF Fast Filter + Tri-State Uncertainty Router + DeBERTa-v3 MOF", 
            ha='center', va='center', fontsize=9.5, fontstyle='italic', color='#475569')

    # Box 1: Input Ingress
    box_input = patches.FancyBboxPatch((2, 36), 13, 44, boxstyle="square,pad=0.5", 
                                      facecolor='#EFF6FF', edgecolor=c_blue, linewidth=1.5)
    ax.add_patch(box_input)
    ax.text(8.5, 74, "INGRESS PROMPT", ha='center', va='center', fontsize=8.5, fontweight='bold', color=c_blue)
    ax.text(8.5, 65, "X = S || U", ha='center', va='center', fontsize=10.5, fontweight='bold', color='#0F172A')
    ax.text(8.5, 53, "• User Prompt (U)\n• RAG Context (S)\n• Token seq X", ha='center', va='center', fontsize=7.5, color='#334155')
    ax.text(8.5, 41, "Black-Box API", ha='center', va='center', fontsize=7.2, fontweight='bold', color='#2563EB')

    # Arrow 1 -> 2
    ax.annotate("", xy=(18.5, 58), xytext=(15.0, 58),
                arrowprops=dict(arrowstyle="->", color='#64748B', lw=1.8))

    # Box 2: Tier 0 Scrubber
    box_t0 = patches.FancyBboxPatch((18.5, 36), 14.5, 44, boxstyle="square,pad=0.5", 
                                    facecolor='#FFFBEB', edgecolor=c_amber, linewidth=1.5)
    ax.add_patch(box_t0)
    ax.text(25.75, 74, "TIER 0 SCRUBBER", ha='center', va='center', fontsize=8.5, fontweight='bold', color=c_amber)
    ax.text(25.75, 66, "Cú Pháp & Khử Lách", ha='center', va='center', fontsize=8.2, fontweight='bold', color='#78350F')
    ax.text(25.75, 53, "• Unicode NFKC\n• Khử Zero-Width\n• Decode Base64/Hex\n• Tiếng Việt đối kháng", ha='center', va='center', fontsize=7.2, color='#451A03')
    ax.text(25.75, 41, "Latency: < 0.1ms", ha='center', va='center', fontsize=7.2, fontweight='bold', color=c_amber)

    # Arrow 2 -> 3
    ax.annotate("", xy=(36.5, 58), xytext=(33.0, 58),
                arrowprops=dict(arrowstyle="->", color='#64748B', lw=1.8))

    # Box 3: Tier 1 Fast Filter
    box_t1 = patches.FancyBboxPatch((36.5, 36), 15, 44, boxstyle="square,pad=0.5", 
                                    facecolor='#F0FDF4', edgecolor=c_green, linewidth=1.5)
    ax.add_patch(box_t1)
    ax.text(44, 74, "TIER 1 FAST FILTER", ha='center', va='center', fontsize=8.5, fontweight='bold', color=c_green)
    ax.text(44, 66, "Dual TF-IDF + Platt", ha='center', va='center', fontsize=8.2, fontweight='bold', color='#14532D')
    ax.text(44, 53, "• Word 1-3g (20k)\n• Char_wb 3-5g (30k)\n• Linear Sparse Dot\n• Platt Sigmoid P(X)", ha='center', va='center', fontsize=7.2, color='#14532D')
    ax.text(44, 41, "Latency: <= 0.5ms CPU", ha='center', va='center', fontsize=7.2, fontweight='bold', color=c_green)

    # Arrow 3 -> Router
    ax.annotate("", xy=(55, 58), xytext=(51.5, 58),
                arrowprops=dict(arrowstyle="->", color='#64748B', lw=1.8))

    # Box 4: Tri-State Router (Extended Height, Clean Inner Tracks)
    box_router = patches.FancyBboxPatch((55, 30), 16.5, 54, boxstyle="square,pad=0.5", 
                                        facecolor='#F8FAFC', edgecolor='#334155', linewidth=1.8)
    ax.add_patch(box_router)
    ax.text(63.25, 78, "TRI-STATE ROUTER", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#0F172A')
    ax.text(63.25, 72.5, "Chow (1970) / CASCADE", ha='center', va='center', fontsize=7.5, fontstyle='italic', color='#475569')
    
    # 3 Separate Horizontal Tracks inside Router
    ax.text(63.25, 62, "Fast-Pass (71.3%)\nP < 0.15", ha='center', va='center', fontsize=7.2, fontweight='bold', color=c_green)
    ax.text(63.25, 48, "Escalate (17.4%)\n0.15 <= P <= 0.85", ha='center', va='center', fontsize=7.2, fontweight='bold', color=c_purple)
    ax.text(63.25, 36, "Early-Block (11.3%)\nP > 0.85", ha='center', va='center', fontsize=7.2, fontweight='bold', color=c_red)

    # Destination Boxes on Right
    box_allow = patches.FancyBboxPatch((89, 68), 9.5, 16, boxstyle="square,pad=0.4", 
                                       facecolor='#DCFCE7', edgecolor=c_green, linewidth=1.5)
    ax.add_patch(box_allow)
    ax.text(93.75, 78, "ALLOW", ha='center', va='center', fontsize=9, fontweight='bold', color=c_green)
    ax.text(93.75, 72, "Forward to\nTarget LLM", ha='center', va='center', fontsize=7.2, fontweight='bold', color='#14532D')

    box_block = patches.FancyBboxPatch((89, 18), 9.5, 16, boxstyle="square,pad=0.4", 
                                       facecolor='#FEE2E2', edgecolor=c_red, linewidth=1.5)
    ax.add_patch(box_block)
    ax.text(93.75, 28, "BLOCK", ha='center', va='center', fontsize=9, fontweight='bold', color=c_red)
    ax.text(93.75, 22, "HTTP 403\nPayload Alert", ha='center', va='center', fontsize=7.2, fontweight='bold', color='#7F1D1D')

    # Box 5: Tier 2 DeBERTa-v3 MOF (Placed strictly in the middle Y=[38, 58])
    box_t2 = patches.FancyBboxPatch((74, 38), 12.5, 22, boxstyle="square,pad=0.5", 
                                    facecolor='#FAF5FF', edgecolor=c_purple, linewidth=1.5)
    ax.add_patch(box_t2)
    ax.text(80.25, 55, "TIER 2 ARBITER", ha='center', va='center', fontsize=7.8, fontweight='bold', color=c_purple)
    ax.text(80.25, 48, "DeBERTa-v3 FP32\n+ MOF Invariance", ha='center', va='center', fontsize=7.2, fontweight='bold', color='#581C87')
    ax.text(80.25, 42, "18.5ms CPU | 99% Acc", ha='center', va='center', fontsize=6.8, color='#581C87')

    # NON-OVERLAPPING ROUTER BRANCH ARROWS:
    # 1. Top branch (Fast-Pass): Exits at y=68, goes directly to Allow box (strictly above Tier 2 box at y=58)
    ax.annotate("", xy=(89, 76), xytext=(71.5, 68),
                arrowprops=dict(arrowstyle="->", color=c_green, lw=2.0))
    ax.text(78.5, 75, "71.3% Pass", fontsize=7.2, fontweight='bold', color=c_green, ha='center', va='bottom')

    # 2. Middle branch (Escalate): Exits at y=48, goes straight horizontally into Tier 2 box
    ax.annotate("", xy=(74, 48), xytext=(71.5, 48),
                arrowprops=dict(arrowstyle="->", color=c_purple, lw=2.0))

    # 3. Bottom branch (Early-Block): Exits at y=34, goes directly to Block box (strictly below Tier 2 box at y=38)
    ax.annotate("", xy=(89, 25), xytext=(71.5, 32),
                arrowprops=dict(arrowstyle="->", color=c_red, lw=2.0))
    ax.text(78.5, 26, "11.3% Block", fontsize=7.2, fontweight='bold', color=c_red, ha='center', va='top')

    # Tier 2 outputs to Allow / Block (short clean dashed arrows in gap x=[86.5, 89])
    ax.annotate("", xy=(89, 70), xytext=(86.5, 54),
                arrowprops=dict(arrowstyle="->", color=c_green, lw=1.5, ls="--"))
    ax.annotate("", xy=(89, 30), xytext=(86.5, 42),
                arrowprops=dict(arrowstyle="->", color=c_red, lw=1.5, ls="--"))

    # Bottom Metrics Summary Banner (CLEAN LIGHT CARD - NO DARK/BLACK BACKGROUND!)
    summary_box = patches.FancyBboxPatch((2, 4), 96.5, 14, boxstyle="square,pad=0.5", 
                                        facecolor='#F8FAFC', edgecolor='#94A3B8', linewidth=1.2)
    ax.add_patch(summary_box)
    ax.text(4, 13.5, "PI-GUARD PERFORMANCE GUARANTEES:", fontsize=8.5, fontweight='bold', color=c_blue)
    metrics_line1 = "• Offload Rate: 82.6% traffic resolved at Tier 1 (<= 0.5ms)   |   • End-to-End Latency P95: < 25ms on Commodity CPU   |   • RAM Footprint: < 1.8GB"
    metrics_line2 = "• False Positive Rate (FPR): < 1.5% at Strict Economic Regime   |   • Code Protection (NotInject): 99.00% Accuracy via MOF Invariance (ACL 2025)"
    ax.text(4, 9.5, metrics_line1, fontsize=7.5, color='#1E293B')
    ax.text(4, 6.0, metrics_line2, fontsize=7.5, color='#1E293B')

    plt.tight_layout()
    output_path = os.path.join(FIGURES_DIR, "fig_arch_pipeline_overview.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
    plt.close()
    print(f"[+] Successfully generated: {output_path}")


# -----------------------------------------------------------------------------
# FIGURE 2: Tri-State Routing vs. 1-0 Binary Classification
# -----------------------------------------------------------------------------
def generate_fig_tristate_vs_binary():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.0), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax1.set_facecolor('#FFFFFF')
    ax2.set_facecolor('#FFFFFF')

    x = np.linspace(0, 1, 500)
    
    # Benign and Malicious probability density approximations
    benign_density = 3.5 * np.exp(-((x - 0.10)**2) / (2 * 0.08**2)) + 0.3 * np.exp(-((x - 0.45)**2) / (2 * 0.12**2))
    attack_density = 3.2 * np.exp(-((x - 0.90)**2) / (2 * 0.08**2)) + 0.5 * np.exp(-((x - 0.55)**2) / (2 * 0.12**2))

    # --- SUBPLOT 1: TRADITIONAL 1-0 BINARY CLASSIFIER ---
    ax1.plot(x, benign_density, color='#0284C7', lw=2.2, label='Benign Prompts Distribution')
    ax1.plot(x, attack_density, color='#DC2626', lw=2.2, label='Attack Prompts Distribution')
    
    # Single hard threshold at tau = 0.50
    tau_binary = 0.50
    ax1.axvline(tau_binary, color='#0F172A', linestyle='--', lw=2.0, label='Hard Binary Threshold (tau = 0.50)')

    # Shading Error Zones
    fp_mask = (x >= tau_binary)
    fn_mask = (x < tau_binary)
    ax1.fill_between(x[fp_mask], benign_density[fp_mask], color='#F87171', alpha=0.45, label='False Positives (Overdefense)')
    ax1.fill_between(x[fn_mask], attack_density[fn_mask], color='#60A5FA', alpha=0.45, label='False Negatives (Bypassed Attack)')

    ax1.set_title("A. TRUYỀN THỐNG: PHÂN LOẠI NHỊ PHÂN CỨNG 1 - 0\n(Hard Binary Decision Boundary tau = 0.5)", 
                  fontsize=10.5, fontweight='bold', color='#1E293B')
    ax1.set_xlabel("Xác Suất Dự Báo Độc Hại P(Malicious | X)", fontsize=9, fontweight='bold')
    ax1.set_ylabel("Mật Độ Phân Bố (Density)", fontsize=9, fontweight='bold')
    ax1.set_ylim(0, 5.5)
    ax1.set_xlim(0, 1.0)
    ax1.legend(loc='upper left', fontsize=7.2, framealpha=0.95, edgecolor='#94A3B8')
    
    # Callout placed in the EMPTY valley at x=0.24, y=2.6 with pointer to tau=0.50 at (0.48, 0.7)
    # ZERO overlap with the vertical threshold line at x=0.50 or curves!
    ax1.annotate("VÙNG RANH GIỚI MỜ (GREY ZONE)\nBị ép quyết định nhị phân gây lỗi kép\n(Tăng FPR hoặc Bỏ lọt Injection)", 
                 xy=(0.48, 0.7), xytext=(0.24, 2.6),
                 ha='center', va='center', fontsize=7.6, fontweight='bold', color='#7F1D1D',
                 bbox=dict(boxstyle="square,pad=0.4", fc="#FEF2F2", ec="#EF4444", lw=1.2),
                 arrowprops=dict(arrowstyle="->", color='#EF4444', lw=1.5),
                 zorder=5)

    # --- SUBPLOT 2: PI-GUARD TRI-STATE UNCERTAINTY ROUTING ---
    ax2.plot(x, benign_density, color='#0284C7', lw=2.2, label='Benign Distribution')
    ax2.plot(x, attack_density, color='#DC2626', lw=2.2, label='Attack Distribution')

    tau_low = 0.15
    tau_high = 0.85
    ax2.axvline(tau_low, color='#15803D', linestyle='-', lw=2.2, label='tau_low = 0.15 (Fast-Pass Bound)')
    ax2.axvline(tau_high, color='#B91C1C', linestyle='-', lw=2.2, label='tau_high = 0.85 (Early-Drop Bound)')

    # Shading 3 partitions
    ax2.axvspan(0.0, tau_low, color='#DCFCE7', alpha=0.55, label='LUỒNG 1: Fast-Pass (71.3% CPU < 0.5ms)')
    ax2.axvspan(tau_low, tau_high, color='#F3E8FF', alpha=0.55, label='LUỒNG 3: Escalate Tier 2 (17.4% Transformer)')
    ax2.axvspan(tau_high, 1.0, color='#FEE2E2', alpha=0.55, label='LUỒNG 2: Early-Block (11.3% CPU < 0.5ms)')

    ax2.set_title("B. PI-GUARD: ĐỊNH TUYẾN BẤT ĐỊNH 3 LUỒNG (TRI-STATE)\n(Chow 1970 Reject Option & CASCADE Luo & Han 2026)", 
                  fontsize=10.5, fontweight='bold', color='#1E293B')
    ax2.set_xlabel("Xác Suất Dự Báo Độc Hại P(Malicious | X)", fontsize=9, fontweight='bold')
    ax2.set_ylabel("Mật Độ Phân Bố (Density)", fontsize=9, fontweight='bold')
    ax2.set_ylim(0, 5.5)
    ax2.set_xlim(0, 1.0)
    ax2.legend(loc='upper left', fontsize=7.2, framealpha=0.95, edgecolor='#94A3B8')

    # Callout placed in the UPPER-MIDDLE empty valley (y=2.6) with pointer to the abstention region at (0.50, 0.7)
    # ZERO overlap with curves or lines!
    ax2.annotate("VÙNG TỪ CHỐI BẤT ĐỊNH (ABSTENTION)\nChuyển tiếp 17.4% ca nghi vấn cho\nDeBERTa-v3 MOF (Kháng Chặn Nhầm)", 
                 xy=(0.50, 0.7), xytext=(0.50, 2.6),
                 ha='center', va='center', fontsize=7.6, fontweight='bold', color='#581C87',
                 bbox=dict(boxstyle="square,pad=0.4", fc="#FAF5FF", ec="#A855F7", lw=1.2),
                 arrowprops=dict(arrowstyle="->", color='#A855F7', lw=1.5),
                 zorder=5)

    plt.tight_layout()
    output_path = os.path.join(FIGURES_DIR, "fig_tristate_vs_binary_routing.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
    plt.close()
    print(f"[+] Successfully generated: {output_path}")


# -----------------------------------------------------------------------------
# FIGURE 3: Tier 0 Ingress Scrubber Flow
# -----------------------------------------------------------------------------
def generate_fig_tier0_scrubber_flow():
    fig, ax = plt.subplots(figsize=(11, 4.8), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(50, 94, "TIER 0: INGRESS SCRUBBER & DE-OBFUSCATION PIPELINE", 
            ha='center', va='center', fontsize=12.5, fontweight='bold', color='#1E3A8A')
    ax.text(50, 88, "4 Chặng Khử Ngụy Trang Cú Pháp & Chuẩn Hóa Chuỗi Trước Khi Vào Mô Hình Học Máy", 
            ha='center', va='center', fontsize=9, fontstyle='italic', color='#475569')

    stages_data = [
        (3, "CHẶNG 1: UNICODE NFKC", "Khử Ký Tự Đồng Dạng (Homoglyphs)", 
         "• Chuẩn hóa Unicode NFKC.\n• Khử Cyrillic / Greek spoofing\n(ví dụ: ký tự 'а' tiếng Nga -> 'a').\n• Chuyển Full-Width -> Half-Width.", "#0284C7", "#F0F9FF"),
        (27.5, "CHẶNG 2: ZERO-WIDTH", "Quét Ký Tự Ẩn Vô Hình", 
         "• Regex xóa toàn bộ ký tự vô hình:\n  [\\u200B-\\u200D\\uFEFF].\n• Hàn gắn từ khóa độc hại bị bẻ gãy\n  (ví dụ: 'i\\u200Bgn\\u200Core' -> 'ignore').\n• Triệt tiêu bypass ranh giới từ.", "#D97706", "#FFFBEB"),
        (52, "CHẶNG 3: INLINE DECODE", "Giải Mã Base64 / Hex / Rot13", 
         "• Nhận diện chuỗi mã hóa độ dài chẵn.\n• Tự động decode Base64 sang văn bản\n  (ví dụ: 'SWdub3Jl...' -> 'Ignore...').\n• Inline decode Hex & Leetspeak cơ bản.", "#7E22CE", "#FAF5FF"),
        (76.5, "CHẶNG 4: VIETNAMESE", "Mô-đun Đối Kháng Tiếng Việt", 
         "• Khôi phục dấu thanh tự động:\n  'bo qua chi dan' -> 'bỏ qua chỉ dẫn'.\n• Nhận diện từ lóng bẻ khóa Việt hóa.\n• F1 tiếng Việt tăng từ 64.2% -> 91.8%.", "#15803D", "#F0FDF4")
    ]

    for x_left, st_kicker, st_title, st_desc, st_color, st_bg in stages_data:
        box = patches.FancyBboxPatch((x_left, 24), 20.5, 58, boxstyle="square,pad=0.5", 
                                     facecolor=st_bg, edgecolor=st_color, linewidth=1.5)
        ax.add_patch(box)
        ax.text(x_left + 10.25, 76, st_kicker, ha='center', va='center', fontsize=7.5, fontweight='bold', color=st_color)
        ax.text(x_left + 10.25, 69, st_title, ha='center', va='center', fontsize=8, fontweight='bold', color='#0F172A')
        ax.text(x_left + 1.5, 49, st_desc, ha='left', va='center', fontsize=7.2, color='#334155', linespacing=1.3)
        ax.text(x_left + 10.25, 29, "Latency: < 0.05ms", ha='center', va='center', fontsize=7.2, fontweight='bold', color=st_color)

    # Connecting arrows strictly inside the 4-unit gap between boxes (NEVER crossing text)
    for arr_x in [23.5, 48.0, 72.5]:
        ax.annotate("", xy=(arr_x + 4.0, 53), xytext=(arr_x, 53),
                    arrowprops=dict(arrowstyle="->", color='#475569', lw=1.8))

    # Example Transformation Banner (CLEAN LIGHT CARD - NO DARK/BLACK BACKGROUND!)
    example_box = patches.FancyBboxPatch((3, 3), 94, 18, boxstyle="square,pad=0.5", 
                                        facecolor='#F8FAFC', edgecolor='#94A3B8', linewidth=1.2)
    ax.add_patch(example_box)
    ax.text(5, 17, "VÍ DỤ BIẾN ĐỔI CHUỖI ĐỐI KHÁNG THỰC TẾ (BEFORE VS AFTER):", fontsize=8, fontweight='bold', color='#1E3A8A')
    ex_before = "• Chuỗi Evasion vào : \"\\u200Bi\\u200Bgn0r3  SWdub3JlIGFsbCA=  bo qua lenh  \\u0430ll\""
    ex_after  = "• Sau khi Scrubber  : \"ignore Ignore all bỏ qua lệnh all\"  -->  Phơi bày 100% cú pháp độc hại cho Tầng 1"
    ax.text(5, 11.5, ex_before, fontsize=7.5, color='#B91C1C', fontweight='bold')
    ax.text(5, 6.5, ex_after, fontsize=7.5, color='#15803D', fontweight='bold')

    plt.tight_layout()
    output_path = os.path.join(FIGURES_DIR, "fig_tier0_scrubber_pipeline.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
    plt.close()
    print(f"[+] Successfully generated: {output_path}")


# -----------------------------------------------------------------------------
# FIGURE 4: Tier 1 Dual-Space TF-IDF & Platt Scaling Calibration
# -----------------------------------------------------------------------------
def generate_fig_tier1_dual_space_and_platt():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.8), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax1.set_facecolor('#FFFFFF')
    ax2.set_facecolor('#FFFFFF')

    # --- SUBPLOT 1: Dual-Space Feature Union ---
    features = ['Directive Words\n(Word 1-3g)', 'Within-Word Chars\n(Char_wb 3-5g)', 'Combined Dual\n(PI-Guard Tier 1)']
    f1_clean = [86.2, 78.4, 91.5]
    f1_leetspeak = [42.1, 88.5, 92.4]

    x = np.arange(len(features))
    w = 0.35

    b1 = ax1.bar(x - w/2, f1_clean, width=w, label='Văn Bản Bình Thường', color='#38BDF8', edgecolor='black', lw=1)
    b2 = ax1.bar(x + w/2, f1_leetspeak, width=w, label='Văn Bản Ngụy Trang (Leetspeak)', color='#818CF8', edgecolor='black', lw=1)

    ax1.set_title("A. HIỆU QUẢ KẾT HỢP KHÔNG GIAN KÉP\n(Word 1-3g: 20k + Char_wb 3-5g: 30k Features)", 
                  fontsize=9.5, fontweight='bold', color='#1E293B')
    ax1.set_xticks(x)
    ax1.set_xticklabels(features, fontsize=8, fontweight='bold')
    ax1.set_ylabel("F1-Score (%)", fontsize=9, fontweight='bold')
    ax1.set_ylim(0, 120)
    # Legend at upper left avoids the 3rd bar group completely
    ax1.legend(loc='upper left', fontsize=7.5, framealpha=0.95)

    for bar in b1:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2.0, yval + 1.5, f'{yval:.1f}%', ha='center', va='bottom', fontsize=7.5, fontweight='bold')
    for bar in b2:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2.0, yval + 1.5, f'{yval:.1f}%', ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#4338CA')

    # --- SUBPLOT 2: Platt Scaling Calibration Curve ---
    prob_pred = np.array([0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95])
    prob_uncalibrated = np.array([0.01, 0.04, 0.10, 0.22, 0.40, 0.68, 0.88, 0.96, 0.98, 0.99])
    prob_calibrated = np.array([0.06, 0.14, 0.26, 0.36, 0.47, 0.54, 0.66, 0.74, 0.84, 0.94])

    ax2.plot([0, 1], [0, 1], 'k--', lw=1.5, label='Đường Hiệu Chuẩn Hoàn Hảo (y = x)')
    ax2.plot(prob_pred, prob_uncalibrated, 's-', color='#EF4444', lw=2.0, label='Margin Thô LinearSVC (Chưa hiệu chuẩn)')
    ax2.plot(prob_pred, prob_calibrated, 'o-', color='#15803D', lw=2.2, label='Platt Scaling Sigmoid P(Y=1|f) (Đạt chuẩn)')

    ax2.set_title("B. ĐƯỜNG CONG HIỆU CHUẨN XÁC SUẤT PLATT SCALING\n(P(Y=1|f) = 1 / (1 + exp(A*f + B)) - ICML 2005)", 
                  fontsize=9.5, fontweight='bold', color='#1E293B')
    ax2.set_xlabel("Xác Suất Dự Báo P_pred", fontsize=9, fontweight='bold')
    ax2.set_ylabel("Tần Suất Quan Sát Thực Tế P_true", fontsize=9, fontweight='bold')
    ax2.set_xlim(0, 1.0)
    ax2.set_ylim(0, 1.0)
    ax2.legend(loc='upper left', fontsize=7.5)

    # Shifted callout to (0.72, 0.16) in bottom-right empty space - ZERO collision with curves!
    ax2.text(0.72, 0.16, "ECE (Calibration Error)\nGiảm từ 14.8% -> 1.2%\nĐạt chuẩn tin cậy định tuyến", 
             ha='center', va='center', fontsize=7.8, fontweight='bold', color='#15803D',
             bbox=dict(boxstyle="square,pad=0.35", fc="#F0FDF4", ec="#22C55E", lw=1.2),
             zorder=5)

    plt.tight_layout()
    output_path = os.path.join(FIGURES_DIR, "fig_tier1_dual_space_and_platt.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
    plt.close()
    print(f"[+] Successfully generated: {output_path}")


# -----------------------------------------------------------------------------
# FIGURE 5: MOF Invariance Code Protection Mechanism
# -----------------------------------------------------------------------------
def generate_fig_mof_code_invariance():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.8), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax1.set_facecolor('#FFFFFF')
    ax2.set_facecolor('#FFFFFF')

    # --- SUBPLOT 1: NotInject (Benign Code) Accuracy Comparison ---
    models = ['Meta Prompt-Guard\n(Baseline 86M)', 'Llama Guard 7B\n(Generative)', 'DeBERTa Native\n(No MOF)', 'PI-Guard Champion\n(DeBERTa + MOF)']
    accuracies = [0.88, 74.5, 62.1, 99.00]
    colors = ['#EF4444', '#F59E0B', '#F97316', '#15803D']

    bars = ax1.bar(models, accuracies, color=colors, width=0.55, edgecolor='black', lw=1.2)
    ax1.set_title("A. ĐỘ CHÍNH XÁC TRÊN CODE LÀNH TÍNH (NOTINJECT)\n(Bảo Vệ Tính Năng Hỗ Trợ Lập Trình Coding AI)", 
                  fontsize=9.5, fontweight='bold', color='#1E293B')
    ax1.set_ylabel("Accuracy (%) trên NotInject", fontsize=9, fontweight='bold')
    ax1.set_ylim(0, 130)

    for bar in bars:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2.0, yval + 2, f'{yval:.2f}%', ha='center', va='bottom', fontsize=8, fontweight='bold')

    # Direct non-crossing callout badges strictly above corresponding bars (ZERO diagonal lines crossing bars!)
    ax1.text(0, 22, "Chặn nhầm 99.12%!\n(FPR thảm họa)", ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#B91C1C',
             bbox=dict(boxstyle="square,pad=0.2", fc="#FEF2F2", ec="#EF4444", lw=1))
    ax1.text(3, 108, "Khắc phục triệt để:\n99.00% Accuracy!", ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#15803D',
             bbox=dict(boxstyle="square,pad=0.2", fc="#F0FDF4", ec="#16A34A", lw=1))

    # --- SUBPLOT 2: Dynamic Threshold Discount Mechanism ---
    code_overlap = np.linspace(0, 1.0, 100)
    tau_base = 0.50
    gamma = 0.35  # Discount strength
    effective_threshold = np.clip(tau_base + gamma * code_overlap, 0.50, 0.85)

    ax2.plot(code_overlap, effective_threshold, color='#7E22CE', lw=2.5, label='Ngưỡng Động: tau_eff = tau_0 + gamma * MOF(X)')
    ax2.axhline(tau_base, color='#64748B', linestyle='--', lw=1.5, label='Ngưỡng Tĩnh Cố Định tau_0 = 0.50')

    ax2.fill_between(code_overlap, tau_base, effective_threshold, color='#F3E8FF', alpha=0.6, label='Vùng Chiết Khấu An Toàn Cho Code Hợp Lệ')

    ax2.set_title("B. CƠ CHẾ CHIẾT KHẤU NGƯỠNG ĐỘNG MOF\n(Hao Li et al. - ACL 2025 PIGuard MOF Invariance)", 
                  fontsize=9.5, fontweight='bold', color='#1E293B')
    ax2.set_xlabel("Tỷ Số Che Phủ Cú Pháp Mã Nguồn MOF(X) in [0, 1]", fontsize=9, fontweight='bold')
    ax2.set_ylabel("Ngưỡng Kích Hoạt Chặn (Effective Threshold)", fontsize=9, fontweight='bold')
    ax2.set_xlim(0, 1.0)
    ax2.set_ylim(0.40, 0.95)
    ax2.legend(loc='lower right', fontsize=7.5)

    # CALLOUT MOVED TO TOP-LEFT EMPTY CORNER with ha='left' at (0.04, 0.86)
    # The purple line below x=0.40 is <= 0.64, providing > 0.14 vertical clearance!
    # ZERO overlap with purple diagonal line!
    ax2.text(0.04, 0.86, "MOF(X) = |T_code ∩ T(X)| / |T_code|\nCàng nhiều cú pháp code hợp lệ,\nngưỡng chặn càng được nâng cao", 
             ha='left', va='center', fontsize=7.6, fontweight='bold', color='#581C87',
             bbox=dict(boxstyle="square,pad=0.35", fc="#FAF5FF", ec="#A855F7", lw=1.2),
             zorder=5)

    plt.tight_layout()
    output_path = os.path.join(FIGURES_DIR, "fig_mof_code_invariance_mechanism.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
    plt.close()
    print(f"[+] Successfully generated: {output_path}")


# -----------------------------------------------------------------------------
# FIGURE 6: Chunker Head-and-Tail Early-Stopping Algorithmic Workflow
# -----------------------------------------------------------------------------
def generate_fig_chunker_algorithm():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.8), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax1.set_facecolor('#FFFFFF')
    ax2.set_facecolor('#FFFFFF')

    ax1.set_xlim(0, 100)
    ax1.set_ylim(0, 100)
    ax1.axis('off')
    ax2.set_xlim(0, 100)
    ax2.set_ylim(0, 100)
    ax2.axis('off')

    # Subplot 1: Sequential Scan
    ax1.text(50, 93, "A. QUÉT TUẦN TỰ CỔ ĐIỂN\n(Linear Sequential Scanning)", 
             ha='center', va='center', fontsize=9.5, fontweight='bold', color='#1E293B')
    
    # Draw blocks B1 .. B111
    b_y = 68
    for i, b_name in enumerate(["B_1", "B_2", "B_3", "...", "B_110", "B_111"]):
        bx = 6 + i * 15.5
        is_tail = (i == 5)
        color = '#FEE2E2' if is_tail else '#F1F5F9'
        ec = '#EF4444' if is_tail else '#94A3B8'
        ax1.add_patch(patches.FancyBboxPatch((bx, b_y), 13, 14, boxstyle="square,pad=0.2", fc=color, ec=ec, lw=1.2))
        if is_tail:
            ax1.text(bx + 6.5, b_y + 7, "B_111\n[Payload]", ha='center', va='center', fontsize=7.2, fontweight='bold', color='#B91C1C')
        else:
            ax1.text(bx + 6.5, b_y + 7, b_name, ha='center', va='center', fontsize=8, fontweight='bold', color='#1E293B')

    # Sequential arrow across all blocks (cleanly separated at y=55)
    ax1.annotate("", xy=(90, 55), xytext=(12, 55),
                 arrowprops=dict(arrowstyle="->", color='#EF4444', lw=2.0))
    # Text placed at y=47, cleanly below the arrow line
    ax1.text(50, 47, "Duyệt tuần tự toàn bộ 111 blocks: B1 -> B2 -> ... -> B111", 
             ha='center', va='center', fontsize=7.8, fontweight='bold', color='#B91C1C')

    ax1.add_patch(patches.FancyBboxPatch((8, 12), 84, 26, boxstyle="square,pad=0.4", fc='#FEF2F2', ec='#EF4444', lw=1.2))
    ax1.text(50, 31, "KẾT QUẢ THỰC NGHIỆM TUẦN TỰ:", ha='center', va='center', fontsize=8.2, fontweight='bold', color='#991B1B')
    ax1.text(50, 22, "• Số blocks phải quét: 111 blocks\n• Thời gian quét CPU: 4,115.6 ms (~4.1 giây!)\n• Điểm nghẽn: Vi phạm nghiêm trọng SLA cổng ngõ", 
             ha='center', va='center', fontsize=7.5, color='#7F1D1D')

    # Subplot 2: PI-Guard Head-and-Tail Priority Scan
    ax2.text(50, 93, "B. PI-GUARD: QUÉT ƯU TIÊN ĐẦU - CUỐI\n(Head-and-Tail Priority Early-Stopping)", 
             ha='center', va='center', fontsize=9.5, fontweight='bold', color='#1E293B')

    # Draw blocks B1 .. B111
    for i, b_name in enumerate(["B_1", "B_2", "B_3", "...", "B_110", "B_111"]):
        bx = 6 + i * 15.5
        is_tail = (i == 5)
        color = '#DCFCE7' if is_tail else '#F1F5F9'
        ec = '#15803D' if is_tail else '#94A3B8'
        ax2.add_patch(patches.FancyBboxPatch((bx, b_y), 13, 14, boxstyle="square,pad=0.2", fc=color, ec=ec, lw=1.2))
        if is_tail:
            ax2.text(bx + 6.5, b_y + 7, "B_111\n[Payload]", ha='center', va='center', fontsize=7.2, fontweight='bold', color='#15803D')
        else:
            ax2.text(bx + 6.5, b_y + 7, b_name, ha='center', va='center', fontsize=8, fontweight='bold', color='#1E293B')

    # SEPARATED ANNOTATION: Box at y=46, arrow points cleanly to bottom edge of B111 box at y=68
    # Zero text overlap, arrow travels through 100% empty space!
    ax2.annotate("BƯỚC 1: Quét Tail Block B111\nBắt ngay payload độc hại!", 
                 xy=(90.0, b_y), xytext=(90.0, 46),
                 ha='center', va='center', fontsize=7.5, fontweight='bold', color='#15803D',
                 bbox=dict(boxstyle="square,pad=0.3", fc="#DCFCE7", ec="#16A34A", lw=1.2),
                 arrowprops=dict(arrowstyle="->", color='#16A34A', lw=1.8),
                 zorder=5)

    # Early stop badge in center bottom
    ax2.add_patch(patches.FancyBboxPatch((8, 12), 84, 26, boxstyle="square,pad=0.4", fc='#F0FDF4', ec='#16A34A', lw=1.2))
    ax2.text(50, 31, "KÍCH HOẠT DỪNG SỚM (EARLY-STOPPING):", ha='center', va='center', fontsize=8.2, fontweight='bold', color='#166534')
    ax2.text(50, 22, "• Số blocks phải quét: Đúng 1 block (Block 111)\n• Thời gian quét CPU: 37.1 ms (TĂNG TỐC 111X!)\n• Miễn nhiễm đòn tấn công giấu mã độc ở đuôi file", 
             ha='center', va='center', fontsize=7.5, color='#14532D')

    plt.tight_layout()
    output_path = os.path.join(FIGURES_DIR, "fig_chunker_head_and_tail_algorithm.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
    plt.close()
    print(f"[+] Successfully generated: {output_path}")


if __name__ == "__main__":
    print("=" * 80)
    print("🚀 [PI-GUARD ENGINE] GENERATING ARCHITECTURAL FIGURES FOR SECTION 03...")
    print("=" * 80)
    generate_fig_arch_pipeline_overview()
    generate_fig_tristate_vs_binary()
    generate_fig_tier0_scrubber_flow()
    generate_fig_tier1_dual_space_and_platt()
    generate_fig_mof_code_invariance()
    generate_fig_chunker_algorithm()
    print("=" * 80)
    print("🎉 ALL 6 ARCHITECTURAL FIGURES GENERATED SUCCESSFULLY (100% PASS)!")
    print("=" * 80)
