# Gate 1 — CIP Completeness Checker & Email Draft Generator

| Thông tin | Nội dung |
| --- | --- |
| Tên dự án tiếng Việt | Xây dựng công cụ tự động kiểm tra tính đầy đủ của hồ sơ CIP và đề xuất bản nháp email phê duyệt tích hợp LLM và Rule-based |
| Tên dự án tiếng Anh | Building an Automated CIP Completeness Checker and Email Draft Generator Powered by LLM and Rule-based Techniques |
| Người thực hiện | Nguyễn Đức Anh — Cặp C |
| Mentor | MinhLQ11 |
| Ngày Gate 1 | 11/11/2026 |
| Phiên bản | v0.1 — 03/11/2026 |
| Trạng thái | Bản nháp chuẩn bị Gate 1; chưa có bằng chứng skeleton chạy hoặc baseline thực đo |

Tài liệu trình bày bài toán, thiết kế và kế hoạch kiểm chứng cho Gate 1. Các lựa chọn kỹ thuật và tiêu chí dưới đây là đề xuất; kết quả thực nghiệm chỉ được điền khi có bằng chứng chạy thực tế. Trong tài liệu này, “email phê duyệt” được hiểu là bản nháp email xin phê duyệt CIP để người dùng rà soát.

## 1. Introduction

### 1.1 Problem & Motivation

CIP là quy trình cần thực hiện trước khi go-live. Trong phạm vi bài toán đã ghi nhận, MC document được lập theo template trên Confluence và gồm sáu mục: Ticket Jira, Service, Type, Risk, BO sign-off và Request. Hai mục BO sign-off và Request chứa tệp email định dạng .msg. Người dùng trực tiếp dự kiến là người chuẩn bị hồ sơ CIP; vai trò cụ thể cần được mentor xác nhận.

Việc kiểm tra thủ công đòi hỏi người chuẩn bị hồ sơ đối chiếu các mục trong MC, đọc bằng chứng liên quan và tổng hợp thông tin để viết email xin phê duyệt. Những thao tác này có khả năng gây bỏ sót thông tin hoặc đưa nội dung chưa nhất quán vào email. Đây là giả thuyết về vấn đề cần kiểm chứng; dự án chưa có số liệu về thời gian xử lý hoặc tỷ lệ sai sót hiện tại.

Dự án đề xuất kết hợp Rule-based và LLM. Bộ luật kiểm tra những điều kiện có thể xác định rõ, như mục bắt buộc, giá trị trống và định dạng. LLM hỗ trợ đọc nội dung theo checklist và tạo bản nháp email dựa trên dữ liệu đã trích xuất cùng kết quả kiểm tra. Mỗi nhận xét cần gắn với nguồn để người dùng kiểm tra lại.

Giá trị kỳ vọng là giảm thao tác kiểm tra, phát hiện mục còn thiếu và giảm thời gian soạn email. Mức cải thiện sẽ được đánh giá bằng thực nghiệm. Bộ mockup được tự dựng theo sáu mục đã xác nhận, không phụ thuộc truy cập Confluence hoặc Jira nội bộ.

### 1.2 Related Works

Các công trình sau cung cấp nền tảng cho thiết kế. Liên hệ với dự án CIP là hướng áp dụng đề xuất, không phải kết quả ứng dụng CIP đã được chứng minh trong các bài báo.

| Công trình | Nội dung liên quan | Vai trò trong dự án |
| --- | --- | --- |
| Vaswani và cộng sự, 2017 — Attention Is All You Need [1] | Giới thiệu kiến trúc Transformer sử dụng cơ chế attention. | Nền tảng lý thuyết để giải thích mô hình ngôn ngữ. |
| Devlin và cộng sự, 2019 — BERT [2] | Biểu diễn ngôn ngữ theo ngữ cảnh hai chiều và tinh chỉnh cho các tác vụ hiểu văn bản. | Tham khảo cho hướng phân loại hoặc trích xuất thông tin; chưa đề xuất triển khai BERT riêng trong skeleton. |
| Brown và cộng sự, 2020 — Language Models are Few-Shot Learners [3] | Khả năng thực hiện tác vụ bằng hướng dẫn và ví dụ trong ngữ cảnh. | Cơ sở thiết kế prompt kèm ví dụ email và quy ước đầu ra. |
| Ji và cộng sự, 2023 — Survey of Hallucination in Natural Language Generation [4] | Tổng quan hiện tượng sinh nội dung thiếu căn cứ, cách đo và giảm thiểu. | Cơ sở xây dựng tiêu chí đánh giá thông tin sai hoặc không có trong nguồn khi sinh email. |
| Lewis và cộng sự, 2020 — Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks [5] | Kết hợp truy xuất tài liệu với sinh ngôn ngữ. | Hướng mở rộng khi cần truy xuất quy trình hoặc hướng dẫn; chưa thuộc skeleton Gate 1. |

Trong tập tài liệu đang có, các nghiên cứu trên chưa trực tiếp giải quyết việc kiểm tra sáu mục MC của dự án và tạo email từ kết quả luật. Bài toán ứng dụng cần làm rõ là cách nối dữ liệu hồ sơ, checklist có phiên bản, kết quả kiểm tra và bản nháp email thành một luồng có thể kiểm chứng. Nhận định này chỉ áp dụng cho tập tài liệu đã chọn, chưa phải kết luận về toàn bộ nghiên cứu hiện có. Nguồn học thuật riêng cho phương pháp Rule-based cần được bổ sung và kiểm tra trước khi hoàn thiện báo cáo.

### 1.3 Contribution/Objectives

Mục tiêu tổng thể là xây dựng MVP kiểm tra tính đầy đủ của hồ sơ CIP và hỗ trợ người dùng soạn email xin phê duyệt bằng cách kết hợp Rule-based với LLM.

Các mục tiêu cụ thể và đóng góp dự kiến gồm:

1. Chuẩn hóa sáu mục MC thành dữ liệu có cấu trúc, kèm vị trí nguồn và trạng thái trích xuất.
2. Xây dựng checklist có phiên bản, phân công rõ tiêu chí do luật xử lý và tiêu chí cần LLM hỗ trợ.
3. Tổng hợp kết quả từng tiêu chí thành đạt, chưa đạt hoặc cần xem xét, kèm lý do và căn cứ.
4. Tạo bản nháp email từ thông tin hồ sơ và kết quả kiểm tra; đánh dấu nội dung thiếu để người dùng bổ sung.
5. Xây dựng bộ mockup có đáp án kỳ vọng và quy trình đo chất lượng trích xuất, kiểm tra, email và thời gian xử lý.

Đầu ra Gate 1 tập trung vào skeleton xuyên suốt, kiểm chứng giả định rủi ro nhất, kế hoạch đã điều chỉnh, baseline và backlog Sprint 1. Các mục tiêu trên chưa được xem là kết quả đã đạt.

## 2. Scope & Skeleton Design

### 2.1 Phạm vi

| Hạng mục | Phạm vi Gate 1 đề xuất |
| --- | --- |
| Đầu vào | Một gói hồ sơ gồm HTML mockup mô phỏng MC và hai tệp .msg giả lập theo manifest. |
| Trích xuất | Ticket Jira, Service, Type, Risk, BO sign-off, Request; nội dung email đọc được và vị trí nguồn. |
| Rule-based | Kiểm tra mục bắt buộc theo checklist mockup, dữ liệu trống, định dạng URL và khả năng đọc tệp. |
| LLM | Kiểm tra nội dung được chọn theo checklist; tạo bản nháp email từ dữ liệu và kết quả kiểm tra. |
| Đầu ra | Báo cáo theo tiêu chí, lỗi xử lý, bản nháp email và thời gian xử lý. |
| Cách chạy | Đề xuất CLI để có thể demo và đánh giá độc lập; giao diện người dùng được ưu tiên sau skeleton. |
| Ngoài phạm vi | Tự phê duyệt, gửi email, ghi lên hệ thống nội bộ, đọc hồ sơ thật, nhiều template và RAG. |

Tính bắt buộc của từng mục và điều kiện hợp lệ trong mockup là quy ước thử nghiệm, chờ mentor rà soát. Không mặc định sự hiện diện của mục BO sign-off đồng nghĩa đã có phê duyệt hợp lệ.

### 2.2 Luồng xử lý

Gói hồ sơ mockup → Đọc HTML/.msg → Chuẩn hóa dữ liệu và nguồn → Chạy luật và kiểm tra nội dung bằng LLM → Tổng hợp kết quả → Sinh bản nháp email → Người dùng rà soát.

| Thành phần | Trách nhiệm | Đầu ra |
| --- | --- | --- |
| Input/Parser | Đọc manifest, HTML và .msg; ghi lỗi đọc và vị trí nguồn. | MC có cấu trúc, evidence và extraction_errors. |
| Rule Engine | Thực hiện checklist xác định. | Kết quả luật theo criterion_id. |
| LLM Checker | Đọc nội dung theo tiêu chí được giao; trả đúng schema. | Nhận xét có evidence hoặc needs_review. |
| Aggregator | Tổng hợp kết quả; giữ lỗi đọc và bất đồng giữa các bộ kiểm tra. | Báo cáo thống nhất. |
| Email Generator | Tạo bản nháp theo mẫu và kết quả kiểm tra. | Tiêu đề và nội dung email. |
| Evaluator | So sánh đầu ra với đáp án và ghi thời gian. | Baseline theo case và metric tổng hợp. |

Kết quả mỗi tiêu chí gồm: criterion_id, status (pass/fail/needs_review), reason, evidence, suggestion, checker và checklist_version. Evidence cần chứa tệp nguồn, vị trí và trích đoạn khi có. Đây là schema đề xuất, chưa phải giao diện đã triển khai.

Không đọc được đầu vào phải tạo lỗi xử lý hoặc needs_review. Kết quả LLM sai schema phải được ghi nhận; không đổi thành pass. Bản nháp email không được tự điền người nhận, trạng thái phê duyệt hoặc thông tin thiếu bằng suy đoán. Nếu hồ sơ còn thiếu, email phải thể hiện điều đó và chưa được xem là sẵn sàng xin duyệt.

### 2.3 Tiêu chí demo skeleton

- Chạy một lệnh cho một gói mockup và tạo được báo cáo cùng bản nháp email.
- Demo tối thiểu ba tình huống: đầy đủ theo checklist mockup, thiếu mục và lỗi đọc tệp.
- Có ít nhất một bước LLM thực sự chạy để kiểm chứng đường tích hợp; nếu dùng stub phải ghi rõ phần chưa được kiểm chứng.
- Chỉ ra được nguồn của thông tin chính và cách hệ thống thể hiện mục thiếu.
- Ghi lại lệnh chạy, phiên bản, đầu ra và thời gian để người khác có thể đối chiếu.

## 3. Riskiest Assumption & Validation

Giả định rủi ro nhất được chọn từ kế hoạch Gate 0: có thể trích xuất MC và email .msg đủ chính xác để kiểm tra theo checklist và dẫn căn cứ đúng vị trí. Nếu dữ liệu hoặc nguồn bị trích xuất sai, kết quả luật và email phía sau đều có thể sai.

| Nội dung | Thiết kế kiểm chứng đề xuất |
| --- | --- |
| Bộ dữ liệu | 12 gói mockup: 3 đầy đủ, 3 thiếu mục hoặc tệp, 3 thay đổi bố cục HTML/thông tin đối chiếu, 3 lỗi định dạng hoặc tệp không đọc được. |
| Đáp án | Nhãn hiện diện, giá trị kỳ vọng, trạng thái đọc và vị trí nguồn của sáu mục; quy ước xử lý trường rỗng và tệp lỗi. |
| Cách chạy | Cố định phiên bản parser và checklist; chạy toàn bộ bộ kiểm chứng; đối chiếu đầu ra với đáp án. |
| Tiêu chí thử nghiệm | Tỷ lệ mục trích xuất đúng ≥ 95%; căn cứ đúng ≥ 95%; cả ba ca lỗi đọc phải được báo lỗi/needs_review, không âm thầm cho đạt. |
| Nếu chưa đạt | Phân loại lỗi HTML/.msg/ánh xạ nguồn; thu hẹp bố cục được hỗ trợ hoặc sửa parser rồi chạy lại và lưu cả hai lần đo. |
| Bằng chứng cần lưu | Dataset manifest, đáp án, lệnh chạy, phiên bản, kết quả từng case và phân tích sai lệch. |
| Kết quả hiện tại | Chưa thực hiện; ngưỡng trên là đề xuất, chưa được mentor duyệt. |

Tệp .msg dùng trong thử nghiệm phải đúng định dạng và được kiểm tra bằng trình đọc phù hợp. Không dùng tệp văn bản đổi đuôi làm bằng chứng đã hỗ trợ .msg. Quy tắc chấm trích xuất đúng phải được chốt trước khi chạy; một mục chỉ đúng khi cả trạng thái hiện diện, giá trị và liên kết bằng chứng phù hợp đáp án. Một mục bắt buộc không có trong hồ sơ vẫn được xem là trích xuất đúng nếu hệ thống nhận diện chính xác là thiếu.

## 4. Baseline Metrics

Baseline là số đo lần chạy đầu tiên, chưa phải mục tiêu chất lượng đã đạt. Bộ 12 gói ở mục 3 phục vụ kiểm chứng sớm; cần bộ đánh giá riêng trước khi kết luận về chất lượng tổng quát.

| Metric | Cách đo | Baseline hiện tại |
| --- | --- | --- |
| Độ đúng trích xuất | Số mục trích xuất đúng / tổng mục được gắn nhãn. | Chưa đo |
| Precision phát hiện thiếu | TP / (TP + FP): tỷ lệ cảnh báo thiếu đúng trong các cảnh báo thiếu. | Chưa đo |
| Recall phát hiện thiếu | TP / (TP + FN): tỷ lệ mục thiếu được phát hiện trong các mục thiếu theo đáp án. | Chưa đo |
| Độ đúng của căn cứ | Số liên kết căn cứ đúng / tổng liên kết căn cứ được trả ra. | Chưa đo |
| Tỷ lệ email có thông tin thiếu căn cứ | Số email chứa ít nhất một khẳng định không được đầu vào hoặc kết quả kiểm tra hỗ trợ / tổng email sinh thành công. | Chưa đo |
| Tỷ lệ email đáp ứng checklist | Số email đạt toàn bộ tiêu chí nội dung / tổng email sinh thành công. | Chưa đo |
| Tỷ lệ hoàn thành luồng | Số gói hợp lệ tạo đủ báo cáo và email / tổng gói đầu vào hợp lệ. | Chưa đo |
| Thời gian xử lý | Trung vị và lớn nhất của thời gian mỗi gói; ghi riêng thời gian gọi LLM. | Chưa đo |

TP là mục thiếu được cảnh báo đúng; FP là mục không thiếu nhưng bị cảnh báo thiếu; FN là mục thiếu bị bỏ sót. Đơn vị đếm là cặp (case_id, criterion_id). Lỗi đọc thuộc nhóm lỗi xử lý, được báo cáo riêng để tránh gộp với lỗi thiếu dữ liệu.

Checklist email đề xuất: thông tin hồ sơ chính xác, thể hiện đúng trạng thái kiểm tra, liệt kê mục thiếu khi có, không tự thêm người nhận hoặc phê duyệt, có nội dung đề nghị phù hợp và giữ thông tin chưa biết dưới dạng cần bổ sung. Người rà soát, phiên bản checklist và lý do không đạt phải được ghi lại.

Nếu mẫu số bằng 0, ghi N/A kèm số đếm; không quy đổi thành 100%. Ghi riêng số lần lỗi sinh email để tỷ lệ tính trên email thành công không che khuất lỗi toàn luồng. Với LLM, lưu model, prompt_version, tham số khả dụng, số lần chạy và đầu ra từng lần.

Để đo giá trị tiết kiệm thời gian ở giai đoạn sau, cần bổ sung baseline thủ công trên cùng tập hồ sơ, ghi rõ người thực hiện và điểm bắt đầu/kết thúc. Chưa có dữ liệu để công bố mức giảm thời gian.

## 5. Revised Plan & Dependencies

### 5.1 Kế hoạch chuẩn bị Gate 1

| Ngày | Công việc dự kiến | Bằng chứng/đầu ra |
| --- | --- | --- |
| 05/11 | Tổng hợp góp ý Gate 0; chốt checklist mockup, schema và metric. | Nhật ký thay đổi, checklist v0.1 và tiêu chí đánh giá. |
| 06/11 | Dựng HTML/.msg mockup và đáp án; kiểm chứng thư viện đọc .msg. | Bộ dữ liệu thử nghiệm và kết quả đọc tệp mẫu. |
| 07/11 | Dựng parser và Rule Engine tối thiểu. | MC có cấu trúc và kết quả luật trên case mẫu. |
| 09/11 | Tích hợp LLM, tổng hợp và tạo email; nối CLI. | Lần chạy xuyên suốt đầu tiên và đầu ra lưu được. |
| 10/11 | Chạy kiểm chứng giả định và baseline; phân tích lỗi. | Báo cáo thực đo, log và thay đổi kế hoạch. |
| 11/11 | Sửa lỗi chặn demo, hoàn thiện backlog và tài liệu; trình Gate 1. | Gói demo, link bằng chứng và nội dung trình bày. |

Lịch trên là đề xuất tại ngày 03/11, chưa phản ánh công việc đã hoàn thành. Lịch tuân theo ngày làm 07/11 trong kế hoạch thực tập.

### 5.2 Ghi nhận điều chỉnh sau Gate 0

| Góp ý/phát hiện | Điều chỉnh | Ảnh hưởng | Bằng chứng |
| --- | --- | --- | --- |
| Chưa có góp ý Gate 0 được ghi nhận trong tài liệu này. | Bổ sung sau buổi 04/11. | Chưa xác định. | Chưa có. |

### 5.3 Rủi ro và phụ thuộc

| Rủi ro/phụ thuộc | Ảnh hưởng | Cách xử lý đề xuất |
| --- | --- | --- |
| Checklist chưa được mentor thống nhất | Không có tiêu chuẩn đáng tin cậy để xác định hồ sơ đủ. | Gắn nhãn quy tắc mockup; trình mentor rà soát và quản lý phiên bản. |
| Khó tạo/đọc .msg hợp lệ | Chặn việc trích xuất bằng chứng. | Kiểm chứng ngày 06/11; ghi rõ giới hạn nếu phải dùng định dạng thay thế được thống nhất. |
| LLM thiếu căn cứ hoặc trả sai schema | Báo cáo/email có thể không đúng. | Kiểm tra schema, liên kết nguồn, đánh dấu needs_review và đo sai lệch. |
| Model/API chưa khả dụng | Chặn tích hợp LLM thực tế. | Xác nhận công cụ được phép và khả năng gọi sớm; ghi rõ stub không hoàn thành kiểm chứng LLM. |
| Bố cục HTML biến đổi | Parser bỏ sót hoặc gắn nhầm nguồn. | Kiểm thử biến thể mockup, công bố template hỗ trợ. |
| Chưa thống nhất giao diện với Vĩnh | Chậm tích hợp theo cặp. | Duy trì chạy độc lập, đề xuất JSON + CLI và thống nhất schema. |

Phối hợp Cặp C hiện là đề xuất: công cụ của Đức Anh xuất kết quả đánh giá có cấu trúc để framework của Vĩnh có thể điều phối. Chưa ghi nhận giao diện hoặc mốc tích hợp đã được cả hai thống nhất.

## 6. Sprint 1 Backlog — 12/11–25/11

Đây là backlog đề xuất, cần cập nhật theo kết quả Gate 1. P0 là việc cần hoàn thành cho luồng cốt lõi; P1 thực hiện sau khi P0 ổn định.

| ID | Công việc | Ưu tiên | Phụ trách | Điều kiện hoàn thành |
| --- | --- | --- | --- | --- |
| S1-01 | Hoàn thiện parser HTML/.msg và ánh xạ nguồn | P0 | Đức Anh | Mọi biến thể nằm trong phạm vi có kết quả đối chiếu; lỗi đọc được báo rõ. |
| S1-02 | Hoàn thiện checklist và Rule Engine | P0 | Đức Anh; mentor rà soát nghiệp vụ | Mỗi luật có mã, mô tả, phiên bản và ca đúng/sai; mọi giả định chưa duyệt được đánh dấu. |
| S1-03 | Hoàn thiện kiểm tra bằng LLM | P0 | Đức Anh | Đầu ra được kiểm tra schema; kết luận có nguồn hoặc needs_review; có đánh giá sai lệch. |
| S1-04 | Hoàn thiện email draft | P0 | Đức Anh | Email bám đầu vào và kết quả; các ca thiếu dữ liệu không bị mô tả là đã đủ. |
| S1-05 | Xây giao diện rà soát tối thiểu | P1 | Đức Anh | Xem báo cáo, nguồn, mục cần bổ sung và sao chép email. |
| S1-06 | Chuẩn hóa bộ đánh giá và báo cáo | P0 | Đức Anh | Có tập phát triển/tập đánh giá riêng, lệnh chạy và kết quả theo phiên bản; tính được metric đã thống nhất. |
| S1-07 | Thử giao diện tích hợp Cặp C | P1 | Đức Anh phụ trách phía CIP; phần Vĩnh chờ thống nhất | Có ví dụ request/result và một lần gọi thử nếu hai bên thống nhất; vẫn chạy độc lập được. |
| S1-08 | Chuẩn bị CP1 và CP2 | P0 | Đức Anh | CP1 demo mockup ngày 18/11; CP2 demo, kết quả Sprint 1 và retro ngày 25/11. |

Từ 19/11, chỉ sử dụng dữ liệu masked nếu được mentor cung cấp và cho phép; lưu tại nơi được chỉ định, không commit. Repo chỉ chứa dữ liệu mockup. Việc tiếp nhận masked không phải điều kiện để hoàn thành skeleton Gate 1.

## 7. Gate 1 Evidence & Review

| Đầu ra bắt buộc | Nội dung trong tài liệu | Bằng chứng còn cần bổ sung |
| --- | --- | --- |
| Skeleton end-to-end | Mục 2 | Link mã nguồn, phiên bản, lệnh chạy, input/output demo. |
| Kiểm chứng giả định rủi ro nhất | Mục 3 | Bộ mockup, đáp án, kết quả chạy và phân tích lỗi. |
| Kế hoạch điều chỉnh | Mục 5 | Góp ý Gate 0 và thay đổi có căn cứ. |
| Baseline metric | Mục 4 | Số đo thực tế, số đếm và cấu hình chạy. |
| Backlog Sprint 1 | Mục 6 | Ưu tiên và phạm vi được cập nhật sau Gate 1. |

Kịch bản trình bày 10 phút đề xuất: 1 phút nêu bài toán và phạm vi; 4 phút chạy demo; 2 phút trình bày kiểm chứng; 2 phút baseline và điều chỉnh; 1 phút backlog. Dành 5 phút hỏi đáp theo kế hoạch thực tập. Khi có trang Confluence và bằng chứng, ghi link đầu ra vào sheet “Mốc”.

## 8. References

1. Vaswani, A., et al. (2017). Attention Is All You Need. https://arxiv.org/abs/1706.03762
2. Devlin, J., Chang, M.-W., Lee, K., & Toutanova, K. (2019). BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. https://aclanthology.org/N19-1423/
3. Brown, T. B., et al. (2020). Language Models are Few-Shot Learners. https://arxiv.org/abs/2005.14165
4. Ji, Z., et al. (2023). Survey of Hallucination in Natural Language Generation. ACM Computing Surveys. https://doi.org/10.1145/3571730 — bản arXiv: https://arxiv.org/abs/2202.03629 (có các bản cập nhật sau xuất bản).
5. Lewis, P., et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. https://arxiv.org/abs/2005.11401

Nguồn yêu cầu Gate 1: Kế hoạch thực tập 6 tuần, mục “Mốc và đầu ra bắt buộc”. Bối cảnh dự án kế thừa từ kế hoạch MVP và pair contract v0 ngày 02/11/2026 trong repo. Khi đưa lên Confluence, bổ sung liên kết tới bản kế hoạch và các trang dự án mà người đọc có quyền truy cập.
