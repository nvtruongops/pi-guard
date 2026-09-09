# THƯ MỤC TÀI LIỆU THAM KHẢO HỌC THUẬT (ACADEMIC REFERENCES & PAPERS)
## 📚 18 Verified Scientific Papers & Foundational Architecture

> [!NOTE]
> Thư mục này lưu trữ bản sao toàn văn PDF và danh mục các công trình nghiên cứu khoa học làm nền tảng lý thuyết và cơ sở thực nghiệm cho đề tài **PI-Guard**.
> Toàn bộ các bài báo full-text PDF và bảng ánh xạ chi tiết được quản lý tập trung tại:  
> 👉 [`References/REFERENCES_LOG.md`](file:///d:/Work/Do-an/References/REFERENCES_LOG.md)

---

### 🎯 1. DANH MỤC 8 BÀI BÁO NỀN TẢNG DÙNG TRONG SLIDE BÁO CÁO GVHD ([`reports/PI-GUARD-Present-109.pptx`](file:///d:/Work/Do-an/reports/PI-GUARD-Present-109.pptx))

Tại buổi báo cáo tiến độ với Giáo viên Hướng dẫn ngày 10/09/2026, toàn bộ 8 công trình học thuật nền tảng được chọn lọc kỹ lưỡng, trích dẫn chuẩn mực tại **Slide 21** và xuyên suốt bài báo cáo:

| # | Slide | Tác Giả & Năm | Tên Công Trình & Nơi Công Bố | Tệp PDF Cục Bộ Trong `References/` | Đóng Góp Kỹ Thuật Cho Hệ Thống PI-Guard |
| :-: | :-: | :--- | :--- | :--- | :--- |
| **[1]** | Slides 4, 6, 7 | **Perez & Ribeiro (2022)** | *Ignore Previous Prompt: Attack Techniques For Language Models* (NeurIPS ML Safety Workshop 2022) | [`Perez_2022_Ignore_This_Title_Hack_This_Paper_Prompt_Injection.pdf`](file:///d:/Work/Do-an/References/Perez_2022_Ignore_This_Title_Hack_This_Paper_Prompt_Injection.pdf) | Bản chất lỗ hổng ranh giới phẳng ($X = S \mathbin{\Vert} U$), cơ chế Goal Hijacking & System Prompt Leaking |
| **[2]** | Slides 5, 6 | **Shen et al. (2024)** | *"Do Anything Now": Characterizing and Evaluating In-The-Wild Jailbreak Prompts on Large Language Models* (ACM CCS '24) | [`Shen_2024_Do_Anything_Now_Jailbreak_Prompts_In_The_Wild.pdf`](file:///d:/Work/Do-an/References/Shen_2024_Do_Anything_Now_Jailbreak_Prompts_In_The_Wild.pdf) | Bản chất bẻ khóa căn chỉnh an toàn RLHF, phân tích cấu trúc prompt DAN và tập dữ liệu in-the-wild |
| **[3]** | Slides 8–11 | **Greshake et al. (2023)** | *Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection* (ACM AISec '23) | [`Greshake_2023_Indirect_Prompt_Injection.pdf`](file:///d:/Work/Do-an/References/Greshake_2023_Indirect_Prompt_Injection.pdf) | 4 Tầng thiệt hại thực tế doanh nghiệp (Data Exfiltration, Agent Hijacking, Denial of Wallet, Chế tài EU AI Act 35M EUR) |
| **[4]** | Slide 12 | **Tencent Zhuque Lab (2026)** | *AI-Infra-Guard: Multi-Layer Attack Surface and Defense Framework for AI Agents* (Tencent Security Tech Report 2026) | [`Tencent_2026_AI_Infra_Guard_MultiLayer_Agent_RedTeaming.pdf`](file:///d:/Work/Do-an/References/Tencent_2026_AI_Infra_Guard_MultiLayer_Agent_RedTeaming.pdf) | Mô hình đe dọa Zero-Trust 4 Zone (Zone 0 đến Zone 3) và định vị vành đai bảo vệ PI-Guard tại Zone 1 |
| **[5]** | Slides 16, 17 | **Jain et al. (2023)** | *Baseline Defenses for Adversarial Attacks Against Aligned Language Models* (arXiv:2309.00614) | [`Jain_2023_Baseline_Defenses_Adversarial_Attacks_LLMs.pdf`](file:///d:/Work/Do-an/References/Jain_2023_Baseline_Defenses_Adversarial_Attacks_LLMs.pdf) | Cơ sở toán học Tầng 1: Character N-Grams TF-IDF bóc tách ký tự đặc biệt, Leetspeak (`1gn0r3`) trong $< 1\text{ms}$ |
| **[6]** | Slide 17 | **He et al. (2021/2023)** | *DeBERTa: Decoding-enhanced BERT with Disentangled Attention* (ICLR 2021 / 2023) | [`He_2023_DeBERTaV3_Disentangled_Attention_ICLR.pdf`](file:///d:/Work/Do-an/References/He_2023_DeBERTaV3_Disentangled_Attention_ICLR.pdf) | Cơ sở toán học Tầng 2: Cơ chế Disentangled Attention phân tách vector nội dung và vị trí tương đối |
| **[7]** | Slide 17 | **Yao et al. (2022)** | *ZeroQuant: Efficient and Affordable Post-Training Quantization for Large-Scale Transformers* (NeurIPS 2022) | [`Yao_2022_ZeroQuant_Efficient_Post_Training_Quantization_Transformers.pdf`](file:///d:/Work/Do-an/References/Yao_2022_ZeroQuant_Efficient_Post_Training_Quantization_Transformers.pdf) | Cơ sở kỹ thuật lượng hóa động INT8 Post-Training Quantization tối ưu độ trễ P95 $< 22\text{ms}$ trên CPU |
| **[8]** | Slide 18 | **Saltzer & Schroeder (1975)** | *The Protection of Information in Computer Systems* (Proceedings of the IEEE, vol. 63, no. 9, Sept. 1975) | [`Saltzer_1975_The_Protection_of_Information_in_Computer_Systems.pdf`](file:///d:/Work/Do-an/References/Saltzer_1975_The_Protection_of_Information_in_Computer_Systems.pdf) | Nguyên lý phân tầng phòng thủ chiều sâu (Defense-in-Depth) & thiết kế kiến trúc Two-Tier Cascaded Guardrail |

---

### 📂 2. TOÀN VĂN DANH MỤC 18 BÀI BÁO KHOA HỌC CHUẨN MỰC:

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
18. **Saltzer & Schroeder (1975)**: *The Protection of Information in Computer Systems.* (Proceedings of the IEEE, vol. 63, no. 9, pp. 1278–1308).

---

### 🔍 3. DANH MỤC 10 BÀI BÁO ĐƯỢC SÀNG LỌC TẠI MEETING 2 (01/09/2026):
Chi tiết biên bản: [`Meeting/Meeting 2_01_09_26.md`](file:///d:/Work/Do-an/Meeting/Meeting%202_01_09_26.md)  
Phân bổ không gian làm việc thành viên: [`workspaces/vietpmh/References/`](file:///d:/Work/Do-an/workspaces/vietpmh/References/), [`workspaces/phuongddd/References/`](file:///d:/Work/Do-an/workspaces/phuongddd/References/), [`workspaces/ducnq/References/`](file:///d:/Work/Do-an/workspaces/ducnq/References/).

| # | Bài Báo / Nguồn | Tác giả & Năm | File PDF Cục Bộ | Quyết Định Sàng Lọc | Ứng Dụng Trong Đồ Án |
| :---: | :--- | :--- | :--- | :--- | :--- |
| 1 | **RAP-ID** (ACL Findings 2026) | Du et al. (2026) | [`Viet_2026_RAP_ID_Robust_Alignment_Preservation_Injection_Defense.pdf`](file:///d:/Work/Do-an/References/Viet_2026_RAP_ID_Robust_Alignment_Preservation_Injection_Defense.pdf) | **IN-SCOPE** | Cơ sở lý thuyết Pre-fill pass dynamics (DL, CG, PC) |
| 2 | **BIPIA** (ACM KDD '25) | Yi et al. (2025) | [`Viet_2024_BIPIA_Benchmarking_Indirect_Prompt_Injection_Attacks.pdf`](file:///d:/Work/Do-an/References/Viet_2024_BIPIA_Benchmarking_Indirect_Prompt_Injection_Attacks.pdf) | **IN-SCOPE** | Benchmark Indirect Prompt Injection đa tác vụ |
| 3 | **Indirect Injection** (ACM AISEC 2023) | Greshake et al. (2023) | [`Greshake_2023_Indirect_Prompt_Injection.pdf`](file:///d:/Work/Do-an/References/Greshake_2023_Indirect_Prompt_Injection.pdf) | **IN-SCOPE** | Cơ sở file upload / RAG bản chất là prompt injection |
| 4 | **Jailbroken** (NeurIPS 2023) | Wei et al. (2023) | [`Wei_2024_Jailbroken_How_LLM_Safety_Training_Fails.pdf`](file:///d:/Work/Do-an/References/Wei_2024_Jailbroken_How_LLM_Safety_Training_Fails.pdf) | ❌ **OUT-OF-SCOPE** | Loại bỏ do can thiệp RLHF/Safety Training bên trong LLM |
| 5 | **GCG Attack** (arXiv:2307.15043) | Zou et al. (2023) | [`Zou_2023_Universal_Transferable_Adversarial_Attacks_GCG.pdf`](file:///d:/Work/Do-an/References/Zou_2023_Universal_Transferable_Adversarial_Attacks_GCG.pdf) | **PARTIAL** | Giữ lại các mẫu đối kháng (adversarial suffixes) làm test set |
| 6 | **Jailbreak Study** (ACL Findings 2024) | ACL (2024) | [`Phuong_2024_ACL_Comprehensive_Study_Jailbreak_Attack_Defense.pdf`](file:///d:/Work/Do-an/References/Phuong_2024_ACL_Comprehensive_Study_Jailbreak_Attack_Defense.pdf) | **IN-SCOPE** | Bảng phân loại tấn công & cơ chế phòng vệ Chapter 2 |
| 7 | **Jailbreak Survey** (arXiv:2407.04295) | Survey (2024) | [`Phuong_2024_Survey_Jailbreak_Attacks_Defenses_LLMs.pdf`](file:///d:/Work/Do-an/References/Phuong_2024_Survey_Jailbreak_Attacks_Defenses_LLMs.pdf) | **IN-SCOPE** | Khảo sát Black-box defenses đặt ngoài API |
| 8 | **Do-Not-Answer** (arXiv:2308.13387) | Wang et al. (2023) | [`Phuong_2023_Do_Not_Answer_Dataset_Evaluating_Safeguards.pdf`](file:///d:/Work/Do-an/References/Phuong_2023_Do_Not_Answer_Dataset_Evaluating_Safeguards.pdf) | **IN-SCOPE** | Luận cứ khoa học: Mô hình nhỏ < 600M (DeBERTa) sánh ngang GPT-4 |
| 9 | **Vulnerabilities Survey** (arXiv:2406.00240) | Survey (2024) | [`Phuong_2024_Exploring_Vulnerabilities_Protections_LLMs_Survey.pdf`](file:///d:/Work/Do-an/References/Phuong_2024_Exploring_Vulnerabilities_Protections_LLMs_Survey.pdf) | **IN-SCOPE** | 3 chiến thuật Jailbreak & 3 kỹ thuật Black-box defense |
| 10 | **JailGuard** (ACM TOSEM 2025) | TOSEM (2025) | [`Duc_2025_JailGuard_Universal_Detection_Framework_TOSEM.pdf`](file:///d:/Work/Do-an/References/Duc_2025_JailGuard_Universal_Detection_Framework_TOSEM.pdf) | **PARTIAL** | Thuật toán Targeted Mutators (Algorithm 1) cho test set Robustness |
