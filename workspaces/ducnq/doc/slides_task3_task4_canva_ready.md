# 📋 TÀI LIỆU COPY-PASTE NHANH QUA CANVA / POWERPOINT (TASK 3 & TASK 4)
## WORKSPACE: `workspaces/ducnq/doc/slides_task3_task4_canva_ready.md`
**Người thực hiện**: Nguyễn Quí Đức (`SE182087`)  
**Tiêu chí thiết kế**: **Đúng 2 Slide siêu tinh gọn** cho Task 3 & Task 4, hình to rõ, cực ít chữ, copy phát ăn ngay vào Canva!

---

# 🖼️ SLIDE 3 (TASK 3): THỰC NGHIỆM TÁI LẬP Y VĂN TRÊN MÁY CÁ NHÂN (REPLICATION BENCHMARK)

### [TIÊU ĐỀ SLIDE]
```text
TASK 3: INDEPENDENT EXPERIMENTAL REPLICATION PIPELINE
```

### [3 BƯỚC THỰC NGHIỆM ĐỘC LẬP TRÊN MÁY (3 CỘT ICON)]

* **BƯỚC 1: DỮ LIỆU ĐỐI CHUẨN (DATASET CURATION)**
  - Tải tập dữ liệu mở chuẩn từ Hugging Face (`deepset/prompt-injections`, `JailbreakV-28K`).
  - Phân tách nghiêm ngặt: $80\%$ Train / $20\%$ Test (chống rò rỉ dữ liệu).

* **BƯỚC 2: HUẤN LUYỆN ĐỐI SÁNH (MODEL BENCHMARKING)**
  - **Mô hình 1 (Classical ML)**: TF-IDF (`char_wb`, n-gram 3–5) + LinearSVC / LogisticRegression.
  - **Mô hình 2 (Transformer)**: DeBERTa-v3 Fine-Tuning với hàm mất mát Focal Loss.

* **BƯỚC 3: KIỂM THỬ ĐỘI ĐỐI KHÁNG (ADVERSARIAL STRESS TEST)**
  - Dùng bộ công cụ `src/jailguard_mutators.py` kiểm tra 10 lát cắt biến dị.
  - Đo đạc 4 chỉ số vàng: $\text{Recall (TPR)}$, $\text{FPR} < 1.5\%$, $\text{Latency P95}$, $F_1\text{-score}$.

### [THANH CHỐT Ở ĐÁY SLIDE (TAG)]
```text
🔬 Mục tiêu: Tái lập 100% kết quả từ bài báo NeurIPS 2023 & ICLR 2023 trên máy cá nhân
```

---

# 🖼️ SLIDE 4 (TASK 4): ĐÓNG GÓP CẢI TIẾN & BẢN SẮC ĐỒ ÁN PI-GUARD (PROPOSED SYSTEM)

### [TIÊU ĐỀ SLIDE]
```text
TASK 4: PI-GUARD PROPOSED ARCHITECTURAL CONTRIBUTIONS
```

### [3 ĐÓNG GÓP KỸ THUẬT ĐỘT PHÁ CỦA PI-GUARD (3 KHỐI CARD)]

* **ĐÓNG GÓP 1: TẦNG TIỀN XỬ LÝ CHUẨN HÓA (HEURISTIC SCRUBBER)**
  - Tự động chuẩn hóa **Unicode NFKC** bóc tách sạch sẽ các ký tự tàng hình Zero-Width (`\u200B`).
  - Giải mã Leetspeak cơ bản và kéo dính khoảng trắng bị bẻ gãy (`i g n o r e` $\rightarrow$ `ignore`).

* **ĐÓNG GÓP 2: ĐIỀU PHỐI PHÂN TẦNG 2 CẤP ĐỘ (TWO-TIER CASCADE ROUTING)**
  - **Tầng 1 (Fast-Pass)**: TF-IDF siêu nhẹ giải quyết $\approx 82.6\%$ truy vấn thông thường trong $< 0.5\text{ms}$.
  - **Tầng 2 (Deep Arbiter)**: DeBERTa-v3 INT8 chỉ thẩm định $17.4\%$ câu mờ ám khó phân định.

* **ĐÓNG GÓP 3: TỐI ƯU HÓA ĐỘ TRỄ & HẠ TẦNG (INT8 QUANTIZATION)**
  - Lượng tử hóa mô hình sang **ONNX Runtime INT8**, giảm dung lượng từ 500MB xuống $< 130\text{MB}$.
  - Chạy mượt mà trên **CPU thông thường**, đạt độ trễ kỳ vọng $\mathbb{E}[L] \approx 3.69\text{ms}$ (P95 $< 20\text{ms}$).

### [THANH CHỐT KẾT QUẢ Ở ĐÁY SLIDE]
```text
🎯 Chuẩn Mực Hệ Thống: An Toàn Tuyệt Đối Tại Ingress | FPR < 1.5% | Độ Trễ Cực Thấp P95 < 20ms
```
