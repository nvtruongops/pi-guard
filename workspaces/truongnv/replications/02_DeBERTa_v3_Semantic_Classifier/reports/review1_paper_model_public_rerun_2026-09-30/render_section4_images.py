from __future__ import annotations

from pathlib import Path
from textwrap import wrap

from PIL import Image, ImageDraw, ImageFont


W, H = 1920, 1080
OUT = Path(__file__).resolve().parents[4] / "reports" / "report_for_review1" / "section4_images"
FONT_DIR = Path("C:/Windows/Fonts")

NAVY = "#102B55"
INK = "#17253A"
MUTED = "#65748A"
BLUE = "#117DA7"
CYAN = "#3DB8CE"
PURPLE = "#7654C8"
GOLD = "#F5B51B"
GREEN = "#29845E"
RED = "#C44D55"
BG = "#F5F7FB"
WHITE = "#FFFFFF"
PALE_BLUE = "#EAF5FA"
PALE_PURPLE = "#F1EDFB"
PALE_GOLD = "#FFF7DF"
PALE_GREEN = "#EAF5EF"
PALE_RED = "#FBEDEE"
LINE = "#D8E0EA"


def font(size: int, bold: bool = False, italic: bool = False) -> ImageFont.FreeTypeFont:
    filename = "arialbi.ttf" if bold and italic else "arialbd.ttf" if bold else "ariali.ttf" if italic else "arial.ttf"
    return ImageFont.truetype(str(FONT_DIR / filename), size=size)


def canvas() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, W, 14), fill=NAVY)
    d.rectangle((W - 360, 0, W, 14), fill=GOLD)
    return im, d


def text(d: ImageDraw.ImageDraw, xy: tuple[int, int], value: str, size: int,
         fill: str = INK, bold: bool = False, anchor: str | None = None) -> None:
    d.text(xy, value, font=font(size, bold), fill=fill, anchor=anchor)


def wrapped(d: ImageDraw.ImageDraw, xy: tuple[int, int], value: str, max_width: int,
            size: int = 23, fill: str = INK, bold: bool = False,
            line_gap: int = 8) -> int:
    f = font(size, bold)
    words = value.split()
    lines: list[str] = []
    line = ""
    for word in words:
        candidate = word if not line else f"{line} {word}"
        if f.getlength(candidate) <= max_width:
            line = candidate
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    y = xy[1]
    for ln in lines:
        d.text((xy[0], y), ln, font=f, fill=fill)
        y += size + line_gap
    return y


def paragraph(d: ImageDraw.ImageDraw, x: int, y: int, value: str, width: int,
              size: int = 22, fill: str = INK, bullet_color: str | None = None,
              bold: bool = False) -> int:
    if value.startswith("• "):
        d.ellipse((x, y + 10, x + 8, y + 18), fill=bullet_color or BLUE)
        value = value[2:]
        x += 22
        width -= 22
    return wrapped(d, (x, y), value, width, size, fill, bold, 7) + 8


def card(d: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int, title: str,
         accent: str, fill: str = WHITE, tag: str | None = None) -> None:
    d.rounded_rectangle((x, y, x + w, y + h), radius=22, fill=fill, outline=LINE, width=2)
    d.rounded_rectangle((x, y, x + w, y + 12), radius=8, fill=accent)
    if tag:
        d.rounded_rectangle((x + 22, y + 24, x + 158, y + 58), radius=15, fill=accent)
        text(d, (x + 90, y + 41), tag, 16, WHITE, True, "mm")
        title_y = y + 74
    else:
        title_y = y + 30
    wrapped(d, (x + 24, title_y), title, w - 48, 27, NAVY, True, 3)


def arrow(d: ImageDraw.ImageDraw, x1: int, y: int, x2: int, color: str = BLUE, width: int = 6) -> None:
    d.line((x1, y, x2 - 15, y), fill=color, width=width)
    d.polygon([(x2 - 15, y - 10), (x2, y), (x2 - 15, y + 10)], fill=color)


def header(d: ImageDraw.ImageDraw, title: str, subtitle: str, index: str) -> None:
    d.rounded_rectangle((60, 48, 140, 128), radius=8, fill=GOLD)
    text(d, (100, 88), "4", 52, NAVY, True, "mm")
    text(d, (165, 50), title, 43, NAVY, True)
    text(d, (168, 110), subtitle, 22, MUTED)
    text(d, (W - 70, 76), index, 19, BLUE, True, "rm")
    d.line((66, 177, W - 66, 177), fill=LINE, width=2)


def footer(d: ImageDraw.ImageDraw, left: str, right: str = "SECTION 04 · ARCHITECTURE PROPOSAL") -> None:
    d.line((66, 1017, W - 66, 1017), fill=LINE, width=2)
    text(d, (70, 1036), left, 16, MUTED)
    text(d, (W - 70, 1036), right, 16, MUTED, True, "ra")


def save(im: Image.Image, filename: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    im.save(OUT / filename, format="PNG", optimize=True)


def architecture_overview() -> None:
    im, d = canvas()
    text(d, (70, 52), "TWO-TIER CASCADED GUARDRAIL ARCHITECTURE", 40, NAVY, True)
    text(d, (72, 112), "Ingress validation → TF-IDF lexical screening → DeBERTa-v3 contextual classification", 23, MUTED)
    text(d, (W - 70, 78), "PROPOSED DESIGN", 18, BLUE, True, "ra")
    d.line((66, 177, W - 66, 177), fill=LINE, width=2)

    y, h = 224, 486
    card(d, 70, y, 438, h, "Prompt and document input", BLUE, PALE_BLUE, "INGRESS")
    text(d, (96, 326), "INPUT SOURCES", 17, BLUE, True)
    yy = 360
    for line in ["• Chat / API prompt text", "• Document or RAG content (proposed)", "• Allowlisted input formats"]:
        yy = paragraph(d, 96, yy, line, 390, 19, INK, BLUE)
    d.rounded_rectangle((94, 500, 484, 674), radius=16, fill=WHITE, outline="#B9E5EC", width=2)
    text(d, (114, 522), "TIER 0 · INPUT VALIDATION", 17, "#168CA4", True)
    yy = 558
    for line in ["• Check type and size", "• Extract readable text", "• Preserve source offsets"]:
        yy = paragraph(d, 114, yy, line, 348, 18, INK, CYAN)

    card(d, 610, y, 548, h, "TF-IDF lexical screen", GOLD, PALE_GOLD, "TIER 1")
    yy = 354
    for line in [
        "• Word + character n-grams",
        "• Logistic Regression baseline",
        "• Locally evaluated on public data",
        "• Lexical score retained as a risk signal",
    ]:
        yy = paragraph(d, 638, yy, line, 492, 21, INK, GOLD)
    d.rounded_rectangle((638, 570, 1130, 664), radius=14, fill=WHITE, outline="#E8D9A4", width=2)
    wrapped(d, (658, 590), "A low score is not a benign verdict; continue to Tier 2 during evaluation.", 452, 18, INK, True, 5)

    card(d, 1260, y, 590, h, "DeBERTa-v3 contextual classifier", PURPLE, PALE_PURPLE, "TIER 2")
    yy = 354
    for line in [
        "• Tokenizer → encoder → classifier head",
        "• Contextual detector candidate",
        "• Released checkpoint evaluated separately",
        "• No project fine-tuning or cascade run yet",
    ]:
        yy = paragraph(d, 1288, yy, line, 534, 21, INK, PURPLE)
    d.rounded_rectangle((1288, 570, 1822, 664), radius=14, fill=WHITE, outline="#D9CFF1", width=2)
    wrapped(d, (1308, 590), "Candidate second stage for contextual classification and error analysis.", 494, 18, INK, True, 5)

    arrow(d, 526, y + h // 2, 592, BLUE)
    arrow(d, 1176, y + h // 2, 1242, BLUE)

    d.rounded_rectangle((70, 766, W - 70, 968), radius=18, fill=WHITE, outline=LINE, width=2)
    text(d, (98, 798), "EVIDENCE STATUS", 18, BLUE, True)
    wrapped(d, (98, 842), "The TF-IDF baseline and released DeBERTa-v3 checkpoint were benchmarked in separate local runs. Tier 0 document parsing and the end-to-end two-tier cascade remain proposed work; this diagram reports no cascade result.", 1680, 22, INK, False, 8)
    footer(d, "Section 04 · proposed model architecture; no operating metrics shown.", "TIER 0 → TIER 1 → TIER 2")
    save(im, "01_architecture_overview.png")


def tier0_detail() -> None:
    im, d = canvas()
    header(d, "TIER 0 | VALID INPUT → TEXT", "Input-contract and document-to-text boundary before model inference", "02 / 04")

    d.rounded_rectangle((70, 210, W - 70, 284), radius=16, fill=PALE_BLUE, outline="#C9E1EB", width=2)
    text(d, (98, 232), "CURRENT API", 18, BLUE, True)
    text(d, (250, 226), "Accepts a text field (`prompt: string`). Document upload and extraction are not implemented.", 24, INK, True)

    # Future document-to-text path.
    labels = [
        (80, 360, 325, 166, "1  FORMAT GATE", BLUE, PALE_BLUE, "Allowlist supported formats\n(define formats before release)"),
        (455, 360, 325, 166, "2  VALIDATE", CYAN, "#ECF9FB", "Check declared/detected type,\nsize bound, and parser success"),
        (830, 360, 325, 166, "3  EXTRACT", PURPLE, PALE_PURPLE, "Extract readable, non-empty\nplain text"),
        (1205, 360, 325, 166, "4  PRESERVE", GREEN, PALE_GREEN, "Keep source, page/chunk,\nand offset metadata"),
        (1580, 360, 260, 166, "TO TIER 1", GOLD, PALE_GOLD, "Pass valid text\nfor classification"),
    ]
    for x, y, w, h, tag, accent, fill, body in labels:
        card(d, x, y, w, h, tag, accent, fill)
        wrapped(d, (x + 22, y + 82), body, w - 44, 20, INK, False, 7)
    for x1, x2 in [(405, 451), (780, 826), (1155, 1201), (1530, 1576)]:
        arrow(d, x1, 443, x2, BLUE, 5)

    d.rounded_rectangle((80, 592, 910, 802), radius=20, fill=WHITE, outline=LINE, width=2)
    d.rounded_rectangle((80, 592, 910, 604), radius=8, fill=RED)
    text(d, (108, 627), "INVALID / UNSUPPORTED INPUT", 21, RED, True)
    y = 674
    for line in ["• Unsupported type or exceeded size bound", "• Corrupt, unreadable, or failed extraction", "• Empty text after extraction"]:
        y = paragraph(d, 110, y, line, 740, 20, INK, RED)
    text(d, (112, 766), "Outcome: explicit reject or documented review path", 19, MUTED, True)

    d.rounded_rectangle((956, 592, W - 80, 802), radius=20, fill=PALE_GOLD, outline="#E9D58F", width=2)
    text(d, (984, 627), "VALIDITY IS NOT A SAFETY VERDICT", 21, "#8A6505", True)
    wrapped(d, (984, 674), "A document that parses successfully is only eligible for text inspection. Its extracted content still goes through the attack detector; Tier 0 does not label content benign.", 790, 23, INK, False, 8)

    d.rounded_rectangle((80, 842, W - 80, 954), radius=18, fill=NAVY)
    text(d, (110, 865), "IMPLEMENTATION STATUS", 18, "#A9D6E9", True)
    wrapped(d, (110, 898), "Text-only ingress exists. File allowlist, MIME/size checks, parsers, extraction, and source-offset preservation are proposed work; no document format is claimed as supported.", 1660, 21, WHITE, False, 6)
    footer(d, "Tier 0 proposal only · supported document formats remain to be specified and tested.")
    save(im, "02_tier0_valid_input_to_text.png")


def tier1_detail() -> None:
    im, d = canvas()
    header(d, "TIER 1 | MEASURED TF-IDF BASELINES", "Public-source split · binary Logistic Regression route probe · distinct from 3-class LinearSVC and not a Jain reproduction", "03 / 04")

    card(d, 70, 218, 1110, 250, "Word + character hybrid (candidate baseline)", GOLD, WHITE, "WORD + CHAR")
    text(d, (104, 330), "WORD SPACE", 17, BLUE, True)
    text(d, (104, 362), "1–2 grams", 27, NAVY, True)
    text(d, (104, 402), "max 40,000 features", 19, MUTED)
    text(d, (450, 330), "+", 36, GOLD, True)
    text(d, (524, 330), "CHARACTER SPACE", 17, PURPLE, True)
    text(d, (524, 362), "char_wb 3–5 grams", 27, NAVY, True)
    text(d, (524, 402), "max 40,000 features", 19, MUTED)
    arrow(d, 866, 382, 934, GOLD, 5)
    d.rounded_rectangle((952, 332, 1148, 430), radius=15, fill=PALE_GOLD, outline="#E8D9A4", width=2)
    text(d, (1050, 357), "LOGISTIC", 18, NAVY, True, "mm")
    text(d, (1050, 389), "REGRESSION", 18, NAVY, True, "mm")
    text(d, (104, 440), "FeatureUnion · C=1 · class_weight=balanced · fitted by the project on pinned public data", 18, MUTED)

    card(d, 1210, 218, 640, 250, "Character-only comparator", PURPLE, WHITE, "CHAR-ONLY")
    text(d, (1246, 330), "char 3–5 grams", 28, NAVY, True)
    text(d, (1246, 374), "max 10,000 features", 21, MUTED)
    text(d, (1246, 417), "Logistic Regression · C=1 · class_weight=balanced", 18, MUTED)

    d.rounded_rectangle((70, 510, W - 70, 804), radius=20, fill=WHITE, outline=LINE, width=2)
    text(d, (100, 536), "LOCAL PUBLIC-VECTOR ATTACK FLAGS AT THE VALIDATION-SELECTED CUTOFF", 20, NAVY, True)
    text(d, (100, 577), "A flag count is not broad vector recall. The Direct and JailbreakBench slices contain attack rows only.", 18, MUTED)

    left, top = 100, 622
    col_x = [100, 470, 790, 1140, 1500]
    headers = ["BASELINE", "DIRECT\n(n=100)", "BIPIA ATTACK\nCONTEXT (n=200)", "JBB ARTIFACT\n(n=106)", "SOURCE TEST\nATTACK (n=167)"]
    widths = [350, 300, 330, 340, 250]
    for i, htxt in enumerate(headers):
        rows = htxt.split("\n")
        for j, row in enumerate(rows):
            text(d, (col_x[i], top + j * 23), row, 16, MUTED, True)
    d.line((100, 674, 1808, 674), fill=LINE, width=2)
    data = [
        ("Word + char", "2/100", "0/200", "35/106", "50/167"),
        ("Char-only", "4/100", "0/200", "32/106", "54/167"),
    ]
    for row_i, row in enumerate(data):
        yy = 694 + row_i * 46
        text(d, (100, yy), row[0], 20, NAVY, True)
        for i, value in enumerate(row[1:], start=1):
            text(d, (col_x[i], yy), value, 22, INK, True)
    d.line((100, 782, 1808, 782), fill=LINE, width=1)

    d.rounded_rectangle((70, 830, 910, 968), radius=18, fill=PALE_BLUE, outline="#C9E1EB", width=2)
    text(d, (96, 852), "SOURCE-HELD-OUT TEST", 17, BLUE, True)
    wrapped(d, (96, 883), "Word+char: 50/167 attacks flagged; FPR 16/1,395 (1.15%). Char-only: 54/167; FPR 19/1,395 (1.36%).", 790, 19, INK, False, 5)

    d.rounded_rectangle((928, 830, W - 70, 968), radius=18, fill=PALE_GOLD, outline="#E9D58F", width=2)
    text(d, (954, 852), "INTERPRETATION", 17, "#8A6505", True)
    wrapped(d, (954, 883), "Cutoff was selected on validation using FPR ≤1.5% as a secondary objective. Low TF-IDF scores cannot safely bypass Tier 2; current probes expose misses in Direct and Indirect too.", 820, 19, INK, False, 5)

    footer(d, "TF-IDF route-probe bundle: Model_Study_01_TFIDF_Syntactic_Baseline/reports/tier1_tfidf_public_evidence_2026-09-30 · no copied paper metrics.")
    save(im, "03_tier1_tfidf_public_baseline.png")


def tier2_detail() -> None:
    im, d = canvas()
    header(d, "TIER 2 | DeBERTa-v3 CANDIDATE", "Contextual classifier proposal informed by a locally run public checkpoint", "04 / 04")

    # Model path.
    path = [(70, 224, 260, "VALID TEXT", BLUE, PALE_BLUE),
            (378, 224, 310, "SUBWORD TOKENIZER", CYAN, "#ECF9FB"),
            (738, 224, 420, "DeBERTa-v3 ENCODER", PURPLE, PALE_PURPLE),
            (1208, 224, 300, "TASK HEAD", GOLD, PALE_GOLD),
            (1558, 224, 292, "RISK OUTPUT", GREEN, PALE_GREEN)]
    for x, y, w, name, accent, fill in path:
        d.rounded_rectangle((x, y, x + w, y + 138), radius=18, fill=fill, outline=LINE, width=2)
        d.rounded_rectangle((x, y, x + w, y + 10), radius=7, fill=accent)
        wrapped(d, (x + 20, y + 51), name, w - 40, 22, NAVY, True, 4)
    for x1, x2 in [(330, 374), (688, 734), (1158, 1204), (1508, 1554)]:
        arrow(d, x1, 293, x2, BLUE, 5)
    text(d, (790, 386), "DeBERTa-v3 model-family reference: He et al., ICLR 2023 [9]", 18, MUTED)
    text(d, (790, 418), "This diagram is a stage proposal; no PI-Guard DeBERTa fine-tune was run.", 19, RED, True)

    d.rounded_rectangle((70, 488, W - 70, 812), radius=20, fill=WHITE, outline=LINE, width=2)
    text(d, (100, 515), "LOCAL CHECKPOINT EVIDENCE — ProtectAI DeBERTa-v3, binary attack flags", 20, NAVY, True)
    text(d, (100, 553), "Pinned public-vector sample · 606 total rows · max length 512 tokens", 18, MUTED)

    # Metric tiles.
    tiles = [
        (100, 600, 390, 142, "DIRECT ATTACK", "95 / 100", BLUE, PALE_BLUE),
        (520, 600, 390, 142, "BIPIA ATTACK CONTEXT", "0 / 200", RED, PALE_RED),
        (940, 600, 390, 142, "JBB ATTACK ARTIFACT", "76 / 106", PURPLE, PALE_PURPLE),
        (1360, 600, 390, 142, "BIPIA CLEAN CONTEXT FLAG", "1 / 200", GREEN, PALE_GREEN),
    ]
    for x, y, w, h, label, value, accent, fill in tiles:
        d.rounded_rectangle((x, y, x + w, y + h), radius=16, fill=fill, outline=LINE, width=2)
        text(d, (x + 22, y + 20), label, 16, accent, True)
        text(d, (x + 22, y + 59), value, 38, NAVY, True)

    d.rounded_rectangle((70, 850, 930, 978), radius=18, fill=PALE_RED, outline="#EAC7CA", width=2)
    text(d, (96, 870), "WHAT THE SAMPLE DOES NOT SHOW", 17, RED, True)
    wrapped(d, (96, 900), "Zero flags on 200 BIPIA attack contexts means this run does not support broad Indirect coverage.", 810, 20, INK, False, 5)

    d.rounded_rectangle((948, 850, W - 70, 978), radius=18, fill=PALE_GOLD, outline="#E9D58F", width=2)
    text(d, (974, 870), "LIMITS", 17, "#8A6505", True)
    wrapped(d, (974, 900), "97/606 inputs were truncated. JBB artifact flags are not jailbreak-class recall or attack success. The live two-tier cascade remains unmeasured.", 820, 20, INK, False, 5)

    footer(d, "External checkpoint inference only · metrics are repository-run sample flags, not paper-reported values.")
    save(im, "04_tier2_deberta_v3_candidate.png")


def main() -> None:
    architecture_overview()
    tier0_detail()
    tier1_detail()
    tier2_detail()
    print(f"Rendered four 1920x1080 PNGs to {OUT}")


if __name__ == "__main__":
    main()
