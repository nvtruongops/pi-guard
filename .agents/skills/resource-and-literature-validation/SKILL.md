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

Mọi AI Agent và thành viên nhóm khi trích dẫn tài liệu hoặc bổ sung đường dẫn vào repo phải tuân thủ 5 nguyên tắc:

### Quy Tắc 0: LOCAL REFERENCES FIRST (Truy Lục Tài Liệu Cục Bộ Trước Tiên)
- Trước khi tìm kiếm tài liệu mới qua MCP (`arxiv`, `openalex`, `semanticscholar`, `scholar-feed`) hoặc trên mạng, **BẮT BUỘC** phải tra cứu [`Final-Report/References/REFERENCES_LOG.md`](file:///d:/Work/Do-an/Final-Report/References/REFERENCES_LOG.md).
- Nếu vấn đề cần dẫn chứng đã được bảo chứng bởi một trong **18 bài báo cốt lõi đã lưu trữ sẵn trong `References/`**, bắt buộc phải tái sử dụng bài báo đó kèm neo trích dẫn `[[N]](#refN)`.
- Tuyệt đối không thêm bài báo mới cho các chủ đề đã có sẵn tài liệu kiểm chứng để tránh dàn trải trích dẫn (Zero Citation Bloat).

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

### A. Công Cụ Kiểm Tra Nhanh & Tra Cứu Open Access: `Final-Report/scripts/verify_resource_url.py`

#### 1. Kiểm tra tính tồn tại của một URL bất kỳ (Web, GitHub, YouTube, Docs):
```bash
python Final-Report/scripts/verify_resource_url.py --url "https://www.youtube.com/watch?v=ATK6fm3cYfI"
```

#### 2. Tra cứu DOI để tự động trích xuất liên kết tải PDF mở miễn phí:
```bash
python Final-Report/scripts/verify_resource_url.py --doi "10.1145/3658644.3670388"
```

#### 3. Quét và kiểm toán toàn bộ link trong một file Markdown trước khi commit:
```bash
python Final-Report/scripts/verify_resource_url.py --file "workspaces/truongnv/docs/model_study/01_tfidf_syntactic_baseline/resources_and_videos.md"
```

---

### B. Công Cụ Kiểm Toán Toàn Diện Repository: `Final-Report/scripts/audit_urls.py`

Kiểm tra toàn bộ hơn 60+ file Markdown trong dự án bằng cơ chế đa luồng song song (`ThreadPoolExecutor`):
```bash
python -u Final-Report/scripts/audit_urls.py
```
- Tự động phân loại URL hoạt động và URL lỗi/paywall.
- Đưa ra danh sách chi tiết các file bị ảnh hưởng để xử lý kịp thời.

---

## 🌐 3. Quy Trình 5 Bước Kiểm Định Học Thuật Nghiêm Ngặt (Academic Paper Rigor Gate)

Mỗi khi agent hoặc thành viên nhóm muốn trích dẫn, bổ sung một bài báo khoa học mới hoặc cập nhật tài liệu tham khảo:

```
[ BƯỚC 1: XÁC THỰC SIÊU DỮ LIỆU VÀ NGUỒN GỐC THEO THỨ TỰ ƯU TIÊN (TIER 0 - BIBLIOGRAPHIC PROVENANCE) ]
  ├── Thứ tự nguồn uy tín: Publisher/proceedings page -> official conference/journal metadata -> DOI/Crossref -> arXiv/DBLP/OpenReview (khi có).
  ├── Lấy chính xác tiêu đề, danh sách tác giả, venue, volume, issue, year, pages, DOI, publication status.
  └── LOẠI BỎ TRIỆT ĐỂ khẩu hiệu/slogan trình diễn (ví dụ: "Ignore This Title..." chỉ là slogan, tiêu đề chuẩn là "Ignore Previous Prompt...").
                         │
                         ▼
[ BƯỚC 2: XÁC THỰC NƠI CÔNG BỐ, SỐ TẬP & NIÊN GIÁM (VOLUME & YEAR) ]
  ├── Tra cứu chính xác số tập kỷ yếu và năm diễn ra hội nghị (ví dụ: NeurIPS 35 = 2022, NeurIPS 36 = 2023, NeurIPS 37 = 2024).
  └── Tuyệt đối không nhầm lẫn niên giám hội nghị với năm nộp bản thảo hoặc năm cập nhật preprint.
                         │
                         ▼
[ BƯỚC 3: KIỂM TOÁN VĂN BẢN THEO MÔ HÌNH PHÂN ĐỊNH 4 TẦNG (FOUR-TIER ATTRIBUTION & PROVENANCE AUDIT) ]
  ├── Tầng 0: Nguồn gốc Thư mục (Bibliographic Provenance: Title, Authors, Venue, Volume, Year, Pages, DOI, Primary Source).
  ├── Tầng 1: Đóng góp gốc của tác giả (Original Author Findings) ── trung thực với những gì paper thực sự chứng minh.
  ├── Tầng 2: Tiếp thu/cảm hứng của PI-Guard (Design Choice & Adaptation) ── giải thích rõ ràng việc kế thừa.
  ├── Tầng 3: Mục tiêu KPI & Giả thuyết thực nghiệm của PI-Guard (Target KPI & Hypotheses) ── không được trình bày KPI, benchmark result, latency, FPR, F1 của PI-Guard như kết quả thực nghiệm của tài liệu tham chiếu.
  ├── CẤM GÁN NGUỒN CÔNG THỨC: Không gán công thức của PI-Guard ($X = S || U$) cho bài báo khảo sát.
  ├── CHÍNH XÁC SỐ LIỆU TẬP DỮ LIỆU: Phân biệt rõ quy mô tổng thể (15,140 prompts) và số mẫu tấn công thực tế (1,405 jailbreak prompts, ~9.29% / làm tròn 9.3%).
  └── TUÂN THỦ KHIÊM TỐN HỌC THUẬT: Cấm các absolute claims ("không lo ngại bất kỳ câu hỏi phản biện nào", "100% PASS cho học thuật").
                         │
                         ▼
[ BƯỚC 4: KIỂM ĐỊNH PHẠM VI & RANH GIỚI HỘP ĐEN (SCOPE & BLACK-BOX INVARIANT) ]
  ├── Kiểm tra tính tương thích: Phải hoạt động ở mức prompt text ngoài cổng API (External Guardrail Proxy).
  └── Nếu phương pháp đòi hỏi truy cập trọng số/nội tại (như RAP-ID): Đánh dấu OUT-OF-SCOPE và ghi rõ lý do chính xác:
      "do phương pháp khai thác internal model states và attention dynamics trong forward pass, khác với kiến trúc external black-box guardrail của PI-Guard".
                         │
                         ▼
[ BƯỚC 5: LƯU TRỮ CỤC BỘ OPEN-ACCESS PDF & CẬP NHẬT BIBTEX CHUẨN ]
  ├── Tải Open-Access PDF vào `Final-Report/References/<filename>.pdf`.
  ├── Lập chỉ mục siêu dữ liệu, đóng góp gốc và mã ánh xạ trong `Final-Report/References/REFERENCES_LOG.md`.
  └── Chạy `python Final-Report/scripts/verify_resource_url.py --file <file.md>` để xác thực liên kết trước khi commit.
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

---

## 🔬 5. Academic Grounding & Citation Anchor Specification

### A. Tiêu Chuẩn Viết Tài Liệu Nghiên Cứu & Chuyên Đề (100% Grounded)
Mọi tài liệu kỹ thuật, chuyên đề nghiên cứu (`docs/research/`, `docs/attack_study/`, `docs/model_study/`, `docs/thesis/`) bắt buộc phải tuân thủ:
1. **Khẳng định kỹ thuật phải có nguồn bảo chứng**: Trích dẫn rõ tác giả, năm và mã trích dẫn nội trang dạng `[[N]](#refN)`. Không đưa ra các tuyên bố chung chung hoặc suy đoán thiếu tài liệu kiểm chứng.
2. **Khối References chuẩn mực ở cuối mỗi trang**:
   Mọi trang có sử dụng trích dẫn `[[N]](#refN)` bắt buộc phải có mục References chứa neo HTML `<a id="refN"></a>` tương ứng trên chính trang đó:
   ```markdown
   ---
   ## References (Tài Liệu Tham Khảo Học Thuật Chuẩn IEEE)

   <a id="ref1"></a>**[1]** W. X. Zhao et al., "A Survey of Large Language Models," *arXiv preprint arXiv:2303.18223*, 2023. Link: [https://arxiv.org/abs/2303.18223](https://arxiv.org/abs/2303.18223).
   <a id="ref2"></a>**[2]** L. Ouyang et al., "Training language models to follow instructions with human feedback," in *NeurIPS 2022*. Link: [https://arxiv.org/abs/2203.02155](https://arxiv.org/abs/2203.02155).
   ```
3. **Quy tắc giải quyết cảnh báo MkDocs**: Neo `<a id="refN"></a>` phải nằm trên cùng một file markdown với liên kết `[[N]](#refN)` để loại bỏ hoàn toàn cảnh báo `contains a link '#refN', but there is no such anchor on this page` khi build.

### B. Bảng Quy Chuẩn Định Dạng Liên Kết & Xử Lý Paywalled DOI
| Loại Tài Nguyên | Cách Định Dạng Chuẩn Trong Markdown | Lý Do Kỹ Thuật |
| :--- | :--- | :--- |
| **arXiv Preprint / OpenAlex PDF** | `[https://arxiv.org/abs/xxxx.yyyyy](https://arxiv.org/abs/xxxx.yyyyy)` | Link mở trực tiếp, crawler HTTP 200/302 luôn hợp lệ |
| **DOI Tường Phí (ACM, Emerald, IEEE)** | Ghi DOI dạng inline code: `(DOI: 10.xxxx/yyyy)` kèm link Open-Access PDF bên cạnh | Tránh bị Cloudflare WAF chặn trả về HTTP 403 khi kiểm tra tự động |
| **Video Bài Giảng (YouTube)** | `[https://www.youtube.com/watch?v=...](https://www.youtube.com/watch?v=...)` | Đã qua kiểm định `youtube.com/oembed` (video công khai, tồn tại) |
| **Tiêu Chuẩn / Báo Cáo Tổ Chức** | `[https://csrc.nist.gov/...](https://csrc.nist.gov/...)` hoặc `[https://owasp.org/...](https://owasp.org/...)` | Nguồn uy tín quốc tế, giao thức HTTPS mở không chặn bot |

### C. Lệnh Kiểm Toán Đa Luồng Toàn Workspace Trước Khi Commit
```bash
python -c "
import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from scripts.verify_resource_url import audit_markdown_file

base_dir = Path('workspaces/truongnv')
all_files = list(base_dir.rglob('*.md'))
failed = []
for f in sorted(all_files):
    for r in audit_markdown_file(f):
        if not r['is_valid']:
            failed.append((str(f), r['url'], r['note']))
if failed:
    print(f'❌ Phát hiện {len(failed)} link lỗi!')
    sys.exit(1)
else:
    print('🎉 100% URLs đạt chuẩn Zero Dead Links!')
"
```

