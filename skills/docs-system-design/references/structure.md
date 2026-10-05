# Khung SDD

Rút từ hai SDD mẫu: *Public Transport Intelligence* (đồ án nghiên cứu, pipeline dữ liệu) và *Hệ thống đặt vé sự kiện* (sản phẩm, đúng đắn dưới tải cao). Bản đặt vé mới hơn và đã qua nhiều lượt sửa, nên khi hai bản khác nhau thì theo bản đặt vé.

SDD trả lời **cái gì, vì sao, và cơ chế chính hoạt động thế nào**. Nó chưa phải đặc tả chi tiết: DDL đầy đủ, mọi endpoint, mọi màn hình thuộc bộ docs sinh sau (skill `docs-master-plan`, `docs-project`). Phần lõi thì phải đủ sâu để người đọc tin rằng thiết kế đúng: câu SQL then chốt, máy trạng thái, cách xử lý tranh chấp, phương án bị loại. Phần phụ chỉ cần đủ để biết nó tồn tại, làm gì và giao tiếp với phần lõi ra sao.

## Khối đầu

```markdown
# <Tên hệ thống> — Thiết kế hệ thống

<Mon D, YYYY> · @<tác giả>

<Đoạn mở đầu 2–4 câu: hệ thống làm gì cho ai; yêu cầu/bất biến quan trọng nhất; giai đoạn này gồm gì, để sau gì (mục 2.3).>
```

Ngày viết kiểu tiếng Anh (`Oct 5, 2026`). Tác giả lấy theo người dùng chỉ định, mặc định là tên người dùng git.

## Các mục

Số mục chỉ là gợi ý. Bỏ mục không áp dụng, tách mục lõi thành nhiều mục, nhưng giữ **thứ tự logic**: vấn đề → mục tiêu → người dùng → kiến trúc → các mục miền (lõi trước) → dữ liệu → API → giao diện → vận hành → kiểm thử → kế hoạch → rủi ro → phụ lục.

### 1. Giới thiệu

| Mục | Nội dung | Dạng |
| --- | --- | --- |
| 1.1 Bối cảnh | Miền nghiệp vụ, vì sao bài toán khó (đặc tính dữ liệu, quy mô, tính chất hàng hóa) | 1–2 đoạn |
| 1.2 Vấn đề thực tế | 3–5 vấn đề, mỗi vấn đề **in đậm một câu tóm tắt** rồi giải thích hậu quả cụ thể | Danh sách |
| 1.3 Tầm nhìn | 2–3 "lớp giá trị", đánh số, **tên lớp in đậm** — giải thích; ghi lớp nào để giai đoạn sau | Danh sách đánh số |

### 2. Mục tiêu, phạm vi và trọng tâm

| Mục | Nội dung |
| --- | --- |
| 2.1 Câu hỏi nghiên cứu *(đồ án)* / Bài toán cốt lõi *(sản phẩm)* | Một câu hỏi trong blockquote `>`, nêu đủ ràng buộc khó ("kể cả khi request bị gửi lại, tiến trình dừng đột ngột…"). Kèm **kịch bản mục tiêu có số** (100.000 người tranh 5.000 vé; 500 xe, 100 event/giây). Nếu có bất biến đứng trên mọi yêu cầu khác thì nêu riêng (có thể trong code block cho nổi bật: `NEVER OVERSELL`) |
| 2.2 Mức độ đầu tư theo module | Bảng `Module · Vai trò · Mức độ đầu tư`. Mức: "Đào sâu, có thực nghiệm đo đạc" / "Đào sâu" / "Triển khai chắc chắn" / "Mức cơ bản" / "Làm sau khi lõi đã đúng". Bảng này quyết định độ sâu của từng mục phía sau |
| 2.3 Phạm vi | **Trong phạm vi** (danh sách, có số liệu và ràng buộc cụ thể). **Để sau** (bảng `Hạng mục · Nội dung · Giai đoạn này xử lý thế nào` — cột cuối chứng minh thiết kế hiện tại không chặn đường phát triển). **Ngoài phạm vi** (danh sách, có lý do khi không hiển nhiên) |

### 3. Người dùng, use case và yêu cầu

| Mục | Nội dung |
| --- | --- |
| 3.1 Nhóm người dùng | Mỗi nhóm: **tên** — cần gì, làm gì. Ghi quan hệ giữa vai trò (một tài khoản có thể có hai vai trò…) |
| 3.2 Use case *(nên có)* | Sơ đồ Mermaid `flowchart LR` actor → UC, nhóm bằng `subgraph`; bảng `Mã · Vai trò · Use case`. Có UC của "Hệ thống" (job tự động) |
| 3.3 Yêu cầu chức năng | Bảng `Mã · Yêu cầu`, `FR-01…`, mỗi dòng một câu có thể kiểm tra |
| 3.4 Yêu cầu phi chức năng | Bảng `Mã · Yêu cầu · Chỉ tiêu`. **Chỉ tiêu có số** và điều kiện đo; NFR quan trọng ghi luôn EXP kiểm chứng. Câu cuối: con số tải là mục tiêu thiết kế, hiệu chỉnh theo máy thực nghiệm |

### 4. Kiến trúc tổng thể và công nghệ

- Đoạn mở: kiểu kiến trúc (modular monolith, pipeline, microservice…) **và lý do** gắn với bài toán ("tính đúng đắn dựa trên transaction cục bộ; tách service buộc phải dùng transaction phân tán").
- Sơ đồ Mermaid toàn hệ thống (người dùng → edge → app → kho dữ liệu → dịch vụ ngoài), nhãn cạnh nói vai trò ("mọi câu ghi có điều kiện", "chỉ để giảm tải"). Một câu dưới sơ đồ tóm tắt luồng chính.
- 4.1 Các thành phần: danh sách đánh số, **tên** — trách nhiệm, công nghệ, ranh giới ("module chỉ gọi nhau qua interface công khai").
- 4.2 Nguyên tắc xuyên suốt (hoặc Luồng dữ liệu nếu là pipeline): 3–6 nguyên tắc in đậm, mỗi nguyên tắc là một quyết định thiết kế có hệ quả ("**Redis chỉ giảm tải, không quyết định.** Mất Redis thì chậm hơn nhưng vẫn không bán vượt").
- 4.3 Công nghệ: bảng `Lớp · Công nghệ`, ghi cụ thể thư viện, không chỉ tên framework.

### 5…N. Các mục miền

Một mục cho mỗi module trong bảng 2.2, **module lõi trước và sâu nhất**. Mỗi mục mở bằng **một câu nêu quy tắc chi phối** của module ("Trạng thái đơn hàng chỉ đổi sang đã thanh toán khi server nhận webhook đã xác minh chữ ký; mọi tín hiệu từ trình duyệt đều không được tin."). Các khối thường dùng (chọn theo nội dung, xem style.md):

- Luồng đánh số kèm `sequenceDiagram`.
- Bảng bất biến `Đối tượng · Bất biến · Được ép bằng`.
- Vòng đời: `stateDiagram-v2` **và** bảng chuyển trạng thái `Từ · Sang · Kích hoạt bởi · Tác động`.
- Câu SQL / đoạn code then chốt kèm giải thích vì sao đúng khi đồng thời.
- Tranh chấp giữa hai luồng: quy tắc trọng tài, các bước, `sequenceDiagram` có `alt`.
- Bảng quy tắc / tham số `Hạng mục · Quy tắc` hoặc `Tham số · Mặc định · Ý nghĩa`.
- Thuật toán: công thức (code block `latex`), các trường hợp, edge case.
- Phân tích phương án: Phương án A/B/C/D, mỗi cái ưu/nhược/kết luận, bảng so sánh, lý do chọn đánh số.
- Bảng cơ chế `Cơ chế · Hiện thực` (độ tin cậy, chịu tải…).
- Hình minh họa giao diện kèm **bản chữ ASCII** để xuất Markdown.

Mức "Mức cơ bản" chỉ cần 1–3 đoạn hoặc một bảng.

### Mô hình dữ liệu

- Câu mở nói rõ mức chi tiết ("chỉ chốt mô hình khái niệm và các ràng buộc bắt buộc; DDL chi tiết viết khi cài đặt") **hoặc** đưa DDL của các bảng lõi.
- `erDiagram` hoặc bảng `Bảng · Loại · Nội dung chính`.
- Bảng **ràng buộc bắt buộc** `Ràng buộc · Bảo vệ điều gì` — ràng buộc là một phần thiết kế, DB từ chối trạng thái sai kể cả khi code lỗi.
- Quy ước chung (tiền là số nguyên đơn vị nhỏ nhất, thời gian UTC, migration bằng gì).

### Backend API

- Câu mở: kiểu API, các nhóm, ai được gọi gì.
- Bảng `Nhóm · Endpoint · Mô tả` (nhóm chỉ ghi ở dòng đầu).
- Ví dụ request/response cho endpoint lõi (JSON đầy đủ, cả response lỗi).
- Quy ước: bảng lỗi `HTTP · code · Khi nào`, tiền, thời gian, phân trang, hợp đồng (OpenAPI → client), truy vết, real-time.

### Giao diện

- Câu mở: một hay nhiều app, khu vực, tải lười phần nặng.
- Luồng màn hình theo từng vai trò (`flowchart LR`).
- Bảng `Khu vực · Màn hình · Nội dung` (hoặc `Màn hình · Nội dung · Phục vụ`).
- Kỹ thuật: tách bundle, quản lý state, real-time, đồng hồ theo server, optimistic UI, khả năng tiếp cận, thiết bị, trạng thái rỗng/tải/lỗi.

### Vận hành, triển khai và chịu lỗi

- Triển khai: sơ đồ, bảng container/workload `Thành phần · Triển khai · Số replica · Ghi chú`, cấu hình và secret.
- Observability và alerting nếu trong phạm vi: log, metric, trace; bảng `Cảnh báo · Điều kiện · Mức`.
- **Hành vi khi có sự cố**: bảng `Sự cố · (Phát hiện) · Hành vi hệ thống · Phục hồi`, gồm sự cố nội bộ và dịch vụ ngoài. Câu nguyên tắc: hệ thống nghiêng về phía an toàn nào.
- Kiểm tra bất biến / đối soát nếu bài toán có bất biến.
- Bảo mật: những điểm tối thiểu, cụ thể.
- Mở rộng theo tải (nếu có): đơn vị song song, giới hạn thật (partition, connection pool, quota), không scale mù.

### Kiểm thử và đánh giá

- Câu mở: tính đúng đắn được chứng minh bằng gì.
- Bảng chiến lược `Loại · Phạm vi · Công cụ`.
- Bảng thực nghiệm `Mã · Thực nghiệm · Cách làm · Chỉ số · Kỳ vọng`, `EXP-01…`. Mỗi tuyên bố định lượng của NFR có ít nhất một EXP. Có **baseline** (bản ngây thơ, không có cơ chế tương ứng) để so sánh.
- Đoạn cuối: nhóm EXP nào là bằng chứng cho tuyên bố nào.

### Kế hoạch triển khai

- Câu mở: nguyên tắc thứ tự (lõi đúng đắn trước, mỗi giai đoạn kết thúc bằng thứ chạy được).
- `flowchart LR` phụ thuộc giữa các giai đoạn, kèm nhánh "Để sau".
- Bảng `Giai đoạn · Nội dung · Kết quả đầu ra` (kết quả có EXP nào).
- **Thứ tự cắt giảm** một câu, kèm phần không được cắt và lý do.
- Kịch bản demo: 5–7 bước đánh số, mỗi bước là một thao tác và điều người xem thấy được.

### Rủi ro và giới hạn

- Bảng `Rủi ro hoặc giới hạn · Ảnh hưởng · Cách xử lý` (8–12 dòng), cách xử lý trỏ về mục đã thiết kế.
- **Điểm còn mở**: danh sách những gì chưa chốt (giá trị mặc định cần duyệt, lựa chọn đề xuất). Rỗng thì ghi "Không có".

### Phụ lục: Cấu trúc repo

Cây thư mục trong code block, comment `#` cho từng thư mục quan trọng, khớp với module ở mục 4.1. Một câu sau cây nếu có phần dùng chung đáng nêu.

## Biến thể

| Loại dự án | Khác biệt |
| --- | --- |
| Đồ án / nghiên cứu | 2.1 là câu hỏi nghiên cứu; 2.2 ghi "Vai trò trong đồ án"; có mục thực nghiệm đầy đủ kèm baseline; dashboard có thể là "công cụ minh chứng"; kế hoạch có cột cắt giảm giữ phần trả lời câu hỏi nghiên cứu |
| Sản phẩm theo giai đoạn | Đoạn mở đầu nói rõ giai đoạn; 2.3 có bảng "Để sau"; mỗi mục ghi phần nào để sau và vì sao thiết kế hiện tại không chặn |
| Pipeline dữ liệu | 4.2 là luồng dữ liệu (sơ đồ); có mục nguồn dữ liệu / giả lập; bảng cơ chế độ tin cậy; mục analytics |
| Hệ thống giao dịch | Bảng bất biến, câu ghi có điều kiện, idempotency, tranh chấp, kiểm tra bất biến |
| Có AI/ML | Mục riêng: AI dùng ở đâu và **không dùng ở đâu**, mẫu "code chuẩn bị state → mô hình phán đoán → code quyết định", ngưỡng, nguyên tắc an toàn, tắt được |
