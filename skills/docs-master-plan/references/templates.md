# Template

A.1–A.7 được chép vào phụ lục A của master plan. B.x là khung cho các tài liệu còn lại, dùng khi viết docs.

## A.1 ADR (MADR rút gọn)

```markdown
# ADR-XXXX: <Tiêu đề nói rõ quyết định>

- Trạng thái: Proposed | Accepted | Superseded by ADR-YYYY
- Ngày: YYYY-MM-DD · Liên quan: DR-xx, DOC-xx, FR-xx, NFR-xx

## Bối cảnh
<Vấn đề, ràng buộc, vì sao phải quyết định bây giờ. Dẫn SDD/DR.>

## Các phương án
1. **<Tên>.** <Mô tả một câu> — ưu / nhược.
2. …

## Quyết định
Chọn **phương án N**.
- <Chi tiết cụ thể: cơ chế, cấu hình, ranh giới.>

## Hệ quả
**Tích cực**
- …

**Tiêu cực**
- …

**Việc phát sinh**
- …
```

## A.2 Use case

```markdown
## UC-XX · <Tên>

- **Actor:** <chính> (role), <phụ>
- **Trigger:** …
- **Tiền điều kiện:** …
- **Luồng chính:**
  1. …
  2. …
- **Luồng thay thế:**
  - 2a. …
- **Luồng lỗi:**
  - E1. … → <hành vi, chuỗi UI "…">
- **Hậu điều kiện:** …
- **Quy tắc:** …
- **Liên quan:** FR-…; màn hình `screens/<x>.md`; endpoint E-…; sự kiện …
```

## A.3 Yêu cầu có tiêu chí nghiệm thu

Dạng bảng (mặc định, gọn):

```markdown
### FR-02 · <Nhóm yêu cầu>

| ID | Yêu cầu | Tiêu chí nghiệm thu | Ưu tiên | Kiểm chứng |
| --- | --- | --- | --- | --- |
| FR-02.2 | Vi phạm validation thì vào DLQ với `stage=SCHEMA` | **G** chunk 500 record, record #37 thiếu `vehicle_id` **T** 499 dòng được ghi; 1 dòng DLQ `SCHEMA` nêu tên trường; offset commit tới cuối chunk | M | Unit test, EXP-03 |
```

Dạng đầy đủ (khi một yêu cầu cần nhiều kịch bản):

```markdown
### FR-02.1 <Tên>
Ưu tiên: Must · Nguồn: SDD 3.2 · UC: UC-08
- Given …
- When …
- Then …
- And …
Kiểm chứng: P2-03 unit test, EXP-03
```

NFR:

```markdown
| ID | Yêu cầu | Chỉ tiêu | Cách đo | Kiểm chứng |
| --- | --- | --- | --- | --- |
| NFR-03 | Độ trễ dữ liệu | p95 < 10 giây ở tải nền | Histogram tại API | EXP-05 |
```

## A.4 Endpoint API

```markdown
### E-xx `GET /stops/{stopId}/arrivals` · `listStopArrivals`

- **Mục đích / UC:** …
- **Quyền:** anonymous (rate limit 60/phút/IP)
- **Tham số:**

  | Tên | Vị trí | Kiểu | Bắt buộc | Mặc định | Ràng buộc |
  | --- | --- | --- | --- | --- | --- |

- **Response 200:** schema + ví dụ JSON đầy đủ
- **Lỗi:** 404 `stop-not-found`, 400 `invalid-param` (Problem Details)
- **Nguồn dữ liệu:** bảng/view, câu truy vấn chính, index dùng
- **Cache:** TTL, key
- **Hiệu năng:** p95 < … ms
- **Sự kiện real-time liên quan:** …
```

## A.5 Đặc tả màn hình

```markdown
# Màn hình: <Tên>

> Trạng thái: … · DOC-xx
> Phụ thuộc: …
> Người dùng chính: Px-xx

## 1. Persona, use case, quyền
## 2. URL và search params
## 3. Wireframe            (ASCII, desktop và mobile nếu có)
## 4. Vùng và component    (tham chiếu design-system)
## 5. Dữ liệu              (endpoint E-xx · kênh real-time · tần suất refetch)
## 6. Tương tác            (hành động → kết quả → lỗi)
## 7. Trạng thái           (loading · empty · error · stale · không có quyền)
## 8. Microcopy
## 9. Tiêu chí nghiệm thu  (Given/When/Then, có mã)
## 10. Ca kiểm thử E2E
## 11. Câu hỏi còn mở
```

## A.6 Protocol thực nghiệm

```markdown
# EXP-XX: <Tên nói rõ tuyên bố được kiểm>

> Trạng thái: … · DOC-xx / EXP-XX
> Phụ thuộc: [protocol chung](README.md), …
> Người dùng chính: Px-xx; chương đánh giá của báo cáo

## 1. Giả thuyết        (H1 (NFR-xx): … đo được bằng …)
## 2. Biến              (độc lập · phụ thuộc · kiểm soát)
## 3. Baseline
## 4. Môi trường        (máy, môi trường chạy, phiên bản git)
## 5. Các bước          (lệnh tự động)
## 6. Chỉ số và công thức
## 7. Tiêu chí đạt
## 8. Phân tích         (script, biểu đồ)
## 9. Mẫu bảng kết quả
## 10. Mối đe dọa tới tính hợp lệ
## 11. Kết quả          (để trống tới khi chạy)
## 12. Câu hỏi còn mở
```

## A.7 Runbook

```markdown
# RB-XX: <Tên alert hoặc thao tác>

> Trạng thái: … · DOC-xx / RB-XX
>
> Alert: `AlertName` (severity, for) · Dashboard: … · Liên quan: DOC-xx §n

## Triệu chứng và ảnh hưởng
## Kiểm tra             (câu lệnh, truy vấn metric, SQL — chạy được nguyên văn)
## Xử lý                (bước 1, 2, 3)
## Trên <môi trường khác> (nếu khác)
## Xác nhận đã xong
## Phòng ngừa và việc sau sự cố
```

---

## B.1 Tài liệu thiết kế (nhóm 06-design)

```markdown
# <Tên thành phần>

> Trạng thái: **Draft** · Cập nhật: YYYY-MM-DD · DOC-xx
> Phụ thuộc: …
> Người dùng chính: <app/module>, Pn-xx…

<Tài liệu mô tả gì; phần nào thuộc tài liệu khác.>

## 1. Mục đích và phạm vi      (bảng thành phần: lớp chính · chạy ở · kích hoạt · đọc · ghi · việc)
## 2. Thành phần và interface  (chữ ký code thật)
## 3. Thuật toán               (pseudo-code đánh số bước)
## 4. Transaction và đồng thời (cái gì commit cùng nhau; khóa; replica)
## 5. Cấu hình                 (Key · Kiểu · Mặc định · Mô tả)
## 6. Metrics và log           (Metric · Loại · Label; alert liên quan)
## 7. Lỗi và cách xử lý        (Tình huống · Hành vi)
## 8. Test bắt buộc            (ID · Kịch bản · Kỳ vọng — tiền tố riêng của tài liệu)
## 9. Câu hỏi còn mở           ("Không có." khi Approved)
```

Thêm mục riêng theo nội dung (máy trạng thái, định dạng file, tương tác với luồng khác) giữa §3 và §5.

## B.2 Persona

```markdown
| ID | Persona | Role trong hệ thống | Thiết bị chính | Mức kỹ thuật | Tần suất dùng |
| --- | --- | --- | --- | --- | --- |

### PS-1 · <Vai trò>: "<Tên minh họa>, <bối cảnh một dòng>"

- **Mục tiêu:** …
- **Nỗi đau:** …
- **Cần từ <hệ thống>:** …
- **Không cần:** …
- **Màn hình:** …
```

Journey: bảng `Bước · Hành động · Điểm chạm (màn hình/endpoint) · Cảm xúc · Cơ hội`.

## B.3 Tính năng

```markdown
| ID | Tính năng | Mô tả | FR | UC | Phase | MoSCoW | Cờ | Phụ thuộc | Cắt ở bước |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
```

## B.4 Glossary

```markdown
## 1. <Nhóm thuật ngữ>

| Thuật ngữ | Tiếng Việt | Định nghĩa | Liên quan |
| --- | --- | --- | --- |
| feed version | phiên bản feed | Một feed đã nạp, định danh bằng … Chỉ một phiên bản `ACTIVE` | DR-10, DOC-21 |
```

## B.5 Bảng dữ liệu (nhóm 05-data)

````markdown
### 5.3 `fact_vehicle_position`

- **Grain:** một dòng cho mỗi (xe, thời điểm event).
- **Business key:** `(vehicle_id, event_timestamp, service_date)`.
- **Ghi bởi:** `etl` (DOC-20). **Đọc bởi:** `api`, `analytics`.

```sql
CREATE TABLE … ;
CREATE INDEX … ;  -- lý do: truy vấn X ở DOC-32 E-05
```

**Upsert mẫu:**

```sql
INSERT … ON CONFLICT (…) DO UPDATE SET … WHERE excluded.event_timestamp > t.event_timestamp;
```
````

## B.6 `docs/README.md`

```markdown
# Tài liệu dự án: <Tên>

Tài liệu thiết kế gốc: [`../<sdd>.md`](../<sdd>.md) (gọi tắt là **SDD gốc**).

## Bắt đầu từ đây

1. [00-master-plan.md](00-master-plan.md): kế hoạch tổng. …
2. [00-decision-register.md](00-decision-register.md): sổ quyết định. …

## Tài liệu

| DOC | Tài liệu | Trạng thái |
| --- | --- | --- |
| DOC-01 | [Tầm nhìn và phạm vi](01-product/vision-and-scope.md) | Chưa viết |

## Cấu trúc

| Thư mục | Nội dung |
| --- | --- |

## Quy ước

- Dòng đầu mỗi file ghi trạng thái (`Draft | Review | Approved | Superseded`) và ngày cập nhật.
- Sơ đồ vẽ bằng Mermaid.
- Mã định danh dùng thống nhất như quy định ở mục 0 của master plan.
- Đổi hành vi thì sửa tài liệu trong cùng PR. Đổi quyết định thì viết ADR mới thay thế ADR cũ.
```
