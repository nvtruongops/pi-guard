# 05 — Backbone DeBERTa của đồ án và bốn model đối chuẩn

## Scope Boundary Declaration

- **Nguồn nhiệm vụ:** [TASK.md](TASK.md), Review 1 lần 2, 2026-10-01.
- **IN-SCOPE:** chốt backbone đề xuất cho classifier L3 của đồ án; lập danh sách bốn detector DeBERTa-family có thể thử đối chuẩn; ghi rõ taxonomy/nguồn và giới hạn.
- **OUT-OF-SCOPE:** tải/huấn luyện model; gọi metric paper là metric PI-Guard; so sánh các model trên dữ liệu hoặc label space không tương thích.

## Câu trả lời: backbone đồ án là gì?

**Đề xuất dùng `microsoft/deberta-v3-base` làm pretrained backbone cho classifier L3 của đồ án.** Model card của Microsoft mô tả đây là model pretrained tổng quát cho fill-mask; nó chưa được huấn luyện riêng để phát hiện prompt injection. Vì vậy mô hình đồ án cần một sequence-classification head và fine-tuning trên dữ liệu đã gắn nhãn của PI-Guard. Nếu taxonomy đồ án là `Benign / Prompt Injection / Jailbreak`, head của model đồ án phải được huấn luyện theo ba lớp đó. [[1]](#ref1)

**Meta Prompt Guard không phải lựa chọn thay cho base này.** `meta-llama/Prompt-Guard-86M` là detector đã fine-tune trên backbone multilingual `mDeBERTa-v3-base`, được phát hành làm checkpoint dùng phân loại prompt. Nó phù hợp vai trò baseline đối chuẩn, không phải checkpoint trắng cho classifier của đồ án. Model có access gate và điều khoản riêng cần rà soát trước khi dùng. [[2]](#ref2)

## Vai trò của L3 trong luồng quyết định

L3 nhận các chunk được L2 gắn route REVIEW, tokenize/chia window nếu cần, rồi trả score và nhãn theo chunk; L3 không phát route REVIEW. API áp dụng ngưỡng/quy tắc đã validation, kiểm tra đủ coverage và kết thúc request bằng ALLOW hoặc BLOCK. REVIEW không phải trạng thái chờ hoặc yêu cầu duyệt thủ công; nó chỉ định tuyến chunk từ L2 sang L3. [[2]](#ref2) [Middleware source](../../src/api/middleware.py)

## Bốn ứng viên đối chuẩn sau này

| # | Checkpoint/model | Backbone / trạng thái | Nhãn và khả năng so sánh | Vai trò đề xuất |
|---|---|---|---|---|
| 1 | [Meta Prompt Guard 86M](https://huggingface.co/meta-llama/Prompt-Guard-86M) | mDeBERTa-v3-base; detector đã fine-tune; truy cập có gate. | Benign / injection / jailbreak; gần taxonomy đồ án nhất. | Baseline đa lớp chính nếu truy cập/điều khoản cho phép. [[2]](#ref2) |
| 2 | [PIGuard](https://huggingface.co/leolee99/PIGuard) | `microsoft/deberta-v3-base` + head và cách huấn luyện MOF; official repo công bố code, data và weights. | Code training khai báo 2 output labels; paper đánh giá over-defense trên các tập riêng. Không phải head 3 lớp của đồ án. | Baseline nghiên cứu DeBERTa/MOF; so sánh trên protocol và label mapping chung. [[3]](#ref3) [[4]](#ref4) |
| 3 | [PromptShield DeBERTa](https://github.com/wagner-group/PromptShield) | Fine-tuned từ `microsoft/deberta-v3-base`; paper CODASPY 2025 [[5]](#ref5) và mã fine-tuning công khai. | Phân loại benign / malicious; tối ưu hóa để triển khai thực tế. | Baseline nghiên cứu DeBERTa-v3-base có paper học thuật và mã nguồn fine-tuning của nhóm tác giả (Wagner group). [[5]](#ref5) |
| 4 | [Llama Prompt Guard 2 86M](https://huggingface.co/meta-llama/Llama-Prompt-Guard-2-86M) | mDeBERTa-base; detector đã fine-tune trong LlamaFirewall (Meta, 2025) [[6]](#ref6). | Benign / malicious nhị phân; cùng kích cỡ backbone 86M như Prompt Guard v1 (khác bản 22M dùng DeBERTa-xsmall). | Baseline đối chuẩn cập nhật từ Meta trên backbone mDeBERTa-base 86M. [[6]](#ref6) |

### Model tham khảo trong bài 2605.26999

Bài báo fine-tune DeBERTa-base làm sequence classifier và báo cáo kết quả paper-matched theo các regime của bài. Dùng nó để tham khảo thiết kế/metric trong y văn; trong lần kiểm tra nguồn hiện tại chưa xác minh được một checkpoint công khai có tên sẵn để tải lại đúng model/split của tác giả. Không tính đây là baseline có thể chạy ngay cho PI-Guard. [[7]](#ref7)

## Cách so sánh công bằng ở bước sau

- So sánh mô hình đồ án và bốn checkpoint trên cùng held-out prompts, text normalization, chunking policy, hardware và latency harness.
- Báo cáo taxonomy gốc của từng checkpoint. Nếu dùng binary track, định nghĩa trước cách gộp `Prompt Injection` và `Jailbreak` thành `malicious`; không đối chiếu trực tiếp binary F1 với 3-class Macro-F1.
- Dùng model card/paper metrics để mô tả nguồn tham khảo; metric đối chuẩn của đồ án phải được chạy lại cục bộ, cùng protocol.
- Ghi model revision, label mapping, checkpoint hash và access/license khi thực nghiệm được phê duyệt ở milestone phù hợp.

## References

<a id="ref1"></a>**[1]** Microsoft, `microsoft/deberta-v3-base` model card. [Hugging Face](https://huggingface.co/microsoft/deberta-v3-base).

<a id="ref2"></a>**[2]** Meta, Prompt Guard 86M model card/repository. [Model card](https://github.com/meta-llama/PurpleLlama/blob/main/Prompt-Guard/MODEL_CARD.md) · [Checkpoint](https://huggingface.co/meta-llama/Prompt-Guard-86M).

<a id="ref3"></a>**[3]** H. Li et al., “PIGuard: Prompt Injection Guardrail via Mitigating Overdefense for Free,” *ACL 2025*. [ACL Anthology](https://aclanthology.org/2025.acl-long.1468/).

<a id="ref4"></a>**[4]** Official PIGuard repository and training code. [GitHub](https://github.com/leolee99/PIGuard) · [`train.py`](https://github.com/leolee99/PIGuard/blob/main/train.py).

<a id="ref5"></a>**[5]** M. Jacob et al., “PromptShield: Deployable Detection for Prompt Injection Attacks,” *ACM CODASPY 2025* / arXiv:2501.15145. [Paper](https://arxiv.org/abs/2501.15145) · [Mã tác giả](https://github.com/wagner-group/PromptShield).

<a id="ref6"></a>**[6]** Meta, Llama Prompt Guard 2 86M / LlamaFirewall (arXiv:2505.03574). [Model card 86M](https://huggingface.co/meta-llama/Llama-Prompt-Guard-2-86M) · [Scanner source](https://github.com/meta-llama/PurpleLlama/tree/main/LlamaFirewall).

<a id="ref7"></a>**[7]** A. Akinrele and S. N. Gowda, “Prompt Injection Detection is Regime-Dependent: A Deployment-Aware Evaluation with Interpretable Structural Signals,” arXiv:2605.26999v1, 2026. [Full text](https://arxiv.org/html/2605.26999).
