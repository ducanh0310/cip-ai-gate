# CIP Mockup Dataset v1

Toàn bộ nội dung ở đây là dữ liệu giả lập để phát triển và đánh giá công cụ CIP. Không có yêu cầu triển khai thật, nhân viên thật hoặc phê duyệt thật. Email chỉ được dựng thành tệp, không được gửi.

## Nguồn trên Jira và Confluence

- [Danh mục Confluence](https://nguyenducanhflm.atlassian.net/wiki/spaces/KAN/pages/1081458).
- [Development — 12 MC](https://nguyenducanhflm.atlassian.net/wiki/spaces/KAN/pages/1277968).
- [Evaluation — 12 MC](https://nguyenducanhflm.atlassian.net/wiki/spaces/KAN/pages/1179756).
- [Evaluation Guide & Ground Truth](https://nguyenducanhflm.atlassian.net/wiki/spaces/KAN/pages/1114221).
- Jira: project KAN; 24 ticket từ KAN-4 đến KAN-27; tìm bằng JQL `project = KAN AND labels = cip-mock-v1 ORDER BY key ASC`.

## Thành phần bộ dữ liệu

| Thành phần | Số lượng |
| --- | --- |
| Hồ sơ phát triển | 12 |
| Hồ sơ đánh giá | 12 |
| Nhóm tình huống | 6; mỗi nhóm có 2 hồ sơ trong mỗi tập |
| Email .msg hợp lệ, đã đọc kiểm chứng | 42 |
| Email .msg cắt cụt có chủ đích | 2 |
| Tệp bằng chứng cố ý để thiếu | 4 |
| Trang MC | 24 |
| Ticket Jira giả lập | 24 |

Sáu nhóm: đầy đủ, thiếu mục/trường trống, thiếu bằng chứng, sai định dạng/lỗi đọc, thông tin không nhất quán và biến thể bố cục. Mục Risk và danh mục Type là quy ước tự dựng; checklist v1 chưa được mentor phê duyệt.

## Cấu trúc thư mục

```text
v1/
  dev/CIP-D01...CIP-D12/    # Đầu vào tập phát triển
  eval/CIP-E01...CIP-E12/   # Đầu vào tập đánh giá
  ground_truth/            # Đáp án từng case, tách khỏi đầu vào
  checklist.json          # 11 tiêu chí và quy tắc tổng hợp
  manifest.json           # Danh mục tổng: mapping tài nguyên, nhóm và nhãn
  remote-resources.json   # ID/link và nội dung dùng để dựng tài nguyên
  attachment-resources.json
  validation-report.json
  remote-validation-report.json
  build_dataset.py
```

Mỗi gói đầu vào chứa `mc.html`, `manifest.json` và những tệp .msg thực sự tồn tại. MC có thể tham chiếu một tên tệp không có trong gói: đó là tình huống thiếu bằng chứng, không tự tạo tệp thay thế. Tệp hỏng có chữ ký CFB nhưng bị cắt cụt có chủ đích; không phải văn bản đổi đuôi .msg.

## Cách sử dụng và tránh lộ đáp án

1. Dùng `dev/` để phát triển parser, luật và prompt.
2. Khi chạy kiểm tra, chỉ truyền `mc.html` và các tệp email của chính gói đó; trên Confluence, chỉ đọc trang MC và attachments tương ứng.
3. Không đưa README này, manifest tổng, checklist có chú giải đáp án, `ground_truth/`, danh mục tình huống hoặc trang Evaluation Guide vào prompt kiểm tra hồ sơ. Checklist quy tắc có thể được cấu hình riêng cho checker; đáp án từng case không được đưa vào checker.
4. Giữ `eval/` để đánh giá sau khi chốt luật/prompt. Nếu đã dùng nó để chỉnh hệ thống, ghi nhận việc này và tạo tập đánh giá mới trước khi công bố kết quả độc lập.
5. Không đọc đệ quy toàn bộ nhánh Confluence để làm đầu vào cho một case, vì nhánh này có cả trang dành cho người đánh giá.

## Đáp án kỳ vọng

Phân bố theo checklist mockup: 8 `pass`, 14 `fail`, 2 `needs_review`. Đây là nhãn kỳ vọng do thiết kế dữ liệu, chưa phải kết quả chạy công cụ CIP.

Tổng hợp: bất kỳ tiêu chí nào `fail` thì toàn hồ sơ `fail`; nếu không có `fail` nhưng có `needs_review` thì toàn hồ sơ `needs_review`; còn lại là `pass`. Nguồn thiếu/hỏng/không hợp lệ khiến các kiểm tra phụ thuộc là `needs_review`, không mặc định đạt.

Checklist chỉ kiểm tra 11 tiêu chí về sáu mục MC, định dạng, khả năng đọc và nhất quán service/ticket. Kết quả đạt không xác minh thẩm quyền phê duyệt. Chưa có nguồn tra cứu cấp bậc nhân viên; tên/email giả lập không đủ để suy ra cấp bậc. Không tự thêm cấp bậc, người nhận hoặc phê duyệt vào email nháp.

## Kiểm chứng đã thực hiện

- Dùng extract-msg 0.58.1 đọc lại 42 .msg hợp lệ và đối chiếu subject, sender, recipient, body với dữ liệu dựng.
- Xác nhận 2 .msg lỗi không đọc được và 4 bằng chứng thiếu đúng thiết kế.
- Kiểm tra lại 24 trang MC: đủ tên/kích thước của 44 attachments đã tải, các liên kết tệp tồn tại trong nội dung.
- Tìm lại trên Jira thấy đủ 24 ticket có label `cip-mock-v1`; từng ticket đã có Web link tới MC.
- Chưa kiểm chứng bằng Outlook; chưa có kết quả chạy checker hoặc metric chất lượng ứng dụng.

## Dựng lại dữ liệu cục bộ

Yêu cầu Python và `extract-msg==0.58.1`. Chạy `python build_dataset.py` từ môi trường đã cài thư viện. Script đọc `remote-resources.json`, dựng gói đầu vào và ground truth cục bộ; không tạo lại ticket/trang Confluence và không gửi email. Không chạy lại script trong lúc đang sửa fixture thủ công vì nó ghi lại các file dữ liệu do script sinh.

Các tài nguyên online đã có sẵn; dùng mapping trong manifest để tránh tạo trùng khi tích hợp. Tệp token hoặc lệnh upload có thông tin xác thực không được lưu vào repo.
