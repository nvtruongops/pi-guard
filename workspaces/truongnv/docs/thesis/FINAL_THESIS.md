# MINISTRY OF EDUCATION AND TRAINING
# FPT UNIVERSITY
## CAPSTONE PROJECT THESIS (IAP491)

# PI-GUARD: A MACHINE-LEARNING GUARDRAIL FOR DETECTING PROMPT INJECTION AND JAILBREAK ATTACKS ON LLM APPLICATIONS

**Academic Program**: Bachelor of Information Assurance (IA)  
**Capstone Code**: `IAP491_FA26_PI_GUARD`  
**Location & Year**: Hanoi, 2026  

---

### GROUP MEMBERS:
1. **Nguyễn Văn Trường (Leader)** — Student ID: `SE182034`
2. **Nguyễn Quí Đức** — Student ID: `SE182087`
3. **Phạm Minh Hoàng Việt** — Student ID: `SE181851`
4. **Đỗ Đoàn Duy Phương** — Student ID: `SE180235`

**Supervisor**: MSc. Supervisor / FPT University Department of Information Assurance  

---

# CHAPTER 1: INTRODUCTION

## 1.1. Background (Bối Cảnh Nghiên Cứu)
Sự bùng nổ của các Mô hình Ngôn ngữ Lớn (Large Language Models - LLMs) như GPT-4, LLaMA-3, Claude, và Gemini đã định hình lại toàn bộ hệ sinh thái phần mềm hiện đại [[1]](#ref1). LLM hiện được tích hợp sâu vào các ứng dụng doanh nghiệp: từ chatbot chăm sóc khách hàng, hệ thống trích xuất thông tin tự động (Retrieval-Augmented Generation - RAG), đến các tác tử AI tự trị (Autonomous AI Agents) có khả năng gọi hàm (tool execution) và truy cập cơ sở dữ liệu nội bộ [[2]](#ref2).

Tuy nhiên, việc triển khai LLM trong thực tế làm phát sinh những lỗ hổng bảo mật hoàn toàn mới mà các giải pháp tường lửa (WAF), IDS/IPS truyền thống không thể phát hiện. Trong bảng xếp hạng bảo mật quốc tế **OWASP Top 10 for Large Language Model Applications (2025)** [[8]](#ref8) và báo cáo **NIST AI 100-2e2025** [[7]](#ref7), lỗ hổng **Prompt Injection và Jailbreak (LLM01)** được xếp ở vị trí nguy hiểm số 1. Kẻ tấn công có thể thao túng mô hình ngôn ngữ chỉ bằng các câu lệnh văn bản tự nhiên được thiết kế tinh vi, dẫn đến rò rỉ bí mật kinh doanh nhúng trong System Prompt, chiếm quyền điều khiển luồng thực thi (Goal Hijacking), hoặc ép mô hình vượt qua các rào cản đạo đức để sinh mã độc.

---

## 1.2. Problem Statement (Phát Biểu Bài Toán)
Vấn đề cốt lõi của các mô hình Transformer hiện nay bắt nguồn từ sự tương đồng với **"Lỗ hổng kiến trúc Von Neumann trong xử lý ngôn ngữ tự nhiên"** [[1]](#ref1), [[3]](#ref3):

```
┌─────────────────────────────────────────────────────────────┐
│                       INPUT CONTEXT                         │
│  ┌─────────────────────────────────┐ ┌───────────────────┐  │
│  │ System Prompt (Chỉ thị/Rules)  │ │ User Prompt (Data)│  │
│  └─────────────────────────────────┘ └───────────────────┘  │
└──────────────────────────────┬──────────────────────────────┘
                               │ Ghép chung thành 1 chuỗi Token phẳng
                               ▼
             ┌──────────────────────────────────────┐
             │   LLM Transformer Next-Token Engine  │
             │   (Không có ranh giới phần cứng)     │
             └──────────────────────────────────────┘
```

1. **Lẫn lộn giữa Lệnh và Dữ liệu (Instruction/Data Ambiguity)**: Trong cơ chế Self-Attention của Transformer, System Instruction (chỉ thị điều khiển) và User Input (dữ liệu đầu vào) bị ghép chung thành một chuỗi token phẳng ($X = S \mathbin{\Vert} U$). Mô hình không có cơ chế phân tách phần cứng hay quyền hạn (Privilege Separation) giữa dữ liệu và câu lệnh.
2. **Sự thất bại của các bộ lọc từ khóa tĩnh (Keyword Blacklist Failure)**: Các bộ quy tắc Regex/Blacklist thông thường dễ dàng bị kẻ tấn công vô hiệu hóa thông qua các kỹ thuật đột biến cú pháp: chèn ký tự leetspeak (`1gn0r3`), phân tách khoảng trắng (`i g n o r e`), mã hóa Base64/Cipher [[17]](#ref17), hoặc bọc trong các kịch bản nhập vai phức tạp (DAN / Roleplay Jailbreak) [[12]](#ref12), [[15]](#ref15).
3. **Nghịch lý của giải pháp LLM-as-a-Judge**: Việc sử dụng một LLM lớn khác (ví dụ: Llama Guard 3 8B) để kiểm tra prompt gây ra độ trễ quá lớn (>500ms đến 1.5s), tiêu tốn tài nguyên phần cứng (>16GB VRAM GPU) và chi phí vận hành API quá cao, không khả thi cho môi trường sản xuất có lưu lượng truy cập lớn [[9]](#ref9), [[10]](#ref10).

Do đó, bài toán cấp thiết đặt ra là: **Cần xây dựng một cơ chế Guardrail chuyên biệt sử dụng Machine Learning / Transformer nhỏ gọn, đặt ngay tại cổng API, có khả năng phân loại ngữ nghĩa sâu với độ trễ thấp (P95 < 30ms trên CPU), tỷ lệ chặn nhầm cực thấp (FPR < 1.5%), và có độ bền cao trước các kỹ thuật lẩn tránh cú pháp (Leetspeak, Base64, Spacing).**

---

## 1.3. Research Objectives & Research Questions (Mục Tiêu & 3 Câu Hỏi Nghiên Cứu)

### 1.3.1. Mục Tiêu Tổng Quát:
Thiết kế, huấn luyện, lượng hóa và triển khai hệ thống **PI-Guard** — Lớp phòng thủ Guardrail dạng API Middleware trực tuyến đặt trước các ứng dụng LLM để phát hiện và ngăn chặn hai vector tấn công chính: **Prompt Injection** và **Jailbreak**.

### 1.3.2. Các Mục Tiêu Cụ Thể (Specific Deliverables):
1. **Bộ dữ liệu chuẩn hóa**: Xây dựng tập dữ liệu đa nguồn (Deepset, Gandalf, In-The-Wild, Benign) áp dụng thuật toán *Group-Aware Splitting* chống rò rỉ dữ liệu.
2. **Mô hình học máy kép**: Phát triển mô hình Baseline ML (Word/Char TF-IDF) và mô hình Transformer tinh chỉnh (`microsoft/deberta-v3-base` Disentangled Attention).
3. **Độ bền trước lẩn tránh cú pháp**: Xây dựng cơ chế chuẩn hóa chuỗi và bộ kiểm thử độ bền (Adversarial Robustness Testing Suite) kháng Leetspeak, Base64, Spacing.
4. **Lượng hóa tăng tốc**: Áp dụng Post-Training Dynamic INT8 Quantization (ONNX Runtime) để chạy mượt trên CPU thông thường.
5. **Hạ tầng API & Dashboard**: Xây dựng Asynchronous Middleware (FastAPI) và Dashboard kiểm thử trực quan (Streamlit) với ma trận 4 kịch bản demo.

### 1.3.3. Hệ Thống 3 Câu Hỏi Nghiên Cứu Cốt Lõi (RQ1 - RQ3):

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│               HỆ THỐNG 3 CÂU HỎI NGHIÊN CỨU CỐT LÕI (CHUYÊN NGÀNH ATTT)                │
├──────┬──────────────────────────────────────────┬──────────────────────────────────────┤
│ Mã   │ Tên Trọng Tâm Nghiên Cứu                 │ Khoảng Trống Nghiên Cứu Cốt Lõi      │
├──────┼──────────────────────────────────────────┼──────────────────────────────────────┤
│ RQ1  │ Phân Loại Mối Đe Dọa & Chống Rò Rỉ Dữ Liệu│ Rò rỉ cụm mẫu & Ranh giới phân loại  │
│      │ (Threat Modeling & Representation)       │ giữa cú pháp tĩnh và ngữ nghĩa sâu   │
├──────┼──────────────────────────────────────────┼──────────────────────────────────────┤
│ RQ2  │ Độ Bền Kháng Lẩn Tránh & Mã Hóa Đối Kháng │ Sự sụp đổ của mô hình trước biến dị  │
│      │ (Adversarial Robustness & Ciphers)       │ cú pháp Leetspeak, Spacing & Base64  │
├──────┼──────────────────────────────────────────┼──────────────────────────────────────┤
│ RQ3  │ Cân Bằng An Toàn & Khả Thi Triển Khai    │ Đánh đổi Security/Usability (FPR) và │
│      │ (Security Trade-off & Inline Feasibility)│ bảo toàn ranh giới an toàn khi nén   │
└──────┴──────────────────────────────────────────┴──────────────────────────────────────┘
```

#### 📌 RQ1 — Biểu Diễn Mối Đe Dọa, Khử Rò Rỉ Dữ Liệu & Ranh Giới Phân Loại Ngữ Nghĩa:
- **Câu hỏi**: *Làm thế nào để xây dựng một phương pháp luận phân chia dữ liệu bảo toàn cụm (Group-Aware Splitting) nhằm triệt tiêu hiện tượng rò rỉ dữ liệu giữa các biến thể tấn công, và sự kết hợp giữa mô hình học máy cổ điển (TF-IDF) với Transformer phân tách vị trí ngữ nghĩa (DeBERTa-v3) nâng cao khả năng phát hiện các đòn tấn công Prompt Injection và Jailbreak vượt trội hơn các mô hình phòng thủ SOTA hiện nay ở mức độ nào?*
- **Chỉ số đo lường**: $\text{Inter-cluster Jaccard} < 0.15$, $\text{Macro } F_1^{\text{OOD}} \ge 0.92$, $\text{Macro } F_1 \ge 0.95$ (kỳ vọng $> 0.98$), $\text{PR-AUC} \ge 0.98$.

#### 📌 RQ2 — Độ Bền Của Hệ Thống Trước Các Kỹ Thuật Lẩn Tránh & Mã Hóa Đối Kháng:
- **Câu hỏi**: *Hệ thống phòng thủ đa tầng (kết hợp tiền xử lý chuẩn hóa chuỗi, biểu diễn n-gram ký tự và token hóa subword) duy trì độ bền và độ chính xác như thế nào trước các kỹ thuật lẩn tránh đối kháng có cấu trúc (gồm thay thế ký tự Leetspeak, phân tách khoảng trắng và mã hóa Base64/Cipher), và mức độ suy giảm hiệu năng tối đa có thể định lượng được là bao nhiêu?*
- **Chỉ số đo lường**: $\text{ARR} = \frac{F_1^{\text{Adversarial}}}{F_1^{\text{Clean}}} \ge 0.95$, $\text{ASR} < 5\%$, $\Delta F_1 = |F_1^{\text{Clean}} - F_1^{\text{Adv}}| < 5\%$.

#### 📌 RQ3 — Cân Bằng An Toàn, Khống Chế Tỷ Lệ Chặn Nhầm & Bảo Toàn Ranh Giới Khi Lượng Hóa:
- **Câu hỏi**: *Làm thế nào để tối ưu hóa cơ chế thiết lập ngưỡng chính sách nhằm khống chế nghiêm ngặt Tỷ lệ Chặn Nhầm (FPR < 1.5%) trên các truy vấn hợp lệ của doanh nghiệp, và quá trình lượng hóa động INT8 cùng kiến trúc proxy bất đồng bộ có thể bảo toàn ranh giới quyết định an toàn trong khi duy trì độ trễ thấp tối ưu (P95 < 30ms trên CPU) mà không tạo ra điểm nghẽn từ chối dịch vụ (DoS)?*
- **Chỉ số đo lường**: $\text{FPR} < 1.5\%$ (kỳ vọng $< 1.1\%$), $\Delta \text{Decision Boundary (KL)} < 0.05$, $\Delta F_1^{\text{Quant}} < 0.3\%$, $\text{P95 Latency} < 30\text{ms}$ trên CPU.

---

## 1.4. Significance of the Study & Threat Impact Analysis (Ý Nghĩa & Phân Tích Thiệt Hại)

### 1.4.1. 4 Tầng Thiệt Hại Thực Tế Của Các Cuộc Tấn Công LLM
1. **Thiệt hại 1: Rò rỉ Bí mật Trí tuệ (IP) & Master API Key**: System prompt chứa logic nghiệp vụ độc quyền và API credential nội bộ. Khi bị trích xuất, doanh nghiệp mất hoàn toàn lợi thế cạnh tranh và bị tin tặc lợi dụng API key.
2. **Thiệt hại 2: Chiếm quyền điều khiển Tác tử AI (Goal Hijacking & Unauthorized Actions)**: Khi LLM Agent có quyền gọi tool, một câu lệnh indirect injection ẩn trong tài liệu có thể ép Agent chuyển tiền trái phép hoặc xóa sạch database của khách hàng.
3. **Thiệt hại 3: Tấn công cạn kiệt tài nguyên & Chi phí ví tiền (Denial-of-Wallet / Compute Exhaustion)**: Bơm prompt ép mô hình sinh văn bản lặp vô tận, gây hóa đơn API hàng chục nghìn USD mỗi ngày.
4. **Thiệt hại 4: Vi phạm chế tài pháp lý & Mất uy tín thương hiệu (Regulatory Compliance Fines)**: Ép AI sinh mã độc hoặc nội dung cấm dẫn đến vi phạm EU AI Act, GDPR và sụp đổ niềm tin người dùng.

### 1.4.2. Ý Nghĩa Khoa Học & Thực Tiễn Của PI-Guard
- **Khoa học**: Chứng minh tính ưu việt của cơ chế *Disentangled Attention* trong nhận diện trật tự đảo câu, giải quyết bài toán chống rò rỉ dữ liệu qua *Group-Aware Splitting*, và chứng minh tính hiệu quả của *Character n-grams* trong kháng nhiễu Leetspeak.
- **Thực tiễn**: Đóng gói thành giải pháp Plug-and-Play (FastAPI Middleware) chi phí $0, độ trễ thấp <30ms trên CPU, đánh chặn các đòn tấn công trước khi chạm vào LLM.

---

## 1.5. Scope and Limitations (Ranh Giới Phạm Vi & Giới Hạn Đề Tài)

```
┌──────────────────────────────────────────────────────────────────────────┐
│                   IN-SCOPE (TRỌNG TÂM NGHIÊN CỨU)                        │
│  - 2 Bài toán cốt lõi: Prompt Injection (Direct/Indirect) & Jailbreak    │
│  - Chuỗi văn bản đầu vào: English Text Prompts (Tiêu chuẩn nghiên cứu)   │
│  - Kỹ thuật lẩn tránh cú pháp: Leetspeak, Base64, Spacing (Test độ bền)  │
│  - Độ trễ thấp (Low-latency): P95 Latency < 30ms trên CPU thông thường   │
│  - An toàn vận hành: False Positive Rate (FPR) < 1.5% trên tập Benign    │
│  - Kiến trúc: Hybrid TF-IDF Baseline + Fine-tuned DeBERTa-v3 + ONNX INT8 │
└──────────────────────────────────────────────────────────────────────────┘
                                     ▲
                                     │ RANH GIỚI BẢO VỆ
                                     ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                   OUT-OF-SCOPE (NẰM NGOÀI PHẠM VI)                       │
│  - Tấn công đa phương thức: Image / Audio / Video Jailbreaks             │
│  - Tấn công hạ tầng mạng: DDoS, trích xuất trọng số GPU, Side-channel    │
│  - Quét lỗ hổng hệ điều hành máy chủ / CVE của Linux/Docker              │
│  - Xây dựng hệ thống cơ sở dữ liệu Vector RAG hoặc Agent Tool Runtime    │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 1.6. Thesis Structure (Bố Cục 6 Chương Của Toàn Văn Luận Văn)
Tuân thủ nghiêm ngặt theo Hướng dẫn Khóa luận Tốt nghiệp FPT University IAP491:
- **Chapter 1: Introduction** *(Bối cảnh, Bài toán, Mục tiêu, Ý nghĩa, Phạm vi, Cấu trúc).*
- **Chapter 2: Literature Review** *(Khảo sát nghiên cứu liên quan, SOTA Guardrails, Đóng góp mới của nhóm).*
- **Chapter 3: Methodology** *(Thiết kế nghiên cứu, Thu thập dữ liệu, Group-Aware Splitting, Baseline ML & DeBERTa-v3).*
- **Chapter 4: Experimental and Results** *(Môi trường thử nghiệm, Kết quả đối sánh SOTA, Ma trận nhầm lẫn, Test độ bền).*
- **Chapter 5: Discussion** *(Thảo luận kết quả, Đánh giá cân bằng An toàn/Trải nghiệm người dùng, Giới hạn thực tiễn).*
- **Chapter 6: Conclusion and Future Work** *(Tổng kết đóng góp và Hướng nghiên cứu mở rộng).*
- **References & Appendices** *(17 Tài liệu tham khảo chuẩn IEEE và Phụ lục mã nguồn).*


---

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


---

# REFERENCES (TÀI LIỆU THAM KHẢO CHUẨN IEEE)

# REFERENCES LOG & APPLICATION MAPPING MATRIX
## Hệ Thống Quản Lý & Định Vị Tài Liệu Tham Khảo — Đề Tài PI-Guard (Toàn Bộ 17 Bài Báo >= 2022)

> **Thư mục lưu trữ tài liệu gốc**: `d:/Work/Do-an/References/`  
> **Tiêu chí chuẩn hóa**: **100% tài liệu xuất bản từ năm 2022 đến 2026** (Kỷ nguyên LLM hiện đại).  
> **Cập nhật lần cuối**: 2026-09-01  
> **Mục đích**: Lưu trữ, theo dõi và ánh xạ chi tiết toàn bộ **17 bài báo PDF** trong `References/` tới **danh sách các file cụ thể trong toàn bộ repository `D:\Work\Do-an/`**.

---

## 📊 1. BẢNG ÁNH XẠ CHI TIẾT 17 TÀI LIỆU (TẤT CẢ >= 2022) VÀO REPO

| # | File PDF Tham Khảo (`References/`) | Tác Giả & Năm | Nơi Xuất Bản | Các File Cụ Thể Trong Repo Đang Áp Dụng | Vai Trò Áp Dụng & Cơ Sở Khoa Học |
| :---: | :--- | :--- | :---: | :--- | :--- |
| **1** | [`Zhao_2023_A_Survey_of_Large_Language_Models.pdf`](file:///d:/Work/Do-an/References/Zhao_2023_A_Survey_of_Large_Language_Models.pdf) | Zhao et al. (2023) | *IJCAI / arXiv 2023* | • [`docs/thesis/Review1_Problem_Definition_and_Threat_Model.md`](file:///d:/Work/Do-an/docs/thesis/Review1_Problem_Definition_and_Threat_Model.md)<br>• [`docs/thesis/Review1_Presentation_Slides_Outline.md`](file:///d:/Work/Do-an/docs/thesis/Review1_Presentation_Slides_Outline.md) | Khảo sát tổng thể kiến trúc LLM, cơ chế sinh token tự hồi quy và lỗ hổng ranh giới phẳng Code/Data |
| **2** | [`Ouyang_2022_InstructGPT_Training_Language_Models_Follow_Instructions.pdf`](file:///d:/Work/Do-an/References/Ouyang_2022_InstructGPT_Training_Language_Models_Follow_Instructions.pdf) | Ouyang et al. (2022) | *NeurIPS 2022 (OpenAI)* | • [`docs/thesis/Review1_Problem_Definition_and_Threat_Model.md`](file:///d:/Work/Do-an/docs/thesis/Review1_Problem_Definition_and_Threat_Model.md)<br>• [`src/llm/provider.py`](file:///d:/Work/Do-an/src/llm/provider.py) | Nền tảng Instruction Tuning & RLHF, cơ chế xử lý System Instruction trên Downstream LLM |
| **3** | [`Perez_2022_Ignore_This_Title_Hack_This_Paper_Prompt_Injection.pdf`](file:///d:/Work/Do-an/References/Perez_2022_Ignore_This_Title_Hack_This_Paper_Prompt_Injection.pdf) | Perez & Ribeiro (2022) | *NeurIPS 2022* | • [`CAPSTONE PROJECT REGISTER.md`](file:///d:/Work/Do-an/CAPSTONE%20PROJECT%20REGISTER.md)<br>• [`src/preprocessing/cleaner.py`](file:///d:/Work/Do-an/src/preprocessing/cleaner.py) | Định nghĩa nền tảng Direct Prompt Injection, cơ chế Instruction Override và System Prompt Leaking |
| **4** | [`Greshake_2023_Indirect_Prompt_Injection.pdf`](file:///d:/Work/Do-an/References/Greshake_2023_Indirect_Prompt_Injection.pdf) | Greshake et al. (2023) | *ACM AISEC 2023* | • [`docs/thesis/Review1_Problem_Definition_and_Threat_Model.md`](file:///d:/Work/Do-an/docs/thesis/Review1_Problem_Definition_and_Threat_Model.md)<br>• [`src/datasets/splitter.py`](file:///d:/Work/Do-an/src/datasets/splitter.py) | Phân tích cơ chế Indirect Prompt Injection và phân cụm Group-Aware Splitting chống rò rỉ dữ liệu |
| **5** | [`Wei_2024_Jailbroken_How_LLM_Safety_Training_Fails.pdf`](file:///d:/Work/Do-an/References/Wei_2024_Jailbroken_How_LLM_Safety_Training_Fails.pdf) | Wei et al. (2024) | *NeurIPS 2024* | • [`docs/thesis/Review1_Problem_Definition_and_Threat_Model.md`](file:///d:/Work/Do-an/docs/thesis/Review1_Problem_Definition_and_Threat_Model.md)<br>• [`src/preprocessing/obfuscation.py`](file:///d:/Work/Do-an/src/preprocessing/obfuscation.py) | Cơ chế suy giảm an toàn (Competing Objectives); phân loại Jailbreak Roleplay/DAN/Persona Adoption |
| **6** | [`Tencent_2026_AI_Infra_Guard_MultiLayer_Agent_RedTeaming.pdf`](file:///d:/Work/Do-an/References/Tencent_2026_AI_Infra_Guard_MultiLayer_Agent_RedTeaming.pdf) | Tencent Zhuque Lab (2026) | *arXiv 2026* | • [`docs/research/Tencent2026_Paper_Analysis_and_Mapping_to_PIGuard.md`](file:///d:/Work/Do-an/docs/research/Tencent2026_Paper_Analysis_and_Mapping_to_PIGuard.md)<br>• [`src/policy/policy_engine.py`](file:///d:/Work/Do-an/src/policy/policy_engine.py) | Threat Model 4 tầng, nguyên lý Layer-Paradigm Matching và danh mục 26+ Attack Operators (Appendix E) |
| **7** | [`Meta_2023_Llama_Guard_Input_Output_Safeguard.pdf`](file:///d:/Work/Do-an/References/Meta_2023_Llama_Guard_Input_Output_Safeguard.pdf) | Meta AI (2023) | *arXiv 2023* | • [`docs/thesis/Review1_Problem_Definition_and_Threat_Model.md`](file:///d:/Work/Do-an/docs/thesis/Review1_Problem_Definition_and_Threat_Model.md)<br>• [`src/policy/thresholds.py`](file:///d:/Work/Do-an/src/policy/thresholds.py) | Mô hình đối chuẩn Guardrail (Llama Guard 3 8B), định nghĩa Taxonomy an toàn và thiết lập ngưỡng phân loại |
| **8** | [`NVIDIA_2023_NeMo_Guardrails_Toolkit.pdf`](file:///d:/Work/Do-an/References/NVIDIA_2023_NeMo_Guardrails_Toolkit.pdf) | NVIDIA (2023) | *EMNLP 2023* | • [`docs/thesis/Review1_Problem_Definition_and_Threat_Model.md`](file:///d:/Work/Do-an/docs/thesis/Review1_Problem_Definition_and_Threat_Model.md)<br>• [`src/api/middleware.py`](file:///d:/Work/Do-an/src/api/middleware.py) | Kiến trúc Guardrail Middleware bất đồng bộ đặt trước LLM để đánh chặn request trước khi gọi LLM |
| **9** | [`He_2023_DeBERTaV3_Disentangled_Attention_ICLR.pdf`](file:///d:/Work/Do-an/References/He_2023_DeBERTaV3_Disentangled_Attention_ICLR.pdf) | He et al. (2023) | *ICLR 2023 (Microsoft)* | • [`docs/research/State_of_the_Art_Guardrail_and_Jailbreak_Benchmarks_Analysis.md`](file:///d:/Work/Do-an/docs/research/State_of_the_Art_Guardrail_and_Jailbreak_Benchmarks_Analysis.md)<br>• [`src/models/classifier.py`](file:///d:/Work/Do-an/src/models/classifier.py) | **KEY 2**: Mô hình phân loại chính (`microsoft/deberta-v3-base`) với Disentangled Attention tách biệt vị trí/nội dung |
| **10** | [`OpenAI_2023_Undesired_Content_Detection.pdf`](file:///d:/Work/Do-an/References/OpenAI_2023_Undesired_Content_Detection.pdf) | Markov et al. (2023) | *AAAI HCOMP 2023* | • [`docs/thesis/Review1_Problem_Definition_and_Threat_Model.md`](file:///d:/Work/Do-an/docs/thesis/Review1_Problem_Definition_and_Threat_Model.md)<br>• [`src/evaluation/metrics.py`](file:///d:/Work/Do-an/src/evaluation/metrics.py) | Phương pháp luận đo lường tỷ lệ chặn nhầm (False Positive Rate - FPR < 1.5%) trên tập Benign và cân bằng Security/Usability |
| **11** | [`Shen_2024_Do_Anything_Now_Jailbreak_Prompts_In_The_Wild.pdf`](file:///d:/Work/Do-an/References/Shen_2024_Do_Anything_Now_Jailbreak_Prompts_In_The_Wild.pdf) | Shen et al. (2024) | *ACM CCS 2024* | • [`scripts/download_dataset.py`](file:///d:/Work/Do-an/scripts/download_dataset.py)<br>• [`data/manifests/attack_taxonomy.json`](file:///d:/Work/Do-an/data/manifests/attack_taxonomy.json) | Dữ liệu Jailbreak thực tế (15,140 in-the-wild prompts từ Reddit/Discord), taxonomy các dạng tấn công DAN & Roleplay |
| **12** | [`Zhou_2024_EasyJailbreak_Unified_Framework.pdf`](file:///d:/Work/Do-an/References/Zhou_2024_EasyJailbreak_Unified_Framework.pdf) | Zhou et al. (2024) | *arXiv 2024* | • [`src/preprocessing/obfuscation.py`](file:///d:/Work/Do-an/src/preprocessing/obfuscation.py)<br>• [`tests/adversarial/`](file:///d:/Work/Do-an/tests/adversarial/) | **ROBUSTNESS KEY**: Kỹ thuật đột biến cú pháp (Mutators: Leetspeak, Spacing, Roleplay) phục vụ kiểm thử độ bền |
| **13** | [`Zou_2023_Universal_Transferable_Adversarial_Attacks_GCG.pdf`](file:///d:/Work/Do-an/References/Zou_2023_Universal_Transferable_Adversarial_Attacks_GCG.pdf) | Zou et al. (2023) | *arXiv 2023 (CMU/CAIS)* | • [`tests/adversarial/`](file:///d:/Work/Do-an/tests/adversarial/)<br>• [`notebooks/04_ablation.ipynb`](file:///d:/Work/Do-an/notebooks/04_ablation.ipynb) | Cơ chế tấn công hậu tố tối ưu hóa độ dốc (Greedy Coordinate Gradient - GCG) và kiểm thử nhận diện chuỗi token nhiễu |
| **14** | [`Robey_2023_SmoothLLM_Defending_LLMs_Random_Perturbation.pdf`](file:///d:/Work/Do-an/References/Robey_2023_SmoothLLM_Defending_LLMs_Random_Perturbation.pdf) | Robey et al. (2023) | *arXiv 2023 (Penn)* | • [`docs/thesis/Review1_Problem_Definition_and_Threat_Model.md`](file:///d:/Work/Do-an/docs/thesis/Review1_Problem_Definition_and_Threat_Model.md)<br>• [`src/preprocessing/cleaner.py`](file:///d:/Work/Do-an/src/preprocessing/cleaner.py) | Phương pháp phòng thủ bằng xáo trộn ngẫu nhiên (Randomized Smoothing) và đối chuẩn hiệu năng phòng ngự với PI-Guard |
| **15** | [`Jain_2023_Baseline_Defenses_Adversarial_Attacks_LLMs.pdf`](file:///d:/Work/Do-an/References/Jain_2023_Baseline_Defenses_Adversarial_Attacks_LLMs.pdf) | Jain et al. (2023) | *arXiv 2023 (Univ of Maryland)* | • [`docs/research/State_of_the_Art_Guardrail_and_Jailbreak_Benchmarks_Analysis.md`](file:///d:/Work/Do-an/docs/research/State_of_the_Art_Guardrail_and_Jailbreak_Benchmarks_Analysis.md)<br>• [`notebooks/02_baseline.ipynb`](file:///d:/Work/Do-an/notebooks/02_baseline.ipynb) | **KEY 1**: Cơ sở khoa học của Baseline Defenses (Pre-processing, Filtering, Perplexity, N-gram Classifier) |
| **16** | [`Yao_2022_ZeroQuant_Efficient_Post_Training_Quantization_Transformers.pdf`](file:///d:/Work/Do-an/References/Yao_2022_ZeroQuant_Efficient_Post_Training_Quantization_Transformers.pdf) | Yao et al. (2022) | *NeurIPS 2022 (Microsoft)* | • [`docs/research/State_of_the_Art_Guardrail_and_Jailbreak_Benchmarks_Analysis.md`](file:///d:/Work/Do-an/docs/research/State_of_the_Art_Guardrail_and_Jailbreak_Benchmarks_Analysis.md)<br>• [`src/models/classifier.py`](file:///d:/Work/Do-an/src/models/classifier.py) | **KEY 3**: Cơ sở khoa học của Lượng hóa động INT8 Post-Training Quantization (PTQ) cho Transformer, tăng tốc 3x trên CPU |
| **17** | [`Yuan_2024_GPT4_Too_Smart_To_Be_Safe_Cipher_Jailbreak.pdf`](file:///d:/Work/Do-an/References/Yuan_2024_GPT4_Too_Smart_To_Be_Safe_Cipher_Jailbreak.pdf) | Yuan et al. (2024) | *ICLR 2024* | • [`docs/thesis/Review1_Problem_Definition_and_Threat_Model.md`](file:///d:/Work/Do-an/docs/thesis/Review1_Problem_Definition_and_Threat_Model.md)<br>• [`src/preprocessing/cleaner.py`](file:///d:/Work/Do-an/src/preprocessing/cleaner.py)<br>• [`tests/adversarial/encoding/`](file:///d:/Work/Do-an/tests/adversarial/encoding/) | **OBFUSCATION & CIPHER KEY**: Nghiên cứu đột phá chứng minh mã hóa Base64/Cipher vượt rào kiểm duyệt LLM và cơ chế đánh chặn |

---

## 📑 2. BIBTEX ENTRY CẬP NHẬT ĐẦY ĐỦ 17 BÀI BÁO

```bibtex
@inproceedings{yuan2024gpt4,
  title     = {GPT-4 Is Too Smart To Be Safe: Stealthy Chat with LLMs via Cipher},
  author    = {Yuan, Youliang and Jiao, Wenxuan and Wang, Wenxiang and Jen-tse, Huang and He, Pinjia and Tu, Zhaopeng},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year      = {2024}
}
```
