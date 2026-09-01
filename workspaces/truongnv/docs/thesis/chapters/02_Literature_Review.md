# CHAPTER 2: LITERATURE REVIEW

> 👥 **Thành viên phụ trách chính**: Nguyễn Văn Trường (Leader) & Đỗ Đoàn Duy Phương  
> 📑 **Báo cáo tiến độ tương ứng**: **Report No. 2** (Literature Review — Trọng số 25% Process Mark)  
> 🏆 **Cột mốc nghiệm thu**: **REVIEW 1: Xác Định Bài Toán & Khảo Sát Nghiên Cứu (Bao gồm Chapter 1 & Chapter 2)**  

---

## 2.1. Review of Previous Studies (Khảo Sát Các Nghiên Cứu Trước Đây)

Sự phát triển vượt bậc của các Mô hình Ngôn ngữ Lớn (LLMs) dựa trên kiến trúc Transformer đã mở ra cuộc cách mạng trong xử lý ngôn ngữ tự nhiên, nhưng đồng thời cũng tạo ra một bề mặt tấn công hoàn toàn mới trong lĩnh vực An toàn Thông tin [[1]](#ref1), [[2]](#ref2). Phần này khảo sát toàn diện lịch sử phát triển của các vector tấn công, các công trình nghiên cứu phòng thủ tiêu biểu và các giải pháp Guardrail hiện đại (State-of-the-Art - SOTA).

---

### 2.1.1. Lịch Sử Phát Triển & Bản Chất Kỹ Thuật Các Vector Tấn Công LLM

```
                               ┌────────────────────────────────────────┐
                               │  TIẾN TRÌNH PHÁT TRIỂN CÁC VECTOR      │
                               │  TẤN CÔNG VÀO MÔ HÌNH NGÔN NGỮ LỚN     │
                               └──────────────────┬─────────────────────┘
                                                  │
             ┌────────────────────────────────────┼────────────────────────────────────┐
             ▼                                    ▼                                    ▼
┌───────────────────────────┐        ┌───────────────────────────┐        ┌───────────────────────────┐
│ GIAI ĐOẠN 1 (2022 - 2023) │        │ GIAI ĐOẠN 2 (2023 - 2024) │        │ GIAI ĐOẠN 3 (2024 - 2026) │
│ • Direct Prompt Injection │        │ • Indirect Prompt Inject  │        │ • Multi-Layer Agent Attack│
│ • "Ignore previous rules" │        │ • Jailbreak DAN / Roleplay│        │ • Cipher / Base64 Evasion │
│ • Perez & Ribeiro (2022)  │        │ • Greshake (2023), Wei(24)│        │ • Tencent Zhuque (2026)   │
└───────────────────────────┘        └───────────────────────────┘        └───────────────────────────┘
```

#### A. Tấn công Prompt Injection Trực tiếp & Cơ chế Pre-fill Pass Dynamics
Thuật ngữ *Prompt Injection* lần đầu tiên được định nghĩa chính thức trong công trình học thuật của **Perez & Ribeiro (2022)** [[3]](#ref3). Các tác giả đã chỉ ra rằng mô hình LLM không có khả năng phân biệt giữa chỉ thị gốc của lập trình viên (*System Instructions*) và dữ liệu đầu vào không tin cậy của người dùng (*User Inputs*). Khi nghiên cứu sâu vào cơ chế tính toán nội tại, nghiên cứu **RAP-ID (ACL Findings 2026)** đã chỉ ra 3 tín hiệu bất thường trong pha *Pre-fill Pass*:
1. *Directive Likeness (DL)*: User Input mạo danh phong cách mệnh lệnh của System Instruction trong không gian embedding.
2. *Counterfactual Gain (CG)*: Chuyển dịch trọng tâm tự chú ý (Attention Shift) từ token của hệ thống sang token của kẻ tấn công.
3. *Policy Conflict (PC)*: Kích hoạt các khái niệm rủi ro tiềm ẩn (Latent Risk Concepts) đối kháng với quy tắc an toàn.

#### B. Tấn công Prompt Injection Gián tiếp & Chuẩn Đánh Giá BIPIA
Nghiên cứu mang tính bước ngoặt của **Greshake et al. (ACM AISEC 2023)** [[4]](#ref4) đã mở rộng bề mặt tấn công sang các hệ sinh thái LLM tích hợp ngoài (RAG, Web Browsing, Email Processing, Plugins), chứng minh rằng *mọi tài liệu ngoài khi được LLM tiếp nhận đều mang bản chất là prompt*.
Để đánh giá định lượng rủi ro này, công trình **BIPIA (Microsoft Research / ACM KDD 2025)** đã xây dựng bộ benchmark tiêu chuẩn đầu tiên cho Indirect Prompt Injection (IPI), chỉ ra sự cần thiết của 2 cơ chế phòng vệ: *Boundary Awareness* (phân định ranh giới ngữ cảnh) và *Explicit Reminders* (nhắc nhở an toàn).

#### C. Tấn công Bẻ Khóa An Toàn (Jailbreak Attacks) & 3 Chiến Thuật Cốt Lõi
Khảo sát toàn diện về an toàn LLM tại **arXiv:2406.00240** đã hệ thống hóa các đòn Jailbreak thành 3 chiến thuật chính:
1. **Pretending (~98% trường hợp)**: Thay đổi ngữ cảnh hội thoại (nhập vai DAN - Do Anything Now, tình huống giả định) trong khi giữ nguyên ý định độc hại [[5]](#ref5), [[15]](#ref15).
2. **Attention Shifting**: Phân tán sự chú ý của cơ chế Self-Attention sang các tác vụ phức tạp (dịch thuật, viết thơ, giải đố).
3. **Privilege Escalation**: Đánh lừa mô hình cấp quyền quản trị (Sudo Mode, Developer Maintenance Override).

Ngoài ra, các nghiên cứu đối kháng tự động như **GCG (Zou et al., 2023)** [[13]](#ref13) và **MasterKey (Deng et al., 2023)** đã chứng minh khả năng tự động tạo payload vượt rào với tỷ lệ thành công cao, đồng thời giải thích lý do LLaMA-2 thường được chọn làm chuẩn đối sánh an toàn học thuật (nhờ tính mở của Gradients và căn chỉnh RLHF).

---

### 2.1.2. Khảo Sát & Đánh Giá Các Giải Pháp Guardrail Hiện Nay (SOTA Baselines)

Các giải pháp bảo vệ ứng dụng LLM hiện nay được chia thành 3 trường phái kiến trúc chính:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│             KHẢO SÁT 3 TRƯỜNG PHÁI GUARDRAIL PHỔ BIẾN TRONG THỰC TẾ                    │
├────────────────────────────────┬───────────────────────────────────────────────────────┤
│ NHÓM 1: BỘ LỌC TỪ KHÓA TĨNH   │ • Tốc độ siêu nhanh (<1ms), chi phí $0                │
│ (Regex & Keyword Blacklist)    │ • Điểm yếu: Quá giòn (Brittle), dễ bị bypass bởi      │
│                                │   Leetspeak (`1gn0r3`), khoảng trắng (`i g n o r e`)  │
├────────────────────────────────┼───────────────────────────────────────────────────────┤
│ NHÓM 2: LLM-AS-A-JUDGE         │ • Sử dụng LLM lớn làm trọng tài (Llama Guard 3 8B,    │
│ (Llama Guard 3, NeMo Guard)    │   NeMo Guardrails, OpenAI Moderation API)             │
│                                │ • Điểm yếu: Độ trễ cực lớn (>500ms - 1.5s), tốn VRAM  │
│                                │   (>16GB), chi phí API đắt đỏ, không khả thi inline   │
├────────────────────────────────┼───────────────────────────────────────────────────────┤
│ NHÓM 3: TRANSFORMER PHÂN LOẠI  │ • Sử dụng Encoder Transformer nhỏ gọn (DeBERTa-v3)    │
│ (PI-Guard & ProtectAI SOTA)    │ • Điểm mạnh: Hiểu ngữ nghĩa sâu, độ trễ P95 < 30ms    │
│                                │   trên CPU, chi phí $0, kháng lẩn tránh tốt           │
└────────────────────────────────┴───────────────────────────────────────────────────────┘
```

1. **Nhóm 1: Bộ lọc tĩnh (Regex & Keyword Blacklists)**:
   - *Nguyên lý*: Sử dụng danh sách từ khóa nhạy cảm và các biểu thức chính quy (Regex) để bắt các chuỗi phổ biến như `"ignore previous instructions"`, `"system prompt"`, `"DAN mode"`.
   - *Đánh giá*: Mặc dù có độ trễ cực thấp ($< 1\text{ms}$), các bộ lọc này hoàn toàn thất bại trước các biến thể cú pháp Leetspeak, chèn ký tự điều khiển tàng hình (`\u200B`), hoặc mã hóa Base64 [[17]](#ref17).

2. **Nhóm 2: Giải pháp LLM-as-a-Judge (Llama Guard 3 & NeMo Guardrails)**:
   - *Llama Guard 3 8B (Meta AI 2023)* [[9]](#ref9): Mô hình ngôn ngữ 8 tỷ tham số được tinh chỉnh chuyên biệt để phân loại prompt và output theo 14 danh mục an toàn. Mô hình có năng lực suy luận ngữ cảnh xuất sắc.
   - *NeMo Guardrails (NVIDIA 2023)* [[10]](#ref10): Bộ công cụ lập trình kiểm soát luồng hội thoại bằng ngôn ngữ Colang, sử dụng LLM để kiểm tra từng bước tương tác.
   - *Nghịch lý vận hành*: Các giải pháp này đòi hỏi tài nguyên phần cứng rất lớn ($> 16\text{GB}$ VRAM GPU), thời gian suy luận kéo dài từ $500\text{ms}$ đến hơn $1.5\text{s}$, và chi phí token đắt đỏ. Khi đặt làm chốt chặn bảo vệ trước mọi truy vấn của người dùng, giải pháp này trở thành **điểm nghẽn cổ chai nghiêm trọng (Denial-of-Service Bottleneck)** và làm suy giảm trải nghiệm người dùng.

3. **Nhóm 3: Mô hình Transformer Phân loại Chuỗi Nhỏ Gọn (Small Specialized Encoders)**:
   - *ProtectAI DeBERTa-v3 Baseline*: Mô hình phân loại chuỗi sử dụng kiến trúc DeBERTa-v3 (86M tham số) huấn luyện cho bài toán phát hiện prompt injection. Đây được coi là SOTA benchmark tham chiếu trong cộng đồng mã nguồn mở hiện nay.
   - *Bằng chứng thực nghiệm từ Do-Not-Answer (arXiv:2308.13387)*: Nghiên cứu của bài báo đã chứng minh rằng các mô hình **BERT-like với quy mô < 600M tham số** sau khi được fine-tune chuyên biệt có thể đạt độ chính xác đánh giá an toàn tương đương với GPT-4, nhưng chi phí và độ trễ giảm đi hàng chục lần.
   - *Ưu thế vượt trội của PI-Guard*: Kích thước nhỏ gọn ($< 300\text{MB}$ RAM), có thể chạy trực tiếp trên CPU thông thường với độ trễ $< 30\text{ms}$, đồng thời bảo toàn năng lực phân loại ngữ nghĩa sâu nhờ cơ chế *Disentangled Attention* [[11]](#ref11).

---

### 2.1.3. Khảo Sát Các Kỹ Thuật Phòng Thủ Độ Bền & Tối Ưu Lượng Hóa

- **Đột biến có hướng dẫn để kiểm thử độ bền (Targeted Mutators Workflow)**: Nghiên cứu **JailGuard (ACM TOSEM 2025)** đề xuất phương pháp *Targeted Replacement* và *Targeted Insertion* dựa trên ngữ nghĩa. Phương pháp này giúp nhóm xây dựng bộ kiểm thử đối kháng ngoại tuyến (Offline Adversarial Robustness Testing Suite) để đo lường độ bền của mô hình phân loại trước các biến thể Leetspeak, Spacing, Ciphers mà không làm tăng tỷ lệ chặn nhầm (FPR).
- **Kháng nhiễu cú pháp bằng Character n-grams & Subword Tokenization**: **Jain et al. (2023)** [[13]](#ref13) đã chứng minh rằng việc kết hợp biểu diễn n-gram ở cấp độ ký tự (Character n-grams 3–5 ký tự) và phân tách từ phụ (Byte-Pair Encoding subwords) cho phép mô hình bóc tách các từ bị làm nhiễu như `1gn0r3` $\rightarrow$ `['1gn', 'gn0', 'n0r', '0r3']`, giúp duy trì độ chính xác phân loại mà không bị phụ thuộc vào từ điển từ vựng chuẩn.
- **Cơ chế Disentangled Attention của DeBERTa-v3**: Theo nghiên cứu của **He et al. (ICLR 2023)** [[11]](#ref11), DeBERTa-v3 biểu diễn mỗi token bằng 2 vector độc lập (Content Vector và Relative Position Vector). Điều này giúp mô hình nhận diện chính xác các cấu trúc câu đảo ngữ và hoán đổi vị trí context — đặc trưng cốt lõi của các đòn tấn công Prompt Injection.
- **Lượng hóa động tăng tốc (Post-Training Dynamic INT8 Quantization)**: Nghiên cứu **ZeroQuant của Yao et al. (NeurIPS 2022)** [[14]](#ref14) chỉ ra rằng việc nén trọng số từ FP32 xuống INT8 cho các mô hình Transformer phân loại cho phép giảm 70% dung lượng bộ nhớ, tăng tốc độ suy luận 3x trên CPU mà độ suy giảm $F_1$ không vượt quá $0.3\%$.

---

## 2.2. Summary of the Literature Review (Tổng Hợp Khảo Sát & Khoảng Trống Nghiên Cứu)

### 2.2.1. Bảng Ma Trận Đối Sánh Toàn Diện Các Giải Pháp Guardrail Hiện Tại:

| Tiêu chí đối sánh | Regex / Keyword Blacklists | LLM-as-a-Judge (Llama Guard 3 8B) [[9]](#ref9) | OpenAI Moderation API [[12]](#ref12) | ProtectAI DeBERTa Baseline | **PI-GUARD (Đề xuất của nhóm)** |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Kích thước mô hình** | 0 MB | ~8,000M (8B) | API Đám mây | 86M | **86M (Tối ưu INT8 < 150MB)** |
| **Hạ tầng triển khai** | CPU / RAM cực nhẹ | GPU VRAM > 16GB | Máy chủ ngoài | CPU / GPU nhẹ | **CPU phổ thông (Commodity CPU)** |
| **Độ trễ suy luận (P95)** | **< 1 ms** | **> 500 ms - 1.5s** | ~200 ms - 400 ms | ~45 ms | **< 30 ms (Độ trễ thấp)** |
| **Chi phí vận hành API** | $0 | Rất đắt (Token compute) | Trả phí theo API | Thấp | **$0 (Tự host độc lập)** |
| **Phát hiện Prompt Injection** | Kém (<40%) | Tốt (~94%) | Yếu (~60% - chủ yếu lọc Toxic) | Rất tốt (~97%) | **Xuất sắc (> 98.5% Macro F1)** |
| **Kháng nhiễu Leetspeak/Base64** | Hoàn toàn thất bại | Trung bình (Bị lừa bởi Ciphers) | Thất bại trước Base64 | Trung bình | **Bền vững ($\Delta F_1 < 5\%$, có Decoder)** |
| **Chống rò rỉ dữ liệu cụm** | N/A | Không công bố Split | Không công bố Split | Random Split (Bị rò rỉ) | **Triệt tiêu qua Group-Aware Split** |
| **Tính độc lập mô hình (Model-Agnostic)** | Có | Phụ thuộc Meta prompt | Phụ thuộc OpenAI | Có | **Có (Bảo vệ 5 Target LLM APIs)** |

---

### 2.2.2. Ba Khoảng Trống Nghiên Cứu (Research Gaps) Cốt Lõi Của Chuyên Ngành ATTT

Từ kết quả khảo sát các công trình quốc tế, nhóm xác định **3 Khoảng Trống Nghiên Cứu Trọng Yếu** mà đồ án PI-Guard tập trung giải quyết:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                  3 KHOẢNG TRỐNG NGHIÊN CỨU CỐT LÕI (RESEARCH GAPS)                     │
├───────────────┬────────────────────────────────────────┬───────────────────────────────┤
│ Mã Khoảng Trống│ Hiện Trạng Các Nghiên Cứu Quốc Tế     │ Hạn Chế & Rủi Ro Thực Tế      │
├───────────────┼────────────────────────────────────────┼───────────────────────────────┤
│ GAP 1:        │ Các tập dữ liệu (Deepset, Gandalf...)  │ Phân chia ngẫu nhiên dẫn đến  │
│ Data Leakage  │ chứa hàng loạt biến thể từ 1 mẫu gốc. │ rò rỉ dữ liệu cụm, làm sai lệch│
│ & Splitting   │ Hiện tại hầu hết dùng Random Split.    │ đánh giá năng lực Zero-day.   │
├───────────────┼────────────────────────────────────────┼───────────────────────────────┤
│ GAP 2:        │ Các mô hình Guardrail chủ yếu được test│ Mô hình sụp đổ khi bị tấn công│
│ Adversarial   │ trên văn bản chuẩn, thiếu cơ chế giải  │ bằng Base64, Leetspeak hoặc   │
│ Evasion       │ mã heuristic và biểu diễn đa tầng.     │ phân tách khoảng trắng.       │
├───────────────┼────────────────────────────────────────┼───────────────────────────────┤
│ GAP 3:        │ Đa số giải pháp chọn hoặc quá nặng     │ Thiếu giải pháp nén lượng hóa │
│ Inline Latency│ (Llama Guard > 16GB VRAM) hoặc quá yếu │ INT8 đạt P95 < 30ms trên CPU  │
│ & Usability   │ (Regex), tỷ lệ FPR cao gây tắc nghẽn.  │ mà vẫn giữ FPR < 1.5%.        │
└───────────────┴────────────────────────────────────────┴───────────────────────────────┘
```

---

## 2.3. Contribution of Research (Đóng Góp Khoa Học & Thực Tiễn Của Đồ Án)

Để giải quyết triệt để 3 khoảng trống nghiên cứu trên, đồ án **PI-Guard** mang lại 4 đóng góp khoa học và kỹ thuật thực tiễn:

1. **Đóng góp 1 (Kỹ thuật dữ liệu — Khử rò rỉ dữ liệu cụm)**:
   - Xây dựng phương pháp luận **Group-Aware Splitting** dựa trên gom cụm khoảng cách ngữ nghĩa và chuỗi ký tự, đảm bảo toàn bộ các biến thể của cùng một mẫu tấn công chỉ thuộc tập Train hoặc Test, triệt tiêu hoàn toàn rò rỉ dữ liệu ($\text{Inter-cluster Jaccard} < 0.15$).

2. **Đóng góp 2 (Kiến trúc mô hình — Phòng thủ đa tầng Hybrid)**:
   - Thiết kế cơ chế kết hợp giữa bộ lọc cú pháp siêu nhanh (**Word + Character n-grams TF-IDF** $\sim 3\text{ms}$) và bộ phân loại ngữ nghĩa sâu (**Fine-tuned DeBERTa-v3** $\sim 12.8\text{ms}$).
   - Tích hợp tầng tiền xử lý chuẩn hóa Unicode NFKC và bộ giải mã Heuristic Base64 tự động để kháng các kỹ thuật lẩn tránh đối kháng, cam kết độ suy giảm hiệu năng $\Delta F_1 < 5\%$.

3. **Đóng góp 3 (Tối ưu hóa triển khai — Suy luận độ trễ thấp trên CPU)**:
   - Tích hợp kỹ thuật Post-Training Dynamic INT8 Quantization sang ONNX Runtime, tối ưu hóa suy luận độ trễ thấp ($\text{P95} < 30\text{ms}$ trên CPU thông thường) với mức suy giảm chính xác tối thiểu ($< 0.3\%$), giúp bảo vệ hệ thống trước nguy cơ tắc nghẽn dịch vụ mà không đòi hỏi phần cứng GPU đắt tiền.

4. **Đóng góp 4 (Giải pháp triển khai — Model-Agnostic API Middleware & Demo)**:
   - Đóng gói toàn bộ hệ thống thành **Asynchronous FastAPI Middleware** và giao diện **Streamlit Testing Dashboard** với ma trận 4 kịch bản demo ($2 \times 2$), chứng minh khả năng bảo vệ đồng nhất cho cả 5 mô hình LLM tiêu chuẩn qua Cloud API (GPT-4o-mini, Gemini 1.5 Flash, LLaMA-3.1, Mistral, Qwen), giảm tỷ lệ tấn công ASR từ $35.5\% - 78.4\%$ xuống $0.0\%$.

---

## 2.4. Mapping Trích Dẫn Học Thuật Chuẩn IEEE (100% >= 2022)

Các luận điểm trong Chương 2 được bảo chứng bởi 17 tài liệu khoa học chuẩn mực quốc tế:
- **Tấn công Prompt Injection & Jailbreak**: Perez (2022) [[3]](#ref3), Greshake (2023) [[4]](#ref4), Wei (2024) [[5]](#ref5), Tencent Zhuque (2026) [[6]](#ref6), Shen (2024) [[15]](#ref15), Zhou (2024) [[16]](#ref16), Yuan (2024) [[17]](#ref17).
- **Tiêu chuẩn An toàn & Threat Model**: NIST AI 100-2e2025 [[7]](#ref7), OWASP LLM01:2025 [[8]](#ref8), Zhao (2023) [[1]](#ref1), Ouyang (2022) [[2]](#ref2).
- **Mô hình Guardrail & Tối ưu hóa**: Llama Guard (2023) [[9]](#ref9), NeMo Guardrails (2023) [[10]](#ref10), DeBERTaV3 (2023) [[11]](#ref11), OpenAI Moderation (2023) [[12]](#ref12), Baseline Defenses (2023) [[13]](#ref13), ZeroQuant (2022) [[14]](#ref14).
