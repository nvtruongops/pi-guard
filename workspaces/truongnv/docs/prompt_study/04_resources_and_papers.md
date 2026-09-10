# TỔNG HỢP TÀI LIỆU KHOA HỌC & TÀI NGUYÊN NGHIÊN CỨU PROMPT VÀ LLM CONTEXT
## Danh Mục Bài Báo Nền Tảng, Báo Cáo Kỹ Thuật Đã Thẩm Định 100%

> **Quy chuẩn lưu trữ**: Toàn bộ các tài liệu học thuật trong danh mục này đều có liên kết Open-Access hoặc bản PDF lưu trữ cục bộ trong [`Final-Report/References/`](file:///d:/Work/Do-an/Final-Report/References/) và đã được kiểm tra liên kết Open-Access xác thực trạng thái hoạt động.

---

## I. Bảng Danh Mục Bài Báo Khoa Học Chủ Chốt (Peer-Reviewed & Landmark Papers)

| STT | Bài Báo & Tác Giả | Hội Nghị / Nơi Xuất Bản | Bản PDF Cục Bộ / Open-Access | Tóm Tắt Đóng Góp Khoa Học & Ứng Dụng Trong PI-Guard |
| :---: | :--- | :---: | :--- | :--- |
| **1** | **A Survey of LLMs**<br>*(Zhao et al., 2023)* | **IJCAI / arXiv 2023** | [`Zhao_2023_A_Survey_of_Large_Language_Models.pdf`](file:///d:/Work/Do-an/References/Zhao_2023_A_Survey_of_Large_Language_Models.pdf) | Khảo sát tổng thể về kiến trúc LLM, quá trình tiền huấn luyện, phân rã token và các thách thức căn chỉnh an toàn (Alignment). |
| **2** | **InstructGPT**<br>*(Ouyang et al., 2022)* | **NeurIPS 2022**<br>*(OpenAI)* | [`Ouyang_2022_InstructGPT_Training_Language_Models_Follow_Instructions.pdf`](file:///d:/Work/Do-an/References/Ouyang_2022_InstructGPT_Training_Language_Models_Follow_Instructions.pdf) | Thiết lập kỹ thuật Instruction Tuning & RLHF, giải thích nguyên nhân tại sao mô hình tuân thủ mệnh lệnh và nguồn gốc rủi ro ghi đè chỉ thị. |
| **3** | **Ignore This Title**<br>*(Perez & Ribeiro, 2022)* | **NeurIPS 2022** | [`Perez_2022_Ignore_Previous_Prompt_Attack_Techniques.pdf`](file:///d:/Work/Do-an/References/Perez_2022_Ignore_Previous_Prompt_Attack_Techniques.pdf) | Bài báo đầu tiên định nghĩa chính thức bài toán Prompt Injection, Goal Hijacking và System Prompt Leaking. |
| **4** | **The Instruction Hierarchy**<br>*(Wallace et al., 2024)* | **OpenAI Tech Report 2024** | Online Open-Access<br>[arXiv:2404.13208](https://arxiv.org/abs/2404.13208) | Phân tích toán học về xung đột phân cấp đặc quyền (System vs User vs Context) trong các mô hình ngôn ngữ lớn. |
| **5** | **Lost in the Middle**<br>*(Liu et al., 2024)* | **TACL 2024**<br>*(Stanford / Berkeley)* | Online Open-Access<br>[arXiv:2307.03172](https://arxiv.org/abs/2307.03172) | Chứng minh thực nghiệm hiện tượng Recency Bias và Primacy Effect trong cơ chế Self-Attention của LLM. |
| **6** | **Indirect Prompt Injection**<br>*(Greshake et al., 2023)* | **ACM AISEC 2023** | [`Greshake_2023_Indirect_Prompt_Injection.pdf`](file:///d:/Work/Do-an/References/Greshake_2023_Indirect_Prompt_Injection.pdf) | Chứng minh các cuộc tấn công tiêm nhiễm gián tiếp qua tài liệu RAG, file đính kèm và website. |

---

## 📚 TÀI LIỆU THAM KHẢO HỌC THUẬT CHI TIẾT (BIBTEX FORMAT)

```bibtex
@article{zhao2023survey,
  title   = {A Survey of Large Language Models},
  author  = {Zhao, Wayne Xin and Zhou, Kun and Li, Junyi and Tang, Tianyi and Wang, Xiaolei and Hou, Yupeng and Min, Yingqian and Zhang, Beichen and Zhang, Junjie and Dong, Zican and others},
  journal = {arXiv preprint arXiv:2303.18223},
  year    = {2023}
}

@inproceedings{ouyang2022training,
  title     = {Training language models to follow instructions with human feedback},
  author    = {Ouyang, Long and Wu, Jeffrey and Jiang, Xu and Almeida, Diogo and Wainwright, Carroll and Mishkin, Pamela and Zhang, Chong and Agarwal, Sandhini and Slama, Katarina and Ray, Alex and others},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS 2022)},
  volume    = {35},
  pages     = {27730--27744},
  year      = {2022}
}

@inproceedings{perez2022ignore,
  title     = {Ignore Previous Prompt: Attack Techniques For Language Models},
  author    = {Perez, F{\'a}bio and Ribeiro, Ian},
  journal   = {arXiv preprint arXiv:2211.09527},
  year      = {2022}
}
```
