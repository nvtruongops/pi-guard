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

1. **Microsoft Research & GitHub Official**:
   - [Microsoft DeBERTa Official Repository & Documentation](https://github.com/microsoft/DeBERTa) — *Kho mã nguồn chính thức của Microsoft cung cấp code pre-training, fine-tuning và benchmark của DeBERTa-v1/v2/v3*.
2. **Hugging Face Transformers Documentation**:
   - [DeBERTa-v2 / DeBERTa-v3 Architecture and API](https://huggingface.co/docs/transformers/model_doc/deberta-v2) — *Hướng dẫn sử dụng lớp `DebertaV2ForSequenceClassification`*.
3. **Towards Data Science**:
   - [DeBERTa Explained: Disentangled Attention & Enhanced Mask Decoder](https://towardsdatascience.com/) — *Trực quan hóa cấu trúc từng tầng Attention*.

---

## 🎥 3. TUYỂN TẬP VIDEO BÀI GIẢNG TRỰC QUAN ĐÃ KIỂM ĐỊNH (100% HOẠT ĐỘNG)

1. **3Blue1Brown (Trực quan hóa Toán học Đỉnh cao)**:
   - **Tiêu đề**: *Attention in transformers, step-by-step | Deep Learning Chapter 6*
   - **Link video**: [https://www.youtube.com/watch?v=eMlx5fFNoYc](https://www.youtube.com/watch?v=eMlx5fFNoYc)
   - **Thời lượng**: ~26 phút.
   - **Điểm hay**: Trực quan hóa hình học không gian vector Query, Key, Value và cơ chế phân phối xác suất Softmax một cách trực quan, xuất sắc nhất thế giới.

2. **Yannic Kilcher (Machine Learning Paper Review)**:
   - **Tiêu đề**: *Attention Is All You Need (Paper Review)*
   - **Link video**: [https://www.youtube.com/watch?v=iDulhoQ2pro](https://www.youtube.com/watch?v=iDulhoQ2pro)
   - **Thời lượng**: ~42 phút.
   - **Điểm hay**: Đọc và phân tích trực tiếp bài báo khoa học gốc, giải thích tại sao Attention thay thế hoàn toàn mạng hồi quy RNN/LSTM.

3. **StatQuest with Josh Starmer**:
   - **Tiêu đề**: *Transformer Neural Networks, ChatGPT's foundation, Clearly Explained!!!*
   - **Link video**: [https://www.youtube.com/watch?v=zxQyTK8quyY](https://www.youtube.com/watch?v=zxQyTK8quyY)
   - **Thời lượng**: ~29 phút.
   - **Điểm hay**: Từng bước tính toán ma trận Attention, Positional Encoding và Residual Connection theo phong cách trực quan, hóm hỉnh đặc trưng của Josh Starmer.

4. **Umar Jamil (Deep Dive Math & Code Walkthrough)**:
   - **Tiêu đề**: *Attention is all you need (Transformer) - Detailed Explanation and Code Walkthrough*
   - **Link video**: [https://www.youtube.com/watch?v=bCz4OMemCcA](https://www.youtube.com/watch?v=bCz4OMemCcA)
   - **Thời lượng**: ~55 phút.
   - **Điểm hay**: Dựng toàn bộ ma trận Attention và Transformer Encoder từ đầu bằng PyTorch thuần, hiểu sâu từng chiều tensor `(batch_size, seq_len, d_model)`.

5. **AssemblyAI (Hugging Face Thực Chiến)**:
   - **Tiêu đề**: *Getting Started With Hugging Face in 15 Minutes | Transformers, Pipeline, Tokenizer, Models*
   - **Link video**: [https://www.youtube.com/watch?v=QEaBAZQCtwE](https://www.youtube.com/watch?v=QEaBAZQCtwE)
   - **Thời lượng**: ~15 phút.
   - **Điểm hay**: Hướng dẫn thực hành tải mô hình Hugging Face, cấu hình Tokenizer và viết pipeline inference cho bài toán phân loại văn bản.
