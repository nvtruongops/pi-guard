# Đề xuất xử lý ảnh Meeting 6 thiếu bằng chứng

## Scope Boundary Declaration

- **IN-SCOPE:** 23 ảnh hiện còn trong `reports/tasks_for_meeting_6/figures/` và căn cứ xóa từng ảnh.
- **OUT-OF-SCOPE:** dữ liệu, kết quả, báo cáo ngoài thư mục ảnh; khôi phục benchmark đã rút; tạo lại ảnh hoặc khẳng định metric mới.

## Căn cứ rà soát

- [README Meeting 6](README.md) giới hạn bằng chứng hiện hành ở PIDS-Bench TF-IDF cùng paper và lần chạy PIGuard trên assets cùng release; chưa có kết quả cascade hoặc KPI P95/FPR đạt được.
- [Sổ đăng ký artifact đã rút](WITHDRAWN_DATA_ARTIFACTS.md) và [provenance audit](../experiment_reports/WORKSPACE_PROVENANCE_AUDIT_2026-09-30.md) đánh dấu các bộ benchmark/chỉ báo Meeting 4–6 cũ là không đủ căn cứ để dùng làm bằng chứng.
- Tìm kiếm tên file và `figures/` trong Markdown, HTML, TeX, YAML và JSON dưới thư mục Meeting 6 không tìm thấy tham chiếu văn bản nào tới các ảnh bên dưới.
- Các ảnh được xem trực tiếp. Nhiều ảnh đưa số đo, ngưỡng, hiệu năng hoặc kết quả cascade không có tệp JSON un-mocked/protocol hợp lệ kèm theo. Một số ảnh thuần khái niệm vẫn gán khẳng định kỹ thuật hoặc kiến trúc PI-Guard mà không có nguồn gắn với từng khẳng định.

## Manifest đề xuất

| Hành động | Tệp | Căn cứ |
|---|---|---|
| DELETE | `figures/fig_agentic_tool_attack_surface.png` | Gọi NIST là căn cứ cho khẳng định “only robust defense”; không có nguồn cụ thể cho khẳng định tuyệt đối này. |
| DELETE | `figures/fig_chunker_head_and_tail_algorithm.png` | Nêu thời gian 4,115.6 ms/37.1 ms và tốc độ 111× như thực nghiệm nhưng không có kết quả/protocol được chấp nhận. |
| DELETE | `figures/fig_conformal_risk_control.png` | Histogram, ngưỡng q̂=0.702 và mức rủi ro 1% không chỉ ra tập calibration hay dữ liệu nguồn. |
| DELETE | `figures/fig_dan_jailbreak_persona.png` | Tuyên bố PI-Guard phát hiện jailbreak 98%+ và TF-IDF bỏ sót 100% mà không có phép đo hợp lệ. |
| DELETE | `figures/fig_deberta_v3_disentangled_attention.png` | Có mô tả attention nhưng kết luận về DAN và khả năng của BERT/RoBERTa không được nguồn hay kết quả cùng paper chứng minh. |
| DELETE | `figures/fig_direct_pi_example.png` | Tình huống “production incident” dựng sẵn, xác suất 0.994, độ trễ 0.85 ms và “100% protection” không có JSON thực nghiệm. |
| DELETE | `figures/fig_five_inscope_breakthroughs.png` | Khẳng định 98.0% accuracy và tăng tốc 111×; không có bằng chứng hợp lệ cho mô hình/đo đạc này. |
| DELETE | `figures/fig_indirect_pi_rag_flow.png` | Không gắn nguồn cho mô tả tấn công; đồng thời trình bày cơ chế phòng thủ PI-Guard như đã triển khai/được kiểm chứng. |
| DELETE | `figures/fig_llama_guard_bottleneck.png` | So sánh P95, VRAM, RAM và chi phí với cascade PI-Guard nhưng thiếu cấu hình phần cứng, protocol và phép đo được chấp nhận. |
| DELETE | `figures/fig_markdown_exfiltration_attack.png` | Ví dụ dựng sẵn đi kèm F1 >98% và kiến trúc ingress/egress như kết quả; không có dữ liệu kiểm chứng. |
| DELETE | `figures/fig_math_formalization_token_space.png` | Công thức được gắn nhãn “theorem” và kết luận bắt buộc external filter không được chứng minh bởi nguồn hiển thị. |
| DELETE | `figures/fig_nist_5axis_radar.png` | Điểm severity/coverage trên radar không có định nghĩa thang đo hoặc dữ liệu; coverage PI-Guard là giá trị tự gán. |
| DELETE | `figures/fig_nist_axis4_5_damage_and_context.png` | Gán mức thiệt hại/pháp lý và nêu FPR, P95, tỷ lệ chặn như cấu hình/hiệu quả đã xác nhận nhưng không có nguồn. |
| DELETE | `figures/fig_overdefense_cost_curve.png` | Các đường FPR theo threshold của Meta, ProtectAI và PI-Guard không có CSV/protocol paper-matched; có metric thuộc các run đã rút. |
| DELETE | `figures/fig_owasp_nist_taxonomy.png` | Xếp hạng/ánh xạ OWASP–NIST và tác động tuân thủ không có trích dẫn cụ thể cho từng mệnh đề. |
| DELETE | `figures/fig_regex_failure_modes.png` | Gọi kết quả là empirical, tuyên bố regex thất bại 100% và recall 99.4% nhưng không có tập mẫu hoặc kết quả hợp lệ. |
| DELETE | `figures/fig_review2_roadmap_timeline.png` | Lịch tuần 7–10 không có task/schedule hiện hành làm nguồn và ảnh không được tài liệu hiện hành dẫn chiếu. |
| DELETE | `figures/fig_saltzer_schroeder_four_principles.png` | Dù nêu Saltzer–Schroeder, các số 82.6%, 0.85 ms, 100% coverage và FPR <1% không có bằng chứng. |
| DELETE | `figures/fig_sota_overdefense_gap.png` | So sánh FPR/P95 và phần cứng giữa nhiều mô hình là kết quả cũ không paper-matched hoặc không có protocol. |
| DELETE | `figures/fig_threat_model_flat_token_space.png` | Dùng phép ví von OS/NX-bit như cơ chế tương đương và khẳng định về attention/goal hijacking không có căn cứ đủ cụ thể. |
| DELETE | `figures/fig_three_scientific_boundaries.png` | Nêu tấn công Crescendo 10–20 lượt và đặc tính/stateless KPI của PI-Guard mà không dẫn dữ liệu hay nguồn gắn với ảnh. |
| DELETE | `figures/fig_tier0_scrubber_pipeline.png` | Đưa latency <0.05 ms và F1 tiếng Việt 64.2%→91.8%; workspace xác nhận chưa có split tiếng Việt được kiểm chứng nguồn. |
| DELETE | `figures/fig_tristate_vs_binary_routing.png` | Nêu cascade F1 98.2%, P95 12.9 ms, FPR 1.15% và conformal benchmark 520 mẫu; cascade chưa được đo và các số cũ không phải bằng chứng hiện hành. |

## Phụ thuộc và phương án thay thế

- Không tìm thấy tài liệu văn bản Meeting 6 nào nhúng hoặc dẫn chiếu các ảnh này; xóa chúng không làm hỏng tham chiếu Markdown/HTML/TeX/YAML/JSON hiện hành.
- Không thay số liệu trong ảnh bằng metric từ báo cáo khác. Hai báo cáo được giữ lại có task/protocol riêng và không chứng minh các claim trong ảnh; dùng [PIDS-Bench report](../../replications/PIDS_Bench_Shire_IEEEAccess2026/REPORT.md) và [PIGuard-only report](../../replications/02_DeBERTa_v3_Semantic_Classifier/reports/review1_paper_model_public_rerun_2026-09-30/REPORT.md) chỉ cho phạm vi kết quả được mô tả trong chính các báo cáo đó.
- Nếu cần hình lý thuyết sau này, tạo lại từng hình từ nguồn paper được pin và gắn citation cho từng claim. Chỉ vẽ biểu đồ kết quả khi có JSON un-mocked cùng protocol và kiểm tra provenance.

## Trạng thái thực thi và xác minh

- **Đánh giá đề xuất:** Đề xuất xóa 23 ảnh là hoàn toàn chính xác theo Rule 03 (chống hallucination/fabrication metric), Rule 05 (chuẩn thuật ngữ hội đồng) và phạm vi Meeting 6 (không có tài liệu nào tham chiếu; các số liệu/cascade không có căn cứ JSON un-mocked).
- **Thực thi:** Đã thực hiện xóa toàn bộ 23 tệp ảnh trong manifest khỏi thư mục `workspaces/truongnv/reports/tasks_for_meeting_6/figures/`.
- **Xác minh số lượng tệp:** Kết quả kiểm tra số tệp còn lại trong thư mục là `0`.
- **Trạng thái Git:** `git status --short -- workspaces/truongnv/reports/tasks_for_meeting_6/figures` ghi nhận đúng 26 tệp ở trạng thái xóa (` D`), gồm 23 tệp theo manifest và 3 tệp đã xóa từ trước.
- **CodeGraph:** `codegraph sync .` đã chạy và xác nhận đồng bộ.
