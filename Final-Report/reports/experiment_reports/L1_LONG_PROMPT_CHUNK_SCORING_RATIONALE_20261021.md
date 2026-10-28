# Lập luận L1 — chấm L2 DeBERTa theo nhiều chunk cho prompt dài

**Ngày:** 2026-10-21  
**Trạng thái:** Cơ sở tài liệu và cấu hình runtime research-candidate; chưa phải kết quả thực nghiệm về hiệu quả PI-Guard.  
**Phạm vi:** L2 DeBERTa và L3 TF-IDF + Logistic Regression xử lý một prompt dài như một session gồm nhiều chunk. Không huấn luyện model hoặc hiệu chuẩn threshold multi-chunk trong thay đổi này.

## 1. Tóm tắt lập luận

Runtime L2 hiện tính hiệu giữa logit Attack và logit Benign trên một lần suy luận; tokenizer cắt input theo max_length 512. Vì vậy nội dung sau 512 token không tham gia điểm L2 hiện tại. Có thể giữ nguyên encoder đã huấn luyện, chấm từng cửa sổ 512 token, rồi lấy điểm margin lớn nhất làm điểm prompt:

\[
s_i = z_{\mathrm{attack},i} - z_{\mathrm{benign},i},
\qquad
S_K(x) = \max_{1 \le i \le K(x)} s_i,
\qquad
\widehat{y}(x) =
\begin{cases}
\mathrm{Attack}, & S_K(x) \ge T_{K(x)}\\
\mathrm{Benign}, & S_K(x) < T_{K(x)}.
\end{cases}
\]

Trong đó \(K(x)\) là số chunk sau khi token hóa và áp dụng overlap; mỗi chunk có tối đa 512 token tính cả special token. Công thức này là một phép gộp theo giả định multiple instance: prompt có thể bị gắn cờ nếu ít nhất một chunk có bằng chứng tấn công đủ mạnh. Đây là **đề xuất cho PI-Guard**, lấy cảm hứng từ các nghiên cứu xử lý văn bản dài, không phải công thức đã được các bài báo xác nhận cho phát hiện prompt injection.

## 2. Trạng thái runtime L2 hiện tại

Trong [cài đặt L2](../../../workspaces/truongnv/pi_guard_l2_deberta_gate_tfidf_subtype/runtime/l2_deberta.py), hàm score token hóa một prompt với truncation bật, dùng max_length của registry, rồi trả về logit lớp Attack trừ logit lớp Benign. [Registry runtime](../../../workspaces/truongnv/pi_guard_l2_deberta_gate_tfidf_subtype/runtime/model_registry.json) đặt max_length là 512 và ghi rõ runtime hiện chưa chia hoặc gộp chunk. [Cascade](../../../workspaces/truongnv/pi_guard_l2_deberta_gate_tfidf_subtype/runtime/cascade.py) so điểm này với threshold đã đăng ký.

Do đó, với prompt dài hơn cửa sổ, điểm hiện tại là điểm của phần được tokenizer giữ lại; nó không phải điểm đã tổng hợp toàn prompt. Khi \(K=1\) và giữ nguyên model/tokenizer/window, \(S_1\) trùng score hiện tại. Với \(K \ge 2\), phép lấy cực đại làm thay đổi phân phối điểm nên threshold hiện hành không thể mặc nhiên áp dụng.

## 3. Bằng chứng tài liệu và giới hạn áp dụng

### 3.1 Bằng chứng gần với phép gộp đề xuất

Gomes, Coutinho và Martins (EACL 2024) nghiên cứu phân loại mã ICD trên hồ sơ xuất viện dài. Trong Chunk Encoding, họ chia tài liệu thành các đoạn, chạy GatorTron riêng trên từng chunk có tối đa 512 token, tạo logits từng chunk rồi max-pool theo trục chunk. Bài báo dùng cửa sổ chồng lấn 255 token để giảm nguy cơ cắt đứt văn bản liên kết ở ranh giới chunk [[68]](#ref68).

Khác biệt cần giữ rõ: paper gộp logits theo lớp qua các chunk; công thức PI-Guard ở đây trước tiên tính margin Attack trừ Benign riêng cho từng chunk rồi mới lấy max của các margin. Đây là phép chuyển thiết kế phù hợp với score hiện tại của L2, không phải phép toán trùng hệt với mô hình trong paper.

Trên MIMIC-III-50, biến thể Chunk Encoding (CE) báo cáo macro/micro F1 lần lượt 65.5/70.0, so với baseline xử lý 512 token đầu (BM) 49.1/56.1. Trên MIMIC-III-clean, CE đạt 16.9/52.1 so với BM 11.0/44.5 [[68]](#ref68). Đây là bằng chứng thực nghiệm rằng một pipeline encoder theo chunk có max-pooling có thể hữu ích cho phân loại tài liệu dài trong tác vụ đó.

Giới hạn quan trọng: paper phân loại mã y khoa đa nhãn, không phân loại prompt injection; biến thể CE khác baseline ở cách bao phủ tài liệu và một số thành phần kiến trúc. Vì vậy các chênh lệch trên không cô lập tác động nhân quả của riêng phép max-pooling và không dự đoán recall, Benign FPR hay precision của PI-Guard.

Paper cũng cảnh báo max-pooling có thể làm xác suất lớp bị đánh giá quá cao và làm giảm calibration trong thiết lập của họ [[68]](#ref68). Với PI-Guard, đây là lý do phải hiệu chuẩn lại threshold trên điểm prompt-level theo đúng cấu hình chunk; không dùng trực tiếp threshold single-window hiện tại.

### 3.2 Đối chiếu với noisy-or

Wang, Li và Metze (Interspeech 2018) so sánh max pooling với noisy-or trong multiple-instance learning cho nhận dạng lời nói và phát hiện sự kiện âm thanh. Họ báo cáo max pooling định vị được phoneme/sự kiện trong các thí nghiệm đó, còn noisy-or thất bại; phân tích của họ lưu ý các instance trong chuỗi có tương quan, trong khi noisy-or thường dựa trên diễn giải xác suất độc lập [[69]](#ref69).

Đây là bằng chứng nền tảng từ miền âm thanh, không phải bằng chứng trực tiếp cho văn bản hoặc L2 PI-Guard. Noisy-or cũng không áp dụng trực tiếp lên raw logit margin \(s_i\), vì margin không phải xác suất. Nếu muốn thử noisy-or, cần xác định phép chuyển sang xác suất và kiểm định giả định phụ thuộc giữa các cửa sổ chồng lấn.

## 4. Vì sao chọn max margin làm ứng viên

- **Bảo toàn tín hiệu ngắn, nằm sâu trong prompt:** một chunk có điểm Attack cao không bị trung bình hóa với nhiều chunk Benign.
- **Tránh suy luận trên prompt siêu dài:** L2 chạy một lần cho mỗi chunk; không cần ghép các chunk thành input vượt giới hạn rồi gọi L2 lần nữa.
- **Có vị trí để báo cáo:** runtime có thể trả chunk đạt max, khoảng token/ký tự và điểm của chunk đó. Đây là vị trí nhạy nhất theo score L2, không phải phân bổ chính xác “bao nhiêu điểm” cho câu đó.
- **Chi phí tăng theo số cửa sổ:** với \(K\) chunk, cần \(K\) lượt mã hóa (có thể batch trên phần cứng phù hợp). Overlap tăng số token được xử lý và số cơ hội phát sinh false positive.

Max pooling không phải lựa chọn tối ưu cho mọi tác vụ. Mean pooling có thể phù hợp khi nhãn phụ thuộc bằng chứng phân tán trên toàn tài liệu, nhưng có thể làm loãng một đoạn tấn công ngắn. Với giả định PI-Guard rằng một đoạn riêng lẻ có thể đủ để gắn cờ prompt, max là ứng viên hợp lý để đưa vào so sánh.

## 5. Hiệu chuẩn threshold theo số chunk

Gọi \(T_k\) là threshold cho prompt có \(k\) chunk. Chọn \(T_k\) trên **prompt Benign thuộc validation**, sau khi chạy đúng tokenizer, kích thước cửa sổ, overlap và cách xác định \(k\) sẽ dùng khi triển khai:

\[
T_k = Q_{1-\alpha}
\left(\left\{S_{K(x)}(x) :
x \in \mathcal{V}_{\mathrm{Benign}},\ K(x)=k\right\}\right),
\]

trong đó \(\alpha\) là mục tiêu Benign FPR và \(Q\) là quantile thực nghiệm theo protocol đã định trước. Nếu dữ liệu validation không đủ cho từng \(k\), cần gộp thành các bucket độ dài được định trước và báo cáo FPR riêng theo bucket; không tuyên bố đạt FPR theo từng \(k\) khi cỡ mẫu không hỗ trợ.

Lý do cần bước này: nếu false-positive event của mỗi chunk độc lập với xác suất \(p\), xác suất ít nhất một chunk vượt threshold là \(1-(1-p)^k\). Công thức này chỉ minh họa hiệu ứng tăng cơ hội báo động; các chunk có overlap tương quan nên không dùng biểu thức độc lập để tự đặt threshold. Cách phù hợp cho phép đo là tính \(S_K\) trên từng prompt Benign hoàn chỉnh và chọn threshold ở cấp prompt.

Với \(K \ge 2\), không dùng threshold \(T_1\) hiện tại trên \(S_K\) nếu chưa hiệu chuẩn. Việc chọn threshold phải chỉ dùng validation, đóng băng trước test; test độc lập chỉ dùng để báo cáo kết quả cuối. Mục tiêu FPR dưới 1.5% của đề tài là KPI cần kiểm chứng, không phải kết quả được suy ra từ paper.

## 6. Protocol kiểm chứng PI-Guard đề xuất

1. **Đóng băng cấu hình:** phiên bản L2, tokenizer revision, 512 token gồm special token, overlap cụ thể, quy tắc chia tại ranh giới câu nếu có, số chunk tối đa được hỗ trợ và cách xử lý phần cuối.
2. **So sánh trên cùng prompt:** baseline hiện tại lấy 512 token đầu; max margin với không overlap; max margin với overlap. Bao gồm prompt có 1, 2 và 3 chunk; với dữ liệu dài hơn, ghi rõ bucket \(K\) thực tế.
3. **Bố trí payload:** payload ở đầu, giữa, cuối; sát trước/sau ranh giới chunk; một đoạn tấn công ngắn nằm trong văn bản Benign dài; các prompt Benign dài có cấu trúc, trích dẫn hoặc hướng dẫn hợp lệ.
4. **Hiệu chuẩn:** xác định \(T_k\) hoặc bucket threshold trên validation Benign theo cùng cấu hình. Lưu số prompt và số chunk trong từng bucket để lượng giá độ bất định.
5. **Báo cáo test ở đơn vị prompt:** confusion matrix, Attack Recall, Benign FPR, predicted-Attack precision, khoảng tin cậy và latency P50/P95; đối chiếu mục tiêu latency P95 dưới 30 ms. Không tính từng chunk như một quan sát độc lập khi báo cáo metric prompt-level.
6. **Tiêu chí quyết định:** giữ phương án chỉ khi nó cải thiện phát hiện payload nằm ngoài 512 token đầu trong khi đạt mục tiêu Benign FPR đã xác định trên test khóa; nêu rõ thay đổi chi phí suy luận do số chunk và overlap.

Không truy cập nguồn dữ liệu bị loại trừ theo chính sách nguồn của dự án. Mọi tập validation/test cho nghiên cứu này cần có manifest, provenance và nhãn được xác nhận độc lập trước khi dùng.

## 7. Kết luận có thể bảo vệ

**Literature fact:** encoder theo chunk với max-pooling đã được dùng thành công trong phân loại tài liệu dài ở một miền khác; overlap được dùng để giảm rủi ro biên chunk [[68]](#ref68). Kết quả được công bố không chứng minh L2 prompt injection.

**PI-Guard design proposal:** lấy max của các chunk margin \(z_{\mathrm{attack}}-z_{\mathrm{benign}}\), kèm threshold hiệu chuẩn từ validation theo số chunk/độ dài. Công thức này hợp với giả định “một đoạn tấn công đủ để gắn cờ cả prompt” và tránh trung bình hóa mất tín hiệu cục bộ.

**Empirical status:** chưa có phép đo hiệu quả PI-Guard cho prompt dài hơn 512 token. Runtime smoke check trên prompt tổng hợp chỉ xác nhận chunking, routing và phép tính; nó không đo recall, Benign FPR hay precision. Chỉ sau khi chạy protocol ở Mục 6 mới được kết luận công thức có hiệu quả và đạt KPI FPR của dự án.

## 8. Cấu hình session L2→L3 trong runtime

Một lần gọi `/api/classify` tạo một `session_id` tạm thời; prompt không được ghi vào file hoặc log. Tokenizer của L2 tạo các chunk tối đa 512 token tính cả special token, chồng lấn 64 token nội dung. Runtime giữ score, số token và khoảng ký tự cho từng chunk trong cùng session.

Với \(s_i = z_{\mathrm{attack},i} - z_{\mathrm{benign},i}\), runtime tính \(S_{L2} = \max_i s_i\). Nếu \(S_{L2}\) thấp hơn threshold đăng ký, API trả ALLOW_CANDIDATE và bỏ qua L3. Nếu bất kỳ chunk nào đạt threshold, API trả REVIEW_TO_L3; chỉ các chunk vượt threshold được đưa qua L3. Đây là luồng kiểm thử nhãn, không gọi model downstream và không tự phát lệnh chặn.

L3 là Logistic Regression nhị phân trên TF-IDF. Với mỗi chunk L2 được chuyển tiếp, margin của lớp dương trong model hiện pin là \(m_i = f_{JB,i} - f_{PI,i} = b + \sum_j x_{ij}w_j\). Feature \(x_{ij}w_j\) là đóng góp chính xác vào margin chunk đó; runtime trả top feature, intercept và sai số tái dựng. Để tạo nhãn session, runtime lấy \(G_{JB}=\max_i m_i\) và \(G_{PI}=\max_i(-m_i)\) trên các chunk được chuyển tiếp, rồi chọn lớp có support lớn hơn. Đóng góp feature được giải thích theo từng chunk; không cộng chúng thành điểm chính xác cho toàn session.

**Giới hạn threshold:** runtime đang dùng threshold single-window hiện có để minh họa routing; khi session có nhiều chunk, response và dashboard đánh dấu trạng thái not_calibrated_for_multi_chunk_sessions. Ngưỡng \(T_k\) theo bucket số chunk ở Mục 5 vẫn là bước cần hiệu chuẩn trên validation session-level trước khi đánh giá hiệu quả. L3 giữ trạng thái external diagnostic, output margin không phải xác suất đã hiệu chuẩn.

Cấu hình nằm tại [registry](../../../workspaces/truongnv/pi_guard_l2_deberta_gate_tfidf_subtype/l2l3/runtime/model_registry.json), [L2 chunk scorer](../../../workspaces/truongnv/pi_guard_l2_deberta_gate_tfidf_subtype/l2l3/runtime/l2_deberta.py), [cascade/session router](../../../workspaces/truongnv/pi_guard_l2_deberta_gate_tfidf_subtype/l2l3/runtime/cascade.py), [L3 margin explainer](../../../workspaces/truongnv/pi_guard_l2_deberta_gate_tfidf_subtype/l2l3/runtime/l3_hviet.py) và [dashboard](../../../workspaces/truongnv/pi_guard_l2_deberta_gate_tfidf_subtype/l2l3/runtime/dashboard.py). Kiểm tra prompt tổng hợp 1/2/3 chunk bằng `python runtime/check_chunked_session.py`; kiểm tra hash bundle bằng `python verify_bundle.py`.

## Tài liệu tham khảo

- [[68]](#ref68) Gomes, Coutinho, and Martins (2024), EACL. [Trang ACL Anthology](https://aclanthology.org/2024.eacl-long.141/) · [PDF Open Access](../../References/Gomes_2024_Accurate_Well_Calibrated_ICD_Chunk_Encoding_EACL.pdf).
- [[69]](#ref69) Wang, Li, and Metze (2018), Interspeech. [Trang ISCA Archive](https://www.isca-archive.org/interspeech_2018/wang18_interspeech.html) · [PDF Open Access](../../References/Wang_Li_Metze_2018_Max_Noisy_Or_Pooling_Interspeech.pdf).
