# NHẬT KÝ TÀI LIỆU NGHIÊN CỨU & KHẢO SÁT HỌC THUẬT (ĐỖ ĐOÀN DUY PHƯƠNG)
## TẬP TRUNG TÀI LIỆU KHẢO SÁT & ĐỐI CHIẾU CÙNG NHÓM (AI CŨNG LÀM $\rightarrow$ THAM KHẢO NHAU $\rightarrow$ CHỐT KẾT QUẢ)

**Thành viên**: Đỗ Đoàn Duy Phương (MSSV: `SE180235`)  
**Mục tiêu chính**: Khảo sát toàn diện bối cảnh tấn công Jailbreak & Prompt Injection, xây dựng bộ phân loại chiến thuật đối kháng cho Chương 2 Luận văn, và tích hợp luồng xử lý trung gian bảo vệ API LLM.  
**Căn cứ cuộc họp**: Biên bản [`Meeting/Meeting 2_01_09_26.md`](file:///d:/Work/Do-an/Meeting/Meeting%202_01_09_26.md)  

---

## 📚 I. DANH MỤC BÀI BÁO KHOA HỌC THỰC TẾ TRONG WORKSPACE

| STT | Tác Giả & Năm | Tên Công Trình Khoa Học | File PDF Cục Bộ | Thẩm Định & Đóng Góp Cho Đề Tài PI-Guard |
| :---: | :--- | :--- | :--- | :--- |
| 1 | **Greshake et al. (2023)** | *Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection* (ACM AISec 2023) | [`Greshake_2023_Indirect_Prompt_Injection.pdf`](file:///d:/Work/Do-an/workspaces/phuongddd/References/Greshake_2023_Indirect_Prompt_Injection.pdf) | 👉 **GIỮ LẠI (IN-SCOPE)**: Đặt nền móng chứng minh dữ liệu ngoài (Web, PDF, RAG) bản chất đều là chuỗi chỉ thị không tin cậy. Dùng cho Chương 1 và Chương 2. |
| 2 | **Wei et al. (2024)** | *Jailbroken: How Does LLM Safety Training Fail?* (NeurIPS 2023) | [`Wei_2024_Jailbroken_How_LLM_Safety_Training_Fails.pdf`](file:///d:/Work/Do-an/workspaces/phuongddd/References/Wei_2024_Jailbroken_How_LLM_Safety_Training_Fails.pdf) | ❌ **LOẠI BỎ (OUT-OF-SCOPE)**: Phân tích sự xung đột mục tiêu (Competing Objectives) và không tương thích (Mismatched Generalization) trong trọng số weights LLM. Đề tài PI-Guard làm guardrail ngoài cổng API, không can thiệp nội tại LLM. |
| 3 | **Zou et al. (2023)** | *Universal and Transferable Adversarial Attacks on Aligned Language Models* (arXiv:2307.15043) | [`Zou_2023_Universal_Transferable_Adversarial_Attacks_GCG.pdf`](file:///d:/Work/Do-an/workspaces/phuongddd/References/Zou_2023_Universal_Transferable_Adversarial_Attacks_GCG.pdf) | 👉 **GIỮ LẠI 1 PHẦN**: Lấy kho adversarial suffix để làm tập mẫu tấn công thử nghiệm độ bền; không triển khai thuật toán tính gradient tối ưu hóa trực tiếp ở runtime. |
| 4 | **ACL Findings (2024)** | *A Comprehensive Study of Jailbreak Attack versus Defense for Large Language Models* (ACL 2024) | [`Phuong_2024_ACL_Comprehensive_Study_Jailbreak_Attack_Defense.pdf`](file:///d:/Work/Do-an/workspaces/phuongddd/References/Phuong_2024_ACL_Comprehensive_Study_Jailbreak_Attack_Defense.pdf) | 👉 **GIỮ LẠI (IN-SCOPE)**: Cung cấp taxonomy toàn cảnh về tấn công và phòng thủ jailbreak phục vụ biên soạn bảng đối sánh cho Chương 2 (Literature Review). |
| 5 | **Survey (2024)** | *Jailbreak Attacks and Defenses Against Large Language Models: A Survey* (arXiv:2407.04295) | [`Phuong_2024_Survey_Jailbreak_Attacks_Defenses_LLMs.pdf`](file:///d:/Work/Do-an/workspaces/phuongddd/References/Phuong_2024_Survey_Jailbreak_Attacks_Defenses_LLMs.pdf) | 👉 **GIỮ LẠI (IN-SCOPE)**: Tham khảo cơ chế phòng vệ hộp đen (Black-box defenses), bộ tiêu chí đánh giá độ trễ và tỷ lệ chặn nhầm (FPR). |
| 6 | **Do-Not-Answer (2023)** | *A Dataset for Evaluating Safeguards in LLMs* (arXiv:2308.13387) | [`Phuong_2023_Do_Not_Answer_Dataset_Evaluating_Safeguards.pdf`](file:///d:/Work/Do-an/workspaces/phuongddd/References/Phuong_2023_Do_Not_Answer_Dataset_Evaluating_Safeguards.pdf) | 👉 **GIỮ LẠI (IN-SCOPE)**: Cung cấp tập dữ liệu mẫu độc hại và luận điểm then chốt: *Mô hình nhỏ phân loại chuyên biệt có thể đạt độ chính xác đánh giá an toàn tương đương GPT-4*. |
| 7 | **Survey (2024)** | *Exploring Vulnerabilities and Protections in Large Language Models: A Survey* (arXiv:2406.00240) | [`Phuong_2024_Exploring_Vulnerabilities_Protections_LLMs_Survey.pdf`](file:///d:/Work/Do-an/workspaces/phuongddd/References/Phuong_2024_Exploring_Vulnerabilities_Protections_LLMs_Survey.pdf) | 👉 **GIỮ LẠI (IN-SCOPE)**: Bổ sung 3 chiến thuật Jailbreak (*Pretending, Attention Shifting, Privilege Escalation*) và 3 kỹ thuật Black-box (*RAP, ONION, MDP*). |

---

## 🔬 II. KẾT QUẢ SÀNG LỌC & KẾ HOẠCH DỰ ÁN
1. **Ranh giới đề tài rõ ràng**: Loại bỏ các nghiên cứu đòi hỏi can thiệp vào trọng số LLM (như paper của Wei et al.) hoặc tính toán gradient phức tạp thời gian thực (Zou et al.). Toàn bộ giải pháp tập trung vào **API Gateway Guardrail bất khả tri (Agnostic Guardrail)**.
2. **Chuẩn bị hồ sơ Review 1**:
   - Dùng các phát hiện từ Do-Not-Answer và ACL 2024 để bảo vệ luận điểm chọn DeBERTa-v3 + TF-IDF trước Hội đồng chấm.
   - Cập nhật các trích dẫn chuẩn IEEE vào Chương 1 & Chương 2 của Luận văn.
