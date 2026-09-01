# THƯ MỤC BỘ KIỂM THỬ TỰ ĐỘNG (AUTOMATED TEST SUITE)
## 🧪 PI-Guard Unit, Integration & Adversarial Robustness Tests

> [!IMPORTANT]
> **QUY TẮC CHẠY KIỂM THỬ (TESTING RULES)**:
> 1. Mọi Pull Request trước khi được duyệt merge vào `src/` phải vượt qua 100% các bài test tự động:
>    ```powershell
>    pytest tests/
>    ```
> 2. Các test suite đối kháng (Adversarial Tests) dùng để đo khả năng phát hiện khi hacker tấn công mã hóa Base64, Leetspeak và chèn khoảng trắng.

---

### 📂 CẤU TRÚC:

```
tests/
├── unit/                          # Kiểm thử đơn vị các hàm tiền xử lý, bóc tách Base64, Tokenizer
├── integration/                   # Kiểm thử tích hợp luồng: Request -> Guardrail -> LLM Proxy -> Response
└── adversarial/                   # Bộ 400+ payload tấn công đối kháng để đo Robustness Score
```
