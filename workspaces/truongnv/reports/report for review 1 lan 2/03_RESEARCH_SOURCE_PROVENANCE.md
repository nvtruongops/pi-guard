# 03 — Nguồn nghiên cứu, checkpoint và giới hạn đối chiếu

## Scope Boundary Declaration

- **Nguồn nhiệm vụ:** [TASK.md](TASK.md), Review 1 lần 2, 2026-10-01.
- **IN-SCOPE:** xác minh nguồn bài arXiv làm căn cứ TF-IDF/threshold; phân biệt backbone đồ án với detector DeBERTa đã huấn luyện; ghi nguồn checkpoint tham khảo và nhãn/điều kiện truy cập.
- **OUT-OF-SCOPE:** hợp nhất kết quả paper khác dataset; báo cáo metric model tham khảo như kết quả của đồ án; cài/tải checkpoint hoặc thay đổi `REFERENCES_LOG.md` master.

## Sổ nguồn

| ID | Nguồn | Điều đã xác minh | Cách dùng trong Review 1 lần 2 |
|---|---|---|---|
| S1 | Akinrele & Gowda, arXiv:2605.26999v1. [[1]](#ref1) | Nêu sparse lexical baseline TF-IDF + Logistic Regression; có DeBERTa-base được fine-tune; có semantic-score routing và validation-only threshold selection. | Căn cứ duy nhất đang dùng để nói TF-IDF + LR là phương án lexical có thể đánh giá. Routing của bài không phải TF-IDF→DeBERTa; không sao chép ngưỡng hay số liệu. |
| S2 | `microsoft/deberta-v3-base` model card. [[2]](#ref2) | Checkpoint tổng quát cho fill-mask/pretraining, MIT license; model card mô tả cấu hình pretrained, không phải detector prompt injection đã fine-tune. | Backbone dự kiến cho classifier riêng của đồ án; cần task-specific classification head và huấn luyện theo dữ liệu/nhãn của dự án. |
| S3 | PIGuard ACL 2025 và repo chính thức. [[3]](#ref3) [[4]](#ref4) | Paper mô tả MOF để giảm over-defense; repo công bố code/dataset/model; code huấn luyện khởi tạo `microsoft/deberta-v3-base` với `num_labels=2`. | Detector DeBERTa đã fine-tune để đối chuẩn sau này; không phải backbone rỗng và không cùng nhãn 3 lớp của đồ án. |
| S4 | Meta Prompt Guard 86M model card/repository. [[5]](#ref5) | Dùng mDeBERTa-v3-base; Prompt Guard v1 phát hiện benign/injection/jailbreak; model có cổng truy cập và điều khoản Llama Community. | Ứng viên đối chuẩn có nhãn gần nhất với nhãn dự kiến của đồ án, tùy điều kiện truy cập/điều khoản; không gọi là base model. |
| S5 | PromptShield DeBERTa (Jacob et al., CODASPY 2025). [[6]](#ref6) | Fine-tuned từ DeBERTa-v3-base; paper công bố và nhóm tác giả cung cấp mã fine-tuning `finetuning_deberta.py`. | Ứng viên đối chuẩn nghiên cứu có paper và mã fine-tuning công khai, tối ưu cho low-FPR regime. |
| S6 | Llama Prompt Guard 2 86M model card và scanner repository. [[7]](#ref7) | Bản 86M dùng mDeBERTa-base (trong khi bản 22M dùng DeBERTa-xsmall); mục tiêu output là benign/malicious nhị phân trong LlamaFirewall (Meta, 2025). | Họ mô hình đối chuẩn cập nhật từ Meta trên cùng backbone 86M; mã scanner/inference công khai. |
| S7 | Audit bằng chứng cục bộ PI-Guard. [[8]](#ref8) | Không có phép chạy cascade/routing đầu-cuối; P95 và FPR hệ thống vẫn là mục tiêu. | Không gán latency, FPR hay lợi ích cascade cho đồ án. |

## Ranh giới route và quyết định trong kiến trúc đề xuất

- L2 phát ba route state theo chunk: ALLOW candidate, REVIEW→L3, hoặc BLOCK candidate. Đây là thiết kế cần đánh giá; score/cutoff chưa được xác nhận cho PI-Guard.
- L3 trả class score/prediction cho chunk được route bằng REVIEW; REVIEW không phải nhãn do L3 phát ra.
- API kiểm tra coverage, tổng hợp kết quả và chỉ phát quyết định cuối ALLOW hoặc BLOCK. Không có pending, HOLD hay reviewer queue trong thiết kế.
- Middleware hiện tại chưa triển khai đúng cascade đề xuất; cần đổi luồng trước khi dùng các route shortcut. [Middleware source](../../src/api/middleware.py)

## Phân biệt “base” với “model tham khảo”

- **Base của đồ án:** `microsoft/deberta-v3-base`, pretrained encoder tổng quát. Khi tạo classifier, cần gắn head cho taxonomy của PI-Guard và huấn luyện/fine-tune trên tập train của dự án. Chỉ tải base rồi gọi inference không tạo ra detector prompt injection. [[2]](#ref2)
- **Meta Prompt Guard:** là detector đã fine-tune trên backbone multilingual `mDeBERTa-v3-base`; không thay vai trò backbone đồ án. Dùng nó như một model đối chuẩn đã huấn luyện, nếu có quyền truy cập phù hợp. [[5]](#ref5)
- **PIGuard và PromptShield:** là các detector dựa trên DeBERTa-v3-base có paper và mã nguồn chính thức; chúng có thể trùng backbone xuất phát với dự án nhưng khác dữ liệu, objective, head và checkpoint cuối. So sánh phải chạy lại theo protocol chung, không so trực tiếp các số paper/model card. [[3]](#ref3) [[4]](#ref4) [[6]](#ref6)
- **DeBERTa-base trong bài 2605.26999:** đây là kết quả nghiên cứu từ encoder được fine-tune trên split trong bài. Trong lần kiểm tra nguồn này chưa xác minh được checkpoint detector công khai để tải; dùng metric của bài như y văn, không ghi thành một checkpoint chắc chắn chạy được. [[1]](#ref1)

## Nguyên tắc đối chiếu sau này

1. Chốt một test set và nhãn chung. Đối với detector nhị phân, có thể nghiên cứu mapping `Prompt Injection + Jailbreak → malicious`, nhưng báo rõ rằng phép gộp làm mất phân biệt lớp; không trộn với metric 3-class.
2. Dùng cùng văn bản đầu vào, preprocessing, split và hardware. Kiểm tra overlap/leakage với dữ liệu huấn luyện checkpoint tham khảo nếu thông tin có sẵn.
3. Tách model result cục bộ khỏi kết quả do paper/model card báo cáo; latency phải đo lại trên cùng môi trường.
4. Xác minh license, access gate, revision/checkpoint hash trước khi thực nghiệm; không giả định checkpoint còn truy cập được từ tên model.

## References

<a id="ref1"></a>**[1]** A. Akinrele and S. N. Gowda, “Prompt Injection Detection is Regime-Dependent: A Deployment-Aware Evaluation with Interpretable Structural Signals,” arXiv:2605.26999v1, 2026. [Full text](https://arxiv.org/html/2605.26999).

<a id="ref2"></a>**[2]** Microsoft, `microsoft/deberta-v3-base` model card. [Hugging Face](https://huggingface.co/microsoft/deberta-v3-base).

<a id="ref3"></a>**[3]** H. Li et al., “PIGuard: Prompt Injection Guardrail via Mitigating Overdefense for Free,” *ACL 2025*. [ACL Anthology](https://aclanthology.org/2025.acl-long.1468/).

<a id="ref4"></a>**[4]** Official PIGuard repository and training code. [GitHub](https://github.com/leolee99/PIGuard) · [`train.py`](https://github.com/leolee99/PIGuard/blob/main/train.py).

<a id="ref5"></a>**[5]** Meta, Prompt Guard 86M model card and model repository. [Model card](https://github.com/meta-llama/PurpleLlama/blob/main/Prompt-Guard/MODEL_CARD.md) · [Model](https://huggingface.co/meta-llama/Prompt-Guard-86M).

<a id="ref6"></a>**[6]** M. Jacob et al., “PromptShield: Deployable Detection for Prompt Injection Attacks,” *ACM CODASPY 2025* / arXiv:2501.15145. [Paper](https://arxiv.org/abs/2501.15145) · [Mã tác giả](https://github.com/wagner-group/PromptShield).
 
<a id="ref7"></a>**[7]** Meta, Llama Prompt Guard 2 86M / LlamaFirewall (arXiv:2505.03574). [Model card 86M](https://huggingface.co/meta-llama/Llama-Prompt-Guard-2-86M) · [Scanner source](https://github.com/meta-llama/PurpleLlama/tree/main/LlamaFirewall).
 
<a id="ref8"></a>**[8]** PI-Guard workspace, “Workspace provenance and metric audit — 2026-09-30.” [Local audit](../experiment_reports/WORKSPACE_PROVENANCE_AUDIT_2026-09-30.md).
