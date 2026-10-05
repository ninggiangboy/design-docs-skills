# Văn phong và các mẫu trình bày

## 1. Văn phong

- Viết bằng ngôn ngữ người dùng chọn (mặc định tiếng Việt). Thuật ngữ kỹ thuật giữ tiếng Anh khi tiếng Việt gượng (reservation, webhook, consumer lag); tên trong code, bảng, cột, endpoint, cấu hình đặt trong backtick.
- Câu ngắn, chủ động, khẳng định. Không rào đón ("có thể cân nhắc", "nên xem xét"), không quảng cáo ("mạnh mẽ", "tối ưu"), không câu đệm.
- **Mỗi khẳng định có lý do hoặc hệ quả đi kèm.** "`SKIP LOCKED` không bao giờ chờ lock, nên không có deadlock và người thua trả về ngay."
- **Con số cụ thể** thay cho tính từ: 10 phút, 3 link mỗi email trong 15 phút, p95 dưới 500 ms, 20.000 ghế. Số định dạng kiểu Việt (`100.000`, `2,5 giây`).
- **Nói rõ cái không làm** và vì sao: "Không dùng Jev cho bunching, ETA…: đó là phép thống kê thuần; dùng mô hình chỉ làm chậm, tốn chi phí và khó kiểm chứng hơn."
- Đầu mỗi mục cấp 2 (và các mục cấp 3 quan trọng) là **một câu nêu quy tắc chi phối**, trước mọi chi tiết.
- Danh sách có tiêu đề in đậm: `- **Tên ý.** Giải thích.` hoặc `- **Tên ý** — giải thích.` Chọn một kiểu và giữ trong cả tài liệu.
- Tham chiếu nội bộ viết `mục 8.4`, `(mục 10.3)`. Tham chiếu yêu cầu viết mã: `NFR-03`, `EXP-10`. Không dùng mã DR/ADR/DOC trong SDD mới; các mã đó thuộc bộ docs sinh sau.
- Nguồn bên ngoài (bài viết kỹ thuật, tài liệu chuẩn) dẫn bằng link Markdown ngay tại câu dùng nó.
- Không dùng emoji. Không viết hoa cả câu, trừ bất biến được tách riêng để nhấn mạnh (`NEVER OVERSELL`).

## 2. Sơ đồ Mermaid

- Mọi sơ đồ dùng Mermaid để render trên GitHub/VS Code. Sơ đồ ASCII chỉ dùng cho luồng xử lý dạng pipeline ngắn hoặc bản chữ của hình.
- **Nhãn node luôn đặt trong ngoặc kép**: `A["Giữ vé (SKIP LOCKED)"]`. Nhãn không ngoặc mà chứa `()[]{}` sẽ làm sơ đồ hỏng.
- Nhãn cạnh cũng trong ngoặc kép: `A -- "webhook" --> B`, `A -. "chỉ để giảm tải" .-> B`.
- Nhãn bằng ngôn ngữ của tài liệu, ngắn, nói vai trò chứ không chỉ tên.
- Chọn loại theo nội dung:

  | Nội dung | Loại |
  | --- | --- |
  | Kiến trúc, thành phần | `flowchart TD` với `subgraph` |
  | Luồng nghiệp vụ có quyết định | `flowchart TD` với node `{"…?"}` và cạnh `-- Có -->` / `-- Không -->` |
  | Tương tác theo thời gian, tranh chấp, retry | `sequenceDiagram` với `par`, `alt`/`else`, `loop`, `Note over`, `autonumber`; mũi tên thất lạc `--x` |
  | Vòng đời thực thể | `stateDiagram-v2`, nhãn chuyển là sự kiện kích hoạt; `note right of` cho trạng thái trung gian |
  | Mô hình dữ liệu | `erDiagram` với nhãn quan hệ tiếng Việt |
  | Use case | `flowchart LR`, actor `(["…"])`, UC nhóm bằng `subgraph` |
  | Kế hoạch | `flowchart LR`, cạnh nét đứt tới "Để sau" |

- Mỗi sơ đồ đi kèm ít nhất một câu nói người đọc cần thấy gì trong đó. Sơ đồ không thay cho bảng quy tắc: vòng đời luôn có cả `stateDiagram` lẫn bảng chuyển trạng thái.

## 3. Các mẫu dùng lại

### Bảng bất biến

```markdown
| Đối tượng | Bất biến | Được ép bằng |
| --- | --- | --- |
| Reservation | Rời trạng thái `ACTIVE` đúng một lần | `UPDATE … WHERE status = 'ACTIVE'` |
```

### Câu ghi có điều kiện kèm giải thích

````markdown
```sql
UPDATE login_token SET used_at = now()
WHERE token_hash = :hash AND used_at IS NULL AND expires_at > now();
```

Đúng một request thắng: request đến sau thấy `used_at` đã khác NULL và cập nhật 0 dòng.
````

Comment trong SQL nói cách đọc kết quả: `-- Số dòng cập nhật phải bằng :qty. Ít hơn: ROLLBACK và trả 409.`

### Tranh chấp giữa hai luồng

1. Câu nêu **ai là trọng tài** ("dòng `reservation` là trọng tài duy nhất").
2. Các bước đánh số của từng luồng, gồm cả nhánh lỗi và timeout.
3. `sequenceDiagram` với `alt` cho từng kết quả.
4. Đoạn cuối giải thích vì sao không còn khe hở, và lưới an toàn cuối cùng nằm ở mục nào.

### Phân tích phương án

```markdown
### 10.3 <Vấn đề>: các phương án và lý do chọn

Hệ thống chọn phương án D: … Ba phương án A, B, C dưới đây đã được xem xét; phần này ghi lại ưu nhược điểm và vì sao bị loại.

**Bài toán.** <Mô tả cái khó bằng một hai câu, kèm sơ đồ nếu giúp thấy vấn đề.>

#### Phương án A: <tên>
<Cách làm, kèm code nếu cần.>
- **Ưu điểm**: …
- **Nhược điểm**: …
- **Kết luận**: …

#### Phương án D: <tên> (chọn)
…

#### So sánh và lý do chọn

| Phương án | <Tiêu chí 1> | <Tiêu chí 2> | Độ phức tạp | Kết luận |
| --- | --- | --- | --- | --- |

1. **<Yêu cầu số một loại phương án nào trước>.**
2. **<Trong số còn lại, chỉ phương án nào giải quyết gốc rễ>.**
3. **<Cái giá của phương án chọn nhỏ trong bài toán này vì…>.**
4. **Lựa chọn được kiểm chứng bằng số đo**: EXP-xx.
```

Phương án bị loại mà vẫn đúng thì giữ làm **baseline** cho thực nghiệm.

### Bảng tham số

```markdown
**Tham số** (cấu hình theo sự kiện; giá trị là mặc định đề xuất, hiệu chỉnh ở EXP-05)

| Tham số | Mặc định | Ý nghĩa |
| --- | --- | --- |
| `max_active` | 500 người | Số người tối đa ở trong khu đặt vé cùng lúc |
```

Kèm một ví dụ tính nhẩm cho thấy các tham số tương tác thế nào.

### Bảng sự cố

```markdown
| Sự cố | Phát hiện | Hành vi hệ thống | Phục hồi |
| --- | --- | --- | --- |
| PostgreSQL không khả dụng | Lỗi kết nối | Mọi thao tác ghi trả 503 | Tự tiếp tục khi database trở lại |
```

Có câu nguyên tắc trước bảng: khi lỗi, hệ thống nghiêng về phía nào.

### Thực nghiệm

```markdown
| Mã | Thực nghiệm | Cách làm | Chỉ số | Kỳ vọng |
| --- | --- | --- | --- | --- |
| EXP-01 | Tranh một ghế | 10.000 request đồng thời giữ ghế A1 | Số lượt giữ thành công; số ghế có hai chủ | Đúng 1 thành công; 0 ghế trùng |
```

Kỳ vọng có số. Thực nghiệm khám phá thì ghi "Báo cáo so sánh, không đặt kỳ vọng trước".

### Hình giao diện kèm bản chữ

````markdown
&#91;embedded content: <mô tả hình>\]

<Một câu chú thích: hình đang cho thấy trạng thái gì.>

Bản chữ của hình trên, dùng khi xuất Markdown (`>` là mục đang chọn):

```
+-----------------------------+
| ASCII khong dau, rong <= 90 |
+-----------------------------+
```
````

### Công thức

Viết trong code block `latex`, sau đó giải thích bằng lời từng trường hợp (N = 1, đường cong, …).

## 4. Độ dài tham khảo

| Phần | PTI (đồ án) | Đặt vé (sản phẩm) |
| --- | --- | --- |
| Tổng | ~790 dòng, 15 mục | ~1.620 dòng, 17 mục, 28 sơ đồ |
| Mục lõi | ETL: ~60 dòng + bảng | Kho vé: ~200 dòng; chịu tải: ~280 dòng |
| Mục "mức cơ bản" | 5–15 dòng | 5–15 dòng |

Độ dài theo mức đầu tư ở 2.2, không chia đều.
