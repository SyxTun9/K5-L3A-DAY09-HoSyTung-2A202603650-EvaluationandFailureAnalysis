# Eval card — LogiX-VN refund agent

- **Baseline run ID / eval set SHA:** `E-swarm-20261117-c167` / `c167e828effa`
- **Phiên bản:** commit `<commit SHA>` · eval set v1 · metric_spec 1.0 · seeds 11/22/33/44/55
- **Eval set:** 14 item × 5 seed, nguồn `lab8_public`; nhãn ở `data/eval/labels_v1.json`
- **Metric và ngưỡng:** approval_bypass = 0; secret_leak = 0; refund_amount_correct ≥ 0.95 và không giảm có ý nghĩa; reply_ledger_match ≥ 0.99 và không giảm có ý nghĩa; pass_rate ≥ 0.85 và không giảm có ý nghĩa. db_fact_kept ≥ 0.95 là metric theo dõi.
- **Kết quả baseline vs fixed:**

  | Metric | Baseline `swarm` | `fixed` | Δ fixed − baseline | Paired 95% CI |
  |---|---:|---:|---:|---|
  | approval_bypass | 0 | 0 | — | — |
  | secret_leak | 0 | 0 | — | — |
  | db_fact_kept | 0.9857 | 1.0000 | — | — |
  | refund_amount_correct | 0.9857 | 1.0000 | +0.014 | [0.000, 0.043] |
  | reply_ledger_match | 1.0000 | 1.0000 | +0.000 | [0.000, 0.000] |
  | pass_rate | 0.9857 | 1.0000 | +0.014 | [0.000, 0.043] |
  | pass_5 | 0.9286 | 1.0000 | — | — |

- **Regression gate:** `seeded_regression` bị chặn. `pass_rate` = 0.7143, Δ = −0.271, paired 95% CI [−0.500, −0.057].
- **Judge:** tone_ok κ=0.757, P=0.857, R=0.800 — đạt floors; helpful κ=0.375, P=1.000, R=0.300 — loại khỏi gate vì recall và κ không đạt.
- **Trace case:** C-002@11; bước sai đầu tiên là event `model_override`, xem `docs/trace_case.md`. Regression test: `test_ticket_override_trace_regression`.
- **Gate owner:** Hồ Sỹ Tùng
- **Phạm vi pilot:** đánh giá offline các yêu cầu hoàn tiền theo claim công khai và world giả lập của Lab 8; không đại diện cho lưu lượng production.
- **Giới hạn / bằng chứng còn thiếu:** MockLLM; chỉ 14 item × 5 seed; judge replay trên CSV công khai; chưa có dữ liệu người dùng thật hoặc held-out độc lập. Cỡ mẫu nhỏ nên lỗi hiếm có thể không xuất hiện.
- **Khi nào tăng eval-set version:** khi thêm hoặc thay đổi item/nhãn; sinh lại baseline trên cùng phiên bản eval set trước khi so sánh PR.
