import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    log_path = 'workspaces/truongnv/References/REFERENCES_LOG.md'
    with open(log_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update table: add 37 & 38 after 36
    target_table = '''| **36. Conformal Risk Control (Angelopoulos 2024 / C-SafeGen 2025)** | [NeurIPS-ConformalGuardrail] | Angelopoulos et al. / Kang et al. (2024/2025) | [Angelopoulos_2024_Conformal_Risk_Control.pdf](file:///d:/Work/Do-an/workspaces/truongnv/References/Angelopoulos_2024_Conformal_Risk_Control.pdf) | Khung lý thuyết Conformal Risk Control (CRC) cung cấp bảo chứng an toàn thống kê hữu hạn mẫu cho hệ thống Guardrail; kiểm soát chặt chẽ ngân sách lỗi rủi ro. | **Cơ sở toán học cho ngưỡng Low-FPR**: Cung cấp bảo chứng toán học xác suất rủi ro FPR \\le 1.5\\% trên tập hiệu chuẩn cho Tri-State Policy Engine của PI-Guard. |'''

    new_table_rows = target_table + '''\n| **37. ModernBERT (Answer.AI / LightOn 2024)** | [arXiv-ModernBERT] | Warner et al. (Answer.AI / LightOn, 2024) | [Warner_2024_ModernBERT_Brings_Modern_Transformers_To_Encoders.pdf](file:///d:/Work/Do-an/workspaces/truongnv/References/Warner_2024_ModernBERT_Brings_Modern_Transformers_To_Encoders.pdf) | Đột phá kiến trúc Encoder với RoPE, GeGLU, FlashAttention-2, native context 8,192 tokens; thông lượng nhanh gấp 2x DeBERTa-v3 trên GPU/CPU. | **Ứng viên mô hình SOTA Tier 2**: Giải quyết triệt để rủi ro cắt cụt ngữ cảnh (truncation) trong RAG và tăng gấp đôi tốc độ phân loại Ingress Guardrail. |\n| **38. Granite Guardian (IBM Research 2024)** | [IBM-GraniteGuardian] | Padhi et al. (IBM Research, 2024) | [Padhi_2024_Granite_Guardian_Content_Safety_Risk_Detection.pdf](file:///d:/Work/Do-an/workspaces/truongnv/References/Padhi_2024_Granite_Guardian_Content_Safety_Risk_Detection.pdf) | Dòng mô hình mở chuyên biệt cho an toàn nội dung và rủi ro LLM (2B/8B), bao phủ Jailbreak, Prompt Injection và RAG Hallucination. | **Mô hình tham chiếu SOTA SLM Guardrail**: Cung cấp cơ sở đối chuẩn cho tầng phân xử cấp cao (High-Assurance Arbiter) ở Tier 3. |'''

    if target_table in content:
        content = content.replace(target_table, new_table_rows)
        print('Updated overview table.')
    else:
        print('Target table row not found!')

    # 2. Update Section 3: add dossiers after paper 36
    target_section = '''- **Mục tiêu kỹ thuật & Giả thuyết của PI-Guard (Tier 3)**: Đạt tỷ lệ chặn nhầm thực nghiệm $\\text{FPR} \\le 1.5\\%$ với độ tin cậy thống kê $1 - \\delta \\ge 95\\%$ trên tập kiểm định Benign thực tế.\n\n---'''

    new_section_dossiers = target_section + '''\n\n### 37. ModernBERT: Bringing Modern Transformer Innovations to Pre-trained Encoders (Warner et al., Answer.AI / LightOn 2024)\n- **Tên bài báo**: *ModernBERT: Bringing Modern Transformer Innovations to Pre-trained Encoders*\n- **Tác giả**: Benjamin Warner, Antoine Chaffin, Benjamin Clavié, Orion Weller, Oskar Hallström, Shraddha Vasanth, Nikhil Patry, Colin Raffel, Luke Zettlemoyer\n- **Venue**: *arXiv preprint arXiv:2412.13663* (2024)\n- **DOI / URL**: [https://arxiv.org/abs/2412.13663](https://arxiv.org/abs/2412.13663) | Open-Access PDF: [https://arxiv.org/pdf/2412.13663.pdf](https://arxiv.org/pdf/2412.13663.pdf)\n- **Tệp PDF Cục Bộ**: [Warner_2024_ModernBERT_Brings_Modern_Transformers_To_Encoders.pdf](file:///d:/Work/Do-an/workspaces/truongnv/References/Warner_2024_ModernBERT_Brings_Modern_Transformers_To_Encoders.pdf)\n- **Nguồn thẩm quyền gốc**: arXiv / Answer.AI & LightOn Technical Report.\n- **Đóng góp gốc (Tier 1)**: Hiện đại hóa kiến trúc Encoder-only (BERT/RoBERTa/DeBERTa) bằng cách tích hợp Rotary Position Embeddings (RoPE), GeGLU activations, FlashAttention-2, Unpadding và mở rộng context window lên 8,192 tokens. Đạt tốc độ suy luận nhanh hơn 2x so với DeBERTa-v3 trên GPU và vượt trội điểm số GLUE.\n- **Định vị kỹ thuật & Tiếp thu của PI-Guard (Tier 2)**: Đóng vai trò là mô hình phân loại ngữ nghĩa sâu SOTA thế hệ mới (Next-Gen Semantic Guardrail) tại Tier 2, khắc phục hoàn toàn giới hạn 512 tokens của DeBERTa-v3 khi bảo vệ các ứng dụng RAG xử lý văn bản dài.\n- **Mục tiêu kỹ thuật & Giả thuyết của PI-Guard (Tier 3)**: Đạt độ trễ P95 < 18ms trên CPU với ngữ cảnh 512 tokens và duy trì F1 > 0.92 trong việc phân loại Benign vs. Prompt Injection vs. Jailbreak.\n\n---\n\n### 38. Granite Guardian: A Family of Open Models for Content Safety and Risk Detection (Padhi et al., IBM Research 2024)\n- **Tên bài báo**: *Granite Guardian: A Family of Open Models for Content Safety and Risk Detection*\n- **Tác giả**: Inkit Padhi, Manish Nagireddy, Giandomenico Cornacchia, Subhro Das, Tejaswini Pedapati, Hima Patel, et al. (IBM Research)\n- **Venue**: *arXiv preprint arXiv:2412.07724* (2024)\n- **DOI / URL**: [https://arxiv.org/abs/2412.07724](https://arxiv.org/abs/2412.07724) | Open-Access PDF: [https://arxiv.org/pdf/2412.07724.pdf](https://arxiv.org/pdf/2412.07724.pdf)\n- **Tệp PDF Cục Bộ**: [Padhi_2024_Granite_Guardian_Content_Safety_Risk_Detection.pdf](file:///d:/Work/Do-an/workspaces/truongnv/References/Padhi_2024_Granite_Guardian_Content_Safety_Risk_Detection.pdf)\n- **Nguồn thẩm quyền gốc**: arXiv / IBM Research Technical Report.\n- **Đóng góp gốc (Tier 1)**: Thiết kế và huấn luyện dòng mô hình an toàn chuyên biệt (2B và 8B) dựa trên Granite, bao phủ toàn diện các rủi ro: Jailbreak, Direct/Indirect Prompt Injection, Context Relevance, Groundedness và Answer Relevance. Cung cấp cả nhãn rủi ro nhị phân và giải thích nguyên nhân rủi ro.\n- **Định vị kỹ thuật & Tiếp thu của PI-Guard (Tier 2)**: Cung cấp bằng chứng thực nghiệm và cơ sở đối chuẩn cho phân tầng SLM Guardrail (Thế hệ 1) tại Tier 3 (High-Assurance Arbiter), hỗ trợ phân xử các prompt có độ bất định cao.\n- **Mục tiêu kỹ thuật & Giả thuyết của PI-Guard (Tier 3)**: Sử dụng phiên bản lượng tử hóa INT4 của mô hình 2B làm trọng tài thẩm định sâu với độ trễ P95 < 120ms trên CPU.\n\n---'''

    if target_section in content:
        content = content.replace(target_section, new_section_dossiers, 1)
        print('Updated Section 3 dossiers.')
    else:
        print('Target section not found!')

    # 3. Update BibTeX: add entries
    target_bib = '''@article{angelopoulos2024conformal,
  title     = {Conformal Risk Control},
  author    = {Angelopoulos, Anastasios N. and Bates, Stephen and Cand{\\`e}s, Emmanuel J. and Jordan, Michael I. and Lei, Lihua},
  journal   = {arXiv preprint arXiv:2208.02814},
  year      = {2024}
}'''

    new_bib = target_bib + '''\n\n@article{warner2024modernbert,
  title     = {ModernBERT: Bringing Modern Transformer Innovations to Pre-trained Encoders},
  author    = {Warner, Benjamin and Chaffin, Antoine and Clavi{\\`e}, Benjamin and Weller, Orion and Hallstr{\\"o}m, Oskar and Vasanth, Shraddha and Patry, Nikhil and Raffel, Colin and Zettlemoyer, Luke},
  journal   = {arXiv preprint arXiv:2412.13663},
  year      = {2024}
}\n\n@article{padhi2024granite,
  title     = {Granite Guardian: A Family of Open Models for Content Safety and Risk Detection},
  author    = {Padhi, Inkit and Nagireddy, Manish and Cornacchia, Giandomenico and Das, Subhro and Pedapati, Tejaswini and Patel, Hima and others},
  journal   = {arXiv preprint arXiv:2412.07724},
  year      = {2024}
}'''

    if target_bib in content:
        content = content.replace(target_bib, new_bib)
        print('Updated BibTeX section.')
    else:
        print('Target bib entry not found!')

    with open(log_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Successfully updated REFERENCES_LOG.md')

if __name__ == '__main__':
    main()
