# TÀI LIỆU HỌC TẬP, BÀI BÁO KHOA HỌC & VIDEO: JAILBREAK ATTACKS

Tài liệu này tổng hợp toàn bộ các bài báo khoa học toàn văn mở (Open-Access Peer-Reviewed & ArXiv Papers) và tuyển tập video phân tích đã được **kiểm định 100% khả dụng** về chuyên đề tấn công **Jailbreak trên LLM**.

---

## 📄 1. CÁC BÀI BÁO KHOA HỌC TOÀN VĂN MỞ (OPEN-ACCESS PAPERS >= 2022)

1. **Shen et al. (ACM CCS 2024) — Nghiên Cứu Khảo Sát Thực Tế Lớn Nhất Thế Giới Về DAN**:
   - **Tên bài báo**: *"\"Do Anything Now\": Characterizing and Evaluating In-The-Wild Jailbreak Prompts on Large Language Models"*.
   - **Hội nghị**: *Proceedings of the 2024 ACM SIGSAC Conference on Computer and Communications Security (CCS 2024)*.
   - **DOI chính thức**: [10.48550/arXiv.2308.03825](https://doi.org/10.48550/arXiv.2308.03825) *(Bản mở ACM CCS 2024)*
   - **Bản đọc mở toàn văn (Open-Access PDF)**: [https://arxiv.org/pdf/2308.03825](https://arxiv.org/pdf/2308.03825)
   - **Trang tóm tắt học thuật**: [arXiv:2308.03825](https://arxiv.org/abs/2308.03825)
   - **Ý nghĩa**: Khảo sát 15,140 prompt jailbreak thực tế, phân loại 4 họ chiến thuật chính (Pretending, Attention Shifting, Privilege Escalation, Obfuscation) và theo dõi lịch sử tiến hóa của DAN.

2. **Yuan et al. (ICLR 2024) — Đột Phá Về Tấn Công Mã Hóa Mật (Cipher Attacks)**:
   - **Tên bài báo**: *"GPT-4 Is Too Smart To Be Safe: Stealthy Chat with LLMs via Cipher"*.
   - **Hội nghị**: *International Conference on Learning Representations (ICLR 2024)*.
   - **DOI chính thức**: [10.48550/arXiv.2312.06674](https://doi.org/10.48550/arXiv.2312.06674)
   - **Bản đọc mở toàn văn (Open-Access PDF)**: [https://arxiv.org/pdf/2312.06674](https://arxiv.org/pdf/2312.06674)
   - **Trang tóm tắt học thuật**: [arXiv:2312.06674](https://arxiv.org/abs/2312.06674)
   - **Ý nghĩa**: Chứng minh nghịch lý "càng thông minh càng kém an toàn" khi mã hóa câu lệnh nguy hại sang Base64, ROT13, Caesar Cipher để vô hiệu hóa hoàn toàn cơ chế căn chỉnh đạo đức của LLM.

3. **Wei et al. (NeurIPS 2024) — Cơ Sở Lý Thuyết Về Sự Thất Bại Căn Chỉnh An Toàn**:
   - **Tên bài báo**: *"Jailbroken: How Does LLM Safety Training Fail?"*.
   - **Hội nghị**: *Advances in Neural Information Processing Systems (NeurIPS 2024)*.
   - **DOI chính thức**: [10.48550/arXiv.2307.02483](https://doi.org/10.48550/arXiv.2307.02483)
   - **Bản đọc mở toàn văn (Open-Access PDF)**: [https://arxiv.org/pdf/2307.02483](https://arxiv.org/pdf/2307.02483)
   - **Trang tóm tắt học thuật**: [arXiv:2307.02483](https://arxiv.org/abs/2307.02483)
   - **Ý nghĩa**: Phân tích hai nguyên nhân toán học gốc rễ của Jailbreak: Xung đột mục tiêu (*Competing Objectives*) và Suy giảm khái quát hóa an toàn (*Mismatched Generalization*).

4. **Kang et al. (2023) — Khai Thác Bản Chất Lập Trình & Giả Lập Terminal**:
   - **Tên bài báo**: *"Exploiting Programmatic Behavior of LLMs: Dual-Use Through Standard Security Attacks"*.
   - **Xuất bản**: *arXiv:2302.05733*.
   - **DOI chính thức**: [10.48550/arXiv.2302.05733](https://doi.org/10.48550/arXiv.2302.05733)
   - **Bản đọc mở toàn văn (Open-Access PDF)**: [https://arxiv.org/pdf/2302.05733](https://arxiv.org/pdf/2302.05733)
   - **Trang tóm tắt học thuật**: [arXiv:2302.05733](https://arxiv.org/abs/2302.05733)
   - **Ý nghĩa**: Cơ sở khoa học của trường phái Virtual Machine & Linux Bash Simulation.

5. **Zou et al. (CMU / CAIS 2023) — Tấn Công Hậu Tố Đối Kháng Tối Ưu Hóa Độ Dốc (GCG)**:
   - **Tên bài báo**: *"Universal and Transferable Adversarial Attacks on Aligned Language Models"*.
   - **Xuất bản**: *arXiv:2307.15043*.
   - **DOI chính thức**: [10.48550/arXiv.2307.15043](https://doi.org/10.48550/arXiv.2307.15043)
   - **Bản đọc mở toàn văn (Open-Access PDF)**: [https://arxiv.org/pdf/2307.15043](https://arxiv.org/pdf/2307.15043)
   - **Trang tóm tắt học thuật**: [arXiv:2307.15043](https://arxiv.org/abs/2307.15043)
   - **Ý nghĩa**: Minh chứng cho việc tối ưu hóa token đối kháng tự động có thể bẻ gãy an toàn trên mọi mô hình LLM.

6. **Anthropic / Anil et al. (NeurIPS 2024) — Khai Thác Cửa Sổ Ngữ Cảnh Dài (Many-Shot Jailbreaking)**:
   - **Tên bài báo**: *"Many-shot Jailbreaking"*.
   - **Hội nghị**: *Advances in Neural Information Processing Systems (NeurIPS 2024)*.
   - **Bản báo cáo kỹ thuật chính thức**: [Anthropic Research Portal](https://www.anthropic.com/research/many-shot-jailbreaking)
   - **Ý nghĩa**: Phát hiện lỗ hổng quy luật lũy thừa (power-law) khi số lượng ví dụ giả định trong ngữ cảnh lấn át lớp căn chỉnh an toàn của LLM.

7. **Russinovich et al. (Microsoft 2024) — Tấn Công Đa Lượt Tích Lũy (Crescendo Attack)**:
   - **Tên bài báo**: *"Great, Now Write an Article About That: The Crescendo Multi-Turn LLM Jailbreak Attack"*.
   - **Xuất bản**: *arXiv:2404.01833*.
   - **DOI chính thức**: [10.48550/arXiv.2404.01833](https://doi.org/10.48550/arXiv.2404.01833)
   - **Bản đọc mở toàn văn (Open-Access PDF)**: [https://arxiv.org/pdf/2404.01833](https://arxiv.org/pdf/2404.01833)
   - **Trang tóm tắt học thuật**: [arXiv:2404.01833](https://arxiv.org/abs/2404.01833)
   - **Ý nghĩa**: Khám phá kỹ thuật leo thang dần dần (Gradual Escalation) qua nhiều lượt chat nhằm qua mặt các bộ lọc Stateless.

8. **Chao et al. (2023) — Tự Động Hóa Bẻ Khóa Đa Tác Tử (PAIR Framework)**:
   - **Tên bài báo**: *"Jailbreaking Black Box Large Language Models in Twenty Queries"*.
   - **Xuất bản**: *arXiv:2310.08419*.
   - **DOI chính thức**: [10.48550/arXiv.2310.08419](https://doi.org/10.48550/arXiv.2310.08419)
   - **Bản đọc mở toàn văn (Open-Access PDF)**: [https://arxiv.org/pdf/2310.08419](https://arxiv.org/pdf/2310.08419)
   - **Trang tóm tắt học thuật**: [arXiv:2310.08419](https://arxiv.org/abs/2310.08419)
   - **Ý nghĩa**: Tự động hóa quá trình thăm dò và tối ưu prompt bẻ khóa trong dưới 20 truy vấn giữa 2 LLM.

9. **Liu et al. (2023) — Giải Thuật Di Truyền Tự Nhiên (AutoDAN)**:
   - **Tên bài báo**: *"AutoDAN: Generating Stealthy Jailbreak Prompts on Aligned Large Language Models"*.
   - **Xuất bản**: *arXiv:2310.04451*.
   - **DOI chính thức**: [10.48550/arXiv.2310.04451](https://doi.org/10.48550/arXiv.2310.04451)
   - **Bản đọc mở toàn văn (Open-Access PDF)**: [https://arxiv.org/pdf/2310.04451](https://arxiv.org/pdf/2310.04451)
   - **Trang tóm tắt học thuật**: [arXiv:2310.04451](https://arxiv.org/abs/2310.04451)
   - **Ý nghĩa**: Sử dụng giải thuật di truyền để sinh prompt jailbreak kín đáo, giữ nguyên tính tự nhiên của câu từ.

---

## 🎥 2. TUYỂN TẬP VIDEO BÀI GIẢNG TRỰC QUAN (ĐÃ XÁC MINH OEMBED 100%)

1. **Computerphile**:
   - **Tiêu đề**: *ChatGPT Jailbreak - Computerphile*
   - **Link video**: [https://www.youtube.com/watch?v=zn2ukSnDqSg](https://www.youtube.com/watch?v=zn2ukSnDqSg)
   - **Thời lượng**: ~13 phút.
   - **Điểm hay**: Phân tích kỹ thuật dưới góc độ khoa học máy tính hàn lâm về cách người dùng lợi dụng prompt engineering để vượt qua các bộ lọc an toàn của OpenAI.

2. **Isiqat (Phân Tích Kỹ Thuật DAN Thực Tế)**:
   - **Tiêu đề**: *How to Jailbreak ChatGPT (Unlock DAN Mode in 2025)*
   - **Link video**: [https://www.youtube.com/watch?v=nmni8C-QIhk](https://www.youtube.com/watch?v=nmni8C-QIhk)
   - **Thời lượng**: ~10 phút.
   - **Điểm hay**: Trình diễn trực tiếp quá trình kích hoạt nhân cách DAN, giải thích cách thức người dùng bypass các câu trả lời từ chối mặc định của LLM.

3. **Raw Onions**:
   - **Tiêu đề**: *How This Hacker JAILBROKE ChatGPT 🤖*
   - **Link video**: [https://www.youtube.com/watch?v=Nzm-9RpiHdc](https://www.youtube.com/watch?v=Nzm-9RpiHdc)
   - **Thời lượng**: ~12 phút.
   - **Điểm hay**: Giải phẫu kịch bản tấn công của hacker, từ việc tạo bối cảnh giả định (Roleplay) đến việc ngụy trang mã độc dưới dạng kịch bản phim.

4. **Copyrocket AI**:
   - **Tiêu đề**: *Get ChatGPT jailbreak prompt*
   - **Link video**: [https://www.youtube.com/watch?v=rOZ242pNdSU](https://www.youtube.com/watch?v=rOZ242pNdSU)
   - **Thời lượng**: ~1 phút (Short format cô đọng).
   - **Điểm hay**: Tóm tắt nhanh cấu trúc prompt bẻ khóa an toàn phổ biến trên mạng xã hội.
