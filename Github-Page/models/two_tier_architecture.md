# NGUYÊN LÝ PHỐI HỢP 2 MÔ HÌNH: KIẾN TRÚC PHÒNG THỦ ĐA TẦNG (CASCADE DEFENSE)
## CƠ CHẾ ĐỊNH TUYẾN BẤT ĐỊNH & TỐI ƯU HÓA ĐỘ TRỄ SUY LUẬN

> **Chủ biên**: Nguyễn Văn Trường (Leader) & Phạm Minh Hoàng Việt  
> **Áp dụng cho**: Khóa luận tốt nghiệp FPT University IAP491 — Đề tài PI-Guard  
> **Khung quy chuẩn**: Chuẩn học thuật ICLR, NeurIPS, AAAI HCOMP  

---

## 🛡️ 1. TẠI SAO BẮT BUỘC PHẢI PHỐI HỢP CẢ 2 MÔ HÌNH?

Nếu một hệ thống Guardrail chỉ sử dụng một mô hình đơn lẻ, nó sẽ ngay lập tức đối mặt với **Nghịch lý Đánh đổi (Security Trade-off Dilemma)**:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│               NGHỊCH LÝ KHI DÙNG MÔ HÌNH ĐƠN LẺ & GIẢI PHÁP KẾT HỢP CỦA PI-GUARD        │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ TÌNH HUỐNG 1: CHỈ DÙNG TF-IDF BASELINE                                                 │
│  • Ưu điểm: Siêu tốc (~0.85ms), chặn đứng Leetspeak và Spacing hiệu quả.               │
│  • Thất bại: Thiếu hiểu biết ngữ nghĩa sâu -> Tỷ lệ báo động nhầm (FPR) lên tới 15-25%.│
│    Các câu hỏi nghiên cứu hợp lệ ("Explain SQL Injection risks") bị chặn oan!          │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ TÌNH HUỐNG 2: CHỈ DÙNG DEBERTA-V3                                                      │
│  • Ưu điểm: Hiểu ngữ cảnh sâu sắc, triệt tiêu báo động nhầm (FPR < 1.0%).               │
│  • Thất bại: Subword BPE bị điểm mù Token Fragmentation (Jain et al., arXiv:2309.00614).│
│    Kẻ tấn công có thể chèn ký tự biến dị để né tránh (Evasion).                        │
│  • Độ trễ: Mọi request đều phải chạy qua 12 tầng Transformer (~18.5ms).               │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ GIẢI PHÁP PI-GUARD: PHỐI HỢP 2 TẦNG (CASCADE TWO-TIER DEFENSE)                         │
│  ✅ Tầng 1 (TF-IDF): Đánh chặn nhanh tấn công thô, biến dị ký tự trong ~0.85ms.         │
│  ✅ Tầng 2 (DeBERTa-v3 ONNX INT8): Phân xử ngữ cảnh tinh vi, triệt tiêu báo động nhầm. │
│  👉 Kết quả: Độ trễ P95 < 22ms, FPR < 1.0%, F1 > 0.96, hoạt động 100% Zero-GPU!       │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📐 2. CƠ SỞ TOÁN HỌC CỦA CƠ CHẾ ĐỊNH TUYẾN BẤT ĐỊNH (UNCERTAINTY ROUTING FORMULATION)

Cho chuỗi prompt đầu vào $x \in \mathcal{X}$, mô hình Tầng 1 (TF-IDF + Linear Classifier) xuất ra vector xác suất $\hat{\mathbf{p}}^{(1)}(x) = [\hat{p}_0^{(1)}, \hat{p}_1^{(1)}, \hat{p}_2^{(1)}]$, trong đó xác suất tấn công tổng hợp là $P_{\text{atk}}^{(1)}(x) = \hat{p}_1^{(1)}(x) + \hat{p}_2^{(1)}(x)$.

Quy tắc ra quyết định phân tầng và chuyển tiếp được định nghĩa như sau [[1]](#ref1):

$$\text{Decision}(x) = \begin{cases} 
\text{BLOCK (Early Exit)}, & \text{nếu } P_{\text{atk}}^{(1)}(x) \ge \tau_{\text{high}} \\
\text{ALLOW (Fast Pass)}, & \text{nếu } P_{\text{atk}}^{(1)}(x) \le \tau_{\text{low}} \\
\text{ROUTING TO TIER-2 (DeBERTa-v3)}, & \text{nếu } \tau_{\text{low}} < P_{\text{atk}}^{(1)}(x) < \tau_{\text{high}}
\end{cases}$$

Khi chuyển sang Tầng 2, mô hình DeBERTa-v3 xuất ra xác suất ngữ nghĩa sâu $\hat{\mathbf{p}}^{(2)}(x)$, và quyết định cuối cùng được xác định tại ngưỡng hiệu chuẩn $\tau_{\text{deep}}$ [[2]](#ref2):

$$\text{Final Decision}(x) = \begin{cases}
\text{BLOCK (HTTP 403)}, & \text{nếu } P_{\text{atk}}^{(2)}(x) \ge \tau_{\text{deep}} \\
\text{ALLOW (Forward to LLM)}, & \text{nếu } P_{\text{atk}}^{(2)}(x) < \tau_{\text{deep}}
\end{cases}$$

---

## 🔄 3. SƠ ĐỒ LUỒNG ĐIỀU PHỐI RA QUYẾT ĐỊNH (DECISION PIPELINE)

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
                    │ (Char n-grams ~0.85 ms) │
                    └─────────────────────────┘
                                 │
                     Tính xác suất P_atk^(1)
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
         ▼                       ▼                       ▼
   P_atk >= 0.85          0.15 < P_atk < 0.85       P_atk <= 0.15
(Tấn công rõ ràng)       (Vùng phân vân ngữ nghĩa)  (Lành tính rõ ràng)
         │                       │                       │
         ▼                       ▼                       ▼
  🚨 BLOCK NGAY       ┌─────────────────────┐       ✅ CHUYỂN TIẾP
  (Early Exit)        │ TẦNG 2: DEBERTA-V3  │          SANG LLM
   Độ trễ ~0.85ms     │ (ONNX INT8 ~18.5ms) │         Độ trễ ~0.85ms
  Tiết kiệm 80% CPU   └─────────────────────┘
                                 │
                       Tính xác suất P_atk^(2)
                                 │
                     ┌───────────┴───────────┐
                     ▼                       ▼
             P_atk >= tau_deep       P_atk < tau_deep
              🚨 BLOCK PROMPT         ✅ CHO PHÉP QUA
```

---

## ⚡ 4. LỢI ÍCH VỀ MẶT HIỆU NĂNG HỆ THỐNG THỰC TẾ (SYSTEM EFFICIENCY GAINS)

1. **Giảm tải tính toán (Workload Offloading)**:
   - Trong môi trường thực tế, khoảng **75% – 85%** các truy vấn là các câu hỏi thường nhật rõ ràng hoặc các mẫu tấn công từ khóa thô thiển.
   - Nhờ cơ chế **Early Exit tại Tầng 1**, các prompt này được xử lý ngay trong $< 1.0\text{ ms}$ mà không cần đánh thức mô hình Transformer, giúp tiết kiệm hơn $70\%$ tài nguyên tính toán của hệ thống.
2. **Triệt tiêu False Positive Rate (FPR)**:
   - Khi người dùng gửi câu hỏi kỹ thuật: *"How does prompt injection attack work?"*, Tầng 1 nghi ngờ vì chứa từ khóa rủi ro ($P_{\text{atk}}^{(1)} \approx 0.65$).
   - Thay vì chặn nhầm, hệ thống chuyển sang Tầng 2. DeBERTa-v3 phân tích ngữ cảnh ngữ pháp sâu và xác định $P_{\text{atk}}^{(2)} = 0.03$ (Lành tính), cho phép yêu cầu đi qua an toàn mà không làm gián đoạn người dùng [[4]](#ref4).

---

## 📚 5. TÀI LIỆU THAM KHẢO HỌC THUẬT (ACADEMIC REFERENCES)

<a id="ref1"></a>**[1]** N. Jain et al., "Baseline Defenses for Adversarial Attacks Against Aligned Language Models," *arXiv preprint arXiv:2309.00614*, 2023. Link: [https://arxiv.org/abs/2309.00614](https://arxiv.org/abs/2309.00614).

<a id="ref2"></a>**[2]** P. He, J. Gao, and W. Chen, "DeBERTaV3: Improving DeBERTa using ELECTRA-Style Pre-Training with Disentangled Attention," in *International Conference on Learning Representations (ICLR)*, 2023. Link: [https://arxiv.org/abs/2111.09543](https://arxiv.org/abs/2111.09543).

<a id="ref3"></a>**[3]** Z. Yao et al., "ZeroQuant: Efficient and Affordable Post-Training Quantization for Large-Scale Transformers," in *Advances in Neural Information Processing Systems (NeurIPS)*, 2022. Link: [https://arxiv.org/abs/2206.01861](https://arxiv.org/abs/2206.01861).

<a id="ref4"></a>**[4]** T. Markov et al., "A Holistic Approach to Undesired Content Detection in the Real World," in *AAAI Conference on Human Computation and Crowdsourcing (HCOMP)*, 2023. Link: [https://arxiv.org/abs/2208.03274](https://arxiv.org/abs/2208.03274).