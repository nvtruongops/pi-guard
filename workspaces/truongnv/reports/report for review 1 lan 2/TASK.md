# Task — Review 1 lần 2: chốt mô hình ingress và sơ đồ đề xuất

**Nguồn giao việc:** các chỉ đạo của người dùng trong session Review 1 lần 2, cập nhật ngày 2026-10-02.

## Scope Boundary Declaration

| IN-SCOPE | OUT-OF-SCOPE |
|---|---|
| Tóm tắt căn cứ dùng `TF-IDF + Logistic Regression` ở L2; xác định `microsoft/deberta-v3-base` là backbone dự kiến cho classifier đồ án ở L3; liệt kê bốn detector DeBERTa-family làm đối chuẩn tương lai; ghi giới hạn bằng chứng cho selective routing; đồng bộ README và báo cáo 01–06 theo ranh giới route L2/L3/API; audit cách paper dùng threshold/routing và ghi protocol validation để chọn hai cutoff PI-Guard; cập nhật overview và các trang chi tiết trong file Draw.io hiện tại. | Huấn luyện hoặc triển khai cascade; cài parser/dependency; đưa ngưỡng số chưa hiệu chỉnh; tuyên bố metric/latency cascade đã đạt; thay đổi backend/API; sửa tài liệu tham chiếu master; đưa nội dung ngoài phạm vi dự án vào kiến trúc. |

## Bổ sung theo yêu cầu sơ đồ 4 trang

| IN-SCOPE | OUT-OF-SCOPE |
|---|---|
| Đảm bảo đúng thứ tự 4 trang: Tổng quan → L1 ingress → L2 TF-IDF + Logistic Regression → L3 DeBERTa/API/LLM/dashboard; đổi trang tiền xử lý hiện có từ Tầng 0 thành chi tiết L1; giữ nguyên canvas và tọa độ đã chỉnh; làm rõ vùng từng tầng, tool-call, dữ liệu vào/ra, xử lý chunk/window, lỗi và nhánh ALLOW/REVIEW/BLOCK. | Tạo trang bổ sung thứ năm (ranh giới này được mở rộng theo yêu cầu mới ở cuối task); đổi kích thước/scale/tọa độ của overview; thêm dependency hoặc sửa backend; gán số cho hai cutoff chưa validation; mô tả luồng đề xuất như tính năng đã triển khai. |

### Checklist cập nhật sơ đồ

- [x] Giữ trang 1 là tổng quan và đủ đúng 4 trang; đặt tên ba trang còn lại L1, L2, L3.
- [x] Chuyển trang Tầng 0 hiện có thành L1 ingress/tiền xử lý, đổi hợp đồng đầu ra thành `CanonicalTextEnvelope` cho L2.
- [x] Làm rõ cutoff L2 theo đúng ba khoảng `p_attack ≤ τ_allow`, `τ_allow < p_attack < τ_block`, `p_attack ≥ τ_block`.
- [x] Bổ sung/kiểm tra tool-call, source map, window coverage, lỗi fail-closed, API aggregation và đường chỉ-ALLOW tới LLM streaming.
- [x] Xác minh XML Draw.io hợp lệ, tên/trật tự trang chính xác và toàn bộ geometry hiện hữu không đổi.
- [x] Đồng bộ mô tả sơ đồ trong README và TASK.

## Bàn giao

- [x] Ghi rõ baseline L2 là TF-IDF + Logistic Regression theo bài arXiv 2605.26999; LinearSVC chỉ là lựa chọn ablation riêng.
- [x] Phân biệt backbone DeBERTa-v3-base của đồ án với các detector DeBERTa đã fine-tune dùng để đối chuẩn.
- [x] Đánh giá paper support cho chia vùng ngưỡng; không chuyển ngưỡng/metric paper sang PI-Guard.
- [x] Giải thích hai ngưỡng là cutoff hậu huấn luyện trên `p_attack`, được chọn bằng validation; không phải classifier riêng.
- [x] Cập nhật sơ đồ một trang overview hiện có, giữ nguyên kích thước/vị trí; thêm trang chi tiết L2 và trang L3 → API → LLM/dashboard.
- [x] Ghi tool-call/đầu vào/đầu ra theo chunk và lối thoát lỗi cho từng tầng.
- [x] Tách route REVIEW→L3 ở L2 khỏi quyết định request cuối; bỏ trạng thái REVIEW/HOLD chờ xử lý thủ công.
- [x] Đồng bộ README và báo cáo 01–07: ba route L2 là ALLOW candidate / REVIEW→L3 / BLOCK candidate; API cuối chỉ phát ALLOW hoặc BLOCK.
- [x] Kiểm tra XML Draw.io, nhãn trang, liên kết nội bộ và nguồn tham khảo.
- [x] Tạo báo cáo 06 phân biệt ngưỡng nhị phân TF-IDF + Logistic Regression với ba vùng semantic routing; ghi cách chọn hai cutoff PI-Guard trên validation mà không sao chép số paper.

## Bổ sung theo yêu cầu chunking và hợp đồng backend

| IN-SCOPE | OUT-OF-SCOPE |
|---|---|
| Thể hiện L1/L2/L3 là module nội bộ FastAPI và ghi rõ DTO/đối tượng Python đi qua từng handoff; chi tiết bước trích xuất file, giới hạn bytes/tokens cấu hình, chunk/window, tool-call TF-IDF/LR, n-gram baseline theo paper và ablation có nhãn; nêu 512 model positions của DeBERTa và đánh dấu kích thước chunk/overlap là ứng viên cần validation. | Sửa backend hoặc cài parser; cố định giới hạn upload/chunk/cutoff thành thông số đã đo; khẳng định char n-gram hoặc cascade có cải thiện; triển khai REST nội bộ/message queue, model training, benchmark hoặc streaming thật. Không đưa INT8, ONNX Runtime, ZeroQuant, white-box steering, KV-cache hay multimodal vào phương án. |

### Checklist chi tiết chunk và handoff

- [x] Tách rõ token budget của chunk ở L1 với `ngram_range` của feature ở L2.
- [x] Ghi cấu hình ứng viên chunk 256/overlap 32, grid validation 128/256/384 × 0/32/64 và giới hạn model 512; không xem ứng viên là kết quả paper.
- [x] Ghi baseline paper word `(1,2)`/20k và gắn `char_wb (3,5)` là ablation dự án chưa kiểm chứng.
- [x] Ghi rõ `CanonicalTextEnvelope` → `ChunkRouteResult` → `RoutedChunk` (band giữa) → `WindowPrediction` bằng lời gọi cùng process; không giả định microservice/queue.
- [x] Cập nhật trang chi tiết L1/L2/L3, README và tạo ghi chú về cấu hình/giới hạn bằng chứng.
- [x] Xác minh XML, đúng bốn trang và geometry/canvas không đổi.

## Bổ sung theo yêu cầu xử lý connector bị chồng — 2026-10-02

Yêu cầu mới của người dùng ưu tiên khả năng đọc sơ đồ và **ghi đè ràng buộc giữ tọa độ thẻ** trong checklist cũ. Vẫn giữ bốn trang và canvas/scale; được phép đổi tọa độ thẻ, kích thước vùng, thứ tự hiển thị và waypoint connector để tránh đường xuyên qua thẻ, chồng đường, hoặc nằm ngoài canvas. Không thay đổi mô hình, cutoff, hợp đồng dữ liệu hay nội dung nghiên cứu.

| IN-SCOPE | OUT-OF-SCOPE |
|---|---|
| Tái cấu trúc hiển thị connector trên cả bốn trang; vẽ region nền trước, connector sau, nội dung thẻ trên cùng; sửa waypoint và bố trí card nơi đường giao cắt; đưa toàn bộ thành phần trong canvas; giữ đủ nội dung và đúng thứ tự trang. | Đổi số trang/canvas scale; xóa nội dung mô hình; thay đổi đề xuất thuật toán/ngưỡng; thêm backend/dependency; tạo số liệu. |

### Checklist hiển thị

- [x] Đọc edge/node geometry cả bốn trang và xác định đường ngoài canvas/xuyên card.
- [x] Sắp thứ tự vẽ region → connector → card/icon/label để line không phủ chữ.
- [x] Tái bố trí overview trong canvas; reroute L1 parser fan-in và L3/API/decision branches.
- [x] Xác minh đúng bốn trang/canvas, đường không cắt qua thẻ không liên quan, waypoint nằm trong canvas và không còn tuyến ngoài trang bằng kiểm tra XML/hình học.
- [x] Gửi yêu cầu mở file Draw.io trong panel Codex; lệnh được nhận ở trạng thái queued để mở khi thread hiện lên.

## Quy tắc quyết định

L2 phát score và đúng ba route state theo chunk: ALLOW candidate, REVIEW→L3, BLOCK candidate. REVIEW chỉ có nghĩa chuyển chunk vùng giữa sang L3; không phải kết quả request cuối hoặc trạng thái chờ người duyệt. L3 trả score/nhãn; API kiểm tra coverage, tổng hợp request và chỉ phát ALLOW hoặc BLOCK. Chỉ ALLOW gọi LLM. Cho tới khi cutoff được đánh giá trên validation, fast-pass/direct-block chưa bật; không gán ngưỡng số hay tuyên bố đã đo được tăng tốc.

## Bổ sung căn tiêu đề vùng và nới khoảng cách thẻ — 2026-10-02

| IN-SCOPE | OUT-OF-SCOPE |
|---|---|
| Căn tiêu đề mọi scope/lane lên đầu khung trên cả bốn trang; dành dải tiêu đề rõ ràng; tăng khoảng cách các thẻ và nhánh đang sát nhau; cập nhật waypoint bị ảnh hưởng. | Đổi nội dung mô hình, số trang, canvas/scale, cutoff, hợp đồng dữ liệu hoặc thêm tính năng triển khai. |

### Checklist bố cục

- [x] Căn tiêu đề region/lane về phía trên và thống nhất padding tiêu đề trên bốn trang.
- [x] Tạo khoảng trống giữa tiêu đề L2 và ba nhánh kết quả; nới khe các thẻ L2, API và footer đang sát nhau.
- [x] Cập nhật waypoint liên quan tới các thẻ đã di chuyển; giữ nguyên nội dung và thứ tự bốn trang.
- [x] Xác minh XML, giới hạn canvas, thứ tự trang và hình học sau chỉnh sửa.

## Bổ sung tách route candidate và quyết định request — 2026-10-02

**Căn cứ rà soát:** [README.md](README.md), [01_TWO_TIER_CASCADE_EVIDENCE.md](01_TWO_TIER_CASCADE_EVIDENCE.md), [06_TFIDF_THRESHOLD_ROUTING_PAPER_AUDIT.md](06_TFIDF_THRESHOLD_ROUTING_PAPER_AUDIT.md), [07_CHUNKING_AND_BACKEND_HANDOFF_DESIGN.md](07_CHUNKING_AND_BACKEND_HANDOFF_DESIGN.md).

| IN-SCOPE | OUT-OF-SCOPE |
|---|---|
| Bỏ đoạn giải thích cutoff dài khỏi thẻ score tổng quan; thể hiện ba route L2: ALLOW candidate, REVIEW→L3, BLOCK candidate; chỉ có ALLOW/BLOCK là kết quả cuối của API; thể hiện prediction L3 quay về API aggregation. | Đổi mô hình hoặc ngưỡng; bật shortcut chưa validation; để L2/L3 phát quyết định request cuối; thay đổi backend hoặc tuyên bố kết quả cascade đã đo. |

### Checklist luồng quyết định

- [x] Thẻ score overview chỉ nêu score/route; trang L2 có ba nhánh ALLOW candidate, REVIEW→L3 và BLOCK candidate.
- [x] API chỉ phát ALLOW/BLOCK sau aggregation; không có REVIEW/HOLD chờ xử lý thủ công.
- [x] L3 có nhánh benign/pass-candidate và attack/block-candidate; cả hai trả prediction về API, không bypass coverage/aggregation.
- [x] Xác minh bốn trang, XML/canvas, không chồng thẻ và các connector mới không cắt thẻ/nhau.

## Bổ sung một điểm giao L2–API–L3 — 2026-10-02

**Quy ước luồng:** L2 trả đúng một ChunkRouteResult[] cho API, với ba route state cho từng chunk: ALLOW candidate, REVIEW→L3, BLOCK candidate. API chuyển chunk REVIEW sang L3; giữ candidate thấp/cao để aggregation. Khi cutoff chưa validation, chuyển tất cả chunk qua L3. L3 không phát route state; API kết thúc request bằng ALLOW hoặc BLOCK. Không có REVIEW/HOLD ở đầu ra caller/dashboard.

### Checklist connector

- [x] Trang tổng quan chỉ còn một connector trực tiếp L2 → API mang toàn bộ kết quả/route-candidate.
- [x] Connector API router → L3 thể hiện dispatch cùng process; không còn đường bypass API từ L2 sang L3.
- [x] L3 detail gọi rõ input là chunk do API route từ L2 chuyển tới.
- [x] REVIEW chỉ là route L2→L3; API final decision chỉ gồm ALLOW hoặc BLOCK.
- [x] Kiểm tra XML, connector endpoint/waypoint, số trang và canvas sau chỉnh sửa.

## Bổ sung thứ tự 5 trang — 2026-10-02

Yêu cầu này thay thế ranh giới sơ đồ 4 trang ở phần trên. Giữ nội dung chi tiết hiện có; tạo bản kiến trúc tối giản từ trang tổng quan rồi đặt nó ở vị trí thứ hai.

| IN-SCOPE | OUT-OF-SCOPE |
|---|---|
| Thứ tự cuối: (1) mô hình 3 tầng chi tiết, (2) mô hình 3 tầng tối giản chỉ có tiêu đề/chức năng/luồng, (3) L1 chi tiết, (4) L2 chi tiết, (5) L3 chi tiết. Cập nhật tên trang, README và kiểm tra XML/geometry. | Tạo trang thứ sáu; xóa hoặc rút gọn ba trang chi tiết; thêm nội dung ghi chú/đánh giá vào trang tối giản; thay đổi mô hình, cutoff, backend hoặc kết quả nghiên cứu. |

### Checklist thứ tự và trang tóm tắt

- [x] Giữ trang 1 là mô hình 3 tầng chi tiết.
- [x] Tạo trang tối giản rồi sắp xếp trang đó ở vị trí thứ 2.
- [x] Giữ L1, L2, L3 lần lượt ở trang 3, 4, 5.
- [x] Trang tối giản chỉ có tiêu đề, chức năng các thành phần và connector luồng.
- [x] Đồng bộ README và TASK với thứ tự 5 trang.
- [x] Xác minh XML hợp lệ, đúng thứ tự trang, kích thước canvas và không chồng thẻ/connector.

## Bổ sung sửa ngữ nghĩa REVIEW — 2026-10-02

Yêu cầu mới thay thế các mô tả REVIEW/HOLD trước đó. REVIEW là trạng thái định tuyến nội bộ của L2, chỉ dùng để chuyển chunk vùng giữa sang L3. Mô hình không giữ prompt chờ người xử lý thủ công và không phát pending/request_id cho một hàng chờ reviewer.

| IN-SCOPE | OUT-OF-SCOPE |
|---|---|
| Đồng bộ 5 trang Draw.io, README và báo cáo 01–07 theo ba route L2 ALLOW / REVIEW→L3 / BLOCK; API phát quyết định request cuối ALLOW hoặc BLOCK; loại bỏ mọi card/line/diễn giải REVIEW-HOLD thủ công. | Sửa backend; bật shortcut chưa validation; đặt ngưỡng số; tuyên bố latency hoặc cải thiện cascade chưa đo. |

### Checklist ngữ nghĩa và kết quả cuối

- [x] REVIEW xuất hiện như route L2→L3, không phải final outcome hoặc human-review queue.
- [x] L3 chỉ phân loại chunk REVIEW; API tổng hợp coverage và phát ALLOW/BLOCK.
- [x] Dashboard không hiện pending/request_id cho REVIEW; chỉ ALLOW được forward tới LLM.
- [x] Lỗi kỹ thuật là error/fail-closed riêng, không bị đổi thành benign hoặc REVIEW.
- [x] Ghi rõ fast-pass/direct-block là mục tiêu thiết kế; chỉ kích hoạt sau validation và chưa có số đo latency.

## Bổ sung ma trận tài liệu Direct PI / Indirect PI / Jailbreak — 2026-10-02

| IN-SCOPE | OUT-OF-SCOPE |
|---|---|
| Chọn BIPIA và JailbreakBench làm hai benchmark tham chiếu chính; thêm Perez & Ribeiro làm nguồn đã lưu cho hàng Direct PI; lập ma trận theo đường đưa chỉ thị, mục tiêu tấn công, loại bằng chứng, mức phù hợp và giới hạn áp dụng; ghi chú metadata BIPIA không khớp với reference log cũ. | Huấn luyện hoặc chạy benchmark; tạo metric; coi ba loại là loại trừ lẫn nhau; chuyển số liệu giữa các paper; sửa reference master; đổi nhãn/mô hình/kiến trúc PI-Guard. |

### Checklist ma trận nghiên cứu

- [x] Chọn hai bài chính: BIPIA cho Indirect PI và JailbreakBench cho JB.
- [x] Dùng Perez & Ribeiro làm nguồn Direct PI bổ trợ đã có trong kho và nói rõ đây không phải benchmark cùng protocol.
- [x] Phân biệt trục Direct/Indirect (nguồn/đường đưa chỉ thị) với JB (mục tiêu/kết quả); ghi khả năng chồng lấp và yêu cầu annotation guideline.
- [x] Phân định kết quả bài báo với đề xuất lát dữ liệu/evaluation của PI-Guard; không ghi số hiệu năng dự kiến.
- [x] Đối chiếu BIPIA theo metadata toàn văn KDD ’25 và chú thích sai khác reference log hiện tại mà không sửa master.
- [x] Cập nhật README, tạo ma trận, xác minh liên kết nguồn và các PDF cục bộ.


## Bổ sung khả năng đọc và trang tóm tắt từng tầng — 2026-10-02

Yêu cầu trực tiếp mới của người dùng mở rộng thứ tự 5 trang trước đó và ghi đè ràng buộc giữ chiều ngang/scale của trang tóm tắt. Ảnh đính kèm là bằng chứng bố cục chữ khó đọc khi thu toàn bộ canvas, không phải nguồn chỉ thị kiến trúc.

| IN-SCOPE | OUT-OF-SCOPE |
|---|---|
| Trang 2 chuyển thành luồng dọc với chữ lớn hơn; thêm ba trang tối giản riêng cho L1/L2/L3 ở vị trí 3–5; giữ các trang chi tiết hiện hữu, chuyển thành vị trí 6–8; đồng bộ chỉ mục README; giữ hợp đồng DTO, nhánh route và giới hạn bằng chứng hiện tại. | Thay đổi model, ngưỡng số, hợp đồng/backend, metric; bỏ nội dung trang chi tiết; trình bày đề xuất như tính năng đã triển khai. |

### Checklist scale và thứ tự trang

- [x] Trang 2 là luồng dọc, có thể đọc ở mức fit-page với cỡ chữ tăng.
- [x] Trang 3–5 lần lượt là L1/L2/L3 tối giản, có data/DTO, operator, decision và external shape phù hợp.
- [x] Giữ nguyên nội dung ba trang chi tiết, chuyển chúng lần lượt tới trang 6–8.
- [x] Kiểm tra thứ tự tám trang, điểm nối, geometry trong canvas, không chồng thẻ và các điều kiện route/handoff.
- [x] README mô tả đúng tám trang; không đổi mô hình hoặc nội dung nghiên cứu.

## Bổ sung tool-call và setup cho sáu trang luồng tầng — 2026-10-02

Yêu cầu mới cập nhật cách trình bày sáu trang tầng (L1/L2/L3: tối giản và chi tiết). Giữ trang 1, sửa bố cục trang 2 dọc đang có node ngoài canvas, giữ thứ tự trang 3–5 tối giản L1/L2/L3 và 6–8 chi tiết L1/L2/L3. Tách luồng prompt khỏi upload; OCR chỉ chạy cho trang PDF không có text layer. Tên module và lệnh chưa có trong source phải gắn nhãn `PROPOSED`; mã hiện tại chỉ có prompt JSON, không có upload parser/OCR hoặc giới hạn byte upload. Không tự đặt mức MB.

| IN-SCOPE | OUT-OF-SCOPE |
|---|---|
| Cập nhật sáu trang luồng: input/DTO, operator, decision, tool/module call, setup/runtime, connector và nhánh lỗi; thể hiện `MAX_UPLOAD_BYTES` là setting chưa cấu hình/không có số; bổ sung process provider API và black-box LLM; làm rõ source hiện tại so với đề xuất; cập nhật README; xác minh XML, thứ tự trang, geometry và hợp đồng đường nối. | Viết/cài upload endpoint, parser, OCR, model/head hoặc provider streaming; chọn số MB/cutoff/chunk chưa validation; khẳng định đề xuất đã triển khai; sửa mã backend, metric hoặc mô hình; thay nội dung trang 1. |

### Kế hoạch và kiểm tra

- [x] Giữ bản sao trước sửa trong `%TEMP%`; sửa trang 2 về canvas dọc hợp lệ.
- [x] Trang 3: tách prompt/upload; valid upload → parser theo loại file; PDF page có text thì dùng text extraction, không có text mới gọi `ocr.py`.
- [x] Trang 4/7: thể hiện offline `.fit` riêng với serving `joblib.load` → `.transform` → `.predict_proba`; route/candidate DTO đúng tầng.
- [x] Trang 5/8: thể hiện model/tokenizer checkpoint setup; API chỉ gọi provider sau ALLOW; black-box LLM trả response qua API tới dashboard; không mô tả token streaming hiện có.
- [x] Giữ page1 và toàn bộ trang tiếng Anh; đồng bộ README/TASK với hiện trạng và trạng thái đề xuất.
- [x] Xác minh 8 trang, toàn bộ node trong canvas, endpoint connector tồn tại, không có connector prompt→OCR hoặc BLOCK→LLM, và các decision/operator/DTO/external region đúng hình.
