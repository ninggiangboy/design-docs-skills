---
name: docs-system-design
description: Viết mới và chỉnh sửa qua nhiều lượt một SDD (tài liệu thiết kế hệ thống, dạng "Tên hệ thống — Thiết kế hệ thống"). Gồm bối cảnh, bài toán cốt lõi, mức đầu tư theo module, phạm vi, yêu cầu, kiến trúc, các mục miền đi sâu (bất biến, máy trạng thái, tranh chấp, phân tích phương án), dữ liệu, API, giao diện, chịu lỗi, thực nghiệm, kế hoạch, rủi ro. Dùng khi người dùng muốn viết SDD, thiết kế hệ thống từ một ý tưởng, hoặc sửa, thêm, bớt, đào sâu, rút gọn, rà soát một file SDD đã có, kể cả các yêu cầu sửa tiếp theo trong cùng phiên. Bước sau là skill docs-master-plan.
argument-hint: "[đường dẫn SDD] [mô tả ý tưởng hoặc yêu cầu sửa]"
license: MIT
---

# Viết và sửa SDD

SDD trả lời **hệ thống làm gì, vì sao thiết kế như vậy, và cơ chế lõi hoạt động thế nào**. Phần lõi phải đủ sâu để người đọc tin thiết kế đúng (câu SQL then chốt, máy trạng thái, tranh chấp, phương án bị loại). Phần phụ chỉ cần đủ để biết nó tồn tại và nối vào lõi ra sao. Đặc tả chi tiết (DDL đầy đủ, mọi endpoint, mọi màn hình) thuộc bộ docs sinh sau bằng `docs-master-plan` và `docs-project`.

Tham chiếu:

- [references/structure.md](references/structure.md): khung các mục, nội dung từng mục, biến thể theo loại dự án. Đọc trước khi viết mới.
- [references/style.md](references/style.md): văn phong, quy ước Mermaid, các mẫu trình bày (bảng bất biến, tranh chấp, phân tích phương án, bảng sự cố, thực nghiệm). Đọc trước khi viết hoặc sửa nội dung.
- [references/revision.md](references/revision.md): quy trình mỗi lượt sửa, loại yêu cầu, **bảng lan truyền thay đổi**, danh sách rà nhất quán. Đọc trước lượt sửa đầu tiên.
- `scripts/check_sdd.py <file> [--outline]`: kiểm tra số mục, tham chiếu `mục X.Y`, mã FR/NFR/UC/EXP, code fence, nhãn Mermaid. Cần Python 3.10+.

`<skill-dir>` trong các lệnh là thư mục chứa file SKILL.md này.

Người dùng có SDD mẫu ưng ý (của dự án trước) thì đọc đoạn cần thiết của nó để bắt độ sâu và giọng văn; khi mẫu và tham chiếu khác nhau về giọng văn, theo mẫu của người dùng.

## Chọn chế độ

- File SDD đích chưa có → **Viết mới**.
- File đã có, hoặc người dùng nói "sửa / thêm / bỏ / đào sâu / rút gọn / rà soát" → **Sửa**.
- Sau lượt đầu, **mọi yêu cầu tiếp theo về SDD trong phiên này đều theo chế độ Sửa**, không cần gọi lại skill. Mỗi lượt vẫn đọc lại file trước khi sửa.

Tên file mặc định: `<slug-du-an>-sdd.md` ở thư mục gốc repo hiện tại (hoặc thư mục người dùng chỉ định).

## Viết mới

### 1. Thu thập

Lấy từ tin nhắn, file đính kèm, ghi chú hoặc tài liệu người dùng chỉ ra. Cần đủ chín điều:

1. Hệ thống làm gì, cho ai, trong miền nào.
2. Loại dự án: đồ án/nghiên cứu, hay sản phẩm làm theo giai đoạn.
3. Bài toán cốt lõi (hoặc câu hỏi nghiên cứu) và bất biến quan trọng nhất.
4. Kịch bản quy mô mục tiêu có số.
5. Các module và module nào là trọng tâm.
6. Phạm vi: trong giai đoạn này, để sau, ngoài phạm vi.
7. Ràng buộc: số người, thời gian, máy chạy, môi trường triển khai, dịch vụ ngoài bắt buộc.
8. Ưu tiên công nghệ (nếu có).
9. Ngôn ngữ tài liệu (mặc định tiếng Việt) và tên tác giả (mặc định tên người dùng git).

Điều nào suy ra hợp lý được thì tự đề xuất và ghi là giả định. Chỉ hỏi những điều làm thay đổi thiết kế: một lần AskUserQuestion (tối đa 4 câu, có phương án đề xuất), hoặc một danh sách câu hỏi ngắn trong chat khi câu trả lời cần tự do.

### 2. Dàn ý để duyệt

Trừ khi người dùng bảo viết luôn hoặc đầu vào đã rất chi tiết, gửi dàn ý ngắn trong chat trước khi viết:

- tên và đoạn mở đầu nháp;
- bài toán cốt lõi (một câu) và bất biến số một;
- bảng mức đầu tư theo module;
- danh sách mục, mỗi mục một dòng nói sẽ có gì (mục lõi ghi rõ cơ chế và phương án sẽ phân tích);
- các giả định quan trọng.

Người dùng chỉnh dàn ý thì cập nhật rồi mới viết.

### 3. Viết

- Ghi khung file trước (khối đầu, mọi tiêu đề), rồi điền từng mục bằng Edit. Không dồn cả tài liệu vào một lần ghi.
- Thứ tự điền: mục 2 → 3 → 4 → các mục miền lõi → các mục miền còn lại → dữ liệu, API, giao diện → vận hành, kiểm thử → kế hoạch, rủi ro, phụ lục → **mục 1 và đoạn mở đầu viết cuối** để khớp với những gì đã thiết kế.
- Với mỗi mục lõi, trước khi viết hãy tự trả lời: bất biến là gì và ép ở đâu; hai luồng nào có thể tranh nhau và ai là trọng tài; request lặp, tiến trình chết giữa chừng, dịch vụ ngoài chậm hay lỗi thì sao; thời gian và đồng hồ lấy từ đâu; quy mô làm cơ chế ngây thơ hỏng ở chỗ nào; có phương án nào hiển nhiên mà bị loại; kiểm chứng bằng EXP nào. Câu trả lời trở thành nội dung của mục.
- Hành vi của dịch vụ ngoài (API thanh toán, SDK, giới hạn quota): không đoán. Kiểm tra tài liệu chính thức nếu có công cụ; không chắc thì ghi vào "Điểm còn mở".
- Mức chi tiết theo bảng 2.2: "Đào sâu" có sơ đồ, SQL/code, bảng quy tắc, edge case; "Mức cơ bản" chỉ một vài đoạn.

### 4. Kiểm tra và báo cáo

- Chạy `python3 <skill-dir>/scripts/check_sdd.py <file>` và sửa mọi lỗi E.
- Đi qua danh sách rà nhất quán (revision.md §4).
- Báo cáo ngắn: đường dẫn file, số mục và số sơ đồ, các giả định đã dùng, nội dung "Điểm còn mở", và 2–3 hướng nên làm ở lượt tiếp theo (ví dụ: đào sâu phương án X, thêm thực nghiệm cho tuyên bố Y, làm rõ tranh chấp Z). Không dán lại tài liệu vào chat.

## Sửa

Làm đúng quy trình ở [references/revision.md](references/revision.md) §1 cho **mỗi** yêu cầu:

1. Đọc lại các mục liên quan trong file (file có thể đã bị sửa tay).
2. Phân loại yêu cầu; yêu cầu mơ hồ thì đề xuất hướng cụ thể.
3. Lập danh sách chỗ bị ảnh hưởng bằng bảng lan truyền và `grep`.
4. Sửa tối thiểu, giữ văn phong và số mục, cập nhật mọi tham chiếu.
5. Chạy check_sdd.py.
6. Báo lại: đã đổi gì ở đâu, chỗ nào phải đổi theo, điều gì cần người dùng quyết.

Lượt đầu ở chế độ Sửa trên một file chưa đọc trong phiên: đọc toàn bộ file, chạy `check_sdd.py --outline`, rồi thực hiện yêu cầu. Không có yêu cầu cụ thể thì tóm tắt hiện trạng (dàn ý, lỗi kiểm tra, chỗ mỏng so với mức đầu tư, chỗ thiếu nhất quán) và đề xuất việc nên sửa.

Không commit trừ khi người dùng yêu cầu (quy ước commit ở revision.md §5).

## Khi SDD đã ổn

Gợi ý bước tiếp theo: `/docs-master-plan <file>` để lập sổ quyết định và master plan, rồi `/docs-project` để viết bộ tài liệu.
