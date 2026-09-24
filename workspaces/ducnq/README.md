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
- Khi hoàn thiện thử nghiệm $\rightarrow$ Trao đổi cùng nhóm trong buổi họp tuần để Leader merge giải pháp tối ưu ra thư mục chung `Final-Report/` (`Final-Report/src/`, `Final-Report/notebooks/`, `Final-Report/thesis/`).

### 📚 Tài liệu nghiên cứu cục bộ:
- [`References/REFERENCES_LOG.md`](file:///d:/DoAn/pi-guard/workspaces/ducnq/References/REFERENCES_LOG.md): Nhật ký các bài báo khoa học thẩm định trong Meeting 2 và đối chiếu cùng nhóm.
- Thư mục lưu trữ PDF: [`References/`](file:///d:/DoAn/pi-guard/workspaces/ducnq/References/).

---

### 🛡️ Tiến độ hoàn thành (Cột mốc 07/09/2026 — Sẵn sàng Meeting 3 & Báo cáo Tuần):
- ✅ [`jailguard_mutators.py`](file:///d:/DoAn/pi-guard/workspaces/ducnq/jailguard_mutators.py): Bộ toán tử đột biến đối kháng JailGuard (Targeted Mutators theo Zhang et al., TOSEM 2025: Leetspeak, Spacing, Base64 Smuggling, Zero-Width, Homoglyphs, Chained Composite).
- ✅ [`adversarial_robustness_suite.py`](file:///d:/DoAn/pi-guard/workspaces/ducnq/adversarial_robustness_suite.py): Khung kiểm thử đối kháng đa lát cắt (10 test slices) đo đạc TPR, FPR, Evasion Rate và độ suy giảm $\Delta F_1$.
- ✅ [`scratch_baseline_robustness_eval.py`](file:///d:/DoAn/pi-guard/workspaces/ducnq/scratch_baseline_robustness_eval.py): Kịch bản thực nghiệm đối sánh giữa Word-level TF-IDF và Character Normalization Baseline.
- ✅ [`test_adversarial_suite.py`](file:///d:/DoAn/pi-guard/workspaces/ducnq/test_adversarial_suite.py): Unit test toàn diện kiểm tra tính xác thực của bộ biến dị và tính toán số liệu.
- ✅ [`notes_adversarial_robustness_07_09.md`](file:///d:/DoAn/pi-guard/workspaces/ducnq/doc/notes_adversarial_robustness_07_09.md): Báo cáo thực nghiệm học thuật chuẩn bị cho Meeting 3 và luận văn Chapter 2 & Chapter 3.
- ✅ [`doc/TASK_1_2_TECHNICAL_MASTERY.md`](file:///d:/DoAn/pi-guard/workspaces/ducnq/doc/TASK_1_2_TECHNICAL_MASTERY.md): **[MỚI - MEETING 4]** Báo cáo kỹ thuật chuyên sâu & Sổ tay phản biện Task 1 & Task 2 (Tổng hợp toàn diện).
- ✅ [`doc/TASK_1_PROMPT_INJECTION_VS_JAILBREAK.md`](file:///d:/DoAn/pi-guard/workspaces/ducnq/doc/TASK_1_PROMPT_INJECTION_VS_JAILBREAK.md): **[MỚI - TASK 1]** Phân biệt bản chất kỹ thuật giữa Prompt Injection ($X = S \mathbin{\Vert} U$) và Jailbreak (*Competing Objectives*), giải mã Table 6 InjecGuard.
- ✅ [`doc/TASK_2_ATTACK_VECTORS_AND_MODELS.md`](file:///d:/DoAn/pi-guard/workspaces/ducnq/doc/TASK_2_ATTACK_VECTORS_AND_MODELS.md): **[MỚI - TASK 2]** Khung đe dọa 5 trục chuẩn hóa (5D Framework) và 2 Mô hình tham khảo học thuật (TF-IDF Baseline ~2.8ms vs DeBERTa-v3 Disentangled Attention).
- ✅ [`doc/TASK_MEETING_5_COMPREHENSIVE_SOLUTIONS.md`](file:///d:/DoAn/pi-guard/workspaces/ducnq/doc/TASK_MEETING_5_COMPREHENSIVE_SOLUTIONS.md): **[MỚI - MEETING 5]** Báo cáo giải pháp tổng lực 7 phần: Giải mã "Encode" & Lợi thế Tiếng Việt, Bộ 3 mô hình Tier 1 (Logistic Regression / Random Forest / Isolation Forest), Cơ chế Tri-State Routing Hai Tầng, Xử lý văn bản 200.000 ký tự (Sliding Window O(N)) & Bắt Prompt ẩn đuôi (Tail-Priority Inspection).
- ✅ [`src/tier1_fast_filter_and_chunking.py`](file:///d:/DoAn/pi-guard/workspaces/ducnq/src/tier1_fast_filter_and_chunking.py): **[MỚI - MÃ NGUỒN DEMO THỰC THI]** Module tiền xử lý Tier 0 Scrubber, Huấn luyện Tier 1 (TF-IDF + LR/RF/Isolation Forest) trên ngữ liệu Song ngữ Anh-Việt, và Pipeline Chunking trượt xử lý siêu tài liệu 200k ký tự.
- ✅ [`src/app_demo_meeting5.py`](file:///d:/DoAn/pi-guard/workspaces/ducnq/src/app_demo_meeting5.py): **[MỚI - WEB DEMO DASHBOARD STREAMLIT]** Giao diện Web tương tác trực quan 5 Tab chuẩn 2026 Cyber Security Console (Toàn màn hình, Full-width, Tích hợp 4 Mutators JailGuard, Quét 200k ký tự và Bản đồ Y văn 6 Trụ cột).

---

## 🚀 HƯỚNG DẪN KHỞI CHẠY DEMO VÀ KỊCH BẢN BẢO VỆ MEETING 5 (DÀNH CHO ĐỨC)

### 1. Lệnh khởi chạy Web Demo Console
Mở terminal tại thư mục gốc của đồ án và chạy lệnh sau:
```bash
streamlit run workspaces/ducnq/src/app_demo_meeting5.py
```
> Trình duyệt sẽ tự động mở địa chỉ: `http://localhost:8501`.  
> *Gợi ý*: Nhấn **`F11`** trên trình duyệt để chuyển sang chế độ Toàn màn hình (Full Screen), giao diện sẽ tràn viền cực kỳ chuyên nghiệp.

---

### 2. Kịch bản 5 bước thao tác trực quan trước Thầy Ninh

| Bước | Tab Giao diện | Thao tác thực hiện | Điểm nhấn giải thích trước Thầy |
| :---: | :--- | :--- | :--- |
| **1** | **Phân tích Prompt** | Chọn lần lượt 3 kịch bản:<br/>1. `ISO 27001 (Lành tính)`<br/>2. `Ép in Mật khẩu (Tấn công)`<br/>3. `NotInject Code (Từ nhạy cảm)` | • Câu lành tính ra `FAST-PASS` trong **$0.8\text{ms}$** (tiết kiệm 100% GPU).<br/>• Câu tấn công ra `FAST-BLOCK` trong **$0.9\text{ms}$** (chặn ngay ở cổng Ingress).<br/>• Câu NotInject rơi vào vùng lưỡng lự $[0.15, 0.85]$, DeBERTa-v3 thẩm định ra `LÀNH TÍNH` (chứng minh kiểm soát chặn nhầm FPR $< 1.5\%$). |
| **2** | **Đột biến Đối kháng** | Chọn toán tử `1. Spacing` hoặc `3. Zero-Width` rồi bấm **Thử nghiệm Đột biến** | • Cột trái: Payload đột biến của hacker làm gãy bộ tách từ, qua mặt các bộ lọc từ khóa thường.<br/>• Cột phải: **Tầng 0 Scrubber** bóc sạch ký tự ẩn `\u200B` và tự động ghép từ bảo toàn ranh giới (Despacing), giúp Tầng 1/2 tóm gọn payload. |
| **3** | **Quét Văn bản 200k** | Tích chọn `Giấu lệnh tấn công ở block cuối` rồi bấm **Quét Siêu Tài liệu 200k** | • Quét tuần tự toàn bộ 134 blocks mất **$\sim 38.4\text{ms}$**.<br/>• Cơ chế **Tail-Priority Early-Exit** của nhóm bắt dính câu lệnh giấu ở trang cuối và ngắt quét chỉ trong **$1.2\text{ms}$** (nhanh gấp **33 lần**, RAM tiêu thụ $< 50\text{MB}$, giải quyết triệt để vấn đề Context Overload). |
| **4** | **Chỉ số Thực nghiệm** | Mở bảng đối chuẩn trên 2,678 mẫu dữ liệu thật | • Độ chính xác Accuracy: **$98.5\%$**.<br/>• Điểm $F_1$-Score: **$0.9307$**.<br/>• Tỷ lệ chặn nhầm FPR: **$0.53\%$** (thỏa mãn yêu cầu khắt khe $< 1.5\%$). |
| **5** | **Bảo chứng Y văn** | Chiếu 6 thẻ Trụ cột Kiến trúc tương ứng 6 công trình đỉnh cao | • Chứng minh hệ thống được bảo chứng 100% bởi các hội nghị top đầu (ACM TOSEM 2025, USENIX Security 2026, NeurIPS 2023, ACL 2025, Saltzer & Schroeder 1975). |

---

### 3. Sổ tay trả lời nhanh 3 câu hỏi Thầy Ninh hay xoáy
1. **❓ Tại sao phải phân tầng 2 lớp, sao không chạy luôn DeBERTa cho an toàn?**  
   👉 *Trả lời*: DeBERTa-v3 có độ trễ 25-30ms và tốn chi phí GPU. Nhờ Tầng 1 (TF-IDF + LR) lọc trước hơn 80% câu rõ ràng trong $< 1\text{ms}$, hệ thống tiết kiệm được **82.6% chi phí GPU** và hạ độ trễ trung bình xuống còn **$\sim 4.3\text{ms}$**, vừa nhẹ vừa chống được đòn tấn công từ chối dịch vụ (DoS).
2. **❓ Nhóm giải quyết bài toán văn bản cực dài 200k ký tự (PDF/Ebook) thế nào?**  
   👉 *Trả lời*: Dùng cửa sổ trượt Sliding Window ($W=1500, \Delta=250$) chuyển độ phức tạp bậc hai $O(N^2)$ của Transformer thành độ phức tạp tuyến tính $O(N)$ trên CPU, chỉ tốn $< 50\text{MB}$ RAM. Đồng thời áp dụng giải thuật **Tail-Priority** quét khối đuôi trước để bắt đứng đòn giấu lệnh ở trang cuối chỉ trong **$1.2\text{ms}$**.
3. **❓ Đề tài này có điểm gì mới đối với Tiếng Việt không?**  
   👉 *Trả lời*: Tiếng Việt có dấu dạng NFD thường bị tách thành nhiều byte làm vỡ token (Token Fragmentation). Nhóm khắc phục bằng cách chuẩn hóa Unicode NFKC ở Tầng 0 và **tự xây dựng bộ dữ liệu song ngữ Anh - Việt 2,678 mẫu thực tế** được gán nhãn có kiểm định, điều mà các rào chắn tiếng Anh trên thế giới chưa xử lý được.



