import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    log_path = 'workspaces/truongnv/References/REFERENCES_LOG.md'
    with open(log_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update table: add 39 after 38
    target_table = '''| **38. Granite Guardian (IBM Research 2024)** | [IBM-GraniteGuardian] | Padhi et al. (IBM Research, 2024) | [Padhi_2024_Granite_Guardian_Content_Safety_Risk_Detection.pdf](file:///d:/Work/Do-an/workspaces/truongnv/References/Padhi_2024_Granite_Guardian_Content_Safety_Risk_Detection.pdf) | Dòng mô hình mở chuyên biệt cho an toàn nội dung và rủi ro LLM (2B/8B), bao phủ Jailbreak, Prompt Injection và RAG Hallucination. | **Mô hình tham chiếu SOTA SLM Guardrail**: Cung cấp cơ sở đối chuẩn cho tầng phân xử cấp cao (High-Assurance Arbiter) ở Tier 3. |'''

    new_table_row = target_table + '''\n| **39. Crescendo Multi-Turn Attack (Microsoft 2024)** | [MS-Crescendo] | Russinovich et al. (Microsoft Research, 2024) | [Russinovich_2024_Crescendo_MultiTurn_Jailbreak_Attack.pdf](file:///d:/Work/Do-an/workspaces/truongnv/References/Russinovich_2024_Crescendo_MultiTurn_Jailbreak_Attack.pdf) | Phát hiện phương thức tấn công đa lượt leo thang (Crescendo Attack); chứng minh các bộ lọc đơn lượt (single-turn) hoàn toàn bất lực trước kỹ thuật khai thác ngữ cảnh tích lũy. | **Cơ sở mở rộng nhánh nghiên cứu Multi-turn State Tracking**: Luận chứng cho việc đánh đổi độ trễ để duy trì bộ nhớ phiên và phân tích trôi dạt ngữ cảnh (Contextual Drift). |'''

    if target_table in content:
        content = content.replace(target_table, new_table_row)
        print('Updated overview table with paper 39.')
    else:
        print('Target table row 38 not found!')

    # 2. Update Section 3: add dossier after paper 38
    target_section = '''- **Mục tiêu kỹ thuật & Giả thuyết của PI-Guard (Tier 3)**: Sử dụng phiên bản lượng tử hóa INT4 của mô hình 2B làm trọng tài thẩm định sâu với độ trễ P95 < 120ms trên CPU.\n\n---'''

    new_section_dossier = target_section + '''\n\n### 39. Great, Now Write an Article About That: The Crescendo Multi-Turn LLM Jailbreak Attack (Russinovich et al., Microsoft Research 2024)\n- **Tên bài báo**: *Great, Now Write an Article About That: The Crescendo Multi-Turn LLM Jailbreak Attack*\n- **Tác giả**: Mark Russinovich, Ahmed Salem, Ronen Eldan (Microsoft Research & Azure)\n- **Venue**: *arXiv preprint arXiv:2404.01833* (2024)\n- **DOI / URL**: [https://arxiv.org/abs/2404.01833](https://arxiv.org/abs/2404.01833) | Open-Access PDF: [https://arxiv.org/pdf/2404.01833.pdf](https://arxiv.org/pdf/2404.01833.pdf)\n- **Tệp PDF Cục Bộ**: [Russinovich_2024_Crescendo_MultiTurn_Jailbreak_Attack.pdf](file:///d:/Work/Do-an/workspaces/truongnv/References/Russinovich_2024_Crescendo_MultiTurn_Jailbreak_Attack.pdf)\n- **Nguồn thẩm quyền gốc**: Microsoft Research Technical Report / arXiv.\n- **Đóng góp gốc (Tier 1)**: Phát hiện và hình thức hóa kỹ thuật tấn công đa lượt Crescendo: kẻ tấn công bắt đầu bằng các câu hỏi hoàn toàn vô hại, sau đó từng bước hướng dẫn LLM tạo ra các khối nội dung nhỏ và cuối cùng kết hợp thành mã độc hoặc vũ khí nguy hại. Bài báo chứng minh tỷ lệ thành công của Crescendo đạt trên 80% trên GPT-4, Claude 3, Llama-2-70B và Gemini Pro, đồng thời làm tê liệt hoàn toàn mọi bộ lọc Ingress đơn lượt.\n- **Định vị kỹ thuật & Tiếp thu của PI-Guard (Tier 2)**: Luận chứng mang tính nền tảng cho việc mở rộng PI-Guard ra ngoài giới hạn đơn lượt của Low-Latency: chấp nhận đánh đổi thêm ~15–25ms độ trễ để duy trì bộ nhớ phiên (Session Sliding Window) và tính toán độ trôi dạt ngữ nghĩa (Semantic Drift Trajectory).\n- **Mục tiêu kỹ thuật & Giả thuyết của PI-Guard (Tier 3)**: Thiết kế mô-đun `MultiTurnCrescendoGuardrail` có khả năng chặn các đợt tấn công leo thang đa lượt với tỷ lệ phát hiện > 85% sau 3-5 lượt hội thoại.\n\n---'''

    if target_section in content:
        content = content.replace(target_section, new_section_dossier, 1)
        print('Updated Section 3 dossiers with paper 39.')
    else:
        print('Target section 38 not found!')

    # 3. Update BibTeX
    target_bib = '''@article{padhi2024granite,
  title     = {Granite Guardian: A Family of Open Models for Content Safety and Risk Detection},
  author    = {Padhi, Inkit and Nagireddy, Manish and Cornacchia, Giandomenico and Das, Subhro and Pedapati, Tejaswini and Patel, Hima and others},
  journal   = {arXiv preprint arXiv:2412.07724},
  year      = {2024}
}'''

    new_bib = target_bib + '''\n\n@article{russinovich2024crescendo,
  title     = {Great, Now Write an Article About That: The Crescendo Multi-Turn LLM Jailbreak Attack},
  author    = {Russinovich, Mark and Salem, Ahmed and Eldan, Ronen},
  journal   = {arXiv preprint arXiv:2404.01833},
  year      = {2024}
}'''

    if target_bib in content:
        content = content.replace(target_bib, new_bib)
        print('Updated BibTeX section with paper 39.')
    else:
        print('Target bib 38 not found!')

    with open(log_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Successfully updated REFERENCES_LOG.md with Paper 39.')

if __name__ == '__main__':
    main()
