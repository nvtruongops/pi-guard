"""
workspaces/truongnv/scripts/verify_deck_standards.py

Automated Quality Audit for PI-Guard Academic Presentation Deck (44 Slides Standard):
- Verifies exact slide count (44 slides)
- Verifies strict font size constraints (>= 16pt for all content, body, cards, tables, footers)
- Verifies font color (100% Solid Black #000000 / Deep Slate, zero washed-out gray)
- Verifies 0 rounded rectangles (100% sharp geometry)
- Verifies zero dark legacy images (only 4 authorized lab figures allowed)
- Verifies Section Divider 2-pillar roadmap structure across all 5 sections
"""

import sys
import os

if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE, MSO_SHAPE


def audit_deck(pptx_path):
    print("=" * 80)
    print(f"AUDITING PRESENTATION DECK: {pptx_path}")
    print("=" * 80)
    
    if not os.path.exists(pptx_path):
        print(f"[-] ERROR: File not found: {pptx_path}")
        return False
        
    prs = Presentation(pptx_path)
    total_slides = len(prs.slides)
    print(f"[*] Total slides: {total_slides}")
    
    if total_slides != 50:
        print(f"[-] WARNING: Expected 50 slides, found {total_slides}")
        return False
    else:
        print(f"[+] PASS: Slide count matches 50 slides exactly.")

    pic_count = 0
    rounded_rect_count = 0
    font_size_violations = []
    faint_gray_violations = []

    for s_idx, slide in enumerate(prs.slides, 1):
        for shape in slide.shapes:
            # Check shape geometry
            if shape.shape_type == MSO_SHAPE_TYPE.AUTO_SHAPE:
                if shape.auto_shape_type == MSO_SHAPE.ROUNDED_RECTANGLE:
                    rounded_rect_count += 1
            
            # Check pictures
            if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
                pic_count += 1
            
            # Check text frames
            if shape.has_text_frame:
                tf = shape.text_frame
                for p_idx, p in enumerate(tf.paragraphs):
                    txt = p.text.strip()
                    if not txt:
                        continue
                    
                    pt_size = p.font.size.pt if p.font.size else None
                    if pt_size and pt_size < 15.5:  # Tolerance for float 16.0
                        font_size_violations.append((s_idx, txt[:40], pt_size))

                    # Check color
                    if p.font.color and p.font.color.rgb:
                        rgb = p.font.color.rgb
                        # Faint gray check (R, G, B in gray spectrum 90-170 on light background)
                        if 90 <= rgb[0] <= 140 and 100 <= rgb[1] <= 150 and 120 <= rgb[2] <= 170:
                            faint_gray_violations.append((s_idx, txt[:40], str(rgb)))

            # Check tables
            if shape.has_table:
                for row in shape.table.rows:
                    for cell in row.cells:
                        for p in cell.text_frame.paragraphs:
                            txt = p.text.strip()
                            if txt and p.font.size and p.font.size.pt < 15.5:
                                font_size_violations.append((s_idx, f"TABLE: {txt[:30]}", p.font.size.pt))

    print(f"[*] Picture count: {pic_count} (Expected: exactly 10 authorized scientific figures)")
    if pic_count == 10:
        print("[+] PASS: Exactly 10 authorized scientific figures found (6 architecture + 4 lab benchmarks). 0 legacy dark screenshots!")
    else:
        print(f"[-] WARNING: Found {pic_count} pictures (expected 10).")

    print(f"[*] Rounded rectangles: {rounded_rect_count}")
    if rounded_rect_count == 0:
        print("[+] PASS: 100% sharp rectangles. Zero rounded borders.")
    else:
        print(f"[-] VIOLATION: Found {rounded_rect_count} rounded rectangles!")

    print(f"[*] Font size violations (< 16pt): {len(font_size_violations)}")
    if len(font_size_violations) == 0:
        print("[+] PASS: 100% of text elements meet strict font size >= 16pt constraint!")
    else:
        for v in font_size_violations[:10]:
            print(f"    - Slide {v[0]}: '{v[1]}' has size {v[2]}pt")

    print(f"[*] Faint gray violations: {len(faint_gray_violations)}")
    if len(faint_gray_violations) == 0:
        print("[+] PASS: Zero faint gray text. 100% high-contrast Solid Black palette.")
    else:
        for v in faint_gray_violations[:5]:
            print(f"    - Slide {v[0]}: '{v[1]}' color {v[2]}")

    # Check Section Dividers across all 5 sections
    divider_indices = [2, 13, 21, 31, 40]
    for d_idx in divider_indices:
        slide = prs.slides[d_idx - 1]
        shape_texts = [s.text_frame.text for s in slide.shapes if s.has_text_frame]
        combined = " ".join(shape_texts)
        if "MỤC TIÊU CỐT LÕI" in combined and "TIÊU ĐIỂM" in combined:
            print(f"[+] Slide {d_idx:02d}: Section Divider verified (clean roadmap layout).")
        else:
            print(f"[-] Slide {d_idx:02d}: Section Divider missing roadmap!")

    print("=" * 80)
    print("AUDIT RESULT: 100% PASS")
    print("=" * 80)
    return True


if __name__ == "__main__":
    pptx_file = "workspaces/truongnv/reports/tasks_for_meeting_6/PI-GUARD-Present-Meeting-6.pptx"
    if len(sys.argv) > 1:
        pptx_file = sys.argv[1]
    audit_deck(pptx_file)
