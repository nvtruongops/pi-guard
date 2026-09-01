# QUY CHẾ LÀM VIỆC NHÓM 4 THÀNH VIÊN: "CẢ 4 CÙNG LÀM SONG SONG — HỌP ĐỒNG QUY TRI THỨC"
## Parallel Full-Pipeline Exploration & Knowledge Convergence Paradigm

Trong đề tài **PI-Guard** (FPT University IAP491), nhóm áp dụng mô hình **Cả 4 cùng làm toàn diện (Full-Stack AI Security Collaboration)** để đảm bảo **ai cũng có kinh nghiệm thực chiến sâu sắc, không ai phải ngồi chờ ai, và tự tin bảo vệ trước Hội đồng**:

---

### 🔄 1. QUY TRÌNH 2 PHA HÀNG TUẦN (SPRINT WORKFLOW)

```
                     ┌────────────────────────────────────────────────────────┐
                     │     QUY TRÌNH HÀNG TUẦN: SONG SONG ──► ĐỒNG QUY        │
                     └───────────────────────────┬────────────────────────────┘
                                                 │
            ┌────────────────────────────────────┴────────────────────────────────────┐
            ▼                                                                         ▼
┌──────────────────────────────────────────────┐              ┌──────────────────────────────────────────────┐
│ PHA 1: KHÁM PHÁ SONG SONG (TRONG TUẦN)       │              │ PHA 2: HỌP ĐỒNG QUY TRI THỨC (CUỐI TUẦN)     │
├──────────────────────────────────────────────┤              ├──────────────────────────────────────────────┤
│ • Cả 4 bạn cùng tự tay làm toàn bộ pipeline: │              │ • Cả 4 ngồi lại họp bàn tròn (30-60 phút):   │
│   - Cùng khảo sát & phân tích dataset        │              │   - So sánh kết quả thực nghiệm của 4 người  │
│   - Cùng train thử nghiệm các thuật toán ML  │              │   - Đánh giá: Model nào F1 cao hơn? Ít FPR?  │
│   - Cùng test tấn công Jailbreak/Base64      │              │   - Chọn giải pháp XUẤT SẮC NHẤT đưa vào     │
│   - Cùng chạy thử nghiệm API/Dashboard       │              │     thư mục chung `src/`                     │
│ • Mỗi bạn làm việc trong `workspaces/<tên>/` │              │ • Cùng tinh gọn báo cáo & diễn tập slide     │
└──────────────────────────────────────────────┘              └──────────────────────────────────────────────┘
```

---

### 👥 2. KẾ HOẠCH HÀNH ĐỘNG SONG SONG 4 THÀNH VIÊN THEO TỪNG CỘT MỐC

| Cột Mốc Đánh Giá | Hoạt Động Song Song Của Cả 4 Bạn | Phiên Họp Tổng Kết & Đồng Quy Tri Thức | Sản Phẩm Đầu Ra Nghiệm Thu |
| :--- | :--- | :--- | :--- |
| **🎯 REVIEW 1**<br>*(Tuần 1 - 4: Xác định bài toán & SOTA)* | Cả 4 cùng đọc 17 papers, cùng phân tích các vụ tấn công thực tế (DAN, Base64), cùng thử các câu lệnh prompt injection. | Cùng thống nhất bảng Threat Model NIST, 3 Câu hỏi nghiên cứu IEEE, và phân vai thuyết trình 9 slide. | [`chapters/01_Introduction.md`](file:///d:/Work/Do-an/docs/thesis/chapters/01_Introduction.md)<br>[`chapters/02_Literature_Review.md`](file:///d:/Work/Do-an/docs/thesis/chapters/02_Literature_Review.md)<br>[`Review1_Presentation_Slides_Outline.md`](file:///d:/Work/Do-an/docs/thesis/Review1_Presentation_Slides_Outline.md) |
| **🎯 REVIEW 2**<br>*(Tuần 5 - 7: Methodology & Baseline ML)* | Cả 4 cùng tải dataset, cùng thử thuật toán gom cụm Group-Aware, cùng huấn luyện các mô hình Baseline (LinearSVC, LogisticRegression, XGBoost, Naive Bayes). | Đối sánh F1-score và FPR giữa các thuật toán của 4 bạn $\rightarrow$ Chọn pipeline Baseline tối ưu nhất đưa vào `src/models/baseline/`. | [`chapters/03_Methodology.md`](file:///d:/Work/Do-an/docs/thesis/chapters/03_Methodology.md)<br>`src/datasets/splitter.py`<br>`notebooks/02_baseline.ipynb` |
| **🏛️ HỘI ĐỒNG 1**<br>*(Tuần 8 - 12: Transformer & Prototype)* | Cả 4 cùng thử fine-tune DeBERTa-v3/RoBERTa, cùng thử các kỹ thuật nén INT8, cùng viết các payload lẩn tránh Base64/Leetspeak để "tấn công thử nghiệm" lẫn nhau. | Chọn checkpoint mô hình có độ trễ thấp nhất (< 15ms) và kháng lẩn tránh tốt nhất $\rightarrow$ Tích hợp vào FastAPI Middleware & Streamlit UI. | [`chapters/04_Experimental_and_Results.md`](file:///d:/Work/Do-an/docs/thesis/chapters/04_Experimental_and_Results.md)<br>`src/models/classifier.py`<br>`src/api/` & `src/dashboard/` |
| **🎓 HỘI ĐỒNG FINAL**<br>*(Tuần 13 - 15: Tốt nghiệp Chính thức)* | Cả 4 cùng đọc toàn văn 6 chương, cùng đặt các câu hỏi phản biện giả định của Hội đồng để tập trả lời (Mock Defense). | Chạy script biên dịch `python scripts/compile_thesis.py`, quét Turnitin (< 20%), tổng duyệt slide và bảo vệ trước Hội đồng. | [`FINAL_THESIS.md`](file:///d:/Work/Do-an/docs/thesis/FINAL_THESIS.md)<br>Slide Bảo Vệ Tốt Nghiệp Chính Thức |

---

### 🛡️ 3. LỢI ÍCH SỐ 1 KHI BẢO VỆ TRƯỚC HỘI ĐỒNG:
- **100% Thành viên đều hiểu toàn bộ hệ sinh thái**: Khi Thầy/Cô trong Hội đồng chỉ định bất kỳ ai trả lời về Data, Model hay API $\rightarrow$ Bạn đó đều đã từng tự tay làm thử và trả lời xuất sắc.
- **Tính đoàn kết và làm chủ đồ án cao nhất**: Không có cảm giác "người gánh team, người đứng ngoài cuộc".
