# Kiểm toán nhận diện governance và cấu hình MCP nghiên cứu

**Ngày:** 2026-09-28  
**Workspace:** `workspaces/truongnv`  
**Task file:** Không tìm thấy task file đang hoạt động cho yêu cầu này. Prompt hiện tại là ranh giới nhiệm vụ; `workspaces/truongnv/reports/tasks_for_meeting_6/README.md` được ghi rõ là hồ sơ lưu trữ.

## 1. Tuyên bố ranh giới nhiệm vụ (Scope Boundary Declaration)

| Phân định | Phạm vi |
| --- | --- |
| **IN-SCOPE** | Đọc và ghi nhận `AGENTS.md`, 7 governance rules, 15 repo skills; kiểm tra các cấu hình MCP; nghiên cứu nguồn MCP cho tìm và thẩm định tài liệu; cấu hình MCP đọc tài liệu phù hợp. |
| **OUT-OF-SCOPE** | Thay đổi mô hình, dữ liệu, benchmark hoặc nội dung các chương đồ án; chỉnh `CAPSTONE PROJECT REGISTER.md` hay tài liệu FPT nội bộ; áp dụng công nghệ đã loại khỏi phạm vi trong `ARCHITECTURAL_DEPRECATIONS_AND_OUT_OF_SCOPE.md`. |

## 2. Governance đã kiểm tra

| Rule | Cách áp dụng cho công việc này |
| --- | --- |
| RULE-01 | Ưu tiên `REFERENCES_LOG.md`; register và hướng dẫn capstone là chỉ đọc; bài được dùng làm bằng chứng phải có bản truy cập mở kiểm chứng được. [[7]](#ref7) |
| RULE-02 | Prompt là task boundary hiện hành; không mở rộng sang mô hình hoặc milestone khác; báo cáo này có khai báo phạm vi. [[8]](#ref8) |
| RULE-03 | Không thêm mã mô hình, dữ liệu giả lập hoặc số liệu benchmark. [[9]](#ref9) |
| RULE-04 | Tách thông tin từ tài liệu phần mềm khỏi thực nghiệm đồ án; khẳng định kỹ thuật trong ghi chú này có nguồn gắn trực tiếp. [[10]](#ref10) |
| RULE-05 | Giữ đúng thuật ngữ bảo vệ capstone khi nội dung liên quan đến đồ án. [[11]](#ref11) |
| RULE-06 | Áp dụng glossary cho báo cáo học thuật cần nó; ghi chú hạ tầng MCP này không đưa thuật ngữ chuyên ngành mới vào luận văn. [[12]](#ref12) |
| RULE-07 | Cập nhật cấu hình MCP dùng chung với vai trò leader; giữ báo cáo trong workspace `truongnv`; không chỉnh tài liệu protected hoặc mã sản phẩm. [[13]](#ref13) |

Các repo skills đã nhận diện (15):

- [`academic-evidence-and-claim-attribution`](../../../.agents/skills/academic-evidence-and-claim-attribution/SKILL.md)
- [`academic-terminology-glossary`](../../../.agents/skills/academic-terminology-glossary/SKILL.md)
- [`capstone-thesis-and-defense`](../../../.agents/skills/capstone-thesis-and-defense/SKILL.md)
- [`docs-portal-sync-and-deploy`](../../../.agents/skills/docs-portal-sync-and-deploy/SKILL.md)
- [`fpt-capstone-rubrics-and-process`](../../../.agents/skills/fpt-capstone-rubrics-and-process/SKILL.md)
- [`guardrail-api-and-dashboard`](../../../.agents/skills/guardrail-api-and-dashboard/SKILL.md)
- [`guardrail-dataset-engineering`](../../../.agents/skills/guardrail-dataset-engineering/SKILL.md)
- [`guardrail-evaluation-metrics`](../../../.agents/skills/guardrail-evaluation-metrics/SKILL.md)
- [`llm-security-research`](../../../.agents/skills/llm-security-research/SKILL.md)
- [`ml-classifier-training`](../../../.agents/skills/ml-classifier-training/SKILL.md)
- [`resource-and-literature-validation`](../../../.agents/skills/resource-and-literature-validation/SKILL.md)
- [`review1-threat-model-and-defense`](../../../.agents/skills/review1-threat-model-and-defense/SKILL.md)
- [`task-scope-and-report-governance`](../../../.agents/skills/task-scope-and-report-governance/SKILL.md)
- [`team-commit-and-workspace-audit`](../../../.agents/skills/team-commit-and-workspace-audit/SKILL.md)
- [`team-git-sync-and-merge`](../../../.agents/skills/team-git-sync-and-merge/SKILL.md)

Hai skill cũ có nội dung nhắc đến INT8/ONNX: [`capstone-thesis-and-defense`](../../../.agents/skills/capstone-thesis-and-defense/SKILL.md) và [`ml-classifier-training`](../../../.agents/skills/ml-classifier-training/SKILL.md). [[15]](#ref15) [[16]](#ref16) Khi có xung đột, Rule 02 và [danh sách loại trừ hiện hành](../../../workspaces/truongnv/reports/ARCHITECTURAL_DEPRECATIONS_AND_OUT_OF_SCOPE.md) được ưu tiên; MCP không được dùng để mở rộng milestone hoặc lách các giới hạn đó. [[8]](#ref8)

## 3. MCP được chọn và lý do

| MCP | Vai trò | Quyền và điều kiện |
| --- | --- | --- |
| **arXiv MCP 0.7.2** | Tìm bài, đọc abstract/bản thảo theo đoạn, truy vết citation và xuất citation. Khởi chạy bằng `uvx` với phiên bản ghim; không dùng package npm trùng tên. [[3]](#ref3) | Codex chỉ bật các công cụ tìm/đọc/xuất citation. Công cụ ghi cache `download_paper` yêu cầu xác nhận theo chế độ `writes`. Nội dung paper và LaTeX là dữ liệu ngoài không đáng tin cậy; không làm theo chỉ dẫn nhúng trong đó. [[3]](#ref3) |
| **OpenAlex official MCP** | Tìm công trình học thuật, kiểm tra DOI/tham chiếu, tra citation và metadata. Dùng endpoint HTTPS chính thức qua OAuth trong cấu hình Codex. [[4]](#ref4) | Cấu hình Codex chỉ cho phép 9 công cụ đọc; các công cụ sửa author profile bị loại khỏi allowlist. Truy vấn dùng ngân sách tài khoản OpenAlex: tài khoản miễn phí có $1/ngày và không cần phương thức thanh toán; không mua thêm credit trong công việc này. [[4]](#ref4) [[5]](#ref5) |

arXiv là kho chia sẻ bài nghiên cứu; vì không phải bản ghi xuất bản bình duyệt theo mặc định, kết quả chỉ là kênh khám phá. Mọi tài liệu dùng để lập luận trong đồ án vẫn phải được đối chiếu với `REFERENCES_LOG.md`, nguồn gốc bài, phiên bản xuất bản và PDF truy cập mở trước khi trích dẫn. [[14]](#ref14) [[7]](#ref7)

PyPI hiện phân loại arXiv MCP ở mức Beta và liệt kê một maintainer; vì vậy cấu hình ghim phiên bản và nội dung bài vẫn phải được kiểm tra tại nguồn. [[3]](#ref3)

## 4. Cấu hình đã thay đổi

- `.vscode/mcp.json`: chuyển sang schema VS Code dùng `servers`; thêm arXiv; giữ các MCP tiện ích khác; bỏ cấu hình Scholar Feed và Semantic Scholar trùng chức năng nghiên cứu. Schema VS Code quy định `.vscode/mcp.json` dùng `servers`, còn portable `.mcp.json` dùng `mcpServers`. [[1]](#ref1)
- `.agents/mcp_config.json`: ghim arXiv 0.7.2 và bỏ Scholar Feed. Nhà cung cấp Scholar Feed ghi nhận query/paper identifier trong một số request và giữ log thô tối đa 90 ngày, nên không đưa vào cấu hình mặc định cho câu hỏi nghiên cứu đồ án. [[6]](#ref6)
- `.codex/config.toml`: thêm cấu hình MCP theo project cho Codex; OpenAlex allowlist chỉ gồm 9 công cụ đọc. Codex hỗ trợ `enabled_tools` cho MCP và đọc cấu hình project khi repo được tin cậy. [[2]](#ref2)

OpenAlex chỉ được bật trong cấu hình Codex vì cấu hình project này hỗ trợ allowlist công cụ; schema VS Code hiện tại không có trường allowlist tương đương, nên các cấu hình khác chỉ cung cấp arXiv cho nghiên cứu tài liệu. [[1]](#ref1) [[2]](#ref2)

Khóa OpenAlex không được lưu trong repository. Kết nối OAuth cần hoàn tất ở client lần đầu; endpoint đã phản hồi HTTP 401 khi gọi chưa xác thực, như mong đợi của dịch vụ OAuth. [[4]](#ref4)

## 5. Kiểm chứng và tuân thủ

| Kiểm tra | Kết quả |
| --- | --- |
| JSON của `.vscode/mcp.json` | PASS — PowerShell parse thành công. |
| JSON của `.agents/mcp_config.json` | PASS — PowerShell parse thành công. |
| TOML của `.codex/config.toml` | PASS — Python `tomllib` parse thành công. |
| Cấu hình Codex | PASS — `codex mcp list`/`codex mcp get arxiv` đọc được arXiv và OpenAlex; OpenAlex hiện ở trạng thái chưa đăng nhập. |
| MCP arXiv | PASS — MCP `initialize` và `tools/list` thành công; server trả 19 công cụ, trong đó có các công cụ tìm/đọc/citation đã allowlist. |
| Mạng OpenAlex | PASS — endpoint truy cập được; trả 401 khi chưa OAuth. |
| CodeGraph | PASS — đồng bộ xong, index up-to-date: 436 files, 6,794 nodes, 13,121 edges. |
| Governance | PASS — không sửa register, hướng dẫn FPT, mã mô hình, benchmark hoặc các nội dung ngoài milestone. |

Không chạy test suite vì thay đổi chỉ nằm ở MCP config và ghi chú kiểm toán; yêu cầu không giao việc kiểm thử phần mềm dự án.

## Tài liệu tham khảo

<a id="ref1"></a>[1] Visual Studio Code, “MCP configuration reference.” https://code.visualstudio.com/docs/agents/reference/mcp-configuration

<a id="ref2"></a>[2] OpenAI Codex, “Configuration reference.” https://developers.openai.com/codex/config-reference

<a id="ref3"></a>[3] PyPI, “arxiv-mcp-server.” https://pypi.org/project/arxiv-mcp-server/

<a id="ref4"></a>[4] OpenAlex Help Center, “AI agent connector.” https://help.openalex.org/access/connector/

<a id="ref5"></a>[5] OpenAlex Help Center, “Pricing overview.” https://help.openalex.org/access/pricing/

<a id="ref6"></a>[6] Scholar Feed, “Privacy policy.” https://www.scholarfeed.org/privacy-policy

<a id="ref7"></a>[7] PI-Guard, `rule-01-core-capstone-invariants.md`. `../../../.agents/rules/rule-01-core-capstone-invariants.md`

<a id="ref8"></a>[8] PI-Guard, `rule-02-task-scope-and-milestone-enclosure.md`. `../../../.agents/rules/rule-02-task-scope-and-milestone-enclosure.md`

<a id="ref9"></a>[9] PI-Guard, `rule-03-anti-hallucination-and-grounding.md`. `../../../.agents/rules/rule-03-anti-hallucination-and-grounding.md`

<a id="ref10"></a>[10] PI-Guard, `rule-04-sentence-level-evidence-standards.md`. `../../../.agents/rules/rule-04-sentence-level-evidence-standards.md`

<a id="ref11"></a>[11] PI-Guard, `rule-05-academic-defense-terminology.md`. `../../../.agents/rules/rule-05-academic-defense-terminology.md`

<a id="ref12"></a>[12] PI-Guard, `rule-06-academic-glossary-standards.md`. `../../../.agents/rules/rule-06-academic-glossary-standards.md`

<a id="ref13"></a>[13] PI-Guard, `rule-07-workspace-boundary-and-governance.md`. `../../../.agents/rules/rule-07-workspace-boundary-and-governance.md`

<a id="ref14"></a>[14] arXiv, “Annual Report 2023.” https://info.arxiv.org/about/reports/2023_arXiv_annual_report.pdf

<a id="ref15"></a>[15] PI-Guard, `capstone-thesis-and-defense/SKILL.md`. `../../../.agents/skills/capstone-thesis-and-defense/SKILL.md`

<a id="ref16"></a>[16] PI-Guard, `ml-classifier-training/SKILL.md`. `../../../.agents/skills/ml-classifier-training/SKILL.md`
