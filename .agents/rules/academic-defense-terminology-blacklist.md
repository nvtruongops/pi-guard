# 🛡️ Academic Defense Terminology & Overclaiming Blacklist/Whitelist Protocol

> **Quy định bất biến về thuật ngữ học thuật, tính khiêm tốn khoa học và phòng thủ phản biện trước Hội đồng Chấm Đồ án FPT University (IAP491)**  
> **Cơ chế thực thi**: Tự động kích hoạt qua Antigravity Rules Engine, được kiểm toán trước mỗi commit qua `python Final-Report/scripts/verify_resource_url.py --audit-attribution <file>` và `validate_local.py`.

---

## 📋 1. BẢNG TRA CỨU THUẬT NGỮ BLACKLIST / WHITELIST CHUẨN MỰC

| Phân Loại | 🚫 Thuật Ngữ Bị Cấm Tuyệt Đối (Blacklist) | ✅ Thuật Ngữ Học Thuật Bắt Buộc (Whitelist) | Luận Giải Kỹ Thuật & Phòng Thủ Hội Đồng |
| :--- | :--- | :--- | :--- |
| **Độ trễ & Hiệu năng** | • "Thời gian thực" / "Real-time"<br>• "Real-time detection"<br>• "Hệ thống thời gian thực" | • **"Độ trễ thấp" / "Low-Latency"**<br>• **"Độ trễ suy luận (Inference Latency)"**<br>• **"Inline Guardrail Proxy"**<br>• **"Thời gian đáp ứng nhanh (P95 < 30ms)"** | Trong Khoa học Máy tính, *"Real-time"* chỉ các hệ thống nhúng có cam kết thời gian ngặt nghèo cấp microsecond (Zero Jitter). Một HTTP Guardrail Proxy không thể cam kết hard real-time; dùng từ này sẽ bị Hội đồng bắt lỗi nặng. |
| **Bản chất Hệ thống & Phạm vi** | • "Hệ thống Production thương mại"<br>• "Production-ready enterprise system"<br>• "Kiến trúc cấp doanh nghiệp"<br>• "Commercial SaaS guardrail" | • **"Nguyên Mẫu Thực Nghiệm Học Thuật (Academic Proof-of-Concept Prototype)"**<br>• **"Môi Trường Đo Đạc Độ Trễ (Inference Latency Testbed)"**<br>• **"Plug-and-Play Guardrail Middleware"** | PI-Guard là Khóa luận Tốt nghiệp Nghiên cứu (**IAP491 Research Thesis**), không phải sản phẩm Kỹ thuật Phần mềm thương mại. Khẳng định "Production" sẽ bị đòi hỏi OAuth2, RBAC, billing, multi-tenancy và load test 100k RPS. |
| **Cam kết An ninh** | • "Bảo vệ 100% tuyệt đối"<br>• "Chống hack hoàn toàn"<br>• "Unbreakable defense"<br>• "Silver bullet solution" | • **"Giảm thiểu rủi ro thực nghiệm (Empirical Risk Mitigation)"**<br>• **"Phòng thủ theo chiều sâu (Defense-in-Depth)"**<br>• **"Độ chính xác cao ($F_1 \ge 0.95$, $\text{FPR} < 1.5\%$)"**<br>• **"Khả năng chống chịu đối kháng (Adversarial Robustness)"** | Không gian token là không gian phẳng ($X = S \mathbin{\Vert} U$); về mặt toán học không thể miễn nhiễm tuyệt đối. Tuyên bố an toàn 100% là phi khoa học. |
| **Phần cứng & Triển khai** | • "Bắt buộc hạ tầng GPU đắt tiền"<br>• "Hệ thống đòi hỏi cụm máy chủ lớn" | • **"Triển khai tối ưu trên CPU tiêu chuẩn (Zero-GPU Commodity CPU)"**<br>• **"Lượng hóa động sau huấn luyện (ONNX INT8 Quantization)"** | Bản đăng ký đề tài ghi rõ triển khai trên CPU đa nhân thông thường, không phát sinh chi phí mua sắm GPU máy chủ cho nhà trường. |
| **Can thiệp Mô hình** | • "Can thiệp trọng số nội tại của GPT-4"<br>• "Retrain lại downstream LLM"<br>• "Sửa đổi KV-cache bộ nhớ" | • **"Lớp lọc đầu vào độc lập (Model-Agnostic External Input Guardrail)"**<br>• **"Kiểm tra mức văn bản (Prompt-Level Inspection)"**<br>• **"Tương thích hộp đen (Black-Box LLM Compatibility)"** | PI-Guard hoạt động như một reverse proxy kiểm tra prompt mức văn bản. Việc can thiệp vào trọng số LLM thương mại hoặc KV-cache là phi thực tế và ngoài phạm vi đề tài. |
| **Khiêm Tốn Khoa Học & Đánh Giá Học Thuật** | • "Không lo ngại bất kỳ câu hỏi phản biện nào"<br>• "Độ chuẩn mực học thuật tối đa"<br>• "100% PASS cho toàn bộ tài liệu/học thuật"<br>• "Tài liệu hoàn hảo không tì vết" | • **"Đủ độ tin cậy làm nền tảng cho Chapter 2"**<br>• **"Các claim được phân tách rõ giữa literature evidence, PI-Guard design choice và project KPI"**<br>• **"Automated validation: 100% PASS; Literature verification: VERIFIED / REVIEWED"** | Trong nghiên cứu khoa học, không có kết quả hay tài liệu nào được tuyên bố "miễn nhiễm phản biện". Cần giữ thái độ khiêm tốn học thuật (Academic Humility) và phân tách rạch ròi giữa việc vượt qua kịch bản kiểm tra phần mềm tự động (Automated Validation) với tính đúng đắn của luận điểm khoa học. |

---

## 🔒 2. QUY TẮC KHẲNG ĐỊNH SỐ LIỆU & NGUỒN GỐC (PROVENANCE & METRIC RIGOR)

1. **Phân biệt Automated Validation vs. Literature Verification**:
   - `validate_local.py = PASS` $\rightarrow$ Chỉ xác nhận kịch bản kiểm thử mã nguồn, ranh giới thư mục và JSON manifest đạt chuẩn kỹ thuật.
   - Luận điểm khoa học, trích dẫn, paraphrase và metadata $\rightarrow$ Phải dùng nhãn **`VERIFIED / REVIEWED`**, không dùng "100% PASS" để tránh tuyệt đối hóa.
2. **Quy tắc Nguồn Gốc Số Liệu (Metric Provenance)**:
   - Không được trình bày KPI, benchmark result, latency, FPR, F1 hoặc performance measurement của PI-Guard như kết quả thực nghiệm của tài liệu tham chiếu, trừ khi tài liệu đó thực sự báo cáo cùng phép đo và cùng điều kiện.
3. **Quy tắc Kiểm Định Tập Dữ Liệu (Dataset Rigor)**:
   - Phân biệt rõ ràng giữa kích thước toàn bộ tập dữ liệu (Total Samples / Corpus Size, ví dụ 15,140 prompts) với số lượng mẫu tấn công thực tế (Positive Attack Samples, ví dụ 1,405 jailbreak prompts).
