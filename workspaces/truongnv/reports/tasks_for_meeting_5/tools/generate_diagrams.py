# -*- coding: utf-8 -*-
"""
PI-Guard Meeting Presentation Diagram Generator (Light Theme & Sharp Rectangles)
Generates high-resolution, pixel-perfect diagrams for:
1. diagram_two_tier_architecture.png & diagram_two_tier_architecture_en.png
2. diagram_flat_token_space.png & diagram_flat_token_space_en.png
3. diagram_5d_threat_framework.png & diagram_5d_threat_framework_en.png
4. diagram_tri_state_distribution.png & diagram_tri_state_distribution_en.png

Theme: Modern Academic Light Theme (Pure White Canvas, Crisp Sharp Rectangles, Deep Contrast)
Author: Nguyen Van Truong (Leader) - PI-Guard Team
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

FIGURES_DIR = r"D:\Work\Do-an\workspaces\truongnv\reports\tasks_for_meeting_5\figures"
os.makedirs(FIGURES_DIR, exist_ok=True)

def get_font(size, bold=False):
    font_names = ["segoeuib.ttf" if bold else "segoeui.ttf", "arialbd.ttf" if bold else "arial.ttf"]
    for fn in font_names:
        try:
            return ImageFont.truetype(fn, size)
        except Exception:
            continue
    return ImageFont.load_default()

def draw_sharp_rect(draw, bbox, fill, outline=None, width=1):
    """Draws a crisp rectangle with sharp (non-rounded) corners."""
    x0, y0, x1, y1 = bbox
    draw.rectangle([int(x0), int(y0), int(x1), int(y1)], fill=fill, outline=outline, width=int(width))

# ==============================================================================
# DIAGRAM 1: TWO-TIER CASCADED ARCHITECTURE WITH TRI-STATE ROUTING
# ==============================================================================
def generate_two_tier_diagram(lang="vi"):
    w, h = 1400, 850
    img = Image.new("RGB", (w, h), "#FFFFFF")
    draw = ImageDraw.Draw(img)

    f_title = get_font(27, bold=True)
    f_sub = get_font(15, bold=False)
    f_h2 = get_font(18, bold=True)
    f_h3 = get_font(15, bold=True)
    f_body = get_font(13, bold=False)
    f_mono = get_font(13, bold=True)
    f_badge = get_font(12, bold=True)

    is_vi = (lang == "vi")

    # Title Banner
    title = "KIẾN TRÚC RÀO CHẮN PHÂN TẦNG HAI CẤP ĐỘ (TWO-TIER CASCADED GUARDRAIL)" if is_vi else "TWO-TIER CASCADED GUARDRAIL ARCHITECTURE (TRI-STATE ROUTING)"
    sub = "Cơ chế Tri-State Routing: Lọc nhanh 82.6% lưu lượng tại Tầng 1 (<0.5ms), chuyển giao 17.4% bất định cho Tầng 2" if is_vi else "Tri-State Routing: 82.6% traffic fast-filtered at Tier 1 (<0.5ms), 17.4% ambiguous requests routed to Tier 2"
    draw.text((40, 25), title, fill="#0284C7", font=f_title)
    draw.text((40, 65), sub, fill="#64748B", font=f_sub)

    # 1. User Input Box (Left)
    draw_sharp_rect(draw, (40, 110, 260, 480), fill="#F8FAFC", outline="#0284C7", width=2)
    draw_sharp_rect(draw, (55, 125, 245, 160), fill="#EFF6FF", outline="#0284C7", width=1)
    draw.text((70, 133), "INGRESS PROMPT" if not is_vi else "CỬA NGÕ INGRESS", fill="#0284C7", font=f_badge)
    
    t_in = "Đầu vào văn bản:" if is_vi else "Text Ingress:"
    draw.text((55, 175), t_in, fill="#0F172A", font=f_h3)
    draw.text((55, 205), "• Direct Chat UI" if is_vi else "• Direct Chat UI", fill="#334155", font=f_body)
    draw.text((55, 230), "• REST API /v1/chat" if is_vi else "• REST API /v1/chat", fill="#334155", font=f_body)
    draw.text((55, 255), "• Trích xuất tệp RAG" if is_vi else "• RAG File Chunks", fill="#334155", font=f_body)
    draw.text((55, 280), "  (PDF, DOCX, Web)" if is_vi else "  (PDF, DOCX, Web)", fill="#64748B", font=f_body)

    draw_sharp_rect(draw, (55, 330, 245, 455), fill="#F5F3FF", outline="#7C3AED", width=1)
    draw.text((65, 340), "TIER 0: SCREENING" if not is_vi else "TẦNG 0: TIỀN XỬ LÝ", fill="#6D28D9", font=f_badge)
    t_t0_1 = "• Chuẩn hóa Unicode" if is_vi else "• Unicode Normalize"
    t_t0_2 = "• Khử dấu khoảng trắng" if is_vi else "• Strip Whitespace"
    t_t0_3 = "• Giải mã Base64" if is_vi else "• Decode Base64"
    t_t0_4 = "• Độ trễ: < 0.05 ms" if is_vi else "• Latency: < 0.05 ms"
    draw.text((65, 365), t_t0_1, fill="#334155", font=f_body)
    draw.text((65, 388), t_t0_2, fill="#334155", font=f_body)
    draw.text((65, 411), t_t0_3, fill="#334155", font=f_body)
    draw.text((65, 434), t_t0_4, fill="#047857", font=f_mono)

    # Arrow 1 -> Tier 1
    draw.line([(260, 295), (320, 295)], fill="#0284C7", width=3)
    draw.polygon([(315, 288), (335, 295), (315, 302)], fill="#0284C7")

    # 2. Tier 1 Box (Middle-Left)
    draw_sharp_rect(draw, (340, 110, 680, 480), fill="#F8FAFC", outline="#0284C7", width=2)
    draw_sharp_rect(draw, (360, 125, 660, 160), fill="#EFF6FF", outline="#0284C7", width=1)
    t_t1_hdr = "TẦNG 1: PHÂN LOẠI NHANH (LIGHTWEIGHT FILTER)" if is_vi else "TIER 1: ULTRA-FAST FILTER (LIGHTWEIGHT ML)"
    draw.text((375, 133), t_t1_hdr, fill="#0284C7", font=f_badge)

    draw.text((360, 175), "TF-IDF N-Grams + LinearSVC" if not is_vi else "TF-IDF Ký Tự N-Grams + LinearSVC", fill="#0F172A", font=f_h3)
    t_t1_b1 = "• Trích xuất sub-word n-grams (3-5 ký tự)" if is_vi else "• Sub-word char n-grams (3-5 chars)"
    t_t1_b2 = "• Bắt trọn Leetspeak ('1gn0r3', biến dạng)" if is_vi else "• Captures Leetspeak ('1gn0r3', evasion)"
    t_t1_b3 = "• Không gian 50.000 chiều siêu thưa" if is_vi else "• 50,000 sparse n-gram feature space"
    t_t1_b4 = "• Dung lượng RAM: < 50 MB" if is_vi else "• Memory footprint: < 50 MB RAM"
    draw.text((360, 205), t_t1_b1, fill="#334155", font=f_body)
    draw.text((360, 232), t_t1_b2, fill="#334155", font=f_body)
    draw.text((360, 259), t_t1_b3, fill="#334155", font=f_body)
    draw.text((360, 286), t_t1_b4, fill="#047857", font=f_mono)

    # Tier 1 Metrics Box
    draw_sharp_rect(draw, (360, 325, 660, 455), fill="#FFFFFF", outline="#0284C7", width=1)
    draw.text((375, 335), "HIỆU NĂNG TẦNG 1:" if is_vi else "TIER 1 PERFORMANCE:", fill="#0284C7", font=f_badge)
    t_m1 = "• Độ trễ CPU: ~0.47 ms (< 0.5 ms)" if is_vi else "• CPU Latency: ~0.47 ms (< 0.5 ms)"
    t_m2 = "• Thông lượng: > 2.000 req/giây" if is_vi else "• Throughput: > 2,000 req/sec"
    t_m3 = "• Tự quyết định: 82.6% lưu lượng!" if is_vi else "• Self-decides: 82.6% of all traffic!"
    draw.text((375, 365), t_m1, fill="#047857", font=f_h3)
    draw.text((375, 395), t_m2, fill="#0F172A", font=f_body)
    draw.text((375, 420), t_m3, fill="#0284C7", font=f_h3)

    # 3 Tri-State Decision Branches out of Tier 1
    # Branch 1: Fast-Pass Benign (Down-Left)
    draw.line([(440, 480), (440, 540)], fill="#059669", width=3)
    draw.polygon([(433, 535), (440, 555), (447, 535)], fill="#059669")
    draw_sharp_rect(draw, (360, 560, 520, 640), fill="#ECFDF5", outline="#059669", width=2)
    draw.text((375, 570), "FAST PASS (71.3%)", fill="#047857", font=f_badge)
    draw.text((375, 595), "P(Attack) <= 0.15", fill="#047857", font=f_mono)
    draw.text((375, 617), "-> Downstream LLM" if is_vi else "-> Downstream LLM", fill="#0F172A", font=f_body)

    # Branch 2: Early Block Malicious (Down-Middle)
    draw.line([(580, 480), (580, 540)], fill="#DC2626", width=3)
    draw.polygon([(573, 535), (580, 555), (587, 535)], fill="#DC2626")
    draw_sharp_rect(draw, (530, 560, 690, 640), fill="#FEF2F2", outline="#DC2626", width=2)
    draw.text((545, 570), "EARLY BLOCK (11.3%)", fill="#B91C1C", font=f_badge)
    draw.text((545, 595), "P(Attack) >= 0.85", fill="#B91C1C", font=f_mono)
    draw.text((545, 617), "-> HTTP 403 Forbidden" if is_vi else "-> HTTP 403 Forbidden", fill="#0F172A", font=f_body)

    # Branch 3: Escalate to Tier 2 (Right)
    draw.line([(680, 295), (760, 295)], fill="#D97706", width=3)
    draw.polygon([(755, 288), (775, 295), (755, 302)], fill="#D97706")
    draw_sharp_rect(draw, (695, 240, 755, 285), fill="#FFFBEB", outline="#D97706", width=1)
    draw.text((702, 250), "17.4%", fill="#B45309", font=f_badge)
    draw.text((700, 268), "Bất định" if is_vi else "Uncertain", fill="#B45309", font=get_font(11, bold=True))

    # 4. Tier 2 Box (Middle-Right)
    draw_sharp_rect(draw, (780, 110, 1150, 480), fill="#F8FAFC", outline="#7C3AED", width=2)
    draw_sharp_rect(draw, (800, 125, 1130, 160), fill="#F5F3FF", outline="#7C3AED", width=1)
    t_t2_hdr = "TẦNG 2: THẨM ĐỊNH NGỮ NGHĨA SÂU (DEEP SEMANTIC ARBITER)" if is_vi else "TIER 2: DEEP SEMANTIC ARBITER (TRANSFORMER)"
    draw.text((815, 133), t_t2_hdr, fill="#6D28D9", font=f_badge)

    draw.text((800, 175), "Mô hình mỏ neo ACL 2025:" if is_vi else "ACL 2025 Anchor Model:", fill="#0F172A", font=f_h3)
    draw.text((800, 205), "• DeBERTa-v3 Disentangled Attention", fill="#334155", font=f_body)
    draw.text((800, 232), "• Tách rời Ma trận Nội dung & Vị trí (c & r)" if is_vi else "• Disentangled Content & Position Matrices", fill="#334155", font=f_body)
    draw.text((800, 259), "• Thuật toán MOF (Mitigating Overdefense for Free)" if is_vi else "• MOF Algorithm (Mitigating Overdefense for Free)", fill="#334155", font=f_body)
    draw.text((800, 286), "• Tối ưu hóa: INT8 ONNX Runtime Engine" if is_vi else "• Optimized via INT8 ONNX Runtime Engine", fill="#0284C7", font=f_mono)

    # Tier 2 Metrics
    draw_sharp_rect(draw, (800, 325, 1130, 455), fill="#FFFFFF", outline="#7C3AED", width=1)
    draw.text((815, 335), "HIỆU NĂNG TẦNG 2 KHI TỐI ƯU HÓA:" if is_vi else "OPTIMIZED TIER 2 PERFORMANCE:", fill="#6D28D9", font=f_badge)
    draw.text((815, 365), "• Độ trễ INT8 CPU: ~18.5 ms (giảm từ 112.4 ms)" if is_vi else "• INT8 CPU Latency: ~18.5 ms (down from 112.4 ms)", fill="#0F172A", font=f_body)
    draw.text((815, 392), "• F1-Score: 0.9416 (Bảo toàn độ chuẩn xác)" if is_vi else "• F1-Score: 0.9416 (Preserves ACL 2025 accuracy)", fill="#0F172A", font=f_body)
    draw.text((815, 419), "• Chỉ kích hoạt thẩm định: 17.4% mẫu khó" if is_vi else "• Only triggered for 17.4% difficult inputs", fill="#0284C7", font=f_h3)

    # Tier 2 Decisions
    draw.line([(1000, 480), (1000, 540)], fill="#7C3AED", width=3)
    draw.polygon([(993, 535), (1000, 555), (1007, 535)], fill="#7C3AED")

    draw_sharp_rect(draw, (880, 560, 1120, 640), fill="#F5F3FF", outline="#7C3AED", width=2)
    draw.text((895, 570), "TIER 2 VERDICT (17.4% MẪU)" if is_vi else "TIER 2 VERDICT (17.4% TRAFFIC)", fill="#6D28D9", font=f_badge)
    draw.text((895, 595), "• Phán quyết an toàn -> Downstream LLM" if is_vi else "• Benign Verdict -> Downstream LLM", fill="#047857", font=f_body)
    draw.text((895, 617), "• Phán quyết độc hại -> Chặn & Ghi log" if is_vi else "• Malicious Verdict -> Block & Audit Log", fill="#B91C1C", font=f_body)

    # 5. Summary KPI Card (Bottom Full Width)
    draw_sharp_rect(draw, (40, 680, 1360, 810), fill="#F1F5F9", outline="#0284C7", width=2)
    draw.text((60, 695), "HIỆU NĂNG KỲ VỌNG TOÀN TRÌNH CỦA PI-GUARD" if is_vi else "END-TO-END EXPECTED SYSTEM PERFORMANCE METRICS", fill="#0284C7", font=f_h2)
    
    if is_vi:
        kpis = [
            ("ĐỘ TRỄ TRUNG BÌNH", "E[L] = 3.69 ms", "0.47 + 0.174 x 18.5 ms", "#047857"),
            ("ĐỘ TRỄ PHÂN VỊ P95", "P95 = 19.8 ms", "Đạt chuẩn P95 < 22ms", "#047857"),
            ("ĐỘ CHÍNH XÁC F1", "F1 = 0.9416", "Bảo toàn mỏ neo ACL 2025", "#0284C7"),
            ("BÁO ĐỘNG GIẢ (FPR)", "FPR < 1.5 %", "Chống Overdefense", "#D97706"),
            ("CHI PHÍ PHẦN CỨNG", "ZERO-GPU", "100% CPU Thông Thường", "#7C3AED")
        ]
    else:
        kpis = [
            ("AVG LATENCY", "E[L] = 3.69 ms", "0.47 + 0.174 x 18.5 ms", "#047857"),
            ("P95 LATENCY", "P95 = 19.8 ms", "Meets P95 < 22ms Target", "#047857"),
            ("F1-SCORE", "F1 = 0.9416", "ACL 2025 Anchor Verified", "#0284C7"),
            ("FALSE POSITIVE (FPR)", "FPR < 1.5 %", "Zero Over-defense", "#D97706"),
            ("HARDWARE COST", "ZERO-GPU", "100% Commodity CPU", "#7C3AED")
        ]
    for idx, (lbl, val, note, col) in enumerate(kpis):
        bx = 60 + idx * 260
        draw.text((bx, 730), lbl, fill="#64748B", font=get_font(12, bold=True))
        draw.text((bx, 750), val, fill=col, font=get_font(18, bold=True))
        draw.text((bx, 778), note, fill="#334155", font=get_font(12, bold=False))

    suffix = "_en.png" if not is_vi else ".png"
    out_p = os.path.join(FIGURES_DIR, f"diagram_two_tier_architecture{suffix}")
    img.save(out_p, quality=95)
    print(f"Generated: {out_p}")


# ==============================================================================
# DIAGRAM 2: FLAT TOKEN SPACE VS VON NEUMANN (CRISP & OVERFLOW-FREE)
# ==============================================================================
def generate_flat_token_diagram(lang="vi"):
    w, h = 1320, 800
    img = Image.new("RGB", (w, h), "#FFFFFF")
    draw = ImageDraw.Draw(img)

    f_title = get_font(26, bold=True)
    f_sub = get_font(15, bold=False)
    f_h2 = get_font(18, bold=True)
    f_h3 = get_font(15, bold=True)
    f_body = get_font(13, bold=False)
    f_mono = get_font(13, bold=True)
    f_badge = get_font(12, bold=True)

    is_vi = (lang == "vi")

    # Title
    t_title = "CĂN NGUYÊN KỸ THUẬT: LỖ HỔNG KHÔNG GIAN TOKEN PHẲNG" if is_vi else "TECHNICAL ROOT CAUSE: FLAT TOKEN SPACE VULNERABILITY"
    t_sub = "So sánh ranh giới phần cứng truyền thống (Von Neumann / SQL) vs. Cơ chế Self-Attention tự hồi quy (X = S || U)" if is_vi else "Comparing Hardware Separation (Von Neumann / SQL) vs. Autoregressive Self-Attention (X = S || U)"
    draw.text((40, 25), t_title, fill="#0284C7", font=f_title)
    draw.text((40, 65), t_sub, fill="#64748B", font=f_sub)

    # Left Column: Traditional Systems (Hardware & DB Separation)
    draw_sharp_rect(draw, (40, 110, 630, 760), fill="#F8FAFC", outline="#059669", width=2)
    draw_sharp_rect(draw, (60, 125, 610, 160), fill="#ECFDF5", outline="#059669", width=1)
    draw.text((80, 133), "HỆ THỐNG TRUYỀN THỐNG: PHÂN TÁCH ĐẶC QUYỀN RẠCH RÒI" if is_vi else "TRADITIONAL SYSTEMS: RIGID PRIVILEGE ISOLATION", fill="#047857", font=f_badge)

    # 1. Von Neumann
    draw_sharp_rect(draw, (60, 180, 610, 350), fill="#FFFFFF", outline="#CBD5E1", width=1)
    draw.text((80, 195), "1. Kiến Trúc Von Neumann (CPU Hardware)" if is_vi else "1. Von Neumann CPU Hardware Architecture", fill="#0F172A", font=f_h3)
    draw.text((80, 225), "• Phân vùng Lệnh (.text) vs. Phân vùng Dữ liệu (.data)" if is_vi else "• Segmented Instruction (.text) vs. Data (.data)", fill="#334155", font=f_body)
    draw.text((80, 250), "• Bảo vệ phần cứng: Cờ NX-bit (No-eXecute) & W^X" if is_vi else "• Hardware Protection: NX-bit (No-eXecute) & W^X policy", fill="#047857", font=f_mono)
    draw.text((80, 275), "• Phân cấp đặc quyền: Ring 0 (Kernel) vs. Ring 3 (User)" if is_vi else "• Privilege Hierarchy: Ring 0 (Kernel) vs. Ring 3 (User)", fill="#334155", font=f_body)
    draw.text((80, 305), "-> CPU từ chối thực thi mã lệnh trong vùng đệm dữ liệu!" if is_vi else "-> CPU refuses to execute code residing in data memory!", fill="#047857", font=get_font(13, bold=True))

    # 2. Relational DB Prepared Statements
    draw_sharp_rect(draw, (60, 370, 610, 540), fill="#FFFFFF", outline="#CBD5E1", width=1)
    draw.text((80, 385), "2. Cơ Sở Dữ Liệu Quan Hệ (Prepared Statements)" if is_vi else "2. Relational Databases (Prepared Statements)", fill="#0F172A", font=f_h3)
    draw.text((80, 415), "• Biên dịch trước câu truy vấn thành cây cú pháp cố định (AST)" if is_vi else "• Pre-compiles query structure into fixed AST syntax tree", fill="#334155", font=f_body)
    draw.text((80, 440), "• Dữ liệu người dùng truyền qua biến giữ chỗ (Placeholder ?)" if is_vi else "• User data passed exclusively via Placeholders (?)", fill="#047857", font=f_mono)
    draw.text((80, 465), "• Tham số dữ liệu không bao giờ thay đổi logic SQL" if is_vi else "• Data parameters can never mutate query logic or syntax", fill="#334155", font=f_body)
    draw.text((80, 495), "-> Triệt tiêu 100% nguy cơ SQL Injection ở tầng kiến trúc!" if is_vi else "-> 100% architectural elimination of SQL Injection!", fill="#047857", font=get_font(13, bold=True))

    # Traditional Conclusion
    draw_sharp_rect(draw, (60, 560, 610, 735), fill="#ECFDF5", outline="#059669", width=1)
    draw.text((80, 575), "KẾT LUẬN AN TOÀN TRUYỀN THỐNG:" if is_vi else "TRADITIONAL SECURITY TAKEAWAY:", fill="#047857", font=f_badge)
    draw.text((80, 605), "• Ranh giới phân quyền nằm ở CẤP ĐỘ PHẦN CỨNG & HĐH." if is_vi else "• Security boundaries enforced at HARDWARE & OS LEVEL.", fill="#0F172A", font=f_body)
    draw.text((80, 635), "• Dữ liệu (Data) không thể biến thành Lệnh (Instruction)." if is_vi else "• Data cannot morph into executable Instructions.", fill="#0F172A", font=f_body)
    draw.text((80, 665), "• Miễn nhiễm với các đòn đánh đồng ngữ cảnh." if is_vi else "• Naturally immune to contextual conflation attacks.", fill="#0F172A", font=f_body)
    draw.text((80, 695), "• Triển khai kiểm tra an ninh tất định tại ranh giới." if is_vi else "• Deterministic security verification at trust boundaries.", fill="#047857", font=f_body)

    # Right Column: LLM Architecture (Flat Token Space Vulnerability)
    draw_sharp_rect(draw, (660, 110, 1280, 760), fill="#F8FAFC", outline="#DC2626", width=2)
    draw_sharp_rect(draw, (680, 125, 1260, 160), fill="#FEF2F2", outline="#DC2626", width=1)
    draw.text((700, 133), "MÔ HÌNH NGÔN NGỮ LỚN (LLM): KHÔNG GIAN NỐI PHẲNG X = S || U" if is_vi else "LARGE LANGUAGE MODELS: FLAT TOKEN SPACE (X = S || U)", fill="#B91C1C", font=f_badge)

    # 1. Flat Token Space with Graphical Token Boxes
    draw_sharp_rect(draw, (680, 175, 1260, 350), fill="#FFFFFF", outline="#CBD5E1", width=1)
    draw.text((700, 188), "1. Hiện Tượng Ghép Nối Phẳng (Token Concatenation)" if is_vi else "1. Flat Token Concatenation Phenomenon", fill="#0F172A", font=f_h3)
    t_desc1 = "Chuỗi chỉ thị (S) và chuỗi người dùng (U) bị ghép phẳng thành một mảng token:" if is_vi else "System instruction (S) and user input (U) are concatenated into a single array:"
    draw.text((700, 214), t_desc1, fill="#334155", font=f_body)

    # Graphical Token Containers
    # Box S (Blue)
    draw_sharp_rect(draw, (700, 242, 890, 282), fill="#EFF6FF", outline="#0284C7", width=2)
    draw.text((715, 252), "S: System Prompt", fill="#0369A1", font=f_mono)
    
    # Clean graphical vertical bars for concatenation (resolving missing glyphs!)
    draw.line([(912, 246), (912, 278)], fill="#D97706", width=3)
    draw.line([(920, 246), (920, 278)], fill="#D97706", width=3)
    
    # Box U (Red)
    draw_sharp_rect(draw, (945, 242, 1180, 282), fill="#FEF2F2", outline="#DC2626", width=2)
    draw.text((960, 252), "U: User / Attacker Input", fill="#B91C1C", font=f_mono)

    # Arrow and Unified Result
    t_arrow = "-> Mảng Token Duy Nhất: X = S || U (Không có cờ NX-bit hay Ring phân quyền!)" if is_vi else "-> Unified Token Sequence: X = S || U (No NX-bit or Ring separation!)"
    draw.text((700, 292), t_arrow, fill="#B91C1C", font=get_font(13, bold=True))
    t_eq = "• Mô hình xem mọi token trong chuỗi X đều có đặc quyền thực thi bình đẳng." if is_vi else "• The model treats all tokens in sequence X with equal execution privilege."
    draw.text((700, 318), t_eq, fill="#64748B", font=f_body)

    # 2. Self-Attention Hijacking & Recency Bias with Clean Formula Box
    draw_sharp_rect(draw, (680, 365, 1260, 545), fill="#FFFFFF", outline="#CBD5E1", width=1)
    draw.text((700, 378), "2. Chiếm Đoạt Ma Trận Self-Attention & Recency Bias" if is_vi else "2. Self-Attention Hijacking & Recency Bias", fill="#0F172A", font=f_h3)

    # Dedicated Formula Callout Box
    draw_sharp_rect(draw, (700, 404, 1240, 452), fill="#F0F9FF", outline="#0284C7", width=1)
    draw.text((720, 416), "Attention( Q, K, V )  =  softmax (  ( Q · Kᵀ )  /  sqrt(d_k)  )  ·  V", fill="#0369A1", font=get_font(15, bold=True))

    t_qk = "• Q · Kᵀ: Tích vô hướng đo tương đồng — mọi token tính toán ngang hàng." if is_vi else "• Q · Kᵀ: Dot-product similarity — all tokens interact equally without hierarchy."
    t_rb = "• Recency Bias: Transformer tự hồi quy ưu tiên xử lý token ở cuối chuỗi." if is_vi else "• Recency Bias: Autoregressive Transformers prioritize tokens near the end."
    t_hq = "-> Hệ quả: Lệnh mới U chiếm trọn Softmax, triệt tiêu chỉ thị an toàn của S!" if is_vi else "-> Result: Injected prompt U dominates Softmax, overriding System Prompt S!"
    draw.text((700, 462), t_qk, fill="#334155", font=f_body)
    draw.text((700, 488), t_rb, fill="#334155", font=f_body)
    draw.text((700, 514), t_hq, fill="#DC2626", font=get_font(13, bold=True))

    # LLM Vulnerability Conclusion (Overflow-Free Layout)
    draw_sharp_rect(draw, (680, 560, 1260, 745), fill="#FEF2F2", outline="#DC2626", width=1)
    draw.text((700, 572), "BẢN CHẤT LỖ HỔNG & YÊU CẦU PHÒNG THỦ:" if is_vi else "VULNERABILITY NATURE & DEFENSE REQUIREMENT:", fill="#B91C1C", font=f_badge)
    
    if is_vi:
        draw.text((700, 598), "• Căn chỉnh an toàn RLHF/DPO nội tại BẤT LỰC:", fill="#0F172A", font=f_h3)
        draw.text((718, 622), "Mô hình coi lệnh tiêm U là chỉ thị hợp lệ mới từ người dùng.", fill="#334155", font=f_body)
        draw.text((700, 648), "• BẮT BUỘC CÓ EXTERNAL GUARDRAIL PROXY TẠI INGRESS:", fill="#0284C7", font=f_h3)
        draw.text((718, 672), "Phân loại văn bản độc lập trước khi nạp vào ngữ cảnh của LLM.", fill="#334155", font=f_body)
        draw.text((700, 702), "-> Đây chính là sứ mệnh khoa học cốt tử của đồ án PI-Guard!", fill="#047857", font=get_font(13, bold=True))
    else:
        draw.text((700, 598), "• Internal RLHF/DPO safety alignment is HELPLESS:", fill="#0F172A", font=f_h3)
        draw.text((718, 622), "The LLM inherently treats injected prompt U as valid new instructions.", fill="#334155", font=f_body)
        draw.text((700, 648), "• MANDATORY EXTERNAL GUARDRAIL PROXY AT INGRESS:", fill="#0284C7", font=f_h3)
        draw.text((718, 672), "Classify text independently before ingestion into LLM context window.", fill="#334155", font=f_body)
        draw.text((700, 702), "-> This defines the fundamental scientific mission of PI-Guard!", fill="#047857", font=get_font(13, bold=True))

    suffix = "_en.png" if not is_vi else ".png"
    out_p = os.path.join(FIGURES_DIR, f"diagram_flat_token_space{suffix}")
    img.save(out_p, quality=95)
    print(f"Generated: {out_p}")


# ==============================================================================
# DIAGRAM 3: 5-AXIS ATTACK SURFACE FRAMEWORK (NO CONFUSING ACRONYM BRACKETS)
# ==============================================================================
def generate_5d_threat_diagram(lang="vi"):
    w, h = 1350, 800
    img = Image.new("RGB", (w, h), "#FFFFFF")
    draw = ImageDraw.Draw(img)

    f_title = get_font(26, bold=True)
    f_sub = get_font(15, bold=False)
    f_h3 = get_font(15, bold=True)
    f_body = get_font(13, bold=False)
    f_mono = get_font(12, bold=True)
    f_badge = get_font(12, bold=True)

    is_vi = (lang == "vi")

    title = "KHUNG PHÂN TÍCH BỀ MẶT TẤN CÔNG 5 TRỤC TOÀN DIỆN" if is_vi else "5-AXIS ATTACK SURFACE ANALYSIS FRAMEWORK"
    sub = "Chuẩn hóa theo NIST AI 100-2e2025 & MITRE ATLAS: Đối chiếu Kênh 1 Direct, Kênh 2 Indirect RAG & Jailbreak" if is_vi else "Standardized under NIST AI 100-2e2025 & MITRE ATLAS: Direct Chat vs. Indirect RAG vs. Jailbreak"
    draw.text((40, 25), title, fill="#0284C7", font=f_title)
    draw.text((40, 65), sub, fill="#64748B", font=f_sub)

    if is_vi:
        cols = [
            ("KÊNH 1: DIRECT CHAT INJECTION", "#0284C7", "#EFF6FF", [
                ("1. Cơ chế & Payload", "Ghi đè mệnh lệnh trực tiếp, Delimiter hijacking, đóng vai debug mode."),
                ("2. Threat Model", "Black-box hoàn toàn. Quyền hạn người dùng thông thường, chi phí Zero-Cost."),
                ("3. Luồng hoạt động", "UI/API -> Ghép chuỗi X=S||U -> Self-Attention -> Hijacked Response."),
                ("4. Dấu vết nhận diện", "Cú pháp: từ khóa phủ định ('ignore', 'instead'). Ngữ nghĩa: đối kháng System."),
                ("5. Bán kính thiệt hại", "Rò rỉ System Prompt, chiếm quyền trợ lý ảo, vi phạm chính sách bảo mật.")
            ]),
            ("KÊNH 2: INDIRECT FILE / RAG INJECTION", "#D97706", "#FFFBEB", [
                ("1. Cơ chế & Payload", "Cấy mã độc vào PDF/DOCX/Web. Lệnh ẩn kích hoạt khi LLM tóm tắt tài liệu."),
                ("2. Threat Model", "Gray-box. Kẻ tấn công kiểm soát tài liệu ngoài; người dùng vô tình kích hoạt."),
                ("3. Luồng hoạt động", "Tải file -> Parser trích xuất raw text -> RAG Vector Search -> LLM Exfiltration."),
                ("4. Dấu vết nhận diện", "Ký tự tàng hình (Zero-width), lệnh ép trích xuất dữ liệu, thẻ Markdown Image."),
                ("5. Bán kính thiệt hại", "Đánh cắp bí mật kinh doanh, API keys, dữ liệu PII người dùng qua webhook ngầm.")
            ]),
            ("NHÓM 3: JAILBREAK ATTACKS (DAN)", "#DC2626", "#FEF2F2", [
                ("1. Cơ chế & Payload", "Nhập vai DAN (Do Anything Now), giả định khoa học, kỹ thuật thôi miên."),
                ("2. Threat Model", "Black/Gray-box. Khai thác Competing Objectives & Mismatched Generalization."),
                ("3. Luồng hoạt động", "Prompt UI -> Vượt qua ranh giới từ chối (Refusal Boundary) trong trọng số theta."),
                ("4. Dấu vết nhận diện", "Kịch bản đóng vai dài, từ khóa 'unrestricted', 'free from rules', base64 cipher."),
                ("5. Bán kính thiệt hại", "Phát ngôn độc hại, hướng dẫn chế tạo vũ khí/chất cấm, vi phạm pháp luật nghiêm trọng.")
            ])
        ]
    else:
        cols = [
            ("CHANNEL 1: DIRECT CHAT INJECTION", "#0284C7", "#EFF6FF", [
                ("1. Mechanism & Payload", "Direct instruction override, delimiter hijacking, debug mode persona."),
                ("2. Threat Model", "Pure Black-box. Standard user privilege level, Zero-Cost execution."),
                ("3. Execution Flow", "UI/API -> Flat concat X=S||U -> Self-Attention hijacking -> Overridden output."),
                ("4. Detection Footprint", "Syntax: negation keywords ('ignore', 'instead'). Semantics: System conflict."),
                ("5. Blast Radius", "System Prompt leakage, agent mission hijacking, policy violations.")
            ]),
            ("CHANNEL 2: INDIRECT FILE / RAG INJECTION", "#D97706", "#FFFBEB", [
                ("1. Mechanism & Payload", "Malicious payload planted in PDF/DOCX/Web. Activates upon summarization."),
                ("2. Threat Model", "Gray-box. Attacker poisons external source; innocent user triggers payload."),
                ("3. Execution Flow", "File ingest -> Parser extracts raw text -> RAG Vector Search -> Exfiltration."),
                ("4. Detection Footprint", "Invisible Zero-width chars, exfiltration markdown images, covert webhooks."),
                ("5. Blast Radius", "Proprietary IP theft, corporate API key exfiltration, sensitive PII leakage.")
            ]),
            ("GROUP 3: JAILBREAK ATTACKS (DAN)", "#DC2626", "#FEF2F2", [
                ("1. Mechanism & Payload", "DAN (Do Anything Now) roleplay, hypothetical research, cognitive framing."),
                ("2. Threat Model", "Black/Gray-box. Exploits Competing Objectives & Mismatched Generalization."),
                ("3. Execution Flow", "Prompt Ingress -> Bypasses safety Refusal Boundary in model weights theta."),
                ("4. Detection Footprint", "Elaborate multi-persona framing, tokens like 'unrestricted', cipher obfuscation."),
                ("5. Blast Radius", "Harmful content generation, illegal CBRN advice, critical legal liability.")
            ])
        ]

    card_w = 405
    gap = 25
    for idx, (col_title, col_clr, col_bg, items) in enumerate(cols):
        c_x = 40 + idx * (card_w + gap)
        draw_sharp_rect(draw, (c_x, 110, c_x + card_w, 755), fill="#FFFFFF", outline=col_clr, width=2)
        draw_sharp_rect(draw, (c_x, 110, c_x + card_w, 155), fill=col_bg, outline=col_clr, width=1)
        draw.text((c_x + 15, 125), col_title, fill=col_clr, font=f_badge)

        y_cursor = 175
        for axis_title, axis_desc in items:
            draw_sharp_rect(draw, (c_x + 12, y_cursor, c_x + card_w - 12, y_cursor + 98), fill="#F8FAFC", outline="#E2E8F0", width=1)
            draw.text((c_x + 22, y_cursor + 10), axis_title, fill="#0F172A", font=f_h3)
            
            # Simple text wrap
            words = axis_desc.split(" ")
            line1, line2 = "", ""
            for w_item in words:
                if len(line1 + " " + w_item) < 42:
                    line1 += (" " if line1 else "") + w_item
                else:
                    line2 += (" " if line2 else "") + w_item
            
            draw.text((c_x + 22, y_cursor + 38), line1, fill="#334155", font=f_body)
            if line2:
                draw.text((c_x + 22, y_cursor + 62), line2, fill="#334155", font=f_body)
            
            y_cursor += 112

    suffix = "_en.png" if not is_vi else ".png"
    out_p = os.path.join(FIGURES_DIR, f"diagram_5d_threat_framework{suffix}")
    img.save(out_p, quality=95)
    print(f"Generated: {out_p}")


# ==============================================================================
# DIAGRAM 4: TRI-STATE UNCERTAINTY DISTRIBUTION
# ==============================================================================
def generate_tri_state_distribution(lang="vi"):
    w, h = 1200, 700
    img = Image.new("RGB", (w, h), "#FFFFFF")
    draw = ImageDraw.Draw(img)

    f_title = get_font(25, bold=True)
    f_sub = get_font(15, bold=False)
    f_h3 = get_font(15, bold=True)
    f_body = get_font(13, bold=False)
    f_mono = get_font(13, bold=True)
    f_badge = get_font(12, bold=True)

    is_vi = (lang == "vi")

    title = "ĐỘNG HỌC ĐỊNH TUYẾN BẤT ĐỊNH 3 TRẠNG THÁI (TRI-STATE UNCERTAINTY ROUTING)" if is_vi else "TRI-STATE UNCERTAINTY ROUTING DYNAMICS"
    sub = "Phân bổ ngưỡng xác suất P(Y=1|X) giải phóng 82.6% lưu lượng tại Tầng 1 và thẩm định 17.4% bất định tại Tầng 2" if is_vi else "Probability threshold distribution P(Y=1|X) fast-filtering 82.6% at Tier 1 and routing 17.4% to Tier 2"
    draw.text((40, 25), title, fill="#0284C7", font=f_title)
    draw.text((40, 65), sub, fill="#64748B", font=f_sub)

    # Main Spectrum Bar
    bar_x0, bar_y0, bar_x1, bar_y1 = 80, 220, 1120, 310
    total_w = bar_x1 - bar_x0
    
    # Region 1: Green [0.0, 0.15] -> 15% of width
    w1 = int(total_w * 0.15)
    draw_sharp_rect(draw, (bar_x0, bar_y0, bar_x0 + w1, bar_y1), fill="#ECFDF5", outline="#059669", width=2)
    draw.text((bar_x0 + 20, bar_y0 + 25), "FAST PASS" if not is_vi else "THÔNG QUA NHANH", fill="#047857", font=f_h3)
    draw.text((bar_x0 + 20, bar_y0 + 52), "71.3% Lưu Lượng" if is_vi else "71.3% of Traffic", fill="#047857", font=f_mono)

    # Region 2: Amber [0.15, 0.85] -> 70% of width
    w2 = int(total_w * 0.70)
    draw_sharp_rect(draw, (bar_x0 + w1, bar_y0, bar_x0 + w1 + w2, bar_y1), fill="#FFFBEB", outline="#D97706", width=2)
    draw.text((bar_x0 + w1 + 180, bar_y0 + 25), "VÙNG BẤT ĐỊNH (UNCERTAINTY ZONE) -> CHUYỂN GIAO TẦNG 2" if is_vi else "UNCERTAINTY ZONE -> ESCALATE TO TIER 2 ARBITER", fill="#B45309", font=f_h3)
    draw.text((bar_x0 + w1 + 250, bar_y0 + 52), "17.4% Mẫu Cần Thẩm Định Chuyên Sâu" if is_vi else "17.4% Complex Boundary Samples", fill="#B45309", font=f_mono)

    # Region 3: Red [0.85, 1.0] -> 15% of width
    draw_sharp_rect(draw, (bar_x0 + w1 + w2, bar_y0, bar_x1, bar_y1), fill="#FEF2F2", outline="#DC2626", width=2)
    draw.text((bar_x0 + w1 + w2 + 15, bar_y0 + 25), "EARLY BLOCK" if not is_vi else "CHẶN TỨC THÌ", fill="#B91C1C", font=f_h3)
    draw.text((bar_x0 + w1 + w2 + 15, bar_y0 + 52), "11.3% Lưu Lượng" if is_vi else "11.3% of Traffic", fill="#B91C1C", font=f_mono)

    # Threshold markers
    draw.text((bar_x0 - 15, bar_y0 - 35), "P = 0.0", fill="#0F172A", font=f_mono)
    draw.text((bar_x0 + w1 - 25, bar_y0 - 35), "tau_low = 0.15", fill="#059669", font=f_mono)
    draw.text((bar_x0 + w1 + w2 - 30, bar_y0 - 35), "tau_high = 0.85", fill="#DC2626", font=f_mono)
    draw.text((bar_x1 - 35, bar_y0 - 35), "P = 1.0", fill="#0F172A", font=f_mono)

    # Dotted tick lines
    draw.line([(bar_x0 + w1, bar_y0 - 12), (bar_x0 + w1, bar_y1 + 15)], fill="#059669", width=2)
    draw.line([(bar_x0 + w1 + w2, bar_y0 - 12), (bar_x0 + w1 + w2, bar_y1 + 15)], fill="#DC2626", width=2)

    # Detailed Explanatory Cards below
    cards = [
        ("FAST-PASS DIRECT ROUTING", "#059669", "#ECFDF5", [
            ("Ngưỡng quyết định:", "P(Attack|X) <= 0.15") if is_vi else ("Decision Threshold:", "P(Attack|X) <= 0.15"),
            ("Hành vi hệ thống:", "Chuyển tiếp trực tiếp sang LLM đích") if is_vi else ("System Behavior:", "Forward directly to Downstream LLM"),
            ("Độ trễ xử lý:", "< 1.0 ms (Tầng 1 hoàn tất ~0.47 ms)") if is_vi else ("Processing Latency:", "< 1.0 ms (Tier 1 completes in ~0.47 ms)"),
            ("Ý nghĩa vận hành:", "Giải phóng 71.3% truy vấn an toàn") if is_vi else ("Operational Benefit:", "Frees 71.3% of traffic instantly")
        ]),
        ("ESCALATE TO TIER 2 (DEBERTA)", "#D97706", "#FFFBEB", [
            ("Ngưỡng quyết định:", "0.15 < P(Attack|X) < 0.85") if is_vi else ("Decision Threshold:", "0.15 < P(Attack|X) < 0.85"),
            ("Hành vi hệ thống:", "Kích hoạt DeBERTa-v3 ONNX INT8") if is_vi else ("System Behavior:", "Trigger DeBERTa-v3 ONNX INT8 Arbiter"),
            ("Độ trễ xử lý:", "~18.5 ms (AVX-512 CPU INT8)") if is_vi else ("Processing Latency:", "~18.5 ms (AVX-512 CPU INT8)"),
            ("Ý nghĩa vận hành:", "Thẩm định sâu 17.4% ca bất định") if is_vi else ("Operational Benefit:", "Deeply inspects 17.4% ambiguous cases")
        ]),
        ("EARLY BLOCK SYSTEM", "#DC2626", "#FEF2F2", [
            ("Ngưỡng quyết định:", "P(Attack|X) >= 0.85") if is_vi else ("Decision Threshold:", "P(Attack|X) >= 0.85"),
            ("Hành vi hệ thống:", "Ngắt kết nối, trả về HTTP 403 Forbidden") if is_vi else ("System Behavior:", "Drop connection, return HTTP 403"),
            ("Độ trễ xử lý:", "< 0.5 ms (Không tốn token LLM)") if is_vi else ("Processing Latency:", "< 0.5 ms (Consumes zero LLM tokens)"),
            ("Ý nghĩa vận hành:", "Chặn đứng 11.3% đòn tấn công thô") if is_vi else ("Operational Benefit:", "Early blocks 11.3% brute-force attacks")
        ])
    ]

    c_w = 320
    c_gap = 40
    for idx, (c_title, c_clr, c_bg, items) in enumerate(cards):
        cx = 80 + idx * (c_w + c_gap)
        draw_sharp_rect(draw, (cx, 370, cx + c_w, 640), fill="#FFFFFF", outline=c_clr, width=2)
        draw_sharp_rect(draw, (cx, 370, cx + c_w, 415), fill=c_bg, outline=c_clr, width=1)
        draw.text((cx + 15, 385), c_title, fill=c_clr, font=f_badge)

        cy = 430
        for lbl, val in items:
            draw.text((cx + 15, cy), lbl, fill="#0F172A", font=get_font(12, bold=True))
            draw.text((cx + 15, cy + 22), val, fill="#334155", font=f_body)
            cy += 50

    suffix = "_en.png" if not is_vi else ".png"
    out_p = os.path.join(FIGURES_DIR, f"diagram_tri_state_distribution{suffix}")
    img.save(out_p, quality=95)
    print(f"Generated: {out_p}")


def main():
    print("Generating High-Resolution Presentation Diagrams for PI-Guard...")
    for lang in ["vi", "en"]:
        print(f"\n--- Generating language: {lang.upper()} ---")
        generate_two_tier_diagram(lang=lang)
        generate_flat_token_diagram(lang=lang)
        generate_5d_threat_diagram(lang=lang)
        generate_tri_state_distribution(lang=lang)
    print("\nAll 8 diagrams (4 Vietnamese + 4 English) successfully generated in:", FIGURES_DIR)

if __name__ == "__main__":
    main()
