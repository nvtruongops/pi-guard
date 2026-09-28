# 🎯 Rule 02: Task-Scope Enclosure & Milestone Boundary Governance

> **Quy định bất biến về khóa chặt ranh giới nhiệm vụ (Task Enclosure), loại bỏ hoàn toàn hiện tượng lan man (Anti-Scope Creep) và tuân thủ tuyệt đối phạm vi của tệp chỉ định nhiệm vụ (Task File)**  
> **Cơ chế thực thi**: Kích hoạt vai trò **Role 4: Strict Task-Scope Guardian**, kiểm toán tự động qua `python Final-Report/scripts/audit_task_scope.py` và tích hợp vào `validate_local.py`.

---

## 🔒 1. NGUYÊN TẮC TỐI THƯỢNG: TỆP NHIỆM VỤ LÀ LUẬT RANH GIỚI (TASK FILE IS THE BOUNDARY LAW)

Mọi khiếm khuyết Agent bị ảo giác, viết code sớm, hoặc sinh báo cáo ngoài phạm vi đều xuất phát từ việc vi phạm nguyên tắc này:

> [!CAUTION]
> **LUẬT RANH GIỚI NHIỆM VỤ (THE TASK BOUNDARY INVARIANT)**:
> Khi một nhiệm vụ được giao gắn liền với một tệp chỉ định cụ thể (ví dụ: `README.md` trong `tasks_for_meeting_6/`, hoặc bất kỳ task file nào):
> 1. **Tệp nhiệm vụ đó là giới hạn tối đa (Upper Bound)** của mọi hành động, phân tích, mã nguồn và báo cáo được sinh ra.
> 2. **CẤM TUYỆT ĐỐI** việc tự ý bổ sung các hạng mục không được yêu cầu trong tệp nhiệm vụ.
> 3. **CẤM TUYỆT ĐỐI** việc "tiện tay" hiện thực hóa mã nguồn hoặc kết luận của các giai đoạn/chương tiếp theo khi nhiệm vụ hiện tại chưa yêu cầu.

---

## 📋 2. QUY TRÌNH 3 BƯỚC BẮT BUỘC TRƯỚC KHI THỰC HIỆN NHIỆM VỤ (PRE-EXECUTION SCOPE BOUNDING)

Trước khi Agent viết bất kỳ dòng mã nào hoặc tạo bất kỳ tệp báo cáo nào, Agent **BẮT BUỘC** phải thực hiện quy trình 3 bước:

```text
┌────────────────────────────────────────────────────────────────────────┐
│             QUY TRÌNH 3 BƯỚC KHÓA CHẶT RANH GIỚI NHIỆM VỤ              │
└────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
       ┌──────────────────────────────────────────────────────────┐
       │ BƯỚC 1: ĐỌC & BÓC TÁCH TỆP NHIỆM VỤ (PARSE TASK FILE)   │
       │ - Xác định chính xác danh mục yêu cầu (Task Items).       │
       │ - Xác định mốc thời gian / Milestone tương ứng.          │
       └──────────────────────────────────────────────────────────┘
                                    │
                                    ▼
       ┌──────────────────────────────────────────────────────────┐
       │ BƯỚC 2: THIẾT LẬP BẢNG RANH GIỚI (SCOPE BOUNDARY TABLE)  │
       │ - IN-SCOPE: Những gì task file yêu cầu bắt buộc bàn giao.│
       │ - OUT-OF-SCOPE: Những gì tuyệt đối không được đưa vào.   │
       └──────────────────────────────────────────────────────────┘
                                    │
                                    ▼
       ┌──────────────────────────────────────────────────────────┐
       │ BƯỚC 3: THI HÀNH KHÉP KÍN (CONFINED EXECUTION & REPORT)  │
       │ - Mã nguồn chỉ nằm trong ranh giới In-Scope.            │
       │ - Báo cáo bắt buộc có mục 'Tuyên Bố Ranh Giới Nhiệm Vụ'. │
       └──────────────────────────────────────────────────────────┘
```

### Bảng Ranh Giới Chuẩn Mực Bắt Buộc Xác Định:
- **Tệp nguồn tham chiếu**: Ghi rõ đường dẫn tệp task (ví dụ: `workspaces/truongnv/reports/tasks_for_meeting_6/README.md`).
- **Phạm vi trong ranh giới (In-Scope Deliverables)**: Liệt kê đúng các câu hỏi/mục tiêu mà GVHD hoặc task file chỉ định.
- **Phạm vi ngoài ranh giới (Strictly Out-of-Scope)**:
  - Các công nghệ đã bị loại trừ trong `ARCHITECTURAL_DEPRECATIONS_AND_OUT_OF_SCOPE.md`.
  - Các giai đoạn tương lai chưa đến kỳ nghiệm thu (ví dụ: mô hình champion của nhóm thuộc Chapter 4, không được đưa vào task thực nghiệm baseline của Chapter 2).

---

## 🏛️ 3. PHÂN ĐỊNH RANH GIỚI CỘT MỐC HỌC THUẬT (MILESTONE PHASE GATING)

Agent phải tuân thủ nghiêm ngặt ranh giới giữa các giai đoạn đồ án:

| Giai Đoạn / Cột Mốc | Phạm Vi Được Phép (STRICTLY IN-SCOPE) | 🚫 Hành Vi Bị Cấm Tuyệt Đối (STRICTLY OUT-OF-SCOPE) |
| :--- | :--- | :--- |
| **Review 1 / Meeting 5–6 (Chương 2)** | • Khảo sát y văn, phân tích nguy cơ (Threat Modeling)<br>• Tái lập thực nghiệm các mô hình baseline công khai (Meta, ProtectAI, DataSentinel, PromptShield)<br>• Tìm kiếm khoảng trống nghiên cứu (Research Gaps - Mục 2.3)<br>• Đề xuất kiến trúc lý thuyết Chương 3 dạng SLA Targets trong văn xuôi | 🚫 Tự tạo module mã nguồn mô hình nhóm (`src/models/cascade/`, `ChampionCascadeClassifier`)<br>🚫 Đưa mô hình nhóm vào bảng đối chuẩn thực nghiệm kèm số liệu (F1 %, Latency ms)<br>🚫 Tuyên bố "đã hoàn thành mô hình vô địch của đồ án" |
| **Review 2 / Meeting 7–10 (Chương 3)** | • Xây dựng công thức toán học và thiết kế chi tiết kiến trúc đề xuất Two-Tier Cascade (SLA P95 < 30ms, Dual TF-IDF + DeBERTa-v3 FP32)<br>• Chuẩn hóa dữ liệu tiền xử lý, kiểm soát ranh giới từ chối | 🚫 Đưa ra bảng nghiệm thu kết quả đánh giá cuối cùng trước Hội đồng |
| **Review 3 / Meeting 11–13 (Chương 4)** | • Huấn luyện chính thức mô hình Champion của đồ án<br>• Đo đạc thực tế đối chuẩn với baselines Chương 2 trên D1–D6<br>• Đánh giá robustness chống evasion attack và nghiệm thu các chỉ số KPI cam kết | 🚫 Giả lập số liệu bằng phân phối ngẫu nhiên (np.random) |

---

## 🚨 4. TUÂN THỦ DANH MỤC CÔNG NGHỆ ĐÃ LOẠI TRỪ (DEPRECATION COMPLIANCE)

Tuân thủ tuyệt đối [`workspaces/truongnv/reports/ARCHITECTURAL_DEPRECATIONS_AND_OUT_OF_SCOPE.md`](file:///d:/Work/Do-an/workspaces/truongnv/reports/ARCHITECTURAL_DEPRECATIONS_AND_OUT_OF_SCOPE.md):
1. **Lượng tử hóa INT8 / ONNX Runtime (ZeroQuant Yao et al. 2022)**: ĐÃ BỊ LOẠI BỎ KHỎI PHẠM VI ÁP DỤNG. Cấm tuyệt đối trình bày INT8/ONNX như kiến trúc hiện thực của đề tài. Tầng 2 đề xuất của nhóm là **Native FP32 DeBERTa-v3** trên CPU tiêu chuẩn kết hợp cơ chế MOF (Hao Li et al. ACL 2025).
2. **Can thiệp trọng số nội bộ / Giám sát KV-Cache / White-Box Steering**: STRICTLY OUT-OF-SCOPE. Đề tài chỉ áp dụng mô hình **External Guardrail Proxy** mức văn bản.
3. **Guardrail dựa trên LLM Sinh (Generative Guardrails như Llama Guard)**: CHỈ LÀ BASELINE ĐO ĐẠC ĐỐI SÁNH, không phải kiến trúc áp dụng của đề tài do độ trễ quá cao (> 500ms).

---

## 📝 5. QUY CHUẨN TẠO BÁO CÁO TIẾN ĐỘ & NHIỆM VỤ (REPORT GOVERNANCE CONTRACT)

Mọi báo cáo nhiệm vụ (`reports/tasks_for_meeting_*/`, `reports/experiment_reports/`) khi được sinh ra BẮT BUỘC phải tuân thủ cấu trúc 3 phần:
1. **Mục 1: Tuyên Bố Ranh Giới Nhiệm Vụ (Scope Boundary Declaration)**:
   - Ghi rõ mã tệp task nguồn.
   - Nêu rõ: Báo cáo này chỉ giải quyết các nhiệm vụ [X, Y, Z] theo chỉ đạo.
   - Cam kết: Không chứa mã nguồn hoặc kết quả nghiệm thu thuộc các chương tiếp theo.
2. **Mục 2: Bàn Giao Kết Quả Theo Nhiệm Vụ (Empirical Deliverables)**:
   - Trình bày chính xác, súc tích các kết quả tương ứng với từng nhiệm vụ.
   - 100% số liệu phải trích xuất từ tệp JSON un-mocked tương ứng trong `04_benchmarks_and_data/`.
3. **Mục 3: Bảng Kiểm Tra Tuân Thủ Phạm Vi (Scope Compliance Checklist)**:
   - Đảm bảo 0% từ khóa cấm / out-of-scope.
   - Đảm bảo không có khẳng định vượt cấp tiến độ.
