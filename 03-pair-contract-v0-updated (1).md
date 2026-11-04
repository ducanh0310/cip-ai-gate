# Pair contract v0 — Cặp C

- **Thành viên** — Nguyễn Đức Anh và Nguyễn Ngọc Vĩnh
- **Mốc nộp** — Gate 0, 04/11/2026
- **Trạng thái** — Hai thành viên đã thống nhất nội dung phối hợp.

## 1. Hai bài toán giao nhau ở đâu và giá trị cộng hưởng là gì?

Đức Anh xây **AI Gate** để kiểm tra MC trên Confluence và soạn email xin phê duyệt CIP. Vĩnh xây **AI SDLC Orchestrator** để điều phối phát triển và kiểm thử phần mềm có AI hỗ trợ, theo định hướng SOX và TDD.

Hai sản phẩm kết nối tại **điểm kiểm soát trước phê duyệt CIP**. Orchestrator thu thập ngữ cảnh từ requirement, task, kiểm thử, review và artifact rồi gửi tham chiếu MC/CIP cho Gate. Gate chạy ruleset và trả kết quả, findings, tham chiếu evidence và thông tin bản nháp email. Orchestrator gắn kết quả vào workflow, chuyển đến bước xử lý hoặc phê duyệt và tổng hợp hồ sơ audit.

Giá trị kỳ vọng là truy vết được từ thay đổi phần mềm đến kết quả kiểm tra MC/CIP và quyết định phê duyệt, đồng thời tăng độ đầy đủ của evidence và giảm thời gian, công sức xử lý thủ công.

## 2. Mỗi người chịu trách nhiệm phần nào và ranh giới ở đâu?

| Thành viên | Trách nhiệm |
| --- | --- |
| **Đức Anh — AI Gate** | Sở hữu logic kiểm tra MC/CIP, checklist và ruleset, findings, mẫu và bản nháp email CIP. Chuẩn bị mockup và đáp án kỳ vọng, cung cấp giao diện chạy và kết quả có cấu trúc, sửa lỗi thuộc Gate. |
| **Vĩnh — AI SDLC Orchestrator** | Sở hữu workflow và trạng thái SDLC, điều phối requirement/task/agent, thu thập ngữ cảnh và artifact. Tích hợp Gate Adapter, xử lý kết quả trong workflow, quản lý approval task, RBAC/SoD, audit trail và hồ sơ evidence tổng thể. |

Gate đánh giá theo ruleset và chỉ tạo bản nháp email trong phạm vi MVP. Orchestrator giữ workflow ở bước xử lý hoặc rà soát khi nhận `FAIL` hoặc `NEEDS_REVIEW`. Khi nhận `PASS`, Orchestrator chuyển đến bước phê duyệt của người có thẩm quyền theo RBAC/SoD. Merge và deploy production vẫn theo quy trình phê duyệt.

Gate có thể chạy và đánh giá độc lập. Orchestrator có thể phát triển và demo với mock/stub. SOX là định hướng thiết kế.

## 3. Hai bên trao đổi gì và theo định dạng nào?

| Chiều trao đổi | Nội dung | Định dạng |
| --- | --- | --- |
| Đức Anh → Vĩnh | Bộ tình huống mockup, đáp án kỳ vọng, hướng dẫn chạy và phiên bản checklist. | JSON, tệp mockup, tài liệu và cấu hình. |
| Orchestrator → Gate | `workflow_id`, `task_id`, `correlation_id`, người yêu cầu, checkpoint, metadata MC/CIP và ngữ cảnh cần thiết. Artifact được tham chiếu bằng URI, phiên bản và hash theo schema. | REST API qua HTTP, JSON request. |
| Gate → Orchestrator | ID truy vết, `gate_run_id`, `PASS` / `FAIL` / `NEEDS_REVIEW`, phiên bản ruleset, kết quả từng tiêu chí, findings (mã control/rule, mức độ, mô tả, tham chiếu evidence), trạng thái hoặc URI email draft và thời điểm hoàn tất. | JSON response. |
| Orchestrator → Đức Anh | Kết quả Gate gắn với workflow, findings, evidence và thông tin lỗi cần xử lý. | JSON hoặc giao diện workflow. |

OpenAPI/JSON Schema là đặc tả chung. Request và response có phiên bản schema hoặc API. Lỗi kỹ thuật như input không hợp lệ, timeout hoặc Gate unavailable được xử lý riêng với kết quả kiểm soát. Log truy vết ghi mã tình huống/change, phiên bản ứng dụng/checklist/ruleset, kết quả, lỗi và thời gian xử lý cùng các ID ở trên.

Khi triển khai, hai bên đưa vào đặc tả các chi tiết đã thống nhất về endpoint, loại MC document và metadata được nhận, trường bắt buộc/tùy chọn, cách lưu và truy cập artifact, xác thực, service identity, phân quyền, error schema, timeout/retry, idempotency và versioning. Bộ mockup chung gồm MC theo sáu mục đã xác nhận, link giả lập, tệp `.msg` và đáp án kỳ vọng.

## 4. Khi nào tích hợp và đo giá trị cộng hưởng bằng gì?

| Mốc | Kết quả cần có |
| --- | --- |
| **Gate 0 — 04/11** | Nộp Pair contract v0 với mục tiêu cộng hưởng, phân công, ranh giới và đặc tả trao đổi ở mức v0. |
| **Gate 1 — 11/11** | Chạy skeleton end-to-end với Gate mock/stub và kiểm chứng rủi ro API lớn nhất. |
| **CP1 — 18/11** | Demo MVP trên mockup, kiểm chứng request/response, trạng thái workflow và truy vết cơ bản. |
| **CP2 — 25/11** | Hoàn thiện luồng tích hợp, xử lý lỗi và evidence. |
| **CP3 — 09/12** | Demo end-to-end, đo giá trị cộng hưởng và bàn giao tài liệu. |

Hai bên dùng mockup tự dựng đến hết CP1. CP2–CP3 chỉ dùng dữ liệu masked do mentor cung cấp và cho phép. Dữ liệu masked nằm ngoài repo. Dữ liệu thật nằm ngoài phạm vi ở mọi mốc.

Đo trên cùng bộ mockup và cùng loại thay đổi qua ba kịch bản **A — xử lý MC/CIP và evidence thủ công**, **B — chạy Orchestrator riêng**, và **C — tích hợp Orchestrator với Gate, human approval và hồ sơ evidence**.

| Chỉ số | Cách đo |
| --- | --- |
| Tỷ lệ tích hợp thành công | Request hợp lệ nhận response đúng schema / tổng request hợp lệ. |
| Độ bao phủ kiểm soát | Rule/control được đánh giá / tổng rule/control trong bộ test. |
| Độ đầy đủ truy vết | Workflow có đủ liên kết request → Gate run → finding/evidence → approval / tổng workflow. |
| Độ đầy đủ evidence | Evidence bắt buộc có đủ metadata và tham chiếu / tổng evidence bắt buộc. |
| Thời gian xử lý | Thời gian từ lúc gửi request đến khi nhận response. |
| Công sức thủ công tiết kiệm | Thời gian thao tác thủ công ở A trừ thời gian thao tác thủ công ở C. |
| Xử lý ngoại lệ | Timeout hoặc response không hợp lệ được ghi nhận và đưa workflow về trạng thái an toàn / tổng số ngoại lệ này. |
| Tuân thủ phê duyệt | Số lượt phê duyệt đúng role và đúng SoD / tổng lượt phê duyệt. |

Hai bên ghi nhận baseline từ bộ test chung để xác định ngưỡng mục tiêu và trình mentor duyệt. Khi triển khai, phân công đầu mối cho contract test, integration test và demo, đồng thời trình mentor xác nhận ranh giới và mức độ phù hợp với quy trình công ty.
