# CIP Project Documentation

| Thông tin | Nội dung |
| --- | --- |
| Tên tiếng Việt | Xây dựng công cụ tự động kiểm tra tính đầy đủ của hồ sơ CIP và đề xuất bản nháp email phê duyệt tích hợp LLM và Rule-based |
| Tên tiếng Anh | Building an Automated CIP Completeness Checker and Email Draft Generator Powered by LLM and Rule-based Techniques |
| Người thực hiện | Nguyễn Đức Anh — Cặp C |
| Mentor | MinhLQ11 |
| Giai đoạn hiện tại | Gate 0 — lập kế hoạch và thống nhất tiêu chí |


## 1. Project Overview

Nội dung trang này là bản kế hoạch tóm tắt để biên tập thành đầu ra 1–2 trang của Gate 0. Các trang 2–7 cung cấp đặc tả hỗ trợ.

### 1.1 Problem & Motivation

CIP là quy trình cần thực hiện trước khi go-live. Trong phạm vi nghiệp vụ đã ghi nhận, MC document được lập theo template trên Confluence, gồm sáu mục: Ticket Jira, Service, Type, Risk, BO sign-off và Request. BO sign-off và Request chứa tệp email .msg.

Người dùng trực tiếp là người chuẩn bị hồ sơ CIP. Công việc cần hỗ trợ gồm rà soát các mục MC, kiểm tra bằng chứng và tổng hợp thông tin để viết email xin phê duyệt.

Các thao tác kiểm tra và tổng hợp thủ công có thể gây bỏ sót, thiếu nhất quán hoặc tốn thời gian. Hiện chưa có số liệu để kết luận tần suất lỗi hoặc mức thời gian có thể tiết kiệm.

Công cụ đề xuất kết hợp Rule-based để kiểm tra điều kiện xác định và LLM để hỗ trợ đọc nội dung, giải thích kết quả và tạo bản nháp email. Người dùng xem lại báo cáo, bổ sung thông tin và rà soát email trước khi gửi.

### 1.2 Related Works

| Nghiên cứu | Nội dung liên quan | Cách sử dụng trong dự án |
| --- | --- | --- |
| Vaswani và cộng sự (2017), Attention Is All You Need [1] | Kiến trúc Transformer dựa trên attention. | Cơ sở lý thuyết về mô hình ngôn ngữ. |
| Devlin và cộng sự (2019), BERT [2] | Biểu diễn ngôn ngữ hai chiều và tinh chỉnh cho tác vụ hiểu văn bản. | Tham khảo hướng hiểu/trích xuất văn bản; chưa chọn triển khai BERT riêng. |
| Brown và cộng sự (2020), Language Models are Few-Shot Learners [3] | Thực hiện tác vụ bằng hướng dẫn và một số ví dụ trong ngữ cảnh. | Cơ sở thiết kế prompt và ví dụ mẫu email. |
| Ji và cộng sự (2023), Survey of Hallucination in Natural Language Generation [4] | Tổng quan nội dung sinh thiếu căn cứ và các hướng đánh giá, giảm thiểu. | Cơ sở đánh giá độ trung thực của email với hồ sơ. |
| Lewis và cộng sự (2020), Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks [5] | Kết hợp truy xuất tài liệu với sinh ngôn ngữ. | Hướng tham khảo mở rộng; chưa đưa RAG vào phạm vi MVP. |

### 1.3 Contribution/Objectives

Mục tiêu tổng thể là xây dựng MVP tự động kiểm tra tính đầy đủ của hồ sơ CIP và hỗ trợ tạo email xin phê duyệt bằng cách kết hợp LLM với Rule-based.

Các mục tiêu và đóng góp dự kiến:

1. Chuẩn hóa sáu mục MC cùng bằng chứng thành dữ liệu có cấu trúc và vị trí nguồn.
2. Xây dựng checklist có phiên bản, phân định tiêu chí do luật xử lý và tiêu chí cần LLM hỗ trợ.
3. Trả kết quả từng tiêu chí gồm trạng thái, lý do, căn cứ và gợi ý bổ sung.
4. Tạo bản nháp email dựa trên dữ liệu đã có, đánh dấu thông tin còn thiếu.
5. Xây dựng bộ mockup có đáp án và quy trình đánh giá để đo chất lượng, thời gian xử lý.

### 1.4 Scope, Value & Success Metrics

| Nội dung | Đề xuất Gate 0 |
| --- | --- |
| Trong phạm vi | Một template MC mockup theo sáu mục; một phương thức nhận đầu vào; kiểm tra trường bắt buộc, định dạng và nội dung theo checklist; báo cáo có căn cứ; tạo email nháp. |
| Ngoài phạm vi | Tự phê duyệt, tự gửi email, ghi lên Confluence/Jira, xử lý dữ liệu thật, nhiều template và RAG. |
| Giá trị kỳ vọng | Giảm bỏ sót và thao tác tổng hợp, giúp người dùng nhìn rõ mục cần bổ sung và giảm thời gian chuẩn bị email. |
| Metric đề xuất | Precision và recall phát hiện thiếu; độ đúng căn cứ; tỷ lệ email đạt checklist; tỷ lệ email có thông tin thiếu căn cứ; thời gian hoàn thành tác vụ có/không có công cụ. |
| Kiến trúc sơ bộ | Mockup → trích xuất có nguồn → luật và LLM → tổng hợp → báo cáo và email → người dùng rà soát. |
| Mốc triển khai | Gate 1: skeleton; CP1: MVP mockup; CP2: kết quả Sprint 1; CP3: final demo, metric và bàn giao. |


### 1.5 References

1. Vaswani, A., et al. (2017). Attention Is All You Need. https://arxiv.org/abs/1706.03762
2. Devlin, J., et al. (2019). BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. https://aclanthology.org/N19-1423/
3. Brown, T. B., et al. (2020). Language Models are Few-Shot Learners. https://arxiv.org/abs/2005.14165
4. Ji, Z., et al. (2023). Survey of Hallucination in Natural Language Generation. https://doi.org/10.1145/3571730 — bản arXiv tương ứng: https://arxiv.org/abs/2202.03629 (có cập nhật sau xuất bản).
5. Lewis, P., et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. https://arxiv.org/abs/2005.11401

## 2. Business Requirements

### 2.1 Business Context & Stakeholders

| Nội dung | Trạng thái hiểu biết |
| --- | --- |
| MC sử dụng template trên Confluence | Đã ghi nhận trong tài liệu dự án. |
| MC có sáu mục nêu tại trang 1 | Đã thực hiện xác nhận trước đó. |
| T4 thực hiện UAT; T3 viết CR gửi T2 | Bối cảnh đã ghi nhận; chưa đủ để suy ra toàn bộ trình tự CIP. |
| Người dùng trực tiếp | Dự kiến là người chuẩn bị hồ sơ; chờ mentor xác nhận chức danh và trách nhiệm. |
| Điều kiện phê duyệt và vai trò BO sign-off | Chưa được xác nhận đầy đủ. |

### 2.2 Business Needs

| ID | Nhu cầu | Kết quả mong đợi |
| --- | --- | --- |
| BR-01 | Biết hồ sơ còn thiếu gì trước khi gửi xin duyệt | Danh sách mục thiếu theo checklist đã thống nhất. |
| BR-02 | Hiểu căn cứ của nhận xét | Có trích đoạn/vị trí nguồn hoặc giải thích thiếu bằng chứng. |
| BR-03 | Giảm công việc tổng hợp email | Có bản nháp đúng dữ liệu, có thể rà soát và chỉnh sửa. |
| BR-04 | Giữ quyền quyết định ở người dùng | Kết quả là hỗ trợ rà soát và bản nháp; có bước kiểm tra của người dùng. |
| BR-05 | Chứng minh giá trị MVP | Đánh giá trên bộ dữ liệu được phép, có đáp án và số đo. |

Luồng nghiệp vụ đề xuất: chuẩn bị MC và bằng chứng → chạy kiểm tra → xem căn cứ → bổ sung thông tin → tạo/rà soát bản nháp email.

### 2.3 Open Questions

- Ai là người trực tiếp sử dụng và ai rà soát đầu ra?
- Mục nào bắt buộc? Khi nào BO sign-off và Request được coi là hợp lệ?
- CR, UAT và MC liên kết bằng thông tin nào?
- Mẫu email, người nhận/CC và các thông tin bắt buộc nên có là gì?
- Checklist và đáp án mockup sẽ được ai xác nhận?

## 3. Functional Requirements

| ID | Chức năng | Tiêu chí chấp nhận đề xuất | Liên hệ |
| --- | --- | --- | --- |
| FR-01 | Nhận gói MC mockup và tệp bằng chứng | Nhận diện đầu vào hợp lệ, thông báo rõ tệp/định dạng lỗi. | BR-01 |
| FR-02 | Trích xuất sáu mục MC | Lưu giá trị, trạng thái hiện diện, nguồn và lỗi đọc. | BR-01, BR-02 |
| FR-03 | Kiểm tra bằng luật | Mỗi luật có mã và phiên bản; xác định mục thiếu/trống hoặc sai định dạng theo checklist. | BR-01 |
| FR-04 | LLM kiểm tra nội dung | Nhận xét đúng cấu trúc, có căn cứ hoặc needs_review khi chưa đủ thông tin. | BR-01, BR-02 |
| FR-05 | Tổng hợp báo cáo | Hiển thị pass/fail/needs_review, lý do và gợi ý từng tiêu chí; giữ lỗi xử lý. | BR-01, BR-02 |
| FR-06 | Tạo email nháp | Bám thông tin hồ sơ và kết quả; chỉ rõ phần thiếu; không tự điền phê duyệt/người nhận. | BR-03, BR-04 |
| FR-07 | Rà soát đầu ra | Người dùng xem được báo cáo, nguồn và sao chép bản nháp. | BR-04 |
| FR-08 | Đánh giá và xuất kết quả | Có đầu ra theo case, phiên bản cấu hình và thời gian để đối chiếu đáp án. | BR-05 |

Yêu cầu chất lượng đề xuất: cấu hình checklist/prompt/mẫu email được quản lý phiên bản; lỗi đọc và lỗi LLM được phân biệt với kết luận nghiệp vụ; có hướng dẫn chạy độc lập. Ngưỡng hiệu năng sẽ được đặt sau baseline Gate 1.

## 4. System Architecture

### 4.1 Proposed Components

| Thành phần | Trách nhiệm |
| --- | --- |
| Input Adapter & Parser | Đọc HTML mô phỏng Confluence và email .msg; giữ vị trí nguồn, trạng thái đọc. |
| Structured MC | Dữ liệu trung gian thống nhất cho luật và LLM. |
| Rule Engine | Kiểm tra điều kiện xác định theo checklist mockup có phiên bản. |
| LLM Checker | Hỗ trợ đánh giá nội dung theo tiêu chí được giao. |
| Result Aggregator | Tổng hợp kết quả và căn cứ; thể hiện bất đồng hoặc thiếu bằng chứng. |
| Email Generator | Tạo email nháp từ dữ liệu và kết quả, theo mẫu. |
| Review Interface | Cho người dùng xem báo cáo và email. |
| Evaluation Runner | So sánh kết quả với đáp án, xuất metric và thời gian. |

Luồng: Input Adapter → Structured MC → Rule Engine/LLM Checker → Result Aggregator → Email Generator → Review Interface. Evaluation Runner đọc đầu ra và đáp án để đánh giá.

### 4.2 Design Decisions to Validate

- HTML và .msg là phương án đầu vào đề xuất; cần kiểm chứng tạo/đọc .msg đúng định dạng.
- Không đọc được nguồn phải được báo lỗi hoặc needs_review; không mặc định là pass.
- Luật, prompt và mẫu email được tách khỏi mã xử lý để dễ thay đổi và truy vết.
- Model, thư viện parser, công nghệ giao diện và phương thức tích hợp CLI/API chưa được chốt.
- Việc soạn tài liệu dự án trên Confluence độc lập với việc tích hợp công cụ vào Confluence thật; MVP hiện chỉ cần xử lý mockup tự dựng.

Giả định rủi ro nhất dự kiến kiểm chứng ở Gate 1: trích xuất MC đủ chính xác để kiểm tra checklist và dẫn căn cứ đúng vị trí.

## 5. Data Structure

### 5.1 MC Schema — Proposed

| Trường | Kiểu | Ý nghĩa |
| --- | --- | --- |
| case_id | string | Mã hồ sơ mockup. |
| ticket_jira | string/null | URL Jira giả lập. |
| service | string/null | Tên dịch vụ giả lập. |
| type | string/null | Loại thay đổi theo danh mục mockup tự định nghĩa. |
| risk | string/null | Nội dung rủi ro giả lập. |
| bo_sign_off | object/null | Tham chiếu .msg, dữ liệu đọc được, trạng thái đọc và nguồn. |
| request | object/null | Tham chiếu .msg, dữ liệu đọc được, trạng thái đọc và nguồn. |
| sources | array | Ánh xạ trường tới tệp, vị trí và trích đoạn nguồn. |
| extraction_errors | array | Danh sách lỗi đọc/chuẩn hóa. |

Thiếu mục, có mục nhưng trống, có tệp nhưng không đọc được là các trạng thái khác nhau. Schema triển khai cần giữ được sự phân biệt này.

### 5.2 Check Result & Email Draft

| Đối tượng | Trường đề xuất |
| --- | --- |
| Kết quả kiểm tra | criterion_id, status (pass/fail/needs_review), reason, evidence, suggestion, checker, checklist_version. |
| Căn cứ | source_file, location, excerpt; trường thiếu dùng tham chiếu vùng/mục đã kiểm tra khi phù hợp. |
| Email nháp | subject, body, missing_information, source_case_id. |
| Thông tin lần chạy | run_id, app_version, checklist_version, prompt_version, model, processing_time, processing_errors. |

### 5.3 Mockup Dataset Specification — Proposed

Đề xuất bộ khởi đầu gồm 24 gói hồ sơ: 12 gói phát triển/kiểm chứng sớm và 12 gói đánh giá giữ riêng. Mỗi tập có hai gói thuộc mỗi nhóm dưới đây. Số lượng này là kế hoạch, chưa phải dữ liệu đã tạo.

| Nhóm | Nội dung tình huống |
| --- | --- |
| Đầy đủ | Sáu mục có thông tin theo quy ước mockup và bằng chứng đọc được. |
| Thiếu mục/trường trống | Bỏ mục, để trống hoặc chỉ có khoảng trắng; xác định rõ mục nào bị ảnh hưởng. |
| Thiếu bằng chứng | MC có tham chiếu nhưng không có tệp .msg tương ứng. |
| Sai định dạng/lỗi đọc | URL không hợp lệ, tệp hỏng hoặc không đúng định dạng .msg. |
| Không nhất quán | Thông tin service/ticket khác nhau giữa MC và email, theo quy tắc đối chiếu đề xuất. |
| Biến thể bố cục | Thay đổi thứ tự mục/bảng trong phạm vi template mockup được hỗ trợ. |

Mỗi gói gồm manifest, MC HTML, tệp .msg liên quan khi có và đáp án. Manifest chỉ định case_id, nhóm tình huống và các tệp. Đáp án ghi giá trị, trạng thái từng mục, kết quả từng tiêu chí, căn cứ và các thông tin email được phép sử dụng. Nhóm thiếu tệp hoặc lỗi định dạng được đánh dấu rõ là tình huống lỗi chủ đích.

Các giá trị, người gửi, người nhận và liên kết đều tự dựng; dùng miền ví dụ như example.test. Các tệp .msg bình thường phải đúng định dạng, không đổi đuôi tệp văn bản. Người tạo gắn nhãn ban đầu; đề xuất mentor rà soát checklist và tính hợp lý của đáp án. Tập đánh giá không dùng làm ví dụ trong prompt; nếu đã dùng để chỉnh hệ thống, cần ghi nhận và thay tập đánh giá trước khi báo cáo kết quả độc lập.

Theo kế hoạch thực tập: đến CP1 chỉ dùng mockup; từ 19/11 chỉ dùng masked khi được mentor cung cấp và cho phép. Repo chỉ chứa mockup; masked lưu nơi mentor chỉ định và không commit. Không dùng dữ liệu thật.

## 6. Development Plan

### 6.1 Milestones

| Mốc | Ngày | Đầu ra |
| --- | --- | --- |
| Gate 0 | 04/11 | Kế hoạch 1–2 trang; rubric cụ thể; pair contract v0; đặc tả mockup; rủi ro/phụ thuộc. |
| Gate 1 | 11/11 | Skeleton end-to-end; kiểm chứng giả định rủi ro nhất; kế hoạch điều chỉnh; baseline; backlog Sprint 1. |
| CP1 | 18/11 | Demo MVP trên mockup và tiến độ so với kế hoạch. |
| CP2 | 25/11 | Demo MVP, kết quả Sprint 1 và retro; dùng masked trong phạm vi được phép nếu được cấp. |
| CP3 | 09/12 | Final demo, metric thực đo và tài liệu bàn giao. |

### 6.2 Gate 0 Completion Plan

Việc cần hoàn thiện | Thời gian dự kiến | Trạng thái |
| --- | --- | --- |
| Biên tập trang Project Overview thành kế hoạch 1–2 trang | 03/11/2026 – 04/11/2026 | Đã hoàn thành, chờ mentor đánh giá. |
| Chốt yêu cầu nghiệp vụ, metric và rubric | 03/11/2026 – 04/11/2026 | Đề xuất trong tài liệu, chờ xác nhận. |
| Chốt đặc tả mockup và cách gắn nhãn | 03/11/2026 | Có bản đề xuất, chưa tạo bộ dữ liệu. |
| Thống nhất pair contract v0 | 03/11/2026 | Chưa  thống nhất lại với Vĩnh. |
| Rà soát rủi ro/phụ thuộc, cập nhật link vào sheet | 04/11/2026, trước buổi Gate 0 | Chờ hoàn thiện trang Confluence và rà soát.

### 6.3 Pair Contract v0 — Proposed

| Câu hỏi bắt buộc | Đề xuất |
| --- | --- |
| Hai bài toán giao nhau ở đâu, giá trị cộng hưởng là gì? | Framework SDLC AI của Vĩnh điều phối chạy bộ đánh giá công cụ CIP, tổng hợp sai lệch và hỗ trợ phát hiện suy giảm sau thay đổi. |
| Mỗi người phụ trách gì, ranh giới ở đâu? | Đức Anh sở hữu công cụ CIP, checklist, mockup, đáp án và sửa lỗi phía CIP. Đề xuất Vĩnh phụ trách điều phối và tổng hợp phía framework; chờ Vĩnh xác nhận. |
| Trao đổi gì, định dạng nào? | Mockup và đáp án JSON; yêu cầu chạy qua CLI hoặc API; kết quả JSON gồm case_id, phiên bản, kết quả từng tiêu chí, lỗi và thời gian. Phương thức/schema cần thống nhất. |
| Khi nào tích hợp, đo cộng hưởng bằng gì? | Gate 1 có mẫu trao đổi và chạy độc lập; CP1 thử điều phối; CP2 demo tích hợp; CP3 đo thời gian/số thao tác chạy đánh giá và lỗi suy giảm phát hiện được. |

Công cụ CIP cần chạy độc lập để tiến độ không phụ thuộc hoàn toàn vào framework. Pair contract chi tiết hiện có tại docs/gate-0/03-pair-contract-v0.md; khi tạo trang Confluence cần liên kết tới trang contract tương ứng. 

### 6.4 Risks & Dependencies

| ID | Rủi ro | Ảnh hưởng | Cách xử lý |
| --- | --- | --- | --- |
| R-01 | Checklist chưa đầy đủ hoặc điều kiện hợp lệ chưa rõ | Có thể kết luận sai hồ sơ đủ/thiếu. | Rà soát từng tiêu chí với mentor; ghi rõ điều kiện đạt/chưa đạt và quản lý phiên bản checklist. |
| R-02 | Trích xuất sai hoặc bỏ sót dữ liệu HTML/.msg | Thông tin đầu vào và căn cứ kiểm tra bị sai lệch. | Đối chiếu dữ liệu trích xuất với đáp án; giữ vị trí nguồn; báo lỗi hoặc needs_review khi không đọc được. |
| R-03 | LLM tự thêm thông tin hoặc trả kết quả sai cấu trúc | Báo cáo và email có thể chứa nội dung không có căn cứ hoặc không xử lý được. | Kiểm tra schema và đối chiếu nguồn; đánh dấu thông tin thiếu; đánh giá lỗi trên bộ mockup. |
| R-05 | Mockup thiếu tình huống hoặc đáp án gắn nhãn sai | Metric không phản ánh đúng chất lượng hệ thống. | Phủ các nhóm lỗi, rà soát đáp án và tách tập phát triển khỏi tập đánh giá. |
| R-07 | Phép đo thời gian thiếu cơ sở so sánh | Không xác định được mức tiết kiệm thời gian của công cụ. | Đo thủ công và có công cụ trên cùng tập hồ sơ, cùng người thực hiện; tính cả thời gian rà soát và sửa email. |
| R-08 | Chưa tìm được cách xác định cấp bậc nhân viên | Chưa đủ căn cứ để kiểm tra cấp bậc của người tham gia và xác định vai trò phù hợp trong hồ sơ, email xin phê duyệt. | Trao đổi với mentor để thống nhất nguồn và cách xác định cấp bậc; dùng bảng ánh xạ nhân viên–cấp bậc giả lập cho MVP; đánh dấu cần xác nhận khi thiếu thông tin, không tự suy đoán. |

## 7. Testing Documentation

Ở Gate 0, trang này đặc tả cách kiểm tra, metric và rubric; chưa báo cáo test đã chạy. Baseline thực đo thuộc Gate 1.

### 7.1 Test Strategy

| Phạm vi | Cách kiểm tra dự kiến | Ví dụ |
| --- | --- | --- |
| Parser | So sánh dữ liệu và nguồn với đáp án | Đảo thứ tự mục, có mục trống, .msg lỗi. |
| Rule Engine | Đối chiếu kết quả từng criterion_id | Phát hiện thiếu Ticket Jira; phân biệt thiếu tệp với lỗi đọc. |
| LLM Checker | Chấm đầu ra theo schema và căn cứ | Nhận xét không có nguồn phải được đánh dấu. |
| Email Generator | Rà soát bằng checklist email | Không thêm người nhận/phê duyệt; phản ánh đúng mục thiếu. |
| End-to-end | Chạy từ gói mockup đến báo cáo/email | Hồ sơ đủ, thiếu và lỗi xử lý. |
| Regression | Chạy lại sau đổi luật, parser hoặc prompt | So sánh kết quả và metric giữa các phiên bản. |

### 7.2 Metric Definitions & Targets — Proposed

| Metric | Cách tính | Ngưỡng mục tiêu đề xuất |
| --- | --- | --- |
| Precision phát hiện thiếu | TP / (TP + FP) | ≥ 90% |
| Recall phát hiện thiếu | TP / (TP + FN) | ≥ 90% |
| Độ đúng căn cứ | Số căn cứ đúng / tổng căn cứ được trả ra | ≥ 95% |
| Email đạt checklist | Số email đạt mọi tiêu chí / tổng email sinh thành công | ≥ 90% |
| Email có thông tin thiếu căn cứ | Số email có ít nhất một khẳng định thiếu căn cứ / tổng email sinh thành công | Mục tiêu 0 email quan sát được trên bộ đánh giá; không khẳng định bảo đảm ngoài bộ này. |
| Giảm thời gian hoàn thành | (Trung vị thời gian thủ công − trung vị thời gian có công cụ) / trung vị thời gian thủ công | ≥ 20%, gồm cả thời gian người dùng rà soát và sửa email. |

Đơn vị TP/FP/FN là cặp (case_id, criterion_id): TP là mục thiếu được phát hiện đúng; FP là mục không thiếu bị cảnh báo thiếu; FN là mục thiếu bị bỏ sót. Mẫu số bằng 0 ghi N/A và số đếm, không quy đổi thành 100%. Lỗi đọc và lỗi sinh email được thống kê riêng, cùng tổng case đủ điều kiện và tổng case xử lý thành công.

Checklist email đề xuất gồm: đúng thông tin hồ sơ; đúng trạng thái kiểm tra; thể hiện các mục cần bổ sung; không tự thêm người nhận hoặc phê duyệt; không tự bịa dữ liệu; nội dung yêu cầu rõ ràng. Nhãn email cần được người rà soát ghi lại cùng lý do không đạt.

Phép đo thời gian dùng cùng bộ hồ sơ và người thực hiện, cân bằng thứ tự làm thủ công/có công cụ để giảm ảnh hưởng ghi nhớ; ghi số mẫu và điều kiện đo. Các ngưỡng trên phục vụ thảo luận Gate 0, chưa được mentor phê duyệt và chưa có số đo đạt ngưỡng.

### 7.3 Rubric Levels 2–3–4 — Proposed

Rubric áp dụng cho đánh giá checkpoint; Gate 0/Gate 1 vẫn là đạt/chưa đạt. Đề xuất cụ thể hóa như sau, chờ mentor duyệt.

| Tiêu chí | 2 — Đạt | 3 — Tốt | 4 — Xuất sắc |
| --- | --- | --- | --- |
| Giá trị và kết quả | Chạy đủ luồng kiểm tra và email; precision/recall ≥ 80%, email đạt checklist ≥ 80% trên tập được phép; không che giấu lỗi xử lý. | Đạt toàn bộ ngưỡng mục 7.2 trên dữ liệu masked được cấp/phép dùng; có ít nhất 1 stakeholder dùng thử và phản hồi ghi nhận. | Precision/recall ≥ 95%, email đạt checklist ≥ 95%, căn cứ ≥ 98%, giảm thời gian ≥ 30%, không quan sát email thiếu căn cứ; stakeholder xác nhận muốn đưa MVP đi tiếp. |
| Chất lượng kỹ thuật | Có hướng dẫn chạy, schema và cấu hình phiên bản; cả 6 nhóm mockup có đầu ra đối chiếu đáp án; mã nguồn đọc hiểu được. | Bộ đánh giá chạy lặp lại bằng một lệnh; có kiểm tra schema/lỗi, kết quả từng case, cấu hình LLM; đánh giá có hệ thống cả phần AI; tuân thủ dữ liệu. | Ít nhất 1 người khác chạy lại theo tài liệu và thêm 1 rule hoặc case mới mà không cần hướng dẫn trực tiếp; có minh chứng bàn giao và kết quả regression. |
| Thực thi và chủ động | Hoàn thành ≥ 80% đầu việc đến hạn đã chốt, có bằng chứng. | Hoàn thành ≥ 90%; báo rủi ro ngay khi ghi nhận và trước hạn bị ảnh hưởng; ghi hướng xử lý góp ý trong 2 ngày làm việc. | Đạt mức 3; có ít nhất 1 điều chỉnh kế hoạch dựa trên số liệu và 1 đóng góp giúp đồng đội được xác nhận. |

Các điều kiện áp dụng theo giai đoạn: CP1 chỉ dùng mockup; CP2/CP3 áp dụng masked khi được cấp và được phép dùng. Nếu không có masked, trình mentor thống nhất phương án đánh giá thay thế trước checkpoint, không tự tuyên bố đạt điều kiện masked. Công việc thay đổi phạm vi phải được ghi nhận trước hạn và thống nhất khi tính tỷ lệ hoàn thành.

### 7.4 Gate 0 Deliverable Mapping

| Yêu cầu Gate 0 | Vị trí trong bộ tài liệu |
| --- | --- |
| Kế hoạch 1–2 trang | 1. Project Overview; kiến trúc tóm tắt tại 1.4 |
| Rubric cụ thể | 7.2–7.3 |
| Pair contract v0 | 6.3 và bản contract chi tiết |
| Đặc tả mockup | 5.1–5.3 |
| Rủi ro và phụ thuộc | 6.4 |
