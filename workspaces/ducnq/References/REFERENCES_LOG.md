# NHẬT KÝ TÀI LIỆU NGHIÊN CỨU & KHẢO SÁT HỌC THUẬT (NGUYỄN QUÍ ĐỨC)
## TẬP TRUNG TÀI LIỆU KHẢO SÁT & ĐỐI CHIẾU CÙNG NHÓM (AI CŨNG LÀM $\rightarrow$ THAM KHẢO NHAU $\rightarrow$ CHỐT KẾT QUẢ)

**Thành viên**: Nguyễn Quí Đức (MSSV: `SE182087`)  
**Mục tiêu chính**: Nghiên cứu mô hình lọc cú pháp siêu nhanh (TF-IDF + LinearSVC/LogisticRegression), thuật toán biến dị kiểm thử độ bền (Targeted Mutators từ JailGuard), và các kỹ thuật phòng thủ đối kháng nền tảng.  
**Căn cứ cuộc họp**: Biên bản [`Meeting/Meeting 2_01_09_26.md`](file:///d:/Work/Do-an/Meeting/Meeting%202_01_09_26.md)  

---

## 📚 I. DANH MỤC BÀI BÁO KHOA HỌC THỰC TẾ TRONG WORKSPACE

| STT | Tác Giả & Năm | Tên Công Trình Khoa Học | File PDF Cục Bộ | Thẩm Định & Đóng Góp Cho Đề Tài PI-Guard |
| :---: | :--- | :--- | :--- | :--- |
| 1 | **Zhang et al. (2025)** | *JailGuard: A Universal Detection Framework for LLM Prompt-based Attacks* (ACM TOSEM 2025 / arXiv:2312.10766) | [`Duc_2025_JailGuard_Universal_Detection_Framework_TOSEM.pdf`](file:///d:/Work/Do-an/workspaces/ducnq/References/Duc_2025_JailGuard_Universal_Detection_Framework_TOSEM.pdf) | 👉 **GIỮ LẠI 1 PHẦN**: Tham khảo **Algorithm 1 (Targeted Mutators Workflow)** để thiết kế các bộ biến dị ký tự (Leetspeak, Base64, Spacing) kiểm thử độ bền hệ thống; ❌ *Loại bỏ* phần Multi-Modal (Ảnh/Video) và cơ chế online multi-pass (gây độ trễ > 3s). |
| 2 | **Jain et al. (2023)** | *Baseline Defenses for Adversarial Attacks on Large Language Models* (arXiv:2309.00614) | [`Jain_2023_Baseline_Defenses_Adversarial_Attacks_LLMs.pdf`](file:///d:/Work/Do-an/workspaces/ducnq/References/Jain_2023_Baseline_Defenses_Adversarial_Attacks_LLMs.pdf) | 👉 **CỐT LÕI (CORE)**: Cung cấp cơ sở lý thuyết so sánh hiệu quả giữa tiền xử lý văn bản (Perplexity filter, Re-tokenization) và các bộ lọc từ khóa/n-grams truyền thống. |
| 3 | **Robey et al. (2023)** | *SmoothLLM: Defending Large Language Models Against Jailbreaking Attacks* (arXiv:2310.03684) | [`Robey_2023_SmoothLLM_Defending_LLMs_Random_Perturbation.pdf`](file:///d:/Work/Do-an/workspaces/ducnq/References/Robey_2023_SmoothLLM_Defending_LLMs_Random_Perturbation.pdf) | 👉 **THAM KHẢO**: Nghiên cứu về độ bền trước nhiễu loạn ngẫu nhiên (Random Character Perturbations), định hướng cho bộ trích xuất đặc trưng Character n-grams TF-IDF. |

---

## 🔬 II. KẾT QUẢ SÀNG LỌC & KẾ HOẠCH THỰC HIỆN
1. **Tiếp thu thuật toán Targeted Mutators từ JailGuard**: Thiết kế bộ sinh mẫu đối kháng tự động trong `src/preprocessing/cleaner.py` và `tests/adversarial/` nhằm đánh giá khả năng phòng thủ của hệ thống trước các biến thể xáo trộn văn bản.
2. **Kế hoạch ML Baseline**:
   - Xây dựng pipeline Character n-grams TF-IDF kết hợp LinearSVC để xử lý nhanh 85% traffic đầu vào với độ trễ P95 $< 3\text{ms}$.
   - Tối ưu hóa ma trận nhầm lẫn (Confusion Matrix) và giữ tỷ lệ cảnh báo sai (FPR) dưới 1.5%.
