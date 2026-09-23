# 📋 TÀI LIỆU COPY-PASTE NHANH QUA CANVA / POWERPOINT (TASK 2)
## WORKSPACE: `workspaces/ducnq/doc/slides_task2_canva_ready.md`
**Người thực hiện**: Nguyễn Quí Đức (`SE182087`)  
**Tiêu chí thiết kế**: **Đúng 2 Slide siêu tinh gọn**, hình to rõ, cực ít chữ, copy phát ăn ngay vào Canva!

---

# 🖼️ SLIDE 1: BỀ MẶT TẤN CÔNG & 2 KÊNH INGRESS (ATTACK VECTORS)

### [TIÊU ĐỀ SLIDE]
```text
ATTACK SURFACE: 2 INGRESS CHANNELS & 5D FRAMEWORK
```

### [KHUNG TRÁI: KÊNH 1]
* **Tiêu đề khối**: `DIRECT INGRESS (CHAT UI / API)`
* **Chiêu thức lách luật**:
  - Chèn khoảng trắng (`i g n o r e`)
  - Biến dị Leetspeak (`1gn0r3`)
  - Ký tự ẩn Zero-Width (`\u200B`)
* **Mục tiêu**: Bẻ gãy logic nghiệp vụ ngay lập tức *(Goal Hijacking)*.

### [KHUNG PHẢI: KÊNH 2]
* **Tiêu đề khối**: `INDIRECT INGRESS (PDF / EMAIL / RAG)`
* **Cơ chế kích hoạt**:
  - Giấu mã độc tàng hình trong file văn bản
  - Ứng dụng đọc file nạp vào bộ nhớ RAG
  - Lệnh độc kích hoạt ngầm từ bên trong
* **Mục tiêu**: Chiếm quyền công cụ tự động *(Tool / Agent Hijacking)*.

### [THANH CHỐT Ở ĐÁY SLIDE (TAG)]
```text
🛡️ 5D Threat Analysis: Chuẩn hóa theo NIST AI 100-2e2025 & MITRE ATLAS
```

---

# 🖼️ SLIDE 2: ĐỐI CHUẨN 2 MÔ HÌNH & KIẾN TRÚC PHÂN TẦNG ĐỀ XUẤT

### [TIÊU ĐỀ SLIDE]
```text
MODEL COMPARISON & TWO-TIER GUARDRAIL ARCHITECTURE
```

### [BẢNG SO SÁNH 2 MÔ HÌNH THAM KHẢO (NỬA TRÊN)]

| Tiêu chí | ⚡ Hướng 1: Classical ML (TF-IDF + Linear) | 🧠 Hướng 2: Deep Transformer (DeBERTa-v3) |
| :--- | :--- | :--- |
| **Cơ chế** | Túi từ n-grams + Ký tự `char_wb` | Chú ý phân tách (Disentangled Attention) |
| **Ưu điểm** | **Siêu nhanh (~2.8ms CPU)**, nhẹ (~25MB RAM) | **Hiểu ngữ nghĩa sâu ($F_1 > 0.97$)**, bắt đòn phức tạp |
| **Điểm nghẽn** | **Mù ngữ nghĩa sâu** trước đòn hoán dụ | **Nặng (~500MB)**, độ trễ CPU cao (~42.5ms) |

---

### [GIẢI PHÁP ĐỀ XUẤT CỦA PI-GUARD (NỬA DƯỚI)]
*Vẽ sơ đồ dòng chảy 2 tầng hoặc đặt 2 thẻ bo góc:*

* **TẦNG 1 (Lọc Nhanh - Fast Scrubber)**:  
  `Khử khoảng trắng + NFKC + TF-IDF nhẹ` $\longrightarrow$ Giải quyết **82.6%** truy vấn rõ ràng trong **$< 0.5\text{ms}$**!
* **TẦNG 2 (Phân Tích Sâu - Deep Arbiter)**:  
  `DeBERTa-v3 lượng hóa INT8` $\longrightarrow$ Chỉ xử lý **17.4%** câu mờ ám khó phân định.

### [THANH CHỐT CHỈ SỐ Ở ĐÁY SLIDE]
```text
🚀 Kết Quả Đạt Được: Độ trễ P95 < 20ms | F1 > 98% | Tiết kiệm 80% phần cứng
```
