# REFERENCES LOG & APPLICATION MAPPING MATRIX
## Hệ Thống Quản Lý & Định Vị Tài Liệu Tham Khảo — Đề Tài PI-Guard (18 Bài Báo Học Thuật Đỉnh Cao)

> **Thư mục lưu trữ tài liệu gốc**: `d:/Work/Do-an/References/`  
> **Tiêu chí chuẩn hóa**: 17 bài báo xuất bản từ 2022–2026 (Kỷ nguyên LLM hiện đại) + 1 công trình kinh điển đặt nền móng kiến trúc phòng vệ phân tầng (Saltzer & Schroeder, IEEE 1975).  
> **Cập nhật lần cuối**: 2026-09-09  
> **Mục đích**: Lưu trữ, theo dõi và ánh xạ chi tiết toàn bộ **18 bài báo PDF** trong `References/` tới **danh sách các file cụ thể trong toàn bộ repository `D:\Work\Do-an/`**.

---

## 📊 1. BẢNG ÁNH XẠ CHI TIẾT 18 TÀI LIỆU KHOA HỌC VÀO REPOSITORY

| # | File PDF Tham Khảo (`References/`) | Tác Giả & Năm (Online URL) | Nơi Xuất Bản | Các File Liên Quan Cụ Thể Trong Repo | Ứng Dụng Cốt Lõi Trong Đồ Án PI-Guard |
| :-: | :--- | :--- | :--- | :--- | :--- |
| <a id="ref1"></a>**1** | [`Zhao_2023_A_Survey_of_Large_Language_Models.pdf`](file:///d:/Work/Do-an/reports/References/Zhao_2023_A_Survey_of_Large_Language_Models.pdf) | [Zhao et al. (2023)](https://arxiv.org/abs/2303.18223) | *IJCAI / arXiv 2023* | • [`docs/thesis/Review1_Problem_Definition_and_Threat_Model.md`](file:///d:/Work/Do-an/docs/thesis/Review1_Problem_Definition_and_Threat_Model.md)<br>• [`docs/prompt_study/01_llm_foundations_and_token_generation.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/prompt_study/01_llm_foundations_and_token_generation.md) | Khảo sát tổng thể kiến trúc LLM, cơ chế sinh token tự hồi quy và lỗ hổng ranh giới phẳng Code/Data |
| <a id="ref2"></a>**2** | [`Ouyang_2022_InstructGPT_Training_Language_Models_Follow_Instructions.pdf`](file:///d:/Work/Do-an/reports/References/Ouyang_2022_InstructGPT_Training_Language_Models_Follow_Instructions.pdf) | [Ouyang et al. (2022)](https://arxiv.org/abs/2203.02155) | *NeurIPS 2022 (OpenAI)* | • [`docs/thesis/Review1_Problem_Definition_and_Threat_Model.md`](file:///d:/Work/Do-an/docs/thesis/Review1_Problem_Definition_and_Threat_Model.md)<br>• [`docs/prompt_study/01_llm_foundations_and_token_generation.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/prompt_study/01_llm_foundations_and_token_generation.md)<br>• [`src/llm/provider.py`](file:///d:/Work/Do-an/src/llm/provider.py) | Nền tảng Instruction Tuning & RLHF, cơ chế xử lý System Instruction trên Downstream LLM |
| <a id="ref3"></a>**3** | [`Perez_2022_Ignore_This_Title_Hack_This_Paper_Prompt_Injection.pdf`](file:///d:/Work/Do-an/reports/References/Perez_2022_Ignore_This_Title_Hack_This_Paper_Prompt_Injection.pdf) | [Perez & Ribeiro (2022)](https://arxiv.org/abs/2211.09527) | *NeurIPS ML Safety 2022* | • [`CAPSTONE PROJECT REGISTER.md`](file:///d:/Work/Do-an/CAPSTONE%20PROJECT%20REGISTER.md)<br>• [`docs/prompt_study/03_instruction_hierarchy_and_flat_boundary.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/prompt_study/03_instruction_hierarchy_and_flat_boundary.md)<br>• [`reports/PI-GUARD-Present-109.pptx`](file:///d:/Work/Do-an/reports/PI-GUARD-Present-109.pptx)<br>• [`src/preprocessing/cleaner.py`](file:///d:/Work/Do-an/src/preprocessing/cleaner.py) | Định nghĩa nền tảng Direct Prompt Injection, cơ chế Instruction Override và System Prompt Leaking |
| <a id="ref4"></a>**4** | [`Greshake_2023_Indirect_Prompt_Injection.pdf`](file:///d:/Work/Do-an/reports/References/Greshake_2023_Indirect_Prompt_Injection.pdf) | [Greshake et al. (2023)](https://arxiv.org/abs/2302.12173) | *ACM AISec 2023* | • [`docs/thesis/Review1_Problem_Definition_and_Threat_Model.md`](file:///d:/Work/Do-an/docs/thesis/Review1_Problem_Definition_and_Threat_Model.md)<br>• [`docs/prompt_study/03_instruction_hierarchy_and_flat_boundary.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/prompt_study/03_instruction_hierarchy_and_flat_boundary.md)<br>• [`reports/PI-GUARD-Present-109.pptx`](file:///d:/Work/Do-an/reports/PI-GUARD-Present-109.pptx)<br>• [`src/datasets/splitter.py`](file:///d:/Work/Do-an/src/datasets/splitter.py) | Phân tích cơ chế Indirect Prompt Injection, 4 tầng thiệt hại doanh nghiệp và phân cụm Group-Aware Splitting |
| <a id="ref5"></a>**5** | [`Wei_2024_Jailbroken_How_LLM_Safety_Training_Fails.pdf`](file:///d:/Work/Do-an/reports/References/Wei_2024_Jailbroken_How_LLM_Safety_Training_Fails.pdf) | [Wei et al. (2024)](https://arxiv.org/abs/2307.02483) | *NeurIPS 2024* | • [`docs/thesis/Review1_Problem_Definition_and_Threat_Model.md`](file:///d:/Work/Do-an/docs/thesis/Review1_Problem_Definition_and_Threat_Model.md)<br>• [`docs/prompt_study/03_instruction_hierarchy_and_flat_boundary.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/prompt_study/03_instruction_hierarchy_and_flat_boundary.md)<br>• [`src/preprocessing/obfuscation.py`](file:///d:/Work/Do-an/src/preprocessing/obfuscation.py) | Cơ chế suy giảm an toàn (Competing Objectives); phân loại Jailbreak Roleplay/DAN/Persona Adoption |
| <a id="ref6"></a>**6** | [`Tencent_2026_AI_Infra_Guard_MultiLayer_Agent_RedTeaming.pdf`](file:///d:/Work/Do-an/reports/References/Tencent_2026_AI_Infra_Guard_MultiLayer_Agent_RedTeaming.pdf) | [Tencent Zhuque Lab (2026)](https://arxiv.org/abs/2606.31227) | *Tencent Tech Report 2026* | • [`docs/research/Tencent2026_Paper_Analysis_and_Mapping_to_PIGuard.md`](file:///d:/Work/Do-an/docs/research/Tencent2026_Paper_Analysis_and_Mapping_to_PIGuard.md)<br>• [`reports/PI-GUARD-Present-109.pptx`](file:///d:/Work/Do-an/reports/PI-GUARD-Present-109.pptx)<br>• [`src/policy/policy_engine.py`](file:///d:/Work/Do-an/src/policy/policy_engine.py) | Threat Model 4 tầng Zero-Trust (Zone 0 đến 3), nguyên lý Layer-Paradigm Matching và 26+ Attack Operators |
| <a id="ref7"></a>**7** | [`Meta_2023_Llama_Guard_Input_Output_Safeguard.pdf`](file:///d:/Work/Do-an/reports/References/Meta_2023_Llama_Guard_Input_Output_Safeguard.pdf) | [Meta AI / Inan et al. (2023)](https://arxiv.org/abs/2312.06674) | *arXiv 2023* | • [`docs/thesis/Review1_Problem_Definition_and_Threat_Model.md`](file:///d:/Work/Do-an/docs/thesis/Review1_Problem_Definition_and_Threat_Model.md)<br>• [`docs/optimization_study/04_benchmarks_metrics_and_tradeoffs.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/optimization_study/04_benchmarks_metrics_and_tradeoffs.md)<br>• [`reports/PI-GUARD-Present-109.pptx`](file:///d:/Work/Do-an/reports/PI-GUARD-Present-109.pptx)<br>• [`src/policy/thresholds.py`](file:///d:/Work/Do-an/src/policy/thresholds.py) | Mô hình đối chuẩn Guardrail (Llama Guard 3 8B), định nghĩa Taxonomy an toàn và thiết lập ngưỡng phân loại |
| <a id="ref8"></a>**8** | [`NVIDIA_2023_NeMo_Guardrails_Toolkit.pdf`](file:///d:/Work/Do-an/reports/References/NVIDIA_2023_NeMo_Guardrails_Toolkit.pdf) | [Rebedea et al. / NVIDIA (2023)](https://arxiv.org/abs/2310.10501) | *EMNLP 2023* | • [`docs/thesis/Review1_Problem_Definition_and_Threat_Model.md`](file:///d:/Work/Do-an/docs/thesis/Review1_Problem_Definition_and_Threat_Model.md)<br>• [`docs/optimization_study/03_inference_acceleration_and_system_design.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/optimization_study/03_inference_acceleration_and_system_design.md)<br>• [`src/api/middleware.py`](file:///d:/Work/Do-an/src/api/middleware.py) | Kiến trúc Guardrail Middleware bất đồng bộ đặt trước LLM để đánh chặn request trước khi gọi LLM |
| <a id="ref9"></a>**9** | [`He_2023_DeBERTaV3_Disentangled_Attention_ICLR.pdf`](file:///d:/Work/Do-an/reports/References/He_2023_DeBERTaV3_Disentangled_Attention_ICLR.pdf) | [He et al. (2021/2023)](https://arxiv.org/abs/2006.03654) | *ICLR 2021 / 2023 (Microsoft)* | • [`docs/research/State_of_the_Art_Guardrail_and_Jailbreak_Benchmarks_Analysis.md`](file:///d:/Work/Do-an/docs/research/State_of_the_Art_Guardrail_and_Jailbreak_Benchmarks_Analysis.md)<br>• [`docs/optimization_study/01_quantization_theory_and_ptq_math.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/optimization_study/01_quantization_theory_and_ptq_math.md)<br>• [`reports/PI-GUARD-Present-109.pptx`](file:///d:/Work/Do-an/reports/PI-GUARD-Present-109.pptx)<br>• [`src/models/classifier.py`](file:///d:/Work/Do-an/src/models/classifier.py) | **Trụ cột An ninh 2**: Mô hình phân loại ngữ nghĩa sâu (`microsoft/deberta-v3-base`) với Disentangled Attention tách biệt vị trí và nội dung |
| <a id="ref10"></a>**10** | [`OpenAI_2023_Undesired_Content_Detection.pdf`](file:///d:/Work/Do-an/reports/References/OpenAI_2023_Undesired_Content_Detection.pdf) | [Markov et al. (2023)](https://arxiv.org/abs/2208.03274) | *AAAI HCOMP 2023* | • [`docs/thesis/Review1_Problem_Definition_and_Threat_Model.md`](file:///d:/Work/Do-an/docs/thesis/Review1_Problem_Definition_and_Threat_Model.md)<br>• [`docs/optimization_study/04_benchmarks_metrics_and_tradeoffs.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/optimization_study/04_benchmarks_metrics_and_tradeoffs.md)<br>• [`src/evaluation/metrics.py`](file:///d:/Work/Do-an/src/evaluation/metrics.py) | **Trụ cột An ninh 3**: Phương pháp luận đo lường tỷ lệ chặn nhầm (False Positive Rate - FPR < 1.5%) trên tập Benign và cân bằng Security/Usability |
| <a id="ref11"></a>**11** | [`Shen_2024_Do_Anything_Now_Jailbreak_Prompts_In_The_Wild.pdf`](file:///d:/Work/Do-an/reports/References/Shen_2024_Do_Anything_Now_Jailbreak_Prompts_In_The_Wild.pdf) | [Shen et al. (2024)](https://arxiv.org/abs/2308.03825) | *ACM CCS 2024* | • [`scripts/download_dataset.py`](file:///d:/Work/Do-an/scripts/download_dataset.py)<br>• [`reports/PI-GUARD-Present-109.pptx`](file:///d:/Work/Do-an/reports/PI-GUARD-Present-109.pptx)<br>• [`notebooks/data/manifests/attack_taxonomy.json`](file:///d:/Work/Do-an/notebooks/data/manifests/attack_taxonomy.json) | Dữ liệu Jailbreak thực tế (15,140 in-the-wild prompts từ Reddit/Discord), taxonomy các dạng tấn công DAN & Roleplay |
| <a id="ref12"></a>**12** | [`Zhou_2024_EasyJailbreak_Unified_Framework.pdf`](file:///d:/Work/Do-an/reports/References/Zhou_2024_EasyJailbreak_Unified_Framework.pdf) | [Zhou et al. (2024)](https://arxiv.org/abs/2403.12171) | *arXiv 2024* | • [`src/preprocessing/obfuscation.py`](file:///d:/Work/Do-an/src/preprocessing/obfuscation.py)<br>• [`tests/adversarial/`](file:///d:/Work/Do-an/tests/adversarial/) | **Kiểm thử Độ bền Đối kháng**: Kỹ thuật đột biến cú pháp (Mutators: Leetspeak, Spacing, Roleplay) phục vụ kiểm thử độ bền |
| <a id="ref13"></a>**13** | [`Zou_2023_Universal_Transferable_Adversarial_Attacks_GCG.pdf`](file:///d:/Work/Do-an/reports/References/Zou_2023_Universal_Transferable_Adversarial_Attacks_GCG.pdf) | [Zou et al. (2023)](https://arxiv.org/abs/2307.15043) | *arXiv 2023 (CMU/CAIS)* | • [`tests/adversarial/`](file:///d:/Work/Do-an/tests/adversarial/)<br>• [`notebooks/04_ablation.ipynb`](file:///d:/Work/Do-an/notebooks/04_ablation.ipynb) | Cơ chế tấn công hậu tố tối ưu hóa độ dốc (Greedy Coordinate Gradient - GCG) và kiểm thử nhận diện chuỗi token nhiễu |
| <a id="ref14"></a>**14** | [`Robey_2023_SmoothLLM_Defending_LLMs_Random_Perturbation.pdf`](file:///d:/Work/Do-an/reports/References/Robey_2023_SmoothLLM_Defending_LLMs_Random_Perturbation.pdf) | [Robey et al. (2023)](https://arxiv.org/abs/2310.03684) | *arXiv 2023 (Penn)* | • [`docs/thesis/Review1_Problem_Definition_and_Threat_Model.md`](file:///d:/Work/Do-an/docs/thesis/Review1_Problem_Definition_and_Threat_Model.md)<br>• [`src/preprocessing/cleaner.py`](file:///d:/Work/Do-an/src/preprocessing/cleaner.py) | Phương pháp phòng thủ bằng xáo trộn ngẫu nhiên (Randomized Smoothing) và đối chuẩn hiệu năng phòng ngự với PI-Guard |
| <a id="ref15"></a>**15** | [`Jain_2023_Baseline_Defenses_Adversarial_Attacks_LLMs.pdf`](file:///d:/Work/Do-an/reports/References/Jain_2023_Baseline_Defenses_Adversarial_Attacks_LLMs.pdf) | [Jain et al. (2023)](https://arxiv.org/abs/2309.00614) | *arXiv 2023 (Univ of Maryland)* | • [`docs/research/State_of_the_Art_Guardrail_and_Jailbreak_Benchmarks_Analysis.md`](file:///d:/Work/Do-an/docs/research/State_of_the_Art_Guardrail_and_Jailbreak_Benchmarks_Analysis.md)<br>• [`docs/prompt_study/01_llm_foundations_and_token_generation.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/prompt_study/01_llm_foundations_and_token_generation.md)<br>• [`reports/PI-GUARD-Present-109.pptx`](file:///d:/Work/Do-an/reports/PI-GUARD-Present-109.pptx)<br>• [`notebooks/02_baseline.ipynb`](file:///d:/Work/Do-an/notebooks/02_baseline.ipynb) | **Trụ cột An ninh 1**: Cơ sở khoa học của Lọc cú pháp Baseline kết hợp Word/Char n-grams kháng phân mảnh token và Leetspeak/Spacing |
| <a id="ref16"></a>**16** | [`Yao_2022_ZeroQuant_Efficient_Post_Training_Quantization_Transformers.pdf`](file:///d:/Work/Do-an/reports/References/Yao_2022_ZeroQuant_Efficient_Post_Training_Quantization_Transformers.pdf) | [Yao et al. (2022)](https://arxiv.org/abs/2206.01861) | *NeurIPS 2022 (Microsoft)* | • [`docs/optimization_study/01_quantization_theory_and_ptq_math.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/optimization_study/01_quantization_theory_and_ptq_math.md)<br>• [`docs/optimization_study/02_onnx_runtime_and_graph_optimizations.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/optimization_study/02_onnx_runtime_and_graph_optimizations.md)<br>• [`reports/PI-GUARD-Present-109.pptx`](file:///d:/Work/Do-an/reports/PI-GUARD-Present-109.pptx)<br>• [`src/models/classifier.py`](file:///d:/Work/Do-an/src/models/classifier.py) | *Kỹ thuật phụ trợ triển khai*: Cơ sở kỹ thuật của Lượng hóa động INT8 Post-Training Quantization (PTQ) cho Transformer, hỗ trợ thực thi trên CPU với độ trễ thấp |
| <a id="ref17"></a>**17** | [`Yuan_2024_GPT4_Too_Smart_To_Be_Safe_Cipher_Jailbreak.pdf`](file:///d:/Work/Do-an/reports/References/Yuan_2024_GPT4_Too_Smart_To_Be_Safe_Cipher_Jailbreak.pdf) | [Yuan et al. (2024)](https://arxiv.org/abs/2308.06463) | *ICLR 2024* | • [`docs/thesis/Review1_Problem_Definition_and_Threat_Model.md`](file:///d:/Work/Do-an/docs/thesis/Review1_Problem_Definition_and_Threat_Model.md)<br>• [`src/preprocessing/cleaner.py`](file:///d:/Work/Do-an/src/preprocessing/cleaner.py)<br>• [`tests/adversarial/encoding/`](file:///d:/Work/Do-an/tests/adversarial/encoding/) | **Kháng Mã Hóa Lẩn Tránh**: Nghiên cứu đột phá chứng minh mã hóa Base64/Cipher vượt rào kiểm duyệt LLM và cơ chế đánh chặn tiền trạm |
| <a id="ref18"></a>**18** | [`Saltzer_1975_The_Protection_of_Information_in_Computer_Systems.pdf`](file:///d:/Work/Do-an/reports/References/Saltzer_1975_The_Protection_of_Information_in_Computer_Systems.pdf) | [Saltzer & Schroeder (1975)](https://web.mit.edu/Saltzer/www/publications/protection/) | *Proc. IEEE 1975* | • [`docs/threat_and_defense_study/02_multi_layer_defense_architecture.md`](file:///d:/Work/Do-an/docs/threat_and_defense_study/02_multi_layer_defense_architecture.md)<br>• [`reports/PI-GUARD-Present-109.pptx`](file:///d:/Work/Do-an/reports/PI-GUARD-Present-109.pptx)<br>• [`workspaces/truongnv/reports/SUPERVISOR_REPORT_10_09_2026.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/SUPERVISOR_REPORT_10_09_2026.md) | **Nguyên lý Thiết kế Hệ thống**: Nền tảng kinh điển về Phòng thủ chiều sâu (Defense-in-Depth), Kiểm duyệt toàn vẹn (Complete Mediation) và cơ sở thiết kế kiến trúc Two-Tier Cascaded Guardrail |

---

## 🎯 2. DANH MỤC 8 BÀI BÁO TRỌNG TÂM DÙNG TRONG SLIDE `reports/PI-GUARD-Present-109.pptx`

Tất cả 8 công trình khoa học nền tảng được chọn lọc trình chiếu tại buổi làm việc với GVHD (10/09/2026) được hệ thống hóa tại Slide 21:

| # | Tài Liệu Báo Cáo | Tác Giả & Năm | Tên Công Trình & Nơi Công Bố | Tệp PDF Cục Bộ | Nhóm Chuyên Đề Nghiên Cứu |
| :-: | :-: | :--- | :--- | :--- | :--- |
| 1 | [PI-GUARD-Present-109.pptx](file:///d:/Work/Do-an/reports/PI-GUARD-Present-109.pptx) | Perez & Ribeiro (2022) | *Ignore Previous Prompt: Attack Techniques For Language Models* (NeurIPS ML Safety Workshop 2022) | [`Perez_2022_Ignore_This_Title_Hack_This_Paper_Prompt_Injection.pdf`](file:///d:/Work/Do-an/reports/References/Perez_2022_Ignore_This_Title_Hack_This_Paper_Prompt_Injection.pdf) | **Group 1**: Attack Mechanisms & Threat Surface |
| 2 | [PI-GUARD-Present-109.pptx](file:///d:/Work/Do-an/reports/PI-GUARD-Present-109.pptx) | Shen et al. (2024) | *"Do Anything Now": Characterizing and Evaluating In-The-Wild Jailbreak Prompts on Large Language Models* (ACM CCS '24) | [`Shen_2024_Do_Anything_Now_Jailbreak_Prompts_In_The_Wild.pdf`](file:///d:/Work/Do-an/reports/References/Shen_2024_Do_Anything_Now_Jailbreak_Prompts_In_The_Wild.pdf) | **Group 1**: Attack Mechanisms & Threat Surface |
| 3 | [PI-GUARD-Present-109.pptx](file:///d:/Work/Do-an/reports/PI-GUARD-Present-109.pptx) | Greshake et al. (2023) | *Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection* (ACM AISec '23) | [`Greshake_2023_Indirect_Prompt_Injection.pdf`](file:///d:/Work/Do-an/reports/References/Greshake_2023_Indirect_Prompt_Injection.pdf) | **Group 1**: Attack Mechanisms & Threat Surface |
| 4 | [PI-GUARD-Present-109.pptx](file:///d:/Work/Do-an/reports/PI-GUARD-Present-109.pptx) | Tencent Zhuque Lab (2026) | *AI-Infra-Guard: Multi-Layer Attack Surface and Defense Framework for AI Agents* (Tencent Security Tech Report 2026) | [`Tencent_2026_AI_Infra_Guard_MultiLayer_Agent_RedTeaming.pdf`](file:///d:/Work/Do-an/reports/References/Tencent_2026_AI_Infra_Guard_MultiLayer_Agent_RedTeaming.pdf) | **Group 1**: Attack Mechanisms & Threat Surface |
| 5 | [PI-GUARD-Present-109.pptx](file:///d:/Work/Do-an/reports/PI-GUARD-Present-109.pptx) | Jain et al. (2023) | *Baseline Defenses for Adversarial Attacks Against Aligned Language Models* (arXiv:2309.00614) | [`Jain_2023_Baseline_Defenses_Adversarial_Attacks_LLMs.pdf`](file:///d:/Work/Do-an/reports/References/Jain_2023_Baseline_Defenses_Adversarial_Attacks_LLMs.pdf) | **Group 2**: Guardrail Architecture & Evaluation |
| 6 | [PI-GUARD-Present-109.pptx](file:///d:/Work/Do-an/reports/PI-GUARD-Present-109.pptx) | He et al. (2021/2023) | *DeBERTa: Decoding-enhanced BERT with Disentangled Attention* (ICLR 2021 / 2023) | [`He_2023_DeBERTaV3_Disentangled_Attention_ICLR.pdf`](file:///d:/Work/Do-an/reports/References/He_2023_DeBERTaV3_Disentangled_Attention_ICLR.pdf) | **Group 2**: Guardrail Architecture & Evaluation |
| 7 | [PI-GUARD-Present-109.pptx](file:///d:/Work/Do-an/reports/PI-GUARD-Present-109.pptx) | Yao et al. (2022) | *ZeroQuant: Efficient and Affordable Post-Training Quantization for Large-Scale Transformers* (NeurIPS 2022) | [`Yao_2022_ZeroQuant_Efficient_Post_Training_Quantization_Transformers.pdf`](file:///d:/Work/Do-an/reports/References/Yao_2022_ZeroQuant_Efficient_Post_Training_Quantization_Transformers.pdf) | **Group 2**: Guardrail Architecture & Evaluation |
| 8 | [PI-GUARD-Present-109.pptx](file:///d:/Work/Do-an/reports/PI-GUARD-Present-109.pptx) | Saltzer & Schroeder (1975) | *The Protection of Information in Computer Systems* (Proceedings of the IEEE, vol. 63, no. 9, Sept. 1975) | [`Saltzer_1975_The_Protection_of_Information_in_Computer_Systems.pdf`](file:///d:/Work/Do-an/reports/References/Saltzer_1975_The_Protection_of_Information_in_Computer_Systems.pdf) | **Group 2**: Guardrail Architecture & Evaluation |

---

## 📑 3. BIBTEX ENTRIES CẬP NHẬT ĐẦY ĐỦ

```bibtex
@inproceedings{perez2022ignore,
  title     = {Ignore Previous Prompt: Attack Techniques For Language Models},
  author    = {Perez, F{\'a}bio and Ribeiro, Ian},
  booktitle = {NeurIPS ML Safety Workshop},
  year      = {2022},
  url       = {https://arxiv.org/abs/2211.09527}
}

@inproceedings{shen2024dan,
  title     = {"Do Anything Now": Characterizing and Evaluating In-The-Wild Jailbreak Prompts on Large Language Models},
  author    = {Shen, Xinyue and Chen, Zeyuan and Backes, Michael and Shen, Yun and Zhang, Yang},
  booktitle = {Proceedings of the 2024 ACM SIGSAC Conference on Computer and Communications Security (ACM CCS '24)},
  pages     = {4172--4186},
  year      = {2024},
  doi       = {10.1145/3658644.3670390}
}

@inproceedings{greshake2023indirect,
  title     = {Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection},
  author    = {Greshake, Kai and Abdelnabi, Sahar and Mishra, Shailesh and Endres, Christoph and Holz, Thorsten and Fritz, Mario},
  booktitle = {Proceedings of the 16th ACM Workshop on Artificial Intelligence and Security (ACM AISec '23)},
  pages     = {79--90},
  year      = {2023},
  doi       = {10.1145/3605764.3623982}
}

@techreport{tencent2026aiinfraguard,
  title       = {AI-Infra-Guard: Multi-Layer Attack Surface and Defense Framework for AI Agents},
  author      = {{Tencent Zhuque Lab}},
  institution = {Tencent Security},
  year        = {2026},
  url         = {https://arxiv.org/abs/2606.31227}
}

@article{jain2023baseline,
  title   = {Baseline Defenses for Adversarial Attacks Against Aligned Language Models},
  author  = {Jain, Neel and Schwarzschild, Avi and Wen, Yuxin and Thattai, Gowthami and Thickstun, John and Goldstein, Tom},
  journal = {arXiv preprint arXiv:2309.00614},
  year    = {2023}
}

@inproceedings{he2023deberta,
  title     = {DeBERTa: Decoding-enhanced BERT with Disentangled Attention},
  author    = {He, Pengcheng and Liu, Xiaodong and Gao, Jianfeng and Chen, Weizhu},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year      = {2021}
}

@inproceedings{yao2022zeroquant,
  title     = {ZeroQuant: Efficient and Affordable Post-Training Quantization for Large-Scale Transformers},
  author    = {Yao, Zhewei and Aminabadi, Reza Yazdani and Zhang, Minjia and Wu, Xiaoxia and Li, Conglong and He, Yuxiong},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  volume    = {35},
  pages     = {27168--27183},
  year      = {2022}
}

@article{saltzer1975protection,
  title   = {The Protection of Information in Computer Systems},
  author  = {Saltzer, Jerome H. and Schroeder, Michael D.},
  journal = {Proceedings of the IEEE},
  volume  = {63},
  number  = {9},
  pages   = {1278--1308},
  year    = {1975},
  doi     = {10.1109/PROC.1975.9939}
}
```
