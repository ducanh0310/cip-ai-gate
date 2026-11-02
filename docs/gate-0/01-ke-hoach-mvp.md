# Kế hoạch MVP — AI Gate hỗ trợ quy trình CIP

- Thực tập sinh: Nguyễn Đức Anh — Cặp C.
- Mentor: MinhLQ11.
- Cập nhật: 02/11/2026.
- Trạng thái: Bản nháp phục vụ Gate 0, chưa được mentor duyệt.
- Đầu việc: C2-001, C2-002.
- Gate 0: chiều 04/11/2026.

## 1. Vấn đề, người dùng và giá trị

CIP là quy trình cần thực hiện trước khi go-live. MC document được lập theo template trên Confluence để phục vụ quy trình CIP. Công cụ cần hỗ trợ kiểm tra MC và soạn bản nháp email xin phê duyệt.

Người dùng trực tiếp dự kiến là người chuẩn bị hồ sơ CIP: cung cấp nội dung MC, xem kết quả kiểm tra, bổ sung thông tin và rà soát email. Cần mentor xác nhận chức danh và trách nhiệm cụ thể của người dùng này.

Giả thuyết giá trị: công cụ giúp giảm thời gian kiểm tra hồ sơ và soạn email, phát hiện thông tin thiếu hoặc mâu thuẫn trước khi gửi duyệt, đồng thời cung cấp căn cứ để người dùng kiểm tra lại. Chưa có số liệu hiện trạng để kết luận mức cải thiện.

## 2. Đầu vào và luồng sử dụng

Các mục trong ảnh đã được Nguyễn Đức Anh xác nhận là cấu trúc MC. Toàn bộ giá trị cụ thể, tài khoản, liên kết, email và tệp mẫu phục vụ phát triển sẽ tự dựng; không chờ tiếp cận dữ liệu hoặc tài liệu nội bộ thật.

| Mục trong MC đã xác nhận | Kiểu dữ liệu | Cách dựng mockup |
| --- | --- | --- |
| Ticket Jira | Link | URL giả lập, ví dụ `https://jira.example.test/browse/DEMO-001`; không cần gọi Jira thật |
| Service | Văn bản | Tên dịch vụ giả lập, ví dụ `Demo Notification Service` |
| Type | Văn bản | Giá trị tự định nghĩa trong danh mục mockup, ghi rõ không phải phân loại nội bộ chính thức |
| Risk | Văn bản | Mô tả rủi ro giả lập; mức phân loại nếu có là giả định của MVP |
| BO sign-off | Tệp .msg | Email xác nhận giả lập, người gửi và nội dung tự dựng |
| Request | Tệp .msg | Email yêu cầu giả lập, có thông tin nhất quán với MC |

Ví dụ trên chỉ minh họa thiết kế dữ liệu, chưa phải bộ mockup đã tạo. Các tệp .msg cần đúng định dạng và đọc được; không đổi đuôi tệp văn bản thành .msg. Cách tạo và đọc tệp sẽ được kiểm chứng ở giai đoạn skeleton.

Checklist kiểm tra và mẫu email cũng do dự án đề xuất cho MVP, tách rõ quy tắc mockup với thông tin nghiệp vụ đã xác nhận. Không coi quy tắc tự dựng là quy định CIP chính thức. Cấu trúc bố cục Confluence sẽ tự mô phỏng từ sáu mục trên, không cần template nội bộ thật.

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
| Đánh giá trên mockup | Đối chiếu với đáp án kỳ vọng |

Ngoài phạm vi đề xuất: tự gửi email, tự phê duyệt, ghi lên Confluence/Jira, tra cứu hệ thống nội bộ thật và hỗ trợ nhiều template.

## 4. Success metric dự kiến

| Metric | Cách đo dự kiến |
| --- | --- |
| Khả năng phát hiện lỗi | Số lỗi phát hiện đúng / tổng lỗi đã gắn nhãn |
| Chất lượng cảnh báo | Số cảnh báo đúng / tổng cảnh báo do công cụ đưa ra |
| Độ đúng của căn cứ | Số kết luận có căn cứ đúng / tổng kết luận cần căn cứ |
| Chất lượng email | Đánh giá độ đầy đủ, chính xác và lượng chỉnh sửa theo checklist email |
| Thời gian xử lý | So sánh thời gian kiểm tra và soạn email có/không có công cụ trên cùng bộ hồ sơ |

Ngưỡng mục tiêu, cách xử lý mẫu số bằng 0, bộ đánh giá và rubric mức 2–3–4 sẽ được xây dựng tại C2-004 ngày 03/11 và trình mentor duyệt. Chưa có baseline thực đo.

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

Giả định rủi ro nhất đề xuất cho Gate 1: có thể trích xuất MC đủ chính xác để kiểm tra theo checklist và dẫn căn cứ đúng vị trí. Kiểm chứng trên mockup có bảng, mục thiếu và thông tin mâu thuẫn, đối chiếu với đáp án kỳ vọng.

## 6. Lộ trình và việc còn mở

| Mốc | Đầu ra |
| --- | --- |
| Gate 0 — 04/11 | Kế hoạch, rubric, pair contract v0, đặc tả mockup, rủi ro và phụ thuộc |
| Gate 1 — 11/11 | Skeleton xuyên suốt, kiểm chứng giả định, baseline, backlog Sprint 1 |
| CP1 — 18/11 | Demo MVP trên mockup và tiến độ |
| CP2 — 25/11 | MVP trên masked, kết quả Sprint 1, retro |
| CP3 — 09/12 | Final demo, metric và bàn giao |

Phạm vi phát triển hiện tại sử dụng hoàn toàn dữ liệu tự dựng theo xác nhận của Nguyễn Đức Anh. Kế hoạch chương trình có mốc dữ liệu masked từ 19/11; nếu sau này mentor cung cấp thì chỉ dùng trong phạm vi được phép, lưu riêng và không commit. Không phụ thuộc việc có masked để dựng MVP và không dùng dữ liệu thật.

Câu hỏi cần chốt với mentor:

- Sáu mục MC đã rõ; cần đề xuất và thống nhất tiêu chí bắt buộc, hợp lệ và nhất quán trên bộ mockup, không yêu cầu template hoặc hồ sơ thật.
- Ai trực tiếp sử dụng công cụ? T2 nhận và phê duyệt theo điều kiện nào?
- CR, kết quả UAT và MC liên kết với nhau ở đâu, bằng bằng chứng gì?
- BO sign-off và Request có bắt buộc không? MVP có cần đọc nội dung .msg?
- Mẫu email tự dựng, người nhận/CC giả lập và danh sách đính kèm đề xuất có phù hợp phạm vi MVP không?
- Phương án nhận HTML mockup và tệp .msg có phù hợp không? Công cụ AI nào được phép sử dụng?
- Ai rà soát tính hợp lý của đáp án mockup và ngưỡng thành công?

## Nguồn

- [Kế hoạch thực tập 6 tuần](../../Kế%20hoạch%20thực%20tập%206%20tuần.pdf).
- [Theo dõi tiến độ Cặp C](../../Theo_doi_tien_do_thuc_tap(Cặp%20C).csv).
- [Ảnh ghi chú nghiệp vụ](../../Pasted%20image.png), đọc cùng các đính chính của Nguyễn Đức Anh trong chat ngày 02/11/2026.

Tài liệu này chưa phải bộ Gate 0 hoàn chỉnh. Metric/rubric chi tiết, đặc tả mockup và danh sách rủi ro riêng thuộc kế hoạch ngày 03/11.
