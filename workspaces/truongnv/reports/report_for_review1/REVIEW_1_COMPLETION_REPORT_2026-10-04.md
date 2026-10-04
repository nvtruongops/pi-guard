# Báo cáo tổng kết Review 1 — 04/10/2026

- **Workspace:** `workspaces/truongnv`
- **Ngày hoàn tất Review 1:** 04/10/2026, theo xác nhận của người giao nhiệm vụ.
- **Task nguồn:** [Review 1 lần 2 — chốt mô hình ingress và sơ đồ đề xuất](../report%20for%20review%201%20lan%202/TASK.md)
- **Phạm vi tài liệu:** tổng hợp đầu ra nghiên cứu và thiết kế đã bàn giao; không phải báo cáo nghiệm thu mô hình.

## 1. Tuyên bố ranh giới nhiệm vụ

| IN-SCOPE | OUT-OF-SCOPE |
|---|---|
| Tổng hợp căn cứ chọn các tầng; trạng thái bằng chứng và nguồn; ngưỡng/routing; chunk và handoff; ma trận Direct PI, Indirect PI và Jailbreak; kết quả sơ đồ và tài liệu Review 1. | Huấn luyện hoặc triển khai cascade; tuyên bố cascade đã chạy; đặt giá trị cutoff/chunk chưa validation; kết luận KPI P95/FPR đã đạt; thay đổi backend, upload/OCR hoặc tài liệu master. |

Task nguồn yêu cầu nghiên cứu và mô tả kiến trúc, đồng thời loại trừ triển khai cascade và metric cascade. Vì vậy, ngày Review 1 hoàn tất được ghi theo chỉ đạo của người dùng; nội dung dưới đây chỉ tổng kết các tài liệu trong workspace và không suy ra một biên bản nghiệm thu riêng.

## 2. Bàn giao theo nhiệm vụ

Gói [Review 1 lần 2](../report%20for%20review%201%20lan%202/README.md) gồm chín ghi chú nghiên cứu và một sơ đồ Draw.io tám trang. Bảng sau định vị nội dung để tra cứu:

| Tệp | Nội dung bàn giao |
|---|---|
| [01 — Cascade evidence](../report%20for%20review%201%20lan%202/01_TWO_TIER_CASCADE_EVIDENCE.md) | Phân định điều paper hỗ trợ và chưa hỗ trợ cho TF-IDF, threshold và cascade. |
| [02 — L2 estimator](../report%20for%20review%201%20lan%202/02_TIER1_LOGREG_VS_LINEARSVC.md) | Cơ sở chọn Logistic Regression làm baseline; LinearSVC giữ ở vai trò ablation. |
| [03 — Provenance](../report%20for%20review%201%20lan%202/03_RESEARCH_SOURCE_PROVENANCE.md) | Nguồn paper, checkpoint, code và giới hạn đối chiếu. |
| [04 — Defense notes](../report%20for%20review%201%20lan%202/04_REVIEW1_DEFENSE_KEY_NOTES.md) | Luận điểm trả lời câu hỏi về tầng, threshold, model tham khảo và latency. |
| [05 — DeBERTa references](../report%20for%20review%201%20lan%202/05_DEBERTA_REFERENCE_MODELS.md) | Phân biệt backbone dự kiến của đồ án với các detector dùng để đối chuẩn. |
| [06 — Threshold audit](../report%20for%20review%201%20lan%202/06_TFIDF_THRESHOLD_ROUTING_PAPER_AUDIT.md) | Đối chiếu paper và protocol validation-only cho hai cutoff của PI-Guard. |
| [07 — Chunking and handoff](../report%20for%20review%201%20lan%202/07_CHUNKING_AND_BACKEND_HANDOFF_DESIGN.md) | Đơn vị chunk, n-gram, DTO, lời gọi nội bộ và giới hạn chưa validation. |
| [08 — PI/Jailbreak taxonomy](../report%20for%20review%201%20lan%202/08_PI_JB_ATTACK_TAXONOMY_MATRIX.md) | Ma trận nguồn/đường đưa chỉ thị, mục tiêu tấn công và giới hạn benchmark. |
| [09 — Research direction](../report%20for%20review%201%20lan%202/09_RESEARCH_DIRECTION_ASSESSMENT.md) | Đánh giá giả thuyết nghiên cứu, rủi ro và lộ trình kiểm chứng. |
| [Sơ đồ ingress đề xuất](../report%20for%20review%201%20lan%202/REVIEW1_PROPOSED_INGRESS_ML_ARCHITECTURE.drawio) | Tám trang: tổng quan, overview dọc, L1/L2/L3 tối giản và L1/L2/L3 chi tiết. |

## 3. Tổng hợp mô hình đề xuất và bằng chứng

### Kiến trúc được trình bày

1. **L1 — ingress:** nhận prompt hoặc file; phần trích xuất, chuẩn hóa, chia chunk và giữ source map là thiết kế đề xuất. Các parser/OCR và giới hạn upload chưa được xác nhận là thành phần đã triển khai.
2. **L2 — lexical baseline:** TF-IDF + Logistic Regression chấm từng chunk. Hai cutoff `τ_allow` và `τ_block` tạo các route ALLOW candidate, REVIEW→L3 và BLOCK candidate; giá trị cutoff chỉ được chọn trên validation rồi đóng băng trước test. [[1]](#ref1) [[3]](#ref3) [[4]](#ref4)
3. **L3 — semantic classifier:** `microsoft/deberta-v3-base` là backbone dự kiến, cần classification head và huấn luyện theo dữ liệu/protocol đồ án. Nó được phân biệt với các detector đã fine-tune được liệt kê làm model đối chuẩn. [[2]](#ref2) [[5]](#ref5)
4. **API aggregation:** REVIEW là route nội bộ từ L2 sang L3; API kiểm tra coverage, tổng hợp prediction và kết thúc request bằng ALLOW hoặc BLOCK. Theo thiết kế, chỉ request ALLOW được chuyển tiếp tới LLM. Đây là proposal, chưa phải hành vi được chứng minh của cascade. [[4]](#ref4)

Sơ đồ mô tả các tầng như module nội bộ cùng process với handoff `CanonicalTextEnvelope` → `ChunkRouteResult[]` → `RoutedChunk[]` → `WindowPrediction[]`. Các giá trị chunk 256 token/overlap 32 và sweep validation là ứng viên; giới hạn 512 vị trí model của backbone không biến chúng thành kết quả benchmark. [[2]](#ref2) [[5]](#ref5)

### Phân định ba loại bằng chứng

- **Y văn:** bài Akinrele và Gowda được dùng để tham chiếu baseline TF-IDF + Logistic Regression, DeBERTa-base và selective routing trên điểm mô hình ngữ nghĩa. Bài đó không kiểm nghiệm chính xác cascade TF-IDF→DeBERTa của PI-Guard, nên không chứng minh được lợi ích cascade hay cutoff PI-Guard. [[1]](#ref1) [[6]](#ref6)
- **Bằng chứng cục bộ có trước Review 1:** báo cáo kỹ thuật trước đây giữ riêng PIDS-Bench TF-IDF cùng nguồn paper và lượt suy luận checkpoint PIGuard trên tài sản do PIGuard phát hành. Hai giao thức khác nhau, không phải so sánh head-to-head và không đo cascade. [[7]](#ref7)
- **Đề xuất đồ án:** ba route tại L2, classifier L3, API aggregation, cấu hình chunk và handoff là thiết kế cần triển khai/đánh giá ở bước sau; không có cutoff số hay KPI cascade nào được báo cáo ở đây. [[4]](#ref4) [[6]](#ref6)

Ma trận taxonomy giữ Direct/Indirect PI như trục nguồn hoặc đường đưa chỉ thị, còn Jailbreak là trục mục tiêu; các thuộc tính có thể giao nhau. BIPIA và JailbreakBench được chọn làm benchmark tham chiếu chính cho hai nhiệm vụ khác nhau, không dùng metric của chúng như metric detector PI-Guard. [[8]](#ref8)

## 4. Bàn giao cho Review 2

Review 2 chuyển từ hồ sơ đề xuất sang nghiên cứu chi tiết và demo chức năng theo [task Review 2](../tasks_for_review2/TASK.md). Gói Review 1 không chứa bằng chứng cascade đã chạy hoặc đạt KPI. Task thực nghiệm cascade được theo dõi riêng tại [TASK.md](../experiment_reports/tfidf_deberta_cascade_2026-10-04/TASK.md); trạng thái hoàn thành phải căn cứ vào output un-mocked và manifest của task đó.

## 5. Bảng kiểm tra tuân thủ phạm vi

| Kiểm tra | Trạng thái | Căn cứ |
|---|---|---|
| Tổng kết bám đúng task Review 1 lần 2 | PASS | Chín ghi chú và sơ đồ trong gói nguồn. |
| Không biến kiến trúc đề xuất thành cascade đã triển khai | PASS | Ranh giới được nêu tại các mục 1 và 3. |
| Không gán số cutoff hoặc KPI chưa đo | PASS | Chỉ nêu protocol validation và mục tiêu thiết kế. |
| Tách y văn, bằng chứng cục bộ và proposal | PASS | Mục 3 phân biệt từng loại. |
| Ghi ngày hoàn tất theo chỉ đạo của người dùng | PASS | 04/10/2026; không suy rộng thành biên bản nghiệm thu. |

## References

<a id="ref1"></a>**[1]** A. Akinrele and S. N. Gowda, “Prompt Injection Detection is Regime-Dependent: A Deployment-Aware Evaluation with Interpretable Structural Signals,” arXiv:2605.26999v1, 2026. [Paper](https://arxiv.org/html/2605.26999).

<a id="ref2"></a>**[2]** Microsoft, [`microsoft/deberta-v3-base` model card](https://huggingface.co/microsoft/deberta-v3-base).

<a id="ref3"></a>**[3]** scikit-learn, [Tuning the decision threshold for class prediction](https://scikit-learn.org/stable/modules/classification_threshold.html).

<a id="ref4"></a>**[4]** PI-Guard, [Review 1 lần 2 — README tổng hợp](../report%20for%20review%201%20lan%202/README.md).

<a id="ref5"></a>**[5]** PI-Guard, [DeBERTa reference models](../report%20for%20review%201%20lan%202/05_DEBERTA_REFERENCE_MODELS.md).

<a id="ref6"></a>**[6]** PI-Guard, [TF-IDF threshold and routing paper audit](../report%20for%20review%201%20lan%202/06_TFIDF_THRESHOLD_ROUTING_PAPER_AUDIT.md).

<a id="ref7"></a>**[7]** PI-Guard, [Review 1 technical evidence status](REVIEW_1_REPORT.md), evidence cut-off 30/09/2026.

<a id="ref8"></a>**[8]** PI-Guard, [Direct PI / Indirect PI / Jailbreak taxonomy matrix](../report%20for%20review%201%20lan%202/08_PI_JB_ATTACK_TAXONOMY_MATRIX.md).
