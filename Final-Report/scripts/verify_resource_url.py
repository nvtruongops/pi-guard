#!/usr/bin/env python3
"""
scripts/verify_resource_url.py - Trình kiểm tra & tìm kiếm tài liệu mở (Open-Access PDF Validator)
Hỗ trợ:
  1. Kiểm tra tính khả dụng của bất kỳ URL nào (HTTP Status, Content-Type).
  2. Xác minh link YouTube có thực sự tồn tại và phát được không (qua oEmbed API).
  3. Tra cứu DOI để tự động tìm kiếm link PDF bản mở (Open-Access) qua Semantic Scholar & OpenAlex.
  4. Quét và kiểm toán toàn bộ link trong một file Markdown.

Cách sử dụng:
  python scripts/verify_resource_url.py --url "https://www.youtube.com/watch?v=ATK6fm3cYfI"
  python scripts/verify_resource_url.py --doi "10.1145/3658644.3670388"
  python scripts/verify_resource_url.py --file "workspaces/truongnv/docs/thesis/Review1_Problem_Definition_and_Threat_Model.md"
"""

import argparse
import json
import re
import ssl
import sys
import urllib.parse
import urllib.request
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Tạo SSL context an toàn với fallback nếu Windows thiếu local cert
try:
    import certifi
    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except Exception:
    SSL_CONTEXT = ssl.create_default_context()
    SSL_CONTEXT.check_hostname = False
    SSL_CONTEXT.verify_mode = ssl.CERT_NONE

def check_url(url: str, timeout: int = 8) -> dict:
    """Kiểm tra một URL, trả về thông tin trạng thái, tiêu đề và loại tài nguyên."""
    res = {
        "url": url,
        "is_valid": False,
        "status": None,
        "content_type": None,
        "title": None,
        "note": "",
        "is_pdf": False
    }

    # Bỏ qua localhost
    if "localhost" in url or "127.0.0.1" in url:
        res["is_valid"] = True
        res["status"] = 200
        res["note"] = "Localhost URL (bỏ qua)"
        return res

    # 1. Kiểm tra YouTube qua oEmbed
    if "youtube.com/watch" in url or "youtu.be/" in url:
        oembed_url = f"https://www.youtube.com/oembed?url={urllib.parse.quote(url)}&format=json"
        req = urllib.request.Request(oembed_url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(req, timeout=timeout, context=SSL_CONTEXT) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                res["is_valid"] = True
                res["status"] = 200
                res["content_type"] = "video/youtube"
                res["title"] = data.get("title")
                res["note"] = f"Video hợp lệ: '{data.get('title')}' bởi {data.get('author_name')}"
                return res
        except Exception as e:
            res["is_valid"] = False
            res["note"] = f"Video YouTube không tồn tại hoặc đã bị ẩn/xóa ({e})"
            return res

    # 2. Kiểm tra các URL thông thường
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=SSL_CONTEXT) as resp:
            res["status"] = resp.status
            content_type = resp.headers.get("Content-Type", "").lower()
            res["content_type"] = content_type
            res["is_pdf"] = "application/pdf" in content_type or url.endswith(".pdf")
            res["is_valid"] = True
            res["note"] = "URL hoạt động bình thường"
            return res
    except urllib.error.HTTPError as e:
        res["status"] = e.code
        if e.code == 403:
            res["note"] = "HTTP 403 Forbidden (Có thể do Cloudflare chặn bot hoặc tường phí Paywall)"
        elif e.code == 404:
            res["note"] = "HTTP 404 Not Found (URL không tồn tại / chết)"
        elif e.code == 401:
            res["note"] = "HTTP 401 Unauthorized (Cần đăng nhập hoặc URL sai ký tự)"
        else:
            res["note"] = f"Lỗi HTTP {e.code}: {e.reason}"
        return res
    except Exception as e:
        res["note"] = f"Lỗi kết nối: {e}"
        return res

def find_open_access(doi: str) -> dict:
    """Tra cứu DOI để tìm kiếm liên kết tải PDF mở miễn phí (Open-Access)."""
    clean_doi = doi.replace("https://doi.org/", "").replace("http://dx.doi.org/", "").strip()
    result = {
        "doi": clean_doi,
        "title": None,
        "is_oa": False,
        "oa_pdf_url": None,
        "oa_landing_url": None,
        "source": None
    }

    # 1. Thử qua OpenAlex API
    openalex_api = f"https://api.openalex.org/works/https://doi.org/{clean_doi}"
    try:
        req = urllib.request.Request(openalex_api, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=10, context=SSL_CONTEXT) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            result["title"] = data.get("title")
            oa = data.get("open_access", {})
            result["is_oa"] = oa.get("is_oa", False)
            result["oa_landing_url"] = oa.get("oa_url")

            # Tìm link PDF trong locations
            for loc in data.get("locations", []):
                pdf_url = loc.get("pdf_url")
                if pdf_url:
                    result["oa_pdf_url"] = pdf_url
                    result["source"] = "OpenAlex"
                    break
    except Exception:
        pass

    # 2. Thử qua Semantic Scholar API nếu OpenAlex chưa có PDF
    if not result["oa_pdf_url"]:
        s2_api = f"https://api.semanticscholar.org/graph/v1/paper/{clean_doi}?fields=title,url,openAccessPdf"
        try:
            req = urllib.request.Request(s2_api, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=10, context=SSL_CONTEXT) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                if not result["title"]:
                    result["title"] = data.get("title")
                oa_data = data.get("openAccessPdf")
                if oa_data and oa_data.get("url"):
                    result["oa_pdf_url"] = oa_data.get("url")
                    result["is_oa"] = True
                    result["source"] = "Semantic Scholar"
                if not result["oa_landing_url"] and data.get("url"):
                    result["oa_landing_url"] = data.get("url")
        except Exception:
            pass

    return result

def audit_markdown_file(file_path: Path) -> list:
    """Quét và kiểm tra toàn bộ liên kết trong một file Markdown bằng đa luồng."""
    from concurrent.futures import ThreadPoolExecutor

    if not file_path.exists():
        print(f"❌ File không tồn tại: {file_path}")
        return []

    content = file_path.read_text(encoding="utf-8", errors="ignore")
    # Loại bỏ code block và inline code để không quét các URL template / ví dụ kỹ thuật
    content_no_code = re.sub(r'```[\s\S]*?```', '', content)
    content_no_code = re.sub(r'`[^`]*`', '', content_no_code)

    # Lấy tất cả URL trong markdown ngoài code block
    urls = re.findall(r'\[(?:[^\]]+)\]\((https?://[^\s\)]+)\)', content_no_code)
    bare_urls = re.findall(r'(?<!\()(https?://[a-zA-Z0-9\.\-\_\/\?\=\&\%\#]+)', content_no_code)
    all_raw = list(set(urls + bare_urls))
    clean_urls = []
    for u in all_raw:
        u = u.rstrip(".,;:`)'\"")
        # Bỏ qua các URL mẫu / template placeholder
        if any(x in u for x in ["...", "xxxx", "yyyy", "{", "}", "<", ">"]):
            continue
        clean_urls.append(u)
    all_urls = sorted(clean_urls)

    print(f"\n📄 Đang kiểm tra file: {file_path}")
    print(f"🔗 Tìm thấy {len(all_urls)} URLs. Bắt đầu kiểm tra song song...")

    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_map = {executor.submit(check_url, u): u for u in all_urls}
        for future in future_map:
            chk = future.result()
            results.append(chk)
            status_icon = "✅" if chk["is_valid"] else "❌"
            note_str = f" ({chk['note']})" if chk["note"] else ""
            print(f"  {status_icon} {chk['url']}{note_str}")

    return results

def main():
    parser = argparse.ArgumentParser(description="PI-Guard Resource & Literature Validator")
    parser.add_argument("--url", help="Kiểm tra một URL cụ thể")
    parser.add_argument("--doi", help="Tra cứu DOI để tìm kiếm Open-Access PDF")
    parser.add_argument("--file", help="Quét và kiểm tra toàn bộ liên kết trong một file Markdown")
    args = parser.parse_args()

    if args.url:
        print(f"🔍 Kiểm tra URL: {args.url}")
        res = check_url(args.url)
        print(f"  Trạng thái: {'✅ HỢP LỆ' if res['is_valid'] else '❌ KHÔNG HỢP LỆ'}")
        print(f"  HTTP Code : {res['status']}")
        print(f"  Loại nội dung: {res['content_type']}")
        print(f"  Ghi chú   : {res['note']}")
        if res["title"]:
            print(f"  Tiêu đề   : {res['title']}")
        sys.exit(0 if res["is_valid"] else 1)

    if args.doi:
        print(f"🔍 Tra cứu DOI: {args.doi}")
        oa = find_open_access(args.doi)
        print(f"  Tiêu đề bài báo: {oa['title']}")
        print(f"  Trạng thái Open Access: {'✅ CÓ (OPEN ACCESS)' if oa['is_oa'] else '⚠️ PAYWALLED / CLOSED'}")
        if oa["oa_pdf_url"]:
            print(f"  🔗 Link tải PDF trực tiếp: {oa['oa_pdf_url']} (Nguồn: {oa['source']})")
        if oa["oa_landing_url"]:
            print(f"  🌐 Trang đọc mở: {oa['oa_landing_url']}")
        if not oa["is_oa"]:
            print("  ⚠️ Gợi ý: Tìm kiếm bản preprint trên arXiv hoặc tra cứu giáo trình/báo cáo kỹ thuật của tác giả.")
        sys.exit(0)

    if args.file:
        res = audit_markdown_file(Path(args.file))
        has_invalid = any(not r["is_valid"] for r in res)
        sys.exit(1 if has_invalid else 0)

    parser.print_help()

if __name__ == "__main__":
    main()
