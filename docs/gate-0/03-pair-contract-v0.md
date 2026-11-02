# Pair contract v0 — Đề xuất phối hợp Cặp C

- Thành viên: Nguyễn Đức Anh và Nguyễn Ngọc Vĩnh.
- Cập nhật: 02/11/2026.
- Trạng thái: Bản đề xuất từ phía bài toán CIP, chưa được Vĩnh thống nhất.
- Đầu việc hôm nay: C2-003. Thống nhất contract tại C2-006 ngày 03/11.

## 1. Điểm giao nhau và giá trị cộng hưởng

Đức Anh xây công cụ AI Gate kiểm tra MC trên Confluence và soạn email xin phê duyệt CIP. Vĩnh phụ trách MVP SDLC AI: framework điều phối phát triển và kiểm thử bằng AI, SOX-ready, định hướng TDD.

Đề xuất sử dụng framework của Vĩnh để điều phối chạy bộ đánh giá công cụ CIP, tổng hợp sai lệch và chạy lại sau thay đổi. Giá trị cần đo là giảm thao tác đánh giá thủ công và phát hiện suy giảm chất lượng khi thay đổi mã nguồn, checklist hoặc prompt.

Đây là phương án cần trao đổi; chưa có bằng chứng tích hợp hoặc giá trị thực đo.

## 2. Trách nhiệm và ranh giới

| Đức Anh | Vĩnh — đề xuất, chờ thống nhất |
| --- | --- |
| Xây công cụ kiểm tra MC và soạn email | Cung cấp cơ chế điều phối chạy đánh giá |
| Sở hữu checklist nghiệp vụ, mẫu email | Thu thập, tổng hợp kết quả chạy |
| Tạo mockup và đáp án kỳ vọng | Hỗ trợ đưa đánh giá vào quy trình phát triển |
| Cung cấp giao diện chạy và kết quả có cấu trúc | Gọi giao diện, báo cáo lỗi và chạy lại |
| Sửa lỗi thuộc công cụ CIP | Sửa lỗi thuộc framework điều phối |

Công cụ CIP phải có cách chạy và đánh giá độc lập. Framework của Vĩnh có thể dùng dữ liệu mẫu để phát triển mà không chờ công cụ CIP. Không mặc định framework hoặc tài liệu này đã đáp ứng yêu cầu SOX.

## 3. Nội dung và định dạng trao đổi

| Chiều trao đổi | Nội dung | Định dạng đề xuất |
| --- | --- | --- |
| Đức Anh → Vĩnh | Tình huống mockup, đáp án kỳ vọng | JSON và tệp mockup |
| Đức Anh → Vĩnh | Giao diện chạy, phiên bản checklist | Tài liệu và cấu hình |
| Framework → công cụ CIP | Yêu cầu chạy bộ đánh giá | CLI hoặc API, cần chọn một phương thức |
| Công cụ CIP → framework | Kết quả từng tiêu chí, lỗi xử lý, thời gian | JSON |
| Framework → Đức Anh | Báo cáo sai lệch, kết quả chạy lại | JSON hoặc Markdown |

Các trường giao diện tối thiểu dự kiến: mã lần chạy, mã tình huống, phiên bản ứng dụng/checklist, kết quả từng tiêu chí, lỗi xử lý và thời gian. Schema chính thức, vị trí lưu và cách xử lý lỗi cần hai bên thống nhất.

Toàn bộ nội dung trao đổi phục vụ phát triển hiện tại là mockup tự dựng: MC theo sáu mục đã xác nhận, link giả lập, tệp .msg và đáp án kỳ vọng. Không phụ thuộc dữ liệu nội bộ thật. Việc tích hợp với dữ liệu masked về sau phải theo phạm vi mentor cho phép; không đưa masked vào repo.

## 4. Mốc tích hợp và cách đo

| Mốc | Mục tiêu đề xuất |
| --- | --- |
| 03/11 | Thống nhất contract, trách nhiệm và giao diện trao đổi |
| Gate 1 — 11/11 | Có mẫu trao đổi, hai bên chạy độc lập |
| CP1 — 18/11 | Thử điều phối đánh giá trên mockup |
| CP2 — 25/11 | Demo luồng tích hợp và xử lý lỗi |
| CP3 — 09/12 | Demo luồng hoàn thiện và số liệu cộng hưởng |

Metric đề xuất:

- Thời gian và số thao tác chạy cùng một bộ đánh giá trước/sau tích hợp.
- Số tình huống được chạy tự động / tổng tình huống dự kiến tự động hóa.
- Số lỗi suy giảm được phát hiện qua các lần thay đổi, có đối chiếu xác nhận.

Chưa cam kết mức điểm cộng hoặc tích hợp hai chiều. Mức tích hợp và ngưỡng metric phải được hai bên thống nhất theo khả năng thực hiện.

## 5. Nội dung cần thống nhất ngày 03/11

- [ ] Vĩnh xác nhận hướng phối hợp có phù hợp bài toán của mình.
- [ ] Hai bên xác nhận trách nhiệm và người phụ trách việc phối hợp.
- [ ] Chọn CLI hoặc API; chốt schema, phiên bản và cách báo lỗi.
- [ ] Chốt mốc tích hợp, bộ mockup dùng chung và metric cộng hưởng.
- [ ] Ghi nhận nội dung đã thống nhất và các thay đổi trong repo khi triển khai.

## Nguồn

- [Kế hoạch thực tập 6 tuần](../../Kế%20hoạch%20thực%20tập%206%20tuần.pdf), phần Teamwork và Pair contract v0.
- [Kế hoạch MVP của Đức Anh](01-ke-hoach-mvp.md).
