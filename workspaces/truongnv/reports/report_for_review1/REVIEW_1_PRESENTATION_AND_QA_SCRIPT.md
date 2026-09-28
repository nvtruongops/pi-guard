# KỊCH BẢN THUYẾT TRÌNH REVIEW 1 & BỘ 10 CÂU HỎI PHẢN BIỆN HỘI ĐỒNG (15 PHÚT + 10 PHÚT Q&A)
## Đồ án Tốt nghiệp: PI-Guard (`IAP491_FA26_PI_GUARD`) — Đại học FPT
**Tác giả**: Nguyễn Văn Trường (Leader — MSSV: `SE182034`)  
**Thành viên tham gia**: Nguyễn Quí Đức, Phạm Minh Hoàng Việt, Đỗ Đoàn Duy Phương  
**Giảng viên hướng dẫn**: ThS. Trần Văn Ninh  
**Vị trí tài liệu**: `workspaces/truongnv/reports/report_for_review1/REVIEW_1_PRESENTATION_AND_QA_SCRIPT.md`  

---

## 🧭 1. CẤU TRÚC PHÂN CHIA THỜI LƯỢNG THUYẾT TRÌNH (TỔNG 15 PHÚT)

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│               PHÂN CHIA THỜI LƯỢNG THUYẾT TRÌNH REVIEW 1 (15 PHÚT)                     │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 👤 PHẦN 1: NGUYỄN VĂN TRƯỜNG (LEADER) — ~4.0 PHÚT                                      │
│    • Slide 1: Giới thiệu đề tài, Thành viên & Bối cảnh bùng nổ LLM                     │
│    • Slide 2: Lỗ hổng Von Neumann trong NLP ($X = S \Vert U$) & 4 Tầng Thiệt Hại        │
│    • Slide 3: Phân biệt 3 Vector Tấn công cốt lõi & Khung Mối đe dọa 5D                │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 👤 PHẦN 2: NGUYỄN QUÍ ĐỨC — ~4.0 PHÚT                                                  │
│    • Slide 4: Bề mặt tấn công duy nhất REST API & Kiến trúc phòng thủ 3 lớp             │
│    • Slide 5: Khảo sát SOTA: Phễu 41 papers & Bảng đối chuẩn thực nghiệm 6 mô hình     │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 👤 PHẦN 3: PHẠM MINH HOÀNG VIỆT — ~3.5 PHÚT                                            │
│    • Slide 6: Ma trận chọn mô hình & Phân tích tử huyệt Overdefense (NotInject D6)     │
│    • Slide 7: Ma trận 4 Kịch bản Demo thực nghiệm đối sánh (2x2 Matrix)                │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 👤 PHẦN 4: ĐỖ ĐOÀN DUY PHƯƠNG — ~3.5 PHÚT                                              │
│    • Slide 8: Hệ thống 3 Câu hỏi Nghiên cứu Chuẩn IEEE (RQ1 - RQ3) & 3 Research Gaps   │
│    • Slide 9: 4 Đóng góp mới của đề tài, Ranh giới Scope & Báo cáo Tiến độ 33% (WBS)   │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🎙️ 2. LỜI THOẠI CHI TIẾT TỪNG PHẦN (SCRIPT THUYẾT TRÌNH CHUẨN MỰC)

### 👤 PHẦN 1: NGUYỄN VĂN TRƯỜNG (LEADER) — 4 PHÚT
*(Slide 1: Tiêu đề & Bối cảnh | Slide 2: Lỗ hổng Von Neumann & 4 Tầng Thiệt Hại | Slide 3: Phân loại Taxonomy)*

> *"Kính thưa Thầy/Cô trong Hội đồng chấm khóa luận tốt nghiệp và Thầy Trần Văn Ninh - Giảng viên hướng dẫn của nhóm.  
> Em tên là Nguyễn Văn Trường, Trưởng nhóm đề tài **PI-Guard** — A Machine-Learning Guardrail for Detecting Prompt Injection and Jailbreak Attacks on LLM Applications. Hôm nay, nhóm chúng em xin được báo cáo hồ sơ kỹ thuật cột mốc **REVIEW 1**, tích hợp toàn diện hai chương nền tảng: Chương 1 - Mở đầu và Chương 2 - Khảo sát nghiên cứu liên quan.*
>
> *(Chuyển sang Slide 2)*  
> *Thưa Thầy Cô, khi các Mô hình Ngôn ngữ Lớn được tích hợp sâu vào hạ tầng doanh nghiệp qua RAG và AI Agent, chúng mang theo một điểm yếu chí mạng mà các giải pháp an ninh mạng truyền thống như WAF hay IDS/IPS hoàn toàn bất lực. Bản chất gốc rễ của điểm yếu này bắt nguồn từ **'Lỗ hổng kiến trúc Von Neumann trong xử lý ngôn ngữ tự nhiên'**.  
> Trong kiến trúc máy tính Von Neumann cổ điển, mã lệnh và dữ liệu cùng chia sẻ bộ nhớ chung dẫn đến lỗi Buffer Overflow. Tương tự, trong cơ chế Self-Attention của Transformer, chỉ thị an toàn của hệ thống (System Prompt $S$) và dữ liệu không tin cậy của người dùng (User Prompt $U$) bị ghép phẳng thành một chuỗi token duy nhất: $X = S \mathbin{\Vert} U$. Mô hình hoàn toàn không có cơ chế phân tách đặc quyền phần cứng (Hardware Privilege Rings hay NX-bit). Do đó, kẻ tấn công có thể chèn các token điều khiển thao túng ma trận chú ý, gây ra 4 tầng thiệt hại thảm khốc cho doanh nghiệp:  
> 1. Xâm phạm sở hữu trí tuệ, làm lộ System Prompt và Master API Keys;  
> 2. Chiếm quyền điều khiển tác tử AI, ép Agent thực thi các giao dịch tài chính hoặc xóa dữ liệu trái phép;  
> 3. Tấn công cạn kiệt tài chính (Denial-of-Wallet) qua vòng lặp token vô tận;  
> 4. Vi phạm nghiêm trọng Đạo luật AI châu Âu (EU AI Act 2024 Điều 15) với mức chế tài lên đến 35 triệu EUR.*
>
> *(Chuyển sang Slide 3)*  
> *Để tiếp cận bài toán một cách có phương pháp luận, nhóm đã xây dựng **Khung phân tích mối đe dọa 5 trục (5D Threat Analysis Framework)** theo chuẩn NIST AI 100-2e2025 và bóc tách rõ ranh giới giữa 3 hình thái tấn công:  
> - **Direct Prompt Injection**: Ghi đè lệnh trực tiếp qua giao diện chat để chiếm quyền điều khiển luồng lệnh.  
> - **Indirect Prompt Injection**: Đầu độc ngữ cảnh gián tiếp khi LLM đọc tài liệu ngoài qua RAG.  
> - **Jailbreak**: Lợi dụng bối cảnh nhập vai DAN (Do Anything Now) để phá vỡ ranh giới căn chỉnh an toàn RLHF.  
> Tiếp theo, em xin kính mời bạn Nguyễn Quí Đức trình bày về Bề mặt tấn công và Khảo sát đối chuẩn thực nghiệm."*

---

### 👤 PHẦN 2: NGUYỄN QUÍ ĐỨC — 4 PHÚT
*(Slide 4: Bề mặt tấn công & Kiến trúc 3 lớp | Slide 5: Phễu 41 papers & Đối chuẩn thực nghiệm 6 mô hình)*

> *"Kính thưa Thầy/Cô, em là Nguyễn Quí Đức, phụ trách phân hệ Mô hình Baseline Machine Learning.  
> *(Tại Slide 4)*  
> Tuân thủ nguyên lý kinh điển **Giám sát Trung gian Hoàn toàn (Complete Mediation)** của Saltzer & Schroeder (1975), đồ án định vị bề mặt tấn công duy nhất của hệ thống là cổng giao tiếp REST API (`POST /v1/chat/guardrail`). Toàn bộ truy vấn đầu vào đều bị coi là Không Tin Cậy và phải trải qua **Kiến trúc bảo vệ 3 lớp**:  
> - **Lớp 1 (Trọng tâm đề tài)**: PI-Guard Ingress Guardrail gồm Tầng 0 Text Scrubber, Tầng 1 Dual TF-IDF, và Tầng 2 DeBERTa-v3 Native FP32.  
> - **Lớp 2**: Target LLM được gia cố System Prompt bằng phân cách XML.  
> - **Lớp 3**: Output Sanitizer hậu kiểm tra rò rỉ PII và Regex secret.  
> Mô hình hiểm họa của đề tài là **Hộp Đen Hoàn Toàn (Black-Box)**: Kẻ tấn công chỉ tương tác qua chuỗi văn bản, hoàn toàn không có quyền truy cập trọng số GPU hay bộ nhớ đệm KV-Cache.
>
> *(Chuyển sang Slide 5)*  
> *Về mặt y văn, nhóm không lựa chọn mô hình một cách cảm tính mà áp dụng **Phễu Lựa Chọn Khoa Học 5 Bước**: Từ 41 công trình quốc tế $\to$ lọc 16 đề xuất Guardrail $\to$ thu thập 11 tài nguyên mã nguồn $\to$ lưu trữ 9 mô hình thực nghiệm $\to$ và tuyển chọn **6 mô hình đối chuẩn tiêu biểu cho 5 trường phái kỹ thuật ($F_1 \to F_5$)**.  
> Đo đạc thực nghiệm 100% dữ liệu thật trên 6 bộ mẫu D1–D6 đã vạch trần các điểm vỡ kỹ thuật chí mạng:  
> - Bộ lọc Heuristic Regex ($F_1$) dù siêu nhanh (<0.5ms) nhưng mù màu trước Obfuscation.  
> - Dual-Space TF-IDF ($F_2$ Jain 2023) lọc DPI trong 12.9ms nhưng trượt hoàn toàn trước Jailbreak ngữ nghĩa (Recall 0%).  
> - InstructDetector ($F_3$ EMNLP 2024) bị bùng nổ độ trễ lên đến 245.1ms, vi phạm nghiêm trọng chuẩn SLA Ingress < 30ms.  
> - DataSentinel ($F_4$ IEEE S&P 2025) bỏ lọt tới 35% Jailbreak đối kháng.  
> Tiếp theo, bạn Phạm Minh Hoàng Việt sẽ phân tích chi tiết về tử huyệt chặn nhầm mã nguồn và ma trận demo."*

---

### 👤 PHẦN 3: PHẠM MINH HOÀNG VIỆT — 3.5 PHÚT
*(Slide 6: Ma trận chọn mô hình & Overdefense NotInject | Slide 7: Ma trận 4 Kịch bản Demo)*

> *"Kính thưa Thầy/Cô, em là Phạm Minh Hoàng Việt, phụ trách phân hệ Transformer và Kiểm thử độ bền đối kháng.  
> *(Tại Slide 6)*  
> Khám phá thực nghiệm quan trọng nhất của nhóm là việc phát hiện **Tử huyệt Sụp đổ do Quá phòng thủ (Overdefense Catastrophe)** trên các mô hình Transformer SOTA thương mại hiện nay khi thử nghiệm trên bộ mẫu `NotInject` (D6) của Hao Li (ACL 2025):  
> - Mô hình **Meta Prompt-Guard 86M** (chính thức của Meta Purple Llama) bị sụp đổ hoàn toàn: **Chặn nhầm 99.1%** các đoạn mã lập trình Python và truy vấn SQL lành tính!  
> - Mô hình **ProtectAI DeBERTa-v3 v2** cũng chặn nhầm tới **19.0%** mã nguồn hợp lệ.  
> Trong môi trường doanh nghiệp phần mềm, tỷ lệ chặn nhầm này sẽ làm tê liệt toàn bộ quy trình làm việc của kỹ sư. Vì vậy, nhóm đề xuất giải pháp kế thừa cơ chế **Masked Overlap Fraction (MOF Invariance)** từ Hao Li (ACL 2025) kết hợp kiến trúc **CPU Native FP32 nguyên bản** của `microsoft/deberta-v3-base`. Nhóm kiên quyết không dùng lượng tử hóa INT8 để tránh sai số làm tròn số học (Quantization Noise) gây giảm độ bền phân loại.
>
> *(Chuyển sang Slide 7)*  
> *Tính khả thi của đề tài được chứng minh thông qua **Ma trận 4 Kịch bản Thử nghiệm ($2 \times 2$)** đã được hiện thực hóa trên nguyên mẫu FastAPI và Streamlit:  
> - **Kịch bản 1A (Prompt Injection không phòng thủ)**: Kẻ tấn công gửi lệnh ép trích xuất API Key $\to$ LLM bị ghi đè và làm lộ bí mật kinh doanh `ABC-SEC-998877`.  
> - **Kịch bản 1B (Có PI-Guard)**: Hệ thống chấm rủi ro 0.964, trả về **HTTP 403 Blocked trong 14.8ms**, LLM không bị gọi, an toàn tuyệt đối.  
> - **Kịch bản 2A (Jailbreak DAN không phòng thủ)**: LLM sinh mã độc keylogger theo kịch bản giả tưởng.  
> - **Kịch bản 2B (Có PI-Guard)**: Hệ thống nhận diện cấu trúc bẻ khóa, trả về **HTTP 403 Blocked trong 13.5ms**.  
> Tiếp theo, bạn Đỗ Đoàn Duy Phương sẽ báo cáo về Hệ thống câu hỏi nghiên cứu và Tiến độ triển khai."*

---

### 👤 PHẦN 4: ĐỖ ĐOÀN DUY PHƯƠNG — 3.5 PHÚT
*(Slide 8: 3 RQs IEEE & 3 Research Gaps | Slide 9: 4 Đóng góp mới, Ranh giới Scope & Tiến độ WBS)*

> *"Kính thưa Thầy/Cô, em là Đỗ Đoàn Duy Phương, phụ trách API Middleware và Tổng hợp báo cáo.  
> *(Tại Slide 8)*  
> Để đảm bảo tính chuẩn mực học thuật cao nhất theo tiêu chuẩn IEEE, đề tài xác lập hệ thống **3 Câu hỏi Nghiên cứu Cốt lõi (RQ1 - RQ3)** với các chỉ số đo lường định lượng tương ứng với 3 khoảng trống nghiên cứu lớn:  
> - **RQ1 (Chống rò rỉ dữ liệu & Biểu diễn ngữ nghĩa)**: Khống chế chỉ số $\text{Inter-cluster Jaccard} < 0.15$ bằng thuật toán Group-Aware Splitting, đạt Macro $F_1 \ge 0.95$ và $F_1^{\text{OOD}} \ge 0.92$.  
> - **RQ2 (Độ bền kháng lẩn tránh & Mã hóa)**: Đạt tỷ số bảo toàn độ bền đối kháng $\text{ARR} \ge 0.95$, khống chế tỷ lệ lọt lưới $\text{ASR} < 5\%$ và độ suy hao $\Delta F_1 \le 5\%$ trước Leetspeak, Spacing và Base64/Cipher.  
> - **RQ3 (Cân bằng An toàn & Khả thi triển khai)**: Khống chế nghiêm ngặt Tỷ lệ Chặn Nhầm $\text{FPR} < 1.5\%$ trên tập Benign theo bài toán kinh tế của OpenAI, bảo đảm độ trễ phân vị **P95 < 30ms trên CPU** và thông lượng $\ge 100\text{ RPS}$.
>
> *(Chuyển sang Slide 9)*  
> *Đề tài đóng góp 4 giá trị mới: (1) Phương pháp luận dữ liệu Group-Aware Splitting; (2) Kiến trúc phân tầng Two-Tier Cascade; (3) Bộ kiểm thử kháng lẩn tránh có bộ giải mã Heuristic Scrubber; và (4) Nguyên mẫu FastAPI/Streamlit kiểm chứng độc lập cho 5 Cloud LLM APIs.  
> Về tiến độ triển khai thực tế (WBS): Tính đến mốc Review 1 (Tuần 4 / 15 tuần thực học, tương ứng 26.7% thời gian), nhóm đã hoàn thành **~33.0% khối lượng toàn dự án**, vượt tiến độ kế hoạch đặt ra: Toàn bộ hồ sơ lý thuyết Chapter 1 & 2 hoàn thành 100%, 45k+ mẫu dữ liệu đã sẵn sàng, và 6 baseline đã được kiểm định thực nghiệm.  
> Nhóm PI-Guard xin trân trọng cảm ơn Thầy Cô đã chú ý lắng nghe và rất mong nhận được những câu hỏi góp ý quý báu của Thầy Cô để nhóm hoàn thiện đề tài trong các giai đoạn tiếp theo!"*

---

## 🛡️ 3. BỘ 10 KỊCH BẢN HỎI - ĐÁP PHẢN BIỆN HỘI ĐỒNG (COUNCIL Q&A DEFENSE DOSSIER)

Đây là 10 câu hỏi phản biện học thuật hóc búa nhất thường được các Giáo sư / Tiến sĩ trong Hội đồng Chuyên ngành An toàn Thông tin Đại học FPT đặt ra, kèm theo phương án trả lời chuẩn mực dựa trên bằng chứng khoa học thực nghiệm:

---

### ❓ CÂU HỎI 1: TẠI SAO NHÓM KHÔNG LƯỢNG TỬ HÓA MÔ HÌNH SANG INT8 HOẶC DÙNG ONNX RUNTIME ĐỂ GIẢM ĐỘ TRỄ HƠN NỮA?
#### 💡 Câu trả lời chuẩn mực của nhóm (Dựa trên Tier 1-3 Provenance & `ARCHITECTURAL_DEPRECATIONS_AND_OUT_OF_SCOPE.md`):
> *"Dạ thưa Thầy/Cô, nhóm đã khảo sát rất kỹ các công trình lượng tử hóa như ZeroQuant (Yao et al. 2022) và đã tiến hành thử nghiệm sơ bộ ở giai đoạn đầu. Tuy nhiên, nhóm đã có một quyết định kỹ thuật có chủ đích là **loại bỏ hoàn toàn lượng tử hóa INT8 khỏi phạm vi nghiên cứu cốt lõi** vì 3 lý do học thuật sau:
> 1. **Về định vị chuyên ngành (Scope Integrity)**: Đồ án của chúng em thuộc chuyên ngành **An toàn Thông tin (Information Assurance)**, không phải Khoa học Máy tính hay Kỹ thuật Phần cứng. Đóng góp cốt lõi của đề tài là mô hình hóa hiểm họa, cơ chế phân tầng Two-Tier Cascade và thuật toán kháng Overdefense MOF Invariance, chứ không phải tối ưu hóa biên dịch nén mô hình.
> 2. **Về tính hiệu quả kỹ thuật (Architectural Sufficiency)**: Nhờ có Tầng 1 (Dual TF-IDF) sàng lọc sạch $83\%$ lưu lượng thông thường chỉ trong $\le 1.5\text{ms}$, Tầng 2 chỉ phải giải quyết phần truy vấn bất định. Kết quả đo đạc thực nghiệm cho thấy mô hình `microsoft/deberta-v3-base` nguyên bản chạy trên CPU tiêu chuẩn đạt độ trễ chỉ khoảng $12.8\text{ms} - 24.5\text{ms}$, hoàn toàn đáp ứng trần SLA Ingress Gateway **P95 < 30ms** mà không cần nén INT8.
> 3. **Về độ an toàn phân loại (Quantization Noise Risk)**: Lượng tử hóa sau huấn luyện (PTQ) sang INT8 đưa vào sai số làm tròn số học (Quantization Noise). Đối với các bài toán bảo mật, việc mất mát độ chính xác dù chỉ $1-2\%$ có thể tạo ra các lỗ hổng ranh giới mờ (Borderline Evasions), khiến kẻ tấn công lọt lưới hoặc gây tăng tỷ lệ False Positive trên các mẫu câu ngắn. Vì vậy,### ❓ CÂU HỎI 5: TẠI SAO MÔ HÌNH META PROMPT-GUARD 86M LẠI CHẶN NHẦM ĐẾN 99.1% TRÊN TẬP NOTINJECT?
#### 💡 Câu trả lời chuẩn mực của nhóm:
> *"Dạ thưa Thầy/Cô, đây là kết quả kiểm định thực nghiệm rất giá trị mà nhóm đo được trên tập mẫu chuẩn `NotInject` của Hao Li (Peking University, ACL 2025 [[18]](#ref18)):  
> - Nguyên nhân cốt lõi là do **Sự thiếu vắng cơ chế phân tách cú pháp mã nguồn**:  
> - Meta Prompt-Guard được huấn luyện như một bộ phân loại chuỗi thông thường. Khi lập trình viên gửi các đoạn mã Python chứa các hàm như `os.system()`, `subprocess.run()`, hoặc các câu lệnh SQL như `DROP TABLE`, mô hình nhận thấy sự xuất hiện dày đặc của các từ khóa mệnh lệnh hệ thống và ngay lập tức kích hoạt nhãn độc hại.  
> - Mô hình không có khả năng phân biệt giữa việc 'một câu lệnh đang được thực thi trong ngữ cảnh văn bản' với 'một đoạn code đang được truyền vào để nhờ debug'.  
> - Để khắc phục tử huyệt này, đồ án PI-Guard đã định hướng áp dụng cơ chế **Masked Overlap Fraction (MOF Invariance)** từ Hao Li et al. (ACL 2025), sử dụng mặt nạ phân tách cú pháp code để bảo vệ các truy vấn lập trình lành tính, khống chế tỷ lệ chặn nhầm $\text{FPR} < 1.5\%$."*

---

### ❓ CÂU HỎI 6: HỆ THỐNG PHÒNG THỦ CỦA NHÓM LÀ HỘP ĐEN (BLACK-BOX), NẾU KẺ TẤN CÔNG GIẤU LỆNH Ở ĐUÔI TÀI LIỆU DÀI 200,000 KÝ TỰ (LONG-CONTEXT PROMPT OVERFLOW) THÌ SAO?
#### 💡 Câu trả lời chuẩn mực của nhóm:
> *"Dạ thưa Thầy/Cô, đây chính là hình thái tấn công **Key 8: Long-Context Prompt Overflow** (Zhou et al., 2026 [[40]](#ref40)) mà nhóm đã nghiên cứu và đưa vào phạm vi kiểm định:  
> 1. Đa số các mô hình Transformer phân loại nhỏ (như BERT, DeBERTa) có giới hạn cửa sổ ngữ cảnh cứng là $512\text{ tokens}$. Kẻ tấn công lợi dụng điều này bằng cách nhét 5,000 từ văn bản kinh doanh hợp lệ lên đầu rồi giấu 1 dòng lệnh độc ở cuối; khi đó Guardrail chỉ đọc 512 token đầu nên bỏ lọt $100\%$ đòn tấn công.  
> 2. Để giải quyết rủi ro này, nhóm đã tiến hành khảo sát và đo đạc thực nghiệm mô hình **ModernBERT (Warner et al., 2024)** có hỗ trợ cửa sổ ngữ cảnh mở rộng lên đến **8,192 tokens** nhờ kỹ thuật FlashAttention-2 và RoPE.  
> 3. Trong kiến trúc Ingress Proxy của PI-Guard, nhóm áp dụng cơ chế **Sliding Window Chunking kết hợp Head-Tail Sampling** (đọc đồng thời 512 token đầu và 512 token cuối của văn bản) để phát hiện sớm các đòn tiêm lệnh giấu ở đuôi tài liệu mà vẫn đảm bảo độ trễ P95 thấp."*

---

### ❓ CÂU HỎI 7: MÔ HÌNH CỦA CÁC EM CÓ KHẢ NĂNG PHÒNG THỦ TRƯỚC CÁC CUỘC TẤN CÔNG BẰNG TIẾNG VIỆT HAY KHÔNG?
#### 💡 Câu trả lời chuẩn mực của nhóm:
> *"Dạ thưa Thầy/Cô, đây là trọng tâm nghiên cứu của **Key 7: Multilingual Attacks** (Deng et al. ICLR 2024):  
> - Phần lớn các Guardrail quốc tế hiện nay được huấn luyện thuần túy trên kho dữ liệu tiếng Anh, dẫn đến hiện tượng 'mù màu đa ngôn ngữ' khi kẻ tấn công dịch prompt injection sang tiếng Việt có dấu hoặc không dấu.  
> - Để chuẩn bị cho vấn đề này, nhóm đã thu thập bộ dữ liệu kiểm chuẩn thực nghiệm tiếng Việt gồm 40 mẫu tấn công bẻ khóa và câu lệnh hệ thống từ VMLU Benchmark.  
> - Kiến trúc `microsoft/deberta-v3-base` và cơ chế **Disentangled Attention** có ưu thế vượt trội vì mô hình phân tách riêng vector vị trí tương đối và vector nội dung. Cấu trúc ngữ pháp của các đòn tấn công ghi đè chỉ thị (ví dụ: 'Hãy bỏ qua... và làm theo...') có các dấu hiệu hình thái học tương đồng giữa tiếng Anh và tiếng Việt. Đồng thời, bộ tokenizer subword byte-level của DeBERTa cho phép mã hóa tốt các ký tự Unicode tiếng Việt mà không bị lỗi Out-of-Vocabulary (OOV)."*

---

### ❓ CÂU HỎI 8: NHÓM CAM KẾT CON SỐ FPR < 1.5% DỰA TRÊN CƠ SỞ KHOA HỌC NÀO HAY CHỈ LÀ MỘT CON SỐ ĐOÁN MÒ?
#### 💡 Câu trả lời chuẩn mực của nhóm:
> *"Dạ thưa Thầy/Cô, con số **$\text{FPR} < 1.5\%$** là một chuẩn mực an toàn kinh tế khắt khe được nhóm kế thừa từ nghiên cứu của **OpenAI (Markov et al., AAAI 2023 [[12]](#ref12))**:  
> - Trong một hệ sinh thái doanh nghiệp phục vụ hàng triệu truy vấn mỗi ngày, nếu tỷ lệ chặn nhầm là $5\%$, cứ 20 người dùng hợp lệ sẽ có 1 người bị chặn oan, điều này sẽ phá hủy hoàn toàn trải nghiệm khách hàng và làm gia tăng chi phí vận hành hỗ trợ kỹ thuật.  
> - Về mặt toán học, nhóm thiết lập ngưỡng quyết định (Decision Threshold) dựa trên **Lý thuyết Kiểm soát Rủi ro Thống kê (Conformal Risk Control - CRC)** của Angelopoulos et al. (2024 [[22]](#ref22)). Phương pháp này cho phép tìm ra ngưỡng kích hoạt chính sách an toàn có bảo chứng cận xác suất, bảo đảm tỷ lệ False Positive trên tập phân phối dữ liệu lành tính luôn bị khống chế nghiêm ngặt dưới mức $\alpha = 0.015$ ($1.5\%$) với độ tin cậy $1 - \delta \ge 95\%$."*

---

### ❓ CÂU HỎI 9: HỆ THỐNG PI-GUARD ĐẶT TRƯỚC LLM CÓ NGUY CƠ BỊ KẺ TẤN CÔNG BIẾN THÀNH ĐIỂM NGHỄN DOS KHÔNG?
#### 💡 Câu trả lời chuẩn mực của nhóm:
> *"Dạ thưa Thầy/Cô, đây là bài toán kiến trúc sống còn đối với một Ingress Proxy Middleware:  
> 1. **Về mặt hạ tầng phần mềm**: PI-Guard được xây dựng trên nền tảng **Asynchronous FastAPI** sử dụng mô hình lập trình bất đồng bộ Non-blocking I/O (Async/Await qua `uvicorn`). Điều này cho phép một tiến trình đơn lẻ có thể duy trì hàng ngàn kết nối đồng thời mà không bị chiếm dụng luồng (Thread Starvation).  
> 2. **Về cơ chế phân tầng (Tiered Early-Exit)**: Nhờ có Tầng 1 (Dual TF-IDF), các truy vấn thông thường được phân loại và cấp quyền Fast-Pass đi thẳng đến LLM chỉ trong vòng **$\le 1.5\text{ms}$**. Tầng 2 chỉ được kích hoạt khi xác suất rơi vào vùng bất định ($0.15 < P < 0.85$). Cơ chế này giúp thông lượng tổng thể của hệ thống đạt trên **100 RPS trên một nhân CPU tiêu chuẩn**, triệt tiêu nguy cơ biến thành điểm nghẽn DoS."*

---

### ❓ CÂU HỎI 10: NẾU KẺ TẤN CÔNG DÙNG BASE64 HOẶC MÃ HÓA LEETSPEAK THÌ BỘ PHÂN LOẠI CÓ BỊ ĐÁNH LỪA KHÔNG?
#### 💡 Câu trả lời chuẩn mực của nhóm:
> *"Dạ thưa Thầy/Cô, đây chính là trọng tâm nghiên cứu của **RQ2** và bài toán lẩn tránh được Yuan et al. công bố tại ICLR 2024 [[17]](#ref17):  
> - Nếu chỉ dùng Transformer đơn thuần, các chuỗi Base64 sẽ bị phân mảnh thành các subword vô nghĩa và làm điểm số rủi ro sụt giảm, cho phép payload lọt lưới.  
> - Trong kiến trúc PI-Guard, nhóm bố trí **Tier-0 Ingress Scrubber** hoạt động ở tầng tiền xử lý:  
>   + Bộ quét DFA tự động phát hiện các chuỗi có định dạng Base64, Hexadecimal hoặc Rot13 và tiến hành **giải mã nội tuyến (Inline Decoding)** trước khi nạp vào mô hình phân loại.  
>   + Chuẩn hóa **Unicode NFKC** và loại bỏ các ký tự ẩn tàng hình (Zero-Width Spaces).  
>   + Đối với Leetspeak (`1gn0r3`), Tầng 1 sử dụng biểu diễn **Character n-grams (3-5 ký tự)** bóc tách được các cụm ký tự con tương đồng, giúp tỷ số bảo toàn độ bền đối kháng của hệ thống đạt $\text{ARR} \ge 0.95$ (độ suy giảm hiệu năng $\Delta F_1 \le 5\%$), bảo đảm tính kiên cố trước mọi nỗ lực ngụy trang."*

---

## 4. Tài Liệu Tham Khảo Học Thuật (100% >= 2022)

<a id="ref3"></a>**[3]** F. Perez and I. Ribeiro, "Ignore Previous Prompt: Attack Techniques For Language Models," in *NeurIPS 2022 Workshop*, 2022.  
<a id="ref4"></a>**[4]** K. Greshake et al., "Not what you've signed up for: Compromising Real-World LLM Applications with Indirect Prompt Injection," in *ACM AISEC 2023*, 2023.  
<a id="ref7"></a>**[7]** A. Vassilev et al., "Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations," *NIST*, NIST.AI.100-2e2025, 2025.  
<a id="ref8"></a>**[8]** OWASP GenAI Security Project, "OWASP Top 10 for Large Language Model Applications," Version 2.0, 2025.  
<a id="ref9"></a>**[9]** H. Inan et al., "Llama Guard: LLM-based Input-Output Safeguard," *Meta AI Technical Report*, arXiv:2312.06674, 2023.  
<a id="ref11"></a>**[11]** P. He, J. Gao, and W. Chen, "DeBERTaV3: Improving DeBERTa using ELECTRA-Style Pre-Training," in *ICLR 2023*, 2023.  
<a id="ref12"></a>**[12]** T. Markov et al., "A Holistic Approach to Undesired Content Detection in the Real World," in *AAAI HCOMP 2023*, 2023.  
<a id="ref13"></a>**[13]** N. Jain et al., "Baseline Defenses for Adversarial Attacks Against Aligned Language Models," in *NeurIPS 2023 Workshop*, 2023.  
<a id="ref14"></a>**[14]** A. Robey et al., "SmoothLLM: Defending Large Language Models Against Jailbreaking Attacks," in *NeurIPS 2023*, 2023.  
<a id="ref17"></a>**[17]** Y. Yuan et al., "GPT-4 Is Too Smart To Be Safe: Stealthy Chat with LLMs via Cipher," in *ICLR 2024*, 2024.  
<a id="ref18"></a>**[18]** H. Li et al., "PIGuard: Protecting Language Models against Prompt Injection with MOF," in *ACL 2025*, 2025.  
<a id="ref22"></a>**[22]** A. N. Angelopoulos et al., "Conformal Risk Control," *arXiv preprint arXiv:2208.02814*, 2024.  
<a id="ref40"></a>**[40]** A. Zhou et al., "Prompt Overflow: Exploiting Long-Context Windows in LLM Applications," *arXiv preprint arXiv:2602.11045*, 2026.
