import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"workspaces\truongnv\reports\tasks_for_meeting_5"
files = []
for root, dirs, filenames in os.walk(base_dir):
    if ".venv" in root or "node_modules" in root:
        continue
    # skip cloned upstream repos
    if any(repo in root for repo in [
        "InstructDetector_EMNLP2024\\InstructDetector_EMNLP2024",
        "Jain_NeurIPS2023\\Jain_NeurIPS2023",
        "Meta_PromptGuard2024\\Meta_PromptGuard2024",
        "Ayub_CAMLIS2024\\Ayub_CAMLIS2024",
        "PIGuard_ACL2025\\PIGuard_ACL2025"
    ]):
        continue
    for f in filenames:
        if f.endswith(".md"):
            files.append(os.path.join(root, f))

print(f"Total project markdown files found: {len(files)}")

blacklist = [
    "thời gian thực",
    "real-time",
    "tuyệt đối",
    "100% unbreakable",
    "bảo vệ tuyệt đối",
    "production-ready"
]

report = []
for fpath in sorted(files):
    rel = os.path.relpath(fpath, base_dir)
    with open(fpath, "r", encoding="utf-8", errors="ignore") as fp:
        content = fp.read()
    
    # citations
    in_text_refs = sorted(list(set(re.findall(r"\[\[(\d+)\]\]", content))), key=lambda x: int(x))
    anchors = sorted(list(set(re.findall(r'<a\s+id=["\']ref(\d+)["\']', content))), key=lambda x: int(x))
    missing_anchors = sorted(list(set(in_text_refs) - set(anchors)), key=lambda x: int(x))
    unused_anchors = sorted(list(set(anchors) - set(in_text_refs)), key=lambda x: int(x))
    
    # images
    imgs = re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", content)
    missing_imgs = []
    valid_imgs = []
    fdir = os.path.dirname(fpath)
    for alt, img_path in imgs:
        if img_path.startswith("http"):
            continue
        clean_p = img_path.replace("file:///", "").replace("/", os.sep)
        if not os.path.isabs(clean_p):
            target = os.path.normpath(os.path.join(fdir, clean_p))
        else:
            target = clean_p
        if not os.path.exists(target):
            missing_imgs.append((img_path, target))
        else:
            valid_imgs.append(clean_p)
            
    # blacklist matches
    bl_found = []
    for b in blacklist:
        matches = re.findall(re.escape(b), content, re.IGNORECASE)
        if matches:
            bl_found.append(f"{b} ({len(matches)})")
            
    has_refs_section = bool(re.search(r"#+\s*(?:TÀI LIỆU THAM KHẢO|REFERENCES|References)", content, re.IGNORECASE))
    
    report.append({
        "file": rel,
        "size": len(content),
        "in_text": in_text_refs,
        "anchors": anchors,
        "missing_anchors": missing_anchors,
        "unused_anchors": unused_anchors,
        "imgs_count": len(imgs),
        "missing_imgs": missing_imgs,
        "valid_imgs_count": len(valid_imgs),
        "has_refs_section": has_refs_section,
        "blacklist": bl_found
    })

for r in report:
    print("=" * 80)
    print(f"FILE: {r['file']} ({r['size']:,} chars)")
    print(f"  Has Refs Section: {r['has_refs_section']}")
    print(f"  In-text Citations ({len(r['in_text'])}): {r['in_text']}")
    print(f"  Reference Anchors ({len(r['anchors'])}): {r['anchors']}")
    if r['missing_anchors']:
        print(f"  [!] BROKEN ANCHORS (cited but no anchor): {r['missing_anchors']}")
    if r['unused_anchors']:
        print(f"  [*] Unused Anchors (anchor defined but not cited in text): {r['unused_anchors']}")
    print(f"  Images: {r['imgs_count']} total | Valid on disk: {r['valid_imgs_count']} | Broken: {len(r['missing_imgs'])}")
    if r['missing_imgs']:
        for orig, target in r['missing_imgs']:
            print(f"      [!] MISSING IMAGE: {orig} -> {target}")
    if r['blacklist']:
        print(f"  [!] BLACKLIST WARNING: {r['blacklist']}")
