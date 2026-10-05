# Quy ước chung của bộ tài liệu

Dùng chung cho master plan, sổ quyết định và mọi tài liệu trong `docs/`. Master plan chép phần cốt lõi của file này vào §0, §7 và phụ lục A, nên sau khi plan đã có thì **plan là nguồn sự thật**. Lệch nhau thì sửa theo plan.

## 1. Mã định danh

Mỗi tiền tố chỉ mang một nghĩa trong toàn dự án. Trước khi đặt tiền tố mới (mã test của một tài liệu, mã việc của một phase đặc biệt), kiểm tra nó chưa được dùng. Ví dụ đã gặp: phase refactor dùng `RF-xx` vì `R-xx` đã là mã test replay.

| Tiền tố | Ý nghĩa | Nơi định nghĩa |
| --- | --- | --- |
| `FR-xx` / `FR-xx.y` | Yêu cầu chức năng / yêu cầu con | requirements |
| `NFR-xx` | Yêu cầu phi chức năng | requirements |
| `UC-xx` | Use case | use-cases |
| `PS-x`, `J-x` | Persona, journey | personas-and-journeys |
| `F-<NHÓM>-xx` | Tính năng | feature-catalog |
| `BR-xx` | Quy tắc nghiệp vụ (nếu cần đánh số) | use-cases |
| `DOC-xx` | Tài liệu | master plan §3.1 |
| `ADR-xxxx` | Quyết định kiến trúc | `04-adr/NNNN-*.md` |
| `DR-xx` | Mục trong sổ quyết định | 00-decision-register |
| `Pn-xx` | Việc thuộc phase n; `Pn-00` luôn là doc gate | master plan §5 |
| `Mn` | Milestone kết thúc phase n | master plan §4 |
| `S-xx` | Spike (thử nghiệm ≤ 1–2 ngày) | master plan Phase 0 |
| `E-xx` | Endpoint API | api-endpoints |
| `DQ-xx` | Rule chất lượng dữ liệu | data-quality-rules |
| `EXP-xx` | Thực nghiệm | experiments/ |
| `RB-xx` | Runbook | runbooks/ |
| `<X>-xx` | Ca test bắt buộc của một tài liệu (mỗi tài liệu một tiền tố riêng, ví dụ `B-`, `R-`, `G-`) | mục "Test bắt buộc" của tài liệu đó; test-strategy có bảng chỉ mục tiền tố |

Quy tắc:

- Số đã cấp thì không đổi, không tái dùng. Mục bị bỏ thì gạch (`~~…~~`) và ghi lý do, không xóa số.
- Mục mới nối vào cuối dãy (`DR-105`, `DOC-49`), kể cả khi về nội dung nó thuộc nhóm ở giữa.
- Dãy được viết gọn: `FR-01…12`, `DOC-07…11`, `DR-21–24`, `P5-06…13`.
- Trỏ tới mục con của tài liệu: `DOC-19 §4.3`. Trỏ tới SDD: `SDD gốc §6.2` (hoặc `SDD 6.2`).

## 2. Khối đầu file

Tài liệu thường:

```markdown
# <Tên tài liệu>

> Trạng thái: **Draft** · Cập nhật: YYYY-MM-DD · DOC-xx
> Phụ thuộc: SDD gốc §x, [DR](../00-decision-register.md) (DR-05, 20), [DOC-yy](../03-architecture/x.md) §2
> Người dùng chính: <ai/việc nào đọc tài liệu này: app, Pn-xx, tài liệu khác>

<1–3 câu: tài liệu nói về cái gì, cái gì KHÔNG nằm ở đây và nằm ở đâu.>
```

Khi cập nhật vì một quyết định, ghi lý do sau ngày: `Cập nhật: 2026-09-30 (DR-104: bố cục Clean Architecture)`.

ADR:

```markdown
# ADR-0003: <Tiêu đề nói rõ quyết định>

- Trạng thái: Accepted
- Ngày: YYYY-MM-DD · Liên quan: DR-13, FR-03, NFR-01, EXP-01
```

Runbook: dòng thứ hai ghi `Alert: \`AlertName\` (severity, for) · Dashboard: … · Liên quan: …`. Thực nghiệm: `DOC-45 / EXP-01`.

## 3. Trạng thái

| Loại | Vòng đời |
| --- | --- |
| Tài liệu | `Draft` → `Review` → `Approved` → `Superseded` |
| ADR | `Proposed` → `Accepted` → `Superseded by ADR-yyyy` |
| DR | `Đề xuất` → `Chốt` hoặc `Đổi` (ghi phương án thay thế) |
| Việc trong plan | trống → `**Xong YYYY-MM-DD** (\`sha\`)`; hoãn/cắt thì ghi lý do |

**Approved** khi đủ cả năm điều:

1. Có đủ các mục bắt buộc ở master plan §3.2.
2. Mục "Câu hỏi còn mở" rỗng ("Không có."), hoặc mỗi câu đã thành DR ở trạng thái Chốt.
3. Mọi thuật ngữ đã có trong glossary; mọi mã (FR, UC, DR, E…) trỏ tới mục có thật.
4. Các tài liệu phụ thuộc được liệt kê ở khối đầu file.
5. Có ví dụ cụ thể (payload, SQL, bảng test) ở mọi chỗ có thể hiểu theo hai cách.

Chỉ Owner chuyển sang Approved, trừ khi Owner đã ủy quyền.

## 4. Quyết định

- Mọi lựa chọn chưa có trong SDD gốc là một **DR**. Không ra quyết định ngầm trong thân tài liệu.
- DR mới: số kế tiếp, đặt trong nhóm chủ đề phù hợp, thêm một dòng vào "Nhật ký chốt" (ngày, người chốt, nội dung, mục bị ảnh hưởng). Người chốt là `Owner`, hoặc `Claude (Owner ủy quyền)` khi Owner đã giao quyền.
- Mỗi DR có dòng **Ghi vào:** liệt kê tài liệu đích. DR ở cấp kiến trúc (khó đảo ngược, ảnh hưởng nhiều module) thì thành ADR.
- Sửa một quyết định đã chốt: không viết đè. Thêm dòng `*Sửa YYYY-MM-DD (DR-yy):* …` ngay trong mục cũ, sửa các tài liệu đích trong cùng lần. ADR không sửa nội dung; viết ADR mới và đánh dấu ADR cũ `Superseded by`.
- Chỗ khác SDD gốc đánh dấu **⚠ lệch SDD gốc** và nêu lý do. Không sửa file SDD gốc.
- Chỗ cần thử mới chốt được đánh dấu **🔬 spike** và có việc `S-xx` ở Phase 0.

## 5. Ngôn ngữ

Mặc định (đổi được khi Owner chốt khác, ghi thành một DR):

- `docs/` viết bằng ngôn ngữ của SDD gốc (thường là tiếng Việt).
- Mọi thứ khác bằng tiếng Anh: code, comment, log, thông báo lỗi API, metric, UI, commit, PR, tên test.
- Thuật ngữ kỹ thuật giữ nguyên tiếng Anh nếu tiếng Việt gượng; tên trong code đặt trong backtick.
- Chuỗi hiện thật trên UI viết trong ngoặc kép bằng tiếng Anh: "Live data is delayed".

## 6. Văn phong

- Câu ngắn, chủ động, một ý một câu. Không quảng cáo, không rào đón, không "có thể cân nhắc".
- Viết đủ để **làm được mà không phải hỏi thêm**: tên bảng, cột, key cấu hình, giá trị mặc định, đơn vị, ngưỡng, mã lỗi.
- Mỗi khẳng định thiết kế dẫn nguồn trong ngoặc: `(DR-21)`, `(SDD 6.3)`, `(DOC-14 §5)`.
- Bảng cho danh mục và so sánh; danh sách đánh số cho trình tự; văn xuôi cho lý do.
- Sơ đồ bằng Mermaid (flowchart, sequenceDiagram, stateDiagram-v2, erDiagram) để render được trên GitHub.
- Ví dụ thật thay cho mô tả trừu tượng: JSON đầy đủ trường, câu SQL chạy được, bảng test có dữ liệu vào và kết quả kỳ vọng.
- Không mô tả lại framework hay chuẩn; chỉ nói dự án dùng nó thế nào và cấu hình gì.
- Mỗi tài liệu nói rõ ranh giới: phần nào thuộc tài liệu khác, tài liệu nào.
- Số liệu ghi rõ là **kế hoạch** hay **đo được** (kèm ngày, máy, script đo).
- Định dạng số theo ngôn ngữ tài liệu (tiếng Việt: `1.233`, `2,5 s`).

## 7. Một nguồn sự thật

| Thứ | Chỉ định nghĩa ở | Nơi khác thì |
| --- | --- | --- |
| Thuật ngữ | glossary | dùng đúng từ, không định nghĩa lại |
| Key cấu hình, biến môi trường | configuration-reference | bảng con trong tài liệu thiết kế được phép, nhưng phải khớp |
| Metric, alert | observability | trỏ tới |
| Bảng, cột, DDL | tài liệu nhóm data | trỏ tới `DOC-xx §n` |
| Endpoint | api-endpoints (`E-xx`) | trỏ bằng mã `E-xx` |
| Topic, message, schema | messaging-contracts | trỏ tới |
| Quyết định | DR / ADR | trỏ tới, không giải thích lại dài |

Thêm một key cấu hình, metric hay thuật ngữ ở bất kỳ đâu thì cập nhật tài liệu nguồn của nó trong cùng lần sửa.

## 8. Cấu trúc thư mục

- `docs/README.md`: mục lục, thứ tự đọc, bảng trạng thái DOC, quy ước rút gọn.
- `docs/00-master-plan.md`, `docs/00-decision-register.md`.
- Thư mục đánh số theo nhóm: `01-product/`, `02-glossary.md`, `03-architecture/`, `04-adr/`, `05-data/`, `06-design/`, `07-api/`, `08-ux-ui/`, `09-operations/`, `10-testing/`, `11-report/`. Nhóm không áp dụng thì bỏ, không đánh lại số.
- Tên file tiếng Anh, kebab-case. ADR: `NNNN-kebab-title.md`. Runbook: `RB-xx-kebab.md`. Thực nghiệm: `EXP-xx-kebab.md`.
- File SDD gốc nằm ở gốc repo, được gọi là **SDD gốc**.
