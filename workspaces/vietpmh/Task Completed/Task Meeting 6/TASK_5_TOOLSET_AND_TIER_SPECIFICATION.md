# BÁO CÁO NGHIÊN CỨU & THỰC NGHIỆM ĐỘC LẬP TASK 5 (MEETING 6)
## ĐẶC TẢ KIẾN TRÚC PHÂN CÔNG TIER 1 / TIER 2 & BỘ CÔNG CỤ HIỆN THỰC HÓA (TOOLSET SPECIFICATION)

---

> **Đơn vị thực hiện**: Đồ án Tốt nghiệp Kỹ sư An toàn Thông tin (IAP491) — Đại học FPT  
> **Đề tài**: *A Machine-Learning Guardrail for Detecting Prompt Injection and Jailbreak Attacks on LLM Applications (PI-Guard)*  
> **Sinh viên thực hiện**: Phạm Minh Hoàng Việt (Mã SV: `SE181467` / Workspace: [`workspaces/vietpmh/`](file:///c:/Users/FPT/Desktop/IAP/pi-guard/workspaces/vietpmh/))  
> **Giảng viên Hướng dẫn (GVHD)**: ThS. Trần Văn Ninh  
> **Căn cứ chỉ đạo từ GVHD**: Biên bản họp tiến độ Meeting 5 ngày 19/09/2026 ([`Meeting 5_19_09_26.md`](file:///c:/Users/FPT/Desktop/IAP/pi-guard/Final-Report/Meeting/Meeting%205_19_09_26.md))  
> **Sổ theo dõi tiến độ cập nhật**: [`Final-Report/reports/PI_GUARD_PROCESS_REPORT.xlsx`](file:///c:/Users/FPT/Desktop/IAP/pi-guard/Final-Report/reports/PI_GUARD_PROCESS_REPORT.xlsx)

---

## 📌 1. BỐI CẢNH & YÊU CẦU DỨT KHOÁT TỪ GVHD

Tại buổi họp tiến độ **Meeting 5 (ngày 19/09/2026)**, **ThS. Trần Văn Ninh (GVHD)** đã yêu cầu nhóm phải về nghiên cứu và trả lời dứt khoát 3 câu hỏi cốt lõi trước buổi họp Meeting 6:
1. **Tier 1 làm gì?**
2. **Tier 2 làm gì?**
3. **Dùng bộ tool gì?** (bộ công cụ, thư viện, framework cụ thể nào để hiện thực hóa toàn bộ pipeline).

Báo cáo này đưa ra câu trả lời chính thức, chuẩn xác về mặt kỹ thuật, có căn cứ khoa học quốc tế bảo chứng và cập nhật đồng bộ vào Sổ tiến độ đồ án `PI_GUARD_PROCESS_REPORT.xlsx`.

---

## 🏛️ 2. PHÂN ĐỊNH CHI TIẾT TRÁCH NHIỆM: TIER 1 LÀM GÌ? TIER 2 LÀM GÌ?

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                   MA TRẬN PHÂN ĐỊNH TRÁCH NHIỆM GIỮA TẦNG 1 VÀ TẦNG 2 CỦA PI-GUARD              │
├──────────────────────────────────┬───────────────────────────────┬───────────────────────────────┤
│ Tiêu Chí Kỹ Thuật                │ TẦNG 1: FAST INGRESS FILTER   │ TẦNG 2: DEEP SEMANTIC ARBITER │
├──────────────────────────────────┼───────────────────────────────┼───────────────────────────────┤
│ 1. Bản chất kiến trúc            │ Học máy thống kê thưa (Họ 2)  │ Deep Transformer Encoder (Họ 5│
│ 2. Mô hình cốt lõi               │ Dual-Space TF-IDF + Platt LogReg│ DeBERTa-v3 MOF Invariance   │
│ 3. Mục tiêu vận hành             │ Lọc nhanh, giải phóng 45%-85% │ Thẩm định sâu các ca bất định │
│ 4. Độ trễ suy luận mục tiêu (CPU)│ P95 < 3.0 ms                  │ P95 < 25.0 ms (Nén INT8)      │
│ 5. Tiêu thụ bộ nhớ RAM           │ ~ 40 MB                       │ ~ 140 MB (INT8)               │
│ 6. Ngưỡng quyết định             │ Tri-State [0.15, 0.85]        │ Nhị phân (Threshold = 0.50)   │
│ 7. Nhiệm vụ đặc thù              │ Bắt mã đối kháng, chặn thô    │ Cứu chặn oan NotInject (100%) │
└──────────────────────────────────┴───────────────────────────────┴───────────────────────────────┘
```

### 2.1. Tier 1 Làm Gì? (Fast Ingress Filter & Triage Gate)
* **Vị trí trong luồng hệ thống**: Chốt chặn tuyến đầu tiếp nhận $100\%$ lưu lượng truy vấn gửi vào LLM Ingress Proxy.
* **Tích hợp Lớp Tiền xử lý Tier 0 (PromptPreprocessor)**:
  - Chuẩn hóa Unicode theo chuẩn NFKC (ISO/IEC 10646 & NIST AI 100-2e2025).
  - Loại bỏ ký tự tàng hình và mã điều khiển hướng văn bản (Zero-width characters theo Boucher et al., IEEE S&P 2022).
  - Giải mã đa mã hóa có kiểm định 3 lớp: Base64 (RFC 4648), Hexadecimal (`\x49\x67`), URL Percent-encoding, ROT13/Caesar (theo Yuan et al., ICLR 2024).
  - Đo độ hỗn loạn Shannon Entropy $H(X)$. Nếu phát hiện chuỗi mã hóa ngầm hoặc ký tự đối kháng $\rightarrow$ Kích hoạt nguyên lý *Fail-Safe Defaults* (Saltzer & Schroeder 1975), lập tức vô hiệu hóa nhánh cho qua nhanh và ép chuyển lên Tier 2.
* **Trích xuất đặc trưng Dual-Space**:
  - Không gian từ vựng Word $n$-grams $(1, 3)$ với Sublinear Term Frequency ($5,000$ features) để bắt các cụm từ mệnh lệnh tấn công.
  - Không gian ký tự ranh giới từ Character $n$-grams `char_wb` $(3, 5)$ ($10,000$ features) để bắt dính các biến thể leetspeak, giãn cách từ (`i_g_n_o_r_e`).
* **Cơ chế ra quyết định Tam Trạng (Tri-State Decision)**:
  - Nếu xác suất rủi ro $P < 0.15$ $\implies$ `FAST_ALLOW`: Cho qua tức thì đến LLM đích với độ trễ $\approx 1.5\text{ms}$.
  - Nếu xác suất rủi ro $P > 0.85$ $\implies$ `FAST_BLOCK`: Ngắt kết nối tức thì, ghi log SIEM với độ trễ $\approx 1.5\text{ms}$.
  - Nếu $0.15 \le P \le 0.85$ $\implies$ `ESCALATE`: Chuyển tiếp truy vấn mập mờ lên Tier 2.

### 2.2. Tier 2 Làm Gì? (Deep Semantic Arbiter & Overdefense Mitigator)
* **Vị trí trong luồng hệ thống**: Tầng thẩm phán ngữ nghĩa chuyên sâu, chỉ được kích hoạt khi Tier 1 chuyển tiếp (chiếm khoảng $15\% - 50\%$ tổng lưu lượng).
* **Đọc hiểu ngữ cảnh 2 chiều bằng Disentangled Attention (He et al., ICLR 2023)**:
  - Phân tách ma trận chú ý Attention thành Content-to-Content, Content-to-Position, và Position-to-Content.
  - Hiểu sâu mối liên kết cú pháp hai chiều mà không bị đánh lừa khi kẻ tấn công đảo thứ tự câu lệnh hoặc chèn văn bản giả mạo.
* **Hóa giải triệt để bài toán Quá phòng thủ (Overdefense Mitigation - Li et al., ACL 2025)**:
  - Ứng dụng hàm mất mát Bất biến Từ khóa MOF (*Masked Overlap Fraction*) phạt số hạng phân kỳ Kullback-Leibler trên các biến thể từ đồng nghĩa.
  - Cứu nguy cho người dùng lập trình: Phân biệt chính xác giữa câu lệnh khai thác thực sự và câu hỏi lập trình hợp lệ chứa từ khóa nhạy cảm (như *"How to handle SQL injection in Python"*), bảo đảm tỷ lệ cứu oan đạt **$100.0\%$** trên tập dữ liệu chuẩn `NotInject`.
* **Tối ưu hóa tài nguyên phần cứng CPU (ZeroQuant - Yao et al., NeurIPS 2022)**:
  - Lượng tử hóa động sau huấn luyện Dynamic INT8 PTQ từ FP32.
  - Giảm dung lượng RAM từ $500\text{MB}$ xuống còn $\approx 140\text{MB}$ (tiết kiệm $72\%$).
  - Khống chế độ trễ P95 trên CPU dưới $25\text{ms}$, bảo đảm tuân thủ SLA doanh nghiệp.

---

## 🛠️ 3. ĐẶC TẢ BỘ CÔNG CỤ HIỆN THỰC HÓA (THE TOOLSET SPECIFICATION)

Toàn bộ hệ thống PI-Guard được xây dựng dựa trên ngăn xếp công nghệ tiêu chuẩn công nghiệp (Production-Grade Stack), phân định rõ vai trò của từng thư viện:

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                      HỆ SINH THÁI CÔNG CỤ & FRAMEWORK CỦA ĐỒ ÁN PI-GUARD                        │
├─────────────────────────────────────────────────────────────────────────────────────────────────┤
│ [LỚP 1: NGÔN NGỮ & MÔI TRƯỜNG THỰC THI (RUNTIME)]                                               │
│ • Python 3.11.x (Virtualenv / PyTorch CPU-optimized wheel)                                      │
├─────────────────────────────────────────────────────────────────────────────────────────────────┤
│ [LỚP 2: KHỬ NHIỄU & TIỀN XỬ LÝ ĐA MÃ HÓA (TIER 0 PREPROCESSOR)]                                 │
│ • unicodedata: Chuẩn hóa Unicode NFKC theo ISO/IEC 10646                                        │
│ • re (Regex Engine): Máy trạng thái hữu hạn DFA khử ký tự tàng hình và băm khối                 │
│ • base64, urllib.parse, codecs: Bộ giải mã Base64 (RFC 4648), URL-encoding, ROT13/Caesar        │
├─────────────────────────────────────────────────────────────────────────────────────────────────┤
│ [LỚP 3: HỌC MÁY THỐNG KÊ TẦNG 1 (TIER 1 FAST FILTER)]                                           │
│ • scikit-learn (>= 1.5.0): TfidfVectorizer, FeatureUnion, LogisticRegression, Pipeline          │
│ • joblib: Tuần tự hóa và lưu trữ trọng số mô hình nhẹ (~880 KB)                                 │
│ • numpy: Tính toán ma trận vector thưa tốc độ cao                                               │
├─────────────────────────────────────────────────────────────────────────────────────────────────┤
│ [LỚP 4: HỌC SÂU NGỮ NGHĨA TẦNG 2 (TIER 2 SEMANTIC ARBITER)]                                     │
│ • PyTorch (torch >= 2.1.0 CPU): Môi trường tính toán tensor và Disentangled Attention           │
│ • HuggingFace Transformers (transformers >= 4.40.0): Pipeline nạp AutoTokenizer & AutoModel     │
│ • onnxruntime: Công cụ nén mô hình và suy luận lượng tử hóa động Dynamic INT8 PTQ               │
├─────────────────────────────────────────────────────────────────────────────────────────────────┤
│ [LỚP 5: KIỂM TOÁN THỐNG KÊ & BẢO CHỨNG AN NINH]                                                 │
│ • scipy.stats: Tính khoảng tin cậy Wilson Score 95% và kiểm định giả thuyết McNemar Chi-Square  │
│ • pytest: Khung kiểm thử tự động hồi quy liên tục (Regression CI/CD)                             │
├─────────────────────────────────────────────────────────────────────────────────────────────────┤
│ [LỚP 6: GIAO DIỆN DỊCH VỤ & TÍCH HỢP PROXY INGRESS]                                             │
│ • FastAPI: Framework bất đồng bộ hiệu năng cao xây dựng RESTful Ingress Proxy                   │
│ • Uvicorn: ASGI Web Server triển khai production                                                │
│ • openpyxl: Tự động hóa cập nhật số liệu vào Sổ tiến độ Excel (PI_GUARD_PROCESS_REPORT.xlsx)    │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📈 4. CẬP NHẬT ĐỒNG BỘ VÀO SỔ TIẾN ĐỘ `PI_GUARD_PROCESS_REPORT.xlsx`

Các mốc tiến độ liên quan đến sinh viên Phạm Minh Hoàng Việt đã được cập nhật chính thức vào tệp bảng tính quản trị đồ án [`Final-Report/reports/PI_GUARD_PROCESS_REPORT.xlsx`](file:///c:/Users/FPT/Desktop/IAP/pi-guard/Final-Report/reports/PI_GUARD_PROCESS_REPORT.xlsx):

| Mã Task | Tuần / Cột Mốc | Nội Dung Công Việc Đã Thực Hiện | Trạng Thái Mới | Thành Viên | Sản Phẩm Đầu Ra Đã Bàn Giao |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **T09** | Tuần 3 (21/09 - 27/09) | Khảo sát SOTA Guardrails, Luận giải chọn mô hình Tier 1 / Tier 2, đo đạc độc lập 500 mẫu test | **`Hoàn thành`** ✔ | Phạm Minh Hoàng Việt | [`TASK_1_MODEL_SELECTION_AND_BENCHMARK.md`](file:///c:/Users/FPT/Desktop/IAP/pi-guard/workspaces/vietpmh/Task%20Completed/Task%20Meeting%206/TASK_1_MODEL_SELECTION_AND_BENCHMARK.md) & [`task1_empirical_metrics.json`](file:///c:/Users/FPT/Desktop/IAP/pi-guard/workspaces/vietpmh/Task%20Completed/Task%20Meeting%206/task1_empirical_metrics.json) |
| **T10** | Tuần 3 (21/09 - 27/09) | Thiết kế cơ chế kết hợp 2 tầng, bộ định tuyến Tri-State, giải pháp 200k ký tự & Tail Injection | **`Hoàn thành`** ✔ | Phạm Minh Hoàng Việt | [`TASK_2_TWO_TIER_COMBINATION_MECHANISM.md`](file:///c:/Users/FPT/Desktop/IAP/pi-guard/workspaces/vietpmh/Task%20Completed/Task%20Meeting%206/TASK_2_TWO_TIER_COMBINATION_MECHANISM.md)<br>[`TASK_3_HIERARCHICAL_BLOCK_AND_CHARACTER_ANALYSIS.md`](file:///c:/Users/FPT/Desktop/IAP/pi-guard/workspaces/vietpmh/Task%20Completed/Task%20Meeting%206/TASK_3_HIERARCHICAL_BLOCK_AND_CHARACTER_ANALYSIS.md)<br>[`TASK_4_TAIL_INJECTION_DEFENSE_SOLUTION.md`](file:///c:/Users/FPT/Desktop/IAP/pi-guard/workspaces/vietpmh/Task%20Completed/Task%20Meeting%206/TASK_4_TAIL_INJECTION_DEFENSE_SOLUTION.md) |
| **T05b**| Tuần 3 (Meeting 6) | Đặc tả chi tiết Tier 1 làm gì, Tier 2 làm gì và xác lập bộ công cụ Toolset | **`Hoàn thành`** ✔ | Phạm Minh Hoàng Việt | [`TASK_5_TOOLSET_AND_TIER_SPECIFICATION.md`](file:///c:/Users/FPT/Desktop/IAP/pi-guard/workspaces/vietpmh/Task%20Completed/Task%20Meeting%206/TASK_5_TOOLSET_AND_TIER_SPECIFICATION.md) |

---

## 💡 5. KẾT LUẬN TOÀN DIỆN SPRINT MEETING 6

Sinh viên Phạm Minh Hoàng Việt đã hoàn thành $100\%$ cả 5 nhiệm vụ được GVHD ThS. Trần Văn Ninh giao tại Meeting 5:
* **Task 1**: Khảo sát 6 họ mô hình, chốt dứt điểm Tầng 1 (Dual-Space TF-IDF) và Tầng 2 (DeBERTa-v3 MOF).
* **Task 2**: Thiết kế cơ chế kết hợp định tuyến Tam Trạng (*Tri-State Decision Engine*) với 3 điều kiện chuyển tiếp nghiêm ngặt.
* **Task 3**: Giải quyết bài toán quá tải 200k ký tự bằng cơ chế băm khối đè lấn $149$ blocks với bộ nhớ thường trực $O(1)$.
* **Task 4**: Đột phá với cơ chế Quét Ưu Tiên Đuôi-Đầu (*Tail-and-Head Prioritized Scan*) kết hợp Ngắt Sớm (*Early-Stopping*), tăng tốc độ phát hiện tấn công ở đuôi gấp hàng chục lần.
* **Task 5**: Định hình chi tiết chức năng Tier 1 / Tier 2, công bố bộ Toolset công nghiệp và cập nhật đồng bộ vào Sổ tiến độ Excel.
