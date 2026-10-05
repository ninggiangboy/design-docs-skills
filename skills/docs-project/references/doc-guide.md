# Hướng dẫn viết từng loại tài liệu

Nguồn sự thật cho **nội dung bắt buộc** là hàng của tài liệu trong master plan §3.2. File này bổ sung: tài liệu tốt trông thế nào, độ sâu cần có, lỗi hay gặp. Khung mục lấy từ templates.md.

## Nguyên tắc chung

- **Bám checklist của plan.** Trước khi viết, chép các ý trong "Nội dung bắt buộc" thành danh sách; mỗi ý thành một mục hoặc một bảng. Viết xong, đánh dấu từng ý đã có ở mục nào.
- **Viết để người khác làm được mà không phải hỏi.** Người đọc là người sẽ code việc `Pn-xx` trỏ tới tài liệu này. Thiếu tên bảng, tên key, giá trị mặc định, mã lỗi là thiếu.
- **Ví dụ thật.** JSON đầy đủ trường, SQL chạy được, bảng test có số liệu cụ thể. Số liệu lấy từ dữ liệu thật khi có (viết script nhỏ đo, ghi đường dẫn script và ngày đo).
- **Ranh giới.** Mỗi tài liệu nói rõ phần nào nằm ở tài liệu khác. Không chép lại nội dung của tài liệu khác; trỏ bằng `DOC-xx §n`.
- **Quyết định mới.** Gặp chỗ phải chọn mà SDD và DR chưa trả lời: tạo DR (xem SKILL.md). Tài liệu nào sinh nhiều quyết định thì thêm câu "Mọi quyết định mới trong tài liệu này được ghi là … và tóm tắt ở §N" và một mục tóm tắt cuối.
- **Câu hỏi còn mở** là mục cuối của mọi tài liệu (trừ ADR). "Không có." khi Approved; nếu đã chốt điều gì trong lúc viết thì có thể ghi kèm: "Không có. Các quyết định phát sinh đã ghi thành DR-67, DR-68."
- **Độ dài** theo nội dung, không theo số trang. Tham khảo dự án mẫu: vision 90 dòng, requirements 200, use case 250, glossary 250, tài liệu thiết kế 300–700, danh mục endpoint 1.600, runbook 50, thực nghiệm 140.

## Glossary (viết đầu tiên)

- Nhóm theo chủ đề (miền nghiệp vụ → dữ liệu → xử lý → hạ tầng → thực nghiệm).
- Có đủ **danh sách tối thiểu** trong plan. Thêm mọi từ mà các tài liệu nền sẽ dùng.
- Định nghĩa nói cả cách dự án dùng từ đó, không chỉ nghĩa từ điển ("Hệ thống này dùng JSON envelope thay cho Protobuf (DR-03)").
- Cột Thuật ngữ là tên dùng trong code/UI. Từ có nhiều nghĩa trong dự án (ví dụ "replay" của DLQ và của raw zone) thì tách nghĩa rõ.

## Product

- **vision-and-scope**: bảng "Mục tiêu đo được" có cột chỉ tiêu, NFR, cách kiểm chứng (EXP/test). Ngoài phạm vi có lý do. Thứ tự cắt giảm khớp master plan §4.3.
- **personas-and-journeys**: bảng tổng PS-x trước, chi tiết sau. Ghi rõ tên persona chỉ để minh họa. Journey nêu điểm chạm cụ thể (màn hình, endpoint) để màn hình về sau trỏ ngược được ("Journey J-1 bước 1–3").
- **requirements**: §0 Quy ước (MoSCoW, ký hiệu G/W/T, cột kiểm chứng). Mỗi FR là một mục `### FR-xx · <tên>` có bảng FR-xx.y. Tiêu chí nghiệm thu có **số cụ thể** (127 dòng, 10 giây p95, 499 trên 500). Yêu cầu sửa sau đó ghi `*Sửa YYYY-MM-DD (DR-xx): …*`. Kết thúc bằng bảng NFR và ma trận FR → UC → F → DOC.
- **use-cases**: §0 sơ đồ use case tổng (Mermaid flowchart actor → UC). Ghi một lần quy ước viết tắt (prefix endpoint, chuỗi UI trong ngoặc kép). Luồng lỗi nêu hành vi UI cụ thể và chuỗi thông báo.
- **feature-catalog**: §0 quy ước cột, §1 tổng quan (số tính năng theo nhóm × phase), mỗi nhóm một bảng, mục cuối ánh xạ thứ tự cắt giảm → tính năng.

## Architecture

- **system-context-and-containers**: Mermaid cho C4 mức 1 và 2; bảng container (công nghệ, trách nhiệm, port, giao thức); bảng đơn vị triển khai; **quyền sở hữu dữ liệu theo từng kho** (bảng/schema/topic/bucket × ghi bởi × đọc bởi); ranh giới tin cậy (ai xác thực ở đâu, secret nào qua ranh giới nào); mục cuối truy vết tới tài liệu khác.
- **data-flows**: mỗi luồng một `sequenceDiagram` kèm vài dòng giải thích các điểm commit/ack. Luồng lỗi quan trọng ngang luồng chính.
- **messaging-contracts**: JSON Schema đặt trong code (đường dẫn ghi rõ), tài liệu có ví dụ đầy đủ và bảng trường. Quy tắc tương thích ngược viết thành luật kiểm được.
- **quality-attributes**: bảng NFR → chiến thuật → cơ chế → nơi hiện thực → kiểm chứng. Ngân sách độ trễ chia chặng có tổng. Ước lượng dung lượng tính từ dữ liệu thật bằng script (ghi tên script). Phân biệt rõ con số kế hoạch và con số đo.
- **tech-stack-and-versions**: phiên bản cố định (không "latest"), lý do chọn, license; bảng tương thích từ spike.

## ADR

- Một ADR một quyết định, nguồn từ DR. Tiêu đề là quyết định ("Effectively-once bằng at-least-once cộng upsert theo business key"), không phải chủ đề.
- "Các phương án" nêu cả phương án hiển nhiên bị loại và lý do loại.
- "Hệ quả" phải có phần **tiêu cực** thật.
- Cập nhật `04-adr/README.md` (bảng ADR · tiêu đề · trạng thái · gate · nguồn).

## Data

- **DDL phải chạy được.** Nếu máy có Docker, dựng DB tạm (`docker run --rm` image đúng phiên bản trong tech-stack) và chạy toàn bộ DDL theo thứ tự trước khi đưa tài liệu sang Review; ghi "DDL đã chạy thử trên <DB phiên bản> ngày …". Không có Docker thì ghi rõ là chưa chạy thử.
- Mỗi bảng: grain, business key, ai ghi/ai đọc, DDL, index kèm lý do (trỏ tới truy vấn dùng nó), câu upsert/truy vấn mẫu.
- Mọi cột trạng thái có `stateDiagram-v2` và bảng chuyển trạng thái (từ → sang · ai · khi nào).
- Ma trận quyền DB đi kèm danh sách ca test quyền (role × thao tác × kỳ vọng).

## Design (06-design)

- Theo khung B.1. Interface viết bằng chữ ký code thật của ngôn ngữ dự án. Thuật toán bằng pseudo-code đánh số bước.
- Mục Transaction và đồng thời trả lời: cái gì commit cùng nhau, offset/ack khi nào, nhiều replica chạy cùng lúc thì sao, tiến trình chết ở từng điểm thì sao.
- **Test bắt buộc**: bảng `ID · Kịch bản · Kỳ vọng`, tiền tố riêng của tài liệu (đăng ký trong test-strategy). Kịch bản và kỳ vọng có số liệu. Thuật toán nghiệp vụ có bảng dữ liệu vào → kết quả kỳ vọng.
- Cấu hình và metric của tài liệu phải xuất hiện trong configuration-reference và observability (thêm vào đó nếu hai tài liệu này đã có).
- Tài liệu xuyên suốt: security có ma trận endpoint × role đầy đủ; observability có alert viết bằng PromQL (hoặc ngôn ngữ truy vấn thật) kèm `for`, severity, link runbook; error-handling có bảng ánh xạ mã lỗi/exception → loại → hành động → HTTP status → Problem type.

## API

- Mỗi endpoint một mục `### E-xx \`METHOD /path\` · \`operationId\``; mã E-xx dùng lại trong màn hình, test, OpenAPI.
- Response ví dụ đầy đủ trường, đúng định dạng thời gian và phân trang của api-guidelines.
- Nguồn dữ liệu nêu câu SQL chính và index; mục tiêu hiệu năng có số.
- §2 Tổng quan là bảng mọi endpoint (mã, method, path, quyền, UC, màn hình).

## UX/UI

- Mỗi màn hình một file theo A.5, wireframe ASCII (desktop và mobile nếu có), dữ liệu trỏ bằng mã E-xx và kênh real-time.
- Tiêu chí nghiệm thu có mã riêng của màn hình, viết Given/When/Then; ca E2E đặt tên được thành test.
- Microcopy viết đúng chuỗi sẽ hiện (ngôn ngữ UI), gom lại trong ui-states-and-copy.

## Operations

- Lệnh trong local-dev, deploy, runbook **chạy được nguyên văn** (copy-paste), có kết quả mong đợi.
- Runbook: Kiểm tra gồm truy vấn metric, SQL, lệnh container/k8s; Xử lý đánh số; Xác nhận đã xong là điều kiện đo được.
- Mỗi alert trong observability có đúng một runbook; README của runbooks có bảng alert → RB.

## Testing

- **test-strategy** có bảng chỉ mục mọi tiền tố mã test và tài liệu chứa chúng, chỉ tiêu coverage theo module, stage CI chạy từng loại test.
- **experiments/README** định nghĩa protocol chung: ground truth, baseline, công thức chỉ số dùng chung, số lần lặp, máy chạy, cách lưu kết quả. Từng EXP chỉ nói phần riêng.
- **demo-script**: mỗi bước có lời thoại, thao tác, kết quả mong đợi, dự phòng khi hỏng; checklist trước buổi; cách reset.
