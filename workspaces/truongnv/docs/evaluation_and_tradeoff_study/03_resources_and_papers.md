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
| **1** | **Markov et al. (2023)** | *A Holistic Approach to Undesired Content Detection in the Real World* | *AAAI HCOMP 2023* | [arXiv Open PDF](https://arxiv.org/abs/2208.03274) | Đặt nền móng cho kinh tế học FPR, phân tích chi phí cảnh báo sai trong sản xuất thực tế. |
| **2** | **Inan et al. (2023)** | *Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations* | *arXiv:2312.06674 (Meta AI)* | [arXiv Open PDF](https://arxiv.org/abs/2312.06674) | Cung cấp chuẩn benchmark đối sánh SOTA guardrail và phân loại 6 danh mục rủi ro an toàn. |
| **3** | **Rebedea et al. (2023)** | *NeMo Guardrails: A Toolkit for Controllable and Safe LLM Applications* | *EMNLP 2023 System Demo* | [arXiv Open PDF](https://arxiv.org/abs/2310.10501) | Phân tích kiến trúc phần mềm trung gian (Middleware) và cơ chế định tuyến bất định. |
| **4** | **Yao et al. (2022)** | *ZeroQuant: Efficient and Affordable Post-Training Quantization for Large-Scale Transformers* | *NeurIPS 2022* | [arXiv Open PDF](https://arxiv.org/abs/2206.01861) | Cơ sở lý thuyết lượng tử hóa INT8 động giúp đạt điểm tối ưu trên đường cong biên Pareto. |
| **5** | **He et al. (2023)** | *DeBERTaV3: Improving DeBERTa using ELECTRA-Style Pre-Training with Disentangled Attention* | *ICLR 2023* | [arXiv Open PDF](https://arxiv.org/abs/2111.09543) | Kiến trúc Transformer phân tách vector nội dung và vị trí tương đối làm Guardrail. |

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

<a id="ref1"></a>**[1]** T. Markov et al., "A Holistic Approach to Undesired Content Detection in the Real World," in *AAAI Conference on Human Computation and Crowdsourcing (HCOMP)*, 2023. Link: [https://arxiv.org/abs/2208.03274](https://arxiv.org/abs/2208.03274).

<a id="ref2"></a>**[2]** H. Inan et al., "Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations," *arXiv preprint arXiv:2312.06674*, 2023. Link: [https://arxiv.org/abs/2312.06674](https://arxiv.org/abs/2312.06674).

<a id="ref3"></a>**[3]** T. Rebedea et al., "NeMo Guardrails: A Toolkit for Controllable and Safe LLM Applications," in *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing (EMNLP)*, 2023. Link: [https://arxiv.org/abs/2310.10501](https://arxiv.org/abs/2310.10501).

<a id="ref4"></a>**[4]** Z. Yao et al., "ZeroQuant: Efficient and Affordable Post-Training Quantization for Large-Scale Transformers," in *Advances in Neural Information Processing Systems (NeurIPS)*, 2022. Link: [https://arxiv.org/abs/2206.01861](https://arxiv.org/abs/2206.01861).

<a id="ref5"></a>**[5]** P. He, J. Gao, and W. Chen, "DeBERTaV3: Improving DeBERTa using ELECTRA-Style Pre-Training with Disentangled Attention," in *International Conference on Learning Representations (ICLR)*, 2023. Link: [https://arxiv.org/abs/2111.09543](https://arxiv.org/abs/2111.09543).
