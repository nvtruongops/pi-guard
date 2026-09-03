# TÀI LIỆU HỌC TẬP, BÀI BÁO GỐC & VIDEO: DEBERTA-V3 & DISENTANGLED ATTENTION

---

## 📄 1. CÁC BÀI BÁO KHOA HỌC GỐC (ICLR / NEURIPS LANDMARK PAPERS)

1. **Pengcheng He, Jianfeng Gao, Weizhu Chen (Microsoft Research) — DeBERTa-v3**:
   - **Tên bài báo**: *"DeBERTaV3: Improving DeBERTa using ELECTRA-Style Pre-Training with Gradient-Disentangled Embedding Sharing"*.
   - **Hội nghị**: **ICLR 2023** (*International Conference on Learning Representations* - Hội nghị AI hàng đầu thế giới).
   - **Link toàn văn arXiv**: [https://arxiv.org/abs/2111.09543](https://arxiv.org/abs/2111.09543)
   - **Link OpenReview**: [https://openreview.net/forum?id=sE7-XhLxHA](https://openreview.net/forum?id=sE7-XhLxHA)

2. **Pengcheng He, Xiaodong Liu, Jianfeng Gao, Weizhu Chen — DeBERTa v1 (Gốc)**:
   - **Tên bài báo**: *"DeBERTa: Decoding-enhanced BERT with Disentangled Attention"*.
   - **Hội nghị**: **ICLR 2021** (Oral Presentation).
   - **Link toàn văn arXiv**: [https://arxiv.org/abs/2006.03654](https://arxiv.org/abs/2006.03654)
   - **Ý nghĩa**: Giới thiệu công thức toán học phân rã Attention thành Content và Relative Position.

3. **Zhewei Yao et al. (Microsoft Research) — ZeroQuant INT8 Post-Training Quantization**:
   - **Tên bài báo**: *"ZeroQuant: Efficient and Affordable Post-Training Quantization for Large-Scale Transformers"*.
   - **Hội nghị**: **NeurIPS 2022**.
   - **Link toàn văn arXiv**: [https://arxiv.org/abs/2206.01861](https://arxiv.org/abs/2206.01861)
   - **Ý nghĩa**: Cơ sở khoa học của kỹ thuật nén mô hình DeBERTa-v3 từ 500MB xuống 140MB chạy trên CPU.

4. **Meta AI Research (2024 - 2025) — Meta Prompt-Guard-86M**:
   - **Mô hình**: [meta-llama/Prompt-Guard-86M trên Hugging Face](https://huggingface.co/meta-llama/Prompt-Guard-86M)
   - **Kiến trúc**: Chính thức sử dụng `mDeBERTa-v3-base` để làm chốt chặn an toàn cho toàn bộ hệ sinh thái LLaMA.

---

## 🌐 2. TÀI LIỆU KỸ THUẬT & BLOG CHUYÊN SÂU

1. **Microsoft Research Blog**:
   - [DeBERTa: Decoding-enhanced BERT with Disentangled Attention](https://www.microsoft.com/en-us/research/blog/deberta-decoding-enhanced-bert-with-disentangled-attention/) — *Bài viết chính thức của nhóm tác giả giải thích động lực nghiên cứu*.
2. **Hugging Face Transformers Documentation**:
   - [DeBERTa-v2 / DeBERTa-v3 Architecture and API](https://huggingface.co/docs/transformers/model_doc/deberta-v2) — *Hướng dẫn sử dụng lớp `DebertaV2ForSequenceClassification`*.
3. **Towards Data Science**:
   - [DeBERTa Explained: Disentangled Attention & Enhanced Mask Decoder](https://towardsdatascience.com/) — *Trực quan hóa cấu trúc từng tầng Attention*.

---

## 🎥 3. TUYỂN TẬP VIDEO BÀI GIẢNG TRỰC QUAN (YOUTUBE)

1. **Yannic Kilcher (Kênh YouTube AI Số 1 Thế Giới)**:
   - **Tiêu đề**: *DeBERTa: Decoding-enhanced BERT with Disentangled Attention (Machine Learning Paper Explained)*
   - **Link video**: [https://www.youtube.com/watch?v=kYJ-wG4sD9U](https://www.youtube.com/watch?v=kYJ-wG4sD9U)
   - **Thời lượng**: ~35 phút.
   - **Điểm hay**: Đây là video xuất sắc nhất thế giới phân tích chi tiết từng phương trình toán học của Disentangled Attention và Enhanced Mask Decoder. Bắt buộc 4 thành viên phải xem trước khi bảo vệ đồ án!

2. **Machine Learning Paper Club (nPlan)**:
   - **Tiêu đề**: *Vahan Hovhannisyan: DEBERTA - Decoding-enhanced BERT with Disentangled Attention*
   - **Link video**: [https://www.youtube.com/watch?v=T_s_7vW9s8M](https://www.youtube.com/watch?v=T_s_7vW9s8M)
   - **Thời lượng**: ~45 phút.
   - **Điểm hay**: Buổi thảo luận khoa học chuyên sâu giữa các chuyên gia AI về lý do tại sao DeBERTa đánh bại RoBERTa trên các benchmark khắt khe.

3. **Umar Jamil**:
   - **Tiêu đề**: *Attention is all you need (Transformer) - Detailed Explanation and Code Walkthrough*
   - **Link video**: [https://www.youtube.com/watch?v=bCz4OMemCcA](https://www.youtube.com/watch?v=bCz4OMemCcA)
   - **Thời lượng**: ~55 phút.
   - **Điểm hay**: Dựng toàn bộ ma trận Attention từ đầu bằng PyTorch, giúp hiểu sâu bản chất Query, Key, Value.

4. **Stanford University CS224N (Natural Language Processing with Deep Learning)**:
   - **Tiêu đề**: *Lecture 5: Self-Attention and Transformers (Prof. Christopher Manning)*
   - **Link video**: [https://www.youtube.com/watch?v=kCc8FmEb1nY](https://www.youtube.com/watch?v=kCc8FmEb1nY)
   - **Điểm hay**: Giáo trình chuẩn của Đại học Stanford giảng dạy bài bản về không gian biểu diễn ngữ nghĩa.
