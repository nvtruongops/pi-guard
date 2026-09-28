# 🛡️ Rule 04: Sentence-Level Evidence Grounding & Attribution Standards

> **Quy định bất biến về bảo chứng bằng chứng cấp độ câu, trích dẫn khoa học chính xác và loại bỏ triệt để các khẳng định võ đoán không nguồn**  
> **Cơ chế thực thi**: Tự động kiểm toán qua `python Final-Report/scripts/audit_claim_evidence.py` và tích hợp vào `validate_local.py`.

---

## 🚫 1. BỐN NGUYÊN TẮC BẤT BIẾN CỐT LÕI (FOUR NON-NEGOTIABLE INVARIANTS)

### 🔴 Nguyên Tắc 1: MỌI CÂU KHẲNG ĐỊNH KỸ THUẬT PHẢI CÓ NEO DẪN CHỨNG (Sentence-Level Evidence Invariant)
1. **Phạm Vi Áp Dụng**: Mọi câu văn đề cập đến: Cơ chế tấn công (Prompt Injection, Jailbreak, Adversarial Evasion), kiến trúc mô hình (Transformer, DeBERTa, ELECTRA, RTD, GDES, TF-IDF, Attention), đặc tính dữ liệu (BPE tokenization, Out-of-vocabulary, class imbalance), và chỉ số an toàn (FPR, P95 latency, TPR @ 1%).
2. **Quy Định Bắt Buộc**:
   - Câu văn **PHẢI** gắn kèm neo trích dẫn khoa học `[[N]](#refN)` trỏ trực tiếp đến tài liệu tham khảo tương ứng trong `REFERENCES_LOG.md`.
   - Tuyệt đối không viết một đoạn văn dài gồm 5–7 câu kỹ thuật mà chỉ gắn một trích dẫn duy nhất ở cuối đoạn hoặc không gắn trích dẫn nào.

---

### 🔴 Nguyên Tắc 2: CẤM TUYỆT ĐỐI VĂN PHONG DẪN NGUỒN MƠ HỒ (Zero Vague Attribution)
1. **Danh Sách Mẫu Câu Bị Chặn**:
   - 🚫 *"Theo các nghiên cứu gần đây..."* $\rightarrow$ Vi phạm vì không định danh tác giả và năm.
   - 🚫 *"Các chuyên gia / nhà khoa học an ninh bảo mật chỉ ra rằng..."* $\rightarrow$ Vi phạm vì phát ngôn vô bằng chứng.
   - 🚫 *"Thực tế cho thấy / như chúng ta đã biết..."* $\rightarrow$ Vi phạm vì coi giả định chủ quan là chân lý hiển nhiên.
   - 🚫 *"Theo y văn / theo lý thuyết chuẩn..."* $\rightarrow$ Vi phạm vì không có địa chỉ bài báo cụ thể.
2. **Quy Chuẩn Chuyển Đổi Bắt Buộc**:
   - Bắt buộc phải thay bằng tên tác giả cụ thể kèm năm và neo trích dẫn:
     - ✅ *"Theo khảo sát của Zhao et al. (2023) [[1]](#ref1)..."*
     - ✅ *"Wei et al. (NeurIPS 2023) [[5]](#ref5) chứng minh rằng..."*
     - ✅ *"Thực nghiệm đo đạc độc lập trên tập D6 tại `cross_dataset_empirical_matrix.json` cho thấy..."*

---

### 🔴 Nguyên Tắc 3: PHÂN ĐỊNH RÕ RÀNG RANH GIỚI NHẬN THỨC (Epistemic Boundary Decoupling)
Mọi câu văn phát sinh trong quá trình trao đổi hoặc soạn thảo văn bản phải phân định rõ ràng 3 ranh giới nhận thức:
1. **Ranh Giới Y Văn (Literature Fact)**: Dùng khi tường thuật kết quả của người khác: *"Theo tác giả X et al. [[N]](#refN)..."*
2. **Ranh Giới Thực Nghiệm Đã Đo (Empirical Fact)**: Dùng khi trích dẫn kết quả đo đạc thực tế của nhóm: *"Kết quả đo đạc độc lập un-mocked tại file JSON `04_benchmarks_and_data/<file>.json` cho thấy..."*
3. **Ranh Giới Đề Xuất Lý Thuyết Của Đồ Án (PI-Guard Proposal)**: Dùng khi mô tả kiến trúc Two-Tier Cascade của nhóm cho Chương 3: *"Trong phạm vi thiết kế đề xuất của đề tài PI-Guard (Chương 3), nhóm định hướng... nhằm hướng tới chỉ tiêu thiết kế SLA..."*
   - Tuyệt đối không phát biểu ý tưởng thiết kế như thể đó là kết quả đã được đo đạc.

---

### 🔴 Nguyên Tắc 4: BẢO CHỨNG BẰNG CHỨNG TRƯỚC KHI XUẤT XƯỞNG (Evidence-Before-Assertion Invariant)
1. **Nguyên Tắc "Không Biết Thì Không Khẳng Định"**:
   - Nếu Agent không chắc chắn bài báo nào chứng minh một hiện tượng, Agent **PHẢI** tra cứu `REFERENCES_LOG.md` trước.
   - Nếu hiện tượng đó không có trong danh mục bài báo lưu trữ, Agent **PHẢI** nói rõ: *"Hiện tượng này là nhận định kỹ thuật cần kiểm chứng, chưa có trong danh mục bài báo chính thức của đề tài"*, tuyệt đối không tự bịa ra trích dẫn hoặc câu khẳng định suông.

---

## 🔍 2. CƠ CHẾ KIỂM TOÁN TỰ ĐỘNG (AUTOMATED ENFORCEMENT)

- Công cụ: `python Final-Report/scripts/audit_claim_evidence.py`
- Tích hợp: `validate_local.py --mode fast`
- Bất kỳ câu văn kỹ thuật nào chứa từ khóa học thuật mà thiếu trích dẫn hoặc chứa cụm từ mơ hồ sẽ bị trả về **EXIT CODE 1** và chặn commit.
