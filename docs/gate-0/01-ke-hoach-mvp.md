# Kế hoạch MVP — AI Gate hỗ trợ quy trình CIP

- Thực tập sinh: Nguyễn Đức Anh — Cặp C.
- Mentor: MinhLQ11.
- Cập nhật: 03/11/2026.
- Trạng thái: Kế hoạch phục vụ Gate 0.
- Gate 0: chiều 04/11/2026.

## 1. Vấn đề, người dùng và giá trị

CIP là quy trình cần thực hiện trước khi go-live. MC document được lập theo template trên Confluence để phục vụ quy trình CIP. Công cụ cần hỗ trợ kiểm tra MC và soạn bản nháp email xin phê duyệt.

Người dùng trực tiếp là người chuẩn bị hồ sơ CIP: cung cấp nội dung MC, xem kết quả kiểm tra, bổ sung thông tin và rà soát email.

Giả thuyết giá trị: công cụ giúp giảm thời gian kiểm tra hồ sơ và soạn email, phát hiện thông tin thiếu hoặc mâu thuẫn trước khi gửi duyệt, đồng thời cung cấp căn cứ để người dùng kiểm tra lại. Chưa có số liệu hiện trạng để kết luận mức cải thiện.

## 2. Đầu vào và luồng sử dụng

Toàn bộ giá trị cụ thể, tài khoản, liên kết, email và tệp mẫu phục vụ phát triển sẽ tự dựng; không chờ tiếp cận dữ liệu hoặc tài liệu nội bộ thật.

| Mục trong MC đã xác nhận | Kiểu dữ liệu | Cách dựng mockup |
| --- | --- | --- |
| Ticket Jira | Link | URL giả lập, ví dụ `https://jira.example.test/browse/DEMO-001`; không cần gọi Jira thật |
| Service | Văn bản | Tên dịch vụ giả lập, ví dụ `Demo Notification Service` |
| Type | Văn bản | Giá trị tự định nghĩa trong danh mục mockup, ghi rõ không phải phân loại nội bộ chính thức |
| Risk | Văn bản | Mô tả rủi ro giả lập; mức phân loại nếu có là giả định của MVP |
| BO sign-off | Tệp .msg | Email xác nhận giả lập, người gửi và nội dung tự dựng |
| Request | Tệp .msg | Email yêu cầu giả lập, có thông tin nhất quán với MC |

Quy ước dữ liệu và các tình huống mock được đặc tả tại mục 7. Các tệp .msg cần đúng định dạng và đọc được; không đổi đuôi tệp văn bản thành .msg. Cách tạo và đọc tệp sẽ được kiểm chứng ở giai đoạn skeleton.

Checklist kiểm tra và mẫu email do dự án đề xuất cho MVP, tách rõ quy tắc mockup với thông tin nghiệp vụ đã xác nhận. Không coi quy tắc tự dựng là quy định CIP chính thức. Cấu trúc bố cục Confluence sẽ tự mô phỏng từ sáu mục trên, không cần template nội bộ thật. Checklist/prompt/mẫu email cần quản lý phiên bản; lỗi đọc và lỗi LLM phải phân biệt với kết luận nghiệp vụ.

Luồng đề xuất:

1. Nhận nội dung MC và bằng chứng mockup liên quan.
2. Trích xuất các mục, trường và vị trí nguồn.
3. Kiểm tra bằng quy tắc và AI theo checklist đã xác nhận.
4. Hiển thị tiêu chí đạt, chưa đạt, cần xem xét; kèm căn cứ và gợi ý bổ sung.
5. Soạn bản nháp email; đánh dấu thông tin còn thiếu.
6. Người dùng rà soát trước khi sử dụng kết quả và email.

Việc T4 làm UAT và T3 viết CR gửi T2 là bối cảnh đã biết. Chưa suy diễn thành thứ tự đầy đủ của quy trình CIP hoặc điều kiện phê duyệt.

## 3. Phạm vi MVP đề xuất

| Trong phạm vi | Kết quả mong đợi |
| --- | --- |
| Một template MC mockup tự dựng theo sáu mục đã xác nhận, một phương thức đầu vào | Nhận diện được các mục và tệp đính kèm |
| Kiểm tra trường bắt buộc | Liệt kê mục thiếu hoặc chưa điền |
| Kiểm tra tính nhất quán theo quy tắc đã xác nhận | Chỉ ra thông tin xung đột kèm căn cứ |
| AI kiểm tra nội dung theo checklist | Nhận xét có trích đoạn; thiếu căn cứ thì chuyển cần xem xét |
| Báo cáo kiểm tra | Trạng thái từng tiêu chí và gợi ý xử lý |
| Sinh email theo mẫu | Bản nháp dùng thông tin có trong hồ sơ, đánh dấu phần thiếu |
| Đánh giá trên mockup | Đối chiếu với đáp án kỳ vọng, ghi phiên bản cấu hình và thời gian |

Ngoài phạm vi đề xuất: tự gửi email, tự phê duyệt, ghi lên Confluence/Jira, tra cứu hệ thống nội bộ thật và hỗ trợ nhiều template.

## 4. Success metric và rubric đánh giá

### 4.1. Metric và ngưỡng mục tiêu

| Metric | Cách đo | Ngưỡng mục tiêu |
| --- | --- | --- |
| Precision phát hiện thiếu | TP / (TP + FP) | ≥ 90% |
| Recall phát hiện thiếu | TP / (TP + FN) | ≥ 90% |
| Độ đúng căn cứ | Số căn cứ đúng / tổng căn cứ được trả ra | ≥ 95% |
| Email đạt checklist | Số email đạt mọi tiêu chí / tổng email sinh thành công | ≥ 90% |
| Email có thông tin thiếu căn cứ | Số email có ít nhất một khẳng định thiếu căn cứ / tổng email sinh thành công | Không quan sát email thiếu căn cứ trên bộ đánh giá; không suy rộng thành bảo đảm ngoài bộ này |
| Giảm thời gian hoàn thành | (Trung vị thời gian thủ công − trung vị thời gian có công cụ) / trung vị thời gian thủ công | ≥ 20% |

Đơn vị TP/FP/FN là cặp `(case_id, criterion_id)`: TP là mục thiếu được phát hiện đúng; FP là mục không thiếu bị cảnh báo thiếu; FN là mục thiếu bị bỏ sót. Mẫu số bằng 0 ghi N/A kèm số đếm, không quy đổi thành 100%. Lỗi đọc và lỗi sinh email được thống kê riêng, cùng tổng case đủ điều kiện và tổng case xử lý thành công.

Checklist email gồm: đúng thông tin hồ sơ; đúng trạng thái kiểm tra; thể hiện các mục cần bổ sung; không tự thêm người nhận hoặc phê duyệt; không bịa dữ liệu; nội dung yêu cầu rõ ràng. Người rà soát ghi nhãn đạt/không đạt cùng lý do.

Phép đo thời gian dùng cùng bộ hồ sơ và người thực hiện, tính cả thời gian rà soát và sửa email; cân bằng thứ tự thủ công/có công cụ để giảm ảnh hưởng ghi nhớ. Báo cáo ghi số mẫu, điều kiện đo và phiên bản checklist/prompt/cấu hình LLM. Baseline được đo tại Gate 1; các ngưỡng trên là mục tiêu đánh giá của MVP.

### 4.2. Rubric mức 2–3–4

Rubric áp dụng cho checkpoint; Gate 0 và Gate 1 đánh giá theo đạt/chưa đạt.

| Tiêu chí | 2 — Đạt | 3 — Tốt | 4 — Xuất sắc |
| --- | --- | --- | --- |
| Giá trị và kết quả | Chạy đủ luồng kiểm tra và email; precision/recall ≥ 80%, email đạt checklist ≥ 80% trên tập được phép; thể hiện rõ lỗi xử lý. | Đạt toàn bộ ngưỡng mục 4.1 trên dữ liệu masked được cấp và được phép dùng; có ít nhất một stakeholder dùng thử và ghi nhận phản hồi. | Precision/recall ≥ 95%, email đạt checklist ≥ 95%, căn cứ đúng ≥ 98%, giảm thời gian ≥ 30%, không quan sát email thiếu căn cứ; stakeholder xác nhận muốn đưa MVP đi tiếp. |
| Chất lượng kỹ thuật | Có hướng dẫn chạy, schema và cấu hình có phiên bản; cả sáu nhóm mockup có đầu ra đối chiếu đáp án; mã nguồn đọc hiểu được. | Bộ đánh giá chạy lại bằng một lệnh; kiểm tra schema/lỗi, lưu kết quả từng case và cấu hình LLM; đánh giá có hệ thống phần AI và tuân thủ dữ liệu. | Ít nhất một người khác chạy lại theo tài liệu và thêm một rule hoặc case mà không cần hướng dẫn trực tiếp; có minh chứng bàn giao và kết quả regression. |
| Thực thi và chủ động | Hoàn thành ≥ 80% đầu việc đến hạn đã chốt, có bằng chứng. | Hoàn thành ≥ 90%; báo rủi ro ngay khi ghi nhận và trước hạn bị ảnh hưởng; ghi hướng xử lý góp ý trong hai ngày làm việc. | Đạt mức 3; có ít nhất một điều chỉnh kế hoạch dựa trên số liệu và một đóng góp giúp đồng đội được xác nhận. |

CP1 đánh giá trên mockup; CP2/CP3 dùng masked khi được cấp và được phép sử dụng. Nếu không có masked, cần thống nhất phương án đánh giá thay thế trước checkpoint và ghi rõ phạm vi dữ liệu khi báo cáo. Thay đổi phạm vi công việc phải được ghi nhận trước hạn và thống nhất khi tính tỷ lệ hoàn thành.

## 5. Kiến trúc sơ bộ

Đề xuất skeleton nhận HTML mockup mô phỏng trang Confluence cùng hai tệp .msg giả lập. Nội dung trang, tệp và liên kết đều tự dựng; các link Jira/Confluence giả không cần truy cập mạng. Tích hợp Confluence thật không phải điều kiện để phát triển hoặc demo MVP. Cách đóng gói đầu vào và công cụ đọc .msg sẽ được kiểm chứng ở giai đoạn skeleton.

```mermaid
flowchart TD
    A[MC và bằng chứng mockup] --> B[Tiếp nhận và trích xuất]
    B --> C[MC có cấu trúc và vị trí nguồn]
    C --> D[Kiểm tra bằng quy tắc]
    C --> E[AI kiểm tra nội dung]
    F[Checklist có phiên bản] --> D
    F --> E
    D --> G[Tổng hợp kết quả và căn cứ]
    E --> G
    C --> H[Soạn bản nháp email]
    G --> H
    I[Mẫu email] --> H
    G --> J[Giao diện rà soát]
    H --> J
```

| Thành phần | Trách nhiệm |
| --- | --- |
| Tiếp nhận, trích xuất | Kiểm tra định dạng; đọc tiêu đề, bảng, trường; giữ vị trí nguồn |
| Bộ quy tắc | Xử lý điều kiện xác định, trường bắt buộc và định dạng |
| AI kiểm tra | Đọc hiểu theo checklist, trả nhận xét có căn cứ |
| Tổng hợp | Chuẩn hóa kết quả; đánh dấu thiếu dữ liệu, lỗi xử lý và kết quả xung đột |
| Soạn email | Điền mẫu từ dữ liệu có căn cứ, đánh dấu phần thiếu |
| Giao diện | Xem lỗi, căn cứ và sao chép bản nháp |
| Bộ đánh giá | So sánh với đáp án mockup, ghi nhận kết quả và thời gian |

Kết quả mỗi tiêu chí đề xuất gồm: `criterion_id`, `status` (`pass`, `fail`, `needs_review`), `reason`, `evidence` (trích đoạn và vị trí), `suggestion`, `checker`, `checklist_version`.

Nguyên tắc: không đọc được tài liệu không được mặc định là đạt; kết quả AI phải đúng cấu trúc; không tự tạo người phê duyệt hoặc thông tin còn thiếu. Checklist và mẫu email được quản lý riêng, có phiên bản. Lựa chọn công nghệ cụ thể và công cụ AI cần xác nhận tính khả dụng trước khi chốt.

Giả định rủi ro nhất đề xuất cho Gate 1: có thể trích xuất MC đủ chính xác để kiểm tra theo checklist và dẫn căn cứ đúng vị trí. Kiểm chứng trên mockup có bảng, mục thiếu và thông tin mâu thuẫn, đối chiếu với đáp án kỳ vọng. Nếu trích xuất không chắc chắn hoặc không đọc được, báo lỗi/`needs_review`, không mặc định đạt.

## 6. Lộ trình và việc còn mở

| Mốc | Đầu ra |
| --- | --- |
| Gate 0 — 04/11 | Kế hoạch, rubric, pair contract v0, đặc tả mockup, rủi ro và phụ thuộc |
| Gate 1 — 11/11 | Skeleton xuyên suốt, kiểm chứng giả định, baseline, backlog Sprint 1 |
| CP1 — 18/11 | Demo MVP trên mockup và tiến độ |
| CP2 — 25/11 | MVP trên masked, kết quả Sprint 1, retro |
| CP3 — 09/12 | Final demo, metric và bàn giao |

## 7. Đặc tả dữ liệu mock — phiên bản v1

### 7.1. Cấu trúc bộ dữ liệu

Bộ mock gồm 24 hồ sơ, chia thành `dev` (12 hồ sơ) và `eval` (12 hồ sơ). Mỗi tập có hai hồ sơ cho mỗi nhóm: đầy đủ, thiếu mục/trường trống, thiếu bằng chứng, sai định dạng/lỗi đọc, không nhất quán và biến thể bố cục. Đây là đặc tả để tạo dữ liệu, không phải báo cáo dữ liệu đã được sinh hoặc kiểm thử.

```text
mock/v1/
├── checklist.json
├── dev/
│   └── CIP-DEV-001/
│       ├── manifest.json
│       ├── mc.html
│       ├── attachments/
│       │   ├── bo-sign-off.msg
│       │   └── request.msg
│       └── expected.json
└── eval/
    └── CIP-EVAL-001/
        └── ... (cùng cấu trúc với dev)
```

`mc.html` và các tệp trong `attachments/` là đầu vào của công cụ. `manifest.json` phục vụ bộ chạy đánh giá; `expected.json` là đáp án, không được đưa vào parser, prompt kiểm tra hoặc prompt sinh email. Đường dẫn tệp là đường dẫn tương đối trong thư mục hồ sơ. Tệp thiếu hoặc hỏng chỉ xuất hiện trong tình huống lỗi có chủ đích.

### 7.2. Nội dung MC và email bằng chứng

Các quy ước dưới đây là quy tắc riêng của mock v1, không phải quy định CIP chính thức. Sáu mục đều bắt buộc trong hồ sơ đầy đủ.

| Khóa chuẩn | Nhãn trong HTML | Kiểu và điều kiện hợp lệ của mock v1 | Giá trị mẫu |
| --- | --- | --- | --- |
| `ticket_jira` | Ticket Jira | URL dạng `https://jira.example.test/browse/DEMO-<số>`; mã ticket được lấy từ phần cuối URL | `https://jira.example.test/browse/DEMO-001` |
| `service` | Service | Văn bản không rỗng sau khi bỏ khoảng trắng đầu/cuối | `Demo Notification Service` |
| `type` | Type | Một trong `standard`, `normal`, `emergency`; danh mục chỉ dùng cho mock | `normal` |
| `risk` | Risk | Văn bản mô tả rủi ro và cách xử lý, không chỉ ghi mức rủi ro | `Thông báo có thể bị trễ; theo dõi hàng đợi và rollback nếu lỗi tăng.` |
| `bo_sign_off` | BO sign-off | Liên kết tới `attachments/bo-sign-off.msg`; tệp đọc được, có nội dung xác nhận rõ cho cùng ticket/service | Email xác nhận mock |
| `request` | Request | Liên kết tới `attachments/request.msg`; tệp đọc được, có yêu cầu cho cùng ticket/service | Email yêu cầu mock |

HTML dùng UTF-8, chứa sáu mục trong bảng nhãn–giá trị hoặc các section có heading. Link tệp dùng đường dẫn tương đối; link Jira không cần truy cập mạng. Bộ trích xuất phải giữ được vị trí theo CSS selector hoặc đường dẫn phần tử, không phụ thuộc duy nhất vào thứ tự hàng.

Hai email dùng định dạng Outlook `.msg` thực, có các trường `sender`, `to`, `cc`, `subject`, `sent_at`, `body`. Người gửi/nhận dùng miền `example.test`; thời gian biểu diễn theo ISO 8601 có múi giờ. Mỗi body chứa `Ticket: DEMO-001` và `Service: Demo Notification Service`. BO sign-off có thêm câu xác nhận `Tôi xác nhận đồng ý với yêu cầu DEMO-001 cho Demo Notification Service.`; Request có câu `Đề nghị triển khai DEMO-001 cho Demo Notification Service.`. Đây là nội dung của bằng chứng đầu vào, không phải email xin phê duyệt do công cụ sinh.

Đối chiếu ticket sau khi trim và chuẩn hóa chữ hoa; service sau khi trim, gộp khoảng trắng và chuyển chữ thường. Không suy đoán hai tên dịch vụ khác nhau là cùng một dịch vụ. Thiếu nội dung để đối chiếu hoặc xác nhận ý nghĩa thì trả `needs_review`.

### 7.3. Manifest và đáp án

Ví dụ `manifest.json` cho hồ sơ đầy đủ:

```json
{
  "dataset_version": "v1",
  "checklist_version": "mock-v1",
  "case_id": "CIP-DEV-001",
  "split": "dev",
  "group": "complete",
  "input": {
    "mc": "mc.html",
    "attachments": ["attachments/bo-sign-off.msg", "attachments/request.msg"]
  },
  "intentional_faults": []
}
```

`case_id` là duy nhất; `split` nhận `dev` hoặc `eval`; `group` nhận `complete`, `missing_field`, `missing_evidence`, `invalid_input`, `inconsistent` hoặc `layout_variant`. `input.attachments` chỉ liệt kê tệp thực có trong gói. `intentional_faults` là mảng đối tượng `{target, fault}` mô tả lỗi chủ đích, chỉ dùng khi đánh giá và không truyền cho công cụ kiểm tra.

| Thành phần trong `expected.json` | Nội dung bắt buộc |
| --- | --- |
| `case_id`, `dataset_version`, `checklist_version` | Khớp manifest và checklist |
| `fields` | Đủ sáu khóa chuẩn; mỗi trường chứa `value`, `state`, `sources`; email có thêm `reference` và dữ liệu email đọc được |
| `criteria` | Đủ các tiêu chí trong checklist; mỗi mục có `criterion_id`, `status`, `reason`, `evidence`, `is_missing` |
| `expected_errors` | Danh sách `{code, source_file}`; rỗng nếu không có lỗi xử lý |
| `email` | `allowed_facts`, `missing_information`, `forbidden_claims`; dùng chấm nội dung, không yêu cầu email khớp nguyên văn |

`state` nhận `present`, `missing`, `empty`, `missing_file`, `unreadable` hoặc `invalid`; `value` là `null` khi không có giá trị đọc được. `sources` và `evidence` là các mảng đối tượng `{source_file, location, excerpt}`. Trường bị thiếu dùng vị trí vùng MC đã kiểm tra với `excerpt: null`; tệp thiếu/hỏng dùng vị trí liên kết trong MC. Không dựng trích đoạn cho nội dung không đọc được.

`is_missing` là nhãn boolean để tính precision/recall phát hiện thiếu: `true` khi thiếu mục, mục trống hoặc thiếu tệp bằng chứng; `false` cho lỗi định dạng, lỗi đọc và mâu thuẫn. Các lỗi này vẫn được chấm bằng trạng thái tiêu chí và thống kê lỗi riêng.

### 7.4. Checklist gắn nhãn

`checklist.json` chứa `version: mock-v1` và mảng tiêu chí với `criterion_id`, mô tả, điều kiện `pass`/`fail`/`needs_review`. Các mã sau được dùng nhất quán trong đáp án và đầu ra:

| Mã tiêu chí | Điều kiện đánh giá |
| --- | --- |
| `MC-01`–`MC-06` | Theo thứ tự sáu trường tại mục 7.2: có mục và có giá trị/tham chiếu không rỗng thì `pass`; thiếu/trống thì `fail` |
| `FMT-01` | Ticket Jira đúng định dạng mock thì `pass`; có giá trị sai định dạng thì `fail`; thiếu trường thì `needs_review` |
| `FMT-02` | Type thuộc danh mục mock thì `pass`; ngoài danh mục thì `fail`; thiếu trường thì `needs_review` |
| `FILE-01`, `FILE-02` | Lần lượt BO sign-off và Request: tệp hiện diện thì `pass`; tham chiếu có nhưng tệp thiếu thì `fail`; không có tham chiếu thì `needs_review` |
| `READ-01`, `READ-02` | Tệp đọc thành công thì `pass`; tệp hỏng/sai định dạng thì `needs_review` và ghi lỗi `MSG_READ_ERROR`; không có tệp thì `needs_review` |
| `MATCH-01`, `MATCH-02` | Lần lượt đối chiếu ticket và service giữa MC với cả hai email; khớp thì `pass`, có xung đột rõ thì `fail`, thiếu dữ liệu đối chiếu thì `needs_review` |
| `CONTENT-01` | BO sign-off xác nhận rõ cùng ticket/service thì `pass`; từ chối rõ hoặc xác nhận cho ticket/service khác thì `fail`; mơ hồ hoặc thiếu nội dung thì `needs_review` |
| `CONTENT-02` | Request có yêu cầu rõ cùng ticket/service thì `pass`; nội dung rõ ràng cho yêu cầu khác thì `fail`; mơ hồ hoặc thiếu nội dung thì `needs_review` |

Mỗi lỗi chỉ gắn `is_missing: true` cho tiêu chí trực tiếp phản ánh thiếu: `MC-*` khi thiếu/trống mục, `FILE-*` khi thiếu tệp. Các tiêu chí phụ thuộc dữ liệu thiếu trả `needs_review` và `is_missing: false`, tránh đếm lặp cùng một lỗi thiếu.

### 7.5. Danh sách hồ sơ và kết quả kỳ vọng

Mỗi ID trong bảng dưới đây mang tiền tố `CIP-`. Hồ sơ lỗi được tạo từ hồ sơ đầy đủ của cùng tập bằng thay đổi được chỉ định; các thành phần còn lại giữ hợp lệ. Tập eval dùng ticket, tên service, nội dung Risk và danh tính email khác tập dev.

| Nhóm | ID dev / biến thể | ID eval / biến thể | Kết quả chính |
| --- | --- | --- | --- |
| Đầy đủ | `DEV-001`: Type normal; `DEV-002`: Type standard | `EVAL-001`: Type emergency; `EVAL-002`: Type normal | Tất cả tiêu chí `pass`; không có lỗi xử lý |
| Thiếu mục/trường trống | `DEV-003`: bỏ Service; `DEV-004`: Risk chỉ có khoảng trắng | `EVAL-003`: bỏ Ticket Jira; `EVAL-004`: Type rỗng | Lần lượt `MC-02`, `MC-04`, `MC-01`, `MC-03` là `fail` và `is_missing: true`; tiêu chí phụ thuộc dữ liệu thiếu là `needs_review` |
| Thiếu bằng chứng | `DEV-005`: thiếu tệp BO sign-off; `DEV-006`: thiếu tệp Request | `EVAL-005`: thiếu tệp BO sign-off; `EVAL-006`: thiếu tệp Request | Giữ link trong MC; `FILE-01` hoặc `FILE-02` là `fail`, `is_missing: true`; tiêu chí đọc/nội dung liên quan là `needs_review` |
| Sai định dạng/lỗi đọc | `DEV-007`: URL Jira sai; `DEV-008`: BO sign-off.msg bị cắt hỏng | `EVAL-007`: URL Jira sai; `EVAL-008`: Request.msg chứa văn bản thuần có chủ đích | URL sai: `FMT-01: fail`, `MATCH-01: needs_review`; tệp lỗi: `READ-* : needs_review` và `MSG_READ_ERROR`; không gắn nhãn thiếu |
| Không nhất quán | `DEV-009`: ticket Request khác MC; `DEV-010`: service BO sign-off khác MC | `EVAL-009`: ticket BO sign-off khác MC; `EVAL-010`: service Request khác MC | `MATCH-01` hoặc `MATCH-02: fail`; tiêu chí nội dung của email khác hồ sơ là `fail`; giữ căn cứ từ hai nguồn mâu thuẫn |
| Biến thể bố cục | `DEV-011`: đảo thứ tự hàng; `DEV-012`: đổi bảng thành section | `EVAL-011`: chia sáu mục vào hai bảng; `EVAL-012`: đổi thứ tự section và thêm wrapper HTML | Giá trị và kết quả như hồ sơ đầy đủ; vị trí căn cứ phản ánh đúng HTML từng hồ sơ |

Đáp án email chỉ cho phép dùng dữ liệu đọc được từ hồ sơ, kèm nguồn và trạng thái kiểm tra. Thông tin mâu thuẫn phải được nêu là mâu thuẫn; thông tin thiếu dùng dấu `[CẦN BỔ SUNG: ...]`. Không tự tạo người phê duyệt, cấp bậc, người nhận/CC hoặc tuyên bố hồ sơ đã được duyệt. Không đưa vào email các giá trị chỉ có trong đáp án.

Tập `eval` được giữ riêng, không dùng làm ví dụ prompt hoặc chỉnh luật. Nếu một hồ sơ eval đã được dùng để chỉnh hệ thống, ghi nhận việc sử dụng và thay hồ sơ đó trước khi báo cáo đánh giá độc lập. Repo chỉ chứa dữ liệu tự dựng; masked được quản lý riêng khi có quyền sử dụng.

## 8. Rủi ro và phụ thuộc

| ID | Rủi ro / phụ thuộc | Ảnh hưởng và xử lý đề xuất |
| --- | --- | --- |
| R-01 | Checklist hoặc điều kiện hợp lệ chưa rõ | Kết luận đủ/thiếu có thể sai; rà từng tiêu chí, ghi điều kiện đạt và phiên bản checklist. |
| R-02 | Trích xuất HTML/.msg sai hoặc thiếu | Sai dữ liệu/căn cứ; đối chiếu đáp án, giữ vị trí nguồn, báo lỗi hoặc `needs_review`. |
| R-03 | LLM thêm thông tin hoặc sai schema | Báo cáo/email không đáng tin; kiểm tra schema, đối chiếu nguồn, đánh dấu thiếu dữ liệu và đo trên mockup. |
| R-05 | Mockup thiếu tình huống hoặc nhãn sai | Metric không đại diện; phủ đủ sáu nhóm, rà đáp án và tách tập phát triển/đánh giá. |
| R-07 | So sánh thời gian không công bằng | Kết luận tiết kiệm thời gian không đáng tin; dùng cùng hồ sơ/người làm, cân bằng thứ tự và tính cả rà soát/sửa. |
| R-08 | Chưa có cách xác định cấp bậc nhân viên | Chưa đủ căn cứ kiểm tra cấp bậc/vai trò; xác định nguồn phù hợp, dùng bảng ánh xạ giả lập cho MVP và chuyển cần xác nhận khi thiếu, không suy đoán. |
| D-01 | Thống nhất pair contract và giao diện tích hợp với Vĩnh | Ranh giới, schema trao đổi và mốc tích hợp có thể chưa chốt; dùng phương án đề xuất, ghi rõ phần hai bên xác nhận. |
| D-02 | Quy tắc CIP/mẫu email và dữ liệu masked phụ thuộc mentor | Không dùng giả định thành chính sách; MVP tiếp tục bằng mockup. Chỉ dùng masked từ 19/11 nếu được cấp và cho phép, lưu theo hướng dẫn, không commit. |

Phạm vi phát triển hiện tại sử dụng hoàn toàn dữ liệu tự dựng theo xác nhận của Nguyễn Đức Anh. Kế hoạch chương trình có mốc dữ liệu masked từ 19/11; nếu sau này mentor cung cấp thì chỉ dùng trong phạm vi được phép, lưu riêng và không commit. Không phụ thuộc việc có masked để dựng MVP và không dùng dữ liệu thật.

Các vấn đề nghiệp vụ cần làm rõ:

- Sáu mục MC đã rõ; cần đề xuất và thống nhất tiêu chí bắt buộc, hợp lệ và nhất quán trên bộ mockup, không yêu cầu template hoặc hồ sơ thật.
- Ai trực tiếp sử dụng công cụ? T2 nhận và phê duyệt theo điều kiện nào?
- CR, kết quả UAT và MC liên kết với nhau ở đâu, bằng bằng chứng gì?
- BO sign-off và Request có bắt buộc không? MVP có cần đọc nội dung .msg?
- Mẫu email tự dựng, người nhận/CC giả lập và danh sách đính kèm đề xuất có phù hợp phạm vi MVP không?
- Phương án nhận HTML mockup và tệp .msg có phù hợp không? Công cụ AI nào được phép sử dụng?
- Ai rà soát tính hợp lý của đáp án mockup và ngưỡng thành công?
