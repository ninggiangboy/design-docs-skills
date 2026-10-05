---
name: docs-master-plan
description: Từ một file SDD (tài liệu thiết kế hệ thống), lập sổ quyết định (docs/00-decision-register.md), master plan (docs/00-master-plan.md) và mục lục docs/README.md theo phương pháp "doc gate". Master plan liệt kê mọi tài liệu cần viết kèm nội dung bắt buộc và gate, mọi việc theo phase kèm tiêu chí nghiệm thu, ma trận truy vết. Dùng khi người dùng muốn "lập master plan từ SDD", "phân tích SDD", "tạo decision register", "chuẩn bị bộ docs cho dự án mới", hoặc cập nhật DR/plan sau khi Owner duyệt. Bước sau là skill docs-project.
argument-hint: "<đường dẫn SDD> | apply-decisions"
license: MIT
---

# SDD → Sổ quyết định + Master plan

Đầu vào: một file SDD ở gốc repo (gọi là **SDD gốc**). Đầu ra, theo thứ tự:

1. `docs/00-decision-register.md`: mọi chỗ SDD chưa nói "chính xác như thế nào", mỗi chỗ một DR kèm một phương án đề xuất.
2. `docs/00-master-plan.md`: tài liệu cần viết (nội dung bắt buộc, gate), lộ trình, việc từng phase, truy vết, quy ước, template.
3. `docs/README.md`: mục lục và bảng trạng thái.

Skill này **không** viết các DOC-xx; việc đó thuộc skill `docs-project`.

Tham chiếu (đọc trước khi viết phần tương ứng):

- [references/conventions.md](references/conventions.md): mã định danh, khối đầu file, trạng thái, quyết định, ngôn ngữ, văn phong. Đọc đầu tiên.
- [references/decision-register.md](references/decision-register.md): khung sổ quyết định và **danh sách soát khoảng trống**.
- [references/doc-catalog.md](references/doc-catalog.md): danh mục tài liệu chuẩn, điều kiện chọn, nội dung bắt buộc, gate mặc định.
- [references/master-plan.md](references/master-plan.md): khung master plan từng mục.
- [references/templates.md](references/templates.md): template A.1–A.7 cho phụ lục A, và B.6 cho README.
- `scripts/check_docs.py [docs_dir]`: kiểm tra mã định danh, link, khối trạng thái. Cần Python 3.10+. `<skill-dir>` trong các lệnh là thư mục chứa file SKILL.md này.

## Chế độ

- `/docs-master-plan <sdd.md>`: tạo mới (bước 1–7).
- `/docs-master-plan apply-decisions`: Owner đã trả lời các DR → bước 8.

## Quy trình

### 1. Kiểm tra trước

- Không có đường dẫn SDD thì tìm file `.md` lớn ở gốc repo có tiêu đề kiểu "Thiết kế hệ thống"/"System design"; không chắc thì hỏi.
- `docs/00-master-plan.md` hoặc `docs/00-decision-register.md` đã có thì **không ghi đè**. Hỏi người dùng: sửa bản hiện có hay dừng.
- Ngày trong mọi khối đầu file là ngày hôm nay.

### 2. Đọc toàn bộ SDD

Đọc hết, không lướt; file dài thì đọc theo đoạn tới cuối. Ghi chú nháp (scratchpad, không vào repo) **hồ sơ dự án**:

- Mục tiêu, câu hỏi nghiên cứu hoặc giá trị chính; phần nào là lõi không được cắt.
- Người dùng và role; FR và NFR (giữ nguyên mã nếu SDD đã đánh số).
- Thành phần, kho dữ liệu, kênh trao đổi (API, broker, file), hệ thống ngoài.
- Có UI không, AI không, thực nghiệm không, báo cáo đồ án không, môi trường triển khai nào.
- Kế hoạch, thứ tự cắt giảm và rủi ro mà SDD đã nêu.
- Mọi danh từ chuyên môn (đầu vào cho danh sách thuật ngữ tối thiểu của glossary).

### 3. Hỏi tối thiểu

Chỉ hỏi điều không suy ra được và làm thay đổi đầu ra. Dùng một lần AskUserQuestion, tối đa 3 câu:

- Ngôn ngữ của `docs/` (mặc định: ngôn ngữ của SDD; code, UI, commit bằng tiếng Anh).
- Phạm vi: làm đầy đủ hay đã biết phần sẽ cắt.
- Khi viết docs về sau, Claude có được tự chốt quyết định nhỏ không (người chốt ghi "Claude (Owner ủy quyền)").

Mọi lựa chọn kỹ thuật khác **không hỏi**: đưa vào sổ quyết định dưới dạng đề xuất.

### 4. Viết sổ quyết định

Theo `references/decision-register.md`. Đi qua SDD từng mục, áp danh sách soát khoảng trống, đọc kỹ để tìm cả mâu thuẫn bên trong SDD. Mỗi DR có quyết định đề xuất **cụ thể đến mức viết code được** (DDL, JSON, bảng, giá trị mặc định có đơn vị). Đánh dấu ⚠ khi lệch SDD, 🔬 khi cần spike. Mỗi DR có "Ghi vào" trỏ tới DOC/ADR sẽ có trong plan. Kết thúc bằng bảng "Tổng hợp theo mức ảnh hưởng". Trạng thái tài liệu: `Review`; mọi DR: `Đề xuất`.

File dài: viết khung trước, rồi thêm từng nhóm bằng Edit, không dồn vào một lần ghi.

### 5. Viết master plan

Theo `references/master-plan.md`, dùng `references/doc-catalog.md` để chọn tài liệu. Thứ tự viết: §1 (từ sổ quyết định) → §3 (cây và nội dung bắt buộc, cụ thể theo dự án) → §4 → §5 → §6 → §2, §7, §8, §9 → phụ lục A (từ `references/templates.md`).

Ràng buộc chéo phải giữ:

- Mỗi "Ghi vào" của DR trỏ tới một DOC có trong cây §3.1 hoặc một ADR trong bảng ADR.
- Mỗi DR cấp kiến trúc có một ADR; mỗi ADR có nguồn (DR hoặc SDD §).
- Mỗi DR 🔬 có một spike `S-xx` trong Phase 0.
- Mỗi phase có `Pn-00` doc gate liệt kê đúng các DOC/ADR có gate = Pn, và có tiêu chí thoát `Mn` kiểm chứng được.
- Mỗi việc trỏ tới DOC chứa thiết kế của nó; mỗi DOC thiết kế được ít nhất một việc dùng.
- Ma trận §6 có mọi FR và NFR; FR nào cũng có việc và cách kiểm chứng.
- Phase 0 có việc "Viết DOC-…" theo thứ tự: glossary → product → kiến trúc + ADR gate P1 → data → ops nền.

### 6. Viết `docs/README.md`

Theo template B.6. Mọi DOC ở trạng thái "Chưa viết".

### 7. Kiểm tra và báo cáo

- Chạy `python3 <skill-dir>/scripts/check_docs.py docs`. Sửa mọi E2 (link hỏng) và mọi E1 với mã do plan hoặc sổ quyết định định nghĩa (`DR-`, `DOC-`, `Pn-`, `S-`, `UC-`). E1 với mã sẽ được định nghĩa trong tài liệu chưa viết (`FR-xx.y`, `EXP-`, `E-`, `RB-`…) là bình thường ở bước này. Dòng I1 "DOC … without a file yet" chỉ là thông tin.
- Tự soát lại danh sách ràng buộc ở bước 5.
- Báo cáo ngắn: số DR (bao nhiêu ⚠, bao nhiêu 🔬), 5–8 khoảng trống nặng nhất, số DOC/ADR/phase/việc, các DR chặn P1 cần Owner xem trước. Bước tiếp theo: Owner duyệt DR (chấp nhận hết, hoặc nêu DR cần đổi) rồi chạy `/docs-master-plan apply-decisions`; sau đó dùng `/docs-project`.

Không commit trừ khi người dùng yêu cầu.

### 8. `apply-decisions`

Khi Owner trả lời:

- Mỗi DR được chốt: tiêu đề thêm `— **Chốt**` (hoặc `**Chốt: <lựa chọn>**`); DR bị đổi: ghi phương án mới vào mục Quyết định, giữ phương án cũ dạng "*Đổi YYYY-MM-DD:* …".
- Thêm dòng vào "Nhật ký chốt" (ngày, người chốt, nội dung, mục bị ảnh hưởng). Chấp nhận gộp thì ghi một dòng "Chấp nhận toàn bộ các đề xuất còn lại".
- Lan quyết định sang master plan (§1.2, §1.3, nội dung bắt buộc, việc, rủi ro) nếu nó làm thay đổi chúng.
- Khi mọi DR chặn P1 đã chốt và Owner duyệt plan: plan chuyển `Approved v1.0`, việc P0-01 ghi xong.
