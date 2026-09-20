# KẾ HOẠCH HÀNH ĐỘNG & DANH MỤC NHIỆM VỤ MEETING 6 (TUẦN TỪ 20/09 ĐẾN 26/09/2026)

**Đề tài**: PI-Guard | **GVHD**: Thầy Trần Văn Ninh  
**Trưởng nhóm phụ trách điều phối**: Nguyễn Văn Trường (`SE182034` / `nvtruongops`)  
**Workspace**: [`workspaces/truongnv/reports/tasks_for_meeting_6/`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_6/)  
**Căn cứ chỉ đạo từ GVHD**: Biên bản Meeting 5 ngày 19/09/2026 ([`Final-Report/Meeting/Meeting 5_19_09_26.md`](file:///d:/Work/Do-an/Final-Report/Meeting/Meeting%205_19_09_26.md))

---

## 📌 Bối Cảnh & Mục Tiêu Trọng Tâm Tuần Này

> [!IMPORTANT]
> **BỐI CẢNH TỪ MEETING 5 (19/09/2026)**:  
> - **Nội dung nhóm đã báo cáo**: Nhóm chưa xác định được mô hình Tầng 1 phù hợp cho đồ án, và chưa phân tích được 2 mô hình (Tầng 1 và Tầng 2) sẽ kết hợp với nhau như thế nào.
> - **Chỉ đạo & Góp ý từ GVHD (Thầy Trần Văn Ninh)**: Thầy yêu cầu nhóm về tìm hiểu thêm các nội dung then chốt:
>   1. **Cơ chế chia tầng & Cách thức phân tích block, ký tự, chuỗi ký tự**: Tìm hiểu sâu cơ chế chia tầng; làm rõ cách thức khi mô hình phân tích các block, ký tự, chuỗi ký tự,... như thế nào (cơ chế trích xuất đặc trưng từ chuỗi ký tự thô, n-gram ký tự/từ, đến token trong từng block văn bản).
>   2. **Xử lý quá tải ký tự**: Tìm hiểu cách xử lý khi văn bản đầu vào quá lớn, lên tới **200k ký tự** (file PDF, Ebook, tài liệu nhiều chữ).
>   3. **Kịch bản prompt giấu ở cuối**: Lưu ý trường hợp kẻ tấn công giấu câu lệnh tiêm nhiễm ở cuối tài liệu (hidden prompt at the end).
>   4. **Làm rõ thiết kế hệ thống**: Trả lời rõ **Tier 1 làm gì**, **Tier 2 làm gì**, và **dùng bộ tool gì**?
> 
> **MỤC TIÊU SPRINT TUẦN NÀY (SPRINT OBJECTIVE)**:  
> Tập trung nghiên cứu, thực nghiệm và giải quyết trọn vẹn 4 định hướng mà GVHD đã giao để chuẩn bị báo cáo Meeting 6.

---

## 📂 Cấu Trúc Thư Mục Phân Hệ `tasks_for_meeting_6/`

```text
workspaces/truongnv/reports/tasks_for_meeting_6/
├── README.md                                # [BÁO CÁO MASTER & DANH MỤC NHIỆM VỤ TUẦN MEETING 6]
├── src/                                     # [MÃ NGUỒN NGUYÊN MẪU THỰC NGHIỆM TUẦN 6]
│   ├── tier0_ingress_scrubber.py            # Lớp 0: Chuẩn hóa Unicode NFKC, strip Zero-width, giải mã Base64/Hex
│   ├── block_chunker.py                     # Băm nhỏ khối 256-512 tokens, Sliding Window 10%, Head & Tail Priority
│   ├── tier1_fast_filter.py                 # Tầng 1: Dual TF-IDF N-Grams + Platt LogReg + Early-Stopping
│   └── tier2_onnx_arbiter.py                # Tầng 2: DeBERTa-v3 MOF lượng tử hóa ONNX INT8 trên CPU
├── tests/                                   # [BỘ TEST SUITE KIỂM THỬ ĐỘC LẬP]
│   ├── test_long_document_200k.py           # Kiểm thử quét tài liệu 200k ký tự & đo P95 latency
│   └── test_hidden_prompt_at_tail.py        # Kiểm thử kịch bản payload ẩn ở trang cuối PDF/Ebook
├── data/                                    # [DỮ LIỆU THỰC NGHIỆM TÀI LIỆU DÀI]
│   ├── sample_benign_200k.txt               # Mẫu văn bản lành tính 200k ký tự
│   └── sample_malicious_tail_200k.txt       # Mẫu văn bản 200k ký tự có cấy prompt ở cuối
└── benchmarks/                              # [KẾT QUẢ ĐỐI CHUẨN & BIỂU ĐỒ ĐO ĐẠC]
    ├── latency_p95_evaluation.json          # Báo cáo đo đạc độ trễ P95 CPU
    └── confusion_matrix_two_tier.png        # Ma trận nhầm lẫn sau khi phân tầng
```

---

## 📋 Bảng Phân Rã 5 Nhiệm Vụ Cụ Thể Cần Làm (Detailed Work Breakdown)

### 🔹 Nhiệm vụ 1: Hiện thực hóa Module Băm Khối (Block Chunking) & Quét Ưu Tiên Hai Đầu
- **Mục tiêu**: Xử lý văn bản lớn lên tới **200k ký tự** mà không gây tràn bộ nhớ (OOM) hay bị lỗi cắt cụt (Truncation Blind Spot).
- **Yêu cầu kỹ thuật**:
  - Kích thước khối (Block Size): $256 - 512\text{ tokens}$ (tương đương $\sim 1.000 - 2.000\text{ ký tự}$).
  - Độ chồng lấn (Overlap): $10\% - 15\%$ ($\sim 30 - 50\text{ tokens}$) giữa 2 block liền kề để chống sót payload bị cắt đôi.
  - **Chiến lược quét ưu tiên vị trí (Head & Tail Priority)**: Quét Block cuối cùng (Tail Block) $\rightarrow$ Block áp chót $\rightarrow$ Block đầu tiên (Header Block) $\rightarrow$ Các block thân (Body Blocks).
  - **Cơ chế ngắt sớm (Early-Stopping)**: Dừng quét ngay lập tức khi phát hiện bất kỳ block nào độc hại ($P \ge 0.85$).

---

### 🔹 Nhiệm vụ 2: Chuẩn hóa & Đóng gói Tầng 1 (Dual-Space TF-IDF N-Grams + LogReg)
- **Mục tiêu**: Bộ lọc thô siêu tốc $\le 0.2\text{ms}$/block trên CPU, giải phóng $> 80\%$ lưu lượng.
- **Yêu cầu kỹ thuật**:
  - Trích xuất đặc trưng kết hợp: Word N-Grams ($n \in [1, 3]$) + Character N-Grams có biên từ ($n \in [3, 5]$).
  - Thuật toán phân loại: Logistic Regression hiệu chuẩn xác suất Platt Scaling ($C=1.0, \text{class\_weight='balanced'}$).
  - Định tuyến 3 trạng thái (Tri-State):
    * $P \le 0.15 \implies$ Cho qua (Benign), chuyển sang block tiếp theo.
    * $P \ge 0.85 \implies$ Chặn (Malicious) + Kích hoạt Early-Stopping dừng toàn bộ tiến trình.
    * $0.15 < P < 0.85 \implies$ Vùng bất định, chuyển tiếp block lên Tầng 2.

---

### 🔹 Nhiệm vụ 3: Lượng tử hóa ONNX INT8 & Tích hợp Tầng 2 (DeBERTa-v3 MOF)
- **Mục tiêu**: Thẩm định ngữ nghĩa sâu cho các block bất định trong thời gian $\le 18.5\text{ms}$/block trên CPU.
- **Yêu cầu kỹ thuật**:
  - Sử dụng trọng số mỏ neo `microsoft/deberta-v3-base` (PIGuard ACL 2025 [[1]](#ref1)).
  - Biên dịch sang ONNX Graph và áp dụng Dynamic INT8 Quantization bằng `onnxruntime`.
  - Giảm dung lượng từ $500\text{MB}$ xuống $\sim 130\text{MB}$, giảm độ trễ CPU từ $112\text{ms}$ xuống $\le 18.5\text{ms}$.
  - Xác minh độ suy hao chất lượng phân loại so với mô hình gốc FP32: Đảm bảo độ suy hao $\Delta F_1 < 0.5\%$.

---

### 🔹 Nhiệm vụ 4: Tích hợp Lớp 0 (Tier-0 Ingress Scrubber) Chống Né Tránh
- **Mục tiêu**: Dọn dẹp bề mặt chuỗi văn bản trong thời gian $\tau_0 < 0.05\text{ms}$, bảo vệ Tầng 1 và Tầng 2 khỏi các đòn ngụy trang giao diện.
- **Yêu cầu kỹ thuật**:
  - Chuẩn hóa Unicode NFKC (`unicodedata.normalize('NFKC', text)`) đưa các ký tự đồng dạng Cyrillic/Greek về Latin chuẩn.
  - Loại bỏ triệt để các ký tự tàng hình (Zero-Width Spaces `\u200B`, `\u200C`, `\u200D`, `\uFEFF`).
  - Phát hiện chuỗi có độ hỗn loạn entropy cao và tự động giải mã ngầm các đoạn mã hóa Base64 / Hexadecimal.
  - Tách hoặc loại bỏ các chuỗi Emoji xen kẽ cố tình làm vỡ từ (`i🔥g🔥n🔥o🔥r🔥e` $\rightarrow$ `ignore`).

---

### 🔹 Nhiệm vụ 5: Đo đạc thực nghiệm độc lập & Cập nhật Sổ tiến độ
- **Mục tiêu**: Thu thập số liệu đo đạc thực tế trên máy cá nhân của cả 4 thành viên, chuẩn bị báo cáo Meeting 6.
- **Yêu cầu kỹ thuật**:
  - Chuẩn bị tập dữ liệu kiểm thử gồm 10 tài liệu dài mẫu ($\approx 200\text{k ký tự}$): tài liệu kỹ thuật, báo cáo tài chính, sách điện tử (Ebook) có cấy câu lệnh tiêm nhiễm ở các vị trí khác nhau (đầu, giữa, cuối).
  - Đo đạc các chỉ số:
    * Độ trễ trung bình và phân vị $\text{P95}$ (mục tiêu $\text{P95} < 30\text{ms}$).
    * Tỷ lệ phát hiện (Recall) và tỷ lệ báo động giả ($\text{FPR} < 1.5\%$).
    * Tỷ lệ số block phải đẩy lên Tầng 2 (mục tiêu $< 20\%$).
  - Đồng bộ số liệu vào file Excel [`PI_GUARD_PROCESS_REPORT.xlsx`](file:///d:/Work/Do-an/Final-Report/reports/PI_GUARD_PROCESS_REPORT.xlsx).

---

## 👥 Nguyên Tắc Phối Hợp Nhóm (Anti-Siloing & Parallel Execution)

Tuân thủ nghiêm ngặt quy định trong [`AGENTS.md`](file:///d:/Work/Do-an/AGENTS.md):
- **Không phân chia chia cắt module**: Không gán thành viên này chỉ làm mô hình, thành viên kia chỉ làm web/data.
- **Ai cũng làm toàn bộ pipeline**: Cả 4 thành viên (Trường, Đức, Việt, Phương) cùng chạy độc lập mã nguồn nguyên mẫu trên máy cá nhân trong workspace của mình (`workspaces/<member>/`) để nắm chắc bản chất, so sánh chéo kết quả tại buổi họp nội bộ trước khi báo cáo GVHD.
- **Kế hoạch tiếp nối phân công từ Meeting 5**:
  - **Nguyễn Quí Đức** (tiếp nối Task 1 & 2): Phân tích cơ chế kết hợp 2 tầng dựa trên các vector tấn công và luồng Ingress.
  - **Đỗ Đoàn Duy Phương** (tiếp nối 4 bài báo y văn): Nghiên cứu kỹ thuật rà soát prompt giấu ở cuối và chuẩn bị tài liệu kiểm thử dài 200k ký tự.
  - **Phạm Minh Hoàng Việt** (tiếp nối cơ chế loại bỏ encoding): Hiện thực hóa và kiểm thử các hàm xử lý chuỗi của Lớp 0 (Tier-0 Ingress Scrubber).
  - **Nguyễn Văn Trường** (tiếp nối Task 3 Replication): Điều phối chung, hiện thực hóa module băm khối (`block_chunker.py`) và lượng tử hóa ONNX INT8 Tầng 2.

---

## 📚 Tài Liệu Tham Khảo (References)

- <a id="ref1"></a>**[[1]]** Hao Li, Xiaogeng Liu, Ning Zhang, and Chaowei Xiao. 2025. *PIGuard: Prompt Injection Guardrail via Mitigating Overdefense for Free*. In *Proc. ACL 2025*. [arXiv:2410.22770](https://arxiv.org/abs/2410.22770).
- <a id="ref4"></a>**[[4]]** K. Greshake et al. 2023. *Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection*. In *Proc. ACM AISec 2023*. [arXiv:2302.12173](https://arxiv.org/abs/2302.12173).
- <a id="ref9"></a>**[[9]]** P. He et al. 2023. *DeBERTaV3: Improving DeBERTa using ELECTRA-Style Pre-Training with Gradient-Disentangled Embedding Sharing*. In *Proc. ICLR 2023*. [arXiv:2111.09543](https://arxiv.org/abs/2111.09543).
- <a id="ref11"></a>**[[11]]** X. Shen et al. 2024. *Do Anything Now: Characterizing and Evaluating In-The-Wild Jailbreak Prompts on Large Language Models*. In *Proc. ACM CCS 2024*. [arXiv:2308.03825](https://arxiv.org/abs/2308.03825).
- <a id="ref17"></a>**[[17]]** Y. Yuan et al. 2024. *GPT-4 Is Too Smart To Be Safe: Stealthy Chat with LLMs via Cipher*. In *Proc. ICLR 2024*. [arXiv:2308.06463](https://arxiv.org/abs/2308.06463).
- <a id="ref19"></a>**[[19]]** J. Yi et al. 2025. *Benchmarking and Defending Against Indirect Prompt Injection Attacks on Large Language Models*. In *Proc. ACM KDD 2025*. [arXiv:2312.14197](https://arxiv.org/abs/2312.14197).
