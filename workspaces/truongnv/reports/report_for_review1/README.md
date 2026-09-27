# PHÂN HỆ HỒ SƠ BÁO CÁO REVIEW 1 (REPORT NO. 1 & REPORT NO. 2)
## Đồ án Tốt nghiệp: PI-Guard (`IAP491_FA26_PI_GUARD`) — Đại học FPT

---

### 📌 THÔNG TIN CỘT MỐC REVIEW 1
- **Cột mốc**: **REVIEW 1** *(Tuần 4 / 15 Tuần — Học kỳ Fall 2026)*
- **Báo cáo tích hợp**:
  - **Report No. 1**: Chapter 1 — Introduction *(Trọng số 10% Process Mark)*
  - **Report No. 2**: Chapter 2 — Literature Review & Threat Modeling *(Trọng số 25% Process Mark)*
- **Tổng trọng số điểm quá trình**: **35% Process Mark** (17.5% tổng điểm đồ án)
- **Người thực hiện**: Nguyễn Văn Trường (Leader - `SE182034`) & Nhóm đồ án PI-Guard
- **Giảng viên hướng dẫn**: ThS. Trần Văn Ninh

---

## 📂 CHỈ MỤC TÀI LIỆU TRONG PHÂN HỆ

| Tệp tài liệu | Mô tả nội dung kỹ thuật | Định dạng | Trạng thái |
| :--- | :--- | :---: | :---: |
| [`REVIEW_1_REPORT.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/report_for_review1/REVIEW_1_REPORT.md) | **BÁO CÁO TOÀN VĂN REVIEW 1 CHÍNH THỨC**<br/>• Chapter 1: Introduction (1.1 - 1.6)<br/>• Chapter 2: Literature Review (2.1 - 2.3 & 17 trích dẫn IEEE)<br/>• Chuyên đề Đánh giá 7 tiêu chí cốt lõi của Hội đồng | Markdown (91 KB) | **ĐÃ HOÀN THÀNH** |

### 🔗 Liên Kết Đến Các Tài Nguyên Liên Quan Trong Workspace:
- **Chương luận văn độc lập**:
  - [`docs/thesis/chapters/01_Introduction.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/thesis/chapters/01_Introduction.md): Bản thảo Chapter 1
  - [`docs/thesis/chapters/02_Literature_Review.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/thesis/chapters/02_Literature_Review.md): Bản thảo Chapter 2
  - [`docs/thesis/Review1_Problem_Definition_and_Threat_Model.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/thesis/Review1_Problem_Definition_and_Threat_Model.md): Hồ sơ kỹ thuật Threat Model ban đầu
- **Slide thuyết trình & Biên bản họp**:
  - [`reports/report_for_meeting_4/PI-GUARD-Present-109.pptx`](file:///d:/Work/Do-an/workspaces/truongnv/reports/report_for_meeting_4/PI-GUARD-Present-109.pptx): Slide báo cáo tiến độ gặp GVHD
  - [`reports/report_for_meeting_4/SUPERVISOR_REPORT_10_09_2026.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/report_for_meeting_4/SUPERVISOR_REPORT_10_09_2026.md): Kịch bản báo cáo GVHD
- **Danh mục 18 bài báo chuẩn mực**:
  - [`References/REFERENCES_LOG.md`](file:///d:/Work/Do-an/workspaces/truongnv/References/REFERENCES_LOG.md): Bảng ma trận tài liệu tham khảo cục bộ

---

## 🎯 TÓM TẮT ĐIỀU HÀNH: 7 TIÊU CHÍ ĐÁNH GIÁ REVIEW 1

```
┌────────────────────────────────────────────────────────────────────────┐
│               TÓM LƯỢC 7 NỘI DUNG ĐÁNH GIÁ REVIEW 1                    │
├────────────────────────────────────────────────────────────────────────┤
│ 1. PROBLEM STATEMENT    │ Lỗ hổng Von Neumann trong NLP: X = S || U    │
│                         │ Lẫn lộn ranh giới Lệnh (S) và Dữ liệu (U)    │
├─────────────────────────┼──────────────────────────────────────────────┤
│ 2. RESEARCH QUESTIONS   │ 3 RQs chuẩn IEEE: RQ1 (Data Leakage & Split),│
│                         │ RQ2 (Robustness & Ciphers), RQ3 (FPR & Delay)│
├─────────────────────────┼──────────────────────────────────────────────┤
│ 3. RESEARCH OBJECTIVES  │ F1 >= 0.95, FPR < 1.5%, P95 < 30ms trên CPU  │
│                         │ Phân rã thành 5 hạng mục bàn giao cụ thể     │
├─────────────────────────┼──────────────────────────────────────────────┤
│ 4. PROPOSED SOLUTION    │ Two-Tier Cascade: Tier-1 TF-IDF char_wb (~3ms│
│                         │ + Tier-2 DeBERTa-v3 (~12.8ms) & Tri-State    │
├─────────────────────────┼──────────────────────────────────────────────┤
│ 5. BOUNDARY             │ In-scope: English Text Prompts, Black-box REST│
│                         │ Out-of-scope: Multimodal, GPU internal weights│
├─────────────────────────┼──────────────────────────────────────────────┤
│ 6. FEASIBILITY PROOF    │ 45k+ samples Group-Aware Split, 5 upstream   │
│                         │ models replicated, FastAPI + Streamlit Demo  │
├─────────────────────────┼──────────────────────────────────────────────┤
│ 7. IMPLEMENT PROGRESS   │ Tuần 4/15 (26.7% thời gian)                  │
│                         │ Khối lượng hoàn thành: ~33.0% (VƯỢT TIẾN ĐỘ) │
└────────────────────────────────────────────────────────────────────────┘
```

### Chi Tiết Tóm Lược Từng Tiêu Chí:

1. **Problem Statement**:
   - Xác định căn nguyên kỹ thuật của Prompt Injection/Jailbreak: Cơ chế Self-Attention trong Transformer ghép phẳng chỉ thị hệ thống và dữ liệu người dùng ($X = S \mathbin{\Vert} U$) mà không có ranh giới phần cứng bảo vệ.
   - Bác bỏ tính khả thi của Regex tĩnh (quá giòn) và LLM-as-a-Judge (trễ >500ms, tốn >16GB VRAM GPU).
2. **Research Questions**:
   - **RQ1**: Gom cụm bảo toàn mẫu (Group-Aware Splitting, Jaccard < 0.15) & Khả năng tổng quát hóa ngoại miền ($F_1^{\text{OOD}} \ge 0.92$).
   - **RQ2**: Độ bền đối kháng trước Leetspeak, Spacing, Base64/Cipher ($\text{ARR} \ge 0.95$, $\Delta F_1 < 5\%$).
   - **RQ3**: Đánh đổi an toàn với trải nghiệm người dùng ($\text{FPR} < 1.5\%$, P95 Latency $< 30\text{ ms}$ trên CPU).
3. **Mục Tiêu Đề Tài**:
   - Mục tiêu tổng quát: Thiết kế nguyên mẫu thực nghiệm External Guardrail Proxy Middleware.
   - 5 mục tiêu cụ thể: Curation dữ liệu, Huấn luyện mô hình kép, Kiểm thử độ bền, Đo đạc P95 CPU, Đóng gói FastAPI & Streamlit.
4. **Giải Pháp Đề Xuất (Proposed Solution)**:
   - **Tier-1**: TF-IDF `char_wb` (3-5 ký tự) lọc cú pháp thô sơ và từ khóa phân mảnh với chi phí cực thấp (~3ms).
   - **Tier-2**: Fine-tuned `microsoft/deberta-v3-base` (86M) tận dụng Disentangled Attention bóc tách câu lệnh chỉ thị khỏi dữ liệu (~12.8ms trên CPU).
   - **Tri-State Engine**: Cơ chế 3 trạng thái (`ALLOW`, `REVIEW`, `BLOCK`) kiểm soát nghiêm ngặt tỷ lệ chặn nhầm.
5. **Ranh Giới Đề Tài (Boundary)**:
   - Tập trung vào chuỗi văn bản tiếng Anh; loại trừ tấn công đa phương thức và tấn công mạng hạ tầng.
   - Luận giải loại trừ mô hình sinh lớn $\ge 7\text{B}$ (Llama Guard 3 8B) do rào cản phần cứng GPU và độ trễ giải mã token. Thẳng thắn nêu 3 giới hạn khoa học ngoài tầm với (Stateful multi-turn, Deep commonsense, White-box KV-cache).
6. **Tính Khả Thi Căn Cứ Trên Thực Tế**:
   - Kho dữ liệu: Đã tích hợp 45,000+ mẫu (Deepset, Gandalf, In-The-Wild, Benign) và chạy thành công thuật toán Group-Aware Splitting.
   - Mô hình: Đã tái lập độc lập 5 mô hình y văn upstream; mô hình TF-IDF và DeBERTa-v3 đã được thử nghiệm đạt P95 < 30ms trên CPU.
   - Hệ thống: Đã dựng xong FastAPI Middleware bất đồng bộ và giao diện Streamlit Dashboard kiểm thử 4 kịch bản trực tiếp.
7. **Tiến Độ Triển Khai (Progress %)**:
   - Thời gian trôi qua: 4/15 tuần = **26.7% thời gian**.
   - Khối lượng công việc đã hoàn thành: **~33.0% tổng dự án** (hoàn thành 100% mục tiêu lý thuyết và dữ liệu của Review 1, vượt tiến độ kế hoạch).

---

👉 **Để đọc toàn văn nội dung chi tiết của báo cáo, vui lòng truy cập**:  
📄 [`REVIEW_1_REPORT.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/report_for_review1/REVIEW_1_REPORT.md)
