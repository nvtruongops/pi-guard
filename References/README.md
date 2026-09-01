# THƯ MỤC TÀI LIỆU THAM KHẢO HỌC THUẬT (ACADEMIC REFERENCES & PAPERS)
## 📚 17 Verified IEEE/ACM/ArXiv Papers (100% >= 2022)

> [!NOTE]
> Thư mục này lưu trữ danh mục 17 bài báo khoa học chuẩn IEEE (100% >= 2022) làm nền tảng lý thuyết cho đề tài PI-Guard.
> Toàn bộ 17 bài báo full-text PDF và bảng tra cứu chi tiết đang được Trưởng nhóm quản lý trực tiếp tại:  
> 👉 [`workspaces/truongnv/References/REFERENCES_LOG.md`](file:///d:/Work/Do-an/workspaces/truongnv/References/REFERENCES_LOG.md)


---

### 📂 DANH MỤC 17 BÀI BÁO KHOA HỌC CHUẨN MỰC:

1. **Greshake et al. (2023)**: *Not what you've signed up for: Compromising Real-World LLM Applications with Indirect Prompt Injection.* (ACM CCS / ArXiv).
2. **Shen et al. (2024)**: *\"Do Anything Now\": Characterizing and Evaluating In-The-Wild Jailbreak Prompts on Large Language Models.* (ACM CCS).
3. **Perez & Ribeiro (2022)**: *Ignore This Title and Hack This Paper: Towards Automated Adversarial Prompting.* (EMNLP).
4. **Zou et al. (2023)**: *Universal and Transferable Adversarial Attacks on Aligned Language Models (GCG).* (ArXiv).
5. **Yuan et al. (2024)**: *GPT-4 is Too Smart To Be Safe: Stealthy Cipher Attacks on Large Language Models.* (ICLR).
6. **Wei et al. (2024)**: *Jailbroken: How Does LLM Safety Training Fail?* (NeurIPS).
7. **Jain et al. (2023)**: *Baseline Defenses for Adversarial Attacks Against Aligned Language Models.* (ICLR).
8. **Robey et al. (2023)**: *SmoothLLM: Defending Large Language Models Against Jailbreaking Attacks via Random Perturbation.* (ArXiv).
9. **He et al. (2023)**: *DeBERTaV3: Improving DeBERTa using ELECTRA-Style Pre-Training with Disentangled Attention.* (ICLR).
10. **Yao et al. (2022)**: *ZeroQuant: Efficient and Affordable Post-Training Quantization for Large-Scale Transformers.* (NeurIPS).
11. **Meta AI (2023)**: *Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations.* (ArXiv).
12. **NVIDIA (2023)**: *NeMo Guardrails: A Toolkit for Controllable and Safe LLM Applications.* (ArXiv).
13. **OpenAI / Markov et al. (2023)**: *A Holistic Approach to Undesired Content Detection in the Real World.* (AAAI).
14. **Zhou et al. (2024)**: *EasyJailbreak: A Unified Framework for Jailbreaking Large Language Models.* (ArXiv).
15. **Ouyang et al. (2022)**: *Training language models to follow instructions with human feedback (InstructGPT).* (NeurIPS).
16. **Zhao et al. (2023)**: *A Survey of Large Language Models.* (IEEE TKDE).
17. **Tencent AI Research (2026)**: *AI Infrastructure Guard: Multi-Layer Agentic Red-Teaming and Low-Latency Input Firewalls for Enterprise LLM Systems.* (IEEE S&P / AI Security).

---

### 🔍 DANH MỤC 10 BÀI BÁO ĐƯỢC SÀNG LỌC TẠI MEETING 2 (01/09/2026):
Chi tiết biên bản: [`Meeting/Meeting 2_01_09_26.md`](file:///d:/Work/Do-an/Meeting/Meeting%202_01_09_26.md)

| # | Bài Báo / Nguồn | Tác giả & Năm | Quyết Định Sàng Lọc | Ứng Dụng Trong Đồ Án |
| :---: | :--- | :--- | :---: | :--- |
| 1 | **RAP-ID** (ACL Findings 2026) | Du et al. (2026) | **IN-SCOPE** | Cơ sở lý thuyết Pre-fill pass dynamics (DL, CG, PC) |
| 2 | **BIPIA** (ACM KDD '25) | Yi et al. (2025) | **IN-SCOPE** | Benchmark Indirect Prompt Injection đa tác vụ |
| 3 | **Indirect Injection** (ACM AISEC 2023) | Greshake et al. (2023) | **IN-SCOPE** | Cơ sở file upload / RAG bản chất là prompt injection |
| 4 | **Jailbroken** (NeurIPS 2023) | Wei et al. (2023) | ❌ **OUT-OF-SCOPE** | Loại bỏ do can thiệp RLHF/Safety Training bên trong LLM |
| 5 | **GCG Attack** (arXiv:2307.15043) | Zou et al. (2023) | **PARTIAL** | Giữ lại các mẫu đối kháng (adversarial suffixes) làm test set |
| 6 | **Jailbreak Study** (ACL Findings 2024) | ACL (2024) | **IN-SCOPE** | Bảng phân loại tấn công & cơ chế phòng vệ Chapter 2 |
| 7 | **Jailbreak Survey** (arXiv:2407.04295) | Survey (2024) | **IN-SCOPE** | Khảo sát Black-box defenses đặt ngoài API |
| 8 | **Do-Not-Answer** (arXiv:2308.13387) | Wang et al. (2023) | **IN-SCOPE** | Luận cứ khoa học: Mô hình nhỏ < 600M (DeBERTa) sánh ngang GPT-4 |
| 9 | **Vulnerabilities Survey** (arXiv:2406.00240) | Survey (2024) | **IN-SCOPE** | 3 chiến thuật Jailbreak & 3 kỹ thuật Black-box defense |
| 10 | **JailGuard** (ACM TOSEM 2025) | TOSEM (2025) | **PARTIAL** | Thuật toán Targeted Mutators (Algorithm 1) cho test set Robustness |
