# Pair contract v0 — Đề xuất phối hợp Cặp C

- Thành viên: Nguyễn Đức Anh và Nguyễn Ngọc Vĩnh.
- Cập nhật: 04/11/2026.
- Trạng thái: Phần của Đức Anh được giữ theo bản gốc. Phần của Vĩnh đã được cập nhật theo đề xuất AI SDLC Orchestrator; toàn bộ nội dung phối hợp và tích hợp vẫn cần hai bên rà soát, thống nhất và mentor xác nhận.
- Mốc rà soát: Gate 0 — 04/11/2026.

## 1. Điểm giao nhau và giá trị cộng hưởng

Đức Anh xây công cụ AI Gate kiểm tra MC trên Confluence và soạn email xin phê duyệt CIP. Vĩnh phụ trách MVP AI SDLC Orchestrator: nền tảng điều phối workflow phát triển và kiểm thử phần mềm có AI hỗ trợ, quản lý trạng thái, task, artifact, review, approval và audit/evidence theo định hướng SOX, TDD.

Hai sản phẩm bổ trợ nhau tại **approval/control checkpoint** trong SDLC:

- **AI SDLC Orchestrator** quản lý ngữ cảnh và workflow thay đổi phần mềm; thu thập requirement, task, kết quả kiểm thử, review và artifact liên quan.
- **AI Gate** là dịch vụ validation/control độc lập, kiểm tra MC document và hỗ trợ soạn email xin phê duyệt CIP theo ruleset.
- Orchestrator gửi MC/CIP metadata và context cần thiết sang Gate. Gate trả về trạng thái kiểm tra, findings, evidence references, ruleset version và email draft (nếu thuộc phạm vi Gate).
- Orchestrator tiếp nhận kết quả, cập nhật workflow, tạo/tiếp tục approval task và đóng gói audit/evidence. Người có thẩm quyền vẫn là người quyết định phê duyệt.

Giá trị cộng hưởng kỳ vọng: kết quả kiểm tra của Gate trở thành một phần có thể truy vết trong workflow SDLC và evidence package. Việc này giúp kết nối kiểm soát MC/CIP với quá trình phát triển, kiểm thử và phê duyệt thay đổi; đồng thời có cơ sở đo độ đầy đủ evidence, khả năng truy vết, thời gian xử lý và công sức thủ công tiết kiệm được.

Đây là hướng phối hợp đề xuất, chưa phải cam kết tích hợp đã được hai bên thống nhất và chưa có số liệu thực đo.

## 2. Trách nhiệm và ranh giới

| Đức Anh | Vĩnh — đề xuất cập nhật, chờ thống nhất |
| --- | --- |
| Xây công cụ kiểm tra MC và soạn email | Sở hữu AI SDLC Orchestrator; thiết kế và quản lý workflow/state của SDLC |
| Sở hữu checklist nghiệp vụ, mẫu email | Sở hữu requirement/task orchestration, agent execution và workflow context |
| Tạo mockup và đáp án kỳ vọng | Thu thập hoặc chuyển metadata/artifact MC-CIP sẵn có theo workflow sang Gate |
| Cung cấp giao diện chạy và kết quả có cấu trúc | Tích hợp AI Gate Adapter; gọi Gate và tiếp nhận response theo API contract |
| Sửa lỗi thuộc công cụ CIP | Xử lý kết quả Gate trong workflow; quản lý approval task, human approval, audit trail và evidence package tổng thể |
|  | Quản lý RBAC/SoD và trạng thái workflow; không tự đánh giá thay ruleset/compliance của Gate |

**Ranh giới trách nhiệm:**

- Đức Anh là owner của logic kiểm tra MC/CIP, checklist/ruleset, findings và việc tạo email draft.
- Vĩnh là owner của workflow SDLC, orchestration, approval workflow, audit/evidence tổng thể và phần tích hợp gọi Gate.
- AI Gate không điều phối toàn bộ SDLC và không tự phê duyệt CIP.
- Orchestrator không thay thế logic kiểm tra hoặc quyết định control của Gate. `PASS` từ Gate không đồng nghĩa với approval của con người.
- Mỗi bên duy trì khả năng phát triển và demo độc lập bằng mock/stub nếu phần còn lại chưa sẵn sàng.
- Các trách nhiệm ở cột Vĩnh là đề xuất của Vĩnh; cần Đức Anh và mentor xác nhận trước khi xem là phân công chính thức.

Công cụ CIP phải có cách chạy và đánh giá độc lập. Framework của Vĩnh có thể phát triển bằng mock/stub mà không chờ công cụ CIP. Không mặc định framework hoặc tài liệu này đã đáp ứng yêu cầu SOX.

## 3. Nội dung và định dạng trao đổi

| Chiều trao đổi | Nội dung | Định dạng đề xuất |
| --- | --- | --- |
| Đức Anh → Vĩnh | Tình huống mockup, đáp án kỳ vọng | JSON và tệp mockup |
| Đức Anh → Vĩnh | Giao diện chạy, phiên bản checklist | Tài liệu và cấu hình |
| Orchestrator → AI Gate | Workflow/task/correlation ID, requester, checkpoint, metadata và URI/version của MC-CIP, context cần thiết | REST API qua HTTP; JSON request |
| AI Gate → Orchestrator | Gate run ID, trạng thái PASS/FAIL/NEEDS_REVIEW, findings, severity, control/rule ID, evidence references, ruleset/version và trạng thái hoặc URI email draft | JSON response |
| Orchestrator → Đức Anh | Kết quả Gate gắn với workflow, findings/evidence và thông tin lỗi cần xử lý | JSON hoặc giao diện workflow; định dạng chi tiết cần thống nhất |

### 3.1. Luồng tích hợp đề xuất

```text
Developer / Workflow
        |
        v
AI SDLC Orchestrator
  - Requirement / Task
  - AI-assisted development
  - Test & review
  - Collect MC/CIP artifacts
        |
        | API request + artifact references
        v
AI Gate
  - Parse / validate MC
  - Evaluate rules
  - Produce findings & evidence
  - Prepare CIP approval email draft
        |
        | PASS / FAIL / NEEDS_REVIEW
        | findings + evidence + ruleset version
        v
AI SDLC Orchestrator
  - Display result
  - Create/continue approval task
  - Human approver decides
  - Update workflow
  - Build audit/evidence package
```

Nếu Gate trả `FAIL` hoặc `NEEDS_REVIEW`, Orchestrator giữ workflow ở trạng thái phù hợp và yêu cầu xử lý/kiểm tra tiếp. Nếu Gate trả `PASS`, workflow vẫn phải đi qua bước human approval theo quyền được cấu hình; không tự động approve, merge hoặc deploy production.

### 3.2. Giao thức và dữ liệu trao đổi

Đề xuất ban đầu từ phía Vĩnh:

- REST API qua HTTP, JSON request/response.
- OpenAPI/JSON Schema làm nguồn thống nhất cho API contract.
- Artifact truyền bằng URI/reference và metadata; không mặc định nhúng file lớn vào JSON.
- Mỗi request có `workflow_id`, `task_id` và `correlation_id` để truy vết.
- Có `schema_version` hoặc API version để quản lý thay đổi.
- Tách lỗi kỹ thuật (timeout, invalid input, service unavailable) khỏi kết quả kiểm soát (`PASS`, `FAIL`, `NEEDS_REVIEW`).

Request minh họa:

```json
{
  "schema_version": "v1",
  "workflow_id": "wf-mock-001",
  "task_id": "task-mock-001",
  "correlation_id": "corr-mock-001",
  "requested_by": {
    "user_id": "user-dev-01",
    "role": "developer"
  },
  "checkpoint": "CIP_APPROVAL",
  "artifacts": {
    "mc_document": {
      "uri": "mock://artifacts/mc-001",
      "version": "1",
      "sha256": "mock-hash"
    },
    "cip_metadata": {
      "change_id": "CHG-MOCK-001",
      "description": "Mock change description",
      "related_requirement_ids": ["REQ-MOCK-001"]
    }
  },
  "context": {
    "repository": "mock/repository",
    "pull_request_id": "PR-MOCK-001"
  }
}
```

Response minh họa:

```json
{
  "schema_version": "v1",
  "workflow_id": "wf-mock-001",
  "task_id": "task-mock-001",
  "correlation_id": "corr-mock-001",
  "gate_run_id": "gate-run-mock-001",
  "status": "NEEDS_REVIEW",
  "ruleset": {
    "id": "mock-ruleset",
    "version": "1.0"
  },
  "findings": [
    {
      "finding_id": "F-001",
      "control_id": "MC-001",
      "severity": "MEDIUM",
      "message": "Mock finding requiring human review",
      "evidence_refs": ["mock://evidence/e-001"]
    }
  ],
  "cip_email_draft": {
    "status": "DRAFTED",
    "artifact_uri": "mock://artifacts/cip-email-draft-001"
  },
  "completed_at": "2026-11-03T10:00:00+07:00"
}
```

Các payload trên chỉ là ví dụ để thảo luận, chưa phải schema đã chốt. Hai bên cần thống nhất field bắt buộc/tùy chọn, endpoint, định dạng artifact, authentication/authorization, error schema, timeout/retry, idempotency và versioning trước khi implement.

Các trường tối thiểu dự kiến cần truy vết: mã workflow, task, correlation, lần chạy Gate, mã tình huống/change, phiên bản ứng dụng/checklist/ruleset, trạng thái, kết quả từng tiêu chí, findings, evidence reference, lỗi xử lý và thời gian.

Toàn bộ nội dung trao đổi phục vụ phát triển hiện tại là mockup tự dựng: MC theo sáu mục đã xác nhận, link giả lập, tệp .msg và đáp án kỳ vọng. Không phụ thuộc dữ liệu nội bộ thật. Việc tích hợp với dữ liệu masked về sau phải theo phạm vi mentor cho phép; không đưa masked vào repo.

## 4. Mốc tích hợp và cách đo

| Mốc | Mục tiêu đề xuất |
| --- | --- |
| Gate 0 — 04/11 | Rà soát mục tiêu cộng hưởng, boundary, trách nhiệm và draft API contract; ghi rõ nội dung đã/chưa thống nhất |
| Gate 1 — 11/11 | Có skeleton end-to-end; Orchestrator gọi Gate mock/stub; kiểm chứng rủi ro API lớn nhất |
| CP1 — 18/11 | Demo MVP trên mock data; chứng minh request/response, trạng thái workflow và khả năng truy vết cơ bản |
| CP2 — 25/11 | Hoàn thiện luồng tích hợp, xử lý lỗi và evidence; dùng masked data nếu mentor cung cấp/cho phép |
| CP3 — 09/12 | Demo end-to-end, đo metric cộng hưởng và bàn giao tài liệu |

Lịch mốc theo kế hoạch thực tập: Gate 0 (04/11), Gate 1 (11/11), CP1 (18/11), CP2 (25/11), CP3 (09/12). Tuần đầu đến CP1 chỉ dùng mockup do thực tập sinh tự dựng. Dữ liệu masked chỉ được dùng từ CP2–CP3 khi mentor cung cấp. Tuyệt đối không dùng dữ liệu thật.

### Metric đề xuất

So sánh ba kịch bản trên cùng bộ mock data và cùng loại change:

- **A — Manual baseline:** chuẩn bị/kiểm tra MC-CIP và evidence thủ công.
- **B — Orchestrator only:** Orchestrator chạy workflow nhưng chưa gọi Gate.
- **C — Integrated:** Orchestrator gọi Gate, nhận findings/evidence, đưa vào human approval và evidence package.

| Metric | Cách đo |
| --- | --- |
| Gate integration success rate | Số request hợp lệ nhận response đúng schema / tổng request hợp lệ |
| Control coverage | Số rule/control mock được đánh giá / tổng rule/control trong test set |
| Traceability completeness | Số workflow có liên kết request → Gate run → finding/evidence → approval / tổng workflow |
| Evidence completeness | Số evidence bắt buộc có đủ metadata/reference / tổng evidence bắt buộc |
| Processing time | Thời gian từ lúc gửi request đến khi nhận kết quả |
| Manual effort saved | Thời gian thao tác thủ công ở A so với C |
| Exception handling | Tỷ lệ timeout/invalid response được ghi nhận và đưa workflow về trạng thái an toàn |
| Human approval integrity | Tỷ lệ trường hợp approval được thực hiện bởi đúng role và không vi phạm SoD |

Mục tiêu số cụ thể cần hai thành viên thống nhất và mentor duyệt. Không tự đặt ngưỡng đạt khi chưa có baseline và test set. Các metric trên là đề xuất để kiểm chứng giá trị cộng hưởng, không phải cam kết kết quả.

## 5. Nội dung cần hai thành viên xác nhận

- [ ] Vĩnh và Đức Anh thống nhất mục tiêu cộng hưởng tại approval/control checkpoint.
- [ ] Xác nhận ranh giới: Orchestrator sở hữu workflow/approval/audit tổng thể; Gate sở hữu logic kiểm tra MC/CIP và tạo email draft.
- [ ] Thống nhất định nghĩa "MC document" và các loại tài liệu/metadata Gate nhận.
- [ ] Thống nhất Gate chỉ tạo email draft hay có thêm thao tác gửi (đề xuất MVP chỉ tạo draft).
- [ ] Chọn endpoint và chốt REST API, OpenAPI/JSON Schema.
- [ ] Chốt request/response, status, findings/evidence schema và error schema.
- [ ] Chốt cách lưu/truyền artifact URI, version/hash.
- [ ] Chốt authentication, service identity và quyền truy cập.
- [ ] Chốt timeout, retry, idempotency và cách xử lý Gate unavailable.
- [ ] Chốt mock dataset và bộ test case chung.
- [ ] Chốt metric cộng hưởng, baseline A/B/C và cách đo.
- [ ] Chốt người phụ trách contract test, integration test và demo.
- [ ] Mentor xác nhận ranh giới và mức độ phù hợp với quy trình công ty.

## Nguồn

- [Kế hoạch thực tập 6 tuần](../../Kế%20hoạch%20thực%20tập%206%20tuần.pdf), phần Teamwork và Pair contract v0.
- [Kế hoạch MVP của Đức Anh](01-ke-hoach-mvp.md).
- `02-mvp-scope-architecture.md` — MVP Scope & Technical Architecture của Vĩnh.
- `03-pair-contract-v0-vinh.md` — đề xuất Pair Contract từ phía Vĩnh.

---

**Nguyên tắc cuối:** tích hợp để chứng minh giá trị của hai sản phẩm, không biến hai sản phẩm thành một khối phụ thuộc chặt. Orchestrator phải chạy được workflow độc lập; Gate phải kiểm tra được input độc lập; contract là ranh giới kết nối giữa hai bên.
