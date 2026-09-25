# BÁO CÁO NGHIÊN CỨU & THỰC NGHIỆM ĐỘC LẬP TASK 3 (MEETING 6)
## CƠ CHẾ CHIA TẦNG VÀ PHÂN TÍCH BLOCK, KÝ TỰ, CHUỖI KÝ TỰ CHO VĂN BẢN LỚN 200,000 KÝ TỰ

---

> **Đơn vị thực hiện**: Đồ án Tốt nghiệp Kỹ sư An toàn Thông tin (IAP491) — Đại học FPT  
> **Đề tài**: *A Machine-Learning Guardrail for Detecting Prompt Injection and Jailbreak Attacks on LLM Applications (PI-Guard)*  
> **Sinh viên thực hiện**: Phạm Minh Hoàng Việt (Mã SV: `SE181467` / Workspace: [`workspaces/vietpmh/`](file:///c:/Users/FPT/Desktop/IAP/pi-guard/workspaces/vietpmh/))  
> **Giảng viên Hướng dẫn (GVHD)**: ThS. Trần Văn Ninh  
> **Căn cứ chỉ đạo từ GVHD**: Biên bản họp tiến độ Meeting 5 ngày 19/09/2026 ([`Meeting 5_19_09_26.md`](file:///c:/Users/FPT/Desktop/IAP/pi-guard/Final-Report/Meeting/Meeting%205_19_09_26.md))  
> **Mã nguồn thực thi**: [`block_analyzer_200k.py`](file:///c:/Users/FPT/Desktop/IAP/pi-guard/workspaces/vietpmh/Task%20Completed/Task%20Meeting%206/block_analyzer_200k.py) | **Dữ liệu đo đạc số hóa**: [`task3_block_analysis_metrics.json`](file:///c:/Users/FPT/Desktop/IAP/pi-guard/workspaces/vietpmh/Task%20Completed/Task%20Meeting%206/task3_block_analysis_metrics.json)

---

## 📌 1. BỐI CẢNH & NHIỆM VỤ ĐƯỢC GIAO TỪ MEETING 5

Tại buổi họp tiến độ **Meeting 5 (ngày 19/09/2026)**, **ThS. Trần Văn Ninh (GVHD)** đã định hướng chuyên sâu:
> 1. *"Cần tìm hiểu sâu về cơ chế chia tầng: Cách thức khi mô hình phân tích các block, ký tự, chuỗi ký tự,... diễn ra như thế nào? (cách bóc tách đặc trưng từ mức chuỗi ký tự thô, n-gram ký tự/từ, đến token trong từng block văn bản)."*  
> 2. *"Cần tìm hiểu cách xử lý khi gặp văn bản đầu vào bị **quá tải ký tự (Context Overload)**, ví dụ các tài liệu lớn lên tới **200,000 ký tự** (từ các file PDF, Ebook, tài liệu doanh nghiệp nhiều chữ) nhằm tránh quá tải tài nguyên và chống nghẽn bộ nhớ."*

Báo cáo này giải quyết toàn diện bài toán trên bằng cách:
1. Phân tích bản chất toán học của **sự bùng nổ độ phức tạp Attention bậc hai $O(N^2)$** khi xử lý văn bản lớn và lý giải tại sao mô hình nguyên khối sẽ bị tràn bộ nhớ (*Out-Of-Memory - OOM*).
2. Xây dựng **Kiến trúc Phân tích Đa Tầng (Multi-Granularity Hierarchical Analysis)**: Từ mức ký tự thô (Character-level DFA), chuỗi $n$-grams có ranh giới (`char_wb`), đến từng khối văn bản con (*Blocks*).
3. Đề xuất và hiện thực hóa giải pháp **Băm Khối Trượt Đè Lấn (Overlapping Block Chunking)** kết hợp kiến trúc dòng (*Streaming Memory Architecture*) giữ mức tiêu thụ bộ nhớ $O(1)$.
4. Kiểm chứng thực tế trên văn bản $200,000$ ký tự qua script [`block_analyzer_200k.py`](file:///c:/Users/FPT/Desktop/IAP/pi-guard/workspaces/vietpmh/Task%20Completed/Task%20Meeting%206/block_analyzer_200k.py).

---

## 🔬 2. NỀN TẢNG KHOA HỌC & LỖ HỔNG CỬA SỔ NGỮ CẢNH (PROMPT OVERFLOW)

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                             3 CĂN CỨ KHOA HỌC CHO BÀI TOÁN VĂN BẢN LỚN                          │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. Vaswani et al. (NeurIPS 2017) & Beltagy (2020)  ───> Độ phức tạp tính toán Attention O(N^2)   │
│ 2. Zhou et al. (arXiv:2605.23196, 2026)             ───> Lỗ hổng bất đối xứng cửa sổ ngữ cảnh   │
│ 3. Boucher et al. (IEEE S&P 2022) & Yuan (ICLR 2024)───> Khử nhiễu cú pháp đa tầng (NFKC/DFA)   │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 2.1. Nghịch Lý Bùng Nổ Bộ Nhớ Của Cơ Chế Tự Chú Ý (Self-Attention O(N^2))
Trong kiến trúc Transformer kinh điển (Vaswani et al. 2017):
$$\text{Attention}(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = \text{Softmax}\left( \frac{\mathbf{Q}\mathbf{K}^\top}{\sqrt{d_k}} \right) \mathbf{V}$$
* Ma trận trọng số $\mathbf{Q}\mathbf{K}^\top$ có kích thước $N \times N$, với $N$ là số lượng tokens đầu vào.
* Khi xử lý một tài liệu lớn $200,000$ ký tự:
  - Giả sử tỷ lệ nén token trung bình là $4$ ký tự/token $\rightarrow N \approx 50,000$ tokens.
  - Ma trận Attention yêu cầu lưu trữ: $50,000 \times 50,000 = 2,500,000,000$ phần tử ($2.5$ tỷ float32).
  - Dung lượng RAM tối thiểu chỉ để chứa một ma trận Attention là:
    $$\text{RAM}_{\text{Attention}} = 2.5 \times 10^9 \times 4\text{ bytes} = 10,000,000,000\text{ bytes} \approx 9.31\text{ GB}$$
  - Với 12 layers và 12 attention heads, bộ nhớ cần thiết sẽ vọt lên tới hàng chục Gigabytes, **lập tức gây tràn bộ nhớ (OOM Crash)** trên bất kỳ hệ thống CPU nào.

### 2.2. Lỗ Hổng Bất Đối Xứng Cửa Sổ Ngữ Cảnh (Prompt Overflow Vulnerability)
* **Tác giả**: Y. Zhou et al. (arXiv:2605.23196, 2026) — *"Prompt Overflow: Vulnerability in Asymmetric Context Windows of LLM Applications"*.
* **File PDF bài báo**: [`Final-Report/References/Zhou_2026_Prompt_Overflow_Guardrail_Window_Mismatch.pdf`](file:///c:/Users/FPT/Desktop/IAP/pi-guard/Final-Report/References/Zhou_2026_Prompt_Overflow_Guardrail_Window_Mismatch.pdf).
* **Bản chất lỗ hổng**: Hiện nay, các LLM thương mại (như GPT-4o, Claude 3.5, Gemini 1.5) hỗ trợ cửa sổ ngữ cảnh cực lớn ($128,000$ đến $1,000,000$ tokens). Tuy nhiên, hầu hết các mô hình phân loại bảo vệ (Guardrails như DeBERTa, BERT, Llama Guard) chỉ hỗ trợ tối đa $512$ hoặc $4096$ tokens.
* **Kỹ thuật tấn công**: Kẻ tấn công cố tình nhồi hàng chục nghìn từ rác (Benign Padding / Distraction Text) vào đầu tài liệu PDF hoặc Ebook để đẩy câu lệnh tiêm nhiễm (*Malicious Prompt*) vượt quá giới hạn $512$ tokens của Guardrail. Nếu hệ thống phòng thủ chỉ cắt cụt đơn giản (`text[:512]`), **Guardrail sẽ chỉ nhìn thấy văn bản sạch, trong khi toàn bộ mã độc ở phía sau vẫn được chuyển thẳng vào LLM để thực thi!**

---

## 🛠️ 3. KIẾN TRÚC PHÂN TÍCH ĐA TẦNG (MULTI-GRANULARITY ARCHITECTURE)

Để vừa chống OOM vừa hóa giải lỗ hổng Prompt Overflow, hệ thống PI-Guard phân tách chuỗi văn bản theo 3 cấp độ bóc tách đặc trưng:

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                      KIẾN TRÚC BÓC TÁCH ĐẶC TRƯNG ĐA TẦNG CỦA PI-GUARD                          │
├─────────────────────────────────────────────────────────────────────────────────────────────────┤
│ [CẤP ĐỘ 1: KÝ TỰ THÔ (RAW CHARACTERS)]                                                          │
│ • Shannon Entropy H(X): Phát hiện chuỗi mật mã đối kháng, token ngẫu nhiên                      │
│ • DFA Regex: Quét mã điều khiển vô hình (Zero-width \u200B), mã đảo chiều RLO (\u202E)         │
│ • Chuẩn hóa NFKC: Ánh xạ toàn bộ ký tự đồng hình (Homoglyphs / Fullwidth) về chuẩn ASCII        │
├─────────────────────────────────────────────────────────────────────────────────────────────────┤
│ [CẤP ĐỘ 2: CHUỖI KÝ TỰ CÓ RANH GIỚI (CHARACTER N-GRAMS WITH BOUNDARIES)]                        │
│ • Khai phá n-grams ký tự (char_wb 3-5): Bắt dính các đòn phân mảnh từ (Leetspeak / Delimited)   │
│ • Ví dụ: "i_g_n_o_r_e" hoặc "i.g.n.o.r.e" được gộp và nhận diện qua ranh giới từ vựng           │
├─────────────────────────────────────────────────────────────────────────────────────────────────┤
│ [CẤP ĐỘ 3: KHỐI VĂN BẢN TRƯỢT ĐÈ LẤN (SLIDING OVERLAPPING BLOCKS)]                              │
│ • Băm tài liệu 200k ký tự thành các blocks: L_block = 1,500 ký tự (~350 tokens)                 │
│ • Độ đè lấn (Overlap): 150 ký tự (10%) chống cắt đôi câu lệnh tiêm nhiễm                        │
│ • Xử lý dòng (Streaming): Duyệt từng block và giải phóng bộ nhớ ngay sau khi quét                │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 3.1. Phân Tích Cấp Ký Tự Thô (Character-Level)
* **Shannon Entropy**: Đo mức độ phân bổ ngẫu nhiên của các ký tự:
  $$H(X) = -\sum_{i=1}^k P(x_i) \log_2 P(x_i)$$
  Văn bản tự nhiên tiếng Anh hoặc tiếng Việt thông thường có $H(X) \approx 3.8 - 4.3$. Nếu $H(X) > 4.8$, chuỗi chứa dấu hiệu của mã hóa Base64 nén hoặc chuỗi ngẫu nhiên GCG.
* **Loại bỏ ký tự tàng hình (Boucher et al., IEEE S&P 2022)**: Loại bỏ các điểm mã `\u200B` (Zero-Width Space), `\u200C` (Zero-Width Non-Joiner), `\uFEFF` (BOM) vốn được kẻ tấn công dùng để chèn vào giữa các từ khóa nhằm làm mù Tokenizer của Guardrail.

### 3.2. Thuật Toán Băm Khối Trượt Đè Lấn (Overlapping Block Chunking)
* **Vấn đề ranh giới (Boundary Splitting Problem)**: Nếu chia khối cứng không đè lấn, một câu lệnh tiêm nhiễm như *"Ignore all previous instructions"* có thể bị cắt đôi thành *"Ignore all"* (nằm ở cuối Block $k$) và *"previous instructions"* (nằm ở đầu Block $k+1$), khiến cả hai block đều không bị phát hiện.
* **Công thức phân khối có đè lấn**:
  $$\text{Block}_i = \text{Text}[i \cdot (L_{\text{block}} - L_{\text{overlap}}) : i \cdot (L_{\text{block}} - L_{\text{overlap}}) + L_{\text{block}}]$$
  Với $L_{\text{block}} = 1,500$ ký tự và $L_{\text{overlap}} = 150$ ký tự ($10\%$), toàn bộ các câu lệnh chỉ thị (thường dài từ $30 - 100$ ký tự) được bảo đảm sẽ xuất hiện trọn vẹn ít nhất trong một block.

---

## 📊 4. KẾT QUẢ ĐO ĐẠC THỰC NGHIỆM ĐỘC LẬP (200,000 KÝ TỰ)

Thực nghiệm được thực thi tự động qua script [`block_analyzer_200k.py`](file:///c:/Users/FPT/Desktop/IAP/pi-guard/workspaces/vietpmh/Task%20Completed/Task%20Meeting%206/block_analyzer_200k.py) trên tài liệu giả lập $200,000$ ký tự có cấy payload ở cuối:

### 4.1. Bảng Số Liệu Đo Đạc Thực Tế Trên CPU Máy Cá Nhân:

| Tiêu Chí Kỹ Thuật | Giá Trị Thực Nghiệm Đo Đạc | Đánh Giá Hiệu Năng & An Toàn |
| :--- | :---: | :--- |
| **Độ dài văn bản thử nghiệm** | **`200,000` ký tự** | Mô phỏng chính xác Ebook / Tài liệu PDF doanh nghiệp theo yêu cầu GVHD. |
| **Kích thước khối (Block Size)** | **`1,500` ký tự** | Tương đương $\approx 350$ tokens, nằm an toàn sâu trong cửa sổ 512 tokens. |
| **Độ đè lấn khối (Block Overlap)** | **`150` ký tự (10%)** | Ngăn chặn triệt để hiện tượng payload bị chia cắt qua ranh giới khối. |
| **Tổng số khối được tạo ra** | **`149` blocks** | Chia nhỏ thành công văn bản $200\text{k}$ ký tự mà không gây nghẽn. |
| **Thời gian xử lý toàn bộ 200k ký tự** | **`46.57 ms`** | Tốc độ quét cực nhanh trên CPU, đạt $\approx 4,300,000\text{ chars/giây}$. |
| **Độ trễ trung bình trên mỗi block** | **`0.313 ms / block`** | Hoàn toàn khả thi cho các hệ thống Ingress thời gian thực. |
| **Mức tiêu thụ bộ nhớ RAM (Memory)**| **`O(1)` (Thường trực < 45 MB)**| Không xảy ra hiện tượng OOM Crash nhờ cơ chế xử lý dòng (Streaming). |
| **Độ hỗn loạn Shannon Entropy** | **`4.1776`** | Nằm trong dải chuẩn an toàn của ngôn ngữ tự nhiên ($3.8 - 4.3$). |

---

## 💡 5. KẾT LUẬN TASK 3

1. **Khẳng định tính đúng đắn của cơ chế chia tầng**:
   - Việc phân tách thành 3 cấp độ (Ký tự $\rightarrow$ Chuỗi n-grams $\rightarrow$ Khối Blocks) giúp hệ thống bóc tách đặc trưng triệt để: bắt dính ký tự ẩn ở Tầng 0, bắt dính leetspeak ở Tầng 1, và đọc hiểu ngữ nghĩa khối ở Tầng 2.
2. **Hóa giải hoàn toàn bài toán quá tải 200k ký tự**:
   - Thay vì nạp nguyên khối khiến RAM bùng nổ $> 9\text{GB}$, cơ chế băm $149$ blocks với bộ nhớ $O(1)$ chỉ mất **$46.57\text{ms}$** trên CPU phổ thông mà không làm tràn bộ nhớ.
3. **Sẵn sàng chuyển tiếp sang Task 4**:
   Phát triển cơ chế quét đảo ngược / ưu tiên đuôi (*Tail-and-Head Prioritized Scanning*) để bắt ngay các câu lệnh tiêm nhiễm bị giấu ở cuối tài liệu $200\text{k}$ ký tự trong $1\text{ms}$.
