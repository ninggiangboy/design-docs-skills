# Danh mục tài liệu chuẩn

Dùng để dựng master plan §3.1 (cây thư mục) và §3.2 (nội dung bắt buộc, gate). Đây là **khung để chọn**, không phải danh sách phải chép nguyên:

1. Lấy mọi tài liệu **Luôn có**.
2. Lấy tài liệu **Có điều kiện** khi SDD thỏa điều kiện.
3. Nhóm `06-design` sinh **một tài liệu cho mỗi thành phần hay cơ chế lớn** trong SDD (mỗi mục cấp 2 của SDD về một module thường là một tài liệu), cộng các tài liệu xuyên suốt.
4. Viết lại cột "Nội dung bắt buộc" cho **dự án cụ thể**: tên bảng, tên job, tên màn hình, mã DR liên quan. Cột này trong plan phải cụ thể đến mức người viết tài liệu biết chính xác phải có những mục nào. Câu chung chung như "mô tả thiết kế" là không đạt.
5. Đánh số `DOC-01…` theo thứ tự xuất hiện trong cây. Tài liệu thêm sau lấy số kế tiếp.

Gate mặc định: tài liệu nền (product, glossary, kiến trúc, mô hình dữ liệu lõi, dev local) gate **P1**; tài liệu thiết kế gate là **phase hiện thực nó**; tài liệu UI gate phase UI; runbook và thực nghiệm gate phase đo/vận hành. Tài liệu "cập nhật liên tục" (configuration-reference, ci-cd) ghi "khung có ở P1".

## 00 · Điều phối (luôn có, do skill master plan tạo)

| File | Nội dung |
| --- | --- |
| `README.md` | Mục lục, thứ tự đọc, bảng DOC × trạng thái, bảng thư mục, quy ước rút gọn |
| `00-master-plan.md` | Theo blueprint master-plan.md |
| `00-decision-register.md` | Theo blueprint decision-register.md |

## 01-product (luôn có)

| File | Nội dung bắt buộc |
| --- | --- |
| `vision-and-scope.md` | Bối cảnh, vấn đề, tầm nhìn (các lớp giá trị). Câu hỏi nghiên cứu hoặc mục tiêu kinh doanh. **Mục tiêu đo được** gắn với NFR và cách kiểm chứng. Trong/ngoài phạm vi (có lý do cho mục ngoài phạm vi). Giả định. Ràng buộc (máy, thời gian, người, ngân sách). Thứ tự cắt giảm |
| `personas-and-journeys.md` | Bảng persona `PS-x` (role trong hệ thống, thiết bị, mức kỹ thuật, tần suất). Mỗi persona: mục tiêu, nỗi đau, cần gì từ hệ thống, không cần gì, màn hình dùng. Mỗi persona một journey `J-x` (bước, cảm xúc, điểm chạm màn hình/endpoint) |
| `requirements.md` | FR giữ mã của SDD, yêu cầu bổ sung đánh số tiếp và ghi "(bổ sung)". Mỗi FR tách thành `FR-xx.y` trong bảng: yêu cầu, **tiêu chí nghiệm thu Given/When/Then có số liệu cụ thể**, ưu tiên MoSCoW, cách kiểm chứng (loại test, EXP). NFR: chỉ tiêu có số, cách đo, công cụ, EXP/việc kiểm chứng. Ma trận FR → UC → F → DOC thiết kế |
| `use-cases.md` | Sơ đồ use case tổng (Mermaid). Mỗi `UC-xx` theo template A.2: actor, trigger, tiền điều kiện, luồng chính đánh số, luồng thay thế (2a…), luồng lỗi (E1…), hậu điều kiện, quy tắc, màn hình/endpoint/sự kiện, FR. Danh sách UC lấy từ master plan §3.4 |
| `feature-catalog.md` | `F-<NHÓM>-xx` theo nhóm. Mỗi tính năng: mô tả, FR, UC, phase hoàn thành, MoSCoW, cờ bật/tắt, phụ thuộc, app chứa nó, bị cắt ở bước nào trong thứ tự cắt giảm |

## 02-glossary.md (luôn có)

Bảng theo nhóm chủ đề: thuật ngữ (tên dùng trong code/UI) · tên tiếng Việt · định nghĩa 1–3 câu (có ví dụ khi cần) · liên quan (DR/DOC/chuẩn). Master plan liệt kê **danh sách thuật ngữ tối thiểu** — quét SDD lấy mọi danh từ chuyên môn, mọi thuật ngữ miền, mọi khái niệm độ tin cậy, mọi tên công cụ hạ tầng. Gate P1 và viết **đầu tiên**.

## 03-architecture

| File | Điều kiện | Nội dung bắt buộc |
| --- | --- | --- |
| `system-context-and-containers.md` | Luôn | C4 mức 1 (người dùng, hệ thống ngoài). C4 mức 2 (mọi container, giao thức giữa chúng). Bảng đơn vị triển khai. **Bảng quyền sở hữu dữ liệu**: bảng/topic/bucket nào do ai ghi, ai đọc. Ranh giới tin cậy |
| `data-flows.md` | ≥ 2 thành phần trao đổi dữ liệu | Sequence diagram cho **mọi luồng chính** (liệt kê tên từng luồng trong plan) **và các luồng lỗi** (DB chết giữa chừng, tiến trình bị kill trước ack, dịch vụ ngoài timeout…) |
| `messaging-contracts.md` | Có broker, event, webhook hay trao đổi file | Bảng topic/queue, envelope, JSON Schema theo version, header, quy tắc tương thích ngược, quy tắc tính hash/khóa |
| `quality-attributes.md` | Luôn | Mỗi NFR: chiến thuật → cơ chế cụ thể → nơi hiện thực → kiểm chứng. Ngân sách độ trễ theo chặng. **Ước lượng dung lượng** (event/s, dòng/ngày, GB/ngày ở tải nền và ×10). Ngân sách tài nguyên trên máy mục tiêu |
| `tech-stack-and-versions.md` | Luôn | Bảng thư viện/công cụ: phiên bản cố định, lý do, license. Công cụ dev. Bảng tương thích (từ spike) |
| `code-architecture.md` | Có quy tắc kiến trúc code (Clean/Hexagonal/layer) | Tầng, quy tắc phụ thuộc, bố cục package, đặt tên, DTO/mapping, transaction ở tầng nào, luật kiểm tra tự động (ArchUnit…), ngoại lệ, checklist review |

## 04-adr (luôn có)

`README.md` (bảng ADR · tiêu đề · trạng thái · gate · nguồn DR) và `0001-record-architecture-decisions.md`. Các ADR khác sinh từ DR ở cấp kiến trúc. Master plan liệt kê từng ADR kèm nguồn (DR/SDD §) và gate.

## 05-data (khi có lưu trữ)

| File | Điều kiện | Nội dung bắt buộc |
| --- | --- | --- |
| `source-data.md` | Có dữ liệu nguồn từ ngoài hoặc hệ thống nguồn | Nguồn, license, hash, thống kê. Trường được dùng và ánh xạ sang bảng. Schema nguồn có DDL. Quy tắc thời gian |
| `<core>-model.md` (warehouse-model, domain-model…) | Có DB | ERD Mermaid. **DDL đầy đủ chạy được** cho mọi bảng nghiệp vụ. Index và lý do. Grain, business key, cột audit. Câu upsert/truy vấn mẫu cho bảng chính |
| `ops-model.md` | Có bảng vận hành/trạng thái (job, queue, audit, cờ) | DDL. **Sơ đồ máy trạng thái** cho mọi cột trạng thái. Enum dùng chung |
| `data-quality-rules.md` | Có ingest/validate dữ liệu | Danh mục `DQ-xx`: bảng, lớp (trước/sau khi ghi), biểu thức hoặc SQL, mức độ, hành động, ngưỡng |
| `db-roles-and-grants.md` | ≥ 2 app hoặc role dùng DB | Ma trận role × bảng × quyền (tới cột nếu cần). App dùng role nào. Cấp secret. Tách user migration khỏi user runtime. Ma trận test quyền |
| `data-lifecycle.md` | Có dữ liệu tăng theo thời gian | Retention từng bảng/bucket. Job bảo trì và dọn dẹp. Lịch backup. Chính sách PII |

## 06-design

**Khung chung** của mọi tài liệu nhóm này (ghi vào plan): Mục đích → Phạm vi → Thành phần và interface (chữ ký code) → Thuật toán (pseudo-code) → Transaction và đồng thời → Cấu hình → Metrics và log → Lỗi và cách xử lý → Test bắt buộc (bảng có mã) → Câu hỏi còn mở (rỗng khi Approved).

Theo từng thành phần trong SDD (ví dụ đã gặp): xử lý batch/chunk, consumer streaming, nạp dữ liệu tĩnh, DLQ và replay, analytics (mỗi thuật toán có **bảng test dữ liệu vào → kết quả kỳ vọng**), AI/LLM (cổng trừu tượng, adapter, ngưỡng, cờ tắt, an toàn), simulator/nguồn giả lập, giao sự kiện real-time (SSE/WebSocket), công cụ demo.

Xuyên suốt (luôn có khi có backend):

| File | Nội dung bắt buộc |
| --- | --- |
| `security.md` | Authn/authz, **ma trận endpoint × role**, CORS, rate limit, secret theo môi trường, TLS, PII, STRIDE rút gọn theo ranh giới tin cậy, quét bảo mật trong CI |
| `observability.md` | **Danh mục metric** (tên, loại, label, service, ý nghĩa). Trường log bắt buộc. Span và lan truyền trace. Dashboard (danh sách panel). **Alert rule viết bằng ngôn ngữ truy vấn thật** (PromQL…) kèm link runbook. Kênh gửi |
| `configuration-reference.md` | Mỗi app: key · kiểu · mặc định · biến môi trường · profile · mô tả. Cờ runtime |
| `error-handling.md` | Phân loại lỗi. Exception/mã lỗi → loại → hành động. Exception → HTTP status → Problem type. Quy ước log lỗi |

## 07-api (khi có API)

| File | Nội dung bắt buộc |
| --- | --- |
| `api-guidelines.md` | Đặt tên, versioning, phân trang, lọc, thời gian, lỗi, cache, header, idempotency |
| `api-endpoints.md` | Mỗi endpoint một mục `E-xx` theo template A.4: mục đích/UC, quyền, tham số, response mẫu, lỗi, nguồn dữ liệu (bảng, câu truy vấn, index), cache, mục tiêu hiệu năng, sự kiện liên quan |
| `<events>.md` | Có SSE/WebSocket/webhook: danh sách kiểu sự kiện, payload mẫu, kênh, quyền |

## 08-ux-ui (khi có UI)

| File | Nội dung bắt buộc |
| --- | --- |
| `ux-principles-and-ia.md` | Nguyên tắc UX đánh số. Sitemap. Điều hướng theo role. Sơ đồ URL kèm search params. Responsive. Ngân sách hiệu năng |
| `design-system.md` | Token (màu, chữ, spacing, radius, dark mode, màu theo trạng thái nghiệp vụ). Danh mục component. Quy ước biểu đồ/bản đồ. Tiêu chí a11y |
| `screens/*.md` | **Mỗi màn hình một file** theo template A.5 + `README.md` chỉ mục. Plan liệt kê tên từng file |
| `ui-states-and-copy.md` | Mẫu loading/empty/error/stale/không có quyền. Toàn bộ microcopy. Định dạng số và thời gian |

## 09-operations

| File | Điều kiện | Nội dung bắt buộc |
| --- | --- | --- |
| `local-dev.md` | Luôn | Yêu cầu máy. Cài công cụ. `make` target. Bảng port. Tài khoản demo. Seed/reset dữ liệu. Lỗi thường gặp |
| `deploy-<target>.md` | Mỗi môi trường đích | Profile, thứ tự khởi động, healthcheck, tài nguyên, biến môi trường và secret, nâng cấp, migration, gỡ bỏ (k8s: probe, PDB, autoscale, NetworkPolicy…) |
| `ci-cd.md` | Luôn | Stage, điều kiện chặn merge, cache, tag image, deploy, smoke test |
| `runbooks/RB-xx-*.md` | Có alert | Mỗi alert một runbook theo template A.7, cộng runbook cho thao tác vận hành nguy hiểm (replay, khôi phục, xoay secret) |
| `backup-restore.md` | Có trạng thái bền | Lịch, quy trình khôi phục từng bước, RPO/RTO, cách kiểm chứng |

## 10-testing

| File | Điều kiện | Nội dung bắt buộc |
| --- | --- | --- |
| `test-strategy.md` | Luôn | Tháp test. Module × tầng test. Công cụ. Quy ước đặt tên. Dữ liệu test/fixture. Chỉ tiêu coverage theo module. Test tiêm lỗi, contract, hiệu năng. Test nào chạy ở stage CI nào. **Chỉ mục tiền tố mã test** của mọi tài liệu |
| `experiments/EXP-xx-*.md` + `README.md` | Có câu hỏi nghiên cứu hoặc tuyên bố định lượng cần chứng minh | README: protocol chung, ground truth, baseline, công thức chung. Mỗi EXP theo template A.6 |
| `demo-script.md` | Có buổi demo/bảo vệ | Các bước kèm lời thoại, thao tác, kết quả mong đợi, dự phòng khi hỏng, checklist trước buổi, cách reset |

## 11-report (khi là đồ án/luận văn/báo cáo)

`thesis-mapping.md`: khung chương báo cáo; mỗi mục lấy nội dung, hình, bảng từ tài liệu/kết quả nào; luận điểm ↔ bằng chứng; quy trình chuẩn bị.
