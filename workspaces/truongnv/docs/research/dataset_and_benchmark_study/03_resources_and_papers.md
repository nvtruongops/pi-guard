# CHUYÊN ĐỀ 03: DANH MỤC TÀI LIỆU HỌC THUẬT, DATASET & BÀI BÁO THỰC NGHIỆM
## HỆ THỐNG NGUỒN TÀI NGUYÊN KIỂM ĐỊNH (ZERO DEAD LINKS & OPEN-ACCESS PDF)

> **Chủ biên**: Nguyễn Văn Trường (Leader)  
> **Áp dụng cho**: Khóa luận tốt nghiệp FPT University IAP491 — Đề tài PI-Guard  
> **Khung quy chuẩn**: Chuẩn học thuật ACM CCS, NeurIPS, ACL Anthology  

---

## 📚 I. BẢNG TỔNG HỢP CÁC CÔNG TRÌNH KHOA HỌC BÌNH DUYỆT (PEER-REVIEWED PAPERS)

Toàn bộ các tài liệu tham khảo dưới đây đều tuân thủ nghiêm ngặt quy định học thuật $\ge 2022$, được xuất bản tại các hội nghị uy tín và có sẵn bản mở Open-Access:

| STT | Tác Giả & Năm | Tên Công Trình Khoa Học | Hội Nghị / Nguồn | Liên Kết Bản Mở (Open-Access PDF) | Đóng Góp Cho Đề Tài PI-Guard |
| :---: | :--- | :--- | :---: | :---: | :--- |
| [[1]](#ref1) | **Shen et al. (2024)** | *Do Anything Now: Characterizing and Evaluating In-The-Wild Jailbreak Prompts on Large Language Models* | *ACM CCS 2024* | [arXiv Open PDF](https://arxiv.org/abs/2308.03825) | Khảo sát 15,140 prompts từ tự nhiên, phân lập 1,405 mẫu Jailbreak thực tế (~9.3%) và phân loại các họ tấn công chính. |
| [[2]](#ref2) | **Jiang et al. (2024)** | *WildJailbreak: A High-Quality Synthetic Dataset for Jailbreak and Benign Contrastive Safety* | *NeurIPS 2024 D&B* | [arXiv Open PDF](https://arxiv.org/abs/2406.18510) | Bộ dữ liệu mở lớn nhất gồm 262,000 cặp câu đối kháng và Hard Benign tương ứng. |
| [[3]](#ref3) | **Chao et al. (2024)** | *JailbreakBench: An Open Robustness Benchmark for Jailbreaking Large Language Models* | *NeurIPS 2024 D&B* | [arXiv Open PDF](https://arxiv.org/abs/2404.01318) | Chuẩn benchmark đối kháng định lượng mã nguồn mở và giao thức đánh giá Attack Success Rate (ASR). |
| [[4]](#ref4) | **Perez & Ribeiro (2022)** | *Ignore Previous Prompt: Attack Techniques For Language Models* | *NeurIPS Workshops* | [arXiv Open PDF](https://arxiv.org/abs/2211.09527) | Bộ dữ liệu SPML và cơ sở toán học phân loại System Prompt Leakage. |
| [[5]](#ref5) | **Lee et al. (2022)** | *Deduplicating Training Data Makes Language Models Better* | *ACL Conference* | [arXiv Open PDF](https://arxiv.org/abs/2107.06499) | Cơ sở lý thuyết về khử trùng lặp MinHash LSH và ảnh hưởng của trùng lặp đến Memorization. |
| [[6]](#ref6) | **Liu et al. (2025)** | *DataSentinel: A Game-Theoretic Detection of Prompt Injection Attacks* | *IEEE S&P 2025* | [arXiv Open PDF](https://arxiv.org/abs/2410.14777) | Khung lý thuyết trò chơi Minimax và nguồn dữ liệu benchmark Open-Prompt-Injection. |
| [[7]](#ref7) | **Taori et al. (2023)** | *Stanford Alpaca: An Instruction-following LLaMA Model* | *Stanford CRFM* | [Stanford Open Repo](https://crfm.stanford.edu/2023/03/13/alpaca.html) | Nguồn dữ liệu huấn luyện cho lớp Benign (52,000 chỉ dẫn thông thường chất lượng cao). |

---

## 🗄️ II. DANH MỤC CÁC BỘ DỮ LIỆU HỌC THUẬT MỞ (HUGGING FACE CORPORA)

Các bộ dữ liệu được tải và xử lý trực tiếp qua Hugging Face Hub phục vụ huấn luyện và đánh giá:

1. **In-The-Wild Jailbreak Dataset (Shen et al. 2024)**:
   - **Đường dẫn**: [https://github.com/verazuo/jailbreak_llms](https://github.com/verazuo/jailbreak_llms)
   - **Ứng dụng**: Huấn luyện lớp `2: Jailbreak` (DAN, Roleplay, Dual-Persona).
2. **WildJailbreak Dataset (Allen Institute for AI - AI2)**:
   - **Đường dẫn**: [https://huggingface.co/datasets/allenai/wildjailbreak](https://huggingface.co/datasets/allenai/wildjailbreak)
   - **Ứng dụng**: Cung cấp các mẫu Hard Benign đối trọng với Jailbreak để tối ưu hóa tỷ lệ FPR.
3. **Deepset Prompt Injections Benchmark**:
   - **Đường dẫn**: [https://huggingface.co/datasets/deepset/prompt-injections](https://huggingface.co/datasets/deepset/prompt-injections)
   - **Ứng dụng**: Huấn luyện và kiểm thử lớp `1: Prompt Injection` dựa trên nghiên cứu của Perez & Ribeiro (2022).
4. **JailbreakBench Benchmark Hub**:
   - **Đường dẫn**: [https://jailbreakbench.github.io/](https://jailbreakbench.github.io/)
   - **Ứng dụng**: Đánh giá khả năng phòng thủ trước các thuật toán tấn công tối ưu hóa gradient (GCG, PAIR).

---

## 🎥 III. VIDEO BÀI GIẢNG & HỘI NGHỊ KHOA HỌC (OEMBED VERIFIED)

Toàn bộ các video dưới đây đều đã được xác thực trạng thái hoạt động công khai thông qua giao thức kiểm định `oEmbed API` của YouTube:

1. **Adversarial Attacks on LLMs & Benchmark Datasets**:
   - **Đơn vị phát hành**: Stanford Center for Research on Foundation Models (CRFM)
   - **Nội dung**: Thảo luận về các thách thức trong thu thập dữ liệu an ninh đối kháng, phân loại Jailbreak và hiện tượng rò rỉ dữ liệu khi đánh giá.
   - **Liên kết**: [https://www.youtube.com/watch?v=Sv5OLj2nVAQ](https://www.youtube.com/watch?v=Sv5OLj2nVAQ)

2. **JailbreakBench: Standardizing LLM Robustness Evaluation**:
   - **Nội dung**: Trình bày tại hội nghị NeurIPS 2024 về kiến trúc benchmark chuẩn hóa, bộ dữ liệu hành vi nguy hại (Harmful Behaviors) và phương pháp đánh giá khách quan.
   - **Liên kết**: [https://www.youtube.com/watch?v=zn2ukSnDqSg](https://www.youtube.com/watch?v=zn2ukSnDqSg)

---

## 📚 TÀI LIỆU THAM KHẢO

<a id="ref1"></a>**[1]** X. Shen et al., "Do Anything Now: Characterizing and Evaluating In-The-Wild Jailbreak Prompts on Large Language Models," in *Proceedings of the 2024 ACM SIGSAC Conference on Computer and Communications Security (CCS '24)*, Oct. 2024, pp. 4233–4246. DOI: 10.1145/3658644.3670390. Open-Access: [https://arxiv.org/abs/2308.03825](https://arxiv.org/abs/2308.03825).

<a id="ref2"></a>**[2]** Y. Jiang et al., "WildJailbreak: A High-Quality Synthetic Dataset for Jailbreak and Benign Contrastive Safety," in *Advances in Neural Information Processing Systems (NeurIPS 2024) Datasets and Benchmarks Track*, Dec. 2024. Open-Access: [https://arxiv.org/abs/2406.18510](https://arxiv.org/abs/2406.18510).

<a id="ref3"></a>**[3]** P. Chao et al., "JailbreakBench: An Open Robustness Benchmark for Jailbreaking Large Language Models," in *Advances in Neural Information Processing Systems (NeurIPS 2024) Datasets and Benchmarks Track*, Dec. 2024. Open-Access: [https://arxiv.org/abs/2404.01318](https://arxiv.org/abs/2404.01318).

<a id="ref4"></a>**[4]** F. Perez and I. Ribeiro, "Ignore Previous Prompt: Attack Techniques For Language Models," in *NeurIPS 2022 Workshop on ML Safety*, Nov. 2022. Open-Access: [https://arxiv.org/abs/2211.09527](https://arxiv.org/abs/2211.09527).

<a id="ref5"></a>**[5]** K. Lee, D. Ippolito, A. Nystrom, C. Zhang, D. Eck, C. Callison-Burch, and N. Carlini, "Deduplicating Training Data Makes Language Models Better," in *Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, May 2022, pp. 8424–8445. DOI: 10.18653/v1/2022.acl-long.577. Open-Access: [https://arxiv.org/abs/2107.06499](https://arxiv.org/abs/2107.06499).

<a id="ref6"></a>**[6]** Y. Liu, Y. Jia, J. Jia, D. Song, and N. Z. Gong, "DataSentinel: A Game-Theoretic Detection of Prompt Injection Attacks," in *Proceedings of the 2025 IEEE Symposium on Security and Privacy (SP '25)*, May 2025. Open-Access: [https://arxiv.org/abs/2410.14777](https://arxiv.org/abs/2410.14777).

<a id="ref7"></a>**[7]** R. Taori, I. Gulrajani, T. Zhang, Y. Dubois, X. Li, C. Guestrin, P. Liang, and T. B. Hashimoto, "Stanford Alpaca: An Instruction-following LLaMA Model," Stanford Center for Research on Foundation Models (CRFM), Mar. 2023. Open-Access: [https://crfm.stanford.edu/2023/03/13/alpaca.html](https://crfm.stanford.edu/2023/03/13/alpaca.html).
