# NGUYÊN LÝ PHỐI HỢP 2 MÔ HÌNH: KIẾN TRÚC PHÒNG THỦ ĐA TẦNG (CASCADE DEFENSE)

---

## 🛡️ 1. TẠI SAO BẮT BUỘC PHẢI PHỐI HỢP CẢ 2 MÔ HÌNH?

Nếu một hệ thống Guardrail chỉ sử dụng một mô hình đơn lẻ, nó sẽ ngay lập tức đối mặt với **Nghịch lý Đánh đổi (Security Trade-off Dilemma)**:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│               NGHỊCH LÝ KHI DÙNG MÔ HÌNH ĐƠN LẺ & GIẢI PHÁP KẾT HỢP CỦA PI-GUARD        │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ TÌNH HUỐNG 1: CHỈ DÙNG TF-IDF BASELINE                                                 │
│  • Ưu điểm: Siêu tốc (~3.2ms), chặn đứng Leetspeak và Spacing.                         │
│  • Thất bại: Thiếu hiểu biết ngữ nghĩa sâu -> Tỷ lệ báo động nhầm (FPR) lên tới 15-25%.│
│    Các câu hỏi nghiên cứu hợp lệ ("Explain SQL Injection risks") bị chặn oan!          │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ TÌNH HUỐNG 2: CHỈ DÙNG DEBERTA-V3                                                      │
│  • Ưu điểm: Hiểu ngữ cảnh sâu sắc, triệt tiêu báo động nhầm (FPR < 1.1%).               │
│  • Thất bại: Subword BPE bị điểm mù Token Fragmentation (Hackett et al., 2025).        │
│    Kẻ tấn công chỉ cần dùng Leetspeak ('1gn0r3') là có thể lẩn tránh (Evasion).        │
│  • Độ trễ: Mọi request đều phải chạy qua 12 tầng Transformer (~13ms).                 │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ GIẢI PHÁP PI-GUARD: PHỐI HỢP 2 TẦNG (CASCADE TWO-TIER DEFENSE)                         │
│  ✅ Tầng 1 (TF-IDF): Đánh chặn nhanh tấn công thô, biến dị ký tự trong ~3.2ms.         │
│  ✅ Tầng 2 (DeBERTa-v3 ONNX INT8): Phân xử ngữ cảnh tinh vi, triệt tiêu báo động nhầm. │
│  👉 Kết quả: Độ trễ P95 < 20ms, FPR < 1.1%, F1 > 0.98, hoạt động 100% Zero-GPU!       │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 2. SƠ ĐỒ LUỒNG ĐIỀU PHỐI RA QUYẾT ĐỊNH (DECISION PIPELINE)

```
                       [User Prompt Đầu Vào]
                                 │
                                 ▼
                     ┌───────────────────────┐
                     │ Tiền Xử Lý Chuẩn Hóa  │
                     │  (Unicode, Heuristic) │
                     └───────────────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │ TẦNG 1: TF-IDF BASELINE │
                    │ (Char n-grams ~3.2 ms)  │
                    └─────────────────────────┘
                                 │
                     Tính xác suất P_tfidf
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
         ▼                       ▼                       ▼
   P_tfidf > 0.85        0.15 <= P <= 0.85        P_tfidf < 0.15
(Tấn công rõ ràng)       (Ngưỡng phân vân)      (Lành tính rõ ràng)
         │                       │                       │
         ▼                       ▼                       ▼
  🚨 BLOCK NGAY       ┌─────────────────────┐       ✅ CHUYỂN TIẾP
  (Early Exit)        │ TẦNG 2: DEBERTA-V3  │          SANG LLM
   Độ trễ ~3ms        │  (ONNX INT8 ~12.8ms)│         Độ trễ ~3ms
  Tiết kiệm CPU       └─────────────────────┘
                                 │
                       Tính xác suất P_deberta
                                 │
                     ┌───────────┴───────────┐
                     ▼                       ▼
             P_deberta > 0.5         P_deberta <= 0.5
              🚨 BLOCK PROMPT         ✅ CHO PHÉP QUA
```

---

## ⚡ 3. LỢI ÍCH VỀ MẶT HIỆU NĂNG SẢN XUẤT (PRODUCTION GAINS)

1. **Giảm tải tính toán (Workload Offloading)**:
   - Trong môi trường thực tế, khoảng **40% – 60%** các cuộc tấn công tiêm nhiễm là các mẫu thô hoặc biến thể ký tự rõ ràng.
   - Nhờ cơ chế **Early Exit tại Tầng 1**, các prompt này bị chặn đứng ngay ở 3ms mà không cần đánh thức mô hình DeBERTa-v3, giúp tiết kiệm hơn 50% tài nguyên CPU của hệ thống.
2. **Triệt tiêu False Positive Rate (FPR)**:
   - Khi người dùng gửi câu hỏi kỹ thuật: *"How does prompt injection attack work?"*, Tầng 1 có thể nghi ngờ vì chứa từ khóa rủi ro ($P_{\text{tfidf}} \approx 0.65$).
   - Thay vì vội vàng chặn nhầm, hệ thống chuyển sang Tầng 2. DeBERTa-v3 phân tích mối quan hệ ngữ pháp (Query hỏi cách thức hoạt động chứ không phải câu lệnh ra lệnh) và kết luận $P_{\text{deberta}} = 0.04$ (Lành tính), cho phép yêu cầu đi qua an toàn!
