---
name: docs-project
description: Viết, duyệt và theo dõi bộ tài liệu dự án (DOC-xx, ADR, runbook, thực nghiệm, đặc tả màn hình…) theo master plan đã lập bằng skill docs-master-plan. Mỗi tài liệu bám đúng "nội dung bắt buộc" và gate trong master plan §3.2, dùng quyết định trong docs/00-decision-register.md, ghi quyết định mới thành DR. Dùng khi người dùng muốn "viết DOC-xx", "viết docs cho gate P1", "viết tài liệu tiếp theo", "duyệt tài liệu", "kiểm tra docs", "trạng thái docs".
argument-hint: "<DOC-xx …> | gate <Pn> | next | review <DOC-xx|all> | status"
license: MIT
---

# Viết docs theo master plan

Điều kiện: đã có `docs/00-master-plan.md` và `docs/00-decision-register.md` (do skill `docs-master-plan` tạo). Chưa có thì dừng và đề nghị chạy `/docs-master-plan <sdd.md>` trước.

Thứ tự ưu tiên khi các nguồn lệch nhau: **master plan** (nội dung bắt buộc, gate, mã) → **sổ quyết định** (DR đã Chốt) → **SDD gốc** → tham chiếu của skill này.

Tham chiếu:

- [references/conventions.md](references/conventions.md): mã, khối đầu file, trạng thái, quyết định, ngôn ngữ, văn phong, một nguồn sự thật. Đọc trước khi viết tài liệu đầu tiên của phiên.
- [references/doc-guide.md](references/doc-guide.md): tài liệu tốt trông thế nào theo từng loại.
- [references/templates.md](references/templates.md): khung tài liệu (A.x giống phụ lục A của plan, B.x cho các loại còn lại).
- `scripts/check_docs.py [docs_dir] [--strict]`: kiểm tra mã định danh, link, khối trạng thái, câu hỏi còn mở. Cần Python 3.10+. `<skill-dir>` trong các lệnh là thư mục chứa file SKILL.md này.

## Chế độ

| Lệnh | Việc |
| --- | --- |
| `/docs-project DOC-06 DOC-03` | Viết các tài liệu được nêu, theo thứ tự |
| `/docs-project gate P1` | Viết mọi tài liệu và ADR có gate P1 chưa có, theo thứ tự phụ thuộc |
| `/docs-project next` | Viết tài liệu kế tiếp theo các việc "Viết DOC-…" của Phase 0 và §9 của plan |
| `/docs-project review <DOC-xx\|all>` | Duyệt theo định nghĩa Approved, không sửa trạng thái |
| `/docs-project status` | Bảng DOC × gate × trạng thái, tài liệu đang chặn gate kế tiếp |

## Viết một tài liệu

### 1. Thu thập đầu vào

- Hàng của DOC trong master plan §3.2: chép "Nội dung bắt buộc" thành checklist. Đây là định nghĩa của "đủ".
- Các DR có `Ghi vào:` nhắc tới DOC này (`grep -n "DOC-xx" docs/00-decision-register.md`), và DR mà nội dung bắt buộc nêu tên. Đọc toàn văn từng DR.
- Các mục SDD gốc liên quan.
- Tài liệu đã có mà DOC này phụ thuộc. Glossary luôn đọc.
- Các việc `Pn-xx` trỏ tới DOC này: chúng cho biết người đọc sẽ làm gì với tài liệu.

**Definition of Ready:** DR liên quan còn ở `Đề xuất` thì báo người dùng. Được đồng ý thì viết theo đề xuất và giữ tài liệu ở `Draft`.

### 2. Dàn ý

Từ checklist và khung trong templates.md / doc-guide.md, lập danh sách mục. Mỗi ý bắt buộc phải nằm ở một mục cụ thể. Tài liệu lớn (danh mục endpoint, thiết kế lõi): ghi khung trước, rồi viết từng mục bằng Edit.

### 3. Viết

- Khối đầu file đúng conventions.md §2, trạng thái `Draft` trong lúc viết.
- Cụ thể, có ví dụ, có số liệu, dẫn nguồn `(DR-xx)`, `(SDD §x)`, `(DOC-yy §z)`.
- Mã mới (FR con, E-xx, DQ-xx, tiền tố test…) cấp theo conventions.md §1; tiền tố test mới phải chưa bị dùng (`grep -rn "| <X>-01" docs/`).

### 4. Quyết định phát sinh

Gặp lựa chọn mà SDD và DR chưa trả lời:

- Owner đã ủy quyền (Nhật ký chốt có ghi, hoặc người dùng nói vậy): thêm DR mới với số kế tiếp, trạng thái `Chốt`, người chốt `Claude (Owner ủy quyền)`, thêm dòng vào Nhật ký chốt, `Ghi vào` gồm DOC đang viết. Quyết định ở cấp kiến trúc thì viết thêm ADR và cập nhật `04-adr/README.md` và bảng ADR của plan.
- Chưa ủy quyền: thêm DR `Đề xuất`, ghi câu hỏi vào "Câu hỏi còn mở" kèm mã DR; tài liệu dừng ở `Draft`.
- Quyết định làm thay đổi tài liệu đã Approved: sửa tài liệu đó trong cùng lần, ghi `*Sửa YYYY-MM-DD (DR-xx):* …` tại chỗ sửa và cập nhật ngày ở khối đầu.

### 5. Lan sang tài liệu nguồn

- Thuật ngữ mới → glossary.
- Key cấu hình mới → configuration-reference; metric/alert mới → observability (nếu các tài liệu này đã có; chưa có thì liệt kê trong báo cáo để thêm khi viết chúng).
- Mã test mới → bảng chỉ mục tiền tố của test-strategy (nếu đã có).

### 6. Hoàn tất

- Đánh dấu checklist: ý nào ở mục nào. Thiếu thì viết tiếp, không bỏ qua.
- Trạng thái → `Review` (chỉ `Approved` khi Owner duyệt hoặc đã ủy quyền duyệt).
- Cập nhật bảng trạng thái trong `docs/README.md` và ghi chú tiến độ ở việc tương ứng của master plan (ví dụ `P0-09 Viết DOC-01…05 — **Review 2026-10-06**`).
- Chạy `python3 <skill-dir>/scripts/check_docs.py docs`; sửa mọi E1/E2 do tài liệu mới gây ra. E1 trỏ tới tài liệu chưa viết là bình thường trong lúc làm theo gate; nêu trong báo cáo.
- Báo cáo ngắn: tài liệu đã viết, DR mới (số, tiêu đề, đã chốt hay đề xuất), câu hỏi còn mở, việc cần lan sang tài liệu chưa có.

Không commit trừ khi người dùng yêu cầu.

## Viết nhiều tài liệu (gate)

- Thứ tự: glossary → product (vision → personas → requirements → use cases → feature catalog) → kiến trúc → ADR → data → thiết kế → API → UX/UI → operations → testing. Bên trong một gate, tài liệu bị phụ thuộc viết trước.
- Glossary và requirements luôn do tác tử chính viết. Sau khi chúng có, các tài liệu **độc lập nhau** trong cùng gate có thể giao song song cho subagent (fork, tối đa 4–5 cùng lúc). Mỗi subagent:
  - chỉ ghi file tài liệu của nó;
  - **không** sửa sổ quyết định, glossary, README, master plan, configuration-reference, observability;
  - quyết định mới ghi tạm là `DR-NEW-<tên-tài-liệu>-<n>` trong tài liệu, và trả về: danh sách DR đề xuất (đầy đủ Vấn đề/Quyết định/Hệ quả), thuật ngữ mới, key cấu hình mới, metric mới, mã test đã dùng.
- Tác tử chính gộp kết quả: cấp số DR thật theo thứ tự và thay mọi `DR-NEW-…`, cập nhật glossary và các tài liệu nguồn, rồi đọc chéo để thống nhất tên bảng, key, mã E-xx giữa các tài liệu (`grep` các tên chính). Cuối cùng chạy check_docs.py.

## Duyệt (`review`)

Với từng tài liệu, kiểm năm điều của định nghĩa Approved (conventions.md §3):

1. So từng ý trong "Nội dung bắt buộc" của plan với mục trong tài liệu; liệt kê ý thiếu.
2. "Câu hỏi còn mở" rỗng, hoặc mỗi câu có DR đã Chốt.
3. Thuật ngữ chuyên môn dùng trong tài liệu có trong glossary; mã trỏ tới mục có thật (check_docs.py).
4. Khối đầu có đủ phụ thuộc.
5. Chỗ có thể hiểu theo hai cách có ví dụ cụ thể.

Thêm: mâu thuẫn với DR đã Chốt hoặc với tài liệu khác (tên bảng, key, ngưỡng, mã lỗi); key/metric chưa có trong tài liệu nguồn. Báo cáo dạng danh sách `DOC-xx §n: vấn đề → cách sửa`. Không đổi trạng thái; khi Owner duyệt mới chuyển `Approved`, cập nhật README, việc doc gate `Pn-00` của plan, và Nhật ký chốt nếu duyệt gộp.

## Trạng thái (`status`)

Đọc §3.1–3.2 của plan, khối đầu mọi file trong `docs/`, chạy check_docs.py. In bảng `DOC · Tài liệu · Gate · Trạng thái`, rồi gate kế tiếp và các DOC/ADR đang chặn nó.
