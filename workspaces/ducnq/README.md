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
