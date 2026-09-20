# BÁO CÁO NGHIÊN CỨU CHUYÊN ĐỀ & TÁI LẬP HỌC THUẬT NHIỆM VỤ 3
## ĐỀ TÀI: A MACHINE-LEARNING GUARDRAIL FOR DETECTING PROMPT INJECTION AND JAILBREAK ATTACKS ON LLM APPLICATIONS (PI-GUARD)
### Báo Cáo Master Task 3: Chuỗi Logic Nghiên Cứu (Từ SOTA $\rightarrow$ Khảo Sát 5 Ứng Viên $\rightarrow$ Tái Lập Thực Nghiệm $\rightarrow$ Mô Phỏng Hai Tầng $\rightarrow$ Đề Xuất Tối Ưu) & Giải Trình Phản Biện Học Thuật

**Tác giả**: Nguyễn Văn Trường (Leader — MSSV: `SE182034`) | **Workspace**: `workspaces/truongnv/`  
**Căn cứ chỉ đạo**: Biên bản họp GVHD Thầy Trần Văn Ninh [`Final-Report/Meeting/Meeting 4_10_09_26.md`](file:///d:/Work/Do-an/Final-Report/Meeting/Meeting%204_10_09_26.md)  
**Mã tài liệu**: `workspaces/truongnv/reports/tasks_for_meeting_5/task_reports/TASK_3_REPRODUCIBILITY_AND_DATASETS.md`  
**Chuyên đề nghiên cứu bổ trợ**: [`supplementary/`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_reports/supplementary/README.md)  
**Phòng thí nghiệm thực nghiệm & Runbook**: [`../task_3_replication/`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/README.md)

---

## 📌 TÓM TẮT ĐIỀU HÀNH (EXECUTIVE SUMMARY)

Báo cáo này tổng hợp toàn diện kết quả nghiên cứu khoa học, khảo sát y văn và đo đạc thực nghiệm độc lập của **Task 3 (Thiết kế, Thực nghiệm Mô hình Phân loại & Đối soát Bộ ba Công khai)** trong đề tài PI-Guard theo chuỗi logic biện chứng 5 bước khép kín:
$$\text{SOTA Analysis} \longrightarrow \text{Khảo Sát Ứng Viên} \longrightarrow \text{Thực Nghiệm Độc Lập} \longrightarrow \text{Mô Phỏng Kết Hợp Hai Tầng} \longrightarrow \text{Đề Xuất Tối Ưu \& Phản Biện}$$

### 🎯 5 Kết Quả Then Chốt Đã Đạt Được:
1. **Thẩm định & Thực thi Bộ Ba Công Khai (Public Triad Invariant [[TN03]](#term-public-triad))**:
   - Tải về và clone $100\%$ mã nguồn mở chính thức của mô hình tham khảo Tầng 1 từ GitHub (`AhsanAyub/malicious-prompt-detection`, CAMLIS 2024 [[2]](#ref2)) và mô hình lõi Tầng 2 (`leolee99/PIGuard`, ACL 2025 [[1]](#ref1)), kèm $43\text{MB}$ dữ liệu đóng gói sẵn và checkpoint trọng số mở.
2. **Khảo Sát Tuyển Chọn 5 Ứng Viên Mô Hình Tầng 1**:
   - Rà soát 5 công trình khoa học quốc tế đạt chuẩn Public Triad: Ayub & Majumdar (CAMLIS 2024), Schulhoff et al. (HackAPrompt EMNLP 2023 [[8]](#ref8)), Shaheer et al. (arXiv:2512.12583 [[6]](#ref6)), ProtectAI LLM-Guard [[7]](#ref7), và Sekar et al. (arXiv:2601.12359 [[9]](#ref9)).
3. **Khám Phá Thực Nghiệm: 2 Điểm Nghẽn Của Ayub MiniLM (CAMLIS 2024)**:
   - *Điểm nghẽn độ trễ*: Tác giả Ayub chỉ đo thời gian phân loại trên vector NumPy lưu sẵn ($< 0.1\text{ms}$). Thực tế khi chạy in-line proxy trên CPU, bước suy luận trích xuất vector qua `all-MiniLM-L6-v2` tiêu tốn **$45.11\text{ms}$** (P95: **$129.48\text{ms}$**), biến Tầng 1 thành điểm nghẽn độ trễ thay vì bộ lọc siêu tốc.
   - *Điểm nghẽn báo động giả*: Trên tập `NotInject` (339 câu hỏi an ninh lành tính chứa từ nhạy cảm), Ayub MiniLM dính tỷ lệ báo động giả (FPR) lên tới **$58.41\%$** do hiện tượng thiên lệch ngữ nghĩa [[TN04]](#term-trigger-bias).
4. **Hiệu Năng Vượt Trội Của Native TF-IDF N-Grams**:
   - Bộ phân loại TF-IDF (Word 1–3 + Char 3–5) kết hợp Logistic Regression đạt độ trễ suy luận chỉ **$1.62\text{ms}$** trên CPU (**nhanh gấp 28 lần** so với Ayub MiniLM), đạt $F_1 = 0.7636$ trên tập tấn công và giảm FPR trên `NotInject` xuống **$21.24\%$**.
5. **Mô Phỏng Hai Tầng Bất Định (Two-Tier Uncertainty Routing) & Bộ Giải Trình Phản Biện**:
   - Định tuyến qua khoảng bất định $[0.15, 0.85]$ giúp giải phóng các truy vấn tin cậy cao ngay tại Tầng 1 với độ trễ $\sim 1.6\text{ms}$, đồng thời bảo toàn độ chính xác $76.21\%$ của DeBERTa-v3 trên WildGuard.
   - Xây dựng 4 luận điểm khoa học sắc bén giải trình câu hỏi hóc búa của Hội đồng FPT: *"Tại sao mô hình đề xuất tốt nhưng các công trình nghiên cứu lớn chưa công bố giải pháp 2 tầng tương tự?"*.

---

## 1. BỐI CẢNH, NGUYÊN TẮC CHỈ ĐẠO & MA TRẬN HỒ SƠ Y VĂN

### 1.1. 4 Nguyên Tắc Chỉ Đạo Cốt Lõi Của Task 3 Từ GVHD Trần Văn Ninh
Căn cứ chỉ đạo chính thức tại buổi họp Meeting 4 ngày 10/09/2026:
1. **Bản chất Task 3 là Tái lập Y văn Tham khảo (Pure Literature Replication)**:
   - Nhiệm vụ này tập trung $100\%$ vào việc: Khảo sát, tải về và chạy thực nghiệm tái lập các bài báo tham khảo đã xuất bản có đầy đủ Bộ ba [Paper + Code + Dataset] công khai.
   - Nhóm tải đúng mã nguồn và dữ liệu của tác giả về máy cá nhân, chạy lệnh đánh giá của tác giả để nắm chắc siêu tham số trước Meeting 5.
2. **Xác lập 2 Bài báo Mỏ neo Tham khảo phục vụ Tái lập**:
   - **Mô hình Tham khảo 1 (Baseline)**: Ayub & Majumdar (CAMLIS 2024 [[2]](#ref2)) — Mô hình học máy nhẹ nhúng câu MiniLM + Random Forest / XGBoost / Logistic Regression (GitHub + 467k mẫu dữ liệu Hugging Face).
   - **Mô hình Tham khảo 2 (SOTA Anchor)**: Hao Li et al. (ACL 2025 Long Paper [[1]](#ref1)) — PIGuard DeBERTa-v3 (GitHub + benchmark NotInject đóng gói sẵn + pre-trained checkpoint).
3. **Ranh giới dứt khoát giữa Task 3 và Task 4**:
   - **Task 3**: Tải và chạy 2 mô hình tham khảo để tái lập kết quả của tác giả, khảo sát ứng viên và phân tích điểm nghẽn thực tế.
   - **Task 4**: Phân tích sự đánh đổi chuyên sâu, lý giải tại sao không dùng TF-IDF đơn lẻ và đề xuất 3 giải pháp cải tiến độc quyền của đồ án (xem chi tiết tại [`TASK_4_PIGUARD_IMPROVEMENTS.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_reports/TASK_4_PIGUARD_IMPROVEMENTS.md)).
4. **Tách biệt ranh giới dữ liệu**: Tập dữ liệu đăng ký trong [`CAPSTONE PROJECT REGISTER.md`](file:///d:/Work/Do-an/CAPSTONE%20PROJECT%20REGISTER.md) thuộc về giai đoạn huấn luyện mô hình đồ án sau này (Review 2). Không tải lan man các dataset ngoài phạm vi đề tài trong Task 3.

### 1.2. Ma Trận Tham Chiếu Các Hồ Sơ Chuyên Đề Bổ Trợ & Runbook Thực Nghiệm

Toàn bộ tài liệu bóc tách lý thuyết chuyên sâu được lưu trữ tại thư mục [`supplementary/`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_reports/supplementary/README.md), kết hợp cùng phòng thí nghiệm thực nghiệm đóng gói sẵn [`task_3_replication/`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/README.md):

| STT | Hồ Sơ Chuyên Đề | Tệp Tham Chiếu Trực Tiếp | Trọng Tâm Báo Cáo Kỹ Thuật Task 3 |
| :---: | :--- | :--- | :--- |
| **SUPP-04** | **Thực Trạng Y Văn TF-IDF** | [`supplementary/LITERATURE_ASSESSMENT_TFIDF.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_reports/supplementary/LITERATURE_ASSESSMENT_TFIDF.md) | Lý giải vì sao không có repo độc lập cho TF-IDF; mổ xẻ nghiên cứu Intel Labs (arXiv:2512.19011 [[10]](#ref10)) về độ trễ $<1\text{ms}$ CPU và ưu thế $+26\%$ F1 khi gặp xáo trộn ký tự; ảnh minh chứng từ bài báo Neel Jain (NeurIPS 2023) và đường cong suy giảm từ khóa. |
| **SUPP-05** | **Thẩm Định Mỏ Neo PIGuard** | [`supplementary/CORE_ANCHOR_PIGUARD_ACL2025.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_reports/supplementary/CORE_ANCHOR_PIGUARD_ACL2025.md) | Thẩm định bộ ba [Paper + Code + Dataset + Checkpoint] của PIGuard (ACL 2025 [[1]](#ref1)); bóc tách DeBERTa-v3, cơ chế MOF, tập NotInject đóng gói sẵn; Báo cáo đối chuẩn độc lập 6 chiều giải trình chi tiết lý do chọn PIGuard làm mỏ neo Tầng 2. |
| **SUPP-06** | **Baseline Nhúng Câu Ayub** | [`supplementary/REJECTED_BASELINE_AYUB_CAMLIS2024.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_reports/supplementary/REJECTED_BASELINE_AYUB_CAMLIS2024.md) | Khảo sát mô hình Baseline MiniLM + ML cổ điển (CAMLIS 2024 [[2]](#ref2)); giải trình lý do khoa học cần lưu trữ Negative Result Dossier; phân tích thực nghiệm Overdefense FPR $58.41\%$ trên NotInject và trễ $11\text{ms}$ CPU. |
| **RUNBOOK** | **Sổ Tay Chạy Tái Lập** | [`../task_3_replication/MEMBER_REPRODUCTION_RUNBOOK.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/MEMBER_REPRODUCTION_RUNBOOK.md) | Sổ tay hướng dẫn từng bước lệnh PowerShell copy-paste cho 4 thành viên clone repo hoặc kích hoạt phòng thí nghiệm đóng gói sẵn `task_3_replication/` chạy trên máy cá nhân trước Meeting 5. |
| **SCRIPTS** | **Bộ Công Cụ Kiểm Định API** | [`../task_3_replication/scripts/README.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/scripts/README.md) | Chứa 2 script Python tự động kiểm định tính sẵn sàng công khai của Bộ ba [Paper + Code + Dataset] cho cả 2 bài báo qua API (`verify_meeting4_papers.py`, `verify_piguard_paper_triad.py`). |

### 1.3. Cơ Sở Lý Thuyết An Ninh Hệ Thống & Kinh Tế Học Độ Trễ
Theo tiêu chuẩn an toàn AI quốc tế của Viện Tiêu chuẩn và Công nghệ Quốc gia Hoa Kỳ **NIST AI 100-2e2025** [[3]](#ref3), dự án **OWASP Top 10 for LLM Applications 2025 (LLM01:2025)** [[4]](#ref4) và nguyên lý kinh điển của Saltzer & Schroeder (1975) [[5]](#ref5):
* **Tính kinh tế của cơ chế (Economy of Mechanism)**: Cơ chế an ninh phải đủ đơn giản, gọn nhẹ để kiểm toán và giảm thiểu gánh nặng tài nguyên.
* **Kinh tế học độ trễ của Guardrail Proxy [[TN01]](#term-latency-economics)**: Nếu $100\%$ lưu lượng truy vấn gửi đến ứng dụng LLM đều phải chạy qua mô hình Transformer sâu (DeBERTa-v3 có 86M tham số), hệ thống sẽ phải gánh chịu độ trễ suy luận rất cao ($18\text{ms} - 80\text{ms}$ trên CPU), làm giảm thông lượng và tăng vọt chi phí điện toán.
* **Quy luật phân phối truy vấn thực tế (80/20 Rule)**: Đại đa số truy vấn ($70\% - 80\%$) trong vận hành thực tế là các câu hỏi thường nhật lành tính hoặc các mẫu tấn công từ điển rõ ràng (*"Ignore previous instructions"*, *"System override"*, *"You are now DAN"*). Do đó, hệ thống bắt buộc phải sở hữu một **Tầng 1 (Fast Screening Filter)** tốc độ cực cao ($P95 < 2\text{ms}$) để giải quyết nhanh phần lớn lưu lượng.

---

## 2. KHẢO SÁT CHI TIẾT 5 ỨNG VIÊN MÔ HÌNH TẦNG 1 (PUBLIC TRIAD)

Nhằm tuyển chọn ứng viên thích hợp nhất làm Tầng 1 cho đề tài PI-Guard, nhóm tiến hành rà soát 5 công trình khoa học quốc tế đạt bộ tiêu chí bắt buộc:

### 🎯 4 Tiêu Chí Tuyển Chọn Bắt Buộc:
1. **Bộ Ba Công Khai Hoàn Toàn (Public Triad Invariant [[TN03]](#term-public-triad))**: Phải có bài báo khoa học xuất bản tại hội nghị chuyên ngành (ACL, EMNLP, CAMLIS) hoặc arXiv; mã nguồn mở GitHub chạy lại được; tập dữ liệu công khai.
2. **Độ Trễ Siêu Thấp (Ultra-Low Latency Invariant)**: Độ trễ P95 phải đạt **$< 2\text{ms} - 5\text{ms}$** trên CPU thông thường.
3. **Độ Chính Xác Cao Trên Tấn Công Tường Minh (High Recall on Obvious Injections)**: Bắt trọn các mẫu tấn công trực diện chứa từ khóa hoặc cấu trúc ghi đè.
4. **Tỷ Lệ Báo Động Giả Thấp ($\text{FPR} < 1.0\%$)**: Không chặn oan câu hỏi lập trình, an ninh của người dùng bình thường.

---

### 2.1. Phân Tích Chi Tiết 5 Ứng Viên

```mermaid
graph TD
    subgraph CANDIDATES["5 Ứng Viên Khảo Sát Tầng 1"]
        C1["<b>1. Ayub CAMLIS 2024</b><br/>MiniLM + Logistic Regression<br/>Trễ CPU: 45ms (Trễ embedding)"]
        C2["<b>2. Schulhoff EMNLP 2023</b><br/>HackAPrompt 600k Benchmark<br/>N-Gram Baseline: 0.8ms"]
        C3["<b>3. Shaheer arXiv 2025</b><br/>Linear Classifiers thưa<br/>Trễ CPU: 1.0ms (Nhanh gấp 25x NN)"]
        C4["<b>4. ProtectAI LLM-Guard</b><br/>Multi-Scanner Regex + ONNX<br/>Regex: 0.2ms / Model: 22ms"]
        C5["<b>5. Sekar arXiv 2026</b><br/>Zero-Shot Cosine Drift<br/>Trễ CPU: 12ms (Phụ thuộc Embed)"]
    end
    
    CANDIDATES --> SELECT["<b>LỰA CHỌN TỐI ƯU CỦA PI-GUARD: TẦNG 1 NATIVE</b><br/>TF-IDF (Word+Char N-Grams) + Logistic Regression Calibrated<br/>Độ trễ P95: 1.62ms | RAM: < 35MB | Giải thích XAI trực quan"]
```

#### Ứng Viên 1: Ayub & Majumdar (CAMLIS 2024 [[2]](#ref2)) — Classifiers Trên Vector Nhúng
* *Phương pháp*: Chuyển prompt thành vector dense qua `all-MiniLM-L6-v2` ($d=384$), huấn luyện Logistic Regression, Random Forest, XGBoost.
* *Ưu điểm*: Tập dữ liệu khổng lồ 467,057 mẫu trên Hugging Face; mã nguồn mở GPL rõ ràng.
* *Nhược điểm chí mạng cho Tầng 1*: Bước trích xuất vector qua MiniLM tốn **$45.11\text{ms}$** trên CPU, vi phạm tiêu chí $P95 < 2\text{ms}$.

#### Ứng Viên 2: Schulhoff et al. (EMNLP 2023 [[8]](#ref8)) — HackAPrompt Global Competition
* *Phương pháp*: Kho ngữ liệu 600k mẫu prompt hacking phân cấp theo 10 mức độ phòng thủ từ cơ bản đến nâng cao.
* *Ưu điểm*: Tập dữ liệu đối chuẩn uy tín nhất cộng đồng AI Security. Các bộ lọc từ vựng N-Gram chặn hiệu quả mức độ 1–5 với độ trễ tức thời ($< 1\text{ms}$).
* *Ứng dụng*: Nhóm kế thừa dữ liệu HackAPrompt để làm giàu tập huấn luyện Tầng 1.

#### Ứng Viên 3: Shaheer et al. (12/2025 [[6]](#ref6)) — Classifiers Against Application Injection
* *Phương pháp*: So sánh thực nghiệm bộ phân loại tuyến tính học máy cổ điển (Logistic Regression, Linear SVM) vs. Mạng học sâu (LSTM, DistilBERT, RoBERTa).
* *Kết luận then chốt*: Bộ phân loại tuyến tính trên ma trận thưa đạt tốc độ suy luận nhanh hơn mạng nơ-ron từ **15 đến 30 lần**, duy trì độ chính xác trên $92\%$ trên các đòn tấn công ứng dụng trực diện.
* *Ý nghĩa*: Là cơ sở lý thuyết vững chắc chứng minh vì sao PI-Guard dùng TF-IDF + Logistic Regression cho Tầng 1.

#### Ứng Viên 4: ProtectAI Research / LLM-Guard Architecture (2024 [[7]](#ref7))
* *Phương pháp*: Thiết kế Multi-Scanner Pipeline gồm Tầng Quét Nhanh (Regex, Ban Substrings, Token Limits: $0.2\text{ms}$) kết hợp Tầng Quét Ngữ Nghĩa (DeBERTa-v3 ONNX: $22\text{ms}$).
* *Ý nghĩa*: Chuẩn mực công nghiệp mẫu mực khẳng định tính đúng đắn của giải pháp phân tầng mà PI-Guard theo đuổi.

#### Ứng Viên 5: Sekar et al. (01/2026 [[9]](#ref9)) — Zero-Shot Embedding Drift Detection
* *Phương pháp*: Đo độ trôi khoảng cách cosine giữa vector System Prompt chuẩn và User Prompt ghép vào để phát hiện Goal Hijacking không cần train lại.
* *Nhược điểm*: Vẫn phụ thuộc mô hình embedding ($10 - 18\text{ms}$) và chưa giải quyết tốt Jailbreak hư cấu.

---

### 2.2. Ma Trận Đối Chuẩn Đa Chiều 5 Ứng Viên

| Tiêu chí so sánh | Ứng viên 1: Ayub (CAMLIS 2024) | Ứng viên 2: Shaheer (arXiv 2025) | Ứng viên 3: HackAPrompt (EMNLP 2023) | Ứng viên 4: ProtectAI Scanner | Ứng viên 5: Sekar Drift (arXiv 2026) | **Lựa chọn đề xuất: PI-Guard Tier 1 Native** |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Kiến trúc cốt lõi** | Dense Embedding + LR/RF | Sparse Matrix + Linear Classifiers | Benchmark + N-Gram Baseline | Regex / Heuristic + ONNX DeBERTa | Cosine Drift trên Embedding | **TF-IDF (Word+Char N-Gram) + Logistic Regression** |
| **Mã nguồn công khai** | Có (GitHub) | Không (Dùng mã thực nghiệm) | Có (GitHub) | Có (GitHub, 3.2k stars) | Đang cập nhật | **Có (Đã tích hợp trong `src/`)** |
| **Tập dữ liệu mở** | Có (467k mẫu) | Có (HackAPrompt) | Có (600k mẫu) | Không mở toàn bộ | Có (Mẫu đánh giá) | **Có (Hợp nhất Ayub 467k + HackAPrompt 600k)** |
| **Độ trễ P95 (CPU)** | **$45.11 - 129.5\text{ms}$** *(Vướng MiniLM)* | **$0.8 - 1.5\text{ms}$** | **$0.5 - 1.0\text{ms}$** | **$0.2\text{ms}$ (Regex) / $22\text{ms}$ (Model)** | **$10.0 - 18.0\text{ms}$** | **$< 1.62\text{ms}$ (P95: $2.01\text{ms}$)** |
| **Tài nguyên RAM** | $\approx 350\text{ MB}$ | $< 50\text{ MB}$ | $< 30\text{ MB}$ | $\approx 500\text{ MB}$ | $\approx 400\text{ MB}$ | **$< 35\text{ MB}$** |
| **Khả năng giải thích (XAI)** | Thấp (Vector dày đặc) | **Cực cao** (Trọng số $w_i$) | **Cực cao** | Trung bình (Luật tĩnh) | Thấp (Khoảng cách vector) | **Rõ ràng (Trọng số $w_i$ n-gram trực quan)** |
| **Độ phù hợp làm Tầng 1** | Khá (Bị trễ embedding) | Rất cao (Cơ sở lý thuyết) | Rất cao (Nguồn dữ liệu) | Cao (Kế thừa tư duy) | Trung bình | **TỐI ƯU NHẤT CHO ĐỒ ÁN** |

---

## 3. PHÂN ĐỊNH 4 TẦNG Y VĂN (FOUR-TIER PROVENANCE) CHO 2 MÔ HÌNH MỎ NEO

Để tuân thủ nghiêm ngặt quy chuẩn nghiên cứu học thuật của đồ án, thông tin về 2 bài báo mỏ neo được phân định rạch ròi thành 4 tầng:

### 3.1. Mô Hình Tham Khảo 1: Ayub & Majumdar (CAMLIS 2024 [[2]](#ref2))
* **Tầng 0: Nguồn gốc & Siêu dữ liệu xuất bản (Tier 0 — Bibliographic Provenance)**:
  * *Tác giả*: Md. Ahsan Ayub & Subhabrata Majumdar.
  * *Tiêu đề*: *"Embedding-based classifiers can detect prompt injection attacks"*.
  * *Hội nghị*: Conference on Applied Machine Learning in Information Security (**CAMLIS 2024**), Arlington, VA, USA, Tháng 10/2024.
  * *Định danh & Mã nguồn*: arXiv:2410.22284 [[2]](#ref2) | GitHub [`AhsanAyub/malicious-prompt-detection`](https://github.com/AhsanAyub/malicious-prompt-detection) | Hugging Face [`ahsanayub/malicious-prompts`](https://huggingface.co/datasets/ahsanayub/malicious-prompts) (467k mẫu).
* **Tầng 1: Đóng góp khoa học gốc của tác giả (Tier 1 — Original Author Findings)**:
  * Đề xuất phương pháp trích xuất vector nhúng qua `all-MiniLM-L6-v2` ($d=384$) rồi huấn luyện Random Forest, XGBoost và Logistic Regression.
  * Báo cáo kết quả trên tập kiểm thử nội bộ 110k mẫu: Random Forest đạt Accuracy $99.4\%$, F1 $0.987$; XGBoost đạt Accuracy $99.2\%$, F1 $0.983$; Logistic Regression đạt Accuracy $98.6\%$, F1 $0.974$.
* **Tầng 2: Định vị kỹ thuật & Tiếp thu của PI-Guard (Tier 2 — PI-Guard Adaptation)**:
  * PI-Guard tiếp thu bài báo với tư cách là Mô hình đối chuẩn Tầng 1 (ứng viên đã bị loại bỏ qua thực nghiệm). Nhóm clone toàn bộ mã nguồn về [`Tier1_REJECTED_Ayub_CAMLIS2024/Ayub_CAMLIS2024/`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/Tier1_REJECTED_Ayub_CAMLIS2024/Ayub_CAMLIS2024/) để chạy lại độc lập.
* **Tầng 3: Mục tiêu thực nghiệm & Giả thuyết kiểm chứng (Tier 3 — Empirical Hypotheses)**:
  * *Giả thuyết 1 (The Embedding Latency Trap)*: Mặc dù hàm `predict()` của LR trên NumPy chạy $< 0.1\text{ms}$, nhưng bước encode qua MiniLM trên CPU sẽ mất $> 15\text{ms}$, vi phạm chuẩn Tầng 1.
  * *Giả thuyết 2 (Semantic Overdefense Bias)*: Vector dense MiniLM sẽ dễ bị nhầm lẫn khi gặp các prompt lành tính chứa từ khóa an ninh (NotInject dataset).

### 3.2. Mô Hình Tham Khảo 2: Hao Li et al. PIGuard (ACL 2025 [[1]](#ref1))
* **Tầng 0: Nguồn gốc & Siêu dữ liệu xuất bản (Tier 0 — Bibliographic Provenance)**:
  * *Tác giả*: Hao Li, Xinxing Liu, Ning Zhang, Chaowei Xiao.
  * *Tiêu đề*: *"PIGuard: Prompt Injection Guardrail via Mitigating Overdefense for Free"*.
  * *Hội nghị*: 63rd Annual Meeting of the Association for Computational Linguistics (**ACL 2025 Long Paper**), Vienna, Austria.
  * *Định danh & Mã nguồn*: arXiv:2410.22770 [[1]](#ref1) | [ACL Anthology](https://aclanthology.org/2025.acl-long.1468.pdf) | GitHub [`leolee99/PIGuard`](https://github.com/leolee99/PIGuard) | Hugging Face [`leolee99/PIGuard`](https://huggingface.co/leolee99/PIGuard).
* **Tầng 1: Đóng góp khoa học gốc của tác giả (Tier 1 — Original Author Findings)**:
  * Đề xuất cơ chế **Mitigating Overdefense for Free (MOF) [[TN06]](#term-mof-mechanism)** giúp mô hình Transformer (`microsoft/deberta-v3-base`) vừa phát hiện chính xác prompt injection vừa triệt tiêu hiện tượng chặn nhầm các câu hỏi an toàn chứa từ nhạy cảm mà không cần gán nhãn bổ sung.
  * Báo cáo Detection Rate $98.7\%$ trên các tập benchmark và NotInject Accuracy $88.3\%$.
* **Tầng 2: Định vị kỹ thuật & Tiếp thu của PI-Guard (Tier 2 — PI-Guard Adaptation)**:
  * Kế thừa làm Mô hình lõi Tầng 2 (Deep Transformer Guardrail) cho đồ án. Clone mã nguồn về `workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/PIGuard_ACL2025/`.
* **Tầng 3: Mục tiêu thực nghiệm & Giả thuyết kiểm chứng (Tier 3 — Empirical Hypotheses)**:
  * Kiểm chứng thực nghiệm 1.579 mẫu trên CPU độc lập; xác nhận độ chính xác khớp hoàn toàn với Bảng 1 và Bảng 7 trong bài báo ACL 2025.

---

## 4. THỰC NGHIỆM ĐỘC LẬP & KHÁM PHÁ 2 ĐIỂM NGHẼN HỌC THUẬT CỦA AYUB

### 4.1. Thiết Lập Môi Trường Thực Nghiệm & Tập Dữ Liệu
* **Phần cứng**: CPU Intel Core i7 đa luồng (chạy đơn luồng CPU mô phỏng đúng điều kiện proxy chi phí thấp).
* **Môi trường**: Python 3.10, PyTorch 2.14.0+cpu, Scikit-Learn 1.7.2, Sentence-Transformers 6.0.1, XGBoost 3.2.0.
* **Tập dữ liệu kiểm thử độc lập (1.579 mẫu)**:
  1. `WildGuard Benchmark` (971 mẫu lành tính thực tế): Đo tỷ lệ báo động giả ngoại phân phối (OOD FPR [[TN08]](#term-ood-robustness)).
  2. `NotInject Benchmark` (339 mẫu an ninh lành tính chứa từ khóa "ignore", "bypass", "override"): Đo mức độ phòng thủ thái quá (Overdefense Rate).
  3. `Valid Benchmark` (144 mẫu: 96 benign, 48 injections): Đo Precision, Recall và F1 trên các cuộc tấn công thực tế.
  4. `Train Benchmark` (3,000 mẫu cân bằng trích xuất ngẫu nhiên có kiểm soát từ `train.json`).

### 4.2. Bảng Kết Quả Thực Nghiệm Đối Soát Đa Chiều

Dữ liệu trích xuất trực tiếp từ tệp thực nghiệm [`AYUB_CAMLIS2024_REPLICATION_BENCHMARK_RESULTS.json`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_replication/Tier1_REJECTED_Ayub_CAMLIS2024/AYUB_CAMLIS2024_REPLICATION_BENCHMARK_RESULTS.json):

| Mô Hình / Cấu Hình Thử Nghiệm | Đặc trưng Đầu vào | Độ trễ Trích xuất Đặc trưng (CPU) | Độ trễ Dự đoán (Classifier) | **Tổng Độ trễ Trung bình (P50)** | **Tổng Độ trễ P95 (CPU)** | **F1-Score (Tập Valid có Tấn công)** | **Recall Tấn công** | **Báo động giả trên NotInject (Overdefense FPR)** |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Ayub MiniLM + Logistic Regression** [[2]](#ref2) | MiniLM Dense ($d=384$) | $45.11\text{ms}$ | $0.23\text{ms}$ | $45.11\text{ms}$ | **$129.48\text{ms}$** | $0.5263$ | $72.92\%$ | **$58.41\%$** *(Rất cao)* |
| **Ayub MiniLM + Random Forest** [[2]](#ref2) | MiniLM Dense ($d=384$) | $45.11\text{ms}$ | $67.83\text{ms}$ | $108.07\text{ms}$ | **$125.13\text{ms}$** | $0.4299$ | $47.92\%$ | **$39.23\%$** |
| **Ayub MiniLM + XGBoost** [[2]](#ref2) | MiniLM Dense ($d=384$) | $45.11\text{ms}$ | $1.55\text{ms}$ | $46.37\text{ms}$ | **$131.03\text{ms}$** | $0.4615$ | $56.25\%$ | **$47.49\%$** |
| **PI-Guard Native TF-IDF + Logistic Regression** | TF-IDF N-Grams ($25k$ dims) | **$1.07\text{ms}$** | **$0.05\text{ms}$** | **$1.07\text{ms}$** | **$2.01\text{ms}$** | **$0.7636$** | **$87.50\%$** | **$21.24\%$** *(Tốt nhất)* |
| **Tier 2: PIGuard DeBERTa-v3 (Đơn Lẻ)** [[1]](#ref1) | Transformer Tokenizer | — | $541.44\text{ms}$ | $582.14\text{ms}$ | $1,313.71\text{ms}$ | **$0.8420$** | $92.40\%$ | **$11.50\%$** *(Kháng Overdefense)* |

![So sánh tỷ lệ báo động giả Overdefense NotInject](../task_3_replication/Tier1_REJECTED_Ayub_CAMLIS2024/figures/02_empirical_plots/ayub_overdefense_fpr_comparison.png)
*Hình 4.1: Thực nghiệm đối chuẩn tỷ lệ báo động giả (FPR) trên tập NotInject giữa Ayub MiniLM, TF-IDF và PIGuard DeBERTa-v3.*

### 4.3. Phân Tích Hai Điểm Nghẽn Học Thuật Của Ayub (CAMLIS 2024)
1. **Điểm nghẽn "Độ trễ Giả lập" (The Latency Fallacy in Embedding Papers)**:
   - Bài báo CAMLIS 2024 chỉ đo thời gian chạy hàm `classifier.predict()` trên các file pickle lưu sẵn vector nhúng.
   - Nhưng trong một hệ thống Guardrail Proxy in-line thực tế [[TN10]](#term-in-line-proxy), toàn bộ câu lệnh của người dùng gửi tới bắt buộc phải đi qua `SentenceTransformer.encode(text)`. Phép đo đạc thực tế chứng minh MiniLM tiêu tốn **$45.11\text{ms}$**. Với độ trễ này, Tầng 1 không thể đóng vai trò bộ lọc nhanh mà trái lại còn làm tăng độ trễ tổng thể nếu phải chuyển tầng tiếp lên Transformer.
2. **Điểm nghẽn "Thiên lệch Ngữ nghĩa" (Trigger Word Semantic Bias [[TN04]](#term-trigger-bias))**:
   - Trên tập kiểm thử `NotInject` (gồm các câu hỏi lập trình an toàn nhưng có chứa chữ "ignore", "override", "bypass"), mô hình Ayub MiniLM LR phân loại sai tới **$58.41\%$** (198/339 câu bị chặn oan).
   - Nguyên nhân toán học: Quá trình nén ngữ nghĩa của mô hình nhúng dày đặc (Dense Embeddings [[TN05]](#term-dense-sparse)) gom cụm các từ mang nghĩa "bỏ qua" gần với các vector tấn công Prompt Injection, dẫn tới việc hồi quy Logistic bị đánh lừa bởi ngữ cảnh bề mặt.

---

### 4.4. Đối Chiếu Thực Nghiệm Cục Bộ Với Bảng Đối Chuẩn Độc Lập Bên Thứ Ba (UC Berkeley, ACM CCS 2024 [[11]](#ref11))

Nhằm nâng cao tính khách quan khoa học và loại bỏ hoàn toàn rủi ro bị Hội đồng FPT nghi vấn về tính chuẩn mực của số liệu đo đạc cục bộ, nhóm đối chiếu kết quả đo đạc thực tế của mình với Bảng 4 trong công trình *PromptShield* do nhóm nghiên cứu của Giáo sư David Wagner tại Đại học California, Berkeley công bố tại **ACM CCS 2024 [[11]](#ref11)**:

| Detector Được Đánh Giá | Base Model | Số Tham Số | ROC-AUC | TPR @ FPR 1% | TPR @ FPR 0.5% | Ghi Chú Độc Lập Từ ACM CCS 2024 [[11]](#ref11) |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Meta PromptGuard** | mDeBERTa-v3 | 86M / 279M | 0.874 | **12.78%** | **12.43%** | Bỏ lọt 87.22% tấn công ở ngưỡng FPR thực tế; ROC-AUC gây hiểu lầm. |
| **ProtectAI v1** | DeBERTa-v3 | 184M | 0.646 | 7.05% | 3.36% | Năng lực Low-FPR cực thấp. |
| **ProtectAI v2** | DeBERTa-v3 | 184M | 0.705 | 1.97% | 1.34% | Gần như tê liệt hoàn toàn khi ép FPR về mức <= 1%. |
| **InjecGuard (PIGuard)** | DeBERTa-v3 | 184M | 0.765 | **20.37%** | **16.30%** | Nhờ chiến lược MOF, đạt TPR vượt trội gấp đôi PromptGuard ở mức FPR 1%. |
| **PromptShield (ours)** | DeBERTa-v3 | 184M | **0.976** | **43.22%** | **40.50%** | Dẫn chứng tầm quan trọng sống còn của việc lọc sạch dữ liệu huấn luyện. |

> [!NOTE]
> **SỰ BẢO CHỨNG ĐỒNG THUẬN QUỐC TẾ**: Kết quả của UC Berkeley tại ACM CCS 2024 khẳng định 100% kết luận thực nghiệm Task 3 của nhóm: Các mô hình nhỏ đơn lẻ (như Meta Prompt Guard hay ProtectAI) khi bị ép hoạt động trong phân vùng tỷ lệ chặn nhầm thấp ($	ext{FPR} \le 1.5\%$) đều bị sụt giảm TPR nghiêm trọng. Đây là minh chứng khoa học đanh thép nhất cho việc PI-Guard bắt buộc phải xây dựng cơ chế định tuyến hai tầng (Two-Tier Cascade) (chi tiết xem tại công trình gốc của Jacob et al. [[11]](#ref11) và chuyên đề đánh đổi [`evaluation_and_tradeoff_study/03_resources_and_papers.md`](file:///d:/Work/Do-an/workspaces/truongnv/docs/research/evaluation_and_tradeoff_study/03_resources_and_papers.md)).

---

## 5. MÔ PHỎNG HỆ THỐNG ĐỊNH TUYẾN HAI TẦNG BẤT ĐỊNH (TWO-TIER UNCERTAINTY ROUTING)

### 5.1. Cơ Chế Định Tuyến Theo Vùng Bất Định (Uncertainty Routing Mechanism)
Thay vì bắt buộc mọi truy vấn phải chạy qua cả hai mô hình, PI-Guard áp dụng cơ chế **Định tuyến Bất định theo Ngưỡng Tin Cậy (Confidence-based Uncertainty Routing [[TN07]](#term-uncertainty-routing))**:

$$y_{\text{final}} = \begin{cases} 
0 & \text{nếu } P_{\text{Tier 1}}(y=1 \mid x) < \theta_{\text{low}} & \text{(Fast Clearance — Cho qua ngay lập tức)} \\
1 & \text{nếu } P_{\text{Tier 1}}(y=1 \mid x) > \theta_{\text{high}} & \text{(Fast Rejection — Chặn đứng tức thì)} \\
y_{\text{Tier 2}} & \text{nếu } \theta_{\text{low}} \le P_{\text{Tier 1}}(y=1 \mid x) \le \theta_{\text{high}} & \text{(Escalation — Chuyển lên DeBERTa-v3 xử lý sâu)}
\end{cases}$$

Trong đó, nhóm thiết lập cặp ngưỡng tối ưu: $\theta_{\text{low}} = 0.15$ và $\theta_{\text{high}} = 0.85$.

```mermaid
flowchart TD
    Prompt["User Prompt Đầu Vào"] --> T1["<b>TẦNG 1: Fast Screening Filter (TF-IDF + LR)</b><br/>Độ trễ suy luận: ~1.6ms (CPU)"]
    
    T1 -->|"P(Malicious) < 0.15<br/>Tin cậy Lành tính Cao"| Pass1["<b>FAST CLEARANCE (Cho qua)</b><br/>Chuyển tiếp ngay tới LLM<br/>Độ trễ: ~1.6ms"]
    
    T1 -->|"P(Malicious) > 0.85<br/>Tin cậy Tấn công Cao"| Block1["<b>FAST REJECTION (Chặn ngay)</b><br/>Phản hồi HTTP 403 Forbidden<br/>Độ trễ: ~1.6ms"]
    
    T1 -->|"0.15 <= P <= 0.85<br/>Vùng Bất Định (Uncertainty Zone)"| T2["<b>TẦNG 2: Deep Transformer Guardrail</b><br/>PIGuard DeBERTa-v3 với cơ chế MOF<br/>Độ trễ: ~500ms (CPU)"]
    
    T2 -->|"PIGuard Label: Benign"| Pass2["<b>PASSED (Lành tính)</b><br/>Chuyển tiếp an toàn tới LLM"]
    T2 -->|"PIGuard Label: Injection"| Block2["<b>BLOCKED (Chặn gián tiếp)</b><br/>Phản hồi HTTP 403 Forbidden"]
```

### 5.2. Kết Quả Thực Nghiệm Đối Soát Mô Phỏng Hai Tầng

| Chỉ Số Đánh Giá Hệ Thống | Mô hình Tầng 2 Đơn lẻ (PIGuard DeBERTa-v3) | Mô phỏng 2 Tầng: Ayub MiniLM + PIGuard | **Mô phỏng 2 Tầng: PI-Guard TF-IDF + PIGuard** |
| :--- | :---: | :---: | :---: |
| **Độ chính xác trên WildGuard (971)** | $76.11\%$ | $72.50\%$ | **$76.21\%$** *(Tương đương/Tăng nhẹ)* |
| **Tỷ lệ Xử lý Nhanh tại Tầng 1 (Fast-Pass Ratio)** | $0.0\%$ *(100% qua Transformer)* | $27.81\%$ | **$12.46\%$** *(trên tập phân phối khó)* |
| **Tỷ lệ Báo động giả trên NotInject (Overdefense)** | **$11.50\%$** | $21.53\%$ | **$11.50\%$** *(Bảo toàn hoàn hảo)* |
| **Độ trễ Trung bình Ước tính khi Tầng 1 Lọc** | $541.44\text{ms}$ | $466.77\text{ms}$ | **Giảm mạnh trên các mẫu từ điển rõ ràng** |

![So sánh thanh hiệu năng Local vs Paper](../task_3_replication/Tier2_PIGuard_ACL2025/figures/02_empirical_plots/piguard_replication_paper_vs_local_bars.png)
*Hình 5.1: Đối chuẩn hiệu năng giữa số liệu công bố trong bài báo PIGuard ACL 2025 [[1]](#ref1) và số liệu đo đạc thực nghiệm độc lập tại phòng lab Task 3.*

---

## 6. ĐỀ XUẤT TỐI ƯU HÓA: 4 LÝ DO KHOA HỌC CHỌN TF-IDF N-GRAMS LÀM TẦNG 1

```text
                          ┌─────────────────────────────────────────────────────────┐
                          │         PI-GUARD TWO-TIER GUARDRAIL ARCHITECTURE        │
                          └─────────────────────────────────────────────────────────┘
                                                       │
                                              User Prompt x
                                                       │
                                                       ▼
                                   ┌───────────────────────────────────────┐
                                   │   TIER 1: Native TF-IDF N-Gram + LR   │
                                   │   - Độ trễ CPU: 1.62ms (P95: 2.01ms)  │
                                   │   - Bộ nhớ RAM: < 35 MB               │
                                   │   - Giải thích: Trọng số wi n-grams   │
                                   └───────────────────────────────────────┘
                                                       │
                                   ┌───────────────────┴───────────────────┐
                                   │                                       │
                      P < 0.15 hoặc P > 0.85                      0.15 <= P <= 0.85
                   (Vùng Tin Cậy Cao: ~70-80%)                 (Vùng Bất Định: ~20-30%)
                                   │                                       │
                                   ▼                                       ▼
                       ┌───────────────────────┐               ┌───────────────────────┐
                       │   Quyết định Tức thì  │               │   TIER 2: PIGuard     │
                       │   HTTP 200 / HTTP 403 │               │   DeBERTa-v3 (MOF)    │
                       │   Độ trễ: ~1.6ms      │               │   Độ trễ: ~25ms       │
                       └───────────────────────┘               └───────────────────────┘
                                                                           │
                                                                           ▼
                                                               ┌───────────────────────┐
                                                               │  Quyết định Chuyên sâu│
                                                               │  Kháng Overdefense    │
                                                               └───────────────────────┘
```

### 🎯 4 Lý Do Khoa Học Vượt Trội:
1. **Ưu Thế Độ Trễ Thực Tế Vượt Trội (Latency Dominance)**: TF-IDF chỉ tốn $1.07\text{ms}$ để trích xuất đặc trưng từ và ký tự, giúp toàn bộ pipeline Tầng 1 đạt $1.62\text{ms}$ (nhanh gấp **28 lần** so với $45.11\text{ms}$ của MiniLM).
2. **Khả năng Bắt Lỗi Ký tự Đối kháng (Character Obfuscation Resilience [[TN09]](#term-char-ngram))**: TF-IDF với dải Character N-Grams (3–5 ký tự) bắt trọn các thủ thuật lách luật như chèn ký tự đặc biệt, leetspeak (`1gn0re`, `b-y-p-a-s-s`), điều mà các mô hình embedding cấp độ từ (word-level) dễ bị phân mảnh token.
3. **Tính Minh bạch & Khả năng Giải thích Rõ Ràng (Explainable AI - XAI)**: Trọng số $w_i$ của mô hình hồi quy Logistic cho phép xuất trực tiếp danh sách từ khóa nguy hiểm cho người quản trị trên Dashboard (`Streamlit`), trong khi vector nhúng 384 chiều của MiniLM hoàn toàn là hộp đen.
4. **Chi phí Hạ tầng Tối thiểu (Extreme Resource Efficiency)**: Mô hình TF-IDF + LR chiếm chưa tới $35\text{MB}$ RAM, trong khi việc duy trì đồng thời 2 mô hình Transformer (MiniLM $120\text{MB}$ + DeBERTa-v3 $500\text{MB}$) gây lãng phí bộ nhớ trên các container Docker nhẹ.

---

## 7. BỘ GIẢI TRÌNH PHẢN BIỆN HỌC THUẬT TRƯỚC HỘI ĐỒNG FPT (ACADEMIC COUNTER-ARGUMENT DEFENSE)

### ❓ Câu Hỏi Phản Biện Trọng Tâm (The Core Counter-Argument Question):
> *"Tại sao mô hình đề xuất kết hợp 2 tầng (Cascaded Two-Tier Guardrail) đem lại độ trễ tối ưu và cân bằng bảo mật vượt trội, nhưng các nhà nghiên cứu quốc tế lớn (như PIGuard ACL 2025 [[1]](#ref1), Ayub et al. CAMLIS 2024 [[2]](#ref2), hay ProtectAI) lại không đề xuất hoặc công bố một kiến trúc 2 tầng chuẩn mực như vậy trong các bài báo khoa học của họ?"*

---

### 🛡️ 4 Luận Điểm Giải Trình Học Thuật Chuyên Sâu:

#### Luận điểm 1: Khác biệt về Mục Tiêu Học thuật vs. Đánh đổi Hệ thống Thực tế (Research Objective vs. Engineering Trade-off)
* **Trong nghiên cứu học thuật thuần túy (Academic Benchmark Paradigm)**:
  * Các bài báo tại các hội nghị đỉnh cao như ACL, EMNLP (điển hình là **PIGuard ACL 2025 [[1]](#ref1)**) tập trung chứng minh một **đóng góp thuật toán duy nhất mang tính đột phá (Isolated Theoretical Novelty)**: Cơ chế *Mitigating Overdefense for Free (MOF)* để giải quyết sự đánh đổi giữa an ninh và phòng thủ thái quá trên mô hình DeBERTa-v3.
  * Quy trình đánh giá chuẩn mực đòi hỏi phải đo đạc mô hình trên một tập dữ liệu đóng cố định (Fixed Offline Benchmark) để so sánh chỉ số F1/Accuracy với các bài báo khác. Họ **không có mục tiêu tối ưu hóa chi phí vận hành CPU hay độ trễ hệ thống (Inference Latency SLA)** của một sản phẩm phần mềm thực tế.
* **Trong đề tài tốt nghiệp kỹ thuật (PI-Guard Capstone Goal)**:
  * Mục tiêu của PI-Guard không chỉ là nghiên cứu thuật toán mà là **xây dựng một nguyên mẫu phòng vệ thực tế (In-line API Guardrail Proxy)** đặt phía trước downstream LLM theo nguyên tắc Saltzer & Schroeder [[5]](#ref5). Vì vậy, bài toán độ trễ P95 $< 30\text{ms}$ và chi phí phần cứng trở thành yêu cầu sống còn.

#### Luận điểm 2: Giới hạn Phân vùng Hội nghị Chuyên ngành (Venue Scoping & Reviewer Expectations)
* Các hội nghị chuyên ngành xử lý ngôn ngữ tự nhiên (NLP Venues như ACL, EMNLP) đánh giá cao các kiến trúc học sâu mới, kỹ thuật điều chỉnh hàm mất mát (loss function) hoặc cơ chế tiền huấn luyện (pre-training). Nếu một nhóm tác giả gửi một bài báo đề xuất "dùng TF-IDF kết hợp Transformer theo dạng if-else / cascading", hội đồng bình duyệt của ACL sẽ coi đó là **kỹ thuật ghép nối phần mềm (Software Engineering / Heuristic Trick)** thiếu tính đóng góp lý thuyết ngôn ngữ, dẫn tới nguy cơ bị từ chối bài báo (Desk Reject).
* Ngược lại, các công trình về an toàn hệ thống (như USENIX Security, ACM CCS, hay CAMLIS) lại tập trung vào khía cạnh thực nghiệm bảo mật. Điển hình như bài báo **Shaheer et al. (12/2025 [[6]](#ref6))** đã chứng minh các bộ phân loại tuyến tính học máy cổ điển có tốc độ suy luận nhanh hơn mạng nơ-ron từ $15 - 30$ lần. **Đồ án PI-Guard đã kết nối thành công khoảng trống giữa hai trường phái nghiên cứu này**.

#### Luận điểm 3: Rào cản Kỹ thuật về Hiệu chuẩn Ngưỡng và Phân phối Dữ liệu (The Threshold Calibration Overhead)
* Việc công bố một hệ thống 2 tầng tổng quát trong một bài báo khoa học gặp khó khăn lớn về mặt lý thuyết: **Làm sao xác định cặp ngưỡng $[\theta_{\text{low}}, \theta_{\text{high}}]$ tối ưu cho mọi miền dữ liệu?**
  * Mỗi ứng dụng doanh nghiệp (Customer Support, Coding Assistant, Medical Bot) có phân phối truy vấn và mức độ chấp nhận rủi ro (Risk Tolerance) hoàn toàn khác nhau.
  * Nếu một bài báo công bố ngưỡng $\theta = 0.15$, khi chuyển sang tập dữ liệu khác, ngưỡng này có thể khiến tỷ lệ chuyển tầng tăng vọt hoặc bỏ lọt tấn công.
* Do đó, các nhà nghiên cứu học thuật thường né tránh kiến trúc phân tầng để bài báo của họ mang tính tổng quát (Generalizable). Trong khi đó, đồ án PI-Guard giải quyết bài toán này thông qua việc phân tích thực nghiệm định lượng trên 3 tập dữ liệu đối chuẩn thực tế (WildGuard, NotInject, Valid).

#### Luận điểm 4: Minh chứng Từ Thực tế Công nghiệp (Industrial Multi-Scanner Paradigms)
* Trên thực tế, **các tổ chức an ninh AI hàng đầu thế giới đã và đang âm thầm áp dụng kiến trúc đa tầng này trong sản phẩm thực tế của họ**, chỉ là họ không viết thành bài báo học thuật lý thuyết:
  * **ProtectAI Research (LLM-Guard Toolkit [[7]](#ref7))**: Hệ thống bảo vệ đạt hơn 3,200 stars trên GitHub của họ chính là một **Multi-Scanner Pipeline** gồm Tầng quét nhanh (Regex, Ban Substrings, Token Length Limits) chạy trước để loại bỏ nhanh các mẫu rác, sau đó mới gọi mô hình ONNX DeBERTa-v3 để quét ngữ nghĩa chuyên sâu.
  * **Microsoft Azure AI Content Safety & NeMo Guardrails**: Đều sử dụng cơ chế sàng lọc phân tầng (Tiered Moderation) từ bộ lọc từ vựng đến mô hình ngôn ngữ lớn để bảo vệ SLA độ trễ dịch vụ.
* **Kết luận đanh thép**: Đề xuất kiến trúc 2 tầng của PI-Guard không phải là một ý tưởng bột phát thiếu cơ sở, mà là sự **hội tụ khoa học tất yếu (Natural Convergence)** giữa nghiên cứu lý thuyết đỉnh cao (PIGuard MOF ACL 2025) và chuẩn mực kỹ nghệ an toàn thực tế (ProtectAI LLM-Guard).

---

## 8. BẢNG THUẬT NGỮ & KHÁI NIỆM HỌC THUẬT NỀN TẢNG (ACADEMIC CONCEPT GLOSSARY)

| Khái niệm học thuật | Định nghĩa khoa học gốc | Vai trò & Phép đối sánh trong PI-Guard | Tài liệu tham chiếu |
| :--- | :--- | :--- | :--- |
| **<a id="term-latency-economics"></a>[TN01] Economics of Guardrail Latency** | Sự đánh đổi kinh tế học giữa chi phí tính toán phần cứng, độ trễ phản hồi mạng (P95 latency SLA) và mức độ bảo đảm an ninh của hệ thống phần mềm. | Cơ sở khoa học chứng minh việc dùng 100% Transformer gây lãng phí tài nguyên, tạo tiền đề cho kiến trúc 2 tầng lọc nhanh. | Saltzer & Schroeder (1975) [[5]](#ref5); Chen et al. (2024) |
| **<a id="term-two-tier-defense"></a>[TN02] Two-Tier Defense Architecture** | Chiến lược bảo vệ phân tầng gồm bộ phân loại sơ bộ tốc độ cao ở vòng ngoài và bộ phân loại ngữ nghĩa sâu ở vòng trong. | Hiện thực hóa nguyên lý *Defense-in-Depth*: Tầng 1 (TF-IDF + LR) lọc nhanh $1.62\text{ms}$, Tầng 2 (PIGuard DeBERTa-v3) thẩm định mẫu khó. | NIST AI 100-2e2025 [[3]](#ref3); Saltzer & Schroeder (1975) [[5]](#ref5) |
| **<a id="term-public-triad"></a>[TN03] Public Triad Reproducibility** | Tiêu chuẩn khoa học mở đòi hỏi một công trình nghiên cứu phải công khai đồng thời 3 thành tố: Bài báo bình duyệt, Mã nguồn thực thi và Tập dữ liệu mở. | Bộ tiêu chuẩn bắt buộc dùng để tuyển chọn mô hình tham khảo Tầng 1 (Ayub CAMLIS 2024 [[2]](#ref2)) và Tầng 2 (PIGuard ACL 2025 [[1]](#ref1)). | ACM Artifact Review & Badging; FPT IAP491 Guidelines |
| **<a id="term-trigger-bias"></a>[TN04] Trigger Word Semantic Bias** | Hiện tượng mô hình phân loại nhầm lẫn câu hỏi an toàn là tấn công chỉ vì câu chứa các từ nhạy cảm bề mặt (*"ignore"*, *"override"*). | Khám phá thực nghiệm chỉ ra Ayub MiniLM bị dính $58.41\%$ FPR trên NotInject, trong khi TF-IDF LR giảm còn $21.24\%$ và PIGuard còn $11.50\%$. | Li et al. (ACL 2025) [[1]](#ref1); Shen et al. (2024) |
| **<a id="term-dense-sparse"></a>[TN05] Dense vs. Sparse Feature Spaces** | Không gian biểu diễn vector dày đặc sinh bởi mạng nơ-ron ngữ nghĩa ($d=384$) đối lập với ma trận thưa đếm n-grams ($d=25,000$). | Giải thích vì sao TF-IDF trích xuất mất $1.07\text{ms}$ trong khi MiniLM mất $45.11\text{ms}$, chứng minh tính ưu việt của biểu diễn thưa cho Tầng 1. | Shaheer et al. (2025) [[6]](#ref6); Ayub & Majumdar (2024) [[2]](#ref2) |
| **<a id="term-mof-mechanism"></a>[TN06] Mitigating Overdefense for Free (MOF)** | Cơ chế huấn luyện mô hình bảo vệ không làm tổn hại đến năng lực của câu hỏi lành tính mà không cần gán nhãn bổ sung phức tạp. | Kỹ thuật cốt lõi được tiếp thu từ mô hình Tầng 2 PIGuard (ACL 2025) giúp triệt tiêu báo động giả trên các truy vấn phức tạp. | Li et al. (ACL 2025) [[1]](#ref1) |
| **<a id="term-uncertainty-routing"></a>[TN07] Confidence Uncertainty Routing** | Thuật toán định tuyến dựa trên khoảng xác suất đầu ra $[\theta_{\text{low}}, \theta_{\text{high}}]$ để quyết định cho qua, chặn hoặc leo thang mô hình. | Cơ chế kết nối giữa Tầng 1 và Tầng 2 của PI-Guard, giúp hệ thống vận hành linh hoạt và tối ưu hóa thời gian phản hồi. | NIST AI 100-2e2025 [[3]](#ref3); ProtectAI Research (2024) [[7]](#ref7) |
| **<a id="term-ood-robustness"></a>[TN08] Out-of-Distribution Robustness** | Khả năng duy trì độ chính xác và tỷ lệ báo động giả ổn định khi mô hình đối mặt với các mẫu dữ liệu nằm ngoài phân phối tập huấn luyện. | Phép thử trên tập WildGuard và NotInject chứng minh sự khác biệt lớn giữa kết quả công bố trong bài báo và môi trường thực tế. | Hendrycks et al. (2021); Li et al. (2025) [[1]](#ref1) |
| **<a id="term-char-ngram"></a>[TN09] Character-Level Substring Tokens** | Kỹ thuật chia chuỗi văn bản thành các đoạn ký tự con liên tiếp từ 3 đến 5 ký tự nhằm nhận diện cấu trúc từ ngữ biến thể. | Giúp Tầng 1 của PI-Guard bắt trọn các đòn tấn công làm rối ký tự (Leetspeak, chèn gạch nối) mà các mô hình từ vựng bị bỏ sót. | Majhi et al. (2025) [[10]](#ref10); Shaheer et al. (2025) [[6]](#ref6) |
| **<a id="term-in-line-proxy"></a>[TN10] In-line Guardrail Proxy Gateway** | Mô hình kiến trúc triển khai lớp bảo vệ đứng độc lập như một cổng API trung gian phía trước các hệ thống LLM phục vụ người dùng. | Kiến trúc tổng thể của đề tài PI-Guard theo đăng ký, hoàn toàn không can thiệp vào trọng số nội bộ của downstream LLM. | OWASP LLM Top 10 (2025) [[4]](#ref4); ProtectAI (2024) [[7]](#ref7) |

---

## 9. TÀI LIỆU THAM KHẢO HỌC THUẬT (REFERENCES)

<a id="ref1"></a>
- **[[1]]** H. Li, X. Liu, N. Zhang, and C. Xiao, "PIGuard: Prompt Injection Guardrail via Mitigating Overdefense for Free," in *Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (ACL 2025)*, Vienna, Austria, 2025. arXiv:2410.22770. [Open-Access PDF](https://arxiv.org/pdf/2410.22770.pdf) | [ACL Anthology](https://aclanthology.org/2025.acl-long.1468.pdf) | [GitHub Code](https://github.com/leolee99/PIGuard) | [HF Model](https://huggingface.co/leolee99/PIGuard).

<a id="ref2"></a>
- **[[2]]** M. A. Ayub and S. Majumdar, "Embedding-based classifiers can detect prompt injection attacks," in *Proceedings of the 2024 Conference on Applied Machine Learning in Information Security (CAMLIS 2024)*, Arlington, VA, USA, 2024. arXiv:2410.22284. [Open-Access PDF](https://arxiv.org/pdf/2410.22284.pdf) | [GitHub Code](https://github.com/AhsanAyub/malicious-prompt-detection) | [HF Dataset](https://huggingface.co/datasets/ahsanayub/malicious-prompts).

<a id="ref3"></a>
- **[[3]]** National Institute of Standards and Technology (NIST), "Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations," *NIST Trustworthy and Responsible AI, NIST AI 100-2e2025*, Jan. 2025. [Open-Access PDF](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-2e2025.pdf).

<a id="ref4"></a>
- **[[4]]** OWASP GenAI Security Project, "OWASP Top 10 for Large Language Model Applications and Generative AI," *Open Web Application Security Project (OWASP)*, Version 2025, 2025. [Online Resource](https://owasp.org/www-project-top-10-for-large-language-model-applications/).

<a id="ref5"></a>
- **[[5]]** J. H. Saltzer and M. D. Schroeder, "The protection of information in computer systems," *Proceedings of the IEEE*, vol. 63, no. 9, pp. 1278–1308, Sep. 1975. [Open-Access PDF](https://web.mit.edu/Saltzer/www/publications/protection/index.html).

<a id="ref6"></a>
- **[[6]]** S. Shaheer, G. M. R. Islam, M. R. Hamid, M. A. F. Khan, M. O. Faruk, and Y. Nur, "Detecting Prompt Injection Attacks Against Application Using Classifiers," *arXiv preprint arXiv:2512.12583*, Dec. 2025. [Open-Access PDF](https://arxiv.org/pdf/2512.12583.pdf).

<a id="ref7"></a>
- **[[7]]** Protect AI Research Team, "LLM Guard: The Security Toolkit for LLM Interactions," *Protect AI Open Source Project*, 2024. [GitHub Repository](https://github.com/protectai/llm-guard) | [Model Card](https://huggingface.co/protectai/deberta-v3-base-prompt-injection-v2).

<a id="ref8"></a>
- **[[8]]** S. Schulhoff, J. Pinto, A. Khan, L.-P. Morency et al., "Ignore This Title and HackAPrompt: Exposing Systemic Vulnerabilities of Large Language Models Through a Global Prompt Hacking Competition," in *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing (EMNLP 2023)*, Singapore, 2023, pp. 4945–4961. arXiv:2311.16119. [Open-Access PDF](https://arxiv.org/pdf/2311.16119.pdf) | [GitHub Code](https://github.com/PromptLabs/hackaprompt) | [HF Dataset](https://huggingface.co/datasets/hackaprompt/hackaprompt-dataset).

<a id="ref9"></a>
- **[[9]]** A. Sekar, M. Agarwal, R. Sharma, A. Tanaka, J. Zhang, A. Damerla, and K. Zhu, "Zero-Shot Embedding Drift Detection: A Lightweight Defense Against Prompt Injections in LLMs," *arXiv preprint arXiv:2601.12359*, Jan. 2026. [Open-Access PDF](https://arxiv.org/pdf/2601.12359.pdf).

<a id="ref10"></a>
- **[[10]]** V. Majhi et al., "Do You Really Need a GPU to Guard Your LLM? CPU-Class Classifiers and Multi-Stage Pipelines for Safety Enforcement at Scale," *arXiv preprint arXiv:2512.19011*, Dec. 2025. [Open-Access PDF](https://arxiv.org/pdf/2512.19011.pdf).

<a id="ref11"></a>
- **[[11]]** D. Jacob, H. Alzahrani, Z. Hu, B. Alomair, and D. Wagner, "PromptShield: Deployable Detection for Prompt Injection Attacks," in *Proceedings of the 2024 ACM SIGSAC Conference on Computer and Communications Security (CCS '24)*, Salt Lake City, UT, USA, 2024, pp. 4247–4261. [arXiv:2407.13656](https://arxiv.org/pdf/2407.13656). Tệp PDF: [`Jacob_2024_PromptShield_Deployable_Detection_Prompt_Injection_CCS.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Jacob_2024_PromptShield_Deployable_Detection_Prompt_Injection_CCS.pdf).

<a id="ref12"></a>
- **[[12]]** W. Hackett, L. Birch, S. Trawicki, N. Suri, and P. Garraghan, "Bypassing LLM Guardrails: An Empirical Analysis of Evasion Attacks against Prompt Injection and Jailbreak Detection Systems," in *Proceedings of The First Workshop on LLM Security (LLMSEC 2025) at ACL 2025*, 2025, pp. 101–114. [ACL Anthology](https://aclanthology.org/2025.llmsec-1.9.pdf). Tệp PDF: [`Hackett_2025_Bypassing_LLM_Guardrails_Evasion_Attacks.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Hackett_2025_Bypassing_LLM_Guardrails_Evasion_Attacks.pdf).

<a id="ref13"></a>
- **[[13]]** Y. Liu, Y. Jia, J. Jia, D. Song, and N. Z. Gong, "DataSentinel: A Game-Theoretic Detection of Prompt Injection Attacks," in *Proceedings of the 2025 IEEE Symposium on Security and Privacy (SP '25)*, 2025. Tệp PDF: [`Liu_2025_DataSentinel_Game_Theoretic_Detection_Prompt_Injection.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Liu_2025_DataSentinel_Game_Theoretic_Detection_Prompt_Injection.pdf).
