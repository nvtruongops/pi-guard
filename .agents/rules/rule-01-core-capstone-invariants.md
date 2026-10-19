# 🛡️ Rule 01: Core Capstone Invariants & Literature Reuse Protocol

> **Quy định bất biến tối thượng về tài nguyên nhà trường, thẩm định tài liệu khoa học và phạm vi kiến trúc đồ án**  
> **Cơ chế áp dụng**: Bắt buộc tuân thủ 100% trong mọi phiên làm việc, mã nguồn, báo cáo kỹ thuật và slide thuyết trình.

---

## 🚫 1. TÀI NGUYÊN BẤT BIẾN & BẢO MẬT NỘI BỘ NHÀ TRƯỜNG (STRICT READ-ONLY)

> [!CAUTION]
> **CÁC BẤT BIẾN TỐI THƯỢNG ĐỐI VỚI HỒ SƠ ĐẠI HỌC FPT**:
> 1. Tệp [`CAPSTONE PROJECT REGISTER.md`](file:///d:/Work/Do-an/CAPSTONE%20PROJECT%20REGISTER.md) là bản đăng ký đề tài chính thức đã ký duyệt bởi GVHD ThS. Trần Văn Ninh và Bộ môn An toàn Thông tin ĐH FPT.
> 2. Thư mục [`docs/fpt_capstone_guide/`](file:///d:/Work/Do-an/docs/fpt_capstone_guide/) chứa biểu mẫu, rubric chấm điểm và quy chế nội bộ của trường (được bảo vệ bởi `.gitignore`).
>
> **TUYỆT ĐỐI KHÔNG SỬA ĐỔI, GHI ĐÈ, XÓA, COMMIT HOẶC CÔNG KHAI CÁC FILE TRONG `docs/fpt_capstone_guide/` VÀ `CAPSTONE PROJECT REGISTER.md`.**
> - Không rò rỉ: Tuyệt đối không sao chép tài liệu nội bộ vào `Github-Page/` hoặc các thư mục công khai.
> - Tài liệu đối chiếu chính thức: Quy chế học tập và rubric chấm điểm được tổng hợp tại [`Final-Report/thesis/FPT_IAP491_Capstone_Guidelines_and_Rubrics_Summary.md`](file:///d:/Work/Do-an/Final-Report/thesis/FPT_IAP491_Capstone_Guidelines_and_Rubrics_Summary.md).
> - Lộ trình 15 tuần Fall 2026: Tuân thủ kế hoạch làm việc với GVHD, không phụ thuộc vào các mốc thời gian cũ trong tài liệu mẫu.

---

## 🔗 2. QUY CHUẨN XÁC MINH TÀI NGUYÊN & LINK OPEN-ACCESS PDF (ZERO DEAD LINKS)

1. **Zero Dead Links (100% URL Sống)**: Mọi liên kết URL (website, repo GitHub, paper, doc) trước khi đưa vào văn bản PHẢI được xác minh tồn tại thực tế (HTTP 200/302). Nghiêm cấm hoàn toàn URL suy đoán hoặc ảo giác.
2. **Xác Minh YouTube oEmbed**: Mọi video YouTube phải được kiểm tra qua `https://www.youtube.com/oembed?url=...&format=json` để đảm bảo video công khai, còn hoạt động.
3. **Mandatory Open-Access PDF**: Đối với mọi bài báo khoa học được trích dẫn, **tuyệt đối không chỉ đưa DOI bị tường phí (paywall)**. BẮT BUỘC phải đính kèm liên kết tải/đọc bản mở (Open-Access PDF) từ arXiv, OpenAlex, Semantic Scholar hoặc kho tài liệu mở của trường đại học tác giả.
4. **An Toàn Với DOI Bị Chặn Bot**: Với các nhà xuất bản chặn bot (ACM, IEEE, Emerald), định dạng DOI dạng inline code (e.g. `DOI: 10.1145/xxxx`) và kèm theo link Open-Access PDF đã xác minh.

---

## 📖 3. TÁI SỬ DỤNG Y VĂN CỤC BỘ TRƯỚC TIÊN (LOCAL REFERENCES FIRST)

1. **Tra Cứu `REFERENCES_LOG.md` Trước Tiên**: Trước khi tìm kiếm bài báo bên ngoài hoặc gọi các công cụ MCP (`arxiv`, `openalex`, `scholar-feed`), BẮT BUỘC tra cứu tệp [`Final-Report/References/REFERENCES_LOG.md`](file:///d:/Work/Do-an/Final-Report/References/REFERENCES_LOG.md).
2. **Ưu Tiên Tuyệt Đối 18 Bài Báo Cốt Lõi**: Repository đã lưu trữ và phê duyệt đầy đủ các bài báo cốt lõi bao quát mọi khía cạnh: Direct/Indirect Prompt Injection, DAN Jailbreak, Dual TF-IDF N-Grams, DeBERTa-v3, Đánh đổi FPR < 1.5%, Kiểm thử Đối kháng, và Nguyên lý Saltzer & Schroeder 1975. Tái sử dụng ngay mã neo `[[N]](#refN)` đã cấp.
3. **Tiêu Chuẩn Nhập Bài Mới**: Chỉ tìm kiếm bài mới khi xuất hiện kỹ thuật tấn công/phòng thủ mới thực sự chưa có trong danh mục. Mọi bài mới phải tải PDF về `Final-Report/References/<filename>.pdf` và lập chỉ mục đầy đủ trong `REFERENCES_LOG.md`.

---

## 🔬 4. TƯƠNG THÍCH KIẾN TRÚC EXTERNAL GUARDRAIL PROXY (ZERO CITATION BLOAT)

1. **Ranh Giới Kiến Trúc Cổng Bảo Vệ Độc Lập**: Mọi công trình khoa học dùng làm luận cứ thiết kế PHẢI tương thích với mô hình **External Guardrail Proxy** (phân loại prompt mức văn bản trước khi gọi LLM đích, không can thiệp trọng số nội bộ và không cần truy cập KV-cache của LLM).
2. **Loại Bỏ Hoàn Toàn Bài Báo Ngoài Phạm Vi**: Loại bỏ các bài báo về tấn công phần cứng (Rowhammer), backdoor mô hình trong pre-training, hoặc data poisoning ngoài tầng ứng dụng.

---

## ⚖️ 5. QUẢN TRỊ NỘI BỘ VÀ CHỐNG PHÂN MẢNH MÔ ĐUN (ZERO SILOING)

1. **Cấm Bảng Phân Công Chia Cắt Mô Đun (Anti-Siloing)**: Tuyệt đối **KHÔNG** tạo bảng chia rẽ module (ví dụ: gán thành viên A chỉ làm Baseline, B chỉ làm Transformer, C chỉ làm Web/API) trong hồ sơ kỹ thuật nộp cho GVHD hoặc Hội đồng.
2. **Chuẩn Hóa Quy Trình Thực Nghiệm Tái Lập (Reproducibility Pipeline)**: Trình bày quy trình thực nghiệm B1–B5 khách quan để bất kỳ ai cũng có thể chạy lại độc lập và cho ra kết quả trùng khớp 100%.
