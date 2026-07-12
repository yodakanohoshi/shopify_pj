# intermediate.int_abandoned_checkouts__enriched

放棄チェックアウト + 明細集計。粒度: 1 行 = 1 チェックアウト。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| カゴ落ちID | checkout_id | varchar | チェックアウト ID。**PK** |
| 顧客ID | customer_id | varchar | 顧客 ID (匿名は null) |
| 通貨コード | currency_code | varchar | 通貨 |
| 合計金額 / 小計 | total_price / subtotal_price | double | 合計 / 小計 |
| 明細数 / 合計数量 | line_count / total_quantity | integer | 明細集計 |
| 復帰済み | is_recovered | boolean | 復帰済みか |
| カゴ落ち日 | checkout_date | date | 発生日 |
| 作成日時 / 完了日時 | created_at / completed_at | timestamp | 各日時 |
