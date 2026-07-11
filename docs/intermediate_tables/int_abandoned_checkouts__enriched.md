# intermediate.int_abandoned_checkouts__enriched

放棄チェックアウト + 明細集計。粒度: 1 行 = 1 チェックアウト。

| カラム | 型 | 説明 |
|---|---|---|
| checkout_id | varchar | チェックアウト ID。**PK** |
| customer_id | varchar | 顧客 ID (匿名は null) |
| currency_code | varchar | 通貨 |
| total_price / subtotal_price | double | 合計 / 小計 |
| line_count / total_quantity | integer | 明細集計 |
| is_recovered | boolean | 復帰済みか |
| checkout_date | date | 発生日 |
| created_at / completed_at | timestamp | 各日時 |
