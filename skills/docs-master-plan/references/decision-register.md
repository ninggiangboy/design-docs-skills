# Blueprint: `docs/00-decision-register.md`

Sổ quyết định là sản phẩm quan trọng nhất của bước lập kế hoạch. SDD thường nói tốt *cái gì* và *vì sao*, nhưng bỏ trống *chính xác như thế nào*. Mỗi chỗ trống là một DR, kèm **một phương án đề xuất cụ thể** để Owner duyệt nhanh. Đoán sai ở tầng dữ liệu và ngữ nghĩa thì rất tốn công sửa, nên các DR đó được chốt trước khi viết code.

## 1. Khung file

```markdown
# Sổ quyết định mở (Decision Register)

> Trạng thái tài liệu: **Review** · Cập nhật: YYYY-MM-DD · Nguồn: phân tích `<sdd>.md` (gọi tắt là **SDD gốc**)

<Một đoạn: SDD tốt ở đâu, thiếu "chính xác như thế nào" ở đâu, vì sao phải chốt trước.>

**Cách dùng**

- Mỗi mục có trạng thái: `Đề xuất` → (người sở hữu duyệt) → `Chốt` hoặc `Đổi` (ghi phương án thay thế).
- Mục đã chốt được chuyển vào tài liệu đích (dòng *Ghi vào*). Mục ở cấp kiến trúc thành ADR trong `docs/04-adr/`.
- **⚠ lệch SDD gốc**: đề xuất khác tài liệu gốc; lý do ghi kèm.
- **🔬 spike**: cần thử ngắn (≤ 1 ngày) trước khi chốt.

## Nhật ký chốt

| Ngày | Người chốt | Nội dung | Mục bị ảnh hưởng |
| --- | --- | --- | --- |

---

## A. <Nhóm chủ đề 1>

### DR-01 · <Câu hỏi cần chốt> — ⚠ lệch SDD gốc
- **Vấn đề:** …
- **Các phương án:** (1) … ; (2) … ; (3) … — chỉ khi có lựa chọn thật
- **Quyết định (đề xuất):** …
- **Hệ quả:** …
- **Ghi vào:** DOC-xx, ADR-xxxx.

…

---

## Tổng hợp theo mức ảnh hưởng

| Mức | Mục | Lý do cần chốt sớm |
| --- | --- | --- |
| Chặn P1 | DR-… | Quyết định schema, contract và cấu trúc repo |
| Chặn P2 | DR-… | … |
```

Khi Owner duyệt, tiêu đề DR thêm kết quả: `### DR-01 · Chọn feed nào — **Chốt: Metro Transit**`, và Nhật ký chốt có một dòng. Owner có thể duyệt gộp ("Chấp nhận toàn bộ các đề xuất còn lại") — ghi đúng như vậy.

## 2. Một DR tốt trông thế nào

- Tiêu đề là **một câu hỏi cụ thể**, không phải một chủ đề ("Ánh xạ poll sang chunk, và ack", không phải "Kafka").
- **Vấn đề** trích đúng chỗ SDD nói (SDD §x) và giải thích hậu quả nếu để nguyên.
- **Quyết định** đủ chi tiết để viết code: DDL, JSON mẫu đầy đủ trường, bảng topic/key/partition, giá trị mặc định có đơn vị, thuật toán đánh số bước, công thức. Ví dụ tốt:

  ```markdown
  ### DR-05 · Danh sách topic, key, partition
  - **Quyết định:**

    | Topic | Key | Partition | Retention | Ghi chú |
    | --- | --- | --- | --- | --- |
    | `gtfs.vehicle_positions` | `route_id` | 12 | 7 ngày | delete |

    Dev: RF = 1. k8s: RF = 3, `min.insync.replicas = 2`. Tạo topic bằng script, không bật auto-create.
  - **Ghi vào:** DOC-09, ADR-0008.
  ```
- Có lựa chọn thật thì liệt kê phương án với ưu/nhược một dòng, rồi chọn một.
- **Hệ quả** nêu cái giá phải trả và việc phát sinh (bảng mới, job dọn dẹp, test bắt buộc).
- Một DR một quyết định. Quyết định lớn có nhiều mảnh thì dùng danh sách con trong cùng DR, không tách ra năm DR vụn.

## 3. Danh sách soát khoảng trống

Đi qua SDD từng mục, với mỗi mục hỏi các câu dưới đây. Câu nào SDD chưa trả lời chính xác thì thành một DR. Không phải dự án nào cũng có đủ nhóm.

**Dữ liệu và nguồn**
- Nguồn dữ liệu cụ thể là gì (file, dataset, API, DB nào), license, kích thước, thống kê? Cần spike đo thật không?
- Schema của mọi nguồn và mọi bảng mà SDD chỉ nhắc tên. Business key / natural key của từng thực thể.
- Múi giờ, đồng hồ, ngày nghiệp vụ, giờ vượt 24h, chuyển giờ mùa hè.
- Dữ liệu tham chiếu có phiên bản không, đổi phiên bản thế nào (staging, swap)?
- Partition, retention, khối lượng ước tính, chỉ mục.
- PII: trường nào, loại bỏ ở đâu, không được đi tới đâu.

**Hợp đồng**
- Định dạng message, envelope, tên trường, `schema_version`, quy tắc tương thích ngược.
- Topic/queue, key, số partition, thứ tự cần giữ.
- Quy ước API: versioning, phân trang, lỗi (Problem Details), thời gian, idempotency của POST.
- Hợp đồng với hệ thống ngoài (SDK, quota, mã lỗi, timeout).

**Ngữ nghĩa đúng đắn**
- Bảo đảm giao nhận (at-most / at-least / effectively-once) và cơ chế cụ thể.
- Idempotency: khóa nào, guard thứ tự nào; insight/kết quả tính toán có idempotent khi chạy lại không (khóa theo event time hay giờ đồng hồ?).
- Ranh giới transaction: commit cái gì cùng nhau; offset/ack commit lúc nào.
- Chạy song song nhiều replica: khóa, fencing, job chạy trùng, khôi phục khi tiến trình chết giữa chừng.
- Máy trạng thái của mọi thực thể có trạng thái.
- Replay/backfill: nguồn nào, có bị cơ chế dedup chặn không.

**Lỗi**
- Phân loại lỗi (dữ liệu / hạ tầng tạm thời / nghiêm trọng) và hành vi cho từng loại.
- Retry, backoff, giới hạn, DLQ, skip limit, circuit breaker.

**Mâu thuẫn và thứ tự trong SDD**
- Quyền và tính năng mâu thuẫn (ví dụ: service chỉ có quyền đọc nhưng có endpoint ghi).
- Tính năng được hẹn ở phase sớm nhưng hạ tầng cần cho nó lại ở phase sau.
- Tuyên bố định lượng (NFR) chưa có cách đo, chưa có ground truth, chưa có baseline.
- Hai cơ chế không dùng được đồng thời.

**Thuật toán và nghiệp vụ**
- Định nghĩa chính xác, tham số và giá trị mặc định, edge case, cơ chế kích hoạt, chu kỳ.
- Ngưỡng nằm ở cấu hình nào; ai sở hữu quyết định (code hay mô hình AI).

**Nền tảng**
- Phiên bản ngôn ngữ, framework, thư viện (mặc định: bản ổn định mới nhất; 🔬 spike tương thích).
- Đơn vị triển khai: bao nhiêu app/image, app nào chạy profile nào, module nào là thư viện.
- Bố cục repo (monorepo?), build tool, kiến trúc code (layer, luật phụ thuộc).
- Identity provider, quản lý secret, TLS.
- Observability backend: metric, log, trace lưu ở đâu; kênh gửi alert.
- Ngân sách tài nguyên trên máy mục tiêu (RAM theo container); image còn được phát hành không; license.

**Frontend và UX** (nếu có UI)
- Stack, routing, state, cách lấy dữ liệu, real-time; bản đồ/biểu đồ; auth trong SPA; ngôn ngữ UI; cấu hình runtime.

**Vận hành, kiểm thử, thực nghiệm**
- Môi trường (local compose, k8s, cloud), cách deploy, CI runner đủ tài nguyên không.
- Backup, RPO/RTO. Runbook cho alert nào.
- Ground truth và baseline cho từng thực nghiệm; số lần lặp; máy chạy.
- Demo: kịch bản, dữ liệu gieo trước, phương án dự phòng.

**Quy trình**
- Ngôn ngữ tài liệu và code; nhánh git; quy ước commit; repo public/private; phạm vi (làm đủ hay cắt).

## 4. Nhóm và thứ tự

- Nhóm theo chủ đề, đặt chữ cái A, B, C…, thứ tự bám theo luồng của hệ thống (nguồn → mô hình dữ liệu → xử lý lõi → nghiệp vụ → AI → API → frontend → vận hành → triển khai/demo).
- Đánh số DR liên tục từ DR-01 theo thứ tự xuất hiện. DR thêm sau lấy số kế tiếp dù đặt ở nhóm nào.
- Thường được 40–70 DR cho một SDD cỡ 50–80 KB. Ít hơn 20 thường là soát chưa kỹ.

## 5. "Tổng hợp theo mức ảnh hưởng"

Gán mỗi DR vào phase đầu tiên mà nó chặn. DR chặn P1 (schema, contract, cấu trúc repo, phiên bản) và chặn P2 (ngữ nghĩa lõi) phải xong trước khi code. Bảng này là đầu vào cho việc P0-01 của master plan.
