"""
Script audit và kiểm tra song song toàn bộ URL trong toàn bộ repository.
Kiểm tra tính khả dụng: HTTP status, YouTube video validity, Open-access status.
"""
import json
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent

# Regex tìm URL http/https trong markdown
URL_REGEX = re.compile(r'https?://[^\s\)\]\>"\']+')

EXCLUDE_DIRS = {
    ".git", ".playwright-mcp", "site", "site_docs", ".cache", "node_modules",
    ".pytest_cache", "__pycache__", "venv", ".venv"
}

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def find_markdown_files():
    md_files = []
    for p in ROOT_DIR.rglob("*.md"):
        if any(part in EXCLUDE_DIRS for part in p.parts):
            continue
        md_files.append(p)
    return md_files

def extract_urls(file_path):
    try:
        with open(file_path, encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception:
        return []

    found = URL_REGEX.findall(content)
    clean = []
    for u in found:
        u = u.rstrip(".,;:`)'\"")
        # Bỏ qua các URL mẫu / template placeholder
        if "..." in u or "xxxx" in u or "yyyy" in u or "<" in u or ">" in u:
            continue
        clean.append(u)
    return clean

def check_url(url):
    """Kiểm tra URL trả về tuple: (url, is_ok, status_code, message)"""
    if "127.0.0.1" in url or "localhost" in url:
        return (url, True, 200, "Localhost (Bỏ qua)")

    # YouTube check qua oEmbed API chính thức
    if "youtube.com/watch" in url or "youtu.be/" in url:
        oembed = f"https://www.youtube.com/oembed?url={urllib.parse.quote(url)}&format=json"
        req = urllib.request.Request(oembed, headers=HEADERS)
        try:
            with urllib.request.urlopen(req, timeout=8, context=ctx) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return (url, True, 200, f"YouTube OK: '{data.get('title')}'")
        except Exception as e:
            return (url, False, 404, f"YouTube: Video không tồn tại hoặc đã bị xóa ({e})")

    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=8, context=ctx) as resp:
            status = resp.status
            content_type = resp.headers.get("Content-Type", "")
            return (url, True, status, f"OK ({content_type.split(';')[0]})")
    except urllib.error.HTTPError as e:
        if e.code == 403:
            return (url, False, e.code, "HTTP 403 Forbidden (Chặn bot hoặc Paywall)")
        return (url, False, e.code, f"HTTP Error {e.code}")
    except urllib.error.URLError as e:
        return (url, False, 0, f"URL Error: {e.reason}")
    except Exception as e:
        return (url, False, 0, f"Error: {type(e).__name__} - {e}")

def main():
    print("🔍 [AUDIT] Đang quét toàn bộ file markdown trong repo...", flush=True)
    md_files = find_markdown_files()
    print(f"📄 Tìm thấy {len(md_files)} file Markdown.", flush=True)

    url_to_files = {}
    for mf in md_files:
        urls = extract_urls(mf)
        for u in urls:
            url_to_files.setdefault(u, []).append(mf.relative_to(ROOT_DIR))

    unique_urls = sorted(url_to_files.keys())
    print(f"🔗 Tìm thấy {len(unique_urls)} URL duy nhất. Bắt đầu kiểm tra song song (15 workers)...\n", flush=True)

    results = []
    broken = []

    with ThreadPoolExecutor(max_workers=15) as executor:
        futures = {executor.submit(check_url, u): u for u in unique_urls}
        count = 0
        for fut in as_completed(futures):
            count += 1
            url, is_ok, code, msg = fut.result()
            results.append((url, is_ok, code, msg))
            icon = "✅" if is_ok else "❌"
            print(f"[{count}/{len(unique_urls)}] {icon} {url} -> {msg}", flush=True)
            if not is_ok:
                broken.append((url, code, msg, url_to_files[url]))

    print("\n" + "="*85, flush=True)
    print(f"📊 BÁO CÁO TỔNG HỢP: {len(unique_urls)} URLs | Hoạt động: {len(unique_urls)-len(broken)} | Lỗi/Cần xử lý: {len(broken)}", flush=True)
    print("="*85, flush=True)

    for u, _code, msg, files in broken:
        print(f"\n❌ URL: {u}", flush=True)
        print(f"   Lý do: {msg}", flush=True)
        print("   File bị ảnh hưởng:", flush=True)
        for f in files:
            print(f"     - {f}", flush=True)

if __name__ == "__main__":
    main()
