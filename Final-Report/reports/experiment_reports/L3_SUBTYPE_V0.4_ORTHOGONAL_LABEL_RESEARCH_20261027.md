# Nghiên cứu L3: chuyển sang nhãn PI/JB độc lập và đánh giá v0.4

**Ngày:** 27-10-2026  
**Trạng thái:** nghiên cứu nội bộ; chưa đủ điều kiện đăng ký runtime hoặc tuyên bố nghiệm thu  
**Câu hỏi:** giữ v0.3.23 và tiếp tục hiệu chỉnh ngưỡng, hay mở dòng v0.4 với hai mục tiêu `PI-present` và `JB-present`?

## 1. Scope Boundary Declaration

| Trong phạm vi | Ngoài phạm vi |
|---|---|
| Audit mục tiêu và nhãn của v0.3.23; kiểm tra nguồn dữ liệu PI/JB overlap; tái lập ngưỡng đa nguồn; fit ứng viên TF-IDF hai head độc lập (v0.4.7, v0.4.16–v0.4.24); sweep threshold, so sánh chính sách calibration, so sánh LinearSVC/LogisticRegression và audit nguồn mở; xác định contract và tiêu chí kiểm định API/dashboard. | Sửa API, dashboard, model registry hoặc model mặc định; mở locked-test payload; nhận điều khoản dataset thay người dùng; gọi nhãn synthetic hoặc source-proxy là human gold; triển khai/production acceptance. |

Không truy cập nguồn bị loại trừ `pids_bench_v3`. Run v0.4.16 chỉ dùng train/calibration/validation của v0.12.4; không đọc test payload trong fit hoặc chấm synthetic. Không sửa runtime hay default model.

## 2. Kết luận điều hành

Nên giữ v0.3.23 như baseline nhị phân `PI` đối `JB`, đồng thời phát triển v0.4 theo hai nhãn nhị phân độc lập. Không tạo v0.3.xxx chỉ để đổi ngưỡng nếu mục tiêu là phát hiện `BOTH`: một ngưỡng trên một decision margin chỉ chọn PI hoặc JB, không tạo thêm hai logit/score độc lập.

Đã fit mới các run `.4.16`–`.4.24` trên CPU. Các run `.4.16`–`.4.23` dùng hai LinearSVC heads word+char TF-IDF; `.4.24` so LogisticRegression hai head trên cùng TF-IDF/data/selection policy. `.4.20`–`.4.22` so class cost 4×/8×/16× balanced; `.4.23` chọn C theo recall tại FPR cap 1.5% thay AUROC nhưng không đổi validation. `.4.24` kém hơn: PI `12.21%/1.20%`, JB `25.70%/2.52%` recall/FPR, so với `.4.23` PI `21.47%/1.46%`, JB `29.72%/2.92%`. Tất cả ứng viên fail gate recall ≥0.80 và FPR ≤0.015. Ngay cả `.4.23` cap 10% cũng chỉ đạt recall PI `32.74%`, JB `72.61%`, với FPR `3.81%/12.14%`. Threshold/C selection và một linear estimator khác không khắc phục domain shift trong nhãn hiện tại. Không có ứng viên v0.4 đủ điều kiện đổi registry/default. Validation không có mẫu joint-known `10`, `01`, `11`, nên không thể ước lượng chất lượng route `BOTH`. Nhãn vẫn là source proxies/weak supervision; không có bộ adjudicated độc lập.

## 3. Vì sao v0.3.23 chỉ có PI và JB?

`v0.3.23/run_01/RUN_MANIFEST.json` khai báo task `attack_only_PI_vs_JB_binary`; dataset v0.3.17 có label schema `[PI, JB]`, 35,264 train rows và 1,344 validation rows. Train có 18,173 PI / 17,091 JB; validation có 1,027 PI / 317 JB. Bộ fit không có lớp Benign/Other/BOTH. Đây là lựa chọn task và nhãn khi tạo v0.3.17, không phải hành vi của thresholding.

Threshold validation đã đăng ký cho v0.3.23 là `-0.2522762685` trên PI decision score: PI nếu score ≥ threshold, ngược lại JB. Điểm này tối đa hóa macro-F1 dưới điều kiện recall mỗi lớp ≥0.80. Trên validation: PI recall 888/1,027 = 86.47%, JB recall 256/317 = 80.76%, macro-F1 0.8089. Không có xác suất hoặc lớp BOTH. Hai test suite ngoài nguồn đã từng được chấm trước đó, nên báo cáo v0.3.23 không phải đánh giá mù; chúng cũng không có benign để ước lượng benign FPR. Tình trạng trong registry vẫn là `RESEARCH_DIAGNOSTIC_NOT_ACCEPTED`.

Dataset các phiên bản sau dùng contract khác: `pi_present` và `jb_present` nhận `0`, `1`, hoặc `null`. Chỉ khi **cả hai bit đã biết** mới suy ra trạng thái `00`, `10`, `01`, `11`. `00` có nghĩa không có PI/JB theo nhãn được cấp; không đồng nghĩa nội dung vô hại. `null` không được biến thành 0. Vì vậy các nhãn `other`, `both` ở một thí nghiệm/dataset cũ không tự động trở thành output của v0.3.23.

PromptSentinel công bố ba lớp loại tấn công `benign`, `jailbreak`, `injection`; card cũng ghi direct harmful requests không có thủ thuật được gắn `benign` theo loại tấn công. Do đó mapping trong dataset v0.9.0 chỉ đặt bit loại được nêu thành 1 và để bit đối diện là unknown, thay vì tự suy ra `BOTH` hoặc một nhãn benign an toàn. [[170]](#ref170)

## 4. Dữ liệu và nguồn nhãn overlap

Dataset v0.9.0 có 100,730 train / 3,900 calibration / 2,476 validation rows. Train có 1,954 hàng joint-known `11`; đây là weak/source labels, gồm các dòng kế thừa từ dataset v0.8.0 và 32 prompt do assistant soạn đã được người dùng cho phép dùng làm weak supervision. Calibration có 3,900 hàng nhưng chỉ 2,930 joint-known `00`; validation có 2,476 hàng nhưng chỉ 2,242 joint-known `00`. Cả calibration và validation đều có **0** hàng joint-known `10`, `01`, hoặc `11`. Dataset manifest đánh dấu research-only, không phải gold và `production_qualified=false`.

PromptSentinel đã truy cập được trong phiên này và snapshot được pin tại revision `a932b3ef5982c97ec2c5c635bf61b9cbb4bd1a5b`. Dataset v0.9.0 lọc nguồn theo license từng hàng, dedupe exact/near, dùng nguồn train của PromptSentinel cho train và validation chính thức của họ cho calibration; test split không được đọc. Card mô tả split theo template family, nhưng split này không làm cho PromptSentinel calibration thành source-family-disjoint với PromptSentinel train. [[170]](#ref170)

Audit CORTYX phát hiện 6 dòng đồng thời có publisher tags `prompt_injection` và `jailbreak_attempt` trong snapshot 4,109 hàng. Đây là ứng viên review, không phải 6 nhãn PI/JB đã adjudicate. Phiếu review ghi từng prompt, candidate spans `[start,end)`, score và route theo v0.4.6. Bốn dòng không có phrase match JB rõ ràng theo quy tắc dò span; điều đó chỉ có nghĩa cần người duyệt, không chứng minh JB vắng mặt. Card nguồn ghi multi-label và CC BY 4.0. [[178]](#ref178)

Necent là nguồn đáng xem tiếp nhưng schema trong card không trực tiếp cung cấp hai bit PI/JB: `prompt_harmful` và `prompt_adversarial` phân biệt harmful content với adversarial behavior; `prompt_type` là một trường loại như jailbreak hoặc prompt_injection. Trang cũng yêu cầu chấp thuận điều kiện truy cập. Tôi chưa chấp thuận điều khoản thay người dùng và chưa dùng dữ liệu Necent. Link: [Necent/llm-jailbreak-prompt-injection-dataset](https://huggingface.co/datasets/Necent/llm-jailbreak-prompt-injection-dataset). [[191]](#ref191)

### 4.1 Nguồn mở bổ sung trong dataset v0.12.6

Quickium `train_nc` được pin tại revision `8d67314bd5c08497ed1f20a62009bec58e7c5eb0`; card ghi đây là split CC-BY-NC chỉ dùng phi thương mại, gồm WildJailbreak và WildGuardMix, không có evaluation split. Tôi chỉ lấy `train_nc`, deterministic-cap theo source/domain/label, rồi exact/near-deduplicate với `.12.5`; trong 51,633 dòng được xét, 18,245 exact và 81 near duplicates bị loại, còn 33,307 dòng được chia 24,982 train / 8,325 group-held-out calibration. [[192]](#ref192)

AI Mitra công bố 1,130 dòng train (860 prompt injection, 270 benign), MIT, synthetic/template-generated; card mô tả thêm một official test riêng gồm 57 dòng. Dataset `.12.6` chỉ dùng snapshot `data/train.jsonl`; test file không được tải vào snapshot nghiên cứu hoặc đọc. Sau lọc trùng và chia theo nhóm, các nhãn AI Mitra vẫn được giữ là source proxies, không phải human gold. [[193]](#ref193)

Hai nguồn mới không tạo thêm nhãn joint-known `11`: Quickium jailbreak rows gán `JB=1/PI=unknown`, Quickium injection và AI Mitra rows gán `PI=1/JB=unknown`, benign controls gán `00`. `.12.6` có 131,071 train / 14,604 calibration / 31,033 validation; validation được giữ nguyên từ `.12.5`, đã selection-exposed bởi `.4.16`. Dataset manifest SHA-256 `1c208adc0bf52fea5e2f6994bb2b50bf482d861a8ebb7f2a0c6745ad6b0cf0e8`; test payload flags false và `prohibited_source_input_accessed=false`.

### 4.2 Audit nguồn mở chưa được nhập

Đã rà soát thêm các card dataset công khai nhưng không nhập thêm dữ liệu. Smooth-3 có schema multi-label với các nhãn như `JAILBREAK` và `INSTRUCTION_OVERRIDE`, song card mô tả taxonomy dựa trên luật/heuristic; dữ liệu tổng hợp từ các nguồn thượng nguồn, trong đó có một bản Qualifire gated, và preview không cho lọc nguồn theo từng hàng. Vì vậy chưa đủ cơ sở chứng minh license/provenance theo từng hàng dù card aggregator khai báo Apache-2.0; không dùng trong train/evaluation. AIDataFdn dùng một trường category đơn, không phải hai bit PI/JB độc lập. NeurAlchemy cũng dùng một trường `category`; nguồn này đã được audit trong lineage PromptSentinel của `.12.6`, nhưng 4,809 dòng lineage được loại do license/provenance upstream không đủ rõ, nên không nhập lại. Horizon Eval Suite gộp PI và jailbreak thành một nhãn binary `injection-or-jailbreak`, không cung cấp target độc lập để kiểm tra BOTH. Necent phân biệt harmful-content với adversarial prompt cùng một trường prompt type và còn yêu cầu chấp thuận điều kiện; các trục đó không tương ứng trực tiếp với `PI-present`/`JB-present`. [[194]](#ref194) [[195]](#ref195) [[196]](#ref196) [[197]](#ref197) [[198]](#ref198) [[191]](#ref191)

## 5. Đánh giá ngưỡng và fit v0.4.7

### 5.1 v0.4.6: ngưỡng theo FPR đa nguồn

Đặt FPR cap 1.5% riêng trên PromptSentinel calibration và calibration v0.8.0 đã tái sử dụng; mỗi head lấy threshold lớn hơn của hai miền. Validation v0.8.0 đã được dùng cho chẩn đoán ứng viên trước đó nên kết quả mang tính exploratory.

| Head | Threshold thô | Validation TP / positives | Recall | FP / known negatives | FPR | AUROC |
|---|---:|---:|---:|---:|---:|---:|
| PI-present | 0.186622 | 111/158 | 70.25% | 27/2,242 | 1.20% | 0.9477 |
| JB-present | 0.461612 | 18/76 | 23.68% | 30/2,242 | 1.34% | 0.8451 |

Ngưỡng macro-F1 v0.4.6 cho JB recall cao hơn nhưng validation FPR của JB là 33.01%; không phù hợp operating point có FPR cap 1.5%. Kết quả chi tiết nằm trong `v0.4.6/research_runs/train_20261027_r01/METRICS.json`, `threshold_20261027_r01/METRICS.json` và `candidate_comparison_20261027_r01/CROSS_DOMAIN_CANDIDATES.csv`.

### 5.2 v0.4.7: fit lại điểm low-FPR cân bằng hơn

Sweep trọng số PromptSentinel chọn 0.2 trong các điểm đã thử. Fit v0.4.7 tạo vectorizer và hai head mới từ đầu trên train v0.9.0; hàng PromptSentinel có sample weight 0.2, hàng train hợp lệ khác weight 1. Hai threshold được chọn riêng trên từng head theo max recall tại FPR ≤1.5% trên hai calibration domains, sau đó đóng băng tại threshold lớn hơn giữa hai miền.

Cấu hình: LinearSVC `C=0.05`, `class_weight=balanced`; word TF-IDF n-grams `(1,2)` tối đa 20,000 features; `char_wb` n-grams `(3,5)` tối đa 30,000 features. Fit 133.9 giây. SHA-256 model `6bc3cfb6d6e8ff70a53053eed1afb07c4cbcc5b020c01a071233fc10e2c9a077`; dataset manifest SHA-256 `ffe485050b15a673061df0f2b495acf7511dd9d20cf7a98da9619c98ed5bd930`.

| Head | Threshold thô | Validation TP / positives | Recall | FP / known negatives | FPR | AUROC |
|---|---:|---:|---:|---:|---:|---:|
| PI-present | 0.267404 | 104/158 | 65.82% | 12/2,242 | 0.54% | 0.9688 |
| JB-present | 0.373621 | 25/76 | 32.89% | 31/2,242 | 1.38% | 0.8698 |

**Artifact:** `training/l3_subtype/versions/v0.4.7/run_01/METRICS.json`, `THRESHOLDS.json`, `RUN_MANIFEST.json`.

v0.4.7 tăng JB recall 9.21 điểm phần trăm so với v0.4.6 tại operating point đa nguồn; PI recall giảm 4.43 điểm. Tuy vậy, trọng số 0.2 đã được chọn dựa trên validation đã tái sử dụng. Đây không phải ước lượng độc lập của khả năng tổng quát hóa. Raw margins không phải xác suất.

Ở validation, v0.4.7 dự đoán route PI=39, JB=64, BOTH=85, NEITHER=2,288. Đây chỉ là số route model phát ra; vì nhãn đối diện của nhiều hàng là unknown và joint-known `11` bằng 0, các số này không đo precision/recall cho route BOTH.

### 5.3 Phiếu review synthetic đã được người dùng duyệt

Đã chấm lại 32 prompt synthetic đã được duyệt bằng v0.4.7, với exact spans và hai raw margins/threshold offsets cho từng prompt. Route in-sample: PI=9, JB=6, BOTH=5, NEITHER=12. Cả 32 prompt đã có mặt trong train, nên đây là phiếu xem nội dung/ngưỡng, không phải đánh giá mô hình. Phiếu để trống quyết định người duyệt: `v0.4.7/research_runs/both_prompt_review_20261027_r05/REVIEW.md`.

### 5.4 v0.4.16: fresh TF-IDF fit trên v0.12.4

Fit mới dùng word `(1,2)` và char_wb `(3,5)` TF-IDF cùng hai LinearSVC head độc lập; `C` được chọn riêng trên validation trong grid đã khai báo. Ngưỡng mỗi head lấy từ calibration theo từng domain với FPR cap 1.5%, rồi đóng băng ở ngưỡng domain lớn nhất. Không dùng validation để đổi threshold. Dataset có 103,966 train / 5,369 calibration / 31,033 validation rows; train có 1,954 joint-known `11`, còn validation có 0 joint-known `11`. Trọng số theo contract dữ liệu được giữ nguyên: PromptSentinel v2 0.2, các nguồn được gán trọng số tường minh 0.5, các hàng không có trọng số 1.0.

| Head | C | Threshold thô | Validation TP / positives | Recall | FP / known negatives | FPR | AUROC | Gate |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| PI-present | 1.0 | 0.844106 | 1,418/6,078 | 23.33% | 384/23,535 | 1.63% | 0.8233 | Fail |
| JB-present | 0.1 | 1.016994 | 392/1,420 | 27.61% | 559/23,535 | 2.38% | 0.9004 | Fail |

Theo nguồn, PI recall là 2.96% trên Horizon BIPIA (29/979 positive; FPR 0/30 negative) và 27.24% trên PromptSentinel v2 (1,389/5,099; FPR 384/23,083). JB recall là 26.94% trên Simsonsun (233/865; không có negative để tính FPR) và 28.65% trên PromptSentinel v2 (159/555; FPR 559/23,083). Đây là source-proxy metrics; validation được dùng chọn C nên không phải ước lượng test độc lập.

Đã chấm lại 32 prompt synthetic PI/JB/BOTH đã duyệt bằng model v0.4.16, kiểm tra lại từng span exact theo offset Unicode codepoint nửa mở. Route in-sample: PI=8, JB=1, BOTH=0, NEITHER=23; đề xuất gốc có 8 prompt mỗi route. Cả 32 prompt nằm trong train nên phiếu chỉ để người dùng duyệt nội dung/nhánh, không phải accuracy hay bằng chứng phát hiện BOTH. Phiếu đầy đủ prompt, evidence spans, margins và route: `training/l3_subtype/versions/v0.4.16/research_runs/both_prompt_review_20261027_r01/REVIEW.md`.

**Artifacts:** `training/l3_subtype/versions/v0.4.16/run_01/{model.joblib,METRICS.json,THRESHOLDS.json,RUN_MANIFEST.json,REPORT.md}`; model SHA-256 `ba9c3d8d5744c3598cb9c2735754dbb0e8d97a0122b9984426b824aac2a6c74b`; dataset manifest SHA-256 `d95e80fe287370d1edd7ff8b42e9c526d0ff181f6a82156f40f09c7eb0ecf2e6`. Artifact hashes khớp manifest, `test_payload_read=false`, và preflight ghi `prohibited_source_input_accessed=false`.

### 5.5 v0.4.17: ablation tăng positive class cost

Run `.4.17` giữ nguyên train `.12.4`, feature space và C của `.4.16`, chỉ tăng positive class cost lên 2× balanced. Đây là fresh fit, không phải tiếp tục từ checkpoint trước. PI đạt TP `1,378/6,078`, recall `22.67%`, FPR `1.51%`, AUROC `0.8194`; JB đạt TP `396/1,420`, recall `27.89%`, FPR `2.44%`, AUROC `0.8955`. Cả hai fail gate; tăng positive weight không cải thiện recall/FPR đồng thời. Model SHA-256 `c3cb4aeed2510d08fadff03d9e3355fb60c61a18172cca13bc6816ba722381c2`; dataset manifest SHA-256 vẫn `.12.4`.

### 5.6 v0.4.18: thêm Wambosec train rows

Run `.4.18` fresh-fit trên `.12.5`, giữ C và class-cost cố định để cô lập ảnh hưởng của Wambosec; chỉ dùng 2,123 hàng Wambosec train đã lọc, cùng 910 hàng group-held-out calibration. PI đạt recall `24.68%`, FPR `1.46%`, AUROC `0.8321`; JB đạt recall `29.08%`, FPR `2.58%`, AUROC `0.8973`. Cả hai vẫn fail gate. Không dùng Wambosec official test. Model SHA-256 `67b2a5cd30fb499b6fc916cd56d46ecee1156aff3f43d1231dcd045b0abea650`; dataset manifest SHA-256 `5b030ec170cb27fc61f8cec1b7ff418c4f763f35bc3dc02a488ad88c38b79422`.

### 5.7 v0.4.19: Quickium train_nc + AI Mitra train

Run `.4.19` fresh-fit trên `.12.6`, giữ feature space, C `PI=1.0/JB=0.1`, 2× positive class cost và sample weights `0.5` cho hai nguồn mới. Đây là TF-IDF/LinearSVC trên CPU, không phải DeBERTa. Calibration domain mới chỉ được dùng cho một head khi có ít nhất 30 held-out positives: Quickium bị loại khỏi PI threshold (10 positives), AI Mitra bị loại khỏi JB threshold (0 positives). PI dùng 5 calibration domains; JB dùng 5 domains khác.

| Head | Threshold thô | Validation TP / positives | Recall | FP / negatives | FPR | AUROC | Gate |
|---|---:|---:|---:|---:|---:|---:|---|
| PI-present | 1.195757 | 1,536/6,078 | 25.27% | 380/23,535 | 1.61% | 0.8299 | Fail |
| JB-present | 1.204785 | 426/1,420 | 30.00% | 649/23,535 | 2.76% | 0.8926 | Fail |

So với `.4.18`, recall tăng `0.59` điểm phần trăm cho PI và `0.92` điểm cho JB, trong khi FPR tăng `0.16` và `0.17` điểm; AUROC giảm nhẹ ở cả hai head. Nguồn bổ sung tạo 24,982 hàng train và 8,325 calibration, nhưng không tạo nhãn `BOTH` mới. Run manifest ghi fit mới, `test_payload_read=false`, `prohibited_source_input_accessed=false`, model SHA-256 `ac21f38e7a0e627987a8ded69d735d7db5716dfcf6f8585fabc89ee31a3c0d8d`, dataset manifest SHA-256 `1c208adc0bf52fea5e2f6994bb2b50bf482d861a8ebb7f2a0c6745ad6b0cf0e8`. Validation vẫn selection-exposed do các run trước, nên đây là kết quả exploratory.

### 5.8 Sweep ngưỡng calibration

Tôi đã chốt các ngưỡng chỉ trên calibration tại cap 0.5%, 1%, 1.5%, 2%, 3%, 5%, 10%; validation chỉ dùng để báo cáo trade-off và đã bị expose trước đó. Ở cap calibration 1.5%, validation recall/FPR là PI `25.27%/1.61%` và JB `30.00%/2.76%`. Ngay cả cap 10%, recall mới là PI `51.53%` với FPR `8.78%`, JB `74.58%` với FPR `11.62%`. Vì vậy threshold-only sweep không tìm được operating point đạt recall 80% cho cả hai head; mở locked test ở trạng thái này không có giá trị promotion.

**Phiếu review:** 32 prompt synthetic đã duyệt, được chấm bằng `.4.19` in-sample. Đề xuất ban đầu là 8 prompt mỗi route; model phát PI=6, JB=3, BOTH=2, NEITHER=21. Phiếu giữ exact evidence spans, offsets và hai threshold offsets: `training/l3_subtype/versions/v0.4.19/research_runs/both_prompt_review_20261027_r03/REVIEW.md`. Đây không phải accuracy hoặc đánh giá BOTH vì các prompt nằm trong train.

**Frontier artifact:** `training/l3_subtype/versions/v0.4.19/research_runs/threshold_frontier_20261027_r01/FRONTIER.md` cùng JSON/manifest. Ngưỡng tại cap 1.5% được assertion đối chiếu với run `.4.19`; script chỉ đọc calibration và validation, không đọc test.

### 5.9 v0.4.20–v0.4.22: ablation positive class cost

Ba run là fresh fit trên cùng `.12.6`, cùng word+char TF-IDF, cùng cách chọn C theo AUROC trên calibration source-specific và cùng ngưỡng cực đại qua bốn domain calibration cũ. Chỉ đổi positive class cost: 4× balanced ở `.20`, 8× ở `.21`, 16× ở `.22`. Calibration source-specific để chọn C (AI Mitra cho PI, Quickium cho JB) không được dùng để chọn threshold. Tất cả scores là raw margins, validation đã có lịch sử bị expose từ `.4.16`, và các nhãn vẫn là source proxies.

| Run | Head | Threshold | TP / positive | Recall | FP / negative | FPR | AUROC | Gate |
|---|---|---:|---:|---:|---:|---:|---:|---|
| `.4.20` | PI | 0.829174 | 1,228 / 6,078 | 20.20% | 266 / 23,535 | 1.13% | 0.8544 | Fail |
| `.4.20` | JB | 1.635242 | 380 / 1,420 | 26.76% | 704 / 23,535 | 2.99% | 0.8650 | Fail |
| `.4.21` | PI | 0.985814 | 1,285 / 6,078 | 21.14% | 318 / 23,535 | 1.35% | 0.8523 | Fail |
| `.4.21` | JB | 1.394922 | 407 / 1,420 | 28.66% | 622 / 23,535 | 2.64% | 0.8879 | Fail |
| `.4.22` | PI | 1.126576 | 1,305 / 6,078 | 21.47% | 344 / 23,535 | 1.46% | 0.8477 | Fail |
| `.4.22` | JB | 1.489864 | 422 / 1,420 | 29.72% | 688 / 23,535 | 2.92% | 0.8819 | Fail |

`.4.22` fit CPU trong 548.56 giây, selected C `PI=0.01/JB=0.1`, model SHA-256 `595ac94ebf34e01498f7aa3cce7bad49684abbd0e8842ce5d5ead243189dcf49`. `.4.21` có operating point cân bằng hơn về FPR so với `.4.22`; `.4.22` chỉ thêm 0.33 điểm recall PI và 1.06 điểm recall JB, trong khi FPR tăng 0.11 và 0.28 điểm, AUROC giảm. Kết quả này không ủng hộ tiếp tục tăng class cost. Cả ba run không thêm nhãn `BOTH`; mỗi run vẫn kế thừa 1,954 joint-known `11` weak labels từ train `.12.6`.

**Phiếu synthetic `.4.22`:** model phát PI=5, JB=3, BOTH=2, NEITHER=22 trên 32 prompt; đề xuất duyệt ban đầu là 8 prompt cho mỗi route. Phiếu `v0.4.22/research_runs/both_prompt_review_20261027_r06/REVIEW.md` chứa từng model input, exact evidence spans/offsets, raw margins, threshold offsets và nhánh dự đoán để người dùng duyệt. Cả 32 prompt có trong train, nên đây là in-sample review, không phải accuracy, human gold hoặc ước lượng hiệu quả BOTH.

**Threshold frontier `.4.22`:** `v0.4.22/research_runs/threshold_frontier_20261027_r04/FRONTIER.md` ghi sweep cap 0.5%–10%, thresholds chỉ chọn trên calibration. Ở cap 1.5%, metric khớp run: PI recall/FPR `21.47%/1.46%`, JB `29.72%/2.92%`. Ở cap 10%, PI `32.74%/3.81%`, JB `72.61%/12.14%`. Do đó đổi threshold trong các operating points đã khảo sát chưa đạt recall 80% với FPR tối đa 1.5%.

### 5.10 Độ nhạy với chính sách threshold gộp nguồn

Một phân tích độ nhạy trên model `.4.20` dùng threshold chọn từ dữ liệu calibration gộp qua bốn domain thay vì threshold lớn nhất theo từng domain. Trên validation, PI recall/FPR là `25.55%/1.99%`, JB `30.77%/3.43%`; recall tăng nhẹ nhưng FPR tăng và vượt cap. Max per-domain calibration FPR cũng lên `7.14%` cho PI và `1.71%` cho JB. Cách gộp này không phù hợp mục tiêu bảo vệ FPR xuyên nguồn và không thay đổi kết luận gate. Artifacts: `v0.4.20/research_runs/threshold_policy_sensitivity_20261027_r01/{FRONTIER.md,FRONTIER.json,MANIFEST.json}`.

### 5.11 v0.4.23: chọn C theo operating objective

Để kiểm tra liệu C selection theo AUROC có lệch khỏi mục tiêu vận hành, `.4.23` giữ nguyên train `.12.6`, TF-IDF, class cost 8×, threshold policy và hai calibration domain chọn C; chỉ chọn C theo maximum recall tại FPR ≤1.5%, tie-break bằng C nhỏ hơn. AI Mitra PI cho cùng recall 100%/FPR 0% ở C=.01, .1, 1 trên 221 positive/56 negative nên chọn C=.01; Quickium JB đạt recall 48.76%/FPR 1.47% ở C=.1 trên 3,944 positive/4,094 negative, cao nhất trong grid. AUROC chỉ lưu làm chẩn đoán.

Kết quả validation giữ nguyên so với `.4.22`: PI TP `1,305/6,078`, FPR `344/23,535` (`21.47%/1.46%` recall/FPR), AUROC `0.8477`; JB TP `422/1,420`, FPR `688/23,535` (`29.72%/2.92%`), AUROC `0.8819`. Model fit CPU 727.74 giây; SHA-256 `fb3c3e23d868fa917e13c374e98cc774f728af35f485b647c7197130b891f5f7`. Chọn C theo low-FPR recall trên calibration source-specific không chuyển thành cải thiện validation; ngưỡng/source shift và thiếu nhãn độc lập còn là giới hạn chính.

Lỗi validation lệch mạnh theo nguồn: PI trên Horizon BIPIA chỉ bắt `5/979` positives, còn PromptSentinel v2 bắt `1,300/5,099` với `344/23,083` false positives. JB bắt `246/865` trên Simsonsun (nguồn này không có negative để tính FPR) và `176/555` trên PromptSentinel v2, với `687/23,083` false positives. Đây là phân rã theo source-proxy validation, không phải causal attribution; `0/30` BIPIA negatives bị gắn cờ cũng không đủ để khẳng định FPR thực bằng 0.

Phiếu `.4.23` chấm lại 32 prompt in-sample: PI=5, JB=3, BOTH=2, NEITHER=22, có spans và threshold offsets cho người dùng duyệt tại `v0.4.23/research_runs/both_prompt_review_20261027_r07/REVIEW.md`. Frontier tại `v0.4.23/research_runs/threshold_frontier_20261027_r05/FRONTIER.md` khớp `.4.22`; ở cap 1.5% và 10% các metric không đổi. Không đọc test payload.

### 5.12 v0.4.24: LogisticRegression trên cùng TF-IDF

Run `.4.24` là fresh fit với LogisticRegression (`liblinear`, L2, `max_iter=1000`), giữ `.12.6`, word+char TF-IDF, 8× balanced positive cost, C grid, C-selection objective và threshold policy của `.4.23`. C được chọn `PI=.01/JB=10` theo recall tại FPR cap 1.5% trên AI Mitra/Quickium calibration holdouts. Validation PI TP `742/6,078`, FPR `282/23,535` (`12.21%/1.20%` recall/FPR), AUROC `0.8171`; JB TP `365/1,420`, FPR `592/23,535` (`25.70%/2.52%`), AUROC `0.8660`. Fit CPU trong 526.86 giây; model SHA-256 `adfbaea9211687bfae1d13d550098bd1e7c3b73bf997efafbbd4fdf194963c07`. Cả hai head kém hơn LinearSVC `.4.23` trên validation và fail gate.

Frontier `.4.24` xác nhận ở cap calibration 10% PI chỉ đạt recall/FPR `24.17%/3.94%`, JB `71.20%/13.26%`. Phiếu review 32 prompt in-sample phát PI=4, JB=4, BOTH=0, NEITHER=24: `v0.4.24/research_runs/both_prompt_review_20261027_r08/REVIEW.md`. Review không phải đánh giá BOTH; frontier và review không đọc test payload.

## 6. API, dashboard và data contract

Không có code API/dashboard được sửa trong nghiên cứu này. Hai runtime có default khác nhau, cần giữ tách biệt khi chọn model cho thử nghiệm:

| Runtime | L3 mặc định đã xác nhận |
|---|---|
| `runtime/` legacy | `hviet-tfidf-lr-20261019` trong `runtime/model_registry.json` |
| `l2l3/runtime/` | `l3-tfidf-linearsvc-v0.3.23` trong `l2l3/runtime/model_registry.json` |

Nghiên cứu ở đây bind trực tiếp artifact v0.3.23 và các fit v0.4.7/v0.4.16–v0.4.24; không lấy lựa chọn mặc định của dashboard làm bằng chứng về model đã được chấm. Runtime `l2l3` vẫn mặc định v0.3.23; chưa có artifact v0.4 nào đăng ký.

**Phạm vi thay đổi nếu mở implementation v0.4 sau khi có adjudication:**

| Thành phần | Contract cần hỗ trợ |
|---|---|
| API classify | Hai raw margins độc lập; threshold, `margin_minus_threshold`, quyết định mỗi bit; route `PI`, `JB`, `BOTH`, `NEITHER`; `scores_are_probabilities=false`; `model_id`, model SHA, dataset version, calibration policy/status. Thêm `context_segments` có `segment_id`, text và origin/trust metadata dưới contract versioned; giữ prompt/context riêng thay vì nối mất nguồn. |
| Cascade/chunk aggregation | Threshold từng bit trên score có cùng semantics với calibration; ghi supporting chunk riêng cho PI/JB, source segment và chunk index. Nếu PI và JB đến từ hai chunk khác nhau, vẫn ghi rõ cross-chunk support để review; không gán chúng thành cùng một span. |
| Review state | Trạng thái `NOT_CALIBRATED`, gần ngưỡng PI/JB, xung đột chunk, thiếu context và source/context chưa được đánh giá. Review band là vùng raw margin được hiệu chỉnh theo workload/error capture, không phải xác suất. |
| Explanation payload | Intercept, threshold offset, TF-IDF features đẩy về PI/JB, tổng feature đang hiển thị và remainder. Highlight chỉ dùng word features có source offsets đúng; character n-grams không được gán span giả. Offsets là Unicode codepoint half-open và gắn với segment gốc. |
| Dashboard | Hiển thị hai trục/head, bốn route, margin và threshold offset; phân biệt hỗ trợ trong cùng chunk với khác chunk; hiển thị feature contributions hai phía và trạng thái context. Giữ leave-one-sentence-out là perturbation độ nhạy; không diễn giải thành xác suất tấn công. |

API hiện tại nhận `prompt`, `l2_model_id`, `l3_model_id`; L3 v0.3.23 dùng một LinearSVC score PI-vs-JB và không trả xác suất. Dashboard `l2l3` đã có contributions TF-IDF, intercept, threshold offset, displayed contribution sum/remainder, word-span offsets và sentence perturbation; phần v0.4 phải mở rộng các mục đó cho hai head và giữ source offsets qua chunk/context. Các mô tả contribution chỉ giải thích score của mô hình, không chứng minh nguyên nhân tấn công.

## 7. Tiêu chí trước khi xem xét promotion

1. **Adjudication:** cùng một prompt và context được hai người gán riêng `PI-present` và `JB-present`; mỗi nhãn có thể `0/1/unknown`, có exact evidence spans và rationale. Bất đồng được adjudicate. Tách hành vi override/exfiltration (PI) khỏi hành vi vượt refusal/safety boundary (JB); không suy `BOTH` chỉ từ một nhãn publisher.
2. **Data provenance:** pin revision, license, source family, template/group ID, context origin và SHA-256. Split theo source family/template sao cho train, calibration, validation và locked test độc lập ở mức đã khai báo. Chỉ train được phép có weak labels; báo riêng human-adjudicated support.
3. **State coverage:** calibration, validation và locked test phải có joint-known `00`, `10`, `01`, `11`, gồm prompt-only và context-bearing cases. Báo confusion 4-state trên rows có cả hai bit known và metrics từng head trên mọi row có label cho head đó.
4. **Threshold policy:** chốt policy trước khi mở validation; chọn mỗi threshold chỉ trên calibration. Report recall, precision, FPR và support/denominator theo từng source family. Với mục tiêu FPR ≤1.5%, báo one-sided 95% confidence bound; 0 FP trên ít nhất 200 benign negatives mới cho upper bound xấp xỉ 1.49%, còn nếu có FP phải tăng support theo bound đã đăng ký.
5. **Locked test:** chọn một ứng viên sau validation, hash-bind model/dataset/threshold, rồi chấm test source-disjoint một lần; không tune từ test. Không mở test mới cho các candidate hiện có vì hai head chưa đạt recall/FPR gate và validation không thể đánh giá BOTH.
6. **Runtime readiness:** đo latency trên đúng API/cascade/chunk path (P95 <30 ms là mục tiêu dự án, chưa phải kết quả của nghiên cứu này), xác minh offsets/context coverage, review-state fallback và compatibility của API schema. Chỉ sau các gate này mới xem xét đổi registry/default.

## 8. Quyết định và artifacts

- Giữ v0.3.23 làm baseline PI-vs-JB; không diễn giải threshold `-0.2523` thành detector BOTH.
- Giữ v0.4.7 và v0.4.16–v0.4.24 là ứng viên nghiên cứu hai head; v0.4.24 là fit L3 TF-IDF mới nhất nhưng kém hơn LinearSVC `.4.23` và fail cả hai head gate. `.4.21` là điểm FPR/recall cân bằng hơn trong ablation class-cost `.20`–`.22`; chưa run nào promotion-ready. Không đăng ký candidate nào vào registry hoặc đổi dashboard default.
- Không tạo v0.3.xxx chỉ để “tìm threshold BOTH”. v0.4 là đúng hướng cho thay đổi semantics nhãn, nhưng chưa promotion-ready do thiếu adjudicated joint validation/test.
- Không mở locked test mới cho các candidate hiện có. Bước cần thiết tiếp theo là adjudication độc lập hai nhãn trên cùng prompt/context và source-held-out calibration/validation có đủ joint-known `00/10/01/11`; phiếu synthetic `.4.24` chỉ là tài liệu duyệt nội dung, không thay thế dữ liệu này. Không tiếp tục đổi C/threshold, class cost hay estimator nếu chưa có giả thuyết/nhãn mới.

Artifacts chính:

- v0.3.23: `training/l3_subtype/versions/v0.3.23/run_01/{RUN_MANIFEST.json,DECISION_RULE.json,VALIDATION_METRICS.json}`.
- Dataset v0.9.0: `shared_data/pi_guard_datasets/l3_subtype/versions/v0.9.0/{DATASET_MANIFEST.json,DATA_CONTRACT.json}`; datasets v0.12.4–v0.12.6: `shared_data/pi_guard_datasets/l3_subtype/versions/{v0.12.4,v0.12.5,v0.12.6}/{DATASET_MANIFEST.json,DATA_CONTRACT.json,SOURCE_PROVENANCE.json}`.
- Fit v0.4.7: `training/l3_subtype/versions/v0.4.7/run_01/{model.joblib,METRICS.json,THRESHOLDS.json,RUN_MANIFEST.json,REPORT.md}`.
- Fit v0.4.16: `training/l3_subtype/versions/v0.4.16/run_01/{model.joblib,METRICS.json,THRESHOLDS.json,RUN_MANIFEST.json,REPORT.md}`.
- Fits v0.4.17–v0.4.19: `training/l3_subtype/versions/{v0.4.17,v0.4.18,v0.4.19}/run_01/{model.joblib,METRICS.json,THRESHOLDS.json,RUN_MANIFEST.json,REPORT.md}`.
- Fits v0.4.20–v0.4.22: `training/l3_subtype/versions/{v0.4.20,v0.4.21,v0.4.22}/run_01/{model.joblib,METRICS.json,THRESHOLDS.json,RUN_MANIFEST.json,REPORT.md}`.
- Fit v0.4.23: `training/l3_subtype/versions/v0.4.23/run_01/{model.joblib,C_SELECTION.json,METRICS.json,THRESHOLDS.json,RUN_MANIFEST.json,REPORT.md}`.
- Fit v0.4.24: `training/l3_subtype/versions/v0.4.24/run_01/{model.joblib,C_SELECTION.json,METRICS.json,THRESHOLDS.json,RUN_MANIFEST.json,REPORT.md}`.
- v0.4.19 threshold frontier: `training/l3_subtype/versions/v0.4.19/research_runs/threshold_frontier_20261027_r01/FRONTIER.md`.
- v0.4.22 synthetic review/frontier: `training/l3_subtype/versions/v0.4.22/research_runs/{both_prompt_review_20261027_r06,threshold_frontier_20261027_r04}/`.
- v0.4.23 synthetic review/frontier: `training/l3_subtype/versions/v0.4.23/research_runs/{both_prompt_review_20261027_r07,threshold_frontier_20261027_r05}/`.
- v0.4.24 synthetic review/frontier: `training/l3_subtype/versions/v0.4.24/research_runs/{both_prompt_review_20261027_r08,threshold_frontier_20261027_r06}/`.
- v0.4.20 pooled-threshold policy sensitivity: `training/l3_subtype/versions/v0.4.20/research_runs/threshold_policy_sensitivity_20261027_r01/`.
- Threshold/candidate comparison: `training/l3_subtype/versions/v0.4.6/research_runs/{threshold_20261027_r01,candidate_comparison_20261027_r01,train_ablation_20261027_r02}/`.
- CORTYX span audit: `training/l3_subtype/versions/v0.4.6/research_runs/open_source_audit_20261027_r03/REVIEW.md`.
- 32 prompt synthetic đã duyệt: `training/l3_subtype/versions/v0.4.7/research_runs/both_prompt_review_20261027_r05/REVIEW.md`.
- Phiếu review 32 prompt synthetic theo v0.4.16: `training/l3_subtype/versions/v0.4.16/research_runs/both_prompt_review_20261027_r01/REVIEW.md`.
- Phiếu review 32 prompt synthetic theo v0.4.19: `training/l3_subtype/versions/v0.4.19/research_runs/both_prompt_review_20261027_r03/REVIEW.md`.

## References

<a id="ref170"></a>
170. Hugging Face, *PromptSentinel*, accessed 2026-10-27. [Dataset card](https://huggingface.co/datasets/nuhmanpk/prompt-sentinel).

<a id="ref178"></a>
178. QuantaSparkLabs, *CORTYX Safety Dataset*, Hugging Face, accessed 2026-10-27. [Pinned dataset card](https://huggingface.co/datasets/QuantaSparkLabs/cortyx-safety-dataset/tree/abac2c21250510993025796f6f29a7b3cecf6147).

<a id="ref191"></a>
191. Necent, *LLM Jailbreak & Prompt-Injection Dataset card*, Hugging Face, accessed 2026-10-27. [Dataset card and access conditions](https://huggingface.co/datasets/Necent/llm-jailbreak-prompt-injection-dataset).

<a id="ref192"></a>
192. Quickium, *Prompt Security v0*, Hugging Face, snapshot `8d67314bd5c08497ed1f20a62009bec58e7c5eb0`, accessed 2026-10-27. [Pinned dataset card](https://huggingface.co/datasets/quickium/prompt-security-v0/tree/8d67314bd5c08497ed1f20a62009bec58e7c5eb0).

<a id="ref193"></a>
193. AI Mitra, *Prompt Injection Dataset*, Hugging Face, snapshot `82baf561be4496f6e38620d33fe9ffdfc7d8d706`, accessed 2026-10-27. [Pinned dataset card](https://huggingface.co/datasets/ai-mitra/prompt-injection-dataset/tree/82baf561be4496f6e38620d33fe9ffdfc7d8d706).

<a id="ref194"></a>
194. Smooth-3, *LLM Prompt Injection Attacks*, Hugging Face, snapshot `dd47798b64ebf0e833ecdbff6b1d73be3e440581`, accessed 2026-10-27. [Pinned dataset card](https://huggingface.co/datasets/Smooth-3/llm-prompt-injection-attacks/tree/dd47798b64ebf0e833ecdbff6b1d73be3e440581).

<a id="ref195"></a>
195. rogue-security, *Prompt Injections Benchmark*, Hugging Face, accessed 2026-10-27. [Dataset card and access status](https://huggingface.co/datasets/rogue-security/prompt-injections-benchmark).

<a id="ref196"></a>
196. AIDataFdn, *Prompt Injection Dataset*, Hugging Face, accessed 2026-10-27. [Dataset card](https://huggingface.co/datasets/AIDataFdn/promptinjection).

<a id="ref197"></a>
197. NeurAlchemy, *Prompt Injection & Jailbreak Detection Dataset*, Hugging Face, accessed 2026-10-27. [Dataset card](https://huggingface.co/datasets/neuralchemy/Prompt-injection-dataset).

<a id="ref198"></a>
198. Horizon-Labs, *Prompt Injection Eval Suite*, Hugging Face, revision `27c7bcd6f46e842f4c4d8b114b30eb6b1d892965`, accessed 2026-10-27. [Pinned dataset card](https://huggingface.co/datasets/Horizon-Labs/prompt-injection-eval-suite/tree/27c7bcd6f46e842f4c4d8b114b30eb6b1d892965).
