# TÀI LIỆU HỌC TẬP, BÀI BÁO GỐC & VIDEO: TF-IDF BASELINE

---

## 📄 1. CÁC BÀI BÁO KHOA HỌC GỐC (PEER-REVIEWED & LANDMARK PAPERS)

1. **Karen Spärck Jones (1972) — Nguồn Gốc Lịch Sử Của IDF**:
   - **Tên bài báo**: *"A statistical interpretation of term specificity and its application in retrieval"*.
   - **Tạp chí**: *Journal of Documentation*, Vol. 28, No. 1, pp. 11–21.
   - **DOI**: [10.1108/eb026526](https://doi.org/10.1108/eb026526)
   - **Ý nghĩa**: Đặt nền móng cho trọng số IDF trong toàn bộ ngành Khoa học Máy tính.

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

## 🎥 3. TUYỂN TẬP VIDEO BÀI GIẢNG TRỰC QUAN (YOUTUBE)

1. **Codebasics (NLP Playlist - Tập 6)**:
   - **Tiêu đề**: *Text Representation Using TF-IDF (Intuition + Code)*
   - **Link video**: [https://www.youtube.com/watch?v=kR5t6H1T4H4](https://www.youtube.com/watch?v=kR5t6H1T4H4)
   - **Thời lượng**: ~20 phút.
   - **Điểm hay**: Giải thích trực quan bằng bảng tính Excel cách tính TF, IDF và viết code Scikit-learn.

2. **Datamlistic**:
   - **Tiêu đề**: *Term Frequency Inverse Document Frequency (TF-IDF) Explained*
   - **Link video**: [https://www.youtube.com/watch?v=38D1n7HhN_s](https://www.youtube.com/watch?v=38D1n7HhN_s)
   - **Thời lượng**: ~8 phút.
   - **Điểm hay**: Cực kỳ cô đọng, đi thẳng vào bản chất công thức toán học và sự khác biệt giữa từ hiếm và từ phổ biến.

3. **Adrian Dolinay**:
   - **Tiêu đề**: *NLP with Python: Term Frequency-Inverse Document Frequency (tf-idf) from Scratch*
   - **Link video**: [https://www.youtube.com/watch?v=f95i3B201_g](https://www.youtube.com/watch?v=f95i3B201_g)
   - **Thời lượng**: ~15 phút.
   - **Điểm hay**: Hướng dẫn tự code thuật toán TF-IDF từ đầu bằng Python thuần không dùng thư viện ngoài.

4. **StatQuest with Josh Starmer (Toán Học & Thuật Toán Tuyến Tính)**:
   - [Logistic Regression Details Pt.1: Coefficients and Odds](https://www.youtube.com/watch?v=yIYKR4sgzI8) — *Hiểu sâu về hàm Sigmoid và Log-Odds*.
   - [Support Vector Machines (SVM) Clearly Explained](https://www.youtube.com/watch?v=efR1C6CvhmE) — *Hiểu về siêu phẳng phân chia và Margin cực đại*.
   - [ROC and AUC Curves Clearly Explained](https://www.youtube.com/watch?v=4jRBRDbJemM) — *Cách vẽ và đánh giá đường cong ROC-AUC*.
