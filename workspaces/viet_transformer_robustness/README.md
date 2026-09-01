# Workspace Cá Nhân — Phạm Minh Hoàng Việt
## Trọng tâm: Transformer Fine-Tuning, ONNX INT8 & Robustness Testing

Chào Việt! Đây là không gian làm việc nháp (Sandbox) riêng của bạn.

### 📌 Nhiệm vụ chính:
1. Fine-tuning mô hình Transformer `microsoft/deberta-v3-base` (Sequence Classification 3 classes: Benign, Injection, Jailbreak).
2. Lượng hóa động *Post-Training Dynamic INT8 Quantization* sang ONNX Runtime (`onnxruntime.quantization`).
3. Kiểm thử độ bền đối kháng: Sinh nhiễu Leetspeak, Spacing, Heuristic Base64 Decoder và đo đạc độ suy giảm $\Delta F_1 < 5\%$.
4. Soạn thảo **Chapter 4: Experimental and Results (Report No.4)** và chuẩn bị **Báo Cáo Hội Đồng 1**.

### 📂 Bạn có thể để file tại đây:
- `scratch_quantize.py`: Thử nghiệm script nén ONNX INT8 và đo latency P95 trên CPU.
- `scratch_evasion_test.py`: Thử nghiệm các payload Base64/Cipher độc hại.
- Khi code đã chạy ổn định $\rightarrow$ Chuyển vào [`src/models/classifier.py`](file:///d:/Work/Do-an/src/models/classifier.py), [`src/preprocessing/obfuscation.py`](file:///d:/Work/Do-an/src/preprocessing/obfuscation.py) và [`notebooks/03_transformer_training.ipynb`](file:///d:/Work/Do-an/notebooks/03_transformer_training.ipynb).
