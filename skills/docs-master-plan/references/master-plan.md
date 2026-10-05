# Blueprint: `docs/00-master-plan.md`

Mục tiêu của master plan: **khi một việc được bắt đầu, mọi thông tin cần để làm nó đã nằm trong docs, không phải hỏi thêm.** Plan nói *tài liệu nào phải có, mỗi tài liệu chứa gì, việc nào làm khi nào, xong thế nào thì được coi là xong*. Plan không chứa thiết kế chi tiết; thiết kế nằm trong DR và các DOC.

Bản đầu tiên là `Review`. Owner duyệt thì thành `Approved v1.0`.

## Khối đầu

```markdown
# Master Plan: xây dựng <Tên dự án> từ đầu đến cuối

> Trạng thái: **Review** · Cập nhật: YYYY-MM-DD · Đi kèm: [00-decision-register.md](00-decision-register.md) · Nguồn: `<sdd>.md` (**SDD gốc**)

Tài liệu này là bản hướng dẫn tổng. Nó gồm:

1. các điểm cần bổ sung sau khi phân tích SDD gốc,
2. **toàn bộ tài liệu cần viết** trong `docs/` (mỗi tài liệu phải chứa gì và cần xong trước phase nào),
3. **toàn bộ công việc triển khai** chia theo phase, mỗi việc có đầu ra và tiêu chí nghiệm thu,
4. ma trận truy vết từ yêu cầu tới công việc và cách kiểm chứng.

Mục tiêu: khi một việc được bắt đầu, mọi thông tin cần để làm nó đã nằm trong docs. Không phải hỏi thêm.
```

## §0. Cách dùng tài liệu này

- Thứ tự đọc cho người mới: §1 → §4 → phase đang làm ở §5 → tài liệu phase đó tham chiếu.
- **Quy tắc doc gate:** mỗi phase có việc `Pn-00` rà soát tài liệu; phase chỉ bắt đầu khi tài liệu nó cần đã `Approved` (§3.3).
- Bảng mã định danh (chép từ conventions.md §1, chỉ giữ tiền tố dự án dùng, thêm tiền tố riêng nếu có).
- Vòng đời trạng thái tài liệu.

## §1. Phân tích SDD gốc

### 1.1 Những gì đã tốt, giữ nguyên
5–8 gạch đầu dòng, cụ thể (không khen chung chung). Đây là phần plan cam kết không đổi.

### 1.2 Khoảng trống chính
Bảng `# · Khoảng trống · Hệ quả nếu để nguyên · DR`, 8–15 dòng nặng nhất lấy từ sổ quyết định. Cột hệ quả phải nói hậu quả thật ("replay sinh bản ghi mới, phá idempotency"), không nói "chưa rõ".

### 1.3 Điều chỉnh so với kế hoạch trong SDD gốc
Bảng `Điều chỉnh · Lý do`. Luôn có dòng **thêm Phase 0: đặc tả và spike**. Các điều chỉnh thường gặp: dời việc bị phụ thuộc ngược phase; CI tối thiểu từ P1; bảng/thành phần phải thêm để luồng SDD mô tả chạy được; thay công cụ nặng bằng cái nhẹ hơn; dùng framework có sẵn thay vì tự xây.

## §2. Nguyên tắc thực hiện

5–8 nguyên tắc đánh số, rút từ trọng tâm của SDD. Luôn có:
1. Phần lõi (trả lời câu hỏi nghiên cứu / giá trị chính) đúng trước, đầy đủ sau; phase lõi không được cắt.
2. Mỗi phase kết thúc bằng thứ chạy được và demo được (milestone).
3. Tài liệu đi cùng code: đổi hành vi thì sửa doc trong cùng PR; đổi quyết định thì ADR mới.
4. Mọi ngưỡng nằm trong cấu hình, mọi cấu hình có trong configuration-reference.

Thêm nguyên tắc riêng của dự án (ví dụ: "ranh giới transaction được chứng minh bằng test tiêm lỗi trước khi viết job thật", "mọi kết quả tính toán phải idempotent và có test chạy hai lần").

## §3. Bộ tài liệu cần viết

### 3.1 Cây thư mục `docs/`
Một code block dạng cây, mỗi file có comment `# DOC-xx` (script kiểm tra đọc mã DOC từ đây). Dựng từ doc-catalog.md.

### 3.2 Nội dung bắt buộc của từng tài liệu
"Cột Gate là phase cần tài liệu Approved trước khi bắt đầu." Mỗi nhóm một bảng `DOC · Tài liệu · Nội dung bắt buộc · Gate`. Nhóm design có đoạn nêu **khung chung**. ADR có bảng riêng `ADR · Chủ đề · Nguồn · Gate`.

Nội dung bắt buộc phải **cụ thể theo dự án**: liệt kê tên bảng cần DDL, tên luồng cần sequence diagram, tên job, tên màn hình, danh sách thuật ngữ tối thiểu của glossary, mã DR áp dụng, chỉ tiêu coverage. Chữ **đậm** cho phần dễ bị bỏ sót nhất.

### 3.3 Định nghĩa "Approved"
Checklist năm điều (conventions.md §3).

### 3.4 Danh sách use case
Bảng `UC · Tên · Actor chính · FR`. Gồm UC của người dùng và UC của hệ thống (scheduler, tự động hóa) và của người vận hành/nghiên cứu.

## §4. Lộ trình

### 4.1 Tổng quan các phase
Bảng `Phase · Tên · Ước lượng (1 người, toàn thời gian) · Milestone`. Milestone `Mn` là câu kiểm chứng được ("`make up` chạy; event lên Kafka; raw zone có file"). Dòng tổng, và hệ số nếu làm bán thời gian. Ghi "con số chỉ để lập kế hoạch, hiệu chỉnh sau mỗi milestone".

Khung phase mặc định (gộp, tách, đổi tên theo SDD; giữ phase của SDD nếu SDD đã có kế hoạch):

| Phase | Nội dung điển hình |
| --- | --- |
| P0 | Đặc tả, chốt DR, spike, viết tài liệu gate P1 |
| P1 | Nền tảng: repo, build, CI tối thiểu, hạ tầng local, migration, nguồn dữ liệu/giả lập |
| P2 | Lõi của hệ thống (phần trả lời câu hỏi nghiên cứu / giá trị chính) |
| P3 | Độ tin cậy, observability, thực nghiệm cho lõi |
| P4 | Nghiệp vụ/analytics và API |
| P5 | Giao diện |
| P6 | Tính năng nâng cao (AI…) |
| P7 | Scale, k8s, chịu lỗi |
| P8 | Hoàn thiện: bảo mật, tài liệu, demo, release |

### 4.2 Phụ thuộc giữa các phase
Mermaid `flowchart LR`, kèm một đoạn: phase nào song song được nếu có hai người.

### 4.3 Thứ tự cắt giảm khi thiếu thời gian
Một dòng, theo thứ tự cắt trước → cắt sau, mỗi mục ghi mã việc. Ghi rõ phần **không được cắt**. Ghi điều kiện kích hoạt (ví dụ milestone trễ > 50%).

## §5. Chi tiết công việc từng phase

"Mỗi bảng có các cột: **ID · Việc · Đầu ra và tiêu chí nghiệm thu · Phụ thuộc · Tài liệu**."

Mỗi phase:

```markdown
### Phase n: <Tên>

Mục tiêu: <một câu>.   (tùy chọn)

| ID | Việc | Đầu ra và nghiệm thu | Phụ thuộc | Tài liệu |
| --- | --- | --- | --- | --- |
| Pn-00 | Doc gate: DOC-…; ADR … | Approved | M(n-1) | — |
| Pn-01 | <việc cụ thể, nêu tên class/job/bảng/lệnh> | <đầu ra kiểm chứng được: lệnh nào chạy ra gì, test nào pass, con số nào> | Pn-xx | DOC-xx |

**Tiêu chí thoát (Mn):** <các kiểm tra tay/tự động, có số liệu>.
```

Quy tắc cho việc:
- Một việc ≈ 0,5–3 ngày công, kết thúc bằng một commit/PR trọn vẹn.
- Cột nghiệm thu là **phép thử**, không phải mô tả: "Test: 1 record lỗi trong chunk 500 → 499 dòng được ghi, 1 dòng DLQ", "`docker compose up` → mọi container healthy ≤ 3 phút", "coverage ≥ 90%".
- Cột Tài liệu trỏ tới DOC chứa thiết kế của việc đó. Việc không có DOC thiết kế là dấu hiệu thiếu tài liệu.
- Phase 0 gồm: P0-01 duyệt sổ quyết định; mỗi spike `S-xx` một việc (đầu ra: ghi chú spike + bằng chứng, cập nhật DR/ADR/DOC nào); các việc "Viết DOC-…" theo thứ tự §9. Tiêu chí thoát M0: mọi tài liệu gate P1 Approved, spike chặn P1 có kết luận.
- Phase cuối có việc tag release.

## §6. Ma trận truy vết

Bảng `Yêu cầu · Tài liệu thiết kế · Công việc · Kiểm chứng`, một dòng cho **mọi** FR và NFR (và quyết định kiến trúc lớn nếu có). Không FR nào thiếu việc; không NFR nào thiếu cách kiểm chứng.

## §7. Quy ước làm việc

- 7.1 Definition of Ready: tài liệu tham chiếu Approved; không còn DR liên quan ở `Đề xuất`; có tiêu chí nghiệm thu đo được; việc phụ thuộc đã Done.
- 7.2 Definition of Done: merge + CI xanh; có test cho hành vi mới, bug fix có test tái hiện; metric/log/cấu hình mới đã vào tài liệu nguồn; tài liệu cập nhật trong cùng PR; chạy được bằng lệnh khởi động chuẩn (nếu có runtime). Thêm điều kiện riêng của dự án (luật kiến trúc…).
- 7.3 Git và code: nhánh, Conventional Commits, ngôn ngữ (conventions.md §5), PR template, formatter, quy ước migration.

## §8. Rủi ro bổ sung (ngoài phần rủi ro của SDD)

Bảng `Rủi ro · Dấu hiệu sớm · Xử lý`. Mỗi spike và mỗi phụ thuộc bên ngoài (SDK, dịch vụ, image, phiên bản mới) thường kéo theo một rủi ro. Cột xử lý nêu phương án lùi cụ thể.

## §9. Bắt đầu ngay: 10 việc đầu tiên

Danh sách đánh số: chốt DR chặn P1/P2 → chạy spike song song → viết glossary → requirements và use case → kiến trúc và ADR gate P1 → mô hình dữ liệu có DDL chạy thử → tài liệu ops nền → duyệt M0 → bắt đầu P1 → tài liệu của P2 viết song song với P1.

## Phụ lục A: Template dùng chung

Chép các template từ templates.md (A.1 ADR, A.2 use case, A.3 yêu cầu, A.4 endpoint, A.5 màn hình, A.6 thực nghiệm, A.7 runbook). Bỏ template của nhóm tài liệu không áp dụng; thay ví dụ bằng ví dụ của dự án.

---

## Cập nhật plan khi đã triển khai (để biết, không làm ở bước tạo plan)

- Việc xong: thêm `— **Xong YYYY-MM-DD** (\`sha\`)` vào cột Việc; lệch tài liệu thì thêm `(… lệch nhẹ tài liệu, DR-xx)`.
- Milestone đạt: thêm đoạn `**Mn đạt ngày YYYY-MM-DD.**` với môi trường đo và bảng `Tiêu chí · Kết quả` có số thật.
- Spike xong: gạch tiêu đề cũ, ghi kết quả và DR/ADR mới.
- Rủi ro đã xảy ra: gạch, ghi "Đã xảy ra, đã xử lý YYYY-MM-DD" và cách xử lý.
