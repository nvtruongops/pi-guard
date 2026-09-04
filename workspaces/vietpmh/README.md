# Workspace Cá Nhân — Phạm Minh Hoàng Việt
## Không Gian Thử Nghiệm Song Song Toàn Trình (Full-Pipeline Exploration Sandbox)

> [!IMPORTANT]
> **Phương châm làm việc toàn đội**: **Ai cũng làm $\rightarrow$ Tham khảo nhau $\rightarrow$ Chốt kết quả**  
> Đây là không gian làm việc nháp (Sandbox) riêng của bạn để tự do thử nghiệm độc lập toàn bộ các mắt xích của hệ thống PI-Guard (từ tiền xử lý dữ liệu, mô hình Baseline TF-IDF, Transformer DeBERTa-v3, kiểm thử đối kháng Evasion cho đến API/Dashboard và viết báo cáo). Không bị bó buộc vào một phần việc cô lập, cả nhóm cùng làm song song, đối chiếu chéo kết quả và họp chốt phương án tối ưu nhất.

### 📌 Lộ trình thực hành toàn trình của bạn:
1. **Khảo sát & Tiền xử lý dữ liệu**: Nghiên cứu tokenizer, các kiểu nhiễu cú pháp (Leetspeak, Spacing, Base64) và tiền xử lý chuẩn hóa.
2. **Baseline ML & Thử nghiệm mô hình**: Chạy thử nghiệm trích xuất đặc trưng TF-IDF n-grams và các bộ phân loại cơ sở.
3. **Transformer Fine-Tuning & Quantization**: Fine-tuning mô hình `microsoft/deberta-v3-base` (3 classes: Benign, Injection, Jailbreak), thực hiện lượng hóa động INT8 sang ONNX Runtime và benchmark độ trễ CPU.
4. **Kiểm thử đối kháng & API**: Đo đạc độ bền trước các tấn công Evasion/Obfuscation, kiểm thử endpoint FastAPI và Streamlit UI.
5. **Biên soạn & Phản biện Báo cáo**: Tham gia viết, đọc chéo và phản biện cả 6 báo cáo (Report No.1 $\rightarrow$ No.6), đồng chủ biên Report No.4 (Experimental and Results).

### 📂 Bạn có thể để file thử nghiệm tại đây:
- `scratch_quantize.py`: Thử nghiệm script nén ONNX INT8 và đo latency P95 trên CPU.
- `scratch_evasion_test.py`: Thử nghiệm các payload Base64/Cipher độc hại.
- `scratch_transformer.py`: Thử nghiệm huấn luyện và đánh giá mô hình.
- Khi hoàn thiện thử nghiệm $\rightarrow$ Trao đổi cùng nhóm trong buổi họp tuần để Leader merge giải pháp tối ưu ra thư mục chung (`src/`, `notebooks/`, `docs/`).

### 📚 Tài liệu nghiên cứu cục bộ:
- [`References/REFERENCES_LOG.md`](file:///d:/Work/Do-an/workspaces/vietpmh/References/REFERENCES_LOG.md): Nhật ký các bài báo khoa học thẩm định trong Meeting 2 và đối chiếu cùng nhóm.
- Thư mục lưu trữ PDF: [`References/`](file:///d:/Work/Do-an/workspaces/vietpmh/References/).

