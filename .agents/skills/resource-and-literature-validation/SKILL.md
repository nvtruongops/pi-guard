---
name: resource-and-literature-validation
description: >-
  Quy trình và công cụ tự động hóa để kiểm tra, xác thực tính khả dụng của tài liệu khoa học, bài báo,
  video YouTube (oEmbed) và liên kết web; tự động tìm kiếm và tải PDF bản mở (Open-Access PDF) từ DOI
  qua OpenAlex/Semantic Scholar, loại bỏ triệt để link chết (Zero Dead Links) và chặn tường phí (Paywall Prevention).
---

# 📚 Resource, URL & Literature Validation Skill (Zero Dead Links & Open-Access PDF Protocol)

Skill này cung cấp các tiêu chuẩn nghiêm ngặt, quy trình tra cứu tài liệu khoa học mở và bộ công cụ tự động hóa để **xác thực tính khả dụng của mọi tài nguyên, liên kết (URL), video bài giảng và bài báo học thuật** trong toàn bộ repository đồ án **PI-Guard**.

---

## 🎯 1. Các Nguyên Tắc Kiểm Định Cốt Lõi (Invariants)

Mọi AI Agent và thành viên nhóm khi trích dẫn tài liệu hoặc bổ sung đường dẫn vào repo phải tuân thủ 4 nguyên tắc:

### Quy Tắc 1: ZERO DEAD LINKS (Không Link Chết / Không Hallucinate)
- Tuyệt đối **KHÔNG ĐƯỢC ĐƯA LINK SUY ĐOÁN** hoặc tự sinh vào tài liệu.
- Mọi URL (website, GitHub, bài báo, tài liệu kỹ thuật) **PHẢI** được kiểm tra thực tế bằng HTTP GET/HEAD và trả về mã trạng thái **`HTTP 200`** hoặc `302/301` hợp lệ.

### Quy Tắc 2: YOUTUBE OEMBED VERIFICATION (Video Khả Dụng Thực Tế)
- AI thường có xu hướng "nhớ" tên bài giảng nhưng hallucinate chuỗi Video ID (ví dụ: `kR5t6H1T4H4`).
- Mọi link YouTube **BẮT BUỘC** phải được kiểm tra qua endpoint oEmbed chính thức:
  `https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={VIDEO_ID}&format=json`
- Chỉ chấp nhận khi API trả về mã `200 OK` kèm tiêu đề video và tên kênh (`author_name`), không bị lỗi 404, riêng tư hoặc gỡ bỏ.

### Quy Tắc 3: MANDATORY OPEN-ACCESS PDF (Chống Tường Phí / Paywall Invariant)
- Đối với các bài báo khoa học, tuyệt đối **KHÔNG ĐƯỢC CHỈ CUNG CẤP DOI BỊ PAYWALL** (khiến người đọc bị chặn bởi thông báo *"You do not currently have access to this content"* từ IEEE, ACM, Springer, Elsevier hay Emerald).
- Bắt buộc phải tìm và cung cấp kèm theo ít nhất **một liên kết tải/đọc toàn văn PDF bản mở (Open-Access)** từ arXiv, OpenAlex, Semantic Scholar hoặc kho tài liệu mở của trường đại học tác giả.

### Quy Tắc 4: DUAL-LINKING STANDARD (Chuẩn Trích Dẫn Kép)
Mọi bài báo khoa học được trích dẫn trong tài liệu, nghiên cứu mô hình hoặc luận văn phải trình bày theo định dạng chuẩn:
```markdown
- **Tên bài báo**: *"Tiêu đề bài báo"*
- **Tác giả & Năm**: Tác giả et al. (Năm)
- **DOI chính thức**: [10.xxxx/yyyy](https://doi.org/10.xxxx/yyyy) *(Trang nhà xuất bản — Yêu cầu tài khoản thư viện)*
- **Bản đọc mở toàn văn (Open-Access PDF)**: [Tải/Đọc PDF trực tiếp](https://arxiv.org/pdf/xxxx.yyyyy) *(Nguồn: arXiv / OpenAlex / Semantic Scholar)*
```

---

## 🛠️ 2. Bộ Công Cụ Tự Động Hóa Trong Repository

Repository đã tích hợp sẵn 2 công cụ Python chuyên dụng để hỗ trợ việc kiểm tra:

### A. Công Cụ Kiểm Tra Nhanh & Tra Cứu Open Access: `scripts/verify_resource_url.py`

#### 1. Kiểm tra tính tồn tại của một URL bất kỳ (Web, GitHub, YouTube, Docs):
```bash
python scripts/verify_resource_url.py --url "https://www.youtube.com/watch?v=ATK6fm3cYfI"
# Kết quả:
# 🔍 Kiểm tra URL: https://www.youtube.com/watch?v=ATK6fm3cYfI
#   Trạng thái: ✅ HỢP LỆ
#   HTTP Code : 200
#   Loại nội dung: video/youtube
#   Ghi chú   : Video hợp lệ: 'Text Representation Using TF-IDF: NLP Tutorial For Beginners - S2 E6' bởi codebasics
```

#### 2. Tra cứu DOI để tự động trích xuất liên kết tải PDF mở miễn phí:
```bash
python scripts/verify_resource_url.py --doi "10.1145/3658644.3670388"
# Kết quả:
# 🔍 Tra cứu DOI: 10.1145/3658644.3670388
#   Tiêu đề bài báo: "Do Anything Now": Characterizing and Evaluating In-The-Wild Jailbreak Prompts on Large Language Models
#   Trạng thái Open Access: ✅ CÓ (OPEN ACCESS)
#   🔗 Link tải PDF trực tiếp: https://dl.acm.org/doi/pdf/10.1145/3658644.3670388 (Nguồn: OpenAlex)
```

#### 3. Quét và kiểm toán toàn bộ link trong một file Markdown trước khi commit:
```bash
python scripts/verify_resource_url.py --file "workspaces/truongnv/docs/model_study/01_tfidf_syntactic_baseline/resources_and_videos.md"
```

---

### B. Công Cụ Kiểm Toán Toàn Diện Repository: `scripts/audit_urls.py`

Kiểm tra toàn bộ hơn 60+ file Markdown trong dự án bằng cơ chế đa luồng song song (`ThreadPoolExecutor`):
```bash
python -u scripts/audit_urls.py
```
- Tự động phân loại URL hoạt động và URL lỗi/paywall.
- Đưa ra danh sách chi tiết các file bị ảnh hưởng để xử lý kịp thời.

---

## 🌐 3. Quy Trình 4 Bước Khi Tìm Kiếm & Đưa Tài Liệu Mới Vào Repo

Mỗi khi agent hoặc thành viên nhóm muốn thêm một bài báo hoặc video hướng dẫn vào tài liệu:

```
[ BƯỚC 1: Thu thập DOI / Tên bài báo / Link Video ]
                       │
                       ▼
[ BƯỚC 2: Chạy verify_resource_url.py ]
  - Nếu là Video  ──> Kiểm tra oEmbed (xác nhận mã 200, tiêu đề thật)
  - Nếu là DOI    ──> Truy vấn OpenAlex/Semantic Scholar tìm Open-Access PDF
                       │
                       ▼
[ BƯỚC 3: Xử lý Paywall (Nếu bài báo bị khóa) ]
  - Dùng MCP tool `arxiv` (search_papers) tìm preprint tương ứng
  - Tra cứu Google Scholar / ResearchGate / Kho lưu trữ Đại học của tác giả
  - Đối với lý thuyết kinh điển (1970-1990), bổ sung giáo trình chuẩn (Stanford IR book)
                       │
                       ▼
[ BƯỚC 4: Ghi vào tài liệu theo định dạng Dual-Linking & Re-test ]
  - Chạy `python scripts/verify_resource_url.py --file <file.md>`
  - Đảm bảo 100% link hoạt động trước khi commit
```

---

## 📖 4. Kho Tài Nguyên Học Thuật Mở Khuyên Dùng (Open-Access Repositories)

| Nguồn Học Thuật | Lĩnh Vực / Đặc Điểm | Link Truy Cập Mở |
| :--- | :--- | :--- |
| **arXiv (cs.CR, cs.CL, cs.AI)** | Cổng preprint hàng đầu thế giới về LLM Security & NLP | [https://arxiv.org](https://arxiv.org) |
| **ACL Anthology** | Toàn bộ kỷ yếu hội nghị NLP đỉnh cao (ACL, EMNLP, NAACL) | [https://aclanthology.org](https://aclanthology.org) |
| **OpenAlex API** | Cơ sở dữ liệu học thuật mở toàn cầu, tự động trích xuất OA PDF | `https://api.openalex.org/works/https://doi.org/{DOI}` |
| **Semantic Scholar API** | Trích xuất đồ thị trích dẫn và link PDF toàn văn | `https://api.semanticscholar.org/graph/v1/paper/{DOI}` |
| **NIST Computer Security Resource Center** | Tiêu chuẩn an ninh AI & phân loại tấn công đối kháng | [https://csrc.nist.gov](https://csrc.nist.gov) |
| **Cambridge Computer Lab Technical Reports** | Báo cáo kỹ thuật gốc của các nhà khoa học máy tính Cambridge | [https://www.cl.cam.ac.uk/techreports/](https://www.cl.cam.ac.uk/techreports/) |
| **Stanford NLP Book (Manning et al.)** | Giáo trình kinh điển về Xử lý ngôn ngữ tự nhiên & IR | [https://nlp.stanford.edu/IR-book/](https://nlp.stanford.edu/IR-book/) |
