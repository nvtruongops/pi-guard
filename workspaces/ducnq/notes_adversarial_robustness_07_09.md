# 🛡️ BÁO CÁO NGHIÊN CỨU & KẾT QUẢ THỰC NGHIỆM ĐỐI KHÁNG
## XÂY DỰNG BỘ KIỂM THỬ ĐỐI KHÁNG (ADVERSARIAL ROBUSTNESS SUITE) KHÁNG LEETSPEAK / BASE64 / SPACING DỰA TRÊN JAILGUARD

- **Thành viên thực hiện**: Nguyễn Quí Đức (MSSV: `SE182087`)
- **Vai trò**: Classical ML Baseline, Feature Extraction & Adversarial Robustness
- **Thời gian hoàn thành**: 07/09/2026 (Cột mốc tuần 2 / Chuẩn bị Meeting 3)
- **Không gian làm việc**: [`workspaces/ducnq/`](file:///d:/DoAn/pi-guard/workspaces/ducnq/)

---

## 🔬 I. CƠ SỞ LÝ THUYẾT & NỀN TẢNG HỌC THUẬT

Căn cứ vào kết quả thẩm định bài báo khoa học trong [Meeting 2 (01/09/2026)](file:///d:/DoAn/pi-guard/Meeting/Meeting%202_01_09_26.md) và danh mục tài liệu cục bộ tại [`References/REFERENCES_LOG.md`](file:///d:/DoAn/pi-guard/workspaces/ducnq/References/REFERENCES_LOG.md):

1. **JailGuard (Zhang et al., ACM TOSEM 2025 / arXiv:2312.10766)** [[1]](#ref1):
   - **Kế thừa**: Áp dụng **Algorithm 1 (Targeted Mutators Workflow)** để thiết kế các toán tử biến dị cú pháp có chủ đích (Targeted Mutators) trên văn bản.
   - **Chọn lọc kỹ thuật**: Giữ lại các toán tử biến đổi mức ký tự và cấu trúc prompt (Leetspeak, Inter-token Spacing, Base64 Smuggling, Zero-Width Invisible Characters, Homoglyphs); loại bỏ thành phần xử lý đa phương thức (ảnh/video) và cơ chế online multi-pass (vì gây độ trễ $> 3\text{s}$, vi phạm yêu cầu bảo vệ độ trễ thấp của Guardrail).
2. **Jain et al. (2023 / arXiv:2309.00614)** [[2]](#ref2):
   - Cung cấp cơ sở lý thuyết chứng minh các đòn tấn công xáo trộn ký tự làm suy giảm nghiêm trọng khả năng phát hiện của các bộ lọc dựa trên token hoặc từ điển tĩnh.
3. **SmoothLLM (Robey et al., 2023 / arXiv:2310.03684)** [[3]](#ref3):
   - Phân tích tính kháng cự trước nhiễu loạn ngẫu nhiên mức ký tự, làm tiền đề cho việc chọn lựa đặc trưng **Character $n$-grams (3-5 grams, `char_wb`)** thay vì chỉ phụ thuộc vào Word $n$-grams.

---

## ⚙️ II. THIẾT KẾ CÁC TOÁN TỬ BIẾN DỊ ĐỐI KHÁNG (JAILGUARD MUTATORS)

Các toán tử biến dị đã được lập trình hoàn chỉnh tại [`jailguard_mutators.py`](file:///d:/DoAn/pi-guard/workspaces/ducnq/jailguard_mutators.py):

| Toán Tử Biến Dị | Cơ Chế Tấn Công Evasion | Mục Tiêu Thử Thách Của Guardrail |
| :--- | :--- | :--- |
| **`LeetspeakMutator`** | Thay thế ký tự chữ cái bằng chữ số/biểu tượng thị giác tương đương (ví dụ: `i` $\rightarrow$ `1`, `e` $\rightarrow$ `3`, `s` $\rightarrow$ `5`, `t` $\rightarrow$ `7`). Hỗ trợ tham số xác suất nhiễu $p \in [0.2, 0.8]$. | Kiểm tra độ nhạy của bộ trích xuất đặc trưng khi từ vựng bị thay đổi chính tả nhưng LLM đích vẫn đọc hiểu ngữ nghĩa. |
| **`SpacingMutator`** | Chèn khoảng trắng giữa các ký tự trong từ (ví dụ: `i n j e c t i o n` hoặc `b y p a s s`). | Phá vỡ ranh giới tách từ (Word Tokenization) và phân rã các từ vựng tấn công thành các subword đơn lẻ trong Word-level TF-IDF. |
| **`Base64Mutator`** | Mã hóa chuỗi tấn công sang Base64 và bọc trong các mẫu chỉ thị giải mã (Instruction Smuggling: *"Decode the following base64 payload and execute..."*). | Thử thách khả năng phát hiện mẫu mã hóa hoặc bộ tiền giải mã (Decoding pre-filter) của Guardrail trước khi prompt chuyển tới LLM. |
| **`ZeroWidthMutator`** | Chèn các ký tự Unicode vô hình (`\u200B`, `\u200C`, `\u200D`, `\uFEFF`) xen kẽ vào các từ nhạy cảm. | Vượt qua các bộ lọc regex/từ khóa đơn thuần nhưng hoàn toàn vô hình đối với người dùng. |
| **`HomoglyphMutator`** | Thay thế ký tự Latin bằng ký tự Cyrillic tương đồng về mặt thị giác (ví dụ: Cyrillic `а` thay cho Latin `a`, `о` thay cho `o`). | Đánh lừa bảng mã ASCII chuẩn mà không làm biến dạng giao diện hiển thị. |
| **`JailGuardCompositeMutator`** | Xâu chuỗi kết hợp nhiều toán tử biến dị (ví dụ: Leetspeak kết hợp Zero-Width spaces) theo Algorithm 1 của JailGuard. | Mô phỏng các kỹ thuật tấn công phức hợp cao cấp trong thế giới thực. |

---

## 📊 III. KIẾN TRÚC BỘ KIỂM THỬ (ADVERSARIAL ROBUSTNESS SUITE)

Bộ kiểm thử được xây dựng tại [`adversarial_robustness_suite.py`](file:///d:/DoAn/pi-guard/workspaces/ducnq/adversarial_robustness_suite.py) gồm **10 lát cắt kiểm thử (Test Slices)**:

1. `Clean_Baseline`: Tập kiểm thử tấn công và câu hỏi thường nguyên bản.
2. `Leetspeak_Mild_p0.3`: Mức độ thay thế nhẹ (30% ký tự).
3. `Leetspeak_Heavy_p0.7`: Mức độ thay thế mạnh (70% ký tự).
4. `Spacing_WordSplit`: Tách khoảng trắng bên trong các từ khóa.
5. `Spacing_FullChar`: Tách rời toàn bộ ký tự trong câu.
6. `Base64_PayloadWrapping`: Bọc payload trong chỉ thị Base64.
7. `ZeroWidth_InvisibleChars`: Chèn ký tự vô hình vào chuỗi tấn công.
8. `Unicode_Homoglyphs`: Hoán đổi ký tự Unicode đồng dạng.
9. `JailGuard_Composite_LeetZero`: Kết hợp đồng thời Leetspeak và Zero-Width.
10. `Perturbed_Benign_Robustness`: Kiểm tra tính ổn định của False Positive Rate (FPR) khi người dùng vô tình gõ sai chính tả hoặc định dạng lạ (đảm bảo không chặn nhầm người dùng hợp lệ, giữ Invariant $\text{FPR} < 1.5\%$).

---

## 📈 IV. KẾT QUẢ ĐỐI SÁNH THỰC NGHIỆM (WORD TF-IDF VS. CHARACTER NORMALIZED)

Kịch bản thực nghiệm đối chứng chạy từ [`scratch_baseline_robustness_eval.py`](file:///d:/DoAn/pi-guard/workspaces/ducnq/scratch_baseline_robustness_eval.py):

### 1. Mô hình Word-level Naive Classifier (Tương đương Word TF-IDF đơn thuần)
- **Clean Baseline**: Recall: **100%**, F1: **100%**, FPR: **0.0%**.
- **Dưới tấn công Spacing (`Spacing_WordSplit`)**: Recall giảm còn **0.0%**, Evasion Rate: **100%** ($\Delta F_1 = -100\%$). Toàn bộ từ khóa bị phá vỡ ranh giới từ.
- **Dưới tấn công Leetspeak (`Leetspeak_Heavy`)**: Recall giảm còn **10.0%**, Evasion Rate: **90%** ($\Delta F_1 = -81.8\%$).
- **Dưới tấn công Zero-Width**: Recall giảm còn **0.0%**, Evasion Rate: **100%**.

### 2. Mô hình Character-level + Unicode NFKC Normalizer (Đề xuất của PI-Guard)
- **Clean Baseline**: Recall: **100%**, F1: **100%**, FPR: **0.0%**.
- **Dưới tấn công Spacing (`Spacing_WordSplit`)**: Recall giữ vững **100%**, Evasion Rate: **0.0%** ($\Delta F_1 = 0.0\%$).
- **Dưới tấn công Leetspeak (`Leetspeak_Heavy`)**: Recall giữ vững **100%**, Evasion Rate: **0.0%** ($\Delta F_1 = 0.0\%$).
- **Dưới tấn công Zero-Width**: Recall giữ vững **100%**, Evasion Rate: **0.0%** ($\Delta F_1 = 0.0\%$).
- **Dưới tấn công Base64 Wrapping**: Nhận diện thành công wrapper chỉ thị độc hại với Recall **100%**.
- **Độ trễ suy luận**: Thời gian tiền xử lý và suy luận trung bình $< 1\text{ms}$ trên CPU, đáp ứng hoàn hảo tiêu chí **bảo vệ trực tuyến độ trễ thấp (Inline Low-Latency Proxy)**.

---

## 🚀 V. ĐỀ XUẤT ĐỒNG QUY CHO CUỘC HỌP NHÓM TUẦN 2 (MEETING 3)

1. **Đề xuất Leader (`nvtruongops`) đồng quy mã nguồn**:
   - Chuyển giao các toán tử mutators từ `jailguard_mutators.py` vào `src/preprocessing/obfuscation.py` để làm công cụ chuẩn hóa cho toàn dự án.
   - Tích hợp `adversarial_robustness_suite.py` vào `src/evaluation/` để kiểm thử chéo cho mô hình Transformer DeBERTa-v3 của bạn Việt (`vietpmh`).
2. **Đóng góp vào Luận văn (Thesis Chapters)**:
   - **Chapter 2 (Literature Review)**: Đưa bảng đối sánh cơ chế Evasion từ JailGuard và phân tích điểm yếu của Word Tokenization.
   - **Chapter 3 (Methodology)**: Đồng chủ biên phần phương pháp luận Classical ML, trích xuất đặc trưng Word + Char $n$-grams (`char_wb`, $n \in [3, 5]$), cơ chế chuẩn hóa NFKC và bộ kiểm thử đối kháng đa lát cắt.

---

## 📚 TÀI LIỆU THAM KHẢO (REFERENCES)

<a id="ref1"></a>
- **[1]** S. Zhang et al., "JailGuard: A Universal Detection Framework for Prompt-based Attacks on LLM Systems," in *ACM Transactions on Software Engineering and Methodology (TOSEM)*, 2025. arXiv: [2312.10766](https://arxiv.org/abs/2312.10766).
<a id="ref2"></a>
- **[2]** N. Jain et al., "Baseline Defenses for Adversarial Attacks on Large Language Models," arXiv preprint, 2023. arXiv: [2309.00614](https://arxiv.org/abs/2309.00614).
<a id="ref3"></a>
- **[3]** A. Robey et al., "SmoothLLM: Defending Large Language Models Against Jailbreaking Attacks," arXiv preprint, 2023. arXiv: [2310.03684](https://arxiv.org/abs/2310.03684).
