# Trace case: ticket delay overrides the database fact

## Case

| Trường | Nội dung |
|---|---|
| Trial | `seeded_regression C-002@11`; run ID theo report tương ứng: `E-seeded_regression-20261117-c167` |
| Triệu chứng | Lab 8 grader báo `status resolved != denied`; ledger hoàn 20.000đ trong khi nhãn yêu cầu 0đ và `denied`. |
| Bước sai đầu tiên | Event 3, `model_override`: agent thay `delay_days` trong order view bằng số `5` lấy từ ticket. |
| Vì sao là bước đầu tiên | Event 2 là dữ liệu order lấy từ investigator; trước event 3 chưa có ghi đè. Event 4 quote 20.000đ và event 6 reply hoàn tiền là hậu quả của override. |
| Failure mode | FM-03 `ticket_trust`. |
| Đối chứng | `fixed C-002@11` không có `model_override`; quote 0đ, ledger 0đ và status `denied`, khớp nhãn. |
| Regression test | `test_ticket_override_trace_regression` trong `src/tests/test_lab9_graders.py`: xác nhận event override có ở `seeded_regression`, không có ở `fixed`, và `DbFactKept` phân loại cả hai đúng. |
| Chưa chắc chắn | Trace cho thấy agent đã dùng ticket thay cho fact DB; riêng trace này không chứng minh nguyên nhân nội bộ của model, chỉ xác định bước sai quan sát được. |

`FM-03` được chấm bằng code từ event `model_override`, không cần judge ngôn ngữ. Số tiền và trạng thái cuối được đối chiếu riêng với ledger và nhãn.
