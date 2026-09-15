# **CHUYÊN ĐỀ 3: KHẢO SÁT BASELINE NHÚNG CÂU KẾT HỢP HỌC MÁY CỔ ĐIỂN (AYUB & MAJUMDAR, 2024)**
## ĐỀ TÀI: A MACHINE-LEARNING GUARDRAIL FOR DETECTING PROMPT INJECTION AND JAILBREAK ATTACKS ON LLM APPLICATIONS (PI-GUARD)
**Tác giả**: Nguyễn Văn Trường (Leader — MSSV: `SE182034`) | **Workspace**: `workspaces/truongnv/`  
**Cổng điều phối chuyên đề Task 3**: [`workspaces/truongnv/reports/tasks_for_meeting_5/task_3_reproducibility/README.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/tasks_for_meeting_5/task_3_reproducibility/README.md)

---

> [!TIP]
> ### 📌 TÓM TẮT ĐIỀU HÀNH CHUYÊN ĐỀ 3 (EXECUTIVE SUMMARY)
> - **Vai trò trong đồ án**: Là công trình học thuật xuất bản chính thức có đầy đủ Bộ ba [Paper + Code + Dataset] nghiên cứu về việc kết hợp **Vector nhúng câu ngữ nghĩa (Sentence Embeddings qua `all-MiniLM-L6-v2`) với các thuật toán học máy cổ điển (Random Forest, Logistic Regression, XGBoost)**.
> - **Trạng thái bộ ba**: <mark>**ĐẦY ĐỦ 100% CÔNG KHAI**</mark> gồm Paper (CAMLIS 2024 / arXiv:2410.22284), Mã nguồn trên GitHub (`AhsanAyub/malicious-prompt-detection`), và 467k mẫu dữ liệu trên Hugging Face.
> - **Ý nghĩa khoa học**: Làm mô hình đối chuẩn bổ trợ cấp cao cho Baseline TF-IDF, chứng minh rằng không cần fine-tune toàn bộ mạng Transformer nặng nề vẫn có thể đạt hiệu năng phân loại cao trên các prompt thông thường.

---

## 1. THÔNG TIN XUẤT BẢN & LIÊN KẾT BÀI BÁO (PAPER)

```text
Tiêu đề chính thức : "Embedding-based classifiers can detect prompt injection attacks"
Tác giả            : Md. Ahsan Ayub & Subhabrata Majumdar
Nơi xuất bản       : Hội nghị CAMLIS 2024 (Conference on Applied Machine Learning in Information Security)
                     Arlington, VA, USA, Tháng 10/2024
Định danh arXiv    : arXiv:2410.22284
Liên kết bài báo   : https://arxiv.org/abs/2410.22284 | PDF: https://arxiv.org/pdf/2410.22284
```

---

## 2. CẤU TRÚC KHO MÃ NGUỒN CHÍNH THỨC (CODE REPOSITORY)

Được công bố chính thức tại Footnote 1 (Trang 2) của bài báo:
- **Địa chỉ GitHub**: [`https://github.com/AhsanAyub/malicious-prompt-detection`](https://github.com/AhsanAyub/malicious-prompt-detection) (`HTTP 200 OK`)
- **Các file mã nguồn cốt lõi**:
  ```text
  AhsanAyub/malicious-prompt-detection/
  ├── binary_classification.py  # Script huấn luyện & đo đạc Logistic Regression, Random Forest, XGBoost
  ├── embedding.py              # Pipeline trích xuất vector nhúng từ văn bản prompt
  ├── visualization.py          # Vẽ biểu đồ ma trận nhầm lẫn và đường cong ROC
  ├── requirements.txt          # Danh mục thư viện phụ thuộc
  └── dataset/                  # Hướng dẫn và liên kết tải tập dữ liệu 467k mẫu
  ```

---

## 3. TẬP DỮ LIỆU CHUẨN CÔNG KHAI CỦA BÀI BÁO (DATASET)

Tác giả đã phát hành tập dữ liệu được làm sạch quy mô lớn trên Hugging Face:
- **Địa chỉ lưu trữ**: [`https://huggingface.co/datasets/ahsanayub/malicious-prompts`](https://huggingface.co/datasets/ahsanayub/malicious-prompts) (`HTTP 200 OK`)
- **Quy mô tập dữ liệu**:
  - Tổng số mẫu duy nhất: **467,057 prompts** (sau khi khử trùng lặp từ 553,185 mẫu thu thập).
  - Phân phối nhãn: **109,934 mẫu Malicious (23.54%)** và **357,123 mẫu Benign (76.46%)**.
- **Nguồn gốc thu thập từ 6 tập dữ liệu an toàn mở**:
  1. `imoxto: Prompt Injection cleaned dataset` (535,105 câu)
  2. `reshabhs: SPML Chatbot Prompt Injection` (16,012 câu)
  3. `Harelix: Prompt Injection Mixed Techniques` (1,174 câu)
  4. `JasperLS: Prompt Injections` (662 câu)
  5. `fka: Awesome ChatGPT Prompts` (153 câu)
  6. `rubend18: ChatGPT Jailbreak Prompts` (79 câu)
- **Cấu trúc trường dữ liệu**: `ID`, `Source`, `Text`, `Label` (0: Benign, 1: Malicious).

---

## 4. PHƯƠNG PHÁP LUẬN, THUẬT TOÁN & SIÊU THAM SỐ (HYPERPARAMETERS)

### 4.1. Quy trình xử lý 2 giai đoạn (Two-Stage Pipeline)
$$\text{Prompt Thô } x \xrightarrow{\text{Sentence Embedding}} \mathbf{e} \in \mathbb{R}^d \xrightarrow{\text{Classical ML}} \hat{y} \in \{0, 1\}$$

- **Mô hình trích xuất vector nhúng (Embedding Models)**:
  1. `sentence-transformers/all-MiniLM-L6-v2` ($d = 384$ chiều) — **Mô hình mã nguồn mở chạy cực nhanh trên CPU, hoàn toàn miễn phí**.
  2. `thenlper/gte-large` ($d = 1024$ chiều).
  3. OpenAI `text-embedding-3-small` ($d = 1536$ chiều).

### 4.2. Các bộ phân loại và siêu tham số trong `binary_classification.py`
- **Logistic Regression**: `solver='lbfgs', max_iter=1000`.
- **Random Forest**: `n_estimators=100, criterion='gini', random_state=0`.
- **XGBoost**: `objective='binary:logistic', random_state=42`.

---

## 5. KẾT QUẢ THỰC NGHIỆM CÔNG BỐ TRONG BÀI BÁO (REPORTED RESULTS)

Trong Bảng kết quả (Table 2 & Table 3) của bài báo CAMLIS 2024, các tác giả công bố:

| Bộ Phân Loại | Embedding Model | Accuracy | Precision | Recall | F1-Score |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Random Forest** | `gte-large` ($d=1024$) | **99.4%** | 0.989 | 0.985 | **0.987** |
| **XGBoost** | `all-MiniLM-L6-v2` ($d=384$) | **99.2%** | 0.985 | 0.981 | **0.983** |
| **Logistic Regression** | `all-MiniLM-L6-v2` ($d=384$) | 98.6% | 0.978 | 0.970 | 0.974 |

> **Kết luận khoa học của tác giả**: Việc kết hợp Sentence Embeddings gọn nhẹ với các thuật toán học máy cổ điển (Random Forest/XGBoost) đạt hiệu năng tương đương hoặc vượt trội hơn việc fine-tune các mạng Transformer phân loại chuỗi nặng nề, đồng thời giảm thiểu đáng kể chi phí huấn luyện.

---

## 6. SO SÁNH VỚI BASELINE TF-IDF TRONG ĐỒ ÁN PI-GUARD

| Tiêu Chí | Baseline TF-IDF (Majhi et al. 2025 [[5]](#ref5)) | Baseline Embedding (Ayub & Majumdar 2024 [[1]](#ref1)) |
| :--- | :--- | :--- |
| **Không gian biểu diễn** | Vector thưa (Sparse Bag-of-Ngrams) 60,000 chiều | Vector dày (Dense Semantic Embedding) 384 chiều |
| **Chi phí trích xuất** | Cực thấp (đếm từ/ký tự tức thì trên CPU) | Cần chạy một mạng Transformer nhỏ (`MiniLM-L6-v2`) |
| **Độ trễ suy luận CPU** | **$< 1\text{ms}$** / prompt | **$\sim 8 - 12\text{ms}$** / prompt |
| **Năng lực kháng Leetspeak** | **Rất tốt** qua Character N-grams | Kém hơn (bộ tokenizer BPE dễ bị phân mảnh) |
| **Vai trò đối với PI-Guard** | **Mô hình Tầng 1 chính thức** trong kiến trúc Two-Tier Routing | **Mô hình đối chuẩn mở rộng** kiểm chứng tính tổng quát hóa |

---

## 7. TÀI LIỆU THAM KHẢO HỌC THUẬT (REFERENCES)

<a id="ref1"></a>
- **[[1]]** M. A. Ayub and S. Majumdar, "Embedding-based classifiers can detect prompt injection attacks," in *Proceedings of the Conference on Applied Machine Learning in Information Security (CAMLIS 2024)*, Arlington, VA, USA, Oct. 2024. [arXiv:2410.22284](https://arxiv.org/pdf/2410.22284).

<a id="ref5"></a>
- **[[5]]** V. Majhi, S. T. S. N. V. P. R. N., A. R. R., and S. S., "Do You Really Need a GPU to Guard Your LLM? CPU-Class Classifiers and Multi-Stage Pipelines for Safety Enforcement at Scale," *arXiv preprint arXiv:2512.19011*, Dec. 2025. [arXiv:2512.19011](https://arxiv.org/pdf/2512.19011).
