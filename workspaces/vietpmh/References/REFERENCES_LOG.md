# NHẬT KÝ TÀI LIỆU NGHIÊN CỨU & KHẢO SÁT HỌC THUẬT (PHẠM MINH HOÀNG VIỆT)
## TẬP TRUNG TÀI LIỆU KHẢO SÁT & ĐỐI CHIẾU CÙNG NHÓM (AI CŨNG LÀM $\rightarrow$ THAM KHẢO NHAU $\rightarrow$ CHỐT KẾT QUẢ)

**Thành viên**: Phạm Minh Hoàng Việt (MSSV: `SE181851`)  
**Mục tiêu chính**: Nghiên cứu kiến trúc Transformer `microsoft/deberta-v3-base` (Disentangled Attention), kỹ thuật lượng hóa động ONNX INT8 Runtime (ZeroQuant), đánh giá độ bền trước tấn công gián tiếp (BIPIA) và cơ chế Attention Shift (RAP-ID).  
**Căn cứ cuộc họp**: Biên bản [`Meeting/Meeting 2_01_09_26.md`](file:///d:/Work/Do-an/Meeting/Meeting%202_01_09_26.md)  

---

## 📚 I. DANH MỤC BÀI BÁO KHOA HỌC THỰC TẾ TRONG WORKSPACE

| STT | Tác Giả & Năm | Tên Công Trình Khoa Học | File PDF Cục Bộ | Thẩm Định & Đóng Góp Cho Đề Tài PI-Guard |
| :---: | :--- | :--- | :--- | :--- |
| 1 | **RAP-ID (2026)** | *Robust Alignment Preservation via Injection Defense* (ACL Findings 2026) | [`Viet_2026_RAP_ID_Robust_Alignment_Preservation_Injection_Defense.pdf`](file:///d:/Work/Do-an/workspaces/vietpmh/References/Viet_2026_RAP_ID_Robust_Alignment_Preservation_Injection_Defense.pdf) | 👉 **GIỮ LẠI (IN-SCOPE)**: Cung cấp cơ sở toán học về cơ chế *Pre-fill pass* (Directive Likeness, Counterfactual Gain, Policy Conflict) và hiện tượng Attention Shift khi bị inject prompt. |
| 2 | **BIPIA (2024)** | *Benchmarking and Defending Against Indirect Prompt Injection Attacks on LLMs* (ACM KDD 2025) | [`Viet_2024_BIPIA_Benchmarking_Indirect_Prompt_Injection_Attacks.pdf`](file:///d:/Work/Do-an/workspaces/vietpmh/References/Viet_2024_BIPIA_Benchmarking_Indirect_Prompt_Injection_Attacks.pdf) | 👉 **GIỮ LẠI (IN-SCOPE)**: Cung cấp bộ benchmark chuẩn và tập dữ liệu Indirect Prompt Injection để kiểm thử độ bền hệ thống. |
| 3 | **He et al. (2023)** | *DeBERTaV3: Improving DeBERTa using ELECTRA-Style Pre-Training with Disentangled Attention* (ICLR 2023) | [`He_2023_DeBERTaV3_Disentangled_Attention_ICLR.pdf`](file:///d:/Work/Do-an/workspaces/vietpmh/References/He_2023_DeBERTaV3_Disentangled_Attention_ICLR.pdf) | 👉 **CỐT LÕI (CORE)**: Kiến trúc Transformer 86M tham số phân tách vector nội dung $H$ và vector vị trí tương đối $P$ làm lõi phân loại ngữ nghĩa sâu cho PI-Guard. |
| 4 | **Yao et al. (2022)** | *ZeroQuant: Efficient and Affordable Post-Training Quantization for Large-Scale Transformers* (NeurIPS 2022) | [`Yao_2022_ZeroQuant_Efficient_Post_Training_Quantization_Transformers.pdf`](file:///d:/Work/Do-an/workspaces/vietpmh/References/Yao_2022_ZeroQuant_Efficient_Post_Training_Quantization_Transformers.pdf) | 👉 **CỐT LÕI (CORE)**: Thuật toán lượng hóa động Post-Training INT8 tối ưu hóa bộ nhớ xuống $< 150\text{MB}$ và độ trễ P95 $< 15\text{ms}$ trên CPU. |

---

## 🔬 II. CÁC ĐIỂM RÚT RA TỪ CUỘC HỌP MEETING 2
1. **Khẳng định tính khả thi của mô hình nhỏ (< 600M tham số)**: Kết quả từ các bài báo chỉ ra rằng mô hình DeBERTa-v3 86M được tinh chỉnh chuyên biệt trên tập dữ liệu đối kháng có thể đạt Macro $F_1 \ge 0.95$, ngang ngửa hoặc vượt trội các mô hình LLM lớn 8B làm judge nhưng có độ trễ nhanh hơn 50 lần.
2. **Kế hoạch thực nghiệm**:
   - Tuần 5–6: Chuẩn bị dữ liệu và fine-tuning DeBERTa-v3 trên GPU Colab/Kaggle.
   - Tuần 9–10: Xuất mô hình sang định dạng ONNX INT8 và đo đạc độ trễ CPU trên tập test BIPIA.
