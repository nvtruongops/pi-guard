# TÀI LIỆU HỌC TẬP, BÀI BÁO GỐC & VIDEO: TF-IDF BASELINE

---

## 📄 1. CÁC BÀI BÁO KHOA HỌC GỐC (PEER-REVIEWED & LANDMARK PAPERS)

1. **Karen Spärck Jones (1972) — Nguồn Gốc Lịch Sử Của IDF**:
   - **Tên bài báo**: *"A statistical interpretation of term specificity and its application in retrieval"*.
   - **Tạp chí**: *Journal of Documentation*, Vol. 28, No. 1, pp. 11–21.
   - **DOI chính thức**: [10.1108/eb026526](https://doi.org/10.1108/eb026526) *(Nhà xuất bản Emerald Insight — Yêu cầu tài khoản thư viện đại học)*.
   - **Bản đọc mở & Giáo trình chuẩn (Open-Access References)**:
     - 📖 **Giáo trình Stanford NLP & IR (Manning, Raghavan, Schütze)**: [Chapter 6: Scoring, Term Weighting and the Vector Space Model (PDF)](https://nlp.stanford.edu/IR-book/pdf/06vect.pdf) — *Trình bày mô hình không gian vector (Vector Space Model) và kỹ thuật tính toán thực nghiệm; bảng ký hiệu chuẩn SMART notation (Hình 6.15, tr.128) với các biến thể sublinear tf, augmented tf, log idf, cosine normalization và pivoted length normalization. (Lưu ý: Nền tảng lý thuyết xác suất sâu xa của IDF được phân tích tại Chương 11: Probabilistic Information Retrieval qua mô hình Binary Independence Model)*.
     - 📄 **Báo cáo kỹ thuật Đại học Cambridge (Robertson & Spärck Jones)**: [Technical Report UCAM-CL-TR-356: Simple, Proven Approaches to Text Retrieval (PDF)](https://www.cl.cam.ac.uk/techreports/UCAM-CL-TR-356.pdf) — *Tài liệu nghiên cứu gốc giải thích cặn kẽ 3 thành tố trọng số: Collection Frequency Weight ($\text{CFW} = \log N - \log n$), Term Frequency & Document Length ($\text{NDL} = \frac{\text{DL}}{\text{AvgDL}}$), và công thức kết hợp BM25 với tham số bão hòa $k_1$ và tham số phạt độ dài văn bản $b$*.
     - 🌐 **Hồ sơ trích dẫn khoa học**: [Karen Spärck Jones (1972) trên Semantic Scholar](https://www.semanticscholar.org/paper/4f09e6ec1b7d4390d23881852fd7240994abeb58).
   - **Ý nghĩa**: Đặt nền móng cho trọng số IDF trong toàn bộ ngành Khoa học Máy tính và NLP.

2. **Neel Jain et al. (University of Maryland, 2023) — TF-IDF Chống Tấn Công LLM**:
   - **Tên bài báo**: *"Baseline Defenses for Adversarial Attacks on Large Language Models"*.
   - **Xuất bản**: arXiv:2309.00614.
   - **Link toàn văn**: [https://arxiv.org/abs/2309.00614](https://arxiv.org/abs/2309.00614)
   - **Ý nghĩa**: Nghiên cứu thực nghiệm chứng minh bộ phân loại TF-IDF Character n-grams chặn đứng 60% – 80% các cuộc tấn công đối kháng LLM với độ trễ siêu thấp.

3. **Giandomenico Cornacchia et al. (2024) — MoJE (Mixture of Jailbreak Experts)**:
   - **Tên bài báo**: *"MoJE: Mixture of Jailbreak Experts, Naive Tabular Classifiers as Guard for Prompt Attacks"*.
   - **Xuất bản**: arXiv:2409.17699.
   - **Link toàn văn**: [https://arxiv.org/abs/2409.17699](https://arxiv.org/abs/2409.17699)
   - **Ý nghĩa**: Chứng minh các bộ phân loại thống kê ngôn ngữ đạt 90% độ chính xác phát hiện Jailbreak mà không làm hại prompt lành tính.

---

## 🌐 2. TÀI LIỆU ĐỌC & HƯỚNG DẪN KỸ THUẬT (DOCUMENTATION)

1. **Tài liệu chính thức Scikit-learn (Mục 6.2 - Feature Extraction)**:
   - [Scikit-Learn Text Feature Extraction Guide](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction)
   - *Nội dung cần đọc*: Giải thích chi tiết toán học của `TfidfVectorizer`, công thức `smooth_idf`, `sublinear_tf` và tham số `char_wb`.
2. **Towards Data Science**:
   - [TF-IDF from Scratch in Python with Mathematics](https://towardsdatascience.com/) — *Giải thích trực quan từng bước nhân ma trận*.

---

## 🎥 3. TUYỂN TẬP VIDEO BÀI GIẢNG TRỰC QUAN ĐÃ KIỂM ĐỊNH (100% HOẠT ĐỘNG)

1. **Codebasics (NLP Playlist - Tập 6)**:
   - **Tiêu đề**: *Text Representation Using TF-IDF: NLP Tutorial For Beginners - S2 E6*
   - **Link video**: [https://www.youtube.com/watch?v=ATK6fm3cYfI](https://www.youtube.com/watch?v=ATK6fm3cYfI)
   - **Thời lượng**: ~20 phút.
   - **Điểm hay**: Giải thích trực quan bằng bảng tính Excel cách tính TF, IDF và viết code Scikit-learn với bộ dữ liệu thực tế.

2. **Krish Naik**:
   - **Tiêu đề**: *Natural Language Processing | TF-IDF Intuition | Text Preprocessing*
   - **Link video**: [https://www.youtube.com/watch?v=D2V1okCEsiE](https://www.youtube.com/watch?v=D2V1okCEsiE)
   - **Thời lượng**: ~15 phút.
   - **Điểm hay**: Đi thẳng vào bản chất công thức toán học TF, IDF và phân tích lý do tại sao từ hiếm có trọng số cao hơn từ phổ biến.

3. **StatQuest with Josh Starmer (Không Gian Vector & Word Embedding)**:
   - **Tiêu đề**: *Word Embedding and Word2Vec, Clearly Explained!!!*
   - **Link video**: [https://www.youtube.com/watch?v=viZrOnJclY0](https://www.youtube.com/watch?v=viZrOnJclY0)
   - **Thời lượng**: ~16 phút.
   - **Điểm hay**: Giúp hiểu rõ bước chuyển dịch từ biểu diễn tần suất từ (TF-IDF bag-of-words) sang không gian embedding ngữ nghĩa.

4. **StatQuest with Josh Starmer (Toán Học & Thuật Toán Tuyến Tính Baseline)**:
   - [Logistic Regression Details Pt.1: Coefficients and Odds](https://www.youtube.com/watch?v=yIYKR4sgzI8) — *Hiểu sâu về hàm Sigmoid và Log-Odds trong bài toán phân loại nhị phân*.
   - [Support Vector Machines (SVM) Clearly Explained](https://www.youtube.com/watch?v=efR1C6CvhmE) — *Hiểu về siêu phẳng phân chia (Hyperplane) và Margin cực đại*.
   - [ROC and AUC Curves Clearly Explained](https://www.youtube.com/watch?v=4jRBRDbJemM) — *Cách vẽ và đánh giá đường cong ROC-AUC phục vụ đo lường False Positive Rate (FPR)*.
