# Workspace Cá Nhân — Nguyễn Quí Đức
## Không Gian Thử Nghiệm Song Song Toàn Trình (Full-Pipeline Exploration Sandbox)

> [!IMPORTANT]
> **Phương châm làm việc toàn đội**: **Ai cũng làm $\rightarrow$ Tham khảo nhau $\rightarrow$ Chốt kết quả**  
> Đây là không gian làm việc nháp (Sandbox) riêng của bạn để tự do thử nghiệm độc lập toàn bộ các mắt xích của hệ thống PI-Guard (từ tiền xử lý dữ liệu, mô hình Baseline TF-IDF, Transformer DeBERTa-v3, kiểm thử đối kháng Evasion cho đến API/Dashboard và viết báo cáo). Không bị bó buộc vào một phần việc cô lập, cả nhóm cùng làm song song, đối chiếu chéo kết quả và họp chốt phương án tối ưu nhất.

### 📌 Lộ trình thực hành toàn trình của bạn:
1. **Khảo sát & Tiền xử lý dữ liệu**: Thử nghiệm làm sạch văn bản, kiểm thử các kỹ thuật lẩn tránh (Leetspeak, Base64, Spacing).
2. **Baseline ML & Trích xuất đặc trưng**: Xây dựng bộ kết hợp Word TF-IDF (1-2 grams) + Character TF-IDF (3-5 n-grams) (`char_wb`), huấn luyện và đối sánh Logistic Regression, LinearSVC, Naive Bayes, XGBoost.
3. **Transformer & Robustness**: Chạy thử nghiệm fine-tuning DeBERTa-v3, đo đạc độ trễ và độ suy giảm $\Delta F_1$ dưới tấn công đối kháng.
4. **API Middleware & Tích hợp**: Thử nghiệm endpoint bảo vệ FastAPI và giao diện Streamlit.
5. **Biên soạn & Phản biện Báo cáo**: Tham gia viết, đọc chéo và phản biện cả 6 báo cáo (Report No.1 $\rightarrow$ No.6), đồng chủ biên Report No.3 (Methodology).

### 📂 Bạn có thể để file thử nghiệm tại đây:
- `scratch_tfidf.py`: Thử nghiệm các tham số TF-IDF (`max_features`, `ngram_range`).
- `scratch_pipeline.py`: Thử nghiệm luồng tiền xử lý hoặc mô hình.
- `notes_model_comparison.md`: So sánh tốc độ và độ chính xác các thuật toán.
- Khi hoàn thiện thử nghiệm $\rightarrow$ Trao đổi cùng nhóm trong buổi họp tuần để Leader merge giải pháp tối ưu ra thư mục chung (`src/`, `notebooks/`, `docs/`).

### 📚 Tài liệu nghiên cứu cục bộ:
- [`References/REFERENCES_LOG.md`](file:///d:/Work/Do-an/workspaces/ducnq/References/REFERENCES_LOG.md): Nhật ký các bài báo khoa học thẩm định trong Meeting 2 và đối chiếu cùng nhóm.
- Thư mục lưu trữ PDF: [`References/`](file:///d:/Work/Do-an/workspaces/ducnq/References/).

