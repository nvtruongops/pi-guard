# Review 1 lần 2 — mô hình ingress và hồ sơ nghiên cứu

**Cập nhật:** 2026-10-02  
**Task boundary:** [TASK.md](TASK.md)

## Mô hình đề xuất hiện tại

```text
User prompt / upload
  → L1: trích xuất, chuẩn hóa, chia chunk và giữ source map
  → L2: TF-IDF + Logistic Regression, chấm từng chunk và tạo đúng 3 route
       ├─ ALLOW candidate: fast-pass candidate sau khi cutoff được validation
       ├─ REVIEW: chỉ chuyển chunk vùng giữa sang L3; không phải trạng thái HOLD
       └─ BLOCK candidate: chặn sớm chỉ sau khi cutoff được validation
  → L3: DeBERTa-v3-base phân loại chunk REVIEW; trả score/nhãn về API
  → API tổng hợp coverage; kết quả request cuối chỉ là ALLOW hoặc BLOCK
  → chỉ ALLOW gọi target LLM; stream phản hồi tới dashboard
```

`microsoft/deberta-v3-base` là backbone tiền huấn luyện tổng quát, không phải detector prompt injection có sẵn. Đồ án dự kiến thêm classification head và huấn luyện/fine-tune theo nhãn, dữ liệu và protocol của mình. Bài arXiv 2605.26999 dùng TF-IDF + Logistic Regression làm lexical baseline, đồng thời fine-tune DeBERTa-base như một encoder baseline; bài không kiểm nghiệm đúng cascade TF-IDF → DeBERTa của PI-Guard. [[1]](#ref1) [[2]](#ref2)

Meta Prompt Guard 86M, PIGuard, PromptShield DeBERTa và Llama Prompt Guard 2 86M là các detector đã được huấn luyện để **đối chuẩn ở bước đánh giá sau**. Meta Prompt Guard không phải backbone thay thế cho `microsoft/deberta-v3-base`; nó là classifier đã fine-tune trên mDeBERTa-v3-base. Nhãn, ngôn ngữ và điều khoản truy cập khác nhau nên cần protocol chung trước khi so sánh. [[3]](#ref3) [[4]](#ref4) [[6]](#ref6)

## Hợp đồng chunk và luồng backend

L1/L2/L3 là module nội bộ của FastAPI. Orchestrator truyền object Python/Pydantic trong cùng process: `CanonicalTextEnvelope` → `ChunkRouteResult[]` → `RoutedChunk[]` (chỉ band giữa) → `WindowPrediction[]` → API aggregation. Không có REST nội bộ hoặc queue giữa các tầng; chỉ L1 nhận file bytes, còn L2/L3 nhận text chunk và metadata.

Kích thước chunk và n-gram là hai tham số khác nhau. L1 dùng **ứng viên** 256 DeBERTa-token/chunk, overlap 32; validation sweep target `{128,256,384}` × overlap `{0,32,64}`. Backbone có giới hạn 512 model positions, tính cả special tokens. Các giá trị chunk là cấu hình để kiểm định, chưa phải khuyến nghị được paper chứng minh.

L2 baseline bám paper là word TF-IDF unigram/bigram `(1,2)`, tối đa 20.000 terms + Logistic Regression. Character `char_wb (3,5)` là ablation riêng, chưa có bằng chứng paper cho cấu hình/cascade này. Chi tiết tool calls, hợp đồng DTO, lỗi và protocol chống rò rỉ dữ liệu nằm trong [07](07_CHUNKING_AND_BACKEND_HANDOFF_DESIGN.md).

## Ngưỡng L2: căn cứ và giới hạn

Bài 2605.26999 có khảo sát phân vùng confident-benign / uncertain / confident-harmful theo **điểm của mô hình ngữ nghĩa**, cùng quy trình chọn threshold trên validation. Kết quả routing/hybrid thay đổi theo benchmark và không chứng minh fast-pass/block của TF-IDF→DeBERTa sẽ tốt hơn. Do đó sơ đồ giữ ba vùng `τ_allow` / vùng giữa / `τ_block` như **cấu trúc cần kiểm định**, không gán số hoặc tuyên bố paper đã xác nhận ngưỡng cho đồ án. Khi xây dựng mô hình, chọn ngưỡng trên validation; nếu chưa được kiểm định thì không bật shortcut và cho toàn bộ chunk đi qua L3 trong chế độ đánh giá. [[1]](#ref1)

Phân tích riêng tại [06](06_TFIDF_THRESHOLD_ROUTING_PAPER_AUDIT.md) xác nhận paper có chọn một cutoff nhị phân cho từng classifier trên validation và có ba vùng selective routing trên semantic score; paper không công bố cặp cutoff số cho TF-IDF và không thử tuyến TF-IDF→DeBERTa. Có thể kế thừa protocol validation-only rồi hiệu chỉnh cutoff của PI-Guard trên validation riêng, không chuyển số paper hoặc dùng test để chọn ngưỡng. [[1]](#ref1)

Ở L2, Logistic Regression học trọng số từ TF-IDF và nhãn train; `predict_proba` cho score `p_attack` mỗi chunk. Hai cutoff hậu huấn luyện tạo ba route: ALLOW candidate, REVIEW→L3, BLOCK candidate. Chọn cutoff bằng validation theo mục tiêu attack escape/FPR rồi đóng băng trước test. Không cần classifier riêng để chia route. REVIEW chỉ là điều phối nội bộ sang L3; API không giữ request chờ người duyệt. Chi tiết protocol nằm trong [02](02_TIER1_LOGREG_VS_LINEARSVC.md). [[1]](#ref1) [[8]](#ref8) [[9]](#ref9)

## File trong bộ báo cáo

| File | Nội dung |
|---|---|
| [01_TWO_TIER_CASCADE_EVIDENCE.md](01_TWO_TIER_CASCADE_EVIDENCE.md) | Bài báo hỗ trợ điều gì về TF-IDF, threshold và selective routing; điều gì chưa được chứng minh. |
| [02_TIER1_LOGREG_VS_LINEARSVC.md](02_TIER1_LOGREG_VS_LINEARSVC.md) | Lý do chọn Logistic Regression làm baseline; vị trí của LinearSVC trong ablation. |
| [03_RESEARCH_SOURCE_PROVENANCE.md](03_RESEARCH_SOURCE_PROVENANCE.md) | Nguồn gốc bài báo, model card, code/checkpoint và giới hạn sử dụng. |
| [04_REVIEW1_DEFENSE_KEY_NOTES.md](04_REVIEW1_DEFENSE_KEY_NOTES.md) | Luận điểm ngắn để bảo vệ cấu trúc tầng, threshold và quyết định API. |
| [05_DEBERTA_REFERENCE_MODELS.md](05_DEBERTA_REFERENCE_MODELS.md) | Backbone đồ án và bốn mô hình DeBERTa-family đối chuẩn cho giai đoạn sau. |
| [06_TFIDF_THRESHOLD_ROUTING_PAPER_AUDIT.md](06_TFIDF_THRESHOLD_ROUTING_PAPER_AUDIT.md) | Paper dùng threshold/routing nào; dữ liệu paper; cách chọn và kiểm định hai cutoff L2 của PI-Guard. |
| [07_CHUNKING_AND_BACKEND_HANDOFF_DESIGN.md](07_CHUNKING_AND_BACKEND_HANDOFF_DESIGN.md) | Đơn vị chunk/n-gram, cấu hình ứng viên, giới hạn token DeBERTa, tool calls và DTO nội bộ giữa L1/L2/L3. |
| [08_PI_JB_ATTACK_TAXONOMY_MATRIX.md](08_PI_JB_ATTACK_TAXONOMY_MATRIX.md) | Ma trận Direct PI / Indirect PI / Jailbreak; hai benchmark tham chiếu chính, nguồn Direct PI bổ trợ, giới hạn so sánh và quy tắc gán nhãn. |
| [Sơ đồ Draw.io](REVIEW1_PROPOSED_INGRESS_ML_ARCHITECTURE.drawio) | 8 trang: tổng quan chi tiết; tổng quan dọc; L1/L2/L3+API tối giản ở trang 3–5; L1/L2/L3+API chi tiết có tool calls/setup ở trang 6–8. |

## Phân định trạng thái

- **Y văn:** bài báo dùng TF-IDF + Logistic Regression, DeBERTa-base và đánh giá theo regime/threshold. [[1]](#ref1)
- **Bằng chứng cục bộ:** các báo cáo hiện có không đo cascade đầu-cuối hoặc routing có điều kiện. [[5]](#ref5)
- **Đề xuất đồ án:** ba route L2 là ALLOW candidate / REVIEW→L3 / BLOCK candidate; L3 phân loại chunk được chuyển; API kết thúc request bằng ALLOW hoặc BLOCK. Đây là kiến trúc đề xuất, chưa phải kết quả cascade đã đo.
- **Luồng quyết định:** REVIEW chỉ là tín hiệu định tuyến nội bộ từ L2 sang L3, không phải quyết định cuối, trạng thái chờ hay yêu cầu duyệt thủ công. L3 trả score/nhãn; API kiểm tra coverage và tổng hợp thành ALLOW/BLOCK. Lỗi kỹ thuật trả lỗi fail-closed riêng, không mặc định benign.
- **Fast path:** chỉ bật ALLOW/BLOCK shortcut sau khi cutoff qua validation. Trước validation, chuyển toàn bộ chunk qua L3 để đo; chưa có cơ sở tuyên bố cascade hiện nhanh hơn.
- **Đối chiếu code hiện tại:** endpoint inspect còn gọi một classifier trên toàn prompt; chunk routing, quyết định cuối ALLOW/BLOCK và token streaming trong sơ đồ là đề xuất, chưa phải hiện trạng. [[7]](#ref7)

## Hiện trạng mã nguồn và trạng thái các tool trong sơ đồ

`POST /v1/chat/guardrail` hiện nhận prompt JSON; `main.py` khởi tạo `MockLLMProvider` mặc định. Source hiện không có `UploadFile`, `MAX_UPLOAD_BYTES`, bộ trích xuất PDF hay Tesseract OCR. Vì vậy `request_validator.py`, `pdf_extract.py`, `ocr.py`, `docx_extract.py`, `train_l2.py`, `load_l3_model.py` và `api_orchestrator.py` trong sơ đồ là **module/call đề xuất**, chưa phải file đã triển khai. Giới hạn upload được để dạng `MAX_UPLOAD_BYTES` chưa gán số; không có mức MB được xác nhận.

`BaseLLMProvider.generate(prompt, system_prompt)` hiện trả về một chuỗi hoàn chỉnh; `main.py` đang dùng mock provider. Luồng external LLM sau ALLOW là thiết kế đề xuất. Token streaming cần provider adapter hỗ trợ stream và chưa được nối vào API hiện tại. Xem [src/api/main.py](../../src/api/main.py), [src/api/middleware.py](../../src/api/middleware.py), [src/api/schemas.py](../../src/api/schemas.py) và [src/llm/provider.py](../../src/llm/provider.py).

## References

<a id="ref1"></a>**[1]** A. Akinrele and S. N. Gowda, “Prompt Injection Detection is Regime-Dependent: A Deployment-Aware Evaluation with Interpretable Structural Signals,” arXiv:2605.26999v1, 2026. [Full text](https://arxiv.org/html/2605.26999).

<a id="ref2"></a>**[2]** Microsoft, `microsoft/deberta-v3-base` model card. [Hugging Face](https://huggingface.co/microsoft/deberta-v3-base).

<a id="ref3"></a>**[3]** Meta, Prompt Guard 86M model card. [Model card](https://github.com/meta-llama/PurpleLlama/blob/main/Prompt-Guard/MODEL_CARD.md) · [Checkpoint](https://huggingface.co/meta-llama/Prompt-Guard-86M).

<a id="ref4"></a>**[4]** H. Li et al., “PIGuard: Prompt Injection Guardrail via Mitigating Overdefense for Free,” ACL 2025; and official code/checkpoint repository. [ACL paper](https://aclanthology.org/2025.acl-long.1468/) · [GitHub](https://github.com/leolee99/PIGuard).

<a id="ref5"></a>**[5]** PI-Guard workspace, “Workspace provenance and metric audit — 2026-09-30.” [Local audit](../experiment_reports/WORKSPACE_PROVENANCE_AUDIT_2026-09-30.md).

<a id="ref6"></a>**[6]** PI-Guard workspace, “DeBERTa reference model candidates.” [05_DEBERTA_REFERENCE_MODELS.md](05_DEBERTA_REFERENCE_MODELS.md).

<a id="ref7"></a>**[7]** PI-Guard current source: [`main.py`](../../src/api/main.py), [`middleware.py`](../../src/api/middleware.py), and [`provider.py`](../../src/llm/provider.py).

<a id="ref8"></a>**[8]** scikit-learn, “Tuning the decision threshold for class prediction.” [User guide](https://scikit-learn.org/stable/modules/classification_threshold.html).

<a id="ref9"></a>**[9]** scikit-learn, “Probability calibration.” [User guide](https://scikit-learn.org/stable/modules/calibration.html).

<a id="ref10"></a>**[10]** F. Perez and I. Ribeiro, “Ignore Previous Prompt: Attack Techniques For Language Models,” ML Safety Workshop at NeurIPS 2022. [arXiv](https://arxiv.org/abs/2211.09527) · PDF cục bộ: `References/Perez_2022_Ignore_This_Title_Hack_This_Paper_Prompt_Injection.pdf`.

<a id="ref11"></a>**[11]** J. Yi et al., “Benchmarking and Defending Against Indirect Prompt Injection Attacks on Large Language Models,” KDD 2025, DOI `10.1145/3690624.3709179`. [Toàn văn/metadata](https://arxiv.org/html/2312.14197) · PDF cục bộ: `References/Viet_2024_BIPIA_Benchmarking_Indirect_Prompt_Injection_Attacks.pdf`. Reference log hiện ghi sai venue/năm; xem [ma trận 08](08_PI_JB_ATTACK_TAXONOMY_MATRIX.md#source-provenance).

<a id="ref12"></a>**[12]** P. Chao et al., “JailbreakBench: An Open Robustness Benchmark for Jailbreaking Large Language Models,” NeurIPS 2024, Datasets and Benchmarks Track. [Proceedings](https://proceedings.neurips.cc/paper_files/paper/2024/hash/63092d79154adebd7305dfd498cbff70-Abstract-Datasets_and_Benchmarks_Track.html) · [Open PDF](https://arxiv.org/pdf/2404.01318.pdf) · PDF cục bộ: `References/Chao_2024_JailbreakBench_Open_Robustness_Benchmark_NeurIPS.pdf`.
