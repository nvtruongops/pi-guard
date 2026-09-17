import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"workspaces\truongnv\reports\tasks_for_meeting_5"
files = []
for root, dirs, filenames in os.walk(base_dir):
    if ".venv" in root or "node_modules" in root:
        continue
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

blacklist = [
    "thời gian thực",
    "real-time",
    "tuyệt đối",
    "100% unbreakable",
    "bảo vệ tuyệt đối",
    "production-ready"
]

print("| STT | Tệp Tin (File) | In-Text Refs | Anchors | Missing Anchors | Images (Total/Valid/Broken) | Blacklist Warnings |")
print("| :---: | :--- | :---: | :---: | :---: | :---: | :--- |")

broken_details = []

for idx, fpath in enumerate(sorted(files), 1):
    rel = os.path.relpath(fpath, base_dir).replace("\\", "/")
    with open(fpath, "r", encoding="utf-8", errors="ignore") as fp:
        content = fp.read()
    
    in_text_refs = sorted(list(set(re.findall(r"\[\[(\d+)\]\]", content))), key=lambda x: int(x))
    anchors = sorted(list(set(re.findall(r'<a\s+id=["\']ref(\d+)["\']', content))), key=lambda x: int(x))
    missing_anchors = sorted(list(set(in_text_refs) - set(anchors)), key=lambda x: int(x))
    
    # images (strip code blocks first to avoid matching example markdown syntax)
    content_no_code = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    content_no_code = re.sub(r'`[^`\n]+`', '', content_no_code)
    imgs = re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", content_no_code)
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
            
    body_for_bl = re.split(r'##\s+.*(?:TÀI LIỆU THAM KHẢO|REFERENCES)', content, flags=re.IGNORECASE)[0]
    bl_found = []
    for b in blacklist:
        matches = re.findall(re.escape(b), body_for_bl, re.IGNORECASE)
        if matches:
            bl_found.append(f"{b} ({len(matches)})")
            
    miss_anc_str = ", ".join([f"ref{x}" for x in missing_anchors]) if missing_anchors else "0 (PASS)"
    img_str = f"{len(imgs)} / {len(valid_imgs)} / {len(missing_imgs)}"
    bl_str = ", ".join(bl_found) if bl_found else "PASS"
    
    print(f"| {idx} | `{rel}` | {len(in_text_refs)} | {len(anchors)} | {miss_anc_str} | {img_str} | {bl_str} |")
    
    if missing_imgs:
        broken_details.append((rel, "BROKEN_IMAGES", missing_imgs))
    if missing_anchors:
        broken_details.append((rel, "BROKEN_ANCHORS", missing_anchors))
    if bl_found:
        broken_details.append((rel, "BLACKLIST", bl_found))

print("\n--- CHI TIẾT CÁC ĐIỂM CẦN HOÀN THIỆN ---")
for item in broken_details:
    print(f"\n[!] {item[0]} - {item[1]}:")
    for d in item[2]:
        print(f"    - {d}")
