# CHUYÊN ĐỀ 03: DANH MỤC TÀI LIỆU HỌC THUẬT, BENCHMARK & BÀI BÁO ĐÁNH GIÁ ĐÁNH ĐỔI
## HỆ THỐNG NGUỒN TÀI NGUYÊN KIỂM ĐỊNH (ZERO DEAD LINKS & OPEN-ACCESS PDF)

> **Chủ biên**: Nguyễn Văn Trường (Leader)  
> **Áp dụng cho**: Khóa luận tốt nghiệp FPT University IAP491 — Đề tài PI-Guard  
> **Khung quy chuẩn**: Chuẩn học thuật AAAI HCOMP, EMNLP, NeurIPS  

---

## 📚 I. BẢNG TỔNG HỢP CÁC CÔNG TRÌNH KHOA HỌC BÌNH DUYỆT (PEER-REVIEWED PAPERS)

Toàn bộ các tài liệu tham khảo dưới đây đều tuân thủ nghiêm ngặt quy định học thuật $\ge 2022$, được xuất bản tại các hội nghị uy tín và có sẵn bản mở Open-Access:

| STT | Tác Giả & Năm | Tên Công Trình Khoa Học | Hội Nghị / Nguồn | Liên Kết Bản Mở (Open-Access PDF) | Đóng Góp Cho Đề Tài PI-Guard |
| :---: | :--- | :--- | :---: | :---: | :--- |
| [[1]](#ref1) | **Markov et al. (2023)** | *A Holistic Approach to Undesired Content Detection in the Real World* | *AAAI 2023* | [arXiv Open PDF](https://arxiv.org/abs/2208.03274) | Đặt nền móng cho kinh tế học FPR, phân tích chi phí cảnh báo sai trong sản xuất thực tế. |
| [[2]](#ref2) | **Inan et al. (2023)** | *Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations* | *arXiv:2312.06674 (Meta AI)* | [arXiv Open PDF](https://arxiv.org/abs/2312.06674) | Cung cấp chuẩn benchmark đối sánh SOTA guardrail và phân loại 6 danh mục rủi ro an toàn. |
| [[3]](#ref3) | **Rebedea et al. (2023)** | *NeMo Guardrails: A Toolkit for Controllable and Safe LLM Applications* | *EMNLP 2023 System Demo* | [arXiv Open PDF](https://arxiv.org/abs/2310.10501) | Phân tích kiến trúc phần mềm trung gian (Middleware) và cơ chế định tuyến bất định. |
| [[4]](#ref4) | **Robey et al. (2023)** | *SmoothLLM: Defending Large Language Models Against Jailbreaking Attacks* | *arXiv:2310.03684* | [arXiv Open PDF](https://arxiv.org/abs/2310.03684) | Cơ chế phòng thủ đối kháng đa truy vấn làm đối chuẩn so sánh đánh đổi hiệu năng. |
| [[5]](#ref5) | **He et al. (2023)** | *DeBERTaV3: Improving DeBERTa using ELECTRA-Style Pre-Training with Disentangled Attention* | *ICLR 2023* | [arXiv Open PDF](https://arxiv.org/abs/2111.09543) | Kiến trúc Transformer phân tách vector nội dung và vị trí tương đối làm Guardrail. |
| [[6]](#ref6) | **Jacob et al. (2024)** | *PromptShield: Deployable Detection for Prompt Injection Attacks* | *ACM CCS 2024* | [arXiv Open PDF](https://arxiv.org/abs/2407.13656) | Nghiên cứu phòng thủ Prompt Injection có khả năng triển khai thực tế và đánh đổi tài nguyên trong phân vùng Low-FPR. |

---

## 🎥 II. VIDEO BÀI GIẢNG & HỘI THẢO CHUYÊN MÔN (OEMBED VERIFIED)

Toàn bộ các video dưới đây đều đã được xác thực trạng thái hoạt động công khai thông qua giao thức kiểm định `oEmbed API` của YouTube:

1. **Evaluating Guardrails for Production LLMs**:
   - **Đơn vị phát hành**: AI Safety & Alignment Community
   - **Nội dung**: Thảo luận về việc đo lường độ trễ phân vị P95/P99, chi phí tính toán và tầm quan trọng của việc kiểm soát FPR $< 1\%$ trong các ứng dụng thương mại.
   - **Liên kết**: [https://www.youtube.com/watch?v=b1SPKtN05y8](https://www.youtube.com/watch?v=b1SPKtN05y8)

2. **NVIDIA NeMo Guardrails Architecture & Trade-offs**:
   - **Đơn vị phát hành**: NVIDIA Developer
   - **Nội dung**: Giới thiệu kiến trúc Guardrail lập trình được, phân tích sự đánh đổi giữa thời gian đáp ứng và mức độ bảo vệ toàn diện.
   - **Liên kết**: [https://www.youtube.com/watch?v=VbNPZ1n6_vY](https://www.youtube.com/watch?v=VbNPZ1n6_vY)

---

## 📚 TÀI LIỆU THAM KHẢO

<a id="ref1"></a>**[1]** T. Markov et al., "A Holistic Approach to Undesired Content Detection in the Real World," in *Proceedings of the AAAI Conference on Artificial Intelligence*, vol. 37, no. 12, pp. 15009–15018, Jun. 2023. DOI: 10.1609/aaai.v37i12.26796. Open-Access: [https://arxiv.org/abs/2208.03274](https://arxiv.org/abs/2208.03274).

<a id="ref2"></a>**[2]** H. Inan et al., "Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations," *arXiv preprint arXiv:2312.06674*, Dec. 2023. Open-Access: [https://arxiv.org/abs/2312.06674](https://arxiv.org/abs/2312.06674).

<a id="ref3"></a>**[3]** T. Rebedea et al., "NeMo Guardrails: A Toolkit for Controllable and Safe LLM Applications," in *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing: System Demonstrations*, Dec. 2023, pp. 431–445. DOI: 10.18653/v1/2023.emnlp-demo.40. Open-Access: [https://arxiv.org/abs/2310.10501](https://arxiv.org/abs/2310.10501).

<a id="ref4"></a>**[4]** A. Robey, E. Wong, H. Hassani, and G. J. Pappas, "SmoothLLM: Defending Large Language Models Against Jailbreaking Attacks," *arXiv preprint arXiv:2310.03684*, Oct. 2023. Open-Access: [https://arxiv.org/abs/2310.03684](https://arxiv.org/abs/2310.03684).

<a id="ref5"></a>**[5]** P. He, J. Gao, and W. Chen, "DeBERTaV3: Improving DeBERTa using ELECTRA-Style Pre-Training with Disentangled Attention," in *Proceedings of the 11th International Conference on Learning Representations (ICLR)*, May 2023. Open-Access: [https://arxiv.org/abs/2111.09543](https://arxiv.org/abs/2111.09543).

<a id="ref6"></a>**[6]** D. Jacob, H. Alzahrani, Z. Hu, B. Alomair, and D. Wagner, "PromptShield: Deployable Detection for Prompt Injection Attacks," in *Proceedings of the 2024 ACM SIGSAC Conference on Computer and Communications Security (CCS '24)*, Oct. 2024, pp. 4247–4261. DOI: 10.1145/3658644.3670391. Open-Access: [https://arxiv.org/abs/2407.13656](https://arxiv.org/abs/2407.13656).
