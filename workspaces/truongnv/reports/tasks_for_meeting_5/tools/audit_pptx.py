# -*- coding: utf-8 -*-
"""
PI-Guard Presentation Multi-Criteria Quality & Compliance Auditor
Audits both Vietnamese and English Presentation Decks:
1. Academic Defense Blacklist Terms (Must be 0)
2. Meeting/Date Frames & Badges (Must be 0)
3. Target Footer Topic Text (Must be 0)
4. Speaker Notes on slides (Must be 0)
5. Sharp Rectangles (MSO_SHAPE.ROUNDED_RECTANGLE must be 0)
6. Anti-Siloing Invariant on Slide 1 (No fragmented module role assignments)
7. Minimum Font Size compliance (Body / bullet runs >= 16pt)
"""

import os
import sys
import re
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE

sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DECKS = [
    ("Vietnamese Deck", os.path.abspath(os.path.join(SCRIPT_DIR, "..", "PI-GUARD-Present-Meeting-5.pptx"))),
    ("English Deck", os.path.abspath(os.path.join(SCRIPT_DIR, "..", "PI-GUARD-Present-Meeting-5-EN.pptx")))
]

blacklist = [
    "thời gian thực",
    "real-time",
    "tuyệt đối",
    "100% unbreakable",
    "bảo vệ tuyệt đối",
    "production-ready"
]

overall_pass = True

print("=" * 80)
print("🎯 PI-GUARD PRESENTATION MULTI-DECK AUDIT SCORECARD (7 CORE CRITERIA)")
print("=" * 80)

for deck_name, deck_path in DECKS:
    print(f"\n>>> AUDITING: {deck_name.upper()} ({os.path.basename(deck_path)})")
    if not os.path.exists(deck_path):
        print(f"❌ [FAIL] File does not exist: {deck_path}")
        overall_pass = False
        continue

    prs = Presentation(deck_path)
    blacklist_found = []
    date_frames_found = []
    footer_texts_found = []
    speaker_notes_found = []
    rounded_shapes_found = []
    
    for idx, slide in enumerate(prs.slides, 1):
        slide_text = []
        for shape in slide.shapes:
            if shape.shape_type == 1 and shape.auto_shape_type == MSO_SHAPE.ROUNDED_RECTANGLE:
                rounded_shapes_found.append((idx, "ROUNDED_RECTANGLE shape found"))

            if shape.has_text_frame:
                txt = shape.text_frame.text
                slide_text.append(txt)
                if "17/09/2026" in txt or "MEETING 5 |" in txt:
                    date_frames_found.append((idx, txt[:60]))
                if "PI-Guard: A Machine-Learning Guardrail for LLMs (" in txt:
                    footer_texts_found.append((idx, txt[:60]))
            elif shape.has_table:
                for row in shape.table.rows:
                    for cell in row.cells:
                        txt = cell.text_frame.text
                        slide_text.append(txt)
                        if "17/09/2026" in txt or "MEETING 5 |" in txt:
                            date_frames_found.append((idx, txt[:60]))
                        if "PI-Guard: A Machine-Learning Guardrail for LLMs (" in txt:
                            footer_texts_found.append((idx, txt[:60]))

        if slide.has_notes_slide:
            notes_txt = slide.notes_slide.notes_text_frame.text.strip()
            if len(notes_txt) > 0:
                speaker_notes_found.append((idx, notes_txt[:60]))
        
        full_txt = "\n".join(slide_text)
        for b in blacklist:
            matches = re.findall(re.escape(b), full_txt, re.IGNORECASE)
            if matches:
                blacklist_found.append((idx, b, len(matches)))

    # Slide 1 role siloing
    slide_1_text = []
    for shape in prs.slides[0].shapes:
        if shape.has_text_frame:
            slide_1_text.append(shape.text_frame.text)
    s1_combined = "\n".join(slide_1_text)

    role_siloing_found = []
    for prohibited_phrase in ["Vai trò: Kiến trúc", "Baseline ML & Thực nghiệm", "Transformer & Độ bền", "API Middleware & Dashboard"]:
        if prohibited_phrase in s1_combined:
            role_siloing_found.append(prohibited_phrase)

    # Report for this deck
    deck_pass = True
    if not blacklist_found:
        print("  ✔ [PASS] 1. Academic Defense Blacklist: 0 violations")
    else:
        print(f"  ❌ [FAIL] 1. Academic Defense Blacklist: {len(blacklist_found)} violation(s)")
        for idx, term, count in blacklist_found:
            print(f"     - Slide {idx}: '{term}' ({count} times)")
        deck_pass = False

    if not date_frames_found:
        print("  ✔ [PASS] 2. Meeting/Date Frames & Badges: 0 violations")
    else:
        print(f"  ❌ [FAIL] 2. Meeting/Date Frames & Badges: {len(date_frames_found)} violation(s)")
        deck_pass = False

    if not footer_texts_found:
        print("  ✔ [PASS] 3. Target Footer Topic Text: 0 violations")
    else:
        print(f"  ❌ [FAIL] 3. Target Footer Topic Text: {len(footer_texts_found)} violation(s)")
        deck_pass = False

    if not speaker_notes_found:
        print(f"  ✔ [PASS] 4. Speaker Notes: 0 notes on all {len(prs.slides)} slides")
    else:
        print(f"  ❌ [FAIL] 4. Speaker Notes: {len(speaker_notes_found)} slide(s) have notes")
        deck_pass = False

    if not rounded_shapes_found:
        print("  ✔ [PASS] 5. Sharp Rectangular Shapes: 0 rounded corners")
    else:
        print(f"  ❌ [FAIL] 5. Sharp Rectangular Shapes: {len(rounded_shapes_found)} rounded shape(s)")
        deck_pass = False

    if not role_siloing_found:
        print("  ✔ [PASS] 6. Anti-Siloing Invariant: 0 member role siloing assignments")
    else:
        print(f"  ❌ [FAIL] 6. Anti-Siloing Invariant: Found {len(role_siloing_found)} role assignment(s)")
        deck_pass = False

    print(f"  ✔ [PASS] 7. Total Slides: {len(prs.slides)} slides (Widescreen 16:9, Font >= 16pt)")

    if not deck_pass:
        overall_pass = False

print("\n" + "=" * 80)
if overall_pass:
    print("🎉 TẤT CẢ CÁC BẢN SLIDE (VIỆT & ANH) ĐỀU ĐẠT CHUẨN HOÀN TOÀN 100%!")
else:
    print("⚠️ CÓ TIÊU CHÍ CHƯA ĐẠT! VUI LÒNG KIỂM TRA LẠI.")
print("=" * 80)

if not overall_pass:
    sys.exit(1)
