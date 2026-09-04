# Workspace Cá Nhân — Đỗ Đoàn Duy Phương
## Không Gian Thử Nghiệm Song Song Toàn Trình (Full-Pipeline Exploration Sandbox)

> [!IMPORTANT]
> **Phương châm làm việc toàn đội**: **Ai cũng làm $\rightarrow$ Tham khảo nhau $\rightarrow$ Chốt kết quả**  
> Đây là không gian làm việc nháp (Sandbox) riêng của bạn để tự do thử nghiệm độc lập toàn bộ các mắt xích của hệ thống PI-Guard (từ tiền xử lý dữ liệu, mô hình Baseline TF-IDF, Transformer DeBERTa-v3, kiểm thử đối kháng Evasion cho đến API/Dashboard và viết báo cáo). Không bị bó buộc vào một phần việc cô lập, cả nhóm cùng làm song song, đối chiếu chéo kết quả và họp chốt phương án tối ưu nhất.

### 📌 Lộ trình thực hành toàn trình của bạn:
1. **Khảo sát & Tiền xử lý dữ liệu**: Khảo sát các bộ dữ liệu Jailbreak/Injection, các kỹ thuật làm sạch văn bản và loại bỏ ký tự ẩn.
2. **Baseline ML & Transformer**: Thử nghiệm huấn luyện các mô hình phân loại nhẹ và kiểm thử suy luận mô hình DeBERTa-v3.
3. **FastAPI Guardrail Middleware & LLM Proxy**: Xây dựng endpoint bất đồng bộ bảo vệ trước LLM (`POST /v1/chat/guardrail`) và tích hợp cơ chế Early-Exit 2 tầng.
4. **Streamlit Dashboard & Trực quan hóa**: Phát triển Dashboard tương tác trực quan với ma trận 4 kịch bản demo ($2 \times 2$) và theo dõi logs kiểm toán.
5. **Biên soạn & Phản biện Báo cáo**: Tham gia viết, đọc chéo và phản biện cả 6 báo cáo (Report No.1 $\rightarrow$ No.6), đồng chủ biên Report No.5 (Discussion) & No.6 (Conclusion).

### 📂 Bạn có thể để file thử nghiệm tại đây:
- `scratch_app.py`: Thử nghiệm giao diện Streamlit UI nháp.
- `scratch_api.py`: Thử nghiệm endpoint FastAPI và streaming token.
- `scratch_integration.py`: Thử nghiệm luồng tích hợp hệ thống.
- Khi hoàn thiện thử nghiệm $\rightarrow$ Trao đổi cùng nhóm trong buổi họp tuần để Leader merge giải pháp tối ưu ra thư mục chung (`src/`, `notebooks/`, `docs/`).

### 📚 Tài liệu nghiên cứu cục bộ:
- [`References/REFERENCES_LOG.md`](file:///d:/Work/Do-an/workspaces/phuongddd/References/REFERENCES_LOG.md): Nhật ký các bài báo khoa học thẩm định trong Meeting 2 và đối chiếu cùng nhóm.
- Thư mục lưu trữ PDF: [`References/`](file:///d:/Work/Do-an/workspaces/phuongddd/References/).

