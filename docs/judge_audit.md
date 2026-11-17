# Judge audit

Chạy trên các replay công khai bằng `python -m lab9.judge --csv <file> --audit 5`.
Floors để dùng judge: κ ≥ 0.6, precision ≥ 0.8, recall ≥ 0.7.

## Hiệu chuẩn

| Tiêu chí | n | κ | Precision | Recall | Đạt floors? | Quyết định |
|---|---:|---:|---:|---:|---|---|
| tone_ok | 100 | 0.757 | 0.857 | 0.800 | Có | Dùng có giới hạn cho tone; tiếp tục spot-check nhãn |
| helpful | 100 | 0.375 | 1.000 | 0.300 | Không | Loại khỏi gate; recall thấp và κ không đạt |

Rogan–Gladen: `tone_ok` có fail rate quan sát 0.28, hiệu chỉnh 0.30; `helpful` có fail rate quan sát 0.09, hiệu chỉnh 0.30. Helpful bỏ sót 21/30 lỗi do người gán nhãn xác định, nên không thể làm gate dù precision là 1.0.

## Bất đồng đã audit

| # | Case | Judge nói | Người nói | Ai đúng? | Hành động sửa rubric/nhãn |
|---:|---|---|---|---|---|
| 1 | tone H-008 | PASS | FAIL | Người | Nêu rõ “em/nha” với khách là quá suồng sã; không để từ lịch sự đầu câu lấn át lỗi xưng hô cuối câu. |
| 2 | tone H-017 | PASS | FAIL | Người | Đánh giá cách xưng hô theo ngữ cảnh và tuổi khách; “bạn” không mặc nhiên phù hợp với khách lớn tuổi. |
| 3 | tone H-029 | PASS | FAIL | Người | Chấm toàn bộ câu trả lời; “không cần nhắn thêm” mang giọng ra lệnh dù mở đầu có “Dạ, vui lòng”. |
| 4 | tone H-042 | FAIL | PASS | Người | Không bắt buộc phải xin lỗi nếu câu ngắn vẫn đủ thông tin và phù hợp giọng điệu. |
| 5 | tone H-051 | FAIL | PASS | Người | Cho phép từ “refund” theo quy ước CS LogiX; không tự động xem từ tiếng Anh là lỗi tone. |
| 6 | tone H-081 | FAIL | PASS | Judge | Nhãn người bị đọc nhầm ticket; sửa nhãn sau khi đối chiếu ngữ cảnh, không sửa rubric để hợp thức hóa nhãn sai. |

## Kết luận

- Chỉ `tone_ok` đạt cả ba floors; nếu dùng, giới hạn nó vào chấm tone và tiếp tục kiểm tra mẫu bất đồng.
- Loại `helpful` khỏi release gate: recall 0.30 nghĩa là bỏ sót phần lớn lỗi; các tiêu chí về tiền và trạng thái phải chấm bằng code/ledger, không dựa vào judge văn bản.
- Dữ liệu là replay công khai, chưa phải held-out. Cần gán nhãn mới độc lập để kiểm tra khả năng khái quát và tiếp tục phát hiện nhãn người sai.
