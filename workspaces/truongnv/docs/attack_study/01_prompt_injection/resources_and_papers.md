# TÀI LIỆU HỌC TẬP, BÀI BÁO KHOA HỌC & VIDEO: PROMPT INJECTION

Tài liệu này tổng hợp toàn bộ các công trình nghiên cứu khoa học mở (Open-Access Papers) và tuyển tập video bài giảng trực quan đã được **kiểm định 100% khả dụng** về chuyên đề tấn công **Prompt Injection**.

---

## 📄 1. CÁC BÀI BÁO KHOA HỌC TOÀN VĂN MỞ (OPEN-ACCESS PAPERS >= 2022)

1. **Perez & Ribeiro (NeurIPS 2022) — Bài Báo Đặt Nền Móng Cho Prompt Injection**:
   - **Tên bài báo**: *"Ignore This Title and Hack This Paper: Towards Automated Adversarial Prompting"*.
   - **Hội nghị**: *Advances in Neural Information Processing Systems (NeurIPS 2022)*.
   - **DOI chính thức**: [10.48550/arXiv.2206.05600](https://doi.org/10.48550/arXiv.2206.05600)
   - **Bản đọc mở toàn văn (Open-Access PDF)**: [https://arxiv.org/pdf/2206.05600](https://arxiv.org/pdf/2206.05600)
   - **Trang tóm tắt học thuật**: [arXiv:2206.05600](https://arxiv.org/abs/2206.05600)
   - **Ý nghĩa**: Công trình khoa học đầu tiên định nghĩa chính thức khái niệm Prompt Injection, phân tích hai kỹ thuật cốt lõi: *Goal Hijacking* và *Prompt Leaking*.

2. **Greshake et al. (ACM AISEC 2023) — Đột Phá Về Tấn Công Gián Tiếp (Indirect Injection)**:
   - **Tên bài báo**: *"Not what you've signed up for: Compromising Real-World LLM Applications with Indirect Prompt Injection"*.
   - **Hội nghị**: *Proceedings of the 16th ACM Workshop on Artificial Intelligence and Security (AISEC 2023)*.
   - **DOI chính thức**: [10.48550/arXiv.2302.12173](https://doi.org/10.48550/arXiv.2302.12173)
   - **Bản đọc mở toàn văn (Open-Access PDF)**: [https://arxiv.org/pdf/2302.12173](https://arxiv.org/pdf/2302.12173)
   - **Trang tóm tắt học thuật**: [arXiv:2302.12173](https://arxiv.org/abs/2302.12173)
   - **Ý nghĩa**: Nghiên cứu chỉ ra nguy cơ chí mạng khi LLM kết nối với dữ liệu bên ngoài (RAG, web browsing, email), chứng minh kẻ tấn công có thể chiếm quyền điều khiển LLM từ xa mà không cần chat trực tiếp.

3. **Yi et al. (ACM KDD 2025) — Bộ Đối Chuẩn Đánh Giá Indirect Injection (BIPIA Benchmark)**:
   - **Tên bài báo**: *"Benchmarking and Defending Against Indirect Prompt Injection Attacks on Large Language Models"*.
   - **Xuất bản**: *ACM SIGKDD Conference on Knowledge Discovery and Data Mining (KDD 2025)*.
   - **DOI chính thức**: [10.48550/arXiv.2312.14197](https://doi.org/10.48550/arXiv.2312.14197)
   - **Bản đọc mở toàn văn (Open-Access PDF)**: [https://arxiv.org/pdf/2312.14197v1](https://arxiv.org/pdf/2312.14197v1)
   - **Trang tóm tắt học thuật**: [arXiv:2312.14197](https://arxiv.org/abs/2312.14197)
   - **Ý nghĩa**: Cung cấp bộ dữ liệu và framework đánh giá độ bền của các mô hình phòng thủ trước 5 tác vụ Indirect Prompt Injection (QA, Summarization, Email, Code, Table).

4. **OWASP Foundation (2025) — Tiêu Chuẩn Bảo Mật Công Nghiệp**:
   - **Tài liệu**: *OWASP Top 10 for Large Language Model Applications and Generative AI (LLM01:2025)*.
   - **Liên kết truy cập mở**: [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
   - **Ý nghĩa**: Hướng dẫn chính thức phân loại rủi ro, phân tích tác động và các biện pháp giảm thiểu Prompt Injection trong môi trường doanh nghiệp.

---

## 🎥 2. TUYỂN TẬP VIDEO BÀI GIẢNG TRỰC QUAN (ĐÃ XÁC MINH OEMBED 100%)

1. **LiveOverflow (Kênh Chuyên Gia Bảo Mật Hàng Đầu Thế Giới)**:
   - **Tiêu đề**: *Attacking LLM - Prompt Injection*
   - **Link video**: [https://www.youtube.com/watch?v=Sv5OLj2nVAQ](https://www.youtube.com/watch?v=Sv5OLj2nVAQ)
   - **Thời lượng**: ~15 phút.
   - **Điểm hay**: Phân tích trực quan dưới góc độ an ninh mạng truyền thống, giải thích tại sao Prompt Injection tương tự lỗ hổng SQL Injection nhưng khó vá hơn gấp bội do bản chất ngôn ngữ tự nhiên.

2. **LiveOverflow (Phần 2: Cơ Chế Phòng Thủ)**:
   - **Tiêu đề**: *Defending LLM - Prompt Injection*
   - **Link video**: [https://www.youtube.com/watch?v=VbNPZ1n6_vY](https://www.youtube.com/watch?v=VbNPZ1n6_vY)
   - **Thời lượng**: ~18 phút.
   - **Điểm hay**: Đánh giá các phương án phòng ngự (Sanitization, Delimiters, Separate LLM Judges) và lý do tại sao cần một bộ Guardrail chuyên dụng.

3. **IBM Technology**:
   - **Tiêu đề**: *What Is a Prompt Injection Attack?*
   - **Link video**: [https://www.youtube.com/watch?v=jrHRe9lSqqA](https://www.youtube.com/watch?v=jrHRe9lSqqA)
   - **Thời lượng**: ~8 phút.
   - **Điểm hay**: Trình bày bảng trắng (Lightboard) cực kỳ trực quan, dễ hiểu về sự khác biệt giữa Direct và Indirect Prompt Injection trong môi trường doanh nghiệp.

4. **ByteByteGo**:
   - **Tiêu đề**: *What is Prompt Injection?*
   - **Link video**: [https://www.youtube.com/watch?v=b1SPKtN05y8](https://www.youtube.com/watch?v=b1SPKtN05y8)
   - **Thời lượng**: ~7 phút.
   - **Điểm hay**: Phân tích sơ đồ kiến trúc hệ thống, dòng dữ liệu (Data Flow) và các điểm bị khai thác trong kiến trúc RAG.

5. **Computerphile**:
   - **Tiêu đề**: *Generative AI's Greatest Flaw*
   - **Link video**: [https://www.youtube.com/watch?v=rAEqP9VEhe8](https://www.youtube.com/watch?v=rAEqP9VEhe8)
   - **Thời lượng**: ~14 phút.
   - **Điểm hay**: GS. Mike Pound của Đại học Nottingham giải thích tường tận nguyên lý toán học và cấu trúc token khiến LLM không thể tự bảo vệ trước Prompt Injection.

6. **Mì AI (Kênh Công Nghệ AI Việt Nam)**:
   - **Tiêu đề**: *Tìm hiểu về Prompt Injection và sự nguy hiểm với LLM*
   - **Link video**: [https://www.youtube.com/watch?v=H5Lsrl0lEAY](https://www.youtube.com/watch?v=H5Lsrl0lEAY)
   - **Thời lượng**: ~12 phút.
   - **Điểm hay**: Minh họa thực tế bằng tiếng Việt, hướng dẫn cách kẻ tấn công khai thác ứng dụng chatbot và các cách thức phòng ngừa cơ bản.
