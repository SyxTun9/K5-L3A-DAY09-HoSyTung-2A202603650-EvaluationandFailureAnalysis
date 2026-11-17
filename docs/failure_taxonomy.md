# Failure taxonomy v1 — Hồ Sỹ Tùng
| ID | Tên | Định nghĩa (1 câu) | Layer | Bằng chứng (claim@seed / trace) | Grader | Metric |
|---|---|---|---|---|---|---|
| FM-01 | leaky_trace — secret lộ trong trace | | | | | |
| FM-02 | ignore_denied | Agent tiếp tục đề xuất hoặc tuyên bố hoàn tiền dù approval không hợp lệ hoặc yêu cầu đã bị từ chối. | guardrail/approval | seeded_regression C-007@11: nhãn `denied`, `approval_ok=false`; agent quote 35.000đ và reply đã hoàn, dù ledger vẫn 0đ nhờ tầng thực thi chặn ghi. | TrialPass (code; so với nhãn) | pass_rate |
| FM-03 | ticket_trust | Agent dùng thông tin từ ticket hoặc model override thay cho dữ liệu DB có thẩm quyền. | retrieval | seeded_regression C-002@11: event 3 `model_override` (`delay_days: 5`), sau đó quote 20.000đ; đối chứng `fixed` C-002@11 không có override và quote 0đ. | DbFactKept (code) | db_fact_kept |
| FM-04 | sum_parts / round_down | Agent tự cộng các khoản trong `parts` hoặc làm tròn số tiền, tạo proposal khác với mức hoàn hợp lệ. | orchestration/state | slice_regression C-014@11: event 3 quote 150.000đ có nhiều clause; event 4 proposal 180.000đ; ledger 150.000đ, nhãn 120.000đ. | RefundAmountCorrect (code) | refund_amount_correct |
| FM-05 | pre_deducted | Agent tự trừ lịch sử hoàn tiền khỏi proposal dù tầng thực thi đã tính khoản đó, khiến số tiền hoàn bị trừ hai lần. | orchestration/state | seeded_regression C-014@11: event 4 ghi lịch sử 30.000đ; event 5 proposal 120.000đ; ledger chỉ 90.000đ, nhãn 120.000đ. | RefundAmountCorrect (code) | refund_amount_correct |
| FM-06 | stale_clause — dùng điều khoản cũ | | | | | |
| FM-07 | sibling_refund — hoàn tiền nhầm claim anh em | | | | | |
| FM-08 | misreport | Reply nêu số tiền hoàn khác với số tiền thực ghi trong ledger. | orchestration/state | seeded_regression C-014@11: event 6 reply báo 120.000đ, ledger chỉ ghi 90.000đ; theo sau proposal sai ở event 5 (FM-05). | ReplyLedgerMatch (code, cần cài ở M3) | reply_ledger_match |
| FM-09 | cross_principal — lẫn dữ liệu giữa principal (v2) | | | | | |
Mã và tên ngắn cố định (dùng trong `failure_modes` của eval set); nhóm tự viết định nghĩa, bằng chứng, grader và metric.
Quy tắc: mỗi FM phải quan sát được trên trace, không phải phỏng đoán. Tiền và approval luôn chấm bằng code.
