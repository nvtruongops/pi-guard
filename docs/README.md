# THƯ MỤC CỔNG TÀI LIỆU GITHUB PAGES (`docs/`)
## 🌐 PI-Guard Official Documentation Portal (MkDocs Material 8-Pillar Architecture)

> [!IMPORTANT]
> **QUY TẮC BẤT DI BẤT DỊCH (DOCUMENTATION INVARIANTS)**:
> 1. Thư mục `docs/` này là **NGUỒN DỮ LIỆU CHÍNH THỨC CỦA CỔNG TÀI LIỆU GITHUB PAGES** (biên dịch qua MkDocs Material).
> 2. Thư mục nội bộ [`docs/fpt_capstone_guide/`](file:///d:/Work/Do-an/docs/fpt_capstone_guide/) là **BẤT BIẾN / READ-ONLY TUYỆT ĐỐI**, không bao giờ được sửa đổi, xóa bỏ hay xuất bản công khai (đã được loại trừ khỏi build qua `exclude_docs` trong `mkdocs.yml`).
> 3. Toàn bộ tài liệu Web UI trong các thư mục con chuyên đề được tự động thu thập, chuẩn hóa liên kết và biên dịch thông qua script `python scripts/build_docs_portal.py`.
> 4. Mọi nghiên cứu và bản thảo cá nhân phải được thực hiện trong `workspaces/<tên_thành_viên>/docs/` trước khi họp chốt đồng quy tri thức.

---

### 📂 CẤU TRÚC PHÂN CẤP TÀI LIỆU GITHUB PAGES:

| Thư mục con / Trang | Nội dung & Chức năng | Cơ chế cập nhật |
| :--- | :--- | :--- |
| [`docs/index.md`](file:///d:/Work/Do-an/docs/index.md) | Trang chủ tổng quan đề tài, sơ đồ kiến trúc Mermaid 2 tầng & thông tin nhóm | Sinh tự động bởi `build_docs_portal.py` |
| [`docs/fpt_capstone_guide/`](file:///d:/Work/Do-an/docs/fpt_capstone_guide/) | Tài liệu, biểu mẫu, rubrics hướng dẫn đồ án nội bộ FPT University | **BẤT BIẾN / READ-ONLY** (Đã ignore khỏi Git) |
| `docs/work/` | Lộ trình tiêu chuẩn FPT IAP491 và biên bản 3 cuộc họp (Meeting 1, 2, 3) | Đồng bộ từ `reports/Meeting/` |
| `docs/prompt_study/` | **Chuyên Đề 1**: Nền tảng LLM, Token Generation, Prompt Structure & Instruction Hierarchy | Đồng bộ từ `workspaces/truongnv/docs/` |
| `docs/attacks/` | **Chuyên Đề 2**: Phân loại Prompt Injection (OWASP LLM01) & 4 trường phái Jailbreak | Đồng bộ từ `workspaces/truongnv/docs/` |
| `docs/threat_defense/` | **Chuyên Đề 3**: Mô hình hóa mối đe dọa (NIST AI 100-2e2025) & Kiến trúc 3 lớp | Đồng bộ từ `workspaces/truongnv/docs/` |
| `docs/dataset_study/` | **Chuyên Đề 4**: Tuyển chọn dữ liệu 3 lớp, MinHash Deduplication & Group-Aware Splitting | Đồng bộ từ `workspaces/truongnv/docs/` |
| `docs/models/` | **Chuyên Đề 5**: Toán học TF-IDF, Transformer DeBERTa-v3 & Điều phối 2 tầng Cascaded | Đồng bộ từ `workspaces/truongnv/docs/` |
| `docs/robustness/` | **Chuyên Đề 6**: Độ bền đối kháng, chống nhiễu Leetspeak, Spacing, Homoglyphs & Base64 | Đồng bộ từ `workspaces/truongnv/docs/` |
| `docs/optimization/` | **Chuyên Đề 7**: Lượng tử hóa INT8 PTQ, tối ưu ONNX Runtime Graph & Độ trễ P95/P99 | Đồng bộ từ `workspaces/truongnv/docs/` |
| `docs/evaluation_study/` | **Chuyên Đề 8**: Kinh tế học FPR, Đường cong biên Pareto & Đánh đổi an toàn/trải nghiệm | Đồng bộ từ `workspaces/truongnv/docs/` |
| `docs/research/` | Các bài nghiên cứu đối sánh SOTA (Llama Guard, NeMo, Target LLMs, Tencent 2026) | Đồng bộ từ `workspaces/truongnv/docs/` |
| `docs/thesis/` | Bản đăng ký đề tài chính thức, hồ sơ Review 1 và các chương luận văn hoàn thiện | Đồng bộ từ `CAPSTONE REGISTER` & `reports/thesis/` |
| `docs/references/` | Bảng tra cứu & ma trận áp dụng 18 bài báo khoa học toàn văn PDF | Đồng bộ từ `reports/References/` |
| `docs/dev/` | Quy chế phân quyền Git, hướng dẫn đóng góp và đặc tả kiến trúc mã nguồn | Đồng bộ từ `AGENTS.md`, `CONTRIBUTING.md` |
| `docs/javascripts/` & `stylesheets/` | Cấu hình MathJax LaTeX hiển thị công thức toán và Custom CSS bảng biểu | Sinh tự động bởi `build_docs_portal.py` |

---

### 🔄 LỆNH BIÊN DỊCH VÀ XEM TRƯỚC CỔNG TÀI LIỆU:

```bash
# 1. Thu thập & chuẩn hóa toàn bộ tài liệu vào docs/
python scripts/build_docs_portal.py

# 2. Khởi chạy máy chủ MkDocs xem trước cục bộ (Hot-reload)
mkdocs serve

# 3. Kiểm tra tính toàn vẹn và biên dịch trang tĩnh sang thư mục site/
mkdocs build --strict
```
