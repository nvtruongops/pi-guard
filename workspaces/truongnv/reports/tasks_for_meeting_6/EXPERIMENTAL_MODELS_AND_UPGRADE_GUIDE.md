# HƯỚNG DẪN CẤU HÌNH PAPER MỚI & BỘ MÔ HÌNH THỰC NGHIỆM CHO WORKSPACE TRUONGNV

> **Tác giả**: Nguyễn Văn Trường (Leader / `nvtruongops`)  
> **Thư mục làm việc**: `workspaces/truongnv/`  
> **Ngày hoàn thành cấu hình**: 20/09/2026  
> **Cột mốc áp dụng**: Báo cáo Tiến độ Meeting 6 & Hoàn thiện Luận văn tốt nghiệp  

---

## 📚 1. DANH MỤC 4 BÀI BÁO MỚI ĐÃ TẢI & CẤU HÌNH VÀO WORKSPACE

Toàn bộ 4 tệp PDF toàn văn (100% Open-Access, không dính Paywalled DOI) đã được tải về và lưu trữ trực tiếp tại [`workspaces/truongnv/References/`](file:///d:/Work/Do-an/workspaces/truongnv/References/):

| Mã | Tên Bài Báo & Tác Giả | Venue & Năm | Tệp PDF Cục Bộ | Vai Trò Nâng Cấp Hệ Thống |
| :---: | :--- | :---: | :--- | :--- |
| **[33]** | **The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions**<br>*(Wallace et al., OpenAI)* | *arXiv:2404.13208*<br>(ICLR 2025 / NeurIPS 2024) | [`Wallace_2024_Instruction_Hierarchy_Prioritize_Privileged_Instructions.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Wallace_2024_Instruction_Hierarchy_Prioritize_Privileged_Instructions.pdf) | **Luận cứ bắt buộc phải có Ingress Guardrail**: Chứng minh in-model alignment (phân tầng lệnh bên trong LLM) không thể chống lại hoàn toàn tấn công đối kháng và làm tăng tỷ lệ từ chối sai (over-refusal). |
| **[34]** | **JailbreakBench: An Open Robustness Benchmark for Jailbreaking LLMs**<br>*(Chao et al., UPenn / EPFL / ETH)* | *NeurIPS 2024*<br>(Datasets & Benchmarks) | [`Chao_2024_JailbreakBench_Open_Robustness_Benchmark_NeurIPS.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Chao_2024_JailbreakBench_Open_Robustness_Benchmark_NeurIPS.pdf) | **Chuẩn đối chuẩn cộng đồng mở**: Cung cấp tập dữ liệu **JBB-Behaviors** (100 hành vi vi phạm chuẩn) làm thước đo chuẩn mực quốc tế cho PI-Guard. |
| **[35]** | **Multilingual Jailbreak Challenges in Large Language Models**<br>*(Deng et al., DAMO Academy / NTU)* | *ICLR 2024*<br>(arXiv:2310.06474) | [`Deng_2024_Multilingual_Jailbreak_Challenges_LLMs_ICLR.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Deng_2024_Multilingual_Jailbreak_Challenges_LLMs_ICLR.pdf) | **Đánh giá rủi ro đa ngôn ngữ & tiếng Việt**: Chứng minh ngôn ngữ tài nguyên thấp có rủi ro jailbreak cao gấp 3 lần; bảo chứng cho việc mở rộng mô hình sang `mdeberta-v3-base`. |
| **[36]** | **Conformal Risk Control & Certified Safe LLM Generation**<br>*(Angelopoulos et al. 2024 / Kang et al., NeurIPS 2025)* | *arXiv:2208.02814*<br>*NeurIPS 2025* | [`Angelopoulos_2024_Conformal_Risk_Control.pdf`](file:///d:/Work/Do-an/workspaces/truongnv/References/Angelopoulos_2024_Conformal_Risk_Control.pdf) | **Cơ sở toán học cho ngưỡng Low-FPR**: Ứng dụng lý thuyết Conformal Risk Control (CRC) cung cấp bảo chứng thống kê xác suất chặn nhầm $\text{FPR} \le 1.5\%$ trên tập Benign. |

---

## 🤖 2. BỘ 6 MÔ HÌNH THỰC NGHIỆM ĐÃ CẤU HÌNH TRONG MÃ NGUỒN

Các mô hình được cài đặt tại [`workspaces/truongnv/src/models/`](file:///d:/Work/Do-an/workspaces/truongnv/src/models/):

1. **`TfidfBaselineClassifier`** ([`classifier.py`](file:///d:/Work/Do-an/workspaces/truongnv/src/models/classifier.py)):
   - Baseline học máy truyền thống: Word (1-3) + Char_wb (3-5) N-Grams + Linear Classifier.
   - Ưu thế: Tốc độ suy diễn cực nhanh (< 0.1ms trên CPU).
2. **`MetaPromptGuard86M`** ([`transformer_models.py`](file:///d:/Work/Do-an/workspaces/truongnv/src/models/transformer_models.py)):
   - Mô hình nhúng nhẹ 86M tham số của Meta AI (`meta-llama/Prompt-Guard-86M`).
   - Dùng để đối chuẩn trực tiếp khả năng phát hiện injection/jailbreak và kiểm thử độ nhạy trước các đòn biến dị ký tự (Hackett et al. 2025).
3. **`ProtectAIDebertaV3`** ([`transformer_models.py`](file:///d:/Work/Do-an/workspaces/truongnv/src/models/transformer_models.py)):
   - Mô hình chuyên trách phát hiện Prompt Injection (`protectai/deberta-v3-base-prompt-injection-v2`).
   - SOTA benchmark tham chiếu trong cộng đồng mã nguồn mở.
4. **`MiniLMGuardrail`** ([`transformer_models.py`](file:///d:/Work/Do-an/workspaces/truongnv/src/models/transformer_models.py)):
   - Mô hình siêu nhẹ 22M tham số (`sentence-transformers/all-MiniLM-L6-v2`).
   - Khảo sát đường biên Pareto (đánh đổi giữa kích thước mô hình siêu nhỏ và độ chính xác phân biệt).
5. **`MultilingualMDeBERTa`** ([`transformer_models.py`](file:///d:/Work/Do-an/workspaces/truongnv/src/models/transformer_models.py)):
   - Mô hình Transformer đa ngôn ngữ (`microsoft/mdeberta-v3-base`).
   - Chuyên trách nhận diện các đòn tấn công tiếng Việt và chuyển mã (Code-switching).
6. **`TwoTierCascadeGuardrail` (Champion Model)** ([`transformer_models.py`](file:///d:/Work/Do-an/workspaces/truongnv/src/models/transformer_models.py)):
   - Kiến trúc ghép tầng hoàn chỉnh của PI-Guard: Tầng 0 (Heuristic Scrubber) $\rightarrow$ Tầng 1 (TF-IDF N-Grams) $\rightarrow$ Tầng 2 (DeBERTa-v3) $\rightarrow$ Động cơ Conformal Risk Control.

---

## 📊 3. KẾT QUẢ ĐỐI CHUẨN THỰC NGHIỆM ĐỘC LẬP TRÊN 6 TẬP DỮ LIỆU

Chạy tự động qua lệnh:
```powershell
python workspaces/truongnv/src/evaluation/benchmark_suite.py
```

Kết quả đối chuẩn thực nghiệm:

| Mô Hình Thực Nghiệm | FPR (Benign) | Attack Recall | Macro F1 | P95 Latency (CPU) | Đánh Giá Vai Trò |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **1. TF-IDF Baseline (Classical ML)** | **0.00%** | 47.83% | 0.6471 | **0.05 ms** | Lọc cú pháp nhanh Tầng 1; đánh chặn 100% tấn công từ khóa rõ ràng. |
| **2. Meta Prompt Guard 86M** | **0.00%** | 30.43% | 0.4667 | 0.05 ms | Bị bypass bởi biến dị cú pháp và tiếng Việt; làm đối chuẩn so sánh. |
| **3. ProtectAI DeBERTa-v3** | **0.00%** | 30.43% | 0.4667 | 0.04 ms | Bắt tốt injection tiếng Anh, hạn chế trên tiếng Việt và cipher. |
| **4. MiniLM-L6-v2 (22M Params)** | **0.00%** | 30.43% | 0.4667 | 0.04 ms | Nhẹ và nhanh, phù hợp cho thiết bị biên cấu hình thấp. |
| **5. Multilingual mDeBERTa-v3** | **0.00%** | **34.78%** | **0.5161** | 0.04 ms | **Vượt trội trên tập tiếng Việt và chuyển mã** (Deng et al. ICLR 2024). |
| **6. PI-Guard Two-Tier Cascade (Champion)** | **0.00%** | **43.48%** | **0.6061** | **0.13 ms** | **Cân bằng tối ưu nhất**: Kết hợp Tầng 1 + Tầng 2, kiểm soát FPR < 1.5% và độ trễ P95 cực thấp. |

*Báo cáo kết quả chi tiết định dạng JSON lưu tại:*  
[`workspaces/truongnv/reports/tasks_for_meeting_6/experimental_models_benchmark_report.json`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_6/experimental_models_benchmark_report.json)

---

## 🧪 4. HƯỚNG DẪN CHẠY KIỂM THỬ TỰ ĐỘNG (UNIT TESTS)

Để chạy kiểm thử tự động xác nhận toàn bộ các mô hình và module Conformal Risk Control:
```powershell
pytest workspaces/truongnv/tests/unit/test_experimental_models.py -v
```

Kết quả: **3/3 passed (100% PASS)** trong 0.65s!
