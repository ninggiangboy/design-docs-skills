# Sửa SDD qua nhiều lượt

Một SDD tốt hình thành qua nhiều lượt trao đổi. Mỗi lượt sửa phải để lại một tài liệu **nhất quán từ đầu đến cuối**, chứ không chỉ đúng ở chỗ vừa sửa. Lỗi hay gặp nhất khi sửa lặp: đổi một quyết định ở mục lõi nhưng bảng NFR, sơ đồ kiến trúc, bảng sự cố, thực nghiệm, kế hoạch và rủi ro vẫn nói theo quyết định cũ.

## 1. Mỗi lượt sửa

1. **Đọc lại trạng thái hiện tại.** File có thể đã bị người dùng sửa tay giữa hai lượt. Luôn đọc lại các mục sẽ động tới (và `--outline` của check_sdd.py), không dựa vào bản trong trí nhớ.
2. **Phân loại yêu cầu** theo bảng ở §2. Yêu cầu mơ hồ ("nhạt quá", "chưa đủ sâu", "viết lại phần này cho hay hơn") thì đề xuất 2–3 hướng cụ thể và hỏi, hoặc chọn hướng hợp lý nhất và nói rõ đã chọn gì.
3. **Lập danh sách chỗ bị ảnh hưởng** bằng bảng lan truyền ở §3 cộng `grep` các từ khóa của quyết định cũ (tên bảng, tên trạng thái, con số, tên công nghệ, mã FR/NFR/EXP).
4. **Sửa tối thiểu.** Edit đúng các đoạn cần đổi; không viết lại mục không liên quan, không đổi văn phong những phần người dùng đã duyệt. Viết lại cả file chỉ khi người dùng yêu cầu tái cấu trúc.
5. **Giữ ổn định số mục và mã.** Thêm mục mới thì ưu tiên thêm cuối mục cha. Bắt buộc chèn giữa hoặc xóa mục thì đánh lại số và cập nhật **mọi** tham chiếu `mục X.Y`. Mã FR/NFR/UC/EXP đã cấp không đổi số; bỏ thì xóa dòng và mọi tham chiếu, thêm thì lấy số kế tiếp.
6. **Chạy** `python3 <skill-dir>/scripts/check_sdd.py <file>` và sửa mọi lỗi E.
7. **Báo lại ngắn**: đã đổi gì ở mục nào, những chỗ phải đổi theo (lan truyền), điều gì còn mở hoặc mâu thuẫn cần người dùng quyết. Không dán lại nội dung đã viết vào chat.

Yêu cầu mâu thuẫn với bất biến hoặc quyết định đã chốt trước đó (ví dụ "cho Redis giữ số vé" trong khi bất biến là không bán vượt): nói rõ mâu thuẫn và hệ quả, đề xuất cách đạt mục đích của người dùng mà không phá bất biến, chờ người dùng chọn.

## 2. Loại yêu cầu

| Loại | Ví dụ | Cách làm |
| --- | --- | --- |
| Đổi quyết định | "Dùng Kafka thay RabbitMQ", "giữ vé 15 phút" | Sửa chỗ định nghĩa, rồi lan truyền theo §3. Quyết định lớn thì cân nhắc thêm phân tích phương án |
| Thêm module / tính năng | "Thêm hoàn tiền", "thêm soát vé" | Hỏi mức đầu tư (2.2) và giai đoạn (trong phạm vi hay để sau). Trong phạm vi: theo hàng "Thêm module" ở §3 |
| Bỏ / dời sang để sau | "Bỏ phòng chờ khỏi giai đoạn này" | Chuyển sang bảng "Để sau" kèm cột "giai đoạn này xử lý thế nào"; gỡ khỏi mọi chỗ khác |
| Đào sâu một mục | "Phân tích thêm các phương án kho vé" | Dùng mẫu phân tích phương án; thêm EXP so sánh nếu tuyên bố cần số đo |
| Rút gọn | "Mục editor dài quá" | Giữ quy tắc, bất biến, quyết định và lý do; bỏ chi tiết cài đặt thuộc docs sau này |
| Sửa văn phong / trình bày | "Thêm sơ đồ", "đổi sang bảng" | Không đổi nội dung; kiểm tra sơ đồ khớp chữ |
| Sửa theo nhận xét review | Danh sách góp ý | Xử lý từng ý, báo lại theo từng ý: đã sửa ở đâu / không sửa vì sao |
| Rà nhất quán | "Kiểm tra lại toàn bộ" | Chạy check_sdd.py, rồi đọc lần lượt theo danh sách §4 |

## 3. Bảng lan truyền

Khi đổi ở cột trái, kiểm tra mọi mục ở cột phải.

| Thay đổi | Phải xem lại |
| --- | --- |
| Phạm vi (thêm, bớt, dời sang để sau) | Đoạn mở đầu, 1.3 Tầm nhìn, 2.2, 2.3, use case, FR, NFR, 4.1, sơ đồ kiến trúc, mục miền liên quan, mô hình dữ liệu, API, màn hình, triển khai, thực nghiệm, kế hoạch và thứ tự cắt giảm, demo, rủi ro, phụ lục repo |
| Thêm module | 2.2 (mức đầu tư), 2.3, use case, FR/NFR, 4.1, sơ đồ kiến trúc, 4.3 công nghệ, mục miền mới, thực thể và ràng buộc, endpoint, màn hình, container triển khai, bảng sự cố, kiểm thử/EXP, giai đoạn kế hoạch, rủi ro, phụ lục repo |
| Công nghệ / hạ tầng | 4.3, sơ đồ kiến trúc, 4.1, mọi mục miền nhắc tên công nghệ cũ (grep), triển khai, bảng sự cố, kiểm thử (công cụ), rủi ro, phụ lục repo, điểm còn mở |
| Cơ chế lõi (cách đảm bảo đúng đắn) | Mục miền lõi, 4.2 nguyên tắc, bảng bất biến, máy trạng thái và bảng chuyển, ràng buộc dữ liệu, mã lỗi API, bảng sự cố, kiểm tra bất biến, EXP và baseline, rủi ro |
| Vòng đời / trạng thái | `stateDiagram`, bảng chuyển, mọi câu SQL dùng tên trạng thái, ràng buộc/index một phần, API (trạng thái trả về), UI (hiển thị), job nền, kiểm tra bất biến |
| Con số (thời hạn, ngưỡng, quy mô tải) | Mọi chỗ có con số đó (grep cả dạng `10 phút`, `10 minutes`, `600`), NFR, tham số, ví dụ tính nhẩm, EXP, demo, rủi ro, điểm còn mở |
| Vai trò / quyền | 3.1, use case, bảng phân quyền, endpoint, màn hình, bảo mật |
| Thực thể / bảng | erDiagram, bảng thực thể, ràng buộc, các câu SQL, endpoint trả thực thể đó, phụ lục repo (module) |
| Endpoint | Bảng endpoint, ví dụ request/response, bảng lỗi, luồng có gọi endpoint (sequence), màn hình |
| Thực nghiệm | Bảng EXP, đoạn "EXP nào chứng minh gì", NFR nhắc EXP, mục miền nhắc EXP, kế hoạch (giai đoạn nào ra số liệu EXP nào) |
| Giai đoạn kế hoạch | Sơ đồ phụ thuộc, bảng giai đoạn, thứ tự cắt giảm, demo, bảng "Để sau" |

## 4. Danh sách rà nhất quán

- Đoạn mở đầu, 1.3, 2.1, 2.3 nói cùng một phạm vi.
- Mỗi module trong 2.2 có mục miền tương ứng với độ sâu đúng mức; mỗi thành phần ở 4.1 có trong sơ đồ kiến trúc và phụ lục repo.
- Mỗi NFR có chỉ tiêu số và ít nhất một EXP hoặc cách kiểm chứng; mỗi EXP được giai đoạn kế hoạch nào đó tạo số liệu.
- Mỗi trạng thái nhắc trong SQL/API/UI có trong máy trạng thái tương ứng, và ngược lại.
- Mọi công nghệ nhắc trong thân bài có trong 4.3.
- Bảng sự cố có mọi kho dữ liệu và dịch vụ ngoài trong sơ đồ kiến trúc.
- Rủi ro nào cũng có cách xử lý trỏ về mục thiết kế; "Điểm còn mở" phản ánh đúng những gì chưa chốt sau lượt sửa này.
- check_sdd.py không còn lỗi E.

## 5. Lịch sử thay đổi

- SDD không có mục changelog trong file; lịch sử nằm ở git.
- Nếu thư mục là git repo và người dùng yêu cầu commit: một commit cho mỗi thay đổi có nghĩa, tiêu đề `docs(sdd): <mô tả bằng tiếng Anh>` (ví dụ `docs(sdd): expand inventory design alternatives and selection rationale`). Không tự commit khi chưa được yêu cầu.
- Khi người dùng muốn so với bản trước: `git diff -- <file>` hoặc so với bản sao lưu người dùng chỉ ra.
